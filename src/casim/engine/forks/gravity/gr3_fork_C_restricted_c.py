"""
Fork C — RESTRICTED-c PROPAGATOR (photon c != matter c)
=========================================================
Finding 14.5(c):  single potential phi, but two coupling exponents — the
photon sector sees the full Paper 6 factor of 2, while the matter sector
sees a *halved* coupling so that clock rates pick up only factor 1.

    c_photon(x) = c_0 / (1 - 2 phi(x) / c_0^2)        (Paper 6, unchanged)
    c_matter(x) = c_0 / (1 -   phi(x) / c_0^2)        (halved exponent)
    tau_rate(x)  = c_matter(x) / c_0  ~  1 + phi/c^2  (factor 1)

Physical interpretation: the lattice's `c(x)` is sector-dependent —
photons (the composite-bilinear E_G/B_G of Paper 1 Eq. 35) couple to
the EMQG vacuum index with coupling 2, while massive fermions couple
with coupling 1.  The two couplings come from different bilinears of
the underlying Weyl pair; no new field is introduced, just two distinct
scaling rules for the same phi.

Predicted outcome:
  GR-1  K       -> 4         (photons see the full 2*phi factor)
  GR-2  ratio   -> 1         (photons see the full 2*phi factor)
  GR-3  ratio_GR -> 1        (matter clocks see only phi/c^2 — FIXED)
  GR-4  Δω      -> SMALLER   (~ 0.5 x baseline, because the matter
                               geodesic now has only half the metric
                               perturbation in BOTH g_00 and g_ii)

The Mercury prediction is the critical *discriminator* against Fork A
and Fork B.  If the lattice records ~0.75% Mercury instead of ~1.5%
baseline, Fork C is the right ansatz; if it records ~1.5%, Forks A/B
are favoured.

Cost of the fix: introduces sector-dependent coupling without a derived
rule.  The closest literature analog is a *scalar-tensor* theory where
the photon and the fermion couple to different conformal factors of the
same metric (Brans-Dicke style).
"""

from __future__ import annotations
import numpy as np


NAME = "fork_C_restricted_c"
DESCRIPTION = "Photon coupling 2; matter coupling 1.  Single phi, sector-specific exponents."


def c_photon(phi: np.ndarray, c_0: float) -> np.ndarray:
    return c_0 / (1.0 - 2.0 * phi / c_0**2)


def c_matter(phi: np.ndarray, c_0: float) -> np.ndarray:
    return c_0 / (1.0 - phi / c_0**2)


def tau_rate(phi: np.ndarray, c_0: float) -> np.ndarray:
    """Matter clocks tick at c_matter / c_0 ~ 1 + phi/c^2 (factor 1)."""
    return (c_0 / (1.0 - phi / c_0**2)) / c_0


def metric(phi: np.ndarray, c_0: float):
    """Matter metric components, halved-coupling.

    At leading order:
        A_C = 1 +   phi/c^2     (vs baseline 1 + 2 phi/c^2)
        B_C = 1 -   phi/c^2     (vs baseline 1 - 2 phi/c^2)
    These are the components the timelike Mercury geodesic uses.  The
    GR formula  Δω = 6 pi GM / (a (1-e^2) c^2)  is calibrated against
    the *full* metric perturbation; with halved couplings the predicted
    advance is halved at leading order.  Mercury (1.5% baseline) should
    show ~ 0.75% in Fork C — that is the falsifier.
    """
    A = 1.0 +       phi / c_0**2
    B = 1.0 -       phi / c_0**2
    return A, B
