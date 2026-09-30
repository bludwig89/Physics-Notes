"""
NB-037 (pp.28-29): the Omega field equation
      1/2 (q~^rho q^nu - q~^nu q^rho)_{;nu} = -(i/2) eta^+ q^rho eta
checked term-by-term against Einstein-Cartan-Sciama-Kibble (ECSK).

Date-time stamp: 2026-09-22 - 18:05

Everything at one point in a local Lorentz frame (q^mu = sigma^mu, Levi-Civita part of Omega = 0):
the Omega equation is algebraic in the non-Riemannian part of Omega, and the derivative terms
of the gravitational action that are linear in it are total derivatives there.
Signature (+,-,-,-); eps_{0123} = +1; kappa = 8 pi G.
Gravity: L_G = -(1/2kappa) sqrt(-g) R, the sign that gives G = +kappa T with the 02b section 7 T (see doc).
Spinor generators (02b section 7.4 convention eta_;mu = d eta + Omega eta):
      Omega_rho = 1/2 w_rho ab S^ab,   S^ab   = 1/4 (s~^a s^b - s~^b s^a)          (eta, uses q^mu)
      Omega^chi_rho = 1/2 w_rho ab Sc^ab, Sc^ab = 1/4 (s^a s~^b - s^b s~^a)         (chi, uses q~^mu)

E1 matrix identities: q^c S^ab - S^ab+ q^c = alpha eps^{cabd} s_d, and the chi analogue (sign flip).
E2 Fierz: eta eta^+ = 1/2 j^a s~_a, j^a = eta^+ s^a eta, j.j = 0.
E3 exact source dL_M/dOmega_rho (Omega an unconstrained complex 2x2, real variation):
   trace part = the notebook's -(i/2) eta^+ q^rho eta (up to the transpose convention);
   traceless part = the ECSK spin tensor.
E4 spin tensor S^{nu ab} = dL_M/dw_{nu ab}: totally antisymmetric, = c eps^{nu a b d} j_d.
E5 connection equation solved (a) in tensor ECSK variables w, (b) in the notebook's spinor variable
   Omega (32 real components); same contorsion; torsion from the tetrad postulate; Cartan equation.
E6 notebook LHS 1/2[Omega_nu, s~^rho s^nu - s~^nu s^rho] = gravity Euler-Lagrange term; linear
   and injective in the torsion; the U(1)/trace directions of Omega carry no gravity term.
E7 Dirac psi = (chi, eta): axial current = j_eta - j_chi; total spin tensor ~ eps J5;
   Hehl-Datta contact term from substituting the solution back.
"""
import sympy as sp
import itertools, json, pathlib

I = sp.I
s0 = sp.eye(2); s1 = sp.Matrix([[0, 1], [1, 0]]); s2 = sp.Matrix([[0, -I], [I, 0]]); s3 = sp.Matrix([[1, 0], [0, -1]])
SIG = [s0, s1, s2, s3]; SIGT = [s0, -s1, -s2, -s3]
ETA = sp.diag(1, -1, -1, -1)
SIG_lo = [ETA[a, a] * SIG[a] for a in range(4)]; SIGT_lo = [ETA[a, a] * SIGT[a] for a in range(4)]
kap = sp.Symbol('kappa', positive=True)

def eps_lo(a, b, c, d): return sp.LeviCivita(a, b, c, d)                      # eps_{0123}=+1
def eps_up(a, b, c, d): return ETA[a, a] * ETA[b, b] * ETA[c, c] * ETA[d, d] * sp.LeviCivita(a, b, c, d)  # eps^{0123}=-1

S_eta = {(a, b): (SIGT[a] * SIG[b] - SIGT[b] * SIG[a]) / 4 for a in range(4) for b in range(4)}
S_chi = {(a, b): (SIG[a] * SIGT[b] - SIG[b] * SIGT[a]) / 4 for a in range(4) for b in range(4)}
PAIRS = [(a, b) for a in range(4) for b in range(4) if a < b]
res = {"build": "NB-037 ECSK", "stamp": "2026-09-22 - 18:05"}

# ------------------------------------------------------------------ E1
def ident(Q, Qlo, Sg):
    alphas = set(); ok = True
    for c in range(4):
        for (a, b) in PAIRS:
            M = Q[c] * Sg[(a, b)] - Sg[(a, b)].H * Q[c]
            Rm = sum((eps_up(c, a, b, d) * Qlo[d] for d in range(4)), sp.zeros(2))
            if Rm == sp.zeros(2):
                ok &= (M == sp.zeros(2)); continue
            # find scalar alpha with M = alpha*Rm
            idx = [i for i in range(4) if Rm[i] != 0][0]
            al = sp.simplify(M[idx] / Rm[idx]); alphas.add(al)
            ok &= sp.simplify(M - al * Rm) == sp.zeros(2)
    return ok, [str(x) for x in alphas]
res["E1_eta_qS-S+q=alpha*eps*s_d"], res["E1_eta_alpha"] = ident(SIG, SIG_lo, S_eta)
res["E1_chi_q~S-S+q~=alpha*eps*s~_d"], res["E1_chi_alpha"] = ident(SIGT, SIGT_lo, S_chi)

# ------------------------------------------------------------------ spinors
xr = sp.symbols('x1 y1 x2 y2', real=True)
eta = sp.Matrix([xr[0] + I * xr[1], xr[2] + I * xr[3]])
zr = sp.symbols('u1 v1 u2 v2', real=True)
chi = sp.Matrix([zr[0] + I * zr[1], zr[2] + I * zr[3]])
j_eta = [sp.expand((eta.H * SIG[a] * eta)[0]) for a in range(4)]
j_chi = [sp.expand((chi.H * SIGT[a] * chi)[0]) for a in range(4)]
jlo = lambda j: [ETA[a, a] * j[a] for a in range(4)]

# E2
fz = sp.expand(eta * eta.H - sum((j_eta[a] * SIGT_lo[a] for a in range(4)), sp.zeros(2)) / 2)
res["E2_Fierz_eta_eta+=1/2 j^a s~_a"] = fz.applyfunc(sp.expand) == sp.zeros(2)
res["E2_j.j"] = str(sp.factor(sp.expand(sum(j_eta[a] * jlo(j_eta)[a] for a in range(4)))))

# ------------------------------------------------------------------ Lagrangian pieces at a point
# connection deviation: general complex 2x2 per rho (32 real)
Wr = [[sp.Symbol(f'k{r}_{i}', real=True) for i in range(8)] for r in range(4)]
def Kmat(r):
    w = Wr[r]; return sp.Matrix([[w[0] + I * w[1], w[2] + I * w[3]], [w[4] + I * w[5], w[6] + I * w[7]]])
Kh = [Kmat(r) for r in range(4)]
allK = [s for r in range(4) for s in Wr[r]]

def LM_coupling(psi, Q, Om):   # the Omega-dependent part of i/2(psi^+ Q psi_; - psi^+_; Q psi)
    return sp.expand(I / 2 * sum((psi.H * (Q[m] * Om[m] - Om[m].H * Q[m]) * psi)[0] for m in range(4)))

def R_tensor(w):   # w[rho][(a,b)] antisym, flat: R = R^{ab}_{ab}, R^a_{b mu nu} = w_mu^a_c w_nu^c_b - (mu<->nu)
    def W(m, a, b):   # w_m^{a}_{b} with first frame index raised
        return ETA[a, a] * w[m][(a, b)]
    tot = 0
    for mu in range(4):
        for nu in range(4):
            for c in range(4):
                # R^{mu nu}_{mu nu}: a=mu, b=nu (frame=coord), second index raised with eta
                tot += ETA[nu, nu] * (W(mu, mu, c) * W(nu, c, nu) - W(nu, mu, c) * W(mu, c, nu))
    return sp.expand(tot)

def R_spinor(Om, Qt=SIGT, Q=SIG):  # R = -1/2 Tr(K_mn q~^m q^n + K^+_mn q^n q~^m), K = [Om_m, Om_n] at the point
    tot = 0
    for m in range(4):
        for n in range(4):
            Kmn = Om[m] * Om[n] - Om[n] * Om[m]
            tot += (Kmn * Qt[m] * Q[n] + Kmn.H * Q[n] * Qt[m]).trace()
    return sp.expand(-tot / 2)

# tensor variables
wv = {(r, p): sp.Symbol(f'w{r}_{p[0]}{p[1]}', real=True) for r in range(4) for p in PAIRS}
def wfull(r):
    d = {}
    for a in range(4):
        for b in range(4):
            d[(a, b)] = 0 if a == b else (wv[(r, (a, b))] if a < b else -wv[(r, (b, a))])
    return d
wF = [wfull(r) for r in range(4)]
Om_eta_w = [sum((wF[r][(a, b)] * S_eta[(a, b)] for a in range(4) for b in range(4)), sp.zeros(2)) / 2 for r in range(4)]
Om_chi_w = [sum((wF[r][(a, b)] * S_chi[(a, b)] for a in range(4) for b in range(4)), sp.zeros(2)) / 2 for r in range(4)]
res["E0_R_spinor(Omega(w))==R_tensor(w)"] = sp.expand(R_spinor(Om_eta_w) - R_tensor(wF)) == 0
res["E0_R_spinor_chi(Omega_chi(w))==R_tensor(w)"] = sp.expand(R_spinor(Om_chi_w, Qt=SIG, Q=SIGT) - R_tensor(wF)) == 0

# ------------------------------------------------------------------ E3 exact source
LMK = LM_coupling(eta, SIG, Kh)
src_ok = True; tr_ok = True
for r in range(4):
    # complex-matrix derivative dL/dK (K, K^+ independent): dL/dK_ij = 1/2(dL/dRe - i dL/dIm)
    D = sp.zeros(2)
    for (i, jj), (re, im) in zip([(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 1), (2, 3), (4, 5), (6, 7)]):
        D[i, jj] = sp.expand((sp.diff(LMK, Wr[r][re]) - I * sp.diff(LMK, Wr[r][im])) / 2)
    expect = (I / 2 * eta * eta.H * SIG[r]).T                    # i/2 (eta eta^+ q^rho)^T
    src_ok &= (D - expect).applyfunc(sp.expand) == sp.zeros(2)
    tr_ok &= sp.expand(D.trace() - I / 2 * j_eta[r]) == 0
    if r == 1:
        res["E3_source_rho1_traceless_part"] = str((D - D.trace() / 2 * sp.eye(2)).applyfunc(sp.factor))
res["E3_dL/dOmega_rho = i/2 (eta eta^+ q^rho)^T"] = src_ok
res["E3_trace_of_source = +i/2 eta^+ q^rho eta  (the notebook's scalar)"] = tr_ok
# traceless part of eta eta^+ q^rho (before transpose) = 1/2 j_a (s~^a s^rho)_traceless = j_a S^{a rho}
tl_ok = all(sp.expand((eta * eta.H * SIG[r] - j_eta[r] / 2 * sp.eye(2))
                      - sum((jlo(j_eta)[a] * S_eta[(a, r)] for a in range(4)), sp.zeros(2))) == sp.zeros(2) for r in range(4))
res["E3_eta_eta+q^rho = 1/2 j^rho I + j_a S^{a rho}"] = tl_ok

# ------------------------------------------------------------------ E4 spin tensor
LMw = LM_coupling(eta, SIG, Om_eta_w)
def spin_tensor(L):
    St = {}
    for r in range(4):
        for (a, b) in PAIRS:
            v = sp.expand(sp.diff(L, wv[(r, (a, b))]))   # dL/dw_{r ab} for a<b (w_{r ab} and -w_{r ba} both counted)
            St[(r, a, b)] = v; St[(r, b, a)] = -v
        for a in range(4): St[(r, a, a)] = 0
    return St
Sp = spin_tensor(LMw)
# raise the rho index: S^{rho}{}_{ab} -> totally antisymmetric test on S_{rho a b} (frame=coord)
anti = all(sp.expand(Sp[(r, a, b)] + Sp[(a, r, b)]) == 0 for r in range(4) for a in range(4) for b in range(4))
res["E4_eta_spin_tensor_totally_antisymmetric"] = anti
cS = sp.Symbol('c')
eqs = [sp.expand(Sp[(r, a, b)] - cS * sum(eps_up(r, a, b, d) * jlo(j_eta)[d] for d in range(4))) for r in range(4) for a in range(4) for b in range(4)]
solc = sp.solve([e for e in eqs if e != 0][:3], cS)
res["E4_eta_S^{rho ab} = c eps^{rho a b d} j_d, c ="] = str(solc)
res["E4_eta_check_all_components"] = all(sp.expand(e.subs(cS, solc[cS])) == 0 for e in eqs)
LMw_chi = LM_coupling(chi, SIGT, Om_chi_w)
Spc = spin_tensor(LMw_chi)
eqc = [sp.expand(Spc[(r, a, b)] - cS * sum(eps_up(r, a, b, d) * jlo(j_chi)[d] for d in range(4))) for r in range(4) for a in range(4) for b in range(4)]
solcc = sp.solve([e for e in eqc if e != 0][:3], cS)
res["E4_chi_S^{rho ab} = c eps^{rho a b d} j_chi_d, c ="] = str(solcc)
res["E4_chi_check_all_components"] = all(sp.expand(e.subs(cS, solcc[cS])) == 0 for e in eqc)

# ------------------------------------------------------------------ E5 solve the connection equation
# (a) tensor ECSK
Lt = -R_tensor(wF) / (2 * kap) + LMw
wlist = list(wv.values())
sol_t = sp.solve([sp.diff(Lt, w) for w in wlist], wlist, dict=True)[0]
# contorsion K_{rho a b} = w_{rho ab}; test K = c2 eps j
c2 = sp.Symbol('c2')
Kt = {(r, a, b): wF[r][(a, b)].subs(sol_t) if a != b else 0 for r in range(4) for a in range(4) for b in range(4)}
e5 = [sp.expand(Kt[(r, a, b)] - c2 * kap * sum(eps_lo(r, a, b, d) * j_eta[d] for d in range(4))) for r in range(4) for a in range(4) for b in range(4)]
s2_ = sp.solve([e for e in e5 if e != 0][:2], c2)
res["E5a_tensor_contorsion_K_{rho ab} = c2 kappa eps j, c2 ="] = str(s2_)
res["E5a_all_components"] = all(sp.expand(e.subs(c2, s2_[c2])) == 0 for e in e5)

# (b) notebook spinor variable: all 32 real components of Omega
Ls = -R_spinor(Kh) / (2 * kap) + LMK
EL = {s: sp.expand(sp.diff(Ls, s)) for s in allK}
# decompose each K_r = a_r I + i b_r I + traceless-Lorentz; the Lorentz part is 1/2 w S^ab (6 real)
# solve the 32 equations restricted to Lorentz-valued K plus trace symbols
ab_ = [(sp.Symbol(f'A{r}', real=True), sp.Symbol(f'B{r}', real=True)) for r in range(4)]
subsK = {}
for r in range(4):
    Mr = Om_eta_w[r] + (ab_[r][0] + I * ab_[r][1]) * sp.eye(2)
    for (i, jj), (re, im) in zip([(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 1), (2, 3), (4, 5), (6, 7)]):
        subsK[Wr[r][re]] = sp.re(sp.expand(Mr[i, jj])); subsK[Wr[r][im]] = sp.im(sp.expand(Mr[i, jj]))
# the 32 EL expressions, evaluated on this family; project with the chain rule onto w and A,B:
Ls_fam = sp.expand(Ls.subs(subsK))
eqs_w = [sp.diff(Ls_fam, w) for w in wlist]
eqs_A = [sp.expand(sp.diff(Ls_fam, ab_[r][0])) for r in range(4)]
eqs_B = [sp.expand(sp.diff(Ls_fam, ab_[r][1])) for r in range(4)]
sol_s = sp.solve(eqs_w, wlist, dict=True)[0]
res["E5b_spinor_solution_equals_tensor_solution"] = all(sp.expand(sol_s[w] - sol_t[w]) == 0 for w in wlist)
res["E5b_real_trace_(dilation)_equation"] = [str(e) for e in eqs_A]
res["E5b_imag_trace_(U(1))_equation"] = [str(sp.factor(e)) for e in eqs_B]
res["E5b_U1_equation_is_-j^rho"] = all(sp.expand(eqs_B[r] + j_eta[r]) == 0 for r in range(4))
# is the Lorentz-restricted family complete? the 32-dim EL at the solution: components outside the
# family (non-Lorentz traceless = none; sl(2,C) is 6 real = Lorentz) -> check dims: 6 Lorentz + 2 trace = 8. ok.
# torsion from the tetrad postulate with the solved Omega:  s^l K_n + K_n^+ s^l = Gamma^l_{t n} s^t
Ksol = [Om_eta_w[r].subs(sol_s) for r in range(4)]
Gam = [[[sp.expand((SIGT_lo[t] * (SIG[l] * Ksol[n] + Ksol[n].H * SIG[l])).trace() / 2) for n in range(4)] for t in range(4)] for l in range(4)]
# ( Tr(s~_t s^m) = 2 delta^m_t )
Tlo = {(l, t, n): sp.expand(ETA[l, l] * (Gam[l][t][n] - Gam[l][n][t])) for l in range(4) for t in range(4) for n in range(4)}
res["E5_torsion_totally_antisymmetric"] = all(sp.expand(Tlo[(l, t, n)] + Tlo[(t, l, n)]) == 0 for l in range(4) for t in range(4) for n in range(4))
c3 = sp.Symbol('c3')
e6 = [sp.expand(Tlo[(l, t, n)] - c3 * kap * sum(eps_lo(l, t, n, d) * j_eta[d] for d in range(4))) for l in range(4) for t in range(4) for n in range(4)]
s3_ = sp.solve([e for e in e6 if e != 0][:2], c3)
res["E5_torsion_T_{l t n} = c3 kappa eps j, c3 ="] = str(s3_)
res["E5_torsion_all_components"] = all(sp.expand(e.subs(c3, s3_[c3])) == 0 for e in e6)
# Cartan equation, trace-free spin: T_{l t n} = +/- kappa S_{l t n}
# S_{ltn} = eps_{ltnd} j^d * c * (sign from lowering 3 indices + eps_up->eps_lo): eps^{...}j_d lowered = eps_{...}j^d * det(eta) = -eps_lo j
ratio = sp.simplify(s3_[c3] / (-solc[cS]))
res["E5_Cartan_T_{ltn} / (kappa S_{ltn})"] = str(ratio)
res["E5_Gamma_metric_compatible_(Gamma_{(l t) n}=0)"] = all(sp.expand(ETA[l, l] * Gam[l][t][n] + ETA[t, t] * Gam[t][l][n]) == 0 for l in range(4) for t in range(4) for n in range(4))

# ------------------------------------------------------------------ E6 notebook LHS
def N_lhs(K, r):   # 1/2 sum_nu [K_nu, s~^rho s^nu - s~^nu s^rho]   (adjoint covariant derivative at the point)
    ETAup = ETA
    tot = sp.zeros(2)
    for n in range(4):
        X = SIGT[r] * SIG[n] - SIGT[n] * SIG[r]    # both indices up; contracted with lower nu of K_nu (no metric)
        tot += K[n] * X - X * K[n]
    return tot / 2
# Real, Lorentz-projected form. The gravity EL for w_{rho ab} vs the notebook LHS N^rho projected on
# the generator: dL_G/dw_{rho ab} =?= beta * Re Tr( N^rho[Omega(w)] * S_eta^{ab} )  (upper ab via eta)
LGw = -R_tensor(wF) / (2 * kap)
beta = sp.Symbol('beta')
e6 = []
for r in range(4):
    Nm = N_lhs(Om_eta_w, r)
    for (a_, b_) in PAIRS:
        lhs = sp.expand(sp.diff(LGw, wv[(r, (a_, b_))]))
        proj = sp.expand((Nm * S_eta[(a_, b_)]).trace())
        e6.append(sp.expand(lhs - beta * (proj + sp.conjugate(proj)) / 2))
bsol = sp.solve([e for e in e6 if e != 0][:1], beta)
res["E6_dL_G/dw = beta Re Tr(N^rho S_ab), beta ="] = str(bsol)
res["E6_all_24_components"] = all(sp.expand(e.subs(beta, bsol[beta])) == 0 for e in e6)
# matter side, same projection: dL_M/dw_{rho ab} = gamma * Re Tr( (i/2 eta eta^+ q^rho) S_eta^{ab} ) ; trace part drops (Tr S = 0)
gam_ = sp.Symbol('gamma_')
e6m = []
for r in range(4):
    M = I / 2 * eta * eta.H * SIG[r]
    for (a_, b_) in PAIRS:
        proj = sp.expand((M * S_eta[(a_, b_)]).trace())
        e6m.append(sp.expand(Sp[(r, a_, b_)] - gam_ * (proj + sp.conjugate(proj)) / 2))
gsol = sp.solve([e for e in e6m if e != 0][:1], gam_)
res["E6_dL_M/dw = gamma Re Tr(i/2 eta eta^+ q^rho S_ab), gamma ="] = str(gsol)
res["E6_matter_all_24_components"] = all(sp.expand(e.subs(gam_, gsol[gam_])) == 0 for e in e6m)
res["E6_trace_part_of_source_projects_to_zero_on_Lorentz"] = all(sp.expand((S_eta[p_]).trace()) == 0 for p_ in PAIRS)
res["E6_notebook_LHS_is_traceless"] = all(sp.expand(N_lhs(Kh, r).trace()) == 0 for r in range(4))
# injectivity: Lorentz part of Omega -> notebook LHS (24 -> 4x(2x2 complex)) has rank 24
vecN = []
for r in range(4):
    Nm = N_lhs(Om_eta_w, r)
    for c in Nm: vecN += [sp.re(sp.expand(c)), sp.im(sp.expand(c))]
Jm = sp.Matrix([[sp.diff(v, w) for w in wlist] for v in vecN])
res["E6_rank_(Lorentz Omega -> LHS)"] = int(Jm.rank())
LG = -R_spinor(Kh) / (2 * kap)
res["E6_trace_directions_absent_from_R"] = all(sp.diff(sp.expand(LG.subs(subsK)), s) == 0 for r in range(4) for s in ab_[r])

# ------------------------------------------------------------------ E7 Dirac
g0 = sp.zeros(4); g0[0:2, 2:4] = s0; g0[2:4, 0:2] = s0
gam = []
for m in range(4):
    G = sp.zeros(4); G[0:2, 2:4] = SIG[m]; G[2:4, 0:2] = SIGT[m]; gam.append(G)
g5 = sp.expand(I * gam[0] * gam[1] * gam[2] * gam[3])
psi = sp.Matrix([chi[0], chi[1], eta[0], eta[1]])
psib = psi.H * gam[0]
J = [sp.expand((psib * gam[m] * psi)[0]) for m in range(4)]
J5 = [sp.expand((psib * gam[m] * g5 * psi)[0]) for m in range(4)]
res["E7_gamma5"] = str(g5)
res["E7_vector_current = j_eta + j_chi"] = all(sp.expand(J[m] - j_eta[m] - j_chi[m]) == 0 for m in range(4))
res["E7_axial_current = j_eta - j_chi"] = all(sp.expand(J5[m] - j_eta[m] + j_chi[m]) == 0 for m in range(4))
Ltot = -R_tensor(wF) / (2 * kap) + LMw + LMw_chi
Sd = spin_tensor(LMw + LMw_chi)
e7 = [sp.expand(Sd[(r, a, b)] - solc[cS] * sum(eps_up(r, a, b, d) * jlo(J5)[d] for d in range(4))) for r in range(4) for a in range(4) for b in range(4)]
res["E7_Dirac_spin_tensor S^{rho ab} = c eps^{rho ab d} J5_d (same c as eta)"] = all(e == 0 for e in e7)
sold = sp.solve([sp.diff(Ltot, w) for w in wlist], wlist, dict=True)[0]
Leff = sp.factor(sp.expand(Ltot.subs(sold)))
J5sq = sp.expand(sum(J5[a] * jlo(J5)[a] for a in range(4)))
cHD = sp.simplify(Leff / (kap * J5sq))
res["E7_L_eff = c_HD kappa J5.J5, c_HD ="] = str(cHD)
res["E7_single_Weyl_L_eff"] = str(sp.factor(sp.expand(Lt.subs(sol_t))))

# ------------------------------------------------------------------ E8 LHS = Cartan tensor; corrected equation
def torsion_of(Kl):
    G_ = [[[sp.expand((SIGT_lo[t] * (SIG[l] * Kl[n] + Kl[n].H * SIG[l])).trace() / 2) for n in range(4)] for t in range(4)] for l in range(4)]
    return {(l, t, n): sp.expand(G_[l][t][n] - G_[l][n][t]) for l in range(4) for t in range(4) for n in range(4)}   # T^l_{tn}
Tg = torsion_of(Om_eta_w)                                     # generic Lorentz connection (24 free w)
Tvec = {n: sp.expand(sum(Tg[(l, n, l)] for l in range(4))) for n in range(4)}   # T_n = T^l_{n l}
def cartan(l, m, n, sgn):  # C^l_{mn} = T^l_{mn} + sgn (delta^l_m T_n - delta^l_n T_m)
    return Tg[(l, m, n)] + sgn * ((1 if l == m else 0) * Tvec[n] - (1 if l == n else 0) * Tvec[m])
# expand N^rho = sum_{a<b} X^{rho ab} S^{ab} with real X (the six S^{ab} are a real basis of sl(2,C))
Xs = {(r, p_): sp.Symbol(f'X{r}_{p_[0]}{p_[1]}', real=True) for r in range(4) for p_ in PAIRS}
Xsol = {}
for r in range(4):
    D8 = (N_lhs(Om_eta_w, r) - sum((Xs[(r, p_)] * S_eta[p_] for p_ in PAIRS), sp.zeros(2))).applyfunc(sp.expand)
    eqr = []
    for c_ in D8: eqr += [sp.re(c_), sp.im(c_)]
    Xsol.update(sp.solve(eqr, [Xs[(r, p_)] for p_ in PAIRS], dict=True)[0])
def Xf(r, a_, b_):
    if a_ == b_: return 0
    v = Xsol[Xs[(r, (a_, b_))]] if a_ < b_ else -Xsol[Xs[(r, (b_, a_))]]
    return v * ETA[a_, a_] * ETA[b_, b_]    # coefficients of upper S^{ab} carry lower ab; raise
# torsion with all indices up (frame=coord): T^{l m n} = T^l_{mn} eta^mm eta^nn ; T^n (up) = T^l_{n l} eta^nn
Tup = lambda l, m, n: Tg[(l, m, n)] * ETA[m, m] * ETA[n, n]
Tv = lambda n: Tvec[n] * ETA[n, n]
cs = sp.symbols('c1:6')
basis = lambda r, a_, b_: [Tup(r, a_, b_), Tup(a_, b_, r) - Tup(b_, a_, r), Tup(a_, r, b_) - Tup(b_, r, a_),
                            ETA[r, a_] * Tv(b_) - ETA[r, b_] * Tv(a_), sum(eps_up(r, a_, b_, d) * sum(eps_lo(d, l, m, n) * Tup(l, m, n) for l in range(4) for m in range(4) for n in range(4)) for d in range(4))]
eqfit = []
for r in range(4):
    for (a_, b_) in PAIRS:
        ex = sp.expand(Xf(r, a_, b_) - sum(c * t for c, t in zip(cs, basis(r, a_, b_))))
        eqfit += list(sp.Poly(ex, *wlist).coeffs())
fit = sp.solve(eqfit, cs, dict=True)
res["E8_LHS_X^{rho ab} fit coefficients [T^{rho ab}, T^{ab rho}-T^{ba rho}, T^{a rho b}-T^{b rho a}, eta^{rho a}T^b-eta^{rho b}T^a, eps eps.T]"] = str(fit)
Cup = lambda r, a_, b_: Tup(r, a_, b_) + ETA[r, a_] * Tv(b_) - ETA[r, b_] * Tv(a_)
ok_c = all((N_lhs(Om_eta_w, r) + sum((Cup(r, a_, b_) * ETA[a_, a_] * ETA[b_, b_] * S_eta[(a_, b_)] for a_ in range(4) for b_ in range(4)), sp.zeros(2))).applyfunc(sp.expand) == sp.zeros(2) for r in range(4))
res["E8_notebook_LHS = - C^rho_{ab} S^{ab} (full sum), C^{rho ab}=T^{rho ab}+eta^{rho a}T^b-eta^{rho b}T^a, generic connection"] = ok_c
# the ECSK/Cartan combination written in the same X-language: C^{rho ab} = T^{rho ab} + eta^{rho a} T^b - eta^{rho b} T^a  (index order as Hehl)

# corrected full matrix equation at the solution:
#   1/2 (q~^rho q^nu - q~^nu q^rho)_{;nu} = -2 kappa * (i/2) [ eta eta^+ q^rho - 1/2 (eta^+ q^rho eta) I ]
ok8 = True; tr8 = []
for r in range(4):
    lhs = N_lhs(Ksol, r).applyfunc(sp.expand)
    rhs = (-2 * kap * I / 2 * (eta * eta.H * SIG[r] - j_eta[r] / 2 * sp.eye(2))).applyfunc(sp.expand)
    ok8 &= (lhs - rhs).applyfunc(sp.expand) == sp.zeros(2)
    tr8.append(str(sp.expand(lhs.trace())))
res["E8_corrected_equation_holds_at_solution_(full 2x2)"] = ok8
res["E8_trace_of_LHS_at_solution"] = tr8
res["E8_notebook_RHS_-(i/2)eta^+q^rho eta_times_I_trace"] = [str(sp.expand(-I * j_eta[r])) for r in range(4)]

if __name__ == "__main__":
    print(json.dumps(res, indent=2, default=str))
    out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-037_ecsk_spin_source.json"
    out.write_text(json.dumps(res, indent=2, default=str))
