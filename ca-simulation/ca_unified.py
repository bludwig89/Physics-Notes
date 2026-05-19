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
                  dt=1.0, dirac_dt=None, n_phi_sub=1,
                  symmetric_phase=False, back_react=False,
                  phase=None):
    """
    One timestep of the coupled Φ–Dirac CA.

    Composition (Strang-symmetric):

        back_react=False (default):
            Φ-free(dt/2)  →  Dirac(dt)  →  Φ-free(dt/2)
            Φ feels its own potential only; fermion feels Φ as a mass
            field via Yukawa.  Vacuum is a fixed point.  Tests F1, F2, F4.

        back_react=True (P1, 2026-05-15):
            Φ-free(dt/2)  →  Yukawa-kick(dt/2)  →  Dirac(dt)
                          →  Yukawa-kick(dt/2)  →  Φ-free(dt/2)
            Adds the symplectic Yukawa source -y·χ†η to Π on either side
            of the Dirac step.  Derived from the joint Hamiltonian
            H = H_KG + H_Dirac_kin + H_Y where H_Y = y·(Φ·η†χ + Φ*·χ†η)
            (Standard-Model Yukawa coupling).  Under this composition
            (Φ, Π, Ψ) are simultaneously canonical variables of a single
            Hamiltonian and total energy is bounded to O(dt²) drift.
            Tests F3 (back-reaction).

    Parameters
    ----------
    state : UnifiedState
    mu2, lam : Mexican-hat V(|Φ|²) = -μ²|Φ|² + λ|Φ|⁴ parameters.
    yukawa : Yukawa coupling y in M(x) = y·Φ(x).
    dt : Time step (shared by Φ and Dirac sub-steps unless `dirac_dt`
        overrides).  The Dirac stepper no longer takes a `c` argument
        — the exact-QCA admissibility constraint  n² + m² = 1  fixes
        n = √(1 − m²) from the mass alone (Finding 9, 2026-05-17).
    dirac_dt : optional override (defaults to dt).
    n_phi_sub : sub-stepping for the Φ-free step.
    symmetric_phase : DEPRECATED.  Use `phase='symmetric'` instead.  Kept
        for backward compatibility — if True and `phase` is not given,
        it is mapped to phase='symmetric'.
    phase : {'broken', 'symmetric', None}.  Selects the Higgs vacuum:
        'broken'    → V = -μ²|Φ|² + λ|Φ|⁴, mu2 ≥ 0, vacuum at |Φ|=v.
        'symmetric' → V = +μ²|Φ|² + λ|Φ|⁴, mu2 ≥ 0, vacuum at Φ=0.
        If None, falls back to legacy behaviour (sign of `mu2` decides).
    back_react : if True, apply symplectic Yukawa back-reaction.  See above.

    Returns
    -------
    state (modified in place; state is also returned for chaining).
    """
    if dirac_dt is None:
        dirac_dt = dt

    # Resolve phase selection.  Explicit `phase` wins; otherwise honour
    # the legacy `symmetric_phase` bool; otherwise leave it to mu2's sign.
    if phase is None:
        phase_resolved = 'symmetric' if symmetric_phase else 'broken'
    else:
        phase_resolved = phase
    # If the caller passed a negative mu2 (legacy F4 convention) while
    # also selecting phase='broken', treat that as the same symmetric-
    # phase result the old code produced.  This keeps F4 working before
    # it migrates to the explicit API.
    mu2_abs = abs(mu2)
    if mu2 < 0 and phase_resolved == 'broken' and phase is None:
        phase_resolved = 'symmetric'

    # Half-step Φ-free (Strang first half of H_KG)
    state.Phi, state.Pi = hg.kg_step_strang(
        state.Phi, state.Pi, mu2_abs, lam, dt=dt * 0.5,
        n_sub=n_phi_sub, phase=phase_resolved)

    # P1: Yukawa half-kick on Π using pre-Dirac Ψ.
    # Post-2026-05-16 Dirac mass-convention refactor: H_D = c·α·k + M·β
    # with M = y·Φ (c only in the kinetic generator).  The Yukawa
    # Hamiltonian density is then the clean SM form
    #     H_Y = y · (Φ·η†χ + Φ*·χ†η)        -- no c² factor.
    # Hamilton's equation gives  δΠ/δt = -∂H_Y/∂Φ* = -y·χ†η.
    if back_react:
        chi_dag_eta = (np.conj(state.chi_u) * state.eta_u +
                       np.conj(state.chi_d) * state.eta_d)
        state.Pi = state.Pi - 0.5 * dt * yukawa * chi_dag_eta

    # Build complex Yukawa mass M(x) = y·Φ(x).
    # P2 (2026-05-14): full Standard-Model Yukawa bilinear.  The Lagrangian
    # L_Y = -y·(Φ·η†·χ + Φ*·χ†·η) gives a complex mass that couples
    # η → χ with coefficient y·Φ and χ → η with coefficient y·Φ*.
    m_R = yukawa * state.Phi.real
    m_I = yukawa * state.Phi.imag

    # Full Dirac step at variable complex mass (exact-QCA propagator —
    # kinetic coefficient n = √(1 − m_0²) is derived inside; no `c`).
    state.eta_u, state.eta_d, state.chi_u, state.chi_d = \
        dirac.dirac_step_2d_varm_complex_splitstep(
            state.eta_u, state.eta_d, state.chi_u, state.chi_d,
            m_R_field=m_R, m_I_field=m_I, dt=dirac_dt)

    # P1: Yukawa half-kick on Π using post-Dirac Ψ.  No c² factor — see
    # the symmetric kick above for the rationale.
    if back_react:
        chi_dag_eta = (np.conj(state.chi_u) * state.eta_u +
                       np.conj(state.chi_d) * state.eta_d)
        state.Pi = state.Pi - 0.5 * dt * yukawa * chi_dag_eta

    # Second half-step Φ-free
    state.Phi, state.Pi = hg.kg_step_strang(
        state.Phi, state.Pi, mu2_abs, lam, dt=dt * 0.5,
        n_sub=n_phi_sub, phase=phase_resolved)

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


def total_energy(state, mu2, lam, yukawa):
    """
    Joint Φ–Ψ Hamiltonian energy.

        H_total = H_KG + H_D_kin + H_Y
        H_KG    = ∫ (|Π|² + |∇Φ|² + V(|Φ|²)) dx     (existing phi_energy)
        H_D_kin = ⟨Ψ| n·α·k |Ψ⟩  with  n = √(1−m_0²),  m_0 = y·mean(Re Φ)
        H_Y     = ∫ y·(Φ·η†χ + Φ*·χ†η) dx           (Yukawa interaction)

    The kinetic block coefficient is no longer a free `c` — under the
    exact-QCA admissibility (Finding 9, 2026-05-17) it is fixed at
    n = √(1 − m_0²) for the baseline mass m_0 = y·mean(Re Φ).  The
    continuum bilinear ⟨Ψ|n·α·k|Ψ⟩ is used here as the small-k limit
    of the exact-QCA Dirac kinetic energy — accurate enough for the F3
    symplectic bound (5% drift tolerance) given the low-k packets and
    small masses used in the regression tests.

    The mass term ∫ Ψ̄ m_eff Ψ is absorbed into H_Y (since m_eff = y·Φ);
    no double-counting.
    """
    # H_KG
    H_KG = phi_energy(state, mu2, lam)

    # Baseline mass and kinetic coefficient
    m0 = float(yukawa * state.Phi.real.mean())
    n0 = float(np.sqrt(max(0.0, 1.0 - m0 * m0)))

    # H_D_kin in Fourier space, small-k continuum form with coefficient n0:
    #   (n·α·k·Ψ)_{η↑} =  n·(kx−iky)·η_↓
    #   (n·α·k·Ψ)_{η↓} =  n·(kx+iky)·η_↑
    #   (n·α·k·Ψ)_{χ↑} = −n·(kx−iky)·χ_↓
    #   (n·α·k·Ψ)_{χ↓} = −n·(kx+iky)·χ_↑
    # Parseval: ∫ |f|² dx = (1/N) ∑_k |F(k)|² for numpy fft conventions.
    Lx, Ly = state.Phi.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    EU = np.fft.fft2(state.eta_u);  ED = np.fft.fft2(state.eta_d)
    CU = np.fft.fft2(state.chi_u);  CD = np.fft.fft2(state.chi_d)
    H_EU =  n0 * (KX - 1j * KY) * ED
    H_ED =  n0 * (KX + 1j * KY) * EU
    H_CU = -n0 * (KX - 1j * KY) * CD
    H_CD = -n0 * (KX + 1j * KY) * CU
    H_D_kin = float(np.real(np.sum(
        np.conj(EU) * H_EU + np.conj(ED) * H_ED +
        np.conj(CU) * H_CU + np.conj(CD) * H_CD
    )) / (Lx * Ly))

    # H_Y = y·(Φ·η†χ + Φ*·χ†η) summed over cells — clean SM Yukawa form.
    # η†χ = conj(η_u)·χ_u + conj(η_d)·χ_d.
    eta_dag_chi = (np.conj(state.eta_u) * state.chi_u +
                   np.conj(state.eta_d) * state.chi_d)
    # Φ·η†χ + Φ*·χ†η = 2·Re(Φ·η†χ)  (since (Φ·η†χ)* = Φ*·χ†η)
    H_Y = 2.0 * yukawa * float(np.real(np.sum(state.Phi * eta_dag_chi)))

    return H_KG + H_D_kin + H_Y
