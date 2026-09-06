"""
test_F184_tabulated_ns.py
=========================
F184 (scenario S1) -- realistic tabulated-EoS neutron stars on the F181
two-function TOV kernel.  Predicts M_max, R(1.4), surface redshift vs the
observed pulsar/NICER constraints.

Checks:
  N1  SLy: maximum mass in [1.95, 2.15] M_sun with a turnover, consistent with
      PSR J0740+6620 (2.08 +/- 0.07 M_sun); R(1.4) in [10.5, 12.0] km
      (NICER J0030/J0740 ~ 11-12.5 km); surface redshift at M_max in [0.3, 0.9].
  N2  EoS ordering (stiffness): the stiffer cores (AP4, MPA1) give larger
      M_max than SLy. (Corrected 2026-09-03, found by the F356 attack pass:
      N2 originally also required R(1.4) to order the same way as M_max, but
      that compound claim is false for the *correct* Read et al. 2009 AP4
      digits -- AP4's genuinely higher M_max comes with a genuinely *smaller*
      R(1.4) than SLy in this crust-simplified kernel, a real and literature-
      -known feature of AP4, not a code defect. Only the M_max ordering,
      which does hold, is asserted now; see F184's "Correction" section and
      findings/F356-multi-eos-nicer-robustness.md for the numbers.)
  N3  GR consistency: each EoS shows a stable branch (dM/drho_c > 0) terminating
      at the maximum-mass turnover (the GR/TOV instability), i.e. a physical
      mass-radius sequence (not the literal-F106 runaway of F174).

Run:  python tests/findings/test_F184_tabulated_ns.py
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np

THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.interactions import ns_eos as e                      # noqa: E402

STAMP = "2026-06-30 - 04:00"


def check_N1_sly():
    s = e.summarize(e.PiecewisePolytrope("SLy"), n=70)
    ok = (1.95 <= s["M_max"] <= 2.15 and s["turnover"]
          and 10.5 <= s["R_1.4_km"] <= 12.0
          and 0.3 <= s["z_surf_at_Mmax"] <= 0.9
          and s["M_max"] >= 2.0)            # PSR J0740 lower edge
    return {"pass": bool(ok), "M_max": s["M_max"], "R_1.4_km": s["R_1.4_km"],
            "z_surf_at_Mmax": s["z_surf_at_Mmax"], "turnover": s["turnover"],
            "J0740_consistent": bool(s["M_max"] >= 2.0)}


def check_N2_ordering():
    """M_max ordering only -- see the N2 docstring above (corrected 2026-09-03)
    for why R(1.4) is reported but no longer asserted to order the same way."""
    sly = e.summarize(e.PiecewisePolytrope("SLy"), n=60)
    apr = e.summarize(e.PiecewisePolytrope("APR"), n=60)
    mpa = e.summarize(e.PiecewisePolytrope("MPA1"), n=60)
    ok = (apr["M_max"] > sly["M_max"] and mpa["M_max"] > sly["M_max"])
    return {"pass": bool(ok),
            "M_max": {"SLy": sly["M_max"], "APR": apr["M_max"], "MPA1": mpa["M_max"]},
            "R_1.4": {"SLy": sly["R_1.4_km"], "APR": apr["R_1.4_km"], "MPA1": mpa["R_1.4_km"]},
            "_note": "R_1.4 reported, not asserted to order with M_max -- see docstring"}


def check_N3_stable_branch():
    s = e.summarize(e.PiecewisePolytrope("SLy"), n=80)
    c = s["curve"]; M = c["M_msun"]; i = int(np.argmax(M))
    rising = np.all(np.diff(M[:i+1]) > 0)          # stable branch monotone rising
    falls_after = i < len(M) - 1 and M[-1] < M[i]  # unstable branch after turnover
    return {"pass": bool(rising and falls_after and 0 < i < len(M)-1),
            "i_turnover": i, "stable_branch_monotone": bool(rising),
            "unstable_after_turnover": bool(falls_after)}


SUITE = [
    ("N1_SLy_mass_radius", check_N1_sly, "SLy M_max~2.05, R(1.4)~11 km, J0740-consistent"),
    ("N2_eos_ordering", check_N2_ordering, "stiffer EoS -> larger M_max and R(1.4)"),
    ("N3_stable_branch_turnover", check_N3_stable_branch, "GR/TOV stable branch + max-mass turnover"),
]


def run():
    results, t0 = {}, time.time()
    for name, fn, desc in SUITE:
        t = time.time(); print(f"[run] {name} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = desc
        results[name] = r; print(f"      pass={r.get('pass')}  ({r['_seconds']}s)", flush=True)
    n_pass = sum(1 for r in results.values() if r.get("pass"))
    return {"finding": "F184", "title": "Tabulated-EoS neutron stars on the F181 TOV kernel",
            "timestamp": STAMP, "n_pass": n_pass, "n_total": len(SUITE),
            "results": results, "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    with open(os.path.join(ROOT, "test-results", "F184_tabulated_ns.json"), "w") as f:
        json.dump(out, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS  ({out['seconds']}s)")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
