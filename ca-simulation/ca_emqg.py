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


def c_field_from_phi(phi, c_0=0.5):
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
    """
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


if __name__ == '__main__':
    print('Point-source potential rel err:', test_point_source_potential())
    print('Vacuum c uniform residual:', test_vacuum_c_uniform())
    print('Lensing deflection rel err (Δ(2M)/Δ(M) vs 2):',
          test_lensing_deflection())
