"""
NB-084 (pp.65-66): TWO different mass-term derivations in the notebook, giving TWO different
Z-mass formulas, with the tension between them left unresolved on the page:

(A) p.65: treat W^3, W^0 as having INDEPENDENT given masses m_W, m_{W0} (a general mass matrix
    (1/2)m_W^2 W3^2 + (1/2)m_{W0}^2 W0^2), rotate to (Z,A) basis, and read off
        m_Z^2 = m_W^2 cos^2(theta) + m_{W0}^2 sin^2(theta)
        m_A^2 = m_W^2 sin^2(theta) + m_{W0}^2 cos^2(theta)
    PLUS an unwanted "anomalous" Z-A cross term the notebook flags as unresolved.

(B) p.66: assume ONLY a Z-mass term exists in the first place ((1/2)m_Z^2 Z_mu^2, with the
    photon A exactly massless a priori), expand IN the W3,W0 basis, and match the W3^2
    coefficient to DEFINE m_W^2 := m_Z^2 cos^2(theta), giving the standard electroweak relation
        m_Z^2 = m_W^2 / cos^2(theta).

This script verifies BOTH expansions algebraically (sympy) and explains, precisely, why they
give different answers: they are not competing derivations of the same physics, they start from
DIFFERENT physical assumptions. (A) posits two independently-massive gauge bosons with no reason
for the photon to end up massless (hence the leftover anomalous cross term -- a real problem,
correctly flagged by the author). (B) is exactly the standard Higgs-mechanism structure, where
the SSB mass matrix in the (W3,B) basis has EXACTLY one massless and one massive eigenvalue BY
CONSTRUCTION (not an independent postulate) -- which is precisely why (B) reproduces the
standard relation and (A) does not.
"""
import sympy as sp
import json, pathlib

theta, mW, mW0, mZ = sp.symbols('theta m_W m_{W0} m_Z', positive=True)
Z, A = sp.symbols('Z A')

W3 = Z * sp.cos(theta) - A * sp.sin(theta)
W0 = Z * sp.sin(theta) + A * sp.cos(theta)

# --- (A) p.65: independent m_W, m_{W0}
L_A = sp.expand(sp.Rational(1, 2) * mW**2 * W3**2 + sp.Rational(1, 2) * mW0**2 * W0**2)
mZ2_from_A = sp.simplify(L_A.coeff(Z, 2) * 2)          # coefficient of (1/2)Z^2
mA2_from_A = sp.simplify(L_A.coeff(A, 2) * 2)
cross_term_ZA = sp.simplify(L_A.coeff(Z, 1).coeff(A, 1))

mZ2_matches_notebook_A = sp.simplify(mZ2_from_A - (mW**2 * sp.cos(theta)**2 + mW0**2 * sp.sin(theta)**2)) == 0
mA2_matches_notebook_A = sp.simplify(mA2_from_A - (mW**2 * sp.sin(theta)**2 + mW0**2 * sp.cos(theta)**2)) == 0
cross_term_is_nonzero_generically = cross_term_ZA != 0  # confirms the "anomalous term" is real, not a notebook mistake

# --- (B) p.66: pure Z-mass term expanded in the W3,W0 basis, define m_W^2 by matching
L_B = sp.expand(sp.Rational(1, 2) * mZ**2 * Z**2)
# re-express Z in terms of W3, W0: Z = W3 cos(theta) + W0 sin(theta) (the notebook's inverse relation)
W3s, W0s = sp.symbols('W3 W0')
Z_in_W = W3s * sp.cos(theta) + W0s * sp.sin(theta)
L_B_in_W = sp.expand(sp.Rational(1, 2) * mZ**2 * Z_in_W**2)
W3sq_coeff = sp.simplify(L_B_in_W.coeff(W3s, 2) * 2)  # should be m_Z^2 cos^2(theta)

# defining m_W^2 := this coefficient, solve for m_Z^2
mW2_defined = W3sq_coeff
solved_mZ2 = sp.solve(sp.Eq(sp.Symbol('m_W_sq'), mW2_defined), mZ**2)
mZ2_result = sp.simplify(solved_mZ2[0]) if solved_mZ2 else None
matches_standard_SM_relation = sp.simplify(mZ2_result - sp.Symbol('m_W_sq') / sp.cos(theta)**2) == 0 if mZ2_result is not None else False

result = {
    "build": "NB-084",
    "reading_A_(p65,_independent_masses)": {
        "m_Z^2": str(mZ2_from_A),
        "matches_notebook": bool(mZ2_matches_notebook_A),
        "m_A^2": str(mA2_from_A),
        "matches_notebook": bool(mA2_matches_notebook_A),
        "Z-A_cross_term_coefficient": str(cross_term_ZA),
        "cross_term_is_genuinely_nonzero_(confirms_the_flagged_'anomalous_term'_is_real)": bool(cross_term_is_nonzero_generically),
    },
    "reading_B_(p66,_pure_Z-mass,_photon_massless_a_priori)": {
        "W3^2_coefficient_in_(1/2)m_Z^2_Z^2_expanded_in_W_basis": str(W3sq_coeff),
        "solving_m_W^2:=this_coefficient_for_m_Z^2": str(mZ2_result),
        "matches_standard_SM_relation_m_Z^2=m_W^2/cos^2(theta)": bool(matches_standard_SM_relation),
    },
    "conclusion": "Both expansions are algebraically correct on their own terms -- they are not "
                  "competing derivations of the same physics, they encode different physical "
                  "assumptions. (A) treats W3,W0 as independently massive with no built-in "
                  "reason for the photon to stay massless, and DOES produce a genuine leftover "
                  "Z-A mixing mass term (confirmed nonzero here, not a notebook slip -- this is "
                  "a real feature of assumption (A), correctly flagged by the author as "
                  "unresolved). (B) assumes the photon is massless FROM THE START (as required "
                  "by unbroken electromagnetism) and asks what W3-coefficient a pure Z-mass term "
                  "implies -- this reproduces the standard m_Z^2=m_W^2/cos^2(theta) relation "
                  "exactly, because it is structurally the same constraint the Higgs mechanism "
                  "enforces automatically (exactly one massless, one massive eigenvalue in the "
                  "W3-B mass matrix, by construction of the Higgs coupling, not by postulate).",
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-084_mass_matrix_comparison.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
