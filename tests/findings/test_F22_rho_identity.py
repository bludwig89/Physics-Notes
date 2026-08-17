"""F22 — the ρ identity, its negative control, and the O(vk) off-shell coefficient.

Registry record: `F22-rho-identity-and-offshell` (gate tier). Physics lives in
`casim.engine.interactions.derive_velocity_addition`.

Why this file exists
--------------------
The 2026-08-04 review found that F22's headline "sympy bit-zero" verification of
``ρ = 1 − 2β_LV`` could not fail. The module wrote

    beta_LV_sym = Rational(1,2) * (1 - rho_derived)
    check       = simplify(rho_derived - (1 - 2*beta_LV_sym))

which is ``x − (1 − 2(1−x)/2) ≡ 0`` for any expression at all — the referee got
residual 0 from a deliberately wrong ρ, and then from ρ = 42.

So the two sides now come from genuinely separate origins: the left from a sympy
limit of the dispersion, the right from the Finding-15 module's own closed form,
which carries its own gate record against the Legendre construction that defines
it. And :func:`test_F22_negative_control_fails` asserts the check *goes red* on a
wrong ρ — without that test, nothing distinguishes the repaired check from the
tautology it replaces.

The off-shell test is the corrected content of F22's claim 1. The finding says the
SR boost acts *exactly* on (ω, k); it does not, and the failure is first order in
v with coefficient 1/ρ − 1. Asserting that the coefficient is **nonzero** is the
point.
"""
from __future__ import annotations

import pytest

from casim.engine.interactions import derive_velocity_addition as m


def test_F22_rho_identity_holds():
    """ρ from a limit of the dispersion equals 1 − 2β_LV from the F15 module."""
    r = m.check_rho_identity()
    assert r["ok"], r["checks"]
    assert r["symbolic_residual"] == "0"
    assert r["acos_asin_lemma_residual"] <= 1e-40


def test_F22_negative_control_fails():
    """The repaired check must reject a wrong ρ. The old one did not."""
    bad = m.check_rho_identity(rho_override="42")
    assert not bad["checks"]["symbolic_identity"]
    assert not bad["checks"]["numeric_identity"]


@pytest.mark.parametrize("mass", [0.3, 0.5, 0.7])
def test_F22_rho_moves_with_mass(mass):
    """ρ > 1 always (tan θ > θ), and it must actually depend on m."""
    r = m.check_rho_identity(m_probe=mass)
    assert r["ok"], r["checks"]
    assert r["rho_from_limit"] == pytest.approx(r["rho_from_f15_module"], abs=1e-14)


def test_F22_rho_is_not_constant_in_mass():
    a = m.check_rho_identity(m_probe=0.3)["rho_from_limit"]
    b = m.check_rho_identity(m_probe=0.7)["rho_from_limit"]
    assert abs(b - a) > 0.05, (a, b)


@pytest.mark.parametrize("mass", [0.3, 0.5, 0.7])
def test_F22_boost_is_not_exact_on_omega_k(mass):
    """CORRECTED CLAIM 1. The linear SR boost does NOT preserve the mass shell.

    The deviation is first order in v with coefficient 1/ρ − 1. This test asserts
    the coefficient matches that closed form *and* that it is not zero — i.e. it
    asserts the failure the finding claimed did not happen.
    """
    o = m.offshell_boost_coefficient(m=mass)
    assert o["rel_err"] < 5e-3, o
    assert abs(o["delta_over_vk"]) > 1e-3, o


def test_F22_entry_point_all_checks():
    r = m.check_offshell_and_control()
    assert r["ok"], r["checks"]
    assert r["n_pass"] == r["n_checks"] == 4
