#!/usr/bin/env python3
"""
run_kns_seagull.py — NATIVE driver for the full Kawai-Nakayama-Seo quartic
expansion: the Wilson 4-gluon seagull (tadpole) + Haar measure contributions to
the gluon self-energy, the last piece needed to close Lambda_MSbar/Lambda_L =
28.8086 (F163). EXCEEDS the 45 s sandbox compute cap -> run on the host.

STATUS / WHY NATIVE
===================
The symbolic quartic expansion (sympy, SU(2) plaquette to O(field^4) with the
two-mode background+fluctuation phase structure) is VALIDATED at quadratic order
(the t^2 term reproduces the lattice field strength exactly:
  S2 = (1/8)(D0 A1 - D1 A0)^2,  D_mu = e^{i q_mu}-1,  |D_mu|^2 = 4 sin^2(q_mu/2),
so the propagator kernel is Khat = sum khat_mu^2 -- machine-confirmed).
The QUARTIC (seagull) term is the same computation one order higher; it is just
too heavy for the 45 s sandbox (the truncated product of four order-4 matrix
exponentials with 13 symbols times out). Natively it completes.

THE COMPUTATION (two interchangeable routes; this runner does the NUMERICAL one)
================================================================================
SEAGULL is a CONTACT term: both quantum legs attach to one vertex, so its loop
sum is a lattice tadpole integral dominated by Z0 = int 1/Khat = 0.1549334 (plus
int cos(k_r)/Khat). This is the physical origin of "28.81 is tadpole-dominated".

  Pi^tad_{mn}(p) = (1/2) sum_{loop pol r, colour a} int_k (1/Khat(k))
                     W_{mn,r a}(p,k),
  W = the s^2 t^2 coefficient of S[s*B + t*phi] (B=background mom p dir m;
      phi=fluctuation mom k dir r colour a), extracted by 2D finite differences
      of the VALIDATED SU(2) action ca_lpt_vertex.wilson_action.

NORMALISATION: fixed by the quadratic. The action's free fluctuation operator is
  M0(k, e_transverse) = d^2 S/d(amp)^2 = N_act * Khat(k) * |e|^2,
so N_act is read off once; the physical (Feynman-gauge) propagator is 1/Khat, and
the seagull is rescaled by 1/N_act to the loop convention. The MEASURE term
(SU(N) Haar Jacobian) adds a constant delta_{mn}: S_meas = (g^2/12) C_A sum A^2
(leading), contributing Pi^meas_{mn} = delta_{mn} (g^2/12) C_A in the same units.

VALIDATION GATE (do NOT trust the number until this passes): loops + seagull +
measure must be TRANSVERSE -- qhat_m Pi^total_{mn} = 0 -- for p != 0. This is the
gauge-invariance check that fixes the seagull normalisation AND the measure
coefficient together. Only then read Lambda = exp((C_lat - C_MSbar)/2),
C_MSbar = 131/66 (analytic, ca_lpt_wilson_selfenergy.continuum_msbar_constant).
Target: SU(3) 28.8086 (use C_A=3 colour factor); the SU(2) action gives the
kinematic structure, colour rescaled C_A: 2->3.

Usage:
    python3 tests/runners/run_kns_seagull.py --L 8 --nk 60 --out test-results/F163_kns_seagull.json

This runner currently implements the seagull EXTRACTOR + normalisation + the
transversality gate scaffold. The honest status (2026-06-19): the extractor and
the quadratic normalisation are in place; the full transversality-validated
assembly is the remaining native computation. See findings/F163.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ca-simulation"))

import ca_lpt_vertex as lv          # validated SU(2) wilson_action  # noqa: E402


def _mode(L, n_vec, pol, color, d=4):
    """real plane-wave field A[mu][x][a] = pol_mu delta(a,color) cos(k.x)."""
    return lv.plane_mode(L, n_vec, pol, color, d=d)


def free_operator_norm(L=8, g=0.4, n_vec=(1, 0, 0, 0)):
    """N_act from M0 = d^2S/d amp^2 = N_act * Khat * |e|^2 (transverse e)."""
    pol = lv._transverse_pol(n_vec, L)
    eps = 1e-3
    Ap = _mode(L, n_vec, pol * eps, 0)
    Am = _mode(L, n_vec, -pol * eps, 0)
    c2 = (lv.wilson_action(Ap, g) + lv.wilson_action(Am, g)) / eps ** 2  # 2nd deriv*2
    kh = lv.khat(n_vec, L)
    return c2 / kh    # = N_act (per |e|^2=1), to be divided out


def seagull_integrand(L, g, p_vec, k_vec, mB=1):
    """W(p,k) = sum_{r,a} (s^2 t^2 coeff of S[s B + t phi]) for background B in
    direction mB (transverse pol), fluctuation phi mom k summed over dir r and
    colour a. 2D finite-difference (3x3 stencil)."""
    # background: transverse polarization in plane perp to p, with a component on mB
    eB = np.zeros(4); eB[mB] = 1.0
    # project out p direction (keep transverse)
    ph = np.array([2 * math.sin(math.pi * n / L) for n in p_vec])
    if np.dot(ph, ph) > 0:
        eB = eB - np.dot(eB, ph) / np.dot(ph, ph) * ph
    nrm = np.linalg.norm(eB)
    if nrm < 1e-9:
        return 0.0
    eB = eB / nrm
    hs, ht = 0.04, 0.04
    W = 0.0
    for r in range(4):
        er = np.zeros(4); er[r] = 1.0
        for a in range(3):
            acc = 0.0
            for si, sc in ((-1, 1), (0, -2), (1, 1)):      # 2nd deriv in s (background)
                for ti, tc in ((-1, 1), (0, -2), (1, 1)):  # 2nd deriv in t (fluct)
                    B = _mode(L, p_vec, eB * (si * hs), 2)          # bg colour 3
                    F = _mode(L, k_vec, er * (ti * ht), a)
                    A = [B[mu] + F[mu] for mu in range(4)]
                    acc += sc * tc * lv.wilson_action(A, g)
            W += acc / (hs ** 2 * ht ** 2)
    return W


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, default=8)
    ap.add_argument("--g", type=float, default=0.4)
    ap.add_argument("--nk", type=int, default=40)
    ap.add_argument("--out", type=str, default="test-results/F163_kns_seagull.json")
    args = ap.parse_args()

    Nact = free_operator_norm(args.L, args.g)
    # sample seagull integrand over random loop momenta at a fixed transverse p
    p_vec = (2, 0, 0, 0)
    rng = np.random.default_rng(0)
    rows = []
    sea = 0.0
    cnt = 0
    for _ in range(args.nk):
        n = tuple(int(x) for x in rng.integers(0, args.L, size=4))
        if all(v == 0 for v in n):
            continue
        kh2 = lv.khat(n, args.L)
        if kh2 < 1e-6:
            continue
        W = seagull_integrand(args.L, args.g, p_vec, n, mB=1)
        sea += 0.5 * W / kh2
        cnt += 1
        rows.append({"k": n, "Khat": kh2, "W": W})
    sea = sea / cnt * (args.L ** 4)        # BZ-average -> integral normalisation
    res = {"N_act": Nact, "p_vec": p_vec, "n_samples": cnt,
           "seagull_raw": sea,
           "note": "raw seagull (action normalisation). Divide by N_act, add "
                   "measure (g^2/12)C_A, rescale colour 2->3, then VALIDATE "
                   "transversality before combining with loops + C_MSbar=131/66. "
                   "This runner provides the extractor + normalisation; the "
                   "transversality-validated assembly is the remaining native step.",
           "sample_rows": rows[:10]}
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(res, f, indent=2, default=float)
    print(json.dumps(res, indent=2, default=float))


if __name__ == "__main__":
    main()
