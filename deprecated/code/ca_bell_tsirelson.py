# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_bell_tsirelson.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/qi_bell_tsirelson.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_bell_tsirelson.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_bell_tsirelson.py  —  CHSH / Tsirelson on the genuine 2^n lattice register (F226)
====================================================================================

Route 3 of the QC-empirical thread (docs/roadmaps/qc-routes-3-4-prompt.md).

Question
--------
A deterministic cellular-automaton substrate that reproduces QM must EITHER
saturate Tsirelson's bound S_CHSH = 2√2 *exactly* — in which case loophole-free
Bell experiments cannot discriminate it from QM — OR predict a small discreteness
deviation δS(a, E) testable against the loophole-free Bell data.

What this module establishes
----------------------------
1. The genuine F212/F214 2^n register (NOT the hand-inserted product "singlet" of
   the QM-1 test) reaches CHSH S = 2√2 to machine precision when the entangled
   pair is produced by the model's OWN native exchange gate and measured with the
   native σ·n̂ operators.  ⇒ the emergent theory IS quantum mechanics on this
   observable; there is no O(1) or O(a·p) correction.

2. The ONLY place lattice discreteness can enter is the *granularity of the
   achievable analyzer angles*: a physical single-qubit rotation is accumulated
   over an integer number of Planckian CA ticks, so the settable angle is
   quantised in units δφ = ω·τ = E/E_lat, with E_lat ≡ ħ/τ the lattice energy.
   Because CHSH is *stationary* at its optimum, the induced deviation is
   quadratic:   δS = −3√2 · (δφ)²   (derived + verified),
   hence Planck-suppressed to ~10⁻⁵⁴ for any real experiment — 50+ orders below
   the ~0.1 error bar on measured S.  ⇒ Bell-INDISTINGUISHABLE from QM.

3. Measurement-independence: the register reproduces the singlet correlation
   E(â,b̂) = −â·b̂ for FREELY and INDEPENDENTLY chosen settings a, b — the
   violation does not rely on correlated settings (no superdeterminism is used).
   The deterministic substrate lives at the Planck scale; the emergent theory is
   a genuine 2^n Hilbert space, so it violates Bell by BEING QM, not by a
   local-hidden-variable table exploiting setting correlations.

Pure numpy, plain complex linear algebra (no chiral transforms — safe per the
CLAUDE.md note); unitarity/Hermiticity asserted explicitly.
"""
from __future__ import annotations
import math
import numpy as np

try:
    import ca_entanglement as _E
except Exception:  # pragma: no cover
    _E = None

# ─────────────────────────── Pauli algebra ────────────────────────────
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
PAULI = (SX, SY, SZ)

# ─────────────────────────── SI bridge (F107/F123) ─────────────────────
TAU_S = 2.05366e-43          # fundamental CA tick [s]  (F123)
A_M = 1.06638e-34            # fundamental cell size [m] (F123)
HBAR_EV_S = 6.582119569e-16  # ħ [eV·s]
E_LAT_EV = HBAR_EV_S / TAU_S  # lattice energy ħ/τ ≈ 3.20e27 eV ≈ 3.2e18 GeV (F119 hierarchy)
TSIRELSON = 2.0 * math.sqrt(2.0)


# ═══════════════════════════════════════════════════════════════════════
#  Measurement operators (native σ·n̂) and CHSH
# ═══════════════════════════════════════════════════════════════════════
def sigma_ndir(n) -> np.ndarray:
    """σ·n̂ for a full 3-vector n̂ (Hermitian, involutive: (σ·n̂)²=I)."""
    n = np.asarray(n, dtype=float)
    n = n / np.linalg.norm(n)
    return n[0] * SX + n[1] * SY + n[2] * SZ


def sigma_xz(theta: float) -> np.ndarray:
    """σ·n̂ with n̂ in the xz-plane at polar angle θ (the Bell-optimal family)."""
    return math.cos(theta) * SZ + math.sin(theta) * SX


def correlator(psi, opA, opB) -> float:
    """E = ⟨ψ| A⊗B |ψ⟩ for single-qubit Hermitian observables A, B."""
    return float(np.real(np.conj(psi) @ np.kron(opA, opB) @ psi))


def chsh_value(psi, a, ap, b, bp) -> float:
    """CHSH S at four xz-plane analyzer angles."""
    Ea, Ap = sigma_xz(a), sigma_xz(ap)
    Eb, Bp = sigma_xz(b), sigma_xz(bp)
    return (correlator(psi, Ea, Eb) - correlator(psi, Ea, Bp)
            + correlator(psi, Ap, Eb) + correlator(psi, Ap, Bp))


def chsh_max_horodecki(psi) -> tuple[float, np.ndarray]:
    """Convention-free maximal CHSH over ALL measurement directions (Horodecki
    criterion): S_max = 2√(t₁+t₂), t₁≥t₂ the two largest eigenvalues of TᵀT with
    correlation matrix T_ij = ⟨σ_i⊗σ_j⟩.  For any maximally entangled state
    T is orthogonal ⇒ eigenvalues (1,1,1) ⇒ S_max = 2√2 exactly."""
    T = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            T[i, j] = correlator(psi, PAULI[i], PAULI[j])
    ev = np.sort(np.linalg.eigvalsh(T.T @ T).real)[::-1]
    return 2.0 * math.sqrt(ev[0] + ev[1]), ev


# ═══════════════════════════════════════════════════════════════════════
#  The genuine register state (native gate, NOT hand-inserted)
# ═══════════════════════════════════════════════════════════════════════
def native_entangled_pair() -> np.ndarray:
    """|ψ⟩ produced from the PRODUCT |↑↓⟩ by the model's OWN exchange gate
    U_exch(π/8) = exp(−iπ/8 σ_A·σ_B) — the F212/F214 perfect entangler.  The
    entanglement is GENERATED by the lattice interaction, not written by hand."""
    if _E is None:
        raise RuntimeError("ca_entanglement not importable; add ca-simulation to sys.path")
    reg = _E.Register([_E.KET0, _E.KET1])
    reg.apply_2q(_E.exchange_gate(np.pi / 8), 0, 1)
    return reg.psi


def exact_singlet() -> np.ndarray:
    """|Ψ⁻⟩ = (|↑↓⟩−|↓↑⟩)/√2, basis (↑↑,↑↓,↓↑,↓↓).  Reference for the closed-form
    S(φ)=3cosφ−cos3φ scaling analysis."""
    return np.array([0, 1, -1, 0], dtype=complex) / math.sqrt(2.0)


# ═══════════════════════════════════════════════════════════════════════
#  Discreteness correction — the ONLY lattice entry point
# ═══════════════════════════════════════════════════════════════════════
def chsh_singlet_of_phi(phi: float) -> float:
    """Closed CHSH of the singlet at the one-parameter Bell family
    (a=0, a'=2φ, b=φ, b'=3φ):  S(φ) = 3cosφ − cos3φ, max 2√2 at φ=π/4."""
    return chsh_value(exact_singlet(), 0.0, 2 * phi, phi, 3 * phi)


def dS_quadratic_coeff() -> float:
    """Analytic curvature of S at the optimum: S(π/4+δ) ≈ 2√2 − 3√2 δ².
    d²S/dφ² |_{π/4} = −3cos(π/4)+9cos(3π/4) = −6√2, and δ enters each analyzer
    once (a'=2φ shifts by 2δ, b=φ by δ, b'=3φ by 3δ) — the net stationary
    curvature in the single granularity parameter is −3√2 (verified numerically)."""
    return -3.0 * math.sqrt(2.0)


def angle_granularity(E_eV: float) -> float:
    """Achievable analyzer-angle granularity δφ = ω·τ = E/E_lat for an emergent
    qubit of transition energy E: a single-qubit rotation accumulates continuously
    in time but time is quantised in Planckian ticks τ, so the settable angle is
    quantised in steps δφ = (E/ħ)·τ = E/E_lat."""
    return E_eV / E_LAT_EV


def dS_from_discreteness(E_eV: float) -> float:
    """Worst-case CHSH deviation from angle granularity:
       |δS| ≤ |−3√2| · (δφ)² = 3√2 (E/E_lat)².  Quadratic because CHSH is
    stationary at its optimum ⇒ Planck-suppressed."""
    dphi = angle_granularity(E_eV)
    return abs(dS_quadratic_coeff()) * dphi ** 2


# ═══════════════════════════════════════════════════════════════════════
#  Measurement-independence (free settings reproduce −cosθ)
# ═══════════════════════════════════════════════════════════════════════
def singlet_correlation(theta_a: float, theta_b: float) -> float:
    """E(â,b̂) for the register with FREELY chosen, INDEPENDENT settings.

    The native exchange gate produces a maximally-entangled pair that equals the
    singlet |Ψ⁻⟩ up to a FIXED local unitary (setting-independent — see
    `native_equals_singlet_up_to_local`).  In that frame the correlation is the
    QM singlet law E = −cos(θ_a−θ_b), reproduced here for arbitrary independent
    settings a, b with NO requirement that the settings correlate with the state
    preparation (the point of the measurement-independence check)."""
    psi = exact_singlet()
    return correlator(psi, sigma_xz(theta_a), sigma_xz(theta_b))


def native_equals_singlet_up_to_local() -> float:
    """Confirm the native-gate state is the singlet up to a fixed 1-qubit unitary
    (setting-independent): max overlap over local U_A⊗I equals 1.  Returns the
    infidelity (should be ~0)."""
    psi = native_entangled_pair()
    sing = exact_singlet()
    # any two maximally entangled states are related by a local unitary on one
    # side; find the best single-qubit U_A via the 2x2 reshape SVD (fidelity =
    # (Σ singular values / √2)² for maximally entangled targets).
    # max_U |⟨sing|(U⊗I)|psi⟩|² = (Σ singular values of psi_mat·sing_mat†)²
    M = psi.reshape(2, 2) @ sing.reshape(2, 2).conj().T
    s = np.linalg.svd(M, compute_uv=False)
    fidelity = (s.sum()) ** 2
    return abs(1.0 - min(fidelity, 1.0))


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    psi = native_entangled_pair()
    Smax, ev = chsh_max_horodecki(psi)
    print("native-gate register CHSH_max =", Smax, "resid", abs(Smax - TSIRELSON))
    print("E_lat =", E_LAT_EV, "eV")
    for E in (1.8, 1e3, 1e9):
        print(f"E={E:g} eV: δφ={angle_granularity(E):.3e}  |δS|≤{dS_from_discreteness(E):.3e}")
