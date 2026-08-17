#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F217 — Field-native two-fermion second quantization: super-exchange J and
        spin entanglement EMERGE from real fermion hopping (beyond F214's
        effective spin model), wired live into casim
========================================================================
Date: 2026-07-01

F214 derived J from an *effective* two-site Hubbard (a spin model).  Here we
build the genuine fermionic Fock space (Jordan–Wigner operators on a lattice
chain, `ca_second_quant.py`) and show the same physics EMERGES from second
quantization — hopping t (from ca_dirac) + on-site U (mass gap) + Pauli — with
the effective exchange gate recovered only in the large-U limit.

Pass gates
----------
G1  genuine fermions: {c_i,c_j†}=δ_ij, {c_i,c_j}=0 to machine zero.
G2  Pauli + product init: |↑,↓⟩ has zero same-site double occupancy, spin
    correlation −¼, and zero spin entanglement (a single Slater determinant).
G3  super-exchange J from full 2nd-quantized diagonalisation == F214 closed
    form ½(√(U²+16t²)−U) to <1e-12, for every m.
G4  large-U limit: as U/t grows the field-native spin dynamics → the pure
    exchange gate — peak spin entanglement → ln2, doublon leakage → 0.
G5  LIVE casim `fermion_chain` channel: from |↑,↓⟩ real hopping generates
    two-site spin entanglement (S grows from 0), norm conserved, and
    checkpoint→resume is bit-identical.
"""
import os, sys, json, math
import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from casim.engine.interactions import qi_entanglement as E
from casim.engine.particles import second_quant as SQ
from casim.engine import Simulation, LatticeSpec, build_channel, build_observer

LN2 = math.log(2.0)
RESULTS = {'finding': 'F217', 'date': '2026-07-01',
           'title': 'Field-native two-fermion second quantization', 'tests': {}}


def test_G1_fermion_algebra():
    c = SQ.jw_annihilation(4)
    cd = [x.conj().T for x in c]
    I = np.eye(16)
    max_ac, max_cc = 0.0, 0.0
    for i in range(4):
        for j in range(4):
            ac = c[i] @ cd[j] + cd[j] @ c[i] - (I if i == j else 0)
            cc = c[i] @ c[j] + c[j] @ c[i]
            max_ac = max(max_ac, float(np.max(np.abs(ac))))
            max_cc = max(max_cc, float(np.max(np.abs(cc))))
    assert max_ac < 1e-12 and max_cc < 1e-12, (max_ac, max_cc)
    RESULTS['tests']['G1_algebra'] = {'max_anticommutator_err': max_ac,
                                      'max_cc': max_cc}
    print(f'G1 fermion algebra: PASS  |{{c,c†}}−δ|={max_ac:.1e}, |{{c,c}}|={max_cc:.1e}')


def test_G2_pauli_product_init():
    t, U = SQ.hopping_and_gap(0.5)
    fc = SQ.FermionChain(2, t, U)
    psi = fc.neel_two_site()
    d = fc.double_occupancy(psi, 0)
    corr = fc.spin_correlation(psi, 0, 1)
    S, w = fc.spin_entanglement(psi, 0, 1)
    assert abs(d) < 1e-12, f'double occupancy nonzero: {d}'
    assert abs(corr + 0.25) < 1e-12, f'spin corr {corr} != -1/4'
    assert abs(S) < 1e-12 and abs(w - 1) < 1e-12
    RESULTS['tests']['G2_pauli'] = {'double_occ': d, 'spin_corr': corr,
                                    'S_init': S, 'one_per_site_weight': w}
    print(f'G2 Pauli/product init: PASS  double-occ={d:.1e}, ⟨S·S⟩={corr:.4f}, S={S:.1e}')


def test_G3_J_emerges():
    rows, worst = [], 0.0
    for m in [0.2, 0.3, 0.5, 0.7, 0.9]:
        t, U = SQ.hopping_and_gap(m)
        J2 = SQ.two_site_singlet_triplet_gap(t, U)   # full 2nd-quantized diag
        Jf = E.superexchange_J(t, U)                 # F214 closed form
        worst = max(worst, abs(J2 - Jf))
        rows.append({'m': m, 't': t, 'U': U, 'J_2ndQ': J2, 'J_F214': Jf})
    assert worst < 1e-12, f'J mismatch {worst}'
    RESULTS['tests']['G3_J_emerges'] = {'rows': rows, 'worst': worst}
    print(f'G3 J emerges from 2nd-quant: PASS  max|J_2ndQ−J_F214|={worst:.1e}')


def test_G4_large_U_limit():
    rows = []
    for m in [0.5, 0.8, 0.9, 0.98]:
        t, U = SQ.hopping_and_gap(m)
        fc = SQ.FermionChain(2, t, U)
        psi0 = fc.neel_two_site()
        tau = E.bell_time_ticks(m)
        peakS, minw, maxd = 0.0, 1.0, 0.0
        for tt in np.linspace(0, tau, 50):
            p = fc.evolve(psi0, tt)
            S, w = fc.spin_entanglement(p)
            peakS = max(peakS, S); minw = min(minw, w)
            maxd = max(maxd, fc.double_occupancy(p, 0))
        rows.append({'m': m, 'U_over_t': U / t, 'peak_S': peakS,
                     'min_one_per_site': minw, 'max_doublon': maxd})
    # convergence: largest U/t is closest to ln2 and least doublon leakage
    assert abs(rows[-1]['peak_S'] - LN2) < 1e-4, rows[-1]
    assert rows[-1]['max_doublon'] < rows[0]['max_doublon']
    RESULTS['tests']['G4_large_U'] = {'rows': rows}
    print(f'G4 large-U → exchange gate: PASS  peakS(m=.98)={rows[-1]["peak_S"]:.6f} '
          f'(ln2={LN2:.6f}), doublon {rows[0]["max_doublon"]:.3f}→{rows[-1]["max_doublon"]:.3f}')


def test_G5_live_channel_and_checkpoint():
    import tempfile
    m = 0.9
    tau = int(round(E.bell_time_ticks(m)))

    def fresh(obs_every=1):
        lat = LatticeSpec(L=8, dims=3, topology='cubic')
        ch = build_channel({'type': 'fermion_chain', 'n_sites': 2,
                            'm': m, 'init': 'neel'})
        obs = build_observer({'type': 'fermion_entanglement', 'every': obs_every})
        return Simulation(lat, [ch], [obs], seed=0, name='ferm')

    sim = fresh(obs_every=max(1, tau // 8))
    res = sim.run(tau + 1)
    recs = res['observers']['fermion_entanglement']['records']
    S0 = recs[0]['spin_entanglement']
    Smax = max(r['spin_entanglement'] for r in recs)
    assert abs(S0) < 1e-12
    assert Smax > 0.6                                   # generated live, near ln2
    assert all(abs(r['norm'] - 1) < 1e-12 for r in recs)

    # checkpoint/resume bit-identical
    A = fresh(); A.step(3)
    with tempfile.TemporaryDirectory() as d:
        p = A.checkpoint(os.path.join(d, 'c.npz'))
        R = Simulation.resume(p); R.step(3)
    B = fresh(); B.step(6)
    cn = list(B.channels)[0]
    err = float(np.max(np.abs(R.states[cn]['psi'] - B.states[cn]['psi'])))
    assert err == 0.0, f'checkpoint/resume not bit-identical: {err}'

    RESULTS['tests']['G5_live'] = {'tau': tau, 'S_initial': S0,
                                   'S_max': Smax, 'checkpoint_err': err}
    print(f'G5 live fermion_chain: PASS  S: {S0:.1e} → {Smax:.6f} live; '
          f'checkpoint/resume bit-identical (err={err})')


def main():
    print('=' * 70)
    print('F217 — field-native two-fermion second quantization')
    print('=' * 70)
    test_G1_fermion_algebra()
    test_G2_pauli_product_init()
    test_G3_J_emerges()
    test_G4_large_U_limit()
    test_G5_live_channel_and_checkpoint()
    print('=' * 70)
    print('ALL PASS — super-exchange J and spin entanglement emerge from real fermion hopping.')
    out = os.path.join(ROOT, 'test-results', 'F217_field_native_fermion_entanglement.json')
    with open(out, 'w') as f:
        json.dump(RESULTS, f, indent=2)
    print(f'Results → {out}')


if __name__ == '__main__':
    main()
