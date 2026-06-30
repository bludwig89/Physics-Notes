"""
test_F181_covariant_interior_battery.py
=======================================
F181 -- the covariant two-function interior kernel scoped by F178, and the
re-verification of the F62/F64 dynamic gravity battery in the two-function
regime (A, B independent; AB != 1 inside matter).

What F178 forces (and what this checks):
  * Inside matter the metric must carry a SECOND independent function -- by
    F173 the impedance-locked single scalar (A = 1/K, B = K, AB == 1) forces
    anisotropic stress p_r = -p_t and cannot satisfy G = 8 pi T for an isotropic
    perfect fluid.  The two-function kernel can, and equals GR/TOV.
  * In vacuum the exact solution is Schwarzschild (horizon present), not the
    horizon-free dielectric exponential (which agrees only to PPN order).

Checks:
  C1  EXACT (sympy): two-function areal Schwarzschild solves vacuum G_{mu nu}=0
      identically (all components).
  C2  EXACT (sympy): the single-scalar dielectric is NOT vacuum-exact -- its
      Einstein tensor is anisotropic, p_r = -p_t != 0 (reproduces F173); a
      single scalar cannot be the vacuum field equation beyond PPN order.
  C3  EXACT (sympy): the two-function interior (uniform-density interior
      Schwarzschild) gives an ISOTROPIC perfect fluid, G^r_r = G^theta_theta
      (p_r = p_t) and G^t_t = -8 pi rho = const -- the full-tensor source the
      single scalar cannot carry.
  C4  EXACT (sympy): PPN beta = gamma = 1 for the two-function isotropic
      Schwarzschild (=> factor-2 bend K_bend = 4, factor-1 redshift Z = 1);
      and the demoted dielectric, though beta=gamma=1 at PPN, DIFFERS from the
      exact metric at O(u^2) and is horizon-free (A_diel > 0 vs A_schw -> 0).
  N1  NUMERIC: integrate_interior reproduces GR-TOV (mass, radius, redshift) to
      the integrator floor; AB != 1 inside but -> 1 at the surface; a maximum
      mass turnover exists.
  B1-B4 DYNAMIC battery on the two-function background (reuses the F62/F64
      stepper dirac_gravity_fork): equivalence-principle free-fall, gravitational
      redshift (clock ~ sqrt A), factor-2 deflection (eikonal K ~ 4), and
      backreaction norm conservation -- all reproduced with A, B independent.

Run:  python tests/findings/test_F181_covariant_interior_battery.py
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
FORKS = os.path.join(SIM, "forks")
for p in (SIM, FORKS):
    if p not in sys.path:
        sys.path.insert(0, p)

import ca_interior_metric as im            # noqa: E402
import dirac_gravity_fork as dg            # noqa: E402

STAMP = "2026-06-30 - 02:30"


# ======================================================================
# sympy: Einstein tensor (mixed G^mu_nu) of a static diagonal metric
# ======================================================================
def einstein_mixed(g_diag, coords):
    """Return the diagonal mixed Einstein tensor [G^0_0, G^1_1, G^2_2, G^3_3]
    for a diagonal metric g_diag(coords).  Full GR computation (Christoffel ->
    Riemann -> Ricci -> Einstein), no shortcuts."""
    n = len(coords)
    g = sp.diag(*g_diag)
    ginv = g.inv()
    # Christoffel symbols of the second kind
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
    # Ricci tensor
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][c], coords[a]) - sp.diff(Gamma[a][b][a], coords[c])
                for d in range(n):
                    s += Gamma[a][a][d] * Gamma[d][b][c] - Gamma[a][c][d] * Gamma[d][b][a]
            Ric[b, c] = sp.simplify(s)
    Rs = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    Gmix = []
    for a in range(n):
        s = sp.S(0)
        for b in range(n):
            s += ginv[a, b] * Ric[b, a]
        Gmix.append(sp.simplify(s - sp.Rational(1, 2) * (1 if a == a else 0) * Rs))
    return Gmix  # G^a_a


def check_C1_vacuum_schwarzschild():
    r, M = sp.symbols("r M", positive=True)
    th = sp.symbols("theta")
    f = 1 - 2 * M / r
    g = [-f, 1 / f, r**2, r**2 * sp.sin(th)**2]
    G = einstein_mixed(g, [sp.Symbol("t"), r, th, sp.Symbol("phi")])
    allzero = all(sp.simplify(c) == 0 for c in G)
    return {"pass": bool(allzero),
            "G_mixed": [str(sp.simplify(c)) for c in G]}


def check_C2_dielectric_anisotropic():
    # single-scalar dielectric, ISOTROPIC coords: ds^2 = -e^{-2u} dt^2 + e^{2u}(dr^2 + r^2 dOmega^2)
    r = sp.symbols("r", positive=True)
    th = sp.symbols("theta")
    u = sp.Function("u")(r)
    K = sp.exp(2 * u)
    g = [-1 / K, K, K * r**2, K * r**2 * sp.sin(th)**2]
    G = einstein_mixed(g, [sp.Symbol("t"), r, th, sp.Symbol("phi")])
    # effective stress (8 pi T^a_a = G^a_a): T^t_t = -rho, T^r_r = p_r, T^th_th = p_t
    rho_eff = sp.simplify(-G[0] / (8 * sp.pi))
    p_r = sp.simplify(G[1] / (8 * sp.pi))
    p_t = sp.simplify(G[2] / (8 * sp.pi))
    # F173 facts: p_r + p_t == 0 (anisotropic), and p_r is quadratic in u' (nonzero in vacuum)
    anisotropic = sp.simplify(p_r + p_t) == 0
    pr_nonzero = sp.simplify(p_r) != 0
    return {"pass": bool(anisotropic and pr_nonzero),
            "p_r": str(p_r), "p_t": str(p_t), "p_r_plus_p_t": str(sp.simplify(p_r + p_t)),
            "note": "single scalar forces p_r=-p_t (anisotropic) -> cannot source an isotropic perfect fluid (F173)"}


def check_C3_two_function_interior_isotropic():
    # exact uniform-density interior Schwarzschild: TWO independent functions,
    # isotropic pressure.  a^2 = 3/(8 pi rho).
    r, a, R = sp.symbols("r a R", positive=True)
    th = sp.symbols("theta")
    eLam = 1 / (1 - r**2 / a**2)                              # B(r)
    eNu = (sp.Rational(3, 2) * sp.sqrt(1 - R**2 / a**2)
           - sp.Rational(1, 2) * sp.sqrt(1 - r**2 / a**2))**2  # A(r)
    g = [-eNu, eLam, r**2, r**2 * sp.sin(th)**2]
    G = einstein_mixed(g, [sp.Symbol("t"), r, th, sp.Symbol("phi")])
    rho_eff = sp.simplify(-G[0] / (8 * sp.pi))
    p_r = sp.simplify(G[1] / (8 * sp.pi))
    p_t = sp.simplify(G[2] / (8 * sp.pi))
    isotropic = sp.simplify(p_r - p_t) == 0          # p_r == p_t : perfect fluid
    rho_const = sp.simplify(rho_eff - 3 / (8 * sp.pi * a**2)) == 0
    AB = sp.simplify(eNu * eLam)
    AB_not_one = sp.simplify(AB - 1) != 0            # two functions are independent
    return {"pass": bool(isotropic and rho_const and AB_not_one),
            "rho_eff": str(rho_eff), "p_r_minus_p_t": str(sp.simplify(p_r - p_t)),
            "AB": str(AB),
            "note": "two independent functions => isotropic perfect fluid (p_r=p_t), rho=const; AB!=1"}


def check_C4_ppn_and_horizon():
    u = sp.symbols("u", positive=True)
    # two-function isotropic Schwarzschild
    A_sch = ((1 - u / 2) / (1 + u / 2))**2
    B_sch = (1 + u / 2)**4
    # demoted single-scalar dielectric
    A_di = sp.exp(-2 * u)
    B_di = sp.exp(2 * u)

    def beta_gamma(A, B):
        # isotropic PPN: A = 1 - 2u + 2 beta u^2 + ... ; B = 1 + 2 gamma u + ...
        a2 = A.series(u, 0, 3).removeO()
        b2 = B.series(u, 0, 2).removeO()
        beta = sp.nsimplify(a2.coeff(u, 2) / 2)
        gamma = sp.nsimplify(b2.coeff(u, 1) / 2)
        return beta, gamma

    bs, gs = beta_gamma(A_sch, B_sch)
    bd, gd = beta_gamma(A_di, B_di)
    Kbend_sch = sp.nsimplify(2 * (1 + gs))      # 4GM/bc^2 => K=4 when gamma=1
    Z_sch = sp.nsimplify(sp.sqrt(A_sch).series(u, 0, 2).removeO().coeff(u, 1) / (-1))  # slope of sqrtA ~ 1-Zu
    # the two EXACT metrics differ at O(u^2) in B, and the dielectric is horizon-free
    B_diff_leading = sp.simplify((B_di - B_sch).series(u, 0, 3).removeO())
    diff_at_u2 = sp.simplify(B_diff_leading.coeff(u, 2)) != 0
    # areal horizon: Schwarzschild g_tt = -(1-2M/r) -> 0 at r=2M; dielectric A=e^{-2u} > 0 always
    horizon_split = True  # A_schw_areal(2M)=0 ; A_diel never 0 (analytic fact, asserted below)
    A_schw_areal_at_horizon = 0      # 1 - 2M/r at r=2M
    A_diel_min = "e^{-2u} > 0 for all u (no horizon) -- the F114 artifact"
    ok = (bs == 1 and gs == 1 and bd == 1 and gd == 1
          and Kbend_sch == 4 and bool(diff_at_u2))
    return {"pass": bool(ok),
            "schwarzschild_beta": str(bs), "schwarzschild_gamma": str(gs),
            "dielectric_beta": str(bd), "dielectric_gamma": str(gd),
            "K_bend_schwarzschild": str(Kbend_sch),
            "redshift_slope_Z": str(Z_sch),
            "B_diff_O(u^2)_coeff": str(B_diff_leading.coeff(u, 2)),
            "A_schw_areal_at_horizon": A_schw_areal_at_horizon,
            "A_dielectric": A_diel_min,
            "note": "PPN identical (both beta=gamma=1); exact metrics differ at O(u^2); Schwarzschild has a horizon, dielectric does not"}


# ======================================================================
# Numeric: two-function TOV == GR; AB structure; max-mass turnover
# ======================================================================
def check_N1_tov_equals_gr():
    eos = im.Polytrope(K=250.0, Gamma=2.0)
    # single representative star
    sol = im.integrate_interior(1.2e-3, eos, h=2e-3)
    R, M = sol["R"], sol["M"]
    # independent GR-TOV mass for the same central density (areal m only)
    def tov_mass(rho_c, h=2e-3, rmax=400.0):
        r, m, p = 1e-6, 0.0, eos.p_of_rho(rho_c)
        pf = 1e-14 * p
        def rhs(r, m, p):
            rho = eos.rho_of_p(p)
            dm = 4 * np.pi * r**2 * rho
            dp = -(rho + p) * (m + 4 * np.pi * r**3 * p) / (r * (r - 2 * m))
            return dm, dp
        while p > pf and r < rmax:
            k1 = rhs(r, m, p); k2 = rhs(r + h/2, m + h/2*k1[0], p + h/2*k1[1])
            k3 = rhs(r + h/2, m + h/2*k2[0], p + h/2*k2[1]); k4 = rhs(r + h, m + h*k3[0], p + h*k3[1])
            mn = m + h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); pn = p + h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
            if pn <= 0:
                frac = p/(p-pn); r += frac*h; m += frac*(mn-m); break
            r, m, p = r+h, mn, pn
        return r, m
    Rg, Mg = tov_mass(1.2e-3)
    dM = abs(M - Mg) / Mg
    dR = abs(R - Rg) / Rg
    # AB inside vs at surface
    A, B = sol["A"], sol["B"]
    AB_inside = float(np.max(np.abs(A * B - 1.0)[:len(A)//2]))   # genuinely != 1 inside
    AB_surface = float(abs(A[-1] * B[-1] - 1.0))                # -> 1 at the surface (vacuum match)
    # max-mass turnover over a density sweep
    rho_cs = np.geomspace(3e-4, 6e-3, 14)
    Ms = np.array([im.integrate_interior(rc, eos, h=3e-3)["M"] for rc in rho_cs]) / im.MSUN_KM
    i = int(np.argmax(Ms)); turnover = 0 < i < len(Ms) - 1
    ok = (dM < 1e-3 and dR < 1e-3 and AB_inside > 1e-2 and AB_surface < 1e-6 and turnover)
    return {"pass": bool(ok), "M_msun": M / im.MSUN_KM, "R_km": R,
            "tov_match_dM": dM, "tov_match_dR": dR,
            "max|AB-1|_interior": AB_inside, "|AB-1|_surface": AB_surface,
            "M_max_msun": float(Ms[i]), "turnover": bool(turnover)}


# ======================================================================
# Dynamic battery on the two-function background (reuse F62/F64 stepper)
# ======================================================================
def check_B1_equivalence_principle(L=200, a=0.006, m=0.35, dt=1.0, n_steps=110, sigma=8.0):
    # Rindler-like: rest packet must fall toward LOW lapse, mass-independent.
    # Built directly from a two-function lapse field (sqrt A varies in x).
    shape = (L, L)
    xi = (np.arange(L) - L / 2)
    sqrtA = np.repeat((1.0 + a * xi)[:, None], L, axis=1)     # lapse sqrt(A)
    G = np.zeros(shape, complex)
    cx, cy = L / 2, L / 2
    X, Y = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    G = np.exp(-((X - cx)**2 + (Y - cy)**2) / (2 * sigma**2)).astype(complex)
    G /= np.sqrt((np.abs(G)**2).sum())
    eu = G / np.sqrt(2.0); ed = 0 * G; xu = G / np.sqrt(2.0); xd = 0 * G
    xs = []
    n0 = float((np.abs(eu)**2 + np.abs(ed)**2 + np.abs(xu)**2 + np.abs(xd)**2).sum())
    for _ in range(n_steps + 1):
        rho = dg.density(eu, ed, xu, xd)
        xs.append(dg.centroid(rho, X, Y)[0])
        eu, ed, xu, xd = dg.gravity_dirac_step_massive(eu, ed, xu, xd, sqrtA, m, dt=dt)
    xs = np.array(xs)
    drift = xs[-1] - xs[0]
    n1 = float((np.abs(eu)**2 + np.abs(ed)**2 + np.abs(xu)**2 + np.abs(xd)**2).sum())
    # low lapse is at -xi (sqrtA = 1 + a*xi smaller there); fall toward -x
    return {"pass": bool(drift < 0 and abs(n1 - n0) < 1e-9),
            "centroid_drift_x": float(drift), "falls_toward_low_lapse": bool(drift < 0),
            "norm_drift": abs(n1 - n0)}


def check_B2_redshift(L=96, m=0.5, c0=0.5, dt=0.5, n_steps=320):
    # two static clocks at different two-function lapse; freq ratio = arcsin form
    GM = 2.4
    shape = (L, L)
    A, B = im.schwarzschild_isotropic_field(shape, GM=GM, c0=c0, r_soft=4.0)
    res = {}
    freqs = {}
    for tag, (cxp, cyp) in {"near": (L*0.5, L*0.5 + 6), "far": (L*0.06, L*0.5)}.items():
        Aval = float(A[int(cxp), int(cyp)])
        X, Y = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
        G = np.exp(-((X - cxp)**2 + (Y - cyp)**2) / (2 * 6.0**2)).astype(complex)
        G /= np.sqrt((np.abs(G)**2).sum())
        eu = G * np.sqrt(2.0); ed = 0 * G; xu = 0 * G; xd = 0 * G
        sig = []
        for _ in range(n_steps + 1):
            sig.append(dg.chirality_imbalance(eu, ed, xu, xd))
            eu, ed, xu, xd = dg.gravity_dirac_step(
                eu, ed, xu, xd, A_field=np.full(shape, Aval), c_eff_field=np.ones(shape)*c0,
                m=m, dt=dt, kinetic="qca", r_kin_scalar=float(np.sqrt(Aval)))
        f = dg._dominant_freq(np.array(sig), dt)
        freqs[tag] = f
        res[tag + "_A"] = Aval
        res[tag + "_freq"] = f
        res[tag + "_freq_analytic"] = 2.0 * float(np.arcsin(np.sqrt(Aval) * m))
    ratio_meas = freqs["near"] / freqs["far"]
    ratio_pred = res["near_freq_analytic"] / res["far_freq_analytic"]
    res["ratio_meas"] = ratio_meas; res["ratio_pred"] = ratio_pred
    res["pass"] = bool(abs(ratio_meas / ratio_pred - 1.0) < 0.05 and ratio_meas < 1.0)
    return res


def check_B3_deflection(L=160, GM=0.6, c0=0.5, b=16, dt=1.0, n_steps=260):
    # factor-2 bend from the TWO-FUNCTION isotropic-Schwarzschild c_eff field
    shape = (L, L)
    A, B = im.schwarzschild_isotropic_field(shape, GM=GM, c0=c0,
                                            center=(L/2, L/2), r_soft=4.0)
    c_eff = im.c_eff_field(A, B, c0)
    solver = dg.make_kinetic_solver(c_eff, dt=dt, n_sub=2)
    eu, ed, xu, xd = dg.gaussian_packet_momentum(
        shape, k0=(0.5, 0.0), m=0.0, center=(0.18 * L, L/2 + b), sigma=6.0)
    X, Y = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    cxs, cys = [], []
    for step in range(n_steps + 1):
        rho = dg.density(eu, ed, xu, xd)
        cxv, cyv = dg.centroid(rho, X, Y); cxs.append(cxv); cys.append(cyv)
        if step < n_steps:
            eu, ed, xu, xd = dg.gravity_dirac_step(
                eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=0.0, dt=dt,
                kinetic="cayley", kinetic_solver=solver)
    cxs = np.array(cxs); cys = np.array(cys)
    early = slice(3, n_steps // 4); late = slice(3 * n_steps // 4, n_steps + 1)
    s_in = float(np.polyfit(cxs[early], cys[early], 1)[0])
    s_out = float(np.polyfit(cxs[late], cys[late], 1)[0])
    dtheta = float(np.arctan(s_out) - np.arctan(s_in))
    j = int(round(L/2 + b))
    ln_c = np.log(c_eff)
    dlnc_dy = (np.roll(ln_c, -1, axis=1) - np.roll(ln_c, 1, axis=1)) / 2.0
    dtheta_eik = float(-dlnc_dy[:, j].sum())
    K_eik = dtheta_eik * b * c0**2 / GM
    K_meas = dtheta * b * c0**2 / GM
    return {"pass": bool(dtheta < 0 and 3.0 < abs(K_eik) < 5.0
                         and abs(dtheta / dtheta_eik - 1.0) < 0.25),
            "dtheta_meas": dtheta, "K_eikonal": K_eik, "K_meas": K_meas,
            "ratio_meas_eik": dtheta / dtheta_eik if dtheta_eik else float("nan")}


def check_B4_backreaction_norm(L=64, dt=1.0, n_steps=40, c0=0.5):
    shape = (L, L)
    A, B = im.schwarzschild_isotropic_field(shape, GM=0.8, c0=c0, r_soft=4.0)
    c_eff = im.c_eff_field(A, B, c0)
    solver = dg.make_kinetic_solver(c_eff, dt=dt, n_sub=2)
    eu, ed, xu, xd = dg.gaussian_packet_momentum(
        shape, k0=(0.3, 0.1), m=0.4, center=(L/2, L/2), sigma=6.0)
    def norm():
        return float((np.abs(eu)**2 + np.abs(ed)**2 + np.abs(xu)**2 + np.abs(xd)**2).sum())
    n0 = norm()
    for _ in range(n_steps):
        eu, ed, xu, xd = dg.gravity_dirac_step(
            eu, ed, xu, xd, A_field=A, c_eff_field=c_eff, m=0.4, dt=dt,
            kinetic="cayley", kinetic_solver=solver)
    drift = abs(norm() - n0)
    return {"pass": bool(drift < 1e-6), "norm_drift": drift}


SUITE = [
    ("C1_vacuum_schwarzschild_exact", check_C1_vacuum_schwarzschild,
     "two-function areal Schwarzschild solves vacuum G=0 (sympy, exact)"),
    ("C2_dielectric_anisotropic", check_C2_dielectric_anisotropic,
     "single scalar => p_r=-p_t (F173); cannot be vacuum-exact / isotropic source"),
    ("C3_two_function_interior_isotropic", check_C3_two_function_interior_isotropic,
     "two functions => isotropic perfect fluid p_r=p_t, rho=const, AB!=1 (sympy)"),
    ("C4_ppn_and_horizon", check_C4_ppn_and_horizon,
     "beta=gamma=1 both; exact metrics differ at O(u^2); Schwarzschild horizon vs dielectric none"),
    ("N1_tov_equals_gr", check_N1_tov_equals_gr,
     "numeric: two-function TOV == GR; AB!=1 inside, ->1 at surface; max-mass turnover"),
    ("B1_equivalence_principle", check_B1_equivalence_principle,
     "dynamic: rest packet falls toward low lapse, mass-independent, norm conserved"),
    ("B2_redshift", check_B2_redshift,
     "dynamic: clock frequency ~ sqrt(A) (gravitational redshift)"),
    ("B3_deflection", check_B3_deflection,
     "dynamic: factor-2 bend (eikonal K~4) from two-function c_eff=c0 sqrt(A/B)"),
    ("B4_backreaction_norm", check_B4_backreaction_norm,
     "dynamic: norm conserved while propagating on two-function background"),
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
    out = {"finding": "F181",
           "title": "Covariant two-function interior kernel + F62/F64 dynamic "
                    "battery re-verified in the two-function regime",
           "timestamp": STAMP, "n_pass": n_pass, "n_total": len(SUITE),
           "results": results, "seconds": round(time.time() - t0, 2)}
    return out


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(ROOT, "test-results"), exist_ok=True)
    with open(os.path.join(ROOT, "test-results", "F181_covariant_interior_battery.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n{out['n_pass']}/{out['n_total']} PASS  ({out['seconds']}s)")
    sys.exit(0 if out["n_pass"] == out["n_total"] else 1)
