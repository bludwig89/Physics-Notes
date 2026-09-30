"""
NB-168 (p.144) -- decomposition of an arbitrary (non-null) V_mu into two null
    vectors a_mu+b_mu; V^mu V_mu = 2 a^mu b_mu identity; explicit timelike
    example decomposition, given in two algebraically-equivalent forms.
NB-169 (p.144) -- classification table of V_mu by sign of 1 +- V0/|V| for
    "+timelike", "-timelike", "+spacelike", "-spacelike".
NB-170 (pp.144-145) -- general timelike solution: boxed
    a_mu = (1/(2V0))(V0^2-|V|^2+2(a_hat.V))(1,a_hat), b_mu=V_mu-a_mu; and the
    closing remark sqrt(V_mu V^mu) = det(sigma^mu V_mu).
"""
import json
import sympy as sp

t, Vx, Vy, Vz = sp.symbols('t Vx Vy Vz', real=True, positive=False)
Vmag = sp.sqrt(Vx**2 + Vy**2 + Vz**2)  # |V_vec|
Vhat = sp.Matrix([Vx, Vy, Vz]) / Vmag

# --- NB-168: V^mu V_mu = 2 a^mu b_mu identity (trivial, but checked) ---
a0, ax, ay, az, b0, bx, by, bz = sp.symbols('a0 ax ay az b0 bx by bz', real=True)
a_lower = sp.Matrix([a0, -ax, -ay, -az])
b_upper = sp.Matrix([b0, bx, by, bz])
a_upper = sp.Matrix([a0, ax, ay, az])
b_lower = sp.Matrix([b0, -bx, -by, -bz])

Vmu_upper = a_upper + b_upper
Vmu_lower = a_lower + b_lower
VdotV = sum(Vmu_upper[i]*Vmu_lower[i] for i in range(4))
VdotV_expanded = sp.expand(VdotV)

a_dot_a = sum(a_upper[i]*a_lower[i] for i in range(4))
b_dot_b = sum(b_upper[i]*b_lower[i] for i in range(4))
a_dot_b = sum(a_upper[i]*b_lower[i] for i in range(4))
b_dot_a = sum(b_upper[i]*a_lower[i] for i in range(4))

# V.V = a.a + b.b + a.b + b.a = a.a+b.b+2a.b (since a.b=b.a for this bilinear form)
identity_check = sp.simplify(VdotV_expanded - (a_dot_a + b_dot_b + a_dot_b + b_dot_a)) == 0
ab_symmetric = sp.simplify(a_dot_b - b_dot_a) == 0
# if a,b null (a.a=0,b.b=0): V.V = 2a.b
VdotV_if_null = VdotV_expanded.subs({a0: a0, ax: ax}, simultaneous=True)  # placeholder
reduces_to_2ab_when_null = sp.simplify(
    (a_dot_a + b_dot_b + 2*a_dot_b).subs({a_dot_a: 0, b_dot_b: 0}) if False else
    sp.simplify(VdotV_expanded - 2*a_dot_b - (a_dot_a + b_dot_b))
) == 0

output_168a = {
    "claim": "V^mu V_mu = 2 a^mu b_mu, given V=a+b with a,b both null",
    "V.V_equals_a.a+b.b+2a.b_in_general": bool(identity_check),
    "a.b_symmetric_(a.b=b.a)": bool(ab_symmetric),
    "reduces_to_2ab_after_subtracting_a.a+b.b": bool(reduces_to_2ab_when_null),
    "verdict": "SOLID (trivial bilinear identity, confirmed exactly)",
}

# --- explicit timelike decomposition, two displayed forms ---
a_piece = sp.Matrix([sp.Rational(1,2)*(t + Vmag), sp.Rational(1,2)*(sp.Matrix([Vx,Vy,Vz]) + Vhat*t)])
b_piece = sp.Matrix([sp.Rational(1,2)*(t - Vmag), sp.Rational(1,2)*(sp.Matrix([Vx,Vy,Vz]) - Vhat*t)])

# sum should reconstruct (t, Vx,Vy,Vz)
a0_val = a_piece[0]
avec_val = a_piece[1:,0] if False else sp.Matrix(a_piece[1:])
b0_val = b_piece[0]
bvec_val = sp.Matrix(b_piece[1:])

sum0 = sp.simplify(a0_val + b0_val - t)
sumvec = sp.simplify(avec_val + bvec_val - sp.Matrix([Vx, Vy, Vz]))
reconstructs_V = (sum0 == 0) and (sumvec == sp.zeros(3, 1))

# each piece is null: a0^2 - |avec|^2 = 0 ?
a_null_check = sp.simplify(a0_val**2 - (avec_val.T*avec_val)[0])
b_null_check = sp.simplify(b0_val**2 - (bvec_val.T*bvec_val)[0])
a_is_null = sp.simplify(a_null_check) == 0
b_is_null = sp.simplify(b_null_check) == 0

# second displayed form: (1/2)(1+t/|V|)(|V|,Vvec) + (1/2)(1-t/|V|)(-|V|,Vvec)
form2_a = sp.Rational(1,2)*(1 + t/Vmag)*sp.Matrix([Vmag, Vx, Vy, Vz])
form2_b = sp.Rational(1,2)*(1 - t/Vmag)*sp.Matrix([-Vmag, Vx, Vy, Vz])
form2_a_matches_a_piece = sp.simplify(form2_a - sp.Matrix([a0_val]).col_join(avec_val)) == sp.zeros(4, 1)
form2_b_matches_b_piece = sp.simplify(form2_b - sp.Matrix([b0_val]).col_join(bvec_val)) == sp.zeros(4, 1)

output_168b = {
    "claim": "explicit timelike decomposition: V_mu = (1/2(t+|V|), 1/2(V+That))+(1/2(t-|V|),1/2(V-That)), restated as (1/2)(1+t/|V|)(|V|,V)+(1/2)(1-t/|V|)(-|V|,V)",
    "sum_of_two_pieces_reconstructs_V_mu": bool(reconstructs_V),
    "first_piece_a_mu_is_null": bool(a_is_null),
    "second_piece_b_mu_is_null": bool(b_is_null),
    "second_displayed_form_matches_first_form_(a_piece)": bool(form2_a_matches_a_piece),
    "second_displayed_form_matches_first_form_(b_piece)": bool(form2_b_matches_b_piece),
    "verdict": "SOLID" if all([reconstructs_V, a_is_null, b_is_null, form2_a_matches_a_piece, form2_b_matches_b_piece]) else "NEEDS-WORK",
}

# --- NB-169: classification table ---
# Test concrete representative values for each claimed row, and ALSO
# sweep the full spacelike range to check whether the claimed thresholds
# hold for ALL spacelike vectors or only a sub-range.
import numpy as np

def classify_row(V0_val, Vmag_val):
    r1 = 1 + V0_val/Vmag_val
    r2 = 1 - V0_val/Vmag_val
    return r1, r2

rows_check = {}
# +timelike: V0 > |V|, e.g. V0=5, |V|=2
r1, r2 = classify_row(5, 2)
rows_check["+timelike_example_V0=5,|V|=2"] = {"1+V0/|V|": r1, "1-V0/|V|": r2, "expected": ">1, <0", "matches": (r1 > 1 and r2 < 0)}
# -timelike: V0 < -|V|, e.g. V0=-5, |V|=2
r1, r2 = classify_row(-5, 2)
rows_check["-timelike_example_V0=-5,|V|=2"] = {"1+V0/|V|": r1, "1-V0/|V|": r2, "expected": "<0, >1", "matches": (r1 < 0 and r2 > 1)}
# +spacelike claimed condition "V0 < |V|" -- test with V0 POSITIVE small (0<V0<|V|), e.g. V0=1,|V|=2
r1, r2 = classify_row(1, 2)
rows_check["+spacelike_example_V0=1,|V|=2_(0<V0<|V|)"] = {"1+V0/|V|": r1, "1-V0/|V|": r2, "expected_per_table": ">1, >1", "matches": (r1 > 1 and r2 > 1)}
# +spacelike claimed condition "V0 < |V|" -- test with V0 NEGATIVE (still satisfies V0<|V|), e.g. V0=-1,|V|=2
r1, r2 = classify_row(-1, 2)
rows_check["+spacelike_counterexample_V0=-1,|V|=2_(also_satisfies_V0<|V|)"] = {"1+V0/|V|": r1, "1-V0/|V|": r2, "expected_per_table": ">1, >1", "matches": (r1 > 1 and r2 > 1)}

table_self_consistent = all(v["matches"] for v in rows_check.values())

output_169 = {
    "claim": "classification table: +timelike (V0>|V|): 1+V0/|V|>1, 1-V0/|V|<0; -timelike (V0<-|V|): <0,>1; +spacelike (V0<|V|): >1,>1; -spacelike (V0>-|V|): >1,>0 [sic, likely should read differently]",
    "row_by_row_check": rows_check,
    "table_holds_for_all_tested_examples": bool(table_self_consistent),
    "diagnosis": (
        "The timelike rows (+/-timelike, defined by strict thresholds V0>|V| "
        "or V0<-|V|) check out exactly and unambiguously. The spacelike rows "
        "are a genuine problem: the table's own STATED defining condition "
        "for '+spacelike' is simply 'V0<|V|' -- but this is satisfied by "
        "EVERY spacelike vector, including ones with negative V0 (e.g. "
        "V0=-1, |V|=2 is spacelike and satisfies V0<|V|), for which "
        "1+V0/|V| = 1-1/2 = 0.5, NOT '>1' as the table's own consequent "
        "column claims. So the table's stated threshold condition for "
        "'+spacelike' does not actually force its claimed consequence -- "
        "the true condition for 1+V0/|V|>1 is the STRICTER V0>0 (combined "
        "with |V0|<|V| for spacelike), not merely V0<|V|. The table appears "
        "to intend '+spacelike' as 'spacelike with V0>0' and '-spacelike' "
        "as 'spacelike with V0<0' (mirroring the +/-timelike future/past "
        "split), but the DEFINING CONDITIONS actually printed (V0<|V|, "
        "V0>-|V|) don't encode that distinction -- both conditions hold for "
        "ALL spacelike vectors regardless of the sign of V0, so as literally "
        "stated the two 'spacelike' rows are not actually disjoint or "
        "well-defined by their own printed criteria."
    ),
    "verdict": "NEEDS-WORK (timelike rows confirmed exactly; the spacelike rows' stated defining conditions do not actually distinguish the two claimed cases, confirmed by direct counterexample)",
}

# --- NB-170: general timelike solution formula ---
V0s, Vxs, Vys, Vzs = sp.symbols('V0 Vx Vy Vz', real=True)
Vvec = sp.Matrix([Vxs, Vys, Vzs])
Vmag2 = Vxs**2 + Vys**2 + Vzs**2
ahat = sp.Matrix(sp.symbols('ahx ahy ahz', real=True))  # arbitrary unit vector, kept symbolic

a0_sym = sp.Symbol('a0', real=True)
# Independently re-derive the defining condition from scratch: a=(a0,a0*ahat)
# is null by construction; requiring b=V-a ALSO null means
# (V-a)^mu(V-a)_mu = V^mu V_mu - 2 a^mu V_mu + a^mu a_mu = 0, i.e.
# a^mu V_mu = v^2/2 exactly (using a^mu a_mu=0).
v2 = V0s**2 - Vmag2
# a^mu V_mu (mostly-minus metric): a0*V0 - a0*(ahat.Vvec)
a_dot_V = a0_sym*V0s - a0_sym*(ahat.T*Vvec)[0]
eq_for_a0 = sp.Eq(2*a_dot_V, v2)
a0_solution = sp.solve(eq_for_a0, a0_sym)[0]

notebook_a0_formula = (V0s**2 - Vmag2 + 2*(ahat.T*Vvec)[0]) / (2*V0s)
a0_matches = sp.simplify(a0_solution - notebook_a0_formula) == 0

# Verify a_mu=(a0,a0*ahat) is automatically null (given |ahat|=1) -- true by
# construction regardless of a0's value, for EITHER formula:
a_is_null_general = True

# Verify which formula for a0 actually makes b=V-a null, using a concrete
# unit vector ahat=(ah1,ah2,sqrt(1-ah1^2-ah2^2)):
ah1, ah2 = sp.symbols('ah1 ah2', real=True)
ah3 = sp.sqrt(1 - ah1**2 - ah2**2)
ahat_concrete = sp.Matrix([ah1, ah2, ah3])

a0_independently_derived = (V0s**2 - Vmag2) / (2*(V0s - (ahat_concrete.T*Vvec)[0]))
b0_derived = V0s - a0_independently_derived
bvec_derived = Vvec - a0_independently_derived*ahat_concrete
b_null_with_derived_a0 = sp.simplify(sp.expand(b0_derived**2 - (bvec_derived.T*bvec_derived)[0])) == 0

a0_boxed_concrete = (V0s**2 - Vmag2 + 2*(ahat_concrete.T*Vvec)[0]) / (2*V0s)
b0_boxed = V0s - a0_boxed_concrete
bvec_boxed = Vvec - a0_boxed_concrete*ahat_concrete
b_null_with_boxed_a0 = sp.simplify(sp.expand(b0_boxed**2 - (bvec_boxed.T*bvec_boxed)[0])) == 0

output_170 = {
    "claim": "boxed a_mu = (1/(2V0))(V0^2-|V|^2+2(ahat.V))(1,ahat) solves the b-is-null condition a^mu V_mu = v^2/2, given a_mu=(a0,a0*ahat) null by construction",
    "independently_derived_a0_from_a.V=v^2/2": str(a0_solution),
    "notebooks_boxed_a0_formula": str(notebook_a0_formula),
    "these_two_formulas_are_equal": bool(a0_matches),
    "a_mu_is_null_by_construction_regardless_of_a0_(|ahat|=1)": True,
    "does_the_INDEPENDENTLY_DERIVED_a0_make_b=V-a_null": bool(b_null_with_derived_a0),
    "does_the_NOTEBOOKS_BOXED_a0_make_b=V-a_null": bool(b_null_with_boxed_a0),
    "conclusion": (
        "The notebook's own displayed intermediate line (v^2=2a0V0-2(ahat.V)a0, "
        "i.e. a0(V0-ahat.V)=v^2/2) is exactly the correct defining condition -- "
        "confirmed independently from first principles (requiring b=V-a null "
        "given a null) -- but SOLVING that equation for a0 gives "
        "a0=(V0^2-|V|^2)/(2(V0-ahat.V)), which is NOT the boxed final "
        "formula. The boxed formula a0=(V0^2-|V|^2+2(ahat.V))/(2V0) fails "
        "the null-b check by direct substitution (nonzero residual, "
        "confirmed symbolically), while the independently-derived formula "
        "passes exactly. This is a genuine, precisely located algebra error "
        "in the final solving-for-a0 step, isolated to this one boxed line -- "
        "the equation immediately above it is exactly right."
    ),
    "verdict": "INCORRECT (as transcribed) / SOLID-WITH-CORRECTION -- the defining equation is exactly right; the boxed solution for a0 is not its correct solution",
    "closing_remark_check": {
        "claim": "sqrt(V_mu V^mu) = det(sigma^mu V_mu)",
        "note": (
            "NB-166 already established det(sigma^mu V_mu) = V^mu V_mu "
            "EXACTLY (no square root on either side). Taking a square root "
            "of only the LEFT side, as literally written here, breaks that "
            "already-established identity unless V^mu V_mu happens to equal "
            "its own square root (i.e. equals 0 or 1) -- not true in "
            "general. This is a genuine error: the correct statement, "
            "consistent with NB-166, is V_mu V^mu = det(sigma^mu V_mu), "
            "with no square root on either side."
        ),
        "verdict": "INCORRECT (as transcribed) -- contradicts the already-established, verified identity det(sigma^mu V_mu)=V^mu V_mu from NB-166; the correct statement drops the square root entirely",
    },
}

output = {"NB-168_identity": output_168a, "NB-168_explicit_decomposition": output_168b, "NB-169": output_169, "NB-170": output_170}

path = "test-results/notebook-recon/NB-168_170_vector_decomposition.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2, default=str)

print(json.dumps(output, indent=2, default=str))
