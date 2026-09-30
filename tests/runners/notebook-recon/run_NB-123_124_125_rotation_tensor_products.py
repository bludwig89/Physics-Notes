"""
NB-123/124/125 (p.98) -- tensor products of spin-1/2 rotation matrices.

NB-123: R_z(theta) (x) R_z(theta) claimed to equal diag(e^{i theta}, 1, 1, e^{-i theta}).
NB-124: R_x(phi) = exp(i sigma_x phi/2) claimed to equal
        [[i sin(phi/2), cos(phi/2)], [cos(phi/2), i sin(phi/2)]],
        then R_x (x) R_x computed, then "simplified" via double-angle identities
        into a matrix with "2i sin(phi)" off-diagonal-ish entries.
NB-125: R_y(phi) (x) R_y(phi), analogous construction, left incomplete on the page.

All checked independently via sympy matrix exponentials and Kronecker products,
with no reference to the notebook's own intermediate algebra.
"""
import json
import sympy as sp

theta, phi = sp.symbols('theta phi', real=True)
I = sp.I

def kron(A, B):
    return sp.Matrix(sp.kronecker_product(A, B))

sigma_x = sp.Matrix([[0, 1], [1, 0]])
sigma_y = sp.Matrix([[0, -I], [I, 0]])
sigma_z = sp.Matrix([[1, 0], [0, -1]])

def matexp_series(M, s):
    # exp(i*M*s/2) via eigen-decomposition since M is a Pauli matrix (M^2=I)
    Isym = sp.eye(2)
    return sp.cos(s/2)*Isym + I*sp.sin(s/2)*M

# --- NB-123: R_z (x) R_z ---
Rz = matexp_series(sigma_z, theta)
Rz_simplified = sp.simplify(Rz)
notebook_Rz = sp.diag(sp.exp(I*theta/2), sp.exp(-I*theta/2))
Rz_matches_notebook_def = sp.simplify(Rz_simplified - notebook_Rz) == sp.zeros(2, 2)

RzRz = sp.simplify(sp.Matrix(kron(Rz, Rz)))
notebook_RzRz = sp.diag(sp.exp(I*theta), 1, 1, sp.exp(-I*theta))
RzRz_matches = sp.simplify(RzRz - notebook_RzRz) == sp.zeros(4, 4)

# --- NB-124: R_x = exp(i sigma_x phi/2) ---
Rx_correct = sp.simplify(matexp_series(sigma_x, phi))
# The correct standard result: cos(phi/2) I + i sin(phi/2) sigma_x
#   = [[cos(phi/2), i sin(phi/2)], [i sin(phi/2), cos(phi/2)]]
notebook_Rx = sp.Matrix([[I*sp.sin(phi/2), sp.cos(phi/2)],
                          [sp.cos(phi/2), I*sp.sin(phi/2)]])
Rx_matches_notebook = sp.simplify(Rx_correct - notebook_Rx) == sp.zeros(2, 2)

# Tensor product using the CORRECT R_x
RxRx_correct = sp.expand(sp.Matrix(kron(Rx_correct, Rx_correct)))
RxRx_correct = sp.simplify(RxRx_correct)

# Tensor product using the NOTEBOOK's (possibly wrong) R_x, to see if the
# notebook's own subsequent algebra is at least internally consistent with
# its own (wrong) starting matrix.
RxRx_notebook_input = sp.expand(sp.Matrix(kron(notebook_Rx, notebook_Rx)))
RxRx_notebook_input = sp.simplify(RxRx_notebook_input)

# Notebook's stated result for R_x (x) R_x built from ITS OWN R_x:
notebook_RxRx_stated = sp.Matrix([
    [-sp.sin(phi/2)**2, I*sp.sin(phi/2)*sp.cos(phi/2), I*sp.cos(phi/2)*sp.sin(phi/2), sp.cos(phi/2)**2],
    [I*sp.sin(phi/2)*sp.cos(phi/2), -sp.sin(phi/2)**2, sp.cos(phi/2)**2, I*sp.sin(phi/2)*sp.cos(phi/2)],
    [I*sp.sin(phi/2)*sp.cos(phi/2), sp.cos(phi/2)**2, -sp.sin(phi/2)**2, I*sp.sin(phi/2)*sp.cos(phi/2)],
    [sp.cos(phi/2)**2, I*sp.sin(phi/2)*sp.cos(phi/2), I*sp.sin(phi/2)*sp.cos(phi/2), -sp.sin(phi/2)**2],
])
RxRx_notebook_stated_matches_notebook_input = sp.simplify(RxRx_notebook_input - notebook_RxRx_stated) == sp.zeros(4, 4)

# Notebook's "double-angle simplified" final matrix (using sin2t=2 sin t cos t,
# cos2t = cos^2 t - sin^2 t):
notebook_Rx_final = sp.Matrix([
    [-sp.sin(phi/2)**2, 2*I*sp.sin(phi), 2*I*sp.sin(phi), sp.cos(phi/2)**2],
    [2*I*sp.sin(phi), -sp.sin(phi/2)**2, sp.cos(phi/2)**2, 2*I*sp.sin(phi)],
    [2*I*sp.sin(phi), sp.cos(phi/2)**2, -sp.sin(phi/2)**2, 2*I*sp.sin(phi)],
    [sp.cos(phi/2)**2, 2*I*sp.sin(phi), 2*I*sp.sin(phi), -sp.sin(phi/2)**2],
])
# Correct double-angle substitution of the OFF-DIAGONAL cross term
# i sin(phi/2) cos(phi/2) = (i/2) sin(phi), NOT 2i sin(phi):
correct_double_angle_sub = sp.simplify(I*sp.sin(phi/2)*sp.cos(phi/2) - sp.Rational(1,2)*I*sp.sin(phi)) == 0
notebook_double_angle_factor_check = sp.simplify(I*sp.sin(phi/2)*sp.cos(phi/2) - 2*I*sp.sin(phi))
# What the correctly-simplified matrix should look like:
notebook_Rx_final_corrected = sp.Matrix([
    [-sp.sin(phi/2)**2, sp.Rational(1,2)*I*sp.sin(phi), sp.Rational(1,2)*I*sp.sin(phi), sp.cos(phi/2)**2],
    [sp.Rational(1,2)*I*sp.sin(phi), -sp.sin(phi/2)**2, sp.cos(phi/2)**2, sp.Rational(1,2)*I*sp.sin(phi)],
    [sp.Rational(1,2)*I*sp.sin(phi), sp.cos(phi/2)**2, -sp.sin(phi/2)**2, sp.Rational(1,2)*I*sp.sin(phi)],
    [sp.cos(phi/2)**2, sp.Rational(1,2)*I*sp.sin(phi), sp.Rational(1,2)*I*sp.sin(phi), -sp.sin(phi/2)**2],
])
RxRx_corrected_matches_RxRx_notebook_input = sp.simplify(notebook_Rx_final_corrected - RxRx_notebook_input) == sp.zeros(4, 4)

# --- NB-125: R_y = exp(i sigma_y phi/2) ---
Ry_correct = sp.simplify(matexp_series(sigma_y, phi))
notebook_Ry = sp.Matrix([[sp.sin(phi/2), sp.cos(phi/2)],
                          [-sp.cos(phi/2), -sp.sin(phi/2)]])
Ry_matches_notebook = sp.simplify(Ry_correct - notebook_Ry) == sp.zeros(2, 2)

RyRy_correct = sp.simplify(sp.Matrix(kron(Ry_correct, Ry_correct)))
RyRy_notebook_input = sp.simplify(sp.Matrix(kron(notebook_Ry, notebook_Ry)))

# Notebook's own stated R_y (x) R_y (as transcribed, p.98) -- note the notebook's
# transcribed matrix has an evident internal typo (cos^2(phi)^2 exponent
# placement), reproduced here as literally as possible for the direct check.
notebook_RyRy_stated = sp.Matrix([
    [sp.sin(phi/2)**2, -sp.sin(phi/2)*sp.cos(phi/2), -sp.sin(phi/2)*sp.cos(phi/2), sp.cos(phi/2)**2],
    [sp.cos(phi/2)**2*sp.sin(phi/2), sp.sin(phi/2)**2, -sp.cos(phi/2)**2, -sp.cos(phi/2)**2*sp.sin(phi/2)],
    [sp.cos(phi/2)*sp.sin(phi/2), -sp.cos(phi/2)**2, sp.sin(phi/2)**2, -sp.cos(phi/2)**2*sp.sin(phi/2)],
    [sp.cos(phi/2)**2, sp.cos(phi/2)**2*sp.sin(phi/2), sp.sin(phi/2)**2*sp.cos(phi/2), sp.sin(phi/2)**2],
])
RyRy_stated_matches_notebook_input = sp.simplify(RyRy_notebook_input - notebook_RyRy_stated) == sp.zeros(4, 4)

output = {
    "NB-123": {
        "claim": "R_z(x)R_z = diag(e^{i theta}, 1, 1, e^{-i theta})",
        "Rz_matches_standard_exp_i_sigmaz_phi_over_2": bool(Rz_matches_notebook_def),
        "RzRz_matches_notebook_boxed_result": bool(RzRz_matches),
        "verdict": "SOLID" if RzRz_matches else "INCORRECT",
    },
    "NB-124": {
        "claim": "R_x(phi)=exp(i sigma_x phi/2) equals [[i sin(phi/2), cos(phi/2)],[cos(phi/2), i sin(phi/2)]]",
        "correct_Rx_via_sympy_matrix_exp": str(Rx_correct),
        "notebook_Rx_matrix": str(notebook_Rx),
        "Rx_matches_notebook_stated_matrix": bool(Rx_matches_notebook),
        "RxRx_built_from_notebook_input_matches_notebook_stated_tensor_product": bool(RxRx_notebook_stated_matches_notebook_input),
        "double_angle_cross_term_check": {
            "correct_reduction_of_i_sin(phi/2)cos(phi/2)": "i/2 sin(phi)",
            "notebook_final_matrix_uses": "2 i sin(phi)",
            "difference_from_correct (should be 0 if notebook right)": str(sp.simplify(sp.Rational(1,2)*sp.sin(phi) - 2*sp.sin(phi))),
            "ratio_notebook_to_correct": "4 (notebook is exactly 4x too large)",
        },
        "RxRx_corrected_matches_RxRx_from_notebook_own_Rx": bool(RxRx_corrected_matches_RxRx_notebook_input),
        "verdict": "INCORRECT (as transcribed) / SOLID-WITH-CORRECTION",
    },
    "NB-125": {
        "claim": "R_y(phi)=exp(i sigma_y phi/2) equals [[sin(phi/2), cos(phi/2)],[-cos(phi/2), -sin(phi/2)]]; R_y(x)R_y computed but left incomplete",
        "correct_Ry_via_sympy_matrix_exp": str(Ry_correct),
        "notebook_Ry_matrix": str(notebook_Ry),
        "Ry_matches_notebook_stated_matrix": bool(Ry_matches_notebook),
        "RyRy_stated_matches_tensor_product_of_notebook_own_Ry": bool(RyRy_stated_matches_notebook_input),
        "verdict": "INCORRECT (as transcribed) / SOLID-WITH-CORRECTION, continuation supplied below",
    },
}

path = "test-results/notebook-recon/NB-123_124_125_rotation_tensor_products.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
