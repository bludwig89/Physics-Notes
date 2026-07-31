"""Electroweak sector — the two faces of the Weinberg angle.

`sin^2 theta_W` has two values in the model and both are correct. They live at
different scales and are reconciled by F231. Before P0 that reconciliation
existed only inside a test file, so nothing in code said which face applied
where — the exact situation that makes a "the model predicts 1/4" claim
ambiguous to a reader.  After C2 a module says which one it means by importing
it, and importing the wrong one is a *type* of error the registry can catch.

    from casim.constants import sin2_thetaW_uv, sin2_thetaW_onshell

Both are ``Fraction``s: `sin2_thetaW_onshell == Fraction(2, 9)` is an exact
comparison. `sin2_thetaW_onshell_f` is the float.
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
    ),
    notes="Numerically 0.2222, against PDG 0.22305 — the on-shell face is the one "
          "that lands. Reconciled with the F45 UV face by F231. This 2/9 is NOT "
          "the same object as the lepton sector's delta* = 2/9 (F175 E_g weight); "
          "they are numerically identical and physically unrelated, which is why "
          "the C2.4 sweep reports an ambiguous 2/9 as 'one of {delta_star, "
          "sin2_thetaW_onshell}' rather than picking one.",
))
