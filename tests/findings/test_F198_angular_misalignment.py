"""
test_F198_angular_misalignment.py
=================================
F198 — relic abundance of the F197 E_g angular mode by misalignment, and the
freeze-out alternative for the heavy amplitude mode.

5 checks:
  G1  misalignment scaling validated: Omega ∝ m_a^{1/2} f^2 theta_i^2.
  G2  with the NATURAL condensate decay constant (f=v/2=123 GeV) misalignment
      needs a TRANS-PLANCKIAN mass -> fails.
  G3  a natural light angular mode (small lambda6) UNDER-produces by many orders.
  G4  reaching the axion window requires f >> the E_g condensate scale (GUT-ish).
  G5  the heavy AMPLITUDE mode via thermal freeze-out DOES reach Omega_DM
      (WIMP window) -> the viable route, updating the F197 candidate.
"""
from __future__ import annotations
import json, os, sys, time
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
FORKS = os.path.join(ROOT, "ca-simulation", "forks")
if FORKS not in sys.path: sys.path.insert(0, FORKS)
import gr_fork_F198_angular_misalignment as F198   # noqa: E402
STAMP = "2026-06-30 - 20:05"

OUT = F198.run()


def check_G1_scaling():
    s = OUT["scaling_check"]
    return {"pass": bool(s["Omega_propto_m^0.5_f^2_theta^2"]),
            "ratio_mass_x4": s["ratio_mass_x4"], "ratio_f_x2": s["ratio_f_x2"],
            "ratio_theta_x2": s["ratio_theta_x2"],
            "note": "Omega ∝ m_a^{1/2} f^2 theta^2 (x4 mass->x2, x2 f->x4, x2 theta->x4)"}


def check_G2_condensate_scale_fails():
    m = OUT["model_condensate_scale"]
    return {"pass": bool(m["trans_planckian"]),
            "f_GeV": m["f_GeV"], "m_a_required_GeV": m["m_a_required_GeV"],
            "m_a_required_over_M_Pl": m["m_a_required_over_M_Pl"],
            "note": "f=v/2=123 GeV needs trans-Planckian m_a -> misalignment fails at the condensate scale"}


def check_G3_light_mode_underproduces():
    n = OUT["natural_light_mode"]
    ok = (n["under_over_production"] == "UNDER" and n["deficit_factor"] > 1e6)
    return {"pass": bool(ok), "m_a_light_GeV": n["m_a_light_GeV"],
            "Omega_h2_obtained": n["Omega_h2_obtained"], "deficit_factor": n["deficit_factor"],
            "note": "light angular mode (small lambda6, f=123 GeV) under-produces by ~15 orders"}


def check_G4_axion_window_needs_high_f():
    a = OUT["f_for_axion_window"]
    ok = a["f_over_condensate_scale"] > 1e6
    return {"pass": bool(ok), "m_a_GeV": a["m_a_GeV"], "f_required_GeV": a["f_required_GeV"],
            "f_over_condensate_scale": a["f_over_condensate_scale"],
            "note": "a light (~ueV) angular mode reaches Omega_DM only at f~10^13 GeV, far above the condensate"}


def check_G5_freezeout_viable():
    fo = OUT["freezeout_amplitude_mode"]
    ok = fo["WIMP_window_reachable"]
    return {"pass": bool(ok), "best": fo["best"],
            "WIMP_window_reachable": fo["WIMP_window_reachable"],
            "note": "heavy amplitude mode (~TeV, EW coupling) hits Omega h^2~0.12 -> the viable relic route"}


SUITE = [
    ("G1_scaling", check_G1_scaling, "misalignment scaling Omega ∝ m^0.5 f^2 theta^2"),
    ("G2_condensate_scale_fails", check_G2_condensate_scale_fails, "f=123 GeV needs trans-Planckian mass"),
    ("G3_light_mode_underproduces", check_G3_light_mode_underproduces, "light angular mode under-produces ~15 orders"),
    ("G4_axion_window_needs_high_f", check_G4_axion_window_needs_high_f, "axion window needs f>>condensate scale"),
    ("G5_freezeout_viable", check_G5_freezeout_viable, "heavy amplitude mode freeze-out reaches Omega_DM"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F198",
            "title": "Angular-mode misalignment relic (fails at condensate scale) vs amplitude-mode freeze-out (viable)",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "verdict": OUT["verdict"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F198_angular_misalignment_test.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
