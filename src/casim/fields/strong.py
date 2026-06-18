"""casim.fields.strong — colour / gluon sector.

Propagator class (F91): gluon **even** (forced; colour coupling is branch-blind).
The BCC gluon propagator was migrated chiral→even on 2026-06-04
(``gluon_rotation_step_spectral_bcc``; old chiral step retained as
``gluon_rotation_step_spectral_bcc_chiral``).  Re-exports legacy strong-sector
kernels, defensively.
"""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401

_MODULES = [
    "ca_gluon", "ca_strong", "ca_colour_condensate", "ca_colour_dielectric",
    "ca_dual_gl_backreaction", "ca_confinement", "spinor_color",
]
_loaded = {}
for _m in _MODULES:
    try:
        _loaded[_m] = _il.import_module(_m)
        globals()[_m] = _loaded[_m]
    except Exception:  # pragma: no cover
        globals()[_m] = None

ca_gluon = _loaded.get("ca_gluon")

__all__ = list(_MODULES)
