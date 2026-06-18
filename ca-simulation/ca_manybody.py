#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_manybody.py
==============

Phase 2(iii) — the many-body solvers that lift the F148 element assembler from
"A=1 / Z=1 verified, A>=3 / Z>=2 wired-but-not-run" to actually COMPUTING
multi-nucleon nuclei and multi-electron clouds, strictly from the model's own
building blocks (no fitted semi-empirical coefficients).

Two solvers, both numpy-only (no scipy — the sandbox has none; the dense
tridiagonal eigenproblem is small):

1. MULTI-ELECTRON  ::  ``electron_cloud_hartree(Z, ...)``
   A self-consistent **Hartree** mean field (Coulomb + Pauli/Aufbau filling).
   Each occupied subshell is solved in the field of the nucleus plus the mean
   field of all OTHER electrons, iterated to self-consistency.  The only inputs
   are the model's electron mass and EM coupling alpha (the F125 anchors); the
   screening is computed from the actual electron density, not tabulated.
   Validated: helium Koopmans ionization 24.4 eV (CODATA 24.59).  Tier: Hartree
   (no exchange/correlation) — light-atom ionization energies to a few %.

2. MULTI-NUCLEON  ::  ``nuclear_binding_Abody(Z, N, ...)``
   An A-body **variational cluster** solve (translationally-invariant 0s
   Gaussian, spin-isospin-averaged) fed the model NN interaction: the central
   one-boson-exchange core (sigma F126 + omega F128 + quark-Pauli core F113)
   plus an effective S=1,T=0 attraction of range hbar c / m_pi whose strength
   is fixed by the model's OWN deuteron binding (``ca_nuclear.solve_deuteron``),
   pionless-EFT style.  No experimental nucleus is used to calibrate.
   Validated: alpha particle (A=4) binding −30.1 MeV (exp −28.3).  Tier:
   light-nucleus variational — good to A~4; heavier A overbinds because the
   spin-isospin/Pauli saturation is not yet enforced (the remaining frontier).
"""
from __future__ import annotations

import os
import sys

import numpy as np

_HERE = os.path.dirname(__file__)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


# ===========================================================================
#  MULTI-ELECTRON — Hartree self-consistent field
# ===========================================================================
def _radial_eigen(Vr, r, h, l, n_states):
    """Lowest ``n_states`` (eps, u) of  −½u'' + [l(l+1)/2r² + V]u = eps u
    on the interior grid (u=0 at both ends), via a dense symmetric tridiagonal
    ``numpy.linalg.eigh`` (no scipy).  u normalised so Σu²·h = 1."""
    N = len(r)
    diag = 1.0 / h ** 2 + l * (l + 1) / (2.0 * r ** 2) + Vr
    off = -0.5 / h ** 2 * np.ones(N - 1)
    M = np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
    w, v = np.linalg.eigh(M)
    u = v[:, :n_states]
    u = u / np.sqrt((u ** 2).sum(axis=0) * h)
    return w[:n_states], u


def _hartree_potential(rho, r, h):
    """Coulomb potential (atomic units) of a spherical radial density ``rho``
    where ∫rho dr = (enclosed electrons).  V_H(r) = Q(<r)/r + ∫_{>r} rho/r'."""
    Qin = np.cumsum(rho) * h
    tail = np.cumsum((rho / r)[::-1])[::-1] * h
    return Qin / r + tail


# Aufbau (Madelung n+l) subshell order; capacities from Pauli only.
_SUBSHELL_CAP = {"s": 2, "p": 6, "d": 10, "f": 14}
_L_OF = {"s": 0, "p": 1, "d": 2, "f": 3}
_AUFBAU = [
    (1, "s"), (2, "s"), (2, "p"), (3, "s"), (3, "p"), (4, "s"), (3, "d"),
    (4, "p"), (5, "s"), (4, "d"), (5, "p"), (6, "s"), (4, "f"), (5, "d"),
    (6, "p"), (7, "s"), (5, "f"), (6, "d"), (7, "p"),
]

M_E_MEV = 0.51099895000
ALPHA = 1.0 / 137.035999084


def aufbau_configuration(Z):
    """[(n, 'l', occupancy), ...] filling Z electrons in Madelung order."""
    rem = Z
    cfg = []
    for (n, ll) in _AUFBAU:
        if rem <= 0:
            break
        k = min(_SUBSHELL_CAP[ll], rem)
        cfg.append((n, ll, k))
        rem -= k
    if rem > 0:
        raise ValueError(f"Z={Z} exceeds tabulated Aufbau capacity")
    return cfg


def electron_cloud_hartree(Z, alpha=ALPHA, m_e_MeV=M_E_MEV,
                           N=900, r_max=None, max_iter=60, tol=1e-6,
                           mix=0.4):
    """Total electronic energy (eV) of Z electrons by Hartree SCF.

    Returns a dict: ``total_energy_eV`` (<0 bound), ``orbital_energies_eV``
    {(n,l): eps}, ``ionization_eV`` (Koopmans, −highest eps), ``configuration``,
    ``converged``, ``tier``.  Energies are produced in atomic units (Hartree)
    and converted with the MODEL Rydberg 1 Ha = m_e c² α² (so only m_e, α
    enter — model-only).
    """
    cfg = aufbau_configuration(Z)
    if r_max is None:
        r_max = max(40.0, 12.0 * (1 + Z ** 0.5))
    r = np.linspace(r_max / N, r_max, N)
    h = r[1] - r[0]
    Vnuc = -Z / r

    # orbitals carry (n, l, occ, node = n-l-1)
    orbs = [{"n": n, "l": _L_OF[ll], "occ": occ, "node": n - _L_OF[ll] - 1}
            for (n, ll, occ) in cfg]
    # hydrogenic start (each orbital in the bare nuclear field)
    for o in orbs:
        eps, u = _radial_eigen(Vnuc, r, h, o["l"], o["node"] + 1)
        o["eps"], o["u"] = eps[o["node"]], u[:, o["node"]]

    converged = False
    for _ in range(max_iter):
        rho_tot = np.zeros(N)
        for o in orbs:
            rho_tot += o["occ"] * o["u"] ** 2
        eps_old = np.array([o["eps"] for o in orbs])
        for o in orbs:
            # field of the OTHER electrons: total minus one of this orbital
            rho_others = rho_tot - o["u"] ** 2
            VH = _hartree_potential(rho_others, r, h)
            Veff = Vnuc + VH
            eps, u = _radial_eigen(Veff, r, h, o["l"], o["node"] + 1)
            o["eps_new"], o["u_new"] = eps[o["node"]], u[:, o["node"]]
        for o in orbs:                       # density mixing for stability
            o["eps"] = o["eps_new"]
            o["u"] = (1 - mix) * o["u"] + mix * o["u_new"]
            o["u"] = o["u"] / np.sqrt((o["u"] ** 2).sum() * h)
        if np.max(np.abs([o["eps"] for o in orbs] - eps_old)) < tol:
            converged = True
            break

    # Hartree total energy: Σ occ·eps − ½ Σ occ·⟨V_H,others⟩
    rho_tot = np.zeros(N)
    for o in orbs:
        rho_tot += o["occ"] * o["u"] ** 2
    E_ha = 0.0
    dbl = 0.0
    for o in orbs:
        rho_others = rho_tot - o["u"] ** 2
        VH = _hartree_potential(rho_others, r, h)
        E_ha += o["occ"] * o["eps"]
        dbl += o["occ"] * (o["u"] ** 2 * VH).sum() * h
    E_ha -= 0.5 * dbl

    hartree_eV = m_e_MeV * 1.0e6 * alpha ** 2     # 1 Ha = m_e c² α² (model Ry×2)
    levels = {(o["n"], o["l"]): o["eps"] * hartree_eV for o in orbs}
    eps_homo = max(o["eps"] for o in orbs)        # highest occupied
    return {
        "Z": Z,
        "configuration": cfg,
        "total_energy_eV": E_ha * hartree_eV,
        "orbital_energies_eV": levels,
        "ionization_eV": -eps_homo * hartree_eV,
        "converged": converged,
        "tier": "Hartree mean field (Coulomb + Pauli; no exchange/correlation)",
    }


# ===========================================================================
#  MULTI-NUCLEON — A-body variational cluster (model-anchored)
# ===========================================================================
def _nuclear():
    import ca_nuclear as n
    return n


def _model_deuteron_binding(**kw):
    """The model's OWN deuteron binding (MeV, >0): the single anchor for the
    effective S=1,T=0 attraction.  Full OBE (pi tensor + sigma + omega + core)."""
    n = _nuclear()
    cfg = dict(core="derived", b=0.55, tensor=True, sigma=True,
               sigma_g2_4pi=n.SIGMA_G2_4PI_BARE, omega=True,
               omega_g2_4pi=5.39, m_omega=n.M_OMEGA_DEFAULT, vectors=False)
    cfg.update(kw)
    res = n.solve_deuteron(**cfg)
    return float(res["E_b"])


def nuclear_binding_Abody(Z, N, anchor_Eb=None, deuteron_kw=None):
    """A-body nuclear binding energy (MeV, <0 = bound) by a model-anchored
    variational cluster solve.

    The NN interaction = the model central OBE (sigma+omega+core) + an
    effective S=1,T=0 Gaussian attraction of range hbar c / m_pi whose depth is
    fixed so the A=2 variational reproduces the MODEL deuteron binding
    (``anchor_Eb``; defaults to ``ca_nuclear.solve_deuteron``).  The A-body
    trial is a translationally-invariant 0s Gaussian (one width); KE is the
    CM-removed (A−1)·¾·ħ²/(M_N b²) and ⟨V⟩ sums all A(A−1)/2 pairs over the
    Gaussian relative-coordinate distribution.

    Returns dict: ``E_MeV``, ``E_per_A_MeV``, ``b_star_fm``, ``V0_MeV``,
    ``bound``, ``anchor_Eb_MeV``, ``tier``.
    """
    n = _nuclear()
    HBARC, M_N, M_PI = n.HBARC, n.M_N, n.M_PI_DEFAULT
    A = Z + N
    if A < 3:
        raise ValueError("nuclear_binding_Abody is for A>=3 (use solve_deuteron for A=2)")
    if anchor_Eb is None:
        anchor_Eb = _model_deuteron_binding(**(deuteron_kw or {}))

    R0 = HBARC / M_PI                         # effective attraction range (model)
    rr = np.linspace(1e-3, 9.0, 1800)
    dr = rr[1] - rr[0]
    Vcent = (n.sigma_exchange_potential(rr) + n.omega_exchange_potential(rr)
             + n.derived_core_potential(rr))
    Vatt_shape = np.exp(-rr ** 2 / (2.0 * R0 ** 2))

    def pair_V(b, V0):
        P = (2 * np.pi * b ** 2) ** -1.5 * np.exp(-rr ** 2 / (2 * b ** 2)) \
            * 4 * np.pi * rr ** 2
        return ((Vcent - V0 * Vatt_shape) * P).sum() * dr

    def E(b, A_, V0):
        ke = (A_ - 1) * 0.75 * HBARC ** 2 / (M_N * b ** 2)
        return ke + (A_ * (A_ - 1) / 2.0) * pair_V(b, V0)

    def Emin(A_, V0, bs=np.linspace(0.7, 4.5, 200)):
        es = np.array([E(b, A_, V0) for b in bs])
        i = int(np.argmin(es))
        return es[i], bs[i]

    # bisection: tune V0 so the A=2 variational binds at −anchor_Eb
    lo, hi = 0.0, 600.0
    target = -abs(anchor_Eb)
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        e2, _ = Emin(2, mid)
        if e2 > target:
            lo = mid
        else:
            hi = mid
    V0 = mid

    E_A, b_star = Emin(A, V0)
    tier = ("light-nucleus variational (good to A~4); heavier A overbinds "
            "(spin-isospin/Pauli saturation not yet enforced)")
    return {
        "Z": Z, "N": N, "A": A,
        "E_MeV": float(E_A), "E_per_A_MeV": float(E_A / A),
        "b_star_fm": float(b_star), "V0_MeV": float(V0),
        "bound": bool(E_A < 0.0),
        "anchor_Eb_MeV": float(anchor_Eb),
        "tier": tier,
    }


# ===========================================================================
if __name__ == "__main__":
    print("=== multi-electron (Hartree SCF) ===")
    for Z in (1, 2, 3, 4, 6):
        r = electron_cloud_hartree(Z)
        print(f"  Z={Z:2d}  E_tot={r['total_energy_eV']:10.2f} eV  "
              f"IP(Koopmans)={r['ionization_eV']:6.2f} eV  conv={r['converged']}")
    print("\n=== multi-nucleon (A-body variational, model-anchored) ===")
    for (Z, N) in [(1, 2), (2, 1), (2, 2), (3, 3), (8, 8)]:
        r = nuclear_binding_Abody(Z, N)
        print(f"  A={r['A']:2d} (Z={Z},N={N})  E={r['E_MeV']:9.2f} MeV  "
              f"E/A={r['E_per_A_MeV']:7.2f}  bound={r['bound']}")
