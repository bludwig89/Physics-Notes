# ===== deprecated/code backup =====================================
# source     : ca-simulation/forks/gr_fork_F196_dilution_exponent.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/forks/gravity/gr_fork_F196_dilution_exponent.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: gr_fork_F196_dilution_exponent.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
gr_fork_F196_dilution_exponent.py
=================================
Finding F196 — deriving the holographic dilution exponent p=2 that F193
left as its named obstruction.  The residual cosmological constant of
F193 is rho_grav = rho_vac * (a/R_H)^p; F193 imported p=2 from the
Cohen-Kaplan-Nelson holographic bound.  This module shows p=2 is *forced*
by the model's own structure, by TWO independent model-native routes that
converge on the same number, and excludes the statistical (p=3/2) route.

Self-contained, real arithmetic only.

Route 1 — black-hole bound (F183 / F178):
    The model's Schwarzschild law puts the horizon at R_s = 2GM/c^2, i.e.
    the maximal mass-energy a region of radius L can hold before it is
    inside its own horizon is  M_max(L) = L c^2 / (2G)  —  LINEAR in L.
    The gravitating density a region can support is then
        rho_grav(L) = M_max(L) c^2 / V(L) = [L c^4/2G] / [(4pi/3)L^3]
                    = 3 c^4 / (8 pi G L^2)   ->   p = 3 - 1 = 2 (exact).
    The "3" is the spatial volume exponent; the "1" is the Schwarzschild
    mass-radius exponent.  d ln rho_grav / d ln L = -2 identically.

Route 2 — holographic horizon (F190 area entropy + Gibbons-Hawking):
    F190 tiles a horizon with lattice cells carrying entropy a^2/4 ellP^2
    = 2 pi sqrt3 nats each, recovering Bekenstein S = A/4 ellP^2.  The
    cosmic (de Sitter) horizon then has N_dof = A/(4 ellP^2) Bekenstein
    degrees of freedom, A = 4 pi R_H^2.  Gibbons-Hawking equipartition
    gives each ~ k_B T_dS = hbar c/(2 pi R_H).  Hence
        rho_holo = N_dof * (hbar c/2pi R_H) / V(R_H)
                 = 3 hbar c / (8 pi ellP^2 R_H^2)
                 = 3 c^4 / (8 pi G R_H^2)   (since hbar c/ellP^2 = c^4/G)
    identical to Route 1.  dof count ~ R_H^2 (area), energy/dof ~ 1/R_H,
    volume ~ R_H^3  ->  p = 2 again.

Both routes land at rho = 3 c^4/(8 pi G R_H^2) = rho_crit (energy form):
within 1.26x (0.10 dex) of the observed rho_Lambda; the leftover factor
is Omega_Lambda ~ 0.69 (the coincidence problem — the new, smaller
residual).  The statistical sqrt(N) fluctuation route gives p=3/2 and
overshoots by ~31 orders, so it is excluded: the effect is gravitational
(black-hole / holographic), not a mode-counting fluctuation.
"""

import json
import os
import numpy as np
from casim.constants import (
    G_CODATA as _G_CODATA,
    a_over_ellP as _a_over_ellP,
    c_SI as _c_SI,
    ell_P_m as _ell_P_m,
    hbar_SI as _hbar_SI,
)

# ── constants (SI / CODATA) ──────────────────────────────
HBAR = _hbar_SI
C    = _c_SI
ELLP = _ell_P_m
G    = _G_CODATA
MPC  = 3.0856775814913673e22

A_CELL = _a_over_ellP * ELLP
TAU    = A_CELL / (C * np.sqrt(3.0))

RHO_LAMBDA = 6.0e-10
OMEGA_L    = 0.69
H0_KM_S_MPC = 67.0

# F164 bare template density (for the simple p=2 estimate)
RHO_VAC = 3.4563582491862774e111


def hubble_radius():
    H0 = H0_KM_S_MPC * 1e3 / MPC
    return H0, C / H0


# ── Route 1: black-hole bound ────────────────────────────
def schwarzschild_max_mass(L):
    """M_max(L) = L c^2/(2G): mass that puts radius L at its own horizon."""
    return L * C ** 2 / (2 * G)


def rho_grav_bh(L):
    """Max gravitating energy density a region of radius L can hold."""
    E = schwarzschild_max_mass(L) * C ** 2
    V = (4 * np.pi / 3) * L ** 3
    return E / V


def exponent_slope():
    """d ln rho_grav / d ln L — must be exactly -2 (the dilution exponent p)."""
    L1, L2 = 1e25, 1e26
    return np.log(rho_grav_bh(L2) / rho_grav_bh(L1)) / np.log(L2 / L1)


# ── Route 2: holographic (F190 area entropy + Gibbons-Hawking) ──
def rho_grav_holographic(R_H):
    """
    N_dof = A/(4 ellP^2) Bekenstein dof on the cosmic horizon (F190 area law),
    each carrying k_B T_dS = hbar c/(2 pi R_H) by Gibbons-Hawking equipartition.
    """
    A = 4 * np.pi * R_H ** 2
    N_dof = A / (4 * ELLP ** 2)              # Bekenstein entropy in nats
    E_per_dof = HBAR * C / (2 * np.pi * R_H)  # k_B T_dS, T_dS = hbar H/2pi k_B
    E = N_dof * E_per_dof
    V = (4 * np.pi / 3) * R_H ** 3
    return E / V


def run():
    H0, R_H = hubble_radius()

    slope = exponent_slope()                 # = -2 exactly  -> p = 2
    rho_bh = rho_grav_bh(R_H)
    rho_holo = rho_grav_holographic(R_H)
    rho_crit_en = 3 * H0 ** 2 * C ** 2 / (8 * np.pi * G)   # energy critical density

    # closed-form identity check: both routes = 3 c^4/(8 pi G R_H^2)
    rho_closed = 3 * C ** 4 / (8 * np.pi * G * R_H ** 2)

    # the three exponents confronted with data
    pred_p15 = RHO_VAC * (A_CELL / R_H) ** 1.5   # statistical sqrt(N): EXCLUDED
    pred_p2_simple = RHO_VAC * (A_CELL / R_H) ** 2  # naive p=2 (lattice-cell tiling)
    pred_p2_bh = rho_bh                              # p=2 with BH/Bekenstein coeff

    # per-cell entropy that sets the lattice-cell vs nat factor (F190)
    per_cell_nats = A_CELL ** 2 / (4 * ELLP ** 2)    # = 2 pi sqrt3

    result = {
        "finding": "F196",
        "H0_per_s": H0,
        "R_H_m": R_H,
        "dilution_exponent_p": abs(slope),                 # 2.0
        "exponent_slope_dlnrho_dlnL": slope,               # -2.0
        "route1_bh_bound_J_per_m3": rho_bh,
        "route2_holographic_J_per_m3": rho_holo,
        "closed_form_3c4_8piG_RH2": rho_closed,
        "rho_crit_energy_J_per_m3": rho_crit_en,
        "routes_agree_rel": abs(rho_bh - rho_holo) / rho_bh,
        "bh_equals_crit_rel": abs(rho_bh - rho_crit_en) / rho_crit_en,
        "rho_Lambda_observed_J_per_m3": RHO_LAMBDA,
        "saturation_over_observed": rho_bh / RHO_LAMBDA,            # ~1.26
        "saturation_dlog10": float(np.log10(rho_bh / RHO_LAMBDA)),  # 0.10
        "omega_L_times_crit_J_per_m3": OMEGA_L * rho_crit_en,       # ~ rho_Lambda
        "omega_L_residual_over_observed": OMEGA_L * rho_crit_en / RHO_LAMBDA,
        "excluded_p1p5_J_per_m3": pred_p15,                # ~1e21, absurd
        "p1p5_overshoot_log10": float(np.log10(pred_p15 / RHO_LAMBDA)),
        "p2_simple_J_per_m3": pred_p2_simple,
        "p2_simple_dlog10": float(np.log10(pred_p2_simple / RHO_LAMBDA)),
        "per_cell_entropy_nats": per_cell_nats,            # 2 pi sqrt3 = 10.88
        "per_cell_entropy_2pi_sqrt3": 2 * np.pi * np.sqrt(3),
    }

    result["checks"] = {
        "p_equals_2_exact": bool(abs(abs(slope) - 2.0) < 1e-9),
        "two_routes_agree": bool(result["routes_agree_rel"] < 1e-6),
        "saturation_is_critical_density": bool(result["bh_equals_crit_rel"] < 1e-9),
        "saturation_within_0p2_dex_of_obs": bool(abs(result["saturation_dlog10"]) < 0.2),
        "p1p5_excluded": bool(result["p1p5_overshoot_log10"] > 20),
        "f190_per_cell_entropy_2pi_sqrt3": bool(
            abs(per_cell_nats - 2 * np.pi * np.sqrt(3)) < 1e-9),
    }
    return result


if __name__ == "__main__":
    res = run()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.normpath(os.path.join(
        here, "..", "..", "test-results", "F196_dilution_exponent.json"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2)
    for k, v in res.items():
        if isinstance(v, dict):
            print(f"{k}:")
            for kk, vv in v.items():
                print(f"    {kk:38s} = {vv}")
        else:
            print(f"{k:38s} = {v}")
    print(f"\nwrote {out}")
