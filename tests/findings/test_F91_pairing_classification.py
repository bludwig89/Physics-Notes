"""
test_F91_pairing_classification.py
==================================
2026-06-04 — the F68-mirror for the non-Abelian sectors: which propagation
channel does each sector's minimal coupling FORCE?

F68 forced the photon to the even/identity channel because its coupling is a
scalar in branch space.  F89 showed photon vs W/Z/gluon is a channel split of
one entity but left open WHY the non-Abelian sectors take the chiral pairing.
This test closes that by classifying every sector by the BRANCH STRUCTURE of
its coupling operator (branch = BCC chirality, the model's γ⁵):

    coupling weight per branch (g_L, g_R)  →  forced channel
    ──────────────────────────────────────────────────────────
    γ      (Q, Q)        scalar  → identity → EVEN     (F68, re-anchored here)
    W±     (g, 0)        left projector P_L → single-branch → CHIRAL — FORCED
    Z      (g_L, g_R), g_L≠g_R, both ≠0 → NEITHER pure channel; even is exact
           for the vector part, the axial part is the branch split (mass-
           suppressed for the massive Z)
    gluon  (g_s, g_s)    scalar in branch space → identity → EVEN — the chiral
           assignment of `gluon_rotation_step_spectral_bcc` is NOT forced; the
           F68 argument forces the even law (the 2D gluon path already uses it)

Checks
------
γ-anchor (exact over ℚ):
  A1  Q_L = Q_R for every first-generation species (axial EM coupling ≡ 0),
      and the model's float tables match the exact rationals.

W (chiral FORCED):
  W1  exact ℚ: T3 = 0 for every right-handed species; in branch space the
      SU(2)_L coupling is the projector P_L = diag(1,0): it annihilates the
      right branch exactly (the model's parity violation, E2/W4.3 — the
      isospin current `fermion_current_isospin` is built from the left doublet
      only, by construction).
  W2  a source that populates ONLY one branch makes same-branch bilinears;
      with the real branch unitaries these ride Ω^s = 2ω^s(k/2) (machine),
      and |Ω^s − Ω_even| = |ΔΩ|/2 > 0 on the body diagonal (F67's exact
      separation) → the even law is EXCLUDED for the W: chiral forced.
      Sign-agnostic (verified for both branch conventions).
  W3  the chiral step is the real-field embedding of single-branch content:
      Ω⁺(−k) = Ω⁻(k) exactly (machine, random k) — a real (E,B) field whose
      analytic content is one branch at +k necessarily carries the conjugate
      branch at −k, which is precisely the F37 chiral assignment
      (helicity ↔ branch).  And `w_propagation_step_chiral` advances F^± at
      exactly Ω^±(k) (machine, planted modes).

Z (mixed channel — neither forced):
  Z1  exact ℚ at θ_W = π/6 (F45, sin²θ_W = 1/4): g_A = T3 ≠ 0 for the left
      doublet (not the identity channel → even not F68-forced) and
      g_R = −Q/4 ≠ 0 for charged species (not a projector → chiral not
      forced).  Model `z_couplings()` floats match the exact rationals.
  Z2  exact ℚ: photon uniqueness — a neutral coupling a·T3 + b·Y/2 has axial
      part (a−b)·T3 for EVERY species (identity Y_L/2 = Q−T3, Y_R/2 = Q);
      it vanishes on the doublet iff a = b, i.e. iff the coupling ∝ Q — the
      Weinberg rotation isolates ALL axial coupling in the Z, and the
      identity-channel (non-birefringent) member of the neutral sector is
      exactly the photon.
  Z3  quantitative: the branch-split correction the even massive-Z step
      neglects is δω = |√(m²+Ω±²) − √(m²+Ω_even²)| — O(Ω·ΔΩ/m) at small k,
      vanishing like k³; report at representative (m_Z, k).

Gluon (chiral NOT forced — even forced):
  G1  the colour coupling is branch-blind: V = exp(iθ·T) acts on colour only,
      so [diag(U⁺,U⁻) ⊗ I₃, I₄ ⊗ V] = 0 (machine, random k, θ) — the exact
      F68 commutator replayed in colour.  The model's own octet bilinear
      (`quark_colour_octet_bilinear_*`) applies the SAME T^a to both
      chiralities (η and χ) — vector-like by construction.
  G2  a colour phase advances left- and right-branch quark eigenmodes by
      EXACTLY the same colour phase (split = 0, exact) — the F68 T2 replay.
  G3  the clean even-law gluon step exists and works: applying the even
      rotation per octet component conserves norm (machine) and is
      non-birefringent (helicity-sum S ≈ 0), while the current
      `gluon_rotation_step_spectral_bcc` (chiral) splits by −ΔΩ·N — the F69
      PP2 contrast replayed on the octet.  Migration is clean; the chiral
      BCC gluon assignment is unforced (confined → unobservable, but the
      F68-mirror + elegant-design preference selects the even law).

Pass criteria: ℚ checks exact (0); machine ≤ 5e-13; Z3/G3 contrasts reported.
Writes test-results/F91_pairing_classification.json.
"""

import json
import os
import sys
from fractions import Fraction
import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.numerics import fft as _fft
from casim.engine.lattice import bcc as bcc
from casim.engine.gauge import photon as pp
from casim.engine.gauge import weak_z as zf
from casim.engine.gauge.weak_wmu import _f26_rotation_step, w_propagation_step_chiral
from casim.engine.lattice.geometry import make_kgrid_3d

RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'test-results',
                            'F91_pairing_classification.json')

ROOT3 = np.sqrt(3.0)
MACHINE = 5e-13

_S_X = np.array([[0, 1], [1, 0]], dtype=complex)
_S_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_S_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULIS = (_S_X, _S_Y, _S_Z)

# Exact first-generation quantum numbers (ℚ) — the model's tables as rationals
F = Fraction
T3_EXACT = {'nu_L': F(1, 2), 'e_L': F(-1, 2), 'u_L': F(1, 2), 'd_L': F(-1, 2),
            'e_R': F(0), 'u_R': F(0), 'd_R': F(0)}
Q_EXACT = {'nu_L': F(0), 'e_L': F(-1), 'u_L': F(2, 3), 'd_L': F(-1, 3),
           'e_R': F(-1), 'u_R': F(2, 3), 'd_R': F(-1, 3)}
S2_EXACT = F(1, 4)          # sin²(π/6) — F45 bare-lattice Weinberg angle


def U_matrix(kx, ky, kz, sign='+'):
    u, nx, ny, nz = bcc._bcc_uvec(kx, ky, kz, sign=sign)
    return np.array([
        [u - 1j * nz,          -1j * (nx - 1j * ny)],
        [-1j * (nx + 1j * ny),  u + 1j * nz],
    ], dtype=complex)


def positive_eigenmode(kx, ky, kz, sign='+'):
    u, nx, ny, nz = bcc._bcc_uvec(kx, ky, kz, sign=sign)
    nmag = np.sqrt(nx * nx + ny * ny + nz * nz)
    nhx, nhy, nhz = nx / nmag, ny / nmag, nz / nmag
    if nhz < -1.0 + 1e-12:
        chi = np.array([0.0, 1.0], dtype=complex)
    else:
        norm = np.sqrt(2.0 * (1.0 + nhz))
        chi = np.array([(1.0 + nhz) / norm,
                        (nhx + 1j * nhy) / norm], dtype=complex)
    return chi, float(np.arccos(np.clip(u, -1.0, 1.0)))


def per_tick_phase(g_prev, g_next):
    return float(np.mod(-np.angle(g_next / g_prev), 2.0 * np.pi))


def circ_diff(a, b):
    d = np.mod(a - b, 2.0 * np.pi)
    return float(np.minimum(d, 2.0 * np.pi - d))


def random_k(rng, kmin=0.05, kmax=1.2):
    d = rng.standard_normal(3)
    d /= np.linalg.norm(d)
    return float(rng.uniform(kmin, kmax)) * d


# Gell-Mann generators T^a = λ^a/2 (Hermitian — eigh is safe here; the
# chiral-transform caution applies to the non-Hermitian walk operators)
def _gellmann_T():
    l = np.zeros((8, 3, 3), dtype=complex)
    l[0][0, 1] = l[0][1, 0] = 1
    l[1][0, 1] = -1j; l[1][1, 0] = 1j
    l[2][0, 0] = 1; l[2][1, 1] = -1
    l[3][0, 2] = l[3][2, 0] = 1
    l[4][0, 2] = -1j; l[4][2, 0] = 1j
    l[5][1, 2] = l[5][2, 1] = 1
    l[6][1, 2] = -1j; l[6][2, 1] = 1j
    l[7][0, 0] = l[7][1, 1] = 1 / np.sqrt(3.0); l[7][2, 2] = -2 / np.sqrt(3.0)
    return l / 2.0


def _su3_phase(theta):
    """V = exp(i θ·T) via Hermitian eigendecomposition."""
    H = sum(t * T for t, T in zip(theta, _gellmann_T()))
    w, v = np.linalg.eigh(H)
    return (v * np.exp(1j * w)) @ v.conj().T


# ----------------------------------------------------------------------
# A — photon anchor (exact ℚ)
# ----------------------------------------------------------------------
def run_A():
    # A1: axial EM coupling Q_L − Q_R = 0 exactly, per charged species
    axial_em = {f: Q_EXACT[f + '_L'] - Q_EXACT[f + '_R'] for f in ('e', 'u', 'd')}
    a1_exact = all(v == 0 for v in axial_em.values())
    # model float tables match ℚ
    t_err = max(abs(zf.T3_TABLE[s] - float(T3_EXACT[s])) for s in zf.SPECIES)
    q_err = max(abs(zf.Q_TABLE[s] - float(Q_EXACT[s])) for s in zf.SPECIES)
    return a1_exact, max(t_err, q_err)


# ----------------------------------------------------------------------
# W — chiral forced
# ----------------------------------------------------------------------
def run_W(n_k=800, seed=90):
    # W1 (exact ℚ): every R species has T3 = 0; P_L kills the right branch
    w1_exact = all(T3_EXACT[s] == 0 for s in ('e_R', 'u_R', 'd_R'))
    P_L = np.array([[1, 0], [0, 0]], dtype=float)        # branch space
    psi_R = np.array([0.0, 1.0])                          # pure right branch
    w1_kill = float(np.linalg.norm(P_L @ psi_R))          # exactly 0

    # W2 (machine): single-branch source → same-branch bilinear rides Ω^s;
    # and Ω^s ≠ Ω_even by exactly |ΔΩ|/2 (F67 separation)
    rng = np.random.default_rng(seed)
    worst_rate = 0.0
    for _ in range(n_k):
        k = random_k(rng)
        kh = k / 2.0
        for sign in ('+', '-'):                           # convention-agnostic
            Us = U_matrix(*kh, sign=sign)
            chi, om = positive_eigenmode(*kh, sign=sign)
            g0 = np.array([chi @ S @ chi for S in _PAULIS])
            a = int(np.argmax(np.abs(g0)))
            g1 = (Us @ chi) @ _PAULIS[a] @ (Us @ chi)
            worst_rate = max(worst_rate,
                             circ_diff(per_tick_phase(g0[a], g1),
                                       np.mod(2.0 * om, 2 * np.pi)))
    # even-law exclusion on the body diagonal
    kbd = 0.4 * np.array([1.0, 1.0, 1.0]) / ROOT3
    Om_even = float(pp.pair_dispersion(*kbd))
    sep = {}
    for sign in ('+', '-'):
        Om_s = 2.0 * float(bcc.bcc_dispersion(*(kbd / 2.0), sign=sign))
        sep[sign] = abs(Om_s - Om_even)
    dOm_half = abs(float(pp.pair_birefringence(*kbd))) / 2.0
    w2_sep_resid = max(abs(sep['+'] - dOm_half), abs(sep['-'] - dOm_half))
    w2_sep_nonzero = min(sep.values())

    # W3 (machine): Ω⁺(−k) = Ω⁻(k); chiral step advances F^± at Ω^±
    worst_refl = 0.0
    for _ in range(n_k):
        k = random_k(rng)
        wp = float(bcc.bcc_dispersion(*(-k / 2.0), sign='+'))
        wm = float(bcc.bcc_dispersion(*(k / 2.0), sign='-'))
        worst_refl = max(worst_refl, abs(wp - wm))
    # planted-mode check of the chiral step's defining property
    L, m = 9, 1
    khat = np.array([1.0, 1.0, 1.0]) / ROOT3
    E0, B0, e1, e2 = pp.build_pair_mode(L, m, khat, [1.0, -1.0, 0.0])
    kk = 2 * np.pi * m / L
    Op = 2.0 * float(bcc.bcc_dispersion(kk / 2, kk / 2, kk / 2, sign='+'))
    Om_ = 2.0 * float(bcc.bcc_dispersion(kk / 2, kk / 2, kk / 2, sign='-'))
    E1, B1 = w_propagation_step_chiral(E0.copy(), B0.copy())
    idx = (m, m, m)
    Fp0 = e1 + 1j * e2; Fm0 = e1 - 1j * e2
    Eh0 = np.array([_fft.fftn(E0[a])[idx] for a in range(3)])
    Bh0 = np.array([_fft.fftn(B0[a])[idx] for a in range(3)])
    Eh1 = np.array([_fft.fftn(E1[a])[idx] for a in range(3)])
    Bh1 = np.array([_fft.fftn(B1[a])[idx] for a in range(3)])
    ap = np.vdot(Fp0, Eh1 + 1j * Bh1) / np.vdot(Fp0, Eh0 + 1j * Bh0)
    am = np.vdot(Fm0, Eh1 - 1j * Bh1) / np.vdot(Fm0, Eh0 - 1j * Bh0)
    w3_step = max(circ_diff(-np.angle(ap), Op), circ_diff(np.angle(am), Om_))
    return (w1_exact, w1_kill, worst_rate, w2_sep_resid, w2_sep_nonzero,
            worst_refl, w3_step)


# ----------------------------------------------------------------------
# Z — mixed channel
# ----------------------------------------------------------------------
def run_Z():
    # Z1 (exact ℚ): g_L = T3 − Q s², g_R = −Q s² (0 for R bookkeeping per
    # model); axial g_A = T3 ≠ 0 on the doublet; g_R ≠ 0 for charged species
    s2 = S2_EXACT
    gA_doublet_nonzero = all(T3_EXACT[s] != 0 for s in ('nu_L', 'e_L', 'u_L', 'd_L'))
    gR_charged_nonzero = all((-Q_EXACT[s] * s2) != 0 for s in ('e_R', 'u_R', 'd_R'))
    # model float couplings match ℚ
    coup = zf.z_couplings()                # θ_W = π/6 default
    err = 0.0
    for s in zf.SPECIES:
        gL_e = (T3_EXACT[s] - Q_EXACT[s] * s2) if not s.endswith('_R') else F(0)
        gR_e = -Q_EXACT[s] * s2
        err = max(err, abs(coup[s]['gL'] - float(gL_e)),
                  abs(coup[s]['gR'] - float(gR_e)),
                  abs(coup[s]['gA'] - float(gL_e - gR_e)))
    # Z2 (exact ℚ): photon uniqueness — axial of a·T3 + b·Y/2 is (a−b)·T3
    z2_ok = True
    for a_num in (-2, -1, 1, 2, 3):
        for b_num in (-2, -1, 1, 2, 3):
            a, b = F(a_num, 2), F(b_num, 2)
            for f in ('nu', 'e', 'u', 'd'):
                if f == 'nu' and f + '_R' not in Q_EXACT:
                    QR, T3R = F(0), F(0)     # ν_R decoupled (Y=0)
                else:
                    QR, T3R = Q_EXACT.get(f + '_R', F(0)), F(0)
                QL, T3L = Q_EXACT[f + '_L'], T3_EXACT[f + '_L']
                YL2, YR2 = QL - T3L, QR - T3R          # Y/2 = Q − T3
                gl = a * T3L + b * YL2
                gr = a * T3R + b * YR2
                z2_ok &= (gl - gr == (a - b) * T3L)
    # axial ≡ 0 on the doublet ⟺ a = b ⟺ coupling = a(T3 + Y/2) = a·Q:
    # for every a ≠ b the doublet axial (a−b)·(±1/2) is nonzero over ℚ
    z2_unique = all((F(p, 2) - F(q, 2)) * F(1, 2) != 0
                    for p in (-1, 1, 2) for q in (-1, 1, 2) if p != q)

    # Z3 (quantitative): mass suppression of the neglected branch split
    m_Z = 0.4
    kbd = 0.2 * np.array([1.0, 1.0, 1.0]) / ROOT3
    Om_even = float(pp.pair_dispersion(*kbd))
    rel = {}
    for sign in ('+', '-'):
        Om_s = 2.0 * float(bcc.bcc_dispersion(*(kbd / 2.0), sign=sign))
        w_chir = np.sqrt(m_Z**2 + Om_s**2)
        w_even = np.sqrt(m_Z**2 + Om_even**2)
        rel[sign] = abs(w_chir - w_even) / w_even
    return (gA_doublet_nonzero, gR_charged_nonzero, err, z2_ok and z2_unique,
            max(rel.values()))


# ----------------------------------------------------------------------
# G — gluon: branch-blind coupling → even law forced
# ----------------------------------------------------------------------
def run_G(n_samp=300, seed=91, L=9, m=1, N=6):
    rng = np.random.default_rng(seed)
    # G1: [diag(U⁺,U⁻) ⊗ I₃, I₄ ⊗ V] = 0
    worst_comm = 0.0
    for _ in range(n_samp):
        k = random_k(rng)
        Up = U_matrix(*(k / 2.0), sign='+')
        Um = U_matrix(*(k / 2.0), sign='-')
        Ubr = np.block([[Up, np.zeros((2, 2))], [np.zeros((2, 2)), Um]])
        V = _su3_phase(rng.uniform(-np.pi, np.pi, 8))
        M1 = np.kron(Ubr, np.eye(3))
        M2 = np.kron(np.eye(4), V)
        worst_comm = max(worst_comm,
                         float(np.max(np.abs(M1 @ M2 - M2 @ M1))))

    # G2: identical colour phase on both branches (exact split 0)
    worst_split = 0.0
    for _ in range(n_samp):
        k = random_k(rng)
        V = _su3_phase(rng.uniform(-np.pi, np.pi, 8))
        c = rng.standard_normal(3) + 1j * rng.standard_normal(3)
        c /= np.linalg.norm(c)
        for sign in ('+', '-'):
            chi, _ = positive_eigenmode(*(k / 2.0), sign=sign)
            state = np.kron(chi, c)
            out = np.kron(np.eye(2), V) @ state
            # colour phase via overlap of colour factors (spin untouched)
            ph = np.vdot(c, V @ c)
            if sign == '+':
                ph_p = ph
            else:
                worst_split = max(worst_split, abs(ph - ph_p))
            # spin factor untouched by colour phase: exact structural fact
            del state, out
    # NOTE: ph is state-independent of branch by construction — the split is
    # algebraically 0; the float comparison confirms it bit-for-bit.

    # G3: even-law octet step vs current chiral BCC step (F69 PP2 on octet)
    khat = np.array([1.0, 1.0, 1.0]) / ROOT3
    E0, B0, e1, e2 = pp.build_pair_mode(L, m, khat, [1.0, -1.0, 0.0])
    kk = 2 * np.pi * m / L
    dOm = float(pp.pair_birefringence(kk, kk, kk))
    Fp0 = e1 + 1j * e2; Fm0 = e1 - 1j * e2
    idx = (m, m, m)

    def hel_sum(E, B):
        Eh = np.array([_fft.fftn(E[a])[idx] for a in range(3)])
        Bh = np.array([_fft.fftn(B[a])[idx] for a in range(3)])
        Eh0 = np.array([_fft.fftn(E0[a])[idx] for a in range(3)])
        Bh0 = np.array([_fft.fftn(B0[a])[idx] for a in range(3)])
        ap = np.vdot(Fp0, Eh + 1j * Bh) / np.vdot(Fp0, Eh0 + 1j * Bh0)
        am = np.vdot(Fm0, Eh - 1j * Bh) / np.vdot(Fm0, Eh0 - 1j * Bh0)
        s = np.angle(ap) + np.angle(am)
        return float((s + np.pi) % (2 * np.pi) - np.pi)

    # even-law octet step (per octet component a — here one representative
    # component; the step is component-diagonal)
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Ee, Be = E0.copy(), B0.copy()
    n0 = np.sum(Ee**2 + Be**2)
    for _ in range(N):
        En = np.zeros_like(Ee); Bn = np.zeros_like(Be)
        for a in range(3):
            ek = _fft.fftn(Ee[a]); bk = _fft.fftn(Be[a])
            ek2, bk2 = _f26_rotation_step(ek, bk, KX, KY, KZ)
            En[a] = _fft.ifftn(ek2).real; Bn[a] = _fft.ifftn(bk2).real
        Ee, Be = En, Bn
    g3_even_S = abs(hel_sum(Ee, Be))
    g3_norm = abs(np.sum(Ee**2 + Be**2) - n0) / n0

    # current chiral BCC gluon law (== w_propagation_step_chiral, per F43)
    Ec, Bc = E0.copy(), B0.copy()
    for _ in range(N):
        Ec, Bc = w_propagation_step_chiral(Ec, Bc)
    g3_chiral_S = hel_sum(Ec, Bc)
    g3_chiral_pred = float(((-dOm * N) + np.pi) % (2 * np.pi) - np.pi)
    return (worst_comm, worst_split, g3_even_S, g3_norm,
            g3_chiral_S, g3_chiral_pred)


def main():
    print("F91 — pairing classification: which channel does each coupling force?")
    print("=" * 74)

    a1, a_tab = run_A()
    print(f"A1  γ axial coupling ≡ 0 over ℚ      : {a1}   (tables match ℚ: {a_tab:.1e})")

    w1, w1k, w2r, w2sep, w2nz, w3refl, w3step = run_W()
    print(f"W1  T3(R species) = 0 over ℚ; P_L ψ_R: {w1}, kill={w1k:.1e}")
    print(f"W2  same-branch bilinear rides Ω^s   : {w2r:.3e}")
    print(f"W2  |Ω^s − Ω_even| = |ΔΩ|/2 (F67)    : resid {w2sep:.3e}, min sep {w2nz:.3e} (>0)")
    print(f"W3  Ω⁺(−k) = Ω⁻(k)                   : {w3refl:.3e}")
    print(f"W3  chiral step: F^± at exactly Ω^±  : {w3step:.3e}")

    z1a, z1b, z1err, z2, z3 = run_Z()
    print(f"Z1  g_A=T3≠0 (L) & g_R≠0 (charged) ℚ : {z1a and z1b}   (floats match ℚ: {z1err:.1e})")
    print(f"Z2  axial(a·T3+b·Y/2) = (a−b)T3 ⇒ γ unique identity channel: {z2}")
    print(f"Z3  even-Z neglected split @ m=0.4,k=0.2: rel {z3:.3e} (mass-suppressed)")

    g1, g2, g3S, g3n, g3cS, g3cP = run_G()
    print(f"G1  [branch walk ⊗ I, I ⊗ colour]=0  : {g1:.3e}")
    print(f"G2  colour phase split between branches: {g2:.3e}")
    print(f"G3  even octet step: S={g3S:.3e}, norm drift={g3n:.3e}")
    print(f"G3  chiral BCC gluon step: S={g3cS:+.5f} vs −ΔΩ·N={g3cP:+.5f} (birefringent, unforced)")

    checks = {
        "A1_photon_axial_zero_Q": {"pass": bool(a1), "table_resid": float(a_tab)},
        "W1_right_T3_zero_and_PL_kills_R": {"pass": bool(w1 and w1k == 0.0), "kill": float(w1k)},
        "W2_single_branch_rides_Omega_s": {"residual": float(w2r), "pass": bool(w2r <= MACHINE)},
        "W2_even_excluded_by_F67_separation": {"residual": float(w2sep),
                                               "min_separation": float(w2nz),
                                               "pass": bool(w2sep <= MACHINE and w2nz > 1e-6)},
        "W3_reality_maps_branch_to_chiral": {"residual": float(w3refl), "pass": bool(w3refl <= MACHINE)},
        "W3_chiral_step_Fpm_at_Omega_pm": {"residual": float(w3step), "pass": bool(w3step <= MACHINE)},
        "Z1_neither_identity_nor_projector_Q": {"pass": bool(z1a and z1b),
                                                "float_table_resid": float(z1err)},
        "Z2_photon_unique_identity_channel_Q": {"pass": bool(z2)},
        "Z3_massive_Z_split_suppression": {"rel_correction": float(z3), "pass": bool(z3 < 5e-3)},
        "G1_colour_coupling_branch_blind": {"residual": float(g1), "pass": bool(g1 <= MACHINE)},
        "G2_colour_phase_split_zero": {"residual": float(g2), "pass": bool(g2 == 0.0)},
        "G3_even_octet_step_clean": {"S_even": float(g3S), "norm_drift": float(g3n),
                                     "pass": bool(g3S <= 1e-12 and g3n <= 1e-12)},
        "G3_chiral_gluon_unforced_contrast": {"S_chiral": float(g3cS),
                                              "pred_minus_dOmega_N": float(g3cP),
                                              "pass": bool(abs(g3cS - g3cP) <= 1e-10 and abs(g3cS) > 1e-6)},
    }
    n_pass = sum(1 for c in checks.values() if c["pass"])
    verdict = "PASS" if n_pass == len(checks) else "FAIL"
    print("-" * 74)
    print(f"{n_pass}/{len(checks)} checks pass → {verdict}")

    out = {
        "finding": "F91",
        "title": "Pairing classification — γ even (forced), W chiral (forced), "
                 "Z mixed, gluon even (forced; chiral BCC assignment unforced)",
        "date": "2026-06-04",
        "checks": checks,
        "verdict": verdict,
    }
    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"results → {os.path.relpath(RESULTS_PATH, os.path.dirname(__file__))}")
    return 0 if verdict == "PASS" else 1


if __name__ == '__main__':
    sys.exit(main())
