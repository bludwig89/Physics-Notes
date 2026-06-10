#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_si_scale.py
==============

P6 of docs/roadmaps/roadmap-matter-binding.md — SI / absolute-scale closure for the MATTER
sector.  Turns the dimensionless P2-P4 hadron results into absolute MeV by
adopting the project's CURRENT SI choice plus one QCD-scale anchor, and scores
the resulting absolute numbers against measurement.

THE CURRENT SI CHOICE (two independent anchors, both already adopted)
--------------------------------------------------------------------
  1. GEOMETRIC CELL (metre, second, G) — the F79/F107 canonical lattice ruler,
     locked in F107 and registry-scored in F112:

         a = sqrt(8 pi) 3^{1/4} ell_P = 6.59782 ell_P = 1.06638e-34 m
         tau = a/(c sqrt3) = 2.05366e-43 s        (si-units Option C)
         G  = a^2 c^3 / (8 pi sqrt3 hbar) = 6.674300e-11   (CODATA to 3.0e-8)
         UV cutoff hbar c / a = 1.85e18 GeV = 0.15 E_P

     This fixes the metre and second (and gravity).  It does NOT fix the hadron
     mass scale: the cell's energy unit hbar c/a is ~1.85e18 GeV, ~18 orders
     above the GeV world (F119: the hierarchy number N is the one open scale).

  2. QCD / HADRON SCALE (the kilogram for the strong sector) — fixed by a SINGLE
     measured hadronic quantity, the pion decay constant (chiral-symmetry-
     breaking order parameter):

         f_pi = 92.07 MeV          (THE anchor; user-selected, roadmap P6)

     Every other strong-sector number is then a DIMENSIONLESS model ratio
     (NJL gap / RPA, F77/F103; ECG three-body, F122) times this one scale.

WHAT BECOMES ABSOLUTE (and is scored in test_P6_si_scale.py)
------------------------------------------------------------
  * constituent quark mass m_c            (NJL gap, F77)        ~ 311 MeV
  * nucleon mass m_p ~ 3 m_c              (P2 / F122)           ~ 934 MeV  (-0.5%)
  * neutron-proton splitting m_n - m_p    (F40 quark gap + EM)  +1.51 MeV
  * pion m_pi, sigma m_sigma, rho m_rho   (F77/F103)
  * quark condensate <qbar q>^{1/3}       (F77)
  * deuteron OPEP range / binding         (P3/P4, F103/F104)

PHILOSOPHY
----------
Only ONE dimensionful number enters the strong sector (f_pi); the NJL couplings
{G Lam^2, m0/Lam} are dimensionless SHAPE inputs.  So each absolute mass is
reported as (model ratio m_i/f_pi) x f_pi^phys — the model's structure times the
single anchor.  This is the strong-sector analogue of F112's geometric registry.

All arithmetic REAL.  numpy only.  Imports the already-validated F77/F103 meson
solver (`ca_meson`) and the F122 three-body baryon solver (`ca_baryon_dynamics`).
"""

from __future__ import annotations

import numpy as np

import ca_meson as MES
import ca_baryon_dynamics as BAR


# ===========================================================================
#  1. The canonical geometric cell (F79 / F107 / F112).  Values are the
#     adopted constants, reproduced here so the SI map is self-contained.
# ===========================================================================
ELL_P = 1.616255e-35       # m   (CODATA Planck length)
C_SI = 2.99792458e8        # m/s (exact)
HBAR = 1.054571817e-34     # J s (CODATA)
G_CODATA = 6.67430e-11     # m^3 kg^-1 s^-2 (CODATA)

A_OVER_ELLP = np.sqrt(8.0 * np.pi) * 3.0 ** 0.25   # = 6.59782 (F79, parameter-free)


def canonical_cell():
    """Return the adopted geometric SI cell and its derived G / UV cutoff."""
    a = A_OVER_ELLP * ELL_P                       # metre anchor
    tau = a / (C_SI * np.sqrt(3.0))               # Option C: a/tau = c sqrt3
    G_pred = a ** 2 * C_SI ** 3 / (8.0 * np.pi * np.sqrt(3.0) * HBAR)
    uv_GeV = HBAR * C_SI / a / 1.602176634e-10    # hbar c / a in GeV
    return {
        "a_over_ellP": A_OVER_ELLP,
        "a_m": a,
        "tau_s": tau,
        "lightcone_m_s": a / tau,                 # = c sqrt3
        "G_pred": G_pred,
        "G_rel_err": abs(G_pred - G_CODATA) / G_CODATA,
        "UV_cutoff_GeV": uv_GeV,
    }


# ===========================================================================
#  2. The QCD anchor and the f_pi-scaled strong-sector spectrum.
#     Single dimensionful input: f_pi^phys.  Everything else is a model ratio.
# ===========================================================================
F_PI_PHYS = 92.07          # MeV  — THE QCD-scale anchor (chiral SB order param)


def strong_spectrum(f_pi_phys=F_PI_PHYS):
    """Absolute MeV strong-sector spectrum from the F77/F103 NJL dimensionless
    ratios times the single anchor f_pi_phys.

    Returns a dict of absolute masses (MeV) plus the underlying ratios.
    """
    s = MES.solve_meson_spectrum()        # canonical F77/F103 point (GeV units)
    f_pi_model = s["f_pi"] * 1e3          # MeV, the model's own f_pi
    scale = f_pi_phys / f_pi_model        # the single anchor rescaling (~1.00)

    def to_MeV(x_GeV):
        return x_GeV * 1e3 * scale

    m_c = to_MeV(s["m_c"])
    out = {
        "f_pi_model_MeV": f_pi_model,
        "anchor_scale": scale,
        "m_c": m_c,                                  # constituent quark mass
        "m_pi": to_MeV(s["m_pi"]),
        "m_sigma": to_MeV(s["m_sigma"]),
        "m_rho": to_MeV(s["m_rho"]),
        "condensate_root": to_MeV(s["condensate_root"]),   # <qbar q>^{1/3}/flavour
        "ratios": {
            "m_c_over_fpi": s["m_c"] / s["f_pi"],
            "m_pi_over_fpi": s["m_pi"] / s["f_pi"],
            "m_sigma_over_fpi": s["m_sigma"] / s["f_pi"],
            "m_rho_over_fpi": s["m_rho"] / s["f_pi"],
        },
        "gmor_rel": s["gmor_rel"],
        "m_sigma_over_2mc": s["m_sigma_over_2mc"],
    }
    return out


# ===========================================================================
#  3. The nucleon in absolute MeV (P2 / F122).
#     Under the f_pi anchor the relevant quark mass is the CONSTITUENT mass m_c
#     (dynamically generated by chi-SB, F77) — NOT the current mass.  F97: the
#     nucleon mass is this dynamical mass, not the few-MeV current-quark sum.
#     Leading constituent estimate m_p ~ 3 m_c; the residual (confinement/OGE/
#     hyperfine) binding among constituents is the few-% correction (P2/F113).
# ===========================================================================
def nucleon_mass(f_pi_phys=F_PI_PHYS):
    sp = strong_spectrum(f_pi_phys)
    m_c = sp["m_c"]
    m_p_leading = 3.0 * m_c                # three constituent quarks
    return {
        "m_c_MeV": m_c,
        "m_p_3mc_MeV": m_p_leading,
        "m_p_PDG": 938.272,
        "m_p_rel_err": (m_p_leading - 938.272) / 938.272,
    }


def np_splitting(f_pi_phys=F_PI_PHYS):
    """n-p splitting in MeV (already absolute: F40 quark gap + EM self-energy)."""
    # PDG current masses (F40 ratio m_d/m_u ~ 2 is consistent); EM external (P5).
    res = BAR.neutron_minus_proton(m_u=2.16, m_d=4.67, sigma=1.0, alpha_s=0.5,
                                   delta_em_p=1.00, delta_em_n=0.0)
    res["m_n_minus_m_p_PDG"] = 1.293
    return res


# ===========================================================================
#  4. The full P6 registry (used by the test).
# ===========================================================================
def si_registry(f_pi_phys=F_PI_PHYS):
    return {
        "cell": canonical_cell(),
        "anchor_f_pi_MeV": f_pi_phys,
        "strong": strong_spectrum(f_pi_phys),
        "nucleon": nucleon_mass(f_pi_phys),
        "np_split": np_splitting(f_pi_phys),
    }


if __name__ == "__main__":
    reg = si_registry()
    c = reg["cell"]
    print("=== P6 SI scale: canonical cell + f_pi anchor ===")
    print(f"a = {c['a_m']:.5e} m = {c['a_over_ellP']:.5f} ell_P,  tau = {c['tau_s']:.5e} s")
    print(f"G_pred = {c['G_pred']:.6e}  (rel err {c['G_rel_err']:.1e} vs CODATA)")
    print(f"UV cutoff = {c['UV_cutoff_GeV']:.3e} GeV")
    s, n = reg["strong"], reg["nucleon"]
    print(f"\nf_pi anchor = {reg['anchor_f_pi_MeV']} MeV  (model f_pi {s['f_pi_model_MeV']:.2f} -> scale {s['anchor_scale']:.4f})")
    print(f"m_c      = {s['m_c']:7.2f} MeV")
    print(f"m_pi     = {s['m_pi']:7.2f} MeV   (PDG 138.04)")
    print(f"m_sigma  = {s['m_sigma']:7.2f} MeV")
    print(f"m_rho    = {s['m_rho']:7.2f} MeV   (PDG 775.26)")
    print(f"<qq>^1/3 = {s['condensate_root']:7.2f} MeV")
    print(f"m_p~3m_c = {n['m_p_3mc_MeV']:7.2f} MeV   (PDG 938.27, {n['m_p_rel_err']*100:+.2f}%)")
    sp = reg["np_split"]
    print(f"m_n-m_p  = {sp['m_n_minus_m_p']:+.2f} MeV   (PDG +1.293)")
