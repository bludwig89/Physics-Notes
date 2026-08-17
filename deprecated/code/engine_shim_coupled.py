"""Deprecated location — moved to `casim.engine.core.coupled` at roadmap C3 (D6).

This shim aliases the old flat path onto the new one so pre-C3 imports keep
working; it is removed wholesale at C9. New code must import from
`casim.engine.core.coupled`.
"""
from __future__ import annotations

import sys as _sys
import warnings as _warnings

from casim.engine.core import coupled as _moved

_warnings.warn(
    "casim.engine.coupled moved to casim.engine.core.coupled "
    "(roadmap C3, D6); update the import — this shim is removed at C9.",
    DeprecationWarning,
    stacklevel=2,
)

# Alias the module object so every attribute resolves to the moved module.
_sys.modules[__name__] = _moved
