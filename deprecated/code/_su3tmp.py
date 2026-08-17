"""
su3_3d_string_tension.py — string tension sigma(beta) from the MODEL's own
SU(3) gauge dynamics in 3D, with beta and the lattice as the ONLY inputs.

This extends the model's 2D-exact confinement (F70: sigma = -ln w(beta) from
the SU(3) group integral, no sigma input) into 3 dimensions, where confinement
is no longer guaranteed by exact solvability — so the area law is a genuine
dynamical result, not a theorem.  The measured sigma(beta) is then available to
feed the F135 scalar-mass bag (closing the "imported sigma" gap flagged in the
2026-06-12 audit).

Reuses the model's exact SU(3) representation:
  - ca_strong.su3_exp  : build SU(3) from 8 real angles (used to make the
                         Metropolis proposal pool)
  - ca_strong.is_su3   : unitarity/det validation
The 3D plaquette, staple and Wilson loops are vectorised numpy matrix algebra
(complex 3x3 link matrices — NOT chiral spinor transforms, so the CLAUDE.md
numpy caveat does not apply; validated by cold <plaq>=1 exactly).

Metropolis update mirrors ca_confinement.metropolis_sweep_2d:
  propose U -> R U,  dS = -(beta/3) Re Tr[(R U - U) Sigma^dag],
  accept with min(1, exp(-dS)); checkerboard by direction (a mu-link's staple
  contains the mu-link at x+-nu, so opposite parities must not update together).
"""
from __future__ import annotations
import os, sys, json, time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "ca-simulation"))
# allow running from the project too
for p in ("ca-simulation", "../ca-simulation"):
    if os.path.isdir(p):
        sys.path.insert(0, p)
try:
    import ca_strong as cstr
    _HAVE_MODEL = True
except Exception:
    _HAVE_MODEL = False

I3 = np.eye(3, dtype=complex)

# ----------------------------------------------------------------------
# matrix helpers on fields of shape (..., 3, 3)
# ----------------------------------------------------------------------
def mm(A, B):
    return np.einsum('...ij,...jk->...ik', A, B)

def dag(A):
    return np.conj(np.swapaxes(A, -1, -2))

def rollp(A, ax):   # result[x] = A[x + e_ax]
    return np.roll(A, -1, axis=ax)

def rollm(A, ax):   # result[x] = A[x - e_ax]
    return np.roll(A, +1, axis=ax)

# ----------------------------------------------------------------------
# proposal pool: symmetric set {R_i, R_i^dag} of small SU(3) steps
# ----------------------------------------------------------------------
def make_pool(eps, n=1500, seed=0):
    rng = np.random.default_rng(seed)
    mats = []
    for _ in range(n):
        if _HAVE_MODEL:
            R = cstr.su3_exp(eps * rng.standard_normal(8))
        else:
            R = _su3_exp_local(eps * rng.standard_normal(8))
        mats.append(R)
        mats.append(np.conj(R.T))     # ensure symmetric proposal distribution
    return np.array(mats)

# fallback su3_exp if model import fails (Gell-Mann generators)
def _gellmann():
    l = np.zeros((8, 3, 3), dtype=complex)
    l[0] = [[0,1,0],[1,0,0],[0,0,0]]
    l[1] = [[0,-1j,0],[1j,0,0],[0,0,0]]
    l[2] = [[1,0,0],[0,-1,0],[0,0,0]]
    l[3] = [[0,0,1],[0,0,0],[1,0,0]]
    l[4] = [[0,0,-1j],[0,0,0],[1j,0,0]]
    l[5] = [[0,0,0],[0,0,1],[0,1,0]]
    l[6] = [[0,0,0],[0,0,-1j],[0,1j,0]]
    l[7] = np.array([[1,0,0],[0,1,0],[0,0,-2]])/np.sqrt(3)
    return l * 0.5
_LAM = _gellmann()
def _su3_exp_local(theta):
    H = sum(theta[a]*_LAM[a] for a in range(8))
    w, V = np.linalg.eigh(H)
    return V @ np.diag(np.exp(1j*w)) @ V.conj().T

# ----------------------------------------------------------------------
# geometry
# ----------------------------------------------------------------------
def cold(L, d):
    return [np.broadcast_to(I3, (L,)*d + (3, 3)).copy() for _ in range(d)]

def staple(U, mu, d):
    """Sigma_mu(x) with sum_{p>=U_mu(x)} Re Tr U_p = Re Tr[U_mu(x) Sigma_mu^dag]."""
    L = U[0].shape[0]
    S = np.zeros((L,)*d + (3, 3), dtype=complex)
    Umu = U[mu]
    for nu in range(d):
        if nu == mu:
            continue
        Unu = U[nu]
        # forward: U_nu(x) U_mu(x+nu) U_nu(x+mu)^dag
        Sp = mm(mm(Unu, rollp(Umu, nu)), dag(rollp(Unu, mu)))
        # backward: U_nu(x-nu)^dag U_mu(x-nu) U_nu(x+mu-nu)
        Unu_pmu_mnu = rollm(rollp(Unu, mu), nu)
        Sm = mm(mm(dag(rollm(Unu, nu)), rollm(Umu, nu)), Unu_pmu_mnu)
        S = S + Sp + Sm
    return S

def mean_plaquette(U, d):
    tot = 0.0; npl = 0
    for mu in range(d):
        for nu in range(mu+1, d):
            P = mm(mm(U[mu], rollp(U[nu], mu)),
                   mm(dag(rollp(U[mu], nu)), dag(U[nu])))
            tot += np.real(np.trace(P, axis1=-2, axis2=-1)).mean()/3.0
            npl += 1
    return tot/npl

def parity_mask(L, d, par):
    g = np.indices((L,)*d)
    return (g.sum(0) % 2) == par

# ----------------------------------------------------------------------
# Metropolis sweep (checkerboard by direction), vectorised over a sublattice
# ----------------------------------------------------------------------
def sweep(U, beta, d, pool, rng, n_hit=3):
    L = U[0].shape[0]
    npool = pool.shape[0]
    acc = 0; tot = 0
    for mu in range(d):
        Sig = None
        for par in (0, 1):
            mask = parity_mask(L, d, par)
            for _ in range(n_hit):
                Sig = staple(U, mu, d)              # recompute (links changed)
                Umu = U[mu]
                idx = rng.integers(0, npool, size=(L,)*d)
                R = pool[idx]                       # (L,L,L,3,3) proposals
                Unew = mm(R, Umu)
                dphi = mm(Unew - Umu, dag(Sig))
                dS = -(beta/3.0) * np.real(np.trace(dphi, axis1=-2, axis2=-1))
                a = (dS <= 0) | (rng.random((L,)*d) < np.exp(-np.minimum(dS, 700)))
                a = a & mask
                U[mu] = np.where(a[..., None, None], Unew, Umu)
                acc += int(a.sum()); tot += int(mask.sum())
    return acc/max(tot, 1)

# ----------------------------------------------------------------------
# Wilson loops
# ----------------------------------------------------------------------
def line(U, mu, R):
    P = U[mu].copy(); cur = U[mu]
    for _ in range(1, R):
        cur = rollp(cur, mu)
        P = mm(P, cur)
    return P

def wilson(U, mu, nu, R, T):
    Lmu = line(U, mu, R)
    Lnu = line(U, nu, T)
    right = Lnu
    for _ in range(R):
        right = rollp(right, mu)
    topdag = Lmu
    for _ in range(T):
        topdag = rollp(topdag, nu)
    P = mm(mm(Lmu, right), mm(dag(topdag), dag(Lnu)))
    return np.real(np.trace(P, axis1=-2, axis2=-1)).mean()/3.0

def all_loops(U, d, rmax, tmax):
    planes = [(mu, nu) for mu in range(d) for nu in range(d) if mu != nu]
    out = {}
    for R in range(1, rmax+1):
        for T in range(1, tmax+1):
            out[(R, T)] = float(np.mean([wilson(U, mu, nu, R, T)
                                         for (mu, nu) in planes]))
    return out

def static_potential(W, rmax, tmax, t_lo=2):
    V = {}
    for R in range(1, rmax+1):
        v = []
        for T in range(t_lo, tmax):
            a, b = W.get((R, T)), W.get((R, T+1))
            if a and b and a > 0 and b > 0:
                v.append(np.log(a/b))
        if v:
            V[R] = float(np.mean(v))
    return V

def fit_linear(V):
    Rs = np.array(sorted(V)); ys = np.array([V[r] for r in Rs])
    A = np.vstack([Rs, np.ones_like(Rs)]).T
    s, *_ = np.linalg.lstsq(A, ys, rcond=None)
    return float(s[0]), float(s[1])

def creutz(W, R, T):
    try:
        num = W[(R, T)]*W[(R-1, T-1)]; den = W[(R-1, T)]*W[(R, T-1)]
        if num > 0 and den > 0:
            return -np.log(num/den)
    except KeyError:
        pass
    return None

# ----------------------------------------------------------------------
def run(beta, L=6, d=3, eps=0.24, n_therm=120, n_meas=120, meas_every=4,
        rmax=4, tmax=5, n_hit=3, seed=1):
    rng = np.random.default_rng(seed)
    pool = make_pool(eps, n=1200, seed=seed+1)
    U = cold(L, d)
    accs = []
    for _ in range(n_therm):
        accs.append(sweep(U, beta, d, pool, rng, n_hit=n_hit))
    Lsum = {(R, T): [] for R in range(1, rmax+1) for T in range(1, tmax+1)}
    plaq = []; n = 0
    for s in range(n_meas):
        a = sweep(U, beta, d, pool, rng, n_hit=n_hit)
        accs.append(a)
        if s % meas_every:
            continue
        n += 1
        plaq.append(mean_plaquette(U, d))
        for k, v in all_loops(U, d, rmax, tmax).items():
            Lsum[k].append(v)
    W = {f"{R},{T}": float(np.mean(Lsum[(R, T)])) for (R, T) in Lsum}
    Wt = {(R, T): float(np.mean(Lsum[(R, T)])) for (R, T) in Lsum}
    return {"beta": beta, "L": L, "d": d, "acceptance": float(np.mean(accs)),
            "mean_plaquette": float(np.mean(plaq)), "n_meas": n, "W": W,
            "_Wt": Wt, "rmax": rmax, "tmax": tmax}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--beta", type=float, default=6.0)
    ap.add_argument("--L", type=int, default=6)
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    if a.smoke:
        U = cold(4, 3)
        print("cold <plaq> =", mean_plaquette(U, 3),
              " is_su3 link[0,0,0]:",
              (cstr.is_su3(U[0][0, 0, 0]) if _HAVE_MODEL else "n/a"))
        t = time.time()
        r = run(beta=6.0, L=4, n_therm=10, n_meas=8, meas_every=2,
                rmax=2, tmax=2, seed=3)
        print("smoke beta=6 L=4: acc=%.2f <plaq>=%.4f W(1,1)=%.4f (%.1fs)"
              % (r["acceptance"], r["mean_plaquette"], r["W"]["1,1"],
                 time.time()-t))
