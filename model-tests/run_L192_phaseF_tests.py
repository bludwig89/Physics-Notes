"""
run_L192_phaseF_tests.py  —  Phase F test suite capped at L=192
================================================================
F1  Vacuum regression (Φ=v → constant-m Dirac reference)
F2  Higgs + Goldstone dispersions
F3  Symplectic Yukawa back-reaction (energy bounded)
F3b Newtonian gravity demo (Cayley variable-c, Φ-sourced c(x))
F4  Symmetry-restored phase (Φ=0, massless Weyl)
"""

import os, sys, json, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ca-simulation'))
import ca_core as ca
import ca_dirac as dirac
import ca_higgs as hg
import ca_unified as un
import ca_curved as cv
import ca_core_exact as ce

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
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
#  F1  L=192, sigma=20, 100 steps — vacuum stability + Dirac match
# ─────────────────────────────────────────────────────────────────
def test_F1():
    section('Phase F1 — Vacuum regression  (L=192)')
    L = 192; shape = (L, L)
    mu2, lam, y = 0.5, 0.5, 0.6
    v = float(np.sqrt(mu2 / (2*lam)))
    m_const = y * v
    print(f'  v={v:.4f}  m_eff=y·v={m_const:.4f}')

    # Reference: constant-m Dirac
    nu_r, nd_r, xu_r, xd_r = dirac.gaussian_dirac_2d(shape, sigma=20.0, chirality='mixed')
    for _ in range(100):
        nu_r, nd_r, xu_r, xd_r = dirac.dirac_step_2d_splitstep(
            nu_r, nd_r, xu_r, xd_r, m=m_const, dt=1.0)

    # Unified CA with Φ=v
    state, v_check = un.setup_vacuum(shape, mu2, lam, fermion='mixed', sigma=20.0)
    assert abs(v_check - v) < 1e-12
    # n_phi_sub=2 to satisfy CFL at this dt (Finding 4)
    for _ in range(100):
        state = un.unified_step(state, mu2, lam, yukawa=y, dt=1.0, n_phi_sub=2)

    phi_drift = float(np.max(np.abs(state.Phi - v)))
    pi_drift  = float(np.max(np.abs(state.Pi)))
    diff = max(float(np.max(np.abs(state.eta_u - nu_r))),
               float(np.max(np.abs(state.eta_d - nd_r))),
               float(np.max(np.abs(state.chi_u - xu_r))),
               float(np.max(np.abs(state.chi_d - xd_r))))

    ok1 = check('Φ stays exactly at v', phi_drift < 1e-12 and pi_drift < 1e-12,
                f'(|Φ−v|={phi_drift:.2e}, |Π|={pi_drift:.2e})')
    ok2 = check('Fermion matches constant-m Dirac', diff < 1e-12,
                f'(max diff={diff:.2e})')
    return ok1 and ok2


# ─────────────────────────────────────────────────────────────────
#  F2  L=192 Higgs + Goldstone
# ─────────────────────────────────────────────────────────────────
def test_F2():
    section('Phase F2 — Higgs + Goldstone dispersions  (L=192)')
    mu2, lam = 0.5, 0.5
    m_h = float(np.sqrt(2*mu2))
    r_h = hg.verify_higgs_dispersion_2d(L=192, n_steps=20, mu2=mu2, lam=lam,
                                         dt=0.15, mode='radial')
    r_g = hg.verify_higgs_dispersion_2d(L=192, n_steps=20, mu2=mu2, lam=lam,
                                         dt=0.5, mode='goldstone')
    print(f'  m_h (analytic) = sqrt(2mu2) = {m_h:.4f}')
    print('  Radial (Higgs):')
    for r in r_h:
        print(f'    |k|={r["kappa"]:.4f}  omega_an={r["omega_analytic"]:.4f}'
              f'  omega_num={r["omega_numeric"]:.4f}  res={r["residual"]:.4e}')
    print('  Angular (Goldstone):')
    for r in r_g:
        print(f'    |k|={r["kappa"]:.4f}  omega_an={r["omega_analytic"]:.4f}'
              f'  omega_num={r["omega_numeric"]:.4f}  res={r["residual"]:.4e}')
    max_h = max(r['residual'] for r in r_h)
    max_g = max(r['residual'] for r in r_g)
    ok1 = check('Higgs radial within 1% of sqrt(k^2+2mu^2)', max_h < 0.01,
                f'(max res={max_h:.2e})')
    ok2 = check('Goldstone massless within 0.5%', max_g < 0.005,
                f'(max res={max_g:.2e})')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ks = [r['kappa'] for r in r_h]
    ax1.plot(ks, [r['omega_analytic'] for r in r_h], 'b-', label='analytic')
    ax1.plot(ks, [r['omega_numeric']  for r in r_h], 'ro', label='numeric')
    ax1.set_xlabel('|k|'); ax1.set_ylabel('omega'); ax1.set_title('Higgs radial  L=192')
    ax1.legend(); ax1.grid(alpha=0.3)
    ax2.plot(ks, [r['omega_analytic'] for r in r_g], 'b-', label='analytic')
    ax2.plot(ks, [r['omega_numeric']  for r in r_g], 'ro', label='numeric')
    ax2.set_xlabel('|k|'); ax2.set_title('Goldstone  L=192'); ax2.legend(); ax2.grid(alpha=0.3)
    out = os.path.join(FIGURES_DIR, 'phaseF2_L192.png')
    plt.savefig(out, dpi=100, bbox_inches='tight'); plt.close()
    return ok1 and ok2


# ─────────────────────────────────────────────────────────────────
#  F3  Symplectic Yukawa back-reaction  L=192, 200 steps
# ─────────────────────────────────────────────────────────────────
def test_F3():
    section('Phase F3 — Symplectic Yukawa back-reaction  (L=192)')
    L = 192; shape = (L, L)
    mu2, lam, y = 0.5, 0.5, 0.2
    v = float(np.sqrt(mu2 / (2*lam)))
    state, _ = un.setup_vacuum(shape, mu2, lam, fermion='mixed', sigma=20.0)
    cx, cy = L//2, L//2
    dt = 0.5; n_steps = 200
    H0 = un.total_energy(state, mu2, lam, y)
    phi_centers = [float(np.abs(state.Phi[cx, cy]))]
    H_trace = [H0]; times = [0.0]; diverged = False
    for step in range(n_steps):
        state = un.unified_step(state, mu2, lam, yukawa=y, dt=dt, back_react=True)
        val = float(np.abs(state.Phi[cx, cy]))
        if not np.isfinite(val) or val > 100.0:
            diverged = True; break
        H_trace.append(un.total_energy(state, mu2, lam, y))
        phi_centers.append(val); times.append((step+1)*dt)
    phi_centers = np.array(phi_centers); H_trace = np.array(H_trace); times = np.array(times)
    max_dev = float(np.max(np.abs(phi_centers - v)))
    H_drift = float(np.max(np.abs(H_trace - H0)))
    H_rel   = H_drift / (abs(H0) + 1e-30)
    print(f'  v={v:.4f}  |Phi| range=[{phi_centers.min():.4f},{phi_centers.max():.4f}]')
    print(f'  max|Phi-v|={max_dev:.4e}  H_rel={H_rel:.4%}  diverged={diverged}')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
    ax1.plot(times, phi_centers, 'b-'); ax1.axhline(v, color='gray', ls='--', label=f'v={v:.3f}')
    ax1.set_ylabel('|Phi|'); ax1.legend(); ax1.set_title('F3 Symplectic Yukawa  L=192')
    ax2.plot(times, H_trace-H0, 'r-'); ax2.axhline(0, color='gray', ls='--', alpha=0.5)
    ax2.set_xlabel('time'); ax2.set_ylabel('DeltaH')
    out = os.path.join(FIGURES_DIR, 'phaseF3_L192.png')
    plt.savefig(out, dpi=100, bbox_inches='tight'); plt.close()
    ok1 = check('Phi depression observed', not diverged and max_dev > 1e-6 and max_dev < 10.0,
                f'(max|Phi-v|={max_dev:.2e})')
    ok2 = check('Energy bounded <5%', not diverged and H_rel < 0.05,
                f'(H_rel={H_rel:.3%})')
    return ok1 and ok2


# ─────────────────────────────────────────────────────────────────
#  F3b  Newtonian gravity demo  L=192 (down from L=960)
#  Cayley LU at L=192 is ~36K DOF — easily fits in RAM
# ─────────────────────────────────────────────────────────────────
def test_F3b():
    section('Phase F3b — Newtonian gravity demo Cayley variable-c  (L=192)')
    L = 192; shape = (L, L)
    mu2, lam = 0.5, 0.5
    v = float(np.sqrt(mu2/(2*lam)))
    alpha = 1.5
    cx0, cy0 = L//2, L//2

    # Build a static |Phi| depression at the centre
    xs = np.arange(L); X, Y = np.meshgrid(xs, xs, indexing='ij')
    r2 = (X - cx0)**2 + (Y - cy0)**2
    w_dep = L // 8          # depression width (scaled from L=960 w=120)
    dep_depth = 0.15
    Phi_static = v * (1.0 - dep_depth * np.exp(-r2 / (2*w_dep**2)))

    # c field: c(x) = c0 * (|Phi|/v)^alpha  — lower c where Phi is depressed
    c0 = 0.5
    c_field = c0 * (Phi_static / v)**alpha
    print(f'  c_min={c_field.min():.4f}  c_max={c_field.max():.4f}  v={v:.4f}')

    # Probe packet entering from left, aimed at y=cy0 + offset
    impact = L // 8         # impact parameter (scaled)
    k_in_x = 0.4
    sigma_p = max(L // 12, 8)
    f_pr, g_pr = ca.gaussian_spinor_2d(shape, sigma=float(sigma_p),
                                        center=(L//6, cy0 + impact),
                                        helicity='left')
    # Imprint a plane-wave momentum kick in x
    xs = np.arange(L)
    X2, _ = np.meshgrid(xs, xs, indexing='ij')
    kick = np.exp(1j * k_in_x * X2)
    f_pr = f_pr * kick; g_pr = g_pr * kick

    # Free-propagation baseline (uniform c=c0)
    n_steps = L // 2
    f_free = f_pr.copy(); g_free = g_pr.copy()
    for _ in range(n_steps):
        f_free, g_free = ca.weyl_step_2d_splitstep(f_free, g_free, c=c0)

    # Cayley variable-c propagation
    f_bent = f_pr.copy(); g_bent = g_pr.copy()
    norm0 = float(np.sum(np.abs(f_bent)**2 + np.abs(g_bent)**2))
    try:
        solver = cv.CayleyVarcSolver2D(c_field)
        for _ in range(n_steps):
            f_bent, g_bent = solver.step(f_bent, g_bent)
        norm1 = float(np.sum(np.abs(f_bent)**2 + np.abs(g_bent)**2))
        norm_drift = abs(norm1 - norm0) / norm0
        cayley_ok = True
    except Exception as exc:
        print(f'  Cayley solver failed: {exc}')
        cayley_ok = False; norm_drift = float('nan')

    if cayley_ok:
        # Measure centroid deflection
        rho_free = np.abs(f_free)**2 + np.abs(g_free)**2
        rho_bent = np.abs(f_bent)**2 + np.abs(g_bent)**2
        cy_free = float(np.sum(Y * rho_free) / np.sum(rho_free))
        cy_bent = float(np.sum(Y * rho_bent) / np.sum(rho_bent))
        deflection = cy_bent - cy_free    # positive = toward centre (bent inward)
        print(f'  cy_free={cy_free:.2f}  cy_bent={cy_bent:.2f}  deflection={deflection:.2f} cells')
        print(f'  norm drift={norm_drift:.2e}')
        ok1 = check('Cayley norm at machine precision', norm_drift < 1e-10,
                    f'(drift={norm_drift:.2e})')
        # Deflection toward centre (cy0) means cy_bent < cy_free for positive impact
        toward_centre = (deflection * (cy0 - (cy0 + impact))) > 0  if impact != 0 else True
        ok2 = check('Probe bends toward mass (gravity-like deflection)', toward_centre,
                    f'(deflection={deflection:.2f} cells, impact={impact})')

        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        im0 = axes[0].imshow(c_field.T, origin='lower', aspect='auto')
        axes[0].set_title('c(x) field'); plt.colorbar(im0, ax=axes[0])
        axes[1].imshow(rho_free.T, origin='lower', aspect='auto')
        axes[1].set_title(f'free  cy={cy_free:.1f}')
        axes[2].imshow(rho_bent.T, origin='lower', aspect='auto')
        axes[2].set_title(f'bent  cy={cy_bent:.1f}  defl={deflection:.1f}')
        for ax in axes: ax.set_xticks([]); ax.set_yticks([])
        plt.suptitle('F3b Newtonian gravity demo  L=192')
        plt.tight_layout()
        out = os.path.join(FIGURES_DIR, 'phaseF3b_L192.png')
        plt.savefig(out, dpi=100, bbox_inches='tight'); plt.close()
        return ok1 and ok2
    else:
        check('Cayley solver ran', False, '(exception)')
        return False


# ─────────────────────────────────────────────────────────────────
#  F4  Symmetry-restored phase  L=192
# ─────────────────────────────────────────────────────────────────
def test_F4():
    section('Phase F4 — Symmetry-restored phase  (L=192)')
    L = 192; shape = (L, L)
    mu2, lam, y = 0.5, 0.5, 0.6   # high-T phase: V=+mu2|Phi|^2+lam|Phi|^4

    state = un.setup_symmetry_restored(shape, mu2, lam, fermion='left', sigma=20.0)

    # Reference: pure exact-QCA Weyl at m=0
    f_ref, g_ref = ca.gaussian_spinor_2d(shape, sigma=20.0, helicity='left')
    for _ in range(50):
        f_ref, g_ref = ce.weyl_step_2d_arccos_splitstep(f_ref, g_ref)
        state = un.unified_step(state, mu2, lam, yukawa=y, dt=1.0,
                                phase='symmetric')

    phi_final = float(np.max(np.abs(state.Phi)))
    pi_final  = float(np.max(np.abs(state.Pi)))
    diff_eu = float(np.max(np.abs(state.eta_u - f_ref)))
    diff_ed = float(np.max(np.abs(state.eta_d - g_ref)))
    chi_mag = float(np.max(np.abs(state.chi_u)) + np.max(np.abs(state.chi_d)))
    print(f'  phi_final={phi_final:.2e}  pi_final={pi_final:.2e}')
    print(f'  eta_u match={diff_eu:.2e}  eta_d match={diff_ed:.2e}  chi={chi_mag:.2e}')

    ok1 = check('Phi=0 preserved (high-T vacuum)', phi_final < 1e-12 and pi_final < 1e-12,
                f'(|Phi|={phi_final:.2e}, |Pi|={pi_final:.2e})')
    ok2 = check('eta matches exact-QCA Weyl reference', max(diff_eu,diff_ed) < 1e-12,
                f'(max diff={max(diff_eu,diff_ed):.2e})')
    ok3 = check('chi stays zero (massless)', chi_mag < 1e-12,
                f'(chi mag={chi_mag:.2e})')
    return ok1 and ok2 and ok3


# ═════════════════════════════════════════════════════════════════
#  Main
# ═════════════════════════════════════════════════════════════════
def main():
    phases = [
        ('F1', test_F1),
        ('F2', test_F2),
        ('F3', test_F3),
        ('F3b', test_F3b),
        ('F4', test_F4),
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
    print('  PHASE F SUMMARY')
    print('='*70)
    passed = sum(1 for v in results.values() if v['pass'])
    for k, v in results.items():
        print(f'  [{"PASS" if v["pass"] else "FAIL"}]  Phase {k}  ({v["seconds"]:.1f}s)')
    print(f'\n  {passed}/{len(phases)} passed  |  total {elapsed()}')

    out_json = os.path.join(os.path.dirname(__file__), '..', 'test-results', 'phaseF_L192.json')
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'  Results: {out_json}')
    return 0 if passed == len(phases) else 1


if __name__ == '__main__':
    sys.exit(main())
