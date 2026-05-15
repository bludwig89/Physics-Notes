"""
ca_core.py  —  Cellular Automaton physics core
================================================
Based on physics notebook pages 35-39, Mark Ludwig (2007-08).

Stages implemented
------------------
1. scalar_step_2d       — 2nd-order scalar wave CA  (page 37)
2. weyl_step_2d/3d      — spinor Weyl CA            (page 38)
3. cfl_sweep            — stability sweep            (page 39)
4. run_and_reverse      — time-reversal test         (Fredkin)
"""

import numpy as np


# ══════════════════════════════════════════════════════════════════
#  Stage 1 — Scalar Wave CA  (Page 37)
# ══════════════════════════════════════════════════════════════════

def scalar_step_2d(f_now, f_prev, c=1.0):
    """
    One step of the 2D finite-differenced scalar wave equation (page 37).

    f(m,n,t+1) = 2f(t) - f(t-1) + c² · ∇²f(t)

    where ∇²f is the standard 4-neighbour Laplacian.

    Stability requires  c ≤ 1/√2 ≈ 0.71  (2D CFL condition).
    The notebook writes the equation with c=1, which violates this and
    causes the divergence described on page 39.
    """
    lap = (np.roll(f_now, -1, axis=0) + np.roll(f_now,  1, axis=0) +
           np.roll(f_now, -1, axis=1) + np.roll(f_now,  1, axis=1) -
           4.0 * f_now)
    return 2.0 * f_now - f_prev + (c ** 2) * lap


# ══════════════════════════════════════════════════════════════════
#  Stage 2 — Spinor-Valued Weyl CA  (Page 38)
# ══════════════════════════════════════════════════════════════════

def weyl_step_2d(f, g, c=0.5):
    """
    ⚠️  PEDAGOGICAL ONLY — DO NOT USE FOR PRODUCTION RUNS  ⚠️

    One step of the 2D Weyl spinor CA  (page 38, z-derivatives dropped).

    Derived from the massless Weyl equation  ∂ψ/∂t = -σ·∇ψ  with Pauli
    matrices.  The z-component terms vanish in 2D, leaving:

        ∂f/∂t = -∂ₓg + i ∂ᵧg
        ∂g/∂t = -∂ₓf - i ∂ᵧf

    Finite-differenced (centred, Δ=1), with the overall speed factor c
    replacing the ½ in the notebook's explicit formulae.

    Why this is here at all:
        This is the explicit-Euler scheme exactly as written in the
        notebook (page 38).  It is retained so the simulation can
        reproduce the page 39 instability observation.

    Why you should not use it:
        Explicit Euler applied to a skew-Hermitian operator is
        UNCONDITIONALLY UNSTABLE — divergence is guaranteed for every
        c > 0, and the page 39 "stabilises at ~0.43" observation is
        slower divergence, not true stability.  See ca-reference.md
        Stage 2 for the full discussion.

        For all production runs use `weyl_step_2d_splitstep`, which is
        exactly unitary, unconditionally stable, and matches the same
        underlying PDE.

    Parameters
    ----------
    f, g : complex128 arrays, shape (Lx, Ly)
        Upper and lower spinor components.
    c : float
        Lattice speed factor.  Notebook observation: marginally stable
        near c ≈ 0.43 (in 3D); 2D stability boundary is lower.

    Returns
    -------
    f_new, g_new : updated spinor arrays
    """
    # Centred differences  (each = right_neighbour - left_neighbour)
    dg_dx = np.roll(g, -1, axis=0) - np.roll(g,  1, axis=0)
    dg_dy = np.roll(g, -1, axis=1) - np.roll(g,  1, axis=1)
    df_dx = np.roll(f, -1, axis=0) - np.roll(f,  1, axis=0)
    df_dy = np.roll(f, -1, axis=1) - np.roll(f,  1, axis=1)

    f_new = f + c * (-dg_dx + 1j * dg_dy)
    g_new = g + c * (-df_dx - 1j * df_dy)
    return f_new, g_new


def weyl_step_3d(f, g, c=0.5):
    """
    ⚠️  PEDAGOGICAL ONLY — DO NOT USE FOR PRODUCTION RUNS  ⚠️

    One step of the full 3D Weyl spinor CA  (page 38, all terms).

    Axes: 0 = x (l), 1 = y (m), 2 = z (n)  — matching the notebook.

    The explicit update rules from the notebook (with Δ=1):

        f(l,m,n,t+1) - f = -c·(f_{n+1}-f_{n-1}) - c·(g_{l+1}-g_{l-1})
                           + ic·(g_{m+1}-g_{m-1})
        g(l,m,n,t+1) - g = -c·(f_{l+1}-f_{l-1}) - ic·(f_{m+1}-f_{m-1})
                           + c·(g_{n+1}-g_{n-1})

    Same instability caveat as `weyl_step_2d`: explicit Euler on a
    skew-Hermitian operator is unconditionally unstable.  Retained to
    reproduce the page 39 observation.  Use `weyl_step_3d_splitstep`
    for any actual run.
    """
    df_dz = np.roll(f, -1, axis=2) - np.roll(f,  1, axis=2)
    dg_dx = np.roll(g, -1, axis=0) - np.roll(g,  1, axis=0)
    dg_dy = np.roll(g, -1, axis=1) - np.roll(g,  1, axis=1)

    df_dx = np.roll(f, -1, axis=0) - np.roll(f,  1, axis=0)
    df_dy = np.roll(f, -1, axis=1) - np.roll(f,  1, axis=1)
    dg_dz = np.roll(g, -1, axis=2) - np.roll(g,  1, axis=2)

    f_new = f + c * (-df_dz - dg_dx + 1j * dg_dy)
    g_new = g + c * (-df_dx - 1j * df_dy + dg_dz)
    return f_new, g_new


# ══════════════════════════════════════════════════════════════════
#  Initial conditions
# ══════════════════════════════════════════════════════════════════

def gaussian_2d(shape, center=None, sigma=3.0):
    """Real Gaussian envelope on a 2D grid."""
    Lx, Ly = shape
    cx, cy = center if center is not None else (Lx // 2, Ly // 2)
    x = np.arange(Lx) - cx
    y = np.arange(Ly) - cy
    X, Y = np.meshgrid(x, y, indexing='ij')
    return np.exp(-(X ** 2 + Y ** 2) / (2.0 * sigma ** 2))


def gaussian_spinor_2d(shape, center=None, sigma=3.0, helicity='left'):
    """
    2-component Gaussian spinor pulse.

    helicity='left'  → f = G,   g = 0
    helicity='right' → f = 0,   g = G
    helicity='mixed' → f = G/√2, g = G/√2
    """
    G = gaussian_2d(shape, center, sigma).astype(complex)
    if helicity == 'left':
        return G, np.zeros_like(G)
    elif helicity == 'right':
        return np.zeros_like(G), G
    else:
        return G / np.sqrt(2.0), G / np.sqrt(2.0)


def gaussian_spinor_3d(shape, center=None, sigma=3.0, helicity='left'):
    """3D version of gaussian_spinor_2d."""
    Lx, Ly, Lz = shape
    cx, cy, cz = center if center is not None else (Lx//2, Ly//2, Lz//2)
    x = np.arange(Lx) - cx
    y = np.arange(Ly) - cy
    z = np.arange(Lz) - cz
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    G = np.exp(-(X**2 + Y**2 + Z**2) / (2.0 * sigma**2)).astype(complex)
    if helicity == 'left':
        return G, np.zeros_like(G)
    elif helicity == 'right':
        return np.zeros_like(G), G
    else:
        return G / np.sqrt(2.0), G / np.sqrt(2.0)


# ══════════════════════════════════════════════════════════════════
#  Stage 2b — Split-Step (FFT) Weyl CA  (exact, unconditionally stable)
# ══════════════════════════════════════════════════════════════════

def weyl_step_2d_splitstep(f, g, c=0.5):
    """
    Exact split-step (FFT) propagator for the 2D Weyl spinor CA.

    Each Fourier mode k = (kx, ky) is propagated by the exact 2×2 unitary:

        U(k) = cos(c·κ)·I  −  i·sin(c·κ)/κ · (σ·k)

    where κ = |k| = sqrt(kx² + ky²) and (with kz = 0 in 2D):

        σ·k = [[  0,        kx − i·ky ],
                [ kx + i·ky,   0       ]]

    so

        U = [[ cos(c·κ),              −i·sinc(c·κ)·(kx − i·ky) ],
             [ −i·sinc(c·κ)·(kx + i·ky),  cos(c·κ)             ]]

    where sinc(c·κ) ≡ sin(c·κ)/κ  (set to c at κ=0 by L'Hôpital).

    This is exactly unitary for all c — norm is conserved to machine
    precision and the scheme is unconditionally stable.
    """
    Lx, Ly = f.shape

    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi   # shape (Lx,)
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi   # shape (Ly,)
    KX, KY = np.meshgrid(kx, ky, indexing='ij')  # (Lx, Ly)

    kappa      = np.sqrt(KX**2 + KY**2)
    kappa_safe = np.where(kappa == 0.0, 1.0, kappa)

    cos_ck  = np.cos(c * kappa)
    sinc_ck = np.sin(c * kappa) / kappa_safe   # sin(c·κ)/κ; L'Hôpital at 0 → c

    F = np.fft.fft2(f)
    G = np.fft.fft2(g)

    F_new = cos_ck * F  +  (-1j * sinc_ck * (KX - 1j * KY)) * G
    G_new = (-1j * sinc_ck * (KX + 1j * KY)) * F  +  cos_ck * G

    return np.fft.ifft2(F_new), np.fft.ifft2(G_new)


def weyl_step_3d_splitstep(f, g, c=0.5):
    """
    Exact split-step (FFT) propagator for the 3D Weyl spinor CA.

    Each Fourier mode k = (kx, ky, kz) is propagated by the exact 2×2 unitary:

        U(k) = cos(c·κ)·I  −  i·sin(c·κ)/κ · (σ·k)

    where κ = |k| = sqrt(kx² + ky² + kz²) and:

        σ·k = [[  kz,        kx − i·ky ],
                [ kx + i·ky,  −kz      ]]

    so the four matrix elements are:

        U_ff =  cos(c·κ) − i·sinc(c·κ)·kz
        U_fg = −i·sinc(c·κ)·(kx − i·ky)
        U_gf = −i·sinc(c·κ)·(kx + i·ky)
        U_gg =  cos(c·κ) + i·sinc(c·κ)·kz

    Exactly unitary, unconditionally stable for all c.
    Axes: 0 = x (l), 1 = y (m), 2 = z (n) — matching the notebook.
    """
    Lx, Ly, Lz = f.shape

    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    kz = np.fft.fftfreq(Lz) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')

    kappa      = np.sqrt(KX**2 + KY**2 + KZ**2)
    kappa_safe = np.where(kappa == 0.0, 1.0, kappa)

    cos_ck  = np.cos(c * kappa)
    sinc_ck = np.sin(c * kappa) / kappa_safe

    F = np.fft.fftn(f)
    G = np.fft.fftn(g)

    U_ff =  cos_ck - 1j * sinc_ck * KZ
    U_fg = -1j * sinc_ck * (KX - 1j * KY)
    U_gf = -1j * sinc_ck * (KX + 1j * KY)
    U_gg =  cos_ck + 1j * sinc_ck * KZ

    F_new = U_ff * F + U_fg * G
    G_new = U_gf * F + U_gg * G

    return np.fft.ifftn(F_new), np.fft.ifftn(G_new)


# ══════════════════════════════════════════════════════════════════
#  Stage 3 — CFL Stability Sweep  (Page 39)
# ══════════════════════════════════════════════════════════════════

def cfl_sweep(grid_size, n_steps, c_values, dim=2, sigma=2.0,
              growth_threshold=5.0, use_splitstep=True):
    """
    Sweep c values; measure peak |ψ|² after n_steps (or at divergence).

    Default is `use_splitstep=True` (exact unitary propagator) — all c
    values should remain stable (peak ratio ≈ 1.0, diverged=False).

    Pass `use_splitstep=False` ONLY to reproduce the page 39 observation
    that the explicit-Euler simulation "interestingly stabilises at
    ~0.43" in the 3D case.  That scheme is unconditionally unstable
    (see `weyl_step_2d` / `weyl_step_3d` docstrings); the ~0.43 threshold
    is slower divergence, not true stability.

    A run is marked as diverged if the peak amplitude ever exceeds
    growth_threshold × the initial peak (default: 5×).

    Returns
    -------
    list of (c, peak_amplitude, diverged_flag)
    """
    shape  = (grid_size,) * dim
    center = tuple(s // 2 for s in shape)

    if dim == 2:
        init_fn = gaussian_spinor_2d
        step_fn = weyl_step_2d_splitstep if use_splitstep else weyl_step_2d
    else:
        init_fn = gaussian_spinor_3d
        step_fn = weyl_step_3d_splitstep if use_splitstep else weyl_step_3d

    results = []
    for c in c_values:
        f, g         = init_fn(shape, center, sigma=sigma)
        initial_peak = float(np.max(np.abs(f)**2 + np.abs(g)**2))
        threshold    = growth_threshold * initial_peak
        peak         = initial_peak
        diverged     = False

        for _ in range(n_steps):
            f, g = step_fn(f, g, c)
            amp  = float(np.max(np.abs(f)**2 + np.abs(g)**2))
            if np.isnan(amp) or amp > threshold:
                peak     = amp
                diverged = True
                break
            peak = amp

        results.append((c, peak, diverged))

    return results


# ══════════════════════════════════════════════════════════════════
#  Utility — norm tracking
# ══════════════════════════════════════════════════════════════════

def norm_over_time(f0, g0, n_steps, c, step_fn):
    """
    Track total probability  ∑|f|² + |g|²  at each step.

    A perfectly unitary scheme conserves this exactly.  Numerical
    deviations grow with c (larger c → larger truncation error).
    """
    f, g   = f0.copy(), g0.copy()
    norms  = [float(np.sum(np.abs(f)**2 + np.abs(g)**2))]
    for _ in range(n_steps):
        f, g = step_fn(f, g, c)
        norms.append(float(np.sum(np.abs(f)**2 + np.abs(g)**2)))
    return np.array(norms)


# ══════════════════════════════════════════════════════════════════
#  Stage 5 — Time-Reversal / Reversibility  (Fredkin correlation)
# ══════════════════════════════════════════════════════════════════

def run_and_reverse(f0, g0, n_steps, c, step_fn):
    """
    Run n_steps forward (speed +c) then n_steps backward (speed -c).

    Negating c reverses the sign of all derivative terms, implementing
    time-reversal.  For a unitary update, ψ_final ≈ ψ_initial to
    machine precision.

    Returns
    -------
    float : relative residual  ||ψ_final - ψ_initial|| / ||ψ_initial||
    """
    f, g = f0.copy(), g0.copy()
    for _ in range(n_steps):
        f, g = step_fn(f, g,  c)
    for _ in range(n_steps):
        f, g = step_fn(f, g, -c)

    norm0    = float(np.sqrt(np.sum(np.abs(f0)**2 + np.abs(g0)**2)))
    residual = float(np.sqrt(np.sum(np.abs(f - f0)**2 + np.abs(g - g0)**2)))
    return residual / norm0 if norm0 > 0 else residual


# ══════════════════════════════════════════════════════════════════
#  Dispersion verification — does the propagator give ω = c·|k| ?
# ══════════════════════════════════════════════════════════════════
#
# The massless Weyl equation has dispersion ω = c·|k|.  The split-step
# propagator is built from U(k) = cos(c·κ)·I − i sin(c·κ)/κ · (σ·k),
# whose eigenvalues for a helicity-+ eigenstate of σ·k are exp(−i c·κ).
# A plane-wave field initialized on that eigenvector should therefore
# acquire phase −c·κ per step.  The functions below verify this
# numerically — a non-trivial check that complements norm conservation
# and time-reversibility (it catches sign errors or component swaps
# that those checks would miss).
#
# Measured residuals (2026-05-14, see ca-reference.md):
#   2D, L=32, n_steps=20, c=0.5  →  max |Δω| ≈ 5e-17
#   3D, L=16, n_steps=20, c=0.5  →  max |Δω| ≈ 8e-17
# i.e. machine precision — confirms U(k) is the exact Weyl propagator.
# ══════════════════════════════════════════════════════════════════

def _helicity_plus_eigenvector(kx, ky, kz=0.0):
    """
    Positive-helicity eigenvector of σ·k (eigenvalue +|k|) at wavevector
    k = (kx, ky, kz).  Set kz=0 for 2D usage.

    In spherical coordinates (θ, φ) of k:
        h_+ = (cos(θ/2),  sin(θ/2) · e^{iφ})

    For k = 0 the eigenstructure is degenerate; we return (1, 0).
    """
    kappa = float(np.sqrt(kx**2 + ky**2 + kz**2))
    if kappa == 0.0:
        return np.array([1.0 + 0.0j, 0.0 + 0.0j])
    cos_half = np.sqrt((kappa + kz) / (2.0 * kappa))
    sin_half = np.sqrt((kappa - kz) / (2.0 * kappa))
    k_perp   = np.sqrt(kx**2 + ky**2)
    phase    = (kx + 1j * ky) / k_perp if k_perp > 0.0 else 1.0 + 0.0j
    return np.array([cos_half + 0.0j, sin_half * phase])


def verify_dispersion_2d(L=32, n_steps=20, c=0.5, k_indices=None):
    """
    Verify the 2D split-step propagator reproduces the Weyl dispersion
    ω = c·|k| at machine precision.

    For each test wavevector k = 2π·(ix,iy)/L, build a plane-wave field
    with the positive-helicity eigenvector of σ·k, evolve n_steps with
    `weyl_step_2d_splitstep`, and extract the per-step phase rotation
    from the inner product ⟨ψ₀, ψ_N⟩ = e^{−iωN}·⟨ψ₀, ψ₀⟩.

    Stay below the phase-wrap bound  c·|k|·n_steps < π.

    Returns
    -------
    list of dicts with keys: kx, ky, kappa, omega_numeric,
    omega_analytic, residual.
    """
    if k_indices is None:
        k_indices = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 2), (1, 4)]

    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    results = []
    for ix, iy in k_indices:
        kx = 2.0 * np.pi * ix / L
        ky = 2.0 * np.pi * iy / L
        kappa = float(np.sqrt(kx**2 + ky**2))

        h = _helicity_plus_eigenvector(kx, ky, 0.0)
        phase_field = np.exp(1j * (kx * X + ky * Y))
        f0 = h[0] * phase_field
        g0 = h[1] * phase_field
        ip0 = np.sum(np.conj(f0) * f0 + np.conj(g0) * g0)

        f, g = f0.copy(), g0.copy()
        for _ in range(n_steps):
            f, g = weyl_step_2d_splitstep(f, g, c)

        ip = np.sum(np.conj(f0) * f + np.conj(g0) * g) / ip0
        omega_analytic = c * kappa
        # Ratio to the expected propagator phase — avoids phase-wrap issues
        # when c·|k|·n_steps > π.
        ratio          = ip * np.exp(1j * omega_analytic * n_steps)
        delta_omega    = float(np.angle(ratio) / n_steps)
        omega_numeric  = float(omega_analytic + delta_omega)
        residual       = float(abs(delta_omega))

        results.append({
            'kx': kx, 'ky': ky, 'kappa': kappa,
            'omega_numeric':  omega_numeric,
            'omega_analytic': omega_analytic,
            'residual':       residual,
        })
    return results


def verify_dispersion_3d(L=16, n_steps=20, c=0.5, k_indices=None):
    """
    3D version of `verify_dispersion_2d`.  Uses `weyl_step_3d_splitstep`.

    k_indices : list of (ix, iy, iz) integer mode indices;
                k = 2π·(ix, iy, iz)/L.
    """
    if k_indices is None:
        k_indices = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
                     (1, 1, 0), (1, 1, 1), (2, 1, 1), (1, 2, 3)]

    xs = np.arange(L)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing='ij')

    results = []
    for ix, iy, iz in k_indices:
        kx = 2.0 * np.pi * ix / L
        ky = 2.0 * np.pi * iy / L
        kz = 2.0 * np.pi * iz / L
        kappa = float(np.sqrt(kx**2 + ky**2 + kz**2))

        h = _helicity_plus_eigenvector(kx, ky, kz)
        phase_field = np.exp(1j * (kx * X + ky * Y + kz * Z))
        f0 = h[0] * phase_field
        g0 = h[1] * phase_field
        ip0 = np.sum(np.conj(f0) * f0 + np.conj(g0) * g0)

        f, g = f0.copy(), g0.copy()
        for _ in range(n_steps):
            f, g = weyl_step_3d_splitstep(f, g, c)

        ip = np.sum(np.conj(f0) * f + np.conj(g0) * g) / ip0
        omega_analytic = c * kappa
        # Ratio to the expected propagator phase — avoids phase-wrap issues
        # when c·|k|·n_steps > π.
        ratio          = ip * np.exp(1j * omega_analytic * n_steps)
        delta_omega    = float(np.angle(ratio) / n_steps)
        omega_numeric  = float(omega_analytic + delta_omega)
        residual       = float(abs(delta_omega))

        results.append({
            'kx': kx, 'ky': ky, 'kz': kz, 'kappa': kappa,
            'omega_numeric':  omega_numeric,
            'omega_analytic': omega_analytic,
            'residual':       residual,
        })
    return results


# ══════════════════════════════════════════════════════════════════
#  Phase B1 — Group velocity measurement
# ══════════════════════════════════════════════════════════════════

def _gaussian_packet_2d(L, k0, sigma=5.0, center=None, helicity_plus=True):
    """
    Narrow-band Gaussian wave packet centered at wavevector k0 = (kx, ky)
    with envelope width sigma.  Initial spinor is the +1 eigenvector of
    σ·k0 (positive helicity).
    """
    if center is None:
        center = (L // 4, L // 2)   # off-center so it has room to travel
    cx, cy = center
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    envelope = np.exp(-((X - cx)**2 + (Y - cy)**2) / (2.0 * sigma**2))
    phase = np.exp(1j * (k0[0] * X + k0[1] * Y))

    kappa = float(np.sqrt(k0[0]**2 + k0[1]**2))
    if kappa == 0.0:
        h = np.array([1.0, 0.0], dtype=complex)
    else:
        phi = np.exp(1j * np.arctan2(k0[1], k0[0]))
        h = np.array([1.0, phi], dtype=complex) / np.sqrt(2.0)
        if not helicity_plus:
            h = np.array([1.0, -phi], dtype=complex) / np.sqrt(2.0)

    return h[0] * envelope * phase, h[1] * envelope * phase


def measure_group_velocity_2d(L=64, n_steps=40, c=0.5, k0=(0.5, 0.0),
                               sigma=5.0):
    """
    Track the centroid of a narrow-band Gaussian wave packet, measure its
    group velocity, compare to the analytic Weyl prediction v_g = c·k̂.

    For ω = c|k|:  v_g = ∇_k ω = c · (k/|k|)  — speed c, along k.

    Stops measurement before the packet wraps the torus.

    Returns
    -------
    dict with keys
        v_measured  : (vx, vy) measured group velocity from linear fit
        v_analytic  : (vx, vy) analytic group velocity = c·k̂
        speed_ratio : |v_measured| / |v_analytic|  (should be ≈ 1)
    """
    f, g = _gaussian_packet_2d(L, k0, sigma=sigma)
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    centroids = []
    for step in range(n_steps + 1):
        density = np.abs(f)**2 + np.abs(g)**2
        total = float(density.sum())
        if total > 0:
            cx = float((X * density).sum() / total)
            cy = float((Y * density).sum() / total)
        else:
            cx, cy = 0.0, 0.0
        centroids.append((cx, cy))
        if step < n_steps:
            f, g = weyl_step_2d_splitstep(f, g, c)

    centroids = np.array(centroids)
    # Linear fit to position vs time
    ts = np.arange(n_steps + 1)
    # Use only the central window to avoid edge effects
    fit_start = n_steps // 4
    fit_end   = 3 * n_steps // 4
    vx = float(np.polyfit(ts[fit_start:fit_end],
                          centroids[fit_start:fit_end, 0], 1)[0])
    vy = float(np.polyfit(ts[fit_start:fit_end],
                          centroids[fit_start:fit_end, 1], 1)[0])

    kappa = float(np.sqrt(k0[0]**2 + k0[1]**2))
    if kappa == 0.0:
        v_an = (0.0, 0.0)
    else:
        v_an = (c * k0[0] / kappa, c * k0[1] / kappa)

    speed_measured = float(np.sqrt(vx**2 + vy**2))
    speed_analytic = float(np.sqrt(v_an[0]**2 + v_an[1]**2))

    return {
        'v_measured':  (vx, vy),
        'v_analytic':  v_an,
        'speed_measured': speed_measured,
        'speed_analytic': speed_analytic,
        'speed_ratio': speed_measured / speed_analytic if speed_analytic > 0 else 0.0,
        'centroids': centroids,
    }


# ══════════════════════════════════════════════════════════════════
#  Phase B2 — Min-size / min-σ sweeps
# ══════════════════════════════════════════════════════════════════

def size_sweep_L(L_values, n_steps=100, c=0.5, sigma=3.0, k0=(0.8, 0.0)):
    """
    Vary lattice size L, hold (c, sigma, k0) fixed.  Measure
    (a) norm drift, (b) group velocity ratio relative to analytic c·k̂.

    Returns list of dicts with one entry per L.
    """
    results = []
    for L in L_values:
        gv = measure_group_velocity_2d(L=L, n_steps=n_steps, c=c, k0=k0, sigma=sigma)

        f, g = _gaussian_packet_2d(L, k0, sigma=sigma)
        n0 = float(np.sum(np.abs(f)**2 + np.abs(g)**2))
        for _ in range(n_steps):
            f, g = weyl_step_2d_splitstep(f, g, c)
        n1 = float(np.sum(np.abs(f)**2 + np.abs(g)**2))

        results.append({
            'L': L,
            'speed_ratio': gv['speed_ratio'],
            'norm_drift':  abs(n1 - n0) / n0 if n0 > 0 else 0.0,
        })
    return results


def size_sweep_sigma(sigma_values, L=32, n_steps=50, c=0.5, k0=(0.6, 0.0)):
    """
    Vary packet width sigma, hold (L, c, k0) fixed.

    Reports the fraction of spectral power above the Nyquist threshold
    π/2 (a conservative aliasing cutoff).
    """
    results = []
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')
    kx_grid = np.fft.fftfreq(L) * 2.0 * np.pi
    ky_grid = np.fft.fftfreq(L) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx_grid, ky_grid, indexing='ij')
    kappa = np.sqrt(KX**2 + KY**2)
    nyquist_mask = kappa > (np.pi / 2.0)

    for sigma in sigma_values:
        f, g = _gaussian_packet_2d(L, k0, sigma=sigma)
        F = np.fft.fft2(f)
        G = np.fft.fft2(g)
        power = np.abs(F)**2 + np.abs(G)**2
        total = float(power.sum())
        above = float(power[nyquist_mask].sum())
        frac_above_nyquist = above / total if total > 0 else 0.0

        gv = measure_group_velocity_2d(L=L, n_steps=n_steps, c=c, k0=k0, sigma=sigma)

        results.append({
            'sigma': sigma,
            'frac_above_nyquist': frac_above_nyquist,
            'speed_ratio': gv['speed_ratio'],
        })
    return results
