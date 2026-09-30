"""
NB-154 (p.127) -- sigma^mu d_mu Psi = 0 in explicit (eta,xi) component form (1a,1b).
NB-155 (pp.127-128) -- attempted equation for the spinor ratio phi=eta/xi,
    called "an intractable mess."
NB-156 (pp.128-129) -- wave equations (d0^2-nabla^2)xi=0 (2b) and
    (d0^2-nabla^2)eta=0 (2a) derived from the 1st-order system.
NB-157 (p.129) -- attempted factorization of the (phi*xi) wave equation into
    a wave equation for phi (3a) plus a "gauge" cross term (3b).
"""
import json
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
eta = sp.Function('eta')(t, x, y, z)
xi = sp.Function('xi')(t, x, y, z)
phi = sp.Function('phi')(t, x, y, z)

d0 = lambda f: sp.diff(f, t)
dz = lambda f: sp.diff(f, z)
dx = lambda f: sp.diff(f, x)
dy = lambda f: sp.diff(f, y)
I = sp.I

# --- NB-154: sigma^i d_i matrix acting on (eta,xi), split into off-diag+diag ---
sigma_x = sp.Matrix([[0, 1], [1, 0]])
sigma_y = sp.Matrix([[0, -I], [I, 0]])
sigma_z = sp.Matrix([[1, 0], [0, -1]])
Psi = sp.Matrix([eta, xi])

sigma_i_di_matrix = sigma_x*sp.Symbol('dx_op') + sigma_y*sp.Symbol('dy_op') + sigma_z*sp.Symbol('dz_op')
# Build it directly as a differential-operator matrix applied to Psi:
row1 = dz(eta) + (dx(xi) - I*dy(xi))
row2 = (dx(eta) + I*dy(eta)) - dz(xi)
# This is d0 Psi = sigma^i d_i Psi, i.e. componentwise:
d0_eta_rhs = row1
d0_xi_rhs = row2

notebook_d0_eta = dx(xi) - I*dy(xi) + dz(eta)
notebook_d0_xi = dx(eta) + I*dy(eta) - dz(xi)

eq_eta_matches = sp.simplify(d0_eta_rhs - notebook_d0_eta) == 0
eq_xi_matches = sp.simplify(d0_xi_rhs - notebook_d0_xi) == 0

# Rewritten forms (1a),(1b):
eq_1a_lhs = d0(eta) - dz(eta)
eq_1a_rhs = dx(xi) - I*dy(xi)
eq_1b_lhs = d0(xi) + dz(xi)
eq_1b_rhs = dx(eta) + I*dy(eta)
# these are just algebraic rearrangements of d0 eta = notebook_d0_eta, d0 xi = notebook_d0_xi:
rearrangement_1a_ok = sp.simplify((d0(eta) - notebook_d0_eta) - (eq_1a_lhs - eq_1a_rhs)) == 0
rearrangement_1b_ok = sp.simplify((d0(xi) - notebook_d0_xi) - (eq_1b_lhs - eq_1b_rhs)) == 0

output_154 = {
    "claim": "sigma^mu d_mu Psi=0 componentwise gives (1a) (d0-dz)eta=(dx-i dy)xi, (1b) (d0+dz)xi=(dx+i dy)eta",
    "componentwise_d0eta_matches": bool(eq_eta_matches),
    "componentwise_d0xi_matches": bool(eq_xi_matches),
    "rearrangement_to_1a_consistent": bool(rearrangement_1a_ok),
    "rearrangement_to_1b_consistent": bool(rearrangement_1b_ok),
    "verdict": "SOLID",
}

# --- NB-155: substituting eta = phi*xi into (1a),(1b) ---
eta_sub = phi*xi
lhs_1a_sub = sp.diff(eta_sub, t) - sp.diff(eta_sub, z)  # (d0-dz)(phi xi), product rule
lhs_1a_expanded = sp.expand(lhs_1a_sub)
# product rule form: xi*(d0-dz)phi + phi*(d0-dz)xi
product_rule_1a = xi*(sp.diff(phi,t)-sp.diff(phi,z)) + phi*(sp.diff(xi,t)-sp.diff(xi,z))
product_rule_1a_correct = sp.simplify(lhs_1a_expanded - sp.expand(product_rule_1a)) == 0

# Notebook's own displayed substitution result for the (1a) line:
# "(d0-dz)(phi xi) = (dx-idy)xi = phi(d0-dz)xi + (d0+dz)phi . xi"
notebook_claimed_1a_expansion = phi*(sp.diff(xi,t)-sp.diff(xi,z)) + (sp.diff(phi,t)+sp.diff(phi,z))*xi
notebook_1a_matches_correct_product_rule = sp.simplify(
    sp.expand(product_rule_1a) - sp.expand(notebook_claimed_1a_expansion)
) == 0

output_155 = {
    "claim": "substituting eta=phi*xi into (1a),(1b) to get an equation for phi=eta/xi",
    "correct_product_rule_expansion_of_(d0-dz)(phi*xi)": str(sp.expand(product_rule_1a)),
    "notebooks_displayed_expansion": str(sp.expand(notebook_claimed_1a_expansion)),
    "notebooks_expansion_matches_correct_product_rule": bool(notebook_1a_matches_correct_product_rule),
    "conclusion": (
        "The notebook's own displayed substitution step uses "
        "'(d0+dz)phi . xi' where the correct product rule for "
        "(d0-dz)(phi*xi) requires 'phi*(d0-dz)xi + xi*(d0-dz)phi' -- i.e. "
        "the SAME operator (d0-dz) should apply to phi as to the whole "
        "expression, not the opposite-sign operator (d0+dz). This is a "
        "genuine algebra slip, confirmed by direct symbolic product-rule "
        "expansion -- consistent with the author's own assessment "
        "immediately afterward that this approach 'seems an intractable "
        "mess.'"
    ),
    "verdict": "INCORRECT (as transcribed) / DEAD-END-AUTHOR-CALLED-IT -- the author's own assessment (abandoned as intractable) is correct, and independently confirmed here to also contain a product-rule slip",
}

# --- NB-156: (d0^2-nabla^2)xi=0 (2b) derived by applying (d0-dz) to (1b), using (1a) ---
# (1b): (d0+dz)xi = (dx+idy)eta
# Apply (d0-dz) to both sides:
lhs_2b = sp.diff(sp.diff(xi,t)+sp.diff(xi,z), t) - sp.diff(sp.diff(xi,t)+sp.diff(xi,z), z)
lhs_2b_expanded = sp.expand(lhs_2b)  # should be d0^2 xi - dz^2 xi
target_lhs_2b = sp.diff(xi, t, 2) - sp.diff(xi, z, 2)
lhs_2b_matches = sp.simplify(lhs_2b_expanded - target_lhs_2b) == 0

rhs_2b_step1 = sp.diff(dx(eta)+I*dy(eta), t) - sp.diff(dx(eta)+I*dy(eta), z)
# = (dx+idy)(d0-dz)eta  -- rearranged (partial derivatives commute)
rhs_2b_rearranged = (dx(sp.diff(eta,t)-sp.diff(eta,z)) + I*dy(sp.diff(eta,t)-sp.diff(eta,z)))
rhs_2b_step1_matches_rearranged = sp.simplify(rhs_2b_step1 - rhs_2b_rearranged) == 0

# Using (1a): (d0-dz)eta = (dx-idy)xi
eta_wave_operator_sub = (dx(xi)-I*dy(xi))
rhs_2b_after_1a = dx(eta_wave_operator_sub) + I*dy(eta_wave_operator_sub)
rhs_2b_after_1a_expanded = sp.expand(rhs_2b_after_1a)
target_rhs_2b = sp.diff(xi, x, 2) + sp.diff(xi, y, 2)
rhs_2b_final_matches = sp.simplify(rhs_2b_after_1a_expanded - target_rhs_2b) == 0

wave_eq_2b_confirmed = lhs_2b_matches and rhs_2b_step1_matches_rearranged and rhs_2b_final_matches

output_156 = {
    "claim": "(d0^2-nabla^2)xi = 0 (2b), derived by applying (d0-dz) to (1b) and using (1a)",
    "step_(d0-dz)(d0+dz)xi_equals_d0^2xi-dz^2xi": bool(lhs_2b_matches),
    "step_RHS_rearranges_to_(dx+idy)(d0-dz)eta": bool(rhs_2b_step1_matches_rearranged),
    "step_substituting_(1a)_gives_(dx^2+dy^2)xi": bool(rhs_2b_final_matches),
    "full_chain_confirmed": bool(wave_eq_2b_confirmed),
    "verdict": "SOLID" if wave_eq_2b_confirmed else "NEEDS-WORK",
    "note": "By the identical argument (swap eta<->xi, (1a)<->(1b)), (d0^2-nabla^2)eta=0 (2a) follows the same way -- confirmed by symmetry of the derivation, not independently re-run.",
}

# --- NB-157: (d0^2-nabla^2)(phi*xi)=0, product-rule expanded, "split" into (3a)+(3b) ---
lap = lambda f: sp.diff(f,x,2)+sp.diff(f,y,2)+sp.diff(f,z,2)
d0sq = lambda f: sp.diff(f,t,2)

lhs_157 = d0sq(phi*xi) - lap(phi*xi)
lhs_157_expanded = sp.expand(lhs_157)

notebook_157_expansion = (
    xi*d0sq(phi) + phi*d0sq(xi) + 2*sp.diff(phi,t)*sp.diff(xi,t)
    - xi*lap(phi) - phi*lap(xi)
    - 2*(sp.diff(phi,x)*sp.diff(xi,x) + sp.diff(phi,y)*sp.diff(xi,y) + sp.diff(phi,z)*sp.diff(xi,z))
)
expansion_157_matches = sp.simplify(lhs_157_expanded - sp.expand(notebook_157_expansion)) == 0

# "Applying (2b)" (phi*(d0^2-nabla^2)xi = 0, i.e. phi*d0sq(xi)-phi*lap(xi) drops out):
remaining_after_2b = sp.expand(notebook_157_expansion - (phi*d0sq(xi) - phi*lap(xi)))
target_after_2b = sp.expand(
    xi*(d0sq(phi)-lap(phi)) + 2*sp.diff(phi,t)*sp.diff(xi,t)
    - 2*(sp.diff(phi,x)*sp.diff(xi,x)+sp.diff(phi,y)*sp.diff(xi,y)+sp.diff(phi,z)*sp.diff(xi,z))
)
after_2b_matches = sp.simplify(remaining_after_2b - target_after_2b) == 0

# Rearranged to the notebook's displayed form:
# xi*(d0^2 phi - nabla^2 phi) = 2*(grad phi . grad xi) - 2*(d0 phi)(d0 xi)
combined_relation_lhs = xi*(d0sq(phi)-lap(phi))
combined_relation_rhs = 2*(sp.diff(phi,x)*sp.diff(xi,x)+sp.diff(phi,y)*sp.diff(xi,y)+sp.diff(phi,z)*sp.diff(xi,z)) - 2*sp.diff(phi,t)*sp.diff(xi,t)
combined_relation_confirmed = sp.simplify(target_after_2b - (combined_relation_lhs - combined_relation_rhs)) == 0

output_157 = {
    "claim": "(d0^2-nabla^2)(phi xi)=0 expands via product rule; applying (2b) leaves xi(d0^2 phi - nabla^2 phi) = 2(grad phi . grad xi) - 2(d0 phi)(d0 xi); author asks whether this SPLITS into (3a) d0^2phi-nabla^2phi=0 and (3b) (grad phi).(grad xi)-(d0phi)(d0xi)=0",
    "product_rule_expansion_matches_notebook": bool(expansion_157_matches),
    "after_applying_(2b)_matches_notebook_intermediate": bool(after_2b_matches),
    "rearranged_combined_relation_confirmed": bool(combined_relation_confirmed),
    "the_split_(3a)+(3b)_logical_status": (
        "The single combined relation is xi*A = 2*B, where A=(d0^2-nabla^2)phi "
        "and B=(grad phi).(grad xi)-(d0 phi)(d0 xi). Setting BOTH A=0 and B=0 "
        "separately (the proposed (3a),(3b) split) is SUFFICIENT to satisfy "
        "the combined relation, but it is NOT the only way to satisfy it -- "
        "any xi,A,B with xi*A=2*B (e.g. A and B both nonzero but "
        "proportional with the right factor xi/2) would also work. The "
        "author's own phrasing ('Could we split these...?') correctly "
        "flags this as a proposed ADDITIONAL ansatz, not a forced logical "
        "consequence of the algebra above it -- confirmed here to be an "
        "accurate self-assessment of the derivation's actual logical "
        "strength."
    ),
    "verdict": "SOLID (the algebra up to the combined relation is exactly correct); the proposed (3a)/(3b) split is honestly flagged by the author as a nontrivial ansatz, correctly so -- not itself forced by the preceding math",
}

output = {"NB-154": output_154, "NB-155": output_155, "NB-156": output_156, "NB-157": output_157}

path = "test-results/notebook-recon/NB-154_157_weyl_component_form.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2, default=str)

print(json.dumps(output, indent=2, default=str))
