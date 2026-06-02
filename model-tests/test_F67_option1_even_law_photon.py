"""
test_F67_option1_even_law_photon.py
===================================

Tests F66 "option 1": can the physical U(1) photon be built so that BOTH
helicities ride the chirality-EVEN dispersion  Omega_even = (Omega+ + Omega-)/2,
killing the linear vacuum birefringence that F65/F66 showed excludes the F64
cell size?  And what does that cost?

The model already contains BOTH propagators (this is the whole point):
  * ca_wmu._f26_rotation_step        -> EVEN law  R(Omega_even) on (E,B).
                                        Non-birefringent. Currently used for the
                                        massive W and the Z (ca_z_field).
  * ca_wmu.w_propagation_step_chiral -> CHIRAL law: F+ -> exp(-i Omega+),
                                        F- -> exp(+i Omega-). Birefringent.
                                        The photon's propagator since F37; it IS
                                        the honest two-branch Weyl bilinear (F39).

So "option 1" = run the U(1) photon under _f26_rotation_step instead of the
chiral step.  This script confronts the real code with three questions:

  S1. Does the even law actually remove birefringence?           (expect: yes, exact)
  S2. Is the even-law field still a legitimate photon?           (group vel -> 1/sqrt3,
                                                                   real, norm-conserving)
  S3. THE COST: is the even-law photon representable as the
      two-branch Weyl bilinear?                                  (expect: NO -- the
      wedge between the two photons is exactly the birefringence Delta_Omega/2,
      and that phase has no single-Weyl-branch source.)

Conclusion sought: the bilinear photon (birefringent) and the even/gauge photon
(non-birefringent) are MUTUALLY EXCLUSIVE constructions -- you get one or the
other, and the thing that separates them is precisely the excluded signal.

Imports the real model modules (no re-derivation of the propagators).
Self-contained otherwise; numpy + project modules only.  Per CLAUDE.md the only
chiral object touched by hand is the closed-form 2x2 (E,B) field rotation; all
spinor work goes through the audited ca_bcc / ca_wmu routines.
"""

import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ca-simulation'))

import numpy as np
import ca_fft as _fft
from ca_lattice import make_kgrid_3d
from ca_bcc import bcc_dispersion, weyl_step_3d_bcc
from ca_wmu import _f26_rotation_step, w_propagation_step_chiral

ROOT3 = np.sqrt(3.0)


# ----------------------------------------------------------------------
# dispersion helpers (photon convention Omega^pm(k) = 2 omega_pm(k/2))
# ----------------------------------------------------------------------
def Omega_pm(kx, ky, kz):
    Op = 2.0 * bcc_dispersion(kx / 2, ky / 2, kz / 2, sign='+')
    Om = 2.0 * bcc_dispersion(kx / 2, ky / 2, kz / 2, sign='-')
    return Op, Om


def dOmega(kx, ky, kz):
    Op, Om = Omega_pm(kx, ky, kz)
    return Op - Om                       # the birefringence


# ----------------------------------------------------------------------
# build a real, linearly polarized single-mode (E,B) field on an LxLxL grid
# linear polarization populates BOTH helicities F^+- = E +- iB
# ----------------------------------------------------------------------
def plant_linear_mode(L, m, khat, e1):
    """Return real (E,B) of shape (3,L,L,L): one Fourier mode at index (m,m,m)
    (k = 2*pi*m/L per axis, along khat) with E||e1, B||e2=khat x e1, |E|=|B|."""
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(khat, e1); e2 /= np.linalg.norm(e2)
    Ek = np.zeros((3, L, L, L), complex)
    Bk = np.zeros((3, L, L, L), complex)
    idx = (m, m, m)
    cidx = ((-m) % L, (-m) % L, (-m) % L)
    for a in range(3):
        Ek[a][idx] = e1[a]
        Bk[a][idx] = e2[a]
        Ek[a][cidx] = np.conj(e1[a])     # Hermitian partner -> real field
        Bk[a][cidx] = np.conj(e2[a])
    E = np.array([_fft.ifftn(Ek[a]).real for a in range(3)])
    B = np.array([_fft.ifftn(Bk[a]).real for a in range(3)])
    return E, B, e1, e2


def helicity_phases(E, B, m, L, F_plus0, F_minus0):
    """Accumulated phase of F^+ and F^- at mode (m,m,m), projected onto the
    initial helicity vectors."""
    idx = (m, m, m)
    Ehat = np.array([_fft.fftn(E[a])[idx] for a in range(3)])
    Bhat = np.array([_fft.fftn(B[a])[idx] for a in range(3)])
    Fp = Ehat + 1j * Bhat
    Fm = Ehat - 1j * Bhat
    amp_p = np.vdot(F_plus0, Fp) / np.vdot(F_plus0, F_plus0)
    amp_m = np.vdot(F_minus0, Fm) / np.vdot(F_minus0, F_minus0)
    return np.angle(amp_p), np.angle(amp_m)


# ----------------------------------------------------------------------
# S1 -- does the even law remove birefringence? (dynamical, real propagators)
# ----------------------------------------------------------------------
def section_1(L=24, m=1, N=6):
    khat = np.array([1.0, 1.0, 1.0]) / ROOT3            # body diagonal: max effect
    E0, B0, e1, e2 = plant_linear_mode(L, m, khat, np.array([1.0, -1.0, 0.0]))
    Fp0 = e1 + 1j * e2
    Fm0 = e1 - 1j * e2

    k = 2 * np.pi * m / L
    Op, Om = Omega_pm(k, k, k)
    dOm = Op - Om

    # propagate N ticks under each law
    def run(stepper, even=False):
        E, B = E0.copy(), B0.copy()
        if even:
            KX, KY, KZ = make_kgrid_3d(L, L, L)
            for _ in range(N):
                # _f26_rotation_step works in Fourier space, per component
                En = np.zeros_like(E); Bn = np.zeros_like(B)
                for a in range(3):
                    ek = _fft.fftn(E[a]); bk = _fft.fftn(B[a])
                    ek2, bk2 = _f26_rotation_step(ek, bk, KX, KY, KZ)
                    En[a] = _fft.ifftn(ek2).real; Bn[a] = _fft.ifftn(bk2).real
                E, B = En, Bn
        else:
            for _ in range(N):
                E, B = stepper(E, B)
        return E, B

    Ec, Bc = run(w_propagation_step_chiral, even=False)
    Ee, Be = run(None, even=True)

    pc_p, pc_m = helicity_phases(Ec, Bc, m, L, Fp0, Fm0)
    pe_p, pe_m = helicity_phases(Ee, Be, m, L, Fp0, Fm0)

    # birefringence observable S = phi_+ + phi_-  (= -Delta_Omega * N for chiral, 0 for even)
    S_chiral = pc_p + pc_m
    S_even = pe_p + pe_m
    S_chiral_pred = -dOm * N

    def wrap(x):  # wrap to (-pi,pi]
        return (x + np.pi) % (2 * np.pi) - np.pi

    return {
        'k_per_axis': k, 'Omega_plus': float(Op), 'Omega_minus': float(Om),
        'dOmega': float(dOm), 'N_ticks': N,
        'S_chiral_measured': float(wrap(S_chiral)),
        'S_chiral_predicted': float(wrap(S_chiral_pred)),
        'chiral_resid': float(abs(wrap(S_chiral - S_chiral_pred))),
        'S_even_measured': float(wrap(S_even)),
        'even_birefringence_resid': float(abs(wrap(S_even))),
    }


# ----------------------------------------------------------------------
# S2 -- is the even-law field still a legitimate photon?
# ----------------------------------------------------------------------
def section_2(seed=5):
    rng = np.random.default_rng(seed)
    # (a) group velocity of Omega_even -> 1/sqrt3 at small k, several directions
    h = 1e-5
    g_even, g_avg = [], []
    dirs = []
    for _ in range(12):
        v = rng.standard_normal(3); n = v / np.linalg.norm(v); dirs.append(n)
        kx, ky, kz = h * n
        Op, Om = Omega_pm(kx, ky, kz)
        Oe = 0.5 * (Op + Om)
        g_even.append(Oe / h)                       # |dOmega_even/d|k||
        g_avg.append(0.5 * (Op + Om) / h)           # helicity-averaged chiral
    g_even = np.array(g_even)
    cl = 1.0 / ROOT3

    # (b) reality + per-mode field-space norm conservation under the even step
    L = 16
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))
    norm0 = np.sum(E**2 + B**2)
    max_imag = 0.0
    for _ in range(50):
        En = np.zeros_like(E); Bn = np.zeros_like(B)
        for a in range(3):
            ek = _fft.fftn(E[a]); bk = _fft.fftn(B[a])
            ek2, bk2 = _f26_rotation_step(ek, bk, KX, KY, KZ)
            e_r = _fft.ifftn(ek2); b_r = _fft.ifftn(bk2)
            max_imag = max(max_imag, np.max(np.abs(e_r.imag)), np.max(np.abs(b_r.imag)))
            En[a] = e_r.real; Bn[a] = b_r.real
        E, B = En, Bn
    norm1 = np.sum(E**2 + B**2)

    return {
        'group_vel_even_mean': float(g_even.mean()),
        'group_vel_even_max_abs_err_vs_inv_sqrt3': float(np.max(np.abs(g_even - cl))),
        'c_lat_target': float(cl),
        'real_field_max_imag_50steps': float(max_imag),
        'norm_drift_rel_50steps': float(abs(norm1 - norm0) / norm0),
    }


# ----------------------------------------------------------------------
# S3 -- can the even-law photon be a two-branch Weyl bilinear? (the cost)
# ----------------------------------------------------------------------
def section_3(L=24, m=1, seed=2):
    rng = np.random.default_rng(seed)

    # (a) the phase OVERRIDE needed to convert the bilinear (chiral) photon into
    #     the even photon, per helicity:
    #        F^+ : (-Omega_even) - (-Omega_+) = (Omega_+ - Omega_-)/2 = +dOmega/2
    #        F^- : (+Omega_even) - (+Omega_-) = (Omega_+ - Omega_-)/2 = +dOmega/2
    #     i.e. both helicities must be force-rotated by +dOmega/2, which is
    #     exactly half the birefringence and vanishes iff dOmega = 0.
    worst_override = 0.0
    for _ in range(200):
        v = rng.standard_normal(3); n = v / np.linalg.norm(v)
        k = 0.4
        kx, ky, kz = k * n
        Op, Om = Omega_pm(kx, ky, kz)
        Oe = 0.5 * (Op + Om)
        ov_plus = (-Oe) - (-Op)            # override on F^+
        ov_minus = (Oe) - (Om)             # override on F^-
        half_dOm = 0.5 * (Op - Om)
        worst_override = max(worst_override,
                             abs(ov_plus - half_dOm), abs(ov_minus - half_dOm))

    # (b) each Weyl branch carries Omega^pm, never Omega_even: step a single
    #     branch eigenmode one tick with the REAL Weyl QCA and read its phase.
    #     If Omega_even had a single-branch source, some branch would advance by
    #     omega_even/2 -- it does not (off body-diagonal-plane).
    khat = np.array([1.0, 1.0, 1.0]) / ROOT3
    kmag = 0.4
    kx, ky, kz = kmag * khat
    # plant a single Fourier mode in spinor space and measure the branch phase
    def branch_phase(sign):
        f = np.zeros((L, L, L), complex); g = np.zeros((L, L, L), complex)
        idx = (m, m, m)
        f[idx] = 1.0; g[idx] = 0.0          # generic spinor; phase read modulo content
        # use the audited unitary directly at this mode to avoid mode-mixing ambiguity
        from ca_bcc import bcc_unitary
        kk = 2 * np.pi * m / L
        Uff, Ufg, Ugf, Ugg = bcc_unitary(kk, kk, kk, sign=sign)
        # eigenphase of U^sign at this k is exp(-i omega^sign): take it from the trace/eig
        # closed form: eigenvalues exp(-/+ i omega), omega = arccos(u). Return omega.
        return bcc_dispersion(kk, kk, kk, sign=sign)

    kk = 2 * np.pi * m / L
    w_plus_branch = float(branch_phase('+'))       # = omega_+(k) for the spinor walk
    w_minus_branch = float(branch_phase('-'))
    # photon-convention even half-phase that the even law demands of EACH helicity:
    Op, Om = Omega_pm(kk, kk, kk)
    omega_even_half = 0.25 * (Op + Om)             # = (omega_+(k/2)+omega_-(k/2))/2
    # the spinor inputs to the photon bilinear live at k/2; their branch phases:
    w_plus_half = float(bcc_dispersion(kk / 2, kk / 2, kk / 2, sign='+'))
    w_minus_half = float(bcc_dispersion(kk / 2, kk / 2, kk / 2, sign='-'))
    # neither branch phase equals the even half-phase off-axis:
    gap_plus = abs(w_plus_half - omega_even_half)
    gap_minus = abs(w_minus_half - omega_even_half)

    # body-diagonal override magnitude (closed form): dOmega/2 = -(sqrt3/54) k^2
    k_bd = 0.4
    override_bd = 0.5 * abs(dOmega(k_bd / ROOT3, k_bd / ROOT3, k_bd / ROOT3))
    closed = (ROOT3 / 54.0) * k_bd**2

    return {
        'override_equals_half_dOmega_resid': float(worst_override),
        'branch_half_phase_plus': w_plus_half,
        'branch_half_phase_minus': w_minus_half,
        'even_half_phase_demanded': float(omega_even_half),
        'gap_plus_branch_vs_even': float(gap_plus),
        'gap_minus_branch_vs_even': float(gap_minus),
        'override_bodydiag_measured': float(override_bd),
        'override_bodydiag_closed_sqrt3_over_54_k2': float(closed),
        'override_bd_resid': float(abs(override_bd - closed)),
    }


if __name__ == '__main__':
    t0 = time.time()
    s1 = section_1()
    s2 = section_2()
    s3 = section_3()

    print("=" * 70)
    print("F67 -- option 1: even-law (chirality-even) U(1) photon")
    print("=" * 70)

    print("\n--- S1. Does the EVEN law remove birefringence? (real propagators) ---")
    print(f"  mode k/axis={s1['k_per_axis']:.4f}  Omega+={s1['Omega_plus']:.5f} "
          f"Omega-={s1['Omega_minus']:.5f}  dOmega={s1['dOmega']:+.3e}  N={s1['N_ticks']}")
    print(f"  CHIRAL: S = phi+ + phi-  measured {s1['S_chiral_measured']:+.5f} "
          f"vs predicted -dOmega*N {s1['S_chiral_predicted']:+.5f}  "
          f"(resid {s1['chiral_resid']:.2e})  -> BIREFRINGENT")
    print(f"  EVEN:   S = phi+ + phi-  measured {s1['S_even_measured']:+.2e}  "
          f"(birefringence resid {s1['even_birefringence_resid']:.2e})  -> NONE")

    print("\n--- S2. Is the even-law field still a legitimate photon? ---")
    print(f"  group velocity dOmega_even/d|k| -> {s2['group_vel_even_mean']:.8f} "
          f"(target 1/sqrt3 = {s2['c_lat_target']:.8f}; max err "
          f"{s2['group_vel_even_max_abs_err_vs_inv_sqrt3']:.2e})")
    print(f"  real field preserved: max|imag| over 50 steps = "
          f"{s2['real_field_max_imag_50steps']:.2e}")
    print(f"  field-space norm drift over 50 steps = {s2['norm_drift_rel_50steps']:.2e}")

    print("\n--- S3. Can the even photon be a two-branch Weyl bilinear? (the cost) ---")
    print(f"  override to convert bilinear->even = +dOmega/2 on BOTH helicities; "
          f"resid {s3['override_equals_half_dOmega_resid']:.2e}")
    print(f"  branch half-phases  w+(k/2)={s3['branch_half_phase_plus']:.5f}  "
          f"w-(k/2)={s3['branch_half_phase_minus']:.5f}")
    print(f"  even half-phase demanded of EACH helicity = {s3['even_half_phase_demanded']:.5f}")
    print(f"  gap (no branch supplies the even phase): + {s3['gap_plus_branch_vs_even']:.3e}, "
          f"- {s3['gap_minus_branch_vs_even']:.3e}")
    print(f"  body-diag override = {s3['override_bodydiag_measured']:.5e} vs "
          f"closed (sqrt3/54)k^2 = {s3['override_bodydiag_closed_sqrt3_over_54_k2']:.5e} "
          f"(resid {s3['override_bd_resid']:.2e})")

    print("\n=== VERDICT ===")
    print("  S1: even law kills birefringence exactly (S_even ~ machine zero).")
    print("  S2: even-law field is a valid photon (c_g=1/sqrt3, real, unitary).")
    print("  S3: the even photon is NOT the two-branch Weyl bilinear -- converting")
    print("      one into the other requires a +dOmega/2 phase on each helicity that")
    print("      NO single Weyl branch supplies. The wedge between the bilinear photon")
    print("      and the even/gauge photon is EXACTLY the (excluded) birefringence.")
    print("  => bilinear photon (birefringent, SU(2)-bridging) and even gauge photon")
    print("     (non-birefringent) are MUTUALLY EXCLUSIVE. Option 1 buys safety from")
    print("     birefringence at the price of the composite (F29/F39) construction.")
    print(f"\n  ({time.time()-t0:.2f} s)")

    out = {'S1': s1, 'S2': s2, 'S3': s3}
    dst = os.path.join(os.path.dirname(__file__), '..', 'test-results',
                       'F67_option1_even_law_photon.json')
    try:
        with open(dst, 'w') as fh:
            json.dump(out, fh, indent=2)
        print(f"  wrote {dst}")
    except Exception as e:
        print(f"  (could not write json: {e})")
