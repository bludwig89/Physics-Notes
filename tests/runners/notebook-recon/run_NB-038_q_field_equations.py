"""
NB-038 (p.29): the q^lambda variation, never assembled in the notebook, completed into the
missing equations of motion, and checked against NB-034 (eta), NB-037 (Omega, 02b section 8)
and 02b section 7 (Tetrode).

Date-time stamp: 2026-09-22 - 19:20

Reuses the pointwise machinery of run_NB-037_ecsk_spin_source.py (imported, not re-derived).
Conventions as 02b sections 7-8: signature (+,-,-,-), eps_{0123}=+1, L = sqrt(-g){-R/(2 kappa) + L_M},
R = -1/2 Tr(K_{mu nu} q~^mu q^nu + K^+_{mu nu} q^nu q~^mu), eta_;mu = d eta + Omega eta,
Omega = 1/2 w_{mu ab} Sigma^ab, Omega^chi = 1/2 w_{mu ab} Sigma_chi^ab.

G1 matrix derivative dR/dq^lambda (q~ held fixed) by brute force vs closed form; notebook p.29 form.
G2 tetrad derivative (q and q~ both from one tetrad): e_{lam a} d(sqrt(-g) R)/de^nu_a
   = sqrt(-g) * (alpha R_{lam nu} + beta R_{nu lam} + gamma g R): fit -> Einstein tensor of w.
G3 matter: Tr[(dL_M/dq^nu)^T q_lam] = canonical Theta_{lam nu}; notebook's p.29 matter line.
G4 assembled q-equation G_{lam nu}(w) = kappa Theta_{lam nu}(w): pointwise torsion content
   with the section-8 solution -- antisymmetric part at O(kappa^2), contact term (Hehl-Datta)
   in the symmetric part.
G5 antisymmetric part at O(kappa), flat background, generic on-shell Dirac field:
   G_[lam nu](d K) = kappa Theta_[lam nu]  (Belinfante-Rosenfeld identity + Cartan eqn).
G6 matter EOMs with torsion: eta and chi equations (the missing chi analog of NB-034),
   torsion term vs the Hehl-Datta effective Lagrangian.
G7 the p.29 note "Omega~^(chi) = -Omega^(chi)+ = Omega": which identities hold.
"""
import sympy as sp
import importlib.util, json, pathlib, sys

here = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("nb37", here / "run_NB-037_ecsk_spin_source.py")
nb = importlib.util.module_from_spec(spec); spec.loader.exec_module(nb)
I = sp.I; ETA = nb.ETA; SIG = nb.SIG; SIGT = nb.SIGT; SIG_lo = nb.SIG_lo; SIGT_lo = nb.SIGT_lo
PAIRS = nb.PAIRS; S_eta = nb.S_eta; S_chi = nb.S_chi; eps_lo = nb.eps_lo; eps_up = nb.eps_up
kap = nb.kap; wv = nb.wv; wF = nb.wF; wlist = nb.wlist
res = {"build": "NB-038 q-field equations", "stamp": "2026-09-22 - 19:20"}

def Om_of(Sg): return [sum((wF[r][(a, b)] * Sg[(a, b)] for a in range(4) for b in range(4)), sp.zeros(2)) / 2 for r in range(4)]
Om = Om_of(S_eta); Omc = Om_of(S_chi)
def Kc(O, m, n): return O[m] * O[n] - O[n] * O[m]      # curvature at a point (constant connection)

# ------------------------------------------------------------------ G1
Qs = [sp.Matrix(2, 2, lambda i, j: sp.Symbol(f'Q{m}_{i}{j}')) for m in range(4)]
Rq = sp.expand(-sum(((Kc(Om, m, n) * SIGT[m] * Qs[n] + Kc(Om, m, n).H * Qs[n] * SIGT[m]).trace()
                     for m in range(4) for n in range(4))) / 2)
ok1 = True; oknb = True; oknb2 = True; okdiff = []
for l in range(4):
    D = sp.Matrix(2, 2, lambda i, j: sp.diff(Rq, Qs[l][i, j]))
    # closed form: dR/dq^lam = 1/2 (K_{lam rho} q~^rho + q~^rho K^+_{lam rho})^T   (K index lowered via eta at the point)
    cf = sum(((Kc(Om, l, r) * SIGT[r] + SIGT[r] * Kc(Om, l, r).H) * ETA[r, r] * ETA[l, l] for r in range(4)), sp.zeros(2)).T / 2
    # careful: Rq uses K_{mu nu} with LOWER indices contracted against q~^mu q^nu (upper) -> K_{mn} is w_m w_n with lower m,n
    cf = sum(((Kc(Om, l, r) * SIGT[r] + SIGT[r] * Kc(Om, l, r).H) for r in range(4)), sp.zeros(2)).T / 2
    ok1 &= (D - cf).applyfunc(sp.expand) == sp.zeros(2)
    # notebook p.29 bracket (Sachs q~ sign reversal accounted for by an overall -1):
    nbf = -(-sum(((Kc(Om, l, r).H * SIGT[r] + SIGT[r] * Kc(Om, l, r)) for r in range(4)), sp.zeros(2)).T / 2)
    oknb &= (D - nbf).applyfunc(sp.expand) == sp.zeros(2)
    oknb2 &= (D + nbf).applyfunc(sp.expand) == sp.zeros(2)
res["G1_dR/dq^lam = 1/2 (K_lam_rho q~^rho + q~^rho K^+_lam_rho)^T"] = ok1
res["G1_notebook_p29_ordering_(K^+ q~ + q~ K) matches (either overall sign)"] = oknb or oknb2

# ------------------------------------------------------------------ G2 tetrad derivative of sqrt(-g) R
eps_ = sp.Symbol('eps')
H = sp.Matrix(4, 4, lambda a, m: sp.Symbol(f'h{a}{m}', real=True))      # e^mu_a = delta + eps H[a,mu]
Fr = sp.eye(4) + eps_ * H
co = (sp.eye(4) - eps_ * H.T)                                             # e_mu^a to O(eps): co[mu,a]
q = [sum((Fr[a, m] * SIG[a] for a in range(4)), sp.zeros(2)) for m in range(4)]
qt = [sum((Fr[a, m] * SIGT[a] for a in range(4)), sp.zeros(2)) for m in range(4)]
sqrtg = 1 - eps_ * H.trace()
# connection components w_{mu ab} are held fixed (first-order formalism): Omega_mu fixed as a matrix
Rfull = sp.expand(-sum(((Kc(Om, m, n) * qt[m] * q[n] + Kc(Om, m, n).H * q[n] * qt[m]).trace()
                        for m in range(4) for n in range(4))) / 2)
f1 = sp.expand(sp.diff(sp.expand(sqrtg * Rfull), eps_).subs(eps_, 0))
R0 = sp.expand(Rfull.subs(eps_, 0))
res["G2_R_spinor==R_tensor(point)"] = sp.expand(R0 - nb.R_tensor(wF)) == 0
# tensor Ricci of the constant connection: R_{mu nu}^{ab} = w_mu^a_c w_nu^cb - w_nu^a_c w_mu^cb
def W(m, a, b): return ETA[a, a] * wF[m][(a, b)]            # w_m{}^a{}_b
def Riem(m, n, a, b):   # R_{mn}{}^a{}_b
    return sum(W(m, a, c) * W(n, c, b) - W(n, a, c) * W(m, c, b) for c in range(4))
Ric = sp.Matrix(4, 4, lambda l, n: sp.expand(sum(Riem(m, n, m, l) * ETA[l, l] * 0 + Riem(m, n, m, l) for m in range(4))))   # R_{n l}? define below
# define Ric[l,n] = R^m{}_{l m n} style candidates and fit
cands = {}
cands["R^m_{lam m nu}"] = sp.Matrix(4, 4, lambda l, n: sp.expand(sum(Riem(m, n, m, l) for m in range(4))))
T_E = sp.Matrix(4, 4, lambda l, n: sp.expand(sum(ETA[a, a] * co[l, a].subs(eps_, 0) * sp.diff(f1, H[a, n]) for a in range(4))))
al, be, ga = sp.symbols('alpha beta gamma')
A = cands["R^m_{lam m nu}"]
eqs = [sp.expand(T_E[l, n] - (al * A[l, n] + be * A[n, l] + ga * ETA[l, n] * R0)) for l in range(4) for n in range(4)]
coeffs = []
for e in eqs: coeffs += sp.Poly(e, *wlist).coeffs()
fit = sp.solve(coeffs, [al, be, ga], dict=True)
res["G2_e_lam_a d(sqrt(-g)R)/de^nu_a = alpha A_lam_nu + beta A_nu_lam + gamma g R, A=R^m_{lam m nu}"] = str(fit)

# ------------------------------------------------------------------ G3 matter
eta = nb.eta; chi = nb.chi
Deta = [sp.Matrix(2, 1, lambda i, j: sp.Symbol(f'd{m}e{i}')) for m in range(4)]      # eta_;mu at the point (symbols)
Detab = [sp.Matrix(1, 2, lambda i, j: sp.Symbol(f'd{m}eb{j}')) for m in range(4)]   # eta^+_;mu (independent symbols)
etab = eta.H
LMq = sp.expand(I / 2 * sum((etab * Qs[m] * Deta[m])[0] - (Detab[m] * Qs[m] * eta)[0] for m in range(4)))
ok3 = True; oknb3 = True; okT = True
for l in range(4):
    D = sp.Matrix(2, 2, lambda i, j: sp.diff(LMq, Qs[l][i, j]))
    outer = (I / 2 * (Deta[l] * etab - eta * Detab[l])).T
    ok3 &= (D - outer).applyfunc(sp.expand) == sp.zeros(2)
    nbv = I / 2 * ((etab * Deta[l])[0] - (Detab[l] * eta)[0])       # the notebook's scalar
    oknb3 &= sp.expand(D.trace() - nbv) == 0
    for lam in range(4):
        th = sp.expand((D.T * SIG_lo[lam]).trace())
        canon = sp.expand(I / 2 * ((etab * SIG_lo[lam] * Deta[l])[0] - (Detab[l] * SIG_lo[lam] * eta)[0]))
        okT &= sp.expand(th - canon) == 0
res["G3_dL_M/dq^lam = i/2 (eta_;lam eta^+ - eta eta^+_;lam)^T (outer product)"] = ok3
res["G3_notebook_p29_scalar = trace of that matrix (not the matrix)"] = oknb3
res["G3_Tr[(dL_M/dq^nu)^T q_lam] = canonical Theta_{lam nu} (without -gL)"] = okT

# ------------------------------------------------------------------ G4 pointwise torsion content of G(w) = kappa Theta(w)
# Dirac matter; torsion solution K_{rho ab} = -1/4 kappa eps_{rho a b d} J5^d  (02b section 8)
J5 = [sp.expand(nb.j_eta[a] - nb.j_chi[a]) for a in range(4)]
J5lo = [ETA[a, a] * J5[a] for a in range(4)]
J5sq = sp.expand(sum(J5[a] * J5lo[a] for a in range(4)))
Ksub = {}
for r in range(4):
    for (a, b) in PAIRS:
        Ksub[wv[(r, (a, b))]] = sp.expand(-kap / 4 * sum(eps_lo(r, a, b, d) * J5[d] for d in range(4)))
# Einstein tensor from the G2 fit: G_{lam nu} = (1/2)(alpha A + beta A^T + gamma g R) / (normalized)
Gt = sp.Matrix(4, 4, lambda l, n: sp.expand(A[l, n] - ETA[l, n] * R0 / 2))
GK = Gt.subs(Ksub).applyfunc(sp.expand)
# connection part of canonical Theta: Theta^K_{lam nu} = i/2 psi^+ (q_lam Omega_nu - Omega_nu^+ q_lam) psi (both sectors)
def thK(psi, Q_lo, O):
    return sp.Matrix(4, 4, lambda l, n: sp.expand(I / 2 * (psi.H * (Q_lo[l] * O[n] - O[n].H * Q_lo[l]) * psi)[0]))
ThK = (thK(eta, SIG_lo, Om) + thK(chi, SIGT_lo, Omc)).subs(Ksub).applyfunc(sp.expand)
res["G4_G^KK antisymmetric part"] = str((GK - GK.T).applyfunc(sp.factor))
res["G4_Theta^K antisymmetric part"] = str((ThK - ThK.T).applyfunc(sp.factor))
Csym = ((kap * ThK - GK + (kap * ThK - GK).T) / 2).applyfunc(sp.expand)
c_ = sp.Symbol('c_')
e4 = [sp.expand(Csym[l, n] - c_ * kap**2 * ETA[l, n] * J5sq) for l in range(4) for n in range(4)]
s4 = sp.solve([e for e in e4 if e != 0][0], c_)
res["G4_(kappa Theta^K - G^KK)_sym = c kappa^2 g J5.J5, c ="] = str(s4)
res["G4_all_components"] = bool(s4) and all(sp.expand(e.subs(c_, s4[0])) == 0 for e in e4)

# G4b: consistency with the effective (Hehl-Datta) action. On the torsion-modified shell the full
# L_M = L0_M + L^K_M vanishes, so L0_M = -L^K_M != 0, and the effective source is
# T_eff = [Theta0_can]_sym - g L0_M - g L_eff.  G0 = kappa T_eff  <=>  (3/16) kappa J5^2 = L^K_M - L_eff
LMK = sp.expand((I / 2 * ((eta.H * sum((SIG[m] * Om[m] - Om[m].H * SIG[m] for m in range(4)), sp.zeros(2)) * eta)[0]
                          + (chi.H * sum((SIGT[m] * Omc[m] - Omc[m].H * SIGT[m] for m in range(4)), sp.zeros(2)) * chi)[0])).subs(Ksub))
RKK = sp.expand(R0.subs(Ksub))
Leff = sp.expand(-RKK / (2 * kap) + LMK)
res["G4b_L^K_M at solution / (kappa J5^2)"] = str(sp.simplify(LMK / (kap * J5sq)))
res["G4b_-R^KK/(2kappa) at solution / (kappa J5^2)"] = str(sp.simplify(-RKK / (2 * kap) / (kap * J5sq)))
res["G4b_L_eff / (kappa J5^2)"] = str(sp.simplify(Leff / (kap * J5sq)))
res["G4b_G0 = kappa(T_Tetrode - g L_eff) consistent: (3/16) kappa J5^2 == L^K_M - L_eff"] = sp.expand(LMK - Leff - sp.Rational(3, 16) * kap * J5sq) == 0

# ------------------------------------------------------------------ G5 antisymmetric O(kappa), flat, on-shell Dirac
t, x, y, z = X = sp.symbols('t x y z', real=True)
ef = [sp.Function(f'e{i}')(*X) for i in (1, 2)]; ebf = [sp.Function(f'eb{i}')(*X) for i in (1, 2)]
cf_ = [sp.Function(f'c{i}')(*X) for i in (1, 2)]; cbf = [sp.Function(f'cb{i}')(*X) for i in (1, 2)]
E_ = sp.Matrix(ef); Eb = sp.Matrix([ebf]); C_ = sp.Matrix(cf_); Cb = sp.Matrix([cbf])
jE = [sp.expand((Eb * SIG[a] * E_)[0]) for a in range(4)]; jC = [sp.expand((Cb * SIGT[a] * C_)[0]) for a in range(4)]
J5f = [jE[a] - jC[a] for a in range(4)]
Kf = {(r, a, b): -kap / 4 * sum(eps_lo(r, a, b, d) * J5f[d] for d in range(4)) for r in range(4) for a in range(4) for b in range(4)}
def Wf(m, a, b): return ETA[a, a] * Kf[(m, a, b)]
# linear Riemann R_{mn}{}^a{}_b = d_m w_n^a_b - d_n w_m^a_b ; Ricci as in G2: A_{l n} = R_{m n}{}^m{}_l
Al = sp.Matrix(4, 4, lambda l, n: sum(sp.diff(Wf(n, m, l), X[m]) - sp.diff(Wf(m, m, l), X[n]) for m in range(4)))
# canonical Theta (flat, no connection) antisymmetric part
def th0(Pb, Q_lo, P):
    return sp.Matrix(4, 4, lambda l, n: I / 2 * ((Pb * Q_lo[l] * P.diff(X[n]))[0] - (Pb.diff(X[n]) * Q_lo[l] * P)[0]))
Th0 = th0(Eb, SIG_lo, E_) + th0(Cb, SIGT_lo, C_)
solE = -(SIG[1] * E_.diff(x) + SIG[2] * E_.diff(y) + SIG[3] * E_.diff(z))
solEb = -(Eb.diff(x) * SIG[1] + Eb.diff(y) * SIG[2] + Eb.diff(z) * SIG[3])
solC = -(SIGT[1] * C_.diff(x) + SIGT[2] * C_.diff(y) + SIGT[3] * C_.diff(z))
solCb = -(Cb.diff(x) * SIGT[1] + Cb.diff(y) * SIGT[2] + Cb.diff(z) * SIGT[3])
os_ = {}
for i in range(2):
    os_[sp.diff(ef[i], t)] = solE[i]; os_[sp.diff(ebf[i], t)] = solEb[i]
    os_[sp.diff(cf_[i], t)] = solC[i]; os_[sp.diff(cbf[i], t)] = solCb[i]
Dif = ((Al - Al.T) / 2 - kap * (Th0 - Th0.T) / 2).applyfunc(lambda v: sp.simplify(sp.expand(sp.expand(v).subs(os_))))
res["G5_G_[lam nu](dK) - kappa Theta_[lam nu] on free shell (flat, O(kappa))"] = str(Dif) if Dif != sp.zeros(4, 4) else "0"
# off shell, for contrast
Dif_off = ((Al - Al.T) / 2 - kap * (Th0 - Th0.T) / 2).applyfunc(lambda v: sp.expand(v))
res["G5_same_off_shell_is_zero"] = Dif_off == sp.zeros(4, 4)

# ------------------------------------------------------------------ G6 matter EOMs with torsion
# eta^+ variation of i/2(eta^+ q eta_; - eta^+_; q eta) at a point, flat frame, connection = K:
#   i [ sigma^mu d_mu eta + 1/2 (sigma^mu Om_mu - Om_mu^+ sigma^mu) eta ]
tor_eta = sum(((SIG[m] * Om[m] - Om[m].H * SIG[m]) / 2 for m in range(4)), sp.zeros(2)).subs(Ksub).applyfunc(sp.expand)
tor_chi = sum(((SIGT[m] * Omc[m] - Omc[m].H * SIGT[m]) / 2 for m in range(4)), sp.zeros(2)).subs(Ksub).applyfunc(sp.expand)
g6 = sp.Symbol('g6')
slash_eta = sum((J5lo[a] * SIG[a] for a in range(4)), sp.zeros(2))     # J5_a sigma^a
slash_chi = sum((J5lo[a] * SIGT[a] for a in range(4)), sp.zeros(2))
def fitc(M, S):
    e = [sp.expand(v) for v in (M - g6 * kap * S)]
    nz = [v for v in e if v != 0]
    s = sp.solve(nz[0], g6) if nz else []
    return (s[0], all(sp.expand(v.subs(g6, s[0])) == 0 for v in e)) if s else (None, False)
res["G6_eta_torsion_term = g kappa J5_a sigma^a, g ="] = str(fitc(tor_eta, slash_eta))
res["G6_chi_torsion_term = g kappa J5_a sigma~^a, g ="] = str(fitc(tor_chi, slash_chi))
# compare with d/d(eta^+) of L_eff = (3 kappa/16) J5.J5 : (3 kappa/16)*2*J5_a sigma^a eta ; kinetic term gives i*(sigma d eta)
# so EOM  i sigma.d eta + i*torsion*eta  must equal  i sigma.d eta + (3k/8) J5.sigma eta  up to overall factor
res["G6_expected_from_L_eff_(i*g = 3/8 for eta, -3/8 for chi)"] = "check: i*g_eta == 3/8 and i*g_chi == -3/8"

# ------------------------------------------------------------------ G7 the p.29 note
epsm = sp.Matrix([[0, 1], [-1, 0]])
ok_a = all(sp.expand(Omc[r] + Om[r].H) == sp.zeros(2) for r in range(4))
ok_b = all(sp.expand(epsm * Om[r].conjugate() * epsm.inv() + Om[r].H) == sp.zeros(2) for r in range(4))
ok_c = all(sp.expand(epsm * Om[r].conjugate() * epsm.inv() - Omc[r]) == sp.zeros(2) for r in range(4))
ok_t = all(sp.expand(Omc[r].T - Om[r]) == sp.zeros(2) for r in range(4))
ok_tm = all(sp.expand(-Omc[r].T - Om[r]) == sp.zeros(2) for r in range(4))
ok_e = all(sp.expand(epsm * Omc[r].T * epsm.inv() + Om[r]) == sp.zeros(2) for r in range(4))
ok_e2 = all(sp.expand(epsm * Omc[r].T * epsm.inv() - Om[r]) == sp.zeros(2) for r in range(4))
res["G7_Omega^chi = -Omega^+"] = ok_a
res["G7_eps Omega^* eps^-1 = -Omega^+"] = ok_b
res["G7_eps Omega^* eps^-1 = Omega^chi (chi = eps eta^* is covariant)"] = ok_c
res["G7_(Omega^chi)^T = Omega"] = ok_t
res["G7_-(Omega^chi)^T = Omega"] = ok_tm
res["G7_eps (Omega^chi)^T eps^-1 = -Omega"] = ok_e
res["G7_eps (Omega^chi)^T eps^-1 = +Omega"] = ok_e2
# chi = eps eta^* : does the chi EOM follow from the eta EOM?  sigma~^mu eps = eps sigma^mu*  ?
res["G7_sigma~^mu eps = eps (sigma^mu)^*"] = all(sp.expand(SIGT[m] * epsm - epsm * SIG[m].conjugate()) == sp.zeros(2) for m in range(4))

if __name__ == "__main__":
    print(json.dumps(res, indent=2, default=str))
    out = here.parents[2] / "test-results" / "notebook-recon" / "NB-038_q_field_equations.json"
    out.write_text(json.dumps(res, indent=2, default=str))
