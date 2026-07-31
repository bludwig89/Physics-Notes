"""casim.lattice.backend — DEPRECATED shim onto `casim.numerics.backends`.

Roadmap C1.1 (D8). This module used to be the *second* of two competing seams:
it held an object registry with a seven-method protocol, while `ca_fft` held a
library switch with a module-level string. Nothing physical imported this one —
its only importers were two tests and its own self-registration — so a GPU
backend registered here would never have been reached by a kernel calling
`ca_fft`.

C1 collapsed both into `casim.numerics.backends`. This file remains so that
`tests/casim/test_backend.py` and any external caller keep working; it is
deleted at C9.

The one visible change: `backend_name()` now returns the *library* name
(`numpy` / `scipy` / `pyfftw`) rather than the constant string `"ca_fft"`,
because the library IS the backend now — that indirection was the thing making
the seam decorative. `"ca_fft"` is kept registered as an alias of the active
library so the old name still resolves.
"""
from __future__ import annotations

from typing import Any

from casim.numerics import backends as _b
from casim.numerics.backends import (          # noqa: F401  (re-export)
    active, active_name, available, describe, register, use,
)

__all__ = [
    "register_backend", "use", "get_backend", "backend_name", "available",
    "fftn", "ifftn", "fft2", "ifft2", "fft", "ifft", "chiral_transform",
]


def register_backend(backend: Any, name: str | None = None) -> None:
    _b.register(backend, name)


def get_backend() -> Any:
    return _b.active()


def backend_name() -> str:
    return _b.active_name()


def fftn(a, **kw):  return _b.active().fftn(a, **kw)
def ifftn(a, **kw): return _b.active().ifftn(a, **kw)
def fft2(a, **kw):  return _b.active().fft2(a, **kw)
def ifft2(a, **kw): return _b.active().ifft2(a, **kw)
def fft(a, **kw):   return _b.active().fft(a, **kw)
def ifft(a, **kw):  return _b.active().ifft(a, **kw)
def chiral_transform(*a, **kw): return _b.active().chiral_transform(*a, **kw)


class _CaFftAlias:
    """Keeps the name `ca_fft` resolvable in `available()` / `use()`.

    It delegates to a library backend rather than to the old `ca_fft` module,
    which is now itself a shim onto `casim.numerics.fft`. Registering the old
    name as a real backend object would recreate the double seam C1 removed.

    `_t()` must NOT be `_b.active()`: after `use("ca_fft")` the active backend
    *is* this alias, so that spelling is infinite recursion. It resolves to the
    best available real library instead — which is also the honest semantics,
    since "ca_fft" never named an implementation, only the indirection.
    """
    name = "ca_fft"
    _PREFERENCE = ("pyfftw", "scipy", "numpy")

    def _t(self):
        cur = _b.active()
        if cur is not self:
            return cur
        for n in self._PREFERENCE:
            if n in _b.available():
                return _b._REGISTRY[n]
        raise RuntimeError("no library FFT backend registered")

    def fftn(self, a, **kw):         return self._t().fftn(a, **kw)
    def ifftn(self, a, **kw):        return self._t().ifftn(a, **kw)
    def fft2(self, a, **kw):         return self._t().fft2(a, **kw)
    def ifft2(self, a, **kw):        return self._t().ifft2(a, **kw)
    def fft(self, a, **kw):          return self._t().fft(a, **kw)
    def ifft(self, a, **kw):         return self._t().ifft(a, **kw)
    def chiral_transform(self, *a, **kw):
        return self._t().chiral_transform(*a, **kw)
    def describe(self):              return self._t().describe()


if "ca_fft" not in _b.available():
    _b.register(_CaFftAlias())
