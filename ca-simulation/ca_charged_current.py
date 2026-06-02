"""
ca_charged_current.py
=====================

FG-8 — Charged-current weak sector and the end-to-end β-decay process

        d  →  u + W⁻  →  u + e⁻ + ν̄_e

This module is *additive*: it introduces the raising / lowering structure
of the weak charged current on top of the already-verified pieces

  * left-handed SU(2)_L doublet bilinears        (F29, ``ca_wmu.fermion_isospin_current``)
  * the W-covariant Dirac doublet step           (F34, ``ca_wmu.covariant_dirac_doublet_step``)
  * the W-coupled quark doublet                   (FG-2/FG-3, ``test_FG3_quark_electroweak``)
  * dynamical W propagation + Proca mass          (F36, ``ca_wmu.w_*_propagation_step_*``)
  * the per-species charge registry               (F35/F48, ``ca_z_field``)

It changes no existing surface.

Conventions
-----------
Weak-isospin generators are ``T^a = τ^a / 2``.  The charge raising / lowering
generators are

    T⁺ = T¹ + i T² = [[0, 1], [0, 0]]      (raises:  down → up)
    T⁻ = T¹ − i T² = [[0, 0], [1, 0]]      (lowers:  up   → down)

with the SU(2) algebra

    [T³, T±] = ± T± ,        [T⁺, T⁻] = 2 T³ = τ³ .

A left-handed doublet is written ψ_L = (f_up, f_down) where ``f_*`` is the
*upper* Weyl component (the only one that couples to W — parity violation,
F34/W4.3).  For the lepton doublet (up, down) = (ν, e); for the quark
doublet (up, down) = (u, d).

The site-local charged currents are the complex bilinears

    J⁺(x) = ψ_L†(x) T⁺ ψ_L(x) = f_up*(x) · f_down(x)          (= J¹ + i J²)
    J⁻(x) = ψ_L†(x) T⁻ ψ_L(x) = f_down*(x) · f_up(x) = J⁺(x)*  (= J¹ − i J²)

so ``J^±`` are exactly ``J1 ± i J2`` of ``ca_wmu.fermion_isospin_current``.

The W field is real per isospin component, ``(E_W, B_W)`` of shape
``(3, L, L, L)`` as in ``ca_wmu``.  The charged (mass-eigenstate) W bosons are

    W⁺ = (W¹ − i W²)/√2 ,        W⁻ = (W¹ + i W²)/√2 ,

and the gauge-invariant interaction is

    L_cc = (g/√2) ( W⁺_μ J⁺^μ + W⁻_μ J⁻^μ ) .

For the d → u transition the quark current that emits the W⁻ is the
*raising* current J⁺_quark = u*_L d_L; the leptonic vertex W⁻ → e⁻ ν̄_e is
the conjugate lowering current J⁻_lepton = e*_L ν_L.

Fermi limit
-----------
Integrating out a heavy W (momentum transfer |q²| ≪ m_W²) gives the
four-fermion contact interaction with

    G_F / √2 = g² / (8 m_W²) .

References:  first-gen-completeness.md §5.1 FG-8;  findings/F34*, F36, F48.
"""

import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np

from ca_wmu import (
    fermion_isospin_current,
    w_propagation_step_spectral,
    w_massive_propagation_step_spectral,
    w_sourced_propagation_step,
)


# ════════════════════════════════════════════════════════════════════
#  1.  Isospin raising / lowering generators (T^a = τ^a / 2)
# ════════════════════════════════════════════════════════════════════

# Pauli matrices in isospin space
TAU1 = np.array([[0, 1], [1, 0]], dtype=complex)
TAU2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
TAU3 = np.array([[1, 0], [0, -1]], dtype=complex)

# Weak-isospin generators
T1 = TAU1 / 2.0
T2 = TAU2 / 2.0
T3 = TAU3 / 2.0

# Raising / lowering
T_PLUS = T1 + 1j * T2     # [[0,1],[0,0]] — down → up
T_MINUS = T1 - 1j * T2    # [[0,0],[1,0]] — up   → down


def commutator(A, B):
    """[A, B] = A·B − B·A for square matrices."""
    return A @ B - B @ A


def su2_raising_algebra_residuals():
    """
    Return the residuals of the SU(2) charged-current algebra:

        r1 = ‖[T³, T⁺] − T⁺‖
        r2 = ‖[T³, T⁻] + T⁻‖
        r3 = ‖[T⁺, T⁻] − 2 T³‖
        r4 = ‖T⁺ − (T¹ + i T²)‖     (definition cross-check)

    All four are exactly zero for half-integer matrices.
    """
    r1 = np.max(np.abs(commutator(T3, T_PLUS) - T_PLUS))
    r2 = np.max(np.abs(commutator(T3, T_MINUS) + T_MINUS))
    r3 = np.max(np.abs(commutator(T_PLUS, T_MINUS) - 2.0 * T3))
    r4 = np.max(np.abs(T_PLUS - (T1 + 1j * T2)))
    return {'[T3,T+]-T+': float(r1), '[T3,T-]+T-': float(r2),
            '[T+,T-]-2T3': float(r3), 'T+ def': float(r4)}


# Isospin eigenstates (up = +1/2, down = −1/2)
KET_UP = np.array([1, 0], dtype=complex)     # u  or  ν
KET_DOWN = np.array([0, 1], dtype=complex)   # d  or  e


def raise_isospin(ket):
    """Apply T⁺ to a 2-component isospin ket (down → up)."""
    return T_PLUS @ ket


def lower_isospin(ket):
    """Apply T⁻ to a 2-component isospin ket (up → down)."""
    return T_MINUS @ ket


# ════════════════════════════════════════════════════════════════════
#  2.  Charged-current site bilinears  J^±(x)
# ════════════════════════════════════════════════════════════════════

def charged_current_plus(f_up, f_down):
    """
    Raising charged current J⁺(x) = f_up*(x) · f_down(x)  (= J¹ + i J²).

    For the quark doublet (f_up, f_down) = (u_L, d_L) this is the d → u
    transition current that emits the W⁻.
    """
    return np.conj(f_up) * f_down


def charged_current_minus(f_up, f_down):
    """
    Lowering charged current J⁻(x) = f_down*(x) · f_up(x) = J⁺(x)*.

    For the lepton doublet (f_up, f_down) = (ν_L, e_L) the conjugate of
    this is the W⁻ → e⁻ ν̄_e vertex.
    """
    return np.conj(f_down) * f_up


def charged_current_from_isospin(f_up, f_down):
    """
    Build (J⁺, J⁻) from the real isospin current J^a of
    ``ca_wmu.fermion_isospin_current`` and verify J± = J1 ± i J2.

    Returns
    -------
    Jp, Jm : complex arrays  — J⁺ = J1 + i J2,  J⁻ = J1 − i J2.
    """
    J = fermion_isospin_current(f_up, f_down)   # (3, L, L, L): J1, J2, J3
    Jp = J[0] + 1j * J[1]
    Jm = J[0] - 1j * J[1]
    return Jp, Jm


# ════════════════════════════════════════════════════════════════════
#  3.  V−A structure / maximal parity violation
# ════════════════════════════════════════════════════════════════════

# Dirac matrices (Weyl/chiral basis) for the V−A projector check
_GAMMA5 = np.diag([-1, -1, 1, 1]).astype(complex)   # chiral basis: P_L upper
_I4 = np.eye(4, dtype=complex)
P_L = (_I4 - _GAMMA5) / 2.0     # left projector  → upper two components
P_R = (_I4 + _GAMMA5) / 2.0     # right projector → lower two components


def va_vertex_kills_right_handed():
    """
    Maximal parity violation: the charged-current vertex carries the
    projector P_L = (1 − γ⁵)/2.  Acting on a purely right-handed spinor
    it gives exactly zero; on a left-handed spinor it is the identity.

    Returns (resid_right, resid_left):
        resid_right = ‖P_L ψ_R‖              (should be 0)
        resid_left  = ‖P_L ψ_L − ψ_L‖        (should be 0)
    """
    psi_R = np.array([0, 0, 1, 1], dtype=complex)   # right-handed (lower)
    psi_L = np.array([1, 1, 0, 0], dtype=complex)   # left-handed (upper)
    resid_right = np.max(np.abs(P_L @ psi_R))
    resid_left = np.max(np.abs(P_L @ psi_L - psi_L))
    return float(resid_right), float(resid_left)


# ════════════════════════════════════════════════════════════════════
#  4.  First-generation charge / baryon / lepton registry  (exact ℚ)
# ════════════════════════════════════════════════════════════════════

#  Q = T3 + Y/2 ;   values stored as exact Fractions.
#                        T3            Y            B           L
QUANTUM_NUMBERS = {
    'u':       dict(T3=Fraction(1, 2),  Y=Fraction(1, 3),  B=Fraction(1, 3), L=Fraction(0)),
    'd':       dict(T3=Fraction(-1, 2), Y=Fraction(1, 3),  B=Fraction(1, 3), L=Fraction(0)),
    'nu':      dict(T3=Fraction(1, 2),  Y=Fraction(-1),    B=Fraction(0),    L=Fraction(1)),
    'e':       dict(T3=Fraction(-1, 2), Y=Fraction(-1),    B=Fraction(0),    L=Fraction(1)),
    # Antiparticles (used for the ν̄_e final state)
    'nubar':   dict(T3=Fraction(-1, 2), Y=Fraction(1),     B=Fraction(0),    L=Fraction(-1)),
    'eplus':   dict(T3=Fraction(1, 2),  Y=Fraction(1),     B=Fraction(0),    L=Fraction(-1)),
    # Gauge bosons
    'W-':      dict(Q=Fraction(-1), B=Fraction(0), L=Fraction(0)),
    'W+':      dict(Q=Fraction(1),  B=Fraction(0), L=Fraction(0)),
}


def charge(species):
    """Electric charge Q = T3 + Y/2 (exact Fraction).  Bosons carry Q directly."""
    qn = QUANTUM_NUMBERS[species]
    if 'Q' in qn:
        return qn['Q']
    return qn['T3'] + qn['Y'] / 2


def baryon_number(species):
    return QUANTUM_NUMBERS[species]['B']


def lepton_number(species):
    return QUANTUM_NUMBERS[species]['L']


def conservation_residuals(initial, final):
    """
    Exact (Fraction) conservation check for a process  initial → final.

    ``initial`` and ``final`` are lists of species names.  Returns a dict of
    ΔQ, ΔB, ΔL, Δ(B−L); each is an exact Fraction equal to 0 if conserved.
    """
    def tot(states, fn):
        return sum((fn(s) for s in states), Fraction(0))
    dQ = tot(final, charge) - tot(initial, charge)
    dB = tot(final, baryon_number) - tot(initial, baryon_number)
    dL = tot(final, lepton_number) - tot(initial, lepton_number)
    dBL = (tot(final, baryon_number) - tot(final, lepton_number)) \
        - (tot(initial, baryon_number) - tot(initial, lepton_number))
    return {'dQ': dQ, 'dB': dB, 'dL': dL, 'dB-L': dBL}


# ════════════════════════════════════════════════════════════════════
#  5.  Charged W mass-eigenstate fields  W± = (W¹ ∓ i W²)/√2
# ════════════════════════════════════════════════════════════════════

_SQRT2 = np.sqrt(2.0)


def w_charged_components(F_W):
    """
    Form the complex charged-W components from the isospin triplet field
    ``F_W`` (either E_W or B_W, shape (3, L, L, L)):

        F(W⁺) = (F¹ − i F²)/√2
        F(W⁻) = (F¹ + i F²)/√2

    Returns (F_Wp, F_Wm).
    """
    Wp = (F_W[0] - 1j * F_W[1]) / _SQRT2
    Wm = (F_W[0] + 1j * F_W[1]) / _SQRT2
    return Wp, Wm


def emit_w_minus(E_W, B_W, f_up, f_down, g_lat=1.0, dt=1.0):
    """
    One emission step:  source the W triplet with the *quark* charged
    current, then read off the W⁻ field that has been produced.

    The triplet source uses J¹, J² from the quark doublet; after the
    additive kick (``ca_wmu.w_sourced_propagation_step``)

        ΔE¹ = g J¹ dt ,   ΔE² = g J² dt ,

    the W⁻ component picks up

        ΔE(W⁻) = (ΔE¹ + i ΔE²)/√2 = (g/√2) (J¹ + i J²) dt = (g/√2) J⁺ dt ,

    i.e. the W⁻ field is sourced by the raising current J⁺ exactly — this
    is the d → u + W⁻ vertex.

    Returns
    -------
    E_W_new, B_W_new : updated triplet fields
    dE_Wm_expected   : (g/√2) J⁺ dt — the analytic W⁻ source kick
    """
    J = fermion_isospin_current(f_up, f_down)        # (3, L, L, L)
    E_W_new, B_W_new = w_sourced_propagation_step(E_W, B_W, J, dt=dt, g_lat=g_lat)
    Jp = J[0] + 1j * J[1]                            # J⁺ = J¹ + i J²
    dE_Wm_expected = (g_lat / _SQRT2) * Jp * dt
    return E_W_new, B_W_new, dE_Wm_expected


# ════════════════════════════════════════════════════════════════════
#  6.  Fermi effective coupling  (heavy-W limit)
# ════════════════════════════════════════════════════════════════════

def fermi_constant(g, m_W):
    """Tree-level Fermi coupling  G_F/√2 = g² / (8 m_W²)."""
    return g ** 2 / (8.0 * m_W ** 2)


def w_exchange_amplitude(g, m_W, q2):
    """
    Charged-current amplitude factor from single-W exchange at (Euclidean,
    spacelike) momentum-transfer-squared ``q2`` ≥ 0:

        A(q²) = g² / [ 8 (m_W² + q²) ] .

    At q² → 0 this is exactly ``fermi_constant(g, m_W)``; the relative
    deviation is  −q²/(m_W² + q²)  ≈ −q²/m_W²  for q² ≪ m_W².
    """
    return g ** 2 / (8.0 * (m_W ** 2 + q2))


def fermi_limit_relative_deviation(g, m_W, q2):
    """(A(q²) − G_F/√2) / (G_F/√2)  =  −q²/(m_W² + q²)."""
    A = w_exchange_amplitude(g, m_W, q2)
    GF = fermi_constant(g, m_W)
    return (A - GF) / GF


# ════════════════════════════════════════════════════════════════════
#  7.  End-to-end β-decay pipeline (integration driver)
# ════════════════════════════════════════════════════════════════════

def gaussian_blob(shape, center, sigma, amp=1.0):
    """Real Gaussian profile on a 3D lattice (helper for localized states)."""
    L = shape[0]
    idx = np.indices(shape)
    r2 = np.zeros(shape, dtype=float)
    for ax in range(3):
        d = idx[ax] - center[ax]
        d = (d + L // 2) % L - L // 2          # periodic minimal image
        r2 = r2 + d ** 2
    return amp * np.exp(-r2 / (2.0 * sigma ** 2))


def run_beta_decay_pipeline(L=16, m_W=0.6, g_lat=0.8, n_prop=24,
                            site_A=None, site_B=None, sigma=1.5, seed=2026):
    """
    End-to-end d → u + W⁻ → u + e⁻ + ν̄_e integration run.

    1.  A localized left-handed quark doublet at site A carries both a
        u and a d amplitude (so J⁺_quark = u* d ≠ 0 there).
    2.  The quark charged current sources the W triplet (``emit_w_minus``);
        the produced W⁻ field is recorded.
    3.  The W⁻ field propagates with the Proca step for ``n_prop`` ticks.
    4.  At a distant site B (initially lepton vacuum) we measure the W⁻
        field that has arrived and the leptonic absorption current
        J⁻_lepton ∝ W⁻ — driving e⁻ + ν̄_e production.

    Returns a dict of integration diagnostics (all real, JSON-serializable).
    """
    if site_A is None:
        site_A = (L // 4, L // 2, L // 2)
    if site_B is None:
        site_B = (3 * L // 4, L // 2, L // 2)
    shape = (L, L, L)
    rng = np.random.default_rng(seed)

    # --- 1. quark doublet localized at A (u and d both populated) ---
    profA = gaussian_blob(shape, site_A, sigma)
    f_u = profA.astype(complex) * (0.9 + 0.0j)
    f_d = profA.astype(complex) * (0.7 * np.exp(0.3j))
    # right-handed singlet content that must NOT couple
    chi_u = profA.astype(complex) * 0.5
    chi_d = profA.astype(complex) * 0.4

    quark_norm0 = float(np.sum(np.abs(f_u) ** 2 + np.abs(f_d) ** 2))

    # --- 2. emit W⁻ ---
    E_W = np.zeros((3,) + shape)
    B_W = np.zeros((3,) + shape)
    E_W, B_W, dE_Wm_expected = emit_w_minus(E_W, B_W, f_u, f_d,
                                            g_lat=g_lat, dt=1.0)
    _, E_Wm = w_charged_components(E_W)
    w_at_A_emit = float(np.abs(E_Wm[site_A]))
    w_at_B_emit = float(np.abs(E_Wm[site_B]))

    # field energy injected (∝ Σ|J⁺|² g²/2)
    Jp_quark = charged_current_plus(f_u, f_d)
    cc_injected = float(np.sum(np.abs(Jp_quark) ** 2))

    # --- 3. propagate W⁻ (Proca) ---
    w_at_B_trace = []
    for _ in range(n_prop):
        E_W, B_W = w_massive_propagation_step_spectral(E_W, B_W, m_W, dt=1.0)
        _, E_Wm_t = w_charged_components(E_W)
        w_at_B_trace.append(float(np.abs(E_Wm_t[site_B])))

    _, E_Wm_final = w_charged_components(E_W)
    w_at_B_final = float(np.abs(E_Wm_final[site_B]))

    # --- 4. lepton absorption at B: J⁻_lepton ∝ W⁻ ---
    # the arriving W⁻ drives an e⁻ ν̄_e amplitude; we report the magnitude
    # of the leptonic charged-current response and which component lights up
    lepton_response = w_at_B_final * g_lat / _SQRT2

    # global electric-charge bookkeeping (exact Fractions → float)
    cons = conservation_residuals(['d'], ['u', 'e', 'nubar'])

    return {
        'L': L, 'm_W': m_W, 'g_lat': g_lat, 'n_prop': n_prop,
        'site_A': list(site_A), 'site_B': list(site_B),
        'quark_norm0': quark_norm0,
        'cc_injected_sum|J+|^2': cc_injected,
        'dE_Wminus_expected_maxabs': float(np.max(np.abs(dE_Wm_expected))),
        'w_at_A_on_emit': w_at_A_emit,
        'w_at_B_on_emit': w_at_B_emit,            # ~0: causal — not yet arrived
        'w_at_B_final': w_at_B_final,             # >0: signal has propagated in
        'w_at_B_max_over_trace': float(max(w_at_B_trace)),
        'lepton_cc_response_at_B': lepton_response,
        'dQ': float(cons['dQ']), 'dB': float(cons['dB']),
        'dL': float(cons['dL']), 'dB-L': float(cons['dB-L']),
    }
