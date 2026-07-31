"""casim.engine — simulation engine, channels, observers (the new layer)."""
from __future__ import annotations

from .core.channel import (
    Channel, register, get_channel_class, build_channel,
    registered_channels,
)
from .core.observers import (
    Observer, register_observer, build_observer, registered_observers,
)
from .core.simulation import Simulation, LatticeSpec

# Importing channels registers the concrete channel classes.
from .core import channels as _channels  # noqa: F401,E402
from .core import coupled as _coupled     # noqa: F401,E402  (Tier-2 coupled channels)
from .core import tier3 as _tier3         # noqa: F401,E402  (Tier-3 MC / variable-c)
from .core import spectral_matter as _spectral_matter  # noqa: F401,E402  (matter-sector spectral solves)
from .core import entanglement_register as _entanglement_register  # noqa: F401,E402  (genuine 2^n entanglement register, F212/F214)
from ..particles import channel as _particles  # noqa: F401,E402  (particle layer)

# The module registry (D11) — importing it self-registers every engine module.
from . import registry as _registry  # noqa: F401,E402

__all__ = [
    "Channel", "register", "get_channel_class", "build_channel",
    "registered_channels",
    "Observer", "register_observer", "build_observer", "registered_observers",
    "Simulation", "LatticeSpec",
]
