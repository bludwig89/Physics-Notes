"""F24 — SL(2,ℂ) → SO(1,3) covariance of the Weyl 4-current, after the 2026-08-04 review.

Registry record: `F24-sl2c-covariance-full` (gate tier). Physics in
`casim.engine.gauge.bilinear`.

What the review changed
-----------------------
The original check used **pure boosts only** at 12 seed-7 draws and quoted
3.71e-16 as "the IEEE-754 double-precision floor". Two problems:

* a pure boost ``A = cosh − sinh(σ·v̂)`` is **Hermitian**, so ``A† = A`` and the
  sandwich ``A† σ̄^μ A`` is blind to the placement of the dagger — the one error
  the test is meant to catch is in the branch it never exercised. Rotations are
  unitary and are added here, along with boost∘rotation compositions, because a
  homomorphism checked only on two separate one-parameter subgroups has not been
  checked as a homomorphism;
* the residual is limited by **conditioning, not eps**. The single-Weyl current is
  null, so an anti-aligned boost makes ``j'^0`` a near-total cancellation and the
  relative error grows like ``e^{2ζ}·eps``. Over 2000 draws the worst case is
  ~1e-13 at ζ ≈ −6.9, three orders above the quoted number.

`test_F24_legacy_sample_was_optimistic` asserts that second point directly, so the
finding cannot drift back to quoting a benign draw as a floor.
"""
from __future__ import annotations

from casim.engine.gauge import bilinear as m


def test_F24_all_channels_covariant():
    r = m.sl2c_covariance_full()
    assert r["ok"], r["checks"]
    assert r["n_pass"] == r["n_checks"] == 5


def test_F24_rotation_branch_is_exercised():
    """Rotations are unitary — this is where A vs A† actually matters."""
    r = m.sl2c_covariance_full()
    assert r["worst_rel_rotation"] <= 1e-12, r["worst_rel_rotation"]


def test_F24_composition_is_a_homomorphism():
    r = m.sl2c_covariance_full()
    assert r["worst_rel_composition"] <= 1e-10, r["worst_rel_composition"]


def test_F24_current_is_null():
    """rank-1 ψψ† ⇒ det = 0 ⇒ j·j = 0. The test only ever probes the null cone."""
    r = m.sl2c_covariance_full()
    assert r["worst_nullity"] <= 1e-12, r["worst_nullity"]


def test_F24_legacy_sample_was_optimistic():
    """The 12-draw 3.71e-16 is a benign sample, not a floor. Assert it, so the
    finding cannot quietly go back to calling it one."""
    r = m.sl2c_covariance_full()
    assert r["worst_rel_boost"] > r["legacy_12_draw_value"] * 100.0


def test_F24_rotation_matrix_is_unitary_not_hermitian():
    """The structural reason the boost-only test was blind."""
    import numpy as np
    R = m.sl2c_rotation([0.0, 0.0, 1.0], 0.7)
    assert np.allclose(R.conj().T @ R, np.eye(2), atol=1e-14)
    assert not np.allclose(R.conj().T, R, atol=1e-6)
