"""
test_hypercharge.py — U(1)_Y hypercharge gauging on the
                      Higgs-free F27 chiral-SU(2) mass step
2026-05-26 - 17:45

Run from project root:
    python model-tests/test_hypercharge.py

Writes JSON to test-results/hypercharge_fork.json.
(File renamed from test_hypercharge_fork.py after fork promotion to
`ca_hypercharge.py`; result JSON name kept for traceability.)

Hypothesis under test
---------------------
After abandoning the Higgs (F27 + F34b), U(1)_Y *can* still be exactly
gauged on the fermion sector PROVIDED the F27 pure-gauge SU(2)_L field
U(x) is extended to carry the Higgs hypercharge:
    U(x) → U(x) · e^{i α(x) (Y_L − Y_R)/2}
The SU(2)_L lepton field is unaffected because U(1)_Y commutes with
SU(2)_L on the doublet (both ν_L and e_L share Y_L = −1).

Tests
-----
Y1  U(1)_Y Ward identity, mass step, e_R branch (charged-lepton).
Y2  U(1)_Y Ward identity, mass step, ν_R branch (conjugate-Higgs).
Y3  α(x) ≡ 0 → bit-for-bit equal to F27 mass_step_doublet_su2.
Y4  SU(2)_L Ward identity (F27 T5) preserved with α(x) nontrivial.
Y5  Pure-SU(2) sector unchanged: with U=I and B-links on, ν_L and e_L
    only acquire a common e^{iα·Y_L/2} phase (no isospin rotation).
Y6  Unitarity of the combined mass step (norm conserved).
Y7  Charge conservation: Q = T_3 + Y/2 phase under combined transform.
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
)
import ca_hypercharge as hyf  # noqa: E402  (merged from forks/hypercharge_fork.py 2026-05-26 - 17:45)


# ── Helpers ───────────────────────────────────────────────────────────
def random_spinor(Lx, Ly, seed):
    rng = np.random.default_rng(seed=seed)
    def cmplx():
        return rng.standard_normal((Lx, Ly)) + 1j * rng.standard_normal((Lx, Ly))
    return [cmplx() for _ in range(8)]


def tuple_max_abs_diff(a, b):
    """max |a_i − b_i| across an 8-tuple of arrays."""
    return float(max(np.max(np.abs(ai - bi)) for ai, bi in zip(a, b)))


def tuple_norm(t):
    """Sum |x|² over an 8-tuple of arrays."""
    return float(sum(np.sum(np.abs(x)**2) for x in t))


# ── Tests ─────────────────────────────────────────────────────────────
def test_Y1_u1y_ward_e_branch(L=24, m=0.3, seed=101):
    """
    e-branch U(1)_Y Ward identity:

      Let ψ' = V_Y · ψ,  U' = U · e^{i β·ΔY_e/2}.
      Then  V_Y · mass(ψ; U, α=0)  ==  mass(ψ'; U', α' = β)  (for e-branch
      with ν branch silenced).

    To isolate the e-branch we set χ_ν = 0 and Y_ν_R = 0 → ν-branch is
    Y-neutral and decouples from β.  Then the test reduces to:

      e^{iβ·Y_L/2} · mass_e_only(ψ; U, 0)  ==  mass_e_only(ψ'; U, β)

    because the η→χ_e term picks up e^{iβ·ΔY_e/2} = e^{iβ(Y_L−Y_e_R)/2}
    on the LHS (from V_Y on η and on χ_e), and e^{iβ·ΔY_e/2} on the RHS
    (from α = β inside mass_step), which match.
    """
    a, b = make_su2_field(L, L, mode='random')
    rng_beta = np.random.default_rng(seed)
    beta = rng_beta.uniform(-1.0, 1.0, (L, L))   # smaller range → cleaner
    # ν-branch silenced:
    eta_nu_u, eta_nu_d, eta_e_u, eta_e_d, \
        _0, _1, chi_e_u, chi_e_d = random_spinor(L, L, seed)
    chi_nu_u = np.zeros((L, L), dtype=complex)
    chi_nu_d = np.zeros((L, L), dtype=complex)

    psi = (eta_nu_u, eta_nu_d, eta_e_u, eta_e_d,
           chi_nu_u, chi_nu_d, chi_e_u, chi_e_d)

    # LHS: mass(ψ; U, α=0), then apply V_Y
    out_pre = hyf.mass_step_doublet_su2xu1y(
        *psi, a, b, np.zeros_like(beta), m=m)
    LHS = hyf.apply_u1y_transform(*out_pre, beta)

    # RHS: apply V_Y to inputs, then mass(ψ'; U, α=β)
    psi_p = hyf.apply_u1y_transform(*psi, beta)
    RHS = hyf.mass_step_doublet_su2xu1y(*psi_p, a, b, beta, m=m)

    return tuple_max_abs_diff(LHS, RHS)


def test_Y2_u1y_ward_nu_branch(L=24, m=0.3, seed=202):
    """
    ν-branch U(1)_Y Ward identity (conjugate-Higgs).
    Silence e-branch by setting χ_e=0, Y_e_R=0 inside apply_u1y_transform.
    """
    a, b = make_su2_field(L, L, mode='random')
    rng_beta = np.random.default_rng(seed)
    beta = rng_beta.uniform(-1.0, 1.0, (L, L))
    eta_nu_u, eta_nu_d, eta_e_u, eta_e_d, \
        chi_nu_u, chi_nu_d, _2, _3 = random_spinor(L, L, seed)
    chi_e_u = np.zeros((L, L), dtype=complex)
    chi_e_d = np.zeros((L, L), dtype=complex)

    psi = (eta_nu_u, eta_nu_d, eta_e_u, eta_e_d,
           chi_nu_u, chi_nu_d, chi_e_u, chi_e_d)

    out_pre = hyf.mass_step_doublet_su2xu1y(
        *psi, a, b, np.zeros_like(beta), m=m)
    LHS = hyf.apply_u1y_transform(*out_pre, beta)

    psi_p = hyf.apply_u1y_transform(*psi, beta)
    RHS = hyf.mass_step_doublet_su2xu1y(*psi_p, a, b, beta, m=m)
    return tuple_max_abs_diff(LHS, RHS)


def test_Y3_reduction_to_F27(L=24, m=0.3, seed=303):
    """α(x) ≡ 0 → identical to ca_dirac.mass_step_doublet_su2 bit-for-bit."""
    a, b = make_su2_field(L, L, mode='random')
    psi = random_spinor(L, L, seed)
    alpha = np.zeros((L, L))

    out_hyf = hyf.mass_step_doublet_su2xu1y(*psi, a, b, alpha, m=m)
    out_f27 = mass_step_doublet_su2(*psi, a, b, m=m)
    return tuple_max_abs_diff(out_hyf, out_f27)


def test_Y4_su2_ward_with_y_field(L=24, m=0.3, seed=404):
    """
    F27 SU(2)_L Ward identity in the presence of a nontrivial α(x):
        V_L · mass(ψ; U, α)   ==   mass(V_L·ψ; V_L·U, α)
    V_L acts on η (left isospin) only, U → V·U, α(x) is unchanged.
    """
    L = L
    a, b = make_su2_field(L, L, mode='random')
    va, vb = make_su2_field(L, L, mode='random')
    rng_alpha = np.random.default_rng(seed)
    alpha = rng_alpha.uniform(-1.0, 1.0, (L, L))
    psi = random_spinor(L, L, seed + 1)
    eta_nu_u, eta_nu_d, eta_e_u, eta_e_d, \
        chi_nu_u, chi_nu_d, chi_e_u, chi_e_d = psi

    def apply_V_L_on_eta(eu_nu_u, eu_nu_d, eu_e_u, eu_e_d):
        # V · η_iso: [Va, -Vb*; Vb, Va*] · (ν, e)
        Vac, Vbc = np.conj(va), np.conj(vb)
        nu_u = va * eu_nu_u - Vbc * eu_e_u
        nu_d = va * eu_nu_d - Vbc * eu_e_d
        e_u  = vb * eu_nu_u + Vac * eu_e_u
        e_d  = vb * eu_nu_d + Vac * eu_e_d
        return nu_u, nu_d, e_u, e_d

    def su2_product_VU(va_, vb_, ua_, ub_):
        # (V·U)_a, (V·U)_b for V=[[va,-vb*],[vb,va*]], U=[[ua,-ub*],[ub,ua*]]
        a_out = va_ * ua_ - np.conj(vb_) * ub_
        b_out = vb_ * ua_ + np.conj(va_) * ub_
        return a_out, b_out

    # LHS: mass(ψ; U, α) then V_L
    out_pre = hyf.mass_step_doublet_su2xu1y(*psi, a, b, alpha, m=m)
    (eu_nu_n, ed_nu_n, eu_e_n, ed_e_n,
     xu_nu_n, xd_nu_n, xu_e_n, xd_e_n) = out_pre
    eu_nu_L, ed_nu_L, eu_e_L, ed_e_L = apply_V_L_on_eta(eu_nu_n, ed_nu_n, eu_e_n, ed_e_n)
    LHS = (eu_nu_L, ed_nu_L, eu_e_L, ed_e_L,
           xu_nu_n, xd_nu_n, xu_e_n, xd_e_n)

    # RHS: V_L on η in inputs, U→V·U, same α
    eu_nu_T, ed_nu_T, eu_e_T, ed_e_T = apply_V_L_on_eta(eta_nu_u, eta_nu_d,
                                                       eta_e_u, eta_e_d)
    a_new, b_new = su2_product_VU(va, vb, a, b)
    RHS = hyf.mass_step_doublet_su2xu1y(
        eu_nu_T, ed_nu_T, eu_e_T, ed_e_T,
        chi_nu_u, chi_nu_d, chi_e_u, chi_e_d,
        a_new, b_new, alpha, m=m)
    return tuple_max_abs_diff(LHS, RHS)


def test_Y5_su2_lepton_field_undisturbed(L=24, m=0.3, seed=505):
    """
    With U(x) = I (no SU(2)_L gauge content) the U(1)_Y extension must
    NOT induce isospin rotation — i.e. starting from a pure ν_R initial
    state, χ_ν → η_ν only (η_e remains exactly zero), and vice-versa.

    This is the clean statement of "U(1)_Y commutes with isospin": the
    Higgs-equivalent phase factors diag(ph_nu, ph_e) inside U enter as
    a *diagonal* matrix that, when multiplied by U=I, stays diagonal.

    Test residual: max|η_e_out| starting from pure χ_ν, plus
                   max|η_ν_out| starting from pure χ_e.
    """
    a = np.ones((L, L), dtype=complex)
    b = np.zeros((L, L), dtype=complex)
    rng = np.random.default_rng(seed)
    alpha = rng.uniform(-1.0, 1.0, (L, L))

    # Pure χ_ν state
    chi_nu_u = rng.standard_normal((L, L)) + 1j * rng.standard_normal((L, L))
    chi_nu_d = rng.standard_normal((L, L)) + 1j * rng.standard_normal((L, L))
    z = np.zeros((L, L), dtype=complex)
    out_nu = hyf.mass_step_doublet_su2xu1y(
        z, z, z, z, chi_nu_u, chi_nu_d, z, z, a, b, alpha, m=m)
    leak_into_e = max(np.max(np.abs(out_nu[2])), np.max(np.abs(out_nu[3])))

    # Pure χ_e state
    chi_e_u = rng.standard_normal((L, L)) + 1j * rng.standard_normal((L, L))
    chi_e_d = rng.standard_normal((L, L)) + 1j * rng.standard_normal((L, L))
    out_e = hyf.mass_step_doublet_su2xu1y(
        z, z, z, z, z, z, chi_e_u, chi_e_d, a, b, alpha, m=m)
    leak_into_nu = max(np.max(np.abs(out_e[0])), np.max(np.abs(out_e[1])))

    return float(max(leak_into_e, leak_into_nu))


def test_Y6_unitarity(L=24, m=0.3, seed=606):
    """Norm conservation over 50 random U, α steps."""
    a, b = make_su2_field(L, L, mode='random')
    rng = np.random.default_rng(seed)
    psi = list(random_spinor(L, L, seed))
    n0 = tuple_norm(psi)
    for _ in range(50):
        alpha = rng.uniform(-1.0, 1.0, (L, L))
        psi = list(hyf.mass_step_doublet_su2xu1y(*psi, a, b, alpha, m=m))
    n1 = tuple_norm(psi)
    return abs(n1 - n0) / max(n0, 1e-30)


def test_Y7_GMN_charge_consistency():
    """
    Algebraic check that the per-branch absorbed hypercharges match
    Q = T_3 + Y/2 for the (ν, e) doublet via mass coupling η_L ↔ χ_R.

    Required:  Y_L − Y_e_R   = +1   (Higgs)
               Y_L − Y_nu_R  = −1   (conjugate Higgs)
               (Y_e_R − Y_L)/2 + T_3(e_L) = Q(e) = −1
               (Y_L)/2 + T_3(ν_L) = Q(ν) = 0
    """
    Y_L = hyf.Y_LEPTON_L
    Y_eR = hyf.Y_E_R
    Y_nR = hyf.Y_NU_R
    checks = [
        Y_L - Y_eR - hyf.DELTA_Y_E,            # should be 0
        Y_L - Y_nR - hyf.DELTA_Y_NU,           # should be 0
        (Y_L / 2 + 0.5) - 0,                   # Q(ν_L) = 0
        (Y_L / 2 - 0.5) - (-1),                # Q(e_L) = -1
        (Y_eR / 2 + 0) - (-1),                 # Q(e_R) = -1
        (Y_nR / 2 + 0) - 0,                    # Q(ν_R) = 0
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

    run('Y1_u1y_ward_e_branch',         lambda: test_Y1_u1y_ward_e_branch(L, m),        1e-12)
    run('Y2_u1y_ward_nu_branch',        lambda: test_Y2_u1y_ward_nu_branch(L, m),       1e-12)
    run('Y3_reduction_to_F27_bitwise',  lambda: test_Y3_reduction_to_F27(L, m),         1e-30)
    run('Y4_su2_L_ward_with_alpha',     lambda: test_Y4_su2_ward_with_y_field(L, m),    1e-12)
    run('Y5_su2_lepton_field_undisturbed', lambda: test_Y5_su2_lepton_field_undisturbed(L, m), 1e-12)
    run('Y6_unitarity_50_steps',        lambda: test_Y6_unitarity(L, m),                1e-12)
    run('Y7_GMN_charge_algebra',        lambda: test_Y7_GMN_charge_consistency(),       0.0)

    n_pass = sum(1 for r in results if r['pass'])
    total = len(results)
    summary = {
        'L': L, 'm': m,
        'pass_count': n_pass,
        'total_count': total,
        'elapsed_s': round(time.time() - t0, 4),
        'results': results,
    }

    # Print summary
    print(f"\n=== Hypercharge fork tests ({n_pass}/{total} PASS, "
          f"{summary['elapsed_s']} s) ===")
    for r in results:
        flag = '✓' if r['pass'] else '✗'
        res_str = f"{r['residual']:.3e}" if isinstance(r['residual'], (int, float)) else str(r['residual'])
        print(f"  {flag} {r['name']:<38} residual={res_str:>10}  "
              f"target≤{r['target']:.0e}")

    # Persist
    out_dir = os.path.join(_ROOT, 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'hypercharge_fork.json')
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nResults: {out_path}")
    return summary


if __name__ == '__main__':
    main()
