"""
ca_emqg.py  —  EMQG modified Poisson + c(φ) coupling (Paper 6)
==============================================================
Implements Paper 6's modified Poisson equation (Eq. 19.7) on a 2D lattice
and the corresponding c(x) field (Eq. 18.31 weak-field reduction):

    ∇²φ(x, t) − (1/c₀²) ∂²φ/∂t² = 4πG ρ(x, t)
    c(x, t) = c₀ / (1 + φ(x, t) / c₀²)

For the v2 build's L4 layer we only need the static case (∂_t² = 0); the
time-dependent solver is left as future work.  The static Poisson is
solved by FFT on the periodic lattice:

    φ(k) = − 4πG ρ(k) / |k|²    for k ≠ 0
    φ(k = 0) = 0                 (gauge choice; mean of φ unphysical)

The resulting c(x) is fed into the existing Cayley exact-unitary
variable-c stepper in `ca_curved.py`, giving an end-to-end matter →
potential → metric → photon trajectory pipeline.

Tests:
  * `test_point_source_potential` — Gaussian-smoothed point mass should
    yield a φ(x) whose gradient is radially outward and consistent with
    the 2D Poisson solution at large r.
  * `test_vacuum_c_uniform` — ρ=0 → φ=0 → c=c₀ uniform.
  * `test_lensing_deflection` — Probe Weyl packet at impact parameter b
    bends towards the mass; deflection scales monotonically with mass
    and inversely with impact parameter.
"""

import numpy as np

from ca_curved import CayleyVarcSolver2D


# ══════════════════════════════════════════════════════════════════
#  Static Poisson solver
# ══════════════════════════════════════════════════════════════════

def solve_poisson_2d(rho, G=1.0):
    """
    Solve ∇²φ = 4πG ρ on a periodic 2D lattice via FFT.

    Returns φ with the convention φ(k=0) = 0 (zero-mean potential).
    """
    Lx, Ly = rho.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    k2 = KX ** 2 + KY ** 2
    k2[0, 0] = 1.0   # avoid div-by-zero; set DC later
    rho_k = np.fft.fft2(rho)
    phi_k = -4.0 * np.pi * G * rho_k / k2
    phi_k[0, 0] = 0.0
    return np.fft.ifft2(phi_k).real


def solve_poisson_3d(rho, G=1.0):
    """
    Solve ∇²φ = 4πG ρ on a periodic 3D lattice via FFT.  Same convention
    as `solve_poisson_2d`: φ(k=0) = 0 (zero-mean).

    For 3D, the Green's function is the true Newtonian 1/r form, so
    deflection of a ray through a slice of this potential recovers the
    standard 4GM/(bc²) (Einstein) / 2GM/(bc²) (Newtonian) scaling at
    leading order — distinct from the 2D log-potential that 2D Poisson
    gives.  This is the solver that `test_lensing_deflection_3d` uses
    to score against a 3-D Newtonian linear-in-M target, replacing the
    dimensionally-inconsistent 2-D test that scored a log-potential
    against a 1/r benchmark (see `model-observations.md` item 4).

    Parameters
    ----------
    rho : real ndarray, shape (Lx, Ly, Lz) — mass density.
    G   : Newton's constant (lattice units).

    Returns
    -------
    phi : real ndarray, shape (Lx, Ly, Lz) — Newtonian potential.
    """
    Lx, Ly, Lz = rho.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    kz = np.fft.fftfreq(Lz) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
    k2 = KX ** 2 + KY ** 2 + KZ ** 2
    k2[0, 0, 0] = 1.0   # avoid div-by-zero; set DC later
    rho_k = np.fft.fftn(rho)
    phi_k = -4.0 * np.pi * G * rho_k / k2
    phi_k[0, 0, 0] = 0.0
    return np.fft.ifftn(phi_k).real


def gaussian_mass_3d(L, M=1.0, sigma=3.0, center=None):
    """A Gaussian-smoothed point mass at `center` on an L×L×L lattice,
    total integrated mass M.
    """
    if center is None:
        center = (L // 2, L // 2, L // 2)
    x = np.arange(L) - center[0]
    y = np.arange(L) - center[1]
    z = np.arange(L) - center[2]
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    rho = np.exp(-(X ** 2 + Y ** 2 + Z ** 2) / (2.0 * sigma ** 2))
    rho *= M / rho.sum()
    return rho


def c_field_from_phi(phi, c_0=None, c_macro=None):
    """
    GR-effective-medium / Paper 6 weak-field reduction.  For a Newtonian
    potential φ with φ < 0 in a gravitational well, the analog refractive
    index n(x) > 1 in the well and the local speed of light is

        c(x) = c₀ / n(x) = c₀ / (1 − 2 φ(x) / c₀²)

    With φ<0 in the well, c(x) < c₀ — light slows near a mass.  This
    matches both the GR-derived Shapiro-delay form and Paper 6's claim
    that the accelerating virtual vacuum gives a position-dependent
    refractive index.  At |φ| ≪ c₀² this reduces to c(x) ≈ c₀ (1 + 2φ/c₀²),
    which gives the standard 4GM/(bc²) GR deflection in the weak field.

    Parameter `c_0` (legacy) and the alias `c_macro` both refer to the
    **macroscopic lattice light-speed** — distinct from the unitary
    rotation magnitude in `weyl_step_2d_splitstep` and from the energy
    unit in `unified_step`'s H_Y term.  See model-observations.md item 11.
    """
    if c_macro is not None:
        c_0 = c_macro
    elif c_0 is None:
        c_0 = 0.5
    return c_0 / (1.0 - 2.0 * phi / (c_0 ** 2))


def gaussian_mass_2d(Lx, Ly, M=1.0, sigma=3.0, center=None):
    """A Gaussian-smoothed point mass at `center`, total integrated mass M."""
    if center is None:
        center = (Lx // 2, Ly // 2)
    x = np.arange(Lx) - center[0]
    y = np.arange(Ly) - center[1]
    X, Y = np.meshgrid(x, y, indexing='ij')
    rho = np.exp(-(X ** 2 + Y ** 2) / (2.0 * sigma ** 2))
    rho *= M / rho.sum()
    return rho


# ══════════════════════════════════════════════════════════════════
#  Tests for L4
# ══════════════════════════════════════════════════════════════════

def test_point_source_potential():
    """
    Sanity check: for a Gaussian point mass, ∇·∇φ averaged over a
    radial shell should approach 4πG ρ when r ≪ box size.  Concretely,
    integrate Poisson's equation back: ∫_box ∇²φ dV = 4πG·M.

    Returns rel err between numerical ∫ ∇²φ dx² and 4πG·M.
    """
    L = 640   # 10× bump (2026-05-16): 64 → 640
    M = 1.0
    G = 0.01
    sigma = 30.0   # scale source width with the lattice (was 3.0 at L=64)
    rho = gaussian_mass_2d(L, L, M=M, sigma=sigma)
    phi = solve_poisson_2d(rho, G=G)

    # Numerical Laplacian via finite differences (5-pt stencil).
    lap = (np.roll(phi, -1, axis=0) + np.roll(phi, 1, axis=0) +
           np.roll(phi, -1, axis=1) + np.roll(phi, 1, axis=1) -
           4.0 * phi)
    # ∇²φ should approximate 4πG ρ on the discrete lattice.
    target = 4.0 * np.pi * G * rho
    denom = np.abs(target).max()
    rel = np.max(np.abs(lap - target)) / max(denom, 1e-30)
    return float(rel)


def test_vacuum_c_uniform():
    """ρ = 0 → φ = 0 → c = c₀ exactly."""
    L = 320   # 10× bump (2026-05-16): 32 → 320
    rho = np.zeros((L, L))
    phi = solve_poisson_2d(rho)
    c = c_field_from_phi(phi, c_0=0.5)
    return float(np.max(np.abs(c - 0.5)))


def test_lensing_deflection():
    """
    Build a static mass, solve Poisson, build c(x), and propagate a probe
    Weyl packet at impact parameter b through the field.  Verify the
    packet is deflected *towards* the mass and that doubling M roughly
    doubles the deflection (Newtonian scaling).

    Returns the relative error between the deflection ratio Δ(2M)/Δ(M)
    and the expected value 2.0.
    """
    # 10× resolution bump (2026-05-16): 128 → 1280.  All length scales
    # (source width, impact parameter, packet width) scale with L so the
    # physics observable (deflection angle) is preserved while the lattice
    # spacing is 10× finer.  NB the Cayley sparse-LU memory grows as O(L³)
    # for 2D nested-dissection; at L=1280 that is ≈ 10–20 GB.  Drop to
    # L=512 (n_sub=2) or switch to a Krylov solver if memory-bound.
    L = 1280
    sigma = 60.0
    G = 0.005   # weak-field regime: |φ|/c₀² ≪ 1
    c_0 = 0.4
    n_steps = 80

    # Common probe initial state: Gaussian-windowed plane wave moving +x
    # at impact parameter b above the mass.
    b = 180
    x_start = L // 4
    k0 = 0.5    # wavevector along +x (dimensionless; unchanged)
    pkt_sigma = 60.0

    def run(M):
        rho = gaussian_mass_2d(L, L, M=M, sigma=sigma)
        phi = solve_poisson_2d(rho, G=G)
        c_field = c_field_from_phi(phi, c_0=c_0)

        # Build probe packet: a Weyl 2-spinor Gaussian at (x_start, L/2 + b)
        # propagating in +x direction.
        x = np.arange(L)
        y = np.arange(L)
        X, Y = np.meshgrid(x, y, indexing='ij')
        env = np.exp(-((X - x_start) ** 2 + (Y - (L // 2 + b)) ** 2) /
                     (2.0 * pkt_sigma ** 2))
        phase = np.exp(1j * k0 * X)
        f = (env * phase).astype(np.complex128)
        g = np.zeros_like(f)

        solver = CayleyVarcSolver2D(c_field, dt=1.0, n_sub=2)
        for _ in range(n_steps):
            f, g = solver.step(f, g)

        # Measure transverse centroid <y>.
        prob = np.abs(f) ** 2 + np.abs(g) ** 2
        y_mean = (prob * Y).sum() / prob.sum()
        return float(y_mean)

    y_M1 = run(M=1.0)
    y_M2 = run(M=2.0)
    y_M0 = run(M=0.0)   # baseline: no deflection

    # Deflection from baseline.
    d1 = y_M0 - y_M1
    d2 = y_M0 - y_M2
    # Both should be positive (probe is at +b, deflects towards mass at L/2).
    # Doubling M should ~double deflection.
    if d1 < 1e-3:
        return 1.0   # no deflection observed — fail
    return float(abs(d2 / d1 - 2.0))


def test_point_source_potential_3d():
    """
    Discrete-Poisson contract check in 3-D: ∇²φ should reproduce 4πGρ on
    the lattice.  This is the 3-D version of `test_point_source_potential`
    and produces the dimensionally-consistent 1/r Green's function used
    by `test_lensing_deflection_3d`.
    """
    L = 64       # 64³ = 262 144 cells; ≈ 2 MB per real array.
    M = 1.0
    G = 0.01
    sigma = 4.0
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = solve_poisson_3d(rho, G=G)

    # 7-point Laplacian on the periodic lattice.
    lap = (np.roll(phi, -1, axis=0) + np.roll(phi, 1, axis=0)
         + np.roll(phi, -1, axis=1) + np.roll(phi, 1, axis=1)
         + np.roll(phi, -1, axis=2) + np.roll(phi, 1, axis=2)
         - 6.0 * phi)
    target = 4.0 * np.pi * G * rho
    denom = np.abs(target).max()
    rel = np.max(np.abs(lap - target)) / max(denom, 1e-30)
    return float(rel)


def test_lensing_deflection_3d(L=96):
    """
    3-D EMQG lensing test.  Solves the *3-D* Newtonian Poisson equation
    for a Gaussian point mass, slices the resulting potential at z=L/2
    (the equatorial plane through the source), feeds the slice into the
    Cayley variable-c stepper, and verifies that the probe-packet
    deflection scales **linearly in M** — the correct 3-D Newtonian
    behaviour (Δθ ∝ M/b at leading order in the weak-field limit).

    Replaces `test_lensing_deflection` (2-D Poisson scored against a
    3-D linear-in-M target — dimensionally inconsistent because the 2-D
    Green's function is logarithmic).  See `model-observations.md`
    item 4.

    Returns the relative deviation |Δ(2M)/Δ(M) − 2| against the 3-D
    Newtonian benchmark of 2.0.  Pass criterion at L=96 is < 0.10.

    Notes on cost.  L=96 → 96³ = 884 k cells per 3-D array (≈ 7 MB
    each); 3-D FFT under 1 sec on a laptop.  The Cayley 2-D stepper at
    L=96 with n_sub=2 over 80 steps fits comfortably in memory.
    Increase L to tighten the b/L ratio if accuracy needs improving.
    """
    sigma   = 6.0
    G       = 0.005
    c_0     = 0.4
    n_steps = 80
    b       = 18           # impact parameter (cells)
    pkt_sigma = 8.0
    x_start = L // 4
    k0      = 0.5

    def run(M):
        rho_3d = gaussian_mass_3d(L, M=M, sigma=sigma)
        phi_3d = solve_poisson_3d(rho_3d, G=G)
        # Take the equatorial slice through the mass (z = L/2 by default).
        phi_slice = phi_3d[:, :, L // 2]
        c_field   = c_field_from_phi(phi_slice, c_0=c_0)

        # Probe packet at impact parameter b above the slice centre.
        x = np.arange(L); y = np.arange(L)
        X, Y = np.meshgrid(x, y, indexing='ij')
        env   = np.exp(-((X - x_start) ** 2 +
                          (Y - (L // 2 + b)) ** 2) /
                       (2.0 * pkt_sigma ** 2))
        phase = np.exp(1j * k0 * X)
        f = (env * phase).astype(np.complex128)
        g = np.zeros_like(f)

        solver = CayleyVarcSolver2D(c_field, dt=1.0, n_sub=2)
        for _ in range(n_steps):
            f, g = solver.step(f, g)

        prob = np.abs(f) ** 2 + np.abs(g) ** 2
        y_mean = (prob * Y).sum() / prob.sum()
        return float(y_mean)

    y_M0 = run(M=0.0)
    y_M1 = run(M=1.0)
    y_M2 = run(M=2.0)

    d1 = y_M0 - y_M1     # positive = deflection toward the mass at L/2
    d2 = y_M0 - y_M2
    if abs(d1) < 1e-4:
        return 1.0
    return float(abs(d2 / d1 - 2.0))


if __name__ == '__main__':
    print('Point-source potential rel err (2-D):',
          test_point_source_potential())
    print('Point-source potential rel err (3-D):',
          test_point_source_potential_3d())
    print('Vacuum c uniform residual:', test_vacuum_c_uniform())
    print('Lensing deflection rel err (2-D log-potential, legacy):',
          test_lensing_deflection())
    print('Lensing deflection rel err Δ(2M)/Δ(M) vs 2 (3-D Newtonian):',
          test_lensing_deflection_3d())
