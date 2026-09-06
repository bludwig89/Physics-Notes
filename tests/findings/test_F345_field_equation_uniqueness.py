"""F345 -- the induced Einstein equation is the only field equation the model's
own derived structure can carry.

Target: rubric row E1 / ledger E1g (fundamental field equation), POSIT.

This does NOT re-test the energy-only alternative, which is closed three times
over (F178: Lorentz covariance, no neutron-star maximum mass; F297: BBN
Y_p = 0.1856 at -17.6 sigma).  It tests the six legs that narrow what E1 still
posits, and the two alternative families closed by the model's own structure.
"""
from __future__ import annotations

from casim.engine.interactions.gravity_field_equation_uniqueness import (
    leg_L1_bianchi,
    leg_L2_variational_source,
    leg_L2b_conservation_on_shell,
    leg_L3_lovelock_dimension,
    leg_L4_truncation_suppression,
    leg_L5_scalar_tensor_closed,
    leg_L6_fR_closed,
    run_all,
)


def test_L1_bianchi_identity_constrains_any_source():
    r = leg_L1_bianchi()
    assert r["div_G_all_zero"], r["div_G_components"]
    assert r["div_g_all_zero"]
    # the zero is not vacuous: the metric family is genuinely curved
    assert r["curvature_nontrivial"]


def test_L2_metric_variation_delivers_the_full_tensor():
    r = leg_L2_variational_source()
    assert r["determinant_identity_ok"], r["determinant_identity_failures"]
    assert r["scalar_matches_textbook"] and r["scalar_symmetric"]
    assert r["maxwell_matches_textbook"] and r["maxwell_symmetric"]
    assert r["scalar_independent_components"] == 10


def test_L2b_source_conservation_is_the_matter_field_equation():
    r = leg_L2b_conservation_on_shell()
    assert r["identity_holds"], r["identity_residual"]
    # and off-shell the divergence does NOT vanish, so the identity has content
    assert r["offshell_divergence_nonzero"]


def test_L3_lovelock_vanishes_in_d4_and_not_in_d5():
    r = leg_L3_lovelock_dimension()
    assert r["d4_vanishes"]
    assert r["d5_does_not_vanish"]
    for row in r["d4"]:
        assert row["first_bianchi_ok"]
        # the Gauss-Bonnet SCALAR is non-zero while its VARIATION vanishes --
        # that contrast is the whole content of the leg
        assert row["GB_scalar_nonzero"]
        assert row["H_all_zero"]


def test_L3_control_dimension_five_turns_it_red():
    r = leg_L3_lovelock_dimension(lovelock_dim=5)
    assert not r["d4_vanishes"], "d=5 must NOT vanish -- the leg would be vacuous"


def test_L3_control_wrong_gauss_bonnet_coefficient_turns_it_red():
    r = leg_L3_lovelock_dimension(gb_ricci_coeff=-3)
    assert not r["d4_vanishes"], (
        "the -4 in R^2 - 4 R_ab R^ab + Riem^2 is what makes the variation "
        "topological; perturbing it must break the identity")


def test_L4_truncation_is_a_decade_not_a_bound():
    r = leg_L4_truncation_suppression()
    # Tightened from the original 1e-60, which left sixteen decades of slack and
    # would have passed if the figure were wrong by 1e15 (review 2026-09-01-b,
    # attack 4).  The worst proxy is sqrt(Kretschmann) at the lightest compact
    # remnant, 6.68e-76 -- so this brackets the actual decade.
    assert 1e-77 < r["worst_epsilon"] < 1e-74, r["rows"]
    assert "Kretschmann" in r["worst_regime"], r["worst_regime"]
    # the O(1) gravitational Wilson coefficient is NOT computed anywhere, and the
    # leg must keep saying so rather than implying F319 supplies it
    assert "UNCOMPUTED" in r["o1_coefficient_status"]
    assert r["a_m"] > 0


def test_L5_scalar_tensor_absent_for_want_of_a_parameter():
    r = leg_L5_scalar_tensor_closed()
    assert r["no_finite_solution"], r["finite_omega_solutions_of_gamma_eq_1"]
    assert r["gamma_bd_limit_omega_to_infinity"] == "1"
    # Only Gdot/G is independent of the AB == 1 / F106 pair that S4-F178
    # reclassifies; the original "3 independent sources" overstated it.
    assert r["structural_sources_total"] == 3
    assert r["independent_of_the_adopted_law"] == 1
    # and the leg must not be read as refuting Brans-Dicke
    assert r["refutes_brans_dicke"] is False
    assert len(r["families_not_addressed"]) == 3


def test_L5_control_gamma_not_exactly_one_reopens_it():
    r = leg_L5_scalar_tensor_closed(model_gamma="0.999999")
    assert not r["no_finite_solution"], (
        "the closure rests on gamma being EXACTLY 1; an approximate 1 admits a "
        "finite Brans-Dicke omega and the family is no longer closed")


def test_L6_fR_closed_on_both_branches():
    r = leg_L6_fR_closed()
    assert r["gamma_fR"] == "1/2"
    assert r["cassini_overshoot_factor"] > 1e4


def test_all_legs_pass():
    r = run_all()
    assert r["all_pass"], [l["leg"] for l in r["legs"] if not l["pass"]]
    assert r["n_legs"] == 8
