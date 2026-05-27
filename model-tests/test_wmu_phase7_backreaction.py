"""
test_wmu_phase7_backreaction.py
================================
Phase 7 tests — Yang-Mills back-reaction and massive W (Proca) dispersion.

Tests
-----
WB.1  fermion_isospin_current — pure ν state: J^3 = +|f|²/2, J^1=J^2=0
WB.2  fermion_isospin_current — equal mix (ν+e)/√2: J^1 = |f|²/2, J^2=J^3=0
WB.3  back-reaction diagonal — J^3 source drives only W^3, leaves W^1,W^2 zero
WB.4  massive W dispersion  — ω²(k) = m_W² + Ω_even²(k), multiple masses
WB.5  massless limit        — w_massive(..., m_W=0, dt=1) == w_propagation_step_spectral

2026-05-24
"""

import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

from ca_wmu import (
    fermion_isospin_current,
    w_sourced_propagation_step,
    w_massive_propagation_step_spectral,
    measure_massive_w_dispersion,
    w_propagation_step_spectral,
)

# ---------------------------------------------------------------------------
# JSON encoder for numpy types
# ---------------------------------------------------------------------------
class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ---------------------------------------------------------------------------
# WB.1 — fermion_isospin_current: pure ν state
# ---------------------------------------------------------------------------
def test_WB1_current_pure_nu():
    """
    Pure neutrino state: f_ν = ψ, f_e = 0.
    Expected:
      J^3 = |ψ|²/2  (positive, max component)
      J^1 = 0       (no off-diagonal coherence)
      J^2 = 0
    """
    rng = np.random.default_rng(1)
    L = 8
    f_nu = rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L))
    f_e  = np.zeros((L, L, L), dtype=complex)

    J = fermion_isospin_current(f_nu, f_e)   # shape (3, L, L, L)

    J1_max = float(np.max(np.abs(J[0])))
    J2_max = float(np.max(np.abs(J[1])))
    J3_ref = 0.5 * np.abs(f_nu)**2
    J3_err = float(np.max(np.abs(J[2] - J3_ref)))

    passed = (J1_max < 1e-14) and (J2_max < 1e-14) and (J3_err < 1e-14)
    return {
        'test': 'WB.1',
        'name': 'fermion_isospin_current pure-nu',
        'J1_max': J1_max,
        'J2_max': J2_max,
        'J3_err': J3_err,
        'threshold': 1e-14,
        'passed': passed,
    }


# ---------------------------------------------------------------------------
# WB.2 — fermion_isospin_current: equal mix (ν+e)/√2
# ---------------------------------------------------------------------------
def test_WB2_current_equal_mix():
    """
    Equal-weight superposition: f_ν = ψ/√2, f_e = ψ/√2 (same phase).
    Expected:
      J^1 = Re(f_ν* f_e) = |ψ|²/2   (real positive)
      J^2 = Im(f_ν* f_e) = 0         (same phase → zero imaginary part)
      J^3 = 0                         (equal populations cancel)
    """
    rng = np.random.default_rng(2)
    L = 8
    psi = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    f_nu = psi / np.sqrt(2)
    f_e  = psi / np.sqrt(2)

    J = fermion_isospin_current(f_nu, f_e)

    J1_ref = 0.5 * np.abs(psi)**2
    J1_err = float(np.max(np.abs(J[0] - J1_ref)))
    J2_max = float(np.max(np.abs(J[1])))
    J3_max = float(np.max(np.abs(J[2])))

    passed = (J1_err < 1e-14) and (J2_max < 1e-14) and (J3_max < 1e-14)
    return {
        'test': 'WB.2',
        'name': 'fermion_isospin_current equal-mix',
        'J1_err': J1_err,
        'J2_max': J2_max,
        'J3_max': J3_max,
        'threshold': 1e-14,
        'passed': passed,
    }


# ---------------------------------------------------------------------------
# WB.3 — Back-reaction diagonal: J^3 drives W^3 only
# ---------------------------------------------------------------------------
def test_WB3_backreaction_diagonal():
    """
    Back-reaction diagonal coupling — two sub-tests:

    (A) Single-step exact increment:
        Start from zero W fields, apply 1 sourced step with pure J^3 source.
        Because the free rotation of a zero field is zero, the only change
        is the source kick: E_W[2] += g * J^3 * dt exactly.
        Residual = max |E_W[2] - g * J^3 * dt|  should be ≤ 1e-14.

    (B) Multi-step diagonal isolation:
        Run n_steps with constant J^3 source.  Since J^1 = J^2 = 0, the
        source can never feed W^1 or W^2 regardless of how E↔B rotate.
        Checks W^1 = W^2 = 0 exactly after all steps.

    Note: E_W[2] after n>1 steps is NOT n*g*J^3*dt because each step's
    free rotation mixes E↔B of the previously kicked W^3 field.  We only
    test the exact increment for the first step, and only test diagonal
    isolation for subsequent steps.
    """
    rng = np.random.default_rng(3)
    L = 8
    f_nu = rng.standard_normal((L, L, L)).astype(complex)
    f_e  = np.zeros((L, L, L), dtype=complex)

    J = fermion_isospin_current(f_nu, f_e)  # J[2] = |f_nu|²/2, J[0]=J[1]=0

    g_lat = 0.5
    dt    = 1.0

    # --- Sub-test A: single step from zero ---
    E_W = np.zeros((3, L, L, L))
    B_W = np.zeros((3, L, L, L))
    E_W1, B_W1 = w_sourced_propagation_step(E_W, B_W, J, dt=dt, g_lat=g_lat)
    W3_expected_1 = J[2] * g_lat * dt   # free rotation of 0 = 0; only kick
    W3_err_1 = float(np.max(np.abs(E_W1[2] - W3_expected_1)))

    # --- Sub-test B: multi-step diagonal isolation ---
    E_W = np.zeros((3, L, L, L))
    B_W = np.zeros((3, L, L, L))
    n_steps = 10
    for _ in range(n_steps):
        E_W, B_W = w_sourced_propagation_step(E_W, B_W, J, dt=dt, g_lat=g_lat)

    W1_max = float(np.max(np.abs(E_W[0])))
    W2_max = float(np.max(np.abs(E_W[1])))
    # W^3 should be non-zero (source drove it)
    W3_nonzero = float(np.max(np.abs(E_W[2]))) > 0.0

    passed = (W3_err_1 < 1e-14) and (W1_max < 1e-14) and (W2_max < 1e-14) and W3_nonzero
    return {
        'test': 'WB.3',
        'name': 'back-reaction diagonal (J^3 drives W^3 only)',
        'single_step_W3_err': W3_err_1,
        'multi_step_W1_max': W1_max,
        'multi_step_W2_max': W2_max,
        'W3_nonzero': W3_nonzero,
        'threshold': 1e-14,
        'passed': passed,
    }


# ---------------------------------------------------------------------------
# WB.4 — Massive W dispersion: ω²(k) = m_W² + Ω_even²(k)
# ---------------------------------------------------------------------------
def test_WB4_massive_dispersion():
    """
    Check the Proca dispersion for three W masses:
        m_W ∈ {0.1, 0.3, 0.8}

    For each mass, measure_massive_w_dispersion evolves a random field
    n_steps=100 steps and compares C_n against C_0 exp(-i ω_eff n_steps).
    Tolerance: max relative error ≤ 1e-10.
    """
    results = {}
    masses = [0.1, 0.3, 0.8]
    tol = 1e-10
    all_passed = True

    for mW in masses:
        err = measure_massive_w_dispersion(L=16, m_W=mW, n_steps=100,
                                           a_comp=0, seed=7)
        ok = err < tol
        results[f'm_W={mW}'] = {'max_rel_err': err, 'passed': ok}
        if not ok:
            all_passed = False

    return {
        'test': 'WB.4',
        'name': 'massive W dispersion (Proca) for multiple masses',
        'mass_results': results,
        'tolerance': tol,
        'passed': all_passed,
    }


# ---------------------------------------------------------------------------
# WB.5 — Massless limit: massive step → free step at m_W=0
# ---------------------------------------------------------------------------
def test_WB5_massless_limit():
    """
    At m_W=0, dt=1, w_massive_propagation_step_spectral must produce
    identically the same result as w_propagation_step_spectral.

    Residual = max |E_massive − E_free| + max |B_massive − B_free|
    Expected: residual ≤ machine precision (~1e-14)
    """
    rng = np.random.default_rng(99)
    L = 12
    E_W = rng.standard_normal((3, L, L, L))
    B_W = rng.standard_normal((3, L, L, L))

    E_free, B_free = w_propagation_step_spectral(E_W, B_W)
    E_mass, B_mass = w_massive_propagation_step_spectral(E_W, B_W, m_W=0.0, dt=1.0)

    E_err = float(np.max(np.abs(E_mass - E_free)))
    B_err = float(np.max(np.abs(B_mass - B_free)))

    tol = 1e-12
    passed = (E_err < tol) and (B_err < tol)
    return {
        'test': 'WB.5',
        'name': 'massless limit: massive step → free step (m_W=0)',
        'E_err': E_err,
        'B_err': B_err,
        'threshold': tol,
        'passed': passed,
    }


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("=" * 62)
    print("Phase 7 — Back-reaction and Massive W Dispersion")
    print("=" * 62)

    runners = [
        test_WB1_current_pure_nu,
        test_WB2_current_equal_mix,
        test_WB3_backreaction_diagonal,
        test_WB4_massive_dispersion,
        test_WB5_massless_limit,
    ]

    all_results = []
    n_pass = 0
    t0 = time.time()

    for fn in runners:
        r = fn()
        all_results.append(r)
        status = "PASS" if r['passed'] else "FAIL"
        if r['passed']:
            n_pass += 1
        print(f"  [{status}] {r['test']} — {r['name']}")

    elapsed = time.time() - t0
    print("-" * 62)
    print(f"  {n_pass}/{len(runners)} tests passed  ({elapsed:.2f}s)")
    print("=" * 62)

    # Save JSON results
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'phase7_backreaction_results.json')
    with open(out_path, 'w') as fh:
        json.dump({
            'suite': 'Phase 7 — Back-reaction and Massive W',
            'n_pass': n_pass,
            'n_total': len(runners),
            'elapsed_s': elapsed,
            'results': all_results,
        }, fh, indent=2, cls=_NumpyEncoder)
    print(f"\n  Results saved → {out_path}")
