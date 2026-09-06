"""F340 — strong CP: the L6 bridge, and reality extended to the full
non-perturbative configuration space (completeness B11, F321 Sec.6).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.colour_theta.check_strong_cp_nonperturbative` (record
`F340-strong-cp-nonperturbative`, tier gate), so this module deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven
records from file collection so nothing runs twice under two contracts.

    casim test --id F340-strong-cp-nonperturbative
    casim test --id F340-strong-cp-nonperturbative --param one_sense=true    # red U1 only
    casim test --id F340-strong-cp-nonperturbative --param bad_reverse=true  # red U2 only

WHAT THIS IS.  F321 Sec.6 named two open items on top of an otherwise closed
result (theta_QCD = 0 from reversal closure of the rule's minimal loop set,
CL278).  This record addresses both, without re-litigating the closed part.

  Item 1 -- the action fork.  `lpt_bcc_vertex`'s HONEST SCOPE said the F26
  rotation law and the rhombic plaquette action disagree at finite momentum
  and did not choose, so F321 T4 ran its argument on both branches rather than
  presupposing a resolution.  F337 (2026-08-30) CLOSED that fork (ledger row
  L6): the rule's gauge action at finite a is the rhombic action's OWN
  quadratic form, not the F26/Omega_even alternative -- which F308 Sec.3
  independently disqualified as non-periodic under the very reciprocal
  lattice the vertices live on, on structural grounds alone.  U1 checks --
  not assumes -- that the loop-word action `colour_theta.loop_action` sums
  over is EXACTLY `lpt_bcc_vertex`'s rhombic action (same generators, same
  order, exact set-equality of all 20 words).  Since that IS the object L6
  decided, F321 Sec.3-4 were already sitting on the settled branch throughout
  -- not merely one that survives an unresolved fork.

  Item 2 -- non-perturbative theta-sectors.  F321 T1a MEASURED Im(S) ~ 1e-14
  on three Haar-random configurations.  U2 proves it instead: the rule's
  loop-word reversal (T0a, exact combinatorics) composed with the exact
  geometric identity `holonomy(reverse(w)) = dagger(holonomy(w))` (checked
  here to machine precision, ~5e-16) and the trivial trace identity
  `Tr(dagger(M)) = conj(Tr(M))` proves Im(S) = 0 EXACTLY for every SU(3) link
  configuration on this lattice -- no restriction to smoothness, disorder
  level, or topological content.  U3 is a 12-seed regression sweep on top of
  that proof (F321 T1 used 3).

  What this does NOT do: decide whether the lattice's clover-based
  topological charge Q is a properly quantized, admissibility-bounded
  invariant in the continuum-limit sense (a genuinely separate lattice-QCD
  question, well documented in the standard literature -- Luscher's
  admissibility condition and fermionic/gradient-flow definitions of Q exist
  precisely because a naive field-theoretic Q is not integer-valued at finite
  a).  See the finding for the theta=0-by-construction argument this DOES
  make (Z as literally defined here, an unrestricted sum over ALL link
  configurations with a real, Q-independent-in-phase weight, already IS the
  theta=0 member Z(0) = sum_Q Z_Q of the standard family
  Z(theta) = sum_Q e^{i theta Q} Z_Q -- by direct comparison to the
  definition, not by an added dynamical argument) and the Vafa-Witten (1984)
  cross-check it motivates.

  Nothing here claims theta-bar = 0, that strong CP is solved, or that arg
  det M_q at three generations (E6/E7) is addressed.  CL279's non-claim
  stands untouched.
"""
import json
import os
import sys


def _bootstrap():
    """Import the module by path so this driver runs from a bare checkout too."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import colour_theta as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_strong_cp_nonperturbative()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
        if c["note"]:
            print(f"          {c['note']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results", "F340_strong_cp_nonperturbative.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["n_pass"] == res["n_total"], (
        "F340 gate failed: " + json.dumps(
            [c for c in res["checks"] if not c["ok"]], default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
