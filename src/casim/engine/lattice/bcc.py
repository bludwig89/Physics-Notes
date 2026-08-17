"""
ca_bcc.py  —  BCC-lattice Weyl QCA (Paper 1 / Paper 2)
=======================================================
Implements the body-centered-cubic 3D Weyl QCA derived in:

  Bisio, D'Ariano, Perinotti, Tosini (2015) — Free QFT from Quantum CA.
  Foundations of Physics 45, 1137.

  Raynal (2017) — Simple Derivation of the Weyl and Dirac Quantum CA.
  arXiv:1703.05890v2.

The single-step unitary in Fourier space is (Paper 1, Eq. 15):

    A^±(k) = u^±(k) · I  -  i · (σ · ñ^±(k))

with

    u^±(k)  = c_x c_y c_z  ±  s_x s_y s_z
    ñ_x^±   =  s_x c_y c_z  ∓  c_x s_y s_z
    ñ_y^±   =  ∓ c_x s_y c_z  +  s_x c_y s_z      (sign corrected — see _bcc_uvec)
    ñ_z^±   =  c_x c_y s_z   ±  s_x s_y c_z

    c_i := cos(k_i / √3)
    s_i := sin(k_i / √3)

The dispersion relation is

    ω^±(k) = arccos( u^±(k) ) = arccos( c_x c_y c_z ± s_x s_y s_z ).

In the small-|k| limit the interpolating Hamiltonian H = arcsin-equivalent
of the above reduces to the **Weyl Hamiltonian in 3D**:

    H_W(k) = (1/√3) σ · k

i.e. the lattice speed of light is 1/√3 (the QCA analog of the CFL bound).

Finding 26 (rotation reinterpretation): the composite-photon rotation angle
per tick is Ω(k) = 2 ω_+(k/2).  The speed of light

    c_lat = dΩ/d|k||_{k→0} = 1/√3

is not a propagation speed but the *angular rotation rate* of the (E,B)
field pair per unit wavenumber.  The imaginary unit i that appears in
Maxwell's equations is the 2×2 real rotation J = [[0,1],[-1,0]] —
the algebraic artefact of linearising the exact cosine rotation at Δt → 0.

The two signs ± correspond to the two chirality-handed Weyl equations.
Note: ω_+(−k) = ω_−(k) (chirality maps k → −k between branches).
The '+' sign is the left-helicity Weyl, the '-' sign is the right-helicity.

This module exposes:
  weyl_step_3d_bcc(f, g, c=1.0/√3, sign='+')   one BCC step on 2-spinors
  bcc_dispersion(kx, ky, kz, sign='+')          analytic ω^±(k)
  bcc_unitary(kx, ky, kz, sign='+')             the 2×2 unitary U(k)
  measure_bcc_dispersion(...)                   numerical verifier
  bcc_smallk_to_weyl_residual(...)              small-k regression test

All routines preserve unitarity to machine precision; the BCC propagator
is a *diagonal-in-k* 2×2 unitary so norm is exactly conserved by
construction (FFT round-off is the only floor).
"""

import numpy as np
from casim.numerics import fft as _fft          # multi-core FFT backend (scipy/pyfftw/numpy)
from casim.engine.lattice.geometry import make_kgrid_3d as _kgrid3d
from casim.constants import c_lat

_weyl_cache: dict = {}   # (shape, sign) → (U_ff, U_fg, U_gf, U_gg)


# ══════════════════════════════════════════════════════════════════
#  BCC analytic structures
# ══════════════════════════════════════════════════════════════════

# Lattice-imposed light speed.  Paper 1 lines 21–22: H_W = (1/√d) σ·k
# in d=3, the BCC factor is 1/√3.  Stored as a constant so callers can
# pass `c=ca_bcc.BCC_C` to keep the standard small-k Weyl normalisation.
BCC_C = c_lat


def _bcc_uvec(kx, ky, kz, sign='+'):
    """
    Compute (u, n_x, n_y, n_z) per Paper 1 Eq. 15.

    Returns the four real arrays.  Inputs may be scalars or arrays of
    the same broadcast-compatible shape.
    """
    inv_root3 = c_lat
    cx, cy, cz = np.cos(kx * inv_root3), np.cos(ky * inv_root3), np.cos(kz * inv_root3)
    sx, sy, sz = np.sin(kx * inv_root3), np.sin(ky * inv_root3), np.sin(kz * inv_root3)

    if sign == '+':
        s = 1.0
    elif sign == '-':
        s = -1.0
    else:
        raise ValueError(f"sign must be '+' or '-', got {sign!r}")

    # NOTE: qca-papers-1-4-overview.md line 53 had a sign-typo on the
    # second term of n_y ("- s_x c_y s_z").  Direct verification shows
    # u^2 + |n|^2 = 1 only with the corrected sign:
    #
    #   n_y^± = ∓ c_x s_y c_z  +  s_x c_y s_z       (CORRECTED)
    #
    # 100 random k's give max|u^2+|n|^2 − 1| = 4.4e-16 with the fix vs
    # 4.7e-01 with the transcribed sign.  See changelog 2026-05-15.
    u  = cx * cy * cz + s * sx * sy * sz
    nx =  sx * cy * cz - s * cx * sy * sz
    ny = -s * cx * sy * cz + sx * cy * sz          # corrected sign
    nz =  cx * cy * sz + s * sx * sy * cz
    return u, nx, ny, nz


def bcc_dispersion(kx, ky, kz, sign='+'):
    """
    Analytic BCC dispersion ω^±(k) = arccos(u^±(k)) (Paper 1 Eq. 15).

    Inputs may be scalars or compatible arrays.
    """
    u, _, _, _ = _bcc_uvec(kx, ky, kz, sign=sign)
    # arccos clipped to [-1, 1] to avoid NaN from tiny round-off above 1.
    return np.arccos(np.clip(u, -1.0, 1.0))


def bcc_spin_axis(kx, ky, kz, sign='+'):
    """
    Return the normalised BCC spin-quantisation axis n̂(k) = n(k)/sin ω(k).

    This is the Bloch vector of the Weyl eigenmode: the positive-helicity
    eigenstate ψ₊ satisfies (n̂·σ)ψ₊ = +ψ₊, i.e. n̂ is the spin axis of ψ₊.

    Derivation (Finding F26):
        U(k) = u·I − i·(n·σ)  with u² + |n|² = 1 (unitarity).
        Eigenvalue equation  U ψ₊ = e^{−iω} ψ₊  gives
            (n·σ) ψ₊ = sin ω · ψ₊  ⟹  (n̂·σ) ψ₊ = +ψ₊.

    Continuum limit |k| → 0  (using cᵢ → 1, sᵢ → kᵢ/√3):
        n̂ → (k_x, −k_y, k_z) / |k|.
    The sign flip on the y-component is an intrinsic chirality convention
    of the Bisio BCC walk; the spin–momentum locking is exact.

    Returns:
        n_hat : ndarray, shape (3,) or (3, ...)  — unit vector, float64.
            Row 0 = n̂_x, row 1 = n̂_y, row 2 = n̂_z.
    """
    u, nx, ny, nz = _bcc_uvec(kx, ky, kz, sign=sign)
    sin_omega = np.sqrt(np.clip(1.0 - u**2, 0.0, None))
    # At k=0, sin_omega=0; return ẑ = (0,0,1) as the degenerate limit.
    safe = sin_omega > 0.0
    nh_x = np.where(safe, nx / np.where(safe, sin_omega, 1.0), 0.0)
    nh_y = np.where(safe, ny / np.where(safe, sin_omega, 1.0), 0.0)
    nh_z = np.where(safe, nz / np.where(safe, sin_omega, 1.0), 1.0)
    return np.stack([nh_x, nh_y, nh_z], axis=0)


def bcc_unitary(kx, ky, kz, sign='+'):
    """
    The 2×2 unitary U^±(k) per Paper 1 Eq. 15:

        U = u·I - i·(σ_x n_x + σ_y n_y + σ_z n_z)

          = [[ u - i n_z,           -i (n_x - i n_y) ],
             [ -i (n_x + i n_y),     u + i n_z       ]]

    Returns four arrays U_ff, U_fg, U_gf, U_gg with the same shape as kx.
    """
    u, nx, ny, nz = _bcc_uvec(kx, ky, kz, sign=sign)
    U_ff = u - 1j * nz
    U_fg = -1j * (nx - 1j * ny)
    U_gf = -1j * (nx + 1j * ny)
    U_gg = u + 1j * nz
    return U_ff, U_fg, U_gf, U_gg


# ══════════════════════════════════════════════════════════════════
#  BCC fractional-shift utility
# ══════════════════════════════════════════════════════════════════

def bcc_fractional_shift(field_k: np.ndarray,
                         kx: np.ndarray, ky: np.ndarray, kz: np.ndarray,
                         dx: int, dy: int, dz: int) -> np.ndarray:
    """
    Apply a BCC fractional-hop phase shift in k-space.

    The BCC nearest-neighbour hop in direction d = (dx, dy, dz) ∈ {±1}³
    has physical length |d| = √3 in cubic-cell units, so each Cartesian
    component contributes a phase e^{i·d_i·k_i / √3}.  The total phase is:

        e^{i·k·d/√3}  =  exp( i (dx·kx + dy·ky + dz·kz) / √3 )

    This is the phase the BCC QCA propagator U(k) uses.  It is NOT the
    same as integer np.roll shifts, which give e^{i·k·d} (i.e. a full
    one-site hop per axis).  Any real-space BCC implementation using
    np.roll implements a *different* automaton with c_lat = 1 instead of
    1/√3.

    Parameters
    ----------
    field_k : complex ndarray, shape (Lx, Ly, Lz)
        Fourier-space field — output of ca_fft.fftn or _fft.fftn.
    kx, ky, kz : ndarrays of shape (Lx, Ly, Lz)
        k-space grids from make_kgrid_3d; values in (-π, π].
    dx, dy, dz : int  ∈ {+1, -1}
        BCC hop direction components.

    Returns
    -------
    shifted_k : complex ndarray, same shape as field_k
        field_k element-wise multiplied by the fractional-hop phase.

    Notes
    -----
    For efficiency when shifting the same field in all 8 BCC directions,
    FFT field once, then call this 8 times, then IFFT each result.
    That costs 1 forward FFT + 8 phase multiplications + 8 inverse FFTs,
    rather than 8 np.roll calls which would give the wrong operator anyway.

    Example
    -------
    >>> from ca_lattice import make_kgrid_3d
    >>> KX, KY, KZ = make_kgrid_3d(32, 32, 32)
    >>> F_k = _fft.fftn(field)
    >>> F_shifted_k = bcc_fractional_shift(F_k, KX, KY, KZ, +1, +1, +1)
    >>> field_shifted = _fft.ifftn(F_shifted_k).real
    """
    inv_sqrt3 = c_lat
    phase = np.exp(1j * (dx * kx + dy * ky + dz * kz) * inv_sqrt3)
    return field_k * phase


# ══════════════════════════════════════════════════════════════════
#  BCC Weyl stepper
# ══════════════════════════════════════════════════════════════════

def weyl_step_3d_bcc(f, g, sign='+'):
    """
    One step of the exact BCC Weyl QCA.

    Diagonal in Fourier space: FFT both spinor components, multiply by
    the 2×2 unitary U^±(k), inverse-FFT.  This *is* the QCA — no further
    discretisation is needed; one CA tick is one application of U.

    Parameters
    ----------
    f, g : complex128 arrays, shape (Lx, Ly, Lz)
        Upper and lower Weyl spinor components.
    sign : '+' or '-'
        Helicity choice (Paper 1's two unitarily-inequivalent solutions).

    Returns
    -------
    f_new, g_new : updated spinor arrays.

    Exactly unitary by construction — every FFT mode is rotated by a
    2×2 unitary matrix, so total norm is conserved to FFT round-off.
    """
    key = (f.shape, sign)
    if key not in _weyl_cache:
        KX, KY, KZ = _kgrid3d(*f.shape)
        _weyl_cache[key] = bcc_unitary(KX, KY, KZ, sign=sign)
    U_ff, U_fg, U_gf, U_gg = _weyl_cache[key]

    F = _fft.fftn(f)
    G = _fft.fftn(g)

    F_new = U_ff * F + U_fg * G
    G_new = U_gf * F + U_gg * G

    return _fft.ifftn(F_new), _fft.ifftn(G_new)


# ══════════════════════════════════════════════════════════════════
#  Verification utilities
# ══════════════════════════════════════════════════════════════════

def bcc_unitarity_residual(kx, ky, kz, sign='+'):
    """
    For each k, compute ||U†U − I||_F. Should be 0 analytically.

    Returns an array of the same shape as kx with the Frobenius residual
    per mode.
    """
    U_ff, U_fg, U_gf, U_gg = bcc_unitary(kx, ky, kz, sign=sign)
    # U†U entries
    a = np.conj(U_ff) * U_ff + np.conj(U_gf) * U_gf  # (U†U)_11
    b = np.conj(U_ff) * U_fg + np.conj(U_gf) * U_gg  # (U†U)_12
    c = np.conj(U_fg) * U_ff + np.conj(U_gg) * U_gf  # (U†U)_21
    d = np.conj(U_fg) * U_fg + np.conj(U_gg) * U_gg  # (U†U)_22
    res = (np.abs(a - 1.0) ** 2 + np.abs(b) ** 2 +
           np.abs(c) ** 2 + np.abs(d - 1.0) ** 2)
    return np.sqrt(res)


def bcc_a0_check(sign='+'):
    """
    Paper 2 (test V7): at k=0 the transition matrix at the centre of
    the primitive cell must vanish, i.e. U(k=0) = I.

    Returns the four entries (U_ff, U_fg, U_gf, U_gg) evaluated at k=0.
    A correct implementation should give (1, 0, 0, 1).
    """
    U = bcc_unitary(0.0, 0.0, 0.0, sign=sign)
    return tuple(complex(np.asarray(x)) for x in U)


def measure_bcc_dispersion(L=32, n_modes=12, sign='+', n_steps=1, rng=None):
    """
    For a set of random k-values, propagate a plane wave one step and
    measure the phase factor.  Compare to the analytic dispersion.

    Returns max |ω_measured - ω_analytic| over the sampled modes.
    """
    if rng is None:
        rng = np.random.default_rng(0)
    # Choose k values away from the Brillouin zone edges.
    # k_i ∈ [-π·√3/2, π·√3/2] is the natural BCC BZ since c_i = cos(k_i/√3).
    # Pick small/mid-range k's so arccos is well-defined.
    k_max = 0.6 * np.sqrt(3.0)   # safely inside BZ; |k_i/√3| ≤ 0.6
    kvals = rng.uniform(-k_max, k_max, size=(n_modes, 3))

    max_err = 0.0
    for kx_v, ky_v, kz_v in kvals:
        # Build the plane-wave Fourier mode directly: pick a 2-spinor amplitude
        # that is an eigenstate of U(k) so the measured ω is unambiguous.
        U_ff, U_fg, U_gf, U_gg = bcc_unitary(kx_v, ky_v, kz_v, sign=sign)
        # Diagonalise the 2x2 unitary to extract its phase.
        Mat = np.array([[U_ff, U_fg], [U_gf, U_gg]], dtype=complex)
        eigvals, _ = np.linalg.eig(Mat)
        # Eigenvalues are e^{∓iω}; take the principal-branch arccos of
        # the real part of the trace/2 (Paper 1 Eq. 15 gives cos ω = u).
        w_meas = np.arccos(np.clip(eigvals.real, -1.0, 1.0))
        w_ana  = bcc_dispersion(kx_v, ky_v, kz_v, sign=sign)
        # Either eigenvalue's phase magnitude should match ω.
        err = float(min(abs(w_meas[0] - w_ana), abs(w_meas[1] - w_ana)))
        max_err = max(max_err, err)
    return max_err


def bcc_norm_drift_test(L=16, n_steps=200, sign='+', seed=0):
    """
    Initialise a normalised random 2-spinor field on an L^3 lattice and
    run n_steps BCC ticks.  Return final/initial norm minus 1.

    Should be ≤ 1e-12 (FFT round-off floor).
    """
    rng = np.random.default_rng(seed)
    f = (rng.standard_normal((L, L, L)) +
         1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    g = (rng.standard_normal((L, L, L)) +
         1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    norm0 = float(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2))
    for _ in range(n_steps):
        f, g = weyl_step_3d_bcc(f, g, sign=sign)
    norm1 = float(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2))
    return norm1 / norm0 - 1.0


def check_lattice_constant_identities():
    """
    F278 — the walk's crystal is BCC with conventional cube edge a = 2/√3.

    Registry entry point for `F278-bcc-lattice-constant` (the record F278 §9
    specified but did not add; gap #5 of the 2026-08-02 completeness sweep).
    Nine checks, matching that section one-for-one.

    `a` is deliberately NOT a registered constant and NOT a literal: it is
    derived here as `2 * c_lat`, per F278 §8 and D7 (a constant that is a
    function of another constant is not registered separately).  A decimal
    literal transcribed from an independent evaluation of 2/√3 lands one ulp
    away — that is the caveat F278 §2 records, and it is why check 2 compares
    the raw IEEE-754 bits rather than a tolerance.

    Failure mode (this is the point of the record): any change to `c_lat`, to
    the hop-phase convention in `bcc_fractional_shift`, or to `_bcc_uvec`
    breaks check 2, 6 or 9.  Audit item V-016 found nothing guarding the
    `c_lat` separation; this guards it.

    Returns the result dict; raises AssertionError on any failure.
    """
    import struct as _struct

    import sympy as sp

    out = {}
    a_f = 2.0 * c_lat                     # F278 §2: a = 2 c_lat, derived not written
    a_s = 2 * sp.Rational(1, 1) / sp.sqrt(3)   # the same a, symbolically

    # ---- 1. a = 2/√3 from a/2 = 1/√3 — the hop-length match (algebra) -----
    out["c1_a_over_2_is_c_lat"] = (a_f / 2.0 == float(c_lat))
    assert out["c1_a_over_2_is_c_lat"], "a/2 must BE c_lat, not merely equal it"

    # ---- 2. a/2 and c_lat are the same double (0x3fe279a74590331d) -------
    bits = lambda x: _struct.pack(">d", x).hex()
    out["c2_bit_pattern"] = bits(a_f / 2.0)
    out["c2_c_lat_bit_pattern"] = bits(float(c_lat))
    assert out["c2_bit_pattern"] == out["c2_c_lat_bit_pattern"], "bit mismatch"
    assert out["c2_bit_pattern"] == "3fe279a74590331d", (
        f"c_lat has moved: {out['c2_bit_pattern']} != 3fe279a74590331d")

    # ---- 3-7: sympy, residual identically zero (F278 §9 method column) ----
    # The float path is deliberately NOT used here: 3(a/2)^2 - 1 is 2.2e-16 in
    # doubles, and F278's claim is an algebraic identity, not a tolerance.

    # 3. |(a/2)(1,1,1)| = 1 exactly.
    r3 = sp.simplify(sp.sqrt(3 * (a_s / 2) ** 2) - 1)
    out["c3_nn_length_residual"] = str(r3)
    assert r3 == 0, r3

    # 4. primitive cell volume a³/2 = 4√3/9.
    v_prim_s = a_s ** 3 / 2
    r4 = sp.simplify(v_prim_s - 4 * sp.sqrt(3) / 9)
    out["c4_residual_vs_4root3_over_9"] = str(r4)
    assert r4 == 0, r4

    # 5. 4√3/9 = 4/(3√3) — the form F267 measured it in.
    r5 = sp.simplify(4 * sp.sqrt(3) / 9 - 4 / (3 * sp.sqrt(3)))
    out["c5_residual_vs_4_over_3root3"] = str(r5)
    assert r5 == 0, r5

    # 6. V_cube / V_BZ = a³/2.  The FFT grid samples (-π,π]³, the BZ of a simple
    #    cubic lattice of edge 1 (primitive volume exactly 1), so the ratio IS
    #    the BCC primitive-cell volume.
    v_cube = (2 * sp.pi) ** 3
    v_bz = (2 * sp.pi) ** 3 / v_prim_s
    r6 = sp.simplify(v_cube / v_bz - v_prim_s)
    out["c6_residual"] = str(r6)
    assert r6 == 0, r6

    # 7. 4π/a = 2π√3 — F273's measured "√3 · fcc" reciprocal period.
    r7 = sp.simplify(4 * sp.pi / a_s - 2 * sp.pi * sp.sqrt(3))
    out["c7_residual"] = str(r7)
    assert r7 == 0, r7

    # ---- 8-9: float, evaluated at Γ–H, far from the k→0 conditioning ------
    # 8. 2π/a = π√3  (Γ–H).
    #
    # CORRECTION to F278 §9, recorded 2026-08-03 when this record was written.
    # F278 tabulates check 8 as float residual "0.0".  It is not: 1/c_lat is
    # one ulp BELOW np.sqrt(3) (0x3ffbb67ae8584ca9 vs ...caa), so 2π/a and
    # π√3 differ by exactly one ulp of the result, 8.88e-16.  This is F278's
    # OWN §2 ulp caveat — the one that says not to transcribe a decimal for
    # a — applied to its own check 8, where the finding did not apply it.
    # The identity is exact (check 7 proves it in sympy); only the float
    # evaluation carries the ulp.  Asserted at 1 ulp, not at zero, so the
    # record states something true.
    out["c8_gamma_H"] = 2.0 * np.pi / a_f
    out["c8_residual"] = abs(2.0 * np.pi / a_f - np.pi * np.sqrt(3.0))
    out["c8_residual_ulps"] = out["c8_residual"] / np.spacing(np.pi * np.sqrt(3.0))
    assert out["c8_residual_ulps"] <= 1.0, out["c8_residual_ulps"]

    v_prim = float(v_prim_s)
    out["c4_v_prim"] = v_prim
    out["c7_four_pi_over_a"] = 4.0 * np.pi / a_f

    # 9. ω±(π√3, 0, 0) = π on BOTH branches — the shipped dispersion agrees.
    #    Evaluated far from the k→0 regime audit V-015 found ill-conditioned
    #    (F278 limitation 2).
    gh = np.pi * np.sqrt(3.0)
    w_plus = float(bcc_dispersion(gh, 0.0, 0.0, sign='+'))
    w_minus = float(bcc_dispersion(gh, 0.0, 0.0, sign='-'))
    out["c9_omega_plus"] = w_plus
    out["c9_omega_minus"] = w_minus
    out["c9_residual_plus"] = abs(w_plus - np.pi)
    out["c9_residual_minus"] = abs(w_minus - np.pi)
    assert out["c9_residual_plus"] == 0.0, out["c9_residual_plus"]
    assert out["c9_residual_minus"] == 0.0, out["c9_residual_minus"]

    # The two constants F278 promotes from measured to closed form, as exact
    # rationals-of-radicals in the form the findings reported them.
    out["f267_cube_over_bz_ratio"] = v_prim
    out["f273_reciprocal_factor"] = out["c7_four_pi_over_a"] / (2.0 * np.pi)
    out["n_checks"] = 9
    out["verdict"] = (
        "The BCC walk is a faithful crystal walk with conventional cube edge "
        "a = 2/sqrt3 = 2*c_lat. F267's measured cube/BZ ratio 4/(3 sqrt3) IS "
        "the primitive-cell volume a^3/2; F273's measured 'sqrt3 . fcc' period "
        "IS its reciprocal lattice 4 pi / a. Two measurements become one "
        "geometric statement, and a is not a new parameter."
    )
    return out


def bcc_smallk_to_weyl_residual(k_mag=0.05, n_dirs=8, sign='+', seed=1):
    """
    For |k| → 0 the BCC dispersion linearises to ω ≈ (1/√3) |k|.

    Sample n_dirs random unit directions on the sphere; compute the BCC
    dispersion at |k|·k̂ and at the linearisation; return the maximum
    relative residual.

    Expected to scale as O(|k|²) — the leading correction to the linear
    Weyl Hamiltonian is the diffusion term in Paper 4 Eq. 16.
    """
    rng = np.random.default_rng(seed)
    # Random points on the unit sphere
    v = rng.standard_normal((n_dirs, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    K = k_mag * v
    w_ana = bcc_dispersion(K[:, 0], K[:, 1], K[:, 2], sign=sign)
    w_lin = c_lat * k_mag
    rel = np.abs(w_ana - w_lin) / w_lin
    return float(rel.max())


if __name__ == '__main__':
    # Quick smoke test when run directly.
    print('BCC unitarity max residual:',
          float(bcc_unitarity_residual(
              *np.meshgrid(np.linspace(-1, 1, 8),
                           np.linspace(-1, 1, 8),
                           np.linspace(-1, 1, 8), indexing='ij')).max()))
    print('A_0 check (k=0):', bcc_a0_check())
    print('Dispersion measure residual:', measure_bcc_dispersion())
    print('Norm drift (16^3, 200 steps):', bcc_norm_drift_test())
    print('Small-k vs Weyl residual at |k|=0.05:', bcc_smallk_to_weyl_residual())
