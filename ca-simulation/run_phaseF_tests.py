"""
run_phaseF_tests.py  —  Phase F: Higgs + Yukawa proposition tests
====================================================================
Tests F1 (vacuum regression), F2 (Higgs dispersion), F3 (sketch),
and F4 (symmetry-restored massless fermions).

F1: contract test.  Φ = v constant, no fermion back-reaction (yet).
    The Dirac field should evolve identically to the constant-m Dirac
    CA with m = y·v.

F2: Higgs propagation.  Around the vacuum, the radial mode of Φ
    propagates with mass m_h = √(2μ²); the angular (Goldstone) mode
    is massless.

F3: Sketch.  A fermion density spike depresses |Φ|; if c(x) = c_0·(|Φ|/v)^-α,
    that depression changes c.  Demonstrating gravitational attraction
    requires the full variable-c stepper plus a stable backreaction; this
    test only reports the |Φ| depression magnitude, not a refraction
    measurement.

F4: Symmetry restored.  Use V = +μ²|Φ|² + λ|Φ|⁴ with Φ = 0 as vacuum.
    Fermions are massless; the Weyl regression should hold.
"""

import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ca_core as ca
import ca_dirac as dirac
import ca_higgs as hg
import ca_unified as un

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
#  F1 — Vacuum regression contract
# ══════════════════════════════════════════════════════════════════

def test_F1():
    section('Phase F1 — Vacuum regression: Φ=v reduces to constant-m Dirac')

    L = 32; shape = (L, L)
    mu2, lam, y = 0.5, 0.5, 0.6
    v = float(np.sqrt(mu2 / (2 * lam)))
    m_const = y * v
    print(f'  Setup: v = sqrt(mu²/2λ) = {v:.4f},  y = {y},  m_eff = yv = {m_const:.4f}')

    # Reference: constant-m Dirac CA
    nu_ref, nd_ref, xu_ref, xd_ref = dirac.gaussian_dirac_2d(
        shape, sigma=3.0, chirality='mixed')
    for _ in range(100):
        nu_ref, nd_ref, xu_ref, xd_ref = dirac.dirac_step_2d_splitstep(
            nu_ref, nd_ref, xu_ref, xd_ref, c=0.5, m=m_const, dt=1.0)

    # Unified CA with Φ=v fixed (vacuum)
    state, v_check = un.setup_vacuum(shape, mu2, lam, fermion='mixed', sigma=3.0)
    assert abs(v_check - v) < 1e-12
    for _ in range(100):
        state = un.unified_step(state, mu2, lam, yukawa=y, c=0.5, dt=1.0)

    # Φ should still be exactly v
    phi_drift = float(np.max(np.abs(state.Phi - v)))
    pi_drift  = float(np.max(np.abs(state.Pi)))

    # Fermion fields should match the reference run
    diff = max(
        float(np.max(np.abs(state.eta_u - nu_ref))),
        float(np.max(np.abs(state.eta_d - nd_ref))),
        float(np.max(np.abs(state.chi_u - xu_ref))),
        float(np.max(np.abs(state.chi_d - xd_ref))),
    )

    ok_phi = check('Φ stays exactly at v (vacuum stability)',
                   phi_drift < 1e-12 and pi_drift < 1e-12,
                   f'(|Φ−v|={phi_drift:.2e}, |Π|={pi_drift:.2e})')
    ok_fermion = check('Fermion field matches constant-m Dirac reference',
                       diff < 1e-12, f'(max diff = {diff:.2e})')
    return ok_phi and ok_fermion


# ══════════════════════════════════════════════════════════════════
#  F2 — Higgs and Goldstone dispersions
# ══════════════════════════════════════════════════════════════════

def test_F2():
    section('Phase F2 — Higgs and Goldstone dispersions')

    mu2, lam = 0.5, 0.5
    m_h = float(np.sqrt(2 * mu2))

    r_h = hg.verify_higgs_dispersion_2d(L=64, n_steps=20, mu2=mu2, lam=lam,
                                          dt=0.15, mode='radial')
    r_g = hg.verify_higgs_dispersion_2d(L=64, n_steps=20, mu2=mu2, lam=lam,
                                          dt=0.5, mode='goldstone')

    print(f'  m_h (analytic) = sqrt(2μ²) = {m_h:.4f}')
    print('  Radial (Higgs):')
    for r in r_h:
        print(f'    |k|={r["kappa"]:.4f}  ω_an={r["omega_analytic"]:.4f}'
              f'  ω_num={r["omega_numeric"]:.4f}  res={r["residual"]:.4e}')
    print('  Angular (Goldstone, should be massless):')
    for r in r_g:
        print(f'    |k|={r["kappa"]:.4f}  ω_an={r["omega_analytic"]:.4f}'
              f'  ω_num={r["omega_numeric"]:.4f}  res={r["residual"]:.4e}')

    max_h = max(r['residual'] for r in r_h)
    max_g = max(r['residual'] for r in r_g)
    ok_h = check('Higgs (radial) dispersion within 1% of √(k² + 2μ²)',
                 max_h < 0.01, f'(max res = {max_h:.2e})')
    ok_g = check('Goldstone dispersion ω = |k| to <0.5% (massless)',
                 max_g < 0.005, f'(max res = {max_g:.2e})')

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ks = [r['kappa'] for r in r_h]
    ax1.plot(ks, [r['omega_analytic'] for r in r_h], 'b-', label='analytic')
    ax1.plot(ks, [r['omega_numeric']  for r in r_h], 'ro', label='numeric')
    ax1.set_xlabel('|k|'); ax1.set_ylabel('ω')
    ax1.set_title('Higgs (radial): ω = √(k² + 2μ²)'); ax1.legend()
    ax1.grid(alpha=0.3)
    ax2.plot(ks, [r['omega_analytic'] for r in r_g], 'b-', label='analytic')
    ax2.plot(ks, [r['omega_numeric']  for r in r_g], 'ro', label='numeric')
    ax2.set_xlabel('|k|'); ax2.set_ylabel('ω')
    ax2.set_title('Goldstone: ω = |k|'); ax2.legend()
    ax2.grid(alpha=0.3)
    out = os.path.join(FIGURES_DIR, 'phaseF2_higgs_dispersion.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()
    check('dispersion figure written', os.path.exists(out), f'-> {out}')
    return ok_h and ok_g


# ══════════════════════════════════════════════════════════════════
#  F3 — Gravitational attraction sketch
# ══════════════════════════════════════════════════════════════════

def test_F3():
    section('Phase F3 — Gravitational-attraction sketch (Φ depression near fermion density)')

    # Sketch only.  A proper backreaction needs a symplectic coupling
    # derived from the joint Lagrangian; the hand-coded source below
    # *demonstrates* the depression effect for small amplitudes and
    # short times but is not energy-conserving long-term.

    L = 64; shape = (L, L)
    mu2, lam, y = 0.5, 0.5, 0.2   # gentle Yukawa
    v = float(np.sqrt(mu2 / (2 * lam)))

    state, _ = un.setup_vacuum(shape, mu2, lam, fermion='mixed', sigma=5.0)
    cx, cy = L // 2, L // 2

    # Yukawa source: ∂_t Π_Φ −= y · 2·Re(η†χ)
    phi_centers = [float(np.abs(state.Phi[cx, cy]))]
    times = [0.0]
    dt = 0.5
    n_steps = 30
    diverged = False
    for step in range(n_steps):
        psi_bar_psi = 2.0 * np.real(
            np.conj(state.eta_u) * state.chi_u +
            np.conj(state.eta_d) * state.chi_d
        )
        state.Pi -= 0.5 * dt * y * psi_bar_psi
        state = un.unified_step(state, mu2, lam, yukawa=y, c=0.5, dt=dt)
        state.Pi -= 0.5 * dt * y * psi_bar_psi

        val = float(np.abs(state.Phi[cx, cy]))
        if not np.isfinite(val) or val > 100.0:
            diverged = True
            break
        phi_centers.append(val)
        times.append((step + 1) * dt)

    phi_centers = np.array(phi_centers)
    times = np.array(times)
    max_dev = float(np.max(np.abs(phi_centers - v)))
    print(f'  Vacuum v = {v:.4f}')
    print(f'  Effective fermion mass at vacuum = y·v = {y*v:.4f}')
    print(f'  |Φ| at center range: [{phi_centers.min():.4f}, {phi_centers.max():.4f}]')
    print(f'  Max deviation from v: {max_dev:.4e}')
    if diverged:
        print(f'  Run stopped early due to divergence (expected with hand-coded source)')

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(times, phi_centers, 'b-', label='|Φ| at fermion center')
    ax.axhline(v, color='gray', linestyle='--', label=f'vacuum v = {v:.3f}')
    ax.set_xlabel('time'); ax.set_ylabel('|Φ|')
    ax.set_title('Phase F3 — Yukawa back-reaction (sketch): Φ depressed by fermion density')
    ax.legend(); ax.grid(alpha=0.3)
    out = os.path.join(FIGURES_DIR, 'phaseF3_gravity_sketch.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()

    # Informational pass: depression observed AND |Φ| varied
    ok = (max_dev > 1e-6) and (max_dev < 10.0)
    check('Φ deflection observed at fermion location (sketch)',
          ok, f'(max |Φ−v| = {max_dev:.2e})')
    return ok


# ══════════════════════════════════════════════════════════════════
#  F4 — Symmetry-restored phase: massless fermions
# ══════════════════════════════════════════════════════════════════

def test_F4():
    section('Phase F4 — Symmetry restored: Φ=0, fermions massless, Weyl recovered')

    L = 32; shape = (L, L)
    # Use V_high = +μ²|Φ|² + λ|Φ|⁴ (positive μ²) — vacuum at Φ=0.
    # In our potential parameterization V(|Φ|²) = -μ²|Φ|² + λ|Φ|⁴ we
    # achieve this by passing a *negative* μ² value to the Φ stepper.
    mu2_neg = -0.5    # → effective V = +0.5|Φ|² + λ|Φ|⁴, minimum at Φ=0
    lam = 0.5
    y = 0.6

    state = un.setup_symmetry_restored(shape, abs(mu2_neg), lam,
                                         fermion='left', sigma=3.0)
    # Reference: pure Weyl evolution at c=0.5
    f_ref, g_ref = ca.gaussian_spinor_2d(shape, sigma=3.0, helicity='left')
    for _ in range(50):
        f_ref, g_ref = ca.weyl_step_2d_splitstep(f_ref, g_ref, c=0.5)
        state = un.unified_step(state, mu2_neg, lam, yukawa=y, c=0.5, dt=1.0)

    phi_drift = float(np.max(np.abs(state.Phi)))
    pi_drift  = float(np.max(np.abs(state.Pi)))
    # η_u should match f_ref (Weyl), η_d should match g_ref, χ stays zero
    diff_eu = float(np.max(np.abs(state.eta_u - f_ref)))
    diff_ed = float(np.max(np.abs(state.eta_d - g_ref)))
    chi_max = float(np.max(np.abs(state.chi_u) + np.abs(state.chi_d)))

    ok_phi = check('Φ remains at 0 (high-T vacuum stable)',
                   phi_drift < 1e-12 and pi_drift < 1e-12,
                   f'(|Φ|={phi_drift:.2e}, |Π|={pi_drift:.2e})')
    ok_weyl = check('η matches Weyl reference (massless)',
                    max(diff_eu, diff_ed) < 1e-12,
                    f'(max diff = {max(diff_eu, diff_ed):.2e})')
    ok_chi = check('χ stays zero (no mass mixing)',
                   chi_max < 1e-12, f'(|χ|max = {chi_max:.2e})')
    return ok_phi and ok_weyl and ok_chi


# ══════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════

def main():
    results = {}
    results['F1'] = test_F1()
    results['F2'] = test_F2()
    results['F3'] = test_F3()
    results['F4'] = test_F4()

    print()
    print('=' * 72)
    print('  PHASE F SUMMARY')
    print('=' * 72)
    for ph, ok in results.items():
        print(f'  [{"PASS" if ok else "FAIL"}]  Phase {ph}')
    print(f'\n  {sum(results.values())} / {len(results)} F-phases passed')

    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
