"""
run_10x_tests.py  —  Comprehensive 10× scale test run
======================================================
Runs all major simulation tests with:
  • L as large as feasible (RAM-limited; 3.4 GB available)
  • 10× time steps vs current defaults
  • Zero-padded DFT phase extraction alongside lsq for every
    phase-rate measurement

Parameter choices:
  SR-2 Part B   : L=128, n_steps=4000 (vs L=48, n_steps=400)
  SR-2 scan     : L=96,  n_steps=2000 (vs L=32, n_steps=200)
                  + static result cached per mass (halves total runs)
  On-grid scan  : L=96, modes 1–7, masses {0.05,0.10,0.20,0.50},
                  n_steps=800 (vs L=32-48, n_steps=80)
  Top-10 tests  : run with their native parameters (most analytic/fast)
  GR-3 PR       : L=128 Poisson grid (vs L=64)
  QG-4 charge   : n_steps=5000 (vs 1000)

All section timings and key numbers are printed with timestamps.
Results appended to test-results/ JSON files where applicable.
"""

import time, json, math, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ca-simulation'))
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'test-results')
t_script_start = time.time()

import ca_fft
from ca_propagator import (BccDiracPropagator, phase_rate_lsq,
                            phase_rate_zeropad, compare_phase_methods)
import test_SR2_3D_time_dilation as sr2

PAD_FACTOR = 32   # zero-pad DFT interpolation factor

def elapsed():
    return f"[+{time.time()-t_script_start:6.1f}s]"

def section(title):
    print()
    print("=" * 80)
    print(f"{elapsed()}  {title}")
    print("=" * 80)

def phase_pair(samples_s, samples_m, dt, label=""):
    """Run both lsq and zero-padded DFT on a (static, moving) sample pair."""
    ws_lsq = phase_rate_lsq(samples_s, dt)
    wm_lsq = phase_rate_lsq(samples_m, dt)
    zp_s   = phase_rate_zeropad(samples_s, dt, pad_factor=PAD_FACTOR)
    zp_m   = phase_rate_zeropad(samples_m, dt, pad_factor=PAD_FACTOR)
    if label:
        print(f"  {label}:")
    print(f"    ω_static  lsq={ws_lsq:.10f}  zpad={zp_s['omega']:.10f}"
          f"  (Δω_eff={zp_s['delta_omega_eff']:.2e}  |res|={zp_s['lsq_residual']:.2e})")
    print(f"    ω_moving  lsq={wm_lsq:.10f}  zpad={zp_m['omega']:.10f}"
          f"  (Δω_eff={zp_m['delta_omega_eff']:.2e}  |res|={zp_m['lsq_residual']:.2e})")
    return ws_lsq, wm_lsq, zp_s, zp_m


# ══════════════════════════════════════════════════════════════════
#  SECTION 1 — SR-2 Part A  (dense algebraic scan)
# ══════════════════════════════════════════════════════════════════

section("SR-2 Part A — Dense algebraic scan")
rows_A = sr2.part_A_scan()
finite = [r for r in rows_A if not math.isnan(r[8])]
finite.sort(key=lambda r: r[8])
print(f"\n{elapsed()}  Part A done — "
      f"best |Δ|={finite[0][8]:.3e}, worst={finite[-1][8]:.3e}")


# ══════════════════════════════════════════════════════════════════
#  SECTION 2 — SR-2 Part B  (L=128, n_steps=4000)
# ══════════════════════════════════════════════════════════════════

section("SR-2 Part B — Numerical propagation  L=128  n_steps=4000")

L_B   = 128
N_B   = 4000
m_B   = 0.1
kx_B  = 0.05
sign_B = '+'

print(f"{elapsed()}  Building BccDiracPropagator(L={L_B}, m={m_B}) …")
prop_B = BccDiracPropagator(shape=L_B, m=m_B, sign=sign_B)
print(f"{elapsed()}  {prop_B.memory_report()}")

print(f"{elapsed()}  Running static propagation ({N_B} steps) …")
t0 = time.time()
samples_s, _, _, _ = sr2.measure_plane_wave_phase_rate_3d_exact(
    L_B, m_B, kx_B, N_B, static=True, propagator=prop_B)
print(f"{elapsed()}  Static done in {time.time()-t0:.1f}s")

print(f"{elapsed()}  Running moving propagation ({N_B} steps) …")
t0 = time.time()
samples_m, vg_m, kxg_m, w_m = sr2.measure_plane_wave_phase_rate_3d_exact(
    L_B, m_B, kx_B, N_B, static=False, propagator=prop_B)
print(f"{elapsed()}  Moving done in {time.time()-t0:.1f}s")

ws_lsq_B, wm_lsq_B, zp_s_B, zp_m_B = phase_pair(
    samples_s, samples_m, dt=1.0, label="L=128 n_steps=4000")

omega_s_pred = sr2.omega_static_qca(m_B)
omega_m_pred = abs(w_m - kxg_m * vg_m)
ratio_lsq    = wm_lsq_B / ws_lsq_B
ratio_pred   = omega_m_pred / omega_s_pred
beta         = vg_m / sr2.C_LAT_3D
inv_gamma    = math.sqrt(1.0 - beta*beta) if abs(beta) < 1.0 else float('nan')

print(f"\n  ratio_lsq   = {ratio_lsq:.14f}")
print(f"  ratio_pred  = {ratio_pred:.14f}")
print(f"  1/γ_SR      = {inv_gamma:.14f}")
print(f"  num-vs-pred = {abs(ratio_lsq - ratio_pred):.3e}")
print(f"  num-vs-SR   = {abs(ratio_lsq - inv_gamma):.3e}")
print(f"  pred-vs-SR  = {abs(ratio_pred - inv_gamma):.3e}")
print(f"\n  FFT floor check (pad_factor={PAD_FACTOR}):")
print(f"    static  |lsq-zpad| = {zp_s_B['lsq_residual']:.3e}")
print(f"    moving  |lsq-zpad| = {zp_m_B['lsq_residual']:.3e}")

result_B = {
    'L': L_B, 'n_steps': N_B, 'm': m_B, 'kx0': kx_B,
    'omega_s_pred': omega_s_pred, 'omega_m_pred': omega_m_pred,
    'omega_s_lsq': ws_lsq_B, 'omega_m_lsq': wm_lsq_B,
    'omega_s_zpad': zp_s_B['omega'], 'omega_m_zpad': zp_m_B['omega'],
    'ratio_lsq': ratio_lsq, 'ratio_pred': ratio_pred,
    'inv_gamma': inv_gamma,
    'num_vs_pred': abs(ratio_lsq - ratio_pred),
    'num_vs_SR':   abs(ratio_lsq - inv_gamma),
    'pred_vs_SR':  abs(ratio_pred - inv_gamma),
    'lsq_zpad_residual_s': zp_s_B['lsq_residual'],
    'lsq_zpad_residual_m': zp_m_B['lsq_residual'],
    'delta_omega_eff': zp_s_B['delta_omega_eff'],
}
with open(os.path.join(RESULTS_DIR, 'sr2_10x_partB.json'), 'w') as f:
    json.dump(result_B, f, indent=2)
print(f"\n{elapsed()}  Part B done — saved sr2_10x_partB.json")


# ══════════════════════════════════════════════════════════════════
#  SECTION 3 — SR-2 Part B scan  (L=96, n_steps=2000)
#              static cached per mass, zero-padded DFT on each pair
# ══════════════════════════════════════════════════════════════════

section("SR-2 Part B scan — L=96  n_steps=2000  static cached per mass")

L_S  = 96
N_S  = 2000
sign_S = '+'

scan_grid = [
    (0.05, 0.005), (0.05, 0.01), (0.05, 0.05), (0.05, 0.10),
    (0.10, 0.01),  (0.10, 0.05), (0.10, 0.10),
    (0.20, 0.05),  (0.20, 0.10), (0.20, 0.20),
    (0.50, 0.05),  (0.50, 0.10), (0.50, 0.20), (0.50, 0.30),
]

print(f"{elapsed()}  Building propagators for {len(set(m for m,_ in scan_grid))} masses …")
prop_cache   = {}
static_cache = {}   # (L, m) → (ws_lsq, ws_zpad, samples_s)
for m, _ in scan_grid:
    if m not in prop_cache:
        prop_cache[m] = BccDiracPropagator(shape=L_S, m=m, sign=sign_S)
        print(f"  {elapsed()}  Propagator m={m}: {prop_cache[m].memory_report()}")

print()
print(f"  {'m':>6} {'k_x':>8} {'v_g':>10} {'v/c':>8} "
      f"{'ratio_lsq':>14} {'1/γ_SR':>14} {'n-vs-p':>10} {'n-vs-SR':>10} "
      f"{'|lsq-zpad_m|':>14}")
print("  " + "-" * 100)

scan_rows = []
for m, kx_target in scan_grid:
    prop = prop_cache[m]

    # Static: run once per mass and cache
    if m not in static_cache:
        t0 = time.time()
        ss, _, _, _ = sr2.measure_plane_wave_phase_rate_3d_exact(
            L_S, m, kx_target, N_S, static=True, propagator=prop)
        ws_lsq  = phase_rate_lsq(ss, 1.0)
        ws_zpad = phase_rate_zeropad(ss, 1.0, pad_factor=PAD_FACTOR)['omega']
        static_cache[m] = (ws_lsq, ws_zpad)
        print(f"  {elapsed()}  Static m={m:.2f}  ω_lsq={ws_lsq:.10f}  "
              f"ω_zpad={ws_zpad:.10f}  t={time.time()-t0:.1f}s")
    ws_lsq, ws_zpad = static_cache[m]

    # Moving
    t0 = time.time()
    sm, vg, kxg, w = sr2.measure_plane_wave_phase_rate_3d_exact(
        L_S, m, kx_target, N_S, static=False, propagator=prop)
    wm_lsq = phase_rate_lsq(sm, 1.0)
    zp_m   = phase_rate_zeropad(sm, 1.0, pad_factor=PAD_FACTOR)

    ws_pred = sr2.omega_static_qca(m)
    wm_pred = abs(w - kxg * vg)
    ratio_lsq  = wm_lsq / ws_lsq
    ratio_pred = wm_pred / ws_pred
    beta       = vg / sr2.C_LAT_3D
    inv_gamma  = math.sqrt(1.0 - beta*beta) if abs(beta) < 1 else float('nan')

    print(f"  {m:6.3f} {kxg:8.5f} {vg:10.6f} {beta:8.5f} "
          f"{ratio_lsq:14.10f} {inv_gamma:14.10f} "
          f"{abs(ratio_lsq-ratio_pred):10.3e} {abs(ratio_lsq-inv_gamma):10.3e} "
          f"{zp_m['lsq_residual']:14.3e}  t={time.time()-t0:.0f}s")

    scan_rows.append({
        'm': m, 'kx_target': kx_target, 'kxg': kxg, 'vg': vg, 'beta': beta,
        'ws_lsq': ws_lsq, 'wm_lsq': wm_lsq,
        'ws_zpad': ws_zpad, 'wm_zpad': zp_m['omega'],
        'ratio_lsq': ratio_lsq, 'ratio_pred': ratio_pred, 'inv_gamma': inv_gamma,
        'num_vs_pred': abs(ratio_lsq - ratio_pred),
        'num_vs_SR':   abs(ratio_lsq - inv_gamma),
        'lsq_zpad_residual_m': zp_m['lsq_residual'],
        'delta_omega_eff': zp_m['delta_omega_eff'],
    })

# Summary statistics
finite_s = [r for r in scan_rows if not math.isnan(r['inv_gamma'])]
best_nvsS  = min(finite_s, key=lambda r: r['num_vs_SR'])
worst_nvsS = max(finite_s, key=lambda r: r['num_vs_SR'])
best_nvsp  = min(finite_s, key=lambda r: r['num_vs_pred'])
worst_nvsp = max(finite_s, key=lambda r: r['num_vs_pred'])
print(f"\n  Scan summary ({len(scan_rows)} points):")
print(f"    num-vs-SR:    best={best_nvsS['num_vs_SR']:.3e}  "
      f"(m={best_nvsS['m']}, k={best_nvsS['kx_target']})"
      f"  worst={worst_nvsS['num_vs_SR']:.3e}")
print(f"    num-vs-pred:  best={best_nvsp['num_vs_pred']:.3e}  "
      f"  worst={worst_nvsp['num_vs_pred']:.3e}")

with open(os.path.join(RESULTS_DIR, 'sr2_10x_scan.json'), 'w') as f:
    json.dump({'L': L_S, 'n_steps': N_S, 'pad_factor': PAD_FACTOR,
               'rows': scan_rows}, f, indent=2)
print(f"\n{elapsed()}  Scan done — saved sr2_10x_scan.json")


# ══════════════════════════════════════════════════════════════════
#  SECTION 4 — On-grid k scan  (L=96, modes 1–7, 10× steps)
# ══════════════════════════════════════════════════════════════════

section("On-grid scan — L=96  modes 1–7  n_steps=800")

L_G   = 96
N_G   = 800
masses_G = [0.05, 0.10, 0.20, 0.50]
modes_G  = [1, 2, 3, 4, 5, 6, 7]

prop_G      = {}
static_G    = {}
grid_rows   = []

for m in masses_G:
    prop_G[m] = BccDiracPropagator(shape=L_G, m=m)

print(f"  {'L':>4} {'mode':>5} {'m':>5} {'k_x':>10} {'v_g':>10} {'v/c':>8}"
      f" {'ratio_lsq':>14} {'1/γ':>14} {'n-vs-p':>10} {'n-vs-SR':>10}")
print("  " + "-" * 100)

for m in masses_G:
    prop = prop_G[m]
    if m not in static_G:
        ss, _, _, _ = sr2.measure_plane_wave_phase_rate_3d_exact(
            L_G, m, 0.0, N_G, static=True, propagator=prop)
        static_G[m] = phase_rate_lsq(ss, 1.0)

    ws_lsq  = static_G[m]
    ws_pred = sr2.omega_static_qca(m)

    for n_mode in modes_G:
        k_target = 2.0 * math.pi * n_mode / L_G
        sm, vg, kxg, w = sr2.measure_plane_wave_phase_rate_3d_exact(
            L_G, m, k_target, N_G, static=False, propagator=prop)
        wm_lsq  = phase_rate_lsq(sm, 1.0)
        wm_pred = abs(w - kxg * vg)
        ratio_lsq  = wm_lsq / ws_lsq
        ratio_pred = wm_pred / ws_pred
        beta = vg / sr2.C_LAT_3D
        inv_gamma = math.sqrt(1.0 - beta*beta) if abs(beta) < 1 else float('nan')

        print(f"  {L_G:>4} {n_mode:>5} {m:>5.2f} {kxg:>10.6f} {vg:>10.6f} {beta:>8.5f}"
              f" {ratio_lsq:>14.10f} {inv_gamma:>14.10f}"
              f" {abs(ratio_lsq-ratio_pred):>10.3e} {abs(ratio_lsq-inv_gamma):>10.3e}")

        grid_rows.append({
            'L': L_G, 'mode': n_mode, 'm': m, 'kxg': kxg, 'vg': vg, 'beta': beta,
            'ratio_lsq': ratio_lsq, 'ratio_pred': ratio_pred, 'inv_gamma': inv_gamma,
            'num_vs_pred': abs(ratio_lsq-ratio_pred),
            'num_vs_SR':   abs(ratio_lsq-inv_gamma),
        })

with open(os.path.join(RESULTS_DIR, 'sr2_10x_ongrid.json'), 'w') as f:
    json.dump({'L': L_G, 'n_steps': N_G, 'rows': grid_rows}, f, indent=2)
print(f"\n{elapsed()}  On-grid scan done — saved sr2_10x_ongrid.json")


# ══════════════════════════════════════════════════════════════════
#  SECTION 5 — Top-10 priority tests
# ══════════════════════════════════════════════════════════════════

section("Top-10 tests")

import subprocess, importlib.util

TOP10_DIR = os.path.join(os.path.dirname(__file__), 'tests-priority')

def run_top10(name):
    path = os.path.join(TOP10_DIR, name)
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, path],
        capture_output=True, text=True, timeout=600)
    elapsed_s = time.time() - t0
    status = "DONE" if result.returncode == 0 else f"FAIL(rc={result.returncode})"
    print(f"  {elapsed()}  {name}: {status}  ({elapsed_s:.1f}s)")
    if result.returncode != 0:
        print("  STDERR:", result.stderr[-500:] if result.stderr else "(none)")
    return result.returncode == 0, elapsed_s, result.stdout

tests_to_run = [
    'test_01_GR1_light_deflection.py',
    'test_01b_GR1_openBC.py',
    'test_02_QM1_CHSH.py',
    'test_04_GR3_pound_rebka.py',
    'test_05_GR2_shapiro.py',
    'test_05b_GR2_openBC.py',
    'test_06_QG2_planck_LV.py',
    'test_07_QFT5_neutrino.py',
    'test_08_QM2_tunneling.py',
    'test_09_GR4_mercury.py',
    'test_10_QG4_charge.py',
]

top10_results = {}
for tname in tests_to_run:
    ok, t_test, stdout = run_top10(tname)
    top10_results[tname] = {'ok': ok, 'time_s': t_test}

passed = sum(1 for v in top10_results.values() if v['ok'])
print(f"\n  Top-10 summary: {passed}/{len(tests_to_run)} passed")
for n, v in top10_results.items():
    mark = "✓" if v['ok'] else "✗"
    print(f"    {mark} {n}  ({v['time_s']:.1f}s)")

with open(os.path.join(RESULTS_DIR, '10x_top10_summary.json'), 'w') as f:
    json.dump(top10_results, f, indent=2)


# ══════════════════════════════════════════════════════════════════
#  SECTION 6 — L-sweep: SR-2 ratio vs lattice size
#   Verify the BCC dispersion correction scales as O(k²) with L
# ══════════════════════════════════════════════════════════════════

section("L-sweep: SR-2 ratio vs lattice size  m=0.1  n_mode=1  n_steps=2000")

L_SWEEP = [32, 48, 64, 80, 96, 128]
m_sw = 0.1
N_sw = 2000
static_sw = {}

print(f"  {'L':>5} {'k_x':>10} {'v_g':>10} {'v/c':>8} "
      f"{'ratio_lsq':>14} {'1/γ':>14} {'n-vs-SR':>10}")
print("  " + "-" * 80)

lsweep_rows = []
for L_i in L_SWEEP:
    prop_i = BccDiracPropagator(shape=L_i, m=m_sw)
    if (L_i, m_sw) not in static_sw:
        ss, _, _, _ = sr2.measure_plane_wave_phase_rate_3d_exact(
            L_i, m_sw, 0.0, N_sw, static=True, propagator=prop_i)
        static_sw[(L_i, m_sw)] = phase_rate_lsq(ss, 1.0)
    ws = static_sw[(L_i, m_sw)]

    k_t = 2.0 * math.pi * 1 / L_i   # mode n=1
    sm, vg, kxg, w = sr2.measure_plane_wave_phase_rate_3d_exact(
        L_i, m_sw, k_t, N_sw, static=False, propagator=prop_i)
    wm = phase_rate_lsq(sm, 1.0)
    ratio = wm / ws
    beta  = vg / sr2.C_LAT_3D
    ig    = math.sqrt(1.0 - beta*beta) if abs(beta) < 1 else float('nan')
    print(f"  {L_i:>5} {kxg:>10.6f} {vg:>10.6f} {beta:>8.5f} "
          f"{ratio:>14.10f} {ig:>14.10f} {abs(ratio-ig):>10.3e}")
    lsweep_rows.append({'L': L_i, 'kxg': kxg, 'vg': vg, 'ratio': ratio,
                        'inv_gamma': ig, 'num_vs_SR': abs(ratio-ig)})

with open(os.path.join(RESULTS_DIR, 'sr2_10x_Lsweep.json'), 'w') as f:
    json.dump({'m': m_sw, 'n_steps': N_sw, 'rows': lsweep_rows}, f, indent=2)
print(f"\n{elapsed()}  L-sweep done — saved sr2_10x_Lsweep.json")


# ══════════════════════════════════════════════════════════════════
#  FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════

total_time = time.time() - t_script_start
print()
print("=" * 80)
print(f"ALL TESTS COMPLETE  total={total_time:.1f}s ({total_time/60:.1f} min)")
print("=" * 80)
print()
print(f"SR-2 Part B  (L={L_B}, n={N_B}):  num-vs-pred={result_B['num_vs_pred']:.3e}"
      f"  num-vs-SR={result_B['num_vs_SR']:.3e}")
print(f"SR-2 Scan    (L={L_S}, n={N_S}):  "
      f"best num-vs-SR={best_nvsS['num_vs_SR']:.3e}  "
      f"worst={worst_nvsS['num_vs_SR']:.3e}")
print(f"Top-10:  {passed}/{len(tests_to_run)} passed")
print()
print("Zero-padded DFT floor (SR-2 Part B):")
print(f"  Δω_eff (pad={PAD_FACTOR}, n={N_B}, dt=1) = {result_B['delta_omega_eff']:.3e} rad/step")
print(f"  |lsq-zpad| static  = {result_B['lsq_zpad_residual_s']:.3e}")
print(f"  |lsq-zpad| moving  = {result_B['lsq_zpad_residual_m']:.3e}")
print()
print("Saved JSON results:")
for fname in ['sr2_10x_partB.json', 'sr2_10x_scan.json',
              'sr2_10x_ongrid.json', 'sr2_10x_Lsweep.json',
              '10x_top10_summary.json']:
    print(f"  test-results/{fname}")
