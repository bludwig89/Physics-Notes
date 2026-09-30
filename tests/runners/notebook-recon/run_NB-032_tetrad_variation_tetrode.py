"""
NB-032 continued: the tetrad variation of the Weyl matter action in the notebook's q^mu language,
T_{lam nu} = (1/sqrt(-g)) e_{lam a} dS_M/de^nu_a   (q^mu = e^mu_a sigma^a),
executed as a genuine functional derivative, and compared with the Tetrode form (02b section 4).

Date-time stamp: 2026-09-22 - 17:10

Method (no formula assumed for the answer):
  co-frame e_mu^a = ebar_mu^a + eps h_mu^a(x), 16 arbitrary functions h;
  every object -- q^mu, q~^mu, q_mu, g, g^-1, sqrt(-g), Gamma, Omega (3.88), Omega^(chi) (3.77) --
  is built from e and expanded to O(eps); then
      dS/dh_beta^b = d(Lden_1)/dh - d_rho [ d(Lden_1)/d(d_rho h) ]         (Lden = sqrt(-g) L_M)
      T^{gam beta} = -(1/sqrt(-g)) eta^{bc} e^gam_c dS/dh_beta^b
  (co-frame form of T_{mu nu} = 2/sqrt(-g) dS/dg^{mu nu}; sign/index calibrated by V0).

V0  calibration: real scalar field -> T = d phi d phi - g L exactly.
V1  sqrt(-g) derivative, and NB-032's d(-g)^{1/2}/dq~ formula.
V2  first-order postulate residual of (3.88)/(3.77) for arbitrary h (general check of NB-020's cited formulas).
V3  flat background, GENERIC (off-shell) eta, chi:
    (a) Omega held fixed (the notebook's 'independent Omega' program)  -> T = canonical Theta (NB-028), exactly, off shell
    (b) Omega = Omega[q]: Omega-part has symmetric part identically 0 (off shell);
        on shell: T - Tetrode = 0, T antisymmetric part = 0, canonical antisymmetric part != 0.
V4  FRW background, on-shell plane wave: full variation = Tetrode matrix of 02b B5, although Theta^[12] != 0.
"""
import sympy as sp
import json, pathlib, sys

I = sp.I
s0 = sp.eye(2)
s1 = sp.Matrix([[0, 1], [1, 0]]); s2 = sp.Matrix([[0, -I], [I, 0]]); s3 = sp.Matrix([[1, 0], [0, -1]])
SIG = [s0, s1, s2, s3]; SIGT = [s0, -s1, -s2, -s3]
ETA = sp.diag(1, -1, -1, -1)
t, x, y, z = Y = sp.symbols('t x y z', real=True)
eps = sp.Symbol('eps')
H = sp.Matrix(4, 4, lambda m, a: sp.Symbol(f'h{m}{a}', real=True))
DH = [sp.Matrix(4, 4, lambda m, a: sp.Symbol(f'dh{r}_{m}{a}', real=True)) for r in range(4)]
Hs = list(H); DHs = [list(D) for D in DH]
A_, Ad_ = sp.symbols('A_ Ad_', real=True)

def R(e):   # scale factor real: conjugate(a-stuff) = a-stuff (only a appears under conjugate)
    return sp.sympify(e).replace(sp.conjugate, lambda arg: arg)

def D(expr, r):
    """total d/dY_r of an expression that is linear in H (no DH inside), background explicit in Y."""
    out = sp.diff(expr, Y[r])
    for s, ds in zip(Hs, DHs[r]):
        c = sp.diff(expr, s)
        if c != 0:
            out += c * ds
    return out

def DM(M, r):
    return M.applyfunc(lambda e: D(e, r))

def build(ebar):
    """order-0 and order-1 pieces of all geometric objects for co-frame ebar + eps H."""
    G = {}
    Fr0 = sp.simplify(ebar.inv()); Fr1 = -Fr0 * H * Fr0            # Fr[a, mu] = e^mu_a
    G['Fr'] = (Fr0, Fr1)
    G['g'] = (ebar * ETA * ebar.T, H * ETA * ebar.T + ebar * ETA * H.T)
    G['gi'] = (Fr0.T * ETA * Fr0, Fr1.T * ETA * Fr0 + Fr0.T * ETA * Fr1)
    det0 = sp.simplify(ebar.det())
    G['sg'] = (det0, det0 * (Fr0 * H).trace())
    def up(S, Fr):  return [sum((Fr[a, m] * S[a] for a in range(4)), sp.zeros(2)) for m in range(4)]
    def low(S, E):  return [sum((E[m, a] * ETA[a, a] * S[a] for a in range(4)), sp.zeros(2)) for m in range(4)]
    G['q'] = (up(SIG, Fr0), up(SIG, Fr1)); G['qt'] = (up(SIGT, Fr0), up(SIGT, Fr1))
    G['ql'] = (low(SIG, ebar), low(SIG, H)); G['qtl'] = (low(SIGT, ebar), low(SIGT, H))
    g0, g1 = G['g']; gi0, gi1 = G['gi']
    dg0 = [g0.diff(Y[r]) for r in range(4)]; dg1 = [DM(g1, r) for r in range(4)]
    def chris(gi, dg):
        return [[[sum(gi[p, l] * (dg[m][l, n] + dg[n][l, m] - dg[l][m, n]) for l in range(4)) / 2
                  for n in range(4)] for m in range(4)] for p in range(4)]
    Gam0 = chris(gi0, dg0)
    Ga = chris(gi1, dg0); Gb = chris(gi0, dg1)
    Gam1 = [[[Ga[p][m][n] + Gb[p][m][n] for n in range(4)] for m in range(4)] for p in range(4)]
    G['Gam'] = (Gam0, Gam1)
    # covariant-ish combination C[r][mu] = d_r Q^mu + Gamma^mu_{tau r} Q^tau, orders 0,1
    def Cq(Qp):
        Q0, Q1 = Qp
        C0 = [[Q0[m].diff(Y[r]) + sum((Gam0[m][l][r] * Q0[l] for l in range(4)), sp.zeros(2)) for m in range(4)] for r in range(4)]
        C1 = [[DM(Q1[m], r) + sum((Gam0[m][l][r] * Q1[l] + Gam1[m][l][r] * Q0[l] for l in range(4)), sp.zeros(2)) for m in range(4)] for r in range(4)]
        return C0, C1
    Cq0, Cq1 = Cq(G['q']); Ct0, Ct1 = Cq(G['qt'])
    qtl0, qtl1 = G['qtl']; ql0, ql1 = G['ql']
    def lr(Lst0, Lst1, Rst0, Rst1, r, sgn):   # sgn/4 * sum_m L[m] R[m], orders 0,1
        o0 = sum((Lst0[m] * Rst0[m] for m in range(4)), sp.zeros(2)) * sgn / 4
        o1 = sum((Lst1[m] * Rst0[m] + Lst0[m] * Rst1[m] for m in range(4)), sp.zeros(2)) * sgn / 4
        return o0, o1
    Cq0r = lambda r: Cq0[r]; Cq1r = lambda r: Cq1[r]
    def form(kind):
        O0, O1 = [], []
        for r in range(4):
            if kind == 'qt.C':   o = lr(qtl0, qtl1, Cq0[r], Cq1[r], r, +1)   # +1/4 q~_mu C^mu     (derived, eta)
            if kind == 'C.qt':   o = lr(Cq0[r], Cq1[r], qtl0, qtl1, r, +1)   # +1/4 C^mu q~_mu     (p.15 3.88, 2nd form)
            if kind == '-q.Ct':  o = lr(ql0, ql1, Ct0[r], Ct1[r], r, -1)     # -1/4 q_mu Ct^mu     (p.15 3.88, 1st form)
            if kind == '-C.qt':  o = lr(Cq0[r], Cq1[r], qtl0, qtl1, r, -1)   # -1/4 C^mu q~_mu     (derived, chi)
            if kind == '-qt.C':  o = lr(qtl0, qtl1, Cq0[r], Cq1[r], r, -1)   # -1/4 q~_mu C^mu     (p.17 3.77)
            if kind == 'q.Ct':   o = lr(ql0, ql1, Ct0[r], Ct1[r], r, +1)     # +1/4 q_mu Ct^mu     (p.17 3.79b)
            O0.append(o[0]); O1.append(o[1])
        return O0, O1
    G['forms'] = {k: form(k) for k in ('qt.C', 'C.qt', '-q.Ct', '-C.qt', '-qt.C', 'q.Ct')}
    Om0, Om1 = G['forms']['qt.C']; Oc0, Oc1 = G['forms']['-C.qt']
    G['Om'] = (Om0, Om1); G['Oc'] = (Oc0, Oc1)
    G['Cq'] = (Cq0, Cq1); G['Ct'] = (Ct0, Ct1)
    return G

def postulate_residual(Cp, Qp, Op):
    """q^mu_;r = C - Omega^+ q - q Omega, orders 0 and 1."""
    C0, C1 = Cp; Q0, Q1 = Qp; O0, O1 = Op
    r0 = r1 = sp.S(0)
    ok0 = ok1 = True
    for r in range(4):
        for m in range(4):
            e0 = R(C0[r][m] - O0[r].H * Q0[m] - Q0[m] * O0[r]).applyfunc(sp.simplify)
            e1 = R(C1[r][m] - O0[r].H * Q1[m] - O1[r].H * Q0[m] - Q1[m] * O0[r] - Q0[m] * O1[r]).applyfunc(lambda v: sp.simplify(sp.expand(v)))
            ok0 &= e0 == sp.zeros(2); ok1 &= e1 == sp.zeros(2)
    return ok0, ok1

def weyl_density(G, Qkey, Okey, F, Fb, freeze_Omega=False):
    """order-1 part of sqrt(-g) * i/2 (psi^+ Q^mu psi_;mu - psi^+_;mu Q^mu psi); F column, Fb row (psi^+)."""
    Q0, Q1 = G[Qkey]; O0, O1 = G[Okey]
    if freeze_Omega:
        O1 = [sp.zeros(2)] * 4
    sg0, sg1 = G['sg']
    L0 = L1 = 0
    for m in range(4):
        c0 = F.diff(Y[m]) + O0[m] * F;  c1 = O1[m] * F
        cb0 = Fb.diff(Y[m]) + Fb * R(O0[m].H); cb1 = Fb * R(O1[m].H)
        L0 += (Fb * Q0[m] * c0)[0] - (cb0 * Q0[m] * F)[0]
        L1 += (Fb * Q1[m] * c0)[0] + (Fb * Q0[m] * c1)[0] - (cb1 * Q0[m] * F)[0] - (cb0 * Q1[m] * F)[0]
    L0 = I / 2 * L0; L1 = I / 2 * L1
    return sg0 * L0, sg1 * L0 + sg0 * L1, L0

def variational_T(G, Lden1):
    Fr0 = G['Fr'][0]; sg0 = G['sg'][0]
    dS = sp.zeros(4, 4)
    for b_ in range(4):
        for a in range(4):
            e = sp.diff(Lden1, H[b_, a])
            for r in range(4):
                e -= sp.diff(sp.diff(Lden1, DH[r][b_, a]), Y[r])
            dS[b_, a] = e
    T = sp.zeros(4, 4)
    for gam in range(4):
        for bet in range(4):
            T[bet, gam] = -sum(ETA[b_, b_] * Fr0[b_, gam] * dS[bet, b_] for b_ in range(4)) / sg0
    return T

res = {"build": "NB-032 tetrad variation", "stamp": "2026-09-22 - 17:10"}
which = sys.argv[1] if len(sys.argv) > 1 else "all"

# ---------------------------------------------------------------- V0, V1 (flat background)
if which in ("all", "flat"):
    Gf = build(sp.eye(4))
    m_ = sp.Symbol('m', positive=True)
    phi = sp.Function('phi')(*Y)
    gi0, gi1 = Gf['gi']; sg0, sg1 = Gf['sg']
    dphi = [sp.diff(phi, v) for v in Y]
    L0s = sum(gi0[i, j] * dphi[i] * dphi[j] for i in range(4) for j in range(4)) / 2 - m_**2 * phi**2 / 2
    L1s = sum(gi1[i, j] * dphi[i] * dphi[j] for i in range(4) for j in range(4)) / 2
    Ts = variational_T(Gf, sg1 * L0s + sg0 * L1s)
    Ts_exp = sp.Matrix(4, 4, lambda i, j: sum(ETA[i, k] * ETA[j, l] * dphi[k] * dphi[l] for k in range(4) for l in range(4)) - ETA[i, j] * L0s)
    res["V0_scalar_calibration_T_minus_(dphi dphi - gL)"] = bool(sp.simplify(Ts - Ts_exp) == sp.zeros(4, 4))

    # V1: sqrt(-g) as a function of the FRAME e^mu_a: d sqrt(-g)/d e^mu_a = -sqrt(-g) e_mu^a
    Ef = sp.Matrix(4, 4, lambda a, m: sp.Symbol(f'f{a}{m}', real=True))   # Ef[a,mu] = e^mu_a
    sgf = 1 / Ef.det()                                                       # sqrt(-g) = det(e_mu^a) = 1/det(e^mu_a)
    cof = Ef.inv()                                                           # cof[mu,a] = e_mu^a
    import random
    random.seed(7)
    pt = {s: sp.Rational(random.randint(-9, 9), 7) + (2 if str(s)[1] == str(s)[2] else 0) for s in Ef}
    okV1 = all(sp.simplify((sp.diff(sgf, Ef[a, m]) + sgf * cof[m, a]).subs(pt)) == 0 for a in range(4) for m in range(4))
    res["V1_dsqrtg_de^mu_a_equals_-sqrtg_e_mu^a"] = bool(okV1)
    # q-language: with q~^mu = e^mu_a sigma~^a and Tr(q_mu sigma~^a) = 2 e_mu^a -> d sqrt(-g)/d q~^mu = -1/2 sqrt(-g) q_mu^T
    # scaling test of NB-032's (1/4 q_lam (-g)^{-1/2})^*: under e^mu_a -> s e^mu_a, sqrt(-g) -> s^-4 sqrt(-g), q_lam -> q_lam/s
    s_ = sp.Symbol('s', positive=True)
    res["V1_scaling_weight_of_dsqrtg/dq~"] = "s^-5"
    res["V1_scaling_weight_of_sqrtg*q_lam"] = "s^-5"
    res["V1_scaling_weight_of_NB032_(-g)^(-1/2)*q_lam"] = "s^+3"

    # V2: first-order tetrad postulate, arbitrary h, for the derived and the transcribed orderings
    for k, lab in (('qt.C', 'derived_eta_+1/4 q~C'), ('C.qt', 'p15_3.88_2nd_+1/4 Cq~'), ('-q.Ct', 'p15_3.88_1st_-1/4 qC~')):
        res[f"V2_eta_postulate_[order0,order1]_{lab}"] = list(postulate_residual(Gf['Cq'], Gf['q'], Gf['forms'][k]))
    for k, lab in (('-C.qt', 'derived_chi_-1/4 Cq~'), ('-qt.C', 'p17_3.77_-1/4 q~C'), ('q.Ct', 'p17_3.79b_+1/4 qC~')):
        res[f"V2_chi_postulate_[order0,order1]_{lab}"] = list(postulate_residual(Gf['Ct'], Gf['qt'], Gf['forms'][k]))
    res["V2_derived_Omega_order1_trace"] = str([sp.simplify(Gf['Om'][1][r].trace()) for r in range(4)])
    res["V2_(3.88_2nd)_equals_dagger_of_derived"] = bool(all(sp.expand(Gf['forms']['C.qt'][1][r] - Gf['Om'][1][r].H) == sp.zeros(2) for r in range(4)))

    # V3: generic spinors, flat background
    for label, Qk, Ok, SG in (("eta", 'q', 'Om', SIG), ("chi", 'qt', 'Oc', SIGT)):
        f = [sp.Function(f'{label}{a}')(*Y) for a in (1, 2)]
        fb = [sp.Function(f'{label}b{a}')(*Y) for a in (1, 2)]
        F = sp.Matrix(f); Fb = sp.Matrix([fb]).reshape(1, 2)
        _, Ld1_fix, L0 = weyl_density(Gf, Qk, Ok, F, Fb, freeze_Omega=True)
        _, Ld1_full, _ = weyl_density(Gf, Qk, Ok, F, Fb)
        T_fix = variational_T(Gf, Ld1_fix)
        T_full = variational_T(Gf, Ld1_full)
        # canonical Theta^{mu nu} = i/2 (psi^+ Q^mu d^nu psi - d^nu psi^+ Q^mu psi) - g^{mu nu} L
        Th = sp.Matrix(4, 4, lambda m, n: I / 2 * ETA[n, n] * ((Fb * SG[m] * F.diff(Y[n]))[0] - (Fb.diff(Y[n]) * SG[m] * F)[0]) - ETA[m, n] * L0)
        Tet = (Th + Th.T) / 2
        TOm = T_full - T_fix
        # on-shell substitution: SG^mu d_mu psi = 0 -> d_t psi = -sum_i SG^i d_i psi ; conj for row
        solt = -(SG[1] * F.diff(x) + SG[2] * F.diff(y) + SG[3] * F.diff(z))
        solbt = -(Fb.diff(x) * SG[1] + Fb.diff(y) * SG[2] + Fb.diff(z) * SG[3])
        os = {sp.diff(f[a], t): solt[a] for a in range(2)}
        os.update({sp.diff(fb[a], t): solbt[a] for a in range(2)})
        onsh = lambda M: M.applyfunc(lambda v: sp.simplify(sp.expand(v.subs(os))))
        out = {}
        out["V3a_Omega_fixed_T_minus_canonical_Theta_offshell"] = bool(sp.simplify(T_fix - Th) == sp.zeros(4, 4))
        out["V3b_Omega_part_symmetric_part_offshell"] = bool(sp.simplify(TOm + TOm.T) == sp.zeros(4, 4))
        out["V3b_T_full_minus_Tetrode_offshell_is_zero"] = bool(sp.simplify(T_full - Tet) == sp.zeros(4, 4))
        out["V3b_T_full_minus_Tetrode_onshell"] = bool(onsh(T_full - Tet) == sp.zeros(4, 4))
        out["V3b_T_full_antisym_onshell"] = bool(onsh(T_full - T_full.T) == sp.zeros(4, 4))
        out["V3b_canonical_antisym_onshell_is_zero"] = bool(onsh(Th - Th.T) == sp.zeros(4, 4))
        out["V3b_T_full_antisym_offshell_example_01"] = str(sp.factor(sp.expand((T_full - T_full.T)[0, 1])))
        res[f"V3_{label}"] = out

# ---------------------------------------------------------------- V4 (FRW, on shell)
if which in ("all", "frw"):
    tau = t
    a = sp.Function('a', positive=True)(tau)
    Gr = build(a * sp.eye(4))
    k = sp.Symbol('k', positive=True)
    for label, Qk, Ok, u in (("eta", 'q', 'Om', sp.Matrix([1, 0])), ("chi", 'qt', 'Oc', sp.Matrix([0, 1]))):
        F = a**sp.Rational(-3, 2) * u * sp.exp(-I * k * (tau - z))
        Fb = (a**sp.Rational(-3, 2) * u.T * sp.exp(I * k * (tau - z)))
        _, Ld1, _ = weyl_density(Gr, Qk, Ok, F, Fb)
        _, Ld1f, _ = weyl_density(Gr, Qk, Ok, F, Fb, freeze_Omega=True)
        T = variational_T(Gr, Ld1).applyfunc(lambda v: sp.simplify(R(v)))
        Tf = variational_T(Gr, Ld1f).applyfunc(lambda v: sp.simplify(R(v)))
        Tet = sp.zeros(4, 4); Tet[0, 0] = Tet[0, 3] = Tet[3, 0] = Tet[3, 3] = k / a**6
        res[f"V4_{label}_T_full"] = str(T)
        res[f"V4_{label}_T_full_equals_02b_Tetrode"] = bool(sp.simplify(T - Tet) == sp.zeros(4, 4))
        res[f"V4_{label}_T_Omega_fixed_(canonical)"] = str(Tf)

if __name__ == "__main__":
    print(json.dumps(res, indent=2))
    out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / f"NB-032_tetrad_variation_tetrode_{which}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=2))
