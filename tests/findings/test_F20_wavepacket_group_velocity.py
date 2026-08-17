"""F20 — wavepacket group velocity on the BCC lattice, after the 2026-08-03 review.

Registry records: `F20-bcc-onaxis-dispersion-exact` (gate) and
`F20-wavepacket-group-velocity` (gate). The physics lives in
`casim.engine.lattice.wavepacket`; this file is the pytest face of it.

What the review changed, and why these assertions look the way they do
---------------------------------------------------------------------
The original finding compared a least-squares centroid slope on a **periodic**
64³ box against ``c_lat`` and reported 0.37%. Both halves of that were wrong:

* the box wraps within 44 ticks, and the resulting centroid bias runs the wrong
  way — at ``L_x = 192`` the fitted "velocity" exceeds ``c_lat``, which is by
  itself proof that the fitted quantity is not a group velocity there. So
  :func:`test_F20_run_is_wrap_free` asserts the boundary weight is ~0, and it is
  the load-bearing assertion of the whole file;
* the target was ``c_lat``, but a finite-width packet seeded with a **fixed**
  spinor moves at ``c_lat⟨n̂ₓ²⟩`` — tilt *and* branch admixture, which the
  finding's own text missed, and which is a factor of two in the deficit.

C1 asserts an **exact zero** at the ``u`` level rather than a small number at the
``ω`` level, and C2 is its control: the same residual off-axis must be O(1), so
C1 is testing a direction and not a tautology.
"""
from __future__ import annotations

import pytest

from casim.constants import c_lat
from casim.engine.lattice import wavepacket as w


def test_F20_onaxis_identity_is_exact():
    """C1 — u(k x̂) = cos(k·c_lat) bit-for-bit, both branches, tolerance 0."""
    for sign in ("+", "-"):
        assert w.onaxis_u_residual(n_k=500, sign=sign) == 0.0


def test_F20_offaxis_control_is_not_zero():
    """C2 — the control. Off the axis the same identity fails at O(1)."""
    assert w.offaxis_u_residual(n_k=500) > 1e-3


def test_F20_closed_forms_match_finite_differences():
    """C3 — all eight analytic checks, incl. the two closed-form group velocities."""
    res = w.check_group_velocity_closed_forms()
    assert res["ok"], res["checks"]
    assert res["onaxis_residual"] <= res["arccos_bound"]


def test_F20_run_is_wrap_free():
    """C4 — the packet never reaches a boundary. This is what F20 got wrong."""
    r = w.check_packet_velocity(m=0.3, seed="branch-pure")
    assert r["edge_weight"] <= 1e-12, r["edge_weight"]


@pytest.mark.parametrize("m,expected", [(0.3, 0.4654257818), (0.5, 0.3485063259)])
def test_F20_branch_pure_drift_is_machine_exact(m, expected):
    """C5 — branch-pure seed ⇒ centroid drift = ⟨∂ω/∂k_x⟩ to 1e-12.

    Both the measurement and the closed form move with ``m``, which is the
    failure mode the original record did not have.
    """
    r = w.check_packet_velocity(m=m, seed="branch-pure")
    assert r["ok"], r["checks"]
    assert r["rel_err_drift"] <= 1e-12
    assert r["asymptotic_drift"] == pytest.approx(expected, abs=1e-9)


def test_F20_fixed_seed_relaxes_to_the_doubled_deficit():
    """C6 — fixed-spinor seed ⇒ c_lat⟨n̂ₓ²⟩, i.e. ~TWICE the tilt deficit.

    The deficit is ~1.73% below ``c_lat``, not the ~0.87% that tilt alone
    (``c_lat⟨n̂ₓ⟩``) would give. The ratio is exactly
    ``(1−⟨n̂ₓ²⟩)/(1−⟨n̂ₓ⟩) = (1+⟨n̂ₓ⟩) − Var(n̂ₓ)/(1−⟨n̂ₓ⟩)``, which approaches 2
    from below as the packet narrows in k; here it is 1.981. Asserting the near-
    factor-of-two — and that it is strictly below 2 — is the point, because
    F20's stated mechanism gives the tilt-only value.
    """
    r = w.check_packet_velocity(m=0.0, seed="fixed")
    assert r["rel_err_drift"] <= 1e-6
    tilt_only = w.predicted_packet_velocity((256, 64, 64), (6.0, 10.0, 10.0),
                                            (0.8, 0.0, 0.0), seed="helicity")
    deficit_both = (c_lat - r["predicted_vg"]) / c_lat
    deficit_tilt = (c_lat - tilt_only) / c_lat
    ratio = deficit_both / deficit_tilt
    assert 1.9 < ratio < 2.0, ratio
    assert ratio == pytest.approx(1.9812700441, rel=1e-6)
