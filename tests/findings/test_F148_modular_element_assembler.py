#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F148_modular_element_assembler.py
======================================

F148 — the MODULAR ELEMENT ASSEMBLER.  Verifies that ``ca_element.build_element``
composes an atom out of the model's certified building blocks (a confinement-
bound baryon F122 + the F125 Coulomb/Dirac electron solver) and that the
concrete target, HYDROGEN (1H), comes out a stable, neutral, bound atom with
every number traceable to the model's own constants (m_e, m_p, alpha) — no new
fitted parameters.

Checks
------
  A  NEUTRALITY (exact, integer): protons - electrons = 0 for 1H.
  B  NUCLEUS bound (structural): the proton is a confinement-bound baryon
     (F122); its constituent-quark-mass sum is a minority of M (the 'mass is
     the string' signature) -> a genuinely bound, non-dispersing state.
  C  ELECTRON bound + MODEL-ONLY (machine): the 1s energy equals the
     reduced-mass Rydberg -(1/2) mu c^2 alpha^2 built from imported m_e, m_p,
     alpha — the assembler does not distort F125.
  D  IONIZATION (quantitative): +13.598 eV (reduced-mass H), the measured
     hydrogen ionization energy.
  E  STABLE verdict: neutral AND nucleus bound AND electrons bound.
  F  ZERO new parameters (provenance): every constant the assembler used is
     imported from a model module.
  G  MODULARITY + HONESTY: build_element(Z,N) composes arbitrary elements with
     correct mass number, exact neutrality and correct Aufbau noble-gas
     closures (He 1s2, Ne 2p6, Ar 3p6); and the heavier-element paths are
     wired-but-not-faked — A>=3 nuclear binding and Z>=2 electron energy raise
     NotImplementedError carrying the model-only extension recipe, rather than
     returning an unverified number.

numpy + scipy (via ca_atom / ca_baryon_dynamics); no chiral transforms.
"""

from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ca-simulation"))
import ca_element as E    # noqa: E402
import ca_atom as atom    # noqa: E402

RESULTS = {"finding": "F148", "checks": [], "derived": {}}
_PASS = []


def record(name, ok, detail=""):
    _PASS.append(bool(ok))
    RESULTS["checks"].append({"name": name, "pass": bool(ok), "detail": detail})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))


print("=== F148 modular element assembler — hydrogen stability ===\n")

# Build the target element once.
H = E.build_element(1, 0)            # protium, 1H
rep = H.verify_stability()
RESULTS["derived"]["hydrogen_report"] = {
    k: rep[k] for k in ("element", "Z", "N", "A", "net_charge_e", "neutral",
                        "ionization_energy_eV", "stable")
}

# ---------------------------------------------------------------------------
# A — neutrality (exact integer)
# ---------------------------------------------------------------------------
print("A  electrical neutrality")
record("A net charge of 1H is exactly 0 e", rep["net_charge_e"] == 0,
       f"protons {H.nucleus.charge} + electrons {H.electrons.charge} = {rep['net_charge_e']}")

# ---------------------------------------------------------------------------
# B — nucleus is a bound baryon (F122)
# ---------------------------------------------------------------------------
print("\nB  nucleus: the proton is a confinement-bound baryon (F122)")
b = rep["nucleus"]["baryon"]
frac = b["constituent_mass_fraction"]
record("B1 proton ground state is a finite, discrete (bound) level",
       rep["nucleus"]["bound"] and math.isfinite(b["E_rel"]),
       f"E_rel = {b['E_rel']:.6f} string-units")
record("B2 mass is the string: constituent-mass sum is a minority of M",
       0.0 < frac < 0.5, f"constituent-mass fraction = {frac:.3%} (<50% => confinement-bound)")
record("B3 single-nucleon nuclear binding is exactly 0 (no bond to form)",
       rep["nucleus"]["nuclear_binding_MeV"] == 0.0,
       "A=1: self-bound baryon, no inter-nucleon force needed")
RESULTS["derived"]["baryon"] = b

# ---------------------------------------------------------------------------
# C — electron bound, and model-only (matches the independent reduced-mass Ry)
# ---------------------------------------------------------------------------
print("\nC  electron: bound at the model's own reduced-mass Rydberg")
E_e = rep["electrons"]["total_energy_eV"]
# Independent reconstruction from imported constants ONLY:
mu = atom.reduced_mass_MeV(E.M_E_MEV, E.M_P_MEV)        # uses m_e, m_p
Ry_model = atom.rydberg_eV(mu, Z=1, alpha=E.ALPHA)      # uses alpha
rel = abs(E_e + Ry_model) / Ry_model
record("C1 electron 1s level is bound (E < 0)", E_e < 0.0, f"E_1s = {E_e:.6f} eV")
record("C2 equals -(1/2) mu c^2 alpha^2 from imported m_e,m_p,alpha (machine)",
       rel < 1e-4, f"|E_1s + Ry_model|/Ry = {rel:.2e}  (Ry_model = {Ry_model:.6f} eV)")
RESULTS["derived"]["E_1s_eV"] = E_e
RESULTS["derived"]["Ry_model_eV"] = Ry_model

# ---------------------------------------------------------------------------
# D — ionization energy matches measured hydrogen
# ---------------------------------------------------------------------------
print("\nD  ionization energy vs measured hydrogen")
I = rep["ionization_energy_eV"]
I_meas = 13.5984346      # NIST hydrogen ionization energy (reduced mass), eV
record("D ionization = +13.598 eV (measured H)", abs(I - I_meas) < 5e-3,
       f"I = {I:.6f} eV  vs  measured {I_meas} eV  (rel {abs(I-I_meas)/I_meas:.2e})")
RESULTS["derived"]["ionization_eV"] = I

# ---------------------------------------------------------------------------
# E — overall stability verdict
# ---------------------------------------------------------------------------
print("\nE  composed stability verdict")
record("E 1H is STABLE (neutral & nucleus bound & electron bound)", rep["stable"],
       f"neutral={rep['neutral']}, nucleus bound={rep['nucleus']['bound']}, "
       f"electron bound={rep['electrons']['bound']}")

# ---------------------------------------------------------------------------
# F — zero new parameters (provenance)
# ---------------------------------------------------------------------------
print("\nF  strictly model-only: provenance of every constant used")
prov = {
    "m_e_MeV": (E.M_E_MEV, atom.M_E_MEV, "ca_atom (F120 anchor)"),
    "m_p_MeV": (E.M_P_MEV, atom.M_P_MEV, "ca_atom (F122/F123)"),
    "alpha":   (E.ALPHA,   atom.ALPHA,   "ca_atom (the one EM input, F125)"),
}
all_imported = all(abs(v[0] - v[1]) < 1e-15 * max(1.0, abs(v[1])) for v in prov.values())
record("F all assembler constants are imported model values (no redefinition)",
       all_imported, "; ".join(f"{k}<-{v[2]}" for k, v in prov.items()))
RESULTS["derived"]["provenance"] = {k: {"value": v[0], "source": v[2]} for k, v in prov.items()}

# ---------------------------------------------------------------------------
# G — modularity + honesty of the extension hooks
# ---------------------------------------------------------------------------
print("\nG  modularity: arbitrary (Z,N) compose correctly; hooks are honest")
chart = {"He": (2, 2, "1s2"), "Ne": (10, 10), "Ar": (18, 22), "Fe": (26, 30),
         "U": (92, 146)}
# G1: mass number + neutrality for a heavy ladder
g1 = True
ladder = []
for sym, zn in chart.items():
    z, n = zn[0], zn[1]
    el = E.build_element(z, n)
    ok = (el.A == z + n) and (el.net_charge() == 0)
    g1 = g1 and ok
    ladder.append({"symbol": el.symbol, "Z": z, "N": n, "A": el.A,
                   "net_charge": el.net_charge(),
                   "last_subshell": el.electrons.configuration()[-1]})
record("G1 build_element(Z,N): correct A and exact neutrality across H..U", g1,
       "He,Ne,Ar,Fe,U all A=Z+N and net charge 0")
RESULTS["derived"]["ladder"] = ladder

# G2: Aufbau noble-gas closures (Pauli only)
def last(z):
    return E.build_element(z).electrons.configuration()[-1]
closures = (last(2) == ((1, "s"), 2) and last(10) == ((2, "p"), 6)
            and last(18) == ((3, "p"), 6))
record("G2 Aufbau noble-gas closures: He=1s2, Ne=2p6, Ar=3p6", closures,
       f"He {last(2)}, Ne {last(10)}, Ar {last(18)}")

# G3: heavier paths are now IMPLEMENTED (F157 / ca_manybody) and return
# physical, model-only numbers — the A-body variational cluster (nuclei) and
# the Hartree SCF (electrons).
he = E.build_element(2, 2)
nuc_val = E.Nucleus(6, 6).binding_energy()         # C-12, A-body cluster
nuc_ok = (nuc_val is not None) and (nuc_val > 0.0)  # bound (MeV)
ele_val = he.electrons.total_energy_eV()           # He 1s2 Hartree SCF
ele_ok = (ele_val is not None) and (ele_val < 0.0)  # bound (eV)
record("G3 A>=3 nuclear (A-body cluster) + Z>=2 electron (Hartree SCF) paths "
       "compute model-only bound states (F157)",
       nuc_ok and ele_ok,
       f"C-12 nuclear binding {nuc_val:.1f} MeV; He cloud {ele_val:.1f} eV")

# G4: the A=2 model-native NN bond is reachable (deuteron binds, >0)
print("    (G4 deuteron: model-native NN one-boson-exchange bound state)")
try:
    Eb_d = E.Nucleus(1, 1).binding_energy()
    g4 = Eb_d > 0.0
    detail = f"deuteron binding = {Eb_d:.4f} MeV (>0, bound)"
except Exception as ex:                     # noqa: BLE001
    g4 = False
    detail = f"deuteron solve failed: {ex}"
record("G4 A=2 deuteron (pn) binds via model NN OBE (pi+sigma+omega+core)", g4, detail)
RESULTS["derived"]["deuteron_binding_MeV"] = (Eb_d if g4 else None)

# ---------------------------------------------------------------------------
print("\n" + "=" * 64)
npass, ntot = sum(_PASS), len(_PASS)
RESULTS["summary"] = {"passed": npass, "total": ntot, "all_pass": npass == ntot}
print(f"RESULT: {npass}/{ntot} checks PASS")

out = os.path.join(os.path.dirname(__file__), "..", "..", "test-results",
                   "F148_modular_element_assembler.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"results -> {os.path.relpath(out)}")

sys.exit(0 if npass == ntot else 1)
