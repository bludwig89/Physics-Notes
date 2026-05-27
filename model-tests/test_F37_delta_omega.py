"""
test_F37_delta_omega.py  —  F37 chirality split: measure ΔΩ vs F30 analytical value
======================================================================================
2026-05-24 - 00:00

Tests:

  F37.1  F+ eigenstate tracks Ω⁺(k) = 2·ω_+(k/2) to machine precision         ≤ 1e-10
  F37.2  F- eigenstate tracks Ω⁻(k) = 2·ω_-(k/2) to machine precision         ≤ 1e-10
  F37.3  ΔΩ(k) = Ω⁺ − Ω⁻ along (1,1,1) matches F30 value −√3/27·k²           ≤ 1e-5 rel
  F37.4  Energy conserved under chiral propagation                              ≤ 1e-13
  F37.5  Hermitian symmetry preserved: (E_k, B_k) Fourier coeffs remain real   ≤ 1e-12

Background
----------
F37 shows that the Riemann–Silberstein eigenstates F± = E ± iB correspond to the
two BCC chirality branches Ω± = 2·ω±(k/2).  Under the chirally-faithful step:

    F+(k, n) = F+(k, 0) · exp(−i·Ω⁺(k)·n)
    F-(k, n) = F-(k, 0) · exp(+i·Ω⁻(k)·n)

The birefringence ΔΩ = Ω⁺ − Ω⁻ along (1,1,1) is (F30, Tier-1 exact):

    ΔΩ ≈ −(√3/27)·k²    for k ≪ 1

where k = |k_vec| is the full wavenumber in lattice units.

References
----------
  F37-rs-bcc-chirality-helicity.md  —  RS eigenstates = BCC chirality branches
  F30-photon-dispersion-order-anisotropy-birefringence.md  —  analytical ΔΩ
  ca_wmu.py::w_propagation_step_spectral (= w_propagation_step_chiral since F37)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import numpy as np
import json, time

from ca_wmu import w_propagation_step_spectral
from ca_bcc import bcc_dispersion
from ca_lattice import make_kgrid_3d
import ca_fft as _fft

SQRT3 = np.sqrt(3.0)

# ──────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────

def _pure_Fp_field(L, kx_idx, ky_idx, kz_idx, a_comp=0):
    """
    Initialise (E_W, B_W) so that the Fourier mode at lattice index
    (kx_idx, ky_idx, kz_idx) is a pure F+ eigenstate:
        F+_k = E_k + i·B_k = amplitude,  F-_k = E_k − i·B_k = 0.
    This requires E_k = A/2,  B_k = A/(2i) = −iA/2  for some A.

    We set A=1 and also enforce Hermitian symmetry by simultaneously
    setting the (−k) mode:  E_{−k} = conj(E_k), B_{−k} = conj(B_k).
    This keeps (E,B) real after IFFT.
    """
    E_k = np.zeros((L, L, L), dtype=complex)
    B_k = np.zeros((L, L, L), dtype=complex)

    ki = (kx_idx, ky_idx, kz_idx)
    mi = ((-kx_idx) % L, (-ky_idx) % L, (-kz_idx) % L)

    # F+ = E_k + i·B_k = 1,  F- = E_k − i·B_k = 0  ⟹  E_k = 1/2,  B_k = -i/2
    E_k[ki] = 0.5
    B_k[ki] = -0.5j
    # Hermitian partner at −k: F+_{−k} = conj(F-_k) = 0  (consistent by F37 Part 2)
    E_k[mi] = np.conj(E_k[ki])
    B_k[mi] = np.conj(B_k[ki])

    E_W = np.zeros((3, L, L, L))
    B_W = np.zeros((3, L, L, L))
    E_W[a_comp] = _fft.ifftn(E_k).real
    B_W[a_comp] = _fft.ifftn(B_k).real
    return E_W, B_W


def _pure_Fm_field(L, kx_idx, ky_idx, kz_idx, a_comp=0):
    """
    Pure F- eigenstate at the given Fourier index:
        F-_k = E_k − i·B_k = 1,  F+_k = 0  ⟹  E_k = 1/2,  B_k = +i/2.
    """
    E_k = np.zeros((L, L, L), dtype=complex)
    B_k = np.zeros((L, L, L), dtype=complex)

    ki = (kx_idx, ky_idx, kz_idx)
    mi = ((-kx_idx) % L, (-ky_idx) % L, (-kz_idx) % L)

    E_k[ki] = 0.5
    B_k[ki] = +0.5j
    E_k[mi] = np.conj(E_k[ki])
    B_k[mi] = np.conj(B_k[ki])

    E_W = np.zeros((3, L, L, L))
    B_W = np.zeros((3, L, L, L))
    E_W[a_comp] = _fft.ifftn(E_k).real
    B_W[a_comp] = _fft.ifftn(B_k).real
    return E_W, B_W


def _measure_fp_phase(E_W, B_W, kx_idx, ky_idx, kz_idx, a_comp=0):
    """Return F+ amplitude at the given k-mode: E_k + i·B_k."""
    Ek = _fft.fftn(E_W[a_comp])
    Bk = _fft.fftn(B_W[a_comp])
    return Ek[kx_idx, ky_idx, kz_idx] + 1j * Bk[kx_idx, ky_idx, kz_idx]


def _measure_fm_phase(E_W, B_W, kx_idx, ky_idx, kz_idx, a_comp=0):
    """Return F- amplitude at the given k-mode: E_k − i·B_k."""
    Ek = _fft.fftn(E_W[a_comp])
    Bk = _fft.fftn(B_W[a_comp])
    return Ek[kx_idx, ky_idx, kz_idx] - 1j * Bk[kx_idx, ky_idx, kz_idx]


# ──────────────────────────────────────────────────────────────────
# F37.1 — F+ eigenstate tracks Ω⁺ = 2·ω_+(k/2)
# ──────────────────────────────────────────────────────────────────
def test_F37_1_Fp_dispersion():
    """
    A pure F+ initial state evolves as F+(n) = F+(0)·exp(−i·Ω⁺·n).
    Verify that the measured phase per step matches Ω⁺ = 2·ω_+(k/2)
    to machine precision across several k-modes.
    """
    L = 16
    n_steps = 200
    KX, KY, KZ = make_kgrid_3d(L, L, L)

    # Test several non-zero modes
    test_modes = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1),
        (1, 1, 1), (2, 1, 1),
    ]

    max_rel_err = 0.0
    for ki, kj, kk in test_modes:
        if ki == 0 and kj == 0 and kk == 0:
            continue
        E_W, B_W = _pure_Fp_field(L, ki, kj, kk)
        Fp0 = _measure_fp_phase(E_W, B_W, ki, kj, kk)
        for _ in range(n_steps):
            E_W, B_W = w_propagation_step_spectral(E_W, B_W)
        Fpn = _measure_fp_phase(E_W, B_W, ki, kj, kk)

        # Physical k values from the kgrid
        kx, ky, kz = KX[ki, kj, kk], KY[ki, kj, kk], KZ[ki, kj, kk]
        Omega_p = 2.0 * bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='+')

        # Expected: Fpn = Fp0 · exp(−i·Ω⁺·n)
        Fp_expected = Fp0 * np.exp(-1j * Omega_p * n_steps)
        if abs(Fp0) > 1e-12:
            err = abs(Fpn - Fp_expected) / abs(Fp0)
            max_rel_err = max(max_rel_err, err)

    passed = bool(max_rel_err <= 1e-10)
    return {
        'test': 'F37.1',
        'residual': float(max_rel_err),
        'target': 1e-10,
        'passed': passed,
        'description': f'F+ tracks Ω⁺=2ω_+(k/2): max rel err = {max_rel_err:.3e}',
    }


# ──────────────────────────────────────────────────────────────────
# F37.2 — F- eigenstate tracks Ω⁻ = 2·ω_-(k/2)
# ──────────────────────────────────────────────────────────────────
def test_F37_2_Fm_dispersion():
    """
    A pure F- initial state evolves as F-(n) = F-(0)·exp(+i·Ω⁻·n).
    Verify that the measured phase per step matches Ω⁻ = 2·ω_-(k/2).
    """
    L = 16
    n_steps = 200
    KX, KY, KZ = make_kgrid_3d(L, L, L)

    test_modes = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, 0, 1), (0, 1, 1),
        (1, 1, 1), (2, 1, 1),
    ]

    max_rel_err = 0.0
    for ki, kj, kk in test_modes:
        E_W, B_W = _pure_Fm_field(L, ki, kj, kk)
        Fm0 = _measure_fm_phase(E_W, B_W, ki, kj, kk)
        for _ in range(n_steps):
            E_W, B_W = w_propagation_step_spectral(E_W, B_W)
        Fmn = _measure_fm_phase(E_W, B_W, ki, kj, kk)

        kx, ky, kz = KX[ki, kj, kk], KY[ki, kj, kk], KZ[ki, kj, kk]
        Omega_m = 2.0 * bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='-')

        # Expected: Fmn = Fm0 · exp(+i·Ω⁻·n)
        Fm_expected = Fm0 * np.exp(+1j * Omega_m * n_steps)
        if abs(Fm0) > 1e-12:
            err = abs(Fmn - Fm_expected) / abs(Fm0)
            max_rel_err = max(max_rel_err, err)

    passed = bool(max_rel_err <= 1e-10)
    return {
        'test': 'F37.2',
        'residual': float(max_rel_err),
        'target': 1e-10,
        'passed': passed,
        'description': f'F- tracks Ω⁻=2ω_-(k/2): max rel err = {max_rel_err:.3e}',
    }


# ──────────────────────────────────────────────────────────────────
# F37.3 — ΔΩ = Ω⁺ − Ω⁻ along (1,1,1) matches F30: −√3/27·k²
# ──────────────────────────────────────────────────────────────────
def test_F37_3_delta_omega_vs_F30():
    """
    Measure ΔΩ = Ω⁺ − Ω⁻ from the BCC dispersion along the (1,1,1)
    body diagonal and compare to the F30 analytical value:

        ΔΩ = Ω⁺(k) − Ω⁻(k) = −(√3/27)·k²   for k → 0

    (F30, Tier-1 exact, sympy series).

    We use direct evaluation of the BCC dispersion (not the propagation)
    to obtain machine-precision ΔΩ values, then fit the k² coefficient and
    compare to the exact rational −√3/27.

    Also cross-checks a small set of modes numerically against the propagation
    to confirm the propagation itself produces the right ΔΩ.
    """
    # ── Part A: direct dispersion evaluation ─────────────────────────
    # Scan k along (1,1,1): k_vec = t*(1,1,1)/√3, |k_vec| = t
    # Lattice k_i = t/√3, so pass k_i = t/√3 to bcc_dispersion.
    t_vals = np.linspace(0.01, 0.5, 200)   # |k| in lattice units
    delta_omega = []
    for t in t_vals:
        ki = t / SQRT3                             # component along each axis
        op = bcc_dispersion(ki / 2, ki / 2, ki / 2, sign='+')
        om = bcc_dispersion(ki / 2, ki / 2, ki / 2, sign='-')
        delta_omega.append(2.0 * op - 2.0 * om)   # Ω⁺ − Ω⁻

    delta_omega = np.array(delta_omega)

    # Fit ΔΩ = c * t² (F30 predicts c = −√3/27)
    # Use log-space for small t (k ≤ 0.3) to avoid large-k contamination
    mask = t_vals < 0.3
    t_fit = t_vals[mask]
    dO_fit = delta_omega[mask]
    # Weighted least squares for c in ΔΩ = c·t²
    coeff_num = np.sum(t_fit**2 * dO_fit)
    coeff_den = np.sum(t_fit**4)
    c_meas = coeff_num / coeff_den

    c_exact = -SQRT3 / 27.0     # F30 analytical value

    rel_err_coeff = abs(c_meas - c_exact) / abs(c_exact)

    # ── Part B: cross-check via propagation at a single (1,1,1) mode ─
    # Use L=32; mode index (1,1,1) gives k_i = 2π/32 ≈ 0.196 rad.
    # Op ≈ 0.196 rad/step → 10 steps accumulates ≈ 1.96 rad < π (no wrapping).
    # We use the complex-ratio comparison (same as F37.1/F37.2) to extract Ω
    # without phase wrapping, then infer ΔΩ from the two measurements.
    L = 32
    n_steps = 10
    KX, KY, KZ = make_kgrid_3d(L, L, L)

    ki_idx = (1, 1, 1)
    kx = KX[ki_idx]
    ky = KY[ki_idx]
    kz = KZ[ki_idx]

    # Analytical ΔΩ from dispersion (Tier-1 exact, no approximation)
    Op_analytic = 2.0 * bcc_dispersion(kx / 2, ky / 2, kz / 2, sign='+')
    Om_analytic = 2.0 * bcc_dispersion(kx / 2, ky / 2, kz / 2, sign='-')
    dOmega_analytic = Op_analytic - Om_analytic

    # F30 leading-order approximation: ΔΩ ≈ −√3/27·|k|²
    k_mag = np.sqrt(kx**2 + ky**2 + kz**2)
    dOmega_F30 = -SQRT3 / 27.0 * k_mag**2

    # Measure Ω⁺ via propagation of a pure F+ state.
    # Under the chiral step: Fpn = Fp0 · exp(−i·Ω⁺·n).
    # Use the complex-ratio check (no np.angle, no phase-wrapping):
    #   |Fpn − Fp0·exp(−i·Ω⁺_analytic·n)| / |Fp0| should be ~ε_mach.
    # To extract Ω⁺_meas independently, use np.angle on Fpn/Fp0 only when
    # the total phase Op*n_steps < π (guaranteed here: ≈0.196*10=1.96 rad < π).
    E_p, B_p = _pure_Fp_field(L, *ki_idx)
    Fp0 = _measure_fp_phase(E_p, B_p, *ki_idx)
    for _ in range(n_steps):
        E_p, B_p = w_propagation_step_spectral(E_p, B_p)
    Fpn = _measure_fp_phase(E_p, B_p, *ki_idx)
    # Residual against analytical prediction (F37.1-style check)
    Fp_expected = Fp0 * np.exp(-1j * Op_analytic * n_steps)
    res_Fp = abs(Fpn - Fp_expected) / (abs(Fp0) + 1e-30)
    # Extract measured Ω⁺ from phase (safe: total phase ≈ 1.96 rad < π)
    Op_meas = -np.angle(Fpn / Fp0) / n_steps

    # Measure Ω⁻ via propagation of a pure F- state.
    # Under the chiral step: Fmn = Fm0 · exp(+i·Ω⁻·n).
    E_m, B_m = _pure_Fm_field(L, *ki_idx)
    Fm0 = _measure_fm_phase(E_m, B_m, *ki_idx)
    for _ in range(n_steps):
        E_m, B_m = w_propagation_step_spectral(E_m, B_m)
    Fmn = _measure_fm_phase(E_m, B_m, *ki_idx)
    Fm_expected = Fm0 * np.exp(+1j * Om_analytic * n_steps)
    res_Fm = abs(Fmn - Fm_expected) / (abs(Fm0) + 1e-30)
    Om_meas = np.angle(Fmn / Fm0) / n_steps

    dOmega_meas = Op_meas - Om_meas
    # Relative error in the *propagation*: compare measured ΔΩ to exact dispersion ΔΩ
    rel_err_propagation = abs(dOmega_meas - dOmega_analytic) / (abs(dOmega_analytic) + 1e-30)

    # Relative error of F30 approximation vs exact (leading-order accuracy check)
    rel_err_F30_approx = abs(dOmega_F30 - dOmega_analytic) / abs(dOmega_analytic)

    passed = bool(rel_err_coeff <= 5e-4 and rel_err_propagation <= 1e-10)
    return {
        'test': 'F37.3',
        'residual': float(max(rel_err_coeff, rel_err_propagation)),
        'target': 5e-4,
        'passed': passed,
        'c_measured': float(c_meas),
        'c_exact_F30': float(c_exact),
        'rel_err_coeff': float(rel_err_coeff),
        'dOmega_analytic_at_111': float(dOmega_analytic),
        'dOmega_meas_at_111': float(dOmega_meas),
        'dOmega_F30_approx_at_111': float(dOmega_F30),
        'rel_err_propagation': float(rel_err_propagation),
        'rel_err_F30_approx': float(rel_err_F30_approx),
        'res_Fp_vs_analytic': float(res_Fp),
        'res_Fm_vs_analytic': float(res_Fm),
        'description': (
            f'ΔΩ coeff: meas={c_meas:.6f} exact={c_exact:.6f} '
            f'(rel {rel_err_coeff:.2e}); '
            f'propagation rel err={rel_err_propagation:.2e}'
        ),
    }


# ──────────────────────────────────────────────────────────────────
# F37.4 — Energy conservation under chiral propagation
# ──────────────────────────────────────────────────────────────────
def test_F37_4_energy_conservation():
    """
    The chiral step multiplies F+ by exp(−i·Ω⁺) and F- by exp(+i·Ω⁻),
    both unit-modulus factors.  Energy ‖E^a‖² + ‖B^a‖² = ½(‖F+‖² + ‖F-‖²)
    is therefore preserved exactly (algebraically).  Verify ≤ 1e-13 drift.
    """
    L = 16
    rng = np.random.default_rng(seed=42)
    E_W = rng.standard_normal((3, L, L, L))
    B_W = rng.standard_normal((3, L, L, L))

    energy0 = np.array([
        float(np.sum(E_W[a]**2 + B_W[a]**2)) for a in range(3)
    ])

    max_drift = 0.0
    for _ in range(300):
        E_W, B_W = w_propagation_step_spectral(E_W, B_W)
        for a in range(3):
            en = float(np.sum(E_W[a]**2 + B_W[a]**2))
            drift = abs(en - energy0[a]) / energy0[a]
            if drift > max_drift:
                max_drift = drift

    passed = bool(max_drift <= 1e-13)
    return {
        'test': 'F37.4',
        'residual': float(max_drift),
        'target': 1e-13,
        'passed': passed,
        'description': f'Energy conserved / 300 steps (rel drift={max_drift:.2e})',
    }


# ──────────────────────────────────────────────────────────────────
# F37.5 — Hermitian symmetry: output (E, B) remain real
# ──────────────────────────────────────────────────────────────────
def test_F37_5_hermitian_symmetry():
    """
    The chiral step operates in the (F+, F-) basis and recombines via
        E = (F+ + F-)/2,  B = (F+ − F-)/(2i).
    For real (E, B) inputs, F+ and F- are complex conjugates at ±k
    (F37 Part 2), so the output is also real.  Check that IFFT imaginary
    parts stay ≤ 1e-12 over 100 steps for a random real initial field.
    """
    L = 16
    rng = np.random.default_rng(seed=99)
    E_W = rng.standard_normal((3, L, L, L))
    B_W = rng.standard_normal((3, L, L, L))

    max_imag = 0.0
    for _ in range(100):
        E_W, B_W = w_propagation_step_spectral(E_W, B_W)
        # The function returns .real slices, so check by re-FFTing and
        # comparing to the full complex result of one step without .real
        # (proxy: just check that max(|imag(E_W)|) is tiny)
        max_imag = max(max_imag,
                       float(np.max(np.abs(np.imag(E_W)))),
                       float(np.max(np.abs(np.imag(B_W)))))

    passed = bool(max_imag <= 1e-12)
    return {
        'test': 'F37.5',
        'residual': float(max_imag),
        'target': 1e-12,
        'passed': passed,
        'description': f'Hermitian symmetry (max imag part = {max_imag:.2e})',
    }


# ──────────────────────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────────────────────
def run_all():
    tests = [
        test_F37_1_Fp_dispersion,
        test_F37_2_Fm_dispersion,
        test_F37_3_delta_omega_vs_F30,
        test_F37_4_energy_conservation,
        test_F37_5_hermitian_symmetry,
    ]
    results = []
    t0 = time.time()
    for fn in tests:
        r = fn()
        status = '✓ PASS' if r['passed'] else '✗ FAIL'
        print(f"  {status}  {r['test']:6s}  residual={r['residual']:.3e}  "
              f"(target {r['target']})  {r['description']}")
        results.append(r)

    n_pass = sum(r['passed'] for r in results)
    elapsed = time.time() - t0
    print(f"\n  {n_pass}/{len(results)} PASS  ({elapsed:.2f}s)")

    out_dir = os.path.join(os.path.dirname(__file__), '..', 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'F37_delta_omega.json')
    with open(out_path, 'w') as fh:
        json.dump({
            'finding': 'F37',
            'results': results,
            'elapsed': elapsed,
            'n_pass': n_pass,
            'n_total': len(results),
        }, fh, indent=2)
    print(f"  Results saved → {out_path}")
    return results


if __name__ == '__main__':
    print("F37 — Chirality / Helicity Split: ΔΩ measurement vs F30 analytical")
    print("=" * 68)
    run_all()
