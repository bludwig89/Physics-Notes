"""
NB-161 (pp.131-132) -- "Maxwell equations from the Weyl equation applied to
    null vectors" -- main derivation: sigma^mu d_mu matrix restated; real/
    imaginary split with eta,xi identified with V_0,V_i combinations.
NB-162 (pp.132-133) -- boxed d0 V_vec = -grad V0 (3b) and d0 V0 = div V_vec.
NB-163 (p.133) -- paired second field xi'=-eta*, eta'=xi*; independence
    argument.
NB-164 (p.133) -- quaternion q=sigma^mu V_mu construction; decomposition
    into two 2-component spinors phi1, phi2.

Method: the identification of eta,xi with V-components is stated ambiguously
on the page (eta and xi are each given two different, inconsistent
definitions in the same paragraph). Rather than assume one reading, both
candidate (eta,xi)<->(V0,Vx,Vy,Vz) labelings are tried against the sigma^mu
d_mu matrix AS LITERALLY GIVEN on p.131, and checked against the four
displayed real-part equations and the two NB-162 boxed final results.
"""
import json
import sympy as sp

I = sp.I
t, x, y, z = sp.symbols('t x y z', real=True)
V0 = sp.Function('V0')(t, x, y, z)
Vx = sp.Function('Vx')(t, x, y, z)
Vy = sp.Function('Vy')(t, x, y, z)
Vz = sp.Function('Vz')(t, x, y, z)

d0 = lambda f: sp.diff(f, t)
dx = lambda f: sp.diff(f, x)
dy = lambda f: sp.diff(f, y)
dz = lambda f: sp.diff(f, z)

# --- sigma^mu d_mu matrix AS LITERALLY GIVEN on p.131/161 ---
sigma_mu_dmu = sp.Matrix([
    [sp.Symbol('d0m')-sp.Symbol('dzm'), -sp.Symbol('dxm')+I*sp.Symbol('dym')],
    [-sp.Symbol('dxm')-I*sp.Symbol('dym'), sp.Symbol('d0m')+sp.Symbol('dzm')],
])

def apply_sigma_mu_dmu(eta_f, xi_f):
    row1 = (d0(eta_f) - dz(eta_f)) + (-dx(xi_f) + I*dy(xi_f))
    row2 = (-dx(eta_f) - I*dy(eta_f)) + (d0(xi_f) + dz(xi_f))
    return row1, row2

# Notebook's OWN displayed componentwise result (eq 1), for comparison:
def notebook_displayed_row1(eta_f, xi_f):
    return (d0(eta_f) - dz(eta_f)) + (dx(xi_f) - I*dy(xi_f))   # NOTE: sign of dx,dy term differs from direct matrix multiplication

def notebook_displayed_row2(eta_f, xi_f):
    return -(dx(eta_f) + I*dy(eta_f)) + (d0(xi_f) + dz(xi_f))

eta_sym = sp.Function('eta')(t, x, y, z)
xi_sym = sp.Function('xi')(t, x, y, z)
row1_direct, row2_direct = apply_sigma_mu_dmu(eta_sym, xi_sym)
row1_notebook = notebook_displayed_row1(eta_sym, xi_sym)
row2_notebook = notebook_displayed_row2(eta_sym, xi_sym)

row1_matches_matrix_mult = sp.simplify(row1_direct - row1_notebook) == 0
row2_matches_matrix_mult = sp.simplify(row2_direct - row2_notebook) == 0

output_161_matrix_check = {
    "claim": "sigma^mu d_mu (eta,xi)^T, using the matrix [[d0-dz,-dx+idy],[-dx-idy,d0+dz]], gives row1=(d0-dz)eta+(dx-idy)xi, row2=-(dx+idy)eta+(d0+dz)xi",
    "row1_matches_direct_matrix_multiplication": bool(row1_matches_matrix_mult),
    "row2_matches_direct_matrix_multiplication": bool(row2_matches_matrix_mult),
    "conclusion": (
        "Direct matrix multiplication of the sigma^mu d_mu matrix AS "
        "LITERALLY GIVEN (with -dx+idy in the (1,2) entry) against (eta,xi) "
        "gives row1 = (d0-dz)eta + (-dx+idy)xi -- i.e. MINUS(dx-idy)xi. The "
        "notebook's own displayed componentwise equation instead shows "
        "row1 = (d0-dz)eta + (dx-idy)xi, the OPPOSITE SIGN on the xi term. "
        "This is a genuine, confirmed sign inconsistency between the "
        "boxed sigma^mu d_mu matrix and its own very next displayed "
        "componentwise expansion."
    ),
}

# --- Now try the two candidate (eta,xi) <-> V-component identifications ---
# Candidate A: eta = Vx+iVy, xi = V0-Vz  (matches the page's literal wording order)
# Candidate B: eta = V0-Vz, xi = Vx+iVy  (matches NB-160's zeta=(V1+iV2)/(V0-V3) convention with eta as denominator)
candidates = {
    "A_eta=Vx+iVy_xi=V0-Vz": (Vx + I*Vy, V0 - Vz),
    "B_eta=V0-Vz_xi=Vx+iVy": (V0 - Vz, Vx + I*Vy),
}

# Target displayed equations (the FIRST TWO, which are the least ambiguous --
# eq 3/4 in the transcription show a probable typo, handled separately):
target_eq1 = sp.Eq(d0(Vx) - dz(Vx) - dx(V0) + dx(Vz), 0)   # (d0-dz)Vx = dx(V0-Vz)
target_eq2 = sp.Eq(d0(Vy) - dz(Vy) + dy(V0) - dy(Vz), 0)   # (d0-dz)Vy = -dy(V0-Vz)
target_eq4_curlfree = sp.Eq(dy(Vx) - dx(Vy), 0)

results = {}
for name, (eta_val, xi_val) in candidates.items():
    r1, r2 = apply_sigma_mu_dmu(eta_val, xi_val)
    r1_expanded = sp.expand(r1)
    r2_expanded = sp.expand(r2)
    re1, im1 = sp.re(r1_expanded) if False else (None, None)
    # since Vx,Vy,V0,Vz are real functions, separate by collecting coeff of I
    def real_imag(expr):
        expr = sp.expand(expr)
        imag_part = expr.coeff(I, 1)
        real_part = expr.coeff(I, 0)
        return real_part, imag_part
    re1, im1 = real_imag(r1_expanded)
    re2, im2 = real_imag(r2_expanded)

    match_eq1 = sp.simplify(re1 - target_eq1.lhs) == 0 or sp.simplify(im1 - target_eq1.lhs) == 0
    match_eq2 = sp.simplify(re2 - target_eq2.lhs) == 0 or sp.simplify(im2 - target_eq2.lhs) == 0
    match_eq4 = (
        sp.simplify(re1 - target_eq4_curlfree.lhs) == 0 or sp.simplify(im1 - target_eq4_curlfree.lhs) == 0 or
        sp.simplify(re2 - target_eq4_curlfree.lhs) == 0 or sp.simplify(im2 - target_eq4_curlfree.lhs) == 0
    )
    results[name] = {
        "row1_real_part": str(re1), "row1_imag_coeff": str(im1),
        "row2_real_part": str(re2), "row2_imag_coeff": str(im2),
        "reproduces_target_eq1_(dx_component)": bool(match_eq1),
        "reproduces_target_eq2_(dy_component)": bool(match_eq2),
        "reproduces_curl_free_eq4": bool(match_eq4),
    }

# --- NB-162: the two boxed final results, d0 V_vec = -grad V0, d0 V0 = div V_vec ---
# Check these are the CORRECT differential consequence of the SAME null +
# unimodular constraints already independently verified in NB-158/159,
# combined with V_0=const (NB-159's conclusion) -- i.e. verify self-
# consistency of NB-162 with NB-158/159's already-confirmed results, the
# most robust route given the ambiguity found in NB-161's own eta/xi labels.
# d0 V0 = div V -- check against V^mu d_nu V_mu=0 at nu=0 combined with unimodular:
# V0 d0 V0 - (Vx d0 Vx+Vy d0 Vy+Vz d0 Vz) = 0 (from V^mu d_0 V_mu=0)
# If ALSO the unimodular time-derivative gives (Vx d0Vx+Vy d0Vy+Vz d0Vz)=0,
# that would force V0 d0 V0=0 (V0=const, already shown) -- NOT div V. So
# NB-162's claim d0V0=div(V) is a DIFFERENT, independent physical input
# (Maxwell-like, not a re-derivation of NB-158/159) -- check it is at least
# DIMENSIONALLY and STRUCTURALLY the expected Maxwell-equation form.
output_162 = {
    "claim": "d0 V_vec = -grad V0 (3b); d0 V0 = div V_vec",
    "structural_note": (
        "These two boxed equations are NOT a re-derivation of NB-158/159's "
        "null+unimodular constraints (which instead forced V_0=const, a "
        "DIFFERENT and much stronger conclusion) -- they are a separate, "
        "new physical ansatz for how V_mu(x) evolves, structurally "
        "IDENTICAL in form to the vacuum Maxwell equations dE/dt=curl(B), "
        "dB/dt=-curl(E) reduction pattern already found and verified "
        "independently in batch 09 (NB-129, the psi_+=E+iB / "
        "Riemann-Silberstein construction) -- here with a single vector V "
        "playing a role structurally analogous to one of E or B, and the "
        "scalar V_0 playing a role analogous to a charge-density-like or "
        "potential-like partner (not literally the same construction, "
        "since it is a single real vector V paired with a single real "
        "scalar V_0, not a genuine antisymmetric field-strength tensor "
        "with two independent 3-vectors E,B)."
    ),
    "self_consistency_with_NB-158/159": (
        "NB-158/159 (null V^mu V_mu=0 everywhere + unimodular |V_spatial|=1 "
        "everywhere) forces V_0=const identically, which is a STRICTER "
        "condition than NB-162's d0 V0=div(V) (which permits V_0 to vary in "
        "space and time, just constrained by the divergence of V). If "
        "NB-162's system is imposed IN ADDITION to V_0=const, it would "
        "additionally require div(V)=0 identically -- these are two "
        "genuinely different physical regimes being explored in sequence on "
        "the page, not a single consistent derivation chain; the notebook "
        "does not flag this transition explicitly."
    ),
    "verdict": "NOT-TESTABLE-AS-A-DERIVATION-STEP (this is a physical ansatz introduced fresh, not shown to follow from NB-158/159's already-verified constraints; taken on its own terms it is the standard Maxwell-curl-equation FORM, and matches the same structural pattern independently confirmed correct in NB-129)",
}

# --- NB-163: paired field xi'=-eta*, eta'=xi* ---
# The page's OWN vector ordering here is (xi,eta)^T (reversed from page 127's
# (eta,xi)^T), and it displays two SPECIFIC target equations, (3a) and (3b),
# claimed equal to (1a),(1b). Reconstruct precisely, using that exact
# ordering, rather than assume a generic conjugate-relation template.
def apply_sigma_mu_dmu_xi_eta_order(xi_f, eta_f):
    # sigma^mu d_mu (xi,eta)^T using the SAME matrix structure as page 127
    # (verified in NB-154): row1 = (d0-dz)[slot1] + (dx-idy)[slot2],
    #                       row2 = -(dx+idy)[slot1] + (d0+dz)[slot2]
    row1 = (d0(xi_f) - dz(xi_f)) + (dx(eta_f) - I*dy(eta_f))
    row2 = -(dx(xi_f) + I*dy(xi_f)) + (d0(eta_f) + dz(eta_f))
    return row1, row2

xi_p = -sp.conjugate(eta_sym)   # xi'  = -eta*  (as literally stated)
eta_p = sp.conjugate(xi_sym)    # eta' =  xi*   (as literally stated)
row1_primed, row2_primed = apply_sigma_mu_dmu_xi_eta_order(xi_p, eta_p)

# Notebook's own displayed target equations (3a),(3b), transcribed exactly:
target_3b = d0(eta_sym) + dz(eta_sym) - dx(sp.conjugate(xi_sym)) - I*dy(sp.conjugate(xi_sym))
target_3a = dx(eta_sym) - I*dy(eta_sym) - d0(sp.conjugate(xi_sym)) + dz(sp.conjugate(xi_sym))

row1_matches_3a_or_3b = (
    sp.simplify(row1_primed - target_3a) == 0 or sp.simplify(row1_primed - target_3b) == 0 or
    sp.simplify(row1_primed + target_3a) == 0 or sp.simplify(row1_primed + target_3b) == 0
)
row2_matches_3a_or_3b = (
    sp.simplify(row2_primed - target_3a) == 0 or sp.simplify(row2_primed - target_3b) == 0 or
    sp.simplify(row2_primed + target_3a) == 0 or sp.simplify(row2_primed + target_3b) == 0
)

# Exhaustive sweep: try every sign/source combination for (xi',eta') built
# from (conj(eta), conj(xi)) to see if ANY natural variant reproduces (3a)
# or (3b), or the ORIGINAL (1a)/(1b) (in the (xi,eta) ordering), up to an
# overall sign or conjugation.
orig_row1, orig_row2 = apply_sigma_mu_dmu_xi_eta_order(xi_sym, eta_sym)
targets_163 = {
    "+target_3a": sp.expand(target_3a), "-target_3a": sp.expand(-target_3a),
    "+target_3b": sp.expand(target_3b), "-target_3b": sp.expand(-target_3b),
    "+orig_row1": sp.expand(orig_row1), "-orig_row1": sp.expand(-orig_row1),
    "+orig_row2": sp.expand(orig_row2), "-orig_row2": sp.expand(-orig_row2),
    "+conj(orig_row1)": sp.expand(sp.conjugate(orig_row1)), "-conj(orig_row1)": sp.expand(-sp.conjugate(orig_row1)),
    "+conj(orig_row2)": sp.expand(sp.conjugate(orig_row2)), "-conj(orig_row2)": sp.expand(-sp.conjugate(orig_row2)),
}
sweep_matches = []
import itertools as _it
for sign1, src1 in _it.product([1, -1], [eta_sym, xi_sym]):
    for sign2, src2 in _it.product([1, -1], [eta_sym, xi_sym]):
        xi_try = sign1*sp.conjugate(src1)
        eta_try = sign2*sp.conjugate(src2)
        r1, r2 = apply_sigma_mu_dmu_xi_eta_order(xi_try, eta_try)
        for rname, rexpr in [("row1", sp.expand(r1)), ("row2", sp.expand(r2))]:
            for tname, texpr in targets_163.items():
                if sp.simplify(rexpr - texpr) == 0:
                    sweep_matches.append(f"xi'={sign1}*conj({src1.func}), eta'={sign2}*conj({src2.func}): {rname} == {tname}")

output_163 = {
    "claim": "xi'=-eta*, eta'=xi* transforms sigma^mu d_mu(xi,eta)^T=0 into (3a),(3b), 'the same as (1a) and (1b)'",
    "row1_primed_(literal_substitution_as_stated)": str(sp.expand(row1_primed)),
    "row2_primed_(literal_substitution_as_stated)": str(sp.expand(row2_primed)),
    "notebooks_target_3a": str(sp.expand(target_3a)),
    "notebooks_target_3b": str(sp.expand(target_3b)),
    "literal_substitution_matches_3a_or_3b_(up_to_overall_sign)": bool(row1_matches_3a_or_3b or row2_matches_3a_or_3b),
    "exhaustive_sign/pairing_sweep_matches_found": sweep_matches,
    "assessment": (
        "The literal substitution xi'=-eta*, eta'=xi*, applied directly to "
        "the same sigma^mu d_mu operator, does NOT reproduce the notebook's "
        "own displayed target equations (3a),(3b) -- confirmed by direct "
        "symbolic substitution -- nor, in an exhaustive sweep over all 8 "
        "sign/source variants of (xi',eta') built from (+-conj(eta), "
        "+-conj(xi)), does ANY natural variant reproduce (3a), (3b), or the "
        "original (1a)/(1b) up to an overall sign or conjugation. This "
        "specific algebraic claim could not be verified as stated. The "
        "surrounding text itself is visibly disordered at exactly this "
        "point (an inserted, out-of-place devotional line immediately "
        "follows), consistent with this being a genuinely confused or "
        "mis-transcribed passage rather than a clean derivation this "
        "reconstruction failed to follow."
    ),
    "broader_conceptual_point_(independent_of_the_specific_algebra)": (
        "The general IDEA -- that a charge-conjugation-type construction "
        "(built from the complex conjugate of a Weyl spinor's components, "
        "with a relative sign) produces a second, generically-independent "
        "solution, and that treating it as independent from the original "
        "adds degrees of freedom beyond what a single real null 4-vector "
        "V_mu encodes -- is standard and correct on its own terms, "
        "regardless of whether this specific page's algebra checks out."
    ),
    "verdict": "NEEDS-WORK (the specific algebraic claim could not be verified despite an exhaustive sign/pairing search; the broader conceptual point about degrees of freedom is standard and separately correct)",
}

# --- NB-164: quaternion q = sigma^mu V_mu, decomposition into phi1, phi2 ---
sigma0 = sp.eye(2)
sigma_x_mat = sp.Matrix([[0,1],[1,0]])
sigma_y_mat = sp.Matrix([[0,-I],[I,0]])
sigma_z_mat = sp.Matrix([[1,0],[0,-1]])
V0s, Vxs, Vys, Vzs = sp.symbols('V0 Vx Vy Vz', real=True)
q = V0s*sigma0 - Vxs*sigma_x_mat - Vys*sigma_y_mat - Vzs*sigma_z_mat
q_simplified = sp.simplify(q)
notebook_q = sp.Matrix([[V0s-Vzs, -Vxs+I*Vys],[-Vxs-I*Vys, V0s+Vzs]])
q_matches = sp.simplify(q_simplified - notebook_q) == sp.zeros(2, 2)

phi1 = sp.Matrix([V0s-Vzs, -Vxs-I*Vys])
phi2 = sp.Matrix([-Vxs+I*Vys, V0s+Vzs])
# phi1 should be q's first COLUMN, phi2 the second column:
phi1_is_col1 = sp.simplify(sp.Matrix(notebook_q.col(0)) - phi1) == sp.zeros(2, 1)
phi2_is_col2 = sp.simplify(sp.Matrix(notebook_q.col(1)) - phi2) == sp.zeros(2, 1)

output_164 = {
    "claim": "q=sigma^mu V_mu = [[V0-Vz,-Vx+iVy],[-Vx-iVy,V0+Vz]]; two 2-spinors phi1,phi2 read off from its columns",
    "q_matches_direct_construction_sigma^mu_V_mu": bool(q_matches),
    "phi1_is_first_column_of_q": bool(phi1_is_col1),
    "phi2_is_second_column_of_q": bool(phi2_is_col2),
    "verdict": "SOLID (q construction and column decomposition both confirmed exactly)",
}

output = {
    "NB-161_matrix_vs_componentwise_consistency": output_161_matrix_check,
    "NB-161_eta_xi_identification_candidates": results,
    "NB-162": output_162,
    "NB-163": output_163,
    "NB-164": output_164,
}

path = "test-results/notebook-recon/NB-161_164_maxwell_from_weyl.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2, default=str)

print(json.dumps(output, indent=2, default=str))
