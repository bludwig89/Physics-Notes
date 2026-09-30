"""F380 — cluster decomposition, F331's residual named as one object
(completeness row A10, QUANT -> PARTIAL).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_cluster_asymptotic_series.check_named_residual_K`
(record `F380-cluster-asymptotic-series-K`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F380-cluster-asymptotic-series-K
    casim test --id F380-cluster-asymptotic-series-K --param reference=axis110  # red (C1, C2)

WHAT IS AND IS NOT CLAIMED.  F331 closed F290's residual 1 (interacting,
3-D cluster decomposition) but its own free-3-D kappa_100(m) validation left
a mass-dependent RATIO TABLE as the residual (1.53 at m=0.05 shrinking to
0.95 at m=0.95) -- a tolerance, not a named object.  This module takes the
rubric's own "first step": evaluate F331's UNMODIFIED
`axis100_measured_kappa` at the mass the self-consistent NJL gap equation
actually selects, m*, rather than the registry default m=0.5.  That
hypothesis (m* is special and the ratio collapses to 1 there) is FALSIFIED
-- ratio(m*)=1.1096, L-converged, not 1 to the numerical floor.  What
follows is more useful: m* turns out to be perfectly ordinary, sitting
inside the SAME distribution as every other tested mass once the whole
table is re-expressed via the EXACT OLS bias formula as an implied
algebraic-prefactor power p_eff(m) = (kappa_measured-kappa_100)/(S_{r,ln
r}/S_{rr}), which is mass-independent to 2.65% AND matches an independently
derived theoretical value p=3/2 (2 transverse stationary-phase dimensions
plus an axial square-root branch point in the dispersion -- see the module
docstring) to under 1% -- one named, theoretically-anchored constant, not
eighteen unexplained numbers. (An earlier version of this finding used a
cruder r_mid proxy and a wrong p=1 "same as Yukawa" mechanism; caught and
fixed by this finding's own review-finding pass -- see "Reviewed &
corrected" in the finding file.) p_eff is MEASURED against a theoretically
DERIVED target, but the sub-leading correction is not yet computed
symbolically (that is the next rung, PARTIAL -> MACHINE, explicit future
work). Does not touch F290's separate 1-D exponent shortfall or S-matrix-
level clustering.

Run standalone:  python3 tests/findings/test_F380_cluster_asymptotic_series.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import qi_cluster_asymptotic_series as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_named_residual_K()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F380 gate failed: " + json.dumps(res["checks"],
                                                             default=str)

    print("\n  control (must go RED, and only where it should):")
    r = m.check_named_residual_K(reference="axis110")
    red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
    assert not r["passed"], "control reference=axis110 did NOT go red"
    assert set(red) == {"C1", "C2"}, \
        f"control reference=axis110 went red at {red}, expected ['C1', 'C2']"
    print(f"    reference=axis110            RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    p_eff (mean, 0.05<=m<=0.90)        {s['F380_p_eff_mean']:.4f}")
    print(f"    p_eff relative spread              {s['F380_p_eff_rel_spread']:.4f}")
    print(f"    theory power (branch point+trans.) {s['F380_theory_power']:.4f}")
    print(f"    deviation from theory              {s['F380_theory_deviation']:.4f}")
    print(f"    raw ratio relative spread          {s['F380_ratio_rel_spread']:.4f}")
    print(f"    NJL dynamical mass m*              {s['F380_m_star']:.4f}")
    print(f"    p_eff at m*                        {s['F380_p_eff_at_m_star']:.4f}")
    print(f"    z-score of p_eff(m*) vs the scan   {s['F380_z_at_m_star']:.2f}")
    print(f"    ratio at m*                        {s['F380_ratio_at_m_star']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
