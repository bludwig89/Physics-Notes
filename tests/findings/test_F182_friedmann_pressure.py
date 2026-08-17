"""
test_F182_friedmann_pressure.py
===============================
F182 -- cosmology under the F178 full-tensor source: pressure gravitates, so
radiation (p = rho c^2/3) enters the acceleration equation as rho + 3p = 2 rho,
giving the standard Friedmann evolution.  The demoted energy-only law would
have mis-weighted the radiation-dominated early universe by exactly a factor 2.

Checks:
  A1  EXACT (sympy): Friedmann I (H^2 = (8 pi G/3) rho) + continuity
      (rho' + 3H(rho + p/c^2) = 0) imply the acceleration equation
      a''/a = -(4 pi G/3)(rho + 3p/c^2).  The +3p term is FORCED by the Bianchi
      identity; the energy-only a''/a = -(4 pi G/3) rho is consistent only if
      p = 0.  (Self-consistency of the full-tensor source.)
  A2  EXACT (sympy): the energy-only law omits the source fraction
      3w/(1+3w) -- 1/2 for radiation, 0 for dust (matches F173's interior result).
  N1  NUMERIC: radiation (w=1/3) gives a ~ t^{1/2} and rho ~ a^{-4}.
  N2  NUMERIC: matter (w=0) gives a ~ t^{2/3} and rho ~ a^{-3}.
  N3  deceleration parameter q: full-tensor q = (1/2)(1+3w) (radiation 1,
      matter 1/2); energy-only q = 1/2 always -> radiation mis-weighted (1 vs 1/2).
  N4  consistency: the numerical a''/a of the Friedmann-I solution matches the
      full-tensor -(4 pi G/3)(rho+3p), NOT the energy-only -(4 pi G/3) rho, in
      the radiation era (ratio -> 2).

Run:  python tests/findings/test_F182_friedmann_pressure.py
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
import sympy as sp

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, "..", ".."))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.interactions import cosmology as cc                  # noqa: E402

STAMP = "2026-06-30 - 02:45"


def check_A1_bianchi_forces_3p():
    """Differentiate Friedmann I, substitute continuity -> acceleration eq.

    Work with H as a free symbol and impose Friedmann I (H^2 = (8 pi G/3) rho)
    by substitution at the end, so a''/a = H' + H^2 reduces to a rho-expression.
    """
    G, c, H, rho, w = sp.symbols("G c H rho w", positive=True)
    k = sp.Rational(8, 3) * sp.pi * G            # 8 pi G / 3
    p = w * rho * c**2
    # continuity: rho' = -3 H (rho + p/c^2)
    rho_dot = -3 * H * (rho + p / c**2)
    # differentiate Friedmann I: 2 H H' = k rho'  =>  H' = k rho'/(2H)  (H cancels)
    Hdot = sp.simplify(k * rho_dot / (2 * H))
    # a''/a = H' + H^2, then impose Friedmann I: H^2 = k rho
    accel_over_a = sp.simplify((Hdot + H**2).subs(H**2, k * rho))
    target_full = sp.simplify(-sp.Rational(4, 3) * sp.pi * G * (rho + 3 * p / c**2))
    target_energy = sp.simplify(-sp.Rational(4, 3) * sp.pi * G * rho)
    matches_full = sp.simplify(accel_over_a - target_full) == 0
    matches_energy_only_if_p0 = sp.simplify((accel_over_a - target_energy).subs(w, 0)) == 0
    matches_energy_general = sp.simplify(accel_over_a - target_energy) == 0
    return {"pass": bool(matches_full and matches_energy_only_if_p0
                         and not matches_energy_general),
            "derived_accel_over_a": str(accel_over_a),
            "target_full(rho+3p)": str(target_full),
            "matches_full": bool(matches_full),
            "energy_only_consistent_only_if_p=0": bool(matches_energy_only_if_p0
                                                       and not matches_energy_general)}


def check_A2_omitted_fraction():
    w = sp.symbols("w")
    frac = sp.simplify(3 * w / (1 + 3 * w))
    rad = sp.simplify(frac.subs(w, sp.Rational(1, 3)))
    dust = sp.simplify(frac.subs(w, 0))
    return {"pass": bool(rad == sp.Rational(1, 2) and dust == 0),
            "omitted_fraction_expr": str(frac),
            "radiation_w=1/3": str(rad), "dust_w=0": str(dust)}


def check_N1_radiation():
    w = 1.0 / 3.0
    t, a = cc.integrate_scale_factor(w, t_end=4.0, a_init=1e-3, dt=2e-5)
    n = cc.fit_power_law_exponent(t, a, frac=0.5)
    # rho ~ a^{-4}
    rho = cc.rho_of_a(a, w)
    slope = float(np.polyfit(np.log(a[len(a)//2:]), np.log(rho[len(a)//2:]), 1)[0])
    return {"pass": bool(abs(n - 0.5) < 2e-3 and abs(slope + 4.0) < 1e-6),
            "exponent_a_vs_t": n, "expected": 0.5,
            "rho_vs_a_slope": slope, "expected_rho_slope": -4.0}


def check_N2_matter():
    w = 0.0
    t, a = cc.integrate_scale_factor(w, t_end=4.0, a_init=1e-3, dt=2e-5)
    n = cc.fit_power_law_exponent(t, a, frac=0.5)
    rho = cc.rho_of_a(a, w)
    slope = float(np.polyfit(np.log(a[len(a)//2:]), np.log(rho[len(a)//2:]), 1)[0])
    return {"pass": bool(abs(n - 2.0/3.0) < 2e-3 and abs(slope + 3.0) < 1e-6),
            "exponent_a_vs_t": n, "expected": 2.0/3.0,
            "rho_vs_a_slope": slope, "expected_rho_slope": -3.0}


def check_N3_deceleration():
    q_rad_full = cc.deceleration_parameter(1.0/3.0, "full")
    q_mat_full = cc.deceleration_parameter(0.0, "full")
    q_rad_energy = cc.deceleration_parameter(1.0/3.0, "energy")
    return {"pass": bool(abs(q_rad_full - 1.0) < 1e-12
                         and abs(q_mat_full - 0.5) < 1e-12
                         and abs(q_rad_energy - 0.5) < 1e-12),
            "q_radiation_full": q_rad_full, "q_matter_full": q_mat_full,
            "q_radiation_energy_only": q_rad_energy,
            "note": "full-tensor radiation q=1; energy-only would give 1/2 (factor-2 mis-weight)"}


def check_N4_numerical_consistency():
    # numerically differentiate a(t) twice in the radiation era; compare a''/a
    # to the full-tensor and energy-only predictions.
    w = 1.0 / 3.0
    t, a = cc.integrate_scale_factor(w, t_end=4.0, a_init=1e-3, dt=2e-5)
    i = len(t) // 2                       # well into the power-law regime
    dt = t[1] - t[0]
    a_pp = (a[i+1] - 2*a[i] + a[i-1]) / dt**2
    num = a_pp / a[i]
    full = cc.accel_over_a(a[i], w, source="full")
    energy = cc.accel_over_a(a[i], w, source="energy")
    return {"pass": bool(abs(num / full - 1.0) < 1e-3
                         and abs(full / energy - 2.0) < 1e-9),
            "numerical_accel_over_a": float(num),
            "full_tensor_pred": float(full), "energy_only_pred": float(energy),
            "num/full": float(num / full), "full/energy_ratio": float(full / energy)}


SUITE = [
    ("A1_bianchi_forces_3p", check_A1_bianchi_forces_3p,
     "Friedmann I + continuity => a''/a=-(4piG/3)(rho+3p); energy-only consistent only if p=0 (sympy)"),
    ("A2_omitted_fraction", check_A2_omitted_fraction,
     "energy-only omits 3w/(1+3w): radiation 1/2, dust 0 (sympy)"),
    ("N1_radiation_t_half", check_N1_radiation,
     "radiation: a ~ t^{1/2}, rho ~ a^{-4}"),
    ("N2_matter_t_twothirds", check_N2_matter,
     "matter: a ~ t^{2/3}, rho ~ a^{-3}"),
    ("N3_deceleration", check_N3_deceleration,
     "q: radiation 1 / matter 1/2 (full); energy-only 1/2 (radiation mis-weighted)"),
    ("N4_numerical_consistency", check_N4_numerical_consistency,
     "numerical a''/a matches full-tensor (rho+3p), 2x the energy-only law"),
]


def run():
    results, t0 = {}, time.time()
    for name, fn, desc in SUITE:
        t = time.time()
        print(f"[run] {name} ...", flush=True)
        r = fn()
        r["_seconds"] = round(time.time() - t, 2)
        r["_desc"] = desc
        results[name] = r
        print(f"      pass={r.get('pass')}  ({r['_seconds']}s)", flush=True)
    n_pass = sum(1 for r in results.values() if r.get("pass"))
    out = {"finding": "F182",
           "title": "FLRW cosmology under the F178 full-tensor source: radiation "
                    "gravitates with pressure -> standard Friedmann",
           "timestamp": STAMP, "n_pass": n_pass, "n_total": len(SUITE),
           "results": results, "seconds": round(time.time() - t0, 2)}
    return out


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    with open(os.path.join(ROOT, "test-results", "F182_friedmann_pressure.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS  ({out['seconds']}s)")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
