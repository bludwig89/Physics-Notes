#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F220 — Field-native execution: quantum gates and a full algorithm run on the
        genuine second-quantized Fock sector (computation on real matter)
========================================================================
Date: 2026-07-01

F217 built the genuine fermionic Fock space; F218/F219 ran algorithms on an
abstract register.  F220 closes the deep tier: it runs the gates — and a
complete algorithm — DIRECTLY on the Fock state.  A logical qubit is the SPIN of
a singly-occupied site.  Single-qubit gates are exact fermionic operators
exp(−i·2θ n̂·S_s) (they conserve the per-site occupation, zero leakage); the
two-qubit entangler is the REAL Hubbard time-evolution e^{−iHt} whose emergent
super-exchange (F214/F217) becomes the exact exchange gate as U/t→∞.

Pass gates
----------
G1  single-qubit fermionic gate == abstract su2_rotor to <1e-12, one-per-site
    weight conserved exactly (=1).
G2  entangler = genuine Hubbard dynamics → exchange gate: fidelity to the ideal
    exchange gate → 1 and spin entropy → ln2 as U/t grows (Bell state on matter).
G3  field-native CNOT acts as the textbook CNOT on the site-spin register to
    sub-percent, leakage-limited (improving story vs the ideal at large U).
G4  full field-native Deutsch–Jozsa: all four oracles classified correctly
    (const→constant, balanced→balanced), the whole computation in Fock space.
G5  live in the engine: fermion_algorithm channel runs DJ tick-by-tick and
    returns the right verdict; checkpoint mid-run resumes bit-identical.
"""
import os, sys, json, tempfile
import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import casim  # noqa: F401
import ca_entanglement as E
import ca_second_quant as SQ
from casim.engine import Simulation, LatticeSpec, build_channel, build_observer

RESULTS = {'finding': 'F220', 'date': '2026-07-01',
           'title': 'Field-native execution in the fermion chain', 'tests': {}}


def _chain(m):
    t, U = E.hopping_amplitude(m), E.mass_gap(m)
    return SQ.FermionChain(2, t, U), t, U


def test_G1_single_qubit_exact():
    fc, t, U = _chain(0.5)
    psi = fc.neel_two_site()                       # |↑,↓⟩ = spin |0,1⟩
    errs = {}
    for axis in [(1, 0, 1), (0, 1, 0), (0, 0, 1), (1, 1, 1)]:
        for th in [0.3, np.pi / 2, 1.7]:
            Uf = fc.fermionic_rotor(0, th, axis)
            out = Uf @ psi
            amps, w = fc.spin_register(out)
            ab = E.apply_gate(E.product_state([E.KET0, E.KET1]),
                              E.su2_rotor(th, axis), [0], 2)
            j = int(np.argmax(np.abs(ab)))
            ph = ab[j] / amps[j]
            errs[f'{axis}_{th:.2f}'] = float(np.max(np.abs(amps * ph - ab)))
            assert abs(w - 1.0) < 1e-12, w        # single-qubit: no leakage
    worst = max(errs.values())
    assert worst < 1e-12, errs
    RESULTS['tests']['G1_single_qubit_exact'] = {'worst_err': worst}
    print(f'G1 single-qubit fermionic gate exact: PASS  worst err {worst:.1e}, '
          f'weight=1 (no leakage)')


def test_G2_entangler_convergence():
    res = {}
    ideal = E.apply_gate(E.product_state([E.KET0, E.KET1]),
                         E.exchange_gate(np.pi / 8), [0, 1], 2)
    prev_fid = 0.0
    for m in [0.5, 0.8, 0.9, 0.95, 0.98]:
        fc, t, U = _chain(m)
        out = fc.fermionic_exchange(fc.neel_two_site(), np.pi / 8)
        amps, w = fc.spin_register(out)
        fid = float(abs(np.vdot(ideal, amps)) ** 2)
        S = E.entropy_of_vector(amps, 2, [0])
        res[m] = {'U_over_t': U / t, 'fidelity': fid, 'weight': w, 'entropy': S}
    # high-U point is essentially the exact exchange gate + a Bell state (S=ln2)
    hi = res[0.98]
    assert hi['fidelity'] > 0.999 and abs(hi['entropy'] - np.log(2)) < 1e-3
    assert res[0.98]['fidelity'] > res[0.5]['fidelity']   # converges with U/t
    RESULTS['tests']['G2_entangler_convergence'] = res
    print(f'G2 entangler = genuine Hubbard dynamics: PASS  fidelity '
          f'{res[0.5]["fidelity"]:.3f}→{hi["fidelity"]:.4f}, S→ln2 (Bell on matter)')


def test_G3_field_native_cnot():
    res = {}
    for m in [0.9, 0.95, 0.98]:
        fc, t, U = _chain(m)
        cnot = fc.fn_cnot(0, 1)
        errs = []
        for b in range(4):
            c, tt = (b >> 1) & 1, b & 1
            psi = fc.fock_state([fc.orb(0, c), fc.orb(1, tt)])
            amps, w = fc.spin_register(cnot @ psi)
            ref = np.zeros(4, complex); ref[(c << 1) | (tt ^ c)] = 1
            j = int(np.argmax(np.abs(ref)))
            ph = ref[j] / amps[j]
            errs.append(float(np.max(np.abs(amps * ph - ref))))
        res[m] = {'U_over_t': U / t, 'max_basis_err': max(errs)}
        assert max(errs) < 0.01, (m, errs)        # sub-percent, leakage-limited
    RESULTS['tests']['G3_field_native_cnot'] = res
    print(f'G3 field-native CNOT: PASS  acts as textbook CNOT to <1% '
          f'(leakage-limited); worst {max(r["max_basis_err"] for r in res.values()):.4f}')


def _dj_program(kind):
    """Deutsch–Jozsa on site0 (input) + site1 (ancilla, starts |1⟩ via Néel)."""
    oracle = {'const0': [], 'const1': [[['x', 1]]],
              'balanced_id': [[['cnot', 0, 1]]],
              'balanced_not': [[['x', 1]], [['cnot', 0, 1]]]}[kind]
    return [[['h', 0], ['h', 1]], *oracle, [['h', 0]]]


def test_G4_field_native_deutsch_jozsa():
    verdicts = {}
    fc, t, U = _chain(0.95)
    for kind in ['const0', 'const1', 'balanced_id', 'balanced_not']:
        psi = fc.apply_program_fock(fc.neel_two_site(), _dj_program(kind))
        amps, w = fc.spin_register(psi)
        p = np.abs(amps) ** 2
        p1 = float(p[2] + p[3])                    # input site0 (MSB) = 1
        verdict = 'balanced' if p1 > 0.5 else 'constant'
        expected = 'constant' if kind.startswith('const') else 'balanced'
        assert verdict == expected, (kind, p1)
        verdicts[kind] = {'verdict': verdict, 'p1': p1, 'weight': w}
    RESULTS['tests']['G4_field_native_dj'] = verdicts
    print(f'G4 field-native Deutsch–Jozsa: PASS  all 4 oracles classified '
          f'correctly on genuine matter')


def test_G5_live_engine_and_checkpoint():
    prog = _dj_program('balanced_id')

    def fresh():
        ch = build_channel({'type': 'fermion_algorithm', 'n_sites': 2, 'm': 0.95,
                            'program': prog})
        obs = build_observer({'type': 'fermion_algorithm_readout', 'every': 1})
        return Simulation(LatticeSpec(L=6, dims=3, topology='cubic'), [ch], [obs],
                          name='dj')

    sim = fresh()
    summ = sim.run(len(prog))['observers']['fermion_algorithm_readout']['summary']
    # balanced → input qubit (site0, MSB) measured 1 → argmax in {2,3}
    assert summ['final_argmax'] in (2, 3), summ
    assert summ['final_weight'] > 0.99

    A = fresh(); A.step(1)
    with tempfile.TemporaryDirectory() as d:
        p = A.checkpoint(os.path.join(d, 'c.npz'))
        R = Simulation.resume(p); R.step(len(prog) - 1)
    B = fresh(); B.step(len(prog))
    cn = list(B.channels)[0]
    err = float(np.max(np.abs(R.states[cn]['psi'] - B.states[cn]['psi'])))
    assert err == 0.0, err
    RESULTS['tests']['G5_live_engine'] = {
        'final_argmax': summ['final_argmax'], 'final_weight': summ['final_weight'],
        'checkpoint_err': err}
    print(f'G5 live in engine: PASS  DJ verdict correct live, weight='
          f'{summ["final_weight"]:.4f}, checkpoint bit-identical')


def main():
    print('=' * 70)
    print('F220 — field-native execution in the fermion chain')
    print('=' * 70)
    test_G1_single_qubit_exact()
    test_G2_entangler_convergence()
    test_G3_field_native_cnot()
    test_G4_field_native_deutsch_jozsa()
    test_G5_live_engine_and_checkpoint()
    print('=' * 70)
    print('ALL PASS — the substrate computes on genuine second-quantized matter.')
    out = os.path.join(ROOT, 'test-results', 'F220_field_native_execution.json')
    with open(out, 'w') as f:
        json.dump(RESULTS, f, indent=2)
    print(f'Results → {out}')


if __name__ == '__main__':
    main()
