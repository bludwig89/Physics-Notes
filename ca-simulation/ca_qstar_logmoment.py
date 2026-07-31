"""DEPRECATED shim — this module moved to `casim.engine.interactions.running_qstar_logmoment`.

Roadmap D6 (C6): `ca-simulation/` is being retired into `src/casim/`.
This file exists only so unmigrated tests keep importing successfully; it is
deleted wholesale at C9. New code must import from `casim.engine.interactions.running_qstar_logmoment`.
"""
import os as _os
import sys as _sys
import warnings as _warnings

# Put `src/` on sys.path before importing the target.
#
# This is not optional. `casim/__init__.py` locates `ca-simulation/` and adds
# it to sys.path, so `import ca_bcc` works from inside the package — but the
# reverse has never been true. Dozens of test files do
# `sys.path.insert(0, "ca-simulation")` and import a kernel with NO reference
# to `src/` anywhere, relying on PYTHONPATH being set. Without this bootstrap
# every one of them would start failing with `ModuleNotFoundError: casim` the
# moment its kernel was migrated — a breakage caused entirely by the move and
# nothing to do with the physics.
# Walk up looking for a `src/casim`, mirroring `casim._locate_legacy`. A plain
# walk handles both `ca-simulation/` and `ca-simulation/forks/` without any
# depth arithmetic to get wrong.
_d = _os.path.dirname(_os.path.abspath(__file__))
while True:
    _src = _os.path.join(_d, "src")
    if _os.path.isdir(_os.path.join(_src, "casim")):
        if _src not in _sys.path:
            _sys.path.insert(0, _src)
        break
    _parent = _os.path.dirname(_d)
    if _parent == _d:
        break
    _d = _parent

import casim.engine.interactions.running_qstar_logmoment as _target

_warnings.warn(
    "ca-simulation/ca_qstar_logmoment.py has moved to casim.engine.interactions.running_qstar_logmoment; this shim is removed at roadmap C9",
    DeprecationWarning, stacklevel=2)

# Re-export everything, including private names — a `from x import *` would
# silently drop every `_`-prefixed symbol, and several kernels expose those to
# their tests.
globals().update({k: v for k, v in vars(_target).items()
                  if k not in ("__name__", "__file__", "__loader__",
                               "__spec__", "__package__", "__doc__")})
