"""
cosmology_anomalous_dimension.py — the tilt needs a gamma, not a scale  (F295)
==============================================================================

Created: 2026-08-02 - 19:20

**Question** (Ben, 2026-08-02): *if alpha and G are allowed to differ from their
adopted values, does that narrow the loop, and can model geometry get closer to
a predictive mechanism?*

Answering it exposed that **F286 mis-read its own theorem**, and the correction
is worth more than the answer.

--------------------------------------------------------------------------
A1 — the correction: p = 0 is not trivial, it is the mechanism class
--------------------------------------------------------------------------

F286 T1 proved that if ``n_s - 1 = F(k xi)`` then Planck's running bounds
``|dlnF/dlnx| < 0.32``, so a power ``F = C x^p`` needs ``|p| < 0.32``.  F286 read
that as "only a log survives" and dismissed ``p = 0`` as the trivial case.

``p = 0`` is **not** trivial.  A constant ``F`` is a **scale-free anomalous
dimension** ``gamma``:

    n_s - 1 = -2 gamma  (constant)   =>   Delta^2 ~ k^(n_s - 1),  a pure power law
                                     =>   dn_s/dlnk = 0  EXACTLY

It needs **no second scale at all**, it is *more* consistent with Planck's null
running than the log class, and it sits exactly on F285 D3's proven line of
fixed points — D3 showed every power law is a fixed point and the exponent is a
free marginal label.  ``gamma`` **is** that label.

So the whole "second scale" framing was too narrow.  The question is not *where
is the second scale* but **what operator carries the anomalous dimension**.

This also repairs F285's row: "scale-free in the metric gives n_s = 1, excluded
at 8.4 sigma" is the ``gamma = 0`` case, so that exclusion is the *positive*
statement ``gamma != 0``, not a dead end.

--------------------------------------------------------------------------
A2 — two sub-classes, and a discriminator
--------------------------------------------------------------------------

    constant-gamma  (this finding):  dn_s/dlnk = 0          exactly
    log-type        (F286 T2):       dn_s/dlnk = -2.62e-4

Both sit inside Planck's ``-0.0045 +/- 0.0067``.  They separate at
``sigma ~ 1e-4`` — beyond CMB-S4, but it is a real discriminator between two
otherwise-identical pictures, and it belongs on the register now.

--------------------------------------------------------------------------
A3 — the inverse problem: does freeing alpha or G help?  No.
--------------------------------------------------------------------------

At one loop ``1 - n_s = g_eff/(2 pi)``, so the data demands

    g_eff = 2 pi (1 - n_s) = 0.2205 +/- 0.0264.

  * **alpha.**  Reaching ``alpha = 0.2205`` by one-loop QED running from ``m_e``
    needs ``ln(mu/m_e) = 208``, i.e. ``mu ~ 1e87 GeV`` — **68 decades above the
    model's own lattice cutoff**.  There is no such scale in the model.
    Excluded, and excluded *by the model's own cutoff* rather than by a fit.
  * **G.**  Gravity's dimensionless coupling is ``g_grav(k) = (k/M_Pl)^2``.  That
    is a **power (p = 2)**, which F286 T1 already excludes on *shape* — before
    magnitude is considered at all.  And the magnitude is ``1.7e-116``.
    **Doubly excluded.**

So freeing the two adopted constants does not narrow the loop.  What it does is
show the loop cannot be a *running gauge coupling* in the first place — which
is the useful half of the answer.

--------------------------------------------------------------------------
A4 — what geometry offers, stated at its real strength
--------------------------------------------------------------------------

A constant ``gamma`` needs a coupling that is **scale-independent**, and the
model owns exactly that kind of object: exact representation weights.  The
required ``g_eff = 0.2205 +/- 0.0264`` sits **0.064 sigma** from ``2/9``, which
this model carries as **three independent registered constants** (``delta*``,
``sin2_thetaW_onshell``, ``c_fierz_colour``) — CLAUDE.md insists they stay
separate precisely because they are unrelated quantities that share a value.

This is a **shape-justified target**, which is more than F286's bare numerical
coincidence was — a scale-free rep weight is the right kind of object for a
constant ``gamma``.  It is still **not a derivation**: F286 T5's look-elsewhere
count applies unchanged to the *value*, and no operator has been identified.
The gap is now sharp: *which operator sets the initial amplitude, and what is
its anomalous dimension?*

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import json
import math

import sympy as sp

from casim.constants import c_lat, delta_star_f, sin2_thetaW_onshell

__all__ = [
    "anomalous_dimension_branch",
    "subclass_discriminator",
    "alpha_inverse_problem",
    "gravity_inverse_problem",
    "representation_weight_target",
    "run",
]

NS_OBS, NS_SIGMA = 0.9649, 0.0042
RUN_OBS, RUN_SIGMA = -0.0045, 0.0067
DECADES_PIVOT_TO_BZ = 58.25962028864585        # F285/F286

ALPHA_EM = 1.0 / 137.035999
M_E_GEV = 0.511e-3
N_CHARGED_LEPTONS = 3.0
M_PL_GEV = 1.22e19                              # non-reduced, for the cutoff line
# k_pivot and M_Pl as energies, for the gravitational coupling.
K_PIVOT_EV = 1.62e-24 * 1.97e-7
M_PL_RED_EV = 2.435e27


def _tilt() -> float:
    return 1.0 - NS_OBS


# ---------------------------------------------------------------------------
# A1 — p = 0 is a scale-free anomalous dimension
# ---------------------------------------------------------------------------
def anomalous_dimension_branch() -> dict:
    r"""A constant ``F`` gives a pure power law and ``dn_s/dlnk = 0`` exactly."""
    k, gamma, A = sp.symbols("k gamma A", positive=True)
    ns_minus_1 = -2 * gamma
    Delta2 = A * k ** ns_minus_1
    log_slope = sp.simplify(k * sp.diff(sp.log(Delta2), k))
    running = sp.simplify(k * sp.diff(log_slope, k))
    return {
        "F286_T1_allowed_p": "|p| < 0.32",
        "p_zero_is_trivial": False,
        "log_slope": str(log_slope),                 # -2*gamma
        "running_exact": str(running),               # 0
        "dns_dlnk_exact_zero": running == 0,
        "gamma_required_nonzero": True,
        "gamma_from_data": _tilt() / 2.0,
        "needs_a_second_scale": False,
        "sits_on_F285_D3_fixed_line": True,
        "repairs_F285_row": ("'scale-free in the metric gives n_s = 1, excluded "
                             "at 8.4 sigma' is the gamma = 0 case, so that "
                             "exclusion is the POSITIVE statement gamma != 0"),
    }


def subclass_discriminator() -> dict:
    r"""constant-gamma predicts 0; the F286 log class predicts -2.62e-4."""
    L = DECADES_PIVOT_TO_BZ * math.log(10.0)
    log_pred = -_tilt() / L
    sep = abs(log_pred - 0.0)
    return {
        "constant_gamma_dns_dlnk": 0.0,
        "log_class_dns_dlnk": log_pred,
        "separation": sep,
        "planck_sigma": RUN_SIGMA,
        "sigma_needed_to_separate": sep,
        "both_consistent_today": (abs(log_pred - RUN_OBS) < RUN_SIGMA
                                  and abs(0.0 - RUN_OBS) < RUN_SIGMA),
        "separable_at_sigma": sep,
        "beyond_CMB_S4": sep < 1.0e-3,
    }


# ---------------------------------------------------------------------------
# A3 — the inverse problem Ben asked for
# ---------------------------------------------------------------------------
def _g_eff() -> tuple[float, float]:
    return 2 * math.pi * _tilt(), 2 * math.pi * NS_SIGMA


def alpha_inverse_problem() -> dict:
    r"""What scale would one-loop QED need to reach ``alpha = g_eff``?"""
    g, dg = _g_eff()
    d_inv = 1.0 / ALPHA_EM - 1.0 / g
    ln_mu_over_me = d_inv / ((2.0 / (3.0 * math.pi)) * N_CHARGED_LEPTONS)
    log10_mu = math.log10(M_E_GEV) + ln_mu_over_me / math.log(10.0)
    log10_cutoff = math.log10(M_PL_GEV * 3.0 ** -0.25)
    return {
        "g_eff": g, "g_eff_sigma": dg,
        "alpha_adopted": ALPHA_EM,
        "factor_required": g / ALPHA_EM,
        "ln_mu_over_me": ln_mu_over_me,
        "log10_mu_GeV": log10_mu,
        "log10_lattice_cutoff_GeV": log10_cutoff,
        "decades_above_cutoff": log10_mu - log10_cutoff,
        "excluded": log10_mu > log10_cutoff,
        "verdict": ("alpha would have to be evaluated ~68 decades ABOVE the "
                    "model's own lattice cutoff — excluded by the model's own "
                    "structure, not by a fit"),
    }


def gravity_inverse_problem() -> dict:
    r"""Gravity's dimensionless coupling is a POWER, so T1 kills it on shape."""
    g_grav = (K_PIVOT_EV / M_PL_RED_EV) ** 2
    g, _ = _g_eff()
    return {
        "g_grav_at_pivot": g_grav,
        "power_p": 2,
        "T1_bound_on_p": 0.32,
        "excluded_on_shape": 2 > 0.32,
        "shortfall_decades": math.log10(g / g_grav),
        "excluded_on_magnitude": True,
        "verdict": ("doubly excluded: F286 T1 rules out p = 2 on SHAPE before "
                    "magnitude is considered, and the magnitude is 1.7e-116"),
    }


# ---------------------------------------------------------------------------
# A4 — the representation-weight target
# ---------------------------------------------------------------------------
def representation_weight_target() -> dict:
    r"""A constant gamma wants a scale-free coupling; the model owns rep weights."""
    g, dg = _g_eff()
    two_ninths = 2.0 / 9.0
    return {
        "g_eff": g, "g_eff_sigma": dg,
        "two_ninths": two_ninths,
        "deviation_sigma": (two_ninths - g) / dg,
        "registered_constants_equal_to_2_9": [
            "delta_star (E_g representation weight, F175)",
            "sin2_thetaW_onshell (electroweak endpoint, F138)",
            "c_fierz_colour (colour Fierz coefficient, F145)",
        ],
        "delta_star_matches": abs(delta_star_f - two_ninths) < 1e-12,
        "sin2_thetaW_matches": abs(sin2_thetaW_onshell - two_ninths) < 1e-12,
        "why_a_rep_weight_fits": ("a constant gamma needs a SCALE-INDEPENDENT "
                                  "coupling, and an exact representation weight "
                                  "is precisely that — unlike alpha or alpha_s, "
                                  "it can be evaluated at CMB momenta trivially"),
        "still_not_a_derivation": True,
        "look_elsewhere_still_applies": ("F286 T5's count applies unchanged to "
                                         "the VALUE; what improved is the SHAPE "
                                         "justification, not the statistics"),
        "open": "which operator sets the initial amplitude, and what is its gamma",
    }


# ---------------------------------------------------------------------------
def run() -> dict:
    return {
        "finding": "F295",
        "question": "does freeing alpha and G narrow the loop? can geometry help?",
        "A1_anomalous_dimension": anomalous_dimension_branch(),
        "A2_discriminator": subclass_discriminator(),
        "A3_alpha": alpha_inverse_problem(),
        "A3_gravity": gravity_inverse_problem(),
        "A4_representation_weight": representation_weight_target(),
        "answer_to_ben": (
            "No — freeing alpha needs it 68 decades above the lattice cutoff, "
            "and freeing G is excluded by SHAPE before magnitude. But asking "
            "the question exposed that F286 mis-read its own theorem: the tilt "
            "is an ANOMALOUS DIMENSION, needs no second scale at all, and "
            "predicts dn_s/dlnk = 0 exactly. Geometry then supplies the right "
            "KIND of object — a scale-free representation weight — with 2/9 "
            "at 0.064 sigma, though the value's look-elsewhere count stands."
        ),
    }


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    res = run()
    path = results_path("F295_anomalous_dimension.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(res, indent=2, sort_keys=True, default=str))
    print("\nwrote", path)
