"""
cosmology_holographic.py — the literature's home for F295's structure  (F296)
=============================================================================

Created: 2026-08-02 - 20:40

**Question** (Ben, 2026-08-02): *research the problem online and attempt to
determine its source.*

F295 derived, from the model's own structure, that the primordial tilt is an
**anomalous dimension** requiring no second scale, and left one open question:
*which operator carries it?*  That structure is not idiosyncratic — it is the
defining feature of **holographic cosmology** (McFadden & Skenderis 2009;
Afshordi, Coriano, Delle Rose, Gould & Skenderis, PRL 118 041301 (2017)), where
the primordial spectrum is computed from a **3-dimensional QFT with no inflaton
and no bulk geometry**.  Four results follow.

--------------------------------------------------------------------------
L1 — the framework exists, and it has been fitted to Planck
--------------------------------------------------------------------------

Holographic cosmology (HC) predicts

    Delta^2_R(q) = Delta^2_0 / [1 + (g q*/q) ln|q/(beta g q*)| + O((g q*/q)^2)]

from the 2-point function of the **trace of the 3D stress tensor**,
``Delta^2_R(q) = -q^3/(4 pi^2) / Im <<T(q) T(-q)>>``.  Afshordi et al fit it to
Planck 2015 + BAO + BKP and find it *competitive* with LambdaCDM: disfavoured
2.2 sigma globally, but within 1 sigma once ``l < 30`` is dropped (where the
dual QFT goes non-perturbative).

--------------------------------------------------------------------------
L2 — F286 T1 RETRODICTS HC's known problem  (the load-bearing result)
--------------------------------------------------------------------------

HC's dual is a **super-renormalizable** 3D theory, so its 't Hooft coupling
``g_eff^2 = g_YM^2 N / q`` is **dimensionful** and runs as ``1/q`` — a power,
``p = -1``.  F286 T1 bounds the tilt's log-derivative at ``0.32``.  Evaluating
T1's diagnostic on HC's *own fitted spectrum* gives **0.675 — over the bound by
2.1x** — and the implied running ``dn_s/dlnk = +0.015`` sits **2.9 sigma** from
Planck.

That is the published tension, recovered from a bound built with no knowledge of
HC.  **T1 is validated on an independent case it was not constructed from**,
which is worth more than the retrodiction itself: it means T1 is a usable
instrument, not a private construction.

--------------------------------------------------------------------------
L3 — the model sits in the branch the literature explicitly does NOT analyse
--------------------------------------------------------------------------

A constant ``gamma`` (F295) needs ``p = 0``, i.e. a **dimensionless** coupling —
a **conformal** dual, not a super-renormalizable one.  In HC's notation that is
``f1 = 0``, and the PRL's own footnote 2 reads: *"This assumes f1 != 0. A
separate analysis is required, where f1 = 0."*

So the model's structure corresponds to a **CFT dual**, and that case is an
**acknowledged gap in the published literature** rather than a re-tread.

--------------------------------------------------------------------------
L4 — the operator is named
--------------------------------------------------------------------------

F295 asked *which operator carries gamma*.  HC answers it: the **trace of the
3-dimensional stress tensor** ``T^i_i``, whose 2-point function *is* the
primordial spectrum.  ``gamma`` is its anomalous dimension.

--------------------------------------------------------------------------
L5 — but the model's own field content, read as the dual, is EXCLUDED by r
--------------------------------------------------------------------------

HC gives the tensor-to-scalar ratio in closed form from the dual's field content:

    r = 32 (1 + sum_M (1 - 8 xi_M)^2) / (1 + 2 N_psi + N_Phi).

Feed in the model's own content — 48 Weyl fermions (3 generations x 16 including
nu_R, F47) and the 2 real scalars of the E_g doublet (the model is Higgs-free,
F27) — and ``r`` comes out **0.32** (conformal scalars) to **0.97** (minimal),
against BICEP/Keck BK18 ``r < 0.036``.  **Over by 9x to 27x.**  Reaching the
bound would need ``N_Phi > 792`` scalars; the model has 2.

This is the same failure mode the PRL reports — *"the data rules out the dual
theory being Yang-Mills theory coupled to fermions only"* — and the model is
fermion-dominated.  **The naive holographic reading of this model is excluded.**

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import json
import math

__all__ = [
    "hc_spectrum_tilt",
    "t1_retrodiction",
    "branch_identification",
    "named_operator",
    "tensor_ratio_from_model_content",
    "run",
]

# Planck 2018 X.
NS_OBS, NS_SIGMA = 0.9649, 0.0042
RUN_OBS, RUN_SIGMA = -0.0045, 0.0067
# BICEP/Keck BK18, 95% CL.
R_BOUND_BK18 = 0.036

# Afshordi, Coriano, Delle Rose, Gould, Skenderis, PRL 118 041301 (2017),
# Table I, all-multipole fit.
HC_G_FIT = -0.00703
HC_LNBETA_FIT = 0.877
HC_DISFAVOURED_SIGMA = 2.2                 # their reported global chi^2 penalty

# F286 T1's Planck-derived bound on the tilt's log-derivative.
T1_BOUND = 0.32

# The model's own field content, read as a candidate 3D dual.
N_WEYL_FERMIONS = 48                       # 3 generations x 16 (incl. nu_R, F47)
N_REAL_SCALARS = 2                         # the E_g doublet; Higgs-free (F27)


def hc_spectrum_tilt(g: float = HC_G_FIT, lnbeta: float = HC_LNBETA_FIT) -> dict:
    r"""Tilt and running of HC's spectrum at its own fitted point.

    With ``u = g q*/q`` and ``D = 1 - u ln|beta u|``,
    ``n_s - 1 = -u (ln|beta u| + 1)/D`` and
    ``dln|n_s-1|/dlnq = -(L+2)/(L+1)``, ``L = ln|beta u|``.
    """
    beta = math.exp(lnbeta)
    u = g                                   # evaluated at q = q*
    L = math.log(abs(beta * u))
    D = 1.0 - u * L
    tilt = -u * (L + 1.0) / D
    dlnF = -(L + 2.0) / (L + 1.0)
    return {
        "g": g, "beta": beta, "ln_abs_beta_u": L, "D": D,
        "n_s_minus_1": tilt,
        "n_s": 1.0 + tilt,
        "log_derivative_of_tilt": dlnF,
        "implied_dns_dlnk": tilt * dlnF,
    }


def t1_retrodiction() -> dict:
    r"""F286 T1, applied to HC's fitted spectrum, recovers its published tension."""
    s = hc_spectrum_tilt()
    p = abs(s["log_derivative_of_tilt"])
    alpha = s["implied_dns_dlnk"]
    return {
        "hc_coupling_is_dimensionful": True,
        "hc_power_p_nominal": -1,
        "t1_bound": T1_BOUND,
        "hc_log_derivative": p,
        "over_bound_factor": p / T1_BOUND,
        "t1_flags_hc": p > T1_BOUND,
        "hc_implied_dns_dlnk": alpha,
        "planck_dns_dlnk": RUN_OBS,
        "planck_sigma": RUN_SIGMA,
        "tension_sigma": (alpha - RUN_OBS) / RUN_SIGMA,
        "published_global_disfavour_sigma": HC_DISFAVOURED_SIGMA,
        "retrodiction_agrees": True,
        "why_it_matters": ("T1 was built from Planck's running alone, with no "
                           "knowledge of holographic cosmology. Recovering HC's "
                           "published tension makes T1 a usable instrument "
                           "rather than a private construction."),
    }


def branch_identification() -> dict:
    r"""Constant gamma needs a dimensionless coupling — a CFT dual, HC's f1 = 0."""
    return {
        "hc_branch": "super-renormalizable 3D QFT, dimensionful g_YM^2, f1 != 0",
        "hc_tilt_shape_p": -1,
        "model_branch": "dimensionless coupling => conformal dual, f1 = 0",
        "model_tilt_shape_p": 0,
        "literature_analyses_model_branch": False,
        "prl_footnote": ("PRL 118 041301 footnote 2: 'This assumes f1 != 0. A "
                         "separate analysis is required, where f1 = 0.'"),
        "status": "acknowledged gap in the published literature, not a re-tread",
    }


def named_operator() -> dict:
    r"""HC identifies the operator F295 could not: the 3D stress-tensor trace."""
    return {
        "operator": "T^i_i — the trace of the 3-dimensional stress tensor",
        "holographic_formula": ("Delta^2_R(q) = -q^3/(4 pi^2) / "
                                "Im <<T(q) T(-q)>>"),
        "gamma_is": "the anomalous dimension of that operator",
        "gamma_required": 0.5 * (1.0 - NS_OBS),
        "answers_F295_open_question": True,
        "caveat": ("this NAMES a candidate operator from an external framework; "
                   "it does not establish that the model has such a dual — "
                   "see L5, where the naive reading is excluded"),
    }


def tensor_ratio_from_model_content(n_psi: int = N_WEYL_FERMIONS,
                                    n_phi: int = N_REAL_SCALARS) -> dict:
    r"""``r = 32(1 + sum(1-8 xi)^2)/(1 + 2 N_psi + N_Phi)`` on the model's content."""
    out = {}
    for name, xi in (("minimal", 0.0), ("conformal", 0.125)):
        S = n_phi * (1.0 - 8.0 * xi) ** 2
        r = 32.0 * (1.0 + S) / (1.0 + 2.0 * n_psi + n_phi)
        out[name] = {"xi": xi, "r": r, "over_BK18_factor": r / R_BOUND_BK18,
                     "excluded": r > R_BOUND_BK18}
    needed = 32.0 / R_BOUND_BK18 - 1.0 - 2.0 * n_psi
    return {
        "n_weyl_fermions": n_psi,
        "n_real_scalars": n_phi,
        "r_BK18_bound": R_BOUND_BK18,
        "cases": out,
        "n_phi_needed_for_bound": needed,
        "model_has": n_phi,
        "shortfall_factor": needed / max(n_phi, 1),
        "matches_published_exclusion": ("the PRL rules out 'Yang-Mills coupled "
                                        "to fermions only'; this model is "
                                        "fermion-dominated"),
        "naive_holographic_reading_excluded": True,
    }


# ---------------------------------------------------------------------------
def run() -> dict:
    return {
        "finding": "F296",
        "question": "where does F295's structure live in the literature?",
        "L1_framework": {
            "name": "holographic cosmology (McFadden-Skenderis; Afshordi et al 2017)",
            "no_inflaton": True,
            "spectrum_from": "2-point function of the 3D stress-tensor trace",
            "fitted_to_planck": True,
            "global_disfavour_sigma": HC_DISFAVOURED_SIGMA,
        },
        "L2_t1_retrodiction": t1_retrodiction(),
        "L3_branch": branch_identification(),
        "L4_operator": named_operator(),
        "L5_tensor_ratio": tensor_ratio_from_model_content(),
        "verdict": (
            "F295's structure has an established home; F286 T1 is VALIDATED by "
            "retrodicting holographic cosmology's published tension (0.675 vs "
            "0.32, and 2.9 sigma running); the model sits in the f1 = 0 CFT "
            "branch the literature explicitly leaves unanalysed; the operator "
            "is NAMED as the 3D stress-tensor trace; but the model's own field "
            "content read as that dual is EXCLUDED by r at 9-27x"
        ),
    }


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    res = run()
    path = results_path("F296_holographic.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(res, indent=2, sort_keys=True, default=str))
    print("\nwrote", path)
