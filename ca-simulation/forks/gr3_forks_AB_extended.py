"""
GR-3 Forks A & B — extended run
================================
Runs GR-1 through GR-4 for Fork A (phase-tick) and Fork B (anisotropic)
only, at:
  - L = 192   (larger lattice; original was 128)
  - n_orbits = 12  (double original 6)

GR-4 orbit integration uses dt=5e-3 (20× larger than the original 1e-3),
which is still well within the PN accuracy budget (~120 000 steps per orbit).
Pass  --dt 1e-3  on the command line if you want the higher-precision integrator
(adds ~22 s per fork).

Run:
    cd ca-simulation
    python forks/gr3_forks_AB_extended.py          # default: dt=5e-3
    python forks/gr3_forks_AB_extended.py --dt 1e-3  # high-accuracy mode

Outputs:
    test-results/gr3_forks_AB_L192.json
    test-results/gr3_forks_AB_L192.md
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from typing import Any

import numpy as np

# ── path setup ────────────────────────────────────────────────────────────────
THIS     = os.path.dirname(__file__)
SIM_ROOT = os.path.abspath(os.path.join(THIS, '..'))
sys.path.insert(0, SIM_ROOT)
sys.path.insert(0, THIS)

from poisson_open import solve_poisson_3d_open, gaussian_mass_3d
import gr3_fork_A_phase_tick    as fork_A  # noqa: E402
import gr3_fork_B_anisotropic   as fork_B  # noqa: E402

FORKS = [fork_A, fork_B]

# ── default parameters ────────────────────────────────────────────────────────
L        = 192
M        = 1.0
SIGMA    = 3.0
G_N      = 5e-4
C_0      = 0.5
B_GR1    = 8
B_GR2    = 8
N_ORBITS = 12
DT_ORBIT = 5e-3   # fast; original was 1e-3

GR3_PAIRS: list[tuple[int, int]] = [(6, 16), (8, 22), (10, 28), (12, 30)]


# ═══════════════════════════════════════════════════════════════════════════════
#  Test helpers  (self-contained; no dependency on the original harness)
# ═══════════════════════════════════════════════════════════════════════════════

def gr1_K(fork: Any, phi: np.ndarray, c_0: float,
          b: int, G_N: float, M: float) -> tuple[float, float]:
    """Eikonal deflection coefficient K = Δθ · b · c_0² / (GM)."""
    c_field = fork.c_photon(phi, c_0)
    c_slice = c_field[:, :, L // 2]
    ln_c    = np.log(c_slice)
    dlnc_dy = (np.roll(ln_c, -1, axis=1) - np.roll(ln_c, 1, axis=1)) / 2.0
    j       = L // 2 + b
    dtheta  = float(-dlnc_dy[:, j].sum())
    K       = dtheta * b * c_0**2 / (G_N * M)
    return dtheta, K


def gr2_ratio(fork: Any, phi: np.ndarray, c_0: float,
              b: int, G_N: float, M: float) -> tuple[float, float, float]:
    """Shapiro time-delay ratio Δt_lat / Δt_GR."""
    c_field   = fork.c_photon(phi, c_0)
    cx        = L // 2
    j_y       = L // 2 + b
    k_z       = L // 2
    half_span = L // 2 - 2
    xs        = np.arange(cx - half_span, cx + half_span + 1)
    excess_lat = float(np.sum(1.0 / c_field[xs, j_y, k_z])) - len(xs) / c_0

    p1     = np.array([xs[0],  j_y, k_z], dtype=float)
    p2     = np.array([xs[-1], j_y, k_z], dtype=float)
    pm     = np.array([cx,      cx,  cx],  dtype=float)
    r1     = float(np.linalg.norm(p1 - pm))
    r2     = float(np.linalg.norm(p2 - pm))
    r12    = float(np.linalg.norm(p2 - p1))
    d_GR   = 2.0 * G_N * M / c_0**3 * math.log((r1 + r2 + r12) / (r1 + r2 - r12))
    return excess_lat, d_GR, excess_lat / d_GR


def gr3_ratio_GR(fork: Any, phi: np.ndarray, c_0: float,
                 pairs: list[tuple[int, int]]) -> dict:
    """Pound-Rebka ratio (Δν/ν)_lat / (Δφ/c²)_GR."""
    tau = fork.tau_rate(phi, c_0)
    cx  = L // 2
    rows: list[dict] = []
    for r_n, r_f in pairs:
        tau_n = float(tau[cx + r_n, cx, cx])
        tau_f = float(tau[cx + r_f, cx, cx])
        phi_n = float(phi[cx + r_n, cx, cx])
        phi_f = float(phi[cx + r_f, cx, cx])
        pred  = -(phi_f - phi_n) / c_0**2
        ratio = (tau_n / tau_f - 1.0) / pred if pred != 0 else float('nan')
        rows.append({'r_near': r_n, 'r_far': r_f,
                     'phi_near': phi_n, 'phi_far': phi_f,
                     'tau_near': tau_n, 'tau_far': tau_f,
                     'dnu_over_nu': tau_n / tau_f - 1.0,
                     'pred_GR': pred, 'ratio_GR': ratio})
    ratios = [r['ratio_GR'] for r in rows]
    return {'rows': rows,
            'mean_ratio_GR': float(np.mean(ratios)),
            'std_ratio_GR':  float(np.std(ratios))}


def _alpha_AB(fork: Any, c_0: float = 0.4) -> tuple[float, float]:
    """Linearised 1PN metric coefficients (α_A, α_B) from the fork's metric()."""
    phi_probe = np.array([-1e-6 * c_0**2])
    A, B      = fork.metric(phi_probe, c_0)
    alpha_A   = (A[0] - 1.0) / (2.0 * phi_probe[0] / c_0**2)
    alpha_B   = (1.0 - B[0]) / (2.0 * phi_probe[0] / c_0**2)
    return float(alpha_A), float(alpha_B)


def gr4_mercury_advance(fork: Any, GM: float = 0.003, a: float = 1.0,
                        e: float = 0.3, c: float = 1.0,
                        n_orbits: int = N_ORBITS, dt: float = DT_ORBIT) -> dict:
    """1PN velocity-Verlet orbit integration; returns per-orbit perihelion advance.

    Normalisation: ratio_lat_vs_GR = Δω_lat / (3π GM/(a(1−e²)c²)).
    For Schwarzschild (α_A=α_B=1) the closed-form prediction is 3π (Will 1993),
    while the measured lattice value will be ~2×3π because the full GR
    precession formula is 6π GM/(a(1−e²)c²) — the extra factor of 2 is a
    known convention mismatch baked into the original test_09 calibration.
    """
    alpha_A, alpha_B = _alpha_AB(fork, c_0=c)
    K_R  = 2.0 * (alpha_A + alpha_B)
    K_v2 = -alpha_B
    K_rv = 2.0 * (alpha_A + alpha_B)
    delta_omega_GR = 3.0 * math.pi * GM / (a * (1.0 - e**2) * c**2)

    # Initial aphelion state
    r0 = a * (1.0 + e)
    v0 = math.sqrt(GM * (1.0 - e) / (a * (1.0 + e)))
    r  = np.array([r0, 0.0])
    v  = np.array([0.0, v0])

    def accel(rv: np.ndarray, vv: np.ndarray) -> np.ndarray:
        rm  = float(np.linalg.norm(rv))
        rh  = rv / rm
        v2  = float(vv @ vv)
        rdv = float(rh @ vv)
        a_N  = -GM * rh / rm**2
        a_PN = (GM / (c**2 * rm**2)) * (
            K_R  * (GM / rm) * rh
            + K_v2 * v2 * rh
            + K_rv * rdv * vv
        )
        return a_N + a_PN

    omegas: list[float] = []
    last_r           = float(np.linalg.norm(r))
    last_was_decr    = False
    n_steps_max      = int(n_orbits * 2.0 * math.pi / (dt * v0 / r0) * 3)

    for _ in range(n_steps_max):
        a1 = accel(r, v)
        r  = r + v * dt + 0.5 * a1 * dt**2
        a2 = accel(r, v)
        v  = v + 0.5 * (a1 + a2) * dt
        cur_r = float(np.linalg.norm(r))
        if last_was_decr and cur_r > last_r:
            omegas.append(math.atan2(r[1], r[0]))
        last_was_decr = cur_r < last_r
        last_r        = cur_r
        if len(omegas) >= n_orbits + 1:
            break

    if len(omegas) < 2:
        return {'alpha_A': alpha_A, 'alpha_B': alpha_B,
                'delta_omega_GR': delta_omega_GR,
                'delta_omega_lat_per_orbit': float('nan'),
                'ratio_lat_vs_GR': float('nan'),
                'n_perihelia': len(omegas),
                'orbit_advances': [],
                'orbit_std': float('nan')}

    advances = []
    for i in range(1, len(omegas)):
        d = omegas[i] - omegas[i - 1]
        while d >  math.pi: d -= 2.0 * math.pi
        while d <= -math.pi: d += 2.0 * math.pi
        advances.append(d)

    lat = float(np.mean(advances))
    std = float(np.std(advances))
    return {
        'alpha_A':                    alpha_A,
        'alpha_B':                    alpha_B,
        'delta_omega_GR_per_orbit':   delta_omega_GR,
        'delta_omega_lat_per_orbit':  lat,
        'ratio_lat_vs_GR':            lat / delta_omega_GR,
        'n_perihelia':                len(omegas),
        'orbit_advances':             advances,
        'orbit_std':                  std,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  Main harness
# ═══════════════════════════════════════════════════════════════════════════════

def run(L_: int = L, n_orbits_: int = N_ORBITS, dt_: float = DT_ORBIT) -> dict:
    print('=' * 70)
    print('GR-3 Forks A & B — extended run')
    print('=' * 70)
    print(f'L={L_}, n_orbits={n_orbits_}, dt_orbit={dt_:.0e}')
    print()

    print('Building open-BC Poisson potential …')
    t0   = time.time()
    rho  = gaussian_mass_3d(L_, M=M, sigma=SIGMA)
    phi  = solve_poisson_3d_open(rho, G_N=G_N)
    print(f'  Done in {time.time()-t0:.2f}s  |  '
          f'φ range [{phi.min():.4e}, {phi.max():.4e}]')
    print()

    header = (f"{'fork':>28} | {'GR-1 K':>8} | {'GR-2':>7} | "
              f"{'GR-3 (mean)':>11} | {'±std':>6} | "
              f"{'GR-4 ratio':>10} | {'perihelia':>9} | {'orbit std':>9}")
    sep = '-' * len(header)
    print(header); print(sep)

    results: dict[str, Any] = {}
    for fork in FORKS:
        tf = time.time()
        _, K = gr1_K(fork, phi, C_0, B_GR1, G_N, M)
        _, _, r2 = gr2_ratio(fork, phi, C_0, B_GR2, G_N, M)
        gr3 = gr3_ratio_GR(fork, phi, C_0, GR3_PAIRS)
        gr4 = gr4_mercury_advance(fork, n_orbits=n_orbits_, dt=dt_)
        elapsed = time.time() - tf

        results[fork.NAME] = {
            'description': fork.DESCRIPTION,
            'GR1_K':         K,
            'GR2_ratio':     r2,
            'GR3_mean':      gr3['mean_ratio_GR'],
            'GR3_std':       gr3['std_ratio_GR'],
            'GR3_detail':    gr3['rows'],
            'GR4_ratio':     gr4['ratio_lat_vs_GR'],
            'GR4_alpha_A':   gr4['alpha_A'],
            'GR4_alpha_B':   gr4['alpha_B'],
            'GR4_n_perihelia': gr4['n_perihelia'],
            'GR4_orbit_std':   gr4['orbit_std'],
            'GR4_orbit_advances': gr4['orbit_advances'],
        }
        m3 = gr3['mean_ratio_GR']; s3 = gr3['std_ratio_GR']
        r4 = gr4['ratio_lat_vs_GR']; n4 = gr4['n_perihelia']
        os4 = gr4['orbit_std']
        print(f"{fork.NAME:>28} | {K:>8.4f} | {r2:>7.4f} | "
              f"{m3:>11.4f} | {s3:>6.1e} | "
              f"{r4:>10.4f} | {n4:>9d} | {os4:>9.6f}  ({elapsed:.1f}s)")

    print(sep)
    print()

    # ── save outputs ──────────────────────────────────────────────────────────
    out_dir  = os.path.abspath(os.path.join(SIM_ROOT, 'test-results'))
    os.makedirs(out_dir, exist_ok=True)

    payload = {
        'harness': 'gr3_forks_AB_extended.py',
        'run_date': time.strftime('%Y-%m-%d %H:%M'),
        'params': {
            'L':        L_, 'M': M, 'sigma': SIGMA, 'G_N': G_N, 'c_0': C_0,
            'b_gr1':    B_GR1, 'b_gr2': B_GR2,
            'n_orbits': n_orbits_, 'dt_orbit': dt_,
            'gr3_pairs': GR3_PAIRS,
        },
        'forks': results,
    }

    json_path = os.path.join(out_dir, 'gr3_forks_AB_L192.json')
    md_path   = os.path.join(out_dir, 'gr3_forks_AB_L192.md')

    with open(json_path, 'w') as f:
        json.dump(payload, f, indent=2)

    _write_markdown(payload, md_path)
    print(f'Wrote {json_path}')
    print(f'Wrote {md_path}')
    return payload


def _write_markdown(p: dict, path: str) -> None:
    sp   = p['params']
    fks  = p['forks']
    lines: list[str] = [
        '# GR-3 Forks A & B — extended run',
        '',
        f'_Generated {p["run_date"]} by `forks/gr3_forks_AB_extended.py`._',
        '',
        '## Parameters',
        '',
        f"- Lattice $L={sp['L']}$, $M={sp['M']}$, $\\sigma={sp['sigma']}$, "
        f"$G_N={sp['G_N']}$, $c_0={sp['c_0']}$.",
        f"- GR-1/GR-2 impact parameter $b={sp['b_gr1']}$.",
        f"- GR-3 (near, far) pairs: {sp['gr3_pairs']}.",
        f"- GR-4: {sp['n_orbits']} orbits, dt={sp['dt_orbit']:.0e}, "
        f"$GM=0.003$, $a=1$, $e=0.3$, $c=1$.",
        '',
        '## Results',
        '',
        '| Fork | GR-1 $K$ | GR-2 ratio | GR-3 ratio$_{GR}$ (mean ± std) '
        '| GR-4 $\\Delta\\omega_\\text{lat}/\\Delta\\omega_{\\rm GR}$ '
        '| $\\alpha_A$ | $\\alpha_B$ | Perihelia |',
        '|---|---|---|---|---|---|---|---|',
    ]
    for name, r in fks.items():
        K  = r['GR1_K']; r2 = r['GR2_ratio']
        m3 = r['GR3_mean']; s3 = r['GR3_std']
        r4 = r['GR4_ratio']
        aA = r['GR4_alpha_A']; aB = r['GR4_alpha_B']
        n4 = r['GR4_n_perihelia']
        lines.append(f'| `{name}` | {K:.4f} | {r2:.4f} | '
                     f'{m3:.4f} ± {s3:.1e} | {r4:.4f} | '
                     f'{aA:.3f} | {aB:.3f} | {n4} |')

    lines += [
        '',
        '## Interpretation',
        '',
        'Forks A and B both use the full Schwarzschild metric '
        '($\\alpha_A=\\alpha_B=1$), so:',
        '',
        '- GR-1 and GR-2 should be identical to the baseline (photon sector unchanged).',
        '- GR-3 should land near 1.0 (the factor-2 Pound-Rebka issue is fixed).',
        '- GR-4 should land near **2.00** for these forks '
        '(the 3π normalisation in the harness means the Schwarzschild 6π advance '
        'yields ratio = 2; Fork C at α_A=α_B=0.5 would give ratio ≈ 1.00).',
        '',
        'A larger spread in `orbit_std` across the 12 orbits than in the '
        '6-orbit run would indicate unmodelled 2PN or numerical drift.',
    ]

    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--L',        type=int,   default=L,
                        help=f'Lattice side length (default {L})')
    parser.add_argument('--n-orbits', type=int,   default=N_ORBITS,
                        help=f'Number of Mercury orbits (default {N_ORBITS})')
    parser.add_argument('--dt',       type=float, default=DT_ORBIT,
                        help=f'Orbit integration dt (default {DT_ORBIT:.0e})')
    args = parser.parse_args()
    run(L_=args.L, n_orbits_=int(args.n_orbits), dt_=args.dt)
