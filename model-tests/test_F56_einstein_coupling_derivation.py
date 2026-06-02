"""
test_F56_einstein_coupling_derivation.py — deriving 16πG/c⁴ from the lattice
============================================================================
Tests the F56 derivation attempt (forks/gr_fork_F56_einstein_coupling_derivation.py).
The coupling is factored 16πG/c⁴ = (16π)·G·c⁻⁴ and each piece is examined:

C1  Coupling lock (EXACT).  Given Newton's 4π and the static-dust trace reversal
    (F55), the tensor coupling ξ in □h̄_μν = −ξ T_μν is forced to 16πG/c⁴, and
    the Einstein-tensor coupling to 8πG/c⁴.  No freedom.
C2  The 4π is lattice geometry.  (a) The bare discrete-Laplacian Green's function
    (NO 4π inserted) has far field −1/(4πr): 4π·C → 1.  (b) The same small-k
    isotropy gives a direction-independent light-cone slope c_lat = 1/√3 (F25/26).
    ⇒ the 4π in gravity and the isotropic light cone are one lattice fact.
C3  Sakharov: induced 1/(16πG) = BZ integral of ω(k)⁻¹ over the F26 dispersion
    scales as Λ² (exponent → 2 ⇒ G ∝ ℓ²), and its O(1) coefficient matches the
    continuum √d/(4π²) estimate — the phase-matching speed c_lat enters the
    coupling.  The lattice spacing in metres remains the one irreducible input.

Writes test-results/F56_einstein_coupling_derivation.json.

Run:
    python model-tests/test_F56_einstein_coupling_derivation.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

THIS = os.path.dirname(__file__)
SIM = os.path.abspath(os.path.join(THIS, "..", "ca-simulation"))
FORKS = os.path.join(SIM, "forks")
for p in (SIM, FORKS):
    if p not in sys.path:
        sys.path.insert(0, p)

import gr_fork_F56_einstein_coupling_derivation as f56   # noqa: E402


# ───────────────────────────────────────────────────────────────────
#  C1 — coupling lock (exact): 4π ⇒ 16π (and 8π for G_μν)
# ───────────────────────────────────────────────────────────────────

def test_C1_coupling_lock():
    res = f56.derive_tensor_coupling(newton_coeff=4.0 * np.pi, G=1.0, c=1.0)
    err_16 = abs(res["xi_over_(G_c4)"] - 16.0 * np.pi)
    err_8 = abs(res["einstein_over_(G_c4)"] - 8.0 * np.pi)
    ok = err_16 < 1e-12 and err_8 < 1e-12
    return {
        "name": "C1_coupling_lock_4pi_implies_16pi",
        "xi_over_(G/c4)": res["xi_over_(G_c4)"],
        "target_16pi": float(16 * np.pi),
        "einstein_tensor_over_(G/c4)": res["einstein_over_(G_c4)"],
        "target_8pi": float(8 * np.pi),
        "max_abs_err": float(max(err_16, err_8)),
        "note": "given Newton 4π + trace reversal, tensor coupling is forced",
        "tol": 1e-12,
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  C2 — the 4π is the lattice solid angle; lightcone isotropy (F25/26)
# ───────────────────────────────────────────────────────────────────

def test_C2_fourpi_is_lattice_solid_angle():
    L = 128
    G = f56.lattice_green_function_sc(L)
    fit = f56.fit_green_far_field_coefficient(G, sigma_lo=5.0, frac_hi=0.22)
    four_pi_C = fit["four_pi_C"]

    # same small-k isotropy → direction-independent c_lat
    dirs = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0)]
    slopes = np.array([f56.lightcone_slope(d) for d in dirs])
    c_lat = float(slopes.mean())
    iso_spread = float(slopes.max() - slopes.min())

    ok = (abs(four_pi_C - 1.0) < 0.03 and fit["fit_r2"] > 0.999
          and abs(c_lat - 1 / np.sqrt(3)) < 1e-3 and iso_spread < 1e-4)
    return {
        "name": "C2_fourpi_lattice_solid_angle_plus_isotropy",
        "four_pi_C": four_pi_C, "green_fit_r2": fit["fit_r2"],
        "c_lat_mean": c_lat, "c_lat_target": float(1 / np.sqrt(3)),
        "c_lat_isotropy_spread": iso_spread,
        "note": "4πC→1 (no 4π inserted) and isotropic c_lat are one lattice fact",
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  C3 — Sakharov: induced 1/G ∝ Λ² (⇒ G ∝ ℓ²); √d coefficient from c_lat
# ───────────────────────────────────────────────────────────────────

def test_C3_sakharov_scaling():
    Lambdas = np.array([0.10, 0.14, 0.20, 0.28, 0.40])
    sc = f56.sakharov_scaling(Lambdas, n_grid=96)
    p = sc["exponent_p"]

    # continuum coefficient check at the smallest Λ: I ≈ √d Λ²/(4π²)
    d = 3
    Lam0 = Lambdas[0]
    I0 = sc["I_values"][0]
    I_cont = np.sqrt(d) * Lam0**2 / (4 * np.pi**2)
    coeff_ratio = I0 / I_cont

    ok = (abs(p - 2.0) < 0.05) and (abs(coeff_ratio - 1.0) < 0.05)
    return {
        "name": "C3_sakharov_Lambda2_scaling",
        "exponent_p": p, "target_exponent": 2.0,
        "I_smallest_Lambda": I0,
        "continuum_estimate_sqrt_d_Lam2_over_4pi2": float(I_cont),
        "coefficient_ratio": float(coeff_ratio),
        "note": ("1/(16πG_ind) ∝ Λ²/c_lat ⇒ G ∝ ℓ²; c_lat=1/√d enters the "
                 "coefficient. Lattice spacing in metres is the one free input."),
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  Driver
# ───────────────────────────────────────────────────────────────────

def main():
    tests = [
        test_C1_coupling_lock,
        test_C2_fourpi_is_lattice_solid_angle,
        test_C3_sakharov_scaling,
    ]
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:  # noqa: BLE001
            import traceback
            results.append({"name": t.__name__, "status": "ERROR",
                            "error": repr(e), "trace": traceback.format_exc()})

    overall = "PASS" if all(r.get("status") == "PASS" for r in results) else "FAIL"
    out = {
        "finding": "F56",
        "title": "Deriving the Einstein coupling 16piG/c4 from the lattice + F25/F26",
        "date": "2026-05-29",
        "overall": overall,
        "tests": results,
    }
    out_dir = os.path.abspath(os.path.join(THIS, "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "F56_einstein_coupling_derivation.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("=" * 72)
    print("F56 — deriving the Einstein coupling 16πG/c⁴ from the lattice + F25/F26")
    print("=" * 72)
    for r in results:
        print(f"  [{r.get('status','?'):>5}]  {r['name']}")
        for kk, vv in r.items():
            if kk in ("name", "status", "trace"):
                continue
            print(f"            {kk}: {vv}")
    print("-" * 72)
    print(f"  OVERALL: {overall}")
    print(f"  wrote {path}")
    return out


if __name__ == "__main__":
    main()
