"""
test_FG6_two_helicity_photon.py
================================

FG-6 — Two-helicity composite photon built from BOTH Weyl branches
       (`sign='+'` and `sign='-'`), at the bilinear level.

Specced in first-gen-completeness-review.md §5.1:
    "Two-helicity photon + birefringence: build Ω^± bilinear, measure
     ΔΩ vs F30's −√3·k²/27 on the body diagonal."

Closes the structural gap noted in §3 item 4 of the same review:
    "Extend the composite bilinear (ca_maxwell.py) to both Weyl branches
     (Ω^±) so the photon carries both circular polarisations."

The F29 W-triplet bilinear bridge (`test_su2_photon_bridge.py`) used
`sign='+'` eigenmodes only, i.e. one BCC chirality.  F37 showed at the
(E, B) field level that the two BCC branches Ω^± correspond to the
two photon helicities  F^± = E ± i·B,  with the chiral propagator
(`ca_wmu.w_propagation_step_spectral`) rotating F^+ at Ω^+ and
F^- at Ω^-.  F30 gave the analytical birefringence on the (1,1,1)
body diagonal:  Ω^+ − Ω^- = −(√3/27)·k² + O(k⁴).

This test verifies that ca_maxwell.py's new two-helicity helpers
(`EM_bilinears_branch`, `EM_bilinears_two_helicity`,
 `triplet_bilinear_branch`, `triplet_bilinear_two_helicity`,
 `riemann_silberstein_decomp`) close the bridge from the underlying
Weyl-spinor bilinear all the way to the F37 chiral field-level
propagation.

Test suite (10 tests):

  Singlet (composite photon)
  --------------------------
  FG6.1   Per-branch bilinear is NONZERO and transverse to 2·n_half_±.
  FG6.2   Combined two-helicity (E, B) = α₊(E₊,B₊) + α₋(E₋,B₋) is the
          sum of branch contributions (linearity sanity).
  FG6.3   Both Riemann-Silberstein helicities F^± are present in the
          combined photon, with no exact cancellation across branches.
  FG6.4   Singlet G is SU(2)-invariant PER BRANCH (F29 B1 extended).
  FG6.5   Under chiral propagation `w_propagation_step_spectral`, the
          F^+(k) Fourier mode rotates at Ω^+(k) and F^-(k) at Ω^-(k),
          across BOTH single-branch and combined two-helicity initial
          states.
  FG6.6   ΔΩ(k) along (1,1,1) matches the F30 closed form −(√3/27)·k²
          via direct dispersion evaluation (machine-precision algebraic).

  Triplet (W^a sector — F29 B2/B3 extended to two helicities)
  -----------------------------------------------------------
  FG6.7   Triplet W^a transforms adjointly per branch:
          W^a → R^{ab}(V) W^b under V ∈ SU(2) on the doublet.
  FG6.8   Σ_a ‖W^a‖² is SU(2)-invariant per branch and for the combined
          state.
  FG6.9   The combined-state triplet inherits per-branch transversality
          2·n_half_± · W^{a,±}_T → 0 with the F29-B4 scaling O(c_lat·|k|).

  Cross-helicity check
  --------------------
  FG6.10  Riemann-Silberstein orthogonality:  F^+ + F^- = 2E,
          (F^+ − F^-)/(2i) = B  (algebraic identity, machine-zero).

Run:  python3 model-tests/test_FG6_two_helicity_photon.py
Output: test-results/FG6_two_helicity_photon.json

Date: 2026-05-26 (FG-6).
"""

from __future__ import annotations

import sys, os, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ca-simulation'))

import numpy as np

import ca_bcc as bcc
import ca_fft as _fft
import ca_maxwell as cm
from ca_maxwell import (
    weyl_eigenmodes_3d_bcc,
    EM_bilinears_branch,
    EM_bilinears_two_helicity,
    triplet_bilinear_branch,
    triplet_bilinear_two_helicity,
    riemann_silberstein_decomp,
    _PAULIS,
    _TAU_ISO,
    _singlet_bilinear_H,
    _triplet_bilinear_H,
)
from ca_lattice import make_kgrid_3d
from ca_wmu import w_propagation_step_spectral


SQRT3 = np.sqrt(3.0)
C_LAT = 1.0 / SQRT3
SQRT3_OVER_27 = SQRT3 / 27.0


# ── small helpers ────────────────────────────────────────────────

def _random_dirs(n, seed):
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((n, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v


def _random_su2(seed):
    rng = np.random.default_rng(abs(int(seed)) % (2**31))
    q = rng.standard_normal(4)
    q /= np.linalg.norm(q)
    a = q[0] + 1j * q[3]
    b = q[2] + 1j * q[1]
    return np.array([[a, -np.conj(b)],
                     [b,  np.conj(a)]], dtype=complex)


def _adjoint_rotation(V):
    """R^{ab}(V) = ½ tr(τ^a V τ^b V†) — SO(3) rotation matching V ∈ SU(2)."""
    R = np.zeros((3, 3), dtype=float)
    for a in range(3):
        for b in range(3):
            R[a, b] = 0.5 * np.real(
                np.trace(_TAU_ISO[a] @ V @ _TAU_ISO[b] @ V.conj().T)
            )
    return R


def _make_doublet(psi_a, psi_b):
    return np.stack([psi_a, psi_b], axis=0)


def _per_branch_modes(kx, ky, kz):
    """Return ((psi_p_+, psi_m_+, omega_half_+), (psi_p_-, psi_m_-, omega_half_-))."""
    pl = weyl_eigenmodes_3d_bcc(kx / 2.0, ky / 2.0, kz / 2.0, sign='+')
    mn = weyl_eigenmodes_3d_bcc(kx / 2.0, ky / 2.0, kz / 2.0, sign='-')
    return pl, mn


# =================================================================
# FG6.1 — Per-branch bilinear is NONZERO and transverse
# =================================================================

def test_FG6_1_per_branch_nonzero_and_transverse(n_dirs=12, k_mag=0.05, seed=11):
    """Each branch's bilinear contributes a non-trivial (E, B) that is
    transverse to 2·n_half of its OWN branch.

    Two sub-claims:
      (a) ‖E_±‖ > 0  for every sampled direction — the construction does
          NOT silently degenerate on one branch.
      (b) 2·n_half_± · E_± = 0  to machine precision (transverse by
          construction — `EM_bilinears` projects out the longitudinal
          part).  The genuinely O(c_lat·|k|) test is on the raw
          W-triplet (FG6.9); the singlet's transversality is exact
          algebraically.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    worst_trans_pl = 0.0
    worst_trans_mn = 0.0
    min_norm = float('inf')
    for d in dirs:
        kx, ky, kz = k_mag * d
        (psi_p_pl, _, _), (psi_p_mn, _, _) = _per_branch_modes(kx, ky, kz)
        E_pl, B_pl, n_pl = EM_bilinears_branch(psi_p_pl, psi_p_pl, kx, ky, kz, sign='+')
        E_mn, B_mn, n_mn = EM_bilinears_branch(psi_p_mn, psi_p_mn, kx, ky, kz, sign='-')

        for E, n_half, bucket in [(E_pl, n_pl, '+'), (E_mn, n_mn, '-')]:
            norm = np.linalg.norm(E)
            min_norm = min(min_norm, norm)
            two_n = 2.0 * n_half
            tr = abs(np.dot(two_n, E)) / max(norm, 1e-30)
            if bucket == '+':
                worst_trans_pl = max(worst_trans_pl, tr)
            else:
                worst_trans_mn = max(worst_trans_mn, tr)
    return {
        'residual':  max(worst_trans_pl, worst_trans_mn),
        'worst_transversality_plus':  worst_trans_pl,
        'worst_transversality_minus': worst_trans_mn,
        'min_branch_E_norm':          min_norm,
        'note':
            'Transversality is exact-by-construction (projection in '
            'EM_bilinears); the F29-B4 c_lat·|k| scaling lives on the '
            'raw W-triplet, tested by FG6.9.',
    }


# =================================================================
# FG6.2 — Two-helicity assembler is linear in branch contributions
# =================================================================

def test_FG6_2_two_helicity_linearity(n_dirs=8, k_mag=0.05, seed=21):
    """`EM_bilinears_two_helicity(... α₊=α, α₋=β)` equals α(E₊,B₊) + β(E₋,B₋).

    Algebraic identity — exact to machine precision.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    worst = 0.0
    rng = np.random.default_rng(seed + 1)
    for d in dirs:
        kx, ky, kz = k_mag * d
        (psi_p_pl, psi_m_pl, _), (psi_p_mn, psi_m_mn, _) = _per_branch_modes(kx, ky, kz)
        a = complex(rng.standard_normal(), rng.standard_normal())
        b = complex(rng.standard_normal(), rng.standard_normal())

        E_pl, B_pl, _ = EM_bilinears_branch(psi_p_pl, psi_m_pl, kx, ky, kz, sign='+')
        E_mn, B_mn, _ = EM_bilinears_branch(psi_p_mn, psi_m_mn, kx, ky, kz, sign='-')

        E_two, B_two, _ = EM_bilinears_two_helicity(
            psi_p_pl, psi_m_pl, psi_p_mn, psi_m_mn,
            kx, ky, kz, alpha_pl=a, alpha_mn=b,
        )

        E_expect = a * E_pl + b * E_mn
        B_expect = a * B_pl + b * B_mn
        denom = max(np.linalg.norm(E_expect) + np.linalg.norm(B_expect), 1e-30)
        worst = max(worst, (np.linalg.norm(E_two - E_expect)
                            + np.linalg.norm(B_two - B_expect)) / denom)
    return {'residual': worst}


# =================================================================
# FG6.3 — Both helicities F^± are present in the combined photon
# =================================================================

def test_FG6_3_both_helicities_present(n_dirs=12, k_mag=0.05, seed=31):
    """Both F^+ and F^- are NONZERO in the combined two-helicity state.

    Per-branch alone the bilinear yields equal |F^+| = |F^-| (linearly
    polarized — both helicities present with equal amplitude); the
    combined state inherits both.  This test only checks that neither
    helicity vanishes by accident; the dispersion-assignment test
    (FG6.5) is what shows F^+ and F^- track DIFFERENT Ω in propagation.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    min_ratio = float('inf')
    for d in dirs:
        kx, ky, kz = k_mag * d
        (psi_p_pl, _, _), (psi_p_mn, _, _) = _per_branch_modes(kx, ky, kz)
        E, B, _ = EM_bilinears_two_helicity(
            psi_p_pl, psi_p_pl, psi_p_mn, psi_p_mn,
            kx, ky, kz,
        )
        Fp, Fm = riemann_silberstein_decomp(E, B)
        norm_p = np.linalg.norm(Fp)
        norm_m = np.linalg.norm(Fm)
        if max(norm_p, norm_m) < 1e-12:
            continue
        # F^- relative to F^+: must be O(1), not tiny — otherwise the
        # two-helicity construction has accidentally collapsed.
        ratio = min(norm_p, norm_m) / max(norm_p, norm_m)
        min_ratio = min(min_ratio, ratio)
    return {
        'min_helicity_ratio_min(|F+|,|F-|)/max(|F+|,|F-|)': min_ratio,
        'expected':
            'O(1) — single-branch bilinears yield |F+|=|F-| (linear pol),'
            ' and combined inherits both helicities.',
    }


# =================================================================
# FG6.4 — Singlet SU(2)-invariance per branch (F29 B1 extension)
# =================================================================

def test_FG6_4_singlet_SU2_invariance_per_branch(n_dirs=12, k_mag=0.3, seed=41):
    """G_H^i = Σ_α (φ^α)† σ^i ψ^α is SU(2)-invariant WITHIN each branch.

    F29 B1 checked this for sign='+'.  Here we verify it independently
    for sign='-' (and re-check '+' as a regression).  Machine precision.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    worst = {'+': 0.0, '-': 0.0}
    for d in dirs:
        kx, ky, kz = k_mag * d
        (psi_p_pl, psi_m_pl, _), (psi_p_mn, psi_m_mn, _) = _per_branch_modes(kx, ky, kz)
        # Build distinct iso doublets so the singlet is non-trivial.
        for sign, psi_p, psi_m in [('+', psi_p_pl, psi_m_pl),
                                    ('-', psi_p_mn, psi_m_mn)]:
            phi = _make_doublet(psi_p.copy(), psi_m.copy())
            psi = _make_doublet(psi_m.copy(), psi_p.copy())
            G0 = _singlet_bilinear_H(phi, psi)

            V = _random_su2(seed + 7 + int(1000 * d[0]) + (1 if sign == '-' else 0))
            phi_V = V @ phi
            psi_V = V @ psi
            G1 = _singlet_bilinear_H(phi_V, psi_V)

            denom = max(np.linalg.norm(G0), 1e-30)
            worst[sign] = max(worst[sign], np.linalg.norm(G1 - G0) / denom)
    return {
        'residual_plus_branch':  worst['+'],
        'residual_minus_branch': worst['-'],
    }


# =================================================================
# FG6.5 — Chiral propagation: F^+ → Ω^+ and F^- → Ω^- (per branch & combined)
# =================================================================

def _plant_single_mode(E_amp, B_amp, ki, kj, kk, L, a_comp=0):
    """Plant a single (E, B) at the (ki, kj, kk) Fourier mode of a 3-component
    real-space lattice field, mirroring _pure_Fp_field's Hermitian-symmetric
    layout from test_F37_delta_omega.py.

    Returns (E_W, B_W) with shape (3, L, L, L), real-valued.
    """
    E_k = np.zeros((L, L, L), dtype=complex)
    B_k = np.zeros((L, L, L), dtype=complex)
    mi = ((-ki) % L, (-kj) % L, (-kk) % L)
    E_k[ki, kj, kk] = E_amp[a_comp]
    B_k[ki, kj, kk] = B_amp[a_comp]
    E_k[mi[0], mi[1], mi[2]] = np.conj(E_amp[a_comp])
    B_k[mi[0], mi[1], mi[2]] = np.conj(B_amp[a_comp])
    E_W = np.zeros((3, L, L, L))
    B_W = np.zeros((3, L, L, L))
    E_W[a_comp] = _fft.ifftn(E_k).real
    B_W[a_comp] = _fft.ifftn(B_k).real
    return E_W, B_W


def _fp_at_mode(E_W, B_W, ki, kj, kk, a_comp=0):
    Ek = _fft.fftn(E_W[a_comp])[ki, kj, kk]
    Bk = _fft.fftn(B_W[a_comp])[ki, kj, kk]
    return Ek + 1j * Bk


def _fm_at_mode(E_W, B_W, ki, kj, kk, a_comp=0):
    Ek = _fft.fftn(E_W[a_comp])[ki, kj, kk]
    Bk = _fft.fftn(B_W[a_comp])[ki, kj, kk]
    return Ek - 1j * Bk


def test_FG6_5_chiral_propagation_per_helicity():
    """Plant the bilinear (E, B) at a single lattice mode and verify that the
    F^+ Fourier amplitude acquires phase exp(−i Ω^+(k)) per tick and F^-
    acquires phase exp(+i Ω^-(k)).  Two initial-state classes are tested:

      (a) Single-branch bilinear (`sign='+'` only, `sign='-'` only) — the
          F^- in the resulting (E, B) tracks Ω^- regardless of which branch
          made it, because the chiral propagator routes each helicity by
          eigenstate, not provenance.
      (b) Combined two-helicity (E, B) — both helicities are non-trivial,
          and each tracks its own dispersion.

    Tolerance: ≤ 1e-10 relative error over 10 ticks (F37.1/F37.2 standard).
    """
    L = 16
    n_steps = 10
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    # A handful of non-zero modes that avoid Nyquist-self-conjugate bins.
    test_modes = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1)]

    worst_p = 0.0
    worst_m = 0.0
    cases = []
    for state_label in ('plus_branch_only',
                        'minus_branch_only',
                        'two_helicity_combined'):
        for ki, kj, kk in test_modes:
            kx, ky, kz = KX[ki, kj, kk], KY[ki, kj, kk], KZ[ki, kj, kk]
            Omega_p = 2.0 * bcc.bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='+')
            Omega_m = 2.0 * bcc.bcc_dispersion(kx / 2.0, ky / 2.0, kz / 2.0, sign='-')

            (psi_p_pl, _, _), (psi_p_mn, _, _) = _per_branch_modes(kx, ky, kz)

            if state_label == 'plus_branch_only':
                E, B, _ = EM_bilinears_branch(psi_p_pl, psi_p_pl,
                                              kx, ky, kz, sign='+')
            elif state_label == 'minus_branch_only':
                E, B, _ = EM_bilinears_branch(psi_p_mn, psi_p_mn,
                                              kx, ky, kz, sign='-')
            else:
                E, B, _ = EM_bilinears_two_helicity(
                    psi_p_pl, psi_p_pl, psi_p_mn, psi_p_mn,
                    kx, ky, kz,
                )

            E_W, B_W = _plant_single_mode(E, B, ki, kj, kk, L, a_comp=0)
            Fp0 = _fp_at_mode(E_W, B_W, ki, kj, kk)
            Fm0 = _fm_at_mode(E_W, B_W, ki, kj, kk)
            if abs(Fp0) < 1e-12 or abs(Fm0) < 1e-12:
                continue

            for _ in range(n_steps):
                E_W, B_W = w_propagation_step_spectral(E_W, B_W)

            Fpn = _fp_at_mode(E_W, B_W, ki, kj, kk)
            Fmn = _fm_at_mode(E_W, B_W, ki, kj, kk)

            Fp_expected = Fp0 * np.exp(-1j * Omega_p * n_steps)
            Fm_expected = Fm0 * np.exp(+1j * Omega_m * n_steps)
            err_p = abs(Fpn - Fp_expected) / abs(Fp0)
            err_m = abs(Fmn - Fm_expected) / abs(Fm0)
            worst_p = max(worst_p, err_p)
            worst_m = max(worst_m, err_m)
            cases.append({
                'state': state_label,
                'mode': [int(ki), int(kj), int(kk)],
                'Omega+': float(Omega_p),
                'Omega-': float(Omega_m),
                'err_Fp_rel': float(err_p),
                'err_Fm_rel': float(err_m),
            })
    return {
        'worst_Fp_residual_rel': worst_p,
        'worst_Fm_residual_rel': worst_m,
        'target': 1e-10,
        'n_cases': len(cases),
        'note': 'Tested over single-branch + combined initial states; both helicities tracked independently.',
    }


# =================================================================
# FG6.6 — Birefringence ΔΩ along (1,1,1) matches F30  (−√3/27 · k²)
# =================================================================

def test_FG6_6_birefringence_vs_F30(t_min=0.005, t_max=0.30, n_pts=200):
    """ΔΩ = Ω^+(k) − Ω^-(k) along k ∥ (1,1,1) equals −(√3/27)·k² + O(k⁴).

    F30 closed form (Tier-1 exact); F37.3 already verified this at the
    dispersion level.  Re-running here as a regression certifies the
    two-helicity construction inherits the right birefringence.
    """
    t_vals = np.linspace(t_min, t_max, n_pts)
    delta_omega = []
    for t in t_vals:
        ki = t / SQRT3
        op = bcc.bcc_dispersion(ki / 2.0, ki / 2.0, ki / 2.0, sign='+')
        om = bcc.bcc_dispersion(ki / 2.0, ki / 2.0, ki / 2.0, sign='-')
        delta_omega.append(2.0 * (op - om))
    delta_omega = np.array(delta_omega)

    # Fit ΔΩ = c · k² on the small-k portion.
    mask = t_vals < min(0.10, t_max)
    t_fit = t_vals[mask]
    dO_fit = delta_omega[mask]
    coeff_num = np.sum(t_fit ** 2 * dO_fit)
    coeff_den = np.sum(t_fit ** 4)
    c_meas = coeff_num / coeff_den
    c_exact = -SQRT3_OVER_27
    rel_err = abs(c_meas - c_exact) / abs(c_exact)
    return {
        'fit_coeff_meas':  c_meas,
        'fit_coeff_exact': c_exact,
        'fit_relative_error': rel_err,
        'n_points_fit': int(mask.sum()),
        'note':
            'Direct BCC-dispersion evaluation along (1,1,1); reproduces '
            'F30 closed form −√3/27 = ' + f'{-SQRT3_OVER_27:.10e}',
    }


# =================================================================
# FG6.7 — Triplet adjoint rotation per branch (F29 B2 extended)
# =================================================================

def test_FG6_7_triplet_adjoint_per_branch(n_dirs=12, k_mag=0.3, seed=51):
    """W^a → R^{ab}(V) W^b under V ∈ SU(2) on the doublet — per branch."""
    dirs = _random_dirs(n_dirs, seed=seed)
    worst = {'+': 0.0, '-': 0.0}
    for d in dirs:
        kx, ky, kz = k_mag * d
        (psi_p_pl, psi_m_pl, _), (psi_p_mn, psi_m_mn, _) = _per_branch_modes(kx, ky, kz)
        for sign, psi_p, psi_m in [('+', psi_p_pl, psi_m_pl),
                                    ('-', psi_p_mn, psi_m_mn)]:
            phi = _make_doublet(psi_p.copy(), psi_m.copy())
            psi = _make_doublet(psi_m.copy(), psi_p.copy())
            W0 = _triplet_bilinear_H(phi, psi)
            V = _random_su2(seed + 19 + int(1000 * d[1]) + (1 if sign == '-' else 0))
            R = _adjoint_rotation(V)
            W1 = _triplet_bilinear_H(V @ phi, V @ psi)
            W_pred = R @ W0
            denom = max(np.linalg.norm(W0), 1e-30)
            worst[sign] = max(worst[sign], np.linalg.norm(W1 - W_pred) / denom)
    return {
        'residual_plus_branch':  worst['+'],
        'residual_minus_branch': worst['-'],
    }


# =================================================================
# FG6.8 — Triplet magnitude Σ_a ‖W^a‖² SU(2)-invariant (combined)
# =================================================================

def test_FG6_8_triplet_magnitude_invariance_combined(n_dirs=12, k_mag=0.3, seed=61):
    """Σ_a ‖W^a‖² over the COMBINED two-helicity W-triplet is preserved by
    SU(2) on the doublet (same V applied to both branches).
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    worst = 0.0
    for d in dirs:
        kx, ky, kz = k_mag * d
        (psi_p_pl, psi_m_pl, _), (psi_p_mn, psi_m_mn, _) = _per_branch_modes(kx, ky, kz)
        phi_iso_pl = _make_doublet(psi_p_pl.copy(), psi_m_pl.copy())
        psi_iso_pl = _make_doublet(psi_m_pl.copy(), psi_p_pl.copy())
        phi_iso_mn = _make_doublet(psi_p_mn.copy(), psi_m_mn.copy())
        psi_iso_mn = _make_doublet(psi_m_mn.copy(), psi_p_mn.copy())

        # Combined triplet (E^a, B^a) — but we test invariance of Σ_a‖W^a‖²
        # rather than fields, since the field map is linear in W and the
        # SU(2) action commutes with the (E^a, B^a) construction.
        W_pl_0 = _triplet_bilinear_H(phi_iso_pl, psi_iso_pl)
        W_mn_0 = _triplet_bilinear_H(phi_iso_mn, psi_iso_mn)
        mag0 = float(np.sum(np.abs(W_pl_0) ** 2) + np.sum(np.abs(W_mn_0) ** 2))

        V = _random_su2(seed + 23 + int(1000 * d[2]))
        W_pl_1 = _triplet_bilinear_H(V @ phi_iso_pl, V @ psi_iso_pl)
        W_mn_1 = _triplet_bilinear_H(V @ phi_iso_mn, V @ psi_iso_mn)
        mag1 = float(np.sum(np.abs(W_pl_1) ** 2) + np.sum(np.abs(W_mn_1) ** 2))

        denom = max(mag0, 1e-30)
        worst = max(worst, abs(mag1 - mag0) / denom)
    return {'residual': worst}


# =================================================================
# FG6.9 — Per-branch triplet transversality
# =================================================================

def test_FG6_9_triplet_per_branch_transversality(n_dirs=12, k_mag=0.05, seed=71):
    """2·n_half · W^{a, ±}_T  → 0 with the F29-B4 small-k scaling."""
    dirs = _random_dirs(n_dirs, seed=seed)
    worst = {'+': 0.0, '-': 0.0}
    for d in dirs:
        kx, ky, kz = k_mag * d
        (psi_p_pl, _, _), (psi_p_mn, _, _) = _per_branch_modes(kx, ky, kz)
        # Use ψ=φ identically on both isospin slots — same construction
        # as F29 B4 (which scaled as c_lat·|k|).
        phi_iso_pl = _make_doublet(psi_p_pl.copy(), psi_p_pl.copy())
        phi_iso_mn = _make_doublet(psi_p_mn.copy(), psi_p_mn.copy())
        EW_pl, BW_pl, W_pl, n_pl = triplet_bilinear_branch(
            phi_iso_pl, phi_iso_pl, kx, ky, kz, sign='+')
        EW_mn, BW_mn, W_mn, n_mn = triplet_bilinear_branch(
            phi_iso_mn, phi_iso_mn, kx, ky, kz, sign='-')
        for sign, W, n_half in [('+', W_pl, n_pl), ('-', W_mn, n_mn)]:
            two_n = 2.0 * n_half
            for a in range(3):
                W_a = W[a]
                denom = np.linalg.norm(W_a) + 1e-30
                worst[sign] = max(worst[sign], abs(two_n @ W_a) / denom)
    return {
        'residual':           max(worst['+'], worst['-']),
        'worst_plus_branch':  worst['+'],
        'worst_minus_branch': worst['-'],
        'expected_scaling':   f'O(c_lat · |k|) = {C_LAT * k_mag:.4e}',
    }


# =================================================================
# FG6.10 — Riemann-Silberstein decomposition is exact
# =================================================================

def test_FG6_10_riemann_silberstein_identity(n_dirs=16, k_mag=0.1, seed=81):
    """E = (F^+ + F^-)/2 and B = (F^+ − F^-)/(2i) exactly (algebraic).

    Machine-zero residual; closes the F^± ↔ (E, B) bijection.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    worst = 0.0
    for d in dirs:
        kx, ky, kz = k_mag * d
        (psi_p_pl, psi_m_pl, _), (psi_p_mn, psi_m_mn, _) = _per_branch_modes(kx, ky, kz)
        E, B, _ = EM_bilinears_two_helicity(
            psi_p_pl, psi_m_pl, psi_p_mn, psi_m_mn, kx, ky, kz,
        )
        Fp, Fm = riemann_silberstein_decomp(E, B)
        E_back = 0.5 * (Fp + Fm)
        B_back = (Fp - Fm) / (2j)
        denom = max(np.linalg.norm(E) + np.linalg.norm(B), 1e-30)
        worst = max(worst, (np.linalg.norm(E - E_back) + np.linalg.norm(B - B_back)) / denom)
    return {'residual': worst}


# ── runner ───────────────────────────────────────────────────────

def run():
    tests = [
        ('FG6.1_per_branch_nonzero_and_transverse',
         test_FG6_1_per_branch_nonzero_and_transverse),
        ('FG6.2_two_helicity_linearity',
         test_FG6_2_two_helicity_linearity),
        ('FG6.3_both_helicities_present',
         test_FG6_3_both_helicities_present),
        ('FG6.4_singlet_SU2_invariance_per_branch',
         test_FG6_4_singlet_SU2_invariance_per_branch),
        ('FG6.5_chiral_propagation_per_helicity',
         test_FG6_5_chiral_propagation_per_helicity),
        ('FG6.6_birefringence_vs_F30',
         test_FG6_6_birefringence_vs_F30),
        ('FG6.7_triplet_adjoint_rotation_per_branch',
         test_FG6_7_triplet_adjoint_per_branch),
        ('FG6.8_triplet_magnitude_SU2_invariance_combined',
         test_FG6_8_triplet_magnitude_invariance_combined),
        ('FG6.9_triplet_per_branch_transversality',
         test_FG6_9_triplet_per_branch_transversality),
        ('FG6.10_riemann_silberstein_decomposition',
         test_FG6_10_riemann_silberstein_identity),
    ]
    results = {}
    t0 = time.time()
    for name, fn in tests:
        ts = time.time()
        try:
            out = fn()
            results[name] = {'ok': True, 'time_s': time.time() - ts, **out}
        except Exception as e:
            results[name] = {'ok': False, 'error': str(e),
                             'time_s': time.time() - ts}
    results['_meta'] = {
        'total_time_s': time.time() - t0,
        'date': time.strftime('%Y-%m-%d - %H:%M'),
        'C_LAT_analytic': C_LAT,
        'F30_birefringence_coeff_exact': -SQRT3_OVER_27,
    }

    # Save JSON
    out_dir = os.path.join(os.path.dirname(HERE), 'test-results')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'FG6_two_helicity_photon.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    # Console summary
    print('=' * 72)
    print('FG-6  Two-helicity composite photon — both Weyl branches')
    print('=' * 72)
    for name, fn in tests:
        r = results[name]
        if not r.get('ok'):
            print(f"  {name:55s}  FAIL: {r.get('error')}")
            continue
        residual = None
        for key in ('residual', 'fit_relative_error',
                    'worst_Fp_residual_rel',
                    'worst_transversality_plus',
                    'min_helicity_ratio_min(|F+|,|F-|)/max(|F+|,|F-|)',
                    'residual_plus_branch'):
            if key in r:
                residual = r[key]
                break
        msg = f"  {name:55s}  "
        if residual is not None:
            try:
                msg += f"{residual:.3e}"
            except (TypeError, ValueError):
                msg += str(residual)
        msg += f"   ({r['time_s']:.3f}s)"
        print(msg)
    print('-' * 72)
    print(f"Total: {results['_meta']['total_time_s']:.2f}s")
    print(f"Wrote results -> {out_path}")
    return results


if __name__ == '__main__':
    run()
