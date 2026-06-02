"""
Fork F46-Dirac — GRAVITY VIA THE SPHERICAL-TRIANGLE LEGS (tetrad Dirac / Fork E3)
================================================================================
Drafted 2026-05-28.  Realises the "curved-spacetime extension" follow-up of
Finding 46 (§9.3) and the "E3 — tetrad Dirac" rung promised in
`gr_fork_E_tensor.py`.

Background
----------
F46 proved the *exact* lattice Dirac dispersion is a spherical-Pythagorean
identity on a right spherical triangle:

      cos Ω_Dirac(k, m)  =  cos Ω_rest(m) · cos ω_kin(k)
                         =  √(1−m²) · cos ω_kin(k)

with the rest leg  Ω_rest = arcsin(m)  (the F27 mass / zitterbewegung
rotation) and the kinetic leg  ω_kin(k)  (the F25/F26 photon rotation, whose
small-k slope is the lattice speed of light c_lat = dω_kin/d|k|).

This fork asks: what happens to that triangle in a *static* curved background?

Tetrad derivation (Sachs route, notebook pp. 16–17, 32–33)
----------------------------------------------------------
Take a static, diagonal metric written with lapse A and spatial factor B,

      ds² = −A(x) c₀² dt²  +  B(x) δ_ij dx^i dx^j       (g₀₀ = −A, g_ii = B)

The diagonal tetrad is  e^0_0 = √A,  e^k_i = √B δ^k_i, so the inverse tetrad
is  e_0^0 = 1/√A,  e_k^i = δ/√B.  Insert into the chiral (Weyl) curved Dirac
equation  i γ^a e_a^μ (∂_μ + Ω_μ) ψ = m ψ  and, dropping the spin connection
Ω_μ (it sources geodesic bending / the gravitational force, not the leading
frequency shift), multiply the time component through by √A γ⁰:

      i ∂_t ψ  =  [  c₀ √(A/B) · α·p̂   +   √A · m c₀² · β  ] ψ
                   └────── kinetic ──────┘   └──── rest ────┘

So **both legs of the F46 triangle become site-dependent**:

      kinetic leg :  ω_kin(k; x)  with effective speed  c_eff(x) = c₀ √(A/B)
      rest    leg :  Ω_rest(m; x) = √A(x) · arcsin(m)        (lapse-rescaled)

and the coordinate-frame Dirac dispersion is the **covariant F46 identity**

   ┌─────────────────────────────────────────────────────────────────────┐
   │ cos Ω_Dirac^coord(x,k,m) = cos(√A(x)·arcsin m) · cos ω_kin(k; c_eff(x))│
   └─────────────────────────────────────────────────────────────────────┘

Continuum limit (small angles):
      Ω² ≈ (√A · m c₀²)²  +  (c_eff |k|)²
         =  A m² c₀⁴   +   (A/B) c₀² |k|²
which is exactly the dispersion of the curved-tetrad Hamiltonian above.

Which leg carries the gravitational redshift?  (Correction to F46 §9.3)
-----------------------------------------------------------------------
F46 §9.3 guessed redshift "enters as a site-dependent renormalisation of the
*kinetic* leg."  The tetrad derivation shows that is the wrong leg for the
*static* (Pound–Rebka) redshift:

  • A static massive clock has k = 0, so the kinetic leg ω_kin = 0 and
    cos ω_kin = 1 *regardless of c_eff(x)*.  A kinetic-leg-only scheme leaves
    Ω_Dirac(k=0) = arcsin(m) everywhere — i.e. NO static redshift.  (This is
    precisely the Finding 14.5 / F16 "single-scalar can't do both" tension,
    seen from the triangle.)

  • The static redshift is carried by the **rest leg** via the lapse:
        Ω_Dirac^coord(k=0) = √A(x) · arcsin(m),
    so two clocks at x₁, x₂ tick in the ratio √(A₁/A₂).  For a weak field
    A = 1 + 2φ/c₀² this gives Δν/ν = Δφ/c₀² — the correct GR factor 1, not
    the baseline factor 2.

  • The kinetic-leg renormalisation (c_eff = c₀√(A/B)) instead carries the
    *propagation* sector: light bending (GR-1), Shapiro delay (GR-2), and the
    finite-k slowing of matter packets.  In the photon limit m = 0 the rest
    leg vanishes and Ω_Dirac = ω_kin(k; c_eff), with c_eff = Fork-B/Fork-E
    c_γ = c₀√(A/B).

Net: redshift = lapse on the **rest** leg;  deflection/Shapiro = c_eff on the
**kinetic** leg.  Both are "site-dependent renormalisations of a leg," which is
why the loose F46 wording is half-right; the *static-clock* redshift is the
rest leg.  This reconciles F46 with F16 (Forks A/B fix GR-3 by decoupling the
clock √A from the propagator c_eff) and discharges Fork E's E3 promise.

Interface
---------
Matches gr3_fork_*.py / gr_fork_E_tensor.py so it drops into the GR harness:

    c_photon(phi, c_0)   c_matter(phi, c_0)   tau_rate(phi, c_0)
    metric(phi, c_0) -> (A, B)     (g_00 = -A, g_ii = B)

Plus the F46-specific predictions:

    rest_leg(phi, c_0, m)            = √A · arcsin(m)
    kinetic_leg(k, phi, c_0, m)      = ω_kin(k; c_eff)        (continuum slope c_eff)
    dirac_omega_coord(k, phi, c_0, m)= arccos(cos rest · cos kin)   (exact triangle)

The metric is reused from gr_fork_E_tensor (exact isotropic-Schwarzschild by
default), so this fork inherits E2's all-PN-orders metric for one static source.
"""

from __future__ import annotations
from types import SimpleNamespace
import os
import sys

import numpy as np

_THIS = os.path.dirname(__file__)
if _THIS not in sys.path:
    sys.path.insert(0, _THIS)

import gr_fork_E_tensor as forkE   # noqa: E402  (metric source)


# ───────────────────────────────────────────────────────────────────
#  Metric + scalar wave speeds (inherited from Fork E)
# ───────────────────────────────────────────────────────────────────

def _AB(phi, c_0, mode="exact_isotropic"):
    """(A, B) with g_00 = -A, g_ii = B.  Defaults to exact isotropic-Schwarzschild."""
    fork = forkE.make_fork(mode)
    return fork.metric(np.asarray(phi, dtype=np.float64), c_0)


def metric(phi, c_0, mode="exact_isotropic"):
    return _AB(phi, c_0, mode)


def c_eff_matter(phi, c_0, mode="exact_isotropic"):
    """Kinetic-leg effective speed c_eff = c_0 √(A/B) seen by a Dirac packet."""
    A, B = _AB(phi, c_0, mode)
    return c_0 * np.sqrt(np.abs(A) / B)


def r_kin(phi, c_0=1.0, mode="exact_isotropic"):
    """Dimensionless kinetic-leg renormalisation r_kin(x) = c_eff/c_0 = √(A/B).

    This is the *gravitational* rescaling of the kinetic leg, independent of
    the unit-bearing c_0.  In a well A<1, B>1 ⇒ r_kin<1, so the rate-rescaled
    exact-QCA leg stays inside the Brillouin zone (bounded by r_kin·π < π).
    """
    A, B = _AB(phi, c_0, mode)
    return np.sqrt(np.abs(A) / B)


# Harness aliases ----------------------------------------------------
def c_photon(phi, c_0, mode="exact_isotropic"):
    return c_eff_matter(phi, c_0, mode)


def c_matter(phi, c_0, mode="exact_isotropic"):
    return c_eff_matter(phi, c_0, mode)


def tau_rate(phi, c_0, mode="exact_isotropic"):
    """Proper-time tick rate = lapse √A (rest-leg renormalisation factor)."""
    A, _ = _AB(phi, c_0, mode)
    return np.sqrt(np.abs(A))


# ───────────────────────────────────────────────────────────────────
#  F46 spherical-triangle legs in the curved background
# ───────────────────────────────────────────────────────────────────

def rest_leg(phi, c_0, m, mode="exact_isotropic"):
    """Ω_rest(x) = √A(x) · arcsin(m).  Carries the static gravitational redshift."""
    return tau_rate(phi, c_0, mode) * float(np.arcsin(m))


def omega_kin_qca_flat(k):
    """Flat exact-QCA Weyl kinetic leg ω_kin⁰(k) = arccos(c_x·c_y), with
    c_i = cos(k_i/√2)  (Paper 1 Eq. 16 = ca_core_exact.exact2d_dispersion;
    the F25/F26/F46 kinetic leg).  Bounded in [0, π]; small-k slope 1/√2.

    Accepts a length-2 wavevector (kx, ky) or scalar arrays.
    """
    k = np.asarray(k, dtype=np.float64)
    if k.ndim and k.shape[-1] == 2:
        kx, ky = k[..., 0], k[..., 1]
    else:                                   # scalar |k| along the diagonal
        kx = ky = k / np.sqrt(2.0)
    inv_root2 = 1.0 / np.sqrt(2.0)
    cprod = np.cos(kx * inv_root2) * np.cos(ky * inv_root2)
    return np.arccos(np.clip(cprod, -1.0, 1.0))


def kinetic_leg(k, phi, c_0, m=0.0, mode="exact_isotropic", form="exact_qca"):
    """Site-dependent kinetic leg ω_kin(k; x).

    form="exact_qca"  (default, promoted form):
        ω_kin = r_kin(x) · arccos(c_x·c_y),   r_kin = √(A/B).
        The bounded Paper-1 Eq.16 Weyl walk, rate-rescaled by the
        gravitational factor √(A/B).  Reduces to the flat F46 leg
        arccos(c_x c_y) when A=B, stays inside the Brillouin zone
        (≤ r_kin·π < π in a well), and carries the finite-k lattice
        anisotropy / dispersion of the true QCA.

    form="continuum":
        ω_kin = c_eff(x) · |k|,  c_eff = c_0√(A/B).  The small-k slope
        used as the Euclidean reference (matches F46-P7's expansion).
    """
    if form == "continuum":
        kk = np.asarray(k, dtype=np.float64)
        kmag = np.sqrt(np.sum(kk**2)) if kk.ndim else float(kk)
        return c_eff_matter(phi, c_0, mode) * kmag
    if form == "exact_qca":
        return r_kin(phi, c_0, mode) * omega_kin_qca_flat(k)
    raise ValueError(f"form must be 'exact_qca' or 'continuum'; got {form!r}")


def dirac_omega_coord(k, phi, c_0, m, mode="exact_isotropic", form="exact_qca"):
    """Coordinate-frame Dirac per-tick angle via the covariant F46 identity:

        cos Ω = cos(rest_leg) · cos(kinetic_leg)

    With form="exact_qca" both factors are bounded, so Ω is the genuine
    bounded-QCA Dirac dispersion in the curved background; at A=B=1 it
    reduces bit-for-bit to the flat F46 identity cos Ω = √(1−m²)·c_x·c_y.
    """
    a = rest_leg(phi, c_0, m, mode)
    b = kinetic_leg(k, phi, c_0, m, mode, form=form)
    cprod = np.clip(np.cos(a) * np.cos(b), -1.0, 1.0)
    return np.arccos(cprod)


def dirac_omega_continuum(k, phi, c_0, m, mode="exact_isotropic"):
    """Euclidean-Pythagorean (continuum) prediction Ω² = rest² + kin².

    Equivalently the curved-tetrad Hamiltonian dispersion
        Ω² = A m² c₀⁴ + (A/B) c₀² |k|².
    Used as the small-angle reference for the spherical identity above
    (uses the continuum kinetic leg).
    """
    a = rest_leg(phi, c_0, m, mode)
    b = kinetic_leg(k, phi, c_0, m, mode, form="continuum")
    return np.sqrt(a**2 + b**2)


# ───────────────────────────────────────────────────────────────────
#  Prototype implementable stepper  (Strang: kinetic c_eff + rest √A)
# ───────────────────────────────────────────────────────────────────
#
# One coordinate tick of the gravity Dirac CA:
#
#     Mix_rest(√A·m, dt/2) ∘ Kinetic(c_eff, dt) ∘ Mix_rest(√A·m, dt/2)
#
# • Mix_rest is the per-cell exact-unitary η↔χ rotation by angle
#   θ(x) = √A(x)·m·dt  (the redshifted rest leg).  This is the existing
#   ca_dirac._mix_eta_chi with a site-dependent angle.
# • Kinetic is the existing ca_curved variable-c machinery applied
#   independently to each chirality (the renormalised kinetic leg).
#
# Each sub-operator is exactly unitary, so total norm is conserved to the
# kinetic stepper's tolerance; Strang error is O(dt²·|∇A|, dt²·|∇c_eff|).
# This realises the boxed identity above at the propagator level.


def make_kinetic_solver(c_eff_field, dt=1.0, n_sub=4):
    """Build a reusable exactly-unitary variable-c kinetic solver for the
    static c_eff(x) field (one LU factorisation, shared by η and χ)."""
    sim_root = os.path.abspath(os.path.join(_THIS, ".."))
    if sim_root not in sys.path:
        sys.path.insert(0, sim_root)
    from ca_curved import CayleyVarcSolver2D
    return CayleyVarcSolver2D(c_eff_field, dt=dt, n_sub=n_sub)


def gravity_dirac_step_2d(eta_u, eta_d, chi_u, chi_d,
                          A_field, c_eff_field, m, dt=1.0, n_sub=4,
                          kinetic_solver=None, kinetic="cayley",
                          r_kin_scalar=None):
    """One Strang tick of the F46 gravity Dirac CA on a 2D lattice.

        Mix_rest(√A·m, dt/2) ∘ Kinetic(dt) ∘ Mix_rest(√A·m, dt/2)

    Parameters
    ----------
    eta_u, eta_d, chi_u, chi_d : (Lx, Ly) complex — Weyl spinor components.
    A_field   : (Lx, Ly) real — lapse² (g_00 = -A); rest leg uses √A.
    c_eff_field : (Lx, Ly) real — kinetic-leg speed c_0√(A/B) (Cayley path).
    m  : float — dimensionless mass (|m| ≤ 1).
    dt : float — coordinate time step.
    n_sub : int — sub-steps for the variable-c kinetic step.
    kinetic : "cayley" | "qca".
        "cayley" — centered-difference variable-c Crank–Nicolson stepper
                   (`ca_curved`); handles an inhomogeneous c_eff_field but its
                   band is the centered-difference one.
        "qca"    — the *bounded exact-QCA* Weyl walk (Paper-1 Eq. 16),
                   rate-rescaled by the scalar r_kin_scalar = √(A/B).
                   Realises ω_kin = r_kin·arccos(c_x c_y) exactly (machine ε).
                   Spectral ⇒ requires a (near-)uniform r_kin (homogeneous or
                   adiabatic background).
    kinetic_solver : optional cached CayleyVarcSolver2D (Cayley path only).
    r_kin_scalar : float — uniform √(A/B) for the "qca" path.

    Each sub-operator is exactly unitary ⇒ norm conserved to the FP/solver
    floor; Strang error O(dt²·|∇A|, dt²·|∇c_eff|).
    """
    sim_root = os.path.abspath(os.path.join(_THIS, ".."))
    if sim_root not in sys.path:
        sys.path.insert(0, sim_root)
    from ca_dirac import _mix_eta_chi, _weyl_half_step_2c

    theta_half = np.sqrt(np.abs(A_field)) * m * dt * 0.5   # redshifted rest leg

    # rest half-step
    eta_u, eta_d, chi_u, chi_d = _mix_eta_chi(eta_u, eta_d, chi_u, chi_d,
                                              theta_half)
    # kinetic full step — η and χ propagate independently
    if kinetic == "qca":
        if r_kin_scalar is None:
            r_kin_scalar = float(np.mean(np.asarray(c_eff_field)))  # fallback
        dt_eff = float(r_kin_scalar) * dt
        # one full QCA step = two exact-QCA half-steps of dt_eff/2
        eta_u, eta_d = _weyl_half_step_2c(eta_u, eta_d, 0.5 * dt_eff)
        eta_u, eta_d = _weyl_half_step_2c(eta_u, eta_d, 0.5 * dt_eff)
        chi_u, chi_d = _weyl_half_step_2c(chi_u, chi_d, 0.5 * dt_eff)
        chi_u, chi_d = _weyl_half_step_2c(chi_u, chi_d, 0.5 * dt_eff)
    else:
        if kinetic_solver is None:
            kinetic_solver = make_kinetic_solver(c_eff_field, dt=dt, n_sub=n_sub)
        eta_u, eta_d = kinetic_solver.step(eta_u, eta_d)
        chi_u, chi_d = kinetic_solver.step(chi_u, chi_d)
    # rest half-step
    eta_u, eta_d, chi_u, chi_d = _mix_eta_chi(eta_u, eta_d, chi_u, chi_d,
                                              theta_half)
    return eta_u, eta_d, chi_u, chi_d


# ───────────────────────────────────────────────────────────────────
#  Module-level harness drop-in (matches gr3_fork_* interface)
# ───────────────────────────────────────────────────────────────────

NAME = "fork_F46_dirac_tetrad"
DESCRIPTION = ("F46 covariant triangle: redshift on rest leg (√A), "
               "deflection/Shapiro on kinetic leg (c_eff=c_0√(A/B)). "
               "Tetrad Dirac = Fork E3.")


def make_fork(mode="exact_isotropic"):
    def _metric(phi, c_0): return _AB(phi, c_0, mode)
    def _cph(phi, c_0):    return c_eff_matter(phi, c_0, mode)
    def _cmt(phi, c_0):    return c_eff_matter(phi, c_0, mode)
    def _tau(phi, c_0):    return tau_rate(phi, c_0, mode)
    return SimpleNamespace(
        NAME=f"fork_F46_dirac_{mode}", DESCRIPTION=DESCRIPTION,
        metric=_metric, c_photon=_cph, c_matter=_cmt, tau_rate=_tau,
        rest_leg=lambda phi, c_0, m: rest_leg(phi, c_0, m, mode),
        dirac_omega_coord=lambda k, phi, c_0, m: dirac_omega_coord(k, phi, c_0, m, mode),
        mode=mode,
    )
