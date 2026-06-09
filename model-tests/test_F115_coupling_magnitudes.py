"""
F115 — Gauge coupling magnitudes e, g, g_s from the model.

Three results, each a separate check block:

  CM1  EW reduction (exact, algebraic): at the bare swap angle sin^2 th_W = 1/4
       the three electroweak couplings collapse to ONE free magnitude:
         e   = g/2,   g' = g/sqrt3,   g_Z = 2g/sqrt3,   g_s-independent.
       The whole EW coupling sector is a one-parameter family.

  CM2  One-loop running of the bare swap angle (the decisive computation the
       audit C.5 asks for). Boundary at the lattice (UV) scale mu_L = 1/a =
       M_Pl/6.5978 (F79/F107): sin^2 th_W = 1/4 (F45). Fix the single free
       magnitude by matching alpha_em(M_Z); PREDICT sin^2 th_W(M_Z), m_Z/m_W,
       g_V^{eL}, and (under g2=g3 at mu_L) alpha_s(M_Z). Run both the SM and the
       Higgs-free (model-correct) beta functions.

  CM3  g_s from the rotor stiffness (F110 chi=1/(4 g_s^2) + rule's symmetric
       (E,B) normalization chi=1): the QCA fixes the COMBINATION g_s^2 * chi = 1/4,
       removing g_s as an independent input once the rule sets the stiffness.
       Cross-check with the F100/F101 sigma_1 = (1/4)<1/Omega>_BZ chain.

All arithmetic is plain python/numpy; rational identities use fractions.
"""

import json, math
from fractions import Fraction as F

results = {}

# ----------------------------------------------------------------------
# CM1 — EW reduction at the bare swap angle (exact rationals / surds)
# ----------------------------------------------------------------------
# sin^2 th_W = 1/4  ->  sin = 1/2, cos = sqrt3/2, tan = 1/sqrt3
sin2 = F(1, 4)
cos2 = 1 - sin2
tan2 = sin2 / cos2                      # = 1/3 = g'^2/g^2  (F45)
# couplings in units of g:
#   e   = g sin th          -> e/g   = 1/2
#   g'  = e/cos th = g tan  -> g'/g  = 1/sqrt3
#   g_Z = g/cos th          -> g_Z/g = 2/sqrt3
e_over_g_sq   = sin2                    # (e/g)^2  = 1/4
gp_over_g_sq  = tan2                    # (g'/g)^2 = 1/3
gZ_over_g_sq  = 1 / cos2                # (g_Z/g)^2 = 4/3
gpgz_consistency = (gp_over_g_sq == F(1,3)) and (e_over_g_sq == F(1,4))
results["CM1"] = {
    "sin2_thetaW_bare": float(sin2),
    "(e/g)^2": str(e_over_g_sq), "(g'/g)^2": str(gp_over_g_sq),
    "(g_Z/g)^2": str(gZ_over_g_sq),
    "g'^2/g^2 == 1/3 (F45)": gp_over_g_sq == F(1,3),
    "free_magnitudes_in_EW_sector": 1,
    "PASS": gpgz_consistency,
}

# ----------------------------------------------------------------------
# CM2 — one-loop running from the lattice (UV) scale to M_Z
# ----------------------------------------------------------------------
# Scales
M_Pl   = 1.220910e19          # GeV, non-reduced Planck energy hbar c / l_P
a_over_lP = math.sqrt(8*math.pi) * 3**0.25   # F79 = 6.59783...
mu_L   = M_Pl / a_over_lP     # lattice momentum scale 1/a in energy units
M_Z    = 91.1876              # GeV
L      = math.log(mu_L / M_Z) # RG "time" interval (positive)

# Measured low-energy anchors (PDG)
inv_alpha_em_MZ = 127.951     # alpha_em(M_Z)^-1, MS-bar
sin2_MZ_msbar   = 0.23122     # PDG MS-bar
sin2_MZ_onshell = 0.22339     # PDG on-shell 1 - (m_W/m_Z)^2
alpha_s_MZ_meas = 0.1179

# One-loop beta coefficients (GUT normalization, g1^2 = 5/3 g'^2)
#   d alpha_i^-1 / d ln mu = - b_i / (2 pi)
def b_coeffs(Ng, NH):
    b1 = F(4,3)*Ng + F(1,10)*NH      # U(1)_Y
    b2 = F(-22,3) + F(4,3)*Ng + F(1,6)*NH   # SU(2)_L
    b3 = F(-11,1) + F(4,3)*Ng        # SU(3)_c
    return float(b1), float(b2), float(b3)

def run_scenario(Ng, NH, label, assume_g2_eq_g3=True):
    b1, b2, b3 = b_coeffs(Ng, NH)
    twopi = 2*math.pi
    # Boundary at mu_L in terms of x = 1/alpha_*(mu_L) (single free magnitude):
    #   alpha_2^-1(mu_L) = x/4 ; alpha_1^-1(mu_L) = 0.45 x ; alpha_3^-1 = x/4
    #   alpha_em^-1(mu_L) = alpha_2^-1 + (5/3) alpha_1^-1 = x
    # Run to M_Z:  alpha_i^-1(M_Z) = alpha_i^-1(mu_L) + (b_i/2pi) L
    # alpha_em^-1(M_Z) = x + [(b2 + (5/3) b1)/2pi] L   ->  solve x from measured value
    coeff = (b2 + (5.0/3.0)*b1) / twopi
    x = inv_alpha_em_MZ - coeff * L
    inv_a2_MZ = x/4.0 + (b2/twopi)*L
    inv_a1_MZ = 0.45*x + (b1/twopi)*L
    inv_a3_MZ = x/4.0 + (b3/twopi)*L
    inv_aem_MZ = inv_a2_MZ + (5.0/3.0)*inv_a1_MZ        # == inv_alpha_em_MZ by constr.
    sin2_pred = inv_a2_MZ / inv_aem_MZ                   # sin^2 th_W(M_Z) prediction
    alpha_s_pred = 1.0/inv_a3_MZ if assume_g2_eq_g3 else None
    mZmW_pred = 1.0/math.sqrt(1.0 - sin2_pred)
    gV_eL_pred = -0.5 - 2*(-1)*sin2_pred                # T3 - 2 Q sin^2 (= 0 at 1/4)
    return {
        "label": label, "Ng": Ng, "NH": NH,
        "mu_L_GeV": mu_L, "L=ln(muL/MZ)": L,
        "b1": b1, "b2": b2, "b3": b3,
        "alpha_star_inv(muL)": x,
        "inv_alpha2(MZ)": inv_a2_MZ, "inv_alpha1(MZ)": inv_a1_MZ,
        "inv_alpha3(MZ)": inv_a3_MZ, "inv_alpha_em(MZ)": inv_aem_MZ,
        "sin2_thetaW(MZ)_pred": sin2_pred,
        "sin2_MSbar_meas": sin2_MZ_msbar,
        "sin2_onshell_meas": sin2_MZ_onshell,
        "resid_vs_MSbar_%": 100*(sin2_pred - sin2_MZ_msbar)/sin2_MZ_msbar,
        "resid_vs_onshell_%": 100*(sin2_pred - sin2_MZ_onshell)/sin2_MZ_onshell,
        "mZ/mW(MZ)_pred": mZmW_pred,
        "gV_eL(MZ)_pred": gV_eL_pred,
        "alpha_s(MZ)_pred[g2=g3]": alpha_s_pred,
        "alpha_s_meas": alpha_s_MZ_meas,
        "bare_sin2_gap_%": 100*(0.25 - sin2_MZ_msbar)/sin2_MZ_msbar,
    }

scenarios = [
    run_scenario(3, 1, "SM (3 gen, 1 Higgs doublet)"),
    run_scenario(3, 0, "Higgs-free (3 gen, model-correct)"),
]

# CM2b — the assumption-light, decisive question:
#   running UP from the *measured* M_Z boundary, at what scale mu* does the SM
#   trajectory pass through sin^2 th_W = 1/4 ?  (No reliance on the Planck anchor.)
def crossing_scale(Ng, NH):
    b1, b2, b3 = b_coeffs(Ng, NH)
    twopi = 2*math.pi
    inv_a2 = sin2_MZ_msbar * inv_alpha_em_MZ                      # 29.58
    inv_a1 = (inv_alpha_em_MZ - inv_a2) * 3.0/5.0                 # 59.02
    # sin^2=1/4  <=>  alpha_1^-1 = (9/5) alpha_2^-1.  Solve for t=ln(mu/MZ):
    #   inv_a1 - (b1/2pi) t = (9/5)[inv_a2 + (-b2/2pi)... ] careful with signs:
    # alpha_i^-1(mu) = inv_ai + (b_i/2pi) * t   (since d/dlnmu = -b/2pi, running UP
    #   means alpha^-1(mu)=alpha^-1(MZ) - (b/2pi)*(ln mu - ln MZ)?? -> use -b)
    # Standard: alpha_i^-1(mu) = alpha_i^-1(MZ) - (b_i/2pi) ln(mu/MZ).
    # Condition inv_a1(mu) = 1.8 inv_a2(mu):
    #   inv_a1 - (b1/2pi)t = 1.8 inv_a2 - 1.8 (b2/2pi) t
    num = inv_a1 - 1.8*inv_a2
    den = (b1/twopi) - 1.8*(b2/twopi)
    t = num/den
    mu_star = M_Z*math.exp(t)
    # verify all three observables coincide at mu* (they are algebraically locked):
    ia2 = inv_a2 - (b2/twopi)*t
    ia1 = inv_a1 - (b1/twopi)*t
    iaem = ia2 + (5.0/3.0)*ia1
    s2 = ia2/iaem
    return {"Ng": Ng, "NH": NH, "mu_star_GeV": mu_star, "t=ln(mu*/MZ)": t,
            "sin2_at_mu_star": s2, "mZ/mW_at_mu_star": 1/math.sqrt(1-s2),
            "gV_eL_at_mu_star": -0.5 + 2*s2}

crossings = [crossing_scale(3,1), crossing_scale(3,0)]
results["CM2"] = {
    "note": "boundary sin^2 th_W=1/4 at mu_L; magnitude fixed by alpha_em(M_Z); "
            "sin^2 th_W(M_Z), m_Z/m_W, g_V^{eL}, alpha_s predicted.",
    "scenarios": scenarios,
    "verdict_Planck_anchor": "one-loop running from the lattice (Planck) scale "
            "OVERSHOOTS: sin^2->0.06, alpha_s unphysical. The +12% gap is NOT a "
            "desert-running effect; running the bare angle the SU(5) way makes it worse.",
    "crossing_scale_measured_trajectory": crossings,
    "verdict_crossing": "the measured SM trajectory passes through sin^2=1/4 at a few "
            "TeV; the 12% gap is a low-scale matching offset, not 16 decades of running.",
}

# ----------------------------------------------------------------------
# CM3 — g_s from the rotor stiffness (F110 / F100 / F101)
# ----------------------------------------------------------------------
# F110 C7 matrix identity: one-plaquette KS rotor electric stiffness chi = 1/(4 g_s^2).
# The QCA rule's symmetric (E,B) rotation fixes chi = 1 (F101 §7).
# Hence the rule LOCKS the combination  g_s^2 * chi = 1/4  -> with chi=1, g_s = 1/2 (bare).
chi_rule = 1                       # symmetric (E,B) rotation normalization (F101)
gs2_chi  = F(1, 4)                 # the locked combination from chi = 1/(4 g_s^2)
gs_bare  = math.sqrt(float(gs2_chi / chi_rule))
# Cross-check: the same rotor's Gaussian string tension sigma_1 = 1/4 <1/Omega>_BZ.
# In the rule's own normalization the 2D value is sigma_1 = 0.2015 (F100 T2). The point
# is that Omega (the rule's rotation rate) is FIXED, so sigma_1 in lattice units is a
# pure number -> there is no free g_s left in the lattice string tension.
sigma1_2D_F100 = 0.2015
results["CM3"] = {
    "F110_identity": "chi = 1/(4 g_s^2)",
    "rule_normalization_chi": chi_rule,
    "locked_combination g_s^2*chi": str(gs2_chi),
    "g_s_bare(chi=1)": gs_bare,
    "sigma1_2D(F100, lattice units)": sigma1_2D_F100,
    "interpretation": "g_s is not independent: the rule's stiffness fixes g_s^2*chi=1/4. "
                      "Lattice sigma_1 = (1/4)<1/Omega>_BZ is a pure number (no free g_s).",
    "PASS": abs(gs_bare - 0.5) < 1e-15,
}

print(json.dumps(results, indent=2, default=str))

# ---- human-readable summary ----
print("\n" + "="*70)
print("CM1  EW reduction:  e=g/2,  g'=g/sqrt3,  g_Z=2g/sqrt3  -> ONE free magnitude")
print("="*70)
for s in scenarios:
    print(f"\nCM2  {s['label']}")
    print(f"   mu_L = {s['mu_L_GeV']:.3e} GeV,  L=ln(muL/MZ)={s['L=ln(muL/MZ)']:.3f}")
    print(f"   b1,b2,b3 = {s['b1']:.4f}, {s['b2']:.4f}, {s['b3']:.4f}")
    print(f"   sin^2 th_W(M_Z) predicted = {s['sin2_thetaW(MZ)_pred']:.5f}")
    print(f"      vs MS-bar 0.23122  ({s['resid_vs_MSbar_%']:+.2f}%)"
          f"   vs on-shell 0.22339 ({s['resid_vs_onshell_%']:+.2f}%)")
    print(f"      [bare 1/4 sits {s['bare_sin2_gap_%']:+.2f}% from MS-bar]")
    print(f"   m_Z/m_W(M_Z) predicted    = {s['mZ/mW(MZ)_pred']:.5f}  (PDG 1.1346)")
    print(f"   g_V^eL(M_Z) predicted     = {s['gV_eL(MZ)_pred']:+.5f}  (PDG ~ -0.038)")
    print(f"   alpha_s(M_Z)[g2=g3] pred  = {s['alpha_s(MZ)_pred[g2=g3]']:.4f}  (PDG 0.1179)")
print("\n" + "-"*70)
print("CM2b  measured SM trajectory: scale where sin^2 th_W = 1/4")
for c in crossings:
    tag = "SM" if c["NH"]==1 else "Higgs-free"
    print(f"   [{tag}]  mu* = {c['mu_star_GeV']:.3e} GeV "
          f"({c['mu_star_GeV']/1000:.2f} TeV);  sin^2(mu*)={c['sin2_at_mu_star']:.4f}"
          f"  m_Z/m_W={c['mZ/mW_at_mu_star']:.4f}  g_V^eL={c['gV_eL_at_mu_star']:+.4f}")
print("\n" + "="*70)
print(f"CM3  g_s bare (chi=1) = {results['CM3']['g_s_bare(chi=1)']:.4f}  "
      f"(locked combo g_s^2*chi = 1/4)")
print("="*70)
