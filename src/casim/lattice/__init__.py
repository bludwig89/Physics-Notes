"""casim.lattice — lattice substrate & FFT backend (re-exports legacy kernels).

Per roadmap: ca_core, ca_core_exact, ca_bcc, ca_fft, ca_lazy, ca_lattice.
"""
from __future__ import annotations

import casim as _casim  # noqa: F401  (ensures legacy dir is on sys.path)

from . import backend  # noqa: F401  (the FFT / chiral-transform seam)

import ca_lattice as ca_lattice          # noqa: E402
import ca_fft as ca_fft                  # noqa: E402
import ca_bcc as ca_bcc                  # noqa: E402
import ca_core as ca_core                # noqa: E402
import ca_core_exact as ca_core_exact    # noqa: E402

try:
    import ca_lazy as ca_lazy            # noqa: E402
except Exception:  # pragma: no cover - optional
    ca_lazy = None

# Commonly used symbols, surfaced at the sub-package level.
from ca_lattice import make_kgrid_1d, make_kgrid_2d, make_kgrid_3d  # noqa: E402
from ca_bcc import (  # noqa: E402
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
