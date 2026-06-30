"""
test_F200_sterile_neutrino_dm.py
================================
F200 — the F47 sterile right-handed neutrino as the model-native dark-matter
relic, passing the bars the E_g sector failed (F199).

5 checks:
  S1  the F47 nu_R is a genuine total SM singlet (Y=0 structurally forced) -> sterile.
  S2  it is cosmologically long-lived at the viable mixing (tau/age ~ 1e9),
      vs the E_g amplitude mode which is ~38 orders below (F199).
  S3  it is massive (clusters, warm DM) and collisionless (only the tiny mixing).
  S4  mixing window: naive see-saw and non-resonant DW-for-100%-DM are X-ray
      excluded; the resonant nuMSM benchmark sits below the X-ray bound & stable.
  S5  verdict: model-native sterile DM candidate; mass scale accommodated (free M_R).
"""
from __future__ import annotations
import json, os, sys, time
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
FORKS = os.path.join(ROOT, "ca-simulation", "forks")
if FORKS not in sys.path: sys.path.insert(0, FORKS)
import gr_fork_F200_sterile_neutrino_dm as F200   # noqa: E402
STAMP = "2026-06-30 - 21:15"

OUT = F200.run()


def check_S1_genuine_sterile():
    e = OUT["existence"]
    ok = (e["genuinely_sterile"] and e["U1_Y"] == 0.0
          and e["SU2_L"] == "singlet" and e["SU3_colour"] == "singlet")
    return {"pass": bool(ok), "U1_Y": e["U1_Y"], "Y_forced_by": e["Y_forced_by"],
            "note": "F47 nu_R is a total SM singlet; Y=0 forced by Higgs-free Majorana U(1)_Y invariance"}


def check_S2_long_lived():
    s = OUT["stability"]
    ok = (s["stable_on_cosmo_time"] and s["tau_over_age_universe"] > 1e6
          and s["contrast_Eg_amplitude_tau_over_age"] < 1e-30)
    return {"pass": bool(ok), "m_s_keV": s["m_s_keV"], "sin2_2theta": s["sin2_2theta"],
            "tau_over_age_universe": s["tau_over_age_universe"],
            "contrast_Eg_amplitude_tau_over_age": s["contrast_Eg_amplitude_tau_over_age"],
            "note": "long-lived by ~9 orders; E_g amplitude mode was ~38 orders below age (F199)"}


def check_S3_clusters_collisionless():
    c = OUT["clustering_collisionless"]
    ok = (c["massive_keV_clusters"] and c["collisionless"])
    return {"pass": bool(ok), "warm_dark_matter": c["warm_dark_matter"],
            "free_streaming_caveat": c["free_streaming_caveat"],
            "note": "keV -> warm DM, clusters on galactic+ scales; only mixing coupling -> Bullet-compatible"}


def check_S4_mixing_window():
    b = OUT["mixing_window"]["benchmarks"]
    ok = (b["naive_seesaw"]["xray_excluded"]
          and b["nonresonant_DW_full"]["xray_excluded"]
          and not b["resonant_nuMSM"]["xray_excluded"]
          and b["resonant_nuMSM"]["stable"])
    return {"pass": bool(ok), "xray_bound": OUT["mixing_window"]["xray_bound_sin2_2theta"],
            "benchmarks": b,
            "note": "naive see-saw & DW-full X-ray excluded; resonant nuMSM benchmark allowed & stable"}


def check_S5_verdict():
    # passes all bars E_g failed: sterile (no decay channel forced), stable, clusters
    e, s, b = OUT["existence"], OUT["stability"], OUT["mixing_window"]["benchmarks"]
    ok = (e["genuinely_sterile"] and s["stable_on_cosmo_time"]
          and not b["resonant_nuMSM"]["xray_excluded"])
    return {"pass": bool(ok), "verdict": OUT["verdict"]}


SUITE = [
    ("S1_genuine_sterile", check_S1_genuine_sterile, "F47 nu_R is a total SM singlet (Y=0 forced)"),
    ("S2_long_lived", check_S2_long_lived, "long-lived (tau/age ~1e9) vs E_g 38 orders below"),
    ("S3_clusters_collisionless", check_S3_clusters_collisionless, "massive (warm, clusters) + collisionless"),
    ("S4_mixing_window", check_S4_mixing_window, "naive/DW X-ray excluded; resonant nuMSM allowed"),
    ("S5_verdict", check_S5_verdict, "model-native sterile DM passes all bars E_g failed"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F200",
            "title": "The F47 sterile right-handed neutrino as the model-native dark-matter relic",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "verdict": OUT["verdict"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F200_sterile_neutrino_dm_test.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
