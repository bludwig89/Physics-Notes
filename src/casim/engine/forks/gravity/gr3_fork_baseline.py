"""
Fork: BASELINE (Paper 6 isotropic-c, current `ca_emqg.py::c_field_from_phi`)
============================================================================
This is *not* a candidate fix — it is the existing v2 ansatz, reproduced
here so the comparison harness has a like-for-like baseline column.

    c_photon(x) = c_matter(x) = c_0 / (1 - 2 phi(x) / c_0^2)
    tau_rate(x)                = c(x) / c_0

Predicted outcome (Finding 14.5):
  GR-1  K  -> 4       (factor-4 deflection)
  GR-2  R  -> 1       (matches GR Shapiro)
  GR-3  R  -> 2       (FAILS: factor of 2 over measured GR)
  GR-4  Δω -> 1.5%    (PASS at the 5% gate, isotropic Schwarzschild)
"""

from __future__ import annotations
import numpy as np


NAME = "baseline_paper6"
DESCRIPTION = "Paper 6 isotropic c(x); identical for photons and matter; tau = c/c_0."


def c_photon(phi: np.ndarray, c_0: float) -> np.ndarray:
    """Effective light speed seen by photons (eikonal ray)."""
    return c_0 / (1.0 - 2.0 * phi / c_0**2)


def c_matter(phi: np.ndarray, c_0: float) -> np.ndarray:
    """Effective light speed seen by matter wave packets."""
    return c_0 / (1.0 - 2.0 * phi / c_0**2)


def tau_rate(phi: np.ndarray, c_0: float) -> np.ndarray:
    """Local proper-time tick rate normalised so tau_rate -> 1 at infinity."""
    return (c_0 / (1.0 - 2.0 * phi / c_0**2)) / c_0


def metric(phi: np.ndarray, c_0: float):
    """Return (-g00, g_ii) used by the GR-4 geodesic.

    For the isotropic-c ansatz both come from the same factor:
        ds^2 = -A(x) c_0^2 dt^2 + B(x) dx^2,   A = B = (1 - 2 phi/c_0^2)^{-2}
    so the photon path obeys c_photon = c_0 sqrt(A/B) = c_0 (unchanged) — but
    *that* would predict factor-2 deflection, not factor-4.  The actual
    Paper 6 eikonal derivation pulls deflection from grad(1/c_photon),
    which gives factor-4 because c_photon itself has the factor of 2.
    For Mercury we use the leading-order 1PN reduction with the
    isotropic-Schwarzschild assignment A = 1 + 2phi/c^2, B = 1 - 2phi/c^2.
    """
    A = 1.0 + 2.0 * phi / c_0**2
    B = 1.0 - 2.0 * phi / c_0**2
    return A, B
