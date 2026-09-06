"""F348 -- is the E1 charged-lepton shape residual (ledger row E1,
docs/status/open-derivations.md) closeable by a computed next-order correction,
or is it already measurement-floor-limited?

F175 D4 uses the two DERIVED numbers delta*=2/9 rad (F175, the exact E_g
representation weight) and eta^2=1/2 (F92, the derived Cooper-pair equipartition)
to predict the charged-lepton mass ratios with ZERO shape parameters: m_mu/m_e to
+0.001%, m_tau/m_e to +0.007% (F175 D4). F175 Sec.5 attributes the residual to
"the ~0.9 sigma eta2-delta tension (F174 S4) ... at current mass precision"
without quantifying it. E1 is graded QUANT x2; this record asks whether a
next-order correction is computable (not fit) from the model's own machinery, or
whether the residual cannot currently be distinguished from measurement noise.

  D1  Recomputes the exact-point vs PDG residual directly in MeV and in units of
      the current PDG m_tau uncertainty (+-0.12 MeV, the dominant error source --
      m_e and m_mu are known many orders of magnitude more precisely).
  D2  A numeric Jacobian of (m_mu/m_e, m_tau/m_e) with respect to (delta, eta2)
      at the exact point shows that the SAME small (delta, eta2) offset already
      flagged by F174 S4 (the free-fit values sitting ~1 sigma from {2/9, 1/2})
      reconstructs BOTH the 0.001% and 0.007% residuals simultaneously to <1%
      relative error -- one joint offset, not two independent unexplained
      corrections.
  D3  Computes the m_tau precision (PDG central value held fixed) at which this
      joint offset would reach 3-sigma or 5-sigma significance -- an explicit,
      falsifiable re-attack threshold.

This record does NOT re-derive delta*=2/9 (F175) or eta^2=1/2 (F92), and does
NOT re-litigate F256's route-(I) dynamical no-go (cos(3 delta*)=-B/(2C) cannot be
exact, independent sea-B/induced-C origins) -- F256's conclusion is used as
given: the model supplies no mechanism for an independent next-order term here,
so this record's verdict is a measurement-floor statement with a named re-attack
condition, not a fabricated correction.
"""

from casim.engine.particles import derive_lepton_shape_precision_floor as mod


# ---------------------------------------------------------------------------
# D1 -- direct residual, in MeV and in measurement sigma
# ---------------------------------------------------------------------------

def test_D1_reproduces_F175_D4_percentages():
    out = mod.run_all()["D1"]
    assert abs(out["pct_err_mu"] - 0.001) < 0.001
    assert abs(out["pct_err_tau"] - 0.007) < 0.001


def test_D1_tau_residual_is_about_one_sigma_not_more():
    out = mod.run_all()["D1"]
    # F76 C3 / F174 S1 independently quote ~0.9-0.91 sigma on closely related
    # (Q-based) metrics; the direct m_tau/m_e residual sigma should land in
    # the same ballpark, and in particular well under 2 sigma.
    assert 0.5 < abs(out["resid_tau_sigma"]) < 2.0


def test_D1_residual_MeV_matches_percentage_reading():
    out = mod.run_all()["D1"]
    # 0.007% of m_tau (~1776.86 MeV) is ~0.124 MeV -- cross-check the two
    # equivalent readings of the same residual agree.
    implied_MeV = out["pct_err_tau"] / 100.0 * mod.M_TAU
    assert abs(implied_MeV - out["resid_tau_MeV"]) / mod.M_TAU < 1e-3


# ---------------------------------------------------------------------------
# D2 -- one joint offset explains both residuals (not two independent ones)
# ---------------------------------------------------------------------------

def test_D2_jacobian_reconstruction_matches_both_ratios():
    out = mod.run_all()["D2"]
    assert out["rel_reconstruction_err_mu"] < 0.01
    assert out["rel_reconstruction_err_tau"] < 0.01


def test_D2_offsets_are_small_and_within_F174_S4_scale():
    out = mod.run_all()["D2"]
    # F174 S1: delta_fit=0.222229 vs 2/9=0.222222..., eta2_fit=0.4999908 vs 0.5
    assert abs(out["delta_offset"]) < 1e-4
    assert abs(out["eta2_offset"]) < 1e-4


# ---------------------------------------------------------------------------
# D3 -- explicit, falsifiable re-attack threshold
# ---------------------------------------------------------------------------

def test_D3_three_sigma_needs_a_few_times_better_m_tau():
    out = mod.run_all()["D3"]["thresholds"]["3"]
    assert 2.0 < out["improvement_factor"] < 4.0
    assert out["needed_unc_MeV"] < mod.M_TAU_UNC


def test_D3_five_sigma_needs_more_improvement_than_three_sigma():
    thresholds = mod.run_all()["D3"]["thresholds"]
    assert thresholds["5"]["improvement_factor"] > thresholds["3"]["improvement_factor"]
    assert thresholds["5"]["needed_unc_MeV"] < thresholds["3"]["needed_unc_MeV"]


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def test_verdict_precision_floor_all_legs_pass():
    out = mod.check_lepton_shape_residual_is_precision_floor_limited()
    assert out["pass"] is True, out["checks"]
    assert "precision philosophy" in out["verdict"].lower() or "measurement noise" in out["verdict"].lower()
    assert "quant x2" in out["verdict"].lower()
