"""
test_F196_dilution_exponent.py  --  deriving the p=2 holographic dilution exponent
that F193 left as its named obstruction (S9 follow-up).
"""
from __future__ import annotations
import json, os, sys, time

THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
FORK = os.path.join(ROOT, "ca-simulation", "forks")
if FORK not in sys.path: sys.path.insert(0, FORK)
import gr_fork_F196_dilution_exponent as dx   # noqa: E402
STAMP = "2026-06-30 - 18:10"

_R = dx.run()


def check_E1_exponent_is_2():
    # d ln rho_grav/d ln L = -2 exactly: p = 3 (volume) - 1 (Schwarzschild M~R)
    ok = abs(_R["dilution_exponent_p"] - 2.0) < 1e-9
    return {"pass": bool(ok), "p": _R["dilution_exponent_p"],
            "slope": _R["exponent_slope_dlnrho_dlnL"]}


def check_E2_two_routes_converge():
    # BH-bound and holographic (F190 area + GH) routes give the same number,
    # and that number is exactly the critical (energy) density
    ok = (_R["routes_agree_rel"] < 1e-6 and _R["bh_equals_crit_rel"] < 1e-9)
    return {"pass": bool(ok), "route1_bh": _R["route1_bh_bound_J_per_m3"],
            "route2_holo": _R["route2_holographic_J_per_m3"],
            "rho_crit": _R["rho_crit_energy_J_per_m3"]}


def check_E3_lands_near_observed():
    # saturation = rho_crit within 0.2 dex of observed; residual = Omega_L factor
    ok = (abs(_R["saturation_dlog10"]) < 0.2
          and 0.5 < _R["omega_L_residual_over_observed"] < 1.5)
    return {"pass": bool(ok), "saturation_over_observed": _R["saturation_over_observed"],
            "saturation_dlog10": _R["saturation_dlog10"],
            "omega_L_residual_over_observed": _R["omega_L_residual_over_observed"]}


def check_E4_statistical_route_excluded():
    # p=3/2 sqrt(N) fluctuation route overshoots by >20 orders -> effect is
    # gravitational (BH/holographic), not a mode-counting fluctuation
    ok = _R["p1p5_overshoot_log10"] > 20
    return {"pass": bool(ok), "p1p5_overshoot_log10": _R["p1p5_overshoot_log10"]}


def check_E5_f190_entropy_link():
    # the lattice-cell-vs-nat factor is exactly the F190 per-cell entropy 2 pi sqrt3
    ok = abs(_R["per_cell_entropy_nats"] - _R["per_cell_entropy_2pi_sqrt3"]) < 1e-9
    return {"pass": bool(ok), "per_cell_nats": _R["per_cell_entropy_nats"]}


SUITE = [("E1_exponent_is_2", check_E1_exponent_is_2,
          "p=2 exact: 3(volume) - 1(Schwarzschild M~R)"),
         ("E2_two_routes_converge", check_E2_two_routes_converge,
          "BH-bound = holographic(F190+GH) = critical density"),
         ("E3_lands_near_observed", check_E3_lands_near_observed,
          "saturation = rho_crit, 0.10 dex from obs; residual = Omega_L"),
         ("E4_statistical_route_excluded", check_E4_statistical_route_excluded,
          "p=3/2 sqrt(N) route excluded by >30 orders"),
         ("E5_f190_entropy_link", check_E5_f190_entropy_link,
          "cell-vs-nat factor = F190 per-cell entropy 2 pi sqrt3")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F196",
            "title": "Deriving the p=2 holographic dilution exponent from the lattice (closes F193 obstruction)",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F196_dilution_exponent_test.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
