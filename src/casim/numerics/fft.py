"""casim.numerics.fft — the FFT surface. Roadmap C1.1 (D8).

Migrated from `ca-simulation/ca_fft.py` (pre-clean original in
`deprecated/code/ca_fft.py`; a deprecation shim remains at the old path until
C9). The library-selection `if/elif` that used to live in every wrapper now
lives in `casim.numerics.backends` as backend *objects*, so choosing pyfftw and
choosing a GPU are the same kind of statement rather than two unrelated seams.

The public API is unchanged, because 20 test files and ~40 kernels call it:

    fftn ifftn fft2 ifft2 fft ifft fftfreq rfftfreq
    get_backend set_backend set_workers get_workers describe info
    memory_estimate fft_floor_estimate

New in C1:

    rfftn irfftn      real-input transforms — the E and B fields are real and
                      were paying full complex transforms (roadmap C1.1)

FFT floor resolution
--------------------
The floating-point norm floor per FFT scales as ~eps_mach x log2(N) for an
N-point transform. For a 64^3 complex128 array this is ~5e-14; for 320^3 it is
~7e-14. These are the hard limits of IEEE 754 and cannot be improved by
choosing a different library — which is exactly why `casim.baselines` treats
sub-1e-12 movement as noise rather than drift.

To improve *spectral* resolution (frequency bin width):
  * larger L         -> dk = 2*pi/L shrinks; more k-modes sampled;
  * more timesteps   -> dw ~ 2*pi/N_t in the time-domain DFT;
  * zero-padding the time series (`ca_propagator.phase_rate_zeropad`) gives
    sub-bin frequency resolution without extra propagation cost.
"""
from __future__ import annotations

import math
import os

import numpy as np

from . import backends as _b

__all__ = [
    "fftn", "ifftn", "fft2", "ifft2", "fft", "ifft", "rfftn", "irfftn",
    "rfft", "irfft",
    "fftfreq", "rfftfreq", "get_backend", "set_backend", "set_workers",
    "get_workers", "describe", "info", "memory_estimate", "fft_floor_estimate",
]


# ---------------------------------------------------------------------------
# Backend control (the ca_fft API, preserved verbatim)
# ---------------------------------------------------------------------------
def get_backend() -> str:
    """Name of the active FFT backend."""
    return _b.active_name()


def set_backend(name: str) -> None:
    """Override the active backend: 'numpy' | 'scipy' | 'pyfftw' | 'cupy' | 'mlx'."""
    try:
        _b.use(name)
    except KeyError:
        raise RuntimeError(
            f"backend {name!r} is not available; have {_b.available()}. "
            f"Install it (`pip install -e '.[fast]'` for pyfftw) or choose "
            f"another.") from None


def set_workers(n: int) -> None:
    """Worker threads for the threaded backends (scipy, pyfftw)."""
    _b.set_workers(n)


def get_workers() -> int:
    return _b.get_workers()


def _nworkers() -> int:
    return _b.nworkers()


def describe() -> str:
    """One-line description of the active backend, for logs and the CLI.

    Roadmap P2.1. The fallback chain used to be silent: `pyfftw` was never a
    declared dependency, so every run quietly used single-threaded scipy while
    the module docstring advertised FFTW. Surfacing this is the actual fix.
    """
    return _b.describe()


def info() -> str:
    return (f"casim.numerics.fft backend={get_backend()!r}  "
            f"workers={'all' if get_workers() == -1 else get_workers()}  "
            f"CPUs={os.cpu_count()}  available={_b.available()}")


# ---------------------------------------------------------------------------
# Transforms
# ---------------------------------------------------------------------------
def fftn(a, s=None, axes=None, norm=None):
    """N-dimensional forward FFT via the active backend."""
    return _b.active().fftn(a, s=s, axes=axes, norm=norm)


def ifftn(a, s=None, axes=None, norm=None):
    """N-dimensional inverse FFT via the active backend."""
    return _b.active().ifftn(a, s=s, axes=axes, norm=norm)


def fft2(a, s=None, axes=(-2, -1), norm=None):
    return _b.active().fft2(a, s=s, axes=axes, norm=norm)


def ifft2(a, s=None, axes=(-2, -1), norm=None):
    return _b.active().ifft2(a, s=s, axes=axes, norm=norm)


def fft(a, n=None, axis=-1, norm=None):
    return _b.active().fft(a, n=n, axis=axis, norm=norm)


def ifft(a, n=None, axis=-1, norm=None):
    return _b.active().ifft(a, n=n, axis=axis, norm=norm)


def rfftn(a, s=None, axes=None, norm=None):
    """Forward transform of a REAL array (roadmap C1.1).

    The (E, B) pair is real-valued and has always paid a full complex
    transform. `rfftn` stores only the non-redundant half-spectrum: ~2x less
    memory and ~2x less work. It is a different output SHAPE, not a different
    result, so it is opt-in per call site rather than a silent substitution —
    `irfftn` needs the original last-axis length `s` to invert unambiguously.
    """
    return _b.active().rfftn(a, s=s, axes=axes, norm=norm)


def irfftn(a, s=None, axes=None, norm=None):
    """Inverse of :func:`rfftn`. Pass `s` (the real shape) for odd lengths.

    If `s` is given and `axes` is not, `axes` is filled in as the trailing
    `len(s)` axes. numpy 2.0 deprecated that combination and will eventually
    raise; more to the point, its fallback behaviour is not the one a caller
    passing a 3-tuple `s` expects, so leaving it implicit is a silent-wrong-
    answer risk rather than a warning to suppress.
    """
    if s is not None and axes is None:
        axes = tuple(range(-len(s), 0))
    return _b.active().irfftn(a, s=s, axes=axes, norm=norm)


def rfft(a, n=None, axis=-1, norm=None):
    """1-D forward transform of a REAL array."""
    return _b.active().rfft(a, n=n, axis=axis, norm=norm)


def irfft(a, n=None, axis=-1, norm=None):
    """Inverse of :func:`rfft`. Pass `n` (the real length) for odd lengths."""
    return _b.active().irfft(a, n=n, axis=axis, norm=norm)


# fftfreq is pure index arithmetic — no backend concern.
fftfreq = np.fft.fftfreq
rfftfreq = np.fft.rfftfreq


# ---------------------------------------------------------------------------
# Memory and precision utilities
# ---------------------------------------------------------------------------
def memory_estimate(shape, n_fields: int = 1, dtype=np.complex128) -> dict:
    """RAM for `n_fields` arrays of `shape` and `dtype`.

    >>> memory_estimate((320, 320, 320), n_fields=4)['GB']
    1.953125
    """
    nbytes = math.prod(shape) * n_fields * np.dtype(dtype).itemsize
    return {"bytes": nbytes, "MB": nbytes / 1e6, "GB": nbytes / 1e9}


def fft_floor_estimate(shape) -> float:
    """Expected absolute norm error after one forward+inverse complex128 FFT.

    Formula: eps_machine x log2(N) x sqrt(N), N = prod(shape). Measured values
    are typically 2-5x lower. This is the number `casim.baselines.MACHINE_FLOOR`
    exists to respect.
    """
    N = math.prod(shape)
    return float(np.finfo(np.float64).eps * math.log2(N) * math.sqrt(N))


if __name__ == "__main__":
    print(info())
    for L in (32, 64, 128, 256, 320, 640):
        s = (L, L, L)
        e = memory_estimate(s, n_fields=4)
        print(f"  L={L:4d}  4-spinor RAM={e['MB']:7.1f} MB  "
              f"FFT floor~{fft_floor_estimate(s):.1e}")
