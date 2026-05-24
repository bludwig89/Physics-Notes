"""
ca_fft.py  —  FFT backend for the CA simulation suite
======================================================
Selects the fastest available FFT library and exposes a uniform API.

Priority order
--------------
1. pyfftw  — FFTW-based, multi-threaded, optional wisdom planning.
             Install: pip install pyfftw
2. scipy.fft  — multi-worker via concurrent.futures (Python threads).
               Ships with scipy; zero extra install.
3. numpy.fft  — always available; single-threaded.

Backend selection
-----------------
Import this module and call the wrappers (fftn, ifftn, fft2, ifft2, …) in
place of np.fft.* throughout the simulation.  No other change is needed.

To override the default choice at runtime::

    import ca_fft
    ca_fft.set_backend('numpy')          # force numpy
    ca_fft.set_workers(4)                # limit scipy/pyfftw to 4 threads
    ca_fft.set_workers(-1)               # use all CPUs (default)

FFT floor resolution
---------------------
The floating-point norm floor per FFT scales as ~ε_mach × log₂(N) for
an N-point transform.  For a 64³ complex128 array this is ~5e-14; for
320³ it is ~7e-14.  These are the hard limits of IEEE 754 arithmetic and
cannot be improved by choosing a different library.

To improve *spectral* resolution (frequency bin width):
  • Larger L  →  Δk = 2π/L shrinks; more k-modes sampled.
  • More timesteps N_t  →  Δω ≈ 2π/N_t in the time-domain DFT.
  • Zero-padding the time series (see ca_propagator.phase_rate_zeropad)
    gives sub-bin frequency resolution without extra propagation cost.
"""

import os
import math
import numpy as np

# ──────────────────────────────────────────────────────────────────
#  Backend detection
# ──────────────────────────────────────────────────────────────────

_backend = 'numpy'   # resolved below
_workers = -1        # -1 → all available CPUs

try:
    import scipy.fft as _scipy_fft
    _backend = 'scipy'
except ImportError:
    _scipy_fft = None

try:
    import pyfftw
    import pyfftw.interfaces.numpy_fft as _pyfftw_fft
    pyfftw.interfaces.cache.enable()
    _backend = 'pyfftw'
except ImportError:
    _pyfftw_fft = None


def get_backend() -> str:
    """Return the name of the active FFT backend."""
    return _backend


def set_backend(name: str) -> None:
    """
    Override the active backend.

    Parameters
    ----------
    name : 'numpy' | 'scipy' | 'pyfftw'
    """
    global _backend
    if name == 'pyfftw' and _pyfftw_fft is None:
        raise RuntimeError("pyfftw is not installed. "
                           "Run: pip install pyfftw")
    if name == 'scipy' and _scipy_fft is None:
        raise RuntimeError("scipy is not installed. "
                           "Run: pip install scipy")
    if name not in ('numpy', 'scipy', 'pyfftw'):
        raise ValueError(f"Unknown backend {name!r}; "
                         "choose 'numpy', 'scipy', or 'pyfftw'.")
    _backend = name


def set_workers(n: int) -> None:
    """
    Set the number of worker threads for scipy / pyfftw backends.

    Parameters
    ----------
    n : int
        Positive integer or -1 (= all CPUs).
    """
    global _workers
    _workers = n


def get_workers() -> int:
    """Return the configured number of worker threads."""
    return _workers


def _nworkers() -> int:
    """Resolve -1 to the actual CPU count."""
    if _workers == -1:
        return os.cpu_count() or 1
    return max(1, _workers)


# ──────────────────────────────────────────────────────────────────
#  Unified wrappers
# ──────────────────────────────────────────────────────────────────

def fftn(a, s=None, axes=None, norm=None):
    """N-dimensional FFT (forward), using the active backend."""
    if _backend == 'pyfftw':
        return _pyfftw_fft.fftn(a, s=s, axes=axes, norm=norm)
    if _backend == 'scipy':
        return _scipy_fft.fftn(a, s=s, axes=axes, norm=norm,
                               workers=_nworkers())
    return np.fft.fftn(a, s=s, axes=axes, norm=norm)


def ifftn(a, s=None, axes=None, norm=None):
    """N-dimensional inverse FFT, using the active backend."""
    if _backend == 'pyfftw':
        return _pyfftw_fft.ifftn(a, s=s, axes=axes, norm=norm)
    if _backend == 'scipy':
        return _scipy_fft.ifftn(a, s=s, axes=axes, norm=norm,
                                workers=_nworkers())
    return np.fft.ifftn(a, s=s, axes=axes, norm=norm)


def fft2(a, s=None, axes=(-2, -1), norm=None):
    """2D FFT (forward), using the active backend."""
    if _backend == 'pyfftw':
        return _pyfftw_fft.fft2(a, s=s, axes=axes, norm=norm)
    if _backend == 'scipy':
        return _scipy_fft.fft2(a, s=s, axes=axes, norm=norm,
                               workers=_nworkers())
    return np.fft.fft2(a, s=s, axes=axes, norm=norm)


def ifft2(a, s=None, axes=(-2, -1), norm=None):
    """2D inverse FFT, using the active backend."""
    if _backend == 'pyfftw':
        return _pyfftw_fft.ifft2(a, s=s, axes=axes, norm=norm)
    if _backend == 'scipy':
        return _scipy_fft.ifft2(a, s=s, axes=axes, norm=norm,
                                workers=_nworkers())
    return np.fft.ifft2(a, s=s, axes=axes, norm=norm)


def fft(a, n=None, axis=-1, norm=None):
    """1D FFT (forward), using the active backend."""
    if _backend == 'pyfftw':
        return _pyfftw_fft.fft(a, n=n, axis=axis, norm=norm)
    if _backend == 'scipy':
        return _scipy_fft.fft(a, n=n, axis=axis, norm=norm,
                              workers=_nworkers())
    return np.fft.fft(a, n=n, axis=axis, norm=norm)


def ifft(a, n=None, axis=-1, norm=None):
    """1D inverse FFT, using the active backend."""
    if _backend == 'pyfftw':
        return _pyfftw_fft.ifft(a, n=n, axis=axis, norm=norm)
    if _backend == 'scipy':
        return _scipy_fft.ifft(a, n=n, axis=axis, norm=norm,
                               workers=_nworkers())
    return np.fft.ifft(a, n=n, axis=axis, norm=norm)


# ──────────────────────────────────────────────────────────────────
#  Convenience: fftfreq always from numpy (no performance concern)
# ──────────────────────────────────────────────────────────────────

fftfreq = np.fft.fftfreq
rfftfreq = np.fft.rfftfreq


# ──────────────────────────────────────────────────────────────────
#  Memory and performance utilities
# ──────────────────────────────────────────────────────────────────

def memory_estimate(shape, n_fields: int = 1,
                    dtype=np.complex128) -> dict:
    """
    Estimate RAM for `n_fields` arrays of shape `shape` and `dtype`.

    Returns a dict with keys 'bytes', 'MB', 'GB'.

    Example
    -------
    >>> memory_estimate((320, 320, 320), n_fields=4)
    {'bytes': 2097152000, 'MB': 2000.0, 'GB': 1.953...}
    """
    nbytes = math.prod(shape) * n_fields * np.dtype(dtype).itemsize
    return {
        'bytes': nbytes,
        'MB':    nbytes / 1e6,
        'GB':    nbytes / 1e9,
    }


def fft_floor_estimate(shape) -> float:
    """
    Rough estimate of the floating-point norm floor for a single
    complex128 FFT of `shape`.

    Formula: ε_machine × log2(N) × √N  where N = prod(shape).

    This represents the expected absolute norm error after one forward +
    inverse FFT pair.  Actual measured values are typically 2–5× lower.
    """
    N = math.prod(shape)
    log_N = math.log2(N)
    return float(np.finfo(np.float64).eps * log_N * math.sqrt(N))


# ──────────────────────────────────────────────────────────────────
#  Self-report
# ──────────────────────────────────────────────────────────────────

def info() -> str:
    """Return a one-line string describing the active configuration."""
    return (f"ca_fft backend={_backend!r}  "
            f"workers={'all' if _workers == -1 else _workers}  "
            f"CPUs={os.cpu_count()}")


if __name__ == '__main__':
    print(info())
    shape3d = (64, 64, 64)
    est = memory_estimate(shape3d, n_fields=4)
    print(f"Memory for 4×{shape3d} complex128: {est['MB']:.1f} MB")
    for L in [32, 64, 128, 256, 320, 640]:
        s = (L, L, L)
        e = memory_estimate(s, n_fields=4)
        floor = fft_floor_estimate(s)
        print(f"  L={L:4d}  4-spinor RAM={e['MB']:7.1f} MB  "
              f"FFT floor≈{floor:.1e}")
