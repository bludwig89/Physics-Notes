"""Lepton / E_g sector — the weight-as-phase constants.

These carry the current charged-lepton canon (key-decisions.md, 2026-07-16,
F253/F255/F256) and, before P0, had **no canonical owner in any module**:
`delta_star` was redefined in two derive scripts and a test, and `lambda_6` was
never a named module constant at all.  C2 gives both an owner here.

    from casim.constants import delta_star, lambda_6, W_star

`delta_star` is a ``Fraction``, so `delta_star == Fraction(2, 9)` is an exact
comparison, not a float one; `delta_star_f` is the float for array code.

The direction of the arrow matters and is recorded explicitly:
`delta_star = 2/9` is **primary** (a founding principle), and `lambda_6` is an
**output** via the F234 arrow.  Reading it the other way round is the F179/CN3
framing that F253 superseded.
"""
from __future__ import annotations

import math
from fractions import Fraction

from . import Constant, Site, register

# ---------------------------------------------------------------------------
# delta*  —  PRIMARY. The E_g representation weight, read as a radian.
# ---------------------------------------------------------------------------
DELTA_STAR = Fraction(2, 9)

register(Constant(
    symbol="delta_star",
    value=DELTA_STAR,
    units="rad",
    exactness="exact",
    provenance=("F175", "F253", "F255", "F256"),
    derivation=r"\delta^* = \dim(E_g)/\dim(T_{1u}\otimes T_{1u}) = 2/9, exact O_h "
               r"group theory (F175: mult_E = 1 of 9 on the BCC second shell). "
               r"It is a GENUINE radian, not a rescalable weight: F255 shows the "
               r"angle is the argument of the E_g order-parameter doublet in the "
               r"deviation simplex, and by Schur's lemma the E_g irrep metric is "
               r"isotropic, so the normalization R = 1 is FORCED (derived, not posited).",
    sector="lepton",
    supersedes=("F179-CN3",),
    tol=0.0,
    sites=(
        Site("src/casim/engine/particles/derive_generator_norm.py", "delta_star",
             kind="import"),
        Site("src/casim/engine/particles/derive_lambda6_sextic.py", "delta_star", kind="import"),
        Site("src/casim/engine/forks/particles/koide_pseudomass_fork.py", "delta_star_f", kind="import"),
        Site("tests/findings/test_F234_Wvc_triple_closed.py", "DELTA_STAR",
             kind="literal", note="the third local redefinition; C7 removes it"),
        Site("tests/findings/test_F230_lepton_angle_geometric_nogo.py", None,
             kind="literal", note="C7"),
    ),
    notes="Adopted as a FOUNDING PRINCIPLE, not derived from condensate dynamics: "
          "the canonical E_g-plane angle IS the representation weight it carries. "
          "Every alternative route is closed — F253 excludes a scale-free "
          "topological origin (the only E_g holonomy on the BCC 2nd shell is "
          "2*pi/3), and F256 proves the dynamical Landau route cannot give exact "
          "3*delta* = Q. Falsification handle: an improved m_tau that moves "
          "delta* off 2/9 (currently -0.89 sigma, 0.003%). NOTE the electroweak "
          "sector's sin2_thetaW_onshell is ALSO 2/9 and is a DIFFERENT OBJECT "
          "(F231); the numeric collision is deliberate to record, not to resolve.",
))

# ---------------------------------------------------------------------------
# cos 3delta*  —  TWO DIFFERENT OBJECTS, 1.7e-5 apart. Do not conflate.
# ---------------------------------------------------------------------------
register(Constant(
    symbol="cos3_delta_star",
    value=math.cos(3 * float(DELTA_STAR)),                # cos(2/3) = 0.7858872...
    units="dimensionless",
    exactness="exact",
    provenance=("F175", "F253"),
    derivation=r"\cos(3\delta^*) = \cos(2/3) with \delta^* = 2/9 exact.",
    sector="lepton",
    tol=1e-12,
    notes="The DERIVED value, resolved from delta_star rather than written as a "
          "decimal (C2.1). Distinct from cos3_delta_data below.",
))

register(Constant(
    symbol="cos3_delta_data",
    value=0.785874,
    units="dimensionless",
    exactness="quantitative",
    provenance=("F93", "F95"),
    derivation="The empirical E_g angle from the F93-O7 charged-lepton mass data.",
    sector="lepton",
    tol=1e-6,
    sites=(
        Site("tests/findings/test_F118_self_consistent_Wvc_and_C.py", "COS3D",
             kind="literal", note="C7"),
        Site("tests/findings/test_F108_democratic_no_go_and_bubble.py", "COS3D",
             kind="literal", note="C7"),
        Site("tests/findings/test_F95_BC_from_qca_loop.py", "COS3D_DATA",
             kind="literal", note="C7"),
        Site("tests/findings/test_F119_kg_scale_three_routes.py", "COS3D",
             kind="literal", note="C7"),
    ),
    notes="This is NOT cos3_delta_star. The two differ by ~1.7e-5, and that gap is "
          "precisely the near-coincidence F256 analyses: B (Dirac sea, F95) and C "
          "(induced condensate coupling, F150) are independent O(1) objects with no "
          "locking relation, so 3*delta* = Q = 2/3 holds only to 1.7e-5. Collapsing "
          "these two into one constant would erase the model's own honest caveat.",
))

# ---------------------------------------------------------------------------
# lambda_6  —  OUTPUT of the F234 arrow, not an input.
#
# C2.5: before C2 this was "nowhere a named module constant" — recomputed in
# each derive script and compared against a literal target inside a test.
# The registry is now its owner.
# ---------------------------------------------------------------------------
register(Constant(
    symbol="lambda_6",
    value=0.243,
    units="dimensionless",
    exactness="quantitative",
    provenance=("F234", "F253", "F256"),
    derivation=r"\lambda_6 = |B|/(2e^6\cos(2/3)), the F234 arrow angle -> brake, "
               r"with B = -5.69e-2 the F95 derived full-BZ sea cubic and "
               r"e = \sqrt3\,\bar y \approx 0.728 the PDG charged-lepton E_g "
               r"amplitude (derive_lambda6_sextic.py, which gives 0.2433). "
               r"[2026-09-29: this text previously cited e ~ 0.733 (e_saturation), "
               r"which gives 0.2334 — outside tol; see notes.]",
    sector="lepton",
    supersedes=("F179-CN3",),
    tol=5e-3,
    sites=(
        Site("src/casim/engine/particles/derive_generator_norm.py", "lam6_F234",
             kind="import",
             note="Imported, used only to back out the implied e for the "
                  "circularity analysis (e6_implied = C_req/lambda_6). Was recorded "
                  "as kind='runtime' ('computed, never substituted'), which the "
                  "code did not match (corrected 2026-09-29)."),
        Site("tests/findings/test_F234_Wvc_triple_closed.py", None, kind="literal",
             note="comparison target, not a definition; C7"),
    ),
    notes="An OUTPUT. F256 proves it is a non-rational strictly between the Fierz "
          "2/9 and the rotor 1/4 (both miss by 5-20%), which is why 'derive "
          "lambda_6 independently' is the wrong request — it is derivative, not "
          "fundamental. Recorded as quantitative, not exact, because it inherits "
          "B's and e's tolerances. OPEN TENSION (2026-09-29): the two registered "
          "determinations of e disagree — sqrt3*ybar (PDG) = 0.728 gives 0.2433 "
          "(this value); e_saturation = 0.733 (F92/F118 solve) gives 0.2334. A 0.7% "
          "move in e is a 4% move in lambda_6 (the e^6 lever).",
))

register(Constant(
    symbol="W_star",
    value=6 * 0.243,                                       # 1.458
    units="dimensionless",
    exactness="quantitative",
    provenance=("F101", "F108", "F118", "F234"),
    derivation=r"W = 6\lambda_6; an output of the same F234 arrow as \lambda_6.",
    sector="lepton",
    tol=5e-3,
    sites=(
        Site("tests/findings/test_F109_f92_bridge_construction.py", "W_STAR",
             kind="literal", expected=1.46, note="C7"),
        Site("tests/findings/test_F108_democratic_no_go_and_bubble.py", "W_STAR",
             kind="literal", expected=1.46, note="C7"),
    ),
    notes="Quoted as 1.46 throughout the tree; 6*0.243 = 1.458. The relation "
          "W = 6*lambda_6 is the F253 statement and was never recorded in code "
          "before P0; C2 makes the registry its owner.",
))

# ---------------------------------------------------------------------------
# The F95 sea cubic — lambda_6's input, worth naming since it is re-typed often.
# ---------------------------------------------------------------------------
register(Constant(
    symbol="B_sea_cubic",
    value=-5.69e-2,
    units="dimensionless",
    exactness="quantitative",
    provenance=("F95",),
    derivation="Derived full-Brillouin-zone Dirac-sea cubic coefficient.",
    sector="lepton",
    tol=1e-3,
    sites=(
        Site("src/casim/engine/particles/derive_generator_norm.py", "B",
             kind="import", note="was a 3-sf local copy (-0.0569)"),
        Site("tests/findings/test_F234_Wvc_triple_closed.py", "B_F95",
             kind="literal", note="C7"),
    ),
))

# ---------------------------------------------------------------------------
# e — the F92/F118 saturation amplitude. lambda_6's OTHER input (C2.5).
# ---------------------------------------------------------------------------
register(Constant(
    symbol="e_saturation",
    value=0.733,
    units="dimensionless",
    exactness="quantitative",
    provenance=("F92", "F118", "F234"),
    derivation="The saturated E_g condensate amplitude entering the F234 arrow "
               "lambda_6 = |B|/(2 e^6 cos(2/3)). Fixed by the F92 consistency "
               "fixed point / F118 self-consistent (W, v, C) solve.",
    sector="lepton",
    tol=5e-3,
    notes="Registered because lambda_6's derivation cites it and nothing owned it. "
          "The e^6 dependence makes lambda_6 acutely sensitive to this number: a "
          "1% move in e is a 6% move in lambda_6, which is most of why lambda_6 "
          "is 'quantitative' and not 'exact'.",
))
