"""
test_emergent_time_T1.py — Phase T1 (Lazy-update + tick heatmap) tests
=========================================================================
Implements the gates spelled out in `ca-emergent-time-plan.md` §T1.

T1.A — Lazy-update propagator
  Wrap each F-gate-relevant propagator with `ca_lazy.lazy_step`.  The
  bookkeeping-only laziness contract means the field output must be
  bit-for-bit identical to the synchronous run (FFT-based propagators
  touch every cell).  Verifies:
    - sync-vs-lazy max per-cell residual < 1e-13 across:
        * F1-like vacuum regression (Φ = v, constant-m Dirac)
        * Weyl free propagation (2D split-step)
        * Higgs Φ free Klein-Gordon
        * Unified step (Φ + Dirac + Yukawa coupling)
    - vacuum cells outside the wavepacket support accumulate 0 ticks
    - the wave-packet support accumulates a strictly positive tick total

T1.B — Tick-field heatmap
  Renders `ticks_heatmap_F1.png`, `ticks_heatmap_weyl.png`,
  `ticks_heatmap_higgs.png`, `ticks_heatmap_unified.png` so the
  visualization claim (matter ticks fastest, vacuum freezes) is
  inspectable.

Gate-pass criteria
------------------
ALL of:
  * max sync-vs-lazy residual < 1e-13   (load-bearing — propagator
    output identical to synchronous run)
  * vacuum ticks == 0                    (counter does not register
    FFT round-off as ticks at ε = 1e-13)
  * packet ticks > 0                     (counter actually advances)
  * F-phase regression numbers from `run_phaseF_tests.py` are
    unchanged (verified separately; this script only checks the
    invariance of the lazy wrapper itself)
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ca_core as ca
import ca_dirac as dirac
import ca_higgs as hg
import ca_unified as un
import ca_lazy as lz
import tick_heatmap as th


FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'figures')
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


RESULTS = {}


# ══════════════════════════════════════════════════════════════════
#  T1.A.1 — Weyl free propagation
# ══════════════════════════════════════════════════════════════════

def test_T1A_weyl(L=64, n_steps=40, sigma=6.0, c=0.5, eps=1e-13):
    section('T1.A.1 — Weyl free 2D split-step (lazy = sync, vacuum frozen)')

    shape = (L, L)
    f0, g0 = ca.gaussian_spinor_2d(shape, sigma=sigma, helicity='left')
    f0 = f0.astype(np.complex128)
    g0 = g0.astype(np.complex128)

    def step_fn(state):
        f, g = state
        return ca.weyl_step_2d_splitstep(f, g, c=c)

    # Sync baseline
    sf, sg = f0.copy(), g0.copy()
    for _ in range(n_steps):
        sf, sg = step_fn((sf, sg))

    # Lazy run
    lf, lg = f0.copy(), g0.copy()
    tc = lz.TickCounter(shape)
    for _ in range(n_steps):
        lf, lg = lz.lazy_step(step_fn, (lf, lg), tc, eps=eps,
                              extract_fields=lz.extract_weyl_2d)

    max_diff = max(float(np.max(np.abs(lf - sf))),
                   float(np.max(np.abs(lg - sg))))

    # Vacuum vs packet support test.  After n_steps · c the packet is at
    # most that many cells from its initial centroid.  Cells more than
    # 5σ + n_steps·c from the start are 'vacuum' and should never tick.
    xs = np.arange(L) - L // 2
    ys = np.arange(L) - L // 2
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    r = np.sqrt(X * X + Y * Y)
    safety = 5.0 * sigma + c * n_steps
    vacuum_mask = r > safety
    vac_ticks = int(tc.N[vacuum_mask].sum())
    pkt_ticks = int(tc.N[~vacuum_mask].sum())

    ok_sync = check('lazy matches sync (max|Δψ|)',
                    max_diff < 1e-13, f'{max_diff:.2e}')
    ok_vac  = check('vacuum cells accumulate zero ticks',
                    vac_ticks == 0, f'{vac_ticks}')
    ok_pkt  = check('packet support accumulates ticks',
                    pkt_ticks > 0,   f'{pkt_ticks}')

    # T1.B heatmap
    title = (f'T1.B — Weyl 2D free, L={L}, n_steps={n_steps}, '
             f'σ={sigma:g}, c={c:g}, ε={eps:.0e}')
    out = os.path.join(FIGURES_DIR, 'ticks_heatmap_weyl.png')
    prob = np.abs(lf) ** 2 + np.abs(lg) ** 2
    th.tick_heatmap(tc.N, title=title, outpath=out, prob_density=prob)
    print(f'  → wrote {out}')

    RESULTS['T1A_weyl'] = {
        'max_diff': max_diff, 'vac_ticks': vac_ticks,
        'pkt_ticks': pkt_ticks, 'eps': eps,
    }
    return ok_sync and ok_vac and ok_pkt


# ══════════════════════════════════════════════════════════════════
#  T1.A.2 — Higgs free KG (Φ = v stable + perturbation propagates)
# ══════════════════════════════════════════════════════════════════

def test_T1A_higgs(L=64, n_steps=40, mu2=0.5, lam=0.5, eps=1e-13):
    section('T1.A.2 — Higgs (Mexican-hat Φ around vacuum, lazy = sync)')

    # Two sub-tests:
    #   (a) Pure vacuum  Φ = v exactly, Π = 0  →  zero ticks anywhere.
    #       The vacuum-as-fixed-point property is *only* present in the
    #       full nonlinear propagator (kg_step_strang); the free KG
    #       propagator treats Φ as an oscillator at mass m_h and is
    #       not the right vacuum reference.
    #   (b) Vacuum + perturbation  Φ = v + 1e-3·bump  →  bit-for-bit
    #       sync match.  With periodic BC the perturbation reaches
    #       every cell within a few wrap distances and registers as
    #       a real (nontrivial) tick at every cell — that is genuine
    #       state change per the proposition's nontriviality definition.

    shape = (L, L)
    v = float(np.sqrt(mu2 / (2.0 * lam)))

    # Use n_sub=4 to keep the symplectic step stable with the nonlinear
    # potential at the unit time step (the free-KG λ=0 propagator is
    # exactly unitary at any dt, but the Mexican-hat residual is only
    # second-order accurate).
    def step_fn(state):
        Phi, Pi = state
        return hg.kg_step_strang(Phi, Pi, mu2=mu2, lam=lam, dt=0.25,
                                  n_sub=1, phase='broken')

    # ── Sub-test (a): pure vacuum ─────────────────────────────────
    Phi_v = np.full(shape, v + 0j)
    Pi_v  = np.zeros(shape, dtype=complex)
    tc_vac = lz.TickCounter(shape)
    Pv, Qv = Phi_v.copy(), Pi_v.copy()
    for _ in range(n_steps):
        Pv, Qv = lz.lazy_step(step_fn, (Pv, Qv), tc_vac, eps=eps,
                               extract_fields=lambda s: list(s))
    vacuum_ticks_pure = int(tc_vac.N.sum())

    # ── Sub-test (b): vacuum + perturbation ──────────────────────
    xs = np.arange(L) - L // 2
    ys = np.arange(L) - L // 2
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    bump = np.exp(-(X * X + Y * Y) / (2.0 * 3.0 ** 2)).astype(complex)
    Phi0 = (v + 1e-3 * bump).astype(complex)
    Pi0  = np.zeros(shape, dtype=complex)

    sP, sQ = Phi0.copy(), Pi0.copy()
    for _ in range(n_steps):
        sP, sQ = step_fn((sP, sQ))

    lP, lQ = Phi0.copy(), Pi0.copy()
    tc = lz.TickCounter(shape)
    for _ in range(n_steps):
        lP, lQ = lz.lazy_step(step_fn, (lP, lQ), tc, eps=eps,
                              extract_fields=lambda s: list(s))

    max_diff = max(float(np.max(np.abs(lP - sP))),
                   float(np.max(np.abs(lQ - sQ))))

    vac_ticks = vacuum_ticks_pure
    pkt_ticks = int(tc.N.sum())

    ok_sync = check('lazy matches sync (max|Δ(Φ,Π)|)',
                    max_diff < 1e-13, f'{max_diff:.2e}')
    ok_vac  = check('pure-vacuum state accumulates zero ticks',
                    vac_ticks == 0, f'{vac_ticks}')
    ok_pkt  = check('bump support accumulates ticks',
                    pkt_ticks > 0, f'{pkt_ticks}')

    title = (f'T1.B — Higgs Mexican-hat, L={L}, n_steps={n_steps}, '
             f'μ²={mu2}, λ={lam}, ε={eps:.0e}')
    out = os.path.join(FIGURES_DIR, 'ticks_heatmap_higgs.png')
    prob = np.abs(lP - v) ** 2 + np.abs(lQ) ** 2
    th.tick_heatmap(tc.N, title=title, outpath=out, prob_density=prob)
    print(f'  → wrote {out}')

    RESULTS['T1A_higgs'] = {
        'max_diff': max_diff, 'vac_ticks': vac_ticks,
        'pkt_ticks': pkt_ticks, 'eps': eps,
    }
    return ok_sync and ok_vac and ok_pkt


# ══════════════════════════════════════════════════════════════════
#  T1.A.3 — F1 vacuum regression (Φ = v stable, Dirac propagates)
# ══════════════════════════════════════════════════════════════════

def test_T1A_F1_unified(L=64, n_steps=30, mu2=0.5, lam=0.5, y=0.6,
                         sigma=4.0, eps=1e-13):
    section('T1.A.3 — F1-like unified step (Φ=v + Dirac), lazy = sync')

    shape = (L, L)
    v = float(np.sqrt(mu2 / (2.0 * lam)))

    def step_fn(s):
        return un.unified_step(s, mu2, lam, yukawa=y, dt=1.0)

    # ── Sub-test (a): pure vacuum (Φ=v, Π=0, no fermions) ────────
    # Build the state by hand — setup_vacuum() seeds a Dirac packet.
    Phi_v = np.full(shape, v + 0j)
    Pi_v  = np.zeros(shape, dtype=complex)
    zero  = np.zeros(shape, dtype=complex)
    vac_state = un.UnifiedState(Phi_v, Pi_v, zero.copy(), zero.copy(),
                                  zero.copy(), zero.copy())
    tc_vac = lz.TickCounter(shape)
    for _ in range(n_steps):
        vac_state = lz.lazy_step(step_fn, vac_state, tc_vac, eps=eps,
                                  extract_fields=lz.extract_unified)
    vacuum_ticks_pure = int(tc_vac.N.sum())

    # ── Sub-test (b): F1-like state with Dirac packet ────────────
    state_sync, _ = un.setup_vacuum(shape, mu2, lam,
                                     fermion='mixed', sigma=sigma)
    state_lazy = state_sync.copy()

    s_s = state_sync
    for _ in range(n_steps):
        s_s = step_fn(s_s)

    s_l = state_lazy
    tc = lz.TickCounter(shape)
    for _ in range(n_steps):
        s_l = lz.lazy_step(step_fn, s_l, tc, eps=eps,
                            extract_fields=lz.extract_unified)

    diff = max(
        float(np.max(np.abs(s_l.Phi   - s_s.Phi))),
        float(np.max(np.abs(s_l.Pi    - s_s.Pi))),
        float(np.max(np.abs(s_l.eta_u - s_s.eta_u))),
        float(np.max(np.abs(s_l.eta_d - s_s.eta_d))),
        float(np.max(np.abs(s_l.chi_u - s_s.chi_u))),
        float(np.max(np.abs(s_l.chi_d - s_s.chi_d))),
    )

    vac_ticks = vacuum_ticks_pure
    pkt_ticks = int(tc.N.sum())

    ok_sync = check('lazy matches sync (max|Δstate|)',
                    diff < 1e-13, f'{diff:.2e}')
    ok_vac  = check('pure-vacuum state accumulates zero ticks',
                    vac_ticks == 0, f'{vac_ticks}')
    ok_pkt  = check('Dirac packet support accumulates ticks',
                    pkt_ticks > 0, f'{pkt_ticks}')

    # The fermion probability density drives the heatmap visualization.
    prob = (np.abs(s_l.eta_u) ** 2 + np.abs(s_l.eta_d) ** 2 +
            np.abs(s_l.chi_u) ** 2 + np.abs(s_l.chi_d) ** 2)
    title = (f'T1.B — Unified F1 (Φ=v + Dirac), L={L}, n_steps={n_steps}, '
             f'y={y:g}, ε={eps:.0e}')
    out = os.path.join(FIGURES_DIR, 'ticks_heatmap_F1_unified.png')
    th.tick_heatmap(tc.N, title=title, outpath=out, prob_density=prob)
    print(f'  → wrote {out}')

    RESULTS['T1A_F1_unified'] = {
        'max_diff': diff, 'vac_ticks': vac_ticks,
        'pkt_ticks': pkt_ticks, 'eps': eps,
    }
    return ok_sync and ok_vac and ok_pkt


# ══════════════════════════════════════════════════════════════════
#  T1.A.4 — ε calibration: residual histogram across all F-gate runs
# ══════════════════════════════════════════════════════════════════

def test_T1A_eps_calibration(L=64, n_steps=40, sigma=6.0, c=0.5,
                              mu2=0.5, lam=0.5):
    section('T1.A.4 — ε calibration: FFT residual floor on pure-vacuum state')

    shape = (L, L)
    v = float(np.sqrt(mu2 / (2.0 * lam)))

    # Three pure-vacuum runs.  In each, the propagator's output should
    # equal the input to FFT round-off — the per-cell residual is the
    # empirical noise floor.
    floors = {}

    # Weyl: ψ ≡ 0 is a fixed point (trivial; should be exactly zero).
    f0 = np.zeros(shape, dtype=complex)
    g0 = np.zeros(shape, dtype=complex)
    res = []
    f, g = f0.copy(), g0.copy()
    for _ in range(n_steps):
        fp, gp = ca.weyl_step_2d_splitstep(f, g, c=c)
        res.append(float(np.max(np.sqrt(np.abs(fp - f) ** 2 +
                                         np.abs(gp - g) ** 2))))
        f, g = fp, gp
    floors['Weyl (ψ=0)']  = max(res)

    # Higgs Mexican-hat: Φ ≡ v, Π ≡ 0 is the true vacuum fixed point
    # of the *full* nonlinear propagator.  Free-KG with mass m_h is not
    # the right reference (it treats Φ as an oscillator at ω=m_h).
    Phi = np.full(shape, v + 0j)
    Pi  = np.zeros(shape, dtype=complex)
    res = []
    for _ in range(n_steps):
        Pp, Qp = hg.kg_step_strang(Phi, Pi, mu2=mu2, lam=lam, dt=1.0,
                                    phase='broken')
        res.append(float(np.max(np.sqrt(np.abs(Pp - Phi) ** 2 +
                                         np.abs(Qp - Pi) ** 2))))
        Phi, Pi = Pp, Qp
    floors['Higgs Mexican-hat (Φ=v)'] = max(res)

    # Unified: full F1-like vacuum (Φ=v, Π=0, all fermions zero).
    zero = np.zeros(shape, dtype=complex)
    state = un.UnifiedState(np.full(shape, v + 0j), zero.copy(),
                              zero.copy(), zero.copy(),
                              zero.copy(), zero.copy())
    res = []
    for _ in range(n_steps):
        before = lz.extract_unified(state)
        state = un.unified_step(state, mu2, lam, yukawa=0.6, dt=1.0)
        after = lz.extract_unified(state)
        r = lz.per_cell_residual_multi(before, after)
        res.append(float(np.max(r)))
    floors['Unified (F1 vac)'] = max(res)

    print('  Per-step max residual on pure-vacuum states:')
    for k, vf in floors.items():
        print(f'    {k:<22} max residual = {vf:.3e}')

    floor_max = max(floors.values())
    eps_default = 1e-13
    if floor_max > 0:
        margin = eps_default / floor_max
        print(f'  → observed floor = {floor_max:.3e}; ε = {eps_default:.0e} '
              f'sits {margin:.3g}× above the floor')
    else:
        print('  → all vacuum residuals are zero; ε = 1e-13 has '
              'infinite margin')

    RESULTS['T1A_eps_calibration'] = {
        'floor_weyl_zero':   floors['Weyl (ψ=0)'],
        'floor_higgs_vac':   floors['Higgs Mexican-hat (Φ=v)'],
        'floor_unified_vac': floors['Unified (F1 vac)'],
        'eps_default':       eps_default,
    }
    # Pass iff the noise floor is below ε (so vacuum will not register).
    return floor_max < eps_default

    RESULTS['T1A_eps_calibration'] = {
        'far_corner_residual_max': fr_max,
        'far_corner_residual_mean': float(fr.mean()),
        'recommended_eps': 1e-13,
    }
    return fr_max < 1e-13


# ══════════════════════════════════════════════════════════════════
#  Top-level
# ══════════════════════════════════════════════════════════════════

def main():
    print('=' * 72)
    print('  Phase T1 — Emergent-time gate tests (lazy + heatmap)')
    print('  Plan: ca-emergent-time-plan.md §T1')
    print('  Proposition: ca-emergent-time-proposition.md')
    print('=' * 72)

    results = []
    results.append(('T1.A.1 Weyl free',          test_T1A_weyl()))
    results.append(('T1.A.2 Higgs free KG',      test_T1A_higgs()))
    results.append(('T1.A.3 F1 unified step',    test_T1A_F1_unified()))
    results.append(('T1.A.4 ε calibration',      test_T1A_eps_calibration()))

    print()
    print('=' * 72)
    print('  T1 summary')
    print('=' * 72)
    all_ok = True
    for name, ok in results:
        all_ok = all_ok and ok
        flag = 'PASS' if ok else 'FAIL'
        print(f'  [{flag}]  {name}')
    print()
    print(f'  Overall: {"PASS" if all_ok else "FAIL"}')

    # Stash a compact JSON for the changelog
    import json
    rep_path = os.path.join(FIGURES_DIR, 'T1_results.json')
    with open(rep_path, 'w') as fh:
        json.dump(RESULTS, fh, indent=2, default=float)
    print(f'  → wrote {rep_path}')

    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
