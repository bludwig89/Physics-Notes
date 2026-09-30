"""F405 -- can quark colour and charge factors on F95's Dirac-sea cubic B
move the Koide equipartition point to the quark values?

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.particles.derive_quark_B_colour_charge.check_quark_B_colour_charge`
(record `F405-quark-B-colour-charge`, tier gate), so this module deliberately
defines no `test_*` functions.

    casim test --id F405-quark-B-colour-charge
    casim test --id F405-quark-B-colour-charge --param generation_charges_up=[2/3,2/3,-1/3]  # red (U1)
    casim test --id F405-quark-B-colour-charge --param mass_dependent_dressing=true         # red (U2)

Run standalone:  python3 tests/findings/test_F405_quark_B_colour_charge.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.particles import derive_quark_B_colour_charge as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_quark_B_colour_charge()
    for name, c in res["checks"].items():
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {name}")
    print(f"\n  OVERALL: {'PASS' if res['pass'] else 'FAIL'}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results", "F405_quark_B_colour_charge.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    assert res["pass"]
    return 0


if __name__ == "__main__":
    sys.exit(main())
