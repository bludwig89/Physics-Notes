"""casim.fields.matter — Weyl/Dirac matter and composite sectors.

Propagator class (F91): per-branch (the audited BCC Weyl walk).  Re-exports
legacy matter kernels, defensively.
"""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401

_MODULES = ["ca_dirac", "ca_dirac_bcc", "ca_baryon", "ca_higgs"]
# Old bare name -> new casim.engine path (roadmap C5). These are imported by
# STRING, so neither the import-line rewriter nor the C3.4 shim checker can see
# them; without this map every name here would resolve through the deprecation
# shim and emit a DeprecationWarning on `import casim.fields`.
_PATHS = {
    "ca_dirac": "casim.engine.particles.dirac",
    "ca_dirac_bcc": "casim.engine.particles.dirac_bcc",
    "ca_baryon": "casim.engine.particles.baryon",
    "ca_higgs": "casim.engine.particles.higgs",
}
_loaded = {}
for _m in _MODULES:
    try:
        _loaded[_m] = _il.import_module(_PATHS.get(_m, _m))
        globals()[_m] = _loaded[_m]
    except Exception:  # pragma: no cover
        globals()[_m] = None

__all__ = list(_MODULES)
