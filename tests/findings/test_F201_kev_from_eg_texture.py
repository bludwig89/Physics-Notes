"""
test_F201_kev_from_eg_texture.py
================================
F201 (part a) — does the lattice prefer a light (keV) M_R eigenvalue?
The F93/F76 Z_3 (E_g) generation texture applied to M_R has cancellation nodes
where one eigenvalue -> 0, making ONE light sterile natural.

5 checks:
  K1  the Z_3 texture reproduces the charged-lepton hierarchy at delta_e (data ~1e-4).
  K2  the texture has a Z_3 node at 135 deg where one sqrt-mass vanishes.
  K3  near the node, one eigenvalue is parametrically suppressed (monotone in proximity).
  K4  delta_nu ~0.14 deg from the node + M_R0 ~ GeV lands M_1 ~ keV, M_3 ~ GeV (nuMSM split).
  K5  verdict: one light sterile is structural; the keV value needs two inputs.
"""
from __future__ import annotations
import json, os, sys, time
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
FORKS = os.path.join(ROOT, "ca-simulation", "forks")
if FORKS not in sys.path: sys.path.insert(0, FORKS)
import gr_fork_F201_kev_from_eg_texture as F201   # noqa: E402
STAMP = "2026-06-30 - 22:00"

OUT = F201.run()


def check_K1_charged_lepton():
    cl = OUT["charged_lepton_reproduction"]
    tex = sorted(cl["texture_mass_ratios"]); obs = sorted(cl["observed_mass_ratios"])
    ok = all(abs(t - o) / o < 1e-2 for t, o in zip(tex, obs))
    return {"pass": bool(ok), "texture_ratios": tex, "observed_ratios": obs,
            "note": "same Z_3 texture reproduces m_e:m_mu:m_tau hierarchy"}


def check_K2_node():
    ok = abs(OUT["z3_node_deg"] - 135.0) < 1e-9
    return {"pass": bool(ok), "z3_node_deg": OUT["z3_node_deg"],
            "note": "1 + sqrt2 cos(135 deg) = 0 -> one sqrt-mass vanishes (cancellation node)"}


def check_K3_suppression_monotone():
    scan = OUT["light_eigenvalue_vs_angle"]
    near = [s for s in scan if s["delta_nu_deg"] >= 130.0]
    ratios = [s["M_min_over_M_max"] for s in near]
    ok = all(ratios[i] > ratios[i + 1] for i in range(len(ratios) - 1)) and ratios[-1] < 1e-7
    return {"pass": bool(ok), "near_node_scan": near,
            "note": "closer to the node -> exponentially lighter eigenvalue"}


def check_K4_kev_landing():
    p = OUT["physical_landing"]
    ok = (1.0 < p["M_lightest_keV"] < 50.0          # keV DM scale
          and 0.1 < p["M_heaviest_GeV"] < 100.0     # GeV heavy-sterile scale
          and p["node_proximity_rad"] < 1e-2)        # modest tuning
    return {"pass": bool(ok), "M_lightest_keV": p["M_lightest_keV"],
            "M_heaviest_GeV": p["M_heaviest_GeV"], "node_proximity_rad": p["node_proximity_rad"],
            "note": "M_R0~GeV + delta_nu ~0.14 deg from node -> M_1~keV, M_3~GeV (nuMSM split)"}


def check_K5_verdict():
    p = OUT["physical_landing"]
    ok = (p["hierarchy_M1_over_M3"] < 1e-5)
    return {"pass": bool(ok), "hierarchy_M1_over_M3": p["hierarchy_M1_over_M3"],
            "verdict": OUT["verdict"]}


SUITE = [
    ("K1_charged_lepton", check_K1_charged_lepton, "Z_3 texture reproduces charged-lepton hierarchy"),
    ("K2_node", check_K2_node, "Z_3 cancellation node at 135 deg"),
    ("K3_suppression_monotone", check_K3_suppression_monotone, "near-node eigenvalue parametrically light"),
    ("K4_kev_landing", check_K4_kev_landing, "M_R0~GeV + node-proximity -> keV + GeV (nuMSM)"),
    ("K5_verdict", check_K5_verdict, "one light sterile structural; keV value = 2 inputs"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F201",
            "title": "A light (keV) sterile from the F93 Z_3/E_g generation texture applied to M_R",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "verdict": OUT["verdict"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F201_kev_from_eg_texture_test.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
