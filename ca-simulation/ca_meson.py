#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_meson.py
===========

P3 of docs/roadmaps/roadmap-matter-binding.md — the DYNAMICAL meson sector: the pion as the
q-qbar pseudoscalar Goldstone of chiral-symmetry breaking, its scalar chiral
partner (sigma), and a vector (rho) contrast.

This module makes the pion a *dynamical* q-qbar bound state by reusing two
already-validated engines:

  • F77 (`test_F77_njl_gap_rpa.py`) — the self-consistent NJL gap + RPA ladder.
    ONE coupling G both generates the constituent mass m_c (gap equation) and,
    summed in the q-qbar ladder, fixes the meson poles 1 - 2 G Pi_M(q^2) = 0.
    The pseudoscalar pole is the pion; the scalar pole is the sigma. This is
    the calibrated continuum theory (Lam=651.5 MeV, G Lam^2=2.10, m0=5.5 MeV
    reproduces measured m_c, f_pi, m_pi, <qbar q>).

  • F74 (`test_F74_bound_state_binding.py`) — the relative-coordinate two-body
    lattice solver (3D tight-binding + contact well; secular Koster-Slater root
    cross-checked against dense diagonalisation to machine precision). This is
    the engine that makes the bound state *real-space / dynamical* rather than
    a continuum pole only.

PHYSICS DELIVERED
-----------------
  1. Goldstone theorem:  in the chiral limit (m0 -> 0) the pion is massless
     because 1 - 2 G Pi_PS(0) = 0 is *identically* the gap equation. (exact)
  2. GMOR:  m_pi^2 f_pi^2 = -m0 <qbar q>_tot  (the explicit-breaking slope).
  3. The non-Goldstone chiral partner (sigma) sits at the 2 m_c threshold with
     the SAME single coupling and NO extra input — the rigorous "the pion is
     anomalously light" contrast (m_pi / m_sigma -> 0 in the chiral limit).
  4. Vector contrast (rho) via the KSRF relation m_rho^2 = 2 g_rhopipi^2 f_pi^2,
     tying the heavy vector to the *model output* f_pi (one external coupling
     g_rhopipi ~ 6, clearly flagged Tier-3).
  5. A real-space relative-coordinate bound-state demonstration (F74 engine),
     secular root vs dense diagonalisation to machine precision.

NUMERICS
--------
Everything here is REAL (Euclidean 3-momentum-cutoff loop integrals; real
symmetric lattice eigenproblem). No chiral/complex transforms, so the CLAUDE.md
numpy caveat does not bite. numpy only.

Author note: prefactors/normalisations are inherited verbatim from F77, which
was validated against the measured light-meson sector. Do not change them
without re-running the F77 validation block.
"""

from __future__ import annotations

import numpy as np

# Loop degeneracy: colour x flavour in the fermion bubble (SU(2) NJL, N_c=3).
N_C, N_F = 3, 2

# Canonical SU(2) NJL parameters (F77 fit; reproduces measured hadron data).
CANONICAL = dict(Lam=0.6515, GLam2=2.10, m0=0.0055)   # GeV


# ===========================================================================
#  NJL loop integrals (3-momentum cutoff Lambda).  Closed forms + quadrature.
#    I1(M)  = (1/2pi^2) \int_0^Lam p^2/E dp ,                E = sqrt(p^2+M^2)
#    K(q2,M)= (1/2pi^2) \int_0^Lam p^2/(E (4E^2 - q2)) dp    (real for q2<4M^2)
#    K(0,M) = (1/2pi^2) \int_0^Lam p^2/(4 E^3) dp
# ===========================================================================
def _E(p, M):
    return np.sqrt(p * p + M * M)


def I1_closed(M, Lam):
    """(1/4pi^2) [ Lam E_Lam - M^2 ln((Lam+E_Lam)/M) ]."""
    EL = np.sqrt(Lam * Lam + M * M)
    return (Lam * EL - M * M * np.log((Lam + EL) / M)) / (4.0 * np.pi ** 2)


def K0_closed(M, Lam):
    """K(0,M) = (1/8pi^2)[ ln((Lam+E_Lam)/M) - Lam/E_Lam ]."""
    EL = np.sqrt(Lam * Lam + M * M)
    return (np.log((Lam + EL) / M) - Lam / EL) / (8.0 * np.pi ** 2)


def K_quad(q2, M, Lam, n=200000):
    """Bubble K(q2,M) for q2 <= 4 M^2 by quadrature (drop the p=0 node)."""
    p = np.linspace(0.0, Lam, n + 1)[1:]
    Ep = _E(p, M)
    return np.trapezoid(p * p / (Ep * (4.0 * Ep * Ep - q2)), p) / (2.0 * np.pi ** 2)


# ===========================================================================
#  Gap equation  M = m0 + 4 G N_c N_f M I1(M)  and the critical coupling.
# ===========================================================================
def gap_solve(G, Lam, m0, M_init=0.3):
    """Damped fixed-point solution of the gap equation. Returns M (>= m0)."""
    M = max(M_init, m0 + 1e-9)
    for _ in range(2000):
        rhs = m0 + 4.0 * G * N_C * N_F * M * I1_closed(M, Lam)
        if abs(rhs - M) < 1e-14:
            return rhs
        M = 0.5 * M + 0.5 * rhs
    return M


def G_critical(Lam):
    """Chiral chi-SB onset:  G_c Lam^2 = pi^2/(N_c N_f) = pi^2/6."""
    return np.pi ** 2 / (N_C * N_F) / Lam ** 2


# ===========================================================================
#  Meson polarizations and pole finder.
#    Pi_PS(q2) = 2 N_c N_f [ I1(M) +  q2          K(q2,M) ]   (pseudoscalar/pi)
#    Pi_S (q2) = 2 N_c N_f [ I1(M) + (q2 - 4M^2)  K(q2,M) ]   (scalar/sigma)
#    pole: 1 - 2 G Pi_M(q2) = 0
# ===========================================================================
def Pi_PS(q2, M, Lam):
    return 2.0 * N_C * N_F * (I1_closed(M, Lam) + q2 * K_quad(q2, M, Lam))


def Pi_S(q2, M, Lam):
    return 2.0 * N_C * N_F * (I1_closed(M, Lam) + (q2 - 4.0 * M * M) * K_quad(q2, M, Lam))


def meson_pole(channel, M, G, Lam, q2max_frac=0.99999):
    """Root of 1 - 2 G Pi(q2) for q2 in [0, 4M^2).
    Returns (mass, q2, sub_threshold_bool)."""
    Pi = Pi_PS if channel == "PS" else Pi_S
    f = lambda q2: 1.0 - 2.0 * G * Pi(q2, M, Lam)
    lo, hi = 0.0, 4.0 * M * M * q2max_frac
    flo, fhi = f(lo), f(hi)
    if flo == 0.0:
        return 0.0, 0.0, True
    if flo * fhi > 0.0:
        # no sub-threshold sign change -> pole at/above 2M (resonance)
        return np.sqrt(4.0 * M * M), 4.0 * M * M, False
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0.0:
            hi = mid
        else:
            lo = mid
    q2 = 0.5 * (lo + hi)
    return np.sqrt(max(q2, 0.0)), q2, True


# ===========================================================================
#  Decay constant, condensate, GMOR.
# ===========================================================================
def f_pi(M, Lam):
    """f_pi^2 = 4 N_c M^2 K(0)."""
    return np.sqrt(4.0 * N_C * M * M * K0_closed(M, Lam))


def condensate_perflavour(M, Lam):
    """<qbar q>_f = -2 N_c M I1(M)  (negative)."""
    return -2.0 * N_C * M * I1_closed(M, Lam)


def gmor_residual(M, Lam, m0, m_pi):
    """Relative residual of GMOR:  m_pi^2 f_pi^2 = -m0 <qbar q>_tot."""
    fp = f_pi(M, Lam)
    qq_tot = 2.0 * condensate_perflavour(M, Lam)
    lhs = m_pi ** 2 * fp ** 2
    rhs = -m0 * qq_tot
    return abs(lhs - rhs) / abs(rhs), lhs, rhs


# ===========================================================================
#  Vector (rho) contrast via KSRF:  m_rho^2 = 2 g_rhopipi^2 f_pi^2.
#  Ties the heavy non-Goldstone vector to the MODEL OUTPUT f_pi; the only
#  external number is the empirical rho-pi-pi coupling g_rhopipi ~ 6.0.
#  Flagged Tier-3 (one external coupling) — used only for the light/heavy
#  contrast, never as a precision claim.
# ===========================================================================
def rho_mass_ksrf(M, Lam, g_rhopipi=6.0):
    fp = f_pi(M, Lam)
    return np.sqrt(2.0) * g_rhopipi * fp


# ===========================================================================
#  Real-space relative-coordinate q-qbar bound state (F74 engine).
#  Rest-frame two-body -> one-body in the relative coordinate on a 3D cubic
#  lattice; rank-1 contact well of depth g.  Secular Koster-Slater root and
#  dense diagonalisation must agree to machine precision.
#    eps(k) = 2 t sum_i (1 - cos k_i)  in [0, 12 t];  band bottom at 0.
#    secular:  1 = g <1/(eps+E_b)>_BZ   (E_b>0 binding energy)
# ===========================================================================
def watson_gc(t=1.0):
    """3D contact binding threshold g_c = 2t / W3 (Watson integral)."""
    WATSON3 = 0.5054620197
    return 2.0 * t / WATSON3


def _eps_grid_finite(L, t=1.0):
    kk = 2.0 * np.pi * np.arange(L) / L
    ck = np.cos(kk)
    S = ck[:, None, None] + ck[None, :, None] + ck[None, None, :]
    return (2.0 * t * (3.0 - S)).ravel()   # length L^3, contains a 0 at k=0


def relcoord_secular(g, L=12, t=1.0):
    """Binding energy E_b from the finite-grid secular root 1=(g/N)sum 1/(eps+E_b)."""
    eps_f = _eps_grid_finite(L, t)
    f = lambda Eb: g * np.mean(1.0 / (eps_f + Eb)) - 1.0
    lo, hi = 1e-9, 1e6
    if f(lo) <= 0.0:
        return 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def relcoord_dense(g, L=12, t=1.0):
    """Lowest eigenvalue E0 of the real-space relative Hamiltonian on L^3."""
    N = L ** 3

    def site(x, y, z):
        return (x % L) * L * L + (y % L) * L + (z % L)

    H = np.zeros((N, N))
    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = site(x, y, z)
                H[i, i] += 6.0 * t
                for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0),
                                   (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                    H[i, site(x + dx, y + dy, z + dz)] += -t
    H[site(0, 0, 0), site(0, 0, 0)] += -g
    return float(np.linalg.eigvalsh(H)[0])


# ===========================================================================
#  Convenience: full meson spectrum at one parameter point.
# ===========================================================================
def solve_meson_spectrum(Lam=None, GLam2=None, m0=None, g_rhopipi=6.0):
    """Return the dynamical meson spectrum at one NJL parameter point.

    Defaults to the canonical SU(2) fit (F77) that reproduces measured data.
    Returns a dict with m_c, m_pi, m_sigma, m_rho, f_pi, condensate, GMOR.
    """
    Lam = CANONICAL["Lam"] if Lam is None else Lam
    GLam2 = CANONICAL["GLam2"] if GLam2 is None else GLam2
    m0 = CANONICAL["m0"] if m0 is None else m0
    G = GLam2 / Lam ** 2

    M = gap_solve(G, Lam, m0)
    m_pi, q2pi, _ = meson_pole("PS", M, G, Lam)
    m_sig, q2s, sub_s = meson_pole("S", M, G, Lam)
    fp = f_pi(M, Lam)
    qq_f = condensate_perflavour(M, Lam)
    gmor_rel, gmor_l, gmor_r = gmor_residual(M, Lam, m0, m_pi)
    m_rho = rho_mass_ksrf(M, Lam, g_rhopipi)

    return {
        "params": {"Lam": Lam, "GLam2": GLam2, "m0": m0, "g_rhopipi": g_rhopipi},
        "m_c": M, "m_pi": m_pi, "m_sigma": m_sig, "m_rho": m_rho,
        "f_pi": fp, "condensate_perflavour": qq_f,
        "condensate_root": -(-qq_f) ** (1.0 / 3.0),
        "m_sigma_over_2mc": m_sig / (2.0 * M),
        "m_pi_over_m_rho": m_pi / m_rho,
        "sigma_sub_threshold": sub_s,
        "gmor_rel": gmor_rel, "gmor_lhs": gmor_l, "gmor_rhs": gmor_r,
    }


if __name__ == "__main__":
    s = solve_meson_spectrum()
    print("Dynamical meson spectrum (canonical SU(2) NJL fit):")
    for k in ("m_c", "m_pi", "m_sigma", "m_rho", "f_pi"):
        print(f"  {k:9s} = {s[k] * 1e3:8.1f} MeV")
    print(f"  m_sigma/2m_c = {s['m_sigma_over_2mc']:.4f}")
    print(f"  m_pi/m_rho   = {s['m_pi_over_m_rho']:.4f}")
    print(f"  GMOR rel res = {s['gmor_rel']:.3e}")
