"""casim.particles — typed particles stacked on the lattice.

See ``roadmap-particle-layer.md``.  ``spec`` holds the exact quantum numbers
and the derived force-applicability matrix; ``channel`` provides the
``particle`` engine channel plus the ``photon_sourced`` / ``gluon_sourced``
field channels that read particle currents.
"""
from __future__ import annotations

from .spec import (
    ParticleSpec, REGISTRY, DOUBLETS, FORCES,
    get_spec, doublet_specs, anomaly_traces,
)
from .composite import (
    CompositeSpec, COMPOSITES, get_composite, beta_decay_ledger,
)

__all__ = [
    "ParticleSpec", "REGISTRY", "DOUBLETS", "FORCES",
    "get_spec", "doublet_specs", "anomaly_traces",
    "CompositeSpec", "COMPOSITES", "get_composite", "beta_decay_ledger",
]
