#!/usr/bin/env python3
"""Sweep the multi-electron SCF across Z, compute non-relativistic and
relativistic (F125 Dirac-Coulomb) Koopmans ionization energies, compare to
CRC/NIST, and quantify where light-element accuracy breaks down."""
import os, sys, json
sys.path.insert(0, "/sessions/jolly-upbeat-meitner/mnt/Physics Notes/ca-simulation")
import ca_manybody as mb

# First ionization energies (eV) — CRC Handbook 84th ed. / NIST ASD
# (via en.wikipedia.org/wiki/Ionization_energies_of_the_elements_(data_page)).
NIST = {1: 13.59844, 2: 24.58738, 3: 5.39171, 4: 9.32269, 5: 8.29803,
        6: 11.26030, 7: 14.53414, 8: 13.61806, 9: 17.42282, 10: 21.5646,
        11: 5.13908, 12: 7.64624, 13: 5.98577, 14: 8.15169, 15: 10.48669,
        16: 10.36001, 17: 12.96764, 18: 15.75962, 19: 4.34066, 20: 6.11316}
SYM = {1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",9:"F",10:"Ne",
       11:"Na",12:"Mg",13:"Al",14:"Si",15:"P",16:"S",17:"Cl",18:"Ar",
       19:"K",20:"Ca"}

rows = []
for Z in range(1, 21):
    r = mb.electron_cloud_hartree(Z, relativistic=True)
    ie_nr = r["ionization_eV"]
    ie_rel = r["ionization_eV_rel"]
    nist = NIST[Z]
    rows.append({
        "Z": Z, "sym": SYM[Z],
        "homo": list(r["orbital_energies_eV"].keys())[
            list(r["orbital_energies_eV"].values()).index(
                max(r["orbital_energies_eV"].values()))],
        "ie_nr": ie_nr, "ie_rel": ie_rel, "nist": nist,
        "err_nr_pct": 100 * (ie_nr - nist) / nist,
        "err_rel_pct": 100 * (ie_rel - nist) / nist,
        "homo_rel_shift_meV": 1000 * (ie_rel - ie_nr),
        "core_1s_rel_shift_eV": r["core_1s_rel_shift_eV"],
        "converged": r["converged"],
    })

# quantify
import statistics as st
errs = [abs(x["err_nr_pct"]) for x in rows if x["Z"] > 1]   # exclude exact H
first_over5 = next((x["Z"] for x in rows if abs(x["err_nr_pct"]) > 5 and x["Z"] > 1), None)
first_over10 = next((x["Z"] for x in rows if abs(x["err_nr_pct"]) > 10 and x["Z"] > 1), None)
max_rel_shift = max(abs(x["homo_rel_shift_meV"]) for x in rows)
# Z^4 scaling check of the 1s core shift (use Ne..Ar where Z_eff~Z)
import math
def slope(a, b):
    return (math.log(abs(rows[b-1]["core_1s_rel_shift_eV"])) -
            math.log(abs(rows[a-1]["core_1s_rel_shift_eV"]))) / (math.log(b) - math.log(a))

summary = {
    "reference": "CRC Handbook 84th ed. / NIST ASD",
    "n_atoms": len(rows),
    "H_ie_nr": rows[0]["ie_nr"], "H_err_pct": rows[0]["err_nr_pct"],
    "mean_abs_err_nr_pct_Z2_20": st.mean(errs),
    "median_abs_err_nr_pct_Z2_20": st.median(errs),
    "max_abs_err_nr_pct": max(errs),
    "first_Z_over_5pct": first_over5,
    "first_Z_over_10pct": first_over10,
    "max_valence_rel_shift_meV": max_rel_shift,
    "core_1s_shift_Ne": rows[9]["core_1s_rel_shift_eV"],
    "core_1s_shift_Ar": rows[17]["core_1s_rel_shift_eV"],
    "core_1s_loglog_slope_Ne_Ar": slope(10, 18),
}

print(f"{'Z':>2} {'el':>3} {'HOMO':>7} {'IE_nr':>7} {'IE_rel':>7} {'NIST':>7} "
      f"{'e_nr%':>7} {'dRel_meV':>8} {'1s_eV':>8}")
for x in rows:
    print(f"{x['Z']:>2} {x['sym']:>3} {str(x['homo']):>7} {x['ie_nr']:7.3f} "
          f"{x['ie_rel']:7.3f} {x['nist']:7.3f} {x['err_nr_pct']:7.1f} "
          f"{x['homo_rel_shift_meV']:8.3f} {x['core_1s_rel_shift_eV']:8.3f}")
print("\nSUMMARY:", json.dumps(summary, indent=2))

with open("/sessions/jolly-upbeat-meitner/mnt/Physics Notes/outputs/sweep_ie.json", "w") as f:
    json.dump({"rows": rows, "summary": summary}, f, indent=2)
print("saved sweep_ie.json")
