"""
cosmology_horizon_thermodynamics.py -- F360

Re-derives the flat-FRW Friedmann pair from a Clausius-relation (Jacobson
1995 / Cai-Kim 2005 style) argument at the cosmological apparent horizon,
using only local horizon thermodynamics -- an Unruh-type temperature set by
the model's own light cone (F26/F180, c_lat=c_grav), an entropy S=A/4G with
the model's own INDUCED G (F79), and the Clausius relation dQ=TdS -- rather
than positing and solving the covariant field equation G_mu_nu=(8 pi G/c^4)
T_mu_nu (F178) with the model's stress-energy content as input (which is
what F182/F188 do, and what F284 re-reads ontologically without changing).

This module does two things, both sympy-exact:

  1. VERIFY_QUASISTATIC -- the standard (Cai-Kim) "quasi-static apparent
     horizon" derivation: with kappa ~= -1/r_A (the horizon radius treated
     as slowly varying over one Clausius step), dQ=TdS together with the
     continuity equation reproduces BOTH Friedmann equations exactly:
         Hdot = -4 pi G (rho+p)              (Friedmann II)
         H^2  = (8 pi G / 3) rho              (Friedmann I, on integration)

  2. QUANTIFY_APPROXIMATION -- the honest check this finding adds. This
     function does NOT hand-type the answer: it builds the EXACT (no
     quasi-static substitution) Hayward-Kodama Clausius relation, which is
     quadratic in Hdot, extracts the quadratic ("dropped") and linear
     ("kept") pieces via sp.Poly, evaluates their ratio at the leading-order
     (quasi-static) solution, substitutes Friedmann I + rho+p=(1+w)rho, and
     ASSERTS the result equals the closed form -3(1+w)/4 as a sympy
     equality (raises AssertionError if it does not -- this is the fix for
     the 2026-09-04 review's Attack-1 finding that the two quantities were
     previously computed side by side and never actually compared). The
     result: an O(1) number for radiation (w=1/3: ratio=-1) and matter
     (w=0: ratio=-3/4), vanishing only for a pure Lambda source (w=-1). So
     the "quasi-static" step is a *convention* that reproduces the
     Friedmann pair exactly, not a controlled small-parameter expansion.

Honest scope (see findings/F360-*.md sec. 5-6 for the full discussion):
  - The FRW symmetry ansatz (homogeneity/isotropy) is still external input,
    shared with the standard approach (and with F284's own reading) -- not
    a new gap this finding introduces or claims to close.
  - The Hayward-Kodama surface-gravity / Unruh-temperature construction and
    the coefficient 1/4 in S=A/4G are imported continuum semiclassical-
    gravity objects, not yet independently re-derived from this lattice's
    own microphysics -- the same kind of import F61 flagged for the R/4
    Lichnerowicz curvature coupling. F190/F355 track the still-open, and
    (as of F355, same day) actively DISAGREEING, lattice-native attempt to
    pin the S=A/4G coefficient from BCC microstates.
  - An attempt at the fully exact "unified first law" (Misner-Sharp energy
    + work density W=(rho-p)/2, which the literature presents as removing
    the quasi-static step) produced sign/consistency inconsistencies in
    this session's own reconstruction that could not be resolved with
    confidence; it is NOT included here as a verified result. NOTE
    (2026-09-04 review): a SIMPLER exact-kappa route (still Clausius-only,
    not the full Misner-Sharp unified first law) *does* close cleanly and
    is what QUANTIFY_APPROXIMATION below implements; the harder Misner-
    Sharp/work-term construction remains unresolved and unattempted here.

Self-contained: sympy only.
"""

from __future__ import annotations

import sympy as sp


def _build_symbols():
    t = sp.symbols("t", real=True)
    G = sp.symbols("G", positive=True)
    H = sp.Function("H", positive=True)(t)
    rho = sp.Function("rho", positive=True)(t)
    p = sp.Function("p", real=True)(t)
    Hdot = sp.symbols("Hdot")
    return t, G, H, rho, p, Hdot


def verify_quasistatic() -> dict:
    """Cai-Kim quasi-static derivation: dQ=TdS + continuity => Friedmann I & II, exactly."""
    t, G, H, rho, p, Hdot = _build_symbols()
    rhodot = sp.symbols("rhodot")

    r_A = 1 / H
    r_A_dot = sp.diff(r_A, t)

    # quasi-static surface gravity / temperature (horizon radius slowly varying)
    kappa_qs = -1 / r_A
    T_qs = -kappa_qs / (2 * sp.pi)

    A_area = 4 * sp.pi * r_A ** 2
    S = A_area / (4 * G)
    dS_dt = sp.diff(S, t)

    dQ_dt = 4 * sp.pi * r_A ** 3 * H * (rho + p)  # energy flux through the horizon

    residual = sp.simplify(dQ_dt - T_qs * dS_dt)
    residual = residual.subs(sp.Derivative(H, t), Hdot)
    residual = sp.simplify(residual)

    Hdot_sol = sp.solve(sp.Eq(residual, 0), Hdot)
    Hdot_target = -4 * sp.pi * G * (rho + p)
    friedmann_II_match = bool(sp.simplify(Hdot_sol[0] - Hdot_target) == 0)

    # integrate via continuity: rhodot = -3H(rho+p) => (rho+p) = -rhodot/(3H)
    Hdot_via_continuity = -4 * sp.pi * G * (-rhodot / (3 * H))
    dH2_dt = sp.simplify(2 * H * Hdot_via_continuity)
    dH2_dt_target = sp.Rational(8, 3) * sp.pi * G * rhodot
    friedmann_I_rate_match = bool(sp.simplify(dH2_dt - dH2_dt_target) == 0)

    return {
        "residual_after_quasistatic": str(residual),
        "Hdot_solutions": [str(s) for s in Hdot_sol],
        "friedmann_II_exact_match": friedmann_II_match,
        "dH2_dt_matches_8piG_over_3_rhodot": friedmann_I_rate_match,
        "conclusion": (
            "H^2 = (8 pi G/3) rho recovered on integration with H->0 as rho->0"
            if friedmann_II_match and friedmann_I_rate_match
            else "MISMATCH -- derivation does not close"
        ),
    }


def quantify_approximation() -> dict:
    """Size of the term the quasi-static convention drops, derived (not hand-typed).

    Builds the EXACT Hayward-Kodama Clausius relation (no kappa~=-1/r_A
    substitution), which is quadratic in Hdot. Extracts the quadratic
    ("dropped") and linear ("kept") coefficients via sp.Poly, forms their
    ratio at the leading-order (quasi-static) solution, substitutes
    Friedmann I (H^2=8 pi G rho/3) and rho+p=(1+w)rho, and ASSERTS -- as a
    sympy equality, not an eyeballed comparison -- that the result is
    exactly -3(1+w)/4. Raises AssertionError if a future edit breaks the
    identity (2026-09-04 review fix: the two quantities were previously
    computed side by side and never compared).
    """
    t, G, H, rho, p, Hdot = _build_symbols()
    w, rho_s = sp.symbols("w rho_s", real=True)

    r_A = 1 / H
    r_A_dot = sp.diff(r_A, t)
    kappa_exact = -(1 / r_A) * (1 - r_A_dot / (2 * H * r_A))
    T_exact = -kappa_exact / (2 * sp.pi)  # same sign convention as verify_quasistatic's T_qs

    A_area = 4 * sp.pi * r_A ** 2
    S = A_area / (4 * G)
    dS_dt = sp.diff(S, t)
    dQ_dt = 4 * sp.pi * r_A ** 3 * H * (rho + p)

    residual_exact = sp.simplify(dQ_dt - T_exact * dS_dt)
    residual_exact = residual_exact.subs(sp.Derivative(H, t), Hdot)
    num, _den = sp.fraction(sp.together(sp.simplify(residual_exact)))
    num = sp.expand(num)

    poly = sp.Poly(num, Hdot)
    c2, c1, c0 = poly.all_coeffs()
    c1n = sp.simplify(c1 / H ** 2)
    c0n = sp.simplify(c0 / H ** 2)
    Hdot0 = sp.simplify(-c0n / c1n)  # leading-order (quasi-static) solution

    friedmann_II_cross_check = bool(sp.simplify(Hdot0 - (-4 * sp.pi * G * (rho + p))) == 0)

    dropped_term = sp.simplify(c2 * Hdot0 ** 2 / H ** 2)
    kept_term = sp.simplify(c1n * Hdot0)
    ratio_general = sp.simplify(dropped_term / kept_term)

    ratio_onshell = ratio_general.subs(rho, rho_s).subs(p, w * rho_s)
    ratio_onshell = ratio_onshell.subs(H ** 2, sp.Rational(8, 3) * sp.pi * G * rho_s)
    ratio_onshell = sp.simplify(ratio_onshell)

    ratio_closed_form = -sp.Rational(3, 4) * (1 + w)
    identity_holds = bool(sp.simplify(ratio_onshell - ratio_closed_form) == 0)
    assert identity_holds, (
        f"quasi-static drop-ratio derivation broke: got {ratio_onshell}, "
        f"expected {ratio_closed_form}"
    )

    cases = {}
    for label, w_val in (("radiation", sp.Rational(1, 3)), ("matter", sp.Integer(0)), ("lambda", sp.Integer(-1))):
        val = ratio_closed_form.subs(w, w_val)
        cases[label] = {
            "w": str(w_val),
            "ratio": str(val),
            "ratio_float": float(val),
            "is_O1_not_small": bool(abs(float(val)) >= sp.Rational(1, 10)),
        }

    return {
        "friedmann_II_cross_check_from_exact_kappa": friedmann_II_cross_check,
        "ratio_derived_onshell": str(ratio_onshell),
        "ratio_closed_form_claimed": str(ratio_closed_form),
        "identity_verified": identity_holds,
        "cases": cases,
        "conclusion": (
            "the quasi-static approximation drops an O(1) term for radiation and "
            "matter (ratio -1 and -3/4 respectively); it vanishes only for a pure "
            "cosmological-constant source (w=-1). This is a CONVENTION that "
            "reproduces the Friedmann pair exactly, not a small-parameter expansion. "
            "The ratio is DERIVED here from the exact Hayward-Kodama residual, not "
            "hand-typed (2026-09-04 review fix)."
        ),
    }


def run_all() -> dict:
    qs = verify_quasistatic()
    approx = quantify_approximation()
    all_pass = bool(
        qs["friedmann_II_exact_match"]
        and qs["dH2_dt_matches_8piG_over_3_rhodot"]
        and approx["friedmann_II_cross_check_from_exact_kappa"]
        and approx["identity_verified"]
        and approx["cases"]["radiation"]["is_O1_not_small"]
        and approx["cases"]["matter"]["is_O1_not_small"]
    )
    return {
        "quasistatic_derivation": qs,
        "approximation_size": approx,
        "all_pass": all_pass,
    }


if __name__ == "__main__":             # guard: never write an artifact at import
    import json
    from casim.engine.particles._results_path import results_path

    result = run_all()
    path = results_path("F360_horizon_thermodynamics.json")
    with open(path, "w") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))
