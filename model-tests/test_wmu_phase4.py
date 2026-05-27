"""
test_wmu_phase4.py — Phase 4: Fermion–W_μ Vertex (Covariant Derivative)
=========================================================================

Tests W4.1–W4.5 from roadmap-wmu-implementation.md.

  W4.1  Full kinetic + mass + W step locally SU(2)_L-invariant (const V)  ≤ 1e-14
  W4.2  Fermion isospin charge Q^a = ∫ J^{a,0} conserved when g=0         ≤ 1e-13
  W4.3  Right-handed χ does not couple to W_μ (parity violation)          = 0 (exact)
  W4.4  W± vertex mixes isospin: ν_L state gains e_L population           structural
  W4.5  Total norm conserved over 100 Strang-split steps, random U_links   ≤ 1e-12
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import numpy as np
import json
import time


class _NumpyEncoder(json.JSONEncoder):
    """Handle numpy scalars / bools that the default encoder rejects."""
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

from ca_wmu import (
    make_w_link_field, covariant_dirac_doublet_step,
    fermion_current_isospin, gauge_transform_links, _su2_product
)

L = 12
rng = np.random.default_rng(seed=42)


# ──────────────────────────────────────────────────────────────────
# Helper: random normalised full Dirac doublet (η, χ) with 4 flavours
# ──────────────────────────────────────────────────────────────────
def _random_dirac_doublet(shape, rng):
    """Random normalised Dirac doublet: 4 spin-isospin × 2 chirality = 8 fields."""
    fields = [rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
              for _ in range(8)]
    total_norm = np.sqrt(sum(np.sum(np.abs(f)**2) for f in fields))
    fields = [f / total_norm for f in fields]
    return tuple(fields)  # (f_nu, f_e, g_nu, g_e, chi_nu_f, chi_e_f, chi_nu_g, chi_e_g)


def _dirac_norm(*fields):
    return float(sum(np.sum(np.abs(f)**2) for f in fields))


def _random_su2_field(shape, rng):
    """Haar-measure SU(2) field."""
    raw = rng.standard_normal(shape + (4,))
    norms = np.linalg.norm(raw, axis=-1, keepdims=True)
    q = raw / norms
    return q[..., 0] + 1j * q[..., 3], q[..., 2] + 1j * q[..., 1]


def _apply_V_left(f_nu, f_e, g_nu, g_e, V_a, V_b):
    """Apply V ∈ SU(2) to the isospin (left-handed η) sector."""
    f_nu_new = V_a * f_nu - np.conj(V_b) * f_e
    f_e_new  = V_b * f_nu + np.conj(V_a) * f_e
    g_nu_new = V_a * g_nu - np.conj(V_b) * g_e
    g_e_new  = V_b * g_nu + np.conj(V_a) * g_e
    return f_nu_new, f_e_new, g_nu_new, g_e_new


# ──────────────────────────────────────────────────────────────────
# W4.1 — Full step SU(2)_L Ward identity (constant V)
# ──────────────────────────────────────────────────────────────────
def test_W4_1_su2_ward_full_step():
    """
    Constant-V Ward identity for the full Strang-split step:
        V · covariant_dirac_step(ψ; U_kin, U_m) =
            covariant_dirac_step(V·ψ; V·U_kin·V†, V·U_m)

    V acts on the isospin (left-handed η) sector only.
    χ (right-handed) is unchanged by V — parity-violation structure (W4.3).

    With constant V the covariant-hopping Ward identity is exact (as verified
    in W1.5), so the full step Ward identity also holds to machine precision.
    """
    shape = (L, L, L)
    (f_nu, f_e, g_nu, g_e,
     chi_nu_f, chi_e_f, chi_nu_g, chi_e_g) = _random_dirac_doublet(shape, rng)

    U_links = make_w_link_field(L, mode='random', seed=11)
    U_a_mass, U_b_mass = _random_su2_field(shape, rng)

    # Constant V (same at every site)
    theta, n = 0.6, np.array([1, 0, 0], dtype=float)
    V_a = (np.cos(theta / 2) + 1j * np.sin(theta / 2) * n[2]) * np.ones(shape, dtype=complex)
    V_b = np.sin(theta / 2) * (n[1] + 1j * n[0]) * np.ones(shape, dtype=complex)

    m, dt = 0.15, 1.0

    # LHS: step then V
    out = covariant_dirac_doublet_step(
        f_nu, f_e, g_nu, g_e,
        chi_nu_f, chi_e_f, chi_nu_g, chi_e_g,
        U_links, U_a_mass, U_b_mass, m, dt)
    sf_nu, sf_e, sg_nu, sg_e = out[:4]
    schi = out[4:]
    Vsf_nu, Vsf_e, Vsg_nu, Vsg_e = _apply_V_left(sf_nu, sf_e, sg_nu, sg_e, V_a, V_b)

    # RHS: transform then step
    Vf_nu, Vf_e, Vg_nu, Vg_e = _apply_V_left(f_nu, f_e, g_nu, g_e, V_a, V_b)
    VU_links = gauge_transform_links(U_links, V_a, V_b)
    VUm_a, VUm_b = _su2_product(V_a, V_b, U_a_mass, U_b_mass)

    out2 = covariant_dirac_doublet_step(
        Vf_nu, Vf_e, Vg_nu, Vg_e,
        chi_nu_f, chi_e_f, chi_nu_g, chi_e_g,
        VU_links, VUm_a, VUm_b, m, dt)
    sVf_nu, sVf_e, sVg_nu, sVg_e = out2[:4]

    res = max(
        np.max(np.abs(Vsf_nu - sVf_nu)),
        np.max(np.abs(Vsf_e  - sVf_e)),
        np.max(np.abs(Vsg_nu - sVg_nu)),
        np.max(np.abs(Vsg_e  - sVg_e)),
    )
    passed = res <= 1e-14
    return {
        'test': 'W4.1',
        'residual': float(res),
        'target': 1e-14,
        'passed': passed,
        'description': f'SU(2)_L Ward identity: full step (const V): {res:.2e}',
    }


# ──────────────────────────────────────────────────────────────────
# W4.2 — Fermion isospin charge conserved when g=0
# ──────────────────────────────────────────────────────────────────
def test_W4_2_current_conservation():
    """
    For a free doublet (U_links = identity, no W coupling), the isospin
    charges Q^a = Σ_x (η†(x) τ^a η(x)) are conserved.

    Since the free BCC step is block-diagonal in isospin (it only acts on
    the spin-1/2 indices), global isospin charges Q^a are exactly conserved:

        Q^a_before = Q^a_after   (residual ≤ FFT round-off)

    We check max_a |Q^a_after − Q^a_before| / |Q^a_before| + 1 ≤ 1e-13.
    """
    shape = (L, L, L)
    (f_nu, f_e, g_nu, g_e,
     chi_nu_f, chi_e_f, chi_nu_g, chi_e_g) = _random_dirac_doublet(shape, rng)

    # Identity links = free evolution
    U_links = make_w_link_field(L, mode='identity')
    U_a_mass = np.ones(shape, dtype=complex)
    U_b_mass = np.zeros(shape, dtype=complex)

    def _isospin_charges(fn, fe, gn, ge):
        """Q^a = Σ_x (fn†τ^a fn + fn†τ^a fn  [spin components summed])"""
        # τ^1: Q1 = 2·Re(Σ fn*·fe + gn*·ge)
        # τ^2: Q2 = 2·Im(Σ fn*·fe + gn*·ge) (note sign)
        # τ^3: Q3 = Σ(|fn|²-|fe|²+|gn|²-|ge|²)
        Q1 = 2.0 * float(np.sum(np.real(np.conj(fn) * fe + np.conj(gn) * ge)))
        Q2 = 2.0 * float(np.sum(np.imag(np.conj(fn) * fe + np.conj(gn) * ge)))
        Q3 = float(np.sum(np.abs(fn)**2 - np.abs(fe)**2 + np.abs(gn)**2 - np.abs(ge)**2))
        return np.array([Q1, Q2, Q3])

    Q0 = _isospin_charges(f_nu, f_e, g_nu, g_e)

    out = covariant_dirac_doublet_step(
        f_nu, f_e, g_nu, g_e,
        chi_nu_f, chi_e_f, chi_nu_g, chi_e_g,
        U_links, U_a_mass, U_b_mass, m=0.0, dt=1.0)
    fn_new, fe_new, gn_new, ge_new = out[:4]

    Q1 = _isospin_charges(fn_new, fe_new, gn_new, ge_new)
    scale = np.abs(Q0) + 1.0
    res = float(np.max(np.abs(Q1 - Q0) / scale))
    passed = res <= 1e-13
    return {
        'test': 'W4.2',
        'residual': float(res),
        'target': 1e-13,
        'Q_before': Q0.tolist(),
        'Q_after': Q1.tolist(),
        'passed': passed,
        'description': f'Isospin charges conserved (g=0, identity links): {res:.2e}',
    }


# ──────────────────────────────────────────────────────────────────
# W4.3 — Right-handed χ does not couple to W_μ (exact)
# ──────────────────────────────────────────────────────────────────
def test_W4_3_rh_no_coupling():
    """
    SU(2)_L is chiral: χ (right-handed) is a singlet and does NOT couple
    to W_μ.  The covariant_dirac_doublet_step always uses identity links for
    the χ kinetic step regardless of what U_links is passed.

    Test with m=0 (massless): with sin(m·dt)=0 the mass coupling vanishes,
    so the full step reduces to two half-kinetic steps.  The χ kinetic step
    uses identity links internally, so χ output is bitwise identical whether
    we pass random or identity U_links to the outer call.  Residual = 0 exactly.

    (With m≠0 the Dirac mass term mixes η into χ and vice versa.  Since η
    depends on U_links, χ would be indirectly affected — correct physics,
    not a bug.  We isolate the kinetic-only property with m=0.)
    """
    shape = (L, L, L)
    (f_nu, f_e, g_nu, g_e,
     chi_nu_f, chi_e_f, chi_nu_g, chi_e_g) = _random_dirac_doublet(shape, rng)

    U_links_random = make_w_link_field(L, mode='random', seed=7)
    U_links_id     = make_w_link_field(L, mode='identity')
    U_a_mass = np.ones(shape, dtype=complex)
    U_b_mass = np.zeros(shape, dtype=complex)

    # m=0: sin(m·dt)=0, mass coupling vanishes → pure kinetic test
    out_rand = covariant_dirac_doublet_step(
        f_nu, f_e, g_nu, g_e,
        chi_nu_f, chi_e_f, chi_nu_g, chi_e_g,
        U_links_random, U_a_mass, U_b_mass, m=0.0, dt=1.0)
    out_id = covariant_dirac_doublet_step(
        f_nu, f_e, g_nu, g_e,
        chi_nu_f, chi_e_f, chi_nu_g, chi_e_g,
        U_links_id, U_a_mass, U_b_mass, m=0.0, dt=1.0)

    # χ components are indices 4–7
    chi_rand = out_rand[4:]
    chi_id   = out_id[4:]

    res = float(max(np.max(np.abs(c1 - c2))
                    for c1, c2 in zip(chi_rand, chi_id)))
    passed = res == 0.0
    return {
        'test': 'W4.3',
        'residual': float(res),
        'target': 0.0,
        'passed': passed,
        'description': f'χ decoupled from W_μ (parity): max|Δχ| = {res:.2e}',
    }


# ──────────────────────────────────────────────────────────────────
# W4.4 — W± vertex mixes isospin: ν_L + W → e_L
# ──────────────────────────────────────────────────────────────────
def test_W4_4_isospin_mixing():
    """
    A W± gauge configuration couples ν_L and e_L.

    Start with a pure ν_L state (f_nu=normalised, all others=0).
    Apply the W-coupled step with a W+ link field (U close to iτ¹/2)
    which is the W1=1 direction.

    After the step the e_L population should be non-zero, confirming
    the vertex ν_L + W- → e_L is active.  This is a structural test.
    """
    shape = (L, L, L)
    f_nu = np.ones(shape, dtype=complex) / L**1.5   # uniform ν_L state
    f_e   = np.zeros(shape, dtype=complex)
    g_nu  = np.zeros(shape, dtype=complex)
    g_e   = np.zeros(shape, dtype=complex)
    chi_nu_f = np.zeros(shape, dtype=complex)
    chi_e_f  = np.zeros(shape, dtype=complex)
    chi_nu_g = np.zeros(shape, dtype=complex)
    chi_e_g  = np.zeros(shape, dtype=complex)

    # W+ field: links close to iτ¹ direction (off-diagonal SU(2))
    # U = cos(θ/2)I + i·sin(θ/2)τ¹ → a = cos(θ/2), b = sin(θ/2)
    theta_w = 0.8  # mixing angle
    U_a = np.cos(theta_w / 2) * np.ones(shape, dtype=complex)
    U_b = np.sin(theta_w / 2) * np.ones(shape, dtype=complex)
    U_links_w = [(U_a, U_b)] * 8  # same for all 8 links

    U_a_mass = np.ones(shape, dtype=complex)
    U_b_mass = np.zeros(shape, dtype=complex)

    nu_norm_before = float(np.sum(np.abs(f_nu)**2))
    e_norm_before  = 0.0

    out = covariant_dirac_doublet_step(
        f_nu, f_e, g_nu, g_e,
        chi_nu_f, chi_e_f, chi_nu_g, chi_e_g,
        U_links_w, U_a_mass, U_b_mass, m=0.2, dt=1.0)
    fn_out, fe_out = out[0], out[1]

    nu_norm_after = float(np.sum(np.abs(fn_out)**2))
    e_norm_after  = float(np.sum(np.abs(fe_out)**2))

    # e_L should acquire population due to W coupling
    e_gain = e_norm_after - e_norm_before
    passed = bool(e_norm_after > 1e-6 and nu_norm_after < nu_norm_before * 0.9999)
    return {
        'test': 'W4.4',
        'residual': float(e_norm_after),   # non-zero = W vertex active
        'target': 'e_L population > 0',
        'nu_before': float(nu_norm_before),
        'e_after': float(e_norm_after),
        'passed': passed,
        'description': (f'W± vertex: e_L population = {e_norm_after:.4f} '
                        f'(structural; ≥ 1e-6 means vertex active)'),
    }


# ──────────────────────────────────────────────────────────────────
# W4.5 — Total norm conserved over 100 steps
# ──────────────────────────────────────────────────────────────────
def test_W4_5_norm_conservation():
    """
    The full Strang-split covariant_dirac_doublet_step is unitary:
    the total norm of all 8 spinor fields is conserved over 100 steps.

    Each sub-step (covariant kinetic, complex-mass) is individually unitary.
    The Strang split of two unitary operators is unitary.

    Target: max drift ≤ 1e-12 over 100 steps.
    """
    shape = (L, L, L)
    (f_nu, f_e, g_nu, g_e,
     chi_nu_f, chi_e_f, chi_nu_g, chi_e_g) = _random_dirac_doublet(shape, rng)

    U_links  = make_w_link_field(L, mode='random', seed=9)
    U_a_mass, U_b_mass = _random_su2_field(shape, rng)
    m, dt = 0.2, 1.0

    norm0 = _dirac_norm(f_nu, f_e, g_nu, g_e, chi_nu_f, chi_e_f, chi_nu_g, chi_e_g)
    max_drift = 0.0
    fields = (f_nu, f_e, g_nu, g_e, chi_nu_f, chi_e_f, chi_nu_g, chi_e_g)

    for _ in range(100):
        fields = covariant_dirac_doublet_step(
            *fields, U_links, U_a_mass, U_b_mass, m, dt)
        norm = _dirac_norm(*fields)
        drift = abs(norm - norm0)
        if drift > max_drift:
            max_drift = drift

    passed = max_drift <= 1e-12
    return {
        'test': 'W4.5',
        'residual': float(max_drift),
        'target': 1e-12,
        'passed': passed,
        'description': f'Norm conserved over 100 full steps: drift = {max_drift:.2e}',
    }


# ──────────────────────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────────────────────
def run_all():
    tests = [
        test_W4_1_su2_ward_full_step,
        test_W4_2_current_conservation,
        test_W4_3_rh_no_coupling,
        test_W4_4_isospin_mixing,
        test_W4_5_norm_conservation,
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
    out_path = os.path.join(out_dir, 'wmu_phase4.json')
    with open(out_path, 'w') as fh:
        json.dump({'phase': 4, 'results': results, 'elapsed': elapsed,
                   'n_pass': int(n_pass), 'n_total': len(results)},
                  fh, indent=2, cls=_NumpyEncoder)
    print(f"  Results saved → {out_path}")
    return results


if __name__ == '__main__':
    print("Phase 4 — Fermion–W_μ Vertex (Covariant Derivative)")
    print("=" * 58)
    run_all()
