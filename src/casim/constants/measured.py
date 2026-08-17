"""C2.3 — the ``@measured`` escape hatch, enumerated rather than regex-matched.

P0 shipped a dict called ``ALLOWLIST`` inside the consistency test, keyed by
``(path, name)``, holding five prose exemptions.  It worked, but it lived in
the test rather than the registry, it had no type, and nothing stopped it
growing into the usual "add a line to make the check pass" surface.

C2 replaces it with typed declarations that live next to the constants they
are about.  There are exactly two legitimate shapes:

  * ``kind="measured"`` — the site computes the SAME physical quantity in a
    regime where the answer genuinely differs.  ``derive_velocity_addition.py``
    measures the emergent light speed on a 2-D SQUARE lattice and gets
    1/sqrt(2); ``forks/curl_fork_cubic.py`` measures it on the SIMPLE CUBIC
    lattice and gets 1.0.  Neither is a drifted ``c_lat`` — both are
    experiments whose entire point is to land somewhere other than 1/sqrt(3),
    and the cubic fork exists precisely to check whether cubic reproduces BCC.

  * ``kind="coincidence"`` — the site holds a DIFFERENT physical quantity that
    happens to equal a registry value.  The SU(3) lambda_8 normalisation is
    1/sqrt(3) for reasons that have nothing to do with a lattice light speed.
    The registry already carried one of these as prose (F231: the electroweak
    on-shell sin^2 theta_W = 2/9 and the lepton delta* = 2/9 are numerically
    identical and physically unrelated); typing it stops a future sweep from
    "helpfully" collapsing them.

Every record carries a reason.  A ``MeasuredConstant`` without one raises at
import — that is the whole difference between this and an allowlist.
"""
from __future__ import annotations

import math

from . import MeasuredConstant, register_measured

# ---------------------------------------------------------------------------
# c_lat measured on a different lattice — the answer SHOULD differ
# ---------------------------------------------------------------------------
register_measured(MeasuredConstant(
    path="src/casim/engine/interactions/derive_velocity_addition.py",
    name="C_LAT",
    compares_to="c_lat",
    kind="measured",
    value=1.0 / math.sqrt(2.0),
    reason="1/sqrt(2), not 1/sqrt(3): the velocity-addition derivation runs on "
           "the 2-D SQUARE lattice, where the emergent speed is 1/sqrt(2d) with "
           "d = 2. Same physical quantity, different lattice. See the sibling "
           "derive_beta_LV.py.",
    provenance=("F26",),
))

register_measured(MeasuredConstant(
    path="tests/findings/test_SR5_photon_frame_invariance.py",
    name="C_LAT",
    compares_to="c_lat",
    kind="measured",
    value=1.0 / math.sqrt(2.0),
    reason="Same 2-D square lattice as derive_velocity_addition: the frame-"
           "invariance check is a 2-D construction and 1/sqrt(2) is its correct "
           "light speed.",
    provenance=("F26",),
))

register_measured(MeasuredConstant(
    path="src/casim/engine/forks/gauge/curl_fork_cubic.py",
    name="C_LAT",
    compares_to="c_lat",
    kind="measured",
    value=1.0,
    reason="1.0 on the simple-cubic fork. The emergent small-k light speed "
           "there is THE QUANTITY UNDER TEST — this fork exists to check "
           "whether cubic reproduces the BCC 1/sqrt(3), and the finding is that "
           "it does not. Rewriting it to import c_lat would delete the result.",
    provenance=("F26", "D1"),
))

# ---------------------------------------------------------------------------
# Numerical coincidences — same number, unrelated physics
# ---------------------------------------------------------------------------
register_measured(MeasuredConstant(
    path="src/casim/engine/interactions/running_njl.py",
    name=None,
    compares_to="c_lat",
    kind="coincidence",
    value=1.0 / math.sqrt(3.0),
    reason="The SU(3) Gell-Mann lambda_8 normalisation diag(1,1,-2)/sqrt(3). "
           "1/sqrt(3) here is a group-theory normalisation with no connection "
           "to a lattice light speed; the collision is arithmetic, not physics.",
    provenance=("F77",),
))

register_measured(MeasuredConstant(
    path="src/casim/engine/gauge/strong.py",
    name=None,
    compares_to="c_lat",
    kind="coincidence",
    value=1.0 / math.sqrt(3.0),
    reason="The same Gell-Mann lambda_8 normalisation, in the SU(3) generator "
           "table itself (_LAMBDA[7]). Not a light speed.",
    provenance=("F43",),
))

register_measured(MeasuredConstant(
    path="src/casim/engine/gauge/bgfield_loop.py",
    name=None,
    compares_to="alpha_hat0_over_pi_CZBR",
    kind="coincidence",
    value=0.97,
    reason="0.97 here is the TOP of the F151/F155 q* band in units of 1/a, "
           "quoted in the d1/q* status report. It is not the CZBR "
           "process-independent effective charge, which is also 0.97. Two "
           "unrelated dimensionless 0.97s, one file apart from each other.",
    provenance=("F155",),
))

register_measured(MeasuredConstant(
    path="src/casim/engine/gauge/bgfield_loop.py",
    name=None,
    compares_to="e_saturation",
    kind="coincidence",
    value=0.733,
    reason="0.733 in the status dict is q*a rounded to three figures (the "
           "registered value is q_star_a_implied = 0.7327), quoted alongside "
           "the Lambda ratio and the Wilson contrast. It is not the lepton "
           "saturation amplitude e ~ 0.733, which lives in a different sector "
           "and matches only because e_saturation carries a 5e-3 tolerance.",
    provenance=("F151", "F155"),
))

register_measured(MeasuredConstant(
    path="src/casim/engine/forks/gravity/gr_fork_F79_structural_G.py",
    name=None,
    compares_to="a_over_ellP",
    kind="measured",
    value=math.sqrt(8.0 * math.pi) * 3.0 ** 0.25,
    reason="This fork DERIVES a/ell_P from the induced Einstein-Hilbert "
           "prefactor and then checks the result against the closed form to "
           "1e-12. The closed form is the thing under test; importing the "
           "registry's copy of it would make the check compare the answer with "
           "itself. F79 is where this constant comes from.",
    provenance=("F79",),
))

register_measured(MeasuredConstant(
    path="src/casim/engine/forks/gravity/gr_fork_F238_geon_relic_abundance.py",
    name=None,
    compares_to="W_star",
    kind="coincidence",
    value=1.453152027,
    reason="A coefficient of the Abramowitz-Stegun 7.1.26 rational "
           "approximation to erfc, hand-rolled because the fork avoids scipy. "
           "It matches W* = 1.458 only because W*'s tolerance is 5e-3. Nothing "
           "in this fork touches the lepton sector.",
    provenance=(),
))

register_measured(MeasuredConstant(
    path="src/casim/engine/forks/darkmatter/dm_fork_F205_sterile_qke_boltzmann.py",
    name="V_D",
    compares_to="lambda_6",
    kind="coincidence",
    value=2.0 * 1.2020569031595943 / math.pi ** 2,          # 2 zeta(3)/pi^2
    reason="2*zeta(3)/pi^2 = 0.24359, the standard thermal-asymmetry prefactor "
           "in the sterile-neutrino quantum kinetic equation. It lands inside "
           "lambda_6's 5e-3 tolerance by accident; the two have no relation.",
    provenance=("F205",),
))

# ---------------------------------------------------------------------------
# F295 — the cosmological tilt's required one-loop coupling happens to equal 2/9
#
# This is the `coincidence` category doing exactly the job it was typed for, and
# it is deliberately NOT resolved by importing one of the three registry symbols
# that already hold 2/9 (delta_star, sin2_thetaW_onshell, c_fierz_colour).
# Importing any one of them would silently PICK A SIDE — and F295's whole point
# is that no mechanism has yet picked one, and that the value's significance
# fails F286's look-elsewhere count. The literal stays, typed and reasoned.
# ---------------------------------------------------------------------------
register_measured(MeasuredConstant(
    path="src/casim/engine/interactions/cosmology_anomalous_dimension.py",
    name="two_ninths",
    compares_to="delta_star",
    kind="coincidence",
    value=2.0 / 9.0,
    reason="A DIFFERENT physical quantity that happens to equal 2/9: the "
           "one-loop coupling the primordial tilt would require, "
           "g_eff = 2 pi (1 - n_s) = 0.2205 +/- 0.0264, which sits 0.064 sigma "
           "from 2/9. It is written as a bare literal ON PURPOSE. Three "
           "registered constants already hold 2/9 and CLAUDE.md keeps them "
           "separate because they are unrelated; importing one here would "
           "assert a link F295 explicitly does not claim. F286 T5's "
           "look-elsewhere count (6 hits in 396 candidates, p = 0.32) rejects "
           "the value's significance, and F295 improves only the SHAPE "
           "argument. Resolve this record by importing a specific symbol ONLY "
           "when a mechanism has identified the operator.",
    provenance=("F295", "F286", "F175"),
))

# ---------------------------------------------------------------------------
# NOT here: the two non-anchor f_pi sites.
#
# P0's ALLOWLIST exempted `spectral_matter.TARGETS` (92.4, the PDG comparison
# target) and `ca_chiral_anomaly.F_PI_MEV` (92.28, the Gamma-convention value)
# because a literal check could not tell them from a drifted anchor.  C2 does
# not need an exemption for either: both now IMPORT the constant they actually
# mean — `f_pi_pdg_target_MeV` and `f_pi_gamma_convention_MeV` — so the
# distinction is carried by the name at the point of use, which is where it
# was always missing.  Two allowlist entries deleted rather than ported.
# ---------------------------------------------------------------------------
