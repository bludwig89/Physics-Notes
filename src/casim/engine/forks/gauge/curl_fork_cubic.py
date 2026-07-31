"""
Fork: SIMPLE-CUBIC Weyl QCA geometry  (curl-O(k) investigation)
================================================================
User hypothesis (2026-05-22): the composite-photon curl equation only
closes to O(k) (Finding 2, residual = |k|/√6), and the emergent light
speed is c_lat = 1/√3 instead of 1.  Working *backwards* from "c should
be 1", maybe the lattice should be simple-cubic, not BCC — and maybe the
cubic geometry that gives c=1 also fixes the curl residual.

This fork implements the canonical naive simple-cubic Weyl QCA so the
harness can measure c_lat, dispersion isotropy, the composite-photon
curl-residual scaling, and the fermion-doubler count, head-to-head with
the BCC baseline.

Construction
------------
Naive cubic Weyl Hamiltonian uses the lattice momentum s_i = sin(k_i):

    H(k) = σ · s,    s = (sin k_x, sin k_y, sin k_z)

The one-tick unitary is U(k) = exp(-i H) = u·I - i(σ·n) with

    u(k)  = cos|s|
    n(k)  = s · sin|s| / |s|          (so u² + |n|² = 1, exactly unitary)

Dispersion:

    ω(k) = arccos(u) = |s| = sqrt(sin²k_x + sin²k_y + sin²k_z)

Small-k limit:  ω ≈ |k|  →  c_lat = 1  (isotropic at leading order).

PREDICTED OUTCOMES (to be checked by the harness)
-------------------------------------------------
  c_lat (small-k)      -> 1            (CONFIRMS user's speed intuition)
  dispersion isotropy  -> isotropic at O(k), anisotropic at O(k³)
  fermion doublers     -> 8           (Nielsen-Ninomiya: 2^d zeros at
                                        k_i ∈ {0, π}; the cost of c=1)
  curl residual scaling-> O(k) (PREDICTION: geometry does NOT fix it;
                                 the residual comes from the pointwise
                                 un-smeared bilinear, not the lattice —
                                 only the coefficient should change from
                                 1/√6).  If instead it falls to O(k³),
                                 the hypothesis is vindicated.
"""
import numpy as np

GEOMETRY_NAME = "simple-cubic"
C_LAT = 1.0          # emergent small-k light speed (to be verified)

_S_X = np.array([[0, 1], [1, 0]], dtype=complex)
_S_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_S_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def uvec(kx, ky, kz, sign="+"):
    """Return (u, nx, ny, nz) for the simple-cubic Weyl QCA. u²+|n|²=1.

    `sign` is accepted for interface parity with the BCC fork; the naive
    cubic Weyl has a single helicity family, so sign is ignored.
    """
    sx, sy, sz = np.sin(kx), np.sin(ky), np.sin(kz)
    smag = np.sqrt(sx*sx + sy*sy + sz*sz)
    # sinc = sin|s|/|s|, with the L'Hopital limit 1 at |s|->0
    with np.errstate(invalid="ignore", divide="ignore"):
        sinc = np.where(smag > 1e-15, np.sin(smag) / np.where(smag == 0, 1, smag), 1.0)
    u = np.cos(smag)
    nx, ny, nz = sx * sinc, sy * sinc, sz * sinc
    return u, nx, ny, nz


def dispersion(kx, ky, kz, sign="+"):
    """ω(k) = |s| = sqrt(Σ sin²k_i)."""
    sx, sy, sz = np.sin(kx), np.sin(ky), np.sin(kz)
    return np.sqrt(sx*sx + sy*sy + sz*sz)


def unitary(kx, ky, kz, sign="+"):
    u, nx, ny, nz = uvec(kx, ky, kz)
    U_ff = u - 1j * nz
    U_fg = -1j * (nx - 1j * ny)
    U_gf = -1j * (nx + 1j * ny)
    U_gg = u + 1j * nz
    return U_ff, U_fg, U_gf, U_gg


def eigenmodes(kx, ky, kz, sign="+"):
    """Return (psi_plus, psi_minus, omega): U·psi_± = e^{∓iω} psi_±, ω≥0."""
    U_ff, U_fg, U_gf, U_gg = unitary(kx, ky, kz)
    M = np.array([[U_ff, U_fg], [U_gf, U_gg]], dtype=complex)
    w, v = np.linalg.eig(M)
    phases = -np.angle(w)           # U = e^{-iω} → phase = -ω
    ip = int(np.argmax(phases))
    im = 1 - ip
    return v[:, ip], v[:, im], float(phases[ip])
