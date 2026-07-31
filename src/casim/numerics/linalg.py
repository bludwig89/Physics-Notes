"""casim.numerics.linalg — the linear-algebra surface. Roadmap C1.1 (D8).

Two jobs.

**1. `batched_matmul` — the einsum trap.** The gauge sector multiplies stacks of
3x3 SU(3) matrices with

    np.einsum('...ij,...jk->...ik', A, B)

`np.einsum` does NOT dispatch batched matrix products to BLAS. `np.matmul`
does — straight to `zgemm` for complex128. This is roadmap P2.5's second item,
and it belongs here rather than in a Monte-Carlo-specific fix because every
non-Abelian channel does it.

**It is not bit-identical, and that was measured rather than assumed.** BLAS
uses a different summation order (and FMA where available), so on complex128
3x3 stacks:

    max |einsum - matmul|      ~9e-16 absolute
    max relative difference    ~4e-16   (1-2 ULP)

and `optimize=True` does not close the gap either. That is four orders below
`casim.baselines.MACHINE_FLOOR` (1e-12) — the project's own definition of the
`machine` exactness class — so the substitution cannot move a residual across
any gate the model asserts. But it does mean **a call site cannot be swapped
and then called bit-identical**: the roadmap's own risk row says to record the
tolerance rather than hide it, so it is recorded here and asserted in
`tests/casim/test_fft_backend_equivalence.py` as a bound, not as equality.

**2. A single optional-scipy surface.** scipy is used in exactly 13 places
across the whole tree — `sparse`, `sparse.linalg.eigsh`, `linalg.eigh`,
`linalg.eigh_tridiagonal`, `optimize.brentq`. Every one of them is inside a
compute-once solve, never a per-tick path. So scipy stays an OPTIONAL
dependency and this module reports its absence with a message naming the
caller, rather than letting an ImportError surface from four modules deep.

(The earlier survey said 1,124 scipy sites. That was a regex counting `sp.`,
which in this repo is `sympy` in 63 files. The real number is 13.)
"""
from __future__ import annotations

from typing import Any

import numpy as np

__all__ = [
    "batched_matmul", "dagger", "have_scipy", "require_scipy",
    "eigh", "eigh_tridiagonal", "eigsh", "brentq", "sparse",
]


# ---------------------------------------------------------------------------
# Dense
# ---------------------------------------------------------------------------
def batched_matmul(a, b):
    """Stacked matrix product `...ij,...jk->...ik`, dispatched to BLAS.

    Drop-in for `np.einsum('...ij,...jk->...ik', a, b)`.
    """
    return np.matmul(a, b)


def dagger(a):
    """Conjugate transpose of the trailing two axes of a stack."""
    return np.conjugate(np.swapaxes(a, -1, -2))


# ---------------------------------------------------------------------------
# Optional scipy
# ---------------------------------------------------------------------------
try:                                    # pragma: no cover - env dependent
    import scipy.linalg as _sla
    import scipy.optimize as _sopt
    import scipy.sparse as _ssp
    import scipy.sparse.linalg as _ssla
    _HAVE = True
except ImportError:                     # pragma: no cover
    _sla = _sopt = _ssp = _ssla = None
    _HAVE = False


def have_scipy() -> bool:
    return _HAVE


def require_scipy(what: str) -> None:
    """Raise a message that names the caller, not a bare ImportError."""
    if not _HAVE:
        raise RuntimeError(
            f"{what} needs scipy, which is not installed. scipy is an "
            f"OPTIONAL dependency here — it appears in 13 compute-once solves "
            f"and no per-tick path — so install it only if you need this "
            f"solve: `pip install -e '.[fast]'`.")


def eigh(*a, **kw):
    require_scipy("linalg.eigh")
    return _sla.eigh(*a, **kw)


def eigh_tridiagonal(*a, **kw):
    require_scipy("linalg.eigh_tridiagonal")
    return _sla.eigh_tridiagonal(*a, **kw)


def eigsh(*a, **kw):
    require_scipy("sparse.linalg.eigsh")
    return _ssla.eigsh(*a, **kw)


def brentq(*a, **kw):
    require_scipy("optimize.brentq")
    return _sopt.brentq(*a, **kw)


class _SparseProxy:
    """`sparse.csr_matrix(...)` etc., with the same named-caller error."""

    def __getattr__(self, name: str) -> Any:
        require_scipy(f"sparse.{name}")
        return getattr(_ssp, name)


sparse = _SparseProxy()
