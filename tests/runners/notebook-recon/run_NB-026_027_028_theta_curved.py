"""
NB-026/027/028 (pp.20-21): the matter energy-momentum tensor Theta^{mu nu} for the two massless
2-spinors eta (q^mu) and chi (q~^mu), flat (NB-026/027) and covariant (NB-028).

Date-time stamp: 2026-09-22 - 16:20

Part A (flat, q^mu = sigma^mu, q~^mu = sigma~^mu, g = diag(1,-1,-1,-1)):
  A1  canonical Theta from the notebook's own symmetrized L_M (p.20) vs the notebook's written
      result -- is the '+ (d^nu eta^+) q^mu eta' sign right?
  A2  L_M vanishes on shell (justifies dropping -g^{mu nu} L).
  A3  Legendre transform H = pi_eta d0 eta + d0 eta^+ pi_eta^+ - L equals corrected Theta^00.
  A4  plane-wave energy: notebook form vs corrected form.
Part B (curved, NB-028): spatially flat FRW in conformal time, g = a(tau)^2 eta, tetrad
  q^mu = sigma^mu / a, q~^mu = sigma~^mu / a.
  B1  metric identity 1/2(q^mu q~^nu + q^nu q~^mu) = g^{mu nu} I.
  B2  spin connection Omega_rho SOLVED from the tetrad postulate
      q^mu_{;rho} = d_rho q^mu + Gamma^mu_{rho lam} q^lam - Omega_rho^+ q^mu - q^mu Omega_rho = 0
      (the unique Leibniz-consistent rule given eta_{;mu} = d_mu eta + Omega_mu eta, p.17);
      compared with the notebook's cited Sachs (3.77) form.
  B3  Leibniz identity  d_mu(sqrt(-g) eta^+ q^mu eta) = sqrt(-g)(eta^+_{;mu} q^mu eta + eta^+ q^mu eta_{;mu})
      for arbitrary eta (off shell).
  B4  on-shell solution eta = a^{-3/2} u exp(-ik(tau - z)) of q^mu eta_{;mu} = 0.
  B5  corrected NB-028 tensor: reality, L_M = 0 on shell, symmetric part T^{mu nu}:
      covariant conservation, tracelessness, radiation scaling rho ~ a^{-4}.
  B6  same for the chi sector (q~^mu, Omega^(chi)).
  B7  the notebook's as-written NB-028 Theta^00.
"""
import sympy as sp
import json, pathlib

I = sp.I
s0 = sp.eye(2)
s1 = sp.Matrix([[0, 1], [1, 0]])
s2 = sp.Matrix([[0, -I], [I, 0]])
s3 = sp.Matrix([[1, 0], [0, -1]])
sig = [s0, s1, s2, s3]
sigt = [s0, -s1, -s2, -s3]
eta_m = sp.diag(1, -1, -1, -1)

def R(expr):
    """a(tau) is real: conjugate of a and its derivatives is itself (only a appears under conjugate)."""
    return sp.simplify(sp.sympify(expr).replace(sp.conjugate, lambda arg: arg))

res = {"build": "NB-026/027/028", "stamp": "2026-09-22 - 16:20"}

# ------------------------------------------------------------------ Part A (flat)
t, x, y, z = X = sp.symbols('t x y z', real=True)
e = [sp.Function(f'e{a}')(*X) for a in (1, 2)]      # eta components
eb = [sp.Function(f'eb{a}')(*X) for a in (1, 2)]    # eta^* components, formally independent
E = sp.Matrix(e); Eb = sp.Matrix(eb)
dE = [[sp.diff(c, v) for v in X] for c in e]
dEb = [[sp.diff(c, v) for v in X] for c in eb]

def Lflat(q):
    L = 0
    for m in range(4):
        L += (Eb.T * q[m] * E.diff(X[m]))[0] - (Eb.diff(X[m]).T * q[m] * E)[0]
    return sp.expand(I / 2 * L)

def canonical_theta(L, q):
    th = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            val = 0
            for a in range(2):
                up_n = eta_m[n, n]
                val += sp.diff(L, dE[a][m]) * up_n * dE[a][n]
                val += up_n * dEb[a][n] * sp.diff(L, dEb[a][m])
            th[m, n] = sp.expand(val - eta_m[m, n] * L)
    return th

Lf = Lflat(sig)
Th = canonical_theta(Lf, sig)
# notebook's written flat result (p.20, last line): i/2 (eta^+ q^mu d^nu eta + (d^nu eta^+) q^mu eta)
Th_nb = sp.zeros(4, 4)
Th_corr = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        up = eta_m[n, n]
        A = (Eb.T * sig[m] * E.diff(X[n]))[0] * up
        B = (Eb.diff(X[n]).T * sig[m] * E)[0] * up
        Th_nb[m, n] = sp.expand(I / 2 * (A + B))
        Th_corr[m, n] = sp.expand(I / 2 * (A - B))
res["A1_canonical_minus_(corrected_form - g L)_is_zero"] = bool(
    sp.simplify(Th - (Th_corr - eta_m * Lf)) == sp.zeros(4, 4))
res["A1_canonical_minus_(notebook_form - g L)_is_zero"] = bool(
    sp.simplify(Th - (Th_nb - eta_m * Lf)) == sp.zeros(4, 4))
res["A1_difference_notebook_minus_canonical_00"] = str(sp.factor(Th_nb[0, 0] - Th[0, 0] - Lf))
# A2: on shell, sigma^mu d_mu eta = 0 and its conjugate: d_t eta = -sigma.grad eta
sol_t = -(s1 * E.diff(x) + s2 * E.diff(y) + s3 * E.diff(z))
sol_tb = -(s1.conjugate() * Eb.diff(x) + s2.conjugate() * Eb.diff(y) + s3.conjugate() * Eb.diff(z))
subs_os = {sp.diff(e[a], t): sol_t[a] for a in range(2)}
subs_os.update({sp.diff(eb[a], t): sol_tb[a] for a in range(2)})
res["A2_L_M_on_shell"] = str(sp.simplify(Lf.subs(subs_os)))
# A3: Legendre
H = sum(sp.diff(Lf, dE[a][0]) * dE[a][0] + dEb[a][0] * sp.diff(Lf, dEb[a][0]) for a in range(2)) - Lf
res["A3_Legendre_H_minus_corrected_Theta00_(with -gL)"] = str(sp.simplify(H - Th[0, 0]))
res["A3_notebook_Theta00_equals_i/2_d0(eta^+eta)"] = bool(
    sp.simplify(Th_nb[0, 0] - I / 2 * sp.diff((Eb.T * E)[0], t)) == 0)
# A4: plane wave, positive helicity along z, omega = k
k = sp.symbols('k', positive=True)
pw = {e[0]: sp.exp(-I * k * (t - z)), e[1]: 0, eb[0]: sp.exp(I * k * (t - z)), eb[1]: 0}
def on_pw(expr):
    return sp.simplify(expr.subs(pw).doit())
res["A4_plane_wave_is_solution"] = str(on_pw((sig[0] * E.diff(t) + s3 * E.diff(z))[0]))
res["A4_notebook_Theta00_plane_wave"] = str(on_pw(Th_nb[0, 0]))
res["A4_corrected_Theta00_plane_wave"] = str(on_pw(Th_corr[0, 0]))

# ------------------------------------------------------------------ Part B (FRW)
tau = sp.symbols('tau', real=True)
Y = (tau, x, y, z)
a = sp.Function('a', positive=True)(tau)
g = a**2 * eta_m
gi = g.inv()
sqrtg = a**4
def christoffel(g, gi, Y):
    G = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for r in range(4):
        for m in range(4):
            for n in range(4):
                G[r][m][n] = sp.simplify(sum(gi[r, l] * (sp.diff(g[l, m], Y[n]) + sp.diff(g[l, n], Y[m])
                                                   - sp.diff(g[m, n], Y[l])) for l in range(4)) / 2)
    return G
Gam = christoffel(g, gi, Y)
q = [s / a for s in sig]
qt = [s / a for s in sigt]
res["B1_metric_identity"] = bool(all(sp.simplify((q[m] * qt[n] + q[n] * qt[m]) / 2 - gi[m, n] * s0) == sp.zeros(2)
                                     for m in range(4) for n in range(4)))

A_, Ad_ = sp.symbols('A_ Ad_', real=True)
def solve_Omega(Q):
    Om = []
    for r in range(4):
        syms = sp.symbols(f'w0:8', real=True)
        W = sp.Matrix([[syms[0] + I * syms[1], syms[2] + I * syms[3]],
                       [syms[4] + I * syms[5], syms[6] + I * syms[7]]])
        eqs = []
        for m in range(4):
            M = sp.diff(Q[m], Y[r]) + sum((Gam[m][r][l] * Q[l] for l in range(4)), sp.zeros(2)) \
                - W.H * Q[m] - Q[m] * W
            M = M.subs(sp.Derivative(a, tau), Ad_).subs(a, A_)
            for c in M:
                c = sp.expand(c)
                eqs += [sp.re(c), sp.im(c)]
        sol = sp.solve(eqs, syms, dict=True)
        assert sol, "tetrad postulate has no solution"
        Wr = W.subs(sol[0])
        # the U(1) (i*real*I) direction is left free by the postulate: that is the EM gauge
        # potential in Sachs' unification. Set it to zero (neutral field).
        Wr = Wr.subs({s: 0 for s in syms}).subs({Ad_: sp.Derivative(a, tau), A_: a})
        Om.append(sp.simplify(Wr))
    return Om
Om = solve_Omega(q)
Omc = solve_Omega(qt)
res["B2_Omega_eta_solved"] = [str(o) for o in Om]
res["B2_Omega_chi_solved"] = [str(o) for o in Omc]
# notebook-cited Sachs (3.77): Omega_rho = -1/4 q~_mu (d_rho q^mu + Gamma^mu_{tau rho} q^tau)
q_low = [sum((g[m, n] * q[n] for n in range(4)), sp.zeros(2)) for m in range(4)]
qt_low = [sum((g[m, n] * qt[n] for n in range(4)), sp.zeros(2)) for m in range(4)]
def sachs377(Qt_low, Q, r):
    return sp.simplify(-sp.Rational(1, 4) * sum((Qt_low[m] * (sp.diff(Q[m], Y[r]) + sum((Gam[m][l][r] * Q[l] for l in range(4)), sp.zeros(2)))
                                                  for m in range(4)), sp.zeros(2)))
S377 = [sachs377(qt_low, q, r) for r in range(4)]
res["B2_Sachs_3.77_as_cited"] = [str(o) for o in S377]
res["B2_Sachs_3.77_equals_solved_Omega_chi_(as_labelled_on_p17)"] = bool(all(sp.simplify(S377[r] - Omc[r]) == sp.zeros(2) for r in range(4)))
# p.17 (3.79b): +1/4 q_mu (d_rho q~^mu + Gamma q~^tau)  -> Omega^(chi)
S379b = [sp.simplify(sp.Rational(1, 4) * sum((q_low[m] * (sp.diff(qt[m], Y[r]) + sum((Gam[m][l][r] * qt[l] for l in range(4)), sp.zeros(2))) for m in range(4)), sp.zeros(2))) for r in range(4)]
res["B2_Sachs_3.79b_equals_solved_Omega_chi"] = bool(all(sp.simplify(S379b[r] - Omc[r]) == sp.zeros(2) for r in range(4)))
# p.15 (3.88): Omega_mu = -1/4 q_rho (d_mu q~^rho + Gamma q~^tau) = +1/4 (d_mu q^rho + Gamma q^tau) q~_rho -> Omega^(eta)
S388a = [sp.simplify(-sp.Rational(1, 4) * sum((q_low[m] * (sp.diff(qt[m], Y[r]) + sum((Gam[m][l][r] * qt[l] for l in range(4)), sp.zeros(2))) for m in range(4)), sp.zeros(2))) for r in range(4)]
S388b = [sp.simplify(sp.Rational(1, 4) * sum(((sp.diff(q[m], Y[r]) + sum((Gam[m][l][r] * q[l] for l in range(4)), sp.zeros(2))) * qt_low[m] for m in range(4)), sp.zeros(2))) for r in range(4)]
res["B2_p15_3.88_first_form_equals_Omega_eta"] = bool(all(sp.simplify(S388a[r] - Om[r]) == sp.zeros(2) for r in range(4)))
res["B2_p15_3.88_second_form_equals_Omega_eta"] = bool(all(sp.simplify(S388b[r] - Om[r]) == sp.zeros(2) for r in range(4)))
res["B2_Sachs_3.77_equals_solved_Omega_eta"] = bool(all(sp.simplify(S377[r] - Om[r]) == sp.zeros(2) for r in range(4)))
res["B2_Sachs_3.77_with_q_<->_q~_equals_solved_Omega"] = bool(all(
    sp.simplify(sachs377(q_low, qt, r) - Om[r]) == sp.zeros(2) for r in range(4)))

def sector(Q, Omg, label, u):
    out = {}
    f = [sp.Function(f'f{a}')(*Y) for a in (1, 2)]
    fb = [sp.Function(f'fb{a}')(*Y) for a in (1, 2)]
    F = sp.Matrix(f); Fb = sp.Matrix(fb)
    def cov(F_, r):  return F_.diff(Y[r]) + Omg[r] * F_
    def covb(Fb_, r): return (Fb_.diff(Y[r]).T + Fb_.T * Omg[r].H)   # row: (psi_;r)^+
    # B3 Leibniz, off shell
    lhs = sum(sp.diff(sqrtg * (Fb.T * Q[m] * F)[0], Y[m]) for m in range(4))
    rhs = sqrtg * sum((covb(Fb, m) * Q[m] * F)[0] + (Fb.T * Q[m] * cov(F, m))[0] for m in range(4))
    out["B3_leibniz_residual"] = str(R(sp.expand(lhs - rhs)))
    # B4 on-shell solution
    kk = sp.symbols('k', positive=True)
    ph = sp.exp(-I * kk * (tau - z))
    sol = a**sp.Rational(-3, 2) * u * ph
    solb = a**sp.Rational(-3, 2) * u.conjugate() * sp.exp(I * kk * (tau - z))
    def covS(r):  return sol.diff(Y[r]) + Omg[r] * sol
    def covSb(r): return solb.diff(Y[r]).T + solb.T * Omg[r].H
    weyl = sp.simplify(sum((Q[m] * covS(m) for m in range(4)), sp.zeros(2, 1)))
    out["B4_field_equation_residual"] = str(weyl)
    # B5 tensor (corrected NB-028): Theta^{mu nu} = i/2 (psi^+ Q^mu psi^{;nu} - psi^{+;nu} Q^mu psi) - g^{mu nu} L
    Lm = R(I / 2 * sum((solb.T * Q[m] * covS(m))[0] - (covSb(m) * Q[m] * sol)[0] for m in range(4)))
    out["B5_L_M_on_shell"] = str(Lm)
    Th = sp.zeros(4, 4); Thnb00 = 0
    for m in range(4):
        for n in range(4):
            val = 0
            for l in range(4):
                val += gi[n, l] * ((solb.T * Q[m] * covS(l))[0] - (covSb(l) * Q[m] * sol)[0])
            Th[m, n] = R(I / 2 * val - gi[m, n] * Lm)
    Thnb00 = R(I / 2 * sum(gi[0, l] * ((solb.T * Q[0] * covS(l))[0] + (covSb(l) * Q[0] * sol)[0]) for l in range(4)))
    out["B5_Theta_is_real"] = bool(all(sp.simplify(sp.im(sp.expand_complex(c.subs(sp.Derivative(a, tau), Ad_).subs(a, A_)))) == 0 for c in Th))
    out["B7_notebook_as_written_Theta00_is_pure_imaginary"] = bool(sp.simplify(sp.re(sp.expand_complex(Thnb00.subs(sp.Derivative(a, tau), Ad_).subs(a, A_)))) == 0)
    out["B5_Theta_antisymmetric_part_zero"] = bool(sp.simplify(Th - Th.T) == sp.zeros(4, 4))
    out["B5_Theta_antisymmetric_part"] = str(sp.simplify((Th - Th.T) / 2))
    out["B5_Theta_canonical_upper"] = str(Th)
    T = sp.simplify((Th + Th.T) / 2)
    out["B5_T_upper"] = str(T)
    div = [R(sum(sp.diff(T[m, n], Y[m]) for m in range(4))
                       + sum(Gam[m][m][l] * T[l, n] for m in range(4) for l in range(4))
                       + sum(Gam[n][m][l] * T[m, l] for m in range(4) for l in range(4))) for n in range(4)]
    out["B5_covariant_divergence"] = [str(d) for d in div]
    out["B5_trace"] = str(R(sum(g[m, n] * T[m, n] for m in range(4) for n in range(4))))
    # energy density for comoving observer u^mu = (1/a,0,0,0): rho = g g T u u = a^2 T^{00}
    rho = R(g[0, 0]**2 * T[0, 0] / a**2)  # rho = T_{00} u^0 u^0, u^0 = 1/a, T_{00} = a^4 T^{00}
    out["B5_rho_comoving"] = str(rho)
    out["B7_notebook_as_written_Theta00"] = str(Thnb00)
    return out

res["eta_sector"] = sector(q, Om, "eta", sp.Matrix([1, 0]))     # sigma^mu: sigma_z u = +u for omega=k
res["chi_sector"] = sector(qt, Omc, "chi", sp.Matrix([0, 1]))   # sigma~^mu: -sigma_z u = +u

if __name__ == "__main__":
    print(json.dumps(res, indent=2))
    out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-026_027_028_theta_curved.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=2))
    print("wrote", out)
