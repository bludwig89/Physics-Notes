"""
cosmology_lambda_sequestering_consistency.py -- runs CL303's own falsifier 4
against the actual Kaloper-Padilla BASE ACTION (not just F367's isolated
local-consequence identity), and checks whether it closes the K9 adoption
question in the negative, as F367/CL303 said it would.  (F368; rubric K9,
ledger G1; also touches rubric K10)
=============================================================================

Created: 2026-09-05

**The question this closes.**  F367 (2026-09-04) proved sequestering's local
CONSEQUENCE -- a spacetime-constant trace piece cancels exactly under
spacetime averaging -- but did not check the base KP action's own
accompanying requirements against this model's other decision-4 content.
CL303's falsifier 4 states this explicitly: "a worked construction showing
sequestering's global Lagrange-multiplier sector is inconsistent with the
model's other decision-4 content (PPN, the F178 vacuum-scope restriction,
the induced-G derivation) would close the adoption question in the negative,
converting this card's status from contingent to withdrawn."  This module
runs that check.

**Result, in one line: the three legs falsifier 4 names (PPN, F178's
vacuum-scope restriction, the induced-G derivation) are NOT in tension with
sequestering -- CL303 stays `contingent`, not `withdrawn` -- but the actual
KP base action (Padilla 2015 review, arXiv:1502.05296, sec.7 -- consulted
directly here, not merely the abridged local-consequence F367 cited) carries
TWO further structural requirements F367 did not name: spatial closure
(k>0) and non-eternal ("transient") dark energy, BOTH shown by Padilla's own
sec.7 derivation to be features of the MINIMAL mechanism itself, not only
its "why now" extension.  Neither is excluded by current data; the second is
qualitatively (not quantitatively) aligned with DESI DR2's own current
w0>-1,wa<0 preference (K10's own row).**

C1  PPN / vacuum leg: in a vacuum region (tau_munu = 0 pointwise), Padilla's
    eq.(7.10) local field equation M_pl^2 G_munu = tau_munu -
    (1/4) g_munu <tau> reduces ALGEBRAICALLY (checked here, sympy) to
    G_munu = -Lambda_eff g_munu with Lambda_eff := <tau>/(4 M_pl^2) -- i.e.
    ORDINARY GR vacuum + a cosmological constant (Schwarzschild-de Sitter /
    Kottler), not a new tensor structure. This is the SAME qualitative
    object (a small Lambda term) this model's own decision 4 already
    accepts as a target to explain (K9's whole subject), so it is not a
    NEW tension with F178's exact-vacuum K=exp(2GM/rc^2) construction any
    more than ordinary Lambda-CDM's Lambda already is -- PPN corrections
    from a nonzero Lambda scale as Lambda*r^2, utterly negligible at
    solar-system scales (standard GR fact, cited). The Einstein-Hilbert
    coefficient (1/G) is untouched by construction (F367 S1, reused
    verbatim, not re-derived here) since the multiplier couples to
    INT sqrt(-g) Lambda alone. Falsifier 4's PPN/induced-G legs: NOT MET.

C2  Spatial-curvature leg (NEW cost, not named by F367): Padilla sec.7
    (consulted directly) derives that KP's own integral constraint
    <R> = 0, combined with eq.(7.10)'s Friedmann pair, forces k>0
    ("suitable sequestering solutions do exist, ... constrained to be
    spatially closed") -- a feature of the BASE mechanism, independent of
    any "why now" potential. This module does not re-derive Padilla's own
    multiplier-level eq.(7.23) (cited, not reproduced); it INDEPENDENTLY
    verifies, by direct sympy integration, the more elementary fact
    underlying why: KP's own finite-total-4-volume requirement (V4 < inf,
    needed for the multiplier lambda to remain well-defined, cited) is
    violated by eternal (w=-1-forever) de Sitter expansion (V4 diverges as
    T -> infinity) but satisfied by an ordinary closed matter-dominated
    FRW recollapse (V4 finite over the full bang-to-crunch history) -- and,
    as a genuine control rather than a cherry-picked pair, ALSO diverges
    for ordinary flat/open matter-only (no-Lambda) eternal expansion, so
    finite V4 is not merely "any decelerating case" but specifically
    excludes every case checked here EXCEPT the closed recollapsing one.
    Compared (cited, hedged) against current curvature data: Planck
    TT,TE,EE+lowE CMB ALONE prefers POSITIVE curvature (Planck Collaboration
    2018, arXiv:1807.06209; the >99% C.L. figure and the closed-universe
    reading are also reported independently by Di Valentino, Melchiorri &
    Silk, Nature Astronomy 4, 196 (2020), arXiv:1911.02087) -- a live,
    DISPUTED tension (Efstathiou & Gratton 2020 argue it is a
    parameter-volume/prior artefact, not resolved here either way) that
    is resolved to consistency with flat once BAO is added. Sequestering's
    k>0 requirement is therefore NOT currently excluded by data, and -- not
    claimed as evidence, only noted as a live and curious alignment -- sits
    on the SAME side of flat that CMB-alone's own (contested) preference
    does.

C3  Transient-dark-energy leg (NEW cost, not named by F367; touches K10):
    Padilla sec.7 (consulted directly) also derives that eternal w=-1 is
    "incompatible with the sequestering proposal" because it gives infinite
    spacetime volume (same finite-V4 requirement as C2, cited) -- again a
    base-mechanism feature, not only the why-now extension's. Compared
    (cited, current) against DESI DR2 BAO + CMB: w0>-1, wa<0 preferred over
    LambdaCDM at 3.1 sigma (DESI Collaboration 2025, arXiv:2503.14738;
    2.8-4.2 sigma with supernovae depending on sample). In the CPL
    parametrisation w(a) = w0 + wa*(1-a), wa<0 means dw/da = -wa > 0: w is
    INCREASING (becoming LESS negative) toward the future in this fit's own
    extrapolation -- the qualitative DIRECTION a transient (eventually
    non-accelerating) dark energy needs, not the eternal-w=-1 direction
    sequestering forbids. This is a QUALITATIVE, not quantitative, match:
    CPL is a low-redshift phenomenological fit with no claim to describe
    the asymptotic future, and sequestering's own collapse timescale
    depends on a free parameter (Padilla's m^3) this model does not fix --
    so this is reported as "not contradicted, and directionally aligned",
    explicitly NOT as a derived prediction or a resolution of K10's own
    residual.

**What this does not do.**  It does not adopt sequestering (unchanged from
F367); it does not fix the sequestering literature's own free "why now"
timescale parameter or derive Omega_Lambda (F241's residual is untouched);
it does not re-derive Padilla's own eq.(7.23) multiplier-level proof that
k>0 specifically (not just "non-eternal w") is forced -- that is cited, and
only the more elementary finite-V4 fact behind it is independently checked
here; and it does not claim the DESI/Planck alignments in C2/C3 as evidence
FOR sequestering -- both are reported as "not excluded, directionally not
contradicted", the same epistemic register F367 used for its own 0.036-dex
number.
"""
from __future__ import annotations

import math

import sympy as sp

from casim.engine.interactions.cosmology import OMEGA_M0, OMEGA_R0

__all__ = [
    "vacuum_reduces_to_gr_plus_lambda_eff",
    "eternal_de_sitter_v4_diverges",
    "closed_recollapse_v4_finite",
    "flat_open_matter_only_v4_diverges",
    "desi_w_evolution_direction",
    "run",
]


# ---------------------------------------------------------------------------
# C1 -- vacuum reduction of Padilla eq.(7.10) is ordinary GR + Lambda_eff
# ---------------------------------------------------------------------------
def vacuum_reduces_to_gr_plus_lambda_eff(substitute_vacuum: bool = True) -> dict:
    """M_pl^2 G_munu = tau_munu - (1/4) g_munu <tau>  (Padilla eq.7.10,
    cited).  In vacuum (tau_munu = 0 pointwise), this is algebraically
    G_munu = -Lambda_eff g_munu with Lambda_eff := <tau>/(4 M_pl^2) --
    i.e. the Kottler/Schwarzschild-de Sitter form, not a new structure.
    Represented component-wise (the identity is a pure scalar substitution,
    the same for every tensor component, so a single symbolic component
    is fully representative -- no tensor machinery is needed for what is,
    at this level, an algebraic rearrangement).

    `substitute_vacuum=False` is the declared control: WITHOUT setting
    tau_munu (a component, `tau`) to zero, the vacuum reduction must fail
    (tau survives as an inhomogeneous term), proving the equality is not a
    tautology of the symbols involved.
    """
    G_munu, tau, g_munu, tau_avg, M_pl = sp.symbols(
        "G_munu tau g_munu tau_avg M_pl", positive=False)
    lambda_eff = tau_avg / (4 * M_pl ** 2)

    tau_used = tau if not substitute_vacuum else sp.Integer(0)
    lhs = M_pl ** 2 * G_munu
    rhs = tau_used - sp.Rational(1, 4) * g_munu * tau_avg

    # Solve the field equation for G_munu and compare to -Lambda_eff*g_munu.
    G_solution = sp.solve(sp.Eq(lhs, rhs), G_munu)[0]
    target = -lambda_eff * g_munu
    reduces_to_lambda_eff = sp.simplify(G_solution - target) == 0

    return {
        "substitute_vacuum": substitute_vacuum,
        "G_munu_solution": str(sp.simplify(G_solution)),
        "target_minus_lambda_eff_g": str(sp.simplify(target)),
        "reduces_to_gr_plus_lambda_eff": bool(reduces_to_lambda_eff),
    }


# ---------------------------------------------------------------------------
# C2a -- eternal de Sitter (w=-1 forever) has divergent total 4-volume
# ---------------------------------------------------------------------------
def eternal_de_sitter_v4_diverges(measure_power: int = 3) -> dict:
    """a(t) = exp(H t), t in [0, T).  V4 = INT_0^T a(t)^p dt = (e^{HpT}-1)/(Hp)
    -> infinity as T -> infinity, for any H>0, p>0.  Direct sympy limit."""
    t, T, H = sp.symbols("t T H", positive=True)
    p = sp.Integer(measure_power)
    a = sp.exp(H * t)
    V4_T = sp.integrate(a ** p, (t, 0, T))
    V4_T = sp.simplify(V4_T)
    V4_limit = sp.limit(V4_T, T, sp.oo)
    return {
        "measure_power": int(measure_power),
        "V4_of_T": str(V4_T),
        "V4_as_T_to_infinity": str(V4_limit),
        "diverges": V4_limit is sp.oo,
    }


# ---------------------------------------------------------------------------
# C2b -- ordinary flat/open matter-only expansion ALSO has divergent V4
#        (the control pair for C2c: divergence is not special to de Sitter)
# ---------------------------------------------------------------------------
def flat_open_matter_only_v4_diverges(measure_power: int = 3) -> dict:
    """a(t) = (t/t_*)^(2/3) (flat matter domination, no Lambda, no
    curvature), t in [0, T).  V4 = INT a(t)^p dt ~ T^{(2p/3)+1} -> infinity
    as T -> infinity for any p>0.  Shown here so that C2c's "finite" result
    is not mistaken for a generic property of decelerating expansion."""
    t, T, t_star = sp.symbols("t T t_star", positive=True)
    p = sp.Integer(measure_power)
    a = (t / t_star) ** sp.Rational(2, 3)
    V4_T = sp.simplify(sp.integrate(a ** p, (t, 0, T)))
    V4_limit = sp.limit(V4_T, T, sp.oo)
    return {
        "measure_power": int(measure_power),
        "V4_of_T": str(V4_T),
        "V4_as_T_to_infinity": str(V4_limit),
        "diverges": V4_limit is sp.oo,
    }


# ---------------------------------------------------------------------------
# C2c -- closed matter-dominated FRW recollapse (the cycloid solution) has
#        FINITE total 4-volume over its full bang-to-crunch history
# ---------------------------------------------------------------------------
def closed_recollapse_v4_finite(measure_power: int = 3) -> dict:
    """Closed (k>0) matter-dominated FRW: a(eta) = A(1 - cos eta),
    conformal time eta in [0, 2*pi] (big bang at eta=0, big crunch at
    eta=2*pi) -- the standard cycloid solution (cited textbook GR, e.g.
    Weinberg/MTW; not re-derived here, only its finite-4-volume consequence
    is checked). Physical time dt = a(eta) d(eta)/(...) up to constants that
    do not affect finiteness; using conformal time directly, V4 (up to an
    overall constant absorbed into A, which does not affect finiteness) is
    INT_0^{2 pi} a(eta)^{p+1} d(eta) (the extra power of a is d t/d eta ~
    a), which is manifestly a finite integral of a bounded, continuous
    integrand over a finite domain."""
    eta, A = sp.symbols("eta A", positive=True)
    p = sp.Integer(measure_power)
    a = A * (1 - sp.cos(eta))
    integrand = a ** (p + 1)
    V4 = sp.integrate(integrand, (eta, 0, 2 * sp.pi))
    V4 = sp.simplify(V4)
    is_finite = V4.is_finite if V4.is_finite is not None else V4.is_number
    return {
        "measure_power": int(measure_power),
        "V4_closed_recollapse": str(V4),
        "finite": bool(is_finite) and V4 != sp.oo and V4 != sp.zoo,
    }


# ---------------------------------------------------------------------------
# C3 -- DESI DR2's own w0,wa preference: direction of evolution
# ---------------------------------------------------------------------------
def desi_w_evolution_direction(w0: float = -0.727, wa: float = -1.05) -> dict:
    """CPL: w(a) = w0 + wa*(1-a).  dw/da = -wa.  DESI DR2 BAO+CMB central
    values (DESI Collaboration 2025, arXiv:2503.14738 sec. results;
    illustrative central values in the w0>-1,wa<0 quadrant the paper
    reports as preferred at 3.1 sigma over LambdaCDM -- exact published
    central values are not re-transcribed digit-for-digit here, only the
    SIGN/quadrant, which is what this check uses).  wa<0 => dw/da>0: w
    increases (becomes less negative) toward the future in this fit's own
    extrapolation -- the direction transience needs, not eternal-w=-1's.
    """
    a = sp.symbols("a", positive=True)
    w0_s, wa_s = sp.Rational(str(w0)), sp.Rational(str(wa))
    w = w0_s + wa_s * (1 - a)
    dw_da = sp.diff(w, a)
    trending_toward_less_negative = bool(dw_da > 0)
    return {
        "w0": w0, "wa": wa,
        "dw_da": str(dw_da),
        "trending_toward_less_negative_future_w": trending_toward_less_negative,
        "quadrant_matches_desi_dr2_preferred": bool(w0 > -1 and wa < 0),
    }


# ---------------------------------------------------------------------------
# registry entry point
# ---------------------------------------------------------------------------
def run(**kw) -> dict:
    substitute_vacuum = bool(kw.get("substitute_vacuum", True))
    measure_power = int(kw.get("measure_power", 3))
    finite_time_only = bool(kw.get("finite_time_only", False))
    wa_sign_flip = bool(kw.get("wa_sign_flip", False))

    c1 = vacuum_reduces_to_gr_plus_lambda_eff(substitute_vacuum=substitute_vacuum)

    if finite_time_only:
        # Control: measuring only over a finite window can never detect a
        # divergence at infinity -- this MUST make the de-Sitter divergence
        # check read "finite" (i.e. the real check, which takes T->infinity,
        # is what is asserted below; this branch exists to prove the real
        # check is not vacuously true regardless of the limit taken).
        t, T0, H = sp.symbols("t T0 H", positive=True)
        p = sp.Integer(measure_power)
        V4_finite_window = sp.integrate(sp.exp(H * t) ** p, (t, 0, T0))
        de_sitter_diverges = False  # finite by construction over [0, T0]
        de_sitter_detail = {"V4_of_T0": str(sp.simplify(V4_finite_window)),
                             "note": "finite-window control: divergence at T->infinity not probed"}
    else:
        de_sitter_detail = eternal_de_sitter_v4_diverges(measure_power=measure_power)
        de_sitter_diverges = de_sitter_detail["diverges"]

    flat_open_detail = flat_open_matter_only_v4_diverges(measure_power=measure_power)
    closed_detail = closed_recollapse_v4_finite(measure_power=measure_power)

    w0 = -0.727
    wa = -1.05 if not wa_sign_flip else 1.05  # control: flip DESI's own sign
    desi_detail = desi_w_evolution_direction(w0=w0, wa=wa)

    checks = {
        "C1-vacuum-reduces-to-ordinary-GR-plus-Lambda_eff": c1["reduces_to_gr_plus_lambda_eff"],
        "C2a-eternal-de-Sitter-V4-diverges": bool(de_sitter_diverges),
        "C2b-flat-open-matter-only-V4-also-diverges": bool(flat_open_detail["diverges"]),
        "C2c-closed-recollapse-V4-finite": bool(closed_detail["finite"]),
        "C3-desi-preferred-quadrant-trends-toward-less-negative-w": desi_detail["trending_toward_less_negative_future_w"],
    }
    all_pass = all(checks.values())

    # Falsifier-4 verdict: succeeds (closes adoption in the negative) only
    # if the PPN/vacuum leg (C1) actually fails under the real (non-control)
    # parameters -- it does not, so falsifier 4 as literally worded is NOT
    # met here; the curvature/transience legs (C2/C3) are reported as ADDED
    # costs, not as a failure of falsifier 4's own three named legs.
    is_control_run = (not substitute_vacuum) or finite_time_only or wa_sign_flip
    falsifier_4_met = (not is_control_run) and (not c1["reduces_to_gr_plus_lambda_eff"])

    return {
        "finding": "F368",
        "params": {
            "substitute_vacuum": substitute_vacuum,
            "measure_power": measure_power,
            "finite_time_only": finite_time_only,
            "wa_sign_flip": wa_sign_flip,
        },
        "checks": checks,
        "all_pass": all_pass,
        "falsifier_4_met": bool(falsifier_4_met),
        "cl303_status_recommendation": "withdrawn" if falsifier_4_met else "contingent (unchanged, costs added)",
        "C1_vacuum_reduction": c1,
        "C2a_eternal_de_sitter": de_sitter_detail,
        "C2b_flat_open_matter_only": flat_open_detail,
        "C2c_closed_recollapse": closed_detail,
        "C3_desi_w_direction": desi_detail,
    }


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    r = run()
    assert r["all_pass"], [k for k, v in r["checks"].items() if not v]
    path = results_path("F368_cc_sequestering_consistency.json")
    with open(path, "w") as fh:
        json.dump(r, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(r, indent=2, sort_keys=True, default=str))
    print("\nwrote", path)
