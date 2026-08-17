"""Headless tests for Bloch-sphere spinor colouring (casim.gui.render).

No vispy/Qt: the render helpers are pure numpy.  We assert the Bloch mapping on
known spinors — f-pole bright, g-pole dark, relative phase → hue, amplitude →
opacity — and that point_cloud_spinor selects the same voxels the density cut
would and colours them by orientation.
"""
from __future__ import annotations

import numpy as np

from casim.gui import render


def test_pure_f_is_bright_pure_g_is_dark():
    # Pure f (g=0): Bloch north pole, θ=0 → bright.  Pure g: south pole → dark.
    rgba_f = render.bloch_rgb(np.array([1.0 + 0j]), np.array([0.0 + 0j]))
    rgba_g = render.bloch_rgb(np.array([0.0 + 0j]), np.array([1.0 + 0j]))
    light_f = rgba_f[0, :3].mean()
    light_g = rgba_g[0, :3].mean()
    assert light_f > 0.8, light_f          # f-pole reads bright
    assert light_g < 0.2, light_g          # g-pole reads dark


def test_relative_phase_sets_hue_not_amplitude():
    # Equal-magnitude spinors differing only in arg(g): θ=π/2 (mid lightness),
    # hue follows φ = arg(g) − arg(f).  φ=0 and φ=π must give different colours.
    f = np.array([1.0 + 0j, 1.0 + 0j])
    g = np.array([1.0 + 0j, -1.0 + 0j])    # φ = 0 and φ = π
    rgba = render.bloch_rgb(f, g)
    assert not np.allclose(rgba[0, :3], rgba[1, :3])
    # mid-latitude → mid lightness band, both visible (neither pole)
    assert 0.3 < rgba[:, :3].mean(axis=1).max() < 0.85


def test_opacity_tracks_amplitude():
    # Same orientation, different amplitude → denser site is more opaque.
    f = np.array([2.0 + 0j, 0.2 + 0j])
    g = np.array([2.0 + 0j, 0.2 + 0j])
    rgba = render.bloch_rgb(f, g)
    assert rgba[0, 3] > rgba[1, 3]


def test_point_cloud_spinor_matches_density_selection():
    rng = np.random.default_rng(0)
    L = 12
    f = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    g = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    pctile = 90.0
    coords, colours, dmax, total = render.point_cloud_spinor(f, g, pctile)

    density = np.abs(f) ** 2 + np.abs(g) ** 2
    expected_mask = density > np.percentile(density.ravel(), pctile)
    assert coords.shape[0] == int(expected_mask.sum())
    assert colours.shape == (coords.shape[0], 4)
    assert np.isclose(dmax, density.max())
    assert np.isclose(total, density.sum())
    # colours are valid RGBA in [0,1]
    assert colours.min() >= 0.0 and colours.max() <= 1.0


def test_empty_input_is_safe():
    rgba = render.bloch_rgb(np.array([], dtype=complex), np.array([], dtype=complex))
    assert rgba.shape == (0, 4)


def test_channel_spinor_field_hook():
    # weyl_bcc exposes (f,g); a non-spinor state returns None.
    from casim.engine.core.channel import Channel
    base = Channel()
    f = np.ones((2, 2, 2), dtype=complex)
    g = np.zeros((2, 2, 2), dtype=complex)
    fg = base.spinor_field({"f": f, "g": g})
    assert fg is not None and fg[0].shape == (2, 2, 2)
    assert base.spinor_field({"K": np.ones((2, 2, 2))}) is None
