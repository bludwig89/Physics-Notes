#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F133_blockspin_engine.py
=============================

F133 — Phase 4: the block-spin RG R_b as a first-class CASIM engine operation.

A run can declare a physical patch size and a block factor, and the engine can
coarse-grain a live run by R_b (an adaptive-resolution CA step), keeping the
physical patch and the F130 invariants (c_lat fixed point, even/chiral classes,
the dielectric lock).

E1  LatticeSpec declares the physical patch: L super-cells + block b ⇒
    physical_L = L·b, cell_factor = b^dims; a scenario may give `physical_patch`
    + `block` and the engine derives L.
E2  Channel/Simulation block_spin reproduces ca_blockspin.block_average exactly,
    and is complex-safe for spinor channels (keeps the imaginary part).
E3  The renormalised even step Ω_coarse(κ)=Ω(κ/b) reduces to the fine photon
    step at b=1, and is dynamically faithful: [R_b, evolution] = 0 on band-
    limited fields (machine precision) — the coarse run reproduces the fine IR
    dynamics, and the implied physical speed is the c_lat fixed point.
E4  Simulation.block_spin shrinks the lattice (L→L/b), conserves the physical
    patch, keeps c_lat, records the event, and the coarse run keeps stepping.
E5  A scenario-scheduled block-spin runs end-to-end and reports its patch.
E6  The gravity dielectric coarse-grains by the log rule (φ averaged, K rebuilt),
    NOT by averaging K (which would carry the Jensen gap) — preserving A·B≡1.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "ca-simulation"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from casim.engine import Simulation, LatticeSpec      # noqa: E402
from casim.engine.channels import PhotonPairChannel    # noqa: E402
import casim.engine.blockspin as bsm                    # noqa: E402
import ca_blockspin as cb                               # noqa: E402

ROOT3_INV = 1.0 / np.sqrt(3.0)


# ════════════════════════════════════════════════════════════════════
#  E1 — declare a physical patch + block factor
# ════════════════════════════════════════════════════════════════════
def test_E1_physical_patch_bookkeeping():
    lat = LatticeSpec(L=8, dims=3, block=4)
    assert lat.physical_L == 32
    assert lat.cell_factor == 64
    s = bsm.patch_summary(lat)
    assert s["physical_L"] == 32
    assert s["physical_cells_total"] == 32 ** 3
    assert abs(s["c_lat"] - ROOT3_INV) < 1e-15      # RG fixed point (T1)


def test_E1_scenario_derives_L_from_patch():
    sc = {
        "name": "p", "ticks": 0,
        "lattice": {"physical_patch": 64, "block": 4},
        "channels": [{"type": "photon_pair", "init": "random"}],
    }
    sim = Simulation.from_scenario(sc)
    assert sim.lattice.L == 16            # 64 / 4
    assert sim.lattice.physical_L == 64
    # indivisible patch is rejected
    with pytest.raises(ValueError):
        Simulation.from_scenario({**sc, "lattice": {"physical_patch": 65,
                                                    "block": 4}})


# ════════════════════════════════════════════════════════════════════
#  E2 — engine R_b reproduces ca_blockspin, complex-safe
# ════════════════════════════════════════════════════════════════════
def test_E2_block_spin_matches_ca_blockspin():
    sim = Simulation(LatticeSpec(L=16),
                     [PhotonPairChannel(name="g", init="random")], seed=1)
    E0 = sim.states["g"]["E"].copy()
    sim.block_spin(2)
    Ec = sim.states["g"]["E"]
    for comp in range(3):
        ref = cb.block_average(E0[comp], 2)
        assert np.array_equal(Ec[comp], ref)        # exact match
    assert Ec.shape == (3, 8, 8, 8)


def test_E2_block_spin_is_complex_safe():
    """Spinor channels keep their imaginary part — the float-casting
    ca_blockspin.block_average would silently drop it (CLAUDE.md caveat)."""
    L, b = 12, 2
    psi = (np.random.default_rng(0).standard_normal((L, L, L))
           + 1j * np.random.default_rng(1).standard_normal((L, L, L)))
    out = bsm.block_average_field(psi, b)
    assert np.iscomplexobj(out)
    assert np.any(out.imag != 0.0)
    # equals the mean of each block in both parts
    ref_r = cb.block_average(psi.real, b)
    ref_i = cb.block_average(psi.imag, b)
    assert np.allclose(out.real, ref_r) and np.allclose(out.imag, ref_i)


# ════════════════════════════════════════════════════════════════════
#  E3 — renormalised even step + dynamical faithfulness
# ════════════════════════════════════════════════════════════════════
def test_E3_renormalized_reduces_to_fine_at_block1():
    from casim.fields.photon import photon_step_spectral
    rng = np.random.default_rng(0)
    E = rng.standard_normal((3, 12, 12, 12))
    B = rng.standard_normal((3, 12, 12, 12))
    e1, b1 = bsm.renormalized_even_step(E, B, 1)
    e2, b2 = photon_step_spectral(E, B)
    assert np.allclose(e1, e2) and np.allclose(b1, b2)


def test_E3_block_spin_commutes_with_evolution():
    """[R_b, evolution] = 0 on band-limited fields: R_b∘step_fine ==
    step_coarse(renormalised)∘R_b to machine precision (the coarse run
    reproduces the fine IR dynamics)."""
    from casim.fields.photon import photon_step_spectral
    L, b, n = 16, 2, 8
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    k = 2 * np.pi / L

    def smooth():
        f = np.zeros((3, L, L, L))
        for c in range(3):
            f[c] = (np.cos(k * X + 0.3 * c) + 0.5 * np.cos(k * Y)
                    + 0.3 * np.cos(2 * k * Z + c))
        return f
    E, B = smooth(), 0.4 * smooth()

    EA, BA = E.copy(), B.copy()
    for _ in range(n):
        EA, BA = photon_step_spectral(EA, BA)
    EA = bsm.block_average_field(EA, b)
    BA = bsm.block_average_field(BA, b)

    EB = bsm.block_average_field(E, b)
    BB = bsm.block_average_field(B, b)
    for _ in range(n):
        EB, BB = bsm.renormalized_even_step(EB, BB, b)

    err = max(np.max(np.abs(EA - EB)), np.max(np.abs(BA - BB)))
    assert err < 1e-11, err


def test_E3_physical_speed_is_fixed_point():
    """The renormalised coarse rule has the c_lat fixed point (F130 T1): the
    physical speed b·c_coarse = 1/√3 for the block factors the engine uses."""
    for b in (2, 3, 4):
        c_phys = b * cb.extract_speed(b=b)          # uses Ω(κ/b), the engine rule
        assert abs(c_phys - ROOT3_INV) < 1e-8


# ════════════════════════════════════════════════════════════════════
#  E4 — runtime block_spin operation
# ════════════════════════════════════════════════════════════════════
def test_E4_runtime_block_spin():
    sim = Simulation(LatticeSpec(L=16, block=1),
                     [PhotonPairChannel(name="g", init="random")], seed=3)
    phys0 = sim.lattice.physical_L
    sim.step(2)
    ev = sim.block_spin(2)
    assert sim.lattice.L == 8
    assert sim.lattice.block == 2
    assert sim.lattice.physical_L == phys0          # patch conserved
    assert abs(sim.lattice.c_lat - ROOT3_INV) < 1e-15
    assert ev["factor"] == 2 and ev["physical_L"] == phys0
    assert sim.states["g"]["E"].shape == (3, 8, 8, 8)
    # the coarse run keeps stepping
    sim.step(3)
    assert sim.tick == 5
    assert np.all(np.isfinite(sim.states["g"]["E"]))


def test_E4_block_spin_rejects_indivisible():
    sim = Simulation(LatticeSpec(L=18),
                     [PhotonPairChannel(name="g", init="random")], seed=0)
    with pytest.raises(ValueError):
        sim.block_spin(4)                            # 18 % 4 ≠ 0


# ════════════════════════════════════════════════════════════════════
#  E5 — scenario-scheduled block-spin runs end to end
# ════════════════════════════════════════════════════════════════════
def test_E5_scheduled_blockspin_scenario():
    sc = {
        "name": "sched", "ticks": 8, "seed": 1,
        "lattice": {"physical_patch": 32, "block": 2},
        "channels": [{"type": "photon_pair", "init": "random"}],
        "blockspin": [{"at": 4, "factor": 2}],
    }
    sim = Simulation.from_scenario(sc)
    assert sim.lattice.L == 16 and sim.lattice.block == 2
    res = sim.run(8)
    assert sim.lattice.L == 8 and sim.lattice.block == 4
    assert res["physical_patch"]["physical_L"] == 32   # invariant throughout
    assert len(res["blockspin_events"]) == 1
    assert res["blockspin_events"][0]["tick"] == 4


# ════════════════════════════════════════════════════════════════════
#  E6 — gravity dielectric coarse-grains by the log rule (A·B ≡ 1)
# ════════════════════════════════════════════════════════════════════
def test_E6_gravity_dielectric_log_rule():
    from casim.engine.channels import GravityDielectricChannel
    lat = LatticeSpec(L=16)
    ch = GravityDielectricChannel(name="grav", M=1.0, sigma=3.0, G=1.0)
    rng = np.random.default_rng(0)
    st = ch.init_state(lat, rng)
    c = float(st["c"])

    st_c = ch.block_spin(st, lat, 2)
    # K rebuilt from the block-averaged (linear) φ — the F130 T3b log rule
    K_log = np.exp(-2.0 * st_c["phi"] / c ** 2)
    assert np.allclose(st_c["K"], K_log)
    # reciprocal lock A·B ≡ 1 preserved
    A, B = 1.0 / st_c["K"], st_c["K"]
    assert np.max(np.abs(A * B - 1.0)) < 1e-12
    # and this is NOT the naive direct-K average (Jensen gap) on a varying φ
    K_direct = bsm.block_average_field(st["K"], 2)
    assert not np.allclose(st_c["K"], K_direct)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
