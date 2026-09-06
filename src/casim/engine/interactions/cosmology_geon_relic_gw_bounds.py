#!/usr/bin/env python3
"""
casim.engine.interactions.cosmology_geon_relic_gw_bounds

F365 -- literature-comparison sharpening of rubric row K7 (dark-matter identity).
Places the F228/F238 graviton-graviton J=2 geon / one-cell Planck-mass black-hole
remnant (M_rem = (sqrt3/2)^(1/2) M_Pl ~= 0.9306 M_Pl, F228 Sec.2) against TWO
external, previously-unchecked 2025 gravitational-wave constraint papers on
exactly this scenario (ultralight-PBH-forms-a-Planck-mass-relic dark matter):

  [DLS/PVL]  Domenech-Lin-Sasaki and Papanikolaou-Vennin-Langlois scalar-induced-GW
             bounds on the initial PBH collapse fraction beta_i(M_form), as compiled
             in Cheek, Ghoshal, Heurtier (arXiv:2506.16154, "Comprehensively
             Constraining Ultra-Light Primordial Black Holes Through Relic Formation
             and Early Mergers"), Eqs. 2.3 (beta_relic,i required for f_PBH=1),
             2.6 (PVL bound), 2.8 (DLS bound).
  [LIGO-PSR] arXiv:2509.20533 ("Gaussian Planck Relics are Ruled-Out as Dark Matter
             by LIGO"): if the small-scale curvature power spectrum P_R that seeds
             the relic-forming PBHs is GAUSSIAN, the accompanying second-order
             scalar-induced GW background exceeds the LIGO O3 stochastic bound
             Omega_GW <~ 5e-9 by 1-3 orders of magnitude for the P_R~1e-2..1e-1
             needed; only non-Gaussian statistics evade this.

This module does NOT re-derive new model physics -- it (a) reproduces F228's own
beta_required(M_form) formula (Sec.4, P_a) and F238's own sigma_req(M_form)
Press-Schechter inversion (Sec.3) so both can be compared numerically against the
external formulas above, and (b) locates the crossover mass at which F228's own
worked examples (M_form in {1e4,1e6,1e8} g) start failing the external bound.
Root-finding is a hand-rolled bisection (both sides are used only through `math`;
no numpy/scipy needed for a monotone 1-D scalar solve, per D8 -- this keeps the
sensitive comparison in plain, auditable arithmetic).

RESULT IN ONE LINE
-------------------------------------------------------------------------------
F228's own beta_required(M_form) formula agrees with the external eq-2.3 literature
formula to a CONSTANT factor 11.68 across all three M_form examples -- EXPECTED,
since both share the same M^1.5 scaling by construction, so the ratio is
guaranteed constant; the informative content is only that the two independent
O(1) normalisations differ by ~12x, itself unremarkable at F228's declared
order-of-magnitude tier. Combining eq-2.3 with the external DLS bound gives an
order-of-magnitude ceiling M_form <~ 1.6e8 g -- so F228's own M_form=1e8 g example
is now marginal (2.9x from the ceiling), not a safely-viable illustration -- BUT
the DLS bound itself is stated by its source (2506.16154) to assume a
monochromatic PBH mass function that "may not reflect a realistic physical
scenario," and to be weakened by early mergers, so this ceiling is an
order-of-magnitude placement, not a hard exclusion. F238's own sigma_req(M_form)
~0.058-0.079 converts, via the GENERAL integral transfer relation (2509.20533's
own Eq.9, sigma^2=(16/81) integral ... W^2 P_R, giving P_R=(81/16) sigma^2), to
P_R~0.017-0.032, inside the P_R~1e-2..1e-1 band that paper's Gaussian-statistics
LIGO-O3 exclusion occupies -- BUT recomputing with that SAME PAPER's own
narrow-bump approximation (its Eq.10, sigma^2=(4/9) P_R, i.e. P_R=(9/4) sigma^2 --
the formula it actually uses for its own headline number) instead gives
P_R~0.0077-0.0141, which puts two of the three points BELOW the band's stated
lower edge. The two conventions disagree on which side of the band edge the
result falls, so this piece is reported as a same-order-of-magnitude
PLAUSIBILITY placement (exactness: bracketed), not a quantitative hit -- see
Sec.5-6 of F365 and its Reviewed & corrected note. Net effect on K7 (unchanged
from the original claim): the candidate's abundance mechanism carries a named,
checkable escape clause (non-Gaussianity of whatever sources the relic-forming
perturbations) rather than being merely "a free input" -- but the strength of
that specific argument is convention-sensitive and flagged as such, while the
formation-mass ceiling (S3/S4) is the more robust of the two results.
"""
import math

# ===========================================================================
# Reproduced from F228 Sec.4 (P_a) -- SAME formula, SAME constants, cited not
# re-derived, so the comparison below is honestly "F228's number vs the
# literature's number", not two independently-invented estimates.
# ===========================================================================
Mpl_GeV       = 1.220890e19          # non-reduced Planck mass, F79/F107 convention
GeV_per_g     = 5.60958865e23        # 1 g -> GeV/c^2
s0_cm3        = 2891.2               # present entropy density, cm^-3
rho_c_over_h2 = 1.0537e-5            # critical density / h^2, GeV cm^-3
g_star        = 106.75               # relativistic dof at high T (SM)
gamma_coll    = 0.2                  # PBH collapse efficiency (radiation-era)
Omega_DM_target = 0.12
M_rem_over_Mpl = (math.sqrt(3.0)/2.0)**0.5     # ~0.93060, F228 Sec.2, exact-algebraic
M_rem_GeV      = M_rem_over_Mpl*Mpl_GeV

def T_form_GeV(M_form_GeV):
    """F228 Sec.4: M_form = gamma*M_Pl^3/(3.32 sqrt(g_*) T^2)."""
    return math.sqrt(gamma_coll*Mpl_GeV**3/(3.32*math.sqrt(g_star)*M_form_GeV))

def beta_required_F228(M_form_g):
    """F228 Sec.4 (P_a): beta(M_form) for Omega_rem h^2 = Omega_DM_target."""
    M_form_GeV = M_form_g*GeV_per_g
    Tf = T_form_GeV(M_form_GeV)
    coeff = M_rem_GeV*(0.75*Tf/M_form_GeV)*(s0_cm3/rho_c_over_h2)
    return Omega_DM_target/coeff

# ===========================================================================
# External literature formulas (2506.16154, Cheek-Ghoshal-Heurtier 2025).
# Hard-coded, cited, NOT registered as model constants (D7 registers physical
# constants of the model; these are external comparison inputs, same practice
# as F238's plain Planck-2018 literals).
# ===========================================================================
def beta_relic_required_eq2p3(M_form_g, f_pbh=1.0):
    """arXiv:2506.16154 Eq. 2.3: beta_relic,i ~= 5.65e-22 (M_form/g)^1.5 f_PBH."""
    return 5.65e-22*(M_form_g**1.5)*f_pbh

def beta_bound_PVL_eq2p6(M_form_g):
    """arXiv:2506.16154 Eq. 2.6 (Papanikolaou-Vennin-Langlois GW bound)."""
    return 1.4e-4*(M_form_g/1e9)**(-0.25)

def beta_bound_DLS_eq2p8(M_form_g):
    """arXiv:2506.16154 Eq. 2.8 (Domenech-Lin-Sasaki GW bound)."""
    return 1.1e-6*(M_form_g/1e4)**(-17.0/24.0)

def _bisect_log10_crossover(f, lo_log10, hi_log10, iters=200):
    """Hand-rolled bisection for log10(M) where f(M) changes sign (no scipy, D8)."""
    flo = f(10.0**lo_log10)
    for _ in range(iters):
        mid = 0.5*(lo_log10+hi_log10)
        fm = f(10.0**mid)
        if (fm > 0) == (flo > 0):
            lo_log10 = mid
        else:
            hi_log10 = mid
    return 10.0**(0.5*(lo_log10+hi_log10))

def M_ceiling_DLS_g():
    """Largest M_form (g) where beta_relic_required_eq2p3 <= beta_bound_DLS_eq2p8."""
    f = lambda M: beta_relic_required_eq2p3(M) - beta_bound_DLS_eq2p8(M)
    return _bisect_log10_crossover(f, 4.0, 12.0)

def M_ceiling_PVL_g():
    f = lambda M: beta_relic_required_eq2p3(M) - beta_bound_PVL_eq2p6(M)
    return _bisect_log10_crossover(f, 4.0, 16.0)

# ===========================================================================
# Reproduced from F238 Sec.3 -- Press-Schechter inversion sigma_req(beta).
# ===========================================================================
DELTA_C = 0.45   # F238 Sec.3, critical-collapse threshold (Carr 1975 range 0.4-0.5)
A_S_PLANCK2018 = 2.1e-9   # Planck 2018 CMB-scale amplitude, cited by F238

def beta_of_sigma(sigma, delta_c=DELTA_C):
    return 0.5*math.erfc(delta_c/(math.sqrt(2.0)*sigma))

def sigma_req(beta_target, delta_c=DELTA_C, lo=1e-4, hi=1.0, iters=200):
    """Hand-rolled bisection inverse of beta_of_sigma (monotone increasing in sigma)."""
    flo = beta_of_sigma(lo, delta_c) - beta_target
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        fm = beta_of_sigma(mid, delta_c) - beta_target
        if (fm > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return 0.5*(lo+hi)

def P_R_from_sigma_general(sigma):
    """arXiv:2509.20533 Eq.9, the GENERAL integral relation in its narrow-window limit:
    sigma^2 = (16/81) P_R(k)  =>  P_R = (81/16) sigma^2. This is the generic
    horizon-crossing transfer relation (O(1) factors vary by window-function choice)."""
    return (81.0/16.0)*sigma*sigma

def P_R_from_sigma_narrowbump(sigma):
    """arXiv:2509.20533 Eq.10, the paper's OWN narrow-bump approximation -- the formula
    it actually uses to compute its own headline P_R(k_c) from its own required sigma:
    sigma^2(R_H) ~= (4/9) P_R(k_c)  =>  P_R = (9/4) sigma^2. Included because review-
    finding attack 6 (F365) found the general-integral coefficient (81/16, factor 5.06)
    and this paper's own headline coefficient (9/4, factor 2.25) disagree by ~2.25x --
    enough to move some of F238's sigma_req points across the LIGO-excluded band's
    stated edge. Reporting BOTH conventions rather than picking one is the honest
    resolution; see run_all() S6 and F365 Sec.5-6."""
    return (9.0/4.0)*sigma*sigma

# ===========================================================================
# Battery
# ===========================================================================
_records = []
def record(name, passed, detail):
    _records.append({"name": name, "passed": bool(passed), "detail": detail})

M_FORM_EXAMPLES_G = (1e4, 1e6, 1e8)

def run_all():
    _records.clear()

    # S1 -- reproduce F228's own beta_required at its three worked examples,
    # confirm the transcription is faithful (self-check against F228 Sec.4's
    # stated values 6.6e-15, 6.6e-12, 6.6e-9).
    f228_stated = {1e4: 6.6e-15, 1e6: 6.6e-12, 1e8: 6.6e-9}
    s1_ok = True
    s1_detail = {}
    for Mg, stated in f228_stated.items():
        computed = beta_required_F228(Mg)
        rel = abs(computed-stated)/stated
        s1_detail[f"{Mg:.0e}"] = {"computed": computed, "stated": stated, "rel_err": rel}
        s1_ok = s1_ok and (rel < 0.05)
    record("S1_reproduce_F228_beta_required", s1_ok,
           f"F228 Sec.4 beta_required(M_form) reproduced from its own stated formula/"
           f"constants to <5% at all 3 worked examples: {s1_detail}")

    # S2 -- cross-check F228's beta_required against the external eq-2.3 formula:
    # same M^1.5 scaling, constant ratio across all three masses.
    ratios = [beta_required_F228(Mg)/beta_relic_required_eq2p3(Mg) for Mg in M_FORM_EXAMPLES_G]
    ratio_spread = (max(ratios)-min(ratios))/min(ratios)
    s2_ok = ratio_spread < 1e-3     # same power law => ratio should be a near-exact constant
    record("S2_cross_check_vs_eq2p3", s2_ok,
           f"F228/eq2.3 ratio at M_form={M_FORM_EXAMPLES_G} g: {[round(r,4) for r in ratios]} "
           f"(constant to {ratio_spread:.2e} relative spread). NOTE (review-finding attack 2): "
           f"the constant ratio is EXPECTED, not a discovery -- both formulas share the same "
           f"M^1.5 scaling by construction (entropy-conserved comoving relic number), so any "
           f"two such formulas give an exactly-constant ratio regardless of whether their O(1) "
           f"normalisations agree. The only informative content is that mean ratio "
           f"{sum(ratios)/len(ratios):.3f} -- i.e. the two independently-chosen O(1) "
           f"normalisations (F228's gamma_coll/g_star convention vs eq2.3's) differ by only "
           f"~12x, unremarkable at F228's own declared order-of-magnitude tier. This is a mild, "
           f"not a strong, cross-check.")

    # S3 -- formation-mass ceiling from the external DLS/PVL GW bounds (using the
    # external eq-2.3 required-beta, since that is the formula the bounds were
    # derived to be compared against).
    M_ceil_dls = M_ceiling_DLS_g()
    M_ceil_pvl = M_ceiling_PVL_g()
    tighter = min(M_ceil_dls, M_ceil_pvl)
    s3_ok = (1e7 < M_ceil_dls < 1e9) and (M_ceil_pvl > M_ceil_dls)
    record("S3_formation_mass_ceiling", s3_ok,
           f"DLS crossover M_form={M_ceil_dls:.3e} g; PVL crossover M_form={M_ceil_pvl:.3e} g "
           f"-- DLS is the tighter bound across this range, consistent with 2506.16154's own "
           f"statement that DLS dominates PVL for M_form below ~1e9 g. Order-of-magnitude "
           f"ceiling: M_form <~ {tighter:.1e} g. CAVEAT (review-finding attack 6): 2506.16154 "
           f"itself states the DLS bound assumes a MONOCHROMATIC PBH mass function that 'may "
           f"not reflect a realistic physical scenario,' and that early PBH mergers may weaken "
           f"it -- so this is an order-of-magnitude placement against a bound that is itself "
           f"model-dependent, not an unconditional exclusion.")

    # S4 -- F228's own M_form=1e8 g worked example against that ceiling.
    req_1e8 = beta_relic_required_eq2p3(1e8)
    bound_1e8 = beta_bound_DLS_eq2p8(1e8)
    margin = bound_1e8/req_1e8
    s4_ok = margin > 1.0    # still (marginally) allowed, not yet excluded
    record("S4_F228_1e8g_example_status", s4_ok,
           f"At F228's own M_form=1e8 g example: eq2.3-required beta={req_1e8:.3e} vs "
           f"DLS bound={bound_1e8:.3e} -- margin factor {margin:.2f}x. Allowed but marginal "
           f"(within a factor {margin:.1f} of the DLS ceiling), NOT a safely-interior "
           f"illustration as F228 Sec.4's table implied; M_form=1e4 g and 1e6 g remain "
           f"comfortably interior (margins {beta_bound_DLS_eq2p8(1e4)/beta_relic_required_eq2p3(1e4):.1e}x "
           f"and {beta_bound_DLS_eq2p8(1e6)/beta_relic_required_eq2p3(1e6):.1e}x).")

    # S5 -- reproduce F238's own sigma_req(M_form), self-check against its stated values.
    f238_stated_sigma = {1e4: 0.058, 1e6: 0.066, 1e8: 0.079}
    s5_ok = True
    s5_detail = {}
    for Mg, stated_sigma in f238_stated_sigma.items():
        beta_t = beta_required_F228(Mg)
        computed_sigma = sigma_req(beta_t)
        rel = abs(computed_sigma-stated_sigma)/stated_sigma
        s5_detail[f"{Mg:.0e}"] = {"computed": computed_sigma, "stated": stated_sigma, "rel_err": rel}
        s5_ok = s5_ok and (rel < 0.02)
    record("S5_reproduce_F238_sigma_req", s5_ok,
           f"F238 Sec.3 sigma_req(M_form) (Press-Schechter inversion at delta_c={DELTA_C}) "
           f"reproduced from F228's own beta_required to <2% at all 3 examples: {s5_detail}")

    # S6 -- convert F238's own sigma_req to P_R under BOTH conventions found in the
    # external paper (its general Eq.9 integral relation, and its own Eq.10 narrow-bump
    # approximation -- the one it actually uses for its headline number) and compare
    # against the LIGO-Gaussian-exclusion band (arXiv:2509.20533, P_R~1e-2..1e-1).
    # review-finding attack 6 found these two conventions disagree by 2.25x, enough to
    # move 2 of 3 points across the band's stated lower edge -- so this check reports
    # BOTH numbers and grades on "same order of magnitude, straddling the band," not
    # "inside the band," and is exactness: bracketed (not quantitative) for that reason.
    LIGO_PR_LO, LIGO_PR_HI = 1e-2, 1e-1
    pr_general, pr_narrowbump = {}, {}
    for Mg in M_FORM_EXAMPLES_G:
        beta_t = beta_required_F228(Mg)
        sig = sigma_req(beta_t)
        pr_general[f"{Mg:.0e}"] = P_R_from_sigma_general(sig)
        pr_narrowbump[f"{Mg:.0e}"] = P_R_from_sigma_narrowbump(sig)
    # pass criterion: same-order-of-magnitude straddle, not "inside the band" --
    # both conventions must land within one order of magnitude of the band on
    # EITHER side (a bracketed placement, not a quantitative hit).
    lo_check = LIGO_PR_LO/10.0
    hi_check = LIGO_PR_HI*10.0
    all_bracketed = all(lo_check <= v <= hi_check for v in list(pr_general.values())+list(pr_narrowbump.values()))
    n_general_in_band = sum(1 for v in pr_general.values() if LIGO_PR_LO <= v <= LIGO_PR_HI)
    n_narrowbump_in_band = sum(1 for v in pr_narrowbump.values() if LIGO_PR_LO <= v <= LIGO_PR_HI)
    record("S6_gaussianity_requirement", all_bracketed,
           f"P_R at M_form={M_FORM_EXAMPLES_G} g -- general-integral convention (Eq.9, "
           f"P_R=(81/16)sigma^2): {[round(v,4) for v in pr_general.values()]} "
           f"({n_general_in_band}/3 inside the stated band); THIS PAPER'S OWN narrow-bump "
           f"convention (Eq.10, P_R=(9/4)sigma^2 -- what it uses for its own headline "
           f"number): {[round(v,4) for v in pr_narrowbump.values()]} "
           f"({n_narrowbump_in_band}/3 inside the stated band). The two conventions "
           f"disagree on which side of the arXiv:2509.20533 P_R~[{LIGO_PR_LO},{LIGO_PR_HI}] "
           f"LIGO-O3-Gaussian-exclusion band edge the result falls (review-finding attack 6, "
           f"2026-09-04) -- so this is graded on 'same order of magnitude as the excluded "
           f"band' (bracketed), not 'inside the band' (quantitative). EXACTNESS: bracketed. "
           f"Also (attack 5): because sigma_req=erfc^-1 compresses ~20 orders of magnitude "
           f"in beta into O(1) range in sigma, landing near this band is not a sharp "
           f"coincidence -- most sub-dominant beta values would land somewhere in a similar "
           f"range. This is reported as a same-regime PLAUSIBILITY argument, not a "
           f"from-first-principles exclusion (see Sec.5-6 of F365 and its Reviewed & "
           f"corrected note).")

    passed = sum(1 for r in _records if r["passed"])
    total = len(_records)
    return {
        "records": _records,
        "passed": passed,
        "total": total,
        "all_pass": passed == total,
        "M_ceiling_DLS_g": M_ceil_dls,
        "M_ceiling_PVL_g": M_ceil_pvl,
        "M_rem_over_Mpl": M_rem_over_Mpl,
        "M_rem_GeV": M_rem_GeV,
    }

if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path
    out = run_all()
    for r in out["records"]:
        print(("PASS " if r["passed"] else "FAIL "), r["name"])
        print("   ", r["detail"][:400])
    print(f"\n{out['passed']}/{out['total']} PASS")
    with open(results_path("F365_geon_relic_gw_bounds.json"), "w") as fh:
        json.dump(out, fh, indent=2)
