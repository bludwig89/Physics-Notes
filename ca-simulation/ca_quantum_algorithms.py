#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_quantum_algorithms.py  —  quantum algorithms from the native gate set (F218)
===============================================================================

Composes the model's native, exactly-compiled universal gate set
(`ca_entanglement`: SU(2) rotor + spinor-exchange → H, CZ, CNOT) into genuine
quantum algorithms, expressed as JSON-serializable circuits (lists of layers)
so they run tick-by-tick through the live `casim` engine.

  * grover_2q(marked)         — 2-qubit Grover search: one iteration finds the
                                marked item of 4 with probability 1.
  * deutsch_jozsa_1(kind)     — Deutsch–Jozsa on 1 input + 1 ancilla: one oracle
                                query decides constant vs balanced.

These are the substrate *computing* — entanglement-powered algorithms, not just
entanglement generation — with every gate reduced to the lattice exchange
interaction + single-cell rotations.
"""
from __future__ import annotations


def _xmask(bits):
    """Layer of X gates on the qubits whose target bit is 0 (for phase-flipping
    an arbitrary basis state via a CZ sandwiched in X masks)."""
    return [["x", q] for q, b in enumerate(bits) if b == 0]


def grover_2q(marked: int):
    """2-qubit Grover search for `marked` ∈ {0,1,2,3}.  Returns (program, n=2).

    One Grover iteration (oracle + diffusion) rotates the uniform superposition
    exactly onto |marked⟩ for a 4-item search (θ=arcsin(½) ⇒ exact after 1 step).
    """
    b = [(marked >> 1) & 1, marked & 1]        # (qubit0 bit, qubit1 bit)
    mask = _xmask(b)
    program = [
        [["h", 0], ["h", 1]],                  # uniform superposition
        # oracle: phase-flip |marked⟩
        mask, [["cz", 0, 1]], mask,
        # diffusion (inversion about the mean)
        [["h", 0], ["h", 1]],
        [["x", 0], ["x", 1]],
        [["cz", 0, 1]],
        [["x", 0], ["x", 1]],
        [["h", 0], ["h", 1]],
    ]
    program = [layer for layer in program if layer]   # drop empty mask layers
    return program, 2


def deutsch_jozsa_1(kind: str):
    """Deutsch–Jozsa, 1 input qubit (q0) + 1 ancilla (q1).  kind ∈
    {"const0","const1","balanced_id","balanced_not"}.  Returns (program, n=2).

    After the circuit, measuring q0 gives 0 for a CONSTANT f and 1 for a
    BALANCED f — decided with a single oracle query.  Ancilla starts in |1⟩.
    """
    oracle = {
        "const0": [],                                  # f(x)=0 : identity
        "const1": [[["x", 1]]],                        # f(x)=1 : flip ancilla
        "balanced_id": [[["cnot", 0, 1]]],             # f(x)=x
        "balanced_not": [[["x", 1]], [["cnot", 0, 1]]],  # f(x)=¬x
    }[kind]
    program = [
        [["x", 1]],                # ancilla → |1⟩
        [["h", 0], ["h", 1]],      # H on both
        *oracle,                   # U_f
        [["h", 0]],                # H on the input qubit
    ]
    return program, 2


def measured_bit0_probability(psi):
    """P(input qubit q0 = 1) for a 2-qubit state (basis 00,01,10,11)."""
    import numpy as np
    p = np.abs(psi) ** 2
    return float(p[2] + p[3])     # q0=1 → indices 10,11


# ═══════════════════════════════════════════════════════════════════════
#  Scaled algorithms (F219) — n-qubit Grover, Bernstein–Vazirani, QFT, GHZ
# ═══════════════════════════════════════════════════════════════════════
import math as _math


def grover_iterations(n, n_marked=1):
    """Optimal number of Grover iterations for `n` qubits, `n_marked` targets:
    round( (π/4)·√(2ⁿ / M) − ½ )."""
    N = 2 ** n
    return max(1, int(round((_math.pi / 4.0) * _math.sqrt(N / n_marked) - 0.5)))


def grover_nq(n, marked, iters=None):
    """n-qubit Grover search for one `marked` item ∈ {0,…,2ⁿ−1}.

    Oracle = X-mask · MCZ(all n qubits) · X-mask (phase-flips |marked⟩).
    Diffusion = H^⊗n · X^⊗n · MCZ(all) · X^⊗n · H^⊗n.
    Uses the direct-action "mcz" spec so it scales to large n.  Returns
    (program, n)."""
    allq = list(range(n))
    bits = [(marked >> (n - 1 - q)) & 1 for q in range(n)]   # q0 = MSB
    xmask = [["x", q] for q in range(n) if bits[q] == 0]
    Hall = [["h", q] for q in range(n)]
    Xall = [["x", q] for q in range(n)]
    mcz = [["mcz", allq]]
    oracle = [xmask, mcz, xmask]
    diffusion = [Hall, Xall, mcz, Xall, Hall]
    program = [Hall]
    it = grover_iterations(n) if iters is None else iters
    for _ in range(it):
        program += oracle + diffusion
    program = [layer for layer in program if layer]
    return program, n


def bernstein_vazirani(secret, n):
    """Bernstein–Vazirani: recover an n-bit `secret` string with ONE oracle
    query.  n input qubits (q0…q_{n−1}) + 1 ancilla (q_n).  Oracle f(x)=s·x
    mod 2 is a set of CNOTs from each input with s_i=1 into the ancilla.
    Measuring the inputs returns `secret` deterministically.  Returns
    (program, n+1)."""
    anc = n
    bits = [(secret >> (n - 1 - q)) & 1 for q in range(n)]   # q0 = MSB of secret
    Hin = [["h", q] for q in range(n)]
    prep_anc = [["x", anc], ["h", anc]]                      # ancilla → |−⟩
    oracle = [["cnot", q, anc] for q in range(n) if bits[q] == 1]
    program = [prep_anc, Hin]
    if oracle:
        program.append(oracle)
    program.append(Hin)
    program = [layer for layer in program if layer]
    return program, n + 1


def qft_circuit(n, inverse=False):
    """Quantum Fourier transform on n qubits from native H + controlled-phase.
    Standard construction: on each qubit q, an H then controlled-phase
    π/2^{k} from every later qubit, followed by a bit-reversal SWAP network.
    `inverse=True` negates the phases and reverses the order (QFT†).  Returns
    a flat gate list (single conceptual layer sequence), n."""
    # Build the forward QFT as a flat gate list, then, if requested, return its
    # exact inverse = reverse the order and conjugate each gate (H/cnot are
    # self-inverse, cphase(θ)→cphase(−θ)).
    gates = []
    for j in range(n):
        gates.append(["h", j])
        for k in range(j + 1, n):
            gates.append(["cphase", k, j, _math.pi / (2 ** (k - j))])
    for i in range(n // 2):                       # bit-reversal SWAP network
        a, b = i, n - 1 - i
        gates += [["cnot", a, b], ["cnot", b, a], ["cnot", a, b]]

    if inverse:
        inv = []
        for g in reversed(gates):
            if g[0] == "cphase":
                inv.append(["cphase", g[1], g[2], -g[3]])
            else:
                inv.append(list(g))
        gates = inv

    layers = [[g] for g in gates]                 # one gate per layer
    return layers, n


def ghz_circuit(n):
    """Prepare the n-qubit GHZ state from |0…0⟩ with a native H + CNOT chain.
    Every single-qubit cut has entanglement entropy ln2.  Returns (program,
    n)."""
    program = [[["h", 0]]]
    for q in range(1, n):
        program.append([["cnot", 0, q]])
    return program, n
