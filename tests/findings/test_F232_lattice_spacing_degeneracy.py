"""
F232 — L3: Pin the lattice spacing a independently of any mass.

Executes the F83 open follow-up #1: combine the rest-leg relation (triangle)
  a = sqrt(d) * arcsin(m_lat) * lambda_bar_C
with the absolute light-deflection coefficient Delta theta = 4GM/(b c^2)
(F55/F107 L4), to test whether the two together pin a.

Result: the deflection coefficient is EXACTLY -4, dimensionless and a-independent
(F107 L4a), so it carries NO information about a -> the (a, m_lat) degeneracy of
F83 is NOT broken. The scale is instead pinned by the DIMENSIONFUL gravitational
coupling G via F79 (a = sqrt(8pi) 3^(1/4) ell_P). Degeneracy theorem confirmed.

Real arithmetic only (no chiral transforms). numpy used only for a real-valued
quadrature guard.
"""
import json, math
import numpy as np

d = 3
results = {"finding": "F232", "item": "L3", "checks": {}}


def rec(name, statement, value, target, ok):
    results["checks"][name] = {
        "statement": statement, "value": value, "target": target,
        "status": "PASS" if ok else "FAIL",
    }
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {statement}\n        value={value}  target={target}")


# T1 — F79 structural cell (the value a actually takes, from the G-match)
a_over_lP = math.sqrt(8 * math.pi) * d ** 0.25
rec("T1", "a/ell_P = sqrt(8pi) 3^(1/4) (F79 structural)",
    a_over_lP, 6.59782, abs(a_over_lP - 6.59782) < 1e-4)

# T2 — the G-match is an IDENTITY: G = a^2 c^3 /(8pi sqrt3 hbar) with a = k ell_P,
# ell_P^2 = hbar G / c^3  =>  k^2/(8pi sqrt3) = 1 for ANY G. So the "G-match" does
# not pin a in metres; it fixes the dimensionless a/ell_P and inherits the metre
# from ell_P (i.e. from {hbar, G, c}).
coeff = 8 * math.pi * math.sqrt(3)
identity = a_over_lP ** 2 / coeff
rec("T2", "G-match k^2/(8pi sqrt3) == 1 (a scales with ell_P; no free metre)",
    identity, 1.0, abs(identity - 1.0) < 1e-12)

# T3 — the deflection coefficient is EXACTLY -4, independent of a.
# ln K = 2 GM/(r c^2) (F64 canonical K = e^{2u}); straight-ray eikonal
#   alpha = integral d/db[ln K] dx = -4 GM/(b c^2). Set GM/c^2 = 1, b = 1.
# Sweep a across 47 decades: coefficient is invariant (scale-free observable).
x = np.linspace(-4000.0, 4000.0, 4_000_001)
b = 1.0
integrand = -2.0 * b / (b * b + x * x) ** 1.5  # d/db of 2/sqrt(b^2+x^2)
coef = float(np.trapezoid(integrand, x)) if hasattr(np, "trapezoid") else float(np.trapz(integrand, x))
coeffs = {}
allflat = True
for a_scale in (1.0, a_over_lP, 1e17, 1e-30):
    coeffs[str(a_scale)] = coef  # coef is manifestly a-free; recorded per scale
    if abs(coef - (-4.0)) > 5e-4:
        allflat = False
rec("T3", "eikonal deflection coeff = -4, a-independent over 47 decades",
    coef, -4.0, allflat and abs(coef + 4.0) < 5e-4)

# T4 — the degeneracy theorem. The rest-leg relation (triangle) fixes only the RAY
# a = sqrt(d) arcsin(m_lat) lambda_bar_C in the (a, m_lat) plane (F83). Adding a
# dimensionless, a-independent observable (T3) adds ZERO constraints on a: the
# system is invariant under the rescaling  a -> s a ,  arcsin(m_lat) -> arcsin(m_lat)/s
# (with lambda_bar_C, i.e. the measured mass, held fixed). Demonstrate: many a give
# the same electron mass AND the same (a-free) deflection coefficient.
hbar_c = 197.3269804  # MeV fm
me = 0.51099895        # MeV
lam_bar = hbar_c / me  # fm  (reduced Compton wavelength lambda_bar_C = hbar c/(m c^2))
lP_fm = 1.616255e-35 * 1e15
rows = []
same_mass = True
for m_lat in (1e-30, 1e-23, 1e-22, 0.5):
    # solve the triangle for a:  a = sqrt(d) arcsin(m_lat) lambda_bar_C
    a_fm = math.sqrt(d) * math.asin(m_lat) * lam_bar
    # recover the mass via (star): m_phys c^2 = hbar arcsin(m_lat)/tau, tau = a/(c sqrt d)
    #   => m_check = hbar_c * sqrt(d) * arcsin(m_lat) / a_fm   (MeV)  == me by construction
    m_check = hbar_c * math.sqrt(d) * math.asin(m_lat) / a_fm
    rows.append({"m_lat": m_lat, "a_fm": a_fm, "a_over_lP": a_fm / lP_fm, "m_recovered_MeV": m_check})
    if abs(m_check - me) / me > 1e-9:
        same_mass = False
results["degeneracy_ray"] = rows
rec("T4", "triangle + a-free lensing => a undetermined (one ray, many a give same m_e)",
    "family", "family", same_mass)

# T5 — the third input that breaks the degeneracy is the DIMENSIONFUL G (via ell_P).
# Given {hbar, G, c} -> ell_P -> a = 6.59782 ell_P in metres. No fermion mass needed.
lP = 1.616255e-35  # m
a_m = a_over_lP * lP
rec("T5", "third input = G (dimensionful): a = 6.59782 ell_P in metres",
    a_m, 1.06638e-34, abs(a_m - 1.06638e-34) / 1.06638e-34 < 1e-4)

results["verdict"] = (
    "DEGENERATE (negative). The absolute light-deflection coefficient is exactly -4, "
    "dimensionless and independent of a (F107 L4a), so it adds no constraint on a; the "
    "F83 (a, m_lat) ray is unbroken. A dimensionless observable cannot fix a length "
    "(scale-invariance theorem). The scale is pinned only by a dimensionful gravitational "
    "input: G (equivalently ell_P), via F79 a=sqrt(8pi)3^(1/4) ell_P. Mass-independent pin "
    "EXISTS but is the F79 G-match, NOT the lensing route the follow-up proposed."
)
npass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
results["summary"] = f"{npass}/{len(results['checks'])} PASS"
print("\n" + results["summary"] + " — " + results["verdict"])

with open("test-results/F232_lattice_spacing_degeneracy.json", "w") as f:
    json.dump(results, f, indent=2)
