"""F288 — Structure formation with zero free functions (K11).

Thirteen checks.  The load-bearing ones are S1/S2/D1/D2, which are sympy
literal zeros, and C1, which is the built-in proof that the numeric legs can
go red.

  S1  (exact)  A B == 1 forces the LINEAR-order gravitational slip coefficient
      to a literal zero. Asserted on the coefficient, not on a tolerance.

  S2  (exact)  F106's sourcing law collapses to Poisson with mu == 1 and
      d mu/d k == 0. Both sympy zeros.

  S3  (count)  Two free functions in the EFT of dark energy, zero in the
      model, from three DISTINCT sources. The distinctness is asserted --
      one fact wearing three hats would not be a constraint count.

  D1  (exact)  gamma_g = 6/11 exactly, and c = 1 iff mu = 1.

  D2  (exact)  Meszaros D(y) = 1 + (3/2) y, residual literal zero.

  D3a (computed)  D(1) against the Carroll-Press-Turner fitting formula --
      an INDEPENDENT published result, so this leg can genuinely fail.

  D3b (computed)  f sigma_8 vs seven RSD points. Diagonal chi^2, said so.

  D4  (computed)  sigma_8 within 4% of Planck with the import budget declared.

  D5  (computed)  mu pinned to ~1% by growth; the shape-only lower edge is
      asserted to be REPORTED AS ABSENT rather than quoted at the scan floor.

  B1  (bound)  Discreteness below 1e-100 even at the Lyman-alpha scale.

  B2  (computed)  sigma_8 is blind to K7's dark-matter identity; asserted
      as a NEGATIVE, so an accidental sensitivity would fail it.

  C1  (control)  mu = 0.90 turns three legs red. This leg passes only when
      the perturbed run FAILS -- if a refactor made growth insensitive to mu,
      it goes red and says so.

  F   (discipline)  Guard: the S8 falsifier must stay stated, and the module
      must keep asserting it has no screening mechanism.

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

from casim.engine.interactions import cosmology_anomalous_dimension as ad
from casim.engine.interactions import cosmology_growth as cg


def check_S1_zero_linear_slip() -> dict:
    r = cg.slip_from_impedance_match()
    assert r["slip_linear_coefficient"] == "0", r["slip_linear_coefficient"]
    assert r["linear_slip_is_exactly_zero"]
    assert r["AB_product"] == "1"
    assert abs(r["eta_residual_at_Phi_1e-5"]) < 1e-4
    assert r["Sigma"] == 1.0
    return r


def check_S2_mu_is_one() -> dict:
    r = cg.mu_from_f106_poisson()
    assert r["mu"] == "1", r["mu"]
    assert r["mu_is_exactly_one"] and r["mu_is_scale_free"]
    assert r["dmu_dk"] == "0"
    assert "sub-horizon" in r["regime"]          # the scope must stay stated
    return r


def check_S3_zero_free_functions() -> dict:
    r = cg.no_free_functions()
    assert r["eft_free_functions"] == 2
    assert r["model_free_functions"] == 0
    # The count is only a count if the sources really are distinct.
    assert r["n_distinct_sources"] == 3, r["distinct_sources"]
    assert r["screening_mechanism"] is None
    return r


def check_D1_growth_index() -> dict:
    r = cg.growth_index_exact()
    assert r["gamma_g_is_6_over_11"], r["gamma_g_exact"]
    assert r["gamma_g_exact"] == "6/11"
    assert r["c_is_exactly_1_iff_mu_is_1"]
    # mu != 1 must move the amplitude, or the order-0 leg proves nothing.
    assert abs(r["c_at_mu_0p90"] - 1.0) > 0.05, r["c_at_mu_0p90"]
    return r


def check_D2_meszaros() -> dict:
    r = cg.meszaros_exact()
    assert r["residual"] == "0", r["residual"]
    assert r["residual_is_literal_zero"]
    assert r["decaying_mode_is_zero"]
    return r


def check_D3a_growth_on_background() -> dict:
    r = cg.growth_summary()
    assert abs(r["D_vs_CPT_relative"]) < 3.0e-3, r["D_vs_CPT_relative"]
    assert abs(r["gamma_g_numerical"] - 0.55) < 0.02
    assert r["gamma_g_numerical"] > r["gamma_g_exact_limit"]
    assert r["f_radiation_sensitivity"] < 1.0e-3
    return r


def check_D3b_fsigma8() -> dict:
    s8 = cg.sigma8_from_As()["sigma_8"]
    r = cg.fsigma8_curve(s8)
    assert r["chi2_per_point"] < 2.0, r["chi2_per_point"]
    assert r["max_abs_pull"] < 3.0, r["max_abs_pull"]
    assert r["n_points"] == len(cg.RSD_DATA)
    assert "DIAGONAL" in r["caveat"]             # the caveat must stay attached
    return r


def check_D4_sigma8_budget() -> dict:
    r = cg.sigma8_from_As()
    assert abs(r["sigma_8_relative_to_planck"]) < 0.04, r["sigma_8"]
    # A_s must be declared free, in the artifact, every run.
    assert "FREE INPUT" in r["import_budget"]["A_s"]
    assert "not predicted" in r["claim"].lower() or "NOT predicted" in r["claim"]
    # n_s must be the LIVE number, so F288 and F295 cannot drift apart.
    assert r["n_s_used"] == ad.NS_OBS
    return r


def check_D5_mu_is_pinned() -> dict:
    r = cg.mu_bound_from_growth()
    a = r["amplitude_anchored"]
    assert a["mu_lo_1sigma"] <= 1.0 <= a["mu_hi_1sigma"]
    assert a["half_width"] < 0.05, a
    assert not a["hit_scan_limit"]
    assert r["dp_dmu_at_1"] == "3/5"
    # The weak bound must be reported as weak, not quoted at the scan floor.
    assert r["shape_only"]["hit_scan_limit"]
    assert "scan floor" in r["shape_only"]["honest_reading"]
    return r


def check_B1_discreteness() -> dict:
    r = cg.discreteness_bound()
    assert r["relative_correction_at_lyman_alpha"] < 1.0e-100
    assert r["relative_correction_at_R8"] < r["relative_correction_at_lyman_alpha"]
    assert r["cells_across_R8"] > 1.0e50
    return r


def check_B2_dm_free_streaming() -> dict:
    r = cg.dark_matter_free_streaming()
    # Asserted as a NEGATIVE: sigma_8 must NOT see the difference.
    assert not r["sigma8_discriminates"]
    assert r["sigma8_fractional_suppression"] < 1.0e-4, r["sigma8_fractional_suppression"]
    # ...and the half-mode must genuinely sit above the sigma_8 scale, or the
    # negative would be vacuous.
    assert (r["sterile_F266"]["half_mode_k_h_per_Mpc"]
            > 100 * r["sigma8_scale_k_h_per_Mpc"])
    assert "Lyman-alpha" in r["verdict"]
    return r


def check_C1_control_goes_red() -> dict:
    r = cg.control_goes_red()
    assert r["baseline_all_green"], "mu = 1 must be green before a control means anything"
    assert r["n_legs_that_went_red"] == 3, r
    assert abs(r["sigma8_fractional_shift"]) > 0.1
    assert r["delta_chi2"] > 10.0
    return r


def check_F_falsifier_stays_stated() -> dict:
    r = cg.s8_falsifier()
    assert r["has_screening"] is False
    assert r["mu_is_k_independent"] is True
    assert r["can_relieve_S8"] is False
    assert "FALSIFIED" in r["falsifier"]
    # The tension with DES Y6 is the thing that can fire; assert it is real.
    assert r["probes"]["DES_Y6_3x2pt"]["n_sigma"] > 2.0
    assert abs(r["probes"]["combined_CMB"]["n_sigma"]) < 1.0
    return r


CHECKS = (
    ("S1_zero_linear_slip", check_S1_zero_linear_slip),
    ("S2_mu_is_one", check_S2_mu_is_one),
    ("S3_zero_free_functions", check_S3_zero_free_functions),
    ("D1_growth_index_6_over_11", check_D1_growth_index),
    ("D2_meszaros_exact", check_D2_meszaros),
    ("D3a_growth_on_background", check_D3a_growth_on_background),
    ("D3b_fsigma8_vs_rsd", check_D3b_fsigma8),
    ("D4_sigma8_with_budget", check_D4_sigma8_budget),
    ("D5_mu_is_pinned_by_growth", check_D5_mu_is_pinned),
    ("B1_discreteness_bound", check_B1_discreteness),
    ("B2_dm_free_streaming", check_B2_dm_free_streaming),
    ("C1_control_goes_red", check_C1_control_goes_red),
    ("F_s8_falsifier", check_F_falsifier_stays_stated),
)


def check_all() -> dict:
    out = {name: fn() for name, fn in CHECKS}
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "K11: linear growth is fixed by the model's own gravity law with ZERO "
        "free functions where the EFT of dark energy has two -- mu = 1 with no "
        "k (F106/F178), no time dependence (F79/F284), no slip (F64 AB=1). "
        "gamma_g = 6/11 and the Meszaros solution are exact. mu is pinned to "
        "1.1% by the data. sigma_8 = 0.8204 is REPORTED with A_s declared free "
        "(K5), never claimed. The lattice is invisible by ~113 orders. sigma_8 "
        "is blind to K7's dark-matter identity; Lyman-alpha is not. Falsifier: "
        "no screening exists, so the DES Y6 low-S8 direction cannot be "
        "accommodated -- 3.0 sigma today."
    )
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    import os
    payload = check_all()
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    path = os.path.join(root, "test-results", "F288_structure_formation.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(payload, indent=2, sort_keys=True, default=str))
