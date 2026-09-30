"""
gravity_four_derivative_locality.py -- does lattice locality FORBID the
four-derivative (curvature-squared) term in the induced gravitational
action, or does it merely SUPPRESS it as an ordinary EFT/Wilsonian tower?

Target: rubric row E1 / ledger row E1g (`docs/status/open-derivations.md`
Part C), the residual F345 L7 named inside the surviving posit: "at-most-
second-order is not a premise the model satisfies exactly ... it holds to
~1e-76 x O(1) with the O(1) uncomputed." This module asks whether the
EXISTENCE of that O(1) coefficient can be forced to zero by locality (the
lattice's finite-range coupling / compact Brillouin zone) -- which would
promote at-most-second-order from posit to derivation -- or whether it is
generically nonzero, which instead closes the sub-item NEGATIVE: the
truncation is provably not exact, only parametrically small, and locality
is the reason the tower is finite term-by-term, not the reason it stops.

The route re-uses F57's own machinery rather than inventing new machinery.
F57 (`gr_fork_F57_induced_eh_from_backreaction.py`) computes the two-
derivative (Einstein-Hilbert) coefficient as the q^2 piece of the static
matter-density polarization

    Pi(q) = int_BZ d^3k/(2 pi)^3 . 1/(omega(k) + omega(k+q))

over the model's own F26/BCC dispersion omega(k) (`casim.engine.lattice.
bcc.bcc_dispersion`), Taylor-expanded in small q:

    Pi(q) = Pi_0 - Pi_2 q^2 + Pi_4 q^4 - ...

Pi_0 is the vacuum-energy/Lambda sector (F56); Pi_2 > 0 is the induced
Einstein-Hilbert (Newton-constant) kinetic term (F57 measured Pi_2 =
+0.061, UV-finite, log-running). Pi_4 is the NEXT term in the SAME
derivative expansion -- in position space it multiplies (nabla^2 Phi)^2,
the four-derivative analogue of a curvature-squared operator in this
scalar/rest-leg channel. If the identical finite, UV-controlled BZ
integral that gives F57's nonzero Pi_2 also gives a nonzero, well-
converged Pi_4, that is a direct, model-native demonstration that the
lattice's locality GENERATES the higher-derivative tower rather than
forbidding it -- exactly the ordinary Wilsonian/EFT expectation (locality
is why a derivative expansion converges term-by-term, not why it
truncates), and the opposite of what would be needed to promote
at-most-second-order to a derivation.

What this module does NOT do: it does not compute the full nonlinear
curvature-squared (R^2, Ricci^2) Wilson coefficient of the gravitational
effective action -- that needs the tensor T_ij T_kl (kinetic-leg, F55)
channel F57 itself left open, not the scalar density channel used here.
Pi_4 is a proxy: the SAME kind of object, in the ONE channel the model
tree has actually computed at two-derivative order, extended one order
further. A nonzero Pi_4 does not by itself supply the number in F345 L4 --
it answers the narrower, prior question of whether such a number can be
forced to zero by locality alone. It cannot: nothing in the construction
gives Pi_4 (or Pi_2n for any n) a reason to vanish identically, and the
d=4 Gauss-Bonnet cancellation that makes L3's curvature-squared term
topological (F345 S4) is a property of the FULL diffeomorphism-invariant
curvature-squared invariant under metric variation, not of this scalar
polarization -- so it supplies no analogous protection here.

What Pi_4's precision actually supports (added after adversarial review):
only its SIGN and order of magnitude, not the specific figures the M2 leg
reports. A bare quartic (order=4) fit is ill-conditioned at the q-scales
used here -- adding a q^6 term (leg M2b) shifts every variant's |Pi_4| by
~2.6-3x while never flipping its sign. Confirmed independently by a cold
blind-rederivation subagent (which needed the same q^6 correction to
stabilize its own estimate) and by this session's adversarial referee (who
reran M2's own four variants at order=6 and found the identical shift).
M2b is kept as a permanent regression check of the part that DOES survive
(sign, and magnitude within an 8x band), not just a one-off verification.

Findings: F383 (this). Builds on F56 (Einstein coupling from lattice
phase matching), F57 (induced EH term from leg-field back-reaction, whose
Pi(q) machinery is extended here to next order), F345 (the residual this
answers, L4/L7), F319 (Wilsonian/EFT reading of the BZ cutoff, the sibling
uncomputed-coefficient statement for the matter sector).
"""

from __future__ import annotations

import json

from casim.numerics import xp as np

from casim.engine.lattice import bcc as _bcc
from casim.engine.particles._results_path import results_path

__all__ = [
    "static_polarization", "polarization_taylor_fit",
    "leg_M1_pi2_regression", "leg_M2_pi4_robust_nonzero",
    "leg_M2b_pi4_sign_survives_q6",
    "leg_M3_pi4_grid_convergence", "leg_M4_pi4_cutoff_scaling",
    "leg_M5_pi4_direction_spread", "leg_L_conclusion",
    "run_all", "check_locality_does_not_forbid",
]


# ===========================================================================
# The Brillouin-zone polarization, extended to its q^4 (quartic) order
# ===========================================================================

def static_polarization(q_vec, n_grid=96, Lambda=np.pi, sign="+"):
    """Pi(q) = int_BZ d^3k/(2 pi)^3 . 1/(omega(k)+omega(k+q)) over the
    CANONICAL F26/BCC dispersion (`casim.engine.lattice.bcc.bcc_dispersion`).
    Grid quadrature on a cube [-Lambda, Lambda)^3 -- F57's BZ proxy, kept
    identical here so the two calculations are directly comparable."""
    g = np.linspace(-Lambda, Lambda, n_grid, endpoint=False) + Lambda / n_grid
    KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
    w1 = _bcc.bcc_dispersion(KX, KY, KZ, sign=sign)
    w2 = _bcc.bcc_dispersion(KX + q_vec[0], KY + q_vec[1], KZ + q_vec[2], sign=sign)
    denom = w1 + w2
    integ = np.where(denom > 1e-9, 1.0 / denom, 0.0)
    dk = g[1] - g[0]
    return float(integ.sum() * dk ** 3 / (2.0 * np.pi) ** 3)


def polarization_taylor_fit(n_grid=128, Lambda=np.pi,
                            qmags=(0.02, 0.04, 0.06, 0.08, 0.10, 0.12),
                            direction=(1.0, 0.0, 0.0), order=4, sign="+"):
    """Fit Pi(q) = Pi0 - Pi2 q^2 + Pi4 q^4 [- Pi6 q^6] along `direction` by
    ordinary least squares over `qmags`. Returns fitted coefficients, the
    raw samples, and the fit quality (R^2), so a caller can see whether the
    extra term is doing real work or fitting noise."""
    v = np.asarray(direction, dtype=np.float64)
    v = v / np.linalg.norm(v)
    qs = np.asarray(qmags, dtype=np.float64)
    Pq = np.array([static_polarization(qq * v, n_grid=n_grid, Lambda=Lambda,
                                       sign=sign) for qq in qs])
    powers = list(range(0, order + 1, 2))          # [0,2,4] or [0,2,4,6]
    A = np.vstack([qs ** p for p in powers]).T
    coef, _res, _rank, _sv = np.linalg.lstsq(A, Pq, rcond=None)
    fit = A @ coef
    resid = Pq - fit
    ss_res = float((resid ** 2).sum())
    ss_tot = float(((Pq - Pq.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    out = {
        "powers": powers, "coef": [float(c) for c in coef],
        "Pq": [float(x) for x in Pq], "qmags": [float(x) for x in qs],
        "ss_res": ss_res, "r2": r2, "n_grid": n_grid, "Lambda": float(Lambda),
        "direction": [float(x) for x in v],
    }
    out["Pi0"] = out["coef"][0]
    if len(out["coef"]) > 1:
        out["Pi2"] = -out["coef"][1]
    if len(out["coef"]) > 2:
        out["Pi4"] = out["coef"][2]
    return out


# ===========================================================================
# M1 -- regression: the quartic fit still reproduces F57's Pi2
# ===========================================================================

def leg_M1_pi2_regression():
    """Extending the fit to include a q^4 term must not disturb the
    already-reviewed Pi2 result (F57: Pi2 = +0.061, UV-finite, correct
    sign). This is a continuity guard, not new content."""
    fit2 = polarization_taylor_fit(n_grid=96, Lambda=np.pi,
                                   qmags=(0.04, 0.08, 0.12, 0.16),
                                   order=2)
    fit4 = polarization_taylor_fit(n_grid=96, Lambda=np.pi,
                                   qmags=(0.04, 0.08, 0.12, 0.16),
                                   order=4)
    pi2_2 = fit2["Pi2"]
    pi2_4 = fit4["Pi2"]
    close = abs(pi2_4 - pi2_2) < 0.5 * max(abs(pi2_2), 1e-9)
    sign_ok = pi2_2 > 0 and pi2_4 > 0
    f57_order = 0.5 < pi2_2 / 0.061 < 3.0 or 0.02 < pi2_2 < 0.3
    return {
        "leg": "M1", "claim": "quartic fit reproduces F57's Pi2 (sign, order of magnitude)",
        "Pi2_quadratic_fit": pi2_2, "Pi2_quartic_fit": pi2_4,
        "F57_reference_Pi2": 0.061,
        "consistent_with_F57_order": bool(f57_order),
        "pass": bool(close and sign_ok),
    }


# ===========================================================================
# M2 -- Pi4 nonzero and robust across independent settings
# ===========================================================================

def _m2_variants(order):
    """The four M2 configurations (baseline, finer grid, different q-window,
    different direction) at a given fit order. Factored out so M2 (order=4)
    and M2b (order=6, the adversarial-review perturbation) run the identical
    settings and differ only in the one thing being tested."""
    base = polarization_taylor_fit(n_grid=110, Lambda=np.pi,
                                   qmags=(0.03, 0.06, 0.09, 0.12, 0.15),
                                   direction=(1, 0, 0), order=order)
    finer_grid = polarization_taylor_fit(n_grid=170, Lambda=np.pi,
                                         qmags=(0.03, 0.06, 0.09, 0.12, 0.15),
                                         direction=(1, 0, 0), order=order)
    diff_window = polarization_taylor_fit(n_grid=110, Lambda=np.pi,
                                          qmags=(0.05, 0.10, 0.15, 0.20, 0.25),
                                          direction=(1, 0, 0), order=order)
    diff_direction = polarization_taylor_fit(n_grid=110, Lambda=np.pi,
                                             qmags=(0.03, 0.06, 0.09, 0.12, 0.15),
                                             direction=(1, 1, 1), order=order)
    return {"baseline": base, "finer_grid": finer_grid,
           "diff_window": diff_window, "diff_direction": diff_direction}


def leg_M2_pi4_robust_nonzero():
    """Compute Pi4 at a baseline configuration and at three independent
    perturbations (finer grid, different q-window, different direction), all
    at a quartic (order=4) fit. PASS iff all four agree in SIGN and lie
    within a factor of 5 of each other -- i.e. Pi4 is a real, well-determined
    feature of the BZ integral, not fit noise. This is the leg the whole
    finding turns on for SIGN; see M2b for why the specific MAGNITUDES here
    are not separately load-bearing (a quartic-only fit is ill-conditioned at
    these q-scales -- adding a q^6 term shifts each variant's magnitude by
    ~2.6-3x, sign-preserving, found independently by both this session's
    blind-rederivation subagent and its adversarial referee)."""
    variants = _m2_variants(order=4)
    pi4s = {k: v["Pi4"] for k, v in variants.items()}
    signs = {k: (v > 0) for k, v in pi4s.items()}
    same_sign = len(set(signs.values())) == 1
    vals = list(pi4s.values())
    magnitudes = [abs(v) for v in vals]
    ratio = (max(magnitudes) / min(magnitudes)) if min(magnitudes) > 0 else float("inf")
    within_band = ratio < 5.0
    r2_ok = all(v["r2"] > 0.9 for v in variants.values())
    return {
        "leg": "M2",
        "claim": "Pi4 is nonzero and has a robust SIGN across grid, window and direction perturbations at a quartic fit "
                 "(magnitude is order-of-magnitude only -- see M2b)",
        "Pi4_by_variant": pi4s, "same_sign": bool(same_sign),
        "magnitude_ratio_max_over_min": ratio, "within_5x_band": bool(within_band),
        "fit_r2_by_variant": {k: v["r2"] for k, v in variants.items()},
        "fit_quality_ok": bool(r2_ok),
        "pass": bool(same_sign and within_band and r2_ok),
    }


def leg_M2b_pi4_sign_survives_q6():
    """Adversarial-review perturbation, kept as a permanent check rather than
    a one-off: rerun M2's identical four variants with a q^6 term ADDED to
    the fit (order=6 instead of order=4). A cold subagent's independent
    reimplementation found a bare quartic fit is ill-conditioned at these
    q-scales (q^2 and q^4 are nearly degenerate over a narrow small-q
    window), and this session's adversarial referee confirmed it on these
    EXACT settings: every variant's |Pi4| shifts by ~2.6-3x when order=6 is
    used instead of order=4. What survives that shift: the SIGN (never
    flips, in either this leg or the referee's run) and the order of
    magnitude (the referee's order=6 ratio was 3.5x, inside an 8x band held
    here with margin). What does NOT survive: the specific 3-sig-fig values
    M2 reports -- those are a fit-order artifact, not a converged number,
    and are not claimed as precise anywhere in this finding."""
    variants4 = _m2_variants(order=4)
    variants6 = _m2_variants(order=6)
    pi4_4 = {k: v["Pi4"] for k, v in variants4.items()}
    pi4_6 = {k: v["Pi4"] for k, v in variants6.items()}
    signs6 = {k: (v > 0) for k, v in pi4_6.items()}
    same_sign6 = len(set(signs6.values())) == 1
    sign_matches_order4 = all((pi4_4[k] > 0) == (pi4_6[k] > 0) for k in pi4_4)
    mags6 = [abs(v) for v in pi4_6.values()]
    ratio6 = (max(mags6) / min(mags6)) if min(mags6) > 0 else float("inf")
    shift_factors = {k: (pi4_6[k] / pi4_4[k]) if pi4_4[k] != 0 else float("inf")
                     for k in pi4_4}
    return {
        "leg": "M2b",
        "claim": "Pi4's SIGN (not its magnitude) survives adding a q^6 term to the fit -- the adversarial-review perturbation",
        "Pi4_order4_by_variant": pi4_4, "Pi4_order6_by_variant": pi4_6,
        "shift_factor_order6_over_order4": shift_factors,
        "same_sign_at_order6": bool(same_sign6),
        "sign_matches_order4": bool(sign_matches_order4),
        "magnitude_ratio_order6_max_over_min": ratio6, "within_8x_band": bool(ratio6 < 8.0),
        "pass": bool(same_sign6 and sign_matches_order4 and ratio6 < 8.0),
    }


# ===========================================================================
# M3 -- Pi4 is finite under grid refinement (a genuine BZ integral, not a
#        quadrature artifact)
# ===========================================================================

def leg_M3_pi4_grid_convergence():
    """Pi4 at increasing n_grid (fixed Lambda, fixed q-window) should
    converge, not blow up -- confirming it is a well-defined finite lattice
    integral rather than an artifact of coarse quadrature."""
    ngrids = (64, 96, 128, 160)
    qmags = (0.04, 0.08, 0.12, 0.16)
    pi4s = []
    for ng in ngrids:
        fit = polarization_taylor_fit(n_grid=ng, Lambda=np.pi, qmags=qmags, order=4)
        pi4s.append(fit["Pi4"])
    rel_changes = [abs(pi4s[i] - pi4s[i - 1]) / max(abs(pi4s[i - 1]), 1e-12)
                  for i in range(1, len(pi4s))]
    converging = rel_changes[-1] < rel_changes[0] + 1e-6 or rel_changes[-1] < 0.15
    finite = all(abs(p) < 1e6 for p in pi4s)
    return {
        "leg": "M3", "claim": "Pi4 converges under grid refinement (finite BZ integral, not a quadrature artifact)",
        "n_grids": list(ngrids), "Pi4_values": pi4s, "relative_changes": rel_changes,
        "pass": bool(converging and finite),
    }


# ===========================================================================
# M4 -- cutoff scaling of Pi4 (descriptive, parallel to F57's K3)
# ===========================================================================

def leg_M4_pi4_cutoff_scaling():
    """How Pi4 scales with a spherical cutoff Lambda -- the same diagnostic
    F57 ran for Pi0 (~Lambda^2) and Pi2 (~log Lambda). Grid resolution is
    scaled with Lambda to hold the quadrature spacing dk roughly fixed, and
    the q-window is held FIXED in absolute terms (not rescaled with
    Lambda), so every cutoff probes the same small-q regime. Descriptive:
    no specific exponent is required for the finding's conclusion, only
    that Pi4 stays finite and well-defined at every cutoff tested."""
    Lambdas = np.array([1.2, 1.6, 2.0, 2.4, 2.8])
    qmags = (0.03, 0.05, 0.07)
    pi4s = []
    for L in Lambdas:
        ng = int(round(110 * float(L) / 2.0))
        fit = polarization_taylor_fit(n_grid=ng, Lambda=float(L), qmags=qmags, order=4)
        pi4s.append(fit["Pi4"])
    pi4s = np.array(pi4s)
    finite = bool(np.all(np.isfinite(pi4s)))
    monotone_ish = bool(np.all(np.diff(pi4s) <= 0) or np.all(np.diff(pi4s) >= 0))
    try:
        exponent = float(np.polyfit(np.log(Lambdas), np.log(np.abs(pi4s)), 1)[0])
    except Exception:
        exponent = None
    return {
        "leg": "M4", "claim": "Pi4 stays finite across a swept spherical cutoff (descriptive scaling)",
        "Lambdas": [float(x) for x in Lambdas], "Pi4_values": [float(x) for x in pi4s],
        "log_log_exponent": exponent, "monotone": monotone_ish,
        "caveat": (
            "Pi4 is flat to 4 significant figures over Lambda=1.2-2.4 (plausible "
            "genuine UV convergence, as F57 K1 found for Pi0) then jumps at "
            "Lambda=2.8 -- not fully diagnosed (likely a cube-domain quadrature "
            "artifact as the window approaches the BZ proxy edge at pi), and NOT "
            "load-bearing for the M2/L conclusion, which does not use this leg. "
            "Flagged rather than smoothed over; a follow-up owes a cleaner "
            "spherical-restriction cutoff study, as F57's own fork used."
        ),
        "pass": bool(finite),
    }


# ===========================================================================
# M5 -- direction dependence of Pi4 (descriptive: is the quartic term
#        close to isotropic, i.e. R^2-like, or does it carry a genuinely
#        anisotropic lattice piece at this order?)
# ===========================================================================

def leg_M5_pi4_direction_spread():
    """Measure Pi4 along three non-equivalent BCC directions. Reported
    honestly either way: isotropy is not required for M2's conclusion
    (nonzero, hence not locality-forbidden) to hold, only for the specific
    reading of Pi4 as an R^2-type invariant rather than a lattice-anisotropy
    artifact."""
    qmags = (0.04, 0.08, 0.12, 0.16)
    dirs = {"axis_100": (1, 0, 0), "face_diag_110": (1, 1, 0), "body_diag_111": (1, 1, 1)}
    pi4s = {}
    for name, d in dirs.items():
        fit = polarization_taylor_fit(n_grid=110, Lambda=np.pi, qmags=qmags,
                                      direction=d, order=4)
        pi4s[name] = fit["Pi4"]
    vals = list(pi4s.values())
    same_sign = len({v > 0 for v in vals}) == 1
    spread = (max(vals) - min(vals)) / max(abs(np.mean(vals)), 1e-12)
    return {
        "leg": "M5", "claim": "direction dependence of Pi4 across axis/face-diagonal/body-diagonal directions",
        "Pi4_by_direction": pi4s, "same_sign": bool(same_sign),
        "fractional_spread": float(spread),
        "isotropic_to_20pct": bool(spread < 0.20),
        "pass": bool(same_sign),
    }


# ===========================================================================
# L -- the structural conclusion this finding rests on
# ===========================================================================

def leg_L_conclusion(m2):
    """Not a new computation: states what M2's result entails for the
    residual F345 L7 names. If Pi4 is robustly nonzero (M2 PASS), the exact
    at-most-second-order restriction is NOT enforced by locality -- the same
    finite BZ mechanism that generates the accepted two-derivative term
    generates the four-derivative one too, with no analogue of L3's d=4
    Gauss-Bonnet protection available in this channel (that protection is a
    property of the full nonlinear curvature-squared invariant under metric
    variation, not of a scalar polarization function)."""
    pi4_nonzero = bool(m2["pass"])
    return {
        "leg": "L", "claim": "locality does not forbid the four-derivative term; it generates it",
        "depends_on": "M2",
        "conclusion": (
            "at-most-second-order is NOT derivable from lattice locality/cone "
            "structure. The identical finite Brillouin-zone integral that "
            "F57 already used to induce a nonzero two-derivative (Einstein- "
            "Hilbert) coefficient produces a nonzero four-derivative "
            "coefficient at the next order, with no symmetry found (or "
            "expected) to force it to vanish in this channel. This closes "
            "the specific sub-question F345 S4 left open -- 'does locality "
            "forbid higher-derivative terms' -- in the negative: locality is "
            "why each term in the tower is UV-finite, not why the tower "
            "stops. The at-most-second-order premise inside F345 L7 remains "
            "what F345 already called it: an EFT truncation, suppressed by "
            "~1e-76 x an O(1) coefficient that is now known to be structurally "
            "nonzero (in the one channel computed here), not exactly zero."
        ) if pi4_nonzero else (
            "Pi4 was not robustly established as nonzero by this module's "
            "checks; the locality-forbids-higher-derivative-terms question "
            "is NOT settled by this attempt."
        ),
        "pass": pi4_nonzero,
    }


def run_all():
    m1 = leg_M1_pi2_regression()
    m2 = leg_M2_pi4_robust_nonzero()
    m2b = leg_M2b_pi4_sign_survives_q6()
    m3 = leg_M3_pi4_grid_convergence()
    m4 = leg_M4_pi4_cutoff_scaling()
    m5 = leg_M5_pi4_direction_spread()
    lc = leg_L_conclusion(m2)
    legs = [m1, m2, m2b, m3, m4, m5, lc]
    n_pass = sum(1 for l in legs if l["pass"])
    return {
        "finding": "F383",
        "title": "Locality generates, not forbids, the four-derivative curvature term: "
                 "the F57 Pi(q) mechanism gives a nonzero Pi4 at the next order",
        "target": "rubric row E1 / ledger E1g, the at-most-second-order sub-item inside F345 L7",
        "carried_not_reattacked": (
            "F345's own residual accounting (one premise plus two open sub-items); "
            "the metric-only-LHS sub-item (untouched here); F345 L3's d=4 Gauss-Bonnet "
            "result (a different, nonlinear-invariant statement, not re-derived or contradicted)"
        ),
        "checks": legs,
        "legs": legs,
        "n_pass": n_pass,
        "n_legs": len(legs),
        "all_pass": bool(n_pass == len(legs)),
    }


def check_locality_does_not_forbid(**_ignored):
    """Registry entry point. Returns the leg payload; does not raise on a
    reddened leg (the runner reads `all_pass`)."""
    result = run_all()
    assert isinstance(result.get("all_pass"), bool), (
        "run_all() must return a boolean 'all_pass' key")
    return result


if __name__ == "__main__":
    res = run_all()
    out = results_path("F383_four_derivative_locality.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(json.dumps({k: v for k, v in res.items() if k != "legs"}, indent=2, default=str))
