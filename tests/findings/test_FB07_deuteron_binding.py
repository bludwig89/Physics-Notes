#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_FB07_deuteron_binding.py
=============================

FB07 — Deuteron: the first nucleus binds via the pion tensor force.

Self-contained execution of falsification test FB07
(tests/falsification/FB07-deuteron-binding.md).  Builds and solves the coupled
3S1-3D1 deuteron bound-state problem with:

  * one-pion-exchange (OPEP) central + TENSOR force        (F103/F104)
  * scalar-isoscalar (sigma) intermediate attraction       (F126; g^2/4pi=8.18,
                                                             m_sigma = 2 m_c)
  * isoscalar-vector (omega) short-range repulsion          (optional, F128)
  * the F113 quark-Pauli + chromomagnetic repulsive core   (+341.8 MeV, derived)

Inputs (honest accounting):
  m_pi, f_pi  -> model (P3/F103/F77)
  g_A = 1.272 -> external, via Goldberger-Treiman for f_piNN = g_A m_pi/(2 f_pi)
  M_N         -> external (P6)
The one TUNED knob is a single short-range core radius (the quark size b that
sets the F113 core width and the OPEP vertex cutoff).

CONSTRAINTS (CLAUDE.md): all arithmetic is REAL; the dense scipy/numpy eigensolve
is CROSS-CHECKED against a hand-rolled inverse-iteration on the same real
symmetric Hamiltonian so we know exactly what the eigensolver returns.

Checks
------
  A  tensor spin-angular matrix from Clebsch-Gordan == Rarita-Schwinger
     [[0, 2 sqrt2], [2 sqrt2, -2]]   to ~1e-14
  B  coupled-channel bound state is a single J^P=1+ I=0 state;
     TENSOR-ESSENTIAL: central-only OPEP at the same core is UNBOUND
  C  D-state P_D few-% (4-7); 3S1 tail slope matches kappa=sqrt(M_N E_b)/hbarc
     to ~<1%; tuning the one core radius lands E_b=2.224 MeV at physical
     kappa = 0.2316 fm^-1.

Writes test-results/FB07_deuteron_binding.json.

Run:  python3 tests/findings/test_FB07_deuteron_binding.py
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

# --------------------------------------------------------------------------
#  Physical constants / inputs
# --------------------------------------------------------------------------
HBARC = 197.32698        # MeV.fm
M_N = 938.918            # MeV   isospin-averaged nucleon mass  -- EXTERNAL (P6)
G_A = 1.272              # axial charge                          -- EXTERNAL (GT)
M_PI = 138.039           # MeV   isospin-averaged pion mass       -- model (P3)
F_PI = 92.07             # MeV   pion decay constant              -- model (P3/F77)
M_C = 311.2              # MeV   constituent quark mass           -- model (F77)
M_SIGMA = 2.0 * M_C      # MeV   scalar pole at 2 m_c             -- model (F103)
# sigma-NN coupling: each constituent quark couples g_sq = m_c/f_pi, charge adds
# coherently over 3 quarks => g_sNN^2/4pi = 9 (m_c/f_pi)^2 / 4pi  (F126)
SIGMA_G2_4PI = 9.0 * (M_C / F_PI) ** 2 / (4.0 * math.pi)          # 8.18
M_OMEGA = 782.66         # MeV   isoscalar-vector pole (= m_rho up to OZI)  (F128)

# F113 derived core: chromomagnetic energy of the antisymmetrised 6q two-cluster
# state, a closed-form rational function of u = exp(-r^2/4b^2).  Coefficients are
# EXACT (sum over the 720 six-quark permutations of the F71 colour-singlet x
# SU(6) deuteron-channel state).  N0/D0 = -16 = 2 E_N (two free nucleons);
# sum N / sum D = 8/3 ([6] full overlap)  => V_core(0) = (8/3 + 16) g_cm = 56/3 g_cm.
GCM = 18.31              # MeV   colour-magnetic coupling from N-Delta = 293
_CORE_N = (-13436928.0, 15925248.0, 15925248.0, -13436928.0)
_CORE_D = (839808.0, 93312.0, 93312.0, 839808.0)
_CORE_2EN = -16.0        # two free nucleons, in units of g_cm


# ==========================================================================
#  Check A -- Clebsch-Gordan and the tensor spin-angular matrix <S12>.
# ==========================================================================
def clebsch_gordan(j1, m1, j2, m2, J, M):
    """<j1 m1 j2 m2 | J M> via the Racah closed form (exact, rational under the
    factorials).  Hand-rolled -- no scipy -- per the chiral/real-arithmetic
    constraint in CLAUDE.md."""
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


_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)
_I2 = np.eye(2, dtype=complex)


def _two_nucleon_triplet_basis():
    """|1,+1>, |1,0>, |1,-1> as 4-vectors in |s1 s2> = {uu, ud, du, dd}."""
    uu = np.array([1, 0, 0, 0], dtype=complex)
    ud = np.array([0, 1, 0, 0], dtype=complex)
    du = np.array([0, 0, 1, 0], dtype=complex)
    dd = np.array([0, 0, 0, 1], dtype=complex)
    return {1: uu, 0: (ud + du) / np.sqrt(2.0), -1: dd}


def _Y2(M, theta, phi):
    """Y_{2,M} for M in {-1,0,1} (the only ones reached at total M=0)."""
    st, ct = np.sin(theta), np.cos(theta)
    if M == 0:
        return math.sqrt(5.0 / (16.0 * np.pi)) * (3.0 * ct * ct - 1.0)
    if M == 1:
        return -math.sqrt(15.0 / (8.0 * np.pi)) * st * ct * np.exp(1j * phi)
    if M == -1:
        return math.sqrt(15.0 / (8.0 * np.pi)) * st * ct * np.exp(-1j * phi)
    raise ValueError(M)


def _sigma1n_sigma2n(nx, ny, nz):
    """(sigma1 . n)(sigma2 . n) as a 4x4 operator on |s1 s2>."""
    s1 = nx * np.kron(_SX, _I2) + ny * np.kron(_SY, _I2) + nz * np.kron(_SZ, _I2)
    s2 = nx * np.kron(_I2, _SX) + ny * np.kron(_I2, _SY) + nz * np.kron(_I2, _SZ)
    return s1 @ s2


def tensor_matrix_via_construction(n_theta=48, n_phi=48):
    """Build <3L'1 | S12 | 3L1> for L,L' in {0,2} at J=1, M=0 by explicit
    spinor-spherical-harmonic quadrature over the unit sphere.  Returns the 2x2
    matrix in basis (S=L0, D=L2).  Should equal [[0, 2sqrt2],[2sqrt2,-2]]."""
    trip = _two_nucleon_triplet_basis()
    sig1 = {"x": np.kron(_SX, _I2), "y": np.kron(_SY, _I2), "z": np.kron(_SZ, _I2)}
    sig2 = {"x": np.kron(_I2, _SX), "y": np.kron(_I2, _SY), "z": np.kron(_I2, _SZ)}
    s1s2 = sig1["x"] @ sig2["x"] + sig1["y"] @ sig2["y"] + sig1["z"] @ sig2["z"]

    Y00 = 1.0 / math.sqrt(4.0 * np.pi)
    cg = {ML: clebsch_gordan(2, ML, 1, -ML, 1, 0) for ML in (-1, 0, 1)}

    x, w = np.polynomial.legendre.leggauss(n_theta)   # nodes in cos(theta)
    thetas = np.arccos(x)
    phis = (np.arange(n_phi) + 0.5) * 2.0 * np.pi / n_phi
    dphi = 2.0 * np.pi / n_phi

    M = np.zeros((2, 2), dtype=complex)
    for it, th in enumerate(thetas):
        st, ct = np.sin(th), np.cos(th)
        for ph in phis:
            nx, ny, nz = st * np.cos(ph), st * np.sin(ph), ct
            S12 = 3.0 * _sigma1n_sigma2n(nx, ny, nz) - s1s2
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


# Analytic Rarita-Schwinger tensor matrix used by the radial solver.
S12_SD = 2.0 * math.sqrt(2.0)
S12_DD = -2.0


# ==========================================================================
#  Radial potentials
# ==========================================================================
def Y_yukawa(x):
    return np.exp(-x) / x


def T_tensor(x):
    return (1.0 + 3.0 / x + 3.0 / (x * x)) * np.exp(-x) / x


def f2_over_4pi(m_pi=M_PI, f_pi=F_PI, g_A=G_A):
    """Pseudovector piNN coupling via Goldberger-Treiman: f_piNN = g_A m_pi/(2 f_pi)."""
    f_piNN = g_A * m_pi / (2.0 * f_pi)
    return f_piNN ** 2 / (4.0 * np.pi)


def derived_core_potential(r, b, g_cm=GCM):
    """F113 short-range repulsive core in MeV.  Positive, 56/3 g_cm at r=0, ->0."""
    u = np.exp(-(np.asarray(r, dtype=float) ** 2) / (4.0 * b * b))
    num = _CORE_N[0] + u * (_CORE_N[1] + u * (_CORE_N[2] + u * _CORE_N[3]))
    den = _CORE_D[0] + u * (_CORE_D[1] + u * (_CORE_D[2] + u * _CORE_D[3]))
    return g_cm * (num / den - _CORE_2EN)


def folded_yukawa(r, m, beta):
    """Scalar Yukawa e^{-mr}/r folded over a Gaussian vertex of width beta (fm).
    Finite at r->0.  m in MeV, r in fm.  Real arithmetic via math.erfc."""
    r = np.asarray(r, dtype=float)
    a = m / HBARC                                   # 1/fm
    pre = math.exp((a * beta) ** 2)
    erfc = np.vectorize(math.erfc)
    t1 = np.exp(-a * r) * erfc(a * beta - r / (2.0 * beta))
    t2 = np.exp(a * r) * erfc(a * beta + r / (2.0 * beta))
    return pre * (t1 - t2) / (2.0 * r)


def sigma_exchange_potential(r, b, g2_4pi=SIGMA_G2_4PI, m_sigma=M_SIGMA):
    """Intermediate-range scalar-isoscalar (sigma) attraction (MeV).  Negative."""
    return -g2_4pi * m_sigma * folded_yukawa(r, m_sigma, b)


def omega_exchange_potential(r, b, g2_4pi, m_omega=M_OMEGA):
    """Short-range isoscalar-vector (omega) repulsion (MeV).  Positive."""
    return +g2_4pi * m_omega * folded_yukawa(r, m_omega, b)


# ==========================================================================
#  Coupled-channel 3S1-3D1 radial Hamiltonian + bound-state solve.
# ==========================================================================
def build_H(b, m_pi=M_PI, f_pi=F_PI, g_A=G_A, m_N=M_N, tensor=True,
            sigma=True, sigma_g2_4pi=SIGMA_G2_4PI, m_sigma=M_SIGMA,
            omega=False, omega_g2_4pi=0.0, m_omega=M_OMEGA,
            R_max=25.0, N=900, r_min=0.02):
    """Assemble the real symmetric 2N x 2N coupled-channel Hamiltonian and the
    radial grid.  Returns (H, r, kin, mu)."""
    mu = m_N / 2.0
    kin = HBARC ** 2 / (2.0 * mu)             # MeV.fm^2
    V0 = f2_over_4pi(m_pi, f_pi, g_A) * m_pi   # MeV
    comp = HBARC / m_pi                        # pion Compton length (fm)

    h = (R_max - r_min) / (N + 1)
    r = r_min + h * np.arange(1, N + 1)        # interior nodes (u=0 both ends)
    x = r / comp

    # -d^2/dr^2 tridiagonal, times kin
    main = 2.0 * np.ones(N) / h ** 2
    off = -1.0 * np.ones(N - 1) / h ** 2
    D2 = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    K = kin * D2
    centrifugal = kin * 6.0 / r ** 2           # L(L+1)=6 for the D-wave

    # vertex form factor (quark size b): smear the OPEP 1/x, 1/x^3 singularities
    reg = (1.0 - np.exp(-(r / b) ** 2)) ** 2
    Y = Y_yukawa(x) * reg
    T = T_tensor(x) * reg

    Vc = derived_core_potential(r, b)          # F113 repulsive core
    Vs = sigma_exchange_potential(r, b, sigma_g2_4pi, m_sigma) if sigma else 0.0 * r
    Vw = omega_exchange_potential(r, b, omega_g2_4pi, m_omega) if omega else 0.0 * r
    Vcentral_extra = Vc + Vs + Vw              # added to both channel diagonals

    V_SS = -V0 * Y + Vcentral_extra
    if tensor:
        V_SD = S12_SD * (-V0 * T)
        V_DD = -V0 * Y + S12_DD * (-V0 * T) + Vcentral_extra
    else:
        V_SD = np.zeros(N)
        V_DD = -V0 * Y + Vcentral_extra

    H = np.zeros((2 * N, 2 * N))
    H[:N, :N] = K + np.diag(V_SS)
    H[N:, N:] = K + np.diag(centrifugal + V_DD)
    H[:N, N:] = np.diag(V_SD)
    H[N:, :N] = np.diag(V_SD)
    return H, r, kin, mu


def lowest_two_eig_dense(H):
    """numpy dense symmetric eigensolve -- lowest two eigenpairs."""
    evals, evecs = np.linalg.eigh(H)
    return evals[0], evals[1], evecs[:, 0]


def lowest_eig_inverse_iteration(H, sigma_shift, n_iter=200, tol=1e-12):
    """Hand-rolled shifted inverse iteration for the eigenpair nearest sigma_shift.
    Cross-checks the dense eigensolve (CLAUDE.md: verify scipy/numpy eigensolves).
    Pure real arithmetic, LU solve of (H - sigma I)."""
    n = H.shape[0]
    A = H - sigma_shift * np.eye(n)
    # LU factorisation once
    import numpy.linalg as la
    rng = np.random.default_rng(0)
    v = rng.standard_normal(n)
    v /= np.linalg.norm(v)
    lam_old = 0.0
    for _ in range(n_iter):
        w = la.solve(A, v)
        w /= np.linalg.norm(w)
        lam = float(w @ (H @ w))
        v = w
        if abs(lam - lam_old) < tol:
            break
        lam_old = lam
    return lam, v


def solve(b, **kw):
    """Solve the coupled-channel deuteron at quark size b; return a dict of
    observables.  Uses the dense eigensolve, verified against inverse iteration
    for the lowest state."""
    tensor = kw.pop("tensor", True)
    H, r, kin, mu = build_H(b, tensor=tensor, **kw)
    N = len(r)
    E0, E1, v0 = lowest_two_eig_dense(H)

    u, w = v0[:N], v0[N:]
    nrm = np.sum(u ** 2 + w ** 2)
    P_D = float(np.sum(w ** 2) / nrm)
    rms_rel = float(math.sqrt(np.sum((u ** 2 + w ** 2) * r ** 2) / nrm))

    E_b = -E0 if E0 < 0 else 0.0
    kappa = math.sqrt(2.0 * mu * E_b) / HBARC if E_b > 0 else 0.0

    return {"E0": float(E0), "E1": float(E1), "E_b": E_b, "bound": E0 < 0.0,
            "P_D": P_D, "kappa": kappa, "rms_rel": rms_rel, "r_d": rms_rel / 2.0,
            "r": r, "u": u, "w": w, "H": H}


def tune_b(target_Eb=2.224, lo=0.30, hi=1.10, **kw):
    """Bisect the single short-range knob b to hit target_Eb.  E_b grows as b
    shrinks (narrower core -> more attractive volume)."""
    def Eb(bb):
        H, r, kin, mu = build_H(bb, **kw)
        ev = np.linalg.eigvalsh(H)
        return -ev[0] if ev[0] < 0 else 0.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if Eb(mid) > target_Eb:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ==========================================================================
#  Driver
# ==========================================================================
def main():
    results = {}
    checks = []

    # ---- Check A: tensor spin-angular matrix == Rarita-Schwinger -----------
    Mt = tensor_matrix_via_construction()
    RS = np.array([[0.0, 2.0 * math.sqrt(2.0)],
                   [2.0 * math.sqrt(2.0), -2.0]])
    res_A = float(np.max(np.abs(Mt - RS)))
    passA = res_A < 1e-13
    checks.append(("A tensor matrix == [[0,2sqrt2],[2sqrt2,-2]]", passA, f"{res_A:.2e}"))
    results["tensor_matrix"] = Mt.tolist()
    results["tensor_residual_vs_RS"] = res_A

    # ---- Check G/C: tune the ONE short-range core radius b -----------------
    # Force: F113 derived core + OPEP (central+tensor) + bare sigma (g^2/4pi=8.18).
    b_tuned = tune_b(target_Eb=2.224, sigma=True, sigma_g2_4pi=SIGMA_G2_4PI,
                     omega=False)
    d = solve(b_tuned, sigma=True, sigma_g2_4pi=SIGMA_G2_4PI, omega=False)
    E_b, kappa, P_D, r_d, E1 = d["E_b"], d["kappa"], d["P_D"], d["r_d"], d["E1"]

    # Verify the dense lowest eigenvalue with hand-rolled inverse iteration.
    lam_inv, _ = lowest_eig_inverse_iteration(d["H"], sigma_shift=d["E0"] - 1.0)
    eig_xcheck = abs(lam_inv - d["E0"])
    passXcheck = eig_xcheck < 1e-6
    checks.append(("eigensolve cross-check (dense vs inverse-iter)",
                   passXcheck, f"{eig_xcheck:.2e} MeV"))

    passEb = abs(E_b - 2.224) < 5e-3
    kappa_phys = 0.2316
    passKappa = abs(kappa - kappa_phys) < 1e-3
    checks.append(("E_b tunable to 2.224 MeV", passEb, f"{E_b:.5f} MeV"))
    checks.append(("kappa = physical 0.2316 fm^-1", passKappa, f"{kappa:.5f} fm^-1"))

    # kappa from sqrt(M_N E_b)/hbarc cross-check (=sqrt(2 mu E_b)/hbarc, mu=M_N/2)
    kappa_form = math.sqrt(M_N * E_b) / HBARC
    results["kappa_form_MNEb"] = kappa_form

    # ---- Check F: 3S1 tail slope vs kappa ----------------------------------
    r, u = d["r"], d["u"]
    mask = (r > 8.0) & (r < 16.0) & (np.abs(u) > 0)
    slope = np.polyfit(r[mask], np.log(np.abs(u[mask])), 1)[0]
    kappa_tail = -slope
    tail_dev_pct = 100.0 * abs(kappa_tail - kappa_form) / kappa_form
    passTail = tail_dev_pct < 1.0
    checks.append(("3S1 tail slope vs kappa < 1%", passTail, f"{tail_dev_pct:.3f}%"))

    # ---- Check E/C: D-state few-% ------------------------------------------
    passPD = 0.04 <= P_D <= 0.075
    checks.append(("D-state P_D in 4-7%", passPD, f"{100*P_D:.2f}%"))

    # ---- Check D: single bound state (E1 >= 0), J^P = 1+ I=0 ---------------
    single_bound = (d["E0"] < 0.0) and (E1 >= 0.0)
    checks.append(("single bound state (E1 >= 0)", single_bound,
                   f"E0={d['E0']:.4f}, E1={E1:.4f}"))
    # J^P = 1+: both coupled waves L=0,2 have parity (-1)^L = +1, spin triplet S=1
    # -> J=1, positive parity, isospin I=0 (T=0 channel) -- by construction.
    JP_ok = True
    checks.append(("J^P = 1+, I=0 by construction", JP_ok, "L in {0,2}, S=1, T=0"))

    # ---- Check B: TENSOR-ESSENTIAL (central-only OPEP unbound at same b) ----
    dc = solve(b_tuned, tensor=False, sigma=True, sigma_g2_4pi=SIGMA_G2_4PI,
               omega=False)
    central_unbound = not dc["bound"]
    checks.append(("TENSOR-ESSENTIAL: central-only UNBOUND at same core",
                   central_unbound, f"central E0={dc['E0']:.4f} (bound={dc['bound']})"))

    # ---- Record numbers ----------------------------------------------------
    results.update({
        "b_tuned_fm": b_tuned,
        "E_b_MeV": E_b,
        "kappa_fm^-1": kappa,
        "kappa_phys": kappa_phys,
        "kappa_tail_fm^-1": float(kappa_tail),
        "tail_slope_dev_pct": tail_dev_pct,
        "P_D": P_D,
        "P_D_pct": 100.0 * P_D,
        "r_d_fm": r_d,
        "E1_MeV": E1,
        "central_only_E0_MeV": dc["E0"],
        "central_only_bound": dc["bound"],
        "f2_4pi": f2_over_4pi(),
        "sigma_g2_4pi": SIGMA_G2_4PI,
        "m_sigma_MeV": M_SIGMA,
        "core_height_MeV": float(derived_core_potential(0.0, b_tuned)),
        "eig_xcheck_MeV": eig_xcheck,
    })

    all_pass = all(p for _, p, _ in checks)
    # Gate: PASS if binds only with tensor (central-only unbound); single 1+ I=0;
    #       E_b tunable to 2.224 at physical kappa; D-state few-%.
    gate_pass = (central_unbound and single_bound and JP_ok and passEb
                 and passKappa and passPD and passTail and passA)
    verdict = "PASS" if gate_pass else "FALSIFIED"

    # ---- Print summary -----------------------------------------------------
    print("=" * 72)
    print("FB07 -- Deuteron binding via the pion tensor force")
    print("=" * 72)
    for name, p, detail in checks:
        print(f"  [{'PASS' if p else 'FAIL'}] {name}: {detail}")
    print("-" * 72)
    print(f"  b (tuned quark size)     = {b_tuned:.4f} fm")
    print(f"  E_b                      = {E_b:.5f} MeV   (target 2.22457)")
    print(f"  kappa (sqrt(2mu Eb)/hc)  = {kappa:.5f} fm^-1 (phys 0.2316)")
    print(f"  kappa (tail slope)       = {kappa_tail:.5f} fm^-1 ({tail_dev_pct:.3f}%)")
    print(f"  P_D                      = {100*P_D:.2f} %   (phys 4-6)")
    print(f"  r_d                      = {r_d:.3f} fm    (phys 1.97)")
    print(f"  E1 (next state)          = {E1:.4f} MeV (>=0 => single bound)")
    print(f"  central-only E0          = {dc['E0']:.4f} MeV (unbound={central_unbound})")
    print(f"  tensor residual vs RS    = {res_A:.2e}")
    print(f"  eigensolve cross-check   = {eig_xcheck:.2e} MeV")
    print("-" * 72)
    print(f"  GATE VERDICT: {verdict}")
    print("=" * 72)

    # ---- Write JSON --------------------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.normpath(os.path.join(here, "..", "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "FB07_deuteron_binding.json")

    payload = {
        "test_id": "FB07",
        "name": "Deuteron: the first nucleus binds via the pion tensor force",
        "verdict": verdict,
        "predicted": {
            "mechanism": "coupled 3S1-3D1 bound state; binds ONLY via OPEP tensor",
            "E_b_MeV": round(E_b, 5),
            "kappa_fm^-1": round(kappa, 5),
            "P_D_pct": round(100 * P_D, 3),
            "r_d_fm": round(r_d, 3),
            "J^P": "1+",
            "I": 0,
            "tensor_essential": True,
            "central_only_bound": dc["bound"],
        },
        "measured_target": {
            "E_b_MeV": 2.22457,
            "J^P": "1+",
            "I": 0,
            "r_d_fm": 1.97,
            "P_D_pct": "4-6",
            "kappa_fm^-1": 0.2316,
        },
        "gate": {
            "criteria": [
                "binds ONLY with tensor (central-only OPEP unbound at same core)",
                "single J^P=1+ I=0 bound state",
                "E_b tunable to 2.224 MeV at physical kappa=0.2316 fm^-1",
                "D-state few-% (4-7)",
                "3S1 tail slope matches kappa to <1%",
                "tensor spin-angular matrix == Rarita-Schwinger to ~1e-14",
            ],
            "all_checks_pass": bool(all_pass),
        },
        "computed": {k: (v if not isinstance(v, np.ndarray) else v.tolist())
                     for k, v in results.items()},
        "checks": [{"name": n, "pass": bool(p), "detail": dstr}
                   for n, p, dstr in checks],
        "inputs": {
            "m_pi_MeV": M_PI, "f_pi_MeV": F_PI, "M_N_MeV": M_N, "g_A": G_A,
            "m_c_MeV": M_C, "m_sigma_MeV": M_SIGMA,
            "sigma_g2_4pi": round(SIGMA_G2_4PI, 4),
            "f2_4pi_OPEP": round(f2_over_4pi(), 5),
            "core_height_MeV": round(float(derived_core_potential(0.0, b_tuned)), 1),
            "g_cm_MeV": GCM, "tuned_knob": "b (quark size / core radius)",
        },
        "commands": [
            "python3 tests/findings/test_FB07_deuteron_binding.py",
        ],
        "timestamp": "2026-06-16",
    }
    with open(out_path, "w") as fh:
        json.dump(payload, fh, indent=2)
    print(f"Wrote {out_path}")

    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
