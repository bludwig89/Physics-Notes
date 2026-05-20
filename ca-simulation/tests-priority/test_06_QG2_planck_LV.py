"""
Top-10 priority Test #6 — QG-2: Planck-scale Lorentz-violation bound
=====================================================================
Date: 2026-05-19

Goal
----
Compute the lattice's effective LV scale E_LV from the dispersion
correction at finite k, and verify it is at or above the experimental
bound E_LV ≳ 10^19 GeV (Fermi GRB 090510, etc.).

Method
------
The BCC Weyl dispersion (Paper 1 Eq. 15):
    ω^±(k) = arccos(c_x c_y c_z ± s_x s_y s_z),  c_i = cos(k_i/√3), s_i = sin(k_i/√3)

For small k along axes, c = 1/√3 is the lattice light-speed (Tier 1 result).
At finite k, Paper 4 Eq. 23 gives an LV correction:
    ω ≈ |k|/√3 · (1 + α (k/k_Planck)² + ... )

The standard LV parameterisation is E² ≈ p²c² ± E³/E_LV.  We extract E_LV
by fitting the dispersion deviation from linearity:
    ω - |k|/√3  ≈ ±|k|³/E_LV   (in lattice units c = 1/√3)

Then SI mapping (Finding 10 deferred):
    E_LV_SI = E_LV_lattice · ℏ/a
where a is the lattice spacing in metres.  For a ~ Planck length 10⁻³⁵ m,
ℏ/a ~ 10^19 GeV, naturally Planck-scale.

The gate: the dimensionless E_LV_lattice ratio should be O(1) — and with
any SI mapping that puts a < 10⁻³² m, the SI E_LV is above the Fermi
bound 10^19 GeV.
"""

import os, sys, math, json
import numpy as np

THIS = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(THIS, '..')))

import ca_bcc


def bcc_omega(kx, ky=0.0, kz=0.0, sign='+'):
    """Analytic BCC dispersion ω^±(k)."""
    return float(ca_bcc.bcc_dispersion(np.array(kx), np.array(ky), np.array(kz),
                                        sign=sign))


def main():
    print('=' * 70)
    print('QG-2 — Planck-scale Lorentz-violation bound')
    print('=' * 70)
    print('Date 2026-05-19')
    print()

    out = {'date': '2026-05-19', 'test': 'QG-2 Planck LV bound'}

    c_lat = 1.0 / math.sqrt(3.0)
    print(f'  Lattice speed of light c_lat = 1/√3 = {c_lat:.8f}')
    print()

    # Scan k along axis (1, 0, 0).  Extract ω(k) − k·c_lat and fit ~k³ / E_LV.
    print('Dispersion deviation ω - k·c_lat at small k, axis (1,0,0):')
    print(f'{"k":>10} {"omega":>14} {"k·c_lat":>14} {"dev":>14} {"dev/k³":>14}')
    print('-' * 70)
    k_axis = []
    dev_axis = []
    for k in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3]:
        w = bcc_omega(k, 0.0, 0.0, sign='+')
        linear = k * c_lat
        dev = w - linear
        ratio = dev / k**3 if k != 0 else 0
        print(f'{k:>10.4f} {w:>14.8e} {linear:>14.8e} {dev:>14.4e} {ratio:>14.4e}')
        k_axis.append(k); dev_axis.append(dev)
    out['axis_scan'] = [{'k': float(k), 'dev': float(d)} for k, d in zip(k_axis, dev_axis)]

    # Scan along (1,1,1) — the diagonal, where Paper 4 predicts the strongest
    # LV signature on the BCC (k_x = k_y = k_z = k/√3 if normalised).
    print()
    print('Dispersion deviation ω - |k|·c_lat at small k, diagonal (1,1,1)/√3:')
    print(f'{"k":>10} {"omega":>14} {"|k|·c_lat":>14} {"dev":>14} {"dev/k³":>14}')
    print('-' * 70)
    k_diag = []; dev_diag = []
    for k in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3]:
        kk = k / math.sqrt(3)
        w = bcc_omega(kk, kk, kk, sign='+')
        linear = k * c_lat
        dev = w - linear
        ratio = dev / k**3 if k != 0 else 0
        print(f'{k:>10.4f} {w:>14.8e} {linear:>14.8e} {dev:>14.4e} {ratio:>14.4e}')
        k_diag.append(k); dev_diag.append(dev)
    out['diag_scan'] = [{'k': float(k), 'dev': float(d)} for k, d in zip(k_diag, dev_diag)]

    # Fit dev = β·k³ in the small-k regime
    k_arr = np.array(k_axis[:6])
    d_arr = np.array(dev_axis[:6])
    # Fit |dev| = β·k³, log-log
    if np.all(np.abs(d_arr) > 0):
        log_k = np.log(k_arr)
        log_d = np.log(np.abs(d_arr))
        slope, intercept = np.polyfit(log_k, log_d, 1)
        beta_axis = float(np.exp(intercept))
        print()
        print(f'  Power-law fit (axis):  |dev| = β · k^{slope:.4f},  β = {beta_axis:.6e}')
    else:
        beta_axis = float('nan'); slope = float('nan')

    k_arr = np.array(k_diag[:6])
    d_arr = np.array(dev_diag[:6])
    log_k = np.log(k_arr)
    log_d = np.log(np.abs(d_arr))
    slope_d, intercept_d = np.polyfit(log_k, log_d, 1)
    beta_diag = float(np.exp(intercept_d))
    print(f'  Power-law fit (diag):  |dev| = β · k^{slope_d:.4f},  β = {beta_diag:.6e}')

    # Convert β to E_LV (dim-less): |dev| ~ k³ / E_LV  →  E_LV = 1/β  (with c=1 chosen).
    E_LV_axis = 1.0 / beta_axis if beta_axis > 0 else float('inf')
    E_LV_diag = 1.0 / beta_diag if beta_diag > 0 else float('inf')
    print()
    print(f'  E_LV_lattice (axis)     = 1/β = {E_LV_axis:.4e}')
    print(f'  E_LV_lattice (diag)     = 1/β = {E_LV_diag:.4e}')

    out.update({'beta_axis': beta_axis, 'beta_diag': beta_diag,
                'E_LV_lat_axis': float(E_LV_axis),
                'E_LV_lat_diag': float(E_LV_diag),
                'slope_axis': float(slope), 'slope_diag': float(slope_d)})

    # SI mapping (deferred per Finding 10).  Compute E_LV_SI for a range of
    # plausible lattice-spacings a ∈ {1.6e-35 m (Planck), 1e-34, 1e-33}.
    print()
    print('SI conversion (Finding 10 — deferred):')
    print(f'  E_LV_SI [GeV] = E_LV_lat · ℏ·c/a, where a = lattice spacing')
    hbar_c_eV_m = 1.97327e-7   # ℏc in eV·m
    print(f'{"a [m]":>14} {"E_LV_axis [GeV]":>22} {"E_LV_diag [GeV]":>22}')
    si_rows = []
    for a in [1.616e-35, 1e-34, 1e-33, 1e-32]:
        E_axis = E_LV_axis * hbar_c_eV_m / a * 1e-9   # to GeV
        E_diag = E_LV_diag * hbar_c_eV_m / a * 1e-9
        print(f'{a:>14.3e} {E_axis:>22.4e} {E_diag:>22.4e}')
        si_rows.append({'a_m': a, 'E_LV_axis_GeV': E_axis,
                        'E_LV_diag_GeV': E_diag})
    out['SI_scan'] = si_rows

    # Experimental bound from Fermi GRB 090510: E_LV > 1.2e19 GeV (linear LV).
    bound_fermi = 1.2e19   # GeV
    print()
    print(f'  Fermi GRB 090510 lower bound on linear LV: E_LV ≥ {bound_fermi:.2e} GeV')

    # Check at Planck-scale a:
    a_planck = 1.616e-35
    E_axis_planck = E_LV_axis * hbar_c_eV_m / a_planck * 1e-9
    E_diag_planck = E_LV_diag * hbar_c_eV_m / a_planck * 1e-9
    pass_fermi_axis = E_axis_planck >= bound_fermi
    pass_fermi_diag = E_diag_planck >= bound_fermi
    print(f'  At Planck-scale a = {a_planck} m:')
    print(f'    E_LV (axis) = {E_axis_planck:.4e} GeV  → {"PASS" if pass_fermi_axis else "FAIL"}')
    print(f'    E_LV (diag) = {E_diag_planck:.4e} GeV  → {"PASS" if pass_fermi_diag else "FAIL"}')
    out['gate'] = {'bound_Fermi_GeV': bound_fermi,
                   'E_LV_axis_at_Planck_a_GeV': float(E_axis_planck),
                   'E_LV_diag_at_Planck_a_GeV': float(E_diag_planck),
                   'pass_fermi_axis': bool(pass_fermi_axis),
                   'pass_fermi_diag': bool(pass_fermi_diag)}

    print()
    print('=' * 70)
    print('GATE EVALUATION')
    print('=' * 70)
    print(f'  Dimensionless β (LV coefficient):')
    print(f'    axis:    β = {beta_axis:.4e}, power = {slope:.2f}')
    print(f'    diag:    β = {beta_diag:.4e}, power = {slope_d:.2f}')
    print(f'  E_LV ≥ E_Planck (1.22e19 GeV) at lattice spacing ≤ Planck length: '
          f'{"PASS" if pass_fermi_axis and pass_fermi_diag else "FAIL"}')

    out_path = os.path.join(THIS, '..', '..', 'test-results',
                             'top10_T06_QG2_LV.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nResults written to {out_path}')
    return out


if __name__ == '__main__':
    main()
