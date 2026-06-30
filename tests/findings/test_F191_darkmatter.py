"""
test_F191_darkmatter.py  --  Rotation curves & Bullet-Cluster test (S8, speculative)
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
SIM = os.path.join(ROOT, "ca-simulation")
if SIM not in sys.path: sys.path.insert(0, SIM)
import ca_darkmatter as dm   # noqa: E402
STAMP = "2026-06-30 - 04:45"


def check_D1_rotation_curves():
    rc = dm.rotation_curves()
    # baryons alone fall; both a dark halo AND modified gravity flatten the curve
    ok = (rc["baryon_falloff"] < 0.7 and rc["nfw_flatness"] > 0.85
          and rc["mond_flatness"] > 0.85)
    return {"pass": bool(ok), "baryon_falloff": rc["baryon_falloff"],
            "nfw_flatness": rc["nfw_flatness"], "mond_flatness": rc["mond_flatness"],
            "note": "rotation curves alone cannot separate dark halo from modified gravity"}


def check_D2_bullet_cluster():
    bc = dm.bullet_cluster()
    # the make-or-break test: lensing (mass) peak offset from the gas (X-ray) peak
    ok = (bc["lensing_gas_offset_mpc"] > 0.1
          and abs(bc["xray_gas_peak_mpc"]) < 0.1)      # gas centred
    return {"pass": bool(ok), "lensing_gas_offset_mpc": bc["lensing_gas_offset_mpc"],
            "xray_gas_peak_mpc": bc["xray_gas_peak_mpc"],
            "lensing_peaks_mpc": bc["lensing_peaks_mpc"],
            "verdict": "lensing offset from gas -> dark SOURCE favoured over pure dielectric reweighting"}


def check_D3_consistency_statement():
    # documents the catalog conclusion: GR + constant G needs a dark source;
    # the dielectric responds to it (it is not itself the dark matter).
    rc = dm.rotation_curves()
    needs_dark = rc["baryon_falloff"] < 0.7        # visible matter insufficient
    return {"pass": bool(needs_dark),
            "baryons_insufficient": bool(needs_dark),
            "conclusion": "under F178 exact GR, missing mass requires a dark gravitating source"}


SUITE = [("D1_rotation_curves", check_D1_rotation_curves, "baryons fall; halo & MOND both flatten"),
         ("D2_bullet_cluster", check_D2_bullet_cluster, "lensing peak offset from gas -> dark source"),
         ("D3_needs_dark_source", check_D3_consistency_statement, "GR+const G needs a dark source")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F191", "title": "Galactic rotation curves & the Bullet-Cluster test (dark-matter assessment)",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F191_darkmatter.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
