"""casim.engine.core.blockspin — the block-spin RG as a first-class engine operation
(Phase 4)
================================================================================

Phase 4 of `docs/roadmaps/roadmap-scale-to-real-space.md`: "implement R_b as a
first-class engine operation so a run can declare a physical patch size and a
block factor."  This wires the F130–F132 block-spin transform R_b into the CASIM
engine so a tractable lattice of N super-cells faithfully represents a patch of
(b·N)^d physical cells.

Two capabilities
----------------
1.  **Declare a physical patch + block factor.**  `LatticeSpec.block` records how
    many physical cells per axis each super-cell stands for; the engine then
    knows the physical patch is `physical_L = L·block` and each super-cell is
    `cell_factor = block^dims` physical cells.  The light speed c_lat is an RG
    fixed point (F130 T1), so it is carried through unchanged.

2.  **Coarse-grain a live run (R_b).**  `Simulation.block_spin(b)` applies R_b to
    every channel state in place, shrinks the lattice L → L/b and accumulates the
    block factor — an adaptive-resolution / multigrid CA step.  The coarse field
    is then propagated by the **renormalised** rule Ω_coarse(κ) = Ω(κ/b)
    (`renormalized_even_step`), which keeps the physical dynamics faithful (F130
    T1/T2).

The per-channel coarse-graining dispatches on the F91 propagator class / state
layout, reusing the audited transforms:
  * even / chiral / dielectric **field** channels (E,B) — block-average each
    polarisation component (the F130 §T3c even-field rule);
  * **spinor** channels (f,g) — complex-safe block-average (NOT the float-casting
    `ca_blockspin.block_average`, which would drop the imaginary part — CLAUDE.md
    caveat);
  * **gravity** dielectric (φ,K) — block-average the LINEAR potential φ (K =
    exp(−2φ/c²) is rebuilt), the F130 §T3b log-correct rule that preserves the
    reciprocal lock A·B ≡ 1.
"""
from __future__ import annotations

from typing import Any, Dict
import numpy as np
from casim.constants import c_lat

ROOT3 = float(np.sqrt(3.0))


# ----------------------------------------------------------------------
# Complex-safe Kadanoff block average (preserves dtype; handles a leading
# component axis).  R_b on a (… , L, L, L) array over its trailing 3 axes.
# ----------------------------------------------------------------------
def block_average_field(arr: np.ndarray, b: int) -> np.ndarray:
    """Average b³ fine cells into one coarse cell over the trailing 3 spatial
    axes.  Preserves dtype (real OR complex), so spinor channels keep their
    imaginary part exactly."""
    a = np.asarray(arr)
    if b == 1:
        return a.copy()
    L = a.shape[-1]
    assert a.shape[-3:] == (L, L, L), f"expected cubic spatial axes, got {a.shape}"
    assert L % b == 0, f"L={L} not divisible by block factor b={b}"
    Lc = L // b
    lead = a.shape[:-3]
    a = a.reshape(lead + (Lc, b, Lc, b, Lc, b))
    return a.mean(axis=(-5, -3, -1))


# ----------------------------------------------------------------------
# Per-channel R_b: coarse-grain one channel state dict by its layout.
# ----------------------------------------------------------------------
def block_state(state: Dict[str, Any], b: int,
                propagator: str = "even") -> Dict[str, Any]:
    """Return a coarse-grained copy of ``state`` under R_b (block factor b).

    Dispatches on the state layout (the same layouts `Channel.density_field`
    knows): (E,B) fields, (f,g) spinors, or the gravity (φ,K) dielectric.
    Scalars and metadata pass through unchanged.
    """
    if b == 1:
        return dict(state)
    out: Dict[str, Any] = {}

    is_gravity = "phi" in state and "K" in state

    for key, val in state.items():
        if not isinstance(val, np.ndarray):
            out[key] = val
            continue
        if is_gravity and key == "K":
            continue                       # rebuilt from the averaged φ below
        if val.ndim >= 3 and val.shape[-3:] == (val.shape[-1],) * 3:
            out[key] = block_average_field(val, b)
        else:
            out[key] = val.copy()          # non-spatial array — leave as is

    if is_gravity:
        c = float(state.get("c", c_lat))
        # φ is the LINEAR Poisson potential → block-average is exact; rebuild K
        # (= exp(−2φ/c²)) so the reciprocal lock A·B ≡ 1 is preserved (F130 T3b).
        out["K"] = np.exp(-2.0 * out["phi"] / (c ** 2))
    return out


# ----------------------------------------------------------------------
# The renormalised even-law propagator: Ω_coarse(κ) = Ω(κ/b)  (F130 T1/T2).
# Lets a coarse (block=b) lattice carry the physically-faithful dynamics.
# ----------------------------------------------------------------------
def renormalized_even_step(E: np.ndarray, B: np.ndarray, block: int):
    """One even-law (E,B) tick on a coarse lattice of block factor ``block``,
    using the renormalised rule Ω_coarse(κ) = Ω(κ/block).

    At block=1 this reduces bit-for-bit to the fine even step
    (`ca_photon_pair.photon_step_spectral`).  At block=b it rotates each mode by
    Ω(κ/b) — the F130 coarse rule that keeps the physical speed (T1) and makes
    the lattice-artifact corrections irrelevant (T2).
    """
    from casim.numerics import fft as _fft  # C1.3: the seam
    from casim.engine.lattice.geometry import make_kgrid_3d
    from casim.engine.gauge.weak_wmu import _f26_rotation_step

    shape = E.shape[-3:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    inv = 1.0 / float(block)
    Ek = _fft.fftn(E, axes=(-3, -2, -1))
    Bk = _fft.fftn(B, axes=(-3, -2, -1))
    Ek2, Bk2 = _f26_rotation_step(Ek, Bk, KX * inv, KY * inv, KZ * inv)
    E_new = _fft.ifftn(Ek2, axes=(-3, -2, -1)).real
    B_new = _fft.ifftn(Bk2, axes=(-3, -2, -1)).real
    return E_new, B_new


def _renormalized_chiral_dispersions(shape, block):
    """(Ω⁺, Ω⁻) at the renormalised momenta κ/block, with the coarse-grid
    Nyquist correction (self-conjugate bins → even average) that keeps the real
    field unitary — the F134 chiral analogue of `ca_wmu._chiral_dispersions`."""
    from casim.engine.lattice.geometry import make_kgrid_3d
    from casim.engine.lattice.bcc import bcc_dispersion

    KX, KY, KZ = make_kgrid_3d(*shape)
    inv = 1.0 / float(block)
    op = 2.0 * bcc_dispersion(KX * inv / 2.0, KY * inv / 2.0, KZ * inv / 2.0, sign='+')
    om = 2.0 * bcc_dispersion(KX * inv / 2.0, KY * inv / 2.0, KZ * inv / 2.0, sign='-')
    nyq = np.zeros(shape, dtype=bool)
    for axis, L in enumerate(shape):
        if L % 2 == 0:
            idx = [slice(None)] * 3
            idx[axis] = L // 2
            nyq[tuple(idx)] = True
    if nyq.any():
        even = op + om
        op = np.where(nyq, 0.5 * even, op)
        om = np.where(nyq, 0.5 * even, om)
    return op, om


def renormalized_chiral_step(E, B, block):
    """One CHIRAL (W±, F37) tick on a coarse lattice of block factor ``block``,
    using the renormalised branch rates Ω±(κ/block).

    Reduces bit-for-bit to `ca_wmu.w_propagation_step_chiral` at block=1.  The
    F± Riemann–Silberstein eigenstates ride their own branch (F91 chiral, forced),
    each rescaled by 1/block so the coarse run keeps the physical dispersion.
    """
    from casim.numerics import fft as _fft  # C1.3: the seam

    shape = E.shape[-3:]
    Op, Om = _renormalized_chiral_dispersions(shape, block)
    Ek = _fft.fftn(E, axes=(-3, -2, -1))
    Bk = _fft.fftn(B, axes=(-3, -2, -1))
    Fp = Ek + 1j * Bk
    Fm = Ek - 1j * Bk
    Fp_new = np.exp(-1j * Op) * Fp
    Fm_new = np.exp(+1j * Om) * Fm
    E_new = _fft.ifftn((Fp_new + Fm_new) * 0.5, axes=(-3, -2, -1)).real
    B_new = _fft.ifftn((Fp_new - Fm_new) * (-0.5j), axes=(-3, -2, -1)).real
    return E_new, B_new


def renormalized_weyl_step(f, g, block, sign='+'):
    """One PER-BRANCH BCC Weyl tick on a coarse lattice of block factor
    ``block``, using the renormalised 2×2 unitary U^±(κ/block).

    Reduces bit-for-bit to `ca_bcc.weyl_step_3d_bcc` at block=1.  Diagonal in
    Fourier space; the closed-form `bcc_unitary` (u·I − i n·σ, no np.linalg.eig)
    is evaluated at κ/block so the spinor walk stays physically faithful.
    """
    from casim.numerics import fft as _fft  # C1.3: the seam
    from casim.engine.lattice.geometry import make_kgrid_3d
    from casim.engine.lattice.bcc import bcc_unitary

    shape = f.shape[-3:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    inv = 1.0 / float(block)
    U_ff, U_fg, U_gf, U_gg = bcc_unitary(KX * inv, KY * inv, KZ * inv, sign=sign)
    F = _fft.fftn(f)
    G = _fft.fftn(g)
    F_new = U_ff * F + U_fg * G
    G_new = U_gf * F + U_gg * G
    return _fft.ifftn(F_new), _fft.ifftn(G_new)


# ----------------------------------------------------------------------
# Physical-patch bookkeeping helpers.
# ----------------------------------------------------------------------
def physical_L(lattice) -> int:
    """Physical cells per axis the lattice represents: L · block."""
    return int(lattice.L) * int(getattr(lattice, "block", 1))


def cell_factor(lattice) -> int:
    """Physical cells per super-cell: block^dims."""
    return int(getattr(lattice, "block", 1)) ** int(getattr(lattice, "dims", 3))


def patch_summary(lattice) -> Dict[str, Any]:
    """Compact description of the physical patch a (possibly coarse) lattice
    stands for — recorded in run results so a run 'declares' its patch."""
    b = int(getattr(lattice, "block", 1))
    return {
        "L_supercells": int(lattice.L),
        "block": b,
        "physical_L": physical_L(lattice),
        "cells_per_supercell": cell_factor(lattice),
        "physical_cells_total": physical_L(lattice) ** int(lattice.dims),
        "c_lat": float(getattr(lattice, "c_lat", c_lat)),         # RG-fixed (T1)
    }
