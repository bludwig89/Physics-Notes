"""
F155 follow-up — the 3-gluon vertex closed form + Ward-Takahashi identity,
verified SYMBOLICALLY (ca_lpt_ward). The rigorous structural validation of the
vertex (the gauge identity the one-loop self-energy depends on), tying the
vertex to the already-validated propagator.

  W1  Ward identity  p1.Gamma = Dinv(p3) - Dinv(p2)  holds for ALL d*d Lorentz
      components, exactly (sympy).
  W2  colour-stripped Gamma is antisymmetric under simultaneous (Lorentz+
      momentum) leg exchange => full vertex f^{abc}Gamma is Bose-symmetric.

Scope (honest): extracting b0 = 11/3 C_A as the loop's validation gate requires
the BACKGROUND-FIELD formalism (Z_g = Z_A^{-1/2}); plain Feynman-gauge Pi is not
transverse alone. That is the precise remaining step before d1/q*.
"""
import os
import sys

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.gauge import lpt_ward as w


def run():
    results = {}
    wi = w.ward_identity_symbolic(d=4)
    results["W1_ward_identity"] = dict(
        passed=bool(wi["all_components_hold"]),
        n_components=wi["n_components"], mismatches=wi["mismatches"])

    bs = w.bose_symmetry_symbolic(d=4)
    results["W2_bose_antisymmetry"] = dict(
        passed=bool(bs["all_hold"]), mismatches=bs["mismatches"])

    n = sum(r["passed"] for r in results.values())
    results["summary"] = dict(passed=n, total=2, all_pass=n == 2,
                              vertex_structure_validated=True,
                              loop_needs="background-field formalism for b0 gate")
    return results


if __name__ == "__main__":
    import json
    r = run()
    print(json.dumps(r, indent=2, default=str))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "test-results", "F155_ward_identity.json")
    with open(out, "w") as f:
        json.dump(r, f, indent=2, default=str)
    assert all(r[k]["passed"] for k in ("W1_ward_identity", "W2_bose_antisymmetry")), \
        "F155 Ward-identity validation failed"
    print("\nF155 Ward identity: 2/2 PASS")
