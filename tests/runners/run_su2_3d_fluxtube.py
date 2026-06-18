"""
su2_3d_fluxtube.py  — Does a confining flux tube appear with NO input string
tension and NO condensate VEV?

Minimal non-trivial testbed: pure SU(2) lattice gauge theory in 3 Euclidean
dimensions, sampled by the exact Creutz/Kennedy-Pendleton heat bath.  The ONLY
inputs are the gauge coupling beta and the lattice.  Nothing about a string
tension sigma, a condensate v, a bag mass, or a smear length is supplied.

If a confining flux tube is genuinely emergent from the gauge dynamics, the
static quark potential V(R) = -lim_T (1/T) ln <W(R,T)> must come out LINEAR,
V(R) = sigma*R + const, with sigma > 0 a pure number extracted from the
Monte-Carlo configurations — i.e. dimensional transmutation.

This is the test the real-space bound-state findings (F135/F137/F139) do NOT
do: they re-import sigma (or v, M_bag, lam) as inputs.  2D (F70) confines at
all couplings trivially; 3D is the place where it could fail.

SU(2) is represented by unit quaternions q=(a0,a1,a2,a3) <-> a0*I + i a.sigma,
so all arithmetic is real (avoids the numpy/chiral complex pitfalls flagged in
CLAUDE.md).  Quaternion product is a faithful SU(2) representation.
"""
from __future__ import annotations
import numpy as np
import json, sys, time

# ----------------------------------------------------------------------
# quaternion (=SU(2)) algebra on component arrays, last axis = 4
# ----------------------------------------------------------------------
def qmul(p, q):
    p0, q0 = p[..., 0], q[..., 0]
    pv, qv = p[..., 1:], q[..., 1:]
    s = p0 * q0 - np.sum(pv * qv, axis=-1)
    v = (p0[..., None] * qv + q0[..., None] * pv
         + np.cross(pv, qv))
    return np.concatenate([s[..., None], v], axis=-1)

def qconj(p):
    out = p.copy()
    out[..., 1:] *= -1.0
    return out

def qnorm(p):
    return np.sqrt(np.sum(p * p, axis=-1))

def identity_field(shape):
    q = np.zeros(shape + (4,))
    q[..., 0] = 1.0
    return q

# ----------------------------------------------------------------------
# geometry: links Q[mu] shape (L,L,L,4), mu in 0..d-1
# ----------------------------------------------------------------------
def roll_fwd(a, mu):   # shift so result[x] = a[x+mu_hat]
    return np.roll(a, -1, axis=mu)
def roll_bwd(a, mu):
    return np.roll(a, +1, axis=mu)

def staple_sum(Q, mu, d):
    """Sum of the 2*(d-1) staples around link Q[mu]; returns quaternion field."""
    L = Q[0].shape[0]
    A = np.zeros((L,) * d + (4,))
    Umu = Q[mu]
    for nu in range(d):
        if nu == mu:
            continue
        Unu = Q[nu]
        # forward staple: U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag
        a = qmul(roll_fwd(Unu, mu), qconj(roll_fwd(Umu, nu)))
        a = qmul(a, qconj(Unu))
        A = A + a
        # backward staple: U_nu(x+mu-nu)^dag U_mu(x-nu)^dag U_nu(x-nu)
        Unu_mnu = roll_bwd(roll_fwd(Unu, mu), nu)
        b = qmul(qconj(Unu_mnu), qconj(roll_bwd(Umu, nu)))
        b = qmul(b, roll_bwd(Unu, nu))
        A = A + b
    return A

# ----------------------------------------------------------------------
# Kennedy-Pendleton heat bath for SU(2), vectorised over a site mask
# ----------------------------------------------------------------------
def kp_sample_a0(beta, k, rng):
    """Sample a0 ~ exp(2*beta*k*a0)*sqrt(1-a0^2) for arrays beta_eff=2*beta*k.
       Returns array a0 in (-1,1). Vectorised rejection (KP)."""
    bk = beta * k                # P(a0) ~ exp(beta*|A|*a0) sqrt(1-a0^2)
    n = k.shape
    a0 = np.empty(n)
    todo = np.ones(n, dtype=bool)
    # guard tiny bk (free links) -> uniform-ish; KP still works but slow; clip
    bk = np.maximum(bk, 1e-6)
    it = 0
    while todo.any():
        it += 1
        m = todo
        cnt = int(m.sum())
        r1 = rng.random(cnt); r2 = rng.random(cnt); r3 = rng.random(cnt)
        # KP: lambda^2 = -(1/(2 bk)) [ln r1 + cos^2(2 pi r2) ln r3]
        lam2 = -(1.0 / (2.0 * bk[m])) * (np.log(r1) + (np.cos(2*np.pi*r2)**2) * np.log(r3))
        cand_a0 = 1.0 - 2.0 * lam2
        acc = rng.random(cnt) ** 2 <= (1.0 - lam2)
        idx = np.where(m.ravel())[0]
        acc_idx = idx[acc]
        flat = a0.ravel()
        flat[acc_idx] = cand_a0[acc]
        a0 = flat.reshape(n)
        tflat = todo.ravel()
        tflat[acc_idx] = False
        todo = tflat.reshape(n)
        if it > 60:   # safety
            flat = a0.ravel(); flat[np.where(todo.ravel())[0]] = 0.0
            a0 = flat.reshape(n); break
    return a0

def _parity_mask(L, d, par):
    grids = np.indices((L,) * d)
    return (grids.sum(axis=0) % 2) == par

def heatbath_link(Q, mu, beta, d, rng, mask):
    """Heat-bath update of the mu-links ON the given sublattice mask only.
    Checkerboard is REQUIRED: a mu-link's staple contains the mu-link at x+-nu,
    so same-direction links of opposite parity must not be updated together
    (else detailed balance is broken and the config runs away to disorder)."""
    A = staple_sum(Q, mu, d)          # uses current Q (correct for masked sites)
    k = qnorm(A)
    kk = np.maximum(k, 1e-12)
    V = A / kk[..., None]
    a0 = kp_sample_a0(beta, k, rng)
    shp = a0.shape
    cphi = 2.0 * rng.random(shp) - 1.0
    sphi = np.sqrt(np.maximum(0.0, 1.0 - cphi * cphi))
    theta = 2.0 * np.pi * rng.random(shp)
    rho = np.sqrt(np.maximum(0.0, 1.0 - a0 * a0))
    W = np.stack([a0,
                  rho * sphi * np.cos(theta),
                  rho * sphi * np.sin(theta),
                  rho * cphi], axis=-1)
    Unew = qmul(W, qconj(V))          # U*V = W has the sampled trace dist.
    m = mask[..., None]
    Q[mu] = np.where(m, Unew, Q[mu])

def sweep(Q, beta, d, rng):
    L = Q[0].shape[0]
    for mu in range(d):
        for par in (0, 1):
            heatbath_link(Q, mu, beta, d, rng, _parity_mask(L, d, par))

# ----------------------------------------------------------------------
# observables
# ----------------------------------------------------------------------
def mean_plaquette(Q, d):
    """<(1/2)Tr U_plaq> averaged over all plaquettes."""
    tot = 0.0; npl = 0
    for mu in range(d):
        for nu in range(mu + 1, d):
            P = qmul(Q[mu], roll_fwd(Q[nu], mu))
            P = qmul(P, qconj(roll_fwd(Q[mu], nu)))
            P = qmul(P, qconj(Q[nu]))
            tot += P[..., 0].mean()   # (1/2)Tr = scalar part
            npl += 1
    return tot / npl

def line_product(Q, mu, R):
    """Ordered product U_mu(x)U_mu(x+mu)...U_mu(x+(R-1)mu), quaternion field."""
    P = Q[mu].copy()
    cur = Q[mu]
    for _ in range(1, R):
        cur = roll_fwd(cur, mu)
        P = qmul(P, cur)
    return P

def wilson_loop(Q, mu, nu, R, T):
    """<(1/2)Tr W(R,T)> in the (mu,nu) plane, averaged over sites."""
    Lmu = line_product(Q, mu, R)                       # x -> x+R mu
    Lnu = line_product(Q, nu, T)                       # x -> x+T nu
    # shift line products to the corners of the rectangle
    top = Lmu                                          # bottom edge  +mu
    right = Lnu
    for _ in range(R):
        right = roll_fwd(right, mu)                    # right edge at x+R mu
    topdag = Lmu
    for _ in range(T):
        topdag = roll_fwd(topdag, nu)                  # top edge at x+T nu (to be daggered)
    leftdag = Lnu                                      # left edge +nu (to be daggered)
    P = qmul(top, right)
    P = qmul(P, qconj(topdag))
    P = qmul(P, qconj(leftdag))
    return P[..., 0].mean()

def all_loops(Q, d, rmax, tmax):
    acc = {}
    planes = [(mu, nu) for mu in range(d) for nu in range(d) if mu != nu]
    for R in range(1, rmax + 1):
        for T in range(1, tmax + 1):
            vals = [wilson_loop(Q, mu, nu, R, T) for (mu, nu) in planes]
            acc[(R, T)] = float(np.mean(vals))
    return acc

# ----------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------
def run(beta, L=8, d=3, n_therm=120, n_meas=120, meas_every=2,
        rmax=4, tmax=4, seed=1):
    rng = np.random.default_rng(seed)
    Q = [identity_field((L,) * d) for _ in range(d)]
    for _ in range(n_therm):
        sweep(Q, beta, d, rng)
    loopsum = {(R, T): [] for R in range(1, rmax + 1) for T in range(1, tmax + 1)}
    plaq = []
    nmeas = 0
    for s in range(n_meas):
        sweep(Q, beta, d, rng)
        if s % meas_every:
            continue
        nmeas += 1
        plaq.append(mean_plaquette(Q, d))
        wl = all_loops(Q, d, rmax, tmax)
        for key, v in wl.items():
            loopsum[key].append(v)
    W = {f"{R},{T}": float(np.mean(loopsum[(R, T)])) for (R, T) in loopsum}
    return {"beta": beta, "L": L, "d": d, "n_meas": nmeas,
            "mean_plaquette": float(np.mean(plaq)),
            "W": W, "rmax": rmax, "tmax": tmax}


def static_potential(W, rmax, tmax, t_lo=2):
    """V(R) from the effective-mass plateau: V(R)=-ln[W(R,T)/W(R,T+1)],
    averaged over T>=t_lo where it plateaus.  Returns dict R->V."""
    V = {}
    for R in range(1, rmax + 1):
        vals = []
        for T in range(t_lo, tmax):
            a, b = W.get(f"{R},{T}"), W.get(f"{R},{T+1}")
            if a and b and a > 0 and b > 0:
                vals.append(np.log(a / b))
        if vals:
            V[R] = float(np.mean(vals))
    return V

def creutz(W, R, T):
    """chi(R,T) = -ln[ W(R,T)W(R-1,T-1)/(W(R-1,T)W(R,T-1)) ] -> sigma."""
    try:
        num = W[f"{R},{T}"] * W[f"{R-1},{T-1}"]
        den = W[f"{R-1},{T}"] * W[f"{R},{T-1}"]
        if num > 0 and den > 0:
            return -np.log(num / den)
    except KeyError:
        pass
    return None

def fit_linear(V):
    """Fit V(R)=sigma*R + V0 over the available R; return sigma, V0."""
    Rs = np.array(sorted(V)); ys = np.array([V[r] for r in Rs])
    A = np.vstack([Rs, np.ones_like(Rs)]).T
    sol, *_ = np.linalg.lstsq(A, ys, rcond=None)
    return float(sol[0]), float(sol[1])


if __name__ == "__main__":
    # tiny smoke test
    t = time.time()
    r = run(beta=4.0, L=6, n_therm=20, n_meas=20, meas_every=2, rmax=3, tmax=3, seed=7)
    print("smoke beta=4 L=6: <plaq>=%.4f  W(1,1)=%.4f  W(2,2)=%.4f  (%.1fs)"
          % (r["mean_plaquette"], r["W"]["1,1"], r["W"]["2,2"], time.time() - t))
