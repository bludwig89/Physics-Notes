"""casim.numerics.precision — one owner for the float32 question. Roadmap P2.7.

The rule this module enforces is not a preference, it is the product: the
`machine` exactness class gates at a **relative 1e-12**, and `float32` eps is
$1.2\\times10^{-7}$ — **five orders above it**. So a device path that silently
runs in single precision does not make results slightly worse, it invalidates
every `machine_precision` claim that flows through it, while continuing to
report success.

Why this exists as a module rather than as a line in each device path
--------------------------------------------------------------------
It already failed once by being a line. C1 gave the MLX backend a correct
`CASIM_ALLOW_FLOAT32` gate and a test asserting no device backend can
self-activate — and the JAX path in `casim.engine.gauge.weak_wmu` (written
earlier, and reachable via `use_jax()`) had **neither**, because it is a fused
`@jax.jit` kernel rather than a registered FFT backend, so the backend
registry's guard did not cover it. Two device paths, one guarded, and the
unguarded one was invisible to the ratchet as well (`audit_numerics.py`'s regex
matched `np`/`numpy`, not `jnp`).

The lesson is that the policy has to live somewhere both kinds of path import,
so a new accelerator cannot arrive without meeting it. Roadmap P2.7.

Usage
-----
    from casim.numerics.precision import require_float64

    require_float64("jax", is_float64=jnp.zeros(1, jnp.complex128).dtype
                                     == jnp.complex128)

Environment
-----------
``CASIM_ALLOW_FLOAT32=1``  accept a float32-backed path. Never set this for a
                          run whose scenario or test record carries a
                          `machine` / `machine_precision` exactness claim.
"""
from __future__ import annotations

import os

#: The `machine` exactness class's relative gate. Mirrors
#: ``casim.baselines.MACHINE_FLOOR``; kept as a module constant here so a
#: device path can quote the number it is being measured against.
MACHINE_GATE = 1e-12

#: float32 machine epsilon, for the error message.
FLOAT32_EPS = 1.1920929e-07


def allow_float32() -> bool:
    """True if the operator has explicitly accepted single precision."""
    return os.environ.get("CASIM_ALLOW_FLOAT32") == "1"


def require_float64(name: str, is_float64: bool) -> None:
    """Refuse to activate a float32-backed path unless it was accepted.

    ``name`` is the path being activated (``"jax"``, ``"mlx"``, …) and appears
    in the error, because "float32 refused" without a name is a message nobody
    can act on.

    Raises
    ------
    RuntimeError
        if ``is_float64`` is False and ``CASIM_ALLOW_FLOAT32`` is not ``1``.
    """
    if is_float64 or allow_float32():
        return
    raise RuntimeError(
        f"{name} is float32-backed here and would silently break every "
        f"machine_precision claim: float32 eps {FLOAT32_EPS:.3g} is five "
        f"orders above the machine gate {MACHINE_GATE:.0e}. "
        f"Set CASIM_ALLOW_FLOAT32=1 to accept that — and do not set it for a "
        f"run carrying a machine-precision claim."
    )


def float32_note(name: str) -> str:
    """The one-line disclosure a float32 path should put in `describe()`."""
    return (f"{name} — FLOAT32 accepted via CASIM_ALLOW_FLOAT32; excluded "
            f"from machine_precision scenarios")
