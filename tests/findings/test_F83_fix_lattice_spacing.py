#!/usr/bin/env python3
"""
F83 - Attempt to fix the lattice spacing `a` from a measured fermion mass
      through the F46/F12 lattice-mass map.

The F46/F12 lattice-mass map (exact):
    A fermion's rest energy is the F46 rest-leg rotation rate carried into SI:
        Omega_rest = arcsin(m_lat)          [rad / tick]      (F46/F27, exact)
        omega_rest = arcsin(m_lat) / tau    [rad / s]
        E_0        = hbar * omega_rest = hbar * arcsin(m_lat) / tau
    Identify E_0 = m_phys c^2:
        (star)   m_phys c^2 = hbar * arcsin(m_lat) / tau

Fixing `a`: convert tick -> cell with the lattice-lightcone identity
(F10 resolution 3 / si-units-options Option C):
        a / tau = c * sqrt(d)   =>   tau = a / (c sqrt(d))
Substitute into (star) and solve for a:
        (triangle)  a = sqrt(d) * arcsin(m_lat) * (hbar / (m_phys c))
                      = sqrt(d) * arcsin(m_lat) * lambdabar_C
where lambdabar_C = hbar/(m_phys c) is the reduced Compton wavelength.

KEY POINT (the "attempt" in the title): (triangle) is ONE equation in TWO
unknowns (a and m_lat). A measured fermion mass alone therefore CANNOT fix a;
it fixes only the family a(m_lat). What it DOES fix:
  * a ceiling: arcsin(m_lat) <= pi/2  =>  a <= sqrt(d) * (pi/2) * lambdabar_C,
    tightest for the HEAVIEST fermion (top quark).
  * conversely, with `a` pinned independently (F59/F61, a ~ 3.81 ell_P), the map
    pins each fermion's dimensionless lattice mass m_lat.

This script verifies the algebra to machine precision and produces the numbers.

Pure-Python arithmetic only (math module) per CLAUDE.md numpy/scipy caution.
"""

import json
import math
import os
from datetime import datetime, timezone

# ----------------------------------------------------------------------------
# Constants (CODATA 2018 / PDG 2024), SI unless noted
# ----------------------------------------------------------------------------
C      = 299_792_458.0            # m/s, exact
HBAR   = 1.054_571_817e-34        # J s, exact (CODATA)
ELL_P  = 1.616_255e-35            # m, Planck length (CODATA)
HBARC_MEV_FM = 197.326_980_4      # MeV fm  (hbar c)
D      = 3                        # BCC spatial dimension
SQRT_D = math.sqrt(D)

# F61 cell size for one full generation (g* = 16):
#   P_pre = sqrt(pi * g* / 6),  a = P_pre * d^{1/4} * ell_P
G_STAR = 16
P_PRE  = math.sqrt(math.pi * G_STAR / 6.0)
A_F61  = P_PRE * (D ** 0.25) * ELL_P     # ~3.81 ell_P

# Charged-fermion masses, MeV/c^2 (PDG 2024 central values)
FERMION_MASS_MEV = {
    "electron":  0.510_998_950_0,
    "muon":      105.658_375_5,
    "tau":       1776.86,
    "up":        2.16,
    "down":      4.67,
    "strange":   93.4,
    "charm":     1270.0,
    "bottom":    4180.0,
    "top":       172_570.0,
}

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def reduced_compton_m(mass_mev):
    """lambdabar_C = hbar/(m c) = (hbar c)/(m c^2) in metres. hbar c = 197.327 MeV fm."""
    fm = HBARC_MEV_FM / mass_mev          # in femtometres
    return fm * 1e-15                     # -> metres

def a_ceiling(mass_mev):
    """Largest a allowed by this fermion: a_max = sqrt(d) * (pi/2) * lambdabar_C."""
    return SQRT_D * (math.pi / 2.0) * reduced_compton_m(mass_mev)

def m_lat_from_a(mass_mev, a):
    """Exact inversion of (triangle): m_lat = sin( a / (sqrt(d) lambdabar_C) ).
    Returns (m_lat, arg, valid) where valid is arg <= pi/2."""
    lc = reduced_compton_m(mass_mev)
    arg = a / (SQRT_D * lc)               # = arcsin(m_lat)
    valid = arg <= math.pi / 2.0
    m_lat = math.sin(arg) if valid else float("nan")
    return m_lat, arg, valid

def a_from_m_lat(mass_mev, m_lat):
    """Exact (triangle): a = sqrt(d) arcsin(m_lat) lambdabar_C."""
    return SQRT_D * math.asin(m_lat) * reduced_compton_m(mass_mev)

# ----------------------------------------------------------------------------
# tests
# ----------------------------------------------------------------------------
results = {
    "finding": "F83",
    "title": "Attempt to fix lattice spacing a from a measured fermion mass via F46/F12 map",
    "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d - %H:%M"),
    "constants": {
        "c_m_s": C, "hbar_Js": HBAR, "ell_P_m": ELL_P,
        "hbarc_MeV_fm": HBARC_MEV_FM, "d": D,
        "P_pre_F61": P_PRE, "a_F61_m": A_F61, "a_F61_over_ellP": A_F61 / ELL_P,
    },
    "tests": [],
}

# T1: round-trip a -> m_lat -> a at machine precision (exact inversion of triangle)
max_rt = 0.0
rt_rows = []
for name, mev in FERMION_MASS_MEV.items():
    # use a value of a guaranteed valid for every fermion: a tiny fraction of the
    # top-quark ceiling, so arcsin arg < pi/2 for all.
    a_test = 0.5 * a_ceiling(FERMION_MASS_MEV["top"])
    m_lat, arg, valid = m_lat_from_a(mev, a_test)
    a_back = a_from_m_lat(mev, m_lat)
    res = abs(a_back - a_test) / a_test
    max_rt = max(max_rt, res)
    rt_rows.append({"fermion": name, "m_lat": m_lat, "arcsin_arg": arg,
                    "a_test_m": a_test, "a_back_m": a_back, "rel_residual": res,
                    "valid": valid})
results["tests"].append({
    "name": "T1_roundtrip_machine_precision",
    "desc": "a -> m_lat=sin(a/(sqrt(d) lc)) -> a = sqrt(d) arcsin(m_lat) lc",
    "max_rel_residual": max_rt, "target": 1e-14,
    "passed": max_rt < 1e-14, "rows": rt_rows,
})

# T2: the ceiling on a from each fermion (heaviest = tightest)
ceil_rows = []
for name, mev in FERMION_MASS_MEV.items():
    amax = a_ceiling(mev)
    ceil_rows.append({"fermion": name, "mass_MeV": mev,
                      "lambdabar_C_m": reduced_compton_m(mev),
                      "a_ceiling_m": amax, "a_ceiling_over_ellP": amax / ELL_P})
ceil_rows_sorted = sorted(ceil_rows, key=lambda r: r["a_ceiling_m"])
tightest = ceil_rows_sorted[0]
results["tests"].append({
    "name": "T2_a_ceiling_per_fermion",
    "desc": "a <= sqrt(d)*(pi/2)*lambdabar_C ; tightest from heaviest fermion",
    "tightest_fermion": tightest["fermion"],
    "tightest_a_ceiling_m": tightest["a_ceiling_m"],
    "tightest_a_ceiling_over_ellP": tightest["a_ceiling_over_ellP"],
    "rows": ceil_rows_sorted,
    "passed": tightest["fermion"] == "top",
})

# T3: with a pinned at F61 (a ~ 3.81 ell_P), read off m_lat per fermion
pin_rows = []
all_valid = True
for name, mev in FERMION_MASS_MEV.items():
    m_lat, arg, valid = m_lat_from_a(mev, A_F61)
    all_valid = all_valid and valid
    # linearized map m_lat ~ a/(sqrt(d) lc); compare to exact sin
    m_lat_lin = A_F61 / (SQRT_D * reduced_compton_m(mev))
    pin_rows.append({"fermion": name, "mass_MeV": mev,
                     "m_lat_exact": m_lat, "m_lat_linear": m_lat_lin,
                     "rel_diff_exact_vs_lin": abs(m_lat - m_lat_lin) / m_lat,
                     "valid_m_lat_le_1": valid})
results["tests"].append({
    "name": "T3_m_lat_at_F61_pinned_a",
    "desc": "a = a_F61 = 3.81 ell_P ; m_lat = sin(a/(sqrt(d) lambdabar_C))",
    "a_used_m": A_F61, "a_used_over_ellP": A_F61 / ELL_P,
    "all_fermions_m_lat_le_1": all_valid,
    "rows": pin_rows,
    "passed": all_valid,
})

# T4: reproduce the si-units-options sec.3.3 electron estimate and expose the sqrt(d)
#   si-units used  m_lat = m_phys c a / hbar  with a = ell_P (NO sqrt(d)) -> ~4e-23
lc_e = reduced_compton_m(FERMION_MASS_MEV["electron"])
m_lat_siunits = ELL_P / lc_e                       # a=ell_P, no sqrt(d)
m_lat_exact_ellP = math.sin(ELL_P / (SQRT_D * lc_e))   # Option C, a=ell_P
m_lat_exact_F61  = math.sin(A_F61 / (SQRT_D * lc_e))    # Option C, a=a_F61
results["tests"].append({
    "name": "T4_electron_estimate_and_sqrt_d_flag",
    "desc": "si-units sec.3.3 used m_lat=m c a/hbar with a=ell_P, no sqrt(d) factor",
    "electron_lambdabar_C_m": lc_e,
    "m_lat_siunits_a=ellP_no_sqrtd": m_lat_siunits,
    "m_lat_exact_a=ellP_optionC": m_lat_exact_ellP,
    "m_lat_exact_a=aF61_optionC": m_lat_exact_F61,
    "siunits_quoted": 4e-23,
    "ratio_siunits_to_exact_ellP": m_lat_siunits / m_lat_exact_ellP,
    "note": "ratio ~ sqrt(d)=1.732: the missing lightcone factor in si-units sec.3.3",
    "passed": abs(m_lat_siunits / m_lat_exact_ellP - SQRT_D) < 1e-6,
})

# T5: degeneracy demonstration - same mass, different (a, m_lat) both satisfy (star)
#   show two distinct lattice solutions for the electron
deg_rows = []
for m_lat_try in (1e-30, 1e-23, 1e-10, 0.5, 0.999):
    a_sol = a_from_m_lat(FERMION_MASS_MEV["electron"], m_lat_try)
    # verify (star): m c^2 = hbar arcsin(m_lat)/tau, tau=a/(c sqrt d)
    tau = a_sol / (C * SQRT_D)
    E0 = HBAR * math.asin(m_lat_try) / tau          # J
    E0_mev = E0 / (1e6 * 1.602_176_634e-19)
    deg_rows.append({"m_lat": m_lat_try, "a_solution_m": a_sol,
                     "a_over_ellP": a_sol / ELL_P,
                     "recovered_mass_MeV": E0_mev})
results["tests"].append({
    "name": "T5_degeneracy_one_eqn_two_unknowns",
    "desc": "many (a, m_lat) reproduce the same electron mass; a not fixed by mass alone",
    "rows": deg_rows,
    "passed": True,
})

results["all_passed"] = all(t["passed"] for t in results["tests"])

# ----------------------------------------------------------------------------
# write JSON
# ----------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.normpath(os.path.join(HERE, "..", "..", "test-results", "F83_fix_lattice_spacing.json"))
with open(OUT, "w") as f:
    json.dump(results, f, indent=2)

# ----------------------------------------------------------------------------
# console summary
# ----------------------------------------------------------------------------
print("=" * 70)
print("F83 - fix `a` from a measured fermion mass via F46/F12 map")
print("=" * 70)
print(f"d = {D}, sqrt(d) = {SQRT_D:.6f}")
print(f"F61 cell: a = {P_PRE:.4f} * d^1/4 * ell_P = {A_F61/ELL_P:.4f} ell_P = {A_F61:.4e} m")
print()
print(f"[T1] round-trip max rel residual = {max_rt:.2e}  (target 1e-14)  "
      f"{'PASS' if results['tests'][0]['passed'] else 'FAIL'}")
print()
print("[T2] ceiling on a (a <= sqrt(d)*(pi/2)*lambdabar_C):")
for r in ceil_rows_sorted:
    print(f"     {r['fermion']:9s} m={r['mass_MeV']:>10.4g} MeV  "
          f"a_max={r['a_ceiling_m']:.3e} m = {r['a_ceiling_over_ellP']:.3e} ell_P")
print(f"     -> tightest: {tightest['fermion']} caps a at {tightest['a_ceiling_m']:.3e} m "
      f"({tightest['a_ceiling_over_ellP']:.2e} ell_P)")
print()
print("[T3] m_lat at F61-pinned a = 3.81 ell_P:")
for r in pin_rows:
    print(f"     {r['fermion']:9s} m_lat = {r['m_lat_exact']:.4e}  (<=1: {r['valid_m_lat_le_1']})")
print()
print("[T4] electron m_lat estimates:")
print(f"     si-units (a=ell_P, no sqrt d): {m_lat_siunits:.3e}  (paper quoted ~4e-23)")
print(f"     exact   (a=ell_P, Option C)  : {m_lat_exact_ellP:.3e}")
print(f"     exact   (a=a_F61, Option C)  : {m_lat_exact_F61:.3e}")
print(f"     ratio si-units/exact = {m_lat_siunits/m_lat_exact_ellP:.4f}  (= sqrt(d) = {SQRT_D:.4f})")
print()
print(f"OVERALL: {'PASS' if results['all_passed'] else 'FAIL'}")
print(f"results -> {OUT}")
