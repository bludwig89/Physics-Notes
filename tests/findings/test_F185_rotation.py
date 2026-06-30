"""
test_F185_rotation.py  --  Slow-rotation frame dragging & moment of inertia (S2)
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
SIM = os.path.join(ROOT, "ca-simulation")
if SIM not in sys.path: sys.path.insert(0, SIM)
import ca_rotation as rot, ca_interior_metric as im   # noqa: E402
STAMP = "2026-06-30 - 04:15"
EOS = im.Polytrope(K=100.0, Gamma=2.0)


def check_R1_moment_of_inertia():
    d = rot.frame_drag(1.0e-3, EOS)
    ok = (0.25 <= d["I_over_MR2"] <= 0.45 and 8 <= d["I_bar"] <= 40
          and 0.0 < d["omega_over_Omega_surface"] < 0.2)
    return {"pass": bool(ok), "M_msun": d["M_msun"], "R_km": d["R_km"],
            "I_over_MR2": d["I_over_MR2"], "I_bar": d["I_bar"],
            "omega_over_Omega_surface": d["omega_over_Omega_surface"]}


def check_R2_framedrag_monotone():
    # more compact stars drag frames more strongly; I_bar decreases with compactness
    rows = [rot.frame_drag(rc, EOS) for rc in [6e-4, 8e-4, 1.0e-3, 1.2e-3]]
    comp = [r["compactness"] for r in rows]
    drag = [r["omega_over_Omega_surface"] for r in rows]
    ibar = [r["I_bar"] for r in rows]
    drag_up = all(drag[i] < drag[i+1] for i in range(len(drag)-1))
    ibar_down = all(ibar[i] > ibar[i+1] for i in range(len(ibar)-1))
    comp_up = all(comp[i] < comp[i+1] for i in range(len(comp)-1))
    return {"pass": bool(drag_up and ibar_down and comp_up),
            "compactness": comp, "framedrag": drag, "I_bar": ibar}


def check_R3_SI_units():
    d = rot.moment_of_inertia_SI(1.0e-3, EOS)
    # typical NS I ~ 1-2 x 10^45 g cm^2
    ok = 0.5 <= d["I_1e45_g_cm2"] <= 3.0
    return {"pass": bool(ok), "I_SI_kg_m2": d["I_SI_kg_m2"],
            "I_1e45_g_cm2": d["I_1e45_g_cm2"]}


SUITE = [("R1_moment_of_inertia", check_R1_moment_of_inertia, "I/MR^2~0.3, I_bar~10-40, frame drag"),
         ("R2_framedrag_monotone", check_R2_framedrag_monotone, "more compact -> more drag, smaller I_bar"),
         ("R3_SI_units", check_R3_SI_units, "I ~ 1e45 g cm^2 (pulsar range)")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F185", "title": "Slow-rotation frame dragging & moment of inertia",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F185_rotation.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
