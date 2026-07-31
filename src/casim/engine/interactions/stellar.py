"""
ca_stellar.py  --  Hydrostatic stellar structure: GR (TOV) vs the dielectric model
===================================================================================

The NICER-overlay step from FC09 / F173.  Both theories agree in the Newtonian
limit and in the *exterior* (M = integral of rho, beta = gamma = 1); they
diverge in the relativistic interior because the single-scalar dielectric
sources gravity from energy density only (F173).  Here we close each theory's
hydrostatic structure and integrate it, producing mass-radius and
surface-redshift-vs-mass curves to overlay on neutron-star data.

Equations (geometric units G = c = 1; lengths in km, masses in km,
1 Msun = 1.476625 km; energy density & pressure in km^-2):

GR -- Tolman-Oppenheimer-Volkoff:
    dm/dr  = 4 pi r^2 rho
    dp/dr  = -(rho + p)(m + 4 pi r^3 p) / (r (r - 2 m))
    surface redshift  z = (1 - 2M/R)^(-1/2) - 1.

MODEL -- dielectric (literal F106 law: energy-only source, exponential metric):
    dmE/dr = 4 pi r^2 rho                       (energy density only -- no pressure)
    dp/dr  = -(rho + p) mE / r^2                (Euler eq. in g_tt = -e^{-2u},
                                                 with the F106 potential u' = -mE/r^2;
                                                 NO relativistic denominator, NO 3p)
    exterior  K = e^{2 M_E/r}  =>  z = e^{M_E/R} - 1.

The two differ by exactly (i) the pressure term in the mass source and (ii) the
(1 - 2m/r) spatial-curvature denominator -- both consequences of one
energy-sourced scalar.  IMPORTANT: this uses the *literal* F106 weak-field law
(flat Laplacian) extended to strong field; a covariant extension is an
untested alternative that could soften the strong-field divergence (see F174).

Self-contained: numpy + a local RK4 (no scipy; CLAUDE.md self-contained numerics).
"""

import numpy as np

MSUN_KM = 1.476625      # GM_sun/c^2 in km


# ======================================================================
# Equation of state (Gamma-law polytrope; swap in a tabulated EoS here)
# ======================================================================
class Polytrope:
    """p = K rho^Gamma, rho the total energy density (geometric units)."""
    def __init__(self, K, Gamma=2.0):
        self.K, self.Gamma = float(K), float(Gamma)

    def p_of_rho(self, rho):
        return self.K * np.maximum(rho, 0.0) ** self.Gamma

    def rho_of_p(self, p):
        return (np.maximum(p, 0.0) / self.K) ** (1.0 / self.Gamma)


# ======================================================================
# Right-hand sides
# ======================================================================
def _tov_rhs(r, m, p, eos):
    rho = eos.rho_of_p(p)
    dm = 4.0 * np.pi * r**2 * rho
    dp = -(rho + p) * (m + 4.0 * np.pi * r**3 * p) / (r * (r - 2.0 * m))
    return dm, dp


def _model_rhs(r, mE, p, eos):
    rho = eos.rho_of_p(p)
    dmE = 4.0 * np.pi * r**2 * rho
    dp = -(rho + p) * mE / r**2           # energy-only source, exponential metric
    return dmE, dp


# ======================================================================
# Integrator (RK4 with linear surface refinement at p -> 0)
# ======================================================================
def integrate_star(rho_c, theory, eos, h=1e-3, rmax=400.0):
    """Integrate one star of central density rho_c.  theory in {'gr','model'}.
    Returns (R_km, M_km, z_surf).  M is the gravitational mass an external
    observer infers (Schwarzschild M for GR; exterior M_E for the model)."""
    rhs = _tov_rhs if theory == "gr" else _model_rhs
    r, m, p = 1e-6, 0.0, eos.p_of_rho(rho_c)
    p_floor = 1e-14 * p
    while p > p_floor and r < rmax:
        k1m, k1p = rhs(r, m, p, eos)
        k2m, k2p = rhs(r + h/2, m + h/2*k1m, p + h/2*k1p, eos)
        k3m, k3p = rhs(r + h/2, m + h/2*k2m, p + h/2*k2p, eos)
        k4m, k4p = rhs(r + h, m + h*k3m, p + h*k3p, eos)
        m_new = m + h/6*(k1m + 2*k2m + 2*k3m + k4m)
        p_new = p + h/6*(k1p + 2*k2p + 2*k3p + k4p)
        if p_new <= 0.0:                  # crossed the surface; refine linearly
            frac = p / (p - p_new)
            r += frac * h
            m += frac * (m_new - m)
            p = 0.0
            break
        r, m, p = r + h, m_new, p_new
    R, M = r, m
    if theory == "gr":
        z = (1.0 - 2.0*M/R) ** -0.5 - 1.0
    else:
        z = np.exp(M / R) - 1.0           # exterior K = e^{2 M_E/r}
    return R, M, z


def mass_radius_curve(rho_c_array, theory, eos, **kw):
    """Return dict of arrays: R_km, M_msun, z_surf over central densities."""
    R, M, Z = [], [], []
    for rc in rho_c_array:
        r, m, z = integrate_star(rc, theory, eos, **kw)
        R.append(r); M.append(m / MSUN_KM); Z.append(z)
    return {"rho_c": np.asarray(rho_c_array), "R_km": np.array(R),
            "M_msun": np.array(M), "z_surf": np.array(Z)}


def max_mass(curve):
    """Maximum gravitational mass on a curve and whether a turnover (TOV-style
    stable/unstable transition) is present within the sampled range."""
    M = curve["M_msun"]
    i = int(np.argmax(M))
    turned_over = i < len(M) - 1               # peak is interior to the range
    return {"M_max_msun": float(M[i]), "R_at_max_km": float(curve["R_km"][i]),
            "turnover_present": bool(turned_over)}


# ======================================================================
# Covariant dielectric variant (F175): the exact-G_tt energy source with
# curvature feedback, optionally restoring the GR (rho+3p) source.
#
# Field equation (from the exact Einstein G^t_t of the dielectric metric,
# F173), in first-order form with s = r^2 u':
#     u' = s / r^2
#     s' = -(1/2)[ s^2/r^2 + 8 pi * src * e^{2u} * r^2 ],   src in {rho, rho+3p}
#     p' = (rho + p) u'                      (Euler eq. in g_tt = -e^{-2u})
# The e^{2u} curvature weighting couples to the ABSOLUTE potential, so u is
# fixed by a boundary-value shoot enforcing u(infinity) = 0.  The vacuum tail
# is integrated in closed form (s' = -s^2/2r^2), so we only integrate to the
# stellar surface:
#     u_inf = u_R + 2 ln(1 + s_R/(2R)),     M_E = -1/(1/s_R + 1/(2R)).
# ======================================================================
def _cov_deriv(r, u, s, p, eos, source):
    rho = eos.rho_of_p(p)
    src = rho if source == "energy" else rho + 3.0 * p
    up = s / r**2
    sp = -0.5 * (s**2 / r**2 + 8.0 * np.pi * src * np.exp(2.0 * u) * r**2)
    pp = (rho + p) * up
    return up, sp, pp


def _cov_to_surface(u_c, rho_c, eos, source, h=5e-3):
    p_c = eos.p_of_rho(rho_c)
    p_floor = 1e-12 * p_c
    r = 1e-4
    upp0 = -(4.0 * np.pi / 3.0) * rho_c * np.exp(2.0 * u_c)   # u''(0), regularity
    u = u_c + 0.5 * upp0 * r**2
    s = r**2 * (upp0 * r)
    p = p_c
    while p > p_floor and r < 200.0:
        k1 = _cov_deriv(r, u, s, p, eos, source)
        k2 = _cov_deriv(r + h/2, u + h/2*k1[0], s + h/2*k1[1], p + h/2*k1[2], eos, source)
        k3 = _cov_deriv(r + h/2, u + h/2*k2[0], s + h/2*k2[1], p + h/2*k2[2], eos, source)
        k4 = _cov_deriv(r + h, u + h*k3[0], s + h*k3[1], p + h*k3[2], eos, source)
        u2 = u + h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        s2 = s + h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        p2 = p + h/6*(k1[2]+2*k2[2]+2*k3[2]+k4[2])
        if p2 <= 0.0:
            frac = p / (p - p2)
            return r + frac*h, u + frac*(u2-u), s + frac*(s2-s)
        u, s, p, r = u2, s2, p2, r + h
    return r, u, s


def _cov_uinf_M(u_c, rho_c, eos, source):
    R, uR, sR = _cov_to_surface(u_c, rho_c, eos, source)
    u_inf = uR + 2.0 * np.log(1.0 + sR / (2.0 * R))     # analytic vacuum tail
    M_E = -1.0 / (1.0 / sR + 1.0 / (2.0 * R))
    return u_inf, R, M_E, uR


def solve_covariant(rho_c, eos, source="energy"):
    """Shoot on the central potential u_c so that u(infinity) = 0.  Returns
    (R_km, M_E_km, z_surf, u_c)."""
    f = lambda uc: _cov_uinf_M(uc, rho_c, eos, source)[0]
    a, b = 0.0, 0.5
    fa, fb = f(a), f(b)
    for _ in range(80):
        if abs(fb) < 1e-9:
            break
        denom = (fb - fa) if (fb - fa) != 0 else 1e-30
        c = b - fb * (b - a) / denom
        if c <= -0.9:
            c = -0.9
        a, fa, b, fb = b, fb, c, f(c)
    _, R, M_E, uR = _cov_uinf_M(b, rho_c, eos, source)
    z = np.exp(uR) - 1.0
    return R, M_E, z, b


def covariant_mass_radius_curve(rho_c_array, eos, source="energy"):
    R, M, Z = [], [], []
    for rc in rho_c_array:
        r, m, z, _ = solve_covariant(rc, eos, source)
        R.append(r); M.append(m / MSUN_KM); Z.append(z)
    return {"rho_c": np.asarray(rho_c_array), "R_km": np.array(R),
            "M_msun": np.array(M), "z_surf": np.array(Z)}


# ----------------------------------------------------------------------
# Two-piece polytrope (Read-et-al-style framework) for a realistic-EoS run.
# Parameters here are a REPRESENTATIVE stiff-core set (not the published SLy
# digits); swap in tabulated SLy/APR values from Read et al. 2009 as a drop-in.
# ----------------------------------------------------------------------
class TwoPiecePolytrope:
    def __init__(self, K1, G1, rho_break, G2):
        self.K1, self.G1, self.rho_break, self.G2 = K1, G1, rho_break, G2
        self.p_break = K1 * rho_break**G1
        self.K2 = self.p_break / rho_break**G2     # pressure continuity
        self.p_of_rho = np.vectorize(self._p_of_rho)
        self.rho_of_p = np.vectorize(self._rho_of_p)

    def _p_of_rho(self, rho):
        rho = max(rho, 0.0)
        return self.K1*rho**self.G1 if rho < self.rho_break else self.K2*rho**self.G2

    def _rho_of_p(self, p):
        p = max(p, 0.0)
        return (p/self.K1)**(1.0/self.G1) if p < self.p_break else (p/self.K2)**(1.0/self.G2)


def at_fixed_mass(curve, M_target_msun):
    """Interpolate R and z at a target gravitational mass (rising branch)."""
    M, R, Z = curve["M_msun"], curve["R_km"], curve["z_surf"]
    i = int(np.argmax(M))                       # restrict to rising branch
    Mr, Rr, Zr = M[:i+1], R[:i+1], Z[:i+1]
    if M_target_msun < Mr.min() or M_target_msun > Mr.max():
        return None
    R_t = float(np.interp(M_target_msun, Mr, Rr))
    z_t = float(np.interp(M_target_msun, Mr, Zr))
    return {"M_msun": M_target_msun, "R_km": R_t, "z_surf": z_t}
