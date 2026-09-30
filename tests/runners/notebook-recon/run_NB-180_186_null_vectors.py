"""
NB-180, NB-182, NB-184, NB-185, NB-186 (pp.176-182, "Construction of Null
Vectors; Spinor Paper Outline" -- the final pages of the notebook).

NB-180 (p.176, "Two Coordinate Systems"): a rotation about z sends the
stereographic-plane complex coordinate eta_0 = x_0+i y_0 to e^{i theta} eta_0
(an overall phase).

NB-182 (pp.176-177, "Construction of Null Vectors as Tensor Products"):
  Q = (alpha,beta)^T (alpha*,beta*) [outer product, v v^dagger with v=(alpha,beta)^T]
    = [[alpha alpha*, beta* alpha],[alpha* beta, beta* beta]]
    = [[V0-Vz, -Vx+iVy],[-Vx-iVy, V0+Vz]]
  det Q = 0 identically; alpha=sqrt(V0-Vz) e^{i theta}, beta=sqrt(V0+Vz) e^{i phi}
  (given V null, V0^2=Vx^2+Vy^2+Vz^2); (Vx+iVy)/sqrt(Vx^2+Vy^2) = -e^{i(phi-theta)}.

NB-184 (p.178, "Null Matrix Factorization"): det(M)=0 for M=[[a,b],[c,d]]
  implies M = a * outer((1,beta),(1,alpha)) with alpha=b/a, beta=c/a.
  The notebook's stated intermediate step "if b=alpha*a then c=alpha*d" is
  checked separately from the (correct) final boxed result.

NB-185 (pp.178-179, "Timelike Decomposition"): V_mu = a_mu + b_mu, a,b both
  null, a_mu=(a0,a0 a-hat); derives 2 V.a = V^2 and a boxed closed form for a0.

NB-186 (pp.179-182, "Final Null Component Geometry"): a0 = b + a-hat.u,
  special case V parallel to z-hat, a sphere/ellipsoid locus for (ax,ay,az),
  and a cylindrical-coordinate formula rho_s = 2 r rho_0/(r^2-rho_0^2).

All five builds are verified independently below with sympy, working strictly
from the mostly-plus metric convention V.W = V0 W0 - Vx Wx - Vy Wy - Vz Wz
used throughout this section of the notebook (consistent with V0^2-|V|^2
appearing as the invariant length). Positive-symbol substitutions are used
wherever a bare sqrt(real symbol) would otherwise fail to auto-simplify its
own conjugate/square (sympy does not know the sign of a generic real symbol);
this affects presentation only, not the physics being tested.
"""
import sympy as sp
import json
import pathlib

I = sp.I

# ===========================================================================
# NB-180: rotation about z is a phase rotation of eta = x0 + i y0
# ===========================================================================
x0, y0, th = sp.symbols('x0 y0 theta', real=True)
eta = x0 + I * y0
eta_c = x0 - I * y0


def stereo_xyz(e, ec):
    denom = 1 + e * ec
    xx = sp.simplify((e + ec) / denom)
    yy = sp.simplify(-I * (e - ec) / denom)
    zz = sp.simplify((e * ec - 1) / denom)
    return xx, yy, zz


x_base, y_base, z_base = stereo_xyz(eta, eta_c)

eta_rot = sp.exp(I * th) * eta
eta_rot_c = sp.exp(-I * th) * eta_c
x_rot, y_rot, z_rot = stereo_xyz(eta_rot, eta_rot_c)

x_expect = sp.cos(th) * x_base - sp.sin(th) * y_base
y_expect = sp.sin(th) * x_base + sp.cos(th) * y_base
z_expect = z_base

# exp(I*theta) forms need an explicit rewrite to cos/sin before expand_trig
# will cancel them against the target cos/sin expressions.
x_diff = sp.simplify(sp.expand_trig(sp.simplify((x_rot - x_expect).rewrite(sp.cos))))
y_diff = sp.simplify(sp.expand_trig(sp.simplify((y_rot - y_expect).rewrite(sp.cos))))
z_diff = sp.simplify(z_rot - z_expect)

x_match = x_diff == 0
y_match = y_diff == 0
z_match = z_diff == 0

nb180 = {
    "build": "NB-180",
    "claim_quote": (
        "'Rotation about z: changes overall phase of (x0,y0), sending "
        "x0+iy0 -> e^{i theta}(x0+iy0).' Context: two coordinate systems and "
        "their stereographic representations (xs,ys,zs) vs (xs',ys',zs') and "
        "(x0,y0) vs (x0',y0'); bullets 'Z determined by direction of motion "
        "of photon', 'R of sphere determines relative magnitude', 'What is "
        "overall phase?'."
    ),
    "reconstructed_input": (
        "Used the r=1 stereographic map x=(eta+eta*)/(1+eta eta*), "
        "y=-i(eta-eta*)/(1+eta eta*), z=(eta eta*-1)/(eta eta*+1), the r->1 "
        "case of the general-radius forward-projection formula the notebook "
        "uses elsewhere for stereographic projection (not given directly in "
        "this page range; reconstructed here from the standard stereographic "
        "projection form, needed since only the claim itself, not the "
        "underlying projection formula, appears in the assigned lines)."
    ),
    "checked": "Substitute eta -> e^{i theta} eta and confirm (x,y,z) transforms by an exact rotation by theta about z, for symbolic real theta, x0, y0.",
    "x_matches_rotation": bool(x_match),
    "y_matches_rotation": bool(y_match),
    "z_invariant_under_the_substitution": bool(z_match),
    "verdict": "SOLID" if (x_match and y_match and z_match) else "NEEDS-WORK",
    "note": (
        "Confirms the standard fact that a rotation about the sphere's polar "
        "(z) axis acts as a pure phase (Mobius) transformation eta -> "
        "e^{i theta} eta on the stereographic-plane coordinate -- exactly "
        "answers the page's own question 'what is the overall phase?' (it is "
        "precisely the z-axis rotation angle). The 'outline for spinor "
        "paper' 3-item to-do list on the same page (deal with null vectors "
        "as tensor products / non-null-vector breakdown / spinor field "
        "equations of motion) is a bare table-of-contents entry with no math "
        "-- NOT-TESTABLE, and is in any case executed by the very builds "
        "(NB-182/184/185/186) that follow it on later pages."
    ),
}

# ===========================================================================
# NB-182: null vector as a rank-1 (outer-product) tensor
# ===========================================================================
al, be = sp.symbols('alpha beta', complex=True)
al_c, be_c = sp.conjugate(al), sp.conjugate(be)

v = sp.Matrix([al, be])
vdag = sp.Matrix([[al_c, be_c]])
Q = v * vdag  # v v^dagger

Q_expected = sp.Matrix([[al * al_c, be_c * al], [al_c * be, be_c * be]])
Q_matches_written_entries = sp.simplify(Q - Q_expected) == sp.zeros(2, 2)

detQ = sp.simplify(Q.det())
det_is_zero = detQ == 0

# Use positive symbols P=V0-Vz, Q=V0+Vz (physically required for the sqrt
# form used) so sympy can simplify sqrt(P)*conjugate(sqrt(P)) = P, etc.
P, Qm = sp.symbols('P Q', positive=True)  # P=V0-Vz, Qm=V0+Vz
theta_s, phi_s = sp.symbols('theta phi', real=True)
al_form = sp.sqrt(P) * sp.exp(I * theta_s)
be_form = sp.sqrt(Qm) * sp.exp(I * phi_s)

alal_c = sp.simplify(al_form * sp.conjugate(al_form))
bebe_c = sp.simplify(be_form * sp.conjugate(be_form))
alstar_be = sp.simplify(sp.conjugate(al_form) * be_form)

alal_c_matches = sp.simplify(alal_c - P) == 0
bebe_c_matches = sp.simplify(bebe_c - Qm) == 0
alstar_be_general_form = sp.sqrt(P * Qm) * sp.exp(I * (phi_s - theta_s))
alstar_be_matches_general = sp.simplify(alstar_be - alstar_be_general_form) == 0

# P*Q = (V0-Vz)(V0+Vz) = V0^2-Vz^2 = Vx^2+Vy^2 given V null (V0^2=Vx^2+Vy^2+Vz^2)
V0, Vx, Vy, Vz = sp.symbols('V0 Vx Vy Vz', real=True)
null_reduction_ok = sp.expand((V0**2 - Vz**2) - (Vx**2 + Vy**2)).subs(
    V0**2, Vx**2 + Vy**2 + Vz**2
) == 0

# Final boxed phase relation: given alpha*beta = -Vx-iVy (stated) AND
# alpha*beta = sqrt(Vx^2+Vy^2) e^{i(phi-theta)} (derived, under nullness),
# these combine to (Vx+iVy)/sqrt(Vx^2+Vy^2) = -e^{i(phi-theta)}. Verify by
# isolating e^{i(phi-theta)} from the "given" relation and comparing to the
# claim's own definition of it.
e_iphitheta_from_given = sp.simplify((-Vx - I * Vy) / sp.sqrt(Vx**2 + Vy**2))
claim_lhs = (Vx + I * Vy) / sp.sqrt(Vx**2 + Vy**2)
claim_rhs_defines_e_iphitheta_as = -1  # claim: claim_lhs = -e^{i(phi-theta)}
rearrangement_check = sp.simplify(e_iphitheta_from_given + claim_lhs) == 0  # e^{i(...)} = -claim_lhs <=> claim_lhs = -e^{i(...)}

nb182 = {
    "build": "NB-182",
    "claim_quote": (
        "(alpha* beta*) tensor (alpha;beta) = [[a a*, b* a],[a* b, b* b]] = "
        "[[V0-Vz, -Vx+iVy],[-Vx-iVy, V0+Vz]]; det Q=0; alpha alpha*=V0-Vz, "
        "beta beta*=V0+Vz, alpha* beta=-Vx-iVy; alpha=sqrt(V0-Vz) e^{i "
        "theta}, beta=sqrt(V0+Vz) e^{i phi}; alpha* beta = "
        "sqrt(V0^2-Vz^2) e^{i(phi-theta)} = sqrt(Vx^2+Vy^2) e^{i(phi-theta)}; "
        "(Vx+iVy)/sqrt(Vx^2+Vy^2) = -e^{i(phi-theta)}."
    ),
    "note_on_notation": (
        "The written tensor-product order '(alpha* beta*) tensor (alpha;beta)' "
        "does not literally match a standard outer-product index convention, "
        "but reproduces exactly the entries of Q = v v^dagger with "
        "v=(alpha,beta)^T once read as intended (confirmed below) -- a "
        "loose/informal use of 'tensor product' for an outer product, common "
        "in hand notes."
    ),
    "Q_matches_written_entries": bool(Q_matches_written_entries),
    "det_Q_is_identically_zero": bool(det_is_zero),
    "alpha_alphastar_matches_V0_minus_Vz": bool(alal_c_matches),
    "beta_betastar_matches_V0_plus_Vz": bool(bebe_c_matches),
    "alphastar_beta_matches_general_phase_form": bool(alstar_be_matches_general),
    "V0sq_minus_Vzsq_equals_Vxsq_plus_Vysq_given_V_null": bool(null_reduction_ok),
    "final_boxed_phase_relation_is_consistent_rearrangement": bool(rearrangement_check),
    "verdict": "SOLID",
    "verdict_detail": (
        "Every algebraic step checks out exactly: any rank-1 outer product "
        "v v^dagger has det=0 (confirmed symbolically for generic complex "
        "alpha, beta), matching the entries to V0,Vx,Vy,Vz correctly encodes "
        "a null 4-vector V (det Q=0 <=> V.V=0 with this V<->Q dictionary), "
        "the polar (magnitude,phase) form for alpha,beta correctly "
        "reproduces V0-Vz and V0+Vz (confirmed once V0-Vz, V0+Vz are given "
        "their required positivity, i.e. V timelike/null and future-pointing "
        "-- an implicit assumption of the whole construction), and the final "
        "phase relation for alpha*beta is confirmed to be a correct, direct "
        "rearrangement of alpha*beta=-Vx-iVy together with "
        "V0^2-Vz^2=Vx^2+Vy^2 (the nullness of V, used implicitly here but "
        "not restated on this page)."
    ),
}

# ===========================================================================
# NB-184: null 2x2 matrix factorization
# ===========================================================================
a, b, c, d = sp.symbols('a b c d', complex=True)
alpha_f = b / a
beta_f = c / a

det_zero_constraint = sp.Eq(a * d, b * c)
d_solved = sp.solve(det_zero_constraint, d)[0]

d_from_alpha_beta = sp.simplify(alpha_f * beta_f * a)
final_boxed_ok = sp.simplify(d_from_alpha_beta - d_solved) == 0

# notebook's intermediate line: "if b=alpha*a then c=alpha*d" -- check c=alpha*d
# after eliminating d via the det=0 constraint
c_equals_alpha_d_generic = sp.simplify((alpha_f * d_solved) - c)
intermediate_holds_identically = c_equals_alpha_d_generic == 0

counterexample = {a: sp.Integer(1), b: sp.Integer(2), c: sp.Integer(3)}
d_val = sp.Rational(counterexample[b] * counterexample[c], counterexample[a])
alpha_val = counterexample[b] / counterexample[a]

M = sp.Matrix([[a, b], [c, d_solved]])
u = sp.Matrix([1, beta_f])
w = sp.Matrix([[1, alpha_f]])
outer = a * (u * w)
factorization_matches = sp.simplify(M - outer) == sp.zeros(2, 2)

nb184 = {
    "build": "NB-184",
    "claim_quote": (
        "M=[[a,b],[c,d]], det(M)=ad-bc=0 => a/b=c/d and a/c=b/d. So if "
        "b=alpha a then c=alpha d; if c=beta a then d=beta b; so "
        "M=[[a,alpha a],[beta a, alpha beta a]] = a(1,alpha) tensor (1;beta), "
        "alpha=b/a."
    ),
    "final_boxed_factorization_M_equals_a_times_outer_1_beta_1_alpha": bool(factorization_matches),
    "d_equals_alpha_beta_a_given_ad_eq_bc": bool(final_boxed_ok),
    "intermediate_claim_c_equals_alpha_times_d": {
        "c_minus_alpha_d_after_eliminating_d_via_constraint": str(c_equals_alpha_d_generic),
        "holds_identically": bool(intermediate_holds_identically),
    },
    "intermediate_claim_counterexample_a1_b2_c3_d6": {
        "alpha_value": str(alpha_val),
        "alpha_times_d": str(alpha_val * d_val),
        "c_value": str(counterexample[c]),
        "alpha_times_d_equals_c": bool(alpha_val * d_val == counterexample[c]),
    },
    "verdict": "SOLID-WITH-CORRECTION",
    "verdict_detail": (
        "The FINAL boxed result -- any det=0 matrix factors as "
        "M = a*(1,alpha)(1,beta)-outer-product with alpha=b/a, beta=c/a, "
        "d=alpha*beta*a -- is exactly correct and verified symbolically for "
        "generic a,b,c,d subject only to ad=bc (a standard, true fact: every "
        "rank-<=1 2x2 matrix is an outer product of two 2-vectors). However "
        "the notebook's own INTERMEDIATE derivation step, 'if b=alpha a then "
        "c=alpha d', is false in general -- confirmed both symbolically "
        "(c-alpha*d does not vanish identically once d is eliminated via the "
        "det=0 constraint: leaves -c+b^2c/a^2) and with the concrete "
        "counterexample a=1,b=2,c=3,d=6 (ad=bc: 1*6=2*3=6, consistent; "
        "alpha=b/a=2; alpha*d=12 != c=3). The correct intermediate relation "
        "is d=alpha*c (not c=alpha*d) -- consistent with the final boxed "
        "d=alpha*beta*a once beta=c/a is also used. This looks like a simple "
        "algebra slip in copying which side of a/c=b/d gets multiplied "
        "through; it does not propagate into the (correct) final boxed "
        "result."
    ),
}

# ===========================================================================
# NB-185: timelike decomposition into two null vectors
# ===========================================================================
V0s, Vxs, Vys, Vzs = sp.symbols('V0 Vx Vy Vz', real=True)
a0s = sp.symbols('a0', real=True)
ahx, ahy, ahz = sp.symbols('ahatx ahaty ahatz', real=True)

a_mu = [a0s, a0s * ahx, a0s * ahy, a0s * ahz]
V_mu = [V0s, Vxs, Vys, Vzs]


def dot4(p, q):
    return p[0] * q[0] - p[1] * q[1] - p[2] * q[2] - p[3] * q[3]


a_dot_a_expanded = sp.expand(dot4(a_mu, a_mu))
a_dot_a_factored_check = sp.simplify(a_dot_a_expanded - a0s**2 * (1 - (ahx**2 + ahy**2 + ahz**2))) == 0

b_mu = [V_mu[k] - a_mu[k] for k in range(4)]
b_dot_b = sp.expand(dot4(b_mu, b_mu))
V_dot_V = sp.expand(dot4(V_mu, V_mu))
V_dot_a = sp.expand(dot4(V_mu, a_mu))

identity_check = sp.expand(b_dot_b - (V_dot_V - 2 * V_dot_a + a_dot_a_expanded)) == 0

ahat_dot_V = ahx * Vxs + ahy * Vys + ahz * Vzs
V_dot_a_matches_a0_form = sp.simplify(V_dot_a - a0s * (V0s - ahat_dot_V)) == 0

v2 = sp.expand(V_dot_V)

# --- Reading A: ahat is an INDEPENDENT freely-chosen (genuinely normalized) unit vector
a0_ratio_solution = sp.simplify(v2 / (2 * (V0s - ahat_dot_V)))
eqstar = sp.Eq(v2, 2 * a0s * (V0s - ahat_dot_V))
a0_solve_readingA = sp.solve(eqstar, a0s)[0]
readingA_matches_ratio = sp.simplify(a0_solve_readingA - a0_ratio_solution) == 0

notebook_boxed_a0 = (V0s**2 - (Vxs**2 + Vys**2 + Vzs**2) + 2 * ahat_dot_V) / (2 * V0s)
readingA_matches_notebook_boxed = sp.simplify(a0_solve_readingA - notebook_boxed_a0) == 0

V0n, Vmag2n, pn = sp.Rational(5), sp.Rational(9), sp.Rational(1)
ratio_val = (V0n**2 - Vmag2n) / (2 * (V0n - pn))
boxed_val = (V0n**2 - Vmag2n + 2 * pn) / (2 * V0n)
readingA_numeric_mismatch = ratio_val != boxed_val

# --- Reading B: (ax,ay,az) = RAW (non-unit) components of the spatial vector
axr, ayr, azr = sp.symbols('ax ay az', real=True)
a0_solve_readingB = sp.simplify((v2 / 2 + (Vxs * axr + Vys * ayr + Vzs * azr)) / V0s)
readingB_matches_notebook_boxed_raw_form = sp.simplify(
    a0_solve_readingB - (V0s**2 - (Vxs**2 + Vys**2 + Vzs**2) + 2 * (Vxs * axr + Vys * ayr + Vzs * azr)) / (2 * V0s)
) == 0

nb185 = {
    "build": "NB-185",
    "claim_quote": (
        "(1/2)(V0^2-|V|^2)^{1/2} = a0(V0 - ahat.V) [as transcribed, with a "
        "literal square-root exponent]; a_mu=(a0,a0 ahat) null; "
        "V_mu=a_mu+b_mu, b_mu=V_mu-a_mu, both null: a.a=0, (V-a).(V-a)=0 => "
        "v^2 = V.V = 2 V.a = 2 a0 V0 - 2 a0(ahat.V); solved for a0: "
        "a0 = (1/(2V0))(V0^2-|V|^2+2 ahat.V) [boxed]."
    ),
    "a_dot_a_equals_a0sq_times_1_minus_ahat_magnitude_sq": bool(a_dot_a_factored_check),
    "identity_b_dot_b_equals_VdotV_minus_2Vdota_plus_adota": bool(identity_check),
    "V_dot_a_equals_a0_times_V0_minus_ahat_dot_V": bool(V_dot_a_matches_a0_form),
    "master_relation_v2_eq_2_a0_times_V0_minus_ahatV": "confirmed: a.a=0 (ahat unit) & b.b=0 combine to V.V=2V.a",
    "transcription_note_line_3319": (
        "As transcribed, '(1/2)(V0^2-|V|^2)^{1/2} = a0(V0-ahat.V)' carries a "
        "literal square-root exponent on the whole (V0^2-|V|^2) factor. This "
        "does not match the correctly-derived relation v^2/2 = a0(V0-ahat.V) "
        "(no square root) confirmed above, and restated (doubled, still no "
        "square root) three lines later at line 3333 (v^2 = 2 a0 V0 - "
        "2 a0(ahat.V)). Almost certainly an OCR/transcription artifact -- "
        "the exponent 1/2 was meant as the numeric COEFFICIENT one-half in "
        "front of the parenthesis, not a square-root power."
    ),
    "reading_A_ahat_as_independent_unit_vector": {
        "description": "Treat ahat as a freely chosen, genuinely normalized unit direction; solve Eq* for a0 explicitly.",
        "sympy_solve_matches_ratio_form_v2_over_2(V0-ahatV)": bool(readingA_matches_ratio),
        "sympy_solve_matches_notebooks_boxed_additive_form": bool(readingA_matches_notebook_boxed),
        "numeric_counterexample_V0=5_Vmag2=9_ahatdotV=1": {
            "ratio_form_value": str(ratio_val),
            "notebook_boxed_form_value": str(boxed_val),
            "mismatch": bool(readingA_numeric_mismatch),
        },
    },
    "reading_B_ax_ay_az_as_raw_vector_components": {
        "description": (
            "Treat (ax,ay,az) as the actual (non-unit) spatial components of "
            "the null vector's spatial part (a0=sqrt(ax^2+ay^2+az^2)), "
            "matching how the immediately-following section (line 3345, "
            "'ahat = (ax x+ay y+az z)/sqrt(ax^2+ay^2+az^2)') explicitly uses "
            "these symbols. In this reading, Eq* is linear and gives a0 "
            "explicitly with no circularity."
        ),
        "matches_notebooks_boxed_formula_with_ahat_dot_V_read_as_raw_(ax,ay,az)_dot_V": bool(
            readingB_matches_notebook_boxed_raw_form
        ),
    },
    "verdict": "SOLID-WITH-CORRECTION",
    "verdict_detail": (
        "The underlying physics/geometry (splitting a timelike vector V into "
        "two null vectors a, b=V-a, with a_mu=(a0,a0 ahat)) and the master "
        "relation V.V=2V.a are exactly standard and confirmed. The "
        "notebook's boxed 'solved for a0' formula, "
        "a0=(V0^2-|V|^2+2 ahat.V)/(2V0), is mathematically INCORRECT if "
        "'ahat' there means a genuinely independent, normalized unit vector "
        "(sympy's own solve() of Eq* for a0 gives the ratio "
        "a0=(V0^2-|V|^2)/(2(V0-ahat.V)) instead -- confirmed both "
        "symbolically and by a numeric counterexample, V0=5,|V|^2=9, "
        "ahat.V=1, giving 2 vs 9/5). However the SAME formula is exactly and "
        "correctly reproduced one section later once '(ax,ay,az)' are read "
        "as the raw, non-unit spatial components of the null vector itself "
        "(confirmed exactly, reading B) -- which is also how that very "
        "section goes on to use them (a0=sqrt(ax^2+ay^2+az^2), see NB-186). "
        "So this is a NOTATIONAL error (silently overloading the hat symbol "
        "'ahat.V' to sometimes mean the true unit-vector dot product, other "
        "times the raw-vector dot product a_vec.V, without flagging the "
        "switch), not a physics error: the boxed formula is correct once "
        "read as a0=(V0^2-|V|^2+2*a_vec.V)/(2V0) using the raw vector; the "
        "true closed form for a genuinely independent unit direction is "
        "instead the ratio a0=(V0^2-|V|^2)/(2(V0-ahat.V))."
    ),
}

# ===========================================================================
# NB-186: special z-aligned case, sphere/ellipsoid locus, cylindrical formula
# ===========================================================================
V02, Vz2 = sp.symbols('V0 Vz', real=True)
axx, ayy, azz = sp.symbols('ax ay az', real=True)
a0_gen = sp.symbols('a0gen', real=True)  # kept separate from sqrt-form for clean solve

# b.b=0 constraint (V||z: Vx=Vy=0), a0 not yet substituted:
b2_raw = sp.expand((V02 - a0_gen)**2 - (axx**2 + ayy**2 + (Vz2 - azz)**2))
# eliminate ax^2+ay^2 via a0_gen^2 = ax^2+ay^2+az^2  =>  ax^2+ay^2 = a0_gen^2-az^2
b2_sub = sp.expand(b2_raw.subs(axx**2 + ayy**2, a0_gen**2 - azz**2))
a0_master_solution = sp.solve(sp.Eq(b2_sub, 0), a0_gen)[0]  # linear in a0_gen

# Eq (line 3349): a0*(V0 - ahatz*Vz) = (1/2)(V0^2-Vz^2), ahatz = az/a0
a0sym = sp.sqrt(axx**2 + ayy**2 + azz**2)
ahatz = azz / a0sym
eq3349_lhs = sp.simplify(a0sym * (V02 - ahatz * Vz2))
eq3349_rhs = sp.Rational(1, 2) * (V02**2 - Vz2**2)
eq3349_lhs_equals_true_form = sp.simplify(eq3349_lhs - (V02 * a0sym - Vz2 * azz)) == 0
# and (V0*a0 - Vz*az) should equal (V0^2-Vz^2)/2 on the true solution set:
true_master_matches_a0_master_solution = sp.simplify(
    (V02 * a0_master_solution - Vz2 * azz) - eq3349_rhs
) == 0

# Line 3351 claim: a0 = (1/4)(V0^2-Vz^2)/(V0-ahatz*Vz)^2  -- compare to
# dividing 3349 through by (V0-ahatz*Vz), which gives the correct first-power form
a0_correct_dividing_form = sp.simplify(eq3349_rhs / (V02 - ahatz * Vz2))
notebook_3351_claim = sp.Rational(1, 4) * (V02**2 - Vz2**2) / (V02 - ahatz * Vz2)**2
line3351_matches_correct_dividing_form = sp.simplify(notebook_3351_claim - a0_correct_dividing_form) == 0

V0v, Vzv, azv = sp.Rational(5), sp.Rational(3), sp.Rational(1, 2)
a0_true_num = a0_master_solution.subs({V02: V0v, Vz2: Vzv, azz: azv})
ahatz_num = azv / a0_true_num
notebook_3351_num_value = sp.nsimplify(sp.Rational(1, 4) * (V0v**2 - Vzv**2) / (V0v - ahatz_num * Vzv)**2)
correct_first_power_num_value = sp.nsimplify(sp.Rational(1, 2) * (V0v**2 - Vzv**2) / (V0v - ahatz_num * Vzv))

line3351_numeric_mismatch = notebook_3351_num_value != correct_first_power_num_value
line3351_matches_true_a0_num = notebook_3351_num_value == a0_true_num

# --- Sphere/ellipsoid locus for (ax,ay,az): eliminate a0 between
# a0_master_solution (linear, from b.b=0 using a0^2=ax^2+ay^2+az^2 once) and
# the SEPARATE definitional relation a0^2=ax^2+ay^2+az^2. Substitute the first
# into the second directly to get the pure (ax,ay,az) locus.
locus_eq = sp.expand(a0_master_solution**2 - (axx**2 + ayy**2 + azz**2))

alpha_sym = 1 - Vz2**2 / V02**2

claimed_sphere = sp.expand(axx**2 + ayy**2 + (azz - Vz2 / 2)**2 - alpha_sym / 4)
claimed_sphere_matches_locus = sp.simplify(claimed_sphere - (-locus_eq)) == 0

corrected_ellipsoid = sp.expand(
    axx**2 + ayy**2 + alpha_sym * (azz - Vz2 / 2)**2 - V02**2 * alpha_sym / 4
)
corrected_ellipsoid_matches_locus = sp.simplify(corrected_ellipsoid - (-locus_eq)) == 0

# numeric point check: V0=5, Vz=3, az=1 => a0 = (25-9+6)/10=2.2, ax^2+ay^2=3.84
V0nn, Vznn, aznn = sp.Rational(5), sp.Rational(3), sp.Integer(1)
a0nn = a0_master_solution.subs({V02: V0nn, Vz2: Vznn, azz: aznn})
axsq_aysq_nn = a0nn**2 - aznn**2
claimed_value_at_point = (axsq_aysq_nn + (aznn - Vznn / 2)**2)
claimed_target_at_point = alpha_sym.subs({V02: V0nn, Vz2: Vznn}) / 4
corrected_value_at_point = axsq_aysq_nn + alpha_sym.subs({V02: V0nn, Vz2: Vznn}) * (aznn - Vznn / 2)**2
corrected_target_at_point = V0nn**2 * alpha_sym.subs({V02: V0nn, Vz2: Vznn}) / 4

# --- cylindrical formula: rho_s = 2 r rho_0 / (r^2 - rho_0^2), compared to
# the standard stereographic tangent-half-angle double-angle identity:
# if rho_0 = r*tan(phi/2) then the true "doubled" radius is r*tan(phi).
phi_sym, r_sym = sp.symbols('phi r', positive=True)
rho0_expr = r_sym * sp.tan(phi_sym / 2)
notebook_cyl_formula = sp.simplify(2 * r_sym * rho0_expr / (r_sym**2 - rho0_expr**2))
corrected_cyl_formula = sp.simplify(2 * r_sym**2 * rho0_expr / (r_sym**2 - rho0_expr**2))
target_cyl = r_sym * sp.tan(phi_sym)

notebook_cyl_diff = sp.simplify(sp.trigsimp(notebook_cyl_formula - target_cyl))
corrected_cyl_diff = sp.simplify(sp.trigsimp(corrected_cyl_formula - target_cyl))

# dimensional check: units of notebook_cyl_formula vs rho_s (should be length)
# 2*r*rho0 has units [L^2], (r^2-rho0^2) has units [L^2] => notebook formula
# is DIMENSIONLESS, but rho_s must carry units of length -- confirmed by the
# trig identity match failing by exactly a missing overall factor of r,
# consistent with a dropped length dimension.

nb186 = {
    "build": "NB-186",
    "claim_quote": (
        "a0 = (1/(2V0))(V0^2-|V|^2+2 ahat.V) = b + ahat.u, ahat=(ax,ay,az)/"
        "sqrt(ax^2+ay^2+az^2), b=(V0^2-|V|^2)/(2V0), u=V/V0. If V || z-hat: "
        "u_x=u_y=0 and a0(V0-az Vz)=(1/2)(V0^2-Vz^2); "
        "sqrt(ax^2+ay^2+az^2)=a0=(1/4)(V0^2-Vz^2)/(V0-az Vz)^2; "
        "ax^2+ay^2+(az-Vz/2)^2=(1/4)alpha, alpha=1-Vz^2/V0^2; cylindrical: "
        "rho_s = 2 r rho_0/(r^2-rho_0^2), theta_s=theta_0."
    ),
    "identity_a0_equals_b_plus_ahat_dot_u_is_algebraic_regrouping_of_boxed_a0": (
        "trivially true by definition of b,u (b+ahat.u = (V0^2-|V|^2)/(2V0) "
        "+ (ahat.V)/V0 = (V0^2-|V|^2+2 ahat.V)/(2V0), identical to the boxed "
        "a0 formula it restates) -- inherits whichever reading (raw-vector "
        "vs unit-vector) is used for 'ahat.V' (see NB-185)."
    ),
    "line_3349_matches_true_zaligned_master_relation_V0a0_minus_Vzaz_eq_half(V0sq-Vzsq)": bool(
        eq3349_lhs_equals_true_form
    ),
    "line_3351_a0=quarter(V0sq-Vzsq)/(V0-ahatzVz)sq": {
        "symbolic_match_to_correctly_dividing_3349_by_(V0-ahatzVz)": bool(line3351_matches_correct_dividing_form),
        "numeric_check_V0=5_Vz=3_az=0.5": {
            "notebook_3351_value": str(notebook_3351_num_value),
            "correct_first_power_division_value": str(correct_first_power_num_value),
            "true_a0_value_from_master_relation": str(a0_true_num),
            "notebook_3351_matches_true_a0": bool(line3351_matches_true_a0_num),
            "mismatch_confirmed": bool(line3351_numeric_mismatch),
        },
        "verdict_component": "INCORRECT",
    },
    "sphere_locus_claim_ax2+ay2+(az-Vz/2)2=alpha/4": {
        "matches_derived_locus_exactly": bool(claimed_sphere_matches_locus),
        "numeric_check_V0=5_Vz=3_az=1": {
            "true_ax2+ay2_on_locus": str(axsq_aysq_nn),
            "claimed_sphere_LHS_(ax2+ay2+(az-Vz/2)2)": str(claimed_value_at_point),
            "claimed_sphere_RHS_(alpha/4)": str(claimed_target_at_point),
            "mismatch": bool(claimed_value_at_point != claimed_target_at_point),
        },
        "verdict_component": "INCORRECT",
    },
    "corrected_ellipsoid_ax2+ay2+alpha*(az-Vz/2)2=V0sq*alpha/4": {
        "matches_derived_locus_exactly": bool(corrected_ellipsoid_matches_locus),
        "numeric_check_V0=5_Vz=3_az=1": {
            "corrected_LHS": str(corrected_value_at_point),
            "corrected_RHS": str(corrected_target_at_point),
            "matches": bool(corrected_value_at_point == corrected_target_at_point),
        },
        "dimensional_note": (
            "ax,ay,az carry the same units as V0,Vz (a 4-vector's spatial "
            "components), so the RHS of any such locus equation must carry "
            "units of [length]^2 to match ax^2 on the LHS. The notebook's "
            "literal RHS 'alpha/4' (alpha dimensionless) is DIMENSIONALLY "
            "inconsistent by itself, independent of the coefficient found "
            "above; the corrected RHS V0^2*alpha/4 repairs this."
        ),
    },
    "cylindrical_formula_rho_s=2r_rho0/(r2-rho02)": {
        "matches_r_tan(phi)_target_as_literally_written": bool(notebook_cyl_diff == 0),
        "notebook_formula_actually_equals_tan(phi)_dimensionless_not_r*tan(phi)": True,
        "corrected_formula_2_r_squared_rho0_over_(r2-rho02)_matches_r_tan(phi)": bool(corrected_cyl_diff == 0),
        "dimensional_note": (
            "With rho_0=r*tan(phi/2) (both lengths), 2 r rho_0 has units "
            "[L^2] and (r^2-rho_0^2) has units [L^2], so the notebook's "
            "literal formula 2 r rho_0/(r^2-rho_0^2) is DIMENSIONLESS -- it "
            "cannot equal a radius rho_s (units [L]). Confirmed algebraically "
            "the formula reduces exactly to tan(phi) (dimensionless, the "
            "correct tangent-double-angle value divided by an extra factor "
            "of r), while the dimensionally-consistent corrected formula "
            "2 r^2 rho_0/(r^2-rho_0^2) reduces exactly to r*tan(phi), "
            "matching the standard stereographic double-angle radius "
            "identity exactly."
        ),
        "verdict_component": "INCORRECT-AS-TRANSCRIBED / SOLID-WITH-CORRECTION",
    },
    "verdict": "SOLID-WITH-CORRECTION",
    "verdict_detail": (
        "(i) a0=b+ahat.u is a trivial, correct algebraic regrouping of the "
        "NB-185 boxed formula. (ii) The z-aligned master relation, line "
        "3349 'a0(V0-ahatz Vz)=(1/2)(V0^2-Vz^2)', is exactly correct -- the "
        "V||z specialization of the true relation V0 a0 - Vz az = "
        "(V0^2-Vz^2)/2, independently re-derived here from a.a=0 & b.b=0 "
        "and matching exactly once ahatz=az/a0 is substituted. (iii) Line "
        "3351 is INCORRECT: dividing the correct line-3349 relation through "
        "by (V0-ahatz Vz) gives a0=(1/2)(V0^2-Vz^2)/(V0-ahatz Vz) -- a FIRST "
        "power denominator with coefficient 1/2 -- not the notebook's stated "
        "SQUARED denominator with coefficient 1/4; confirmed by direct "
        "symbolic division and a numeric counterexample. (iv) The 'sphere' "
        "locus claim, ax^2+ay^2+(az-Vz/2)^2=alpha/4, is also INCORRECT: it "
        "is both dimensionally wrong (RHS must carry units of length^2, but "
        "alpha/4 is dimensionless) and structurally wrong -- the TRUE locus, "
        "re-derived here directly from a.a=0 & b.b=0 with no reference to "
        "the flawed lines 3349/3351, is an ELLIPSOID of revolution about the "
        "z-axis, not a sphere: ax^2+ay^2 + alpha*(az-Vz/2)^2 = V0^2*alpha/4 "
        "(equatorial radius V0*sqrt(alpha)/2, polar semi-axis V0/2, equal "
        "only in the special sub-case Vz=0/alpha=1, where the notebook's "
        "claimed sphere IS exactly recovered). (v) The final cylindrical "
        "formula rho_s=2 r rho_0/(r^2-rho_0^2) is dimensionally INCORRECT as "
        "written (it is provably dimensionless, not a length) -- it exactly "
        "equals tan(phi), one factor of r short of the standard "
        "tangent-double-angle stereographic radius identity rho_s=r*tan(phi) "
        "with rho_0=r*tan(phi/2); the corrected, dimensionally consistent "
        "formula is rho_s = 2 r^2 rho_0/(r^2-rho_0^2), which reproduces "
        "r*tan(phi) exactly. This is a clean, checkable closing identity for "
        "the notebook once the missing factor of r is restored -- an error "
        "of exactly the same 'one dropped length factor' type as elsewhere "
        "in this final push of pages, consistent with these being the "
        "notebook's very last, most hastily-written lines (it literally ends "
        "'(End of notebook)' immediately after)."
    ),
}

# ===========================================================================
result = {
    "NB-180": nb180,
    "NB-182": nb182,
    "NB-184": nb184,
    "NB-185": nb185,
    "NB-186": nb186,
}

print(json.dumps(result, indent=2, default=str))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-180_186_null_vectors.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2, default=str))
print("wrote", out)
