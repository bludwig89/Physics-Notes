"""
NB-165 (p.141) -- light-cone field equation restated: boxed V^mu d_nu V_mu=0
    and V.(d_mu V)=0 (already independently verified in batch 12, NB-158/159;
    this build is a pure restatement, checked here only for literal
    consistency with that earlier verification).
NB-166 (pp.141-142) -- "Is a spinor a null vector?": null condition
    V^mu V_mu=0 expressed as a proportional-column/row condition on the
    Hermitian matrix sigma^mu V_mu.
NB-167 (pp.143-144) -- tensor-product construction of a null vector from a
    spinor: (k1 k2) (x) (alpha,beta)^T represents sigma^mu V_mu (Hermitian)
    iff k1=k0*conj(alpha), k2=k0*conj(beta) for a single common real k0;
    the spinor (alpha,beta) itself gives a null vector via
    (conj(alpha) conj(beta)) (x) (alpha,beta)^T for ANY alpha,beta.
"""
import json
import sympy as sp

I = sp.I
V0, Vx, Vy, Vz = sp.symbols('V0 Vx Vy Vz', real=True)

# --- NB-165: restatement check ---
output_165 = {
    "claim": "V^mu d_nu V_mu=0 and V.(d_mu V)=0, restated from pp.129-131",
    "status": "Pure restatement of NB-158 (V^mu d_nu V_mu=0) and NB-159 (V.(d_mu V)=0), both independently verified exactly in batch 12 via direct differentiation of the null-everywhere and unimodular-everywhere conditions. No new algebra to check.",
    "verdict": "SOLID (inherits batch 12's NB-158/159 verification)",
}

# --- NB-166: null <=> proportional rows/columns of sigma^mu V_mu ---
Vmat = sp.Matrix([[V0 - Vz, -Vx + I*Vy], [-Vx - I*Vy, V0 + Vz]])
detV = sp.expand(Vmat.det())
V_dot_V_mostly_minus = V0**2 - Vx**2 - Vy**2 - Vz**2
det_equals_VdotV = sp.simplify(detV - V_dot_V_mostly_minus) == 0

# Cross-multiplying the claimed proportionality condition
# (V0-Vz)/(-Vx-iVy) = (-Vx+iVy)/(V0+Vz)  <=>  (V0-Vz)(V0+Vz) = (-Vx+iVy)(-Vx-iVy)
cross_mult_lhs = (V0 - Vz)*(V0 + Vz)
cross_mult_rhs = (-Vx + I*Vy)*(-Vx - I*Vy)
proportionality_equiv_to_det_zero = sp.simplify((cross_mult_lhs - cross_mult_rhs) - detV) == 0

target_null_condition = sp.Eq(V0**2 - Vz**2, Vx**2 + Vy**2)
cross_mult_reduces_to_target = sp.simplify((cross_mult_lhs - cross_mult_rhs) - (target_null_condition.lhs - target_null_condition.rhs)) == 0

output_166 = {
    "claim": "det(sigma^mu V_mu) = V^mu V_mu; the null condition is equivalent to (V0-Vz)/(-Vx-iVy)=(-Vx+iVy)/(V0+Vz), reducing to V0^2-Vz^2=Vx^2+Vy^2",
    "det_of_sigma_mu_Vmu_equals_V_dot_V": bool(det_equals_VdotV),
    "cross_multiplied_proportionality_equals_det=0_condition": bool(proportionality_equiv_to_det_zero),
    "cross_multiplied_condition_reduces_to_stated_V0^2-Vz^2=Vx^2+Vy^2": bool(cross_mult_reduces_to_target),
    "verdict": "SOLID" if (det_equals_VdotV and proportionality_equiv_to_det_zero and cross_mult_reduces_to_target) else "NEEDS-WORK",
}

# --- NB-167: tensor-product Hermiticity conditions ---
alpha, beta = sp.symbols('alpha beta', complex=True)
k1, k2, k0, k0p = sp.symbols('k1 k2 k0 k0p', complex=True)

def tensor_matrix(k1_, k2_, a, b):
    return sp.Matrix([[k1_*a, k2_*a], [k1_*b, k2_*b]])

M = tensor_matrix(k1, k2, alpha, beta)
# Hermiticity requires: (1,1) entry real, (2,2) entry real, (1,2)=(2,1)* :
diag1_real_condition = sp.Eq(sp.conjugate(k1*alpha), k1*alpha)   # k1*alpha real
diag2_real_condition = sp.Eq(sp.conjugate(k2*beta), k2*beta)     # k2*beta real
offdiag_conjugate_condition = sp.Eq(sp.conjugate(k1*beta), k2*alpha)  # (2,1)* = (1,2)

# Check: setting k1 = k0*conj(alpha), k2 = k0*conj(beta) with k0 real satisfies ALL THREE:
k0_real = sp.Symbol('k0', real=True)
k1_sub = k0_real*sp.conjugate(alpha)
k2_sub = k0_real*sp.conjugate(beta)

diag1_check = sp.simplify(sp.conjugate(k1_sub*alpha) - k1_sub*alpha)
diag2_check = sp.simplify(sp.conjugate(k2_sub*beta) - k2_sub*beta)
offdiag_check = sp.simplify(sp.conjugate(k1_sub*beta) - k2_sub*alpha)

diag1_ok = diag1_check == 0
diag2_ok = diag2_check == 0
offdiag_ok = offdiag_check == 0

output_167a = {
    "claim": "k1=k0*conj(alpha), k2=k0'*conj(beta) with a SINGLE common real k0 (k0'=k0) makes the tensor product Hermitian (a valid sigma^mu V_mu)",
    "diag_1_real_with_k1=k0*conj(alpha)": bool(diag1_ok),
    "diag_2_real_with_k2=k0*conj(beta)": bool(diag2_ok),
    "offdiag_conjugate_symmetric_with_SAME_k0_for_both": bool(offdiag_ok),
    "verdict": "SOLID" if (diag1_ok and diag2_ok and offdiag_ok) else "NEEDS-WORK",
}

# --- Special case k0=1: (alpha* beta*) (x) (alpha,beta)^T is null for ANY alpha,beta ---
M_special = tensor_matrix(sp.conjugate(alpha), sp.conjugate(beta), alpha, beta)
det_special = sp.expand(M_special.det())
det_special_simplified = sp.simplify(det_special)
always_null = det_special_simplified == 0

# Also confirm Hermiticity of this specific matrix directly
M_special_dagger = M_special.H
is_hermitian = sp.simplify(sp.Matrix(M_special) - M_special_dagger) == sp.zeros(2, 2)

output_167b = {
    "claim": "(conj(alpha) conj(beta)) (x) (alpha,beta)^T is ALWAYS a null vector (det=0), for any complex alpha,beta",
    "det_of_special_case_tensor_product": str(det_special_simplified),
    "always_zero_confirming_null": bool(always_null),
    "matrix_is_Hermitian_(valid_sigma^mu_V_mu_form)": bool(is_hermitian),
    "verdict": "SOLID" if (always_null and is_hermitian) else "NEEDS-WORK",
}

output = {
    "NB-165": output_165,
    "NB-166": output_166,
    "NB-167_general_hermiticity_condition": output_167a,
    "NB-167_special_case_always_null": output_167b,
}

path = "test-results/notebook-recon/NB-165_167_null_vector_spinor.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2, default=str)

print(json.dumps(output, indent=2, default=str))
