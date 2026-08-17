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

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
# allow running from the project too
try:
    from casim.engine.gauge import strong as cstr
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

def _noise_floor(W, abs_floor=1e-4, k=5.0):
    """Statistical noise floor for the Wilson loops.  Large loops decay
    exponentially and eventually sink into the Monte-Carlo noise, where the
    mean goes tiny and even negative.  Estimate the floor from the magnitude of
    the loops that have gone negative (pure noise): floor = max(abs_floor,
    k * max|W_negative|).  Below this a loop carries no signal and must not be
    used to build the potential."""
    negs = [abs(v) for v in W.values() if v <= 0]
    return max(abs_floor, k * max(negs)) if negs else abs_floor


def static_potential(W, rmax, tmax, t_lo=2, w_floor=None, plateau_tol=0.08):
    """Effective-mass static potential V(R) = ln[W(R,T)/W(R,T+1)] on a CLEAN
    plateau.

    Earlier this averaged the effective mass over every T-window up to tmax and
    kept every R up to rmax.  At large R/T the Wilson loops have decayed below
    the statistical noise floor (tiny, then negative), so those windows are pure
    noise — folding them in drove V(R) non-monotone at large R and gave the
    Cornell fit an unphysical negative sigma.  The fix applies three guards:
      1. floor    : only windows with BOTH loops above the noise floor are used;
      2. monotone : require W(R,T) > W(R,T+1) > 0 (loops must decay in T) and
                    stop scanning a given R at the first window that violates it;
      3. plateau  : reject window outliers deviating > plateau_tol from the
                    median effective mass (kills the inflated last-clean window).
    R values left with fewer than two clean windows are dropped — their loops
    have decayed into noise and carry no reliable potential."""
    if w_floor is None:
        w_floor = _noise_floor(W)
    V = {}
    for R in range(1, rmax + 1):
        meff = []
        for T in range(t_lo, tmax):
            a, b = W.get((R, T)), W.get((R, T + 1))
            if a is None or b is None:
                continue
            if a > w_floor and b > w_floor and a > b:   # clean & monotone decay
                meff.append(np.log(a / b))
            else:
                break                                   # rest of this R is noise
        if len(meff) < 2:
            continue
        med = float(np.median(meff))
        keep = [m for m in meff if abs(m - med) <= plateau_tol * abs(med)]
        if len(keep) < 2:
            keep = meff
        V[R] = float(np.mean(keep))
    return V

def fit_linear(V):
    Rs = np.array(sorted(V)); ys = np.array([V[r] for r in Rs])
    A = np.vstack([Rs, np.ones_like(Rs)]).T
    s, *_ = np.linalg.lstsq(A, ys, rcond=None)
    return float(s[0]), float(s[1])


def fit_coulomb_linear(V, rmin=1):
    """Cornell fit V(R) = V0 - (4/3) alpha_V / R + sigma R to the measured
    static potential.  The Coulomb coefficient gives the V-scheme coupling
    alpha_V(q) at the lattice scale (q ~ 1/a_g), the leg Residual A-NP needs;
    sigma is the string tension (F124/F146 leg).  Linear least squares in the
    basis {1, 1/R, R}.  Returns alpha_V, sigma, V0 and the fit residual."""
    Rs = np.array([r for r in sorted(V) if r >= rmin], dtype=float)
    if len(Rs) < 3:
        return {"ok": False, "reason": "need >=3 R points", "nR": len(Rs)}
    ys = np.array([V[r] for r in Rs])
    A = np.vstack([np.ones_like(Rs), 1.0 / Rs, Rs]).T   # [V0, c, sigma]
    coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
    V0, c, sigma = (float(x) for x in coef)
    alpha_V = -c / (4.0 / 3.0)        # c = -(4/3) alpha_V
    resid = float(np.sqrt(np.mean((A @ coef - ys) ** 2)))
    return {"ok": True, "alpha_V": alpha_V, "sigma": sigma, "V0": V0,
            "rms_resid": resid, "Rs_used": [int(r) for r in Rs],
            "alpha_s_uv_lock": 0.25 / (4.0 * 3.141592653589793)}

def creutz(W, R, T):
    try:
        num = W[(R, T)]*W[(R-1, T-1)]; den = W[(R-1, T)]*W[(R, T-1)]
        if num > 0 and den > 0:
            return -np.log(num/den)
    except KeyError:
        pass
    return None

# ----------------------------------------------------------------------
def _result_dict(beta, L, d, accs, plaq, Lsum, n, rmax, tmax):
    """Assemble the run() result dict from the current accumulators.  Safe to
    call mid-run (for checkpoints): only (R,T) with at least one sample are
    included, and empty accumulators give 0.0 rather than a nan from mean([])."""
    W, Wt = {}, {}
    for (R, T), samples in Lsum.items():
        if samples:
            m = float(np.mean(samples))
            W[f"{R},{T}"] = m
            Wt[(R, T)] = m
    return {"beta": beta, "L": L, "d": d,
            "acceptance": float(np.mean(accs)) if accs else 0.0,
            "mean_plaquette": float(np.mean(plaq)) if plaq else 0.0,
            "n_meas": n, "W": W, "_Wt": Wt, "rmax": rmax, "tmax": tmax}


def write_output(out, run_result, params, secs, complete):
    """Write the {run, analysis, params, secs, complete} JSON atomically.

    Used for BOTH periodic checkpoints (complete=False) and the final dump
    (complete=True), so a killed run still leaves a usable lower-statistics
    file at `out`.  The write goes to a temp file then os.replace()s into
    place, so an interrupt mid-write never corrupts the JSON.  `complete`
    lets a resumed batch tell a finished run from a partial one.  Returns the
    payload (so the caller can print the analysis without recomputing)."""
    r = dict(run_result)                       # shallow copy; keep caller's _Wt
    ana = analyse(r)                            # reads r["_Wt"]
    r.pop("_Wt", None)                          # tuple keys aren't JSON-friendly
    payload = {"run": r, "analysis": ana, "params": params,
               "secs": round(secs, 1), "complete": bool(complete)}
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    tmp = out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2, default=str)
    os.replace(tmp, out)                        # atomic
    return payload


def run(beta, L=6, d=3, eps=0.24, n_therm=120, n_meas=120, meas_every=4,
        rmax=4, tmax=5, n_hit=3, seed=1, verbose=False,
        out=None, checkpoint_every=0, run_params=None):
    rng = np.random.default_rng(seed)
    pool = make_pool(eps, n=1200, seed=seed+1)
    U = cold(L, d)
    t0 = time.time()
    every = max(1, (n_therm + n_meas) // 40)   # ~40 heartbeats over the whole run
    accs = []
    for i in range(n_therm):
        accs.append(sweep(U, beta, d, pool, rng, n_hit=n_hit))
        if verbose and (i % every == 0 or i == n_therm - 1):
            el = time.time() - t0
            eta = el / (i + 1) * (n_therm + n_meas) - el
            print("  [therm %d/%d] acc=%.2f <plaq>=%.4f  %.0fs elapsed, ~%.0fs left"
                  % (i + 1, n_therm, accs[-1], mean_plaquette(U, d), el, eta),
                  flush=True)
    Lsum = {(R, T): [] for R in range(1, rmax+1) for T in range(1, tmax+1)}
    plaq = []; n = 0
    for s in range(n_meas):
        a = sweep(U, beta, d, pool, rng, n_hit=n_hit)
        accs.append(a)
        if verbose and (s % every == 0 or s == n_meas - 1):
            el = time.time() - t0
            eta = el / (n_therm + s + 1) * (n_therm + n_meas) - el
            print("  [meas %d/%d] acc=%.2f  %.0fs elapsed, ~%.0fs left"
                  % (s + 1, n_meas, a, el, eta), flush=True)
        if s % meas_every:
            continue
        n += 1
        plaq.append(mean_plaquette(U, d))
        for k, v in all_loops(U, d, rmax, tmax).items():
            Lsum[k].append(v)
        # periodic checkpoint: a killed run still leaves a usable JSON at `out`.
        # Triggered on the measurement counter n (NOT the sweep index s, which
        # would alias against meas_every and could never fire).
        if out and checkpoint_every and n % checkpoint_every == 0:
            write_output(out, _result_dict(beta, L, d, accs, plaq, Lsum, n,
                                           rmax, tmax),
                         run_params, time.time() - t0, complete=False)
            if verbose:
                print("  [checkpoint] wrote %s at meas-sweep %d (n=%d recorded)"
                      % (out, s + 1, n), flush=True)
    return _result_dict(beta, L, d, accs, plaq, Lsum, n, rmax, tmax)


def analyse(r):
    """Static potential + Cornell (Coulomb+linear) fit from a run() result.

    Accepts either a live run() dict (tuple-keyed ``_Wt``) or one reloaded from
    JSON (string-keyed ``W`` of the form ``"R,T"``), so a saved run can be
    re-analysed without repeating the Monte-Carlo."""
    if "_Wt" in r:
        Wt = r["_Wt"]
    else:
        Wt = {(int(k.split(",")[0]), int(k.split(",")[1])): v
              for k, v in r["W"].items()}
    V = static_potential(Wt, r["rmax"], r["tmax"])
    sig_lin, off = fit_linear(V) if len(V) >= 2 else (None, None)
    cl = fit_coulomb_linear(V)
    return {"V_of_R": {str(k): v for k, v in V.items()},
            "linear_fit": {"sigma": sig_lin, "offset": off},
            "cornell_fit": cl}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--beta", type=float, default=6.0)
    ap.add_argument("--L", type=int, default=6)
    ap.add_argument("--ntherm", type=int, default=120)
    ap.add_argument("--nmeas", type=int, default=120)
    ap.add_argument("--meas_every", type=int, default=4)
    ap.add_argument("--rmax", type=int, default=4)
    ap.add_argument("--tmax", type=int, default=5)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default=None,
                    help="write the run() dict + Cornell-fit analysis to JSON")
    ap.add_argument("--checkpoint_every", type=int, default=50,
                    help="write a partial JSON to --out every N recorded "
                         "measurements (~N*meas_every sweeps; 0 disables); a "
                         "killed run still leaves usable data. Final dump is "
                         "marked \"complete\": true.")
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
    else:
        t = time.time()
        print("running beta=%.2f L=%d: %d therm + %d meas sweeps "
              "(~%.0f min at this L; progress below)..."
              % (a.beta, a.L, a.ntherm, a.nmeas,
                 (a.ntherm + a.nmeas) * (a.L / 24.0) ** 3 * 0.59 / 60.0), flush=True)
        r = run(beta=a.beta, L=a.L, n_therm=a.ntherm, n_meas=a.nmeas,
                meas_every=a.meas_every, rmax=a.rmax, tmax=a.tmax, seed=a.seed,
                verbose=True, out=a.out, checkpoint_every=a.checkpoint_every,
                run_params=vars(a))
        print("beta=%.2f L=%d: acc=%.2f <plaq>=%.4f (%.1fs)"
              % (r["beta"], r["L"], r["acceptance"], r["mean_plaquette"],
                 time.time() - t))
        if a.out:
            payload = write_output(a.out, r, vars(a), time.time() - t,
                                   complete=True)
            print("  Cornell fit:", payload["analysis"]["cornell_fit"])
            print("  wrote", a.out, "(complete)")
        else:
            print("  Cornell fit:", analyse(r)["cornell_fit"])
