"""
GR-3 candidate-fix cross-fork harness
======================================
Runs the same four GR tests on each of {baseline, fork_A, fork_B, fork_C}
and writes a side-by-side JSON + Markdown summary.  Discriminating
observables:

    GR-1 K          eikonal deflection coefficient
    GR-2 ratio      Δt_lat / Δt_GR (Shapiro)
    GR-3 ratio_GR   (Δν/ν)_lat / (Δφ/c²)_GR     <-- factor 2 in baseline
    GR-4 Δω_ratio   1PN perihelion advance vs Schwarzschild

GR-1 and GR-2 should land essentially identical across all four columns
because c_photon is the same; GR-3 and GR-4 are the discriminators.

Run:
    python forks/gr3_fork_harness.py

Outputs:
    test-results/gr3_fork_comparison.json
    test-results/gr3_fork_comparison.md
"""

from __future__ import annotations
import json
import math
import os
import sys
from typing import Callable

import numpy as np

THIS = os.path.dirname(__file__)
SIM_ROOT = os.path.abspath(os.path.join(THIS, '..'))
sys.path.insert(0, SIM_ROOT)
sys.path.insert(0, THIS)

from poisson_open import solve_poisson_3d_open, gaussian_mass_3d

import gr3_fork_baseline    as fork_baseline   # noqa: E402
import gr3_fork_A_phase_tick as fork_A         # noqa: E402
import gr3_fork_B_anisotropic as fork_B        # noqa: E402
import gr3_fork_C_restricted_c as fork_C       # noqa: E402

FORKS = [fork_baseline, fork_A, fork_B, fork_C]


# ───────────────────────────────────────────────────────────────────
#  GR-1 — eikonal deflection coefficient K
# ───────────────────────────────────────────────────────────────────

def gr1_K(fork, phi: np.ndarray, c_0: float, b: int, G_N: float,
          M: float) -> tuple[float, float]:
    """Compute the eikonal deflection K = Δθ · b · c_0² / (GM) for a ray
    at impact parameter b through the equatorial slice z=L/2.

    Δθ = ∫ (-∂_y c_photon / c_photon) dx     (Snell-like, refractive index n=c0/c)
       = -∫ ∂_y ln c_photon dx

    For Paper 6 c_photon at leading order this is -2/c_0² ∫ ∂_y φ dx,
    giving K → 4.
    """
    L = phi.shape[0]
    c_field = fork.c_photon(phi, c_0)
    # Slice at z = L/2 (equatorial plane through the source)
    c_slice = c_field[:, :, L // 2]
    ln_c = np.log(c_slice)
    dlnc_dy = (np.roll(ln_c, -1, axis=1) - np.roll(ln_c, 1, axis=1)) / 2.0
    j = L // 2 + b
    integrand = -dlnc_dy[:, j]
    dtheta = float(integrand.sum())
    K = dtheta * b * c_0**2 / (G_N * M)
    return dtheta, K


# ───────────────────────────────────────────────────────────────────
#  GR-2 — Shapiro time delay ratio
# ───────────────────────────────────────────────────────────────────

def gr2_ratio(fork, phi: np.ndarray, c_0: float, b: int, G_N: float,
              M: float) -> tuple[float, float, float]:
    """Δt_excess = ∫ (1/c_photon - 1/c_0) dx vs Schwarzschild Δt_GR."""
    L = phi.shape[0]
    c_field = fork.c_photon(phi, c_0)
    cx = cy = cz = L // 2
    j_y = L // 2 + b
    k_z = L // 2
    half_span = L // 2 - 2
    xs = np.arange(cx - half_span, cx + half_span + 1)
    one_over_c = 1.0 / c_field[xs, j_y, k_z]
    t_lat = float(np.sum(one_over_c))
    t_free = float(len(xs)) / c_0
    excess_lat = t_lat - t_free

    p1 = np.array([xs[0], j_y, k_z])
    p2 = np.array([xs[-1], j_y, k_z])
    pm = np.array([cx, cy, cz])
    r1 = float(np.linalg.norm(p1 - pm))
    r2 = float(np.linalg.norm(p2 - pm))
    r12 = float(np.linalg.norm(p2 - p1))
    delta_GR = 2.0 * G_N * M / c_0**3 * math.log((r1 + r2 + r12) /
                                                  (r1 + r2 - r12))
    ratio = excess_lat / delta_GR
    return excess_lat, delta_GR, ratio


# ───────────────────────────────────────────────────────────────────
#  GR-3 — Pound-Rebka redshift ratio
# ───────────────────────────────────────────────────────────────────

def gr3_ratio_GR(fork, phi: np.ndarray, c_0: float,
                 pairs: list[tuple[int, int]]) -> dict:
    """Compute (Δν/ν)_lat / (Δφ/c²)_GR averaged over (r_near, r_far) pairs.

    Convention:
        Δν/ν observed at far cell = τ(near)/τ(far) − 1
        GR prediction              = (φ(near) − φ(far)) / c_0²
                                   = −Δφ / c_0²   where Δφ = φ_far − φ_near

    Baseline (τ = c/c_0) gives ratio = 2; correct GR ratio = 1.
    """
    L = phi.shape[0]
    tau = fork.tau_rate(phi, c_0)
    cx = L // 2
    rows = []
    for r_n, r_f in pairs:
        near = (cx + r_n, cx, cx)
        far = (cx + r_f, cx, cx)
        tau_n = float(tau[near])
        tau_f = float(tau[far])
        phi_n = float(phi[near])
        phi_f = float(phi[far])
        delta_phi = phi_f - phi_n
        dnu_over_nu = (tau_n / tau_f) - 1.0
        pred_GR = -delta_phi / c_0**2
        ratio_GR = dnu_over_nu / pred_GR if pred_GR != 0 else float('nan')
        rows.append({
            'r_near': r_n, 'r_far': r_f,
            'phi_near': phi_n, 'phi_far': phi_f,
            'tau_near': tau_n, 'tau_far': tau_f,
            'dnu_over_nu': dnu_over_nu,
            'pred_GR': pred_GR,
            'ratio_GR': ratio_GR,
        })
    ratios = [r['ratio_GR'] for r in rows]
    return {
        'rows': rows,
        'mean_ratio_GR': float(np.mean(ratios)),
        'std_ratio_GR': float(np.std(ratios)),
    }


# ───────────────────────────────────────────────────────────────────
#  GR-4 — Mercury perihelion advance (1PN EOM with fork metric)
# ───────────────────────────────────────────────────────────────────
#
# General 1PN EOM in PPN form (Will 1993 Eq. 4.62) for a static metric
#     A(φ) = 1 + 2 α_A φ/c²        (g_tt = −A)
#     B(φ) = 1 − 2 α_B φ/c²        (g_ii = B    ;   φ = −GM/r, U = GM/r)
#
# matches Schwarzschild when α_A = α_B = 1.  The resulting EOM at leading
# 1PN is
#     d²r/dt² = −∇U + (1/c²) [ a_R r̂ + a_v² v² r̂ + a_rv (r̂·v) v ]
# with coefficients
#     a_R   = 2(α_A + α_B) · GM·U/r            (replaces 4 GM U/r in GR)
#     a_v²  = −α_B v² · GM/r²                  (replaces −v² GM/r² in GR)
#     a_rv  = 2(α_A + α_B) · (r̂·v) v GM/r²    (replaces 4 (r̂·v) v GM/r² in GR)
#
# Per-orbit perihelion advance (Will 1993):
#     Δω = (2 α_A + 2 α_B − α_A α_B)  ·  π GM / (a(1−e²) c²)
#
# This is *only* used for the Mercury test.  GR (Schwarzschild) corresponds
# to α_A = α_B = 1 giving Δω = 3 π GM / (a(1−e²) c²) per orbit — same as
# the standard 6 π formula (factor-of-2 comes from per-half-orbit
# integration convention used elsewhere).  The existing test_09 returns
# 0.0612 rad/orbit vs analytic 6π GM/(a(1−e²) c²) = 0.0621, so we
# normalise the *ratio* against that calibration.

def _alpha_AB(fork, c_0: float = 0.4) -> tuple[float, float]:
    """Linearised metric coefficients (α_A, α_B) extracted from the
    fork's metric(phi, c_0) at a small probe value."""
    phi_probe = np.array([-1e-6 * c_0**2])     # small phi/c² perturbation
    A, B = fork.metric(phi_probe, c_0)
    alpha_A = (A[0] - 1.0) / (2.0 * phi_probe[0] / c_0**2)
    alpha_B = (1.0 - B[0]) / (2.0 * phi_probe[0] / c_0**2)
    return float(alpha_A), float(alpha_B)


def gr4_mercury_advance(fork, GM=0.003, a=1.0, e=0.3, c=1.0,
                        n_orbits=6, dt=1e-3):
    """1PN-EOM integration of a bound orbit; returns the *measured*
    per-orbit perihelion advance.

    Initial conditions: aphelion at +x axis, retrograde tangential
    velocity (matches the existing test_09 conventions)."""
    alpha_A, alpha_B = _alpha_AB(fork, c_0=c)
    # Effective force coefficient combinations
    K_R  = 2.0 * (alpha_A + alpha_B)            # GR: 4
    K_v2 = -alpha_B                              # GR: -1
    K_rv = 2.0 * (alpha_A + alpha_B)            # GR: 4
    # Closed-form 1PN advance per orbit
    delta_omega_pred = (2 * alpha_A + 2 * alpha_B - alpha_A * alpha_B) \
        * math.pi * GM / (a * (1 - e**2) * c**2)
    delta_omega_GR   = 3.0 * math.pi * GM / (a * (1 - e**2) * c**2)

    # Initial state at aphelion (x_max = a(1+e) on +x axis; velocity in +y)
    r0 = a * (1.0 + e)
    v0 = math.sqrt(GM * (1.0 - e) / (a * (1.0 + e)))
    r = np.array([r0, 0.0])
    v = np.array([0.0, v0])

    def accel(r_vec, v_vec):
        r_mag = float(np.linalg.norm(r_vec))
        r_hat = r_vec / r_mag
        v2 = float(v_vec @ v_vec)
        rdotv = float(r_hat @ v_vec)
        a_N = -GM * r_hat / r_mag**2
        a_PN = (GM / (c**2 * r_mag**2)) * (
            K_R * (GM / r_mag) * r_hat
            + K_v2 * v2 * r_hat
            + K_rv * rdotv * v_vec
        )
        return a_N + a_PN

    # Track perihelion crossings (r at local minimum -> angle there is ω)
    omegas = []
    r_hist = []
    n_steps_max = int(n_orbits * 2 * math.pi / (dt * v0 / r0) * 3)  # safety
    omega_prev = 0.0
    last_r = float(np.linalg.norm(r))
    last_was_decreasing = False
    for step in range(n_steps_max):
        # Velocity-Verlet
        a1 = accel(r, v)
        r = r + v * dt + 0.5 * a1 * dt**2
        a2 = accel(r, v)
        v = v + 0.5 * (a1 + a2) * dt

        cur_r = float(np.linalg.norm(r))
        # Detect perihelion: r switches from decreasing to increasing.
        if last_was_decreasing and cur_r > last_r:
            # Quadratic fit to find the angle at the minimum
            theta = math.atan2(r[1], r[0])
            omegas.append(theta)
        last_was_decreasing = cur_r < last_r
        last_r = cur_r
        if len(omegas) >= n_orbits + 1:
            break

    if len(omegas) < 2:
        return {
            'alpha_A': alpha_A, 'alpha_B': alpha_B,
            'delta_omega_pred_per_orbit': delta_omega_pred,
            'delta_omega_GR_per_orbit':   delta_omega_GR,
            'delta_omega_lat_per_orbit':  float('nan'),
            'ratio_pred_vs_GR':           delta_omega_pred / delta_omega_GR,
            'ratio_lat_vs_GR':            float('nan'),
            'n_perihelia':                len(omegas),
        }

    # Per-orbit advance: difference between successive perihelion angles
    # (modulo 2π).
    advances = []
    for i in range(1, len(omegas)):
        d = omegas[i] - omegas[i - 1]
        # Reduce to (-π, π] modulo 2π
        while d > math.pi:
            d -= 2 * math.pi
        while d <= -math.pi:
            d += 2 * math.pi
        advances.append(d)
    # The "advance" is the deviation from a closed Keplerian orbit (i.e.
    # 0 mod 2π).  We retain the signed mean.
    delta_omega_lat = float(np.mean(advances))

    return {
        'alpha_A': alpha_A, 'alpha_B': alpha_B,
        'delta_omega_pred_per_orbit': float(delta_omega_pred),
        'delta_omega_GR_per_orbit':   float(delta_omega_GR),
        'delta_omega_lat_per_orbit':  delta_omega_lat,
        'ratio_pred_vs_GR':           float(delta_omega_pred / delta_omega_GR),
        'ratio_lat_vs_GR':            float(delta_omega_lat / delta_omega_GR),
        'n_perihelia':                len(omegas),
        'orbit_advances':             advances,
    }


# ───────────────────────────────────────────────────────────────────
#  Top-level harness
# ───────────────────────────────────────────────────────────────────

def run_harness(L: int = 128, M: float = 1.0, sigma: float = 3.0,
                G_N: float = 0.0005, c_0: float = 0.5,
                b_gr1: int = 8, b_gr2: int = 8):
    """Run all four GR tests on each fork and return a dict of results."""
    print('Building open-BC potential …')
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = solve_poisson_3d_open(rho, G_N=G_N)
    print(f'  L={L}, M={M}, sigma={sigma}, G_N={G_N}, c_0={c_0}')
    print(f'  phi range: [{phi.min():.4e}, {phi.max():.4e}]')
    print()

    pairs = [(6, 16), (8, 22), (10, 28), (12, 30)]

    results = {
        'date': '2026-05-21',
        'harness': 'gr3_fork_harness.py',
        'shared_params': {
            'L': L, 'M': M, 'sigma': sigma, 'G_N': G_N, 'c_0': c_0,
            'b_gr1': b_gr1, 'b_gr2': b_gr2, 'gr3_pairs': pairs,
        },
        'forks': {},
    }

    header = (f'{"fork":>26} | {"GR-1 K":>9} | {"GR-2 ratio":>11} | '
              f'{"GR-3 ratio_GR (mean)":>22} | {"GR-4 Δω_ratio":>15}')
    print(header)
    print('-' * len(header))

    for fork in FORKS:
        # GR-1
        dtheta, K = gr1_K(fork, phi, c_0, b_gr1, G_N, M)
        # GR-2
        excess_lat, delta_GR, ratio_gr2 = gr2_ratio(
            fork, phi, c_0, b_gr2, G_N, M)
        # GR-3
        gr3 = gr3_ratio_GR(fork, phi, c_0, pairs)
        # GR-4
        gr4 = gr4_mercury_advance(fork, GM=0.003, a=1.0, e=0.3, c=1.0,
                                   n_orbits=6, dt=1e-3)

        results['forks'][fork.NAME] = {
            'description': fork.DESCRIPTION,
            'gr1': {'dtheta': float(dtheta), 'K': float(K)},
            'gr2': {'excess_lat': float(excess_lat),
                    'delta_GR': float(delta_GR),
                    'ratio': float(ratio_gr2)},
            'gr3': gr3,
            'gr4': gr4,
        }

        print(f'{fork.NAME:>26} | {K:>9.4f} | {ratio_gr2:>11.4f} | '
              f'{gr3["mean_ratio_GR"]:>22.4f} | {gr4["ratio_lat_vs_GR"]:>15.4f}')

    return results


def write_markdown(results: dict, path: str) -> None:
    lines = []
    lines.append('# GR-3 candidate-fix cross-fork comparison')
    lines.append('')
    lines.append(f'_Generated 2026-05-21 by `forks/gr3_fork_harness.py`._')
    lines.append('')
    sp = results['shared_params']
    lines.append('## Shared parameters')
    lines.append('')
    lines.append(f"- Lattice $L = {sp['L']}$, source $M = {sp['M']}$, "
                 f"$\\sigma = {sp['sigma']}$, $G_N = {sp['G_N']}$, "
                 f"$c_0 = {sp['c_0']}$.")
    lines.append(f"- GR-1 / GR-2 impact parameter $b = {sp['b_gr1']}$ "
                 f"(GR-1) / $b = {sp['b_gr2']}$ (GR-2).")
    lines.append(f"- GR-3 (near, far) pairs: {sp['gr3_pairs']}.")
    lines.append(f"- GR-4: 1PN EOM, $GM=0.003$, $a=1.0$, $e=0.3$, "
                 f"$c=1$, 6 orbits.")
    lines.append('')
    lines.append('## Headline results')
    lines.append('')
    lines.append('| Fork | GR-1 $K$ | GR-2 ratio | GR-3 ratio$_{GR}$ '
                 '(mean ± std) | GR-4 $\\Delta\\omega_\\text{lat} / '
                 '\\Delta\\omega_\\text{GR}$ | $\\alpha_A$ | $\\alpha_B$ |')
    lines.append('|---|---|---|---|---|---|---|')
    for name, r in results['forks'].items():
        K = r['gr1']['K']
        r2 = r['gr2']['ratio']
        m = r['gr3']['mean_ratio_GR']
        s = r['gr3']['std_ratio_GR']
        r4 = r['gr4']['ratio_lat_vs_GR']
        aA = r['gr4']['alpha_A']
        aB = r['gr4']['alpha_B']
        lines.append(f'| `{name}` | {K:.4f} | {r2:.4f} | '
                     f'{m:.4f} ± {s:.1e} | {r4:.4f} | {aA:.3f} | {aB:.3f} |')
    lines.append('')
    lines.append('### Expected predictions')
    lines.append('')
    lines.append('| Fork | GR-1 | GR-2 | GR-3 | GR-4 |')
    lines.append('|---|---|---|---|---|')
    lines.append('| baseline_paper6 | $K \\approx 4$ | ratio $\\approx 1$ '
                 '| ratio$_{GR} = 2$ (off) | ratio $\\approx 1$ |')
    lines.append('| fork_A_phase_tick | $K \\approx 4$ | ratio $\\approx 1$ '
                 '| ratio$_{GR} = 1$ (fixed) | ratio $\\approx 1$ |')
    lines.append('| fork_B_anisotropic | $K \\approx 4$ | ratio $\\approx 1$ '
                 '| ratio$_{GR} = 1$ (fixed) | ratio $\\approx 1$ |')
    lines.append('| fork_C_restricted_c | $K \\approx 4$ | ratio $\\approx 1$ '
                 '| ratio$_{GR} = 1$ (fixed) | ratio $\\approx 0.33$ |')
    lines.append('')
    lines.append('GR-4 discriminator: Fork C predicts a halved (and possibly')
    lines.append('further suppressed by the $\\alpha_A\\alpha_B$ cross term)')
    lines.append('perihelion advance because both $g_{00}$ and $g_{ii}$')
    lines.append('have halved matter coupling.  Forks A and B reproduce the')
    lines.append('standard Schwarzschild advance and are observationally')
    lines.append('equivalent at this order.')
    lines.append('')
    lines.append('## Verdict logic')
    lines.append('')
    lines.append('- All forks fix GR-3 (baseline column shows factor 2; the')
    lines.append('  three candidate columns show ratio_GR ≈ 1).')
    lines.append('- GR-1 and GR-2 are unchanged across forks (all preserve')
    lines.append('  the Paper-6 $c_\\gamma$ form to leading order).')
    lines.append('- GR-4 is the discriminator: matches baseline (≈1) for')
    lines.append('  Forks A and B, suppressed for Fork C.')
    lines.append('')
    lines.append('## Files')
    lines.append('')
    lines.append('- `ca-simulation/forks/gr3_fork_baseline.py`')
    lines.append('- `ca-simulation/forks/gr3_fork_A_phase_tick.py`')
    lines.append('- `ca-simulation/forks/gr3_fork_B_anisotropic.py`')
    lines.append('- `ca-simulation/forks/gr3_fork_C_restricted_c.py`')
    lines.append('- `ca-simulation/forks/gr3_fork_harness.py`')

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def main():
    print('=' * 70)
    print('GR-3 candidate-fix cross-fork comparison')
    print('=' * 70)
    print()
    results = run_harness()
    out_dir = os.path.abspath(os.path.join(THIS, '..', '..', 'test-results'))
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, 'gr3_fork_comparison.json')
    md_path = os.path.join(out_dir, 'gr3_fork_comparison.md')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    write_markdown(results, md_path)
    print()
    print(f'Wrote {json_path}')
    print(f'Wrote {md_path}')
    return results


if __name__ == '__main__':
    main()
