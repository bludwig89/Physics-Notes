"""casim.viz — static figure helpers (re-exports legacy viz, tick_heatmap)."""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401

for _m in ("viz", "tick_heatmap"):
    try:
        globals()[_m] = _il.import_module(_m)
    except Exception:  # pragma: no cover
        globals()[_m] = None

__all__ = ["viz", "tick_heatmap"]
