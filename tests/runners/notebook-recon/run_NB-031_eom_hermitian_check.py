"""
NB-031 (p.25): the final boxed EOM q^mu (d_mu eta + Omega_mu eta) = 0 is obtained by combining
  (2a) eta^+_;mu q^mu = 0     (the conjugate-field equation)
  (2b) q^mu eta_;mu = 0       (the field equation itself)
and the notebook asserts: "if q^mu is Hermitian, q^mu+ = q^mu, these are just the same
equation."

This script checks PRECISELY what that claim requires: does Hermiticity of q^mu ALONE force
(2a) and (2b) to be equivalent, with NO additional assumption needed on Omega_mu (which the
notebook does not assume Hermitian or anti-Hermitian)? Checked with fully generic (non-Hermitian)
complex 2x2 Omega and a generic HERMITIAN q, using symbolic dagger (conjugate transpose), not
just a schematic hand-wave.
"""
import sympy as sp
import json, pathlib

# generic complex 2x2 Omega (NOT assumed Hermitian)
o11, o12, o21, o22 = sp.symbols('o11 o12 o21 o22', complex=True)
Omega = sp.Matrix([[o11, o12], [o21, o22]])

# generic Hermitian q: q = a*sigma0 + bx*sigma_x + by*sigma_y + bz*sigma_z with a,bx,by,bz real
a, bx, by, bz = sp.symbols('a bx by bz', real=True)
I2 = sp.eye(2)
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
q = a * I2 + bx * sx + by * sy + bz * sz
q_dagger = q.H  # conjugate transpose
q_is_hermitian = sp.simplify(q - q_dagger) == sp.zeros(2, 2)

# generic spinor eta and its derivative d_mu eta (independent symbol, since d_mu eta is not
# algebraically related to eta itself -- we're checking an operator identity, so both eta and
# d_mu eta are free)
e1, e2, de1, de2 = sp.symbols('e1 e2 de1 de2', complex=True)
eta = sp.Matrix([e1, e2])
deta = sp.Matrix([de1, de2])  # stands for d_mu eta

eta_cov = deta + Omega * eta          # eta_;mu = d_mu eta + Omega_mu eta

# (2b): q * eta_;mu
eq_2b = q * eta_cov

# (2a): eta^+_;mu q, where eta^+_;mu = (eta_;mu)^+ = deta^+ + eta^+ Omega^+
eta_cov_dagger = eta_cov.H  # (d_mu eta + Omega eta)^+ = d_mu eta^+ + eta^+ Omega^+
eq_2a_row = eta_cov_dagger * q       # 1x2 row vector

# dagger of (2a)'s row equation should equal (2b) IF q is Hermitian and this is the only
# assumption needed
eq_2a_dagger = eq_2a_row.H           # back to a 2x1 column

residual = sp.simplify(eq_2a_dagger - eq_2b)
match = residual == sp.zeros(2, 1)

result = {
    "build": "NB-031",
    "q_is_hermitian_by_construction": bool(q_is_hermitian),
    "dagger_of_(2a)_minus_(2b)_residual": str(residual),
    "hermiticity_of_q_alone_is_sufficient_no_extra_condition_on_Omega_needed": bool(match),
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-031_eom_hermitian_check.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
