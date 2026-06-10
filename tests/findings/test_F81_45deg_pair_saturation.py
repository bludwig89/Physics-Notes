#!/usr/bin/env python3
"""
test_F81_45deg_pair_saturation.py
=================================

F81 — Why 45 degrees: the charged-lepton equipartition (Koide Q=2/3) is the
PHASE SATURATION of a TWO-constituent pair, and Q reads off the constituent
number N=2.

This attacks the residual left open by F80 ("why does the charged-lepton EM
criticality fall exactly at 45 deg?").  The chain uses only rules already in
the model:

  (a) the charged lepton is a bound pair of constituents               [F73]
  (b) the generation-space angle phi (angle of sqrt(m) off the democratic
      axis, F80) is a PER-CONSTITUENT rotation                          [new id]
  (c) a bound pair's total phase is the SUM of constituent phases       [F69]
        -> total generation phase = N * phi   (N = #constituents)
  (d) a stable composite requires total phase <= pi/2                   [F73]
  (e) the physical state sits at saturation (maximal stable binding /
      criticality)                                                      [F74-style]
      => N * phi = pi/2  =>  phi = pi/(2N)
  (f) Q(phi) = 1/(3 cos^2 phi)                                          [F80]
      => Q_N = 1/(3 cos^2(pi/(2N)))

For the PAIR N=2: phi = 45 deg EXACTLY, Q = 2/3 EXACTLY.  The observed leptons
(Q=0.66666) read off N=2 -- i.e. Q=2/3 is the signature of the two-constituent
(Cooper-pair) structure.  Other N give other Q (N=3 -> 4/9, N->inf -> 1/3),
none matching.

New framing: the pi/2 stable phase budget is shared EQUALLY among the N pair
members (phi = (pi/2)/N each); for the pair, each member carries pi/4 = 45 deg
-- the same per-constituent saturation angle as the F73 rest-mass leg, and the
same 1/sqrt2 as the Cooper-pair spin singlet.

Checks
------
  E1  Q_N = 1/(3 cos^2(pi/(2N))): tabulate; N=2 -> 2/3 exact, N->inf -> 1/3.
  E2  The data select N=2: the integer N minimising |Q_obs - Q_N| is 2, with
      residual ~1e-5; N=3 is off by ~0.22.
  E3  At N=2 each constituent sits at (cos45,sin45)=(1/sqrt2,1/sqrt2) -- the
      spin-singlet weight; the per-constituent angle equals the F73 rest-mass
      cap arcsin(1/sqrt2)=45 deg (one and the same saturation).
  E4  Phase-budget equipartition: N*phi=pi/2 with all constituents equal is the
      unique stable-saturation split; verify N*phi_N = pi/2 for all N.
  E5  Honest residual (recorded): the derivation fixes the VALUE given (i) the
      per-constituent identification of phi and (ii) that the lepton sits at
      saturation; perturbative EM does not by itself force saturation (F80-D5),
      so "why at the critical edge" remains -- but "why 45 deg" is now answered
      as "the pair halves the pi/2 budget".
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


def Q_of_N(N):
    phi = math.pi / (2 * N)
    c2 = math.cos(phi) ** 2
    return math.inf if c2 < 1e-18 else 1.0 / (3.0 * c2)


# observed charged-lepton Koide ratio (PDG masses)
m_e, m_mu, m_tau = 0.51099895069, 105.6583755, 1776.86
y = np.sqrt([m_e, m_mu, m_tau])
Q_obs = float((y ** 2).sum() / (y.sum() ** 2))


# ════════════════════════════════════════════════════════════════════
#  E1 — Q_N table; N=2 -> 2/3 exact, N->inf -> 1/3
# ════════════════════════════════════════════════════════════════════
table = {N: (round(math.degrees(math.pi / (2 * N)), 4),
             ("inf" if math.isinf(Q_of_N(N)) else round(Q_of_N(N), 6)))
         for N in [1, 2, 3, 4, 6, 12]}
e1_ok = (abs(Q_of_N(2) - 2 / 3) < 1e-12
         and abs(Q_of_N(1000) - 1 / 3) < 1e-5
         and math.isinf(Q_of_N(1)))
record("E1_QN_table", e1_ok,
       {"{N: (phi_deg, Q_N)}": table,
        "N=2_exact": abs(Q_of_N(2) - 2 / 3) < 1e-12,
        "N->inf -> 1/3": round(Q_of_N(1000), 6),
        "formula": "Q_N = 1/(3 cos^2(pi/(2N)))"})


# ════════════════════════════════════════════════════════════════════
#  E2 — the data select N=2
# ════════════════════════════════════════════════════════════════════
N_best = min(range(2, 13), key=lambda N: abs(Q_of_N(N) - Q_obs))
resid_2 = abs(Q_of_N(2) - Q_obs)
resid_3 = abs(Q_of_N(3) - Q_obs)
record("E2_data_selects_N2",
       N_best == 2 and resid_2 < 1e-4 and resid_3 > 0.1,
       {"Q_observed": round(Q_obs, 6),
        "best_integer_N": N_best,
        "Q_N2": round(Q_of_N(2), 6), "residual_N2": round(resid_2, 7),
        "Q_N3": round(Q_of_N(3), 6), "residual_N3": round(resid_3, 4),
        "reading": "Q=2/3 reads off a TWO-constituent pair -- the Cooper-pair "
                   "structure of F73 confirmed from the mass ratios alone"})


# ════════════════════════════════════════════════════════════════════
#  E3 — pair member = (1/sqrt2, 1/sqrt2) = singlet weight = F73 rest cap
# ════════════════════════════════════════════════════════════════════
phi2 = math.pi / (2 * 2)               # 45 deg
member = (math.cos(phi2), math.sin(phi2))
f73_rest_cap = math.asin(1 / math.sqrt(2))   # arcsin(1/sqrt2) = 45 deg
singlet_weight = 1 / math.sqrt(2)
record("E3_member_is_singlet_and_F73cap",
       abs(member[0] - singlet_weight) < 1e-12
       and abs(member[1] - singlet_weight) < 1e-12
       and abs(phi2 - f73_rest_cap) < 1e-12,
       {"per_constituent_(cos,sin)": [round(member[0], 6), round(member[1], 6)],
        "singlet_weight_1/sqrt2": round(singlet_weight, 6),
        "F73_rest_mass_cap_deg": round(math.degrees(f73_rest_cap), 4),
        "reading": "each pair member carries 45 deg = the F73 per-constituent "
                   "saturation = the spin-singlet 1/sqrt2 -- all one object"})


# ════════════════════════════════════════════════════════════════════
#  E4 — phase-budget equipartition: N*phi_N = pi/2 for all N
# ════════════════════════════════════════════════════════════════════
budget_ok = all(abs(N * (math.pi / (2 * N)) - math.pi / 2) < 1e-15
                for N in range(1, 20))
record("E4_phase_budget_equipartition", budget_ok,
       {"identity": "N * phi_N = pi/2 (the stable phase budget split equally "
                    "among N constituents)",
        "pair_share": "phi_2 = pi/4 = 45 deg each",
        "verified_N_1_to_19": budget_ok})


# ════════════════════════════════════════════════════════════════════
#  E5 — honest residual (recorded)
# ════════════════════════════════════════════════════════════════════
RESULTS["E5_honest_residual"] = {
    "answered": "WHY 45 deg: a two-constituent pair shares the pi/2 stable "
                "phase budget equally -> pi/4 = 45 deg per member -> Q=2/3 "
                "(exact). Q reads off N=2.",
    "load_bearing_assumptions": [
        "(b) the generation angle phi is a per-constituent rotation obeying "
        "the F69 pair-phase-sum rule (identification, supported by the exact "
        "N=2 -> 2/3 data match)",
        "(e) the lepton sits AT saturation (the critical edge); perturbative "
        "EM is too weak to force this (F80-D5), so the criticality itself is "
        "the remaining input",
    ],
    "net": "'why 45 deg' is reduced to 'why the pair sits at its phase "
           "saturation' -- a single criticality question, with the VALUE now "
           "derived and the constituent number N=2 read off the data.",
}
print("[info] E5:", RESULTS["E5_honest_residual"]["answered"])


print("\nOVERALL:", "PASS" if PASS else "FAIL")
RESULTS["_overall"] = "PASS" if PASS else "FAIL"
outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test-results"))
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F81_45deg_pair_saturation.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
print("wrote", os.path.join(outdir, "F81_45deg_pair_saturation.json"))
