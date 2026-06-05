"""casim.gravity — F64 dielectric gravity.

Gravity is a single impedance-matched lattice **dielectric** K(x) renormalising
the (E,B) rotation rule (Finding 64), *not* a sourced metric.  Canonical index
K = exp(2GM/rc²) with A=1/K, B=K (reciprocal lock AB≡1); GR-identical
(PPN β=γ=1).

Re-exports:
    poisson_open  — pure-numpy open-boundary Poisson solver (always available).
    ca_curved     — dynamical variable-c Weyl stepper (needs SciPy; lazy).
    ca_emqg       — EM-quantum-gravity helpers (needs SciPy via ca_curved; lazy).
"""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401

# Always-available, pure-numpy Poisson background.
import poisson_open as poisson_open  # noqa: E402
from poisson_open import (  # noqa: E402
    solve_poisson_3d_open,
    gaussian_mass_3d,
)


def _lazy(name):
    """Import a SciPy-dependent gravity module on demand; ``None`` if absent."""
    try:
        return _il.import_module(name)
    except Exception:
        return None


def ca_curved():
    """Return the ``ca_curved`` module (dynamical varc stepper) or None."""
    return _lazy("ca_curved")


def ca_emqg():
    """Return the ``ca_emqg`` module or None."""
    return _lazy("ca_emqg")


__all__ = [
    "poisson_open", "solve_poisson_3d_open", "gaussian_mass_3d",
    "ca_curved", "ca_emqg",
]
