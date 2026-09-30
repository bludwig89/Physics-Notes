"""
NB-109/NB-110 (pp.83-84): rather than re-trace the notebook's full multi-step derivation
pipeline (U_DW -> basis images -> gamma_i -> u(k)) to every transcribed sign -- which turned out
to itself contain an isolated arithmetic slip (see run_NB-105_110_dirac_weyl_transform.py: the
notebook's own explicit U_DW matrix has the wrong sign in its (2,2) entry relative to U_DW=U_0*Uy
as actually computed from its own stated U_0, U_y) -- this script instead applies the more
robust, convention-independent test: do the notebook's own BOXED FINAL spinors actually solve
the momentum-space Dirac equation (gamma^mu k_mu - m) psi = 0 in the Weyl representation, for
on-shell momentum (k_0^2 - k_3^2 = m^2)? This is the physically meaningful question regardless
of which specific derivation path produced the answer.
"""
import sympy as sp
import json, pathlib

s0 = sp.eye(2)
s1 = sp.Matrix([[0, 1], [1, 0]])
s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
s3 = sp.Matrix([[1, 0], [0, -1]])


def kron(A, B):
    return sp.Matrix(sp.kronecker_product(A, B))


# Weyl-rep gammas (p.83, verified in the companion script): gamma^0 = beta = -s1 (x) s0,
# gamma^i = beta*alpha_i = -i s2 (x) s_i
gamma0 = kron(-s1, s0)
gamma3 = kron(-sp.I * s2, s3)

k0, k3, m = sp.symbols('k_0 k_3 m', real=True)
onshell = {k3: sp.sqrt(k0**2 - m**2)}  # substitute k3 in terms of k0,m for the on-shell check
# (keeping k0,k3 symbolic and only substituting the on-shell relation numerically per case avoids
# a messy square-root expression propagating through everywhere; do the check numerically instead)

DiracOp = gamma0 * k0 - gamma3 * k3 - m * sp.eye(4)


def dirac_residual_numeric(spinor_expr, k0_val, m_val, sign_k3=1, mass_sign=-1):
    # mass_sign=-1: particle equation (gamma.k - m)u=0; mass_sign=+1: antiparticle equation
    # (gamma.k + m)v=0 -- the v(k) solutions in NB-109/110 are built with a +mI term (per p.82's
    # own v^alpha(k) = (-gamma^mu k_mu + m I)/norm v^alpha(0) formula), so they should be tested
    # against (gamma.k + m)v=0, not (gamma.k - m)v=0.
    k3_val = sign_k3 * sp.sqrt(k0_val**2 - m_val**2)
    op = gamma0 * k0 - gamma3 * k3 + mass_sign * m * sp.eye(4)
    op_num = op.subs({k0: k0_val, k3: k3_val, m: m_val})
    spinor_num = spinor_expr.subs({k0: k0_val, k3: k3_val, m: m_val})
    res = sp.simplify(op_num * spinor_num)
    total = 0.0
    for c in res:
        cn = complex(sp.N(c))
        total += abs(cn)
    return res, total


norm_generic = sp.sqrt(sp.Symbol('N', positive=True))  # overall normalization is irrelevant to solving a homogeneous eqn

# notebook's boxed spinors (amplitude only, normalization factor dropped -- irrelevant for a
# homogeneous linear equation)
psi_z_2plus = sp.Matrix([(1 + sp.I) * (k3 - k0 - m), 0, (1 + sp.I) * (k3 + k0 + m), 0])
psi_z_1minus = sp.Matrix([(1 - sp.I) * (k0 - k3) + (1 + sp.I) * m, 0, (1 + sp.I) * (k0 + k3) + (1 - sp.I) * m, 0])
psi_z_2minus = sp.Matrix([0, (1 - sp.I) * (k0 + k3) + (1 + sp.I) * m, 0, (1 + sp.I) * (k0 - k3) + (1 - sp.I) * m])

test_k0, test_m = sp.Rational(5, 1), sp.Rational(2, 1)

results = {}
for name, spinor, mass_sign in [("psi_z_2plus_(particle,_gamma.k-m)", psi_z_2plus, -1),
                                 ("psi_z_1minus_(antiparticle,_gamma.k+m)", psi_z_1minus, 1),
                                 ("psi_z_2minus_(antiparticle,_gamma.k+m)", psi_z_2minus, 1)]:
    # sign of k3 tested both ways to find which (if either) solves the equation, rather than
    # assuming one -- and using the CORRECT equation for each branch (particle: gamma.k-m=0;
    # antiparticle: gamma.k+m=0, matching p.82's own v^alpha(k) = (-gamma^mu k_mu + mI)/norm
    # v^alpha(0) definition).
    res_plus, mag_plus = dirac_residual_numeric(spinor, test_k0, test_m, sign_k3=1, mass_sign=mass_sign)
    res_minus, mag_minus = dirac_residual_numeric(spinor, test_k0, test_m, sign_k3=-1, mass_sign=mass_sign)
    results[name] = {
        "residual_norm_with_k3=+sqrt(k0^2-m^2)": abs(mag_plus),
        "residual_norm_with_k3=-sqrt(k0^2-m^2)": abs(mag_minus),
        "solves_dirac_eq_for_either_sign_of_k3": bool(abs(mag_plus) < 1e-9 or abs(mag_minus) < 1e-9),
    }

print(json.dumps(results, indent=2, default=str))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-109_110_dirac_equation_check.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(results, indent=2, default=str))
print("wrote", out)
