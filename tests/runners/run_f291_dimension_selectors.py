#!/usr/bin/env python3
"""F291 runner — emit the dimension-selector result artifact.

Writes `test-results/F291_dimension_selectors.json`.  All nine checks are
exact-algebraic except D2, which finite-differences the engine's own BCC walk
and lands at machine precision.

    PYTHONPATH=src python3 tests/runners/run_f291_dimension_selectors.py
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
    from test_F291_dimension_selectors import check_all
    return results_path, check_all




# The runner's failure mode (P1 / D9). Without this it wrote numbers and always
# exited 0: `audit_tests.py` counted it UNFALSIFIABLE, and the manifest links
# F291_dimension_selectors.json to the sibling tests/findings file by exact stem,
# so the runner inherited no baseline of its own either. These four are the
# finding's claim, not a restatement of the code: d = 3, signature 1+3, the
# engine's own BCC walk agreeing with the symbolic Jacobian at the FD floor, and
# the full leg count.
def _assert_verdict(out: dict) -> None:
    assert int(out["E1_verdict"]["d_selected"]) == 3, out["E1_verdict"]
    assert str(out["E1_verdict"]["signature"]) == "1+3", out["E1_verdict"]
    assert float(out["D2_engine_cross_check"]
                 ["max_abs_residual_vs_symbolic"]) < 1e-9, \
        out["D2_engine_cross_check"]
    assert int(out["n_checks"]) == 9, out["n_checks"]


def main() -> int:
    results_path, check_all = _bootstrap()
    out = check_all()
    _assert_verdict(out)
    dest = results_path("F291_dimension_selectors.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True, default=str)
    print(f"wrote {dest}")
    print(f"  checks   : {out['n_checks']}")
    print(f"  d         : {out['E1_verdict']['d_selected']}")
    print(f"  signature : {out['E1_verdict']['signature']}")
    print(f"  engine FD : {out['D2_engine_cross_check']['max_abs_residual_vs_symbolic']:.2e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
