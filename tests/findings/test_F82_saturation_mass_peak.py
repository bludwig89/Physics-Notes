#!/usr/bin/env python3
"""
test_F82_saturation_mass_peak.py
================================

F82 — Why the charged-lepton pair sits at its phase-saturation edge.

F81 derived Q=2/3 from a two-constituent pair AT saturation (N*phi=pi/2), but
left "why at saturation" open, and F80-D5 flagged that perturbative EM looks
~340x too weak to drive the rotation.  This finding resolves both with one
observation:

  The composite (lepton) mass m_H = sin(2*phi) PEAKS at the saturation edge
  2*phi = pi/2 (phi=45deg).  A condensate lowers its energy by increasing its
  gap (the composite mass), E(phi) = E0 - lambda*sin(2*phi), lambda>0.  This is
  minimised at phi=45deg for ANY lambda>0 -- the LOCATION of the minimum is
  INDEPENDENT of the coupling strength.

So the lepton sits at saturation because that is where its own mass is maximal,
and even an infinitesimal binding puts the energy minimum exactly there.  The
weakness of EM (F80-D5) sets only the DEPTH of the well, not its location ->
the "340x too weak" objection dissolves.

The one remaining assumption is that phi is a FLAT direction (a modulus): no
stiffness kappa favouring the democratic point.  With kappa>0 the minimum
moves below 45deg, so the observed EXACT 45deg is itself evidence that the
generation-rotation direction is flat (a free lattice background, F76).

Corollary: Q is monotonic in the composite mass / degree of binding.  A
massless (unbound) pair sits at phi=0 -> Q=1/3 (democratic); a maximally bound
pair at phi=45deg -> Q=2/3.  A CLEAN two-body pair therefore has Q<=2/3,
saturating at 2/3.  Charged leptons (bound) -> 2/3; neutrinos (nearly unbound)
-> near democratic; quarks Q>2/3 -> NOT clean two-body pairs (QCD).

Checks
------
  G1  m_H = sin(2*phi) peaks at phi=45deg exactly (value 1).
  G2  E(phi)=E0-lambda*sin(2*phi) is minimised at phi=45deg for every lambda
      over 10 decades -> the saturation LOCATION is coupling-independent.
  G3  With stiffness kappa>0, E=kappa*phi^2/2 - lambda*sin(2*phi) minimises
      BELOW 45deg, ->45deg only as kappa->0: exact 45deg <=> flat direction.
  G4  Q(m_H) is monotonic from 1/3 (m_H=0, unbound/democratic) to 2/3 (m_H=1,
      maximally bound); clean two-body pairs satisfy Q<=2/3 (charged leptons
      saturate; quark Q>2/3 falls outside -> not clean pairs).
  G5  honest residual: the flat-direction (kappa=0) assumption, supported by
      the data sitting at EXACTLY 45deg.
"""

import json
import os
import math
import numpy as np

RESULTS = {}
PASS = True


def record(name, ok, detail):
    global PASS
    RESULTS[name] = {"pass": bool(ok), **detail}
    PASS = PASS and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


phis = np.linspace(0.0, math.pi / 2, 200001)


# ════════════════════════════════════════════════════════════════════
#  G1 — composite mass peaks at the saturation edge
# ════════════════════════════════════════════════════════════════════
mH = np.sin(2 * phis)
peak_deg = math.degrees(phis[int(np.argmax(mH))])
record("G1_composite_mass_peaks_at_45",
       abs(peak_deg - 45.0) < 1e-2 and abs(mH.max() - 1.0) < 1e-12,
       {"argmax_phi_deg": round(peak_deg, 4), "m_H_max": round(float(mH.max()), 8),
        "note": "m_H = sin(2 phi) is maximal exactly at the saturation edge "
                "2 phi = pi/2"})


# ════════════════════════════════════════════════════════════════════
#  G2 — the energy-minimum LOCATION is coupling-independent
#       E(phi) = E0 - lambda sin(2 phi), lambda>0  ->  min at 45deg for all lambda
# ════════════════════════════════════════════════════════════════════
locs = {}
ok_G2 = True
for lam in [1e-6, 1e-3, 1.0, 1e3, 1e6]:
    E = -lam * np.sin(2 * phis)
    loc = math.degrees(phis[int(np.argmin(E))])
    locs[f"lambda={lam:g}"] = round(loc, 4)
    ok_G2 = ok_G2 and abs(loc - 45.0) < 1e-2
# also analytic: dE/dphi = -2 lambda cos(2 phi) = 0 -> phi=45; d2E/dphi2=4 lambda>0 (min)
record("G2_minimum_location_coupling_independent", ok_G2,
       {"argmin_phi_deg_vs_lambda": locs,
        "analytic": "dE/dphi=-2 lambda cos(2 phi)=0 -> phi=45 ; "
                    "d2E/dphi2=4 lambda sin(2 phi)=4 lambda>0 -> minimum",
        "payoff": "the 45deg LOCATION does not depend on the coupling "
                  "strength -> F80-D5's '340x too weak' sets the DEPTH, not "
                  "the location; even infinitesimal binding lands at 45deg"})


# ════════════════════════════════════════════════════════════════════
#  G3 — exact 45deg <=> flat direction (kappa=0)
#       E(phi) = kappa phi^2/2 - lambda sin(2 phi)
# ════════════════════════════════════════════════════════════════════
lam = 1.0
kappa_scan = {}
for kappa in [0.0, 0.25, 0.5, 1.0, 2.0, 5.0]:
    E = 0.5 * kappa * phis ** 2 - lam * np.sin(2 * phis)
    kappa_scan[f"kappa={kappa:g}"] = round(math.degrees(phis[int(np.argmin(E))]), 3)
flat_at_45 = abs(kappa_scan["kappa=0"] - 45.0) < 1e-2
moves_below = (kappa_scan["kappa=0.5"] < 45.0 and kappa_scan["kappa=2"] < kappa_scan["kappa=0.5"])
record("G3_exact_45_iff_flat_direction",
       flat_at_45 and moves_below,
       {"argmin_phi_deg_vs_kappa(lambda=1)": kappa_scan,
        "reading": "any stiffness kappa>0 favouring the democratic point pulls "
                   "the minimum BELOW 45deg; the observed EXACT 45deg is "
                   "evidence that phi is a flat direction (kappa=0) -- a free "
                   "lattice background (F76), not a paid-for distortion"})


# ════════════════════════════════════════════════════════════════════
#  G4 — Q monotonic in binding; clean two-body pairs have Q <= 2/3
# ════════════════════════════════════════════════════════════════════
def Q_of_mH(m):
    phi = 0.5 * math.asin(max(0.0, min(1.0, m)))
    return 1.0 / (3.0 * math.cos(phi) ** 2)


Qcurve = {f"m_H={m}": round(Q_of_mH(m), 5) for m in [0.0, 0.25, 0.5, 0.75, 0.9, 1.0]}
mono = all(Q_of_mH(m2) >= Q_of_mH(m1)
           for m1, m2 in zip([0, .25, .5, .75, .9], [.25, .5, .75, .9, 1.0]))
bounded = abs(Q_of_mH(0.0) - 1 / 3) < 1e-9 and abs(Q_of_mH(1.0) - 2 / 3) < 1e-9
# sector contrast
Q_lep = 0.666660511465522
up = [2.16, 1270.0, 172690.0]
down = [4.67, 93.4, 4180.0]


def koideQ(v):
    v = np.sqrt(np.abs(np.array(v, float)))
    return float((v ** 2).sum() / (v.sum() ** 2))


Q_up, Q_down = koideQ(up), koideQ(down)
record("G4_Q_monotonic_in_binding",
       mono and bounded and Q_up > 2 / 3 and Q_down > 2 / 3,
       {"Q(m_H)_curve": Qcurve,
        "massless->democratic": round(Q_of_mH(0.0), 5),
        "maximally_bound->equipartition": round(Q_of_mH(1.0), 5),
        "clean_two_body_bound": "Q in [1/3, 2/3]; charged leptons saturate at 2/3",
        "Q_leptons": round(Q_lep, 5),
        "Q_up_quarks": round(Q_up, 3), "Q_down_quarks": round(Q_down, 3),
        "quark_note": "Q_quark > 2/3 lies OUTSIDE the clean-pair band -> quarks "
                      "are not clean two-body pairs (QCD/confinement), as "
                      "expected"})


# ════════════════════════════════════════════════════════════════════
#  G5 — honest residual
# ════════════════════════════════════════════════════════════════════
RESULTS["G5_honest_residual"] = {
    "answered": "WHY at saturation: the composite mass m_H=sin(2 phi) peaks at "
                "the saturation edge, and a binding energy E0 - lambda*m_H is "
                "minimised there for ANY lambda>0. The lepton sits where its "
                "own mass is maximal; coupling strength sets the depth, not the "
                "45deg location -> the F80-D5 weakness objection dissolves.",
    "remaining_assumption": "phi is a FLAT direction (no stiffness kappa>0 "
                            "favouring the democratic point). Supported by the "
                            "data sitting at EXACTLY 45deg (G3: any kappa>0 "
                            "would put it below). Plausibly the orthorhombic "
                            "lattice anisotropy (F76) is a free background.",
    "net": "the residual is now 'why is the generation-rotation a flat modulus' "
           "-- a structural lattice question -- rather than 'why criticality' "
           "or 'why isn't EM too weak'.",
}
print("[info] G5:", RESULTS["G5_honest_residual"]["answered"][:90], "...")


print("\nOVERALL:", "PASS" if PASS else "FAIL")
RESULTS["_overall"] = "PASS" if PASS else "FAIL"
outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test-results"))
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F82_saturation_mass_peak.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
print("wrote", os.path.join(outdir, "F82_saturation_mass_peak.json"))
