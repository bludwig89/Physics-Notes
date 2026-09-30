"""F404 -- FORK: Koide pseudo-masses for quarks (route 1 of the 2026-09-24
flavour research report) -- viable, and what breaks.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.forks.particles.koide_pseudomass_fork.check_koide_pseudomass_fork`
(record `F404-koide-pseudomass-fork`, tier gate), so this module deliberately
defines no `test_*` functions.

    casim test --id F404-koide-pseudomass-fork
    casim test --id F404-koide-pseudomass-fork --param down_signs=+++    # red (P3, P4b, P7)
    casim test --id F404-koide-pseudomass-fork --param ckm_weight=0.0    # red (P4a)

Run standalone:  python3 tests/findings/test_F404_koide_pseudomass_fork.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.forks.particles import koide_pseudomass_fork as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_koide_pseudomass_fork()
    for name, c in res["checks"].items():
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {name}")
    print(f"\n  OVERALL: {'PASS' if res['pass'] else 'FAIL'}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results", "F404_koide_pseudomass_fork.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    assert res["pass"]
    return 0


if __name__ == "__main__":
    sys.exit(main())
