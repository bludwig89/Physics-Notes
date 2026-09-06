"""Strong sector — the QCD anchor, the IR coupling bracket, the scales, and
the calibration block.

Three hazards this module exists to make visible:

  * **f_pi is three different numbers**, and the differences are legitimate.
    92.07 is THE model anchor (an input); 92.4 is the PDG experimental target
    (a thing to be compared against, never an input); 92.28 belongs to a
    different Gamma convention entirely.  Nothing in the tree distinguished
    them at the point of use; after C2 each site imports the one it means.
  * **M(0) lives in three unit systems** with the lattice<->MeV bridge stated
    only in a comment.  The bridge is a constant in its own right so a
    conversion can be written instead of retyped.
  * **The QCD calibration block is the model's largest cluster of underived
    inputs** — items 6-10 of the 2026-06-06 audit's open ledger.  C2.5
    registers all of them, because an input that is not visible as an input is
    the one that quietly becomes a result.  Every entry here is
    ``exactness="external"`` or ``"quantitative"`` and says so.

    from casim.constants import f_pi_anchor_MeV, Lambda_NJL_GeV, g_A
"""
from __future__ import annotations

import math
from fractions import Fraction

from . import Constant, Site, register

# ---------------------------------------------------------------------------
# The colour-Fierz 2/9 — the THIRD distinct 2/9 in the model (C2.4 found it).
#
# The C2 sweep flagged 42 occurrences of 0.2222... in the legacy flat tree as
# "delta_star | sin2_thetaW_onshell".  Reading them showed most were neither:
# they are the colour-Fierz coefficient of the one-gluon-exchange -> NJL
# scalar channel, which the project already names in F256 ("the Fierz 2/9").
#
# So the model carries 2/9 three times over, in three sectors, for three
# unrelated reasons — the E_g representation weight (lepton), the on-shell
# m_W^2:m_Z^2 count (electroweak), and this.  C2.2's rule applies exactly as
# written: they stay three constants.  Registering this one is what lets a
# reader of ca_gap_solve.py tell at a glance that its 2/9 is not delta*.
# ---------------------------------------------------------------------------
register(Constant(
    symbol="c_fierz_colour",
    value=Fraction(2, 9),
    units="dimensionless",
    exactness="exact",
    provenance=("F77", "F116", "F256"),
    derivation="The colour-Fierz coefficient carried by the one-gluon-exchange "
               "to NJL scalar-channel transformation for SU(3), appearing "
               "throughout the gap equation as GS = (2/9)(g^2/2)/(eps_c K + M_g^2). "
               "Named 'the Fierz 2/9' in F256, where it is one of the two "
               "candidate rational values lambda_6 is proved NOT to take.",
    sector="strong",
    tol=0.0,
    sites=(
        Site("src/casim/engine/interactions/running_gap_solve.py", None, kind="import",
             note="three gap-equation branches: const, running, and the field re-solve"),
        Site("src/casim/engine/interactions/running_njl.py", None, kind="import",
             note="contact / resolved / running modes, plus the contact anchor"),
        Site("src/casim/engine/particles/eg_sextic.py", None, kind="import",
             note="gap kernel, the c_fierz default of induced_lambda6, and the "
                  "two inverse-quartic targets"),
        Site("src/casim/engine/interactions/running_scheme_constant.py", None, kind="import"),
    ),
    notes="NOT delta_star (lepton, F175) and NOT sin2_thetaW_onshell "
          "(electroweak, F49/F141), both of which are also exactly 2/9. Three "
          "constants, one number, no relation between them. Before C2 nothing "
          "in the tree distinguished the three at the point of use, which is "
          "the same class of hazard as the three f_pi values.",
))

# ---------------------------------------------------------------------------
# f_pi — three distinct constants, not one contested one
# ---------------------------------------------------------------------------
register(Constant(
    symbol="f_pi_anchor_MeV",
    value=92.07,
    units="MeV",
    exactness="external",
    provenance=("F77", "F123"),
    derivation="THE QCD-scale anchor: the single dimensionful input of the strong "
               "sector. Everything else in the sector is a model ratio scaled by it.",
    sector="strong",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/lattice/si_scale.py", "F_PI_PHYS", kind="import",
             note="was the canonical definition"),
        Site("src/casim/engine/particles/nuclear.py", "F_PI_DEFAULT", kind="import"),
        Site("src/casim/engine/core/spectral_matter.py", None, kind="import",
             note="f_pi_MeV config default"),
        Site("tests/findings/test_FB07_deuteron_binding.py", "F_PI",
             kind="literal", note="C7"),
    ),
))

register(Constant(
    symbol="f_pi_pdg_target_MeV",
    value=92.4,
    units="MeV",
    exactness="external",
    provenance=("PDG",),
    derivation="Experimental value used as a COMPARISON TARGET in the NJL "
               "spectral-matter channel. Never an input to the model.",
    sector="strong",
    tol=1e-9,
    sites=(Site("src/casim/engine/core/spectral_matter.py", "TARGETS", kind="import",
                note="was an unlabelled 92.4 inside the TARGETS dict — one of "
                     "P0's five ALLOWLIST entries, now deleted because the "
                     "import names which f_pi it means"),),
    notes="Deliberately distinct from f_pi_anchor_MeV. If these two are ever "
          "unified, a prediction has been turned into an input.",
))

register(Constant(
    symbol="f_pi_gamma_convention_MeV",
    value=92.28,
    units="MeV",
    exactness="external",
    provenance=("PDG",),
    derivation=r"f_\pi in the convention \Gamma = a^2m^3/(64\pi^3f_\pi^2), used "
               r"only by the chiral-anomaly / pi0 -> gamma gamma calculation.",
    sector="strong",
    tol=1e-9,
    sites=(Site("src/casim/engine/gauge/chiral_anomaly.py", "F_PI_MEV", kind="import",
                note="also one of P0's five ALLOWLIST entries; same resolution"),),
    notes="A different convention, not a disagreement. Documented at "
          "ca_chiral_anomaly.py:1157.",
))

# ---------------------------------------------------------------------------
# The constituent mass M(0) — one physics, three unit systems (C2.5)
# ---------------------------------------------------------------------------
LAMBDA_NJL_GEV = 0.6515
GEV_PER_UNIT = LAMBDA_NJL_GEV / math.pi                   # 0.20737 GeV per lattice unit

register(Constant(
    symbol="GeV_per_lattice_unit",
    value=GEV_PER_UNIT,
    units="GeV per lattice unit",
    exactness="exact",
    provenance=("F77",),
    derivation=r"\Lambda_\text{NJL}/\pi, from the q = 0..\pi momentum map.",
    sector="strong",
    tol=1e-6,
    sites=(Site("src/casim/engine/interactions/running_gap_solve.py", "GEV_PER_UNIT", kind="import"),),
    notes="The lattice<->MeV bridge. Registered so conversions can be computed "
          "rather than retyped; before P0 this existed only as a code comment. "
          "'exact' relative to Lambda_NJL, which is itself a fitted external.",
))

register(Constant(
    symbol="M0_constituent_MeV",
    value=311.2,
    units="MeV",
    exactness="quantitative",
    provenance=("F77",),
    derivation="Canonical NJL constituent quark mass.",
    sector="strong",
    tol=1e-6,
    sites=(
        Site("src/casim/engine/particles/nuclear.py", "M_C_DEFAULT", kind="import"),
        Site("tests/findings/test_FB07_deuteron_binding.py", "M_C",
             kind="literal", note="C7"),
    ),
))

register(Constant(
    symbol="M0_constituent_lattice",
    value=1.50,
    units="lattice units",
    exactness="quantitative",
    provenance=("F77",),
    derivation="The same F77 constituent mass in lattice units: "
               "1.50 * GeV_per_lattice_unit * 1e3 = 311.1 MeV.",
    sector="strong",
    tol=1e-9,
    sweep=False,
    sweep_reason="The value is 1.5. Like F106_COEFF_LATTICE it is too common a "
                 "literal to sweep for without drowning the report; its two "
                 "sites are recorded explicitly.",
    sites=(
        Site("src/casim/engine/interactions/running_gap_solve.py", "M0_TARGET", kind="import"),
        Site("src/casim/engine/interactions/running_scheme_constant.py", "M_TARGET_LAT", kind="import"),
    ),
    notes="Same physics as M0_constituent_MeV. The two agree to 0.03% through "
          "GeV_per_lattice_unit; the residual is rounding in the 311.2 quote.",
))

register(Constant(
    symbol="M0_constituent_GeV",
    value=1.50 * GEV_PER_UNIT,                            # 0.31106 GeV
    units="GeV",
    exactness="quantitative",
    provenance=("F77",),
    derivation="The third unit system: M0_constituent_lattice converted through "
               "GeV_per_lattice_unit. Resolved from the bridge, never retyped "
               "(C2.1) — which is why it differs from 0.3112 in the last digit.",
    sector="strong",
    tol=1e-6,
    notes="C2.5 registered this because the audit named M(0) as living in three "
          "unit systems while only two had owners. The 0.03% gap against "
          "M0_constituent_MeV is the rounding in the 311.2 quote, and it is "
          "visible here rather than hidden in a conversion at a call site.",
))

# ---------------------------------------------------------------------------
# The IR coupling — a BRACKET, and the bracket is the result
# ---------------------------------------------------------------------------
register(Constant(
    symbol="alpha_eff_star",
    bracket=(0.376, 0.411),
    units="dimensionless",
    exactness="bracketed",
    provenance=("F88", "F117", "F145", "F151", "F152", "F154"),
    derivation="The IR face of the strong coupling from the F145 self-consistent "
               "resolved gap: 0.376 at the Debye mass m_D = 0.532 (F88) and 0.411 "
               "at m_V = 0.727 (F117). F154's L-stable nonlinear gap solve brackets "
               "it anchor-free to [0.31, 0.38], with 0.39 at the top.",
    sector="strong",
    sites=(
        Site("src/casim/engine/interactions/running_ir_coupling.py", "ALPHA_EFF_STAR_mD", kind="import",
             note="endpoint('alpha_eff_star', 'lo')"),
        Site("src/casim/engine/interactions/running_ir_coupling.py", "ALPHA_EFF_STAR_mV", kind="import",
             note="endpoint('alpha_eff_star', 'hi')"),
    ),
    notes="Registered as a bracket on purpose and exported with NO scalar surface "
          "(C2.2): `from casim.constants import alpha_eff_star` does not work, and "
          "a caller must write endpoint('alpha_eff_star', 'lo'|'hi'). The "
          "frequently-quoted 0.39 is the midpoint of two SCALE CHOICES, not an "
          "independently determined number; treating it as one would launder a "
          "range into a result.",
))

register(Constant(
    symbol="Lambda_QCD_nf3_GeV",
    value=0.347,
    units="GeV",
    exactness="quantitative",
    provenance=("F151",),
    derivation="The three-flavour QCD scale in the rule's V-scheme (F151-S5, "
               "a_1 = 11/3 exact). Compare FLAG 343(12) MeV.",
    sector="strong",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/interactions/running_gap_solve.py", "Lam3", kind="import",
             note="was gap_solve(..., Lam3=0.347) — a FUNCTION DEFAULT ARGUMENT, "
                  "one of P0's 12 unenforceable sites. C2.4's polarity flip makes "
                  "it enforceable precisely because the default now names an "
                  "imported symbol instead of carrying a literal."),
        Site("tests/findings/test_F154_residuals_A_B.py", None,
             kind="literal", note="C7"),
    ),
    notes="Quoted as '347 MeV' in every comment but stored in GeV. Unit-ambiguous "
          "at every call site; the symbol here carries the unit explicitly.",
))

# ---------------------------------------------------------------------------
# The dual-Meissner gluon mass — the SCALE of the IR face (C2.5)
#
# The audit's open ledger and F152-J2 both turn on m_D: it is the scale at
# which the running freezes, and the two endpoints of alpha_eff_star are two
# choices for it. Registering both makes the bracket's origin queryable.
# ---------------------------------------------------------------------------
register(Constant(
    symbol="m_D_F88_lattice",
    value=0.532,
    units="lattice units",
    exactness="quantitative",
    provenance=("F88",),
    derivation="Dual-Meissner (Debye) gluon mass from the F88 CC8 8^3 run. The "
               "freeze scale of the IR coupling (F152-J2): m_D/Lambda = O(1) puts "
               "the model on the SATURATING branch, not the Landau-pole branch.",
    sector="strong",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/interactions/running_njl.py", "M_D_F88", kind="import",
             note="was the canonical definition; ca_gap_solve and "
                  "ca_eg_sextic_coupling re-export it from here"),
        Site("src/casim/engine/interactions/running_gap_solve.py", "M_D_F88", kind="reexport"),
        Site("src/casim/engine/particles/eg_sextic.py", "M_D_F88", kind="reexport"),
    ),
    notes="Pairs with alpha_eff_star's LOW endpoint 0.376.",
))

register(Constant(
    symbol="m_V_F117_lattice",
    value=0.727,
    units="lattice units",
    exactness="quantitative",
    provenance=("F117",),
    derivation="The same dual-Meissner chain at the F117 representative run "
               "(L = 6). A different scale choice, not a different measurement.",
    sector="strong",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/interactions/running_njl.py", "M_V_F117", kind="import"),
        Site("src/casim/engine/interactions/running_gap_solve.py", "M_V_F117", kind="reexport"),
        Site("src/casim/engine/particles/eg_sextic.py", "M_V_F117", kind="reexport"),
    ),
    notes="Pairs with alpha_eff_star's HIGH endpoint 0.411. The spread between "
          "this and m_D_F88_lattice IS the width of the alpha_eff_star bracket, "
          "which is why that bracket has no midpoint accessor.",
))

# ===========================================================================
#  C2.5 — THE QCD CALIBRATION BLOCK
#
#  Items 6-10 of the open ledger in
#  docs/audits/project-audit-inputs-dynamism-2026-06-06.md. These are the
#  model's genuinely underived strong-sector inputs. They are registered not
#  because they are derived but because they are NOT: an input that no
#  registry names is an input that can quietly be re-described as a result.
#  Each one below states where it enters and what would close it.
# ===========================================================================

register(Constant(
    symbol="Lambda_NJL_GeV",
    value=LAMBDA_NJL_GEV,
    units="GeV",
    exactness="external",
    provenance=("F77", "F116"),
    derivation="NJL cutoff = the Brillouin-zone edge, 651.5 MeV. FITTED, with "
               "G*Lambda^2 and m_0, to the measured (m_c, f_pi, m_pi, <qbar q>) "
               "at 0.2-4.2%. Audit open-ledger item 6.",
    sector="strong",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/interactions/running_njl.py", "LAMBDA_NJL",
             kind="import", note="was the canonical definition"),
        Site("src/casim/engine/interactions/running_gap_solve.py", "LAMBDA_NJL", kind="reexport"),
        Site("src/casim/engine/interactions/running_scale_ratio.py", "LAM", kind="import"),
    ),
    notes="The BZ-edge identification is structural; the 651.5 MeV VALUE is the "
          "fit. GeV_per_lattice_unit is Lambda_NJL/pi, so every lattice->MeV "
          "conversion in the strong sector inherits this fit.",
))

register(Constant(
    symbol="G_Lambda2_NJL",
    value=2.10,
    units="dimensionless",
    exactness="external",
    provenance=("F77", "F116"),
    derivation="The dimensionless NJL four-fermion coupling G*Lambda^2. Fitted "
               "alongside Lambda and m_0. Audit open-ledger item 6.",
    sector="strong",
    tol=1e-9,
    sites=(Site("src/casim/engine/interactions/running_scale_ratio.py", "GLAM2", kind="import"),),
    notes="The audit's C-section route to closing this: integrate out the "
          "dynamical gluon/colour dielectric at the second shell (F97/F98 "
          "enforcer = binder) to INDUCE the contact coupling, the same "
          "Sakharov logic already validated in F57-F61/F79 and F95. F88's "
          "hand-off v = m_D/e = 0.713 is the existing bridge.",
))

register(Constant(
    symbol="m0_current_quark_MeV",
    value=5.5,
    units="MeV",
    exactness="external",
    provenance=("F77", "F116"),
    derivation="Current (bare) light-quark mass in the NJL fit. Third member of "
               "the fitted triple {Lambda, G*Lambda^2, m_0}. Audit item 6.",
    sector="strong",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/interactions/running_gap_solve.py", "M0_CURRENT", kind="import",
             note="held as 0.0055 GeV / GeV_per_lattice_unit, i.e. in lattice "
                  "units — the conversion now goes through the registered bridge"),
        Site("src/casim/engine/interactions/running_scale_ratio.py", "M0", kind="import",
             note="held in GeV as 0.0055"),
    ),
))

register(Constant(
    symbol="g_A",
    value=1.2723,
    units="dimensionless",
    exactness="external",
    provenance=("PDG",),
    derivation="Nucleon axial charge, measured. Enters the F104 piNN coupling "
               "via Goldberger-Treiman. Audit open-ledger item 7.",
    sector="strong",
    tol=1e-9,
    sites=(Site("src/casim/engine/particles/nuclear.py", "G_A", kind="import"),),
    notes="The audit quotes 1.272; the code carries 1.2723 and the code is the "
          "one that runs, so 1.2723 is registered. Closing this needs a "
          "dynamical baryon — the same P2 gap that leaves M_N external.",
))

register(Constant(
    symbol="M_N_isoaveraged_MeV",
    value=938.918,
    units="MeV",
    exactness="external",
    provenance=("PDG",),
    derivation="Isospin-averaged nucleon mass, measured. Enters F104's binding "
               "kinematics. External because the dynamical baryon mass (P2) is "
               "not built — F71's proton is operator-level only. Audit item 8.",
    sector="strong",
    tol=1e-9,
    sites=(Site("src/casim/engine/particles/nuclear.py", "M_N", kind="import"),),
    notes="Distinct from ca_element.py's M_N_MEV = 939.56542052, which is the "
          "NEUTRON rest energy (CODATA), not the isospin average. Two different "
          "quantities that a careless sweep would merge; registered separately.",
))

register(Constant(
    symbol="M_n_neutron_MeV",
    value=939.56542052,
    units="MeV",
    exactness="external",
    provenance=("CODATA",),
    derivation="Neutron rest energy (CODATA). Used by the element/isotope "
               "bookkeeping; F122 derives the m_n - m_p SIGN, not the value.",
    sector="strong",
    tol=1e-9,
    sites=(Site("src/casim/engine/particles/element.py", "M_N_MEV", kind="import"),),
))

register(Constant(
    symbol="r_c_hardcore_fm",
    value=0.448,
    units="fm",
    exactness="quantitative",
    provenance=("F104",),
    derivation="Deuteron short-range hard-core radius. THE ONE TUNED KNOB in "
               "F104 — tuned to reproduce the deuteron binding energy. Audit "
               "open-ledger item 9, and the 'missing ingredient' the matter-"
               "binding roadmap predicted.",
    sector="strong",
    tol=1e-3,
    sites=(Site("src/casim/engine/particles/nuclear.py", None, kind="runtime",
                note="solve_deuteron(r_c=0.50) is a STARTING value; the tuner "
                     "`tune_r_c` solves for 0.448. The tuned result is the "
                     "constant, so the site is runtime, not a literal to strip."),),
    notes="Registered explicitly because it is the strong sector's only fitted "
          "geometric knob and the audit singles it out. A short-range repulsion "
          "derived from the colour dielectric would close it.",
))

register(Constant(
    symbol="g_rho_pi_pi",
    value=6.0,
    units="dimensionless",
    exactness="external",
    provenance=("PDG",),
    derivation="Empirical rho-pi-pi coupling, used only in the KSRF relation "
               "m_rho^2 = 2 g^2 f_pi^2 for the F103-F vector contrast. "
               "Explicitly Tier-3. Audit open-ledger item 10.",
    sector="strong",
    tol=1e-9,
    sweep=False,
    sweep_reason="The value is exactly 6.0 — an integer that appears all over the "
                 "tree as a loop bound, a dimension, and a lattice size. Sweeping "
                 "for it would be pure noise. Its sites are recorded explicitly.",
    sites=(Site("src/casim/engine/particles/meson.py", None, kind="import",
                note="g_rhopipi default argument on rho_mass_ksrf and "
                     "solve_meson_spectrum"),),
    notes="The smallest-consequence input in the block: it feeds one contrast "
          "number and nothing downstream depends on it.",
))

# ---------------------------------------------------------------------------
# External comparison targets for the IR face (F152-J3). Targets, not inputs.
# ---------------------------------------------------------------------------
register(Constant(
    symbol="alpha_hat0_over_pi_CZBR",
    value=0.97,
    units="dimensionless",
    exactness="external",
    provenance=("PDG",),
    derivation="Continuum process-independent effective charge at zero momentum, "
               "alpha_hat(0)/pi, from Cui-Zhang-Binosi-Roberts arXiv:1912.08232. "
               "A COMPARISON TARGET for F152-J3, never an input.",
    sector="strong",
    tol=1e-9,
    sites=(Site("src/casim/engine/interactions/running_ir_coupling.py", "ALPHA_HAT0_OVER_PI",
                kind="import"),),
))

register(Constant(
    symbol="m_g_continuum_GeV",
    value=0.50,
    units="GeV",
    exactness="external",
    provenance=("FLAG",),
    derivation="Dynamical gluon mass from Landau-gauge continuum lattice QCD, "
               "0.5(2) GeV. The continuum counterpart of the model's own "
               "dual-Meissner gap (F152-J3). A target.",
    sector="strong",
    tol=1e-9,
    sweep=False,
    sweep_reason="The value is 0.5, one of the least diagnostic literals there "
                 "is. Its single site is recorded explicitly.",
    sites=(Site("src/casim/engine/interactions/running_ir_coupling.py", "M_G_GEV", kind="import"),),
    notes="The 0.20 GeV uncertainty is carried at the site as M_G_ERR; a "
          "one-sided constant cannot hold it, and inventing a bracket here "
          "would misrepresent a measurement's error bar as a model range.",
))

register(Constant(
    symbol="q_star_a_band_lo",
    value=1.0 / math.sqrt(3.0),
    units="1/a (inverse lattice spacing)",
    exactness="exact",
    provenance=("F151", "F155"),
    derivation="Lower edge of the F151 sqrt(3) matching-scale band for q*, in "
               "units of 1/a. Exact, and numerically identical to c_lat.",
    sector="strong",
    tol=1e-12,
    sites=(
        Site("src/casim/engine/gauge/gluon_self_energy.py", "BAND", kind="import"),
        Site("src/casim/engine/interactions/running_qstar_logmoment.py", "BAND", kind="import"),
        Site("src/casim/engine/gauge/bgfield_loop.py", "BAND", kind="import"),
        Site("src/casim/engine/interactions/running_scheme_constant.py", "QSTAR_LO", kind="import"),
    ),
    notes="Registered as its own constant rather than folded into c_lat. Both "
          "are 1/sqrt(3) and both descend from the BCC sqrt(3), but one is a "
          "SPEED (cells per tick) and this is a MOMENTUM SCALE (inverse lattice "
          "spacing). Writing `QSTAR_LO = c_lat` would typecheck and read as "
          "nonsense. Same discipline as the three 2/9s and the three f_pi.",
))

register(Constant(
    symbol="q_star_a_implied",
    value=0.7327,
    units="1/a (inverse lattice spacing)",
    exactness="quantitative",
    provenance=("F151", "F155"),
    derivation="The PDG-implied lattice-to-MSbar matching scale q*a from F151's "
               "V-scheme determination. F155 brackets q* a to [1/sqrt(3), ~0.97] "
               "and this implied value sits inside; the finite digit is still "
               "open pending the 3-gluon+ghost vertex form factors (F162).",
    sector="strong",
    tol=1e-9,
    sites=(
        Site("src/casim/engine/gauge/gluon_self_energy.py", "QSTAR_IMPLIED",
             kind="import"),
        Site("src/casim/engine/gauge/bgfield_loop.py", "QSTAR_IMPLIED", kind="import"),
        Site("src/casim/engine/gauge/lpt_d1_subtracted.py", "_q_star_a_implied",
             kind="import"),
    ),
    notes="C2.4 surfaced this: the sweep flagged 0.7327 as e_saturation (0.733, "
          "5e-3 tolerance) and reading the sites showed a completely different "
          "quantity. Registering it separates the two rather than widening a "
          "tolerance until the collision goes away. NOT e_saturation (lepton) — "
          "another same-number-different-object pair, like the three 2/9s.",
))

register(Constant(
    symbol="sqrt_sigma_GeV",
    value=0.42,
    units="GeV",
    exactness="quantitative",
    provenance=("F122", "F124", "F146"),
    derivation="The model's string-tension QCD-scale anchor sqrt(sigma), used as "
               "the dual-Meissner scale in the F152-J2 saturating-branch check.",
    sector="strong",
    tol=1e-9,
    sites=(Site("src/casim/engine/interactions/running_ir_coupling.py", "SQRT_SIGMA_GEV", kind="import"),
           Site("src/casim/engine/particles/baryon_dynamics.py", "SQRT_SIGMA_GEV_DEFAULT", kind="import")),
))
