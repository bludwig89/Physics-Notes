"""F307 — the F280 subtracted estimator on one code path, each side on its own
action and its own Brillouin zone; and an F272/F277-class refold still live in
``lpt_selfenergy``.

Registry record `F307-action-consistent-d1`, tier gate, entry
`check_action_consistent_d1` on `casim.engine.gauge.lpt_d1_action_consistent`.

NOTE the record deliberately does NOT assert a value for dLoops.  Its S3 leg is
the quoting gate and is RED at these grids by design — see the finding's
"honest scope".  Asserting a number here is precisely the failure F287 sec.6
exists to prevent.
"""
import json
import math
import os

import pytest

NS = (6, 8)     # gate-tier grids; the finding quotes the n = 12/16/20 ladder

from casim.engine.gauge.lpt_d1_action_consistent import (
    budget_with_full_dloops, check_action_consistent_d1, delta_loops,
    refold_defect, transverse_B,
)


def _results_path(name):
    here = os.path.abspath(__file__)
    root = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    return os.path.join(root, "test-results", name)


def test_S1_shared_path_reproduces_the_wilson_pipeline_once_unrefolded():
    """The hypercubic branch of the shared code path agrees with the established
    ``lpt_selfenergy._pi_bgfield`` to round-off when that module's 2-pi refold is
    removed — and the refold is worth ~0.1 in the longitudinal component."""
    r = refold_defect()
    assert r["max_mismatch_when_unwrapped"] < 1e-12, r
    assert r["defect_size"] > 1e-3, r
    assert r["pass"]


def test_control_reintroducing_the_refold_reddens_S1():
    """The declared D9 control: put the 2-pi refold back into THIS path and the
    agreement must break, because being refold-free is what S1 asserts."""
    assert refold_defect()["pass"] is True
    assert refold_defect(wrap_control=True)["pass"] is False


def test_S2_estimator_runs_end_to_end_on_both_normalisations():
    d = delta_loops(NS)
    for key in ("series_slope_normalised", "series_analytic_normalised"):
        assert all(math.isfinite(v) for v in d[key]), d
    assert len(d["rows"]) == 2


def test_S3_is_red_and_that_is_the_point():
    """The quoting gate. b0 recovery is far from 1 on the BCC side at these
    grids, so no constant may be read off; the record records that rather than
    quoting a number without an error bar."""
    d = delta_loops(NS)
    assert d["worst_b0_recovery_deviation"] > 0.15, d
    assert d["quotable"] is False


def test_wilson_side_b0_recovery_is_the_healthier_one():
    """Sanity on the diagnostic itself: the hypercubic side, whose BZ is the cube
    it is integrated over, recovers b0 far better than the BCC side at equal n."""
    d = delta_loops(NS)
    for row in d["rows"]:
        assert abs(row["b0_recovery_wilson"] - 1.0) < abs(row["b0_recovery_rule_phys"] - 1.0)


def test_budget_still_closes_as_bookkeeping():
    """Feeding the measured dLoops into F280's leg-2 slot must keep the budget an
    identity — the arithmetic is not what is uncertain here."""
    b = budget_with_full_dloops(delta_loops(NS))
    assert b["closes_to_total"], b
    assert b["leg1_plus_leg3_is_anchor_fixed"], b
    assert b["quotable"] is False


def test_transverse_coefficient_is_finite_on_both_actions():
    for action in ("sc", "bcc"):
        v = transverse_B(action, 0.9, 10)
        assert math.isfinite(v)


def test_record_writes_its_artifact():
    r = check_action_consistent_d1(NS)
    assert r["pass"], r["legs"]                    # S1 and S2; S3 is red by design
    assert r["legs"]["S3_quotable"] is False
    with open(_results_path("F307_action_consistent_d1.json"), "w") as f:
        json.dump(r, f, indent=1, default=str)


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
