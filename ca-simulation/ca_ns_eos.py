"""
ca_ns_eos.py  --  Tabulated-EoS neutron stars on the F181 two-function kernel
=============================================================================

Scenario S1 of `docs/roadmaps/gravity-sector-scenarios-2026-06-30.md`.  F181
made the neutron-star interior genuine GR/TOV (two independent metric functions,
the AB==1 single-scalar residual removed).  This module drops a realistic
**piecewise-polytrope** equation of state (Read, Lackey, Owen & Friedman,
PRD 79, 124032, 2009) into a TOV solve and predicts the mass-radius relation,
the maximum mass, the canonical R(1.4 M_sun), and the surface redshift -- the
quantities confronted by PSR J0740+6620 and the NICER radii.

EoS construction (Read et al. 2009): a single low-density crust polytrope plus a
three-piece high-density core fixed by (log10 p1, Gamma1, Gamma2, Gamma3) at
dividing rest-mass densities rho1 = 10^14.7, rho2 = 10^15 g/cm^3.  Energy density
follows from first-law continuity, epsilon_i(rho) = (1+a_i) rho + K_i/(Gamma_i-1)
rho^Gamma_i / c^2, with a_i fixed by continuity of epsilon at each boundary.

Self-contained: numpy + a local RK4.  CGS internally; geometric (km, M_sun) out.
Date: 2026-06-30 (F184).
"""

from __future__ import annotations

import numpy as np

# ---- cgs constants ---------------------------------------------------
C_CGS = 2.99792458e10          # cm/s
G_CGS = 6.67430e-8             # cm^3 g^-1 s^-2
MSUN_CM = 1.476625e5           # GM_sun/c^2 in cm
GC2 = G_CGS / C_CGS**2         # cm/g     (mass-density -> geometric cm^-2)
GC4 = G_CGS / C_CGS**4         # s^2 g^-1 cm^-1  (pressure -> geometric cm^-2)

# ---- published piecewise-polytrope parameters (Read et al. 2009) -----
# Core: (log10 p1 [dyn/cm^2 at rho1=10^14.7], Gamma1, Gamma2, Gamma3)
EOS_PARAMS = {
    "SLy": (34.384, 3.005, 2.988, 2.851),
    "APR": (34.616, 3.514, 3.141, 3.291),   # APR4
    "MPA1": (34.495, 3.446, 3.572, 2.887),
}
# common crust low-density polytrope (Read et al.): p = K_crust rho^Gamma_crust
GAMMA_CRUST = 1.35692
K_CRUST = 3.99874e-8           # cgs
RHO1 = 10**14.7                # g/cm^3 (core piece 1/2 boundary; logp1 anchor)
RHO2 = 10**15.0                # g/cm^3 (core piece 2/3 boundary)


class PiecewisePolytrope:
    """Read et al. (2009) crust + 3-core piecewise polytrope EoS in cgs."""

    def __init__(self, name="SLy"):
        logp1, G1, G2, G3 = EOS_PARAMS[name]
        self.name = name
        p1 = 10**logp1
        K1 = p1 / RHO1**G1
        K2 = K1 * RHO1**(G1 - G2)
        K3 = K2 * RHO2**(G2 - G3)
        # crust-core boundary: K_crust rho^Gc = K1 rho^G1
        rho_cc = (K_CRUST / K1)**(1.0 / (G1 - GAMMA_CRUST))
        # pieces in increasing density: (rho_lower, K, Gamma)
        self.rho_lo = np.array([0.0, rho_cc, RHO1, RHO2])
        self.K = np.array([K_CRUST, K1, K2, K3])
        self.G = np.array([GAMMA_CRUST, G1, G2, G3])
        # first-law continuity constants a_i (epsilon continuous at boundaries)
        self.a = np.zeros(4)
        for i in range(1, 4):
            rb = self.rho_lo[i]
            self.a[i] = (self.a[i-1]
                         + self.K[i-1] / (self.G[i-1] - 1) * rb**(self.G[i-1]-1) / C_CGS**2
                         - self.K[i] / (self.G[i] - 1) * rb**(self.G[i]-1) / C_CGS**2)
        # pressure at each lower boundary (for p->piece lookup)
        self.p_lo = self.K * np.where(self.rho_lo > 0, self.rho_lo, 0.0)**self.G

    def _piece_from_rho(self, rho):
        i = np.searchsorted(self.rho_lo, rho, side="right") - 1
        return int(np.clip(i, 0, 3))

    def _piece_from_p(self, p):
        i = np.searchsorted(self.p_lo, p, side="right") - 1
        return int(np.clip(i, 0, 3))

    def p_of_rho(self, rho):
        i = self._piece_from_rho(rho)
        return self.K[i] * rho**self.G[i]

    def eps_of_rho(self, rho):
        """Total energy density (g/cm^3) = (1+a) rho + K/(G-1) rho^G / c^2."""
        i = self._piece_from_rho(rho)
        return (1 + self.a[i]) * rho + self.K[i] / (self.G[i]-1) * rho**self.G[i] / C_CGS**2

    def eps_of_p(self, p):
        if p <= 0:
            return 0.0
        i = self._piece_from_p(p)
        rho = (p / self.K[i])**(1.0 / self.G[i])
        return (1 + self.a[i]) * rho + p / ((self.G[i]-1) * C_CGS**2)


# ======================================================================
# TOV integration (geometric units, cm) carrying both metric functions
# ======================================================================
def integrate_tov(eos, rho_c, h_cm=500.0, rmax_cm=4e6):
    """Integrate one star of central rest-mass density rho_c (g/cm^3).
    Returns (R_km, M_msun, z_surface)."""
    eps_c = eos.eps_of_rho(rho_c) * GC2          # geometric cm^-2
    p_c = eos.p_of_rho(rho_c) * GC4
    r, m, p = 1.0, 0.0, p_c
    p_floor = 1e-12 * p_c

    def rhs(r, m, p):
        eps = eos.eps_of_p(p / GC4) * GC2        # p back to cgs -> eps -> geometric
        dm = 4 * np.pi * r**2 * eps
        dp = -(eps + p) * (m + 4 * np.pi * r**3 * p) / (r * (r - 2 * m))
        return dm, dp

    while p > p_floor and r < rmax_cm:
        k1 = rhs(r, m, p)
        k2 = rhs(r + h_cm/2, m + h_cm/2*k1[0], p + h_cm/2*k1[1])
        k3 = rhs(r + h_cm/2, m + h_cm/2*k2[0], p + h_cm/2*k2[1])
        k4 = rhs(r + h_cm, m + h_cm*k3[0], p + h_cm*k3[1])
        m_new = m + h_cm/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        p_new = p + h_cm/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        if p_new <= 0:
            frac = p / (p - p_new)
            r += frac * h_cm; m += frac * (m_new - m); break
        r, m, p = r + h_cm, m_new, p_new
    R_km = r / 1e5
    M_msun = m / MSUN_CM
    z = (1 - 2 * m / r)**-0.5 - 1.0
    return R_km, M_msun, z


def mass_radius_curve(eos, rho_c_array):
    R, M, Z = [], [], []
    for rc in rho_c_array:
        r, m, z = integrate_tov(eos, rc)
        R.append(r); M.append(m); Z.append(z)
    return {"rho_c": np.asarray(rho_c_array), "R_km": np.array(R),
            "M_msun": np.array(M), "z_surf": np.array(Z)}


def summarize(eos, n=60):
    """Maximum mass, R(1.4), and the surface redshift at M_max."""
    rho_c = np.geomspace(3e14, 4e15, n)
    c = mass_radius_curve(eos, rho_c)
    i = int(np.argmax(c["M_msun"]))
    M_max = float(c["M_msun"][i]); R_at_max = float(c["R_km"][i])
    z_max = float(c["z_surf"][i])
    # R at 1.4 Msun on the stable (rising) branch
    Ms, Rs = c["M_msun"][:i+1], c["R_km"][:i+1]
    R_14 = float(np.interp(1.4, Ms, Rs)) if Ms.max() >= 1.4 else float("nan")
    return {"eos": eos.name, "M_max": M_max, "R_at_Mmax_km": R_at_max,
            "R_1.4_km": R_14, "z_surf_at_Mmax": z_max,
            "turnover": bool(0 < i < n-1), "curve": c}
