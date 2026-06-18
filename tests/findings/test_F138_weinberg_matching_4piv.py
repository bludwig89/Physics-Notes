"""
F138 — Closing the +12% Weinberg gap: sin^2 th_W = 1/4 as the COMPOSITENESS-SCALE
matching condition (mu* = 4 pi v), not a bare UV boundary value.

Chain under test (no new free parameters; only the model's existing rulers
alpha_em and the EW scale v = (sqrt2 G_F)^(-1/2)):

  WM1 (exact algebra)
      (a) In any embedding with g'^2/g^2 = (1/3) * gX^2/(gX^2 + kappa) — i.e. the
          331-type relation gX^2/gL^2 = s^2/(1-4s^2) — sin^2 th_W -> 1/4 EXACTLY
          as the abelian coupling gX -> infinity. F41's hypercharge is a
          Stueckelberg wrap on U(x) with NO independent lattice kinetic term
          (formally infinite bare abelian coupling), so sin^2 th_W = 1/4 is the
          matching value AT THE SCALE WHERE THE Y KINETIC TERM IS GENERATED.
      (b) Bridge identity (2/9)/(1/4) = 8/9 (exact rational).
      (c) F49's 2/9 read on-shell: m_Z/m_W = 3/sqrt7 (algebraic).

  WM2 (one-loop RG prediction)
      Anchor sin^2 th_W(mu*) = 1/4 at mu* = 4 pi v (NDA compositeness scale of
      the Higgs-free EWSB sector). One magnitude fixed by alpha_em(M_Z).
      PREDICT sin^2 th_W(M_Z) in MS-bar; compare to PDG 0.23122.
      Run both SM and Higgs-free (model-correct) beta functions.

  WM3 (consistency checks)
      (a) F115 CM2b crossing scale mu_star (measured trajectory through 1/4)
          vs 4 pi v: agreement in ln mu.
      (b) On-shell endpoint: measured 1 - (mW/mZ)^2 vs 2/9; mZ/mW vs 3/sqrt7.

Plain python + fractions; <0.1 s.
"""

import json, math
from fractions import Fraction as F

results = {}

# ----------------------------------------------------------------------
# Inputs (PDG / CODATA; same anchors as F115 where shared)
# ----------------------------------------------------------------------
M_Z   = 91.1880               # GeV (PDG 2024)
m_W   = 80.3692               # GeV (PDG 2024 world average)
inv_alpha_em_MZ = 127.951     # MS-bar
sin2_MZ_msbar   = 0.23122     # PDG MS-bar
G_F   = 1.1663787e-5          # GeV^-2
v     = (math.sqrt(2.0)*G_F)**-0.5      # 246.22 GeV
mu_star_NDA = 4.0*math.pi*v             # 3.094 TeV

# ----------------------------------------------------------------------
# WM1 — exact algebra
# ----------------------------------------------------------------------
# (a) 331-type relation: s^2 = t2/(1+4 t2) with t2 = gX^2/gL^2 -> 1/4 as t2->inf.
#     Symbolically: lim s^2 = 1/4; and s^2 < 1/4 for all finite t2 > 0.
def s2_of_t2(t2):   # t2 = gX^2/gL^2
    return t2/(1.0 + 4.0*t2)
cap_checks = all(s2_of_t2(t) < 0.25 for t in (0.1, 1.0, 10.0, 1e6))
cap_limit  = abs(s2_of_t2(1e15) - 0.25) < 1e-14
# (b) bridge
bridge = F(2,9) / F(1,4)            # = 8/9 exact
# (c) on-shell algebra: sin^2_os = 2/9 <=> (mW/mZ)^2 = 7/9 <=> mZ/mW = 3/sqrt7
mZmW_F49 = 3.0/math.sqrt(7.0)
results["WM1"] = {
    "s2(t2)_strictly_below_quarter": cap_checks,
    "s2->1/4_as_gX->inf": cap_limit,
    "bridge_(2/9)/(1/4)": str(bridge),
    "bridge_is_8/9": bridge == F(8,9),
    "mZ/mW_at_2/9": mZmW_F49,
    "PASS": cap_checks and cap_limit and bridge == F(8,9),
}

# ----------------------------------------------------------------------
# WM2 — one-loop running from mu* = 4 pi v down to M_Z
# ----------------------------------------------------------------------
# GUT normalization g1^2 = (5/3) g'^2; alpha_em^-1 = alpha_2^-1 + (5/3) alpha_1^-1;
# sin^2 th_W(mu) = alpha_2^-1(mu) / alpha_em^-1(mu).
# Running (down): alpha_i^-1(M_Z) = alpha_i^-1(mu*) + (b_i/2pi) ln(mu*/M_Z).
def b_coeffs(Ng, NH):
    b1 = F(4,3)*Ng + F(1,10)*NH
    b2 = F(-22,3) + F(4,3)*Ng + F(1,6)*NH
    return float(b1), float(b2)

def predict_sin2_MZ(mu_star, Ng, NH, label):
    b1, b2 = b_coeffs(Ng, NH)
    twopi = 2.0*math.pi
    L = math.log(mu_star/M_Z)
    bem = b2 + (5.0/3.0)*b1                       # beta coeff of alpha_em^-1
    inv_aem_star = inv_alpha_em_MZ - (bem/twopi)*L
    inv_a2_star  = 0.25*inv_aem_star              # sin^2(mu*) = 1/4 EXACT anchor
    inv_a2_MZ    = inv_a2_star + (b2/twopi)*L
    s2 = inv_a2_MZ / inv_alpha_em_MZ
    return {
        "label": label, "b1": b1, "b2": b2,
        "mu_star_GeV": mu_star, "L": L,
        "sin2(mu*)": 0.25,
        "sin2_MZ_pred": s2,
        "resid_vs_MSbar_%": 100.0*(s2 - sin2_MZ_msbar)/sin2_MZ_msbar,
    }

wm2_sm = predict_sin2_MZ(mu_star_NDA, 3, 1, "SM (3 gen, 1 Higgs doublet)")
wm2_hf = predict_sin2_MZ(mu_star_NDA, 3, 0, "Higgs-free (model-correct)")
results["WM2"] = {
    "v_GeV": v, "mu*=4piv_GeV": mu_star_NDA,
    "scenarios": [wm2_sm, wm2_hf],
    "bare_gap_was_%": 100.0*(0.25 - sin2_MZ_msbar)/sin2_MZ_msbar,
    "PASS": abs(wm2_hf["resid_vs_MSbar_%"]) < 0.5,
}

# ----------------------------------------------------------------------
# WM3 — consistency checks
# ----------------------------------------------------------------------
# (a) F115 CM2b crossing scale (measured trajectory through 1/4) vs 4 pi v
def crossing_scale(Ng, NH):
    b1, b2 = b_coeffs(Ng, NH)
    twopi = 2.0*math.pi
    inv_a2 = sin2_MZ_msbar * inv_alpha_em_MZ
    inv_a1 = (inv_alpha_em_MZ - inv_a2) * 3.0/5.0
    num = inv_a1 - 1.8*inv_a2
    den = (b1/twopi) - 1.8*(b2/twopi)
    t = num/den
    return M_Z*math.exp(t)
mu_x_sm = crossing_scale(3,1)
mu_x_hf = crossing_scale(3,0)
ln_offset_hf = math.log(mu_x_hf/mu_star_NDA)
# (b) on-shell endpoint
sin2_os_meas = 1.0 - (m_W/M_Z)**2
mZmW_meas    = M_Z/m_W
res_29  = 100.0*(float(F(2,9)) - sin2_os_meas)/sin2_os_meas
res_mzw = 100.0*(mZmW_F49 - mZmW_meas)/mZmW_meas
results["WM3"] = {
    "mu_star_crossing_SM_GeV": mu_x_sm,
    "mu_star_crossing_HF_GeV": mu_x_hf,
    "4piv_GeV": mu_star_NDA,
    "ln(mu_x_HF/4piv)": ln_offset_hf,
    "sin2_onshell_meas": sin2_os_meas,
    "2/9": float(F(2,9)), "resid_2/9_vs_onshell_%": res_29,
    "mZ/mW_meas": mZmW_meas, "3/sqrt7": mZmW_F49,
    "resid_3/sqrt7_%": res_mzw,
    "PASS": (abs(ln_offset_hf) < 0.15) and (abs(res_mzw) < 0.1),
}

results["ALL_PASS"] = all(results[k]["PASS"] for k in ("WM1","WM2","WM3"))
print(json.dumps(results, indent=2, default=str))

print("\n" + "="*72)
print("F138 — Weinberg gap closure: sin^2 th_W = 1/4 matched at mu* = 4 pi v")
print("="*72)
print(f"  v = {v:.3f} GeV   ->   mu* = 4 pi v = {mu_star_NDA/1e3:.3f} TeV")
for s in (wm2_sm, wm2_hf):
    print(f"  [{s['label']}]")
    print(f"     sin^2 th_W(M_Z) predicted = {s['sin2_MZ_pred']:.5f}"
          f"   (PDG MS-bar 0.23122, resid {s['resid_vs_MSbar_%']:+.2f}%)")
print(f"  bare gap was {results['WM2']['bare_gap_was_%']:+.2f}%  ->  "
      f"{wm2_hf['resid_vs_MSbar_%']:+.2f}% (Higgs-free)")
print(f"  crossing scale (HF, measured trajectory) = {mu_x_hf/1e3:.2f} TeV; "
      f"ln-offset to 4piv = {ln_offset_hf:+.3f}")
print(f"  on-shell: 1-(mW/mZ)^2 = {sin2_os_meas:.5f} vs 2/9 = 0.22222 "
      f"({res_29:+.2f}%);  mZ/mW = {mZmW_meas:.5f} vs 3/sqrt7 = {mZmW_F49:.5f} "
      f"({res_mzw:+.3f}%)")
print(f"  ALL_PASS = {results['ALL_PASS']}")

with open("test-results/F138_weinberg_matching_4piv.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
