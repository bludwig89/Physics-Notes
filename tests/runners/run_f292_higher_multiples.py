#!/usr/bin/env python3
"""F292 runner — emit the higher-multiples result artifact.

Writes `test-results/F292_higher_multiples.json`.  Every leg is exact over
Z or Q; there is no floating-point step in this finding at all.

    PYTHONPATH=src python3 tests/runners/run_f292_higher_multiples.py
"""
from __future__ import annotations

import json
import os
import sys

def _bootstrap():
    """Put src/ and tests/findings/ on sys.path and return what this runner needs.

    Inside a call, not at module scope: a bare `sys.path.insert` at import time is
    what the `import_time_work` ratchet (tools/audit_tests.py) counts, and it is
    the one thing every runner in this tree used to cost. Same shape as F290/F297.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "..", "..", "src"),
              os.path.join(here, "..", "findings")):
        if p not in sys.path:
            sys.path.insert(0, p)
    from casim.engine.particles._results_path import results_path
    from test_F292_higher_multiples import check_all
    return results_path, check_all




# The runner's failure mode (P1 / D9) — see the note in
# run_f291_dimension_selectors.py. These are F292's claim: d = 6 loses
# chirality, d = 9 keeps it but dies on the bivector condition, d = 2 is
# excluded twice over leaving 3, founding decision 1 survives the reducible
# reading, and every leg ran.
def _assert_verdict(out: dict) -> None:
    assert [int(x) for x in out["A2_integer_roots"]["excluded"]] == [6, 9, 12], \
        out["A2_integer_roots"]
    assert bool(out["B2_chirality_parity"]["d6_chiral"]) is False, \
        out["B2_chirality_parity"]
    assert bool(out["B2_chirality_parity"]["d9_chiral"]) is True, \
        out["B2_chirality_parity"]
    assert int(out["B3_d_two_excluded_twice"]["surviving_dimension"]) == 3, \
        out["B3_d_two_excluded_twice"]
    assert bool(out["C1_reducible_collapse"]
                ["founding_decision_1_untouched"]) is True, \
        out["C1_reducible_collapse"]
    assert int(out["n_checks"]) == 8, out["n_checks"]


def main() -> int:
    results_path, check_all = _bootstrap()
    out = check_all()
    _assert_verdict(out)
    dest = results_path("F292_higher_multiples.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True, default=str)
    print(f"wrote {dest}")
    print(f"  checks          : {out['n_checks']}")
    print(f"  d=6 fails       : {out['D1_verdict']['d6_fails']}")
    print(f"  d=9 fails       : {out['D1_verdict']['d9_fails']}")
    print(f"  d=9 frozen dirs : {out['D1_verdict']['d9_frozen_directions']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
