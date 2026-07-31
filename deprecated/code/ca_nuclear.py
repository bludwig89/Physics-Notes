# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_nuclear.py
# migrated   : 2026-07-30 - 16:06
# target     : src/casim/engine/particles/nuclear.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_nuclear.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_nuclear.py
=============

P4 of docs/roadmaps/roadmap-matter-binding.md — the first NUCLEUS: the deuteron, a proton and
a neutron bound by the residual strong force.  Full ³S₁–³D₁ coupled-channel
treatment with the pion TENSOR force (the user-selected faithful scope).

PHYSICS
-------
The long-range nucleon-nucleon force is one-pion exchange (OPEP).  In the
deuteron channel (total spin S=1, isospin T=0, J^P=1^+) the static OPEP is

    V_pi(r) = -(f^2/4pi) m_pi [ (sigma1.sigma2) Y(x) + S12 T(x) ],   x = m_pi r/hbar c

    Y(x) = e^{-x}/x ,   T(x) = (1 + 3/x + 3/x^2) e^{-x}/x

with sigma1.sigma2 = +1 (triplet) and the tensor operator
S12 = 3 (sigma1.n)(sigma2.n) - sigma1.sigma2.  S12 is NOT diagonal: it mixes the
L=0 (³S₁) and L=2 (³D₁) partial waves, and in the {³S₁, ³D₁} basis its
spin-angular matrix is the Rarita-Schwinger result

    <S12> = [[ 0,      2*sqrt(2) ],
             [ 2*sqrt(2), -2      ]]          (verified here by CG construction).

Because central OPEP alone is too weak to bind (2 mu V0 a^2/hbar^2 ~ 0.5 < the
Yukawa threshold 1.68), the deuteron binds ONLY through the tensor coupling that
mixes in the D-wave — this is the sharp, falsifiable signature.

ENGINE
------
The radial problem is the F74 two-body bound-state solver generalised from a
single contact channel to a 2-channel (S,D) coupled system: a real symmetric
2N×2N Hamiltonian (finite-difference kinetic + centrifugal + the OPEP potential
matrix), lowest eigenvalue by dense diagonalisation.  A hard core at r_c
regularises the 1/x^3 tensor singularity (the phenomenological short-range core
the model does not yet derive — flagged).

CALIBRATION / INPUTS  (honest accounting)
-----------------------------------------
  • m_pi, f_pi        : from P3 (`ca_meson.py` / F77), the model's own outputs.
  • g_A = 1.2723      : EXTERNAL (measured axial charge) — the one new number,
                        analogous to the ρ's g_rhopipi in P3.
  • f^2/4pi           : DERIVED from the above by Goldberger-Treiman at the
                        nucleon, f_piNN = g_A m_pi/(2 f_pi)  ->  f^2/4pi.
  • M_N = 938.92 MeV  : EXTERNAL nucleon mass (P2 not built; absolute scale is a
                        P6 concern).  Sets the reduced mass mu = M_N/2.
  • r_c               : the short-range core radius — the one tuned knob; tuned
                        to the physical E_b = 2.224 MeV.

The PREDICTION is the binding MECHANISM and structure (tensor force essential,
single shallow 1^+ I=0 bound state, few-percent D-state), not an absolute MeV
from first principles.

All arithmetic REAL.  numpy only.
"""

from __future__ import annotations

import math
import numpy as np
from casim.constants import M_N_isoaveraged_MeV, g_A
from casim.constants import (
    M0_constituent_MeV as _M0_constituent_MeV,
    f_pi_anchor_MeV as _f_pi_anchor_MeV,
)

HBARC = 197.32698        # MeV·fm
M_N = M_N_isoaveraged_MeV  # MeV  (isospin-averaged nucleon mass) — EXTERNAL (P6)
G_A = g_A                # axial charge — EXTERNAL
M_PI_DEFAULT = 138.039   # MeV  (isospin-averaged) — P3 supplies the model value
F_PI_DEFAULT = _f_pi_anchor_MeV     # MeV  — P3/F77 supplies the model value


# ===========================================================================
#  Derived short-range repulsive core (F113) — replaces the tuned hard wall.
#  ---------------------------------------------------------------------------
#  V_core(r;b) = g_cm * [ <H_CM>(r) - 2 E_N ],  with the chromomagnetic energy
#  of the antisymmetrised two-cluster state a closed-form rational function of
#  u = exp(-r^2/4b^2):
#        <H_CM>(r) = (N0 + N1 u + N2 u^2 + N3 u^3)/(D0 + D1 u + D2 u^2 + D3 u^3)
#  The coefficients are EXACT (sum over the 720 six-quark permutations of the
#  F71 colour-singlet x SU(6) deuteron-channel state); extracted once from
#  ca_nuclear_core.py and embedded here so the solver pays no permutation cost.
#  Checks: N0/D0 = -16 = 2 E_N (two free nucleons, r->inf);  sum N/sum D = 8/3
#  ([6] state at full overlap);  V_core(0) = g_cm*(8/3+16) = 56/3 g_cm.
# ===========================================================================
GCM_DEFAULT = 18.31      # MeV  — colour-magnetic coupling from measured N-Delta=293
B_QUARK_DEFAULT = 0.55   # fm   — single-quark Gaussian size (constituent scale)
_CORE_N = (-13436928.0, 15925248.0, 15925248.0, -13436928.0)   # F113 numerator
_CORE_D = (839808.0, 93312.0, 93312.0, 839808.0)               # F113 = norm kernel K
_CORE_2EN = -16.0        # two free nucleons, in units of g_cm


def derived_core_potential(r, b=B_QUARK_DEFAULT, g_cm=GCM_DEFAULT):
    """The F113 short-range repulsive core in MeV at separation r (fm).
    Positive (repulsive), height 56/3*g_cm at r=0, -> 0 as r -> infinity.
    r may be a scalar or numpy array."""
    u = np.exp(-(np.asarray(r, dtype=float) ** 2) / (4.0 * b * b))
    num = _CORE_N[0] + u * (_CORE_N[1] + u * (_CORE_N[2] + u * _CORE_N[3]))
    den = _CORE_D[0] + u * (_CORE_D[1] + u * (_CORE_D[2] + u * _CORE_D[3]))
    return g_cm * (num / den - _CORE_2EN)


# ===========================================================================
#  Intermediate-range ATTRACTION (F115) — scalar-isoscalar (σ) exchange.
#  ---------------------------------------------------------------------------
#  The σ is the chiral scalar PARTNER of the pion (F103/F77 NJL): the model's
#  economical realisation of correlated two-pion exchange.  Both its mass and
#  its NN coupling are model-native:
#    m_σ = 2 m_c = 622 MeV               (F103: the scalar pole sits at 2 m_c)
#    g_σNN = 3 (m_c/f_π)                 (chiral quark model: each constituent
#       quark couples g_σq = m_c/f_π — the σ-analogue of the pion's Goldberger-
#       Treiman; the scalar-isoscalar charge adds coherently over 3 quarks)
#    => g_σNN²/4π = 9 (m_c/f_π)²/4π = 8.09   (squarely in the OBE range 5–9)
#  The σNN vertex is folded over the finite quark size b (a Gaussian density),
#  giving a scalar Yukawa that is FINITE at the origin (no spurious short-range
#  pocket); the closed form uses erfc.  Attractive, central, isoscalar -> added
#  to both ³S₁ and ³D₁ diagonals.
# ===========================================================================
M_C_DEFAULT = _M0_constituent_MeV      # MeV  constituent quark mass (F77 canonical NJL)
M_SIGMA_DEFAULT = 622.4  # MeV  = 2 m_c (F103 scalar pole)
SIGMA_G2_4PI_BARE = 9.0 * (M_C_DEFAULT / F_PI_DEFAULT) ** 2 / (4.0 * math.pi)  # 8.09

_erfc_vec = np.vectorize(math.erfc)


def folded_yukawa(r, m, beta):
    """Scalar Yukawa e^{-mr}/r folded over a Gaussian vertex of width beta (fm):
    the convolution with two Gaussian quark densities (Fourier e^{-q^2 beta^2}).
    Finite at r -> 0.  m in MeV, r in fm.  Returns the dimensionless radial shape
    (-> e^{-x}/x as beta -> 0)."""
    r = np.asarray(r, dtype=float)
    a = m / HBARC                                   # 1/fm
    pre = np.exp((a * beta) ** 2)
    t1 = np.exp(-a * r) * _erfc_vec(a * beta - r / (2.0 * beta))
    t2 = np.exp(a * r) * _erfc_vec(a * beta + r / (2.0 * beta))
    return pre * (t1 - t2) / (2.0 * r)


def sigma_exchange_potential(r, b=B_QUARK_DEFAULT, g2_4pi=SIGMA_G2_4PI_BARE,
                             m_sigma=M_SIGMA_DEFAULT):
    """Intermediate-range scalar-isoscalar (σ) attraction in MeV at r (fm).
    Negative (attractive), V = -(g²/4π)·m_σ·folded_yukawa(r;m_σ,b)."""
    return -g2_4pi * m_sigma * folded_yukawa(r, m_sigma, b)


# ===========================================================================
#  Short-range REPULSION (F128) — isoscalar-VECTOR (ω) exchange.
#  ---------------------------------------------------------------------------
#  The ω is the isoscalar (I=0) member of the q̄q VECTOR (J^P=1^-) RPA pole, the
#  spin-1 sibling of the σ/π channels (F69/F77/F89).  It couples to the conserved
#  BARYON-NUMBER current ψ̄γ^μψ.  Two nucleons each carry B=+1 (like sign), so —
#  exactly as for like electric charges in the paired-photon channel (F69/F89) —
#  the static TIME-COMPONENT vector exchange is REPULSIVE.  This is the only sign
#  difference from the σ: spin-1 (j^0 j^0, like charges repel) vs spin-0 (scalar
#  density, always attractive).  Hence the single sign flip below (+ vs the σ's -).
#  Mass: the vector bubble is flavour-blind, so m_ω = m_ρ up to OZI (~1%); the
#  model's vector pole sits at ~0.78 GeV (m_ω = 782.7 MeV adopted).  The PRECISE
#  NJL value is scheme-dependent because a sharp 3-momentum cutoff breaks vector
#  current conservation (see F128); the degeneracy m_ω=m_ρ is the robust statement.
#  Coupling: g_ωNN = 3 g_ωq (baryon number adds coherently over 3 quarks, exactly
#  as the σ-isoscalar charge does in F126); SU(6) gives g_ωNN = 3 g_ρNN.
# ===========================================================================
M_OMEGA_DEFAULT = 782.66      # MeV  isoscalar-vector pole (= m_ρ up to OZI)
OMEGA_G2_4PI_OBE = 11.0       # g_ωNN²/4π — OBE/SU(6) window value (F128, Tier-B)


def omega_exchange_potential(r, b=B_QUARK_DEFAULT, g2_4pi=OMEGA_G2_4PI_OBE,
                             m_omega=M_OMEGA_DEFAULT):
    """Short-range isoscalar-vector (ω) REPULSION in MeV at r (fm).
    POSITIVE (repulsive) — the lone sign flip vs the σ: V = +(g²/4π)·m_ω·
    folded_yukawa(r;m_ω,b).  Same folded vertex (quark size b) as the σ."""
    return +g2_4pi * m_omega * folded_yukawa(r, m_omega, b)


# ===========================================================================
#  Clebsch-Gordan + the tensor spin-angular matrix <S12> by explicit
#  construction (machine-precision verification of [[0, 2√2],[2√2, -2]]).
# ===========================================================================
def clebsch_gordan(j1, m1, j2, m2, J, M):
    """<j1 m1 j2 m2 | J M> via the Racah closed form (exact for our half-integers)."""
    if m1 + m2 != M:
        return 0.0
    if not (abs(j1 - j2) <= J <= j1 + j2):
        return 0.0
    if abs(m1) > j1 or abs(m2) > j2 or abs(M) > J:
        return 0.0
    f = math.factorial
    pref = (2 * J + 1) * f(int(J + j1 - j2)) * f(int(J - j1 + j2)) * f(int(j1 + j2 - J))
    pref /= f(int(j1 + j2 + J + 1))
    pref *= (f(int(J + M)) * f(int(J - M)) * f(int(j1 - m1)) * f(int(j1 + m1)) *
             f(int(j2 - m2)) * f(int(j2 + m2)))
    pref = math.sqrt(pref)
    s = 0.0
    for k in range(0, int(j1 + j2 + J) + 2):
        d = [j1 + j2 - J - k, j1 - m1 - k, j2 + m2 - k, J - j2 + m1 + k, J - j1 - m2 + k]
        if any(x < 0 for x in d):
            continue
        s += ((-1) ** k) / (f(k) * f(int(j1 + j2 - J - k)) * f(int(j1 - m1 - k)) *
                            f(int(j2 + m2 - k)) * f(int(J - j2 + m1 + k)) *
                            f(int(J - j1 - m2 + k)))
    return pref * s


# Pauli matrices and the two-nucleon (4-dim) spin space.
_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)
_I2 = np.eye(2, dtype=complex)


def _sigma_dot_n(nx, ny, nz):
    return nx * _SX + ny * _SY + nz * _SZ


def _two_nucleon_triplet_basis():
    """|1,+1>, |1,0>, |1,-1> as 4-vectors in |s1 s2> = {uu, ud, du, dd}."""
    uu = np.array([1, 0, 0, 0], dtype=complex)
    ud = np.array([0, 1, 0, 0], dtype=complex)
    du = np.array([0, 0, 1, 0], dtype=complex)
    dd = np.array([0, 0, 0, 1], dtype=complex)
    return {1: uu, 0: (ud + du) / np.sqrt(2.0), -1: dd}


def _Y2(M, theta, phi):
    """Spherical harmonics Y_{2,M} for M in {-1,0,1} (the only ones reached at total M=0)."""
    st, ct = np.sin(theta), np.cos(theta)
    if M == 0:
        return math.sqrt(5.0 / (16.0 * np.pi)) * (3.0 * ct * ct - 1.0)
    if M == 1:
        return -math.sqrt(15.0 / (8.0 * np.pi)) * st * ct * np.exp(1j * phi)
    if M == -1:
        return math.sqrt(15.0 / (8.0 * np.pi)) * st * ct * np.exp(-1j * phi)
    raise ValueError(M)


def tensor_matrix_via_construction(n_theta=48, n_phi=48):
    """Build <³L'₁ | S12 | ³L₁> for L,L' in {0,2} at total J=1, M=0 by quadrature
    over the sphere with explicit spinor-spherical-harmonic states.
    Returns the 2×2 matrix in basis (S=L0, D=L2). Should equal [[0,2√2],[2√2,-2]]."""
    trip = _two_nucleon_triplet_basis()
    sig1 = {  # sigma1 . n  acting on s1 (first qubit): (n.sigma) ⊗ I
        "x": np.kron(_SX, _I2), "y": np.kron(_SY, _I2), "z": np.kron(_SZ, _I2)}
    sig2 = {"x": np.kron(_I2, _SX), "y": np.kron(_I2, _SY), "z": np.kron(_I2, _SZ)}
    s1s2 = sig1["x"] @ sig2["x"] + sig1["y"] @ sig2["y"] + sig1["z"] @ sig2["z"]

    # |³S₁,0> = Y00 |1,0>;   |³D₁,0> = sum_{ML} <2 ML 1 -ML|1 0> Y_{2,ML} |1,-ML>
    Y00 = 1.0 / math.sqrt(4.0 * np.pi)
    cg = {ML: clebsch_gordan(2, ML, 1, -ML, 1, 0) for ML in (-1, 0, 1)}

    # Gauss-Legendre in cosθ, uniform in φ.
    x, w = np.polynomial.legendre.leggauss(n_theta)      # nodes in cosθ ∈ [-1,1]
    thetas = np.arccos(x)
    phis = (np.arange(n_phi) + 0.5) * 2.0 * np.pi / n_phi
    dphi = 2.0 * np.pi / n_phi

    M = np.zeros((2, 2), dtype=complex)
    for it, th in enumerate(thetas):
        st, ct = np.sin(th), np.cos(th)
        for ph in phis:
            nx, ny, nz = st * np.cos(ph), st * np.sin(ph), ct
            S12 = 3.0 * (_sigma_dot_n_kron(nx, ny, nz)) - s1s2
            # states at this (θ,φ)
            psiS = Y00 * trip[0]
            psiD = np.zeros(4, dtype=complex)
            for ML in (-1, 0, 1):
                psiD += cg[ML] * _Y2(ML, th, ph) * trip[-ML]
            states = [psiS, psiD]
            weight = w[it] * dphi
            for a in range(2):
                for b in range(2):
                    M[a, b] += weight * np.vdot(states[a], S12 @ states[b])
    return M.real


def _sigma_dot_n_kron(nx, ny, nz):
    """(sigma1 . n)(sigma2 . n) as a 4×4 operator."""
    s1 = nx * np.kron(_SX, _I2) + ny * np.kron(_SY, _I2) + nz * np.kron(_SZ, _I2)
    s2 = nx * np.kron(_I2, _SX) + ny * np.kron(_I2, _SY) + nz * np.kron(_I2, _SZ)
    return s1 @ s2


# Analytic Rarita-Schwinger tensor matrix used by the fast solver.
S12_SS, S12_SD, S12_DD = 0.0, 2.0 * math.sqrt(2.0), -2.0


# ===========================================================================
#  OPEP radial form factors and the coupling.
# ===========================================================================
def Y_yukawa(x):
    return np.exp(-x) / x


def T_tensor(x):
    return (1.0 + 3.0 / x + 3.0 / (x * x)) * np.exp(-x) / x


def f2_over_4pi(m_pi=M_PI_DEFAULT, f_pi=F_PI_DEFAULT, g_A=G_A):
    """Pseudovector πNN coupling from Goldberger-Treiman: f_piNN = g_A m_pi/(2 f_pi)."""
    f_piNN = g_A * m_pi / (2.0 * f_pi)
    return f_piNN ** 2 / (4.0 * np.pi)


# ===========================================================================
#  Coupled-channel ³S₁–³D₁ radial solver (F74 engine, 2 channels).
# ===========================================================================
def solve_deuteron(r_c=0.50, R_max=25.0, N=900, m_pi=M_PI_DEFAULT,
                   f_pi=F_PI_DEFAULT, g_A=G_A, tensor=True, m_N=M_N, vectors=True,
                   core="hard", b=B_QUARK_DEFAULT, g_cm=GCM_DEFAULT, r_min=0.02,
                   sigma=False, sigma_g2_4pi=SIGMA_G2_4PI_BARE,
                   m_sigma=M_SIGMA_DEFAULT,
                   omega=False, omega_g2_4pi=OMEGA_G2_4PI_OBE,
                   m_omega=M_OMEGA_DEFAULT):
    """Lowest eigenstate of the coupled ³S₁–³D₁ OPEP Hamiltonian.

    core="hard"     : infinite wall at r_c (the original tuned-knob model).
    core="derived"  : the F113 short-range repulsive core V_core(r;b) added to
                      both channel diagonals — NO tuned wall (grid starts at
                      r_min); the OPEP 1/x and 1/x^3 singularities are smeared
                      by the same quark size b via f(r)=[1-exp(-(r/b)^2)]^2, so
                      one physical length b governs both the core width and the
                      vertex form factor.  This replaces the tuned r_c with the
                      derived substructure repulsion.

    tensor=False zeroes the S12 (tensor) terms -> central OPEP only.
    vectors=False uses eigvalsh (eigenvalues only) — ~2× faster for tuning.
    """
    mu = m_N / 2.0
    kin = HBARC ** 2 / (2.0 * mu)             # MeV·fm^2  (= hbar^2/2mu)
    V0 = f2_over_4pi(m_pi, f_pi, g_A) * m_pi   # MeV
    comp = HBARC / m_pi                        # pion Compton length (fm)

    r_lo = r_min if core == "derived" else r_c
    h = (R_max - r_lo) / (N + 1)
    r = r_lo + h * np.arange(1, N + 1)         # interior nodes (u=0 at both ends)
    x = r / comp

    # finite-difference -d^2/dr^2 (tridiagonal), times kin
    main = 2.0 * np.ones(N) / h ** 2
    off = -1.0 * np.ones(N - 1) / h ** 2
    D2 = (np.diag(main) + np.diag(off, 1) + np.diag(off, -1))   # = -d^2/dr^2
    K = kin * D2

    centrifugal = kin * 6.0 / r ** 2           # L(L+1)=6 for D-wave

    Y = Y_yukawa(x)
    T = T_tensor(x)
    if core == "derived":
        # vertex form factor (quark size b): kills the OPEP short-range
        # singularities so the grid can run to r_min without a hard wall.
        reg = (1.0 - np.exp(-(r / b) ** 2)) ** 2
        Y = Y * reg
        T = T * reg
        Vc = derived_core_potential(r, b=b, g_cm=g_cm)   # derived repulsive core
    else:
        Vc = np.zeros(N)

    # intermediate-range scalar-isoscalar (σ) attraction, central in both channels
    Vs = (sigma_exchange_potential(r, b=b, g2_4pi=sigma_g2_4pi, m_sigma=m_sigma)
          if sigma else np.zeros(N))
    # short-range isoscalar-vector (ω) REPULSION (F128), central in both channels
    Vw = (omega_exchange_potential(r, b=b, g2_4pi=omega_g2_4pi, m_omega=m_omega)
          if omega else np.zeros(N))
    Vs = Vs + Vw

    # OPEP potential matrix (MeV). sigma1.sigma2 = +1 (triplet).
    V_SS = -V0 * Y + Vc + Vs
    if tensor:
        V_SD = S12_SD * (-V0 * T)              # 2√2 · (tensor radial)
        V_DD = -V0 * Y + S12_DD * (-V0 * T) + Vc + Vs   # central+(-2)tensor+core+σ
    else:
        V_SD = np.zeros(N)
        V_DD = -V0 * Y + Vc + Vs               # central only in D-channel

    H = np.zeros((2 * N, 2 * N))
    H[:N, :N] = K + np.diag(V_SS)
    H[N:, N:] = K + np.diag(centrifugal + V_DD)
    H[:N, N:] = np.diag(V_SD)
    H[N:, :N] = np.diag(V_SD)

    if vectors:
        evals, evecs = np.linalg.eigh(H)
        v0 = evecs[:, 0]
        u, w = v0[:N], v0[N:]
        nrm = np.sum(u ** 2 + w ** 2)
        P_D = float(np.sum(w ** 2) / nrm)
        rms_rel = float(math.sqrt(np.sum((u ** 2 + w ** 2) * r ** 2) / nrm))
    else:
        evals = np.linalg.eigvalsh(H)
        u = w = None
        P_D = float("nan")
        rms_rel = float("nan")
    E0 = float(evals[0])
    E1 = float(evals[1])
    E_b = -E0 if E0 < 0 else 0.0
    kappa = math.sqrt(2.0 * mu * E_b) / HBARC if E_b > 0 else 0.0   # 1/fm

    return {
        "E": E0, "E1": E1, "E_b": E_b, "bound": E0 < 0.0,
        "P_D": P_D, "kappa": kappa, "V0": V0, "comp": comp,
        "r": r, "u": u, "w": w, "h": h, "r_c": r_c, "N": N,
        "core": core, "b": b, "Vcore0": float(derived_core_potential(0.0, b, g_cm)),
        "rms_rel": rms_rel, "r_d": rms_rel / 2.0,   # deuteron radius = rms_rel/2
        "sigma": sigma, "sigma_g2_4pi": sigma_g2_4pi if sigma else 0.0,
        "omega": omega, "omega_g2_4pi": omega_g2_4pi if omega else 0.0,
        "f2_4pi": f2_over_4pi(m_pi, f_pi, g_A),
    }


def tune_sigma_to_binding(b=B_QUARK_DEFAULT, target_Eb=2.224, lo=2.5, hi=5.0, **kw):
    """At a FIXED (physical) quark size b, bisect the σ coupling g²/4π to hit the
    target binding energy with the F113 derived core + OPEP + σ attraction.
    Returns (g²/4π, result).  E_b grows with the σ coupling."""
    def Eb(g2):
        return solve_deuteron(core="derived", b=b, sigma=True, sigma_g2_4pi=g2,
                              vectors=False, **kw)["E_b"]
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if Eb(mid) > target_Eb:
            hi = mid       # too deep -> weaken σ
        else:
            lo = mid
    g2 = 0.5 * (lo + hi)
    return g2, solve_deuteron(core="derived", b=b, sigma=True, sigma_g2_4pi=g2, **kw)


def tune_b_to_binding(target_Eb=2.224, lo=0.30, hi=1.10, **kw):
    """Bisection on the quark size b (the derived-core width) to hit a target
    binding energy, replacing tune_core_to_binding's tuned hard wall.  E_b grows
    as b shrinks (narrower core -> more attractive volume).  Returns (b, result).
    """
    def Eb(bb):
        return solve_deuteron(core="derived", b=bb, vectors=False, **kw)["E_b"]
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if Eb(mid) > target_Eb:
            lo = mid       # too deep -> widen the core
        else:
            hi = mid
    bb = 0.5 * (lo + hi)
    return bb, solve_deuteron(core="derived", b=bb, **kw)


def tune_core_to_binding(target_Eb=2.224, lo=0.2, hi=1.2, **kw):
    """Bisection on the hard-core radius r_c to hit a target binding energy.
    E_b decreases as r_c grows (less attractive volume). Returns (r_c, result)."""
    def Eb(rc):
        return solve_deuteron(r_c=rc, vectors=False, **kw)["E_b"]
    # ensure bracket: small r_c -> deeper (E_b larger); large r_c -> shallower
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if Eb(mid) > target_Eb:
            lo = mid      # too deep -> increase r_c
        else:
            hi = mid
    rc = 0.5 * (lo + hi)
    return rc, solve_deuteron(r_c=rc, **kw)   # final solve WITH vectors (P_D, ψ)


if __name__ == "__main__":
    print("Tensor spin-angular matrix <S12> by CG construction:")
    Mt = tensor_matrix_via_construction()
    print(np.array2string(Mt, precision=6, suppress_small=True))
    print(f"  target [[0, 2√2],[2√2,-2]] = [[0, {2*math.sqrt(2):.6f}],[..,-2]]\n")

    rc, d = tune_core_to_binding()
    print(f"Deuteron (full ³S₁–³D₁ OPEP, TUNED hard wall r_c = {rc:.4f} fm):")
    print(f"  E_b   = {d['E_b']:.4f} MeV   (target 2.224)")
    print(f"  P_D   = {100*d['P_D']:.2f} %   (D-state admixture)")
    print(f"  kappa = {d['kappa']:.4f} /fm")
    dc = solve_deuteron(r_c=rc, tensor=False)
    print(f"  central-only at same r_c: bound={dc['bound']}  (tensor essential)")

    print(f"\nDeuteron with the DERIVED F113 core (no hard wall), tuning quark size b:")
    bD, dD = tune_b_to_binding()
    print(f"  b        = {bD:.4f} fm   (the one physical knob; was the ad-hoc r_c)")
    print(f"  V_core(0)= {dD['Vcore0']:.1f} MeV   (DERIVED: 56/3·g_cm, exact)")
    print(f"  E_b      = {dD['E_b']:.4f} MeV   (target 2.224)")
    print(f"  P_D      = {100*dD['P_D']:.2f} %")
    print(f"  kappa    = {dD['kappa']:.4f} /fm   (phys 0.2316)")
    dDc = solve_deuteron(core="derived", b=bD, tensor=False)
    print(f"  central-only at same b: bound={dDc['bound']}  (tensor still essential)")
