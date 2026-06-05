"""casim.gui — interactive viewer (roadmap Phase E), grown from live_display.py.

Phase 1 re-points the viewer at a ``casim.engine.Simulation`` instead of a
module-level loop; Phase 2 adds a Qt control panel (run/pause/step/run-to-tick,
channel + threshold selectors, live observer readouts, checkpoint save/load).
Needs the optional ``casim[gui]`` extra (vispy + PyQt6); the numpy-only render
helpers in ``casim.gui.render`` work without it.
"""
from __future__ import annotations

from . import render  # noqa: F401  (numpy-only, always importable)


def gui_available() -> bool:
    try:
        import vispy  # noqa: F401
        from PyQt6 import QtWidgets  # noqa: F401
        return True
    except Exception:
        return False


GUI_AVAILABLE = gui_available()


def launch(scenario_path: str | None = None):  # pragma: no cover
    """Launch the interactive viewer for a scenario (or the default packet)."""
    from .app import run
    run(scenario_path)


__all__ = ["render", "gui_available", "GUI_AVAILABLE", "launch"]
