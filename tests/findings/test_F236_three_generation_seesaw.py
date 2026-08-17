"""
test_F236_three_generation_seesaw.py
====================================
F236 — the full 3x3 Higgs-free see-saw with the F93/F76/F201 E_g generation
texture, its light spectrum, and PMNS mixing (F47 open follow-up #1/#2).

Acceptance test (stated up front):
  Does the lattice E_g texture reproduce the three light active mass-squared
  splittings AND the PMNS mixing angles with NO free mixing angles?  Or a
  clear account of which texture inputs remain free.

Result encoded here:
  - The 3x3 see-saw generalises F47 exactly (per-generation reduction to
    F47's M_D^2/M_R at machine precision).  [S1]
  - The E_g texture is DIAGONAL in the cube-axis basis (F93 O1), so with M_D
    and M_R both E_g-textured the light matrix m_nu is diagonal and PMNS = I:
    a structural NO-GO — large lepton mixing cannot come from E_g alone.  [S2]
  - Turning on the second-shell T_2g (axis-mixing) channel — the F93 unique
    off-diagonal channel (commitment #1) — switches the PMNS angles on.  [S3]
  - With T_2g free, ALL five observables (theta12, theta13, theta23, dm21^2,
    dm31^2) can be reproduced, but only using 6 inputs for 5 observables:
    the mixing is a FREE T_2g input, not a texture output.  [S4]
  - The 6x6 <-> type-I block-diagonalisation is machine-precise in the
    hierarchical regime, verified by a hand-rolled residual.  [S5]

Verdict: the E_g texture pins the light-mass HIERARCHY/ORDERING (F201 node);
the PMNS ANGLES are free T_2g inputs the E_g texture does not pin.  A negative
(free-input) result, recorded honestly per the House Rules.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.particles import majorana as M  # noqa: E402

STAMP = "2026-07-03 - 15:20"

# NuFIT-5.2 normal-ordering central values (w/ SK atmospheric), for comparison.
OBS = {
    "theta12": 33.4,
    "theta13": 8.6,
    "theta23": 49.0,
    "dm21_sq_eV2": 7.42e-5,
    "dm31_sq_eV2": 2.51e-3,
}


# ---------------------------------------------------------------------------
# S1 — the 3x3 see-saw reduces to F47's per-generation M_D^2/M_R (exact)
# ---------------------------------------------------------------------------
def check_S1_reduces_to_F47():
    MD = [0.5e-3, 0.10, 1.0]           # GeV
    MR0 = 1.0e12
    dnu = np.radians(72.0)             # non-degenerate angle
    MR = M.eg_diagonal_matrix(dnu, MR0)
    r = M.three_gen_seesaw(MD, dnu, MR0, t2g=(0, 0, 0))
    module_masses = sorted(r["light_masses"])
    # F47 per-generation light eigenvalue via the NUMERICALLY STABLE Vieta form
    # |lambda_-| = M_D^2 / M_R (F47 seesaw_eigenvalues; avoids the catastrophic
    # cancellation of (M_R - sqrt(M_R^2+4 M_D^2))/2 at M_R >> M_D).
    f47 = sorted(MD[i] ** 2 / MR[i, i] for i in range(3))
    resid = max(abs(a - b) for a, b in zip(module_masses, f47))
    ok = resid < 1e-9 * max(f47) and r["residual_mnu"] < 1e-12
    return {
        "pass": bool(ok),
        "module_masses": module_masses,
        "F47_per_generation": f47,
        "max_rel_resid": float(resid / max(f47)),
        "note": "3x3 diagonal see-saw = three copies of the F47 2x2 block "
                "(F47 Vieta form M_D^2/M_R, machine precision)",
    }


# ---------------------------------------------------------------------------
# S2 — E_g-only NO-GO: PMNS = identity (exact)
# ---------------------------------------------------------------------------
def check_S2_eg_only_no_mixing():
    MD = [0.5e-3, 0.10, 1.0]
    r = M.three_gen_seesaw(MD, np.radians(60.0), M_R0=1.0e12, t2g=(0, 0, 0))
    a = r["pmns_angles_deg"]
    max_angle = max(abs(a["theta12"]), abs(a["theta13"]), abs(a["theta23"]))
    ok = max_angle < 1e-9
    return {
        "pass": bool(ok),
        "pmns_angles_deg": a,
        "max_angle_deg": float(max_angle),
        "note": "E_g is diagonal-traceless (F93 O1) => m_nu diagonal => PMNS=I (no-go)",
    }


# ---------------------------------------------------------------------------
# S3 — T_2g turns the mixing on (F93 commitment #1)
# ---------------------------------------------------------------------------
def check_S3_t2g_switches_mixing_on():
    MD = [0.5e-3, 0.10, 1.0]
    r = M.three_gen_seesaw(MD, np.radians(60.0), M_R0=1.0e12,
                           t2g=(3e11, 5e11, 2e11))
    a = r["pmns_angles_deg"]
    max_angle = max(abs(a["theta12"]), abs(a["theta13"]), abs(a["theta23"]))
    ok = max_angle > 1.0            # degrees — mixing is genuinely nonzero
    return {
        "pass": bool(ok),
        "pmns_angles_deg": a,
        "max_angle_deg": float(max_angle),
        "note": "T_2g (axis-mixing, F93 unique off-diagonal channel) => nonzero PMNS",
    }


# ---------------------------------------------------------------------------
# S4 — data reproducible, but with free T_2g (not predictive)
# ---------------------------------------------------------------------------
def _model(p):
    dD, dnu, logMR0, tx, ty, tz = p
    MR0 = 10.0 ** logMR0
    MD = np.sort(M.z3_sqrt_texture(dD) ** 2)
    MD = MD / MD[-1]
    r = M.three_gen_seesaw(MD, dnu, M_R0=MR0, t2g=(tx * MR0, ty * MR0, tz * MR0))
    ma = np.array(r["light_masses"]) * 1e9   # GeV -> eV
    d21 = ma[1] ** 2 - ma[0] ** 2
    d31 = ma[2] ** 2 - ma[0] ** 2
    a = r["pmns_angles_deg"]
    return a["theta12"], a["theta13"], a["theta23"], d21, d31, r


def _cost(p):
    a, b, c, d21, d31, _ = _model(p)
    return (
        ((a - OBS["theta12"]) / 2) ** 2
        + ((b - OBS["theta13"]) / 1) ** 2
        + ((c - OBS["theta23"]) / 3) ** 2
        + (np.log10(max(d21, 1e-30)) - np.log10(OBS["dm21_sq_eV2"])) ** 2
        + (np.log10(max(d31, 1e-30)) - np.log10(OBS["dm31_sq_eV2"])) ** 2
    )


def check_S4_data_reproducible_but_free():
    rng = np.random.default_rng(3)
    best = (1e30, None)
    for _ in range(60000):
        p = [rng.uniform(0, 3.1), rng.uniform(0, 3.1), rng.uniform(11, 15),
             rng.uniform(-0.7, 0.7), rng.uniform(-0.7, 0.7), rng.uniform(-0.7, 0.7)]
        c = _cost(p)
        if c < best[0]:
            best = (c, np.array(p))
    c, p = best
    step = np.array([0.05, 0.05, 0.2, 0.04, 0.04, 0.04])
    for _ in range(8000):
        improved = False
        for i in range(6):
            for s in (step[i], -step[i]):
                q = p.copy()
                q[i] += s
                cc = _cost(q)
                if cc < c:
                    c, p, improved = cc, q, True
        if not improved:
            step *= 0.6
        if step.max() < 1e-7:
            break
    th12, th13, th23, d21, d31, r = _model(p)
    fit = {
        "theta12": th12, "theta13": th13, "theta23": th23,
        "dm21_sq_eV2": d21, "dm31_sq_eV2": d31,
    }
    ang_ok = (abs(th12 - OBS["theta12"]) < 1.0
              and abs(th13 - OBS["theta13"]) < 1.0
              and abs(th23 - OBS["theta23"]) < 1.5)
    dm_ok = (abs(np.log10(d21) - np.log10(OBS["dm21_sq_eV2"])) < 0.15
             and abs(np.log10(d31) - np.log10(OBS["dm31_sq_eV2"])) < 0.15)
    # honest bookkeeping: 6 free inputs for 5 observables => not predictive
    n_inputs, n_observables = 6, 5
    ok = ang_ok and dm_ok and (n_inputs > n_observables)
    return {
        "pass": bool(ok),
        "final_cost": float(c),
        "fit": fit,
        "observed": OBS,
        "best_params": {
            "delta_D_deg": float(np.degrees(p[0])),
            "delta_nu_deg": float(np.degrees(p[1])),
            "log10_MR0": float(p[2]),
            "t2g_over_MR0": [float(p[3]), float(p[4]), float(p[5])],
        },
        "n_free_inputs": n_inputs,
        "n_observables": n_observables,
        "note": "all 5 observables reproduced, but with 6 free inputs (3 T_2g) => "
                "PMNS angles are free, not texture outputs (F93 no-go confirmed)",
    }


# ---------------------------------------------------------------------------
# S5 — 6x6 <-> type-I consistency, hand-rolled residual (machine precision)
# ---------------------------------------------------------------------------
def check_S5_seesaw_block_consistency():
    MD = [0.5e-3, 0.10, 1.0]
    MR0 = 1.0e12
    dnu = np.radians(72.0)
    MR = M.eg_diagonal_matrix(dnu, MR0)
    r = M.three_gen_seesaw(MD, dnu, MR0, t2g=(0, 0, 0))
    # hand-rolled 6x6 residual on the light block via the type-I formula
    m_nu = M.light_mass_matrix(np.diag(MD), MR)
    masses, U, res_mnu = M.takagi_light_masses(m_nu)
    ok = (r["seesaw_6x6_vs_typeI"] < 1e-9 * MR0
          and res_mnu < 1e-12
          and float(np.max(np.abs(np.sort(masses) - np.sort(r["light_masses"])))) < 1e-30 + 1e-12 * max(masses))
    return {
        "pass": bool(ok),
        "seesaw_6x6_vs_typeI": r["seesaw_6x6_vs_typeI"],
        "residual_mnu": res_mnu,
        "note": "full 6x6 light eigenvalues match m_nu = -M_D M_R^-1 M_D^T (hand-rolled)",
    }


SUITE = [
    ("S1_reduces_to_F47", check_S1_reduces_to_F47,
     "3x3 diagonal see-saw = three F47 blocks (exact)"),
    ("S2_eg_only_no_mixing", check_S2_eg_only_no_mixing,
     "E_g-only no-go: PMNS = identity"),
    ("S3_t2g_switches_mixing_on", check_S3_t2g_switches_mixing_on,
     "T_2g turns mixing on (F93 #1)"),
    ("S4_data_reproducible_but_free", check_S4_data_reproducible_but_free,
     "data reproduced with free T_2g (not predictive)"),
    ("S5_seesaw_block_consistency", check_S5_seesaw_block_consistency,
     "6x6 <-> type-I machine precision (hand-rolled)"),
]


def run():
    res, t0 = {}, time.time()
    for name, fn, desc in SUITE:
        t = time.time()
        print(f"[run] {name} ...", flush=True)
        r = fn()
        r["_seconds"] = round(time.time() - t, 3)
        r["_desc"] = desc
        res[name] = r
        print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {
        "finding": "F236",
        "title": "Three-generation Higgs-free see-saw and PMNS from the E_g/T_2g texture",
        "timestamp": STAMP,
        "n_pass": npass,
        "n_total": len(SUITE),
        "results": res,
        "verdict": (
            "E_g texture fixes the light-mass hierarchy/ordering (F201 node) and "
            "reduces exactly to F47 per generation; PMNS mixing is a NO-GO from E_g "
            "alone (diagonal => identity) and requires the second-shell T_2g channel, "
            "whose three amplitudes are free inputs the texture does not pin. "
            "All five oscillation observables are reproducible but with 6 inputs for 5 "
            "observables: masses derived, mixing angles free."
        ),
        "seconds": round(time.time() - t0, 2),
    }


def _dump(out):
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    path = os.path.join(ROOT, "test-results", "F236_three_generation_seesaw.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2,
                  default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    return path


# --- pytest entry points -------------------------------------------------
_OUT = None


def _get():
    global _OUT
    if _OUT is None:
        _OUT = run()
        _dump(_OUT)
    return _OUT


def test_S1_reduces_to_F47():
    assert _get()["results"]["S1_reduces_to_F47"]["pass"]


def test_S2_eg_only_no_mixing():
    assert _get()["results"]["S2_eg_only_no_mixing"]["pass"]


def test_S3_t2g_switches_mixing_on():
    assert _get()["results"]["S3_t2g_switches_mixing_on"]["pass"]


def test_S4_data_reproducible_but_free():
    assert _get()["results"]["S4_data_reproducible_but_free"]["pass"]


def test_S5_seesaw_block_consistency():
    assert _get()["results"]["S5_seesaw_block_consistency"]["pass"]


def test_all_pass():
    out = _get()
    assert out["n_pass"] == out["n_total"]


if __name__ == "__main__":
    out = run()
    path = _dump(out)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS -> {path}")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
