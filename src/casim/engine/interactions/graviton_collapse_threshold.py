"""graviton_collapse_threshold.py -- does a head-on collision of two band-top
photons/gravitons (F357) reach the model's own exact gravitational-collapse
threshold (F228's one-cell Planck-mass black-hole remnant)?  (rubric row E12,
quantum-gravity sector -- the DYNAMICAL residual F357 Sec.7 named and left open.)
===============================================================================

**The residual this addresses.**  F357 closed E12's KINEMATIC half: a single
photon/graviton line cannot carry more than E_max = sqrt(pi*sqrt3/8) E_Planck
= 0.8247 E_Planck (exact, zero new free parameters).  F357 Sec.7 stated
explicitly what it did NOT compute: "a graviton-graviton scattering amplitude,
interaction vertex, or partial-wave unitarity bound" -- the DYNAMICAL question
of what a would-be near-band-top graviton-graviton collision actually does.

**Why this module does not attempt a partial-wave S-matrix computation.**  The
standard continuum EFT-of-gravity literature (Donoghue gr-qc/9512024, already
cited by F357) states graviton-graviton tree amplitudes grow with energy and
formally exceed |a_J|<=1 near the Planck scale, but the O(1) numerical
coefficient of that violation is process/helicity/convention-dependent across
papers (differs by factors of a few depending on which channel, which Planck-
mass convention).  Importing one such external coefficient wholesale, without
re-deriving the model's own cubic graviton self-interaction vertex from the
induced Einstein-Hilbert action, would risk grafting an external, convention-
sensitive number onto this model dressed as a "prediction" -- exactly the kind
of import-without-derivation this project's exactness discipline exists to
avoid.  What THIS module computes instead needs no imported coefficient at
all: it is a plain relativistic CM-energy THRESHOLD comparison between two
already-exact, already-published, model-native numbers -- F357's E_max and
F228's one-cell remnant mass M_rem -- both already derived from the SAME
registered structural ruler a_over_ellP (F79/F107), so the comparison costs
zero new free parameters and needs no external import.

**THE RESULT (headline, exact-algebraic).**  Write A := a_over_ellP (F79/F107,
registered).  F357 gives E_max/E_Planck = pi*sqrt(3)/A.  F228 derives the
one-cell remnant by tiling a Schwarzschild horizon (area 16*pi*(M/M_Pl)^2 *
ell_P^2) with F107 cells (area a^2 = A^2 * ell_P^2 = 8*pi*sqrt(3)*ell_P^2) and
setting the cell count N=1: M_rem/M_Pl = A/(4*sqrt(pi)) -- reproducing F228's
own closed form 3^(1/4)/sqrt(2) exactly (check B).  Two band-top quanta
colliding head-on carry CM energy sqrt(s_max) = 2*E_max.  The ratio to M_rem
is then

    sqrt(s_max) / (M_rem c^2)  =  [2*pi*sqrt(3)/A] / [A/(4*sqrt(pi))]
                                =  8*pi^(3/2)*sqrt(3) / A^2
                                =  8*pi^(3/2)*sqrt(3) / (8*pi*sqrt(3))   [A^2=8*pi*sqrt3]
                                =  sqrt(pi)   -- EXACTLY, A cancels completely.

So a head-on collision of two of the model's own maximum-energy photons or
gravitons supplies EXACTLY sqrt(pi) ~= 1.7725 times the rest-mass-energy of
the model's own minimal stable black hole -- comfortably super-threshold, in
closed form, with zero new free parameters (check C).  A SINGLE band-top
quantum, by contrast, falls short: E_max/(M_rem c^2) = sqrt(pi)/2 ~= 0.8862
exactly (check D) -- sub-threshold alone, super-threshold in a head-on pair.

**Physical reading, honestly scoped.**  Standard relativistic kinematics: for
two colliding particles, sqrt(s) is the CM energy available to produce a
state at rest in that frame, and sqrt(s) >= (target rest-mass energy) is the
ordinary threshold condition (zero leftover KE at exact threshold; a margin
above it, here exactly a factor sqrt(pi), leaves room for outgoing KE/recoil).
That two band-top quanta clear the model's own exact black-hole-remnant
threshold is exactly the kinematic precondition of the "self-completeness /
classicalization" resolution of the naive graviton-graviton unitarity puzzle
(Dvali & Gomez, "Self-Completeness of Einstein Gravity," arXiv:1005.3497;
't Hooft, Phys. Lett. B 198 (1987) 61 -- gravitational collapse, not a growing
perturbative amplitude, is the correct description once a collision's CM
energy exceeds its own Schwarzschild threshold).  This module establishes the
KINEMATIC half of that argument is realised, exactly, inside this model's own
already-published numbers.  It does **not** compute the dynamical black-hole-
formation cross-section, an impact-parameter/hoop-conjecture bound, or any
graviton-graviton scattering amplitude -- that dynamical calculation remains
open, precisely where F357 Sec.7 left it (see "Honest scope" below).

**Order-of-magnitude cross-check (not exact, honestly tagged).**  F223's geon
virial mass mu = sqrt(2) M_Pl carries F223's own "order-of-magnitude" tier (a
relativistic self-gravitating virial estimate, not a closed-form derivation).
Against it: E_max/mu = sqrt(pi)*3^(1/4)/4 ~= 0.583 (sub-threshold alone) and
sqrt(s_max)/mu = sqrt(pi)*3^(1/4)/2 ~= 1.166 (super-threshold for the pair) --
a closed form exists (both cancel the same A), but it inherits mu's order-of-
magnitude tier, not exact, so it is reported separately (check E) rather than
folded into the headline exact claim (checks C, D).

**Numerics discipline (CLAUDE.md).**  Real arithmetic + sympy throughout (a
threshold-energy comparison, no chiral/complex spinor transform anywhere);
`casim.numerics.xp` for the one numeric cross-check against the live registry
value of `a_over_ellP`.

Run:  python3 -m casim.engine.interactions.graviton_collapse_threshold
"""

from __future__ import annotations

import sympy as sp

from casim.constants import a_over_ellP as _A_OVER_ELLP
from casim.numerics import xp

# ---- constants (D7: imported, never re-typed as literals) ------------------
A_OVER_ELLP = _A_OVER_ELLP                      # F79/F107 structural SI ruler
SQRT2 = float(xp.sqrt(2.0))                     # F223's N=2 geon virial factor

CHECKS: dict[str, dict] = {}


def _record(name: str, passed: bool | None, detail: dict) -> dict:
    out = {"pass": (None if passed is None else bool(passed)), "detail": detail}
    CHECKS[name] = out
    return out


# ---- shared sympy symbols ---------------------------------------------------
_A = sp.sqrt(8 * sp.pi) * sp.Integer(3) ** sp.Rational(1, 4)   # exact a_over_ellP


# ===========================================================================
# A -- the canonical-cell identity A^2 = 8*pi*sqrt(3) (F79/F107, reused)
# ===========================================================================
def check_A_canonical_cell_identity() -> dict:
    """A = sqrt(8*pi)*3^(1/4)  =>  A^2 = 8*pi*sqrt(3) exactly (sympy); the
    registered numeric a_over_ellP must match this closed form to the
    registry's own tolerance."""
    residual_symbolic = sp.simplify(_A**2 - 8 * sp.pi * sp.sqrt(3))
    numeric_resid = abs(A_OVER_ELLP**2 - 8.0 * float(xp.pi) * float(xp.sqrt(3.0)))
    return _record(
        "A_canonical_cell_identity",
        residual_symbolic == 0 and numeric_resid < 1e-9,
        {
            "A_squared_minus_8pi_sqrt3_symbolic": str(residual_symbolic),
            "A_squared_minus_8pi_sqrt3_numeric": numeric_resid,
            "registered_a_over_ellP": A_OVER_ELLP,
        },
    )


# ===========================================================================
# B -- the one-cell remnant mass, re-derived symbolically from A (F228 reuse)
# ===========================================================================
def check_B_remnant_mass_closed_form() -> dict:
    """F228: Schwarzschild horizon area 16*pi*(M/M_Pl)^2*ell_P^2 tiled by
    F107 cells of area A^2*ell_P^2; N(M)=16*pi*(M/M_Pl)^2/A^2; N=1 gives
    M_rem/M_Pl = A/(4*sqrt(pi)).  Must equal F228's own published closed form
    3^(1/4)/sqrt(2) exactly, and match its published numeric value 0.93060."""
    m_rem_from_A = _A / (4 * sp.sqrt(sp.pi))
    m_rem_f228_form = sp.Integer(3) ** sp.Rational(1, 4) / sp.sqrt(2)
    residual_symbolic = sp.simplify(m_rem_from_A - m_rem_f228_form)
    m_rem_float = float(m_rem_from_A)
    f228_published = 0.93060
    return _record(
        "B_remnant_mass_closed_form",
        residual_symbolic == 0 and abs(m_rem_float - f228_published) < 5e-5,
        {
            "M_rem_over_MPl_from_A": m_rem_float,
            "M_rem_over_MPl_F228_closed_form": float(m_rem_f228_form),
            "residual_symbolic": str(residual_symbolic),
            "F228_published_value": f228_published,
        },
    )


# ===========================================================================
# C -- HEADLINE: two band-top quanta vs the remnant threshold (exact)
# ===========================================================================
def check_C_two_quantum_threshold(pairing_law: str = "even") -> dict:
    """sqrt(s_max)/(M_rem c^2) = sqrt(pi) exactly for the physical paired
    "even" dispersion law (F357/F248/F69); the un-paired chiral_double control
    must NOT reproduce this fixed physical target."""
    e_max_over_eplanck = (
        sp.pi * sp.sqrt(3) / _A if pairing_law == "even"
        else 2 * sp.pi * sp.sqrt(3) / _A          # chiral_double control (F357 Sec.3)
    )
    sqrt_s_max = 2 * e_max_over_eplanck
    m_rem = _A / (4 * sp.sqrt(sp.pi))
    ratio = sp.simplify(sqrt_s_max / m_rem)
    physical_target = sp.sqrt(sp.pi)
    ratio_float = float(ratio)
    return _record(
        "C_two_quantum_threshold",
        abs(ratio_float - float(physical_target)) < 1e-9,
        {
            "pairing_law": pairing_law,
            "sqrt_s_max_over_MremC2": ratio_float,
            "closed_form": str(ratio),
            "physical_expected_closed_form": "sqrt(pi)",
            "physical_expected": float(physical_target),
            "super_threshold": ratio_float > 1.0,
        },
    )


# ===========================================================================
# D -- single quantum vs the remnant threshold (exact, sub-threshold)
# ===========================================================================
def check_D_single_quantum_subthreshold(pairing_law: str = "even") -> dict:
    """E_max/(M_rem c^2) = sqrt(pi)/2 exactly for the even law -- a single
    band-top quantum alone falls short of the remnant rest-mass energy."""
    e_max_over_eplanck = (
        sp.pi * sp.sqrt(3) / _A if pairing_law == "even"
        else 2 * sp.pi * sp.sqrt(3) / _A
    )
    m_rem = _A / (4 * sp.sqrt(sp.pi))
    ratio = sp.simplify(e_max_over_eplanck / m_rem)
    physical_target = sp.sqrt(sp.pi) / 2
    ratio_float = float(ratio)
    return _record(
        "D_single_quantum_subthreshold",
        abs(ratio_float - float(physical_target)) < 1e-9,
        {
            "pairing_law": pairing_law,
            "E_max_over_MremC2": ratio_float,
            "closed_form": str(ratio),
            "physical_expected_closed_form": "sqrt(pi)/2",
            "physical_expected": float(physical_target),
            "sub_threshold_alone": ratio_float < 1.0,
        },
    )


# ===========================================================================
# E -- order-of-magnitude cross-check vs F223's geon virial mass (not exact)
# ===========================================================================
def check_E_geon_virial_cross_check(pairing_law: str = "even") -> dict:
    """Cross-check against F223's mu_geon = sqrt(2) M_Pl. F223 states this
    mass at ORDER-OF-MAGNITUDE tier (a virial estimate), so this check is
    reported at that tier -- it does not participate in the exact headline
    claim (checks C, D) and is not gated to the same tolerance."""
    e_max_over_eplanck = (
        sp.pi * sp.sqrt(3) / _A if pairing_law == "even"
        else 2 * sp.pi * sp.sqrt(3) / _A
    )
    sqrt_s_max = float(2 * e_max_over_eplanck)
    e_max = float(e_max_over_eplanck)
    mu_geon = SQRT2  # F223: mu/M_Pl = sqrt(2), order-of-magnitude
    ratio_pair = sqrt_s_max / mu_geon
    ratio_single = e_max / mu_geon
    # order-of-magnitude tier: pass = consistent direction (pair super-threshold,
    # single sub-threshold), not a tight numeric match
    consistent = (ratio_pair > 1.0) and (ratio_single < 1.0)
    return _record(
        "E_geon_virial_cross_check",
        consistent,
        {
            "pairing_law": pairing_law,
            "tier": "order-of-magnitude (inherits F223's mu tier, not exact)",
            "sqrt_s_max_over_mu_geon": ratio_pair,
            "E_max_over_mu_geon": ratio_single,
            "mu_geon_over_MPl": mu_geon,
        },
    )


# ===========================================================================
def run_all(pairing_law: str = "even") -> dict:
    """Gate entry.

    Declared negative control (D9/H2): ``pairing_law="chiral_double"`` swaps
    F357's physical paired "even" law for the un-paired doubled law (F248/
    CLAUDE.md: NOT the physical photon/graviton dispersion). Checks C and D
    test the COMPUTED ratio against FIXED physical targets (sqrt(pi),
    sqrt(pi)/2) rather than adapting to whichever law was selected, so both
    must go red: the control's band top is double, giving ratios 2*sqrt(pi)
    and sqrt(pi) instead. A and B do not read the dispersion law at all and
    stay green. E also flips red under the control (verified live): doubling
    the band top pushes even the SINGLE-quantum energy above mu_geon, so its
    "sub-threshold-alone" direction check fails too -- a stronger control
    effect than strictly required, left as a genuine (not hand-tuned) result
    rather than loosened to pass.
    """
    global CHECKS
    CHECKS = {}
    checks = {
        "A_canonical_cell_identity": check_A_canonical_cell_identity(),
        "B_remnant_mass_closed_form": check_B_remnant_mass_closed_form(),
        "C_two_quantum_threshold": check_C_two_quantum_threshold(pairing_law),
        "D_single_quantum_subthreshold": check_D_single_quantum_subthreshold(pairing_law),
        "E_geon_virial_cross_check": check_E_geon_virial_cross_check(pairing_law),
    }
    counted = {k: v for k, v in checks.items() if v.get("pass") is not None}
    n_pass = sum(1 for v in counted.values() if v["pass"])
    return {
        "finding": "F359",
        "title": ("Two band-top photons/gravitons collide with sqrt(pi) times "
                   "the model's own minimal black-hole remnant energy -- a "
                   "kinematic threshold on E12's still-open dynamical residual, "
                   "not a computation of it"),
        "pairing_law": pairing_law,
        "checks": checks,
        "n_pass": n_pass,
        "n_total": len(counted),
        "all_pass": n_pass == len(counted),
    }


if __name__ == "__main__":            # guard: never write an artifact at import
    import json
    from casim.engine.particles._results_path import results_path

    res = run_all()
    path = results_path("F359_graviton_collapse_threshold.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(f"{res['n_pass']}/{res['n_total']} PASS -> {path}")
