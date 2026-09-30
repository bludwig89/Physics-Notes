"""
NB-130-134 (pp.103-104) -- neutral-charge operator Q' = t3 cot(theta_W) - t0 tan(theta_W),
evaluated at the experimental sin^2(theta_W), then explored at two HYPOTHETICAL values
(sin(theta_W)=1/2, and sin(theta_W)=sqrt(2)/3 <=> sin^2(theta_W)=2/9, arising from demanding
the charged-current coupling be exactly "3e"). NB-134 ends with the author's own self-flagged
inconsistency ("x") in a follow-up algebra check.

All numbers recomputed independently from the notebook's own STARTING assumptions (never from
its intermediate numeric results), using sympy for exact symbolic values and float evaluation
for the decimals actually printed on the page.
"""
import json
import sympy as sp

# --- NB-130: experimental sin^2(theta_W) = 0.232 ---
sin2_exp = sp.Rational(232, 1000)
sin_exp = sp.sqrt(sin2_exp)
cos2_exp = 1 - sin2_exp
cos_exp = sp.sqrt(cos2_exp)
cot_exp = cos_exp / sin_exp
tan_exp = sin_exp / cos_exp

sin_exp_f, cos_exp_f, cot_exp_f, tan_exp_f = [float(x) for x in (sin_exp, cos_exp, cot_exp, tan_exp)]
Qp_11 = cot_exp_f + tan_exp_f
Qp_22 = -cot_exp_f + tan_exp_f

nb130_notebook_values = {
    "sin_theta_W": 0.481, "cos_theta_W": 0.876, "cot_theta_W": 1.821, "tan_theta_W": 0.549,
    "Q'_11": 2.37, "Q'_22": -1.27,
}
nb130_derived = {
    "sin_theta_W": round(sin_exp_f, 3), "cos_theta_W": round(cos_exp_f, 3),
    "cot_theta_W": round(cot_exp_f, 3), "tan_theta_W": round(tan_exp_f, 3),
    "Q'_11": round(Qp_11, 2), "Q'_22": round(Qp_22, 2),
}
nb130_match = all(
    abs(nb130_notebook_values[k] - nb130_derived[k]) < 0.006
    for k in nb130_notebook_values
)

# --- NB-131: hypothetical sin(theta_W) = 1/2 ---
sin_half = sp.Rational(1, 2)
cos_half = sp.sqrt(1 - sin_half**2)
cot_half = sp.simplify(cos_half / sin_half)
tan_half = sp.simplify(sin_half / cos_half)
nb131_check = {
    "cos_theta_W_equals_sqrt3_over_2": sp.simplify(cos_half - sp.sqrt(3)/2) == 0,
    "cot_theta_W_equals_sqrt3": sp.simplify(cot_half - sp.sqrt(3)) == 0,
    "tan_theta_W_equals_1_over_sqrt3": sp.simplify(tan_half - 1/sp.sqrt(3)) == 0,
}

# --- NB-132: tau_+/-, V_+/-, coupling identity g W1 tau1 + g W2 tau2 = g(W- tau+ + W+ tau-) ---
I = sp.I
tau1 = sp.Matrix([[0, 1], [1, 0]])
tau2 = sp.Matrix([[0, -I], [I, 0]])
sqrt2 = sp.sqrt(2)
tau_plus = sp.simplify((tau1 + I*tau2) / sqrt2)
tau_minus = sp.simplify((tau1 - I*tau2) / sqrt2)
notebook_tau_plus = sp.Matrix([[0, sqrt2], [0, 0]])
notebook_tau_minus = sp.Matrix([[0, 0], [sqrt2, 0]])
tau_plus_ok = tau_plus == notebook_tau_plus
tau_minus_ok = tau_minus == notebook_tau_minus

W1, W2, g = sp.symbols('W1 W2 g', real=True)
Wp = (W1 + I*W2) / sqrt2  # V_+ in notebook notation
Wm = (W1 - I*W2) / sqrt2  # V_-
lhs = sp.simplify(g*W1*tau1 + g*W2*tau2)
rhs = sp.simplify(g*(Wm*tau_plus + Wp*tau_minus))
identity_holds = sp.simplify(lhs - rhs) == sp.zeros(2, 2)

modulus_identity = sp.simplify(sp.Abs(Wp)**2 + sp.Abs(Wm)**2 - (W1**2 + W2**2))
# Abs() on symbolic complex combos needs conjugate substitution; redo with explicit assumption W1,W2 real
Wp_mag2 = sp.simplify((W1 + I*W2)*(W1 - I*W2) / 2)
Wm_mag2 = sp.simplify((W1 - I*W2)*(W1 + I*W2) / 2)
modulus_identity_ok = sp.simplify(Wp_mag2 + Wm_mag2 - (W1**2 + W2**2)) == 0

# coupling ~ sqrt(2) g ~ sqrt(2)/sin(theta_W) * e, given e = g sin(theta_W)
e_sym, sinw = sp.symbols('e sinw', positive=True)
g_from_e = e_sym / sinw
coupling_expr = sp.simplify(sqrt2 * g_from_e)
coupling_matches_notebook_form = sp.simplify(coupling_expr - sqrt2*e_sym/sinw) == 0

# --- NB-133: hypothetical coupling to W^+- = 3e exactly ---
eq_sin = sp.Eq(sqrt2 / sp.Symbol('sinw2', positive=True), 3)
sinw_from_3e = sp.solve(eq_sin, sp.Symbol('sinw2', positive=True))[0]
sin2_from_3e = sp.simplify(sinw_from_3e**2)
nb133_check = {
    "sin_theta_W_from_coupling=3e": str(sinw_from_3e),
    "sin_theta_W_equals_sqrt2_over_3": sp.simplify(sinw_from_3e - sqrt2/3) == 0,
    "sin2_theta_W_equals_2_over_9": sp.simplify(sin2_from_3e - sp.Rational(2, 9)) == 0,
    "sin2_theta_W_decimal": float(sin2_from_3e),
}

# --- NB-134: sin^2(theta_W)=2/9 -- cot, tan, Q_z, and the self-flagged "other algebra" check ---
sin2_29 = sp.Rational(2, 9)
sin_29 = sp.sqrt(sin2_29)
cos2_29 = 1 - sin2_29
cos_29 = sp.sqrt(cos2_29)
cot_29 = sp.simplify(cos_29 / sin_29)
tan_29 = sp.simplify(sin_29 / cos_29)

nb134_notebook_symbolic = {
    "sin_theta_W": sp.sqrt(2)/3,
    "tan_theta_W_as_stated": sp.sqrt(sp.Rational(1, 7)),   # notebook's own printed radical
    "cot_theta_W_as_stated": sp.sqrt(sp.Rational(7, 2)),
}
tan_matches_stated_1_over_7 = sp.simplify(tan_29 - nb134_notebook_symbolic["tan_theta_W_as_stated"]) == 0
tan_matches_2_over_7 = sp.simplify(tan_29 - sp.sqrt(sp.Rational(2, 7))) == 0
cot_matches_stated = sp.simplify(cot_29 - nb134_notebook_symbolic["cot_theta_W_as_stated"]) == 0

Qz_11_exact = sp.simplify(cot_29 + tan_29)
Qz_22_exact = sp.simplify(cot_29 - tan_29)
Qz_11_f = float(Qz_11_exact)
Qz_22_f = float(Qz_22_exact)

notebook_Qz_11_symbolic = 2*sp.sqrt(7)/3
notebook_Qz_22_symbolic = 1/sp.sqrt(3)
Qz_11_matches_stated_symbolic = sp.simplify(Qz_11_exact - notebook_Qz_11_symbolic) == 0
Qz_22_matches_stated_symbolic = sp.simplify(Qz_22_exact - notebook_Qz_22_symbolic) == 0

notebook_Qz_11_decimal = 2.37
notebook_Qz_22_decimal = 1.33
Qz_11_decimal_matches = abs(Qz_11_f - notebook_Qz_11_decimal) < 0.01
Qz_22_decimal_matches = abs(Qz_22_f - notebook_Qz_22_decimal) < 0.01

# Is the boxed decimal 2.37 actually just NB-130's experimental Q'_11 value, copied over?
Qz_11_equals_nb130_Qp_11 = abs(notebook_Qz_11_decimal - Qp_11) < 0.005

# The "other algebra" self-consistency check: cot+tan=7/3, cot-tan=4/3 => cot=11/6;
# does 11/6 + 6/11 actually equal 7/3?
lhs_other = sp.Rational(11, 6) + sp.Rational(6, 11)
rhs_other = sp.Rational(7, 3)
other_algebra_consistent = lhs_other == rhs_other
other_algebra_exact_value = lhs_other

# What is the TRUE cot(theta_W) at sin^2=2/9, and does it equal 11/6?
cot_29_f = float(cot_29)
cot_equals_11_over_6 = sp.simplify(cot_29 - sp.Rational(11, 6)) == 0

output = {
    "NB-130": {
        "notebook_values": nb130_notebook_values,
        "derived_values": nb130_derived,
        "all_match_within_rounding": bool(nb130_match),
        "verdict": "SOLID" if nb130_match else "NEEDS-WORK",
    },
    "NB-131": {
        "checks": {k: bool(v) for k, v in nb131_check.items()},
        "verdict": "SOLID" if all(nb131_check.values()) else "NEEDS-WORK",
    },
    "NB-132": {
        "tau_plus_matches_notebook": bool(tau_plus_ok),
        "tau_minus_matches_notebook": bool(tau_minus_ok),
        "identity_gW1tau1+gW2tau2=g(W-tau++W+tau-)_holds": bool(identity_holds),
        "modulus_identity_|W+|^2+|W-|^2=|W1|^2+|W2|^2_holds": bool(modulus_identity_ok),
        "coupling_scaling_sqrt2_g_=_sqrt2_e/sinw_consistent": bool(coupling_matches_notebook_form),
        "verdict": "SOLID" if all([tau_plus_ok, tau_minus_ok, identity_holds, modulus_identity_ok]) else "NEEDS-WORK",
    },
    "NB-133": {
        "checks": nb133_check,
        "verdict": "SOLID" if (nb133_check["sin_theta_W_equals_sqrt2_over_3"] and nb133_check["sin2_theta_W_equals_2_over_9"]) else "NEEDS-WORK",
    },
    "NB-134": {
        "tan_theta_W_matches_notebooks_stated_sqrt(1/7)": bool(tan_matches_stated_1_over_7),
        "tan_theta_W_actually_equals_sqrt(2/7)": bool(tan_matches_2_over_7),
        "tan_theta_W_numeric_(both_should_match_decimal_0.535)": float(tan_29),
        "cot_theta_W_matches_notebooks_stated_sqrt(7/2)": bool(cot_matches_stated),
        "Qz_11_exact_symbolic": str(Qz_11_exact),
        "Qz_11_matches_notebooks_stated_symbolic_2sqrt7/3": bool(Qz_11_matches_stated_symbolic),
        "Qz_11_decimal_true_value": round(Qz_11_f, 4),
        "Qz_11_notebook_stated_decimal": notebook_Qz_11_decimal,
        "Qz_11_decimal_matches_within_0.01": bool(Qz_11_decimal_matches),
        "Qz_11_notebook_decimal_actually_equals_NB-130s_experimental_Qp_11": bool(Qz_11_equals_nb130_Qp_11),
        "Qz_22_exact_symbolic": str(Qz_22_exact),
        "Qz_22_matches_notebooks_stated_symbolic_1/sqrt3": bool(Qz_22_matches_stated_symbolic),
        "Qz_22_decimal_true_value": round(Qz_22_f, 4),
        "Qz_22_notebook_stated_decimal": notebook_Qz_22_decimal,
        "Qz_22_decimal_matches_within_0.01": bool(Qz_22_decimal_matches),
        "other_algebra_self_check": {
            "notebook_used_cot+tan=7/3_and_cot-tan=4/3": True,
            "these_rounded_fractions_solve_to_cot=11/6": True,
            "does_11/6+6/11_actually_equal_7/3": bool(other_algebra_consistent),
            "11/6+6/11_exact_value": str(other_algebra_exact_value),
            "true_cot_theta_W_at_sin2=2/9": str(cot_29),
            "true_cot_theta_W_decimal": round(cot_29_f, 4),
            "true_cot_equals_11/6": bool(cot_equals_11_over_6),
            "author_self_flagged_with_an_X_mark": True,
            "confirmed_genuine_inconsistency": not bool(other_algebra_consistent),
        },
        "conclusion": (
            "Two separate, precisely-locatable errors, both confirmed genuine (not "
            "transcription artifacts): (1) the printed radical for tan(theta_W), "
            "sqrt(1/7)=0.378, does not match its own accompanying decimal "
            "'~0.535' -- the correct closed form is sqrt(2/7)=0.5345, matching the "
            "decimal exactly; the '1/7' should be '2/7'. (2) The boxed Q_z decimal "
            "2.37 for cot+tan is NOT the correct value at sin^2(theta_W)=2/9 (true "
            "value 2.4053) -- it exactly equals NB-130's EXPERIMENTAL Q'_11 value "
            "computed three lines earlier on the previous page, strongly suggesting "
            "it was carried over rather than recomputed for the new hypothesis. The "
            "other Q_z decimal, 1.33, IS correct (true value 1.3363) and its stated "
            "symbolic form 1/sqrt(3)=0.577 is, however, wrong (doesn't match 1.3363 "
            "at all). The author's own follow-up 'other algebra' self-consistency "
            "check (treating cot+tan=7/3 and cot-tan=4/3 as exact and solving for a "
            "single cot(theta_W)=11/6) is CONFIRMED to genuinely fail: 11/6+6/11 = "
            "157/66 = 2.379, not 7/3 = 2.333 -- the author's self-flagged 'X' is a "
            "correct catch, not an overreaction. Root cause: 7/3 and 4/3 are only "
            "rough two-decimal-place roundings of the true cot+tan=2.405 and "
            "cot-tan=1.336 (themselves already partly corrupted by the copied-over "
            "2.37), not exact fractions -- there is no single self-consistent "
            "rational shortcut here, exactly as the author's own arithmetic "
            "discovered."
        ),
        "verdict": "NEEDS-WORK (self-flagged error confirmed genuine, root cause identified)",
    },
}

path = "test-results/notebook-recon/NB-130_134_sin2thetaw_numerology.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2, default=str)

print(json.dumps(output, indent=2, default=str))
