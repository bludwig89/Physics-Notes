"""
ca_baryon_blockspin.py — the coarse-grained baryon element (F140)
=================================================================

`2026-06-11`

F132 handled the baryon under the block-spin RG by *ingredient covariance* — its
mass is the F130-C1-covariant string scale ($E_\\text{rel}\\propto\\sigma^{2/3}$),
because the F122 three-body solver is an explicitly-correlated-Gaussian (ECG)
basis, not a lattice that can be block-spun directly.  F140 supplies the missing
piece: a genuine **lattice baryon element** that *can* be coarse-grained.

The reduction
-------------
The rest-frame three-equal-mass-quark problem is 6-D (mass-normalised Jacobi
coordinates $\\xi_1,\\xi_2$; F122).  Project onto the **hyperradius**
$\\rho^2=\\xi_1^2+\\xi_2^2$ in the lowest ($K=0$) hyperspherical channel — the
symmetric S-state that dominates the confined ground state.  The 6-D Laplacian
reduces to a 1-D radial equation in $\\rho$ for the reduced amplitude
$u(\\rho)=\\rho^{5/2}R(\\rho)$:

    -1/(2m) u'' + [1/(2m)] (15/4)/ρ² u + V_eff(ρ) u = E u,    u(0)=u(∞)=0,

with the $K=0$ grand-orbital centrifugal $15/4 = (d-1)(d-3)/4$ at $d=6$.  The
pairwise Cornell confinement averages over the hypersphere to a LINEAR effective
potential (the OGE $1/r$ has a divergent $K=0$ hyperangular average — it couples
high-$K$ channels — so the confinement-dominated baryon, F122, is the clean case):

    V_eff(ρ) = C_σ · σ · ρ,   C_σ = 3·√2·⟨|u|⟩_{S⁵} = 3√2·16/(15π) = 16√2/(5π),

the three pairs × the pair length $\\sqrt2\\rho|\\hat n\\!\\cdot\\!\\hat e|$ averaged over
the unit 5-sphere (⟨|u|⟩ = 16/15π).

Calibration
-----------
The fixed-$K{=}0$ channel captures the confinement SCALING exactly
($E\\propto\\sigma^{2/3}$, slope $2/3$) but only $\\sim63\\%$ of the full ECG energy
(the higher-$K$ channels are the rest — the adiabatic gap).  A single,
$\\sigma$-independent effective coefficient $C_\\text{eff}=\\kappa\\,C_\\sigma$ matched
once to the ECG ($\\kappa\\approx2.0$) makes the element reproduce the F122 baryon
across the whole $\\sigma$ range to $<0.1\\%$ — an EFT-style matching, not a per-point
fit.

Coarse-graining (the F140 payoff)
---------------------------------
The element is a 1-D lattice, so $R_b$ is grid decimation ($h\\to b\\,h$).  At fixed
physical $C_\\text{eff}$ the smooth linear potential block-averages and the baryon
mass + rms hyperradius are reproduced with the irrelevant $O(h^2)$ error (like the
F132 deuteron).  In *lattice* units the confining $\\sigma$ is instead the relevant
operator $\\hat\\sigma\\to b\\hat\\sigma$ (F130-C1) — the same physical mass either way.

Real-symmetric tridiagonal Hamiltonian — numpy/scipy safe (no chiral transform).
Wraps `ca_baryon_dynamics` (ECG) read-only for the calibration/validation.
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

# Hyperangular constants (closed form on the unit 5-sphere, d=6):
#   ⟨|u|⟩ = (1/5)/(3π/16) = 16/(15π);  C_σ = 3·√2·⟨|u|⟩ = 16√2/(5π).
PROJ_ABS_6 = 16.0 / (15.0 * np.pi)           # ⟨|n̂·ê|⟩ on S⁵
HYPER_C0 = 3.0 * np.sqrt(2.0) * PROJ_ABS_6   # geometric K=0 confinement coeff
CENTRIFUGAL_K0 = 15.0 / 4.0                  # (d-1)(d-3)/4 at d=6, K=0

#: adiabatic-channel calibration κ (C_eff = κ·C_σ), matched once to the ECG
#: baryon at σ=1, m=1, α_s=0 (σ-independent — see module docstring).  ≈ 2.0.
BARYON_ADIABATIC_CAL = 2.0006

__all__ = [
    "PROJ_ABS_6", "HYPER_C0", "CENTRIFUGAL_K0", "BARYON_ADIABATIC_CAL",
    "hyperradial_baryon", "calibrate_to_ecg", "baryon_confinement_scaling",
    "baryon_coarse_grain", "confinement_relevant_flow",
]


# ----------------------------------------------------------------------
# The 1-D hyperradial baryon element
# ----------------------------------------------------------------------
def hyperradial_baryon(sigma, m=1.0, N=1200, Rmax=25.0, calibrated=True,
                       alpha_s=0.0):
    """Lowest hyperradial (K=0) eigenstate of the confined three-quark baryon.

    Returns dict with E_rel (relative-coordinate ground energy = baryon mass −
    3m), the reduced amplitude u(ρ) and grid ρ, and the rms hyperradius.  With
    ``calibrated=True`` the effective confinement is κ·C_σ (matched to the ECG);
    ``alpha_s`` adds an optional (regularised) hyperangular OGE term — off by
    default (the K=0 average of 1/r is channel-mixing; the baryon is
    confinement-dominated)."""
    h = Rmax / (N + 1)
    r = h * np.arange(1, N + 1)
    Csig = HYPER_C0 * (BARYON_ADIABATIC_CAL if calibrated else 1.0)
    D2 = sp.diags([-1.0 / h ** 2 * np.ones(N - 1),
                   2.0 / h ** 2 * np.ones(N),
                   -1.0 / h ** 2 * np.ones(N - 1)], [-1, 0, 1])
    cent = (1.0 / (2.0 * m)) * CENTRIFUGAL_K0 / r ** 2
    V = Csig * sigma * r
    if alpha_s:
        # softened hyperradial OGE (regularised; subdominant)
        V = V - (2.0 * alpha_s / 3.0) * 3.0 / np.sqrt(r ** 2 + h ** 2)
    H = (1.0 / (2.0 * m)) * D2 + sp.diags(cent + V)
    w, v = eigsh(H.tocsc(), k=1, which="SA")
    u = v[:, 0]
    rms = float(np.sqrt(np.sum(u ** 2 * r ** 2) / np.sum(u ** 2)))
    return {"E_rel": float(w[0]), "rho": r, "u": u, "rms_rho": rms,
            "h": h, "N": N, "sigma": sigma, "m": m}


def calibrate_to_ecg(sigma=1.0, m=1.0, N=1500):
    """Return the adiabatic calibration κ = (E_ECG/E_{K=0})^{3/2} matched at one
    (σ,m) to the F122 ECG (σ-independent because both scale as σ^{2/3})."""
    import ca_baryon_dynamics as _bd
    E_k0 = hyperradial_baryon(sigma, m, N=N, calibrated=False)["E_rel"]
    E_ecg = _bd.ground_state_relative_energy(m=m, sigma=sigma,
                                             alpha_s=0.0)["E_rel_cholesky"]
    return float((E_ecg / E_k0) ** 1.5)


def baryon_confinement_scaling(sigmas, m=1.0, N=1200):
    """Log-log slope of E_rel(σ) for the hyperradial element — the linear-
    potential virial 2/3 (the string scale, RG-covariant via F130-C1)."""
    E = np.array([hyperradial_baryon(s, m, N=N)["E_rel"] for s in sigmas])
    return E, float(np.polyfit(np.log(sigmas), np.log(E), 1)[0])


# ----------------------------------------------------------------------
# Coarse-graining the element (R_b = hyperradial grid decimation)
# ----------------------------------------------------------------------
def _block_average_1d(arr, b):
    a = np.asarray(arr, dtype=np.float64)
    n = (len(a) // b) * b
    return a[:n].reshape(-1, b).mean(axis=1)


def baryon_coarse_grain(N_fine, b, sigma=1.0, m=1.0, Rmax=25.0):
    """Coarse-grain the baryon element by R_b (decimate the hyperradial grid by
    b, h→b·h), at fixed physical C_eff.  Returns fine/coarse E_rel, rms and their
    relative errors, plus the block-averaged-fine ↔ coarse amplitude overlap —
    the baryon mass reproduced on b× fewer cells (irrelevant O(h²))."""
    rf = hyperradial_baryon(sigma, m, N=N_fine, Rmax=Rmax)
    rc = hyperradial_baryon(sigma, m, N=N_fine // b, Rmax=Rmax)
    rel = lambda a, c: abs(c - a) / max(abs(a), 1e-30)
    uf_b = _block_average_1d(np.abs(rf["u"]), b)
    uc = np.abs(rc["u"])
    n = min(len(uf_b), len(uc))
    overlap = float(abs(uf_b[:n] @ uc[:n])
                    / (np.linalg.norm(uf_b[:n]) * np.linalg.norm(uc[:n])))
    return {
        "E_rel_fine": rf["E_rel"], "E_rel_coarse": rc["E_rel"],
        "E_rel_rel_err": rel(rf["E_rel"], rc["E_rel"]),
        "rms_fine": rf["rms_rho"], "rms_coarse": rc["rms_rho"],
        "rms_rel_err": rel(rf["rms_rho"], rc["rms_rho"]),
        "overlap": overlap, "h_fine": rf["h"], "h_coarse": rc["h"],
        "N_fine": N_fine, "N_coarse": N_fine // b,
    }


def confinement_relevant_flow(b):
    """The C1 tie: in lattice units the confining coupling is the RELEVANT
    operator σ̂→b·σ̂ (eigenvalue b>1, F130-C1), so the physical baryon mass —
    a function of the physical string scale — is invariant under R_b.  Returns
    the eigenvalue (= b)."""
    return float(b)
