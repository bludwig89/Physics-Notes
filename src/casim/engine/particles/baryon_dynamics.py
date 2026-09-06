#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_baryon_dynamics.py
=====================

P2 of docs/roadmaps/roadmap-matter-binding.md — the DYNAMICAL baryon: a real-time, non-
dispersing, mass-measured three-quark bound state (proton uud, then neutron
udd), replacing the operator-level colour singlet of F71 with a genuine
solution of the three-body Schrodinger problem.

WHAT THIS DELIVERS (and what it must obey)
------------------------------------------
F97 proved a NO-GO: the baryon mass CANNOT come from constituent-phase
kinematics (PDG current-quark sum is 0.96% of m_p) — the only stable colour
combinations are N-ality-0 closures, and the binder is the Z3 centre phase,
i.e. the confining STRING (P1: F70 area law / F94 3+1D MC sigma / F110 real-time
flux tube). So the dynamical baryon's mass must be sourced predominantly by the
P1 confining potential, NOT by the sum of quark masses. This module makes that
quantitative: it solves the three-body Hamiltonian whose pairwise interaction is
the P1 confining + one-gluon-exchange Cornell potential and shows the relative
(confinement+kinetic) energy is the bulk of the mass.

THE MODEL
---------
Rest-frame three equal-mass constituents -> a six-dimensional relative problem in
mass-normalised Jacobi coordinates (xi1, xi2):

    xi1 = (r1 - r2)/sqrt2 ,   xi2 = (r1 + r2 - 2 r3)/sqrt6

so the relative kinetic operator is diagonal, T = -(1/2m)(grad^2_xi1 + grad^2_xi2),
and the three pair separations are linear forms r_p = (w_p . xi):

    pair(12): w = (sqrt2, 0)           |w|^2 = 2
    pair(13): w = (sqrt2/2,  sqrt6/2)  |w|^2 = 2
    pair(23): w = (-sqrt2/2, sqrt6/2)  |w|^2 = 2

The pairwise potential is the Casimir-scaled Cornell potential (colour 3bar in a
baryon -> the qq attraction is HALF the qqbar one; the confining slope is shared):

    V_p(r) = (1/2) sigma r  -  (2 alpha_s / 3) (1/2) (1/r)
           = (sigma/2) r  -  (alpha_s/3) (1/r)             (per pair)

[The 1/2 colour factor: <T^a.T^a>_{3bar} = -2/3 vs -4/3 for a singlet qqbar, so
each qq pair feels half the meson Cornell strength. Summed over the three pairs
this reproduces the standard quark-model "1/2 sum_{i<j}" baryon potential.]

ENGINE — explicitly-correlated Gaussians (ECG)
----------------------------------------------
The relative wavefunction is expanded in correlated Gaussians

    g_A(xi) = exp(-1/2 xi^T (A (x) I3) xi) ,   A symmetric 2x2 positive definite,

for which the overlap, kinetic energy, and the matrix elements of r and 1/r are
ALL closed-form (no quadrature in the linear solve). The ground state is the
lowest root of the generalised eigenproblem  H c = E S c.  This is the F74 two-
body solver generalised to three bodies; the F74 contact well is replaced by the
confining Cornell channel and the secular root by the ECG generalised eigensolve.

CLOSED-FORM MATRIX ELEMENTS (C = A + B, beta_p = w_p^T C^{-1} w_p):
    S_AB              = det(C)^{-3/2}                      (overlap, const dropped)
    <T>_AB / S_AB     = (3/2)(1/m) Tr(A C^{-1} B)
    <r_p>_AB / S_AB   = sqrt(8 beta_p / pi)
    <1/r_p>_AB / S_AB = sqrt(2 / (pi beta_p))
    <r_p^2>_AB / S_AB = 3 beta_p                           (used for HO self-test)

All arithmetic is REAL (real symmetric generalised eigenproblem); no
chiral/complex transforms, so the CLAUDE.md numpy caveat does not bite. The
generalised eigenproblem is solved TWO independent ways — scipy.linalg.eigh(H,S)
and a hand-rolled Cholesky reduction + numpy.linalg.eigvalsh — which must agree
to machine precision (the F74 "two routes" discipline).

Author note: the colour/Casimir factors and the Cornell form are standard quark-
model inputs; sigma is the P1 string tension, alpha_s the strong coupling, m the
constituent quark mass. Everything dimensionful is carried in units of sqrt(sigma)
unless an explicit scale is supplied (the absolute MeV is a P6 concern).
"""

from __future__ import annotations

import numpy as np

from casim.constants import sqrt_sigma_GeV as SQRT_SIGMA_GEV_DEFAULT

try:
    from scipy.linalg import eigh as _scipy_eigh
    _HAVE_SCIPY = True
except Exception:  # pragma: no cover
    _HAVE_SCIPY = False


# ---------------------------------------------------------------------------
#  Jacobi pair-weight vectors (equal masses; mass-normalised Jacobi).
#    r_p = w_p . (xi1, xi2),  with |w_p|^2 = 2 for all three pairs.
# ---------------------------------------------------------------------------
S2 = np.sqrt(2.0)
S6 = np.sqrt(6.0)
PAIR_W = {
    "12": np.array([S2, 0.0]),
    "13": np.array([S2 / 2.0, S6 / 2.0]),
    "23": np.array([-S2 / 2.0, S6 / 2.0]),
}


# ===========================================================================
#  ECG matrix-element kernels (general symmetric 2x2 A, B).
# ===========================================================================
def _overlap(C):
    """S_AB = det(C)^{-3/2}  (the (2pi)^3 constant cancels in the gen. eig)."""
    return np.linalg.det(C) ** (-1.5)


def _kinetic_over_S(A, B, C, m):
    """<T>/<S> = (3/2)(1/m) Tr(A C^{-1} B)."""
    Cinv = np.linalg.inv(C)
    return 1.5 / m * np.trace(A @ Cinv @ B)


def _beta_pairs(C):
    """beta_p = w_p^T C^{-1} w_p for the three pairs."""
    Cinv = np.linalg.inv(C)
    return {p: float(w @ Cinv @ w) for p, w in PAIR_W.items()}


def _r_over_S(beta):
    """<r>/<S> for a single pair, Gaussian marginal variance beta."""
    return np.sqrt(8.0 * beta / np.pi)


def _inv_r_over_S(beta):
    """<1/r>/<S>."""
    return np.sqrt(2.0 / (np.pi * beta))


def _r2_over_S(beta):
    """<r^2>/<S>  (used only by the harmonic self-test)."""
    return 3.0 * beta


# ===========================================================================
#  Basis generation — geometric (GEM) mesh of correlated Gaussians.
#    Diagonal A = diag(1/a^2, 1/c^2) over geometric width meshes, PLUS a set of
#    correlated (off-diagonal) Gaussians to capture rho-lambda correlation.
# ===========================================================================
# 120-degree kinematic rotation of the Jacobi pair (xi1,xi2) under the cyclic
# particle permutation (1->2->3->1).  Derived exactly:
#   xi1' = -1/2 xi1 + sqrt3/2 xi2 ,  xi2' = -sqrt3/2 xi1 - 1/2 xi2.
# A Gaussian g_A -> g_{R^T A R} under this map; closing the basis under R makes
# the totally symmetric (S3) baryon ground state EXACTLY representable, so the
# three pair radii come out equal to machine precision.
_R_CYC = np.array([[-0.5, np.sqrt(3.0) / 2.0],
                   [-np.sqrt(3.0) / 2.0, -0.5]])


def symmetrize_basis(basis):
    """Append the two cyclic-permutation images R^T A R, R^T^2 A R^2 of each A,
    closing the basis under the 3-cycle (combined with the xi1-reflection the
    diagonal Gaussians already respect, this spans the full S3-symmetric space)."""
    R, R2 = _R_CYC, _R_CYC @ _R_CYC
    out = list(basis)
    for A in basis:
        out.append(R.T @ A @ R)
        out.append(R2.T @ A @ R2)
    return out


def make_basis(n1=8, n2=8, a_min=0.2, a_max=8.0, correlated=True, symmetrize=True):
    """Return a list of symmetric 2x2 A matrices (positive definite).

    symmetrize=True closes the set under the cyclic particle permutation so the
    spatial ground state is exactly S3-symmetric (machine-precision equal pair
    radii); set False for the bare (asymmetric) variational mesh."""
    a_vals = a_min * (a_max / a_min) ** (np.arange(n1) / max(n1 - 1, 1))
    c_vals = a_min * (a_max / a_min) ** (np.arange(n2) / max(n2 - 1, 1))
    basis = []
    for a in a_vals:
        for c in c_vals:
            basis.append(np.array([[1.0 / a ** 2, 0.0], [0.0, 1.0 / c ** 2]]))
    if correlated:
        # a modest set of correlated Gaussians: shared width with off-diagonal
        # coupling +/- rho*sqrt(d11 d22).  Keeps A positive definite (|rho|<1).
        for a in a_vals[::2]:
            for rho in (-0.5, 0.5):
                d = 1.0 / a ** 2
                off = rho * d
                basis.append(np.array([[d, off], [off, d]]))
    if symmetrize:
        basis = symmetrize_basis(basis)
    return basis


# ===========================================================================
#  Assemble H and S, solve the generalised eigenproblem two ways.
# ===========================================================================
def build_HS(basis, m, sigma, alpha_s, conf_per_pair=1.0, oge_casimir=2.0 / 3.0):
    """Build the relative Hamiltonian and overlap matrices in the ECG basis.

    Pairwise Cornell potential (roadmap-literal default):
        V_p(r) = conf_per_pair * sigma * r  -  oge_casimir * alpha_s * (1/r)

    Defaults reproduce the roadmap spec  V_p = sigma r - (2 alpha_s/3)/r:
      * conf_per_pair = 1   -> full string tension sigma on each pair;
      * oge_casimir   = 2/3 -> the qq-in-3bar colour Casimir factor for OGE.
    Set conf_per_pair=1/2 (and oge_casimir=1/3) for the alternative '1/2 rule'
    Casimir-scaling of BOTH terms; the STRUCTURAL results (confinement
    dominance, n-p sign, two-route agreement) are invariant under this choice.
    """
    n = len(basis)
    H = np.zeros((n, n))
    Smat = np.zeros((n, n))
    kappa = oge_casimir * alpha_s   # Coulomb coeff per pair
    slope = conf_per_pair * sigma   # confining slope per pair
    for i in range(n):
        for j in range(i, n):
            A, B = basis[i], basis[j]
            C = A + B
            S = _overlap(C)
            T = _kinetic_over_S(A, B, C, m) * S
            betas = _beta_pairs(C)
            V = 0.0
            for p, beta in betas.items():
                V += (slope * _r_over_S(beta) - kappa * _inv_r_over_S(beta)) * S
            H[i, j] = H[j, i] = T + V
            Smat[i, j] = Smat[j, i] = S
    return H, Smat


def _solve_canonical(H, S, tol=1e-10, want_vec=False):
    """Generalised eigenproblem via canonical orthogonalisation — robust to the
    near-singular overlap of an overcomplete (e.g. symmetrised) Gaussian basis.

    S = U s U^T ; keep columns with s_i/s_max > tol ; X = U_keep diag(s^{-1/2}) ;
    diagonalise X^T H X.  Returns (eigvals[, ground_vec_in_original_basis])."""
    sval, U = np.linalg.eigh(S)
    keep = sval / sval.max() > tol
    X = U[:, keep] / np.sqrt(sval[keep])
    Hp = X.T @ H @ X
    Hp = 0.5 * (Hp + Hp.T)
    w, v = np.linalg.eigh(Hp)
    if want_vec:
        c0 = X @ v[:, 0]
        return w, c0
    return w, None


def _solve_gen_eig_cholesky(H, S):
    """Lowest generalised eigenvalue via hand-rolled Cholesky reduction.
    S = L L^T ;  solve standard eig of  L^{-1} H L^{-T}.  numpy only."""
    L = np.linalg.cholesky(S)
    Linv = np.linalg.inv(L)
    M = Linv @ H @ Linv.T
    M = 0.5 * (M + M.T)            # symmetrise against round-off
    w = np.linalg.eigvalsh(M)
    return float(w[0]), w


def _solve_gen_eig_scipy(H, S):
    """Lowest generalised eigenvalue via scipy.linalg.eigh(H, S)."""
    if not _HAVE_SCIPY:
        return None, None
    w = _scipy_eigh(H, S, eigvals_only=True)
    return float(w[0]), w


def spectrum_and_ground_vector(m, sigma, alpha_s, basis=None,
                               conf_per_pair=1.0, oge_casimir=2.0 / 3.0):
    """Return (eigenvalues, ground eigenvector, basis, H, S) via Cholesky route.

    The eigenvector is normalised in the S metric (c^T S c = 1).  A confining
    potential has a PURELY DISCRETE spectrum (no scattering continuum), so every
    eigenvalue is a genuine bound, non-dispersing state — the ground state in
    particular cannot fall apart, the dynamical realisation of F71's energetic
    confinement argument.
    """
    if basis is None:
        basis = make_basis()
    H, S = build_HS(basis, m, sigma, alpha_s, conf_per_pair, oge_casimir)
    w, c0 = _solve_canonical(H, S, want_vec=True)   # robust to overcomplete S
    return w, c0, basis, H, S


def pair_radii(c0, basis, conf_per_pair=1.0, oge_casimir=2.0 / 3.0):
    """Ground-state pair separations <r_p> for the three pairs, S-normalised.

    For equal masses the Hamiltonian is symmetric under the three Jacobi
    rearrangements, so the ground state is totally spatially symmetric (S3) and
    the three <r_p> must be equal — the spin/colour antisymmetry of the baryon
    rides on a SYMMETRIC spatial wavefunction (F71 BS6/BS7)."""
    n = len(basis)
    out = {}
    norm = 0.0
    for p, w in PAIR_W.items():
        acc = 0.0
        for i in range(n):
            for j in range(n):
                C = basis[i] + basis[j]
                S = _overlap(C)
                beta = float(w @ np.linalg.inv(C) @ w)
                acc += c0[i] * c0[j] * _r_over_S(beta) * S
        out[p] = acc
    # normalisation <psi|psi>
    for i in range(n):
        for j in range(n):
            C = basis[i] + basis[j]
            norm += c0[i] * c0[j] * _overlap(C)
    return {p: out[p] / norm for p in out}


def ground_state_relative_energy(m, sigma, alpha_s, basis=None, method="both",
                                 conf_per_pair=1.0, oge_casimir=2.0 / 3.0):
    """Relative-coordinate ground-state energy E_rel of the three-body system.

    Returns a dict with E_rel from each method and their difference (the
    'two routes agree to machine precision' check).  E_rel is the kinetic +
    pairwise-Cornell energy in the rest frame; the baryon mass is
    M = 3 m + E_rel (equal-mass case).
    """
    if basis is None:
        # energy / two-route checks want a WELL-CONDITIONED mesh (the symmetrised
        # mesh is overcomplete -> singular S); symmetry is verified separately.
        basis = make_basis(symmetrize=False)
    H, S = build_HS(basis, m, sigma, alpha_s, conf_per_pair, oge_casimir)
    E_chol, _ = _solve_gen_eig_cholesky(H, S)
    E_scipy, _ = _solve_gen_eig_scipy(H, S)
    out = {"E_rel_cholesky": E_chol, "n_basis": len(basis)}
    if E_scipy is not None:
        out["E_rel_scipy"] = E_scipy
        out["route_diff"] = abs(E_chol - E_scipy)
    return out


# ===========================================================================
#  Harmonic self-test: V_p = (1/2) k r_p^2  has the EXACT relative ground
#  energy  E = 3 sqrt(3 k / m)  (two decoupled 3D oscillators, omega=sqrt(3k/m)).
#  A single Gaussian already spans the exact ground state -> machine precision.
# ===========================================================================
def harmonic_ground_energy_exact(k, m):
    return 3.0 * np.sqrt(3.0 * k / m)


def harmonic_ground_energy_ecg(k, m, basis=None):
    if basis is None:
        basis = make_basis(n1=8, n2=8, correlated=False)
    n = len(basis)
    H = np.zeros((n, n))
    Smat = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            A, B = basis[i], basis[j]
            C = A + B
            S = _overlap(C)
            T = _kinetic_over_S(A, B, C, m) * S
            betas = _beta_pairs(C)
            V = sum(0.5 * k * _r2_over_S(beta) * S for beta in betas.values())
            H[i, j] = H[j, i] = T + V
            Smat[i, j] = Smat[j, i] = S
    try:                              # well-conditioned -> Cholesky (full precision)
        E, _ = _solve_gen_eig_cholesky(H, Smat)
        return E
    except np.linalg.LinAlgError:     # overcomplete -> canonical orthogonalisation
        w, _ = _solve_canonical(H, Smat)
        return float(w[0])


# ===========================================================================
#  EM self-energy -- pairwise quark-charge Coulomb from the SAME <1/r> as OGE.
#
#  F372: an independent, model-native check of the ad hoc classical EM self-
#  energy input (delta_em_p=1.00, delta_em_n=0.0 MeV) used by
#  neutron_minus_proton() below.  Re-derives the proton-neutron EM difference
#  from the P2 three-body ground state's own <1/r> -- the SAME position-space
#  expectation value the OGE term already uses -- instead of importing an
#  external classical estimate.  Zero new free parameters.
# ===========================================================================
def pair_inv_radii(c0, basis):
    """Ground-state <1/r_p> for the three pairs, S-normalised (companion to
    pair_radii; the input the pairwise Coulomb self-energy needs)."""
    n = len(basis)
    out = {}
    norm = 0.0
    for p, w in PAIR_W.items():
        acc = 0.0
        for i in range(n):
            for j in range(n):
                C = basis[i] + basis[j]
                Sij = _overlap(C)
                beta = float(w @ np.linalg.inv(C) @ w)
                acc += c0[i] * c0[j] * _inv_r_over_S(beta) * Sij
        out[p] = acc
    for i in range(n):
        for j in range(n):
            C = basis[i] + basis[j]
            norm += c0[i] * c0[j] * _overlap(C)
    return {p: out[p] / norm for p in out}


ALPHA_EM = 1.0 / 137.035999084          # CODATA fine-structure constant

# Quark electric charges in units of e (up-type +2/3, down-type -1/3).  A
# baryon's pairwise Coulomb self-energy is alpha_em * <1/r> * sum_{i<j} q_i q_j;
# for the S3-symmetric P2 ground state <1/r> is common to all three pairs
# (F122 check S4), so the charge structure alone fixes each species' factor:
#   proton (u,u,d):  sum q_i q_j = (2/3)(2/3) + 2*(2/3)(-1/3) = 4/9 - 4/9 = 0
#   neutron(u,d,d):  sum q_i q_j = 2*(2/3)(-1/3) + (-1/3)(-1/3) = -4/9 + 1/9 = -1/3
CHARGE_SUM_PROTON = 0.0
CHARGE_SUM_NEUTRON = -1.0 / 3.0


def em_self_energy_pairwise(m_q, sigma, alpha_s, sqrt_sigma_gev=SQRT_SIGMA_GEV_DEFAULT,
                             basis=None, conf_per_pair=1.0, oge_casimir=2.0 / 3.0):
    """Model-native re-derivation of the proton-neutron EM self-energy
    difference, reusing the P2 three-body ground state's own <1/r>.

        delta_EM(B) = alpha_em * <1/r> * sum_{i<j} q_i q_j      (pairwise Coulomb)

    With the common <1/r> (S3 symmetry, F122 S4) this collapses to a single
    number X = alpha_em * <1/r> times each baryon's charge factor: proton -> 0
    (its two up quarks' mutual repulsion exactly cancels the two u-d
    attractions for a net +1 baryon); neutron -> -X/3 (net attractive).  So
    delta_EM_p - delta_EM_n = +X/3 > 0 -- EM makes the proton's self-energy
    the larger (less negative) of the two, the same qualitative statement
    F122 made from its classical whole-nucleon estimate.

    ``sqrt_sigma_gev`` defaults to the registered ``sqrt_sigma_GeV`` constant
    (D7; F122/F124/F146) -- F122 Sec.5's own quoted empirical string-tension
    scale; this function does not derive it (unifying it with the f_pi anchor
    is F123 Sec.5's open debt) -- it is the same external anchor F122 already
    used to state its own m_p/sqrt(sigma) ~ 2.24 comparison, reused here for
    the same reason: dimensionless P2 output times one length anchor.
    Defaults (m_q=0.785, sigma=1.0, alpha_s=0.5) match F122's own baseline
    three-body solve.
    """
    if basis is None:
        basis = make_basis()
    _, c0, basis2, _, _ = spectrum_and_ground_vector(
        m_q, sigma, alpha_s, basis=basis,
        conf_per_pair=conf_per_pair, oge_casimir=oge_casimir)
    inv_r = pair_inv_radii(c0, basis2)
    inv_r_vals = list(inv_r.values())
    inv_r_spread = max(inv_r_vals) - min(inv_r_vals)           # S3-symmetry check
    inv_r_common = sum(inv_r_vals) / 3.0                        # units of sqrt(sigma)
    inv_r_phys_mev = inv_r_common * sqrt_sigma_gev * 1000.0     # MeV
    X = ALPHA_EM * inv_r_phys_mev                                # MeV
    delta_em_p = CHARGE_SUM_PROTON * X
    delta_em_n = CHARGE_SUM_NEUTRON * X
    return {
        "inv_r_common_units_sqrt_sigma": inv_r_common,
        "inv_r_spread_units_sqrt_sigma": inv_r_spread,
        "inv_r_phys_MeV": inv_r_phys_mev,
        "X_alpha_over_r_MeV": X,
        "delta_em_p_MeV": delta_em_p,
        "delta_em_n_MeV": delta_em_n,
        "delta_em_p_minus_n_MeV": delta_em_p - delta_em_n,
    }


# ===========================================================================
#  Baryon masses and the n-p splitting.
# ===========================================================================
def baryon_mass(m_q, sigma, alpha_s, basis=None):
    """Equal-mass baryon mass M = 3 m_q + E_rel (same units as inputs)."""
    res = ground_state_relative_energy(m_q, sigma, alpha_s, basis=basis)
    E = res.get("E_rel_scipy", res["E_rel_cholesky"])
    return 3.0 * m_q + E, E, res


def neutron_minus_proton(m_u, m_d, sigma, alpha_s, delta_em_p, delta_em_n,
                         basis=None):
    """n(udd) - p(uud) splitting.

    Strong part: to first order the relative (confinement) wavefunction is
    common; the leading difference is the constituent-mass sum
        Delta_strong = (2 m_d + m_u) - (2 m_u + m_d) = (m_d - m_u).
    (A small wavefunction/kinetic response is second order in (m_d-m_u)/m and is
    neglected at this order — the controlled NR statement.)
    EM self-energy is supplied externally (P5 machinery): the proton (uud, two
    charge +2/3 quarks) has the larger Coulomb self-energy, so delta_em_p >
    delta_em_n and EM REDUCES m_n - m_p.

        m_n - m_p = (m_d - m_u) + (delta_em_n - delta_em_p)
    """
    d_strong = (m_d - m_u)
    d_em = (delta_em_n - delta_em_p)
    return {
        "m_d_minus_m_u": d_strong,
        "em_term": d_em,
        "m_n_minus_m_p": d_strong + d_em,
        "sign_positive": (d_strong + d_em) > 0.0,
    }


if __name__ == "__main__":
    # quick smoke run in sqrt(sigma)=1 units, constituent quark baseline
    sigma = 1.0
    alpha_s = 0.5
    m_q = 0.785            # m_constituent / sqrt(sigma) ~ 0.33/0.42 GeV
    M, E, res = baryon_mass(m_q, sigma, alpha_s)
    print("relative-energy routes:", res)
    print(f"E_rel = {E:.6f} sqrt(sigma)")
    print(f"M_baryon = {M:.6f} sqrt(sigma)   (m_p/sqrt(sigma))")
