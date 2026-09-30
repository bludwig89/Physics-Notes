"""F406 -- the charged-lepton frame fork: picture (a) E_g-diagonal vs picture (b)
[111] circulant, decided (F118 tie; three inequivalent circulant branches; the
quadratic crystal-field phase diagram).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.particles.derive_lepton_frame_fork.check_lepton_frame_fork`
(record `F406-lepton-frame-fork`, tier gate), so this module deliberately
defines no `test_*` functions.

    casim test --id F406-lepton-frame-fork
    casim test --id F406-lepton-frame-fork --param sea_generation_blind=false   # red (K2, V)
    casim test --id F406-lepton-frame-fork --param s12sq_band=nufit60           # red (K4, V)

Run standalone:  python3 tests/findings/test_F406_lepton_frame_fork.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.particles import derive_lepton_frame_fork as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_lepton_frame_fork()
    for name, c in res["checks"].items():
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {name}")
    print(f"\n  OVERALL: {'PASS' if res['pass'] else 'FAIL'}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results", "F406_lepton_frame_fork.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    assert res["pass"]
    return 0


if __name__ == "__main__":
    sys.exit(main())
