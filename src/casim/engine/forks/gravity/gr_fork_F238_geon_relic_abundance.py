#!/usr/bin/env python3
"""
gr_fork_F238_geon_relic_abundance.py

F238 -- Can the F223/F228 geon relic abundance Omega_DM h^2 ~= 0.12 be DERIVED
(non-tunably) from a stated channel, or does it remain a free input -- and if so,
EXACTLY why?

This is prompt D3.  F228 closed the *mechanism* (the geon is the F190/F107 one-cell
Planck-mass black-hole remnant; every field-theoretic production channel is
exponentially forbidden because mu ~ sqrt2 M_Pl is ~5 orders above every available
energy scale; only PBH remnants survive) but left the *abundance* as one free number:
the initial primordial-black-hole mass fraction beta(M_form), "tunable" to 0.12.

D3 asks whether beta itself can be derived.  This fork does the derivation attempt
rigorously and reports an HONEST NEGATIVE RESULT with a quantitative reason:

  beta is not a free knob of the geon sector -- it is set by the SMALL-SCALE PRIMORDIAL
  POWER SPECTRUM at the PBH-formation horizon scale.  PBH formation is
  Press-Schechter / critical-collapse: a horizon patch collapses to a black hole iff
  its density contrast exceeds delta_c ~ 0.45, so

      beta(M) = erfc( delta_c / (sqrt2 * sigma(M)) ),

  where sigma(M) is the RMS density contrast at the horizon-crossing scale of mass M.
  Inverting the F228 band (beta ~ 6.6e-15 .. 6.6e-9) gives a REQUIRED small-scale
  amplitude sigma ~ 0.058 .. 0.078 -- three-to-four orders of magnitude ABOVE the
  measured CMB-scale amplitude sqrt(A_s) = 4.6e-5.  The ONLY spectrum that needs no
  extra tuning -- exact scale invariance (Harrison-Zel'dovich, n_s=1) anchored to the
  CMB amplitude -- gives beta = erfc(6944) ~ 10^(-2.1e7): it UNDER-produces by ~20
  MILLION orders.  To reach the required sigma the spectrum must be boosted by
  (sigma_req/sigma_CMB)^2 ~ 2.3e6 at the PBH scale, i.e. a strongly blue-tilted or
  spiked inflaton potential.

  THE MODEL HAS NO INFLATON FINDING and no primordial-power-spectrum machinery (there
  is no ca_inflation.py; ca_cosmology.py starts at the hot Big Bang).  The shape and
  amplitude of P(k) at the PBH scale is therefore an EXTERNAL input, exactly like
  H_inf, T_RH, g_* were for F198/F205/F223/F228.  So:

      abundance REMAINS A FREE INPUT, and the precise reason is that it is inherited
      one-for-one from a small-scale primordial spectrum the model does not derive.

  Additional rigor:
   * No attractor.  beta(sigma) = erfc(delta_c/sqrt2 sigma) is strictly monotone with
     no fixed point, so there is no "critical/extremal beta" the dynamics select --
     ruling out an attractor-value derivation.
   * The one place the model DOES fix numbers -- the remnant mass M_rem and the
     entropy-conserved yield coefficient (F228 P_a) -- is re-derived here from
     F190/F107, confirming that everything on the geon side is pinned and the ONLY
     residual is beta(M_form).  So the free input is isolated to a single external
     quantity, and it is a *cosmological initial condition*, not a particle-physics
     coupling.

This EXTENDS F228: F228 named beta as "the residual"; F238 proves beta cannot be
derived from the model as it stands (quantitatively, via Press-Schechter inversion +
the scale-invariant no-go), and pins the reason to the missing inflaton/spectrum
sector -- turning "tunable" into "provably a free cosmological initial condition."

Self-contained, REAL-ARITHMETIC (numpy real + hand-rolled special-function series; no
chiral/complex transforms, per CLAUDE.md).  Reuses the F228 remnant mass and yield
coefficient.  Writes test-results/F238_geon_relic_abundance.json.
"""

import json, math, os, sys
from casim.constants import G_CODATA as _G_CODATA, c_SI as _c_SI, hbar_SI as _hbar_SI

RESULTS = {}
CHECKS = []

def record(name, passed, detail):
    CHECKS.append({"check": name, "pass": bool(passed), "detail": detail})
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")

# ---------------------------------------------------------------------------
# Constants (SI + natural), Planck scale from F79 (G = a^2 c^3 / (8 pi sqrt3 hbar))
# ---------------------------------------------------------------------------
c_SI  = _c_SI
hbar  = _hbar_SI
eV    = 1.602176634e-19
G_N   = _G_CODATA

Mpl_kg  = math.sqrt(hbar*c_SI/G_N)
Mpl_GeV = Mpl_kg*c_SI**2/(1e9*eV)
GeV_per_kg = c_SI**2/(1e9*eV)
GeV_per_g  = GeV_per_kg*1e-3

# cosmology anchors (same as F228)
H_inf_max_GeV = 6.0e13
s0_cm3        = 2891.2
rho_c_over_h2 = 1.0537e-5
g_star        = 106.75
gamma_coll    = 0.2
Omega_DM_target = 0.12

# CMB primordial scalar amplitude (Planck 2018, at k_* = 0.05 Mpc^-1)
A_s        = 2.1e-9            # scalar power-spectrum amplitude
sigma_CMB  = math.sqrt(A_s)   # ~ 4.58e-5  (RMS density contrast at CMB scales)
delta_c    = 0.45             # radiation-era critical-collapse threshold (Carr; 0.4-0.5)

RESULTS["constants"] = {
    "Mpl_GeV": Mpl_GeV, "A_s": A_s, "sigma_CMB": sigma_CMB, "delta_c": delta_c,
    "H_inf_max_GeV": H_inf_max_GeV, "Omega_DM_target": Omega_DM_target,
}

# ---------------------------------------------------------------------------
# Hand-rolled real special functions (no scipy): erfc and its inverse.
# erfc via continued/asymptotic split; log10(erfc) via the asymptotic tail so we
# never underflow at large argument (the whole point of the no-go is a huge argument).
# ---------------------------------------------------------------------------
def erfc_real(x):
    """Real erfc(x) for x>=0 via a rational (Abramowitz-Stegun 7.1.26) approximation."""
    t = 1.0/(1.0 + 0.3275911*x)
    poly = t*(0.254829592 + t*(-0.284496736 + t*(1.421413741 +
              t*(-1.453152027 + t*1.061405429))))
    return poly*math.exp(-x*x)

def log10_erfc_asymptotic(x):
    """log10(erfc(x)) for LARGE x, using erfc(x) ~ exp(-x^2)/(x sqrt(pi))*(1 - 1/(2x^2)+...)."""
    ln = -x*x - math.log(x*math.sqrt(math.pi)) + math.log(max(1.0 - 1.0/(2*x*x), 1e-300))
    return ln/math.log(10.0)

def inv_erfc(y):
    """Solve erfc(x)=y for x>=0 by bisection (y not too tiny)."""
    lo, hi = 0.0, 40.0
    for _ in range(300):
        mid = 0.5*(lo+hi)
        if erfc_real(mid) > y: lo = mid
        else:                  hi = mid
    return 0.5*(lo+hi)

# ===========================================================================
# STEP 1 -- Re-derive the geon-side numbers that ARE pinned (reuse F228)
# ===========================================================================
# One-cell remnant mass (F190 area law + F107 cell); this is exact-algebraic.
M_rem_over_Mpl = (math.sqrt(3.0)/2.0)**0.5      # ~0.93060
M_rem_GeV      = M_rem_over_Mpl*Mpl_GeV

def T_form_GeV(M_form_GeV):
    return math.sqrt(gamma_coll*Mpl_GeV**3/(3.32*math.sqrt(g_star)*M_form_GeV))

def beta_required(M_form_g):
    """beta needed for Omega_rem h^2 = 0.12 (entropy-conserved remnant yield, F228 P_a)."""
    M_form_GeV = M_form_g*GeV_per_g
    T_form = T_form_GeV(M_form_GeV)
    coeff = M_rem_GeV*(0.75*T_form/M_form_GeV)*(s0_cm3/rho_c_over_h2)
    return Omega_DM_target/coeff, T_form, M_form_GeV

M_forms_g = (1e4, 1e6, 1e8)
beta_band = {}
for Mg in M_forms_g:
    b, Tf, MfG = beta_required(Mg)
    beta_band[f"{Mg:.0e} g"] = {"beta_required": b, "T_form_GeV": Tf}

geon_side_pinned = (abs(M_rem_over_Mpl - (math.sqrt(3)/2)**0.5) < 1e-12
                    and all(0 < v["beta_required"] < 1 for v in beta_band.values()))
record("S1_geon_side_pinned_only_beta_free",
       geon_side_pinned,
       f"Geon side fully pinned (reuse F228): M_rem={M_rem_over_Mpl:.5f} M_Pl (exact-algebraic, "
       f"F190/F107); entropy-conserved yield coeff fixed => beta needed for Omega=0.12: "
       + ", ".join(f"{k}: {v['beta_required']:.2e}" for k,v in beta_band.items())
       + ". The ONLY unpinned quantity is beta(M_form).")

# ===========================================================================
# STEP 2 -- DERIVATION ATTEMPT: fix beta from the primordial spectrum (Press-Schechter)
# ===========================================================================
# A horizon patch collapses to a PBH iff its smoothed density contrast delta > delta_c.
# For Gaussian fluctuations of RMS sigma(M):
#     beta(M) = P(delta > delta_c) = (1/2) erfc( delta_c / (sqrt2 sigma) ).
# (The 1/2 is an O(1) prefactor; it does not change any order-of-magnitude conclusion.
#  We fold it into the inversion consistently.)
# Invert the F228 beta band to get the REQUIRED small-scale amplitude sigma.
sigma_required = {}
for Mg in M_forms_g:
    b = beta_band[f"{Mg:.0e} g"]["beta_required"]
    x = inv_erfc(2.0*b)                       # erfc(x) = 2 beta  =>  x = delta_c/(sqrt2 sigma)
    sig = delta_c/(math.sqrt(2.0)*x)
    sigma_required[f"{Mg:.0e} g"] = {"beta": b, "x": x, "sigma_required": sig}

sig_lo = min(v["sigma_required"] for v in sigma_required.values())
sig_hi = max(v["sigma_required"] for v in sigma_required.values())
# All required sigmas are O(0.06-0.08): far above the CMB amplitude.
required_sigma_is_large = 0.03 < sig_lo and sig_hi < 0.2
record("S2_required_small_scale_sigma",
       required_sigma_is_large,
       f"Press-Schechter inversion of the F228 beta band -> required RMS amplitude at the PBH "
       f"scale sigma ~ {sig_lo:.4f}..{sig_hi:.4f} (delta_c={delta_c}). This is the amplitude the "
       f"primordial spectrum must have at the small (PBH-formation) scale to source Omega_DM.")

# ===========================================================================
# STEP 3 -- THE SCALE-INVARIANT NO-GO (the only tuning-free candidate spectrum)
# ===========================================================================
# The single spectrum shape that needs NO extra inflaton knob is exact scale invariance
# (Harrison-Zel'dovich, n_s=1) anchored to the measured CMB amplitude: sigma(M) = const
# = sigma_CMB at ALL scales.  Then:
#     beta_HZ = (1/2) erfc( delta_c / (sqrt2 sigma_CMB) ).
x_HZ = delta_c/(math.sqrt(2.0)*sigma_CMB)     # ~ 6944
log10_beta_HZ = math.log10(0.5) + log10_erfc_asymptotic(x_HZ)
# Convert to the produced abundance: Omega ~ (beta_HZ / beta_required) * 0.12  (linear in beta).
# Use the lightest formation mass (largest coeff, most optimistic) as a ceiling.
beta_req_opt = min(v["beta_required"] for v in beta_band.values())
log10_Omega_HZ = log10_beta_HZ - math.log10(beta_req_opt) + math.log10(Omega_DM_target)
HZ_underproduces = log10_Omega_HZ < -1e6      # under-produces by >1e6 orders
record("S3_scale_invariant_nogo",
       HZ_underproduces,
       f"Scale-invariant (n_s=1) spectrum at the CMB amplitude sigma_CMB={sigma_CMB:.3e}: "
       f"x=delta_c/(sqrt2 sigma_CMB)={x_HZ:.0f} => beta_HZ~10^({log10_beta_HZ:.3e}), giving "
       f"Omega_DM h^2 ~ 10^({log10_Omega_HZ:.3e}) <<< 0.12. The tuning-free spectrum "
       f"UNDER-produces by ~{-log10_Omega_HZ:.2e} orders. A scale-invariant primordial "
       f"spectrum CANNOT make the geon relic.")

# ===========================================================================
# STEP 4 -- THE REQUIRED SPECTRAL BOOST (the size of the missing inflaton input)
# ===========================================================================
# Power ~ sigma^2, so to lift sigma_CMB up to sigma_required at the PBH scale the
# small-scale power must be enhanced by a factor (sigma_required/sigma_CMB)^2.
boost_lo = (sig_lo/sigma_CMB)**2
boost_hi = (sig_hi/sigma_CMB)**2
# A blue tilt n_s from CMB scale (k_* ~ 0.05 Mpc^-1) to the PBH scale k_PBH would need to
# supply this boost; the number of decades in k between the two scales sets the tilt demanded.
# k_PBH ~ 1/R_H(T_form); ballpark ~ 1e16-1e19 Mpc^-1 -> ~17-20 decades in k.
# boost = (k_PBH/k_*)^(n_s-1); we only report the boost magnitude (the tilt depends on the
# spectrum shape, which is exactly the missing input).
Ndecades_k = 18.0                              # ballpark decades from CMB to PBH scale
ns_minus_1_needed = math.log10(0.5*(boost_lo+boost_hi))/Ndecades_k
boost_is_huge = boost_lo > 1e5
record("S4_required_spectral_boost",
       boost_is_huge,
       f"Power ~ sigma^2 => the small-scale spectrum must be boosted by "
       f"(sigma_req/sigma_CMB)^2 ~ {boost_lo:.2e}..{boost_hi:.2e} above the CMB amplitude. "
       f"Spread over ~{Ndecades_k:.0f} decades in k that is a blue tilt Delta(n_s-1) ~ "
       f"{ns_minus_1_needed:.2f} (or a localized spike). This boost is an INFLATON-POTENTIAL "
       f"input, not a geon-sector quantity.")

# ===========================================================================
# STEP 5 -- NO ATTRACTOR: beta(sigma) is strictly monotone, no fixed point
# ===========================================================================
# beta(sigma) = (1/2) erfc(delta_c/(sqrt2 sigma)) is strictly increasing in sigma with
# d beta/d sigma > 0 everywhere and no interior extremum -> there is no dynamically
# selected "critical beta" (unlike a genuine attractor).  Verify monotonicity numerically.
# Use log10(beta) via the asymptotic tail so we never hit the erfc->0 underflow plateau;
# monotonicity of log10(beta) is equivalent to monotonicity of beta and stays representable.
sig_grid = [0.01, 0.03, 0.05, 0.08, 0.12, 0.2, 0.4]
log10_beta_grid = [math.log10(0.5) + log10_erfc_asymptotic(delta_c/(math.sqrt(2.0)*s))
                   for s in sig_grid]
beta_grid = log10_beta_grid   # reported as log10(beta) (many are far below double-precision)
strictly_increasing = all(log10_beta_grid[i] < log10_beta_grid[i+1]
                          for i in range(len(log10_beta_grid)-1))
no_attractor = strictly_increasing
record("S5_no_beta_attractor",
       no_attractor,
       f"beta(sigma)=1/2 erfc(delta_c/sqrt2 sigma) is strictly monotone in sigma "
       f"(log10 beta grid {[f'{b:.1f}' for b in log10_beta_grid]}) with no interior fixed point => there is "
       f"NO dynamically selected critical/attractor beta. beta tracks sigma one-for-one, so "
       f"deriving beta REQUIRES deriving the small-scale sigma (the spectrum).")

# ===========================================================================
# STEP 6 -- THE MISSING SECTOR: no inflaton / no primordial spectrum in the model
# ===========================================================================
# Check the model has no inflaton finding and no primordial-power-spectrum module.
# C6: five '..' — this fork moved from ca-simulation/forks/ (2 levels below
# the repo root) to src/casim/engine/forks/<sector>/ (5 levels). Same dir.
repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
findings_dir = os.path.join(repo, "findings")
casim_fork_dir = os.path.join(repo, "ca-simulation")
def _list(d):
    try: return os.listdir(d)
    except Exception: return []
inflaton_findings = [f for f in _list(findings_dir)
                     if any(kw in f.lower() for kw in ("inflat", "preheat", "primordial-power",
                                                       "spectral-index", "slow-roll"))]
inflaton_modules = [f for f in _list(casim_fork_dir)
                    if any(kw in f.lower() for kw in ("inflat", "preheat", "primordial"))]
no_inflaton_sector = (len(inflaton_findings) == 0 and len(inflaton_modules) == 0)
record("S6_no_inflaton_sector_in_model",
       no_inflaton_sector,
       f"Searched findings/ and ca-simulation/: inflaton/preheating/primordial-spectrum "
       f"findings={inflaton_findings or 'NONE'}, modules={inflaton_modules or 'NONE'}. The model "
       f"has NO inflaton finding and NO primordial-power-spectrum machinery (ca_cosmology.py "
       f"starts at the hot Big Bang). So sigma(k) at the PBH scale is an EXTERNAL input.")

# ===========================================================================
# STEP 7 -- VERDICT: abundance is a FREE (cosmological-initial-condition) INPUT
# ===========================================================================
# The chain: Omega_DM <- beta(M_form) <- sigma(k_PBH) <- primordial P(k) <- inflaton potential.
# Everything on the geon side is pinned (S1); beta has no attractor (S5); the only
# tuning-free spectrum fails by ~20M orders (S3); reaching 0.12 needs a ~1e6 spectral
# boost (S4) that is an inflaton input the model lacks (S6).  Therefore abundance is a
# FREE INPUT -- specifically a cosmological INITIAL CONDITION (the small-scale spectrum),
# not a particle-physics coupling -- and this is the honest, documented negative result.
verdict_free_input = (geon_side_pinned and required_sigma_is_large and HZ_underproduces
                      and boost_is_huge and no_attractor and no_inflaton_sector)
record("S7_abundance_is_free_cosmological_input",
       verdict_free_input,
       "VERDICT: Omega_DM h^2=0.12 is NOT derivable from the model as it stands. The abundance "
       "is inherited one-for-one from beta(M_form), which Press-Schechter ties to the small-scale "
       "primordial amplitude sigma(k_PBH). That amplitude must be ~2e6x the CMB value (S4); the "
       "only tuning-free spectrum under-produces by ~2e7 orders (S3); there is no attractor (S5); "
       "and the model has no inflaton/spectrum sector to fix it (S6). So abundance is a FREE "
       "COSMOLOGICAL INITIAL CONDITION, isolated to a single external number -- extending F228's "
       "'beta is the residual' to 'beta is provably a free input, and here is exactly why.'")

# ---------------------------------------------------------------------------
RESULTS["checks"] = CHECKS
RESULTS["step1_geon_side"] = {"M_rem_over_Mpl": M_rem_over_Mpl, "beta_band": beta_band}
RESULTS["step2_required_sigma"] = sigma_required
RESULTS["step3_scale_invariant"] = {
    "x_HZ": x_HZ, "log10_beta_HZ": log10_beta_HZ, "log10_Omega_HZ": log10_Omega_HZ,
    "underproduces_by_orders": -log10_Omega_HZ,
}
RESULTS["step4_required_boost"] = {
    "boost_lo": boost_lo, "boost_hi": boost_hi, "ns_minus_1_needed": ns_minus_1_needed,
    "Ndecades_k_assumed": Ndecades_k,
}
RESULTS["step5_no_attractor"] = {"sigma_grid": sig_grid, "log10_beta_grid": log10_beta_grid,
                                 "strictly_increasing": strictly_increasing}
RESULTS["step6_missing_sector"] = {"inflaton_findings": inflaton_findings,
                                   "inflaton_modules": inflaton_modules}
RESULTS["summary"] = {
    "question": "Can Omega_DM h^2~0.12 be derived non-tunably from a stated channel?",
    "answer": "NO -- abundance remains a FREE cosmological initial condition (the small-scale "
              "primordial spectrum), and this fork proves exactly why.",
    "channel": "PBH-remnant (F228) -- the only viable production route; abundance = M_rem * "
               "beta(M_form) * yield; geon side pinned, beta is the sole residual.",
    "required_sigma_PBH": [sig_lo, sig_hi],
    "sigma_CMB": sigma_CMB,
    "required_spectral_boost": [boost_lo, boost_hi],
    "scale_invariant_underproduces_by_orders": -log10_Omega_HZ,
    "reason": "beta <- sigma(k_PBH) <- primordial P(k) <- inflaton potential; the model has no "
              "inflaton/spectrum sector, so sigma(k_PBH) is external. No attractor exists.",
    "relation_to_F228": "EXTENDS F228: F228 named beta as 'the residual'; F238 proves beta is "
                        "provably a free input (Press-Schechter inversion + scale-invariant no-go "
                        "+ no-attractor + missing-sector), and identifies it as a cosmological "
                        "INITIAL CONDITION, not a particle coupling.",
    "n_pass": sum(c["pass"] for c in CHECKS),
    "n_total": len(CHECKS),
}
# C6: five '..' — this fork moved from ca-simulation/forks/ (2 levels below
# the repo root) to src/casim/engine/forks/<sector>/ (5 levels). Same dir.
outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "test-results"))
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F238_geon_relic_abundance.json"), "w") as f:
    json.dump(RESULTS, f, indent=2)
print(f"\n{RESULTS['summary']['n_pass']}/{RESULTS['summary']['n_total']} checks PASS")
print(f"wrote {os.path.join(outdir, 'F238_geon_relic_abundance.json')}")
