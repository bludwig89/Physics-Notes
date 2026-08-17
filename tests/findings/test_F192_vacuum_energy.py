"""
test_F192_vacuum_energy.py  --  Cosmological constant under the full tensor (S9, open)
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import vacuum_energy as ve   # noqa: E402
STAMP = "2026-06-30 - 04:50"


def check_V1_vacuum_eos_sign():
    e = ve.vacuum_equation_of_state()
    # w=-1 -> rho+3p = -2 rho < 0 -> full tensor ACCELERATES (correct dark-energy sign)
    ok = (e["w_vacuum"] == -1.0 and abs(e["rho_plus_3p_over_rho"] + 2.0) < 1e-12
          and e["full_tensor_accelerates"])
    return {"pass": bool(ok), "w": e["w_vacuum"],
            "rho_plus_3p_over_rho": e["rho_plus_3p_over_rho"],
            "accelerates": e["full_tensor_accelerates"]}


def check_V2_bare_overshoot():
    o = ve.bare_overshoot()
    # reproduces the F164 ~120-order overshoot
    ok = 115 < o["log10_overshoot"] < 124
    return {"pass": bool(ok), "log10_overshoot": o["log10_overshoot"],
            "rho_vac_J_m3": o["rho_vac_J_m3"]}


def check_V3_open_status():
    # honest: every candidate cancellation is undically derived -> problem open
    c = ve.cancellation_ledger()
    none_derived = all(not v["derived"] for v in c.values())
    return {"pass": bool(none_derived), "n_candidates": len(c),
            "all_underived": bool(none_derived),
            "status": "full-tensor fixes the SIGN; the magnitude (F164) stays open"}


SUITE = [("V1_vacuum_eos_sign", check_V1_vacuum_eos_sign, "w=-1: rho+3p=-2rho -> accelerates (sign right)"),
         ("V2_bare_overshoot", check_V2_bare_overshoot, "reproduces F164 ~10^120 overshoot"),
         ("V3_open_status", check_V3_open_status, "candidate cancellations all underived (open)")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F192", "title": "The cosmological constant under the full-tensor source (sign fixed, magnitude open)",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F192_vacuum_energy.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
