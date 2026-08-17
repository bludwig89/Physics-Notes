"""F299 — reinstating F294's discriminator and running it on the model's own engine.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.casimir_scaling.check_casimir_scaling` (record
`F299-casimir-scaling`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F299-casimir-scaling
    casim test --id F299-casimir-scaling --param tower=kstring   # must go red
    casim test --id F299-casimir-scaling --param beta=2.0        # must go red

WHAT THIS SETTLES AND WHAT IT DOES NOT.  F298 withdrew F294's physical
discriminator as "degenerate at N=3".  That withdrawal is scoped to the
antisymmetric (k-string) tower, in which at N=3 irrep and triality are in
bijection so no centre law can disagree with any Casimir law.  Outside that
tower the test is live, and the model's own exactly solvable 2D SU(3) engine
answers it: **Casimir scaling, hence H2.**  It does NOT derive N_c, and it does
NOT explain why the measured alpha_s prefers H1 to 0.08% -- it shows that
conflict is structural rather than a tolerance, because H2 cannot be rescued by
moving mu_0.

  S1   the sextet (2,0) shares the antitriplet's triality (2) while carrying
       C_2 = 10/3 against 4/3 -- exactly over Q.  This single row is why the
       discriminator is not degenerate at N=3.
  S2   the two laws SEPARATE on the full rep set (6, 8, 10, 15, 15', 27).
  S2b  CONTROL: inside the antisymmetric tower they provably cannot -- that IS
       F298's degeneracy, reproduced rather than disputed.
  S3   the generalised character quadrature reproduces
       `confinement.string_tension` in the fundamental to <1e-12, so the
       higher-rep numbers come from the engine already in the tree.
  S4   at the model's own coupling (g_s = 1/2 => beta = 2N/g_s^2 = 24) the
       engine follows Casimir scaling to <1.5% on every rung.
  S4b  ... and centre dominance is excluded: the sextet measures 2.491 against
       a centre prediction of 1.
  S5   the residual to EXACT Casimir scaling falls monotonically to zero as
       beta grows -- the sub-percent agreement is the approach to an exact law,
       not a coincidence at one coupling.
  S6   grid convergence at 1e-10: the quadrature is spectral, not merely
       convergent.
  S7   higher-rep Wilson loops are polynomial in the fundamental loop matrix,
       so F94's 3+1D Monte-Carlo could measure sigma_6/sigma_8/sigma_10 with NO
       new sampling.  That is the tool for the d=4 IR question, which is a
       different question from C7's bare normalisation.
  S8   H2 needs mu_0 ~ 6e24 GeV, several decades ABOVE the Planck mass, while
       H1 lands within 2% of the model's own 1.85e18 GeV.  The conflict is
       structural.

Run standalone:  python3 tests/findings/test_F299_casimir_scaling.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import casimir_scaling as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_casimir_scaling()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F299 gate failed: " + json.dumps(res["checks"],
                                                            default=str)

    controls = [
        ({"tower": "kstring"}, ("S2", "S4b")),
        ({"beta": 2.0}, ("S4",)),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_casimir_scaling(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<24} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    beta (model, g_s=1/2)           {s['F299_beta_model']}")
    print(f"    reps that separate the laws     {s['F299_separating_reps']}")
    print(f"    k-string tower degenerate       {s['F299_kstring_degenerate']}")
    print(f"    sigma_6/sigma_3 measured        {s['F299_sextet_measured']:.7f}")
    print(f"      Casimir law                   {s['F299_sextet_casimir_law']}")
    print(f"      centre law                    {s['F299_sextet_centre_law']}")
    print(f"    worst dev from Casimir          {s['F299_worst_dev_from_casimir']:.3%}")
    print(f"    law selected                    {s['F299_law_selected']}")
    print(f"    mu_0 H1 needs (GeV)             {s['F299_mu0_required_H1_GeV']:.4e}")
    print(f"    mu_0 H2 needs (GeV)             {s['F299_mu0_required_H2_GeV']:.4e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
