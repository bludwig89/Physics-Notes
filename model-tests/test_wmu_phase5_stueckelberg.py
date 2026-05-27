"""
test_wmu_phase5_stueckelberg.py — Phase 5B: Stueckelberg W Mass Generation
===========================================================================

Tests W5.1–W5.5 from roadmap-wmu-implementation.md (Path 5B).

  W5.1  Identity U_st → m_W = 0; random U_st → m_W > 0           structural
  W5.2  wmu_mass_stueckelberg preserves link unitarity              ≤ 1e-13
  W5.3  m_W invariant under constant SU(2) rotation of U_st        ≤ 1e-14
  W5.4  Gradient flow damps kinetic energy of U_st (heat kernel)    structural
  W5.5  mass_field has all 3 SU(2) components non-zero (long. d.o.f.)  structural
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import numpy as np
import json, time

from ca_wmu import (make_stueckelberg_field, stueckelberg_mass_term,
                    wmu_mass_stueckelberg, make_w_link_field,
                    link_unitarity_residual)

L = 8
rng = np.random.default_rng(seed=42)


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def _kinetic_energy(U_st_a, U_st_b):
    """
    Spectral kinetic energy: Σ_k (k²·|Û_a(k)|² + k²·|Û_b(k)|²).
    This is (1/2) tr[(∂_μ U_st†)(∂_μ U_st)] summed over all sites.
    """
    import numpy.fft as fft
    shape = U_st_a.shape
    L = shape[0]
    # Frequency grid (same convention as _kgrid3d in ca_wmu)
    kvals = 2 * np.pi * np.fft.fftfreq(L)
    KX, KY, KZ = np.meshgrid(kvals, kvals, kvals, indexing='ij')
    k2 = KX**2 + KY**2 + KZ**2

    Ua_k = fft.fftn(U_st_a)
    Ub_k = fft.fftn(U_st_b)
    return float(np.sum(k2 * (np.abs(Ua_k)**2 + np.abs(Ub_k)**2)))


# ──────────────────────────────────────────────────────────────────
# W5.1 — Identity → m_W = 0; random → m_W > 0
# ──────────────────────────────────────────────────────────────────
def test_W5_1_mass_formula_structural():
    """
    Structural test of the Stueckelberg mass formula.

    1. Identity U_st: all Fourier components at k≠0 are zero →
       kinetic energy = 0 → m_W_estimate = 0 exactly.

    2. Random U_st: spatially varying field → kinetic energy > 0 →
       m_W_estimate > 0.

    The Stueckelberg mass m_W = g·f where f = sqrt(mean kinetic energy)
    is a real positive number for any non-constant U_st.
    """
    # Identity
    U_a_id, U_b_id = make_stueckelberg_field(L, mode='identity')
    _, m_W_id = stueckelberg_mass_term(U_a_id, U_b_id, g_lat=1.0)

    # Random
    U_a_rand, U_b_rand = make_stueckelberg_field(L, mode='random', seed=7)
    _, m_W_rand = stueckelberg_mass_term(U_a_rand, U_b_rand, g_lat=1.0)

    res_id = float(abs(m_W_id))
    passed = bool(res_id <= 1e-13 and float(m_W_rand) > 1e-3)
    return {
        'test': 'W5.1',
        'residual': res_id,
        'target': 'identity→0, random>0',
        'm_W_identity': float(m_W_id),
        'm_W_random': float(m_W_rand),
        'passed': passed,
        'description': (f'Identity m_W={m_W_id:.2e}≈0; '
                        f'random m_W={m_W_rand:.4f}>0'),
    }


# ──────────────────────────────────────────────────────────────────
# W5.2 — wmu_mass_stueckelberg preserves link unitarity
# ──────────────────────────────────────────────────────────────────
def test_W5_2_mass_step_link_unitarity():
    """
    After applying wmu_mass_stueckelberg 10 times, all link variables
    remain exactly SU(2): |a|² + |b|² = 1.

    The mass step applies an SU(2) rotation R to each link via
    _su2_product(R, U), which preserves unitarity exactly (closed
    under matrix multiplication in the (a,b) representation).
    Target: residual ≤ 1e-13.
    """
    U_links = make_w_link_field(L, mode='random', seed=11)
    U_a_st, U_b_st = make_stueckelberg_field(L, mode='random', seed=22)

    for _ in range(10):
        U_links, U_a_st, U_b_st = wmu_mass_stueckelberg(
            U_links, U_a_st, U_b_st, dt=0.01, g_lat=1.0)

    res = link_unitarity_residual(U_links)
    passed = bool(res <= 1e-13)
    return {
        'test': 'W5.2',
        'residual': float(res),
        'target': 1e-13,
        'passed': passed,
        'description': f'Link unitarity after 10 mass steps: {res:.2e}',
    }


# ──────────────────────────────────────────────────────────────────
# W5.3 — m_W invariant under constant SU(2) rotation of U_st
# ──────────────────────────────────────────────────────────────────
def test_W5_3_mass_gauge_invariant():
    """
    The Stueckelberg kinetic term Σ_x |∂_μ U_st(x)|² =
        Σ_k k²(|Û_a|² + |Û_b|²) = (1/2) tr[(∂U_st†)(∂U_st)]

    is invariant under left-multiplication by a constant SU(2) matrix V:
        |∂(V·U_st)|² = |V·∂U_st|² = |∂U_st|²  (V constant, |V|=1).

    Therefore m_W_estimate is gauge-invariant under constant rotations.
    Target: |m_W_after - m_W_before| / m_W_before ≤ 1e-14.
    """
    U_a_st, U_b_st = make_stueckelberg_field(L, mode='random', seed=33)
    _, m_W_before = stueckelberg_mass_term(U_a_st, U_b_st, g_lat=1.0)

    # Apply constant V = exp(i·0.7·n·τ/2)
    theta = 0.7
    n = np.array([1, 2, 3]) / np.sqrt(14)
    V_a_val = np.cos(theta / 2) + 1j * np.sin(theta / 2) * n[2]
    V_b_val = np.sin(theta / 2) * (n[1] + 1j * n[0])

    # Left-multiply: new_U = V · old_U
    # SU(2) product (a1,b1)·(a2,b2) = (a1·a2 - conj(b1)·b2, b1·a2 + conj(a1)·b2)
    new_a = (V_a_val * U_a_st - np.conj(V_b_val) * U_b_st)
    new_b = (V_b_val * U_a_st + np.conj(V_a_val) * U_b_st)

    _, m_W_after = stueckelberg_mass_term(new_a, new_b, g_lat=1.0)

    res = float(abs(m_W_after - m_W_before) / (abs(m_W_before) + 1e-30))
    passed = bool(res <= 1e-14)
    return {
        'test': 'W5.3',
        'residual': res,
        'target': 1e-14,
        'm_W_before': float(m_W_before),
        'm_W_after': float(m_W_after),
        'passed': passed,
        'description': f'm_W gauge-invariant (const V): rel change {res:.2e}',
    }


# ──────────────────────────────────────────────────────────────────
# W5.4 — Gradient flow damps kinetic energy of U_st
# ──────────────────────────────────────────────────────────────────
def test_W5_4_gradient_flow_damps():
    """
    The wmu_mass_stueckelberg evolution step applies a heat-kernel gradient
    flow to U_st:
        Û_st_new(k) = exp(dt · (-(k_x² + k_y² + k_z²))) · Û_st(k).

    Since -(k²) ≤ 0 for all k, every Fourier mode is multiplied by a
    factor ≤ 1, so the total kinetic energy Σ_k k²|Û|² decreases
    monotonically with the number of flow steps (before re-unitarisation).

    After re-unitarisation the decrease may be partial, but the
    net kinetic energy after N steps should be ≤ initial kinetic energy.

    Target: E_kin_after ≤ E_kin_before (structural).
    """
    U_a_st, U_b_st = make_stueckelberg_field(L, mode='random', seed=44)
    U_links = make_w_link_field(L, mode='identity')

    E_kin_before = _kinetic_energy(U_a_st, U_b_st)

    Ua, Ub = U_a_st.copy(), U_b_st.copy()
    for _ in range(5):
        _, Ua, Ub = wmu_mass_stueckelberg(U_links, Ua, Ub, dt=0.1, g_lat=1.0)

    E_kin_after = _kinetic_energy(Ua, Ub)

    passed = bool(E_kin_after <= E_kin_before * (1.0 + 1e-10))
    return {
        'test': 'W5.4',
        'residual': float(E_kin_after / max(E_kin_before, 1e-30)),
        'target': '≤ 1.0 (decreasing)',
        'E_kin_before': float(E_kin_before),
        'E_kin_after': float(E_kin_after),
        'passed': passed,
        'description': (f'Gradient flow decreases E_kin: '
                        f'{E_kin_before:.3e} → {E_kin_after:.3e}'),
    }


# ──────────────────────────────────────────────────────────────────
# W5.5 — mass_field has all 3 SU(2) components (longitudinal d.o.f.)
# ──────────────────────────────────────────────────────────────────
def test_W5_5_longitudinal_dof():
    """
    In the massless theory only 2 transverse polarisations propagate.
    After Stueckelberg mass generation, all 3 W^a components (a=1,2,3)
    of the mass_field should be non-zero for a generic U_st configuration.

    This confirms the longitudinal d.o.f. is present in the mass field:
    mass_field^a is non-zero for a=1,2,3 independently.

    Also check: for identity U_st, mass_field = 0 exactly (no spurious mass).
    Target: structural (all 3 components > threshold for random U_st).
    """
    U_a_rand, U_b_rand = make_stueckelberg_field(L, mode='random', seed=55)
    mass_field, _ = stueckelberg_mass_term(U_a_rand, U_b_rand, g_lat=1.0)

    # All 3 components should be non-trivial
    comp_norms = [float(np.max(np.abs(mass_field[a]))) for a in range(3)]
    all_nonzero = all(c > 1e-6 for c in comp_norms)

    # Identity → zero mass
    U_a_id, U_b_id = make_stueckelberg_field(L, mode='identity')
    mass_id, _ = stueckelberg_mass_term(U_a_id, U_b_id, g_lat=1.0)
    identity_zero = float(np.max(np.abs(mass_id))) <= 1e-13

    passed = bool(all_nonzero and identity_zero)
    res = float(np.max(np.abs(mass_id)))
    return {
        'test': 'W5.5',
        'residual': res,
        'target': 'all 3 components > 1e-6; identity → 0',
        'component_norms': comp_norms,
        'identity_max': float(np.max(np.abs(mass_id))),
        'passed': passed,
        'description': (f'Long. d.o.f.: |F^1|={comp_norms[0]:.2e}, '
                        f'|F^2|={comp_norms[1]:.2e}, |F^3|={comp_norms[2]:.2e}; '
                        f'id→{res:.2e}'),
    }


# ──────────────────────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────────────────────
def run_all():
    tests = [
        test_W5_1_mass_formula_structural,
        test_W5_2_mass_step_link_unitarity,
        test_W5_3_mass_gauge_invariant,
        test_W5_4_gradient_flow_damps,
        test_W5_5_longitudinal_dof,
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
    out_path = os.path.join(out_dir, 'wmu_phase5_stueckelberg.json')
    with open(out_path, 'w') as fh:
        json.dump({'phase': '5B', 'results': results, 'elapsed': elapsed,
                   'n_pass': int(n_pass), 'n_total': len(results)},
                  fh, indent=2, cls=_NumpyEncoder)
    print(f"  Results saved → {out_path}")
    return results


if __name__ == '__main__':
    print("Phase 5B — Stueckelberg W Mass Generation")
    print("=" * 50)
    run_all()
