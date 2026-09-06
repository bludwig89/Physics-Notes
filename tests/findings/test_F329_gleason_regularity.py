"""F329 — A6r: closing the Cooke-Keane-Moran / Gleason regularity residual.

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_gleason_regularity.check_gleason_regularity`
(record `F329-gleason-regularity`, tier gate), so this file deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven
records from file collection so nothing runs twice under two contracts.

    casim test --id F329-gleason-regularity
    casim test --id F329-gleason-regularity --param control=True   # red on H2/H3 only

F304 section 5.5 named exactly one residual after proving the frame-function
dichotomy for f in L^2: "Gleason's theorem holds for merely BOUNDED f, and
the bridge -- a non-negative frame function is automatically continuous --
is the Cooke-Keane-Moran regularity lemma, ... not reproved here."

This closes it by reproducing/adapting the IDENTICAL proposition already
proved in Gleason's own 1957 paper (Theorem 2.8, using the same non-negativity
and compactness Theorem 2.3 already assumed -- no appeal to CKM's separate,
later, lower-prerequisite proof of the same fact is needed), combined with the
reduction to any Hilbert space of dimension >= 3 (Lemma 3.3 / Theorem 3.5, via
"completely real" subspaces).  See the module docstring's "What is cited vs
adapted vs verified" section for the precise boundary between what is CITED
from the primary 1957 source, what is ADAPTED to this model, and what is
independently VERIFIED by this file's checks.

The legs that matter for reading the result:

  H1  Theorem 3.5's hypothesis (dim >= 3 admits a completely real 3-dim
      subspace) machine-checked for every dimension this model actually
      builds a Born-rule measurement context on (F304 section 1.1, F312 G7),
      PLUS a negative control confirming F304's own d=2 hole is correctly
      excluded rather than papered over by this check.

  H2  The frame condition itself (sum over MANY random orthonormal bases of
      R^3 is constant), the converse half of Gleason's Lemma 2.1, checked on
      a genuine regular (quadratic-form) frame function.  Must go RED under
      `control=True`, which adds F304 section 3.1's own P_3(x_1) mode -- a
      k=3 harmonic F304 section 5.3 proves is NOT annihilated by the frame
      condition at d=3.

  H3  The equator-constancy identity Theorem 2.8's own proof turns on:
      g(q) = f(q) + f(uq) is EXACTLY constant over the equator of a pole p,
      because {p, q, uq} is an orthonormal triple.  Must go RED under the
      same control, for the same reason -- the identity is a CONSEQUENCE of
      the frame condition, not an independent fact.

What this file will NOT assert, deliberately:

  * that Gleason's Lemmas 2.5-2.7 (the oscillation-propagation covering
    argument that turns "small oscillation somewhere" into "continuous
    everywhere") have been independently re-derived here.  They are CITED
    from the primary 1957 text, not re-proved -- see the module docstring.
  * that a genuinely non-measurable (Hamel-basis) frame function has been
    exhibited failing the identity.  Neither is possible on a computer, and
    it is not what closes the residual: what closes it is that the
    PROPOSITION F304 section 5.5 named is Gleason's own peer-reviewed
    theorem, whose hypothesis (dim >= 3) is what H1 verifies transfers.

Run standalone:  python3 tests/findings/test_F329_gleason_regularity.py
"""

from __future__ import annotations

import json

from casim.engine.interactions.qi_gleason_regularity import check_gleason_regularity


def main() -> dict:
    res_honest = check_gleason_regularity(control=False)
    res_control = check_gleason_regularity(control=True)

    print(json.dumps(res_honest["checks"], indent=2, sort_keys=False))
    print(f"\nhonest:  {res_honest['n_pass']}/{res_honest['n_checks']} PASS")
    print(f"control: {res_control['n_pass']}/{res_control['n_checks']} PASS "
          f"(H2/H3 must be exactly the two that flip red)")

    assert res_honest["all_pass"], (
        f"only {res_honest['n_pass']}/{res_honest['n_checks']} legs passed "
        "in the honest (control=False) run")

    control_checks = {c["id"]: c["pass"] for c in res_control["checks"]}
    assert control_checks["H2"] is False and control_checks["H3"] is False, (
        "the control (added P_3 mode) must turn H2 and H3 red -- "
        f"got {control_checks}")
    for cid, ok in control_checks.items():
        if cid in ("H2", "H3"):
            continue
        assert ok, f"control leg {cid} must stay green -- it does not touch H2/H3's input"

    result = {"honest": res_honest, "control": res_control}
    return result


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    result = main()
    out = results_path("F329_gleason_regularity.json")
    with open(out, "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote", out)
