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
import ca_curved as cc

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

    # 10× bump (2026-05-16): L=32→320, σ=3→30.
    L = 320; shape = (L, L)
    mu2, lam, y = 0.5, 0.5, 0.6
    v = float(np.sqrt(mu2 / (2 * lam)))
    m_const = y * v
    print(f'  Setup: v = sqrt(mu²/2λ) = {v:.4f},  y = {y},  m_eff = yv = {m_const:.4f}')

    # Reference: constant-m Dirac CA (exact-QCA — `c` argument removed,
    # the kinetic coefficient n = √(1−m²) is derived from m internally).
    nu_ref, nd_ref, xu_ref, xd_ref = dirac.gaussian_dirac_2d(
        shape, sigma=30.0, chirality='mixed')
    for _ in range(100):
        nu_ref, nd_ref, xu_ref, xd_ref = dirac.dirac_step_2d_splitstep(
            nu_ref, nd_ref, xu_ref, xd_ref, m=m_const, dt=1.0)

    # Unified CA with Φ=v fixed (vacuum)
    state, v_check = un.setup_vacuum(shape, mu2, lam, fermion='mixed', sigma=30.0)
    assert abs(v_check - v) < 1e-12
    for _ in range(100):
        state = un.unified_step(state, mu2, lam, yukawa=y, dt=1.0)

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

    # 10× bump (2026-05-16): L=64→640
    r_h = hg.verify_higgs_dispersion_2d(L=640, n_steps=20, mu2=mu2, lam=lam,
                                          dt=0.15, mode='radial')
    r_g = hg.verify_higgs_dispersion_2d(L=640, n_steps=20, mu2=mu2, lam=lam,
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
    section('Phase F3 — Gravitational-attraction (symplectic Yukawa back-reaction, P1)')

    # P1 (2026-05-15).  The Yukawa back-reaction is now derived from the
    # joint Hamiltonian H = H_KG + H_Dirac_kin + H_Y and integrated via a
    # Strang split that wraps the Dirac step in two half-kicks
    # Π −= dt/2·y·χ†η.  This composition is symplectic — total energy
    # drifts by O(dt²) per step, bounded over arbitrary run length.

    # 10× bump (2026-05-16): L=64→640, σ=5→50
    L = 640; shape = (L, L)
    mu2, lam, y = 0.5, 0.5, 0.2
    v = float(np.sqrt(mu2 / (2 * lam)))

    state, _ = un.setup_vacuum(shape, mu2, lam, fermion='mixed', sigma=50.0)
    cx, cy = L // 2, L // 2

    dt = 0.5
    n_steps = 200

    H0 = un.total_energy(state, mu2, lam, y)
    phi_centers = [float(np.abs(state.Phi[cx, cy]))]
    H_trace     = [H0]
    times       = [0.0]
    diverged = False

    for step in range(n_steps):
        state = un.unified_step(state, mu2, lam, yukawa=y,
                                  dt=dt, back_react=True)
        val = float(np.abs(state.Phi[cx, cy]))
        if not np.isfinite(val) or val > 100.0:
            diverged = True
            break
        H_trace.append(un.total_energy(state, mu2, lam, y))
        phi_centers.append(val)
        times.append((step + 1) * dt)

    phi_centers = np.array(phi_centers)
    H_trace     = np.array(H_trace)
    times       = np.array(times)
    max_dev   = float(np.max(np.abs(phi_centers - v)))
    H_drift   = float(np.max(np.abs(H_trace - H0)))
    H_rel     = H_drift / (abs(H0) + 1e-30)

    print(f'  Vacuum v = {v:.4f}')
    print(f'  Effective fermion mass at vacuum = y·v = {y*v:.4f}')
    print(f'  |Φ| at center range: [{phi_centers.min():.4f}, {phi_centers.max():.4f}]')
    print(f'  Max deviation from v: {max_dev:.4e}')
    print(f'  Initial H = {H0:.6e}')
    print(f'  Max |H − H0| over {n_steps} steps = {H_drift:.4e}  ({H_rel:.2%})')
    if diverged:
        print(f'  Run diverged at step {step}')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    ax1.plot(times, phi_centers, 'b-', label='|Φ| at fermion center')
    ax1.axhline(v, color='gray', linestyle='--', label=f'vacuum v = {v:.3f}')
    ax1.set_ylabel('|Φ|'); ax1.legend(); ax1.grid(alpha=0.3)
    ax1.set_title('Phase F3 — Symplectic Yukawa back-reaction (P1)')
    ax2.plot(times, H_trace - H0, 'r-', label='ΔH = H(t) − H(0)')
    ax2.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('time'); ax2.set_ylabel('ΔH')
    ax2.legend(); ax2.grid(alpha=0.3)
    out = os.path.join(FIGURES_DIR, 'phaseF3_gravity_symplectic.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()

    # Two checks now:
    #  1. Φ depression is observed (qualitative back-reaction).
    #  2. Total energy is bounded — the symplectic split's main contract.
    ok_depression = (not diverged) and (max_dev > 1e-6) and (max_dev < 10.0)
    ok_energy     = (not diverged) and (H_rel < 0.05)   # <5% drift over 200 steps
    check('Φ deflection observed at fermion location',
          ok_depression, f'(max |Φ−v| = {max_dev:.2e})')
    check('Total energy bounded (symplectic)',
          ok_energy, f'(max |ΔH|/H₀ = {H_rel:.2%} over {n_steps} steps)')
    return ok_depression and ok_energy


# ══════════════════════════════════════════════════════════════════
#  F3b — Newtonian-gravity demo: c(x) sourced by |Φ|, probe refracts
# ══════════════════════════════════════════════════════════════════

def test_F3b():
    section('Phase F3b — Newtonian gravity demo (Cayley variable-c + Φ source, P3)')

    # Setup: a static |Φ| depression at the lattice centre (representing the
    # back-reaction from a fermion mass concentration after F3 settles).  A
    # probe Weyl packet enters from the left; we measure the deflection of
    # its trajectory toward the centre vs. straight-line free propagation.
    # 10× bump (2026-05-16): L=96→960.  Cayley LU at L=960 needs ~5 GB.
    # If memory-bound, drop to L=384 with proportionally scaled lengths.
    L = 960; shape = (L, L)
    mu2, lam = 0.5, 0.5
    v = float(np.sqrt(mu2 / (2 * lam)))
    alpha = 1.5                          # metric-coupling exponent  (free parameter — see model review)
    cx0, cy0 = L // 2, L // 2

    # Build a static |Φ| field with a Gaussian depression centred on the
    # lattice.  F3 showed fermion density depresses |Φ|, so this static
    # profile stands in for the F3 back-reaction at equilibrium.
    # Coupling:  c(x) = c_0 · (|Φ(x)|/v)^(+α).
    # Depression (|Φ|<v) → c<c_0 at the centre → slower propagation
    # → analog of gravitational time dilation; rays bend toward the
    # depression (Newtonian attraction in the optical analogy).
    # NOTE: this is the opposite sign of the exponent in
    # `ca-unified-proposition.md` line 69, which was self-inconsistent
    # with the F3 depression direction; the +α form is what gives
    # gravitational attraction.
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')
    R2 = (X - cx0)**2 + (Y - cy0)**2
    sigma_phi = 120.0   # 10× bump: 12 → 120
    depress_depth = 0.35
    Phi_mag = v * (1.0 - depress_depth * np.exp(-R2 / (2 * sigma_phi**2)))
    c0 = 0.45
    ratio = Phi_mag / v
    c_field = c0 * (ratio ** (alpha))

    print(f'  Setup: L={L}, v={v:.4f}, α={alpha}, depression depth={depress_depth:.2f}')
    print(f'  c_field range: [{c_field.min():.4f}, {c_field.max():.4f}]')
    print(f'  c at centre:   {c_field[cx0, cy0]:.4f}    c at edge: {c_field[0, 0]:.4f}')

    # Probe wave packet: a Gaussian Weyl spinor entering from the left,
    # offset in y above the depression centre.  In flat space (c uniform)
    # it would propagate straight; near the depression c is larger
    # (faster propagation), refracting ray paths.
    sigma_pk = 80.0             # 10× bump: 8 → 80
    pkt_x0 = L // 4
    pkt_y0 = cy0 + 180          # 10× bump: offset above centre 18 → 180 cells
    env = np.exp(-((X - pkt_x0)**2 + (Y - pkt_y0)**2) / (2 * sigma_pk**2))
    kx_in, ky_in = 0.30, 0.00
    phase = np.exp(1j * (kx_in * X + ky_in * Y))
    kappa_in = float(np.sqrt(kx_in**2 + ky_in**2))
    phi = np.exp(1j * np.arctan2(ky_in, kx_in))
    h = np.array([1.0, phi], dtype=complex) / np.sqrt(2.0)
    f_pkt = h[0] * env * phase
    g_pkt = h[1] * env * phase

    # Also run the *same* packet with a FLAT c-field as a baseline.
    c_flat = np.full(shape, c0)

    # Cayley solvers (LU-factored once, reused).
    solver_curved = cc.CayleyVarcSolver2D(c_field, dt=1.0, n_sub=2)
    solver_flat   = cc.CayleyVarcSolver2D(c_flat,   dt=1.0, n_sub=2)

    n_steps = 1200   # 10× bump to match the 10× longer flight path
    norm0 = float(np.sum(np.abs(f_pkt)**2 + np.abs(g_pkt)**2))

    f_c, g_c = f_pkt.copy(), g_pkt.copy()    # curved (with depression)
    f_f, g_f = f_pkt.copy(), g_pkt.copy()    # flat baseline

    # Track centroid trajectory of each
    cy_curved_trace = []
    cy_flat_trace   = []
    for step in range(n_steps + 1):
        dens_c = np.abs(f_c)**2 + np.abs(g_c)**2
        dens_f = np.abs(f_f)**2 + np.abs(g_f)**2
        cy_curved_trace.append(float((Y * dens_c).sum() / dens_c.sum()))
        cy_flat_trace.append  (float((Y * dens_f).sum() / dens_f.sum()))
        if step < n_steps:
            f_c, g_c = solver_curved.step(f_c, g_c)
            f_f, g_f = solver_flat.step  (f_f, g_f)

    norm_c_final = float(np.sum(np.abs(f_c)**2 + np.abs(g_c)**2))
    norm_f_final = float(np.sum(np.abs(f_f)**2 + np.abs(g_f)**2))
    drift_curved = abs(norm_c_final - norm0) / norm0
    drift_flat   = abs(norm_f_final - norm0) / norm0

    cy_curved_trace = np.array(cy_curved_trace)
    cy_flat_trace   = np.array(cy_flat_trace)

    # Deflection: how much further y the curved-c packet moved toward cy0
    # vs the flat baseline.  Δy < 0 means it moved toward the centre.
    dy_curved = cy_curved_trace[-1] - cy_curved_trace[0]
    dy_flat   = cy_flat_trace[-1]   - cy_flat_trace[0]
    deflection = dy_curved - dy_flat       # extra Δy due to curvature
    print(f'  packet starts y = {cy_curved_trace[0]:.2f}, target y_centre = {cy0}')
    print(f'  flat-c   packet final y = {cy_flat_trace[-1]:.4f}  (Δy = {dy_flat:+.4f})')
    print(f'  curved-c packet final y = {cy_curved_trace[-1]:.4f}  (Δy = {dy_curved:+.4f})')
    print(f'  Extra deflection toward density: Δy_curved − Δy_flat = {deflection:+.4f} cells')
    print(f'  Norm drift  flat:   {drift_flat:.3e}')
    print(f'  Norm drift  curved: {drift_curved:.3e}')

    # Save figure: density at start and end for both runs.
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))
    extent = [0, L, 0, L]
    axes[0, 0].imshow(np.abs(f_pkt)**2 + np.abs(g_pkt)**2, origin='lower',
                       extent=extent, cmap='viridis')
    axes[0, 0].set_title('Initial probe packet')
    axes[0, 0].axhline(cy0, color='red', linestyle='--', alpha=0.5)
    axes[0, 1].imshow(np.abs(f_f)**2 + np.abs(g_f)**2, origin='lower',
                       extent=extent, cmap='viridis')
    axes[0, 1].set_title('Flat c — final')
    axes[0, 1].axhline(cy0, color='red', linestyle='--', alpha=0.5)
    axes[0, 2].imshow(np.abs(f_c)**2 + np.abs(g_c)**2, origin='lower',
                       extent=extent, cmap='viridis')
    axes[0, 2].set_title('Curved c (depression at centre) — final')
    axes[0, 2].axhline(cy0, color='red', linestyle='--', alpha=0.5)
    axes[1, 0].imshow(c_field, origin='lower', extent=extent, cmap='magma')
    axes[1, 0].set_title('c(x) field')
    axes[1, 0].axhline(cy0, color='red', linestyle='--', alpha=0.5)
    axes[1, 1].plot(cy_flat_trace,   'b-', label='flat')
    axes[1, 1].plot(cy_curved_trace, 'r-', label='curved')
    axes[1, 1].axhline(cy0, color='gray', linestyle='--', alpha=0.5,
                        label='depression centre')
    axes[1, 1].set_xlabel('step'); axes[1, 1].set_ylabel('packet centroid y')
    axes[1, 1].legend(); axes[1, 1].grid(alpha=0.3)
    axes[1, 1].set_title('Packet centroid y vs time')
    axes[1, 2].plot(np.arange(n_steps + 1),
                     cy_curved_trace - cy_flat_trace, 'r-')
    axes[1, 2].axhline(0, color='gray', alpha=0.5)
    axes[1, 2].set_xlabel('step')
    axes[1, 2].set_ylabel('Δy_curved − Δy_flat')
    axes[1, 2].set_title('Differential deflection (curved − flat)')
    axes[1, 2].grid(alpha=0.3)
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, 'phaseF3b_gravity_cayley.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()

    # Tests:
    #  1. Packet centroid moved toward the depression.  The packet starts at
    #     y = cy0 + 180, so "toward centre" means lower y.  The curved-c run
    #     must end at lower y than the flat-c run, i.e. deflection < 0.
    #     Threshold scaled with the 10× lattice bump (0.05 → 0.5).
    #  2. Norm conserved at machine precision (Cayley contract).
    ok_deflection = deflection < -0.5
    ok_norm       = drift_curved < 1e-10
    check('Probe packet deflected toward density depression (gravitational pull)',
          ok_deflection, f'(extra Δy = {deflection:+.4f} cells)')
    check('Norm conserved at machine precision (Cayley exact-unitary)',
          ok_norm, f'(drift = {drift_curved:.2e})')
    return ok_deflection and ok_norm


# ══════════════════════════════════════════════════════════════════
#  F3b-scan — Newtonian 1/b scaling check (model-observations item 12)
# ══════════════════════════════════════════════════════════════════

def _f3b_run_at_offset(L, b_offset, n_steps,
                        sigma_phi, depress_depth, alpha,
                        c0, sigma_pk, kx_in=0.30):
    """
    Run a single F3b-style deflection measurement at impact parameter
    `b_offset` (probe packet enters offset by this many cells in y above
    the depression centre).

    Returns dict(b, deflection, dy_curved, dy_flat, drift_curved).
    """
    shape = (L, L)
    mu2, lam = 0.5, 0.5
    v = float(np.sqrt(mu2 / (2 * lam)))
    cx0, cy0 = L // 2, L // 2

    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')
    R2 = (X - cx0)**2 + (Y - cy0)**2
    Phi_mag = v * (1.0 - depress_depth * np.exp(-R2 / (2 * sigma_phi**2)))
    ratio = Phi_mag / v
    c_field = c0 * (ratio ** alpha)

    pkt_x0 = L // 4
    pkt_y0 = cy0 + b_offset
    env = np.exp(-((X - pkt_x0)**2 + (Y - pkt_y0)**2) / (2 * sigma_pk**2))
    ky_in = 0.0
    phase = np.exp(1j * (kx_in * X + ky_in * Y))
    phi = np.exp(1j * np.arctan2(ky_in, kx_in))
    h = np.array([1.0, phi], dtype=complex) / np.sqrt(2.0)
    f_pkt = h[0] * env * phase
    g_pkt = h[1] * env * phase
    c_flat = np.full(shape, c0)

    solver_curved = cc.CayleyVarcSolver2D(c_field, dt=1.0, n_sub=2)
    solver_flat   = cc.CayleyVarcSolver2D(c_flat,   dt=1.0, n_sub=2)

    norm0 = float(np.sum(np.abs(f_pkt)**2 + np.abs(g_pkt)**2))
    f_c, g_c = f_pkt.copy(), g_pkt.copy()
    f_f, g_f = f_pkt.copy(), g_pkt.copy()
    cy_c_init = pkt_y0
    cy_f_init = pkt_y0
    for _ in range(n_steps):
        f_c, g_c = solver_curved.step(f_c, g_c)
        f_f, g_f = solver_flat.step(f_f, g_f)
    dens_c = np.abs(f_c)**2 + np.abs(g_c)**2
    dens_f = np.abs(f_f)**2 + np.abs(g_f)**2
    cy_c_final = float((Y * dens_c).sum() / dens_c.sum())
    cy_f_final = float((Y * dens_f).sum() / dens_f.sum())
    dy_curved = cy_c_final - cy_c_init
    dy_flat   = cy_f_final - cy_f_init
    deflection = dy_curved - dy_flat

    norm_c_final = float(np.sum(dens_c))
    drift_curved = abs(norm_c_final - norm0) / norm0

    return {
        'b': b_offset,
        'deflection': deflection,
        'dy_curved': dy_curved,
        'dy_flat': dy_flat,
        'drift_curved': drift_curved,
    }


def test_F3b_scan():
    """
    F3b-scan — verify Δy(b) ∝ 1/b for the Newtonian gravity analog
    (model-observations.md item 12).  Uses a smaller lattice than F3b
    (L=480) to keep total runtime manageable across the 5 b values.

    Pass criteria:
      • All five b values give deflection < 0 (toward depression).
      • Power-law fit slope in log|deflection| vs log b is within ±0.4
        of the expected −1 (Newtonian).
      • All five runs preserve norm to machine precision.
    """
    section('Phase F3b-scan — 1/b scaling of Newtonian deflection')

    # Lean scan lattice: L=192, σ_phi=15 so the source is compact relative
    # to b.  Pick b ∈ {40, 60, 80, 110, 150}, all > 2·σ_phi so the
    # far-field 1/b regime applies.  Per-run cost ≈ 15s on a laptop;
    # 5 runs ≈ 75s total (proportional to L²·n_steps).
    L = 192; n_steps = 160
    sigma_phi = 15.0; sigma_pk = 14.0
    alpha = 1.5; c0 = 0.45; depress_depth = 0.35
    bs = [40, 60, 80, 110, 150]

    print(f'  Setup: L={L}, n_steps={n_steps}, σ_phi={sigma_phi}, b∈{bs}')
    results = []
    for b in bs:
        r = _f3b_run_at_offset(L=L, b_offset=b, n_steps=n_steps,
                                sigma_phi=sigma_phi,
                                depress_depth=depress_depth,
                                alpha=alpha, c0=c0, sigma_pk=sigma_pk)
        results.append(r)
        print(f'    b={b:>3d}  Δy_curved={r["dy_curved"]:+8.3f}  '
              f'Δy_flat={r["dy_flat"]:+8.3f}  '
              f'deflection={r["deflection"]:+8.3f}  '
              f'norm drift={r["drift_curved"]:.2e}')

    deflections = np.array([r['deflection'] for r in results])
    norms       = np.array([r['drift_curved'] for r in results])

    # Power-law fit: log|deflection| = m · log(b) + k.  Expect m ≈ -1.
    if np.all(deflections < 0):
        log_b   = np.log(np.array(bs, dtype=float))
        log_def = np.log(-deflections)
        # least-squares slope
        m, k = np.polyfit(log_b, log_def, 1)
        print(f'  Power-law fit log|Δy|=m·log(b)+k  →  m = {m:+.3f} '
              f'(Newtonian expectation: −1)')
    else:
        m = float('nan')
        print('  WARNING: some deflections non-negative; cannot fit log-log')

    # Save figure
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    if np.all(deflections < 0):
        ax.loglog(bs, -deflections, 'o-', label='measured')
        b_arr = np.array(bs, dtype=float)
        c_fit = np.exp(np.mean(log_def + log_b))   # |Δy|·b ≈ const
        ax.loglog(b_arr, c_fit / b_arr, 'k--',
                   label=f'fit m=−1 (Newtonian)')
        ax.set_xlabel('b (impact parameter, cells)')
        ax.set_ylabel('|deflection|  (cells)')
        ax.set_title('F3b-scan: deflection vs impact parameter')
        ax.legend(); ax.grid(alpha=0.3, which='both')
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, 'phaseF3b_scan.png')
    plt.savefig(out, dpi=120, bbox_inches='tight'); plt.close()

    ok_sign  = bool(np.all(deflections < 0))
    ok_slope = bool(abs(m + 1.0) < 0.4)
    ok_norm  = bool(np.all(norms < 1e-10))
    check('All b values give deflection toward depression (Δy<0)',
          ok_sign, f'(min Δy={deflections.max():+.3f}, max |Δy|={(-deflections).max():.3f})')
    check('Newtonian 1/b scaling: power-law slope within ±0.4 of −1',
          ok_slope, f'(slope m = {m:+.3f})')
    check('Norm conserved at machine precision across all b runs',
          ok_norm, f'(max drift = {norms.max():.2e})')
    return ok_sign and ok_slope and ok_norm


# ══════════════════════════════════════════════════════════════════
#  F-dt — Strang-composition dt→0 convergence  (model-observations 13)
# ══════════════════════════════════════════════════════════════════

def test_dt_convergence():
    """
    Verify that the Strang-composed `unified_step` exhibits the expected
    O(dt²) convergence as dt is halved.

    Method: run the same initial state for fixed total time T with
    dt ∈ {dt0, dt0/2, dt0/4}; compute pairwise differences of the
    final states.  The ratio

        ratio = ‖Ψ(dt0) − Ψ(dt0/2)‖ /  ‖Ψ(dt0/2) − Ψ(dt0/4)‖

    should be ≈ 4 for a second-order method (the dominant error term
    A·dt² gives a Richardson factor of 4).  Pass if 3.0 ≤ ratio ≤ 5.5.

    This is the missing dt-scan that `model-observations.md` item 13
    flags: the unconditionally-stable split-step propagator can mask
    order-of-accuracy bugs, since norm is preserved exactly regardless
    of dt.  This test specifically targets the Strang composition.
    """
    section('Phase F-dt — Strang composition O(dt²) convergence')
    L = 64; shape = (L, L)
    mu2, lam, y = 0.5, 0.5, 0.6
    v = float(np.sqrt(mu2 / (2 * lam)))

    # Initial state: small radial perturbation around vacuum + Gaussian fermion.
    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')
    cx0, cy0 = L // 2, L // 2
    perturb = 1e-3 * np.cos(2 * np.pi * X / L)
    Phi_init = (v + perturb).astype(complex)
    Pi_init  = np.zeros_like(Phi_init)

    nu0, nd0, xu0, xd0 = dirac.gaussian_dirac_2d(shape, sigma=4.0,
                                                   chirality='mixed')

    def run(dt, n_steps):
        st = un.UnifiedState(Phi_init.copy(), Pi_init.copy(),
                              nu0.copy(), nd0.copy(),
                              xu0.copy(), xd0.copy())
        for _ in range(n_steps):
            un.unified_step(st, mu2, lam, yukawa=y, dt=dt,
                             n_phi_sub=1)
        return st

    T = 8.0
    # Three runs over the same total time, halving dt each time.
    states = {}
    for dt in (1.0, 0.5, 0.25):
        n = int(round(T / dt))
        states[dt] = run(dt, n)
        print(f'  dt={dt:<5}  n_steps={n}')

    def diff(s1, s2):
        d_Phi = float(np.max(np.abs(s1.Phi - s2.Phi)))
        d_eta = float(np.max(np.abs(s1.eta_u - s2.eta_u) +
                               np.abs(s1.eta_d - s2.eta_d)))
        d_chi = float(np.max(np.abs(s1.chi_u - s2.chi_u) +
                               np.abs(s1.chi_d - s2.chi_d)))
        return max(d_Phi, d_eta, d_chi)

    d_coarse = diff(states[1.0],  states[0.5])
    d_fine   = diff(states[0.5],  states[0.25])
    ratio = d_coarse / d_fine if d_fine > 0 else float('inf')

    print(f'  ‖Ψ(dt=1.0) − Ψ(dt=0.5)‖  = {d_coarse:.3e}')
    print(f'  ‖Ψ(dt=0.5) − Ψ(dt=0.25)‖ = {d_fine:.3e}')
    print(f'  Richardson ratio          = {ratio:.2f}   (expect ≈ 4 for O(dt²))')

    ok = (3.0 <= ratio <= 5.5)
    return check('Strang composition convergence ratio ∈ [3.0, 5.5] (O(dt²))',
                  ok, f'(ratio = {ratio:.2f})')


# ══════════════════════════════════════════════════════════════════
#  F4 — Symmetry-restored phase: massless fermions
# ══════════════════════════════════════════════════════════════════

def test_F4():
    section('Phase F4 — Symmetry restored: Φ=0, fermions massless, Weyl recovered')

    # 10× bump (2026-05-16): L=32→320, σ=3→30
    L = 320; shape = (L, L)
    # Symmetric (high-T) phase: V = +μ²|Φ|² + λ|Φ|⁴, vacuum at Φ=0.
    # Selected via the explicit phase='symmetric' API on unified_step;
    # `mu2` is the positive magnitude.  (2026-05-16 refactor: replaces
    # the legacy mu2=-0.5 sign-flip kludge.)
    mu2 = 0.5
    lam = 0.5
    y = 0.6

    state = un.setup_symmetry_restored(shape, mu2, lam,
                                         fermion='left', sigma=30.0)
    # Reference: pure exact-QCA Weyl evolution (Paper 1 Eq. 16).  At
    # m=0 the exact-QCA Dirac reduces to diag(W_k, W'_k); the η-block
    # matches `weyl_step_2d_arccos_splitstep` bit-for-bit (Finding 9).
    import ca_core_exact as ce
    f_ref, g_ref = ca.gaussian_spinor_2d(shape, sigma=30.0, helicity='left')
    for _ in range(50):
        f_ref, g_ref = ce.weyl_step_2d_arccos_splitstep(f_ref, g_ref)
        state = un.unified_step(state, mu2, lam, yukawa=y, dt=1.0,
                                  phase='symmetric')

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
    results['F1']  = test_F1()
    results['F2']  = test_F2()
    results['F3']  = test_F3()
    results['F3b'] = test_F3b()
    results['F3b-scan'] = test_F3b_scan()
    results['F-dt']     = test_dt_convergence()
    results['F4']  = test_F4()

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
