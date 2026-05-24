"""
Fork B — ANISOTROPIC METRIC (g_00 and g_ii independent)
========================================================
Finding 14.5(b):  abandon the isotropic single-c ansatz and introduce
an explicit anisotropic metric  (g_00(x), g_ii(x)).

Use the textbook isotropic-Schwarzschild assignment at leading order:

    g_00(x) = -(1 + 2 phi(x) / c_0^2)        =>  A = 1 + 2 phi/c^2
    g_ii(x) =  (1 - 2 phi(x) / c_0^2)        =>  B = 1 - 2 phi/c^2

From these:
    c_photon(x) = c_0 * sqrt(|g_00|/g_ii) = c_0 * sqrt(A/B)
                ~ c_0 * (1 + 2 phi/c_0^2 + 2 phi^2/c_0^4 + ...)         (factor 2)
    tau_rate(x) = sqrt(|g_00|)            ~  1 +  phi/c_0^2             (factor 1)

The factor-4 deflection comes from the *difference* between A and B in
the eikonal integrand; the factor-1 redshift comes from A alone.

Predicted outcome (textbook GR):
  GR-1  K       -> 4         (Einstein, recovered)
  GR-2  ratio   -> 1         (recovered)
  GR-3  ratio_GR -> 1        (FIXED)
  GR-4  Δω      -> matches GR Schwarzschild (1.5% baseline; same since
                               isotropic-Schwarzschild already used the
                               (A, B) split — Fork B just exposes the two
                               separately throughout the stack)

Cost of the fix: introduces a per-cell two-component metric instead of
a single c(x).  No new sources are added — both A and B are sourced by
the same phi.  This is the most physically defensible fork; effectively
it makes the lattice reproduce GR in isotropic coordinates by
construction.  Loses the "single emergent variable" parsimony of v2.
"""

from __future__ import annotations
import numpy as np


NAME = "fork_B_anisotropic"
DESCRIPTION = "Anisotropic metric A=1+2phi/c^2, B=1-2phi/c^2 (isotropic-Schwarzschild)."


def _AB(phi: np.ndarray, c_0: float):
    A = 1.0 + 2.0 * phi / c_0**2
    B = 1.0 - 2.0 * phi / c_0**2
    return A, B


def c_photon(phi: np.ndarray, c_0: float) -> np.ndarray:
    """c_photon = c_0 * sqrt(A/B).

    At leading order: c_0 * (1 + 2 phi/c^2), reproducing the Paper 6
    factor-2 form by accident from the (A,B) combination — this is how
    we keep the GR-1/GR-2 results unchanged.
    """
    A, B = _AB(phi, c_0)
    return c_0 * np.sqrt(np.abs(A) / B)


def c_matter(phi: np.ndarray, c_0: float) -> np.ndarray:
    """Matter follows the same metric — c_matter equals c_photon at this
    order; the difference between photons and matter shows up in the
    timelike geodesic equation, not in the scalar c."""
    A, B = _AB(phi, c_0)
    return c_0 * np.sqrt(np.abs(A) / B)


def tau_rate(phi: np.ndarray, c_0: float) -> np.ndarray:
    """Local clock rate = sqrt(|g_00|) = sqrt(A).

    Leading-order:  tau_rate ~ 1 + phi/c^2  (factor 1, matches GR).
    """
    A, _ = _AB(phi, c_0)
    return np.sqrt(np.abs(A))


def metric(phi: np.ndarray, c_0: float):
    """Return (A, B) directly — by construction this is the isotropic-
    Schwarzschild metric.  GR-4 should match the baseline result at the
    same precision (the Mercury test already used these A,B in its 1PN
    EOM)."""
    return _AB(phi, c_0)
