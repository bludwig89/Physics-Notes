"""casim.fields.em — σ-bilinear EM field construction.

Per F67 this construction is **retired as the photon** (birefringent → excluded
by GRB/AGN polarimetry); it is retained ONLY for the massive / non-Abelian
sectors (W/Z/gluon), which are not under the polarimetry bound.  Re-exports the
legacy ``ca_maxwell`` / ``ca_maxwell_2d`` kernels, defensively.
"""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401

_MODULES = ["ca_maxwell", "ca_maxwell_2d"]
# Old bare name -> new casim.engine path (roadmap C4). The σ-bilinear field
# construction now lives at casim.engine.gauge.bilinear (retained for W/Z/gluon;
# NOT the photon — that is casim.engine.gauge.photon, the paired-spinor photon).
_PATHS = {
    "ca_maxwell": "casim.engine.gauge.bilinear",
    "ca_maxwell_2d": "casim.engine.gauge.bilinear_2d",
}
_loaded = {}
for _m in _MODULES:
    try:
        _loaded[_m] = _il.import_module(_PATHS.get(_m, _m))
        globals()[_m] = _loaded[_m]
    except Exception:  # pragma: no cover
        globals()[_m] = None

__all__ = list(_MODULES)
