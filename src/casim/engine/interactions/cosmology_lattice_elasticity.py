"""
cosmology_lattice_elasticity.py — Can the BCC lattice be elastic?  (F283, F284)
==============================================================================

Created: 2026-08-02 - 13:45

**Question.** F282 turns on the lattice cutoff sitting below the Planck mass.
The obvious escape is to make the fundamental spacing *variable* — an elastic
lattice, ``a -> s(t) a``.  Does that rescue inflation, and if not, what ARE the
primordial universe and cosmic expansion on a rigid lattice?

--------------------------------------------------------------------------
F283 — four independent answers, all negative
--------------------------------------------------------------------------

E1 (exact).  **Elasticity cannot touch F282.**  F79 ties Newton's constant to
    the spacing, ``G = a^2 c^3 / (8 pi sqrt3 hbar)``, so under ``a -> s a``:

        M_Pl = 3^(1/4) hbar/(s a c)      and      Lambda_UV = hbar/(s a c)

    scale *together*.  Their ratio is ``M_Pl/Lambda = 3^(1/4)`` and

        r = M_Pl^2 / Lambda_UV^2 = sqrt(3) = 1/c_lat      for every s,
        dr/ds = 0 identically.

    The F282 obstruction is a **dimensionless geometric invariant of the BCC
    lattice**, not a property of the F107 value of ``a``.  This CORRECTS F282
    falsifier #5, which claimed a smaller ``a`` would evaporate the no-go.  It
    cannot: the no-go is scale-free.

E2 (quantitative).  **An elastic lattice has a varying G.**  Parametrise the
    stretch as ``s ~ a_FRW^q`` (q=0 rigid, q=1 fully comoving).  Then
    ``Gdot/G = 2 q H``.  Lunar laser ranging and BBN both bound q at the
    ~1e-3 level, and a fully comoving lattice (q=1) misses BBN by 17 decades.
    **The lattice is rigid to ~0.1%** — a prediction the model did not know it
    was making.

E3 (structural).  **The volume mode is not a new field; it is ``ln K``.**  A
    variable fundamental spacing IS the conformal/volume deformation of the
    lattice, and the model already owns that mode: F79 gives it **zero tree
    stiffness**, F180 gives it a wave equation *sourced* by ``T^00``, and F216
    proves the propagating vacuum content is exactly 2 dof (TT), so ``ln K`` is
    constrained, not free.  So "make the lattice elastic" is a dichotomy:
    either it means ``K``, in which case nothing is added and the answer is
    F284; or it means a genuinely new independent scalar, in which case it
    breaks the 2-dof count and shows up as a PPN scalar at Cassini.

E4 (quantitative).  **A tree elastic term would give gravity its own light
    cone.**  F180 derives ``c_grav = c_lat`` precisely *because* the graviton
    kinetic term is the induced matter loop — it inherits the matter cone.  A
    tree-level elastic stiffness contributes with its own sound speed ``c_s``,
    breaking that inheritance.  GW170817 bounds the tree elastic fraction at
    the 1e-15 level.

--------------------------------------------------------------------------
F284 — what the primordial universe and expansion then ARE
--------------------------------------------------------------------------

The lattice is rigid and eternal; ``a`` is a constant of the substrate.  So:

  * Cosmic expansion is the evolution of the emergent metric's conformal
    factor — the homogeneous mode of ``K`` — on a **fixed** substrate.  The
    FRW scale factor is not the lattice spacing.  Falsifiable content:
    ``Gdot/G = 0`` **exactly**, where a comoving lattice predicts ``2 H_0``.
  * A comoving mode has a **fixed wavelength in cells** forever, so no mode is
    ever created or destroyed by expansion and there is **no trans-Planckian
    problem** — and equally, no mechanism to generate a spectrum by stretching.
    That is F282's conclusion arrived at from the other side.
  * There is **no initial singularity in the substrate**.  The earliest epoch
    the lattice can resolve is the one whose Hubble radius is a single cell:

        H_max = c_lat / a = 3^(-3/4) M_Pl,     t_min = a/c_lat = sqrt(3) ticks.

    Everything "before" is sub-cell, which the lattice does not resolve — the
    cutoff does the work usually handed to quantum gravity.

Real arithmetic only — no chiral/complex transforms (CLAUDE.md).
"""
from __future__ import annotations

import json
import math

import sympy as sp

from casim.constants import a_over_ellP, c_lat, c_SI, ell_P_m

__all__ = [
    "invariance_under_stretch",
    "varying_G_bounds",
    "volume_mode_dichotomy",
    "graviton_cone_bound",
    "earliest_resolvable_epoch",
    "lattice_cell_budget",
    "run",
]

# --- external measurements -------------------------------------------------
H0_KM_S_MPC = 67.4                      # Planck 2018 TT,TE,EE+lowE+lensing
MPC_IN_M = 3.0856775814913673e22
YEAR_IN_S = 3.1557e7

# Lunar laser ranging. Hofmann & Muller 2018 (CQG 35 035015) is the tightest;
# the looser value is carried so the conclusion does not ride on one analysis.
LLR_BOUNDS = {"hofmann_muller_2018_2sigma": 1.5e-13, "conservative": 4.0e-13}

# BBN: helium-4 abundance vs an altered expansion rate. z_BBN ~ 4e8.
Z_BBN = 4.0e8
BBN_DELTA_G_BOUNDS = (0.10, 0.20)

# GW170817 + GRB 170817A: -3e-15 < (c_grav - c_EM)/c_EM < 7e-16.
GW170817_DC_OVER_C = 3.0e-15

# Cassini Shapiro delay: |gamma - 1| < 2.3e-5.
CASSINI_GAMMA_MINUS_1 = 2.3e-5

# SI, for the epoch numbers. ell_P and c come from the registry (D7); the
# Planck TIME has no registry symbol yet, so it stays a declared CODATA literal
# here and is used only for the informational t_min/t_P ratio.
T_PLANCK_S = 5.391247e-44               # CODATA Planck time, display only


def _H0_per_year() -> float:
    return H0_KM_S_MPC * 1.0e3 / MPC_IN_M * YEAR_IN_S


# ---------------------------------------------------------------------------
# E1 — the obstruction is invariant under any elastic stretch (exact)
# ---------------------------------------------------------------------------
def invariance_under_stretch() -> dict:
    r"""``dr/ds = 0``: F282's ``r = sqrt(3)`` survives ``a -> s a`` identically.

    Done symbolically, keeping ``hbar``, ``c``, ``a`` and ``s`` free, so the
    cancellation is exhibited rather than asserted.
    """
    a, hbar, c, s = sp.symbols("a hbar c s", positive=True)
    G = (s * a) ** 2 * c ** 3 / (8 * sp.pi * sp.sqrt(3) * hbar)   # F79
    M2 = sp.simplify(hbar * c / (8 * sp.pi * G))                  # reduced M_Pl^2
    Lam = sp.simplify(hbar / ((s * a) * c))                       # cutoff as a mass
    ratio = sp.simplify(sp.sqrt(M2) / Lam)
    r = sp.simplify(M2 / Lam ** 2)
    dr_ds = sp.simplify(sp.diff(r, s))
    return {
        "M_Pl_over_Lambda": str(ratio),
        "r": str(r),
        "r_float": float(r),
        "dr_ds": str(dr_ds),
        "invariant": dr_ds == 0,
        "r_equals_inverse_c_lat": abs(float(r) - 1.0 / c_lat) < 1e-14,
        "corrects": "F282 falsifier #5 (a rescaling of a CANNOT falsify the no-go)",
    }


# ---------------------------------------------------------------------------
# E2 — an elastic lattice varies G; LLR and BBN bound how elastic it can be
# ---------------------------------------------------------------------------
def varying_G_bounds() -> dict:
    r"""``G ~ s^2`` (F79), so ``s ~ a_FRW^q`` gives ``Gdot/G = 2 q H``."""
    H0 = _H0_per_year()
    comoving_rate = 2.0 * H0                       # the q = 1 prediction
    llr = {
        name: {"bound_per_yr": b, "q_max": b / comoving_rate,
               "exclusion_factor": comoving_rate / b}
        for name, b in LLR_BOUNDS.items()
    }
    # BBN: |ln(G_BBN/G_0)| = 2 q ln(1+z)
    bbn = {
        f"delta_G_{d:g}": {"q_max": d / (2.0 * math.log1p(Z_BBN))}
        for d in BBN_DELTA_G_BOUNDS
    }
    comoving_G_ratio = (1.0 + Z_BBN) ** -2
    q_max = min([v["q_max"] for v in llr.values()] + [v["q_max"] for v in bbn.values()])
    return {
        "H0_per_yr": H0,
        "comoving_Gdot_over_G_per_yr": comoving_rate,
        "llr": llr,
        "bbn": bbn,
        "z_BBN": Z_BBN,
        "comoving_G_BBN_over_G0": comoving_G_ratio,
        "comoving_bbn_decades_off": -math.log10(comoving_G_ratio),
        "q_max": q_max,
        "rigid_to_percent": 100.0 * q_max,
        "fully_comoving_excluded": q_max < 1.0,  # D9: derived from q_max, not hardcoded
    }


# ---------------------------------------------------------------------------
# E3 — the volume mode is ln K, or it is a new scalar that Cassini sees
# ---------------------------------------------------------------------------
def volume_mode_dichotomy() -> dict:
    r"""Either elasticity IS ``K`` (nothing new), or it is a PPN scalar.

    For a Brans-Dicke-like matter-scalar coupling ``alpha``,
    ``gamma - 1 = -2 alpha^2/(1 + alpha^2)``, so Cassini bounds ``alpha``.
    A mode of the substrate that carries gravity would have ``alpha = O(1)``.
    """
    g = CASSINI_GAMMA_MINUS_1
    alpha2 = g / (2.0 - g)                     # from |gamma-1| = 2a^2/(1+a^2)
    return {
        "branch_A": "the volume mode IS ln K — constrained, not free "
                    "(F79 zero tree stiffness; F180 sourced wave equation; "
                    "F216 exactly 2 propagating dof). Nothing is added; see F284.",
        "branch_B": "a genuinely new independent scalar dof — breaks F216's "
                    "2-dof count and appears as a PPN scalar.",
        "cassini_gamma_minus_1": g,
        "alpha_squared_max": alpha2,
        "alpha_max": math.sqrt(alpha2),
        "natural_alpha_for_a_substrate_mode": 1.0,
        "suppression_required": 1.0 / math.sqrt(alpha2),
        "graviton_dof_F216": 2,
    }


# ---------------------------------------------------------------------------
# E4 — a tree elastic term would give gravity its own cone; GW170817 bounds it
# ---------------------------------------------------------------------------
def graviton_cone_bound(cs_squared_offset: float = 1.0) -> dict:
    r"""Tree elastic fraction ``f_tree`` from ``dc/c ~ (f_tree/2)(c_s^2/c_lat^2 - 1)``.

    F180's ``c_grav = c_lat`` is *derived* from the kinetic term being purely
    the induced matter loop. A tree stiffness adds an independent cone.
    """
    f_tree = 2.0 * GW170817_DC_OVER_C / cs_squared_offset
    return {
        "gw170817_dc_over_c": GW170817_DC_OVER_C,
        "cs_squared_offset_assumed": cs_squared_offset,
        "tree_elastic_fraction_max": f_tree,
        "decades_below_unity": -math.log10(f_tree),
        "c_grav_equals_c_lat_source": "F180 (induced loop inherits the matter cone)",
    }


# ---------------------------------------------------------------------------
# F284 — the earliest epoch the rigid lattice can resolve
# ---------------------------------------------------------------------------
def earliest_resolvable_epoch() -> dict:
    r"""The Hubble radius equals one cell at ``H = c_lat/a = 3^(-3/4) M_Pl``.

    With ``a = 3^(1/4)/M_Pl`` (F282 leg A, reduced units) and
    ``R_H = c_lat/H``, setting ``R_H = a`` gives ``H = c_lat/a``.
    ``t_min = 1/H = a/c_lat = sqrt(3)`` ticks: light crosses one cell in
    ``1/c_lat = sqrt(3)`` ticks, so the first resolvable moment is one
    cell-crossing old.  No singularity — just a sub-cell region the lattice
    does not resolve.
    """
    a_over_ell_red = 3.0 ** 0.25
    H_max_over_MPl = c_lat / a_over_ell_red
    a_SI = a_over_ellP * ell_P_m
    # Canonical tick (si_scale): tau = c_lat a / c, so that c_lat a/tau = c.
    # t_min = (1/c_lat) ticks = a/c seconds.  Before 2026-09-29 this was
    # a/(c_lat c) = sqrt(3) a/c, i.e. a tick of a/c — sqrt(3) longer than the
    # si_scale / cosmology_lambda_dynamics tick (t_min/t_P moves 11.43 -> 6.60).
    tau_s = c_lat * a_SI / c_SI
    t_min_s = (1.0 / c_lat) * tau_s
    return {
        "H_max_over_MPl": H_max_over_MPl,
        "H_max_closed_form": 3.0 ** -0.75,
        "t_min_ticks": 1.0 / c_lat,
        "t_min_ticks_closed_form": math.sqrt(3.0),
        "a_metres": a_SI,
        "tick_seconds": tau_s,
        "t_min_seconds": t_min_s,
        "t_min_over_planck_time": t_min_s / T_PLANCK_S,
        "singularity_in_substrate": False,
        "power_of_three_ladder": {
            "c_lat": "3^(-1/2)",
            "Lambda_UV_over_MPl": "3^(-1/4)",
            "H_max_over_MPl": "3^(-3/4)",
            "r_min": "3^(+1/2)",
        },
    }


def lattice_cell_budget() -> dict:
    """How many cells the present Hubble volume holds — the substrate is vast."""
    a_SI = a_over_ellP * ell_P_m
    R_H = c_SI / (H0_KM_S_MPC * 1.0e3 / MPC_IN_M)
    cells = R_H / a_SI
    return {
        "R_H_metres": R_H,
        "R_H_in_cells": cells,
        "hubble_volume_in_cells": cells ** 3,
        "comoving_mode_wavelength_in_cells": "constant — the lattice does not stretch",
        "trans_planckian_problem": False,
    }


# ---------------------------------------------------------------------------
def run() -> dict:
    e1 = invariance_under_stretch()
    e2 = varying_G_bounds()
    epoch = earliest_resolvable_epoch()
    cell_budget = lattice_cell_budget()
    # D9: the gate record must be able to fail. These are the finding's own
    # already-computed exact/definitional claims (docstring E1/F284 above),
    # not new physics: dr/ds = 0 exactly (E1), the comoving (q=1) elasticity
    # is excluded by the LLR/BBN bound (E2), and the rigid-substrate F284
    # consequences (no substrate singularity, no trans-Planckian problem).
    passed = bool(
        e1["invariant"] and e1["r_equals_inverse_c_lat"]
        and e2["fully_comoving_excluded"]
        and epoch["singularity_in_substrate"] is False
        and cell_budget["trans_planckian_problem"] is False
    )
    return {
        "findings": ["F283", "F284"],
        "question": "can the BCC lattice be elastic, and if not what is expansion?",
        "E1_invariance": e1,
        "E2_varying_G": e2,
        "E3_volume_mode": volume_mode_dichotomy(),
        "E4_graviton_cone": graviton_cone_bound(),
        "F284_earliest_epoch": epoch,
        "F284_cell_budget": cell_budget,
        "passed": passed,
        "verdict": (
            "the lattice is rigid (q < 1e-3); elasticity cannot rescue F282 "
            "(dr/ds = 0 exactly); cosmic expansion is the conformal mode of K "
            "on a fixed substrate, predicting Gdot/G = 0 exactly"
        ),
    }


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    res = run()
    path = results_path("F283_F284_lattice_elasticity.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(res, indent=2, sort_keys=True, default=str))
    print("\nwrote", path)
