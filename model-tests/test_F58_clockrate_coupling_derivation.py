"""
test_F58_clockrate_coupling_derivation.py
=========================================
Does the clock-rate ↔ rest-mass coupling 4πG of F52 follow from the CA
neighbour-coupling rule (c_lat = dΩ/d|k| = 1/√d of F25/F26), or is it posited?

Tests forks/gr_fork_F58_clockrate_coupling_derivation.py:

 Q0  Universality (EXACT).  The fractional clock-rate deficit 1−√A is the SAME
     for every mass (√A multiplies arcsin m as a common factor).  A single
     scalar coupling G can only exist if clock slowing per unit potential is
     mass-independent — the weak equivalence principle.  Residual must be 0.

 Q1  The 4π is the lattice solid angle.  The bare 6-neighbour neighbour-coupling
     Laplacian (NO 4π inserted) has point-source far field −1/(4π·hopping·r):
     4π·hopping·C → 1.  So the 4π in ∇²Φ = 4πGρ is geometry the neighbour rule
     resolves, not a hand-inserted constant.

 Q2  The Laplacian FORM is forced.  The small-k neighbour symbol is the
     isotropic stiffness·|k|² (anisotropy → 0 across 100/110/111) — the unique
     local isotropic 2nd-order operator.  ⇒ the field equation must be ∇²Φ ∝ ρ.

 Q3a The F25/F26 lock.  c_lat and the Green's-function stiffness both come from
     ONE neighbour-hopping amplitude J: sweeping J, c_lat ∝ J and stiffness ∝ J²,
     so stiffness/c_lat² is J-independent.  Hence 1/G ∝ stiffness ∝ c_lat² — the
     coupling's dependence on the light-cone speed (and thus on √d) is fixed by
     the neighbour rule.  Also checks the actual BCC c_lat = 1/√3.

 Q3b The dimensionful magnitude is irreducible (Sakharov).  1/G from the BZ
     integral of the F26 dispersion scales as Λ² (exponent → 2 ⇒ G ∝ ℓ²): the
     lattice spacing in metres is the one input a dimensionless lattice cannot
     supply.  Choosing ℓ IS choosing G.

Writes test-results/F58_clockrate_coupling_derivation.json.
Run:  python model-tests/test_F58_clockrate_coupling_derivation.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

THIS = os.path.dirname(__file__)
SIM = os.path.abspath(os.path.join(THIS, "..", "ca-simulation"))
FORKS = os.path.join(SIM, "forks")
for p in (SIM, FORKS):
    if p not in sys.path:
        sys.path.insert(0, p)

import gr_fork_F58_clockrate_coupling_derivation as f58   # noqa: E402


def test_Q0_universality():
    masses = [0.01, 0.05, 0.1, 0.3, 0.6, 0.9]
    A_values = [0.999, 0.99, 0.9, 0.8]
    res = f58.universality_residual(masses, A_values)
    ok = res["max_spread_over_mass"] < 1e-15
    return {
        "name": "Q0_universality_clock_slowing_mass_independent",
        "max_spread_over_mass": res["max_spread_over_mass"],
        "weak_field_check": res["weak_field"][:2],
        "note": "1-sqrt(A) independent of m (common factor) = weak equivalence principle",
        "tol": 1e-15,
        "status": "PASS" if ok else "FAIL",
    }


def test_Q1_fourpi_clockrate_greens_function():
    Phi = f58.clockrate_green_function(L=64, hopping=1.0)
    fit = f58.fit_far_field(Phi)
    four_pi_C = 4.0 * np.pi * fit["C"]              # hopping = 1
    ok = abs(four_pi_C - 1.0) < 5e-3 and fit["fit_r2"] > 0.999
    return {
        "name": "Q1_fourpi_is_lattice_solid_angle",
        "four_pi_hopping_C": float(four_pi_C),
        "target": 1.0,
        "fit_r2": fit["fit_r2"],
        "note": "point mass -> clock-rate field -1/(4pi r); 4pi is bare-lattice geometry",
        "tol": 5e-3,
        "status": "PASS" if ok else "FAIL",
    }


def test_Q2_laplacian_form_forced():
    res = f58.neighbour_symbol_small_k(hopping=1.0)
    ok = res["anisotropy_spread"] < 1e-6
    return {
        "name": "Q2_laplacian_is_unique_isotropic_local_operator",
        "anisotropy_spread": res["anisotropy_spread"],
        "stiffness_per_dir": res["stiffness_per_dir"],
        "note": "isotropic |k|^2 leading order ⇒ field equation must be ∇²Φ ∝ ρ",
        "tol": 1e-6,
        "status": "PASS" if ok else "FAIL",
    }


def test_Q3a_stiffness_clat_lock():
    lock = f58.stiffness_clat_lock(hoppings=(0.5, 1.0, 2.0, 4.0))
    clat_bcc = f58.measured_clat_bcc()
    inv_sqrt3 = 1.0 / np.sqrt(3.0)
    ok = (lock["ratio_spread"] < 1e-9
          and abs(clat_bcc - inv_sqrt3) < 1e-3)
    return {
        "name": "Q3a_coupling_stiffness_locked_to_clat_F25F26",
        "stiffness_over_clat2_spread": lock["ratio_spread"],
        "stiffness_over_clat2_mean": lock["ratio_mean"],
        "rows": lock["rows"],
        "measured_bcc_c_lat": float(clat_bcc),
        "target_1_over_sqrt3": float(inv_sqrt3),
        "note": "c_lat ∝ J, stiffness ∝ J² ⇒ 1/G ∝ stiffness ∝ c_lat² (carries √d)",
        "status": "PASS" if ok else "FAIL",
    }


def test_Q3b_dimensionful_G_irreducible_sakharov():
    res = f58.sakharov_exponent(Lambdas=(0.5, 0.7, 1.0, 1.4), n_grid=56)
    ok = abs(res["exponent_p"] - 2.0) < 0.05
    return {
        "name": "Q3b_dimensionful_G_locked_to_lattice_spacing",
        "sakharov_exponent_p": res["exponent_p"],
        "target": 2.0,
        "I_values": res["I_values"],
        "note": "1/G ∝ Λ² ⇒ G ∝ ℓ² (Planck length); ℓ in metres is irreducible input",
        "tol": 0.05,
        "status": "PASS" if ok else "FAIL",
    }


def main():
    tests = [
        test_Q0_universality,
        test_Q1_fourpi_clockrate_greens_function,
        test_Q2_laplacian_form_forced,
        test_Q3a_stiffness_clat_lock,
        test_Q3b_dimensionful_G_irreducible_sakharov,
    ]
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:  # noqa: BLE001
            import traceback
            results.append({"name": t.__name__, "status": "ERROR",
                            "error": repr(e), "trace": traceback.format_exc()})

    overall = "PASS" if all(r.get("status") == "PASS" for r in results) else "FAIL"
    out = {
        "finding": "F58",
        "title": "Does the clock-rate <-> rest-mass coupling 4piG follow from the neighbour rule?",
        "date": "2026-05-30",
        "overall": overall,
        "tests": results,
    }
    out_dir = os.path.abspath(os.path.join(THIS, "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "F58_clockrate_coupling_derivation.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("=" * 72)
    print("F58 — does 4πG (clock-rate↔rest-mass) follow from the neighbour rule?")
    print("=" * 72)
    for r in results:
        print(f"  [{r.get('status','?'):>5}]  {r['name']}")
        for kk, vv in r.items():
            if kk in ("name", "status", "trace", "rows"):
                continue
            print(f"            {kk}: {vv}")
    print("-" * 72)
    print(f"  OVERALL: {overall}")
    print(f"  wrote {path}")
    return out


if __name__ == "__main__":
    main()
