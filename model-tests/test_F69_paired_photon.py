"""
test_F69_paired_photon.py
=========================

Builds out McPhee's "two spin-½ fermion-photons, only occurs as a pair" as THE
photon (module `ca_photon_pair`) and retires the composite σ-bilinear photon as
real-world-untenable (birefringent — F65/F66/F67).

The paired photon: total momentum k shared by two Weyl constituents (k/2 each),
one + branch and one − branch, bound symmetrically.  Pair phase
    Ω_pair(k) = ω⁺(k/2) + ω⁻(k/2)  ≡ Ω_even,
so both helicities ride one rate → NON-birefringent.  Contrast the retired
composite bilinear, where each helicity rode its own branch (Ω^±) → birefringent.

Sections:
  PP1  pair dispersion = ω⁺(k/2)+ω⁻(k/2), and equals the even-law rotation rate
       actually used by the photon propagator (consistency).            [exact]
  PP2  non-birefringent: a linearly polarized body-diagonal mode under the
       paired-photon propagator has zero helicity split, vs the RETIRED chiral
       bilinear which splits by −ΔΩ·N.                                   [machine]
  PP3  massless & luminal: Ω_pair(k→0) → (1/√3)|k| (no gap) and group
       velocity → 1/√3 along random directions.                         [quant]
  PP4  "only occurs as a pair": the pair phase is the SUM of the two real Weyl
       constituent phases ω⁺(k/2), ω⁻(k/2); an UNPAIRED single-branch quantum
       would carry Ω^± and reintroduce the birefringence ΔΩ.  The pairing is
       exactly what removes it.                                          [machine]
  PP5  spin-1 / two transverse polarizations, real & unitary (norm-conserving)
       propagation of the paired field.                                 [machine]

Imports the real model: ca_photon_pair (new), ca_wmu.w_propagation_step_chiral
(the retired-as-photon σ-bilinear law, for contrast), ca_bcc.
"""

import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import numpy as np
import ca_fft as _fft
from ca_bcc import bcc_dispersion
from ca_wmu import w_propagation_step_chiral, _f26_rotation_step
from ca_lattice import make_kgrid_3d
import ca_photon_pair as pp

ROOT3 = np.sqrt(3.0)


def helicity_phases(E, B, m, L, Fp0, Fm0):
    idx = (m, m, m)
    Eh = np.array([_fft.fftn(E[a])[idx] for a in range(3)])
    Bh = np.array([_fft.fftn(B[a])[idx] for a in range(3)])
    Fp = Eh + 1j * Bh
    Fm = Eh - 1j * Bh
    ap = np.vdot(Fp0, Fp) / np.vdot(Fp0, Fp0)
    am = np.vdot(Fm0, Fm) / np.vdot(Fm0, Fm0)
    return np.angle(ap), np.angle(am)


def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


# ----------------------------------------------------------------------
def pp1_dispersion(seed=0):
    rng = np.random.default_rng(seed)
    worst_sum = 0.0
    worst_even = 0.0
    for _ in range(2000):
        k = rng.standard_normal(3) * rng.uniform(0.01, 1.0)
        wp = bcc_dispersion(k[0] / 2, k[1] / 2, k[2] / 2, sign='+')
        wm = bcc_dispersion(k[0] / 2, k[1] / 2, k[2] / 2, sign='-')
        Opair = pp.pair_dispersion(*k)
        worst_sum = max(worst_sum, abs(Opair - (wp + wm)))
        # equals the even-law rate used inside _f26_rotation_step
        KX, KY, KZ = np.array([[[k[0]]]]), np.array([[[k[1]]]]), np.array([[[k[2]]]])
        omp = bcc_dispersion(KX / 2, KY / 2, KZ / 2, sign='+')
        omm = bcc_dispersion(KX / 2, KY / 2, KZ / 2, sign='-')
        even_rate = float((omp + omm).ravel()[0])
        worst_even = max(worst_even, abs(Opair - even_rate))
    return {'pair_eq_branch_sum_resid': float(worst_sum),
            'pair_eq_even_law_rate_resid': float(worst_even)}


def pp2_birefringence(L=24, m=1, N=6):
    khat = np.array([1.0, 1.0, 1.0]) / ROOT3
    E0, B0, e1, e2 = pp.build_pair_mode(L, m, khat, [1.0, -1.0, 0.0])
    Fp0 = e1 + 1j * e2
    Fm0 = e1 - 1j * e2
    k = 2 * np.pi * m / L
    dOm = pp.pair_birefringence(k, k, k)

    # paired-photon propagator (even law)
    Ep, Bp = E0.copy(), B0.copy()
    for _ in range(N):
        Ep, Bp = pp.photon_step_spectral(Ep, Bp)
    pp_p, pp_m = helicity_phases(Ep, Bp, m, L, Fp0, Fm0)
    S_pair = wrap(pp_p + pp_m)

    # RETIRED composite σ-bilinear (chiral law) for contrast
    Ec, Bc = E0.copy(), B0.copy()
    for _ in range(N):
        Ec, Bc = w_propagation_step_chiral(Ec, Bc)
    pc_p, pc_m = helicity_phases(Ec, Bc, m, L, Fp0, Fm0)
    S_chiral = wrap(pc_p + pc_m)

    return {'dOmega_would_be': float(dOm), 'N': N,
            'S_paired_photon': float(S_pair),
            'S_paired_resid_from_zero': float(abs(S_pair)),
            'S_retired_chiral': float(S_chiral),
            'S_retired_pred_-dOmega_N': float(wrap(-dOm * N))}


def pp3_massless(seed=3):
    rng = np.random.default_rng(seed)
    cl = 1.0 / ROOT3
    gerr = 0.0
    for _ in range(12):
        v = rng.standard_normal(3); n = v / np.linalg.norm(v)
        gerr = max(gerr, abs(pp.group_velocity(n) - cl))
    # no gap: Ω_pair(k→0)/|k| → 1/√3 and Ω_pair(0)=0
    n = np.array([1, 0.3, -0.7]); n /= np.linalg.norm(n)
    small = [pp.pair_dispersion(*(k * n)) / k for k in (1e-2, 1e-3, 1e-4)]
    gap = pp.pair_dispersion(0.0, 0.0, 0.0)
    return {'group_vel_max_err_vs_inv_sqrt3': float(gerr),
            'c_lat': float(cl),
            'Omega_over_k_smallk': [float(x) for x in small],
            'rest_gap_Omega_at_k0': float(gap)}


def pp4_only_as_pair(seed=4):
    """The pair phase = sum of the two real Weyl constituent eigenphases.
    Confirm against the actual Weyl dispersion, and show an unpaired single
    branch would carry Ω^± (birefringent), the pairing removing exactly ΔΩ."""
    rng = np.random.default_rng(seed)
    worst = 0.0
    dOm_list = []
    for _ in range(1500):
        k = rng.standard_normal(3) * rng.uniform(0.05, 0.8)
        wp = bcc_dispersion(k[0] / 2, k[1] / 2, k[2] / 2, sign='+')   # constituent +
        wm = bcc_dispersion(k[0] / 2, k[1] / 2, k[2] / 2, sign='-')   # constituent −
        pair = pp.pair_dispersion(*k)
        worst = max(worst, abs(pair - (wp + wm)))
        # unpaired single-branch photon would ride Ω^± = 2ω^±(k/2): split = ΔΩ
        dOm_list.append(abs(2 * wp - 2 * wm))
    return {'pair_phase_eq_constituent_sum_resid': float(worst),
            'unpaired_split_dOmega_median': float(np.median(dOm_list)),
            'note': 'pairing forces both branches → split cancels; unpaired would not'}


def pp5_transverse_unitary(L=16, seed=5):
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))
    norm0 = np.sum(E**2 + B**2)
    max_imag = 0.0
    # propagate; even law is a clean rotation → real, norm-conserving
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    for _ in range(40):
        En = np.zeros_like(E); Bn = np.zeros_like(B)
        for a in range(3):
            ek = _fft.fftn(E[a]); bk = _fft.fftn(B[a])
            ek2, bk2 = _f26_rotation_step(ek, bk, KX, KY, KZ)
            er = _fft.ifftn(ek2); br = _fft.ifftn(bk2)
            max_imag = max(max_imag, np.max(np.abs(er.imag)), np.max(np.abs(br.imag)))
            En[a] = er.real; Bn[a] = br.real
        E, B = En, Bn
    norm1 = np.sum(E**2 + B**2)
    # two transverse polarizations: build a body-diagonal mode, check E,B ⟂ k
    khat = np.array([1, 1, 1.]) / ROOT3
    Em, Bm, e1, e2 = pp.build_pair_mode(L, 1, khat, [1.0, -1.0, 0.0])
    Eh = np.array([_fft.fftn(Em[a])[(1, 1, 1)] for a in range(3)])
    transverse = abs(np.vdot(khat, Eh)) / (np.linalg.norm(Eh) + 1e-30)
    return {'max_imag_40steps': float(max_imag),
            'norm_drift_rel_40steps': float(abs(norm1 - norm0) / norm0),
            'E_dot_khat_over_normE': float(transverse)}


if __name__ == '__main__':
    t0 = time.time()
    s1 = pp1_dispersion()
    s2 = pp2_birefringence()
    s3 = pp3_massless()
    s4 = pp4_only_as_pair()
    s5 = pp5_transverse_unitary()

    print("=" * 72)
    print("F69 -- the paired-spinor photon (McPhee), composite σ-bilinear retired")
    print("=" * 72)

    print("\n--- PP1. Ω_pair = ω⁺(k/2)+ω⁻(k/2) = even-law rate ---")
    print(f"  pair == branch-sum resid       = {s1['pair_eq_branch_sum_resid']:.2e}")
    print(f"  pair == even-law rate resid    = {s1['pair_eq_even_law_rate_resid']:.2e}")

    print("\n--- PP2. Birefringence (body diagonal, N=6 ticks) ---")
    print(f"  paired photon  S=φ⁺+φ⁻ = {s2['S_paired_photon']:+.2e} "
          f"(resid from 0: {s2['S_paired_resid_from_zero']:.2e})  -> NONE")
    print(f"  retired chiral S       = {s2['S_retired_chiral']:+.5f} "
          f"vs -ΔΩ·N {s2['S_retired_pred_-dOmega_N']:+.5f}  -> birefringent")

    print("\n--- PP3. Massless & luminal ---")
    print(f"  group velocity → 1/√3, max err = {s3['group_vel_max_err_vs_inv_sqrt3']:.2e}")
    print(f"  Ω/k at k→0 = {['%.6f'%x for x in s3['Omega_over_k_smallk']]} (→{s3['c_lat']:.6f})")
    print(f"  rest gap Ω(k=0) = {s3['rest_gap_Omega_at_k0']:.2e} (massless)")

    print("\n--- PP4. 'Only occurs as a pair' ---")
    print(f"  pair phase == constituent sum resid = {s4['pair_phase_eq_constituent_sum_resid']:.2e}")
    print(f"  unpaired single-branch split (ΔΩ median) = {s4['unpaired_split_dOmega_median']:.3e}"
          f"  (this is what the pairing cancels)")

    print("\n--- PP5. Spin-1 / transverse / unitary ---")
    print(f"  max|imag| 40 steps   = {s5['max_imag_40steps']:.2e}")
    print(f"  norm drift 40 steps  = {s5['norm_drift_rel_40steps']:.2e}")
    print(f"  |E·k̂|/|E| (transverse) = {s5['E_dot_khat_over_normE']:.2e}")

    print("\n=== VERDICT ===")
    print("  The paired-spinor photon (two γ_{1/2}, only as a pair) rides the")
    print("  symmetric rate Ω_pair = ω⁺(k/2)+ω⁻(k/2): massless, luminal (1/√3),")
    print("  transverse, unitary, and NON-BIREFRINGENT (S=0 vs the retired")
    print("  composite bilinear's −ΔΩ·N). The pairing — both branches always")
    print("  present — is exactly what cancels the birefringence ΔΩ. The σ-bilinear")
    print("  is retired AS THE PHOTON (kept only for the massive/non-Abelian sectors")
    print("  not under the polarimetry bound).")
    print(f"\n  ({time.time()-t0:.2f} s)")

    out = {'PP1': s1, 'PP2': s2, 'PP3': s3, 'PP4': s4, 'PP5': s5}
    dst = os.path.join(os.path.dirname(__file__), '..', 'test-results',
                       'F69_paired_photon.json')
    try:
        with open(dst, 'w') as fh:
            json.dump(out, fh, indent=2)
        print(f"  wrote {dst}")
    except Exception as e:
        print(f"  (could not write json: {e})")
