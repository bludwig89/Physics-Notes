#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F132_blockspin_dynamical_bound_states.py
=============================================

F132 — Coarse-graining the model's DYNAMICAL bound states under the F130
block-spin RG, exposing the Wilsonian relevant/irrelevant distinction:

  P (pion, F74/F103, CONTACT)  — the contact coupling is RELEVANT: it must RUN
     under R_b (g_coarse ≠ g_fine), the flow fixed by the Watson threshold ratio
     g/g_c; once run, E_b, the wavefunction and the size are reproduced on b³×
     fewer cells.
  D (deuteron, F104, FINITE-RANGE) — the smooth Yukawa/OBE coupling is held
     FIXED; coarse-graining is grid decimation and the shallow halo reproduces
     with the irrelevant O(h²) error, no running.
  B (baryon, F122, CONFINED) — confinement-dominated: E_rel ∝ σ^{2/3} (string
     scale), carried by the F130-C1-covariant σ; the ECG engine reproduces the
     analytic harmonic three-body ground state.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "ca-simulation"))

pytest.importorskip("scipy")
import ca_blockspin_dynamical as bd   # noqa: E402


# ════════════════════════════════════════════════════════════════════
#  P — pion (contact): the coupling RUNS (relevant operator)
# ════════════════════════════════════════════════════════════════════
@pytest.fixture(scope="module")
def pion_b2():
    return bd.contact_coarse_grain(12, t=1.0, g=4.0, b=2)


@pytest.fixture(scope="module")
def pion_b3():
    return bd.contact_coarse_grain(12, t=1.0, g=4.0, b=3)


def test_P_coupling_runs(pion_b2, pion_b3):
    """The contact coupling is relevant — it runs strongly under R_b
    (g: 4 → ~1 at b=2, ~0.45 at b=3), not held fixed."""
    assert pion_b2["coupling_ran"]
    assert pion_b2["g_coarse_exact"] < 0.5 * pion_b2["g_fine"]
    assert pion_b3["g_coarse_exact"] < pion_b2["g_coarse_exact"]


def test_P_flow_predicted_by_watson_ratio(pion_b2, pion_b3):
    """The running is fixed by proximity to the Watson threshold: holding
    g/g_c invariant predicts g_coarse to a few %."""
    for r in (pion_b2, pion_b3):
        rel = abs(r["g_coarse_exact"] - r["g_coarse_predicted"]) \
            / r["g_coarse_predicted"]
        assert rel < 0.05
        # the RG-invariant ratio is preserved
        assert abs(r["g_over_gc_coarse"] - r["g_over_gc_fine"]) < 0.05


def test_P_binding_reproduced(pion_b2, pion_b3):
    """With the run coupling, the physical binding energy is reproduced."""
    for r in (pion_b2, pion_b3):
        assert abs(r["E_b_coarse"] - r["E_b_fine"]) / r["E_b_fine"] < 1e-3


def test_P_wavefunction_and_size_reproduced(pion_b2, pion_b3):
    """Bound-state wavefunction overlap → 1 and the rms size is reproduced,
    on b³× fewer cells."""
    assert pion_b2["ground_overlap"] > 0.98
    assert pion_b3["ground_overlap"] > 0.97
    for r in (pion_b2, pion_b3):
        assert abs(r["rms_coarse"] - r["rms_fine"]) / r["rms_fine"] < 0.05
    assert pion_b2["n_cells_coarse"] * 8 == pion_b2["n_cells_fine"]
    assert pion_b3["n_cells_coarse"] * 27 == pion_b3["n_cells_fine"]


# ════════════════════════════════════════════════════════════════════
#  D — deuteron (finite-range): coupling FIXED, irrelevant O(h²)
# ════════════════════════════════════════════════════════════════════
DEUT_CFG = dict(core="derived", b=0.55, sigma=True, sigma_g2_4pi=3.693,
                tensor=True)


@pytest.fixture(scope="module")
def deuteron_scan():
    return {bb: bd.deuteron_coarse_grain(800, bb, **DEUT_CFG) for bb in (2, 4)}


def test_D_stays_bound_under_coarse_graining(deuteron_scan):
    """The shallow deuteron stays bound as the radial grid is decimated."""
    for r in deuteron_scan.values():
        assert r["bound_fine"] and r["bound_coarse"]
        assert r["E_b_coarse"] > 0.0


def test_D_binding_reproduced_no_running(deuteron_scan):
    """At fixed physical coupling, E_b and r_d are reproduced — <1% at b=2,
    the error growing ~b² (the irrelevant discretisation operator)."""
    r2, r4 = deuteron_scan[2], deuteron_scan[4]
    assert r2["E_b_rel_err"] < 0.01
    assert r4["E_b_rel_err"] < 0.05
    assert r2["r_d_rel_err"] < 0.01
    # error grows with the block factor (irrelevant operator, ~h²)
    assert r4["E_b_rel_err"] > r2["E_b_rel_err"]


def test_D_radius_is_a_halo():
    """Sanity: the deuteron is a large, IR halo (r_d ≈ 1.9 fm ≫ the grid),
    which is why it coarse-grains so well."""
    r = bd.deuteron_coarse_grain(800, 2, **DEUT_CFG)
    assert 1.5 < r["r_d_fine"] < 3.0


# ════════════════════════════════════════════════════════════════════
#  B — baryon (confined): mass = C1-covariant string scale
# ════════════════════════════════════════════════════════════════════
def test_B_confinement_scaling_is_string_scale():
    """The three-body confined ground energy scales as E_rel ∝ σ^{2/3} (linear-
    potential virial) — the baryon mass IS the string scale, carried by the
    F130-C1-covariant σ, hence RG-covariant."""
    _, slope = bd.baryon_confinement_scaling([0.5, 1.0, 2.0, 4.0, 8.0])
    assert abs(slope - 2.0 / 3.0) < 0.01


def test_B_ecg_engine_reproduces_analytic_harmonic():
    """The correlated-Gaussian engine reproduces the analytic three-body
    harmonic ground state E = 3√(3k/m) — the machine-precision self-test the
    coarse-graining argument rests on."""
    exact, ecg, rel = bd.baryon_harmonic_validation(k=0.7, m=1.3)
    assert rel < 0.01


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
