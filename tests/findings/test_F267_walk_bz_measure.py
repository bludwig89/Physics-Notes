"""F267 — the fermion walk's BZ is not the cubic FFT cube. Roadmap P3.1's spike.

Asserts the five checks of `casim.engine.lattice.derive_walk_bz_measure`. The two
that matter most are opposite in sign, and both have to hold:

  * **S3 must pass** — exactly one ω=0 point per branch and no ω=π point inside
    the cube, so the mismatched domain introduces **no doubler** and F250 / the
    F69 paired-spinor photon are safe. If this ever fails, D1 re-opens.
  * **S1's second row must fail as a period** — the FFT grid's own 2π period is
    *not* a symmetry of the walk, which is what makes the cube not a fundamental
    domain and the gauge side's factor 4 inapplicable.

Run:
    python3 tests/findings/test_F267_walk_bz_measure.py
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pytest

# No module-scope `sys.path` preamble, deliberately (roadmap C7.4): this file is
# a registry record with an `entry:`, `tests/conftest.py` puts `src/` on the path
# for pytest, and `PYTHONPATH=src` is the documented way to run it standalone. A
# preamble here would raise the `import_time_work` ratchet for no benefit.
from casim.engine.lattice import derive_walk_bz_measure as D


# ---------------------------------------------------------------- S1
@pytest.mark.machine_precision
def test_S1_walk_period_is_root3_fcc():
    r = D.s1_periodicity()
    for key in ("root3_fcc_110", "root3_fcc_101", "root3_fcc_011"):
        assert r[key]["is_period"], f"{key} should be a period"
        assert r[key]["max_domega"] < 1e-12, r[key]


@pytest.mark.exact
def test_S1_gauge_period_and_fft_period_are_NOT_walk_periods():
    """The load-bearing negative result.

    If either of these ever became a period, the cube *would* be a fundamental
    domain (or an integer number of them) and F267's whole conclusion would
    dissolve. The separation is O(1), not marginal.
    """
    r = D.s1_periodicity()
    assert not r["fcc_pi_110_gauge_side"]["is_period"]
    assert r["fcc_pi_110_gauge_side"]["max_domega"] > 1.0
    assert not r["cubic_2pi_100_fft_grid"]["is_period"]
    assert r["cubic_2pi_100_fft_grid"]["max_domega"] > 1.0


# ---------------------------------------------------------------- S2
@pytest.mark.exact
def test_S2_cube_is_4_over_3root3_of_one_zone():
    r = D.s2_volumes()
    assert r["residual"] < 1e-12, r
    # and it is NOT an integer number of copies — the structural reason no
    # integer correction factor exists.
    ratio = r["ratio"]
    assert abs(ratio - round(ratio)) > 0.2, ratio
    assert abs(ratio - 4.0 / (3.0 * np.sqrt(3.0))) < 1e-15


# ---------------------------------------------------------------- S3
@pytest.mark.exact
def test_S3_no_doubler_is_introduced():
    """One ω=0 per branch, no ω=π. F250 and the photon depend on this."""
    r = D.s3_weyl_points()
    assert r, "no sizes measured"
    for size, per in r.items():
        for sign in ("+", "-"):
            assert per[sign]["n_zero"] == 1, (size, sign, per[sign])
            assert per[sign]["n_pi"] == 0, (size, sign, per[sign])


# ---------------------------------------------------------------- S4
@pytest.mark.quantitative
def test_S4_cube_mean_differs_from_domain_mean():
    """The cost, asserted as a band rather than a point.

    A tighter assertion would encode the Monte-Carlo seed rather than the
    physics; a looser one would not notice the error going away. 5%-30% brackets
    the measured 10.7% / 16.9% with room for MC noise on either side.
    """
    r = D.s4_measure_error(L=36, n_mc=120_000, seeds=(0, 1))
    for label in ("omega", "inv_omega"):
        rel = r[label]["rel_error"]
        assert 0.05 < rel < 0.30, (label, r[label])
        # the domain estimate must be precise enough for the claim to mean
        # anything (the FA4 lesson: a noisy estimator can agree by luck)
        assert r[label]["domain_mc_sd"] < 0.01 * abs(r[label]["domain_mean"])


# ---------------------------------------------------------------- S5
@pytest.mark.machine_precision
def test_S5_hop_is_fractional_but_unitary():
    r = D.s5_hop_is_fractional()
    assert not r["is_lattice_hop"], r
    assert r["cells_above_1e-3"] > 100, r
    assert abs(r["unitarity"] - 1.0) < 1e-12, r
    # a real lattice hop would put all the probability in one cell
    assert r["peak_prob"] < 0.5, r


def main() -> int:
    res = D.run()
    checks = [
        ("S1 walk period = sqrt3*fcc", res["verdict"]["walk_period_is_root3_fcc"]),
        ("S1 gauge period is NOT a walk period",
         res["verdict"]["gauge_period_is_not_a_walk_period"]),
        ("S1 FFT cube is NOT a fundamental domain",
         res["verdict"]["fft_cube_is_not_a_fundamental_domain"]),
        ("S2 cube/zone = 4/(3 sqrt3) exactly",
         res["S2_volumes"]["residual"] < 1e-12),
        ("S3 no doubler introduced", res["verdict"]["no_doubler_introduced"]),
        ("S4 measure error in 5-30%",
         all(0.05 < res["S4_measure_error"][k]["rel_error"] < 0.30
             for k in ("omega", "inv_omega"))),
        ("S5 hop is fractional, unitary",
         (not res["S5_hop_is_fractional"]["is_lattice_hop"])
         and abs(res["S5_hop_is_fractional"]["unitarity"] - 1.0) < 1e-12),
    ]
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    n = sum(1 for _, ok in checks if ok)
    print(f"\n  -> {n}/{len(checks)} PASS")

    from casim.engine.particles._results_path import results_path
    p = results_path("F267_walk_bz_measure.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, default=float)
    print(f"  -> wrote {p}")
    return 0 if n == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
