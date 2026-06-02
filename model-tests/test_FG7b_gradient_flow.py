"""
test_FG7b_gradient_flow.py — SU(3) Wilson gradient flow / cooling driver
========================================================================

Verifies the smoother delivered in `ca-simulation/ca_cooling.py`, which
closes the F43/FG-7 follow-up "real-time link evolution from a near-identity
start (gradient flow / cooling)".

The correctness contract for a Wilson flow:
  GF1  cold configuration is a fixed point          (force = 0 bit-for-bit)
  GF2  SU(3) unitarity preserved (flow + cooling)    (machine ε)
  GF3  Wilson action is monotonically non-increasing (flow RK3, Euler, cool)
  GF4  flow force ∈ su(3): anti-Hermitian + traceless (machine ε)
  GF5  flow is gauge-covariant: flow(U^g)=flow(U)^g  (machine ε)
  GF6  flow acts as the lattice Laplacian (diffusion): decay rate ∝ k̂²

Module under test:  ca-simulation/ca_cooling.py
Created:            2026-06-01
"""
import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import ca_cooling as cc        # noqa: E402
import ca_strong as cs         # noqa: E402


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


def _local_V_field(shape, rng):
    Vfield = np.zeros(shape + (3, 3), dtype=complex)
    flat = Vfield.reshape(-1, 3, 3)
    for n in range(flat.shape[0]):
        flat[n] = cs.su3_exp(rng.standard_normal(8))
    return Vfield


# ═════════════════════════════════════════════════════════════════════
#  GF1 — cold fixed point
# ═════════════════════════════════════════════════════════════════════

def test_GF1_cold_fixed_point():
    """GF1 — cold links: flow force is exactly zero; a step leaves U unchanged."""
    U = cs.cold_links_2d((10, 10))
    Z = cc.wilson_flow_force_2d(U)
    force_res = float(np.max(np.abs(Z)))
    U1 = cc.wilson_flow_step_rk3_2d(U, eps=0.1)
    step_res = float(np.max(np.abs(U1 - U)))
    Uc = cc.cooling_step_2d(U)
    cool_res = float(np.max(np.abs(Uc - U)))
    res = max(force_res, step_res, cool_res)
    return {'test': 'GF1', 'name': 'Cold configuration is a flow/cooling fixed point',
            'residual': res, 'target': 0.0,
            'force_res': force_res, 'flow_step_res': step_res, 'cool_res': cool_res,
            'passed': bool(res == 0.0),
            'description': 'staples = 2I → TA(2I)=0 bit-for-bit; cooling projects I→I'}


# ═════════════════════════════════════════════════════════════════════
#  GF2 — SU(3) unitarity preserved
# ═════════════════════════════════════════════════════════════════════

def test_GF2_unitarity_preserved():
    """GF2 — flow (RK3) and cooling keep every link in SU(3) over many steps."""
    U = cc.hot_links_2d((10, 10), seed=3)
    Uf, _ = cc.run_wilson_flow_2d(U, eps=0.05, n_steps=15, integrator='rk3', record=False)
    flow_res = cc.su3_unitarity_residual(Uf)
    flow_det = cc.su3_det_residual(Uf)
    Uc, _ = cc.run_cooling_2d(U, n_steps=15, record=False)
    cool_res = cc.su3_unitarity_residual(Uc)
    cool_det = cc.su3_det_residual(Uc)
    res = max(flow_res, flow_det, cool_res, cool_det)
    return {'test': 'GF2', 'name': 'SU(3) unitarity + det=1 preserved (flow & cooling)',
            'residual': res, 'target': 1e-12,
            'flow_unitarity': flow_res, 'flow_det': flow_det,
            'cool_unitarity': cool_res, 'cool_det': cool_det,
            'passed': bool(res < 1e-12),
            'description': 'exp of su(3) and SU(3)-projection stay in the group'}


# ═════════════════════════════════════════════════════════════════════
#  GF3 — monotonic action decrease
# ═════════════════════════════════════════════════════════════════════

def test_GF3_monotonic_action():
    """GF3 — Wilson action is non-increasing under flow (RK3, Euler) and cooling."""
    U = cc.hot_links_2d((12, 12), seed=5)

    def max_increase(hist):
        S = [h[1] for h in hist]
        return max((S[i + 1] - S[i] for i in range(len(S) - 1)), default=0.0)

    _, h_rk3 = cc.run_wilson_flow_2d(U, eps=0.04, n_steps=20, integrator='rk3')
    _, h_eul = cc.run_wilson_flow_2d(U, eps=0.01, n_steps=40, integrator='euler')
    _, h_cool = cc.run_cooling_2d(U, n_steps=20)

    inc = max(max_increase(h_rk3), max_increase(h_eul), max_increase(h_cool))
    # allow a tiny positive tolerance for round-off
    tol = 1e-9
    return {'test': 'GF3', 'name': 'Wilson action monotonically non-increasing',
            'residual': inc, 'target': tol,
            'S0': h_rk3[0][1], 'S_final_rk3': h_rk3[-1][1],
            'S_final_cool': h_cool[-1][1],
            'max_step_increase': inc,
            'passed': bool(inc < tol),
            'description': 'gradient descent on S_W: dS/dt = -Σ‖Z‖² ≤ 0'}


# ═════════════════════════════════════════════════════════════════════
#  GF4 — force lives in the su(3) Lie algebra
# ═════════════════════════════════════════════════════════════════════

def test_GF4_force_in_algebra():
    """GF4 — flow force Z is anti-Hermitian and traceless (∈ su(3))."""
    U = cc.hot_links_2d((10, 10), seed=7)
    Z = cc.wilson_flow_force_2d(U)
    anti = float(np.max(np.abs(Z + np.conj(np.swapaxes(Z, -1, -2)))))
    trace = float(np.max(np.abs(np.trace(Z, axis1=-2, axis2=-1))))
    res = max(anti, trace)
    return {'test': 'GF4', 'name': 'Flow force Z ∈ su(3) (anti-Hermitian, traceless)',
            'residual': res, 'target': 1e-13,
            'antiherm_res': anti, 'traceless_res': trace,
            'passed': bool(res < 1e-13),
            'description': 'TA projection yields a Lie-algebra-valued force'}


# ═════════════════════════════════════════════════════════════════════
#  GF5 — gauge covariance of the flow
# ═════════════════════════════════════════════════════════════════════

def test_GF5_gauge_covariance():
    """GF5 — flow commutes with gauge transformations: flow(U^g)=flow(U)^g."""
    rng = np.random.default_rng(9)
    shape = (8, 8)
    U = cc.hot_links_2d(shape, seed=9)
    Vfield = _local_V_field(shape, rng)

    # path 1: gauge-transform then flow
    Ug = cs.gauge_transform_links(U, Vfield)
    Ug_flow, _ = cc.run_wilson_flow_2d(Ug, eps=0.05, n_steps=8, integrator='rk3', record=False)
    # path 2: flow then gauge-transform
    U_flow, _ = cc.run_wilson_flow_2d(U, eps=0.05, n_steps=8, integrator='rk3', record=False)
    U_flow_g = cs.gauge_transform_links(U_flow, Vfield)

    res = float(np.max(np.abs(Ug_flow - U_flow_g)))
    return {'test': 'GF5', 'name': 'Flow is gauge-covariant: flow(U^g) = flow(U)^g',
            'residual': res, 'target': 1e-11,
            'passed': bool(res < 1e-11),
            'description': 'the central correctness certificate for the integrator'}


# ═════════════════════════════════════════════════════════════════════
#  GF6 — diffusive smoothing (decay rate ∝ lattice-Laplacian eigenvalue)
# ═════════════════════════════════════════════════════════════════════

def _abelian_transverse_links(L, n, amp):
    """U_y(x,y) = exp(i a_y T^3), a_y = amp·cos(k x); U_x = I.  Transverse mode."""
    k = 2.0 * np.pi * n / L
    x = np.arange(L)
    a_y = amp * np.cos(k * x)[:, None] * np.ones((1, L))   # (L,L), depends on x
    U = cs.cold_links_2d((L, L))
    T3 = cs.T_GEN[2]
    H = a_y[..., None, None] * T3                          # (L,L,3,3)
    U[1] = cc.su3_exp_algebra(1j * H)
    return U, k


def _extract_ay_amp(U, n, L):
    """Project a_y = 2·angle(U_y[...,0,0]) onto cos(k x); return amplitude."""
    k = 2.0 * np.pi * n / L
    a_y = 2.0 * np.angle(U[1][..., 0, 0])                  # (L,L)
    x = np.arange(L)
    proj = (2.0 / L) * np.einsum('xy,x->y', a_y, np.cos(k * x))
    return float(np.mean(proj))


def test_GF6_diffusive_smoothing():
    """GF6 — single Euler step decays each transverse mode at a rate ∝ k̂².

    The Wilson flow linearises to the lattice Laplacian, so the per-step
    relative decay δ(k) = eps·C·k̂² + O(amp²). We verify δ/k̂² is the same
    constant across several modes (to high precision at small amplitude),
    the signature of diffusion — high-k disorder is removed fastest.
    """
    L = 16
    eps = 1e-3
    amp = 1e-4
    ratios = []
    khat2_list = []
    for n in (1, 2, 3, 5):
        U, k = _abelian_transverse_links(L, n, amp)
        a0 = _extract_ay_amp(U, n, L)
        U1 = cc.wilson_flow_step_euler_2d(U, eps=eps)
        a1 = _extract_ay_amp(U1, n, L)
        delta = 1.0 - a1 / a0
        khat2 = 2.0 * (1.0 - np.cos(k))
        ratios.append(delta / khat2)
        khat2_list.append(khat2)
    ratios = np.array(ratios)
    spread = float(np.max(np.abs(ratios - np.mean(ratios))) / np.abs(np.mean(ratios)))
    # also confirm decay is positive (smoothing, not amplifying)
    positive = bool(np.all(ratios > 0))
    return {'test': 'GF6', 'name': 'Flow acts as lattice Laplacian (decay rate ∝ k̂²)',
            'residual': spread, 'target': 1e-3,
            'delta_over_khat2': ratios.tolist(),
            'mean_ratio': float(np.mean(ratios)),
            'all_decaying': positive,
            'passed': bool(spread < 1e-3 and positive),
            'description': 'diffusive smoothing: rate proportional to k̂² across modes'}


# ─────────────────────────────────────────────────────────────────────
# Main runner
# ─────────────────────────────────────────────────────────────────────

def main():
    t_start = time.perf_counter()
    tests = [
        test_GF1_cold_fixed_point,
        test_GF2_unitarity_preserved,
        test_GF3_monotonic_action,
        test_GF4_force_in_algebra,
        test_GF5_gauge_covariance,
        test_GF6_diffusive_smoothing,
    ]
    results = []
    n_pass = 0
    for fn in tests:
        t0 = time.perf_counter()
        try:
            r = fn()
            r['elapsed_s'] = time.perf_counter() - t0
            results.append(r)
            ok = bool(r.get('passed'))
            n_pass += int(ok)
            print(f"  [{'PASS' if ok else 'FAIL'}] {r.get('test'):5s}  "
                  f"{r.get('name'):58s}  res = {r.get('residual')}  "
                  f"({r['elapsed_s']:.3f} s)")
        except Exception as exc:
            import traceback
            traceback.print_exc()
            results.append({'test': fn.__name__, 'passed': False, 'error': repr(exc)})
            print(f"  [ERROR] {fn.__name__}: {exc!r}")

    total_t = time.perf_counter() - t_start
    summary = {
        'suite': 'FG-7b — SU(3) Wilson gradient flow / cooling driver',
        'date': '2026-06-01',
        'n_tests': len(tests),
        'n_passed': n_pass,
        'total_elapsed_s': total_t,
        'results': results,
    }
    print(f"\n  → {n_pass}/{len(tests)} PASS  in  {total_t:.2f} s")
    return summary


if __name__ == '__main__':
    summary = main()
    out = os.path.join(os.path.dirname(__file__),
                       '..', 'test-results', 'FG7b_gradient_flow.json')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(summary, f, indent=2, cls=_NumpyEncoder)
    print(f"  → wrote {out}")
    raise SystemExit(0 if summary['n_passed'] == summary['n_tests'] else 1)
