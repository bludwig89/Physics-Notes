"""F285 — What n_s can an initial-condition measure on the lattice give?

Seven checks. D0 and D3 are exact-algebraic and are re-derived here with sympy
INDEPENDENTLY of the module.

  D0  (exact)  The spectral bridge. Poisson (F106) gives P_Phi = P_rho/k^4 and
      Delta^2 = k^3 P, so Delta^2_Phi ~ k^(n_s - 1) forces P_rho ~ k^(n_s).
      Re-derived symbolically rather than asserted.

  D1a (structural)  The four candidate measures give n_s = 0, 0, 4, 1 — the two
      generic ones BRACKET the observation without touching it, and the best
      candidate (scale-free in the metric) is still 8.4 sigma out.

  D1b (computed)  The pivot sits 58.26 decades below the BZ edge, so the state
      must carry ~56 decades LESS large-scale power than white noise and ~177
      decades MORE than conserved-causal.

  D2  (computed)  (k a)^2 at the pivot is ~3e-116, and it is time-independent
      because the lattice is rigid (F284).

  D3  (exact)  Kadanoff dilation maps A k^n -> b^-(3+n) A k^n for EVERY n, so
      the exponent is an exactly marginal label. Checked for six integer n and
      for general symbolic n.

  D4  (synthesis)  Exact HZ (n_s = 1) is excluded at 8.36 sigma, so the state
      must be tilted; a tilt needs a second scale; the lattice has one, 116
      decades too weak.

  D5  (consistency)  F285 must not contradict F282/F284: the same a, the same
      rigidity, and D3's marginality is about a DIFFERENT object from F282 C3's
      gap.

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import math

import sympy as sp

from casim.engine.interactions import cosmology_initial_conditions as ic
from casim.engine.interactions import cosmology_lattice_elasticity as el
from casim.engine.interactions import cosmology_primordial as cp


def check_D0_spectral_bridge():
    """P_rho ~ k^n_s, derived from Poisson + Delta^2 = k^3 P."""
    k = sp.Symbol("k", positive=True)
    ns, m = sp.symbols("n_s m", real=True)
    P_rho = k ** m
    P_Phi = P_rho / k ** 4                      # Poisson: Phi ~ rho/k^2
    Delta2 = sp.simplify(k ** 3 * P_Phi)        # dimensionless power
    # read the exponent off as the log-slope, then match to n_s - 1
    slope = sp.simplify(k * sp.diff(sp.log(Delta2), k))
    assert sp.simplify(slope - (m - 1)) == 0
    (sol,) = sp.solve(sp.Eq(slope, ns - 1), m)
    assert sp.simplify(sol - ns) == 0
    assert ic.ns_from_density_slope(0.9649) == 0.9649
    return {"Delta2_slope": str(slope), "P_rho_exponent": str(sol),
            "relation": "P_rho ~ k^(n_s)"}


def check_D1a_measures_bracket():
    got = ic.measure_predictions()
    c = got["candidates"]
    assert c["uniform_max_entropy"]["n_s"] == 0.0
    assert c["local_short_range_correlated"]["n_s"] == 0.0
    assert c["locally_conserved_causal"]["n_s"] == 4.0
    assert c["scale_free_in_the_metric"]["n_s"] == 1.0
    # the generic pair brackets the observation without hitting it
    assert got["generic_measures_bracket_without_hitting"] is True
    assert c["uniform_max_entropy"]["deviation_sigma"] > 200.0
    assert c["locally_conserved_causal"]["deviation_sigma"] > 700.0
    # and the BEST candidate is still excluded
    assert got["best_candidate"] == "scale_free_in_the_metric"
    assert 8.0 < got["best_deviation_sigma"] < 9.0
    return got


def check_D1b_non_genericity():
    got = ic.required_non_genericity()
    assert 58.0 < got["decades_below_BZ"] < 58.5
    assert 56.0 < got["suppression_vs_white_noise_decades"] < 56.5
    assert 176.0 < got["enhancement_vs_conserved_causal_decades"] < 177.5
    # non-generic in BOTH directions — that is the point
    assert got["suppression_vs_white_noise_decades"] > 10.0
    assert got["enhancement_vs_conserved_causal_decades"] > 10.0
    return got


def check_D2_brillouin_zone_closed():
    got = ic.brillouin_zone_reach()
    assert got["leading_correction_ka_squared"] < 1e-100
    assert got["correction_decades"] > 100.0
    assert got["time_independent_because_lattice_is_rigid"] is True
    return got


def check_D3_tilt_is_marginal():
    """A k^n -> b^-(3+n) A k^n for every n, from scratch."""
    A, k, b = sp.symbols("A k b", positive=True)
    n = sp.Symbol("n", real=True)
    img = sp.simplify((A * k ** n).subs(k, k / b) * b ** -3)
    # exponent out == exponent in, identically
    assert sp.simplify(k * sp.diff(sp.log(img), k) - n) == 0
    # and the whole effect is an amplitude factor b^-(3+n)
    assert sp.simplify(img / (A * k ** n) - b ** (-(3 + n))) == 0

    got = ic.blockspin_tilt_marginality()
    assert got["every_power_law_preserved"] is True
    assert got["exponent_is_marginal"] is True
    assert got["general_exponent_out"] == "n"
    for row in got["rows"].values():
        assert row["exponent_preserved"] is True
        assert row["recovered_exponent"] == row["input_exponent"]
    return got


def check_D4_tilt_needs_a_second_scale():
    got = ic.tilt_needs_a_second_scale()
    # exact scale invariance is EXCLUDED, so the state must be tilted
    assert got["hz_exact_deviation_sigma"] > 8.0
    assert abs(got["tilt_magnitude"] - 0.0351) < 1e-6
    # and the lattice's single scale is far too weak to supply it
    assert got["lattice_scales_available"] == 1
    assert got["lattice_scale_imprint_at_pivot"] < 1e-100
    return got


def check_D5_consistent_with_F282_F284():
    """Same lattice, same rigidity; and the two marginality claims differ."""
    a_from_F285 = ic.required_non_genericity()["a_metres"]
    a_from_F284 = el.earliest_resolvable_epoch()["a_metres"]
    assert abs(a_from_F285 - a_from_F284) < 1e-45
    # F282 C3: the DYNAMICAL operator spectrum has a GAP at marginality
    assert cp.rg_marginality()["any_nearly_marginal_scalar"] is False
    # F285 D3: the INITIAL-STATE index is exactly MARGINAL — different object
    assert ic.blockspin_tilt_marginality()["exponent_is_marginal"] is True
    return {"a_metres": a_from_F285, "objects_are_distinct": True}


CHECKS = (
    ("D0_spectral_bridge", check_D0_spectral_bridge),
    ("D1a_measures_bracket", check_D1a_measures_bracket),
    ("D1b_non_genericity", check_D1b_non_genericity),
    ("D2_brillouin_zone_closed", check_D2_brillouin_zone_closed),
    ("D3_tilt_is_marginal", check_D3_tilt_is_marginal),
    ("D4_tilt_needs_a_second_scale", check_D4_tilt_needs_a_second_scale),
    ("D5_consistent_with_F282_F284", check_D5_consistent_with_F282_F284),
)


def check_all():
    """Registry entry point. Returns the full result dict."""
    out = {name: fn() for name, fn in CHECKS}
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "all three initial-condition directions close; the residual is the "
        "3.5% tilt, which needs a second slowly-evolving scale"
    )
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
