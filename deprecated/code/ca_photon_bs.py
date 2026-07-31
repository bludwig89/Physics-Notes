# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_photon_bs.py
# migrated   : 2026-07-30 - 14:48
# target     : src/casim/engine/gauge/photon_bound_state.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_photon_bs.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed (S1/S2 code-clean already applied at F69/F91)
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
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
  * for small k the continuum bottom sits AT the symmetric split p = 0, so
    T(k) = Omega_even(k) exactly -> the interacting threshold bound state
    reproduces the F69 photon dispersion (and its 1/sqrt(3) light speed).

Only closed-form arccos(u) dispersion + real linear algebra are used; no
np.linalg.eig on chiral matrices, and no scipy (own bisection root finder),
per CLAUDE.md.
"""

import numpy as np
from ca_bcc import bcc_dispersion as _w
import ca_fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

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


def true_threshold(k, iters=8000, step0=0.2, seed=0):
    """Continuum bottom T(k) = min_p E0(p; k) by local stochastic descent around
    the symmetric split p = 0.  (The symmetric split is NOT the exact minimum at
    finite k — its gradient is O(k) — so the true floor sits O(k^2) below
    Omega_even; this returns that floor.)"""
    k = np.asarray(k, float)
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


def critical_coupling(k, L, eps=1e-9):
    """g_c(k) = 1 / <1/(E0 - T)>_BZ, the contact strength at which the bound
    state sits exactly at the continuum bottom T(k) (the marginal / threshold
    'photon' coupling).  The integrable 1/(E0-T) singularity at the band
    minimum is excluded (it is integrable in 3D — finite g_c, cf. F74 Watson)."""
    E = relative_dispersion(k, L)
    T = E.min()
    m = E > T + eps
    return 1.0 / np.mean(1.0 / (E[m] - T)), T


def threshold_wavefunction(k, L, eps=1e-9):
    """The marginally-bound (E = T) photon wavefunction psi(p) ∝ 1/(E0 - T),
    normalised.  Returns (psi_flat, T).  Normalizable in 3D (the same Watson
    finiteness that makes g_c finite)."""
    E = relative_dispersion(k, L)
    T = E.min()
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
