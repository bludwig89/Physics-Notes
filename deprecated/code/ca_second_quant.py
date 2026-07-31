# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_second_quant.py
# migrated   : 2026-07-30 - 16:06
# target     : src/casim/engine/particles/second_quant.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_second_quant.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_second_quant.py  —  field-native second quantization on a lattice chain (F217)
=================================================================================

F214 derived the entangler's coupling J from an *effective* two-site Hubbard
model (a spin model at half filling).  This module removes the "effective":
it builds a genuine fermionic Fock space with Jordan–Wigner creation/annihilation
operators on a chain of lattice cells, and lets the entanglement — and the
super-exchange J itself — EMERGE from the real fermion hopping + Pauli exclusion.

Spin-orbitals: for `n_sites` cells with spin-½ fermions there are
`2·n_sites` spin-orbitals, ordered (site0↑, site0↓, site1↑, site1↓, …).
The Fock space is the full 2^(2·n_sites) occupation-number space; fermionic
antisymmetry is carried exactly by the Jordan–Wigner string signs.

Hubbard Hamiltonian (the minimal field-native model):

    H = −t Σ_{⟨ij⟩,σ} (c†_{iσ} c_{jσ} + h.c.)  +  U Σ_i n_{i↑} n_{i↓}

with
    t = the ca_dirac nearest-neighbour hopping amplitude (measured, F214),
    U = the mass gap 2·arcsin(m) (the double-occupancy cost, F214).

Key results this module establishes (see test_F217):
  * {c_i, c_j†} = δ_ij, {c_i,c_j}=0 — genuine fermions (machine precision).
  * Pauli exclusion: no amplitude ever has two same-spin fermions on one site.
  * Half-filling two-site singlet–triplet gap = J = ½(√(U²+16t²)−U) — the F214
    super-exchange, now emergent from second quantization, not imposed.
  * Starting from the Fock PRODUCT |↑ on site0, ↓ on site1⟩ (a single Slater
    determinant, spin-unentangled), the real hopping GENERATES two-site spin
    entanglement, and at large U the dynamics matches the F214 exchange gate.

Pure numpy; all operators are real/integer sparse-dense matrices (no chiral
transform, so the numpy caveat in CLAUDE.md does not apply); we assert the
fermion algebra explicitly.
"""
from __future__ import annotations

import numpy as np

try:
    import ca_entanglement as _E
except Exception:  # pragma: no cover
    _E = None


# ─────────────────────── Jordan–Wigner fermion operators ───────────────────
def jw_annihilation(n_orb):
    """Return the list [c_0, …, c_{n_orb−1}] of annihilation operators on the
    2^n_orb-dim Fock space, with Jordan–Wigner string signs so that
    {c_i, c_j†} = δ_ij and {c_i, c_j} = 0 exactly.

    Convention: orbital 0 is the most-significant bit; the JW string runs over
    orbitals with index < i (occupied-count parity gives the sign).
    """
    sz = np.array([[1.0, 0.0], [0.0, -1.0]])      # parity operator (−1)^n on one mode
    lower = np.array([[0.0, 1.0], [0.0, 0.0]])    # |0⟩⟨1| : annihilate one mode
    I2 = np.eye(2)
    ops = []
    for i in range(n_orb):
        mats = []
        for j in range(n_orb):
            if j < i:
                mats.append(sz)      # JW string: parity of earlier orbitals
            elif j == i:
                mats.append(lower)
            else:
                mats.append(I2)
        op = mats[0]
        for m in mats[1:]:
            op = np.kron(op, m)
        ops.append(op)
    return ops


class FermionChain:
    """A genuine second-quantized spin-½ fermion chain (Hubbard model).

    orbital index = 2*site + (0 for ↑, 1 for ↓).
    """

    def __init__(self, n_sites, t, U):
        self.n_sites = int(n_sites)
        self.n_orb = 2 * self.n_sites
        self.t = float(t)
        self.U = float(U)
        self.c = jw_annihilation(self.n_orb)
        self.cd = [ci.conj().T for ci in self.c]
        self.n = [self.cd[i] @ self.c[i] for i in range(self.n_orb)]
        self.H = self._build_H()

    # orbital helpers
    def orb(self, site, spin):   # spin: 0=↑, 1=↓
        return 2 * site + spin

    def _build_H(self):
        dim = 2 ** self.n_orb
        H = np.zeros((dim, dim))
        # hopping between adjacent sites, spin-conserving
        for s in range(self.n_sites - 1):
            for spin in (0, 1):
                a = self.orb(s, spin)
                b = self.orb(s + 1, spin)
                hop = self.cd[a] @ self.c[b] + self.cd[b] @ self.c[a]
                H = H - self.t * hop
        # on-site Hubbard repulsion
        for s in range(self.n_sites):
            up = self.orb(s, 0)
            dn = self.orb(s, 1)
            H = H + self.U * (self.n[up] @ self.n[dn])
        return H

    # --- Fock states -------------------------------------------------------
    def fock_state(self, occupied_orbitals):
        """Return the occupation-number basis vector with the given orbitals
        occupied (built by applying c† in ascending order to the vacuum, so the
        state is a proper antisymmetric Slater determinant with fixed sign)."""
        dim = 2 ** self.n_orb
        vac = np.zeros(dim); vac[-1 if False else 0] = 0.0
        # vacuum = |00…0⟩ is index 0 in the big-endian kron basis
        vac[0] = 1.0
        psi = vac
        for orb in sorted(occupied_orbitals):
            psi = self.cd[orb] @ psi
        nrm = np.linalg.norm(psi)
        return psi / nrm if nrm > 0 else psi

    def neel_two_site(self):
        """|↑ on site0, ↓ on site1⟩ — a single Slater determinant, spin-product."""
        return self.fock_state([self.orb(0, 0), self.orb(1, 1)])

    # --- dynamics ----------------------------------------------------------
    def evolve(self, psi, time):
        """Exact unitary evolution e^{−iHt} ψ (Hermitian H → eigen-exponential)."""
        w, V = np.linalg.eigh(self.H)
        phase = np.exp(-1j * w * time)
        return V @ (phase * (V.conj().T @ psi.astype(complex)))

    # --- observables -------------------------------------------------------
    def double_occupancy(self, psi, site):
        up, dn = self.orb(site, 0), self.orb(site, 1)
        D = self.n[up] @ self.n[dn]
        return float(np.real(np.vdot(psi, D @ psi)))

    def spin_ops(self, site):
        """Sx, Sy, Sz for the fermion spin on `site` (½ σ in the ↑/↓ orbitals)."""
        up, dn = self.orb(site, 0), self.orb(site, 1)
        Sp = self.cd[up] @ self.c[dn]           # S⁺ = c†_↑ c_↓
        Sm = self.cd[dn] @ self.c[up]           # S⁻
        Sx = 0.5 * (Sp + Sm)
        Sy = -0.5j * (Sp - Sm)
        Sz = 0.5 * (self.n[up] - self.n[dn])
        return Sx, Sy, Sz

    def spin_correlation(self, psi, s0, s1):
        """⟨S_{s0}·S_{s1}⟩ (−3/4 for a spin singlet, +1/4 for a triplet)."""
        A = self.spin_ops(s0)
        B = self.spin_ops(s1)
        val = sum(np.vdot(psi, (a @ b) @ psi) for a, b in zip(A, B))
        return float(np.real(val))

    def singly_occupied_projector(self):
        """Projector onto the half-filling, one-fermion-per-site subspace."""
        dim = 2 ** self.n_orb
        P = np.eye(dim)
        for s in range(self.n_sites):
            ns = self.n[self.orb(s, 0)] + self.n[self.orb(s, 1)]
            # keep states with exactly one fermion on this site: project ns→1
            # build projector onto ns==1 eigenspace
            w, V = np.linalg.eigh(ns)
            keep = np.abs(w - 1.0) < 1e-9
            Ps = (V[:, keep]) @ (V[:, keep].conj().T)
            P = P @ Ps
        return P

    # --- field-native gate execution (F220) -------------------------------
    #
    # A logical qubit is the SPIN of a singly-occupied site.  In the one-fermion-
    # per-site sector the fermionic spin operators S_s act as ½σ, so the genuine
    # second-quantized operators below execute quantum gates directly on the Fock
    # space — no abstract register.  Single-qubit gates are EXACT (they conserve
    # the per-site occupation); the two-qubit entangler is the REAL Hubbard
    # time-evolution whose emergent super-exchange (F214/F217) becomes the exact
    # exchange gate in the large-U limit (leakage into doublons → 0).

    def fermionic_rotor(self, site, theta, axis=(0.0, 0.0, 1.0)):
        """Single-qubit SU(2) gate on `site`'s spin, as a genuine fermionic
        operator U = exp(−i·2θ n̂·S_site).  Matches the abstract
        `ca_entanglement.su2_rotor(θ, n̂)=exp(−iθ n̂·σ)` exactly on the qubit
        subspace (S=½σ there), and preserves the singly-occupied sector."""
        axis = np.asarray(axis, float)
        axis = axis / np.linalg.norm(axis)
        Sx, Sy, Sz = self.spin_ops(site)
        G = 2.0 * theta * (axis[0] * Sx + axis[1] * Sy + axis[2] * Sz)
        w, V = np.linalg.eigh(G)
        return (V * np.exp(-1j * w)) @ V.conj().T

    def superexchange_J(self):
        """Emergent super-exchange coupling J=½(√(U²+16t²)−U) of this chain."""
        return 0.5 * (np.sqrt(self.U ** 2 + 16.0 * self.t ** 2) - self.U)

    def exchange_time_for_angle(self, theta):
        """Hubbard evolution time t so the emergent spin exchange accumulates
        angle θ: H_eff=(J/4)σ_A·σ_B ⇒ exp(−iH_eff t)=exp(−iθ σ·σ) at t=4θ/J."""
        return 4.0 * theta / self.superexchange_J()

    def exchange_operator(self, theta):
        """Matrix form of the genuine Hubbard propagator e^{−iH t} for the time
        that accumulates spin-exchange angle θ (t=4θ/J).  This is the field-
        native two-qubit gate as an operator on the full Fock space."""
        w, V = np.linalg.eigh(self.H)
        tt = self.exchange_time_for_angle(theta)
        return (V * np.exp(-1j * w * tt)) @ V.conj().T

    def fermionic_exchange(self, psi, theta):
        """Two-qubit entangler executed by the GENUINE Hubbard dynamics: evolve
        e^{−iH t} for the time that accumulates spin-exchange angle θ.  In the
        large-U limit this is the exact exchange gate on the site spins; at
        finite U it also excites virtual doublons (quantified leakage)."""
        return self.evolve(psi, self.exchange_time_for_angle(theta))

    def spin_register(self, psi):
        """Project ψ onto the one-fermion-per-site sector and return the
        2^{n_sites} spin amplitude vector (site spin ↑=0, ↓=1, big-endian) plus
        the weight (probability) remaining in that sector.  This is the isometry
        that maps the Fock state to the abstract n-qubit register."""
        n = self.n_sites
        dim = 2 ** n
        amps = np.zeros(dim, dtype=complex)
        for idx in range(dim):
            orbs = [self.orb(s, (idx >> (n - 1 - s)) & 1) for s in range(n)]
            bra = self.fock_state(orbs)
            amps[idx] = np.vdot(bra, psi)
        w = float(np.real(np.vdot(amps, amps)))
        nrm = np.sqrt(w)
        if nrm > 1e-14:
            amps = amps / nrm
        return amps, w

    # --- field-native named gates + circuit runner (F220) -----------------
    def fn_hadamard(self, s):
        """Field-native Hadamard on site `s` (exact fermionic single-qubit gate;
        H = i·su2_rotor(π/2,(1,0,1)) in operator form)."""
        return 1j * self.fermionic_rotor(s, np.pi / 2, (1, 0, 1))

    def fn_x(self, s):
        """Field-native X (bit flip) on site `s` (exact)."""
        return 1j * self.fermionic_rotor(s, np.pi / 2, (1, 0, 0))

    def fn_z(self, s):
        """Field-native Z on site `s` (exact)."""
        return 1j * self.fermionic_rotor(s, np.pi / 2, (0, 0, 1))

    def fn_cnot(self, control, target):
        """Field-native CNOT: exchange-derived CZ dressed by field-native H on the
        target.  The ZZ core is the GENUINE Hubbard exchange (exact only as
        U/t→∞), so this gate is leakage-limited at finite U; single-qubit
        dressings are exact."""
        Xe = self.exchange_operator(-np.pi / 8)
        szc = self.fermionic_rotor(control, np.pi / 2, (0, 0, 1))
        zzq = -(Xe @ szc @ Xe @ szc)               # exp(iπ/4 Z_cZ_t), leakage-limited
        Rzc = self.fermionic_rotor(control, np.pi / 4, (0, 0, 1))
        Rzt = self.fermionic_rotor(target, np.pi / 4, (0, 0, 1))
        cz = np.exp(1j * np.pi / 4) * zzq @ Rzc @ Rzt
        H = self.fn_hadamard(target)
        return H @ cz @ H

    def apply_program_fock(self, psi, program):
        """Run a JSON gate program (same format as ca_entanglement) DIRECTLY on
        the fermionic Fock state.  Single-qubit gates (h/x/z/rz) are exact
        fermionic operators; 'cnot'/'cz'/'exch' use the genuine Hubbard exchange.
        Sites index logical qubits (site spin ↑=0, ↓=1)."""
        for layer in program:
            for spec in layer:
                kind = spec[0]
                if kind == "h":
                    psi = self.fn_hadamard(int(spec[1])) @ psi
                elif kind == "x":
                    psi = self.fn_x(int(spec[1])) @ psi
                elif kind == "z":
                    psi = self.fn_z(int(spec[1])) @ psi
                elif kind == "rz":
                    psi = self.fermionic_rotor(int(spec[1]), float(spec[2]) / 2.0,
                                               (0, 0, 1)) @ psi
                elif kind == "cnot":
                    psi = self.fn_cnot(int(spec[1]), int(spec[2])) @ psi
                elif kind == "exch":
                    psi = self.exchange_operator(float(spec[3])) @ psi
                else:
                    raise ValueError(f"field-native runner: unknown gate {kind!r}")
        return psi

    def spin_entanglement(self, psi, s0=0, s1=1):
        """Entanglement entropy between the two site-SPINS, computed in the
        half-filling (one-per-site) subspace where each site carries a clean
        qubit.  Projects ψ onto that subspace, maps to a 2-qubit spin state,
        and returns the von Neumann entropy of site s0's spin."""
        # In the Sz-resolved one-per-site sector the spin state is spanned by
        # |↑↑⟩,|↑↓⟩,|↓↑⟩,|↓↓⟩ on (s0,s1).  Extract those four amplitudes.
        basis = {
            (0, 0): [self.orb(s0, 0), self.orb(s1, 0)],
            (0, 1): [self.orb(s0, 0), self.orb(s1, 1)],
            (1, 0): [self.orb(s0, 1), self.orb(s1, 0)],
            (1, 1): [self.orb(s0, 1), self.orb(s1, 1)],
        }
        amps = np.zeros(4, dtype=complex)
        for idx, (key, orbs) in enumerate(basis.items()):
            bra = self.fock_state(orbs)
            amps[idx] = np.vdot(bra, psi)
        nrm = np.linalg.norm(amps)
        if nrm < 1e-14:
            return 0.0, 0.0
        amps = amps / nrm
        # reduced density matrix of the first spin (2×2)
        C = amps.reshape(2, 2)
        rho = C @ C.conj().T
        ev = np.linalg.eigvalsh(rho).real
        ev = ev[ev > 1e-15]
        S = float(-(ev * np.log(ev)).sum())
        weight = float(nrm ** 2)   # probability in the one-per-site sector
        return S, weight


# ───────────────────────── convenience / derivation ────────────────────────
def two_site_singlet_triplet_gap(t, U):
    """Singlet–triplet gap of the genuine two-site, two-fermion Hubbard model
    (S_z=0 sector), by exact diagonalisation of the second-quantized H."""
    fc = FermionChain(2, t, U)
    w, V = np.linalg.eigh(fc.H)
    # restrict to the N=2, S_z=0 sector
    Ntot = sum(fc.n)
    Sz = 0.5 * sum(fc.n[fc.orb(s, 0)] - fc.n[fc.orb(s, 1)] for s in range(2))
    energies = []
    for k in range(len(w)):
        v = V[:, k]
        nN = np.real(np.vdot(v, Ntot @ v))
        nSz = np.real(np.vdot(v, Sz @ v))
        if abs(nN - 2) < 1e-6 and abs(nSz) < 1e-6:
            energies.append(w[k])
    energies = sorted(energies)
    # singlet is the ground state; the S_z=0 triplet member sits at E=0
    E_singlet = energies[0]
    E_triplet = min(e for e in energies if e > E_singlet - 1e-9 and abs(e) < 1e-6) \
        if any(abs(e) < 1e-6 for e in energies) else 0.0
    return float(E_triplet - E_singlet)


def hopping_and_gap(m):
    """(t, U) for mass m, taken from the ca_dirac hopping and mass gap (F214)."""
    if _E is None:
        raise RuntimeError("ca_entanglement not importable")
    return _E.hopping_amplitude(m), _E.mass_gap(m)
