"""
Fork A — SEPARATE PHASE-TICK FIELD
===================================
Finding 14.5(a):  keep the Paper 6 c(x) for spatial propagation (so GR-1
deflection and GR-2 Shapiro stay correct), but route gravitational
redshift through a *separate* clock-rate field tau(x) that does not
feed back into the propagator.

    c_photon(x) = c_matter(x) = c_0 / (1 - 2 phi(x) / c_0^2)     [unchanged]
    tau_rate(x)                = 1 + phi(x) / c_0^2              [factor 1, NEW]

Physical interpretation: the lattice has two emergent variables.  c(x)
encodes the spatial propagation rate of the unitary update (governs
light deflection, Shapiro, and the timelike Mercury geodesic just as
in the baseline).  tau(x) is the rate at which the discrete phase
*tick* advances per spatial step — a temporal-only book-keeping field
that decouples from spatial transport.  Pound-Rebka measures
tau_emit / tau_receive, which is now factor 1.

Predicted outcome:
  GR-1  K       -> 4         (unchanged from baseline open-BC: 3.88)
  GR-2  ratio   -> 1         (unchanged from baseline open-BC: 1.0006)
  GR-3  ratio_GR -> 1        (FIXED, this is what the fork is designed to do)
  GR-4  Δω      -> ≈ baseline (matter still feels Paper 6 c(x) in
                               the spatial sector; geodesic identical)

Cost of the fix: introduces a *second* scalar field with no derivation
from a Poisson source.  tau(x) is defined by hand from phi(x); in a
"real" physics theory it would need its own field equation.  The closest
literature analog is a *bimetric* gravity, where the photon metric and
the matter metric are independent.
"""

from __future__ import annotations
import numpy as np


NAME = "fork_A_phase_tick"
DESCRIPTION = "Separate phase-tick field; c(x) unchanged from Paper 6, tau(x) decoupled."


def c_photon(phi: np.ndarray, c_0: float) -> np.ndarray:
    return c_0 / (1.0 - 2.0 * phi / c_0**2)


def c_matter(phi: np.ndarray, c_0: float) -> np.ndarray:
    # Same as baseline: matter follows the c(x) sector.  Only the
    # *clock-tick readout* tau(x) is independent.
    return c_0 / (1.0 - 2.0 * phi / c_0**2)


def tau_rate(phi: np.ndarray, c_0: float) -> np.ndarray:
    """Linear-in-phi clock rate, factor 1 by construction.

    Equivalent to Schwarzschild g_00:  -(c dt_proper)^2 = -(1 + 2phi/c^2)
    (c dt_coord)^2  =>  dt_proper / dt_coord = sqrt(1 + 2phi/c^2)
                                              = 1 + phi/c^2 + O(phi^2).
    """
    return 1.0 + phi / c_0**2


def metric(phi: np.ndarray, c_0: float):
    """Effective metric for the Mercury geodesic test.

    Fork A keeps the spatial metric identical to baseline (matter and
    photons share c(x)), so g_ii = (1 - 2 phi/c^2)^{-1} ~ 1 + 2 phi/c^2.
    The temporal piece is set by tau_rate^2:  g_00 = -(tau_rate)^2.
    Linearising both:
        A = 1 + 2 phi/c^2,    B = 1 - 2 phi/c^2   (same as Schwarzschild)
    so GR-4 prediction is identical to baseline.
    """
    A = 1.0 + 2.0 * phi / c_0**2
    B = 1.0 - 2.0 * phi / c_0**2
    return A, B
