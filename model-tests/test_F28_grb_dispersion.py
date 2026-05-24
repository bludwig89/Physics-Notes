"""
F27 — GRB / AGN dispersion test of the F26 photon rotation prediction
=====================================================================
Date: 2026-05-23

Goal
----
Confront F26's structural prediction against current best experimental limits
on photon vacuum dispersion (quadratic, n=2, subluminal).

F26 prediction (composite-photon rotation truncation)
-----------------------------------------------------
The exact (E, B) rotation per CA tick is Ω = 2 ω(|k|/2). Expanding:

    ω(k) = c · k  −  c³ k³ / 6  +  O(k⁵)

Phase velocity:   v_φ/c = 1 − (c k)² / 6
Group velocity:   v_g/c = 1 − (c k)² / 2     ← what time-of-flight measures

Assuming the lattice tick is the Planck time (Bisio et al. unique-QCA),
Ω = E / E_Planck, so:

    v_g(E) / c  =  1  −  ½ (E / E_Planck)²

Mapped onto the standard LIV parameterisation  v/c = 1 − s_n (E/E_QG,n)^n
with n = 2, s = +1 (subluminal):

    E_QG,2 (F26)  =  √2 · E_Planck  ≈  1.726 × 10¹⁹ GeV

Method
------
For each archetypal source (GRB or AGN flare with high-E photon timing),
compute:
  1. The F26-predicted spectral time-of-flight delay Δt_F26
       Δt  =  (3/2) · (E_h² − E_l²) / E_QG² · (1/H₀) · κ₂(z)
     with κ₂(z) = ∫₀^z (1+z')² / √(Ω_m(1+z')³ + Ω_Λ) dz'.
  2. The observed (or implied) experimental sensitivity Δt_obs.
  3. The verdict: EXCLUDED if Δt_F26 > Δt_obs, MARGINAL if within a decade,
     BELOW SENSITIVITY otherwise.

Sources used
------------
  - GRB 090510   z=0.903, E_max≈31 GeV   (Fermi-LAT, Vasileiou+ 2013)
                 Published 95% CL bound: E_QG,2 > 1.3 × 10¹¹ GeV (subluminal)
  - GRB 221009A  z=0.151, E_max≈13 TeV   (LHAASO 2024)
                 Published 95% CL bound: E_QG,2 > 7.0 × 10¹¹ GeV (subluminal)
  - Mrk 501      z=0.034, E_max≈10 TeV   (MAGIC 2008)
                 Published 95% CL bound: E_QG,2 > 5.7 × 10¹⁰ GeV (subluminal)

Output
------
  - prints a table to stdout
  - writes test-results/F27_grb_dispersion.json
"""

import os, sys, json, math
import numpy as np
from scipy.integrate import quad

THIS = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.abspath(os.path.join(THIS, '..', 'test-results'))

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
E_PLANCK_GEV = 1.22089e19        # Planck energy in GeV
H0_KM_S_MPC  = 67.4              # Planck 2018 cosmology
MPC_M        = 3.0857e22         # 1 Mpc in metres
H0_PER_SEC   = (H0_KM_S_MPC * 1e3) / MPC_M   # ≈ 2.184e-18 s⁻¹
T_HUBBLE_SEC = 1.0 / H0_PER_SEC              # ≈ 4.578e17 s
OMEGA_M      = 0.315
OMEGA_L      = 0.685

# F26 prediction
E_QG_F26_GEV = math.sqrt(2.0) * E_PLANCK_GEV       # subluminal n=2

# --------------------------------------------------------------------------
# Cosmological distance factor κ_n(z) for n=2
# --------------------------------------------------------------------------
def kappa_n(z, n=2):
    integrand = lambda zp: (1.0 + zp)**n / math.sqrt(OMEGA_M*(1.0+zp)**3 + OMEGA_L)
    val, _ = quad(integrand, 0.0, z)
    return val

def delta_t_n2(E_h_GeV, E_l_GeV, z, E_QG_GeV):
    """Predicted arrival-time delay for n=2 subluminal LIV (sec)."""
    prefac = 1.5 * (E_h_GeV**2 - E_l_GeV**2) / (E_QG_GeV**2)
    return prefac * T_HUBBLE_SEC * kappa_n(z, 2)

# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------
SOURCES = [
    {
        "name":              "GRB 090510 (Fermi-LAT)",
        "z":                 0.903,
        "E_high_GeV":        31.0,
        "E_low_GeV":         1.0e-4,           # ~100 keV
        "E_QG_limit_GeV":    1.3e11,           # Vasileiou+ 2013 95% CL subluminal n=2
        "ref":               "Vasileiou et al. 2013, PRD 87, 122001 (arXiv:1305.3463)",
    },
    {
        "name":              "GRB 221009A (LHAASO)",
        "z":                 0.151,
        "E_high_GeV":        1.3e4,            # ~13 TeV
        "E_low_GeV":         2.0e2,            # 200 GeV (LHAASO low edge)
        "E_QG_limit_GeV":    7.0e11,           # Piran & Ouyang 2024 best n=2 subluminal
        "ref":               "Piran & Ouyang 2024 (arXiv:2308.03031); LHAASO Collab. 2024",
    },
    {
        "name":              "Mrk 501 flare (MAGIC 2005)",
        "z":                 0.034,
        "E_high_GeV":        1.0e4,            # ~10 TeV
        "E_low_GeV":         2.5e2,            # 250 GeV
        "E_QG_limit_GeV":    5.7e10,           # MAGIC Collab. 2008 95% CL n=2 subluminal
        "ref":               "MAGIC Collab. 2008, Phys. Lett. B 668, 253",
    },
]

# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------
def main():
    print('=' * 78)
    print('F27 — GRB / AGN dispersion test of F26 photon rotation prediction')
    print('=' * 78)
    print(f'Date 2026-05-23')
    print()
    print(f'F26 group-velocity correction:  v_g/c = 1 − ½ (E / E_P)²')
    print(f'F26 equivalent LIV scale     :  E_QG,2 = √2 · E_Planck = {E_QG_F26_GEV:.4e} GeV')
    print(f'(Planck energy             E_P = {E_PLANCK_GEV:.4e} GeV)')
    print()
    print(f'Cosmology: H₀ = {H0_KM_S_MPC} km/s/Mpc, Ω_m = {OMEGA_M}, Ω_Λ = {OMEGA_L}')
    print(f'Hubble time t_H = 1/H₀ = {T_HUBBLE_SEC:.4e} s')
    print()

    output = {
        "test":            "F27 GRB/AGN photon dispersion vs F26",
        "date":            "2026-05-23",
        "F26_prediction": {
            "v_g_form":             "v_g/c = 1 − ½ (E/E_Planck)²",
            "equivalent_E_QG_GeV":  E_QG_F26_GEV,
            "sign":                 "subluminal",
            "coefficient":          "1/2 (group velocity); 1/6 (phase velocity)",
        },
        "cosmology": {
            "H0_km_s_Mpc": H0_KM_S_MPC,
            "Omega_m":     OMEGA_M,
            "Omega_L":     OMEGA_L,
            "t_Hubble_s":  T_HUBBLE_SEC,
        },
        "sources": [],
    }

    print(f'{"Source":<32} {"z":>6} {"E_h [GeV]":>12} {"κ₂(z)":>7} '
          f'{"Δt(F26) [s]":>14} {"Δt(limit) [s]":>16} {"verdict":>20}')
    print('-' * 116)

    for src in SOURCES:
        z   = src["z"]
        E_h = src["E_high_GeV"]
        E_l = src["E_low_GeV"]
        k2  = kappa_n(z, 2)

        dt_F26   = delta_t_n2(E_h, E_l, z, E_QG_F26_GEV)
        dt_limit = delta_t_n2(E_h, E_l, z, src["E_QG_limit_GeV"])

        # Verdict: experimental sensitivity ≈ dt_limit (the delay that the
        # quoted E_QG limit corresponds to). If F26's predicted delay exceeds
        # that sensitivity, F26 would already be excluded.
        ratio = dt_F26 / dt_limit
        if ratio > 1.0:
            verdict = "EXCLUDED"
        elif ratio > 0.1:
            verdict = "MARGINAL"
        else:
            verdict = f"below sens. ({-math.log10(ratio):.1f} dec)"

        # Also: ratio of F26 LIV scale to experimental floor.
        scale_margin = E_QG_F26_GEV / src["E_QG_limit_GeV"]

        print(f'{src["name"]:<32} {z:>6.3f} {E_h:>12.3e} {k2:>7.3f} '
              f'{dt_F26:>14.3e} {dt_limit:>16.3e} {verdict:>20}')

        output["sources"].append({
            "name":                  src["name"],
            "z":                     z,
            "E_high_GeV":            E_h,
            "E_low_GeV":             E_l,
            "kappa_2_z":             k2,
            "dt_F26_s":              dt_F26,
            "dt_experimental_limit_s": dt_limit,
            "ratio_F26_over_limit":  ratio,
            "verdict":               verdict,
            "E_QG_limit_GeV":        src["E_QG_limit_GeV"],
            "E_QG_F26_over_limit":   scale_margin,
            "reference":             src["ref"],
        })

    print('-' * 116)
    print()

    # ----- Energy threshold to reach F26 at current best (LHAASO) timing -----
    print('Photon energy required to bring Δt(F26) up to today\'s best limit:')
    print(f'(i.e., the energy at which F26 would START to become testable)')
    print()
    for src in SOURCES:
        # Δt(F26) at E_h_new equals Δt(experimental limit) at E_h_actual?
        # delta_t(F26, E_new) = delta_t(limit, E_actual)
        # 1.5 E_new² / E_QG_F26² · t_H · κ_2 = delta_t_limit
        # so E_new = E_actual · (E_QG_F26 / E_QG_limit)
        E_h_actual = src["E_high_GeV"]
        scale = E_QG_F26_GEV / src["E_QG_limit_GeV"]
        E_h_needed = E_h_actual * scale
        print(f'  {src["name"]:<32} need E ≥ {E_h_needed:.3e} GeV '
              f'({E_h_needed/1e9:.3e} EeV)  '
              f'[× {scale:.2e} current observed]')

    output["energy_threshold_to_test"] = [
        {"source": s["name"], "E_required_GeV": s["E_high_GeV"] * (E_QG_F26_GEV / s["E_QG_limit_GeV"])}
        for s in SOURCES
    ]

    print()
    print('=' * 78)
    print('Summary')
    print('=' * 78)
    best_ratio = max(s["ratio_F26_over_limit"] for s in output["sources"])
    margin_decades = -math.log10(best_ratio)
    print(f'  Best constraint margin: {margin_decades:.1f} decades in Δt')
    print(f'  F26 E_QG    = {E_QG_F26_GEV:.3e} GeV')
    print(f'  Best limit  = {max(s["E_QG_limit_GeV"] for s in SOURCES):.3e} GeV (LHAASO 221009A)')
    print(f'  Ratio        = {E_QG_F26_GEV / max(s["E_QG_limit_GeV"] for s in SOURCES):.2e}')
    print()
    print(f'  Verdict: F26 is NOT excluded by any current experiment.')
    print(f'  It sits ~{margin_decades:.0f} decades below current Δt sensitivity in the')
    print(f'  best case (LHAASO GRB 221009A). Confirmation/exclusion requires')
    print(f'  photon energies ~{best_ratio**-0.5:.1e}× higher, or proportionally')
    print(f'  longer baselines.')

    output["summary"] = {
        "best_margin_decades_in_dt":    margin_decades,
        "best_E_QG_limit_GeV":          max(s["E_QG_limit_GeV"] for s in SOURCES),
        "F26_scale_above_best_limit":   E_QG_F26_GEV / max(s["E_QG_limit_GeV"] for s in SOURCES),
        "verdict":                      "not excluded; below current Δt sensitivity",
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, "F27_grb_dispersion.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print()
    print(f'Saved JSON: {out_path}')


if __name__ == '__main__':
    main()
