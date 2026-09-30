"""
NB-001 (p.1): KG field equation, Lagrangian, canonical momentum, Hamiltonian density
for a real scalar field. Cold independent reconstruction — see
docs/theory/notebook-reconstruction-01-scalar-qft-opening.md batch 01.

Verifies, via symbolic Euler-Lagrange on an unconstrained field phi(t,x,y,z):
  1. L = 1/2 (d_mu phi)(d^mu phi) - 1/2 m^2 phi^2  =>  EL eqn reduces to  d_mu d^mu phi + m^2 phi = 0
  2. pi = dL/d(phi_dot) = phi_dot
  3. H = pi*phi_dot - L = 1/2(pi^2 + (grad phi)^2 + m^2 phi^2)
Deterministic, no RNG needed.
"""
import sympy as sp
import json, pathlib

t, x, y, z, m = sp.symbols('t x y z m', real=True)
phi = sp.Function('phi')(t, x, y, z)

phi_t = sp.diff(phi, t)
phi_x = sp.diff(phi, x)
phi_y = sp.diff(phi, y)
phi_z = sp.diff(phi, z)

# metric signature (+,-,-,-): (d^mu phi)(d_mu phi) = phi_t^2 - phi_x^2 - phi_y^2 - phi_z^2
L = sp.Rational(1, 2) * (phi_t**2 - phi_x**2 - phi_y**2 - phi_z**2) - sp.Rational(1, 2) * m**2 * phi**2

# --- Euler-Lagrange: d_mu( dL/d(d_mu phi) ) - dL/dphi = 0, mu = t,x,y,z with metric weights (+,-,-,-)
dL_dphit = sp.diff(L, phi_t)
dL_dphix = sp.diff(L, phi_x)
dL_dphiy = sp.diff(L, phi_y)
dL_dphiz = sp.diff(L, phi_z)
dL_dphi = sp.diff(L, phi)

# d_mu (dL/d(d_mu phi)), PLAIN sum over mu = t,x,y,z (the metric already entered when L was
# written in terms of the component derivatives phi_t, phi_x, phi_y, phi_z themselves).
EL = sp.diff(dL_dphit, t) + sp.diff(dL_dphix, x) + sp.diff(dL_dphiy, y) + sp.diff(dL_dphiz, z) - dL_dphi
EL = sp.expand(EL)

kg_target = sp.diff(phi, t, 2) - sp.diff(phi, x, 2) - sp.diff(phi, y, 2) - sp.diff(phi, z, 2) + m**2 * phi
match_kg = sp.simplify(EL - kg_target) == 0

# --- Hamiltonian via Legendre transform
pi = sp.symbols('pi')
L_explicit = sp.Rational(1, 2) * phi_t**2 - sp.Rational(1, 2) * (phi_x**2 + phi_y**2 + phi_z**2) - sp.Rational(1, 2) * m**2 * phi**2
pi_def = sp.diff(L_explicit, phi_t)
match_pi = sp.simplify(pi_def - phi_t) == 0

H = sp.simplify(pi_def * phi_t - L_explicit)
H_target = sp.Rational(1, 2) * (phi_t**2 + phi_x**2 + phi_y**2 + phi_z**2 + m**2 * phi**2)
match_H = sp.simplify(H - H_target) == 0

result = {
    "build": "NB-001",
    "euler_lagrange_matches_KG": bool(match_kg),
    "canonical_momentum_is_phidot": bool(match_pi),
    "hamiltonian_matches_notebook": bool(match_H),
    "EL_residual": str(sp.simplify(EL - kg_target)),
    "H_residual": str(sp.simplify(H - H_target)),
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-001_kg_scalar.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
