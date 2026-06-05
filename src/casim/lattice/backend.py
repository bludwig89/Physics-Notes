"""casim.lattice.backend — the one seam for FFTs and chiral transforms.

Roadmap §8 (deferred-but-seam-from-day-one).  All spectral work in the engine
should route through this module so the numerical backend can later be swapped
(hand-written chiral library per the CLAUDE.md numpy/scipy-on-chiral-transforms
concern, or numba/GPU) without touching physics code.

The default backend delegates to the audited ``ca_fft`` (which itself selects
scipy/pyfftw/numpy and manages worker threads), so behaviour is unchanged today.
A backend is any object exposing ``fftn/ifftn/fft2/ifft2/fft/ifft``.  Register
alternatives with :func:`register_backend` and select with :func:`use`.
"""
from __future__ import annotations

from typing import Any, Callable, Dict

import casim as _casim  # noqa: F401  (legacy dir on sys.path)
import ca_fft as _ca_fft  # noqa: E402


class _CaFftBackend:
    """Default backend: thin pass-through to the legacy ``ca_fft`` module."""
    name = "ca_fft"

    def fftn(self, a, **kw):  return _ca_fft.fftn(a, **kw)
    def ifftn(self, a, **kw): return _ca_fft.ifftn(a, **kw)
    def fft2(self, a, **kw):  return _ca_fft.fft2(a, **kw)
    def ifft2(self, a, **kw): return _ca_fft.ifft2(a, **kw)
    def fft(self, a, **kw):   return _ca_fft.fft(a, **kw)
    def ifft(self, a, **kw):  return _ca_fft.ifft(a, **kw)

    # Chiral-transform seam: kernels that must avoid numpy/scipy on chiral
    # matrices (CLAUDE.md) should call this rather than np.linalg directly.
    # The default raises so a swap-in is a deliberate, visible choice.
    def chiral_transform(self, *a, **kw):  # pragma: no cover
        raise NotImplementedError(
            "no chiral_transform on the default ca_fft backend; register a "
            "backend that provides one (the hand-written chiral library seam).")


_REGISTRY: Dict[str, Any] = {}
_ACTIVE: list = []  # single-element holder for the active backend


def register_backend(backend: Any, name: str | None = None) -> None:
    key = name or getattr(backend, "name", None)
    if not key:
        raise ValueError("backend needs a name")
    _REGISTRY[key] = backend


def use(name: str) -> None:
    """Select the active backend by name."""
    if name not in _REGISTRY:
        raise KeyError(f"unknown backend {name!r}; have {sorted(_REGISTRY)}")
    if _ACTIVE:
        _ACTIVE[0] = _REGISTRY[name]
    else:
        _ACTIVE.append(_REGISTRY[name])


def get_backend() -> Any:
    return _ACTIVE[0]


def backend_name() -> str:
    return getattr(_ACTIVE[0], "name", "?")


def available() -> list:
    return sorted(_REGISTRY)


# Module-level convenience functions (what kernels should import).
def fftn(a, **kw):  return _ACTIVE[0].fftn(a, **kw)
def ifftn(a, **kw): return _ACTIVE[0].ifftn(a, **kw)
def fft2(a, **kw):  return _ACTIVE[0].fft2(a, **kw)
def ifft2(a, **kw): return _ACTIVE[0].ifft2(a, **kw)
def fft(a, **kw):   return _ACTIVE[0].fft(a, **kw)
def ifft(a, **kw):  return _ACTIVE[0].ifft(a, **kw)
def chiral_transform(*a, **kw): return _ACTIVE[0].chiral_transform(*a, **kw)


# Register + activate the default on import.
register_backend(_CaFftBackend())
use("ca_fft")

__all__ = [
    "register_backend", "use", "get_backend", "backend_name", "available",
    "fftn", "ifftn", "fft2", "ifft2", "fft", "ifft", "chiral_transform",
]
