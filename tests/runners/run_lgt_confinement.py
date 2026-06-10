"""
run_lgt_confinement.py — production 3+1D SU(3) string-tension measurement (P1 Option A)
=======================================================================================

The heavy, user-run counterpart of `test_FA_lgt_mc.py`.  Thermalises a 4D SU(3)
Wilson ensemble with the heat-bath/over-relaxation engine in
`ca-simulation/forks/lgt_fork_A_mc.py`, measures the static quark potential
V(R) with the Lüscher–Weisz **two-level** estimator (beating the exponential
signal-to-noise wall that defeated the plain Metropolis in
`run_confinement_mc.py`), fits  V(R) = mu + sigma R - e/R, and reports the
string tension sigma with a jackknife error.  Cross-checks against the
leading strong-coupling value sigma ≈ -ln(beta/18).

This runs **longer than a sandbox tick** — launch it yourself:

    cd tests/findings && python3 run_lgt_confinement.py            # default production
    cd tests/findings && python3 run_lgt_confinement.py --smoke    # ~1 min sanity run

Outputs (Claude-readable):
    test-results/lgt_confinement.json
    test-results/lgt_confinement.md

Runtime guide (pure-numpy, single core):
    --smoke   L=6,  ~1-2 min   (qualitative V(R) only)
    default   L=10, ~1-3 h     (sigma with error bars; raise n_conf for tighter)
"""
import sys
import os
import json
import time
import argparse
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ca-simulation'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ca-simulation', 'forks'))

import lgt_fork_A_mc as A          # noqa: E402


def measure_potential(L=10, beta=5.8, n_therm=400, n_conf=40, n_decorr=10,
                      n_blocks=None, n_sub=20, R_list=(1, 2, 3, 4), seed=20260604,
                      verbose=True):
    """
    Measure V(R) via the two-level Polyakov correlator on an L^4 lattice.

    Returns dict: per-R correlator mean/err, V(R), and the (sigma,e,mu) fit
    with a jackknife sigma error over the outer configurations.
    """
    rng = np.random.default_rng(seed)
    D = 4
    T = L
    if n_blocks is None:
        # pick the largest block count (>=2) dividing T, capped at T//2
        n_blocks = max(d for d in range(2, T // 2 + 1) if T % d == 0)

    U = A.cold_links(L, D)
    if verbose:
        print(f"[therm] L={L} beta={beta}: {n_therm} heat-bath(+OR) sweeps ...")
    t0 = time.time()
    for s in range(n_therm):
        U = A.heatbath_sweep(U, beta, rng, n_or=3)
        if verbose and (s + 1) % max(1, n_therm // 10) == 0:
            print(f"   sweep {s+1}/{n_therm}  <plaq>={A.mean_plaquette(U):.4f}  "
                  f"({time.time()-t0:.0f}s)")

    # measurement: per outer config, two-level correlator at each R
    corr_samples = {R: [] for R in R_list}
    for c in range(n_conf):
        for _ in range(n_decorr):
            U = A.heatbath_sweep(U, beta, rng, n_or=3)
        for R in R_list:
            cc = A.polyakov_correlator_twolevel(U, beta, rng, R,
                                                n_blocks=n_blocks, n_sub=n_sub,
                                                space_axis=0)
            corr_samples[R].append(np.real(cc))
        if verbose:
            print(f"[meas] config {c+1}/{n_conf}  "
                  + "  ".join(f"C({R})={np.mean(corr_samples[R]):.3e}" for R in R_list))

    # jackknife over configs for sigma
    Rs = list(R_list)
    corr_arr = {R: np.array(corr_samples[R]) for R in Rs}
    corr_mean = {R: float(corr_arr[R].mean()) for R in Rs}
    corr_err = {R: float(corr_arr[R].std(ddof=1) / np.sqrt(len(corr_arr[R]))) for R in Rs}
    V = {R: A.static_potential_from_polyakov(corr_mean[R], T) for R in Rs}

    # full fit
    good = [R for R in Rs if np.isfinite(V[R])]
    fit = A.fit_linear_plus_coulomb([R for R in good], [V[R] for R in good]) \
        if len(good) >= 3 else None

    # jackknife sigma error
    sigma_jk = []
    n = len(corr_arr[Rs[0]])
    for k in range(n):
        Vk = {}
        for R in Rs:
            mk = np.mean(np.delete(corr_arr[R], k))
            Vk[R] = A.static_potential_from_polyakov(mk, T)
        gk = [R for R in Rs if np.isfinite(Vk[R])]
        if len(gk) >= 3:
            fk = A.fit_linear_plus_coulomb(gk, [Vk[R] for R in gk])
            sigma_jk.append(fk['sigma'])
    sigma_jk = np.array(sigma_jk)
    sigma_err = float(np.sqrt((n - 1) / n * np.sum((sigma_jk - sigma_jk.mean()) ** 2))) \
        if len(sigma_jk) > 1 else float('nan')

    return {
        'L': L, 'beta': beta, 'T': T, 'n_blocks': n_blocks, 'n_sub': n_sub,
        'n_therm': n_therm, 'n_conf': n_conf, 'n_decorr': n_decorr,
        'R_list': Rs,
        'corr_mean': corr_mean, 'corr_err': corr_err,
        'V': {R: (float(V[R]) if np.isfinite(V[R]) else None) for R in Rs},
        'fit': fit,
        'sigma_jackknife_err': sigma_err,
        'strong_coupling_sigma': A.strong_coupling_sigma(beta),
        'mean_plaquette': A.mean_plaquette(U),
        'elapsed_s': time.time() - t0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true', help='fast ~1-2 min sanity run')
    ap.add_argument('--L', type=int, default=None)
    ap.add_argument('--beta', type=float, default=5.8)
    args = ap.parse_args()

    if args.smoke:
        cfg = dict(L=args.L or 6, beta=args.beta, n_therm=60, n_conf=8,
                   n_decorr=4, n_sub=10, R_list=(1, 2, 3))
    else:
        cfg = dict(L=args.L or 10, beta=args.beta, n_therm=400, n_conf=40,
                   n_decorr=10, n_sub=20, R_list=(1, 2, 3, 4))

    print("=" * 70)
    print(f"Option A — 3+1D SU(3) string tension   ({'SMOKE' if args.smoke else 'PRODUCTION'})")
    print("=" * 70)
    res = measure_potential(**cfg)

    fit = res['fit']
    sig = fit['sigma'] if fit else float('nan')
    print("\n--- result ---")
    print(f"  beta = {res['beta']},  L = {res['L']},  <plaq> = {res['mean_plaquette']:.4f}")
    for R in res['R_list']:
        print(f"  V({R}) = {res['V'][R]}")
    if fit:
        print(f"  fit V(R) = {fit['mu']:.4f} + {fit['sigma']:.4f} R - {fit['e']:.4f}/R "
              f"(rms {fit['rms']:.2e})")
        print(f"  sigma = {sig:.4f} +/- {res['sigma_jackknife_err']:.4f}")
    print(f"  strong-coupling -ln(beta/18) = {res['strong_coupling_sigma']:.4f}")

    out_json = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..', '..', 'test-results', 'lgt_confinement.json'))
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, 'w') as f:
        json.dump(res, f, indent=2, default=lambda o: float(o) if isinstance(o, np.floating) else o)
    out_md = out_json.replace('.json', '.md')
    with open(out_md, 'w') as f:
        f.write(f"# Option A — 3+1D SU(3) string tension\n\n")
        f.write(f"- beta = {res['beta']}, L = {res['L']}^4, <plaq> = {res['mean_plaquette']:.4f}\n")
        f.write(f"- mode: {'smoke' if args.smoke else 'production'}, "
                f"n_therm={res['n_therm']}, n_conf={res['n_conf']}, "
                f"two-level n_blocks={res['n_blocks']} n_sub={res['n_sub']}\n\n")
        f.write("| R | C(R) | err | V(R) |\n|---|------|-----|------|\n")
        for R in res['R_list']:
            f.write(f"| {R} | {res['corr_mean'][R]:.3e} | {res['corr_err'][R]:.1e} | {res['V'][R]} |\n")
        if fit:
            f.write(f"\n**Fit** V(R) = {fit['mu']:.4f} + {fit['sigma']:.4f} R - {fit['e']:.4f}/R, "
                    f"rms {fit['rms']:.2e}\n\n")
            f.write(f"**sigma = {sig:.4f} ± {res['sigma_jackknife_err']:.4f}**  "
                    f"(lattice units; strong-coupling -ln(beta/18) = {res['strong_coupling_sigma']:.4f})\n")
    print(f"\n  -> wrote {out_json}\n  -> wrote {out_md}")


if __name__ == '__main__':
    main()
