"""
ca_ir_coupling.py — F152: the IR FACE of the strong coupling.

Context: the concurrent F151 (`ca_scheme_constant.py`) DETERMINED the UV face —
the rule's coupling is the V-scheme coupling (tree-exact, from F110's static
energy), the one-loop conversion to MSbar is the known a1=(93-10nf)/9, and the
residual is a matching scale q* in a derived sqrt(3) band; Lambda^(3)=347 MeV
(FLAG 1.1%).  Crucially, F151-S5 SPLIT OFF the IR face as a *distinct* object:
the self-consistent chiral-SB gap fixes an IR effective coupling
alpha_eff* = 0.376 (m_D=0.532) / 0.411 (m_V=0.727) ~ 0.39, "connected through
the full running but not identical" to the UV scheme constant.

This module develops that IR face:

  J1  the IR number: alpha_eff* ~ 0.39 (F151-S5 / F145 self-consistent gap,
      M(0)=1.50 = F77 constituent mass) — THE IR coupling value.
  J2  its SCALE is the dual-Meissner gluon mass gap m_D: the gap-massive
      propagator freezes the running at m_D, m_D/Lambda=O(1) -> finite alpha(0)
      -> the model is on the SATURATING (decoupling) branch, not Landau-pole.
  J3  continuum grounding: real QCD saturates (alpha_hat(0)/pi=0.97 [CZBR]) via
      a gluon mass gap m_g=0.5(2) GeV; the model makes that gap by mechanism
      (dual superconductor == IR saturation); alpha_eff*~0.39 is in the
      continuum frozen-coupling range (~0.3-0.5, MOM/V/APT schemes).
  J4  F150's E_g brake lambda_6 belongs to THIS face (the saturation regime),
      not the UV scheme constant -> the IR face owns both chiral SB and lambda_6.
  J5  distinct from F151's UV face; residual = the full nonperturbative
      crossover solve (self-consistent M(k); F101 Gaussian->confinement) that
      yields alpha_eff* without the F77 fit.

Numerics: numpy/stdlib; reuses ca_alpha_s_running (F144) for the running.
"""
from __future__ import annotations

import math

import ca_alpha_s_running as asr

# ----------------------------------------------------------------------
#  The IR-face number (from F151-S5 / F145 self-consistent resolved gap)
# ----------------------------------------------------------------------
ALPHA_EFF_STAR_mD = 0.376          # m_D = 0.532 (F88)
ALPHA_EFF_STAR_mV = 0.411          # m_V = 0.727 (F117)

# ----------------------------------------------------------------------
#  External anchors (TARGETS, not inputs) — with provenance
# ----------------------------------------------------------------------
ALPHA_HAT0_OVER_PI = 0.97          # process-independent charge, CZBR arXiv:1912.08232
M_G_GEV            = 0.50          # dynamical gluon mass, Landau-gauge lattice
M_G_ERR            = 0.20          #   (~0.5(2) GeV; 0.63-0.72 constant-fit)
SQRT_SIGMA_GEV     = 0.42          # model QCD-scale anchor (F122/F124/F146)
ALPHA_FROZEN_CONT_LO = 0.30        # continuum frozen-coupling range (MOM/V/APT)
ALPHA_FROZEN_CONT_HI = 0.50


# ======================================================================
#  J1 — the IR coupling value
# ======================================================================
def ir_coupling_value() -> dict:
    a = 0.5 * (ALPHA_EFF_STAR_mD + ALPHA_EFF_STAR_mV)
    return {"alpha_eff_star_mD": ALPHA_EFF_STAR_mD,
            "alpha_eff_star_mV": ALPHA_EFF_STAR_mV,
            "alpha_eff_star_mean": a,
            "spread_frac": (ALPHA_EFF_STAR_mV - ALPHA_EFF_STAR_mD) / a,
            "source": "F151-S5 / F145 self-consistent gap, M(0)=1.50 (F77)"}


# ======================================================================
#  J2 — the freeze scale is the gluon mass gap; saturating branch
# ======================================================================
def saturating_branch(loops: int = 2) -> dict:
    ch = asr.alpha_s_chain(asr.ALPHA_S_UV, asr.MU0_GEV, loops)
    lam3 = asr.lambda_msbar_2loop(ch["alpha_mc"], asr.M_C, nf=3)     # GeV
    b0 = 11.0 - 2.0 * 3 / 3.0                                         # nf=3 -> 9
    mD_gev = SQRT_SIGMA_GEV          # dual-Meissner scale ~ sqrt(sigma), O(0.5 GeV)

    def alpha_massive(Q2, m2, Lam2):
        arg = (Q2 + 4.0 * m2) / Lam2
        return 4.0 * math.pi / (b0 * math.log(arg)) if arg > 1.0 else float("nan")

    a0 = alpha_massive(0.0, mD_gev ** 2, lam3 ** 2)
    return {"Lambda3_GeV": lam3,
            "mD_scale_GeV(~sqrt_sigma)": mD_gev,
            "mD_over_Lambda": mD_gev / lam3,
            "mg_continuum_over_Lambda": M_G_GEV / lam3,
            "alpha0_massive_1loop": a0,
            "on_saturating_branch": (a0 > 0) and math.isfinite(a0),
            "mD_O1_vs_Lambda": 0.3 < mD_gev / lam3 < 5.0}


# ======================================================================
#  J3 — continuum grounding
# ======================================================================
def continuum_grounding() -> dict:
    a = ir_coupling_value()["alpha_eff_star_mean"]
    return {"alpha_hat0_over_pi": ALPHA_HAT0_OVER_PI,
            "m_g_continuum_GeV": M_G_GEV,
            "model_mD_scale_GeV": SQRT_SIGMA_GEV,
            "model_gap_matches_continuum": abs(SQRT_SIGMA_GEV - M_G_GEV) <= (M_G_ERR + 0.15),
            "alpha_eff_star_in_continuum_frozen_range":
                ALPHA_FROZEN_CONT_LO <= a <= ALPHA_FROZEN_CONT_HI,
            "continuum_frozen_range": [ALPHA_FROZEN_CONT_LO, ALPHA_FROZEN_CONT_HI],
            "branch": "saturating/decoupling — model generates m_D>0 (F88/F117); "
                      "dual superconductor and IR saturation are the same gap"}


# ======================================================================
#  J4 — lambda_6 (F150) belongs to the IR face
# ======================================================================
def lambda6_on_ir_face() -> dict:
    return {"lambda6_F150": 0.243,
            "belongs_to": "IR face (saturation regime), per F151-S5 split",
            "ir_face_owns": ["chiral SB (F145/F77)", "E_g sextic brake lambda_6 (F150)"],
            "not": "the UV scheme constant (F151: a1 + q* band)"}


# ======================================================================
#  J5 — distinct from F151's UV face; the residual
# ======================================================================
def relation_to_uv_face() -> dict:
    return {"uv_face": "F151: V-scheme + a1=(93-10nf)/9 + q* band; Lambda3=347 MeV",
            "ir_face": "this finding: alpha_eff* ~ 0.39, gap-saturated, scale m_D",
            "identical": False,           # F151-S5: connected by running, not identical
            "residual": "the full nonperturbative crossover (self-consistent M(k); "
                        "F101 Gaussian->confinement) that yields alpha_eff* without "
                        "the F77 fit"}


def report() -> dict:
    return {"J1_ir_value": ir_coupling_value(),
            "J2_saturating_branch": saturating_branch(),
            "J3_continuum_grounding": continuum_grounding(),
            "J4_lambda6": lambda6_on_ir_face(),
            "J5_uv_relation": relation_to_uv_face()}


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
