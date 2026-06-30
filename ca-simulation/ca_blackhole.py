"""
ca_blackhole.py  --  The black hole under the F178 gravity sector
=================================================================

F178 made the **induced Einstein equation** G_{mu nu} = (8 pi G/c^4) T_{mu nu}
the canonical strong-field law and demoted the single-scalar dielectric
K = e^{2u} to the vacuum/weak-field (PPN-order) representation.  The immediate
consequence for black holes (F183): the canonical exact vacuum solution is
**Schwarzschild** (Kerr with rotation) -- *with a genuine event horizon* --
replacing the horizon-free "dielectric black hole" of F114.

This module computes the strong-field black-hole observables of the canonical
(GR) solution, the rotating (Kerr) extension on the same two-function kernel,
an exact Oppenheimer-Snyder dust collapse to horizon formation, and the one
place the BCC lattice substrate still departs from GR: the curvature
singularity is **regulated at the lattice cell scale** (a Planck-scale core,
not a point singularity).  Each quantity is given in geometric units (G=c=1,
lengths/times in units of M) with SI conversions where physical.

Sectors:
  * Schwarzschild  -- horizon, photon sphere, shadow b_c = 3 sqrt 3 M, ISCO,
    surface gravity, Hawking temperature & lifetime, eikonal QNM tied to the
    photon sphere.
  * Kerr           -- inner/outer horizons, ergosphere, horizon frame-dragging
    Omega_H, prograde/retrograde ISCO (Bardeen-Press-Teukolsky), and the
    spin-dependent (Bardeen) shadow outline.
  * Collapse       -- exact homogeneous-dust (Oppenheimer-Snyder) surface
    cycloid, horizon-crossing and singularity proper times.
  * Lattice core   -- the cutoff radius where the Kretschmann curvature reaches
    the BCC lattice scale -> singularity resolution (new, non-GR).

Contrast with the superseded F114 dielectric black hole is provided by
`f114_dielectric_contrast()`.

Self-contained: numpy only.  Date: 2026-06-30 (F183).
"""

from __future__ import annotations

import numpy as np

# ---- physical constants (SI / CODATA) --------------------------------
G_SI    = 6.67430e-11          # m^3 kg^-1 s^-2
C_SI    = 2.99792458e8         # m/s
HBAR_SI = 1.054571817e-34      # J s
KB_SI   = 1.380649e-23         # J/K
MSUN_KG = 1.98892e30           # kg
ELLP    = 1.616255e-35         # m  (Planck length)
# F107 canonical BCC cell:  a = sqrt(8 pi) 3^{1/4} ell_P
A_CELL  = np.sqrt(8 * np.pi) * 3 ** 0.25 * ELLP
SECONDS_PER_YEAR = 3.15576e7


# ======================================================================
# Schwarzschild sector  (geometric units, lengths in M)
# ======================================================================
def schwarzschild(M=1.0):
    """All key Schwarzschild observables for a non-rotating BH of mass M
    (geometric units).  Returns a dict."""
    r_h   = 2.0 * M                       # event horizon
    r_ph  = 3.0 * M                       # photon sphere
    b_c   = 3.0 * np.sqrt(3.0) * M        # shadow critical impact parameter
    r_isco = 6.0 * M                      # ISCO (test particle)
    kappa = 1.0 / (4.0 * M)               # surface gravity
    T_hawk_geo = kappa / (2.0 * np.pi)    # = 1/(8 pi M)
    # eikonal QNM tied to the photon sphere (Cardoso et al. 2009):
    #   omega = Omega_c * l - i (n+1/2) |lambda|, with Omega_c = lambda = 1/(3 sqrt3 M)
    Omega_c = np.sqrt(M / r_ph**3)        # circular-geodesic ang. freq = 1/(3 sqrt3 M)
    lam_lyap = Omega_c                    # photon-sphere Lyapunov exponent (Schwarzschild)
    return {
        "M": M, "r_horizon": r_h, "r_photon_sphere": r_ph,
        "shadow_b_crit": b_c, "shadow_b_over_M": b_c / M,
        "r_isco": r_isco, "surface_gravity_kappa": kappa,
        "T_hawking_geometric": T_hawk_geo,
        "QNM_Omega_c": Omega_c, "QNM_lyapunov": lam_lyap,
        "QNM_eikonal_real_per_l": Omega_c,            # omega_R = Omega_c * l
        "QNM_eikonal_imag_n0": 0.5 * lam_lyap,        # omega_I = (n+1/2) lambda
        "has_horizon": True, "redshift_at_horizon": np.inf,
    }


def hawking_temperature_SI(M_solar=1.0):
    """Hawking temperature in kelvin for a Schwarzschild BH of M_solar M_sun."""
    M_kg = M_solar * MSUN_KG
    return HBAR_SI * C_SI**3 / (8.0 * np.pi * G_SI * M_kg * KB_SI)


def hawking_lifetime_years(M_solar=1.0):
    """Evaporation lifetime t ~ 5120 pi G^2 M^3 / (hbar c^4)  (years)."""
    M_kg = M_solar * MSUN_KG
    t_s = 5120.0 * np.pi * G_SI**2 * M_kg**3 / (HBAR_SI * C_SI**4)
    return t_s / SECONDS_PER_YEAR


def schwarzschild_radius_km(M_solar=1.0):
    return 2.0 * G_SI * (M_solar * MSUN_KG) / C_SI**2 / 1000.0


# ======================================================================
# Null-geodesic shadow check (numeric photon-sphere / critical impact b)
# ======================================================================
def photon_effective_potential(r, M=1.0):
    """V(r) = (1 - 2M/r)/r^2 for null geodesics; b_c = 1/sqrt(V_max)."""
    return (1.0 - 2.0 * M / r) / r**2


def numeric_shadow(M=1.0):
    """Find the photon sphere (max of V) and b_c = 1/sqrt(V_max) numerically,
    to compare against the analytic 3M / 3 sqrt3 M."""
    r = np.linspace(2.01 * M, 12.0 * M, 400001)
    V = photon_effective_potential(r, M)
    i = int(np.argmax(V))
    r_ph = r[i]
    b_c = 1.0 / np.sqrt(V[i])
    return {"r_photon_sphere_numeric": r_ph, "b_crit_numeric": b_c}


# ======================================================================
# Kerr sector  (geometric units, lengths in M, spin a in [0, M])
# ======================================================================
def kerr(M=1.0, a=0.9):
    """Kerr horizons, ergosphere, frame-dragging, and prograde/retrograde
    ISCO.  a is the spin parameter (0 <= a <= M)."""
    a = float(a)
    disc = M**2 - a**2
    if disc < 0:
        raise ValueError("naked singularity (a > M) is excluded")
    rt = np.sqrt(disc)
    r_plus  = M + rt                      # outer (event) horizon
    r_minus = M - rt                      # inner (Cauchy) horizon
    r_ergo_eq = 2.0 * M                   # ergosphere outer radius, equator
    Omega_H = a / (r_plus**2 + a**2)      # horizon angular velocity (frame drag)
    # Bardeen-Press-Teukolsky ISCO
    astar = a / M
    Z1 = 1 + (1 - astar**2)**(1/3) * ((1 + astar)**(1/3) + (1 - astar)**(1/3))
    Z2 = np.sqrt(3 * astar**2 + Z1**2)
    r_isco_pro = M * (3 + Z2 - np.sqrt((3 - Z1) * (3 + Z1 + 2 * Z2)))
    r_isco_ret = M * (3 + Z2 + np.sqrt((3 - Z1) * (3 + Z1 + 2 * Z2)))
    return {
        "M": M, "a": a, "a_star": astar,
        "r_horizon_outer": r_plus, "r_horizon_inner": r_minus,
        "r_ergosphere_equator": r_ergo_eq,
        "Omega_horizon_framedrag": Omega_H,
        "r_isco_prograde": r_isco_pro, "r_isco_retrograde": r_isco_ret,
        "has_horizon": True,
    }


def kerr_shadow_outline(M=1.0, a=0.9, theta_o=np.pi/2, n=2000):
    """Bardeen shadow outline (celestial coords alpha, beta) for an observer
    at inclination theta_o.  Parametrised by the photon-orbit radius r.
    Returns alpha, beta arrays (in units of M) tracing the critical curve, plus
    summary widths."""
    a = float(a)
    if a < 1e-2 * M:
        raise ValueError("Bardeen parametrisation is singular as a->0; the "
                         "Schwarzschild shadow is the exact circle b_c=3 sqrt3 M "
                         "(use schwarzschild()). Use a >= 0.01 M here.")
    rs = np.linspace(M * (1 + np.sqrt(1 - (a/M)**2)) + 1e-6, 9.0 * M, n)
    # critical photon orbit constants of motion (e.g. Bardeen 1973)
    xi = -(rs**3 - 3 * M * rs**2 + a**2 * rs + a**2 * M) / (a * (rs - M))
    eta = rs**3 * (4 * a**2 * M - rs * (rs - 3 * M)**2) / (a**2 * (rs - M)**2)
    sin_o = np.sin(theta_o); cos_o = np.cos(theta_o)
    alpha = -xi / sin_o
    beta2 = eta + a**2 * cos_o**2 - xi**2 * (cos_o**2 / sin_o**2)
    good = beta2 >= 0
    alpha, beta2 = alpha[good], beta2[good]
    if alpha.size == 0:
        raise ValueError("no valid photon orbits found; widen the rs range")
    beta = np.sqrt(beta2)
    alpha_full = np.concatenate([alpha, alpha[::-1]])
    beta_full = np.concatenate([beta, -beta[::-1]])
    a_min, a_max = float(alpha.min()), float(alpha.max())
    b_max = float(beta.max())
    width_horizontal = a_max - a_min
    height_vertical = 2.0 * b_max
    # geometric centroid offset (the prograde-side displacement)
    alpha_center = 0.5 * (a_max + a_min)
    return {
        "alpha": alpha_full, "beta": beta_full,
        "width_horizontal_M": width_horizontal,
        "height_vertical_M": height_vertical,
        "horizontal_offset_M": alpha_center,
        "asymmetry": width_horizontal / height_vertical,
    }


# ======================================================================
# Oppenheimer-Snyder collapse: homogeneous dust ball -> horizon (exact)
# ======================================================================
def oppenheimer_snyder(M=1.0, R0=10.0, n=2000):
    """Exact OS collapse of a pressureless dust ball that starts at rest with
    surface areal radius R0.  The surface follows the cycloid

        R(eta) = (R0/2)(1 + cos eta),
        tau(eta) = sqrt(R0^3/(8M)) (eta + sin eta),

    reaching R = 0 (the classical singularity) at eta = pi.  Returns the proper
    times of horizon crossing (R = 2M) and of singularity formation, plus
    the trajectory."""
    eta = np.linspace(0.0, np.pi, n)
    R = (R0 / 2.0) * (1.0 + np.cos(eta))
    tau = np.sqrt(R0**3 / (8.0 * M)) * (eta + np.sin(eta))
    tau_sing = float(np.sqrt(R0**3 / (8.0 * M)) * np.pi)
    # horizon crossing: surface reaches R = 2M
    if R0 > 2.0 * M:
        idx = np.argmin(np.abs(R - 2.0 * M))
        tau_horizon = float(tau[idx])
        eta_h = float(eta[idx])
    else:
        tau_horizon = 0.0; eta_h = 0.0
    return {
        "M": M, "R0": R0, "eta": eta, "R": R, "tau": tau,
        "tau_singularity": tau_sing,
        "tau_horizon_crossing": tau_horizon,
        "eta_horizon": eta_h,
        "horizon_forms": bool(R0 > 2.0 * M),
        "free_fall_finite": True,           # collapse completes in finite proper time
    }


# ======================================================================
# Lattice-cutoff core: where Kretschmann curvature meets the BCC cell scale
# (the one genuinely non-GR strong-field characteristic)
# ======================================================================
def kretschmann_schwarzschild(r, M=1.0):
    """K = 48 M^2 / r^6  (geometric units)."""
    return 48.0 * M**2 / r**6


def lattice_core_radius(M_solar=1.0):
    """Radius at which the Schwarzschild Kretschmann curvature K = 48 (GM/c^2)^2/r^6
    reaches the BCC lattice curvature scale 1/a^4 (a = F107 canonical cell):

        r_core = (48 (GM/c^2)^2 a^4)^{1/6}.

    Below r_core the lattice substrate caps the curvature -> the point
    singularity is replaced by a Planck-scale core (singularity resolution).
    Returns r_core (m), its ratio to a and to the horizon r_h = 2GM/c^2."""
    rg = G_SI * (M_solar * MSUN_KG) / C_SI**2     # GM/c^2 (m)
    r_core = (48.0 * rg**2 * A_CELL**4) ** (1.0 / 6.0)
    r_h = 2.0 * rg
    return {
        "M_solar": M_solar, "r_core_m": r_core,
        "r_core_over_a": r_core / A_CELL,
        "r_core_over_horizon": r_core / r_h,
        "a_cell_m": A_CELL,
        "note": "curvature capped at the lattice scale -> no point singularity",
    }


# ======================================================================
# Contrast with the superseded F114 dielectric black hole
# ======================================================================
def f114_dielectric_contrast(M=1.0):
    """Side-by-side of the canonical (F178, Schwarzschild) BH vs the superseded
    F114 horizon-free dielectric BH.  All in units of M (geometric)."""
    e = np.e
    return {
        "event_horizon":        {"F178_canonical": 2.0 * M,              "F114_dielectric": None,            "note": "F114 had NO finite horizon"},
        "photon_sphere":        {"F178_canonical": 3.0 * M,              "F114_dielectric": 2.0 * np.sqrt(e) * M},
        "shadow_b_crit":        {"F178_canonical": 3.0 * np.sqrt(3) * M, "F114_dielectric": 2.0 * e * M},
        "shadow_pct_vs_GR":     {"F178_canonical": 0.0,                  "F114_dielectric": (2 * e) / (3 * np.sqrt(3)) - 1.0},
        "redshift_deep":        {"F178_canonical": "infinite at horizon","F114_dielectric": "finite, 1+z=e at throat"},
        "hawking_radiation":    {"F178_canonical": "present (T=hbar c^3/8 pi G M k_B)", "F114_dielectric": "absent (no horizon)"},
        "ringdown":             {"F178_canonical": "QNM (photon-sphere modes)", "F114_dielectric": "GW echoes (horizonless)"},
        "singularity":          {"F178_canonical": "regulated at lattice cell a (Planck core)", "F114_dielectric": "wormhole-like throat, no trapped surface"},
        "information":          {"F178_canonical": "horizon present; unitarity via lattice microstates / Planck core", "F114_dielectric": "trivially unitary (nothing sealed)"},
    }
