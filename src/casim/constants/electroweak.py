"""Electroweak sector — the two faces of the Weinberg angle, and the
lepton hypercharges.

`sin^2 theta_W` has two values in the model and both are correct. They live at
different scales and are reconciled by F231. Before P0 that reconciliation
existed only inside a test file, so nothing in code said which face applied
where — the exact situation that makes a "the model predicts 1/4" claim
ambiguous to a reader.  After C2 a module says which one it means by importing
it, and importing the wrong one is a *type* of error the registry can catch.

    from casim.constants import sin2_thetaW_uv, sin2_thetaW_onshell

Both are ``Fraction``s: `sin2_thetaW_onshell == Fraction(2, 9)` is an exact
comparison. `sin2_thetaW_onshell_f` is the float.

The lepton hypercharges (F279 follow-up 1)
------------------------------------------
`Y_LEPTON_L`, `Y_E_R`, `Y_NU_R` were literals in
`casim.engine.gauge.hypercharge` under a comment calling them the Standard
Model's assignment.  They are not an input: F165 derived them, F279 re-derived
them over ℚ and corrected the attribution, and the register was rewritten to
say so on 2026-08-02.  The code kept saying the opposite — the one live
code-vs-finding contradiction the 2026-08-04 completeness sweep still carried
(H5).  They live here now, with the F279 arrow written into the values:

    from casim.constants import Y_LEPTON_L, Y_E_R, Y_NU_R          # exact
    from casim.constants import Y_LEPTON_L_f, Y_E_R_f, Y_NU_R_f    # array code

The three are **not equally derived**, and the registry says which is which
rather than flattening them into "the SM values":

  * `Y_NU_R = 0` is forced outright, with no normalisation freedom — the F47
    Majorana bilinear carries 2*y_nu, so gauge invariance gives y_nu = 0.
  * `Y_E_R = 2 * Y_LEPTON_L` is derived, and holds for **every** colour
    multiplicity (F279 A3: y_L : y_e = -N_c : -2N_c for all N_c).
  * `Y_LEPTON_L = -1` **is** the residual — the one overall normalisation
    F279 names as the unit of charge.  It is exact because it is a choice of
    unit, not because it was computed.

That split is also why the quark hypercharges are NOT here.  `Y_QUARK_L`,
`Y_U_R`, `Y_D_R` sit on the same solution line, but their *fractions* are
quantisation **plus** N_c = 3 (F279 A3), and N_c = 3 is underived (F293 grades
it PARTIAL).  Registering them would also force them into the C2.4 sweep —
1/3, 4/3 and -2/3 are diagnostic values, so `sweep=False` is not available to
them — and the sweep would then flag every unrelated third in `src/`.  Left in
`hypercharge.py` deliberately; see the note there.
"""
from __future__ import annotations

from fractions import Fraction

from . import Constant, Site, register

register(Constant(
    symbol="sin2_thetaW_uv",
    value=Fraction(1, 4),
    units="dimensionless",
    exactness="exact",
    provenance=("F45", "F231"),
    derivation=r"From the bare coupling ratio g'^2/g^2 = 1/3 (F45), which matches "
               r"the Casimir/dimension count: \sin^2\theta_W = (g'^2/g^2)/(1+g'^2/g^2) "
               r"= 1/4. This is the UV / bare face.",
    sector="electroweak",
    tol=0.0,
    sweep=False,
    sweep_reason="The value is 0.25. Sweeping for it would flag every half-of-a-"
                 "half in the tree. Its one site computes it with exact rational "
                 "arithmetic and is recorded explicitly.",
    sites=(Site("tests/runners/FA07_weinberg_angle.py", None, kind="runtime",
                note="computed inside main() as weinberg_from_ratio(Fraction(1,3)) "
                     "with exact rational arithmetic — derived, never hardcoded, "
                     "so there is no literal for C2 to strip"),),
    notes="Reported as a PREDICTION against PDG 0.22305 in "
          "tests/findings/test_F112_si_predictions.py. Compare at the right scale: "
          "this is the UV cap, not the on-shell value.",
))

register(Constant(
    symbol="sin2_thetaW_onshell",
    value=Fraction(2, 9),
    units="dimensionless",
    exactness="exact",
    provenance=("F49", "F138", "F141", "F231"),
    derivation=r"The on-shell ratio m_W^2:m_Z^2 = 7:9 from the BCC Wigner-Seitz "
               r"facet-axis count (F141: the F49 '7' is the Voronoi facet axes, "
               r"exact), giving \sin^2\theta_W = 2/9.",
    sector="electroweak",
    tol=0.0,
    sites=(
        Site("tests/findings/test_F175_lattice_2_9_eg_weight.py", None,
             kind="runtime", note="derived from the shell count, not written down"),
        Site("tests/findings/test_F141_ws_cell_mass_counting.py", None,
             kind="runtime"),
        Site("src/casim/engine/gauge/derive_gauge_boson_masses.py",
             "sin2_thetaW_onshell", kind="import",
             note="F320 recomputes 2/9 from the 7:2 counts and asserts equality "
                  "against this registry value rather than trusting either -- "
                  "B0a. The import is the guard, not a convenience."),
    ),
    notes="Numerically 0.2222, against PDG 0.22305 — the on-shell face is the one "
          "that lands. Reconciled with the F45 UV face by F231. This 2/9 is NOT "
          "the same object as the lepton sector's delta* = 2/9 (F175 E_g weight); "
          "they are numerically identical and physically unrelated, which is why "
          "the C2.4 sweep reports an ambiguous 2/9 as 'one of {delta_star, "
          "sin2_thetaW_onshell}' rather than picking one.",
))

# ---------------------------------------------------------------------------
# Lepton-sector hypercharges.  Convention: Y = 2y, Q = T_3 + Y/2 (the
# `hypercharge.py` convention; F279 works in y and F38 quotes Y).
#
# The arrow is written into the values, not just into the prose: Y_E_R resolves
# from Y_LEPTON_L (C2.1, the same pattern as W_star = 6*lambda_6), because the
# ratio is what F279 derives and the normalisation is what it does not.
# ---------------------------------------------------------------------------
Y_L_NORMALISATION = Fraction(-1)          # the one residual: the unit of charge

register(Constant(
    symbol="Y_LEPTON_L",
    value=Y_L_NORMALISATION,
    units="dimensionless",
    exactness="exact",
    provenance=("F165", "F279"),
    derivation=r"The overall normalisation of the F279 hypercharge line, fixed at "
               r"Y_L = -1 (equivalently y_Q = 1/6, Y = 2y). F279 A2: the six-row "
               r"system [SU(2)]^2U(1), [SU(3)]^2U(1), the three F27/F41 mass-step "
               r"rows and the F47 Majorana row has rank 6 in 7 unknowns, so the "
               r"RATIOS y_Q:y_u:y_d:y_L:y_e:y_nu = 1:4:-2:-3:-6:0 are derived and "
               r"exactly one number is free. This is that number. Exact because it "
               r"is a choice of unit, not because it was computed.",
    sector="electroweak",
    tol=0.0,
    sweep=False,
    sweep_reason="The value is -1. Sweeping for it would flag every sign flip, "
                 "every decrement and every reversed direction cosine in the tree. "
                 "Its two sites are recorded explicitly instead.",
    sites=(
        Site("src/casim/engine/gauge/hypercharge.py", "Y_LEPTON_L", kind="import",
             note="was a literal under a comment reading 'SM hypercharge "
                  "assignment'; F279 follow-up 1"),
        Site("src/casim/engine/forks/electroweak/hypercharge_fork.py",
             "Y_LEPTON_L", kind="reexport",
             note="drop-in superset of the promoted module; re-exports the "
                  "binding, so nothing here can drift"),
    ),
    notes="NOT a Standard-Model input, which is what the code said until F279's "
          "follow-up 1 landed. What remains free is one unit of charge — the F49 "
          "alpha / sin^2(theta_W) question, not a quantisation question. Read with "
          "Y_E_R (derived from this one) and Y_NU_R (forced outright). The quark "
          "hypercharges are deliberately not registered: see the module docstring.",
))

register(Constant(
    symbol="Y_E_R",
    value=2 * Y_L_NORMALISATION,                           # -2, resolved not typed
    units="dimensionless",
    exactness="exact",
    provenance=("F165", "F279"),
    derivation=r"Y_e = 2 Y_L, derived. The F27/F41 charged-lepton mass-step row "
               r"y_e = y_L - y_phi with y_phi = 3y_Q closes the system to "
               r"y_L:y_e = -3:-6 (F279 A2). F279 A3 shows the same ratio is "
               r"y_L:y_e = -N_c:-2N_c for EVERY colour multiplicity, so this "
               r"factor of 2 is N_c-independent — unlike the quark fractions.",
    sector="electroweak",
    tol=0.0,
    sweep=False,
    sweep_reason="The value is -2. A literal -2 in the tree is an exponent, a "
                 "stride or an offset far more often than a hypercharge, so "
                 "finding one is not evidence.",
    sites=(
        Site("src/casim/engine/gauge/hypercharge.py", "Y_E_R", kind="import"),
        Site("src/casim/engine/forks/electroweak/hypercharge_fork.py", "Y_E_R",
             kind="reexport"),
    ),
    notes="Resolved as 2*Y_LEPTON_L rather than written as -2, so the derived "
          "relation cannot drift away from the normalisation it depends on. "
          "Y_LEPTON_L - Y_E_R = +1 is the Higgs-equivalent DELTA_Y_E absorbed "
          "into U(x) by F41; hypercharge.py computes it from these two.",
))

register(Constant(
    symbol="Y_NU_R",
    value=Fraction(0),
    units="dimensionless",
    exactness="exact",
    provenance=("F279", "F47", "F266"),
    derivation=r"Forced, with NO normalisation freedom: the F47 Higgs-free "
               r"Majorana bilinear nu_R^T C nu_R carries hypercharge 2 y_nu, so "
               r"U(1)_Y invariance of that term gives 2 y_nu = 0, hence y_nu = 0 "
               r"exactly over Q. F279 A2 — this is the row that actually closes "
               r"the hypercharge system, and F279 A1 shows the [grav]^2 U(1) row "
               r"F165 credited adds no rank once nu_R is carried as a field.",
    sector="electroweak",
    tol=0.0,
    sweep=False,
    sweep_reason="The value is 0. Every module in the tree assigns zero to "
                 "something; the sweep skips bare integer constants for exactly "
                 "this reason and a float 0.0 is no more diagnostic.",
    sites=(
        Site("src/casim/engine/gauge/hypercharge.py", "Y_NU_R", kind="import"),
        Site("src/casim/engine/forks/electroweak/hypercharge_fork.py", "Y_NU_R",
             kind="reexport"),
    ),
    notes="The strongest of the three: it is not conditional on the "
          "normalisation, on N_c, or on the anomaly rows. F266 records the same "
          "fact as 'Y = 0 structurally forced' for the sterile-neutrino dark "
          "matter channel. The comment it replaces called it 'sterile in the "
          "minimal SM', which named the SM's reason and not the model's.",
))
