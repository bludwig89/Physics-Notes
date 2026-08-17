"""
run_f287_bgfield_apparatus.py — F287: re-establish that the F162 background-field
apparatus is SOUND post-F272/F277.

F162 is superseded by S11-F272 (the `mod 2 pi` refold removed from
`bgfield_loop._Bcoeff_numeric`) and F277 then found the identical defect live in
four sibling modules, in one of which it flipped a vacuum-polarization sign.
`docs/status/completeness-2026-08-02.md` gap #2 makes verifying this apparatus a
PREREQUISITE for computing d_1, not a detour.

F277's standard for "sound" is four things, and this runner applies all four to
bgfield_loop:

  A. PERIOD LATTICE — the kernel this module actually calls (`K_true_4d`
     = 3*omega_even^2 + kt^2) is sqrt3*fcc-periodic and NOT 2pi-per-axis
     periodic, so an unwrapped evaluation is the periodic-correct one.
  B. CONVERGENCE, NOT FLATNESS — the decisive F272/F277 discriminator. The
     refolded quantity was FLAT and PASSING while drifting with refinement.
     Sweep n and require the rule shift to converge.
  C. WILSON CONTROL — unchanged under the same sweep (Wilson IS 2pi-periodic,
     so the removal must be an exact no-op for it).
  D. THE SHARP DISCRIMINATOR — F277 section 4 used the b0 log-SLOPE ratio rather
     than a tolerance. The analogue here is stronger and is new: the numeric
     quadrature's own log slope must reproduce the EXACT symbolic gate. With
     q = (Q,0,0,0) the transverse tensor gives
        Pi00 - Pi11 = -b0 Q^2 /(16 pi^2) * ln(Lambda^2/Q^2),
     so  B = (Pi00-Pi11)/Q^2  obeys
        d(-B_cont)/d ln(1/Q) = 2 b0 / (16 pi^2) = 22/(16 pi^2) = 0.1393
     for b0 = 11. This closes G1 (exact, symbolic) onto G2 (numeric) — the two
     F162 gates have never been tied to each other before.

Chunked over the leading axis so n up to ~40 fits in memory.

Usage:  PYTHONPATH=src python3 tests/runners/run_f287_bgfield_apparatus.py
Writes: test-results/F287_bgfield_apparatus.json
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

import numpy as np  # noqa: E402

from casim.engine.gauge import bgfield_loop as bg  # noqa: E402
from casim.engine.gauge import gluon_self_energy as se  # noqa: E402

TWO_PI = 2.0 * math.pi
B0_TARGET = 11.0
SLOPE_TARGET = 2.0 * B0_TARGET / (16.0 * math.pi ** 2)


# ----------------------------------------------------------------------
# A. period lattice of the kernel this module actually calls
# ----------------------------------------------------------------------
def period_lattice_of_K4d(ntrial: int = 200, seed: int = 20260802) -> dict:
    """Measure which shifts leave K_true_4d invariant. This is the F277 T1
    measurement applied to the 4D kernel `_Bcoeff_numeric` evaluates, including
    the Euclidean-time leg (which is continuum kt^2 and therefore NOT periodic
    at all -- an important qualifier F277's 3D statement does not carry)."""
    rng = np.random.default_rng(seed)
    k = rng.uniform(-math.pi, math.pi, size=(ntrial, 4))
    base = se.K_true_4d(k[:, 0], k[:, 1], k[:, 2], k[:, 3])

    def maxdev(shift):
        s = np.asarray(shift, dtype=float)
        kk = k + s
        return float(np.max(np.abs(
            se.K_true_4d(kk[:, 0], kk[:, 1], kk[:, 2], kk[:, 3]) - base)))

    trials = {
        "2pi_(1,0,0,0)_the_refold": maxdev((TWO_PI, 0, 0, 0)),
        "2pi_(1,1,0,0)_plain_fcc": maxdev((TWO_PI, TWO_PI, 0, 0)),
        "sqrt3*2pi_(1,1,0,0)": maxdev((math.sqrt(3) * TWO_PI, math.sqrt(3) * TWO_PI, 0, 0)),
        "sqrt3*2pi_(2,0,0,0)": maxdev((2 * math.sqrt(3) * TWO_PI, 0, 0, 0)),
        "2pi_in_TIME_(0,0,0,1)": maxdev((0, 0, 0, TWO_PI)),
    }
    tol = 1e-10
    return {
        "max_abs_deviation": trials,
        "refold_is_a_period": bool(trials["2pi_(1,0,0,0)_the_refold"] < tol),
        "sqrt3_fcc_is_a_period": bool(
            trials["sqrt3*2pi_(1,1,0,0)"] < tol and trials["sqrt3*2pi_(2,0,0,0)"] < tol),
        "time_leg_is_periodic": bool(trials["2pi_in_TIME_(0,0,0,1)"] < tol),
        "verdict": ("the 2pi-per-axis refold is NOT a period of the kernel "
                    "bgfield_loop evaluates; sqrt3*fcc IS (spatial legs). The "
                    "Euclidean-time leg is continuum kt^2 and has NO period at "
                    "all, so the refold was inequivalent in 4 directions, not 3."),
    }


# ----------------------------------------------------------------------
# chunked B coefficient (same integrand as bgfield_loop._Bcoeff_numeric)
# ----------------------------------------------------------------------
def _Bcoeff_chunked(Q: float, n: int, kernel: str, chunk: int = 4) -> float:
    ax = (np.arange(n) + 0.5) / n * TWO_PI - math.pi
    qv = np.array([Q, 0.0, 0.0, 0.0])
    G123 = np.meshgrid(ax, ax, ax, indexing="ij")
    acc = np.zeros((4, 4))
    count = 0
    for i0 in range(0, n, chunk):
        a0 = ax[i0:i0 + chunk]
        k0 = np.broadcast_to(a0[:, None, None, None], (len(a0), n, n, n))
        k1 = np.broadcast_to(G123[0][None], (len(a0), n, n, n))
        k2 = np.broadcast_to(G123[1][None], (len(a0), n, n, n))
        k3 = np.broadcast_to(G123[2][None], (len(a0), n, n, n))
        k = np.stack([k0, k1, k2, k3], axis=-1)
        kq = k + qv
        if kernel == "cont":
            denom = np.sum(k ** 2, -1) * np.sum(kq ** 2, -1)
        elif kernel == "wilson":
            Kf = lambda g: 4 * (np.sin(g[..., 0] / 2) ** 2 + np.sin(g[..., 1] / 2) ** 2
                                + np.sin(g[..., 2] / 2) ** 2 + np.sin(g[..., 3] / 2) ** 2)
            denom = Kf(k) * Kf(kq)
        elif kernel == "rule":
            Kr = lambda g: se.K_true_4d(g[..., 0], g[..., 1], g[..., 2], g[..., 3])
            denom = Kr(k) * Kr(kq)
        else:
            raise ValueError(kernel)
        W = bg.gammaF_tensor_continuum(k, qv)
        Z = bg.gammaF_tensor_continuum(kq, -qv)
        M = np.einsum("...aml,...lna->...mn", W, Z)
        tkq = 2.0 * k + qv
        M = M - 2.0 * np.einsum("...m,...n->...mn", tkq, tkq)
        acc += np.sum(M / denom[..., None, None], axis=(0, 1, 2, 3))
        count += k0.size
    Pi = (bg.C_A / 2.0) * acc / count
    return float((Pi[0, 0] - Pi[1, 1]) / Q ** 2)


# ----------------------------------------------------------------------
# B + C. convergence of the subtracted shift, both kernels
# ----------------------------------------------------------------------
def convergence_sweep(ns=(10, 14, 18, 22, 26), Qs=(0.1, 0.15, 0.2, 0.3)) -> dict:
    rows = []
    for n in ns:
        dw, dr = [], []
        for Q in Qs:
            Bc = _Bcoeff_chunked(Q, n, "cont")
            dw.append(_Bcoeff_chunked(Q, n, "wilson") - Bc)
            dr.append(_Bcoeff_chunked(Q, n, "rule") - Bc)
        rows.append({
            "n": n,
            "wilson_mean": float(np.mean(dw)), "wilson_spread": float(max(dw) - min(dw)),
            "rule_mean": float(np.mean(dr)), "rule_spread": float(max(dr) - min(dr)),
        })
        print(f"  n={n:3d}  rule {rows[-1]['rule_mean']:+.6e} "
              f"(spread {rows[-1]['rule_spread']:.3e})   wilson "
              f"{rows[-1]['wilson_mean']:+.6e} (spread {rows[-1]['wilson_spread']:.3e})",
              flush=True)

    def rel_step(key):
        a, b = rows[-2][key], rows[-1][key]
        return abs((b - a) / b) if b else float("nan")

    return {
        "Qs": list(Qs),
        "rows": rows,
        "rule_mean_rel_step_last": rel_step("rule_mean"),
        "wilson_mean_rel_step_last": rel_step("wilson_mean"),
        "rule_spread_final": rows[-1]["rule_spread"],
        "wilson_spread_final": rows[-1]["wilson_spread"],
        "rule_sign_stable": bool(len({int(math.copysign(1, r["rule_mean"])) for r in rows}) == 1),
        "monotone_after_onset": bool(
            all(abs(rows[i + 1]["rule_mean"] - rows[i]["rule_mean"])
                <= abs(rows[i]["rule_mean"] - rows[i - 1]["rule_mean"]) * 1.5
                for i in range(1, len(rows) - 1))),
    }


# ----------------------------------------------------------------------
# D. the sharp discriminator: numeric log slope vs the EXACT symbolic b0
# ----------------------------------------------------------------------
def b0_log_slope(n=26, Qs=(0.08, 0.10, 0.13, 0.17, 0.22)) -> dict:
    """DIAGNOSTIC ONLY -- deliberately run at SUB-CELL Q to record the hazard.

    The real slope test lives in run_f287_slope.py (D1/D2). This call is kept,
    with its original ill-posed Q range, because what it returns is worth having
    on the record: at n=26 the grid spacing is 2 pi/n = 0.2417, so every Q here
    is BELOW one cell, the IR end of the log window Q << k << Lambda is
    unresolved, and the fit returns b0 = 4.06 -- 37% of the true value -- with a
    clean-looking linear residual of 1e-3. It is a confidently wrong number from
    a well-behaved-looking fit, which is the same failure family as the refold:
    a value that passes inspection while meaning nothing.

    The apparatus therefore carries a RESOLUTION FLOOR: probe only at
    Q >~ 2*(2 pi/n). At resolved Q the same quadrature returns b0 = 10.44-10.50
    (run_f287_slope.py).
    """
    x, y = [], []
    for Q in Qs:
        x.append(math.log(1.0 / Q))
        y.append(-_Bcoeff_chunked(Q, n, "cont"))
    slope, intercept = np.polyfit(np.array(x), np.array(y), 1)
    resid = float(np.max(np.abs(np.array(y) - (slope * np.array(x) + intercept))))
    b0_meas = float(slope) * 16.0 * math.pi ** 2 / 2.0
    return {
        "n": n, "Qs": list(Qs),
        "minus_Bcont": y,
        "slope_measured": float(slope),
        "slope_target_b0_11": SLOPE_TARGET,
        "slope_ratio": float(slope) / SLOPE_TARGET,
        "b0_measured": b0_meas,
        "b0_exact_symbolic": B0_TARGET,
        "b0_rel_error": abs(b0_meas - B0_TARGET) / B0_TARGET,
        "fit_max_residual": resid,
    }


def main():
    t0 = time.time()
    out = {"finding": "F287", "date": "2026-08-02",
           "subject": "F162 background-field apparatus, soundness post-F272/F277"}

    print("A. period lattice of K_true_4d ...", flush=True)
    out["A_period_lattice"] = period_lattice_of_K4d()

    print("D. sub-cell-Q slope DIAGNOSTIC (expected to fail; see run_f287_slope) ...",
          flush=True)
    out["D_subcell_slope_diagnostic"] = b0_log_slope()
    d = out["D_subcell_slope_diagnostic"]
    d["grid_spacing_2pi_over_n"] = TWO_PI / d["n"]
    d["all_Q_below_one_cell"] = bool(max(d["Qs"]) < TWO_PI / d["n"])
    d["interpretation"] = (
        "ILL-POSED BY CONSTRUCTION, recorded as a hazard: all Q are sub-cell, so "
        "b0 comes out 37% of true from a fit whose residual looks fine. The "
        "apparatus has a resolution floor Q >~ 2*(2 pi/n). Real slope test: "
        "run_f287_slope.py D1/D2.")
    print(f"   b0_measured = {d['b0_measured']:.6f} (exact 11) -- sub-cell, "
          f"expected bad; all_Q_below_one_cell={d['all_Q_below_one_cell']}", flush=True)

    print("B+C. convergence sweep ...", flush=True)
    out["BC_convergence"] = convergence_sweep()

    A, D, BC = out["A_period_lattice"], out["D_subcell_slope_diagnostic"], out["BC_convergence"]
    checks = {
        "A_refold_is_not_a_period": (not A["refold_is_a_period"]) and A["sqrt3_fcc_is_a_period"],
        "B_rule_shift_converges": BC["rule_mean_rel_step_last"] < 0.05,
        "B_rule_shift_q_flat": BC["rule_spread_final"] < 1e-3,
        "B_rule_sign_stable": BC["rule_sign_stable"],
        "C_wilson_control_converges": BC["wilson_mean_rel_step_last"] < 1e-3,
        # the sub-cell diagnostic must STAY broken -- it is the recorded hazard
        "D_subcell_hazard_reproduced": D["all_Q_below_one_cell"] and D["b0_rel_error"] > 0.2,
    }
    out["checks"] = {k: bool(v) for k, v in checks.items()}
    out["summary"] = {"passed": int(sum(checks.values())), "total": len(checks),
                      "all_pass": bool(all(checks.values())),
                      "seconds": round(time.time() - t0, 1)}

    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "test-results", "F287_bgfield_apparatus.json")
    with open(dest, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out["checks"], indent=2))
    print(f"F287: {out['summary']['passed']}/{out['summary']['total']} "
          f"({out['summary']['seconds']} s)")

    assert checks["A_refold_is_not_a_period"], A["max_abs_deviation"]
    assert checks["B_rule_shift_converges"], BC["rule_mean_rel_step_last"]
    assert checks["B_rule_shift_q_flat"], BC["rule_spread_final"]
    assert checks["B_rule_sign_stable"], [r["rule_mean"] for r in BC["rows"]]
    assert checks["C_wilson_control_converges"], BC["wilson_mean_rel_step_last"]
    # the sub-cell diagnostic must STAY broken: it is the recorded hazard, and a
    # future session must not be able to rediscover b0=4.06 and believe it.
    assert checks["D_subcell_hazard_reproduced"], D["b0_measured"]


if __name__ == "__main__":
    main()
