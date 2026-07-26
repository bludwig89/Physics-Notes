"""casim.fields.entanglement — genuine many-body (2ⁿ) register sector (F212/F214).

Re-exports the audited ``ca_entanglement`` kernel: the native SU(2) rotor and
spinor-exchange gates, the flat-state-vector helpers used by the live engine
channel, and the super-exchange derivation that fixes the entangler's coupling
J from the ``ca_dirac`` hopping.  This is the *only* casim sector that carries
genuine 2ⁿ entanglement (all others are first-quantised / mean-field).
"""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401  (ensures ca-simulation is on sys.path)

try:
    ca_entanglement = _il.import_module("ca_entanglement")
except Exception:  # pragma: no cover
    ca_entanglement = None

__all__ = ["ca_entanglement"]
