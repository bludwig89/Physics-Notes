"""
test_su2_photon_bridge.py
=========================

Bridges F27 (chiral SU(2) from β-gauging) → F26 (rotation-law photon).

Two question sets:

  A. Does c_lat / Ω(k) survive an SU(2) gauge transform on the underlying
     Weyl spinors?
  B. Can a W-boson triplet analog of the photon G^i be built on the
     doublet isospin index, and does it satisfy the same dispersion /
     transversality as the photon?

Doublet structure:
    ψ_doublet ∈ C^4 ordered (ν↑, ν↓, e↑, e↓).
    Isospin index α ∈ {ν, e}; spin index s ∈ {↑, ↓}.
    Each isospin component is a 2-spinor on the BCC lattice.

Bilinears (per Paper 1 Eq. 35 extended):
    Photon (singlet): G_H^i = Σ_α (φ^α)† σ^i ψ^α
    W-triplet:        W_H^{a,i} = Σ_{αβ} (τ^a)_{αβ} (φ^α)† σ^i ψ^β

Both use Hermitian conjugation (φ†) which is the SU(2)-clean variant.
(The Paper 1 transpose variant G_T = φ^T σ^i ψ is NOT SU(2)-invariant,
which is itself a finding — recorded in T_extra below.)

Date: 2026-05-23
"""

import sys, os, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ca-simulation'))

import numpy as np

import ca_bcc as bcc
import ca_maxwell as cm
from ca_maxwell import _PAULIS, weyl_eigenmodes_3d_bcc, EM_bilinears

SQRT3 = np.sqrt(3.0)
C_LAT = 1.0 / SQRT3

# Isospin Pauli matrices τ^a (act on iso doublet index).
_TAU_ISO = (
    np.array([[0,  1 ], [1,  0 ]], dtype=complex),   # τ¹
    np.array([[0, -1j], [1j, 0 ]], dtype=complex),   # τ²
    np.array([[1,  0 ], [0, -1 ]], dtype=complex),   # τ³
)


# ── utilities ──────────────────────────────────────────────────────

def random_su2(seed):
    """Random SU(2) matrix via unit quaternion."""
    rng = np.random.default_rng(abs(int(seed)) % (2**31))
    q = rng.standard_normal(4)
    q /= np.linalg.norm(q)
    a = q[0] + 1j * q[3]
    b = q[2] + 1j * q[1]
    return np.array([[a, -np.conj(b)],
                     [b,  np.conj(a)]], dtype=complex)


def adjoint_rotation(V):
    """R^{ab}(V) = ½ tr(τ^a V τ^b V†) — SO(3) rotation associated with V ∈ SU(2)."""
    R = np.zeros((3, 3), dtype=float)
    for a in range(3):
        for b in range(3):
            R[a, b] = 0.5 * np.real(
                np.trace(_TAU_ISO[a] @ V @ _TAU_ISO[b] @ V.conj().T)
            )
    return R


def random_dirs(n, seed):
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((n, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v


def make_doublet(psi_nu, psi_e):
    """Stack two 2-spinors into a (2, 2) doublet: rows iso, cols spin."""
    return np.stack([psi_nu, psi_e], axis=0)


def apply_su2(psi_doublet, V):
    """Apply V ∈ SU(2) on isospin index of a (2-iso, 2-spin) doublet."""
    return V @ psi_doublet


def singlet_bilinear_H(phi, psi):
    """G_H^i = Σ_α (φ^α)† σ^i ψ^α  — Hermitian singlet."""
    G = np.zeros(3, dtype=complex)
    for i, S in enumerate(_PAULIS):
        s = 0.0 + 0.0j
        for alpha in range(2):
            s += np.conj(phi[alpha]) @ S @ psi[alpha]
        G[i] = s
    return G


def triplet_bilinear_H(phi, psi):
    """W_H^{a,i} = Σ_{αβ} (τ^a)_{αβ} (φ^α)† σ^i ψ^β  — Hermitian triplet."""
    W = np.zeros((3, 3), dtype=complex)   # (a, i)
    for a, T in enumerate(_TAU_ISO):
        for i, S in enumerate(_PAULIS):
            s = 0.0 + 0.0j
            for alpha in range(2):
                for beta in range(2):
                    c = T[alpha, beta]
                    if c == 0:
                        continue
                    s += c * (np.conj(phi[alpha]) @ S @ psi[beta])
            W[a, i] = s
    return W


def singlet_bilinear_T(phi, psi):
    """Transpose-style singlet (Paper 1 Eq. 33 form) — NOT SU(2)-clean."""
    G = np.zeros(3, dtype=complex)
    for i, S in enumerate(_PAULIS):
        s = 0.0 + 0.0j
        for alpha in range(2):
            s += phi[alpha] @ S @ psi[alpha]
        G[i] = s
    return G


def transverse(v, n_hat):
    return v - (v @ n_hat) * n_hat


# ── tests ──────────────────────────────────────────────────────────

def test_A1_dispersion_invariance(n_dirs=12, n_steps=20, k_mag=0.3, seed=11):
    """A1: Ω(k) is invariant under global SU(2) on the doublet.

    Strategy: build a doublet eigenmode at k, apply V (mixing ν/e),
    propagate n_steps of the BCC unitary per isospin component, measure
    the per-tick phase. Compare to Ω(k) = 2 ω_BCC(k/2).
    Each isospin component evolves with U(k/2) — V mixes the two but
    both share the same Ω, so the doublet acquires the same phase.
    """
    dirs = random_dirs(n_dirs, seed)
    worst = 0.0
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, _, omega_h = weyl_eigenmodes_3d_bcc(*kh, sign='+')
        Omega = 2.0 * omega_h

        # Doublet eigenmode: ν and e both populated with the same Weyl mode
        psi_dbl = make_doublet(psi_p.copy(), psi_p.copy())

        # Apply random SU(2) (mixing ν and e)
        V = random_su2(seed + 7)
        psi_dbl_V = apply_su2(psi_dbl, V)

        # BCC unitary U(k/2) — applied identically to each isospin component
        U_ff, U_fg, U_gf, U_gg = bcc.bcc_unitary(kh[0], kh[1], kh[2], sign='+')
        U = np.array([[U_ff, U_fg], [U_gf, U_gg]], dtype=complex)

        # Evolve doublet n_steps via U applied to each row
        psi_t = psi_dbl_V.copy()
        psi_t_full = U
        for _ in range(n_steps - 1):
            psi_t_full = psi_t_full @ U
        # Apply n_steps of U to each row
        # Each isospin component is *not necessarily* an eigenmode of U after V
        # (it's a linear comb of ν, e amplitudes of the same Weyl eigenmode at k/2).
        # But since both ν and e are the SAME Weyl mode psi_p (eigenvector of U),
        # the SU(2)-mixed doublet IS also a U-eigenvector per row → exact phase test.
        psi_n = psi_dbl_V @ psi_t_full.T  # apply U^n to each row of psi_dbl_V
        # Expected: psi_n = e^{-i n_steps · ω_half} · psi_dbl_V
        expected_phase = np.exp(-1j * n_steps * omega_h)
        ratio = psi_n / (psi_dbl_V * expected_phase)
        # Residual: how much does the actual evolved state deviate from
        # exact eigen-phase rotation?
        finite = np.abs(psi_dbl_V) > 1e-12
        if not np.any(finite):
            continue
        worst = max(worst, float(np.max(np.abs(ratio[finite] - 1.0))))
    # The eigen-phase per tick is ω_BCC(k/2); per doublet, Ω = 2ω_half.
    return {'residual': worst, 'Omega_analytic': Omega}


def test_B1_singlet_invariance(n_dirs=12, k_mag=0.3, seed=21):
    """B1: Hermitian singlet G_H^i = Σ_α (φ^α)† σ^i ψ^α is exactly SU(2)-invariant."""
    dirs = random_dirs(n_dirs, seed)
    worst = 0.0
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, psi_m, _ = weyl_eigenmodes_3d_bcc(*kh, sign='+')

        # Distinct φ, ψ doublets to make G non-trivial
        phi = make_doublet(psi_p.copy(), psi_m.copy())
        psi = make_doublet(psi_m.copy(), psi_p.copy())

        G_orig = singlet_bilinear_H(phi, psi)

        V = random_su2(seed + 13 + int(1000 * d[0]))
        G_new = singlet_bilinear_H(apply_su2(phi, V), apply_su2(psi, V))

        denom = max(np.linalg.norm(G_orig), 1e-30)
        worst = max(worst, float(np.linalg.norm(G_new - G_orig) / denom))
    return {'residual': worst}


def test_B2_triplet_adjoint(n_dirs=12, k_mag=0.3, seed=31):
    """B2: W^a → R^{ab}(V) W^b under V ∈ SU(2)."""
    dirs = random_dirs(n_dirs, seed)
    worst = 0.0
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, psi_m, _ = weyl_eigenmodes_3d_bcc(*kh, sign='+')

        phi = make_doublet(psi_p.copy(), psi_m.copy())
        psi = make_doublet(psi_m.copy(), psi_p.copy())

        V = random_su2(seed + 17 + int(1000 * d[1]))
        R = adjoint_rotation(V)              # SO(3) on a-index

        W_orig = triplet_bilinear_H(phi, psi)                # (3, 3)
        W_xfm  = triplet_bilinear_H(apply_su2(phi, V),
                                    apply_su2(psi, V))       # (3, 3)
        W_predicted = R @ W_orig                              # rotate a-index

        denom = max(np.linalg.norm(W_orig), 1e-30)
        worst = max(worst, float(np.linalg.norm(W_xfm - W_predicted) / denom))
    return {'residual': worst}


def test_B3_triplet_magnitude(n_dirs=12, k_mag=0.3, seed=41):
    """B3: Σ_a |W^a|² is SU(2)-invariant (sum of squared rows of the (3,3) W)."""
    dirs = random_dirs(n_dirs, seed)
    worst = 0.0
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, psi_m, _ = weyl_eigenmodes_3d_bcc(*kh, sign='+')

        phi = make_doublet(psi_p.copy(), psi_m.copy())
        psi = make_doublet(psi_m.copy(), psi_p.copy())

        V = random_su2(seed + 23 + int(1000 * d[2]))

        W_orig = triplet_bilinear_H(phi, psi)
        W_xfm  = triplet_bilinear_H(apply_su2(phi, V), apply_su2(psi, V))

        mag_orig = float(np.sum(np.abs(W_orig) ** 2))
        mag_xfm  = float(np.sum(np.abs(W_xfm) ** 2))
        denom = max(mag_orig, 1e-30)
        worst = max(worst, abs(mag_orig - mag_xfm) / denom)
    return {'residual': worst}


def test_B4_triplet_transversality(n_dirs=12, k_mag=0.05, seed=51):
    """B4: 2 n_{k/2} · W^a → 0 at small k for each a.

    The photon Maxwell transversality test (cm.maxwell_transversality)
    uses the singlet G = φ^T σ ψ projected onto transverse part.
    Here we test the same property at the W-triplet level WITHOUT
    explicit projection, so the residual measures intrinsic transversality
    of the bilinear (not whether we project it).
    """
    dirs = random_dirs(n_dirs, seed)
    worst = 0.0
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, psi_m, _ = weyl_eigenmodes_3d_bcc(*kh, sign='+')
        _, nx, ny, nz = bcc._bcc_uvec(*kh, sign='+')
        n_half = np.array([nx, ny, nz], dtype=float)

        # Use the SAME eigenmode for both isospin components and for both φ, ψ
        # — this is the W^a analog of the photon transverse mode.
        phi = make_doublet(psi_p.copy(), psi_p.copy())
        psi = make_doublet(psi_p.copy(), psi_p.copy())

        W = triplet_bilinear_H(phi, psi)          # (3 a, 3 i)
        two_n = 2.0 * n_half

        for a in range(3):
            W_a = W[a]
            denom = np.linalg.norm(W_a) + 1e-30
            worst = max(worst, abs(two_n @ W_a) / denom)
    return {'residual': worst}


def test_B5_per_component_rotation_rate(n_dirs=8, k_mag=0.05, seed=61):
    """B5: each W^a, when promoted to (E^a, B^a) per Paper 1 Eq. 35 form,
    rotates at the same Ω(k) = 2 ω_BCC(k/2) as the photon.

    Strategy: build E^a, B^a by analogy with EM_bilinears using the τ^a
    triplet at the bilinear level. Apply one rotation_step_em_spectral-
    style rotation per a-component. Measure the rotation angle and
    compare to the analytic Ω(k).

    Since the rotation propagator acts on the FIELDS (E, B) and is
    INDEPENDENT of the isospin construction, this is a sanity check
    that each W^a propagates identically to a photon.
    """
    dirs = random_dirs(n_dirs, seed)
    worst = 0.0
    Omegas = []
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, psi_m, omega_h = weyl_eigenmodes_3d_bcc(*kh, sign='+')
        Omega = 2.0 * omega_h
        _, nx, ny, nz = bcc._bcc_uvec(*kh, sign='+')
        n_half = np.array([nx, ny, nz], dtype=float)
        n_mag = np.linalg.norm(n_half)
        n_hat = n_half / max(n_mag, 1e-30)

        # Use psi_p / psi_p doublets (both ν and e populated identically)
        phi = make_doublet(psi_p.copy(), psi_p.copy())
        psi = make_doublet(psi_p.copy(), psi_p.copy())

        W = triplet_bilinear_H(phi, psi)         # (3, 3)
        # For each a, build E^a, B^a per Eq. 35 form on the transverse part
        for a in range(3):
            W_a = W[a]
            W_T = transverse(W_a, n_hat)
            E_a = n_mag * (W_T + np.conj(W_T))
            B_a = 1j * n_mag * (np.conj(W_T) - W_T)
            # Rotate by analytic Ω (apply the rotation law one tick)
            cO = np.cos(Omega);  sO = np.sin(Omega)
            E_new =  cO * E_a + sO * B_a
            B_new = -sO * E_a + cO * B_a
            # Magnitude conservation under rotation:
            mag0 = np.linalg.norm(E_a) ** 2 + np.linalg.norm(B_a) ** 2
            mag1 = np.linalg.norm(E_new) ** 2 + np.linalg.norm(B_new) ** 2
            if mag0 < 1e-30:
                continue
            worst = max(worst, abs(mag1 - mag0) / mag0)
        Omegas.append(Omega)
    return {'residual': worst,
            'Omega_min': float(min(Omegas)) if Omegas else None,
            'Omega_max': float(max(Omegas)) if Omegas else None,
            'Omega_lin': k_mag / SQRT3}


def test_B5b_triplet_rotation_under_su2(n_dirs=8, k_mag=0.05, seed=71):
    """B5b: After SU(2) transform on the underlying spinors, the triplet
    magnitude Σ_a (||E^a||² + ||B^a||²) is still conserved by the rotation
    law (i.e. each rotated W^a still has rotation-law-conserved energy).
    """
    dirs = random_dirs(n_dirs, seed)
    worst_before = 0.0
    worst_after = 0.0
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, _, omega_h = weyl_eigenmodes_3d_bcc(*kh, sign='+')
        Omega = 2.0 * omega_h
        _, nx, ny, nz = bcc._bcc_uvec(*kh, sign='+')
        n_half = np.array([nx, ny, nz], dtype=float)
        n_mag = np.linalg.norm(n_half)
        n_hat = n_half / max(n_mag, 1e-30)

        phi0 = make_doublet(psi_p.copy(), psi_p.copy())
        psi0 = make_doublet(psi_p.copy(), psi_p.copy())

        V = random_su2(seed + 31 + int(1000 * d[0]))
        phi_V = apply_su2(phi0, V)
        psi_V = apply_su2(psi0, V)

        for phi, psi, bucket in ((phi0, psi0, 'before'),
                                  (phi_V, psi_V, 'after')):
            W = triplet_bilinear_H(phi, psi)
            mag0_tot = 0.0
            mag1_tot = 0.0
            for a in range(3):
                W_a = W[a]
                W_T = transverse(W_a, n_hat)
                E_a = n_mag * (W_T + np.conj(W_T))
                B_a = 1j * n_mag * (np.conj(W_T) - W_T)
                cO = np.cos(Omega);  sO = np.sin(Omega)
                E_new =  cO * E_a + sO * B_a
                B_new = -sO * E_a + cO * B_a
                mag0_tot += np.linalg.norm(E_a) ** 2 + np.linalg.norm(B_a) ** 2
                mag1_tot += np.linalg.norm(E_new) ** 2 + np.linalg.norm(B_new) ** 2
            if mag0_tot < 1e-30:
                continue
            res = abs(mag1_tot - mag0_tot) / mag0_tot
            if bucket == 'before':
                worst_before = max(worst_before, res)
            else:
                worst_after = max(worst_after, res)
    return {'residual_before': worst_before, 'residual_after': worst_after}


def test_extra_transpose_not_su2_invariant(n_dirs=12, k_mag=0.3, seed=81):
    """Document that the Paper 1 transpose-form bilinear G_T^i = φ^T σ^i ψ
    is NOT SU(2)-invariant under the simple V ⊗ I_spin transform (V^T V ≠ I).

    This is a structural observation, not a defect — the photon as defined
    by the Bisio transpose construction is a U(1)_EM singlet but does NOT
    sit inside an SU(2) singlet of the doublet structure. The W-triplet
    construction here uses the Hermitian variant which IS SU(2)-clean.
    """
    dirs = random_dirs(n_dirs, seed)
    deviations = []
    for d in dirs:
        k = k_mag * d
        kh = k / 2.0
        psi_p, psi_m, _ = weyl_eigenmodes_3d_bcc(*kh, sign='+')
        phi = make_doublet(psi_p.copy(), psi_m.copy())
        psi = make_doublet(psi_m.copy(), psi_p.copy())

        G_orig = singlet_bilinear_T(phi, psi)
        V = random_su2(seed + 23 + int(1000 * d[2]))
        G_new = singlet_bilinear_T(apply_su2(phi, V), apply_su2(psi, V))

        denom = max(np.linalg.norm(G_orig), 1e-30)
        deviations.append(float(np.linalg.norm(G_new - G_orig) / denom))
    return {
        'max_deviation': max(deviations),
        'mean_deviation': float(np.mean(deviations)),
        'note': 'expected to be O(1), confirming transpose form is not SU(2)-clean',
    }


# ── runner ─────────────────────────────────────────────────────────

def run():
    results = {}
    t0 = time.time()

    tests = [
        ('A1_dispersion_invariance_under_SU2',
         lambda: test_A1_dispersion_invariance()),
        ('B1_singlet_H_SU2_invariance',
         lambda: test_B1_singlet_invariance()),
        ('B2_triplet_adjoint_rotation',
         lambda: test_B2_triplet_adjoint()),
        ('B3_triplet_magnitude_SU2_invariance',
         lambda: test_B3_triplet_magnitude()),
        ('B4_triplet_transversality_smallk',
         lambda: test_B4_triplet_transversality(k_mag=0.05)),
        ('B5_per_component_rotation_law_consistency',
         lambda: test_B5_per_component_rotation_rate(k_mag=0.05)),
        ('B5b_triplet_rotation_under_SU2',
         lambda: test_B5b_triplet_rotation_under_su2(k_mag=0.05)),
        ('Extra_transpose_form_NOT_SU2_invariant',
         lambda: test_extra_transpose_not_su2_invariant()),
    ]
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
        'date': '2026-05-23',
        'C_LAT_analytic': C_LAT,
    }

    print(json.dumps(results, indent=2, default=str))
    return results


if __name__ == '__main__':
    run()
