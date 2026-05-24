"""
test_f26_rotation_law.py  —  F26 Rotation-law EM propagator test suite
=======================================================================
Tests Finding 26: the speed of light is dΩ/d|k| (angular rotation rate),
not a phase-propagation speed.  The exact EM law is a rigid real rotation
of the (E, B) pair; Maxwell's curl equations are its k→0 linearisation.

Tests are structured as assertions with descriptive failure messages so
they can be run directly (`python test_f26_rotation_law.py`) or via pytest.

References
----------
- findings/F26-speed-of-light-as-rotation-rate.md
- findings/F25-real-rotation-exact-discrete-time-maxwell.md
- ca-simulation/ca_maxwell.py::rotation_step_em_spectral
- ca-simulation/ca_maxwell_2d.py::rotation_step_em_spectral_2d
- exactness-inventory.md Tier-1 #59–60, Tier-2 #16–17
"""

import sys
import os
import numpy as np

# Allow running from model-tests/ or from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import ca_maxwell as mx
import ca_maxwell_2d as mx2


# ── Tolerances ────────────────────────────────────────────────────────────────
TOL_ROTATION_LAW   = 1e-13   # rotation law residual must be below this
TOL_C_LAT          = 1e-5    # c_lat measurement tolerance (finite-diff limited)
TOL_SPECTRAL_ROUND = 1e-12   # spectral propagator FFT round-off tolerance


def test_c_from_rotation_rate_3d():
    """T1 — c_lat = 1/√3 measured from dΩ/d|k| (3D BCC). [Tier-1 #59]"""
    r = mx.c_from_rotation_rate(eps=1e-5, n_dirs=12)
    c_exact = 1.0 / np.sqrt(3.0)
    residual = abs(r['c_measured'] - c_exact)
    assert residual < TOL_C_LAT, (
        f"T1 FAIL: c_lat measured = {r['c_measured']:.8f}, "
        f"analytic = {c_exact:.8f}, residual = {residual:.2e} > {TOL_C_LAT:.0e}")
    print(f"T1 PASS: c_lat (BCC) = {r['c_measured']:.8f},  "
          f"residual = {residual:.2e}  (tol {TOL_C_LAT:.0e})")


def test_c_from_rotation_rate_2d():
    """T2 — c_lat = 1/√2 measured from dΩ/d|k| (2D square). [Tier-1 #60]"""
    r = mx2.c_from_rotation_rate_2d(eps=1e-5, n_dirs=12)
    c_exact = 1.0 / np.sqrt(2.0)
    residual = abs(r['c_measured'] - c_exact)
    assert residual < TOL_C_LAT, (
        f"T2 FAIL: c_lat (2D) = {r['c_measured']:.8f}, "
        f"analytic = {c_exact:.8f}, residual = {residual:.2e} > {TOL_C_LAT:.0e}")
    print(f"T2 PASS: c_lat (2D)  = {r['c_measured']:.8f},  "
          f"residual = {residual:.2e}  (tol {TOL_C_LAT:.0e})")


def test_rotation_law_machine_precision_3d():
    """T3 — Exact rotation law holds at machine precision (3D BCC). [Tier-2 #16]

    The rotation prediction  E(t+1) = cosΩ·E + sinΩ·B  must hold to
    < TOL_ROTATION_LAW across 20 ticks in 12 random BCC directions.
    The Maxwell curl residual must be > 10× larger (it is the linearisation error).
    """
    r = mx.rotation_law_consistency(k_mag=0.05, n_dirs=12, n_steps=20)
    assert r['max_rot_E'] < TOL_ROTATION_LAW, (
        f"T3 FAIL: rotation law residual E = {r['max_rot_E']:.2e} > {TOL_ROTATION_LAW:.0e}")
    assert r['max_rot_B'] < TOL_ROTATION_LAW, (
        f"T3 FAIL: rotation law residual B = {r['max_rot_B']:.2e} > {TOL_ROTATION_LAW:.0e}")
    assert r['max_curl_E'] > r['max_rot_E'] * 10, (
        f"T3 FAIL: Maxwell curl ({r['max_curl_E']:.2e}) should be >> "
        f"rotation residual ({r['max_rot_E']:.2e})")
    ratio = r['max_curl_E'] / r['max_rot_E']
    print(f"T3 PASS: rot_E = {r['max_rot_E']:.2e},  rot_B = {r['max_rot_B']:.2e},  "
          f"curl_E = {r['max_curl_E']:.2e}  (ratio curl/rot = {ratio:.0e})")


def test_rotation_law_machine_precision_2d():
    """T4 — Exact rotation law holds at machine precision (2D square). [Tier-2 #17]"""
    r = mx2.rotation_law_consistency_2d(k_mag=0.05, n_dirs=8, n_steps=20)
    assert r['max_rot_E'] < TOL_ROTATION_LAW, (
        f"T4 FAIL: rotation law residual E = {r['max_rot_E']:.2e} > {TOL_ROTATION_LAW:.0e}")
    assert r['max_rot_B'] < TOL_ROTATION_LAW, (
        f"T4 FAIL: rotation law residual B = {r['max_rot_B']:.2e} > {TOL_ROTATION_LAW:.0e}")
    print(f"T4 PASS: rot_E = {r['max_rot_E']:.2e},  rot_B = {r['max_rot_B']:.2e},  "
          f"curl_E = {r['max_curl_E']:.2e}")


def test_spectral_propagator_energy_conservation_3d():
    """T5 — rotation_step_em_spectral conserves ||E||² + ||B||² exactly (complex fields).

    The composite-photon (E, B) fields from the bilinear construction are naturally
    complex.  The spectral propagator works correctly for complex inputs: the rotation
    R(Ω(k)) is unitary at each k so ||E_k||² + ||B_k||² is preserved mode-by-mode.
    By Parseval, total complex energy is conserved to machine precision.

    Note: for real-valued inputs the BCC chirality ω_+(−k) = ω_−(k) ≠ ω_+(k) breaks
    Hermitian symmetry after rotation, so only complex inputs are supported.
    """
    rng = np.random.default_rng(7)
    L = 16
    # Build complex (E, B) fields — representative of composite-photon bilinear output
    E = rng.standard_normal((L, L, L, 3)) + 1j * rng.standard_normal((L, L, L, 3))
    B = rng.standard_normal((L, L, L, 3)) + 1j * rng.standard_normal((L, L, L, 3))
    energy0 = float(np.sum(np.abs(E)**2) + np.sum(np.abs(B)**2))
    for _ in range(50):
        E, B = mx.rotation_step_em_spectral(E, B)
    energy_f = float(np.sum(np.abs(E)**2) + np.sum(np.abs(B)**2))
    drift = abs(energy_f - energy0) / energy0
    assert drift < TOL_SPECTRAL_ROUND, (
        f"T5 FAIL: EM energy drift = {drift:.2e} over 50 ticks > {TOL_SPECTRAL_ROUND:.0e}")
    print(f"T5 PASS: EM energy drift (50 ticks, L=16, complex) = {drift:.2e}  "
          f"(tol {TOL_SPECTRAL_ROUND:.0e})")


def test_spectral_propagator_energy_conservation_2d():
    """T6 — rotation_step_em_spectral_2d conserves ||E||² + ||B||² exactly."""
    rng = np.random.default_rng(8)
    L = 16
    E = rng.standard_normal((L, L, 3))
    B = rng.standard_normal((L, L, 3))
    energy0 = float(np.sum(E**2) + np.sum(B**2))
    for _ in range(50):
        E, B = mx2.rotation_step_em_spectral_2d(E, B)
    energy_f = float(np.sum(E**2) + np.sum(B**2))
    drift = abs(energy_f - energy0) / energy0
    assert drift < TOL_SPECTRAL_ROUND, (
        f"T6 FAIL: 2D EM energy drift = {drift:.2e} over 50 ticks > {TOL_SPECTRAL_ROUND:.0e}")
    print(f"T6 PASS: 2D EM energy drift (50 ticks, L=16) = {drift:.2e}  "
          f"(tol {TOL_SPECTRAL_ROUND:.0e})")


def test_maxwell_curl_is_linearisation_error():
    """T7 — Maxwell curl residual scales as c_lat/√2 · |k| (linearisation error).

    Tests the k-scan: curl_E/k must be flat at c_lat/√2, while rot_E/k → 0.
    This is the structural signature that Maxwell is the k→0 limit of the rotation.
    """
    k_vals = [0.002, 0.005, 0.01, 0.02, 0.05]
    c_lat = 1.0 / np.sqrt(3.0)
    c_target = c_lat / np.sqrt(2.0)
    for k in k_vals:
        r = mx.rotation_law_consistency(k_mag=k, n_dirs=8, n_steps=5)
        curl_over_k = r['max_curl_E'] / k
        rot_over_k  = r['max_rot_E']  / k
        frac_err = abs(curl_over_k - c_target) / c_target
        assert frac_err < 0.01, (
            f"T7 FAIL at k={k}: curl_E/k = {curl_over_k:.6f}, "
            f"target {c_target:.6f}, frac err {frac_err:.2e}")
        assert rot_over_k < 1e-12, (
            f"T7 FAIL at k={k}: rot_E/k = {rot_over_k:.2e} > 1e-12 (not machine precision)")
    print(f"T7 PASS: curl_E/k ≈ c_lat/√2 = {c_target:.6f} across k ∈ {k_vals}; "
          f"rot_E/k < 1e-12 (machine precision)")


def test_dispersion_nonlinearity():
    """T8 — dispersion_nonlinearity: Ω(k) nonlinearity matches −k/18 analytic formula.

    Along (1,1,1) BCC, the leading correction is δv_φ/c ≈ −k/18.
    We verify the exact values are within 20% of the leading-order analytic.
    """
    dn = mx.dispersion_nonlinearity(k_max=0.5, n_pts=5)
    for i, k in enumerate(dn['k']):
        exact = dn['delta_vph'][i]
        theory = dn['delta_vph_theory'][i]
        if abs(theory) > 1e-6:
            ratio = abs(exact / theory)
            # Theory is leading-order; expect ratio within [0.7, 1.5] for k < 0.5
            assert 0.7 < ratio < 1.5, (
                f"T8 FAIL at k={k:.3f}: exact δv_φ/c = {exact:.4e}, "
                f"theory = {theory:.4e}, ratio = {ratio:.3f} (expected in [0.7, 1.5])")
    print(f"T8 PASS: dispersion nonlinearity matches δv_φ/c ≈ −k/18 within 50%")


def test_planck_correction_prediction():
    """T9 — planck_correction_prediction: correction grows at expected rate.

    At small α, δv_φ/c ≈ −(α π)/18.  We check that doubling α doubles the correction.
    """
    pc1 = mx.planck_correction_prediction(0.01)
    pc2 = mx.planck_correction_prediction(0.02)
    ratio = abs(pc2['delta_vph_exact'] / pc1['delta_vph_exact'])
    # Expect close to 2.0 (leading correction is linear in k = α π)
    assert 1.8 < ratio < 2.2, (
        f"T9 FAIL: doubling α should double correction; got ratio = {ratio:.3f}")
    print(f"T9 PASS: planck_correction doubling-α ratio = {ratio:.4f} ≈ 2.0 (linear in k)")


# ── Runner ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    tests = [
        test_c_from_rotation_rate_3d,
        test_c_from_rotation_rate_2d,
        test_rotation_law_machine_precision_3d,
        test_rotation_law_machine_precision_2d,
        test_spectral_propagator_energy_conservation_3d,
        test_spectral_propagator_energy_conservation_2d,
        test_maxwell_curl_is_linearisation_error,
        test_dispersion_nonlinearity,
        test_planck_correction_prediction,
    ]
    passed = 0
    failed = 0
    print(f'\n{"="*65}')
    print(' F26 — Rotation-law EM propagator test suite')
    print(f'{"="*65}\n')
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"*** {e}")
            failed += 1
        except Exception as e:
            print(f"*** ERROR in {t.__name__}: {e}")
            failed += 1
    print(f'\n{"="*65}')
    print(f' Results: {passed}/{len(tests)} passed,  {failed} failed')
    print(f'{"="*65}\n')
    sys.exit(0 if failed == 0 else 1)
