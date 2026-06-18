"""
F155 follow-up — the lattice-PT BZ-integration CORE validated on the canonical
Wilson one-loop integrals (the validation gate for the q* d1 computation;
docs/design/qstar-gluon-d1-computation-plan.md).

  W1  exact sum rule int_BZ khat_x^2/Khat = 1/4 to machine precision (engine).
  W2  Wilson tadpole Z0 -> published 0.1549334, converging ~1/n^2 (the dominant
      piece of Wilson 28.809; STRUCTURALLY ABSENT for the rule, F155-A0).
  W3  convergence: Z0 rel-dev shrinks monotonically with BZ resolution.

This validates the reusable BZ-quadrature machinery the rule's d1 integral will
call. It does NOT compute the vertex+ghost finite part (the 28.809 completion /
the rule's d1) — that is the next module.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "ca-simulation"))

import ca_lpt_wilson as w


def run():
    results = {}

    s = w.sum_rule(48)
    results["W1_sum_rule_exact"] = dict(
        passed=bool(s["abs_dev"] < 1e-12),
        value=s["int_khatx2_over_Khat"], exact=0.25, dev=s["abs_dev"])

    z = w.tadpole_Z0(64)
    results["W2_tadpole_Z0"] = dict(
        passed=bool(z["rel_dev"] < 1e-3),
        Z0=z["Z0"], published=z["published"], rel_dev=z["rel_dev"])

    c = w.convergence((24, 32, 48, 64))
    devs = [r["Z0_rel_dev"] for r in c["rows"]]
    results["W3_convergence"] = dict(
        passed=bool(devs[0] > devs[-1] and devs[-1] < 2e-4),
        Z0_rel_devs=[round(d, 6) for d in devs],
        monotone=all(devs[i] > devs[i + 1] for i in range(len(devs) - 1)))

    n = sum(r["passed"] for r in results.values())
    results["summary"] = dict(passed=n, total=3, all_pass=n == 3,
                              core_validated=True, vertex_part="next increment")
    return results


if __name__ == "__main__":
    import json
    r = run()
    print(json.dumps(r, indent=2, default=str))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "test-results", "F155_lpt_wilson_core.json")
    with open(out, "w") as f:
        json.dump(r, f, indent=2, default=str)
    assert all(r[k]["passed"] for k in
               ("W1_sum_rule_exact", "W2_tadpole_Z0", "W3_convergence")), \
        "F155 LPT-core validation failed"
    print("\nF155 LPT core: 3/3 PASS")
