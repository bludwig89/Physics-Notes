"""
test_F55_spatial_metric_backreaction.py — Einstein's factor-2 from trace reversal
=================================================================================
Tests the F55 hypothesis (forks/gr_fork_F55_spatial_metric_backreaction.py):
sourcing the spatial metric B from the SAME mass density as the rest leg, via the
linearised-Einstein trace reversal, promotes F52's Newtonian factor-1 deflection
to Einstein's factor-2 — self-consistently, not imposed.

Tests
-----
J1  Trace-reversal identity.  For a static-dust source (T_ij = 0) the trace
    reversal forces the spatial metric perturbation to EQUAL the temporal one:
    h_ij = h₀₀ pointwise.  Verified to machine precision on a Poisson field.
J2  Redshift unchanged.  Adding B does not touch the rest leg, so the redshift
    stays factor-1 (Δν/ν = Δφ/c²), reproducing F52-H2.
J3  Deflection → factor-2.  Eikonal coefficient K ≡ αbc²/GM with the
    trace-reversed (A,B): K → 4 (Einstein), vs F52's rest-only K = 2.  Checked on
    both the analytic φ and the self-consistent lattice field.
J4  Uniqueness.  Sweeping the spatial fraction λ (B = 1 + λ(B_GR−1)) gives a
    linear K(λ) = 2(1+λ): K(0)=2, K(1)=4.  Only the trace-reversal value λ=1
    yields factor-2 — the model is not free to give any answer.
J5  Consistency.  The trace-reversed (A,B) equals gr_fork_E_tensor's *linearised*
    metric bit-for-bit (no silent divergence from the project's metric infra).

Writes test-results/F55_spatial_metric_backreaction.json.

Run:
    python model-tests/test_F55_spatial_metric_backreaction.py
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

import gr_fork_F55_spatial_metric_backreaction as f55   # noqa: E402
import gr_fork_E_tensor as forkE                        # noqa: E402
from ca_emqg import gaussian_mass_3d                     # noqa: E402

C0 = 0.5
G = 1.0


def _analytic_phi_slice(L, GM, center_xy):
    x = np.arange(L) - center_xy[0]
    y = np.arange(L) - center_xy[1]
    X, Y = np.meshgrid(x, y, indexing="ij")
    r = np.sqrt(X**2 + Y**2)
    r[r < 1e-9] = 1e-9
    return -GM / r


# ───────────────────────────────────────────────────────────────────
#  J1 — trace-reversal identity: h_ij = h00 for static dust
# ───────────────────────────────────────────────────────────────────

def test_J1_trace_reversal_identity():
    L = 64
    rho = gaussian_mass_3d(L, M=0.05, sigma=3.0)
    phi = f55.newtonian_potential(rho, G=G)
    tr = f55.trace_reversed_perturbation(phi, C0)
    # spatial perturbation must equal temporal, although T_ij = 0
    resid = float(np.max(np.abs(tr["hij"] - tr["h00"])))
    # and each equals -2φ/c²
    resid_value = float(np.max(np.abs(tr["h00"] - (-2.0 * phi / C0**2))))
    ok = resid < 1e-15 and resid_value < 1e-15
    return {
        "name": "J1_trace_reversal_identity",
        "max_abs_hij_minus_h00": resid,
        "max_abs_h00_minus_(-2phi/c2)": resid_value,
        "note": "static dust T_ij=0 yet h_ij=h00 — the extra factor-1",
        "tol": 1e-15,
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  J2 — redshift still factor-1 (rest leg untouched by B)
# ───────────────────────────────────────────────────────────────────

def test_J2_redshift_unchanged():
    GM = 0.02
    pairs = [(6.0, 16.0), (8.0, 22.0), (10.0, 28.0), (12.0, 30.0)]
    ratios = []
    for r_n, r_f in pairs:
        phi_n = np.array([-GM / r_n])
        phi_f = np.array([-GM / r_f])
        A_n, _ = f55.metric_trace_reversed(phi_n, C0)
        A_f, _ = f55.metric_trace_reversed(phi_f, C0)
        tau_n = np.sqrt(np.abs(A_n))[0]
        tau_f = np.sqrt(np.abs(A_f))[0]
        dnu = tau_n / tau_f - 1.0
        pred_GR = -(float(phi_f[0]) - float(phi_n[0])) / C0**2
        ratios.append(dnu / pred_GR)
    ratios = np.array(ratios)
    ok = abs(ratios.mean() - 1.0) < 0.05
    return {
        "name": "J2_redshift_unchanged_factor1",
        "mean_ratio_GR": float(ratios.mean()),
        "target_ratio": 1.0,
        "note": "sourcing B leaves the rest-leg redshift at factor-1",
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  J3 — deflection becomes factor-2 (analytic + self-consistent)
# ───────────────────────────────────────────────────────────────────

def test_J3_deflection_factor2():
    L = 256
    GM = 0.02
    center = (L // 2, L // 2)
    phi = _analytic_phi_slice(L, GM, center)
    A, B = f55.metric_trace_reversed(phi, C0)
    A_rest, B_rest = f55.metric_spatial_fraction(phi, C0, lam=0.0)  # B=1

    impacts = [8, 12, 16]
    window = 90
    K_full, K_rest = [], []
    for b in impacts:
        a_full = f55.eikonal_deflection_AB(A, B, C0, impact_index=center[1] + b,
                                           window=window)
        a_rest = f55.eikonal_deflection_AB(A_rest, B_rest, C0,
                                           impact_index=center[1] + b,
                                           window=window)
        K_full.append(a_full * b * C0**2 / GM)
        K_rest.append(a_rest * b * C0**2 / GM)
    K_full = np.array(K_full)
    K_rest = np.array(K_rest)

    # self-consistent lattice cross-check (weak field), ratio only
    Ls = 128
    rho = gaussian_mass_3d(Ls, M=0.03, sigma=3.0)
    phi_sc = f55.newtonian_potential(rho, G=G)[:, :, Ls // 2]
    A_sc, B_sc = f55.metric_trace_reversed(phi_sc, C0)
    A_sc_r, B_sc_r = f55.metric_spatial_fraction(phi_sc, C0, lam=0.0)
    b = 14
    a_full_sc = f55.eikonal_deflection_AB(A_sc, B_sc, C0,
                                          impact_index=Ls // 2 + b, window=40)
    a_rest_sc = f55.eikonal_deflection_AB(A_sc_r, B_sc_r, C0,
                                          impact_index=Ls // 2 + b, window=40)
    ratio_sc = a_full_sc / a_rest_sc

    ok = (abs(K_full.mean() - 4.0) < 0.30 and
          abs(K_rest.mean() - 2.0) < 0.15 and
          abs(ratio_sc - 2.0) < 0.05)
    return {
        "name": "J3_deflection_factor2",
        "K_full_mean": float(K_full.mean()),
        "K_rest_mean": float(K_rest.mean()),
        "K_full_per_b": [float(v) for v in K_full],
        "selfconsistent_ratio_full_over_rest": float(ratio_sc),
        "target_full": 4.0, "target_rest": 2.0,
        "note": "trace-reversed B gives Einstein 4GM/bc²; emerges from ρ",
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  J4 — uniqueness: K(λ) = 2(1+λ); only λ=1 gives factor-2
# ───────────────────────────────────────────────────────────────────

def test_J4_uniqueness_Koflambda():
    L = 256
    GM = 0.02
    center = (L // 2, L // 2)
    phi = _analytic_phi_slice(L, GM, center)
    b = 12
    window = 90
    lams = np.array([0.0, 0.5, 1.0, 1.5])
    Ks = []
    for lam in lams:
        A, B = f55.metric_spatial_fraction(phi, C0, lam=lam)
        a = f55.eikonal_deflection_AB(A, B, C0, impact_index=center[1] + b,
                                      window=window)
        Ks.append(a * b * C0**2 / GM)
    Ks = np.array(Ks)
    slope, intercept = np.polyfit(lams, Ks, 1)
    K_at_1 = float(np.interp(1.0, lams, Ks))
    ok = (abs(slope - 2.0) < 0.1 and abs(intercept - 2.0) < 0.1
          and abs(K_at_1 - 4.0) < 0.15)
    return {
        "name": "J4_uniqueness_K_of_lambda",
        "lambdas": [float(v) for v in lams],
        "K_values": [float(v) for v in Ks],
        "fit_slope": float(slope), "fit_intercept": float(intercept),
        "K_at_lambda1": K_at_1,
        "expected": "K(λ)=2(1+λ); λ=1 (trace reversal) → 4",
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  J5 — consistency with gr_fork_E_tensor linearised metric
# ───────────────────────────────────────────────────────────────────

def test_J5_consistency_with_forkE_linearized():
    GM = 0.03
    r = np.array([6.0, 9.0, 13.0, 20.0, 40.0])
    phi = -GM / r
    A53, B53 = f55.metric_trace_reversed(phi, C0)
    AE, BE = forkE.make_fork("linearized").metric(phi, C0)
    resid_A = float(np.max(np.abs(A53 - AE)))
    resid_B = float(np.max(np.abs(B53 - BE)))
    ok = resid_A < 1e-15 and resid_B < 1e-15
    return {
        "name": "J5_consistency_forkE_linearized",
        "max_abs_dA": resid_A, "max_abs_dB": resid_B,
        "note": "trace-reversed metric == gr_fork_E_tensor linearised, bit-for-bit",
        "tol": 1e-15,
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  Driver
# ───────────────────────────────────────────────────────────────────

def main():
    tests = [
        test_J1_trace_reversal_identity,
        test_J2_redshift_unchanged,
        test_J3_deflection_factor2,
        test_J4_uniqueness_Koflambda,
        test_J5_consistency_with_forkE_linearized,
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
        "finding": "F55",
        "title": "Spatial metric from trace reversal: Einstein factor-2 from mass",
        "date": "2026-05-29",
        "C0": C0, "G": G,
        "overall": overall,
        "tests": results,
    }
    out_dir = os.path.abspath(os.path.join(THIS, "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "F55_spatial_metric_backreaction.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("=" * 70)
    print("F55 — spatial metric from trace reversal (Einstein factor-2 from mass)")
    print("=" * 70)
    for r in results:
        print(f"  [{r.get('status','?'):>5}]  {r['name']}")
        for kk, vv in r.items():
            if kk in ("name", "status", "trace"):
                continue
            print(f"            {kk}: {vv}")
    print("-" * 70)
    print(f"  OVERALL: {overall}")
    print(f"  wrote {path}")
    return out


if __name__ == "__main__":
    main()
