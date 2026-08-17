#!/usr/bin/env python3
"""F313 runner — emit the time-signature result artifact.

Writes `test-results/F313_time_signature.json`.  Every check is exact-algebraic
over Q(i) or over Z except C7, which measures a 4x4 commutator norm on the
massive Dirac walk and lands at machine precision.

    PYTHONPATH=src python3 tests/runners/run_f313_time_signature.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    """Put src/ and tests/findings/ on sys.path and return what this runner needs.

    Inside a call, not at module scope: a bare `sys.path.insert` at import time
    is what the `import_time_work` ratchet (tools/audit_tests.py) counts.  Same
    shape as F290/F291/F297.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "..", "..", "src"),
              os.path.join(here, "..", "findings")):
        if p not in sys.path:
            sys.path.insert(0, p)
    from casim.engine.particles._results_path import results_path
    from test_F313_time_signature import check_all
    return results_path, check_all


def main() -> int:
    results_path, check_all = _bootstrap()
    out = check_all()

    # The runner's failure mode (P1 / D9).  Without this it would write numbers
    # and always exit 0, which `audit_tests.py` counts UNFALSIFIABLE.  These
    # five are the FINDING's claim, not a restatement of the code: the commutant
    # is 2-dimensional, its scalar part is exactly the shift lattice, the update
    # is the fundamental Pell unit of a squarefree extension, <A> is infinite,
    # and the signature reads 3+1 off the single input s = 2.
    claims = {
        "commutant_is_two_dimensional":
            out["C1b_commutant_is_two_dimensional"]["commutant_dim"] == 2,
        "scalar_part_is_exactly_the_shifts":
            out["C3b_nothing_but_shifts_is_scalar_unitary"]["none_unitary"],
        "update_is_the_fundamental_pell_unit":
            out["C4a_discriminant_is_squarefree"]["squarefree"]
            and out["C4b_update_is_the_fundamental_unit"]["satisfies_pell"],
        "time_is_infinite_cyclic":
            out["C5c_update_has_infinite_order"]["never_a_shift"],
        "signature_is_three_plus_one":
            out["C6_signature_at_the_minimal_cell"]["signature"] == "3+1",
        # Added 2026-08-13: the withdrawn identity must stay withdrawn.  If
        # 2log2(s)+1 and dim su(s) ever agreed at s = 4 the numerology would be
        # defensible; they do not, and the artifact records that they do not.
        "withdrawn_identity_stays_withdrawn":
            out["C6_signature_at_the_minimal_cell"]["functions_diverge_at_s4"],
        # Added 2026-08-13: the d = 1 non-tautology control.
        "theorem_fails_in_one_dimension":
            out["C0_one_dimension_fails_the_theorem"]["theorem_fails_in_1d"],
    }
    out["runner_claims"] = claims
    failed = [k for k, v in claims.items() if not v]

    path = results_path("F313_time_signature.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str, sort_keys=True)
    print(f"wrote {path}")
    print(f"{out['n_checks']} checks; "
          f"signature {out['C6_signature_at_the_minimal_cell']['signature']}; "
          f"imported step: {out['imported_step']}")

    if failed:
        print("FAIL — runner claims not met: " + ", ".join(failed))
        return 1
    print("OK — all runner claims met")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
