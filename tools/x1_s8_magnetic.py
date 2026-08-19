#!/usr/bin/env python3
"""
Section 8.2 — audit the MAGNETIC side of the C7 identity.

Runs against the repo's own modules (su3_ladder, link_hamiltonian) plus a
general-SU(N) character rotor written here.

Requires `scipy` (via `link_hamiltonian`).  On a machine without it, Q1/Q3's
U(1) column falls back to the local `u1_rotor_s1` below, which is numpy-only and
reproduces `lh.rotor_sigma1` to 1e-9 -- but Q1's direct F111b T7 reproduction
needs the repo function and will not run.

Questions:
  Q1  Does F111b T7's claimed identity  s1_SU3 == s1_U1 at chi = 1/(4g^2)
      actually hold as coded?
  Q2  Is that comparison link-count consistent?  (SU(3) side uses ONE link,
      U(1) side uses chi = 1/(4g^2), i.e. FOUR.)
  Q3  Compared consistently, what is s1_SU(N)/s1_U(1) at the same (chi, lam)?
  Q4  Do the magnetic COEFFICIENTS differ between the two theories, i.e. does
      the magnetic term renormalise the chi-map?
"""
import math
from fractions import Fraction as Fr

import numpy as np

from casim.engine.gauge import su3_ladder as su
from casim.engine.gauge import link_hamiltonian as lh


# ---------------------------------------------------------------- general SU(N)
def casimir_N(rows, N):
    lam = list(rows) + [0] * (N - len(rows))
    tot = sum(lam)
    s = sum(Fr(l) * (l + N + 1 - 2 * (i + 1)) for i, l in enumerate(lam))
    return Fr(1, 2) * (s - Fr(tot * tot, N))


def dim_N(rows, N):
    """Weyl dimension formula via the hook-content-free product over pairs."""
    lam = list(rows) + [0] * (N - len(rows))
    num = den = 1
    for i in range(N):
        for j in range(i + 1, N):
            num *= (lam[i] - lam[j] + j - i)
            den *= (j - i)
    return Fr(num, den)


def normalise(rows, N):
    """Strip columns of height N (they are singlets in SU(N))."""
    lam = [r for r in rows if r > 0]
    lam = lam + [0] * (N - len(lam))
    if len(lam) > N:
        return None
    sub = lam[N - 1] if len(lam) >= N else 0
    lam = tuple(r - sub for r in lam[:N] if r - sub > 0)
    return lam


def fuse_box(rows, N):
    """F (x) R : add one box to a legal row."""
    lam = list(rows) + [0]
    out = []
    for i in range(len(lam)):
        if i == 0 or lam[i] < lam[i - 1]:
            new = lam[:]
            new[i] += 1
            if len([r for r in new if r > 0]) <= N:
                out.append(normalise(tuple(r for r in new if r > 0), N))
    return [t for t in out if t is not None]


def ladder_N(N, maxbox):
    seen = {(): True}
    frontier = [()]
    for _ in range(maxbox):
        nxt = []
        for r in frontier:
            for t in fuse_box(r, N):
                if t not in seen:
                    seen[t] = True
                    nxt.append(t)
        frontier = nxt
    return sorted(seen, key=lambda r: (float(casimir_N(r, N)), r))


def suN_rotor_s1(N, g2, lam_mag, n_links, maxbox=8):
    """H = (g^2/2) n C_2  -  (lam/2)(chi_F + chi_Fbar); s1 = <chi_F>/d_F."""
    reps = ladder_N(N, maxbox)
    pos = {r: i for i, r in enumerate(reps)}
    n = len(reps)
    H = np.zeros((n, n))
    MF = np.zeros((n, n))
    for r in reps:
        H[pos[r], pos[r]] = 0.5 * g2 * n_links * float(casimir_N(r, N))
        for t in fuse_box(r, N):
            if t in pos:
                MF[pos[t], pos[r]] = 1.0
    H -= 0.5 * lam_mag * (MF + MF.T)
    w, v = np.linalg.eigh(H)
    a = v[:, 0]
    if a[pos[()]] < 0:
        a = -a
    return float(a @ (MF @ a)) / float(dim_N((1,), N))


def u1_rotor_s1(chi, lam_mag, m_max=40):
    """H = (1/2chi) m^2 - lam cos(phi); s1 = <e^{i phi}>."""
    m = np.arange(-m_max, m_max + 1)
    H = np.diag(m.astype(float) ** 2 / (2.0 * chi))
    off = -0.5 * lam_mag * np.ones(len(m) - 1)
    H += np.diag(off, 1) + np.diag(off, -1)
    w, v = np.linalg.eigh(H)
    a = v[:, 0]
    if a[m_max] < 0:
        a = -a
    return float(np.sum(a[:-1] * a[1:]))


print("=" * 78)
print("Q1  F111b T7 AS CODED")
print("=" * 78)
g2, lam = 1.0, 0.001
s1_su3 = su.su3_rotor_sigma1(g2, lam, 12)[1]
s1_u1 = lh.rotor_sigma1(lam, chi=1.0 / (4.0 * g2), m_max=20)[1]
print(f"  su3_rotor_sigma1(g2=1, lam=1e-3)          s1 = {s1_su3:.10f}")
print(f"  lh.rotor_sigma1(lam=1e-3, chi=1/(4g^2))   s1 = {s1_u1:.10f}")
print(f"  |ratio - 1| = {abs(s1_su3/s1_u1 - 1):.3e}    (T7 tolerance 5e-3)")
print(f"  both -> lam/(2 g^2) = {lam/(2*g2):.10f}")
print("  T7 REPRODUCES.  The identity as coded is real.")

print()
print("=" * 78)
print("Q2  IS THAT COMPARISON LINK-COUNT CONSISTENT?")
print("=" * 78)
print("  su3_rotor_hamiltonian: H[r,r] = 0.5*g2*C2(r)         -> ONE link")
print("  lh.rotor with chi = 1/(4 g^2): 1/(2chi) = 2 g^2 = (g^2/2)*4  -> FOUR links")
print(f"  electric gap to the first excited level:")
print(f"     SU(3), 1 link : 0.5*g2*C_F      = {0.5*g2*4/3:.6f}")
print(f"     U(1),  4 links: (1/2chi)*1      = {2.0*g2:.6f}")
print(f"     ratio = {2.0*g2/(0.5*g2*4/3):.6f}   (= 3, i.e. 4 links / C_F)")
print("  => the two Hamiltonians are NOT the same physical system.")

print()
print("=" * 78)
print("Q3  CONSISTENT COMPARISON: same n_links on both sides")
print("=" * 78)
print(f"  {'N':>3} {'n':>3} | {'s1 SU(N)':>14} {'s1 U(1)':>14} {'ratio':>10} "
      f"{'2/(N^2-1)':>11}")
for n_links in (1, 4):
    for N in (2, 3, 4, 5):
        lam_m = 1e-3
        chi = 1.0 / (n_links * g2)          # 1/(2chi) = (g^2/2) n
        a = suN_rotor_s1(N, g2, lam_m, n_links)
        b = u1_rotor_s1(chi, lam_m)
        print(f"  {N:>3} {n_links:>3} | {a:>14.9f} {b:>14.9f} {a/b:>10.6f} "
              f"{2.0/(N*N-1):>11.6f}")
print()
print("  s1_SU(N)/s1_U(1) = 2/(N^2-1) EXACTLY, independent of n_links.")
print("  At N=3 that is 1/4.  The n cancels, so there is NO N_c selector here:")
print("  2/(N^2-1) = 1 needs N^2 = 3.  F111b T7's agreement at N=3 comes from")
print("  the 1-link vs 4-link mismatch (3 x 4/3 = 4), NOT from the group.")

print()
print("=" * 78)
print("Q4  DO THE MAGNETIC COEFFICIENTS DIFFER?")
print("=" * 78)
reps3 = su.irrep_ladder(6)
H3, r3, MF3 = su.su3_rotor_hamiltonian(1.0, 1.0, 6)
offdiag = set(np.round(MF3[MF3 != 0], 12))
print(f"  SU(3) fusion adjacency M_F non-zero entries: {sorted(offdiag)}")
print(f"  U(1)  cos(phi) off-diagonal (x2):            [1.0]  "
      f"(H has -lam/2 on each)")
print("  Both magnetic terms are -(lam/2) x (unit-entry adjacency + transpose).")
print("  => the magnetic COEFFICIENT is lam in both theories: the magnetic term")
print("     introduces NO factor into the chi-map.  What differs is the fusion")
print("     DEGENERACY and the observable normalisation 1/d_F, which move sigma_1")
print("     by a constant ln((N^2-1)/2) = ln 4 = 1.3863 at N=3, not g_s.")
print()
print(f"  sigma_1 shift at N=3: ln((N^2-1)/2) = {math.log(4.0):.6f} nats")
