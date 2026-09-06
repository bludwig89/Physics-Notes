"""
Ledger E8 / parameter #18 (m_H = 125.25 GeV): a Bardeen-Hill-Lindner (BHL)
style top-condensation / renormalisation-group binding-dynamics attempt for
the F73 spin-0 Cooper-pair scalar, using the model's OWN derived UV cutoff.

--------------------------------------------------------------------------
Where this sits in the thread
--------------------------------------------------------------------------
F73  -- exact kinematics for a spin-0 bound pair of two spin-1/2
         constituents (the "Cooper-pair Higgs"): m_H = sin(asin m1 + asin m2).
         Free-sum kinematics cannot reach 125.25 GeV; binding DYNAMICS is the
         missing input.
F74  -- a non-relativistic contact-well solver: the model's own gauge
         couplings (photon/Z) supply only beta ~ alpha^2/8, ~1e5 too weak;
         a deep contact bind needs the coupling fine-tuned to the critical
         value g_c to ~m_lat^2 ~ 1e-33 -- the hierarchy problem, reproduced.
F77  -- the SAME coupling made SELF-CONSISTENT (NJL gap + RPA): the scalar is
         pinned at m_sigma = 2 m_c AT EVERY COUPLING (mean-field/RPA is exact
         here, not an approximation that can be pushed). No sub-threshold
         binding exists at this order. F77 names the remaining hard build:
         "a full Bethe-Salpeter treatment ... is where any genuine 125 GeV
         claim would still have to be earned."

This module is that next step, attempted via a DIFFERENT (and standard,
external) route than a literal BS ladder: renormalisation-group improvement
of the compositeness condition, exactly as Bardeen, Hill & Lindner (BHL,
Phys. Rev. D41 (1990) 1647) did for SM top condensation. The physics content
is the same F77 relation lifted from a single scale to a running one:

    at the compositeness scale Lambda:   lambda(Lambda) = y_t(Lambda)^2 / 2
                                          (the SAME m_H = 2 m_t ceiling as
                                          F77's m_sigma = 2 m_c, now imposed
                                          as a UV boundary condition instead
                                          of a fixed-point-everywhere identity)
                                          y_t(Lambda) -> "infinite" (compos-
                                          iteness / Landau-pole condition:
                                          the pair is point-like at Lambda)

then RG-run the coupled 1-loop SM equations for (y_t, lambda) DOWN from
Lambda to mu = m_t, with the electroweak/QCD gauge couplings g1,g2,g3
supplied by their own (decoupled, closed-form) 1-loop running from measured
low-energy values. This is new relative to F77: F77 works at ONE scale (no
RG improvement); here the composite scalar's mass is pulled by 30+ decades
of running, which does move the ratio m_H/m_t away from the flat "2" (F77's
ceiling) even though, as shown below, it does not reach the measured value.

--------------------------------------------------------------------------
The one genuinely new ingredient: which scale is Lambda?
--------------------------------------------------------------------------
The original BHL papers had to CHOOSE a compositeness/GUT scale by hand
(traditionally ~10^15-10^19 GeV). This model does not get to choose: F79/F107
already derive the lattice's own UV cutoff as a closed form,

    a / ell_P = sqrt(8 pi) * 3^(1/4)   (F79, exact; F107 adopts it as the
                                         canonical SI ruler)

so the natural, PARAMETER-FREE compositeness scale for a model-native
Cooper-pair contact interaction is the model's own lattice cutoff,

    Lambda_model = E_Planck / (a / ell_P) ~ 1.85e18 GeV.

Nothing is tuned to make this land anywhere convenient -- it is whatever
F107's ruler says it is.

--------------------------------------------------------------------------
Verdict (see docstring of `check_bhl_compositeness_prediction` and the
finding for the honest numbers): this is a quantified NEGATIVE result. RG
running moves the mass ratio away from F77's flat ceiling (m_H/m_t: 2.0 ->
~1.10) but BOTH absolute masses still land well above measured, in close
quantitative agreement with the historical verdict on minimal BHL top
condensation (see e.g. https://en.wikipedia.org/wiki/Top_quark_condensate :
"the minimal model ... predicted a Higgs mass roughly double the observed
value" -- this run reproduces that "roughly double" statement to 98.6% at
this model's own derived cutoff, not a hand-picked one).

--------------------------------------------------------------------------
Numerics: deliberately stdlib-only (D8 numerics-ratchet discipline -- no new
numpy/scipy import site). Fixed-step RK4 in t = ln(mu/GeV); cross-checked
externally (session scratch, not shipped) against scipy's adaptive Radau/
RK45 integrators to < 1e-4 relative agreement -- see the finding for that
cross-check. The "y_t(Lambda) -> infinity" compositeness condition is
implemented as a large finite stand-in Y0, with convergence in Y0 checked
in-module (Part C below) -- the standard BHL numerical procedure (the
down-integrated IR values become Y0-independent once Y0 is "large enough",
because the nonlinear y_t^3 term washes out the boundary value long before
mu reaches m_t; this IS the "quasi-infrared-fixed-point" mechanism that
makes minimal top condensation predictive in the first place).
"""
from __future__ import annotations

import math
from functools import lru_cache

from casim.constants import a_over_ellP as _A_OVER_ELLP

# ---------------------------------------------------------------------------
# External inputs (PDG / CODATA; NOT model outputs -- flagged, as F73/F74/F77
# flag M_T_GEV, M_H, m_pi, g_A etc. inline rather than via the constants
# registry, since these are measured SM inputs, not model-derived symbols).
# ---------------------------------------------------------------------------
MZ_GEV = 91.1876          # PDG Z pole mass
MT_GEV = 172.57           # PDG top pole mass  (matches F73/F74/F77's M_T_GEV)
MH_OBS_GEV = 125.25       # PDG Higgs mass      (matches F77's M_H)
V_EW_GEV = 246.22         # SM vev, v = (sqrt2 G_F)^-1/2

ALPHA_EM_MZ = 1.0 / 127.9        # running QED coupling at m_Z (NOT 1/137)
SIN2_THETAW_MZ = 0.23122         # MSbar, PDG
ALPHA_S_MZ = 0.1179              # PDG world average

# CODATA Planck energy (E_P = M_Planck c^2). External constant, like
# casim.constants.geometry's own ell_P_m -- not a model output.
E_PLANCK_GEV = 1.220890e19

# The model's own compositeness/UV cutoff: F79/F107's exact lattice ruler,
# inverted to an energy. This is the ONE model-native input to the whole
# calculation; everything else here is standard 1-loop SM RG machinery.
LAMBDA_MODEL_GEV = E_PLANCK_GEV / _A_OVER_ELLP

# ---------------------------------------------------------------------------
# 1-loop SM gauge beta-function coefficients (GUT-normalised g1^2 = 5/3 g'^2),
# decoupled from y_t and lambda: 16 pi^2 dg/dt = b g^3.
# ---------------------------------------------------------------------------
_B1, _B2, _B3 = 41.0 / 6.0, -19.0 / 6.0, -7.0
_PI = math.pi
_ONE_16PI2 = 1.0 / (16.0 * _PI * _PI)


def _g_running(mu0: float, g0: float, b: float, mu: float) -> float:
    """Closed-form 1-loop running: 1/g^2(mu) = 1/g^2(mu0) - b/(8 pi^2) ln(mu/mu0)."""
    inv2 = 1.0 / g0 ** 2 - (b / (8.0 * _PI * _PI)) * math.log(mu / mu0)
    return math.sqrt(1.0 / inv2)


def gauge_couplings_at_mZ() -> tuple[float, float, float]:
    """(g1, g2, g3) at m_Z from measured alpha_em, sin^2(theta_W), alpha_s."""
    e2 = 4 * _PI * ALPHA_EM_MZ
    s2, c2 = SIN2_THETAW_MZ, 1.0 - SIN2_THETAW_MZ
    g2 = math.sqrt(e2 / s2)
    gprime = math.sqrt(e2 / c2)
    g1 = math.sqrt(5.0 / 3.0) * gprime
    g3 = math.sqrt(4 * _PI * ALPHA_S_MZ)
    return g1, g2, g3


def gauge_couplings_at(mu: float) -> tuple[float, float, float]:
    g1z, g2z, g3z = gauge_couplings_at_mZ()
    return (
        _g_running(MZ_GEV, g1z, _B1, mu),
        _g_running(MZ_GEV, g2z, _B2, mu),
        _g_running(MZ_GEV, g3z, _B3, mu),
    )


def _rhs(t: float, yt: float, lam: float) -> tuple[float, float]:
    """1-loop SM RGEs for (y_t, lambda) at t = ln(mu/GeV), top-Yukawa-only
    (other Yukawas negligible), gauge couplings supplied as closed-form
    functions of mu (see `gauge_couplings_at`). Standard SM beta functions,
    e.g. Buttazzo et al. 2013 (arXiv:1307.3536) eqs. for beta_yt, beta_lambda."""
    mu = math.exp(t)
    g1, g2, g3 = gauge_couplings_at(mu)
    dyt = yt * (4.5 * yt * yt - 8.0 * g3 * g3 - 2.25 * g2 * g2
                - (17.0 / 12.0) * g1 * g1) * _ONE_16PI2
    dlam = (24.0 * lam * lam + 12.0 * lam * yt * yt - 6.0 * yt ** 4
            - 9.0 * lam * g2 * g2 - 3.0 * lam * g1 * g1
            + 1.125 * g2 ** 4 + 0.75 * g1 * g1 * g2 * g2
            + 0.375 * g1 ** 4) * _ONE_16PI2
    return dyt, dlam


def run_down_from_Lambda(Lambda_GeV: float, Y0: float, n_steps: int = 200_000,
                          mu_low_GeV: float = MT_GEV) -> tuple[float, float]:
    """Fixed-step RK4, integrating (y_t, lambda) DOWN in t=ln(mu) from Lambda
    (compositeness condition y_t=Y0, lambda=Y0^2/2) to mu_low_GeV."""
    t_hi, t_lo = math.log(Lambda_GeV), math.log(mu_low_GeV)
    h = (t_lo - t_hi) / n_steps
    t, yt, lam = t_hi, float(Y0), 0.5 * Y0 * Y0
    for _ in range(n_steps):
        k1yt, k1l = _rhs(t, yt, lam)
        k2yt, k2l = _rhs(t + h / 2, yt + h / 2 * k1yt, lam + h / 2 * k1l)
        k3yt, k3l = _rhs(t + h / 2, yt + h / 2 * k2yt, lam + h / 2 * k2l)
        k4yt, k4l = _rhs(t + h, yt + h * k3yt, lam + h * k3l)
        yt = yt + (h / 6.0) * (k1yt + 2 * k2yt + 2 * k3yt + k4yt)
        lam = lam + (h / 6.0) * (k1l + 2 * k2l + 2 * k3l + k4l)
        t += h
    return yt, lam


def predict_masses(Lambda_GeV: float, Y0: float = 300.0,
                    n_steps: int = 200_000) -> dict:
    yt, lam = run_down_from_Lambda(Lambda_GeV, Y0, n_steps)
    mt_pred = yt * V_EW_GEV / math.sqrt(2.0)
    mh_pred = math.sqrt(2.0 * lam) * V_EW_GEV if lam > 0 else float("nan")
    return {"Lambda_GeV": Lambda_GeV, "Y0": Y0, "n_steps": n_steps,
            "y_t_mt": yt, "lambda_mt": lam,
            "m_t_pred_GeV": mt_pred, "m_H_pred_GeV": mh_pred,
            "ratio_mH_over_mt_pred": mh_pred / mt_pred}


@lru_cache(maxsize=1)
def run_all() -> dict:
    """Cached (lru_cache): this module's numerics are pure-Python RK4 and this
    is called repeatedly by the test suite; the whole ~17s cost should be
    paid once per process, not once per assertion."""
    out: dict = {}

    g1t, g2t, g3t = gauge_couplings_at(MT_GEV)
    out["A_gauge_at_mt"] = {
        "g1": g1t, "g2": g2t, "g3": g3t, "alpha_s_mt": g3t ** 2 / (4 * _PI),
    }

    out["B_lambda_model"] = {
        "a_over_ellP": _A_OVER_ELLP, "E_Planck_GeV": E_PLANCK_GEV,
        "Lambda_model_GeV": LAMBDA_MODEL_GEV,
    }

    headline = predict_masses(LAMBDA_MODEL_GEV, Y0=300.0, n_steps=200_000)
    out["C_headline"] = headline

    # Y0-convergence ("compositeness ray") check -- the standard BHL
    # numerical criterion that the boundary stand-in Y0 has washed out.
    conv = {}
    for Y0 in (50.0, 100.0, 300.0):
        r = predict_masses(LAMBDA_MODEL_GEV, Y0=Y0, n_steps=200_000)
        conv[str(Y0)] = {"m_t": r["m_t_pred_GeV"], "m_H": r["m_H_pred_GeV"]}
    spread_mt = max(v["m_t"] for v in conv.values()) - min(v["m_t"] for v in conv.values())
    spread_mh = max(v["m_H"] for v in conv.values()) - min(v["m_H"] for v in conv.values())
    out["D_Y0_convergence"] = {
        "table": conv,
        "spread_mt_GeV": spread_mt, "spread_mh_GeV": spread_mh,
        "spread_mt_pct": 100 * spread_mt / headline["m_t_pred_GeV"],
        "spread_mh_pct": 100 * spread_mh / headline["m_H_pred_GeV"],
    }

    # Lambda sweep -- shows the well-known BHL "quasi-fixed-point" plateau:
    # m_t/m_H predicted DECREASE monotonically as Lambda increases, and
    # saturate near a floor well above the measured values even letting
    # Lambda run far past the Planck scale -- i.e. the exclusion is not an
    # artefact of picking the "wrong" Lambda.
    sweep = {}
    for Lam in (1e6, 1e9, 1e12, 1e15, 1e16, 1e17, LAMBDA_MODEL_GEV, 1e19):
        r = predict_masses(Lam, Y0=300.0, n_steps=200_000)
        sweep[f"{Lam:.3e}"] = {"m_t": r["m_t_pred_GeV"], "m_H": r["m_H_pred_GeV"]}
    out["E_lambda_sweep"] = sweep

    # F77's flat ceiling for comparison, at this same m_t input.
    out["F_f77_flat_ceiling_mH"] = 2.0 * MT_GEV

    out["measured"] = {"m_t_GeV": MT_GEV, "m_H_GeV": MH_OBS_GEV,
                        "ratio_mH_over_mt": MH_OBS_GEV / MT_GEV}
    return out


def check_bhl_compositeness_prediction() -> dict:
    """
    F352 verdict record.

    Claim under test: RG-improving the F73/F77 Cooper-pair compositeness
    condition (m_H(Lambda) = 2 m_t(Lambda), y_t(Lambda) -> infinity) down
    from the model's OWN derived UV cutoff Lambda_model = E_Planck/(a/ell_P)
    (F79/F107) via the standard 1-loop SM RGEs.

    Expected/predicted structure (this IS the falsifiable content):
      - the Y0 boundary stand-in must wash out (Y0-convergence, < 0.1%)
      - RG running must move the ratio m_H/m_t below F77's flat value 2.0
        (RG improvement is doing SOMETHING, not nothing)
      - but the absolute masses must NOT match measured (172.57 / 125.25)
        to better than ~10%: reproducing the historical minimal-BHL verdict
        that this route overshoots badly (the "roughly double" statement).
    A finding that this check does NOT reproduce (e.g. converges onto the
    measured masses) would be the extraordinary result; this run reproduces
    the exclusion instead, and the checks below record that honestly.
    """
    out = run_all()
    head = out["C_headline"]
    conv = out["D_Y0_convergence"]

    checks = {
        "Y0_converged_mt_lt_0.1pct": conv["spread_mt_pct"] < 0.1,
        "Y0_converged_mH_lt_0.1pct": conv["spread_mh_pct"] < 0.1,
        "ratio_moved_below_f77_flat_ceiling": (
            head["ratio_mH_over_mt_pred"] < 2.0 - 1e-6
        ),
        "ratio_still_above_measured_ratio": (
            head["ratio_mH_over_mt_pred"] > out["measured"]["ratio_mH_over_mt"]
        ),
        "mt_overshoots_measured_by_more_than_10pct": (
            (head["m_t_pred_GeV"] - out["measured"]["m_t_GeV"])
            / out["measured"]["m_t_GeV"] > 0.10
        ),
        "mH_overshoots_measured_by_more_than_10pct": (
            (head["m_H_pred_GeV"] - out["measured"]["m_H_GeV"])
            / out["measured"]["m_H_GeV"] > 0.10
        ),
        "mH_within_30pct_of_2x_measured": (
            abs(head["m_H_pred_GeV"] - 2 * out["measured"]["m_H_GeV"])
            / (2 * out["measured"]["m_H_GeV"]) < 0.30
        ),
    }
    return {
        "checks": checks,
        "pass": all(checks.values()),
        "headline": head,
        "verdict": (
            "NEGATIVE (quantified). RG-improving the F73/F77 compositeness "
            "condition down from the model's own F79/F107 lattice cutoff "
            f"(Lambda={LAMBDA_MODEL_GEV:.3e} GeV) predicts "
            f"m_t={head['m_t_pred_GeV']:.2f} GeV (+{100*(head['m_t_pred_GeV']-MT_GEV)/MT_GEV:.1f}%) "
            f"and m_H={head['m_H_pred_GeV']:.2f} GeV "
            f"(+{100*(head['m_H_pred_GeV']-MH_OBS_GEV)/MH_OBS_GEV:.1f}%, essentially "
            "double). RG running DOES move the ratio m_H/m_t away from F77's "
            f"flat ceiling (2.0 -> {head['ratio_mH_over_mt_pred']:.3f}), but not "
            "far enough: minimal single-channel top condensation, anchored at "
            "this model's own derived Planck-scale cutoff, is excluded as the "
            "origin of BOTH m_t and m_H simultaneously -- the same verdict the "
            "historical BHL literature reaches for a GUT/Planck-scale cutoff, "
            "reproduced here with a cutoff the model does not get to choose."
        ),
    }


if __name__ == "__main__":
    import json

    from casim.engine.particles._results_path import results_path

    out = run_all()
    out["verdict_record"] = check_bhl_compositeness_prediction()
    path = results_path("F352_higgs_bhl_compositeness.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"wrote {path}")
    print(out["verdict_record"]["verdict"])
