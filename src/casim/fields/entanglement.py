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

# C6: `ca_entanglement` migrated to `casim.engine.interactions.qi_entanglement`.
# The old name still resolves through the ca-simulation shim, but that shim is
# deleted at C9 — and because this module loads by STRING, neither the import
# rewriter nor the C3.4 shim-import checker can see it. So the engine path is
# named explicitly, exactly as C4 did for fields/em|strong|electroweak.py.
_PATH = "casim.engine.interactions.qi_entanglement"

try:
    ca_entanglement = _il.import_module(_PATH)
except Exception:  # pragma: no cover
    ca_entanglement = None

__all__ = ["ca_entanglement"]
