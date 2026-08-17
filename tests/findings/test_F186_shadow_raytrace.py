"""
test_F186_shadow_raytrace.py  --  BH shadow ray-tracer + mu-as predictions (S3)
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import raytrace as rt   # noqa: E402
STAMP = "2026-06-30 - 04:20"


def check_T1_numeric_bc():
    bc = rt.numeric_shadow_b(M=1.0)
    return {"pass": bool(abs(bc - 3*np.sqrt(3)) < 1e-3),
            "b_c_numeric": bc, "3sqrt3": 3*np.sqrt(3)}


def check_T2_eht_uas():
    p = rt.eht_predictions()
    m87, sgr = p["M87*"], p["SgrA*"]
    # GR shadow smaller than F114; both in EHT ballpark (M87 ring 42+-3, SgrA 51.8+-2.3)
    ok = (m87["shadow_uas_GR"] < m87["shadow_uas_F114"]
          and 35 < m87["shadow_uas_GR"] < 43
          and 48 < sgr["shadow_uas_GR"] < 56
          and abs(m87["F114_enlargement_pct"] - 4.63) < 0.05)
    return {"pass": bool(ok), "M87_GR_uas": m87["shadow_uas_GR"],
            "M87_F114_uas": m87["shadow_uas_F114"], "SgrA_GR_uas": sgr["shadow_uas_GR"],
            "F114_enlargement_pct": m87["F114_enlargement_pct"]}


def check_T3_kerr_spin_shadow():
    k = rt.kerr_shadow_extents()
    offs = [abs(k[f"a={a}"]["offset_M"]) for a in (0.3, 0.6, 0.9, 0.998)]
    grows = all(offs[i] < offs[i+1] for i in range(len(offs)-1))
    return {"pass": bool(grows and offs[-1] > offs[0]),
            "offsets_by_spin": offs, "grows_with_spin": bool(grows)}


SUITE = [("T1_numeric_b_crit", check_T1_numeric_bc, "ray-traced b_c = 3sqrt3 M"),
         ("T2_eht_microarcsec", check_T2_eht_uas, "M87*/SgrA* GR shadow vs F114 (+4.63%)"),
         ("T3_kerr_spin_shadow", check_T3_kerr_spin_shadow, "shadow displacement grows with spin")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F186", "title": "BH shadow ray-tracer + EHT mu-as predictions",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F186_shadow_raytrace.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
