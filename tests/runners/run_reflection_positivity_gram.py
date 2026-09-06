"""Battery runner: the reflection-positivity Gram-matrix cross-check (F335).

NOT a re-attack of the confinement-measure (string-tension) sampling named in
completeness row B7 as unable to close that residual regardless of statistics.
This checks a different, structural quantity -- see
`casim.engine.gauge.reflection_positivity` module docstring item 4.

    python3 tests/runners/run_reflection_positivity_gram.py --which anisotropic
    python3 tests/runners/run_reflection_positivity_gram.py --which isotropic
    python3 tests/runners/run_reflection_positivity_gram.py --which strong

Writes test-results/F335_reflection_positivity_gram_<which>.json. This is a
`result_dump` at tier `battery`, not a gate record -- each run takes ~90s at
these settings, which does not fit the gate's <2 min combined budget (the
gate carries the FAST exact/identity/su2 legs plus a tiny 24-sweep smoke Gram
check instead; see the `F335-reflection-positivity-bcc` gate record).
"""
import argparse
import json
import os
import sys
import time


def _bootstrap():
    here = os.path.dirname(os.path.abspath(__file__))
    root = here
    for _ in range(6):
        root = os.path.dirname(root)
        if os.path.isdir(os.path.join(root, "src", "casim")):
            break
    src = os.path.join(root, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    return root


CONFIGS = {
    'anisotropic': dict(L=4, Lt=6, N=2, beta_s=2.0, beta_t=8.0, n_therm=150, n_sweeps=1600, n_or=2, tau_pos=1, seed=1),
    'isotropic':   dict(L=4, Lt=6, N=2, beta_s=2.0, beta_t=2.0, n_therm=150, n_sweeps=1600, n_or=2, tau_pos=1, seed=2),
    'strong':      dict(L=4, Lt=6, N=2, beta_s=0.5, beta_t=2.0, n_therm=150, n_sweeps=1600, n_or=2, tau_pos=1, seed=3),
}


def main(argv=None):
    root = _bootstrap()
    from casim.engine.gauge.reflection_positivity import reflection_positivity_gram_check

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--which", choices=list(CONFIGS), required=True)
    args = p.parse_args(argv)

    t0 = time.time()
    cfg = CONFIGS[args.which]
    result = reflection_positivity_gram_check(**cfg)
    result['which'] = args.which
    result['wall_time_s'] = time.time() - t0

    out_dir = os.path.join(root, "test-results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"F335_reflection_positivity_gram_{args.which}.json")
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps({'which': args.which, 'min_eig': result['min_eig'],
                       'max_eig': result['max_eig'],
                       'boot_std': result['min_eig_bootstrap_std'],
                       'wall_time_s': result['wall_time_s']}, indent=2))
    print(f"wrote {out_path}")


if __name__ == '__main__':
    main()
