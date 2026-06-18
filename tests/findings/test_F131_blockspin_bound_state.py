#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F131_blockspin_bound_state.py
==================================

F131 — Phase-2: a coarse-grained bound state reproduces the fine-grained
spectrum.  The block-spin transform R_b (F130) must COMMUTE WITH BINDING — a
bound state on a coarse lattice of N super-cells reproduces the spectrum of the
(bN)^d-cell fine problem in the long-wavelength sector.

H = -(1/2m) ∇² + V(x) on the F130 `lap_nd` stencil; coarse-grained as
H_coarse = -(1/2m) lap_coarse/b² + diag(R_b V).

B1  Binding survives — discrete, bound, correct ordering, harmonic spacing ω,
    3-fold first-excited degeneracy (O_h shell), preserved by R_b.
B2  RG commutes with binding — low eigenvalues match; the residual is the
    irrelevant O((k a)²) discretisation operator (shrinks as the state is more IR
    / grows ~b² with the block factor), NOT a binding failure.
B3  Wavefunction reproduction — |⟨R_b ψ_fine | ψ_coarse⟩| → 1.
B4  Absolute accuracy — both converge to the analytic continuum spectrum
    E_N = ω(N + 3/2); the coarse run reaches it with b^d × fewer cells.
B5  Coulomb / hydrogen stand-in — the EM bound state (E0 < 0) is reproduced.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "ca-simulation"))

pytest.importorskip("scipy")
import ca_blockspin_binding as bb   # noqa: E402

# Canonical harmonic problem: well wide enough to be smooth (IR) yet contained
# in the L=24 box.
L = 24
K = 4e-3
MASS = 1.0
OMEGA = np.sqrt(K / MASS)


@pytest.fixture(scope="module")
def harmonic_b2():
    Vf = bb.harmonic_potential(L, K)
    return bb.coarse_grain_spectrum(Vf, 2, mass=MASS, n_states=4)


# ════════════════════════════════════════════════════════════════════
#  B1 — binding survives R_b
# ════════════════════════════════════════════════════════════════════
def test_B1_levels_are_bound_and_ordered(harmonic_b2):
    """Fine and coarse spectra are discrete, bound (below the well top), and
    correctly ordered."""
    Ef, Ec = harmonic_b2["E_fine"], harmonic_b2["E_coarse"]
    well_top = 0.5 * K * (L // 2) ** 2
    for E in (Ef, Ec):
        assert np.all(E < well_top)              # bound
        assert np.all(np.diff(E) >= -1e-9)       # ordered (non-decreasing)
    assert Ef[0] < Ef[1] - 1e-6                   # a real gap above the ground


def test_B1_harmonic_spacing_and_degeneracy(harmonic_b2):
    """The first-excited level is the O_h triplet at ω above the ground, and the
    3-fold degeneracy survives coarse-graining."""
    for E in (harmonic_b2["E_fine"], harmonic_b2["E_coarse"]):
        # level spacing E1 - E0 ≈ ω
        assert abs((E[1] - E[0]) - OMEGA) / OMEGA < 0.05
        # 3-fold degeneracy of the first excited shell
        triplet = E[1:4]
        assert np.ptp(triplet) < 1e-6 * abs(E[1])


# ════════════════════════════════════════════════════════════════════
#  B2 — RG commutes with binding
# ════════════════════════════════════════════════════════════════════
def test_B2_low_levels_match(harmonic_b2):
    """Ground + first shell agree fine↔coarse to <1% (b=2)."""
    assert harmonic_b2["rel_err"][0] < 0.01
    assert np.all(harmonic_b2["rel_err"][:4] < 0.02)


def test_B2_error_shrinks_as_state_becomes_IR():
    """The coarse↔fine ground error decreases as the well widens (state more
    IR) — it is the irrelevant discretisation operator, not a binding failure."""
    errs = []
    for k in (8e-3, 4e-3, 2e-3):
        r = bb.coarse_grain_spectrum(bb.harmonic_potential(L, k), 2,
                                     mass=MASS, n_states=2)
        errs.append(r["rel_err"][0])
    assert errs[0] > errs[1] > errs[2]           # monotone decrease


def test_B2_coarse_error_grows_like_bsquared():
    """The coarse discretisation error grows ~b² (the O((k a)²) operator), the
    same irrelevant scaling as F130 T2 — staying small, never diverging."""
    Vf = bb.harmonic_potential(L, K)
    e2 = bb.coarse_grain_spectrum(Vf, 2, mass=MASS, n_states=2)["rel_err"][0]
    e4 = bb.coarse_grain_spectrum(Vf, 4, mass=MASS, n_states=2)["rel_err"][0]
    # b=4 vs b=2: (4²-1)/(2²-1) = 5× in the leading correction; allow a band
    ratio = e4 / e2
    assert 2.0 < ratio < 8.0
    assert e4 < 0.02                              # still small (bound, faithful)


# ════════════════════════════════════════════════════════════════════
#  B3 — wavefunction reproduction
# ════════════════════════════════════════════════════════════════════
def test_B3_ground_wavefunction_overlap(harmonic_b2):
    """Block-averaged fine ground state == coarse ground state."""
    assert harmonic_b2["ground_overlap"] > 0.999


def test_B3_fewer_cells(harmonic_b2):
    """The coarse run uses b^d × fewer cells (here 8×)."""
    assert harmonic_b2["n_cells_coarse"] * 8 == harmonic_b2["n_cells_fine"]


# ════════════════════════════════════════════════════════════════════
#  B4 — absolute accuracy vs the analytic continuum spectrum
# ════════════════════════════════════════════════════════════════════
def test_B4_converges_to_continuum(harmonic_b2):
    """Both fine and coarse ground energies match the analytic E_0 = (3/2)ω; the
    coarse one does so with 8× fewer cells."""
    E0_cont = bb.harmonic_continuum_levels(K, MASS, n_levels=1)[0]
    assert abs(harmonic_b2["E_fine"][0] - E0_cont) / E0_cont < 0.01
    assert abs(harmonic_b2["E_coarse"][0] - E0_cont) / E0_cont < 0.01


def test_B4_first_shell_matches_continuum(harmonic_b2):
    """The first-excited triplet sits at the analytic E_1 = (5/2)ω."""
    E1_cont = bb.harmonic_continuum_levels(K, MASS, n_levels=2)[1]
    assert abs(harmonic_b2["E_coarse"][1] - E1_cont) / E1_cont < 0.02


# ════════════════════════════════════════════════════════════════════
#  B5 — Coulomb / hydrogen stand-in (the EM bound state)
# ════════════════════════════════════════════════════════════════════
def test_B5_coulomb_ground_state_reproduced():
    """The attractive Coulomb (F125 hydrogen long-wavelength) ground state is
    bound (E0 < 0) and reproduced by the coarse run (b=2) to <1%, overlap >0.99."""
    Vf = bb.coulomb_potential(L, alpha=2.0, soft=2.0)
    r = bb.coarse_grain_spectrum(Vf, 2, mass=MASS, n_states=3)
    assert r["E_fine"][0] < 0.0                   # bound
    assert r["E_coarse"][0] < 0.0
    assert r["rel_err"][0] < 0.01
    assert r["ground_overlap"] > 0.99


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
