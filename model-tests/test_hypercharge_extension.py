"""
test_hypercharge_extension.py — F42 extension of F41:
    (a) quark-sector mass step Y-coupling
    (b) right-handed singlets (e_R, u_R, d_R) promoted to *dynamical*
        U(1)_Y-coupled fields in the kinetic step.
2026-05-27 - 09:00

Run from project root:
    python model-tests/test_hypercharge_extension.py

Writes JSON to test-results/hypercharge_extension.json.

Tests
-----
Y8   U(1)_Y Ward identity, quark mass step alone, d-branch (Higgs).
Y9   U(1)_Y Ward identity, quark mass step alone, u-branch (conjugate-Higgs).
Y10  α(x) ≡ 0 → bit-for-bit equal to ca_dirac.mass_step_doublet_su2.
Y11  SU(2)_L Ward identity preserved with nontrivial α(x) — quark side.
Y12  Quark mass step unitarity over 50 random (U, α) steps.
Y13  χ kinetic step gauge covariance:  S[α+β](e^{iβY/2}χ) = e^{iβY/2} S[α](χ)
     for each of e_R (Y=-2), u_R (Y=+4/3), d_R (Y=-2/3).
Y14  α(x) ≡ 0 → χ kinetic step is bit-for-bit equal to the bare
     ca_dirac._weyl_half_step_2c (regression guarantee).
Y15  Gell-Mann–Nishijima algebra on the quark side
     (ΔY_u = −1, ΔY_d = +1, Q(u_L)=2/3, Q(d_L)=−1/3, Q(u_R)=2/3, Q(d_R)=−1/3).
"""

from __future__ import annotations
import json
import os
import sys
import time
import numpy as np


# ── Path bootstrap ────────────────────────────────────────────────────
_THIS = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_THIS, '..'))
sys.path.insert(0, os.path.join(_ROOT, 'ca-simulation'))

from ca_dirac import (
    mass_step_doublet_su2,
    make_su2_field,
    _weyl_half_step_2c,
)
import ca_hypercharge as hyf


# ── Helpers ───────────────────────────────────────────────────────────
def random_8_spinors(Lx, Ly, seed):
    rng = np.random.default_rng(seed=seed)
    def cmplx():
        return rng.standard_normal((Lx, Ly)) + 1j * rng.standard_normal((Lx, Ly))
    return [cmplx() for _ in range(8)]


def random_2_spinors(Lx, Ly, seed):
    rng = np.random.default_rng(seed=seed)
    def cmplx():
        return rng.standard_normal((Lx, Ly)) + 1j * rng.standard_normal((Lx, Ly))
    return cmplx(), cmplx()


def tuple_max_abs_diff(a, b):
    return float(max(np.max(np.abs(ai - bi)) for ai, bi in zip(a, b)))


def tuple_norm(t):
    return float(sum(np.sum(np.abs(x)**2) for x in t))


# ── Y8 — Quark U(1)_Y Ward identity, d-branch ────────────────────────
def test_Y8_u1y_ward_d_branch(L=24, m=0.3, seed=801):
    """
    d-branch Ward identity.  Silence u-branch by zeroing χ_u and using
    the SM Y_u_R = +4/3 ≠ 0 — but to isolate d-branch we instead set
    Y_u_R = 0 effectively by silencing χ_u; the η-doublet shares
    Y_QUARK_L so we can apply the full quark V_Y on both isospin states.

    LHS:  V_Y · M_quark(ψ; U, α=0)
    RHS:  M_quark(V_Y · ψ; U, α = β)
    """
    a, b = make_su2_field(L, L, mode='random')
    rng_beta = np.random.default_rng(seed)
    beta = rng_beta.uniform(-1.0, 1.0, (L, L))

    psi = random_8_spinors(L, L, seed)
    eta_u_u, eta_u_d, eta_d_u, eta_d_d, _0, _1, chi_d_u, chi_d_d = psi
    # silence u-branch χ
    chi_u_u = np.zeros((L, L), dtype=complex)
    chi_u_d = np.zeros((L, L), dtype=complex)

    psi8 = (eta_u_u, eta_u_d, eta_d_u, eta_d_d,
            chi_u_u, chi_u_d, chi_d_u, chi_d_d)

    # LHS: mass(ψ; U, α=0) then V_Y
    out_pre = hyf.mass_step_quark_doublet_su2xu1y(
        *psi8, a, b, np.zeros_like(beta), m=m)
    LHS = hyf.apply_u1y_transform_quark(*out_pre, beta)

    # RHS: V_Y on ψ then mass(ψ'; U, α=β)
    psi_p = hyf.apply_u1y_transform_quark(*psi8, beta)
    RHS = hyf.mass_step_quark_doublet_su2xu1y(*psi_p, a, b, beta, m=m)

    return tuple_max_abs_diff(LHS, RHS)


# ── Y9 — Quark U(1)_Y Ward identity, u-branch ────────────────────────
def test_Y9_u1y_ward_u_branch(L=24, m=0.3, seed=902):
    """u-branch Ward identity; silence d-branch by zeroing χ_d."""
    a, b = make_su2_field(L, L, mode='random')
    rng_beta = np.random.default_rng(seed)
    beta = rng_beta.uniform(-1.0, 1.0, (L, L))

    psi = random_8_spinors(L, L, seed)
    eta_u_u, eta_u_d, eta_d_u, eta_d_d, chi_u_u, chi_u_d, _2, _3 = psi
    chi_d_u = np.zeros((L, L), dtype=complex)
    chi_d_d = np.zeros((L, L), dtype=complex)

    psi8 = (eta_u_u, eta_u_d, eta_d_u, eta_d_d,
            chi_u_u, chi_u_d, chi_d_u, chi_d_d)

    out_pre = hyf.mass_step_quark_doublet_su2xu1y(
        *psi8, a, b, np.zeros_like(beta), m=m)
    LHS = hyf.apply_u1y_transform_quark(*out_pre, beta)

    psi_p = hyf.apply_u1y_transform_quark(*psi8, beta)
    RHS = hyf.mass_step_quark_doublet_su2xu1y(*psi_p, a, b, beta, m=m)
    return tuple_max_abs_diff(LHS, RHS)


# ── Y10 — α≡0 reduces to F40/ca_dirac mass step bit-for-bit ──────────
def test_Y10_reduction_to_F40(L=24, m=0.3, seed=1003):
    """
    α(x) ≡ 0 → identical to ca_dirac.mass_step_doublet_su2 (the same
    primitive that F40's quark_doublet_mass_step_su2 wraps).  Bit-for-bit.
    """
    a, b = make_su2_field(L, L, mode='random')
    psi = random_8_spinors(L, L, seed)
    alpha = np.zeros((L, L))

    out_hyf = hyf.mass_step_quark_doublet_su2xu1y(*psi, a, b, alpha, m=m)
    out_f27 = mass_step_doublet_su2(*psi, a, b, m=m)
    return tuple_max_abs_diff(out_hyf, out_f27)


# ── Y11 — SU(2)_L Ward identity preserved with nontrivial α(x) ───────
def test_Y11_su2_ward_quark_with_y_field(L=24, m=0.3, seed=1104):
    """
    F27 SU(2)_L Ward identity with α(x) ≠ 0 — quark side:
        V_L · M_quark(ψ; U, α)  ==  M_quark(V_L·ψ; V·U, α)
    """
    a, b = make_su2_field(L, L, mode='random')
    va, vb = make_su2_field(L, L, mode='random')
    rng_alpha = np.random.default_rng(seed)
    alpha = rng_alpha.uniform(-1.0, 1.0, (L, L))
    psi = random_8_spinors(L, L, seed + 1)
    eta_u_u, eta_u_d, eta_d_u, eta_d_d, \
        chi_u_u, chi_u_d, chi_d_u, chi_d_d = psi

    def apply_V_L_on_eta(eu_u_u, eu_u_d, eu_d_u, eu_d_d):
        Vac, Vbc = np.conj(va), np.conj(vb)
        u_u = va * eu_u_u - Vbc * eu_d_u
        u_d = va * eu_u_d - Vbc * eu_d_d
        d_u = vb * eu_u_u + Vac * eu_d_u
        d_d = vb * eu_u_d + Vac * eu_d_d
        return u_u, u_d, d_u, d_d

    def su2_product_VU(va_, vb_, ua_, ub_):
        a_out = va_ * ua_ - np.conj(vb_) * ub_
        b_out = vb_ * ua_ + np.conj(va_) * ub_
        return a_out, b_out

    out_pre = hyf.mass_step_quark_doublet_su2xu1y(*psi, a, b, alpha, m=m)
    (eu_u_n, ed_u_n, eu_d_n, ed_d_n,
     xu_u_n, xd_u_n, xu_d_n, xd_d_n) = out_pre
    eu_u_L, ed_u_L, eu_d_L, ed_d_L = apply_V_L_on_eta(eu_u_n, ed_u_n,
                                                     eu_d_n, ed_d_n)
    LHS = (eu_u_L, ed_u_L, eu_d_L, ed_d_L,
           xu_u_n, xd_u_n, xu_d_n, xd_d_n)

    eu_u_T, ed_u_T, eu_d_T, ed_d_T = apply_V_L_on_eta(eta_u_u, eta_u_d,
                                                     eta_d_u, eta_d_d)
    a_new, b_new = su2_product_VU(va, vb, a, b)
    RHS = hyf.mass_step_quark_doublet_su2xu1y(
        eu_u_T, ed_u_T, eu_d_T, ed_d_T,
        chi_u_u, chi_u_d, chi_d_u, chi_d_d,
        a_new, b_new, alpha, m=m)
    return tuple_max_abs_diff(LHS, RHS)


# ── Y12 — Quark mass step unitarity ──────────────────────────────────
def test_Y12_quark_mass_unitarity(L=24, m=0.3, seed=1205):
    a, b = make_su2_field(L, L, mode='random')
    rng = np.random.default_rng(seed)
    psi = list(random_8_spinors(L, L, seed))
    n0 = tuple_norm(psi)
    for _ in range(50):
        alpha = rng.uniform(-1.0, 1.0, (L, L))
        psi = list(hyf.mass_step_quark_doublet_su2xu1y(
            *psi, a, b, alpha, m=m))
    n1 = tuple_norm(psi)
    return abs(n1 - n0) / max(n0, 1e-30)


# ── Y13 — χ kinetic step gauge covariance ────────────────────────────
def test_Y13_chi_kinetic_gauge_covariance(L=24, dt=0.5, seed=1306):
    """
    Exact gauge covariance:  S[α+β]( e^{iβY/2} χ )  =  e^{iβY/2} · S[α](χ)
    for each first-generation right-handed singlet.

    Returns the max residual across the three (e_R, u_R, d_R) checks
    plus the constant-α sanity sub-residual.
    """
    rng = np.random.default_rng(seed)
    alpha = rng.uniform(-1.0, 1.0, (L, L))
    beta  = rng.uniform(-1.0, 1.0, (L, L))

    residuals = []
    for label, y_charge in (('e_R', hyf.Y_E_R),
                            ('u_R', hyf.Y_U_R),
                            ('d_R', hyf.Y_D_R)):
        chi_u, chi_d = random_2_spinors(L, L, seed + hash(label) % 997)

        # LHS:  S[α](χ), then apply V_Y(β)
        out_pre_u, out_pre_d = hyf.kinetic_half_step_chi_u1y(
            chi_u, chi_d, alpha, y_charge, dt_half=dt)
        LHS_u, LHS_d = hyf.apply_u1y_transform_chi(
            out_pre_u, out_pre_d, beta, y_charge)

        # RHS:  V_Y(β) on χ first, then S[α+β] on it
        chi_u_p, chi_d_p = hyf.apply_u1y_transform_chi(
            chi_u, chi_d, beta, y_charge)
        RHS_u, RHS_d = hyf.kinetic_half_step_chi_u1y(
            chi_u_p, chi_d_p, alpha + beta, y_charge, dt_half=dt)

        residuals.append(float(max(np.max(np.abs(LHS_u - RHS_u)),
                                   np.max(np.abs(LHS_d - RHS_d)))))

    # Sanity sub-test: constant α factors out (kinetic is unobservable
    # for a global phase) — i.e. S[const_α](χ) == e^{iα Y/2} · spectral(χ)
    # · e^{-iα Y/2} which equals spectral(χ) (because const phase commutes).
    chi_u, chi_d = random_2_spinors(L, L, seed + 13)
    alpha_const = 0.42 * np.ones((L, L))
    out_const = hyf.kinetic_half_step_chi_u1y(
        chi_u, chi_d, alpha_const, hyf.Y_U_R, dt_half=dt)
    out_bare = _weyl_half_step_2c(chi_u, chi_d, dt)
    residuals.append(float(max(np.max(np.abs(out_const[0] - out_bare[0])),
                               np.max(np.abs(out_const[1] - out_bare[1])))))

    return float(max(residuals))


# ── Y14 — χ kinetic step α=0 reduces to bare _weyl_half_step_2c ──────
def test_Y14_chi_kinetic_alpha_zero_reduction(L=24, dt=0.5, seed=1407):
    """
    α(x) ≡ 0 → kinetic_half_step_chi_u1y is bit-for-bit equal to
    ca_dirac._weyl_half_step_2c for any hypercharge.
    """
    alpha = np.zeros((L, L))
    residuals = []
    for y_charge in (hyf.Y_E_R, hyf.Y_U_R, hyf.Y_D_R, 0.0, -3.7):
        chi_u, chi_d = random_2_spinors(L, L, seed)
        out_y = hyf.kinetic_half_step_chi_u1y(
            chi_u, chi_d, alpha, y_charge, dt_half=dt)
        out_bare = _weyl_half_step_2c(chi_u, chi_d, dt)
        residuals.append(float(max(np.max(np.abs(out_y[0] - out_bare[0])),
                                   np.max(np.abs(out_y[1] - out_bare[1])))))
    return float(max(residuals))


# ── Y15 — Gell-Mann–Nishijima algebra (quark side) ───────────────────
def test_Y15_quark_GMN_algebra():
    """
    Required:
        ΔY_u   = Y_QUARK_L − Y_u_R = −1
        ΔY_d   = Y_QUARK_L − Y_d_R = +1
        Q(u_L) = Y_QUARK_L/2 + 1/2 = +2/3
        Q(d_L) = Y_QUARK_L/2 − 1/2 = −1/3
        Q(u_R) = Y_u_R/2          = +2/3
        Q(d_R) = Y_d_R/2          = −1/3
    """
    YL = hyf.Y_QUARK_L
    YU = hyf.Y_U_R
    YD = hyf.Y_D_R
    checks = [
        YL - YU - hyf.DELTA_Y_U,           # 0
        YL - YD - hyf.DELTA_Y_D,           # 0
        (YL / 2 + 0.5) - (+2.0 / 3.0),     # Q(u_L) = 2/3
        (YL / 2 - 0.5) - (-1.0 / 3.0),     # Q(d_L) = -1/3
        (YU / 2 + 0.0) - (+2.0 / 3.0),     # Q(u_R) = 2/3
        (YD / 2 + 0.0) - (-1.0 / 3.0),     # Q(d_R) = -1/3
        hyf.DELTA_Y_U - (-1.0),            # ΔY_u = -1
        hyf.DELTA_Y_D - (+1.0),            # ΔY_d = +1
    ]
    return float(max(abs(c) for c in checks))


# ── Runner ────────────────────────────────────────────────────────────
def main():
    L = 24
    m = 0.3
    t0 = time.time()
    results = []

    def run(name, fn, target):
        t = time.time()
        try:
            r = fn()
            ok = (r is not None) and (r <= target)
        except Exception as exc:
            r = f"ERROR: {exc!r}"
            ok = False
        results.append({
            'name': name,
            'residual': r if isinstance(r, (int, float)) else r,
            'target': target,
            'pass': bool(ok),
            'elapsed_s': round(time.time() - t, 4),
        })

    run('Y8_quark_u1y_ward_d_branch',
        lambda: test_Y8_u1y_ward_d_branch(L, m),                 1e-12)
    run('Y9_quark_u1y_ward_u_branch',
        lambda: test_Y9_u1y_ward_u_branch(L, m),                 1e-12)
    run('Y10_quark_alpha_zero_reduces_to_F40',
        lambda: test_Y10_reduction_to_F40(L, m),                 1e-30)
    run('Y11_quark_su2_L_ward_with_alpha',
        lambda: test_Y11_su2_ward_quark_with_y_field(L, m),      1e-12)
    run('Y12_quark_mass_unitarity_50_steps',
        lambda: test_Y12_quark_mass_unitarity(L, m),             1e-12)
    run('Y13_chi_kinetic_gauge_covariance',
        lambda: test_Y13_chi_kinetic_gauge_covariance(L),        1e-10)
    run('Y14_chi_kinetic_alpha_zero_bitwise',
        lambda: test_Y14_chi_kinetic_alpha_zero_reduction(L),    1e-30)
    run('Y15_quark_GMN_algebra',
        lambda: test_Y15_quark_GMN_algebra(),                    1e-15)

    n_pass = sum(1 for r in results if r['pass'])
    total = len(results)
    summary = {
        'L': L, 'm': m,
        'pass_count': n_pass,
        'total_count': total,
        'elapsed_s': round(time.time() - t0, 4),
        'results': results,
    }

    print(f"\n=== Hypercharge extension tests (F42) "
          f"({n_pass}/{total} PASS, {summary['elapsed_s']} s) ===")
    for r in results:
        flag = '✓' if r['pass'] else '✗'
        res_str = f"{r['residual']:.3e}" if isinstance(r['residual'], (int, float)) else str(r['residual'])
        print(f"  {flag} {r['name']:<42} residual={res_str:>10}  "
              f"target≤{r['target']:.0e}")

    out_dir = os.path.join(_ROOT, 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'hypercharge_extension.json')
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nResults: {out_path}")
    return summary


if __name__ == '__main__':
    main()
