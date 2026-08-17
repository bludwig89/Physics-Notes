"""F306 — the σ-bilinear curl equation closes at O(k³); the O(k) failure was a reading.

Registry record: `F306-curl-closes-at-k3` (gate tier). Physics in
`casim.engine.gauge.bilinear`.

The control is the point
------------------------
`test_F306_original_reading_does_not_fall` is what makes this finding falsifiable
rather than a restatement. Both residuals are computed from the *same* fields at
the *same* k: the original real-pair reading sits flat at c_lat/√2 across two
decades, while the analytic-amplitude reading falls by ~10⁴. Without that side
by side, "it closes at O(k³)" would just be a different function returning a
smaller number.
"""
from __future__ import annotations

import pytest

from casim.constants import c_lat
from casim.engine.gauge import bilinear as m


def test_F306_all_checks():
    r = m.check_curl_closes_at_k3()
    assert r["ok"], r["checks"]
    assert r["n_pass"] == r["n_checks"] == 5


def test_F306_closes_at_k3():
    """Normalised residual ~ c_lat³k²/48, i.e. the curl violation is O(k³)."""
    r = m.check_curl_closes_at_k3()
    for row in r["rows"]:
        if row["k"] >= 1e-2:
            assert row["rel"] < 0.05, row


def test_F306_original_reading_does_not_fall():
    """THE CONTROL. Same fields, same k — the real-pair reading is flat at c_lat/√2."""
    r = m.check_curl_closes_at_k3()
    orig = r["original_real_pair"]
    assert max(orig) - min(orig) < 1e-2, orig
    assert orig[-1] == pytest.approx(c_lat / 2 ** 0.5, abs=1e-4)


def test_F306_geometry_is_why():
    """B = n̂ × E exactly ⇒ ∂_t E ∥ B while ∇×B ∥ −E. Orthogonal, at every Δt."""
    r = m.check_curl_closes_at_k3()
    assert r["worst_cos_B_nhat_cross_E"] > 1.0 - 1e-9


def test_F306_analytic_residual_scales_like_k_squared():
    r = m.check_curl_closes_at_k3()
    assert r["analytic_drop_over_two_decades"] > 5e3
