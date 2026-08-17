#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F140_coarse_grained_baryon.py
==================================

F140 — the coarse-grained baryon element.  A genuine LATTICE reduction of the
F122 three-quark Cornell problem (the hyperradial K=0 channel as a 1-D radial
element) that can be block-spun — supplying what F132 handled only by ingredient
covariance (the ECG is a basis, not a lattice).

K1  the element reproduces the F122 ECG baryon ground energy across σ once a
    single (σ-independent) adiabatic coefficient is matched (EFT-style);
K2  it is confinement-dominated — E_rel ∝ σ^{2/3} (the string scale);
K3  it coarse-grains under R_b (hyperradial grid decimation): baryon mass + rms
    hyperradius reproduced on b× fewer cells, with the irrelevant O(h²) error;
K4  the confining coupling is the F130-C1 relevant operator (σ̂→b·σ̂), so the
    physical baryon mass is the RG-covariant string scale;
K5  the hyperangular K=0 constants are the closed forms (⟨|u|⟩=16/15π, C_σ,
    centrifugal 15/4).
"""
import os
import sys

import numpy as np
import pytest

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

pytest.importorskip("scipy")
from casim.engine.lattice import blockspin_baryon as bb        # noqa: E402


# ════════════════════════════════════════════════════════════════════
#  K5 — closed-form hyperangular constants
# ════════════════════════════════════════════════════════════════════
def test_K5_closed_form_constants():
    assert abs(bb.PROJ_ABS_6 - 16.0 / (15.0 * np.pi)) < 1e-15
    assert abs(bb.HYPER_C0 - 16.0 * np.sqrt(2.0) / (5.0 * np.pi)) < 1e-12
    assert bb.CENTRIFUGAL_K0 == 15.0 / 4.0


# ════════════════════════════════════════════════════════════════════
#  K1 — reproduces the ECG baryon (calibrated once, σ-independent)
# ════════════════════════════════════════════════════════════════════
def test_K1_matches_ecg_across_sigma():
    from casim.engine.particles import baryon_dynamics as bd
    for s in (0.5, 1.0, 2.0, 4.0):
        E = bb.hyperradial_baryon(s, m=1.0, N=1200)["E_rel"]
        E_ecg = bd.ground_state_relative_energy(
            m=1.0, sigma=s, alpha_s=0.0)["E_rel_cholesky"]
        assert abs(E - E_ecg) / E_ecg < 0.005          # <0.5% across the range


def test_K1_calibration_is_sigma_independent():
    """The single adiabatic coefficient matched at σ=1 also matches σ=4 — it is
    a constant (both scale as σ^{2/3}), not a per-point fit."""
    k1 = bb.calibrate_to_ecg(sigma=1.0)
    k4 = bb.calibrate_to_ecg(sigma=4.0)
    assert abs(k1 - k4) / k1 < 0.01
    assert abs(k1 - bb.BARYON_ADIABATIC_CAL) / bb.BARYON_ADIABATIC_CAL < 0.01


# ════════════════════════════════════════════════════════════════════
#  K2 — confinement-dominated string scale
# ════════════════════════════════════════════════════════════════════
def test_K2_confinement_scaling_two_thirds():
    _, slope = bb.baryon_confinement_scaling([0.5, 1.0, 2.0, 4.0])
    assert abs(slope - 2.0 / 3.0) < 0.01


# ════════════════════════════════════════════════════════════════════
#  K3 — the element coarse-grains under R_b
# ════════════════════════════════════════════════════════════════════
@pytest.fixture(scope="module")
def cg_scan():
    return {b: bb.baryon_coarse_grain(1200, b, sigma=1.0, m=1.0)
            for b in (2, 4, 8)}


def test_K3_mass_reproduced(cg_scan):
    assert cg_scan[2]["E_rel_rel_err"] < 0.01          # <1% at b=2
    assert cg_scan[4]["E_rel_rel_err"] < 0.02
    # error grows with the block factor (irrelevant O(h²) operator)
    assert cg_scan[8]["E_rel_rel_err"] > cg_scan[2]["E_rel_rel_err"]
    assert cg_scan[8]["E_rel_rel_err"] < 0.05          # still faithful at b=8


def test_K3_wavefunction_and_size_reproduced(cg_scan):
    for b, r in cg_scan.items():
        assert r["overlap"] > 0.99                     # amplitude reproduced
        assert r["rms_rel_err"] < 0.01
    assert cg_scan[8]["N_coarse"] * 8 == cg_scan[8]["N_fine"]


def test_K3_stays_confined(cg_scan):
    """The coarse baryon is still a real bound element: positive E_rel
    (confinement energy) and a finite, sensible hyperradius."""
    for r in cg_scan.values():
        assert r["E_rel_coarse"] > 0.0
        assert 0.5 < r["rms_coarse"] < 5.0


# ════════════════════════════════════════════════════════════════════
#  K4 — confining coupling is the C1 relevant operator
# ════════════════════════════════════════════════════════════════════
def test_K4_confinement_is_relevant():
    for b in (2, 3, 4):
        assert bb.confinement_relevant_flow(b) == float(b)
        assert bb.confinement_relevant_flow(b) > 1.0   # relevant (vs LIV b^-n)


def test_K4_matches_F130_C1_eigenvalue():
    """The element's confining flow is the same relevant eigenvalue λ_σ=b proved
    in F130-C1."""
    from casim.engine.lattice import blockspin as cb
    for b in (2, 3):
        assert bb.confinement_relevant_flow(b) == cb.confinement_eigenvalue(b)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
