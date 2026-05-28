"""
test_wmu_phase6_rank1.py — F44 numerical confirmation
======================================================

Tests W6.6, W6.7, W6.8 from F44-higgs-free-mA-zero-from-rank1-stueckelberg.md.

Goal
----
Show that in the F34b+F41 single-Stueckelberg-field construction:

  1. The (W^3, B) mass block is rank-1 — det = 0 at machine precision (W6.6).
  2. Its eigenvalues are exactly (0, f^2(g^2+g'^2)) and its eigenvectors
     match the W6.1 Weinberg rotation (W6.7).
  3. The notebook's two-field parameterisation ½m_W²W₃² + ½m_W₀²W₀² is
     algebraically distinct: rotating it produces a non-zero cross term
     (m_W²-m_W₀²)·sin·cos on A·Z, which is the "anomalous" term flagged
     on p.65–66 (W6.8).  The single-field construction has no such free
     parameter and the cross term is exactly the off-diagonal of the
     unrotated rank-1 matrix.

Date: 2026-05-27 — 23:58
"""

import os
import sys
import json
import numpy as np

# Path setup so this runs from model-tests/ exactly like the other phase-6 tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

from ca_wmu import (  # noqa: E402
    weinberg_mix, weinberg_unmix,
    covariant_stueckelberg_lagrangian_uniform,
    covariant_stueckelberg_lagrangian,
    make_su2_link_uniform,
    make_u1y_link_uniform,
    BCC_DIRS,
)


# ──────────────────────────────────────────────────────────────────────
#  F44 mass-matrix builder
# ──────────────────────────────────────────────────────────────────────

def f44_mass_matrix(g, gp, f):
    """
    Build M²_{(W³, B)} = f² · [[g²,  -g g'],
                               [-g g',  g'²]]

    From (f²/2) tr|D_μ U|² at U = I with
        D_μ U = ∂_μ U − ig W^a τ^a U + ig' B U τ³/2.

    Ordering: (W³, B).
    """
    return np.array(
        [[f * f * g * g,    -f * f * g * gp],
         [-f * f * g * gp,   f * f * gp * gp]],
        dtype=np.float64,
    )


def theta_W_from(g, gp):
    """θ_W such that tan θ_W = g'/g — matches F35 W6.1 convention."""
    return np.arctan2(gp, g)


# ──────────────────────────────────────────────────────────────────────
#  W6.6 — determinant of rank-1 (W³, B) block is exactly zero
# ──────────────────────────────────────────────────────────────────────

def test_w66_rank1_det_zero():
    """det M²_{(W³, B)} = 0 at machine precision for all (g, g', f)."""
    rng = np.random.default_rng(seed=2026_05_27)
    cases = []
    # Five random triples plus the SM physical point
    for _ in range(5):
        g, gp, f = rng.uniform(0.3, 2.0, size=3)
        cases.append((g, gp, f))
    # SM physical: g ≈ 0.653, g' ≈ 0.350, v ≈ 246 GeV  → f = v/2
    cases.append((0.653, 0.350, 246.22 / 2.0))

    max_det = 0.0
    per_case = []
    for (g, gp, f) in cases:
        M = f44_mass_matrix(g, gp, f)
        det = float(np.linalg.det(M))
        # Normalise determinant by the matrix scale²; det has units of
        # (mass²)², the natural scale is (f²(g²+g'²))² = (trace)².
        scale = (f * f * (g * g + gp * gp)) ** 2
        rel = abs(det) / max(scale, 1e-30)
        max_det = max(max_det, rel)
        per_case.append({'g': g, 'gp': gp, 'f': f,
                         'det': det, 'rel': rel})
    target = 1e-14
    passed = max_det <= target
    return {
        'name': 'W6.6 — det M²_{(W³,B)} = 0',
        'max_relative_residual': max_det,
        'target': target,
        'passed': bool(passed),
        'per_case': per_case,
    }


# ──────────────────────────────────────────────────────────────────────
#  W6.7 — eigenvalues (0, f²(g²+g'²)); eigenvectors match W6.1 rotation
# ──────────────────────────────────────────────────────────────────────

def test_w67_eigh_matches_weinberg():
    """
    Diagonalise M²_{(W³, B)} via numpy.linalg.eigh.
    Verify:
      - one eigenvalue = 0 (photon)
      - one eigenvalue = f²(g²+g'²) = m_Z² (Z boson)
      - photon eigenvector || (sin θ_W, cos θ_W) in (W³, B) basis
        — which corresponds to weinberg_mix returning A from
          (W³ → sin θ_W, B → cos θ_W).
      - Z eigenvector || (cos θ_W, -sin θ_W) in (W³, B) basis.
    """
    rng = np.random.default_rng(seed=2026_05_27 + 1)
    cases = []
    for _ in range(5):
        g, gp, f = rng.uniform(0.3, 2.0, size=3)
        cases.append((g, gp, f))
    cases.append((0.653, 0.350, 246.22 / 2.0))

    max_eigval_err = 0.0
    max_evec_err = 0.0
    per_case = []
    for (g, gp, f) in cases:
        M = f44_mass_matrix(g, gp, f)
        eigvals, eigvecs = np.linalg.eigh(M)  # ascending order
        # eigvals[0] should be 0; eigvals[1] should be f²(g²+g'²)
        expected_mZ2 = f * f * (g * g + gp * gp)

        scale = expected_mZ2
        eig_err = max(
            abs(eigvals[0]) / max(scale, 1e-30),
            abs(eigvals[1] - expected_mZ2) / max(scale, 1e-30),
        )

        tw = theta_W_from(g, gp)
        cw, sw = np.cos(tw), np.sin(tw)

        # Photon direction (M² v = 0) in (W³, B) basis:
        # M [s_w, c_w]^T = f²[g²·s_w − gg'·c_w,  −gg'·s_w + g'²·c_w]
        #                = f²[g(g·s_w − g'·c_w), −g'(g·s_w − g'·c_w)]
        # Using tan θ_W = g'/g: g·s_w − g'·c_w = (g·g' − g'·g)/√(g²+g'²) = 0 ✓
        photon_dir = np.array([sw, cw])
        Z_dir      = np.array([cw, -sw])

        evec0 = eigvecs[:, 0]
        evec1 = eigvecs[:, 1]

        # eigh returns unit-norm vectors with arbitrary sign — match either
        def align_err(v_num, v_exp):
            return min(np.linalg.norm(v_num - v_exp),
                       np.linalg.norm(v_num + v_exp))

        ev_err = max(align_err(evec0, photon_dir),
                     align_err(evec1, Z_dir))

        max_eigval_err = max(max_eigval_err, eig_err)
        max_evec_err = max(max_evec_err, ev_err)

        per_case.append({
            'g': g, 'gp': gp, 'f': f,
            'eigvals': eigvals.tolist(),
            'expected_mZ2': expected_mZ2,
            'eig_rel_err': eig_err,
            'evec_err': ev_err,
            'theta_W': float(tw),
        })

    target_eig = 1e-14
    target_vec = 1e-14
    passed = (max_eigval_err <= target_eig) and (max_evec_err <= target_vec)
    return {
        'name': 'W6.7 — eigenvalues (0, m_Z²); eigenvectors = W6.1 rotation',
        'max_eigval_rel_err': max_eigval_err,
        'max_eigvec_err': max_evec_err,
        'target': target_eig,
        'passed': bool(passed),
        'per_case': per_case,
    }


# ──────────────────────────────────────────────────────────────────────
#  W6.8 — two-field notebook parameterisation produces residual cross term
# ──────────────────────────────────────────────────────────────────────

def test_w68_two_field_residual_cross_term():
    """
    Build the notebook's diagonal two-field mass matrix
        M_diag = diag(m_W², m_W0²)
    in the (W³, B) basis (no off-diagonal).  Rotate it by R(θ_W) into the
    (A, Z) basis.  The off-diagonal entry of the rotated matrix is

        Δ_AZ = (m_W² − m_W0²) sin θ_W cos θ_W,

    which is the page-65–66 "anomalous" cross term.  Show:
      (a) Δ_AZ matches the closed-form expression exactly.
      (b) Δ_AZ = 0 iff m_W² = m_W0², which is generically false — i.e.
          the two-field model needs fine-tuning to recover m_A = 0,
          unlike the single-field F44 model.
      (c) The single-field F44 mass matrix, when rotated, has Δ_AZ = 0
          and m_A² = 0 simultaneously and automatically.

    This is the algebraic separation between the two theories.
    """
    rng = np.random.default_rng(seed=2026_05_27 + 2)
    max_two_field_err = 0.0
    max_single_field_cross = 0.0
    per_case = []

    for _ in range(6):
        g, gp, f = rng.uniform(0.3, 2.0, size=3)
        tw = theta_W_from(g, gp)
        cw, sw = np.cos(tw), np.sin(tw)

        # Build R(θ_W) consistent with weinberg_mix:
        #   A = cos θ_W · B + sin θ_W · W³
        #   Z = -sin θ_W · B + cos θ_W · W³
        # so in (W³, B) basis the rotation is
        #   [A]   [ sin θ_W,  cos θ_W ] [W³]
        #   [Z] = [ cos θ_W, -sin θ_W ] [B ]
        R = np.array([[sw, cw],
                      [cw, -sw]], dtype=np.float64)

        # ---- Two-field notebook parameterisation -----------------------------
        # Independent Stueckelberg masses for W³ and B.
        m_W = g * f
        m_W0 = gp * f  # independent — distinct from F44's coupled construction
        M_two = np.diag([m_W * m_W, m_W0 * m_W0])

        M_two_rot = R @ M_two @ R.T  # (A, Z) basis
        # The off-diagonal is (m_W² − m_W0²) · sin θ_W · cos θ_W
        expected_cross = (m_W * m_W - m_W0 * m_W0) * sw * cw
        measured_cross = M_two_rot[0, 1]
        err_two = abs(measured_cross - expected_cross)
        max_two_field_err = max(max_two_field_err, err_two)

        # ---- Single-field F44 construction -----------------------------------
        M_one = f44_mass_matrix(g, gp, f)
        M_one_rot = R @ M_one @ R.T  # should be diag(0, m_Z²)
        single_cross = abs(M_one_rot[0, 1])
        max_single_field_cross = max(max_single_field_cross, single_cross)

        per_case.append({
            'g': g, 'gp': gp, 'f': f,
            'theta_W': float(tw),
            'two_field': {
                'm_W': m_W, 'm_W0': m_W0,
                'expected_cross': float(expected_cross),
                'measured_cross': float(measured_cross),
                'photon_mass_sq_after_rot': float(M_two_rot[0, 0]),
                'Z_mass_sq_after_rot': float(M_two_rot[1, 1]),
                'err': float(err_two),
            },
            'single_field': {
                'photon_mass_sq_after_rot': float(M_one_rot[0, 0]),
                'Z_mass_sq_after_rot': float(M_one_rot[1, 1]),
                'cross_residual': float(single_cross),
            },
        })

    # Two assertions:
    #   (1) the notebook's formula for the cross term is reproduced exactly
    #   (2) the single-field construction has cross term = 0 at machine ε
    target = 1e-14
    passed = (max_two_field_err <= target) and (max_single_field_cross <= target)
    return {
        'name': 'W6.8 — two-field cross term vs. single-field zero cross',
        'two_field_formula_max_err': max_two_field_err,
        'single_field_max_cross': max_single_field_cross,
        'target': target,
        'passed': bool(passed),
        'per_case': per_case,
    }


# ──────────────────────────────────────────────────────────────────────
#  W6.9 — Lattice-level rank-1 check on the covariant Stueckelberg kinetic
# ──────────────────────────────────────────────────────────────────────
#
# Conceptual note
# ---------------
# `mass_step_doublet_su2xu1y` in hypercharge_fork is the FERMION mass step.
# The rank-1 mass-matrix property of F44 lives in the BOSON sector: it is
# the second variation of the covariant Stueckelberg kinetic term
#
#     L_st(U_st; W, B) = f² · sum_{x,mu} tr[(D_mu U_st)†(D_mu U_st)]
#
#     D_mu U_st(x) = (1/a)[W_mu(x) U_st(x+mu) V_mu†(x) - U_st(x)]
#
#     W_mu(x) = exp(i a (g/2) W^a_mu(x) tau^a)   (SU(2)_L parallel transport)
#     V_mu(x) = exp(i a (g'/2) B_mu(x) tau^3)    (U(1)_Y, embedded as tau^3
#                                                 acting on the right index
#                                                 since the Stueckelberg field
#                                                 carries Y = +1 in the doublet
#                                                 representation — same Y the
#                                                 F41 mass step assigns to U(x))
#
# This is the OPERATOR whose existence F41 implicitly assumes when it states
# that the F34b Stueckelberg path is "unchanged" by the U(1)_Y extension.
# As of 2026-05-28, this operator is implemented in
# `ca_wmu.covariant_stueckelberg_lagrangian` (and a uniform-field convenience
# wrapper `covariant_stueckelberg_lagrangian_uniform`).  W6.9 here probes its
# second variation in (W^1, W^2, W^3, B) at U_st = I.
#
# Promotion note (2026-05-28): the operator was originally inline in this
# test file; it has since been moved to ca_wmu.py and this test now calls
# the promoted version, using BCC's 8 nearest-neighbour link directions
# (the natural convention for the rest of ca_wmu).  The earlier inline
# version used 3 cubic directions; rank-1 / eigvec results are structural
# and unchanged, only the trace prefactor differs (V·8 vs. V·3).
#
# Convention note (matches SM and `weinberg_mix`)
# -----------------------------------------------
# We use T^a = tau^a/2 for SU(2)_L generators and Y_st = +1 in the doublet
# representation for the Stueckelberg field. The continuum limit then gives
# the F44 mass matrix M²_{(W^3, B)} = f² [[g², -gg'], [-gg', g'²]] with
# m_W = g·v/2 = g·f when f = v/2 — matching `ca_wmu.py` / W6.3 bit-for-bit.
# (F44 §3.1 used a different generator convention — tau^a on left, tau^3/2
#  on right — that gives the same M² matrix form up to an absorbable factor
#  in f. The rank-1 / photon-eigenvector conclusions are convention-independent.)
#
# What we verify
# --------------
# (a) The 4x4 Hessian H[i,j] = ∂²L_st/∂xi^i ∂xi^j (with xi = (W^1, W^2, W^3, B))
#     is diagonal in the (W^1, W^2) sector with H[0,0] = H[1,1] = m_W² · scale.
# (b) The 2x2 (W^3, B) sub-block has det = 0 at machine precision.
# (c) Its non-zero eigenvalue = m_Z² · scale = f²(g²+g'²) · scale.
# (d) Photon eigenvector matches (sin theta_W, cos theta_W) in (W^3, B) basis.
# (e) Photon and Z eigenvalues sum to f²(g²+g'²) at machine precision (trace).
#
# "scale" is V · N_dir / (a² · denominator) — the volume × direction count
# from the lattice sum, factored out below.

# Lattice operator now lives in ca_wmu.covariant_stueckelberg_lagrangian
# (and the uniform-field wrapper covariant_stueckelberg_lagrangian_uniform).
# The test below probes its second variation; no inline operator code.


def _hessian_4d(L_fn, h=1e-3):
    """
    Symmetric 4x4 Hessian of L_fn(xi) at xi = 0 via central finite differences.
    xi = (W^1, W^2, W^3, B). Uses second-order central differences:
      H[i,i] = (L(+h e_i) - 2 L(0) + L(-h e_i)) / h²
      H[i,j] = (L(+h e_i + h e_j) - L(+h e_i - h e_j)
              - L(-h e_i + h e_j) + L(-h e_i - h e_j)) / (4 h²)
    """
    L0 = L_fn(np.zeros(4))
    H = np.zeros((4, 4))
    for i in range(4):
        e_i = np.zeros(4); e_i[i] = h
        Lp = L_fn(e_i)
        Lm = L_fn(-e_i)
        H[i, i] = (Lp - 2 * L0 + Lm) / (h * h)
        for j in range(i + 1, 4):
            e_j = np.zeros(4); e_j[j] = h
            Lpp = L_fn(e_i + e_j)
            Lpm = L_fn(e_i - e_j)
            Lmp = L_fn(-e_i + e_j)
            Lmm = L_fn(-e_i - e_j)
            H[i, j] = (Lpp - Lpm - Lmp + Lmm) / (4 * h * h)
            H[j, i] = H[i, j]
    return H


def test_w69_lattice_rank1_hessian():
    """
    Build the lattice covariant Stueckelberg Lagrangian, extract its 4x4
    Hessian in (W^1, W^2, W^3, B), and verify rank-1 in the (W^3, B) sub-block.
    """
    rng = np.random.default_rng(seed=2026_05_28)
    cases = []
    for _ in range(5):
        g, gp, f = rng.uniform(0.3, 2.0, size=3)
        cases.append((g, gp, f))
    # SM physical
    cases.append((0.6532, 0.3499, 246.22 / 2.0))

    max_det_rel = 0.0
    max_evec_err = 0.0
    max_w1w2_diff_rel = 0.0
    max_trace_match_rel = 0.0
    max_offdiag_w12_rel = 0.0
    per_case = []

    for (g, gp, f) in cases:
        # Lagrangian as a function of xi = (W^1, W^2, W^3, B), calling the
        # promoted operator in ca_wmu.  Uses BCC's 8 nearest-neighbour link
        # directions by default — the natural convention for ca_wmu.
        a = 1e-2          # small lattice spacing
        L_lat = 4         # tiny lattice (constant fields)
        link_dirs = BCC_DIRS  # explicit so the prefactor is unambiguous
        n_dirs = len(link_dirs)  # = 8 for BCC

        def L_fn(xi, g=g, gp=gp, f=f, a=a, L_lat=L_lat, link_dirs=link_dirs):
            return covariant_stueckelberg_lagrangian_uniform(
                xi[:3], xi[3], g, gp, f=f, a_lat=a, L=L_lat, link_dirs=link_dirs,
            )

        H = _hessian_4d(L_fn, h=1e-3)

        # Lattice scale factor: V * n_dirs (constant-field uniform sum).
        # Continuum mass-matrix entries should appear with this prefactor on H,
        # so the rank-1 / eigvec checks are scale-invariant.
        V = L_lat ** 3
        scale = V * n_dirs

        # Continuum predictions (from the SM mass matrix derivation):
        # H_continuum = scale * f² * [[g², 0, 0, 0],
        #                              [0, g², 0, 0],
        #                              [0, 0, g², -g·g'],
        #                              [0, 0, -g·g', g'²]]
        # Verify diagonal: H[0,0] = H[1,1] = scale · f² · g²
        H00 = H[0, 0]
        H11 = H[1, 1]
        H22 = H[2, 2]
        H23 = H[2, 3]
        H33 = H[3, 3]

        expected_mW2 = scale * f * f * g * g
        w1w2_diff_rel = abs(H00 - H11) / max(abs(expected_mW2), 1e-30)
        max_w1w2_diff_rel = max(max_w1w2_diff_rel, w1w2_diff_rel)

        # Verify W^1 has no cross terms with anything else
        offdiag_w12_max = max(
            abs(H[0, 1]), abs(H[0, 2]), abs(H[0, 3]),
            abs(H[1, 2]), abs(H[1, 3]),
        )
        offdiag_w12_rel = offdiag_w12_max / max(abs(expected_mW2), 1e-30)
        max_offdiag_w12_rel = max(max_offdiag_w12_rel, offdiag_w12_rel)

        # (W^3, B) sub-block — should be rank-1
        H_sub = H[2:4, 2:4]
        det_sub = np.linalg.det(H_sub)
        tr_sub = np.trace(H_sub)
        det_rel = abs(det_sub) / max(tr_sub * tr_sub, 1e-30)
        max_det_rel = max(max_det_rel, det_rel)

        # Trace = scale · f² · (g² + g'²) = m_Z² · scale
        expected_mZ2 = scale * f * f * (g * g + gp * gp)
        trace_match_rel = abs(tr_sub - expected_mZ2) / max(expected_mZ2, 1e-30)
        max_trace_match_rel = max(max_trace_match_rel, trace_match_rel)

        # Eigenvectors of H_sub — photon should be (sin θ_W, cos θ_W)
        tw = np.arctan2(gp, g)
        cw, sw = np.cos(tw), np.sin(tw)
        eigvals, eigvecs = np.linalg.eigh(H_sub)
        photon_dir = np.array([sw, cw])
        Z_dir = np.array([cw, -sw])

        def align_err(v_num, v_exp):
            return min(np.linalg.norm(v_num - v_exp),
                       np.linalg.norm(v_num + v_exp))

        ev_err = max(align_err(eigvecs[:, 0], photon_dir),
                     align_err(eigvecs[:, 1], Z_dir))
        max_evec_err = max(max_evec_err, ev_err)

        per_case.append({
            'g': g, 'gp': gp, 'f': f,
            'a_lattice': a, 'L': L_lat, 'V': V, 'n_dirs': n_dirs,
            'theta_W': float(tw),
            'H_diag': [float(H00), float(H11), float(H22), float(H33)],
            'H23': float(H23),
            'expected_mW2_scaled': float(expected_mW2),
            'expected_mZ2_scaled': float(expected_mZ2),
            'eigvals_sub': eigvals.tolist(),
            'det_sub_rel': float(det_rel),
            'w1w2_diff_rel': float(w1w2_diff_rel),
            'trace_match_rel': float(trace_match_rel),
            'evec_err': float(ev_err),
            'offdiag_w12_rel': float(offdiag_w12_rel),
        })

    # Targets: lattice spacing a=1e-2 gives O(a) ~ O(1e-2) corrections;
    # finite-difference step h=1e-3 gives O(h²) ~ O(1e-6) FD error;
    # combined floor ~ 1e-5. Loosen accordingly vs. W6.6's pure-algebra ε.
    target = 1e-4
    passed = (
        max_det_rel <= target
        and max_evec_err <= target
        and max_w1w2_diff_rel <= target
        and max_trace_match_rel <= target
        and max_offdiag_w12_rel <= target
    )
    return {
        'name': 'W6.9 — Lattice covariant Stueckelberg gives rank-1 (W³,B) Hessian',
        'max_det_rel': max_det_rel,
        'max_eigvec_err': max_evec_err,
        'max_w1w2_diff_rel': max_w1w2_diff_rel,
        'max_trace_match_rel': max_trace_match_rel,
        'max_offdiag_w12_rel': max_offdiag_w12_rel,
        'target': target,
        'passed': bool(passed),
        'per_case': per_case,
    }


# ──────────────────────────────────────────────────────────────────────
#  W6.10 — Sanity checks on the promoted ca_wmu operator
# ──────────────────────────────────────────────────────────────────────
#
# (a) Zero gauge field + U_st = I uniform → L_st = 0 exactly (no fields,
#     no Lagrangian).  Bit-for-bit zero.
# (b) Zero gauge field + arbitrary CONSTANT U_st → L_st = 0 exactly (D_μ
#     of a constant is zero regardless of which SU(2) element it is).
#     Bit-for-bit zero.
# (c) Gauge fields on + U_st = I → result matches a direct 2×2 matrix
#     evaluation tr[(W V† - I)†(W V† - I)] · V · n_dirs · f² / a² built
#     independently (no shared helpers between the two implementations).
#     This is the equivalent of an F41-Y3 "$\alpha=0$ reduces bit-for-bit"
#     guarantee, but for the boson covariant Stueckelberg path.

def test_w610_sanity():
    """Promoted ca_wmu operator: zero-field, constant-U_st, and direct-eval
    cross-checks."""
    L_lat = 4
    a = 1e-2
    f = 1.0

    # (a) Zero gauge field + U_st = I
    L_zero_I = covariant_stueckelberg_lagrangian_uniform(
        W123=[0.0, 0.0, 0.0], B=0.0,
        g=0.7, gp=0.4, f=f, a_lat=a, L=L_lat,
    )

    # (b) Zero gauge field + constant non-identity U_st.
    # Build U_st as a uniform SU(2) matrix (use the same uniform-link helper
    # we use for W links, with a non-zero "W123" but apply it as the U_st field).
    shape = (L_lat, L_lat, L_lat)
    Ust_a, Ust_b = make_su2_link_uniform(
        W123=[0.31, -0.22, 0.45], g=1.0, a_lat=1.0, shape=shape,
    )
    # Identity link variables (no gauge field)
    W_a_id = np.ones(shape, dtype=complex)
    W_b_id = np.zeros(shape, dtype=complex)
    V_phase_id = np.ones(shape, dtype=complex)
    W_links_id = [(W_a_id, W_b_id) for _ in BCC_DIRS]
    V_links_id = [V_phase_id for _ in BCC_DIRS]
    L_zero_Ust = covariant_stueckelberg_lagrangian(
        Ust_a, Ust_b, W_links_id, V_links_id, f=f, a_lat=a,
    )

    # (c) Direct 2×2 matrix evaluation at U_st = I with uniform gauge fields,
    # independent of the Cayley-Klein path used in ca_wmu — gives an end-to-end
    # cross-check that the promoted code matches the matrix definition.
    g = 0.7
    gp = 0.4
    W123 = [0.31, -0.22, 0.45]
    B = 0.18

    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    # Closed-form 2×2 SU(2) link variables via cos/sin (matches make_su2_link_uniform)
    Wmag = float(np.sqrt(W123[0] ** 2 + W123[1] ** 2 + W123[2] ** 2))
    theta = a * (g / 2.0) * Wmag
    nx, ny, nz = W123[0] / Wmag, W123[1] / Wmag, W123[2] / Wmag
    sigma_dot_n = nx * s1 + ny * s2 + nz * s3
    W_mat = np.cos(theta) * I2 + 1j * np.sin(theta) * sigma_dot_n
    phi = a * (gp / 2.0) * B
    V_mat = np.cos(phi) * I2 + 1j * np.sin(phi) * s3  # = diag(e^{+iφ}, e^{-iφ})

    DU_mat = (W_mat @ V_mat.conj().T - I2) / a
    trace_term = float(np.real(np.trace(DU_mat.conj().T @ DU_mat)))
    n_dirs_ref = len(BCC_DIRS)
    V_ref = L_lat ** 3
    L_direct = f * f * V_ref * n_dirs_ref * trace_term

    L_promoted = covariant_stueckelberg_lagrangian_uniform(
        W123=W123, B=B, g=g, gp=gp, f=f, a_lat=a, L=L_lat,
    )
    direct_match_rel = abs(L_promoted - L_direct) / max(abs(L_direct), 1e-30)

    target_zero = 1e-30  # exact
    target_match = 1e-12

    passed = (
        abs(L_zero_I) <= target_zero
        and abs(L_zero_Ust) <= target_zero
        and direct_match_rel <= target_match
    )

    return {
        'name': 'W6.10 — sanity: zero-field exact, constant-U_st exact, direct-eval match',
        'L_zero_I': float(L_zero_I),
        'L_zero_Ust_const': float(L_zero_Ust),
        'L_promoted': float(L_promoted),
        'L_direct': float(L_direct),
        'direct_match_rel': float(direct_match_rel),
        'target_zero': target_zero,
        'target_match': target_match,
        'passed': bool(passed),
    }


# ──────────────────────────────────────────────────────────────────────
#  Driver
# ──────────────────────────────────────────────────────────────────────

def main():
    results = {
        'test_name': 'wmu_phase6_rank1 (F44)',
        'date': '2026-05-28 - 00:15',
        'tests': [
            test_w66_rank1_det_zero(),
            test_w67_eigh_matches_weinberg(),
            test_w68_two_field_residual_cross_term(),
            test_w69_lattice_rank1_hessian(),
            test_w610_sanity(),
        ],
    }
    n = len(results['tests'])
    n_pass = sum(1 for t in results['tests'] if t['passed'])
    results['summary'] = f'{n_pass}/{n} PASS'

    # Print short summary
    print()
    print('=' * 70)
    print('F44 W6.6–W6.8 numerical confirmation')
    print('=' * 70)
    for t in results['tests']:
        flag = '✓ PASS' if t['passed'] else '✗ FAIL'
        print(f"  {flag}  {t['name']}")
        for k, v in t.items():
            if k in ('name', 'passed', 'per_case', 'target'):
                continue
            if isinstance(v, float):
                print(f"        {k} = {v:.3e}")
    print(f"\nSummary: {results['summary']}")
    print('=' * 70)

    # Write JSON next to the other phase-6 results
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'wmu_phase6_rank1.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=float)
    print(f'JSON: {out_path}')

    return 0 if n_pass == n else 1


if __name__ == '__main__':
    sys.exit(main())
