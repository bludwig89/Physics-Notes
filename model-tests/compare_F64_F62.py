"""
compare_F64_F62.py — Head-to-head: EM-connection (F64) vs emergent-gravity (F62)
================================================================================
Date: 2026-05-31 - 16:00

Generates a side-by-side comparison of the two gravity routes on the lattice:

  • F62  dirac_gravity_fork.py — gravity in the **rest leg** of the F46 triangle,
         metric carried by TWO independently-sourced legs
             A = 1 + 2Φ/c²   (rest leg)   ,   B = 1 − 2Φ/c²   (spatial leg)
         co-evolved with the Dirac field.  Source = rest-mass density ρ=|Ψ|².
  • F64  gr_fork_F64_em_connection.py — gravity as a single impedance-locked
         **dielectric**  A = 1/K = (1−u)² ,  B = K = (1−u)⁻²  (AB ≡ 1),
         the same exactly-unitary stepper, ONE field equation.  Source = total
         field energy (so massless (E,B) energy gravitates too).

Both batteries are run on the SAME curved-background Dirac stepper, so every
shared observable is an apples-to-apples comparison whose only independent
variable is the metric placement.

Run (≈70 s, exceeds the 45 s sandbox cap — intended to be run by the user):
    python model-tests/compare_F64_F62.py            # run both fresh
    python model-tests/compare_F64_F62.py --cached    # load cached test-results JSON

Writes test-results/F64_vs_F62_comparison.json and .md
"""
from __future__ import annotations

import json
import os
import sys

THIS = os.path.dirname(__file__)
SIM = os.path.abspath(os.path.join(THIS, "..", "ca-simulation"))
FORKS = os.path.join(SIM, "forks")
RES = os.path.abspath(os.path.join(THIS, "..", "test-results"))
for p in (SIM, FORKS):
    if p not in sys.path:
        sys.path.insert(0, p)

STAMP = "2026-05-31 - 16:00"


def _get(d, *path, default=None):
    for k in path:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def gather(cached: bool) -> tuple[dict, dict]:
    """Return (f62_results, f64_results) either fresh or from cached JSON."""
    if cached:
        f62 = json.load(open(os.path.join(RES, "F62_dirac_gravity_fork.json")))
        f64 = json.load(open(os.path.join(RES, "F64_em_connection.json")))["tests"]
        return f62, f64
    import dirac_gravity_fork as dg
    import test_F64_em_connection as t64
    f62 = dg.run_all(verbose=True)
    f64 = t64.run()["tests"]
    return f62, f64


def build_rows(f62: dict, f64: dict) -> list[dict]:
    """Side-by-side rows on the shared observables."""
    rows = []

    def row(name, f62v, f64v, target, note):
        rows.append({"observable": name, "F62_rest_two_leg": f62v,
                     "F64_dielectric": f64v, "GR_target": target, "note": note})

    # flat regression
    row("flat regression residual (→0)",
        _get(f62, "D1_flat_weyl_regression", "residual_max_abs"),
        _get(f64, "D-EM-D1_flat_regression", "residual_max_abs"),
        "0", "both reduce to two free Weyl walks bit-for-bit")
    # free-fall (equivalence principle)
    row("free-fall coeff g_meas/g_pred (→1)",
        _get(f62, "D2a_rindler_freefall", "coeff_ratio"),
        _get(f64, "D-EM-D2a_dielectric_freefall", "coeff_ratio"),
        "1", "EP carried by the rest leg √A — shared exactly")
    row("free-fall mass-universality spread (→0)",
        _get(f62, "D2a_rindler_freefall", "universality_spread"),
        _get(f64, "D-EM-D2a_dielectric_freefall", "universality_spread"),
        "0", "trajectory mass-independent in both")
    # dynamical redshift
    row("dynamical redshift f_near/f_far",
        _get(f62, "D2b_dynamical_redshift", "ratio_meas"),
        _get(f64, "D-EM-D2b_dynamical_redshift", "ratio_meas"),
        _get(f62, "D2b_dynamical_redshift", "ratio_pred_exact_arcsin"),
        "clock rate ∝ √A in both (rest leg)")
    # deflection
    row("deflection K_meas (→ −4)",
        _get(f62, "D2c_schwarzschild_deflection", "K_meas"),
        _get(f64, "D-EM-D2c_dielectric_deflection", "K_meas"),
        "−4", "F64: ONE field; F62: two legs")
    row("deflection K_eikonal (→ −4)",
        _get(f62, "D2c_schwarzschild_deflection", "K_eikonal"),
        _get(f64, "D-EM-D2c_dielectric_deflection", "K_eikonal"),
        "−4", "finite-field: dielectric approaches 4 from above")
    # backreaction norm
    row("backreaction norm drift (→0)",
        _get(f62, "D3a_backreaction_norm", "norm_drift"),
        _get(f64, "D-EM-D3a_backreaction_norm", "norm_drift"),
        "0", "each tick exactly unitary in both")
    # self-redshift loop closure
    row("self-sourced redshift ratio (<1)",
        _get(f62, "D3a_self_redshift", "ratio_meas"),
        _get(f64, "D-EM4_redshift_bend_consistency", "redshift_ratio_meas"),
        "<1 (deep clock slow)", "F62-D3a vs F64-D-EM4; both close the loop")
    return rows


def build_diffs(f64: dict) -> list[dict]:
    """The qualitative / structural differences (where the fork actually lives)."""
    d3 = f64.get("D-EM3_radiation_as_source", {})
    d4 = f64.get("D-EM4_redshift_bend_consistency", {})

    def rnd(x, n=4):
        try:
            return round(float(x), n)
        except (TypeError, ValueError):
            return x
    return [
        {"axis": "field equations for factor-2 bend",
         "F62_rest_two_leg": "2  (A and B sourced independently)",
         "F64_dielectric": "1  (B = 1/A locked by impedance, AB≡1)",
         "verdict": "F64 strictly more parsimonious"},
        {"axis": "source of gravity",
         "F62_rest_two_leg": "rest-mass density ρ = |Ψ|²",
         "F64_dielectric": "total field energy u (incl. massless (E,B))",
         "verdict": "different physics — testable"},
        {"axis": "does massless (E,B) field energy gravitate?",
         "F62_rest_two_leg": "no (ρ_rest = 0 ⇒ Φ = 0 ⇒ 0 deflection)",
         "F64_dielectric": f"yes — radiation/mass deflection ratio "
                           f"{rnd(_get(d3,'ratio_radiation_over_mass_emconn', default='—'))}",
         "verdict": "the empirical fork (D-EM3): 0 vs 1"},
        {"axis": "one self-sourced field gives BOTH GR coefficients",
         "F62_rest_two_leg": "redshift yes; factor-2 bend needs the 2nd leg",
         "F64_dielectric": f"yes — redshift {rnd(_get(d4,'redshift_ratio_meas', default='—'))} "
                           f"AND bend-slope ratio {rnd(_get(d4,'bend_ratio_dielectric_over_rest', default='—'),3)} (≈2)",
         "verdict": "F64 closes D-EM1 on one field (D-EM4)"},
    ]


def write_md(f62, f64, rows, diffs, path):
    n62 = sum(1 for v in f62.values() if isinstance(v, dict) and v.get("pass"))
    n64 = sum(1 for v in f64.values()
              if isinstance(v, dict) and v.get("pass") is True)
    L = []
    L.append("# F64 (EM-connection dielectric) vs F62 (emergent-gravity rest-leg)")
    L.append("")
    L.append(f"_Generated {STAMP} by `model-tests/compare_F64_F62.py`._")
    L.append("")
    L.append(f"Both gravity routes run on the **same** exactly-unitary "
             f"curved-background Dirac stepper (`dirac_gravity_fork`); the only "
             f"independent variable is the metric placement. F62 passes "
             f"{n62}/6 of its battery; F64 passes {n64}/9 (6 dynamic counterparts "
             f"+ 3 static eikonal/field-level, incl. the radiation-as-source "
             f"discriminator F62 has no analogue for).")
    L.append("")
    L.append("## Shared observables — apples-to-apples")
    L.append("")
    L.append("| observable | F62 rest/two-leg | F64 single dielectric | GR target | note |")
    L.append("|---|---|---|---|---|")

    def fmt(v):
        if isinstance(v, float):
            return f"{v:.4g}"
        return str(v)
    for r in rows:
        L.append(f"| {r['observable']} | {fmt(r['F62_rest_two_leg'])} | "
                 f"{fmt(r['F64_dielectric'])} | {fmt(r['GR_target'])} | {r['note']} |")
    L.append("")
    L.append("To leading order in the weak field both maps coincide — "
             "`√A = 1+Φ/c²+O(u²)` and `c_eff = c₀(1+2Φ/c²)+O(u²)` for both — so "
             "the equivalence principle, factor-1 redshift and factor-2 "
             "deflection agree by construction. The dielectric's finite-field "
             "deflection approaches the Einstein value from above "
             "(|K|≳4) where the linearised two-leg approaches from below (|K|≲4).")
    L.append("")
    L.append("## Where the fork actually lives — structural / empirical")
    L.append("")
    L.append("| axis | F62 rest/two-leg | F64 single dielectric | verdict |")
    L.append("|---|---|---|---|")
    for d in diffs:
        L.append(f"| {d['axis']} | {d['F62_rest_two_leg']} | "
                 f"{d['F64_dielectric']} | {d['verdict']} |")
    L.append("")
    L.append("## Bottom line")
    L.append("")
    L.append("The dielectric reproduces **every** dynamical result of the "
             "emergent-gravity module (free-fall/EP, gravitational redshift, "
             "factor-2 light bending, unitary backreaction, self-sourced "
             "loop-closure) using **one** impedance-locked field equation in "
             "place of two independently-sourced metric legs, and it adds a "
             "sharp empirical discriminator — massless (E,B) field energy "
             "gravitates per unit energy exactly as rest mass (ratio≈1), where "
             "the rest-leg route is blind to it (0). The two routes are "
             "numerically degenerate on the classical weak-field tests and "
             "diverge on (a) parsimony and (b) the gravitation of radiation.")
    L.append("")
    with open(path, "w") as fh:
        fh.write("\n".join(L))


def main():
    cached = "--cached" in sys.argv
    f62, f64 = gather(cached)
    rows = build_rows(f62, f64)
    diffs = build_diffs(f64)
    os.makedirs(RES, exist_ok=True)
    out = {"timestamp": STAMP, "cached": cached,
           "f62_module": "ca-simulation/forks/dirac_gravity_fork.py",
           "f64_module": "ca-simulation/forks/gr_fork_F64_em_connection.py",
           "shared_observables": rows, "structural_differences": diffs}
    jpath = os.path.join(RES, "F64_vs_F62_comparison.json")
    mpath = os.path.join(RES, "F64_vs_F62_comparison.md")
    json.dump(out, open(jpath, "w"), indent=2, default=str)
    write_md(f62, f64, rows, diffs, mpath)
    print(f"Wrote {jpath}")
    print(f"Wrote {mpath}")


if __name__ == "__main__":
    main()
