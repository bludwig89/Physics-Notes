"""
Top-10 priority Test #5 — GR-2: absolute Shapiro time delay
============================================================
Date: 2026-05-19

Goal
----
Compare lattice-computed Shapiro delay against the closed-form GR expression
    Δt = (2GM/c³) · log[(r_1 + r_2 + r_12)/(r_1 + r_2 − r_12)]
to 0.1% in the weak-field regime r_s/b ≤ 1e-3.

Note on coupling
----------------
The Paper 6 effective-medium form c(x) = c_0/(1 − 2φ/c_0²) gives an
isotropic refractive index n(x) = c_0/c(x).  The light propagation time
through this index from r_1 to r_2 is

    Δt_lat = ∫ (c_0/c(x)) dℓ / c_0  =  ∫ (1 − 2φ/c_0²) dℓ / c_0

vs. the free-space time Δt_0 = |r_12|/c_0.  The excess delay is
    Δt_lat − Δt_0  =  −2/c_0² · ∫ φ dℓ

For a Newtonian point mass φ(r) = −GM/r and a ray of impact parameter b
running from x = −R to x = +R (with R ≫ b), the integral evaluates to
    ∫ φ dℓ  =  −GM · log[(R + √(R² + b²))² / b²]
             =  −2GM · log[(R + √(R²+b²)) / b]

so
    Δt_lat − Δt_0  =  (4GM/c_0²) · log[(R + √(R²+b²)) / b]   (lattice)
    Δt_GR  − Δt_0  =  (2GM/c_0³) · log[(r_1+r_2+r_12)/(r_1+r_2-r_12)]
                    ≈ (4GM/c_0³) · log[(R + √(R²+b²)) / b]    (asymptotic, r=R, r_12=2R)

Wait — careful with the c³ vs c² distinction.  Δt has units of time;
GM/c³ has units of time; ∫φ dℓ has units (m/s²)·m = (m²/s²).  Need to
divide by c³ for the latter to give time.  Let's redo:

Light path:  along ℓ at constant velocity ~ c_0 (1 − 2φ/c_0²).  Time per
distance is  dt/dℓ = 1/c = (1 − 2φ/c_0²)/c_0.  Total excess time over
free space:  −(2/c_0³) · ∫ φ dℓ.  For φ = −GM/r this gives
  Δt_excess = (2GM/c_0³) · ∫(1/r)dℓ.

The integral ∫dℓ/√(b² + (x − x₀)²) from x = −R to x = R is
  2 sinh⁻¹(R/b)  =  2 log[(R + √(R² + b²)) / b]

So  Δt_excess_lat = (4GM/c_0³) · log[(R + √(R² + b²))/b].

And  Δt_excess_GR = (2GM/c_0³) · log[(r_1 + r_2 + r_12)/(r_1 + r_2 − r_12)].

For a symmetric trajectory r_1 = r_2 = R, r_12 = 2R, both expressions give
  Δt_GR  = (2GM/c_0³) · log[(2R + 2R)/(2R − 2R)] → diverges.

The GR formula is for r_12 < r_1 + r_2.  For a ray with impact parameter b
passing close to mass, with r_1 = r_2 = R and the closest approach b ≪ R,
we have r_12 = 2√(R² − b²) ≈ 2R(1 − b²/(2R²)).  Then:
  (r_1+r_2+r_12)/(r_1+r_2−r_12) = (2R + 2R(1-b²/(2R²)))/(2R - 2R(1-b²/(2R²)))
                                = (4R − Rb²/R)/(b²/R) = (4R² − b²)/b² ≈ 4R²/b²
  log ≈ 2·log(2R/b)
  Δt_GR ≈ (2GM/c_0³) · 2·log(2R/b)  =  (4GM/c_0³)·log(2R/b)

The lattice form:
  Δt_lat ≈ (4GM/c_0³)·log((R + R)/b) = (4GM/c_0³)·log(2R/b)

They agree exactly in the asymptotic limit R ≫ b.

Gate (from roadmap): 0.1% absolute residual at r_s/b ≤ 1e-3.

Implementation
--------------
Direct numerical line integral of (1/c(x))·dℓ for a straight ray of
impact parameter b through a Gaussian-mass potential.  Compare to the
analytic GR formula evaluated at the same (r_1, r_2, r_12).
"""

import os, sys, math, json
import numpy as np

THIS = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(THIS, '..')))


def gaussian_mass_3d(L, M=1.0, sigma=3.0, center=None):
    if center is None: center = (L//2, L//2, L//2)
    x = np.arange(L) - center[0]
    y = np.arange(L) - center[1]
    z = np.arange(L) - center[2]
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    rho = np.exp(-(X**2 + Y**2 + Z**2) / (2*sigma**2))
    rho *= M / rho.sum()
    return rho


def solve_poisson_3d(rho, G=1.0):
    Lx, Ly, Lz = rho.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    kz = np.fft.fftfreq(Lz) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
    k2 = KX**2 + KY**2 + KZ**2
    k2[0,0,0] = 1.0
    rho_k = np.fft.fftn(rho)
    phi_k = -4.0 * np.pi * G * rho_k / k2
    phi_k[0,0,0] = 0.0
    return np.fft.ifftn(phi_k).real


def shapiro_delay_lattice(L, M, sigma, G, c_0, b, x_start, x_end):
    """Compute Shapiro delay by integrating 1/c(x) along a straight ray
    at impact parameter b above the center of the mass at L/2.

    Returns (Δt_lat_excess, Δt_GR_excess, r_1, r_2, r_12, M_eff)."""
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = solve_poisson_3d(rho, G=G)
    c_field = c_0 / (1.0 - 2.0 * phi / c_0**2)

    # Ray runs along +x at y = L/2 + b, z = L/2
    j_y = L//2 + b
    k_z = L//2
    # Lattice cells along the ray
    xs = np.arange(x_start, x_end + 1)
    # 1/c at each cell along the path
    one_over_c = 1.0 / c_field[xs, j_y, k_z]
    # Total ray time
    t_lat = float(np.sum(one_over_c))
    # Free-space time
    t_free = float(len(xs)) / c_0
    excess_lat = t_lat - t_free

    # Geometric quantities, taking the mass center at (L/2, L/2, L/2)
    cx, cy, cz = L//2, L//2, L//2
    p_start = np.array([x_start, j_y, k_z])
    p_end   = np.array([x_end,   j_y, k_z])
    p_mass  = np.array([cx, cy, cz])
    r_1  = float(np.linalg.norm(p_start - p_mass))
    r_2  = float(np.linalg.norm(p_end   - p_mass))
    r_12 = float(np.linalg.norm(p_end   - p_start))

    # GR Shapiro formula
    # Δt = (2GM/c³) · log[(r_1+r_2+r_12)/(r_1+r_2-r_12)]
    # Use M_eff = M (the integrated mass)
    arg_num = r_1 + r_2 + r_12
    arg_den = r_1 + r_2 - r_12
    if arg_den < 1e-12:
        return None
    delta_GR = 2.0 * G * M / c_0**3 * math.log(arg_num / arg_den)
    return excess_lat, delta_GR, r_1, r_2, r_12


def main():
    print('=' * 70)
    print('GR-2 — absolute Shapiro time delay')
    print('=' * 70)
    print('Date 2026-05-19')
    print()
    out = {'date': '2026-05-19', 'test': 'GR-2 Shapiro absolute'}

    L = 128
    M = 1.0
    sigma = 4.0
    G = 0.0005   # weaker field for cleaner weak-field
    c_0 = 0.5

    print(f'  L={L}, M={M}, sigma={sigma}, G={G}, c_0={c_0}')
    print()
    print(f'{"b":>4} {"Δt_lat":>14} {"Δt_GR":>14} {"ratio":>10} {"rel_resid":>12}')
    print('-' * 60)
    rows = []
    for b in [6, 10, 16, 24]:
        # Ray spans from x = L/2 - 40 to L/2 + 40
        x_start = L//2 - 40
        x_end   = L//2 + 40
        result = shapiro_delay_lattice(L, M, sigma, G, c_0, b, x_start, x_end)
        if result is None: continue
        excess_lat, delta_GR, r_1, r_2, r_12 = result
        ratio = excess_lat / delta_GR if delta_GR != 0 else float('inf')
        rel = abs(excess_lat - delta_GR) / abs(delta_GR) if delta_GR != 0 else 0
        rows.append({'b': b, 'excess_lat': excess_lat, 'delta_GR': delta_GR,
                     'ratio': ratio, 'rel_residual': rel,
                     'r_1': r_1, 'r_2': r_2, 'r_12': r_12})
        print(f'{b:>4d} {excess_lat:>14.6e} {delta_GR:>14.6e} {ratio:>10.5f} {rel:>12.4e}')

    out['rows'] = rows

    print()
    # The ratio should be 1 (within finite-L effects).
    # If it's 2, that's the Paper 6 effective-medium "factor 2" issue
    # (consistent with GR-3 outcome).
    mean_ratio = float(np.mean([r['ratio'] for r in rows]))
    print(f'  Mean ratio Δt_lat / Δt_GR = {mean_ratio:.5f}')
    print()
    print('=' * 70)
    print('GATE EVALUATION')
    print('=' * 70)
    deviation = abs(mean_ratio - 1.0)
    print(f'  Lattice/GR ratio = {mean_ratio:.5f}')
    print(f'  |ratio − 1| =     {deviation:.4e}')
    pass_01 = deviation < 1e-3
    print(f'  → GR-2 0.1% gate: {"PASS" if pass_01 else "FAIL"}')
    # If ratio ≈ 2, that's the c(x) factor-2 effective-medium scaling
    if abs(mean_ratio - 2.0) < 0.1:
        print(f'\n  Note: ratio ≈ 2 — consistent with Paper 6 c(x) effective-medium')
        print(f'  giving a factor-of-2 over GR (see GR-3 result).')
    out['gate'] = {'mean_ratio': mean_ratio, 'deviation_from_1': deviation,
                   'pass_1em3': pass_01}

    out_path = os.path.join(THIS, '..', '..', 'test-results',
                             'top10_T05_GR2_shapiro.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults written to {out_path}')
    return out


if __name__ == '__main__':
    main()
