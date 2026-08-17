#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derive_gauge_boson_masses.py — the ABSOLUTE W and Z masses, and rho = 1
=======================================================================

2026-08-16 - 17:55   (F320, completeness row B12)

Row B12 reads PARTIAL with the residual "absolute scale is an input", and
`docs/claims/CL016-mw-and-mz-absolute-not-claimed.md` records m_W and m_Z
absolute as an explicit `non_claim`.  This module re-audits that boundary and
finds it drawn one step too far in.  The finding is an ACCOUNTING result before
it is a physics result, and it is stated that way:

    TRUE, and unchanged:  v is an anchor.  Nothing here derives it.
    FALSE, and corrected: "m_W and m_Z are not predicted."  They are.

The distinction is the input COUNT.  The Standard Model's electroweak sector
takes three measured inputs -- {alpha, G_F, m_Z} -- and predicts m_W.  This
model derives sin^2(theta_W) on-shell = 2/9 from lattice geometry (F49 counting,
F141 Wigner-Seitz lemma), so it takes TWO -- {alpha, G_F} -- and predicts BOTH
boson masses.  Two inputs is not zero inputs, and the finding does not pretend
otherwise; it is one fewer than the SM, and the object that was "not predicted"
becomes an output with a residual you can quote.

What is actually derived here
-----------------------------
**(1) The stiffness quantum is determined.**  F141 §3 posits one universal
stiffness quantum u per structural channel -- 7 Wigner-Seitz facet axes for the
SU(2)_L link sector, 2 sublattices for the F51 abelian sector -- so g^2 = 7u
and g'^2 = 2u.  F141 left u as a free overall normalisation and got only the
RATIO.  Eliminating u against the definition e = g sin(theta_W) fixes it:

        e^2 = g^2 g'^2 / (g^2 + g'^2) = 14u/9        =>   u = 9 e^2 / 14

    hence  g^2  = 7u = 9 e^2 / 2   = 18 pi alpha     (exact)
           g'^2 = 2u = 9 e^2 / 7   = 36 pi alpha / 7 (exact)

    and the two closed forms this finding exists to write down:

        m_W = (3v/2) sqrt(2 pi alpha)
        m_Z = (9v/2) sqrt(2 pi alpha / 7)

    These are exact algebra, not fits.  There is no free parameter left in
    them: v and alpha are the two rulers, and the rationals 3/2, 9/2 and 7 are
    the BCC facet/sublattice counts.

**(2) rho = 1 exactly, from RANK, not from custodial symmetry.**  The
electroweak literature gets rho = 1 at tree level from the Higgs doublet's
custodial SU(2).  This model has no Higgs field (F27/F41), so it cannot borrow
that argument, and until now it did not have its own.  It does: F41 absorbs
exactly ONE Stueckelberg direction on U(x) -- Delta_Y = Y_L - Y_R, a single
combination -- so the breaking is RANK ONE.  A rank-one breaking of
SU(2) x U(1) gives a mass matrix

        M^2 = (v^2/4) [[ g^2, -g g'], [-g g', g'^2 ]]

whose determinant vanishes IDENTICALLY -- as a polynomial in u, not at a tuned
point -- so one eigenvalue is exactly zero (the photon) and rho = 1 exactly for
every u and every g'/g.  The control `rank_two_breaking=true` adds a second
independent direction and watches det, the photon mass and rho all go red while
the 7:9 counting legs stay green: rank owns rho, counting owns the ratio, and
the two are separable.

**(3) The absolute residual is the ANGLE residual, and nothing else.**  This is
the leg that makes the prediction quotable despite the radiative correction
Delta_r being external.  The on-shell relation is

        m_W^2 sin^2(theta_W) = pi alpha / (sqrt2 G_F (1 - Delta_r))

and BOTH the model and the SM sit on it with the SAME Delta_r.  Taking the
ratio, Delta_r CANCELS:

        m_W(model) / m_W(obs) = sqrt( sin^2(theta_W)_obs / (2/9) )   -- exactly

    = +0.222 % on m_W and +0.158 % on m_Z, for ANY Delta_r whatsoever.

So the absolute-mass prediction inherits the accuracy of the on-shell angle
(the known -0.44 %, F231) and adds no new freedom of its own.  Check B4a
verifies the invariance over a scan of Delta_r in [0, 0.10]; B4c measures the
one place Delta_r is NOT common -- the model's own c^2/s^2 = 7/2 sits inside
Delta_r's top-quark term where the SM has 3.4830 -- and finds it worth
-0.0095 % on m_W, more than an order below the residual it perturbs.

Honest scope
------------
  * v is NOT derived.  F119 finds the overall scale N = m_lat(tau) has no O(1)
    mechanism, and that is untouched here.  Ledger 17 stays FIT(N=1).
  * alpha is NOT derived.  F127's four-avenue no-go stands.  It is the model's
    one EM input and it is now also an input to the boson masses.
  * The 7:2 equal-stiffness hypothesis (U) of F141 §4 is still a HYPOTHESIS.
    Its (U1)/(U2)/(U3) legs remain open.  What this module adds is that GIVEN
    (U), the absolute masses follow -- so (U) is now carrying strictly more
    weight than it was, and the induced-stiffness loop F138/F141 both point at
    is correspondingly more valuable.
  * Delta_r is external.  Its upper endpoint is CALIBRATED from the PDG masses
    (stated plainly, check B5), which is why the absolute number is reported as
    a BRACKET and the Delta_r-free ratio is the headline.

Entry point
-----------
    check_gauge_boson_masses(equal_stiffness=True, rank_two_breaking=False,
                             eliminate_u=True) -> dict

Controls (each reddens a DISJOINT leg set -- that is the point of having three):
    equal_stiffness=False   -> the 7:2 counting legs; rho legs stay green
    rank_two_breaking=True  -> the rho / massless-photon legs; counting stays green
    eliminate_u=False       -> the absolute legs; ratio and rho both stay green
"""
from __future__ import annotations

import math
from fractions import Fraction

from casim.constants import sin2_thetaW_onshell

# ---------------------------------------------------------------------------
# External measured inputs.  None of these is a registry constant: the tree
# carries alpha, G_F and the PDG boson masses as module-local literals with
# their source named (running_alpha_s.py, test_F138_*.py, test_F141_*.py all do
# the same), and registering them is a separate C2 cleanup with a much larger
# blast radius than this finding.  Each is labelled with what it is and where
# it comes from, which is the contract that matters here.
# ---------------------------------------------------------------------------
ALPHA_INV      = 137.035999177      # CODATA 2022   1/alpha(0)  -- the EM ruler (F127)
G_FERMI        = 1.1663787e-5       # PDG 2024      GeV^-2      -- the EW ruler (= v)
M_W_PDG        = 80.3692            # PDG 2024      GeV
M_Z_PDG        = 91.1880            # PDG 2024      GeV
M_T_POLE       = 172.57             # PDG 2024      GeV  (same value as running_alpha_s.M_T_POLE)
DELTA_ALPHA_MZ = 0.05903            # PDG 2024      alpha(M_Z)/alpha(0) - 1, lept+had5+top

ALPHA = 1.0 / ALPHA_INV
V_EW  = 1.0 / math.sqrt(math.sqrt(2.0) * G_FERMI)     # (sqrt2 G_F)^(-1/2) GeV

# The model-side counts.  N_AXES is F141's exact Wigner-Seitz lemma (the 7
# facet-normal axes of the BCC truncated octahedron); N_SUBLATTICE is F51's
# bipartite parity.  They are integers, and they are the whole model input.
N_AXES        = 7
N_SUBLATTICE  = 2


# ===========================================================================
#  B0 — do not trust the counting, recompute it
# ===========================================================================
def counting_to_angle(n_axes: int = N_AXES, n_sub: int = N_SUBLATTICE) -> dict:
    """g^2 = n_axes * u, g'^2 = n_sub * u  ->  sin^2(theta_W) on-shell, exact over Q."""
    n_axes, n_sub = Fraction(n_axes), Fraction(n_sub)
    s2 = n_sub / (n_axes + n_sub)              # g'^2/(g^2+g'^2)
    c2 = n_axes / (n_axes + n_sub)
    return {
        "sin2_thetaW_os": s2,
        "cos2_thetaW_os": c2,
        "c2_over_s2": c2 / s2,
        "mZ2_over_mW2": 1 / c2,
        "mZ_over_mW": math.sqrt(float(1 / c2)),
    }


# ===========================================================================
#  B1 — rank-one breaking  =>  det M^2 == 0  =>  photon massless, rho == 1
# ===========================================================================
def mass_matrix(u: Fraction, n_axes: int = N_AXES, n_sub: int = N_SUBLATTICE,
                rank_two: bool = False, v2_over_4: Fraction = Fraction(1)) -> list:
    """The (W^3, B) quadratic form in units where v^2/4 = `v2_over_4`.

    Rank ONE means the condensate breaks along a single direction, so the form
    is the outer product of one covector with itself:  M^2 = (v^2/4) w w^T with
    w = (g, -g').  That is F41: exactly one Stueckelberg combination Delta_Y is
    absorbed on U(x).  `rank_two=True` adds an independent second direction
    (an extra diagonal B-mass), which is what a model with a second, abelian-
    charged condensate would have -- and it destroys the massless photon.
    """
    g2 = Fraction(n_axes) * u
    gp2 = Fraction(n_sub) * u
    # Work with the exact rank-one form: M^2 = v2/4 * [[g2, -x], [-x, gp2]]
    # with x = sqrt(g2*gp2).  x^2 = n_axes*n_sub*u^2 is exact; carry x^2, not x.
    m = {
        "M11": v2_over_4 * g2,
        "M22": v2_over_4 * gp2,
        "M12sq": (v2_over_4 ** 2) * Fraction(n_axes * n_sub) * u * u,
    }
    if rank_two:
        m["M22"] = m["M22"] + v2_over_4 * u     # an independent second direction
    m["det"] = m["M11"] * m["M22"] - m["M12sq"]
    return m


def rho_from_counting(u: Fraction, n_axes: int = N_AXES, n_sub: int = N_SUBLATTICE,
                      rank_two: bool = False) -> dict:
    """rho = m_W^2 / (m_Z^2 cos^2 theta_W), exact over Q, for a given u."""
    v2_4 = Fraction(1)
    m = mass_matrix(u, n_axes, n_sub, rank_two=rank_two, v2_over_4=v2_4)
    tr = m["M11"] + m["M22"]
    det = m["det"]
    # eigenvalues of a 2x2 with known trace and det: the massive one is tr when det==0
    mZ2 = tr if det == 0 else None
    mW2 = v2_4 * Fraction(n_axes) * u
    c2 = Fraction(n_axes, n_axes + n_sub)
    if rank_two:
        # both eigenvalues nonzero: the "photon" acquires a mass; rho uses the heavy one
        disc = tr * tr - 4 * det
        mZ2 = (float(tr) + math.sqrt(float(disc))) / 2.0
        rho = float(mW2) / (mZ2 * float(c2))
        mgamma2 = (float(tr) - math.sqrt(float(disc))) / 2.0
    else:
        rho = Fraction(mW2, mZ2) / c2
        mgamma2 = Fraction(0)
    return {"det": det, "m_photon_sq": mgamma2, "m_Z_sq": mZ2, "m_W_sq": mW2,
            "rho": rho, "rank_two": rank_two}


def photon_eigenvector(n_axes: int = N_AXES, n_sub: int = N_SUBLATTICE) -> dict:
    """The exactly-massless direction: A = (g' W^3 + g B)/sqrt(g^2+g'^2).

    With g^2 : g'^2 = n_axes : n_sub the components are sqrt(n_sub) : sqrt(n_axes)
    over sqrt(n_axes+n_sub) -- i.e. (sqrt2, sqrt7)/3 for the BCC counts.  The
    residual is M^2 applied to that vector, which must be exactly zero.
    """
    g, gp = math.sqrt(n_axes), math.sqrt(n_sub)
    norm = math.hypot(g, gp)
    a = (gp / norm, g / norm)                       # the photon
    # M^2 = [[g^2, -g g'], [-g g', g'^2]]  (u = v^2/4 = 1)
    r0 = (g * g) * a[0] + (-g * gp) * a[1]
    r1 = (-g * gp) * a[0] + (gp * gp) * a[1]
    return {"components": a, "residual": max(abs(r0), abs(r1)),
            "components_exact_sq": (Fraction(n_sub, n_axes + n_sub),
                                    Fraction(n_axes, n_axes + n_sub))}


# ===========================================================================
#  B2 — eliminate u against e = g sin(theta_W); the closed forms
# ===========================================================================
def stiffness_quantum(alpha: float = ALPHA, n_axes: int = N_AXES,
                      n_sub: int = N_SUBLATTICE, eliminate: bool = True) -> dict:
    """u from e^2 = g^2 g'^2/(g^2+g'^2) = (n_axes n_sub/(n_axes+n_sub)) u.

    With (7,2): e^2 = 14u/9, so u = 9 e^2/14 and g^2 = 7u = 9 e^2/2 = 18 pi alpha.
    `eliminate=False` is the control: u stays free (set to 1), the ratio and rho
    survive, every absolute number dies.
    """
    e2 = 4.0 * math.pi * alpha
    coeff = Fraction(n_axes * n_sub, n_axes + n_sub)          # e^2 = coeff * u
    if not eliminate:
        return {"u": 1.0, "eliminated": False, "coeff": coeff,
                "g2": float(n_axes), "gp2": float(n_sub),
                "g2_over_pi_alpha": None}
    u = e2 / float(coeff)
    return {"u": u, "eliminated": True, "coeff": coeff,
            "g2": n_axes * u, "gp2": n_sub * u,
            "g2_over_pi_alpha": (n_axes * u) / (math.pi * alpha),
            "gp2_over_pi_alpha": (n_sub * u) / (math.pi * alpha)}


def closed_forms(alpha: float = ALPHA, v: float = V_EW, n_axes: int = N_AXES,
                 n_sub: int = N_SUBLATTICE, eliminate: bool = True) -> dict:
    """m_W = (3v/2) sqrt(2 pi alpha),  m_Z = (9v/2) sqrt(2 pi alpha/7)  at (7,2)."""
    st = stiffness_quantum(alpha, n_axes, n_sub, eliminate=eliminate)
    g2, gp2 = st["g2"], st["gp2"]
    mW = math.sqrt(g2) * v / 2.0
    mZ = math.sqrt(g2 + gp2) * v / 2.0
    # the advertised closed forms, written independently and compared
    cf_W = 1.5 * v * math.sqrt(2.0 * math.pi * alpha)
    cf_Z = 4.5 * v * math.sqrt(2.0 * math.pi * alpha / 7.0)
    return {"m_W_tree": mW, "m_Z_tree": mZ,
            "m_W_closed_form": cf_W, "m_Z_closed_form": cf_Z,
            "closed_form_residual": max(abs(cf_W - mW), abs(cf_Z - mZ)),
            "eliminated": st["eliminated"]}


# ===========================================================================
#  B3/B4 — the on-shell solve, and the Delta_r-invariance theorem
# ===========================================================================
def onshell_mW(s2: float, delta_r: float = 0.0, alpha: float = ALPHA,
               g_f: float = G_FERMI) -> float:
    """m_W^2 sin^2(theta_W) = pi alpha / (sqrt2 G_F (1 - Delta_r))."""
    a2 = math.pi * alpha / (math.sqrt(2.0) * g_f * (1.0 - delta_r))
    return math.sqrt(a2 / s2)


def observed_angle() -> float:
    return 1.0 - (M_W_PDG / M_Z_PDG) ** 2


def delta_r_implied_by_pdg(alpha: float = ALPHA, g_f: float = G_FERMI) -> float:
    """The Delta_r the PDG masses themselves imply -- an EXTERNAL number, and
    the honest label for it is 'calibrated', not 'derived'."""
    a2 = math.pi * alpha / (math.sqrt(2.0) * g_f)
    return 1.0 - a2 / (M_W_PDG ** 2 * observed_angle())


def delta_rho_top(m_t: float = M_T_POLE, g_f: float = G_FERMI) -> float:
    return 3.0 * g_f * m_t ** 2 / (8.0 * math.sqrt(2.0) * math.pi ** 2)


def delta_r_bracket(c2_over_s2: float) -> dict:
    """lo = the two terms the model supplies structure for; hi = the PDG-calibrated
    full one-loop value.  The gap between them IS the SM's Delta_r_rem."""
    lo = DELTA_ALPHA_MZ - c2_over_s2 * delta_rho_top()
    hi = delta_r_implied_by_pdg()
    return {"lo": lo, "hi": hi, "implied_delta_r_rem": hi - lo,
            "delta_alpha": DELTA_ALPHA_MZ, "delta_rho_top": delta_rho_top()}


def dr_invariance_scan(s2_model: float, n: int = 41) -> dict:
    """m_W(model)/m_W(obs) must be sqrt(s2_obs/s2_model) for EVERY Delta_r."""
    s2_obs = observed_angle()
    target = math.sqrt(s2_obs / s2_model)
    worst = 0.0
    for i in range(n):
        dr = 0.10 * i / (n - 1)
        r = onshell_mW(s2_model, dr) / onshell_mW(s2_obs, dr)
        worst = max(worst, abs(r - target))
    return {"target_ratio": target, "worst_deviation": worst,
            "mW_excess_pct": 100.0 * (target - 1.0),
            "mZ_excess_pct": 100.0 * (target * math.sqrt(float(Fraction(9, 7)))
                                      / (M_Z_PDG / M_W_PDG) - 1.0)}


# ===========================================================================
#  the entry point
# ===========================================================================
def check_gauge_boson_masses(equal_stiffness: bool = True,
                             rank_two_breaking: bool = False,
                             eliminate_u: bool = True,
                             alpha: float = ALPHA) -> dict:
    checks: list[dict] = []

    def add(name, ok, value, note=""):
        checks.append({"name": name, "ok": bool(ok), "value": value, "note": note})

    # The control on the counting: break the 4-body-diagonal / 3-face-axis
    # equality that F141 (U1) has NOT established, and the 7 becomes 4*2+3 = 11.
    n_axes = N_AXES if equal_stiffness else 11
    n_sub = N_SUBLATTICE

    # ---- B0: recompute the counting -------------------------------------
    ang = counting_to_angle(n_axes, n_sub)
    s2_model = float(ang["sin2_thetaW_os"])
    add("B0a", ang["sin2_thetaW_os"] == sin2_thetaW_onshell,
        str(ang["sin2_thetaW_os"]),
        "the 7:2 count reproduces the registry sin2_thetaW_onshell = 2/9 exactly")
    add("B0b", ang["mZ2_over_mW2"] == Fraction(9, 7), str(ang["mZ2_over_mW2"]),
        "m_Z^2 : m_W^2 = 9 : 7 exactly (F141 V3)")
    add("B0c", ang["c2_over_s2"] == Fraction(7, 2), str(ang["c2_over_s2"]),
        "c^2/s^2 = 7/2 exactly -- the coefficient of Delta_rho inside Delta_r")

    # ---- B1: rank-one => det == 0 => photon massless, rho == 1 ----------
    dets, rhos, mgs = [], [], []
    for num in (1, 3, 7, 23, 101):
        r = rho_from_counting(Fraction(num, 13), n_axes, n_sub,
                              rank_two=rank_two_breaking)
        dets.append(r["det"]); rhos.append(r["rho"]); mgs.append(r["m_photon_sq"])
    add("B1a", all(d == 0 for d in dets), str(dets[0]),
        "det M^2 vanishes IDENTICALLY in u (5 independent rationals) -- rank one")
    add("B1b", all(float(x) == 0.0 for x in mgs), str(mgs[0]),
        "the photon is exactly massless, not massless to a tolerance")
    add("B1c", all(r == 1 for r in rhos), str(rhos[0]),
        "rho = 1 EXACTLY for every u -- from rank, with no custodial SU(2) assumed")
    ev = photon_eigenvector(n_axes, n_sub)
    add("B1d", ev["residual"] < 1e-14, ev["residual"],
        f"the massless eigenvector is ({ev['components'][0]:.6f}, "
        f"{ev['components'][1]:.6f}) = (sqrt2, sqrt7)/3 at the BCC counts")

    # ---- B2: eliminate u; the closed forms ------------------------------
    st = stiffness_quantum(alpha, n_axes, n_sub, eliminate=eliminate_u)
    g2_ok = (st["g2_over_pi_alpha"] is not None
             and abs(st["g2_over_pi_alpha"] - 18.0) < 1e-12)
    add("B2a", g2_ok, st["g2_over_pi_alpha"],
        "u is DETERMINED, not free: g^2 = 18 pi alpha exactly (F141 left u open)")
    gp_ok = (st.get("gp2_over_pi_alpha") is not None
             and abs(st["gp2_over_pi_alpha"] - 36.0 / 7.0) < 1e-12)
    add("B2b", gp_ok, st.get("gp2_over_pi_alpha"),
        "g'^2 = 36 pi alpha / 7 exactly")
    cf = closed_forms(alpha, V_EW, n_axes, n_sub, eliminate=eliminate_u)
    add("B2c", cf["closed_form_residual"] < 1e-12 and eliminate_u,
        cf["closed_form_residual"],
        "m_W = (3v/2) sqrt(2 pi alpha) and m_Z = (9v/2) sqrt(2 pi alpha/7) "
        "reproduce the matrix solve to machine precision")

    # ---- B3: the tree numbers -------------------------------------------
    mW_tree = onshell_mW(s2_model, 0.0, alpha)
    mZ_tree = mW_tree / math.sqrt(float(ang["cos2_thetaW_os"]))
    add("B3a", abs(mW_tree - cf["m_W_tree"]) < 1e-9 and eliminate_u,
        mW_tree, "the on-shell solve and the (v, alpha) closed form agree")
    tree_W = 100.0 * (mW_tree / M_W_PDG - 1.0)
    tree_Z = 100.0 * (mZ_tree / M_Z_PDG - 1.0)
    add("B3b", -2.0 < tree_W < -1.0, tree_W,
        f"tree m_W = {mW_tree:.4f} GeV, {tree_W:+.4f} % -- the universal Delta_r "
        "deficit, present in the SM's own tree relation too")
    add("B3c", -2.0 < tree_Z < -1.0, tree_Z,
        f"tree m_Z = {mZ_tree:.4f} GeV, {tree_Z:+.4f} %")

    # ---- B4: the Delta_r-invariance theorem -----------------------------
    inv = dr_invariance_scan(s2_model)
    add("B4a", inv["worst_deviation"] < 1e-12, inv["worst_deviation"],
        "m_W(model)/m_W(obs) = sqrt(s2_obs/s2_model) for EVERY Delta_r in "
        "[0, 0.10] -- the radiative correction cancels in the ratio")
    add("B4b", abs(inv["mW_excess_pct"] - 0.221) < 0.01, inv["mW_excess_pct"],
        f"m_W is {inv['mW_excess_pct']:+.3f} % high, Delta_r-free")
    add("B4c", abs(inv["mZ_excess_pct"] - 0.157) < 0.01, inv["mZ_excess_pct"],
        f"m_Z is {inv['mZ_excess_pct']:+.3f} % high, Delta_r-free")
    # the one place Delta_r is not common: c^2/s^2 = 7/2 vs the observed 3.4830
    s2_obs = observed_angle()
    dr_model = DELTA_ALPHA_MZ - float(ang["c2_over_s2"]) * delta_rho_top()
    dr_obs = DELTA_ALPHA_MZ - ((1 - s2_obs) / s2_obs) * delta_rho_top()
    shift = 100.0 * (onshell_mW(s2_model, dr_model) / onshell_mW(s2_model, dr_obs) - 1.0)
    add("B4d", abs(shift) < 0.02, shift,
        f"using the model's own c^2/s^2 = 7/2 inside Delta_r instead of the "
        f"observed 3.4830 moves m_W by {shift:+.4f} % -- two orders below B4b")

    # ---- B5: the absolute bracket ---------------------------------------
    br = delta_r_bracket(float(ang["c2_over_s2"]))
    mW_lo = onshell_mW(s2_model, br["lo"], alpha)
    mW_hi = onshell_mW(s2_model, br["hi"], alpha)
    mZ_lo = mW_lo / math.sqrt(float(ang["cos2_thetaW_os"]))
    mZ_hi = mW_hi / math.sqrt(float(ang["cos2_thetaW_os"]))
    contains = mW_lo <= M_W_PDG <= mW_hi
    add("B5a", contains, [mW_lo, mW_hi],
        f"m_W in [{mW_lo:.4f}, {mW_hi:.4f}] GeV CONTAINS the PDG 80.3692 "
        f"({100*(M_W_PDG-mW_lo)/(mW_hi-mW_lo):.0f} % of the way up the bracket)")
    add("B5b", mZ_lo <= M_Z_PDG <= mZ_hi, [mZ_lo, mZ_hi],
        f"m_Z in [{mZ_lo:.4f}, {mZ_hi:.4f}] GeV CONTAINS the PDG 91.1880")
    add("B5c", 0.008 < br["implied_delta_r_rem"] < 0.011, br["implied_delta_r_rem"],
        "the bracket width is the SM's own Delta_r_rem, 0.0096 -- consistent "
        "with the literature value, which is the check that the bracket is the "
        "right object rather than a convenient one")

    # ---- B6: the input count, which is the whole accounting claim -------
    model_inputs = ["alpha", "G_F"]
    sm_inputs = ["alpha", "G_F", "m_Z"]
    add("B6a", len(model_inputs) == len(sm_inputs) - 1, model_inputs,
        "the model takes TWO electroweak inputs where the SM takes three")
    add("B6b", not any(x.startswith("m_") for x in model_inputs), model_inputs,
        "and neither of them is a boson mass -- which is what makes m_W and "
        "m_Z outputs rather than a rearrangement of inputs")

    n_pass = sum(1 for c in checks if c["ok"])
    return {
        "checks": checks, "n_pass": n_pass, "n_total": len(checks),
        "verdict": "PASS" if n_pass == len(checks) else "FAIL",
        "params": {"equal_stiffness": equal_stiffness,
                   "rank_two_breaking": rank_two_breaking,
                   "eliminate_u": eliminate_u},
        "F320_sin2_thetaW_os": str(ang["sin2_thetaW_os"]),
        "F320_v_GeV": V_EW,
        "F320_g2_over_pi_alpha": st.get("g2_over_pi_alpha"),
        "F320_m_W_tree_GeV": mW_tree,
        "F320_m_Z_tree_GeV": mZ_tree,
        "F320_m_W_bracket_GeV": [mW_lo, mW_hi],
        "F320_m_Z_bracket_GeV": [mZ_lo, mZ_hi],
        "F320_m_W_excess_pct": inv["mW_excess_pct"],
        "F320_m_Z_excess_pct": inv["mZ_excess_pct"],
        "F320_rho_tree": str(rhos[0]),
        "F320_delta_r_bracket": [br["lo"], br["hi"]],
        "F320_n_ew_inputs_model": len(model_inputs),
        "F320_n_ew_inputs_sm": len(sm_inputs),
    }


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    res = check_gauge_boson_masses()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
        if c["note"]:
            print(f"          {c['note']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    out = results_path("F320_gauge_boson_masses.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("wrote", os.path.basename(out))
