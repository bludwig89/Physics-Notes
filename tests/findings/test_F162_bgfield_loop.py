"""
F162 — the background-field one-loop gluon self-energy: the b0 = 11/3 C_A
recovery gate, assembled and PASSED exactly (continuum), plus the
well-conditioned lattice-b0 confirmation. The finite d1 to the digit stays open
(needs the bespoke lattice vertex form factors, Wilson-28.81-validated); the
F155 q* bracket stands.

  G1 (EXACT, symbolic): the assembled background-field self-energy (gluon loop
     GammaF.GammaF + ghost loop -2(2k+q)(2k+q), Abbott xi=1 / hep-ph/9406271) is
     EXACTLY transverse and its UV log coefficient gives b0 = 11/3 C_A = 11, with
     the gluon:ghost split 10:1. Scalar-bubble calibration g=1 fixes the
     normalisation. Certifies the loop ASSEMBLY (what F155 lacked).

  G2 (WELL-CONDITIONED): swapping the continuum propagator for the lattice one
     (Wilson / rule K=3 Omega_even^2) leaves the log coefficient UNCHANGED — the
     subtracted transverse coefficient Delta = B_lat - B_cont is q-flat (Wilson
     to <1e-3), no residual log. So lattice b0 = continuum b0 = 11. The rule's
     propagator-driven shift is ~0 (near-perfect action) -> q* at the band top.

  G3 (SCOPE, honest): the finite d1 that pins q* a = exp(-d1/2b0^alpha) = 0.733
     to the digit needs the vertex form-factor finite part (the bespoke lattice
     3-gluon+ghost cos(k/2) vertices), validated against the Wilson finite
     constant 28.81. NOT executed here. F155 bracket [1/sqrt3, ~0.97] stands.
"""
import math
import os
import sys

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.gauge import bgfield_loop as bg


def run():
    results = {}

    # ---- G1: the b0 gate, exact (symbolic) ----
    g = bg.b0_gate_symbolic()
    okG1 = (g["gate_pass"] and g["b0_total"] == "11" and g["transverse"]
            and g["calibration_ok"] and g["g_tensor_coeff_total"] == "22/3"
            and g["b0_gluon"] == "10" and g["b0_ghost"] == "1")
    results["G1_b0_gate_exact"] = dict(
        passed=bool(okG1), b0_total=g["b0_total"], b0_target=g["b0_target"],
        transverse=g["transverse"], calibration_g=g["scalar_bubble_calibration_g"],
        gluon_ghost_split=[g["b0_gluon"], g["b0_ghost"]],
        tensor_coeff=g["g_tensor_coeff_total"])

    # ---- G2: lattice b0 = continuum b0 (subtracted, well-conditioned) ----
    lc = bg.lattice_b0_consistency(n=18)
    okG2 = (lc["b0_propagator_independent"] and lc["rule_shift_small"]
            and lc["wilson_shift_spread"] < 1e-3)
    results["G2_lattice_b0_propagator_independent"] = dict(
        passed=bool(okG2), wilson_shift_spread=lc["wilson_shift_spread"],
        wilson_shift_mean=lc["wilson_shift_mean"],
        rule_shift_mean=lc["rule_shift_mean"], n=lc["n"])

    # ---- G3: scope honesty — the finite d1 gate is sharp and open ----
    st = bg.d1_qstar_status()
    okG3 = (st["qstar_a_implied_F151"] == 0.7327 and st["lambda_ratio_target"] == 1.78
            and st["wilson_contrast"] == 28.81
            and "OPEN" in st["finite_d1_to_digit"])
    results["G3_finite_d1_open_bracket_stands"] = dict(
        passed=bool(okG3), qstar_bracket=st["qstar_a_bracket"],
        implied_qstar=st["qstar_a_implied_F151"], lambda_ratio_target=st["lambda_ratio_target"],
        wilson_contrast=st["wilson_contrast"],
        verdict="b0 gate PASS (exact + lattice); finite d1 to digit OPEN "
                "(vertex form factors, Wilson-28.81 gate); F155 bracket stands")

    n = sum(r["passed"] for r in results.values())
    results["summary"] = dict(passed=n, total=3, all_pass=n == 3,
                              b0_gate="PASS (exact 11 = 10 gluon + 1 ghost)",
                              qstar_pinned=False, qstar_bracketed=True)
    return results


if __name__ == "__main__":
    import json
    r = run()
    print(json.dumps(r, indent=2, default=str))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "test-results", "F162_bgfield_loop.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(r, f, indent=2, default=str)
    assert all(r[k]["passed"] for k in
               ("G1_b0_gate_exact", "G2_lattice_b0_propagator_independent",
                "G3_finite_d1_open_bracket_stands")), "F162 checks failed"
    print("\nF162: 3/3 PASS")
