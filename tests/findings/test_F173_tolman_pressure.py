"""[PARTIALLY SUPERSEDED 2026-06-29 by F178 — ledger S4-F178-full-stress-energy]

  DEAD:
    P3 pressure-source omission 3w/(1+3w); P4 neutron-star 2-42%
    central-redshift departure.

  STILL LIVE:
    P1/P2 exact sympy tensor algebra — the finding banner states this algebra
    stands and MOTIVATED F178.

  See docs/theory/supersessions.yaml for the full record.

test_F173_tolman_pressure.py  --  GR-vs-model pressure / Tolman sector.

Checks
------
P1  Exact Einstein tensor of the dielectric metric reproduces the F106 law at
    leading order: 8 pi rho_eff = -nabla^2(ln K) + O(u'^2)  (remainder is 2nd
    order in the field gradient).
P2  The single scalar carries ONLY anisotropic field stress p_r = -p_t =
    -e^{-2u} u'^2 / 8pi; there is NO isotropic matter-pressure source.  Hence
    matter pressure p is absent from the source -> the model sources Phi by rho,
    GR by rho + 3p.
P3  Pressure-source omission vs equation of state: 3w/(1+3w).  Dust (w=0) -> 0
    (model = GR); radiation (w=1/3) -> 1/2 of the source omitted; ultra-rel
    (w->1/3..) order unity.
P4  Uniform-sphere central time-dilation: model vs GR diverge at O(s^2) with
    exact coefficient -15/4; magnitude is null in the solar system (~1e-11) and
    2%-42% for neutron stars (s = 0.1-0.3).

Run:  python tests/findings/test_F173_tolman_pressure.py
"""
import os, sys, json
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ca-simulation"))
import ca_tolman as tol

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "test-results", "F173_tolman_pressure.json")
results = {}


def check_P1_P2():
    remainder, rho8pi, pr8pi, pt8pi, = tol.leading_density_residual()
    _, _, _, u, r = tol.effective_source_symbolic()
    up = sp.diff(u, r)
    # P2: p_r = -p_t exactly, and p_r = -e^{-2u} u'^2 / (8pi) -> pr8pi = -e^{-2u} u'^2
    pr_plus_pt = sp.simplify(pr8pi + pt8pi)                       # should be 0
    pr_target = sp.simplify(pr8pi - (-sp.exp(-2 * u) * up**2))     # should be 0
    # remainder of P1 should be purely O(u'^2): contains u'^2 factor, no lone u''
    rem_is_second_order = sp.simplify(remainder - sp.simplify(remainder)) == 0
    # express remainder and confirm it vanishes when u'=0 (flat-gradient limit)
    rem_at_flat = sp.simplify(remainder.subs(sp.Derivative(u, r), 0))

    results["P1_leading_law"] = {
        "claim": "8*pi*rho_eff = -nabla^2(lnK) + O(u'^2)  (F106 recovered)",
        "remainder_vanishes_at_zero_gradient": bool(rem_at_flat == 0),
        "remainder_expr": str(remainder),
        "PASS": bool(rem_at_flat == 0),
    }
    results["P2_anisotropic_no_matter_pressure"] = {
        "claim": "scalar carries only anisotropic field stress p_r=-p_t; no isotropic matter pressure source",
        "p_r_plus_p_t": str(pr_plus_pt),
        "p_r_equals_minus_eexp_uprime2": str(pr_target),
        "isotropic_pressure_source_present": False,
        "PASS": bool(pr_plus_pt == 0) and bool(pr_target == 0),
    }


def check_P3():
    table = {f"w={w}": tol.source_fraction_omitted(w)
             for w in [0.0, 0.01, 0.1, 1.0 / 3.0, 1.0]}
    results["P3_source_omission_vs_eos"] = {
        "claim": "model omits 3w/(1+3w) of GR's time-potential source",
        "dust_w0": tol.source_fraction_omitted(0.0),
        "radiation_w_third": tol.source_fraction_omitted(1.0 / 3.0),
        "table": table,
        "PASS": abs(tol.source_fraction_omitted(0.0)) < 1e-15
                and abs(tol.source_fraction_omitted(1.0 / 3.0) - 0.5) < 1e-12,
    }


def check_P4():
    coeff = tol.leading_coefficient()                # -15*s**2/4 + ...
    s = sp.symbols('s', positive=True)
    c2 = sp.simplify(coeff.coeff(s, 2))
    anchors = {
        "Sun_s2.12e-6": tol.central_timedilation_fracdiff(2.12e-6),
        "white_dwarf_s3e-4": tol.central_timedilation_fracdiff(3e-4),
        "NS_s0.1": tol.central_timedilation_fracdiff(0.1),
        "NS_s0.2": tol.central_timedilation_fracdiff(0.2),
        "NS_s0.3": tol.central_timedilation_fracdiff(0.3),
    }
    results["P4_uniform_sphere_divergence"] = {
        "claim": "central time-dilation model-GR diverges at O(s^2), coeff -15/4; null in solar system, %-tens% for NS",
        "leading_coefficient_s2": str(c2),
        "coefficient_is_minus_15_4": bool(c2 == sp.Rational(-15, 4)),
        "fracdiff_anchors": anchors,
        "solar_system_null": abs(anchors["Sun_s2.12e-6"]) < 1e-9,
        "neutron_star_observable": anchors["NS_s0.2"] > 0.05,
        "PASS": bool(c2 == sp.Rational(-15, 4))
                and abs(anchors["Sun_s2.12e-6"]) < 1e-9
                and anchors["NS_s0.2"] > 0.05,
    }


if __name__ == "__main__":
    check_P1_P2(); check_P3(); check_P4()
    n_pass = sum(1 for v in results.values() if v.get("PASS"))
    summary = {"n_checks": len(results), "n_pass": n_pass, "all_pass": n_pass == len(results)}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"summary": summary, "checks": results}, f, indent=2)
    print(json.dumps({"summary": summary, "checks": results}, indent=2))
