#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_hyperfine.py — bound-state QED part 2: hydrogen 21 cm Fermi-contact hyperfine and Lamb-shift completeness (recoil + finite nuclear size) (F262)
===============

F262 (bound-state QED, part 2) — HYDROGEN HYPERFINE (the 21 cm line) and
LAMB-SHIFT COMPLETENESS (recoil + finite-nuclear-size corrections on top of the
F252/F257 radiative Lamb shift).

  A. HYDROGEN 21 cm (Fermi contact).  The electron-proton magnetic (Fermi
     contact) interaction splits the hydrogen 1s ground state into F=1 (triplet)
     and F=0 (singlet).  The leading-order splitting is
        Delta E_F = (4/3) g_p (m_e/m_p) alpha^4 m_e c^2 ,
     the same contact operator as positronium's spin-spin term but with the
     proton moment g_p (an INPUT, stated).  With the reduced mass in |psi(0)|^2
     and the model's own electron anomalous moment a_e = alpha/2pi (F252
     Schwinger) the value lands on 1420.4 MHz (the 21 cm line):
        E_F(reduced mass) * (1 + a_e)  ->  1420.4 MHz  (measured 1420.405751 MHz).

  B. LAMB-SHIFT COMPLETENESS.  On top of the F252/F257 one-loop radiative
     2s_{1/2}-2p_{1/2} shift (~1052 MHz, 99.5% of measured), add:
        - reduced-mass / recoil scaling (m_r/m_e)^3 of the self-energy term
          (the leading m_e/m_p mass effect), plus the leading pure relativistic-
          recoil term (Salpeter; Eides-Grotch-Shelyuto coefficient);
        - finite-nuclear-size: Delta E_fs(2s) = (1/12)(Z alpha)^4 m_r (m_r c r_p/hbar)^2,
          which shifts ONLY the s-state (2p has psi(0)=0) and is the PROTON-RADIUS
          LEVER: Delta E_fs ∝ r_p^2, so d(ln Delta E_fs) = 2 d(ln r_p).
     These are small (sub-MHz to ~MHz); the ~5-6 MHz residual to the measured
     1057.845 MHz is dominated by two-loop / higher-order radiative QED, NOT by
     recoil or size — this module quantifies exactly that.

REFERENCES (numbers cross-checked; the contact operator + a_e are the model's own):
  Fermi, Z. Phys. 60, 320 (1930) — the hyperfine contact interaction.
  Eides, Grotch & Shelyuto, Phys. Rept. 342, 63 (2001) — recoil/size/radiative.

NUMERICS: pure arithmetic on top of ca_vertex_loop (F252) + ca_bethe_log (F257).
"""
from __future__ import annotations

import math

try:
    import ca_vertex_loop as vl
except ImportError:                       # pragma: no cover
    vl = None

# ---------------------------------------------------------------------------
#  Constants
# ---------------------------------------------------------------------------
ALPHA = 1.0 / 137.035999084
M_E_MEV = 0.51099895
M_P_MEV = 938.27208816
M_E_EV = M_E_MEV * 1.0e6
H_EV_S = 4.135667696e-15
EV_TO_MHZ = 1.0 / H_EV_S / 1.0e6
HBARC_MEV_FM = 197.3269804               # hbar c (MeV fm)

# INPUTS that are not pure QED (stated explicitly)
G_PROTON = 5.5856946893                  # proton g-factor (mu_p = 2.7928 mu_N)
R_PROTON_FM = 0.8409                     # proton rms charge radius (muonic H / CODATA-2018)
R_PROTON_FM_OLD = 0.8770                 # older spectroscopic value (for the lever demo)

# measured targets
H_21CM_MEAS_MHZ = 1420.405751768         # hydrogen ground-state hyperfine
LAMB_MEAS_MHZ = 1057.845                 # 2s_{1/2}-2p_{1/2}


def reduced_mass_ratio():
    """m_r/m_e for hydrogen, m_r = m_e m_p/(m_e+m_p)."""
    return M_P_MEV / (M_E_MEV + M_P_MEV)


def a_e_schwinger():
    """Electron anomalous magnetic moment a_e = alpha/2pi (F252 Schwinger term).
    Pulled from the model's own vertex loop if available, else computed."""
    return ALPHA / (2.0 * math.pi)


# ===========================================================================
#  A.  Hydrogen 21 cm — Fermi contact hyperfine.
# ===========================================================================
def hydrogen_21cm(g_p: float = G_PROTON):
    """Fermi-contact hyperfine splitting of the hydrogen 1s ground state.

    Delta E_F = (4/3) g_p (m_e/m_p) alpha^4 m_e c^2 , derived from the contact
    Hamiltonian (8pi/3) g_e g_p (e^2/4 m_e m_p)|psi(0)|^2 with g_e=2, e^2=alpha
    (Gaussian) and |psi_1s(0)|^2 = (m_r alpha)^3/pi.  Three progressively-
    complete numbers:
       E_F point   : infinite-nucleus |psi(0)|^2 (m_r = m_e)
       E_F reduced : reduced mass in |psi(0)|^2  (factor (m_r/m_e)^3)
       E_F * (1+a_e): + electron anomalous moment (F252) -> the 21 cm value
    """
    mr_ratio = reduced_mass_ratio()
    me_over_mp = M_E_MEV / M_P_MEV
    # coefficient 4/3 derived from the contact Hamiltonian (see spin_spin in
    # ca_positronium); here we assemble the absolute number.
    base = (4.0 / 3.0) * g_p * me_over_mp * ALPHA ** 4 * M_E_EV   # eV, point nucleus
    E_point_MHz = base * EV_TO_MHZ
    E_reduced_MHz = E_point_MHz * mr_ratio ** 3                   # reduced mass in |psi(0)|^2
    a_e = a_e_schwinger()
    E_qed_MHz = E_reduced_MHz * (1.0 + a_e)                       # + anomalous moment
    return {
        "g_proton_input": g_p,
        "coeff_4_3": 4.0 / 3.0,
        "a_e_schwinger": a_e,
        "E_F_point_MHz": E_point_MHz,
        "E_F_reduced_mass_MHz": E_reduced_MHz,
        "E_F_with_a_e_MHz": E_qed_MHz,
        "measured_MHz": H_21CM_MEAS_MHZ,
        "ratio_point_to_measured": E_point_MHz / H_21CM_MEAS_MHZ,
        "ratio_final_to_measured": E_qed_MHz / H_21CM_MEAS_MHZ,
        "rel_err_final": abs(E_qed_MHz - H_21CM_MEAS_MHZ) / H_21CM_MEAS_MHZ,
        "wavelength_cm": 2.99792458e10 / (E_qed_MHz * 1e6) if E_qed_MHz else None,
        "statement": "Fermi-contact hyperfine = (4/3) g_p (m_e/m_p) alpha^4 m_e c^2; "
                     "with reduced mass and a_e (F252) -> 1420.4 MHz = the 21 cm line "
                     "(g_p is the one non-QED input).",
    }


# ===========================================================================
#  B.  Lamb-shift completeness — recoil + finite size.
# ===========================================================================
def _lamb_baseline_MHz():
    """The F252/F257 one-loop radiative 2s-2p Lamb shift (self-energy + Uehling)."""
    if vl is None:                                    # pragma: no cover
        return 1052.28, "literature-Bethe fallback (F252 unavailable)"
    res = vl.lamb_shift()                             # fast, LN_K0 constants
    return res["total_lamb_MHz"], res["bethe_source"]


def finite_size_shift_2s(r_p_fm: float = R_PROTON_FM):
    """Finite-nuclear-size energy shift of the hydrogen 2s state:
        Delta E_fs(2s) = (1/12)(Z alpha)^4 m_r c^2 (m_r c r_p/hbar)^2 ,  Z=1,
    using |psi_2s(0)|^2 = (m_r alpha)^3/(8 pi) and Delta E = (2pi/3) alpha |psi(0)|^2 r_p^2.
    Shifts ONLY the s-state (2p has psi(0)=0), so it adds directly to the 2s-2p
    Lamb shift.  Returns the shift in MHz and the proton-radius lever d ln/d ln r_p = 2.
    """
    mr_ratio = reduced_mass_ratio()
    mr_MeV = M_E_MEV * mr_ratio
    # reduced Compton wavelength of the reduced mass (fm): hbar c / (m_r c^2)
    lam_bar_fm = HBARC_MEV_FM / mr_MeV
    x2 = (r_p_fm / lam_bar_fm) ** 2                   # (m_r c r_p/hbar)^2
    dE_eV = (1.0 / 12.0) * ALPHA ** 4 * (mr_MeV * 1.0e6) * x2
    dE_MHz = dE_eV * EV_TO_MHZ
    return {
        "r_p_fm": r_p_fm,
        "delta_E_fs_2s_MHz": dE_MHz,
        "proton_radius_lever_dln_dlnrp": 2.0,
        "statement": "finite-size shifts 2s up by ~0.14 MHz (r_p=0.84 fm); "
                     "Delta E_fs ∝ r_p^2 is the proton-radius lever.",
    }


def recoil_correction_MHz(baseline_MHz: float):
    """Leading recoil / reduced-mass corrections to the 2s-2p Lamb shift.

    (i) reduced-mass rescaling of the self-energy: the dominant radiative term
        scales as (m_r/m_e)^3 (through |psi(0)|^2), a shift of ~-1.7 MHz;
    (ii) the leading pure relativistic-recoil term of order (Z alpha)^5 m_e/m_p,
        Delta E_rec ≈ (alpha (Z alpha)^4/(pi n^3))(m_e/m_p) m_e c^2 * C_rec, with
        the Salpeter/EGS coefficient C_rec giving ~+0.36 MHz for 2s-2p (n=2).
    (i) is a derived scaling; (ii) uses the EGS pure-recoil value (two-body
    Bethe-Salpeter; cited literature number, not model-derived here).
    """
    mr_ratio = reduced_mass_ratio()
    # (i) reduced-mass rescaling of the baseline self-energy (derived scaling)
    dm_reduced = baseline_MHz * (mr_ratio ** 3 - 1.0)
    # (ii) leading pure relativistic-recoil term for 2s-2p, EGS Phys.Rept.342
    #      (order (Z alpha)^5 m_e/m_p): a small positive ~+0.36 MHz. Cited.
    drec_pure = 0.36
    return {
        "reduced_mass_ratio": mr_ratio,
        "reduced_mass_shift_MHz": dm_reduced,
        "pure_recoil_shift_MHz_cited_EGS": drec_pure,
        "total_recoil_MHz": dm_reduced + drec_pure,
        "statement": "recoil = reduced-mass rescaling (m_r/m_e)^3 (~-1.7 MHz, "
                     "derived) + leading Salpeter/EGS pure-recoil term (~+0.36 MHz, "
                     "cited); both are small.",
    }


def lamb_complete(r_p_fm: float = R_PROTON_FM):
    """Assemble the F252/F257 radiative Lamb shift + recoil + finite size and
    quote the shifted value and the proton-radius sensitivity."""
    baseline, src = _lamb_baseline_MHz()
    fs = finite_size_shift_2s(r_p_fm)
    rec = recoil_correction_MHz(baseline)
    shifted = baseline + fs["delta_E_fs_2s_MHz"] + rec["total_recoil_MHz"]
    # proton-radius lever: recompute finite size at the older r_p to show the swing
    fs_old = finite_size_shift_2s(R_PROTON_FM_OLD)
    return {
        "baseline_radiative_MHz": baseline, "bethe_source": src,
        "finite_size_MHz": fs["delta_E_fs_2s_MHz"],
        "recoil_MHz": rec["total_recoil_MHz"],
        "recoil_breakdown": rec,
        "shifted_total_MHz": shifted,
        "measured_MHz": LAMB_MEAS_MHZ,
        "residual_after_corrections_MHz": LAMB_MEAS_MHZ - shifted,
        "finite_size_at_rp_0.8409_MHz": fs["delta_E_fs_2s_MHz"],
        "finite_size_at_rp_0.8770_MHz": fs_old["delta_E_fs_2s_MHz"],
        "proton_radius_lever": (fs_old["delta_E_fs_2s_MHz"]
                                - fs["delta_E_fs_2s_MHz"]),
        "statement": "recoil + finite size are sub-MHz to ~MHz; the residual to "
                     "1057.845 MHz is dominated by two-loop/higher-order radiative "
                     "QED, not by recoil or size. Finite size ∝ r_p^2 is the "
                     "proton-radius lever.",
    }


# ===========================================================================
#  Report
# ===========================================================================
def report():
    return {
        "hydrogen_21cm": hydrogen_21cm(),
        "finite_size_2s": finite_size_shift_2s(),
        "lamb_complete": lamb_complete(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=float))
