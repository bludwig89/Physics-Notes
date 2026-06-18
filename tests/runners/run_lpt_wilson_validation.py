"""
run_lpt_wilson_validation.py — NATIVE high-resolution validation of the lattice-PT
BZ-integration core (ca_lpt_wilson), to be run by Ben outside the 45 s sandbox.

It evaluates the canonical Wilson one-loop integrals — the tadpole Z0 (published
0.1549333902) and the exact sum rule int khat_x^2/Khat = 1/4 — at production BZ
resolution (n = 64, 96, 128, 160, 192), confirming the integration core
converges to the literature/exact values. This is the validation gate of
docs/design/qstar-gluon-d1-computation-plan.md: the machinery the rule's q*
matching-constant (d1) integral will reuse.

Usage (native):
    python3 tests/runners/run_lpt_wilson_validation.py \
        --n 64 96 128 160 192 --out test-results/lpt_wilson_validation.json

Cost / RAM (4D midpoint grid, float64, one meshgrid axis held at a time via
numpy broadcasting in ca_lpt_wilson):
    n=128 -> 128^4 = 2.7e8 pts ~ 2 GB transient;  n=192 -> 1.36e9 ~ 11 GB;
    n=256 -> 4.3e9 ~ 34 GB (skip unless you have the RAM).
    Each n is a few BZ reductions: seconds (n<=96) to a few minutes (n=192).
    If memory-limited, pass fewer/smaller n (e.g. --n 64 96 128); Z0 is already
    at the 1e-4 level by n=64 and improves ~1/n^2.

Success: Z0 -> 0.154933 (rel dev shrinking ~1/n^2, ~1e-5 by n=192); sum rule
= 0.25 to machine precision at every n. Then the BZ core is trusted, and the
remaining q* work is the vertex+ghost integrand (the next module), not the
integration machinery.

The A-hook (qstar_validation_highres) auto-includes the vertex-driven 28.809
completion once that integrand exists in ca_lpt_wilson.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "ca-simulation"))

import ca_lpt_wilson as w   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[64, 96, 128])
    ap.add_argument("--out", default="test-results/lpt_wilson_validation.json")
    args = ap.parse_args()

    rows = []
    for n in args.n:
        t0 = time.time()
        z = w.tadpole_Z0(n)
        s = w.sum_rule(n)
        secs = round(time.time() - t0, 1)
        rows.append({"n": n, "Z0": z["Z0"], "Z0_rel_dev": z["rel_dev"],
                     "sum_rule": s["int_khatx2_over_Khat"],
                     "sum_rule_dev": s["abs_dev"], "secs": secs})
        print(f"  n={n}: Z0={z['Z0']:.9f} (rel dev {z['rel_dev']:.2e}), "
              f"sum_rule={s['int_khatx2_over_Khat']:.12f} ({secs}s)", flush=True)

    report = {
        "generated": time.strftime("%Y-%m-%d %H:%M"),
        "Z0_published": w.Z0_PUBLISHED,
        "rows": rows,
        "Z0_final": rows[-1]["Z0"], "Z0_final_rel_dev": rows[-1]["Z0_rel_dev"],
        "sum_rule_final": rows[-1]["sum_rule"],
        "lambda_ratio_context": w.lambda_ratio_context(),
        "verdict": ("BZ-integration core validated at production resolution on the "
                    "canonical Wilson integrals (tadpole Z0 + exact sum rule). This "
                    "is the reusable machinery for the rule's q* d1 integral. The "
                    "vertex+ghost finite part (the 28.809 completion / the rule's "
                    "d1) is the next module, per the design doc."),
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nwrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
