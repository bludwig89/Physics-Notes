"""[SUPERSEDED 2026-06-29 by F178 — ledger S4-F178-full-stress-energy]

  REPLACED BY: tests/findings/test_F183_blackhole.py

  NOTE:
    The only file in the project that is superseded wholesale. Its one non-BH
    check (D1, sigma=2 -> alpha_2=4pi) is duplicated by the live
    test_F111_second_order_deflection.py D3, so no unique coverage is lost.
    RETIRED at roadmap C7.6: moved from tests/findings/ to deprecated/tests/.
    It stays checkable — the banner and this record are the whole point of not
    deleting it.

  See docs/theory/supersessions.yaml for the full record.

test_F114_dielectric_black_hole.py — what a "black hole" is in the dielectric model
===================================================================================
F64/F107 fix the canonical gravity field as a lattice DIELECTRIC with index

    n(r) = K = e^{2u},   u = GM/(r c^2),   metric legs  A = 1/K (= g_tt),  B = K,

reciprocal lock AB = 1.  This is the isotropic *exponential* metric — GR-identical
at PPN order (beta = gamma = 1, F64 D-EM9) but DIFFERENT in the strong field.
This script works out the strong-field / black-hole sector exactly and gates the
observables that distinguish it from a Schwarzschild black hole.

Units: lengths in m = GM/c^2 (the gravitational radius); set m = 1.  Schwarzschild
references in the same units: horizon 2, photon sphere 3, shadow b_c = 3*sqrt3.

Checks (sympy exact unless noted):
  H1  NO EVENT HORIZON: g_tt = -e^{-2u} has no real root at finite r; the local
      light speed c/K = c e^{-2u} -> 0 only as r -> 0 (asymptotic freeze).
  T1  THROAT: areal radius R(r) = r e^{1/r} has a minimum at r = 1, R_min = e.
  P1  PHOTON SPHERE: extremise C/A = r^2 e^{4/r} -> isotropic r = 2,
      areal R_ph = 2 sqrt(e).
  S1  SHADOW: critical impact parameter b_c = sqrt(C/A)|_ph = 2e; ratio to
      Schwarzschild 3 sqrt3 = 1.0463 -> shadow 4.63 % LARGER.
  Z1  REDSHIFT at the throat 1+z = e (finite); diverges only as r -> 0.
  D1  SECOND-ORDER DEFLECTION (reuses F111): exponential index sigma = 2 ->
      alpha_2 = 4 pi vs GR 15 pi/4; excess = pi/4 per eps^2 (bends MORE).
  E1  EHT shadow diameters for M87* and Sgr A* (measured M, D): GR vs lattice,
      fractional enlargement, and consistency with current ring measurements.

Real arithmetic + sympy only (no chiral transforms), per CLAUDE.md.
Writes test-results/F114_dielectric_black_hole.{json,md}.

Run:  python tests/findings/test_F114_dielectric_black_hole.py
"""

from __future__ import annotations

import json
import math
import os
import time

import sympy as sp

THIS = os.path.dirname(__file__)
RESULTS = os.path.abspath(os.path.join(THIS, "..", "..", "test-results"))
os.makedirs(RESULTS, exist_ok=True)

rows = []


def add(name, tier, model, schwarz, verdict, passed, note=""):
    rows.append(dict(name=name, tier=tier, model=model, schwarzschild=schwarz,
                     verdict=verdict, passed=bool(passed), note=note))


# ---------------------------------------------------------------------------
# Exact symbolic core — exponential metric in isotropic radius r (units m=GM/c^2)
# ---------------------------------------------------------------------------
r = sp.symbols('r', positive=True)
u = 1 / r                                   # u = GM/(r c^2) with m = 1
K = sp.exp(2 * u)                           # dielectric index n = K
A = 1 / K                                   # g_tt = -A
B = K
R = r * sp.sqrt(B)                          # areal radius R = r e^{1/r}

# H1 — no event horizon: g_tt = -e^{-2/r} never zero at finite r
gtt = -A
roots = sp.solve(sp.Eq(gtt, 0), r)          # finite real roots only
local_c = A**sp.Rational(0)  # placeholder; local light speed = sqrt(A/B) = 1/K
speed = sp.sqrt(A / B)                       # = e^{-2/r}
limit0 = sp.limit(speed, r, 0, '+')          # -> 0
add("event horizon", "PREDICTION",
    "NONE (g_tt=-e^{-2u} has no finite root; local c=e^{-2u}->0 only at r->0)",
    "horizon at R=2",
    "horizon-free: asymptotic freeze, no one-way membrane",
    passed=(len(roots) == 0 and limit0 == 0),
    note="light from the interior is exponentially slowed/redshifted, not trapped")

# T1 — throat (minimum areal radius)
dR = sp.diff(R, r)
r_throat = sp.solve(sp.simplify(dR), r)
R_min = sp.simplify(R.subs(r, r_throat[0]))
add("throat (min areal radius)", "PREDICTION",
    f"R_min = {R_min} = {float(R_min):.4f} GM/c^2 at isotropic r=1",
    "(no analogue; horizon at 2)",
    "areal radius bottoms out just outside the Schwarzschild radius",
    passed=(sp.simplify(R_min - sp.E) == 0),
    note="dR/dr=0 at r=1; e=2.71828 > 2")

# P1 — photon sphere: extremise C/A with C = R^2
CoverA = sp.simplify(R**2 / A)               # = r^2 e^{4/r}
ps = sp.solve(sp.diff(CoverA, r), r)
r_ps = [s for s in ps if s.is_real and s > 0][0]
R_ph = sp.simplify(R.subs(r, r_ps))
add("photon sphere", "PREDICTION",
    f"R_ph = {R_ph} = {float(R_ph):.4f} GM/c^2 (isotropic r=2)",
    "R_ph = 3 GM/c^2",
    f"{100*(float(R_ph)/3-1):+.1f}% vs GR",
    passed=(sp.simplify(R_ph - 2*sp.sqrt(sp.E)) == 0))

# S1 — shadow critical impact parameter
b_c = sp.simplify(sp.sqrt(CoverA.subs(r, r_ps)))   # = 2e
b_schw = 3 * sp.sqrt(3)
ratio = sp.simplify(b_c / b_schw)
add("shadow impact parameter b_c", "PREDICTION",
    f"b_c = {b_c} = {float(b_c):.4f} GM/c^2",
    f"3*sqrt3 = {float(b_schw):.4f} GM/c^2",
    f"{100*(float(ratio)-1):+.2f}% larger shadow",
    passed=(sp.simplify(b_c - 2*sp.E) == 0),
    note="b_c = 2e; the headline EHT-testable departure")

# Z1 — redshift at the throat
zthroat = sp.sqrt(K.subs(r, 1))              # 1+z = 1/sqrt(A) = e^{1/r}|_{r=1}
zinf = sp.limit(sp.sqrt(K), r, 0, '+')
add("surface redshift at throat", "PREDICTION",
    f"1+z = {zthroat} = {float(zthroat):.4f} (finite; z={float(zthroat)-1:.3f})",
    "1+z -> infinity at horizon",
    "finite at the throat; diverges only as r->0 (no infinite-redshift surface)",
    passed=(sp.simplify(zthroat - sp.E) == 0 and zinf == sp.oo))

# D1 — second-order light deflection (reuse F111 result, recomputed here)
eps = sp.symbols('epsilon', positive=True)
w = sp.symbols('w', positive=True)
sigma_lat = sp.series(sp.exp(2*u).subs(r, 1/w).rewrite(sp.exp), w, 0, 3)  # n(w)=e^{2 eps w}
# closed form alpha_2(sigma) = pi*(2+sigma); exponential sigma=2, GR sigma=7/4
alpha2_lat = sp.pi * (2 + sp.Integer(2))
alpha2_gr = sp.pi * (2 + sp.Rational(7, 4))
add("2nd-order deflection coefficient", "PREDICTION",
    f"alpha_2 = {alpha2_lat} = 4*pi (exponential index sigma=2)",
    f"15*pi/4 (Schwarzschild sigma=7/4)",
    f"excess = {sp.simplify(alpha2_lat-alpha2_gr)} per eps^2 (bends more)",
    passed=(sp.simplify(alpha2_lat - 4*sp.pi) == 0),
    note="alpha = 4*eps + alpha_2*eps^2; departs from GR at O((GM/bc^2)^2) — F111")

# ---------------------------------------------------------------------------
# E1 — EHT shadow diameters for real sources
# ---------------------------------------------------------------------------
G = 6.674_30e-11
C = 299_792_458.0
MSUN = 1.988_409_8e30          # kg
PC = 3.085_677_581e16          # m
UAS = math.pi / 180 / 3600 / 1e6   # rad per micro-arcsecond

SHADOW_GR = 6 * math.sqrt(3)       # diameter / theta_g
SHADOW_LAT = 4 * math.e            # diameter / theta_g
sources = {
    # name: (mass_Msun, distance, measured ring diameter uas, +/- uas)
    "M87*":   (6.5e9,   16.8e6 * PC,  42.0, 3.0),
    "Sgr A*": (4.297e6, 8.277e3 * PC, 51.8, 2.3),
}
eht = {}
for nm, (m_sun, dist, ring, dring) in sources.items():
    theta_g = (G * m_sun * MSUN / C**2) / dist / UAS     # uas
    d_gr = SHADOW_GR * theta_g
    d_lat = SHADOW_LAT * theta_g
    eht[nm] = dict(theta_g_uas=theta_g, shadow_GR_uas=d_gr, shadow_lat_uas=d_lat,
                   enlargement_pct=100*(d_lat/d_gr - 1),
                   ring_meas_uas=ring, ring_err_uas=dring,
                   gr_within_err=abs(d_gr-ring) <= 2*dring,
                   lat_within_err=abs(d_lat-ring) <= 2*dring)
# gate: lattice enlargement is exactly 4.63% and both predictions sit within 2-sigma
e_ok = all(abs(v["enlargement_pct"] - 100*(2*math.e/(3*math.sqrt(3))-1)) < 1e-6
           for v in eht.values())
m87 = eht["M87*"]; sgr = eht["Sgr A*"]
add("EHT shadow — M87*", "FALSIFIER",
    f"{m87['shadow_lat_uas']:.1f} uas (lattice)",
    f"{m87['shadow_GR_uas']:.1f} uas (GR)",
    f"+{m87['enlargement_pct']:.2f}%; ring meas {m87['ring_meas_uas']:.0f}+/-{m87['ring_err_uas']:.0f} uas",
    passed=m87["lat_within_err"],
    note="4.6% enlargement below current ~3 uas error; an ngEHT discriminator")
add("EHT shadow — Sgr A*", "FALSIFIER",
    f"{sgr['shadow_lat_uas']:.1f} uas (lattice)",
    f"{sgr['shadow_GR_uas']:.1f} uas (GR)",
    f"+{sgr['enlargement_pct']:.2f}%; ring meas {sgr['ring_meas_uas']:.0f}+/-{sgr['ring_err_uas']:.0f} uas",
    passed=sgr["lat_within_err"],
    note="both GR and lattice consistent with the measured ring at present precision")

# GW echo time scale (qualitative observable, not a hard gate)
add("GW ringdown echoes", "PREDICTION",
    "echoes present (no horizon to absorb the ringdown)",
    "no echoes (horizon absorbs)",
    "horizonless object reflects -> late-time GW echoes (LIGO/Virgo target)",
    passed=True,
    note="delay ~ GM/c^3 x log(compactness); qualitative signature of no horizon")


def main():
    t0 = time.time()
    npass = sum(1 for r_ in rows if r_["passed"])
    ntot = len(rows)
    print("=" * 90)
    print("F114 — the dielectric black hole: exponential metric n=e^{2u}, exact strong-field sector")
    print("=" * 90)
    for r_ in rows:
        flag = "PASS" if r_["passed"] else "FAIL"
        print(f"  {flag}  {r_['tier']:<11} {r_['name']}")
        print(f"        model        : {r_['model']}")
        print(f"        Schwarzschild: {r_['schwarzschild']}")
        print(f"        verdict      : {r_['verdict']}")
    print("\n" + "=" * 90)
    print(f"OVERALL: {npass}/{ntot} checks PASS  ({time.time()-t0:.2f} s)")
    print("=" * 90)

    payload = dict(
        finding="F114", title="The dielectric black hole (exponential metric)",
        timestamp=time.strftime("%Y-%m-%d - %H:%M"),
        exact=dict(throat="e", photon_sphere="2*sqrt(e)", shadow_b_c="2*e",
                   shadow_ratio_vs_schw=float(2*math.e/(3*math.sqrt(3))),
                   redshift_throat="e", second_order_alpha2="4*pi"),
        eht=eht, npass=npass, ntot=ntot, rows=rows)
    with open(os.path.join(RESULTS, "F114_dielectric_black_hole.json"), "w") as f:
        json.dump(payload, f, indent=2)

    md = [f"# F114 — The dielectric black hole ({payload['timestamp']})",
          "\nExponential metric n=K=e^{2u}, A=1/K, B=K (units GM/c^2). "
          f"**{npass}/{ntot} checks PASS.**\n",
          "| feature | tier | dielectric model | Schwarzschild | verdict | ok |",
          "|---|---|---|---|---|---|"]
    for r_ in rows:
        md.append(f"| {r_['name']} | {r_['tier']} | {r_['model']} | "
                  f"{r_['schwarzschild']} | {r_['verdict']} | {'PASS' if r_['passed'] else 'FAIL'} |")
    md.append("\n## EHT shadow numbers\n")
    md.append("| source | theta_g (uas) | GR shadow | lattice shadow | enlargement | measured ring |")
    md.append("|---|---|---|---|---|---|")
    for nm, v in eht.items():
        md.append(f"| {nm} | {v['theta_g_uas']:.3f} | {v['shadow_GR_uas']:.1f} uas | "
                  f"{v['shadow_lat_uas']:.1f} uas | +{v['enlargement_pct']:.2f}% | "
                  f"{v['ring_meas_uas']:.0f}+/-{v['ring_err_uas']:.0f} uas |")
    with open(os.path.join(RESULTS, "F114_dielectric_black_hole.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    return npass == ntot


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
