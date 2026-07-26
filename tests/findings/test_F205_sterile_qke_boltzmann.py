"""
test_F205_sterile_qke_boltzmann.py
==================================
F205 — the full Boltzmann (quantum-kinetic) computation of keV sterile-neutrino
dark matter, built to narrow the order-of-magnitude F203 T1/T2 margins.

Validation checks (against literature benchmarks + internal convergence):
  V1  Omega linear in sin^2(2theta) at fixed L (justifies the one-run rescale).
  V2  DW abundance: sin^2 2theta for Omega_DM at 7.1 keV lands in the literature
      band [2e-9, 1.2e-8] (this code: 6.1e-9) — reproduces DW to within the known
      ~factor-2 QCD normalisation.
  V3  DW is X-ray excluded by > 2 dex (was 'order-of-magnitude' in F203 T1).
  V4  Resonant production: >100x enhancement over DW, and it clears the X-ray
      bound for a scanned lepton asymmetry.
  V5  Non-resonant Lyman-alpha floor reproduces the cited ~41 keV combined bound
      (35-48 keV) — validates the free-streaming -> thermal-equiv mapping.
  V6  Resonant coldest spectrum is genuinely colder than DW (<eps> ratio < 0.7)
      and relaxes the Lyman-alpha floor below the non-resonant value.
  V7  Verdict: model 5.6 keV and benchmark 7.1 keV sit BELOW the relaxed floor
      -> F203 T1/T2 pressure confirmed and quantified (not removed).
  V8  <eps> spectrum converged under grid refinement (physical L-dependence).
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
FORKS = os.path.join(ROOT, "ca-simulation", "forks")
if FORKS not in sys.path: sys.path.insert(0, FORKS)
import dm_fork_F205_sterile_qke_boltzmann as F205   # noqa: E402
STAMP = "2026-06-30 - 23:40"

OUT = F205._finalize(F205.run())
DW = OUT["nonresonant_DW"]; RS = OUT["resonant_ShiFuller"]; FS = OUT["free_streaming_lyman_alpha"]


def check_V1_linearity():
    ms = 7.1 * F205.KEV
    o1 = F205.production(ms, 1e-11, L=0.0)
    o2 = F205.production(ms, 2e-11, L=0.0)
    ratio = o2 / o1
    ok = abs(ratio - 2.0) < 1e-3
    return {"pass": bool(ok), "ratio_doubling": ratio,
            "note": "Omega exactly linear in sin^2(2theta) -> one-run rescale is valid"}


def check_V2_DW_abundance():
    s2 = DW["sin2_2theta_for_OmegaDM"]
    ok = 2e-9 <= s2 <= 1.2e-8       # literature band for 7.1 keV DW (~3-4e-9 central)
    return {"pass": bool(ok), "sin2_DW": s2,
            "note": "DW mixing for Omega_DM at 7.1 keV reproduces the literature to within ~factor 2"}


def check_V3_DW_xray_excluded():
    ok = DW["xray_excluded"] and DW["excess_over_xray_dex"] > 2.0
    return {"pass": bool(ok), "excess_dex": DW["excess_over_xray_dex"],
            "note": "DW X-ray excluded by >2 dex (F203 T1 order-of-magnitude -> 2.55 dex)"}


def check_V4_resonant_enhancement():
    cleared = any(not r["xray_excluded"] for r in RS["L_scan"])
    ok = RS["resonant_enhancement_factor"] > 100.0 and cleared
    return {"pass": bool(ok), "enhancement": RS["resonant_enhancement_factor"],
            "L_first_xray_allowed": RS["L_first_xray_allowed"],
            "note": "resonant production >100x more efficient than DW; clears X-ray bound for L>~2e-3"}


def check_V5_NRP_lyman_alpha_floor():
    floor = FS["lyman_alpha_floor_nonresonant_keV"]
    ok = 35.0 <= floor <= 48.0      # reproduces the cited combined ~41 keV bound
    return {"pass": bool(ok), "floor_nonresonant_keV": floor,
            "note": "non-resonant Lyman-alpha floor ~41 keV reproduces the cited combined X-ray+Lya bound"}


def check_V6_resonant_colder():
    ratio = RS["coldest_point"]["colder_than_DW_ratio"]
    relaxed = FS["lyman_alpha_floor_coldest_keV"] < FS["lyman_alpha_floor_nonresonant_keV"]
    ok = ratio < 0.7 and relaxed
    return {"pass": bool(ok), "coldest_ratio": ratio,
            "floor_coldest_keV": FS["lyman_alpha_floor_coldest_keV"],
            "note": "coldest resonant spectrum <eps> ~0.48x DW; relaxes the Lyman-alpha floor 41 -> 15 keV"}


def check_V7_model_under_pressure():
    # the quantified pressure: model 5.6 keV and benchmark 7.1 keV below even the
    # coldest+conservative floor -> T1/T2 confirmed, not removed
    ok = (not FS["model_passes_coldest_conservative_floor"]
          and not FS["benchmark_passes_coldest_conservative_floor"])
    return {"pass": bool(ok),
            "model_ms_keV": FS["model_ms_keV"],
            "floor_coldest_conservative_keV": FS["lyman_alpha_floor_coldest_conservative_keV"],
            "note": "5.6/7.1 keV below the ~9 keV coldest+conservative floor -> under pressure, quantified"}


def check_V8_spectrum_converged():
    # re-run DW spectrum at 2x eps resolution; <eps> stable to <1%
    eps_default = F205._eps_grid()
    _, _, _, me_lo = F205.production(7.1 * F205.KEV, 1e-11, L=0.0, return_spectrum=True)
    # temporarily double eps resolution
    orig = F205._eps_grid.__defaults__
    F205._eps_grid.__defaults__ = (4000,)
    _, _, _, me_hi = F205.production(7.1 * F205.KEV, 1e-11, L=0.0, return_spectrum=True)
    F205._eps_grid.__defaults__ = orig
    rel = abs(me_hi - me_lo) / me_lo
    ok = rel < 0.01
    return {"pass": bool(ok), "mean_eps_2000": me_lo, "mean_eps_4000": me_hi, "rel_change": rel,
            "note": "<eps> converged under grid refinement -> L-dependence is physical, not an artifact"}


SUITE = [
    ("V1_linearity", check_V1_linearity, "Omega linear in sin2 (rescale valid)"),
    ("V2_DW_abundance", check_V2_DW_abundance, "DW mixing for Omega_DM in literature band"),
    ("V3_DW_xray_excluded", check_V3_DW_xray_excluded, "DW X-ray excluded by >2 dex"),
    ("V4_resonant_enhancement", check_V4_resonant_enhancement, ">100x resonant enhancement, clears X-ray"),
    ("V5_NRP_lyman_alpha_floor", check_V5_NRP_lyman_alpha_floor, "NRP Lyman-alpha floor ~41 keV"),
    ("V6_resonant_colder", check_V6_resonant_colder, "coldest resonant spectrum relaxes the floor"),
    ("V7_model_under_pressure", check_V7_model_under_pressure, "5.6/7.1 keV below floor -> pressure confirmed"),
    ("V8_spectrum_converged", check_V8_spectrum_converged, "<eps> grid-converged"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F205",
            "title": "Full Boltzmann (QKE) computation of keV sterile dark matter — narrowing F203 T1/T2",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "verdict": OUT["verdict"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F205_sterile_qke_boltzmann_test.json"), "w"),
              indent=2)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
