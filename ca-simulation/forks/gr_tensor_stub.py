"""
gr_tensor_stub.py — runnable demonstration of Fork E (tensor-metric gravity)
============================================================================
Finding 19, the structurally-honest path beyond Paper 6.

What this stub shows, on one shared open-BC potential:

  (1) GR-3 is fixed *structurally*.  Carrying g_00 (clock = sqrt(-g_00))
      instead of folding everything into one refractive index drives the
      Pound-Rebka ratio_GR from the baseline factor-2 to 1 — with no
      ad-hoc phase-tick field.  Fork E "linearized" reproduces Fork B
      bit-for-bit (sanity); Fork E "exact_isotropic" keeps ratio ~ 1 to
      all PN orders.

  (2) GR-1 / GR-2 are untouched by the fix (the photon line integral sees
      c_gamma = c_0 sqrt(A/B), unchanged to leading order), confirming the
      deflection/Shapiro residual is discretisation, not the scalar->tensor
      structure.

  (3) GR-4 done the honest way.  A direct equatorial *geodesic* integral on
      the exact isotropic-Schwarzschild metric (no hand-written 1PN force
      law) returns the perihelion advance complete to all PN orders.  In the
      weak field it reproduces 6 pi GM / (a(1-e^2) c^2) to quadrature
      precision; that agreement is the integrator self-check.  The point:
      the 1.5% cap on the existing GR-4 test is a 2PN *truncation of the
      EOM*, not a lattice limit — the metric geodesic removes it.

Run (sandbox-friendly default L=96):
    python forks/gr_tensor_stub.py
    python forks/gr_tensor_stub.py 64       # quicker
    python forks/gr_tensor_stub.py 128      # sharper GR-1/2/3 residuals

Outputs:
    test-results/gr_tensor_stub.json
    test-results/gr_tensor_stub.md
"""

from __future__ import annotations
import json
import math
import os
import sys

import numpy as np

THIS = os.path.dirname(__file__)
SIM_ROOT = os.path.abspath(os.path.join(THIS, ".."))
sys.path.insert(0, SIM_ROOT)
sys.path.insert(0, THIS)

from poisson_open import solve_poisson_3d_open, gaussian_mass_3d   # noqa: E402
from gr3_fork_harness import gr1_K, gr2_ratio, gr3_ratio_GR        # noqa: E402
import gr3_fork_baseline as fork_baseline                          # noqa: E402
import gr3_fork_B_anisotropic as fork_B                            # noqa: E402
import gr_fork_E_tensor as forkE                                   # noqa: E402


# ═══════════════════════════════════════════════════════════════════
#  GR-4 done structurally: timelike geodesic in the EXACT isotropic
#  Schwarzschild metric, integrated by the angle-sweep quadrature.
#
#  Equatorial isotropic metric (g_rr = B, g_phiphi = B r^2):
#      ds^2 = -A(r) c^2 dt^2 + B(r) dr^2 + B(r) r^2 dphi^2
#  Conserved E = A c^2 t' , L = B r^2 phi'  (prime = d/dtau).  Timelike
#  normalisation gives
#      (r')^2 = (1/B)[ E^2/(A c^2) - c^2 - L^2/(B r^2) ].
#  Perihelion advance per orbit:
#      Dw = 2 ∫_{r1}^{r2} (dphi/dr) dr - 2 pi
#  with dphi/dr = [L/(B r^2)] / sqrt((r')^2).  The sqrt turning-point
#  singularities at r1, r2 are removed by r = c0 - c1 cos(chi).
# ═══════════════════════════════════════════════════════════════════

def _A_exact(r, GM, c):
    u = GM / (r * c**2)
    h = 0.5 * u
    return ((1.0 - h) / (1.0 + h))**2


def _B_exact(r, GM, c):
    u = GM / (r * c**2)
    h = 0.5 * u
    return (1.0 + h)**4


def geodesic_perihelion_advance(GM, r_peri, r_apo, c=1.0, n=20000):
    """Per-orbit perihelion advance for a bound timelike geodesic of the
    exact isotropic-Schwarzschild metric, defined by its turning radii.

    Returns dict with the measured advance (rad/orbit), the 1PN reference
    6 pi GM/(p c^2), and the orbit's (a, e, p, v2/c2)."""
    r1, r2 = float(r_peri), float(r_apo)
    A1, A2 = _A_exact(r1, GM, c), _A_exact(r2, GM, c)
    B1, B2 = _B_exact(r1, GM, c), _B_exact(r2, GM, c)

    # Solve the 2x2 turning-point system for P = E^2, Q = L^2:
    #   P/(A_i c^2) - Q/(B_i r_i^2) = c^2
    M = np.array([[1.0 / (A1 * c**2), -1.0 / (B1 * r1**2)],
                  [1.0 / (A2 * c**2), -1.0 / (B2 * r2**2)]])
    rhs = np.array([c**2, c**2])
    P, Q = np.linalg.solve(M, rhs)        # P = E^2, Q = L^2
    E = math.sqrt(P)
    L = math.sqrt(Q)

    # Angle sweep peri->apo via chi-substitution (removes sqrt singularity).
    c0 = 0.5 * (r1 + r2)
    c1 = 0.5 * (r2 - r1)
    # Open midpoint rule on chi in (0, pi).
    chi = (np.arange(n) + 0.5) * (math.pi / n)
    r = c0 - c1 * np.cos(chi)
    dr_dchi = c1 * np.sin(chi)
    u = GM / (r * c**2)
    h = 0.5 * u
    A = ((1.0 - h) / (1.0 + h))**2
    B = (1.0 + h)**4
    rdot2 = (1.0 / B) * (P / (A * c**2) - c**2 - Q / (B * r**2))
    rdot2 = np.clip(rdot2, 1e-300, None)          # guard tiny negatives at ends
    dphi_dr = (L / (B * r**2)) / np.sqrt(rdot2)
    half_sweep = float(np.sum(dphi_dr * dr_dchi) * (math.pi / n))
    advance = 2.0 * half_sweep - 2.0 * math.pi

    a = 0.5 * (r1 + r2)
    e = (r2 - r1) / (r2 + r1)
    p = a * (1.0 - e**2)
    dw_1PN = 6.0 * math.pi * GM / (p * c**2)
    # Rough orbital speed scale at semi-latus crossing:
    v2_over_c2 = GM / (p * c**2)

    return {
        "GM": GM, "c": c, "r_peri": r1, "r_apo": r2,
        "a": a, "e": e, "p": p, "v2_over_c2": v2_over_c2,
        "E": E, "L": L,
        "advance_geodesic": advance,
        "advance_1PN_ref": dw_1PN,
        "ratio_geodesic_over_1PN": advance / dw_1PN,
    }


# ═══════════════════════════════════════════════════════════════════
#  Field-sector comparison: GR-1 / GR-2 / GR-3 across forks
# ═══════════════════════════════════════════════════════════════════

def run_field_sector(L=96, M=1.0, sigma=3.0, G_N=5e-4, c_0=0.5, b=8):
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = solve_poisson_3d_open(rho, G_N=G_N)
    pairs = [(6, 16), (8, 22), (10, 28), (12, 30)]

    columns = {
        "baseline_paper6": fork_baseline,
        "fork_B_anisotropic": fork_B,
        "fork_E_linearized": forkE.make_fork("linearized"),
        "fork_E_exact_isotropic": forkE.make_fork("exact_isotropic"),
    }

    out = {}
    for name, fk in columns.items():
        _, K = gr1_K(fk, phi, c_0, b, G_N, M)
        _, _, r2 = gr2_ratio(fk, phi, c_0, b, G_N, M)
        gr3 = gr3_ratio_GR(fk, phi, c_0, pairs)
        out[name] = {
            "gr1_K": float(K),
            "gr2_ratio": float(r2),
            "gr3_ratio_GR": float(gr3["mean_ratio_GR"]),
            "gr3_std": float(gr3["std_ratio_GR"]),
        }
    meta = {"L": L, "M": M, "sigma": sigma, "G_N": G_N, "c_0": c_0,
            "b": b, "pairs": pairs,
            "phi_min": float(phi.min()), "phi_max": float(phi.max())}
    return out, meta


# ═══════════════════════════════════════════════════════════════════
#  Self-checks
# ═══════════════════════════════════════════════════════════════════

def self_checks(field, geo_weak):
    checks = {}
    # (a) Fork E linearized must equal Fork B on every field observable.
    fb = field["fork_B_anisotropic"]
    fe = field["fork_E_linearized"]
    dmax = max(abs(fb["gr1_K"] - fe["gr1_K"]),
               abs(fb["gr2_ratio"] - fe["gr2_ratio"]),
               abs(fb["gr3_ratio_GR"] - fe["gr3_ratio_GR"]))
    checks["E_linearized_matches_forkB"] = {
        "max_abs_diff": dmax, "pass": dmax < 1e-9}
    # (b) GR-3 fixed structurally in exact mode (ratio_GR ~ 1, not ~ 2).
    g3 = field["fork_E_exact_isotropic"]["gr3_ratio_GR"]
    checks["E_exact_fixes_gr3"] = {
        "gr3_ratio_GR": g3, "pass": abs(g3 - 1.0) < 0.05}
    # (c) baseline still shows the factor 2 (control).
    g3b = field["baseline_paper6"]["gr3_ratio_GR"]
    checks["baseline_still_factor2"] = {
        "gr3_ratio_GR": g3b, "pass": abs(g3b - 2.0) < 0.05}
    # (d) geodesic integrator reproduces 1PN in the weak field.
    rr = geo_weak["ratio_geodesic_over_1PN"]
    checks["geodesic_recovers_1PN_weakfield"] = {
        "ratio_geodesic_over_1PN": rr, "pass": abs(rr - 1.0) < 2e-3}
    return checks


# ═══════════════════════════════════════════════════════════════════
#  Driver
# ═══════════════════════════════════════════════════════════════════

def main():
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 96
    print("=" * 70)
    print("Fork E — tensor-metric gravity stub  (Finding 19)")
    print("=" * 70)
    print(f"Field sector at L={L} …")
    field, meta = run_field_sector(L=L)

    hdr = f'{"fork":>26} | {"GR-1 K":>9} | {"GR-2":>8} | {"GR-3 ratio_GR":>14}'
    print()
    print(hdr)
    print("-" * len(hdr))
    for name, r in field.items():
        print(f'{name:>26} | {r["gr1_K"]:>9.4f} | {r["gr2_ratio"]:>8.4f} | '
              f'{r["gr3_ratio_GR"]:>14.4f}')

    print()
    print("GR-4 — geodesic perihelion advance on the EXACT metric")
    print("-" * 70)
    # Mercury-like (matches test_09 / gr4 conventions: GM=0.003, a=1, e=0.3)
    GM, a, e, c = 0.003, 1.0, 0.3, 1.0
    r_peri, r_apo = a * (1 - e), a * (1 + e)
    geo = geodesic_perihelion_advance(GM, r_peri, r_apo, c=c)
    # A genuinely weak-field orbit for the integrator self-check.
    geo_weak = geodesic_perihelion_advance(1e-5, 1.0 * (1 - 0.2),
                                           1.0 * (1 + 0.2), c=1.0)
    print(f'  Mercury-like (GM={GM}, a={a}, e={e}, v2/c2={geo["v2_over_c2"]:.3e}):')
    print(f'     geodesic advance   = {geo["advance_geodesic"]:.6e} rad/orbit')
    print(f'     1PN reference 6πGM/pc^2 = {geo["advance_1PN_ref"]:.6e} rad/orbit')
    print(f'     geodesic/1PN       = {geo["ratio_geodesic_over_1PN"]:.6f}')
    print(f'  Weak-field self-check (GM=1e-5, e=0.2):')
    print(f'     geodesic/1PN       = {geo_weak["ratio_geodesic_over_1PN"]:.8f}')

    checks = self_checks(field, geo_weak)
    print()
    print("Self-checks")
    print("-" * 70)
    all_pass = True
    for k, v in checks.items():
        ok = v["pass"]
        all_pass = all_pass and ok
        print(f'  [{"PASS" if ok else "FAIL"}]  {k}')
    print()
    print(f'  ALL CHECKS: {"PASS" if all_pass else "FAIL"}')

    results = {
        "date": "2026-05-21",
        "stub": "forks/gr_tensor_stub.py",
        "meta": meta,
        "field_sector": field,
        "gr4_geodesic_mercury": geo,
        "gr4_geodesic_weakfield_selfcheck": geo_weak,
        "self_checks": checks,
        "all_pass": all_pass,
    }
    out_dir = os.path.abspath(os.path.join(THIS, "..", "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    jpath = os.path.join(out_dir, "gr_tensor_stub.json")
    mpath = os.path.join(out_dir, "gr_tensor_stub.md")
    with open(jpath, "w") as f:
        json.dump(results, f, indent=2)
    _write_md(results, mpath)
    print()
    print(f"Wrote {jpath}")
    print(f"Wrote {mpath}")
    return results


def _write_md(results, path):
    m = results["meta"]
    f = results["field_sector"]
    geo = results["gr4_geodesic_mercury"]
    gw = results["gr4_geodesic_weakfield_selfcheck"]
    L = []
    L.append("# Fork E — tensor-metric gravity stub")
    L.append("")
    L.append("_Generated 2026-05-21 by `forks/gr_tensor_stub.py` (Finding 19)._")
    L.append("")
    L.append(f"Shared open-BC potential: $L={m['L']}$, $M={m['M']}$, "
             f"$\\sigma={m['sigma']}$, $G_N={m['G_N']}$, $c_0={m['c_0']}$, "
             f"$b={m['b']}$; $\\phi\\in[{m['phi_min']:.3e}, {m['phi_max']:.3e}]$.")
    L.append("")
    L.append("## Field sector (GR-1 / GR-2 / GR-3)")
    L.append("")
    L.append("| Fork | GR-1 $K$ | GR-2 ratio | GR-3 ratio$_{GR}$ |")
    L.append("|---|---|---|---|")
    for name, r in f.items():
        L.append(f"| `{name}` | {r['gr1_K']:.4f} | {r['gr2_ratio']:.4f} | "
                 f"{r['gr3_ratio_GR']:.4f} ± {r['gr3_std']:.1e} |")
    L.append("")
    L.append("Baseline shows the factor-2 GR-3 ratio; carrying $g_{00}$ "
             "(clock $=\\sqrt{-g_{00}}$) in Fork E drives it to 1. "
             "GR-1/GR-2 are unchanged across columns — the deflection/Shapiro "
             "residual is discretisation, not the scalar→tensor structure.")
    L.append("")
    L.append("## GR-4 — geodesic perihelion advance on the exact metric")
    L.append("")
    L.append("| Orbit | $v^2/c^2$ | geodesic (rad/orbit) | $6\\pi GM/pc^2$ | ratio |")
    L.append("|---|---|---|---|---|")
    L.append(f"| Mercury-like | {geo['v2_over_c2']:.3e} | "
             f"{geo['advance_geodesic']:.6e} | {geo['advance_1PN_ref']:.6e} | "
             f"{geo['ratio_geodesic_over_1PN']:.5f} |")
    L.append(f"| weak-field check | {gw['v2_over_c2']:.3e} | "
             f"{gw['advance_geodesic']:.6e} | {gw['advance_1PN_ref']:.6e} | "
             f"{gw['ratio_geodesic_over_1PN']:.7f} |")
    L.append("")
    L.append("The weak-field ratio → 1 is the integrator self-check. The "
             "Mercury-like geodesic carries all PN orders, so its small "
             "departure from the 1PN closed form is physical higher-order "
             "content, not truncation error.")
    L.append("")
    L.append("## Self-checks")
    L.append("")
    for k, v in results["self_checks"].items():
        L.append(f"- [{'PASS' if v['pass'] else 'FAIL'}] `{k}`")
    L.append("")
    L.append(f"**ALL CHECKS: {'PASS' if results['all_pass'] else 'FAIL'}**")
    with open(path, "w") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    main()
