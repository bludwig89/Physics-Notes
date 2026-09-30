"""
NB-086 (p.67): mass-term structure mc^2 psibar psi = mc^2(Rbar L + Lbar R), i.e. a Dirac mass
term only ever connects opposite chiralities, same-chirality bilinears vanish identically.

Verified with an explicit 4-component Dirac spinor and Weyl-basis gamma matrices (chiral
projectors P_L=(1-gamma5)/2, P_R=(1+gamma5)/2, gamma5=diag(1,1,-1,-1), gamma^0 off-diagonal
block form consistent with the Weyl basis used throughout this notebook), not just cited.
"""
import sympy as sp
import json, pathlib

g5 = sp.diag(1, 1, -1, -1)
I4 = sp.eye(4)
PL = (I4 - g5) / 2
PR = (I4 + g5) / 2
gamma0 = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])

psi = sp.Matrix(sp.symbols('p1 p2 p3 p4', complex=True))
psiL = PL * psi
psiR = PR * psi
psibar = (psi.H) * gamma0
psibarL = (psiL.H) * gamma0
psibarR = (psiR.H) * gamma0

full = sp.expand((psibar * psi)[0])
split = sp.expand((psibarL * psiR)[0] + (psibarR * psiL)[0])
same_chirality_LL = sp.simplify((psibarL * psiL)[0])
same_chirality_RR = sp.simplify((psibarR * psiR)[0])

result = {
    "build": "NB-086",
    "psibar_psi_minus_(psibarL_psiR+psibarR_psiL)": str(sp.simplify(full - split)),
    "identity_confirmed": bool(sp.simplify(full - split) == 0),
    "same_chirality_LL_bilinear": str(same_chirality_LL),
    "same_chirality_RR_bilinear": str(same_chirality_RR),
    "same_chirality_bilinears_vanish": bool(same_chirality_LL == 0 and same_chirality_RR == 0),
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-086_chiral_mass_identity.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
