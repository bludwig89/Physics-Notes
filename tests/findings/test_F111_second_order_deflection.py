"""F111 — Second-order light deflection: canonical dielectric K=e^{2u} vs GR.

2026-06-07

F107/L4a proved the straight-ray deflection is exactly -4u_b at all field
strengths. This script computes the next order — the O(u^2) ray-bending term —
where the exponential index can first differ from GR.

Method (exact, sympy):
  A spherically symmetric index n(r) in flat space bends a ray with asymptotic
  impact parameter b by (Bouguer / eikonal, w = b/r):

      Delta_phi = 2 * Integral( dw / sqrt(n(w)^2 - w^2), w=0..w0 ),
      alpha = Delta_phi - pi,    n(w) = n(r=b/w),   n(w0) = w0 (turning point).

  For any index with expansion n = 1 + 2*eps*w + sigma*eps^2*w^2 (eps = GM/(b c^2)),
  truncation at O(eps^2) makes n^2 - w^2 QUADRATIC in w, so the integral is an
  exact arcsin and the series is closed-form:

      alpha = 4*eps + pi*(2 + sigma)*eps^2 + O(eps^3).

  GR (isotropic Schwarzschild, n = (1+x)^3/(1-x), x = m/2r):  sigma = 7/4
      -> alpha_2 = 15*pi/4   (the textbook second-order coefficient: validates
                              the machinery).
  Lattice canonical (F64/F107):  n = K = e^{2u} = 1 + 2u + 2u^2 + ...,  sigma = 2
      -> alpha_2 = 4*pi.
  Deprecated weak-field map (1-u)^{-2} = 1 + 2u + 3u^2: sigma = 3 -> 5*pi (info).

Checks:
  D1  general closed form alpha_2(sigma) = pi*(2+sigma)        [Tier 1, sympy]
  D2  GR cross-check sigma=7/4 -> 15*pi/4                      [Tier 1]
  D3  lattice sigma=2 -> 4*pi; difference vs GR = pi/4 * eps^2 [Tier 1]
  D4  deprecated map sigma=3 -> 5*pi (informational)
  N1  mpmath quadrature of the FULL exponential index -> coefficient -> 4*pi
  N2  solar-limb magnitudes in microarcseconds (IAU constants)

Results JSON: test-results/F111_second_order_deflection.json
"""

import json
import sympy as sp
import mpmath as mp

results = {"finding": "F111", "date": "2026-06-07", "checks": {}}
all_pass = True


def record(name, ok, **info):
    global all_pass
    all_pass = all_pass and ok
    results["checks"][name] = {"pass": bool(ok), **info}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {info}")


# ----------------------------------------------------------------------------
# D1: general second-order deflection for n = 1 + 2 eps w + sigma eps^2 w^2
# ----------------------------------------------------------------------------
eps, w, sigma = sp.symbols("epsilon w sigma", positive=True)
n_gen = 1 + 2 * eps * w + sigma * eps**2 * w**2

# truncate n^2 - w^2 at O(eps^2): higher eps powers cannot affect alpha at O(eps^2)
f2 = sp.expand(n_gen**2 - w**2)
f2 = sum(
    t for t in f2.as_ordered_terms() if sp.degree(sp.Poly(t, eps), eps) <= 2
)
f2 = sp.expand(f2)  # = 1 + 4 eps w - (1 - (4+2 sigma) eps^2) w^2

A = -f2.coeff(w, 2)          # 1 - (4+2 sigma) eps^2
B = f2.coeff(w, 1)           # 4 eps
C = f2.coeff(w, 0)           # 1
assert sp.simplify(A - (1 - (4 + 2 * sigma) * eps**2)) == 0
assert B == 4 * eps and C == 1

# exact integral of a quadratic: Int dw / sqrt(C + B w - A w^2), 0 .. upper root
# = (1/sqrt(A)) * [ pi/2 - arcsin( -B / sqrt(B^2 + 4 A C) ) ]
disc = sp.sqrt(B**2 + 4 * A * C)
delta_phi = 2 / sp.sqrt(A) * (sp.pi / 2 + sp.asin(B / disc))
alpha_gen = sp.series(delta_phi - sp.pi, eps, 0, 3).removeO()

c1 = alpha_gen.coeff(eps, 1)
c2 = sp.simplify(alpha_gen.coeff(eps, 2))
d1_ok = (sp.simplify(c1 - 4) == 0) and (sp.simplify(c2 - sp.pi * (2 + sigma)) == 0)
record("D1_general_closed_form", d1_ok,
       alpha="4*eps + pi*(2+sigma)*eps^2", c1=str(c1), c2=str(c2))

# ----------------------------------------------------------------------------
# D2: GR cross-check — isotropic Schwarzschild index has sigma = 7/4 -> 15 pi/4
# ----------------------------------------------------------------------------
u_ = sp.symbols("u", positive=True)          # u = m/r
x = u_ / 2
n_gr = (1 + x) ** 3 / (1 - x)
ser = sp.series(n_gr, u_, 0, 3).removeO()
sigma_gr = sp.simplify(ser.coeff(u_, 2))     # expect 7/4
alpha2_gr = sp.simplify(c2.subs(sigma, sigma_gr))
d2_ok = (sigma_gr == sp.Rational(7, 4)) and (sp.simplify(alpha2_gr - sp.Rational(15, 4) * sp.pi) == 0)
record("D2_GR_crosscheck_15pi4", d2_ok, sigma_GR=str(sigma_gr), alpha2=str(alpha2_gr))

# ----------------------------------------------------------------------------
# D3: lattice canonical K = e^{2u} has sigma = 2 -> 4 pi; excess over GR = pi/4
# ----------------------------------------------------------------------------
n_lat = sp.exp(2 * u_)
ser = sp.series(n_lat, u_, 0, 3).removeO()
sigma_lat = sp.simplify(ser.coeff(u_, 2))    # expect 2
alpha2_lat = sp.simplify(c2.subs(sigma, sigma_lat))
excess = sp.simplify(alpha2_lat - alpha2_gr)
d3_ok = (sigma_lat == 2) and (sp.simplify(alpha2_lat - 4 * sp.pi) == 0) \
        and (sp.simplify(excess - sp.pi / 4) == 0)
record("D3_lattice_4pi_excess_pi4", d3_ok,
       sigma_lat=str(sigma_lat), alpha2=str(alpha2_lat), excess_over_GR=str(excess))

# ----------------------------------------------------------------------------
# D4 (info): deprecated (1-u)^{-2} map -> sigma = 3 -> 5 pi
# ----------------------------------------------------------------------------
n_dep = (1 - u_) ** -2
sigma_dep = sp.simplify(sp.series(n_dep, u_, 0, 3).removeO().coeff(u_, 2))
alpha2_dep = sp.simplify(c2.subs(sigma, sigma_dep))
record("D4_deprecated_map_info", sigma_dep == 3 and sp.simplify(alpha2_dep - 5 * sp.pi) == 0,
       sigma=str(sigma_dep), alpha2=str(alpha2_dep))

# ----------------------------------------------------------------------------
# N1: numeric guard — FULL exponential index, mpmath quadrature -> 4 pi
# ----------------------------------------------------------------------------
mp.mp.dps = 40


def alpha_exact_exp(e):
    """Deflection for n(w) = exp(2 e w), exact turning point, theta-substitution.

    Integrand written as 1/sqrt(h) with h = f(W)/(w0^2 - W^2), which is regular
    at the turning point (the cos(theta) factors cancel analytically); at the
    endpoint h -> -f'(w0)/(2 w0) by l'Hopital.
    """
    w0 = mp.findroot(lambda W: mp.e ** (2 * e * W) - W, mp.mpf(1) + 2 * e)

    def f(W):
        return mp.e ** (4 * e * W) - W * W

    h_limit = -(4 * e * mp.e ** (4 * e * w0) - 2 * w0) / (2 * w0)

    def integrand(th):
        c = mp.cos(th)
        if c < mp.mpf("1e-12"):
            return 1 / mp.sqrt(h_limit)
        W = w0 * mp.sin(th)
        h = f(W) / (w0 * w0 * c * c)
        return 1 / mp.sqrt(h)

    return 2 * mp.quad(integrand, [0, mp.pi / 2]) - mp.pi


n1_rows, c2_vals = [], []
for e in [mp.mpf("1e-3"), mp.mpf("1e-4"), mp.mpf("1e-5")]:
    a_num = alpha_exact_exp(e)
    coeff = (a_num - 4 * e) / e**2
    c2_vals.append(coeff)
    n1_rows.append({"eps": mp.nstr(e, 3), "alpha2_coeff": mp.nstr(coeff, 12)})
resid = abs(c2_vals[-1] - 4 * mp.pi) / (4 * mp.pi)
n1_ok = resid < 1e-4
record("N1_numeric_full_exponential", n1_ok,
       rows=n1_rows, target=mp.nstr(4 * mp.pi, 12), rel_resid_at_eps_1e5=mp.nstr(resid, 3))

# ----------------------------------------------------------------------------
# N2: solar-limb magnitudes (IAU: GM_sun, R_sun; readout anchors only)
# ----------------------------------------------------------------------------
GM_sun = mp.mpf("1.32712440018e20")   # m^3/s^2 (IAU, G-independent product)
R_sun = mp.mpf("6.957e8")             # m (IAU nominal)
c_si = mp.mpf("299792458.0")
eps_sun = GM_sun / (R_sun * c_si**2)
RAD2UAS = mp.mpf(180) / mp.pi * 3600 * 1e6

first = 4 * eps_sun * RAD2UAS
gr2 = sp.Rational(15, 4) * sp.pi
second_gr = float(gr2) * eps_sun**2 * RAD2UAS
second_lat = 4 * mp.pi * eps_sun**2 * RAD2UAS
diff = (4 * mp.pi - float(gr2)) * eps_sun**2 * RAD2UAS
n2_ok = abs(first / 1e6 - mp.mpf("1.75119")) < 1e-4   # consistency with F107 L4d
record("N2_solar_limb_uas", n2_ok,
       eps_sun=mp.nstr(eps_sun, 8),
       first_order_uas=mp.nstr(first, 8),
       second_order_GR_uas=mp.nstr(second_gr, 6),
       second_order_lattice_uas=mp.nstr(second_lat, 6),
       lattice_minus_GR_uas=mp.nstr(diff, 6))

# ----------------------------------------------------------------------------
results["overall_pass"] = all_pass
out = "test-results/F111_second_order_deflection.json"
with open(out, "w") as fh:
    json.dump(results, fh, indent=2)
print(f"\nOverall: {'ALL PASS' if all_pass else 'FAILURES PRESENT'} -> {out}")
