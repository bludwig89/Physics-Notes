#!/usr/bin/env python3
"""
test_F264_qed_allorders_anomaly.py — F264: the ALL-ORDERS / STRUCTURAL
completeness of the model's QED.  Where F251/F252/F258 computed the three
one-loop 1PI functions, this battery establishes that the model's QED is a
renormalizable, anomaly-consistent gauge theory:

  RENORMALIZABILITY CLOSURE  (ca_qed_renormalization.py)
    R1  D = 4 - (3/2)E_f - E_gamma, order-independent                exact (sympy)
    R2  census: only {Sigma, Pi, Lambda} diverge; 4-photon finite    exact
    R3  operator basis dim <= 4: exactly {Z1, Z2, Z3, delta m}      exact

  WARD-TAKAHASHI ALL ORDERS -> CHARGE UNIVERSALITY
    R4  photon-insertion identity S(p')qslash S(p) = S(p) - S(p')    exact (sympy)
        + chain telescope, n = 1..4                                  exact rational
    R5  differential WT forces Z1 = Z2 (unique solution)             exact (sympy)
    R6  e_R = Z3^(1/2) e_0 species-independent (two masses)          exact (sympy)

  RENORMALIZATION GROUP
    R7  CS equation; beta = e^3/12pi^2 from F251 b0 = 4/3;
        gamma_3 = e^2/12pi^2; beta = e*gamma_3 (all orders)           exact (sympy)
    R8  Landau pole ~250 decades above the F107 lattice cutoff        quantitative

  CHIRAL ANOMALY + LATTICE DOUBLING  (ca_chiral_anomaly.py)
    A1  gamma_5 algebra + Tr[g5 gggg] = -4i eps (256),
        Tr[g5 sig sig] = +4i eps (256)                               exact (sympy)
    A2  classical vector conserved / axial = 2im psibar g5 psi        exact (sympy)
    A3  Fujikawa: |coeff| = 1/16pi^2, regulator cancels              exact (sympy)
    A4  shift surface term = 1/32pi^2, D-independent; ratio 2         exact (sympy)
    A5  vector anomaly 0 / axial -2A_0; branch-blind F68/F87 coupling exact (sympy)
    A6  Weyl census: 2 points per branch in the true fcc BZ,
        sum chi = 0; mirror partner at omega = pi (band top)          exact (sympy)
    A7  independent BZ scan confirms the census after folding         numerical
    A8  Nielsen-Ninomiya: exactly one hypothesis fails               structural
    A9  pi0 -> gamma gamma width vs PDG (tests coeff AND N_c = 3)    quantitative

Run:  python3 tests/findings/test_F264_qed_allorders_anomaly.py --json out.json
Test: pytest -q tests/findings/test_F264_qed_allorders_anomaly.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _cand in (
    os.path.join(_HERE, "ca-simulation"),
    os.path.join(_HERE, "..", "..", "ca-simulation"),
    os.path.join(_HERE, "..", "ca-simulation"),
):
    _cand = os.path.abspath(_cand)
    if os.path.isdir(_cand) and _cand not in sys.path:
        sys.path.insert(0, _cand)

import ca_chiral_anomaly as an  # noqa: E402
import ca_qed_renormalization as rn  # noqa: E402


def run_all(scan_n: int = 61) -> dict:
    r1a = rn.superficial_degree_symbolic()
    r1b = rn.divergent_amplitude_census()
    r1c = rn.counterterm_operator_basis()
    r2a = rn.photon_insertion_telescoping_symbolic(max_props=4)
    r2b = rn.differential_wt_forces_z1_eq_z2_symbolic()
    r2c = rn.charge_universality_symbolic()
    r3a = rn.callan_symanzik_symbolic()
    r3c = rn.landau_pole()

    a1 = an.gamma5_basis_symbolic()
    a2 = an.current_divergences_symbolic()
    a3 = an.fujikawa_anomaly_symbolic()
    a4 = an.shift_surface_term_symbolic()
    a5 = an.gauge_vs_axial_weighting_symbolic()
    nn1 = an.weyl_point_census()
    nn2 = an.weyl_point_scan(n=scan_n)
    nn3 = an.nielsen_ninomiya_consistency()
    a6 = an.pi0_to_gamma_gamma()

    checks = {
        # ---------------- renormalizability closure ----------------
        "R1_superficial_degree": {
            "quantity": "D = 4 - (3/2) E_f - E_gamma, independent of V and L",
            "tier": "exact",
            "D_expr": r1a["D_expr"],
            "dD_dV": r1a["dD_dV"], "dD_dL": r1a["dD_dL"],
            "order_independent": r1a["order_independent"],
            "pass": bool(r1a["gate_pass"]),
        },
        "R2_divergence_census": {
            "quantity": "only Sigma, Pi, Lambda diverge; 4-photon box finite; "
                        "four-fermion not generated",
            "tier": "exact",
            "divergent": r1b["divergent_amplitudes"],
            "counterterms": r1b["counterterms"],
            "n_counterterms": r1b["n_counterterms"],
            "D_four_fermion": r1b["D_four_fermion"],
            "pass": bool(r1b["gate_pass"]),
        },
        "R3_operator_basis": {
            "quantity": "gauge/Lorentz/P/C-allowed local operators of dim <= 4",
            "tier": "exact",
            "allowed": r1c["allowed_dim_le_4"],
            "excluded_by_gauge": r1c["excluded_by_gauge_invariance"],
            "excluded_by_parity": r1c["excluded_by_parity"],
            "pass": bool(r1c["gate_pass"]),
        },
        # ---------------- Ward-Takahashi / universality ----------------
        "R4_photon_insertion_telescope": {
            "quantity": "S(p') qslash S(p) = S(p) - S(p'); chain telescope n=1..4",
            "tier": "exact (core symbolic; chains exact-rational)",
            "core_zero": r2a["core_residual_is_zero"],
            "closed_form_propagator_exact": r2a["closed_form_propagator_exact"],
            "telescope": {k: v["residual_is_zero"] for k, v in r2a["telescope"].items()},
            "pass": bool(r2a["gate_pass"]),
        },
        "R5_z1_eq_z2_all_orders": {
            "quantity": "differential WT => Z_1 = Z_2 (unique solution, every mu)",
            "tier": "exact",
            "Z1_solution": r2b["Z1_solution"],
            "one_loop_difference": r2b["one_loop_instance"]["difference"],
            "pass": bool(r2b["gate_pass"]),
        },
        "R6_charge_universality": {
            "quantity": "e_R = Z_3^(1/2) e_0, independent of fermion species",
            "tier": "exact",
            "species_Z2_differs": r2c["species_Z2_actually_differs"],
            "e_R_difference": r2c["e_R_difference"],
            "pass": bool(r2c["gate_pass"]),
        },
        # ---------------- RG ----------------
        "R7_callan_symanzik": {
            "quantity": "CS equation; beta from F251 b0=4/3; gamma_3; beta = e gamma_3",
            "tier": "exact",
            "beta": r3a["beta_from_F251_b0"],
            "b0_read_back": r3a["b0_read_back"],
            "gamma_3": r3a["gamma_3_one_loop_e"],
            "gamma_2": r3a["gamma_2_one_loop"],
            "structural_beta_eq_e_gamma3": r3a["structural_holds"],
            "pass": bool(r3a["gate_pass"]),
        },
        "R8_landau_pole": {
            "quantity": "one-loop Landau scale vs the F107 lattice cutoff",
            "tier": "quantitative",
            "landau_log10_GeV": r3c["landau_scale_log10_GeV"],
            "cutoff_log10_GeV": r3c["lattice_cutoff_log10_GeV"],
            "decades_above_cutoff": r3c["decades_landau_above_cutoff"],
            "pass": bool(r3c["gate_pass"]),
        },
        # ---------------- anomaly ----------------
        "A1_gamma5_traces": {
            "quantity": "gamma_5 algebra; Tr[g5 gggg] = -4i eps (256); "
                        "Tr[g5 sig sig] = +4i eps (256)",
            "tier": "exact",
            "gggg_ok": a1["trace_g5_gggg_eq_m4i_eps"],
            "sigsig_ok": a1["trace_g5_sigsig_eq_p4i_eps"],
            "n_combinations": a1["n_trace_g5_gggg"] + a1["n_trace_g5_sigsig"],
            "pass": bool(a1["gate_pass"]),
        },
        "A2_classical_divergences": {
            "quantity": "vector conserved (any m); axial = 2 i m psibar g5 psi",
            "tier": "exact",
            "gamma5_anticommutes_kinetic": a2["gamma5_anticommutes_kinetic"],
            "gamma5_commutes_mass": a2["gamma5_commutes_mass"],
            "pass": bool(a2["gate_pass"]),
        },
        "A3_fujikawa_coefficient": {
            "quantity": "|anomaly coeff| = 1/16pi^2, regulator cancels",
            "tier": "exact",
            "signed": a3["anomaly_coefficient_signed"],
            "magnitude": a3["anomaly_coefficient_magnitude"],
            "gaussian": a3["gaussian"],
            "regulator_cancels": a3["regulator_cancels"],
            "EdotB_form": a3["form_EdotB"],
            "pass": bool(a3["gate_pass"]),
        },
        "A4_surface_term": {
            "quantity": "shift surface term = 1/32pi^2, D-independent; ratio 2",
            "tier": "exact",
            "surface": a4["surface_term"],
            "D_independent": a4["D_independent"],
            "ratio": a4["ratio_anomaly_over_surface"],
            "pass": bool(a4["gate_pass"]),
        },
        "A5_vector_safe_axial_anomalous": {
            "quantity": "A_vector = 0, A_axial = -2 A_0; branch-blind U(1)",
            "tier": "exact",
            "A_vector": a5["A_vector"], "A_axial": a5["A_axial"],
            "branch_blind": a5["identity_channel_branch_blind"],
            "pass": bool(a5["gate_pass"]),
        },
        "A6_weyl_census": {
            "quantity": "true fcc BZ: 2 Weyl points per branch, sum chi = 0; "
                        "mirror partner at omega = pi",
            "tier": "exact",
            "copies_of_bz_in_cube": nn1["copies_of_bz_in_cube"],
            "n_weyl_per_branch": {s: nn1["census"][s]["n_weyl_points"]
                                  for s in ("+", "-")},
            "chirality_sums": {s: nn1["census"][s]["chirality_sum"]
                               for s in ("+", "-")},
            "light_dirac_points": nn1["light_dirac_points"],
            "mirror_points": nn1["mirror_points_gapped_at_band_top"],
            "pass": bool(nn1["gate_pass"]),
        },
        "A7_weyl_scan": {
            "quantity": "independent BZ scan; 8 zeros mod 2pi fold to 2 under fcc",
            "tier": "numerical",
            "per_branch": {k: {"mod2pi": v["n_zeros_mod_2pi"],
                               "fcc": v["n_inequivalent_after_fcc_folding"]}
                           for k, v in nn2["per_branch"].items()},
            "pass": bool(nn2["gate_pass"]),
        },
        "A8_nielsen_ninomiya": {
            "quantity": "exactly one NN hypothesis fails (conserved chiral charge)",
            "tier": "structural",
            "failing": nn3["failing_hypotheses"],
            "chirality_sum_still_zero": nn3["chirality_sum_still_zero"],
            "honest_correction": nn3["honest_correction"]["verdict"],
            "pass": bool(nn3["gate_pass"]),
        },
        "A9_pi0_width": {
            "quantity": "Gamma(pi0->gamma gamma) = alpha^2 m^3/64pi^3 f_pi^2 vs PDG",
            "tier": "quantitative",
            "width_eV": a6["width_eV"], "pdg_eV": a6["pdg_eV"],
            "rel_err": a6["rel_err"], "n_sigma": a6["n_sigma"],
            "Nc_sensitivity": {k: v["width_eV"]
                               for k, v in a6["colour_count_sensitivity"].items()},
            "pass": bool(a6["gate_pass"]),
        },
    }

    n_pass = sum(1 for c in checks.values() if c["pass"])
    return {
        "finding": "F264",
        "title": ("All-orders QED: renormalizability closure, Ward-Takahashi "
                  "Z1=Z2 and charge universality, the Callan-Symanzik equation, "
                  "and the ABJ anomaly with Nielsen-Ninomiya consistency"),
        "checks": checks,
        "n_pass": n_pass,
        "n_total": len(checks),
        "all_pass": bool(n_pass == len(checks)),
        "detail": {
            "renormalization": {
                "R1a": r1a, "R1b": r1b, "R1c": r1c,
                "R2a": r2a, "R2b": r2b, "R2c": r2c,
                "R3a": r3a, "R3c": r3c,
            },
            "anomaly": {
                "A1": a1, "A2": a2, "A3": a3, "A4": a4, "A5": a5,
                "NN1": nn1, "NN2": nn2, "NN3": nn3, "A6": a6,
            },
        },
    }


_CACHE: dict = {}


def _res() -> dict:
    if "r" not in _CACHE:
        _CACHE["r"] = run_all()
    return _CACHE["r"]


# ---------------------------------------------------------------- pytest
def test_R1_superficial_degree():
    assert _res()["checks"]["R1_superficial_degree"]["pass"]


def test_R2_divergence_census():
    assert _res()["checks"]["R2_divergence_census"]["pass"]


def test_R3_operator_basis():
    assert _res()["checks"]["R3_operator_basis"]["pass"]


def test_R4_photon_insertion_telescope():
    assert _res()["checks"]["R4_photon_insertion_telescope"]["pass"]


def test_R5_z1_eq_z2_all_orders():
    assert _res()["checks"]["R5_z1_eq_z2_all_orders"]["pass"]


def test_R6_charge_universality():
    assert _res()["checks"]["R6_charge_universality"]["pass"]


def test_R7_callan_symanzik():
    assert _res()["checks"]["R7_callan_symanzik"]["pass"]


def test_R8_landau_pole():
    assert _res()["checks"]["R8_landau_pole"]["pass"]


def test_A1_gamma5_traces():
    assert _res()["checks"]["A1_gamma5_traces"]["pass"]


def test_A2_classical_divergences():
    assert _res()["checks"]["A2_classical_divergences"]["pass"]


def test_A3_fujikawa_coefficient():
    assert _res()["checks"]["A3_fujikawa_coefficient"]["pass"]


def test_A4_surface_term():
    assert _res()["checks"]["A4_surface_term"]["pass"]


def test_A5_vector_safe_axial_anomalous():
    assert _res()["checks"]["A5_vector_safe_axial_anomalous"]["pass"]


def test_A6_weyl_census():
    assert _res()["checks"]["A6_weyl_census"]["pass"]


def test_A7_weyl_scan():
    assert _res()["checks"]["A7_weyl_scan"]["pass"]


def test_A8_nielsen_ninomiya():
    assert _res()["checks"]["A8_nielsen_ninomiya"]["pass"]


def test_A9_pi0_width():
    assert _res()["checks"]["A9_pi0_width"]["pass"]


def test_all_pass():
    assert _res()["all_pass"]


# ---------------------------------------------------------------- CLI
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    ap.add_argument("--scan-n", type=int, default=61)
    args = ap.parse_args()

    res = run_all(scan_n=args.scan_n)
    for name, c in res["checks"].items():
        flag = "PASS" if c["pass"] else "FAIL"
        print(f"[{flag}] {name:34s} ({c['tier']:>34s})  {c['quantity']}")
    print(f"\n{res['n_pass']}/{res['n_total']} checks pass")

    if args.json:
        with open(args.json, "w") as fh:
            json.dump(res, fh, indent=2, default=str)
        print(f"wrote {args.json}")
