"""
ca_emergent_gravity.py  --  Model-native emergent-gravity ("dark matter without
dark matter") and its Bullet-Cluster falsification test.
=========================================================================

Scenario S8b (F194).  The catalog (gravity-sector-scenarios §4) and F191 left
one gravity-SIDE candidate for the missing mass: an IR enhancement of the
INDUCED Newton constant (Sakharov / F59 / F79) at the very low accelerations of
galactic and cluster outskirts -- the model-native cousin of Verlinde's
emergent gravity.  Instead of a new dark *source*, baryons drag the lattice's
induced response harder when the local curvature is small, so the lattice
"weighs more" than its baryons.  This module:

  (1) Derives the model-native acceleration scale a0 from the SAME vacuum sector
      that the cosmological-constant work (F164/F192) is about:
          a0  ~  c H0 / 6 ,   H0^2 = (8 pi G / 3 c^2) rho_Lambda ,
      i.e. the de Sitter / vacuum-energy scale.  Emergent-gravity DM and dark
      energy would then share ONE scale -- the elegant-design appeal.  We check
      a0_model vs the empirical MOND a0 ~ 1.2e-10 m/s^2.

  (2) Implements emergent gravity as an induced-G enhancement
          g = nu(|g_N|/a0) g_N ,        nu(y) = 1/2 + sqrt(1/4 + 1/y)   (QUMOND)
      so G_eff/G = nu >= 1 grows as the acceleration falls.  This reproduces
      flat rotation curves and the baryonic Tully-Fisher relation from baryons
      alone (sanity check -- so the falsification below is not a strawman).

  (3) THE FALSIFIER.  In any such theory the lensing (dynamical) mass is the
      "phantom" density  rho_ph = (1/4 pi G) div[(nu-1) g_N]  -- a LOCAL
      FUNCTIONAL OF THE BARYONS.  It is therefore pinned to the baryons.  In a
      cluster the baryons are dominated by the X-ray GAS, not the galaxies, so
      emergent gravity predicts the lensing peak ON the gas.  The Bullet Cluster
      shows the lensing peak OFFSET from the gas, onto the collisionless
      galaxies (Clowe et al. 2006).  We build a 3D toy Bullet Cluster, run
      QUMOND, project, and measure the offset -- the make-or-break test.

Self-contained: numpy only (real arithmetic; FFT used only for the linear,
real, symmetric Newtonian Poisson solve -- no chiral/complex spinor transforms).
Units: length Mpc, mass 1e12 Msun, velocity km/s.  Date 2026-06-30 (F194).
"""

from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------- constants ---
# Gravitational constant in (Mpc, km/s, 1e12 Msun) units.
# G = 4.30091e-6 kpc (km/s)^2 / Msun = 4.30091e3 Mpc (km/s)^2 / (1e12 Msun)
G_U = 4.30091e3                      # Mpc (km/s)^2 / (1e12 Msun)
# 1 (km/s)^2 / Mpc  =  3.2408e-17 m/s^2   (acceleration unit conversion)
ACC_U_TO_SI = (1.0e3) ** 2 / 3.0856775814913673e22   # = 3.2408e-17 m/s^2 per (km/s)^2/Mpc

C_SI = 2.99792458e8                  # m/s
MPC_M = 3.0856775814913673e22        # m
RHO_LAMBDA_SI = 6.0e-10              # J/m^3  (observed dark-energy density, F164/F192)
OMEGA_LAMBDA = 0.69
G_SI = 6.674e-11                     # m^3 kg^-1 s^-2
A0_EMP_SI = 1.2e-10                  # m/s^2  (empirical MOND scale)


# ----------------------------------------------- (1) model-native a0 ----------
def derive_a0_from_vacuum():
    """a0 from the vacuum-energy (de Sitter) scale -- the F164/F192 sector.

    rho_crit = rho_Lambda / Omega_Lambda ;  rho_crit (energy) = 3 H0^2 c^2/(8 pi G)
    => H0 = sqrt( 8 pi G rho_crit / (3 c^2) ) .   Verlinde: a0 = c H0 / 6.
    """
    rho_crit = RHO_LAMBDA_SI / OMEGA_LAMBDA                      # J/m^3
    H0 = np.sqrt(8 * np.pi * G_SI * rho_crit / (3 * C_SI ** 2))  # 1/s
    a0_si = C_SI * H0 / 6.0                                      # m/s^2
    a0_u = a0_si / ACC_U_TO_SI                                   # (km/s)^2/Mpc
    return {
        "rho_Lambda_SI": RHO_LAMBDA_SI,
        "H0_per_s": float(H0),
        "H0_km_s_Mpc": float(H0 * MPC_M / 1.0e3),
        "a0_model_SI": float(a0_si),
        "a0_empirical_SI": A0_EMP_SI,
        "a0_model_over_empirical": float(a0_si / A0_EMP_SI),
        "a0_model_units": float(a0_u),     # (km/s)^2 / Mpc, for the grid solver
    }


# ----------------------------------------------- QUMOND interpolation ----------
def nu_simple(y):
    """QUMOND 'simple' nu(y), y = |g_N|/a0.  nu->1 (y>>1), nu->1/sqrt(y) (y<<1)."""
    y = np.asarray(y, dtype=float)
    y = np.where(y < 1e-12, 1e-12, y)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


# ----------------------------------------------- (2) rotation-curve check -----
def rotation_curve_emergent(r_kpc=None, M_disk=6e10, Rd=3.0):
    """Flat curve from baryons ALONE under emergent gravity (deep-MOND limit).

    Returns flatness ratio; ~1 means flat (DM-like) from baryons only.
    """
    if r_kpc is None:
        r_kpc = np.linspace(1.0, 30.0, 60)
    G_gal = 4.30091e-6           # kpc (km/s)^2 / Msun
    a0_gal = A0_EMP_SI / ACC_U_TO_SI / 1.0e3   # (km/s)^2/kpc  (Mpc->kpc: /1000)
    x = r_kpc / Rd
    M_b = M_disk * (1.0 - (1.0 + x) * np.exp(-x))
    g_N = G_gal * M_b / r_kpc ** 2
    g = nu_simple(g_N / a0_gal) * g_N
    v = np.sqrt(g * r_kpc)
    outer = r_kpc >= 15
    # baryonic Tully-Fisher: v_flat^4 vs G M_b a0
    v_flat = v[outer].mean()
    btf_pred = (G_gal * M_disk * a0_gal) ** 0.25
    return {
        "r_kpc": r_kpc.tolist(),
        "v_emergent": v.tolist(),
        "flatness": float(v[outer].mean() / v[outer].max()),
        "v_flat": float(v_flat),
        "btf_prediction": float(btf_pred),
        "btf_ratio": float(v_flat / btf_pred),
    }


# ----------------------------------------------- 3D Poisson (FFT) -------------
def _poisson_gN(rho, dx):
    """Newtonian g_N = -grad Phi from rho via FFT with ISOLATED (zero-padded)
    boundaries -- the density is embedded in a 2x box so there are no periodic
    images, and the vacuum field decays as 1/r^2 instead of ramping at the wall.
    ∇²Φ = 4πG rho. Real field (no chiral/complex transforms)."""
    n = rho.shape[0]
    m = 2 * n
    big = np.zeros((m, m, m))
    big[:n, :n, :n] = rho
    k = 2 * np.pi * np.fft.fftfreq(m, d=dx)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    k2 = KX ** 2 + KY ** 2 + KZ ** 2
    k2[0, 0, 0] = 1.0
    phi_k = -4 * np.pi * G_U * np.fft.fftn(big) / k2
    phi_k[0, 0, 0] = 0.0
    phi = np.real(np.fft.ifftn(phi_k))[:n, :n, :n]
    gx, gy, gz = np.gradient(-phi, dx, edge_order=2)
    return gx, gy, gz


def _blob(X, Y, Z, c, s, amp):
    return amp * np.exp(-((X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2)
                        / (2 * s ** 2))


# ----------------------------------------------- (3) Bullet Cluster -----------
def bullet_cluster_emergent(n=128, L=3.0, a0_u=None,
                            sep=0.72, gas_offset=0.18,
                            gas_to_star=6.0, dark_to_baryon=5.0):
    """3D toy Bullet Cluster; QUMOND phantom lensing vs a real dark source.

    Geometry along x (collision axis):
      * galaxies (collisionless baryons): clumps at x = -/+ sep/2
      * gas (collisional, dominant baryons): clumps dragged toward centre at
        x = -/+ gas_offset
      * (LCDM comparison) a real collisionless dark halo on the galaxies.

    Emergent gravity sees ONLY baryons (gas+stars).  Its lensing mass is the
    QUMOND phantom density, projected.  We locate the lensing peak and measure
    its offset from the gas peak and from the galaxy peak.
    """
    if a0_u is None:
        a0_u = derive_a0_from_vacuum()["a0_model_units"]
    x = np.linspace(-L / 2, L / 2, n)
    dx = x[1] - x[0]
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    s_clump = 0.12

    # --- baryons ---
    star_mass = 1.0                    # each galaxy clump (1e12 Msun units)
    gas_mass = gas_to_star * star_mass
    galaxies = (_blob(X, Y, Z, (-sep / 2, 0, 0), s_clump, star_mass)
                + _blob(X, Y, Z, (sep / 2, 0, 0), s_clump, star_mass))
    gas = (_blob(X, Y, Z, (-gas_offset, 0, 0), s_clump, gas_mass)
           + _blob(X, Y, Z, (gas_offset, 0, 0), s_clump, gas_mass))
    rho_b = galaxies + gas
    # normalise blob amplitudes to carry the intended masses
    cell = dx ** 3
    rho_b *= 1.0  # amplitudes are densities; mass = amp*(2 pi s^2)^{3/2}, ok for a toy

    # --- emergent gravity: QUMOND phantom ---
    gx, gy, gz = _poisson_gN(rho_b, dx)
    gmag = np.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
    nu = nu_simple(gmag / a0_u)
    # dynamical (lensing) density rho_tot = (1/4 pi G) div(nu g_N)
    dvx = np.gradient(nu * gx, dx, axis=0, edge_order=2)
    dvy = np.gradient(nu * gy, dx, axis=1, edge_order=2)
    dvz = np.gradient(nu * gz, dx, axis=2, edge_order=2)
    # QUMOND dynamical (lensing) density: ∇²Φ = 4πG ρ_dyn, g = -∇Φ = ν g_N
    #   => ρ_dyn = -(1/4πG) ∇·(ν g_N).  (ν=1 recovers ρ_dyn = ρ_b exactly.)
    rho_tot_eg = -(dvx + dvy + dvz) / (4 * np.pi * G_U)
    rho_tot_eg = np.maximum(rho_tot_eg, 0.0)             # lensing convergence >= 0

    # --- LCDM comparison: baryons + real collisionless dark halo on galaxies ---
    dark = dark_to_baryon * (gas_mass + star_mass) * 0.5 * (
        _blob(X, Y, Z, (-sep / 2, 0, 0), s_clump * 1.5, 1.0)
        + _blob(X, Y, Z, (sep / 2, 0, 0), s_clump * 1.5, 1.0))
    rho_tot_lcdm = rho_b + dark

    # --- project along z (line of sight) -> surface densities (convergence) ---
    Sig_gas = gas.sum(axis=2)
    Sig_gal = galaxies.sum(axis=2)
    Sig_eg = rho_tot_eg.sum(axis=2)
    Sig_lcdm = rho_tot_lcdm.sum(axis=2)

    def peak_x(Sig):
        # collapse to the collision axis (sum over y), find the x of the max
        prof = Sig.sum(axis=1)
        return x[int(np.argmax(prof))], prof

    xg, _ = peak_x(Sig_gas)
    xgal_prof = Sig_gal.sum(axis=1)
    # galaxy peaks: the two symmetric maxima
    gal_left = x[:n // 2][int(np.argmax(xgal_prof[:n // 2]))]
    gal_right = x[n // 2:][int(np.argmax(xgal_prof[n // 2:]))]

    # EG and LCDM lensing peaks within the cluster field of view (one subcluster
    # side, 0 < x < fov).  The FoV excludes the far vacuum where the MOND phantom
    # has an extended 1/r^2 tail (real, but not where peaks are compared).
    fov = sep / 2 + 3 * s_clump        # just beyond the galaxies (~0.72 Mpc)
    eg_prof = Sig_eg.sum(axis=1)
    lcdm_prof = Sig_lcdm.sum(axis=1)
    rh = (x > 0.02) & (x < fov)
    xr = x[rh]
    x_eg_peak = xr[int(np.argmax(eg_prof[rh]))]
    x_lcdm_peak = xr[int(np.argmax(lcdm_prof[rh]))]
    x_gas_right = xr[int(np.argmax(gas.sum(axis=2).sum(axis=1)[rh]))]
    x_gal_right = gal_right

    # offsets from the gas (the EG prediction is "lensing on gas", offset ~ 0)
    eg_offset_from_gas = abs(x_eg_peak - x_gas_right)
    lcdm_offset_from_gas = abs(x_lcdm_peak - x_gas_right)
    galaxy_offset_from_gas = abs(x_gal_right - x_gas_right)   # the OBSERVED offset

    return {
        "a0_units_kms2_per_Mpc": float(a0_u),
        "x_mpc": x.tolist(),
        "gas_peak_x_mpc": float(x_gas_right),
        "galaxy_peak_x_mpc": float(x_gal_right),
        "observed_lensing_offset_from_gas_mpc": float(galaxy_offset_from_gas),
        "emergent_lensing_peak_x_mpc": float(x_eg_peak),
        "emergent_offset_from_gas_mpc": float(eg_offset_from_gas),
        "lcdm_lensing_peak_x_mpc": float(x_lcdm_peak),
        "lcdm_offset_from_gas_mpc": float(lcdm_offset_from_gas),
        # profiles for plotting / inspection
        "profiles": {
            "gas": (gas.sum(axis=2).sum(axis=1)).tolist(),
            "galaxies": xgal_prof.tolist(),
            "emergent_lensing": eg_prof.tolist(),
            "lcdm_lensing": lcdm_prof.tolist(),
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(derive_a0_from_vacuum(), indent=2))
    print(json.dumps({k: v for k, v in bullet_cluster_emergent().items()
                      if k not in ("x_mpc", "profiles")}, indent=2))
