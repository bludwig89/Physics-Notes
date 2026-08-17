"""F316 — the polynomial->Laurent transfer, proved: F313's last import is gone.

F313 sec.6 cited Dubickas-Steuding Thm 2, whose descent needs
`deg f = 0 => f constant` — FALSE in a Laurent ring, since deg(1 + w^-1) = 0 and
1 + w^-1 is not a unit.  The 2026-08-13 review named that transfer, not "Abel",
as the real import.  This record verifies the in-repo replacement.

Ten checks.  The load-bearing ones are re-derived here INDEPENDENTLY of
`casim.engine.lattice.laurent_pell`: the width, the leading coefficient and the
whole descent are re-implemented from the definitions against a DIFFERENT
Q-independent direction lambda, so agreeing with the module is a real
cross-check.  A theorem that held only for one lambda would be an artifact.

  C1  (machine) GENERICITY.  The lambda-maximiser is unique, so h is additive
      and lc multiplicative — both residuals must be 0, and the maximiser gap
      must be strictly positive.
  C2  (exact)   D DETECTS UNITS, WHERE deg DOES NOT.  Asserted on the exact
      counterexample that breaks the imported hypothesis: 1 + w1^-1 has Laurent
      degree 0, is NOT a unit, and D separates it.  Both halves are asserted —
      that it is not a unit AND that D > 0.
  C3  (exact)   UNITARITY => CENTRAL SYMMETRY.  a* = a and b* = -b on every
      solution, hence h(lambda) = h(-lambda).  This is the ingredient the
      polynomial proof has no analogue of.
  C4  (machine) h_a = h_b + c.
  C5  (exact)   lc(a) = +- i lc(b) lc(u), so EXACTLY ONE of b*u +- a*i cancels
      at the top.
  C6  (exact)   b' b'' = 1 + b^2 as an exact ring identity, and
      D(1 + b^2) <= 2 D(b).
  C7  (machine) THE DESCENT.  D(b) drops by exactly 2c per step whenever
      D(b) > 0.  The decisive leg.
  C8  (exact)   THE BASE CASE.  u is not a difference of two monomials (it has
      eight), and an anti-self-adjoint monomial is a purely imaginary constant.
  C9  (exact)   THE HYPOTHESIS IS LOAD-BEARING.  At D(b) = 0 we have b = +-i,
      so 1 + b^2 = 0 and C6's identity degenerates.  Asserted, because the
      first run of this work applied the descent to the base case and the lemma
      "failed" — correctly.
  C10 (exact)   LAMBDA-INDEPENDENCE.  The verdict is unchanged under a second,
      unrelated Q-independent direction.  Without this the whole proof could be
      an artifact of one lucky lambda.

Three declared controls (D9/H2), all verified RED:

  ``--param degenerate_lambda=True``  uses lambda = (0, 1, sqrt2), which is
      BLIND to w1.  The eight cube corners collapse to four doubled values, so
      the maximiser stops being unique (C1), and 1 + w1^-1 acquires width 0
      while remaining a non-unit (C2) — which is precisely the (*) failure mode
      the whole proof exists to avoid.  NOTE: a merely Q-dependent direction
      such as (1,2,3) is NOT enough — it still separates these supports and the
      control leaks.  Blindness, not irrationality, is the real hypothesis.
  ``--param nmax=1``                only the base case is in range, so the
      descent has nothing to descend (the F298 idiom).  C7 must go red.
  ``--param drop_unitarity=True``   tests the descent on a NON-unitary pair, so
      the Newton polytopes are no longer centrally symmetric.  C3 must go red —
      this is L3, the step D-S neither has nor needs.
"""
from __future__ import annotations

import math
from fractions import Fraction as F

from casim.engine.lattice.time_signature import (
    Laurent, bcc_u, bcc_discriminant, laurent_const, laurent_mono,
)

# A DIFFERENT Q-independent direction from the module's (1, sqrt2, sqrt3).
_LAM = (1.0, math.sqrt(5.0), math.sqrt(7.0))
_LAM_ALT = (math.sqrt(11.0), 1.0, math.sqrt(3.0))     # C10's second opinion
# The control direction.  NOT merely "rational": lambda = (1,2,3) is
# Q-dependent yet still happens to separate these particular supports, so it
# leaks.  A direction only fails when it is BLIND to a lattice direction — here
# lambda_1 = 0, so w1 is invisible: the eight cube corners collapse to four
# doubled values (maximiser not unique, C1 dies) and 1 + w1^-1 acquires width 0
# while remaining a non-unit (C2 dies, which is exactly the (*) failure mode).
_LAM_DEGENERATE = (0.0, 1.0, math.sqrt(2.0))

_I = laurent_const(0, 1)
_MI = laurent_const(0, -1)
_ONE = laurent_const(1)


def _h(f, lam, s=1):
    return max(s * (m[0] * lam[0] + m[1] * lam[1] + m[2] * lam[2]) for m in f)


def _D(f, lam):
    return None if not f else _h(f, lam, 1) + _h(f, lam, -1)


def _lead(f, lam, s=1):
    m = max(f, key=lambda m: s * (m[0] * lam[0] + m[1] * lam[1] + m[2] * lam[2]))
    return m, f[m]


def _gap(f, lam, s=1):
    v = sorted((s * (m[0] * lam[0] + m[1] * lam[1] + m[2] * lam[2]) for m in f),
               reverse=True)
    return math.inf if len(v) < 2 else v[0] - v[1]


def _mul(x, y, N):
    a1, b1 = x
    a2, b2 = y
    return (a1 * a2 + (b1 * b2) * N, a1 * b2 + b1 * a2)


def _tower(nmax, drop_unitarity=False):
    u, N = bcc_u("+"), bcc_discriminant("+")
    A = (u, _MI)
    out, cur = [], (_ONE, Laurent())
    for _ in range(max(nmax, 1)):
        cur = _mul(cur, A, N)
        out.append(cur)
    if drop_unitarity:
        # Break L3 without breaking the ring arithmetic: multiply b by a
        # monomial, which destroys b* = -b (central symmetry) while leaving
        # every element a perfectly good member of R.
        shift = laurent_mono((1, 0, 0))
        out = [(a, b * shift if b else b) for a, b in out]
    return out, u, N


def _star_is(f, sign):
    return f.star() == (f if sign > 0 else f.scale((F(-1), F(0))))


# ══════════════════════════════════════════════════════════════════

def check_C1_genericity(nmax=6, degenerate_lambda=False):
    """Unique lambda-maximiser => h additive, lc multiplicative."""
    lam = _LAM_DEGENERATE if degenerate_lambda else _LAM
    tower, u, N = _tower(nmax)
    probes = [u, N] + [x for p in tower[:3] for x in p if x]
    gaps = [g for f in probes for g in (_gap(f, lam, 1), _gap(f, lam, -1))
            if g != math.inf]
    hadd, lcm = [], []
    for f in probes[:4]:
        for g in probes[:4]:
            fg = f * g
            if not fg:
                continue
            hadd.append(abs(_h(fg, lam) - _h(f, lam) - _h(g, lam)))
            cf, cg, cfg = _lead(f, lam)[1], _lead(g, lam)[1], _lead(fg, lam)[1]
            pr = (cf[0] * cg[0] - cf[1] * cg[1], cf[0] * cg[1] + cf[1] * cg[0])
            lcm.append(abs(float(cfg[0] - pr[0])) + abs(float(cfg[1] - pr[1])))
    out = {"lambda": lam, "min_gap": float(min(gaps)),
           "max_h_residual": float(max(hadd)),
           "max_lc_residual": float(max(lcm))}
    assert out["min_gap"] > 1e-9, (
        "the lambda-maximiser is NOT unique — genericity fails and neither h "
        f"nor lc is well behaved: {out}")
    assert out["max_h_residual"] < 1e-9, out
    assert out["max_lc_residual"] < 1e-12, out
    return out


def check_C2_width_detects_units_where_degree_does_not(degenerate_lambda=False):
    """D(f) = 0 iff f is a unit — on the counterexample that breaks D-S's (*)."""
    lam = _LAM_DEGENERATE if degenerate_lambda else _LAM
    counter = laurent_mono((0, 0, 0)) + laurent_mono((-1, 0, 0))   # 1 + w1^-1
    monos = [laurent_mono(e) for e in ((0, 0, 0), (2, -1, 3), (-1, -1, -1))]
    out = {"counterexample": "1 + w1^-1",
           "counterexample_is_unit": bool(len(counter) == 1),
           "counterexample_width": float(_D(counter, lam)),
           "monomial_widths": [float(_D(m, lam)) for m in monos],
           "all_monomials_are_units": all(len(m) == 1 for m in monos)}
    # BOTH halves: it really is not a unit, and D really does separate it.
    assert not out["counterexample_is_unit"], (
        f"1 + w1^-1 was read as a unit — the whole gap disappears: {out}")
    assert out["counterexample_width"] > 1e-9, (
        "D fails to separate 1 + w1^-1 from a unit, so it is no better than "
        f"the degree it replaces: {out}")
    assert all(abs(w) < 1e-12 for w in out["monomial_widths"]), out
    assert out["all_monomials_are_units"], out
    return out


def check_C3_unitarity_gives_central_symmetry(nmax=6, drop_unitarity=False):
    """a* = a, b* = -b => h(lambda) = h(-lambda).  L3, the extra ingredient."""
    tower, _, _ = _tower(nmax, drop_unitarity=drop_unitarity)
    rows, worst = [], 0.0
    for n, (a, b) in enumerate(tower, start=1):
        sa, sb = _star_is(a, +1), (_star_is(b, -1) if b else True)
        r = abs(_h(a, _LAM, 1) - _h(a, _LAM, -1))
        if b:
            r = max(r, abs(_h(b, _LAM, 1) - _h(b, _LAM, -1)))
        worst = max(worst, r)
        rows.append({"n": n, "a_self_adjoint": sa, "b_anti_self_adjoint": sb})
    out = {"rows": rows, "max_symmetry_residual": float(worst),
           "all_symmetric": all(r["a_self_adjoint"] and r["b_anti_self_adjoint"]
                                for r in rows)}
    assert out["all_symmetric"], (
        "a* = a / b* = -b fails, so the Newton polytopes are not centrally "
        f"symmetric and the Laurent descent has no footing: {out}")
    assert out["max_symmetry_residual"] < 1e-9, out
    return out


def check_C4_h_relation(nmax=6):
    """h_a = h_b + c."""
    tower, u, _ = _tower(nmax)
    c = _h(u, _LAM)
    res = [abs(_D(a, _LAM) - (_D(b, _LAM) or 0.0) - 2 * c) for a, b in tower]
    out = {"c": float(c), "max_residual": float(max(res)), "n": len(res)}
    assert out["max_residual"] < 1e-9, out
    return out


def check_C5_leading_sign(nmax=6):
    """Exactly one of b*u +- a*i cancels at the top."""
    tower, u, _ = _tower(nmax)
    c = _h(u, _LAM)
    rows = []
    for n, (a, b) in enumerate(tower, start=1):
        if not b:
            continue
        hb = _h(b, _LAM)
        tops = [(None if not x else _h(x, _LAM))
                for x in (b * u + a * _I, b * u - a * _I)]
        canc = [(t is None) or (t < hb + c - 1e-9) for t in tops]
        rows.append({"n": n, "exactly_one": bool(sum(canc) == 1)})
    out = {"rows": rows, "always_exactly_one": all(r["exactly_one"] for r in rows)}
    assert rows, out
    assert out["always_exactly_one"], out
    return out


def check_C6_product_identity(nmax=6):
    """b' b'' = 1 + b^2 exactly, and D(1 + b^2) <= 2 D(b)."""
    tower, u, _ = _tower(nmax)
    rows = []
    for n, (a, b) in enumerate(tower, start=1):
        if not b or (_D(b, _LAM) or 0.0) <= 1e-12:
            continue                      # base case: 1 + b^2 = 0, see C9
        bp, bpp = b * u + a * _I, b * u - a * _I
        tgt = _ONE + b * b
        rows.append({"n": n, "exact": bool((bp * bpp) == tgt),
                     "bounded": bool(_D(tgt, _LAM) <= 2 * _D(b, _LAM) + 1e-9)})
    out = {"rows": rows, "all_exact": all(r["exact"] for r in rows),
           "all_bounded": all(r["bounded"] for r in rows)}
    assert len(rows) >= 2, out
    assert out["all_exact"] and out["all_bounded"], out
    return out


def check_C7_descent(nmax=7):
    """THE DECISIVE LEG: D(b) drops by exactly 2c per step when D(b) > 0."""
    tower, u, _ = _tower(nmax)
    c = _h(u, _LAM)
    rows = []
    for n, (a, b) in enumerate(tower, start=1):
        db = _D(b, _LAM)
        if db is None or db <= 1e-12:
            continue
        ds = [_D(x, _LAM) for x in (b * u + a * _I, b * u - a * _I)]
        fin = [x for x in ds if x is not None]
        best = min(fin) if fin else 0.0
        rows.append({"n": n, "D_b": db, "D_after": best,
                     "strict": bool(best < db - 1e-9),
                     "drop_is_2c": bool(abs((db - best) - 2 * c) < 1e-9)})
    out = {"c": float(c), "n_live": len(rows), "rows": rows,
           "all_strict": all(r["strict"] for r in rows),
           "all_drop_2c": all(r["drop_is_2c"] for r in rows)}
    assert out["n_live"] >= 2, (
        f"fewer than two live descent steps — nothing has been descended: {out}")
    assert out["all_strict"], out
    assert out["all_drop_2c"], out
    return out


def check_C8_base_case():
    """u is not a difference of two monomials; anti-self-adjoint monomial = i*real."""
    u = bcc_u("+")
    out = {"u_monomials": len(u),
           "u_is_difference_of_two": bool(len(u) <= 2),
           "off_origin_anti_self_adjoint":
               [bool(_star_is(laurent_mono(e, (3, 5)), -1))
                for e in ((1, 0, 0), (2, -1, 3))],
           "pure_imag_const_ok": bool(_star_is(laurent_mono((0, 0, 0), (0, 7)), -1)),
           "real_const_not": bool(not _star_is(laurent_mono((0, 0, 0), (7, 0)), -1))}
    assert not out["u_is_difference_of_two"], (
        f"u has <= 2 monomials — the base case reopens: {out}")
    assert not any(out["off_origin_anti_self_adjoint"]), out
    assert out["pure_imag_const_ok"] and out["real_const_not"], out
    return out


def check_C9_hypothesis_is_load_bearing():
    """At D(b) = 0 we have b = +-i, so 1 + b^2 = 0 and C6 degenerates.

    Asserted because the first run of this work applied the descent to the base
    case and the lemma "failed" — correctly.  The hypothesis D(b) > 0 is real,
    not decoration.
    """
    tower, u, _ = _tower(2)
    a1, b1 = tower[0]                      # A itself: b = -i
    degenerate = (_ONE + b1 * b1) == Laurent()
    out = {"b_at_n1": "-i", "D_b_at_n1": float(_D(b1, _LAM)),
           "one_plus_b_squared_is_zero": bool(degenerate)}
    assert abs(out["D_b_at_n1"]) < 1e-12, out
    assert out["one_plus_b_squared_is_zero"], (
        "1 + b^2 is nonzero at the base case, so C6 would not have degenerated "
        f"and the D(b) > 0 hypothesis would be unnecessary: {out}")
    return out


def check_C10_lambda_independence(nmax=6):
    """The verdict is unchanged under a second, unrelated Q-independent lambda.

    Without this the proof could be an artifact of one lucky direction.
    """
    tower, u, _ = _tower(nmax)
    verdicts = {}
    for name, lam in (("primary", _LAM), ("alternate", _LAM_ALT)):
        c = _h(u, lam)
        drops = []
        for a, b in tower:
            db = _D(b, lam)
            if db is None or db <= 1e-12:
                continue
            ds = [_D(x, lam) for x in (b * u + a * _I, b * u - a * _I)]
            fin = [x for x in ds if x is not None]
            drops.append(abs((db - min(fin)) - 2 * c) < 1e-9)
        verdicts[name] = {"c": float(c), "n": len(drops), "all_drop_2c": all(drops)}
    out = {"verdicts": verdicts,
           "agree": bool(verdicts["primary"]["all_drop_2c"]
                         == verdicts["alternate"]["all_drop_2c"] is True)}
    assert verdicts["alternate"]["n"] >= 2, out
    assert out["agree"], (
        "the descent verdict depends on the choice of lambda — the proof would "
        f"be an artifact of one direction: {out}")
    return out


CHECKS = (
    ("C1_genericity", check_C1_genericity),
    ("C2_width_detects_units_where_degree_does_not",
     check_C2_width_detects_units_where_degree_does_not),
    ("C3_unitarity_gives_central_symmetry", check_C3_unitarity_gives_central_symmetry),
    ("C4_h_relation", check_C4_h_relation),
    ("C5_leading_sign", check_C5_leading_sign),
    ("C6_product_identity", check_C6_product_identity),
    ("C7_descent", check_C7_descent),
    ("C8_base_case", check_C8_base_case),
    ("C9_hypothesis_is_load_bearing", check_C9_hypothesis_is_load_bearing),
    ("C10_lambda_independence", check_C10_lambda_independence),
)


def check_all(nmax=7, degenerate_lambda=False, drop_unitarity=False):
    """Registry entry point.

    Three declared controls (D9/H2, `control:` on `F316-laurent-pell`):

    ``--param degenerate_lambda=True`` lambda = (0,1,sqrt2) is BLIND to w1, so
        the maximiser stops being unique and D stops detecting units.  C1/C2
        red.  (A merely Q-dependent (1,2,3) leaks — see the module docstring.)
    ``--param nmax=1``               only the base case is in range, so the
        descent has nothing to descend (F298 idiom).  C7 red.
    ``--param drop_unitarity=True``  a non-unitary pair, so the Newton polytopes
        lose central symmetry.  C3 red — that is L3, the step D-S has no
        analogue of.
    """
    kw = {
        "check_C1_genericity": {"nmax": nmax, "degenerate_lambda": degenerate_lambda},
        "check_C2_width_detects_units_where_degree_does_not":
            {"degenerate_lambda": degenerate_lambda},
        "check_C3_unitarity_gives_central_symmetry":
            {"nmax": min(nmax, 6), "drop_unitarity": drop_unitarity},
        "check_C4_h_relation": {"nmax": min(nmax, 6)},
        "check_C5_leading_sign": {"nmax": min(nmax, 6)},
        "check_C6_product_identity": {"nmax": min(nmax, 6)},
        "check_C7_descent": {"nmax": nmax},
        "check_C10_lambda_independence": {"nmax": min(nmax, 6)},
    }
    out = {}
    for name, fn in CHECKS:
        out[name] = fn(**kw.get(fn.__name__, {}))
    out["n_checks"] = len(CHECKS)
    out["import_discharged"] = (
        "Dubickas-Steuding 2004 Thm 2 — the polynomial->Laurent transfer. "
        "F313 sec.6 no longer imports anything.")
    out["verdict"] = (
        "The Pell descent is proved over the Laurent ring with NO import. The "
        "failing hypothesis 'deg f = 0 => f constant' is replaced by the "
        "two-sided width D, which vanishes exactly on units; UNITARITY makes "
        "every Newton polytope centrally symmetric, which is the ingredient the "
        "polynomial proof neither has nor needs; the descent then lowers D(b) by "
        "exactly D(u) per step until it lands on {+-1, +-A^+-1}. Scope: this N, "
        "under unitarity — NOT a re-proof of D-S in several variables."
    )
    return out


# --- no pytest surface ------------------------------------------------------
# `entry:` record; tests/casim/test_registry_integrity.py forbids both contracts.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, default=str))
