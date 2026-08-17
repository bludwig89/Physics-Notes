"""casim.viz — the static-figure and colour-mapping API.  Roadmap P5.1.

Before P5 this was a 13-line import shim that tried to import two flat modules
(``viz``, ``tick_heatmap``) which no longer exist post-C9, so it re-exported
``None`` and nothing imported it.  It is now the one home for the **numpy-only**
rendering helpers — no vispy/Qt here, so everything below is headless and
unit-testable — plus the matplotlib tick-heatmap figure (guarded, since
matplotlib is an optional figure dependency).

Provenance of the consolidation (P5.1):

  * ``density_to_rgba`` / ``bloch_rgb`` / ``point_cloud*`` / ``tinted_rgba`` /
    ``lattice_medium`` come from :mod:`casim.gui.render`, the production colour
    maps the live GUI uses.  ``engine/core/_viz_live_display`` held a byte-for-
    byte duplicate of ``density_to_rgba``; that module is retired (it is imported
    by nothing) and now re-exports this one, so there is a single implementation.
  * ``spinor_to_rgb`` / ``make_bloch_legend`` come from
    ``engine/core/_viz_spinor_color`` — production code, driven by 15 channels.
  * ``tick_heatmap`` / ``tick_heatmap_with_phi`` come from
    ``engine/core/_viz_tick_heatmap``; importing them here gives that
    previously test-only module a real consumer.
"""
from __future__ import annotations

# Numpy-only colour maps and point-cloud builders (always importable).
from casim.gui.render import (
    density_to_rgba,
    bloch_rgb,
    tinted_rgba,
    point_cloud,
    point_cloud_spinor,
    lattice_medium,
)
from casim.engine.core._viz_spinor_color import spinor_to_rgb, make_bloch_legend

# The matplotlib tick-heatmap figure is optional: it is the one helper that
# pulls a plotting backend, so a headless install without matplotlib still gets
# every colour map above.
try:
    from casim.engine.core._viz_tick_heatmap import (
        tick_heatmap, tick_heatmap_with_phi,
    )
    HAVE_TICK_HEATMAP = True
except Exception:  # pragma: no cover - matplotlib optional
    tick_heatmap = tick_heatmap_with_phi = None  # type: ignore
    HAVE_TICK_HEATMAP = False


__all__ = [
    "density_to_rgba", "bloch_rgb", "tinted_rgba",
    "point_cloud", "point_cloud_spinor", "lattice_medium",
    "spinor_to_rgb", "make_bloch_legend",
    "tick_heatmap", "tick_heatmap_with_phi", "HAVE_TICK_HEATMAP",
]
