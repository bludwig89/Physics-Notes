"""
ca_higgs.py  —  Complex scalar Φ (Higgs) field CA
====================================================
Implements the proposition's scalar field with Mexican-hat self-potential.

Field equations:
    L = ∂_μΦ* ∂^μΦ  −  V(|Φ|²)
    V(|Φ|²) = −μ² |Φ|²  +  λ |Φ|⁴

    Equations of motion (∂_t²Φ − ∇²Φ + V'·Φ = 0 where V' = dV/d|Φ|²·2/|Φ|·|Φ|):
        ∂_t Φ = Π
        ∂_t Π = ∇²Φ  −  (−μ² + 2λ|Φ|²)·Φ

Vacuum:  |Φ|² = μ²/(2λ) ≡ v² ⇒ Φ_vac = v·e^{iα} (any α).
Higgs mass (radial mode):  m_h² = 2μ²    (standard SM convention)

State per cell: Φ (complex) + Π (complex) — 4 real numbers.

Propagator: Strang split between the linear (FFT-diagonal) Klein-Gordon
kinetic part and the nonlinear position-space correction:

    H_lin  = ∇² − m_0²·I,   with m_0² = 2μ² (Higgs mass around vacuum)
    H_nl   = m_0² − (−μ² + 2λ|Φ|²)
           = 3μ² − 2λ|Φ|²   (the residual after absorbing linear mass)

Test contract:  setting Φ = v, Π = 0 keeps the field at vacuum exactly,
because V'(|Φ|²=v²)·Φ = 0.
"""

import numpy as np


# ══════════════════════════════════════════════════════════════════
#  Free Klein-Gordon split-step propagator
# ══════════════════════════════════════════════════════════════════

def kg_step_free_2d_splitstep(Phi, Pi, m, dt=1.0):
    """
    One step of free (V=0) Klein-Gordon CA with mass m, via Fourier-space
    exact propagator.

    Each k-mode evolves as a 2D rotation in (Φ, Π) phase space with
    angular frequency ω = √(k² + m²):

        [Φ_new]   [ cos(ωdt)         sin(ωdt)/ω ]   [Φ]
        [     ] = [                              ] · [ ]
        [Π_new]   [ −ω·sin(ωdt)      cos(ωdt)   ]   [Π]

    This is exactly unitary (preserves the Klein-Gordon energy norm).
    """
    Lx, Ly = Phi.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')

    omega = np.sqrt(KX**2 + KY**2 + m**2)
    omega_safe = np.where(omega == 0.0, 1.0, omega)

    cos_w = np.cos(omega * dt)
    sin_w = np.sin(omega * dt)
    sinc_w = sin_w / omega_safe
    sinc_w = np.where(omega == 0.0, dt, sinc_w)

    Phi_k = np.fft.fft2(Phi)
    Pi_k  = np.fft.fft2(Pi)

    Phi_new_k = cos_w * Phi_k + sinc_w * Pi_k
    Pi_new_k  = -omega**2 * sinc_w * Phi_k + cos_w * Pi_k

    return np.fft.ifft2(Phi_new_k), np.fft.ifft2(Pi_new_k)


# ══════════════════════════════════════════════════════════════════
#  Mexican-hat self-interaction (nonlinear position-space step)
# ══════════════════════════════════════════════════════════════════

def _resolve_phase_sign(phase):
    """
    Resolve the broken/symmetric phase keyword into the sign multiplier
    that the V' formula applies to mu2.

      phase='broken'    →  V = -mu2|Φ|² + λ|Φ|⁴      (μ²>0, vacuum at |Φ|=v)
      phase='symmetric' →  V = +mu2|Φ|² + λ|Φ|⁴      (μ²>0, vacuum at Φ=0)

    `mu2` is always a non-negative magnitude in the new API.  The legacy
    convention of passing a *negative* mu2 to flip the quadratic term
    still works (phase='broken' with mu2<0 reproduces the old behaviour),
    so existing callers do not break.
    """
    if phase == 'broken':
        return +1.0
    if phase == 'symmetric':
        return -1.0
    raise ValueError(
        f"phase must be 'broken' or 'symmetric', got {phase!r}")


def kg_nonlinear_kick(Phi, Pi, mu2, lam, m0_sq, dt, phase='broken'):
    """
    Apply the nonlinear residual of V'(|Φ|²) for time dt:

        Π → Π − dt · [V'_full(|Φ|²) − m_0²]·Φ
           = Π − dt · [(−s·μ² + 2λ|Φ|²) − m_0²]·Φ
           = Π − dt · (−s·μ² − m_0² + 2λ|Φ|²)·Φ

    where s = +1 for phase='broken' (V = -μ²|Φ|²+λ|Φ|⁴) and s = -1 for
    phase='symmetric' (V = +μ²|Φ|²+λ|Φ|⁴).  `mu2` is the *magnitude* μ²≥0.

    The "kick" is a single per-cell update to Π.  Exact for the
    nonlinear piece; Strang composition with the free K-G step gives
    O(dt²) accuracy overall.

    Set m_0² = 2μ² to absorb the *vacuum-mass* part of V' into the
    linear step.  At |Φ|² = v² = μ²/(2λ), the residual is exactly
    zero — vacuum is a fixed point of the full update.
    """
    s = _resolve_phase_sign(phase)
    mu2_eff = s * mu2
    abs2 = (Phi * np.conj(Phi)).real
    V_prime_full = -mu2_eff + 2.0 * lam * abs2
    # V(|Φ|²) = -s·μ²|Φ|² + λ|Φ|⁴.  ∂V/∂Φ* = (-s·μ² + 2λ|Φ|²)·Φ.
    # Equation of motion: □Φ + ∂V/∂Φ* = 0.
    # ∂_t Π = ∇²Φ - (-s·μ² + 2λ|Φ|²)·Φ
    # In the linear step we already included -m_0²·Φ in the force.
    # The residual is the difference: -[(-s·μ²+2λ|Φ|²) - m_0²]·Φ
    force = -(V_prime_full - m0_sq) * Phi
    Pi_new = Pi + dt * force
    return Phi.copy(), Pi_new


def _laplacian_2d(Phi):
    """FFT-exact 2D Laplacian (periodic boundaries)."""
    Lx, Ly = Phi.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    k2 = -(KX**2 + KY**2)
    return np.fft.ifft2(k2 * np.fft.fft2(Phi))


def _force(Phi, mu2, lam, phase='broken'):
    """
    Force on Π:  F(Φ) = ∇²Φ − V'_total(|Φ|²)·Φ
                       = ∇²Φ − (−s·μ² + 2λ|Φ|²)·Φ

    where s = _resolve_phase_sign(phase).

      phase='broken'    (s=+1): V = -μ²|Φ|² + λ|Φ|⁴  →  vacuum |Φ|=v.
      phase='symmetric' (s=-1): V = +μ²|Φ|² + λ|Φ|⁴  →  vacuum Φ=0.

    `mu2` is always a non-negative magnitude μ²≥0 in the new API.  The
    legacy convention (negative mu2, phase='broken') is still honoured.

    At broken-phase vacuum |Φ|² = μ²/(2λ) = v² (constant in space),
    ∇²Φ = 0 and (−μ² + 2λv²) = 0, so F = 0.  At symmetric-phase vacuum
    Φ = 0, F = 0 trivially.
    """
    s = _resolve_phase_sign(phase)
    mu2_eff = s * mu2
    abs2 = (Phi * np.conj(Phi)).real
    V_prime = -mu2_eff + 2.0 * lam * abs2
    return _laplacian_2d(Phi) - V_prime * Phi


def kg_step_strang(Phi, Pi, mu2, lam, dt=1.0, n_sub=1, phase='broken',
                    **kwargs):
    """
    Symplectic velocity-Verlet integrator for the full nonlinear K-G CA.

    Per sub-step:
        Π_{n+1/2} = Π_n  +  (dt/2)·F(Φ_n)
        Φ_{n+1}   = Φ_n  +  dt·Π_{n+1/2}
        Π_{n+1}   = Π_{n+1/2}  +  (dt/2)·F(Φ_{n+1})

    Symplectic: conserves energy to O(dt²) over arbitrary time.

    Parameters
    ----------
    mu2 : float
        Magnitude μ² ≥ 0.  Sign convention is set by `phase`.
    lam : float
        Quartic coefficient λ > 0.
    phase : {'broken', 'symmetric'}
        'broken' (default) uses V = -μ²|Φ|² + λ|Φ|⁴; vacuum (Φ=v, Π=0)
        is a fixed point because F(Φ=v)=0.
        'symmetric' uses V = +μ²|Φ|² + λ|Φ|⁴; vacuum (Φ=0, Π=0) is the
        fixed point.  This replaces the old kludge of passing mu2 < 0.
    n_sub : int
        Sub-divide the timestep for stiffer regimes.
    """
    dt_sub = dt / n_sub
    for _ in range(n_sub):
        F = _force(Phi, mu2, lam, phase=phase)
        Pi_half = Pi + 0.5 * dt_sub * F
        Phi_new = Phi + dt_sub * Pi_half
        F_new = _force(Phi_new, mu2, lam, phase=phase)
        Pi_new = Pi_half + 0.5 * dt_sub * F_new
        Phi, Pi = Phi_new, Pi_new
    return Phi, Pi


# ══════════════════════════════════════════════════════════════════
#  Verifications
# ══════════════════════════════════════════════════════════════════

def verify_vacuum_fixed_point(L=32, n_steps=1000, mu2=0.5, lam=0.5, dt=0.5):
    """
    Set Φ = v exactly, Π = 0.  Run the propagator and check it stays put.
    This is F1's vacuum-stability test.
    """
    v = float(np.sqrt(mu2 / (2.0 * lam)))
    Phi = np.full((L, L), v + 0.0j)
    Pi  = np.zeros((L, L), dtype=complex)

    Phi_0 = Phi.copy()
    for _ in range(n_steps):
        Phi, Pi = kg_step_strang(Phi, Pi, mu2, lam, dt=dt)

    deviation = float(np.max(np.abs(Phi - Phi_0)))
    pi_max    = float(np.max(np.abs(Pi)))
    return {
        'v':         v,
        'max_drift_Phi': deviation,
        'max_drift_Pi':  pi_max,
    }


def verify_higgs_dispersion_2d(L=64, n_steps=20, mu2=0.5, lam=0.5, dt=0.15,
                                 amplitude=1e-4, k_indices=None,
                                 mode='radial'):
    """
    F2 test.  The Mexican-hat potential has *two* propagating modes
    around the vacuum:

      Radial (Higgs):     Re(δΦ) — mass²  m_h² = 2μ²
      Angular (Goldstone): Im(δΦ) — mass²  0

    These decouple at linear order because V depends only on |Φ|², so
    Re and Im of δΦ feel different effective potentials.

    For each mode, the dispersion is:
        radial:   ω(k) = √(k² + 2μ²)
        Goldstone: ω(k) = |k|

    Method.  Use a real cosine initial profile in the chosen Re or Im
    direction, with Π = 0.  Track ⟨cos(k·x), δΦ_proj(t)⟩ across the run,
    fit  A·cos(ω·t)  by linear least squares on (cos, sin) features.

    Keep n_steps·ω_max·dt below π to avoid sign ambiguities.

    Returns: list of dicts with kx, ky, kappa, omega_numeric,
    omega_analytic, residual.
    """
    if k_indices is None:
        k_indices = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 2)]

    v = float(np.sqrt(mu2 / (2.0 * lam)))
    m_h_sq = 2.0 * mu2
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    results = []
    for ix, iy in k_indices:
        kx = 2.0 * np.pi * ix / L
        ky = 2.0 * np.pi * iy / L
        kappa = float(np.sqrt(kx**2 + ky**2))

        if mode == 'radial':
            omega_an = float(np.sqrt(kappa**2 + m_h_sq))
            spatial = np.cos(kx * X + ky * Y)
            delta_Phi = (amplitude * spatial).astype(complex)   # purely real
        elif mode == 'goldstone':
            omega_an = float(kappa)
            spatial = np.cos(kx * X + ky * Y)
            delta_Phi = (1j * amplitude * spatial)              # purely imaginary
        else:
            raise ValueError(mode)

        Phi = v + delta_Phi
        Pi  = np.zeros_like(Phi)

        # Track projection on cos(k·x) across time
        proj_amps = []
        times = []
        norm = float(np.sum(spatial * spatial))
        for step in range(n_steps + 1):
            if mode == 'radial':
                comp = (Phi - v).real
            else:
                comp = (Phi - v).imag
            p = float(np.sum(spatial * comp)) / norm
            proj_amps.append(p)
            times.append(step * dt)
            if step < n_steps:
                Phi, Pi = kg_step_strang(Phi, Pi, mu2, lam, dt=dt)
        proj_amps = np.array(proj_amps)
        times = np.array(times)

        # Linear LSQ: proj(t) = A·cos(ω·t) — but ω is unknown.
        # Use Fourier search: scan ω in a small range around omega_an and
        # find the value that maximizes the (cos, sin) correlation.
        omegas = np.linspace(omega_an * 0.5, omega_an * 1.5, 4001)
        best_corr = -np.inf
        best_omega = omega_an
        for w in omegas:
            cs = np.cos(w * times)
            corr = abs(np.dot(proj_amps, cs)) / np.linalg.norm(cs)
            if corr > best_corr:
                best_corr = corr
                best_omega = float(w)
        residual = float(abs(best_omega - omega_an))

        results.append({
            'kx': kx, 'ky': ky, 'kappa': kappa,
            'omega_numeric':  best_omega,
            'omega_analytic': omega_an,
            'residual':       residual,
        })
    return results
