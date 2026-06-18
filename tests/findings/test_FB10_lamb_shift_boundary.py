#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FB10 — Lamb shift boundary: 2s_{1/2} == 2p_{1/2} at Dirac order.

This is a BOUNDARY / HONESTY test (Tier B). It does NOT claim to predict the
1057.8 MHz Lamb shift. It asserts the opposite: at Dirac (one-particle
relativistic) order the model gives the EXACT degeneracy

    2s_{1/2} == 2p_{1/2}   (machine precision),

because the Dirac-Coulomb (Sommerfeld) spectrum depends only on (n, j):

    2s_{1/2}: l=0, j=1/2 -> kappa = -1   (|kappa|=1)
    2p_{1/2}: l=1, j=1/2 -> kappa = +1   (|kappa|=1)

same n=2, same |kappa| -> identical energy. The residual MEASURED splitting
(2s_{1/2} - 2p_{1/2} ≈ 1057.8 MHz) is therefore EXPLICITLY a QED radiative
effect — vacuum polarization + electron self-energy — that lives OUTSIDE the
current one-body Dirac sector (open QFT-4 roadmap item). A claim to reproduce
1057 MHz without a loop sector would be the falsifier.

Provenance: F125 §I (test ledger item I).

Reuse note: the hand-rolled radial-Dirac integrator (RK4, inward+outward
Wronskian matching of the large/small components G,F, in real arithmetic — NO
scipy for the Dirac pieces, per CLAUDE.md) lives in ca-simulation/ca_atom.py.
That is the same Dirac route exercised by the P5 test (FB05's fine-structure
solve). We import and reuse it directly rather than re-implementing.

Run:
    python3 tests/findings/test_FB10_lamb_shift_boundary.py
Writes:
    test-results/FB10_lamb_shift_boundary.json
"""

import os
import sys
import json
import math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CASIM_DIR = os.path.join(ROOT, "ca-simulation")
if CASIM_DIR not in sys.path:
    sys.path.insert(0, CASIM_DIR)

import ca_atom as atom  # hand-rolled radial-Dirac integrator + Sommerfeld closed form

# Measured Lamb shift (the thing we are explicitly NOT predicting at Dirac order)
LAMB_SHIFT_MHZ_MEASURED = 1057.8          # 2s_{1/2} - 2p_{1/2}, QED
H_PLANCK_eV_PER_HZ = 4.135667696e-15      # eV per Hz (E = h*nu)
MACHINE_EPS_GATE = 1e-13                  # degeneracy must sit at/below this

results = {
    "test_id": "FB10",
    "name": "Lamb shift boundary: 2s_1/2 == 2p_1/2 at Dirac order (Lamb shift is QED-beyond-sector)",
    "tier": "B",
    "model_element": "F125 §I — pure Dirac-Coulomb 2s_1/2 / 2p_1/2 degeneracy; explicit QED/QFT-4 boundary",
    "provenance": "F125 §I (test ledger item I); reuses ca-simulation/ca_atom.py radial-Dirac integrator (same Dirac route as the P5/FB05 fine-structure solve)",
}

print("=" * 72)
print("FB10 — Lamb shift BOUNDARY test: Dirac 2s_1/2 == 2p_1/2 (machine)")
print("=" * 72)

# --- kappa assignment -------------------------------------------------------
# 2s_{1/2}: l=0, j=l+1/2 -> kappa=-1 ;  2p_{1/2}: l=1, j=l-1/2 -> kappa=+1
kap_2s12 = atom.kappa_of(0, True)   # -1
kap_2p12 = atom.kappa_of(1, False)  # +1
print(f"\nkappa(2s_1/2) = {kap_2s12:+d}   kappa(2p_1/2) = {kap_2p12:+d}   "
      f"(|kappa|=1 both, n=2 both)")
assert abs(kap_2s12) == 1 and abs(kap_2p12) == 1

# --- (A) Closed-form Sommerfeld degeneracy (machine precision) --------------
E_2s12_som = atom.sommerfeld_energy(2, kap_2s12)   # units m c^2
E_2p12_som = atom.sommerfeld_energy(2, kap_2p12)
deg_som = abs(E_2s12_som - E_2p12_som)             # dimensionless (m c^2 units)
# Express the closed-form split as a binding-energy difference in eV / MHz too.
Eb_2s12_som = atom.sommerfeld_binding_eV(2, kap_2s12)
Eb_2p12_som = atom.sommerfeld_binding_eV(2, kap_2p12)
deg_som_eV = abs(Eb_2s12_som - Eb_2p12_som)
deg_som_MHz = deg_som_eV / H_PLANCK_eV_PER_HZ / 1.0e6

print("\n(A) Closed-form Dirac-Coulomb (Sommerfeld):")
print(f"    E(2s_1/2) = {E_2s12_som:.15f} m c^2")
print(f"    E(2p_1/2) = {E_2p12_som:.15f} m c^2")
print(f"    |2s_1/2 - 2p_1/2| = {deg_som:.3e} (m c^2 units)  = {deg_som_eV:.3e} eV"
      f"  = {deg_som_MHz:.3e} MHz")

# --- (B) Hand-rolled numerical radial-Dirac solve (genuine RK4 solve) -------
# Reuse ca_atom.numerical_dirac_energy (RK4 inward+outward Wronskian matching,
# real arithmetic). Solve both levels independently and confirm the numerical
# energies coincide to the solver floor — i.e. NO spurious Dirac-level split.
print("\n(B) Hand-rolled numerical radial-Dirac (RK4 inward+outward matching):")
E_2s12_num = atom.numerical_dirac_energy(2, kap_2s12)
E_2p12_num = atom.numerical_dirac_energy(2, kap_2p12)
deg_num = abs(E_2s12_num - E_2p12_num)
# numerical vs closed-form residual (binding-relative) for sanity
Eb_2s12_num = (E_2s12_num - 1.0) * atom.M_E_MEV * 1e6
Eb_2p12_num = (E_2p12_num - 1.0) * atom.M_E_MEV * 1e6
binding = abs(Eb_2s12_som)
rel_2s = abs(Eb_2s12_num - Eb_2s12_som) / binding
rel_2p = abs(Eb_2p12_num - Eb_2p12_som) / binding
print(f"    E_num(2s_1/2) = {E_2s12_num:.15f} m c^2  (rel-binding dev vs Sommerfeld {rel_2s:.2e})")
print(f"    E_num(2p_1/2) = {E_2p12_num:.15f} m c^2  (rel-binding dev vs Sommerfeld {rel_2p:.2e})")
print(f"    |2s_1/2 - 2p_1/2|_num = {deg_num:.3e} (m c^2 units)  "
      f"-> solver floor, not a physical split")

# --- Verdict / gate ---------------------------------------------------------
# PASS requires:
#   1. closed-form Dirac degeneracy at/below machine gate (the exact identity), AND
#   2. the Lamb shift correctly flagged as QED-beyond-sector (asserted below; we
#      do NOT predict 1057 MHz — we record it as a boundary, not a prediction).
closed_form_exact = deg_som <= MACHINE_EPS_GATE
# The numerical solve must not introduce a SPURIOUS split larger than its own
# matching floor. We require the numerical degeneracy to be small relative to
# the fine-structure scale (the 2p_3/2 - 2p_1/2 splitting ~ 4.5e-5 eV); a split
# anywhere near the physical Lamb shift would indicate an internal error.
fs_split_eV = abs(atom.sommerfeld_binding_eV(2, atom.kappa_of(1, True))
                  - atom.sommerfeld_binding_eV(2, atom.kappa_of(1, False)))
deg_num_eV = deg_num * atom.M_E_MEV * 1e6
no_spurious_num_split = deg_num_eV < 0.1 * fs_split_eV   # well below the FS scale
lamb_flagged_qed_beyond = True  # asserted by this test's construction & docs (below)

verdict = "PASS" if (closed_form_exact and no_spurious_num_split
                     and lamb_flagged_qed_beyond) else "FALSIFIED"

print("\n" + "-" * 72)
print(f"closed-form 2s_1/2==2p_1/2 within machine gate ({MACHINE_EPS_GATE:.0e}): "
      f"{closed_form_exact}  (deg={deg_som:.2e})")
print(f"numerical solve introduces no spurious split (< 0.1 * FS = "
      f"{0.1*fs_split_eV:.2e} eV): {no_spurious_num_split}  (deg_num={deg_num_eV:.2e} eV)")
print(f"Lamb shift flagged as QED-beyond-sector (not predicted): {lamb_flagged_qed_beyond}")
print(f"\nVERDICT: {verdict}")
print("-" * 72)

boundary_statement = (
    "At Dirac (one-particle relativistic) order the model gives EXACT "
    "2s_1/2 == 2p_1/2 degeneracy (machine precision): both have n=2 and "
    "|kappa|=1, and the Dirac-Coulomb (Sommerfeld) spectrum E_{n,kappa} "
    "depends only on (n, |kappa|) i.e. (n, j). The MEASURED 2s_1/2-2p_1/2 "
    "Lamb shift (~1057.8 MHz) is therefore EXPLICITLY a QED radiative effect "
    "(vacuum polarization + electron self-energy) that lies OUTSIDE the "
    "current one-body Dirac sector — an open QFT-4 roadmap item, NOT a present "
    "prediction. This test exists to mark that boundary; a claim to reproduce "
    "1057 MHz without an explicit QED loop sector would be the falsifier."
)

results.update({
    "verdict": verdict,
    "predicted": {
        "dirac_2s12_2p12_degeneracy_mc2units": deg_som,
        "dirac_2s12_2p12_degeneracy_eV": deg_som_eV,
        "dirac_2s12_2p12_degeneracy_MHz": deg_som_MHz,
        "statement": "2s_1/2 == 2p_1/2 EXACTLY at Dirac order (machine precision)",
        "lamb_shift_MHz": None,
        "lamb_shift_prediction_note": ("NOT predicted at Dirac order — QED loop "
                                       "physics outside the current sector"),
    },
    "measured_target": {
        "lamb_shift_2s12_minus_2p12_MHz": LAMB_SHIFT_MHZ_MEASURED,
        "source": "QED (vacuum polarization + self-energy); textbook/CODATA Lamb shift",
        "in_current_sector": False,
        "sector": "QFT-4 (radiative loop sector), open roadmap item",
    },
    "gate": {
        "machine_eps_gate_mc2units": MACHINE_EPS_GATE,
        "closed_form_degeneracy_within_gate": closed_form_exact,
        "numerical_no_spurious_split": no_spurious_num_split,
        "numerical_split_gate_eV": 0.1 * fs_split_eV,
        "lamb_flagged_qed_beyond_sector": lamb_flagged_qed_beyond,
        "pass_rule": ("PASS iff closed-form Dirac 2s_1/2==2p_1/2 within machine "
                      "gate AND no spurious numerical Dirac split AND Lamb shift "
                      "flagged QED-beyond-sector"),
    },
    "computed": {
        "kappa_2s12": kap_2s12,
        "kappa_2p12": kap_2p12,
        "E_2s12_sommerfeld_mc2units": E_2s12_som,
        "E_2p12_sommerfeld_mc2units": E_2p12_som,
        "Eb_2s12_sommerfeld_eV": Eb_2s12_som,
        "Eb_2p12_sommerfeld_eV": Eb_2p12_som,
        "E_2s12_numerical_dirac_mc2units": E_2s12_num,
        "E_2p12_numerical_dirac_mc2units": E_2p12_num,
        "numerical_dirac_degeneracy_mc2units": deg_num,
        "numerical_dirac_degeneracy_eV": deg_num_eV,
        "numerical_dirac_relbinding_dev_2s12": rel_2s,
        "numerical_dirac_relbinding_dev_2p12": rel_2p,
        "fine_structure_2p32_2p12_split_eV": fs_split_eV,
        "alpha": atom.ALPHA,
        "m_e_MeV": atom.M_E_MEV,
        "integrator": ("hand-rolled radial-Dirac RK4, inward+outward Wronskian "
                       "matching of large/small components G,F, real arithmetic "
                       "(no scipy for Dirac pieces); reused from "
                       "ca-simulation/ca_atom.py — same Dirac route as the "
                       "P5/FB05 fine-structure solve"),
    },
    "boundary_statement": boundary_statement,
    "commands": ["python3 tests/findings/test_FB10_lamb_shift_boundary.py"],
    "timestamp": "2026-06-16",
})

out_dir = os.path.join(ROOT, "test-results")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "FB10_lamb_shift_boundary.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nwrote {out_path}")
print("\nBOUNDARY: " + boundary_statement)

sys.exit(0 if verdict == "PASS" else 1)
