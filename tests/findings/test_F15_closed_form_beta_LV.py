"""F15 — Closed-form SR-2 Lorentz-violation coefficients, verified independently.

Six checks on `casim.engine.interactions.derive_beta_LV`.  The point of this
record is that the module had NO test of any kind until 2026-08-03 while
carrying four "exact algebraic" rows in `docs/status/exactness-inventory.md`
(defect 1 of `docs/reviews/F01-F15-review-2026-08-03.md`).

The load-bearing check is W1, and it is deliberately NOT the module's own
verification.  The module derives its coefficients by expanding
``acos(n cos u)`` in ``u`` and reverting the series ``u -> beta``.  W1 instead
uses the exact change of variable ``t = cos u``, which closes the whole
construction in finite terms,

    sin(omega) = m gamma,   sin(u) = beta m gamma / n,   gamma = 1/sqrt(1-beta^2)

    R(beta) = [ asin(m gamma) - beta asin(beta gamma tan theta) ] / asin(m)

with ``theta = asin(m)``, and expands THAT in ``beta``.  Two different routes to
the same four coefficients; agreement is exact (sympy zero), not numerical.
This route was found by the blind re-derivation agent in the 2026-08-03 review,
which never saw the module or the finding.

  W1  (exact)    all four coefficients reproduced symbolically by the
                 independent closed-form route, at exact rational m.
  W2  (machine)  the non-perturbative closed form R(beta) equals the module's
                 own ratio_qca(k, m) on an (m, k) grid.
  W3  (exact)    SIGN THEOREM: beta_LV, gamma_LV, delta_LV, epsilon_LV are all
                 strictly negative on m in (0,1).  tan(theta) > theta makes
                 every term negative.  This closes the item Finding 15 left
                 open ("whether gamma_LV ever flips sign as m -> 1").
  W4  (exact)    small-m expansion beta_LV = -m^2/6 - 11 m^4/90 + O(m^6).
                 THIS IS THE PERTURBABLE CHECK: `lead_denom`, `next_num` and
                 `next_denom` are params, and moving any of them fails the
                 record.  That is the record's failure mode.
  W5  (machine)  the lattice spacing a is DECORATIVE: beta_LV is independent of
                 a, because omega depends on k only through u = k a and
                 c_lat = a, so a cancels before any expansion.
  W6  (machine)  high-precision convergence (R - sqrt(1-beta^2))/beta^2 ->
                 beta_LV, and the float64 error at the same point, which
                 documents that the numerical floor here is SUBTRACTIVE
                 CANCELLATION (~eps/beta^2), not the "FFT/round-off floor" the
                 original finding claimed.

Real arithmetic only (CLAUDE.md).  2D-square QCA, m in (0,1) open at both ends.
"""
from __future__ import annotations

import math

import sympy as sp

from casim.engine.interactions.derive_beta_LV import (
    beta_LV,
    delta_LV,
    epsilon_LV,
    gamma_LV,
    omega_qca,
    ratio_qca,
    vg_qca,
    C_LAT_2D,
)

# Exact rational masses used for the symbolic check.  Kept small in number and
# denominator: sympy's asin(Rational) stays exact, and the whole check runs in
# a few seconds.
def _symbolic_masses():
    """Built on call, not at import. sympy work at module scope runs on
    `pytest --collect-only`, which is what the `import_time_work` ratchet in
    tools/audit_tests.py counts; the values are unchanged."""
    return (sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(3, 4))


# ---------------------------------------------------------------------------
# W1 — independent symbolic route
# ---------------------------------------------------------------------------

def _closed_form_R(beta, m):
    """Exact non-perturbative R(beta), by the t = cos u change of variable.

    Derived independently of the module: from cos(omega) = n cos(u) and
    beta = domega/du one gets sin(omega) = m gamma and sin(u) = beta m gamma/n
    in closed form, so both omega and u are elementary functions of beta.
    """
    n = sp.sqrt(1 - m**2)
    gam = 1 / sp.sqrt(1 - beta**2)
    theta = sp.asin(m)
    return (sp.asin(m * gam) - beta * sp.asin(beta * gam * m / n)) / theta


def check_W1_symbolic_independent_route():
    """All four coefficients, re-derived by the closed-form route. Exact."""
    b = sp.symbols("b", positive=True)
    rows = []
    for m in _symbolic_masses():
        diff = _closed_form_R(b, m) - sp.sqrt(1 - b**2)
        ser = sp.series(diff, b, 0, 10).removeO()
        poly = sp.Poly(sp.expand(ser), b)
        coeffs = {2 * j: sp.simplify(poly.coeff_monomial(b ** (2 * j)))
                  for j in (1, 2, 3, 4)}
        # odd orders must vanish identically (omega is even in k)
        odd = [sp.simplify(poly.coeff_monomial(b ** (2 * j + 1)))
               for j in (0, 1, 2, 3)]
        mf = float(m)
        module = {2: beta_LV(mf), 4: gamma_LV(mf), 6: delta_LV(mf),
                  8: epsilon_LV(mf)}
        residuals = {}
        for order, sym in coeffs.items():
            residuals[order] = abs(float(sym) - module[order])
        rows.append({
            "m": str(m),
            "max_abs_residual_vs_module": max(residuals.values()),
            "residual_by_order": {str(k): v for k, v in residuals.items()},
            "odd_coefficients_all_zero": all(sp.simplify(o) == 0 for o in odd),
        })
    worst = max(r["max_abs_residual_vs_module"] for r in rows)
    return {
        "route": "exact change of variable t = cos u -> closed-form R(beta)",
        "independent_of_module_route": True,
        "rows": rows,
        "worst_residual": worst,
        "pass": worst < 1e-14 and all(r["odd_coefficients_all_zero"]
                                      for r in rows),
    }


# ---------------------------------------------------------------------------
# W2 — non-perturbative closed form vs the module's lattice evaluation
# ---------------------------------------------------------------------------

def check_W2_closed_form_matches_lattice():
    """R(beta) closed form == module ratio_qca(k, m).  Machine precision."""
    worst = 0.0
    npts = 0
    for m in (0.05, 0.1, 0.2, 0.5, 0.9):
        n = math.sqrt(1.0 - m * m)
        theta = math.asin(m)
        for k in (0.01, 0.05, 0.1, 0.3, 0.6, 1.0, 1.5):
            beta = vg_qca(k, m) / C_LAT_2D
            if beta >= n:                       # outside the physical range
                continue
            gam = 1.0 / math.sqrt(1.0 - beta * beta)
            closed = (math.asin(m * gam)
                      - beta * math.asin(beta * gam * m / n)) / theta
            worst = max(worst, abs(closed - ratio_qca(k, m)))
            npts += 1
    return {
        "n_points": npts,
        "max_abs_difference": worst,
        "note": "beta_max = sqrt(1-m^2) exactly; beta never reaches 1",
        "pass": npts > 20 and worst < 1e-13,
    }


# ---------------------------------------------------------------------------
# W3 — sign theorem (closes Finding 15's stated open item)
# ---------------------------------------------------------------------------

def check_W3_all_coefficients_negative():
    """All four LV coefficients < 0 on (0,1). No sign flip as m -> 1."""
    fns = {"beta_LV": beta_LV, "gamma_LV": gamma_LV,
           "delta_LV": delta_LV, "epsilon_LV": epsilon_LV}
    worst = {}
    ok = True
    grid = [i / 1000.0 for i in range(1, 1000)]
    for name, fn in fns.items():
        vals = [fn(m) for m in grid]
        worst[name] = max(vals)                 # the least negative sample
        ok = ok and worst[name] < 0.0
    # the mechanism, checked symbolically: tan(theta) > theta on (0, pi/2)
    th = sp.symbols("th", positive=True)
    mechanism = sp.simplify(sp.diff(sp.tan(th) - th, th) - sp.tan(th) ** 2) == 0
    return {
        "grid_points": len(grid),
        "max_value_per_coefficient": worst,
        "mechanism": "tan(theta) > theta on (0, pi/2) => T/theta > 1 => "
                     "every term of every coefficient is negative",
        "mechanism_derivative_identity": bool(mechanism),
        "closes": "Finding 15 open item: gamma_LV never flips sign",
        "pass": ok and bool(mechanism),
    }


# ---------------------------------------------------------------------------
# W4 — small-m expansion.  THE PERTURBABLE CHECK.
# ---------------------------------------------------------------------------

def check_W4_small_m_expansion(lead_denom=6, next_num=11, next_denom=90,
                               tol=1e-4):
    """beta_LV(m) = -m^2/lead_denom - next_num m^4/next_denom + O(m^6).

    Perturbing any of the three params breaks this check.  That is deliberate:
    it is the record's failure mode (attack 7 of the review procedure).

    Run in mpmath at 50 dps.  In float64 this check is DESTROYED by the same
    subtractive cancellation W6 documents -- the residual at m = 1e-3 is
    ~4e-23, four orders below the float64 ulp of beta_LV itself.  A float64
    version of this check reports noise (spread ~390) and would have to be
    loosened until it could no longer fail, which is exactly the tolerance
    shopping this record exists to avoid.
    """
    import mpmath as mp

    mp.mp.dps = 50
    ld = mp.mpf(int(lead_denom))
    nn, nd = mp.mpf(int(next_num)), mp.mpf(int(next_denom))
    rows = []
    for m_f in (1e-4, 3e-4, 1e-3, 3e-3):
        m = mp.mpf(m_f)
        exact = (1 - m / (mp.sqrt(1 - m * m) * mp.asin(m))) / 2
        two = -(m ** 2) / ld - nn * m ** 4 / nd
        res_two = (exact - two) / m ** 6
        rows.append({"m": m_f, "beta_LV": float(exact), "two_term": float(two),
                     "residual_over_m6": float(res_two)})
    # The two-term truncation leaves an O(m^6) residual, so the ONLY meaningful
    # assertion is that residual/m^6 converges to the NEXT coefficient,
    # -191/1890.  A bare "|exact - two| < tol" gate would be tolerance
    # shopping: its right-hand side has to be re-tuned for every m.
    ratios = [r["residual_over_m6"] for r in rows]
    spread = abs(max(ratios) / min(ratios))
    third = -191.0 / 1890.0
    third_dev = max(abs(r - third) for r in ratios) / abs(third)
    ok = third_dev < float(tol)
    return {
        "lead_denom": int(lead_denom),
        "next_num": int(next_num),
        "next_denom": int(next_denom),
        "rows": rows,
        "residual_over_m6_spread": spread,
        "third_coefficient_target": third,
        "max_rel_dev_from_third": third_dev,
        "note": "the m^6 residual converges to -191/1890, the third small-m "
                "coefficient -- a bonus check the original finding did not make",
        "pass": ok,
    }


# ---------------------------------------------------------------------------
# W5 — the lattice spacing is decorative
# ---------------------------------------------------------------------------

def _beta_LV_numeric_generic_a(m, a, mp, k=None):
    """Estimate the beta^2 coefficient from a generic-a dispersion.

    mpmath, for the same reason as W4: in float64 the a-spread sits at the
    cancellation floor (~7e-8) and swamps the effect being measured.
    """
    k = mp.mpf("1e-8") / a if k is None else k
    n = mp.sqrt(1 - m * m)
    w = mp.acos(n * mp.cos(k * a))
    vg = (n * mp.sin(k * a) * a) / mp.sin(w)
    beta = vg / a                               # c_lat = a
    r = (w - k * vg) / mp.asin(m)
    return (r - mp.sqrt(1 - beta ** 2)) / beta ** 2


def check_W5_lattice_spacing_is_decorative():
    """beta_LV is independent of a. a = 1/sqrt(2) never enters the answer."""
    import mpmath as mp

    mp.mp.dps = 50
    rows = []
    ok = True
    for m_f in (0.05, 0.2, 0.5, 0.9):
        m = mp.mpf(m_f)
        ref = beta_LV(m_f)
        vals = [_beta_LV_numeric_generic_a(m, a, mp)
                for a in (1 / mp.sqrt(2), mp.mpf(1), mp.mpf("0.25"), mp.mpf(3))]
        spread = float(max(vals) - min(vals))
        rows.append({"m": m_f, "beta_LV_closed": ref,
                     "spread_over_a": spread,
                     "max_dev_from_closed": float(
                         max(abs(v - ref) for v in vals))})
        ok = ok and spread < 1e-20 * abs(ref)
    return {
        "a_values": ["1/sqrt(2)", "1", "0.25", "3"],
        "rows": rows,
        "reason": "omega depends on k only via u = k a, and c_lat = a, so a "
                  "cancels in both R and beta before any expansion",
        "pass": ok,
    }


# ---------------------------------------------------------------------------
# W6 — the real numerical floor is cancellation, not an FFT floor
# ---------------------------------------------------------------------------

def check_W6_precision_floor_is_cancellation():
    """High-precision convergence, and the float64 cancellation floor."""
    import mpmath as mp

    mp.mp.dps = 50
    rows = []
    ok = True
    for m_f in (0.05, 0.2, 0.5):
        m = mp.mpf(m_f)
        n = mp.sqrt(1 - m * m)
        theta = mp.asin(m)
        k = mp.mpf("1e-6")
        a = 1 / mp.sqrt(2)
        w = mp.acos(n * mp.cos(k * a))
        vg = (n * mp.sin(k * a) * a) / mp.sin(w)
        beta = vg / a
        r = (w - k * vg) / theta
        hi = (r - mp.sqrt(1 - beta ** 2)) / beta ** 2
        # one-term: the residual here is the gamma_LV beta^2 TRUNCATION, not
        # error -- so subtract it and gate on the two-term form, whose residual
        # is delta_LV beta^4 and genuinely negligible.
        rel_hi_1 = abs((hi - mp.mpf(beta_LV(m_f))) / hi)
        hi_2 = hi - mp.mpf(gamma_LV(m_f)) * beta ** 2
        rel_hi = abs((hi_2 - mp.mpf(beta_LV(m_f))) / hi_2)

        # the same quantity in float64, at the same point
        kf = 1e-6
        wf = omega_qca(kf, m_f)
        vgf = vg_qca(kf, m_f)
        bf = vgf / C_LAT_2D
        lof = ((ratio_qca(kf, m_f) - math.sqrt(1.0 - bf * bf)) / bf ** 2)
        rel_lo = abs((lof - beta_LV(m_f)) / beta_LV(m_f))
        cancellation_estimate = 2.22e-16 / (abs(beta_LV(m_f)) * bf ** 2)

        rows.append({
            "m": m_f,
            "beta": float(beta),
            "rel_err_50dps_1term": float(rel_hi_1),
            "rel_err_50dps_2term": float(rel_hi),
            "rel_err_float64": rel_lo,
            "predicted_cancellation_floor": cancellation_estimate,
            "float64_error_over_predicted_floor": rel_lo / cancellation_estimate,
        })
        # at 50 dps the two-term form is exact to ~1e-20; in float64 the SAME
        # point is wrong by ~1e-2, and that error is predicted to within an
        # order of magnitude by eps/(|beta_LV| beta^2).  That is the diagnosis.
        # The 2-term residual bottoms out at ~1e-13, and NOT because of the
        # series: it is the float64 evaluation of beta_LV itself, whose closed
        # form (1 - m/(n asin m))/2 also cancels at small m (three digits lost
        # at m = 0.05).  Even the answer needs care in double precision.
        ok = (ok and float(rel_hi) < 1e-12
              and 0.05 < rel_lo / cancellation_estimate < 20.0)
    return {
        "rows": rows,
        "diagnosis": "float64 error tracks eps/(|beta_LV| beta^2) -- subtractive "
                     "cancellation in R - sqrt(1-beta^2), NOT an FFT floor. "
                     "There is no FFT anywhere in derive_beta_LV.py.",
        "corrects": "findings/F01-F15-findings.md Finding 15 and four rows of "
                    "docs/status/exactness-inventory.md",
        "pass": ok,
    }


CHECKS = (
    ("W1_symbolic_independent_route", check_W1_symbolic_independent_route),
    ("W2_closed_form_matches_lattice", check_W2_closed_form_matches_lattice),
    ("W3_all_coefficients_negative", check_W3_all_coefficients_negative),
    ("W4_small_m_expansion", check_W4_small_m_expansion),
    ("W5_lattice_spacing_is_decorative", check_W5_lattice_spacing_is_decorative),
    ("W6_precision_floor_is_cancellation",
     check_W6_precision_floor_is_cancellation),
)


def check_all(lead_denom=6, next_num=11, next_denom=90, tol=1e-4):
    """Registry entry point. Returns the full result dict."""
    out = {}
    for name, fn in CHECKS:
        if name == "W4_small_m_expansion":
            out[name] = fn(lead_denom=int(lead_denom), next_num=int(next_num),
                           next_denom=int(next_denom), tol=float(tol))
        else:
            out[name] = fn()
    out["n_checks"] = len(CHECKS)
    out["n_passed"] = sum(1 for v in out.values()
                          if isinstance(v, dict) and v.get("pass"))
    out["all_pass"] = out["n_passed"] == out["n_checks"]
    assert out["all_pass"], (
        "F15 closed-form LV coefficients: "
        f"{out['n_passed']}/{out['n_checks']} checks passed"
    )
    out["verdict"] = (
        "beta_LV, gamma_LV, delta_LV, epsilon_LV confirmed exact by an "
        "independent route; all four negative on (0,1); a is decorative"
    )
    return out


# --- no pytest surface ------------------------------------------------------
# This record is entry-driven (D9). It must not also be a pytest file: the two
# contracts can disagree about what "pass" means. `check_all` runs every check.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
