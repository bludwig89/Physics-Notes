"""F289 — the spin-statistics connection (completeness-2026-08-04 row A9).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_spin_statistics.check_spin_statistics` (record
`F289-spin-statistics`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F289-spin-statistics
    casim test --id F289-spin-statistics --param rotation_turns=2.0   # red
    casim test --id F289-spin-statistics --param exchange_alpha=0.5   # red
    casim test --id F289-spin-statistics --param jw_string=false      # red

WHAT IS AND IS NOT CLAIMED.  This is not a new proof of the spin-statistics
theorem.  The standard topological derivation needs two inputs it cannot supply
itself -- the spatial dimension (pi_1 of the configuration space is S_n for
d>=3 and the braid group for d=2, so only d>=3 forces sigma^2=1 and hence only
+-1) and the 2pi rotation phase of the object exchanged.  In ordinary quantum
mechanics both are inputs.  In THIS model both are outputs: d=3 is derived
(F291, F292) and the 2pi phase is a property of the model's own SU(2) rotor.
That is the contribution, and the finding says so in those words.

The eleven checks:

  S1   R(2pi) = -1 exactly on the model's rotor (input I2).
  S2   ... for every axis, so it is a property of the group and not of a frame.
  S3   the exchange is an involution, sigma^2 = 1 (the consequence of input I1).
  S3b  the anyonic alternative is still UNITARY -- so what excludes it is the
       DIMENSION, not the algebra.  This is the check that makes F291/F292
       load-bearing rather than decorative.
  S3c  spectrum exactly {+1 x3, -1 x1}: exactly two statistics.
  S4   F217's Jordan-Wigner operators anticommute -- they REALISE the -1.
  S4b  removing the JW string breaks it, so the string carries the sign.
  S5   Pauli exclusion c^dag c^dag = 0 exactly.
  S5c  the antisymmetriser kills same-mode states and KEEPS distinct ones,
       rank C(n,2).  Stated as a projector rank on purpose: writing
       `phi (x) phi - phi (x) phi` and noting it vanishes is a tautology of
       subtraction, which is the defect pattern this repo keeps finding.
  S5b  k-particle sector dimensions are exactly C(n,k), not the bosonic
       C(n+k-1,k) -- integer arithmetic, and it distinguishes the statistics.
  S6   the paired-spinor photon (key decision 5) is a BOSON: (-1)^2 = +1.

Run standalone:  python3 tests/findings/test_F289_spin_statistics.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import qi_spin_statistics as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_spin_statistics()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F289 gate failed: " + json.dumps(res["checks"],
                                                            default=str)

    controls = [
        ({"rotation_turns": 2.0}, ("S1", "S6")),
        ({"exchange_alpha": 0.5}, ("S3",)),
        ({"jw_string": False}, ("S4",)),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_spin_statistics(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<28} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    R(2pi) + 1                         {s['A9_R2pi_residual']:.2e}")
    print(f"    worst over 60 axes                 {s['A9_axis_independence_worst']:.2e}")
    print(f"    SWAP^2 - 1                         {s['A9_swap_involution_residual']}")
    print(f"    anyons unitary / non-involutive    {s['A9_anyons_all_unitary']} / {s['A9_anyons_none_involutive']}")
    print(f"    JW anticommutators                 {s['A9_jw_anticommutator_cc']}")
    print(f"    sector dims                        {s['A9_sector_dims']}")
    print(f"    photon pair 2pi residual           {s['A9_photon_pair_2pi_residual']:.2e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
