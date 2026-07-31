# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_cosmology.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/cosmology.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_cosmology.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_cosmology.py  --  Homogeneous-isotropic (FLRW) cosmology of the full-tensor
                     source adopted in F178
==============================================================================

F178 makes the **induced Einstein equation** G_{mu nu} = (8 pi G/c^4) T_{mu nu}
the canonical gravitational law (the single-scalar energy-only dielectric is
demoted to the static weak-field representation).  The sharpest consequence in
cosmology: **pressure gravitates**.  For a flat FLRW metric

    ds^2 = -c^2 dt^2 + a(t)^2 (dx^2 + dy^2 + dz^2),

the two independent Einstein components give the standard Friedmann pair

    H^2 = (a'/a)^2          = (8 pi G/3) rho                      (G^0_0)
    a''/a                   = -(4 pi G/3)(rho + 3 p/c^2)          (G^i_i)

with the continuity equation (Bianchi identity / energy conservation)

    rho' + 3 H (rho + p/c^2) = 0 .

The acceleration equation carries the **rho + 3p** combination -- the Tolman
pressure term.  The *energy-only* law that F178 demotes would instead read
a''/a = -(4 pi G/3) rho, omitting 3p; for radiation (p = rho c^2/3) this
under-weights the source by exactly a factor (rho + 3p)/rho = 2, mis-weighting
the deceleration of the early, radiation-dominated universe.

This module integrates the standard pair for a barotropic fluid p = w rho c^2
and exposes the deceleration parameter, so the F182 test can confirm the
textbook solutions (a ~ t^{1/2} radiation, a ~ t^{2/3} matter) and quantify the
energy-only mis-weighting.

Geometric/natural units: set 8 pi G/3 = 1 and c = 1 by default (only ratios and
power-law exponents are physical here).  Self-contained: numpy + local RK4.

Date: 2026-06-30
"""

from __future__ import annotations

import numpy as np


# ======================================================================
# Barotropic fluid:  p = w rho c^2 ;  continuity => rho ~ a^{-3(1+w)}
# ======================================================================
def rho_of_a(a, w, rho0=1.0, a0=1.0):
    """Energy density from the continuity equation for constant w."""
    return rho0 * (a / a0) ** (-3.0 * (1.0 + w))


def hubble(a, w, K83=1.0, rho0=1.0, a0=1.0):
    """H = a'/a from Friedmann I:  H = sqrt((8 pi G/3) rho).  K83 := 8 pi G/3."""
    return np.sqrt(K83 * rho_of_a(a, w, rho0, a0))


def accel_over_a(a, w, K83=1.0, rho0=1.0, c2=1.0, source="full"):
    """a''/a.  source='full' uses the F178 induced-Einstein source rho+3p/c^2;
    source='energy' uses the demoted energy-only law (rho only)."""
    rho = rho_of_a(a, w, rho0)
    p = w * rho * c2
    half = K83 / 2.0                     # (4 pi G/3) = (1/2)(8 pi G/3)
    if source == "full":
        return -half * (rho + 3.0 * p / c2)
    elif source == "energy":
        return -half * rho               # mis-weighted: omits 3p
    raise ValueError(source)


def deceleration_parameter(w, source="full"):
    """q = -a'' a / a'^2.  For a flat single-component universe:
        full   : q = (1/2)(1 + 3w)        (radiation 1, matter 1/2)
        energy : q = 1/2                  (omits 3p -> wrong for w>0)."""
    if source == "full":
        return 0.5 * (1.0 + 3.0 * w)
    elif source == "energy":
        return 0.5
    raise ValueError(source)


def omitted_source_fraction(w):
    """Fraction of GR's acceleration source the energy-only law drops:
    3p/(rho + 3p) = 3w/(1 + 3w)  (radiation 1/2, dust 0)."""
    return 3.0 * w / (1.0 + 3.0 * w)


# ======================================================================
# Integrate a(t) from Friedmann I (a' = a H), local RK4
# ======================================================================
def integrate_scale_factor(w, t_end, a_init=1e-3, dt=None, K83=1.0, rho0=1.0):
    """Return (t, a) integrating a' = a*H with H from Friedmann I.  rho0 is the
    density at a=1; a_init is the starting scale factor."""
    if dt is None:
        dt = t_end / 200000.0
    n = int(np.ceil(t_end / dt))
    ts = np.empty(n + 1); as_ = np.empty(n + 1)
    t, a = 0.0, a_init
    ts[0], as_[0] = t, a
    f = lambda a: a * hubble(a, w, K83, rho0)
    for i in range(1, n + 1):
        k1 = f(a)
        k2 = f(a + dt/2 * k1)
        k3 = f(a + dt/2 * k2)
        k4 = f(a + dt * k3)
        a = a + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
        t = i * dt
        ts[i], as_[i] = t, a
    return ts, as_


def fit_power_law_exponent(t, a, frac=0.5):
    """Fit a ~ t^n on the late half (avoid the a_init offset); return n."""
    i0 = int(len(t) * frac)
    lt, la = np.log(t[i0:]), np.log(a[i0:])
    return float(np.polyfit(lt, la, 1)[0])


# ======================================================================
# Multi-component flat LCDM background (scenario S5)
#   E(a)^2 = (H/H0)^2 = Om_r a^-4 + Om_m a^-3 + Om_L,   Om_r+Om_m+Om_L = 1
#   accel: a''/a = -(H0^2/2) [ Om_r*2 a^-4 + Om_m a^-3 - 2 Om_L ]   (rho+3p)
# ======================================================================
# Planck-2018-like defaults
H0_KM_S_MPC = 67.4
OMEGA_R0 = 9.182e-5            # photons + neutrinos
OMEGA_M0 = 0.3153
OMEGA_L0 = 1.0 - OMEGA_R0 - OMEGA_M0
MPC_KM = 3.0856775814913673e19
GYR_S = 3.15576e16
H0_INV_GYR = (1.0 / (H0_KM_S_MPC / MPC_KM)) / GYR_S    # Hubble time in Gyr


def E_of_a(a, Om_r=OMEGA_R0, Om_m=OMEGA_M0, Om_L=OMEGA_L0):
    """Dimensionless Hubble rate H(a)/H0 for the flat 3-component background."""
    return np.sqrt(Om_r * a**-4 + Om_m * a**-3 + Om_L)


def accel_over_a_lcdm(a, Om_r=OMEGA_R0, Om_m=OMEGA_M0, Om_L=OMEGA_L0):
    """a''/a in units of H0^2, full-tensor source (rho + 3p):
       radiation w=1/3 -> factor (1+3w)=2; matter -> 1; Lambda w=-1 -> -2."""
    return -0.5 * (2.0 * Om_r * a**-4 + Om_m * a**-3 - 2.0 * Om_L)


def z_matter_radiation_equality(Om_r=OMEGA_R0, Om_m=OMEGA_M0):
    """1 + z_eq = Om_m / Om_r (where rho_m = rho_r)."""
    return Om_m / Om_r - 1.0


def z_acceleration_onset(Om_m=OMEGA_M0, Om_L=OMEGA_L0):
    """a''=0 when Om_m a^-3 = 2 Om_L  ->  a_acc=(Om_m/2Om_L)^{1/3} (radiation negligible)."""
    a_acc = (Om_m / (2.0 * Om_L)) ** (1.0 / 3.0)
    return 1.0 / a_acc - 1.0


def age_of_universe_gyr(Om_r=OMEGA_R0, Om_m=OMEGA_M0, Om_L=OMEGA_L0, n=2_000_000):
    """t0 = (1/H0) integral_0^1 da / (a E(a))  in Gyr."""
    a = np.linspace(1e-8, 1.0, n)
    integrand = 1.0 / (a * E_of_a(a, Om_r, Om_m, Om_L))
    t0_over_tH = np.trapz(integrand, a)
    return t0_over_tH * H0_INV_GYR


def lcdm_summary():
    return {
        "z_eq_matter_radiation": z_matter_radiation_equality(),
        "z_acceleration_onset": z_acceleration_onset(),
        "age_gyr": age_of_universe_gyr(),
        "Hubble_time_gyr": H0_INV_GYR,
        "Omega": {"r": OMEGA_R0, "m": OMEGA_M0, "L": OMEGA_L0},
    }
