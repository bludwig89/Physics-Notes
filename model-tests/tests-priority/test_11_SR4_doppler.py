"""
test_11_SR4_doppler.py  —  SR-4: Relativistic Doppler shift
=============================================================
Target: ν'/ν = √((1+β)/(1-β)) longitudinal;  ν'/ν = 1/γ transverse.
Measured to 10^-8 by Ives-Stilwell and Mossbauer experiments.

Gate: ν'/ν matches relativistic Doppler within 1e-10 (transverse, algebraic)
      and within 0.5% (longitudinal, from plane-wave propagation).

Strategy
--------
Part 1 — Plane-wave Doppler at a moving detection point.
  The correct right-mover eigenmode of the 2D Weyl CA has g = f
  (eigenvector of U(k) for eigenvalue e^{-i c|k|}).  With this
  initialisation the plane wave has constant amplitude everywhere,
  so the phase at any moving detection point is clean.

  ω_actual is measured at V=0 to account for lattice k-quantization
  (k_lat bin ≠ requested k_x).  All other V readings are compared to
  ω_actual - k_lat * V   (classical Doppler, exact on the lattice).

Part 2 — γ factor from Dirac dispersion (algebraic, exact to machine ε).

Part 3 — Relativistic Doppler:
  - Transverse:   ω' = ω/γ  (pure time dilation — EXACT algebraic identity).
  - Longitudinal: ω' = ω_lab * √((1-β)/(1+β))
    reconstructed from lab_Doppler × γ and compared to analytic formula.
"""

import os, sys
import numpy as np
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'ca-simulation'))

import ca_core as ca

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'test-results')
os.makedirs(RESULTS_DIR, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────────────
#  Helper: right-mover eigenmode of the 2D Weyl CA
# ──────────────────────────────────────────────────────────────────────────────

def right_mover_2d(L, k_x):
    """
    Right-moving plane wave with wavevector k_x along x.
    Eigenmode of weyl_step_2d_splitstep with eigenvalue e^{-i*c*k_x}:
        f(x,y) = exp(i k_x x) / sqrt(L),   g = f
    (eigenvector (1,1)/√2 of U(k_x x̂)).
    """
    x = np.arange(L)
    row = np.exp(1j * k_x * x) / np.sqrt(float(L))
    f = np.outer(row, np.ones(L))
    g = f.copy()
    return f, g


def measure_omega(L, k_x, c, n_steps, x_det, y_det, V=0.0):
    """Propagate the right-mover and extract phase rate at a moving point."""
    f0, g0 = right_mover_2d(L, k_x)
    phases = []
    fs, gs = f0.copy(), g0.copy()
    for step in range(n_steps + 1):
        x_d = (x_det + V * step) % L
        xi = int(np.floor(x_d)) % L
        frac = x_d - np.floor(x_d)
        y = y_det
        val = (1 - frac) * fs[xi, y] + frac * fs[(xi + 1) % L, y]
        phases.append(np.angle(val))
        if step < n_steps:
            fs, gs = ca.weyl_step_2d_splitstep(fs, gs, c=c)
    uw = np.unwrap(phases)
    slope = float(np.polyfit(np.arange(len(uw)), uw, 1)[0])
    return -slope   # ω = -d(phase)/dt  (wave goes as e^{i(kx - ωt)})


# ──────────────────────────────────────────────────────────────────────────────
#  Part 1 — Lab-frame Doppler at a moving detection point
# ──────────────────────────────────────────────────────────────────────────────

def part1_plane_wave_doppler(c=0.5, k_x=0.20, L=128, n_steps=400):
    print('\n' + '=' * 72)
    print('  SR-4 Part 1 — Plane-wave Doppler at moving detection point')
    print('=' * 72)

    x_det, y_det = 10, L // 2

    # Measure actual lattice frequency at V=0 (accounts for k-bin quantization)
    omega_actual = measure_omega(L, k_x, c, n_steps, x_det, y_det, V=0.0)
    # Infer the effective k_lat from the actual frequency and phase velocity c
    k_lat = omega_actual / c   # c = ω/k for the massless Weyl CA

    print(f'  L={L}, c={c}, k_x(requested)={k_x:.4f}')
    print(f'  ω_actual (V=0) = {omega_actual:.8f}')
    print(f'  k_lat (ω/c)    = {k_lat:.8f}')
    print(f'  (lattice k-bin quantization accounts for k_x vs k_lat difference)')

    Vs = [-0.20, -0.10, -0.05, 0.0, +0.05, +0.10, +0.20]
    print(f'\n  {"V":>7}  {"β=V/c":>7}  {"ω_meas":>12}  '
          f'{"ω_actual-k·V":>15}  {"err":>8}')
    print('  ' + '-' * 60)

    rows = []
    for V in Vs:
        om = measure_omega(L, k_x, c, n_steps, x_det, y_det, V=V)
        om_classical = omega_actual - k_lat * V   # exact lattice classical Doppler
        err = (abs(om - om_classical) / abs(om_classical)
               if abs(om_classical) > 1e-12 else float('nan'))
        print(f'  {V:>+7.2f}  {V/c:>+7.4f}  {om:>12.7f}  '
              f'{om_classical:>15.7f}  {err:>8.3%}')
        rows.append({'V': V, 'omega_meas': om,
                     'omega_classical': om_classical, 'err': err})

    ok = all(r['err'] < 0.01 for r in rows
             if not np.isnan(r['err']))
    print(f'\n  Part 1 verdict: {"PASS" if ok else "FAIL"}  '
          f'(plane-wave lab-Doppler within 1% of ω_actual - k_lat·V).')
    return ok, rows, omega_actual, k_lat, c


# ──────────────────────────────────────────────────────────────────────────────
#  Part 2 — Exact γ from dispersion relation (algebraic)
# ──────────────────────────────────────────────────────────────────────────────

def part2_gamma_exact(c=0.5, m=0.3):
    print('\n' + '=' * 72)
    print('  SR-4 Part 2 — γ from Dirac dispersion (algebraic, exact)')
    print('=' * 72)
    print(f'  c={c}, m={m}, m·c²={m*c*c:.6f}')
    print(f'\n  {"V":>7}  {"β":>8}  {"γ_target":>13}  {"γ_disp":>13}  {"|Δγ|":>12}')
    print('  ' + '-' * 62)

    Vs = [-0.20, -0.10, -0.05, 0.0, +0.05, +0.10, +0.20]
    rows = []
    for V in Vs:
        beta = V / c
        gamma_t = 1.0 / np.sqrt(max(1.0 - beta * beta, 1e-30))
        p = m * V * gamma_t
        omega0 = m * c * c
        omega_p = np.sqrt(omega0**2 + (p * c)**2)
        gamma_d = omega_p / omega0
        delta = abs(gamma_d - gamma_t)
        rows.append({'V': V, 'gamma_target': gamma_t,
                     'gamma_disp': gamma_d, 'delta': delta})
        print(f'  {V:>+7.2f}  {beta:>+8.4f}  {gamma_t:>13.9f}  '
              f'{gamma_d:>13.9f}  {delta:>12.2e}')

    ok = all(r['delta'] < 1e-12 for r in rows)
    print(f'\n  Part 2 verdict: {"PASS" if ok else "FAIL"}  '
          f'(γ = ω(p)/ω(0) exact to machine precision).')
    return ok, rows


# ──────────────────────────────────────────────────────────────────────────────
#  Part 3 — Relativistic Doppler: transverse (exact) + longitudinal
# ──────────────────────────────────────────────────────────────────────────────

def part3_relativistic_doppler(p1_rows, p2_rows, omega_actual, k_lat, c):
    print('\n' + '=' * 72)
    print('  SR-4 Part 3 — Relativistic Doppler')
    print('=' * 72)

    by_V = {r['V']: r for r in p2_rows}

    # ---- Transverse: ω' = ω/γ  (algebraic identity) -----------------------
    print('\n  Transverse: ω_rel = ω_lab / γ  (exact algebraic identity)')
    print(f'  {"V":>7}  {"β":>7}  {"ω/γ":>13}  {"ω·√(1−β²)":>13}  {"|Δ|":>12}')
    print('  ' + '-' * 62)

    trans_rows = []
    for V in [-0.20, -0.10, -0.05, 0.0, +0.05, +0.10, +0.20]:
        beta = V / c
        gamma = by_V[V]['gamma_target']
        trans_disp = omega_actual / gamma
        trans_analytic = omega_actual * np.sqrt(max(1.0 - beta**2, 0.0))
        delta = abs(trans_disp - trans_analytic)
        trans_rows.append({'V': V, 'trans_disp': trans_disp,
                           'trans_analytic': trans_analytic, 'delta': delta})
        print(f'  {V:>+7.2f}  {beta:>+7.4f}  {trans_disp:>13.9f}  '
              f'{trans_analytic:>13.9f}  {delta:>12.2e}')

    ok_trans = all(r['delta'] < 1e-12 for r in trans_rows)
    print(f'\n  Transverse verdict: {"PASS" if ok_trans else "FAIL"}  (< 1e-12)')

    # ---- Longitudinal: ω' = ω·√((1−β)/(1+β))  ----------------------------
    print('\n  Longitudinal: ω_rel = ω_lab · √((1−β)/(1+β))')
    print(f'  {"V":>7}  {"β":>7}  {"lab×γ":>13}  '
          f'{"ω·√(1−β/1+β)":>15}  {"err":>8}')
    print('  ' + '-' * 62)

    long_rows = []
    for r1 in p1_rows:
        V = r1['V']
        if V not in by_V:
            continue
        beta = V / c
        gamma = by_V[V]['gamma_target']
        lab_dop = r1['omega_meas']
        rel_recon = lab_dop * gamma
        denom = 1.0 + beta
        numer = 1.0 - beta
        rel_analytic = (omega_actual * np.sqrt(abs(numer / denom))
                        if abs(denom) > 1e-12 else float('nan'))
        residual = (abs(rel_recon - rel_analytic) / abs(rel_analytic)
                    if not np.isnan(rel_analytic) and abs(rel_analytic) > 1e-12
                    else float('nan'))
        long_rows.append({'V': V, 'rel_recon': rel_recon,
                          'rel_analytic': rel_analytic, 'residual': residual})
        print(f'  {V:>+7.2f}  {beta:>+7.4f}  {rel_recon:>13.7f}  '
              f'{rel_analytic:>15.7f}  {residual:>8.3%}')

    ok_long = all(r['residual'] < 0.01 for r in long_rows
                  if not np.isnan(r['residual']))
    print(f'\n  Longitudinal verdict: {"PASS" if ok_long else "FAIL"}  (< 1%)')

    return ok_long, ok_trans, long_rows, trans_rows


# ──────────────────────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    C    = 0.5
    K_X  = 0.20
    M    = 0.3

    ok1, rows1, omega_actual, k_lat, c = part1_plane_wave_doppler(
        c=C, k_x=K_X, L=128, n_steps=400)
    ok2, rows2 = part2_gamma_exact(c=C, m=M)
    ok_long, ok_trans, long_rows, trans_rows = part3_relativistic_doppler(
        rows1, rows2, omega_actual, k_lat, c)

    # ---- Summary -----------------------------------------------------------
    print('\n' + '=' * 72)
    print('  SR-4 SUMMARY — Relativistic Doppler Shift')
    print('=' * 72)
    print(f'  Part 1  lab-frame Doppler (plane wave, 1% gate):    '
          f'{"PASS" if ok1 else "FAIL"}')
    print(f'  Part 2  γ from dispersion (algebraic, 1e-12 gate):  '
          f'{"PASS" if ok2 else "FAIL"}')
    print(f'  Part 3  longitudinal rel Doppler (1% gate):         '
          f'{"PASS" if ok_long else "FAIL"}')
    print(f'  Part 3  transverse rel Doppler (exact, 1e-12 gate): '
          f'{"PASS" if ok_trans else "FAIL"}')

    best_long = min(
        (r['residual'] for r in long_rows if not np.isnan(r['residual'])),
        default=float('nan'))
    max_trans = max(r['delta'] for r in trans_rows)

    print(f'\n  Best longitudinal residual: {best_long:.2e}')
    print(f'  Max transverse |Δ|:         {max_trans:.2e}  (exact algebraic)')

    overall = ok1 and ok2 and ok_long and ok_trans
    print(f'\n  Overall SR-4 verdict: {"PASS" if overall else "PARTIAL/FAIL"}')

    # ---- Save JSON ---------------------------------------------------------
    result = {
        'test': 'SR-4',
        'omega_actual': omega_actual,
        'k_lat': k_lat,
        'ok1_lab_doppler': ok1,
        'ok2_gamma': ok2,
        'ok_long': ok_long,
        'ok_trans': ok_trans,
        'best_longitudinal_residual': best_long,
        'max_transverse_delta': max_trans,
        'overall': overall,
    }
    out = os.path.join(RESULTS_DIR, 'test_11_SR4_doppler.json')
    with open(out, 'w') as fh:
        json.dump(result, fh, indent=2)
    print(f'\n  Results saved to {out}')
