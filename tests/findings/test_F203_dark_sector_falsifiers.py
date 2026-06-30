"""
test_F203_dark_sector_falsifiers.py
===================================
F203 — the dark-sector falsifiability battery: builds out all six observational
tests in docs/theory/dark-sector-overview.md §4 and asserts each is (a) well-posed
(model prediction + current observation + quantified margin + explicit falsifier
all present) and (b) correctly classified by current data.

6 checks (one per §4 test):
  T1  keV sterile X-ray line: prediction E=m_s/2, rate below XRISM line limit,
      but 100%-DM floor (~41 keV) above the model mass -> 'under_pressure'.
  T2  warm-DM structure: keV is below the non-resonant Lyman-alpha floor and
      survives only via resonant production -> 'under_pressure'.
  T3  dark energy w=-1: DESI DR2 rejects the CC at 2.8-4.2 sigma (not >=5) -> 'under_pressure'.
  T4  Bullet lensing on the collisionless component; emergent gravity falsified -> 'consistent'.
  T5  WIMP/axion nulls agree with the keV-sterile identity -> 'consistent'.
  T6  a0=c*H0/6 reproduces empirical to ~10% (diagnostic) -> 'consistent'.

The battery currently returns 0 falsified, 3 under_pressure, 3 consistent.
"""
from __future__ import annotations
import json, os, sys, time
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
FORKS = os.path.join(ROOT, "ca-simulation", "forks")
if FORKS not in sys.path: sys.path.insert(0, FORKS)
import gr_fork_F203_dark_sector_falsifiers as F203   # noqa: E402
STAMP = "2026-06-30 - 22:45"

OUT = F203.run()
TESTS = OUT["tests"]

REQUIRED_KEYS = ("model_prediction", "current_observation", "margin", "status",
                 "status_reason", "falsifier")


def _well_posed(t):
    """A falsifier test is well-posed iff it carries all of: a model prediction,
    a current observation, a quantified margin, a status, a reason, a falsifier."""
    return all(k in t and t[k] not in (None, "", {}, []) for k in REQUIRED_KEYS)


def check_T1_xray_line():
    t = TESTS["T1_xray_line"]
    m = t["margin"]
    ok = (_well_posed(t)
          and t["status"] == "under_pressure"
          and m["line_rate_headroom_factor"] > 1.0        # model rate below XRISM limit
          and m["below_100pct_DM_floor"] is True)         # but below the 41 keV 100%-DM floor
    return {"pass": bool(ok), "status": t["status"],
            "line_rate_headroom_dex": m["line_rate_headroom_dex"],
            "model_ms_keV": m["model_ms_keV"],
            "predicted_lines": {k: v["E_line_keV"] for k, v in t["model_prediction"]["lines"].items()},
            "note": "X-ray line at E=m_s/2; survives XRISM line limit but below the 41 keV 100%-DM floor"}


def check_T2_warm_structure():
    t = TESTS["T2_warm_structure"]
    m = t["margin"]
    ok = (_well_posed(t)
          and t["status"] == "under_pressure"
          and m["excluded_if_nonresonant"] is True
          and m["survives_if_resonant"] is True)
    return {"pass": bool(ok), "status": t["status"],
            "model_ms_keV": m["model_ms_keV"],
            "excluded_if_nonresonant": m["excluded_if_nonresonant"],
            "survives_if_resonant": m["survives_if_resonant"],
            "note": "warm-DM cutoff; non-resonant excluded, resonant survives at the edge"}


def check_T3_dark_energy_w():
    t = TESTS["T3_dark_energy_w"]
    m = t["margin"]
    pred = t["model_prediction"]
    ok = (_well_posed(t)
          and t["status"] == "under_pressure"
          and pred["w0"] == -1.0 and pred["wa"] == 0.0
          and 2.8 <= m["sigma_against_model"] < 5.0)      # tension, not discovery
    return {"pass": bool(ok), "status": t["status"],
            "model_w0wa": [pred["w0"], pred["wa"]],
            "sigma_against_model": m["sigma_against_model"],
            "note": "DESI DR2 rejects CC at 2.8-4.2 sigma; tension but < 5 sigma discovery"}


def check_T4_bullet_lensing():
    t = TESTS["T4_bullet_lensing"]
    m = t["margin"]
    ok = (_well_posed(t)
          and t["status"] == "consistent"
          and abs(m["model_minus_observed_Mpc"]) < 0.05    # model offset ~ observed
          and m["emergent_gravity_misprediction_Mpc"] > 0.1)  # EG misses by the full separation
    return {"pass": bool(ok), "status": t["status"],
            "model_minus_observed_Mpc": m["model_minus_observed_Mpc"],
            "emergent_gravity_misprediction_Mpc": m["emergent_gravity_misprediction_Mpc"],
            "note": "lensing on collisionless component matches Clowe 2006; emergent gravity falsified"}


def check_T5_not_wimp_not_axion():
    t = TESTS["T5_not_wimp_not_axion"]
    ok = (_well_posed(t)
          and t["status"] == "consistent"
          and t["margin"]["soft_falsifier"] is True)
    return {"pass": bool(ok), "status": t["status"],
            "identity": t["model_prediction"]["identity"],
            "note": "keV-sterile identity; WIMP/axion nulls consistent (soft falsifier)"}


def check_T6_a0_coincidence():
    t = TESTS["T6_a0_coincidence"]
    m = t["margin"]
    ok = (_well_posed(t)
          and t["status"] == "consistent"
          and abs(m["percent_off"]) < 15.0)                # a0 within ~15% of empirical
    return {"pass": bool(ok), "status": t["status"],
            "ratio": m["ratio"], "percent_off": m["percent_off"],
            "note": "a0=c*H0/6 within ~10% of empirical (diagnostic only)"}


def check_T7_battery_summary():
    """Meta-check: the battery is internally consistent — 6 tests, 0 falsified,
    and the count of under_pressure + consistent + falsified == 6."""
    s = OUT["summary"]
    ok = (s["n_tests"] == 6
          and s["n_falsified"] == 0
          and s["n_under_pressure"] == 3
          and s["n_consistent"] == 3
          and (s["n_falsified"] + s["n_under_pressure"] + s["n_consistent"]) == s["n_tests"])
    return {"pass": bool(ok), "summary": s,
            "note": "6 tests: 0 falsified, 3 under_pressure (T1/T2 sterile, T3 w), 3 consistent (T4/T5/T6)"}


SUITE = [
    ("T1_xray_line", check_T1_xray_line, "keV sterile X-ray line at E=m_s/2 (under pressure)"),
    ("T2_warm_structure", check_T2_warm_structure, "warm-DM Lyman-alpha squeeze (under pressure)"),
    ("T3_dark_energy_w", check_T3_dark_energy_w, "w=-1 vs DESI DR2 (under pressure)"),
    ("T4_bullet_lensing", check_T4_bullet_lensing, "lensing on collisionless component (consistent)"),
    ("T5_not_wimp_not_axion", check_T5_not_wimp_not_axion, "not WIMP / not axion (consistent)"),
    ("T6_a0_coincidence", check_T6_a0_coincidence, "a0=c*H0/6 (consistent, diagnostic)"),
    ("T7_battery_summary", check_T7_battery_summary, "battery internally consistent (0 falsified)"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}  status={r.get('status', '-')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F203",
            "title": "Dark-sector falsifiability battery (overview §4 built out)",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "verdict": OUT["verdict"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F203_dark_sector_falsifiers_test.json"), "w"),
              indent=2)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
