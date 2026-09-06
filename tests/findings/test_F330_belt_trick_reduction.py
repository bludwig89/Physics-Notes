"""F330 — the belt-trick residual, precisely named (completeness row A9).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_belt_trick.check_belt_trick_reduction` (record
`F330-belt-trick-reduction`, tier gate), so this module deliberately defines
no `test_*` functions -- `tests/conftest.py` hides entry-driven records from
file collection so nothing runs twice under two contracts.

    casim test --id F330-belt-trick-reduction
    casim test --id F330-belt-trick-reduction --param theta_exchange=6.283185307179586  # red
    casim test --id F330-belt-trick-reduction --param wrong_singlet=true                # red

WHAT IS AND IS NOT CLAIMED.  F289 left the belt trick itself -- the homotopy
identifying particle exchange with a 2*pi rotation -- external.  This module
does not derive it either.  What it does: (1) pin the residual down to a
single, precisely stated, peer-reviewed postulate (Anastopoulos's "Postulate
1", quant-ph/0110169) rather than a vague "the belt trick, imported"; and (2)
verify, using the model's OWN rotor (the same one F289 uses for R(2pi)=-1),
the two representation-theoretic facts that make that postulate's spin-1/2
consequence concrete: the antisymmetric singlet is an exact scalar under the
diagonal rotation for every angle and axis, while the symmetric triplet is
not (at the belt trick's own exchange angle, pi) -- which is why the naive
"exchange = a c-number phase" identification is clean for fermions and is,
precisely, the still-partially-open "Berry-Robbins problem" for anything
beyond a single antisymmetric pair.

    B1   the true singlet never leaks out of its own span under R(t,n)⊗R(t,n)
         for a swept grid of angles and axes -- an exact trivial-representation
         statement, not a tautology about 1-dimensional subspaces (see B1's
         control below).
    B2   the triplet IS an invariant subspace but is NOT a scalar
         representation at theta = pi: its restriction has eigenvalues
         {-1, +1, -1}, not a multiple of the identity.
    B2b  ... but the subspace itself has zero leak (it does not mix with the
         singlet) -- this is the "invariant, not the same as scalar" contrast
         the whole point rests on.
    B3   two applications of the theta=pi exchange give exactly the identity
         on the two-spin space, via F289's own already-derived R(2pi) = -1
         per constituent -- reused, not recomputed.

Run standalone:  python3 tests/findings/test_F330_belt_trick_reduction.py
"""
from __future__ import annotations

import json
import math
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import qi_belt_trick as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_belt_trick_reduction()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F330 gate failed: " + json.dumps(res["checks"],
                                                             default=str)

    controls = [
        ({"theta_exchange": 2.0 * math.pi}, ("B2",)),
        ({"wrong_singlet": True}, ("B1",)),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_belt_trick_reduction(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<28} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    singlet worst leak                 {s['F330_singlet_worst_leak']:.2e}")
    print(f"    singlet worst phase deviation      {s['F330_singlet_worst_phase_deviation']:.2e}")
    print(f"    triplet deviation from scalar (pi) {s['F330_triplet_deviation_from_scalar_at_pi']:.6f}")
    print(f"    triplet subspace leak (pi)         {s['F330_triplet_subspace_leak_at_pi']:.2e}")
    print(f"    two exchanges - identity           {s['F330_two_exchanges_minus_identity']:.2e}")
    print(f"    F289 R(2pi) cross-check            {s['F330_f289_r2pi_residual']:.2e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
