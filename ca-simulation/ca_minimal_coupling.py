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

from ca_bcc import weyl_step_3d_bcc


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
    from ca_dirac_bcc import dirac_step_3d_bcc_splitstep
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
    from ca_gluon import _su3_expmap_field
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
    import ca_strong as cstr
    H = np.einsum('aij,axyz->xyzij', cstr.T_GEN, A_oct)
    H_t = np.einsum('ij,xyzjk,lk->xyzil', V, H, np.conj(V))
    # tr(T^a H') = Σ_ij T^a_ij H'_ji  (real: both Hermitian)
    return 2.0 * np.real(np.einsum('aij,xyzji->axyz', cstr.T_GEN, H_t))
