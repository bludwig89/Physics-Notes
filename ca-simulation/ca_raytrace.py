"""
ca_raytrace.py  --  Black-hole shadow by null-geodesic ray tracing + mu-as map
==============================================================================

Scenario S3.  Backward-integrates null geodesics in the canonical (F178)
Schwarzschild geometry to locate the shadow boundary numerically (capture vs
escape), confirming the analytic critical impact parameter b_c = 3 sqrt3 M, and
converts the shadow to an on-sky angular diameter in micro-arcseconds for
M87* and Sgr A* to compare against the EHT rings.  Also reports the Kerr
spin-dependent shadow extent (Bardeen), reusing ca_blackhole.

Photon orbit equation (Schwarzschild, Binet form, u = 1/r):
    d^2u/dphi^2 + u = 3 M u^2 .
A ray launched from far away with impact parameter b either plunges
(u -> 1/2M, capture) or turns around (escape); the boundary is b_c.

Self-contained: numpy + a local RK4.  Date: 2026-06-30 (F186).
"""

from __future__ import annotations

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import ca_blackhole as bh                   # noqa: E402

# EHT targets: (mass M_sun, distance Mpc)
TARGETS = {
    "M87*":  (6.5e9, 16.8),       # EHT 2019
    "SgrA*": (4.297e6, 8.277e-3),  # EHT 2022 (8.277 kpc -> Mpc)
}
RAD_TO_UAS = 180.0 / np.pi * 3600.0 * 1e6


def _plunges(b, M=1.0, phi_max=4 * np.pi, n=200000):
    """Integrate the photon orbit from u~0 inward at impact parameter b; return
    True if it reaches the horizon (capture)."""
    # initial: far away, u=1e-6, du/dphi = -1/b (incoming) approximately
    u = 1e-6
    du = 1.0 / b              # magnitude of du/dphi for a ray aimed with impact b
    dphi = phi_max / n
    f = lambda u: 3.0 * M * u**2 - u          # u'' = 3Mu^2 - u
    for _ in range(n):
        k1u, k1d = du, f(u)
        k2u, k2d = du + dphi/2*k1d, f(u + dphi/2*k1u)
        k3u, k3d = du + dphi/2*k2d, f(u + dphi/2*k2u)
        k4u, k4d = du + dphi*k3d, f(u + dphi*k3u)
        u = u + dphi/6*(k1u + 2*k2u + 2*k3u + k4u)
        du = du + dphi/6*(k1d + 2*k2d + 2*k3d + k4d)
        if u >= 1.0 / (2.0 * M):              # crossed the horizon
            return True
        if u <= 0:                             # escaped back to infinity
            return False
    return False


def numeric_shadow_b(M=1.0, lo=4.0, hi=7.0, iters=40):
    """Bisection for the critical impact parameter (capture boundary)."""
    assert _plunges(lo, M) and not _plunges(hi, M)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if _plunges(mid, M):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def angular_shadow_uas(M_solar, D_mpc, b_over_M=None):
    """On-sky shadow angular DIAMETER in micro-arcsec.  b_over_M defaults to the
    Schwarzschild 3 sqrt3 (shadow radius); diameter = 2 b_c (GM/c^2)/D."""
    if b_over_M is None:
        b_over_M = 3.0 * np.sqrt(3.0)
    G = 6.67430e-11; c = 2.99792458e8; Msun = 1.98892e30; Mpc = 3.0857e22
    rg = G * (M_solar * Msun) / c**2          # GM/c^2 (m)
    D = D_mpc * Mpc
    theta_diam = 2.0 * b_over_M * rg / D       # radians
    return theta_diam * RAD_TO_UAS


def eht_predictions():
    """Shadow diameters (mu-as) for the canonical GR BH vs the superseded F114
    dielectric BH, for the EHT targets."""
    out = {}
    for name, (Msun, Dmpc) in TARGETS.items():
        gr = angular_shadow_uas(Msun, Dmpc, 3 * np.sqrt(3))
        f114 = angular_shadow_uas(Msun, Dmpc, 2 * np.e)   # F114 b_c = 2e M
        out[name] = {"shadow_uas_GR": gr, "shadow_uas_F114": f114,
                     "F114_enlargement_pct": 100 * (2 * np.e / (3 * np.sqrt(3)) - 1)}
    return out


def kerr_shadow_extents(M=1.0, spins=(0.3, 0.6, 0.9, 0.998)):
    """Horizontal width and prograde-side displacement of the equatorial Kerr
    shadow as a function of spin (reuses the Bardeen outline)."""
    out = {}
    for a in spins:
        s = bh.kerr_shadow_outline(M=M, a=a, theta_o=np.pi/2)
        out[f"a={a}"] = {"width_M": s["width_horizontal_M"],
                         "height_M": s["height_vertical_M"],
                         "offset_M": s["horizontal_offset_M"]}
    return out
