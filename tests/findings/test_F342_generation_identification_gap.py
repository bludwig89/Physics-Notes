"""F342 -- rubric row C1 (exactly three generations): does F75's own defining
condition (i) ("identical gauge quantum numbers") select the T_1u triplet at
all, against any other 3-dim subspace of the same shell, including T_2g?

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.particles.derive_generation_identification_gap.check_generation_identification_gap`
(record `F342-generation-identification-gap`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F342-generation-identification-gap
    casim test --id F342-generation-identification-gap --param symmetry_group=C4z_only   # red (H1)
    casim test --id F342-generation-identification-gap --param charge_locality=block      # red (H3)

WHAT IS AND IS NOT CLAIMED.  F75's group theory (Sigma d^2 = 48, T_1u the
unique maximal single-valued triplet) is NOT re-attacked here -- closed.
F292's independent n-copies multiplicity check is NOT re-attacked -- closed.
What this finding adds: F75 Sec.7's own operational condition (i) -- that a
generation multiplet must "carry identical gauge quantum numbers" -- is shown
to supply ZERO selecting power between T_1u and T_2g (the triplet F75 Step 3
excludes only by a parity argument) under the charge structure this project's
gauge modules actually implement (a scalar charge, diagonal in the site
basis, with no site/shell/irrep index anywhere in charge_coupling.py or
minimal_coupling.py).  That "zero selecting power" is forced by one fact
about the shell: the 8 vertices form a SINGLE orbit under the full O_h vacuum
symmetry (transitivity), which is verified here, together with an exact,
independent (equivariant-embedding, not character-projection) cross-check of
F75 T2's A1g (+) A2u (+) T1u (+) T2g decomposition.  What WOULD supply
selecting power -- an irrep-block-dependent, non-diagonal charge -- is
exhibited exactly and shown to be absent from the adopted (non-fork) engine.

Run standalone:  python3 tests/findings/test_F342_generation_identification_gap.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.particles import derive_generation_identification_gap as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_generation_identification_gap()
    for name, c in res["checks"].items():
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {name}")
    print(f"\n  OVERALL: {'PASS' if res['pass'] else 'FAIL'}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F342_generation_identification_gap.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["pass"], "F342 gate failed: " + json.dumps(res["checks"], default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
