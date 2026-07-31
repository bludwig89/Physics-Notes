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
# Old bare name -> new casim.engine path (roadmap C4). Migrated kernels import
# from their engine location; ca_dual_gl_backreaction is a C6 kernel not yet
# migrated, so it stays on its bare name (ca-simulation shim) until then.
_PATHS = {
    "ca_gluon": "casim.engine.gauge.gluon",
    "ca_strong": "casim.engine.gauge.strong",
    "ca_colour_condensate": "casim.engine.gauge.colour_condensate",
    "ca_colour_dielectric": "casim.engine.gauge.colour_dielectric",
    "ca_confinement": "casim.engine.gauge.confinement",
    # C6: the last bare name C4 left here, now that its kernel has migrated.
    "ca_dual_gl_backreaction": "casim.engine.interactions.gravity_backreaction",
    "spinor_color": "casim.engine.core._viz_spinor_color",
}
_loaded = {}
for _m in _MODULES:
    try:
        _loaded[_m] = _il.import_module(_PATHS.get(_m, _m))
        globals()[_m] = _loaded[_m]
    except Exception:  # pragma: no cover
        globals()[_m] = None

ca_gluon = _loaded.get("ca_gluon")

__all__ = list(_MODULES)
