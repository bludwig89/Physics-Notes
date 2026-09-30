"""F283/F284 — Can the BCC lattice be elastic, and what is expansion if not?

Eight checks. E1 and F1 are exact-algebraic and are re-derived here with sympy
INDEPENDENTLY of the module, so this cross-checks rather than restates it.

  E1  (exact)  Under a -> s*a, F79's G ~ a^2 makes M_Pl and Lambda_UV BOTH
      scale as 1/s, so M_Pl/Lambda = 3^(1/4) and r = sqrt(3) = 1/c_lat for
      EVERY s, with dr/ds identically 0.  This is what corrects F282
      falsifier #5, so it is the load-bearing check of both findings.

  E2  (quantitative)  G ~ s^2, so s ~ a_FRW^q gives Gdot/G = 2qH.  LLR and
      BBN independently bound q at ~1e-3, and a fully comoving lattice (q=1)
      misses BBN by >17 decades.

  E3  (structural)  The volume mode is ln K (F79 zero tree stiffness, F180
      sourced, F216 two dof) or it is a PPN scalar Cassini bounds at 3.4e-3.

  E4  (quantitative)  A tree elastic term would give gravity its own cone;
      GW170817 bounds the tree fraction >14 decades below unity.

  F1  (exact)  H_max = c_lat/a = 3^(-3/4) M_Pl and t_min = 1/c_lat = sqrt(3)
      ticks — one cell-crossing.  No substrate singularity.

  F2  (computed)  The SI epoch numbers and the Hubble-volume cell budget.

  F3  (consistency)  The quarter-powers-of-three ladder is internally
      consistent: c_lat = 3^(-1/2), Lambda/M_Pl = 3^(-1/4),
      H_max/M_Pl = 3^(-3/4), r = 3^(+1/2), and r = 1/c_lat.

  F4  (regression)  F283's invariance must AGREE with F282's r at the
      canonical spacing — the correction changes the falsifier, not the number.

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import math

import sympy as sp

from casim.constants import c_lat
from casim.engine.interactions import cosmology_lattice_elasticity as el
from casim.engine.interactions import cosmology_primordial as cp


def check_E1_invariance_exact():
    """dr/ds = 0 from scratch, symbols free."""
    a, hbar, c, s = sp.symbols("a hbar c s", positive=True)
    G = (s * a) ** 2 * c ** 3 / (8 * sp.pi * sp.sqrt(3) * hbar)      # F79
    M2 = sp.simplify(hbar * c / (8 * sp.pi * G))
    Lam = hbar / ((s * a) * c)
    r = sp.simplify(M2 / Lam ** 2)
    assert r == sp.sqrt(3)                       # no a, no s, no hbar, no c
    assert sp.simplify(sp.diff(r, s)) == 0
    assert sp.simplify(sp.sqrt(M2) / Lam) == 3 ** sp.Rational(1, 4)

    got = el.invariance_under_stretch()
    assert got["invariant"] is True
    assert got["dr_ds"] == "0"
    assert got["r"] == "sqrt(3)"
    assert got["r_equals_inverse_c_lat"] is True
    return got


def check_E2_varying_G():
    got = el.varying_G_bounds()
    # a fully comoving lattice is excluded by both probes
    assert got["fully_comoving_excluded"] is True
    assert got["comoving_bbn_decades_off"] > 17.0
    for v in got["llr"].values():
        assert v["exclusion_factor"] > 100.0
        assert v["q_max"] < 1.0e-2
    for v in got["bbn"].values():
        assert v["q_max"] < 1.0e-2
    # the headline: rigid to ~0.1%
    assert got["q_max"] < 2.0e-3
    assert got["rigid_to_percent"] < 0.2
    # LLR and BBN are independent probes 17 orders apart in epoch and AGREE
    llr_q = got["llr"]["hofmann_muller_2018_2sigma"]["q_max"]
    bbn_q = got["bbn"]["delta_G_0.1"]["q_max"]
    assert 0.2 < llr_q / bbn_q < 5.0
    return got


def check_E3_volume_mode():
    got = el.volume_mode_dichotomy()
    assert got["graviton_dof_F216"] == 2
    assert got["alpha_max"] < 1.0e-2
    # a substrate mode carrying gravity would need >100x suppression
    assert got["suppression_required"] > 100.0
    return got


def check_E4_graviton_cone():
    got = el.graviton_cone_bound()
    assert got["decades_below_unity"] > 14.0
    assert got["tree_elastic_fraction_max"] < 1.0e-14
    return got


def check_F1_earliest_epoch_exact():
    """H_max = 3^(-3/4) M_Pl and t_min = sqrt(3) ticks, from scratch."""
    # Reduced-Planck units: a = 3^(1/4)/M_Pl, R_H = c_lat/H; set R_H = a.
    a_red = 3 ** sp.Rational(1, 4)                 # in units of 1/M_Pl
    c_l = 1 / sp.sqrt(3)
    H_max = sp.simplify(c_l / a_red)
    assert sp.simplify(H_max - 3 ** sp.Rational(-3, 4)) == 0
    assert sp.simplify(1 / H_max - 3 ** sp.Rational(3, 4)) == 0    # t_min in 1/M_Pl

    # Lattice units: a = 1 cell by definition, so the SAME time is 1/c_lat ticks.
    t_min_ticks = sp.simplify(1 / c_l)
    assert t_min_ticks == sp.sqrt(3)

    got = el.earliest_resolvable_epoch()
    assert abs(got["H_max_over_MPl"] - 3.0 ** -0.75) < 1e-14
    assert abs(got["t_min_ticks"] - math.sqrt(3.0)) < 1e-14
    assert got["singularity_in_substrate"] is False
    return got


def check_F2_epoch_si_and_budget():
    ep = el.earliest_resolvable_epoch()
    bd = el.lattice_cell_budget()
    # t_min is ABOVE the Planck time, because a is 6.6 non-reduced Planck lengths
    assert ep["t_min_over_planck_time"] > 1.0
    # t_min = a/c exactly (one cell-crossing at the canonical tick), so
    # t_min/t_P = a/ell_P.  Was 10 < x < 13 (11.43), which pinned the
    # sqrt(3)-long tick corrected 2026-09-29.
    from casim.constants import a_over_ellP
    assert abs(ep["t_min_over_planck_time"] / a_over_ellP - 1.0) < 1e-5
    assert 1e-35 < ep["a_metres"] < 1e-33
    assert bd["R_H_in_cells"] > 1e59
    assert bd["hubble_volume_in_cells"] > 1e179
    assert bd["trans_planckian_problem"] is False
    return {"epoch": ep, "budget": bd}


def check_F3_power_of_three_ladder():
    """The four scales are consistent quarter-powers of 3."""
    assert abs(c_lat - 3.0 ** -0.5) < 1e-15
    cut = cp.cutoff_ratio()
    ep = el.earliest_resolvable_epoch()
    assert abs(cut["Lambda_over_MPl"] - 3.0 ** -0.25) < 1e-14
    assert abs(ep["H_max_over_MPl"] - 3.0 ** -0.75) < 1e-14
    assert abs(cut["r_min"] - 3.0 ** 0.5) < 1e-14
    # the ladder closes: H_max = c_lat * Lambda, and r = 1/c_lat
    assert abs(ep["H_max_over_MPl"] - c_lat * cut["Lambda_over_MPl"]) < 1e-14
    assert abs(cut["r_min"] - 1.0 / c_lat) < 1e-14
    return {"c_lat": c_lat, "Lambda_over_MPl": cut["Lambda_over_MPl"],
            "H_max_over_MPl": ep["H_max_over_MPl"], "r_min": cut["r_min"]}


def check_F4_agrees_with_F282():
    """The correction changes F282's falsifier, not its number."""
    r_from_F282 = cp.cutoff_ratio()["r_min"]
    r_from_F283 = el.invariance_under_stretch()["r_float"]
    assert abs(r_from_F282 - r_from_F283) < 1e-14
    assert abs(r_from_F283 - math.sqrt(3.0)) < 1e-14
    # and F282's per-candidate verdicts are untouched
    assert abs(cp.eg_clock_coefficient()["K_closed_form"] - 9.0) < 1e-12
    return {"r_F282": r_from_F282, "r_F283": r_from_F283, "agree": True}


CHECKS = (
    ("E1_invariance_exact", check_E1_invariance_exact),
    ("E2_varying_G", check_E2_varying_G),
    ("E3_volume_mode", check_E3_volume_mode),
    ("E4_graviton_cone", check_E4_graviton_cone),
    ("F1_earliest_epoch_exact", check_F1_earliest_epoch_exact),
    ("F2_epoch_si_and_budget", check_F2_epoch_si_and_budget),
    ("F3_power_of_three_ladder", check_F3_power_of_three_ladder),
    ("F4_agrees_with_F282", check_F4_agrees_with_F282),
)


def check_all():
    """Registry entry point. Returns the full result dict."""
    out = {name: fn() for name, fn in CHECKS}
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "elastic lattice excluded four ways; the F282 obstruction is "
        "scale-invariant; expansion is K's conformal mode on a rigid substrate"
    )
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
