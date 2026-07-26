"""
test_F243 — Falsification attempt: F3 lensing prediction failure at low
fermion density.  (next-steps line 5 / exactness-inventory not-met #4)
=======================================================================
F3 predicts a fermion density concentration sources a |Phi| depression (the
lensing well) via the symplectic Yukawa back-reaction Pi -= dt*y*(chi^dag eta).
Scale the fermion amplitude by sqrt(rho_frac) (density ~ rho_frac), run F3,
measure D(rho)=max|Phi-v|.  Falsified if at low density the depression
reverses sign / vanishes discontinuously / breaks the linear source law.
NOT falsified if it stays a correct-sign depression scaling linearly.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'ca-simulation'))
RESULTS = os.path.join(HERE, '..', '..', 'test-results')
import ca_unified as un


def run_density(rho_frac, L=128, sigma=12.0, mu2=0.5, lam=0.5, y=0.2,
                dt=0.5, n_steps=120):
    v = float(np.sqrt(mu2 / (2 * lam)))
    state, _ = un.setup_vacuum((L, L), mu2, lam, fermion='mixed', sigma=sigma)
    amp = float(np.sqrt(rho_frac))
    state.eta_u *= amp; state.eta_d *= amp
    state.chi_u *= amp; state.chi_d *= amp
    cx, cy = L // 2, L // 2
    max_dev, diverged = 0.0, False
    for _ in range(n_steps):
        state = un.unified_step(state, mu2, lam, yukawa=y, dt=dt, back_react=True)
        dev = float(np.max(np.abs(np.abs(state.Phi) - v)))
        if not np.isfinite(dev) or dev > 10.0:
            diverged = True; break
        max_dev = max(max_dev, dev)
    phi_center = float(np.abs(state.Phi[cx, cy]))
    return dict(rho_frac=rho_frac, max_dev=max_dev,
                is_depression=bool(phi_center < v), diverged=bool(diverged))


def run():
    fracs = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]
    rows = [run_density(f) for f in fracs]
    rf = np.array([r['rho_frac'] for r in rows])
    dv = np.array([r['max_dev'] for r in rows])

    ok_finite = bool(np.all([not r['diverged'] for r in rows]))
    ok_depression = bool(np.all([r['is_depression'] for r in rows]))
    ok_positive = bool(np.all(dv > 0))
    slope = float(np.polyfit(np.log(rf), np.log(dv), 1)[0])
    wf = rf < 1.0
    slope_wf = float(np.polyfit(np.log(rf[wf]), np.log(dv[wf]), 1)[0])
    ok_linear = bool(abs(slope_wf - 1.0) < 0.15)
    ok_survives = bool(dv[-1] > 1e3 * np.finfo(float).eps)

    falsified = not (ok_finite and ok_depression and ok_positive and
                     ok_linear and ok_survives)
    checks = [
        ("C1 no divergence at any density", ok_finite),
        ("C2 correct depression sign at all densities", ok_depression),
        ("C3 depression positive-definite", ok_positive),
        ("C4 weak-field slope ~1 (linear source law)", ok_linear),
        ("C5 signal survives to rho=0.001", ok_survives),
        ("C6 prediction NOT falsified at low density", not falsified),
    ]
    result = dict(rows=rows, loglog_slope=slope, loglog_slope_weakfield=slope_wf,
                  falsified=falsified,
                  verdict=("NOT FALSIFIED — linear, correct-sign, graceful"
                           if not falsified else "FALSIFIED"),
                  checks={k: bool(v) for k, v in checks})
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "F243_f3_lowdensity_lensing.json"), "w") as f:
        json.dump(result, f, indent=2)

    for k, v in checks:
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"  weak-field log-log slope = {slope_wf:.4f} (linear => 1.000)")
    npass = sum(1 for _, v in checks if v)
    print(f"F243: {npass}/{len(checks)} PASS — {result['verdict']}")
    return npass == len(checks)


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
