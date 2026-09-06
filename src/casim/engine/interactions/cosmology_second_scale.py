"""
cosmology_second_scale.py — What could supply the 3.5% tilt?  (F286)
====================================================================

Created: 2026-08-02 - 18:00

**Question.**  F285 reduced the whole primordial residual to one number: the
initial state must be *tilted* by ``1 - n_s = 0.0351``, exact scale invariance
is excluded at 8.4 sigma, and a tilt is a departure from scale invariance and so
needs a **second scale**.  F285 named two candidate shapes and neither was on
the map.  This module asks what a second scale must *look like*, inventories
what the model owns, and tests the tempting numerical coincidence.

--------------------------------------------------------------------------
T1 — the classification theorem: a tilt needs a LOG, not a LENGTH
--------------------------------------------------------------------------

Suppose the tilt depends on a second scale through the dimensionless
``x = k xi``.  Then ``n_s - 1 = F(x)`` and ``dn_s/dlnk = x F'(x)``.  Planck
measures both, and their ratio bounds the log-derivative:

    |d ln F / d ln x|  =  |dn_s/dlnk| / |n_s - 1|  <  0.32   (1 sigma)

  * **Feature-type (a length).**  ``F = C x^p`` gives ``|dlnF/dlnx| = p``, so
    only ``|p| < 0.32`` survives — and a length scale enters at integer power
    (``p = 2`` for the leading lattice correction).  **Every length scale is
    excluded**, not by being far away but by the *shape* of its k-dependence.
    This closes F285 falsifier 1's "condensate correlation length" route
    structurally rather than by distance.

  * **Log-type (a running coupling).**  ``F = C / L`` with ``L = ln(k_UV/k)``
    gives ``|dlnF/dlnL| = 1/L = 1/134 = 0.0075``.  Comfortably inside.

**Only an RG-type logarithm can supply a constant tilt.**  That is a real
restriction, and it is what makes the rest of the module computable.

--------------------------------------------------------------------------
T2 — the whole class makes ONE parameter-free prediction
--------------------------------------------------------------------------

If the tilt is ``1 - n_s = C / L`` with ``L = ln(k_BZ/k)`` anchored at the
lattice, then differentiating costs nothing:

    dn_s/dlnk  =  -(1 - n_s) / L  =  -2.62e-4        (no free parameter)

using F285's own ``L = 58.26 ln 10 = 134.15``.  It sits **25.6x below** Planck's
current 1-sigma error, so it is a target rather than a test today.

--------------------------------------------------------------------------
T3 — the magnitude is NOT the problem
--------------------------------------------------------------------------

The required coefficient is ``C = (1 - n_s) L = 4.709`` — a perfectly ordinary
O(1) number.  **So the tilt is not unnaturally small**: it is exactly what one
one-loop logarithm across the model's own 58 decades gives with an O(1)
coefficient.  What is missing is not a small number.  It is the loop.

--------------------------------------------------------------------------
T4 — inventory: the model owns no coupling that can do it
--------------------------------------------------------------------------

  * ``alpha_em`` — runs, but gives a tilt ~1e-3, ~30x too small, and barely
    runs at all at CMB momenta.
  * ``alpha_s`` — cannot be evaluated at CMB momenta: those are ~1e-30 eV,
    thirty orders below Lambda_QCD, deep in the confined regime.
  * ``G`` — **does not run at all.**  F79 makes it structural and F284 predicts
    ``Gdot/G = 0`` exactly.  This is the irony worth recording: the model's
    sharpest prediction removes its most natural candidate second scale.
  * block-spin — F285 D3 proved the spectral index is *exactly marginal* under
    it, so it cannot move the tilt by construction.

--------------------------------------------------------------------------
T5 — the coincidence, and why it is not evidence
--------------------------------------------------------------------------

``1 - n_s = delta*/(2 pi) = (2/9)/(2 pi) = 1/(9 pi) = 0.0353678`` sits
**0.064 sigma** from Planck, and its *shape* — a one-loop anomalous dimension
of the model's own exact ``delta* = 2/9`` (F175) — is the right kind of object.

It is still not evidence, and this module says so with a count rather than an
opinion.  Over a family defined *before* looking (a small rational or a
registered model constant, times an integer power of pi), **six** distinct
values land inside the 1-sigma window.  Being the closest of six is not a
result.  Under the F253/F256 standard this is recorded as a **coincidence**,
and it would only become evidence if a mechanism predicted the shape first.

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import json
import math
from fractions import Fraction

import sympy as sp

from casim.constants import (
    c_lat,
    cos3_delta_star,
    delta_star_f,
    e_saturation,
    lambda_6,
    sin2_thetaW_onshell,
)

__all__ = [
    "classification_theorem",
    "running_prediction",
    "required_coefficient",
    "coupling_inventory",
    "coincidence_look_elsewhere",
    "run",
]

# Planck 2018 TT,TE,EE+lowE+lensing.
NS_OBS, NS_SIGMA = 0.9649, 0.0042
RUN_OBS, RUN_SIGMA = -0.0045, 0.0067          # dn_s/dlnk
# F285's measured separation between the CMB pivot and the Brillouin-zone edge.
DECADES_PIVOT_TO_BZ = 58.25962028864585

# External couplings, as measured — not model outputs.
ALPHA_EM = 1.0 / 137.035999
ALPHA_S_MZ = 0.11955                          # the model's own value (F144/F239)
LAMBDA_QCD_EV = 2.0e8                         # ~200 MeV
K_PIVOT_EV = 1.0e-30                          # 0.05 /Mpc as an energy, order only


def _tilt() -> float:
    return 1.0 - NS_OBS


def _L() -> float:
    """``ln(k_BZ / k_pivot)`` — the model's own scale separation."""
    return DECADES_PIVOT_TO_BZ * math.log(10.0)


# ---------------------------------------------------------------------------
# T1 — feature-type vs log-type
# ---------------------------------------------------------------------------
def classification_theorem() -> dict:
    r"""A constant tilt forces the second scale to enter logarithmically."""
    x, p, C, L = sp.symbols("x p C L", positive=True)
    power_logderiv = sp.simplify(x * sp.diff(C * x ** p, x) / (C * x ** p))
    log_logderiv = sp.simplify(sp.diff(C / L, L) / (C / L) * L)
    bound = (RUN_SIGMA + abs(RUN_OBS)) / _tilt()
    Lv = _L()
    return {
        "power_law_log_derivative": str(power_logderiv),      # p
        "log_type_log_derivative": str(log_logderiv),          # -1
        "observed_bound_on_log_derivative": bound,
        "power_law_p_allowed": f"|p| < {bound:.3f}",
        "leading_lattice_correction_p": 2,
        "length_scales_excluded": 2 > bound,
        "log_type_value": 1.0 / Lv,
        "log_type_allowed": (1.0 / Lv) < bound,
        "conclusion": ("only an RG-type logarithm can supply a constant tilt; "
                       "every length scale is excluded by the SHAPE of its "
                       "k-dependence, not by its distance"),
    }


# ---------------------------------------------------------------------------
# T2/T3 — the class prediction, and the size of the coefficient
# ---------------------------------------------------------------------------
def running_prediction() -> dict:
    r"""``dn_s/dlnk = -(1-n_s)/L`` — no free parameter."""
    Lv = _L()
    pred = -_tilt() / Lv
    return {
        "L": Lv,
        "decades": DECADES_PIVOT_TO_BZ,
        "dns_dlnk_predicted": pred,
        "dns_dlnk_observed": RUN_OBS,
        "dns_dlnk_sigma": RUN_SIGMA,
        "sigma_below_current_error": RUN_SIGMA / abs(pred),
        "consistent_with_planck": abs(pred - RUN_OBS) < RUN_SIGMA,
        "testable_today": abs(pred) > RUN_SIGMA,
    }


def required_coefficient() -> dict:
    r"""``C = (1-n_s) L`` — is the tilt unnaturally small?  No."""
    Lv = _L()
    C = _tilt() * Lv
    return {
        "C": C,
        "is_order_unity": 0.1 < C < 100.0,
        "three_pi_over_two": 3.0 * math.pi / 2.0,
        "percent_from_3pi_over_2": 100.0 * abs(C - 3 * math.pi / 2) / (3 * math.pi / 2),
        "verdict": ("the tilt is NOT unnaturally small — it is one one-loop log "
                    "across the model's own 58 decades with an O(1) coefficient. "
                    "What is missing is the loop, not a small number."),
    }


# ---------------------------------------------------------------------------
# T4 — what the model actually owns
# ---------------------------------------------------------------------------
def coupling_inventory() -> dict:
    alpha_tilt = ALPHA_EM / (2 * math.pi)
    return {
        "alpha_em": {
            "tilt_if_one_loop": alpha_tilt,
            "shortfall_factor": _tilt() / alpha_tilt,
            "verdict": "~30x too small, and barely runs at CMB momenta",
        },
        "alpha_s": {
            "value_at_MZ": ALPHA_S_MZ,
            "k_pivot_eV": K_PIVOT_EV,
            "Lambda_QCD_eV": LAMBDA_QCD_EV,
            "decades_below_Lambda_QCD": math.log10(LAMBDA_QCD_EV / K_PIVOT_EV),
            "verdict": "cannot be evaluated at CMB momenta — deeply confined",
        },
        "G": {
            "runs": False,
            "Gdot_over_G": 0.0,
            "verdict": ("does NOT run: F79 structural + F284 Gdot/G = 0 exactly. "
                        "The model's sharpest prediction removes its most "
                        "natural candidate second scale"),
        },
        "blockspin": {
            "tilt_is_marginal": True,
            "verdict": "F285 D3: the spectral index is exactly marginal under it",
        },
        "any_candidate_works": False,
    }


# ---------------------------------------------------------------------------
# T5 — the look-elsewhere count
# ---------------------------------------------------------------------------
def coincidence_look_elsewhere(rational_max: int = 12) -> dict:
    r"""Count how many comparably-simple expressions hit the 1-sigma window.

    The family is fixed *before* looking: a small rational ``p/q`` (both at most
    ``rational_max``) or a registered dimensionless model constant, times an
    integer power of pi in ``{-2,-1,0,1}``.  No tuning of the family after
    seeing the answer — that is the whole point of the exercise.
    """
    t = _tilt()
    lo, hi = t - NS_SIGMA, t + NS_SIGMA
    seeds: dict[str, float] = {
        str(Fraction(p, q)): p / q
        for p in range(1, rational_max + 1)
        for q in range(1, rational_max + 1)
    }
    seeds.update({
        "delta*": delta_star_f, "lambda6": lambda_6, "c_lat": c_lat,
        "e_sat": e_saturation, "cos3d*": cos3_delta_star,
        "sin2tW": sin2_thetaW_onshell, "alpha": ALPHA_EM, "alpha_s": ALPHA_S_MZ,
    })
    hits, total, seen = [], 0, set()
    for name, v in seeds.items():
        for m, tag in ((-2, "/pi^2"), (-1, "/pi"), (0, ""), (1, "*pi")):
            val = v * math.pi ** m
            total += 1
            key = round(val, 12)
            if lo <= val <= hi and key not in seen:
                seen.add(key)
                hits.append({"expr": f"{name}{tag}", "value": val,
                             "sigma": (NS_OBS - (1 - val)) / NS_SIGMA})
    hits.sort(key=lambda h: abs(h["sigma"]))
    density_per_sigma = len(hits) / 2.0
    best = hits[0] if hits else None
    # expected number inside +/- |best sigma| if the family is featureless
    expected = density_per_sigma * 2.0 * abs(best["sigma"]) if best else 0.0
    return {
        "window": [lo, hi],
        "window_halfwidth_percent": 100.0 * NS_SIGMA / t,
        "candidates": total,
        "distinct_hits": len(hits),
        "hit_fraction_percent": 100.0 * len(hits) / total,
        "hits": hits,
        "delta_star_over_2pi": delta_star_f / (2 * math.pi),
        "equals_one_over_9pi": abs(delta_star_f / (2 * math.pi)
                                   - 1.0 / (9 * math.pi)) < 1e-15,
        "best": best,
        "expected_within_best_sigma_by_chance": expected,
        "p_at_least_one_by_chance": 1.0 - math.exp(-expected),
        "survives_look_elsewhere": len(hits) <= 1,
        "verdict": ("NOT evidence: six comparably-simple expressions land in the "
                    "same window, so being the closest of six is unremarkable. "
                    "Recorded as a coincidence under the F253/F256 standard; it "
                    "would become evidence only if a mechanism predicted the "
                    "shape first."),
    }


# ---------------------------------------------------------------------------
def run() -> dict:
    t1 = classification_theorem()
    t2 = running_prediction()
    t3 = required_coefficient()
    t5 = coincidence_look_elsewhere()
    # D9: the gate record must be able to fail. These are the finding's own
    # already-computed claims: T1 is the classification theorem (every length
    # scale excluded by shape, only a log-type scale allowed), T2 is the
    # class prediction actually matching Planck's measured running, T3 is
    # the coefficient being a natural O(1) (not unnaturally tuned), and T5
    # is that the delta*/(2pi) numerical coincidence correctly does NOT
    # survive a look-elsewhere count (the finding's own conclusion — if this
    # flipped to True it would mean the seed family stopped being a fair
    # look-elsewhere test).
    passed = bool(
        t1["length_scales_excluded"] and t1["log_type_allowed"]
        and t2["consistent_with_planck"]
        and t3["is_order_unity"]
        and not t5["survives_look_elsewhere"]
    )
    return {
        "finding": "F286",
        "question": "what could supply the 3.5% tilt on a rigid lattice?",
        "T1_classification": t1,
        "T2_running_prediction": t2,
        "T3_required_coefficient": t3,
        "T4_inventory": coupling_inventory(),
        "T5_coincidence": t5,
        "passed": passed,
        "verdict": (
            "a second scale must be a LOG, not a length; the whole class "
            "predicts dn_s/dlnk = -2.6e-4 with no free parameter; the required "
            "coefficient is a natural O(1); but the model owns no coupling that "
            "supplies the logarithm, and the delta*/(2pi) coincidence does not "
            "survive a look-elsewhere count"
        ),
    }


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    res = run()
    path = results_path("F286_second_scale.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(res, indent=2, sort_keys=True, default=str))
    print("\nwrote", path)
