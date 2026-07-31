"""casim.lattice — lattice substrate & FFT backend (re-exports legacy kernels).

Per roadmap: ca_core, ca_core_exact, ca_bcc, ca_fft, ca_lazy, ca_lattice.
"""
from __future__ import annotations

import casim as _casim  # noqa: F401  (ensures legacy dir is on sys.path)

from . import backend  # noqa: F401  (the FFT / chiral-transform seam)

from casim.engine.lattice import geometry as ca_lattice  # noqa: E402
from casim.numerics import fft as ca_fft  # noqa: E402  (C1.3: the
# legacy NAME is kept because callers do `from casim.lattice import
# ca_fft`, but it now resolves to the façade rather than being a
# second, independent route to numpy.fft.
from casim.engine.lattice import bcc as ca_bcc  # noqa: E402
from casim.engine.lattice import core as ca_core  # noqa: E402
from casim.engine.lattice import core_exact as ca_core_exact  # noqa: E402

try:
    import ca_lazy as ca_lazy            # noqa: E402
except Exception:  # pragma: no cover - optional
    ca_lazy = None

# Commonly used symbols, surfaced at the sub-package level.
from casim.engine.lattice.geometry import make_kgrid_1d, make_kgrid_2d, make_kgrid_3d  # noqa: E402
from casim.engine.lattice.bcc import (  # noqa: E402
    bcc_dispersion,
    bcc_unitary,
    weyl_step_3d_bcc,
    measure_bcc_dispersion,
    bcc_unitarity_residual,
    bcc_norm_drift_test,
)

__all__ = [
    "ca_lattice", "ca_fft", "ca_bcc", "ca_core", "ca_core_exact", "ca_lazy",
    "backend",
    "make_kgrid_1d", "make_kgrid_2d", "make_kgrid_3d",
    "bcc_dispersion", "bcc_unitary", "weyl_step_3d_bcc",
    "measure_bcc_dispersion", "bcc_unitarity_residual", "bcc_norm_drift_test",
]
