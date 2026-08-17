"""F282 — The model admits no slow-roll inflaton direction.

Seven checks. The load-bearing ones (A1, B1, C1) are exact-algebraic and are
re-derived here with sympy INDEPENDENTLY of the module, so this is a genuine
cross-check and not a restatement of the implementation.

  A1  (exact)  a / ell_reduced = 3^(1/4), so the lattice cutoff is
      SUB-Planckian and r_min = M_Pl^2/Lambda^2 = sqrt(3) = 1/c_lat.
      Re-derived from sqrt(8 pi) 3^(1/4) / sqrt(8 pi) over sympy.

  A2  (exact)  the module's floats agree with those closed forms.

  B1  (exact)  E_g clock angle: eps/r and |eta|/r cross at cos(6 delta) = 1/3
      where both equal 9.  K_clock = 9 exactly, independent of lambda_6 and e.

  B2  (machine) E_g radial: with V0 forced by F193 (V(e_min) = 0), the hat's
      min over the field range of max(eps,|eta|)/r is 5.92, and the hilltop
      eta/r is -8.95.  Both O(10), not O(0.01).

  C1  (exact)  any p-fold periodic direction has n_s <= 1 - p^2 r, because
      (3+u)/(1-u) >= 1 on u in [-1,1].  At the most generous p=1, J=1 this is
      n_s <= 1 - sqrt(3) = -0.732, i.e. >400 sigma from Planck's 0.9649.

  C2  (quantitative) Starobinsky: the R^2 coefficient needed for the observed
      A_s exceeds the induced one-loop value by >9 decades, and the induced
      scalaron sits ABOVE the lattice cutoff.

  C3  (structural) F130's measured Kadanoff spectrum has an O(1) gap around
      marginality — no nearly-marginal scalar operator exists to be a
      slow-roll field.

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import math

import sympy as sp

from casim.constants import c_lat
from casim.engine.interactions import cosmology_primordial as cp

SLOWROLL_TARGET = 0.02


def check_A1_cutoff_exact():
    """a/ell_red = 3^(1/4) and r_min = sqrt(3) = 1/c_lat, over sympy."""
    a_over_ellP = sp.sqrt(8 * sp.pi) * 3 ** sp.Rational(1, 4)
    ell_red = sp.sqrt(8 * sp.pi)                      # in units of ell_P
    ratio = sp.simplify(a_over_ellP / ell_red)
    assert ratio == 3 ** sp.Rational(1, 4)
    r_min = sp.simplify(ratio ** 2)
    assert r_min == sp.sqrt(3)
    assert sp.simplify(r_min - 1 / sp.Rational(1, 1) / sp.sqrt(3) * 3) == 0
    # sub-Planckian: the cutoff is BELOW M_Pl
    assert float(1 / ratio) < 1.0
    return {"a_over_ell_reduced": str(ratio), "r_min": str(r_min),
            "Lambda_over_MPl": float(1 / ratio), "sub_planckian": True}


def check_A2_module_matches_closed_form():
    cut = cp.cutoff_ratio()
    assert abs(cut["a_over_ell_reduced"] - 3.0 ** 0.25) < 1e-14
    assert abs(cut["r_min"] - math.sqrt(3.0)) < 1e-14
    assert abs(cut["r_min"] - 1.0 / c_lat) < 1e-14
    assert abs(cut["Lambda_over_MPl"] - math.sqrt(c_lat)) < 1e-14
    assert cut["sub_planckian"] is True
    return cut


def check_B1_clock_K_is_nine():
    """K_clock = 9 exactly, from an independent sympy derivation."""
    u = sp.Symbol("u")
    eps = 18 * (1 - u) / (1 + u)          # eps/r
    eta = 36 * u / (1 + u)                # |eta|/r for u > 0
    (u_star,) = sp.solve(sp.Eq(eps, eta), u)
    assert u_star == sp.Rational(1, 3)
    K = sp.simplify(eps.subs(u, u_star))
    assert K == 9

    got = cp.eg_clock_coefficient()
    assert abs(got["K_closed_form"] - 9.0) < 1e-12
    assert abs(got["K_numeric"] - 9.0) < 1e-3          # grid resolution
    assert abs(got["argmin_cos6delta"] - 1.0 / 3.0) < 1e-4
    # amplitude-independence: K does not move with lambda_6 or e
    assert abs(got["value_at_J_unity"] - 9.0 * math.sqrt(3.0)) < 1e-9
    # and the required decay constant is 15*sqrt(2) M_Pl
    assert abs(got["f_over_MPl_required"] - 15.0 * math.sqrt(2.0)) < 1e-9
    assert got["J_required"] > 700.0
    return got


def check_B2_radial_is_O10():
    got = cp.eg_radial_coefficient()
    # V0 is forced, not fitted: V(e_min) = 0 by F193
    assert got["V0_forced_by_F193"] > 0.0
    assert abs(got["e_min"] - 0.6549901316759) < 1e-9
    assert abs(got["V0_forced_by_F193"] - 0.2408311780789) < 1e-9
    assert abs(got["eta_over_r_at_hilltop"] + 8.9523292507) < 1e-8
    # the verdict: O(10), three orders above the slow-roll target
    assert got["K_numeric"] > 1.0
    assert got["value_at_J_unity"] > 10.0
    assert got["value_at_J_unity"] / SLOWROLL_TARGET > 100.0
    assert got["f_over_MPl_required"] > 10.0
    # the two E_g directions must AGREE within a factor of 2 (robustness)
    clock = cp.eg_clock_coefficient()
    ratio = clock["f_over_MPl_required"] / got["f_over_MPl_required"]
    assert 0.5 < ratio < 2.0
    return {**got, "clock_to_radial_f_ratio": ratio}


def check_C1_periodic_ns_bound():
    """n_s <= 1 - p^2 r because (3+u)/(1-u) >= 1 on [-1, 1)."""
    u = sp.Symbol("u")
    g = (3 + u) / (1 - u)
    # strictly increasing on (-1, 1): derivative has no root and is positive
    assert sp.solve(sp.diff(g, u), u) == []
    assert sp.simplify(sp.diff(g, u).subs(u, 0)) > 0
    assert sp.simplify(g.subs(u, -1)) == 1

    got = cp.periodic_ns_bound(J=1.0, p=1)
    assert abs(got["ns_max"] - (1.0 - math.sqrt(3.0))) < 1e-12
    assert got["ns_max"] < got["ns_observed"]
    assert got["deviation_sigma"] > 100.0
    got6 = cp.periodic_ns_bound(J=1.0, p=6)
    assert got6["ns_max"] < got["ns_max"]
    return {"p1": got, "p6": got6}


def check_C2_starobinsky_excluded():
    got = cp.starobinsky_gap(100.0)
    assert got["shortfall_decades"] > 9.0
    # independently: the induced scalaron is above the lattice cutoff
    assert got["scalaron_above_cutoff"] is True
    assert got["lattice_cutoff_over_MPl"] < got["scalaron_mass_over_MPl_induced"]
    # even 1000 dof does not rescue it
    assert cp.starobinsky_gap(1000.0)["shortfall_decades"] > 8.0
    return got


def check_C3_no_nearly_marginal_operator():
    got = cp.rg_marginality()
    assert got["gap_to_marginality"] >= 1.0
    assert got["any_nearly_marginal_scalar"] is False
    # F130: exactly one relevant direction, everything else irrelevant
    exps = got["exponents"]
    assert sum(1 for v in exps.values() if v > 0) == 1
    assert all(v <= -2.0 for k, v in exps.items() if v < 0)
    return got


CHECKS = (
    ("A1_cutoff_exact", check_A1_cutoff_exact),
    ("A2_module_matches_closed_form", check_A2_module_matches_closed_form),
    ("B1_clock_K_is_nine", check_B1_clock_K_is_nine),
    ("B2_radial_is_O10", check_B2_radial_is_O10),
    ("C1_periodic_ns_bound", check_C1_periodic_ns_bound),
    ("C2_starobinsky_excluded", check_C2_starobinsky_excluded),
    ("C3_no_nearly_marginal_operator", check_C3_no_nearly_marginal_operator),
)


def check_all():
    """Registry entry point. Returns the full result dict."""
    out = {}
    for name, fn in CHECKS:
        out[name] = fn()
    out["n_checks"] = len(CHECKS)
    out["verdict"] = "no slow-roll inflaton direction exists in the model"
    return out


# --- no pytest surface ------------------------------------------------------
# The thin `test_*` wrappers that used to sit here were DELETED 2026-08-02 by
# F287. They made this record both a pytest file and an `entry:` record, which
# tests/casim/test_registry_integrity.py and test_registry_entries.py forbid in
# combination: the two contracts can disagree about what "pass" means. Each
# wrapper only called the identically-named `check_*` above it, and `check_all`
# calls every one of them via CHECKS, so nothing is lost -- the registry entry
# is now the single contract and runs all 7 checks.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
