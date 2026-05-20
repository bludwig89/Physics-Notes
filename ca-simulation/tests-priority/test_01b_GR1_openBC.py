"""
GR-1 Stage A re-test with OPEN-BOUNDARY Poisson kernel
=======================================================
Date: 2026-05-19 - 22:53

Replaces the periodic FFT-Poisson in test_01_GR1_light_deflection.py
with the James/Hockney zero-padded FFT solver in poisson_open.py.

Test the same eikonal ray-tracer integral
    K = Δθ · b · c_0² / (GM)
on a Gaussian point mass at the centre of the box, now with the
true *free-space* 1/r potential instead of the periodic-cell sum.

Expected: |K| → 4 (Einstein) as L grows (no PBC suppression).
"""

import os, sys, math, json
import numpy as np

THIS = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(THIS, '..')))

from poisson_open import solve_poisson_3d_open, gaussian_mass_3d


def eikonal_K(L, M=1.0, b=18, sigma=6.0, G_N=0.005, c_0=0.4, factor=2.0):
    """Eikonal deflection coefficient K = Δθ · b · c_0² / (GM)
    using the *open-BC* Newtonian Poisson kernel."""
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = solve_poisson_3d_open(rho, G_N=G_N)
    phi_slice = phi[:, :, L//2]
    dphi_dy = (np.roll(phi_slice, -1, axis=1) -
               np.roll(phi_slice, 1, axis=1)) / 2.0
    j = L // 2 + b
    # Use the full x range along the ray
    integrand = -factor * dphi_dy[:, j] / c_0**2
    dtheta = float(integrand.sum())
    K = dtheta * b * c_0**2 / (G_N * M)
    return dtheta, K


def main():
    print('=' * 70)
    print('GR-1 Stage A — OPEN-BC Poisson kernel re-test')
    print('=' * 70)
    print('Date 2026-05-19 - 22:53')
    print()
    out = {'date': '2026-05-19 - 22:53',
           'test': 'GR-1 Stage A (open BC)',
           'kernel': 'James/Hockney zero-padded FFT-Poisson'}

    # Stage 1: linear-in-M check at L=96
    print('Stage 1: scan M at L=96, b=18')
    print(f'{"M":>6} {"Δθ":>14} {"K = Δθ·b·c²/(GM)":>22}')
    Ks = []
    for M in [0.5, 1.0, 2.0, 4.0]:
        dtheta, K = eikonal_K(L=96, M=M, b=18, sigma=6.0,
                               G_N=0.005, c_0=0.4, factor=2.0)
        Ks.append(K)
        print(f'{M:>6.2f} {dtheta:>14.6e} {K:>22.5f}')
    K_mean = float(np.mean(Ks))
    K_std  = float(np.std(Ks))
    print(f'\n  Mean K = {K_mean:.5f}, std = {K_std:.2e}')
    out['stage1_M_scan'] = {'Ks': Ks, 'mean': K_mean, 'std': K_std}

    # Stage 2: convergence in L holding *b* fixed (R/b → ∞ as L grows).
    # The asymptotic Einstein integral ∫∂_yφ dx from -∞ to +∞ has a finite-R
    # truncation factor R/√(R²+b²); at fixed b this → 1 as R = L/2 → ∞.
    print()
    print('Stage 2: convergence in L at fixed b=8, σ=3 (R/b → ∞)')
    print(f'{"L":>6} {"R/b":>6} {"R/√(R²+b²)":>12} {"K":>14} {"K/factor":>10}')
    K_L = []
    b_fix = 8
    sig_fix = 3.0
    for L in [64, 96, 128, 160, 192]:
        R = L / 2
        truncation = R / math.sqrt(R**2 + b_fix**2)
        dtheta, K = eikonal_K(L=L, M=1.0, b=b_fix, sigma=sig_fix,
                               G_N=0.005, c_0=0.4, factor=2.0)
        K_corrected = K / truncation
        K_L.append({'L': L, 'K': K, 'K_truncation_corrected': K_corrected,
                    'truncation': truncation})
        print(f'{L:>6d} {R/b_fix:>6.2f} {truncation:>12.6f} {K:>14.6f} {K_corrected:>10.4f}')
    out['stage2_L_scan'] = K_L

    # Stage 3: b scan at fixed L (sensitivity to ray geometry)
    print()
    print('Stage 3: b scan at L=128')
    print(f'{"b":>6} {"K":>14}')
    K_b = []
    for b in [10, 14, 18, 24, 30, 40]:
        dtheta, K = eikonal_K(L=128, M=1.0, b=b, sigma=6.0,
                               G_N=0.005, c_0=0.4, factor=2.0)
        K_b.append((b, K))
        print(f'{b:>6d} {K:>14.6f}')
    out['stage3_b_scan'] = K_b

    # Stage 4: control — factor=1 (Newtonian eikonal weight) at L=128
    print()
    print('Stage 4: control — factor=1 (Newtonian) at L=128, b=18')
    dtheta1, K1 = eikonal_K(L=128, M=1.0, b=18, sigma=6.0,
                             G_N=0.005, c_0=0.4, factor=1.0)
    print(f'  factor=1: K = {K1:.6f}  (expected ≈ K_einstein/2)')
    out['stage4_control_factor1'] = K1

    # ─── Gate ───
    print()
    print('=' * 70)
    print('GATE EVALUATION')
    print('=' * 70)
    K_final = K_L[-1]['K']
    K_corrected = K_L[-1]['K_truncation_corrected']
    K_mag = abs(K_final)
    K_mag_corr = abs(K_corrected)
    print(f'  Truncation-corrected |K| at L=256: {K_mag_corr:.4f}')
    print(f'  Final |K| at L=192:                  {K_mag:.4f}')
    print(f'  Einstein prediction:                  4.0')
    print(f'  Newtonian prediction:                 2.0')
    print(f'  ||K| - 4|/4:                          {abs(K_mag - 4.0)/4.0*100:.2f}%')
    print(f'  ||K| - 2|/2:                          {abs(K_mag - 2.0)/2.0*100:.2f}%')
    pass_10pct = abs(K_mag_corr - 4.0) / 4.0 < 0.10
    pass_5pct  = abs(K_mag_corr - 4.0) / 4.0 < 0.05
    pass_1pct  = abs(K_mag_corr - 4.0) / 4.0 < 0.01
    print(f'  ||K_corr| - 4|/4:                     {abs(K_mag_corr - 4.0)/4.0*100:.3f}%')
    print(f'  → GR-1 Stage A 10% Einstein gate:    {"PASS" if pass_10pct else "FAIL"}')
    print(f'  → 5% gate:                            {"PASS" if pass_5pct else "FAIL"}')
    print(f'  → 1% gate:                            {"PASS" if pass_1pct else "FAIL"}')

    out['gate'] = {
        'K_final_abs': K_mag,
        'K_corrected_abs': K_mag_corr,
        'rel_off_einstein_corrected': abs(K_mag_corr - 4.0) / 4.0,
        'pass_10pct': pass_10pct,
        'pass_5pct':  pass_5pct,
        'pass_1pct':  pass_1pct,
    }

    out_path = os.path.join(THIS, '..', '..', 'test-results',
                             'top10_T01b_GR1_openBC.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults written to {out_path}')
    return out


if __name__ == '__main__':
    main()
