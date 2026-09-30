"""
NB-076 (p.59): standard Dirac alpha_i, beta from (alpha.p c + m c^2 beta)^2 = (p^2c^2+m^2c^4)I,
representation alpha_i = sigma3 (x) sigma_i, beta = -sigma1 (x) sigma0.
NB-077 (p.59): non-uniqueness -- beta = (a sigma1 + b sigma2) (x) sigma0, a^2+b^2=1, solves the
same algebra.
NB-078 (p.60): gauging beta_g = (U sigma1 U^+) (x) sigma0, U = diag(1, e^{i theta}) -- does this
remain a valid Dirac beta (same algebra) for every theta?

Verified: explicit 4x4 matrices (tensor products of Pauli matrices), Dirac algebra relations
{alpha_i, alpha_j} = 2 delta_ij, {alpha_i, beta} = 0, beta^2 = I checked directly by matrix
multiplication for the standard rep, for the general (a,b) rep, and for the gauged rep at a
generic symbolic theta.
"""
import sympy as sp
import json, pathlib

I2 = sp.eye(2)
s0 = sp.eye(2)
s1 = sp.Matrix([[0, 1], [1, 0]])
s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
s3 = sp.Matrix([[1, 0], [0, -1]])


def kron(A, B):
    return sp.Matrix(sp.kronecker_product(A, B))


alpha = [kron(s3, s1), kron(s3, s2), kron(s3, s3)]  # alpha_i = sigma3 (x) sigma_i
beta_std = kron(-s1, s0)


def check_dirac_algebra(alpha_list, beta):
    ok = True
    details = {}
    for i in range(3):
        for j in range(3):
            anticomm = sp.simplify(alpha_list[i] * alpha_list[j] + alpha_list[j] * alpha_list[i])
            target = 2 * (1 if i == j else 0) * sp.eye(4)
            if sp.simplify(anticomm - target) != sp.zeros(4, 4):
                ok = False
    for i in range(3):
        anticomm_ab = sp.simplify(alpha_list[i] * beta + beta * alpha_list[i])
        if anticomm_ab != sp.zeros(4, 4):
            ok = False
    beta_sq = sp.simplify(beta * beta)
    if beta_sq != sp.eye(4):
        ok = False
    return ok


std_ok = check_dirac_algebra(alpha, beta_std)

# --- NB-077: general (a,b) beta with a^2+b^2=1
a, b = sp.symbols('a b', real=True)
beta_ab = kron(a * s1 + b * s2, s0)
# check algebra symbolically, using a^2+b^2=1 as a substitution where needed
ab_ok = True
for i in range(3):
    anticomm_ab = sp.simplify(alpha[i] * beta_ab + beta_ab * alpha[i])
    if anticomm_ab != sp.zeros(4, 4):
        ab_ok = False
beta_ab_sq = sp.expand(beta_ab * beta_ab)
beta_ab_sq_simplified = beta_ab_sq.applyfunc(lambda e: sp.simplify(e.subs(b**2, 1 - a**2)))
beta_ab_sq_ok = beta_ab_sq_simplified == sp.eye(4)

# --- NB-078: gauged beta_g = (U s1 U^+) (x) s0, U = diag(1, e^{i theta})
theta = sp.symbols('theta', real=True)
U = sp.Matrix([[1, 0], [0, sp.exp(sp.I * theta)]])
Udag = U.H
beta_g_block = sp.simplify(U * s1 * Udag)
beta_g = kron(beta_g_block, s0)

gauged_ok = True
for i in range(3):
    anticomm_g = sp.simplify(alpha[i] * beta_g + beta_g * alpha[i])
    if anticomm_g != sp.zeros(4, 4):
        gauged_ok = False
beta_g_sq = sp.simplify(beta_g * beta_g)
beta_g_sq_ok = beta_g_sq == sp.eye(4)

result = {
    "build": "NB-076/NB-077/NB-078",
    "NB-076_standard_rep_satisfies_dirac_algebra": bool(std_ok),
    "NB-077_general_(a,b)_rep_anticommutes_with_alpha_i": bool(ab_ok),
    "NB-077_general_(a,b)_rep_beta_squared_equals_I_given_a2+b2=1": bool(beta_ab_sq_ok),
    "NB-078_gauged_beta_still_anticommutes_with_alpha_i_for_ALL_theta": bool(gauged_ok),
    "NB-078_gauged_beta_squared_equals_I_for_ALL_theta": bool(beta_g_sq_ok),
    "note": "NB-078's gauged beta_g depends only on the UPPER-LEFT 2x2 block (the alpha_i = "
            "sigma3 (x) sigma_i representation acts trivially -- via the identity sigma0 -- on "
            "the second tensor factor where beta lives), which is exactly why gauging beta only "
            "affects 'one half of the bispinor' as the notebook observes: the algebra survives "
            "for any theta because alpha_i never touches that second factor's phase at all.",
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-076_077_078_dirac_matrix_nonuniqueness.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
