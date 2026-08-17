"""F309 — K2/G10: g_*(T) and g_*s(T) from the model's own field content.

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.thermodynamics_gstar.check_gstar` (record
`F309-gstar-model-content`, tier gate), so this file deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F309-gstar-model-content
    casim test --id F309-gstar-model-content --param branch_odd_control=True  # red
    casim test --id F309-gstar-model-content --param sm_content_control=True  # red

This closes gap #4 of `docs/status/completeness-2026-08-07.md` and next step #1
of F300.  The four checks that matter for reading the result:

  GS-3/6  The fermionic lattice EoS coefficients, in closed form.  F300 sec. 7.2
          named the blocker as "the fermionic BZ sums with the branch-odd term
          handled".  Handled turns out to mean KEPT: the branch-odd term does
          not cancel for a single Weyl branch, it enters squared at exactly the
          order the anisotropic term does, and it supplies 3/7 of the
          coefficient.  C_u^F = 310 pi^2/441 = (31/4) C_u^gamma.
  GS-7    C_u/C_w = 15/2 for fermions too, and it SURVIVES the branch-odd
          control.  F300 proved the ratio for the photon; it is a property of
          degree-3 homogeneity, not of statistics or of the anisotropy.
  GS-8/9  g_*(10 MeV) = 10.75 and g_*s -> 2 + (21/4)(4/11), from the model's own
          content on the emergent T_nu/T_gamma.  The content F297 assumed is the
          content the model derives -- which nobody could say before this run.
  GS-13   The one non-null substitution: F297's BBN on the model's OWN electron
          mass (F121, 0.51069 MeV) moves Y_p by +1.08e-4 (+0.032 sigma) and D/H
          by +1.06e-4 relative (+0.009 sigma).  Both TOWARD the data, both far
          below the observational error.

Two things this file will NOT assert, and each is deliberate:

  * **that the BBN result is now parameter-free.**  It is not.  eta10, V_ud,
    G_F and the reaction network remain external (F297's ledger); this closes
    exactly one import, the degree-of-freedom count.
  * **that the high-T g_* difference is observable.**  GS-12 finds the model's
    g_* above the top threshold differs from the SM's by exactly one degree of
    freedom in either direction, so 106.75 is unavailable to it.  The one
    observable that would carry it, Omega_GW ~ g_* g_*s^(-4/3), moves by 0.31 %
    -- labelled, not published as a falsifier (F300's discipline).

Run standalone:  python3 tests/findings/test_F309_gstar.py
"""
from __future__ import annotations

import os
import sys


def _bootstrap():
    # Inside the function, not at module scope: a module-level sys.path preamble
    # is what `tools/audit_tests.py` counts as import-time work.
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import thermodynamics_gstar as m
    return m


def main() -> int:
    m = _bootstrap()

    res = m.check_gstar()
    print("F309 / K2+G10 — g_*(T) from the model's own field content\n")
    for c in res["checks"]:
        print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['id']:8s} {c['desc']}")
    assert res["all_pass"], f"only {res['n_pass']}/{res['n_total']} passed"

    controls = [
        ({"branch_odd_control": True}, ("GS-3", "GS-4", "GS-5")),
        ({"sm_content_control": True}, ("GS-8", "GS-9")),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_gstar(**kwargs)
        red = [c["id"] for c in r["checks"] if not c["pass"]]
        assert not r["all_pass"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<34} RED: {', '.join(red)}")

    # GS-7 must SURVIVE the branch-odd control: that is the structural half.
    r = m.check_gstar(branch_odd_control=True)
    ratio_leg = [c for c in r["checks"] if c["id"] == "GS-7"][0]
    assert ratio_leg["pass"], "C_u/C_w = 15/2 must be invariant under the " \
                              "branch-odd deletion"

    e, w, bw = res["eos"], res["weyl"], res["bbn_window"]
    ra, pr, lc, sh = res["ratios"], res["excluded"], res["lattice"], res["shift"]
    print("\n  headline numbers:")
    print(f"    content                   {w['weyl_total']} Weyl "
          f"({w['weyl_L_total']} L + {w['weyl_R_total']} R), "
          f"imbalance {w['chirality_imbalance']}")
    print(f"    C_u^F closed 310 pi^2/441 {e['Cu_exact']:.7f}  measured {e['Cu_meas']:.7f}")
    print(f"    C_w^F closed 124 pi^2/1323 {e['Cw_exact']:.7f}  measured {e['Cw_meas']:.7f}")
    print(f"    C_s^F closed  31 pi^2/49  {e['Cs_exact']:.7f}  measured {e['Cs_meas']:.7f}")
    print(f"    ratio C_u/C_w = 15/2      {e['ratio_meas']:.6f}")
    print(f"    fermion/photon = 31/4     {ra['ratio_u']:.6f} "
          f"= {ra['geometric_factor']:.0f} x {ra['statistics_factor']:.6f}")
    print(f"    branch-odd share = 3/7    {ra['branch_odd_share']:.6f}")
    print(f"    g_*(10 MeV)               {bw['g_star_early']:.6f}  (10.75)")
    print(f"    g_*  late                 {bw['g_star_late']:.6f}  "
          f"({bw['g_star_late_target']:.6f})")
    print(f"    g_*s late                 {bw['g_star_s_late']:.6f}  "
          f"({bw['g_star_s_late_target']:.6f})")
    print(f"    muon residual at 10 MeV   {pr['delta_g_muon_rel']:.3g} of g_*")
    print(f"    E_g mass bound            > {pr['m_Eg_bound_MeV']:.1f} MeV "
          f"({pr['m_Eg_bound_criterion']})")
    print(f"    lattice correction at BBN {lc['delta_g_star_rel']:.3g} "
          f"(Theta = {lc['theta']:.3g})")
    print(f"    Y_p  PDG m_e -> model m_e {sh['Y_p_pdg']:.6f} -> "
          f"{sh['Y_p_model']:.6f}  ({sh['delta_Y_p_in_sigma']:+.4f} sigma)")
    print(f"    D/H  PDG m_e -> model m_e {sh['DH_pdg']:.6e} -> "
          f"{sh['DH_model']:.6e}  ({sh['delta_DH_in_sigma']:+.4f} sigma)")
    print(f"    sigma(Y_p) needed to see it "
          f"{sh['sigma_Yp_needed_to_see_it']:.2e} "
          f"({sh['improvement_factor_needed']:.0f}x Aver 2021)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
