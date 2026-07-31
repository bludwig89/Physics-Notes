"""
Fork E — TENSOR-METRIC GRAVITY (the structurally-honest path beyond Paper 6)
============================================================================
Finding 19.  Paper 6's EMQG carries gravity in a *single scalar* — the
vacuum potential phi feeding a refractive index c(x) = c_0/(1 - 2 phi/c_0^2).
That scalar cannot independently set g_00 and g_ii, which is the root cause
of the GR-3 factor-2 redshift (Finding 14.5) and is why Forks A/B/C had to
*patch* the clock/propagator split by hand.

Fork E removes the patch by carrying the metric itself.  For a static,
spherically-symmetric source the linearised Einstein equations in harmonic
(Lorenz) gauge,

        box  hbar_{mu nu}  =  -16 pi G / c^4  T_{mu nu},                (1)

with dust  T_00 = rho c^2  (all other components negligible at 1PN),
reduce to a single Poisson solve for the trace-reversed  hbar_00, after
which the *trace reversal* hands back two independent metric pieces:

        hbar_00 = -4 phi / c^2 ,   all other hbar_{mu nu} = 0
        =>  h_00 = -2 phi / c^2 ,   h_ij = -2 phi / c^2 delta_ij
        =>  g_00 = -(1 + 2 phi/c^2) ,   g_ij = (1 - 2 phi/c^2) delta_ij    (2)

This is *exactly* Fork B's (A, B) assignment — but now it is a DERIVED
consequence of solving the spin-2 field equation, not a hand-written
ansatz.  The value of writing it this way is that it generalises in three
directions that the single scalar cannot:

  * E1 (10-component solve).  Source the full T_{mu nu}: momentum density
    T_0i -> gravitomagnetic hbar_0i -> frame dragging (GR-5); stress T_ij
    -> the spatial metric's anisotropy.  The single scalar has no slot for
    either.

  * E2 (exact metric).  Replace the *linearised* (A, B) of Eq. (2) with the
    closed-form isotropic-Schwarzschild metric, removing the 1PN truncation
    that caps GR-4 Mercury at 1.5% and the deflection coefficient at
    K = 4(1 + O(GM/rc^2)).  This is the "algebraic-exactness" rung the
    project prizes: a closed form, exact to all PN orders for one static
    source, with the only residual being the discrete Laplacian/gradient.

  * E3 (tetrad Dirac).  Couple matter through a vierbein e^a_mu and spin
    connection (the curved-space Dirac equation) so fermions move on true
    geodesics of g_{mu nu}.  Then the factor-1 redshift falls out of
    sqrt(-g_00) automatically and GR-3 needs no separate phase-tick field.

This module supplies the *metric* half (E2, with E1's derivation made
explicit in the docstring).  E3 is a propagator change tracked separately.

----------------------------------------------------------------------------
Interface (matches ca-simulation/forks/gr3_fork_*.py so it drops straight
into gr3_fork_harness.py):

    c_photon(phi, c_0)   c_matter(phi, c_0)   tau_rate(phi, c_0)
    metric(phi, c_0) -> (A, B)   where  g_00 = -A,  g_ii = B

Two modes, selected by make_fork(mode) or the module-level default:

    mode = "linearized"      -> Eq. (2); identical to Fork B (sanity anchor)
    mode = "exact_isotropic" -> closed-form isotropic-Schwarzschild (E2)

Convention for converting the harness's potential to a metric: for a single
spherical source the Newtonian potential encodes the radius via
        u(x) := -phi(x) / c_0^2  =  GM / (r c_0^2)   >= 0  in a well.
The exact isotropic-Schwarzschild metric is then

        A_exact = ((1 - u/2) / (1 + u/2))^2          (g_00 = -A)
        B_exact = (1 + u/2)^4                         (g_ii = B)

whose small-u expansion is A -> 1 - 2u = 1 + 2 phi/c^2 and
B -> 1 + 2u = 1 - 2 phi/c^2, recovering Eq. (2) exactly.  Outside the
isotropic horizon u < 2; we clip at u = 2(1 - 1e-9) so the stepper never
divides by zero (the test probes the run-up to the horizon, not the
singularity).
"""

from __future__ import annotations
from types import SimpleNamespace
import numpy as np

# Hard ceiling just inside the isotropic-coordinate horizon r = GM/2c^2 (u=2).
_U_MAX = 2.0 * (1.0 - 1.0e-9)


def _u_of_phi(phi: np.ndarray, c_0: float) -> np.ndarray:
    """u = GM/(r c^2) = -phi/c^2, clipped to stay outside the horizon."""
    u = -np.asarray(phi, dtype=np.float64) / c_0**2
    return np.clip(u, -np.inf, _U_MAX)


# ───────────────────────────────────────────────────────────────────
#  Linearised tensor metric  (Eq. 2)  ==  Fork B, but derived from (1)
# ───────────────────────────────────────────────────────────────────

def _AB_linearized(phi: np.ndarray, c_0: float):
    u = _u_of_phi(phi, c_0)
    A = 1.0 - 2.0 * u          # = 1 + 2 phi/c^2
    B = 1.0 + 2.0 * u          # = 1 - 2 phi/c^2
    return A, B


# ───────────────────────────────────────────────────────────────────
#  Exact isotropic-Schwarzschild metric  (E2)
# ───────────────────────────────────────────────────────────────────

def _AB_exact(phi: np.ndarray, c_0: float):
    u = _u_of_phi(phi, c_0)
    half = 0.5 * u
    A = ((1.0 - half) / (1.0 + half))**2
    B = (1.0 + half)**4
    return A, B


_MODES = {
    "linearized": _AB_linearized,
    "exact_isotropic": _AB_exact,
}


def make_fork(mode: str = "exact_isotropic") -> SimpleNamespace:
    """Return a fork object exposing the harness interface for `mode`."""
    if mode not in _MODES:
        raise ValueError(f"mode must be one of {list(_MODES)}; got {mode!r}")
    AB = _MODES[mode]

    def metric(phi, c_0):
        return AB(phi, c_0)

    def c_photon(phi, c_0):
        A, B = AB(phi, c_0)
        return c_0 * np.sqrt(np.abs(A) / B)

    def c_matter(phi, c_0):
        # Same scalar as the photon; the photon/matter difference lives in
        # the timelike geodesic equation (see gr_tensor_stub.geodesic_*),
        # not in a scalar wave speed.
        A, B = AB(phi, c_0)
        return c_0 * np.sqrt(np.abs(A) / B)

    def tau_rate(phi, c_0):
        A, _ = AB(phi, c_0)
        return np.sqrt(np.abs(A))

    name = f"fork_E_tensor_{mode}"
    desc = ("Linearised tensor metric (==Fork B, derived from box hbar=−16πGT)"
            if mode == "linearized"
            else "Exact isotropic-Schwarzschild metric A,B (all PN orders, one source)")
    return SimpleNamespace(
        NAME=name, DESCRIPTION=desc,
        metric=metric, c_photon=c_photon,
        c_matter=c_matter, tau_rate=tau_rate, mode=mode,
    )


# Module-level default so this file can also be dropped into the harness'
# FORKS list directly (exact mode).
_default = make_fork("exact_isotropic")
NAME = _default.NAME
DESCRIPTION = _default.DESCRIPTION
metric = _default.metric
c_photon = _default.c_photon
c_matter = _default.c_matter
tau_rate = _default.tau_rate
