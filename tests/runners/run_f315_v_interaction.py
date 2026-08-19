#!/usr/bin/env python3
"""F315 runner — emit the falsifier-5 result artifact.

Writes `test-results/F315_V_interaction.json`.  Every quantity is a commutator,
phase-difference or degeneracy count, so the class is `machine` rather than
`exact`; the one structural leg (the L = 2 degeneracy) is exact.

    PYTHONPATH=src python3 tests/runners/run_f315_v_interaction.py
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
    from test_F315_V_interaction import check_all
    return results_path, check_all


def main() -> int:
    results_path, check_all = _bootstrap()
    out = check_all()

    # The runner's failure mode (P1 / D9).  These five are the FINDING's claim,
    # not a restatement of the code: V is broken by a genuine scatterer, the
    # breaking is maximal rather than marginal, the O(G) deformation is
    # obstructed, the test can still report survival on an integrable control,
    # and the evolution's own charge is untouched on the same resonant set.
    claims = {
        "V_is_broken_by_contact":
            out["C3_contact_breaks_V"]["max_dphi_V_live"] > 1.0,
        "breaking_is_maximal":
            out["C3_contact_breaks_V"]["max_dphi_V_live"] > 3.0,
        "deformation_is_obstructed":
            out["C5_deformation_is_obstructed"]["obstructed"] > 0,
        "test_can_report_survival":
            out["C2_test_can_report_survival"]["obstructed"] == 0,
        "control_free_charge_untouched":
            out["C6_control_free_charge_survives_on_resonant_set"][
                "control_free_charge"] < 1e-12,
    }
    out["runner_claims"] = claims
    failed = [k for k, v in claims.items() if not v]

    path = results_path("F315_V_interaction.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, sort_keys=True)
    print(f"wrote {path}")
    print(f"{out['n_checks']} checks; "
          f"contact obstructed = {out['C5_deformation_is_obstructed']['obstructed']}; "
          f"integrable control obstructed = "
          f"{out['C2_test_can_report_survival']['obstructed']}")

    if failed:
        print("FAIL — runner claims not met: " + ", ".join(failed))
    # `assert`, not a bare `return 1`. The exit code is the same either way, but
    # tools/audit_tests.py reads the SOURCE (`has_assert`), and a runner whose
    # only failure mode is an integer return reads as UNFALSIFIABLE — which is
    # what put this file on the 2026-08-19 ratchet list. The claims above are
    # the finding's, so this is the assertion that was always meant to be here.
    assert not failed, "runner claims not met: " + ", ".join(failed)
    print("OK — falsifier 5 does not fire; V does not survive interaction")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
