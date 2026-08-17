#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F218 — A quantum ALGORITHM run through the engine: native exchange→CZ/CNOT
        compilation + live 2-qubit Grover and Deutsch–Jozsa
========================================================================
Date: 2026-07-01

Capstone of the entanglement tier.  F212 showed the substrate *generates*
entanglement; here the substrate *computes*.  The exchange operator σ·σ=XX+YY+ZZ
commutes with ZZ and its XX,YY signs flip under σz⊗I, so two native exchange
gates sandwiching a σz give exactly exp(iπ/4 ZZ) — hence CZ and CNOT compile
EXACTLY from the lattice exchange interaction + SU(2) rotors (a constructive
universality proof, complementing F212's perfect-entangler certificate).  Those
gates are composed into genuine algorithms that run tick-by-tick through the
live `casim` engine.

Pass gates
----------
G1  native gate set exact: exp(iπ/4 ZZ), CZ, CNOT, Hadamard from exchange+rotors
    to <1e-12; all unitary.
G2  2-qubit Grover finds every marked item (0..3) with probability 1 (<1e-12).
G3  Grover runs LIVE through the engine (quantum_circuit channel): final argmax =
    marked, p=1; norm conserved.
G4  Deutsch–Jozsa (1 query) decides constant vs balanced for all four oracles.
G5  engine integrity: checkpoint mid-algorithm → resume reproduces the exact
    final state and correct answer (bit-identical).
"""
import os, sys, json, math
import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import casim  # noqa: F401  (package bootstrap)
from casim.engine.interactions import qi_entanglement as E
from casim.engine.interactions import qi_algorithms as QA
from casim.engine import Simulation, LatticeSpec, build_channel, build_observer

RESULTS = {'finding': 'F218', 'date': '2026-07-01',
           'title': 'Quantum algorithm through the engine', 'tests': {}}


def _unitary_err(U):
    return float(np.max(np.abs(U.conj().T @ U - np.eye(U.shape[0]))))


def test_G1_native_gates_exact():
    zz = E.native_zz_quarter()
    zz_ref = np.diag([np.exp(1j*np.pi/4), np.exp(-1j*np.pi/4),
                      np.exp(-1j*np.pi/4), np.exp(1j*np.pi/4)])
    zz_aligned = zz * (zz_ref[0, 0] / zz[0, 0])   # up to global phase
    cz = E.native_cz(); cnot = E.native_cnot(); H = E.native_hadamard()
    errs = {
        'zz': float(np.max(np.abs(zz_aligned - zz_ref))),
        'cz': float(np.max(np.abs(cz - np.diag([1, 1, 1, -1])))),
        'cnot': float(np.max(np.abs(cnot - E.CNOT_REF))),
        'hadamard': float(np.max(np.abs(H - np.array([[1, 1], [1, -1]]) / np.sqrt(2)))),
    }
    for k, v in errs.items():
        assert v < 1e-12, f'{k} err {v}'
    for U in (zz, cz, cnot, H):
        assert _unitary_err(U) < 1e-12
    RESULTS['tests']['G1_native_gates'] = errs
    print(f'G1 native gates exact: PASS  CZ={errs["cz"]:.1e}, CNOT={errs["cnot"]:.1e}')


def test_G2_grover_direct():
    res = {}
    for w in range(4):
        prog, n = QA.grover_2q(w)
        p = E.probabilities(E.run_circuit(n, prog))
        assert int(np.argmax(p)) == w and abs(p[w] - 1.0) < 1e-12, (w, p)
        res[w] = float(p[w])
    RESULTS['tests']['G2_grover_direct'] = res
    print(f'G2 Grover (direct): PASS  all 4 marked items found with p=1')


def test_G3_grover_live():
    res = {}
    for w in range(4):
        prog, n = QA.grover_2q(w)
        ch = build_channel({'type': 'quantum_circuit', 'n_qubits': n, 'program': prog})
        obs = build_observer({'type': 'circuit_readout', 'every': 1})
        sim = Simulation(LatticeSpec(L=8, dims=3, topology='cubic'), [ch], [obs], name='grover')
        summ = sim.run(len(prog))['observers']['circuit_readout']['summary']
        assert summ['final_argmax'] == w and abs(summ['final_p'] - 1.0) < 1e-12
        assert abs(sim.state_norms()[ch.name] - 1.0) < 1e-12
        res[w] = summ['final_p']
    RESULTS['tests']['G3_grover_live'] = res
    print(f'G3 Grover (live in engine): PASS  all 4 found with p=1, norm conserved')


def test_G4_deutsch_jozsa():
    verdicts = {}
    for kind in ['const0', 'const1', 'balanced_id', 'balanced_not']:
        prog, n = QA.deutsch_jozsa_1(kind)
        p1 = QA.measured_bit0_probability(E.run_circuit(n, prog))
        verdict = 'balanced' if p1 > 0.5 else 'constant'
        expected = 'constant' if kind.startswith('const') else 'balanced'
        assert verdict == expected, (kind, p1)
        # deterministic: p1 is exactly 0 or 1
        assert min(p1, 1 - p1) < 1e-12
        verdicts[kind] = verdict
    RESULTS['tests']['G4_deutsch_jozsa'] = verdicts
    print(f'G4 Deutsch–Jozsa: PASS  const→constant, balanced→balanced (1 query)')


def test_G5_checkpoint_midalgorithm():
    import tempfile
    prog, n = QA.grover_2q(2)

    def fresh():
        ch = build_channel({'type': 'quantum_circuit', 'n_qubits': n, 'program': prog})
        obs = build_observer({'type': 'circuit_readout', 'every': 1})
        return Simulation(LatticeSpec(L=8, dims=3, topology='cubic'), [ch], [obs], name='g')

    A = fresh(); A.step(3)                       # partway through the circuit
    with tempfile.TemporaryDirectory() as d:
        p = A.checkpoint(os.path.join(d, 'c.npz'))
        R = Simulation.resume(p); R.step(len(prog) - 3)
    B = fresh(); B.step(len(prog))
    cn = list(B.channels)[0]
    err = float(np.max(np.abs(R.states[cn]['psi'] - B.states[cn]['psi'])))
    assert err == 0.0, f'not bit-identical: {err}'
    # resumed run still solves it
    pr = E.probabilities(R.states[cn]['psi'])
    assert int(np.argmax(pr)) == 2 and abs(pr[2] - 1) < 1e-12
    RESULTS['tests']['G5_checkpoint'] = {'psi_max_err': err, 'answer': int(np.argmax(pr))}
    print(f'G5 checkpoint mid-algorithm: PASS  bit-identical resume, answer=2')


def main():
    print('=' * 70)
    print('F218 — quantum algorithm through the engine')
    print('=' * 70)
    test_G1_native_gates_exact()
    test_G2_grover_direct()
    test_G3_grover_live()
    test_G4_deutsch_jozsa()
    test_G5_checkpoint_midalgorithm()
    print('=' * 70)
    print('ALL PASS — the substrate computes: native exchange→CNOT, Grover & DJ live in the engine.')
    out = os.path.join(ROOT, 'test-results', 'F218_algorithm_through_engine.json')
    with open(out, 'w') as f:
        json.dump(RESULTS, f, indent=2)
    print(f'Results → {out}')


if __name__ == '__main__':
    main()
