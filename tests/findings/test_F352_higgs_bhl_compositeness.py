"""F352 -- ledger E8 / parameter #18 (m_H = 125.25 GeV): does RG-improving the
F73/F77 Cooper-pair compositeness condition, anchored at the model's own
derived F79/F107 lattice cutoff Lambda = E_Planck/(a/ell_P), reproduce the
measured top and Higgs masses via a Bardeen-Hill-Lindner-style top-
condensation calculation?

F73 gives exact bound-pair kinematics but leaves the binding dynamics open.
F74 (contact well) and F77 (self-consistent NJL gap+RPA) both show the scalar
pinned at or above the m_sigma=2 m_c threshold at every coupling -- no
sub-threshold binding at mean-field order, and F77 names the remaining hard
build as "a full Bethe-Salpeter treatment". This record attempts a different,
standard, external route to the same class of question: RG-improve the same
compositeness relation (m_H(Lambda) = 2 m_t(Lambda)) from Lambda down to m_t
via the coupled 1-loop SM RGEs for (y_t, lambda), with Lambda fixed -- not
chosen for convenience -- by the model's own F79/F107 UV cutoff.

D1  Y0-convergence: the "y_t(Lambda) -> infinity" compositeness condition is
    implemented with a large finite stand-in Y0; the down-integrated IR
    values must be Y0-independent (the standard BHL "compositeness ray" /
    quasi-infrared-fixed-point criterion) or the whole calculation is not
    predictive.
D2  RG running must move the ratio m_H/m_t away from F77's flat, scale-free
    ceiling of exactly 2.0 -- otherwise RG improvement contributed nothing
    beyond F77 and this record would just be F77 restated.
D3  Both absolute masses must still overshoot measured (172.57 / 125.25 GeV)
    by a wide, quantified margin -- this is the honest verdict, not a
    reproduction of the measured values, and matches the historical verdict
    on minimal BHL top condensation at a GUT/Planck-scale cutoff (see e.g.
    the Top quark condensate literature: "the minimal model predicted a
    Higgs mass roughly double the observed value").

This record does NOT re-derive F73's kinematics, F74's contact threshold, or
F77's gap equation / RPA ladder -- those are used as given. It does not
re-attempt a literal lattice Bethe-Salpeter ladder (still open).
"""

from casim.engine.particles import derive_higgs_bhl_compositeness as mod


# ---------------------------------------------------------------------------
# A -- the model-native input: F79/F107's lattice cutoff, not a hand pick
# ---------------------------------------------------------------------------

def test_A_lambda_model_is_planck_scale_from_F107_ruler():
    out = mod.run_all()["B_lambda_model"]
    # a/ell_P = sqrt(8 pi) 3^(1/4) = 6.5978... (F79, exact; F107 canonical)
    assert abs(out["a_over_ellP"] - 6.59782) < 1e-3
    assert 1e18 < out["Lambda_model_GeV"] < 3e18


# ---------------------------------------------------------------------------
# B -- gauge couplings at m_t sane vs standard values
# ---------------------------------------------------------------------------

def test_B_gauge_couplings_at_mt_match_standard_SM_values():
    out = mod.run_all()["A_gauge_at_mt"]
    assert abs(out["alpha_s_mt"] - 0.109) < 0.01
    assert 0.60 < out["g2"] < 0.68
    assert 0.42 < out["g1"] < 0.50


# ---------------------------------------------------------------------------
# D1 -- Y0-convergence (compositeness-ray criterion)
# ---------------------------------------------------------------------------

def test_D1_Y0_convergence_below_0_1_percent():
    out = mod.run_all()["D_Y0_convergence"]
    assert out["spread_mt_pct"] < 0.1
    assert out["spread_mh_pct"] < 0.1


# ---------------------------------------------------------------------------
# D2 -- RG running moves the ratio away from F77's flat ceiling
# ---------------------------------------------------------------------------

def test_D2_ratio_moves_below_F77_flat_ceiling_of_two():
    head = mod.run_all()["C_headline"]
    assert head["ratio_mH_over_mt_pred"] < 2.0 - 1e-6
    # but RG running does not overshoot down to (or below) the measured ratio
    assert head["ratio_mH_over_mt_pred"] > mod.MH_OBS_GEV / mod.MT_GEV


# ---------------------------------------------------------------------------
# D3 -- both masses overshoot measured by a wide, quantified margin
# ---------------------------------------------------------------------------

def test_D3_mt_overshoots_measured_substantially():
    head = mod.run_all()["C_headline"]
    dev = (head["m_t_pred_GeV"] - mod.MT_GEV) / mod.MT_GEV
    assert 0.20 < dev < 0.45


def test_D3_mH_overshoots_measured_by_roughly_double():
    head = mod.run_all()["C_headline"]
    dev = (head["m_H_pred_GeV"] - mod.MH_OBS_GEV) / mod.MH_OBS_GEV
    assert 0.80 < dev < 1.20   # "roughly double" the observed mass


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def test_verdict_negative_and_all_legs_pass():
    out = mod.check_bhl_compositeness_prediction()
    assert out["pass"] is True, out["checks"]
    assert "negative" in out["verdict"].lower()
