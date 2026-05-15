"""
ca_unified.py  —  Unified stepper coupling Higgs field Φ to Dirac fermion
===========================================================================
Implements the proposition in `ca-unified-proposition.md`:
  - Φ (complex scalar) is the Higgs field, with Mexican-hat self-potential.
  - Dirac mass is sourced by Φ via Yukawa coupling:  m_eff(x) = y · |Φ(x)|.
  - Local light speed is sourced by Φ via the metric coupling:
    c(x) = c_0 · (|Φ(x)| / v)^(-alpha)  (Phase F3 — left as an option).

The unified stepper composes:
  1. Half-step Φ evolution (velocity Verlet on the K-G + Mexican-hat).
  2. Full Dirac step using m_eff(x) from current Φ
     (and optionally variable c, via the variable-c stepper).
  3. Half-step Φ evolution.

When Φ = v constant, this reduces exactly to the existing Dirac CA with
mass yv.  When y = 0, Φ evolves freely with no fermion back-reaction.

This module exposes:
  - `unified_step` — one timestep of the coupled system.
  - `setup_vacuum` — produce Φ = v initial condition.
  - `setup_higgs_perturbation` — produce a Higgs wave packet.
  - `setup_symmetry_restored` — produce Φ = 0 initial condition (F4).
"""

import numpy as np
import ca_higgs as hg
import ca_dirac as dirac


# ══════════════════════════════════════════════════════════════════
#  State container
# ══════════════════════════════════════════════════════════════════

class UnifiedState:
    """All field values for the unified CA cell state."""
    __slots__ = ('Phi', 'Pi', 'eta_u', 'eta_d', 'chi_u', 'chi_d')

    def __init__(self, Phi, Pi, eta_u, eta_d, chi_u, chi_d):
        self.Phi   = Phi
        self.Pi    = Pi
        self.eta_u = eta_u
        self.eta_d = eta_d
        self.chi_u = chi_u
        self.chi_d = chi_d

    def copy(self):
        return UnifiedState(self.Phi.copy(), self.Pi.copy(),
                             self.eta_u.copy(), self.eta_d.copy(),
                             self.chi_u.copy(), self.chi_d.copy())


# ══════════════════════════════════════════════════════════════════
#  Initial conditions
# ══════════════════════════════════════════════════════════════════

def setup_vacuum(shape, mu2, lam, fermion='left', sigma=3.0,
                  fermion_center=None):
    """
    Φ = v everywhere, Π = 0.  Fermion field as a Gaussian wave packet
    (4-spinor) at the lattice center with the given chirality.
    """
    v = float(np.sqrt(mu2 / (2.0 * lam)))
    Phi = np.full(shape, v + 0.0j)
    Pi  = np.zeros(shape, dtype=complex)
    nu, nd, xu, xd = dirac.gaussian_dirac_2d(shape, center=fermion_center,
                                              sigma=sigma, chirality=fermion)
    return UnifiedState(Phi, Pi, nu, nd, xu, xd), v


def setup_higgs_perturbation(shape, mu2, lam, k_perturb=(1, 0),
                              amplitude=1e-3):
    """
    Φ = v + small radial perturbation A·cos(k·x).  Π = 0.
    No fermion population (zeros).  Used for F2 (Higgs dispersion).
    """
    v = float(np.sqrt(mu2 / (2.0 * lam)))
    Lx, Ly = shape
    xs = np.arange(Lx); ys = np.arange(Ly)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    kx = 2.0 * np.pi * k_perturb[0] / Lx
    ky = 2.0 * np.pi * k_perturb[1] / Ly
    Phi = (v + amplitude * np.cos(kx * X + ky * Y)).astype(complex)
    Pi  = np.zeros(shape, dtype=complex)
    z = np.zeros(shape, dtype=complex)
    return UnifiedState(Phi, Pi, z.copy(), z.copy(), z.copy(), z.copy()), v


def setup_symmetry_restored(shape, mu2_eff_positive, lam, fermion='left',
                              sigma=3.0):
    """
    Φ = 0 everywhere, Π = 0.  This is the vacuum of the high-temperature
    phase where the symmetry is restored — all coefficients in V positive.

    For this initial condition to be a fixed point, use a potential
    V_high(|Φ|²) = +mu2_pos·|Φ|² + λ|Φ|⁴ with positive μ².  Then Φ=0 is
    the unique minimum, and fermions are massless.

    For F4 testing.
    """
    Phi = np.zeros(shape, dtype=complex)
    Pi  = np.zeros(shape, dtype=complex)
    nu, nd, xu, xd = dirac.gaussian_dirac_2d(shape, sigma=sigma,
                                              chirality=fermion)
    return UnifiedState(Phi, Pi, nu, nd, xu, xd)


# ══════════════════════════════════════════════════════════════════
#  Unified step
# ══════════════════════════════════════════════════════════════════

def unified_step(state, mu2, lam, yukawa=1.0,
                  c=0.5, dt=1.0, dirac_dt=None, n_phi_sub=1,
                  symmetric_phase=False):
    """
    One timestep of the coupled Φ–Dirac CA.

    Composition (Strang-symmetric):
        Φ half-step  →  Dirac step (using m_eff from current Φ)  →  Φ half-step

    Parameters
    ----------
    state : UnifiedState
    mu2, lam : scalars defining the Mexican-hat V(|Φ|²) = -μ²|Φ|² + λ|Φ|⁴.
              For the symmetry-restored regime, pass mu2 < 0 (handled by
              caller's setup function).
    yukawa : Yukawa coupling y in m_eff(x) = y·|Φ(x)|.
    c, dt : Dirac kinetic speed and time step.
    dirac_dt : optional override (defaults to dt).
    n_phi_sub : sub-stepping for Φ evolution.
    symmetric_phase : if True, treat as symmetry-restored — use V_high
                      with positive μ².  In this case mu2 should be passed
                      as a positive value representing +μ².

    Returns
    -------
    state (modified in place; state is also returned for chaining).
    """
    if dirac_dt is None:
        dirac_dt = dt

    # Half-step Φ
    state.Phi, state.Pi = hg.kg_step_strang(
        state.Phi, state.Pi, mu2, lam, dt=dt * 0.5, n_sub=n_phi_sub)

    # Build m_eff(x) from current Φ
    m_eff = yukawa * np.abs(state.Phi)

    # Full Dirac step at variable mass
    state.eta_u, state.eta_d, state.chi_u, state.chi_d = \
        dirac.dirac_step_2d_varm_splitstep(
            state.eta_u, state.eta_d, state.chi_u, state.chi_d,
            m_field=m_eff, c=c, dt=dirac_dt)

    # Second half-step Φ
    state.Phi, state.Pi = hg.kg_step_strang(
        state.Phi, state.Pi, mu2, lam, dt=dt * 0.5, n_sub=n_phi_sub)

    return state


# ══════════════════════════════════════════════════════════════════
#  Norms
# ══════════════════════════════════════════════════════════════════

def fermion_norm(state):
    return float(np.sum(
        np.abs(state.eta_u)**2 + np.abs(state.eta_d)**2 +
        np.abs(state.chi_u)**2 + np.abs(state.chi_d)**2))


def chirality_imbalance(state):
    """ρ_η − ρ_χ summed over all cells, normalized to total fermion norm."""
    n_eta = float(np.sum(np.abs(state.eta_u)**2 + np.abs(state.eta_d)**2))
    n_chi = float(np.sum(np.abs(state.chi_u)**2 + np.abs(state.chi_d)**2))
    total = n_eta + n_chi
    return (n_eta - n_chi) / total if total > 0 else 0.0


def phi_norm(state):
    """∫|Φ|² — used for energy bookkeeping of Φ."""
    return float(np.sum(np.abs(state.Phi)**2))


def phi_energy(state, mu2, lam):
    """Klein-Gordon energy density integrated over the lattice."""
    kinetic = float(np.sum(np.abs(state.Pi)**2))
    grad_Phi = hg._laplacian_2d(state.Phi) * (-1)  # =  -∇²Φ in some sign convention
    # Energy: ∫ (|Π|² + |∇Φ|² + V(|Φ|²)) dx
    # Use FFT to get |∇Φ|² directly
    Lx, Ly = state.Phi.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    PhiK = np.fft.fft2(state.Phi)
    grad2 = float(np.sum((KX**2 + KY**2) * np.abs(PhiK)**2) / (Lx * Ly))
    abs2 = (state.Phi * np.conj(state.Phi)).real
    V = float(np.sum(-mu2 * abs2 + lam * abs2 * abs2))
    return kinetic + grad2 + V
