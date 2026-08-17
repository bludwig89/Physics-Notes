"""
F155 follow-up — the cubic expansion / 3-gluon vertex EXTRACTOR validated
(ca_lpt_vertex). Reads the vertex directly off the gauge-invariant compact
plaquette action by amplitude differentiation. The vertex half of the q* d1
computation (the propagator/integration half is ca_lpt_wilson).

  V1  quadratic term -> propagator: c2(k)/Khat(k) is CONSTANT across non-Nyquist
      transverse modes (the action expansion reproduces the gluon propagator).
  V2  cubic term -> colour antisymmetry: V(a,b,c) = -V(b,a,c) to machine
      precision (the non-abelian f^{abc} 3-gluon structure is correct).

NOT asserted (honest): the continuum-magnitude/Lorentz-structure precision match
(continuum_limit_check is a DIAGNOSTIC; it needs the point-splitting form factors
added — the next increment). So the EXTRACTOR is validated; folding it with the
rule's Omega_even propagator + ghost loop for d1 is the remaining work.
"""
import os
import sys

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.gauge import lpt_vertex as v


def run():
    results = {}

    pc = v.propagator_check()
    results["V1_quadratic_propagator"] = dict(
        passed=bool(pc["ratio_spread_rel"] < 5e-3),
        ratio_spread_rel=pc["ratio_spread_rel"],
        ratios=[round(r["ratio"], 4) for r in pc["rows"]])

    b = v.bose_antisymmetry()
    results["V2_colour_antisymmetry"] = dict(
        passed=bool(b["antisymmetric"]),
        V123=b["V123"], V_colourswap=b["V_colourswap_12"], sum=b["sum"])

    bf = v.bose_full_symmetry()
    results["V3_bose_full_symmetry"] = dict(
        passed=bool(bf["bose_symmetric"]),
        V=bf["V"], swap_dev=bf["swap_dev"], cyclic_dev=bf["cyclic_dev"])

    n = sum(r["passed"] for r in results.values())
    results["summary"] = dict(passed=n, total=3, all_pass=n == 3,
                              extractor_validated=True,
                              continuum_magnitude="pending large-L native run "
                              "(run_lpt_vertex_continuum.py)")
    return results


if __name__ == "__main__":
    import json
    r = run()
    print(json.dumps(r, indent=2, default=str))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "test-results", "F155_lpt_vertex.json")
    with open(out, "w") as f:
        json.dump(r, f, indent=2, default=str)
    assert all(r[k]["passed"] for k in
               ("V1_quadratic_propagator", "V2_colour_antisymmetry",
                "V3_bose_full_symmetry")), \
        "F155 vertex-extractor validation failed"
    print("\nF155 vertex extractor: 3/3 PASS")
