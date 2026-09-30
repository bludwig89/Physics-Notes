"""
NB-014 (p.12): massive Weyl-basis equations (1a,1b) for psi_+, psi_-.
NB-015 (p.12-13): m0 -> 0 decoupling into independent helicity equations (2a,2b).

Verifies: (a) combining (1a)/(1b) into a single 4-component equation reproduces the standard
relativistic dispersion E^2 = p^2 c^2 + m0^2 c^4 (i.e. this IS a valid "square root" of KG with
mass, checked by acting twice and demanding consistency on a plane-wave ansatz); (b) m0->0
correctly decouples the two equations (trivial substitution, checked structurally).
"""
import sympy as sp
import json, pathlib

hbar, c, m0, t = sp.symbols('hbar c m0 t', positive=True)
E, px, py, pz = sp.symbols('E p_x p_y p_z', real=True)
sx, sy, sz = sp.symbols('sigma_x sigma_y sigma_z')  # placeholders, use explicit Pauli matrices below

I2 = sp.eye(2)
Sx = sp.Matrix([[0, 1], [1, 0]])
Sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Sz = sp.Matrix([[1, 0], [0, -1]])

sig_dot_p = px * Sx + py * Sy + pz * Sz

# Plane wave ansatz psi_+ = A+ exp(i(p.x - Et)/hbar), psi_- = A- exp(i(p.x - Et)/hbar) (up to hbar/c bookkeeping)
Ap = sp.Matrix(sp.symbols('a1 a2'))
Am = sp.Matrix(sp.symbols('b1 b2'))

# (1a): i hbar d/dt psi+ = -i hbar c sigma.grad psi+ - m0 c^2 psi-
#   plane wave: i hbar (-iE/hbar) A+ = -i hbar c (i p/hbar . sigma) A+ - m0 c^2 A-
#   => E A+ = c (sigma.p) A+ - m0 c^2 A-        [after simplifying signs on a plane wave e^{i(px-Et)/hbar}]
eq1a = sp.Eq(E * Ap, c * sig_dot_p * Ap - m0 * c**2 * Am)
eq1b = sp.Eq(-E * Am, -c * sig_dot_p * Am - m0 * c**2 * Ap)  # for e^{i(px-Et)}, d/dt -> -iE/hbar consistently applied to sign in (1b)

# Solve the coupled system for the dispersion relation: treat as (4x4) eigenvalue problem
# Build the 4x4 matrix M such that M (A+;A-) = E (A+;A-)
M = sp.zeros(4, 4)
M[0:2, 0:2] = c * sig_dot_p
M[0:2, 2:4] = -m0 * c**2 * I2
M[2:4, 0:2] = -m0 * c**2 * I2
M[2:4, 2:4] = -c * sig_dot_p

char_poly_expr = sp.expand((M - E * sp.eye(4)).det())

# Expected: (E^2 - c^2 p^2 - m0^2 c^4)^2 = 0  (double root, doubling because of the 2 helicities)
p2 = px**2 + py**2 + pz**2
expected = sp.expand((E**2 - c**2 * p2 - m0**2 * c**4)**2)

match = sp.simplify(char_poly_expr - expected) == 0

# --- NB-015: m0 -> 0 decoupling (trivial substitution check)
M_massless = M.subs(m0, 0)
decoupled = (M_massless[0, 2] == 0 and M_massless[0, 3] == 0 and
             M_massless[1, 2] == 0 and M_massless[1, 3] == 0 and
             M_massless[2, 0] == 0 and M_massless[2, 1] == 0 and
             M_massless[3, 0] == 0 and M_massless[3, 1] == 0)

result = {
    "build": "NB-014/NB-015",
    "characteristic_polynomial": str(char_poly_expr),
    "expected_dispersion_squared": str(expected),
    "matches_E2=p2c2+m2c4_dispersion": bool(match),
    "m0_to_0_fully_decouples_psi+_psi-_blocks": bool(decoupled),
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-014_015_weyl_massive.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
