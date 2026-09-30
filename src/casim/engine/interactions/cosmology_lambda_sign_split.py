"""
cosmology_lambda_sign_split.py -- the a0/a1 SIGN SPLIT of the model's one
all-fermion heat-kernel sum, and what it does to the live cosmological-
constant route (F408; rubric K9, ledger G1)
=============================================================================

Created: 2026-09-27

**The question.**  The live K9/G1 route is "F193 sec.B + F196": the F183/F190
capacity ceiling rho <= 3c^4/(8 pi G L^2), read at L = R_H.  The tree quotes
the two as ONE route.  But F193 sec.B writes the residual as the bare
zero-point density DILUTED, rho_vac*(a/R_H)^2 (an a0 object), while F196
writes it as 3c^4/(8 pi G R_H^2) (built from G, i.e. an a1 object).  F164
fixes the sign of a0 as NEGATIVE (all-fermion vacuum, no fundamental
bosons); F61 fixes the sign of a1 as POSITIVE (Lichnerowicz R/4 flips the
spinor trace, the fermion determinant flips it back).  F193 line 88's reason
why the sign problem "is not in tension" -- "there is no negative beable
tower" -- is Part A, which CL275 EXCLUDED on 2026-08-18.  Nothing since has
re-checked the sign.  This module does.

Legs (one function each):

S1  Sign split, EXACT (Fraction arithmetic over the model's own content):
    per 2-component Weyl field, a0 (zero-point) carries statistics sign
    s=-1 times 2 dof; a1/R carries s * (1/2) * 4 * (1/6 - E_L) with E_L = 1/4
    the Lichnerowicz coefficient -> +1/6, i.e. eta = +1/12 (F61).  Summed
    over the model's 48 Weyl fields and ZERO fundamental bosons, a0 < 0 and
    a1 > 0: sign(a0)*sign(a1) = -1.  DECLARED INPUTS: (i) the continuum
    Lichnerowicz E = R/4 (F61 imports it); (ii) every gauge boson is
    composite (decision 5, F67-F69, F164 Part B) -- a fundamental massless
    vector with ghosts contributes c = -2/3 = -4 scalar units, so 48 Weyl +
    12 fundamental vectors would give sum(eta) = 0 exactly and no induced
    1/G at this order (lever `fundamental_vectors`); (iii) the principal
    quasi-energy branch with a filled negative sea for the a0 sign (on the
    [0, 2 pi) branch of a unitary QCA the lower band is not negative).
    Levers: `lichnerowicz_E=0` flips a1; `fundamental_bosons` (a scalar tower
    larger than the 96 fermionic dof) flips a0; `fundamental_vectors=12`
    zeroes a1.

S2  The two "halves" of the live route are different objects, EXACT +
    MACHINE, with the SAME field content in both moments:
    sign(a0 term) = -1, sign(F196) = sign(G) = sign(a1) = +1, and
        |a0 term| (a/R_H)^2 / (3c^4/8 pi G R_H^2) = 4 N_b I_cc / (3 sum eta)
    (N_b = |a0| in half-hbar-omega branches, the cell a = sqrt(2 pi sum eta)
    3^(1/4) ell_P from F59/F79).  For the model (N_b = 96, sum eta = 4, which
    IS the registered canonical cell, checked) this is 32 I_cc = 24 sqrt3 pi
    = 130.59 (2.12 dex), independent of the field count.  F193 sec.B as
    written used g*=2 branches against a G calibrated at 48 Weyl fields and
    got sqrt3 pi/2 = 2.72 -- a content mismatch (its 0.09% proximity to e is
    an artifact of the mismatch), reported but not a result.  Numerics on
    the tree's own `sakharov_moments` grid (n even) with the structural G:
    machine precision.  Lever `zero_point_weight` breaks the ratio leg alone.

S3  The capacity ceiling cannot act on a negative a0, EXACT (sympy) but
    ELEMENTARY -- a one-sided upper bound cannot raise or cancel a negative
    term (a negative a0 satisfies the bound for every L); with positive matter
    present the bound applies to the TOTAL density and says nothing about a0:
    (a) the Schwarzschild saturation 2 G m(L)/(L c^2) = 1 with
        m = (4 pi/3) rho L^3 has NO positive root L when rho < 0 (and
        exactly one, L = c sqrt(3/(8 pi G rho)), when rho > 0);
    (b) flat Friedmann-I H^2 = 8 pi G rho/3 has NO real H when rho < 0, so
        there is no de Sitter horizon and F196 Route 2 (Bekenstein count x
        Gibbons-Hawking T = hbar H/2 pi) has nothing to count.
    The ceiling constrains positive gravitating energy only.  The F164 sum,
    being negative, is not "made to respect it" -- it is outside its domain.

S4  The positive a1 side IS confinement-shaped, EXACT (sympy): the capacity
    energy of a region E(L) = rho_ceiling(L) * (4 pi/3) L^3 = c^4 L/(2G) is
    LINEAR in L (d2E/dL2 = 0), a string tension
        sigma_H = c^4/(2G) = 4 pi sqrt3 hbar c / a^2
    (structural G), whose sign is sign(a1).  Same form as F86's BPS
    V(R) = sigma R with sigma = 2 pi v^2 n set by the condensate stiffness.
    F332 K1 already showed this ceiling IS Friedmann-I at L = R_H, so this is
    a reading of the geometric side, not a new source.

S5  The only non-local a0-remover the tree has built is sign-blind, EXACT
    (sympy) -- this is the Kaloper-Padilla mechanism's defining property,
    re-checked, not a new result: the
    F367 Kaloper-Padilla subtraction T(t0) - <T> is independent of an
    additive constant C with C a REAL symbol of either sign (F367 declared C
    positive; this re-derives with C real and evaluates C = +X vs -X).
    Control lever `sequester` (False) evaluates raw T(t0) and must red it.

Net for G1: a0 removal needs a sign-blind mechanism (S3: the ceiling cannot
do it; S5: F367's can -- as can a finite bare-Lambda counterterm, which is a
fit, not a mechanism); the positive, correctly signed a1 horizon term sets
the ceiling/scale rho_crit (by F332 K1 it IS Friedmann-I, not a source);
Omega_Lambda (F241) is unchanged.
"""
from __future__ import annotations

import math
from fractions import Fraction

import sympy as sp

from casim.constants import G_CODATA, a_over_ellP, c_SI, ell_P_m, hbar_SI
from casim.engine.interactions.cosmology import H0_KM_S_MPC, MPC_KM
from casim.engine.interactions.qed_uv_completion import sakharov_moments

__all__ = [
    "model_weyl_content",
    "heat_kernel_signs",
    "route_halves",
    "ceiling_domain",
    "capacity_tension",
    "sequestering_sign_blind",
    "run",
]

# The first-generation 2-component Weyl content F61 Part B counts (Higgs-free
# SU(2), with the F47 sterile nu_R), per generation; three generations.
_WEYL_PER_GENERATION = {"L": 2, "e_R": 1, "Q": 6, "u_R": 3, "d_R": 3, "nu_R": 1}
_GENERATIONS = 3


def model_weyl_content() -> int:
    """g* = number of gravitating 2-component Weyl fields (F61: 48)."""
    return _GENERATIONS * sum(_WEYL_PER_GENERATION.values())


# ---------------------------------------------------------------------------
# S1 -- exact sign split of the two heat-kernel moments
# ---------------------------------------------------------------------------
def heat_kernel_signs(lichnerowicz_E: Fraction = Fraction(1, 4),
                      fundamental_bosons: int = 0,
                      fundamental_vectors: int = 0) -> dict:
    """Statistics-signed a0 and a1 coefficients summed over the model content.

    Conventions (F59/F61): a Laplace-type operator -Box + E on a bundle of
    rank r has a1/R = r/6 - trE/R.  A real minimal scalar: r=1, E=0,
    statistics +1, one real dof.  A Dirac field: r=4, E = R/4 (Lichnerowicz),
    statistics -1; a 2-component Weyl field is half a Dirac.  The
    statistics-signed a1 per field, c = s * a1/R, sources +1/16 pi G with
    eta = c/2 (F61).  a0 is the zero-point count: s times the number of
    real propagating dof (Weyl: 2, scalar: 1).

    A massless gauge VECTOR with its two Faddeev-Popov ghosts: r=4,
    E = -Ricci (tr E = -R), so a1/R = 4/6 - (-1)... written out:
    vector 4/6 + (-1) -> -1/3, minus two ghost scalars 2*(1/6) -> -2/3,
    statistics +1: c_vector = -2/3 = -4 scalar units; a0: 2 physical dof.
    The model has NO fundamental vectors (every gauge boson is composite,
    decision 5 / F67-F69 / F164 Part B) -- that is a DECLARED INPUT of the
    a1 sign: 48 Weyl + 12 fundamental vectors would give sum(eta) = 0."""
    g_star = model_weyl_content()
    s_f, s_b = -1, +1
    weyl_rank_half = Fraction(4, 2)                 # half the Dirac rank
    c_weyl = s_f * weyl_rank_half * (Fraction(1, 6) - lichnerowicz_E)
    c_scalar = s_b * Fraction(1, 6)
    c_vector = s_b * (Fraction(4, 6) - 1 - 2 * Fraction(1, 6))
    a0_weyl, a0_scalar, a0_vector = s_f * 2, s_b * 1, s_b * 2

    a0_total = (g_star * a0_weyl + fundamental_bosons * a0_scalar
                + fundamental_vectors * a0_vector)
    c_total = (g_star * c_weyl + fundamental_bosons * c_scalar
               + fundamental_vectors * c_vector)
    eta_total = c_total / 2                          # sum of eta_i (F61)

    sign = lambda x: (x > 0) - (x < 0)
    return {
        "g_star_weyl": g_star,
        "fundamental_bosons": fundamental_bosons,
        "fundamental_vectors": fundamental_vectors,
        "c_vector": str(c_vector),
        "lichnerowicz_E": str(lichnerowicz_E),
        "c_weyl": str(c_weyl),
        "eta_weyl": str(c_weyl / 2),
        "a0_total_dof_signed": a0_total,
        "c_total": str(c_total),
        "eta_total": str(eta_total),
        "sign_a0": sign(a0_total),
        "sign_a1": sign(c_total),
        "sign_product": sign(a0_total) * sign(c_total),
    }


# ---------------------------------------------------------------------------
# S2 -- F193 sec.B vs F196: sign and H0-free closed-form ratio
# ---------------------------------------------------------------------------
def route_halves(sign_a0: int, sign_a1: int, n_branches: int, eta_total: Fraction,
                 zero_point_weight: float = 1.0, n: int = 64,
                 g_star_F193: int = 2) -> dict:
    """Evaluate both halves of the "one" live route at L = R_H, with the SAME
    field content in both moments.

    n_branches = |a0| in half-hbar-omega units (S1: 2 per Weyl field, 96 for
    the model) is what multiplies F164's per-branch density
    sqrt3 I_cc hbar c/a^4 (F164 wrote g*=2, "two BCC Weyl branches" = ONE
    Weyl field).  eta_total = sum(eta_i) (S1: 4) is what fixes the cell,
    a = sqrt(2 pi eta_total) 3^(1/4) ell_P (F59/F79; the registered canonical
    a/ell_P = sqrt(8 pi) 3^(1/4) IS eta_total = 4, checked here).  Then
        |a0 term| (a/R_H)^2 / (3c^4/8piG R_H^2) = 4 n_branches I_cc / (3 eta_total)
    which for 48 Weyl fields (n_branches = 2 g, eta_total = g/12) is
    32 I_cc = 24 sqrt3 pi = 130.59, INDEPENDENT of the field count.

    F193 as written (g*=2 in rho_vac, structural G calibrated at 48 Weyl)
    gives sqrt3 pi/2 = 2.72 -- a content mismatch, reported, not a result.
    n must be even so the q->q+pi pairing makes <omega> = pi/2 node-by-node."""
    a = a_over_ellP * ell_P_m
    H0 = H0_KM_S_MPC / MPC_KM
    R_H = c_SI / H0

    I_cc, _I_g = sakharov_moments(n=n)
    I_cc_exact = 3.0 * math.sqrt(3.0) * math.pi / 4.0    # 3 sqrt3 * <omega>/2
    eta_f = float(eta_total)
    # the canonical cell and the content must agree: (a/ell_P)^2 = 2 pi eta sqrt3
    cell_content_residual = abs(a_over_ellP**2 / (2.0 * math.pi * eta_f * math.sqrt(3.0)) - 1.0) \
        if eta_f > 0 else float("inf")

    branch_density = math.sqrt(3.0) * I_cc * hbar_SI * c_SI / a**4   # per half-hbar-omega branch
    rho_vac_mag = zero_point_weight * n_branches * branch_density
    rho_193B = sign_a0 * rho_vac_mag * (a / R_H) ** 2
    # G's sign is a1's sign (F79: 1/G IS the a1 sum; no bare kinetic term).
    # Magnitude: the decision-4 structural G = a^2 c^3 / (8 pi sqrt3 hbar).
    G_struct = a**2 * c_SI**3 / (8.0 * math.pi * math.sqrt(3.0) * hbar_SI)
    if sign_a1 == 0:
        rho_196 = float("nan")        # no induced 1/G at this order: no ceiling
        ratio_num = float("nan")
    else:
        rho_196 = 3.0 * c_SI**4 / (8.0 * math.pi * sign_a1 * G_struct * R_H**2)
        ratio_num = abs(rho_193B) / abs(rho_196)
    ratio_closed = (4.0 * n_branches * I_cc_exact / (3.0 * eta_f)) if eta_f else float("nan")
    ratio_model = 24.0 * math.sqrt(3.0) * math.pi

    # exact symbolic reduction with the content-derived cell
    Nb, eta, Icc, lP, c_s, hb, RH = sp.symbols("N_b eta I_cc ell_P c hbar R_H", positive=True)
    a_sym = sp.sqrt(2 * sp.pi * eta) * sp.root(3, 4) * lP
    G_sym = lP**2 * c_s**3 / hb
    rho_v = Nb * sp.sqrt(3) * Icc * hb * c_s / a_sym**4
    ratio_sym = sp.simplify((rho_v * (a_sym / RH) ** 2)
                            / (3 * c_s**4 / (8 * sp.pi * G_sym * RH**2)))
    ratio_sym_ok = sp.simplify(ratio_sym - 4 * Nb * Icc / (3 * eta)) == 0
    # content-independence: N_b = 2g, eta = g/12  ->  32 I_cc, no g
    g = sp.Symbol("g", positive=True)
    ratio_model_sym = sp.simplify(ratio_sym.subs({Nb: 2 * g, eta: g / 12}))
    ratio_model_sym_ok = sp.simplify(ratio_model_sym - 32 * Icc) == 0

    # what F193 section B wrote: g*=2 branches against the 48-Weyl structural G
    rho_193B_as_written = rho_vac_mag / n_branches * g_star_F193 * (a / R_H) ** 2 \
        if n_branches else float("nan")
    ratio_as_written = rho_193B_as_written / abs(rho_196) if sign_a1 else float("nan")

    return {
        "n_branches": n_branches,
        "eta_total": str(eta_total),
        "R_H_m": R_H,
        "G_structural_over_CODATA_minus_1": G_struct / G_CODATA - 1.0,
        "cell_content_residual": cell_content_residual,
        "I_cc_grid": I_cc,
        "I_cc_closed_form_3sqrt3pi_over_4": I_cc_exact,
        "I_cc_residual": abs(I_cc - I_cc_exact),
        "rho_a0_term_signed_J_per_m3": rho_193B,
        "rho_F196_signed_J_per_m3": rho_196,
        "ratio_numeric": ratio_num,
        "ratio_closed_form_4Nb_Icc_over_3eta": ratio_closed,
        "ratio_model_24sqrt3pi": ratio_model,
        "ratio_model_dex": math.log10(ratio_model),
        "ratio_residual": (abs(ratio_num - ratio_closed) / ratio_closed) if ratio_closed == ratio_closed and ratio_num == ratio_num else float("inf"),
        "ratio_symbolic": str(ratio_sym),
        "ratio_symbolic_ok": bool(ratio_sym_ok),
        "ratio_content_independent": bool(ratio_model_sym_ok),
        "F193B_as_written_g2_J_per_m3": rho_193B_as_written,
        "F193B_as_written_over_F196": ratio_as_written,
        "F193B_as_written_note": "g*=2 in rho_vac against a G calibrated at 48 Weyl fields: "
                                 "content mismatch; sqrt3 pi/2 ~ e is an artifact of it",
    }


# ---------------------------------------------------------------------------
# S3 -- the ceiling's domain is positive energy
# ---------------------------------------------------------------------------
def ceiling_domain(sign_a0: int) -> dict:
    L, G, c, X = sp.symbols("L G c X", positive=True)
    rho = sign_a0 * X                                   # |rho| = X > 0
    m = sp.Rational(4, 3) * sp.pi * rho * L**3
    saturation = sp.Eq(2 * G * m / (L * c**2), 1)
    roots = [r for r in sp.solve(saturation, L) if r.is_positive]
    H2 = 8 * sp.pi * G * rho / 3                        # flat Friedmann-I (units c=1 in rho)
    H_real = sp.ask(sp.Q.nonnegative(H2))              # True / False / None
    return {
        "sign_a0": sign_a0,
        "saturation_positive_roots": [str(r) for r in roots],
        "has_saturation_root": len(roots) > 0,
        "H_squared": str(H2),
        "real_hubble_horizon": H_real,
        "note": "elementary: a one-sided upper bound cannot raise or cancel a negative "
                "term; a negative a0 satisfies rho <= 3c^4/8piGL^2 for every L. Flat slicing "
                "(F182) assumed for the H^2 < 0 statement.",
    }


# ---------------------------------------------------------------------------
# S4 -- the a1 capacity energy is a linear (string-like) tension
# ---------------------------------------------------------------------------
def capacity_tension(sign_a1: int) -> dict:
    L, a_s, c_s, hb = sp.symbols("L a c hbar", positive=True)
    G = sign_a1 * a_s**2 * c_s**3 / (8 * sp.pi * sp.sqrt(3) * hb)
    rho_ceiling = 3 * c_s**4 / (8 * sp.pi * G * L**2)
    E = sp.simplify(rho_ceiling * sp.Rational(4, 3) * sp.pi * L**3)
    sigma = sp.simplify(sp.diff(E, L))
    curvature = sp.simplify(sp.diff(E, L, 2))
    sigma_closed = sign_a1 * 4 * sp.pi * sp.sqrt(3) * hb * c_s / a_s**2
    a = a_over_ellP * ell_P_m
    sigma_SI = float(sigma.subs({a_s: a, c_s: c_SI, hb: hbar_SI}))
    return {
        "E_of_L": str(E),
        "sigma_H": str(sigma),
        "d2E_dL2": str(curvature),
        "linear_in_L": curvature == 0,
        "sigma_matches_4pi_sqrt3_hbar_c_over_a2": sp.simplify(sigma - sigma_closed) == 0,
        "sigma_positive": bool(sigma.subs({a_s: 1, c_s: 1, hb: 1}) > 0),
        "sigma_H_N": sigma_SI,
        "sigma_H_c4_over_2G_CODATA_N": c_SI**4 / (2.0 * G_CODATA),
    }


# ---------------------------------------------------------------------------
# S5 -- the F367 subtraction does not care about the sign of the constant
# ---------------------------------------------------------------------------
def sequestering_sign_blind(sequester: bool = True) -> dict:
    t, t0, rho_m0, X = sp.symbols("t t0 rho_m0 X", positive=True)
    C = sp.Symbol("C", real=True)                       # EITHER sign
    n = sp.Rational(2, 3)
    a = (t / t0) ** n
    T = -rho_m0 * a ** -3 - C
    w = a**3                                            # sqrt(-g) FRW measure
    T_now = T.subs(t, t0)
    if sequester:
        T_avg = sp.integrate(w * T, (t, 0, t0)) / sp.integrate(w, (t, 0, t0))
        residual = sp.simplify(T_now - T_avg)
    else:
        residual = sp.simplify(T_now)
    d_dC = sp.simplify(sp.diff(residual, C))
    plus_minus = sp.simplify(residual.subs(C, X) - residual.subs(C, -X))
    return {
        "sequester": sequester,
        "residual": str(residual),
        "d_residual_dC": str(d_dC),
        "C_of_either_sign_drops_out": d_dC == 0 and plus_minus == 0,
    }


# ---------------------------------------------------------------------------
# registry entry point
# ---------------------------------------------------------------------------
def run(**kw) -> dict:
    E_L = Fraction(str(kw.get("lichnerowicz_E", "1/4")))
    bosons = int(kw.get("fundamental_bosons", 0))
    vectors = int(kw.get("fundamental_vectors", 0))
    zpw = float(kw.get("zero_point_weight", 1.0))
    sq = kw.get("sequester", True)
    sequester = sq if isinstance(sq, bool) else str(sq).strip().lower() not in ("false", "0", "no", "")

    s1 = heat_kernel_signs(lichnerowicz_E=E_L, fundamental_bosons=bosons,
                           fundamental_vectors=vectors)
    s2 = route_halves(s1["sign_a0"], s1["sign_a1"],
                      n_branches=abs(s1["a0_total_dof_signed"]),
                      eta_total=Fraction(s1["eta_total"]), zero_point_weight=zpw)
    s3 = ceiling_domain(s1["sign_a0"])
    s4 = capacity_tension(s1["sign_a1"])
    s5 = sequestering_sign_blind(sequester=sequester)

    checks = {
        "S1-a0-negative": s1["sign_a0"] < 0,
        "S1-a1-positive": s1["sign_a1"] > 0,
        "S1-eta-is-gstar-over-12": Fraction(s1["eta_total"]) == Fraction(s1["g_star_weyl"], 12),
        "S1-sign-split": s1["sign_product"] == -1,
        "S2-cell-matches-content": s2["cell_content_residual"] < 1e-12,
        "S2-F193B-negative": s2["rho_a0_term_signed_J_per_m3"] < 0,
        "S2-F196-positive": s2["rho_F196_signed_J_per_m3"] > 0,
        "S2-ratio-closed-form": (s2["ratio_symbolic_ok"] and s2["ratio_content_independent"]
                                 and s2["I_cc_residual"] < 1e-12
                                 and s2["ratio_residual"] < 1e-12),
        "S3-no-saturation-for-a0": not s3["has_saturation_root"],
        "S3-no-horizon-for-a0": s3["real_hubble_horizon"] is False,
        "S4-linear-tension": bool(s4["linear_in_L"] and s4["sigma_matches_4pi_sqrt3_hbar_c_over_a2"]),
        "S4-tension-positive": s4["sigma_positive"],
        "S5-sequestering-sign-blind": bool(s5["C_of_either_sign_drops_out"]),
    }
    return {
        "finding": "F408",
        "params": {"lichnerowicz_E": str(E_L), "fundamental_bosons": bosons,
                   "fundamental_vectors": vectors,
                   "zero_point_weight": zpw, "sequester": sequester},
        "checks": checks,
        "all_pass": all(checks.values()),
        "S1_heat_kernel_signs": s1,
        "S2_route_halves": s2,
        "S3_ceiling_domain": s3,
        "S4_capacity_tension": s4,
        "S5_sequestering_sign_blind": s5,
    }


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    r = run()
    assert r["all_pass"], [k for k, v in r["checks"].items() if not v]
    path = results_path("F408_cc_sign_split.json")
    with open(path, "w") as fh:
        json.dump(r, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(r["checks"], indent=2))
    print("\nwrote", path)
