"""casim.fields.matter — Weyl/Dirac matter and composite sectors.

Propagator class (F91): per-branch (the audited BCC Weyl walk).  Re-exports
legacy matter kernels, defensively.
"""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401

_MODULES = ["ca_dirac", "ca_dirac_bcc", "ca_baryon", "ca_higgs"]
_loaded = {}
for _m in _MODULES:
    try:
        _loaded[_m] = _il.import_module(_m)
        globals()[_m] = _loaded[_m]
    except Exception:  # pragma: no cover
        globals()[_m] = None

__all__ = list(_MODULES)
