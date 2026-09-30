"""
NB-145-148 (pp.112-114) -- stereographic projection with a sphere of radius
1/2 centered at (0,0,1/2). Line from (0,0,1) through (alpha,beta,0),
parametrized (18a-c); intersection condition (19)/(20); t=(1+|zeta|^2)^-1
(21,23); projection formulas x,y,z(zeta,zeta*) (24a-c); inverse zeta=(x+iy)/(1-z)
(25); homogeneous/projective form (27a-c) using zeta=xi/eta.

Method: re-derive x,y,z from first principles for BOTH candidate spheres in
play on this page -- (A) the ACTUALLY-DESCRIBED radius-1/2 sphere centered at
(0,0,1/2), and (B) the standard textbook unit sphere (radius 1, centered at
the origin) -- and check which formula matches which, rather than assuming
the notebook's own formulas are self-consistent.
"""
import json
import sympy as sp

I = sp.I
alpha, beta, s = sp.symbols('alpha beta s', real=True)

# --- Ground truth (A): radius-1/2 sphere at (0,0,1/2), line from (0,0,1)
# through (alpha,beta,0), i.e. (18a-c) WITHOUT any extra 1/2 factor ---
xA = s*alpha
yA = s*beta
zA = 1 - s
sphere_A_eq = sp.expand(xA**2 + yA**2 + (zA - sp.Rational(1, 2))**2 - sp.Rational(1, 4))
sol_A = sp.solve(sp.Eq(sphere_A_eq, 0), s)
s_A = [x for x in sol_A if x != 0][0]
x_A, y_A, z_A = [sp.simplify(v.subs(s, s_A)) for v in (xA, yA, zA)]

notebook_eq21_t = 1/(alpha**2 + beta**2 + 1)
t_matches_eq21 = sp.simplify(s_A - notebook_eq21_t) == 0

# --- Ground truth (B): standard UNIT sphere at the origin, same line ---
xB = s*alpha
yB = s*beta
zB = 1 - s
sphere_B_eq = sp.expand(xB**2 + yB**2 + zB**2 - 1)
sol_B = sp.solve(sp.Eq(sphere_B_eq, 0), s)
s_B = [x for x in sol_B if x != 0][0]
x_B, y_B, z_B = [sp.simplify(v.subs(s, s_B)) for v in (xB, yB, zB)]

# --- Notebook's (18a) as LITERALLY transcribed (with the explicit 1/2 on x) ---
xC = sp.Rational(1, 2)*s*alpha
yC = s*beta
zC = 1 - s
sphere_C_eq = sp.expand(xC**2 + yC**2 + (zC - sp.Rational(1, 2))**2 - sp.Rational(1, 4))
sol_C = sp.solve(sp.Eq(sphere_C_eq, 0), s)

# --- Notebook's (24a-c), (27a-c) as literally transcribed ---
zeta, zetac = alpha + I*beta, alpha - I*beta
x_24a = sp.simplify((zeta + zetac) / (1 + zeta*zetac))
y_24b_as_written = sp.simplify((zeta - zetac) / (1 + zeta*zetac))       # missing i, as transcribed
y_24b_corrected = sp.simplify((zeta - zetac) / (I*(1 + zeta*zetac)))    # with the missing i restored
z_24c = sp.simplify((zeta*zetac) / (1 + zeta*zetac))

xi, eta_, xi_c, eta_c_ = sp.symbols('xi eta_ xi_c eta_c', complex=True)
x_27a = (xi*eta_c_ + eta_*xi_c) / (xi_c*xi + eta_*eta_c_)
y_27b = (xi*eta_c_ - eta_*xi_c) / (xi_c*xi + eta_*eta_c_)
z_27c = (xi*xi_c - eta_*eta_c_) / (xi_c*xi + eta_*eta_c_)
reduction_subs = {eta_: 1, eta_c_: 1, xi_c: sp.conjugate(xi)}
x_27a_at1 = sp.simplify(x_27a.subs(reduction_subs).subs(xi, alpha + I*beta))
y_27b_at1_as_written = sp.simplify(y_27b.subs(reduction_subs).subs(xi, alpha + I*beta))
y_27b_at1_corrected = sp.simplify(y_27b_at1_as_written / I)
z_27c_at1 = sp.simplify(z_27c.subs(reduction_subs).subs(xi, alpha + I*beta))

def ratio(expr, denom):
    return sp.simplify(expr/denom) if denom != 0 else None

comparisons = {
    "24a_vs_true_radius_half_x_A": ratio(x_24a, x_A),
    "24a_vs_unit_sphere_x_B": ratio(x_24a, x_B),
    "24b_corrected_vs_true_radius_half_y_A": ratio(y_24b_corrected, y_A),
    "24b_corrected_vs_unit_sphere_y_B": ratio(y_24b_corrected, y_B),
    "24c_vs_true_radius_half_z_A": ratio(z_24c, z_A),
    "24c_vs_unit_sphere_z_B": ratio(z_24c, z_B),
    "27a_vs_unit_sphere_x_B": ratio(x_27a_at1, x_B),
    "27b_corrected_vs_unit_sphere_y_B": ratio(y_27b_at1_corrected, y_B),
    "27c_vs_true_radius_half_z_A": ratio(z_27c_at1, z_A),
    "27c_vs_unit_sphere_z_B": ratio(z_27c_at1, z_B),
}

output = {
    "NB-145": {
        "claim": "line (18a-c) intersects the radius-1/2 sphere per (19), giving t=(alpha^2+beta^2+1)^-1 (21)",
        "18a_literal_(with_the_stated_1/2_factor_on_x)_solutions_for_t": [str(x) for x in sol_C],
        "18a_without_the_1/2_factor_solutions_for_s": [str(x) for x in sol_A],
        "matches_boxed_eq21_t=(alpha^2+beta^2+1)^-1": bool(t_matches_eq21),
        "conclusion": (
            "(18a)'s explicitly stated factor of 1/2 on x is itself the "
            "error: solving the actual radius-1/2 sphere equation with the "
            "line AS STATED IN WORDS (from (0,0,1) through (alpha,beta,0), "
            "i.e. x=alpha*t with NO 1/2) reproduces the boxed t=(alpha^2+"
            "beta^2+1)^-1 of eq (21) exactly; keeping the literal 1/2 factor "
            "instead gives a different, non-matching t. Eq (19)-(21) are "
            "self-consistent with each other and with the correct line "
            "parametrization; only (18a)'s explicit '1/2' is the odd one out."
        ),
        "verdict": "SOLID-WITH-CORRECTION",
    },
    "NB-146": {
        "claim": "x,y,z in terms of zeta,zeta* (24a-c), using t=(1+|zeta|^2)^-1",
        "comparison_ratios": {k: str(v) for k, v in comparisons.items() if k.startswith("24")},
        "conclusion": (
            "A precise, three-way split found: (24a) and (24b) (once its "
            "own separate, obviously-needed missing factor of i is restored "
            "-- (zeta-zetabar)=2i*beta is purely imaginary, so as literally "
            "transcribed (24b) cannot equal the real coordinate y at all) "
            "BOTH turn out to be EXACTLY TWICE the true radius-1/2-sphere "
            "x,y -- and exactly equal to the standard TEXTBOOK stereographic "
            "projection formula for a UNIT sphere (radius 1) centered at the "
            "ORIGIN instead (independently re-derived and confirmed here). "
            "(24c), in sharp contrast, exactly matches the TRUE radius-1/2 "
            "sphere z-coordinate (not the unit-sphere z, which differs from "
            "it). In other words: (24a)/(24b) use one sphere convention "
            "(the standard unit sphere, likely copied from memory/a "
            "reference rather than freshly derived) while (24c) uses a "
            "DIFFERENT, correct-for-this-page convention (the actual "
            "radius-1/2 sphere set up two paragraphs earlier) -- (24a-c) is "
            "an internally MIXED, inconsistent set, not merely a single "
            "typo."
        ),
        "verdict": "INCORRECT (as transcribed) / SOLID-WITH-CORRECTION",
    },
    "NB-147": {
        "claim": "zeta=(x+iy)/(1-z) inverts (24a-c)",
        "note": (
            "Checked directly against the TRUE radius-1/2 sphere coordinates "
            "(x_A,y_A,z_A): (x_A+iy_A)/(1-z_A) reduces exactly to "
            "zeta=alpha+i*beta, confirming this inverse formula is correct "
            "for the sphere actually described on the page -- independent "
            "of the (24a-c) mixed-convention issue found above, since the "
            "inverse map only needs the RATIO (x+iy)/(1-z), which turns out "
            "to be convention-independent under the specific x,y,z used "
            "(the same overall scale factor that makes (24a,b) 2x too big "
            "would cancel out of a homogeneous ratio like this one, though "
            "not out of (24a-c) themselves since they equal zeta directly, "
            "not a ratio)."
        ),
        "verified_against_true_radius_half_sphere": bool(
            sp.simplify(
                (x_A + I*y_A) / (1 - z_A) - (alpha + I*beta)
            ) == 0
        ),
        "verdict": "SOLID",
    },
    "NB-148": {
        "claim": "zeta=xi/eta (26); homogeneous/projective formulas (27a-c); scale ambiguity matches (14)",
        "comparison_ratios": {k: str(v) for k, v in comparisons.items() if k.startswith("27")},
        "scaling_invariance_under_(xi,eta)->(lambda xi,lambda eta)": bool(
            sp.simplify(
                x_27a.subs({xi: sp.Symbol('lam')*xi, eta_: sp.Symbol('lam')*eta_,
                            xi_c: sp.conjugate(sp.Symbol('lam'))*xi_c,
                            eta_c_: sp.conjugate(sp.Symbol('lam'))*eta_c_}) - x_27a
            ) == 0
        ),
        "conclusion": (
            "Unlike (24a-c), the projective triple (27a-c) is INTERNALLY "
            "CONSISTENT: at eta=1, all three of x,y (once (27b)'s own "
            "identical missing-i issue is corrected the same way as (24b)'s) "
            "and z exactly match the STANDARD UNIT SPHERE convention "
            "(confirmed independently re-derived above) -- none of the three "
            "matches the actual radius-1/2 sphere from earlier in the page. "
            "So (27a-c) is a self-consistent, correctly-executed formula for "
            "a DIFFERENT sphere than the one geometrically set up on pp.112-113; "
            "(24a-c) is internally inconsistent between its own three "
            "components. The scale-invariance under (xi,eta)->(lambda xi,"
            "lambda eta) is confirmed exactly regardless, correctly "
            "reproducing the spinor ambiguity of eq (14)."
        ),
        "verdict": "SOLID-WITH-CORRECTION",
    },
}

path = "test-results/notebook-recon/NB-145_148_stereographic_projection_half.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2, default=str)

print(json.dumps(output, indent=2, default=str))
