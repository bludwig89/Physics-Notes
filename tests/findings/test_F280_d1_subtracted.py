"""F280 — d_1 formulated SUBTRACTED against the Wilson Lambda_MSbar/Lambda_L
anchor (completeness-2026-08-04 gap #3).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.lpt_d1_subtracted.check_d1_subtracted` (record
`F280-d1-subtracted`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F280-d1-subtracted
    casim test --id F280-d1-subtracted --param lambda_wilson=1.0   # must go red

The six checks:

  S1  the master identity Lambda_MSbar/Lambda_rule = 28.8086 exp(-(T_w+dLoops)/2)
      closes to round-off -- the whole formulation uses differences only.
  S2  the slope-normalised constant is EXACTLY invariant under an overall
      measure factor, and the analytic-normalised one is not (closed form).
  S3  the propagator face of dLoops is measured, monotone in n, and converges.
  S4  the three-leg budget closes, and leg1+leg3 is fixed by the anchor alone.
  S5  the tadpole-free band [1, exp(dC_wilson_loops/2)] contains the required
      Lambda_MSbar/Lambda_rule and excludes Wilson.
  S6  the OPEN vertex leg is now a minority share of the required shift.

Run standalone:  python3 tests/findings/test_F280_d1_subtracted.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    """Path preamble + import, INSIDE a function on purpose.

    `tools/audit_tests.py` counts any module-level call as import-time work, and
    its own docstring notes that the usual `sys.path` preamble makes every new
    test file raise that count even when the file is a model citizen. There is
    no reason to pay it here: nothing in this file needs to run at import.
    """
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import lpt_d1_subtracted as m
    return m


def main() -> int:
    m = _bootstrap()
    check_d1_subtracted = m.check_d1_subtracted
    res = check_d1_subtracted()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}   -> {c['value']}")
    assert res["passed"], "F280 gate failed: " + json.dumps(res["checks"], default=str)

    legs = res["legs"]
    print("\n  budget (dC units), total required shift from Wilson = "
          f"{res['total_required_shift']:.4f}")
    for k, v in legs.items():
        print(f"    {k:<18} {v:+.4f}   ({abs(v / res['total_required_shift']):.1%})")
    print(f"\n  d_1(rule) required = {res['d1_rule_required']:.5f}   "
          f"Lambda_MSbar/Lambda_rule = {res['lambda_rule_required']:.4f}   "
          f"band = [{res['band'][0]:.2f}, {res['band'][1]:.2f}]")

    # the control must fail — a record with no failure mode is not a test (D9)
    control = check_d1_subtracted(lambda_wilson=1.0)
    assert not control["passed"], (
        "CONTROL DID NOT FAIL: with lambda_wilson=1.0 the Wilson scheme gap is "
        "gone, so the tadpole-free band must collapse below the target. A gate "
        "that stays green under this perturbation is not testing anything.")
    print("\n  [PASS] control (lambda_wilson=1.0) goes red as required")
    print("\nF280: 6/6 PASS + control")
    return 0


if __name__ == "__main__":
    # only under __main__: nothing here may run at import (D9 / CLAUDE.md)
    raise SystemExit(main())
