#!/usr/bin/env python3
"""F400 runner — emit the coordination-selector result artifact.

Writes `test-results/F400_coordination_selector.json`. All four checks are
exact integer/rational arithmetic — no floats, no finite differences.

    PYTHONPATH=src python3 tests/runners/run_f400_coordination_selector.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    """Put src/ and tests/findings/ on sys.path and return what this runner needs.

    Inside a call, not at module scope — see F291's own runner for why.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "..", "..", "src"),
              os.path.join(here, "..", "findings")):
        if p not in sys.path:
            sys.path.insert(0, p)
    from casim.engine.particles._results_path import results_path
    from test_F400_coordination_selector import check_all
    return results_path, check_all


def _assert_verdict(out: dict) -> None:
    assert out["A2_tetrahedron_equals_diamond_bonds"]["equal_as_sets"] is True
    assert out["A2_tetrahedron_equals_diamond_bonds"]["grams_identical"] is True
    assert out["B1_diamond_shift_not_fcc_vector"]["orbit_invariant"] is False
    assert int(out["n_checks"]) == 4, out["n_checks"]


def main() -> int:
    results_path, check_all = _bootstrap()
    out = check_all()
    _assert_verdict(out)
    dest = results_path("F400_coordination_selector.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True, default=str)
    print(f"wrote {dest}")
    print(f"  checks              : {out['n_checks']}")
    print(f"  bcc-tetra=diamond   : "
          f"{out['A2_tetrahedron_equals_diamond_bonds']['equal_as_sets']}")
    print(f"  diamond is Bravais  : "
          f"{out['B1_diamond_shift_not_fcc_vector']['orbit_invariant']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
