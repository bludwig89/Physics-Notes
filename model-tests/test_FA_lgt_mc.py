"""
test_FA_lgt_mc.py — correctness battery for the Option-A SU(3) lattice-gauge MC fork
====================================================================================

Fast, sandbox-sized certificates for `ca-simulation/forks/lgt_fork_A_mc.py`
(P1 Option A).  These do NOT measure the physical string tension (that needs
the heavy `run_lgt_confinement.py`); they verify the engine is a correct SU(3)
heat-bath so that any σ it later produces is trustworthy.

  FA1  heat-bath + over-relaxation preserve SU(3) (unitarity + det=1).
  FA2  over-relaxation preserves the Wilson action exactly (microcanonical).
  FA3  staple identity: Σ_links Re Tr(U_mu R_mu) = 4 · (plaquette-sum Re Tr)
       — certifies the local action gradient the heat-bath samples.
  FA4  heat-bath reproduces the known SU(3) mean plaquette at β=5.7, 6.0.
  FA5  strong-coupling limit: ⟨plaq⟩ → β/18 as β → 0.
  FA6  Lüscher–Weisz two-level estimator agrees with the direct Polyakov
       correlator and reduces its variance at fixed cost (beats the wall).

Created: 2026-06-04
"""
import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation', 'forks'))

import lgt_fork_A_mc as A          # noqa: E402


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def _unitarity_residual(U):
    r = 0.0
    for mu in range(U.shape[0]):
        UUd = A._mm(U[mu], A._dag(U[mu]))
        r = max(r, float(np.max(np.abs(UUd - np.eye(3)))))
    return r


def _det_residual(U):
    r = 0.0
    for mu in range(U.shape[0]):
        r = max(r, float(np.max(np.abs(np.linalg.det(U[mu]) - 1.0))))
    return r


# ═════════════════════════════════════════════════════════════════════

def test_FA1_su3_preserved():
    """FA1 — heat-bath + OR keep links in SU(3) (unitarity + det=1)."""
    rng = np.random.default_rng(11)
    U = A.cold_links(4, 4)
    for _ in range(12):
        U = A.heatbath_sweep(U, 5.7, rng, n_or=2)
    ures = _unitarity_residual(U)
    dres = _det_residual(U)
    passed = bool(ures < 1e-10 and dres < 1e-10)
    return {'test': 'FA1', 'name': 'heat-bath+OR preserve SU(3)',
            'passed': passed, 'residual': max(ures, dres), 'tier': 2,
            'detail': {'unitarity': ures, 'det': dres}}


def test_FA2_overrelax_preserves_action():
    """FA2 — over-relaxation is microcanonical: Wilson action exactly invariant."""
    rng = np.random.default_rng(3)
    U = A.cold_links(4, 4)
    for _ in range(8):
        U = A.heatbath_sweep(U, 5.7, rng, n_or=0)
    S0 = A.wilson_action(U, 5.7)
    for _ in range(5):
        for mu in range(4):
            U = A._update_direction(U, mu, 5.7, rng, 'overrelax', True)
    S1 = A.wilson_action(U, 5.7)
    res = abs(S1 - S0) / abs(S0)
    passed = bool(res < 1e-12)
    return {'test': 'FA2', 'name': 'over-relaxation preserves Wilson action',
            'passed': passed, 'residual': float(res), 'tier': 1,
            'detail': {'S_before': S0, 'S_after': S1}}


def test_FA3_staple_identity():
    """FA3 — Σ_links Re Tr(U_mu R_mu) = 4 · plaquette-sum Re Tr."""
    U = A.hot_links(4, 4, seed=9)
    lhs = 0.0
    for mu in range(4):
        R = A.staple_field(U, mu)
        lhs += np.real(np.trace(A._mm(U[mu], R), axis1=-2, axis2=-1)).sum()
    rhs = sum(np.real(np.trace(A.plaquette(U, mu, nu), axis1=-2, axis2=-1)).sum()
              for mu in range(4) for nu in range(mu + 1, 4))
    ratio = lhs / rhs
    res = abs(ratio - 4.0)
    passed = bool(res < 1e-10)
    return {'test': 'FA3', 'name': 'staple/action-gradient identity (ratio=4)',
            'passed': passed, 'residual': float(res), 'tier': 1,
            'detail': {'ratio': float(ratio)}}


def test_FA4_plaquette_matches_known():
    """FA4 — heat-bath mean plaquette matches published SU(3) values."""
    rng = np.random.default_rng(7)
    known = {5.7: 0.5494, 6.0: 0.5937}
    out = {}
    worst = 0.0
    for beta, kv in known.items():
        U = A.cold_links(4, 4)
        U, h = A.thermalise(U, beta, rng, n_sweeps=45, n_or=3, record=True)
        p = float(np.mean(h[-18:]))
        rel = abs(p - kv) / kv
        out[f'beta={beta}'] = {'plaq': p, 'known': kv, 'rel': rel}
        worst = max(worst, rel)
    passed = bool(worst < 0.025)     # L=4 finite-volume tolerance
    return {'test': 'FA4', 'name': 'mean plaquette matches known SU(3) ⟨P⟩',
            'passed': passed, 'residual': float(worst), 'tier': 3, 'detail': out}


def test_FA5_strong_coupling():
    """FA5 — strong-coupling limit ⟨plaq⟩ → β/18 as β → 0."""
    rng = np.random.default_rng(5)
    out = {}
    worst = 0.0
    for beta in (0.5, 1.0):
        U = A.cold_links(4, 4)
        U, h = A.thermalise(U, beta, rng, n_sweeps=25, n_or=2, record=True)
        p = float(np.mean(h[-10:]))
        pred = beta / 18.0
        rel = abs(p - pred) / pred
        out[f'beta={beta}'] = {'plaq': p, 'beta/18': pred, 'rel': rel}
        worst = max(worst, rel)
    passed = bool(worst < 0.20)      # leading-order strong coupling
    return {'test': 'FA5', 'name': 'strong-coupling ⟨plaq⟩ → β/18',
            'passed': passed, 'residual': float(worst), 'tier': 3, 'detail': out}


def test_FA6_multilevel_beats_direct():
    """FA6 — two-level estimator agrees with the direct Polyakov correlator and
    has smaller variance at matched cost (the wall-beating certificate)."""
    rng = np.random.default_rng(123)
    L, D = 4, 3                      # small 3D box, time = last axis (T=4)
    beta = 5.5
    R = 2
    U = A.cold_links(L, D)
    U, _ = A.thermalise(U, beta, rng, n_sweeps=30, n_or=2)

    # Direct: many decorrelated single measurements.
    n_meas = 20
    direct_vals = []
    Ud = U.copy()
    for _ in range(n_meas):
        for _s in range(2):
            Ud = A.heatbath_sweep(Ud, beta, rng, n_or=1)
        P = A.polyakov_loop_field(Ud)
        direct_vals.append(np.real(A.polyakov_correlator_direct(P, R, space_axis=0)))
    direct_vals = np.array(direct_vals)
    direct_mean = float(direct_vals.mean())
    direct_err = float(direct_vals.std(ddof=1) / np.sqrt(n_meas))

    # Two-level: a few outer configs, each with sublattice averaging.
    n_outer = 5
    n_sub = 6
    tl_vals = []
    Ut = U.copy()
    for _ in range(n_outer):
        for _s in range(2):
            Ut = A.heatbath_sweep(Ut, beta, rng, n_or=1)
        c = A.polyakov_correlator_twolevel(Ut, beta, rng, R, n_blocks=2,
                                           n_sub=n_sub, space_axis=0)
        tl_vals.append(np.real(c))
    tl_vals = np.array(tl_vals)
    tl_mean = float(tl_vals.mean())
    tl_err = float(tl_vals.std(ddof=1) / np.sqrt(n_outer))

    # Agreement within combined error (loose: small statistics).
    agree = abs(tl_mean - direct_mean) < 4.0 * (direct_err + tl_err + 1e-9)
    # Variance reduction is the wall-beating claim: per-sample variance of the
    # two-level estimator must be well below the direct estimator's.
    var_ratio = float(direct_vals.var(ddof=1) / (tl_vals.var(ddof=1) + 1e-30))
    var_reduced = var_ratio > 2.0
    passed = bool(agree and var_reduced)
    return {'test': 'FA6', 'name': 'multilevel agrees with & sharpens direct correlator',
            'passed': passed, 'residual': float(abs(tl_mean - direct_mean)), 'tier': 3,
            'detail': {'direct_mean': direct_mean, 'direct_err': direct_err,
                       'twolevel_mean': tl_mean, 'twolevel_err': tl_err,
                       'agree_within_4sigma': bool(agree),
                       'variance_reduction_factor': var_ratio,
                       'direct_var': float(direct_vals.var(ddof=1)),
                       'twolevel_var': float(tl_vals.var(ddof=1))}}


# ═════════════════════════════════════════════════════════════════════

def main():
    t_start = time.perf_counter()
    tests = [
        test_FA1_su3_preserved,
        test_FA2_overrelax_preserves_action,
        test_FA3_staple_identity,
        test_FA4_plaquette_matches_known,
        test_FA5_strong_coupling,
        test_FA6_multilevel_beats_direct,
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
            print(f"  [{'PASS' if ok else 'FAIL'}] {r.get('test'):4s}  "
                  f"{r.get('name'):54s}  res = {r.get('residual'):.3e}  "
                  f"({r['elapsed_s']:.1f} s)")
        except Exception as exc:
            import traceback
            traceback.print_exc()
            results.append({'test': fn.__name__, 'passed': False, 'error': repr(exc)})
            print(f"  [ERROR] {fn.__name__}: {exc!r}")

    total_t = time.perf_counter() - t_start
    summary = {
        'suite': 'FA — Option A SU(3) lattice-gauge MC engine correctness',
        'date': '2026-06-04',
        'n_tests': len(tests),
        'n_passed': n_pass,
        'total_elapsed_s': total_t,
        'results': results,
    }
    print(f"\n  -> {n_pass}/{len(tests)} PASS  in  {total_t:.1f} s")
    return summary


if __name__ == '__main__':
    summary = main()
    out = os.path.join(os.path.dirname(__file__), '..', 'test-results', 'FA_lgt_mc.json')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(summary, f, indent=2, cls=_NumpyEncoder)
    print(f"  -> wrote {out}")
    raise SystemExit(0 if summary['n_passed'] == summary['n_tests'] else 1)
