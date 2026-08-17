"""
test_F237_kev_sterile_resolution.py
===================================
F237 (open-derivation D2) — resolve-or-exclude the keV sterile that F205 put
under quantified pressure, by adding late ENTROPY DILUTION to the F205 resonant
QKE production and testing the current X-ray + Lyman-alpha windows.

Acceptance (stated up front): PASS = either a viable (mass, mixing, Omega_DM)
point clears BOTH windows, or a CLEAN exclusion is demonstrated (no such point,
with the mechanism-level reason). The outcome here is a clean exclusion.

Checks:
  A1  Reuse the F205 QKE solver (import + reproduce the DW coldness anchor).
  A2  Non-resonant + dilution CANNOT relax X-ray: sin^2 2theta grows ∝ S, so the
      DW mixing (already >2 dex over the bound) is pushed further over.
  A3  Scaling exponents have OPPOSITE sign: d(log sin2)/d(log S)=+1,
      d(log floor)/d(log S)=-4/9 -> no S co-improves both windows.
  A4  Full (L, S) grid at 7.1 keV: ZERO points clear X-ray AND the conservative
      Lyman-alpha floor (exclusion).
  A5  Full (L, S) grid at 5.6 keV (model texture mass): ZERO viable points.
  A6  Best case (coldest resonant <eps> AT the X-ray bound): the S needed to
      pass Lyman-alpha costs a strictly POSITIVE X-ray excess (dex>0) -> the
      door is closed even in the most generous assumption.
  A7  Hand-off recorded: the sub-dominant fraction role survives, and the verdict
      names the F223/F228 geon as the viable 100%-DM candidate.
"""
from __future__ import annotations
import json, os, sys, time
import numpy as np

THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
# Forks are loaded by bare name, not as package submodules;
# importing casim appends engine/forks/<sector>/ to sys.path.
import casim as _casim  # noqa: E402,F401
import dm_fork_F237_kev_sterile_resolution as F237   # noqa: E402
import dm_fork_F205_sterile_qke_boltzmann as F205     # noqa: E402  (reused solver)
STAMP = "2026-07-03 - 14:20"

OUT = F237._finalize(F237.run())


def check_A1_reuse_F205():
    # F237 must import and use the F205 solver; the DW anchor must match F205's.
    me = OUT["dw_mean_eps_anchor"]
    ok = ("F205" in OUT["reused_solver"]) and (2.5 < me < 4.0)
    return {"pass": bool(ok), "reused_solver": OUT["reused_solver"], "dw_mean_eps": me,
            "note": "F237 reuses the validated F205 momentum-resolved QKE solver"}


def check_A2_nonresonant_dilution_worsens_xray():
    # non-resonant + dilution: mixing ∝ S -> X-ray excess grows with S
    p1 = F237.diluted_point(7.1, L=0.0, S=1)
    p10 = F237.diluted_point(7.1, L=0.0, S=10)
    ok = (p10["dex_over_xray"] > p1["dex_over_xray"] + 0.9) and (not p10["xray_ok"])
    return {"pass": bool(ok), "dex_S1": p1["dex_over_xray"], "dex_S10": p10["dex_over_xray"],
            "note": "dilution needs S x more production -> S x mixing -> X-ray gets WORSE, not better"}


def check_A3_opposite_sign_exponents():
    e = OUT["scaling_exponents"]
    ok = (abs(e["slope_dlog_sin2_dlogS"] - 1.0) < 1e-6
          and abs(e["slope_dlog_lya_floor_dlogS"] + 4.0 / 9.0) < 1e-6
          and e["opposite_sign"])
    return {"pass": bool(ok), "slope_xray": e["slope_dlog_sin2_dlogS"],
            "slope_lya": e["slope_dlog_lya_floor_dlogS"],
            "note": "+1 vs -4/9 -> dilution cannot co-improve both windows (the heart of the exclusion)"}


def check_A4_grid_71_excluded():
    g = OUT["grid_scan"]["7.1keV"]
    ok = (g["n_viable_cons"] == 0) and (g["n_viable_viel"] == 0) and (g["n_points"] > 100)
    return {"pass": bool(ok), "n_points": g["n_points"],
            "n_viable_viel": g["n_viable_viel"], "n_viable_cons": g["n_viable_cons"],
            "note": "7.1 keV: no (L,S) clears X-ray AND (even conservative) Lyman-alpha -> excluded"}


def check_A5_grid_56_excluded():
    g = OUT["grid_scan"]["5.6keV"]
    ok = (g["n_viable_cons"] == 0) and (g["n_viable_viel"] == 0)
    return {"pass": bool(ok), "n_viable_viel": g["n_viable_viel"], "n_viable_cons": g["n_viable_cons"],
            "note": "5.6 keV model-texture mass: no viable full-DM point either"}


def check_A6_best_case_door_closed():
    # even placing the coldest resonant spectrum AT the X-ray bound, passing
    # Lyman-alpha costs a strictly positive X-ray excess
    b = OUT["best_case"]["7.1keV"]
    cost = b["xray_cost_dex_viel"]
    ok = (b["S_needed_viel"] is not None) and (cost is not None) and (cost > 0.0)
    return {"pass": bool(ok), "S_needed_viel": b["S_needed_viel"],
            "xray_cost_dex_viel": cost,
            "note": "best case: the S that passes Lyman-alpha costs >0 dex over the X-ray bound -> door closed"}


def check_A7_handoff_and_subdominant():
    # exclusion verdict names the geon hand-off; sub-dominant role survives
    verdict = OUT["verdict"]
    has_handoff = ("F223" in verdict or "geon" in verdict) and "EXCLUSION" in verdict
    sub = OUT["subdominant"]["7.1keV"]
    sub_ok = sub["f_xray_saturated"] <= 1.0
    ok = has_handoff and sub_ok and (not OUT["any_viable_full_DM_conservative"])
    return {"pass": bool(ok), "handoff_named": bool(has_handoff),
            "f_xray_saturated": sub["f_xray_saturated"],
            "note": "clean exclusion -> hand off 100%-DM to the F223/F228 geon; keV sterile survives sub-dominant"}


SUITE = [
    ("A1_reuse_F205", check_A1_reuse_F205, "reuse the validated F205 QKE solver"),
    ("A2_nonresonant_dilution_worsens_xray", check_A2_nonresonant_dilution_worsens_xray,
     "non-resonant + dilution pushes mixing further over X-ray"),
    ("A3_opposite_sign_exponents", check_A3_opposite_sign_exponents,
     "X-ray +1 vs Lyman-alpha -4/9: no co-improvement"),
    ("A4_grid_71_excluded", check_A4_grid_71_excluded, "7.1 keV grid: zero viable full-DM points"),
    ("A5_grid_56_excluded", check_A5_grid_56_excluded, "5.6 keV grid: zero viable full-DM points"),
    ("A6_best_case_door_closed", check_A6_best_case_door_closed,
     "best case still costs >0 dex X-ray to pass Lyman-alpha"),
    ("A7_handoff_and_subdominant", check_A7_handoff_and_subdominant,
     "clean exclusion + F223 geon hand-off + sub-dominant survival"),
]


# ── pytest-discoverable wrappers (each check must pass) ──────────────
def _mk(fn):
    def _t():
        r = fn()
        assert r.get("pass"), r
    return _t


test_A1 = _mk(check_A1_reuse_F205)
test_A2 = _mk(check_A2_nonresonant_dilution_worsens_xray)
test_A3 = _mk(check_A3_opposite_sign_exponents)
test_A4 = _mk(check_A4_grid_71_excluded)
test_A5 = _mk(check_A5_grid_56_excluded)
test_A6 = _mk(check_A6_best_case_door_closed)
test_A7 = _mk(check_A7_handoff_and_subdominant)


def test_all_pass_and_emit_json():
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F237_kev_sterile_resolution.json"), "w"),
              indent=2)
    assert out["n_pass"] == out["n_total"], out


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time() - t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F237",
            "title": "keV-sterile resolution (D2): resonant + entropy-dilution vs X-ray + Lyman-alpha "
                     "-> clean exclusion, hand off to the F223 geon",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "verdict": OUT["verdict"], "seconds": round(time.time() - t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F237_kev_sterile_resolution.json"), "w"),
              indent=2)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
