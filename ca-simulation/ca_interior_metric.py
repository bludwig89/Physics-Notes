"""
ca_interior_metric.py  --  Covariant two-function interior metric kernel (F181)
===============================================================================

The follow-up scoped by **F178** (gravity sources from the full stress-energy
tensor; the single-scalar dielectric is demoted to the vacuum/weak-field
representation).  Inside matter the metric must carry its **second independent
function**: by F173 the impedance-locked single scalar (A = 1/K, B = K,
AB == 1) forces an *anisotropic* effective stress (p_r = -p_t) and therefore
cannot satisfy G_{mu nu} = 8 pi T_{mu nu} for an isotropic perfect fluid.

This module replaces that single dynamic dielectric channel *inside sources*
with a genuine **two-function** static, spherically-symmetric metric

    ds^2 = -A(r) dt^2 + B(r) dr^2 + r^2 dOmega^2 ,     A, B independent,

i.e. the GR/TOV interior (areal radius r), plus the exact Schwarzschild
exterior.  In the dielectric the two legs are locked by AB == 1; here they are
free, which is exactly what the full-tensor source needs.

Two coordinate presentations are provided:

  * AREAL (Schwarzschild) coordinates --  TOV interior with
        B(r) = 1 / (1 - 2 m(r)/r),   A(r) = e^{2 nu(r)},
    nu integrated from dnu/dr = (m + 4 pi r^3 p)/(r(r - 2m)) and matched at the
    surface to the exterior A_ext = 1 - 2M/r (so A B -> 1 only in vacuum).

  * ISOTROPIC coordinates -- the closed-form exact-Schwarzschild legs
        A = ((1 - u/2)/(1 + u/2))^2 ,  B = (1 + u/2)^4 ,   u = GM/(r c^2),
    used to build the (A_field, B_field) backgrounds the F62/F64 dynamic
    wave-packet battery consumes (g_00 = -A, g_ii = B; c_eff = c0 sqrt(A/B)).
    Note AB = ((1-u/2)/(1+u/2))^2 (1+u/2)^4 = (1 - u^2/4)^2 (1+u/2)^2 != 1 --
    the two functions are genuinely independent, unlike the dielectric e^{2u}.

Self-contained: numpy + a local RK4 (no scipy; CLAUDE.md self-contained
numerics).  The sympy exactness checks live in the F181 test.

Date: 2026-06-30
"""

from __future__ import annotations

import numpy as np

MSUN_KM = 1.476625      # GM_sun/c^2 in km (geometric units G = c = 1)


# ======================================================================
# Equation of state (Gamma-law polytrope; swap in a tabulated EoS here)
# ======================================================================
class Polytrope:
    """p = K rho^Gamma, rho the total energy density (geometric units)."""

    def __init__(self, K, Gamma=2.0):
        self.K, self.Gamma = float(K), float(Gamma)

    def p_of_rho(self, rho):
        return self.K * np.maximum(rho, 0.0) ** self.Gamma

    def rho_of_p(self, p):
        return (np.maximum(p, 0.0) / self.K) ** (1.0 / self.Gamma)


# ======================================================================
# TOV right-hand side carrying BOTH metric functions (m -> B, nu -> A)
# ======================================================================
def _tov_two_function_rhs(r, m, p, nu, eos):
    """RHS for (m, p, nu).  m fixes the radial leg B = 1/(1 - 2m/r); nu fixes
    the time leg A = e^{2 nu}.  These are the two independent functions GR
    carries and the single scalar cannot (F173)."""
    rho = eos.rho_of_p(p)
    denom = r * (r - 2.0 * m)
    dm = 4.0 * np.pi * r**2 * rho
    dnu = (m + 4.0 * np.pi * r**3 * p) / denom
    dp = -(rho + p) * dnu                       # hydrostatic equilibrium
    return dm, dp, dnu


def integrate_interior(rho_c, eos, h=1e-3, rmax=400.0):
    """Integrate one star of central density rho_c carrying TWO metric
    functions.  Returns dict with radial profiles r, m, p, nu, lam and the
    matched metric legs A(r) = e^{2 nu}, B(r) = 1/(1 - 2m/r), plus exterior M.

    nu is integrated with nu(0) = 0 and then *shifted* so that at the surface
    e^{2 nu(R)} = 1 - 2M/R (continuity with the exact Schwarzschild exterior).
    The radial leg B is fixed pointwise by m(r); A and B are independent."""
    r, m, p, nu = 1e-6, 0.0, eos.p_of_rho(rho_c), 0.0
    p_floor = 1e-14 * p
    rs, ms, ps, nus = [r], [m], [p], [nu]
    while p > p_floor and r < rmax:
        k1 = _tov_two_function_rhs(r, m, p, nu, eos)
        k2 = _tov_two_function_rhs(r + h/2, m + h/2*k1[0], p + h/2*k1[1], nu + h/2*k1[2], eos)
        k3 = _tov_two_function_rhs(r + h/2, m + h/2*k2[0], p + h/2*k2[1], nu + h/2*k2[2], eos)
        k4 = _tov_two_function_rhs(r + h, m + h*k3[0], p + h*k3[1], nu + h*k3[2], eos)
        m_new = m + h/6*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
        p_new = p + h/6*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
        nu_new = nu + h/6*(k1[2] + 2*k2[2] + 2*k3[2] + k4[2])
        if p_new <= 0.0:                          # crossed the surface; refine
            frac = p / (p - p_new)
            r += frac * h
            m += frac * (m_new - m)
            nu += frac * (nu_new - nu)
            p = 0.0
            rs.append(r); ms.append(m); ps.append(0.0); nus.append(nu)
            break
        r, m, p, nu = r + h, m_new, p_new, nu_new
        rs.append(r); ms.append(m); ps.append(p); nus.append(nu)
    R, M = r, m
    rs = np.array(rs); ms = np.array(ms); ps = np.array(ps); nus = np.array(nus)
    # shift nu so the time leg is continuous with the exterior at the surface
    nu_shift = 0.5 * np.log(1.0 - 2.0 * M / R) - nus[-1]
    nus = nus + nu_shift
    A = np.exp(2.0 * nus)                          # time leg  (g_tt = -A)
    B = 1.0 / (1.0 - 2.0 * ms / rs)                # radial leg (g_rr =  B)
    lam = 0.5 * np.log(B)
    return {"r": rs, "m": ms, "p": ps, "nu": nus, "lam": lam,
            "A": A, "B": B, "R": R, "M": M,
            "z_surf": (1.0 - 2.0 * M / R) ** -0.5 - 1.0}


def metric_AB_areal(r, M, interior=None):
    """Two-function metric legs (A, B) at areal radius r.  In vacuum (r >= R)
    this is *exact Schwarzschild*: A = 1 - 2M/r, B = 1/(1 - 2M/r) (AB == 1 only
    here, in vacuum).  Inside, pass the integrate_interior() dict to interpolate
    the genuinely-independent interior legs."""
    r = np.asarray(r, dtype=float)
    A = 1.0 - 2.0 * M / r
    B = 1.0 / (1.0 - 2.0 * M / r)
    if interior is not None:
        ri = interior["r"]; mask = r < interior["R"]
        A = np.where(mask, np.interp(r, ri, interior["A"]), A)
        B = np.where(mask, np.interp(r, ri, interior["B"]), B)
    return A, B


# ======================================================================
# Isotropic exact-Schwarzschild field builder for the dynamic battery
# (two INDEPENDENT legs; g_00 = -A, g_ii = B, c_eff = c0 sqrt(A/B))
# ======================================================================
_U_MAX = 2.0 * (1.0 - 1e-9)     # just inside the isotropic-coordinate horizon


def schwarzschild_isotropic_field(shape, GM, c0, center=None, r_soft=3.0):
    """Build (A_field, B_field) for the exact isotropic-Schwarzschild metric on
    a 2D grid.  u = GM/(r c0^2); the two legs are independent:

        A = ((1 - u/2)/(1 + u/2))^2 ,     B = (1 + u/2)^4 .

    Reduces to the weak-field A = 1 - 2u, B = 1 + 2u at small u (so the F62/F64
    weak-field battery is reproduced), but is EXACT to all PN orders for one
    static source -- where the dielectric e^{2u} differs at O(u^2) and is
    horizon-free.  AB != 1 (the genuine two-function content)."""
    Lx, Ly = shape
    if center is None:
        center = (Lx / 2.0, Ly / 2.0)
    xs = np.arange(Lx); ys = np.arange(Ly)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    r = np.sqrt((X - center[0])**2 + (Y - center[1])**2 + r_soft**2)
    u = np.clip(GM / (r * c0**2), -np.inf, _U_MAX)
    half = u / 2.0
    A = ((1.0 - half) / (1.0 + half))**2
    B = (1.0 + half)**4
    return A, B


def c_eff_field(A, B, c0):
    """Kinetic-leg speed seen by a Dirac packet:  c_eff = c0 sqrt(A/B)."""
    return c0 * np.sqrt(np.abs(A) / np.abs(B))


def lapse(A):
    """Redshift / rest-leg factor sqrt(A) = sqrt(-g_tt)."""
    return np.sqrt(np.abs(A))


# ======================================================================
# Reference: the demoted single-scalar dielectric legs (AB == 1)
# ======================================================================
def dielectric_field(shape, GM, c0, center=None, r_soft=3.0):
    """The F64/F178-demoted single-scalar dielectric: A = e^{-2u}, B = e^{2u},
    AB == 1.  Provided for side-by-side comparison with the two-function legs
    in the battery; it agrees at O(u) but differs at O(u^2) and is horizon-free."""
    Lx, Ly = shape
    if center is None:
        center = (Lx / 2.0, Ly / 2.0)
    xs = np.arange(Lx); ys = np.arange(Ly)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    r = np.sqrt((X - center[0])**2 + (Y - center[1])**2 + r_soft**2)
    u = GM / (r * c0**2)
    A = np.exp(-2.0 * u)
    B = np.exp(2.0 * u)
    return A, B
