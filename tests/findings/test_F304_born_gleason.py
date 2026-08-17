"""F304 — the Born rule as a theorem on the lattice (completeness row A6).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_born_gleason.check_born_gleason` (record
`F304-born-rule-gleason`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F304-born-rule-gleason
    casim test --id F304-born-rule-gleason --param coupling=contextual
    casim test --id F304-born-rule-gleason --param locality=nonlocal
    casim test --id F304-born-rule-gleason --param gleason_dim=2
    casim test --id F304-born-rule-gleason --param zonal=naive

Each of those four perturbations must go RED, on a different leg; they are
verified in `main()` below rather than being asserted only in prose.

What this finding does, in one paragraph
----------------------------------------
Gleason's theorem says a non-contextual additive weight on the rays of a space
of dimension >= 3 IS <v|rho|v>.  It is not used as a derivation of the Born rule
in ordinary QM because both premises are free assumptions there.  In this model
neither is: a measurement needs a RECORD and a record needs cells, so the
smallest measurement Hilbert space is 4 (B1); and the record channel is
H_int = sum_x alpha_hat(x) (x) n_hat(x), a FIXED OPERATOR OF THE RULE that
carries no reference to the measured basis, so two contexts sharing a ray write
the same record (B2), while remote contexts are blocked by exact no-signalling
(B3).  Gleason then forces w(v) = |<v|psi>|^2.  F281 leg 1's hypothesis --
"branch weights are a function of the amplitudes at all" -- becomes a
CONCLUSION, and its ell^2 result a corollary of Tr rho = 1 (B6b).

The sixteen checks, by leg:

  B1  the model owns NO two-dimensional measurement context.
      B1a  {n_hat(x)} is maximal abelian (commutant dim 2^n) -> exactly one
           pointer context, recomputed here because B2 stands on it.
      B1b  with zero record cells |D(t)| is identically 1: no record, no
           outcome.  So dim >= 2^(1+1) = 4 > 2, structurally.
      B1c  the free step's 2-dim momentum blocks ARE invariant (leakage
           2.2e-16) but are NOT pointer contexts: ||[Pi_k, n_hat]|| = 0.17539,
           matching sqrt(2/N - 2/N^2) with residual 0.0.  Invariant but
           unreadable -- this is the objection that had to be answered.

  B2  non-contextuality is a property of the GENERATOR, not of the experimenter.
      B2a  five contexts sharing a ray write the same record (ray infidelity
           2.2e-16); the basis-referencing control gives 0.4916.
      B2b  the same for the weight: spread 0.0 literal; control 0.1549.
      B2c  routing the ray to a different pointer slot writes a different
           record but must not move the weight -- 2.2e-16.  Outcome LABELS are
           not contexts, and permutation symmetry is measured separately rather
           than folded into B2a.

  B3  remote non-contextuality is no-signalling.
      B3a  A varies WHICH BASIS she measures; B's marginal moves by 9.7e-17.
           The non-local control (A's system coupled to B's record cells, a term
           outside the F227 cone) moves it by 0.1985.

  B4/B5  the dichotomy, computed, so that B1 is load-bearing.
      B4a  an explicit non-Born frame function at d=2: frame condition to
           1.1e-15, best-fit density-operator residual 0.14713.
      B4b  the same family at d=3 is not a frame function at all: spread
           0.35724 over 4000 orthonormal triads.
      B5a  frame-function space dimension = d^2 at d=3,4 for every degree.
      B5b  at d=2 it is 1 + sum_{odd l<=deg}(2l+1) = 4, 4, 11, 11, 22, 22 --
           every entry matching its closed form as an INTEGER, unbounded.
      B5c  the d>=3 solution space IS the Hermitian forms (5.7e-15).

  B7  the theorem itself, PROVED rather than cited.
      Averaging the frame condition over the bases containing a fixed ray gives
      f + (d-1)Bf = W with B the mean over the unit sphere of v^perp.  B is
      U(d)-equivariant, hence scalar on each isotypic component of
      L^2(CP^{d-1}), with b_k = (-1)^k / C(k+d-2,k).  A component survives iff
      1 + (d-1)b_k = 0, and that ONE formula gives both halves of the dichotomy.
      B7a  B's spectrum matches the closed form with dim V_k multiplicities,
           at (d,k) = (2,1),(2,3),(3,1),(3,2),(4,1),(4,2), <= 1.6e-15, and the
           function-space dimension matches sum_j dim V_j as an integer.
      B7b  1 + (d-1)b_1 = 0 EXACTLY (Fraction arithmetic), d = 2..12.
      B7c  d >= 3, k >= 2: strictly positive, min gap 0.5, k <= 40 -- because
           C(k+d-2,k) is strictly increasing and exceeds d-1 for k >= 2.
      B7d  d = 2: survivors are EXACTLY the odd k.  The hole is derived, not
           exhibited by example.
      B7e  the proof PREDICTS B5a/B5b as integers with no fitting:
           1 + sum_{k odd <= deg} (2k+1) = 4,4,11,11,22,22 at d = 2, and
           1 + dim V_1 = d^2 at d >= 3.

  B6  closure.
      B6a  the model's own record channel returns |<v|psi>|^2 (2.2e-16).
      B6b  ell^2 uniquely conserved by a genuine BCC Weyl tick, called through
           F281's own `lp_conservation_bcc` so the two findings cannot drift.

NOT claimed: the B7 proof is complete for f in L^2.  Gleason's theorem holds for
merely BOUNDED f, and the bridge -- a non-negative frame function is
automatically continuous -- is the Cooke-Keane-Moran regularity lemma, cited not
reproved.  That is the only external step left, and its content is the exclusion
of NON-MEASURABLE weight assignments.  One premise also remains irreducible --
that an exhaustive set of records carries weights summing to one -- and that is
the definition of the object being derived, not a physical input.
"""
from __future__ import annotations

import json
import os

# Imports live inside `main()` deliberately: `tools/audit_tests.py --ratchet`
# counts import-time physics, and nothing here needs to run at collection.

CONTROLS = (
    ({"coupling": "contextual"}, ("B2a", "B2b")),
    ({"locality": "nonlocal"}, ("B3a",)),
    ({"gleason_dim": 2}, ("B5a",)),
    ({"zonal": "naive"}, ("B7a",)),
)


def main() -> int:
    from casim.engine.interactions.qi_born_gleason import check_born_gleason
    from casim.engine.particles._results_path import results_path

    res = check_born_gleason()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['id']:10s} {c['desc']}"
              f"  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["all_pass"], (
        "F304 checks failed: "
        f"{[c['id'] for c in res['checks'] if not c['pass']]}")

    print("\n  declared controls (each must go RED, on its own leg):")
    ok = res["all_pass"]
    for params, expected in CONTROLS:
        out = check_born_gleason(**params)
        red = tuple(c["id"] for c in out["checks"] if not c["pass"])
        good = red == tuple(expected)
        ok = ok and good
        print(f"    {'OK  ' if good else 'BAD '} {params} -> red {red} "
              f"(expected {tuple(expected)})")
        assert good, (
            f"declared control {params} reddened {red}, expected "
            f"{tuple(expected)} -- a control that does not fire on its own leg "
            f"is not a control")

    dest = results_path("F304_born_rule_gleason.json")
    with open(dest, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("\n  wrote", os.path.basename(dest))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
