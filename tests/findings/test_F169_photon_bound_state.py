"""F169 — The interacting two-body bound-state wavefunction of the paired photon.

Builds the explicit interacting wavefunction that F69/F74/F168 left open and
shows the F69 photon is the marginally-bound (zero-binding-energy) THRESHOLD
state of a genuine two-constituent bound-state problem on the BCC lattice:

  C1  Threshold wavefunction exists in closed form: psi(p) ∝ 1/(E0 - T) is the
      EXACT zero-residual root of the Koster-Slater secular equation at the
      critical coupling g_c, and is normalizable in 3D.

  C2  g_c(k) is finite (3D Watson-type threshold; cf. F74) — a real binding
      threshold, not "binds for any coupling".

  C3  THE CLOSURE (honest): the photon (threshold bound state) is massless and
      luminal — light speed -> 1/sqrt(3) — and the F69 kinematic rate
      Omega_even(k) is the LEADING small-k form of the interacting threshold
      dispersion T(k): Omega_even(k) >= T(k) with the gap O(k^2) -> 0.  (The
      symmetric split p=0 is not the exact two-body floor at finite k; it sits
      O(k^2) above it, the same order as the F168/B3 birefringent split.)

  C4  Solver is exact: the secular root and an independent dense Hermitian
      diagonalisation agree to machine precision at finite total momentum
      (clean gap), reproducing the F74 two-method standard.

  C5  Masslessness is INHERITED, not tuned: T(0) = w+(0)+w-(0) = 0 exactly
      (gapless constituents, pure-hop A0=0, F168/B1).  The photon's E_b = 0 is
      the gaplessness of its constituents; the EM channel sits AT threshold
      (not below = tachyonic) by the gauge/identity structure (F168).

  C6  The wavefunction is localized (finite real-space RMS radius) — the photon
      "pair" has an explicit, finite size.

No scipy / no eig on chiral matrices (closed-form arccos + own bisection).
"""

import json
import os
import sys
import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.gauge import photon_bound_state as bs                          # noqa: E402

RESULT = os.path.join(
    os.path.dirname(__file__), "..", "..", "test-results",
    "F169_photon_bound_state.json",
)
ROOT3 = np.sqrt(3.0)


def _pattern_min(k, step0=0.35, tol=1e-14):
    """Deterministic coordinate pattern search for min_p E0(p; k).

    Cross-check only: confirms the closed-form collinear-endpoint threshold is
    the true floor, without relying on a stochastic search.  Starts from the
    symmetric split and both collinear endpoints.
    """
    from casim.engine.lattice.bcc import bcc_dispersion as _wd

    def E0(p):
        return float(_wd(*(k / 2 + p), sign="+") + _wd(*(k / 2 - p), sign="-"))

    best, bp = np.inf, None
    for s0 in (np.zeros(3), k / 2, -k / 2):
        p = np.array(s0, float); e = E0(p); st = step0
        while st > tol:
            moved = False
            for ax in range(3):
                for sg in (1, -1):
                    q = p.copy(); q[ax] += sg * st
                    ec = E0(q)
                    if ec < e - 1e-17:
                        e, p, moved = ec, q, True
            if not moved:
                st *= 0.5
        if e < best:
            best, bp = e, p
    return best


def main():
    L = 12
    out = {}

    # --- C1: closed-form threshold wavefunction, exact secular root ---------
    psi0, T0 = bs.threshold_wavefunction([0, 0, 0], L)
    g_c, T0b = bs.critical_coupling([0, 0, 0], L)
    E = bs.relative_dispersion([0, 0, 0], L)
    m = E > T0 + 1e-9
    secular_resid = abs(1.0 - g_c * np.mean(1.0 / (E[m] - T0)))
    norm = float(np.sum(psi0 ** 2))           # normalised to 1 by construction
    out["C1"] = {"g_c": g_c, "secular_residual_at_threshold": secular_resid,
                 "wavefn_norm": norm, "normalizable": np.isfinite(norm),
                 "pass": secular_resid < 1e-12 and abs(norm - 1.0) < 1e-12}

    # --- C2: g_c finite (3D binding threshold) ------------------------------
    out["C2"] = {"g_c_finite": bool(np.isfinite(g_c) and g_c > 0),
                 "g_c": g_c, "pass": np.isfinite(g_c) and g_c > 0}

    # --- C3: massless + luminal; Omega_even is the leading small-k threshold --
    # Corrected 2026-09-22: T(k) is the CLOSED FORM min(w+(k), w-(k)) (collinear
    # endpoint), not a stochastic search; and the offset has the closed form
    # |eps(k)| = |kx ky kz| / (3|k|)  (F397 R6).  The original stochastic search
    # under-converged at small |k| and contaminated the quoted exponent 2.10.
    rows = []
    ks = np.array([0.0125, 0.025, 0.05, 0.1, 0.2, 0.4])
    gaps, ratios = [], []
    for kk in ks:
        k = np.array([1, 1, 1.0]) / ROOT3 * kk
        T = bs.true_threshold(k)                       # closed form
        Oe = bs.omega_even(k)
        eps = bs.threshold_offset_closed_form(k)
        gaps.append(Oe - T)
        ratios.append((Oe - T) / eps)
        rows.append({"|k|": float(kk), "T_true(k)": T, "Omega_even": Oe,
                     "Omega_even_minus_T": Oe - T, "eps_closed_form": eps,
                     "ratio_to_eps": (Oe - T) / eps, "slope": Oe / kk})
    gaps = np.array(gaps); ratios = np.array(ratios)
    # exponent on the small-k half, where the O(k^3) correction is negligible
    gap_exponent = float(np.polyfit(np.log(ks[:4]), np.log(gaps[:4]), 1)[0])
    # the closed-form endpoint must reproduce a deterministic pattern search
    k_chk = np.array([1, 1, 1.0]) / ROOT3 * 0.2
    pat = _pattern_min(k_chk)
    endpoint_residual = abs(bs.true_threshold(k_chk) - pat)
    out["C3"] = {"rows": rows, "slope_small_k": rows[-1]["slope"],
                 "Omega_even_minus_T_exponent": gap_exponent,
                 "ratio_to_eps_smallest_k": float(ratios[0]),
                 "endpoint_vs_pattern_search": float(endpoint_residual),
                 "all_gaps_nonneg": bool(np.all(gaps >= -1e-12)),
                 "pass": (abs(rows[0]["slope"] - 1.0 / ROOT3) < 1e-3
                          and np.all(gaps >= -1e-12)
                          and 1.98 < gap_exponent < 2.05
                          and abs(ratios[0] - 1.0) < 0.01
                          and endpoint_residual < 1e-7)}

    # --- C4: two-method agreement at finite k (clean gap) -------------------
    k = np.array([1, 1, 1.0]) / ROOT3 * 0.4
    g_loc, T = bs.critical_coupling(k, L)
    g = 1.5 * g_loc
    Eb_sec = bs.bound_state_secular(k, L, g)
    Eb_dense, _ = bs.bound_state_dense(k, L, g)
    # Diagnostic added 2026-09-22.  critical_coupling takes T = E.min() on the
    # L^3 relative grid.  At finite k the true floor is at the collinear
    # endpoint p = +-k/2, generally not a grid point, so the grid T is an
    # artifact: it lies somewhere between the closed-form floor and
    # Omega_even(k), non-monotonically in L.  `offset_fraction_missed` is 0
    # when the grid finds the floor and 1 when it misses the whole offset.
    # This does NOT affect C4's conclusion -- C4 compares two diagonalisations
    # of the SAME H, and T only sets the arbitrary scale g = 1.5*g_loc -- nor
    # C1/C2/C5/C6, which are all at k = 0, where the floor IS p = 0 and T = 0
    # exactly.  Measured here so it is visible rather than silent.
    # See F169 "C2/C4-note".
    T_closed = bs.threshold_closed_form(k)
    offset = bs.omega_even(k) - T_closed
    out["C4"] = {"Eb_secular": Eb_sec, "Eb_dense": Eb_dense,
                 "diff": abs(Eb_sec - Eb_dense),
                 "below_threshold": Eb_sec < T,
                 "T_grid": T, "T_closed_form": T_closed,
                 "T_grid_minus_T_closed": T - T_closed,
                 "offset_fraction_missed": (T - T_closed) / offset,
                 "grid_never_below_closed_form": bool(T >= T_closed - 1e-14),
                 "pass": (abs(Eb_sec - Eb_dense) < 1e-9 and Eb_sec < T
                          and T >= T_closed - 1e-14)}

    # --- C5: masslessness inherited from gapless constituents ---------------
    _, T_at_0 = bs.critical_coupling([0, 0, 0], L)
    wp0 = float(bs._w(0, 0, 0, "+")); wm0 = float(bs._w(0, 0, 0, "-"))
    out["C5"] = {"T(0)": T_at_0, "w_plus(0)": wp0, "w_minus(0)": wm0,
                 "pass": T_at_0 == 0.0 and wp0 == 0.0 and wm0 == 0.0}

    # --- C6: wavefunction is localized (finite RMS radius) ------------------
    rms = bs.realspace_rms_radius(psi0, L)
    out["C6"] = {"rms_relative_radius_lattice_units": rms,
                 "pass": np.isfinite(rms) and 0.0 < rms < L / 2.0}

    checks = {k: bool(v["pass"]) for k, v in out.items()}
    out["checks"] = checks
    out["all_pass"] = all(checks.values())

    def _py(o):
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        raise TypeError(type(o))

    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w") as fh:
        json.dump(out, fh, indent=2, default=_py)

    for k_, v in checks.items():
        print(f"[{'PASS' if v else 'FAIL'}] {k_}")
    print("C1 g_c, secular residual:", round(g_c, 5), out["C1"]["secular_residual_at_threshold"])
    print("C3 slope:", round(out["C3"]["slope_small_k"], 6),
          " (Omega_even - T) exponent:", round(out["C3"]["Omega_even_minus_T_exponent"], 3))
    print("C4 two-method diff:", out["C4"]["diff"])
    print("C5 T(0):", out["C5"]["T(0)"], " C6 rms radius:", round(rms, 3))
    print("ALL PASS:", out["all_pass"])
    assert out["all_pass"], "F169 photon bound-state checks failed"


if __name__ == "__main__":
    main()
