#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F134_phase4_completion.py
==============================

F134 — completing Phase 4 of roadmap-scale-to-real-space.md beyond the F133
even-law engine op:

  A  block-aware renormalised steps for the CHIRAL (W±) and PER-BRANCH (Weyl)
     classes reduce bit-for-bit to the fine kernels at b=1;
  B  [R_b, evolution] = 0 on band-limited fields for chiral + Weyl (the coarse
     run reproduces the fine IR dynamics for every propagator class);
  C  the coarse chiral/Weyl steps stay unitary (norm conserved);
  D  a verified hand-rolled chiral linear-algebra core (explicit real/imag
     arithmetic, no np.linalg on chiral matrices — CLAUDE.md) matches the
     audited kernels bit-for-bit;
  E  the backend seam works: the chiral core registers + dispatches, and a
     second FFT backend (numpy_fft) is identical to ca_fft to round-off (the
     regression a future GPU backend must pass);
  F  the FFT round-off floor stays ~1 ulp/step as L grows (no degradation);
  G  the W-chiral and Weyl-BCC engine channels run faithfully with block > 1.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

import casim.engine.core.blockspin as bsm                      # noqa: E402
import casim.lattice.chiral_core as cc                    # noqa: E402
from casim.lattice import backend                          # noqa: E402
from casim.engine.lattice.bcc import weyl_step_3d_bcc                         # noqa: E402
from casim.engine.gauge.weak_wmu import w_propagation_step_chiral               # noqa: E402


def _bandlimited_real(L, nc=3, seed=0):
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    k = 2 * np.pi / L
    f = np.zeros((nc, L, L, L))
    for c in range(nc):
        f[c] = np.cos(k * X + 0.2 * c) + 0.5 * np.cos(k * Y) + 0.3 * np.cos(2 * k * Z + c)
    return f


def _bandlimited_complex(L):
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    k = 2 * np.pi / L
    return (np.cos(k * X) + 0.5j * np.cos(k * Y) + 0.3 * np.cos(2 * k * Z)).astype(np.complex128)


# ════════════════════════════════════════════════════════════════════
#  A — block-aware steps reduce to the fine kernels at b=1
# ════════════════════════════════════════════════════════════════════
def test_A_chiral_reduces_at_block1():
    rng = np.random.default_rng(0)
    E = rng.standard_normal((3, 12, 12, 12))
    B = rng.standard_normal((3, 12, 12, 12))
    e1, b1 = bsm.renormalized_chiral_step(E, B, 1)
    e2, b2 = w_propagation_step_chiral(E, B)
    assert np.allclose(e1, e2, atol=1e-13) and np.allclose(b1, b2, atol=1e-13)


def test_A_weyl_reduces_at_block1():
    rng = np.random.default_rng(0)
    f = rng.standard_normal((12, 12, 12)) + 1j * rng.standard_normal((12, 12, 12))
    g = rng.standard_normal((12, 12, 12)) + 1j * rng.standard_normal((12, 12, 12))
    f1, g1 = bsm.renormalized_weyl_step(f, g, 1, "+")
    f2, g2 = weyl_step_3d_bcc(f, g, "+")
    assert np.allclose(f1, f2, atol=1e-13) and np.allclose(g1, g2, atol=1e-13)


# ════════════════════════════════════════════════════════════════════
#  B — [R_b, evolution] = 0 (chiral + Weyl)
# ════════════════════════════════════════════════════════════════════
def test_B_chiral_commutes_with_evolution():
    L, b, n = 16, 2, 8
    E, B = _bandlimited_real(L), 0.4 * _bandlimited_real(L)
    EA, BA = E.copy(), B.copy()
    for _ in range(n):
        EA, BA = w_propagation_step_chiral(EA, BA)
    EA = bsm.block_average_field(EA, b); BA = bsm.block_average_field(BA, b)
    EB = bsm.block_average_field(E, b); BB = bsm.block_average_field(B, b)
    for _ in range(n):
        EB, BB = bsm.renormalized_chiral_step(EB, BB, b)
    assert max(np.max(np.abs(EA - EB)), np.max(np.abs(BA - BB))) < 1e-11


def test_B_weyl_commutes_with_evolution():
    L, b, n = 16, 2, 8
    f, g = _bandlimited_complex(L), 0.7 * _bandlimited_complex(L)
    fA, gA = f.copy(), g.copy()
    for _ in range(n):
        fA, gA = weyl_step_3d_bcc(fA, gA, "+")
    fA = bsm.block_average_field(fA, b); gA = bsm.block_average_field(gA, b)
    fB = bsm.block_average_field(f, b); gB = bsm.block_average_field(g, b)
    for _ in range(n):
        fB, gB = bsm.renormalized_weyl_step(fB, gB, b, "+")
    assert max(np.max(np.abs(fA - fB)), np.max(np.abs(gA - gB))) < 1e-11


# ════════════════════════════════════════════════════════════════════
#  C — coarse chiral/Weyl steps stay unitary
# ════════════════════════════════════════════════════════════════════
def test_C_coarse_steps_conserve_norm():
    rng = np.random.default_rng(3)
    E = rng.standard_normal((3, 12, 12, 12)); B = rng.standard_normal((3, 12, 12, 12))
    n0 = np.sum(E ** 2 + B ** 2)
    for _ in range(100):
        E, B = bsm.renormalized_chiral_step(E, B, 2)
    assert abs(np.sum(E ** 2 + B ** 2) - n0) / n0 < 1e-12

    f = rng.standard_normal((12, 12, 12)) + 1j * rng.standard_normal((12, 12, 12))
    g = rng.standard_normal((12, 12, 12)) + 1j * rng.standard_normal((12, 12, 12))
    m0 = np.sum(np.abs(f) ** 2 + np.abs(g) ** 2)
    for _ in range(100):
        f, g = bsm.renormalized_weyl_step(f, g, 2, "+")
    assert abs(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2) - m0) / m0 < 1e-12


# ════════════════════════════════════════════════════════════════════
#  D — verified hand-rolled chiral core
# ════════════════════════════════════════════════════════════════════
def test_D_cmul_matches_complex_multiply():
    rng = np.random.default_rng(4)
    a = rng.standard_normal(50) + 1j * rng.standard_normal(50)
    b = rng.standard_normal(50) + 1j * rng.standard_normal(50)
    r, i = cc.cmul(a.real, a.imag, b.real, b.imag)
    assert np.allclose(r + 1j * i, a * b)


def test_D_handrolled_weyl_matches_kernel():
    rng = np.random.default_rng(1)
    f = rng.standard_normal((12, 12, 12)) + 1j * rng.standard_normal((12, 12, 12))
    g = rng.standard_normal((12, 12, 12)) + 1j * rng.standard_normal((12, 12, 12))
    f1, g1 = cc.weyl_step(f, g, "+", block=1)
    f2, g2 = weyl_step_3d_bcc(f, g, "+")
    assert max(np.max(np.abs(f1 - f2)), np.max(np.abs(g1 - g2))) < 1e-13
    # block-renormalised hand-rolled == blockspin renormalised
    f3, g3 = cc.weyl_step(f, g, "+", block=2)
    f4, g4 = bsm.renormalized_weyl_step(f, g, 2, "+")
    assert max(np.max(np.abs(f3 - f4)), np.max(np.abs(g3 - g4))) < 1e-13


def test_D_handrolled_chiral_rs_matches_kernel():
    rng = np.random.default_rng(2)
    E = rng.standard_normal((3, 12, 12, 12)); B = rng.standard_normal((3, 12, 12, 12))
    e1, b1 = cc.chiral_rs_step(E, B, block=1)
    e2, b2 = w_propagation_step_chiral(E, B)
    assert max(np.max(np.abs(e1 - e2)), np.max(np.abs(b1 - b2))) < 1e-13


# ════════════════════════════════════════════════════════════════════
#  E — the backend seam works (swap validation)
# ════════════════════════════════════════════════════════════════════
def test_E_chiral_core_registers_and_dispatches():
    core = cc.register()
    assert "chiral_core" in backend.available()
    rng = np.random.default_rng(5)
    f = rng.standard_normal((10, 10, 10)) + 1j * rng.standard_normal((10, 10, 10))
    g = rng.standard_normal((10, 10, 10)) + 1j * rng.standard_normal((10, 10, 10))
    fs, gs = core.chiral_transform("weyl", f, g, sign="+")
    fk, gk = weyl_step_3d_bcc(f, g, "+")
    assert np.allclose(fs, fk) and np.allclose(gs, gk)


def test_E_numpy_backend_matches_cafft():
    rng = np.random.default_rng(2)
    a = rng.standard_normal((16, 16, 16)) + 1j * rng.standard_normal((16, 16, 16))
    try:
        backend.use("ca_fft")
        fa = backend.fftn(a)
        backend.use("numpy_fft")
        fb = backend.fftn(a)
        assert np.max(np.abs(fa - fb)) < 1e-10            # identical to round-off
        assert np.allclose(backend.ifftn(backend.fftn(a)), a)
    finally:
        backend.use("ca_fft")


# ════════════════════════════════════════════════════════════════════
#  F — FFT round-off floor stays at ~1 ulp/step as L grows
# ════════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("L", [8, 16, 32])
def test_F_fft_floor_stable(L):
    from casim.fields.photon import photon_step_spectral
    rng = np.random.default_rng(0)
    E = rng.standard_normal((3, L, L, L)); B = rng.standard_normal((3, L, L, L))
    n0 = np.sum(E ** 2 + B ** 2)
    n = 200
    for _ in range(n):
        E, B = photon_step_spectral(E, B)
    per_step = abs(np.sum(E ** 2 + B ** 2) - n0) / n0 / n
    assert per_step < 1e-14            # ~1 ulp/step, no L degradation


# ════════════════════════════════════════════════════════════════════
#  G — engine channels run faithfully with block > 1
# ════════════════════════════════════════════════════════════════════
def test_G_w_chiral_channel_coarse_run():
    from casim.engine import Simulation, LatticeSpec
    from casim.engine.core.channels import WChiralChannel
    sim = Simulation(LatticeSpec(L=8, block=2, topology="cubic"),
                     [WChiralChannel(name="w")], seed=1)
    e0 = sim.channels["w"].energy(sim.states["w"])
    sim.step(5)
    assert np.all(np.isfinite(sim.states["w"]["E"]))
    assert abs(sim.channels["w"].energy(sim.states["w"]) - e0) / e0 < 1e-10


def test_G_weyl_channel_blockspin_preserves_complex():
    from casim.engine import Simulation, LatticeSpec
    from casim.engine.core.channels import WeylBCCChannel
    sim = Simulation(LatticeSpec(L=16, topology="bcc"),
                     [WeylBCCChannel(name="w", sign="+")], seed=2)
    sim.step(2)
    sim.block_spin(2)
    assert sim.lattice.L == 8 and sim.lattice.block == 2
    f = sim.states["w"]["f"]
    assert np.iscomplexobj(f) and np.any(f.imag != 0.0)   # imag part kept
    assert f.shape == (8, 8, 8)
    sim.step(3)                                            # coarse run continues
    assert np.all(np.isfinite(sim.states["w"]["f"]))


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
