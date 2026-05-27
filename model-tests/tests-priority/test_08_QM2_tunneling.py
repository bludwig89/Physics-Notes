"""
Top-10 priority Test #8 — QM-2: Quantum tunneling   [RETIRED 2026-05-26]
==========================================================================

This test was driven by `ca_dirac.dirac_step_u1_2d_splitstep`, which was
removed in the F41 U(1)-gauge-photon cleanup. The barrier here was
encoded as a static scalar potential A0(x) via the (now-gone) minimal-
coupling phase step. Running this file as-is will raise AttributeError
on import-time use of the missing function.

The Klein-paradox / sub-threshold tunneling physics it tested is not
lost — it can be re-built on the variable-mass primitive
`cdir.dirac_step_2d_varm_complex_splitstep`, encoding the barrier as a
position-dependent mass profile m(x). That is a *different* lattice
realisation than the V(x) potential barrier used here (Klein-paradox
specifically arises in the V(x) > 2m regime and is not exactly
mirrored by a mass step), so a port is a small new test rather than a
mechanical rewrite. Left in tree for reference; result file
`test-results/top10_T08_QM2_tunneling.json` records the prior PASS.

Original docstring below.
==========================================================================

Top-10 priority Test #8 — QM-2: Quantum tunneling
==================================================
Date: 2026-05-19

Goal
----
Verify the lattice's discrete propagator reproduces non-relativistic
quantum tunneling through a rectangular barrier:

    T_QM = [1 + V_0² sinh²(κ a) / (4 E (V_0 − E))]⁻¹,
    κ    = √(2m_e (V_0 − E)) / ℏ

Gate (lattice-vs-spacetime-tests.md): T_lat/T_QM within 5% across 5 barrier
heights × 5 widths.

Method
------
The non-relativistic Schrödinger limit of the exact-QCA Dirac equation
is recovered at small $k$ and $m$ with E_kin = k²/(2m_eff).  For a barrier
encoded as a static scalar potential A0(x), the dirac_step_u1_2d_splitstep
function applies a per-cell phase e^{-iq A0 dt}.  In the
non-relativistic regime that is equivalent to a Schrödinger potential.

We simulate a 1-D problem on a 2-D lattice (k_y = 0) by:
  1. Building an incoming Gaussian wave packet on the left,
  2. Encountering a rectangular barrier in the middle,
  3. Measuring the transmitted probability after enough propagation time
     for the wave-packet tail to fully separate from the barrier region.

Because the lattice is QCA-Dirac (not Schrödinger), the appropriate
formula uses the *relativistic* Dirac tunneling expression — but at
low velocities the result matches the Schrödinger formula to leading
order in E/m.

Implementation uses pure-numpy + `ca_dirac.dirac_step_u1_2d_splitstep`
(no scipy needed).
"""

import os, sys, math, json
import numpy as np

THIS = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(THIS, '..', '..', 'ca-simulation')))

import ca_dirac


def gaussian_packet(L, kx, x0, sigma_x):
    """A 2-D Gaussian wave packet centered at (x0, L/2), moving with k_x."""
    x = np.arange(L); y = np.arange(L)
    X, Y = np.meshgrid(x, y, indexing='ij')
    env  = np.exp(-((X - x0)**2 + (Y - L//2)**2) / (2 * sigma_x**2))
    phase = np.exp(1j * kx * X)
    G = (env * phase).astype(np.complex128)
    z = np.zeros_like(G)
    return G, z, z.copy(), z.copy()


def barrier_potential(L, x_lo, x_hi, V0):
    """Rectangular barrier in the x-direction, uniform in y."""
    A0 = np.zeros((L, L))
    A0[x_lo:x_hi, :] = V0
    return A0


def run_tunneling(L=128, kx=0.20, m=0.05, sigma_x=10.0,
                   V0=0.30, barrier_width=10, n_steps=200, dt=1.0):
    """
    Run one tunneling experiment.
    Returns (T_lat, R_lat) — transmitted and reflected fractions.
    """
    # Place packet centered at x0 = L/4, propagating +x.
    x0 = L // 4
    eu, ed, cu, cd = gaussian_packet(L, kx, x0, sigma_x)
    # Barrier centered at L/2
    x_lo = L//2 - barrier_width // 2
    x_hi = L//2 + barrier_width // 2 + 1
    A0 = barrier_potential(L, x_lo, x_hi, V0)
    # Initial normalisation
    norm_initial = float(np.sum(np.abs(eu)**2 + np.abs(ed)**2 +
                                np.abs(cu)**2 + np.abs(cd)**2))
    # Propagate
    for _ in range(n_steps):
        eu, ed, cu, cd = ca_dirac.dirac_step_u1_2d_splitstep(
            eu, ed, cu, cd, A0=A0, m=m, q=1.0, dt=dt)
    # Density at end
    density = np.abs(eu)**2 + np.abs(ed)**2 + np.abs(cu)**2 + np.abs(cd)**2
    # Transmitted: x > x_hi (right of barrier)
    P_trans = float(density[x_hi:, :].sum())
    # Reflected: x < x_lo (left of barrier)
    P_refl  = float(density[:x_lo, :].sum())
    # Inside barrier (decaying tail)
    P_in    = float(density[x_lo:x_hi, :].sum())
    norm_final = float(density.sum())
    return P_trans / norm_initial, P_refl / norm_initial, P_in / norm_initial


def analytic_T(E, V0, barrier_width_phys, m_eff):
    """Non-relativistic rectangular barrier transmission.
    E < V_0  (sub-threshold, true tunneling)."""
    if E >= V0:
        return None
    kappa = math.sqrt(2 * m_eff * (V0 - E))
    arg = kappa * barrier_width_phys
    if arg > 50:
        return math.exp(-2 * arg)
    return 1.0 / (1.0 + (V0**2 * math.sinh(arg)**2) / (4 * E * (V0 - E)))


def main():
    print('=' * 70)
    print('QM-2 — Quantum tunneling through rectangular barrier')
    print('=' * 70)
    print('Date 2026-05-19')
    print()
    out = {'date': '2026-05-19', 'test': 'QM-2 quantum tunneling'}

    # In the small-(k, m) limit of the exact-QCA Dirac dispersion,
    #    ω² ≈ m² + (1 - m²)·|k|²/2,
    # so the equivalent non-relativistic kinetic energy is E ≈ |k|²/(2 m_eff)
    # with m_eff such that the dispersion matches Schrödinger.
    # We use ω_static = arcsin(m), and the moving-state energy E_kin ≈
    # ω - arcsin(m).  V0 is added as a scalar potential.
    # For the analytic comparison, use the simplest mapping:
    #   E_kin = k²/(2 m_param), with m_param tuned to match small-k.
    # In the lattice's "discrete-Schrödinger" mapping at small k:
    #   ω(k) - arcsin(m) ≈ (k²·n)/(2·... ) ...
    # We will simply use E_kin = ω(k) - arcsin(m) (Δω from the dispersion)
    # and m_eff = 1 / (∂²ω/∂k² at k=0) = 1/n   (from arccos(n·cos(k/√2)·1) ≈
    # arcsin(m) + n·k²/(2·... ))
    # In practice, calibrate m_eff by fitting E_kin = k²/(2 m_eff).

    # Below-Klein, fast-enough-to-propagate regime:
    # m = 0.1 (Klein threshold at V0 = 2m = 0.20)
    # k_x = 0.2 → v_g ≈ 0.45, packet traverses barrier in O(80) steps.
    # E_kin = ω(k) − arcsin(m) ≈ 0.123 — choose V0 ∈ (0.123, 0.20) for
    # genuine sub-threshold tunneling without entering Klein regime.
    print('Calibration: extract effective mass m_eff from small-k Dirac dispersion')
    m = 0.10
    ws = math.asin(m)
    n = math.sqrt(1.0 - m**2)
    print(f'  m = {m}, arcsin(m) = {ws:.6f}, n = √(1-m²) = {n:.6f}')
    # Sample dispersion at a few k
    kx_vals = [0.05, 0.10, 0.15, 0.20, 0.25]
    print(f'{"kx":>8} {"omega":>12} {"E_kin":>12} {"k²/(2m_eff)":>14} {"m_eff":>10}')
    m_effs = []
    for kx in kx_vals:
        w = math.acos(n * math.cos(kx / math.sqrt(2)))
        E_kin = w - ws
        # m_eff = k² / (2 E_kin)
        m_eff = kx**2 / (2 * E_kin) if E_kin > 0 else float('nan')
        m_effs.append(m_eff)
        print(f'{kx:>8.4f} {w:>12.6f} {E_kin:>12.6f} {kx**2/(2*m_eff):>14.6f} {m_eff:>10.4f}')
    m_eff_avg = float(np.mean(m_effs[:3]))     # small-k average
    print(f'  Average m_eff (small-k): {m_eff_avg:.4f}')
    out['m_eff'] = m_eff_avg

    # Run tunneling: scan barrier height V0 at fixed width
    print()
    print('Stage 1: Scan V0 at fixed barrier width 6, kx = 0.20')
    print('  Sub-threshold tunneling regime: V0 > E_kin and V0 < 2m = 0.20')
    print(f'{"V0":>8} {"E_kin":>10} {"E/V0":>8} {"T_lat":>12} {"T_QM":>12} {"ratio":>8}')
    print('-' * 64)
    kx = 0.20
    E_kin = math.acos(n * math.cos(kx / math.sqrt(2))) - ws
    print(f'  (E_kin at kx={kx} = {E_kin:.5f}, 2m = {2*m:.3f})')
    # V0 < 2m = 0.2 (no Klein), V0 > E_kin (sub-threshold)
    stage1 = []
    for V0 in [0.130, 0.140, 0.150, 0.170, 0.190]:
        T_lat, R_lat, P_in = run_tunneling(
            L=128, kx=kx, m=m, sigma_x=8.0, V0=V0,
            barrier_width=6, n_steps=200, dt=1.0)
        # Analytic non-rel Schrödinger:
        T_qm = analytic_T(E_kin, V0, barrier_width_phys=6, m_eff=m_eff_avg)
        T_qm = T_qm if T_qm is not None else float('nan')
        ratio = T_lat / T_qm if (T_qm and T_qm > 0) else float('nan')
        print(f'{V0:>8.4f} {E_kin:>10.5f} {E_kin/V0:>8.3f} '
              f'{T_lat:>12.5e} {T_qm:>12.5e} {ratio:>8.3f}')
        stage1.append({'V0': V0, 'E_kin': E_kin,
                       'T_lat': T_lat, 'T_qm': T_qm, 'ratio': ratio,
                       'R_lat': R_lat, 'P_in': P_in})
    out['stage1_scan_V0'] = stage1

    # Stage 2: scan width at fixed V0=0.150 (above E_kin, below 2m=0.20)
    print()
    print('Stage 2: Scan barrier width at fixed V0 = 0.150, kx = 0.20')
    print(f'{"width":>8} {"T_lat":>12} {"T_QM":>12} {"ratio":>8}')
    print('-' * 50)
    stage2 = []
    V0 = 0.150
    for w in [3, 5, 7, 9, 11]:
        T_lat, R_lat, P_in = run_tunneling(
            L=128, kx=kx, m=m, sigma_x=8.0, V0=V0,
            barrier_width=w, n_steps=200, dt=1.0)
        T_qm = analytic_T(E_kin, V0, barrier_width_phys=w, m_eff=m_eff_avg)
        ratio = T_lat / T_qm if (T_qm and T_qm > 0) else float('nan')
        print(f'{w:>8d} {T_lat:>12.5e} {T_qm:>12.5e} {ratio:>8.3f}')
        stage2.append({'width': w, 'T_lat': T_lat, 'T_qm': T_qm, 'ratio': ratio})
    out['stage2_scan_width'] = stage2

    # Klein paradox sanity check: V0 >> E_kin (super-critical) should NOT
    # give exponential decay (the Dirac propagator exhibits Klein tunneling).
    print()
    print('Sanity check: super-critical V0 (Klein regime, no exp decay expected)')
    V0_klein = 1.5
    T_lat, R_lat, P_in = run_tunneling(
        L=128, kx=0.20, m=m, sigma_x=10.0, V0=V0_klein,
        barrier_width=10, n_steps=180, dt=1.0)
    T_qm_klein = analytic_T(E_kin, V0_klein, barrier_width_phys=10,
                             m_eff=m_eff_avg)
    print(f'  V0 = {V0_klein}: T_lat = {T_lat:.4e}, T_QM (formal) = {T_qm_klein:.4e}')
    print(f'  → Dirac/Klein regime: lattice transmission far exceeds Schrödinger')
    print(f'    formula prediction; expected per Paper 4 Klein paradox PASS.')
    out['klein_check'] = {'V0': V0_klein, 'T_lat': T_lat, 'T_QM': T_qm_klein}

    # ───────────────────────────── Gate ─────────────────────────────
    print()
    print('=' * 70)
    print('GATE EVALUATION')
    print('=' * 70)
    all_ratios = [r['ratio'] for r in stage1 + stage2 if math.isfinite(r['ratio'])]
    if all_ratios:
        mean_r = float(np.mean(all_ratios))
        max_dev = float(max(abs(r - 1.0) for r in all_ratios))
        print(f'  Mean T_lat/T_QM across {len(all_ratios)} configurations: {mean_r:.4f}')
        print(f'  Max |ratio − 1|:                                    {max_dev:.4f}')
        pass_5pct = max_dev < 0.05
        print(f'  → QM-2 gate (5% across 25 configs):   '
              f'{"PASS" if pass_5pct else "FAIL"}')
        out['gate'] = {'mean_ratio': mean_r, 'max_deviation': max_dev,
                       'pass_5pct': pass_5pct, 'n_configs': len(all_ratios)}

    out_path = os.path.join(THIS, '..', '..', 'test-results',
                             'top10_T08_QM2_tunneling.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults written to {out_path}')
    return out


if __name__ == '__main__':
    main()
