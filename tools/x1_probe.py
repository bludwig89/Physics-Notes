#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
x1_probe.py — reproduction script for docs/status/x1-colour-normalisation-fork-2026-08-18.md

Standalone (numpy only, no casim import) so that every number in the X1 report
can be checked without the repo on the path.  Three blocks:

  A.  The C7 matching under its three possible readings.  The C_F that creates
      the X1 fork appears ONLY in the mixed reading (abelian rotor eigenvalue
      in the numerator, SU(N) gauge eigenvalue in the denominator).  Both
      self-consistent readings give chi = 1/(4 g^2) exactly, for every N and
      every irrep.  Exact over Q.

  B.  F299's 2D SU(3) Weyl-torus quadrature, reimplemented from scratch, run at
      beta = 24 (branch B's coupling), beta = 32 (branch A's coupling) and
      beta = 96.  Casimir scaling is beta-independent, so the "discriminator"
      returns the same answer under both branches.

  C.  F280's tadpole-free band, rebuilt from the committed anchors, with each
      branch's requirement placed on it.  Branch A sits 5.63 decades above the
      band top.

Usage:  python3 x1_probe.py
"""
from fractions import Fraction as F
import math

import numpy as np

# =====================================================================
# A.  The C7 matching under three readings
# =====================================================================
N_LINKS = 4                 # BCC 4-bond rhombus / square plaquette (F265, F303 4.2)
G2 = F(1, 4)                # so the abelian answer is chi = 1


def casimir(rows, N):
    """C_2 of the SU(N) irrep with Young rows `rows`, normalised C_2(fund)=(N^2-1)/2N."""
    lam = list(rows) + [0] * (N - len(rows))
    tot = sum(lam)
    s = sum(F(l) * (l + N + 1 - 2 * (i + 1)) for i, l in enumerate(lam))
    return F(1, 2) * (s - F(tot * tot, N))


def C_F(N):
    return F(N * N - 1, 2 * N)


def sym_residue_sq(k, N):
    """s(k)^2, the rotor level link_hamiltonian.sym_residue assigns to flux k."""
    r = ((k + N // 2) % N) - N // 2
    return r * r


def chi(rotor_eig, gauge_eig):
    """(g^2/2) * n_links * gauge = (1/2 chi) * rotor   =>   chi = rotor/(g^2 n gauge)."""
    return F(rotor_eig) / (G2 * N_LINKS * F(gauge_eig))


def irreps(N, maxbox=5):
    """All Young diagrams with <= N-1 rows and <= maxbox boxes."""
    out = []

    def rec(rows, remaining):
        if rows:
            out.append(tuple(rows))
        if len(rows) >= N - 1:
            return
        start = rows[-1] if rows else maxbox
        for l in range(min(start, remaining), 0, -1):
            rec(rows + [l], remaining - l)

    rec([], maxbox)
    return out


def block_A():
    print("=" * 78)
    print("A.  THE C7 MATCHING, THREE READINGS  (k-string tower, g^2 = 1/4)")
    print("=" * 78)
    print(f"{'N':>3} | {'both abelian (F294)':>20} | {'MIXED (F298)':>28} | {'both SU(N)':>12}")
    print("-" * 78)
    for N in (2, 3, 4, 5, 6, 7):
        ab, mx, na = set(), set(), set()
        for k in range(1, N):
            s2, c2 = sym_residue_sq(k, N), casimir([1] * k, N)
            if s2:
                ab.add(chi(s2, s2))
                mx.add(chi(s2, c2))
            na.add(chi(c2, c2))
        f = (lambda s: str(sorted(s)[0]) if len(s) == 1
             else "level-dep " + ",".join(map(str, sorted(s))))
        print(f"{N:>3} | {f(ab):>20} | {f(mx):>28} | {f(na):>12}")
    print()
    print("  MIXED reproduces F298: 1/C_F at N<=3 (4/3, 3/4), level-dependent for N>=4.")
    print("  Both self-consistent readings are 1 = 1/(4 g^2) everywhere.")
    print()
    print("  Full-irrep scan of the consistent SU(N) reading:")
    for N in (2, 3, 4, 5, 6, 7):
        vals, n = set(), 0
        for rows in irreps(N):
            c2 = casimir(rows, N)
            if c2 == 0:
                continue
            vals.add(chi(c2, c2))
            n += 1
        print(f"    SU({N}): {n:>3} irreps -> chi in {sorted(vals)}  "
              f"level-independent: {len(vals) == 1}")
    print("  => no C_F, and NO N_c <= 3 restriction: CN19 is a property of the mixed reading.")
    print()


# =====================================================================
# B.  F299's engine, reimplemented, at both branches' couplings
# =====================================================================
REPS = {  # label: (Young rows, dim, C_2)
    '3':   ((1, 0, 0), 3, F(4, 3)),
    '3bar': ((1, 1, 0), 3, F(4, 3)),
    '6':   ((2, 0, 0), 6, F(10, 3)),
    '8':   ((2, 1, 0), 8, F(3)),
    '10':  ((3, 0, 0), 10, F(6)),
    '15':  ((3, 1, 0), 15, F(16, 3)),
    "15'": ((4, 0, 0), 15, F(28, 3)),
    '27':  ((4, 2, 0), 27, F(8)),
}
CENTRE = {'3': 1, '3bar': 1, '6': 1, '8': 0, '10': 0, '15': 1, "15'": 1, '27': 0}


def _h(z, kmax):
    """Complete homogeneous symmetric polynomials h_0..h_kmax in 3 variables."""
    e1 = z[0] + z[1] + z[2]
    e2 = z[0] * z[1] + z[0] * z[2] + z[1] * z[2]
    e3 = z[0] * z[1] * z[2]
    h = [np.ones_like(e1)]
    for k in range(1, kmax + 1):
        v = e1 * h[k - 1]
        if k >= 2:
            v = v - e2 * h[k - 2]
        if k >= 3:
            v = v + e3 * h[k - 3]
        h.append(v)
    return h


def schur(z, lam, kmax=14):
    """Division-free Jacobi-Trudi: no 0/0 at degenerate torus points."""
    h = _h(z, kmax)
    zero = np.zeros_like(h[0])

    def H(i):
        return zero if i < 0 else h[i]

    M = [[H(lam[i] - (i + 1) + (j + 1)) for j in range(3)] for i in range(3)]
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def sigmas(beta, n=240, N=3):
    phi = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    P1, P2 = np.meshgrid(phi, phi, indexing='ij')
    P3 = -(P1 + P2)
    z = (np.exp(1j * P1), np.exp(1j * P2), np.exp(1j * P3))
    meas = (2 * (1 - np.cos(P1 - P2))
            * 2 * (1 - np.cos(P1 - P3))
            * 2 * (1 - np.cos(P2 - P3)))
    wt = np.exp((beta / N) * np.real(z[0] + z[1] + z[2])) * meas
    Z = wt.sum()
    return {k: -np.log(np.real((schur(z, lam) / d * wt).sum() / Z))
            for k, (lam, d, _c2) in REPS.items()}


def block_B():
    print("=" * 78)
    print("B.  F299's ENGINE AT BOTH BRANCHES' COUPLINGS")
    print("=" * 78)
    for beta, tag in ((24.0, "branch B, g_s = 1/2"),
                      (32.0, "branch A, g_s = sqrt3/4"),
                      (96.0, "continuum-ward")):
        s = sigmas(beta)
        base = s['3']
        print(f"  beta = {beta:5.1f}   ({tag})")
        for k, (_lam, _d, c2) in REPS.items():
            law = float(c2 / F(4, 3))
            print(f"     {k:>4}: sigma_R/sigma_3 = {s[k]/base:8.5f}   "
                  f"Casimir = {law:7.4f} ({100*(s[k]/base/law-1):+6.2f}%)   "
                  f"centre = {CENTRE[k]}")
        print()
    print("  sigma_6/sigma_3 is the SAME under both branches (2.49115 vs 2.49540):")
    print("  Casimir scaling in 2D is a theorem about the SU(3) Wilson measure at")
    print("  weak coupling, true at every beta, so it carries no information about")
    print("  which beta the rule fixes.  F299 measures link REPRESENTATION CONTENT.")
    print()


# =====================================================================
# C.  F280's band, and where each branch lands on it
# =====================================================================
LAMBDA_W = 28.8086      # Kawai-Nakayama-Seo, SU(3) pure gauge
C_LAT_LOOPS = 6.138643  # F163
C_MSBAR = 131 / 66      # F163, analytic dim reg
MU0 = 1.850e18          # F107
MZ = 91.1876
PDG = 0.1180


def b0(nf):
    return (33.0 - 2.0 * nf) / (12.0 * math.pi)


def block_C():
    print("=" * 78)
    print("C.  F280's TADPOLE-FREE BAND, AND THE TWO BRANCHES ON IT")
    print("=" * 78)
    dC_W = 2 * math.log(LAMBDA_W)
    dC_W_loops = C_LAT_LOOPS - C_MSBAR
    T_W = dC_W - dC_W_loops
    top = math.exp(dC_W_loops / 2)
    print(f"  dC_W            = {dC_W:.6f}   (2 ln 28.8086)")
    print(f"  dC_W^loops      = {dC_W_loops:.6f}")
    print(f"  T_W (seagull+Haar) = {T_W:.6f}   [F280 leg 1 published -2.5676]")
    print(f"  band            = [1, {top:.4f}]   [F280 S5 published [1, 7.980]]")
    print()
    print(f"  {'':<26}{'Lambda':>12} {'dC_rule^loops':>15} {'x Wilson loops':>15}  position")
    for name, L in (("branch B (no C_F)", 1.773444),
                    ("Wilson action", LAMBDA_W),
                    ("branch A (Casimir)", 3.4e6)):
        dC = 2 * math.log(L)
        pos = ("inside, at %.1f%%" % (100 * (L - 1) / (top - 1)) if L <= top
               else "ABOVE top by %.4gx = %.2f decades"
                    % (L / top, math.log10(L / top)))
        print(f"  {name:<26}{L:>12.6g} {dC:>15.4f} {dC/dC_W_loops:>15.3f}  {pos}")
    print()
    d_inv = 16 * math.pi * (4 / 3 - 1)
    print(f"  branch A's requirement, derived: 16 pi (C_F - 1) = {d_inv:.4f} in 1/alpha")
    print(f"    -> Lambda ratio exp(d/(2 b0(nf=6))) = {math.exp(d_inv/(2*b0(6))):.4g}")
    print()
    print("  Every value the d1 apparatus has ever returned: 1.633, ~2.06-2.08, 2.135,")
    print("  14.27 (non-converged).  None within 5 decades of branch A.")
    print()

    # running, for the alpha_s numbers quoted in the report
    def down(a, hi, lo, nf):
        return 1.0 / (1.0 / a - 2.0 * b0(nf) * math.log(hi / lo))

    def up(a, lo, hi, nf):
        return 1.0 / (1.0 / a + 2.0 * b0(nf) * math.log(hi / lo))

    print("  one-loop running mu0 -> M_Z:")
    for name, g2 in (("branch B (g_s=1/2)      ", F(1, 4)),
                     ("branch A (g_s=sqrt3/4)  ", F(1, 4) / C_F(3))):
        a0 = float(g2) / (4 * math.pi)
        a = down(down(a0, MU0, 172.69, 6), 172.69, MZ, 5)
        print(f"    {name}: alpha_0={a0:.8f}  1/a0={1/a0:8.4f}  "
              f"alpha_s(M_Z)={a:.5f} ({100*(a/PDG-1):+.2f}% vs PDG)")
    a_req = up(up(PDG, MZ, 172.69, 5), 172.69, MU0, 6)
    print(f"    alpha_0 demanded by PDG: {a_req:.8f}  "
          f"(F298 publishes 0.0198779; branch B deviates by "
          f"{100*(float(F(1,4))/(4*math.pi)/a_req-1):+.3f}%)")
    print()


if __name__ == "__main__":
    block_A()
    block_B()
    block_C()
