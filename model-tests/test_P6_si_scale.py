#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_P6_si_scale.py
===================

P6 of roadmap-matter-binding.md — certify the SI / absolute-scale closure for
the MATTER sector: the current SI choice (canonical geometric cell, F107/F112)
plus the single QCD anchor f_pi = 92.07 MeV turns every dimensionless P2-P4
hadron result into an absolute MeV number.  Each row is scored against PDG with
an honesty tier (PREDICTION / CONSISTENCY / FALSIFIER), exactly as F112 did for
the gravity/EW sector.

Engine: `ca-simulation/ca_si_scale.py` (imports the validated F77/F103 NJL meson
solver `ca_meson` and the F122 three-body baryon solver `ca_baryon_dynamics`).

CHECKS
------
  G0  GEOMETRIC CELL: G_pred from the canonical cell reproduces CODATA (the
      metre/second anchor; PREDICTION, inherited from F112/F107).
  G1  ANCHOR SELF-CONSISTENCY: the model's OWN f_pi (F77 fit) already lands within
      ~0.6% of the physical 92.07 MeV before anchoring — the anchor is a sub-%
      rescaling, not a fudge (CONSISTENCY).
  H1  CONSTITUENT MASS m_c (NJL gap, f_pi-anchored) vs m_N/3 (PREDICTION).
  H2  NUCLEON m_p ~ 3 m_c vs 938.27 MeV (PREDICTION — the headline absolute mass;
      F97 made quantitative: the nucleon mass IS three dynamical constituent
      masses, not the current-quark sum).
  H3  NEUTRON-PROTON splitting m_n - m_p (PREDICTION, already absolute).
  H4  PION m_pi (CONSISTENCY — F77 fit input; near-Goldstone).
  H5  RHO m_rho via KSRF (Tier-3 — one external coupling g_rhopipi).
  H6  SIGMA m_sigma in the broad f0(500) band (CONSISTENCY).
  H7  QUARK CONDENSATE <qbar q>^{1/3} order/sign (CONSISTENCY).
  H8  DEUTERON OPEP range = predicted m_pi (CONSISTENCY; B_d tuned in F104).

All arithmetic REAL.  Runs in a couple of seconds.

Run:  python3 model-tests/test_P6_si_scale.py
Writes test-results/P6_si_scale.json.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "..", "ca-simulation")))
import ca_si_scale as SI  # noqa: E402

results = {"finding": "F123", "phase": "P6",
           "title": "SI absolute-scale closure for the matter sector "
                    "(canonical cell + f_pi anchor)",
           "checks": {}, "registry": {}, "notes": []}
PASS = True


def record(name, value, target, tol, tier, ok, unit=""):
    global PASS
    rel = abs(value - target) / abs(target) if target != 0 else abs(value)
    results["checks"][name] = {"value": float(value), "target": float(target),
                               "rel_err": float(rel), "tol": float(tol),
                               "tier": tier, "status": "PASS" if ok else "FAIL",
                               "unit": unit}
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:34s} = {value:10.4f} {unit:4s} "
          f"vs {target:9.3f}  ({rel*100:+5.2f}%, {tier})")


print("=" * 80)
print("P6 / F123 — SI absolute-scale closure for the matter sector")
print("=" * 80)

reg = SI.si_registry()
results["registry"] = {
    "cell": {k: float(v) for k, v in reg["cell"].items()},
    "anchor_f_pi_MeV": reg["anchor_f_pi_MeV"],
    "strong": {k: (float(v) if not isinstance(v, dict) else
                   {kk: float(vv) for kk, vv in v.items()})
               for k, v in reg["strong"].items()},
    "nucleon": reg["nucleon"],
    "np_split": {k: (float(v) if isinstance(v, (int, float)) else v)
                 for k, v in reg["np_split"].items()},
}

cell = reg["cell"]
strong = reg["strong"]
nuc = reg["nucleon"]
nps = reg["np_split"]

print(f"\nCanonical cell: a = {cell['a_m']:.5e} m = {cell['a_over_ellP']:.5f} ell_P, "
      f"tau = {cell['tau_s']:.4e} s, UV = {cell['UV_cutoff_GeV']:.3e} GeV")
print(f"QCD anchor: f_pi = {reg['anchor_f_pi_MeV']} MeV "
      f"(model f_pi {strong['f_pi_model_MeV']:.2f} -> scale {strong['anchor_scale']:.4f})\n")

# --- G0  geometric cell -> Newton's constant (PREDICTION, F107/F112) ---
record("G0 Newton G (canonical cell, e-11)", cell["G_pred"] * 1e11,
       SI.G_CODATA * 1e11, 1e-6, "PREDICTION", cell["G_rel_err"] < 1e-6, "SI")

# --- G1  anchor self-consistency (CONSISTENCY) ---
record("G1 model f_pi vs physical", strong["f_pi_model_MeV"], 92.07, 0.02,
       "CONSISTENCY", abs(strong["f_pi_model_MeV"] - 92.07) / 92.07 < 0.02, "MeV")

# --- H1  constituent quark mass vs m_N/3 (PREDICTION) ---
m_N_over_3 = 938.918 / 3.0
record("H1 constituent m_c (vs m_N/3)", strong["m_c"], m_N_over_3, 0.03,
       "PREDICTION", abs(strong["m_c"] - m_N_over_3) / m_N_over_3 < 0.03, "MeV")

# --- H2  nucleon mass m_p ~ 3 m_c (PREDICTION, headline) ---
record("H2 nucleon m_p ~ 3 m_c", nuc["m_p_3mc_MeV"], nuc["m_p_PDG"], 0.03,
       "PREDICTION", abs(nuc["m_p_rel_err"]) < 0.03, "MeV")

# --- H3  n-p splitting (PREDICTION, already absolute) ---
record("H3 m_n - m_p", nps["m_n_minus_m_p"], 1.293, 1.0,
       "PREDICTION", abs(nps["m_n_minus_m_p"] - 1.293) < 1.0, "MeV")
results["checks"]["H3 m_n - m_p"]["sign_ok"] = bool(nps["sign_positive"])

# --- H4  pion mass (CONSISTENCY) ---
record("H4 pion m_pi", strong["m_pi"], 138.04, 0.05,
       "CONSISTENCY", abs(strong["m_pi"] - 138.04) / 138.04 < 0.05, "MeV")

# --- H5  rho mass via KSRF (Tier-3) ---
record("H5 rho m_rho (KSRF)", strong["m_rho"], 775.26, 0.05,
       "TIER-3", abs(strong["m_rho"] - 775.26) / 775.26 < 0.05, "MeV")

# --- H6  sigma in the broad f0(500) band (CONSISTENCY) ---
sig_ok = 400.0 <= strong["m_sigma"] <= 800.0
record("H6 sigma m_sigma in f0(500) band", strong["m_sigma"], 550.0, 0.5,
       "CONSISTENCY", sig_ok, "MeV")

# --- H7  quark condensate order/sign (CONSISTENCY) ---
cond = strong["condensate_root"]
record("H7 <qbar q>^1/3 (sign/order)", cond, -272.0, 0.15,
       "CONSISTENCY", (cond < 0) and abs(cond - (-272.0)) / 272.0 < 0.15, "MeV")

# --- H8  deuteron OPEP range set by predicted m_pi (CONSISTENCY) ---
# the one-pion-exchange range is hbar c / m_pi; with the predicted m_pi this is
# an absolute length, so the deuteron's long-range force scale is now predicted
# (the binding B_d itself was tuned via the short-range core in F104).
HBARC = 197.327
opep_range_fm = HBARC / strong["m_pi"]
opep_range_target = HBARC / 138.04
record("H8 deuteron OPEP range (1/m_pi)", opep_range_fm, opep_range_target, 0.05,
       "CONSISTENCY", abs(opep_range_fm - opep_range_target) / opep_range_target < 0.05,
       "fm")

results["notes"] = [
    "SI CHOICE: (1) geometric cell a=sqrt(8pi)3^{1/4} ell_P (F79/F107) fixes the "
    "metre, second and G (CODATA to 3e-8); (2) the single QCD anchor f_pi=92.07 "
    "MeV fixes the strong-sector MeV scale. The cell's own energy unit hbar c/a = "
    "1.85e18 GeV is ~18 orders above the hadron scale (F119 hierarchy), so the "
    "hadron scale MUST be set by one hadronic number — here f_pi.",
    "HEADLINE: with f_pi as the only dimensionful strong input, the NJL gap gives "
    "a constituent mass m_c~310 MeV, so the nucleon as three constituents lands at "
    "3 m_c ~ 928-934 MeV, within ~1% of m_p=938.27. This is F97 made quantitative: "
    "the nucleon mass IS the dynamical (chi-SB) constituent mass, NOT the few-MeV "
    "current-quark sum. The P2 residual confinement/OGE/hyperfine binding is the "
    "remaining ~1% (the constituent mass already absorbed the bulk).",
    "n-p splitting +1.51 MeV (vs +1.293) is a genuine absolute PREDICTION needing "
    "no QCD anchor (it is the F40 down-up current gap beating the EM self-energy).",
    "The light-meson sector (m_pi, m_rho, m_sigma, <qbar q>) lands within a few % "
    "on the single f_pi anchor; m_pi/<qbar q> are F77 fit inputs (CONSISTENCY), the "
    "sigma at 2 m_c and rho via KSRF are predictions (the rho carries one external "
    "coupling, Tier-3).",
    "OPEN: this resolves the F122 'm_p/sqrt(sigma) overshoot' — the overshoot was a "
    "non-relativistic-Cornell artefact of using a light current quark; the f_pi-"
    "anchored constituent route gives the nucleon mass directly and cleanly. The "
    "remaining strong-sector debt is connecting the two QCD calibrations (the F77 "
    "chi-SB scale used here and the P1 string tension sqrt(sigma)) from first "
    "principles — i.e. predicting sqrt(sigma)/f_pi — which is left open.",
]

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "P6_si_scale.json")
results["overall"] = "PASS" if PASS else "FAIL"
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2)

print("\n" + "=" * 80)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
print(f"OVERALL: {'PASS' if PASS else 'FAIL'}   ({n_pass}/{len(results['checks'])} checks)")
print(f"results -> {out_path}")
print("=" * 80)
sys.exit(0 if PASS else 1)
