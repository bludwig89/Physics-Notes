"""
test_F52_restleg_backreaction.py — Gravity as a self-consistent rest-leg field
==============================================================================
Tests the F52 hypothesis (forks/gr_fork_F52_restleg_backreaction.py): the lapse
√A that F50 *imports* via an analytic φ = −GM/r is instead the equilibrium of a
lattice field equation in which the rest-leg (clock-rate) deficit is sourced
directly by rest-mass density ρ — closing the F50 loop.

Tests
-----
H1  Loop closure (spectral).  Self-consistent Φ = solve(∇²Φ=4πGρ) from a
    Gaussian mass M reproduces the imported −GM/r OUTSIDE the source: a linear
    fit Φ_sc vs (−1/r) has slope = G·M_eff with M_eff = M (the input mass) and
    r² ≈ 1.  ⇒ F50's lapse is recoverable from mass alone.
H1b Loop closure (literal fixed point).  A hand-rolled Jacobi relaxation of the
    SAME field equation converges to a field with the same GM amplitude as the
    analytic −GM/r, to the relaxation tolerance.  ⇒ the clock field is a genuine
    lattice fixed point, not just a spectral artefact.
H2  Redshift (factor 1).  Given the self-consistent field reproduces −GM/r, the
    rest leg Ω = √A·arcsin m gives the GR factor-1 redshift Δν/ν = Δφ/c²
    (mean ratio → 1), reproducing F50-G2 with NO imported potential.
H3  Deflection discriminator (factor 1 vs 2).  Eikonal deflection through the
    field: sourcing ONLY the rest/clock leg (B = 1) gives K ≡ αbc²/GM = 2
    (Newtonian/factor-1); sourcing the spatial metric too (full isotropic) gives
    K = 4 (Einstein/factor-2).  The ratio K_full/K_rest = 2 is the clean
    discriminator (common lattice errors cancel).  Cross-checked on the
    self-consistent lattice slice, not only the analytic potential.

Writes test-results/F52_restleg_backreaction.json.

Run:
    python model-tests/test_F52_restleg_backreaction.py
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

import gr_fork_F52_restleg_backreaction as f52   # noqa: E402
from ca_emqg import gaussian_mass_3d             # noqa: E402

C0 = 0.5
MODE = "exact_isotropic"
G = 1.0


def _radii(L, center):
    x = np.arange(L) - center[0]
    y = np.arange(L) - center[1]
    z = np.arange(L) - center[2]
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    return np.sqrt(X**2 + Y**2 + Z**2)


# ───────────────────────────────────────────────────────────────────
#  H1 — loop closure (spectral): Φ_sc reproduces the imported −GM/r
# ───────────────────────────────────────────────────────────────────

def test_H1_loop_closure_spectral():
    L = 96
    M = 1.0
    sigma = 3.0
    center = (L // 2, L // 2, L // 2)
    rho = gaussian_mass_3d(L, M=M, sigma=sigma, center=center)
    Phi = f52.restleg_potential_fft(rho, G=G)
    r = _radii(L, center)

    # clean radial shell: well outside the Gaussian (>4σ) and well inside the
    # box (avoid periodic images near faces)
    mask = (r > 4 * sigma) & (r < L / 4)
    inv_r = -1.0 / r[mask]              # the −1/r basis of −GM/r
    phi_vals = Phi[mask]
    # linear fit Φ = slope·(−1/r) + const ; slope should be G·M_eff
    A_design = np.vstack([inv_r, np.ones_like(inv_r)]).T
    coef, *_ = np.linalg.lstsq(A_design, phi_vals, rcond=None)
    slope, const = coef
    M_eff = slope / G
    pred = A_design @ coef
    ss_res = np.sum((phi_vals - pred) ** 2)
    ss_tot = np.sum((phi_vals - phi_vals.mean()) ** 2)
    r2 = 1.0 - ss_res / ss_tot

    ok = (abs(M_eff / M - 1.0) < 0.05) and (r2 > 0.999)
    return {
        "name": "H1_loop_closure_spectral",
        "M_input": M, "M_eff_from_fit": float(M_eff),
        "M_eff_over_M": float(M_eff / M),
        "fit_r2": float(r2),
        "note": "Φ_sc sourced by ρ reproduces the −GM/r that F50 imports",
        "tol_M": 0.05, "tol_r2": 0.999,
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  H1b — loop closure (literal fixed point via hand-rolled relaxation)
# ───────────────────────────────────────────────────────────────────

def test_H1b_loop_closure_fixed_point():
    L = 48
    M = 1.0
    sigma = 2.5
    center = (L // 2, L // 2, L // 2)
    rho = gaussian_mass_3d(L, M=M, sigma=sigma, center=center)
    Phi, res, iters = f52.relax_restleg_potential(rho, G=G, n_iter=8000,
                                                   tol=1e-8)
    r = _radii(L, center)
    # shell away from source and from the Dirichlet box faces
    mask = (r > 4 * sigma) & (r < L / 2 - 6)
    inv_r = -1.0 / r[mask]
    A_design = np.vstack([inv_r, np.ones_like(inv_r)]).T
    coef, *_ = np.linalg.lstsq(A_design, Phi[mask], rcond=None)
    slope = coef[0]
    M_eff = slope / G
    pred = A_design @ coef
    r2 = 1.0 - np.sum((Phi[mask] - pred) ** 2) / np.sum(
        (Phi[mask] - Phi[mask].mean()) ** 2)
    # Dirichlet box truncates the 1/r tail, biasing M_eff low by a few %;
    # allow 12% on amplitude but demand a clean 1/r shape (r²) and convergence.
    ok = (abs(M_eff / M - 1.0) < 0.12) and (r2 > 0.99) and (res < 1e-6)
    return {
        "name": "H1b_loop_closure_fixed_point",
        "M_eff_over_M": float(M_eff / M),
        "fit_r2": float(r2),
        "relax_residual": float(res),
        "relax_iters": int(iters),
        "note": "hand-rolled Jacobi fixed point reproduces the 1/r amplitude",
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  H2 — redshift factor 1 from the self-consistent rest leg
# ───────────────────────────────────────────────────────────────────

def test_H2_redshift_factor1():
    # Given H1 (Φ_sc = −GM/r), evaluate the rest leg on that profile.
    m = 0.3
    GM = 0.02
    pairs = [(6.0, 16.0), (8.0, 22.0), (10.0, 28.0), (12.0, 30.0)]
    ratios = []
    rest_resid = []
    for r_n, r_f in pairs:
        phi_n = np.array([-GM / r_n])
        phi_f = np.array([-GM / r_f])
        # Ω(k=0) must equal the rest leg exactly (same identity as F50-G2)
        om_n = f52.rest_leg(phi_n, C0, m, MODE)[0]
        s_n = f52.clock_field(phi_n, C0, MODE)[0]
        rest_resid.append(abs(om_n - s_n * float(np.arcsin(m))))
        tau_n = f52.clock_field(phi_n, C0, MODE)[0]
        tau_f = f52.clock_field(phi_f, C0, MODE)[0]
        dnu = tau_n / tau_f - 1.0
        pred_GR = -(float(phi_f[0]) - float(phi_n[0])) / C0**2   # Δφ/c²
        ratios.append(dnu / pred_GR)
    ratios = np.array(ratios)
    ok = (abs(ratios.mean() - 1.0) < 0.05) and (max(rest_resid) < 1e-13)
    return {
        "name": "H2_redshift_factor1",
        "mean_ratio_GR": float(ratios.mean()),
        "std_ratio_GR": float(ratios.std()),
        "baseline_factor2": 2.0,
        "max_rest_leg_residual": float(np.max(rest_resid)),
        "target_ratio": 1.0,
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  H3 — deflection discriminator: rest-leg-only = factor 1, full = factor 2
# ───────────────────────────────────────────────────────────────────

def _analytic_phi_slice(L, GM, center_xy):
    """2D equatorial slice of φ = −GM/r (true 3D Newtonian, sliced at z=0)."""
    x = np.arange(L) - center_xy[0]
    y = np.arange(L) - center_xy[1]
    X, Y = np.meshgrid(x, y, indexing="ij")
    r = np.sqrt(X**2 + Y**2)
    r[r < 1e-9] = 1e-9
    return -GM / r


def _coeff_K(alpha, b, GM):
    """K = α·b·c²/GM with c=C0 ; reads off 2κ for n−1 = κ·GM/(r c²)."""
    return alpha * b * C0**2 / GM


def test_H3_deflection_discriminator():
    L = 256                       # fine slice for a clean line integral
    GM = 0.02
    center = (L // 2, L // 2)
    phi = _analytic_phi_slice(L, GM, center)

    impacts = [8, 12, 16]
    window = 90                   # ±90 cells: W/√(W²+b²) ≈ 0.99 → ~1% truncation
    K_rest, K_full = [], []
    for b in impacts:
        a_rest = f52.eikonal_deflection(phi, C0, axis_long=0, axis_perp=1,
                                        impact_index=center[1] + b,
                                        window=window, mode=MODE,
                                        sector="rest_only")
        a_full = f52.eikonal_deflection(phi, C0, axis_long=0, axis_perp=1,
                                        impact_index=center[1] + b,
                                        window=window, mode=MODE,
                                        sector="full")
        K_rest.append(_coeff_K(a_rest, b, GM))
        K_full.append(_coeff_K(a_full, b, GM))
    K_rest = np.array(K_rest)
    K_full = np.array(K_full)
    ratio = K_full / K_rest

    # absolute coefficients (≈2 and ≈4, a little low from finite window/lattice);
    # the RATIO is the clean, lattice-error-cancelling discriminator.
    ok = (abs(K_rest.mean() - 2.0) < 0.15 and
          abs(K_full.mean() - 4.0) < 0.30 and
          abs(ratio.mean() - 2.0) < 0.05)
    return {
        "name": "H3_deflection_discriminator",
        "K_rest_only_mean": float(K_rest.mean()),
        "K_full_mean": float(K_full.mean()),
        "K_ratio_full_over_rest_mean": float(ratio.mean()),
        "K_rest_per_b": [float(v) for v in K_rest],
        "K_full_per_b": [float(v) for v in K_full],
        "target_rest": 2.0, "target_full": 4.0, "target_ratio": 2.0,
        "note": ("rest-leg-only is Newtonian factor-1; Einstein factor-2 "
                 "requires the spatial metric B to be sourced too"),
        "status": "PASS" if ok else "FAIL",
    }


def test_H3b_deflection_on_selfconsistent_field():
    """Cross-check H3's ratio on the SELF-CONSISTENT lattice field (not the
    analytic φ): build Φ_sc from ρ via the spectral solver, slice it, and
    confirm the full/rest deflection ratio is still 2."""
    L = 128
    M = 0.03           # weak field (u = GM/rc² ≈ 0.009 at the probe) so the
    sigma = 3.0        # factor-2 relation is in its leading-order regime, as H3
    center = (L // 2, L // 2, L // 2)
    rho = gaussian_mass_3d(L, M=M, sigma=sigma, center=center)
    Phi = f52.restleg_potential_fft(rho, G=G)
    phi_slice = Phi[:, :, center[2]]          # equatorial slice
    b = 14
    window = 40
    a_rest = f52.eikonal_deflection(phi_slice, C0, impact_index=center[1] + b,
                                    window=window, mode=MODE, sector="rest_only")
    a_full = f52.eikonal_deflection(phi_slice, C0, impact_index=center[1] + b,
                                    window=window, mode=MODE, sector="full")
    ratio = a_full / a_rest
    ok = abs(ratio - 2.0) < 0.05
    return {
        "name": "H3b_deflection_ratio_selfconsistent",
        "alpha_rest": float(a_rest),
        "alpha_full": float(a_full),
        "ratio_full_over_rest": float(ratio),
        "target_ratio": 2.0,
        "note": "discriminator holds on the mass-sourced lattice field",
        "status": "PASS" if ok else "FAIL",
    }


# ───────────────────────────────────────────────────────────────────
#  Driver
# ───────────────────────────────────────────────────────────────────

def main():
    tests = [
        test_H1_loop_closure_spectral,
        test_H1b_loop_closure_fixed_point,
        test_H2_redshift_factor1,
        test_H3_deflection_discriminator,
        test_H3b_deflection_on_selfconsistent_field,
    ]
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:  # noqa: BLE001
            import traceback
            results.append({"name": t.__name__, "status": "ERROR",
                            "error": repr(e),
                            "trace": traceback.format_exc()})

    overall = "PASS" if all(r.get("status") == "PASS" for r in results) else "FAIL"
    out = {
        "finding": "F52",
        "title": "Gravity as a self-consistent rest-leg (clock-rate) field",
        "date": "2026-05-29",
        "C0": C0, "metric_mode": MODE, "G": G,
        "overall": overall,
        "tests": results,
    }
    out_dir = os.path.abspath(os.path.join(THIS, "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "F52_restleg_backreaction.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("=" * 68)
    print("F52 — gravity as a self-consistent rest-leg (clock-rate) field")
    print("=" * 68)
    for r in results:
        print(f"  [{r.get('status','?'):>5}]  {r['name']}")
        for kk, vv in r.items():
            if kk in ("name", "status", "trace"):
                continue
            print(f"            {kk}: {vv}")
    print("-" * 68)
    print(f"  OVERALL: {overall}")
    print(f"  wrote {path}")
    return out


if __name__ == "__main__":
    main()
