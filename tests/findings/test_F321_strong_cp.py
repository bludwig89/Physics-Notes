"""F321 — strong CP: theta_QCD = 0 from the rule's loop set (completeness B11).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.colour_theta.check_strong_cp` (record `F321-strong-cp`, tier
gate), so this module deliberately defines no `test_*` functions --
`tests/conftest.py` hides entry-driven records from file collection so nothing
runs twice under two contracts.

    casim test --id F321-strong-cp
    casim test --id F321-strong-cp --param reverse_senses=false      # red
    casim test --id F321-strong-cp --param vertex_one_sense=true     # red
    casim test --id F321-strong-cp --param flat_links=true           # red

WHAT IS AND IS NOT CLAIMED.  This record does **not** solve the strong CP
problem, and it does not predict theta-bar.  Peccei-Quinn asks why a FREE
parameter is tiny; this rule has no slot for that parameter, which is a
different statement -- contingent on the rule being the right rule, and not a
relaxation mechanism.  The physical invariant is theta-bar = theta + arg det M_q:
the first term closes here, the second is the quark mass texture (open-derivations
E6/E7) and does NOT.

It also does not repair completeness B11's citation by itself.  B11's residual
quotes 3.3e-16 against F53, but F53 P5 measures the F27 COMPLEX-MASS phase and
F53's own Remaining section says strong CP "is a separate phase in the gluon
sector (F43), untouched here".  The number is correct and attached to the wrong
object; T5a/T5b record it under the quantity it measures.

  T0a-b the rule's 20 oriented minimal rhombi are CLOSED UNDER REVERSAL, and so
        is the 12-loop hypercubic reference set through the same code path.  This
        is the load-bearing input and control 1 removes it.
  T1a   Im S = 0 on Haar-random SU(3) 4-D configurations.  In Euclidean
        signature the theta-term is the UNIQUE purely-imaginary invariant, so
        this IS theta_QCD = 0 -- non-perturbatively, configuration by
        configuration.  S is returned complex and never Re()-projected.
  T1b   those configurations are 99.7 % disordered, so T1a is a cancellation
        inside a non-trivial sum of 20 x N_sites complex traces.
  T1c-d S is CP- and P-invariant.
  T2a-e every position-space vertex coefficient is REAL at LITERAL zero at 2, 3
        and 4 legs, colour indices SAMPLED -- and the 3-point vertex is the one
        the 2026-06-29 audit's G1 caveat named as unanalysed.  Because the class
        of functions obeying V(-k) = conj(V(k)) is closed under products and
        under q -> -q symmetric loop integration, the effective action obeys it
        at EVERY order: no loop generates an imaginary part, i.e. no loop
        generates theta.  That is the audit's item.
  T3a-b the two 4I projections are exact, and the clover Q = sum_a E^a.B^a is
        NON-ZERO -- without which T1 and T2 would be statements about an
        operator this lattice does not carry.
  T3c   injecting theta by hand gives Im S = -theta * sum Q EXACTLY.  The slope
        IS the topological charge, so T1a has FULL sensitivity and its zero is a
        measurement rather than an absence.
  T3d   the discrete symmetry is exact: S invariant under U -> U*, the one-sense
        loop functional odd under it at literal zero.
  T4a-b the fork-robustness leg.  lpt_bcc_vertex declares that the F26 rotation
        law and the rhombic plaquette action disagree at finite momentum and does
        not choose, so the argument is run on the other branch too: the EVEN law
        is P-even, the retained CHIRAL law is not, and theta E.B is P-odd.
  T5a-c theta-bar's second term.  At one generation arg det M_q is not merely
        theta-independent, it is ZERO (F53 quotes the off-diagonal PRODUCT, -m^2;
        the determinant is minus that), so theta-bar = 0 + 0 with the two zeros
        coming from different places.  At three generations it is E6/E7 and open.

THE THREE CONTROLS REDDEN DISJOINT LEG SETS.  Dropping the reversed half of the
loop set kills the non-perturbative reality block and leaves the vertices and the
non-vacuity legs standing; doing the same to the vertex generator kills only the
vertex block; flattening the links kills only the non-vacuity legs.  So the
non-perturbative result, the perturbative result and the sensitivity of the
measurement rest on three different objects, and the record measures that.

CONTROL 2 FOUND A DEFECT IN THIS FINDING'S OWN FIRST DRAFT, which is the reason
it exists.  The first vertex probe used lpt_bcc_vertex.terms's hardcoded colour
assignment [T^0, T^1, T^2] and stayed GREEN under control 2 -- the one-sense loop
set passed a reality test while its action's imaginary part was a visible O(A^3).
The imaginary part lives in the antisymmetric f^{abc} structure, which a
fixed-index probe cannot see.  `_terms_colour` samples colour indices instead.

MEASURED AND NOT USED: the clover's finite-a parity eigenvalue.  parity_map is an
exact symmetry of the action (T1d), but Q does NOT map to -Q under it at finite
lattice spacing -- relative defect 0.42-0.83, and it does NOT fall as the field
weakens.  So "E.B is P-odd" is used as a CONTINUUM statement only and every
load-bearing leg rests on reality / U -> U* instead.  See F321 sec.7.
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
    res = m.check_strong_cp()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
        if c["note"]:
            print(f"          {c['note']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results", "F321_strong_cp.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["n_pass"] == res["n_total"], (
        "F321 gate failed: " + json.dumps(
            [c for c in res["checks"] if not c["ok"]], default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
