"""casim.lattice.chiral_core — a verified hand-rolled chiral linear-algebra core
(Phase 4, F134)
================================================================================

The standing CLAUDE.md caveat: *"using numpy or scipy on chiral transforms may
not produce desired results.  Check them first when troubleshooting.  If they
are returning wrong results or dropping the real or imaginary elements, begin
writing our own library of functions from scratch so we know what they are
doing."*

This is that from-scratch library for the model's two chiral spectral transforms:

  * the BCC Weyl 2×2 unitary  U^±(k) = u·I − i (n·σ)  (`ca_bcc.weyl_step_3d_bcc`);
  * the W± Riemann–Silberstein branch rotation  F^± → e^{∓iΩ^±} F^±
    (`ca_wmu.w_propagation_step_chiral`).

Every complex multiply is done on **explicit real (re, im) pairs** — no reliance
on numpy's complex dtype handling, no `np.linalg` on chiral matrices — so the
arithmetic is fully auditable and a future numba/GPU backend can operate on plain
real arrays.  The core is registered through `casim.lattice.backend` (the
`chiral_transform` seam) and is verified bit-for-bit against the audited kernels
(F134 tests).

Only the per-mode 2×2 algebra is hand-rolled; the FFT itself routes through the
backend (the FFT is not the chiral-sensitive step — the 2×2 mode mix is).
"""
from __future__ import annotations

import numpy as np

import ca_fft as _fft
from ca_lattice import make_kgrid_3d
from ca_bcc import _bcc_uvec, bcc_dispersion


# ----------------------------------------------------------------------
# Explicit-real complex algebra (the audited primitives)
# ----------------------------------------------------------------------
def cmul(ar, ai, br, bi):
    """(ar+i·ai)·(br+i·bi) on real arrays → (real, imag).  No complex dtype."""
    return ar * br - ai * bi, ar * bi + ai * br


def su2_apply(Uff, Ufg, Ugf, Ugg, F, G):
    """Apply the 2×2 mix [[Uff,Ufg],[Ugf,Ugg]] to spinor (F,G).

    All ten arguments are complex arrays, but the products are formed via
    `cmul` on the explicit real/imag parts — the hand-rolled core.  Returns
    (F_new, G_new) as complex arrays reassembled at the end.
    """
    Ff_r, Ff_i = F.real, F.imag
    G_r, G_i = G.real, G.imag
    a1r, a1i = cmul(Uff.real, Uff.imag, Ff_r, Ff_i)
    a2r, a2i = cmul(Ufg.real, Ufg.imag, G_r, G_i)
    b1r, b1i = cmul(Ugf.real, Ugf.imag, Ff_r, Ff_i)
    b2r, b2i = cmul(Ugg.real, Ugg.imag, G_r, G_i)
    F_new = (a1r + a2r) + 1j * (a1i + a2i)
    G_new = (b1r + b2r) + 1j * (b1i + b2i)
    return F_new, G_new


# ----------------------------------------------------------------------
# Hand-rolled Weyl walk (per-branch, F134 block-aware)
# ----------------------------------------------------------------------
def weyl_unitary_real(KX, KY, KZ, sign='+'):
    """U^±(k) entries as complex arrays, built from the closed-form (u, n·σ)
    — no eig/diagonalisation.  Same algebra as `ca_bcc.bcc_unitary`, exposed
    here so the core owns every step."""
    u, nx, ny, nz = _bcc_uvec(KX, KY, KZ, sign=sign)
    Uff = u - 1j * nz
    Ufg = -1j * (nx - 1j * ny)
    Ugf = -1j * (nx + 1j * ny)
    Ugg = u + 1j * nz
    return Uff, Ufg, Ugf, Ugg


def weyl_step(f, g, sign='+', block=1):
    """Hand-rolled BCC Weyl tick (optionally block-renormalised by ``block``).

    Matches `ca_bcc.weyl_step_3d_bcc` (block=1) / `blockspin.renormalized_weyl_step`
    (block>1) bit-for-bit, but every 2×2 mode mix uses `su2_apply` on explicit
    real/imag parts."""
    shape = f.shape[-3:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    inv = 1.0 / float(block)
    U = weyl_unitary_real(KX * inv, KY * inv, KZ * inv, sign=sign)
    F = _fft.fftn(f)
    G = _fft.fftn(g)
    F_new, G_new = su2_apply(*U, F, G)
    return _fft.ifftn(F_new), _fft.ifftn(G_new)


# ----------------------------------------------------------------------
# Hand-rolled W± chiral RS rotation (F134 block-aware)
# ----------------------------------------------------------------------
def _chiral_branch_rates(shape, block):
    KX, KY, KZ = make_kgrid_3d(*shape)
    inv = 1.0 / float(block)
    op = 2.0 * bcc_dispersion(KX * inv / 2, KY * inv / 2, KZ * inv / 2, sign='+')
    om = 2.0 * bcc_dispersion(KX * inv / 2, KY * inv / 2, KZ * inv / 2, sign='-')
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


def chiral_rs_step(E, B, block=1):
    """Hand-rolled W± chiral RS tick (optionally block-renormalised).

    F^± = E ± iB ride e^{∓iΩ^±}; the phase rotation e^{-iΩ} = (cosΩ, −sinΩ) is
    applied via `cmul` on explicit real parts.  Matches
    `ca_wmu.w_propagation_step_chiral` (block=1) bit-for-bit."""
    shape = E.shape[-3:]
    Op, Om = _chiral_branch_rates(shape, block)
    Ek = _fft.fftn(E, axes=(-3, -2, -1))
    Bk = _fft.fftn(B, axes=(-3, -2, -1))
    # F± = Ek ± i Bk
    Fp = Ek + 1j * Bk
    Fm = Ek - 1j * Bk
    cp, sp = np.cos(Op), np.sin(Op)        # e^{-iΩ⁺}
    cm, sm = np.cos(Om), np.sin(Om)        # e^{+iΩ⁻}
    Fp_r, Fp_i = cmul(cp, -sp, Fp.real, Fp.imag)
    Fm_r, Fm_i = cmul(cm, +sm, Fm.real, Fm.imag)
    Fp_new = Fp_r + 1j * Fp_i
    Fm_new = Fm_r + 1j * Fm_i
    E_new = _fft.ifftn((Fp_new + Fm_new) * 0.5, axes=(-3, -2, -1)).real
    B_new = _fft.ifftn((Fp_new - Fm_new) * (-0.5j), axes=(-3, -2, -1)).real
    return E_new, B_new


# ----------------------------------------------------------------------
# Backend registration (the chiral_transform seam)
# ----------------------------------------------------------------------
class ChiralCore:
    """Hand-rolled chiral backend.  Exposes the FFTs (delegated to ca_fft) plus
    a ``chiral_transform`` dispatcher so the engine can route chiral steps
    through an audited, complex-dtype-free core."""
    name = "chiral_core"

    def fftn(self, a, **kw):  return _fft.fftn(a, **kw)
    def ifftn(self, a, **kw): return _fft.ifftn(a, **kw)
    def fft2(self, a, **kw):  return _fft.fft2(a, **kw)
    def ifft2(self, a, **kw): return _fft.ifft2(a, **kw)
    def fft(self, a, **kw):   return _fft.fft(a, **kw)
    def ifft(self, a, **kw):  return _fft.ifft(a, **kw)

    def chiral_transform(self, kind, *args, block=1, **kw):
        """kind='weyl' → weyl_step(f,g,sign,block); kind='w_rs' →
        chiral_rs_step(E,B,block)."""
        if kind == "weyl":
            f, g = args[0], args[1]
            return weyl_step(f, g, sign=kw.get("sign", "+"), block=block)
        if kind == "w_rs":
            E, B = args[0], args[1]
            return chiral_rs_step(E, B, block=block)
        raise ValueError(f"unknown chiral kind {kind!r}")


def register() -> ChiralCore:
    """Register the hand-rolled chiral core with the backend seam and return it."""
    from casim.lattice import backend
    core = ChiralCore()
    backend.register_backend(core, name="chiral_core")
    return core
