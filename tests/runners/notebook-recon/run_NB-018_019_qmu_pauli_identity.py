"""
NB-018/NB-019 (pp.16-17): q^mu, qtilde^mu Pauli-matrix representations, and the core quaternion
identity underlying the whole Sachs formalism: g^{mu nu} = -1/2 (q^mu qtilde^nu + q^nu qtilde^mu)
(boxed at p.23/line 534) should reduce to the flat Minkowski metric diag(1,-1,-1,-1) when
q^mu = sigma^mu (standard flat-space sigma matrices sigma^mu=(I,sx,sy,sz), sigma-tilde^mu =
(I,-sx,-sy,-sz)).

This is the standard sigma-matrix identity underlying all 2-spinor GR (Penrose & Rindler,
Sachs): sigma^mu sigma~^nu + sigma^nu sigma~^mu = 2 eta^{mu nu} I. Checked directly with
explicit 2x2 matrices, all 16 (mu,nu) combinations, not just a schematic argument.

ALSO checks the p.16 line-330 form q_mu qtilde^mu = -4 sigma^0_0 (a same-index, summed-over-mu
statement) against the flat-space sigma matrices, to see whether it is consistent with the
p.23/p.27 boxed forms or is a separate (possibly inconsistent) convention -- flagged either way.
"""
import sympy as sp
import json, pathlib

I2 = sp.eye(2)
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])

sigma = {0: I2, 1: sx, 2: sy, 3: sz}          # sigma^mu = (I, sx, sy, sz)
sigma_tilde = {0: I2, 1: -sx, 2: -sy, 3: -sz}  # sigma~^mu = (I, -sx, -sy, -sz)

eta = {(0, 0): 1, (1, 1): -1, (2, 2): -1, (3, 3): -1}

def eta_val(mu, nu):
    return eta.get((mu, nu), 0)

# --- core identity: sigma^mu sigma~^nu + sigma^nu sigma~^mu = 2 eta^{mu nu} I, for all mu,nu
all_match = True
mismatches = []
for mu in range(4):
    for nu in range(4):
        lhs = sigma[mu] * sigma_tilde[nu] + sigma[nu] * sigma_tilde[mu]
        rhs = 2 * eta_val(mu, nu) * I2
        diff = sp.simplify(lhs - rhs)
        if diff != sp.zeros(2, 2):
            all_match = False
            mismatches.append({"mu": mu, "nu": nu, "lhs": str(lhs), "rhs": str(rhs)})

# --- p.16 line-330 form: q_mu qtilde^mu = -4 sigma^0_0 (interpreted as SUM over mu of
# sigma_mu * sigma~^mu, compared against "-4 sigma^0_0" i.e. -4 times the identity's (0,0) entry
# scaled... this line as transcribed is dimensionally/notationally ambiguous (a matrix identity
# equated to a scalar-looking RHS), so we test the most literal reading: sum_mu sigma_mu sigma~^mu
sum_val = sp.zeros(2, 2)
for mu in range(4):
    sum_val += sigma[mu] * sigma_tilde[mu]
# using eta upper/lower without distinction (flat space, sigma_mu = eta_mu_mu sigma^mu with our
# sigma^mu already using upper convention above -- test both raw sum and eta-weighted sum)
sum_val_lowered = sp.zeros(2, 2)
for mu in range(4):
    sum_val_lowered += eta_val(mu, mu) * sigma[mu] * sigma_tilde[mu]

result = {
    "build": "NB-018/NB-019",
    "core_identity_sigma_sigmatilde_all_16_combos_match_2eta_I": all_match,
    "mismatches": mismatches,
    "p16_line330_sum_sigma_mu_sigmatilde_mu_raw": str(sum_val),
    "p16_line330_sum_sigma_mu_sigmatilde_mu_eta_lowered": str(sum_val_lowered),
    "p16_claim_neg4_sigma00_as_matrix": str(-4 * I2),
    "p16_raw_sum_matches_neg4I": bool(sp.simplify(sum_val - (-4 * I2)) == sp.zeros(2, 2)),
    "p16_eta_lowered_sum_matches_neg4I": bool(sp.simplify(sum_val_lowered - (-4 * I2)) == sp.zeros(2, 2)),
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-018_019_qmu_pauli_identity.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
