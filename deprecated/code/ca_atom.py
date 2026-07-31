# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_atom.py
# migrated   : 2026-07-30 - 16:06
# target     : src/casim/engine/particles/atom.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_atom.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_atom.py
==========

P5 of docs/roadmaps/roadmap-matter-binding.md — the ATOM: an electron (P0) bound to a nucleus
by the electromagnetic (U(1), F69 paired-spinor photon) channel.  Hydrogen first,
with positronium as the clean two-body de-risking check, and the relativistic
fine structure from the Dirac — not Schrödinger — kinetic operator.

WHAT THIS DELIVERS
------------------
  1. POSITRONIUM (two-body validation, run FIRST).  The electron+positron
     Coulomb problem reduces in the relative coordinate to a one-body Coulomb
     problem with reduced mass mu = m_e/2.  Same radial 1/r solver as hydrogen;
     every level is exactly HALF the m_e-reduced-mass hydrogen value
     (Ry scales linearly in mu).  This validates the two-body -> relative-
     coordinate reduction before the heavy proton is introduced.

  2. HYDROGEN, non-relativistic.  The attractive-1/r analogue of the F74 contact
     solver: the reduced radial Schrödinger equation
          -(1/2) u''(x) + [ l(l+1)/(2x^2) - 1/x ] u(x) = eps u(x)
     (x = r/a0, eps = E/(mu c^2 (Z alpha)^2)) solved by finite difference on a
     tridiagonal grid.  Eigenvalues eps_n = -1/(2 n^2)  ->  E_n = -Ry/n^2, the
     1/n^2 Rydberg series with the exact l-degeneracy of the Coulomb problem.

  3. ABSOLUTE SCALE (the headline number).  The physical Rydberg
          Ry = (1/2) mu c^2 (Z alpha)^2
     is built from the model's OWN electron mass (P0 / F120-F121) and the
     electromagnetic coupling alpha; hydrogen's ground state then comes out at
     -13.606 eV with NO further input.  (m_e is a model anchor; alpha is the EM
     coupling — the one empirical EM number, the P5 analogue of P4's g_A.)

  4. FINE STRUCTURE from the DIRAC kinetic operator.  The exact Dirac-Coulomb
     (Sommerfeld) spectrum
          E_{n,kappa} = m c^2 [ 1 + ( Z alpha / (n_r + gamma) )^2 ]^{-1/2},
          gamma = sqrt(kappa^2 - (Z alpha)^2),  n_r = n - |kappa|
     reproduces the gross -13.6/n^2 series AND splits levels of equal n but
     different j by O(alpha^2) relative to the binding (O(alpha^4) absolute) —
     the fine structure.  A hand-rolled numerical radial-Dirac integrator
     (RK4, inward+outward matching) reproduces the Sommerfeld eigenvalues, so
     the splitting is a genuine solve, not just the closed form.  In pure
     Dirac-Coulomb 2s_{1/2} and 2p_{1/2} are EXACTLY degenerate; the residual
     2s-2p Lamb shift is a beyond-Dirac QED effect (ties to the open QFT-4 item
     in first-gen-completeness.md §5.4).

NUMERICS
--------
The non-relativistic radial problem is a REAL symmetric tridiagonal eigenproblem.
The Dirac integrator is REAL (large/small radial components G,F), hand-rolled
RK4 — no chiral/complex transforms, so the CLAUDE.md numpy caveat does not bite.
numpy + scipy.linalg.eigh_tridiagonal only.
"""

from __future__ import annotations

import math
import numpy as np

try:
    from scipy.linalg import eigh_tridiagonal
except ImportError:                       # numpy-only fallback (no scipy)
    def eigh_tridiagonal(d, e, select="a", select_range=None):
        """Drop-in for ``scipy.linalg.eigh_tridiagonal`` (subset of the API
        used here): symmetric tridiagonal eigenproblem via a dense
        ``numpy.linalg.eigh``.  Honours ``select='i'`` index ranges.  Exact to
        the same floor for the modest N this module uses; slower at very large
        N (dense), which is acceptable for the sandbox fallback."""
        d = np.asarray(d, float)
        e = np.asarray(e, float)
        M = np.diag(d) + np.diag(e, 1) + np.diag(e, -1)
        w, v = np.linalg.eigh(M)
        if select == "i" and select_range is not None:
            lo, hi = int(select_range[0]), int(select_range[1])
            return w[lo:hi + 1], v[:, lo:hi + 1]
        return w, v


# ===========================================================================
#  Physical constants (CODATA 2018).  m_e is the model's P0/F120-F121 anchor;
#  alpha is the electromagnetic coupling (the one empirical EM input).
# ===========================================================================
M_E_MEV = 0.51099895000        # electron rest energy  m_e c^2  (MeV)
M_P_MEV = 938.27208816         # proton  rest energy   m_p c^2  (MeV)
HBARC_EVNM = 197.3269804       # hbar c  (eV·nm)   -> handy for lengths in nm
ALPHA = 1.0 / 137.035999084    # fine-structure constant (EM coupling)
RY_EV_CODATA = 13.605693122994 # Rydberg energy (eV) — infinite-nucleus, CODATA


def reduced_mass_MeV(m1_MeV, m2_MeV):
    """Two-body reduced mass mu = m1 m2 / (m1 + m2) in MeV."""
    return m1_MeV * m2_MeV / (m1_MeV + m2_MeV)


def rydberg_eV(mu_MeV, Z=1, alpha=ALPHA):
    """Physical Rydberg  Ry = (1/2) mu c^2 (Z alpha)^2  in eV.
    mu_MeV is the reduced mass (rest energy) in MeV."""
    return 0.5 * (mu_MeV * 1.0e6) * (Z * alpha) ** 2


def bohr_radius_nm(mu_MeV, Z=1, alpha=ALPHA):
    """Bohr radius a0 = hbar c / (mu c^2 Z alpha) in nm."""
    return HBARC_EVNM / (mu_MeV * 1.0e6 * Z * alpha)


# ===========================================================================
#  1./2.  Non-relativistic radial Coulomb solver (the F74 1/r analogue).
#  Dimensionless reduced radial equation in Bohr-radius units x = r/a0:
#        H u = eps u ,   H = -(1/2) d^2/dx^2 + l(l+1)/(2 x^2) - 1/x
#  exact spectrum eps_n = -1/(2 n^2)  ->  E_n[Ry] = 2 eps_n = -1/n^2.
#  Tridiagonal finite difference; u(0)=u(x_max)=0.
# ===========================================================================
def radial_coulomb_levels(l, n_levels=4, x_max=None, N=6000):
    """Lowest `n_levels` eigen-energies (in RYDBERG units, so the exact answer
    is -1/n^2) of the dimensionless hydrogenic radial equation for orbital l.

    Returns (energies_Ry, x_grid, wavefns) where wavefns[:,k] is the reduced
    radial function u_k(x)=x R(x) on x_grid, normalised to sum |u|^2 dx = 1.
    """
    if x_max is None:
        # cover up to n ~ l+n_levels: <r> ~ n^2; pad generously.
        n_top = l + n_levels
        x_max = max(60.0, 6.0 * n_top * n_top)
    h = x_max / (N + 1)
    i = np.arange(1, N + 1)
    x = i * h                                   # interior nodes (u=0 at 0 and x_max)
    diag = 1.0 / h ** 2 + l * (l + 1) / (2.0 * x ** 2) - 1.0 / x
    off = -0.5 / h ** 2 * np.ones(N - 1)
    eps, vecs = eigh_tridiagonal(diag, off, select="i",
                                 select_range=(0, n_levels - 1))
    E_Ry = 2.0 * eps                            # E[Ry] = 2 eps
    # normalise the reduced radial functions
    norm = np.sqrt((vecs ** 2).sum(axis=0) * h)
    u = vecs / norm
    return E_Ry, x, u


def hydrogen_spectrum(n_max=5, mu_MeV=None, Z=1, alpha=ALPHA, N=6000):
    """Absolute hydrogen(-like) spectrum E_{n,l} in eV.

    mu_MeV defaults to the e-p reduced mass.  Returns a dict:
       'Ry_eV', 'a0_nm', and 'levels' = {(n,l): E_eV}.
    The dimensionless solver supplies E[Ry]=-1/n^2 (+grid error); the absolute
    eV comes from Ry = (1/2) mu c^2 (Z alpha)^2.
    """
    if mu_MeV is None:
        mu_MeV = reduced_mass_MeV(M_E_MEV, M_P_MEV)
    Ry = rydberg_eV(mu_MeV, Z, alpha)
    levels = {}
    raw = {}
    for l in range(0, n_max):
        nlev = n_max - l                        # principal n = l+1, ..., n_max
        E_Ry, _, _ = radial_coulomb_levels(l, n_levels=nlev, N=N)
        for k in range(nlev):
            n = l + 1 + k
            raw[(n, l)] = E_Ry[k]               # in Ry units (≈ -1/n^2)
            levels[(n, l)] = E_Ry[k] * Ry       # eV
    return {"Ry_eV": Ry, "a0_nm": bohr_radius_nm(mu_MeV, Z, alpha),
            "mu_MeV": mu_MeV, "levels": levels, "levels_Ry": raw}


# ===========================================================================
#  4.  Dirac-Coulomb fine structure.
#  kappa(j,l):  kappa = -(l+1) for j=l+1/2 ;  kappa = +l for j=l-1/2.
#  Sommerfeld:  E/mc^2 = [1 + (Za/(n_r+gamma))^2]^{-1/2}, gamma=sqrt(k^2-(Za)^2).
# ===========================================================================
def kappa_of(l, j_is_l_plus_half):
    return -(l + 1) if j_is_l_plus_half else l


def sommerfeld_energy(n, kappa, Z=1, alpha=ALPHA):
    """Exact Dirac-Coulomb total energy in units of m c^2 (includes rest mass)."""
    Za = Z * alpha
    gamma = math.sqrt(kappa * kappa - Za * Za)
    n_r = n - abs(kappa)
    return (1.0 + (Za / (n_r + gamma)) ** 2) ** (-0.5)


def sommerfeld_binding_eV(n, kappa, mc2_MeV=M_E_MEV, Z=1, alpha=ALPHA):
    """Dirac-Coulomb binding energy (E - mc^2) in eV (negative for bound)."""
    return (sommerfeld_energy(n, kappa, Z, alpha) - 1.0) * mc2_MeV * 1.0e6


def fine_structure_series_eV(n, j, mc2_MeV=M_E_MEV, Z=1, alpha=ALPHA):
    """The standard expansion of the Dirac binding to O((Za)^4):
        E_b ≈ -(1/2) mc^2 (Za)^2/n^2 * [ 1 + (Za)^2/n^2 ( n/(j+1/2) - 3/4 ) ].
    Returns (leading_eV, fine_correction_eV)."""
    Za = Z * alpha
    mc2 = mc2_MeV * 1.0e6
    lead = -0.5 * mc2 * Za ** 2 / n ** 2
    corr = lead * (Za ** 2 / n ** 2) * (n / (j + 0.5) - 0.75)
    return lead, corr


# ---------------------------------------------------------------------------
#  Numerical radial-Dirac eigenvalue by inward+outward RK4 matching.
#  Units: hbar=c=m_e=1; lengths in Compton wavelengths, energies in m_e c^2.
#  V(r) = -Z alpha / r.
#    G' = -(kappa/r) G + (E - V + 1) F
#    F' =  (kappa/r) F - (E - V - 1) G          (G large, F small component)
# ---------------------------------------------------------------------------
def _dirac_rhs(r, G, F, kappa, E, Za):
    V = -Za / r
    dG = -(kappa / r) * G + (E - V + 1.0) * F
    dF = (kappa / r) * F - (E - V - 1.0) * G
    return dG, dF


def _rk4_segment(r0, r1, G, F, kappa, E, Za, nsteps):
    h = (r1 - r0) / nsteps
    r = r0
    for _ in range(nsteps):
        k1G, k1F = _dirac_rhs(r, G, F, kappa, E, Za)
        k2G, k2F = _dirac_rhs(r + 0.5 * h, G + 0.5 * h * k1G, F + 0.5 * h * k1F, kappa, E, Za)
        k3G, k3F = _dirac_rhs(r + 0.5 * h, G + 0.5 * h * k2G, F + 0.5 * h * k2F, kappa, E, Za)
        k4G, k4F = _dirac_rhs(r + h, G + h * k3G, F + h * k3F, kappa, E, Za)
        G += (h / 6.0) * (k1G + 2 * k2G + 2 * k3G + k4G)
        F += (h / 6.0) * (k1F + 2 * k2F + 2 * k3F + k4F)
        r += h
    return G, F


def _dirac_mismatch(E, n, kappa, Za, r0, r_m, r_max, nout, nin):
    """Wronskian-style mismatch G_out F_in - F_out G_in at the matching radius
    r_m; zero at an eigenvalue.  Outward from r0 (series IC), inward from r_max
    (decaying IC)."""
    gamma = math.sqrt(kappa * kappa - Za * Za)
    # outward IC at r0 (pointlike-Coulomb small-r behaviour ~ r^gamma)
    G0 = r0 ** gamma
    F0 = (gamma + kappa) / Za * r0 ** gamma
    G_out, F_out = _rk4_segment(r0, r_m, G0, F0, kappa, E, Za, nout)
    # inward IC at r_max (decaying tail ratio F/G = -lambda/(E+1))
    lam = math.sqrt(max(1.0 - E * E, 1e-30))
    G1 = 1.0
    F1 = -lam / (E + 1.0)
    G_in, F_in = _rk4_segment(r_max, r_m, G1, F1, kappa, E, Za, nin)
    # normalise magnitudes to avoid overflow dominating the sign
    sc_out = max(abs(G_out), abs(F_out), 1e-300)
    sc_in = max(abs(G_in), abs(F_in), 1e-300)
    G_out, F_out = G_out / sc_out, F_out / sc_out
    G_in, F_in = G_in / sc_in, F_in / sc_in
    return G_out * F_in - F_out * G_in


def numerical_dirac_energy(n, kappa, Z=1, alpha=ALPHA, window=2.0e-7,
                           r0=1e-5, nout=20000, nin=20000):
    """Bisect the radial-Dirac mismatch around the Sommerfeld value to recover
    the eigenvalue numerically (units m c^2).  `window` is the relative bracket
    half-width around Sommerfeld.  Returns the bisected E."""
    Za = Z * alpha
    E_som = sommerfeld_energy(n, kappa, Z, alpha)
    # length scales: bound orbit ~ n^2/(Za) Compton; tail decay length n/(Za).
    a_bohr = 1.0 / Za
    r_m = max(2.0, n * n * a_bohr)
    r_max = r_m + 9.0 * n * a_bohr            # ~9 decay lengths beyond the orbit
    lo = E_som * (1.0 - window)
    hi = E_som * (1.0 + window)
    flo = _dirac_mismatch(lo, n, kappa, Za, r0, r_m, r_max, nout, nin)
    fhi = _dirac_mismatch(hi, n, kappa, Za, r0, r_m, r_max, nout, nin)
    if flo == 0.0:
        return lo
    if flo * fhi > 0.0:
        # bracket failed — widen once
        lo = E_som * (1.0 - 10 * window)
        hi = E_som * (1.0 + 10 * window)
        flo = _dirac_mismatch(lo, n, kappa, Za, r0, r_m, r_max, nout, nin)
        fhi = _dirac_mismatch(hi, n, kappa, Za, r0, r_m, r_max, nout, nin)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fm = _dirac_mismatch(mid, n, kappa, Za, r0, r_m, r_max, nout, nin)
        if flo * fm <= 0.0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


# ===========================================================================
#  Convenience: a full hydrogen registry used by the test.
# ===========================================================================
def hydrogen_registry(alpha=ALPHA, N=6000):
    mu_H = reduced_mass_MeV(M_E_MEV, M_P_MEV)
    mu_Ps = M_E_MEV / 2.0
    spec_H = hydrogen_spectrum(n_max=5, mu_MeV=mu_H, alpha=alpha, N=N)
    spec_Ps = hydrogen_spectrum(n_max=3, mu_MeV=mu_Ps, alpha=alpha, N=N)
    return {"alpha": alpha, "mu_H_MeV": mu_H, "mu_Ps_MeV": mu_Ps,
            "hydrogen": spec_H, "positronium": spec_Ps}


if __name__ == "__main__":
    print("=== P5 atom: hydrogen + positronium + Dirac fine structure ===\n")
    reg = hydrogen_registry()
    H = reg["hydrogen"]
    print(f"Ry(H) = {H['Ry_eV']:.6f} eV   a0 = {H['a0_nm']:.6f} nm")
    print("Hydrogen Rydberg series (E_n,l in eV):")
    for (n, l), E in sorted(H["levels"].items()):
        orb = "spdfg"[l]
        print(f"   {n}{orb}: {E:10.5f} eV   (E[Ry]={H['levels_Ry'][(n,l)]:+.6f}, -1/n^2={-1.0/n**2:+.6f})")

    Ps = reg["positronium"]
    print(f"\nPositronium: Ry(Ps) = {Ps['Ry_eV']:.6f} eV  (= Ry(H_infty)/2),  ground "
          f"{Ps['levels'][(1,0)]:.5f} eV")

    print("\nDirac-Coulomb fine structure (binding, eV):")
    for (n, l, jh, lbl) in [(1, 0, True, "1s_1/2"), (2, 0, True, "2s_1/2"),
                            (2, 1, False, "2p_1/2"), (2, 1, True, "2p_3/2")]:
        kap = kappa_of(l, jh)
        eb = sommerfeld_binding_eV(n, kap)
        print(f"   {lbl:8s} kappa={kap:+d}  E_b = {eb:.9f} eV")
    d_split = (sommerfeld_binding_eV(2, kappa_of(1, True))
               - sommerfeld_binding_eV(2, kappa_of(1, False)))
    print(f"   2p_3/2 - 2p_1/2 splitting = {d_split*1e6:.4f} ueV "
          f"({d_split/4.135667696e-15/1e9:.4f} GHz)")

    print("\nNumerical radial-Dirac vs Sommerfeld (units m_e c^2):")
    for (n, kap, lbl) in [(1, -1, "1s_1/2"), (2, +1, "2p_1/2"), (2, -2, "2p_3/2")]:
        Enum = numerical_dirac_energy(n, kap)
        Esom = sommerfeld_energy(n, kap)
        print(f"   {lbl:8s}  num={Enum:.12f}  som={Esom:.12f}  rel={abs(Enum-Esom)/abs(1-Esom):.2e}")
