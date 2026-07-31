"""casim.gravity — F64 dielectric gravity.

Gravity is a single impedance-matched lattice **dielectric** K(x) renormalising
the (E,B) rotation rule (Finding 64), *not* a sourced metric.  Canonical index
K = exp(2GM/rc²) with A=1/K, B=K (reciprocal lock AB≡1); GR-identical
(PPN β=γ=1).

Re-exports:
    ca_gravity    — the main-model gravity field element (F64 mainlined):
                    canonical dielectric maps, D-EM8 dynamical Φ wave stepper,
                    F106 T⁰⁰ sourcing (structural coupling = 1 in lattice
                    units; G_LATTICE = 1/(72π)), F62 lapse mix.  Pure numpy.
    poisson_open  — pure-numpy open-boundary Poisson solver (always available).
    ca_curved     — dynamical variable-c Weyl stepper (needs SciPy; lazy).
    ca_emqg       — EM-quantum-gravity helpers (needs SciPy via ca_curved; lazy).
"""
from __future__ import annotations

import importlib as _il
import casim as _casim  # noqa: F401

# The gravity field element (pure numpy, always available).
from casim.engine.interactions import gravity as ca_gravity  # noqa: E402
from casim.engine.interactions.gravity import (  # noqa: E402
    C_LAT_BCC, F106_COEFF_LATTICE, G_LATTICE,
    K_canonical, dielectric_from_phi,
    T00_dirac_rest, T00_field_energy, phi_source,
    lap_nd, solve_phi_poisson, phi_wave_step, phi_field_energy,
    lapse_mix_half,
)

# Always-available, pure-numpy Poisson background.
from casim.engine.lattice import poisson_open as poisson_open  # noqa: E402
from casim.engine.lattice.poisson_open import (  # noqa: E402
    solve_poisson_3d_open,
    gaussian_mass_3d,
)


def _lazy(name):
    """Import a SciPy-dependent gravity module on demand; ``None`` if absent."""
    try:
        return _il.import_module(name)
    except Exception:
        return None


# C6: both loaders name their ENGINE path. They load by string, so neither the
# import rewriter nor the C3.4 shim checker can see them — the old bare names
# would have kept resolving through the ca-simulation shims right up to the
# moment C9 deletes those shims, and then failed silently into `None` (the
# `except` branch), which is the worst possible failure mode for a lazy loader.
def ca_curved():
    """Return the ``ca_curved`` module (dynamical varc stepper) or None."""
    return _lazy("casim.engine.lattice.curved")


def ca_emqg():
    """Return the ``ca_emqg`` module or None."""
    return _lazy("casim.engine.interactions.gravity_emqg")


__all__ = [
    "ca_gravity",
    "C_LAT_BCC", "F106_COEFF_LATTICE", "G_LATTICE",
    "K_canonical", "dielectric_from_phi",
    "T00_dirac_rest", "T00_field_energy", "phi_source",
    "lap_nd", "solve_phi_poisson", "phi_wave_step", "phi_field_energy",
    "lapse_mix_half",
    "poisson_open", "solve_poisson_3d_open", "gaussian_mass_3d",
    "ca_curved", "ca_emqg",
]
