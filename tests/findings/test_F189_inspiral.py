"""
test_F189_inspiral.py  --  PN binary inspiral / GW phasing (S6)
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import inspiral as ins   # noqa: E402
STAMP = "2026-06-30 - 04:35"


def check_I1_gw150914():
    g = ins.gw150914()
    # measured: chirp mass ~28.6 Msun, f_isco ~70 Hz, ~0.2 s in band from 35 Hz
    ok = (27.0 < g["Mc_solar"] < 29.0 and 60 < g["f_isco_Hz"] < 75
          and 0.15 < g["time_from_35Hz_s"] < 0.25)
    return {"pass": bool(ok), "Mc_solar": g["Mc_solar"], "f_isco_Hz": g["f_isco_Hz"],
            "time_from_35Hz_s": g["time_from_35Hz_s"]}


def check_I2_chirp_scaling():
    # df/dt ~ f^{11/3}: doubling f multiplies the rate by 2^{11/3}
    Mc = ins.chirp_mass_solar(36, 29)
    r1 = ins.df_dt(50.0, Mc); r2 = ins.df_dt(100.0, Mc)
    ratio = r2 / r1
    return {"pass": bool(abs(ratio - 2**(11/3)) / 2**(11/3) < 1e-6),
            "ratio_meas": ratio, "ratio_expected_2^(11/3)": 2**(11/3)}


def check_I3_chirp_mass_formula():
    # equal masses: Mc = m / 2^{1/5}
    Mc = ins.chirp_mass_solar(30, 30)
    return {"pass": bool(abs(Mc - 30 / 2**0.2) < 1e-9),
            "Mc_equal_mass": Mc, "expected_30/2^0.2": 30 / 2**0.2}


SUITE = [("I1_gw150914", check_I1_gw150914, "GW150914 chirp mass ~28.6, f_isco ~70 Hz, ~0.2 s"),
         ("I2_chirp_scaling", check_I2_chirp_scaling, "df/dt ~ f^{11/3} (quadrupole)"),
         ("I3_chirp_mass_formula", check_I3_chirp_mass_formula, "equal mass Mc = m/2^{1/5}")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F189", "title": "PN compact-binary inspiral & GW phasing",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F189_inspiral.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
