# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_darkmatter.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/darkmatter.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_darkmatter.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_darkmatter.py  --  Galactic rotation curves & the Bullet-Cluster test
========================================================================

Scenario S8 (speculative).  Under F178 the gravity sector is exact GR with
constant G, so the "missing mass" must be a real, dark, gravitating source --
the vacuum dielectric only *responds* to it (catalog §4).  This module makes
the assessment concrete:

  (1) Rotation curves.  Baryons alone (exponential disk) give a FALLING curve;
      adding a collisionless dark halo (NFW) flattens it -- the standard CDM
      result.  A modified-gravity / dielectric-reweighting toy (MOND, a0) also
      flattens the curve, so rotation curves alone do not decide.

  (2) Bullet Cluster.  A toy two-component collision: collisional gas (most of
      the baryons) shocks and lags at the centre, while collisionless mass
      (galaxies + any particle dark matter) passes through.  The lensing
      (total-mass) peak then sits on the collisionless component, OFFSET from
      the gas (X-ray) peak.  Modified gravity that tracks baryons predicts the
      lensing peak ON the gas -> contradicted.  This is the make-or-break test
      that favours a dark *source* over a pure dielectric reweighting.

Self-contained: numpy only.  Units: kpc, km/s, 1e10 M_sun.  Date: 2026-06-30 (F191).
"""

from __future__ import annotations

import numpy as np

G_GAL = 4.30091e-6        # kpc (km/s)^2 / M_sun  (gravitational constant)
A0_MOND = 3.6e3           # (km/s)^2 / kpc  ~ 1.2e-10 m/s^2 in galactic units


def v_disk(r, M_disk=6e10, Rd=3.0):
    """Circular speed of an exponential disk (thin-disk enclosed-mass approx)."""
    x = r / Rd
    M_enc = M_disk * (1.0 - (1.0 + x) * np.exp(-x))
    return np.sqrt(G_GAL * M_enc / r)


def v_nfw(r, M200=1e12, c=12.0, R200=200.0):
    """Circular speed from an NFW dark halo."""
    rs = R200 / c
    g = np.log(1 + c) - c / (1 + c)
    x = r / rs
    M_enc = M200 * (np.log(1 + x) - x / (1 + x)) / g
    return np.sqrt(G_GAL * M_enc / r)


def v_total(r, **kw):
    return np.sqrt(v_disk(r)**2 + v_nfw(r)**2)


def v_mond(r, M_disk=6e10, Rd=3.0):
    """Deep-MOND prediction from baryons only: v^4 = G M_b a0 (flat)."""
    x = r / Rd
    M_b = M_disk * (1.0 - (1.0 + x) * np.exp(-x))
    g_newt = G_GAL * M_b / r**2
    # simple interpolating function mu(g/a0)=g/(g+a0): g_eff = sqrt(g_newt a0) deep
    g_eff = np.sqrt(g_newt * A0_MOND + g_newt**2)
    return np.sqrt(g_eff * r)


def rotation_curves(r=None):
    if r is None:
        r = np.linspace(1.0, 30.0, 60)
    vb = v_disk(r); vt = v_total(r); vm = v_mond(r)
    flat = lambda v: v[r >= 15].mean() / v.max()
    return {"r_kpc": r, "v_baryons": vb, "v_total_NFW": vt, "v_mond": vm,
            "baryon_falloff": float(vb[-1] / vb.max()),
            "nfw_flatness": float(vt[r >= 15].mean() / vt[r >= 15].max()),
            "mond_flatness": float(vm[r >= 15].mean() / vm[r >= 15].max())}


def bullet_cluster(gas_frac=0.9, n=400):
    """Toy post-collision mass distribution along the collision axis.
    Each cluster's baryons are mostly collisional gas (gas_frac); the rest is in
    galaxies, plus a collisionless dark component equal to ~5x the baryons
    (cluster mass budget).  After the pass-through, gas piles up near the centre
    while the collisionless mass continues to the original cluster offsets.
    Returns the X-ray (gas) peak vs the lensing (total-mass) peak positions."""
    x = np.linspace(-1.5, 1.5, n)            # Mpc along the collision axis
    # collisionless components (DM + galaxies) sit at the two original centroids
    sep = 0.72                                # Mpc (Bullet Cluster ~0.72 Mpc)
    def gauss(c, s): return np.exp(-(x - c)**2 / (2 * s**2))
    M_baryon_each = 1.0                       # arbitrary units
    M_dark_each = 5.0 * M_baryon_each         # cluster DM ~5x baryons
    galaxies = (1 - gas_frac) * M_baryon_each
    # gas: shocked, decelerated -> piles toward the centre
    gas = gas_frac * M_baryon_each * (gauss(-0.15, 0.18) + gauss(0.15, 0.18))
    collisionless = (M_dark_each + galaxies) * (gauss(-sep/2, 0.15) + gauss(sep/2, 0.15))
    total_mass = gas + collisionless          # what lensing measures
    xray_peak = x[np.argmax(gas)]             # gas peak (X-ray)
    # lensing peaks: the two collisionless centroids
    left = total_mass.copy(); left[x > 0] = 0
    right = total_mass.copy(); right[x < 0] = 0
    lensing_peaks = sorted([x[np.argmax(left)], x[np.argmax(right)]])
    lensing_centroid_offset = min(abs(lensing_peaks[0] - xray_peak),
                                  abs(lensing_peaks[1] - xray_peak))
    return {"x_mpc": x, "gas": gas, "collisionless": collisionless,
            "total_mass": total_mass, "xray_gas_peak_mpc": float(xray_peak),
            "lensing_peaks_mpc": [float(p) for p in lensing_peaks],
            "lensing_gas_offset_mpc": float(lensing_centroid_offset),
            "verdict": "lensing offset from gas -> collisionless dark source "
                       "(favoured over baryon-tracking modified gravity)"}
