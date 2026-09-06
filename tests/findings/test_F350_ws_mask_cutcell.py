"""F350 -- an anti-aliased (cut-cell) Wigner-Seitz-cell mask, built to test
F337 Sec.4/6's named hypothesis for d1 leg 3's anomalously slow convergence
(the sharp 0/1 domain mask's O(1/n) staircase discretisation error). This
record covers only the gate-cheap module-correctness gates (G1: the
first-shell-only half-space test reproduces `lpt_bcc_vertex.ws_mask` exactly;
G2: the mask's own isolated volume-estimate error is far smaller than the
sharp mask's, and roughly flat in n). The NATIVE re-run of the physics loop
integral with this mask swapped in (whether it changes the measured
convergence rate) is NOT gate-tier -- see findings/F350-*.md and
test-results/smoothed_ws_mask_sweep_checkpoint.json.
"""
import pytest

from casim.engine.gauge.lpt_ws_mask_cutcell import (
    mask_isolation_convergence, shell1_matches_ws_mask, smoothed_ws_mask,
)

NS = (8, 12, 16, 20, 24, 28, 32, 36, 40)


def test_G1_first_shell_reproduces_ws_mask_exactly():
    for n in (8, 16, 24):
        r = shell1_matches_ws_mask(n=n)
        assert r["n_mismatch"] == 0, r
        assert r["pass"]


def test_G2_smoothed_mask_isolation_error_is_small_and_hard_mask_is_order_n_minus_1():
    r = mask_isolation_convergence(ns=NS, depth_max=5)
    assert r["slope_hard"] < -0.7, r  # the F337-diagnosed staircase order, ~-1
    assert max(row["smooth_err"] for row in r["rows"]) < 5e-3, r
    assert r["pass"]


def test_control_shallow_depth_fails_the_isolation_gate():
    """Declared D9 control: cutting the octree refinement to depth_max=1
    (barely any refinement past the initial ambiguous classification) must
    NOT meet the isolation gate's accuracy bar -- a hardcoded pass could not
    fail this way, only a genuine per-depth measurement can."""
    r = mask_isolation_convergence(ns=NS, depth_max=1)
    assert max(row["smooth_err"] for row in r["rows"]) >= 5e-3
    assert r["pass"] is False


def test_mask_is_a_real_partition_weight_in_0_1():
    w, n_amb = smoothed_ws_mask(16, depth_max=5)
    assert n_amb > 0
    assert float(w.min()) >= 0.0
    assert float(w.max()) <= 1.0
    # non-ambiguous cells keep their exact 0/1 value (proved by the interval
    # bound, not just measured) -- every weight is either in {0, 1} or was
    # part of the ambiguous set
    import numpy as np
    on_grid_binary = np.isclose(w, 0.0) | np.isclose(w, 1.0)
    assert int((~on_grid_binary).sum()) <= n_amb


def test_effective_depth_is_independent_of_node_budget():
    """Regression test for the bug an adversarial review of this finding's
    F350 caught 2026-09-02: an earlier version shared one node-count budget
    across the WHOLE ambiguous-voxel array, so the depth actually reached
    fell as the array (and therefore n) grew -- exactly backwards. The fixed
    batching scheme makes the result independent of the budget (as long as
    it is big enough for one batch): a MUCH larger budget must reproduce the
    SAME mask, at every n, including the largest tested here."""
    import numpy as np
    from casim.engine.gauge.lpt_ws_mask_cutcell import _cutcell_fraction
    for n in (24, 40):
        w_small, _ = smoothed_ws_mask(n, depth_max=5, node_budget=4_000_000)
        w_big, _ = smoothed_ws_mask(n, depth_max=5, node_budget=50_000_000)
        assert float(np.max(np.abs(w_small - w_big))) == 0.0, n
