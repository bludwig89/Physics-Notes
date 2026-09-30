"""F398 robustness audit trail (2026-09-23, from the finding's own attack-and-fix review,
docs/reviews/F398-review-2026-09-23.md, attacks 2 and 12).

The review found no auditable evidence in the repository that the gate's two L values (10, 100)
were "verified clean" of grid-commensurability resonance before being fixed as parameters, and
showed by direct neighbour scan that a raw single-point deficit(L_lo)/deficit(L_hi) ratio is
fragile -- most L within a few units of L=10 or L=100 land far outside the gate's original band.

This script is the audit trail the review asked for: it re-runs BOTH the raw single-point ratio
(the pre-fix estimator) and the `deficit_robust_min`/`bulk_robust_min` lower-envelope estimator
(the post-fix estimator, now what `check_pryce_composite_commutator` actually gates on) across
every (L_lo, L_hi) pair in the review's own tested range, [8,13] x [95,105], and writes the full
result so the claim "the robust estimator is stable across this whole neighbourhood, not just the
one committed anchor pair" is checkable rather than asserted.

Not a gate-tier test (no pass/fail assertion of its own -- the gate's own `deficit_shrinks_with_L`
and `bulk_norm_is_L3` legs, run at the fixed (10, 100) anchor, are that); this is a standalone
diagnostic run, per CLAUDE.md's `tests/runners/` convention.
"""
import json
import os

from casim.engine.gauge.photon_pryce_commutator import (
    deficit_at, deficit_robust_min, bulk_robust_min,
)

ZERO_K = (0.0, 0.0, 0.0)


def scan():
    L_los = list(range(8, 14))
    L_his = [95, 98, 100, 102, 105]
    raw_ratios, robust_deficit_ratios, robust_bulk_ratios = {}, {}, {}
    for L_lo in L_los:
        for L_hi in L_his:
            key = f"{L_lo},{L_hi}"
            d_lo_raw = deficit_at(ZERO_K, L_lo)
            d_hi_raw = deficit_at(ZERO_K, L_hi)
            raw_ratios[key] = d_lo_raw / d_hi_raw

            d_lo_rob, _ = deficit_robust_min(ZERO_K, L_lo)
            d_hi_rob, _ = deficit_robust_min(ZERO_K, L_hi)
            robust_deficit_ratios[key] = d_lo_rob / d_hi_rob

            b_lo_rob, _ = bulk_robust_min(ZERO_K, L_lo)
            b_hi_rob, _ = bulk_robust_min(ZERO_K, L_hi)
            robust_bulk_ratios[key] = b_lo_rob / b_hi_rob

    raw_vals = list(raw_ratios.values())
    robust_vals = list(robust_deficit_ratios.values())
    bulk_vals = list(robust_bulk_ratios.values())
    return {
        "L_los": L_los,
        "L_his": L_his,
        "raw_ratios": raw_ratios,
        "robust_deficit_ratios": robust_deficit_ratios,
        "robust_bulk_ratios": robust_bulk_ratios,
        "summary": {
            "raw_min": min(raw_vals), "raw_max": max(raw_vals),
            "raw_pass_band_30_400": sum(1 for v in raw_vals if 30.0 <= v <= 400.0),
            "n_pairs": len(raw_vals),
            "robust_deficit_min": min(robust_vals), "robust_deficit_max": max(robust_vals),
            "robust_deficit_pass_band_20_200": sum(1 for v in robust_vals if 20.0 <= v <= 200.0),
            "robust_bulk_min": min(bulk_vals), "robust_bulk_max": max(bulk_vals),
        },
    }


def _results_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        cand = os.path.join(here, "test-results")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(here)
        if parent == here:
            raise RuntimeError("cannot locate test-results/ above " + __file__)
        here = parent


if __name__ == "__main__":
    result = scan()
    out = os.path.join(_results_dir(), "F398_robustness_scan.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=2)
    s = result["summary"]
    print(f"wrote {out}")
    print(f"raw single-point ratio: [{s['raw_min']:.2f}, {s['raw_max']:.2f}], "
          f"{s['raw_pass_band_30_400']}/{s['n_pairs']} pairs in the original [30,400] band")
    print(f"robust (lower-envelope) deficit ratio: [{s['robust_deficit_min']:.2f}, "
          f"{s['robust_deficit_max']:.2f}], {s['robust_deficit_pass_band_20_200']}/{s['n_pairs']} "
          f"pairs in the new [20,200] band")
    print(f"robust bulk ratio: [{s['robust_bulk_min']:.4f}, {s['robust_bulk_max']:.4f}] "
          f"(diagnostic only, no band)")
