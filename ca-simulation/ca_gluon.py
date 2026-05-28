"""
ca_gluon.py — Dynamical SU(3) gauge sector  (FG-7, 2026-05-27)
===============================================================

Brings the colour sector up to the level the W received in `ca_wmu.py`
(findings F29, F33, F36).  Until now, SU(3) lived as link variables in
`ca_strong.py`; this module promotes it to a first-class dynamical
field:

  Phase A — Free gluon rotation law (F26 analog, per a-component)
  Phase B — Wilson plaquette  G^a_{μν}  and Yang-Mills self-coupling
  Phase C — Wilson-loop area-law diagnostic on frozen non-trivial links
  Phase D — Quark colour current J^{a,μ} sourcing the gluon (back-reaction)

Two lattices are supported throughout: 2D-square (matches `ca_strong.py`,
fast tests) and 3D BCC (matches `ca_wmu.py`, full QCA kinematics).

Conventions
-----------
  T^a = λ^a / 2  (Gell-Mann generators, Tr(T^a T^b) = ½ δ^{ab})
  f^{abc} — totally antisymmetric SU(3) structure constants:
            [T^a, T^b] = i f^{abc} T^c
  Non-zero f^{abc}:
    f^{123} = 1
    f^{147} = f^{246} = f^{257} = f^{345} = +1/2
    f^{156} = f^{367}                       = −1/2
    f^{458} = f^{678}                       = +√3/2

References
----------
  F29 — W-triplet bilinear bridges F26 to F27 (ca_wmu / SU(2))
  F33 — W_μ Phase 3: Yang-Mills self-coupling
  F36 — W_μ Phase 7: back-reaction + Proca dispersion
"""

import numpy as np

import ca_strong as cstr
import ca_bcc as cbcc
import ca_maxwell_2d as cm2
import ca_wmu as cwmu


# ══════════════════════════════════════════════════════════════════
#  SU(3) structure constants  f^{abc}
# ══════════════════════════════════════════════════════════════════

def _build_f_su3():
    """Totally antisymmetric SU(3) structure constants  [T^a,T^b]=if^{abc}T^c."""
    f = np.zeros((8, 8, 8), dtype=float)
    SQRT3_2 = np.sqrt(3.0) / 2.0

    def _set(a, b, c, v):
        # totally antisymmetric — 6 signed permutations
        for (i, j, k), s in (
            ((a, b, c), +1), ((b, c, a), +1), ((c, a, b), +1),
            ((b, a, c), -1), ((a, c, b), -1), ((c, b, a), -1),
        ):
            f[i, j, k] = s * v

    # Indices below are 1-based per the standard SU(3) convention;
    # we store as 0-based.
    _set(0, 1, 2, 1.0)            # f^{123}=1
    _set(0, 3, 6, 0.5)            # f^{147}=1/2
    _set(0, 4, 5, -0.5)           # f^{156}=-1/2  (i.e. f^{156})
    _set(1, 3, 5, 0.5)            # f^{246}=1/2
    _set(1, 4, 6, 0.5)            # f^{257}=1/2
    _set(2, 3, 4, 0.5)            # f^{345}=1/2
    _set(2, 5, 6, -0.5)           # f^{367}=-1/2
    _set(3, 4, 7, SQRT3_2)        # f^{458}=√3/2
    _set(5, 6, 7, SQRT3_2)        # f^{678}=√3/2
    return f


_F_SU3 = _build_f_su3()


def structure_constants_jacobi_residual():
    """
    Jacobi identity for the structure constants:
        f^{abe} f^{cde} + f^{cbe} f^{ade} + f^{dbe} f^{ace} = 0

    Equivalent (and the form we test): [[T^a,T^b],T^c] + cyclic = 0
    translates to  f^{abe} f^{ecd} + cyclic(a,b,c) = 0.

    Returns max |residual| over a,b,c,d ∈ {0..7}.
    """
    max_res = 0.0
    for a in range(8):
        for b in range(8):
            for c in range(8):
                for d in range(8):
                    s = 0.0
                    for e in range(8):
                        s += (_F_SU3[a, b, e] * _F_SU3[e, c, d]
                              + _F_SU3[b, c, e] * _F_SU3[e, a, d]
                              + _F_SU3[c, a, e] * _F_SU3[e, b, d])
                    if abs(s) > max_res:
                        max_res = abs(s)
    return float(max_res)


# ══════════════════════════════════════════════════════════════════
#  Phase A — Free gluon rotation law  (F26 analog, per a-component)
# ══════════════════════════════════════════════════════════════════

# 2D --------------------------------------------------------------

def _rotation_step_em_scalar_2d(E, B):
    """
    F26 2D rotation law on scalar-per-site fields (no Lorentz axis).

    E, B : (Lx, Ly) real.  Returns the spectrally-rotated pair after
    one tick at Δt = 1.
    """
    Lx, Ly = E.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    Omega = cm2.rotation_omega_2d(KX, KY)
    cosO = np.cos(Omega)
    sinO = np.sin(Omega)
    Ek = np.fft.fft2(E)
    Bk = np.fft.fft2(B)
    E_new = np.fft.ifft2(cosO * Ek + sinO * Bk).real
    B_new = np.fft.ifft2(-sinO * Ek + cosO * Bk).real
    return E_new, B_new


def gluon_rotation_step_spectral_2d(E_G, B_G):
    """
    One tick of free gluon propagation on 2D-square lattice.

    E_G, B_G : (8, Lx, Ly) real — colour-octet electric/magnetic fields,
        a ∈ {0..7} (octet), scalar per lattice site.
    Applies the F26 2D rotation law independently to each a-component:
        (E^a, B^a) ← R(Ω_2D(k)) · (E^a, B^a),  Ω_2D = 2·ω_2D(k/2)

    Cold structure: no a-coupling at the free-field level — the rotation
    is the same for every a, exactly as in F29 / F33 for SU(2).
    """
    if E_G.shape[0] != 8 or B_G.shape[0] != 8:
        raise ValueError("E_G, B_G must have first axis size 8 (SU(3) octet)")
    E_new = np.zeros_like(E_G)
    B_new = np.zeros_like(B_G)
    for a in range(8):
        E_new[a], B_new[a] = _rotation_step_em_scalar_2d(E_G[a], B_G[a])
    return E_new, B_new


# BCC -------------------------------------------------------------

def gluon_rotation_step_spectral_bcc(E_G, B_G):
    """
    One tick of free gluon propagation on the BCC lattice.

    E_G, B_G : (8, L, L, L) real — colour-octet (E^a, B^a) fields.
    Uses `ca_wmu.w_propagation_step_spectral` (the F37 chirally-faithful
    branch step) per a-component.  Each a is decoupled at the free-field
    level; SU(3) acts adjointly on the 'a' label only, which the rotation
    does not see.
    """
    if E_G.shape[0] != 8 or B_G.shape[0] != 8:
        raise ValueError("E_G, B_G must have first axis size 8 (SU(3) octet)")
    # Reuse the W's per-tick chiral step.  It expects shape (3,L,L,L), so
    # we loop over a-components in pairs of 3 (and handle the leftover 2).
    E_new = np.zeros_like(E_G)
    B_new = np.zeros_like(B_G)
    # Process in chunks of 3 to reuse the (3,L,L,L) interface verbatim.
    for start in range(0, 8, 3):
        end = min(start + 3, 8)
        size = end - start
        if size == 3:
            En, Bn = cwmu.w_propagation_step_spectral(E_G[start:end], B_G[start:end])
        else:
            # Pad to 3, propagate, slice back
            shp = E_G.shape[1:]
            E_pad = np.zeros((3,) + shp)
            B_pad = np.zeros((3,) + shp)
            E_pad[:size] = E_G[start:end]
            B_pad[:size] = B_G[start:end]
            En, Bn = cwmu.w_propagation_step_spectral(E_pad, B_pad)
            En = En[:size]
            Bn = Bn[:size]
        E_new[start:end] = En
        B_new[start:end] = Bn
    return E_new, B_new


def gluon_massive_step_spectral_bcc(E_G, B_G, m_g=0.0, dt=1.0):
    """
    Proca-style massive gluon propagation.  m_g=0 default reduces exactly
    to `gluon_rotation_step_spectral_bcc` (the F36 WB.5 invariant — the
    massless limit is bit-for-bit the free step).

    Physically QCD gluons are massless; this is provided so the source
    step (Phase D) and any future colour-confinement-effective-mass
    constructions can share the same primitive.
    """
    if m_g == 0.0:
        return gluon_rotation_step_spectral_bcc(E_G, B_G)
    E_new = np.zeros_like(E_G)
    B_new = np.zeros_like(B_G)
    for start in range(0, 8, 3):
        end = min(start + 3, 8)
        size = end - start
        if size == 3:
            En, Bn = cwmu.w_massive_propagation_step_spectral(
                E_G[start:end], B_G[start:end], m_g, dt=dt)
        else:
            shp = E_G.shape[1:]
            E_pad = np.zeros((3,) + shp)
            B_pad = np.zeros((3,) + shp)
            E_pad[:size] = E_G[start:end]
            B_pad[:size] = B_G[start:end]
            En, Bn = cwmu.w_massive_propagation_step_spectral(
                E_pad, B_pad, m_g, dt=dt)
            En = En[:size]
            Bn = Bn[:size]
        E_new[start:end] = En
        B_new[start:end] = Bn
    return E_new, B_new


# ══════════════════════════════════════════════════════════════════
#  Colour-octet bilinear  G^{a,i}  (analog of F29 W-triplet)
# ══════════════════════════════════════════════════════════════════
#
# G^{a,i}(x) = Σ_{f,d,c,c'} (T^a)_{cc'} (q^{f,c,d})*(x) σ^i_{d d'} q^{f,c',d'}(x)
#
# Hermitian variant (F29 finding: transpose form fails SU because V^T V ≠ I
# for SU(3) too — Hermitian only).  Sum is over flavour, summed over both
# chiralities (η + χ).  σ^i runs over the three spatial Pauli matrices on
# the (↑,↓) sub-block of each chirality.

_PAULIS = (
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
)


def quark_colour_octet_bilinear_2d(q):
    """
    Build the colour-octet Pauli-vector bilinear from a 2D quark field.

    Parameters
    ----------
    q : quark dict from `ca_strong.zero_quark_field` (Lx, Ly) per channel.

    Returns
    -------
    G : (8, Lx, Ly, 3) complex — G[a, x, y, i] = octet a, Pauli i ∈ {x,y,z}.

    Property (F29 B2 analog): under  q → V q  with constant V ∈ SU(3),
                                G^a → R_adj^{ab}(V) G^b ,
    with R_adj from `ca_strong.adjoint_rotation`.
    """
    sample = next(iter(q.values()))
    Lx, Ly = sample.shape
    G = np.zeros((8, Lx, Ly, 3), dtype=complex)
    for f in cstr.FLAVOURS:
        # Colour triplets of the 4 Dirac components
        eu = cstr._colour_triplet(q, f, 'eu')   # (Lx,Ly,3) — η_↑
        ed = cstr._colour_triplet(q, f, 'ed')   # (Lx,Ly,3) — η_↓
        cu = cstr._colour_triplet(q, f, 'cu')   # (Lx,Ly,3) — χ_↑
        cd = cstr._colour_triplet(q, f, 'cd')   # (Lx,Ly,3) — χ_↓
        for a in range(8):
            Ta = cstr.T_GEN[a]
            # T^a acts on the colour index of the spinor-up / spinor-down pair.
            # The Pauli σ^i acts on (↑,↓).
            # σ^1 = [[0,1],[1,0]]:  (↑→↓, ↓→↑)
            #   G^{a,1} = Σ ψ†_↑ T^a ψ_↓ + ψ†_↓ T^a ψ_↑
            # σ^2 = [[0,-i],[i,0]]: G^{a,2} = i(ψ†_↓ T^a ψ_↑ − ψ†_↑ T^a ψ_↓)
            # σ^3 = [[1,0],[0,-1]]: G^{a,3} = ψ†_↑ T^a ψ_↑ − ψ†_↓ T^a ψ_↓
            for chir_up, chir_dn in ((eu, ed), (cu, cd)):
                Ta_up = np.einsum('ij,xyj->xyi', Ta, chir_up)
                Ta_dn = np.einsum('ij,xyj->xyi', Ta, chir_dn)
                term_du = np.sum(np.conj(chir_dn) * Ta_up, axis=-1)
                term_ud = np.sum(np.conj(chir_up) * Ta_dn, axis=-1)
                diag_up = np.sum(np.conj(chir_up) * Ta_up, axis=-1)
                diag_dn = np.sum(np.conj(chir_dn) * Ta_dn, axis=-1)
                G[a, ..., 0] += term_ud + term_du            # σ^x
                G[a, ..., 1] += 1j * (term_du - term_ud)     # σ^y
                G[a, ..., 2] += diag_up - diag_dn            # σ^z
    return G


def quark_colour_octet_bilinear_bcc(q):
    """
    BCC analog of `quark_colour_octet_bilinear_2d`.

    Parameters
    ----------
    q : dict with keys (f, c, d) → (L, L, L) complex.

    Returns
    -------
    G : (8, L, L, L, 3) complex.
    """
    sample = next(iter(q.values()))
    L = sample.shape
    G = np.zeros((8,) + L + (3,), dtype=complex)
    # Build colour triplet by stacking (r,g,b)
    def _trip(q, f, d):
        return np.stack([q[(f, c, d)] for c in cstr.COLOURS], axis=-1)
    for f in cstr.FLAVOURS:
        eu = _trip(q, f, 'eu')
        ed = _trip(q, f, 'ed')
        cu = _trip(q, f, 'cu')
        cd = _trip(q, f, 'cd')
        for a in range(8):
            Ta = cstr.T_GEN[a]
            for chir_up, chir_dn in ((eu, ed), (cu, cd)):
                Ta_up = np.einsum('ij,xyzj->xyzi', Ta, chir_up)
                Ta_dn = np.einsum('ij,xyzj->xyzi', Ta, chir_dn)
                term_du = np.sum(np.conj(chir_dn) * Ta_up, axis=-1)
                term_ud = np.sum(np.conj(chir_up) * Ta_dn, axis=-1)
                diag_up = np.sum(np.conj(chir_up) * Ta_up, axis=-1)
                diag_dn = np.sum(np.conj(chir_dn) * Ta_dn, axis=-1)
                G[a, ..., 0] += term_ud + term_du
                G[a, ..., 1] += 1j * (term_du - term_ud)
                G[a, ..., 2] += diag_up - diag_dn
    return G


def octet_norm_sq(G):
    """Σ_{a,x,i} |G^{a,i}(x)|²  — the SU(3) Casimir of the bilinear field."""
    return float(np.sum(np.abs(G) ** 2))


def octet_adjoint_rotate(G, V):
    """
    Apply G^a → R_adj^{ab}(V) G^b for a constant V ∈ SU(3).

    The adjoint matrix is the same one returned by `ca_strong.adjoint_rotation`.
    """
    R = cstr.adjoint_rotation(V)
    # G has shape (8, ...).  Contract on the leading 'a' axis.
    return np.einsum('ab,b...->a...', R, G)


# ══════════════════════════════════════════════════════════════════
#  Phase B — SU(3) Wilson plaquette  G^a_{μν}  and Yang-Mills update
# ══════════════════════════════════════════════════════════════════

def plaquette_matrix_su3_2d(U, mu=0, nu=1):
    """
    Full Wilson-plaquette matrix  U_□_{μν}(x)  on the 2D square lattice.

    Returns (Lx, Ly, 3, 3) complex.
    """
    Umu = U[mu]
    Unu_shift = np.roll(U[nu], -1, axis=mu)
    Umu_shift_nu = np.roll(U[mu], -1, axis=nu)
    Unu = U[nu]
    Umu_shift_nu_dag = np.conj(np.transpose(Umu_shift_nu, (0, 1, 3, 2)))
    Unu_dag = np.conj(np.transpose(Unu, (0, 1, 3, 2)))
    return np.einsum('xyij,xyjk,xykl,xylm->xyim',
                     Umu, Unu_shift, Umu_shift_nu_dag, Unu_dag)


def plaquette_field_strength_su3_2d(U, g_lat=1.0, a_lat=1.0):
    """
    SU(3) field strength G^a_{xy}(x) extracted from the Wilson plaquette
    on the 2D square lattice.

    Definition (F33 SU(3) analog):
        G^a_{μν}(x) = -i/(g · a²) · Tr[ T^a · (U_□ − U_□†) ]

    Equivalently — using Tr(T^a T^b) = ½δ^{ab} —
        G^a_{μν}(x) =  2 · Im( Tr[ T^a · U_□ ] ) / (g · a²) .

    For U_□ = I, U_□ − U_□† = 0, so G^a = 0 exactly (bit-for-bit).

    Returns (8, Lx, Ly) real.
    """
    Uplaq = plaquette_matrix_su3_2d(U, mu=0, nu=1)
    G = np.zeros((8,) + Uplaq.shape[:2], dtype=float)
    norm = g_lat * a_lat ** 2
    for a in range(8):
        # Tr(T^a · U_□)  per site
        Ta = cstr.T_GEN[a]
        tr = np.einsum('ij,xyji->xy', Ta, Uplaq)
        G[a] = 2.0 * np.imag(tr) / norm
    return G


def yang_mills_norm_sq_2d(G_field):
    """Σ_{a,x} |G^a(x)|²  — Lorentz-scalar field-strength magnitude."""
    return float(np.sum(G_field ** 2))


def gluon_self_coupling_step_2d(U, dt=0.05, g_lat=1.0):
    """
    Single Yang-Mills self-coupling tick on the 2D-square SU(3) link field,
    using the structure constants f^{abc}.

    Algorithm (mirrors F33 `w_self_interaction_step`):
        G^a   = plaquette_field_strength_su3_2d(U)
        W^a   = link-averaged colour-vector field (small-amplitude readout)
        δW^a  = dt · g · f^{abc} · W^b · G^c
        U_ℓ   ← exp(i · δW^a · T^a) · U_ℓ                    (SU(3) update)

    Preserves SU(3) link unitarity to floating-point round-off (Phase B
    test PB.4).
    """
    G = plaquette_field_strength_su3_2d(U, g_lat=g_lat)   # (8, Lx, Ly)

    # Small-amplitude readout  W^a = 2·Im(Tr(T^a · U_link)) averaged over μ.
    n_dir, Lx, Ly = U.shape[:3]
    W = np.zeros((8, Lx, Ly), dtype=float)
    for mu in range(n_dir):
        for a in range(8):
            tr = np.einsum('ij,xyji->xy', cstr.T_GEN[a], U[mu])
            W[a] += 2.0 * np.imag(tr)
    W /= n_dir

    # δW^a = g·dt · f^{abc} W^b G^c    (summed over b,c)
    deltaW = g_lat * dt * np.einsum('abc,b...,c...->a...', _F_SU3, W, G)

    # Build R(x) = exp(i · δW^a · T^a) per site
    R = _su3_expmap_field(deltaW)

    # Apply R · U_ℓ  for every direction
    U_new = np.empty_like(U)
    for mu in range(n_dir):
        U_new[mu] = np.einsum('xyij,xyjk->xyik', R, U[mu])
    return U_new


def _su3_expmap_field(theta_field):
    """
    Build  V(x) = exp(i · Σ_a θ^a(x) · T^a)  for a (8, Lx, Ly) or
    (8, Lx, Ly, Lz) real field θ.  Returns (Lx, Ly[, Lz], 3, 3) complex.

    Uses Hermitian eigendecomposition per site.  Cold (θ=0) → V = I bit-for-bit.
    """
    shape = theta_field.shape[1:]
    V = np.zeros(shape + (3, 3), dtype=complex)
    flat_theta = theta_field.reshape(8, -1)
    flat_V = V.reshape(-1, 3, 3)
    # Vectorised Hermitian build:  H = Σ_a θ^a · T^a
    for n in range(flat_theta.shape[1]):
        H = sum(flat_theta[a, n] * cstr.T_GEN[a] for a in range(8))
        if not np.any(flat_theta[:, n]):
            flat_V[n] = np.eye(3, dtype=complex)
            continue
        w, U = np.linalg.eigh(H)
        flat_V[n] = U @ np.diag(np.exp(1j * w)) @ U.conj().T
    return flat_V.reshape(shape + (3, 3))


# BCC plaquette ----------------------------------------------------

def _bcc_eff_links_su3(U_bcc):
    """
    Build six straight-line +x, +y, +z SU(3) effective links from BCC pairs.

    U_bcc : list of 8 arrays of shape (L, L, L, 3, 3), one per BCC direction
            (ordered as `ca_wmu.BCC_DIRS`).
    Returns (Ux, Uy, Uz) each (L, L, L, 3, 3) corresponding to a 2-unit hop.
    """
    BCC = cwmu.BCC_DIRS.tolist()
    idx = {tuple(d): i for i, d in enumerate(BCC)}

    def _eff(d1, d2):
        i1, i2 = idx[d1], idx[d2]
        U1 = U_bcc[i1]
        U2 = U_bcc[i2]
        dx, dy, dz = d1
        U2s = np.roll(np.roll(np.roll(U2, -dx, 0), -dy, 1), -dz, 2)
        return np.einsum('xyzij,xyzjk->xyzik', U1, U2s)

    Ux = _eff((1, 1, 1), (1, -1, -1))
    Uy = _eff((1, 1, 1), (-1, 1, -1))
    Uz = _eff((1, 1, 1), (-1, -1, 1))
    return Ux, Uy, Uz


def plaquette_field_strength_su3_bcc(U_bcc, g_lat=1.0):
    """
    SU(3) field strength G^a_{μν}(x) on the BCC lattice, three planes.

    U_bcc : list of 8 (L,L,L,3,3) arrays — colour-link field on the BCC
            8-neighbour graph (mirrors ca_wmu link layout).
    Returns: dict('xy','xz','yz') → (8, L, L, L) real.

    Identity links → all G zero (bit-for-bit).
    """
    Ux, Uy, Uz = _bcc_eff_links_su3(U_bcc)

    def _shift(arr, dx, dy, dz):
        return np.roll(np.roll(np.roll(arr, -dx, 0), -dy, 1), -dz, 2)

    def _dag(A):
        return np.conj(np.transpose(A, (0, 1, 2, 4, 3)))

    def _plaq(A, B, shiftA, shiftB):
        # P = A(x) B(x+shiftA) A†(x+shiftB) B†(x)
        B_sA = _shift(B, *shiftA)
        A_sB_dag = _dag(_shift(A, *shiftB))
        B_dag = _dag(B)
        step1 = np.einsum('xyzij,xyzjk->xyzik', A, B_sA)
        step2 = np.einsum('xyzij,xyzjk->xyzik', step1, A_sB_dag)
        return np.einsum('xyzij,xyzjk->xyzik', step2, B_dag)

    P_xy = _plaq(Ux, Uy, (2, 0, 0), (0, 2, 0))
    P_xz = _plaq(Ux, Uz, (2, 0, 0), (0, 0, 2))
    P_yz = _plaq(Uy, Uz, (0, 2, 0), (0, 0, 2))

    a2 = 4.0     # 2-unit composite plaquette area

    def _extract(P):
        G = np.zeros((8,) + P.shape[:3], dtype=float)
        for a in range(8):
            tr = np.einsum('ij,xyzji->xyz', cstr.T_GEN[a], P)
            G[a] = 2.0 * np.imag(tr) / (g_lat * a2)
        return G

    return {'xy': _extract(P_xy), 'xz': _extract(P_xz), 'yz': _extract(P_yz)}


def gluon_self_coupling_step_bcc(U_bcc, dt=0.05, g_lat=1.0):
    """
    Yang-Mills self-coupling tick on the BCC SU(3) link field.

    Direct port of `ca_wmu.w_self_interaction_step` with τ^a → T^a,
    ε^{abc} → f^{abc}.  Returns updated link list; SU(3) unitarity is
    preserved to round-off.
    """
    G = plaquette_field_strength_su3_bcc(U_bcc, g_lat=g_lat)
    G_avg = (G['xy'] + G['xz'] + G['yz']) / 3.0    # (8, L, L, L)

    # Small-amplitude readout per direction, then average
    n_dir = len(U_bcc)
    L = U_bcc[0].shape[:3]
    W = np.zeros((8,) + L, dtype=float)
    for d in range(n_dir):
        for a in range(8):
            tr = np.einsum('ij,xyzji->xyz', cstr.T_GEN[a], U_bcc[d])
            W[a] += 2.0 * np.imag(tr)
    W /= n_dir

    # δW^a = g·dt · f^{abc} W^b G^c
    deltaW = g_lat * dt * np.einsum('abc,b...,c...->a...', _F_SU3, W, G_avg)
    R = _su3_expmap_field(deltaW)        # (L, L, L, 3, 3)

    U_new = []
    for d in range(n_dir):
        U_new.append(np.einsum('xyzij,xyzjk->xyzik', R, U_bcc[d]))
    return U_new


def link_unitarity_residual_su3(U):
    """
    max_{μ,x} || U U† − I ||_∞   for a 2D or BCC SU(3) link field.

    Works on:
      • 2D shape (n_dir, Lx, Ly, 3, 3)
      • BCC list of n_dir arrays of shape (L, L, L, 3, 3)
    """
    if isinstance(U, list):
        worst = 0.0
        for Ud in U:
            UUd = np.einsum('...ij,...kj->...ik', Ud, np.conj(Ud))
            res = float(np.max(np.abs(UUd - np.eye(3))))
            worst = max(worst, res)
        return worst
    UUd = np.einsum('...ij,...kj->...ik', U, np.conj(U))
    return float(np.max(np.abs(UUd - np.eye(3))))


# ══════════════════════════════════════════════════════════════════
#  Phase C — Wilson-loop area-law diagnostic  (frozen non-trivial links)
# ══════════════════════════════════════════════════════════════════

def wilson_loop_2d_rect(U, r, t, x0=0, y0=0):
    """
    Re Tr ⟨W(r × t)⟩  for a single rectangular Wilson loop on 2D-square SU(3).

    Loop is the ordered product of links going +x for r steps, +y for t steps,
    −x for r steps, −y for t steps, starting at (x0, y0).  Returns a real
    scalar Re Tr W (no spatial average — the caller chooses the corner).
    """
    Lx, Ly = U.shape[1:3]
    Ux = U[0]      # +x links
    Uy = U[1]      # +y links

    W = np.eye(3, dtype=complex)
    # +x edge
    x, y = x0 % Lx, y0 % Ly
    for _ in range(r):
        W = W @ Ux[x, y]
        x = (x + 1) % Lx
    # +y edge
    for _ in range(t):
        W = W @ Uy[x, y]
        y = (y + 1) % Ly
    # −x edge (use inverse: U_{-x}(x) = U_x†(x − x̂))
    for _ in range(r):
        x = (x - 1) % Lx
        W = W @ np.conj(Ux[x, y].T)
    # −y edge
    for _ in range(t):
        y = (y - 1) % Ly
        W = W @ np.conj(Uy[x, y].T)
    return float(np.real(np.trace(W)))


def wilson_loop_2d_avg(U, r, t):
    """Spatial average of Re Tr W(r,t) over all (x0, y0) corners."""
    Lx, Ly = U.shape[1:3]
    total = 0.0
    for x0 in range(Lx):
        for y0 in range(Ly):
            total += wilson_loop_2d_rect(U, r, t, x0, y0)
    return total / (Lx * Ly)


def wilson_loop_gauge_residual_2d(U, V_field, r, t):
    """
    Verify  ⟨Re Tr W(r,t)⟩  is invariant under a *local* SU(3) gauge
    transformation U → V U V†.  Returns |W_before − W_after|.

    For a closed Wilson loop W and any V(x), V cancels at the start/end
    corner exactly — so the trace is invariant by construction.  This
    residual tests the implementation, not the math; expect machine ε.
    """
    W_before = wilson_loop_2d_avg(U, r, t)
    U_rot = cstr.gauge_transform_links(U, V_field)
    W_after = wilson_loop_2d_avg(U_rot, r, t)
    return float(abs(W_before - W_after))


def wilson_loop_area_law_data(U, r_max=4, t_max=4):
    """
    Compute  ⟨Re Tr W(r,t)⟩  for r ∈ 1..r_max, t ∈ 1..t_max.

    Returns dict[(r, t)] → mean loop trace.  Caller compares to area-law
    expectation:  ⟨W⟩ ≈ N_c · exp(−σ · r · t)  for confining links.
    For cold (U=I) links, ⟨W⟩ = N_c = 3 exactly for every (r, t).
    """
    out = {}
    for r in range(1, r_max + 1):
        for t in range(1, t_max + 1):
            out[(r, t)] = wilson_loop_2d_avg(U, r, t)
    return out


# ══════════════════════════════════════════════════════════════════
#  Phase D — Quark colour current → gluon back-reaction
# ══════════════════════════════════════════════════════════════════

def quark_colour_current_2d(q):
    """
    Build J^{a, μ}(x) — colour-current density on the 2D-square lattice.

    Time component  J^{a,0}  via  `ca_strong.noether_charge_density`.
    Spatial         J^{a,i}  via  `ca_strong.noether_current_spatial`.

    Returns
    -------
    J0 : (8, Lx, Ly) real
    Js : (2, 8, Lx, Ly) real  (spatial components, axis 0 = μ ∈ {x,y})
    """
    J0 = cstr.noether_charge_density(q)         # (8, Lx, Ly)
    Js = cstr.noether_current_spatial(q)        # (2, 8, Lx, Ly)
    return J0, Js


def gluon_sourced_step_2d(E_G, B_G, J_a, dt=1.0, g_lat=1.0):
    """
    Linearised Yang-Mills with quark source on the 2D-square lattice:

        ∂_t E^a(k) = Ω(k) B^a(k) + g · J^a(k)

    Split:
      (1) free rotation (one tick of `gluon_rotation_step_spectral_2d`)
      (2) source kick   E^a += g · J^a · dt   (real-space, diagonal in a)

    E_G, B_G : (8, Lx, Ly) real.
    J_a      : (8, Lx, Ly) real.

    Diagonal in colour: an a=3-only source drives only the a=3 octet
    component at linear order (same property as the W in F36 WB.3).
    """
    E_new, B_new = gluon_rotation_step_spectral_2d(E_G, B_G)
    E_new = E_new + g_lat * J_a * dt
    return E_new, B_new


def gluon_sourced_step_bcc(E_G, B_G, J_a, dt=1.0, g_lat=1.0):
    """
    BCC analog of `gluon_sourced_step_2d`.

    E_G, B_G, J_a : (8, L, L, L) real.
    """
    E_new, B_new = gluon_rotation_step_spectral_bcc(E_G, B_G)
    E_new = E_new + g_lat * J_a * dt
    return E_new, B_new


def free_gluon_dispersion_residual_bcc(L=12, n_steps=50, a_comp=0, seed=11):
    """
    Verify free-gluon dispersion ω(k) = Ω⁺(k) = 2·ω_+(k/2) per a-component
    on the BCC lattice.  Direct port of `ca_wmu.w_free_dispersion_check`
    to the 8-component octet.

    Returns max relative error over significant Fourier modes.
    """
    rng = np.random.default_rng(seed=seed)
    E = np.zeros((8, L, L, L))
    B = np.zeros((8, L, L, L))
    E[a_comp] = rng.standard_normal((L, L, L))
    B[a_comp] = rng.standard_normal((L, L, L))

    KX, KY, KZ = cwmu._kgrid3d(L, L, L)
    Omega_pred, _ = cwmu._chiral_dispersions((L, L, L))

    E0 = np.fft.fftn(E[a_comp])
    B0 = np.fft.fftn(B[a_comp])
    C0 = E0 + 1j * B0

    for _ in range(n_steps):
        E, B = gluon_rotation_step_spectral_bcc(E, B)

    En = np.fft.fftn(E[a_comp])
    Bn = np.fft.fftn(B[a_comp])
    Cn = En + 1j * Bn
    C_expected = C0 * np.exp(-1j * Omega_pred * n_steps)

    amp0 = np.abs(C0)
    sig = amp0 > 1e-8 * np.max(amp0)
    rel = np.where(sig, np.abs(Cn - C_expected) / (amp0 + 1e-30), 0.0)
    return float(np.max(rel))


# ══════════════════════════════════════════════════════════════════
#  Helper — BCC link field initialisation
# ══════════════════════════════════════════════════════════════════

def make_su3_link_field_bcc(L, mode='identity', seed=7):
    """
    Initialise an SU(3) link field on the BCC 8-neighbour graph.

    mode='identity'  : every link = I (cold start)
    mode='random'    : Haar-random SU(3) per link
    mode='near_id'   : exp(i · ε · θ^a · T^a) with small θ — useful for
                       linearised Bianchi / dispersion tests
    """
    n_dir = len(cwmu.BCC_DIRS)
    if mode == 'identity':
        I = np.zeros((L, L, L, 3, 3), dtype=complex)
        I[..., 0, 0] = 1.0
        I[..., 1, 1] = 1.0
        I[..., 2, 2] = 1.0
        return [I.copy() for _ in range(n_dir)]
    rng = np.random.default_rng(seed=seed)
    out = []
    if mode == 'random':
        for _ in range(n_dir):
            Ud = np.zeros((L, L, L, 3, 3), dtype=complex)
            for i in range(L):
                for j in range(L):
                    for k in range(L):
                        Ud[i, j, k] = cstr.su3_haar(rng)
            out.append(Ud)
        return out
    if mode == 'near_id':
        eps = 0.05
        for _ in range(n_dir):
            theta = eps * rng.standard_normal((8, L, L, L))
            Ud = _su3_expmap_field(theta)
            out.append(Ud)
        return out
    raise ValueError(f"unknown mode {mode!r}")
