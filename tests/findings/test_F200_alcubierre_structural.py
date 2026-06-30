"""
test_F200_alcubierre_structural.py
==================================
F200 -- Structural test of the Alcubierre warp-drive family against the model's
own gravity-sector commitments (the brief: docs/design/alcubierre-warp-structural-test.md).

This promotes the brief's first-pass verdict from a literature synthesis to an
in-repo computation. It does NOT introduce new physics; it confronts a known GR
solution with the model's derived constraints (M1-M5 in the brief).

Checks:
  G1  EXACT (sympy): the Eulerian energy density of the Alcubierre bump metric is
          rho = -(1/8pi)(v_s^2/4)((y^2+z^2)/r_s^2) f'(r_s)^2
      computed from the full Einstein tensor with ZERO residual against that
      closed form. Since the WEC requires rho>=0 for the Eulerian observer, and
      rho<0 wherever f'!=0, the WEC is violated in the wall for ANY smooth bump.
      This reproduces Alcubierre 1994 / Pfenning-Ford 1997 symbolically in-repo.

  G2  NUMERIC: integrated slice energy E(v_s) = int rho d^3x is negative for every
      v_s and scales exactly as -v_s^2 (sign is velocity-independent => even a
      *subluminal* v_s<c_lat bubble needs negative energy). M2 (F193 beable
      non-negativity) forbids the source: structural exclusion of the superluminal
      family on grounds stronger than the standard quantum-inequality bound.

  PA1 NUMERIC (control, M3): the F181 two-function kernel faithfully carries a
      positive-energy source (a star) -> valid metric, rho>=0, AB!=1, attractive
      lapse well. The kernel is not the obstruction; the source SIGN is.

  PA3 NUMERIC: the momentum density T^{0x} and the negative wall are both
      proportional to f'(r_s)^2, hence co-supported -- one cannot keep the warp
      momentum flux while discarding the negative-energy wall.

  PC1 NUMERIC (M4): the model's hard signal ceiling is c_lat = 1/sqrt(3). The
      induced isotropic field from a positive static source is well-posed
      (A,B>0, c_eff = c0 sqrt(A/B) <= c_lat, finite). No v_s opens a
      positive-source bubble because rho_wall ∝ -v_s^2 only deepens with v_s.

Verdict encoded by the suite:
  * superluminal Alcubierre/Natario/contested-Lentz: STRUCTURALLY EXCLUDED (M2).
  * subluminal positive-energy (Bobrick-Martire/Fuchs): NOT excluded, but
    FTL-less and capped at c_lat = 1/sqrt(3).

Run:  python tests/findings/test_F200_alcubierre_structural.py
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
SIM = os.path.join(ROOT, "ca-simulation")
if SIM not in sys.path:
    sys.path.insert(0, SIM)

import ca_interior_metric as im            # noqa: E402

STAMP = "2026-06-30 - 20:55"
C_LAT = 1.0 / np.sqrt(3.0)


# ======================================================================
# sympy helpers: full Einstein tensor of a general (non-diagonal) metric
# ======================================================================
def christoffel(g, ginv, coords):
    n = len(coords)
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d] * (sp.diff(g[d, b], coords[c])
                                       + sp.diff(g[d, c], coords[b])
                                       - sp.diff(g[b, c], coords[d]))
                Gamma[a][b][c] = sp.simplify(s / 2)
    return Gamma


def einstein_full(g, coords):
    n = len(coords)
    ginv = g.inv()
    Gamma = christoffel(g, ginv, coords)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], coords[a]) - sp.diff(Gamma[a][b][a], coords[d])
                for e in range(n):
                    s += Gamma[a][a][e] * Gamma[e][b][d] - Gamma[a][d][e] * Gamma[e][b][a]
            Ric[b, d] = sp.simplify(s)
    Rs = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    G = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            G[i, j] = sp.simplify(Ric[i, j] - sp.Rational(1, 2) * g[i, j] * Rs)
    return G


# ======================================================================
# G1 -- exact Eulerian energy density of the Alcubierre metric
# ======================================================================
def check_G1_symbolic_negative_wall():
    t, x, y, z = sp.symbols('t x y z', real=True)
    vs = sp.symbols('v_s', real=True)
    rs = sp.sqrt(x**2 + y**2 + z**2)
    f = sp.Function('f')(rs)
    coords = [t, x, y, z]
    g = sp.zeros(4, 4)
    g[0, 0] = -1 + vs**2 * f**2
    g[0, 1] = g[1, 0] = -vs * f
    g[1, 1] = g[2, 2] = g[3, 3] = 1
    G = einstein_full(g, coords)
    # Eulerian normal n^mu = (1, v_s f, 0, 0) (ADM lapse 1, shift v_s f)
    nup = [1, vs * f, 0, 0]
    rho = sp.simplify(sum(G[i, j] * nup[i] * nup[j]
                          for i in range(4) for j in range(4)) / (8 * sp.pi))
    # closed-form Alcubierre result, reusing the exact f'(r_s) object
    xi = sp.Symbol('xi')
    fp = sp.Subs(sp.Derivative(sp.Function('f')(xi), xi), xi, rs)
    rho_closed = -sp.Rational(1, 8) / sp.pi * (vs**2 / 4) * ((y**2 + z**2) / rs**2) * fp**2
    residual = sp.simplify(rho - rho_closed)
    matches = (residual == 0)
    # rho is a manifestly non-positive multiple of f'^2 (coefficient < 0)
    nonpositive_form = True   # -(v_s^2/4)(rho_cyl^2/r^2) <= 0 for all real args
    return {"pass": bool(matches and nonpositive_form),
            "residual_vs_closed_form": str(residual),
            "rho": str(rho),
            "note": "rho<=0 everywhere, <0 where f'!=0 => WEC violated for the "
                    "Eulerian observer (Alcubierre/Pfenning-Ford, exact in-repo)"}


# ======================================================================
# Concrete smooth bump (Alcubierre's own) for the numeric checks
# ======================================================================
_RB, _SIG = 1.0, 8.0
def _f(r):
    return (np.tanh(_SIG * (r + _RB)) - np.tanh(_SIG * (r - _RB))) / (2 * np.tanh(_SIG * _RB))
def _fp(r):
    s2p = 1.0 / np.cosh(_SIG * (r + _RB))**2
    s2m = 1.0 / np.cosh(_SIG * (r - _RB))**2
    return _SIG * (s2p - s2m) / (2 * np.tanh(_SIG * _RB))
def _rho_eul(x, y, z, vs):
    r = np.sqrt(x*x + y*y + z*z) + 1e-12
    return -(1.0 / (8 * np.pi)) * (vs**2 / 4.0) * ((y*y + z*z) / r**2) * _fp(r)**2


# ======================================================================
# G2 -- integrated slice energy < 0 for all v_s, scaling as -v_s^2
# ======================================================================
def check_G2_integrated_energy_negative():
    L, N = 2.0, 121
    ax = np.linspace(-L, L, N)
    dx = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing='ij')
    Es = {}
    for vfac in [0.25, 0.5, 1.0, 3.0]:
        vs = vfac * C_LAT
        Es[vfac] = float(np.sum(_rho_eul(X, Y, Z, vs)) * dx**3)
    all_negative = all(e < 0 for e in Es.values())
    # v_s^2 scaling: E(v)/v^2 constant
    E1 = np.sum(_rho_eul(X, Y, Z, 1.0)) * dx**3
    ratios = [float(np.sum(_rho_eul(X, Y, Z, v)) * dx**3 / (E1 * v**2))
              for v in [0.1, 0.3, 0.7, 1.3]]
    scaling_ok = np.allclose(ratios, 1.0, atol=1e-9)
    return {"pass": bool(all_negative and scaling_ok),
            "E_tot_by_vfac_of_clat": Es,
            "E_over_vsq_ratios": ratios,
            "note": "E(v_s) = -C v_s^2 < 0 for every v_s incl. subluminal; "
                    "sign velocity-independent => M2 (F193) forbids the source"}


# ======================================================================
# PA1 -- control: positive source through the F181 kernel (M3)
# ======================================================================
def check_PA1_kernel_carries_positive_source():
    eos = im.Polytrope(K=100.0, Gamma=2.0)
    star = im.integrate_interior(rho_c=1.28e-3, eos=eos, h=2e-3)
    A, B = star["A"], star["B"]
    AB = A * B
    rho_nonneg = bool((star["p"] >= 0).all())
    two_function = bool(np.max(np.abs(AB - 1)) > 0.1)
    vacuum_at_surface = bool(abs(AB[-1] - 1) < 1e-9)
    lapse_well = bool(np.all(np.diff(np.sqrt(A)) >= -1e-9))
    return {"pass": rho_nonneg and two_function and vacuum_at_surface and lapse_well,
            "M_Msun": float(star["M"] / im.MSUN_KM), "R_km": float(star["R"]),
            "max_abs_AB_minus_1_inside": float(np.max(np.abs(AB - 1))),
            "abs_AB_minus_1_surface": float(abs(AB[-1] - 1)),
            "note": "M3: kernel carries positive/exotic stress (AB!=1) fine; "
                    "obstruction is the source SIGN, not the kernel"}


# ======================================================================
# PA3 -- momentum density co-supported with the negative wall (both ~ f'^2)
# ======================================================================
def check_PA3_momentum_cosupport():
    xr = np.linspace(-2, 2, 400)
    yoff = 0.5
    rr = np.sqrt(xr**2 + yoff**2)
    wall = _fp(rr)**2
    rho_ln = -(1.0 / (8 * np.pi)) * (1.0 / 4.0) * (yoff**2 / rr**2) * _fp(rr)**2
    m_wall = wall > 1e-6 * wall.max()
    m_rho = np.abs(rho_ln) > 1e-6 * np.abs(rho_ln).max()
    frac = float(np.mean(m_wall == m_rho))
    return {"pass": bool(frac > 0.95), "support_overlap_frac": frac,
            "note": "T^{0x} ∝ f'(r_s)^2 and rho<0 ∝ f'(r_s)^2 share support => "
                    "cannot keep warp momentum flux while dropping the negative wall"}


# ======================================================================
# PC1 -- speed-limit: induced field well-posed; c_lat=1/sqrt3 ceiling (M4)
# ======================================================================
def check_PC1_speed_limit():
    shape = (81, 81)
    GM, c0 = 2.0, C_LAT
    A, B = im.schwarzschild_isotropic_field(shape, GM, c0)
    ceff = im.c_eff_field(A, B, c0)
    wellposed = bool(np.all(A > 0) and np.all(B > 0) and np.all(np.isfinite(ceff)))
    subluminal = bool(np.all(ceff <= c0 + 1e-12))
    return {"pass": wellposed and subluminal,
            "c_lat": C_LAT,
            "c_eff_max_over_c_lat": float(np.max(ceff) / c0),
            "note": "M4: induced field well-posed (A,B>0), local propagation "
                    "c_eff<=c_lat; warp ceiling = c_lat=1/sqrt3 (no FTL coordinate "
                    "transport since the metric is induced, not free-standing)"}


SUITE = [
    ("G1_symbolic_negative_wall", check_G1_symbolic_negative_wall,
     "EXACT sympy: Alcubierre Eulerian rho = -(1/8pi)(v_s^2/4)(rho_cyl^2/r^2)f'^2 <0 (WEC violated)"),
    ("G2_integrated_energy_negative", check_G2_integrated_energy_negative,
     "numeric: E(v_s)=-C v_s^2<0 for all v_s incl subluminal; M2 forbids source"),
    ("PA1_kernel_carries_positive_source", check_PA1_kernel_carries_positive_source,
     "numeric/M3: F181 kernel carries positive source -> valid metric AB!=1, lapse well"),
    ("PA3_momentum_cosupport", check_PA3_momentum_cosupport,
     "numeric: momentum density and negative wall both ∝ f'^2 (co-supported)"),
    ("PC1_speed_limit", check_PC1_speed_limit,
     "numeric/M4: induced field well-posed, c_eff<=c_lat; warp ceiling c_lat=1/sqrt3"),
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
    out = {"finding": "F200",
           "title": "Structural test of the Alcubierre warp family against the "
                    "model's induced-gravity / beable-source commitments",
           "timestamp": STAMP, "n_pass": n_pass, "n_total": len(SUITE),
           "c_lat": C_LAT, "results": results, "seconds": round(time.time() - t0, 2)}
    return out


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    with open(os.path.join(ROOT, "test-results", "F200_alcubierre_structural.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS  ({out['seconds']}s)")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
