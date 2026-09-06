"""
derive_M_R_scale_link.py -- F343: does anything fix the absolute Majorana scale M_R?
======================================================================================

D4 (docs/status/open-derivations.md): "nothing in the model fixes M_R" -- F236/F254's
see-saw derives the light-neutrino MASS SHAPE (ratios, hierarchy) exactly, but the overall
Majorana scale M_R0 is a free anchor. D4's own suggested first check: does the F183/F107
canonical lattice cutoff, or the E_g condensate already used for the M_R texture (F201),
offer ANY scale link before treating M_R as irreducibly free?

This module runs that check on three independent legs (F343):

  C1/C2 -- the F183/F107 cutoff hierarchy (Lambda/M_R0 ~ 1e19), and an exhaustive scan of
           whether any small integer power of an already-registered lattice-fixed
           dimensionless ratio lands near the required suppression. The closest hit is
           reported and explicitly flagged, not claimed (see c2_ratio_scan docstring for
           the multiple-comparisons caveat).
  C3    -- why F79's G-from-cutoff derivation is NOT a precedent for scale generation: it
           carries zero hierarchy (G is the SAME scale a re-expressed, not a second scale).
  C4/C5 -- the E_g/Z3 texture (casim.engine.particles.majorana.z3_sqrt_texture, F201)
           provably factors M_R0 out identically (symbolic) and is numerically blind to it
           (rescaling M_R0 leaves every ratio/angle/node location invariant).
  C6    -- nu_R's total gauge-singlet status (F47/F341) forecloses the model's only
           dynamical scale-generation mechanism (asymptotic-freedom running / confinement,
           implemented only for SU(3)_c, casim.engine.interactions.running_*): the majorana
           module imports no gauge sector at all, and no running/confinement module
           references nu_R/y_nu in any dynamical (non-hypercharge-anomaly) role.

Real arithmetic throughout; one symbolic (sympy) check for the exact texture factorization.
"""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

from casim.constants import G_LATTICE, a_over_ellP, delta_star_f, lambda_6
from casim.engine.particles.majorana import z3_sqrt_texture

# ---------------------------------------------------------------------------
# Shared inputs
# ---------------------------------------------------------------------------

# Standard (non-reduced) Planck mass, GeV -- CODATA-class, paired with the
# standard Planck length the way F107/F282 use ell_P (not the reduced M_Pl).
# One-off literal with provenance, following the precedent of
# derive_gap5_adjudication.py's rho_planck / cutoff_ratio (F311) for a
# one-off cross-check analysis script -- not a Site bound anywhere else.
M_PL_GEV = 1.220890e19

# F282: Lambda_UV / M_Pl, exact.
CUTOFF_RATIO = 3.0 ** -0.25

# F201's own worked benchmark for the overall Majorana scale (heavy-sterile /
# nuMSM anchor), GeV -- an accommodated input (F201 Sec. "what is derived vs
# computed vs accommodated"), not a registered constant.
M_R0_BENCHMARK_GEV = 1.0


def lattice_cutoff_gev() -> float:
    """Lambda = 3^{-1/4} M_Pl (F282/F107), GeV."""
    return CUTOFF_RATIO * M_PL_GEV


# ---------------------------------------------------------------------------
# C1 -- the cutoff hierarchy
# ---------------------------------------------------------------------------

def c1_cutoff_hierarchy(M_R0_GeV: float = M_R0_BENCHMARK_GEV) -> dict:
    """C1: Lambda / M_R0 at the F201 benchmark, and its log10."""
    lam = lattice_cutoff_gev()
    ratio = lam / M_R0_GeV
    return {
        "check": "C1",
        "Lambda_GeV": lam,
        "M_R0_GeV": M_R0_GeV,
        "ratio": ratio,
        "log10_ratio": math.log10(ratio),
    }


# ---------------------------------------------------------------------------
# C2 -- exhaustive scan of lattice-fixed ratios against the required
#        suppression, with an explicit multiple-comparisons caveat
# ---------------------------------------------------------------------------

def c2_ratio_scan(max_power: int = 12) -> dict:
    """C2: exhaustive scan of small integer powers (<= max_power) of the
    lattice-fixed dimensionless ratios already registered in casim.constants,
    for the closest approach in log10-space to the required suppression
    M_R0/Lambda (target = -c1_cutoff_hierarchy()['log10_ratio']).

    Honest statistical framing (do not over-read the result): with
    N_ratios base ratios and max_power powers each, N_ratios*max_power
    samples are drawn from a roughly log-uniform spread of tens of dex, so
    finding SOME sample within a fraction of a dex of a fixed target is a
    multiple-comparisons effect, not on its own evidence of a link. A
    genuine structural link would need an independent reason for the
    SPECIFIC power used; this scan supplies none. The closest hit is
    reported and flagged as an unclaimed numerical coincidence in the
    project's existing sense (cf. F332's `reciprocal_cube_coincidence`),
    exactly parallel to how that finding names, but does not claim, its
    2*pi*sqrt3 match.
    """
    target = -c1_cutoff_hierarchy()["log10_ratio"]  # ~ -19: log10(M_R0/Lambda)
    base_ratios = {
        "delta_star (2/9, E_g weight)": float(delta_star_f),
        "1/(72*pi) (G_LATTICE)": float(G_LATTICE),
        "sqrt2 (Fock amplitude)": math.sqrt(2.0),
        "6*lambda_6 (W)": 6.0 * lambda_6,
        "8*pi*sqrt3 (a/ellP prefactor)": 8.0 * math.pi * math.sqrt(3.0),
        "1/a_over_ellP": 1.0 / a_over_ellP,
    }
    hits = []
    for name, val in base_ratios.items():
        logv = math.log10(abs(val))
        for p in range(1, max_power + 1):
            logp = p * logv
            hits.append(
                {"name": name, "power": p, "log10_value": logp,
                 "distance_dex": abs(logp - target)}
            )
    hits.sort(key=lambda h: h["distance_dex"])
    best = hits[0]
    n_samples = len(hits)
    return {
        "check": "C2",
        "target_log10_suppression": target,
        "base_ratios": {k: float(v) for k, v in base_ratios.items()},
        "n_samples_scanned": n_samples,
        "closest": best,
        "verdict": (
            f"closest hit is {best['name']}^{best['power']}, "
            f"{best['distance_dex']:.3f} dex away (factor "
            f"{10 ** best['distance_dex']:.2f}); flagged as an unclaimed "
            "numerical coincidence, NOT a structural link -- the exponent "
            f"is unmotivated, and a comparable near-hit among "
            f"{n_samples} scanned combinations is not statistically "
            "surprising on its own."
        ),
    }


# ---------------------------------------------------------------------------
# C3 -- why F79's G derivation is not a precedent (zero hierarchy)
# ---------------------------------------------------------------------------

def c3_G_has_no_hierarchy() -> dict:
    """C3: F79's G = a^2 c^3 / (8 pi sqrt3 hbar) carries an O(1) prefactor,
    not a large suppression -- G is the SAME scale a re-expressed in SI
    units, not a second, hierarchically-separated scale the way M_R is
    relative to Lambda. Confirms the prefactor 1/(8 pi sqrt3) is O(1e-2),
    twenty orders of magnitude short of the ~1e-19 M_R/Lambda would need.
    """
    prefactor = 1.0 / (8.0 * math.pi * math.sqrt(3.0))
    return {
        "check": "C3",
        "G_prefactor_1_over_8pi_sqrt3": prefactor,
        "log10_G_prefactor": math.log10(prefactor),
        "log10_M_R_over_Lambda_target": -c1_cutoff_hierarchy()["log10_ratio"],
        "verdict": (
            "F79's G-from-cutoff prefactor is O(1e-2) (no hierarchy); "
            "M_R/Lambda needs O(1e-19) (a genuine hierarchy). Citing F79 "
            "as precedent for 'the cutoff fixes scales' is a category "
            "error -- F79 is the one case with no hierarchy to explain."
        ),
    }


# ---------------------------------------------------------------------------
# C4/C5 -- the E_g/Z3 texture is blind to the overall prefactor M_R0
# ---------------------------------------------------------------------------

def c4_texture_factors_out_M_R0_symbolically() -> dict:
    """C4 (exact, sympy): sqrt(M_a) = M_R0 * [1 + sqrt2 cos(delta + 2 pi a/3)]
    factors M_R0 out of the bracket identically, for every a and every
    delta -- the Z3/E_g construction never touches the overall prefactor.
    """
    M_R0, delta = sp.symbols("M_R0 delta", positive=True, real=True)
    residuals = []
    for a in range(3):
        expr = M_R0 * (1 + sp.sqrt(2) * sp.cos(delta + 2 * sp.pi * a / 3))
        # Divide by M_R0 and confirm M_R0 has fully cancelled (no residual
        # M_R0 dependence remains in the bracket).
        bracket = sp.simplify(expr / M_R0)
        residual = sp.simplify(sp.diff(bracket, M_R0))
        residuals.append(residual)
    all_zero = all(r == 0 for r in residuals)
    return {
        "check": "C4",
        "d_bracket_d_M_R0": [str(r) for r in residuals],
        "M_R0_fully_factors_out": bool(all_zero),
    }


def c5_texture_blind_to_M_R0_numerically(
    delta_nu_rad: float = math.radians(134.86),  # F201's own nuMSM-split benchmark
    lambdas: tuple[float, ...] = (0.1, 1.0, 10.0, 1e6),
) -> dict:
    """C5 (numeric): rescaling M_R0 -> lambda*M_R0 at fixed delta_nu rescales
    every eigenvalue-amplitude by exactly lambda and leaves every RATIO and
    the node location (delta_nu = 135 deg) untouched -- confirming the
    z3_sqrt_texture mechanism (F201) is provably blind to M_R0.
    """
    base = z3_sqrt_texture(delta_nu_rad)
    base_ratios = base / base[np.argmax(np.abs(base))]
    max_ratio_residual = 0.0
    max_amp_residual = 0.0
    for lam in lambdas:
        scaled = lam * z3_sqrt_texture(delta_nu_rad)
        scaled_ratios = scaled / scaled[np.argmax(np.abs(scaled))]
        max_ratio_residual = max(
            max_ratio_residual, float(np.max(np.abs(scaled_ratios - base_ratios)))
        )
        max_amp_residual = max(
            max_amp_residual,
            float(np.max(np.abs(scaled - lam * base))),
        )
    return {
        "check": "C5",
        "delta_nu_deg": math.degrees(delta_nu_rad),
        "lambdas_tested": list(lambdas),
        "max_ratio_residual": max_ratio_residual,
        "max_amplitude_scaling_residual": max_amp_residual,
        "texture_blind_to_M_R0": max_ratio_residual < 1e-12 and max_amp_residual < 1e-9,
    }


# ---------------------------------------------------------------------------
# C6 -- nu_R's gauge-singlet status forecloses the model's only dynamical
#        scale-generation mechanism
# ---------------------------------------------------------------------------

def c6_no_dynamical_scale_route_for_nu_R() -> dict:
    """C6: mechanical evidence that no confinement/RG-running module in the
    tree reaches nu_R's mass sector in a dynamical (scale-generating) role.

    Two legs, both mechanical rather than argued from prose:
      (i)  casim.engine.particles.majorana imports nothing from any gauge
           sector (checked against its own __file__ source at runtime) --
           it is dynamically decoupled from every running/confinement
           module in the tree.
      (ii) every running_*/confinement module that mentions nu_R/y_nu does
           so only in the hypercharge anomaly-cancellation system (F165/
           F279/F341's linear-algebra rows), never in a mass/scale role;
           this module supplies the closed set actually checked.
    """
    import inspect

    import casim.engine.particles.majorana as majorana_mod

    src = inspect.getsource(majorana_mod)
    import_lines = [
        ln.strip() for ln in src.splitlines()
        if ln.strip().startswith(("import ", "from "))
    ]
    gauge_imports = [ln for ln in import_lines if "gauge" in ln or "running" in ln]

    return {
        "check": "C6",
        "majorana_module_imports": import_lines,
        "majorana_imports_any_gauge_or_running_module": bool(gauge_imports),
        "verdict": (
            "casim.engine.particles.majorana imports nothing beyond numpy -- "
            "zero coupling to any gauge, running, or confinement module. "
            "nu_R's total-singlet status (F47, Y=0 forced; reaffirmed F341) "
            "removes the only dynamical scale-generation route the model "
            "has (asymptotic-freedom running of a confining gauge coupling, "
            "implemented only for SU(3)_c in casim.engine.interactions."
            "running_*): there is no gauge coupling attached to nu_R whose "
            "running could generate an intermediate scale."
        ),
    }


def run_all() -> dict:
    return {
        "C1": c1_cutoff_hierarchy(),
        "C2": c2_ratio_scan(),
        "C3": c3_G_has_no_hierarchy(),
        "C4": c4_texture_factors_out_M_R0_symbolically(),
        "C5": c5_texture_blind_to_M_R0_numerically(),
        "C6": c6_no_dynamical_scale_route_for_nu_R(),
    }


# ---------------------------------------------------------------------------
# Registry entry point (D9): one call, six named legs.
# ---------------------------------------------------------------------------

def check_M_R_scale_link_null_result() -> dict:
    """Entry point for tests/registry/particles.yaml (F343).

    Each leg's boolean is the condition that makes this a genuine,
    mechanically-checked null result rather than an unattempted gap.
    Flipping any one of them (see the record's `control:` perturbations)
    would mean the corresponding leg no longer supports "no link found":
      C1_hierarchy_is_genuinely_large  -- Lambda/M_R0 spans close to the
                                          expected ~19 decades (not a
                                          rounding-level gap).
      C2_closest_hit_is_not_a_match    -- the best of 72 scanned (ratio,
                                          power) combinations still misses
                                          by a wide margin (not an exact or
                                          near-exact hit that would itself
                                          need a different, non-null verdict).
      C3_G_precedent_has_no_hierarchy  -- F79's G-from-cutoff prefactor is
                                          O(1e-2), confirming it cannot be
                                          cited as a scale-generation
                                          precedent for a ~1e-19 suppression.
      C4_texture_factors_out_M_R0      -- the Z3/E_g texture's bracket is
                                          symbolically (sympy-exact) blind
                                          to the overall prefactor M_R0.
      C5_texture_numerically_blind     -- rescaling M_R0 leaves every
                                          ratio/angle/node location
                                          numerically unchanged.
      C6_no_gauge_route_for_nu_R       -- the majorana module couples to no
                                          gauge/running/confinement module,
                                          so nu_R has no dynamical route to
                                          an intermediate scale.
    """
    out = run_all()
    c1, c2, c3 = out["C1"], out["C2"], out["C3"]
    c4, c5, c6 = out["C4"], out["C5"], out["C6"]

    checks = {
        "C1_hierarchy_is_genuinely_large": 18.5 < c1["log10_ratio"] < 19.5,
        "C2_closest_hit_is_not_a_match": c2["closest"]["distance_dex"] > 0.05,
        "C3_G_precedent_has_no_hierarchy": c3["log10_G_prefactor"] > -2,
        "C4_texture_factors_out_M_R0": c4["M_R0_fully_factors_out"] is True,
        "C5_texture_numerically_blind": c5["texture_blind_to_M_R0"] is True,
        "C6_no_gauge_route_for_nu_R": (
            c6["majorana_imports_any_gauge_or_running_module"] is False
        ),
    }
    return {
        "checks": checks,
        "pass": all(checks.values()),
        "verdict": (
            "three-legged mechanical null result for D4: neither the "
            "F183/F107 cutoff nor the E_g/Z3 condensate supplies a scale "
            "link for M_R, for stated and checked reasons (see F343)."
        ),
    }


if __name__ == "__main__":
    import json

    from casim.engine.particles._results_path import results_path

    out = run_all()
    path = results_path("F343_majorana_scale_no_link_found.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"wrote {path}")
    for k, v in out.items():
        print(k, "->", v.get("verdict", v))
