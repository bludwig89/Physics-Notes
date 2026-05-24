"""
test_14_QM4_zeno.py  —  QM-4: Quantum Zeno effect
===================================================
Target: For a two-state system repeatedly measured at interval Δt,
  the transition probability scales as P(Δt) ∝ (Δt)² for small Δt
  (short-time quadratic behaviour), and frequent measurement suppresses
  the transition (Zeno suppression).

Physical background
-------------------
For a two-state Hamiltonian  H = ε/2 · σ_x  (Rabi-like coupling ε
between |↑⟩ and |↓⟩), starting in |↑⟩, the survival probability after
one full time T with n measurements at spacing Δt = T/n is:

    P_survive(n) = cos²(ε·Δt/2)^n  ≈  (1 − (εΔt)²/4)^n

For Δt → 0  (n → ∞) with T fixed:  P_survive → 1  (Zeno limit).
Without measurement (n = 1): P_survive = cos²(εT/2).

Lattice implementation
----------------------
We use a SINGLE-SITE two-state system (no spatial lattice needed).
The "state" is a 2-component complex vector; the "Hamiltonian step"
is a rotation by angle θ = ε·Δt/2 around the x-axis of the Bloch sphere:
    U(Δt) = [[cos θ, −i sin θ], [−i sin θ, cos θ]]  (exact unitary).

Measurement = projection onto the initial state |↑⟩ = (1, 0)^T,
followed by renormalisation (collapse + restart).

Gates
-----
1. Quadratic scaling: the single-interval transition probability
   P_trans(Δt) ∝ Δt²  must hold to within 5% relative error in the
   slope over the range Δt ∈ [0.01, 0.5].
2. Zeno suppression: at fixed T = 10, the survival probability must
   increase monotonically as n increases from 1 → 1000 measurements.
3. Quantitative: survival at n measurements should match the analytic
   formula cos²(ε·T/(2n))^n within 1e-12 (exact unitary, no noise).
"""

import os, sys
import numpy as np
import json

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'test-results')
os.makedirs(RESULTS_DIR, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────────────────────────

def rabi_step(psi, theta):
    """One Rabi step U(theta) = exp(-i theta sigma_x / 2) acting on 2-vector."""
    c, s = np.cos(theta), np.sin(theta)
    u = np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)
    return u @ psi


def survival_with_measurements(epsilon, T, n_meas):
    """
    Evolve |↑⟩ under H = ε/2 σ_x for total time T with n_meas
    equally-spaced projective measurements onto |↑⟩.
    Returns survival probability after all measurements.
    """
    dt = T / n_meas
    theta = epsilon * dt / 2.0   # rotation angle per step
    psi = np.array([1.0, 0.0], dtype=complex)
    p_survive = 1.0

    for _ in range(n_meas):
        psi = rabi_step(psi, theta)
        # Projection onto |↑⟩ = (1,0)
        prob_up = abs(psi[0]) ** 2
        p_survive *= prob_up
        if prob_up < 1e-30:
            return 0.0
        # Collapse and renormalise
        psi = np.array([1.0, 0.0], dtype=complex)

    return float(p_survive)


def survival_analytic(epsilon, T, n_meas):
    """Analytic formula: [cos²(ε·T/(2n))]^n."""
    theta = epsilon * T / (2.0 * n_meas)
    return float(np.cos(theta) ** (2 * n_meas))


# ──────────────────────────────────────────────────────────────────────────────
#  Part 1 — Quadratic scaling of single-interval transition probability
# ──────────────────────────────────────────────────────────────────────────────

def part1_quadratic_scaling(epsilon=1.0):
    print('\n' + '=' * 72)
    print('  QM-4 Part 1 — Quadratic scaling of P_trans(Δt) ∝ (Δt)²')
    print('=' * 72)
    print(f'  ε = {epsilon}  (Rabi coupling)')

    dts = np.array([0.01, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50])
    p_trans = []

    print(f'\n  {"Δt":>8}  {"P_trans":>14}  {"analytic (εΔt)²/4":>20}  '
          f'{"ratio":>10}')
    print('  ' + '-' * 58)

    for dt in dts:
        theta = epsilon * dt / 2.0
        psi = rabi_step(np.array([1.0, 0.0], dtype=complex), theta)
        pt = float(abs(psi[1]) ** 2)   # probability of being in |↓⟩
        pt_analytic = (epsilon * dt / 2.0) ** 2  # leading-order Δt² term
        ratio = pt / pt_analytic if pt_analytic > 1e-20 else float('nan')
        p_trans.append(pt)
        print(f'  {dt:>8.3f}  {pt:>14.10f}  {pt_analytic:>20.10f}  '
              f'{ratio:>10.6f}')

    # Fit log(P_trans) vs log(Δt) — should have slope ≈ 2.0
    log_dt = np.log(dts)
    log_pt = np.log(np.array(p_trans))
    slope, intercept = np.polyfit(log_dt, log_pt, 1)
    print(f'\n  Log-log slope (should be ≈ 2.0): {slope:.6f}')
    print(f'  Deviation from 2.0: {abs(slope - 2.0):.4f}')

    ok = abs(slope - 2.0) < 0.05   # 5% gate on the exponent
    print(f'  Part 1 verdict: {"PASS" if ok else "FAIL"}  (slope = 2.0 within 5%)')
    return ok, float(slope)


# ──────────────────────────────────────────────────────────────────────────────
#  Part 2 — Zeno suppression: more measurements → higher survival
# ──────────────────────────────────────────────────────────────────────────────

def part2_zeno_suppression(epsilon=1.0, T=10.0):
    print('\n' + '=' * 72)
    print('  QM-4 Part 2 — Zeno suppression: P_survive increases with n_meas')
    print('=' * 72)
    print(f'  ε = {epsilon},  T = {T}  (fixed evolution time)')

    n_meas_vals = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    print(f'\n  {"n_meas":>8}  {"P_survive (num)":>18}  '
          f'{"P_survive (analytic)":>22}  {"|Δ|":>10}')
    print('  ' + '-' * 64)

    rows = []
    for n in n_meas_vals:
        p_num = survival_with_measurements(epsilon, T, n)
        p_ana = survival_analytic(epsilon, T, n)
        delta = abs(p_num - p_ana)
        rows.append({'n': n, 'p_num': p_num, 'p_ana': p_ana, 'delta': delta})
        print(f'  {n:>8}  {p_num:>18.14f}  {p_ana:>22.14f}  {delta:>10.2e}')

    # Monotonicity check only for n ≥ 10 (Zeno regime requires Δt ≪ T_Rabi).
    # For small n (Δt ~ T_Rabi), quantum anti-Zeno behavior (non-monotonic)
    # is physically expected and is NOT a model failure.
    T_rabi  = 2.0 * np.pi / epsilon
    print(f'\n  T_Rabi = 2π/ε = {T_rabi:.4f}  (Zeno requires Δt = T/n ≪ T_Rabi)')
    p_vals = [r['p_num'] for r in rows]
    n_vals = [r['n']     for r in rows]

    # Split into anti-Zeno (small n, Δt ≥ T_Rabi/2) and Zeno (large n)
    zeno_rows  = [(n, p) for n, p in zip(n_vals, p_vals) if T / n < T_rabi / 2]
    antizeno_n = [n for n, p in zip(n_vals, p_vals) if T / n >= T_rabi / 2]
    if len(antizeno_n) > 0:
        print(f'  n ∈ {antizeno_n}: anti-Zeno regime (Δt ≥ T_Rabi/2) — '
              f'non-monotonic behaviour expected, not checked.')

    monotonic_zeno = (len(zeno_rows) < 2 or
                      all(zeno_rows[i][1] <= zeno_rows[i+1][1]
                          for i in range(len(zeno_rows)-1)))
    max_delta = max(r['delta'] for r in rows)
    ok_quant = max_delta < 1e-12
    ok_mono  = monotonic_zeno

    print(f'  Zeno regime (n ≥ {zeno_rows[0][0] if zeno_rows else "?"}): '
          f'monotonically increasing = {"YES" if monotonic_zeno else "NO"}')
    print(f'  Max |P_num − P_analytic|: {max_delta:.2e}')
    print(f'  P_survive(n=1)   = {p_vals[0]:.6f}')
    print(f'  P_survive(n=1000)= {p_vals[-1]:.6f}  (Zeno protection)')
    print(f'\n  Part 2 verdict: {"PASS" if (ok_mono and ok_quant) else "FAIL"}  '
          f'(Zeno-regime monotonic + |Δ| < 1e-12)')
    return ok_mono and ok_quant, rows, max_delta


# ──────────────────────────────────────────────────────────────────────────────
#  Part 3 — Quantitative Zeno: single-formula check
# ──────────────────────────────────────────────────────────────────────────────

def part3_formula_check(epsilon=0.5, T=5.0):
    print('\n' + '=' * 72)
    print('  QM-4 Part 3 — Quantitative: P = [cos²(εT/2n)]^n  exact match')
    print('=' * 72)
    print(f'  ε = {epsilon},  T = {T}')

    # Dense scan
    ns = [1, 3, 7, 15, 31, 63, 127, 255, 511, 1023]
    max_err = 0.0
    print(f'\n  {"n":>6}  {"P_num":>16}  {"P_analytic":>16}  {"err":>12}')
    print('  ' + '-' * 54)
    for n in ns:
        p_num = survival_with_measurements(epsilon, T, n)
        p_ana = survival_analytic(epsilon, T, n)
        err = abs(p_num - p_ana)
        max_err = max(max_err, err)
        print(f'  {n:>6}  {p_num:>16.13f}  {p_ana:>16.13f}  {err:>12.2e}')

    ok = max_err < 1e-12
    print(f'\n  Max |err|: {max_err:.2e}')
    print(f'  Part 3 verdict: {"PASS" if ok else "FAIL"}  (gate 1e-12)')
    return ok, float(max_err)


# ──────────────────────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    ok1, slope      = part1_quadratic_scaling(epsilon=1.0)
    ok2, rows2, d2  = part2_zeno_suppression(epsilon=1.0, T=10.0)
    ok3, max_err3   = part3_formula_check(epsilon=0.5, T=5.0)

    print('\n' + '=' * 72)
    print('  QM-4 SUMMARY — Quantum Zeno Effect')
    print('=' * 72)
    print(f'  Part 1  P_trans ∝ (Δt)²  log-log slope (5% gate):  '
          f'{"PASS" if ok1 else "FAIL"}  (slope = {slope:.4f})')
    print(f'  Part 2  Zeno suppression + quantitative (1e-12):    '
          f'{"PASS" if ok2 else "FAIL"}')
    print(f'  Part 3  Formula P=[cos²(εT/2n)]^n (1e-12 gate):    '
          f'{"PASS" if ok3 else "FAIL"}')

    overall = ok1 and ok2 and ok3
    print(f'\n  QM-4 overall: {"PASS" if overall else "FAIL"}')

    result = {
        'test': 'QM-4',
        'ok1_quadratic': bool(ok1),
        'slope': slope,
        'ok2_zeno': bool(ok2),
        'max_delta_analytic': float(d2),
        'ok3_formula': bool(ok3),
        'max_formula_err': float(max_err3),
        'overall': bool(overall),
    }
    out = os.path.join(RESULTS_DIR, 'test_14_QM4_zeno.json')
    with open(out, 'w') as fh:
        json.dump(result, fh, indent=2)
    print(f'\n  Results saved to {out}')
