"""
ca_lattice.py  —  Lattice configuration and k-grid utilities
=============================================================
Central location for all k-space grid construction.  Every propagator
and stepper should call `make_kgrid_*` here rather than recomputing
fftfreq / meshgrid inline.

Key exports
-----------
LatticeConfig      — dataclass holding shape + cached k-grids
make_kgrid_1d      — 1D k-axis (1D)
make_kgrid_2d      — (KX, KY) meshgrid for a 2D lattice
make_kgrid_3d      — (KX, KY, KZ) meshgrid for a 3D lattice
kgrid_from_shape   — dispatch on ndim (1, 2, or 3)
good_fft_sizes     — return N values near a target with low FFT cost

Design note
-----------
For 10× scaling the expensive part is *not* recomputing the k-grid
(that's O(N) trig) but recomputing the full unitary U(k) on every step.
The k-grid and U(k) are fixed once the lattice shape is fixed, so this
module serves as the single source of truth for k-grid construction that
`ca_propagator.py` caches into propagator objects.
"""

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple, Union

from ca_fft import fftfreq, memory_estimate


# ──────────────────────────────────────────────────────────────────
#  Low-level k-grid builders
# ──────────────────────────────────────────────────────────────────

def make_kgrid_1d(L: int) -> np.ndarray:
    """Return the 1D k-axis for a lattice of size L (angular freq units)."""
    return fftfreq(L) * 2.0 * math.pi


def make_kgrid_2d(Lx: int, Ly: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Return (KX, KY) meshgrid arrays of shape (Lx, Ly).

    k_x runs over  2π·{0, 1/Lx, …, (Lx−1)/Lx, −(Lx/2)/Lx, …, −1/Lx}
    (standard FFT frequency convention).
    """
    kx = fftfreq(Lx) * 2.0 * math.pi
    ky = fftfreq(Ly) * 2.0 * math.pi
    return np.meshgrid(kx, ky, indexing='ij')


def make_kgrid_3d(Lx: int, Ly: int, Lz: int,
                  ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Return (KX, KY, KZ) meshgrid arrays of shape (Lx, Ly, Lz).
    """
    kx = fftfreq(Lx) * 2.0 * math.pi
    ky = fftfreq(Ly) * 2.0 * math.pi
    kz = fftfreq(Lz) * 2.0 * math.pi
    return np.meshgrid(kx, ky, kz, indexing='ij')


def kgrid_from_shape(shape: tuple):
    """
    Dispatch to make_kgrid_1d / _2d / _3d based on len(shape).

    Returns a tuple of ndarray meshgrid components.
    """
    ndim = len(shape)
    if ndim == 1:
        return (make_kgrid_1d(shape[0]),)
    if ndim == 2:
        return make_kgrid_2d(*shape)
    if ndim == 3:
        return make_kgrid_3d(*shape)
    raise ValueError(f"kgrid_from_shape: ndim={ndim} not supported (1–3 only).")


# ──────────────────────────────────────────────────────────────────
#  LatticeConfig dataclass
# ──────────────────────────────────────────────────────────────────

@dataclass
class LatticeConfig:
    """
    Immutable description of a simulation lattice.

    Parameters
    ----------
    shape : tuple of int
        Lattice dimensions (Lx,) or (Lx, Ly) or (Lx, Ly, Lz).
    cache_kgrid : bool
        If True (default), the k-grid is computed once on init and
        stored in `self.kgrid`.  For very large lattices (L ≥ 512)
        you may want False to avoid allocating the meshgrid unless
        the propagator is building U(k).

    Attributes
    ----------
    shape        : tuple of int
    ndim         : int (1, 2, or 3)
    N            : int  (total number of lattice points)
    kgrid        : tuple of ndarray | None  (cached meshgrid)
    delta_k      : tuple of float  (bin spacing in k per axis)
    """
    shape: Tuple[int, ...]
    cache_kgrid: bool = True
    kgrid: Optional[Tuple] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        self.ndim = len(self.shape)
        self.N = math.prod(self.shape)
        # bin spacings
        self.delta_k = tuple(2.0 * math.pi / L for L in self.shape)
        if self.cache_kgrid:
            self.kgrid = kgrid_from_shape(self.shape)

    # ── convenience constructors ────────────────────────────────────

    @classmethod
    def cubic(cls, L: int, **kwargs) -> 'LatticeConfig':
        """Create an L×L×L cubic 3D lattice."""
        return cls((L, L, L), **kwargs)

    @classmethod
    def square(cls, L: int, **kwargs) -> 'LatticeConfig':
        """Create an L×L square 2D lattice."""
        return cls((L, L), **kwargs)

    # ── memory reporting ─────────────────────────────────────────────

    def memory(self, n_fields: int = 1,
               dtype=np.complex128) -> dict:
        """
        Estimate RAM for `n_fields` spinor component arrays on this lattice.

        Example (3D BCC Dirac — 4 components) ::

            cfg = LatticeConfig.cubic(64)
            cfg.memory(n_fields=4)
            # {'bytes': 67108864, 'MB': 67.1, 'GB': 0.067}
        """
        return memory_estimate(self.shape, n_fields=n_fields, dtype=dtype)

    def propagator_cache_memory(self, n_unitary_blocks: int = 8,
                                dtype=np.complex128) -> dict:
        """
        Estimate RAM for a cached propagator (e.g. 8 complex arrays for
        the BCC Dirac 4×4 unitary split into independent blocks).
        """
        return memory_estimate(self.shape,
                               n_fields=n_unitary_blocks, dtype=dtype)

    # ── scaling helpers ──────────────────────────────────────────────

    def scaled(self, factor: int) -> 'LatticeConfig':
        """Return a new LatticeConfig with all dimensions multiplied by factor."""
        return LatticeConfig(
            tuple(L * factor for L in self.shape),
            cache_kgrid=self.cache_kgrid,
        )

    def __repr__(self) -> str:
        mem = self.memory(n_fields=1)['MB']
        return (f"LatticeConfig(shape={self.shape}, N={self.N}, "
                f"delta_k={tuple(f'{dk:.4f}' for dk in self.delta_k)}, "
                f"~{mem:.1f} MB/field)")


# ──────────────────────────────────────────────────────────────────
#  Good FFT sizes
# ──────────────────────────────────────────────────────────────────

def _fft_cost(n: int) -> float:
    """
    Rough FFT cost proxy: n × log₂(n).  Valid for power-of-2 and smooth
    (only 2, 3, 5, 7 prime factors) sizes that most FFT libraries handle
    efficiently.
    """
    return n * math.log2(n)


def _is_smooth(n: int, primes=(2, 3, 5, 7)) -> bool:
    """Return True if n has no prime factors outside `primes`."""
    for p in primes:
        while n % p == 0:
            n //= p
    return n == 1


def good_fft_sizes(target: int,
                   window: int = 50,
                   primes: tuple = (2, 3, 5, 7)) -> list:
    """
    Return all integers in [target, target+window] whose only prime
    factors are in `primes`, sorted by FFT cost n×log₂(n).

    These are the sizes where FFTW / scipy.fft are fastest.

    Parameters
    ----------
    target : int
        Minimum desired size.
    window : int
        Search range above target.
    primes : tuple
        Allowed prime factors.

    Returns
    -------
    list of int, sorted ascending by cost.

    Example
    -------
    >>> good_fft_sizes(100)
    [100, 108, 112, 125, 128, ...]
    """
    results = [n for n in range(target, target + window + 1)
               if _is_smooth(n, primes)]
    results.sort(key=_fft_cost)
    return results


def next_good_fft_size(target: int,
                       primes: tuple = (2, 3, 5, 7)) -> int:
    """
    Return the smallest integer ≥ target with only prime factors in `primes`.

    Use this to round up lattice dimensions to FFT-optimal sizes.

    Example
    -------
    >>> next_good_fft_size(100)    # → 100 (= 4 × 25 = 2² × 5²)
    100
    >>> next_good_fft_size(101)    # → 108 (= 4 × 27 = 2² × 3³)
    108
    """
    n = target
    while not _is_smooth(n, primes):
        n += 1
    return n


# ──────────────────────────────────────────────────────────────────
#  Scaling table — quick survey for planning
# ──────────────────────────────────────────────────────────────────

def print_scaling_table(base_L: int = 64,
                        factors: tuple = (1, 2, 4, 5, 8, 10)):
    """
    Print a scaling table showing memory and FFT floor for multiples
    of base_L in 3D with a 4-spinor (Dirac) field.

    Usage::

        from ca_lattice import print_scaling_table
        print_scaling_table(64)
    """
    from ca_fft import fft_floor_estimate
    print(f"{'Scale':>7} {'L':>6} {'N (M pts)':>12} "
          f"{'4-spinor RAM':>14} {'FFT floor':>12} "
          f"{'Prop cache (8 blk)':>20}")
    print("-" * 80)
    for fac in factors:
        L = base_L * fac
        shape = (L, L, L)
        N = L ** 3
        mem4 = memory_estimate(shape, n_fields=4)
        mem8 = memory_estimate(shape, n_fields=8)
        floor = fft_floor_estimate(shape)
        print(f"{fac:>7}× {L:>6}  {N/1e6:>10.1f}M "
              f"  {mem4['GB']:>8.2f} GB "
              f"   {floor:>10.1e} "
              f"    {mem8['GB']:>8.2f} GB")


if __name__ == '__main__':
    import sys
    print("=== LatticeConfig demo ===")
    cfg = LatticeConfig.cubic(64)
    print(cfg)
    print(f"  4-spinor: {cfg.memory(4)['MB']:.1f} MB")
    print(f"  prop cache (8 blocks): {cfg.propagator_cache_memory(8)['MB']:.1f} MB")
    print()
    print("=== Scaling table (base L=64) ===")
    print_scaling_table(64)
    print()
    print("=== Good FFT sizes near 320 ===")
    print(good_fft_sizes(300, window=60))
