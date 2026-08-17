#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F221 — Decoherence channels + stabilizer error correction: the engine studies
        fault tolerance, built on the native gate set
========================================================================
Date: 2026-07-01

F218/F219 are exact-unitary; F220 exposed a NATIVE decoherence source (virtual
doublon leakage).  F221 gives the engine the two ingredients fault tolerance
needs: an explicit Kraus noise channel and error-correcting codes, both built on
the model's own native gates (exchange-derived CNOT + SU(2) rotors).

Pass gates
----------
G1  noise channels are valid CPTP maps: Σ E†E = I; density matrices stay
    trace-1, Hermitian, PSD after each channel.
G2  3-qubit bit-flip code — corrected logical fidelity matches the exact
    closed form F=(1−3p²+2p³)+(3p²−2p³)(2ab)² to <1e-12, and the logical
    infidelity is O(p²) (quadratic suppression) vs the uncorrected O(p).
G3  9-qubit Shor code corrects an ARBITRARY single-qubit error (every X,Y,Z on
    every one of the 9 qubits) with fidelity 1 to <1e-12.
G4  correction beats no-correction (pseudo-threshold): F_corr > F_uncorr for all
    tested p, across bit-flip and phase-flip codes.
G5  live in the engine: error_correction channel holds a logical qubit against
    repeated noise rounds (corrected fidelity stays high while the uncorrected
    control decays); checkpoint mid-run resumes bit-identical.
"""
import os, sys, json, tempfile
import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import casim  # noqa: F401
from casim.engine.interactions import qi_entanglement as E
from casim.engine.interactions import qi_noise as N
from casim.engine import Simulation, LatticeSpec, build_channel, build_observer

N._E = E   # ensure the native-gate kernel handle is set
RESULTS = {'finding': 'F221', 'date': '2026-07-01',
           'title': 'Noise channels + error correction', 'tests': {}}
A, B = float(np.cos(0.7)), float(np.sin(0.7))


def test_G1_channels_cptp():
    checks = {}
    for name, kr in [('bitflip', N.kraus_bitflip(0.3)),
                     ('phaseflip', N.kraus_phaseflip(0.3)),
                     ('depolarizing', N.kraus_depolarizing(0.3)),
                     ('amp_damp', N.kraus_amp_damp(0.3))]:
        S = sum(Ek.conj().T @ Ek for Ek in kr)
        checks[name] = float(np.max(np.abs(S - np.eye(2))))
        assert checks[name] < 1e-12
    # density matrix stays physical after a channel
    psi = N.encode_bitflip(A, B); rho = N.apply_channel_all(N.density(psi),
                                                            N.kraus_depolarizing(0.2), 3)
    herm = float(np.max(np.abs(rho - rho.conj().T)))
    tr = float(np.real(np.trace(rho)))
    ev = np.linalg.eigvalsh(rho).real.min()
    assert herm < 1e-12 and abs(tr - 1) < 1e-12 and ev > -1e-12
    RESULTS['tests']['G1_cptp'] = {'sum_EdaggerE_err': checks, 'herm': herm,
                                   'trace': tr, 'min_eig': float(ev)}
    print(f'G1 channels CPTP: PASS  Σ E†E=I to {max(checks.values()):.1e}, ρ physical')


def test_G2_bitflip_exact_and_quadratic():
    psiL = N.encode_bitflip(A, B); rho0 = N.density(psiL)
    res, worst = {}, 0.0
    for p in [0.05, 0.1, 0.2, 0.3, 0.5]:
        rho = N.apply_channel_all(rho0.copy(), N.kraus_bitflip(p), 3)
        Fc = N.fidelity(N.recover_bitflip(rho), psiL)
        Fan = N.bitflip_corrected_fidelity(p, A, B)
        worst = max(worst, abs(Fc - Fan))
        res[p] = {'F_corr': Fc, 'F_analytic': Fan, 'F_uncorr': N.fidelity(rho, psiL)}
    assert worst < 1e-12, worst
    # quadratic suppression: 1−F_corr ∝ p² (ratio ~const at small p)
    ratios = [(1 - N.bitflip_corrected_fidelity(p, A, B)) / p ** 2
              for p in (0.001, 0.002, 0.004)]
    assert max(ratios) - min(ratios) < 1e-3      # ratio → const ⇒ 1−F = O(p²)
    RESULTS['tests']['G2_bitflip'] = {'worst_err': worst, 'infidelity_over_p2': ratios,
                                      'curve': res}
    print(f'G2 bit-flip code exact + O(p²): PASS  analytic match {worst:.1e}, '
          f'1−F∝p² ratio≈{np.mean(ratios):.3f}')


def test_G3_shor_arbitrary_single_error():
    psiS = N.encode_shor(A, B); rho0 = N.density(psiS)
    worst = 0.0
    for pauli, nm in [(N.X, 'X'), (N.Y, 'Y'), (N.Z, 'Z')]:
        for q in range(9):
            Ef = N.embed(pauli, q, 9)
            rho_rec = N.recover_shor(Ef @ rho0 @ Ef.conj().T)
            worst = max(worst, abs(1 - N.fidelity(rho_rec, psiS)))
    assert worst < 1e-12, worst
    RESULTS['tests']['G3_shor'] = {'worst_infidelity': worst,
                                   'errors_tested': '27 (X,Y,Z × 9 qubits)'}
    print(f'G3 Shor arbitrary single-error: PASS  all 27 corrected, worst 1−F={worst:.1e}')


def test_G4_pseudothreshold():
    res = {}
    for code, noise, enc in [('bitflip', N.kraus_bitflip, N.encode_bitflip),
                             ('phaseflip', N.kraus_phaseflip, N.encode_phaseflip)]:
        psiL = enc(A, B); rho0 = N.density(psiL)
        rec = N.recover_bitflip if code == 'bitflip' else N.recover_phaseflip
        row = {}
        for p in [0.05, 0.1, 0.2, 0.3]:
            rho = N.apply_channel_all(rho0.copy(), noise(p), 3)
            Fu = N.fidelity(rho, psiL); Fc = N.fidelity(rec(rho), psiL)
            assert Fc > Fu, (code, p, Fu, Fc)
            row[p] = {'F_uncorr': Fu, 'F_corr': Fc}
        res[code] = row
    RESULTS['tests']['G4_pseudothreshold'] = res
    print(f'G4 correction beats no-correction: PASS  F_corr>F_uncorr for '
          f'bit-flip & phase-flip codes')


def test_G5_live_engine_and_checkpoint():
    def fresh(correct):
        ch = build_channel({'type': 'error_correction', 'code': 'bitflip',
                            'noise': 'bitflip', 'p': 0.1, 'correct': correct})
        obs = build_observer({'type': 'error_correction_fidelity', 'every': 1})
        return Simulation(LatticeSpec(L=6, dims=3, topology='cubic'), [ch], [obs],
                          name='qec')
    rounds = 8
    sc = fresh(True); s_corr = sc.run(rounds)['observers']['error_correction_fidelity']['summary']
    su = fresh(False); s_unc = su.run(rounds)['observers']['error_correction_fidelity']['summary']
    # corrected qubit stays near-perfect; uncorrected decays well below it
    assert s_corr['F_final'] > 0.99 and s_unc['F_final'] < s_corr['F_final'] - 0.3
    # trace preserved
    cn = list(sc.channels)[0]
    assert abs(np.real(np.trace(sc.states[cn]['rho'])) - 1) < 1e-12

    # checkpoint mid-run bit-identical
    A2 = fresh(True); A2.step(3)
    with tempfile.TemporaryDirectory() as d:
        p = A2.checkpoint(os.path.join(d, 'c.npz'))
        R = Simulation.resume(p); R.step(rounds - 3)
    Bs = fresh(True); Bs.step(rounds)
    cnb = list(Bs.channels)[0]
    err = float(np.max(np.abs(R.states[cnb]['rho'] - Bs.states[cnb]['rho'])))
    assert err == 0.0, err
    RESULTS['tests']['G5_live_engine'] = {
        'F_corr_final': s_corr['F_final'], 'F_uncorr_final': s_unc['F_final'],
        'rounds': rounds, 'checkpoint_err': err}
    print(f'G5 live in engine: PASS  corrected F={s_corr["F_final"]:.4f} vs '
          f'uncorrected F={s_unc["F_final"]:.4f} over {rounds} rounds, checkpoint exact')


def main():
    print('=' * 70)
    print('F221 — noise channels + stabilizer error correction')
    print('=' * 70)
    test_G1_channels_cptp()
    test_G2_bitflip_exact_and_quadratic()
    test_G3_shor_arbitrary_single_error()
    test_G4_pseudothreshold()
    test_G5_live_engine_and_checkpoint()
    print('=' * 70)
    print('ALL PASS — the engine has noise + error correction; codes suppress errors.')
    out = os.path.join(ROOT, 'test-results', 'F221_noise_error_correction.json')
    with open(out, 'w') as f:
        json.dump(RESULTS, f, indent=2)
    print(f'Results → {out}')


if __name__ == '__main__':
    main()
