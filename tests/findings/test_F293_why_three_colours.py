"""F293 — why three colours (completeness-2026-08-04 row B10).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_ncolour.check_ncolour` (record
`F293-why-three-colours`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F293-why-three-colours
    casim test --id F293-why-three-colours --param alpha_s_MZ=0.05      # red
    casim test --id F293-why-three-colours --param alpha0_factor=1.25   # red
    casim test --id F293-why-three-colours --param mu0_factor=100.0     # red

WHAT IS AND IS NOT CLAIMED.  N_c = 3 is **not derived** here.  Four routes are
examined; two are closed as no-gos, one is shown circular, and one works as an
EMPIRICAL SELECTOR that consumes a measured number.  The finding leads with that.

  B1   the FULL F279 six-constraint hypercharge system has nullspace dimension
       1 for EVERY N_c (symbolic over Q, plus N_c = 1,2,3,4,5,7), with ratios
       1:(N_c+1):(1-N_c):-N_c:-2N_c:0.
  B1b  the gravitational and cubic anomalies are identically zero as polynomials
       in N_c ⇒ anomaly freedom selects nothing.  The standard SM argument
       (N_c Y_Q + Y_L = 0 forces 3) is unavailable HERE because Y_Q is not
       independently given -- it comes out of the same nullspace, ∝ N_c.
  B2   the O_h 3-cycle about [111] is an even permutation, det = +1, so it IS
       an SU(3) element.
  B2b  ... and does not commute with the Gell-Mann generators, so an
       axis-identified colour would be rotated by a lattice rotation.
  B2c  control: a genuine internal index DOES commute, residual 0.0.
  B3   the Z_3 centre route is circular -- the tree introduces Z_3 AS the
       centre of SU(3) -- and is recorded rather than counted as evidence.
  B5   alpha_s(mu_0) = 1/(16 pi) carries no N_c and no Casimir.  This is the
       fact that makes the running a one-unknown equation, and it rests on
       F110 C7's 4 being a count of plaquette links.
  B5b  the selector returns N_c = 2.998.
  B5g  PRIMARY and non-circular: Lambda spans 28.3 decades over N_c = 2..4 and
       only N_c = 3 lands at the observed hadronic scale.
  B5h  the circularity is audited: the PDG alpha_s IS extracted inside QCD with
       N_c = 3, so B5b is partly circular and is labelled so.
  B5i  the one physical flavour threshold moves N_c by 0.09%.
  B5c  among integers only N_c = 3 lands alpha_s(M_Z).
  B5d  N_c >= 4 puts the Landau pole ABOVE M_Z (256 TeV at N_c = 4).
  B5e  log-robust: F280's factor-8 scheme band moves N_c by only 0.21.
  B5f  ... but the COUPLING is the fragile direction -- the named falsifier.

Run standalone:  python3 tests/findings/test_F293_why_three_colours.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import derive_ncolour as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_ncolour()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    print(f"  N_c selected = {res['N_c_selected']:.4f}")
    assert res["passed"], "F293 gate failed: " + json.dumps(res["checks"],
                                                            default=str)

    controls = [
        ({"alpha_s_MZ": 0.05}, ("B5b",)),
        ({"alpha0_factor": 1.25}, ("B5b",)),
        ({"mu0_factor": 100.0}, ("B5b",)),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_ncolour(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<28} N_c -> {r['N_c_selected']:.4f}   "
              f"RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    anomaly nullspace dim (any N_c)   {s['B10_anomaly_nullspace_dim']}")
    print(f"    hypercharge ratios                {s['B10_hypercharge_ratios']}")
    print(f"    [C3, colour] commutator           {s['B10_C3_commutator_with_colour']:.4f}")
    print(f"    internal-index control            {s['B10_control_internal_commutes']}")
    print(f"    alpha_s(mu_0) = 1/(16 pi)         {s['B10_alpha_s_mu0']:.7f}")
    print(f"    N_c selected                      {s['B10_N_c_selected']:.4f}")
    print(f"    N_c with thresholds               {s['B10_N_c_thresholded']:.4f}")
    print(f"    Lambda span over N_c=2..4         {s['B10_lambda_span_decades']:.1f} decades")
    print(f"    N_c band over F280 scheme band    {s['B10_N_c_band_scheme']}")
    print(f"    dN_c per % of coupling            {s['B10_dNc_per_percent_coupling']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
