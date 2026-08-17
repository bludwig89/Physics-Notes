"""
test_F197_first_excitation_dark.py
==================================
F197 — the first excitation channel as a unified dark sector.

Tests the discriminator that COMPARES the two near-vacuum channels (F193 §E):
  Channel A = F93 E_g second-shell condensate; Channel B = F69 marginal-binding.
The make-or-break (F191): a dark-matter source must be (i) smooth-cosmic w=-1,
(ii) clustering/cold w->0, (iii) collisionless.

5 checks:
  E1  equation of state separates by excitation type (VEV w=-1, gapped cold w->0,
      massless w=1/3) — the physical basis of the smooth-vs-clustering split.
  E2  Channel A (E_g) has GAPPED fluctuation modes (amplitude + angular), both
      m^2>0, at the F93 orthorhombic minimum -> cold-capable.
  E3  Channel B (F69) is GAPLESS (massless photon, marginal binding) -> radiation,
      cannot be cold dark matter.
  E4  Clustering contrast (F193 §73): the homogeneous piece is non-normalizable
      (Friedmann/dark-energy only), but a localized gapped-mode clump gives a
      convergent mass and a FLAT rotation curve.
  E5  Channel verdict: A is the unique unified dark sector (DE+DM); B is excluded.
"""
from __future__ import annotations
import json, os, sys, time
THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
# Forks are loaded by bare name, not as package submodules;
# importing casim appends engine/forks/<sector>/ to sys.path.
import casim as _casim  # noqa: E402,F401
import gr_fork_F197_first_excitation_dark as F197   # noqa: E402
STAMP = "2026-06-30 - 19:20"

OUT = F197.run()


def check_E1_eos_split():
    e = OUT["eos"]
    ok = (e["w_VEV_darkenergy"] == -1.0
          and e["w_gapped_cold"] < 1e-3
          and abs(e["w_massless_radiation"] - 1.0 / 3.0) < 1e-12)
    return {"pass": bool(ok), **e,
            "note": "VEV=-1 (dark energy); gapped cold ->0 (clusters); massless=1/3 (radiation)"}


def check_E2_Eg_gapped():
    g = OUT["channel_A_Eg"]["gap"]
    ok = (g["both_gapped"] and g["orthorhombic"]
          and g["mass_ratio_light_to_heavy"] < 1.0)   # angular mode lighter
    return {"pass": bool(ok), "delta_star_deg": g["delta_star_deg"],
            "cos3delta_star": g["cos3delta_star"],
            "m2_angular_light": g["m2_angular_light"], "m2_amplitude_heavy": g["m2_amplitude_heavy"],
            "mass_ratio_light_to_heavy": g["mass_ratio_light_to_heavy"],
            "note": "E_g condensate: two gapped modes; angular (axion-like, light) + amplitude (Higgs-like, heavy)"}


def check_E3_F69_gapless():
    g = OUT["channel_B_F69"]["gap"]
    ok = (g["gapless"] and not OUT["channel_B_F69"]["can_be_dark_matter"])
    return {"pass": bool(ok), "gap": g["gap"],
            "note": "F69 paired-spinor photon massless / marginal binding -> radiation, not cold DM"}


def check_E4_clustering_contrast():
    c = OUT["clustering"]
    ok = (c["homogeneous_nonnormalizable"]
          and c["clump_total_mass_converges"]
          and c["baryon_falloff"] < 0.7
          and c["rotation_flatness_with_clump"] > 0.85)
    return {"pass": bool(ok),
            "homogeneous_nonnormalizable": c["homogeneous_nonnormalizable"],
            "clump_total_mass_converges": c["clump_total_mass_converges"],
            "baryon_falloff": c["baryon_falloff"],
            "rotation_flatness_with_clump": c["rotation_flatness_with_clump"],
            "note": "homogeneous -> Friedmann/dark-energy only (F193 §73); localized clump -> flat curve"}


def check_E5_verdict():
    A, B = OUT["channel_A_Eg"], OUT["channel_B_F69"]
    ok = (A["unified_dark_sector"] and not B["unified_dark_sector"]
          and A["can_be_dark_energy"] and A["can_be_dark_matter"])
    return {"pass": bool(ok),
            "Eg_unified": A["unified_dark_sector"], "F69_unified": B["unified_dark_sector"],
            "verdict": OUT["verdict"]}


SUITE = [
    ("E1_eos_split", check_E1_eos_split, "EoS separates: VEV=-1, gapped cold->0, massless=1/3"),
    ("E2_Eg_gapped", check_E2_Eg_gapped, "E_g condensate has two gapped (cold-capable) modes"),
    ("E3_F69_gapless", check_E3_F69_gapless, "F69 channel gapless -> radiation, not cold DM"),
    ("E4_clustering_contrast", check_E4_clustering_contrast, "homogeneous non-normalizable; clump -> flat curve"),
    ("E5_verdict", check_E5_verdict, "E_g = unified dark sector; F69 excluded"),
]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F197",
            "title": "First excitation channel as a unified dark sector (E_g condensate vs F69), discriminator",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "open_obstruction": OUT["open_obstruction"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F197_first_excitation_dark_test.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
