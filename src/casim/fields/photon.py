"""casim.fields.photon — the paired-spinor photon (F67/F68/F69).

Propagator class: **even** (forced).  γ is the symmetric (+,-) bound pair of two
spin-1/2 Weyl quanta; both helicities ride the single rate
Ω_pair = ω⁺(k/2)+ω⁻(k/2) ≡ Ω_even — massless, luminal (c=1/√3), transverse,
non-birefringent.  Re-exports the legacy ``ca_photon_pair`` kernel.
"""
from __future__ import annotations

import casim as _casim  # noqa: F401

from casim.engine.gauge import photon as ca_photon_pair  # noqa: E402
from casim.engine.gauge.photon import (  # noqa: E402
    pair_dispersion,
    pair_birefringence,
    photon_step_spectral, photon_step_dielectric,
    build_pair_mode,
    build_beam_packet,
    group_velocity,
    group_velocity_at,
)

__all__ = [
    "ca_photon_pair",
    "pair_dispersion", "pair_birefringence", "photon_step_spectral", "photon_step_dielectric",
    "build_pair_mode", "build_beam_packet",
    "group_velocity", "group_velocity_at",
]
