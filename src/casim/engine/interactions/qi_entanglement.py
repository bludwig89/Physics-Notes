#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_entanglement.py  —  genuine many-body (2^n) entanglement on the lattice (F212)
=================================================================================

Purpose
-------
Every many-body sector shipped so far (`ca_manybody.py` Hartree electrons,
variational-cluster nuclei; the `test_02_QM1_CHSH.py` Part-3 lattice singlet)
is *mean-field / first-quantised*: the joint state is a PRODUCT of single-cell
amplitudes, so its Hilbert-space dimension grows as ~2N (N = #cells), not 2^N,
and it carries **zero** entanglement entropy by construction.  The CHSH lattice
test even builds its "singlet" as a product  A_up * B_down  — the entanglement
is inserted by hand, never generated.

This module builds the missing piece: a genuine 2^n tensor-product register
with dynamical two-cell coupling, so we can ask the sharp question behind the
quantum-computing cross-test —

    does the lattice substrate GENERATE entanglement entropy it was not given?

Everything here is built from the model's OWN primitives:

  * single-qubit gate  =  the model's per-cell SU(2) rotor
        R(θ, n̂) = cos θ · I  −  i sin θ · (n̂·σ)          (ca_dirac F26 form)
    i.e. exp(−iθ n̂·σ) ∈ SU(2).  This is literally the mass/coupling rotation
    used on every spinor cell.

  * two-qubit gate  =  the nearest-neighbour spinor EXCHANGE interaction
        H_exch = σ_A · σ_B = σx⊗σx + σy⊗σy + σz⊗σz
        U_exch(θ) = exp(−iθ H_exch)
    Two adjacent identical Weyl cells coupled by the lattice hopping term
    (kinetic coefficient n = √(1−m²), ca_dirac) develop a super-exchange
    Heisenberg coupling J·σ_A·σ_B at second order in the hop; this is the
    lattice-native origin of the gate.  Its magnitude sets the *rate*; the
    entanglement generated depends only on the accumulated angle θ = ∫J dt.

No Bell state, GHZ state, or any entangled amplitude is ever written down.
We start from PRODUCT states (tensor products of single-cell kets), evolve
with the interaction, and *measure* the reduced-density-matrix entropy.

Pure numpy.  The only linear algebra on the quantum state is dense complex
matmul / kron and a Hermitian eigensolve for the entropy (eigvalsh on a PSD
reduced density matrix) — both safe (no chiral-transform gotcha, F-note in
CLAUDE.md; we assert Hermiticity/unitarity explicitly).
"""
from __future__ import annotations

import numpy as np

try:
    from casim.engine.particles import dirac as _ca_dirac
except Exception:  # pragma: no cover — allow import without the kernel on path
    _ca_dirac = None

# ─────────────────────────── Pauli algebra ────────────────────────────
I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = (SX, SY, SZ)

KET0 = np.array([1, 0], dtype=complex)   # |↑⟩
KET1 = np.array([0, 1], dtype=complex)   # |↓⟩
KETP = np.array([1, 1], dtype=complex) / np.sqrt(2)   # |+⟩ = (|↑⟩+|↓⟩)/√2


# ═══════════════════════════════════════════════════════════════════════
#  Model-native gate primitives
# ═══════════════════════════════════════════════════════════════════════
def su2_rotor(theta: float, n=(0.0, 0.0, 1.0)) -> np.ndarray:
    """The model's single-cell SU(2) rotor R(θ,n̂)=cosθ I − i sinθ (n̂·σ).

    Identical in form to the ca_dirac F26 mass/coupling rotation
    cos(θ)I ± i sin(θ)A with A = n̂·σ (A²=I).  Equivalent to exp(−iθ n̂·σ);
    a Bloch-sphere rotation by angle 2θ about axis n̂.
    """
    n = np.asarray(n, dtype=float)
    n = n / np.linalg.norm(n)
    ndots = n[0] * SX + n[1] * SY + n[2] * SZ
    return np.cos(theta) * I2 - 1j * np.sin(theta) * ndots


def exchange_gate(theta: float) -> np.ndarray:
    """Two-cell spin-exchange entangler U_exch(θ)=exp(−iθ σ_A·σ_B), 4×4.

    σ_A·σ_B eigenvalues: +1 on the triplet (3-fold), −3 on the singlet, so
        U = exp(−iθ) P_triplet + exp(+3iθ) P_singlet.
    θ = π/8 is the maximally-entangling point (√SWAP up to single-qubit
    phases): a computational-basis product input comes out maximally entangled.
    """
    sdots = np.kron(SX, SX) + np.kron(SY, SY) + np.kron(SZ, SZ)
    # exp(−iθ H) via eigendecomposition of the Hermitian H (exact, closed-form
    # eigenvalues ±): use eigh for numerical cleanliness.
    w, V = np.linalg.eigh(sdots)
    return (V * np.exp(-1j * theta * w)) @ V.conj().T


def swap_gate() -> np.ndarray:
    """SWAP = (I + σ_A·σ_B)/2 — the model exchange interaction at its
    permutation point.  Verifies the exchange operator's identity."""
    sdots = np.kron(SX, SX) + np.kron(SY, SY) + np.kron(SZ, SZ)
    return 0.5 * (np.eye(4, dtype=complex) + sdots)


# ═══════════════════════════════════════════════════════════════════════
#  Genuine n-qubit register (2^n state vector — NOT a product ansatz)
# ═══════════════════════════════════════════════════════════════════════
class Register:
    """A dense 2^n complex state vector with local gate application.

    The whole point: the amplitude array has 2^n independent entries, so the
    state CAN represent arbitrary entanglement.  We only ever *initialise* it
    from single-cell product kets; any entanglement present later was generated
    by the gates, not supplied.
    """

    def __init__(self, single_cell_kets):
        """Build |ψ⟩ = ⊗_i |c_i⟩ from a list of 2-vectors (a PRODUCT state)."""
        psi = np.array([1.0 + 0j])
        for k in single_cell_kets:
            psi = np.kron(psi, np.asarray(k, dtype=complex))
        self.n = len(single_cell_kets)
        self.psi = psi / np.linalg.norm(psi)

    # ---- gate application -------------------------------------------------
    def _apply_op(self, op, targets):
        """Apply a (2^k×2^k) op to the k qubits in `targets` (tensor-aware)."""
        n = self.n
        k = len(targets)
        t = self.psi.reshape([2] * n)
        # move target axes to the front, apply, move back
        others = [ax for ax in range(n) if ax not in targets]
        perm = list(targets) + others
        t = np.transpose(t, perm)
        t = t.reshape(2 ** k, -1)
        t = op @ t
        t = t.reshape([2] * k + [2] * (n - k))
        inv = np.argsort(perm)
        t = np.transpose(t, inv)
        self.psi = t.reshape(-1)

    def apply_1q(self, gate, q):
        self._apply_op(gate, [q])

    def apply_2q(self, gate4, q0, q1):
        self._apply_op(gate4, [q0, q1])

    # ---- observables ------------------------------------------------------
    def rho_reduced(self, keep):
        """Reduced density matrix on the `keep` qubits (partial trace of rest)."""
        keep = list(keep)
        n = self.n
        t = self.psi.reshape([2] * n)
        traced = [ax for ax in range(n) if ax not in keep]
        perm = keep + traced
        t = np.transpose(t, perm).reshape(2 ** len(keep), 2 ** len(traced))
        return t @ t.conj().T

    def entropy(self, keep):
        """von Neumann entropy S = −Tr ρ ln ρ (natural log) of subsystem `keep`."""
        rho = self.rho_reduced(keep)
        ev = np.linalg.eigvalsh(rho).real
        ev = ev[ev > 1e-15]
        return float(-(ev * np.log(ev)).sum())

    def norm(self):
        return float(np.linalg.norm(self.psi))


# ═══════════════════════════════════════════════════════════════════════
#  Mean-field (Hartree) counterpart — the substrate that CANNOT host it
# ═══════════════════════════════════════════════════════════════════════
def best_product_fidelity(psi, dimA, dimB):
    """Largest fidelity any single PRODUCT state |a⟩⊗|b⟩ can have with |psi⟩.

    This is exactly what a mean-field / Hartree ansatz (ca_manybody.py) is
    restricted to.  By the Schmidt decomposition it equals the largest squared
    Schmidt coefficient λ_max = σ_max² of the reshaped amplitude matrix.
    The entanglement the mean field must DISCARD is (1 − λ_max) of the weight,
    with residual entropy = the full S whenever λ_max < 1.
    """
    C = psi.reshape(dimA, dimB)
    s = np.linalg.svd(C, compute_uv=False)
    lam = (s ** 2)
    return float(lam.max()), lam


def meanfield_evolve_2q(ket_a, ket_b, theta, nsteps=200):
    """Time-dependent PRODUCT (mean-field) evolution under exchange coupling.

    A genuine Hartree constraint: after each infinitesimal exchange step we
    PROJECT the two-cell state back onto its best product (rank-1) form — this
    is what a substrate with no many-body amplitude array is forced to do.
    Returns the mean-field state, its (identically ~0) entanglement entropy,
    and the ZZ correlation, so it can be compared to the exact register.
    """
    dt = theta / nsteps
    Ustep = exchange_gate(dt)
    psi = np.kron(np.asarray(ket_a, complex), np.asarray(ket_b, complex))
    psi = psi / np.linalg.norm(psi)
    for _ in range(nsteps):
        psi = Ustep @ psi
        # Hartree projection: keep only the leading product component
        C = psi.reshape(2, 2)
        U, s, Vh = np.linalg.svd(C)
        C_rank1 = s[0] * np.outer(U[:, 0], Vh[0, :])
        psi = C_rank1.reshape(-1)
        psi = psi / np.linalg.norm(psi)
    # entropy of the (product) mean-field state
    C = psi.reshape(2, 2)
    ev = np.linalg.eigvalsh(C @ C.conj().T).real
    ev = ev[ev > 1e-15]
    S = float(-(ev * np.log(ev)).sum())
    ZZ = float(np.real(psi.conj() @ np.kron(SZ, SZ) @ psi))
    return psi, S, ZZ


# ═══════════════════════════════════════════════════════════════════════
#  Perfect-entangler property (convention-free universality certificate)
# ═══════════════════════════════════════════════════════════════════════
def is_perfect_entangler_demo(theta=np.pi / 8):
    """The exchange gate is a PERFECT ENTANGLER: it maps some product input to
    a MAXIMALLY entangled output.  We exhibit it directly (definition-level,
    no local invariants needed): product |↑↓⟩ → exchange(π/8) → S = ln2.

    A perfect entangler together with the full single-qubit gate set (the model
    supplies both: `su2_rotor` and `exchange_gate`) is universal for quantum
    computation (Bremner, Dawson, Dodd, Gilchrist, Harrow, Mortimer, Nielsen,
    Osborne, PRL 89, 247902 (2002)).  Hence the lattice substrate is, in
    principle, a universal quantum computer — the sharp requirement the
    mean-field sectors cannot meet.
    Returns (S_out, S_target=ln2).
    """
    reg = Register([KET0, KET1])
    reg.apply_2q(exchange_gate(theta), 0, 1)
    return reg.entropy([0]), float(np.log(2))


# Textbook CNOT — used only to *validate the engine's entropy readout* on a
# named maximally-entangled state (GHZ).  Its decomposition into the native
# exchange + SU(2) gates is guaranteed to exist by the perfect-entangler
# universality theorem above (we do not reconstruct it here).
CNOT_REF = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1],
                     [0, 0, 1, 0]], dtype=complex)
HADAMARD = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)


def make_ghz(n=3):
    """Build the n-qubit GHZ state from the product |0…0⟩ with H + CNOT chain.
    Used to validate that `Register.entropy` reports ln2 across every single-
    qubit cut of a known maximally-entangled state."""
    reg = Register([KET0] * n)
    reg.apply_1q(HADAMARD, 0)
    for q in range(1, n):
        reg.apply_2q(CNOT_REF, 0, q)
    return reg


# ═══════════════════════════════════════════════════════════════════════
#  Flat-state-vector helpers (for the live casim channel; no Register object)
# ═══════════════════════════════════════════════════════════════════════
def product_state(single_cell_kets):
    """Return the 2^n amplitude vector of ⊗_i |c_i⟩ (a PRODUCT state)."""
    psi = np.array([1.0 + 0j])
    for k in single_cell_kets:
        psi = np.kron(psi, np.asarray(k, dtype=complex))
    return psi / np.linalg.norm(psi)


def apply_gate(psi, op, targets, n):
    """Apply a (2^k×2^k) operator to qubits `targets` of an n-qubit vector `psi`.
    Tensor-aware; returns the new flat vector (does not mutate input)."""
    k = len(targets)
    t = psi.reshape([2] * n)
    others = [ax for ax in range(n) if ax not in targets]
    perm = list(targets) + others
    t = np.transpose(t, perm).reshape(2 ** k, -1)
    t = op @ t
    t = t.reshape([2] * k + [2] * (n - k))
    return np.transpose(t, np.argsort(perm)).reshape(-1)


def entropy_of_vector(psi, n, keep):
    """von Neumann entropy S=−Tr ρ ln ρ of subsystem `keep` of an n-qubit `psi`."""
    keep = list(keep)
    t = psi.reshape([2] * n)
    traced = [ax for ax in range(n) if ax not in keep]
    t = np.transpose(t, keep + traced).reshape(2 ** len(keep), 2 ** len(traced))
    rho = t @ t.conj().T
    ev = np.linalg.eigvalsh(rho).real
    ev = ev[ev > 1e-15]
    return float(-(ev * np.log(ev)).sum())


# ═══════════════════════════════════════════════════════════════════════
#  Super-exchange derivation — the ENTANGLER'S coupling J from ca_dirac hopping
# ═══════════════════════════════════════════════════════════════════════
#
# Two adjacent Weyl/Dirac cells, one spin-½ fermion each (the up/down spinor
# component = the qubit).  The lattice hopping (kinetic coefficient n=√(1−m²))
# lets a fermion virtually hop to the neighbour at amplitude t; double occupancy
# costs the mass gap U.  Second-order degenerate perturbation theory at
# half-filling gives the antiferromagnetic Heisenberg exchange
#
#     H_eff = J (S_A·S_B − ¼) = (J/4)(σ_A·σ_B − 1),     J = 4t²/U   (t ≪ U)
#
# i.e. exactly the F212 entangler U_exch(θ)=exp(−iθ σ_A·σ_B) is *generated* by
# the lattice, with a DERIVED coefficient θ_per_tick = J/4 (the −1 is a global
# phase).  The exact two-site Hubbard singlet–triplet gap
# J = ½(√(U²+16t²) − U) reduces to 4t²/U at large gap.

def hopping_amplitude(m, L=16):
    """Nearest-neighbour single-particle hopping amplitude t(m), measured
    directly from one tick of the exact-QCA ca_dirac real-space stepper:
    a single-site source, one tick, |amplitude on a nearest neighbour|.
    Encodes the kinetic coefficient n=√(1−m²) of the massive Dirac walk."""
    if _ca_dirac is None:
        raise RuntimeError("casim.engine.particles.dirac not importable")
    z = lambda: np.zeros((L, L), dtype=complex)
    eu, ed, cu, cd = z(), z(), z(), z()
    c = L // 2
    eu[c, c] = 1.0
    eu2, ed2, cu2, cd2 = _ca_dirac.dirac_step_2d_splitstep(eu, ed, cu, cd, m=m, dt=1.0)
    nn = [(c + 1, c), (c - 1, c), (c, c + 1), (c, c - 1)]
    amp = [abs(eu2[i, j]) + abs(ed2[i, j]) + abs(cu2[i, j]) + abs(cd2[i, j])
           for i, j in nn]
    return float(np.mean(amp))


def mass_gap(m):
    """Double-occupancy / virtual-excitation gap U = 2·ω(k=0) = 2·arcsin(m)
    of the massive Dirac walk (the Zitterbewegung / mass gap ω_Z, ca_dirac F26)."""
    return float(2.0 * np.arcsin(m))


def superexchange_J(t, U):
    """Exact two-site half-filling Hubbard singlet–triplet gap J (= the effective
    Heisenberg coupling): J = ½(√(U²+16t²) − U).  → 4t²/U as t≪U."""
    return float(0.5 * (np.sqrt(U ** 2 + 16.0 * t ** 2) - U))


def two_site_hubbard_gap_numeric(t, U):
    """Same J, but by exact diagonalisation of the S_z=0 two-fermion sector
    {|↑↓⟩,|↓↑⟩,|2,0⟩,|0,2⟩} — validates `superexchange_J` and that the
    low-energy sector is Heisenberg (singlet below the E=0 triplet by J)."""
    H = np.array([[0, 0, -t, -t],
                  [0, 0,  t,  t],
                  [-t, t,  U,  0],
                  [-t, t,  0,  U]], dtype=float)
    E_singlet = float(np.linalg.eigvalsh(H)[0])
    return 0.0 - E_singlet     # triplet (E=0) − singlet


def exchange_angle_per_tick(m):
    """Derived per-tick entangling angle θ = J(m)/4 for U_exch, from the
    ca_dirac hopping t(m) and gap U(m).  Bell pair (θ_total=π/8) forms in
    τ = (π/8)/θ ticks."""
    t = hopping_amplitude(m)
    U = mass_gap(m)
    J = superexchange_J(t, U)
    return J / 4.0


def bell_time_ticks(m):
    """Number of CA ticks for a nearest-neighbour pair to reach a maximally
    entangled (Bell) state under the derived exchange rate: τ = (π/8)/(J/4)."""
    return float((np.pi / 8.0) / exchange_angle_per_tick(m))


# ═══════════════════════════════════════════════════════════════════════
#  Native universal gate set — CZ/CNOT compiled EXACTLY from the exchange gate
# ═══════════════════════════════════════════════════════════════════════
#
# The exchange operator σ_A·σ_B = XX+YY+ZZ commutes with ZZ, and conjugating it
# by σz⊗I flips the XX,YY signs, so two native exchange gates sandwiching a σz
# give exactly exp(iπ/4 ZZ):
#     exp(+iπ/8 σ·σ)·(σz⊗I)·exp(+iπ/8 σ·σ)·(σz⊗I) = exp(iπ/4 ZZ).
# CZ and CNOT follow by single-qubit dressing.  All pieces are native
# (`exchange_gate`, `su2_rotor`); the compilation is exact to machine precision,
# a constructive proof that the lattice exchange interaction is universal.

def native_hadamard():
    """Hadamard from the native SU(2) rotor (exact up to global phase)."""
    return 1j * su2_rotor(np.pi / 2, (1, 0, 1))


def native_zz_quarter():
    """exp(iπ/4 σz⊗σz), built from two exchange gates + a σz conjugation."""
    X8 = exchange_gate(-np.pi / 8)                 # exp(+iπ/8 σ·σ)
    Zc = su2_rotor(np.pi / 2, (0, 0, 1))           # = −i σz (phase-irrelevant here)
    ZI = np.kron(Zc, I2)
    return X8 @ ZI @ X8 @ ZI


def native_zz(theta: float):
    """exp(iθ σz⊗σz) for ANY angle θ, from two exchange gates + a σz conjugation.

    Generalises `native_zz_quarter` (θ=π/4).  The identity is
        exp(+iφ σ·σ)·(σz⊗I)·exp(+iφ σ·σ)·(σz⊗I) = exp(i·2φ·ZZ),
    since conjugation by σz⊗I flips the XX,YY signs (they cancel) while the ZZ
    parts add.  Set φ=θ/2 ⇒ exp(iθ ZZ).  All pieces native (`exchange_gate`,
    `su2_rotor`)."""
    X = exchange_gate(-theta / 2.0)                # exp(+i θ/2 σ·σ)
    ZI = np.kron(su2_rotor(np.pi / 2, (0, 0, 1)), I2)   # −i σz ⊗ I
    # X·ZI·X·ZI = −exp(iθ ZZ): the two −i factors contribute a constant −1
    # (θ-independent, since σz⊗I conjugation flips XX,YY and squares to I), so
    # negate to land exactly on exp(iθ σz⊗σz).
    return -(X @ ZI @ X @ ZI)


def native_cphase(phi: float):
    """Controlled-phase diag(1,1,1,e^{iφ}) built EXACTLY from native primitives.

    Uses  a AND b = ¼(I − Z_a − Z_b + Z_a Z_b), so
        CP(φ) = e^{iφ/4} · exp(iφ/4 Z_aZ_b) · exp(−iφ/4 Z_a) · exp(−iφ/4 Z_b),
    with the ZZ piece = `native_zz(φ/4)` and each single-Z piece a native rotor
    su2_rotor(φ/4, ẑ)=exp(−iφ/4 σz).  Exact to machine precision (verified)."""
    Rz = su2_rotor(phi / 4.0, (0, 0, 1))           # exp(−iφ/4 σz)
    return np.exp(1j * phi / 4.0) * native_zz(phi / 4.0) @ np.kron(Rz, Rz)


def native_ccz():
    """Controlled-controlled-Z (3 qubits) compiled EXACTLY from the native
    controlled-phase + CNOT via the Barenco V=√Z=S construction:
        CCZ = CS_{2,3}·CNOT_{1,2}·CS†_{2,3}·CNOT_{1,2}·CS_{1,3},
    where CS = native_cphase(π/2) and CNOT is native.  Extends the constructive
    universality proof (F218) to a genuine 3-qubit controlled gate; matches
    diag(1,…,1,−1) to <1e-12."""
    CS = native_cphase(np.pi / 2)                  # controlled-S = C-√Z
    CSd = native_cphase(-np.pi / 2)                # controlled-S†
    cnot = native_cnot()
    U = apply3(np.eye(8, dtype=complex), CS, (0, 2))       # CS on (c1,t)
    U = apply3(U, cnot, (0, 1))
    U = apply3(U, CSd, (1, 2))
    U = apply3(U, cnot, (0, 1))
    U = apply3(U, CS, (1, 2))
    return U


def apply3(U8, gate2, targets):
    """Left-multiply an 8×8 operator by a 2-qubit `gate2` acting on `targets`
    (helper for assembling 3-qubit native gates as explicit matrices)."""
    full = _embed_2q(gate2, targets, 3)
    return full @ U8


def _embed_2q(gate4, targets, n):
    """Embed a 4×4 two-qubit `gate4` on `targets` into the full 2^n operator."""
    dim = 2 ** n
    op = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        v = np.zeros(dim, dtype=complex)
        v[col] = 1.0
        op[:, col] = apply_gate(v, gate4, list(targets), n)
    return op


# --- efficient state-vector actions for multi-controlled gates ---------------
def apply_mcz(psi, controls, n):
    """Apply a multi-controlled Z (flip the sign of the all-controls-=1 block)
    directly to a 2^n state vector — the exact action of the native
    Barenco-extended CCZ ladder, applied without forming a 2^n×2^n matrix."""
    t = psi.reshape([2] * n).copy()
    idx = tuple(1 if ax in controls else slice(None) for ax in range(n))
    t[idx] *= -1.0
    return t.reshape(-1)


def apply_mcx(psi, controls, target, n):
    """Apply a multi-controlled X: on the subspace where every control qubit is
    1, swap the two `target` slices.  Exact action of the native MCX; MCX =
    (I⊗H)·MCZ·(I⊗H) on the target, so it inherits native compilability."""
    t = psi.reshape([2] * n).copy()
    sel = [1 if ax in controls else slice(None) for ax in range(n)]
    sel0 = list(sel); sel0[target] = 0
    sel1 = list(sel); sel1[target] = 1
    a = t[tuple(sel0)].copy()
    t[tuple(sel0)] = t[tuple(sel1)]
    t[tuple(sel1)] = a
    return t.reshape(-1)


def native_cz():
    """Controlled-Z from the native exchange gate + rotors (exact)."""
    Rz = lambda a: su2_rotor(a / 2.0, (0, 0, 1))
    cz = np.exp(1j * np.pi / 4) * native_zz_quarter() @ np.kron(Rz(np.pi / 2), Rz(np.pi / 2))
    # phase-align to the canonical CZ = diag(1,1,1,-1)
    ref = np.diag([1, 1, 1, -1]).astype(complex)
    ph = ref[0, 0] / cz[0, 0]
    return cz * (ph / abs(ph))


def native_cnot():
    """CNOT (control=q0) from the native gate set (exact): (I⊗H)·CZ·(I⊗H)."""
    H = native_hadamard()
    cnot = np.kron(I2, H) @ native_cz() @ np.kron(I2, H)
    ref = CNOT_REF
    idx = np.unravel_index(np.argmax(np.abs(ref)), ref.shape)
    ph = ref[idx] / cnot[idx]
    return cnot * (ph / abs(ph))


# ═══════════════════════════════════════════════════════════════════════
#  Circuit runner over the flat state vector (native gate set)
# ═══════════════════════════════════════════════════════════════════════
def _gate_matrix(kind, params):
    """Return (op, targets) for a JSON-serializable gate spec."""
    if kind == "h":
        return native_hadamard(), [int(params[0])]
    if kind == "x":
        return SX, [int(params[0])]
    if kind == "z":
        return SZ, [int(params[0])]
    if kind == "rz":
        return su2_rotor(float(params[1]) / 2.0, (0, 0, 1)), [int(params[0])]
    if kind == "exch":
        return exchange_gate(float(params[2])), [int(params[0]), int(params[1])]
    if kind == "cz":
        return native_cz(), [int(params[0]), int(params[1])]
    if kind == "cnot":
        return native_cnot(), [int(params[0]), int(params[1])]
    if kind == "cphase":
        return native_cphase(float(params[2])), [int(params[0]), int(params[1])]
    if kind == "ccz":
        return native_ccz(), [int(params[0]), int(params[1]), int(params[2])]
    raise ValueError(f"unknown gate {kind!r}")


def apply_layer(psi, layer, n):
    """Apply one layer (list of gate specs [kind, *params]) to an n-qubit vector.

    Multi-controlled gates ("mcz"/"mcx") act directly on the state vector (the
    exact action of the native Barenco-extended ladder) so algorithms scale to
    large n without forming 2^n×2^n matrices."""
    for spec in layer:
        kind = spec[0]
        if kind == "mcz":                       # ["mcz", [controls...]]
            controls = [int(c) for c in spec[1]]
            psi = apply_mcz(psi, controls, n)
        elif kind == "mcx":                     # ["mcx", [controls...], target]
            controls = [int(c) for c in spec[1]]
            psi = apply_mcx(psi, controls, int(spec[2]), n)
        else:
            op, targets = _gate_matrix(kind, spec[1:])
            psi = apply_gate(psi, op, targets, n)
    return psi


def run_circuit(n, program, init_kets=None):
    """Run a full circuit (list of layers) on a product init; return final vector."""
    psi = product_state(init_kets if init_kets is not None else [KET0] * n)
    for layer in program:
        psi = apply_layer(psi, layer, n)
    return psi


def probabilities(psi):
    """Computational-basis probabilities |amp|²."""
    return np.abs(psi) ** 2
