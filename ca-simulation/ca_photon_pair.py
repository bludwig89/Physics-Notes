"""
ca_photon_pair.py  —  The photon as a bound pair of two spin-½ Weyl quanta
==========================================================================

McPhee's "spinor electrodynamics" picture (notebook pp.5–6): the photon is
NOT a single spin-1 gauge boson, and NOT the helicity↔branch composite bilinear
of `ca_maxwell.py` (which is birefringent and excluded by GRB/AGN polarimetry —
F65/F66/F67).  It is a BOUND PAIR of two spin-½ "fermion-photons" γ_{1/2} that
"behave together like a single boson γ that only occurs as a pair.  They don't
occur separately."  (A Cooper-pair-like, massless, spin-1 bound state.)

The decisive structural difference from the retired composite bilinear
(F67/F68):

  * Composite σ-bilinear (RETIRED as the photon): the two photon helicities
    F^± = E ± iB are assigned to the two BCC chiral branches independently
    (F^+ ↔ Ω^+, F^- ↔ Ω^-).  A generic linear polarization populates both, so
    they split → linear vacuum BIREFRINGENCE (ΔΩ = Ω^+ − Ω^-).  Excluded.

  * Paired photon (THIS module): the photon is the SYMMETRIC (+,−) bound pair.
    Total momentum k is shared, each constituent carrying k/2 — one on the +
    branch, one on the − branch.  The pair phase is the SUM of the constituent
    phases:

        Ω_pair(k) = ω⁺(k/2) + ω⁻(k/2)  ≡  Ω_even(k).

    Because the pair ALWAYS contains both branches symmetrically ("only occurs
    as a pair"), there is no "+only" photon to split off — both helicities of
    the resulting (E,B) field ride the single rate Ω_pair.  NON-birefringent.

This is the physical mechanism behind F68's "identity channel": the U(1) gauge
phase e^{iθ}·I is helicity-blind, and the only (E,B) construction consistent
with it is the helicity-symmetric pair, whose rate is ω⁺(k/2)+ω⁻(k/2).

Massless & luminal: at small k, ω±(k/2) → (1/√3)(k/2)/... so Ω_pair → (1/√3)|k|
(no gap; the binding energy makes the pair rest-massless), giving c = 1/√3
(F26), identical to the constituent light speed.

Propagator: the paired photon's (E,B) evolves by the even-law rotation
R(Ω_pair) — which is exactly `ca_wmu._f26_rotation_step` (already the W/Z law).
So no new propagator is needed; this module names it as THE photon law and
provides the pair construction + verification helpers.

CLAUDE.md: closed-form dispersion + real 2×2 (E,B) rotation only; the spinor
constituents go through the audited ca_bcc Weyl walk.  No np.linalg.eig on
chiral matrices.
"""

import numpy as np
import ca_fft as _fft
from ca_lattice import make_kgrid_3d
from ca_bcc import bcc_dispersion
from ca_wmu import _f26_rotation_step

ROOT3 = np.sqrt(3.0)


# ----------------------------------------------------------------------
# Pair dispersion  Ω_pair(k) = ω⁺(k/2) + ω⁻(k/2)  (= Ω_even)
# ----------------------------------------------------------------------
def pair_dispersion(kx, ky, kz):
    """Rotation rate per tick of the bound (+,−) photon pair.

    Total momentum k is shared by the two constituents (k/2 each); the pair
    phase is the sum of the two constituent branch phases at k/2.  This is the
    helicity-symmetric (non-birefringent) rate.  Scalars or arrays.
    """
    wp = bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='+')
    wm = bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='-')
    return wp + wm


def pair_birefringence(kx, ky, kz):
    """ΔΩ that the pair does NOT have (would be the split if the photon could
    occur as a single branch).  Returned for diagnostics/contrast only."""
    Op = 2.0 * bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='+')
    Om = 2.0 * bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='-')
    return Op - Om


# ----------------------------------------------------------------------
# The photon propagator: even-law (E,B) rotation at Ω_pair.
# (This IS ca_wmu._f26_rotation_step; named here as the canonical photon law.)
# ----------------------------------------------------------------------
def photon_step_spectral(E, B):
    """One tick of the paired-photon (E,B) evolution on an (3,Lx,Ly,Lz) real
    field.  Rotates the (E,B) pair by R(Ω_pair(k)) per Fourier mode — the
    helicity-symmetric, non-birefringent law.

    Returns (E_new, B_new), real, norm-conserving.
    """
    shape = E.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    E_new = np.zeros_like(E)
    B_new = np.zeros_like(B)
    for a in range(3):
        ek = _fft.fftn(E[a])
        bk = _fft.fftn(B[a])
        ek2, bk2 = _f26_rotation_step(ek, bk, KX, KY, KZ)
        E_new[a] = _fft.ifftn(ek2).real
        B_new[a] = _fft.ifftn(bk2).real
    return E_new, B_new


# ----------------------------------------------------------------------
# Pair construction helper: build the photon (E,B) from a transverse
# polarization, and confirm both helicities ride the single rate Ω_pair.
# ----------------------------------------------------------------------
def build_pair_mode(L, m_index, khat, e1):
    """Plant one real, linearly polarized photon Fourier mode at lattice index
    (m,m,m)·sign(khat-axes): E ∥ e1, B ∥ e2 = k̂×e1, |E|=|B| (a standard
    transverse EM mode — populates both RS helicities F^± = E ± iB).

    The pairing is implicit in the propagator (photon_step_spectral): both
    helicities ride Ω_pair, so this single field is the bound pair.
    Returns (E, B, e1, e2).
    """
    khat = np.asarray(khat, float); khat = khat / np.linalg.norm(khat)
    e1 = np.asarray(e1, float); e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(khat, e1); e2 /= np.linalg.norm(e2)
    Ek = np.zeros((3, L, L, L), complex)
    Bk = np.zeros((3, L, L, L), complex)
    idx = tuple(int(round(m_index)) for _ in range(3))
    cidx = tuple((-int(round(m_index))) % L for _ in range(3))
    for a in range(3):
        Ek[a][idx] = e1[a]; Bk[a][idx] = e2[a]
        Ek[a][cidx] = np.conj(e1[a]); Bk[a][cidx] = np.conj(e2[a])
    E = np.array([_fft.ifftn(Ek[a]).real for a in range(3)])
    B = np.array([_fft.ifftn(Bk[a]).real for a in range(3)])
    return E, B, e1, e2


def group_velocity(nhat, h=1e-5):
    """|dΩ_pair/d|k|| along nhat at small k (the photon's signal speed)."""
    nhat = np.asarray(nhat, float); nhat = nhat / np.linalg.norm(nhat)
    kx, ky, kz = h * nhat
    return float(pair_dispersion(kx, ky, kz) / h)


if __name__ == '__main__':
    # quick self-check
    n = np.array([1, 1, 1.]) / ROOT3
    print("Ω_pair(body diag, k=0.3) =", pair_dispersion(*(0.3 * n)))
    print("group velocity → 1/√3 =", group_velocity(n), "vs", 1 / ROOT3)
