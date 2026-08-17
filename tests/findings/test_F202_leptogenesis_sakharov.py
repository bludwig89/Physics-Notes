"""
test_F202_leptogenesis_sakharov.py
==================================
F202 (part b) — can the model's intrinsic L-violation (F47) source the lepton
asymmetry resonant keV-DM production (F200) needs? Check the three Sakharov
conditions against the model's own structure.

5 checks:
  L1  L-violation present (F47 Majorana anti-linear) -> DERIVED.
  L2  CP violation available: 3-generation lepton sector has physical phases
      (1 Dirac + 2 Majorana); F53's single-gen J=0 is NOT a 3-gen no-go.
  L3  out-of-equilibrium + sphalerons: feeble sterile coupling + SU(2)_L sphalerons.
  L4  magnitude: the required late lepton asymmetry (~1e6 x Y_B) and the baryon
      asymmetry come from the SAME N_{2,3} sector at different epochs (ARS).
  L5  verdict: all Sakharov conditions met; CP phases + N_{2,3} degeneracy free.
"""
from __future__ import annotations
import json, os, sys, time
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
# Forks are loaded by bare name, not as package submodules;
# importing casim appends engine/forks/<sector>/ to sys.path.
import casim as _casim  # noqa: E402,F401
import gr_fork_F202_leptogenesis_sakharov as F202   # noqa: E402
STAMP = "2026-06-30 - 22:30"

OUT = F202.run()


def check_L1_L_violation():
    c = OUT["sakharov"]["1_L_violation"]
    return {"pass": bool(c["met"]), "source": c["source"], "status": c["status"],
            "note": "F47 Majorana step anti-linear -> intrinsic lepton-number violation"}


def check_L2_cp_available():
    c = OUT["sakharov"]["2_C_and_CP_violation"]
    cp = c["CP_three_generation"]
    ok = (c["C_maximal"] and cp["cp_available"] and cp["total_low_energy_phases"] >= 1)
    return {"pass": bool(ok), "C_maximal": c["C_maximal"],
            "dirac_phases": cp["pmns_dirac_phases"], "majorana_phases": cp["majorana_phases"],
            "note": "F53: C maximal; 3-gen (F75) lepton sector has 1 Dirac + 2 Majorana phases"}


def check_L3_out_of_equilibrium_and_sphalerons():
    c3 = OUT["sakharov"]["3_out_of_equilibrium"]
    conv = OUT["sakharov"]["conversion_L_to_B"]
    ok = (c3["met"] and conv["sphalerons_exist"])
    return {"pass": bool(ok), "out_of_equilibrium": c3["met"],
            "sphalerons": conv["sphalerons_exist"], "sphaleron_source": conv["source"],
            "note": "feeble sterile coupling -> freeze-in; SU(2)_L -> sphalerons convert L to B"}


def check_L4_magnitude_same_sector():
    r = OUT["asymmetry_reach"]
    ok = (r["both_from_same_sector"] and r["lepton_to_baryon_ratio"] > 1e3)
    return {"pass": bool(ok), "Y_B_observed": r["Y_B_observed"],
            "delta_L_over_s_for_resonant_DM": r["delta_L_over_s_for_resonant_DM"],
            "lepton_to_baryon_ratio": r["lepton_to_baryon_ratio"], "requires": r["requires"],
            "note": "baryon asymmetry (sphaleron freeze-out) + larger late lepton asymmetry both from N_{2,3}"}


def check_L5_verdict():
    return {"pass": bool(OUT["all_sakharov_met"]), "verdict": OUT["verdict"]}


SUITE = [
    ("L1_L_violation", check_L1_L_violation, "F47 Majorana -> intrinsic L-violation"),
    ("L2_cp_available", check_L2_cp_available, "3-gen CP phases available (F53/F75)"),
    ("L3_out_of_eq_sphalerons", check_L3_out_of_equilibrium_and_sphalerons, "out-of-eq + SU(2)_L sphalerons"),
    ("L4_magnitude_same_sector", check_L4_magnitude_same_sector, "baryon + lepton asymmetry from same N_{2,3}"),
    ("L5_verdict", check_L5_verdict, "all Sakharov conditions met"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F202",
            "title": "Leptogenesis from the model's intrinsic L-violation (F47) + 3-generation CP (F53/F75)",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "verdict": OUT["verdict"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F202_leptogenesis_sakharov_test.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
