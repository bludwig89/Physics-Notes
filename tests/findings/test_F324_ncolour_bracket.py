"""F324 — the N_c bracket (completeness row B10, "why 3 colours").

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_ncolour_bracket.check_ncolour_bracket` (record
`F324-ncolour-bracket`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F324-ncolour-bracket
    casim test --id F324-ncolour-bracket --param n_generations=2              # red
    casim test --id F324-ncolour-bracket --param include_lepton_doublet=false # red
    casim test --id F324-ncolour-bracket --param vector_like_su2=true         # red
    casim test --id F324-ncolour-bracket --param quark_colour_rep=adjoint     # red
    casim test --id F324-ncolour-bracket --param c7_n_max=3                   # red
    casim test --id F324-ncolour-bracket --param scan_from=2                  # red
    casim test --id F324-ncolour-bracket --param doubler_multiplicity=2       # red
    casim test --id F324-ncolour-bracket --param empty_tower_passes=true      # red

WHAT IS AND IS NOT CLAIMED.  N_c = 3 is NOT derived from nothing, the parity
argument is NOT new, and the incremental content over F298 is ONE BIT.

  PRIOR ART.  Baer & Wiese, "Can one see the number of colors?", Nucl. Phys.
  B609 (2001) 225: "In order to cancel Witten's global anomaly, the number of
  colors must be odd in the standard model" -- obtained unconditionally, per
  generation, i.e. stronger than the default form here.  What is new is that
  the group and content are DERIVED in this tree, and the PAIRING with F298.

  SIX PREMISES, all in the finding's section 0: (i) n_gen odd (F75; only the
  parity, and retired entirely under `per_generation=True`); (ii) the colour
  sector exists -- F318's residual, and what the N = 1 edge restates;
  (iii) the rotor modulus is the centre Z_{N_c} (F97/F99) -- the one premise
  with NO control; (iv) quarks in the defining rep; (v) the chiral multiplet
  structure; (vi) no fermion doubling (CL020 is `narrowed`).

  NOT consumed: any measured NUMBER, the three-constituent baryon, or either
  branch of X1.  "No measured number" is not "no empirical input" and the
  finding never uses them interchangeably.

  G0   the Witten mod-2 rule (2j = 1 mod 4), QUOTED, and cross-checked against
       the independent "Dynkin index odd" form: T = 1, 4, 10, 20, 35.
  W1   the content is N_c quark doublets + 1 lepton doublet per generation --
       the y_L = -N_c y_Q row, imported.  NOT param-adaptive.
  W2   the parity: doublet count even <=> N_c ODD.  Exact over Z.
  W2b  ... and it is not vacuous: it excludes exactly the even N_c.
  W3   colour's OWN Z_2 anomaly at N_c = 2 is SATISFIED, so N_c = 2 falls to
       the WEAK count.  Does NOT show the constraint is colour-input-free.
  W3b  premise (iv), MEASURED: fundamental {3}, adjoint {2}, two-index-antisym
       {2,3}, symmetric {2}.  The bit's sign is set by the assumed content.
  Y1   the SAME constraint arrives LOCALLY under a U(2) embedding, via the
       quantisation rule q = 2j mod 2 on the model's own y_L = -N_c.
  W4   F293's six anomaly-CANCELLATION rows contain neither reading.  R1 stays
       closed; measured, not argued.
  U1   F298's criterion imported, scanned to N = 1: support {2,3}.
  U1b  ... and both edges labelled: N = 1 fails by CONVENTION (the other
       reading gives {1,2,3}), N = 2 passes VACUOUSLY.  Exactly one
       non-trivial pass, at N = 3.
  U1c  ... and the k-string truncation cuts BOTH ways: the sextet gives
       chi = 3/10 against the tower's 3/4, so level-independence fails at
       N = 3 too outside the sector F110 deferred.  Falsifier 5b.
  B1   {Z_2-consistent} AND {C7 support} = {3} over N = 1..12, both edges
       scanned.
  B1c  the argument CAN fail: at a true N_c >= 4 the bracket is EMPTY.
  P1   the constituent count IS N_c -- a COROLLARY of premise (iv).  Its value
       is the DIRECTION: F317 sec 6's input was never independent of N_c.
  P2   agreement with F317 sec 6's float/SVD route.  NOT confirmation.

NOT COUNTED IN THE PASS TOTAL: the `declarations` field.  A flag that cannot
go red has no business occupying a slot in an n/n.

Run standalone:  python3 tests/findings/test_F324_ncolour_bracket.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import derive_ncolour_bracket as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_ncolour_bracket()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    print(f"  declarations (not counted): {res['declarations']}")
    for p in res["premises"]:
        print(f"  premise: {p}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F324_ncolour_bracket.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["passed"], "F324 gate failed: " + json.dumps(res["checks"],
                                                            default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
