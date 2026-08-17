"""F297 — K2: Big-Bang nucleosynthesis and the light-element abundances.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.cosmology_bbn.check_k2` (record
`F297-bbn-light-elements`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F297-bbn-light-elements
    casim test --id F297-bbn-light-elements --param delta_m_mev=1.51   # red
    casim test --id F297-bbn-light-elements --param law=energy         # red

The twelve checks are listed in the finding (F297 section 7).  The two that
matter for reading the result:

  K2-6   the DEMOTED energy-only law (F106) is excluded by Y_p at 17.6 sigma,
         which is an independent confirmation of the F178 adoption on an
         observable unrelated to the neutron-star argument that decided it.
  K2-9   the MODEL's own m_n - m_p = +1.51 MeV (F122/F123) is excluded at
         36.6 sigma.  BBN bounds the splitting to +-0.0056 MeV where F122's own
         acceptance check (S8b) used +-1 MeV -- a factor 179.

Two things this file will NOT assert, and each is deliberate:

  * **lithium.**  The A=7 chain in this network is an order of magnitude low
    against the same published reference the other species are validated on, so
    four of the twelve rate fits are wrong or incomplete here.  Li7 is returned
    by the module (suppressing it would hide the defect) and is excluded from
    the battery.  No lithium claim is made in either direction.
  * **absolute abundances as model predictions.**  The network carries a ~0.9%
    absolute offset, measured by K2-1/K2-2.  Every model-level conclusion is a
    DIFFERENCE computed inside this same network, so that offset cancels; the
    absolutes are context and are quoted with the offset attached.

Run standalone:  python3 tests/findings/test_F297_bbn.py
"""
from __future__ import annotations

import os
import sys


def _bootstrap():
    # Inside the function, not at module scope: a module-level sys.path preamble
    # is what `tools/audit_tests.py` counts as import-time work, and every new
    # test file that writes one costs the ratchet a point for no physics reason.
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import cosmology_bbn as m
    return m


def main() -> int:
    m = _bootstrap()

    res = m.check_k2()
    print("F297 / K2 — BBN light-element abundances\n")
    for c in res["checks"]:
        flag = "PASS" if c["passed"] else "FAIL"
        val = "" if c["value"] is None else f"   {c['value']:+.6g}"
        print(f"  {flag}  {c['check']}{val}")
    assert res["passed"], f"only {res['n_pass']}/{res['n_total']} passed"

    # --- controls: each must go red, and only where it should ---------------
    controls = [
        ({"delta_m_mev": m.MODEL_DELTA_M_MEV}, ("K2-11", "K2-12")),
        ({"law": "energy"}, ("K2-11", "K2-12")),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_k2(**kwargs)
        red = [c["check"].split()[0] for c in r["checks"] if not c["passed"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<34} RED: {', '.join(red)}")

    v, lc, dm = m.validate_network(), m.law_control(), m.delta_m_confrontation()
    print("\n  headline numbers:")
    print(f"    network Y_p vs reference           {100*v['Y_p_rel_err']:+.2f}%")
    print(f"    network D/H vs reference           {100*v['D_H_rel_err']:+.2f}%")
    print(f"    Li7 vs reference (NOT validated)   {100*v['Li7_H_rel_err']:+.1f}%")
    print(f"    N_eff                              {m.n_eff_model()['N_eff']:.3f}")
    print(f"    energy-only law, Y_p               {lc['Y_p_energy']:.4f} "
          f"({lc['Y_p_energy_sigma']:+.1f} sigma)")
    print(f"    full-tensor law,  Y_p              {lc['Y_p_full']:.4f} "
          f"({lc['Y_p_full_sigma']:+.2f} sigma)")
    print(f"    Y_p at model delta m = 1.51 MeV    {dm['Y_p_model']:.4f} "
          f"({dm['Y_p_model_sigma']:+.1f} sigma)")
    print(f"    tau_n at model delta m             "
          f"{dm['tau_n_model_dm']:.1f} s vs {dm['tau_n_measured']:.1f} s measured")
    print(f"    BBN bound on delta m (1 sigma)     "
          f"+-{dm['delta_m_bound_1sigma_MeV']:.4f} MeV "
          f"(F122 checked to +-{dm['F122_tolerance_MeV']:.0f} MeV)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
