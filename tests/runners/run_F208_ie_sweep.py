#!/usr/bin/env python3
"""Range-based SCF IE sweep that APPENDS to a persistent JSON (so it can run in
sub-45s chunks).  Usage: python3 sweep_chunk.py Zlo Zhi"""
import os, sys, json
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.core import manybody as mb

NIST = {1: 13.59844, 2: 24.58738, 3: 5.39171, 4: 9.32269, 5: 8.29803,
        6: 11.26030, 7: 14.53414, 8: 13.61806, 9: 17.42282, 10: 21.5646,
        11: 5.13908, 12: 7.64624, 13: 5.98577, 14: 8.15169, 15: 10.48669,
        16: 10.36001, 17: 12.96764, 18: 15.75962, 19: 4.34066, 20: 6.11316}
SYM = {1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",9:"F",10:"Ne",
       11:"Na",12:"Mg",13:"Al",14:"Si",15:"P",16:"S",17:"Cl",18:"Ar",
       19:"K",20:"Ca"}
OUT = "/sessions/jolly-upbeat-meitner/mnt/Physics Notes/outputs/sweep_ie_rows.json"

rows = []
if os.path.exists(OUT):
    rows = json.load(open(OUT))
have = {r["Z"] for r in rows}
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for Z in range(lo, hi + 1):
    if Z in have:
        continue
    r = mb.electron_cloud_hartree(Z, N=900, relativistic=True)
    levels = r["orbital_energies_eV"]
    homo = max(levels, key=levels.get)
    rows.append({
        "Z": Z, "sym": SYM[Z], "homo": list(homo),
        "ie_nr": r["ionization_eV"], "ie_rel": r["ionization_eV_rel"],
        "nist": NIST[Z],
        "err_nr_pct": 100 * (r["ionization_eV"] - NIST[Z]) / NIST[Z],
        "err_rel_pct": 100 * (r["ionization_eV_rel"] - NIST[Z]) / NIST[Z],
        "homo_rel_shift_meV": 1000 * (r["ionization_eV_rel"] - r["ionization_eV"]),
        "core_1s_rel_shift_eV": r["core_1s_rel_shift_eV"],
        "converged": r["converged"],
    })
    print(f"Z={Z} {SYM[Z]:>2} IE_nr={r['ionization_eV']:.3f} "
          f"err={100*(r['ionization_eV']-NIST[Z])/NIST[Z]:+.1f}% "
          f"dRel={1000*(r['ionization_eV_rel']-r['ionization_eV']):.3f}meV "
          f"1s={r['core_1s_rel_shift_eV']:.3f}eV", flush=True)
    rows.sort(key=lambda x: x["Z"])          # save incrementally
    json.dump(rows, open(OUT, "w"), indent=2)
print(f"have Z={sorted(x['Z'] for x in rows)}", flush=True)
