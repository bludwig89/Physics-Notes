"""
test_F187_qnm.py  --  Quasinormal-mode ringdown spectrum (WKB) (S4)
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import qnm as q   # noqa: E402
STAMP = "2026-06-30 - 04:25"


def check_Q1_fundamentals():
    sp = q.spectrum()
    # n=0 fundamentals: WKB-1 within 8% (real), 2% (imag), improving with l
    fund = {k: v for k, v in sp.items() if k.endswith("n0")}
    real_ok = all(v["err_real"] < 0.08 for v in fund.values())
    imag_ok = all(v["err_imag"] < 0.02 for v in fund.values())
    # convergence with l
    errs = [sp[f"l{l}_n0"]["err_real"] for l in (2, 3, 4)]
    converging = errs[0] > errs[1] > errs[2]
    return {"pass": bool(real_ok and imag_ok and converging),
            "fundamentals": fund, "real_errors_l234": errs}


def check_Q2_ringdown_waveform():
    w = q.ringdown_waveform(l=2, n=0)
    # damped sinusoid: positive quality factor, finite damping time
    ok = w["quality_factor"] > 1.5 and w["tau_ringdown_M"] > 0 and np.isfinite(w["h"]).all()
    return {"pass": bool(ok), "quality_factor": w["quality_factor"],
            "tau_ringdown_M": w["tau_ringdown_M"], "f_real_per_M": w["f_real_per_M"]}


def check_Q3_echo_suppressed():
    e = q.echo_amplitude_bound()
    # true horizon -> echo transmission exponentially small (<< 1)
    return {"pass": bool(e["single_barrier_transmission_~"] < 1e-3),
            "transmission": e["single_barrier_transmission_~"], "regime": e["echo_regime"]}


SUITE = [("Q1_fundamentals_vs_GR", check_Q1_fundamentals, "WKB QNM n=0 within 8%, converging"),
         ("Q2_ringdown_waveform", check_Q2_ringdown_waveform, "damped sinusoid, Q>1.5"),
         ("Q3_echo_suppressed", check_Q3_echo_suppressed, "horizon -> echoes exp. suppressed (vs F114)")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F187", "title": "Quasinormal-mode ringdown spectrum (WKB Regge-Wheeler)",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F187_qnm.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
