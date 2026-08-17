"""
cosmology_primordial.py — Does the lattice admit an inflaton?  (F282)
=====================================================================

Created: 2026-08-02 - 11:40

**Question** (completeness-2026-08-02 gap #1, rubric row K4).  The model has no
inflaton finding, no preheating finding and no primordial-power-spectrum module
— F238 §6 documents that absence and pins ``Omega_DM`` to it.  Before building
such a sector, ask the prior question: *does this model admit a slow-roll
direction at all?*  A no-go here is worth as much as a mechanism.

**Answer: no.**  Every scalar direction the model owns fails slow roll by
O(1)–O(10), and they all fail for the *same* reason, which is exact:

    LEG A (exact).  The F107 canonical cell fixes the lattice spacing at
        a / ell_P = sqrt(8 pi) * 3^(1/4)      (F79 structural G, F107 adoption)
    and the *reduced* Planck length is ell_red = sqrt(8 pi) ell_P, so

        a / ell_red = 3^(1/4)  exactly,   Lambda_UV = 1/a = 3^(-1/4) M_Pl,

    i.e. the lattice UV cutoff is **sub-Planckian**, and the dimensionless
    obstruction constant is

        r_min  =  M_Pl^2 / Lambda_UV^2  =  sqrt(3)  =  1 / c_lat     (exact).

    The number that blocks inflation is the *inverse lattice light speed*.
    Equivalently  Lambda_UV = sqrt(c_lat) * M_Pl.

    LEG B (structural).  A cellular automaton has a bounded per-cell state
    space — unit spinors, SU(2) links, compact angles.  There is no non-compact
    scalar direction to run up.  So every candidate's canonical decay constant
    is  f = sqrt(J)/a  with J the dimensionless lattice stiffness, and every
    slow-roll parameter carries the universal prefactor

        r  =  M_Pl^2 / f^2  =  sqrt(3) / J .

    LEG C (computed, per candidate).  For each candidate the model's OWN
    potential — no free parameters are left in it — gives

        min over the field range of  max(eps, |eta|)  =  K * r,

    with K a pure number computed here.  Slow roll needs that below ~0.02.

The two E_g directions are the only genuine scalar directions in the model
(the model is Higgs-free by construction, F27), and they independently demand
f ~ 20 M_Pl — about 28x the lattice cutoff — i.e. a stiffness J ~ 5e2-8e2 in a
sector where every coupling the model has computed is O(1).

Also checked here: the periodic-potential spectral-index bound (any cosine
potential gives n_s <= 1 - sqrt(3)/J, vs Planck 0.9649 +/- 0.0042), the
Starobinsky R^2 escape (induced c2 is short of the required ~5e8 by ~9.7
decades), and the N-flation escape (needs ~400x more scalar directions than
the model has).

Real arithmetic only — no chiral/complex transforms (CLAUDE.md).
"""
from __future__ import annotations

import json
import math
from typing import Callable

from casim.constants import (
    a_over_ellP,
    c_lat,
    e_saturation,
    lambda_6,
)
from casim.numerics import xp

__all__ = [
    "cutoff_ratio",
    "slowroll",
    "min_slowroll",
    "eg_clock_coefficient",
    "eg_radial_coefficient",
    "periodic_ns_bound",
    "starobinsky_gap",
    "rg_marginality",
    "required_decay_constant",
    "run",
]

# The F118 self-consistent (kappa_E, c, W) point on the spontaneous-E_g branch,
# section 4: kappa_E = -2.156, c = 1.10, v = 0.16, W = W*(v) = 0.438.  These are
# the model's own numbers, not fits made here.
F118_KAPPA_E = -2.156
F118_C_QUARTIC = 1.10

# Planck 2018 TT,TE,EE+lowE+lensing.
NS_OBS = 0.9649
NS_OBS_SIGMA = 0.0042

# Slow-roll target.  |eta| <~ 1/(2 N_e) with N_e ~ 55-60 e-folds; 0.02 is the
# standard loose threshold and is generous.
SLOWROLL_TARGET = 0.02

# One-loop induced-gravity R^2 coefficient scale: c2 ~ N_dof / (96 pi^2).
INDUCED_C2_DENOM = 96.0 * math.pi ** 2
# Scalaron mass that reproduces A_s = 2.1e-9 in Starobinsky inflation.
STAROBINSKY_MS_OVER_MPL = 1.3e-5


# ---------------------------------------------------------------------------
# Leg A — the exact sub-Planckian cutoff
# ---------------------------------------------------------------------------
def cutoff_ratio() -> dict:
    r"""``M_Pl^2 / Lambda_UV^2`` for the F107 canonical cell.

    ``a/ell_P = sqrt(8 pi) 3^{1/4}`` and ``ell_red = sqrt(8 pi) ell_P``, so
    ``a/ell_red = 3^{1/4}`` exactly and ``r_min = sqrt(3) = 1/c_lat``.
    """
    a_over_ellred = a_over_ellP / math.sqrt(8.0 * math.pi)
    return {
        "a_over_ellP": a_over_ellP,
        "a_over_ell_reduced": a_over_ellred,
        "a_over_ell_reduced_closed_form": 3.0 ** 0.25,
        "Lambda_over_MPl": 1.0 / a_over_ellred,
        "Lambda_over_MPl_closed_form": math.sqrt(c_lat),
        "r_min": a_over_ellred ** 2,
        "r_min_closed_form": 1.0 / c_lat,
        "sub_planckian": a_over_ellred > 1.0,
    }


# ---------------------------------------------------------------------------
# Leg B/C — generic slow-roll machinery in units of r = M_Pl^2 / f^2
# ---------------------------------------------------------------------------
def slowroll(V: Callable, dV: Callable, d2V: Callable, chi):
    """``(eps/r, |eta|/r)`` at dimensionless field value(s) ``chi``.

    ``phi = f * chi``, so ``eps = (r/2)(V'/V)^2`` and ``eta = r V''/V`` with
    primes taken with respect to ``chi``.  Factoring ``r`` out is the whole
    point: it is the same universal number for every candidate.
    """
    v = V(chi)
    return 0.5 * (dV(chi) / v) ** 2, xp.abs(d2V(chi) / v)


def min_slowroll(V, dV, d2V, lo: float, hi: float, n: int = 400001):
    """Minimise ``max(eps, |eta|)/r`` over ``chi`` in ``[lo, hi]``."""
    chi = xp.linspace(lo, hi, n)
    eps, eta = slowroll(V, dV, d2V, chi)
    worst = xp.maximum(eps, eta)
    i = int(xp.argmin(worst))
    return float(worst[i]), float(chi[i])


def required_decay_constant(K: float, target: float = SLOWROLL_TARGET) -> dict:
    """What ``f`` and ``J`` a candidate with coefficient ``K`` would need."""
    r_req = target / K
    return {
        "K": K,
        "r_required": r_req,
        "f_over_MPl_required": 1.0 / math.sqrt(r_req),
        "J_required": (1.0 / c_lat) / r_req,
        "value_at_J_unity": K / c_lat,
    }


# ---------------------------------------------------------------------------
# Candidate 1 — the E_g clock angle delta.  V = lambda_6 e^6 cos^2(3 delta)
# ---------------------------------------------------------------------------
def eg_clock_coefficient() -> dict:
    r"""The E_g sextic clock invariant, ``V = lambda_6 e^6 cos^2(3 delta)``.

    Writing ``u = cos(6 delta)``, ``V = (A/2)(1+u)`` with ``A = lambda_6 e^6``:

        eps/r  = 18 (1-u)/(1+u),      |eta|/r = 36 |u|/(1+u).

    ``eps`` falls and ``|eta|`` rises with ``u``; they cross at ``u = 1/3``,
    where both equal ``9``.  So ``K = 9`` — closed form, independent of
    ``lambda_6`` and ``e`` (the amplitude cancels between ``V''`` and ``V``).
    The harmonic number 6 of the clock invariant is what makes this large:
    a generic ``p``-fold periodic potential gives ``K = p^2/4``.
    """
    A = lambda_6 * e_saturation ** 6

    def V(x):
        return 0.5 * A * (1.0 + xp.cos(6.0 * x))

    def dV(x):
        return -3.0 * A * xp.sin(6.0 * x)

    def d2V(x):
        return -18.0 * A * xp.cos(6.0 * x)

    # delta in (0, pi/6): the max at delta=0 down to the min at delta=pi/6.
    # Stop short of the minimum, where V -> 0 and both parameters diverge.
    K_num, chi = min_slowroll(V, dV, d2V, 1e-9, 0.999 * math.pi / 6.0)
    u_star = 1.0 / 3.0
    K_closed = 18.0 * (1.0 - u_star) / (1.0 + u_star)
    out = {
        "amplitude_A": A,
        "K_closed_form": K_closed,
        "K_numeric": K_num,
        "argmin_delta": chi,
        "argmin_cos6delta": math.cos(6.0 * chi),
    }
    out.update(required_decay_constant(K_closed))
    return out


# ---------------------------------------------------------------------------
# Candidate 2 — the E_g radial magnitude e (the F118 Mexican hat)
# ---------------------------------------------------------------------------
def eg_radial_coefficient() -> dict:
    r"""The F118 spontaneous-E_g hat, ``V = (kappa_E/2) e^2 + c e^4 + lambda_6 e^6``.

    The additive constant is **not** free: F193 proves the ontic lattice vacuum
    gravitates as exactly zero, so ``V(e_min) = 0`` and the hilltop energy
    ``V(0) = -hat(e_min)`` is fixed.  With that, every number below is
    determined by the model.
    """
    kE, c4, l6 = F118_KAPPA_E, F118_C_QUARTIC, lambda_6

    def hat(e):
        return 0.5 * kE * e ** 2 + c4 * e ** 4 + l6 * e ** 6

    def hat1(e):
        return kE * e + 4.0 * c4 * e ** 3 + 6.0 * l6 * e ** 5

    def hat2(e):
        return kE + 12.0 * c4 * e ** 2 + 30.0 * l6 * e ** 4

    # hat'(e) = 0 with e != 0:  6 l6 e^4 + 4 c e^2 + kappa_E = 0
    disc = (4.0 * c4) ** 2 - 4.0 * (6.0 * l6) * kE
    e2 = (-4.0 * c4 + math.sqrt(disc)) / (2.0 * 6.0 * l6)
    e_min = math.sqrt(e2)
    V0 = -hat(e_min)                      # forced by F193

    def V(e):
        return hat(e) + V0

    K_num, chi = min_slowroll(V, hat1, hat2, 1e-6, e_min * 0.999)
    out = {
        "kappa_E": kE,
        "c_quartic": c4,
        "lambda_6": l6,
        "e_min": e_min,
        "e_saturation_F118": e_saturation,
        "V0_forced_by_F193": V0,
        "eta_over_r_at_hilltop": hat2(0.0) / V0,
        "K_numeric": K_num,
        "argmin_e": chi,
    }
    out.update(required_decay_constant(K_num))
    return out


# ---------------------------------------------------------------------------
# Cross-check — the spectral-index bound for ANY periodic direction
# ---------------------------------------------------------------------------
def periodic_ns_bound(J: float = 1.0, p: int = 1) -> dict:
    r"""``n_s`` for a ``p``-fold periodic potential ``Lambda^4 (1 - cos(p phi/f))``.

    ``n_s - 1 = 2 eta - 6 eps = -p^2 r (3+u)/(1-u)`` with ``u = cos(p phi/f)``.
    ``(3+u)/(1-u)`` is minimised at ``u = -1`` (the hilltop) where it equals 1,
    so ``n_s <= 1 - p^2 r`` over the whole field range.  ``p = 1`` is the most
    generous case; the model's own clock invariant has ``p = 6``.
    """
    r = (1.0 / c_lat) / J
    ns_max = 1.0 - p ** 2 * r
    return {
        "J": J,
        "harmonic_p": p,
        "r": r,
        "ns_max": ns_max,
        "ns_observed": NS_OBS,
        "sigma": NS_OBS_SIGMA,
        "deviation_sigma": (NS_OBS - ns_max) / NS_OBS_SIGMA,
    }


# ---------------------------------------------------------------------------
# Cross-check — the Starobinsky R^2 escape
# ---------------------------------------------------------------------------
def starobinsky_gap(n_dof: float = 100.0) -> dict:
    r"""``R^2`` plateau inflation needs ``c2 ~ 5e8``; induced gravity gives O(0.1).

    For ``L = (M_Pl^2/2) R + c2 R^2`` the scalaron mass is
    ``M_s^2 = M_Pl^2/(12 c2)``, and the CMB amplitude fixes
    ``M_s ~ 1.3e-5 M_Pl``.  F79 gives gravity **zero tree stiffness** — the
    whole graviton kinetic term is the induced matter loop — so ``c2`` is a
    one-loop induced coefficient ``~ N_dof/(96 pi^2)``, not a free parameter.
    """
    c2_req = 1.0 / (12.0 * STAROBINSKY_MS_OVER_MPL ** 2)
    c2_ind = n_dof / INDUCED_C2_DENOM
    Ms_ind = 1.0 / math.sqrt(12.0 * c2_ind)
    return {
        "n_dof": n_dof,
        "c2_required": c2_req,
        "c2_induced": c2_ind,
        "shortfall": c2_req / c2_ind,
        "shortfall_decades": math.log10(c2_req / c2_ind),
        "scalaron_mass_over_MPl_induced": Ms_ind,
        "lattice_cutoff_over_MPl": math.sqrt(c_lat),
        "scalaron_above_cutoff": Ms_ind > math.sqrt(c_lat),
    }


# ---------------------------------------------------------------------------
# Cross-check — slow roll IS near-marginality, and F130 measured the spectrum
# ---------------------------------------------------------------------------
def rg_marginality(b: float = 2.0, n_max: int = 4) -> dict:
    r"""Restate the no-go in RG language against F130's measured eigenvalues.

    A slow-roll direction is an operator that is *nearly marginal*: it must
    barely change under a scale change, or ``eta = M^2 V''/V`` is not small.
    Marginal means Kadanoff eigenvalue ``lambda = b^0 = 1``.

    F130 measured the full spectrum of the block-spin transformation on this
    lattice: **one** relevant direction, confinement, ``lambda_sigma = b``
    (exact); every lattice-artifact / LIV operator irrelevant with
    ``lambda_n = b^{-n}``, ``n >= 2`` (exact, a round-off-floor identity); the
    deconfining ``lambda`` irrelevant at ``~b^{-2}``.  The continuum light
    speed is the one marginal direction (``b^0``) — and it is not a scalar
    field with a potential, it is the fixed point itself.

    So the spectrum has a **gap around marginality**: the nearest scaling
    exponents to 0 are ``+1`` and ``-2``.  There is no nearly-marginal scalar
    operator for a slow-roll field to be.  This is the same O(1) obstruction
    the potentials give, read off the RG flow instead of a Lagrangian.
    """
    exponents = {"confinement_sigma": 1.0, "deconfining_lambda": -2.0}
    exponents.update({f"LIV_n{n}": -float(n) for n in range(2, n_max + 1)})
    scalar_exponents = {k: v for k, v in exponents.items()}
    gap = min(abs(v) for v in scalar_exponents.values())
    return {
        "b": b,
        "exponents": exponents,
        "eigenvalues": {k: b ** v for k, v in exponents.items()},
        "marginal_exponent": 0.0,
        "gap_to_marginality": gap,
        "any_nearly_marginal_scalar": gap < 0.1,
    }


# ---------------------------------------------------------------------------
def run() -> dict:
    cut = cutoff_ratio()
    clock = eg_clock_coefficient()
    radial = eg_radial_coefficient()
    return {
        "finding": "F282",
        "question": "does the CA model admit a slow-roll inflaton direction?",
        "cutoff": cut,
        "eg_clock_angle": clock,
        "eg_radial_magnitude": radial,
        "periodic_ns_bound_p1_J1": periodic_ns_bound(1.0, 1),
        "periodic_ns_bound_p6_J1": periodic_ns_bound(1.0, 6),
        "starobinsky": starobinsky_gap(100.0),
        "rg_marginality": rg_marginality(),
        "n_scalar_directions_available": 2,
        "n_scalar_directions_required_Nflation": clock["J_required"] / 1.0,
        "verdict": "no slow-roll direction; primordial P(k) is an initial condition",
    }


if __name__ == "__main__":                          # pragma: no cover
    # Imported here, not at module scope: the write must never fire on import
    # (pkgutil / pytest collection / `casim index` all walk the package).
    from casim.engine.particles._results_path import results_path

    res = run()
    path = results_path("F282_primordial_sector_nogo.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
    print(json.dumps(res, indent=2, sort_keys=True))
    print("\nwrote", path)
