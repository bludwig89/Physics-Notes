"""casim.numerics — the ONLY numerics surface. Roadmap C1, decision D8.

    from casim.numerics import xp, fft, linalg, rng, chiral

**D8: no physics module imports numpy, scipy or ca_fft directly.** Before C1
there were 169 files doing so, 273 `np.fft.*`/`ca_fft.*` call sites, and a
device seam (`casim.lattice.backend`) that **zero physics modules imported** —
its only importers were two tests and its own self-registration. Swapping in a
GPU backend would have changed nothing. One import surface is what makes the
swap real, and it is why the roadmap folds P2.2/P2.3/P2.4 into this phase.

What is here
------------
``fft``     — `fftn/ifftn/fft2/ifft2/fft/ifft`, plus `rfftn/irfftn` (new: the
              real-valued E and B fields were paying full complex transforms).
``linalg``  — `batched_matmul` (BLAS `zgemm`, unlike `np.einsum`), `dagger`,
              and the optional-scipy surface behind named-caller errors.
``rng``     — one independent stream per named consumer, so adding a channel
              does not perturb the numbers every other channel sees.
``chiral``  — `cmul` / `su2_apply` on explicit real pairs, per the CLAUDE.md
              caveat that numpy may drop a component on chiral transforms.
``backends``— the registry. `use("pyfftw")` and `use("cupy")` are the same
              kind of statement.

On ``xp``
---------
`xp` is the array namespace, and today it **is** numpy — deliberately, and this
is the honest part of the façade. Genuinely swapping the array namespace (MLX
or CuPy arrays flowing through every kernel) is not a C1 change: it would alter
the type every `ca_*` module receives and every `isinstance` check in the tree.
What C1 makes swappable is the *transform* layer, which is where the time goes.

So `xp` exists to give the migration one name to move to now, and a place to
put a real dispatch later. It is not advertised as more than that. Precision
holds at complex128 throughout: float32 eps is 1.2e-7, five orders above the
`machine` class's 1e-12 gate, and that gate is the product, not a tunable.

Environment
-----------
``CASIM_BACKEND=pyfftw``    pick a backend at startup
``CASIM_ALLOW_FLOAT32=1``   required before the MLX backend will activate
"""
from __future__ import annotations

import numpy as _np

from . import backends, chiral, fft, linalg, rng

# The array namespace. See "On xp" above for what this does and does not promise.
xp = _np

__all__ = ["xp", "fft", "linalg", "rng", "chiral", "backends", "describe"]


def describe() -> str:
    """One line naming the active FFT backend."""
    return backends.describe()
