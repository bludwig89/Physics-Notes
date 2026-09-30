"""
NB-083 (p.64) continued: after deriving g'/g=tan(theta) from requiring A_mu not couple to nu_L
(the T3=+1/2 component), the notebook wants A's coupling to e_L (T3=-1/2) to be e, writing
"g W^3_mu + g' W^0_mu = e A_mu + beta Z_mu" and deriving e=2g sin(theta), beta=(1/2)e(cot(theta)
-tan(theta)) -- flagging a sign issue itself ("the author flips a sign somewhere; both forms are
kept as written").

Reconstruction: page 63's own coupling matrix (i[[g+g',0],[0,-g+g']] -> i[[gW3+g'W0,0],[0,-gW3+
g'W0]]) shows nu_L (T3=+1/2) couples via +gW3+g'W0 while e_L (T3=-1/2) couples via -gW3+g'W0 --
i.e. the e_L equation should have a RELATIVE SIGN FLIP on the g term compared to the nu_L
equation, which page 64's prose does not restate (it reuses "gW3+g'W0" without the flip). This
script checks BOTH readings against the notebook's own claimed e=2g*sin(theta) and beta=(1/2)e
(cot(theta)-tan(theta)) targets, to see which one (if either) is actually self-consistent, and
to pin down precisely where the author's self-flagged sign issue lives.
"""
import sympy as sp
import json, pathlib

theta, g = sp.symbols('theta g', real=True, positive=True)
gp = g * sp.tan(theta)  # from the already-confirmed g'/g = tan(theta) result

# reading 1: literal p.64 text, SAME sign as the nu_L equation (+g W3 + g' W0)
combo1 = g * (sp.cos(theta) - sp.I * 0) * 0  # placeholder, build properly below
W3_expr = lambda Z, A: Z * sp.cos(theta) - A * sp.sin(theta)
W0_expr = lambda Z, A: Z * sp.sin(theta) + A * sp.cos(theta)
Z_s, A_s = sp.symbols('Z A')

combo_reading1 = sp.expand(g * W3_expr(Z_s, A_s) + gp * W0_expr(Z_s, A_s))
e1 = sp.simplify(combo_reading1.coeff(A_s))
beta1 = sp.simplify(combo_reading1.coeff(Z_s))

# reading 2: p.63-consistent, T3=-1/2 sign flip on the g term (-g W3 + g' W0)
combo_reading2 = sp.expand(-g * W3_expr(Z_s, A_s) + gp * W0_expr(Z_s, A_s))
e2 = sp.simplify(combo_reading2.coeff(A_s))
beta2 = sp.simplify(combo_reading2.coeff(Z_s))

e_target = 2 * g * sp.sin(theta)
beta_target = sp.Rational(1, 2) * e_target * (sp.cot(theta) - sp.tan(theta))
beta_target_simplified = sp.simplify(beta_target)

result = {
    "build": "NB-083 (e, beta sign issue)",
    "reading1_(literal_p64_text,_no_sign_flip)": {
        "e": str(e1), "beta": str(beta1),
        "e_matches_target_2g_sin_theta": bool(sp.simplify(e1 - e_target) == 0),
        "beta_matches_target": bool(sp.simplify(beta1 - beta_target_simplified) == 0),
    },
    "reading2_(p63-consistent_T3=-1/2_sign_flip)": {
        "e": str(e2), "beta": str(beta2),
        "e_matches_target_2g_sin_theta": bool(sp.simplify(e2 - e_target) == 0),
        "beta_matches_target": bool(sp.simplify(beta2 - beta_target_simplified) == 0),
    },
    "beta_target_simplified_closed_form": str(beta_target_simplified),
    "conclusion": "Reading 2 (the p.63-consistent T3=-1/2 sign flip on the g-term, NOT the "
                  "literal same-sign reuse of the nu_L combination that p.64's prose text "
                  "writes) is the physically correct one: it reproduces e=2g*sin(theta) "
                  "EXACTLY, matching the notebook's own stated result. But the resulting "
                  "beta = g(1/cos(theta) - 2cos(theta)) is the EXACT NEGATIVE of the notebook's "
                  "own target g(2cos(theta) - 1/cos(theta)) (beta_target_simplified above) -- "
                  "i.e. e checks out exactly and pinpoints reading 2 as the intended setup, "
                  "while beta comes out with the opposite overall sign from what the notebook "
                  "states. This independently confirms and precisely locates the author's own "
                  "self-flagged uncertainty ('the author flips a sign somewhere') -- it is "
                  "specifically in beta, not in e, and the correction is beta -> -beta.",
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-083_e_beta_sign_issue.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
