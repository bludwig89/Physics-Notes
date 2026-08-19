#!/usr/bin/env python3
"""F316 runner — emit the Laurent-Pell descent artifact.

Writes `test-results/F316_laurent_pell.json`.  Coefficient arithmetic is exact
over Q(i); the support function is evaluated against an irrational lambda in
float, so the SEPARATION statements are machine-precision comparisons with an
explicit reported gap.  Hence `machine`, not `exact`.

    PYTHONPATH=src python3 tests/runners/run_f316_laurent_pell.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    """Put src/ and tests/findings/ on sys.path and return what this runner needs.

    Inside a call, not at module scope: a bare `sys.path.insert` at import time
    is what the `import_time_work` ratchet (tools/audit_tests.py) counts.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "..", "..", "src"),
              os.path.join(here, "..", "findings")):
        if p not in sys.path:
            sys.path.insert(0, p)
    from casim.engine.particles._results_path import results_path
    from test_F316_laurent_pell import check_all
    return results_path, check_all


def main() -> int:
    results_path, check_all = _bootstrap()
    out = check_all()

    # The runner's failure mode (P1 / D9).  These five are the FINDING's claim.
    # The first is the whole point: the width separates the element that breaks
    # the imported theorem's hypothesis, which is why the transfer needed doing.
    claims = {
        "width_beats_degree_on_the_counterexample":
            (not out["C2_width_detects_units_where_degree_does_not"]
                 ["counterexample_is_unit"])
            and out["C2_width_detects_units_where_degree_does_not"][
                "counterexample_width"] > 1e-9,
        "unitarity_gives_central_symmetry":
            out["C3_unitarity_gives_central_symmetry"]["all_symmetric"],
        "product_identity_is_exact":
            out["C6_product_identity"]["all_exact"],
        "descent_is_strict_and_by_exactly_2c":
            out["C7_descent"]["all_strict"] and out["C7_descent"]["all_drop_2c"],
        "base_case_is_closed":
            not out["C8_base_case"]["u_is_difference_of_two"],
    }
    out["runner_claims"] = claims
    failed = [k for k, v in claims.items() if not v]

    path = results_path("F316_laurent_pell.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, sort_keys=True)
    print(f"wrote {path}")
    print(f"{out['n_checks']} checks; "
          f"descent drop = 2c at every step: {out['C7_descent']['all_drop_2c']}; "
          f"live steps = {out['C7_descent']['n_live']}")

    if failed:
        print("FAIL — runner claims not met: " + ", ".join(failed))
    # `assert`, not a bare `return 1`. The exit code is the same either way, but
    # tools/audit_tests.py reads the SOURCE (`has_assert`), and a runner whose
    # only failure mode is an integer return reads as UNFALSIFIABLE — which is
    # what put this file on the 2026-08-19 ratchet list. The claims above are
    # the finding's, so this is the assertion that was always meant to be here.
    assert not failed, "runner claims not met: " + ", ".join(failed)
    print("OK — the polynomial->Laurent transfer is proved; F313 imports nothing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
