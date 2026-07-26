#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F212 — Does the lattice substrate GENERATE entanglement it isn't given?
=======================================================================
Date: 2026-07-01

Follow-up to the quantum-computing cross-test.  Every many-body sector so far
(`ca_manybody.py` Hartree/variational; `test_02_QM1_CHSH.py` Part-3) is
mean-field / first-quantised: a PRODUCT of single-cell amplitudes, dimension
~2N, zero entanglement by construction.  The CHSH lattice test even inserts its
"singlet" by hand as A_up·B_down.

Here we build a genuine 2^n tensor-product register (`ca_entanglement.py`) whose
gates are the model's OWN primitives — the per-cell SU(2) rotor (ca_dirac F26
form) and the nearest-neighbour spinor EXCHANGE interaction σ_A·σ_B — start
from PRODUCT states, and MEASURE the reduced-density-matrix entropy.

Gates (both native):
  * single-qubit  R(θ,n̂) = cosθ I − i sinθ (n̂·σ)   [ca_dirac mass/coupling rotor]
  * two-qubit     U_exch(θ) = exp(−iθ σ_A·σ_B)      [lattice super-exchange]

Pass gates
----------
T1  primitives unitary to <1e-12; SWAP=(I+σ·σ)/2 permutes exactly.
T2  product init entropy = 0 (<1e-12);  exchange(π/8) drives S → ln2 (<1e-12);
    entropy sweep matches the analytic curve S(θ) with p=cos²2θ (<1e-12).
T3  MEAN-FIELD cannot host it: best single-product fidelity to the Bell output
    = 1/2 (<1e-12); Hartree time-evolution keeps S ≈ 0 (<1e-9); the generated
    entropy gap = ln2.
T4  native 3-qubit dynamical generation: product |+00⟩ → exchange(0,1),(1,2)
    yields all three single-qubit-cut entropies > 0 (genuine tripartite),
    norm preserved (<1e-12).
T5  engine-readout validation: GHZ has S = ln2 across every single-qubit cut
    (<1e-12).
"""
import os, sys, json, math
import numpy as np

THIS = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(THIS, '..', '..', 'ca-simulation')))
import ca_entanglement as E

LN2 = math.log(2.0)
RESULTS = {'finding': 'F212', 'date': '2026-07-01',
           'title': 'Dynamical entanglement generation on the lattice', 'tests': {}}


def _analytic_S(theta):
    p = math.cos(2 * theta) ** 2
    if p <= 0 or p >= 1:
        return 0.0
    return -(p * math.log(p) + (1 - p) * math.log(1 - p))


def test_T1_primitives():
    exch = E.exchange_gate(0.31)
    rot = E.su2_rotor(0.7, (1, 0, 1))
    swap = E.swap_gate()
    for G in (exch, rot, swap):
        u = G.conj().T @ G
        assert np.max(np.abs(u - np.eye(G.shape[0]))) < 1e-12
    # SWAP permutes |↑↓⟩ ↔ |↓↑⟩ exactly
    v = swap @ np.array([0, 1, 0, 0], complex)
    assert np.allclose(v, np.array([0, 0, 1, 0], complex), atol=1e-14)
    # exchange operator identity: SWAP == (I + σ·σ)/2
    sdots = (np.kron(E.SX, E.SX) + np.kron(E.SY, E.SY) + np.kron(E.SZ, E.SZ))
    assert np.max(np.abs(swap - 0.5 * (np.eye(4) + sdots))) < 1e-14
    RESULTS['tests']['T1_primitives'] = {'unitary': True, 'swap_identity': True}
    print('T1 primitives: PASS')


def test_T2_two_qubit_generation():
    # PRODUCT initial state — no entanglement supplied
    reg = E.Register([E.KET0, E.KET1])
    S0 = reg.entropy([0])
    assert abs(S0) < 1e-12, f'initial state not a product: S0={S0}'

    # exchange drives it to a MAXIMALLY entangled state
    reg.apply_2q(E.exchange_gate(math.pi / 8), 0, 1)
    S1 = reg.entropy([0])
    assert abs(reg.norm() - 1) < 1e-12
    assert abs(S1 - LN2) < 1e-12, f'S1={S1}'

    # analytic sweep 0 → π/8
    sweep = []
    max_err = 0.0
    for th in np.linspace(0, math.pi / 8, 17):
        r = E.Register([E.KET0, E.KET1])
        r.apply_2q(E.exchange_gate(th), 0, 1)
        S = r.entropy([0])
        err = abs(S - _analytic_S(th))
        max_err = max(max_err, err)
        sweep.append({'theta': float(th), 'S': float(S), 'S_analytic': _analytic_S(th)})
    assert max_err < 1e-12, f'sweep max_err={max_err}'
    assert sweep[-1]['S'] > sweep[0]['S']  # monotone rise, generated dynamically

    # perfect-entangler certificate
    Se, Stgt = E.is_perfect_entangler_demo()
    assert abs(Se - Stgt) < 1e-12

    RESULTS['tests']['T2_two_qubit'] = {
        'S_initial_product': float(S0), 'S_final': float(S1),
        'S_target_ln2': LN2, 'residual': float(abs(S1 - LN2)),
        'sweep_max_err': float(max_err),
        'perfect_entangler': True, 'sweep': sweep}
    print(f'T2 two-qubit: PASS  S: {S0:.2e} → {S1:.12f} (ln2={LN2:.12f})')


def test_T3_meanfield_cannot_host():
    # exact Bell output
    reg = E.Register([E.KET0, E.KET1])
    reg.apply_2q(E.exchange_gate(math.pi / 8), 0, 1)
    S_exact = reg.entropy([0])

    # best product (Hartree) fidelity = largest squared Schmidt coeff = 1/2
    lam_max, lam = E.best_product_fidelity(reg.psi, 2, 2)
    assert abs(lam_max - 0.5) < 1e-12, f'lam_max={lam_max}'

    # explicit time-dependent Hartree evolution stays unentangled
    psi_mf, S_mf, ZZ_mf = E.meanfield_evolve_2q(E.KET0, E.KET1, math.pi / 8)
    assert S_mf < 1e-9, f'mean-field developed entropy: {S_mf}'

    # mean-field state fidelity to the exact entangled state ≤ best product = 1/2
    fid = abs(np.vdot(psi_mf, reg.psi)) ** 2
    assert fid <= 0.5 + 1e-9, f'fid={fid}'

    RESULTS['tests']['T3_meanfield'] = {
        'S_exact': float(S_exact), 'S_meanfield': float(S_mf),
        'entropy_gap': float(S_exact - S_mf),
        'best_product_fidelity': float(lam_max),
        'meanfield_state_fidelity': float(fid)}
    print(f'T3 mean-field: PASS  exact S={S_exact:.6f}, Hartree S={S_mf:.2e}, '
          f'gap={S_exact - S_mf:.6f}, product-fidelity={lam_max:.6f}')


def test_T4_native_tripartite():
    reg = E.Register([E.KETP, E.KET0, E.KET0])   # product |+00⟩
    cuts0 = [reg.entropy([q]) for q in range(3)]
    assert max(abs(c) for c in cuts0) < 1e-12

    # native exchange dynamics spreads entanglement across all three cells
    reg.apply_2q(E.exchange_gate(math.pi / 8), 0, 1)
    reg.apply_2q(E.exchange_gate(math.pi / 8), 1, 2)
    cuts = [reg.entropy([q]) for q in range(3)]
    assert abs(reg.norm() - 1) < 1e-12
    assert all(c > 1e-6 for c in cuts), f'not genuinely tripartite: {cuts}'

    RESULTS['tests']['T4_tripartite'] = {
        'cuts_initial': [float(c) for c in cuts0],
        'cuts_final': [float(c) for c in cuts],
        'genuine_tripartite': True}
    print(f'T4 native 3-qubit: PASS  cuts {[round(c,4) for c in cuts]} (all > 0)')


def test_T5_ghz_readout():
    reg = E.make_ghz(3)
    cuts = [reg.entropy([q]) for q in range(3)]
    for c in cuts:
        assert abs(c - LN2) < 1e-12, f'GHZ cut {c} != ln2'
    # GHZ amplitudes only on |000⟩ and |111⟩
    amp = reg.psi
    big = np.where(np.abs(amp) > 1e-9)[0]
    assert set(big.tolist()) == {0, 7}
    RESULTS['tests']['T5_ghz'] = {'cuts': [float(c) for c in cuts], 'target': LN2}
    print(f'T5 GHZ readout: PASS  cuts {[round(c,6) for c in cuts]} = ln2')


def main():
    print('=' * 70)
    print('F208 — Dynamical entanglement generation on the lattice')
    print('=' * 70)
    test_T1_primitives()
    test_T2_two_qubit_generation()
    test_T3_meanfield_cannot_host()
    test_T4_native_tripartite()
    test_T5_ghz_readout()
    print('=' * 70)
    print('ALL PASS — the substrate generates entanglement entropy it is not given.')
    out = os.path.join(THIS, '..', '..', 'test-results', 'F212_entanglement_generation.json')
    with open(out, 'w') as f:
        json.dump(RESULTS, f, indent=2)
    print(f'Results → {out}')


if __name__ == '__main__':
    main()
