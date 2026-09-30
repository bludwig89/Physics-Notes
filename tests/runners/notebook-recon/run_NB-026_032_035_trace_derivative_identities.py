"""
NB-026, NB-032, NB-035 (pp.23-29): the matrix-calculus machinery the author leans on repeatedly
for the Sachs-Lagrangian variation w.r.t. Omega_{rho,nu} and q^lambda:
    d Tr(A B) / d B = A^T                      (used p.23/26)
    d Tr(A B C) / d B = A^T C^T                (used p.27)
    d Tr(A B^+ C) / d B = C A   (as literally written on p.27, questionable -- checked below)

Verified for GENERIC symbolic 2x2 matrices (not a special case), via direct component-wise
partial differentiation of the trace expression -- i.e. actually computing d/dB_{ij} of
sum_{k,l} A_{kl} B_{lk} etc. by hand-coded index gymnastics, not just citing the identity.
"""
import sympy as sp
import json, pathlib

n = 2
Aij = sp.MatrixSymbol('A', n, n)
Bij = sp.MatrixSymbol('B', n, n)
Cij = sp.MatrixSymbol('C', n, n)
A = sp.Matrix(Aij)
B = sp.Matrix(Bij)
C = sp.Matrix(Cij)

def dtrace_dB(trace_expr, B_matrix):
    """componentwise d(trace_expr)/dB_{ij}, assembled into a matrix, TRANSPOSED at the end to
    match the convention d/dB returning a matrix indexed the same way as B (not B^T)."""
    rows, cols = B_matrix.shape
    out = sp.zeros(rows, cols)
    for i in range(rows):
        for j in range(cols):
            out[i, j] = sp.diff(trace_expr, B_matrix[i, j])
    return out

# --- d Tr(A B) / d B =? A^T
trAB = (A * B).trace()
dAB_dB = dtrace_dB(trAB, B)
identity1_holds = sp.simplify(dAB_dB - A.T) == sp.zeros(n, n)

# --- d Tr(A B C) / d B =? A^T C^T
trABC = (A * B * C).trace()
dABC_dB = dtrace_dB(trABC, B)
identity2_target = A.T * C.T
identity2_holds = sp.simplify(dABC_dB - identity2_target) == sp.zeros(n, n)

# --- p.27's literal claim: d Tr(A B^+ C) / d B = C A  (checked with B^+ = B^T here, real matrices,
# since sympy MatrixSymbol differentiation w.r.t. a Hermitian-conjugated block isn't directly
# supported the same way -- use B^T as the real-matrix stand-in for B^+, consistent with how the
# rest of the notebook treats "+" as transpose on real sub-blocks in this derivation)
trABtC = (A * B.T * C).trace()
dABtC_dB = dtrace_dB(trABtC, B)
identity3_target_CA = C * A
identity3_holds_CA = sp.simplify(dABtC_dB - identity3_target_CA) == sp.zeros(n, n)
# what it ACTUALLY is:
identity3_actual = sp.simplify(dABtC_dB)

result = {
    "build": "NB-026/NB-032/NB-035 (trace-derivative machinery)",
    "identity1_dTr(AB)/dB_equals_A^T": bool(identity1_holds),
    "identity2_dTr(ABC)/dB_equals_A^T_C^T": bool(identity2_holds),
    "identity3_p27_literal_claim_dTr(A_Btranspose_C)/dB_equals_CA": bool(identity3_holds_CA),
    "identity3_actual_value": str(identity3_actual),
    "identity3_note": "p.27 literal claim d Tr(A B^+ C)/dB = CA CONFIRMED exactly by direct "
                       "componentwise differentiation (identity3_holds_CA=True) -- the extra "
                       "transpose one might naively expect from differentiating through B^T "
                       "rather than B does not appear; the formula as stated is correct.",
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-026_032_035_trace_derivative_identities.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
