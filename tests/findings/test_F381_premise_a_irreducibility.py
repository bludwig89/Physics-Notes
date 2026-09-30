"""F381 — is F333's premise (a) (real baryons are fermions) reducible to
F289/F330's derived spin-statistics connection? (completeness row B1).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_premise_a_irreducibility.check_premise_a_irreducibility`
(record `F381-premise-a-irreducibility`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F381-premise-a-irreducibility
    casim test --id F381-premise-a-irreducibility --param inject_colour_token=true          # red
    casim test --id F381-premise-a-irreducibility --param inject_fake_param=true            # red
    casim test --id F381-premise-a-irreducibility --param force_all_fermionic=true          # red
    casim test --id F381-premise-a-irreducibility --param strip_premise_ii=true             # red
    casim test --id F381-premise-a-irreducibility --param assume_f324_premise_count=1       # red

WHAT IS AND IS NOT CLAIMED.  Does not re-attack F333's own premises (a),(b)
themselves, F317's four closed legs, or B10 ($N_c=3$).  Answers the specific
question the session brief posed: can premise (a) be discharged using
physics already in the tree (F289/F330), rather than imported from
experiment?  Answer: no -- and the module computes why rather than asserting
it, and also closes the one apparent escape (substituting F324's chain).

  S1  F289's and F330's own source text is scanned for colour/composite-count
      tokens (colour, color, SU(N), N_c, baryon, quark) -- zero hits.
  S2  every public function in those two modules is scanned via
      `inspect.signature` for a colour-count-shaped parameter -- none found.
  S3  F333's own S1+S2 machinery, run for N=2..7, genuinely bifurcates
      (fermion at odd N, boson at even N); F289's own rotor fact
      (`rotor_2pi_phase`) is unchanged across every branch, because it is
      never given N.
  S4  F324's own premise (ii), read from its returned `premises` list, is
      literally "the colour sector exists" -- so using F324 to discharge
      B1's existence residual would be circular.
  S5  the net premise cost of that substitution, computed rather than
      asserted: F324's six premises against F333's two -- a net increase.

Run standalone:  python3 tests/findings/test_F381_premise_a_irreducibility.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import derive_premise_a_irreducibility as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_premise_a_irreducibility()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F381_premise_a_irreducibility.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["passed"], "F381 gate failed: " + json.dumps(res["checks"],
                                                             default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
