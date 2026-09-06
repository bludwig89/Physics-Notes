"""F338 -- B10 after F325: the odd-N_c bracket does not narrow further.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_ncolour_ceiling.check_ncolour_ceiling` (record
`F338-ncolour-ceiling`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from
file collection so nothing runs twice under two contracts.

    casim test --id F338-ncolour-ceiling
    casim test --id F338-ncolour-ceiling --param su3_pi4_order_override=2   # red (G1)
    casim test --id F338-ncolour-ceiling --param include_nu_r=false         # red (G2)
    casim test --id F338-ncolour-ceiling --param assumed_anomaly_modulus=8  # red (G3)
    casim test --id F338-ncolour-ceiling --param n_gen=2                    # red (G0, G3)

WHAT IS AND IS NOT CLAIMED.  This finding does NOT narrow the odd-N_c
bracket {3,5,7,9,11,...} F325 left B10 with.  It closes one further
candidate route (G1) and flags one unverified lead (G3) for a future
session; both are stated as such before anything else.

  G0  the CURRENT bracket, recomputed directly from the surviving Witten-
      parity leg (F324's own `witten_scan`, imported unmodified -- the
      withdrawn C7 leg is NOT reintroduced), confirming F325's withdrawal
      is correctly reflected outside the finding's own prose.  N_c=1 is
      dropped on the separate, still-standing premise that a non-trivial
      colour sector exists at all (F317 Sec.0 item (i); F318's residual),
      not via the withdrawn C7 identity.
  G1  a candidate route nobody in this tree had checked and closed: does
      the COLOUR gauge group SU(N_c) itself carry an analogous pi_4 global
      anomaly (as opposed to the already-used SU(2)_L route)?  No --
      pi_4(SU(N)) = 0 identically for N >= 3 (cited, standard homotopy-of-
      Lie-groups fact).  Closes a previously-unexamined candidate.
  G2  the model's own per-generation Weyl fermion count is EXACTLY
      4(N_c+1) (elementary dimension count, exact over Z), equal to 16
      precisely at N_c=3.
  G3  FLAGGED, NOT VERIFIED, NOT CLAIMED.  If the Wang-Wen-Witten /
      Garcia-Etxebarria-Montero mod-16 Pin+/Dai-Freed anomaly of one
      Majorana-completed SM generation generalises to "total Weyl count
      over odd n_gen generations is a multiple of 16" for general N_c
      content, the arithmetic consequence is N_c = 3 (mod 4), narrowing
      the odd bracket to {3,7,11,15,...}.  The physical premise (the
      discrete symmetry generator X = 5(B-L) - 4Y's own N_c-dependence)
      is NOT re-derived here.  Excluded from the pass count.

EXTERNAL LITERATURE CROSS-CHECK, recorded in `external_literature_check()`
and reported as a `declarations` field (also uncounted): Baer & Wiese's own
2001 paper states low-energy pion physics cannot distinguish N_c=3 from
5,7,...; Tanizaki (JHEP08(2018)171) derives 't Hooft anomaly matching for
GENERIC N_c with no N_c=3 discrimination; hep-ph/0009242 shows the textbook
pi0 -> 2 gamma argument does not constrain N_c at all.  So the residual is
generic to any chiral gauge theory of this shape, not a lattice-specific
gap.

DO NOT RE-ATTACK from here: the anomaly-cancellation route (F293 R1), the
spatial-3 identification (F293 R2), the Z_3-centre route (F293 R3), F303's
n*C_F=4 three-link-plaquette route, or F325/CN19's withdrawn C7 upper bound.

Run standalone:  python3 tests/findings/test_F338_ncolour_ceiling.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import derive_ncolour_ceiling as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_ncolour_ceiling()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    print(f"  current_bracket: {res['current_bracket']}")
    print(f"  declarations (not counted): "
          f"{list(res['declarations'].keys())}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F338_ncolour_ceiling.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["passed"], "F338 gate failed: " + json.dumps(res["checks"],
                                                            default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
