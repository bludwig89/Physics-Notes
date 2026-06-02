"""
Test harness for F79 - Newton's constant from the lattice structure (Sakharov-free).
2026-06-02 - 02:35

Runs the six structural checks and writes test-results/F79_structural_G.json.
Exit code 0 iff all pass.  numpy + fractions only; < 1 s.
"""
from __future__ import annotations
import os
import sys
import json
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "ca-simulation", "forks"))

import gr_fork_F79_structural_G as F79  # noqa: E402


def main():
    res = F79.run_all()

    checks = []

    s1 = res["S1_clat_invG_scaling"]
    checks.append(("S1 I*c c-independent (1/G ~ 1/c_lat = sqrt d)",
                   s1["passed"], f"spread={s1['Ic_spread']:.2e}, c_lat(d=3)={s1['c_lat_BCC'][3]:.6f}"))

    s2 = res["S2_eta_weyl_exact"]
    checks.append(("S2 eta_Weyl = 1/12 exact (rational)",
                   s2["passed"], f"eta_weyl={s2['eta_weyl']}, eta_dirac={s2['eta_dirac']}"))

    s3 = res["S3_em_traceless_zero_tree"]
    checks.append(("S3 EM stress traceless => zero tree K-stiffness",
                   s3["passed"], f"|trT|_max={s3['EM_trace_max_abs']:.2e}, "
                                 f"massive-scalar trace={s3['massive_scalar_trace_mean']:.3f}>0"))

    s4 = res["S4_channel_gap"]
    checks.append(("S4 channel gap c_lat^3 (tree 2, loop -1, gap -3); loop forced",
                   bool(s4["passed"]), f"tree={s4['tree_exponent']:.4f}, "
                                       f"loop={s4['loop_exponent']:.4f}, gap={s4['gap_exponent']:.4f}"))

    s5 = res["S5_gstar_structural"]
    checks.append(("S5 g_* = 48 structural (16/gen x dim T_1u=3; no 4th)",
                   s5["passed"], f"16 x 3 = {s5['g_star']}"))

    s6 = res["S6_assemble_G"]
    checks.append(("S6 a/ell_P = sqrt(8 pi) 3^1/4 = 6.5978; G closed form consistent",
                   s6["passed"], f"a/ellP={s6['a_over_ellP_PREDICTION']:.6f}, "
                                 f"coeff={s6['invG_coefficient_2pi_eta_gstar_sqrt_d']:.4f}, "
                                 f"G_resid={s6['G_consistency_residual']:.2e}"))

    print("=" * 72)
    print("F79 - Newton's constant from the lattice structure (Sakharov-free)")
    print("=" * 72)
    all_ok = True
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        all_ok = all_ok and ok
        print(f"[{status}] {name}\n        {detail}")
    print("-" * 72)
    print(f"a/ell_P (PREDICTION)        = {s6['a_over_ellP_PREDICTION']:.6f}")
    print(f"a  (SI, anchored at ell_P)  = {s6['a_SI_m']:.4e} m")
    print(f"tau(SI, anchored at t_P)    = {s6['tau_SI_s']:.4e} s")
    print(f"1/G = 2 pi eta g_* sqrt d * hbar / (a^2 c^3),  2 pi eta g_* sqrt d = "
          f"{s6['invG_coefficient_2pi_eta_gstar_sqrt_d']:.4f} = 8 pi sqrt 3")
    print(f"G_from_cell (SI)            = {s6['G_from_cell_SI']:.6e}  "
          f"(CODATA 6.67430e-11, resid {s6['G_consistency_residual']:.1e})")
    print("-" * 72)
    print(f"OVERALL: {'ALL PASS' if all_ok else 'FAILURE'}  ({sum(c[1] for c in checks)}/{len(checks)})")

    outdir = os.path.join(ROOT, "test-results")
    os.makedirs(outdir, exist_ok=True)
    payload = {
        "finding": "F79",
        "title": "Newton's constant from the lattice structure (Sakharov-free)",
        "timestamp": "2026-06-02 - 02:35",
        "checks": [{"name": n, "passed": bool(ok), "detail": d} for n, ok, d in checks],
        "n_passed": int(sum(c[1] for c in checks)),
        "n_total": len(checks),
        "all_passed": bool(all_ok),
        "results": res,
    }
    with open(os.path.join(outdir, "F79_structural_G.json"), "w") as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"results -> test-results/F79_structural_G.json")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
