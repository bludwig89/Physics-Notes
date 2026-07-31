"""
ca_rotation.py  --  Slow-rotation frame dragging & moment of inertia (Hartle)
=============================================================================

Scenario S2.  Extends the F181 two-function interior to first order in spin
(Hartle 1967): the dragging of inertial frames omega(r) and the stellar moment
of inertia I.  This is the rotating-compact-object rung -- Lense-Thirring frame
dragging and the I that enters the I-Love-Q relations and pulsar timing.

The frame-dragging potential varpi(r) = Omega - omega(r) obeys Hartle's linear
ODE on the static background (areal radius r, metric legs A=e^{2nu}, B):

    d/dr [ r^4 j(r) dvarpi/dr ] + 4 r^3 (dj/dr) varpi = 0 ,
    j(r) = (A B)^{-1/2}  =  e^{-nu} sqrt(1 - 2m/r)  (=1 in vacuum).

Outside the star omega = 2J/r^3, so the angular momentum and moment of inertia
are read off from the surface values,

    J = (1/6) R^4 varpi'(R),    Omega = varpi(R) + (R/3) varpi'(R),    I = J/Omega.

Self-contained: numpy + the F181 background.  Date: 2026-06-30 (F185).
"""

from __future__ import annotations

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from casim.engine.interactions import interior_metric as im  # noqa: E402
from casim.constants import G_CODATA as _G_CODATA, c_SI as _c_SI

MSUN_KM = im.MSUN_KM


def _background(rho_c, eos, h=2e-3):
    sol = im.integrate_interior(rho_c, eos, h=h)
    r, A, B, m = sol["r"], sol["A"], sol["B"], sol["m"]
    j = (A * B) ** -0.5                      # Hartle j(r) (=1 at the surface)
    return sol, r, j, m


def frame_drag(rho_c, eos, h=2e-3):
    """Solve Hartle's varpi ODE on the interior; return I and frame-drag data.
    varpi is defined up to overall scale (linear ODE) -> set varpi_c = 1."""
    sol, r, j, m = _background(rho_c, eos, h)
    n = len(r)
    dj = np.gradient(j, r)
    varpi = np.empty(n); dvarpi = np.empty(n)
    varpi[0] = 1.0; dvarpi[0] = 0.0          # regularity at centre
    # integrate the 2nd-order ODE: varpi'' = -[(4/r) + j'/j] varpi' - (4 j'/(r j)) varpi
    for i in range(n - 1):
        ri = max(r[i], 1e-6); dr = r[i+1] - r[i]
        ji = max(j[i], 1e-12); dji = dj[i]
        acc = -((4.0 / ri) + dji / ji) * dvarpi[i] - (4.0 * dji / (ri * ji)) * varpi[i]
        # semi-implicit Euler-Cromer (stable for this stiff-ish linear ODE)
        dvarpi[i+1] = dvarpi[i] + acc * dr
        varpi[i+1] = varpi[i] + dvarpi[i+1] * dr
    R = r[-1]
    vR, dvR = varpi[-1], dvarpi[-1]
    J = (1.0 / 6.0) * R**4 * dvR
    Omega = vR + (R / 3.0) * dvR
    I_km3 = J / Omega                        # geometric (km^3, since G=c=1, km units)
    M = sol["M"]
    # dimensionless diagnostics
    I_over_MR2 = I_km3 / (M * R**2)
    I_bar = I_km3 / M**3                      # I/M^3 (I-Love-Q variable)
    omega_surf_ratio = (Omega - vR) / Omega   # omega(R)/Omega = 1 - varpi(R)/Omega
    return {"M_msun": M / MSUN_KM, "R_km": R, "I_km3": I_km3,
            "I_over_MR2": I_over_MR2, "I_bar": I_bar,
            "omega_over_Omega_surface": omega_surf_ratio,
            "J_over_Omega": I_km3, "compactness": M / R}


def moment_of_inertia_SI(rho_c, eos):
    """Moment of inertia in SI (kg m^2) and in 10^45 g cm^2 (pulsar units)."""
    d = frame_drag(rho_c, eos)
    # I in km^3 geometric -> physical: I_phys = I_km3 * c^2/G  (km^3 -> kg m^2)
    c = _c_SI; G = _G_CODATA
    I_km3 = d["I_km3"]
    I_m3 = I_km3 * (1e3)**3                   # km^3 -> m^3 (geometric)
    I_SI = I_m3 * c**2 / G                    # kg m^2
    return {**d, "I_SI_kg_m2": I_SI, "I_1e45_g_cm2": I_SI * 1e3 * 1e4 / 1e45}
