"""
ca_majorana.py — three-generation Higgs-free see-saw and PMNS mixing
====================================================================

Promotes the F47 single-flavour Majorana / see-saw primitives to the full
3x3 case (F47 open follow-up #1).  This module builds the 6x6 see-saw matrix

        M6 = [[ 0 ,  M_D ],
              [ M_D^T, M_R ]]                                   (F47 §Open #2)

with M_R textured by the F93/F76 Z3 (E_g-condensate) generation structure
(F201): in the cube-axis ("generation-axis") basis the E_g channel is the
unique NON-mixing, diagonal-traceless splitter (F93 O1), so the E_g texture
gives a *diagonal* M_R,

        sqrt(M_a) = M_R0 [ 1 + sqrt2 cos(delta_nu + 2 pi a/3) ],  a = 0,1,2.

M_D (Dirac) is likewise diagonal in the SAME cube-axis basis when it too is an
A_1g + E_g object (charged-lepton texture, F76/F93 at delta_e = 12.73 deg).

CENTRAL STRUCTURAL RESULT (see F236):
  With M_R and M_D both E_g-textured, they are SIMULTANEOUSLY diagonal in the
  cube-axis basis, so the light-neutrino mass matrix m_nu = -M_D M_R^{-1} M_D^T
  is diagonal and the PMNS matrix is the IDENTITY.  Large lepton mixing is
  therefore NOT a free fit here: it is forced to come from the second-shell
  T_2g (axis-mixing) channel — exactly the F93 falsifiable commitment #1 that
  T_2g is the unique off-diagonal (CKM/PMNS-like) channel.  The E_g texture
  fixes the three light MASSES (and their splittings); the PMNS ANGLES are the
  T_2g input that the E_g texture does not pin.

Numerics caution (House Rule): numpy/scipy eigen-routines on complex/near-
degenerate matrices can silently mishandle real/imag parts, so every spectrum
returned here is checked with a hand-rolled residual ||M v - lambda v||, and
the block-diagonalisation is cross-checked against the exact type-I see-saw
formula m_nu = -M_D M_R^{-1} M_D^T.

Real arithmetic throughout (the textures are real-symmetric); complex phases
(Dirac CP phase) are supported via complex M_D / M_R but default to real --
see F353 for the delta_CP / Jarlskog-invariant machinery (jarlskog_invariant,
sin_delta_cp) and the Takagi-factorisation fix that makes the complex branch
trustworthy for phase-sensitive quantities.
"""

from __future__ import annotations

import numpy as np

SQRT2 = np.sqrt(2.0)


# ---------------------------------------------------------------------------
# 1.  The E_g / Z3 generation texture (F76 C6, F93 O4, F201)
# ---------------------------------------------------------------------------

def z3_sqrt_texture(delta_rad: float) -> np.ndarray:
    """The F93/F76 Z3 texture amplitudes  1 + sqrt2 cos(delta + 2 pi a/3).

    These are the sqrt-mass amplitudes (per-constituent, F92) up to the
    overall scale M_0; squaring gives the mass eigenvalues.
    """
    return np.array(
        [1.0 + SQRT2 * np.cos(delta_rad + 2.0 * np.pi * a / 3.0) for a in range(3)]
    )


def eg_diagonal_matrix(delta_rad: float, scale: float = 1.0) -> np.ndarray:
    """Diagonal 3x3 mass matrix from the E_g texture (cube-axis basis).

    M = scale * diag( (1 + sqrt2 cos(delta + 2 pi a/3))^2 ).
    The E_g channel is diagonal-traceless (F93 O1): it splits the three
    generation axes WITHOUT mixing them, so the matrix is exactly diagonal.
    """
    s = z3_sqrt_texture(delta_rad)
    return scale * np.diag(s ** 2)


# ---------------------------------------------------------------------------
# 2.  The second-shell T_2g (axis-mixing) channel — the PMNS source (F93 #1)
# ---------------------------------------------------------------------------

def t2g_offdiagonal_matrix(t_xy: float, t_yz: float, t_zx: float) -> np.ndarray:
    """Symmetric off-diagonal (T_2g) perturbation on the generation axes.

    T_2g is the UNIQUE second-shell channel that mixes the three cube axes
    (F93 O1, commitment #1).  A real symmetric off-diagonal matrix:

        [[ 0 , t_xy, t_zx],
         [t_xy,  0 , t_yz],
         [t_zx, t_yz,  0 ]].

    These three amplitudes are the mixing (PMNS-angle) inputs that the E_g
    texture does NOT fix.
    """
    return np.array(
        [
            [0.0, t_xy, t_zx],
            [t_xy, 0.0, t_yz],
            [t_zx, t_yz, 0.0],
        ]
    )


# ---------------------------------------------------------------------------
# 3.  The 6x6 see-saw matrix and the exact type-I light-mass formula
# ---------------------------------------------------------------------------

def seesaw_6x6(M_D: np.ndarray, M_R: np.ndarray) -> np.ndarray:
    """Assemble the 6x6 see-saw matrix  [[0, M_D], [M_D^T, M_R]] (F47 #2)."""
    M_D = np.asarray(M_D, dtype=complex)
    M_R = np.asarray(M_R, dtype=complex)
    n = M_D.shape[0]
    M6 = np.zeros((2 * n, 2 * n), dtype=complex)
    M6[:n, n:] = M_D
    M6[n:, :n] = M_D.T
    M6[n:, n:] = M_R
    return M6


def light_mass_matrix(M_D: np.ndarray, M_R: np.ndarray) -> np.ndarray:
    """Exact type-I see-saw light block  m_nu = - M_D M_R^{-1} M_D^T."""
    M_D = np.asarray(M_D, dtype=complex)
    M_R = np.asarray(M_R, dtype=complex)
    return -M_D @ np.linalg.inv(M_R) @ M_D.T


# ---------------------------------------------------------------------------
# 4.  Diagonalisation with a hand-rolled residual check
# ---------------------------------------------------------------------------

def _residual(M: np.ndarray, vals: np.ndarray, vecs: np.ndarray) -> float:
    """max_j || M v_j - lambda_j v_j ||  — the hand-rolled sanity check."""
    r = 0.0
    for j in range(len(vals)):
        v = vecs[:, j]
        r = max(r, float(np.linalg.norm(M @ v - vals[j] * v)))
    return r


def takagi_light_masses(m_nu: np.ndarray):
    """Physical (non-negative) light masses + PMNS mixing from m_nu.

    For a complex symmetric m_nu the physical masses are the singular values
    (Takagi/Autonne factorisation); the PMNS matrix is the associated unitary.
    For a REAL symmetric m_nu this reduces to |eigenvalues| with the
    eigenvector orthogonal matrix, which is what we use (real textures).
    Returns (masses_sorted_ascending, U_pmns, residual).

    F353 fix (2026-09-03): the complex branch previously returned the raw
    eigenvectors of m_nu^dagger m_nu (an eigh call) AS IF they were the Takagi
    U.  That reproduces every modulus |U_ij| exactly -- so it never affected a
    PMNS ANGLE (F236/F254 only ever fit real T_2g, and pmns_angles() below only
    reads np.abs(U)) -- but it silently drops the Takagi phase correction, so
    any phase-sensitive invariant built on it (the Jarlskog invariant, the
    Dirac CP phase) was forced toward an unphysical value regardless of the
    input phases.  See F353 (open-derivations D4 / parameter #26) for the
    numerical demonstration and docs/reviews/F353-review-2026-09-03.md.  The
    correct construction (Horn & Johnson-style, via SVD) is used below and
    verified by reconstructing m_nu = U diag(masses) U^T to machine precision
    (folded into the returned residual), not merely by an eigenvalue check on
    the auxiliary Hermitian matrix.
    """
    m_nu = np.asarray(m_nu)
    # F353: the branch test must be SCALE-RELATIVE.  Light-neutrino m_nu is
    # typically ~1e-9 to 1e-20 in these units (GeV), so np.allclose(imag, 0)
    # at its numpy DEFAULT absolute tolerance (atol=1e-8) silently called
    # EVERY such matrix "real" regardless of its imaginary content -- the
    # complex branch below was unreachable dead code for any physically
    # scaled input.  Compare the imaginary part to the matrix's own scale.
    abs_scale = float(np.max(np.abs(m_nu))) or 1.0
    if np.max(np.abs(m_nu.imag)) <= 1e-10 * abs_scale:
        M = m_nu.real
        w, V = np.linalg.eigh(M)            # M symmetric real
        res = _residual(M, w, V)
        masses = np.abs(w)
        order = np.argsort(masses)
        return masses[order], V[:, order], res
    # Complex-symmetric Autonne-Takagi factorisation m_nu = U diag(masses) U^T,
    # via SVD m_nu = W diag(S) V^dagger (W, V unitary, S >= 0 real).  Symmetry
    # of m_nu forces Phi = V^T W to be diagonal unitary (checked, not assumed);
    # U = W with each column rephased by Phi_ii^{-1/2} then satisfies the
    # Takagi identity exactly (Horn & Johnson, *Matrix Analysis*, Corollary
    # 4.4.4, specialised to n=3).
    W, S, Vh = np.linalg.svd(m_nu)
    Vsvd = Vh.conj().T
    Phi = Vsvd.T @ W
    phi_offdiag_err = float(np.max(np.abs(Phi - np.diag(np.diag(Phi)))))
    col_phase = np.exp(-1j * np.angle(np.diag(Phi)) / 2.0)
    U = W * col_phase[np.newaxis, :]
    masses = S
    order = np.argsort(masses)
    recon_res = float(np.max(np.abs(m_nu - (U * masses[np.newaxis, :]) @ U.T)))
    res = max(phi_offdiag_err, recon_res)
    return masses[order], U[:, order], res


def pmns_angles(U: np.ndarray):
    """Extract (theta12, theta13, theta23) in degrees from a 3x3 mixing U.

    Standard PDG parametrisation moduli:
      s13 = |U_e3|,  s12 = |U_e2| / sqrt(1 - |U_e3|^2),
      s23 = |U_mu3| / sqrt(1 - |U_e3|^2).
    Rows are ordered (e, mu, tau); columns (1,2,3) ascending mass.
    """
    U = np.abs(np.asarray(U))
    s13 = U[0, 2]
    c13 = np.sqrt(max(1.0 - s13 ** 2, 1e-300))
    s12 = U[0, 1] / c13
    s23 = U[1, 2] / c13
    th13 = np.degrees(np.arcsin(np.clip(s13, 0, 1)))
    th12 = np.degrees(np.arcsin(np.clip(s12, 0, 1)))
    th23 = np.degrees(np.arcsin(np.clip(s23, 0, 1)))
    return th12, th13, th23


def jarlskog_invariant(U: np.ndarray) -> float:
    """Standard rephasing-invariant Jarlskog combination (F353).

        J = Im( U_e1 U_mu2 U_e2^* U_mu1^* ),   rows (e,mu,tau), cols (1,2,3).

    J is invariant under U -> U @ diag(phases) (any column/Majorana-phase
    rephasing) -- only the Dirac-type phase content survives in it.  J = 0
    identically whenever U is real (e.g. every F236/F254 result: real T_2g).
    """
    U = np.asarray(U)
    return float(np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0])))


def sin_delta_cp(U: np.ndarray):
    """sin(delta_CP) via J = s12 c12 s13 c13^2 s23 c23 sin(delta) (standard PDG
    relation).  Returns (sin_delta, J); sin_delta is None where the angle
    prefactor is ~0 (delta undefined there, e.g. theta13 = 0).  Does not
    resolve the delta <-> 180 deg - delta branch ambiguity that sin(delta)
    alone carries -- this module only needs whether delta is free, not its
    value.
    """
    th12, th13, th23 = pmns_angles(U)
    J = jarlskog_invariant(U)
    r12, r13, r23 = np.radians(th12), np.radians(th13), np.radians(th23)
    pref = (np.sin(r12) * np.cos(r12) * np.sin(r13) * np.cos(r13) ** 2
            * np.sin(r23) * np.cos(r23))
    if abs(pref) < 1e-12:
        return None, J
    return float(np.clip(J / pref, -1.0, 1.0)), J


# ---------------------------------------------------------------------------
# 5.  Full pipeline
# ---------------------------------------------------------------------------

def three_gen_seesaw(
    M_D_diag,
    delta_nu_rad: float,
    M_R0: float,
    t2g=(0.0, 0.0, 0.0),
    charged_lepton_U=None,
):
    """Build and diagonalise the 3-generation Higgs-free see-saw.

    Parameters
    ----------
    M_D_diag : (3,) Dirac masses in the cube-axis basis (E_g-diagonal).
    delta_nu_rad : the neutrino-sector E_g condensate angle.
    M_R0 : overall Majorana scale.
    t2g : (t_xy, t_yz, t_zx) T_2g axis-mixing amplitudes on M_R (PMNS source).
    charged_lepton_U : optional 3x3 unitary rotating from the charged-lepton
        mass basis to the cube-axis basis; PMNS = U_e^dagger U_nu.  Default
        None => charged leptons already diagonal in the cube-axis basis
        (both sectors E_g at their own angle) => U_e = I.

    Returns a dict of everything the F236 test consumes.
    """
    M_D = np.diag(np.asarray(M_D_diag, dtype=float))
    M_R = eg_diagonal_matrix(delta_nu_rad, scale=M_R0) + t2g_offdiagonal_matrix(*t2g)

    M6 = seesaw_6x6(M_D, M_R)
    m_nu = light_mass_matrix(M_D, M_R)

    masses, U_nu, res_mnu = takagi_light_masses(m_nu)

    # PMNS = U_e^dagger U_nu (charged-lepton rotation on the left)
    if charged_lepton_U is None:
        U_pmns = U_nu
    else:
        U_pmns = np.asarray(charged_lepton_U).conj().T @ U_nu
    th12, th13, th23 = pmns_angles(U_pmns)

    # cross-check: smallest 3 |eigenvalues| of the full 6x6 vs the type-I block
    w6 = np.linalg.eigvals(M6)
    light6 = np.sort(np.abs(w6))[:3]
    seesaw_consistency = float(
        np.max(np.abs(np.sort(masses) - np.sort(light6)))
    )

    return {
        "M_D_diag": np.asarray(M_D_diag, dtype=float).tolist(),
        "delta_nu_deg": float(np.degrees(delta_nu_rad)),
        "M_R0": float(M_R0),
        "t2g": list(t2g),
        "M_R": M_R.tolist(),
        "light_masses": masses.tolist(),
        "dm21_sq": float(masses[1] ** 2 - masses[0] ** 2),
        "dm31_sq": float(masses[2] ** 2 - masses[0] ** 2),
        "pmns_angles_deg": {"theta12": th12, "theta13": th13, "theta23": th23},
        "U_pmns_abs": np.abs(U_pmns).tolist(),
        "residual_mnu": res_mnu,
        "seesaw_6x6_vs_typeI": seesaw_consistency,
    }
