"""gravity_core_completeness.py -- geodesic completeness of the lattice-regulated
black-hole core, and a no-go on the point-group route to it  (rubric row E10).
===============================================================================

**The residual this closes.**  F183 SS L1 established that the Schwarzschild
Kretschmann scalar meets the BCC cell scale ``1/a^4`` at a finite radius, so
curvature *saturates*.  That is a statement about an invariant, not about
worldlines, and the gap is real: bounded curvature does **not** imply geodesic
completeness (Zhou & Modesto, PRD **107** 044016, arXiv:2208.02557, exhibit
regular black holes with everywhere-bounded curvature that are geodesically
incomplete -- the analytically extended Hayward metric among them).

**What this module proves, and what it refutes.**

  THE RESULT (B1).  For the general TWO-function static spherically symmetric
  metric ``ds^2 = -A dt^2 + dr^2/B + r^2 dOmega^2``, the Kretschmann scalar is an
  exact **sum of squares** of orthonormal-frame Riemann components:

      K = 4 R_trtr^2 + 8 R_thth^2 + 8 R_rthrth^2 + 4 R_thphthph^2
      R_thphthph = (1-B)/r^2 ,  R_rthrth = -B'/(2r) ,  R_tththt = B A'/(2 r A)

  A global bound ``K <= 1/a^4`` therefore bounds **each term separately**, which
  forces ``B(0) = 1`` (no mass / solid-angle defect), ``B'(0) = 0`` and
  ``A'(0) = 0``: the metric is ``eta_uv + O(r^2)`` in Cartesian coordinates, i.e.
  ``C^{1,1}`` and Lorentzian, and the centre is an interior point of the
  manifold rather than a boundary.  At ``C^{1,1}`` geodesics exist and are unique
  (Chruskiel-Grant), so radial and null geodesics pass **through** the centre.

  This uses ONLY the curvature bound.  No parity, no point group, no saturation,
  no ``A = B``.  It holds in the two-function class F178/F181 say the interior
  actually requires -- where a one-function (``AB = 1``) representative such as
  Bardeen does not belong.  **This is the E10 result.**

  THE NO-GO (B2).  An earlier draft of this finding claimed the stronger and
  more attractive result that the BCC site group *forces* the parity condition
  Hayward-class metrics fail, because ``-1 in O_h``.  **That claim is false, and
  this module now records why**, because a closed elegant route is worth more on
  the record than quietly dropped:

    (i)  NOT SUFFICIENT.  Hayward's own density
         ``rho = 3ML^3/(4 pi (L^3+r^3)^2) = 3M/(4 pi L^3) - (3M/2 pi L^6) r^3 + ...``
         is a function of ``r`` alone, hence invariant under all of O(3) and so
         under ``O_h`` and ``-1`` -- yet it carries an **odd r^3 term**, ``m(r)``
         is not odd, ``f`` is not even, and the spacetime is ZM-incomplete.
         The reason: ``r^(2k+1) = (x^2+y^2+z^2)^((2k+1)/2)`` is an ``O_h``
         invariant that is odd in ``r`` and *not a polynomial*.  B3's Reynolds
         projection proves the parity statement for POLYNOMIALS only, and that
         is exactly the loophole.
    (ii) NOT NECESSARY.  The ``T_d`` invariant ring is ``R[r^2, xyz, x^4+y^4+z^4]``,
         so every odd-degree ``T_d`` invariant carries the factor ``xyz``, whose
         spherical average vanishes identically.  The Misner-Sharp ``m(r)`` is
         therefore unchanged and a non-centrosymmetric (diamond / zincblende)
         lattice yields the **same** regular centre in the monopole channel.

  So inversion is neither sufficient nor necessary for the conclusion it was
  credited with.  **The real hypothesis is smoothness (analyticity) of the
  coarse-grained core density at the centre in Cartesian coordinates** -- which
  is precisely what is unavailable over a ~2.2-cell core, and which, once
  granted, makes ``O_h`` redundant in the isotropic channel (Whitney: a smooth
  spherically symmetric function is a smooth function of ``r^2``).

  WHAT O_h DOES BUY (B3).  For a density already known to be SMOOTH in Cartesian
  ``x``, ``O_h``-invariance kills every odd-degree term -- which sphericity is
  not available to do when the density is anisotropic, as a lattice density is.
  That is a real but much smaller statement than the refuted one, and it is
  downstream of the smoothness hypothesis rather than a replacement for it.

**Prior art, cited.**  The regularity criterion (``f(0)=1`` plus evenness) is
published in stronger form: Antonelli & Sebastianutti, *Singularity and
differentiability at the origin of regular black holes*, arXiv:2509.15477, PRD
10.1103/hf4r-19xh -- an *iff*, in the two-function class, with differentiability
classes.  This module's contribution is the substrate reading, the no-go, and
the scales; not the criterion.

**Contingency of the scales (B6).**  Three inputs are consumed that the first
draft did not declare, and each is quantified here rather than hidden:

  * SATURATION as an equality (``K(0) = 1/a^4``, not ``<=``).  Without it every
    scale is a one-sided bound: ``L >= 24^(1/4) a`` and so on.
  * The CEILING CONVENTION.  F183 uses ``K_max = 1/a^4``; F284's ``H_max = 1/a``
    implies ``K_max = 24/a^4`` for a de Sitter ceiling.  Under the latter
    ``L = a`` exactly and the infall e-folding is ``sqrt(3)`` ticks = exactly one
    cell crossing = F284's own ``t_min``.  Only one can be fundamental; this is
    flagged as an open decision, not settled here.
  * The PROFILE.  ``L`` is profile-independent (it depends only on ``rho(0)``),
    but the mass-to-core-radius relation is not: Bardeen and an even Gaussian
    differ by a factor 0.643 in the core radius at fixed ``M`` and ``L``, so the
    ``2^(1/6)`` comparison to F183's proxy is Bardeen-specific.

Self-contained: sympy + numpy, no scipy (CLAUDE.md self-contained numerics).

Date: 2026-09-03 - 14:20  (rewritten after the session's own attack pass
refuted the first draft's mechanism; see docs/reviews/F354-review-2026-09-03.md)
"""
from __future__ import annotations

from itertools import permutations, product

import sympy as sp

from casim.constants import (
    G_CODATA as _G_CODATA,
    a_over_ellP as _a_over_ellP,
    c_SI as _c_SI,
    c_lat as _c_lat,
    ell_P_m as _ell_P_m,
)

# ---- constants (D7: imported, never written as literals) -------------------
G_SI = _G_CODATA
C_SI = _c_SI
ELLP = _ell_P_m
A_CELL = _a_over_ellP * ELLP          # F107 canonical BCC cell, metres

# c_lat as an exact sympy object, derived from the registered value rather than
# re-typed as a literal (D7).  c_lat = 1/sqrt(3) exactly on the BCC lattice.
C_LAT_EXACT = sp.nsimplify(_c_lat, [sp.sqrt(3)], rational=False)

# Solar mass and the Planck mass are MEASURED inputs, not model constants; they
# enter only the SI presentation layer.  Sourced here from the registered
# constants so no CODATA number is re-typed (D7).
#   m_Pl = sqrt(hbar c / G) -- built from the registry, not hardcoded.
from casim.constants import hbar_SI as _hbar_SI
M_PLANCK_KG = float(sp.sqrt(sp.Float(_hbar_SI) * sp.Float(C_SI) / sp.Float(G_SI)))
MSUN_KG = 1.98892e30                  # kg -- IAU nominal; presentation only

_r, _M, _g, _L = sp.symbols("r M g L", positive=True)
_A = sp.Function("A")
_B = sp.Function("B")


# ===========================================================================
# A1 -- the substrate tier (structural; NOT counted in the pass tally)
# ===========================================================================
def check_tick_completeness() -> dict:
    """Property (TC) for the BCC automaton -- Grant-Kunzinger-Saemann
    (arXiv:1804.10423): every inextendible timelike geodesic has infinite
    length, length being the time-separation function, here the maximal causal
    chain length in ticks.

    This is a DECLARATION of three engine premises, recorded so the argument can
    be attacked at the premise level.  It computes nothing, so it is reported
    but deliberately **excluded from the pass count** -- an earlier draft
    counted it and thereby inflated a 6-leg battery to "7/7".
    """
    return {
        "criterion": ("Grant-Kunzinger-Saemann property (TC), with length = "
                      "maximal causal chain length = tick count"),
        "premises": {
            "update_is_total": ("the BCC rule is defined at every cell for every "
                                "neighbourhood configuration"),
            "lattice_is_boundaryless": ("infinite, rigid, eternal (F283/F284); "
                                        "no boundary, no excised region"),
            "update_is_norm_preserving": ("unitary, so no chain terminates for "
                                          "want of amplitude"),
        },
        "conclusion": "chain length is unbounded: the substrate is tick-complete",
        "sufficiency": ("NECESSARY, NOT SUFFICIENT -- it does not forbid the "
                        "emergent affine parameter saturating while ticks run "
                        "on. B1 is what rules that out."),
        "counted_in_pass_tally": False,
        "pass": None,
    }


# ===========================================================================
# B1 -- THE RESULT: bounded curvature forces a C^{1,1} regular centre
# ===========================================================================
def _kretschmann_two_function():
    """Exact Kretschmann scalar of ds^2 = -A(r) dt^2 + dr^2/B(r) + r^2 dOmega^2
    by full Riemann contraction."""
    t, th, ph = sp.symbols("t theta phi")
    A, B = _A(_r), _B(_r)
    gm = sp.diag(-A, 1 / B, _r**2, _r**2 * sp.sin(th) ** 2)
    X = [t, _r, th, ph]
    gi = gm.inv()
    Ga = [[[sp.simplify(sum(gi[i, l] * (sp.diff(gm[l, j], X[k])
                                        + sp.diff(gm[l, k], X[j])
                                        - sp.diff(gm[j, k], X[l]))
                            for l in range(4)) / 2)
            for k in range(4)] for j in range(4)] for i in range(4)]
    R = [[[[sp.simplify(sp.diff(Ga[i][j][l], X[k]) - sp.diff(Ga[i][j][k], X[l])
                        + sum(Ga[i][k][q] * Ga[q][j][l]
                              - Ga[i][l][q] * Ga[q][j][k] for q in range(4)))
            for l in range(4)] for k in range(4)] for j in range(4)]
         for i in range(4)]
    Rd = [[[[sum(gm[i, q] * R[q][j][k][l] for q in range(4))
             for l in range(4)] for k in range(4)] for j in range(4)]
          for i in range(4)]
    Ru = [[[[sum(gi[j, b] * gi[k, c] * gi[l, d] * R[Z][b][c][d]
                 for b in range(4) for c in range(4) for d in range(4))
             for l in range(4)] for k in range(4)] for j in range(4)]
          for Z in range(4)]
    return sp.simplify(sum(Rd[i][j][k][l] * Ru[i][j][k][l]
                           for i in range(4) for j in range(4)
                           for k in range(4) for l in range(4)))


def check_sum_of_squares(solid_angle_deficit: float = 0.0) -> dict:
    """Verify the sum-of-squares decomposition and read off what a global
    curvature bound forces at the centre.

    The ``solid_angle_deficit`` parameter is the declared negative control: a
    global-monopole metric ``B(0) = 1 - delta`` has a genuine solid-angle deficit
    at the origin.  The decomposition must then DETECT it -- the
    ``R_thphthph = (1-B)/r^2`` term diverges as ``delta/r^2``, so ``K ~ 4 delta^2/r^4``
    is unbounded and the premise of the theorem fails.  That is the check having
    teeth: a conical/monopole defect is the classic bounded-*some*-invariants but
    incomplete counterexample, and the bound is what excludes it.
    """
    A, B = _A(_r), _B(_r)
    K = _kretschmann_two_function()
    R_thph = (1 - B) / _r**2
    R_rth = -sp.diff(B, _r) / (2 * _r)
    R_tth = B * sp.diff(A, _r) / (2 * _r * A)
    R_tr = (2 * A * B * sp.diff(A, _r, 2) + A * sp.diff(A, _r) * sp.diff(B, _r)
            - B * sp.diff(A, _r) ** 2) / (4 * A**2)
    sos = 4 * R_tr**2 + 8 * R_tth**2 + 8 * R_rth**2 + 4 * R_thph**2
    identity_holds = sp.simplify(K - sos) == 0

    # what the bound forces, term by term
    forced = {
        "B(0)=1_no_solid_angle_defect":
            "|1-B|/r^2 <= K^(1/2)/2 bounded  =>  B(0)=1",
        "Bprime(0)=0": "|B'|/(2r) bounded  =>  B'(0)=0",
        "Aprime(0)=0": "B|A'|/(2rA) bounded  =>  A(0) finite nonzero, A'(0)=0",
        "conclusion": ("metric = eta_uv + O(r^2) in Cartesian coords: C^{1,1}, "
                       "Lorentzian, centre is a manifold interior point"),
    }

    # CONTROL: a solid-angle deficit must be DETECTED (K unbounded at r->0)
    delta = sp.Float(solid_angle_deficit)
    B_def = 1 - delta                       # global monopole: B const < 1
    K_def = sp.simplify(sos.subs({B: B_def, A: sp.Integer(1)}).doit())
    K_def = sp.simplify(K_def)
    leading = sp.simplify(sp.limit(K_def * _r**4, _r, 0))
    deficit_detected = bool(sp.simplify(leading) != 0)
    bound_premise_holds = not deficit_detected     # green only when delta = 0

    return {
        "sum_of_squares_identity": bool(identity_holds),
        "K_expression_is_sum_of_squares":
            "K = 4 R_trtr^2 + 8 R_tththt^2 + 8 R_rthrth^2 + 4 R_thphthph^2",
        "forced_by_bound": forced,
        "solid_angle_deficit": float(solid_angle_deficit),
        "deficit_leading_K_times_r4": sp.sstr(leading),
        "deficit_detected_as_unbounded_K": deficit_detected,
        "two_function_class": True,
        "uses_parity": False,
        "uses_saturation": False,
        "pass": bool(identity_holds and bound_premise_holds),
    }


# ===========================================================================
# B2 -- THE NO-GO: O_h is neither sufficient nor necessary for the parity
# ===========================================================================
def check_point_group_nogo() -> dict:
    """Record, by explicit computation, why the point-group route to the parity
    condition is closed.  Both legs must fire for the no-go to stand."""
    # (i) NOT SUFFICIENT -- Hayward's O(3)-invariant density has an odd r^3 term
    m_hay = _M * _r**3 / (_r**3 + _L**3)
    rho_hay = sp.simplify(sp.diff(m_hay, _r) / (4 * sp.pi * _r**2))
    ser = sp.series(rho_hay, _r, 0, 5).removeO()
    odd3 = sp.simplify(ser.coeff(_r, 3))
    m_not_odd = sp.simplify(m_hay.subs(_r, -_r) + m_hay) != 0
    not_sufficient = bool(odd3 != 0 and m_not_odd)

    # (ii) NOT NECESSARY -- every odd T_d invariant carries xyz, monopole zero
    x, y, z, th, ph = sp.symbols("x y z theta phi")
    sub = {x: sp.sin(th) * sp.cos(ph), y: sp.sin(th) * sp.sin(ph), z: sp.cos(th)}
    monopoles = {}
    for name, poly in (("xyz", x * y * z),
                       ("xyz*r^2", x * y * z * (x**2 + y**2 + z**2)),
                       ("xyz*(x^4+y^4+z^4)", x * y * z * (x**4 + y**4 + z**4))):
        val = sp.integrate(sp.integrate(sp.simplify(poly.subs(sub)) * sp.sin(th),
                                        (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
        monopoles[name] = sp.sstr(sp.simplify(val))
    not_necessary = all(sp.simplify(sp.sympify(v)) == 0
                        for v in monopoles.values())

    return {
        "leg_i_not_sufficient": {
            "rho_hayward": sp.sstr(rho_hay),
            "series": sp.sstr(sp.series(rho_hay, _r, 0, 7)),
            "odd_r3_coefficient": sp.sstr(odd3),
            "m_is_not_odd": bool(m_not_odd),
            "why": ("rho depends on r alone, so it is O(3)- hence O_h- hence "
                    "-1-invariant, yet it is ODD in r. r^(2k+1) = (x^2+y^2+z^2)"
                    "^((2k+1)/2) is a non-polynomial O_h invariant, which is the "
                    "loophole a polynomial-only Reynolds argument leaves open."),
            "holds": not_sufficient,
        },
        "leg_ii_not_necessary": {
            "Td_invariant_ring": "R[r^2, xyz, x^4+y^4+z^4]",
            "spherical_averages": monopoles,
            "why": ("every odd-degree T_d invariant carries xyz, whose monopole "
                    "vanishes, so m(r) is unchanged and a non-centrosymmetric "
                    "lattice gives the same regular centre in the f(r) channel"),
            "holds": not_necessary,
        },
        "verdict": ("the point-group route is CLOSED. The load-bearing "
                    "hypothesis is smoothness/analyticity of the coarse-grained "
                    "core density at the centre, not inversion symmetry."),
        "pass": bool(not_sufficient and not_necessary),
    }


# ===========================================================================
# B3 -- what O_h DOES buy, stated at its true (smaller) strength
# ===========================================================================
def _group_elements(point_group: str = "Oh"):
    """Signed 3x3 permutation matrices. ``Oh`` = all 48; ``Td`` = the stabiliser
    of xyz (24, non-centrosymmetric); ``O`` = the chiral rotations (24)."""
    x, y, z = sp.symbols("x y z")
    els = []
    for p in permutations(range(3)):
        for sg in product((1, -1), repeat=3):
            Mx = sp.zeros(3, 3)
            for i in range(3):
                Mx[i, p[i]] = sg[i]
            if point_group == "O" and Mx.det() != 1:
                continue
            if point_group == "Td":
                w = Mx * sp.Matrix([x, y, z])
                if sp.expand(w[0] * w[1] * w[2] - x * y * z) != 0:
                    continue
            els.append(Mx)
    return els


def check_polynomial_parity(max_degree: int = 6, point_group: str = "Oh") -> dict:
    """Exact Reynolds projection: every ``O_h``-invariant POLYNOMIAL has even
    total degree.

    The word POLYNOMIAL is doing all the work and is stated in the leg's name
    for that reason -- B2(i) is the counterexample showing the statement is
    false without it.  What this buys, given smoothness as a separate
    hypothesis, is that an ANISOTROPIC smooth lattice density has no odd-degree
    Cartesian terms, which sphericity is not available to establish.
    """
    els = _group_elements(point_group)
    x, y, z = sp.symbols("x y z")
    v = sp.Matrix([x, y, z])

    def reynolds(poly):
        tot = 0
        for Mx in els:
            w = Mx * v
            tot += poly.subs({x: w[0], y: w[1], z: w[2]}, simultaneous=True)
        return sp.expand(tot / len(els))

    per_degree = {}
    for d in range(max_degree + 1):
        mons = [x**i * y**j * z**k
                for i in range(d + 1) for j in range(d + 1) for k in range(d + 1)
                if i + j + k == d]
        images = [sp.simplify(reynolds(m)) for m in mons]
        nonzero = [q for q in images if q != 0]
        per_degree[d] = {"n_distinct_invariants":
                         len({sp.srepr(q) for q in nonzero})}
    odd_vanish = all(per_degree[d]["n_distinct_invariants"] == 0
                     for d in range(1, max_degree + 1, 2))
    return {
        "point_group": point_group,
        "group_order": len(els),
        "inversion_in_group": any(m == -sp.eye(3) for m in els),
        "per_degree": per_degree,
        "odd_degree_polynomial_invariants_vanish": bool(odd_vanish),
        "scope_limit": ("POLYNOMIALS ONLY. Non-polynomial O_h invariants such as "
                        "r^3 = (x^2+y^2+z^2)^(3/2) are odd in r -- see B2(i)."),
        "what_it_buys": ("given smoothness as a separate hypothesis, an "
                         "anisotropic lattice density has no odd-degree "
                         "Cartesian terms"),
        "pass": bool(odd_vanish),
    }


# ===========================================================================
# B4 -- geodesics through a C^{1,1} regular centre
# ===========================================================================
def check_geodesics() -> dict:
    """The four regimes. Completeness rests on the E>1 and NULL cases passing
    THROUGH the centre -- which is exactly what B1 licenses.

    The E=1 case is reported but explicitly de-weighted: its "infinite proper
    time, never arrives" reading is physically hollow, because the infaller is
    inside the central cell after tau = L ln(L/a) ~ 3 ticks, beyond which the
    exponential law describes sub-cell motion the model does not resolve.
    """
    E = sp.Symbol("E", positive=True)
    f = 1 - _r**2 / _L**2                      # generic regular centre, O(r^4)
    rdot2 = E**2 - f

    at0 = sp.simplify(rdot2.subs(_r, 0))
    slope0 = sp.simplify(sp.diff(rdot2, _r).subs(_r, 0))
    v_E1 = sp.simplify(1 - f)
    efold_rate = sp.simplify(sp.sqrt(v_E1) / _r)          # = 1/L
    eps = sp.Symbol("eps", positive=True)
    tau_E1 = sp.integrate(1 / sp.sqrt(v_E1), (_r, eps, _L))
    E1_diverges = sp.limit(tau_E1, eps, 0) == sp.oo
    r_turn = sp.solve(sp.Eq(f, E**2), _r)[0]

    # how long before the E=1 infaller is inside the central cell
    L_over_a = 24 ** sp.Rational(1, 4)
    ticks_to_central_cell = sp.simplify(L_over_a / C_LAT_EXACT * sp.log(L_over_a))

    return {
        "E_gt_1_rdot2_at_centre": sp.sstr(at0),
        "E_gt_1_transversal": bool(sp.simplify(at0 - (E**2 - 1)) == 0),
        "E_gt_1_no_cusp": bool(slope0 == 0),
        "null_radial": ("dr/dlam = +/- E: reaches and CROSSES the centre at "
                        "finite affine parameter"),
        "load_bearing": ("E>1 and null: they reach r=0 and must pass through, "
                         "which requires B1's C^{1,1} interior point"),
        "E_eq_1_efold_rate": sp.sstr(efold_rate),
        "E_eq_1_proper_time_diverges": bool(E1_diverges),
        "E_eq_1_caveat": ("de-weighted: after tau = L ln(L/a) = "
                          f"{float(ticks_to_central_cell):.3f} ticks the infaller "
                          "is inside the central cell, where the model resolves "
                          "no metric; the continuum law is extrapolation there"),
        "E_lt_1_turning_radius": sp.sstr(sp.simplify(r_turn)),
        "nonradial": ("Lz^2/r^2 barrier diverges as r->0 since f(0)=1>0: no "
                      "non-radial geodesic reaches the centre"),
        "scope": ("LOCAL r->0 analysis. NOT a completeness proof for the "
                  "maximal extension, which for a two-horizon core requires the "
                  "full conformal diagram."),
        "pass": bool(sp.simplify(at0 - (E**2 - 1)) == 0 and slope0 == 0
                     and E1_diverges and sp.simplify(efold_rate - 1 / _L) == 0),
    }


# ===========================================================================
# B5 -- parity screen against the literature
# ===========================================================================
def _screen_one(f_expr, order: int = 8) -> dict:
    """T1 no pole and f(0)=1; T2 functional parity f(-r) == f(r); T3 no odd
    power in the Laurent expansion; T4 analytic at 0 (series not identically
    flat).  A metric that is smooth-but-flat at the origin (Culetu-Simpson-
    Visser and its even modification) passes T3 vacuously; T4 separates those
    from the analytically-even class, which is the one that matters here."""
    s = sp.expand(sp.series(f_expr, _r, 0, order).removeO())
    coeffs = {d: sp.simplify(s.coeff(_r, d)) for d in range(-3, order)}
    coeffs = {d: c for d, c in coeffs.items() if c != 0}
    poles = sorted(d for d in coeffs if d < 0)
    odd = sorted(d for d in coeffs if d > 0 and d % 2 == 1)
    f0 = coeffs.get(0, sp.Integer(0))
    t1 = (not poles) and sp.simplify(f0 - 1) == 0
    t2 = sp.simplify(sp.expand(f_expr.subs(_r, -_r) - f_expr)) == 0
    t3 = not odd
    # analytic: the series has at least one nonzero term beyond the constant
    t4 = any(d > 0 for d in coeffs)
    return {
        "T1_f0_is_1_no_pole": bool(t1),
        "T2_functional_parity": bool(t2),
        "T3_no_odd_series_term": bool(t3),
        "T4_analytic_nonflat": bool(t4),
        "lowest_odd_power": (odd[0] if odd else None),
        "lowest_odd_coeff": (sp.sstr(coeffs[odd[0]]) if odd else None),
        "analytically_even_regular_centre": bool(t1 and t3 and t4),
        "smooth_but_flat": bool(t1 and not t4),
    }


def check_parity_screen() -> dict:
    """Screen the literature's regular black holes. Calibrated by reproducing
    Zhou-Modesto's Hayward obstruction; cross-checked against ZM's own verdicts
    so a disagreement is visible rather than hidden."""
    al, gam = sp.symbols("alpha gamma", positive=True)
    cases = {
        "bardeen": 1 - 2 * _M * _r**2 / (_r**2 + _g**2) ** sp.Rational(3, 2),
        "schwarzschild": 1 - 2 * _M / _r,
        "hayward_r3_plus_L3": 1 - 2 * _M * _r**2 / (_r**3 + _L**3),
        "bonanno_reuter_rg_improved":
            1 - 2 * _M * _r**2 / (_r**3 + al * (_r + gam * _M)),
        "culetu_simpson_visser": 1 - (2 * _M / _r) * sp.exp(-_g / _r),
        "csv_even_modified_ZM": 1 - (2 * _M / _r) * sp.exp(-_g**2 / _r**2),
    }
    out = {k: _screen_one(v) for k, v in cases.items()}

    # calibration against ZM's published Hayward coefficient
    hay = out["hayward_r3_plus_L3"]
    hay_coeff = sp.sympify(hay["lowest_odd_coeff"], locals={"M": _M, "L": _L})
    calibrated = (hay["lowest_odd_power"] == 5
                  and sp.simplify(hay_coeff - 2 * _M / _L**6) == 0)

    # agreement with ZM's own completeness verdicts, stated explicitly
    zm_verdict = {"bardeen": True, "hayward_r3_plus_L3": False,
                  "culetu_simpson_visser": False, "csv_even_modified_ZM": True}
    agree = {}
    for k, zm in zm_verdict.items():
        if k == "csv_even_modified_ZM":
            # ZM restore completeness at the C^inf level; this row is smooth but
            # FLAT at the origin, so the analytic screen cannot adjudicate it.
            # Recorded as out-of-scope rather than as a false negative.
            agree[k] = ("out-of-scope (smooth-but-flat: "
                        f"{out[k]['smooth_but_flat']}), ZM say complete")
        else:
            agree[k] = bool(out[k]["analytically_even_regular_centre"] == zm)
    in_scope_ok = all(v is True for k, v in agree.items()
                      if isinstance(v, bool))

    return {
        "cases": out,
        "reproduces_ZM_hayward_r5_coeff_2M_over_L6": bool(calibrated),
        "agreement_with_ZM": agree,
        "screen_scope": ("adjudicates the ANALYTICALLY-even class only; metrics "
                         "that are smooth but flat at the origin (CSV and its "
                         "even modification) are out of scope and are reported "
                         "as such, not scored"),
        "bonanno_reuter_note": ("BR carries an odd r^3 from the linear alpha*r "
                                "in its denominator, so it sits in ZM's "
                                "incomplete class. Reported as this screen's "
                                "output; we have found no paper stating or "
                                "disputing it and claim no priority."),
        "pass": bool(calibrated and in_scope_ok),
    }


# ===========================================================================
# B6 -- the scales, with their contingency made explicit
# ===========================================================================
def check_scales(core_profile: str = "bardeen") -> dict:
    """Compute the scales under each of the two ceiling conventions and both
    profiles, so the contingency is a table rather than a footnote.

    ``core_profile`` is the declared negative control: switching to an even
    Gaussian changes the mass-to-core-radius relation and so the comparison with
    F183's proxy, demonstrating that the ``2^(1/6)`` figure is Bardeen-specific
    while ``L`` is not.
    """
    a = sp.Symbol("a", positive=True)
    out = {}
    for conv, Kmax in (("F183_K_le_1_over_a4", 1 / a**4),
                       ("F284_H_le_1_over_a", 24 / a**4)):
        L_sol = sp.simplify(sp.solve(sp.Eq(24 / _L**4, Kmax), _L)[0])
        ticks = sp.simplify(L_sol / a / C_LAT_EXACT)
        out[conv] = {
            "L_over_a": sp.sstr(sp.nsimplify(sp.simplify(L_sol / a))),
            "L_over_a_float": float(L_sol / a),
            "efold_ticks": sp.sstr(sp.nsimplify(ticks)),
            "efold_ticks_float": float(ticks),
        }
    # L is profile-independent; the mass-to-core-radius relation is not
    if core_profile == "bardeen":
        # rho0 = 3M/(4 pi g^3) ; 1/L^2 = 2M/g^3  => g = (2 M L^2)^(1/3)
        core_of_ML = (2 * _M * _L**2) ** sp.Rational(1, 3)
    elif core_profile == "gaussian":
        s = sp.Symbol("s", positive=True)
        core_of_ML = sp.solve(
            sp.Eq(1 / _L**2,
                  8 * sp.pi * _M / (3 * (2 * sp.pi) ** sp.Rational(3, 2) * s**3)),
            s)[0]
    else:
        raise ValueError(f"unknown core_profile {core_profile!r}")

    L_F183 = 24 ** sp.Rational(1, 4) * a
    core_F183 = sp.simplify(core_of_ML.subs(_L, L_F183))
    proxy = (48 * _M**2 * a**4) ** sp.Rational(1, 6)          # F183 SS L1
    ratio = sp.simplify(core_F183 / proxy)
    bardeen_ratio = sp.simplify(
        ((2 * _M * L_F183**2) ** sp.Rational(1, 3)) / proxy)

    return {
        "ceiling_conventions": out,
        "ceiling_fork_is_open": ("F183 and F284 imply ceilings differing by a "
                                 "factor 24 in K (24^(1/4) in length); under "
                                 "F284's the core radius is L = a exactly and "
                                 "the e-folding is sqrt(3) ticks = one cell "
                                 "crossing = F284's own t_min. Open decision."),
        "core_profile": core_profile,
        "core_radius_of_M_and_L": sp.sstr(sp.simplify(core_of_ML)),
        "ratio_to_F183_proxy": sp.sstr(sp.nsimplify(ratio)),
        "ratio_to_F183_proxy_float": float(ratio),
        "L_is_profile_independent": True,
        "ratio_is_profile_dependent": True,
        "saturation_is_an_assumption": ("without saturation as an EQUALITY every "
                                        "scale is a one-sided bound: "
                                        "L >= 24^(1/4) a, etc."),
        "pass": bool(
            # L under F183's convention is 24^(1/4) a, profile-independently
            sp.simplify(sp.sympify(out["F183_K_le_1_over_a4"]["L_over_a"])
                        - 24 ** sp.Rational(1, 4)) == 0
            # and under F284's it is exactly 1 cell, with sqrt(3) ticks
            and sp.simplify(sp.sympify(out["F284_H_le_1_over_a"]["L_over_a"]) - 1) == 0
            and sp.simplify(sp.sympify(out["F284_H_le_1_over_a"]["efold_ticks"])
                            - sp.sqrt(3)) == 0
            # and the Bardeen-specific ratio is 2^(1/6) -- reds under gaussian
            and sp.simplify(ratio - bardeen_ratio) == 0
            and sp.simplify(ratio - 2 ** sp.Rational(1, 6)) == 0),
    }


# ===========================================================================
# B7 -- resolvability, the corrected offset bound, and M_ext
# ===========================================================================
def check_resolvability(masses_solar=(1.0, 10.0, 1.0e6)) -> dict:
    """SI numbers, the corrected covering radius, and the extremal mass.

    Two corrections to the first draft are recorded here:
      * the inversion-centre array is simple cubic of spacing a/2, so its
        COVERING RADIUS is (sqrt3/2)(a/2) = sqrt(3) a/4 = 0.433 a, not a/4;
        and the worst-case point (1/4,1/4,1/4) is Wyckoff 8c with site symmetry
        -43m = T_d -- the very group B2(ii) shows is inversion-free.
      * M_crit (core one cell across) is NOT the black-hole threshold: the
        horizon disappears at M_ext = (3 sqrt3/4) L, ~28x higher, so below
        ~19 Planck masses there is no horizon at all.
    """
    a = A_CELL
    L_m = float(24 ** 0.25) * a
    covering_radius_over_a = float(sp.sqrt(3) / 4)
    rows = []
    for Ms in masses_solar:
        rg = G_SI * Ms * MSUN_KG / C_SI**2
        core = (96.0 * rg**2 * a**4) ** (1.0 / 6.0)
        rows.append({
            "M_solar": Ms,
            "r_horizon_m": 2 * rg,
            "core_radius_m": core,
            "core_over_a": core / a,
            "F183_proxy_m": (48.0 * rg**2 * a**4) ** (1.0 / 6.0),
            "offset_parity_bound": covering_radius_over_a * a / core,
        })
    M_crit_planck = float(_a_over_ellP) / (96.0 ** 0.5)
    # extremal mass: horizon disappears. Bardeen: M_ext = (3 sqrt3/4) g_ext with
    # g_ext = L; in Planck masses via L/ellP.
    M_ext_planck = float(3 * sp.sqrt(3) / 4) * (float(24 ** 0.25)
                                                * float(_a_over_ellP))
    return {
        "a_cell_m": a,
        "L_universal_m": L_m,
        "L_over_a": L_m / a,
        "covering_radius_over_a": covering_radius_over_a,
        "covering_radius_note": ("simple-cubic inversion-centre array of spacing "
                                 "a/2; worst-case point (1/4,1/4,1/4) is Wyckoff "
                                 "8c, site symmetry -43m = T_d"),
        "first_draft_said": "a/4 = 0.25 a  -- WRONG by sqrt(3)",
        "M_crit_planck_masses": M_crit_planck,
        "M_crit_note": ("core one cell across; NOT a black-hole threshold"),
        "M_ext_planck_masses": M_ext_planck,
        "M_ext_note": ("horizon disappears below this: sub-~19-Planck-mass black "
                       "holes do not exist in this model. This is the physically "
                       "meaningful small-mass threshold."),
        "M_ext_over_M_crit": M_ext_planck / M_crit_planck,
        "rows": rows,
        "pass": bool(abs(L_m / a - 24 ** 0.25) < 1e-12
                     and abs(covering_radius_over_a - 3 ** 0.5 / 4) < 1e-15
                     and M_ext_planck > M_crit_planck
                     and all(r["offset_parity_bound"] < 1e-11 for r in rows)),
    }


# ===========================================================================
# battery
# ===========================================================================
def run_all(solid_angle_deficit: float = 0.0,
            core_profile: str = "bardeen",
            point_group: str = "Oh") -> dict:
    """Gate entry.

    Declared negative controls (D9/H2), both perturbing COMPUTED quantities:

      ``solid_angle_deficit=0.1``  a global-monopole metric B(0) = 1 - delta.
                                   B1 must go red: the sum-of-squares term
                                   (1-B)/r^2 makes K ~ 4 delta^2/r^4, unbounded,
                                   so the theorem's premise genuinely fails on a
                                   defect -- the classic bounded-invariants-but-
                                   incomplete case the bound must exclude.
      ``core_profile="gaussian"``  swaps the even core profile. B6 must go red:
                                   the mass-to-core-radius relation changes, so
                                   the 2^(1/6) comparison with F183's proxy is
                                   Bardeen-specific, while L is not.
    """
    checks = {
        "B1_sum_of_squares_regular_centre":
            check_sum_of_squares(solid_angle_deficit),
        "B2_point_group_nogo": check_point_group_nogo(),
        "B3_polynomial_parity": check_polynomial_parity(point_group=point_group),
        "B4_geodesics": check_geodesics(),
        "B5_parity_screen": check_parity_screen(),
        "B6_scales": check_scales(core_profile),
        "B7_resolvability": check_resolvability(),
    }
    counted = {k: v for k, v in checks.items() if v.get("pass") is not None}
    n_pass = sum(1 for v in counted.values() if v["pass"])
    return {
        "finding": "F354",
        "title": ("Lattice core geodesic completeness from bounded curvature; "
                  "point-group route to the parity condition is a no-go"),
        "substrate_tier_not_counted": check_tick_completeness(),
        "checks": checks,
        "n_pass": n_pass,
        "n_total": len(counted),
        "all_pass": n_pass == len(counted),
    }


if __name__ == "__main__":            # guard: never write an artifact at import
    import json
    from casim.engine.particles._results_path import results_path

    res = run_all()
    path = results_path("F354_core_geodesic_completeness.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(f"{res['n_pass']}/{res['n_total']} PASS -> {path}")
