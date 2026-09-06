"""F337 — ledger row L6 decided: the rhombic action's own quadratic form is the
propagator (not the F26/Omega_even rotation-law K_true_4d), and the redundant
link-axis mode is not dynamical. The native n=28-40 sweep the ledger called for
is run (memory-bounded so it fits on a 4 GB machine) and does NOT close d1 leg
3 -- it sharpens the tension instead. See findings/F337-*.md for the full
technical account; this record covers only the gate-cheap leg-1 test. The
leg-2 (branch fork) and leg-3 (quotability) native-sweep evidence lives in the
committed result_dump artifacts, not re-run here at full n.

Registry record `F337-l6-propagator-choice`, tier gate, entry
`check_l6_decision` on `casim.engine.gauge.lpt_d1_action_consistent`.
"""
import math
import warnings

import pytest

from casim.engine.gauge.lpt_d1_action_consistent import (
    check_l6_decision, pi_loop, pi_loop_chunked, propagator_scheme_divergence,
)

warnings.filterwarnings("ignore", category=RuntimeWarning)

NS = (6, 8, 10, 12)   # gate-tier grid; the finding's native sweep is n=24-40


def test_chunked_path_is_bit_identical_to_the_unchunked_path():
    """pi_loop_chunked must reproduce pi_loop exactly -- it exists ONLY to fit
    larger n in bounded memory, not to change the physics."""
    for branch in ("phys", "raw"):
        Pi1, tax1 = pi_loop("bcc", 0.3, 8, branch)
        Pi2, tax2 = pi_loop_chunked("bcc", 0.3, 8, branch, chunk=3)
        assert tax1 == tax2
        assert float(max(abs((Pi1 - Pi2).flatten()))) < 1e-12


def test_L6_leg1_own_quadratic_form_converges_and_swap_diverges():
    """The decisive empirical test (F305 sec.7.4: the machinery is
    action-agnostic, testing the alternative costs one function). Paired with
    the SAME rhombic vertices, the action's own quadratic form's b0-recovery
    deviation from 1 must not worsen with n; the F26/Omega_even K_true_4d
    substitution must get WORSE, because that kernel is not periodic on the
    reciprocal lattice the vertices are exactly periodic under (F308 sec.3)."""
    r = propagator_scheme_divergence(NS)
    assert r["own_dev_nonincreasing"], r
    assert r["swap_diverges"], r
    assert r["pass"]


def test_control_swapping_the_roles_reddens_the_leg():
    """Declared D9 control: assign the roles the other way (own_fn <-> swap_fn).
    A genuine measurement, not a hardcoded verdict, must flip both conditions."""
    r = propagator_scheme_divergence(NS, swap_control=True)
    assert r["own_dev_nonincreasing"] is False
    assert r["swap_diverges"] is False
    assert r["pass"] is False


def test_record_writes_its_artifact():
    r = check_l6_decision(NS)
    assert r["pass"], r["legs"]
    import json
    import os
    here = os.path.abspath(__file__)
    root = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    with open(os.path.join(root, "test-results", "F337_l6_decision.json"), "w") as f:
        json.dump(r, f, indent=1, default=str)


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
