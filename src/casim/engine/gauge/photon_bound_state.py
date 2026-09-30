"""
ca_photon_bs.py  —  The interacting two-body bound-state wavefunction of the
                    paired photon (F169).

This is the explicit two-constituent bound-state solver that F69 / F74 / F168
flagged as the outstanding "interacting wavefunction" build.  It works in the
relative-momentum coordinate of the two Weyl constituents that make up the
photon (one on the + chiral branch, one on the - branch), at fixed total
momentum k.

Construction
------------
Constituent + carries momentum k/2 + p, constituent - carries k/2 - p, so the
total is k and p is the *relative* momentum.  The free two-body dispersion is

    E0(p; k) = w+(k/2 + p) + w-(k/2 - p)              (omega = arccos u, ca_bcc)

and the F69 "paired photon" is the p = 0 member, with energy
Omega_even(k) = w+(k/2) + w-(k/2).  The two constituents are bound by a
single attractive contact in the relative coordinate (the lattice NJL / ladder
contact; cf. F74 for the spin-0 sibling):

    H = E0(p; k)  -  g |c><c|,     |c> = uniform (zero-range) state.

Because the contact is rank-1 the bound state below the continuum bottom
T(k) = min_p E0(p; k) is the exact root of the Koster-Slater secular equation

    1 = g < 1 / (E0(p; k) - Eb) >_BZ ,      Eb < T(k),                    (*)

with wavefunction  psi(p) ∝ 1 / (E0(p; k) - Eb).

The PHOTON is the threshold / marginally-bound state Eb -> T(k) at the
critical coupling g_c(k) = 1 / <1/(E0 - T)>_BZ.  Two facts make it massless and
recover F69:

  * T(0) = w+(0) + w-(0) = 0 exactly (gapless constituents, pure-hop A0 = 0,
    F168/B1), so the threshold photon is massless: its zero binding energy is
    inherited from the gapless constituents, not tuned.
  * the continuum bottom does NOT sit at the symmetric split p = 0 at finite k.
    It sits at the COLLINEAR ENDPOINT p = +-k/2, where one constituent carries
    all of k and the other carries zero.  Since w(0) = arccos(1) = 0, the floor
    is the closed form T(k) = min(w+(k), w-(k))  -- no search required.  The
    symmetric split sits above it by |eps(k)| = |kx ky kz| / (3|k|) + O(k^3)
    (F397).  Only as k -> 0 does T(k) -> Omega_even(k), which is the sense in
    which the interacting threshold state reproduces the F69 photon dispersion
    (and its 1/sqrt(3) light speed).
    [Corrected 2026-09-22; the previous docstring asserted T(k) = Omega_even(k)
    exactly at small k, which is false -- see F169 C3 and F397 R6.]

Only closed-form arccos(u) dispersion + real linear algebra are used; no
np.linalg.eig on chiral matrices, and no scipy (own bisection root finder),
per CLAUDE.md.
"""

import numpy as np
from casim.engine.lattice.bcc import bcc_dispersion as _w
from casim.numerics import fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

ROOT3 = np.sqrt(3.0)


# ----------------------------------------------------------------------
def _grid(L):
    ks = np.arange(L) * 2.0 * np.pi / L          # [0, 2pi)
    return np.meshgrid(ks, ks, ks, indexing="ij")


def relative_dispersion(k, L):
    """Free two-body dispersion E0(p; k) = w+(k/2+p) + w-(k/2-p) on an L^3
    relative-momentum grid.  Returns a flat (L^3,) array."""
    KX, KY, KZ = _grid(L)
    k = np.asarray(k, float)
    wp = _w(k[0] / 2 + KX, k[1] / 2 + KY, k[2] / 2 + KZ, sign="+")
    wm = _w(k[0] / 2 - KX, k[1] / 2 - KY, k[2] / 2 - KZ, sign="-")
    return (wp + wm).ravel()


def omega_even(k):
    """The F69 paired-photon rate Omega_even(k) = w+(k/2) + w-(k/2) (= E0 at p=0)."""
    k = np.asarray(k, float)
    return float(_w(k[0] / 2, k[1] / 2, k[2] / 2, "+")
                 + _w(k[0] / 2, k[1] / 2, k[2] / 2, "-"))


def threshold_closed_form(k):
    """The two-body continuum floor T(k) = min_p E0(p; k), in CLOSED FORM.

    The minimum of E0(p; k) = w+(k/2+p) + w-(k/2-p) is attained at the collinear
    endpoint p = +-k/2, i.e. one constituent carries the whole momentum k and the
    other carries zero.  Because w+-(0) = arccos(1) = 0 identically, the endpoint
    values are exactly w+(k) and w-(k), so

        T(k) = min( w+(k), w-(k) )                                   (exact)

    Verified against a deterministic pattern search from five starts, 2M random
    BZ points and Nelder-Mead from the zero-energy BZ nodes (F397): nothing sits
    below this value, and at 60-digit precision E0(k, k/2) - min_b w^b(k) is
    identically 0.

    Replaces the stochastic `true_threshold` search, which under-converged badly
    at small |k| (it could return no improvement at all over Omega_even) and
    contaminated F169's originally quoted exponent 2.10.  The converged exponent
    is 2.010.
    """
    k = np.asarray(k, float)
    return float(min(_w(k[0], k[1], k[2], "+"), _w(k[0], k[1], k[2], "-")))


def threshold_offset_closed_form(k):
    """Omega_even(k) - T(k) to leading order = |eps(k)| = |kx ky kz| / (3|k|).

    eps is the odd, degree-2-homogeneous chiral term in w+-(q) = c|q| +- eps(q)
    + O(q^3).  It vanishes on the coordinate planes (where the offset drops to
    O(k^3)) and is maximal along the body diagonal.  Derived in F397 R6.
    """
    k = np.asarray(k, float)
    n = float(np.linalg.norm(k))
    if n == 0.0:
        return 0.0
    return abs(k[0] * k[1] * k[2]) / (3.0 * n)


def true_threshold(k, iters=8000, step0=0.2, seed=0, method="closed"):
    """Continuum bottom T(k) = min_p E0(p; k).

    method="closed" (default): the exact closed form, `threshold_closed_form`.
    method="stochastic": the ORIGINAL F169 local stochastic descent around
        p = 0, retained only so the 2026-09-22 correction is reproducible.  It
        is NOT converged at small |k| -- do not use it for physics.

    The symmetric split p = 0 (= Omega_even) is not the minimum at finite k; it
    sits |eps(k)| = |kx ky kz|/(3|k|) above the floor.  See F169 C3, F397 R6.
    """
    k = np.asarray(k, float)
    if method == "closed":
        return threshold_closed_form(k)
    if method != "stochastic":
        raise ValueError("method must be 'closed' or 'stochastic'")
    rng = np.random.default_rng(seed)
    p = np.zeros(3)
    best = omega_even(k)          # E0 at p = 0
    step = step0
    for _ in range(iters):
        cand = p + rng.normal(0, step, 3)
        e = float(_w(*(k / 2 + cand), "+") + _w(*(k / 2 - cand), "-"))
        if e < best:
            best, p = e, cand
        step *= 0.9995
    return best


def critical_coupling(k, L, eps=1e-9, threshold="grid"):
    """g_c(k) = 1 / <1/(E0 - T)>_BZ, the contact strength at which the bound
    state sits exactly at the continuum bottom T(k) (the marginal / threshold
    'photon' coupling).  The integrable 1/(E0-T) singularity at the band
    minimum is excluded (it is integrable in 3D — finite g_c, cf. F74 Watson).

    ``threshold`` selects how T is obtained:

    "grid" (default, UNCHANGED since F169): T = E.min() over the L^3 relative
        grid.  EXACT AT k = 0 ONLY — the true floor is at p = 0, which IS a
        grid point there, and T = 0 exactly, so the k = 0 value (the quoted
        F169 g_c = 2.2596) is unaffected.  AT FINITE k this is a GRID
        ARTIFACT: the true floor sits at the collinear endpoint p = +-k/2
        (see `threshold_closed_form`), generally not a grid point, and the
        discrete argmin lands somewhere between the closed-form floor and
        Omega_even(k), NON-MONOTONICALLY in L — e.g. at |k| = 0.2 along (111)
        the fraction of the offset still missed runs 1.00, 1.00, 1.00, 1.00,
        0.36, 0.25, 0.36 at L = 12, 24, 32, 48, 96, 144, 192.  Kept as the
        default only so F169's own C2/C4-note diagnostic (which measures this
        artifact) is reproducible unchanged; see F169 for that measurement.
    "closed" (F401): T = `threshold_closed_form(k)`, exact at every k.
        Converges cleanly and MONOTONICALLY in L (no commensurability
        artifact, since T no longer depends on which grid point happens to be
        closest to the true floor).  This is the physically meaningful choice
        at finite k — see F401 for the re-derived g_c(k) and its genuine,
        monotonically decreasing dependence on |k| along (111).

    Neither option changes anything at k = 0, where grid and closed-form T
    coincide exactly."""
    E = relative_dispersion(k, L)
    if threshold == "grid":
        T = E.min()
    elif threshold == "closed":
        T = threshold_closed_form(k)
    else:
        raise ValueError("threshold must be 'grid' or 'closed'")
    m = E > T + eps
    return 1.0 / np.mean(1.0 / (E[m] - T)), T


def threshold_wavefunction(k, L, eps=1e-9, threshold="grid"):
    """The marginally-bound (E = T) photon wavefunction psi(p) ∝ 1/(E0 - T),
    normalised.  Returns (psi_flat, T).  Normalizable in 3D (the same Watson
    finiteness that makes g_c finite).

    Carries the same ``threshold`` choice as `critical_coupling` ("grid",
    default, UNCHANGED since F169, exact at k=0 / artifact at finite k;
    "closed", F401, exact and cleanly convergent at every k)."""
    E = relative_dispersion(k, L)
    if threshold == "grid":
        T = E.min()
    elif threshold == "closed":
        T = threshold_closed_form(k)
    else:
        raise ValueError("threshold must be 'grid' or 'closed'")
    m = E > T + eps
    psi = np.zeros_like(E)
    psi[m] = 1.0 / (E[m] - T)
    psi /= np.sqrt(np.sum(psi ** 2))
    return psi, T


# ----------------------------------------------------------------------
def _bisect(f, a, b, tol=1e-13, it=300):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("no sign change")
    for _ in range(it):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm) < tol or 0.5 * (b - a) < tol:
            return m
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b)


def bound_state_secular(k, L, g):
    """Solve (*) for the bound-state energy Eb < T(k) by bisection.  Returns Eb."""
    E = relative_dispersion(k, L)
    T = E.min()
    return _bisect(lambda Eb: 1.0 - g * np.mean(1.0 / (E - Eb)), -8.0, T - 1e-7)


def bound_state_dense(k, L, g):
    """Lowest eigenvalue / eigenvector of H = diag(E0) - g|c><c| by dense
    Hermitian diagonalisation (independent cross-check of the secular root)."""
    E = relative_dispersion(k, L)
    N = E.size
    c = np.ones(N) / np.sqrt(N)
    H = np.diag(E) - g * np.outer(c, c)
    ev, V = np.linalg.eigh(H)
    return float(ev[0]), V[:, 0]


def realspace_rms_radius(psi_flat, L):
    """RMS radius (lattice units) of the relative-coordinate wavefunction
    obtained by FFT of psi(p)."""
    ps = psi_flat.reshape(L, L, L)
    psir = _fft.ifftn(ps)
    prob = np.abs(psir) ** 2
    prob /= prob.sum()
    c = np.fft.fftfreq(L, d=1.0 / L)
    X, Y, Z = np.meshgrid(c, c, c, indexing="ij")
    return float(np.sqrt(np.sum(prob * (X ** 2 + Y ** 2 + Z ** 2))))
