"""
test_F194_emergent_gravity_bullet.py
====================================
F194 -- model-native emergent-gravity ("dark matter without dark matter")
falsified by the Bullet-Cluster lensing/gas offset.

Checks (5/5):
  E1  a0 derived from the vacuum/de-Sitter scale (F164/F192 sector) matches the
      empirical MOND a0 ~ 1.2e-10 m/s^2 to within 30%   -> NOT a strawman.
  E2  emergent gravity flattens the rotation curve from baryons alone and obeys
      the baryonic Tully-Fisher relation                 -> reproduces galaxies.
  E3  Newtonian-limit self-consistency: as a0->0, nu->1 and the QUMOND
      dynamical density recovers the baryons (solver validation).
  E4  THE FALSIFIER: in the toy Bullet Cluster the emergent-gravity lensing peak
      sits ON the gas (offset ~0), because the lensing mass is a local functional
      of the baryons; the OBSERVED lensing peak is offset onto the collisionless
      galaxies (~0.19 Mpc), which LCDM reproduces.       -> EG falsified.
  E5  verdict assembly.

Run:  python3 tests/findings/test_F194_emergent_gravity_bullet.py
Writes test-results/F194_emergent_gravity_bullet.json (+ figure if matplotlib).
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "ca-simulation"))

import ca_emergent_gravity as eg   # noqa: E402

GRID_CELL_MPC = 3.0 / 128          # ~0.0234 Mpc; peak resolution


def run():
    checks = {}

    # -- E1: a0 from the vacuum sector ------------------------------------
    a0 = eg.derive_a0_from_vacuum()
    e1 = abs(a0["a0_model_over_empirical"] - 1.0) < 0.30
    checks["E1_a0_from_vacuum"] = {
        "a0_model_SI": a0["a0_model_SI"],
        "a0_empirical_SI": a0["a0_empirical_SI"],
        "ratio": a0["a0_model_over_empirical"],
        "H0_km_s_Mpc": a0["H0_km_s_Mpc"],
        "pass": bool(e1),
    }

    # -- E2: rotation curve + BTF -----------------------------------------
    rc = eg.rotation_curve_emergent()
    e2 = (rc["flatness"] > 0.85) and (abs(rc["btf_ratio"] - 1.0) < 0.25)
    checks["E2_rotation_curve"] = {
        "flatness": rc["flatness"], "btf_ratio": rc["btf_ratio"], "pass": bool(e2),
    }

    # -- E3: Newtonian-limit solver self-consistency ----------------------
    rN = eg.bullet_cluster_emergent(a0_u=1e-3)   # a0->0 => nu->1
    bar = np.array(rN["profiles"]["gas"]) + np.array(rN["profiles"]["galaxies"])
    egN = np.array(rN["profiles"]["emergent_lensing"])
    xx = np.array(rN["x_mpc"]); m = np.abs(xx) < 0.75
    integ_ratio = float(egN[m].sum() / bar[m].sum())
    corr = float(np.corrcoef(egN[m], bar[m])[0, 1])
    e3 = (abs(integ_ratio - 1.0) < 0.05) and (corr > 0.99)
    checks["E3_newtonian_recovery"] = {
        "rho_dyn_over_rho_b": integ_ratio, "corr": corr, "pass": bool(e3),
    }

    # -- E4: the Bullet-Cluster falsifier ---------------------------------
    b = eg.bullet_cluster_emergent()
    eg_off = b["emergent_offset_from_gas_mpc"]
    obs_off = b["observed_lensing_offset_from_gas_mpc"]
    lcdm_off = b["lcdm_offset_from_gas_mpc"]
    # EG predicts lensing ON the gas (offset ~ 0, within a couple of cells);
    # observation puts it on the galaxies (offset ~ obs_off >> 0).
    eg_on_gas = eg_off <= 2 * GRID_CELL_MPC
    obs_on_galaxies = obs_off > 0.1
    lcdm_matches_obs = abs(lcdm_off - obs_off) < 0.05
    # the model misprediction = the full observed offset it fails to produce
    misprediction_mpc = abs(obs_off - eg_off)
    e4 = eg_on_gas and obs_on_galaxies and lcdm_matches_obs and misprediction_mpc > 0.1
    checks["E4_bullet_falsifier"] = {
        "gas_peak_mpc": b["gas_peak_x_mpc"],
        "galaxy_peak_mpc": b["galaxy_peak_x_mpc"],
        "emergent_lensing_peak_mpc": b["emergent_lensing_peak_x_mpc"],
        "emergent_offset_from_gas_mpc": eg_off,
        "observed_offset_from_gas_mpc": obs_off,
        "lcdm_offset_from_gas_mpc": lcdm_off,
        "emergent_misprediction_mpc": misprediction_mpc,
        "emergent_lensing_on_gas": bool(eg_on_gas),
        "observed_lensing_on_galaxies": bool(obs_on_galaxies),
        "lcdm_reproduces_observation": bool(lcdm_matches_obs),
        "pass": bool(e4),
    }

    # -- E5: verdict ------------------------------------------------------
    e5 = e1 and e2 and e3 and e4
    checks["E5_verdict"] = {
        "model_native_emergent_gravity": "FALSIFIED by Bullet Cluster",
        "reason": ("emergent gravity / IR-running induced-G makes the lensing "
                   "mass a local functional of the baryons, so its peak tracks "
                   "the gas; the observed peak is on the collisionless galaxies, "
                   "offset by ~0.19 Mpc. A dark *source* (F191) is required."),
        "pass": bool(e5),
    }

    n_pass = sum(1 for v in checks.values() if v.get("pass"))
    result = {
        "finding": "F194",
        "title": "Model-native emergent-gravity dark matter, falsified by the "
                 "Bullet-Cluster lensing/gas offset",
        "date": "2026-06-30 - 15:10",
        "n_pass": n_pass, "n_total": len(checks),
        "all_pass": n_pass == len(checks),
        "checks": checks,
        "bullet_profiles": {  # for the figure / reproducibility
            "x_mpc": b["x_mpc"], **b["profiles"],
        },
    }
    return result


def make_figure(result, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None
    p = result["bullet_profiles"]
    x = np.array(p["x_mpc"])
    norm = lambda a: np.array(a) / max(np.array(a)[np.abs(x) < 0.75].max(), 1e-30)
    m = (x > 0) & (x < 0.75)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.fill_between(x[m], 0, norm(p["gas"])[m], color="tab:red", alpha=.30,
                    label="gas (X-ray, dominant baryons)")
    ax.plot(x[m], norm(p["galaxies"])[m], color="tab:blue", lw=2,
            label="galaxies (collisionless baryons)")
    ax.plot(x[m], norm(p["emergent_lensing"])[m], color="k", lw=2.4,
            label="emergent-gravity lensing (predicted)")
    ax.plot(x[m], norm(p["lcdm_lensing"])[m], color="tab:green", lw=1.8, ls="--",
            label="$\\Lambda$CDM lensing (dark source)")
    c = result["checks"]["E4_bullet_falsifier"]
    ax.axvline(c["gas_peak_mpc"], color="tab:red", ls=":", lw=1)
    ax.axvline(c["galaxy_peak_mpc"], color="tab:blue", ls=":", lw=1)
    ax.set_xlabel("position along collision axis  [Mpc]")
    ax.set_ylabel("normalised surface density")
    ax.set_title("F194  Bullet Cluster: emergent gravity puts lensing on the gas\n"
                 "(observed & $\\Lambda$CDM: lensing on the galaxies) — EG falsified")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    return path


if __name__ == "__main__":
    res = run()
    outdir = os.path.join(ROOT, "test-results")
    os.makedirs(os.path.join(outdir, "figures"), exist_ok=True)
    with open(os.path.join(outdir, "F194_emergent_gravity_bullet.json"), "w") as f:
        json.dump(res, f, indent=2)
    figpath = make_figure(res, os.path.join(outdir, "figures",
                                            "F194_emergent_gravity_bullet.png"))
    print(f"F194  {res['n_pass']}/{res['n_total']} checks pass "
          f"(all_pass={res['all_pass']})")
    for name, c in res["checks"].items():
        print(f"  {'PASS' if c.get('pass') else 'FAIL'}  {name}")
    ef = res["checks"]["E4_bullet_falsifier"]
    print(f"\n  emergent-gravity lensing peak: {ef['emergent_lensing_peak_mpc']:.3f} Mpc "
          f"(gas at {ef['gas_peak_mpc']:.3f}) -> offset {ef['emergent_offset_from_gas_mpc']:.3f} Mpc")
    print(f"  observed lensing offset from gas: {ef['observed_offset_from_gas_mpc']:.3f} Mpc "
          f"(on galaxies at {ef['galaxy_peak_mpc']:.3f})")
    print(f"  EG misprediction: {ef['emergent_misprediction_mpc']:.3f} Mpc")
    if figpath:
        print(f"  figure: {figpath}")
    sys.exit(0 if res["all_pass"] else 1)
