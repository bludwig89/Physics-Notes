"""F333 — does the colour index have to exist at all? (completeness row B1).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_internal_index_existence.check_internal_index_existence`
(record `F333-internal-index-existence`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F333-internal-index-existence
    casim test --id F333-internal-index-existence --param n_probe=4                    # red
    casim test --id F333-internal-index-existence --param n_probe=1                    # red
    casim test --id F333-internal-index-existence --param bosonic_baryon=true          # red
    casim test --id F333-internal-index-existence --param partial_generator_check=true # red

WHAT IS AND IS NOT CLAIMED.  This does not derive N_c = 3 (that stays F317
S6 / F318 SD / F324's).  It narrows F324's own named residual -- "the index
exists by fiat" -- to two named observational facts (baryons are fermions;
quarks are confined) combined with the model's own SU(N) representation
theory (generalised here from F317 S6's fixed k=3) and derived Fermi
statistics (F289).

  S0  dim su(1) = 0 exactly: N=1 carries no generators, no gauge boson.
  S1  the SU(N)-invariant subspace of Lambda^k(C^N) is 1-dim iff k=N, scanned
      over the full (N,k) grid (generalises F317 S6's fixed-k=3 scan).
  S2  the block-swap exchange parity of k identical fermions is exactly
      (-1)^k, built and measured for k=1..6, not quoted.
  S3  hence a quark-only colour-N baryon is fermionic iff N is odd; matches
      the observed fact that real baryons (protons, neutrons) are fermions.
  S4  hence N=1 is excluded by confinement: dim su(1)=0, no gauge boson
      exists to confine with, inconsistent with quarks being observed
      confined (never free).
  S5  {N odd, N>=2} = {3,5,7,9,11} over N=1..12 -- matches F324's own
      independent post-S22 bracket, reached from different premises
      (Witten anomaly + generation parity). Cross-check only, not used to
      pin N=3.

Run standalone:  python3 tests/findings/test_F333_internal_index_existence.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import derive_internal_index_existence as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_internal_index_existence()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F333_internal_index_existence.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["passed"], "F333 gate failed: " + json.dumps(res["checks"],
                                                            default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
