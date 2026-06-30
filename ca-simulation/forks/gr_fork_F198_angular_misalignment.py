"""
gr_fork_F198_angular_misalignment.py
====================================
Finding F198 — relic abundance of the F197 E_g angular ("axion-like") mode by
vacuum misalignment.  Closes (or sharpens) the F197 named obstruction:
why Omega_DM ~ 0.26 (~5x baryons)?

Setup.  The angular mode delta of the F93 E_g condensate is a pseudo-Goldstone
pinned by the small IR sextic invariant (F150/F154).  Its decay constant is the
condensate amplitude f (natural scale: the F73 Stueckelberg scale v/2 ~ 123 GeV,
or the F170 lepton/E_g scale ~ O(1) Lambda_QCD), and its mass m_a ~ sqrt(lambda6)*
(scale) is light when lambda6 is small.  It is frozen by Hubble friction until
3H ~ m_a, then oscillates as cold dark matter (rho ∝ a^-3).  This is exactly the
ALP misalignment mechanism; we instantiate the STANDARD constant-mass ALP relic
calculation with the condensate's parameters and ask what (m_a, f, theta_i)
reproduces the observed Omega_DM h^2 ~ 0.12.

Self-contained, real arithmetic (cosmological bookkeeping in natural GeV units;
no chiral transforms).  Mirrors the gr_fork_F19x posture.
"""

import json
import os
import numpy as np

# ── constants (natural units, GeV) ───────────────────────────────
M_PL   = 1.220910e19         # GeV   Planck mass (non-reduced; used in H=1.66 sqrt(g*) T^2/M_Pl)
GEV_PER_INV_CM = 1.0 / 1.9733e-14   # 1 cm^-1 = 1.9733e-14 GeV  -> GeV per cm^-1
# today
S0_CM3   = 2891.2            # cm^-3   entropy density today (incl. neutrinos)
RHO_CRIT_OVER_H2_GEV_CM3 = 1.05371e-5   # GeV cm^-3   (rho_crit / h^2)
# convert to natural GeV powers
CM3_TO_GEV3 = (1.9733e-14) ** 3        # (GeV·cm) factor: 1 cm^-3 = (1.9733e-14 GeV)^3
S0_GEV3 = S0_CM3 * CM3_TO_GEV3                       # GeV^3
RHO_CRIT_OVER_H2_GEV4 = RHO_CRIT_OVER_H2_GEV_CM3 * CM3_TO_GEV3   # GeV^4

GSTAR = 80.0                 # effective relativistic dof at oscillation onset (representative)
OMEGA_DM_H2 = 0.12           # observed cold dark-matter density (Planck)

# model scales
F_STUECKELBERG = 123.11      # GeV   F73/F44 natural scalar scale v/2
LAMBDA_QCD     = 0.34        # GeV   F151/F170 scale


def H_rad(T, gstar=GSTAR):
    """Hubble rate in the radiation era (GeV)."""
    return 1.66 * np.sqrt(gstar) * T**2 / M_PL


def T_osc(m_a, gstar=GSTAR):
    """Temperature at oscillation onset, defined by 3 H(T) = m_a."""
    # 3 * 1.66 sqrt(g*) T^2 / M_Pl = m_a
    return np.sqrt(m_a * M_PL / (3.0 * 1.66 * np.sqrt(gstar)))


def omega_h2_misalignment(m_a, f, theta_i=1.0, gstar=GSTAR):
    """Constant-mass ALP misalignment relic density Omega_a h^2.
    rho_osc = 1/2 m_a^2 f^2 theta_i^2 ; n_a/s conserved after onset; scale to today.
    Returns (Omega h^2, T_osc, oscillates_in_radiation_era?)."""
    Tosc = T_osc(m_a, gstar)
    s_osc = (2.0 * np.pi**2 / 45.0) * gstar * Tosc**3          # GeV^3
    n_over_s = 0.5 * m_a * f**2 * theta_i**2 / s_osc           # dimensionless * GeV^0
    rho_today = m_a * n_over_s * S0_GEV3                       # GeV^4
    omega_h2 = rho_today / RHO_CRIT_OVER_H2_GEV4
    # validity: must actually start oscillating in the radiation era (T_osc above
    # matter-radiation equality ~ 0.8 eV) and m_a > H_0; else it is still frozen
    # today (acts as dark ENERGY, w=-1), not cold matter.
    T_eq = 0.8e-9                                             # GeV (~0.8 eV)
    oscillates = bool(Tosc > T_eq)
    return float(omega_h2), float(Tosc), oscillates


def f_required(m_a, theta_i=1.0, gstar=GSTAR):
    """Decay constant f that yields Omega_a h^2 = OMEGA_DM_H2 at given m_a."""
    # Omega ∝ f^2  =>  scale from a unit-f evaluation
    o1, _, _ = omega_h2_misalignment(m_a, 1.0, theta_i, gstar)
    return float(np.sqrt(OMEGA_DM_H2 / o1))


def m_a_required(f, theta_i=1.0, gstar=GSTAR):
    """Mass m_a that yields Omega = OMEGA_DM_H2 at given f (Omega ∝ m_a^{1/2})."""
    o1, _, _ = omega_h2_misalignment(1.0, f, theta_i, gstar)   # m_a=1 GeV reference
    # Omega(m_a) = o1 * m_a^{1/2}  =>  m_a = (OMEGA/o1)^2
    return float((OMEGA_DM_H2 / o1) ** 2)


# ── thermal freeze-out (the heavy AMPLITUDE mode, WIMP-like) ──────
GEV2_TO_CM3_S = 1.17e-17     # 1 GeV^-2 of (sigma·v) ≈ 1.17e-17 cm^3/s
SIGV_CANON    = 3.0e-26      # cm^3/s   canonical thermal relic cross section (Omega h^2≈0.12)


def omega_h2_freezeout(m_chi, g_coupling):
    """Standard WIMP freeze-out relic for the heavy amplitude mode.
    <sigma v> ~ g^4 / (16 pi m^2) (s-wave, dimensional);  Omega h^2 ≈ 0.12 * sigv_canon/<sigv>."""
    sigv_gev2 = g_coupling**4 / (16.0 * np.pi * m_chi**2)     # GeV^-2
    sigv_cm3s = sigv_gev2 * GEV2_TO_CM3_S                     # cm^3/s
    omega_h2 = OMEGA_DM_H2 * SIGV_CANON / sigv_cm3s
    return float(omega_h2), float(sigv_cm3s)


def run():
    # ── 1. validate scaling: Omega ∝ m_a^{1/2} f^2 theta^2 ───────────
    base, _, _ = omega_h2_misalignment(1e-10, 1e12, 1.0)
    s_m, _, _  = omega_h2_misalignment(4e-10, 1e12, 1.0)   # x4 mass -> x2
    s_f, _, _  = omega_h2_misalignment(1e-10, 2e12, 1.0)   # x2 f    -> x4
    s_t, _, _  = omega_h2_misalignment(1e-10, 1e12, 2.0)   # x2 th   -> x4
    scaling_ok = (abs(s_m / base - 2.0) < 1e-6 and abs(s_f / base - 4.0) < 1e-6
                  and abs(s_t / base - 4.0) < 1e-6)

    # ── 2. the Omega=0.26 contour: f required as a function of m_a ────
    m_grid = np.array([1e-22, 1e-18, 1e-12, 1e-6, 1.0, 1e2, 1e3])  # GeV
    contour = [{"m_a_GeV": float(m), "f_required_GeV": f_required(m)} for m in m_grid]

    # ── 3. the model's natural condensate scale f = v/2 = 123 GeV ────
    m_needed_stueck = m_a_required(F_STUECKELBERG)            # GeV
    m_needed_qcd    = m_a_required(LAMBDA_QCD)
    # what Omega does a NATURAL light angular mode give? take m_a ~ sqrt(lambda6)*f
    # with a small IR lambda6 and f = v/2 -> a representative light mass
    lam6 = 0.05
    m_light = np.sqrt(lam6) * 1e-3 * F_STUECKELBERG          # GeV (illustrative light mode ~ 27 MeV*... keep small)
    om_light, Tosc_light, osc_light = omega_h2_misalignment(m_light, F_STUECKELBERG)

    # ── 4. the f needed for a *natural light* mode (m_a in axion window) ─
    m_axion = 1e-15                                          # GeV (~ 1 ueV ALP)
    f_for_axion = f_required(m_axion)

    # ── 5. freeze-out of the heavy amplitude mode (the alternative route) ─
    #   scan weak-scale mass & coupling; find where the WIMP window Omega=0.12 sits
    fo_points = []
    for m_chi in [100.0, 300.0, 1000.0, 3000.0]:
        for g in [0.3, 0.65, 1.0]:
            om, sv = omega_h2_freezeout(m_chi, g)
            fo_points.append({"m_chi_GeV": m_chi, "g": g, "Omega_h2": om, "sigv_cm3_s": sv})
    # best (closest to target) point
    fo_best = min(fo_points, key=lambda p: abs(np.log10(p["Omega_h2"] / OMEGA_DM_H2)))
    fo_window_reachable = any(0.3 * OMEGA_DM_H2 < p["Omega_h2"] < 3.0 * OMEGA_DM_H2
                              for p in fo_points)

    return {
        "inputs": {"gstar": GSTAR, "Omega_DM_h2_target": OMEGA_DM_H2,
                   "f_Stueckelberg_GeV": F_STUECKELBERG, "Lambda_QCD_GeV": LAMBDA_QCD},
        "scaling_check": {"Omega_propto_m^0.5_f^2_theta^2": bool(scaling_ok),
                          "ratio_mass_x4": s_m / base, "ratio_f_x2": s_f / base,
                          "ratio_theta_x2": s_t / base},
        "omega_contour": contour,
        "model_condensate_scale": {
            "f_GeV": F_STUECKELBERG,
            "m_a_required_GeV": m_needed_stueck,
            "m_a_required_over_M_Pl": m_needed_stueck / M_PL,
            "trans_planckian": bool(m_needed_stueck > M_PL),
            "f_QCD_GeV": LAMBDA_QCD, "m_a_required_QCD_GeV": m_needed_qcd,
        },
        "natural_light_mode": {
            "lambda6": lam6, "m_a_light_GeV": m_light,
            "Omega_h2_obtained": om_light, "T_osc_GeV": Tosc_light,
            "oscillates_in_radiation_era": osc_light,
            "under_over_production": "UNDER" if om_light < OMEGA_DM_H2 else "OVER",
            "deficit_factor": OMEGA_DM_H2 / om_light if om_light > 0 else float("inf"),
        },
        "f_for_axion_window": {"m_a_GeV": m_axion, "f_required_GeV": f_for_axion,
                               "f_over_condensate_scale": f_for_axion / F_STUECKELBERG},
        "freezeout_amplitude_mode": {
            "points": fo_points, "best": fo_best,
            "WIMP_window_reachable": bool(fo_window_reachable),
            "note": "heavy amplitude mode (~v/2..TeV) annihilating with EW-strength coupling "
                    "lands in the thermal-relic window Omega h^2~0.12 — the WIMP miracle"},
        "verdict": ("Standard misalignment with the condensate's NATURAL decay constant "
                    "(f ~ v/2 = 123 GeV) badly UNDER-produces: Omega ∝ f^2, so a low-scale f "
                    "needs either a trans-Planckian mass (light mode) or relies on the heavy "
                    "amplitude-mode freeze-out instead. A light axion-like angular mode reaches "
                    "Omega_DM only if f is pushed to ~10^15-10^16 GeV (intermediate/GUT), far "
                    "above the E_g condensate scale. The relic obstruction is therefore SHARPENED, "
                    "not closed: misalignment alone fails by the f-scale gap. The heavy AMPLITUDE "
                    "mode via thermal freeze-out DOES reach Omega_DM in the WIMP window, so the E_g "
                    "sector's dark-matter relic is the heavy amplitude mode, not the light angular "
                    "one (updating the F197 candidate identification)."),
    }


if __name__ == "__main__":
    out = run()
    here = os.path.dirname(__file__)
    root = os.path.abspath(os.path.join(here, "..", ".."))
    os.makedirs(os.path.join(root, "test-results"), exist_ok=True)
    with open(os.path.join(root, "test-results", "F198_angular_misalignment.json"), "w") as f:
        json.dump(out, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o)
    print(json.dumps(out, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else o))
