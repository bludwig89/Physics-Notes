"""
GR-2 absolute Shapiro time delay — OPEN-BOUNDARY Poisson kernel re-test
=======================================================================
Date: 2026-05-20

Replaces the periodic FFT-Poisson in test_05_GR2_shapiro.py with the
free-space James/Hockney solver in poisson_open.py.

Shapiro delay: integrate the photon travel-time excess
    Δt_excess = ∫ (1/c(x) − 1/c_0) dℓ ,   c(x) = c_0/(1 − 2φ/c_0²)
along a straight ray of impact parameter b through the free-space
Newtonian potential of a Gaussian point mass.  Compare to the
closed-form GR Shapiro
    Δt_GR = (2GM/c_0³) · log[(r_1+r_2+r_12)/(r_1+r_2−r_12)].

Under the *periodic* kernel this ratio was ~0.5 (rising slowly with L,
because the periodic Green's function suppresses the far-field 1/r tail
that dominates the Shapiro log).  With the *open-BC* kernel the potential
is the true free-space 1/r, so the ratio should approach 1.
"""

import os, sys, math, json
import numpy as np

THIS = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(THIS, '..', '..', 'ca-simulation')))

from poisson_open import solve_poisson_3d_open, gaussian_mass_3d


def shapiro_open(L, M, sigma, G_N, c_0, b, half_span=None):
    """Open-BC Shapiro delay.  Ray runs along +x at y=L/2+b, z=L/2,
    spanning x ∈ [L/2 - half_span, L/2 + half_span].  Returns
    (excess_lat, delta_GR, r_1, r_2, r_12, ratio)."""
    if half_span is None:
        half_span = L // 2 - 2
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = solve_poisson_3d_open(rho, G_N=G_N)
    c_field = c_0 / (1.0 - 2.0 * phi / c_0**2)

    cx = cy = cz = L // 2
    j_y = L//2 + b
    k_z = L//2
    x_start = cx - half_span
    x_end   = cx + half_span
    xs = np.arange(x_start, x_end + 1)

    one_over_c = 1.0 / c_field[xs, j_y, k_z]
    t_lat  = float(np.sum(one_over_c))
    t_free = float(len(xs)) / c_0
    excess_lat = t_lat - t_free

    p_start = np.array([x_start, j_y, k_z])
    p_end   = np.array([x_end,   j_y, k_z])
    p_mass  = np.array([cx, cy, cz])
    r_1  = float(np.linalg.norm(p_start - p_mass))
    r_2  = float(np.linalg.norm(p_end   - p_mass))
    r_12 = float(np.linalg.norm(p_end   - p_start))

    arg_num = r_1 + r_2 + r_12
    arg_den = r_1 + r_2 - r_12
    if arg_den < 1e-12:
        return None
    delta_GR = 2.0 * G_N * M / c_0**3 * math.log(arg_num / arg_den)
    ratio = excess_lat / delta_GR if delta_GR != 0 else float('nan')
    return excess_lat, delta_GR, r_1, r_2, r_12, ratio


def main():
    print('=' * 70)
    print('GR-2 — absolute Shapiro time delay (OPEN-BC kernel)')
    print('=' * 70)
    print('Date 2026-05-20')
    print()
    out = {'date': '2026-05-20', 'test': 'GR-2 Shapiro absolute (open BC)',
           'kernel': 'James/Hockney free-space FFT-Poisson'}

    M = 1.0
    sigma = 3.0
    G_N = 0.0005
    c_0 = 0.5

    # Stage 1: b scan at L=128, full-box ray
    print(f'Stage 1: b scan at L=128 (full-box ray), M={M}, σ={sigma}, '
          f'G={G_N}, c_0={c_0}')
    print(f'{"b":>4} {"Δt_lat":>14} {"Δt_GR":>14} {"ratio":>10} {"rel_resid":>12}')
    print('-' * 60)
    rows = []
    L = 128
    for b in [6, 10, 16, 24]:
        res = shapiro_open(L, M, sigma, G_N, c_0, b)
        if res is None:
            continue
        excess_lat, delta_GR, r_1, r_2, r_12, ratio = res
        rel = abs(excess_lat - delta_GR) / abs(delta_GR)
        print(f'{b:>4d} {excess_lat:>14.6e} {delta_GR:>14.6e} {ratio:>10.5f} {rel:>12.4e}')
        rows.append({'b': b, 'excess_lat': excess_lat, 'delta_GR': delta_GR,
                     'ratio': ratio, 'rel_residual': rel})
    out['stage1_b_scan'] = rows
    mean_ratio_128 = float(np.mean([r['ratio'] for r in rows]))
    print(f'\n  Mean ratio at L=128: {mean_ratio_128:.5f}')

    # Stage 2: convergence in L at fixed b=8
    print()
    print('Stage 2: convergence in L at fixed b=8, σ=3 (full-box ray)')
    print(f'{"L":>6} {"Δt_lat":>14} {"Δt_GR":>14} {"ratio":>10}')
    L_rows = []
    for L in [64, 96, 128, 160, 192]:
        res = shapiro_open(L, M, sigma, G_N, c_0, b=8)
        if res is None:
            continue
        excess_lat, delta_GR, r_1, r_2, r_12, ratio = res
        print(f'{L:>6d} {excess_lat:>14.6e} {delta_GR:>14.6e} {ratio:>10.5f}')
        L_rows.append({'L': L, 'ratio': ratio, 'excess_lat': excess_lat,
                       'delta_GR': delta_GR})
    out['stage2_L_scan'] = L_rows

    # The GR Shapiro log formula is itself sensitive to the finite ray
    # endpoints (r_1, r_2, r_12), so both Δt_lat and Δt_GR use the SAME
    # finite geometry — the ratio is the meaningful comparison and should
    # → 1 regardless of truncation, because both sides see the same r's.
    print()
    print('=' * 70)
    print('GATE EVALUATION')
    print('=' * 70)
    ratio_final = L_rows[-1]['ratio']
    print(f'  Ratio Δt_lat/Δt_GR at L=192, b=8: {ratio_final:.5f}')
    print(f'  |ratio − 1|:                       {abs(ratio_final-1.0)*100:.2f}%')
    # Compare to the periodic-kernel result (0.5–0.62)
    print(f'  (Periodic kernel gave ratio ≈ 0.47–0.62)')
    pass_5pct  = abs(ratio_final - 1.0) < 0.05
    pass_1pct  = abs(ratio_final - 1.0) < 0.01
    pass_01pct = abs(ratio_final - 1.0) < 0.001
    print(f'  → 5% gate:    {"PASS" if pass_5pct else "FAIL"}')
    print(f'  → 1% gate:    {"PASS" if pass_1pct else "FAIL"}')
    print(f'  → 0.1% gate:  {"PASS" if pass_01pct else "FAIL"}')
    out['gate'] = {
        'ratio_final': ratio_final,
        'rel_off_1': abs(ratio_final - 1.0),
        'pass_5pct': pass_5pct, 'pass_1pct': pass_1pct,
        'pass_01pct': pass_01pct,
    }

    out_path = os.path.join(THIS, '..', '..', 'test-results',
                             'top10_T05b_GR2_openBC.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults written to {out_path}')
    return out


if __name__ == '__main__':
    main()
