"""casim.viz static-figure API — roadmap P5.1, finding F275.

*Created 2026-07-31 - 22:58.*

The failure mode being guarded: before P5.1 ``casim.viz`` re-exported ``None``
for everything (it imported two flat modules deleted at C9), and nothing caught
it because nothing imported ``casim.viz``.  These checks assert the API is real
and that its ``density_to_rgba`` is the single canonical one — the same object
``casim.gui.render`` exposes — so the duplicate in ``_viz_live_display`` cannot
quietly diverge and be picked up instead.
"""
from __future__ import annotations

import numpy as np

import casim.viz as viz
from casim.gui import render


def test_public_api_is_populated_not_none():
    for name in ("density_to_rgba", "bloch_rgb", "tinted_rgba", "point_cloud",
                 "spinor_to_rgb", "make_bloch_legend"):
        assert getattr(viz, name) is not None, f"{name} is None"
        assert callable(getattr(viz, name))


def test_density_to_rgba_is_the_canonical_render_one():
    assert viz.density_to_rgba is render.density_to_rgba


def test_density_to_rgba_shape_and_monotone_alpha():
    vals = np.array([0.0, 0.25, 0.5, 1.0])
    rgba = viz.density_to_rgba(vals, 1.0)
    assert rgba.shape == (4, 4) and rgba.dtype == np.float32
    # denser -> more opaque (alpha non-decreasing)
    assert np.all(np.diff(rgba[:, 3]) >= -1e-7)
    # vmax below the floor yields all-zero, not a divide-by-zero
    assert np.all(viz.density_to_rgba(vals, 0.0) == 0.0)


def test_bloch_and_spinor_colour_maps_run():
    f = np.array([1 + 0j, 0 + 0j])
    g = np.array([0 + 0j, 1 + 0j])
    assert viz.bloch_rgb(f, g).shape == (2, 4)
    assert viz.spinor_to_rgb(f, g).shape == (2, 3)


def test_tick_heatmap_flag_matches_availability():
    # If matplotlib is present the figure helper is a callable; if not, the flag
    # says so and the name is None (headless install still gets the colour maps).
    if viz.HAVE_TICK_HEATMAP:
        assert callable(viz.tick_heatmap)
    else:
        assert viz.tick_heatmap is None


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
