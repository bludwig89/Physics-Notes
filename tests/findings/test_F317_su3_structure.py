"""F317 — the STRUCTURE of the colour gauge field (completeness row B1, colour leg).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_su3_structure.check_su3_structure` (record
`F317-su3-structure`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F317-su3-structure
    casim test --id F317-su3-structure --param use_compensator=false   # red
    casim test --id F317-su3-structure --param chiral_colour=true      # red
    casim test --id F317-su3-structure --param rule_reads_colour=true  # red
    casim test --id F317-su3-structure --param drop_d_R=true           # red
    casim test --id F317-su3-structure --param n_colour=4              # red
    casim test --id F317-su3-structure --param n_colour=2              # red

WHAT IS AND IS NOT CLAIMED.  SU(3)_c is **not derived from nothing**.  Row B1's
"colour is still put in" bundles six impositions; this record derives four of
them, pins a fifth given one empirical input, and leaves the sixth -- THAT the
quark carries an internal index at all -- as an input, which the finding leads
with rather than buries.

  S0   the su(N) basis is checked, not trusted (Tr T^a T^b = delta/2 at 0.0).
  S1a  SU(2): ALL 27 symmetric anomaly coefficients are EXACTLY zero, so a
       chiral doublet is allowed.  Exact over Q[i].
  S1b  SU(3): A^{888} = -1/sqrt(3) exactly, so a chiral triplet is NOT.
  S1c  among {vector-like, chiral, conjugate} exactly ONE colour assignment is
       anomaly-free.  This closes F91's `by construction`.
  S2a  hence the branch-space coupling is a SCALAR (traceless part 0.0), so
       F68/F91's even propagation law is FORCED, not selected on elegance.
  S2b  the contrast: a chiral colour would have split the branches by
       |dOmega|/2 = 5.137e-3 on the body diagonal.
  S3a  a CA rule is ONE operator per cell, so a SITE-DEPENDENT V(x) commutes
       with the on-site step exactly -- which is WHY F27's U(x) is pure gauge.
  S3b  the HOP compares two cells: covariance fails at O(1) (1.343).
  S3c  U_mu -> V(x) U_mu V^dag(x+mu) restores it exactly (6.0e-16).  The gluon
       field is the price of the rule being local.
  S3d  the same three legs on the TREE's own SU(3) operators, not a toy.
  S4a  the model's own steps generate the FULL M_4 on the Dirac factor (16),
       and the re-typed BCC walk IS unitary (2.2e-16) -- the guard the F313
       review found missing in check_C4b.
  S4b  the commutant of the rule is M_3, dim 9 => the group is exactly U(3).
  S4c  corollary and PREDICTION: every level is exactly 3-fold degenerate.
  S5a  [SU(2)_L]^2 U(1)_Y is IDENTICALLY zero in N_c on the model's own
       nullspace (imported from derive_ncolour, not re-derived).
  S5b  [SU(2)_L]^2 U(1)_trace = N_c b / 2 != 0 => the U(1) factor of U(N_c)
       cannot be gauged.  It fails BECAUSE SU(2)_L is chiral (F27).
  S5c  only ONE abelian direction exists (nullspace dim 1) and Y has it.
  S5d  on the model's own content the cubic SU(N)^3 anomaly cancels 2 - 2,
       and A(fund) is nonzero, so it is a statement about the CONTENT.
  S5e  the mixed SU(N)^2 U(1)_Y anomaly vanishes identically in N_c
       (y_u = N_c+1, y_d = 1-N_c cancel against 2 y_Q).
  S6a  Lambda^3(C^N) carries a singlet at EXACTLY one N, and it is 3.
  S6b  ... so the three-constituent totally antisymmetric singlet exists at 3.
  S7   dim su(3) = 8 gluons and the algebra closes on f^abc.

Run standalone:  python3 tests/findings/test_F317_su3_structure.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import derive_su3_structure as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_su3_structure()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results", "F317_su3_structure.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["passed"], "F317 gate failed: " + json.dumps(res["checks"],
                                                            default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
