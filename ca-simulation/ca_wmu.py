"""
ca_wmu.py  —  SU(2) W_μ gauge field on the BCC lattice
=======================================================
Implements the W_μ roadmap (2026-05-24):

  Phase 1  — SU(2) link variables & covariant BCC hopping
  Phase 2  — Free W propagation (F26 rotation law per a-component)
  Phase 3  — Non-Abelian self-coupling (Yang–Mills)
  Phase 4  — Fermion–W_μ vertex (covariant derivative for doublet)
  Phase 5B — W mass generation via Stueckelberg / Ludwig U(x)
  Phase 6  — Electroweak mixing (W³ ↔ B ↔ γ)

Design commitments:
  - BCC lattice substrate, same as photon and Weyl spinors.
  - SU(2) link variables U_ℓ stored as (U_a, U_b) arrays satisfying
    U = [[a, -b*],[b, a*]],  |a|² + |b|² = 1.
  - Real-space covariant hopping (gauge-invariant by construction).
  - g_lat = 1 (CA-natural units; calibrated to SM in Phase 6).
  - Exactness goal: Ward identities ≤ 10⁻¹⁴.

References:
  F26 — speed of light as rotation rate
  F27 — chiral SU(2) from β-gauging
  F29 — W-triplet bilinear bridge
  roadmap-wmu-implementation.md
"""

import numpy as np
import ca_fft as _fft
from ca_lattice import make_kgrid_3d as _kgrid3d
from ca_bcc import bcc_dispersion, bcc_unitary, weyl_step_3d_bcc, BCC_C

# ═══════════════════════════════════════════════════════════════════
#  BCC geometry constants
# ═══════════════════════════════════════════════════════════════════

# 8 BCC nearest-neighbor link directions: all (±1, ±1, ±1) combinations.
# Ordered so that index i and index i^4 (XOR with 4) are antipodal pairs:
#   dir 0=(+++) and dir 7=(---), etc.
BCC_DIRS = np.array([
    [a, b, c]
    for a in [1, -1]
    for b in [1, -1]
    for c in [1, -1]
], dtype=int)  # shape (8, 3)

# For each direction i, store the index of its antipodal direction (-d):
_ANTIPODAL = np.array([
    np.where((BCC_DIRS == -BCC_DIRS[i]).all(axis=1))[0][0]
    for i in range(8)
])


def _spinor_matrix(a_dir, b_dir, c_dir, sign='+'):
    """
    2×2 complex spinor coefficient matrix M_d for BCC link direction
    d = (a_dir, b_dir, c_dir) ∈ {±1}³ and chirality sign ∈ {'+', '-'}.

    The BCC unitary in Fourier space decomposes as
        U(k) = Σ_d  M_d · exp(i k·d / √3)
    derived by expanding cx = cos(kx/√3) etc. as sums of complex exponentials.

    Derivation (sign='+'):
        u   = (1/8) Σ (1 + i·abc)       · e^{ikd/√3}
        nx  = (1/8) Σ (−ia + bc)        · e^{ikd/√3}
        ny  = (1/8) Σ (ib − ac)         · e^{ikd/√3}
        nz  = (1/8) Σ (−ic − ab)        · e^{ikd/√3}
    Combined:  U = u·I − i(σ·n)
        M[0,0] = (1/8)(1 + i·abc − c + i·ab)
        M[0,1] = (1/8)(a(c−1) − ib(1+c))
        M[1,0] = (1/8)(−a(1+c) + ib(1−c))
        M[1,1] = (1/8)(1 + i·abc + c − i·ab)

    For sign='−' all i → −i (complex conjugate of sign='+').
    """
    a, b, c = a_dir, b_dir, c_dir
    abc = a * b * c
    s = 1.0 if sign == '+' else -1.0
    M = np.array([
        [(1 + s * 1j * abc - c + s * 1j * a * b),
         (a * (c - 1) - s * 1j * b * (1 + c))],
        [(-a * (1 + c) + s * 1j * b * (1 - c)),
         (1 + s * 1j * abc + c - s * 1j * a * b)],
    ], dtype=complex) / 8.0
    return M


# Precompute for both signs.
# Used by covariant_weyl_step_3d_bcc_exact and verify_spinor_matrix_decomp.
_SPINOR_MATS = {
    sign: np.stack(
        [_spinor_matrix(a, b, c, sign=sign) for a, b, c in BCC_DIRS],
        axis=0
    )  # shape (8, 2, 2)
    for sign in ('+', '-')
}


# ═══════════════════════════════════════════════════════════════════
#  Phase 1 — Link variables & covariant BCC hopping
# ═══════════════════════════════════════════════════════════════════

def make_w_link_field(L, mode='identity', seed=42):
    """
    Initialise SU(2) link variables on all 8 BCC link directions.

    Parameters
    ----------
    L : int or (Lx, Ly, Lz) tuple
        Lattice size.
    mode : str
        'identity'   — U_ℓ = I everywhere (a=1, b=0).
        'random'     — U_ℓ uniform on SU(2) via Haar measure.
        'pure_gauge' — U_ℓ = V(x+ê) V(x)† for a random V(x) field.
    seed : int
        RNG seed for reproducibility.

    Returns
    -------
    U_links : list of 8 elements, each a tuple (U_a, U_b) of complex128
              arrays of shape (Lx, Ly, Lz).
              U_ℓ(x) = [[U_a[x], −conj(U_b[x])],
                         [U_b[x],  conj(U_a[x])]]
    """
    if isinstance(L, int):
        shape = (L, L, L)
    else:
        shape = tuple(L)

    rng = np.random.default_rng(seed=seed)

    if mode == 'identity':
        U_links = [(np.ones(shape, dtype=complex),
                    np.zeros(shape, dtype=complex))
                   for _ in range(8)]

    elif mode == 'random':
        U_links = []
        for _ in range(8):
            raw = rng.standard_normal(shape + (4,))
            norms = np.linalg.norm(raw, axis=-1, keepdims=True)
            q = raw / norms  # unit quaternion (q0,q1,q2,q3)
            U_a = q[..., 0] + 1j * q[..., 3]
            U_b = q[..., 2] + 1j * q[..., 1]
            U_links.append((U_a, U_b))

    elif mode == 'pure_gauge':
        # Generate a random V(x) field, then set U_ℓ(x) = V(x+d)·V(x)†.
        raw = rng.standard_normal(shape + (4,))
        norms = np.linalg.norm(raw, axis=-1, keepdims=True)
        q = raw / norms
        Va = q[..., 0] + 1j * q[..., 3]
        Vb = q[..., 2] + 1j * q[..., 1]
        U_links = []
        for dx, dy, dz in BCC_DIRS:
            Va_shift = np.roll(np.roll(np.roll(Va, -dx, 0), -dy, 1), -dz, 2)
            Vb_shift = np.roll(np.roll(np.roll(Vb, -dx, 0), -dy, 1), -dz, 2)
            # U = V(x+d) · V(x)†  in SU(2) multiplication:
            # V(x+d) = [[Va', -Vb'*],[Vb', Va'*]]
            # V(x)†  = [[Va*, Vb*],[-Vb, Va]]
            # Product (a,b) components:
            # a'' = Va'·Va* + Vb'·Vb = Va'·Va* + Vb'·Vb  (real part)
            # Hmm, use SU(2) product: [a1,b1]·[a2†,−b2†] form
            # V(x+d) · V(x)†:
            #   a_out = Va_shift * conj(Va) + Vb_shift * conj(Vb)  ... wait
            # SU(2): if A=[[a,-b*],[b,a*]] and B=[[c,-d*],[d,c*]]
            # A·B† = A · [[c*,d*],[-d,c]]  (B† = [[c*,d],[−d*,c*]] ← careful)
            # B = [[c,-d*],[d,c*]]  so B† = [[c*,d*],[-d,c]]
            # A·B†: (1,1) = a·c* + (-b*)·(-d) = a·c* + b*·d
            #       (1,2) = a·d* + (-b*)·c = a·d* - b*·c
            #       (2,1) = b·c* + c*·(-d) ... let me do this properly.
            # For SU(2) product [[a,-b*],[b,a*]] · [[c*,d*],[-d,c]]:
            # (1,1): a·c* + (-b*)·(-d) = a·c* + conj(b)·d
            # (1,2): a·d* + (-b*)·c    = a·d* - conj(b)·c
            # (2,1): b·c* + a*·(-d)    = b·c* - conj(a)·d
            # (2,2): b·d* + a*·c       = b·d* + conj(a)·c
            # New SU(2) form [[A,-B*],[B,A*]]:
            #   A = a·c* + conj(b)·d,  B = b·c* - conj(a)·d
            U_a_pg = Va_shift * np.conj(Va) + np.conj(Vb_shift) * Vb
            U_b_pg = Vb_shift * np.conj(Va) - np.conj(Va_shift) * Vb
            U_links.append((U_a_pg, U_b_pg))
    else:
        raise ValueError(f"Unknown mode {mode!r}. Use 'identity', 'random', or 'pure_gauge'.")

    return U_links


def link_unitarity_residual(U_links):
    """
    Return max_{ℓ,x} ‖U_ℓ(x)†U_ℓ(x) − I‖_F over all links and sites.

    For exact SU(2): |U_a|² + |U_b|² = 1, so the Frobenius norm of
    U†U − I = 2·|( |a|²+|b|²−1 )|.
    """
    max_res = 0.0
    for U_a, U_b in U_links:
        norm_sq = np.abs(U_a)**2 + np.abs(U_b)**2  # should be 1 everywhere
        res = np.max(np.abs(norm_sq - 1.0))
        if res > max_res:
            max_res = res
    return max_res


def _apply_su2_to_isospin(U_a, U_b, psi_nu, psi_e):
    """
    Apply U = [[a, -b*],[b, a*]] to the isospin doublet (ψ_ν, ψ_e).
    Returns (ψ_ν_new, ψ_e_new).
    """
    psi_nu_new = U_a * psi_nu - np.conj(U_b) * psi_e
    psi_e_new  = U_b * psi_nu + np.conj(U_a) * psi_e
    return psi_nu_new, psi_e_new


def _u_eff_from_links(U_links):
    """
    Compute a site-centred SU(2) effective gauge field from U_links by
    averaging the 8 link variables at each site and re-unitarising.

    Architecture note
    -----------------
    weyl_step_3d_bcc is a SPECTRAL (FFT) walk with irrational-distance hops
    (nearest-neighbour distance = √3 in physical units), NOT a simple integer
    nearest-neighbour hop on Z³.  It cannot be written as a finite real-space
    sum over (±1,±1,±1) integer shifts.

    The gauge-covariant step therefore uses:
        ψ̃(x) = U_eff(x) · ψ(x)          [position-space gauge rotation]
        ψ'    = weyl_step_3d_bcc(ψ̃)      [spectral kinetic step]

    Properties:
      • U_links = identity  →  U_eff = I  →  reduces EXACTLY to
        weyl_step_3d_bcc, residual = 0 to FFT round-off  (W1.2).
      • Global SU(2)_L (constant V): Ward identity exact to machine ε
        because V commutes with BCC (acts on spin; V acts on isospin).
      • Local SU(2)_L: Ward identity holds in the continuum limit (O(a)
        corrections at finite lattice spacing), the same status as all
        improved fermion actions in lattice gauge theory.
    """
    U_a_sum = sum(U_a for (U_a, _) in U_links)
    U_b_sum = sum(U_b for (_, U_b) in U_links)
    # Re-unitarise (polar decomposition of the SU(2) average)
    norm = np.sqrt(np.abs(U_a_sum)**2 + np.abs(U_b_sum)**2)
    norm = np.where(norm > 1e-14, norm, 1.0)
    return U_a_sum / norm, U_b_sum / norm


def covariant_weyl_step_3d_bcc(f_nu, f_e, g_nu, g_e, U_links, sign='+'):
    """
    One covariant BCC Weyl step for an SU(2) isospin doublet.

    Implementation: gauge-rotate in position space via a site-centred
    effective gauge field, then apply the spectral BCC unitary.

        ψ̃_α(x) = [U_eff(x)]_{αα'} ψ_{α'}(x)     [isospin rotation at each site]
        ψ'_α    = BCC_spectral[ ψ̃_α ]              [spectral BCC kinetic step]

    The site-centred U_eff(x) is the re-unitarised average of the 8 link
    variables at x (see _u_eff_from_links).

    Architecture note — why this is an O(a) approximation
    -------------------------------------------------------
    weyl_step_3d_bcc is spectral (FFT-based) and applies
    U(k) = Σ_d M_d e^{ik·d/√3}, corresponding to hops of size d/√3 (an
    irrational number of lattice units) rather than integer hops.  There is
    NO finite real-space sum over (±1,±1,±1) integer rolls that reproduces
    this exactly — integer rolls correspond to e^{ik·d}, not e^{ik·d/√3}.
    Consequently, a per-link covariant sum using np.roll is a *different*
    kinetic operator (c_lat = 1 instead of 1/√3) and breaks W1.2.

    The site-average approach preserves the exact BCC QCA kinetic operator
    (W1.2, W1.3) and approximates the local Ward identity in the continuum
    limit, where slowly-varying V(x) commutes with the hop phase to O(a):

        V(x) ≈ V(x+d)  ⟹  W1.4 residual ~ a·|∇V| · L,

    exactly the status of O(a)-improved fermion actions in lattice QCD.

    Properties
    ----------
    • W1.2: U_links = identity → U_eff = I → reduces exactly to
      weyl_step_3d_bcc per flavour.  Residual ≤ FFT round-off.
    • W1.3: norm conserved to machine precision for any unitary U_links.
    • W1.4: local Ward identity holds to O(a) ~ a·|∇V|·L.
      For random V on L=16: residual ~ 0.04 (O(1) in a·L units).
      For smooth V with |∇V|·a ≪ 1: residual ≪ 1.
    • Exact local Ward identity (W1.4 ≤ 1e-14) is not achievable with a
      spectral kinetic step — would require a different, non-BCC-QCA kinetic
      operator.  This is a known fundamental tension, not a bug.

    Parameters
    ----------
    f_nu, f_e : complex128 (Lx,Ly,Lz)  — upper Weyl spinor, ν and e.
    g_nu, g_e : complex128 (Lx,Ly,Lz)  — lower Weyl spinor.
    U_links   : list of 8 (U_a, U_b) tuples from make_w_link_field.
    sign      : '+' or '-' for BCC chirality.

    Returns
    -------
    f_nu_new, f_e_new, g_nu_new, g_e_new

    When U_links are identity: U_eff = I → ψ̃ = ψ → reduces exactly to
    weyl_step_3d_bcc per flavour (W1.2, residual ≤ FFT round-off ≈ 1e-15).
    """
    # 1. Site-centred effective gauge field from links
    U_a, U_b = _u_eff_from_links(U_links)

    # 2. Apply U_eff to the isospin doublet at each site
    tf_nu, tf_e = _apply_su2_to_isospin(U_a, U_b, f_nu, f_e)
    tg_nu, tg_e = _apply_su2_to_isospin(U_a, U_b, g_nu, g_e)

    # 3. Apply spectral BCC step to each flavour independently
    f_nu_new, g_nu_new = weyl_step_3d_bcc(tf_nu, tg_nu, sign=sign)
    f_e_new,  g_e_new  = weyl_step_3d_bcc(tf_e,  tg_e,  sign=sign)

    return f_nu_new, f_e_new, g_nu_new, g_e_new


def verify_spinor_matrix_decomp(n_modes: int = 20, sign: str = '+',
                                seed: int = 7) -> float:
    """
    Verify the _SPINOR_MATS decomposition against bcc_unitary directly.

    The claim (from _spinor_matrix docstring) is:

        U_BCC(k) = Σ_{d ∈ BCC_DIRS}  M_d  ·  exp(i k·d / √3)

    This function samples n_modes random k-points, reconstructs U from
    the sum, and measures the Frobenius deviation from bcc_unitary.

    Returns
    -------
    max_err : float
        Maximum ||U_reconstructed − U_BCC||_F over sampled modes.
        Expected: < 1e-14 (machine precision).
    """
    rng = np.random.default_rng(seed)
    k_max = 0.6 * np.sqrt(3.0)
    kvals = rng.uniform(-k_max, k_max, size=(n_modes, 3))

    M_mats = _SPINOR_MATS[sign]           # (8, 2, 2)
    INV_SQRT3 = 1.0 / np.sqrt(3.0)

    max_err = 0.0
    for kx_v, ky_v, kz_v in kvals:
        # Reconstruct from spinor matrices
        U_rec = np.zeros((2, 2), dtype=complex)
        for i, (dx, dy, dz) in enumerate(BCC_DIRS):
            phase = np.exp(1j * (dx * kx_v + dy * ky_v + dz * kz_v) * INV_SQRT3)
            U_rec += M_mats[i] * phase

        # Direct formula
        U_ff, U_fg, U_gf, U_gg = bcc_unitary(
            np.array(kx_v), np.array(ky_v), np.array(kz_v), sign=sign)
        U_bcc = np.array([[complex(U_ff), complex(U_fg)],
                          [complex(U_gf), complex(U_gg)]])

        err = float(np.linalg.norm(U_rec - U_bcc, ord='fro'))
        max_err = max(max_err, err)
    return max_err


def covariant_weyl_step_3d_bcc_exact(f_nu, f_e, g_nu, g_e,
                                     U_links, sign='+'):
    """
    Exact gauge-covariant BCC Weyl step via per-link FFT fractional shifts.

    The BCC unitary decomposes as (see _spinor_matrix):

        U_BCC(k) = Σ_{d ∈ BCC_DIRS}  M_d · exp(i k·d / √3)

    where each M_d is a precomputed 2×2 spin matrix and the phase
    exp(i k·d/√3) is a fractional hop of size 1/√3 lattice units per
    Cartesian axis.  In real space this is:

        ψ'(x) = Σ_d  U_link_d(x) · M_d · [shift_{d/√3} ψ](x)

    where [shift_{d/√3} ψ] = IFFT[ exp(i k·d/√3) · FFT[ψ] ] is the
    exact fractional shift implemented via bcc_fractional_shift.

    Contrast with covariant_weyl_step_3d_bcc (the O(a) site-average
    version): that function re-unitarises the average of all 8 link
    variables into a single U_eff(x), then applies the spectral BCC
    unitary.  It conserves norm exactly but blurs per-link gauge coupling.

    Properties
    ----------
    W1.2 (exact)    : U_links = identity → identical to weyl_step_3d_bcc
                      to FFT round-off (< 1e-15).  Proof: sum reduces to
                      Σ_d M_d · shift_{d/√3} = U_BCC by construction.
    W1.3 (approx)   : Norm is NOT conserved for non-identity U_links.
                      The sum Σ_d U_d M_d shift_{d/√3} is unitary only when
                      all U_d = I.  Use covariant_weyl_step_3d_bcc for
                      norm-conserving long-run dynamics.
    W1.4 (O(a))     : Local SU(2)_L Ward identity holds to O(a)·|∇V|·L —
                      same continuum-limit order as the site-average version,
                      because the integer link hops (used by gauge_transform_links)
                      differ from the fractional kinetic hops by O(a).
    W1.6 (exact)    : Verified by test_W1_6_exact_identity_reduces_to_bcc.

    Performance
    -----------
    4 forward FFTs (once) + 8 × (4 phase multiplications + 4 IFFTs) = 36 FFTs
    vs the site-average version's ~10 FFTs.  ~3.5× slower but structurally
    correct.

    Parameters
    ----------
    f_nu, f_e : complex128 (Lx,Ly,Lz) — upper Weyl spinor, ν and e components.
    g_nu, g_e : complex128 (Lx,Ly,Lz) — lower Weyl spinor.
    U_links   : list of 8 (U_a, U_b) tuples from make_w_link_field.
    sign      : '+' or '-' for BCC chirality.

    Returns
    -------
    f_nu_new, f_e_new, g_nu_new, g_e_new
    """
    from ca_bcc import bcc_fractional_shift

    KX, KY, KZ = _kgrid3d(*f_nu.shape)

    # Forward FFT all four spinor components — done once, reused per direction.
    F_nu_k = _fft.fftn(f_nu)
    F_e_k  = _fft.fftn(f_e)
    G_nu_k = _fft.fftn(g_nu)
    G_e_k  = _fft.fftn(g_e)

    M_mats = _SPINOR_MATS[sign]   # shape (8, 2, 2) — spin coefficient matrices

    f_nu_new = np.zeros_like(f_nu)
    f_e_new  = np.zeros_like(f_e)
    g_nu_new = np.zeros_like(g_nu)
    g_e_new  = np.zeros_like(g_e)

    for i, (dx, dy, dz) in enumerate(BCC_DIRS):
        # ── Step 1: fractional BCC shift in k-space, then back to real space ──
        f_nu_sh = _fft.ifftn(bcc_fractional_shift(F_nu_k, KX, KY, KZ, dx, dy, dz))
        f_e_sh  = _fft.ifftn(bcc_fractional_shift(F_e_k,  KX, KY, KZ, dx, dy, dz))
        g_nu_sh = _fft.ifftn(bcc_fractional_shift(G_nu_k, KX, KY, KZ, dx, dy, dz))
        g_e_sh  = _fft.ifftn(bcc_fractional_shift(G_e_k,  KX, KY, KZ, dx, dy, dz))

        # ── Step 2: apply M_d to spin indices (ν and e independently) ─────────
        # M acts on the (f, g) Weyl spin-space; ν and e are parallel isospin lanes.
        M = M_mats[i]                          # 2×2 complex
        f_nu_rot = M[0, 0] * f_nu_sh + M[0, 1] * g_nu_sh
        g_nu_rot = M[1, 0] * f_nu_sh + M[1, 1] * g_nu_sh
        f_e_rot  = M[0, 0] * f_e_sh  + M[0, 1] * g_e_sh
        g_e_rot  = M[1, 0] * f_e_sh  + M[1, 1] * g_e_sh

        # ── Step 3: apply isospin gauge link U_link_d (acts on (ν, e) space) ──
        U_a, U_b = U_links[i]
        f_nu_new += U_a * f_nu_rot - np.conj(U_b) * f_e_rot
        f_e_new  += U_b * f_nu_rot + np.conj(U_a) * f_e_rot
        g_nu_new += U_a * g_nu_rot - np.conj(U_b) * g_e_rot
        g_e_new  += U_b * g_nu_rot + np.conj(U_a) * g_e_rot

    return f_nu_new, f_e_new, g_nu_new, g_e_new


def gauge_transform_links(U_links, V_a, V_b):
    """
    Apply a local SU(2) gauge transformation V(x) to all link variables:

        U_ℓ(x) → V(x + ê_ℓ) · U_ℓ(x) · V(x)†

    Parameters
    ----------
    U_links : list of 8 (U_a, U_b) tuples.
    V_a, V_b : complex128 (Lx,Ly,Lz) — SU(2) gauge transformation field.

    Returns
    -------
    U_links_new : list of 8 transformed (U_a, U_b) tuples.
    """
    U_links_new = []
    for i, ((U_a, U_b), (dx, dy, dz)) in enumerate(zip(U_links, BCC_DIRS)):
        # V(x+d):
        Va_xpd = np.roll(np.roll(np.roll(V_a, -dx, 0), -dy, 1), -dz, 2)
        Vb_xpd = np.roll(np.roll(np.roll(V_b, -dx, 0), -dy, 1), -dz, 2)

        # Step 1: U' = V(x+d) · U_ℓ(x)
        # SU(2) product [[a1,-b1*],[b1,a1*]] · [[a2,-b2*],[b2,a2*]]:
        #   a_out = a1·a2 − b1*·b2
        #   b_out = b1·a2 + a1*·b2
        mid_a = Va_xpd * U_a - np.conj(Vb_xpd) * U_b
        mid_b = Vb_xpd * U_a + np.conj(Va_xpd) * U_b

        # Step 2: result · V(x)†
        # V(x)† = [[Va*, Vb*],[-Vb, Va]] = [[conj(Va), conj(Vb)],[-Vb, Va]]
        # As SU(2): a = conj(Va), b = -Vb  → but need canonical form
        # Equivalently: multiply by V†: a'' = a'·Va* + b'·Vb* (if V† = [[Va*,Vb*],[-Vb,Va]])
        # SU(2) product [[mid_a,-mid_b*],[mid_b,mid_a*]] · [[Va*,Vb*],[-Vb,Va]]:
        #   a_out = mid_a·Va* + (-mid_b*)·(-Vb) = mid_a·conj(Va) + conj(mid_b)·Vb
        #   b_out = mid_b·Va* + mid_a*·(-Vb)    ... wait, let me be careful.
        # V† = [[Va*,Vb*],[-Vb,Va]] has canonical SU(2) form with a=Va*, b=-Vb.
        # Product formula with B = (c,d) where c=Va*, d=-Vb:
        #   a_out = mid_a·c - conj(mid_b)·d = mid_a·Va* - conj(mid_b)·(-Vb)
        #         = mid_a·conj(Va) + conj(mid_b)·Vb
        #   b_out = mid_b·c + conj(mid_a)·d = mid_b·Va* + conj(mid_a)·(-Vb)
        #         = mid_b·conj(Va) - conj(mid_a)·Vb
        new_a = mid_a * np.conj(V_a) + np.conj(mid_b) * V_b
        new_b = mid_b * np.conj(V_a) - np.conj(mid_a) * V_b

        U_links_new.append((new_a, new_b))

    return U_links_new


def gauge_transform_links_kspace(U_links, V_a, V_b):
    """
    Apply a local SU(2) gauge transformation using FRACTIONAL k-space shifts.

    Convention matched to covariant_weyl_step_3d_bcc_exact:

        U_d(x)  →  V(x) · U_d(x) · V†(x + d/√3)

    where V†(x+d/√3) = IFFT[ e^{i k·d/√3} · FFT[V†](k) ] is the same
    fractional-hop phase used in covariant_weyl_step_3d_bcc_exact.

    This makes the Ward identity for covariant_weyl_step_3d_bcc_exact exact:

        V(x) · step(ψ; U) = step(V·ψ; gauge_transform_links_kspace(V, U))

    Proof
    -----
    The covariant step is ψ'(x) = Σ_d M_d · U_d(x) · [shift_{d/√3} ψ](x).
    Under ψ → V·ψ and U_d → U'_d:

        ψ'_new(x) = Σ_d M_d · U'_d(x) · [shift_{d/√3}(V·ψ)](x)
                  = Σ_d M_d · U'_d(x) · V(x+d/√3) · [shift_{d/√3}ψ](x)

    For V·ψ'(x) = ψ'_new(x): V(x)·U_d(x) = U'_d(x)·V(x+d/√3), giving
    U'_d(x) = V(x) · U_d(x) · V†(x+d/√3).  With fractional shifts,
    V(x+d/√3) is evaluated exactly, so the identity holds to FFT round-off.

    Contrast
    --------
    gauge_transform_links uses integer np.roll, giving V(x+d_int)·U·V†(x).
    That convention matches a real-space hop of distance d_int = 1 per axis,
    whereas the BCC kinetic hop is d/√3 per axis.  The mismatch is O(a) for
    smooth V, which is why the W1.4 Ward residual is ~0.04 with the old pair.

    Parameters
    ----------
    U_links : list of 8 (U_a, U_b) tuples from make_w_link_field.
    V_a, V_b : complex128 (Lx,Ly,Lz) — local SU(2) gauge transformation.

    Returns
    -------
    U_links_new : list of 8 transformed (U_a, U_b) tuples.
    """
    from ca_bcc import bcc_fractional_shift

    shape = V_a.shape
    KX, KY, KZ = _kgrid3d(*shape)

    # Forward FFT of V†'s (α,β) components for fractional shifting.
    # V = [[Va, -Vb*],[Vb, Va*]]  →  V† = [[Va*, Vb*],[-Vb, Va]]
    # In canonical SU(2) (α,β) form for V†: α = conj(Va), β = -Vb.
    Vdag_a_k = _fft.fftn(np.conj(V_a))   # FFT of α of V†
    Vdag_b_k = _fft.fftn(-V_b)            # FFT of β of V†

    U_links_new = []
    for i, ((U_a, U_b), (dx, dy, dz)) in enumerate(zip(U_links, BCC_DIRS)):

        # ── V†(x + d/√3): fractional-shift V† in k-space ────────────────────
        Vdag_sh_a = _fft.ifftn(
            bcc_fractional_shift(Vdag_a_k, KX, KY, KZ, dx, dy, dz))
        Vdag_sh_b = _fft.ifftn(
            bcc_fractional_shift(Vdag_b_k, KX, KY, KZ, dx, dy, dz))

        # ── Step 1: mid = V(x) · U_d(x) ─────────────────────────────────────
        # SU(2) product (a1,b1)·(a2,b2): a = a1·a2 − b1*·b2, b = b1·a2 + a1*·b2
        mid_a = V_a * U_a - np.conj(V_b) * U_b
        mid_b = V_b * U_a + np.conj(V_a) * U_b

        # ── Step 2: result · V†(x+d/√3) ─────────────────────────────────────
        # V†_sh as (α,β) = (Vdag_sh_a, Vdag_sh_b).
        # (mid)·(V†_sh): a = mid_a·Vdag_sh_a − conj(mid_b)·Vdag_sh_b
        #                b = mid_b·Vdag_sh_a + conj(mid_a)·Vdag_sh_b
        new_a = mid_a * Vdag_sh_a - np.conj(mid_b) * Vdag_sh_b
        new_b = mid_b * Vdag_sh_a + np.conj(mid_a) * Vdag_sh_b

        U_links_new.append((new_a, new_b))

    return U_links_new


# ═══════════════════════════════════════════════════════════════════
#  Phase 2 — Free W propagation (F26 rotation law per a-component)
# ═══════════════════════════════════════════════════════════════════

def extract_EW_BW(U_links, L=None):
    """
    Extract linearized (E_W^a, B_W^a) from the link field.

    In the small-amplitude limit U_ℓ ≈ I + (i/2)τ^a W_ℓ^a, the
    W^a field components per link are:
        W^1 = 2·Im(U_b),   W^2 = −2·Re(U_b),   W^3 = 2·Im(U_a)

    We form site-centred W^a_x, W^a_y, W^a_z by averaging link values
    weighted by the link's projection onto each Cartesian axis, then
    compute E^a = −∂_t W^a and B^a = ∇ × W^a using spectral derivatives.
    Here we return the averaged Cartesian components as a proxy for (E,B)
    so that the rotation law can be applied per a.

    Returns
    -------
    W_vec : (3, 3, Lx, Ly, Lz) float — W_vec[a, mu] = W^a_mu field.
            a ∈ {0,1,2} (isospin), mu ∈ {0,1,2} (x,y,z).
    """
    if L is None:
        L = U_links[0][0].shape

    W = np.zeros((3,) + L, dtype=complex)  # W^a averaged over all links

    for i, (dx, dy, dz) in enumerate(BCC_DIRS):
        U_a, U_b = U_links[i]
        # Linearized W^a components from this link
        w1 = 2.0 * np.imag(U_b)
        w2 = -2.0 * np.real(U_b)
        w3 = 2.0 * np.imag(U_a)
        # Weight by the link direction vector (unnormalised)
        W[0] += w1
        W[1] += w2
        W[2] += w3

    W /= 8.0  # average over 8 links
    return W.real


def _f26_rotation_step(E_k, B_k, KX, KY, KZ):
    """
    Apply one tick of the F26 rotation law in Fourier space:
        [E(k,t+1), B(k,t+1)] = R(Ω(k)) · [E(k,t), B(k,t)]
    where Ω(k) = ω_+(k/2) + ω_-(k/2) (symmetrized / even dispersion),
    and R is a 2×2 real rotation.

    Symmetrization note
    -------------------
    The BCC dispersion ω_+(k) is NOT even in k: ω_+(-k) = ω_-(k) ≠ ω_+(k).
    For real-valued W fields (gauge potentials), applying a chirally asymmetric
    rotation would break Hermitian symmetry of the Fourier coefficients, causing
    IFFT imaginary parts and energy non-conservation.  The correct prescription
    for a real field is the EVEN dispersion:

        Ω_even(k) = [Ω_+(k) + Ω_+(-k)] / 2
                  = [2ω_+(k/2) + 2ω_+(−k/2)] / 2
                  = ω_+(k/2) + ω_-(k/2)

    which is manifestly even.  This preserves real-field Hermitian symmetry
    exactly, so IFFT(rotation · FFT(E_real)) is real to FFT round-off.

    Physical interpretation: the real W gauge potential is the sum of a
    positive-chirality and negative-chirality mode; the even dispersion averages
    over both.  In the continuum limit both chiralities give the same dispersion
    ω → c|k|, so Ω_even → 2c|k| = Ω_+ = Ω_- (no difference at low k).

    Works directly on the Fourier-space arrays E_k, B_k.
    Returns updated E_k_new, B_k_new.
    """
    # Symmetrized (even) dispersion for real W fields
    omega_p = bcc_dispersion(KX / 2.0, KY / 2.0, KZ / 2.0, sign='+')
    omega_m = bcc_dispersion(KX / 2.0, KY / 2.0, KZ / 2.0, sign='-')
    Omega = omega_p + omega_m   # = [Ω_+(k) + Ω_+(-k)] / 1, the even sum
    cos_O = np.cos(Omega)
    sin_O = np.sin(Omega)
    E_new_k = cos_O * E_k + sin_O * B_k
    B_new_k = -sin_O * E_k + cos_O * B_k
    return E_new_k, B_new_k


def _chiral_dispersions(shape):
    """
    Compute (Op, Om) = (Ω⁺, Ω⁻) for the chiral propagation step, with
    Nyquist-bin correction for even-length grids.

    The BCC chirality constraint  Ω⁺(−k) = Ω⁻(k)  makes the chiral step
    exactly unitary for real fields — EXCEPT at DFT Nyquist bins.

    For even L, the Nyquist index L/2 maps to itself under negation:
      (−L/2) % L = L/2.  The kgrid stores kx = −π there, but the physical
      conjugate of −π is +π.  Since bcc_dispersion(−π/2) ≠ bcc_dispersion(+π/2),
      the constraint fails and the chiral phase factor is not unitary for those
      modes → taking .real after IFFT leaks energy (~3–12 % per step for L=16/32).

    Fix: at Nyquist bins, set Op = Om = (Ω⁺ + Ω⁻)/2 (the even/symmetric
    dispersion).  Those bins are self-conjugate in the DFT, so the two helicity
    branches are indistinguishable there — the even average is the physically
    correct choice.  Non-Nyquist bins are unaffected (Op, Om unchanged).

    Odd L: no Nyquist bin; correction mask is all-False; no overhead.

    Returns
    -------
    Op : (Lx, Ly, Lz) array — Ω⁺, corrected at Nyquist bins
    Om : (Lx, Ly, Lz) array — Ω⁻, corrected at Nyquist bins
    """
    KX, KY, KZ = _kgrid3d(*shape)
    omega_p = bcc_dispersion(KX / 2, KY / 2, KZ / 2, sign='+')
    omega_m = bcc_dispersion(KX / 2, KY / 2, KZ / 2, sign='-')
    Op = 2.0 * omega_p
    Om = 2.0 * omega_m

    # Build Nyquist mask: True at any index equal to L//2 (only non-trivial for even L)
    nyq_mask = np.zeros(shape, dtype=bool)
    for axis, L in enumerate(shape):
        if L % 2 == 0:
            idx = [slice(None)] * 3
            idx[axis] = L // 2
            nyq_mask[tuple(idx)] = True

    if nyq_mask.any():
        Omega_even = Op + Om   # = ω_+(k/2) + ω_-(k/2), the original even dispersion
        Op = np.where(nyq_mask, Omega_even * 0.5, Op)
        Om = np.where(nyq_mask, Omega_even * 0.5, Om)

    return Op, Om


def w_propagation_step_chiral(E_W, B_W):
    """
    Chirality-faithful W-field propagation (F37).

    Each Riemann–Silberstein eigenstate propagates at its own BCC branch:
        F⁺(k) = E_k + i·B_k  →  exp(−i·Ω⁺(k))·F⁺(k),   Ω⁺ = 2·ω_+(k/2)
        F⁻(k) = E_k − i·B_k  →  exp(+i·Ω⁻(k))·F⁻(k),   Ω⁻ = 2·ω_-(k/2)

    Nyquist bins on even grids use the even-dispersion average (see
    _chiral_dispersions for the full explanation).  Energy is conserved
    to ≤ 1e-13 relative drift for any grid size.
    """
    shape = E_W.shape[1:]
    Op, Om = _chiral_dispersions(shape)
    E_new = np.zeros_like(E_W)
    B_new = np.zeros_like(B_W)
    for a in range(3):
        Ek = _fft.fftn(E_W[a])
        Bk = _fft.fftn(B_W[a])
        Fp = Ek + 1j * Bk   # F⁺ eigenstate  (eigenvalue exp(−iΩ⁺))
        Fm = Ek - 1j * Bk   # F⁻ eigenstate  (eigenvalue exp(+iΩ⁻))
        Fp_new = np.exp(-1j * Op) * Fp
        Fm_new = np.exp(+1j * Om) * Fm
        E_new[a] = _fft.ifftn((Fp_new + Fm_new) * 0.5).real
        B_new[a] = _fft.ifftn((Fp_new - Fm_new) * (-0.5j)).real
    return E_new, B_new


# F37 (2026-05-24): w_propagation_step_spectral is now the chirally-faithful
# split-basis propagation (F+ at Ω⁺=2ω_+(k/2), F- at Ω⁻=2ω_-(k/2)), replacing
# the previous even-dispersion single-rotation step (_f26_rotation_step).
# The old even step is kept as _f26_rotation_step for the B-field and massive-W
# paths where the even dispersion is still the correct choice.
w_propagation_step_spectral = w_propagation_step_chiral


def w_free_dispersion_check(L=32, n_steps=200, a_comp=0, seed=7):
    """
    Measure the W-field dispersion Ω_W(k) from a plane-wave initialisation
    and compare to the predicted F37 / F26 value Ω⁺(k) = 2·ω_+(k/2).

    Initialises a single-mode (E^a, B^a) plane wave, evolves for n_steps
    using w_propagation_step_spectral (the chirally-faithful chiral step),
    and extracts the oscillation frequency from the final phase of the
    F+ = E_k + i·B_k eigenstate.

    Under the chiral step:
        F+(k, n) = F+(k, 0) · exp(−i·Ω⁺(k)·n)   where Ω⁺ = 2·ω_+(k/2)
        F-(k, n) = F-(k, 0) · exp(+i·Ω⁻(k)·n)   where Ω⁻ = 2·ω_-(k/2)

    C0 = E_k + i·B_k = F+ in Fourier space, so it tracks the Ω⁺ branch.

    Returns
    -------
    max_rel_err : float — max |Ω⁺_measured − Ω⁺_predicted| / Ω⁺_predicted
                  over all non-zero k modes.
    """
    rng = np.random.default_rng(seed=seed)
    # Random initial condition: a small random (E, B) field
    E_W = np.zeros((3, L, L, L))
    B_W = np.zeros((3, L, L, L))
    E_W[a_comp] = rng.standard_normal((L, L, L))
    B_W[a_comp] = rng.standard_normal((L, L, L))

    # Record initial Fourier-space F+ amplitudes: C0 = E_k + i*B_k
    KX, KY, KZ = _kgrid3d(L, L, L)
    E0_k = _fft.fftn(E_W[a_comp])
    B0_k = _fft.fftn(B_W[a_comp])
    C0 = E0_k + 1j * B0_k

    for _ in range(n_steps):
        E_W, B_W = w_propagation_step_spectral(E_W, B_W)

    En_k = _fft.fftn(E_W[a_comp])
    Bn_k = _fft.fftn(B_W[a_comp])
    Cn = En_k + 1j * Bn_k

    # Predicted: Ω⁺(k) from _chiral_dispersions (includes Nyquist correction).
    # Nyquist bins use the even average (Op+Om)/2; non-Nyquist use 2·ω_+(k/2).
    # The prediction must match _chiral_dispersions exactly to avoid spurious errors.
    Omega_pred, _ = _chiral_dispersions((L, L, L))

    # Under the chiral step: F+_n = F+_0 · exp(−i·Ω⁺·n_steps)
    # Compare measured final F+ against the expected evolved F+.
    C_expected = C0 * np.exp(-1j * Omega_pred * n_steps)
    amp0 = np.abs(C0)
    sig = amp0 > 1e-8 * np.max(amp0)
    rel_err = np.where(sig, np.abs(Cn - C_expected) / (amp0 + 1e-30), 0.0)
    return float(np.max(rel_err))


# ═══════════════════════════════════════════════════════════════════
#  Phase 3 — Non-Abelian self-coupling (Yang–Mills)
# ═══════════════════════════════════════════════════════════════════

# SU(2) structure constants: ε^{abc} (Levi-Civita)
_EPS = np.zeros((3, 3, 3), dtype=float)
_EPS[0, 1, 2] = _EPS[1, 2, 0] = _EPS[2, 0, 1] = 1.0
_EPS[0, 2, 1] = _EPS[2, 1, 0] = _EPS[1, 0, 2] = -1.0


def _su2_product(a1, b1, a2, b2):
    """SU(2) matrix product: [[a,-b*],[b,a*]] · [[a2,-b2*],[b2,a2*]]."""
    a_out = a1 * a2 - np.conj(b1) * b2
    b_out = b1 * a2 + np.conj(a1) * b2
    return a_out, b_out


def plaquette_field_strength(U_links, g_lat=1.0):
    """
    Compute the SU(2) field strength F^a_{μν}(x) from BCC link variables
    using composite plaquettes.

    We construct 6 effective straight-line links along ±x, ±y, ±z by
    composing two BCC half-steps.  The +x effective link at site x is:
        U_x(x) = U_{(+1,+1,+1)}(x) · U_{(+1,−1,−1)}(x+(1,1,1))
    (and analogously for y, z).

    Wilson plaquette in the xy-plane:
        P_xy(x) = U_x(x) U_y(x+2ê_x) U_x†(x+2ê_y) U_y†(x)

    The field strength is extracted from P ≈ I + ig·a²·τ^a·F^a_{xy}:
        F^a_{xy} ≈ −2/(g·a²) · Im(tr(τ^a · P))  (leading order in g)

    Returns
    -------
    F : dict with keys ('xy','xz','yz') each of shape (3, Lx, Ly, Lz).
        F['xy'][a] = F^a_{xy}(x).
    """
    # Build 6 effective SC links from BCC pairs
    # +x: dirs (1,1,1) and (1,-1,-1)
    _idx = {tuple(d): i for i, d in enumerate(BCC_DIRS.tolist())}

    def _eff_link(d1, d2):
        """U_d1(x) · U_d2(x+d1)."""
        i1, i2 = _idx[d1], _idx[d2]
        a1, b1 = U_links[i1]
        a2, b2 = U_links[i2]
        dx, dy, dz = d1
        a2_shifted = np.roll(np.roll(np.roll(a2, -dx, 0), -dy, 1), -dz, 2)
        b2_shifted = np.roll(np.roll(np.roll(b2, -dx, 0), -dy, 1), -dz, 2)
        return _su2_product(a1, b1, a2_shifted, b2_shifted)

    # Effective links in +x, +y, +z (composite of two BCC hops)
    Ux = _eff_link((1, 1, 1), (1, -1, -1))   # +x, magnitude 2
    Uy = _eff_link((1, 1, 1), (-1, 1, -1))   # +y, magnitude 2
    Uz = _eff_link((1, 1, 1), (-1, -1, 1))   # +z, magnitude 2

    def _dagger(a, b):
        return np.conj(a), -b

    def _plaquette(Ua, Ub_pair, shift1, Va_pair, Vb_pair, shift2):
        """P = U(x) V(x+shift1) U†(x+shift2) V†(x)."""
        U_a, U_b = Ua, Ub_pair
        dx1, dy1, dz1 = shift1
        V_a = np.roll(np.roll(np.roll(Va_pair, -dx1, 0), -dy1, 1), -dz1, 2)
        V_b = np.roll(np.roll(np.roll(Vb_pair, -dx1, 0), -dy1, 1), -dz1, 2)
        # UV
        UV_a, UV_b = _su2_product(U_a, U_b, V_a, V_b)
        # U†(x+shift2)
        dx2, dy2, dz2 = shift2
        Uda = np.roll(np.roll(np.roll(np.conj(U_a), -dx2, 0), -dy2, 1), -dz2, 2)
        Udb = np.roll(np.roll(np.roll(-U_b, -dx2, 0), -dy2, 1), -dz2, 2)
        UVUd_a, UVUd_b = _su2_product(UV_a, UV_b, Uda, Udb)
        # V†(x)
        Vd_a, Vd_b = _dagger(Va_pair, Vb_pair)
        Vd_a_loc = np.roll(np.roll(np.roll(Vd_a, 0, 0), 0, 1), 0, 2)
        Vd_b_loc = np.roll(np.roll(np.roll(Vd_b, 0, 0), 0, 1), 0, 2)
        Pa, Pb = _su2_product(UVUd_a, UVUd_b, Vd_a_loc, Vd_b_loc)
        return Pa, Pb

    # Wilson plaquettes in xy, xz, yz planes
    # P_xy = Ux(x) · Uy(x+2ex) · Ux†(x+2ey) · Uy†(x)
    Ux_a, Ux_b = Ux
    Uy_a, Uy_b = Uy
    Uz_a, Uz_b = Uz

    def _shift(arr, dx, dy, dz):
        return np.roll(np.roll(np.roll(arr, -dx, 0), -dy, 1), -dz, 2)

    # P_xy
    step1_a, step1_b = _su2_product(Ux_a, Ux_b,
                                     _shift(Uy_a, 2, 0, 0), _shift(Uy_b, 2, 0, 0))
    step2_a, step2_b = _su2_product(step1_a, step1_b,
                                     np.conj(_shift(Ux_a, 0, 2, 0)), _shift(-Ux_b, 0, 2, 0))
    Pxy_a, Pxy_b = _su2_product(step2_a, step2_b, np.conj(Uy_a), -Uy_b)

    # P_xz
    step1_a, step1_b = _su2_product(Ux_a, Ux_b,
                                     _shift(Uz_a, 2, 0, 0), _shift(Uz_b, 2, 0, 0))
    step2_a, step2_b = _su2_product(step1_a, step1_b,
                                     np.conj(_shift(Ux_a, 0, 0, 2)), _shift(-Ux_b, 0, 0, 2))
    Pxz_a, Pxz_b = _su2_product(step2_a, step2_b, np.conj(Uz_a), -Uz_b)

    # P_yz
    step1_a, step1_b = _su2_product(Uy_a, Uy_b,
                                     _shift(Uz_a, 0, 2, 0), _shift(Uz_b, 0, 2, 0))
    step2_a, step2_b = _su2_product(step1_a, step1_b,
                                     np.conj(_shift(Uy_a, 0, 0, 2)), _shift(-Uy_b, 0, 0, 2))
    Pyz_a, Pyz_b = _su2_product(step2_a, step2_b, np.conj(Uz_a), -Uz_b)

    # Extract F^a from P ≈ I + ig·a²·τ^a·F^a  →  F^a ≈ 2·Im(τ^a·P) / (g·a²)
    # tr(τ^1·P) = tr([[0,1],[1,0]]·[[Pa,-Pb*],[Pb,Pa*]]) = Pb + (-Pb*) ... hmm
    # τ^1 = [[0,1],[1,0]]: tr(τ^1·M) = M[0,1] + M[1,0] = (-Pb*) + Pb = 2i·Im(Pb)
    # τ^2 = [[0,-i],[i,0]]: tr(τ^2·M) = -i·M[0,1] + i·M[1,0] = -i(-Pb*) + i·Pb = i(Pb+Pb*) = 2i·Re(Pb)
    # τ^3 = [[1,0],[0,-1]]: tr(τ^3·M) = M[0,0] - M[1,1] = (Pa - Pa*) = 2i·Im(Pa)
    # So:  F^1 = Im(Pb)/g,  F^2 = Re(Pb)/g,  F^3 = Im(Pa)/g   (up to lattice factors)
    a2 = 4.0  # plaquette area: 2×2 lattice units

    def _extract_F(P_a, P_b):
        F = np.zeros((3,) + P_a.shape)
        F[0] = np.imag(P_b) / (g_lat * a2)
        F[1] = np.real(P_b) / (g_lat * a2)
        F[2] = np.imag(P_a) / (g_lat * a2)
        return F

    return {
        'xy': _extract_F(Pxy_a, Pxy_b),
        'xz': _extract_F(Pxz_a, Pxz_b),
        'yz': _extract_F(Pyz_a, Pyz_b),
    }


def w_self_interaction_step(U_links, dt=0.05, g_lat=1.0):
    """
    One step of the non-Abelian self-interaction update.

    In the continuum, the Yang–Mills equation of motion has a source term
        D^μ F_μν^a = 0   (vacuum, no matter)
    At the link level we implement a Strang-split: free propagation (Phase 2)
    handles the linear part; this function adds the commutator correction
        δU_ℓ^a ≈ dt · g · ε^{abc} · W_ℓ^b · F_ℓ^c
    via an infinitesimal SU(2) rotation of each link by the self-coupling term.

    For small g and short dt this is a first-order integrator for the
    non-Abelian part.  The Bianchi identity (W3.2) tests structural correctness.
    """
    F = plaquette_field_strength(U_links, g_lat=g_lat)
    W_vec = extract_EW_BW(U_links)  # shape (3, Lx, Ly, Lz)

    # Compute commutator contribution: δW^a = g·ε^{abc}·W^b·F_xy^c  (using xy-plane)
    F_avg = (F['xy'] + F['xz'] + F['yz']) / 3.0  # average over planes

    delta_W = np.zeros_like(W_vec)
    for a in range(3):
        for b in range(3):
            for c in range(3):
                delta_W[a] += _EPS[a, b, c] * W_vec[b] * F_avg[c]
    delta_W *= g_lat * dt

    # Update links via exp(i·δW^a·τ^a/2) applied as small SU(2) rotation
    # For small δW: δU_a ≈ 1, δU_b ≈ i·δW_complex/2 where δW_complex = δW^1 + i·δW^2
    delta_W3 = delta_W[2]  # for U_a update
    delta_Wc = delta_W[0] + 1j * delta_W[1]  # for U_b update

    # Build the small-rotation SU(2) element R = exp(i·δW^a·τ^a/2)
    theta = np.sqrt(delta_W[0]**2 + delta_W[1]**2 + delta_W[2]**2)
    safe = theta > 1e-14
    sinc = np.where(safe, np.sin(theta / 2.0) / np.where(safe, theta, 1.0), 0.5)
    R_a = np.cos(theta / 2.0) + 1j * delta_W3 * sinc
    R_b = (delta_W[1] + 1j * delta_W[0]) * sinc  # (δW^2 + i·δW^1) component

    # Apply R to each link: U_ℓ → R · U_ℓ
    U_links_new = []
    for (U_a, U_b) in U_links:
        new_a, new_b = _su2_product(R_a, R_b, U_a, U_b)
        U_links_new.append((new_a, new_b))
    return U_links_new


def bianchi_residual(F):
    """
    Compute the Bianchi identity residual D_{[μ}F_{νρ]}^a ≈ 0 in the
    continuum / linearized limit using spectral derivatives.

    For an abelian field (g→0), the Bianchi identity is exact:
        ∂_x F_yz + ∂_y F_zx + ∂_z F_xy = 0  (per a-component).

    Returns max_a max_x |∂_x F^a_yz + ∂_y F^a_zx + ∂_z F^a_xy|.
    """
    shape = F['xy'].shape[1:]
    KX, KY, KZ = _kgrid3d(*shape)

    max_res = 0.0
    for a in range(3):
        Fxy_k = _fft.fftn(F['xy'][a])
        Fxz_k = _fft.fftn(F['xz'][a])
        Fyz_k = _fft.fftn(F['yz'][a])
        # ∂_z F_xy + ∂_y F_xz(-F_zx) + ∂_x F_yz  (using spectral ik)
        bianchi_k = 1j * KZ * Fxy_k - 1j * KY * Fxz_k + 1j * KX * Fyz_k
        bianchi_r = _fft.ifftn(bianchi_k)
        res = float(np.max(np.abs(bianchi_r)))
        if res > max_res:
            max_res = res
    return max_res


# ═══════════════════════════════════════════════════════════════════
#  Phase 4 — Fermion–W_μ vertex (covariant derivative for doublet)
# ═══════════════════════════════════════════════════════════════════

def fermion_current_isospin(f_nu, f_e, g_nu, g_e):
    """
    Compute the isospin current J^{a,μ} = ψ̄_L γ^μ τ^a ψ_L at the
    bilinear level (reusing F29 W-triplet construction).

    We compute the spatial current density J^a_i = η† σ^i τ^a η where
    η = (η_ν, η_e) is the left-handed doublet (f component only,
    χ does not couple to W — parity violation test W4.3).

    Parameters
    ----------
    f_nu, f_e : (Lx,Ly,Lz) upper Weyl components (left-handed doublet)
    g_nu, g_e : (Lx,Ly,Lz) lower Weyl components

    Returns
    -------
    J : (3, 3, Lx, Ly, Lz) — J[a, mu] = J^{a,mu}
        a = isospin index (0,1,2 ↔ a=1,2,3)
        mu = spatial direction (0,1,2 ↔ x,y,z)
    """
    shape = f_nu.shape
    # Left-handed doublet in spin space
    eta = np.array([[f_nu, f_e],    # spin-up, isospin (ν, e)
                    [g_nu, g_e]])   # spin-down, isospin (ν, e)

    # Pauli matrices (spin)
    sigma = [
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    ]
    # Isospin Pauli matrices (tau)
    tau = [
        np.array([[0, 1], [1, 0]], dtype=complex),
        np.array([[0, -1j], [1j, 0]], dtype=complex),
        np.array([[1, 0], [0, -1]], dtype=complex),
    ]

    J = np.zeros((3, 3) + shape, dtype=complex)
    for a in range(3):
        for mu in range(3):
            # J^a_mu = Σ_{s,s',α,α'} η†[s,α] * σ^mu[s,s'] * τ^a[α,α'] * η[s',α']
            for s in range(2):
                for sp in range(2):
                    for alpha in range(2):
                        for alphap in range(2):
                            J[a, mu] += (np.conj(eta[s, alpha]) *
                                         sigma[mu][s, sp] *
                                         tau[a][alpha, alphap] *
                                         eta[sp, alphap])
    return J.real


def covariant_dirac_doublet_step(f_nu, f_e, g_nu, g_e,
                                 chi_nu_f, chi_e_f, chi_nu_g, chi_e_g,
                                 U_links, U_a_mass, U_b_mass,
                                 m, dt=1.0):
    """
    Full Dirac step for an SU(2) doublet with covariant kinetic term and
    complex-mass coupling (closes F27 limitations #1 and #2).

    Strang split: kinetic(dt/2) → mass(dt) → kinetic(dt/2).

    Kinetic step: covariant_weyl_step_3d_bcc applied to η (left-handed, sign='+')
                  and χ (right-handed, sign='-') with U_links.
    Mass step: F27 complex-mass doublet coupling with U_mass field.

    For χ: the kinetic step uses U_links for the isospin structure, but
    since χ is a SU(2)_L singlet (doesn't transform), we pass identity links.
    Test W4.3 verifies right-handed sector does not couple.

    Returns all 8 updated spinor components.
    """
    from ca_bcc import weyl_step_3d_bcc
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))

    cm = np.cos(m * dt)
    sm = np.sin(m * dt)

    # Half kinetic step: left-handed doublet with gauge links
    f_nu_h, f_e_h, g_nu_h, g_e_h = covariant_weyl_step_3d_bcc(
        f_nu, f_e, g_nu, g_e, U_links, sign='+')

    # Right-handed uses identity links (no SU(2)_L coupling)
    id_links = make_w_link_field(f_nu.shape[0], mode='identity')
    cf_nu_h, cf_e_h, cg_nu_h, cg_e_h = covariant_weyl_step_3d_bcc(
        chi_nu_f, chi_e_f, chi_nu_g, chi_e_g, id_links, sign='-')

    # Mass step (F27 complex-mass SU(2) doublet coupling)
    # η_new = cm*η + i*sm*(U⊗I)*χ
    # χ_new = i*sm*(U†⊗I)*η + cm*χ
    U_a, U_b = U_a_mass, U_b_mass
    # Apply (U⊗I) to χ: acts on isospin, not spin
    Uchi_f_nu = U_a * cf_nu_h - np.conj(U_b) * cf_e_h
    Uchi_f_e  = U_b * cf_nu_h + np.conj(U_a) * cf_e_h
    Uchi_g_nu = U_a * cg_nu_h - np.conj(U_b) * cg_e_h
    Uchi_g_e  = U_b * cg_nu_h + np.conj(U_a) * cg_e_h
    # Apply (U†⊗I) to η
    Udeta_f_nu = np.conj(U_a) * f_nu_h + np.conj(U_b) * f_e_h
    Udeta_f_e  = -U_b * f_nu_h + U_a * f_e_h
    Udeta_g_nu = np.conj(U_a) * g_nu_h + np.conj(U_b) * g_e_h
    Udeta_g_e  = -U_b * g_nu_h + U_a * g_e_h

    f_nu_m = cm * f_nu_h + 1j * sm * Uchi_f_nu
    f_e_m  = cm * f_e_h  + 1j * sm * Uchi_f_e
    g_nu_m = cm * g_nu_h + 1j * sm * Uchi_g_nu
    g_e_m  = cm * g_e_h  + 1j * sm * Uchi_g_e

    cf_nu_m = 1j * sm * Udeta_f_nu + cm * cf_nu_h
    cf_e_m  = 1j * sm * Udeta_f_e  + cm * cf_e_h
    cg_nu_m = 1j * sm * Udeta_g_nu + cm * cg_nu_h
    cg_e_m  = 1j * sm * Udeta_g_e  + cm * cg_e_h

    # Second half kinetic step
    f_nu_out, f_e_out, g_nu_out, g_e_out = covariant_weyl_step_3d_bcc(
        f_nu_m, f_e_m, g_nu_m, g_e_m, U_links, sign='+')
    cf_nu_out, cf_e_out, cg_nu_out, cg_e_out = covariant_weyl_step_3d_bcc(
        cf_nu_m, cf_e_m, cg_nu_m, cg_e_m, id_links, sign='-')

    return (f_nu_out, f_e_out, g_nu_out, g_e_out,
            cf_nu_out, cf_e_out, cg_nu_out, cg_e_out)


# ═══════════════════════════════════════════════════════════════════
#  Phase 5B — W mass generation (Stueckelberg / Ludwig)
# ═══════════════════════════════════════════════════════════════════

def make_stueckelberg_field(L, mode='identity', seed=13):
    """
    Initialise the Stueckelberg SU(2) field U_st(x) — a site-centred
    SU(2) field that, when given a kinetic term |∂_μ U_st|², generates W mass.

    In F27, U(x) was demonstrated pure-gauge (no physical d.o.f.).  Here
    we promote it to a dynamical field by adding a kinetic term.

    Returns
    -------
    U_st_a, U_st_b : (Lx,Ly,Lz) complex — the SU(2) Stueckelberg field.
    """
    if isinstance(L, int):
        shape = (L, L, L)
    else:
        shape = tuple(L)
    rng = np.random.default_rng(seed=seed)

    if mode == 'identity':
        return (np.ones(shape, dtype=complex), np.zeros(shape, dtype=complex))
    elif mode == 'random':
        raw = rng.standard_normal(shape + (4,))
        norms = np.linalg.norm(raw, axis=-1, keepdims=True)
        q = raw / norms
        return (q[..., 0] + 1j * q[..., 3], q[..., 2] + 1j * q[..., 1])
    else:
        raise ValueError(f"Unknown mode {mode!r}")


def stueckelberg_mass_term(U_st_a, U_st_b, g_lat=1.0):
    """
    Compute the Stueckelberg mass contribution to the W field.

    The Stueckelberg kinetic Lagrangian (chiral / nonlinear-sigma style):
        ℒ_st = (f²/2) tr[(∂_μ U_st)(∂^μ U_st†)]

    This generates a W-mass term m_W² W^a_μ W^{a,μ} / 2 with m_W = g·f
    (Stueckelberg mass formula), where f is the decay constant.

    In the CA: we approximate ∂_μ U_st(x) by finite differences of the
    site-centered U_st field and extract the effective mass term.

    Returns
    -------
    mass_field : (3, Lx, Ly, Lz) — effective mass correction to W^a,
                 to be added to the link update in w_self_interaction_step.
    m_W_estimate : float — estimated W mass from the field configuration.
    """
    shape = U_st_a.shape
    KX, KY, KZ = _kgrid3d(*shape)

    # Spectral derivatives of U_st components
    Ua_k = _fft.fftn(U_st_a)
    Ub_k = _fft.fftn(U_st_b)

    # |∂_x U_st_a|² + |∂_y U_st_a|² + |∂_z U_st_a|² (kinetic for U_a)
    kin_a = (np.abs(_fft.ifftn(1j * KX * Ua_k))**2 +
             np.abs(_fft.ifftn(1j * KY * Ua_k))**2 +
             np.abs(_fft.ifftn(1j * KZ * Ua_k))**2)
    kin_b = (np.abs(_fft.ifftn(1j * KX * Ub_k))**2 +
             np.abs(_fft.ifftn(1j * KY * Ub_k))**2 +
             np.abs(_fft.ifftn(1j * KZ * Ub_k))**2)

    # Estimate m_W from field configuration (spatial average of kinetic energy)
    kinetic_energy = np.mean(kin_a + kin_b)
    m_W_estimate = g_lat * np.sqrt(np.maximum(kinetic_energy, 0.0))

    # Mass correction to W^a fields (proportional to W^a itself)
    W_vec = np.zeros((3,) + shape)  # placeholder: actual coupling enters in evolution
    W_vec[2] = np.imag(U_st_a)     # W^3 ~ Im(U_a) (Stueckelberg identification)
    W_vec[0] = np.imag(U_st_b)     # W^1 ~ Im(U_b)
    W_vec[1] = -np.real(U_st_b)    # W^2 ~ -Re(U_b)

    mass_field = g_lat**2 * W_vec
    return mass_field, m_W_estimate


def wmu_mass_stueckelberg(U_links, U_st_a, U_st_b, dt=1.0, g_lat=1.0):
    """
    Apply one W-mass step via Stueckelberg mechanism.

    The Stueckelberg field U_st(x) generates a mass for W^a via the
    kinetic term |D_μ U_st|² = |∂_μ U_st − ig W^a_μ τ^a U_st|².

    This is the non-linear σ-model / Stückelberg approach: U_st acts as
    the would-be Goldstone boson that is "eaten" by W to gain mass.

    Step: update U_st via its equation of motion, then update U_links to
    incorporate the mass-induced correction.

    Returns
    -------
    U_links_new : updated link field (W acquired mass correction).
    U_st_a_new, U_st_b_new : evolved Stueckelberg field.
    """
    mass_field, m_W = stueckelberg_mass_term(U_st_a, U_st_b, g_lat=g_lat)

    # Update Stueckelberg field: U_st evolves under covariant gradient flow
    # δU_st/δt = ΔU_st (lattice Laplacian)
    shape = U_st_a.shape
    KX, KY, KZ = _kgrid3d(*shape)
    lap = -(KX**2 + KY**2 + KZ**2)  # spectral Laplacian eigenvalue

    Ua_k = _fft.fftn(U_st_a)
    Ub_k = _fft.fftn(U_st_b)

    # Gradient flow step
    Ua_new_k = Ua_k * np.exp(dt * lap)
    Ub_new_k = Ub_k * np.exp(dt * lap)
    Ua_new = _fft.ifftn(Ua_new_k)
    Ub_new = _fft.ifftn(Ub_new_k)

    # Re-unitarize (Gram-Schmidt on the SU(2) pair)
    norm = np.sqrt(np.abs(Ua_new)**2 + np.abs(Ub_new)**2)
    norm = np.where(norm > 1e-14, norm, 1.0)
    Ua_new /= norm
    Ub_new /= norm

    # Update links with mass correction: U_ℓ → exp(i·m²·W^a·τ^a·dt/2) · U_ℓ
    theta = np.sqrt(mass_field[0]**2 + mass_field[1]**2 + mass_field[2]**2) * dt
    safe = theta > 1e-14
    sinc = np.where(safe, np.sin(theta / 2) / np.where(safe, theta, 1.0), 0.5)
    R_a = np.cos(theta / 2) + 1j * mass_field[2] * dt * sinc
    R_b = (mass_field[1] + 1j * mass_field[0]) * dt * sinc

    U_links_new = []
    for (U_a, U_b) in U_links:
        new_a, new_b = _su2_product(R_a, R_b, U_a, U_b)
        U_links_new.append((new_a, new_b))

    return U_links_new, Ua_new, Ub_new


def measure_w_dispersion(E_W, B_W, n_steps=100, mass_correction=0.0):
    """
    Measure the W-field dispersion including a mass correction.

    For a massive W:  ω²(k) = m_W² + c²_lat |k|²

    Evolves (E_W, B_W) under w_propagation_step_spectral, measures the
    oscillation frequency per k-mode.

    Returns
    -------
    omega_sq : (Lx, Ly, Lz) measured ω²(k) per mode (component a=0).
    omega_sq_pred : (Lx, Ly, Lz) predicted from F26 + mass.
    """
    shape = E_W.shape[1:]
    KX, KY, KZ = _kgrid3d(*shape)

    # Evolve
    E0_k = _fft.fftn(E_W[0])
    B0_k = _fft.fftn(B_W[0])
    C0 = E0_k + 1j * B0_k

    for _ in range(n_steps):
        E_W, B_W = w_propagation_step_spectral(E_W, B_W)

    En_k = _fft.fftn(E_W[0])
    Bn_k = _fft.fftn(B_W[0])
    Cn = En_k + 1j * Bn_k

    phase = np.angle(Cn / np.where(np.abs(C0) > 1e-12, C0, 1.0))
    omega = np.abs(phase) / n_steps

    # Predicted (massless F26)
    omega_pred = 2.0 * bcc_dispersion(KX / 2.0, KY / 2.0, KZ / 2.0)

    return omega**2, omega_pred**2 + mass_correction**2


# ═══════════════════════════════════════════════════════════════════
#  Phase 5C — Covariant Stueckelberg kinetic (SU(2)_L × U(1)_Y)
#  2026-05-28
# ═══════════════════════════════════════════════════════════════════
#
# Promotes the inline operator originally written in
# `model-tests/test_wmu_phase6_rank1.py` (W6.9) into the main module so
# other tests / live runs can reuse it.  This implements the lattice
# version of
#
#     L_st = f² · Σ_{x,μ} tr[(D_μ U_st)†(D_μ U_st)]
#
#     D_μ U_st(x) = (1/a) [ W_μ(x) · U_st(x+μ̂) · V_μ†(x) - U_st(x) ]
#
# where W_μ(x) ∈ SU(2)_L is the parallel transporter for the SU(2)_L
# gauge field W^a, V_μ(x) = exp(i a (g'/2) B_μ(x) τ³) ∈ U(1)_Y is the
# parallel transporter for the hypercharge gauge field B (acting on the
# Stueckelberg field's right index — F41's Y_U = +1 doublet embedding),
# and a is the lattice spacing.
#
# F44 (rank-1 mass block) is the second variation of L_st in
# (W^1, W^2, W^3, B) at U_st = I.  W6.9 in the rank-1 test driver uses
# this operator to confirm det M²_{(W^3,B)} = 0 and the W^1/W^2 block
# is bit-for-bit decoupled at the lattice level.
#
# Convention notes
# ----------------
# * SU(2) Cayley-Klein form U = [[a, -b*], [b, a*]] — same as ca_wmu
#   throughout (matches make_w_link_field, _su2_product, ...).
# * Hypercharge link is stored as a single complex phase per site/dir
#   (|V| = 1), interpreted as the (0,0) entry of V_μ in the σ³ basis;
#   the (1,1) entry is its conjugate.  This matches the make_hypercharge_link_field
#   convention.
# * Generators T^a = τ^a/2 on the SU(2)_L side (standard SM); the U(1)_Y
#   side uses Y_U = +1 in the doublet representation, embedded as τ³ on
#   the right.  These are the conventions for which the F44 mass matrix
#   reduces to f²[[g², -g g'], [-g g', g'²]] with m_W = g·f, m_Z² =
#   f²(g²+g'²), and f = v/2 matches W6.3 / `stueckelberg_mass_term`
#   bit-for-bit at the SM physical point (80.415 / 91.226 GeV).
#
# Public API
# ----------
#   make_su2_link_uniform(W123, g, a_lat, shape)  → (W_a, W_b)
#   make_u1y_link_uniform(B,    gp, a_lat, shape) → V_phase
#   covariant_stueckelberg_difference(U_st_a, U_st_b, W_a, W_b, V_phase,
#                                     dx, dy, dz, a_lat)
#       → (DU_a, DU_b)  for a single link direction
#   covariant_stueckelberg_lagrangian(U_st_a, U_st_b,
#                                     W_links, V_links, f, a_lat)
#       → real, total Σ_{x,μ} contribution
#   covariant_stueckelberg_lagrangian_uniform(W123, B, g, gp, f, a_lat,
#                                             L, link_dirs)
#       → convenience wrapper for constant-field, U_st=I configurations

def _su2_right_mult_by_diag(M_a, M_b, p0):
    """
    Right-multiply SU(2) (in Cayley-Klein form [[a,-b*],[b,a*]]) by the
    diagonal matrix diag(p0, conj(p0)).  Returns (M'_a, M'_b) such that

        M' = [[a·p0, -b*·conj(p0)], [b·p0, a*·conj(p0)]]
           = [[A, -B*], [B, A*]]   with   A = a·p0,  B = b·p0.

    Used for the V_μ† right multiplication where V_μ = diag(p0*, p0)
    (so V_μ† = diag(p0, p0*)).
    """
    return M_a * p0, M_b * p0


def make_su2_link_uniform(W123, g, a_lat, shape):
    """
    Build a *uniform* SU(2)_L link field W_μ(x) = exp(i a (g/2) W^a τ^a)
    for a constant 3-vector W123 = (W^1, W^2, W^3).

    Returns (W_a, W_b) of shape `shape`, in Cayley-Klein form.
    """
    W1, W2, W3 = W123
    Wmag = float(np.sqrt(W1 * W1 + W2 * W2 + W3 * W3))
    theta = a_lat * (g / 2.0) * Wmag
    if Wmag < 1e-30:
        return (np.ones(shape, dtype=complex), np.zeros(shape, dtype=complex))
    nx, ny, nz = W1 / Wmag, W2 / Wmag, W3 / Wmag
    # exp(i θ (σ·n)) = cos θ · I + i sin θ · (σ·n)
    # Cayley-Klein:  a = cosθ + i sinθ · nz
    #                b = i sinθ · nx − sinθ · ny  =  sinθ·(i nx − ny)
    c, s = float(np.cos(theta)), float(np.sin(theta))
    W_a = (c + 1j * s * nz) * np.ones(shape, dtype=complex)
    W_b = (s * (1j * nx - ny)) * np.ones(shape, dtype=complex)
    return W_a, W_b


def make_u1y_link_uniform(B, gp, a_lat, shape):
    """
    Build a *uniform* U(1)_Y link phase V_μ(x) = exp(i a (g'/2) B · τ³)
    for constant B, returned as the (0,0) entry e^{+i a (g'/2) B} on each
    site (the (1,1) entry is its complex conjugate).
    """
    phase = complex(np.exp(1j * a_lat * (gp / 2.0) * B))
    return phase * np.ones(shape, dtype=complex)


def covariant_stueckelberg_difference(U_st_a, U_st_b, W_a, W_b, V_phase,
                                      dx, dy, dz, a_lat):
    """
    One-direction lattice covariant difference

        D_μ U_st(x) = (1/a) [ W_μ(x) · U_st(x+μ̂) · V_μ†(x) − U_st(x) ]

    in SU(2) Cayley-Klein form.  Returns (DU_a, DU_b) — the same parameter-
    isation, but representing a general 2×2 complex matrix (not necessarily
    in SU(2); the *difference* of two SU(2) matrices is generally not unitary).

    Parameters
    ----------
    U_st_a, U_st_b : (Lx, Ly, Lz) complex — Stueckelberg field at site x.
    W_a, W_b : (Lx, Ly, Lz) complex — SU(2)_L link variable for direction μ̂.
    V_phase  : (Lx, Ly, Lz) complex — U(1)_Y link phase for direction μ̂
                  (the (0,0) entry of V_μ; (1,1) entry = conj).
    dx, dy, dz : ints — link-direction offset.
    a_lat : float — lattice spacing.

    Returns
    -------
    DU_a, DU_b : (Lx, Ly, Lz) complex — Cayley-Klein components of D_μ U_st.
    """
    # Forward shift of U_st: site x sees U_st(x + d).  np.roll(arr, -d) maps
    # arr[x] = arr[x+d].
    Ust_a_sh = np.roll(np.roll(np.roll(U_st_a, -dx, 0), -dy, 1), -dz, 2)
    Ust_b_sh = np.roll(np.roll(np.roll(U_st_b, -dx, 0), -dy, 1), -dz, 2)

    # SU(2)_L parallel transport: W_μ(x) · U_st(x+d)
    inner_a, inner_b = _su2_product(W_a, W_b, Ust_a_sh, Ust_b_sh)

    # U(1)_Y right multiplication: ... · V_μ†(x).
    # `V_phase` stores the (0,0) entry of V_μ itself:
    #     V_μ = diag(V_phase, conj(V_phase))   with V_phase = e^{+i a (g'/2) B}
    # so V_μ† = diag(conj(V_phase), V_phase), and the diagonal entry that
    # multiplies the LEFT column of the SU(2) matrix is p0 = conj(V_phase).
    full_a, full_b = _su2_right_mult_by_diag(
        inner_a, inner_b, np.conj(V_phase)
    )

    DU_a = (full_a - U_st_a) / a_lat
    DU_b = (full_b - U_st_b) / a_lat
    return DU_a, DU_b


def covariant_stueckelberg_lagrangian(U_st_a, U_st_b, W_links, V_links,
                                      f=1.0, a_lat=1.0, link_dirs=None):
    """
    Lattice covariant Stueckelberg mass Lagrangian.

        L_st = f² · Σ_{x,μ} tr[(D_μ U_st)† D_μ U_st]

    For a 2×2 matrix M = [[A, -B*], [B, A*]] (the Cayley-Klein parameterisation
    used by D_μ U_st), tr(M† M) = 2(|A|² + |B|²).

    Parameters
    ----------
    U_st_a, U_st_b : (Lx, Ly, Lz) complex — Stueckelberg field.
    W_links : list of N_dir tuples (W_a, W_b) — SU(2)_L link variables for
              each link direction.
    V_links : list of N_dir complex arrays — U(1)_Y link phases (|V| = 1).
    f, a_lat : Stueckelberg decay constant and lattice spacing.
    link_dirs : optional (N_dir, 3) int array of link offsets.  Defaults to
                BCC_DIRS (the 8 BCC nearest neighbours).  Pass a different
                array for cubic / other lattices.

    Returns
    -------
    L_real : float — real Lagrangian value (sum over sites and link dirs).
    """
    if link_dirs is None:
        link_dirs = BCC_DIRS

    if len(W_links) != len(link_dirs) or len(V_links) != len(link_dirs):
        raise ValueError(
            f"W_links ({len(W_links)}) / V_links ({len(V_links)}) length "
            f"must match link_dirs ({len(link_dirs)})"
        )

    total = 0.0
    for ((W_a, W_b), V_phase, (dx, dy, dz)) in zip(W_links, V_links, link_dirs):
        DU_a, DU_b = covariant_stueckelberg_difference(
            U_st_a, U_st_b, W_a, W_b, V_phase, int(dx), int(dy), int(dz), a_lat
        )
        total += float(np.sum(2.0 * (np.abs(DU_a) ** 2 + np.abs(DU_b) ** 2)))
    return f * f * total


def covariant_stueckelberg_lagrangian_uniform(W123, B, g, gp, f=1.0,
                                              a_lat=1.0, L=4, link_dirs=None):
    """
    Convenience wrapper: evaluate covariant_stueckelberg_lagrangian with
    U_st = I uniform on an L³ cubic lattice and uniform gauge fields
    W123 = (W^1, W^2, W^3) and B.

    Used by W6.9 (model-tests/test_wmu_phase6_rank1.py) to extract the
    Hessian H_ij = ∂²L_st/∂ξ^i∂ξ^j at ξ = 0 in (W^1, W^2, W^3, B).

    Parameters
    ----------
    W123 : sequence of 3 floats — uniform (W^1, W^2, W^3) values.
    B    : float — uniform B value.
    g, gp, f, a_lat : SU(2)_L coupling, U(1)_Y coupling, Stueckelberg constant,
                      lattice spacing.
    L : int — cubic lattice edge length.
    link_dirs : optional link-direction set; defaults to BCC_DIRS (8 dirs).

    Returns
    -------
    L_real : float — total Lagrangian Σ_{x,μ} L_st-density.
    """
    if link_dirs is None:
        link_dirs = BCC_DIRS
    shape = (L, L, L)
    # U_st = I uniform
    U_st_a = np.ones(shape, dtype=complex)
    U_st_b = np.zeros(shape, dtype=complex)
    # Uniform links — same link variable for every BCC direction (constant
    # gauge field, every link sees the same parallel transport).
    W_a, W_b = make_su2_link_uniform(W123, g, a_lat, shape)
    V_phase = make_u1y_link_uniform(B, gp, a_lat, shape)
    W_links = [(W_a, W_b) for _ in range(len(link_dirs))]
    V_links = [V_phase for _ in range(len(link_dirs))]
    return covariant_stueckelberg_lagrangian(
        U_st_a, U_st_b, W_links, V_links, f=f, a_lat=a_lat, link_dirs=link_dirs
    )


# ═══════════════════════════════════════════════════════════════════
#  Phase 6 — Electroweak mixing (W³ ↔ B ↔ γ)
# ═══════════════════════════════════════════════════════════════════

def make_hypercharge_link_field(L, mode='identity', seed=17):
    """
    Initialise U(1)_Y hypercharge link variables.

    U(1) links stored as a single complex array U_Y with |U_Y| = 1.
    8 link directions, same BCC geometry as W_μ.

    Returns
    -------
    Y_links : list of 8 complex128 (Lx,Ly,Lz) arrays (phase factors).
    """
    if isinstance(L, int):
        shape = (L, L, L)
    else:
        shape = tuple(L)
    rng = np.random.default_rng(seed=seed)

    if mode == 'identity':
        return [np.ones(shape, dtype=complex) for _ in range(8)]
    elif mode == 'random':
        return [np.exp(1j * rng.uniform(0, 2 * np.pi, shape)) for _ in range(8)]
    else:
        raise ValueError(f"Unknown mode {mode!r}")


def hypercharge_propagation_step(E_B, B_B):
    """
    Free U(1)_Y propagation: apply F26 rotation law to (E_B, B_B).
    Same as the photon/W propagation.
    """
    shape = E_B.shape
    KX, KY, KZ = _kgrid3d(*shape)
    Ek = _fft.fftn(E_B)
    Bk = _fft.fftn(B_B)
    Ek_new, Bk_new = _f26_rotation_step(Ek, Bk, KX, KY, KZ)
    return _fft.ifftn(Ek_new).real, _fft.ifftn(Bk_new).real


def weinberg_mix(W3_E, W3_B, B_E, B_B, theta_W=np.pi / 6):
    """
    Diagonalise the W³–B system at Weinberg angle θ_W to produce
    the massless photon A and massive Z eigenstates.

        A = cos(θ_W)·B + sin(θ_W)·W³
        Z = −sin(θ_W)·B + cos(θ_W)·W³

    Parameters
    ----------
    W3_E, W3_B : (Lx,Ly,Lz) — W³ electric/magnetic fields
    B_E,  B_B  : (Lx,Ly,Lz) — B (hypercharge) electric/magnetic fields
    theta_W    : float — Weinberg angle (radians).
                 Default: θ_W = π/6 (sin²θ_W = 1/4), the bare lattice
                 value derived from the σ↔τ swap geometry (F45).
                 SM on-shell value: θ_W ≈ 0.4916 rad (sin²θ_W ≈ 0.231).

    Returns
    -------
    A_E, A_B : photon (massless eigenstate) fields.
    Z_E, Z_B : Z boson (massive eigenstate) fields.
    """
    cw = np.cos(theta_W)
    sw = np.sin(theta_W)
    A_E = cw * B_E + sw * W3_E
    A_B = cw * B_B + sw * W3_B
    Z_E = -sw * B_E + cw * W3_E
    Z_B = -sw * B_B + cw * W3_B
    return A_E, A_B, Z_E, Z_B


def weinberg_unmix(A_E, A_B, Z_E, Z_B, theta_W=np.pi / 6):
    """Inverse of weinberg_mix: recover (W³, B) from (A, Z).

    theta_W defaults to π/6 (sin²θ_W = 1/4, the F45 σ↔τ swap value),
    matching weinberg_mix; pass the same angle used in the forward mix.
    """
    cw = np.cos(theta_W)
    sw = np.sin(theta_W)
    B_E = cw * A_E - sw * Z_E
    B_B = cw * A_B - sw * Z_B
    W3_E = sw * A_E + cw * Z_E
    W3_B = sw * A_B + cw * Z_B
    return W3_E, W3_B, B_E, B_B


def ew_charge(T3, Y_over_2):
    """
    Electric charge formula: Q = T³ + Y/2.
    Returns the electric charge for a particle with weak isospin T³ and
    hypercharge Y/2.
    """
    return T3 + Y_over_2


# ═══════════════════════════════════════════════════════════════════
#  Phase 7 — Back-reaction and massive W dispersion (Proca)
#  2026-05-24
# ═══════════════════════════════════════════════════════════════════

def fermion_isospin_current(f_nu, f_e):
    """
    Left-handed SU(2)_L isospin current J^a(x) = ψ_L†(x) (τ^a/2) ψ_L(x).

    Uses only the upper Weyl (f) components; lower (g) are right-handed
    and do not couple to SU(2)_L (verified in W4.3 / F34).

        J^1(x) = Re(f_ν*(x) f_e(x))
        J^2(x) = Im(f_ν*(x) f_e(x))
        J^3(x) = (|f_ν(x)|² − |f_e(x)|²) / 2

    Parameters
    ----------
    f_nu, f_e : (Lx, Ly, Lz) complex — upper Weyl components of the
                left-handed SU(2) doublet (neutrino, electron).

    Returns
    -------
    J : (3, Lx, Ly, Lz) real — isospin charge density per lattice site.
        J[0] = J^1,  J[1] = J^2,  J[2] = J^3.
    """
    J1 = np.real(np.conj(f_nu) * f_e)
    J2 = np.imag(np.conj(f_nu) * f_e)
    J3 = 0.5 * (np.abs(f_nu)**2 - np.abs(f_e)**2)
    return np.stack([J1, J2, J3], axis=0)


def w_sourced_propagation_step(E_W, B_W, J_a, dt=1.0, g_lat=1.0):
    """
    One step of W propagation with fermion current back-reaction.

    Implements the linearized Yang–Mills equation with source:
        ∂_t E^a(k) = Ω(k) B^a(k) + g J^a(k)

    Split:
      1. Free F26 rotation (one tick)
      2. Source kick in real space: E^a += g · J^a · dt

    The source term is additive and diagonal in isospin: J^3 drives W^3
    only, J^1 drives W^1 only, etc.  This is the linearized (Abelian)
    coupling; the full non-Abelian back-reaction also includes the
    commutator [W, J] but that is O(g²) and handled in w_self_interaction_step.

    Parameters
    ----------
    E_W, B_W : (3, L, L, L) real — W isospin electric/magnetic fields.
    J_a      : (3, L, L, L) real — isospin current (fermion_isospin_current).
    dt       : float — time step (lattice ticks).
    g_lat    : float — lattice coupling constant.

    Returns
    -------
    E_W_new, B_W_new : updated W fields.
    """
    # Step 1: free F26 rotation (one tick)
    E_new, B_new = w_propagation_step_spectral(E_W, B_W)
    # Step 2: source kick E^a += g J^a dt  (real-space, diagonal in a)
    E_new = E_new + g_lat * J_a * dt
    return E_new, B_new


def _omega_even(KX, KY, KZ):
    """
    Even (Hermitian-symmetry-preserving) BCC dispersion for real W fields:
        Ω_even(k) = ω_+(k/2) + ω_-(k/2)

    This is the same quantity used by _f26_rotation_step.  Factored out
    here so that the massive step can reuse it without recomputation.
    """
    omega_p = bcc_dispersion(KX / 2.0, KY / 2.0, KZ / 2.0, sign='+')
    omega_m = bcc_dispersion(KX / 2.0, KY / 2.0, KZ / 2.0, sign='-')
    return omega_p + omega_m


def w_massive_propagation_step_spectral(E_W, B_W, m_W, dt=1.0):
    """
    One step of massive Proca W propagation.

    Replaces the free dispersion Ω_even(k) with the massive dispersion:
        ω_eff(k) = sqrt(m_W² + Ω_even²(k))

    The (E^a, B^a) pair at each k-mode rotates by angle ω_eff(k)·dt:
        E^a(k) → cos(ω_eff dt) E^a(k) + sin(ω_eff dt) B^a(k)
        B^a(k) → −sin(ω_eff dt) E^a(k) + cos(ω_eff dt) B^a(k)

    At m_W=0, dt=1: ω_eff = Ω_even, so this reduces exactly to
    w_propagation_step_spectral (W finding WB.5).

    Dispersion relation (Finding F36):
        ω²(k) = m_W² + Ω_even²(k)
    Continuum limit k→0:  Ω_even → 2c_lat|k|, so
        ω² → m_W² + 4 c_lat² |k|²   (Proca / Klein–Gordon dispersion).

    Parameters
    ----------
    E_W, B_W : (3, L, L, L) real — W isospin electric/magnetic fields.
    m_W      : float — W mass in lattice units (m_W ≥ 0).
    dt       : float — time step (lattice ticks, default 1).

    Returns
    -------
    E_W_new, B_W_new : updated W fields.
    """
    shape = E_W.shape[1:]
    KX, KY, KZ = _kgrid3d(*shape)
    Omega_even = _omega_even(KX, KY, KZ)
    omega_eff = np.sqrt(m_W**2 + Omega_even**2)
    cos_e = np.cos(omega_eff * dt)
    sin_e = np.sin(omega_eff * dt)

    E_new = np.zeros_like(E_W)
    B_new = np.zeros_like(B_W)
    for a in range(3):
        Ek = _fft.fftn(E_W[a])
        Bk = _fft.fftn(B_W[a])
        Ek_new = cos_e * Ek + sin_e * Bk
        Bk_new = -sin_e * Ek + cos_e * Bk
        E_new[a] = _fft.ifftn(Ek_new).real
        B_new[a] = _fft.ifftn(Bk_new).real
    return E_new, B_new


def measure_massive_w_dispersion(L=16, m_W=0.3, n_steps=50, a_comp=0, seed=42):
    """
    Verify the massive W dispersion ω²(k) = m_W² + Ω_even²(k).

    Initialises a random (E^a, B^a) field, evolves n_steps using
    w_massive_propagation_step_spectral, and compares the final Fourier
    amplitudes against the closed-form prediction:
        C_n(k) = C_0(k) · exp(−i · ω_eff(k) · n_steps)
    where C = E_k + i B_k.

    Uses direct complex-amplitude comparison (no np.angle call) to avoid
    phase-wrapping artefacts.

    Parameters
    ----------
    L        : int — lattice size.
    m_W      : float — W mass (lattice units).
    n_steps  : int — evolution steps.
    a_comp   : int — isospin component to test (0, 1, or 2).
    seed     : int — RNG seed.

    Returns
    -------
    max_rel_err : float — max |C_n − C_expected| / |C_0| over significant modes.
    """
    rng = np.random.default_rng(seed=seed)
    E_W = np.zeros((3, L, L, L))
    B_W = np.zeros((3, L, L, L))
    E_W[a_comp] = rng.standard_normal((L, L, L))
    B_W[a_comp] = rng.standard_normal((L, L, L))

    KX, KY, KZ = _kgrid3d(L, L, L)
    E0_k = _fft.fftn(E_W[a_comp])
    B0_k = _fft.fftn(B_W[a_comp])
    C0 = E0_k + 1j * B0_k

    for _ in range(n_steps):
        E_W, B_W = w_massive_propagation_step_spectral(E_W, B_W, m_W, dt=1.0)

    En_k = _fft.fftn(E_W[a_comp])
    Bn_k = _fft.fftn(B_W[a_comp])
    Cn = En_k + 1j * Bn_k

    Omega_even = _omega_even(KX, KY, KZ)
    omega_eff = np.sqrt(m_W**2 + Omega_even**2)
    C_expected = C0 * np.exp(-1j * omega_eff * n_steps)

    amp0 = np.abs(C0)
    sig = amp0 > 1e-8 * np.max(amp0)
    rel_err = np.where(sig, np.abs(Cn - C_expected) / (amp0 + 1e-30), 0.0)
    return float(np.max(rel_err))


def measure_photon_dispersion_from_mix(W3_E, W3_B, B_E, B_B, theta_W,
                                       n_steps=50):
    """
    Verify that the mixed A eigenstate obeys the F26 dispersion after
    Weinberg mixing — confirming A is massless.

    Returns max relative dispersion error.
    """
    A_E, A_B, _, _ = weinberg_mix(W3_E, W3_B, B_E, B_B, theta_W)
    shape = A_E.shape
    KX, KY, KZ = _kgrid3d(*shape)
    C0 = _fft.fftn(A_E) + 1j * _fft.fftn(A_B)

    for _ in range(n_steps):
        A_E, A_B = hypercharge_propagation_step(A_E, A_B)

    Cn = _fft.fftn(A_E) + 1j * _fft.fftn(A_B)
    phase = np.angle(Cn / np.where(np.abs(C0) > 1e-10, C0, 1.0))
    Omega_meas = np.abs(phase) / n_steps
    Omega_pred = 2.0 * bcc_dispersion(KX / 2.0, KY / 2.0, KZ / 2.0)
    sig = np.abs(C0) > 1e-8 * np.max(np.abs(C0))
    rel_err = np.where(sig,
                       np.abs(Omega_meas - Omega_pred) / (Omega_pred + 1e-30),
                       0.0)
    return float(np.max(rel_err))
