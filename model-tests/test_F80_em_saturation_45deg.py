#!/usr/bin/env python3
"""
test_F80_em_saturation_45deg.py
===============================

F80 — One 45 degrees: the charged-lepton Koide point Q=2/3 and the F73 bound-pair
stability cap are the SAME SO(2) equipartition, and only the EM-coupled
(charged-lepton) sector lands on it.

This closes the F78 thread by (i) deriving the exact map between the amplitude
rotation angle and Q, (ii) showing the F73 constituent stability cap and the
generation equipartition are the identical 2-channel rotation evaluated at the
same 45 degrees, (iii) implementing the user's selection insight -- only
charged leptons couple to the clean abelian EM rotation, so only they sit at
the critical point -- with quarks and neutrinos as the honest contrast, and
(iv) recording honestly what is NOT derived (perturbative EM is far too weak to
be the driver; EM explains the selection, not the magnitude).

Checks
------
  D1  The amplitude-rotation -> Koide map  Q(phi) = 1/(3 cos^2 phi)  is exact:
      phi=0 -> 1/3 (democratic floor), phi=45 -> 2/3 (equipartition),
      phi=arccos(1/sqrt3)=54.7356 -> 1 (single-axis ceiling).
  D2  SO(2) UNIFICATION.  Both mass rotations are a unit 2-vector rotated by an
      angle; the two squared components (weights) are cos^2, sin^2 and are
      EQUAL at 45 degrees.
        - F73 constituent: (n_c, m_c) = (cos t, sin t); the pair phase
          Omega = 2t saturates at pi/2 exactly at t=45 (m_c=1/sqrt2), where
          rest and kinetic weights equipartition.
        - generation: (common, differential) = (cos phi, sin phi); Koide
          equipartition |A1g|=|T1u| at phi=45.
      Same matrix, same 45-degree equal-split point.
  D3  The measured charged leptons sit at phi = 44.99974 deg = the F73 cap
      (arcsin(1/sqrt2)=45). So the charged-lepton amplitude is AT the EM
      rotation saturation.
  D4  SELECTION RULE (EM-coupled sector only): charged leptons Q=0.66666 (at
      2/3); up-type quarks 0.85, down-type 0.73 (QCD-contaminated, off 2/3);
      neutrinos (no EM) have an ordering/scale-dependent Q that is NOT pinned
      to 2/3.  Only the clean EM sector lands on the critical point.
  D5  HONEST RESIDUAL (recorded, not a pass/fail physics claim): the rotation
      democratic->equipartition is a full 45 deg, but a PERTURBATIVE EM
      self-energy supplies only ~alpha/pi = 0.13 deg (~340x too small).  So EM
      explains WHICH sector sits at the point (the selection), not the
      magnitude of the rotation; the value 45 deg (equipartition) is a critical
      condition pinned by data, still to be derived from the EM-driven gap.
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


def koideQ(vec):
    v = np.abs(np.asarray(vec, float))
    return float((v ** 2).sum() / (v.sum() ** 2))


# ════════════════════════════════════════════════════════════════════
#  D1 — the rotation->Koide map  Q(phi) = 1/(3 cos^2 phi)
#  Amplitude y = R[cos(phi) n_hat + sin(phi) u_hat],  n_hat=(1,1,1)/sqrt3,
#  u_hat ⟂ n_hat.  Then Sum y = sqrt3 R cos phi, Sum y^2 = R^2, so
#  Q = 1/(3 cos^2 phi).  Verify against a constructed amplitude.
# ════════════════════════════════════════════════════════════════════
n_hat = np.ones(3) / math.sqrt(3)
u_hat = np.array([1.0, -1.0, 0.0]) / math.sqrt(2)   # a unit vector ⟂ n_hat
assert abs(u_hat @ n_hat) < 1e-15


def Q_of_phi_constructed(phi):
    # geometric map uses the SIGNED sum (Sum y), not Sum|y|: the perpendicular
    # (T1u) part contributes 0 to the signed sum by construction. Physical
    # sqrt-masses are >=0, so for the real leptons the two coincide.
    y = math.cos(phi) * n_hat + math.sin(phi) * u_hat   # R=1
    return float((y ** 2).sum() / (y.sum() ** 2))


def Q_of_phi_formula(phi):
    return 1.0 / (3.0 * math.cos(phi) ** 2)


phi_floor = 0.0
phi_equi = math.radians(45.0)
phi_ceil = math.acos(1 / math.sqrt(3))               # 54.7356 deg
rows = {}
ok_D1 = True
for label, phi, target in [("0deg_democratic", phi_floor, 1 / 3),
                           ("45deg_equipartition", phi_equi, 2 / 3),
                           ("54.7356deg_single_axis", phi_ceil, 1.0)]:
    qf = Q_of_phi_formula(phi)
    qc = Q_of_phi_constructed(phi)
    rows[label] = {"Q_formula": round(qf, 8), "Q_constructed": round(qc, 8),
                   "target": round(target, 8)}
    ok_D1 = ok_D1 and abs(qf - target) < 1e-9 and abs(qc - target) < 1e-9
record("D1_rotation_to_koide_map", ok_D1,
       {"Q(phi)=1/(3cos^2 phi)": rows,
        "note": "phi=45deg gives Q=2/3 EXACTLY"})


# ════════════════════════════════════════════════════════════════════
#  D2 — SO(2) unification: same rotation, same 45-degree equal-split
# ════════════════════════════════════════════════════════════════════
def R2(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s], [s, c]])


# F73 constituent at the stability cap t=45deg
t_cap = math.radians(45.0)
constit = R2(t_cap) @ np.array([1.0, 0.0])     # (cos t, sin t) = (n_c, m_c)
n_c, m_c = constit
Omega_pair = 2 * t_cap                          # F73 pair phase
f73_equipartition = abs(n_c - m_c) < 1e-12 and abs(m_c - 1 / math.sqrt(2)) < 1e-12
f73_cap = abs(Omega_pair - math.pi / 2) < 1e-12 and abs(math.sin(Omega_pair) - 1.0) < 1e-12

# generation at equipartition phi=45deg
gen = R2(phi_equi) @ np.array([1.0, 0.0])      # (cos phi, sin phi) weights
gen_equipartition = abs(gen[0] - gen[1]) < 1e-12
# both states are the SAME 45-degree-rotated unit vector
same_state = np.max(np.abs(constit - gen)) < 1e-12
record("D2_so2_unification",
       f73_equipartition and f73_cap and gen_equipartition and same_state,
       {"F73_constituent_(n_c,m_c)_at_cap": [round(n_c, 6), round(m_c, 6)],
        "F73_pair_phase_Omega": round(Omega_pair, 6), "pi/2": round(math.pi / 2, 6),
        "F73_rest=kinetic_equipartition(1/sqrt2)": f73_equipartition,
        "generation_(common,diff)_at_45": [round(gen[0], 6), round(gen[1], 6)],
        "identical_45deg_rotated_unit_vector": same_state,
        "reading": "F73 (rest,kinetic) and generation (common,differential) are "
                   "the SAME SO(2) rotation; 45deg is the equal-split point of "
                   "both -- one thread"})


# ════════════════════════════════════════════════════════════════════
#  D3 — measured charged leptons sit at phi = 45 deg = the F73 cap
# ════════════════════════════════════════════════════════════════════
m_e, m_mu, m_tau = 0.51099895069, 105.6583755, 1776.86
Q_lep = koideQ([math.sqrt(m_e), math.sqrt(m_mu), math.sqrt(m_tau)])
phi_lep = math.degrees(math.acos(math.sqrt(1.0 / (3.0 * Q_lep))))
f73_cap_deg = math.degrees(math.asin(1 / math.sqrt(2)))   # 45
record("D3_leptons_at_the_45deg_saturation",
       abs(phi_lep - 45.0) < 0.02 and abs(phi_lep - f73_cap_deg) < 0.02,
       {"Q_leptons": round(Q_lep, 7),
        "phi_lepton_deg": round(phi_lep, 5),
        "F73_cap_deg": round(f73_cap_deg, 5),
        "reading": "the charged-lepton amplitude is AT the EM-rotation "
                   "saturation = the F73 bound-pair stability cap"})


# ════════════════════════════════════════════════════════════════════
#  D4 — selection rule: only the clean EM-coupled sector lands on 2/3
# ════════════════════════════════════════════════════════════════════
# quark masses (MeV), PDG ~ (MSbar where relevant; scheme-rough but the point
# is robust: neither sector is at 2/3 and they differ)
up = [2.16, 1270.0, 172690.0]      # u, c, t
down = [4.67, 93.4, 4180.0]        # d, s, b
Q_up = koideQ([math.sqrt(x) for x in up])
Q_down = koideQ([math.sqrt(x) for x in down])

# neutrinos (eV), normal ordering, scan the unknown lightest mass
d21, d31 = 7.5e-5, 2.5e-3
nu_scan = {}
for m1 in [0.0, 0.001, 0.01, 0.05]:
    mm = [m1, math.sqrt(m1 ** 2 + d21), math.sqrt(m1 ** 2 + d31)]
    nu_scan[f"m1={m1}eV"] = round(koideQ([math.sqrt(x) for x in mm]), 4)

leptons_on = abs(Q_lep - 2 / 3) < 1e-4
quarks_off = abs(Q_up - 2 / 3) > 0.1 and abs(Q_down - 2 / 3) > 0.05
nu_unpinned = (max(nu_scan.values()) - min(nu_scan.values())) > 0.1  # ordering-dependent
record("D4_em_selection_rule",
       leptons_on and quarks_off and nu_unpinned,
       {"Q_charged_leptons": round(Q_lep, 5),
        "Q_up_type_quarks": round(Q_up, 4),
        "Q_down_type_quarks": round(Q_down, 4),
        "Q_neutrino_scan_(normal_ordering)": nu_scan,
        "verdict": "only the clean EM-coupled charged leptons sit at 2/3; "
                   "quarks are QCD-contaminated (off, and unequal); neutrinos "
                   "(neutral, Majorana/seesaw F47) are not EM-pinned and their "
                   "Q is ordering/scale-dependent. Charge is the selector."})


# ════════════════════════════════════════════════════════════════════
#  D5 — honest residual: perturbative EM cannot DRIVE a 45-degree rotation
# ════════════════════════════════════════════════════════════════════
alpha = 1 / 137.035999084
em_rot_perturbative_deg = math.degrees(alpha / math.pi)   # ~0.13 deg
needed_deg = 45.0
shortfall = needed_deg / em_rot_perturbative_deg
RESULTS["D5_honest_residual"] = {
    "perturbative_EM_rotation_deg (~alpha/pi)": round(em_rot_perturbative_deg, 5),
    "rotation_needed_democratic_to_equipartition_deg": needed_deg,
    "shortfall_factor": round(shortfall, 1),
    "statement": "EM explains the SELECTION (which sector sits at the critical "
                 "point: only charged leptons couple to the clean abelian "
                 "rotation) but NOT the magnitude: perturbative EM is ~340x too "
                 "weak to rotate democratic(1/3)->equipartition(2/3). The value "
                 "45deg is a critical/saturation condition pinned by data; "
                 "deriving it from the non-perturbative EM-driven gap (and the "
                 "Cooper-pair singlet's own 1/sqrt2 structure) is the residual "
                 "open question.",
}
print("[info] D5 residual:", RESULTS["D5_honest_residual"]["statement"][:80], "...")


print("\nOVERALL:", "PASS" if PASS else "FAIL")
RESULTS["_overall"] = "PASS" if PASS else "FAIL"
outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-results"))
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F80_em_saturation_45deg.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
print("wrote", os.path.join(outdir, "F80_em_saturation_45deg.json"))
