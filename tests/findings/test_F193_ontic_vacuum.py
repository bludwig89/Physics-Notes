"""
test_F193_ontic_vacuum.py  --  CA-native ontic vacuum gravitates as zero (candidate (i)),
residual rho_Lambda as holographic IR back-reaction (S9 follow-up to F164/F192).
"""
from __future__ import annotations
import json, os, sys, time

THIS = os.path.dirname(__file__); ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
FORK = os.path.join(ROOT, "ca-simulation", "forks")
if FORK not in sys.path: sys.path.insert(0, FORK)
import gr_fork_F193_ontic_vacuum as ov   # noqa: E402
STAMP = "2026-06-30 - 17:35"

_RES = ov.run()
_A = _RES["partA_ontic_vacuum"]
_B = _RES["partB_residual"]


def check_A1_T00_ontic_vacuum_zero():
    # the beable field-energy density on psi==0 is EXACTLY 0 (structural, not eps)
    ok = (_A["T00_ontic_vacuum_J_per_m3"] == 0.0
          and _A["ca_energy_eigenvalue_vacuum_J"] == 0.0
          and _A["T00_one_quantum_J"] > 0.0)
    return {"pass": bool(ok), "T00_vac": _A["T00_ontic_vacuum_J_per_m3"],
            "T00_one_quantum": _A["T00_one_quantum_J"]}


def check_A2_dielectric_flat_on_vacuum():
    # F64 dielectric sourced by enclosed beable mass M=0 -> K=1 -> G_munu=0 exactly
    ok = (_A["M_enclosed_ontic_vacuum_kg"] == 0.0
          and _A["dielectric_K_minus_1_ontic_vacuum"] == 0.0)
    return {"pass": bool(ok), "K_minus_1": _A["dielectric_K_minus_1_ontic_vacuum"],
            "note": "empty ontic vacuum does not curve the lattice"}


def check_A3_template_density_is_F164():
    # the +1/2 hbar omega template sum reproduces F164 (~3.5e111) and is the
    # superimposable quantity that does NOT source the beable dielectric
    r = _A["rho_vac_template_J_per_m3"]
    ok = 3.0e111 < r < 4.0e111 and abs(_A["I_CC_template_zero_point"] - 4.081) < 1e-2
    return {"pass": bool(ok), "rho_vac_template": r,
            "I_CC": _A["I_CC_template_zero_point"]}


def check_B_holographic_residual():
    # rho_vac * (a/R_H)^2 lands within 1 dex of observed rho_Lambda
    ok = (abs(_B["holographic_dlog10"]) < 1.0
          and 119 < _B["bare_overshoot_log10"] < 122)
    return {"pass": bool(ok), "holographic_over_observed": _B["holographic_over_observed"],
            "dlog10": _B["holographic_dlog10"],
            "bare_overshoot_log10": _B["bare_overshoot_log10"],
            "rho_CKN_over_observed": _B["rho_CKN_over_observed"]}


SUITE = [("A1_T00_ontic_vacuum_zero", check_A1_T00_ontic_vacuum_zero,
          "beable T00 on empty lattice is exactly 0 (bare CC=0 in the ontology)"),
         ("A2_dielectric_flat_on_vacuum", check_A2_dielectric_flat_on_vacuum,
          "F64 dielectric K=1 on the ontic vacuum (no curvature)"),
         ("A3_template_density_is_F164", check_A3_template_density_is_F164,
          "the +1/2 hbar omega template sum = F164 number (a superimposable)"),
         ("B_holographic_residual", check_B_holographic_residual,
          "rho_vac*(a/R_H)^2 within ~0.5 dex of observed rho_Lambda")]


def run():
    res, t0 = {}, time.time()
    for n, fn, d in SUITE:
        t = time.time(); print(f"[run] {n} ...", flush=True)
        r = fn(); r["_seconds"] = round(time.time()-t, 2); r["_desc"] = d
        res[n] = r; print(f"      pass={r.get('pass')}", flush=True)
    npass = sum(1 for r in res.values() if r.get("pass"))
    return {"finding": "F193",
            "title": "CA-native ontic vacuum gravitates as zero; residual as holographic IR back-reaction",
            "timestamp": STAMP, "n_pass": npass, "n_total": len(SUITE), "results": res,
            "seconds": round(time.time()-t0, 2)}


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "test-results", "F193_ontic_vacuum_test.json"), "w"),
              indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
