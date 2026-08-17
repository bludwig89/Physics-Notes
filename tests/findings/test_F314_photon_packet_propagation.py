"""F314 — the paired-spinor photon propagates across the lattice, at machine precision.

Registry records: `F314-pair-group-velocity-closed-form` (gate) and
`F314-photon-packet-propagation` (gate). The physics lives in
`casim.engine.gauge.photon_packet`; this file is the pytest face of it.

What this closes
----------------
F20 item (3) claimed "the photon exists and moves end-to-end" using the σ-bilinear
composite photon, which `S1-F69-sigma-bilinear-photon` retired. The F20 remediation
of 2026-08-03 withdrew that leg and left the replacement DEFERRED, so until now the
model had **no real-space demonstration that its own photon propagates**.

Why the assertions look the way they do
---------------------------------------
Each one is a defect from the F20 review, turned into a gate:

* **the target.** F20's photon leg fitted a centroid slope and compared it to
  ``c_lat``. A beam of finite transverse width does not travel at ``c_lat``; it
  travels at the packet-weighted ``⟨∂Ω_pair/∂k_x⟩``. C3 asserts the deficit is
  real (0.78%, four decades above the tolerance), so a test that passed against
  ``c_lat`` would be measuring nothing.
* **the box.** C2 asserts the boundary weight, and C6 asserts the *carrier*
  condition that turns out to matter just as much — see its docstring.
* **conservation.** F20's photon leg tracked a density that lost 37% of its
  weight over the run while quoting a conservation figure obtained from a global
  scalar phase applied with no lattice step at all. C4 measures the real thing on
  the moving packet.
* **exactness.** C1 asserts an exact zero at the ``u`` level with an off-axis
  control, rather than a small number at the ``Ω`` level.
"""
from __future__ import annotations

import pytest

from casim.constants import c_lat
from casim.engine.gauge import photon_packet as pp


def test_F314_onaxis_pair_identity_is_exact():
    """C1 — u^±(k/2 · x̂) = cos(k·c_lat/2) bit-for-bit, both branches, tolerance 0."""
    for sign in ("+", "-"):
        assert pp.onaxis_pair_u_residual(n_k=500, sign=sign) == 0.0


def test_F314_offaxis_control_is_not_zero():
    """C1b — the control. Off the axis the same identity fails at O(1) (0.723)."""
    assert pp.offaxis_pair_u_residual(n_k=500) > 1e-3


def test_F314_closed_form_matches_finite_differences_on_all_three_axes():
    """C1c — ∂Ω_pair/∂k_i vs a central difference of ``pair_dispersion``, i = x,y,z.

    All three axes is the point. The ``c_lat·n̂_i`` form that
    ``lattice.wavepacket`` uses passes on x (7.99e-11, the h² floor) and fails on
    y (0.574) and z (0.021) — see the F314 finding, §"Defect found in a
    neighbouring module". Testing only ``axis=0`` cannot tell the two apart.
    """
    res = pp.check_pair_group_velocity_closed_form()
    assert res["ok"], res["checks"]
    assert max(res["closed_form_residual_per_axis"]) <= 1e-8
    assert len(res["closed_form_residual_per_axis"]) == 3


def test_F314_onaxis_photon_velocity_is_exactly_c_lat():
    """C1d — an axis-aligned photon travels at ``c_lat`` at every k in the zone.

    Not a k → 0 limit: the on-axis cone is straight and its curvature is zero, so
    there is no lattice ``k²`` dispersion for axial propagation at any energy.
    (F105 states this; here it is guarded, with the endpoints excluded because
    ``sin ω`` vanishes there and the closed form is 0/0 by coordinate choice.)
    """
    assert pp.onaxis_pair_velocity_residual(n_k=500) <= 1e-10
    assert abs(pp.onaxis_pair_curvature(k0=0.8)) <= 1e-6


def test_F314_run_is_wrap_free():
    """C2 — the packet never reaches a boundary. This is what F20 got wrong."""
    r = pp.check_photon_packet_propagation()
    assert r["edge_weight"] <= pp.EDGE_WEIGHT_CEILING, r["edge_weight"]


def test_F314_drift_matches_closed_form_at_machine_precision():
    """C3 — measured centroid drift = ⟨∂Ω_pair/∂k_x⟩ to 1e-12, and NOT to c_lat.

    The tolerance is pre-registered and derived: at the asserted wrap ceiling the
    estimator bias is 2.2e-13 relative and the float64 FFT floor over 24 spectral
    rotations is the same order. The residual comes in at ~8e-16.

    The second assertion is the one that gives the first one teeth. The drift sits
    0.78% *below* ``c_lat`` because the beam has a finite transverse aperture —
    real physics, four decades above the tolerance — so this record could not have
    been passed by comparing against ``c_lat``.
    """
    r = pp.check_photon_packet_propagation()
    assert r["ok"], r["checks"]
    assert r["rel_err_drift"] <= pp.DRIFT_TOL
    assert r["deficit_measured"] > 1e-4
    assert r["asymptotic_drift"] < c_lat


def test_F314_energy_is_conserved_on_the_moving_packet():
    """C4 — Σ(|E|²+|B|²) constant to 1e-12 *during* the motion.

    The gate F20's item (3) could not pass: its ``Σ|G^i|²`` fell 1.000 → 0.628
    over 44 ticks and → 0.289 by tick 100, identically at every box size.
    """
    r = pp.check_photon_packet_propagation()
    assert r["energy_rel_drift"] <= 1e-12, r["energy_rel_drift"]


def test_F314_drift_is_polarisation_independent_and_has_no_transient():
    """C5 — bit-identical across polarisation axes, and no fit-window freedom.

    ``Ω_pair`` is a scalar rate, so rotating the polarisation cannot change the
    speed — measured difference exactly 0.0. And because the seed is one-sided
    there is no ±beat: the **first** tick already moves at the asymptotic speed
    (1.6e-14), where F20's fixed-spinor Weyl packet starts at exactly ``c_lat``
    and leaves 2e-4 in a whole-window least-squares fit.
    """
    r = pp.check_photon_packet_propagation()
    assert r["pol_independence"] == 0.0
    assert r["transient_frac"] <= 1e-8
    assert r["rel_err_lstsq"] <= 1e-11


def test_F314_undersampled_carrier_is_the_negative_control():
    """C6 — being wrap-free is a condition on the CARRIER, not only on the box.

    The seed is one-sided only up to the Gaussian tail of its own carrier. That
    tail runs *backwards* at ``−c_lat`` and reaches the boundary long before the
    packet does. At ``k₀σₓ = 3.14`` — the "``≳ 3``" that ``build_beam_packet``
    suggests — the boundary weight is 1.8e-8 and the residual degrades to ~1e-6,
    six decades worse, on the same box with the same physics.

    Asserting the failure is what makes ``one_sided_carrier`` a real check rather
    than a parameter that happened to be set well.
    """
    bad = pp.run_photon_packet(shape=(128, 48, 48), sigma=(4.0, 6.0, 6.0),
                               m_index=16, n_steps=20)
    assert bad["k0_sigma_axis"] < 5.0
    assert bad["edge_weight"] > 1e-10
    assert bad["rel_err_drift"] > 1e-9

    good = pp.run_photon_packet()
    assert good["k0_sigma_axis"] >= 5.0
    assert good["rel_err_drift"] < bad["rel_err_drift"] / 1e6


def test_F314_f105_small_angle_approximation_is_close_but_wrong():
    """C7 — the exact packet sum vs F105's ``1/(2(k₀σ⊥)²)``.

    F105 measured the aperture deficit at the percent level on a periodic box and
    reported "2.5% observed vs 2.3% predicted". The approximation is the right
    order and the right scaling and is wrong by ~5.8% *of the deficit*; the sum
    ``Σ w(k)·∂Ω_pair/∂k_x`` is the exact statement, and it is what lets the same
    physics close at 1e-15 instead of at 1e-2.
    """
    r = pp.check_photon_packet_propagation()
    assert 0.01 < r["approx_error_frac_of_deficit"] < 0.5
    assert r["deficit_f105_approx"] < r["deficit_predicted"]
    assert r["deficit_predicted"] == pytest.approx(r["deficit_measured"], rel=1e-12)
