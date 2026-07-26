#!/usr/bin/env python3
"""
run_F261_twoloop_qed.py — standalone runner for the F261 two-loop QED sector.
Emits a JSON result file (per CLAUDE.md: sandbox-timeout-safe path for Claude to
read). Runs the full ca_twoloop_ae + ca_amu reports plus the test-battery
summary, at production quadrature resolution.

Usage:
    python3 tests/runners/run_F261_twoloop_qed.py [--json PATH] [--n 600]
"""
from __future__ import annotations
import os, sys, json, argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
for _cand in (
    os.path.join(_HERE, "..", "..", "ca-simulation"),
    os.path.join(_HERE, "..", "ca-simulation"),
):
    _cand = os.path.abspath(_cand)
    if os.path.isdir(_cand) and _cand not in sys.path:
        sys.path.insert(0, _cand)

import ca_twoloop_ae as tl  # noqa: E402
import ca_amu as amu        # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(
        _HERE, "..", "..", "test-results", "F261_twoloop_qed.json"))
    ap.add_argument("--n", type=int, default=600,
                    help="Gauss-Legendre nodes for the dispersive VP integral")
    args = ap.parse_args()

    me, mmu, mtau = tl.M_E, tl.M_MU, tl.M_TAU

    # high-resolution VP-insertion coefficients (all from F251's spectral function)
    vp = {
        "equal_mass": tl.A2_vp_dispersive(1.0, 1.0, n=args.n),
        "e_in_mu": tl.A2_vp_dispersive(me, mmu, n=args.n),
        "tau_in_mu": tl.A2_vp_dispersive(mtau, mmu, n=args.n),
        "mu_in_e": tl.A2_vp_dispersive(mmu, me, n=args.n),
        "tau_in_e": tl.A2_vp_dispersive(mtau, me, n=args.n),
    }

    out = {
        "finding": "F261",
        "title": "Two-loop QED: A2, two-loop beta, muon a_mu universality",
        "quadrature_nodes": args.n,
        "twoloop_ae": tl.report(),
        "amu": amu.report(),
        "vp_coefficients_highres": vp,
        "reference_targets": {
            "A2_sommerfield_petermann": -0.328478965,
            "A2_vp_equal_mass_exact": 119.0 / 36.0 - (3.141592653589793 ** 2) / 3.0,
            "A2_vp_e_in_mu_known": amu.A2_VP_E_IN_MU_KNOWN,
            "A2_muon_known": amu.A2_MU_KNOWN,
            "two_loop_beta_coeff_alpha3_pi2": 0.5,
        },
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
    with open(args.json, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"wrote {os.path.abspath(args.json)}")
    # brief console summary
    print(f"  A2 (model)          = {out['twoloop_ae']['T2_A2_assembly']['A2_numeric']:.9f}"
          f"  (target -0.328478965)")
    print(f"  VP equal-mass       = {vp['equal_mass']:.9f}  (119/36-pi^2/3)")
    print(f"  A2^VP(e in mu)      = {vp['e_in_mu']:.7f}  (known 1.0942583)")
    print(f"  A2(mu) total        = {out['amu']['U3_a_mu_two_loop']['A2_muon_total']:.9f}"
          f"  (known 0.765857410)")
    print(f"  two-loop beta coeff = {out['twoloop_ae']['BETA_two_loop']['two_loop_coeff_symbolic']}"
          f"  (b1={out['twoloop_ae']['BETA_two_loop']['b1_QED']})")


if __name__ == "__main__":
    main()
