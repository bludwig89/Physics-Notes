"""F382 -- d1 leg 3, next candidate after F350's excluded WS-mask hypothesis.
F350 Sec.5/7 named two untested mechanisms for d1 leg 3's anomalous slow
convergence: (a) the vertex form factors' own behaviour / the phys-branch
projection, (b) the g_s=1/2 monotonicity assumption. This record attacks (a):
G7/F305 proves the propagator's own quadratic form is EXACTLY invariant
under the BCC reciprocal lattice, which is the argument F305/F280/F337 use
to justify integrating the FULL loop (vertex and propagator together) over
just the Wigner-Seitz quarter of the cube. That invariance is measured here
to NOT extend to the vertex-derived numerator M (tens-of-percent deviation
under the identical shift). The natural remedy this raises -- integrate over
the full cube instead of the WS quarter, in case the WS restriction is
dropping genuine vertex contributions -- is tested directly and found to
make convergence WORSE (divergence past 1, both branches), not better,
ruling the candidate out and reinforcing F337's L6 decision (domain='ws',
branch='phys') on an independent axis. See findings/F382-*.md.

Registry record `F382-vertex-domain-periodicity`, tier gate, entry
`check_d1_vertex_domain_f382` on `casim.engine.gauge.lpt_d1_action_consistent`.
"""
import warnings

import pytest

from casim.engine.gauge.lpt_d1_action_consistent import (
    check_d1_vertex_domain_f382, domain_choice_divergence, vertex_g_periodicity,
)

warnings.filterwarnings("ignore", category=RuntimeWarning)

NS = (6, 8, 10, 12, 14, 16, 18, 20)


def test_propagator_control_confirms_G7_invariance():
    """Sanity anchor: the SAME measurement methodology, pointed at the
    propagator instead of the vertex kernel, must reproduce G7's exact
    invariance to near machine precision."""
    r = vertex_g_periodicity(control_use_propagator=True)
    assert r["pass"]
    assert r["worst_rel_dev"] < 1e-10, r


def test_vertex_kernel_is_not_G_periodic():
    """The vertex-derived numerator M does NOT share the propagator's exact
    invariance under the BCC reciprocal lattice -- new, disclosed fact."""
    r = vertex_g_periodicity()
    assert r["pass"]
    assert r["worst_rel_dev"] > 0.05, r


def test_cube_domain_diverges_worse_than_ws_both_branches():
    for branch in ("phys", "raw"):
        r = domain_choice_divergence(NS, branch=branch)
        assert r["pass"], (branch, r)
        assert r["bad_diverges"]


def test_b0_recovery_deviation_metric_is_not_used_for_the_short_range_false_positive():
    """Review regression (2026-09-10): a naive |1 - b0_recovery| endpoint
    comparison over ns=(6,8,10) misreads domain='cube' as converging, because
    that metric is non-monotonic through the sign crossing 'cube' passes
    through between n=8 and n=10. The fixed (monotonicity-based) criterion
    must NOT report pass=True on this short range -- it should honestly
    report "not enough signal yet" (pass=False), never a false convergence."""
    r = domain_choice_divergence(ns=(6, 8, 10))
    assert r["pass"] is False
    assert r["bad_diverges"] is False


def test_control_swapping_which_domain_is_asserted_good_reddens_the_leg():
    """Declared D9 control: assert the WRONG domain (cube) is the one that
    should stay bounded. A genuine measurement, not a hardcoded verdict,
    must fail this -- it is 'cube' that actually diverges."""
    r = domain_choice_divergence(NS, swap_control=True)
    assert r["good_bounded"] is False
    assert r["bad_diverges"] is False
    assert r["pass"] is False


def test_entry_point_forwards_swap_control_for_the_registry_level_D9_control():
    """Review regression: the registry's declared control perturbs the entry
    point itself (`swap_control`), not just the internal helper -- casim's
    own control-soundness checker caught this as INVALID before the entry
    point forwarded the parameter. Confirms the fix: the registry-declared
    control actually reaches and reddens this leg through the entry point."""
    r = check_d1_vertex_domain_f382(NS, swap_control=True)
    assert r["checks"]["cube_domain_does_not_fix_it"] is False
    assert r["pass"] is False


def test_record_writes_its_artifact():
    r = check_d1_vertex_domain_f382(NS)
    assert r["pass"], r["legs"]
    import json
    import os
    here = os.path.abspath(__file__)
    root = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    with open(os.path.join(root, "test-results", "F382_vertex_domain_periodicity.json"), "w") as f:
        json.dump(r, f, indent=1, default=str)


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
