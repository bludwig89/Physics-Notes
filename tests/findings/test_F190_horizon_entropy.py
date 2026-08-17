"""
test_F190_horizon_entropy.py  --  Lattice microstates & S=A/4 (S7, speculative)
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import horizon_entropy as he   # noqa: E402
STAMP = "2026-06-30 - 04:40"


def check_E1_per_cell_closed_form():
    s = he.summary(1.0)
    target = 2 * np.pi * np.sqrt(3)
    ok = (abs(s["s_per_cell"] - target) < 1e-9
          and abs(he.required_entropy_per_cell() - target) < 1e-9)
    return {"pass": bool(ok), "s_per_cell": s["s_per_cell"], "2pi_sqrt3": target,
            "microstates_per_cell": s["microstates_per_cell"],
            "note": "S=A/4 reproduced iff each F107 horizon cell carries 2 pi sqrt3 nats"}


def check_E2_area_law():
    a = he.area_law_check(1.0, 2.0)
    return {"pass": bool(abs(a["ratio_S"] - a["ratio_M2_expected"]) < 1e-12),
            "S(2M)/S(M)": a["ratio_S"], "expected_(M2/M1)^2": a["ratio_M2_expected"]}


def check_E3_magnitude():
    s = he.summary(1.0)
    # solar-mass BH entropy ~ 1e77 (k_B=1); cells ~ 1e76
    ok = 1e76 < s["S_BH"] < 1e78 and 1e75 < s["N_cells"] < 1e77
    return {"pass": bool(ok), "S_BH_1Msun": s["S_BH"], "N_cells_1Msun": s["N_cells"]}


SUITE = [("E1_per_cell_closed_form", check_E1_per_cell_closed_form, "s_cell=2pi sqrt3 (F107 -> S=A/4)"),
         ("E2_area_law", check_E2_area_law, "S ~ A ~ M^2 (area law exact)"),
         ("E3_magnitude", check_E3_magnitude, "S(1Msun)~1e77 nats, ~1e76 cells")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F190", "title": "Lattice microstates and the Bekenstein-Hawking area law",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F190_horizon_entropy.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
