"""casim.engine — simulation engine, channels, observers (the new layer)."""
from __future__ import annotations

from .channel import (
    Channel, register, get_channel_class, build_channel,
    registered_channels,
)
from .observers import (
    Observer, register_observer, build_observer, registered_observers,
)
from .simulation import Simulation, LatticeSpec

# Importing channels registers the concrete channel classes.
from . import channels as _channels  # noqa: F401,E402
from . import coupled as _coupled     # noqa: F401,E402  (Tier-2 coupled channels)
from . import tier3 as _tier3         # noqa: F401,E402  (Tier-3 MC / variable-c)
from ..particles import channel as _particles  # noqa: F401,E402  (particle layer)

__all__ = [
    "Channel", "register", "get_channel_class", "build_channel",
    "registered_channels",
    "Observer", "register_observer", "build_observer", "registered_observers",
    "Simulation", "LatticeSpec",
]
