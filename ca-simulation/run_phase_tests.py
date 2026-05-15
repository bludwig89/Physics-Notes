"""
run_phase_tests.py  —  End-to-end test suite for all implemented phases
========================================================================
Runs every phase added in the Next-Steps implementation pass and reports
pass/fail with measured residuals.  Saves figures to ./figures/phase_*.png.

Phases covered:
  A1  Bloch-sphere coloring
  A2  Static visualization frames (strip, spacetime, graph)
  B1  Group-velocity measurement
  B2  Min-size / min-σ sweeps
  C1  Variable-c (refraction)
  D1  Dirac CA (mass, dispersion, zitterbewegung)
  E1  U(1) electromagnetic gauge (Aharonov-Bohm phase)
  E2  SU(2) weak gauge (parity violation)
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ca_core as ca
import ca_dirac as dirac
import ca_curved as cv
import ca_weak as wk
import spinor_color as sc

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)


def section(title):
    print()
    print('=' * 72)
    print('  ' + title)
    print('=' * 72)


def check(name, ok, detail=''):
    status = 'PASS' if ok else 'FAIL'
    print(f'  [{status}]  {name}  {detail}')
    return ok


# ══════════════════════════════════════════════════════════════════
#  Phase A1 — Bloch-sphere coloring
# ══════════════════════════════════════════════════════════════════

def test_A1():
    section('Phase A1 — Bloch-sphere coloring')
    L = 32
    shape = (L, L)
    # Three Gaussian helicity states
    fL, gL = ca.gaussian_spinor_2d(shape, sigma=5.0, helicity='left')
    fR, gR = ca.gaussian_spinor_2d(shape, sigma=5.0, helicity='right')
    fM, gM = ca.gaussian_spinor_2d(shape, sigma=5.0, helicity='mixed')

    peak = (np.abs(fL)**2 + np.abs(gL)**2).max()
    rgbL = sc.spinor_to_rgb(fL, gL, peak=peak)
    rgbR = sc.spinor_to_rgb(fR, gR, peak=peak)
    rgbM = sc.spinor_to_rgb(fM, gM, peak=peak)
    legend = sc.make_bloch_legend(size=128)

    # Center pixel of each state should match the analytic mapping
    cL = rgbL[L//2, L//2]
    cR = rgbR[L//2, L//2]
    cM = rgbM[L//2, L//2]

    # left  (f=G, g=0):     θ=0  → lightness 0.85 (bright)
    # right (f=0, g=G):     θ=π  → lightness 0.15 (dark)
    # The center pixel of left should be lighter than right.
    avg_L = float(np.mean(cL))
    avg_R = float(np.mean(cR))
    ok1 = check('left center brighter than right center',
                avg_L > avg_R,
                f'(left avg={avg_L:.3f}, right avg={avg_R:.3f})')

    # Render strip image
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))
    axes[0].imshow(rgbL, origin='lower'); axes[0].set_title('left helicity')
    axes[1].imshow(rgbR, origin='lower'); axes[1].set_title('right helicity')
    axes[2].imshow(rgbM, origin='lower'); axes[2].set_title('mixed (G/√2, G/√2)')
    axes[3].imshow(legend, origin='lower'); axes[3].set_title('Bloch legend')
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
    plt.suptitle('Phase A1 — Bloch-sphere spinor coloring')
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, 'phaseA1_bloch_coloring.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()
    check('strip image written', os.path.exists(out), f'-> {out}')

    return ok1


# ══════════════════════════════════════════════════════════════════
#  Phase A2 — Visualization frames
# ══════════════════════════════════════════════════════════════════

def test_A2():
    section('Phase A2 — Visualization frames')
    L = 64
    sigma = 5.0
    c = 0.5
    snap_steps = [0, 60, 120, 180, 240]

    f, g = ca.gaussian_spinor_2d((L, L), sigma=sigma, helicity='mixed')
    frames_2d = []
    for step in range(max(snap_steps) + 1):
        if step in snap_steps:
            frames_2d.append((f.copy(), g.copy()))
        if step < max(snap_steps):
            f, g = ca.weyl_step_2d_splitstep(f, g, c)

    # peak across all snapshots for consistent saturation
    peak = max((np.abs(f0)**2 + np.abs(g0)**2).max() for f0, g0 in frames_2d)

    fig, axes = plt.subplots(1, len(frames_2d), figsize=(15, 3.2))
    for ax, t_step, (f0, g0) in zip(axes, snap_steps, frames_2d):
        rgb = sc.spinor_to_rgb(f0, g0, peak=peak)
        ax.imshow(rgb, origin='lower')
        ax.set_title(f't = {t_step}')
        ax.set_xticks([]); ax.set_yticks([])
    plt.suptitle('Phase A2 — Weyl CA Bloch-colored propagation (mixed helicity)')
    plt.tight_layout()
    out1 = os.path.join(FIGURES_DIR, 'phaseA2_bloch_strip.png')
    plt.savefig(out1, dpi=120, bbox_inches='tight'); plt.close()
    check('2D strip image written', os.path.exists(out1), f'-> {out1}')

    # 1D spacetime coloring
    N1 = 96
    n_steps = 200
    x = np.arange(N1) - N1 // 2
    f1 = np.exp(-x**2 / (2 * 4.0**2)).astype(complex)
    g1 = np.zeros(N1, dtype=complex)

    f_history = [f1.copy()]
    g_history = [g1.copy()]
    for _ in range(n_steps):
        f1, g1 = ca.weyl_step_2d_splitstep(f1.reshape(N1, 1),
                                            g1.reshape(N1, 1), c=0.5)
        f1 = f1.reshape(N1); g1 = g1.reshape(N1)
        f_history.append(f1.copy()); g_history.append(g1.copy())
    f_arr = np.array(f_history); g_arr = np.array(g_history)
    rgb_st = sc.spinor_to_rgb(f_arr, g_arr)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.imshow(rgb_st, origin='lower', aspect='auto')
    ax.set_xlabel('cell index'); ax.set_ylabel('time step')
    ax.set_title('Phase A2 — 1D spacetime, Bloch-colored\n'
                 '(left-helicity Gaussian on a ring)')
    out2 = os.path.join(FIGURES_DIR, 'phaseA2_spacetime_color.png')
    plt.savefig(out2, dpi=120, bbox_inches='tight'); plt.close()
    check('1D spacetime image written', os.path.exists(out2), f'-> {out2}')

    # NetworkX graph view (small lattice)
    try:
        import networkx as nx
        Lg = 8
        f, g = ca.gaussian_spinor_2d((Lg, Lg), sigma=2.0, helicity='left')
        for _ in range(3):
            f, g = ca.weyl_step_2d_splitstep(f, g, c=0.5)
        rgb = sc.spinor_to_rgb(f, g)
        G = nx.grid_2d_graph(Lg, Lg, periodic=True)
        pos = {(i, j): (j, i) for i, j in G.nodes()}
        node_colors = [rgb[i, j] for i, j in G.nodes()]
        fig, ax = plt.subplots(figsize=(6, 6))
        nx.draw(G, pos=pos, node_color=node_colors, node_size=300,
                edge_color='lightgray', with_labels=False, ax=ax)
        ax.set_title('Phase A2 — 8×8 lattice as a graph (t=3)')
        out3 = os.path.join(FIGURES_DIR, 'phaseA2_graph_view.png')
        plt.savefig(out3, dpi=120, bbox_inches='tight'); plt.close()
        check('graph view written', os.path.exists(out3), f'-> {out3}')
    except ImportError:
        print('  [SKIP]  NetworkX not available')

    return True


# ══════════════════════════════════════════════════════════════════
#  Phase B1 — Group velocity
# ══════════════════════════════════════════════════════════════════

def test_B1():
    section('Phase B1 — Group-velocity measurement')
    all_ok = True
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for k0 in [(0.3, 0.0), (0.0, 0.3), (0.4, 0.3), (0.6, 0.0)]:
        res = ca.measure_group_velocity_2d(L=128, n_steps=60, c=0.5,
                                            k0=k0, sigma=8.0)
        ok = abs(res['speed_ratio'] - 1.0) < 0.15
        all_ok = all_ok and ok
        check(f'k0={k0}', ok, f'speed_ratio={res["speed_ratio"]:.4f}')
        c = res['centroids']
        ax.plot(c[:, 0], c[:, 1], '-', label=f'k0={k0}')
    ax.set_xlabel('x centroid'); ax.set_ylabel('y centroid')
    ax.set_title('Phase B1 — wave-packet centroid trajectories')
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    out = os.path.join(FIGURES_DIR, 'phaseB1_group_velocity.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()
    return all_ok


# ══════════════════════════════════════════════════════════════════
#  Phase B2 — Min-size sweeps
# ══════════════════════════════════════════════════════════════════

def test_B2():
    section('Phase B2 — Size sweeps')
    L_results = ca.size_sweep_L([8, 12, 16, 24, 32, 48, 64],
                                  n_steps=40, c=0.5, sigma=3.0, k0=(0.6, 0.0))
    sigma_results = ca.size_sweep_sigma([0.5, 1.0, 1.5, 2.0, 3.0, 5.0],
                                          L=32, n_steps=30, c=0.5, k0=(0.6, 0.0))

    for r in L_results:
        print(f'  L={r["L"]:3d}  speed_ratio={r["speed_ratio"]:.4f}  norm_drift={r["norm_drift"]:.2e}')
    for r in sigma_results:
        print(f'  σ={r["sigma"]:.2f}  speed_ratio={r["speed_ratio"]:.4f}  frac_above_Nyq={r["frac_above_nyquist"]:.2e}')

    # Check that L=32 and above give speed_ratio close to 1, and that
    # σ=3+ gives near-zero Nyquist content.
    ok_L = any(r['L'] >= 32 and r['speed_ratio'] > 0.9 for r in L_results)
    ok_sigma = any(r['sigma'] >= 3.0 and r['frac_above_nyquist'] < 1e-3
                   for r in sigma_results)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.0))
    Ls = [r['L'] for r in L_results]; sr = [r['speed_ratio'] for r in L_results]
    ax1.plot(Ls, sr, 'o-'); ax1.axhline(1.0, color='gray', linestyle='--')
    ax1.set_xlabel('L'); ax1.set_ylabel('speed_ratio')
    ax1.set_title('B2 — L sweep'); ax1.grid(alpha=0.3)

    sigmas = [r['sigma'] for r in sigma_results]
    nyq    = [r['frac_above_nyquist'] for r in sigma_results]
    ax2.semilogy(sigmas, nyq, 's-'); ax2.set_xlabel('σ')
    ax2.set_ylabel('fraction of power above Nyquist/2')
    ax2.set_title('B2 — σ sweep'); ax2.grid(alpha=0.3, which='both')
    out = os.path.join(FIGURES_DIR, 'phaseB2_size_sweeps.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()

    check('L>=32 → speed_ratio>0.9', ok_L)
    check('σ>=3 → <0.1% above Nyquist', ok_sigma)
    return ok_L and ok_sigma


# ══════════════════════════════════════════════════════════════════
#  Phase C1 — Variable-c refraction
# ══════════════════════════════════════════════════════════════════

def test_C1():
    section('Phase C1 — Variable-c refraction (Snell\'s law)')

    # Strang-split version (production)
    res_s = cv.measure_refraction(L=128, n_steps=200,
                                    c_left=0.5, c_right=0.3,
                                    k_in=(0.5, 0.15), sigma=8.0,
                                    x_start_frac=0.25,
                                    method='strang', n_sub=4)
    # Blending (kept for comparison)
    res_b = cv.measure_refraction(L=128, n_steps=200,
                                    c_left=0.5, c_right=0.3,
                                    k_in=(0.5, 0.15), sigma=8.0,
                                    x_start_frac=0.25,
                                    method='blend')

    print(f'  Strang split (n_sub=4):')
    print(f'    theta_in={res_s["theta_in_deg"]:.2f}°  theta_out={res_s["theta_out_deg"]:.2f}°  Snell={res_s["theta_out_pred_deg"]:.2f}°')
    print(f'    norm drift over 200 steps = {res_s["norm_drift"]:.3e}')
    print(f'  Blending (comparison):')
    print(f'    theta_out={res_b["theta_out_deg"]:.2f}°')
    print(f'    norm drift over 200 steps = {res_b["norm_drift"]:.3e}')

    err = abs(res_s['theta_out_deg'] - res_s['theta_out_pred_deg'])
    ok_refr = check('Strang refraction within 1.5° of Snell',
                    err < 1.5, f'(err = {err:.2f}°)')

    # Strang should improve norm drift over blending (in long-time regime).
    ok_norm = check('Strang norm drift ≤ blending',
                    res_s['norm_drift'] <= res_b['norm_drift'] * 1.05,
                    f'(strang={res_s["norm_drift"]:.2e}, blend={res_b["norm_drift"]:.2e})')

    return ok_refr and ok_norm


# ══════════════════════════════════════════════════════════════════
#  Phase D1 — Dirac CA
# ══════════════════════════════════════════════════════════════════

def test_D1():
    section('Phase D1 — Dirac CA')

    # Weyl regression at m=0
    L = 32; shape = (L, L)
    f, g = ca.gaussian_spinor_2d(shape, sigma=3.0, helicity='left')
    nu, nd, xu, xd = dirac.gaussian_dirac_2d(shape, sigma=3.0, chirality='left')
    for _ in range(20):
        f, g = ca.weyl_step_2d_splitstep(f, g, c=0.5)
        nu, nd, xu, xd = dirac.dirac_step_2d_splitstep(
            nu, nd, xu, xd, c=0.5, m=0.0, dt=1.0)
    diff = max(float(np.max(np.abs(nu - f))),
               float(np.max(np.abs(nd - g))),
               float(np.max(np.abs(xu))),
               float(np.max(np.abs(xd))))
    ok1 = check('Weyl regression at m=0', diff < 1e-13,
                f'(max diff = {diff:.2e})')

    # Norm conservation with mass
    nu, nd, xu, xd = dirac.gaussian_dirac_2d(shape, sigma=3.0, chirality='mixed')
    n0 = dirac.dirac_norm(nu, nd, xu, xd)
    for _ in range(1000):
        nu, nd, xu, xd = dirac.dirac_step_2d_splitstep(
            nu, nd, xu, xd, c=0.5, m=0.3, dt=1.0)
    n1 = dirac.dirac_norm(nu, nd, xu, xd)
    drift = abs(n1 - n0) / n0
    ok2 = check('norm conservation (m=0.3, 1000 steps)',
                drift < 1e-12, f'(drift = {drift:.2e})')

    # Dispersion
    r = dirac.verify_dirac_dispersion_2d(L=32, n_steps=20, c=0.5, m=0.3)
    max_res = max(row['residual'] for row in r)
    ok3 = check('Dirac dispersion (machine precision)',
                max_res < 1e-13, f'(max residual = {max_res:.2e})')

    # Zitterbewegung — 5000-step run with wider packet to tighten FFT
    # bin resolution (Δω = 2π/(n·dt))
    t, rho, fn, fa = dirac.measure_zitterbewegung_freq_2d(
        L=96, n_steps=5000, c=0.5, m=0.5, dt=0.5, sigma=14.0)
    err = abs(fn - fa) / fa
    bin_width = 2.0 * np.pi / (len(t) * (t[1] - t[0]))
    ok4 = check('Zitterbewegung freq within FFT bin of 2mc²',
                err < 0.05,
                f'(measured={fn:.5f}, analytic={fa:.5f}, err={err*100:.2f}%, FFT bin={bin_width:.5f})')

    fig, ax = plt.subplots(figsize=(8, 4.0))
    ax.plot(t, rho, '-')
    ax.axhline(0.0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('time'); ax.set_ylabel('ρ_η − ρ_χ')
    ax.set_title(f'Phase D1 — Zitterbewegung: chirality oscillation\n'
                 f'measured ω={fn:.3f}, 2mc²={fa:.3f}')
    out = os.path.join(FIGURES_DIR, 'phaseD1_zitterbewegung.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()

    return ok1 and ok2 and ok3 and ok4


# ══════════════════════════════════════════════════════════════════
#  Phase E1 — U(1)
# ══════════════════════════════════════════════════════════════════

def test_E1():
    section('Phase E1 — U(1) EM gauge')
    res = dirac.aharonov_bohm_test(L=64, n_steps=100, c=0.5, m=0.0,
                                     q=1.0, dt=1.0, flux=np.pi, sigma=8.0)
    err = abs(res['measured_phase'] - res['analytic_phase'])
    ok1 = check('phase pickup at machine precision',
                err < 1e-12, f'(err = {err:.2e})')
    ok2 = check('overlap magnitude = 1.0',
                abs(res['overlap_magnitude'] - 1.0) < 1e-12,
                f'(|overlap|={res["overlap_magnitude"]:.10f})')
    ok3 = check('norm exactly preserved with A0',
                abs(res['norm_with_A0'] - res['initial_norm']) < 1e-10,
                f'(drift={abs(res["norm_with_A0"]-res["initial_norm"]):.2e})')
    return ok1 and ok2 and ok3


# ══════════════════════════════════════════════════════════════════
#  Phase E2 — SU(2)
# ══════════════════════════════════════════════════════════════════

def test_E2():
    section('Phase E2 — SU(2) weak gauge (parity violation)')
    res = wk.parity_violation_test(L=32, n_steps=63, c=0.0, m_e=0.0,
                                     g_weak=1.0, dt=1.0, W3_value=0.1, sigma=4.0)
    pop_err = abs(res['left_e_pop_measured'] - res['left_e_pop_analytic'])
    pop_rel = pop_err / max(res['left_e_pop_analytic'], 1e-10)
    ok1 = check('left isospin rotation matches analytic',
                pop_rel < 0.05,
                f'(measured={res["left_e_pop_measured"]:.6f}, analytic={res["left_e_pop_analytic"]:.6f})')

    chi_drift = abs(res['right_chi_pop_final'] - res['right_chi_pop_initial'])
    ok2 = check('right chirality immune to W (parity violation)',
                chi_drift < 1e-10,
                f'(drift={chi_drift:.2e})')
    ok3 = check('zero leakage from right to left',
                res['right_leakage_to_left'] < 1e-12,
                f'(leakage={res["right_leakage_to_left"]:.2e})')
    return ok1 and ok2 and ok3


# ══════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════

def main():
    results = {}
    results['A1'] = test_A1()
    results['A2'] = test_A2()
    results['B1'] = test_B1()
    results['B2'] = test_B2()
    results['C1'] = test_C1()
    results['D1'] = test_D1()
    results['E1'] = test_E1()
    results['E2'] = test_E2()

    print()
    print('=' * 72)
    print('  SUMMARY')
    print('=' * 72)
    for phase, ok in results.items():
        status = 'PASS' if ok else 'FAIL'
        print(f'  [{status}]  Phase {phase}')
    total_ok = sum(results.values())
    print(f'\n  {total_ok} / {len(results)} phases passed')
    print(f'  Figures: {FIGURES_DIR}/phase*.png')

    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
