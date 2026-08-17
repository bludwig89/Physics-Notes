#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F222 — Scaling the substrate's quantum algorithms to many qubits, and proving
        the exponential register stays stable
========================================================================
Date: 2026-07-01

F218 ran 2-qubit Grover / Deutsch–Jozsa through the engine.  F222 scales it:
a general native controlled-phase and a fully-compiled native CCZ extend the
exact universality proof to 3-qubit controlled gates, and multi-controlled Z/X
act directly on the 2ⁿ vector (the exact action of the native Barenco ladder)
so genuine algorithms — n-qubit Grover, Bernstein–Vazirani, QFT, GHZ — scale to
large registers.  The question this finding answers: does the exponential
Hilbert space stay stable (norm, unitarity, correct answers, checkpointing) as n
grows?  Answer: yes, to machine precision through n≈12.

Pass gates
----------
G1  native CCZ + controlled-phase exact: native_ccz == diag(1..1,−1), native_cphase(φ)
    == diag(1,1,1,e^{iφ}) to <1e-12; both unitary.
G2  n-qubit Grover: success probability ≥ theoretical bound and argmax=marked for
    n = 3..12; norm conserved to <1e-10.
G3  QFT matches the discrete Fourier transform to <1e-10 and QFT†·QFT = I
    (round-trip) for n = 3..8.
G4  Bernstein–Vazirani recovers the secret string with ONE query, input-register
    marginal deterministic (P=1) for n = 4..12.
G5  Stability / engine integrity at scale: GHZ every-cut entropy = ln2 for n up to
    12; live 8-qubit Grover through the engine returns the marked item; checkpoint
    mid-algorithm resumes bit-identically (Δψ = 0).
"""
import os, sys, json, math, tempfile
import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import casim  # noqa: F401  (package bootstrap)
from casim.engine.interactions import qi_entanglement as E
from casim.engine.interactions import qi_algorithms as QA
from casim.engine import Simulation, LatticeSpec, build_channel, build_observer

RESULTS = {'finding': 'F222', 'date': '2026-07-01',
           'title': 'Scaled quantum algorithms + register stability', 'tests': {}}


def _unit(U):
    return float(np.max(np.abs(U.conj().T @ U - np.eye(U.shape[0]))))


def test_G1_native_ccz_cphase_exact():
    ccz = E.native_ccz()
    ccz_ref = np.diag([1, 1, 1, 1, 1, 1, 1, -1]).astype(complex)
    errs = {'ccz': float(np.max(np.abs(ccz - ccz_ref))), 'ccz_unit': _unit(ccz)}
    cp_errs = {}
    for phi in [np.pi / 2, np.pi / 3, -np.pi / 4, 1.234]:
        cp = E.native_cphase(phi)
        ref = np.diag([1, 1, 1, np.exp(1j * phi)])
        cp_errs[f'{phi:.3f}'] = float(np.max(np.abs(cp - ref)))
        assert _unit(cp) < 1e-12
    for v in list(errs.values())[:1] + list(cp_errs.values()):
        assert v < 1e-12, (errs, cp_errs)
    assert errs['ccz_unit'] < 1e-12
    RESULTS['tests']['G1_native_ccz_cphase'] = {'ccz': errs, 'cphase': cp_errs}
    print(f'G1 native CCZ+cphase exact: PASS  CCZ={errs["ccz"]:.1e}, '
          f'CP(max)={max(cp_errs.values()):.1e}')


def test_G2_grover_scaling():
    res = {}
    for n in range(3, 13):
        w = (2 ** n) // 3
        prog, _ = QA.grover_nq(n, w)
        psi = E.run_circuit(n, prog)
        p = E.probabilities(psi)
        it = QA.grover_iterations(n)
        # theoretical single-target success after `it` iterations
        theta = math.asin(1.0 / math.sqrt(2 ** n))
        p_theory = math.sin((2 * it + 1) * theta) ** 2
        assert int(np.argmax(p)) == w, (n, np.argmax(p), w)
        assert abs(p[w] - p_theory) < 1e-6, (n, p[w], p_theory)
        assert abs(np.linalg.norm(psi) - 1) < 1e-10, (n, np.linalg.norm(psi))
        res[n] = {'iters': it, 'P': float(p[w]), 'P_theory': p_theory,
                  'norm_err': float(abs(np.linalg.norm(psi) - 1))}
    worst_norm = max(r['norm_err'] for r in res.values())
    RESULTS['tests']['G2_grover_scaling'] = res
    print(f'G2 Grover n=3..12: PASS  all argmax=marked, P matches theory, '
          f'worst norm err {worst_norm:.1e}')


def test_G3_qft_correct_and_invertible():
    res = {}
    for n in range(3, 9):
        fwd, _ = QA.qft_circuit(n)
        inv, _ = QA.qft_circuit(n, inverse=True)
        x = (2 ** n) // 3
        kets = [E.KET1 if (x >> (n - 1 - q)) & 1 else E.KET0 for q in range(n)]
        psi0 = E.product_state(kets)
        psi = psi0.copy()
        for L in fwd:
            psi = E.apply_layer(psi, L, n)
        N = 2 ** n
        ref = np.array([np.exp(2j * np.pi * x * y / N) for y in range(N)]) / np.sqrt(N)
        ph = ref[0] / psi[0]
        dft_err = float(np.max(np.abs(psi * ph - ref)))
        for L in inv:
            psi = E.apply_layer(psi, L, n)
        rt = float(np.max(np.abs(psi - psi0)))
        assert dft_err < 1e-10 and rt < 1e-10, (n, dft_err, rt)
        res[n] = {'dft_err': dft_err, 'roundtrip_err': rt}
    RESULTS['tests']['G3_qft'] = res
    print(f'G3 QFT n=3..8: PASS  matches DFT and QFT†·QFT=I to <1e-10')


def test_G4_bernstein_vazirani():
    res = {}
    for n in [4, 6, 8, 10, 12]:
        secret = (2 ** n - 1) // 3
        prog, nq = QA.bernstein_vazirani(secret, n)
        psi = E.run_circuit(nq, prog)
        p = E.probabilities(psi).reshape([2] * nq)
        marg = p.sum(axis=nq - 1).reshape(-1)     # trace out the ancilla
        assert int(np.argmax(marg)) == secret and abs(marg[secret] - 1) < 1e-10
        res[n] = {'secret': secret, 'P': float(marg[secret])}
    RESULTS['tests']['G4_bernstein_vazirani'] = res
    print(f'G4 Bernstein–Vazirani n=4..12: PASS  secret recovered in 1 query, P=1')


def test_G5_stability_and_engine():
    # GHZ entropy = ln2 across every single-qubit cut, up to n=12
    ghz = {}
    for n in [3, 4, 8, 12]:
        prog, _ = QA.ghz_circuit(n)
        psi = E.run_circuit(n, prog)
        Ss = [E.entropy_of_vector(psi, n, [q]) for q in range(n)]
        assert abs(min(Ss) - np.log(2)) < 1e-9 and abs(max(Ss) - np.log(2)) < 1e-9
        ghz[n] = {'S_min': float(min(Ss)), 'S_max': float(max(Ss))}

    # live 8-qubit Grover through the engine
    n = 8; w = (2 ** n) // 3
    prog, _ = QA.grover_nq(n, w)
    ch = build_channel({'type': 'quantum_circuit', 'n_qubits': n, 'program': prog})
    obs = build_observer({'type': 'circuit_readout', 'every': 1})
    sim = Simulation(LatticeSpec(L=8, dims=3, topology='cubic'), [ch], [obs], name='g8')
    summ = sim.run(len(prog))['observers']['circuit_readout']['summary']
    assert summ['final_argmax'] == w and summ['final_p'] > 0.99
    assert abs(sim.state_norms()[ch.name] - 1) < 1e-10

    # checkpoint mid-algorithm → bit-identical resume
    def fresh():
        c = build_channel({'type': 'quantum_circuit', 'n_qubits': n, 'program': prog})
        o = build_observer({'type': 'circuit_readout', 'every': 1})
        return Simulation(LatticeSpec(L=8, dims=3, topology='cubic'), [c], [o], name='g')
    half = len(prog) // 2
    A = fresh(); A.step(half)
    with tempfile.TemporaryDirectory() as d:
        p = A.checkpoint(os.path.join(d, 'c.npz'))
        R = Simulation.resume(p); R.step(len(prog) - half)
    B = fresh(); B.step(len(prog))
    cn = list(B.channels)[0]
    err = float(np.max(np.abs(R.states[cn]['psi'] - B.states[cn]['psi'])))
    assert err == 0.0, err
    RESULTS['tests']['G5_stability_engine'] = {
        'ghz': ghz, 'live_grover8': {'argmax': summ['final_argmax'],
                                     'P': summ['final_p']},
        'checkpoint_err': err}
    print(f'G5 stability+engine: PASS  GHZ cuts=ln2 to n=12, live n=8 Grover P='
          f'{summ["final_p"]:.4f}, checkpoint bit-identical')


def main():
    print('=' * 70)
    print('F222 — scaled quantum algorithms + register stability')
    print('=' * 70)
    test_G1_native_ccz_cphase_exact()
    test_G2_grover_scaling()
    test_G3_qft_correct_and_invertible()
    test_G4_bernstein_vazirani()
    test_G5_stability_and_engine()
    print('=' * 70)
    print('ALL PASS — the exponential register scales and stays stable to n≈12.')
    out = os.path.join(ROOT, 'test-results', 'F222_scaled_quantum_algorithms.json')
    with open(out, 'w') as f:
        json.dump(RESULTS, f, indent=2)
    print(f'Results → {out}')


if __name__ == '__main__':
    main()
