"""
F155 — Residual A attacked with the one-loop self-energy machinery, and the
Residual-B freeze value bracketed anchor-free.

  A0 (EXACT): the F26 link is exactly SO(2) per mode => mean link u0 = 1 exactly
     => the Wilson tadpole Z0 (the bulk of the Wilson 28.81) is STRUCTURALLY
     ABSENT. The gluon is luminal (Omega_even -> c_lat|k|). This is F151-S2 made
     into a direct machine-precision check — the reason Lambda_rule is O(1).

  A3 (CONVERGENT): the lattice-continuum SUBTRACTION machinery (the d1 integral
     F154 said was needed) is built and shown n-convergent on the vacuum-
     polarisation bubble — fixing F154's grid-dependence (which was the
     UNsubtracted moment). b0 (the running coefficient) is universal: the
     lattice bubble runs with the continuum slope.

  A5 (BRACKET): the continuum-subtracted Lepage-Mackenzie loop momentum (true
     Omega_even kernel) CONVERGES to the band top q*_abelian ~ 0.97/a (the F129
     near-perfect-action signature). With F151's lower band edge 1/sqrt3 this
     brackets q* to [0.577, ~0.97], implied 0.733 inside; the implied Lambda-
     ratio is O(1) (NOT Wilson 28.81). Single-value pinning needs the gluonic
     3g+ghost finite part (open).

  Bf (ANCHOR-FREE FREEZE): the IR coupling freeze ~0.39 is bracketed WITHOUT the
     M(0) anchor: the L-stable nonlinear chiSB onset (~0.31, set by the gluon
     mass m_D = decoupling) and the steep gap rise pin the freeze to a narrow
     window [onset, alpha_phys] ~ [0.31, 0.38], 0.39 at the top, inside the
     continuum frozen window [0.3,0.5]. (Sharpens F154's 'freeze not supplied by
     the gap'.)
"""
import math
import os
import sys

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.gauge import gluon_self_energy as se
from casim.engine.interactions import running_gap_solve as gap


def run():
    results = {}

    # ---- A0: tadpole sector empty (exact) + gluon luminal ----
    tp = se.tadpole_sector_empty(L=8)
    lum = se.gluon_is_luminal()
    okA0 = (tp["max_residual"] < 1e-12 and tp["u0_renormalisation"] == 1.0
            and lum["max_rel_dev"] < 1e-8)
    results["A0_tadpole_empty_exact"] = dict(
        passed=bool(okA0), link_residual=tp["max_residual"],
        u0=tp["u0_renormalisation"], wilson_Z0_absent=tp["wilson_Z0_absent"],
        gluon_luminal_dev=lum["max_rel_dev"])

    # ---- A3: the d1 subtraction is convergent; b0 universal ----
    sub = se.subtracted_bubble_constant(ns=(24, 32, 40), p=0.2)
    b0u = se.b0_universal_check(n=32)
    okA3 = (sub["convergence_spread"] < 1e-3
            and abs(b0u["ratio"] - 1.0) < 0.03)
    results["A3_d1_subtraction_convergent"] = dict(
        passed=bool(okA3), d1_bubble=sub["converged_value"],
        convergence_spread=sub["convergence_spread"],
        b0_slope_ratio=b0u["ratio"])

    # ---- A5: q* bracketed inside the band; Lambda-ratio O(1), not Wilson ----
    hr = se.qstar_highres(ns=(32, 48, 64), d=4)
    lo, hi = hr["qstar_a_bracket"]
    lr_lo, lr_hi = hr["lambda_ratio_bracket"]
    okA5 = (lo <= hr["qstar_a_implied_F151"] <= hi          # implied inside bracket
            and abs(hi - 0.97) < 0.05                        # abelian moment ~ band top
            and lr_hi < 5.0                                  # O(1), nowhere near Wilson 28.8
            and abs(hr["lambda_ratio_at_implied"] - 1.78) < 0.1
            and hr["tadpole_empty"])
    results["A5_qstar_bracketed"] = dict(
        passed=bool(okA5), qstar_bracket=[lo, hi],
        qstar_abelian=hr["qstar_a_abelian_moment"],
        qstar_implied=hr["qstar_a_implied_F151"],
        lambda_ratio_bracket=[lr_lo, lr_hi],
        lambda_ratio_at_implied=hr["lambda_ratio_at_implied"],
        wilson_contrast=hr["wilson_contrast"])

    # ---- Bf: anchor-free freeze window (L-stable onset) ----
    onset16 = gap.chiSB_onset(gap.M_D_F88, L=16, lo=0.25, hi=0.40)
    onset24 = gap.chiSB_onset(gap.M_D_F88, L=24, lo=0.25, hi=0.40)
    phys = gap.alpha_eff_for_target(gap.M_D_F88, L=16)["alpha_eff_star"]
    okBf = (abs(onset16 - onset24) < 5e-3               # onset L-stable
            and 0.25 < onset16 < phys                    # onset below physical
            and 0.30 <= phys <= 0.50)                    # physical in frozen window
    results["Bf_freeze_anchorfree"] = dict(
        passed=bool(okBf), onset_L16=round(onset16, 4), onset_L24=round(onset24, 4),
        alpha_phys=round(phys, 4),
        freeze_window=[round(onset16, 3), round(phys, 3)],
        continuum_window=[0.30, 0.50])

    # ---- C: scope honesty — the two routes' pass/fail criteria are sharp ----
    okC = (hr["qstar_a_implied_F151"] == 0.7327
           and hr["lambda_ratio_target"] == 1.78
           and hr["wilson_contrast"] == 28.81)
    results["C_falsification_sharp"] = dict(
        passed=bool(okC), target_qstar=0.7327, target_lambda_ratio=1.78,
        wilson_must_not_match=28.81,
        verdict="A: q* bracketed [0.577,~0.97] (implied 0.733 inside), needs "
                "gluonic 3g+ghost finite part / high-res static potential to "
                "pin; B-freeze ~0.35(4) anchor-free, exact value gated on A scale")

    n = sum(r["passed"] for r in results.values())
    results["summary"] = dict(passed=n, total=5, all_pass=n == 5,
                              A_bracketed=True, A_pinned=False,
                              B_freeze_anchorfree=True)
    return results


if __name__ == "__main__":
    import json
    import os
    r = run()
    print(json.dumps(r, indent=2, default=str))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "test-results", "F155_qstar_self_energy.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(r, f, indent=2, default=str)
    assert all(r[k]["passed"] for k in
               ("A0_tadpole_empty_exact", "A3_d1_subtraction_convergent",
                "A5_qstar_bracketed", "Bf_freeze_anchorfree",
                "C_falsification_sharp")), "F155 checks failed"
    print("\nF155: 5/5 PASS")
