# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_quantum_noise.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/qi_noise.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_quantum_noise.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_quantum_noise.py  —  decoherence channels + stabilizer error correction (F221)
=================================================================================

The register/algorithm sectors (F212/F218/F219) are exact-unitary, and the
field-native fermion sector (F220) carries a *native* decoherence source —
virtual **doublon leakage** out of the one-per-site qubit subspace.  To study
fault tolerance the engine needs (a) an explicit noise channel and (b) an error-
correcting code.  This module supplies both, built on the model's own native
gate set (`ca_entanglement`: exchange-derived CNOT + SU(2) rotors).

Density-matrix formalism (exact channel averaging)
--------------------------------------------------
A noise channel is a set of Kraus operators {E_k} with Σ E_k†E_k = I acting as
    ρ → Σ_k E_k ρ E_k† .
We carry the full 2ⁿ×2ⁿ density matrix (small n), so the channel is applied
*exactly* — no Monte-Carlo sampling.  The single-qubit Pauli operators are the
model's own (X,Y,Z from the SU(2) rotor); amplitude damping is the standard
non-unital channel.

Codes
-----
  * 3-qubit bit-flip code  — corrects one X error;  stabilizers Z₀Z₁, Z₁Z₂.
  * 3-qubit phase-flip code — Hadamard-dual; corrects one Z error.
  * 9-qubit Shor code       — corrects an ARBITRARY single-qubit error (X,Y,Z).

Recovery is stabilizer syndrome extraction by projective measurement followed by
the Pauli correction, expressed on the density matrix as
    ρ → Σ_s C_s P_s ρ P_s C_s† ,
with {P_s} the syndrome projectors (a complete orthogonal set) and C_s the
recovery Pauli for syndrome s.  This is exact and deterministic.
"""
from __future__ import annotations

import numpy as np

try:
    import ca_entanglement as _E
except Exception:  # pragma: no cover
    _E = None

# Pauli matrices (the model's own; X,Z are ±i·su2_rotor(π/2,·) up to phase)
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)


# ─────────────────────────── embedding helpers ─────────────────────────────
def embed(op1, q, n):
    """Embed a single-qubit operator on qubit `q` (q=0 is most significant)."""
    mats = [op1 if i == q else I2 for i in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def embed2(op2, q0, q1, n):
    """Embed a 4×4 two-qubit operator on (q0,q1) into the full 2ⁿ operator."""
    dim = 2 ** n
    out = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        v = np.zeros(dim, dtype=complex); v[col] = 1.0
        out[:, col] = _E.apply_gate(v, op2, [q0, q1], n)
    return out


def density(psi):
    return np.outer(psi, psi.conj())


def fidelity(rho, psi_target):
    """⟨ψ|ρ|ψ⟩ — fidelity of a (possibly mixed) ρ with a pure target."""
    return float(np.real(psi_target.conj() @ rho @ psi_target))


# ─────────────────────────── Kraus noise channels ──────────────────────────
def kraus_bitflip(p):
    return [np.sqrt(1 - p) * I2, np.sqrt(p) * X]


def kraus_phaseflip(p):
    return [np.sqrt(1 - p) * I2, np.sqrt(p) * Z]


def kraus_depolarizing(p):
    """Depolarizing: with prob p replace by maximally mixed; Kraus form
    E0=√(1−3p/4)I, E_{X,Y,Z}=√(p/4)·{X,Y,Z}."""
    return [np.sqrt(1 - 3 * p / 4) * I2, np.sqrt(p / 4) * X,
            np.sqrt(p / 4) * Y, np.sqrt(p / 4) * Z]


def kraus_amp_damp(gamma):
    """Amplitude damping (non-unital): E0=diag(1,√(1−γ)), E1=√γ|0⟩⟨1|."""
    E0 = np.array([[1, 0], [0, np.sqrt(1 - gamma)]], dtype=complex)
    E1 = np.array([[0, np.sqrt(gamma)], [0, 0]], dtype=complex)
    return [E0, E1]


def apply_channel(rho, kraus, q, n):
    """Apply a single-qubit Kraus channel to qubit `q` of an n-qubit ρ."""
    out = np.zeros_like(rho)
    for Ek in kraus:
        Efull = embed(Ek, q, n)
        out = out + Efull @ rho @ Efull.conj().T
    return out


def apply_channel_all(rho, kraus, n, qubits=None):
    """Apply the same single-qubit channel independently to each qubit."""
    qubits = range(n) if qubits is None else qubits
    for q in qubits:
        rho = apply_channel(rho, kraus, q, n)
    return rho


# ───────────────────────── native encoders (state vectors) ─────────────────
def _cnot(psi, c, t, n):
    return _E.apply_gate(psi, _E.native_cnot(), [c, t], n)


def _had(psi, q, n):
    return _E.apply_gate(psi, _E.native_hadamard(), [q], n)


def encode_bitflip(alpha, beta):
    """Encode α|0⟩+β|1⟩ → α|000⟩+β|111⟩ with a native CNOT fan-out."""
    psi = np.zeros(8, dtype=complex); psi[0] = alpha; psi[4] = beta   # (α|0⟩+β|1⟩)⊗|00⟩
    psi = _cnot(psi, 0, 1, 3)
    psi = _cnot(psi, 0, 2, 3)
    return psi / np.linalg.norm(psi)


def encode_phaseflip(alpha, beta):
    """Phase-flip code = bit-flip code conjugated by H on all three qubits."""
    psi = encode_bitflip(alpha, beta)
    for q in range(3):
        psi = _had(psi, q, 3)
    return psi


def encode_shor(alpha, beta):
    """9-qubit Shor code: phase-flip code across three blocks, each bit-flip
    encoded.  α|0⟩+β|1⟩ → α|+++...⟩-type logical state.  Built from native
    CNOT + H only."""
    # block structure: qubits 0..8, block b = {3b,3b+1,3b+2}; block leaders 0,3,6
    psi = np.zeros(2 ** 9, dtype=complex)
    psi[0] = alpha; psi[1 << 8] = beta       # (α|0⟩+β|1⟩) on qubit0, rest |0⟩
    n = 9
    # outer phase-flip encode on block leaders 0,3,6
    psi = _cnot(psi, 0, 3, n)
    psi = _cnot(psi, 0, 6, n)
    for q in (0, 3, 6):
        psi = _had(psi, q, n)
    # inner bit-flip encode within each block
    for b in (0, 3, 6):
        psi = _cnot(psi, b, b + 1, n)
        psi = _cnot(psi, b, b + 2, n)
    return psi / np.linalg.norm(psi)


# ───────────────────────── stabilizer syndrome recovery ────────────────────
def _proj_pm(stab, n):
    """The ± eigenprojectors (P+,P−) of a Hermitian, involutory stabilizer."""
    Pp = 0.5 * (np.eye(2 ** n, dtype=complex) + stab)
    Pm = 0.5 * (np.eye(2 ** n, dtype=complex) - stab)
    return Pp, Pm


def recover_bitflip(rho):
    """Syndrome-measure Z₀Z₁, Z₁Z₂ and apply the X correction (density-matrix,
    exact).  Corrects any single bit-flip."""
    n = 3
    Z0Z1 = embed(Z, 0, n) @ embed(Z, 1, n)
    Z1Z2 = embed(Z, 1, n) @ embed(Z, 2, n)
    P0p, P0m = _proj_pm(Z0Z1, n)
    P1p, P1m = _proj_pm(Z1Z2, n)
    # syndrome → correction: (s01,s12): (+,+)→I, (−,+)→X0, (−,−)→X1, (+,−)→X2
    branches = [(P0p @ P1p, np.eye(2 ** n, dtype=complex)),
                (P0m @ P1p, embed(X, 0, n)),
                (P0m @ P1m, embed(X, 1, n)),
                (P0p @ P1m, embed(X, 2, n))]
    out = np.zeros_like(rho)
    for P, C in branches:
        out = out + C @ (P @ rho @ P.conj().T) @ C.conj().T
    return out


def recover_phaseflip(rho):
    """Phase-flip recovery = bit-flip recovery in the Hadamard basis."""
    n = 3
    Hall = embed(H1, 0, n) @ embed(H1, 1, n) @ embed(H1, 2, n)
    rho = Hall @ rho @ Hall.conj().T
    rho = recover_bitflip(rho)
    return Hall @ rho @ Hall.conj().T


def recover_shor(rho):
    """9-qubit Shor recovery: bit-flip correct each block, then phase-flip
    correct across blocks (density-matrix, exact)."""
    n = 9
    # --- inner: bit-flip syndrome per block ---
    for b in (0, 3, 6):
        Za = embed(Z, b, n) @ embed(Z, b + 1, n)
        Zb = embed(Z, b + 1, n) @ embed(Z, b + 2, n)
        Pap, Pam = _proj_pm(Za, n)
        Pbp, Pbm = _proj_pm(Zb, n)
        branches = [(Pap @ Pbp, np.eye(2 ** n, dtype=complex)),
                    (Pam @ Pbp, embed(X, b, n)),
                    (Pam @ Pbm, embed(X, b + 1, n)),
                    (Pap @ Pbm, embed(X, b + 2, n))]
        out = np.zeros_like(rho)
        for P, C in branches:
            out = out + C @ (P @ rho @ P.conj().T) @ C.conj().T
        rho = out
    # --- outer: phase-flip syndrome across blocks ---
    def Xblock(b):
        return embed(X, b, n) @ embed(X, b + 1, n) @ embed(X, b + 2, n)
    SA = Xblock(0) @ Xblock(3)          # X⊗X on blocks 0,1
    SB = Xblock(3) @ Xblock(6)          # X⊗X on blocks 1,2
    Pap, Pam = _proj_pm(SA, n)
    Pbp, Pbm = _proj_pm(SB, n)

    def Zblock(b):                      # a logical Z-correction on a block
        return embed(Z, b, n)
    branches = [(Pap @ Pbp, np.eye(2 ** n, dtype=complex)),
                (Pam @ Pbp, Zblock(0)),
                (Pam @ Pbm, Zblock(3)),
                (Pap @ Pbm, Zblock(6))]
    out = np.zeros_like(rho)
    for P, C in branches:
        out = out + C @ (P @ rho @ P.conj().T) @ C.conj().T
    return out


# ───────────────────────── analytic reference ──────────────────────────────
def bitflip_corrected_fidelity(p, a=1.0, b=0.0):
    """Exact logical fidelity of the 3-qubit code under per-qubit bit-flip p, for
    the encoded state a|0_L⟩+b|1_L⟩.

    0 or 1 physical flips (prob 1−3p²+2p³) are corrected perfectly → fidelity 1.
    2 or 3 flips (prob 3p²−2p³) MIScorrect to the logical-flipped state X_L|ψ⟩,
    which still overlaps the target by |⟨ψ|X_L|ψ⟩|²=(2ab)².  Hence
        F_corr = (1−3p²+2p³) + (3p²−2p³)(2ab)²,
    so the logical *infidelity* 1−F_corr = (3p²−2p³)(1−(2ab)²) = O(p²) — the
    quadratic error suppression that is the whole point of the code (vs the
    uncorrected O(p))."""
    P_ok = 1.0 - 3.0 * p ** 2 + 2.0 * p ** 3
    return P_ok + (1.0 - P_ok) * (2.0 * a * b) ** 2

def bitflip_uncorrected_fidelity(p, a=1.0, b=0.0):
    """Fidelity of the encoded state to itself under bit-flip noise with NO
    correction: only the no-error branch (and partial X_L overlaps) survive."""
    # ρ = Σ over 3-bit error patterns; ⟨ψ|E ρ ... ⟩.  Closed form:
    # F = (1−p)³ + p³(2ab)² + [3p(1−p)² + 3p²(1−p)]·0 ... only 0-flip and 3-flip
    # keep support on {|000⟩,|111⟩}; 1- and 2-flip land outside the code space.
    return (1 - p) ** 3 + p ** 3 * (2 * a * b) ** 2
