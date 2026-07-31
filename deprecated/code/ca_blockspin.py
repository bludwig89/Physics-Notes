# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_blockspin.py
# migrated   : 2026-07-30 - 13:53
# target     : src/casim/engine/lattice/blockspin.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_blockspin.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_blockspin.py — Phase-1 block-spin / coarse-graining RG scheme (F130)
========================================================================

`2026-06-11 - 04:17`

Phase 1 of `docs/roadmaps/roadmap-scale-to-real-space.md`: a renormalisation-
group (block-spin) transformation R_b that groups b^d fine cells into one
super-cell and is PROVED to preserve the rotation rule's physical content, so a
coarse simulation of N super-cells faithfully represents a patch of (bN)^d
physical cells.  Without it every later phase is a bigger toy, not a smaller
universe.

This module is the **gauge + gravity** half of F130 (the free-photon sector is
F129, a concurrent push).  It imports the free-photon dispersion as a read-only
dependency (`ca_photon_pair.pair_dispersion`, the even law
`ca_wmu._f26_rotation_step`) and does NOT re-derive it.

What R_b is
-----------
Kadanoff block average.  For a periodic field f on a fine lattice (spacing 1):

    (R_b f)(X) = b^{-d} Σ_{r ∈ [0,b)^d} f(b·X + r)             [scalars / EM field]

Electric flux (a 1-form) blocks by SUM across the coarse face, not average —
the Migdal-Kadanoff bond-moving rule — so Gauss's law telescopes (gauge sector).
The gravity dielectric blocks in its LOG variable u = ½ ln K, the linear Poisson
potential, so the reciprocal lock A·B = 1 is preserved pointwise (gravity sector).

The dispersion is a property of the rule, not the field: blocking attenuates mode
amplitudes by a real, helicity-blind form factor D_b(k) (≤1, =1 at k=0) and
rescales the Brillouin zone by b.  The coarse rule in coarse units is therefore

    Ω_coarse(κ) = Ω(κ / b),      κ ∈ coarse BZ = (−π, π]^d.

Theorems (all to algebraic exactness, verified to machine precision in
`tests/findings/test_F130_blockspin_gauge_gravity.py`)
------------------------------------------------------------------------------
T1  c_lat is an RG fixed point.  Physical speed  c_phys = (b/τ)·dΩ_coarse/dκ|₀
    = (b/τ)·(1/b)·dΩ/dk|₀ = c/τ  for every b — exactly invariant.
T2  Lattice-artifact (LIV) operators are irrelevant.  Writing v(q)/c =
    1 + Σ_{n≥2} g_n (q·spacing)^n, the coarse coupling is g_n^(b) = b^{-n} g_n,
    RG eigenvalue λ_n = b^{-n} < 1.  The leading even-law operator (F30, body
    diagonal) is g_2 = −1/162 in the Ω-form (δv_g/c = −k²/54); its eigenvalue is
    exactly b^{-2}.  The continuum law Ω = c|k| is the attractive IR fixed point.
    (In the roadmap's Ω-power index m = n+1 this reads b^{1-m}, m ≥ 2 — same.)
T3a Gauss law survives blocking.  With the electric field blocked as coarse-face
    flux-sums and charge blocked as block-sums, div_coarse E_coarse = R_b(div E)
    = enclosed charge — the discrete divergence theorem, integer-exact.
T3b The gravity dielectric survives blocking.  Averaging u = ½ ln K keeps
    A·B ≡ 1 exactly (e^{-2ū}·e^{+2ū} = 1); averaging K directly breaks it by the
    Jensen variance gap ⟨1/K⟩⟨K⟩ − 1 ≥ 0.  The linear Poisson source law is form-
    invariant under R_b.
T3c Propagator class is preserved.  D_b(k) is a real scalar per mode, so it
    commutes with the even (real 2×2) rotation and cannot mix the F91 even/chiral
    classes:  [R_b, R(Ω)] = 0 to machine precision.
C1  Confinement is the ONE relevant direction.  The string tension is the static
    potential slope; in the strong-coupling (confined) phase σ̂ = g²/2 exactly
    (F110, λ=0).  Bond-moving b parallel fine links into one coarse link gives
    g²_coarse = b·g²_fine, so σ̂_coarse = b·σ̂_fine — RG eigenvalue λ_σ = b > 1
    (relevant), the lone IR scale, in contrast to the irrelevant LIV operators
    (b^{-n}).  The physical confining energy V(R_phys)=σ_phys·R_phys is invariant:
    a coarse F110 run on b× fewer plaquettes reproduces the fine V(b·R) exactly.
    The magnetic coupling λ only deforms σ̂ by a fraction r(λ) ∝ λ²/g⁴ that
    *shrinks* as b^{-2} under blocking, so the λ=0 area law is IR-attractive (the
    deconfining perturbation is irrelevant, like the leading LIV operator).

Pure numpy for the field/dispersion/gravity sectors (no np.linalg.eig on chiral
matrices, CLAUDE.md caveat).  The confinement helpers wrap the audited F110
Kogut–Susskind solver (`ca_link_hamiltonian`, which uses scipy.sparse) read-only.
"""
from __future__ import annotations

import numpy as np

# Read-only dependencies (we consume, never re-derive, the free-photon law)
from ca_bcc import bcc_dispersion
from ca_photon_pair import pair_dispersion
import ca_gravity as _grav
from casim.constants import c_lat
import ca_fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

C_LAT = c_lat                       # F26 BCC rotation rate (lattice units)

__all__ = [
    "C_LAT",
    # block kernel
    "block_average", "block_kernel_factor", "box_blur_fourier",
    # dispersion RG
    "coarse_dispersion", "fit_dispersion_coeffs", "extract_speed",
    "extract_leading_liv", "rg_eigenvalue",
    # theorem checks
    "c_lat_fixed_point", "liv_irrelevance",
    # gauge sector
    "lattice_divergence", "coarse_face_flux", "block_charge",
    "gauss_law_residual",
    # gravity sector
    "coarse_grain_u", "dielectric_from_u", "reciprocal_lock_residual",
    "dielectric_jensen_gap", "poisson_form_invariance_residual",
    # propagator class
    "even_rotation_commutator",
    # confinement sector (C1)
    "string_tension_lambda0", "confinement_rg_step", "confinement_eigenvalue",
    "coarse_static_potential", "magnetic_deformation_ratio",
    "BODY_DIAGONAL", "FACE_DIAGONAL", "AXIS",
]

# Canonical sampling directions (unit vectors).  The even-law LIV correction is
# anisotropic (F30): identically zero along a cubic axis, maximal (−1/162) along
# the body diagonal.
AXIS = np.array([1.0, 0.0, 0.0])
FACE_DIAGONAL = np.array([1.0, 1.0, 0.0]) / np.sqrt(2.0)
BODY_DIAGONAL = np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0)


# ══════════════════════════════════════════════════════════════════
#  Block kernel R_b  (Kadanoff average + its Fourier form factor)
# ══════════════════════════════════════════════════════════════════
def block_average(field, b):
    """R_b f : average b^d disjoint fine cells into one coarse cell.

    `field` is a real array of shape (L,)*d with L % b == 0.  Returns the
    coarse field of shape (L/b,)*d.  This is the EM / scalar blocking rule.
    """
    f = np.asarray(field, dtype=np.float64)
    d = f.ndim
    L = f.shape[0]
    assert all(s == L for s in f.shape), "field must be a cube"
    assert L % b == 0, f"L={L} not divisible by b={b}"
    Lc = L // b
    # reshape each axis into (Lc, b) then mean over the b sub-axes
    new_shape = []
    for _ in range(d):
        new_shape += [Lc, b]
    g = f.reshape(new_shape)
    mean_axes = tuple(range(1, 2 * d, 2))
    return g.mean(axis=mean_axes)


def block_kernel_factor(k, b):
    """1-D Fourier multiplier of the centred b-cell box average.

    D_b(k) = sin(b k / 2) / (b sin(k / 2)),  D_b(0) = 1.  Real, even, ≤ 1.
    Helicity-blind (a scalar), which is why R_b cannot mix the F91 even/chiral
    propagator classes (T3c).
    """
    k = np.asarray(k, dtype=np.float64)
    num = np.sin(b * k / 2.0)
    den = b * np.sin(k / 2.0)
    out = np.where(np.abs(den) < 1e-300, 1.0, num / np.where(den == 0, 1.0, den))
    # exact DC limit
    out = np.where(np.abs(k) < 1e-12, 1.0, out)
    return out


def box_blur_fourier(field_k, b):
    """Apply the same-grid box-blur multiplier ∏_i D_b(k_i) in Fourier space.

    `field_k` is the FFT of a real (L,)*d field (numpy fft convention).  Used by
    the propagator-commutation check; stays on the fine grid (no decimation), so
    it is a pure per-mode real scalar.
    """
    fk = np.asarray(field_k)
    d = fk.ndim
    L = fk.shape[0]
    kvec = np.fft.fftfreq(L) * 2.0 * np.pi
    fac = np.ones_like(fk, dtype=np.float64)
    grids = np.meshgrid(*([kvec] * d), indexing="ij")
    for K in grids:
        fac = fac * block_kernel_factor(K, b)
    return fk * fac


# ══════════════════════════════════════════════════════════════════
#  Dispersion RG
# ══════════════════════════════════════════════════════════════════
def coarse_dispersion(kappa_vec, b, disp=pair_dispersion):
    """Renormalised coarse rule Ω_coarse(κ) = Ω(κ / b).

    `kappa_vec` is (kx, ky, kz) in COARSE lattice units (coarse spacing = b).
    The /b rescale is what keeps the physical speed fixed (T1).
    """
    kx, ky, kz = kappa_vec
    return disp(kx / b, ky / b, kz / b)


def _disp_along(direction, kmag, b=1, disp=pair_dispersion):
    """Ω_coarse at coarse |κ| = kmag along `direction` (unit vector)."""
    d = np.asarray(direction, dtype=np.float64)
    d = d / np.linalg.norm(d)
    kappa = d * kmag
    return coarse_dispersion(kappa, b, disp=disp)


def fit_dispersion_coeffs(direction, b=1, disp=pair_dispersion,
                          kmax=0.30, n=24, n_even=3):
    """Least-squares fit  Ω/|κ| = c (1 + g2 κ² + g4 κ⁴ + …)  along `direction`.

    Returns (c, g2, g4, …) with `n_even` even coefficients.  Sampling avoids the
    arccos round-off floor near κ=0 (the dispersion is flat-to-round-off on a
    cubic axis); a moderate window [kmax/n, kmax] resolves c to ~1e-12 and the
    leading LIV coefficient cleanly.
    """
    kk = np.linspace(kmax / n, kmax, n)
    yy = np.array([_disp_along(direction, k, b=b, disp=disp) / k for k in kk])
    # design matrix in powers κ^{0,2,4,...}
    cols = [kk ** (2 * j) for j in range(n_even)]
    A = np.vstack(cols).T
    coef, *_ = np.linalg.lstsq(A, yy, rcond=None)
    c = coef[0]
    rest = coef[1:] / c               # g_n = coef_n / c
    return (c, *rest)


def extract_speed(direction=BODY_DIAGONAL, b=1, disp=pair_dispersion):
    """Coarse-unit speed c_coarse = dΩ_coarse/d|κ| at κ→0 (= c/b)."""
    return fit_dispersion_coeffs(direction, b=b, disp=disp)[0]


def extract_leading_liv(direction=BODY_DIAGONAL, b=1, disp=pair_dispersion):
    """Leading even-law LIV coefficient g_2 in Ω/|κ| = c(1 + g2 κ² + …)."""
    return fit_dispersion_coeffs(direction, b=b, disp=disp)[1]


def rg_eigenvalue(b, direction=BODY_DIAGONAL, disp=pair_dispersion, order=2,
                  kmax=0.30, n=24, n_even=3):
    """RG eigenvalue of the order-`order` velocity operator under R_b.

    λ = g_n(coarse,b) / g_n(fine) = b^{-order}, exact (T2).

    Matched-sampling proof: the coarse rule Ω_coarse(κ)=Ω(κ/b) sampled at the
    coarse points κ_i = b·k_i gives IDENTICAL dispersion values to the fine rule
    at k_i.  The two least-squares fits then share the same right-hand side and
    differ only by the b^{2j} column rescale, so g_n^coarse = b^{-n} g_n^fine to
    the round-off floor — independent of how well the polynomial fits.
    """
    j = order // 2          # 1 → g2, 2 → g4, …
    d = np.asarray(direction, dtype=np.float64)
    d = d / np.linalg.norm(d)
    kk = np.linspace(kmax / n, kmax, n)                 # fine momenta
    yy = np.array([disp(*(d * k)) / k for k in kk])     # shared RHS

    def coeffs(scale):
        kappa = scale * kk                              # coarse: scale = b
        A = np.vstack([kappa ** (2 * m) for m in range(n_even)]).T
        coef, *_ = np.linalg.lstsq(A, yy, rcond=None)
        return coef[1 + (j - 1)] / coef[0]              # g_n = coef_n / coef_0

    return coeffs(b) / coeffs(1)


# ---- packaged theorem checks ----------------------------------------------
def c_lat_fixed_point(b_list=(1, 2, 3, 4, 5), direction=BODY_DIAGONAL,
                      disp=pair_dispersion):
    """T1.  Returns dict b → physical speed  b · c_coarse(b).  All == 1/√3."""
    return {b: b * extract_speed(direction=direction, b=b, disp=disp)
            for b in b_list}


def liv_irrelevance(b_list=(2, 3, 4, 5), direction=BODY_DIAGONAL,
                    disp=pair_dispersion, order=2):
    """T2.  Returns dict b → (measured eigenvalue, predicted b^{-order})."""
    return {b: (rg_eigenvalue(b, direction=direction, disp=disp, order=order),
                float(b) ** (-order))
            for b in b_list}


# ══════════════════════════════════════════════════════════════════
#  Gauge sector — Gauss law under block-spin  (T3a)
# ══════════════════════════════════════════════════════════════════
#
# Electric field on a periodic L^d lattice: E_axis is a list of d arrays, each
# (L,)*d; E[a][x] is the flux on the link from site x in the +a direction.
# Divergence at a site is outgoing minus incoming flux (F110 convention).
def lattice_divergence(E_axis):
    """(div E)(x) = Σ_a ( E_a[x] − E_a[x − ê_a] )  on a periodic lattice."""
    d = len(E_axis)
    div = np.zeros_like(np.asarray(E_axis[0], dtype=np.float64))
    for a in range(d):
        Ea = np.asarray(E_axis[a], dtype=np.float64)
        div = div + Ea - np.roll(Ea, 1, axis=a)
    return div


def coarse_face_flux(E_axis, b):
    """Block the electric flux: a coarse +a link carries the SUM of the b^{d-1}
    fine +a links piercing the coarse face at the coarse-cell boundary.

    Returns the coarse E_axis list (each array (L/b,)*d).  This is the 1-form /
    bond-moving blocking that makes Gauss's law telescope.
    """
    d = len(E_axis)
    L = np.asarray(E_axis[0]).shape[0]
    assert L % b == 0
    Lc = L // b
    coarse = []
    for a in range(d):
        Ea = np.asarray(E_axis[a], dtype=np.float64)
        # The coarse face at coarse cell X (its +a boundary) sits at the fine
        # layer x_a = b*X + (b-1)  →  link from that site to the next cell.
        # Sum the transverse b^{d-1} fine links over that face.
        # 1) pick the boundary layer along axis a:
        sl = [slice(None)] * d
        sl[a] = slice(b - 1, L, b)
        face = Ea[tuple(sl)]                      # shape: Lc along a, L elsewhere
        # 2) sum the transverse axes in blocks of b
        # reshape every axis != a from L into (Lc, b) and sum the b-subaxis
        shp = []
        sum_axes = []
        ax = 0
        for axis in range(d):
            if axis == a:
                shp.append(Lc)
                ax += 1
            else:
                shp.append(Lc)
                shp.append(b)
                sum_axes.append(ax + 1)
                ax += 2
        face = face.reshape(shp).sum(axis=tuple(sum_axes))
        coarse.append(face)
    return coarse


def block_charge(q, b):
    """Block-sum the charge density (total enclosed charge per coarse cell)."""
    qf = np.asarray(q, dtype=np.float64)
    d = qf.ndim
    L = qf.shape[0]
    Lc = L // b
    shp = []
    for _ in range(d):
        shp += [Lc, b]
    g = qf.reshape(shp)
    return g.sum(axis=tuple(range(1, 2 * d, 2)))


def gauss_law_residual(E_axis, b):
    """T3a residual:  div_coarse(coarse_face_flux(E)) − block_charge(div E).

    Returns the max-abs residual; it is exactly 0 (integer/round-off) because
    summing the fine divergence over a b^d block telescopes to the coarse-face
    fluxes (the discrete divergence theorem).
    """
    q_fine = lattice_divergence(E_axis)
    E_coarse = coarse_face_flux(E_axis, b)
    div_coarse = lattice_divergence(E_coarse)
    Q_coarse = block_charge(q_fine, b)
    return float(np.max(np.abs(div_coarse - Q_coarse)))


# ══════════════════════════════════════════════════════════════════
#  Gravity sector — the dielectric under block-spin  (T3b)
# ══════════════════════════════════════════════════════════════════
def coarse_grain_u(u_fine, b):
    """Block-average the dielectric LOG variable u = ½ ln K (= −Φ/c²).

    This is the RG-covariant variable: the Poisson potential is linear in u, and
    averaging u preserves the reciprocal lock (below)."""
    return block_average(u_fine, b)


def dielectric_from_u(u):
    """(A, B, K) from u: K = e^{2u}, A = 1/K, B = K (F64 canonical, AB ≡ 1)."""
    u = np.asarray(u, dtype=np.float64)
    K = np.exp(2.0 * u)
    return 1.0 / K, K, K


def reciprocal_lock_residual(u_fine, b):
    """T3b impedance leg:  max |A·B − 1| for the LOG-averaged coarse dielectric.

    A·B ≡ 1 holds for any u (A = 1/K = e^{-2ū}, B = K = e^{+2ū}), so the
    impedance match (non-birefringence) is preserved by R_b to round-off — but
    ONLY because we coarse-grain in u.  See `dielectric_jensen_gap` for why the
    naive choice (averaging K) is the wrong RG variable.
    """
    uc = coarse_grain_u(u_fine, b)
    A, B, _ = dielectric_from_u(uc)
    return float(np.max(np.abs(A * B - 1.0)))


def dielectric_jensen_gap(u_fine, b):
    """T3b discriminator: log-averaging vs direct K-averaging.

    The RG-covariant variable is u = ½ ln K (the LINEAR Poisson potential), not
    K.  Coarse K two ways:
        K_log    = exp(2·R_b u)        (correct — keeps Poisson linearity)
        K_direct = R_b(exp 2u)         (naive — averages the dielectric itself)
    By Jensen, K_direct ≥ K_log pointwise; the gap = the variance of u inside
    each block.  A nonzero gap is the price of choosing the wrong RG variable
    (it over-stiffens the lattice and breaks the linear source law).

    Returns (max gap, mean gap) ≥ 0.
    """
    uc = coarse_grain_u(u_fine, b)
    K_log = np.exp(2.0 * uc)
    _, _, K = dielectric_from_u(u_fine)
    K_direct = block_average(K, b)
    gap = K_direct - K_log
    return float(np.max(gap)), float(np.mean(gap))


def poisson_form_invariance_residual(u_fine, b):
    """T3b source leg: the linear Poisson law is form-invariant under R_b in the
    IR (long-wavelength) limit.

    The fine source is s = lap u (F106: lap ln K = −T00 → lap u = −T00/2).  The
    PHYSICAL Laplacian on the coarse grid (spacing b) is lap_coarse / b², so

        (1/b²) lap_coarse(R_b u)  →  R_b(lap_fine u)

    as the potential's wavelength → ∞.  The mismatch is itself an irrelevant
    operator: it is O((k a)²) smaller than the source, the SAME b-suppression as
    the T2 LIV operators, so the gravity discretisation error coarse-grains away.

    Returns max| (1/b²) lap_coarse(R_b u) − R_b(lap_fine u) |.
    """
    s_fine = _grav.lap_nd(np.asarray(u_fine, dtype=np.float64))
    uc = coarse_grain_u(u_fine, b)
    s_coarse = _grav.lap_nd(uc) / (b ** 2)        # physical Laplacian, spacing b
    s_fine_blocked = block_average(s_fine, b)
    return float(np.max(np.abs(s_coarse - s_fine_blocked)))


# ══════════════════════════════════════════════════════════════════
#  Propagator-class preservation  (T3c)
# ══════════════════════════════════════════════════════════════════
def even_rotation_commutator(L=16, b=2, seed=3):
    """[R_b, R(Ω)] on a random even-law (E,B) field, in Fourier space.

    R(Ω) is the even rotation (ca_wmu._f26_rotation_step); R_b here is the same-
    grid box blur (a real per-mode scalar).  Returns the max-abs difference of
    the two orderings — exactly 0 (a scalar commutes with a 2×2 rotation per
    mode), so blocking cannot mix the F91 even/chiral classes.
    """
    from ca_wmu import _f26_rotation_step
    from ca_lattice import make_kgrid_3d

    rng = np.random.default_rng(seed)
    shape = (L, L, L)
    E = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    B = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    KX, KY, KZ = make_kgrid_3d(L, L, L)

    # work in k-space directly: both ops are diagonal-in-k there
    Ek = _fft.fftn(E)
    Bk = _fft.fftn(B)

    # order 1: rotate then blur
    Er, Br = _f26_rotation_step(Ek, Bk, KX, KY, KZ)
    Erb = box_blur_fourier(Er, b)
    Brb = box_blur_fourier(Br, b)

    # order 2: blur then rotate
    Eb = box_blur_fourier(Ek, b)
    Bb = box_blur_fourier(Bk, b)
    Ebr, Bbr = _f26_rotation_step(Eb, Bb, KX, KY, KZ)

    return float(max(np.max(np.abs(Erb - Ebr)), np.max(np.abs(Brb - Bbr))))


# ══════════════════════════════════════════════════════════════════
#  Confinement sector — the ONE relevant direction  (C1)
# ══════════════════════════════════════════════════════════════════
#
# The string tension σ̂ is the static-potential slope of the F110 Kogut–Susskind
# Hamiltonian.  Unlike the LIV operators (irrelevant, λ_n = b^{-n}), σ is the one
# RELEVANT coupling — confinement is an IR phenomenon.  Block-spin (bond-moving)
# merges b parallel fine links into one coarse link, so the coarse link carries b
# times the energy per unit coarse length:  g²_coarse = b·g²_fine, σ̂_coarse =
# b·σ̂_fine, eigenvalue λ_σ = b > 1.  The PHYSICAL confining energy
# V(R_phys) = σ_phys·R_phys is invariant, so a coarse run on b× fewer cells
# reproduces the fine static potential at matched physical separation.
def string_tension_lambda0(g2):
    """λ=0 (pure strong-coupling) string tension σ̂ = g²/2 — the exact F110
    static-potential slope for a unit (q=1) flux string."""
    return 0.5 * g2


def confinement_rg_step(g2, b):
    """Bond-moving flow of the gauge coupling under R_b: g²_coarse = b·g²_fine.

    A coarse link spans b fine lengths, so to keep the PHYSICAL string tension
    (energy per physical length) fixed the coarse lattice coupling must grow by
    b.  This is the relevant (IR) direction."""
    return float(b) * g2


def confinement_eigenvalue(b):
    """RG eigenvalue of the string tension under R_b: λ_σ = b (relevant, >1).

    Contrast `rg_eigenvalue(b, order=n)` = b^{-n} < 1 for the irrelevant LIV
    operators — confinement is the unique relevant scale."""
    return float(b)


def coarse_static_potential(nx_fine, b, g2_fine=1.0, lam=0.0, group='Z3',
                            m_max=None, R_coarse=None):
    """Reproduce the fine F110 static potential from a coarse (b× smaller) run.

    Builds a fine PlaquetteGrid(nx_fine, 1) and a coarse PlaquetteGrid(nx_fine//b,
    1) with the bond-moved coupling g²_coarse = b·g²_fine.  Returns
        (V_fine_at_matched, V_coarse, sep_phys)
    where for each coarse separation R_c the matched physical (fine) separation is
    b·R_c, so V_coarse[R_c] should equal V_fine[b·R_c] — the coarse simulation,
    with b× fewer plaquettes, reproducing the same physical confining energy.
    """
    import ca_link_hamiltonian as _kh

    assert nx_fine % b == 0
    nx_c = nx_fine // b
    if R_coarse is None:
        R_coarse = list(range(1, nx_c))
    R_fine_matched = [b * R for R in R_coarse]

    geom_f = _kh.PlaquetteGrid(nx_fine, 1)
    geom_c = _kh.PlaquetteGrid(nx_c, 1)
    g2_c = confinement_rg_step(g2_fine, b)

    Vf = _kh.static_potential(geom_f, row=0, R_list=R_fine_matched,
                              g2=g2_fine, lam=lam, group=group, m_max=m_max)
    Vc = _kh.static_potential(geom_c, row=0, R_list=R_coarse,
                              g2=g2_c, lam=lam, group=group, m_max=m_max)
    V_fine_matched = {R: Vf[b * R] for R in R_coarse}
    sep_phys = {R: b * R for R in R_coarse}
    return V_fine_matched, Vc, sep_phys


def magnetic_deformation_ratio(nx, g2, lam_list, b=1, group='Z3'):
    """Fractional magnetic deformation of σ̂:  r(λ) = [σ̂(0) − σ̂(λ)]/σ̂(0).

    Measures how much the plaquette (magnetic) coupling λ — the would-be
    deconfining perturbation — bends the pure area law.  The 2nd-order strong-
    coupling correction is Δσ̂ = c₂λ² with c₂ ∝ 1/g² (F110, c₂=1/6 at g²=1), so
    r(λ) = Δσ̂/σ̂(0) ∝ λ²/g⁴.  Under bond-moving g²→b·g² (lattice λ fixed) this
    gives r_coarse/r_fine → b^{-2} as λ→0: the deconfining perturbation is
    irrelevant (same suppression as the leading LIV operator), so the λ=0
    confining fixed point is IR-attractive.  Returns dict λ → r, on
    PlaquetteGrid(nx,1) with coupling b·g2 (b=1 = fine).
    """
    import ca_link_hamiltonian as _kh

    geom = _kh.PlaquetteGrid(nx, 1)
    g2_eff = confinement_rg_step(g2, b) if b != 1 else g2
    R_list = list(range(1, nx))
    s0, _, _ = _kh.fit_linear_potential(
        _kh.static_potential(geom, 0, R_list, g2=g2_eff, lam=0.0, group=group))
    out = {}
    for lam in lam_list:
        s, _, _ = _kh.fit_linear_potential(
            _kh.static_potential(geom, 0, R_list, g2=g2_eff, lam=lam, group=group))
        out[float(lam)] = float((s0 - s) / s0)
    return out
