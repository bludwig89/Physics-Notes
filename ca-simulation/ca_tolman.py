"""
ca_tolman.py  --  GR-vs-model pressure / Tolman sector
=======================================================

The open discriminator flagged in FC08.  In general relativity the source of
the *time* potential (clock rate, slow-particle orbits) is the trace-reversed
stress-energy, R_00 = (4 pi G/c^2)(rho + 3p/c^2): pressure gravitates (the
Tolman term).  The F64/F106 dielectric sources a SINGLE scalar K from the
energy density alone, nabla^2 ln K = -(8 pi G/c^4) T^00.  A single scalar
cannot carry both GR interior metric functions independently, so the question
is sharp: does the dielectric reproduce the +3p Tolman source, or omit it?

This module answers it two ways:

  (A) SYMBOLIC.  The exact Einstein tensor of the isotropic dielectric metric
      ds^2 = -(1/K) dt^2 + K (dr^2 + r^2 dOmega^2),  K = e^{2u(r)},
      has mixed components

        8 pi rho_eff = -e^{-2u} ( u'^2 + 2 u'' + (4/r) u' )
        8 pi p_r     = -e^{-2u} u'^2
        8 pi p_t     = +e^{-2u} u'^2.

      So (i) at leading order 8 pi rho = -nabla^2(ln K)  [confirms F106], and
      (ii) the only stress the scalar carries is the ANISOTROPIC field stress
      p_r = -p_t = O(u'^2) -- there is NO isotropic matter-pressure source.
      Matter pressure p is therefore absent from the source: the model uses
      rho only, GR uses rho + 3p.

  (B) QUANTITATIVE.  Exterior fields agree (both carry M = integral of rho, so
      every solar-system / exterior test is identical, beta = gamma = 1).  The
      divergence is interior / strong-field: for a uniform sphere the central
      time-dilation differs from GR at O(s^2), s = GM/(R c^2), with the exact
      leading coefficient -15/4.  Null in the solar system (~1e-11), but
      2%-42% for neutron stars (s = 0.1-0.3) -- a genuine, testable departure.

Symbolic via sympy; numeric via mpmath.  Standalone.
"""

import sympy as sp
import mpmath as mp


# ======================================================================
# (A) exact effective source of the dielectric metric
# ======================================================================
def effective_source_symbolic():
    """Return (rho8pi, pr8pi, pt8pi, u, r): the exact 8*pi*{rho,p_r,p_t} of the
    isotropic dielectric metric, as sympy expressions in u(r)."""
    r = sp.symbols('r', positive=True)
    u = sp.Function('u')(r)
    K = sp.exp(2 * u)
    g = sp.diag(-1 / K, K, K * r**2, K * r**2 * sp.sin(sp.symbols('theta'))**2)
    th = sp.symbols('theta')
    g = sp.diag(-1 / K, K, K * r**2, K * r**2 * sp.sin(th)**2)
    ginv = g.inv()
    coords = [sp.symbols('t'), r, th, sp.symbols('phi')]
    n = 4
    Gamma = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                Gamma[a][b][c] = sp.simplify(sum(
                    ginv[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
                                  - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
    Ric = sp.zeros(n)
    for b in range(n):
        for c in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(Gamma[a][b][c], coords[a]) - sp.diff(Gamma[a][b][a], coords[c])
                for d in range(n):
                    s += Gamma[a][a][d] * Gamma[d][b][c] - Gamma[a][c][d] * Gamma[d][b][a]
            Ric[b, c] = sp.simplify(s)
    Rs = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    Gmix = sp.simplify(ginv * (Ric - sp.Rational(1, 2) * g * Rs))
    rho8pi = sp.simplify(-Gmix[0, 0])
    pr8pi = sp.simplify(Gmix[1, 1])
    pt8pi = sp.simplify(Gmix[2, 2])
    return rho8pi, pr8pi, pt8pi, u, r


def leading_density_residual():
    """Check 8*pi*rho_eff = -nabla^2(ln K) + O(u'^2), i.e. the F106 law is the
    leading term.  Returns the exact remainder (should be the e^{-2u} dressing
    times u'^2 plus the (e^{-2u}-1) factor -- all second order)."""
    rho8pi, pr8pi, pt8pi, u, r = effective_source_symbolic()
    lnK = 2 * u
    lap_lnK = sp.diff(lnK, r, 2) + (2 / r) * sp.diff(lnK, r)   # flat spherical Laplacian
    # leading: 8 pi rho ~ -lap_lnK ; remainder:
    remainder = sp.simplify(rho8pi + lap_lnK)
    return remainder, rho8pi, pr8pi, pt8pi


# ======================================================================
# (B) pressure-source statement and the uniform-sphere divergence
# ======================================================================
def source_fraction_omitted(w):
    """Fraction of the GR time-potential source that the model omits, for an
    equation of state p = w rho c^2.  GR sources Phi by (rho + 3p/c^2); the
    model by rho.  Omitted fraction = 3w/(1+3w)."""
    return 3.0 * w / (1.0 + 3.0 * w)


def uniform_sphere_central_gtt_model(s):
    """Model central g_tt for a uniform-density sphere: nabla^2 ln K = -8 pi rho
    (flat Poisson) gives ln K(0) = 3 M/R, so g_tt(0) = -e^{-3s}, s = GM/Rc^2."""
    return -mp.e**(-3 * mp.mpf(s))


def uniform_sphere_central_gtt_gr(s):
    """GR interior Schwarzschild central g_tt(0) = -[ (3/2) sqrt(1-2s) - 1/2 ]^2."""
    s = mp.mpf(s)
    return -(mp.mpf(3) / 2 * mp.sqrt(1 - 2 * s) - mp.mpf(1) / 2)**2


def central_timedilation_fracdiff(s):
    """Fractional difference (model-GR)/GR in central time-dilation sqrt(-g_tt)."""
    m = mp.sqrt(-uniform_sphere_central_gtt_model(s))
    g = mp.sqrt(-uniform_sphere_central_gtt_gr(s))
    return float((m - g) / g)


def leading_coefficient():
    """Exact leading divergence of g_tt(0): model - GR = -(15/4) s^2 + O(s^3)."""
    s = sp.symbols('s', positive=True)
    model = -sp.exp(-3 * s)
    gr = -((sp.Rational(3, 2) * sp.sqrt(1 - 2 * s) - sp.Rational(1, 2))**2)
    return sp.series(model - gr, s, 0, 3).removeO()
