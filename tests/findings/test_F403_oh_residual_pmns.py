"""F403 -- can any residual symmetry drawn from O_h fix PMNS, given the model's
charged-lepton frame?

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.particles.derive_oh_residual_pmns.check_oh_residual_pmns`
(record `F403-oh-residual-pmns`, tier gate), so this module deliberately
defines no `test_*` functions.

    casim test --id F403-oh-residual-pmns
    casim test --id F403-oh-residual-pmns --param frame=trimaximal      # red (N1)
    casim test --id F403-oh-residual-pmns --param theta13_lo_deg=0      # red (N1, N2, B2)

Run standalone:  python3 tests/findings/test_F403_oh_residual_pmns.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.particles import derive_oh_residual_pmns as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_oh_residual_pmns()
    for name, c in res["checks"].items():
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {name}")
    print(f"\n  OVERALL: {'PASS' if res['pass'] else 'FAIL'}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results", "F403_oh_residual_pmns.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    assert res["pass"]
    return 0


if __name__ == "__main__":
    sys.exit(main())
