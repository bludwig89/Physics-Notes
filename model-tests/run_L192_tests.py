"""
run_L192_tests.py  —  Full phase-A–E test suite capped at L=192
================================================================
Identical physics to run_phase_tests.py but all lattice sizes are
capped at L=192 (and time-step counts / sigmas scaled down in
proportion) so the whole suite fits in ~3 GB RAM and completes in
a few minutes.

Phases:
  A1  Bloch-sphere spinor coloring
  A2  Visualization frames (2-D strip + 1-D spacetime)
  B1  Group-velocity measurement
  B2  Min-size / min-σ sweeps
  C1  Variable-c refraction (Strang, blend, Cayley)
  D1  Dirac CA (Weyl regression, norm, dispersion, zitterbewegung)
  E1  U(1) Aharonov–Bohm
  E2  SU(2) weak / parity violation
  E3  Discrete current conservation (∂_t ρ + ∇·J = 0)
"""

import os, sys, json, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ca-simulation'))
import ca_core as ca
import ca_dirac as dirac
import ca_curved as cv
import ca_weak as wk
import spinor_color as sc
import ca_core_exact as ce

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
RESULTS = {}

T0 = time.time()

def elapsed():
    return f"[+{time.time()-T0:5.1f}s]"

def section(title):
    print(); print('='*70); print(f'  {elapsed()}  {title}'); print('='*70)

def check(name, ok, detail=''):
    status = 'PASS' if ok else 'FAIL'
    print(f'  [{status}]  {name}  {detail}')
    return ok


# ─────────────────────────────────────────────────────────────────
#  Phase A1  L=192  sigma=30
# ─────────────────────────────────────────────────────────────────
def test_A1():
    section('Phase A1 — Bloch-sphere coloring  (L=192)')
    L = 192; shape = (L, L)
    fL, gL = ca.gaussian_spinor_2d(shape, sigma=30.0, helicity='left')
    fR, gR = ca.gaussian_spinor_2d(shape, sigma=30.0, helicity='right')
    fM, gM = ca.gaussian_spinor_2d(shape, sigma=30.0, helicity='mixed')
    peak = (np.abs(fL)**2 + np.abs(gL)**2).max()
    rgbL = sc.spinor_to_rgb(fL, gL, peak=peak)
    rgbR = sc.spinor_to_rgb(fR, gR, peak=peak)
    rgbM = sc.spinor_to_rgb(fM, gM, peak=peak)
    avg_L = float(np.mean(rgbL[L//2, L//2]))
    avg_R = float(np.mean(rgbR[L//2, L//2]))
    ok1 = check('left center brighter than right center',
                avg_L > avg_R,
                f'(left={avg_L:.3f}, right={avg_R:.3f})')
    fig, axes = plt.subplots(1, 3, figsize=(9, 3))
    for ax, rgb, title in zip(axes, [rgbL, rgbR, rgbM],
                               ['left', 'right', 'mixed']):
        ax.imshow(rgb, origin='lower'); ax.set_title(title); ax.axis('off')
    plt.suptitle('Phase A1 — Bloch-sphere coloring  L=192')
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, 'phaseA1_L192.png')
    plt.savefig(out, dpi=100, bbox_inches='tight'); plt.close()
    ok2 = check('strip image written', os.path.exists(out))
    return ok1 and ok2


# ─────────────────────────────────────────────────────────────────
#  Phase A2  2-D strip L=192, steps=400; 1-D N=192, steps=400
# ─────────────────────────────────────────────────────────────────
def test_A2():
    section('Phase A2 — Visualization frames  (L=192)')
    L = 192; sigma = 30.0; c = 0.5
    snap_steps = [0, 100, 200, 300, 400]
    f, g = ca.gaussian_spinor_2d((L, L), sigma=sigma, helicity='mixed')
    frames = []
    for step in range(max(snap_steps)+1):
        if step in snap_steps:
            frames.append((f.copy(), g.copy()))
        if step < max(snap_steps):
            f, g = ca.weyl_step_2d_splitstep(f, g, c)
    peak = max((np.abs(f0)**2+np.abs(g0)**2).max() for f0,g0 in frames)
    fig, axes = plt.subplots(1, len(frames), figsize=(12, 2.5))
    for ax, t_, (f0, g0) in zip(axes, snap_steps, frames):
        ax.imshow(sc.spinor_to_rgb(f0, g0, peak=peak), origin='lower')
        ax.set_title(f't={t_}'); ax.axis('off')
    plt.suptitle('Phase A2 — 2D strip  L=192'); plt.tight_layout()
    out1 = os.path.join(FIGURES_DIR, 'phaseA2_L192_strip.png')
    plt.savefig(out1, dpi=100, bbox_inches='tight'); plt.close()
    check('2D strip written', os.path.exists(out1))

    # 1-D spacetime
    N1 = 192; n_steps = 400
    x = np.arange(N1) - N1//2
    f1 = np.exp(-x**2/(2*25.0**2)).astype(complex)
    g1 = np.zeros(N1, dtype=complex)
    fh, gh = [f1.copy()], [g1.copy()]
    for _ in range(n_steps):
        f1, g1 = ca.weyl_step_2d_splitstep(f1.reshape(N1,1), g1.reshape(N1,1), c)
        f1 = f1.reshape(N1); g1 = g1.reshape(N1)
        fh.append(f1.copy()); gh.append(g1.copy())
    f_arr = np.array(fh); g_arr = np.array(gh)
    rgb_st = sc.spinor_to_rgb(f_arr, g_arr)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.imshow(rgb_st, origin='lower', aspect='auto')
    ax.set_xlabel('cell'); ax.set_ylabel('time step')
    ax.set_title('Phase A2 — 1D spacetime  L=192')
    out2 = os.path.join(FIGURES_DIR, 'phaseA2_L192_spacetime.png')
    plt.savefig(out2, dpi=100, bbox_inches='tight'); plt.close()
    ok2 = check('1D spacetime written', os.path.exists(out2))
    return ok2


# ─────────────────────────────────────────────────────────────────
#  Phase B1  L=192, n_steps=120, sigma=25
# ─────────────────────────────────────────────────────────────────
def test_B1():
    section('Phase B1 — Group-velocity measurement  (L=192)')
    all_ok = True
    fig, ax = plt.subplots(figsize=(7, 4))
    for k0 in [(0.3, 0.0), (0.0, 0.3), (0.4, 0.3), (0.6, 0.0)]:
        res = ca.measure_group_velocity_2d(L=192, n_steps=120, c=0.5,
                                           k0=k0, sigma=25.0)
        ok = abs(res['speed_ratio'] - 1.0) < 0.15
        all_ok = all_ok and ok
        check(f'k0={k0}', ok, f'speed_ratio={res["speed_ratio"]:.4f}')
        c_ = res['centroids']
        ax.plot(c_[:, 0], c_[:, 1], '-', label=str(k0))
    ax.set_xlabel('x centroid'); ax.set_ylabel('y centroid')
    ax.set_title('Phase B1 — group-velocity  L=192')
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    out = os.path.join(FIGURES_DIR, 'phaseB1_L192.png')
    plt.savefig(out, dpi=100, bbox_inches='tight'); plt.close()
    return all_ok


# ─────────────────────────────────────────────────────────────────
#  Phase B2  L sweep [32,48,64,96,128,192], sigma sweeps
# ─────────────────────────────────────────────────────────────────
def test_B2():
    section('Phase B2 — Size sweeps  (L up to 192)')
    L_res = ca.size_sweep_L([32, 48, 64, 96, 128, 192],
                             n_steps=120, c=0.5, sigma=20.0, k0=(0.6, 0.0))
    sigma_res = ca.size_sweep_sigma([3.0, 5.0, 8.0, 12.0, 18.0, 25.0],
                                     L=192, n_steps=80, c=0.5, k0=(0.6, 0.0))
    for r in L_res:
        print(f'  L={r["L"]:4d}  speed_ratio={r["speed_ratio"]:.4f}  norm_drift={r["norm_drift"]:.2e}')
    for r in sigma_res:
        print(f'  sigma={r["sigma"]:5.1f}  speed_ratio={r["speed_ratio"]:.4f}  frac_above_Nyq={r["frac_above_nyquist"]:.2e}')
    ok_L     = any(r['L'] >= 128 and r['speed_ratio'] > 0.9 for r in L_res)
    ok_sigma = any(r['sigma'] >= 18.0 and r['frac_above_nyquist'] < 1e-3 for r in sigma_res)
    check('L>=128 → speed_ratio>0.9', ok_L)
    check('sigma>=18 → <0.1% above Nyquist', ok_sigma)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.5))
    ax1.plot([r['L'] for r in L_res], [r['speed_ratio'] for r in L_res], 'o-')
    ax1.axhline(1.0, color='gray', ls='--'); ax1.set_xscale('log')
    ax1.set_xlabel('L'); ax1.set_ylabel('speed_ratio'); ax1.set_title('B2 L sweep')
    ax2.semilogy([r['sigma'] for r in sigma_res], [r['frac_above_nyquist'] for r in sigma_res], 's-')
    ax2.set_xlabel('sigma'); ax2.set_title('B2 sigma sweep')
    out = os.path.join(FIGURES_DIR, 'phaseB2_L192.png')
    plt.savefig(out, dpi=100, bbox_inches='tight'); plt.close()
    return ok_L and ok_sigma


# ─────────────────────────────────────────────────────────────────
#  Phase C1  L=192, n_steps=400 (Cayley LU at L=192 is fine)
# ─────────────────────────────────────────────────────────────────
def test_C1():
    section('Phase C1 — Variable-c refraction  (L=192)')
    L, n_steps, sigma = 192, 400, 25.0
    res_s = cv.measure_refraction(L=L, n_steps=n_steps, c_left=0.5, c_right=0.3,
                                   k_in=(0.5, 0.15), sigma=sigma,
                                   x_start_frac=0.25, method='strang', n_sub=4)
    res_b = cv.measure_refraction(L=L, n_steps=n_steps, c_left=0.5, c_right=0.3,
                                   k_in=(0.5, 0.15), sigma=sigma,
                                   x_start_frac=0.25, method='blend')
    res_c = cv.measure_refraction(L=L, n_steps=n_steps, c_left=0.5, c_right=0.3,
                                   k_in=(0.5, 0.15), sigma=sigma,
                                   x_start_frac=0.25, method='cayley')

    print(f'  Strang:  theta_out={res_s["theta_out_deg"]:.2f}° (Snell={res_s["theta_out_pred_deg"]:.2f}°)  norm_drift={res_s["norm_drift"]:.2e}')
    print(f'  Blend:   theta_out={res_b["theta_out_deg"]:.2f}°  norm_drift={res_b["norm_drift"]:.2e}')
    print(f'  Cayley:  theta_out={res_c["theta_out_deg"]:.2f}° (Snell={res_c["theta_out_pred_deg"]:.2f}°)  norm_drift={res_c["norm_drift"]:.2e}')

    err_s = abs(res_s['theta_out_deg'] - res_s['theta_out_pred_deg'])
    err_c = abs(res_c['theta_out_deg'] - res_c['theta_out_pred_deg'])
    ok1 = check('Strang within 1.5° of Snell', err_s < 1.5, f'(err={err_s:.2f}°)')
    ok2 = check('Strang norm drift <= blend', res_s['norm_drift'] <= res_b['norm_drift']*1.05,
                f'(strang={res_s["norm_drift"]:.2e}, blend={res_b["norm_drift"]:.2e})')
    ok3 = check('Cayley within 8° of Snell', err_c < 8.0, f'(err={err_c:.2f}°)')
    ok4 = check('Cayley norm drift < 1e-10 (exact-unitary)', res_c['norm_drift'] < 1e-10,
                f'(drift={res_c["norm_drift"]:.2e})')
    ratio = res_s['norm_drift'] / max(res_c['norm_drift'], 1e-18)
    ok5 = check('Cayley >= 1e10x better norm than Strang', ratio > 1e10,
                f'(ratio={ratio:.2e})')
    return ok1 and ok2 and ok3 and ok4 and ok5


# ─────────────────────────────────────────────────────────────────
#  Phase D1  L=192, zitterbewegung L=192 n_steps=3000
# ─────────────────────────────────────────────────────────────────
def test_D1():
    section('Phase D1 — Dirac CA  (L=192)')
    L = 192; shape = (L, L)

    # Weyl regression at m=0
    f, g   = ca.gaussian_spinor_2d(shape, sigma=20.0, helicity='left')
    nu, nd, xu, xd = dirac.gaussian_dirac_2d(shape, sigma=20.0, chirality='left')
    for _ in range(20):
        f,  g  = ce.weyl_step_2d_arccos_splitstep(f, g)
        nu, nd, xu, xd = dirac.dirac_step_2d_splitstep(nu, nd, xu, xd, m=0.0, dt=1.0)
    diff = max(float(np.max(np.abs(nu-f))), float(np.max(np.abs(nd-g))),
               float(np.max(np.abs(xu))),   float(np.max(np.abs(xd))))
    ok1 = check('Weyl regression at m=0', diff < 1e-13, f'(max diff={diff:.2e})')

    # Norm conservation
    nu, nd, xu, xd = dirac.gaussian_dirac_2d(shape, sigma=20.0, chirality='mixed')
    n0 = dirac.dirac_norm(nu, nd, xu, xd)
    for _ in range(1000):
        nu, nd, xu, xd = dirac.dirac_step_2d_splitstep(nu, nd, xu, xd, m=0.3, dt=1.0)
    drift = abs(dirac.dirac_norm(nu, nd, xu, xd) - n0) / n0
    ok2 = check('norm conservation 1000 steps m=0.3', drift < 1e-12, f'(drift={drift:.2e})')

    # Dispersion
    r = dirac.verify_dirac_dispersion_2d(L=192, n_steps=20, m=0.3)
    max_res = max(row['residual'] for row in r)
    ok3 = check('dispersion (exact-QCA)', max_res < 1e-13, f'(max res={max_res:.2e})')

    # Zitterbewegung at L=192, n_steps=3000, dt=0.5, sigma=50
    t, rho, fn, fa = dirac.measure_zitterbewegung_freq_2d(
        L=192, n_steps=3000, m=0.5, dt=0.5, sigma=50.0)
    err = abs(fn - fa) / fa
    bin_width = 2.0*np.pi / (len(t)*(t[1]-t[0]))
    ok4 = check('Zitterbewegung within FFT bin of 2·arcsin(m)', err < 0.05,
                f'(meas={fn:.5f}, analytic={fa:.5f}, err={err*100:.2f}%, bin={bin_width:.5f})')
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(t, rho, '-')
    ax.axhline(0.0, color='gray', ls='--', alpha=0.5)
    ax.set_xlabel('time'); ax.set_ylabel('rho_eta - rho_chi')
    ax.set_title(f'Phase D1 Zitterbewegung  L=192  measured={fn:.4f}, 2arcsin(m)={fa:.4f}')
    out = os.path.join(FIGURES_DIR, 'phaseD1_L192.png')
    plt.savefig(out, dpi=100, bbox_inches='tight'); plt.close()
    return ok1 and ok2 and ok3 and ok4


# ─────────────────────────────────────────────────────────────────
#  Phase E1  L=192, n_steps=100
# ─────────────────────────────────────────────────────────────────
def test_E1():
    section('Phase E1 — U(1) Aharonov–Bohm  (L=192)')
    res = dirac.aharonov_bohm_test(L=192, n_steps=100, m=0.0,
                                    q=1.0, dt=1.0, flux=np.pi, sigma=25.0)
    err = abs(res['measured_phase'] - res['analytic_phase'])
    ok1 = check('phase pickup at machine precision', err < 1e-12, f'(err={err:.2e})')
    ok2 = check('|overlap| = 1.0', abs(res['overlap_magnitude']-1.0) < 1e-12,
                f'(|olap|={res["overlap_magnitude"]:.10f})')
    ok3 = check('norm exactly preserved with A0',
                abs(res['norm_with_A0']-res['initial_norm']) < 1e-10,
                f'(drift={abs(res["norm_with_A0"]-res["initial_norm"]):.2e})')
    return ok1 and ok2 and ok3


# ─────────────────────────────────────────────────────────────────
#  Phase E2  L=192
# ─────────────────────────────────────────────────────────────────
def test_E2():
    section('Phase E2 — SU(2) parity violation  (L=192)')
    res = wk.parity_violation_test(L=192, n_steps=63, c=0.0, m_e=0.0,
                                    g_weak=1.0, dt=1.0, W3_value=0.1, sigma=25.0)
    pop_err = abs(res['left_e_pop_measured'] - res['left_e_pop_analytic'])
    pop_rel = pop_err / max(res['left_e_pop_analytic'], 1e-10)
    ok1 = check('left isospin rotation matches analytic', pop_rel < 0.05,
                f'(meas={res["left_e_pop_measured"]:.6f}, analytic={res["left_e_pop_analytic"]:.6f})')
    ok2 = check('right chirality immune to W', res['right_chi_pop_final']-res['right_chi_pop_initial'] < 1e-10)
    ok3 = check('zero leakage right→left', res['right_leakage_to_left'] < 1e-12,
                f'(leak={res["right_leakage_to_left"]:.2e})')
    return ok1 and ok2 and ok3


# ─────────────────────────────────────────────────────────────────
#  Phase E3  Discrete current conservation  (L=64 — fixed small)
# ─────────────────────────────────────────────────────────────────
def test_E3():
    section('Phase E3 — Discrete current conservation  (L=64)')
    L = 64; shape = (L, L)
    n_kin = 1.0; q = 1.0
    xs = np.arange(L); X, Y = np.meshgrid(xs, xs, indexing='ij')
    A0_uniform = np.full(shape, 0.1)

    def _rho_J(eu, ed, cu, cd):
        rho = np.abs(eu)**2 + np.abs(ed)**2 + np.abs(cu)**2 + np.abs(cd)**2
        Jx = 2*np.real(np.conj(eu)*ed) - 2*np.real(np.conj(cu)*cd)
        Jy = 2*np.imag(np.conj(eu)*ed) - 2*np.imag(np.conj(cu)*cd)
        return rho, Jx, Jy

    def residual(dt):
        nu, nd, xu, xd = dirac.gaussian_dirac_2d(shape, sigma=6.0, chirality='mixed')
        plane = np.exp(1j*0.30*X)
        nu = nu*plane; nd = nd*plane; xu = xu*plane; xd = xd*plane
        rho0, Jx0, Jy0 = _rho_J(nu, nd, xu, xd)
        nu1, nd1, xu1, xd1 = dirac.dirac_step_u1_2d_splitstep(
            nu, nd, xu, xd, A0=A0_uniform, m=0.0, q=q, dt=dt)
        rho1, Jx1, Jy1 = _rho_J(nu1, nd1, xu1, xd1)
        Jx_m = 0.5*(Jx0+Jx1); Jy_m = 0.5*(Jy0+Jy1)
        divJ = ((np.roll(Jx_m,-1,0)-np.roll(Jx_m,+1,0))/2 +
                (np.roll(Jy_m,-1,1)-np.roll(Jy_m,+1,1))/2)
        res = rho1 - rho0 + dt*n_kin*divJ
        return float(np.max(np.abs(res))), float(np.max(rho0))

    r1, rho_scale = residual(0.20)
    r2, _         = residual(0.10)
    r3, _         = residual(0.05)
    rat1 = r1/r2 if r2>0 else float('inf')
    rat2 = r2/r3 if r3>0 else float('inf')
    print(f'  U(1)  dt=0.20  rel={r1/rho_scale:.3e}')
    print(f'  U(1)  dt=0.10  rel={r2/rho_scale:.3e}')
    print(f'  U(1)  dt=0.05  rel={r3/rho_scale:.3e}')
    print(f'  Richardson ratios = {rat1:.2f}, {rat2:.2f}  (expect ~4 for O(dt^2))')
    ok_a = check('U(1) continuity O(dt^2)', 2.5<=rat1<=5.5 and 2.5<=rat2<=5.5,
                 f'(ratios {rat1:.2f}, {rat2:.2f})')

    # SU(2) local density invariance
    L2 = 32; shape2 = (L2, L2)
    G = np.exp(-((np.arange(L2)[:,None]-L2/2)**2 +
                 (np.arange(L2)[None,:]-L2/2)**2) / (2*4.0**2)).astype(complex)
    z = np.zeros_like(G)
    eta_nu = [G.copy(), z.copy()]; eta_e = [z.copy(), z.copy()]; chi_e = [z.copy(), z.copy()]
    rho_b = np.abs(eta_nu[0])**2+np.abs(eta_nu[1])**2+np.abs(eta_e[0])**2+np.abs(eta_e[1])**2
    W3 = np.full(shape2, 0.5); W0 = np.zeros(shape2)
    eta_nu_n, eta_e_n, chi_e_n = wk.step_weak_2d(eta_nu, eta_e, chi_e,
        W1=W0, W2=W0, W3=W3, c=0.0, m_e=0.0, g_weak=1.0, dt=1.0)
    rho_a = np.abs(eta_nu_n[0])**2+np.abs(eta_nu_n[1])**2+np.abs(eta_e_n[0])**2+np.abs(eta_e_n[1])**2
    drift = float(np.max(np.abs(rho_a-rho_b)))
    ok_b = check('SU(2) isospin preserves local rho', drift < 1e-12, f'(drift={drift:.2e})')
    return ok_a and ok_b


# ═════════════════════════════════════════════════════════════════
#  Main
# ═════════════════════════════════════════════════════════════════
def main():
    phases = [
        ('A1', test_A1),
        ('A2', test_A2),
        ('B1', test_B1),
        ('B2', test_B2),
        ('C1', test_C1),
        ('D1', test_D1),
        ('E1', test_E1),
        ('E2', test_E2),
        ('E3', test_E3),
    ]
    results = {}
    for name, fn in phases:
        t0 = time.time()
        try:
            ok = fn()
        except Exception as exc:
            print(f'  [ERROR]  {exc}')
            ok = False
        results[name] = {'pass': ok, 'seconds': round(time.time()-t0, 1)}
        print(f'  {elapsed()}  Phase {name}: {"PASS" if ok else "FAIL"}  ({results[name]["seconds"]:.1f}s)')

    print()
    print('='*70)
    print('  SUMMARY')
    print('='*70)
    passed = sum(1 for v in results.values() if v['pass'])
    for k, v in results.items():
        mark = 'PASS' if v['pass'] else 'FAIL'
        print(f'  [{mark}]  Phase {k}  ({v["seconds"]:.1f}s)')
    print(f'\n  {passed}/{len(phases)} phases passed  |  total {elapsed()}')

    out_json = os.path.join(os.path.dirname(__file__), '..', 'test-results', 'phaseAE_L192.json')
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'  Results: {out_json}')
    return 0 if passed == len(phases) else 1


if __name__ == '__main__':
    sys.exit(main())
