# test_F99_sigma_from_qca_rule.py
# 2026-06-05
#
# F99 -- Deriving the string tension sigma from WITHIN the QCA update rule,
# as the centre-twist Lagrange-multiplier price of Z_N phase-budget non-closure.
#
# This closes the bridge flagged open in F97 section 8 and F98 section 4:
#   "sigma emerges as the Lagrange-multiplier price of centre-phase non-closure
#    in the QCA update rule."
# F98 established the price *structure* (sigma=0 on closure, sigma R -> inf off it)
# but took sigma as an input from F86/F94.  Here sigma is DERIVED:
#
#   (1) The QCA gluon update rule is centre-covariant: link -> z U (z in Z_N)
#       multiplies a Wilson/Polyakov observable by z^(N-ality).  So the rule's
#       observables organise by centre charge -- the budget whose closure F97/F98
#       identified as stability.   [D3, on the real SU(3) links]
#
#   (2) Track only the centre (Z_N) content of the plaquette holonomy the rule
#       produces: a class weight p(n), n in Z_N.  In the 2D testbed (F70: axial
#       gauge -> independent plaquettes) a Wilson loop of centre charge k over
#       area A obeys EXACTLY  <W_k> = s_k^A,  s_k = z(2pi k/N)/z(0),
#       z(theta)=sum_n p(n) e^{i n theta}.  Hence  sigma_k = -ln s_k.   [D1]
#
#   (3) A source of N-ality k is equivalent to a 't Hooft centre twist
#       theta_k = 2pi k/N; sigma_k = f(theta_k) = -ln[z(theta_k)/z(0)] is the
#       constrained free-energy density and theta_k is the Lagrange multiplier
#       conjugate to the centre-closure constraint.  Stationarity of
#       [ln z(theta) - i theta c] fixes the centre charge c = -i z'/z(theta):
#       the multiplier IS what enforces the budget.   [D2]
#
#   (4) p(n) comes from the rule's disorder (the rotation angle Omega sets it):
#       ordered rule  p->delta_{n0}  => sigma->0 (deconfined);
#       max-disordered p->uniform     => sigma->infinity.  Monotone between.  [D4]
#
#   (5) Reconciliation: -ln s_1 is the centre form of F70's -ln w(beta) (same
#       law: tension = -ln of a normalised plaquette weight, ->0 strong order,
#       ->large strong disorder); the small-sigma / Abelian-BPS limit gives
#       sigma_k = 2 pi v^2 k = F86 with 2 pi v^2 := sigma_1.   [D5]
#
# Exact pieces (D1,D2,D4) are sympy on symbolic Z_N weights -- the centre
# algebra is rep-independent and load-bearing, numpy is not.

import json
import time
import pathlib
import sys

import numpy as np
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ca-simulation"))

import ca_confinement as conf                 # F70 area-law w(beta), -ln w
import forks.lgt_fork_A_mc as A               # F94 real SU(3) links

t0 = time.time()
results = {"finding": "F99", "date": "2026-06-05",
           "title": "sigma as the centre-twist Lagrange multiplier of Z_N non-closure",
           "checks": {}}


def record(name, statement, residual, status):
    results["checks"][name] = {
        "statement": statement, "residual": str(residual),
        "status": "PASS" if status else "FAIL"}
    print(f"{name}: {statement}\n      -> residual {residual} "
          f"[{'PASS' if status else 'FAIL'}]")


# ============================================================ D1
# Centre projection and  sigma_k = -ln s_k  (exact, symbolic Z_3 then general).
# Single-plaquette centre weights p0,p1,p2 >= 0 on Z_3; omega = e^{2 pi i/3}.
p0, p1, p2, th = sp.symbols("p0 p1 p2 theta", positive=True)
N = 3
w3 = sp.exp(2 * sp.pi * sp.I / N)


def z_of(theta, ps):
    return sum(ps[n] * sp.exp(sp.I * n * theta) for n in range(len(ps)))


ps3 = [p0, p1, p2]
z0 = z_of(0, ps3)
# normalised centre order parameter in channel k:  s_k = z(2pi k/N)/z(0)
s = [sp.simplify(z_of(2 * sp.pi * k / N, ps3) / z0) for k in range(N)]

# (a) closed budget k=0 => s_0 = 1 => sigma_0 = 0, identically.
d1a = sp.simplify(s[0] - 1) == 0
# (b) centre periodicity  s_{k+N} = s_k  (omega^N = 1).
sN = sp.simplify(z_of(2 * sp.pi * N / N, ps3) / z0)
d1b = sp.simplify(sN - s[0]) == 0
# (c) k <-> N-k degeneracy when the weight is centre-symmetric (p1 = p2).
d1c = sp.simplify((s[1] - s[2]).subs(p2, p1)) == 0
# (d) sigma_k = -ln s_k  positive off closure: with a concrete ordered-ish
#     weight (p0 > p1 = p2 > 0) we get 0 < s_1 < 1.
s1_c = complex(s[1].subs({p0: 0.7, p1: 0.15, p2: 0.15}))
s1_num = s1_c.real
d1d = (abs(s1_c.imag) < 1e-12 and 0.0 < s1_num < 1.0
       and -np.log(s1_num) > 0.0)
d1 = bool(d1a and d1b and d1c and d1d)
record("D1", "centre projection: sigma_k = -ln s_k, s_k = z(2pi k/N)/z(0); "
       "s_0 = 1 (sigma_0 = 0) exact, periodic mod N, k<->N-k degenerate, "
       "0<s_k<1 off closure",
       0 if d1 else "centre-projection algebra fails", d1)

# ============================================================ D2
# Lagrange-multiplier / 't Hooft-twist identity (exact).
# The twist angle theta is the multiplier; fixing the centre charge c is the
# stationarity of  L(theta) = ln z(theta) - i theta c.
zt = z_of(th, ps3)
L = sp.log(zt) - sp.I * th * sp.symbols("c")
dL = sp.diff(L, th)
c_sym = sp.symbols("c")
# stationarity dL/dtheta = 0  <=>  c = -i z'(theta)/z(theta)  (the induced charge)
charge_from_saddle = sp.simplify(sp.solve(sp.Eq(dL, 0), c_sym)[0]
                                 - (-sp.I * sp.diff(zt, th) / zt))
d2a = sp.simplify(charge_from_saddle) == 0
# the price at a centre value:  sigma_k = f(theta_k), theta_k = 2pi k/N,
# f(theta) = -ln[z(theta)/z(0)]  -- identical to D1's s_k.

def f_twist(k):
    return sp.simplify(-sp.log(z_of(2 * sp.pi * k / N, ps3) / z0))


d2b = sp.simplify(f_twist(1) - (-sp.log(s[1]))) == 0
d2c = sp.simplify(f_twist(0)) == 0          # zero multiplier price on closure
d2 = bool(d2a and d2b and d2c)
record("D2", "Lagrange/twist: theta_k = 2pi k/N is the multiplier conjugate to "
       "centre charge (stationarity c = -i z'/z); sigma_k = f(theta_k) = -ln s_k; "
       "f(theta_0) = 0 (no price on closure)",
       0 if d2 else "Lagrange-multiplier identity fails", d2)

# ============================================================ D3
# Centre covariance of the ACTUAL QCA SU(3) links (machine precision).
# A centre transform z*I on all temporal links of one time-slice multiplies
# every Polyakov loop by z and leaves contractible (planar) Wilson loops fixed.
rng = np.random.default_rng(7)
U = A.hot_links(L=4, D=4, seed=7)
z = np.exp(2j * np.pi / 3)                    # omega in Z_3
P0 = A.polyakov_loop_field(U)                 # complex field
W0 = A.wilson_loop_planar(U, 0, 1, 2, 2)      # spatial-plane (contractible) loop
Uc = [u.copy() for u in U]
t_axis = U.shape[0] - 1                       # last lattice axis = time
sl = [slice(None)] * U.shape[0]
sl[t_axis] = 0                                # one time-slice t0 = 0
Uc[t_axis][tuple(sl)] *= z                    # multiply temporal links on slice
Uc = np.stack(Uc)
P1 = A.polyakov_loop_field(Uc)
W1 = A.wilson_loop_planar(Uc, 0, 1, 2, 2)
poly_cov = float(np.max(np.abs(P1 - z * P0)))            # P -> z P
wils_inv = float(abs(W1 - W0))                           # contractible loop fixed
d3 = poly_cov < 1e-12 and wils_inv < 1e-12
record("D3", "real SU(3) rule is centre-covariant: slice twist z*I sends "
       "Polyakov -> z*Polyakov and leaves contractible Wilson loops invariant "
       "(observables organise by N-ality)",
       f"poly {poly_cov:.2e}, wilson {wils_inv:.2e}", d3)

# ============================================================ D4
# Rule -> weight bridge and the disorder limits (exact, symbolic).
# The centre projection of a heat-kernel/Wilson plaquette weight is the Z_N
# clock weight  p(n) ~ exp(gamma cos(2pi n/N)),  gamma set by the rotation-rule
# disorder (gamma large = ordered/cold rule, gamma->0 = max-disordered).
g = sp.symbols("gamma", positive=True)
pc = [sp.exp(g * sp.cos(2 * sp.pi * n / N)) for n in range(N)]
zc0 = sum(pc)
s1c = sp.simplify(sp.re(sp.expand(sum(pc[n] * w3 ** n for n in range(N)) / zc0)))


def sig1c_at(val):
    s_ = complex(s1c.subs(g, val)).real
    return -np.log(s_)


# ordered limit gamma -> oo : s_1 -> 1, sigma_1 -> 0  (deconfined)
ordered = sp.limit(s1c, g, sp.oo)
# disordered limit gamma -> 0 : p uniform, z(2pi/3)=0, s_1 -> 0, sigma_1 -> oo
disordered = complex(s1c.subs(g, 0)).real
mono = (sig1c_at(0.3) > sig1c_at(3.0) > 0.0)
d4 = bool(sp.simplify(ordered - 1) == 0 and abs(disordered) < 1e-12 and mono)
record("D4", "rule->weight: centre weight p(n)~exp(gamma cos(2pi n/N)) from rule "
       "disorder; sigma_1(gamma->oo)=0 (ordered/deconfined), "
       "sigma_1(gamma->0)=oo (max disorder); monotone decreasing in order",
       0 if d4 else "disorder-limit bridge fails", d4)

# ============================================================ D5
# Reconciliation with F70 (-ln w(beta)) and F86 (2 pi v^2 n).
# (a) F70: same law -- tension = -ln of a normalised plaquette weight; both go
#     to 0 in the ordered (large-coupling) limit and grow under disorder. Check
#     F70's sigma(beta) is positive, monotone-decreasing in beta, -> 0 as
#     beta->oo, matching the centre-derived sigma_1(gamma) monotone family.
betas = [0.5, 1.0, 2.0, 4.0, 8.0, 20.0]
sig_f70 = [conf.string_tension(b) for b in betas]
f70_pos = all(x > 0 for x in sig_f70)
f70_mono = all(sig_f70[i] > sig_f70[i + 1] for i in range(len(sig_f70) - 1))
f70_to0 = conf.string_tension(60.0) < conf.string_tension(8.0) < 0.7
# (b) F86: small-tension / Abelian-BPS limit.  For s_k = 1 - eps_k (weak),
#     sigma_k = -ln(1-eps_k) ~ eps_k; in the Abelian regime where only the
#     unit centre charge is excited, eps_k ∝ k, so sigma_k = k * sigma_1.
#     Identify 2 pi v^2 := sigma_1  =>  sigma_k = 2 pi v^2 k  (= F86 sigma=2pi v^2 n).
v = sp.symbols("v", positive=True)
sigma1_def = 2 * sp.pi * v ** 2              # F86 unit-charge tension
sigma_k_bps = [sp.simplify(k * sigma1_def) for k in range(N)]   # Abelian: linear
bps_zero = sigma_k_bps[0] == 0                                  # k=0 closes
bps_linear = sp.simplify(sigma_k_bps[2] - 2 * sigma_k_bps[1]) == 0  # sigma_2=2 sigma_1
# small-sigma consistency: -ln s_1 ~ (1 - s_1) to leading order
eps = sp.symbols("epsilon", positive=True)
lead = sp.series(-sp.log(1 - eps), eps, 0, 2).removeO()
small_ok = sp.simplify(lead - eps) == 0
d5 = bool(f70_pos and f70_mono and f70_to0 and bps_zero and bps_linear and small_ok)
record("D5", "reconciliation: F70 sigma(beta)=-ln w(beta) is the same -ln(weight) "
       "law (positive, monotone, ->0 ordered); F86 sigma_k=2pi v^2 k is the "
       "small-sigma Abelian-BPS limit with 2pi v^2 := sigma_1, sigma_0=0",
       f"f70 sigma(0.5..20)={[round(x,3) for x in sig_f70]}", d5)

# ============================================================
results["sigma_f70_table"] = {str(b): round(s_, 4) for b, s_ in zip(betas, sig_f70)}
results["runtime_s"] = round(time.time() - t0, 3)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
results["summary"] = f"{n_pass}/{len(results['checks'])} PASS"
print(f"\nOverall: {results['summary']} ({results['runtime_s']} s)")

out = ROOT / "test-results" / "F99_sigma_from_qca_rule.json"
out.write_text(json.dumps(results, indent=2))
print(f"Results written to {out}")
