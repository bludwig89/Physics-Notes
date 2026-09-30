"""
NB-114 (pp.86-88): four boxed mass-perturbed plane-wave spinors (6A-6D):
    Psi_RP = N ((k0+k3)^2+lam0^2)^{-1/2} (k0+k3, 0, lam0, 0)^T          [right-handed particle, k0>0]
    Psi_LA = N ((k0-k3)^2+lam0^2)^{-1/2} (lam0, 0, k0-k3, 0)^T          [left-handed antiparticle, k0<0]
    Psi_RA = N ((k0-k3)^2+lam0^2)^{-1/2} (0, k0-k3, 0, lam0)^T          [right-handed antiparticle, k0<0]
    Psi_LP = N ((k0+k3)^2+lam0^2)^{-1/2} (0, lam0, 0, k0+k3)^T          [left-handed particle, k0>0]
with lam0 = m0*c/hbar, on-shell k0^2-k3^2=lam0^2 (p.87's own boxed relation).

Verified with the same robust, convention-independent Dirac-equation test used for NB-109/110:
do these solve (gamma.k -/+ m)Psi=0 (particle/antiparticle) in the Weyl representation, for
on-shell momentum? This sidesteps re-tracing the full (3a)-(4d) derivation chain and directly
tests whether the FINAL boxed results are physically correct.
"""
import sympy as sp
import json, pathlib

s0 = sp.eye(2)
s1 = sp.Matrix([[0, 1], [1, 0]])
s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
s3 = sp.Matrix([[1, 0], [0, -1]])


def kron(A, B):
    return sp.Matrix(sp.kronecker_product(A, B))


gamma0 = kron(-s1, s0)
gamma3 = kron(-sp.I * s2, s3)

k0, k3, lam0 = sp.symbols('k_0 k_3 lambda_0', real=True)

Psi_RP = sp.Matrix([k0 + k3, 0, lam0, 0])
Psi_LA = sp.Matrix([lam0, 0, k0 - k3, 0])
Psi_RA = sp.Matrix([0, k0 - k3, 0, lam0])
Psi_LP = sp.Matrix([0, lam0, 0, k0 + k3])


def check(spinor, mass_sign, k0_val, lam0_val, k3_sign):
    k3_val = k3_sign * sp.sqrt(k0_val**2 - lam0_val**2)
    op = gamma0 * k0 - gamma3 * k3 + mass_sign * lam0 * sp.eye(4)
    op_num = op.subs({k0: k0_val, k3: k3_val, lam0: lam0_val})
    spinor_num = spinor.subs({k0: k0_val, k3: k3_val, lam0: lam0_val})
    res = sp.simplify(op_num * spinor_num)
    total = sum(abs(complex(sp.N(c))) for c in res)
    return total


test_lam0 = sp.Rational(3, 10)
results = {}
for name, spinor, mass_sign, k0_vals in [
    ("Psi_RP_(particle,k0>0)", Psi_RP, -1, [sp.Rational(3, 1)]),
    ("Psi_LA_(antiparticle,k0<0)", Psi_LA, 1, [sp.Rational(-3, 1)]),
    ("Psi_RA_(antiparticle,k0<0)", Psi_RA, 1, [sp.Rational(-3, 1)]),
    ("Psi_LP_(particle,k0>0)", Psi_LP, -1, [sp.Rational(3, 1)]),
]:
    entry = {}
    for k0v in k0_vals:
        for k3sign in (1, -1):
            resid = check(spinor, mass_sign, k0v, test_lam0, k3sign)
            entry[f"k0={k0v},k3_sign={k3sign}"] = float(resid)
    results[name] = entry

print(json.dumps(results, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-114_mass_perturbed_spinors.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(results, indent=2))
print("wrote", out)
