#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F130_blockspin_gauge_gravity.py
====================================

F130 — Phase-1 block-spin / coarse-graining RG scheme, gauge + gravity sectors.

Verifies, to algebraic exactness (machine precision), that the Kadanoff block
transform R_b (group b^d fine cells into one super-cell) preserves the rotation
rule's physical content, so a coarse run of N super-cells faithfully represents
(bN)^d physical cells.  This is the Phase-1 gate of
`docs/roadmaps/roadmap-scale-to-real-space.md`.

The free-photon sector is F129 (concurrent); this suite covers the gauge (F110
Kogut–Susskind Gauss law) and gravity (F64/F106 dielectric) sectors and the
shared dispersion theorems, consuming the free-photon dispersion read-only.

Theorems
--------
T1   c_lat is an RG fixed point — physical speed invariant for all b (exact).
T2   LIV / lattice-artifact operators are irrelevant — eigenvalue b^{-n}; the
     leading even-law operator reproduces F30 (g2 = −1/162, δv_g/c = −k²/54).
T3a  Gauss law survives blocking (integer-exact discrete divergence theorem).
T3b  The gravity dielectric survives blocking (AB≡1 under log-averaging; the
     naive K-average carries a Jensen gap; linear Poisson law IR-invariant).
T3c  The F91 even/chiral propagator class is preserved ([R_b, R(Ω)] = 0).
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "ca-simulation"))

import ca_blockspin as bs   # noqa: E402

ROOT3_INV = 1.0 / np.sqrt(3.0)


# ════════════════════════════════════════════════════════════════════
#  T1 — c_lat is an RG fixed point
# ════════════════════════════════════════════════════════════════════
@pytest.mark.machine_precision
@pytest.mark.parametrize("b", [1, 2, 3, 4, 5])
def test_T1_clat_fixed_point(b):
    """Physical speed b·c_coarse(b) == 1/√3 for every block factor b."""
    c_phys = b * bs.extract_speed(b=b)
    assert abs(c_phys - ROOT3_INV) < 1e-9, f"b={b}: c_phys={c_phys}"


@pytest.mark.machine_precision
def test_T1_clat_fixed_point_all_directions():
    """The fixed point holds along axis, face- and body-diagonal alike."""
    for direction in (bs.AXIS, bs.FACE_DIAGONAL, bs.BODY_DIAGONAL):
        for b in (1, 2, 4):
            c_phys = b * bs.extract_speed(direction=direction, b=b)
            assert abs(c_phys - ROOT3_INV) < 1e-8


# ════════════════════════════════════════════════════════════════════
#  T2 — lattice-artifact (LIV) operators are irrelevant
# ════════════════════════════════════════════════════════════════════
@pytest.mark.exact
def test_T2_leading_liv_matches_F30():
    """Leading even-law operator on the body diagonal: g2 = −1/162
    (equivalently δv_g/c = −k²/54, the F30/E_QG2 prediction)."""
    g2 = bs.extract_leading_liv(direction=bs.BODY_DIAGONAL)
    assert abs(g2 - (-1.0 / 162.0)) < 1e-6, g2
    # velocity form: dv_g/c = 3·g2·k²  →  coefficient −1/54
    assert abs(3.0 * g2 - (-1.0 / 54.0)) < 3e-6


@pytest.mark.machine_precision
@pytest.mark.parametrize("b", [2, 3, 4, 5])
def test_T2_liv_eigenvalue_order2(b):
    """The leading LIV operator has RG eigenvalue exactly b^{-2}."""
    eig = bs.rg_eigenvalue(b, order=2)
    assert abs(eig - b ** (-2.0)) < 1e-10, f"b={b}: eig={eig}"


@pytest.mark.machine_precision
@pytest.mark.parametrize("b", [2, 3])
def test_T2_liv_eigenvalue_order4(b):
    """The next operator has eigenvalue b^{-4} (even more irrelevant)."""
    eig = bs.rg_eigenvalue(b, order=4)
    assert abs(eig / b ** (-4.0) - 1.0) < 1e-7, f"b={b}: eig={eig}"


def test_T2_eigenvalues_strictly_below_one():
    """Every artifact operator shrinks: λ_n = b^{-n} < 1 (IR-attractive)."""
    for b, (meas, pred) in bs.liv_irrelevance((2, 3, 4, 5)).items():
        assert meas < 1.0
        assert abs(meas - pred) < 1e-9


# ════════════════════════════════════════════════════════════════════
#  T3a — Gauss law survives block-spin (F110 gauge sector)
# ════════════════════════════════════════════════════════════════════
@pytest.mark.exact
@pytest.mark.parametrize("b", [2, 3, 4])
def test_T3a_gauss_law_integer_exact(b):
    """For an INTEGER electric field (ℤ-flux, F110 dual basis) the discrete
    divergence theorem is exactly integer: residual == 0."""
    rng = np.random.default_rng(7)
    L = 12 if b == 3 else 12 if b == 2 else 12
    L = b * (L // b)
    E = [rng.integers(-4, 5, (L, L, L)).astype(float) for _ in range(3)]
    res = bs.gauss_law_residual(E, b)
    assert res == 0.0, res


@pytest.mark.machine_precision
@pytest.mark.parametrize("b", [2, 3, 4])
def test_T3a_gauss_law_float(b):
    """For a continuous (float) electric field the theorem holds to round-off."""
    rng = np.random.default_rng(11)
    L = b * 4
    E = [rng.standard_normal((L, L, L)) for _ in range(3)]
    res = bs.gauss_law_residual(E, b)
    assert res < 1e-12, res


@pytest.mark.exact
def test_T3a_charge_is_conserved_block_total():
    """Total enclosed charge per coarse cell == block-sum of fine charge:
    the coarse run sees the right number of charges in each super-cell."""
    rng = np.random.default_rng(3)
    L, b = 9, 3
    E = [rng.integers(-2, 3, (L, L, L)).astype(float) for _ in range(3)]
    q_fine = bs.lattice_divergence(E)
    Q_coarse = bs.block_charge(q_fine, b)
    # global charge neutrality and per-block conservation
    assert abs(q_fine.sum() - Q_coarse.sum()) < 1e-9
    E_coarse = bs.coarse_face_flux(E, b)
    div_c = bs.lattice_divergence(E_coarse)
    assert np.max(np.abs(div_c - Q_coarse)) == 0.0


# ════════════════════════════════════════════════════════════════════
#  T3b — gravity dielectric survives blocking (F64/F106)
# ════════════════════════════════════════════════════════════════════
def _smooth_u(L, amp=0.13, seed=0):
    x = np.linspace(0, 2 * np.pi, L, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    return amp * (np.cos(X) * np.sin(Y) + 0.5 * np.cos(Z))


@pytest.mark.machine_precision
@pytest.mark.parametrize("b", [2, 3])
def test_T3b_reciprocal_lock_preserved(b):
    """A·B ≡ 1 (impedance match, non-birefringence) survives R_b when the
    dielectric is coarse-grained in its log u = ½ ln K."""
    u = _smooth_u(24 if b in (2, 3) else 24)
    assert bs.reciprocal_lock_residual(u, b) < 1e-14


@pytest.mark.exact
def test_T3b_jensen_gap_flags_wrong_variable():
    """Averaging K directly (the naive RG variable) carries a strictly positive
    Jensen gap K_direct ≥ K_log — proof that u, not K, is the covariant
    variable.  The gap vanishes only for a constant potential."""
    u = _smooth_u(24)
    gmax, gmean = bs.dielectric_jensen_gap(u, 3)
    assert gmax > 1e-6 and gmean > 0.0
    # constant potential → no variance → no gap
    u0 = np.full((12, 12, 12), 0.2)
    g0max, _ = bs.dielectric_jensen_gap(u0, 3)
    assert g0max < 1e-14


@pytest.mark.machine_precision
def test_T3b_poisson_form_invariance_is_irrelevant():
    """The linear Poisson source law is form-invariant in the IR: the residual
    of (1/b²)lap_coarse(R_b u) vs R_b(lap u) shrinks as b^{-2} per L-doubling,
    i.e. the gravity discretisation error is itself an irrelevant operator."""
    b = 2
    rels = []
    for L in (16, 32, 64, 128):
        x = np.linspace(0, 2 * np.pi, L, endpoint=False)
        X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
        u = 0.1 * np.cos(X) * np.cos(Y) * np.cos(Z)
        res = bs.poisson_form_invariance_residual(u, b)
        smax = np.max(np.abs(bs._grav.lap_nd(u)))
        rels.append(res / smax)
    rels = np.array(rels)
    # each L-doubling halves k → relative error ÷4 (→ exactly 1/b² = 1/4)
    ratios = rels[1:] / rels[:-1]
    assert np.all(ratios < 0.30)
    assert abs(ratios[-1] - 0.25) < 0.02, ratios


# ════════════════════════════════════════════════════════════════════
#  T3c — propagator class (F91 even/chiral) is preserved
# ════════════════════════════════════════════════════════════════════
@pytest.mark.machine_precision
@pytest.mark.parametrize("b", [2, 3, 4])
def test_T3c_blockspin_commutes_with_even_rotation(b):
    """[R_b, R(Ω)] = 0: a real, helicity-blind block kernel cannot mix the even
    and chiral propagator classes."""
    comm = bs.even_rotation_commutator(L=16 if b != 3 else 18, b=b)
    assert comm < 1e-11, comm


@pytest.mark.exact
def test_T3c_block_kernel_is_real_and_dc_preserving():
    """D_b(k) is real, even, ≤ 1, and D_b(0) = 1 (DC/charge preserved)."""
    k = np.linspace(-np.pi, np.pi, 401)
    for b in (2, 3, 4, 5):
        D = bs.block_kernel_factor(k, b)
        assert np.allclose(D.imag if np.iscomplexobj(D) else 0.0, 0.0)
        assert abs(bs.block_kernel_factor(0.0, b) - 1.0) < 1e-15
        assert np.all(D <= 1.0 + 1e-12)
        # even
        assert np.allclose(D, bs.block_kernel_factor(-k, b))


# ════════════════════════════════════════════════════════════════════
#  Sanity: block_average reproduces its Fourier form factor (DC + linearity)
# ════════════════════════════════════════════════════════════════════
@pytest.mark.machine_precision
def test_block_average_preserves_mean():
    """R_b conserves the field mean (DC) — the n=0 marginal direction."""
    rng = np.random.default_rng(5)
    f = rng.standard_normal((12, 12, 12))
    fc = bs.block_average(f, 3)
    assert abs(f.mean() - fc.mean()) < 1e-13


# ════════════════════════════════════════════════════════════════════
#  C1 — confinement is the ONE relevant direction (F110 gauge sector)
# ════════════════════════════════════════════════════════════════════
@pytest.mark.exact
@pytest.mark.parametrize("b", [2, 3, 4])
def test_C1_sigma_is_relevant_eigenvalue_b(b):
    """The string-tension RG eigenvalue is λ_σ = b > 1 (relevant), in contrast to
    the irrelevant LIV operators (b^{-n} < 1)."""
    assert bs.confinement_eigenvalue(b) == float(b)
    assert bs.confinement_eigenvalue(b) > 1.0
    assert bs.rg_eigenvalue(b, order=2) < 1.0          # the LIV contrast


@pytest.mark.exact
def test_C1_lambda0_string_tension_is_g2_over_2():
    """σ̂ = g²/2 exactly at λ=0 (F110 static-potential slope)."""
    for g2 in (0.5, 1.0, 2.0):
        assert abs(bs.string_tension_lambda0(g2) - 0.5 * g2) < 1e-15


@pytest.mark.machine_precision
@pytest.mark.parametrize("b", [2, 3])
def test_C1_coarse_run_reproduces_physical_potential(b):
    """A coarse F110 run on b× fewer plaquettes (with bond-moved g²=b·g²_fine)
    reproduces the fine static potential at matched physical separation — the
    confining energy V(R_phys) is an RG invariant."""
    pytest.importorskip("scipy")
    V_fine_matched, V_coarse, sep = bs.coarse_static_potential(
        6, b=b, g2_fine=1.0, lam=0.0)
    for R in V_coarse:
        assert abs(V_coarse[R] - V_fine_matched[R]) < 1e-12


@pytest.mark.parametrize("b", [2, 3])
def test_C1_magnetic_coupling_is_irrelevant(b):
    """The deconfining magnetic coupling λ deforms σ̂ by a fraction that shrinks
    as ≈ b^{-2} under blocking (→ the λ=0 area law is IR-attractive)."""
    pytest.importorskip("scipy")
    lam = [0.05]                                       # small-λ → clean b^{-2}
    r_fine = bs.magnetic_deformation_ratio(6, 1.0, lam, b=1)[lam[0]]
    r_coarse = bs.magnetic_deformation_ratio(6, 1.0, lam, b=b)[lam[0]]
    ratio = r_coarse / r_fine
    assert ratio < 1.0                                 # irrelevant (shrinks)
    assert abs(ratio - b ** (-2.0)) < 0.05             # ≈ b^{-2}


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
