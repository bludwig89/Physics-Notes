"""
test_FG7c_confinement.py — static quark potential, string tension, confinement
==============================================================================

Verifies `ca-simulation/ca_confinement.py`: the 2D SU(3) lattice gauge sector
produces a *linear* static quark potential, i.e. an isolated colour charge
costs infinite energy — the model-level statement of *why a quark cannot exist
alone*.

  CF1  w(β) limits: w(0)=0, monotone increasing, 0<w<1, w→1 large β
  CF2  w(β) Weyl-torus quadrature converges to machine precision
  CF3  string tension σ(β) = −ln w(β) > 0 for every finite β  (confinement
       at all couplings, exact)
  CF4  Creutz ratio χ(R,T) = σ exactly, independent of (R,T)  (area law)
  CF5  static potential V(R) = σ·R exactly linear (loop estimator T-independent)
  CF6  Metropolis lattice mean plaquette matches the quadrature w(β)
  CF7  gradient flow raises ⟨plaquette⟩ → lowers measured σ (smoothing the
       disorder dissolves confinement — ties to ca_cooling)
  CF8  Schur lemma ⟨U⟩ = w·I (the engine of the exact area-law factorisation)

Modules under test:  ca-simulation/ca_confinement.py  (+ ca_cooling.py)
Created:             2026-06-01
"""
import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import ca_confinement as cf    # noqa: E402
import ca_cooling as cc        # noqa: E402
import ca_strong as cs         # noqa: E402


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


# ═════════════════════════════════════════════════════════════════════

def test_CF1_w_limits():
    """CF1 — w(0)=0; w monotone increasing in β; 0<w<1; w→1 at large β."""
    w0 = cf.plaquette_mean(0.0)
    betas = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    ws = [cf.plaquette_mean(b) for b in betas]
    monotone = all(ws[i] < ws[i + 1] for i in range(len(ws) - 1))
    bounded = all(0.0 < w < 1.0 for w in ws)
    big = cf.plaquette_mean(40.0)
    res = abs(w0)
    ok = (res < 1e-12) and monotone and bounded and (big > 0.85)
    return {'test': 'CF1', 'name': 'w(β) limits and monotonicity',
            'residual': res, 'target': 1e-12,
            'w0': w0, 'w_table': dict(zip(betas, ws)), 'w_40': big,
            'monotone': monotone, 'bounded': bounded,
            'passed': bool(ok),
            'description': 'w(0)=⟨Tr U⟩_Haar=0; w↑ to 1 as β→∞'}


def test_CF2_quadrature_convergence():
    """CF2 — Weyl-torus quadrature for w(β) is grid-converged (machine ε)."""
    worst = 0.0
    for b in (0.5, 2.0, 6.0):
        w_lo = cf.plaquette_mean(b, n_grid=160)
        w_hi = cf.plaquette_mean(b, n_grid=320)
        worst = max(worst, abs(w_lo - w_hi))
    return {'test': 'CF2', 'name': 'w(β) quadrature converges (n_grid 160→320)',
            'residual': worst, 'target': 1e-12,
            'passed': bool(worst < 1e-12),
            'description': 'periodic rectangle rule is spectrally accurate'}


def test_CF3_string_tension_positive():
    """CF3 — σ(β) = −ln w(β) > 0 for every finite β; σ decreasing in β."""
    betas = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 20.0]
    sig = [cf.string_tension(b) for b in betas]
    positive = all(s > 0 for s in sig)
    decreasing = all(sig[i] > sig[i + 1] for i in range(len(sig) - 1))
    return {'test': 'CF3', 'name': 'String tension σ(β)>0 for all finite β',
            'residual': float(min(sig)), 'target': 0.0,
            'sigma_table': dict(zip(betas, sig)),
            'positive': positive, 'decreasing': decreasing,
            'passed': bool(positive and decreasing),
            'description': '2D SU(3) confines at all couplings — no free quark'}


def test_CF4_creutz_ratio_exact():
    """CF4 — Creutz ratio χ(R,T) = σ exactly, independent of (R,T)."""
    worst = 0.0
    details = {}
    for b in (1.0, 3.0):
        w = cf.plaquette_mean(b)
        sigma = -np.log(w)
        loops = cf.area_law_loops(w, 6, 6)
        for (r, t) in [(2, 2), (3, 3), (4, 4), (5, 5), (3, 2), (2, 5), (4, 3)]:
            chi = cf.creutz_ratio(loops, r, t)
            dev = abs(chi - sigma)
            worst = max(worst, dev)
        details[f'beta={b}'] = {'sigma': float(sigma),
                                'chi(3,3)': cf.creutz_ratio(loops, 3, 3)}
    return {'test': 'CF4', 'name': 'Creutz ratio χ(R,T)=σ ∀(R,T) (exact area law)',
            'residual': worst, 'target': 1e-12,
            'detail': details,
            'passed': bool(worst < 1e-12),
            'description': 'size-independent χ ⇒ strict area law ⇒ confinement'}


def test_CF5_linear_potential():
    """CF5 — static potential V(R)=σ·R exactly linear; loop estimator T-stable."""
    w = cf.plaquette_mean(2.0)
    sigma = -np.log(w)
    loops = cf.area_law_loops(w, 6, 6)
    # closed form linearity: V(R)/R = σ for all R
    lin = [cf.static_potential_linear(w, r) / r for r in range(1, 6)]
    lin_dev = float(np.max(np.abs(np.array(lin) - sigma)))
    # loop estimator V(R) from W(R,T)/W(R,T-1) is T-independent and = σR
    est_dev = 0.0
    for r in range(1, 5):
        for t in range(2, 6):
            v = cf.static_potential_from_loops(loops, r, t)
            est_dev = max(est_dev, abs(v - sigma * r))
    res = max(lin_dev, est_dev)
    return {'test': 'CF5', 'name': 'Static potential V(R)=σR linear, T-independent',
            'residual': res, 'target': 1e-12,
            'V_over_R': lin, 'sigma': float(sigma),
            'passed': bool(res < 1e-12),
            'description': 'constant force dV/dR=σ ⇒ infinite energy to isolate a quark'}


def test_CF6_mc_plaquette_matches_quadrature():
    """CF6 — Metropolis lattice mean plaquette matches w(β) from quadrature."""
    beta = 2.0
    w = cf.plaquette_mean(beta)
    loops, plaq, n = cf.mc_wilson_loops(beta, L=6, n_therm=120, n_meas=200,
                                        r_max=1, t_max=1, eps=0.3, seed=2024)
    rel = abs(plaq - w) / w
    return {'test': 'CF6', 'name': 'MC mean plaquette ↔ quadrature w(β)',
            'residual': rel, 'target': 0.05,
            'w_quad': w, 'plaq_mc': plaq, 'n_meas': n,
            'passed': bool(rel < 0.05),
            'description': 'independent MC validates the deterministic w(β)'}


def test_CF7_flow_dissolves_confinement():
    """CF7 — Wilson flow raises ⟨plaq⟩ → lowers the effective σ (smoothing)."""
    beta = 1.5
    # thermalise a disordered config
    rng = np.random.default_rng(31)
    U = cs.cold_links_2d((10, 10))
    for _ in range(120):
        U, _ = cf.metropolis_sweep_2d(U, beta, rng, eps=0.3)
    plaq0 = cc.mean_plaquette_2d(U)
    sigma0 = -np.log(max(plaq0, 1e-9))
    Uf, hist = cc.run_wilson_flow_2d(U, eps=0.05, n_steps=20, integrator='rk3')
    plaq1 = cc.mean_plaquette_2d(Uf)
    sigma1 = -np.log(max(plaq1, 1e-9))
    improved = (plaq1 > plaq0) and (sigma1 < sigma0)
    return {'test': 'CF7', 'name': 'Gradient flow smooths disorder → σ_eff decreases',
            'residual': float(sigma1 - sigma0), 'target': 0.0,
            'plaq_before': plaq0, 'plaq_after': plaq1,
            'sigma_before': sigma0, 'sigma_after': sigma1,
            'passed': bool(improved),
            'description': 'confinement lives in the disordered ensemble, not the cooled one'}


def test_CF8_schur_lemma():
    """CF8 — single-plaquette mean ⟨U⟩ = w·I (Schur — engine of factorisation).

    Primary, machine-precision criterion: ⟨(1/N)Tr U⟩ is exactly real (Im part
    = 0 by the φ↔−φ symmetry of the Weyl measure) and equals w(β).  With Schur's
    lemma this is the statement ⟨U⟩ = w·I.  A light Metropolis matrix average
    corroborates the off-diagonal → 0 (statistical, 1/√N).
    """
    beta = 2.0
    w_quad = cf.plaquette_mean(beta)
    tr_complex = cf.plaquette_mean_complex(beta)
    im_part = abs(tr_complex.imag)                       # → 0 machine ε
    re_match = abs(tr_complex.real - w_quad)             # → 0 machine ε
    det_res = max(im_part, re_match)
    # corroborating MC: ⟨U⟩ off-diagonal → 0
    acc = np.zeros((3, 3), dtype=complex)
    ws = []
    for sd in range(6):
        Um, wmc = cf.single_plaquette_mean_matrix(beta, n_samples=8000, seed=200 + sd)
        acc += Um
        ws.append(wmc)
    Umean = acc / 6
    offdiag = float(np.max(np.abs(Umean - np.diag(np.diag(Umean)))))
    ok = (det_res < 1e-12) and (offdiag < 0.05)
    return {'test': 'CF8', 'name': 'Schur: ⟨U⟩ = w·I for the single plaquette',
            'residual': det_res, 'target': 1e-12,
            'Im[<TrU>/N]': im_part, 'Re_match_w': re_match,
            'mc_offdiag': offdiag, 'w_quad': w_quad,
            'passed': bool(ok),
            'description': '⟨(1/N)Tr U⟩ real = w (exact) + MC off-diag→0 ⇒ ⟨W⟩=w^{RT}'}


# ─────────────────────────────────────────────────────────────────────

def main():
    t_start = time.perf_counter()
    tests = [
        test_CF1_w_limits,
        test_CF2_quadrature_convergence,
        test_CF3_string_tension_positive,
        test_CF4_creutz_ratio_exact,
        test_CF5_linear_potential,
        test_CF6_mc_plaquette_matches_quadrature,
        test_CF7_flow_dissolves_confinement,
        test_CF8_schur_lemma,
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
                  f"{r.get('name'):60s}  res = {r.get('residual')}  "
                  f"({r['elapsed_s']:.3f} s)")
        except Exception as exc:
            import traceback
            traceback.print_exc()
            results.append({'test': fn.__name__, 'passed': False, 'error': repr(exc)})
            print(f"  [ERROR] {fn.__name__}: {exc!r}")

    total_t = time.perf_counter() - t_start
    summary = {
        'suite': 'FG-7c — static quark potential / string tension / confinement',
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
                       '..', 'test-results', 'FG7c_confinement.json')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(summary, f, indent=2, cls=_NumpyEncoder)
    print(f"  → wrote {out}")
    raise SystemExit(0 if summary['n_passed'] == summary['n_tests'] else 1)
