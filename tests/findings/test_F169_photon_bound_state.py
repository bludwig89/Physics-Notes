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
    rows = []
    ks = np.array([0.05, 0.1, 0.2, 0.4])
    gaps = []
    for kk in ks:
        k = np.array([1, 1, 1.0]) / ROOT3 * kk
        T = bs.true_threshold(k)
        Oe = bs.omega_even(k)
        gaps.append(Oe - T)
        rows.append({"|k|": float(kk), "T_true(k)": T, "Omega_even": Oe,
                     "Omega_even_minus_T": Oe - T, "slope": Oe / kk})
    gaps = np.array(gaps)
    gap_exponent = float(np.polyfit(np.log(ks), np.log(gaps), 1)[0])
    out["C3"] = {"rows": rows, "slope_small_k": rows[0]["slope"],
                 "Omega_even_minus_T_exponent": gap_exponent,
                 "all_gaps_nonneg": bool(np.all(gaps >= -1e-12)),
                 "pass": (abs(rows[0]["slope"] - 1.0 / ROOT3) < 1e-4
                          and np.all(gaps >= -1e-12)
                          and 1.7 < gap_exponent < 2.3)}

    # --- C4: two-method agreement at finite k (clean gap) -------------------
    k = np.array([1, 1, 1.0]) / ROOT3 * 0.4
    g_loc, T = bs.critical_coupling(k, L)
    g = 1.5 * g_loc
    Eb_sec = bs.bound_state_secular(k, L, g)
    Eb_dense, _ = bs.bound_state_dense(k, L, g)
    out["C4"] = {"Eb_secular": Eb_sec, "Eb_dense": Eb_dense,
                 "diff": abs(Eb_sec - Eb_dense),
                 "below_threshold": Eb_sec < T,
                 "pass": abs(Eb_sec - Eb_dense) < 1e-9 and Eb_sec < T}

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
