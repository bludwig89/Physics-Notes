"""ca_minimal_coupling — U(1) and SU(3) minimal coupling on the 3D BCC walk.

2026-06-05 - 19:10

Promotes the particle layer's EM and strong couplings from source-only to
two-way (roadmap-particle-layer.md Phase P2) using the two architectures
already audited elsewhere in the model — nothing new is invented here, the
constructions are ported to 3D BCC and verified:

1. **U(1) Stueckelberg-form wrap** (the F41/F42 ``kinetic_half_step_chi_u1y``
   architecture, exact gauge covariance):

       ψ̃(x)  = e^{-i q α(x)} ψ(x)        [gauge-fix to invariant frame]
       ψ̃'    = weyl_step_3d_bcc(ψ̃)      [exact unitary QCA kinetic step]
       ψ'(x) = e^{+i q α(x)} ψ̃'(x)       [restore physical frame]

   Properties (verified in tests/test_particle_layer.py P2 suite):
   * α ≡ 0           → bit-for-bit equal to the free step.
   * exact covariance: S[α+β](e^{iqβ}ψ) = e^{iqβ} S[α](ψ) for any β(x),
     machine precision — the F27 "static gauge angle is unobservable"
     statement, now for the 3D BCC kinetic step.
   * exactly unitary (phases × unitary spectral step).
   * dynamics: a *time-dependent* α(x,t) = Σ φ(x) dt (the A₀ Wilson line of
     a scalar potential φ) inserts the relative phase e^{-iqφdt} between
     consecutive kinetic steps — the electrostatic force.  A static α is
     pure gauge and force-free, exactly as F27 requires.

2. **SU(3) site-local rotate-then-step** (the audited SU(2) architecture of
   ``ca_wmu.covariant_weyl_step_3d_bcc`` / ``_u_eff_from_links``):

       q̃(x) = V(x) q(x),  V(x) = exp(i ε A^a(x) T^a)   [ca_gluon expmap]
       q'_c  = weyl_step_3d_bcc(q̃_c)  per colour c

   * A ≡ 0 → bit-for-bit free.  Exactly norm-conserving.
   * global SU(3) Ward identity exact (constant V commutes with the
     colour-blind kinetic step) — same status as the audited W coupling;
     local Ward is O(a), as for all improved lattice fermion actions.
"""
from __future__ import annotations

import numpy as np

from casim.engine.lattice.bcc import weyl_step_3d_bcc


# ----------------------------------------------------------------------
# 1. U(1) wrap step (EM / hypercharge minimal coupling, exact covariance)
# ----------------------------------------------------------------------
def u1_wrap_weyl_step_3d_bcc(f, g, alpha, q, sign='+'):
    """U(1)-covariant BCC Weyl step via the Stueckelberg-form wrap.

    Parameters
    ----------
    f, g   : (L,L,L) complex — Weyl spinor (spin ↑, ↓).
    alpha  : (L,L,L) real — U(1) gauge angle field α(x) (e.g. accumulated
             A₀ Wilson line from a Coulomb potential).
    q      : float — the particle's U(1) charge (exact Fraction upstream).
    sign   : BCC chirality branch.
    """
    if q == 0:
        return weyl_step_3d_bcc(f, g, sign=sign)
    ph_in = np.exp(-1j * q * alpha)
    ph_out = np.conj(ph_in)
    f_n, g_n = weyl_step_3d_bcc(ph_in * f, ph_in * g, sign=sign)
    return ph_out * f_n, ph_out * g_n


def u1_wrap_dirac_step_3d_bcc(eta_u, eta_d, chi_u, chi_d,
                              alpha, q, m=0.0, dt=1.0, sign='+'):
    """U(1) wrap around the exact 3D BCC Dirac split-step (massive particle).

    The vector U(1) charge q phases both chiralities identically, so the wrap
    commutes with the F27 mass mixing and the covariance identity holds for
    the full massive step.
    """
    from casim.engine.particles.dirac_bcc import dirac_step_3d_bcc_splitstep
    if q == 0:
        return dirac_step_3d_bcc_splitstep(eta_u, eta_d, chi_u, chi_d,
                                           m=m, dt=dt, sign=sign)
    ph_in = np.exp(-1j * q * alpha)
    ph_out = np.conj(ph_in)
    out = dirac_step_3d_bcc_splitstep(ph_in * eta_u, ph_in * eta_d,
                                      ph_in * chi_u, ph_in * chi_d,
                                      m=m, dt=dt, sign=sign)
    return tuple(ph_out * comp for comp in out)


# ----------------------------------------------------------------------
# 2. SU(3) rotate-then-step (strong minimal coupling, audited SU(2) pattern)
# ----------------------------------------------------------------------
def su3_rotate_weyl_step_3d_bcc(f_c, g_c, A_oct, eps=1.0, sign='+'):
    """SU(3)-coupled BCC Weyl step for a colour triplet.

    Parameters
    ----------
    f_c, g_c : (3, L, L, L) complex — colour-stacked Weyl spinor.
    A_oct    : (8, L, L, L) real — accumulated gluon potential A^a(x).
    eps      : float — coupling strength (lattice units).
    sign     : BCC chirality branch.
    """
    if A_oct is None or not np.any(A_oct):
        f_n = np.empty_like(f_c)
        g_n = np.empty_like(g_c)
        for c in range(3):
            f_n[c], g_n[c] = weyl_step_3d_bcc(f_c[c], g_c[c], sign=sign)
        return f_n, g_n
    from casim.engine.gauge.gluon import _su3_expmap_field
    V = _su3_expmap_field(eps * A_oct)            # (L,L,L,3,3)
    # Site-local colour rotation: q̃_i = V_ij q_j  (colour axis first).
    f_rot = np.einsum('xyzij,jxyz->ixyz', V, f_c)
    g_rot = np.einsum('xyzij,jxyz->ixyz', V, g_c)
    f_n = np.empty_like(f_rot)
    g_n = np.empty_like(g_rot)
    for c in range(3):
        f_n[c], g_n[c] = weyl_step_3d_bcc(f_rot[c], g_rot[c], sign=sign)
    return f_n, g_n


def su3_global_transform(f_c, g_c, V):
    """Apply a constant V ∈ SU(3) to a colour triplet (Ward-identity tests)."""
    f_t = np.einsum('ij,jxyz->ixyz', V, f_c)
    g_t = np.einsum('ij,jxyz->ixyz', V, g_c)
    return f_t, g_t


def su3_adjoint_transform_potential(A_oct, V):
    """A^a T^a → V (A^a T^a) V†, returned in octet components (exact:
    re-projected with A'^a = 2 tr(T^a H'), tr(T^aT^b) = δ_ab/2)."""
    from casim.engine.gauge import strong as cstr
    H = np.einsum('aij,axyz->xyzij', cstr.T_GEN, A_oct)
    H_t = np.einsum('ij,xyzjk,lk->xyzil', V, H, np.conj(V))
    # tr(T^a H') = Σ_ij T^a_ij H'_ji  (real: both Hermitian)
    return 2.0 * np.real(np.einsum('aij,xyzji->axyz', cstr.T_GEN, H_t))


# ----------------------------------------------------------------------
# 3. U(1) per-link covariant step (Stage 2, photon-fermion coupling
#    roadmap) — the directional handle §1.2 found missing from #1's wrap.
# ----------------------------------------------------------------------
def u1_link_weyl_step_3d_bcc(f, g, A, q, sign='+'):
    """Per-link Peierls-phase U(1)-covariant BCC Weyl step — the U(1)
    analogue of ``weak_wmu.covariant_weyl_step_3d_bcc_exact``.

    Why #1's wrap (``u1_wrap_weyl_step_3d_bcc``) cannot push a fermion
    -----------------------------------------------------------------
    That construction multiplies ψ by a *single* site phase e^{∓iqα(x)}
    before and after the *same* unbiased kinetic step — a common factor
    applied uniformly across all 8 BCC hop directions from x. A common
    factor cannot bias the hop amplitude in one direction over its
    opposite, and a direction-biased hop is what momentum transfer *is*
    (roadmap §1.2). This function supplies the missing directional handle
    by attaching a **separate** Peierls phase to **each** of the 8
    fractional shifts that already appear in the BCC unitary's own
    decomposition (``weak_wmu._spinor_matrix``'s docstring):

        U_BCC(k) = Σ_{d∈BCC_DIRS} M_d · e^{ik·d/√3}
        ψ'(x)    = Σ_d  U_d(x) · [M_d · shift_{d/√3}ψ](x) ,
        U_d(x)   = exp( i q A(x)·d/√3 )

    ``U_d(x)`` is the discretised Wilson-line phase for the hop of
    physical length ``d/√3`` that ``bcc_fractional_shift`` already
    implements, evaluated (to leading order) at the destination site —
    the same site-local convention ``make_w_link_field``'s SU(2) links use.
    Since ``d`` and ``-d`` are antipodal BCC directions, ``U_d(x)`` and
    ``U_{-d}(x)`` are exact complex conjugates whenever ``A(x)≠0`` and not
    parallel to the hop: the +d and −d hop amplitudes genuinely differ.
    That asymmetry is the force this model has been missing.

    The known tension (stated up front, per the roadmap)
    ------------------------------------------------------
    ``covariant_weyl_step_3d_bcc_exact``'s own docstring already records
    it for the SU(2) case: ``Σ_d U_d M_d shift_d`` is unitary **only**
    when every ``U_d = I``. The same is true here — see
    :func:`u1_link_norm_drift` and the fork adjudication in
    ``engine/forks/gauge/u1_link_unitarity_forks.py`` (Stage 2's declared
    risk: a construction that pushes the fermion and one that conserves
    its norm may not be the same operator).

    **Exact special case — spatially uniform A.** When ``A(x)≡A0`` is a
    constant vector (not a genuine field), every ``U_d(x)=e^{iqA0·d/√3}``
    is also constant, and the whole sum becomes exactly
    ``Σ_d M_d e^{i(k+qA0)·d/√3} = U_BCC(k+qA0)`` — a **rigid shift of the
    momentum argument of the same unitary**, unitary for every argument
    because ``U_BCC`` is unitary for every argument. This is the lattice
    form of the continuum canonical-momentum shift ``p→p-qA`` and is
    verified bit-for-bit in the Stage-2 finding. The tension above is
    strictly a property of *non-uniform* A — genuinely local physics, not
    a flaw in the mechanism.

    Parameters
    ----------
    f, g : (Lx,Ly,Lz) complex — Weyl spinor (spin ↑, ↓).
    A    : (3,Lx,Ly,Lz) real — the U(1) vector potential the fermion
           reads (site-local convention; Stage 3 supplies the dynamical
           source). ``None`` or all-zero reduces exactly to the free step.
    q    : float — the particle's U(1) charge (exact Fraction upstream).
    sign : BCC chirality branch.

    Returns
    -------
    f_new, g_new
    """
    if q == 0 or A is None or not np.any(A):
        return weyl_step_3d_bcc(f, g, sign=sign)

    from casim.numerics import fft as _fft
    from casim.engine.lattice.geometry import make_kgrid_3d
    from casim.engine.lattice.bcc import bcc_fractional_shift
    from casim.engine.gauge.weak_wmu import BCC_DIRS, _SPINOR_MATS
    from casim.constants import c_lat

    KX, KY, KZ = make_kgrid_3d(*f.shape)
    F_k = _fft.fftn(f)
    G_k = _fft.fftn(g)
    M_mats = _SPINOR_MATS[sign]
    inv_sqrt3 = c_lat

    f_new = np.zeros_like(f)
    g_new = np.zeros_like(g)
    for i, (dx, dy, dz) in enumerate(BCC_DIRS):
        f_sh = _fft.ifftn(bcc_fractional_shift(F_k, KX, KY, KZ, dx, dy, dz))
        g_sh = _fft.ifftn(bcc_fractional_shift(G_k, KX, KY, KZ, dx, dy, dz))
        M = M_mats[i]
        f_rot = M[0, 0] * f_sh + M[0, 1] * g_sh
        g_rot = M[1, 0] * f_sh + M[1, 1] * g_sh
        phase = q * inv_sqrt3 * (A[0] * dx + A[1] * dy + A[2] * dz)
        U_d = np.exp(1j * phase)
        f_new += U_d * f_rot
        g_new += U_d * g_rot
    return f_new, g_new


def u1_link_norm_drift(f, g, A, q, sign='+'):
    """‖ψ'‖² − ‖ψ‖² for one :func:`u1_link_weyl_step_3d_bcc` tick — the
    diagnostic the Stage-2 fork adjudication reads. Zero exactly when
    ``A≡0``; zero to machine precision when ``A`` is spatially uniform
    (see that function's docstring); generically nonzero, and the subject
    of the fork bound, otherwise."""
    f2, g2 = u1_link_weyl_step_3d_bcc(f, g, A, q, sign=sign)
    n0 = float(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2))
    n1 = float(np.sum(np.abs(f2) ** 2 + np.abs(g2) ** 2))
    return n1 - n0
