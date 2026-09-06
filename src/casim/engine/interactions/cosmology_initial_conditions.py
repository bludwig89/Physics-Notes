"""
cosmology_initial_conditions.py — What n_s can an initial-condition measure give?  (F285)
=========================================================================================

Created: 2026-08-02 - 16:00

**Question.**  F282 proved the model has no inflaton; F284 showed the rigid
substrate offers no process that could generate a spectrum, so the primordial
``P(k)`` must live in the automaton's ``t=0`` state.
``docs/theory/primordial-sector.md`` §7 handed on three untested directions for
making that respectable.  This module executes all three and asks the only
question that matters: **what ``n_s`` does each actually predict?**

--------------------------------------------------------------------------
The one relation everything runs through
--------------------------------------------------------------------------

Poisson (the model's own F106 law, ``grad^2 ln K = -8 pi G T^00``) gives
``Phi(k) ~ rho(k)/k^2``, so ``P_Phi = P_rho / k^4``.  With
``Delta^2(k) = k^3 P(k)/2pi^2`` and ``Delta^2_Phi ~ k^(n_s - 1)``:

        P_rho(k)  ~  k^(n_s)          <-- exact, and the whole story.

So "what is n_s?" is literally "what is the large-scale slope of the initial
energy-density power spectrum?"  Observation (Planck 2018) wants
``P_rho ~ k^0.9649``, i.e. very nearly ``k^1``.

--------------------------------------------------------------------------
D1 — a natural measure on the t=0 state
--------------------------------------------------------------------------

  * **Uniform / maximum-entropy** (each cell independent): white noise,
    ``P_rho = const`` -> **n_s = 0**.
  * **Any local functional of short-range-correlated fields** (thermal, gapped,
    even a critical Gaussian field squared): for ``k << 1/xi`` the density
    correlator tends to a constant -> **n_s = 0** again.  This is the robust
    generic case and it does not depend on criticality details.
  * **Locally conserved** initial data (energy-momentum conservation forbids
    the ``k^0`` and ``k^2`` terms — the Traschen integral constraints):
    ``P_rho ~ k^4`` -> **n_s = 4**.  The classic causal-seed result.
  * **Scale-free in the metric** ("the simplest non-trivial initial condition
    for ``ln K``", ``Delta^2_Phi = const``): **n_s = 1 exactly** — Harrison-
    Zel'dovich.  This is the most charitable reading available, and Planck
    excludes exactly 1 at **8.4 sigma**.

The two generic measures bracket the observation (0 and 4) without touching it,
and the one principled scale-free choice overshoots by 8.4 sigma.

--------------------------------------------------------------------------
D2 — the Brillouin-zone edge
--------------------------------------------------------------------------

Dead, quantitatively: the CMB pivot sits ~58 decades below the BZ edge, so a
lattice correction of order ``(k a)^2`` is ~1e-117.  And because F284's lattice
is **rigid**, that ratio is time-independent — the BZ edge was never nearer to
observable scales at any epoch.  That is strictly stronger than the naive
statement.

--------------------------------------------------------------------------
D3 — block-spin stability
--------------------------------------------------------------------------

Proved symbolically: under a Kadanoff dilation a power law ``P(k) = A k^n`` maps
to ``b^-(3+n) A k^n`` — the **same exponent for every n**, with the whole effect
absorbed into the amplitude.  So the fixed-point set is a one-parameter *line*
of power laws and ``n`` is an exactly **marginal** label.  Block-spin explains
why ``P(k)`` should be a power law and says **nothing** about the tilt.

Note the contrast with F282 C3: there the *dynamical operator* spectrum has an
``O(1)`` gap around marginality, so there is nothing for a slow-roll field to
BE; here the *initial-state* spectral index is exactly marginal, so there is
nothing to FIX THE TILT.  Two different objects; both cut the same way.

--------------------------------------------------------------------------
The synthesis
--------------------------------------------------------------------------

The only scale-free initial condition is ``n_s = 1``, excluded at 8.4 sigma.
A *tilt* requires a second scale.  The rigid lattice has exactly one scale
(``a``), 58 decades away, contributing ~1e-117.  Inflation supplies the second
scale for free (``n_s - 1 = -6 eps + 2 eta`` is small *because* it is a
slow-roll ratio) — and that is exactly the object F282 excluded.

**So the hard observation is not the scale invariance. It is the 3.5%
departure from it.**

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import json
import math

import sympy as sp

from casim.constants import a_over_ellP, ell_P_m

__all__ = [
    "ns_from_density_slope",
    "measure_predictions",
    "required_non_genericity",
    "brillouin_zone_reach",
    "blockspin_tilt_marginality",
    "tilt_needs_a_second_scale",
    "run",
]

# Planck 2018 TT,TE,EE+lowE+lensing.
NS_OBS = 0.9649
NS_OBS_SIGMA = 0.0042
K_PIVOT_PER_MPC = 0.05
MPC_IN_M = 3.0856775814913673e22

# The four candidate measures, as large-scale slopes of P_rho(k) ~ k^m.
# n_s = m exactly (see the module docstring).
MEASURE_SLOPES = {
    "uniform_max_entropy": 0.0,
    "local_short_range_correlated": 0.0,
    "locally_conserved_causal": 4.0,
    "scale_free_in_the_metric": 1.0,
}


def ns_from_density_slope(m: float) -> float:
    """``P_rho ~ k^m`` implies ``n_s = m``. Poisson supplies the ``k^-4``."""
    return m


# ---------------------------------------------------------------------------
# D1 — what each candidate measure predicts
# ---------------------------------------------------------------------------
def measure_predictions() -> dict:
    out = {}
    for name, m in MEASURE_SLOPES.items():
        ns = ns_from_density_slope(m)
        out[name] = {
            "P_rho_slope": m,
            "n_s": ns,
            "deviation_sigma": abs(NS_OBS - ns) / NS_OBS_SIGMA,
        }
    brackets = (
        min(v["n_s"] for v in out.values()) < NS_OBS < max(v["n_s"] for v in out.values())
    )
    return {
        "candidates": out,
        "n_s_observed": NS_OBS,
        "sigma": NS_OBS_SIGMA,
        "generic_measures_bracket_without_hitting": brackets,
        "best_candidate": min(out, key=lambda k: out[k]["deviation_sigma"]),
        "best_deviation_sigma": min(v["deviation_sigma"] for v in out.values()),
    }


def required_non_genericity() -> dict:
    r"""How far the initial state must sit from white noise at the CMB pivot.

    In units of the BZ edge, the pivot is at ``x = k_pivot/k_BZ``.  White noise
    is ``P_rho ~ k^0``; observation needs ``k^n_s``.  The ratio at the pivot is
    ``x^n_s`` — the size of the required departure from the generic measure.
    """
    a_m = a_over_ellP * ell_P_m
    k_BZ = math.pi / a_m                                  # rad/m
    k_pivot = K_PIVOT_PER_MPC / MPC_IN_M                  # rad/m
    x = k_pivot / k_BZ
    decades = -math.log10(x)
    return {
        "a_metres": a_m,
        "k_BZ_per_m": k_BZ,
        "k_pivot_per_m": k_pivot,
        "pivot_over_BZ": x,
        "decades_below_BZ": decades,
        "suppression_vs_white_noise_decades": decades * NS_OBS,
        "enhancement_vs_conserved_causal_decades": decades * (4.0 - NS_OBS),
        "comment": ("the initial state must carry ~56 decades LESS large-scale "
                    "power than white noise, and ~177 decades MORE than "
                    "conserved-causal — non-generic in both directions"),
    }


# ---------------------------------------------------------------------------
# D2 — the Brillouin-zone edge is 58 decades away, permanently
# ---------------------------------------------------------------------------
def brillouin_zone_reach() -> dict:
    r"""Lattice corrections go as ``(k a)^2``; at the pivot that is ~1e-117."""
    g = required_non_genericity()
    ka = g["pivot_over_BZ"] * math.pi          # k*a, undoing the pi in k_BZ
    return {
        "decades_below_BZ": g["decades_below_BZ"],
        "k_times_a_at_pivot": ka,
        "leading_correction_ka_squared": ka ** 2,
        "correction_decades": -math.log10(ka ** 2),
        "time_independent_because_lattice_is_rigid": True,
        "verdict": ("closed — and permanently, since a rigid lattice (F284) "
                    "keeps k/k_BZ fixed at every epoch"),
    }


# ---------------------------------------------------------------------------
# D3 — block-spin preserves EVERY power law: the tilt is exactly marginal
# ---------------------------------------------------------------------------
def blockspin_tilt_marginality(b_value: int = 2,
                               slopes=(-2, -1, 0, 1, 2, 4)) -> dict:
    r"""Every power law is a fixed point of the Kadanoff dilation. Exactly.

    This is a theorem, not a measurement, and it is proved here symbolically.
    Under a dilation ``x -> b x`` (equivalently ``k -> k/b``), a power law
    ``P(k) = A k^n`` maps to

        P'(k) = b^(-(3+n)) A k^n            (d = 3, with the standard
                                             field-variance normalisation)

    — **the same exponent for every n**, with the whole effect of the
    transformation absorbed into the amplitude.  So the fixed-point set of the
    block-spin map is a one-parameter *line* of power laws, and ``n`` is an
    exactly **marginal** label along it: ``d(exponent)/d(block step) = 0``
    identically.

    (A Monte-Carlo version of this — generate Gaussian fields, block-average,
    refit the slope — was tried first and discarded.  Block averaging is a
    top-hat *plus decimation*, so it carries a window bias and an aliasing sum
    that are artifacts of the estimator rather than of the RG, and they swamp
    the effect at the few-percent level.  Verifying a three-line identity with
    a noisy estimator that introduces two of its own is the wrong instrument.)

    **The point, and the contrast with F282 C3.**  F282 found the *dynamical*
    operator spectrum has an ``O(1)`` gap around marginality — there is nothing
    for a slow-roll field to *be*.  Here the *initial-state* spectral index is
    exactly marginal — there is nothing to *fix the tilt*.  Two different
    marginality statements about two different objects, and both cut against
    the model.
    """
    A, k, b = sp.symbols("A k b", positive=True)

    def _exponent(expr):
        """The log-slope ``k d(log P)/dk`` — reads off the exponent for any n."""
        return sp.simplify(k * sp.diff(sp.log(expr), k))

    rows = {}
    for n in slopes:
        P = A * k ** n
        # dilation k -> k/b, with the d=3 variance normalisation
        P_prime = sp.simplify((P.subs(k, k / b)) * b ** -3)
        amp = sp.simplify(P_prime / k ** n)
        rows[f"n={n:+d}"] = {
            "input_exponent": n,
            "image": str(P_prime),
            "amplitude_factor": str(sp.simplify(amp / A)),
            "exponent_preserved": bool(sp.simplify(_exponent(P_prime) - n) == 0),
            "recovered_exponent": int(_exponent(P_prime)),
        }
    all_preserved = all(v["exponent_preserved"] for v in rows.values())

    # General n: the exponent out equals the exponent in, identically.
    n_sym = sp.Symbol("n", real=True)
    img = sp.simplify((A * k ** n_sym).subs(k, k / b) * b ** -3)
    exp_out = _exponent(img)
    return {
        "b": b_value,
        "rows": rows,
        "every_power_law_preserved": all_preserved,
        "general_exponent_out": str(exp_out),
        "exponent_is_marginal": bool(sp.simplify(exp_out - n_sym) == 0),
        "fixed_point_set": "a one-parameter LINE of power laws",
        "contrast_with_F282_C3": (
            "F282 C3: the DYNAMICAL operator spectrum has an O(1) gap around "
            "marginality (nothing to be a slow-roll field). Here: the "
            "INITIAL-STATE spectral index is exactly marginal (nothing to fix "
            "the tilt). Different objects, same direction of damage."),
        "conclusion": ("block-spin gives the power-law FORM for free and "
                       "cannot select the tilt"),
    }


# ---------------------------------------------------------------------------
# The synthesis — a tilt needs a second scale, and the lattice has none
# ---------------------------------------------------------------------------
def tilt_needs_a_second_scale() -> dict:
    hz_sigma = abs(NS_OBS - 1.0) / NS_OBS_SIGMA
    bz = brillouin_zone_reach()
    return {
        "only_scale_free_choice_is_ns_1": True,
        "hz_exact_deviation_sigma": hz_sigma,
        "tilt_magnitude": abs(1.0 - NS_OBS),
        "lattice_scales_available": 1,
        "lattice_scale_imprint_at_pivot": bz["leading_correction_ka_squared"],
        "inflation_supplies_tilt_as": "n_s - 1 = -6 eps + 2 eta (a slow-roll ratio)",
        "verdict": ("the hard observation is NOT the scale invariance — it is "
                    "the 3.5% DEPARTURE from it, which needs a slowly-evolving "
                    "second scale, i.e. exactly what F282 excluded"),
    }


# ---------------------------------------------------------------------------
def run() -> dict:
    d1 = measure_predictions()
    d3 = blockspin_tilt_marginality()
    synthesis = tilt_needs_a_second_scale()
    # D9: the gate record must be able to fail. These are the finding's own
    # already-computed exact claims: D3 is a symbolic theorem (every power
    # law is a block-spin fixed point, and the exponent is exactly marginal
    # — proved via sympy, not measured), and D1 is the observational fact
    # that n_s=0.9649 sits strictly between the two generic-measure
    # predictions (0 and 4) without matching either.
    passed = bool(
        d3["every_power_law_preserved"] and d3["exponent_is_marginal"]
        and d1["generic_measures_bracket_without_hitting"]
    )
    return {
        "finding": "F285",
        "question": "what n_s can an initial-condition measure actually give?",
        "key_relation": "P_rho(k) ~ k^(n_s), via Poisson + Delta^2 = k^3 P",
        "D1_measures": d1,
        "D1b_non_genericity": required_non_genericity(),
        "D2_brillouin_zone": brillouin_zone_reach(),
        "D3_blockspin": d3,
        "synthesis": synthesis,
        "passed": passed,
        "verdict": (
            "all three directions close: generic measures give n_s = 0 or 4, "
            "the one scale-free choice gives exactly 1 (8.4 sigma off), the BZ "
            "edge is 58 decades away permanently, and block-spin fixes the "
            "shape but leaves the tilt marginal"
        ),
    }


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    res = run()
    path = results_path("F285_initial_condition_measure.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(res, indent=2, sort_keys=True, default=str))
    print("\nwrote", path)
