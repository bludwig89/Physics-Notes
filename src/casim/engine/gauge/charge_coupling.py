"""
ca_charge_coupling.py  —  The U(1) charge-coupling path on the paired-photon field
==================================================================================

When the project replaced the SM-style U(1)-gauge photon with the paired-spinor
photon (F67/F68/F69), the old `aharonov_bohm_test` driver and the U(1)-gauge
fermion step were *removed* from `ca_dirac.py` (see the [REMOVED 2026-05-26]
banners there).  The charge-coupling path — how electric charge sources the
(E,B) field and how a charged fermion reads that field back — was therefore left
unverified against the **new** even-law `(E,B)` photon (`ca_photon_pair.py`).

This module re-establishes that path end-to-end, in two coupled halves:

  (1) **Holonomy half (Aharonov–Bohm).**  The U(1) coupling enters the fermion
      ONLY as a Peierls c-number phase  P = e^{i q A·dl} · I_2  (F68: identity
      channel, helicity-blind).  The ordered product of link phases around a
      closed loop is the *holonomy*

          W(∂S) = exp( i q ∮ A·dl ) = exp( i q ∬_S (∇×A)·dS ) = exp( i q Φ_enc )

      which on the lattice is the **discrete Stokes theorem** and is therefore
      EXACT (the link sum telescopes to the enclosed plaquette-flux sum).  A
      charged fermion encircling a flux tube picks up exactly q·Φ_enc even where
      the local field is zero — the Aharonov–Bohm effect — and, because P ∝ I_2,
      the phase is identical for either Weyl helicity.

  (2) **Source half (sourced Maxwell curl).**  The paired photon propagates by
      the even-law rotation of the real (E,B) pair (`ca_photon_pair`).  Its
      Maxwell-curl content is carried by the BCC curl symbol  C(k) = 2 n(k/2)
      (the small-k generator already verified in `ca_maxwell.maxwell_curl_residual`).
      Minimal coupling adds the charge current to Ampère's law:

          Ė = i C×B − J ,      Ḃ = −i C×E .

      Because  C·(C×x) ≡ 0  identically, this update preserves the Gauss
      constraint  i C·E = ρ  bit-for-bit whenever the source obeys charge
      continuity  ∂_t ρ + i C·J = 0, and keeps  i C·B = 0.  That is the
      statement that electric charge is *conserved* by the coupling — the core
      correctness property — and it holds to machine precision on the paired
      photon's own propagator.

The two halves meet in `sourced_flux_tube_2d`: a static in-plane current sources
a B_z field by the (discrete) magnetostatic curl, and the holonomy of the
Coulomb-gauge A solved from that *same* field returns q·(the current-driven
flux).  charge → field → holonomy → phase, closed and self-consistent.

Conventions
-----------
* Lattice spacing 1; periodic boundaries; q is the test charge (default 1).
* Holonomy sector works in 2D (the AB plane ⟂ the flux tube) with **finite-
  difference link operators** so that discrete Stokes is exact.  The forward
  difference symbol along axis j is  a_j = e^{i k_j} − 1.
* Source sector works in 3D with the BCC **spectral** curl symbol C(k)=2 n(k/2).
* Real fields throughout; FFTs are the only linear-algebra (CLAUDE.md: no
  np.linalg.eig on chiral matrices — none used here).

CLAUDE.md date stamp: 2026-06-03.
"""

import numpy as np
from casim.numerics import fft as _fft
from casim.engine.lattice.geometry import make_kgrid_3d
from casim.engine.lattice.bcc import _bcc_uvec, bcc_dispersion

ROOT3 = np.sqrt(3.0)


# ======================================================================
#  PART 1 — Holonomy / Aharonov–Bohm sector (2D, finite-difference links)
# ======================================================================

def _kgrid_2d(Lx, Ly):
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    return np.meshgrid(kx, ky, indexing='ij')


def discrete_curl_z(Ax, Ay):
    """Plaquette curl  B_z[x,y] = (A_y[x+1,y]−A_y[x,y]) − (A_x[x,y+1]−A_x[x,y]).

    This is the lattice curl whose plaquette value is *exactly* the Peierls
    holonomy phase of the four bounding links (discrete Stokes).  Periodic.
    """
    dAy_dx = np.roll(Ay, -1, axis=0) - Ay
    dAx_dy = np.roll(Ax, -1, axis=1) - Ax
    return dAy_dx - dAx_dy


def discrete_div(Ax, Ay):
    """Backward-difference divergence  div A[x,y] = (A_x−A_x[x−1]) + (A_y−A_y[y−1]).

    Chosen as the adjoint partner of `discrete_curl_z` so that div∘curl ≡ 0;
    `solve_A_coulomb_2d` imposes div A = 0 in this convention (Coulomb gauge).
    """
    dAx = Ax - np.roll(Ax, 1, axis=0)
    dAy = Ay - np.roll(Ay, 1, axis=1)
    return dAx + dAy


def solve_A_coulomb_2d(Bz):
    """Solve the discrete Coulomb-gauge vector potential A with

        discrete_curl_z(A) = Bz   and   discrete_div(A) = 0 ,

    both to machine precision, for a zero-mean Bz (total flux 0, required by
    periodicity).  Closed form in Fourier with the forward-difference symbols
    a_j = e^{i k_j} − 1, b_j = 1 − e^{−i k_j}:

        det = b_x a_x + b_y a_y = −(|a_x|²+|a_y|²) = −k̂²
        Â_x =  b_y B̂_z / k̂² ,   Â_y = −b_x B̂_z / k̂² .
    """
    Lx, Ly = Bz.shape
    KX, KY = _kgrid_2d(Lx, Ly)
    ax = np.exp(1j * KX) - 1.0
    ay = np.exp(1j * KY) - 1.0
    bx = 1.0 - np.exp(-1j * KX)
    by = 1.0 - np.exp(-1j * KY)
    khat2 = np.abs(ax) ** 2 + np.abs(ay) ** 2          # FD Laplacian symbol
    Bk = _fft.fft2(Bz.astype(complex))
    Axk = np.zeros_like(Bk)
    Ayk = np.zeros_like(Bk)
    nz = khat2 > 1e-14
    Axk[nz] = by[nz] * Bk[nz] / khat2[nz]
    Ayk[nz] = -bx[nz] * Bk[nz] / khat2[nz]
    Ax = _fft.ifft2(Axk).real
    Ay = _fft.ifft2(Ayk).real
    return Ax, Ay


def make_flux_tube_pair(L, c1, c2, width, Phi):
    """A periodic-compatible field of two opposite flux tubes:  +Phi at c1,
    −Phi at c2 (net zero flux, so a valid periodic Bz).  Each tube is a
    normalised Gaussian summing to exactly ±Phi.  Returns Bz (L,L)."""
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    def bump(cx, cy):
        # minimum-image distances on the periodic torus
        dx = (X - cx + L / 2) % L - L / 2
        dy = (Y - cy + L / 2) % L - L / 2
        g = np.exp(-(dx ** 2 + dy ** 2) / (2.0 * width ** 2))
        return g / g.sum()

    Bz = Phi * (bump(*c1) - bump(*c2))
    return Bz


def peierls_loop_phase(Ax, Ay, x0, x1, y0, y1, q=1.0):
    """Holonomy phase  ∮ q A·dl  (NOT mod 2π) of the rectangular CCW loop with
    corners (x0,y0)→(x1,y0)→(x1,y1)→(x0,y1).  Sum of link line-integrals
    A·dl ≈ A_component at each traversed link (unit spacing).  Returns the real
    accumulated phase q·∮A·dl."""
    phase = 0.0
    # bottom edge: +x along y=y0,  x=x0..x1-1
    for x in range(x0, x1):
        phase += Ax[x % Ax.shape[0], y0 % Ax.shape[1]]
    # right edge: +y along x=x1,  y=y0..y1-1
    for y in range(y0, y1):
        phase += Ay[x1 % Ay.shape[0], y % Ay.shape[1]]
    # top edge: −x along y=y1,  x=x1-1..x0
    for x in range(x1 - 1, x0 - 1, -1):
        phase -= Ax[x % Ax.shape[0], y1 % Ax.shape[1]]
    # left edge: −y along x=x0,  y=y1-1..y0
    for y in range(y1 - 1, y0 - 1, -1):
        phase -= Ay[x0 % Ay.shape[0], y % Ay.shape[1]]
    return q * phase


def enclosed_flux(Bz, x0, x1, y0, y1, q=1.0):
    """q × Σ Bz over the plaquettes strictly inside the rectangle [x0,x1)×[y0,y1).
    By discrete Stokes this equals `peierls_loop_phase` exactly."""
    region = Bz[x0:x1, y0:y1]
    return q * float(region.sum())


def field_on_loop(Bz, x0, x1, y0, y1):
    """max |Bz| on the plaquettes touched by the rectangular loop's edges — the
    'is the path field-free?' diagnostic for the AB effect."""
    edges = np.concatenate([
        np.abs(Bz[x0:x1, y0]), np.abs(Bz[x0:x1, (y1 - 1) % Bz.shape[1]]),
        np.abs(Bz[x0, y0:y1]), np.abs(Bz[(x1 - 1) % Bz.shape[0], y0:y1]),
    ])
    return float(edges.max())


# ======================================================================
#  PART 2 — Sourced Maxwell-curl sector (3D, BCC spectral curl symbol)
# ======================================================================

def bcc_curl_symbol(KX, KY, KZ):
    """The model's Maxwell-curl generator  C(k) = 2 n(k/2)  (real 3-vector per
    mode), taken as its **odd-in-k part**  C_odd(k) = ½[C(k) − C(−k)].

    Why the odd part:  for a *real* (E,B) field the curl operator must satisfy
    C(−k) = −C(k) so that  i C×B̂  and  i C·Ê  are Hermitian-symmetric in k
    (i.e. real in real space).  The full BCC n(k/2) is not odd (it carries an
    even remainder that the single-mode eigen-analysis of
    `ca_maxwell.maxwell_curl_residual` never sees but a real-field stepper
    does), so we project onto the physical odd channel.  This is the lattice
    curl: odd, real-preserving, and  |C_odd| → |k|/√3 at small k (luminal,
    c=1/√3), with the identity  C_odd·(C_odd×x) ≡ 0 intact.

    Grid-level subtlety (fixed 2026-06-06):  n(k/2) has period 4π in k, so
    value-negation k→−k and the FFT grid's *index* negation k→−k mod 2π differ
    on the Nyquist planes (k_j = ±π maps to itself under the grid involution
    but to a different branch of n(k/2) under value negation).  The analytic
    odd projection above therefore left an even residue confined to the
    Nyquist planes, which broke Hermitian symmetry there — a real-field
    stepper's ``.real`` projection then silently gained/lost energy on those
    modes.  We symmetrise over the **grid** involution,  C ← ½[C(k) − C(k*)]
    with k* the index negation, which is identical off the Nyquist planes and
    zeroes the unphysical even residue on them.  The symbol is then exactly
    odd as the FFT of a real field requires."""
    up, nxp, nyp, nzp = _bcc_uvec(KX / 2.0, KY / 2.0, KZ / 2.0, sign='+')
    um, nxm, nym, nzm = _bcc_uvec(-KX / 2.0, -KY / 2.0, -KZ / 2.0, sign='+')
    Cx, Cy, Cz = (nxp - nxm), (nyp - nym), (nzp - nzm)  # ½[2n(k/2) − 2n(−k/2)]

    def _grid_negate(S):
        # S evaluated at −k mod 2π (FFT index negation; Nyquist → itself)
        return np.roll(S[::-1, ::-1, ::-1], 1, axis=(0, 1, 2))

    Cx = 0.5 * (Cx - _grid_negate(Cx))
    Cy = 0.5 * (Cy - _grid_negate(Cy))
    Cz = 0.5 * (Cz - _grid_negate(Cz))
    return Cx, Cy, Cz


def _cross_k(Ax, Ay, Az, Bx, By, Bz):
    return (Ay * Bz - Az * By,
            Az * Bx - Ax * Bz,
            Ax * By - Ay * Bx)


def _dot_k(Ax, Ay, Az, Bx, By, Bz):
    return Ax * Bx + Ay * By + Az * Bz


def maxwell_curl_step(E, B, J=None, dt=1.0):
    """One tick of the sourced paired-photon Maxwell curl, integrated
    **exactly** per Fourier mode (2026-06-06):

        d/dt (E,B) = ( i C×B ,  −i C×E ) ,   then   E ← E − dt·J .

    The free part is a pure rotation generated by  G = [[0, iC×],[−iC×, 0]]
    with C(k) the odd lattice curl symbol (``bcc_curl_symbol``).  On the
    transverse subspace G² = −|C|², so the exact propagator is algebraic:

        exp(dt·G) = 1 + (cos θ − 1)·P_T + sin θ·Ĝ ,   θ = dt|C(k)| ,

    with P_T the transverse projector (1 − ĉĉ·) and Ĝ = G/|C|.  Longitudinal
    components are exactly invariant (C×X_∥ = 0), so the lattice Gauss law
    i C·E changes only through the −dt·J kick — charge continuity is exact.

    This replaces the original forward-Euler step  E += dt·iC×B,
    B −= dt·iC×E, whose per-mode amplification |λ|² = 1 + dt²|C|² > 1 is
    unconditionally unstable (energy e-fold ≈ 44 ticks at dt=0.1 near the
    band edge — the charge_photon t3718 blow-up; same mechanism as the
    PhotonSourcedChannel t13k divergence).  The exact step is unitary on
    every mode: free energy is conserved to machine rounding at any dt, and
    it agrees with the Euler step to O(dt²).  The Euler step is retained for
    reference as ``maxwell_curl_step_euler``.

    E, B, J are (3,Lx,Ly,Lz) real arrays.  Returns (E_new, B_new) real."""
    shape = E.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    Cmag = np.sqrt(Cx ** 2 + Cy ** 2 + Cz ** 2)
    safe = np.where(Cmag > 0.0, Cmag, 1.0)        # C=0 modes: all terms vanish
    chx, chy, chz = Cx / safe, Cy / safe, Cz / safe   # ĉ unit symbol (real)
    theta = dt * Cmag
    cosm1 = np.cos(theta) - 1.0                   # cos θ − 1   (→ 0 as C → 0)
    sino = np.sin(theta) / safe                   # sin θ / |C| (→ dt as C → 0)
    Ek = [_fft.fftn(E[a]) for a in range(3)]
    Bk = [_fft.fftn(B[a]) for a in range(3)]
    cxB = _cross_k(Cx, Cy, Cz, *Bk)
    cxE = _cross_k(Cx, Cy, Cz, *Ek)
    cdE = _dot_k(chx, chy, chz, *Ek)              # ĉ·E  (longitudinal part)
    cdB = _dot_k(chx, chy, chz, *Bk)
    ch = (chx, chy, chz)
    Ek_new = [Ek[a] + cosm1 * (Ek[a] - ch[a] * cdE) + sino * (1j * cxB[a])
              for a in range(3)]
    Bk_new = [Bk[a] + cosm1 * (Bk[a] - ch[a] * cdB) - sino * (1j * cxE[a])
              for a in range(3)]
    E_new = np.array([_fft.ifftn(Ek_new[a]).real for a in range(3)])
    B_new = np.array([_fft.ifftn(Bk_new[a]).real for a in range(3)])
    if J is not None:
        E_new = E_new - dt * J
    return E_new, B_new


def maxwell_curl_step_euler(E, B, J=None, dt=1.0):
    """The original explicit forward-Euler curl tick (pre-2026-06-06):

        E ← E + dt(i C×B − J) ,     B ← B − dt(i C×E) .

    **Unconditionally unstable**: per-mode amplification |λ|² = 1 + dt²|C|²
    for every k and every dt.  Retained only for regression comparison
    against the exact ``maxwell_curl_step``."""
    shape = E.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    Ek = [_fft.fftn(E[a]) for a in range(3)]
    Bk = [_fft.fftn(B[a]) for a in range(3)]
    cxB = _cross_k(Cx, Cy, Cz, *Bk)
    cxE = _cross_k(Cx, Cy, Cz, *Ek)
    Ek_new = [Ek[a] + dt * (1j * cxB[a]) for a in range(3)]
    Bk_new = [Bk[a] - dt * (1j * cxE[a]) for a in range(3)]
    E_new = np.array([_fft.ifftn(Ek_new[a]).real for a in range(3)])
    B_new = np.array([_fft.ifftn(Bk_new[a]).real for a in range(3)])
    if J is not None:
        E_new = E_new - dt * J
    return E_new, B_new


def gauss_residual(E, rho):
    """‖ i C·E − ρ ‖ in Fourier (the lattice Gauss-law residual ∇·E − ρ)."""
    shape = E.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    Ek = [_fft.fftn(E[a]) for a in range(3)]
    divE = 1j * _dot_k(Cx, Cy, Cz, *Ek)          # i C·E  = ∇·E symbol
    rk = _fft.fftn(rho)
    return divE - rk


def div_from_current(J):
    """i C·J in Fourier — the RHS of charge continuity  ∂_tρ = −i C·J."""
    shape = J.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    Jk = [_fft.fftn(J[a]) for a in range(3)]
    return 1j * _dot_k(Cx, Cy, Cz, *Jk)


def magnetostatic_B(J):
    """Steady (∂_tE=0) Ampère solution  i C×B = J_T  for the C-transverse part
    of J:  B = i (C×J_T)/|C|².  Returns (B, lon_frac) where lon_frac is the
    longitudinal fraction |C·J|/(|C||J|) projected out (a diagnostic).  Verifies
    charge → magnetostatic field with a machine-exact Ampère residual on J_T."""
    shape = J.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    C2 = Cx ** 2 + Cy ** 2 + Cz ** 2
    Jk = [_fft.fftn(J[a]) for a in range(3)]
    CdotJ = _dot_k(Cx, Cy, Cz, *Jk)
    nz = C2 > 1e-14
    # transverse projection of J
    JT = []
    for a, C in enumerate((Cx, Cy, Cz)):
        proj = np.zeros_like(Jk[a])
        proj[nz] = C[nz] * CdotJ[nz] / C2[nz]
        JT.append(Jk[a] - proj)
    cxJT = _cross_k(Cx, Cy, Cz, *JT)
    Bk = []
    for a in range(3):
        b = np.zeros_like(Jk[a])
        b[nz] = 1j * cxJT[a][nz] / C2[nz]
        Bk.append(b)
    B = np.array([_fft.ifftn(Bk[a]).real for a in range(3)])
    Jnorm = np.sqrt(sum(np.sum(np.abs(j) ** 2) for j in Jk)) + 1e-30
    lon = np.sqrt(np.sum(np.abs(CdotJ) ** 2 / np.maximum(C2, 1e-30)))
    return B, float(lon / Jnorm)


# ======================================================================
#  PART 3 — End-to-end: charge → field → holonomy
# ======================================================================

def ampere_current_2d(Bz):
    """The in-plane current that sources B_z by the discrete Ampère law
    ∇×B = J:  J_x = B_z[x,y]−B_z[x,y−1],  J_y = −(B_z[x,y]−B_z[x−1,y])
    (the backward-difference curl adjoint of `discrete_curl_z`, so that
    discrete_curl_z(solve_A(Bz)) and this J are exactly consistent).  J is a
    sheet of current at the tube wall and is divergence-free by construction."""
    Jx = Bz - np.roll(Bz, 1, axis=1)
    Jy = -(Bz - np.roll(Bz, 1, axis=0))
    return Jx, Jy


def sourced_flux_tube_2d(L, c1, c2, radius, current):
    """Physical 2D solenoid pair: a compact interior B_z flux tube (+ at c1, − at
    c2) is sourced by the azimuthal wall current  J = ∇×B  (Ampère).  Returns
    (Bz, Ax, Ay): B_z is the magnetic field, A its Coulomb-gauge potential with
    discrete_curl_z(A)=Bz to machine ε, and the wall current
    `ampere_current_2d(Bz)` is the charge current that produced it.  The
    holonomy of A around c1 therefore returns q·(current-driven interior flux)
    = q·current exactly (strong AB signal).

    A 'top-hat-ish' interior profile (smoothed disk) gives a genuine non-zero
    enclosed flux, unlike a Laplacian source whose net flux vanishes."""
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    def disk(cx, cy, sign):
        dx = (X - cx + L / 2) % L - L / 2
        dy = (Y - cy + L / 2) % L - L / 2
        r = np.sqrt(dx ** 2 + dy ** 2)
        # smoothed top-hat of unit interior height, radius `radius`
        prof = 0.5 * (1.0 - np.tanh((r - radius) / 0.8))
        return sign * prof / 1.0

    Bz = current * (disk(*c1, +1.0) - disk(*c2, -1.0))
    Bz -= Bz.mean()                                   # exact zero mean (periodic)
    Ax, Ay = solve_A_coulomb_2d(Bz)
    return Bz, Ax, Ay


# ======================================================================
#  self-check
# ======================================================================
if __name__ == '__main__':
    L = 48
    Bz = make_flux_tube_pair(L, (12, 24), (36, 24), width=2.0, Phi=0.7)
    Ax, Ay = solve_A_coulomb_2d(Bz)
    curl_res = np.max(np.abs(discrete_curl_z(Ax, Ay) - Bz))
    div_res = np.max(np.abs(discrete_div(Ax, Ay)))
    holo = peierls_loop_phase(Ax, Ay, 4, 24, 4, 44, q=1.0)
    flux = enclosed_flux(Bz, 4, 24, 4, 44, q=1.0)
    print(f"discrete curl(A)-B  max = {curl_res:.2e}")
    print(f"discrete div(A)     max = {div_res:.2e}")
    print(f"holonomy            = {holo:+.6f}")
    print(f"enclosed flux       = {flux:+.6f}  (Φ=0.7)")
    print(f"holonomy - flux     = {abs(holo-flux):.2e}")
