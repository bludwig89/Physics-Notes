"""F318 — can the model's CELL carry the internal index? (F317's residual).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.lattice.cell_internal_index.check_cell_internal_index` (record
`F318-cell-internal-index`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F318-cell-internal-index
    casim test --id F318-cell-internal-index --param internal_dispersive=true  # red
    casim test --id F318-cell-internal-index --param n_constituents=2          # red
    casim test --id F318-cell-internal-index --param max_clifford_k=1          # red
    casim test --id F318-cell-internal-index --param n_int=1                   # red

WHAT IS AND IS NOT CLAIMED.  F317's residual is NOT closed.  Three questions
were tangled inside it and they have three different answers: the cell PERMITS
the index at zero cost, FORCES its shape, and does NOT force its existence.
The forcing is Fermi statistics, and the input that remains is "the matter
sector contains a three-constituent bound state" -- smaller and more concrete
than "an internal index exists", but still an input, and F317 section 6
consumes the SAME fact, so the two findings do not independently confirm
each other.

  A1   the Clifford rank of a cell is 2k+1 (s = 2,4,8 -> 3,5,7), built by
       Jordan-Wigner and verified constructively AND for maximality.  The
       tree's own `dimensionality.max_anticommuting_traceless_hermitian`
       RAISES for s != 2, so F291's general remark had never been run.
  A2   ... so on the NAIVE reading the model's s = 36 quark cell would permit
       d <= 11 and F291's S1 would be gone.  The worry, at full strength.
  B1   one Weyl branch: the hop's traceless span is 3, anticommuting rank 3.
  B2   THE RESULT.  The model's branch-doubled (massless Dirac) cell widens
       the span to SIX and leaves the anticommuting rank at THREE, because
       tau_3 (x) sigma_i COMMUTES with 1 (x) sigma_i.  So F291's "conditional
       on s = 2" is not conditional on s = 2 -- it is conditional on the HOP's
       anticommuting rank, which the model's real cell does not move.
  B3   an internal factor (x)1_N changes nothing at all: span 6, rank 3, on a
       cell of dimension 12.
  B4   CONVERSE, and what stops B1-B3 being vacuous: a walk that genuinely
       USES five anticommuting generators on C^4 has ker J = coker J = 0 at
       d = 5, so the selector returns 5.  Enlargements are not all alike.
  C1   the commutant over generic momenta FACTORISES, 2 -> 18 at N = 3, i.e.
       exactly a factor N^2.
  C2   ... and every added element is NON-DISPERSIVE (literal 0.0) while the
       update disperses at 0.2846.  A commuting unitary is a clock only if it
       disperses -- the criterion F313 never had to state.  F313 section 9's
       second flow WAS dispersive, which is why F315 had to kill it.
  D1   the 3-constituent totally antisymmetric state on one nodeless level
       exists at N = 3 (dim 20), by explicit antisymmetrisation.
  D2   ... and N = 1 is EXCLUDED: spin alone caps a nodeless level at TWO.
       This is what forces the index to exist, and it is not the cell.
  D3   the honest negative: every space/time verdict is IDENTICAL at N = 1 and
       N = 3 while the commutant is not.  The cell is INDIFFERENT.

Run standalone:  python3 tests/findings/test_F318_cell_internal_index.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.lattice import cell_internal_index as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_cell_internal_index()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F318_cell_internal_index.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["passed"], "F318 gate failed: " + json.dumps(res["checks"],
                                                            default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
