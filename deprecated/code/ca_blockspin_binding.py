# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_blockspin_binding.py
# migrated   : 2026-07-30 - 13:53
# target     : src/casim/engine/lattice/blockspin_binding.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_blockspin_binding.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_blockspin_binding.py — Phase-2: a coarse-grained bound state reproduces the
fine-grained spectrum  (F131)
===============================================================================

`2026-06-11`

Phase 2 of `docs/roadmaps/roadmap-scale-to-real-space.md`: "real space with
nothing in it is pointless; the payoff is atoms."  The block-spin transform R_b
(F130, `ca_blockspin.py`) was shown to preserve the *rule* (c_lat, the dielectric,
the propagator classes, Gauss's law, confinement).  Phase 2 demands the harder
thing — that **R_b commutes with BINDING**: a bound state computed on a coarse
lattice of N super-cells must reproduce the fine-grained spectrum of the
(bN)^d-cell problem, at least in the long-wavelength sector.

Construction
------------
A non-relativistic quantum bound state on the lattice — the long-wavelength limit
of an electromagnetic (F125 hydrogen) or dielectric (F64 gravity well) binding —

    H = -(1/2m) ∇²  +  V(x),      ∇² → the F130 stencil `lap_nd`.

Fine problem: spacing 1, H_fine = -(1/2m) lap + diag(V).  Coarse problem under
R_b: the kinetic Laplacian carries the physical 1/b² (coarse spacing = b) and the
potential is the block-average R_b V (the same coarse-graining used for the
gravity dielectric, F130 §5):

    H_coarse = -(1/2m) lap_coarse / b²  +  diag(R_b V).

Both discretise the SAME continuum H, so their low-lying (smooth, IR) eigenpairs
must agree.

Claims (verified in tests/findings/test_F131_blockspin_bound_state.py)
----------------------------------------------------------------------
B1  Binding survives.  The coarse spectrum stays discrete and bound (E below the
    continuum threshold), with the correct level ORDERING and (harmonic) the
    correct uniform level spacing ω.
B2  RG commutes with binding.  The low eigenvalues match, |E_n^coarse −
    E_n^fine| / |E_n^fine| → 0 as the state becomes more IR (wider well / smaller
    b); the residual is the irrelevant O((k a)²) discretisation operator of F130
    T2 — i.e. it shrinks ~b^{-2}, NOT a binding failure.
B3  Wavefunction reproduction.  The block-averaged fine eigenstate equals the
    coarse eigenstate, normalised overlap |⟨R_b ψ_fine | ψ_coarse⟩| → 1.
B4  Absolute accuracy.  Both fine and coarse energies converge to the analytic
    continuum spectrum (harmonic E_N = ω(N + 3/2)); the coarse run reaches it
    with b^d × fewer cells.

Uses scipy.sparse (sparse Hamiltonian + Lanczos `eigsh`) read-only, exactly as
the audited F110 link Hamiltonian does.  No chiral transforms here (a real,
symmetric Schrödinger operator), so numpy/scipy linear algebra is safe.
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

from ca_blockspin import block_average

__all__ = [
    "harmonic_potential", "coulomb_potential",
    "laplacian_sparse", "solve_bound_states",
    "coarse_grain_spectrum", "harmonic_continuum_levels",
    "wavefunction_overlap",
]


# ----------------------------------------------------------------------
# Potentials (sampled on a periodic L^d grid, in fine-lattice units)
# ----------------------------------------------------------------------
def _coords(L, d=3):
    """Centred integer coordinates [-L/2, L/2) along each axis (meshgrid)."""
    c = np.arange(L) - L // 2
    return np.meshgrid(*([c] * d), indexing="ij")


def harmonic_potential(L, k, d=3):
    """Isotropic harmonic well V = ½ k r², centred, on a periodic L^d grid."""
    g = _coords(L, d)
    r2 = sum(c.astype(np.float64) ** 2 for c in g)
    return 0.5 * k * r2


def coulomb_potential(L, alpha, soft=1.0, d=3):
    """Attractive softened Coulomb well V = −α / √(r² + soft²) (the long-
    wavelength EM/hydrogen binding; soft core avoids the lattice r=0 singularity)."""
    g = _coords(L, d)
    r2 = sum(c.astype(np.float64) ** 2 for c in g)
    return -alpha / np.sqrt(r2 + soft ** 2)


# ----------------------------------------------------------------------
# Sparse lattice Hamiltonian and its bound states
# ----------------------------------------------------------------------
def laplacian_sparse(L, d=3):
    """The F130 `lap_nd` stencil (periodic, unit spacing) as a sparse matrix:
    -2d on the diagonal, +1 to each of the 2d nearest neighbours."""
    N = L ** d
    # build via explicit COO (handles periodic wrap cleanly)
    rows, cols, vals = [], [], []
    rows.append(np.arange(N)); cols.append(np.arange(N))
    vals.append((-2.0 * d) * np.ones(N))
    stride = 1
    for _ax in range(d):
        idx = np.arange(N)
        coord = (idx // stride) % L
        for shift in (+1, -1):
            nc = (coord + shift) % L
            j = idx + (nc - coord) * stride
            rows.append(idx); cols.append(j); vals.append(np.ones(N))
        stride *= L
    return sp.csr_matrix((np.concatenate(vals),
                          (np.concatenate(rows), np.concatenate(cols))),
                         shape=(N, N))


def solve_bound_states(V, mass=1.0, spacing=1.0, n_states=6):
    """Lowest `n_states` eigenpairs of H = -(1/2m) lap/spacing² + diag(V).

    `V` is a (L,)*d real array.  Returns (energies[n_states], psis[N, n_states]),
    psis column-normalised.  Lanczos `eigsh` (which='SA'); the operator is real-
    symmetric so this is safe (no chiral transform)."""
    L = V.shape[0]
    d = V.ndim
    lap = laplacian_sparse(L, d)
    H = (-0.5 / mass / spacing ** 2) * lap + sp.diags(V.reshape(-1))
    N = L ** d
    k = min(n_states, N - 2)
    w, v = eigsh(H.tocsc(), k=k, which="SA")
    order = np.argsort(w)
    return w[order], v[:, order]


def wavefunction_overlap(psi_a, psi_b):
    """Normalised overlap |⟨a|b⟩| / (‖a‖‖b‖) of two real vectors (phase/scale
    invariant)."""
    a = np.asarray(psi_a, dtype=np.float64).reshape(-1)
    b = np.asarray(psi_b, dtype=np.float64).reshape(-1)
    return float(abs(a @ b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ----------------------------------------------------------------------
# The Phase-2 coarse-graining check
# ----------------------------------------------------------------------
def coarse_grain_spectrum(V_fine, b, mass=1.0, n_states=4):
    """Solve the bound-state problem fine and coarse-grained by R_b, and compare.

    Coarse-graining: H_coarse = -(1/2m) lap_coarse/b² + diag(R_b V).  Returns a
    dict with the fine/coarse energies, per-level relative energy error, and the
    block-averaged-fine ↔ coarse ground-state overlap.
    """
    L = V_fine.shape[0]
    d = V_fine.ndim
    assert L % b == 0, f"L={L} not divisible by b={b}"

    E_f, psi_f = solve_bound_states(V_fine, mass=mass, spacing=1.0,
                                    n_states=n_states)
    V_coarse = block_average(V_fine, b)            # R_b applied to the potential
    E_c, psi_c = solve_bound_states(V_coarse, mass=mass, spacing=float(b),
                                    n_states=n_states)

    n = min(len(E_f), len(E_c))
    rel = np.abs(E_c[:n] - E_f[:n]) / np.maximum(np.abs(E_f[:n]), 1e-30)

    # ground-state wavefunction reproduction: block-average the fine ψ0
    psi0_f_grid = psi_f[:, 0].reshape([L] * d)
    psi0_f_blocked = block_average(psi0_f_grid, b)
    psi0_c_grid = psi_c[:, 0].reshape([L // b] * d)
    overlap0 = wavefunction_overlap(psi0_f_blocked, psi0_c_grid)

    return {
        "E_fine": E_f[:n],
        "E_coarse": E_c[:n],
        "rel_err": rel,
        "ground_overlap": overlap0,
        "bound_fine": bool(E_f[0] < (V_fine.max() + V_fine.min()) * 0.5
                           or E_f[0] < 0),
        "n_cells_fine": L ** d,
        "n_cells_coarse": (L // b) ** d,
    }


def harmonic_continuum_levels(k, mass=1.0, n_levels=4, d=3):
    """Analytic continuum spectrum of the isotropic oscillator:
    E_N = ω (N + d/2),  ω = √(k/m),  N = 0,1,2,…  (the binding target for B4)."""
    omega = np.sqrt(k / mass)
    return np.array([omega * (N + d / 2.0) for N in range(n_levels)])
