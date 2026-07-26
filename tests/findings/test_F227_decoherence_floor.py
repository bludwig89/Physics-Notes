#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F227 — Route 4: intrinsic-decoherence / unitarity floor from discreteness
==========================================================================
Date: 2026-07-02

Does a long quantum computation on the lattice show any intrinsic departure from
perfect unitarity (a minimum decoherence rate, a maximum entangling velocity, a
gate-error floor) set by a and c_lat?  The expected honest answer is ZERO or
Planck-suppressed, below all current bounds.

Pass gates
----------
G1  intrinsic unitarity floor is zero / Planck-suppressed: the LIV-suppressed
    rate Γ ≲ E³/(ħ E_lat²) (F130 n≥2 irrelevance) is astronomically small for an
    optical-scale qubit; the effective-theory floor is exactly 0 (unitary gates).
G2  Lieb–Robinson: the fundamental signalling speed = c_lat = 1/√3 EXACTLY
    (dispersion slope dΩ/d|k|, F26/F105/F180) to machine precision.
G3  strict causal cone in the QC sector: nearest-neighbour native exchange gates
    give a HARD Lieb–Robinson cone — the connected correlation is EXACTLY zero
    (<1e-12) strictly outside r=2t; no instantaneous propagation.
G4  confront experiment: the predicted floor sits below the measured atomic-clock
    and transmon decoherence (conservative ceiling ≥9 orders below) and below the
    CSL/GRW collapse rate (model rate ≥20 orders below); model is unitary, no
    objective collapse ⇒ Route does NOT yield a near-term test.
G5  the one non-Planck channel — emergent doublon leakage (2t/U)² (F220/F225) —
    is separated from the fundamental floor by ≥20 orders (distinct physics).
"""
import os, sys, json, math
import numpy as np

THIS = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(THIS, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'ca-simulation'))
import ca_decoherence_floor as D

RES = {'finding': 'F227', 'date': '2026-07-02',
       'title': 'Intrinsic-decoherence / unitarity floor (Route 4)', 'tests': {}}


def g1_intrinsic_floor():
    E = 1.8
    liv = D.intrinsic_rate_liv(E)
    cons = D.intrinsic_rate_conservative(E)
    floor0 = D.unitary_floor_is_zero()
    ok = liv < 1e-30 and cons < 1e-6 and floor0['effective_theory_floor'] == 0.0
    RES['tests']['G1_intrinsic_floor'] = {
        'E_eV': E, 'gamma_liv_s^-1': liv, 'gamma_conservative_s^-1': cons,
        'effective_theory_floor': floor0['effective_theory_floor'],
        'E_lat_eV': D.E_LAT_EV, 'pass': bool(ok)}
    return ok


def g2_lieb_robinson_speed():
    slope = D.fundamental_dispersion_slope()
    resid = abs(slope - D.C_LAT)
    ok = resid < 1e-12
    RES['tests']['G2_lieb_robinson_speed'] = {
        'dispersion_slope_dOmega_dk': slope, 'c_lat': D.C_LAT,
        'residual': resid, 'source': 'F26/F105/F180 exact on-axis Ω=|k|/√3',
        'pass': bool(ok)}
    return ok


def g3_strict_causal_cone():
    times, fronts, outside = D.exchange_chain_lightcone(nqubits=9, nlayers=3)
    # front must never exceed the 2t cone bound
    within = all(f <= cone for (f, cone) in [fr for fr in fronts])
    ok = outside < 1e-12 and within
    RES['tests']['G3_strict_causal_cone'] = {
        'times': times, 'front_and_cone_2t': fronts,
        'max_correlation_outside_cone': outside,
        'front_within_cone': within, 'pass': bool(ok)}
    return ok


def g4_confront_experiment():
    c = D.confront_experiment(1.8)
    ok = (c['conservative_orders_below_clock'] > 9 and
          c['conservative_orders_below_transmon'] > 12 and
          c['liv_orders_below_CSL_GRW'] > 20)
    RES['tests']['G4_confront_experiment'] = {**c, 'pass': bool(ok)}
    return ok


def g5_leakage_separation():
    s = D.floor_vs_leakage_separation(E_eV=1.8, tU=0.018)
    ok = s['separation_orders'] > 20 and s['doublon_leakage_per_gate'] > 1e-4
    RES['tests']['G5_leakage_separation'] = {**s, 'pass': bool(ok)}
    return ok


def main():
    gates = [g1_intrinsic_floor(), g2_lieb_robinson_speed(), g3_strict_causal_cone(),
             g4_confront_experiment(), g5_leakage_separation()]
    npass = sum(gates)
    RES['summary'] = {'passed': npass, 'total': len(gates), 'all_pass': npass == len(gates)}
    out = os.path.join(ROOT, 'test-results', 'F227_decoherence_floor.json')
    with open(out, 'w') as f:
        json.dump(RES, f, indent=2, default=lambda o: float(o) if hasattr(o, 'dtype') else str(o))
    print(f"F227 decoherence floor: {npass}/{len(gates)} PASS")
    for k, v in RES['tests'].items():
        print(f"  {k}: {'PASS' if v['pass'] else 'FAIL'}")
    print("verdict: no intrinsic floor (unitary; Planck-suppressed) ⇒ Route 4 gives no near-term test")
    print(f"results → {out}")
    assert npass == len(gates), "F227 gate(s) failed"


def test_F227_all():
    """pytest entrypoint — runs all gates and asserts 5/5."""
    main()


if __name__ == '__main__':
    main()
