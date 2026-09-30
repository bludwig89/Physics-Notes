"""
NB-126/127 (p.99-100) -- explicit 3x3 spin-1 matrices, Pauli tensor products,
and the basis transformation block-diagonalizing "sigma(x)sigma... into S".

NB-126: S_x, S_y, S_z (3x3, standard real Cartesian L=1 generators) and
        sigma_x(x)sigma_x, sigma_y(x)sigma_y, sigma_z(x)sigma_z (4x4, verbatim
        Pauli tensor products).
NB-127: a 3x3 real orthogonal matrix A claimed to "turn sigma_z(x)sigma_z etc.
        into (0 . ; . S_x)" (spin-1 (+) spin-0 block form); new-basis
        S_x, S_y, S_z given explicitly for the resulting 3x3 block.

This script checks BOTH the literal reading of the notebook's own words
(transform the raw tensor PRODUCTS sigma_i(x)sigma_i) and the physically
standard Clebsch-Gordan construction (transform the SUM/total-spin operators
S_i = (sigma_i(x)I + I(x)sigma_i)/2, i.e. angular-momentum ADDITION,
1/2 (x) 1/2 = 1 (+) 0), to see which one actually reproduces the notebook's
stated new-basis S_x, S_y, S_z -- and checks the notebook's own stated
matrices for internal self-consistency (do they satisfy their own su(2)
algebra?) independent of either derivation.
"""
import json
import sympy as sp

I = sp.I

def kron(A, B):
    return sp.Matrix(sp.kronecker_product(A, B))

# --- NB-126: stated real-Cartesian spin-1 matrices and Pauli tensor products ---
Sx = sp.Matrix([[0, 0, 0], [0, 0, -I], [0, I, 0]])
Sy = sp.Matrix([[0, 0, I], [0, 0, 0], [-I, 0, 0]])
Sz = sp.Matrix([[0, -I, 0], [I, 0, 0], [0, 0, 0]])

comm_xy = Sx*Sy - Sy*Sx
comm_yz = Sy*Sz - Sz*Sy
comm_zx = Sz*Sx - Sx*Sz
su2_algebra_ok = (
    sp.simplify(comm_xy - I*Sz) == sp.zeros(3, 3) and
    sp.simplify(comm_yz - I*Sx) == sp.zeros(3, 3) and
    sp.simplify(comm_zx - I*Sy) == sp.zeros(3, 3)
)
casimir = sp.simplify(Sx*Sx + Sy*Sy + Sz*Sz)
casimir_ok = casimir == 2*sp.eye(3)

sigma_x = sp.Matrix([[0, 1], [1, 0]])
sigma_y = sp.Matrix([[0, -I], [I, 0]])
sigma_z = sp.Matrix([[1, 0], [0, -1]])
Id2 = sp.eye(2)

sxsx = kron(sigma_x, sigma_x)
sysy = kron(sigma_y, sigma_y)
szsz = kron(sigma_z, sigma_z)

notebook_sxsx = sp.Matrix([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]])
notebook_sysy = sp.Matrix([[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]])
notebook_szsz = sp.Matrix([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]])

sxsx_ok = sxsx == notebook_sxsx
sysy_ok = sysy == notebook_sysy
szsz_ok = szsz == notebook_szsz

# --- NB-127: literal reading -- transform the raw tensor PRODUCTS ---
sqrt2 = sp.sqrt(2)
# Standard Clebsch-Gordan basis change, rows = (|1,1>,|1,0>,|1,-1>,|0,0>),
# columns = (|++>,|+->,|-+>,|-->):
U = sp.Matrix([
    [1, 0, 0, 0],
    [0, 1/sqrt2, 1/sqrt2, 0],
    [0, 0, 0, 1],
    [0, 1/sqrt2, -1/sqrt2, 0],
])
U_unitary = sp.simplify(U*U.T - sp.eye(4)) == sp.zeros(4, 4)

szsz_new = sp.simplify(U * szsz * U.T)
literal_product_reading_gives_diag_1_0_neg1 = sp.simplify(
    szsz_new[0:3, 0:3] - sp.diag(1, 0, -1)
) == sp.zeros(3, 3)

# --- NB-127: standard construction -- transform the SUM (total spin) ---
Sz_tot = (kron(sigma_z, Id2) + kron(Id2, sigma_z)) / 2
Sx_tot = (kron(sigma_x, Id2) + kron(Id2, sigma_x)) / 2
Sy_tot = (kron(sigma_y, Id2) + kron(Id2, sigma_y)) / 2

Sz_tot_new = sp.simplify(U * Sz_tot * U.T)
Sx_tot_new = sp.simplify(U * Sx_tot * U.T)
Sy_tot_new = sp.simplify(U * Sy_tot * U.T)

triplet_Sz = Sz_tot_new[0:3, 0:3]
triplet_Sx = Sx_tot_new[0:3, 0:3]
triplet_Sy = Sy_tot_new[0:3, 0:3]

notebook_new_Sx = sp.Matrix([[0,1,0],[1,0,1],[0,1,0]])
notebook_new_Sy = sp.Matrix([[0,-I,0],[I,0,-I],[0,I,0]])
notebook_new_Sz = sp.diag(1, 0, -1)

triplet_Sz_matches_notebook_exactly = sp.simplify(triplet_Sz - notebook_new_Sz) == sp.zeros(3, 3)
triplet_Sx_matches_notebook_up_to_sqrt2 = sp.simplify(triplet_Sx*sqrt2 - notebook_new_Sx) == sp.zeros(3, 3)
triplet_Sy_matches_notebook_up_to_sqrt2 = sp.simplify(triplet_Sy*sqrt2 - notebook_new_Sy) == sp.zeros(3, 3)

# --- Internal self-consistency check of the notebook's OWN stated triple,
# independent of either derivation route: does [Sx,Sy]=i Sz hold, and is
# S^2 proportional to the identity, using its own literal numbers? ---
comm_nb = sp.simplify(notebook_new_Sx*notebook_new_Sy - notebook_new_Sy*notebook_new_Sx)
notebook_own_triple_satisfies_own_algebra = sp.simplify(comm_nb - I*notebook_new_Sz) == sp.zeros(3, 3)
casimir_nb = sp.simplify(notebook_new_Sx**2 + notebook_new_Sy**2 + notebook_new_Sz**2)
casimir_nb_is_scalar = casimir_nb[0,0] == casimir_nb[1,1] == casimir_nb[2,2] and casimir_nb.is_diagonal()

# The corrected triple (each of Sx,Sy divided by sqrt2) should restore both:
Sx_corr = notebook_new_Sx/sqrt2
Sy_corr = notebook_new_Sy/sqrt2
comm_corr = sp.simplify(Sx_corr*Sy_corr - Sy_corr*Sx_corr)
corrected_satisfies_algebra = sp.simplify(comm_corr - I*notebook_new_Sz) == sp.zeros(3, 3)
casimir_corr = sp.simplify(Sx_corr**2 + Sy_corr**2 + notebook_new_Sz**2)
corrected_casimir_is_2I = casimir_corr == 2*sp.eye(3)

# The notebook's own stated 3x3 A transform, checked for orthogonality:
A = sp.Matrix([
    [1/sqrt2, 0, 1/sqrt2],
    [0, 1, 0],
    [1/sqrt2, 0, -1/sqrt2],
])
A_orthogonal = sp.simplify(A*A.T - sp.eye(3)) == sp.zeros(3, 3)
# A matches the (|1,1>,|1,0>,|1,-1>)-vs-(|++>, symmetrized-middle, |-->)
# block of U, once the 4-dim middle pair (|+->,|-+>) is pre-symmetrized into
# a single reduced basis vector (the natural reading of the page's own
# 3-vs-4-dimensional bookkeeping):
U_reduced_block = sp.Matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])  # trivial once the symmetric combination is *already* the input basis
# i.e. A is not literally a sub-block of U -- it is a SEPARATE, self-standing
# orthogonal transform. Report that distinction plainly rather than force a
# match that isn't structurally there.

output = {
    "NB-126": {
        "Sx_Sy_Sz_satisfy_su2_algebra": bool(su2_algebra_ok),
        "Sx_Sy_Sz_casimir_equals_2_identity": bool(casimir_ok),
        "sigma_x_tensor_sigma_x_matches_notebook": bool(sxsx_ok),
        "sigma_y_tensor_sigma_y_matches_notebook": bool(sysy_ok),
        "sigma_z_tensor_sigma_z_matches_notebook": bool(szsz_ok),
        "verdict": "SOLID" if (su2_algebra_ok and casimir_ok and sxsx_ok and sysy_ok and szsz_ok) else "NEEDS-WORK",
    },
    "NB-127": {
        "literal_reading_transform_the_PRODUCT_sigma_i_tensor_sigma_i": {
            "U_is_unitary": bool(U_unitary),
            "does_szsz_block_diagonalize_to_diag(1,0,-1)": bool(literal_product_reading_gives_diag_1_0_neg1),
            "finding": "FALSE -- the raw tensor PRODUCT sigma_z(x)sigma_z block-diagonalizes to a DIFFERENT matrix (eigenvalues +-1 on both triplet and singlet, unrelated to the S_z=1,0,-1 pattern), confirmed by direct computation. The literal phrase 'turn sigma_z(x)sigma_z... into S_x' does not hold for the product operator.",
        },
        "standard_construction_transform_the_SUM_total_spin_S=(sigma1+sigma2)/2": {
            "triplet_Sz_matches_notebook_new_Sz_exactly": bool(triplet_Sz_matches_notebook_exactly),
            "triplet_Sx_matches_notebook_new_Sx_up_to_missing_1_over_sqrt2_factor": bool(triplet_Sx_matches_notebook_up_to_sqrt2),
            "triplet_Sy_matches_notebook_new_Sy_up_to_missing_1_over_sqrt2_factor": bool(triplet_Sy_matches_notebook_up_to_sqrt2),
            "finding": "The physically correct Clebsch-Gordan addition of two spin-1/2's, S_total = (sigma_1+sigma_2)/2 (SUM, not tensor product), exactly reproduces the notebook's stated new-basis S_z=diag(1,0,-1), and reproduces S_x, S_y up to a missing overall 1/sqrt(2) normalization factor.",
        },
        "internal_self_consistency_of_notebooks_own_stated_triple": {
            "as_stated_satisfies_own_su2_algebra_[Sx,Sy]=i*Sz": bool(notebook_own_triple_satisfies_own_algebra),
            "as_stated_casimir_diagonal_entries": [int(casimir_nb[0,0]), int(casimir_nb[1,1]), int(casimir_nb[2,2])],
            "as_stated_casimir_is_scalar_multiple_of_identity": bool(casimir_nb_is_scalar),
            "after_dividing_Sx_Sy_by_sqrt2_satisfies_algebra": bool(corrected_satisfies_algebra),
            "after_correction_casimir_equals_2_identity": bool(corrected_casimir_is_2I),
        },
        "A_matrix_orthogonality": bool(A_orthogonal),
        "conclusion": (
            "NB-127 contains a genuine, self-detectable error: the new-basis "
            "S_x, S_y matrices exactly as written do NOT satisfy their own "
            "su(2) commutation algebra (comm gives 2i*Sz, not i*Sz) and their "
            "Casimir is not a scalar multiple of the identity (diag entries "
            "3,4,3, not 2,2,2) -- an internal inconsistency detectable "
            "without reference to any external derivation. Dividing S_x and "
            "S_y each by sqrt(2) fixes BOTH defects exactly and simultaneously "
            "matches the physically correct Clebsch-Gordan total-spin "
            "construction. Separately, the page's own PROSE ('turn "
            "sigma_z(x)sigma_z... into S_x') is imprecise: block-diagonalizing "
            "the literal tensor PRODUCT operators does not give the spin-1 "
            "generators at all; only the SUM (total spin) does. The stated "
            "S_z=diag(1,0,-1), taken alone, is exactly correct with no "
            "correction needed."
        ),
        "verdict": "SOLID-WITH-CORRECTION",
    },
}

path = "test-results/notebook-recon/NB-126_127_spin1_clebsch_gordan.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
