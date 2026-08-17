"""
test_F254_t2g_pmns_selector.py
==============================
F254 — Is there a lattice selector for the T_2g PMNS channel (open-derivation
D1 follow-up to F236)?

Acceptance test (stated up front):
  Find a symmetry / dynamical selector on the BCC lattice that fixes the three
  second-shell T_2g axis-mixing amplitudes (t_xy, t_yz, t_zx) — and hence the
  PMNS angles — from geometry, reproducing NuFIT with NO free mixing inputs; OR
  a clean proof that the T_2g amplitudes are genuinely free (parallel to D3's
  free geon-abundance beta).

Result encoded here (the SECOND branch, sharpened into a theorem):
  - T1  The E_g-stabiliser D_2h acts on the T_2g triplet as three INEQUIVALENT
        nontrivial 1-d irreps (B_1g, B_2g, B_3g): distinct, zero-sum characters.
        => no residual symmetry relates the three amplitudes.               [T1]
  - T2  The democratic (S_3-symmetric) point t_xy=t_yz=t_zx is invariant under
        only {+I,-I} of D_2h => not symmetry-protected; and the F92 equipartition
        selector cannot apply (it equalises a single degenerate multiplet, but
        the E_g condensate splits the triplet into three inequivalent irreps). [T2]
  - T3  Numerical no-go: democratic and single-channel T_2g both miss NuFIT-5.2
        by hundreds of deg^2; only the full THREE-amplitude fit reaches the data
        (~1e-11 deg), with exactly 3 inputs for 3 angles (no predictive slack).  [T3]
  - T4  Consistency with F236: E_g-only still gives PMNS = 1 exactly (no-go
        carried over) — the selector search does not disturb the mass sector.  [T4]

Verdict: the T_2g amplitudes are GENUINELY FREE — three independent order
parameters in three inequivalent D_2h channels. The D1 selector provably does
not exist among residual-symmetry / equipartition mechanisms. A negative
(free-input) closure, recorded honestly per the House Rules.
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

from casim.engine.particles import majorana as M          # noqa: E402
from casim.engine.particles import derive_t2g_pmns as D  # noqa: E402

STAMP = "2026-07-16 - 10:40"

OBS = {"theta12": 33.4, "theta13": 8.6, "theta23": 49.0}


# ---------------------------------------------------------------------------
# T1 — D_2h acts on the T_2g triplet as three inequivalent 1-d irreps
# ---------------------------------------------------------------------------
def check_T1_three_inequivalent_irreps():
    irr = D.analyse_irreps()
    ok = (irr["all_nontrivial_1d"] and irr["all_inequivalent"])
    return {
        "pass": bool(ok),
        "characters": irr["characters"],
        "all_nontrivial_1d": irr["all_nontrivial_1d"],
        "all_inequivalent": irr["all_inequivalent"],
        "note": "t_xy,t_yz,t_zx transform as B_1g,B_2g,B_3g of D_2h — three "
                "inequivalent nontrivial 1-d irreps; no residual symmetry "
                "relates them.",
    }


# ---------------------------------------------------------------------------
# T2 — democracy is not symmetry-protected; equipartition cannot apply
# ---------------------------------------------------------------------------
def check_T2_democracy_unprotected():
    irr = D.analyse_irreps()
    order = irr["democratic_stabiliser_order"]
    # democratic (1,1,1) fixed by only +I and -I => order exactly 2
    ok = (order == 2)
    return {
        "pass": bool(ok),
        "democratic_stabiliser_order": order,
        "note": "democratic point invariant under only {+I,-I} of D_2h (order 2 "
                "of 8): not protected. F92 equipartition equalises ONE degenerate "
                "multiplet, but the E_g condensate splits T_2g into three "
                "inequivalent irreps => no multiplet to equipartition over.",
    }


# ---------------------------------------------------------------------------
# T3 — one-parameter symmetric ansaetze fail; only 3 free amplitudes reach data
# ---------------------------------------------------------------------------
def check_T3_oneparameter_nogo():
    dem = D.scan_democratic()
    singles = D.scan_single_channel()
    full = D.fit_full()
    # democratic must be far from data; full fit must reach it
    dem_far = dem["cost"] > 100.0
    singles_far = all(b["cost"] > 100.0 for b in singles.values())
    full_reaches = full["max_abs_deg"] < 1e-6
    ok = dem_far and singles_far and full_reaches
    return {
        "pass": bool(ok),
        "democratic_cost_deg2": dem["cost"],
        "democratic_angles": [round(x, 2) for x in dem["angles"]],
        "single_channel_costs_deg2": {k: v["cost"] for k, v in singles.items()},
        "full_fit_max_abs_deg": full["max_abs_deg"],
        "target": OBS,
        "note": "democratic & single-channel T_2g miss NuFIT by >100 deg^2; only "
                "the full 3-amplitude fit reaches it (3 inputs / 3 angles, no slack).",
    }


# ---------------------------------------------------------------------------
# T4 — E_g-only still forces PMNS = 1 (F236 no-go carried over)
# ---------------------------------------------------------------------------
def check_T4_eg_only_identity():
    MD = [0.5e-3, 0.10, 1.0]
    MR0 = 1.0e12
    dnu = np.radians(72.0)
    r = M.three_gen_seesaw(MD, dnu, MR0, t2g=(0, 0, 0))
    ang = r["pmns_angles_deg"]
    max_angle = max(abs(ang["theta12"]), abs(ang["theta13"]), abs(ang["theta23"]))
    ok = max_angle < 1e-6
    return {
        "pass": bool(ok),
        "pmns_angles_deg": ang,
        "max_angle_deg": float(max_angle),
        "note": "E_g-only => PMNS = 1 to <1e-6 deg (F236 S2 no-go preserved).",
    }


CHECKS = [
    ("T1_three_inequivalent_irreps", check_T1_three_inequivalent_irreps),
    ("T2_democracy_unprotected", check_T2_democracy_unprotected),
    ("T3_oneparameter_nogo", check_T3_oneparameter_nogo),
    ("T4_eg_only_identity", check_T4_eg_only_identity),
]


def main():
    t0 = time.time()
    results = {}
    n_pass = 0
    for name, fn in CHECKS:
        r = fn()
        results[name] = r
        ok = r.get("pass", False)
        n_pass += int(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {r.get('note', '')}")
    summary = {
        "finding": "F254",
        "stamp": STAMP,
        "n_pass": n_pass,
        "n_total": len(CHECKS),
        "elapsed_s": round(time.time() - t0, 2),
        "results": results,
    }
    out_dir = os.path.join(ROOT, "test-results")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "F254_t2g_pmns_selector.json")
    with open(out, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"\n{n_pass}/{len(CHECKS)} PASS  ({summary['elapsed_s']} s)  -> {out}")
    return n_pass == len(CHECKS)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
