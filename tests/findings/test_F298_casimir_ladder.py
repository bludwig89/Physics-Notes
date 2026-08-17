"""F298 — the SU(N) Casimir ladder F110 deferred, and the C7 re-run against it.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.casimir_ladder.check_casimir_ladder` (record
`F298-casimir-ladder`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F298-casimir-ladder
    casim test --id F298-casimir-ladder --param tower=symmetric   # must go red
    casim test --id F298-casimir-ladder --param n_max=3           # must go red

WHAT THIS SETTLES AND WHAT IT DOES NOT.  It executes F294's named deciding
computation for the k-string sector.  It does NOT resolve the H1/H2 tension --
structure says H2, the measured alpha_s says H1 to 0.08% -- and it does NOT
derive N_c = 3.  What is new is a STRUCTURAL N_c bound that consumes no measured
number: the C7 identity exists only for N_c <= 3.

  L1   C_2(fund) = (N^2-1)/2N and C_2(adj) = N, exactly over Q.
  L2   the C7 identity (a single level-independent chi) exists ONLY for
       N <= 3.  For N >= 4 chi comes out level-dependent and there is no
       identity at all.  This is independent of H1/H2: the identity exists for
       N <= 3 under both readings and for N >= 4 under neither.
  L3   where it exists, chi = 1/(4 g^2 C_F) -- so the Casimir DOES enter, and
       F294's hypothesis H2 is the structurally correct reading.
  L3b  CONTROL: the symmetric tower is uniform at NO N, so L2 is a property of
       the k-string sector rather than of a conveniently chosen ladder.
  L4   the discriminator F294 recommended is DEGENERATE at N=3 -- Casimir,
       centre and sine all give sigma_2/sigma_1 = 1, because k=2 is the
       conjugate of k=1.  F294's recommendation is withdrawn.
  L4b  ... and F86's BPS law gives 2, disagreeing with all three, which locates
       F86 in the non-interacting-vortex regime rather than settling anything.
  L4c  ... the laws DO separate at N=4, so the test is sound and merely
       inapplicable at the N the model has.
  L5   empirically H1 matches the required bare coupling to +0.08% while H2 is
       -24.9% -- the half of the tension that points the other way.

Run standalone:  python3 tests/findings/test_F298_casimir_ladder.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import casimir_ladder as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_casimir_ladder()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F298 gate failed: " + json.dumps(res["checks"],
                                                            default=str)

    controls = [
        ({"tower": "symmetric"}, ("L2", "L3")),
        ({"n_max": 3}, ("L2",)),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_casimir_ladder(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<26} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    N with a C7 identity            {s['F298_N_with_C7_identity']}")
    print(f"    chi values                      {s['F298_chi_values']}")
    print(f"    chi = 1/C_F where defined       {s['F298_chi_is_one_over_CF']}")
    print(f"    k-string laws degenerate at 3   {s['F298_kstring_laws_degenerate_at_3']}")
    print(f"    ... but separate at 4           {s['F298_kstring_laws_separate_at_4']}")
    print(f"    required alpha_0                {s['F298_required_alpha_0']:.7f}")
    print(f"    H1 error / H2 error             {s['F298_H1_relative_error']:+.4%} / {s['F298_H2_relative_error']:+.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
