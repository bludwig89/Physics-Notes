#!/usr/bin/env python3
"""F-new: medium-Z (Sc-Zn, Z=21-30) SCF IE sweep, appends to JSON incrementally.
Uses tighter density mixing (mix=0.2, max_iter=150) than the F208 default
(mix=0.4, max_iter=60) because plain-Aufbau atoms with near-degenerate 4s/3d
orbitals (late 3d series) don't converge under the light-element defaults.
Usage: python3 sweep_ie_medZ.py Zlo Zhi [--force]"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "src"))
from casim.engine.core import manybody as mb

NIST = {21: 6.5615, 22: 6.8281, 23: 6.7462, 24: 6.7665, 25: 7.43402,
        26: 7.9024, 27: 7.8810, 28: 7.6398, 29: 7.72638, 30: 9.3942}
SYM = {21:"Sc",22:"Ti",23:"V",24:"Cr",25:"Mn",26:"Fe",27:"Co",28:"Ni",29:"Cu",30:"Zn"}

OUT = os.path.join(HERE, "sweep_ie_medZ_rows.json")
force = "--force" in sys.argv
argv = [a for a in sys.argv[1:] if a != "--force"]
lo, hi = int(argv[0]), int(argv[1])
rows = json.load(open(OUT)) if os.path.exists(OUT) else []
if force:
    rows = [r for r in rows if r["Z"] < lo or r["Z"] > hi]
have = {r["Z"] for r in rows}
for Z in range(lo, hi + 1):
    if Z in have:
        continue
    t0 = time.time()
    r = mb.electron_cloud_hartree(Z, N=900, relativistic=True,
                                   max_iter=150, mix=0.2, tol=1e-6)
    levels = r["orbital_energies_eV"]
    homo = max(levels, key=levels.get)
    row = {
        "Z": Z, "sym": SYM[Z], "homo": list(homo),
        "configuration": r["configuration"],
        "ie_nr": r["ionization_eV"], "ie_rel": r["ionization_eV_rel"],
        "nist": NIST[Z],
        "err_nr_pct": 100 * (r["ionization_eV"] - NIST[Z]) / NIST[Z],
        "err_rel_pct": 100 * (r["ionization_eV_rel"] - NIST[Z]) / NIST[Z],
        "homo_rel_shift_meV": 1000 * (r["ionization_eV_rel"] - r["ionization_eV"]),
        "core_1s_rel_shift_eV": r["core_1s_rel_shift_eV"],
        "converged": r["converged"],
        "scf_params": {"max_iter": 150, "mix": 0.2, "tol": 1e-6},
    }
    rows.append(row)
    print(f"Z={Z} {SYM[Z]:>2} cfg={r['configuration']} IE_nr={r['ionization_eV']:.3f} "
          f"err={row['err_nr_pct']:+.1f}% dRel={row['homo_rel_shift_meV']:.3f}meV "
          f"1score={r['core_1s_rel_shift_eV']:.3f}eV conv={r['converged']} "
          f"t={time.time()-t0:.1f}s", flush=True)
    rows.sort(key=lambda x: x["Z"])
    json.dump(rows, open(OUT, "w"), indent=2)
print("have Z=", sorted(x['Z'] for x in rows))
