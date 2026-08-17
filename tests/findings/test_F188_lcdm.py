"""
test_F188_lcdm.py  --  Multi-component (LCDM) cosmology under the full tensor (S5)
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import cosmology as cc   # noqa: E402
STAMP = "2026-06-30 - 04:30"


def check_L1_timeline():
    s = cc.lcdm_summary()
    ok = (3000 < s["z_eq_matter_radiation"] < 3700
          and 0.5 < s["z_acceleration_onset"] < 0.8
          and 13.0 < s["age_gyr"] < 14.5)
    return {"pass": bool(ok), "z_eq": s["z_eq_matter_radiation"],
            "z_acc": s["z_acceleration_onset"], "age_gyr": s["age_gyr"]}


def check_L2_acceleration_sign():
    # full-tensor a''/a: decelerating in matter/radiation era (small a), accelerating now
    a_early = cc.accel_over_a_lcdm(1e-3)      # radiation/matter dominated
    a_now = cc.accel_over_a_lcdm(1.0)         # today
    a_future = cc.accel_over_a_lcdm(3.0)      # Lambda dominated
    ok = a_early < 0 < a_now and a_future > a_now
    return {"pass": bool(ok), "accel_early": a_early, "accel_now": a_now,
            "accel_future": a_future,
            "note": "pressure (rho+3p): radiation+matter decelerate, Lambda (w=-1) accelerates"}


def check_L3_normalization():
    # E(a=1) = 1 by construction (flat, Omegas sum to 1)
    E1 = cc.E_of_a(1.0)
    return {"pass": bool(abs(E1 - 1.0) < 1e-12), "E(1)": float(E1)}


SUITE = [("L1_cosmic_timeline", check_L1_timeline, "z_eq~3400, z_acc~0.63, age~13.8 Gyr"),
         ("L2_acceleration_sign", check_L2_acceleration_sign, "decelerate early, accelerate now (rho+3p)"),
         ("L3_flat_normalization", check_L3_normalization, "E(1)=1 (flat, sum Omega=1)")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F188", "title": "Multi-component LCDM cosmology under the full-tensor source",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F188_lcdm.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
