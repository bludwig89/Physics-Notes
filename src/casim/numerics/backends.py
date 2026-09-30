"""casim.numerics.backends — the one device/library seam. Roadmap C1.1 (D8).

Before C1 this repo had **two** seams for the same job and neither was load-bearing:

  * `ca_fft` selected numpy/scipy/pyfftw with a module-level `_backend` string
    and an `if/elif` in every wrapper — a *library* seam;
  * `casim.lattice.backend` held an object registry with a seven-method
    protocol — a *device* seam, which **zero physics modules imported**. Its
    only importers were two tests and its own self-registration.

Having two meant a GPU backend could be registered in one while every kernel
kept calling the other. This module is the single registry, and the library
choices are now backend *objects* registered alongside any device backend, so
"use pyfftw" and "use MLX" are the same kind of statement.

The protocol is seven methods: `fftn ifftn fft2 ifft2 fft ifft` plus
`chiral_transform`. A backend is any object exposing them and a `name`.

**Every backend must clear `tests/casim/test_fft_backend_equivalence.py`**
before it ships: agreement to 1e-12 relative, round-trip identity, thread count
cannot change the result, and — the chiral-specific one CLAUDE.md demands —
real and imaginary parts both survive.
"""
from __future__ import annotations

import os
from typing import Any, Dict

import numpy as np

from . import precision as _precision

_np_complex128 = np.complex128

__all__ = [
    "register", "use", "active", "active_name", "available", "describe",
    "set_workers", "get_workers", "nworkers", "NumpyBackend",
]

_REGISTRY: Dict[str, Any] = {}
_ACTIVE: list = []
_WORKERS = [-1]                       # -1 -> all CPUs


# ---------------------------------------------------------------------------
# Worker threads
# ---------------------------------------------------------------------------
def set_workers(n: int) -> None:
    """Thread count for backends that are threaded (scipy, pyfftw)."""
    _WORKERS[0] = n


def get_workers() -> int:
    return _WORKERS[0]


def nworkers() -> int:
    return os.cpu_count() or 1 if _WORKERS[0] == -1 else max(1, _WORKERS[0])


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
def register(backend: Any, name: str | None = None) -> None:
    key = name or getattr(backend, "name", None)
    if not key:
        raise ValueError("backend needs a name")
    _REGISTRY[key] = backend


def use(name: str) -> None:
    if name not in _REGISTRY:
        raise KeyError(f"unknown backend {name!r}; have {sorted(_REGISTRY)}")
    # The float32 refusal lives HERE, not only on the CASIM_BACKEND path, so
    # use()/fft.set_backend() cannot switch to a float32 device silently
    # (2026-09-29; before, only the env-var route was gated).
    if name == "mlx":
        _precision.require_float64("use('mlx')", is_float64=False)
    elif name == "jax":
        _precision.require_float64(
            "use('jax')", is_float64=getattr(_REGISTRY[name], "_float64", False))
    if _ACTIVE:
        _ACTIVE[0] = _REGISTRY[name]
    else:
        _ACTIVE.append(_REGISTRY[name])


def active() -> Any:
    return _ACTIVE[0]


def active_name() -> str:
    return getattr(_ACTIVE[0], "name", "?")


def available() -> list[str]:
    return sorted(_REGISTRY)


def describe() -> str:
    """One line naming the live backend. P2.1's rule: a fallback you can see is
    a choice, one you cannot is a bug."""
    b = _ACTIVE[0]
    if hasattr(b, "describe"):
        return b.describe()
    return getattr(b, "name", "?")


# ---------------------------------------------------------------------------
# Backends
# ---------------------------------------------------------------------------
class _Base:
    """Default `chiral_transform`: refuse.

    Not a stub for politeness. CLAUDE.md's standing caveat is that numpy/scipy
    on chiral transforms may drop the real or imaginary part, so silently
    falling back to a vendored routine is the exact failure mode to avoid. A
    backend that has not been checked against `casim.numerics.chiral` says so.
    """
    name = "?"

    def chiral_transform(self, *a, **kw):        # pragma: no cover
        raise NotImplementedError(
            f"backend {self.name!r} has no verified chiral_transform. Use "
            f"casim.numerics.chiral (the hand-rolled explicit-real core), or "
            f"register a backend that has cleared the chiral half of "
            f"tests/casim/test_fft_backend_equivalence.py.")


class NumpyBackend(_Base):
    """`numpy.fft`. Always available, single-threaded, the correctness anchor."""
    name = "numpy"

    def fftn(self, a, **kw):  return np.fft.fftn(a, **kw)
    def ifftn(self, a, **kw): return np.fft.ifftn(a, **kw)
    def fft2(self, a, **kw):  return np.fft.fft2(a, **kw)
    def ifft2(self, a, **kw): return np.fft.ifft2(a, **kw)
    def fft(self, a, **kw):   return np.fft.fft(a, **kw)
    def ifft(self, a, **kw):  return np.fft.ifft(a, **kw)
    def rfftn(self, a, **kw): return np.fft.rfftn(a, **kw)
    def irfftn(self, a, **kw): return np.fft.irfftn(a, **kw)
    def rfft(self, a, **kw):  return np.fft.rfft(a, **kw)
    def irfft(self, a, **kw): return np.fft.irfft(a, **kw)

    def describe(self) -> str:
        return ("numpy.fft (single-threaded) — neither pyfftw nor scipy is "
                "installed; this is the slowest path")


class ScipyBackend(_Base):
    """`scipy.fft`, multi-worker via a thread pool."""
    name = "scipy"

    def __init__(self, mod) -> None:
        self._m = mod

    def fftn(self, a, **kw):  return self._m.fftn(a, workers=nworkers(), **kw)
    def ifftn(self, a, **kw): return self._m.ifftn(a, workers=nworkers(), **kw)
    def fft2(self, a, **kw):  return self._m.fft2(a, workers=nworkers(), **kw)
    def ifft2(self, a, **kw): return self._m.ifft2(a, workers=nworkers(), **kw)
    def fft(self, a, **kw):   return self._m.fft(a, workers=nworkers(), **kw)
    def ifft(self, a, **kw):  return self._m.ifft(a, workers=nworkers(), **kw)
    def rfftn(self, a, **kw): return self._m.rfftn(a, workers=nworkers(), **kw)
    def irfftn(self, a, **kw): return self._m.irfftn(a, workers=nworkers(), **kw)
    def rfft(self, a, **kw):  return self._m.rfft(a, workers=nworkers(), **kw)
    def irfft(self, a, **kw): return self._m.irfft(a, workers=nworkers(), **kw)

    def describe(self) -> str:
        return (f"scipy.fft ({nworkers()} workers) — pyfftw not installed; "
                f"`pip install -e '.[fast]'` for the FFTW backend")


class PyfftwBackend(_Base):
    """FFTW via pyfftw's numpy_fft interface.

    `threads=` is passed on every call. P2.1 found that the six original call
    sites omitted it, so `set_workers` was documented as applying to pyfftw and
    did nothing — the FFTW path ran single-threaded even when installed.
    """
    name = "pyfftw"

    def __init__(self, mod) -> None:
        self._m = mod

    def fftn(self, a, **kw):  return self._m.fftn(a, threads=nworkers(), **kw)
    def ifftn(self, a, **kw): return self._m.ifftn(a, threads=nworkers(), **kw)
    def fft2(self, a, **kw):  return self._m.fft2(a, threads=nworkers(), **kw)
    def ifft2(self, a, **kw): return self._m.ifft2(a, threads=nworkers(), **kw)
    def fft(self, a, **kw):   return self._m.fft(a, threads=nworkers(), **kw)
    def ifft(self, a, **kw):  return self._m.ifft(a, threads=nworkers(), **kw)
    def rfftn(self, a, **kw): return self._m.rfftn(a, threads=nworkers(), **kw)
    def irfftn(self, a, **kw): return self._m.irfftn(a, threads=nworkers(), **kw)
    def rfft(self, a, **kw):  return self._m.rfft(a, threads=nworkers(), **kw)
    def irfft(self, a, **kw): return self._m.irfft(a, threads=nworkers(), **kw)

    def describe(self) -> str:
        return f"pyfftw (FFTW, {nworkers()} threads, plan cache on)"


class _DeviceBackend(_Base):
    """Shared shape for array-library backends (MLX, CuPy).

    Both move the array to the device, transform, and bring it back, so the
    calling kernel keeps receiving a numpy array and no physics module has to
    know a device exists. That round-trip is the cost; it is worth paying only
    for transforms large enough to dominate it, which is why these are opt-in
    rather than auto-selected. **Neither is exercised on this machine** — see
    `docs/status/C1-completion-overview.md`.
    """

    def __init__(self, mod) -> None:
        self._m = mod

    def _to(self, a):    raise NotImplementedError
    def _from(self, a):  raise NotImplementedError
    def _fft(self):      raise NotImplementedError

    def fftn(self, a, **kw):  return self._from(self._fft().fftn(self._to(a), **kw))
    def ifftn(self, a, **kw): return self._from(self._fft().ifftn(self._to(a), **kw))
    def fft2(self, a, **kw):  return self._from(self._fft().fft2(self._to(a), **kw))
    def ifft2(self, a, **kw): return self._from(self._fft().ifft2(self._to(a), **kw))
    def fft(self, a, **kw):   return self._from(self._fft().fft(self._to(a), **kw))
    def ifft(self, a, **kw):  return self._from(self._fft().ifft(self._to(a), **kw))
    def rfftn(self, a, **kw): return self._from(self._fft().rfftn(self._to(a), **kw))
    def irfftn(self, a, **kw): return self._from(self._fft().irfftn(self._to(a), **kw))
    def rfft(self, a, **kw):  return self._from(self._fft().rfft(self._to(a), **kw))
    def irfft(self, a, **kw): return self._from(self._fft().irfft(self._to(a), **kw))


class CupyBackend(_DeviceBackend):
    """CUDA via CuPy (roadmap P2.4 'later, cloud')."""
    name = "cupy"

    def _to(self, a):   return self._m.asarray(a)
    def _from(self, a): return self._m.asnumpy(a)
    def _fft(self):     return self._m.fft

    def describe(self) -> str:
        return f"cupy (CUDA device FFT) — {self._m.cuda.runtime.getDeviceCount()} device(s)"


class JaxBackend(_DeviceBackend):
    """JAX (CPU/Metal/CUDA) — roadmap **P2.7**.

    Registered so that the JAX device path is *visible* the way CuPy and MLX
    are. Before P2.7 there was a live JAX path in
    `casim.engine.gauge.weak_wmu` (two `@jax.jit` kernels, opt-in via
    `use_jax()`) that was not in this registry at all — so the "no device
    backend auto-selects" test did not cover it, and `audit_numerics.py`'s
    `np|numpy` regex could not see its eight `jnp.fft` calls.

    **x64 is not optional here.** JAX defaults to float32 and *silently
    downcasts* `complex128` input, which is worse than refusing it. So
    registration enables `jax_enable_x64` and then **verifies** it took effect;
    if it did not, the shared `casim.numerics.precision` gate refuses the
    backend unless `CASIM_ALLOW_FLOAT32=1`. That check is a measurement of the
    live config, not a trust in the `update()` call — `jax_enable_x64` is
    ignored once arrays have been created, so the order matters and the
    verification is what makes it safe.
    """
    name = "jax"

    def __init__(self, mod, float64: bool) -> None:
        super().__init__(mod)
        self._float64 = bool(float64)

    def _to(self, a):   return self._m.numpy.asarray(a)
    def _from(self, a): return np.asarray(a)
    def _fft(self):     return self._m.numpy.fft

    def describe(self) -> str:
        dev = ", ".join(sorted({d.platform for d in self._m.devices()}))
        if not self._float64:
            return _precision.float32_note(f"jax ({dev})")
        return f"jax ({dev}, x64) — device FFT"


class MlxBackend(_DeviceBackend):
    """Apple-Silicon Metal via MLX (roadmap P2.4 'now').

    **Precision warning, and it is disqualifying by default.** MLX's FFT is
    float32-backed. `complex128` is not a preference in this project, it is the
    product: `float32` eps is 1.2e-7, five orders above the `machine` class's
    1e-12 gate. So this backend refuses to activate unless
    `CASIM_ALLOW_FLOAT32=1` is set, and it must never be used for a scenario
    that carries a `machine_precision` claim. It is for viz, density fields,
    and statistically-averaged MC observables.
    """
    name = "mlx"

    def _to(self, a):   return self._m.array(a)
    def _from(self, a): return np.array(a)
    def _fft(self):     return self._m.fft

    def describe(self) -> str:
        return _precision.float32_note("mlx (Metal)")


# ---------------------------------------------------------------------------
# Discovery: register whatever is importable, prefer the fastest safe one.
# ---------------------------------------------------------------------------
def _discover() -> str:
    register(NumpyBackend())
    best = "numpy"

    try:
        import scipy.fft as _sf
        register(ScipyBackend(_sf))
        best = "scipy"
    except ImportError:
        pass

    try:
        import pyfftw
        import pyfftw.interfaces.numpy_fft as _pf
        pyfftw.interfaces.cache.enable()
        # Without a keepalive the plan cache is dropped between calls and every
        # transform re-plans, which costs more than the threading gains.
        pyfftw.interfaces.cache.set_keepalive_time(60.0)
        register(PyfftwBackend(_pf))
        best = "pyfftw"
    except ImportError:
        pass

    try:
        import cupy as _cp
        if _cp.cuda.runtime.getDeviceCount() > 0:
            register(CupyBackend(_cp))
    except Exception:
        pass

    try:
        import mlx.core as _mx
        register(MlxBackend(_mx))
    except Exception:
        pass

    # P2.7. x64 must be enabled BEFORE any array is created, and then verified:
    # `jax_enable_x64` is ignored once JAX has been used, so a successful
    # `update()` call is not evidence. Measure the live dtype instead.
    try:
        import jax as _jx
        try:
            _jx.config.update("jax_enable_x64", True)
        except Exception:
            pass
        _f64 = _jx.numpy.zeros(1, dtype=_jx.numpy.complex128).dtype == \
            _np_complex128
        register(JaxBackend(_jx, _f64))
    except Exception:
        pass

    # Device backends are registered but never auto-selected: CuPy needs a
    # sized problem to beat the host round-trip, and MLX is float32.
    env = os.environ.get("CASIM_BACKEND")
    if env:
        if env not in _REGISTRY:
            raise RuntimeError(
                f"CASIM_BACKEND={env!r} is not available; have "
                f"{sorted(_REGISTRY)}")
        if env == "mlx":
            _precision.require_float64("CASIM_BACKEND=mlx", is_float64=False)
        if env == "jax":
            _precision.require_float64(
                "CASIM_BACKEND=jax", is_float64=_REGISTRY[env]._float64)
        best = env
    use(best)
    return best


_discover()
