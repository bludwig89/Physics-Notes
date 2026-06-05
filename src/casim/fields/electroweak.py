"""casim.fields.electroweak — W±/Z/hypercharge sector.

Propagator class (F91): W± chiral (forced; left-projector coupling, right-branch
weight ≡ 0); Z even for its vector part with a mass-suppressed axial split.
Re-exports the legacy electroweak kernels.  Optional/heavy modules are imported
defensively so a missing dependency never breaks ``import casim``.
"""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401

_MODULES = [
    "ca_wmu", "ca_weak", "ca_z_field", "ca_charged_current", "ca_hypercharge",
]
_loaded = {}
for _m in _MODULES:
    try:
        _loaded[_m] = _il.import_module(_m)
        globals()[_m] = _loaded[_m]
    except Exception as _e:  # pragma: no cover
        globals()[_m] = None

# Key symbols (the W/γ even-law rotation and the chiral W law) when available.
ca_wmu = _loaded.get("ca_wmu")
if ca_wmu is not None:
    _f26_rotation_step = getattr(ca_wmu, "_f26_rotation_step", None)
    w_propagation_step_chiral = getattr(ca_wmu, "w_propagation_step_chiral", None)

__all__ = list(_MODULES) + ["_f26_rotation_step", "w_propagation_step_chiral"]
