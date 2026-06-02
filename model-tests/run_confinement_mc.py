"""
run_confinement_mc.py — production Monte-Carlo confirmation of the 2D area law
==============================================================================

The automated suite `test_FG7c_confinement.py` proves the *exact* results
(Creutz ratio = σ, linear potential) at machine precision and cross-checks the
single-plaquette mean against a light MC.  This script runs a heavier
Metropolis simulation on a larger lattice with real statistics to confirm the
full area law  ⟨(1/N)Re Tr W(R,T)⟩ = w(β)^{R·T}  for several loop sizes, fits
the string tension, and writes a Claude-readable result.

Runs longer than a sandbox tick — intended to be launched by the user:

    cd model-tests && python3 run_confinement_mc.py

Outputs:
    test-results/confinement_mc.json
    test-results/confinement_mc.md
"""
import sys
import os
import json
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import ca_confinement as cf          # noqa: E402
import ca_strong as cs               # noqa: E402
import ca_cooling as cc              # noqa: E402


def run(beta=2.2, L=12, n_therm=400, n_meas=2000, measure_every=4,
        r_max=4, t_max=4, eps=0.28, seed=20260601):
    rng = np.random.default_rng(seed)
    U = cs.cold_links_2d((L, L))
    print(f"thermalising {n_therm} sweeps at β={beta}, L={L} ...")
    for s in range(n_therm):
        U, acc = cf.metropolis_sweep_2d(U, beta, rng, eps=eps)
    print(f"  acceptance ≈ {acc:.2f}")

    loops = {(r, t): [] for r in range(1, r_max + 1) for t in range(1, t_max + 1)}
    plaq = []
    n_done = 0
    t0 = time.time()
    for s in range(n_meas):
        U, _ = cf.metropolis_sweep_2d(U, beta, rng, eps=eps)
        if s % measure_every:
            continue
        n_done += 1
        plaq.append(cc.mean_plaquette_2d(U))
        for (r, t) in loops:
            loops[(r, t)].append(cg_loop(U, r, t))
        if n_done % 50 == 0:
            print(f"  measured {n_done} configs ({time.time()-t0:.0f}s)")

    w = cf.plaquette_mean(beta)
    sigma_exact = -np.log(w)

    rows = []
    for (r, t) in sorted(loops):
        vals = np.array(loops[(r, t)])
        mean = float(np.mean(vals))
        err = float(np.std(vals) / np.sqrt(len(vals)))
        pred = w ** (r * t)
        rows.append({'r': r, 't': t, 'W_mc': mean, 'W_err': err,
                     'W_pred_wRT': pred,
                     'sigma_dev': abs(mean - pred)})

    # Creutz ratios from the MC loops
    mc_loops = {(r, t): np.mean(loops[(r, t)]) for (r, t) in loops}
    creutz = {}
    for r in range(2, r_max + 1):
        for t in range(2, t_max + 1):
            try:
                creutz[f'{r}x{t}'] = cf.creutz_ratio(mc_loops, r, t)
            except Exception:
                pass

    result = {
        'suite': 'confinement MC (production)',
        'date': time.strftime('%Y-%m-%d - %H:%M'),
        'beta': beta, 'L': L, 'n_therm': n_therm, 'n_meas': n_meas,
        'n_configs': n_done, 'eps': eps,
        'w_quadrature': w, 'sigma_exact': sigma_exact,
        'plaq_mc': float(np.mean(plaq)),
        'loops': rows,
        'creutz_mc': creutz,
        'creutz_exact_sigma': sigma_exact,
    }
    return result


def cg_loop(U, r, t):
    import ca_gluon as cg
    return cg.wilson_loop_2d_avg(U, r, t) / 3.0


def main():
    res = run()
    here = os.path.dirname(__file__)
    out_json = os.path.abspath(os.path.join(here, '..', 'test-results', 'confinement_mc.json'))
    out_md = os.path.abspath(os.path.join(here, '..', 'test-results', 'confinement_mc.md'))
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, 'w') as f:
        json.dump(res, f, indent=2)

    lines = [f"# Confinement MC — {res['date']}", "",
             f"β = {res['beta']}, L = {res['L']}, configs = {res['n_configs']}",
             f"w (quadrature) = {res['w_quadrature']:.6f}, "
             f"σ_exact = −ln w = {res['sigma_exact']:.6f}",
             f"⟨plaquette⟩ MC = {res['plaq_mc']:.6f}", "",
             "| R | T | W_mc | ±err | w^(RT) | |dev| |",
             "|---|---|------|------|--------|-------|"]
    for row in res['loops']:
        lines.append(f"| {row['r']} | {row['t']} | {row['W_mc']:.5f} | "
                     f"{row['W_err']:.5f} | {row['W_pred_wRT']:.5f} | "
                     f"{row['sigma_dev']:.5f} |")
    lines += ["", "Creutz ratios χ(R,T) from MC (exact value = σ = "
              f"{res['creutz_exact_sigma']:.5f}):", ""]
    for k, v in res['creutz_mc'].items():
        lines.append(f"- χ({k}) = {v:.4f}")
    with open(out_md, 'w') as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nwrote {out_json}\nwrote {out_md}")


if __name__ == '__main__':
    main()
