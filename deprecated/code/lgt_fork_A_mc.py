# ===== deprecated/code backup =====================================
# source     : ca-simulation/forks/lgt_fork_A_mc.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/forks/gauge/lgt_fork_A_mc.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: lgt_fork_A_mc.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
lgt_fork_A_mc.py — Fork A: 3+1D SU(3) lattice-gauge Monte-Carlo + multilevel  (P1, Option A)
============================================================================================

Created: 2026-06-04

The **standard, rigorous** binding-force route from
`deprecated/roadmap-P1-binding-force-options.md`, built as a fork to stand head-to-head
with Option C (F86, the colour-dielectric / dual superconductor).  Where C is a
model-native, algebraically-exact mechanism, A is the textbook lattice-gauge
computation: thermalise the SU(3) Wilson ensemble with a proper heat-bath, beat
the exponential signal-to-noise wall with a Lüscher–Weisz multilevel estimator,
and read off the confining static potential  V(R) = mu + sigma R - e/R.

This directly repairs the wall that `tests/runners/run_confinement_mc.py`
(plain 2D Metropolis) ran into: large Wilson/Polyakov correlators decay as
exp(-sigma·Area) far below the 1/sqrt(N) noise floor.  Heat-bath gives short
autocorrelation; the two-level estimator factorises the correlator into
sublattice averages whose variance multiplies instead of adding, recovering an
exponentially better signal.

Contents
--------
  * D-dimensional SU(3) Wilson link field (D=3,4 used here).
  * Plaquette, staple (all planes), mean plaquette, Wilson action.
  * Cabibbo–Marinari pseudo-heat-bath via SU(2) subgroups (Creutz a0 sampler),
    checkerboard-vectorised; SU(2)-subgroup over-relaxation.
  * Observables: planar Wilson loops, Polyakov loop and its correlator.
  * Lüscher–Weisz **two-level** estimator for the Polyakov-loop correlator.

All pure-numpy (no scipy), per project practice.  Heavy production runs go
through `tests/runners/run_lgt_confinement.py`; the sandbox battery
`tests/findings/test_FA_lgt_mc.py` exercises correctness on small lattices.

Conventions
-----------
  Wilson action  S = beta * sum_plaq ( 1 - (1/3) Re Tr U_plaq ),  N=3.
  Link field shape:  (D,) + (L,)*D + (3,3)  complex; axis 0 = direction mu;
  by convention the LAST lattice axis is Euclidean time.
"""

import numpy as np

# SU(3) helpers reused from the validated cooling module.
import sys as _sys, os as _os
_CA = _os.path.join(_os.path.dirname(__file__), '..')
if _CA not in _sys.path:
    _sys.path.insert(0, _CA)
import ca_cooling as _cc            # _mm, _dag, su3_project, su3_exp_algebra
import ca_strong as _cs            # su3_haar

_mm = _cc._mm
_dag = _cc._dag
su3_project = _cc.su3_project


# ══════════════════════════════════════════════════════════════════
#  Link-field construction
# ══════════════════════════════════════════════════════════════════

def cold_links(L, D):
    """Cold (ordered) start: every link = I.  Shape (D,)+(L,)*D+(3,3)."""
    shp = (D,) + (L,) * D + (3, 3)
    U = np.zeros(shp, dtype=complex)
    eye = np.eye(3, dtype=complex)
    U[...] = eye
    return U


def hot_links(L, D, seed=0):
    """Hot (disordered) start: every link Haar-random SU(3)."""
    rng = np.random.default_rng(seed)
    shp = (D,) + (L,) * D
    U = np.empty(shp + (3, 3), dtype=complex)
    for idx in np.ndindex(shp):
        U[idx] = _cs.su3_haar(rng)
    return U


# ══════════════════════════════════════════════════════════════════
#  Geometry: plaquettes, staples (D-dimensional)
# ══════════════════════════════════════════════════════════════════

def _shift(A, mu, sign):
    """Shift a per-site field so result[x] = A[x + sign*e_mu] (mu a lattice axis index)."""
    return np.roll(A, -sign, axis=mu)


def plaquette(U, mu, nu):
    """U_mu(x) U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag — per-site (...,3,3)."""
    Umu = U[mu]
    Unu = U[nu]
    Unu_xmu = _shift(Unu, mu, +1)
    Umu_xnu = _shift(Umu, nu, +1)
    return _mm(_mm(Umu, Unu_xmu), _mm(_dag(Umu_xnu), _dag(Unu)))


def mean_plaquette(U):
    """⟨(1/3) Re Tr U_plaq⟩ over all planes and sites."""
    D = U.shape[0]
    tot = 0.0
    npl = 0
    for mu in range(D):
        for nu in range(mu + 1, D):
            P = plaquette(U, mu, nu)
            tot += np.real(np.trace(P, axis1=-2, axis2=-1)).mean() / 3.0
            npl += 1
    return float(tot / npl)


def wilson_action(U, beta):
    """S = beta * sum_plaq (1 - (1/3)Re Tr U_plaq)."""
    D = U.shape[0]
    s = 0.0
    for mu in range(D):
        for nu in range(mu + 1, D):
            P = plaquette(U, mu, nu)
            s += np.sum(1.0 - np.real(np.trace(P, axis1=-2, axis2=-1)) / 3.0)
    return float(beta * s)


def staple_field(U, mu):
    """
    Staple *completion* attached to U_mu(x), per site (...,3,3).

    Returns  R_mu(x) = sum_nu [ Unu(x+mu) Umu(x+nu)^dag Unu(x)^dag           (C+)
                                + Unu(x+mu-nu)^dag Umu(x-nu)^dag Unu(x-nu) ] (C-)
    so that  sum_{plaq ∋ U_mu(x)} Re Tr U_plaq = Re Tr[ U_mu(x) · R_mu(x) ].
    (In the Σ-notation R = Σ^dag; the local heat-bath weight is exp((β/N) Re Tr[U R]).)
    Verified: sum over links of Re Tr(U_mu R_mu) = 4 · (plaquette-sum Re Tr).
    """
    D = U.shape[0]
    Umu = U[mu]
    Sigma = np.zeros_like(Umu)
    for nu in range(D):
        if nu == mu:
            continue
        Unu = U[nu]
        # forward staple:  Unu(x+mu) Umu(x+nu)^dag Unu(x)^dag
        Unu_xmu = _shift(Unu, mu, +1)
        Umu_xnu = _shift(Umu, nu, +1)
        Sigma += _mm(_mm(Unu_xmu, _dag(Umu_xnu)), _dag(Unu))
        # backward staple: Unu(x+mu-nu)^dag Umu(x-nu)^dag Unu(x-nu)
        Unu_xmu_mnu = _shift(_shift(Unu, mu, +1), nu, -1)
        Umu_mnu = _shift(Umu, nu, -1)
        Unu_mnu = _shift(Unu, nu, -1)
        Sigma += _mm(_mm(_dag(Unu_xmu_mnu), _dag(Umu_mnu)), Unu_mnu)
    return Sigma


# ══════════════════════════════════════════════════════════════════
#  SU(2)-subgroup machinery  (Cabibbo–Marinari)
# ══════════════════════════════════════════════════════════════════

_SUBGROUPS = ((0, 1), (0, 2), (1, 2))


def _su2_from_block(w):
    """
    Project a batch of 2×2 complex blocks w (M,2,2) onto SU(2): return (V2, k)
    with V2 the unit-SU(2) matrix M(v) and k = |quaternion| (>=0).

    Quaternion of w:  a0=Re(w00+w11)/2, a1=Im(w01+w10)/2,
                      a2=Re(w01-w10)/2,  a3=Im(w00-w11)/2;  k=|a|.
    V2 = M(a/k) with M(q)=[[q0+i q3, q2+i q1],[-q2+i q1, q0-i q3]].
    """
    a0 = 0.5 * (w[..., 0, 0].real + w[..., 1, 1].real)
    a1 = 0.5 * (w[..., 0, 1].imag + w[..., 1, 0].imag)
    a2 = 0.5 * (w[..., 0, 1].real - w[..., 1, 0].real)
    a3 = 0.5 * (w[..., 0, 0].imag - w[..., 1, 1].imag)
    k = np.sqrt(a0 * a0 + a1 * a1 + a2 * a2 + a3 * a3)
    ksafe = np.where(k > 1e-15, k, 1.0)
    q0, q1, q2, q3 = a0 / ksafe, a1 / ksafe, a2 / ksafe, a3 / ksafe
    V2 = _quat_to_mat(q0, q1, q2, q3)
    return V2, k


def _quat_to_mat(q0, q1, q2, q3):
    """SU(2) matrix M(q) = q0 I + i(q1 σ1 + q2 σ2 + q3 σ3), batched."""
    M = np.empty(q0.shape + (2, 2), dtype=complex)
    M[..., 0, 0] = q0 + 1j * q3
    M[..., 0, 1] = q2 + 1j * q1
    M[..., 1, 0] = -q2 + 1j * q1
    M[..., 1, 1] = q0 - 1j * q3
    return M


def _embed_su2(R2, i, j, batch_shape):
    """Embed a batch of 2×2 SU(2) matrices R2 into 3×3 identity at indices (i,j)."""
    E = np.broadcast_to(np.eye(3, dtype=complex), batch_shape + (3, 3)).copy()
    E[..., i, i] = R2[..., 0, 0]
    E[..., i, j] = R2[..., 0, 1]
    E[..., j, i] = R2[..., 1, 0]
    E[..., j, j] = R2[..., 1, 1]
    return E


def _sample_su2_heatbath(V2, k, beta, rng):
    """
    Sample the subgroup update matrix R2 for the Cabibbo–Marinari heat-bath.

    Effective coupling  xi = (2 beta / 3) k.  Draw x ∈ SU(2) with scalar a0 ~
    P(a0) ∝ sqrt(1-a0^2) exp(xi a0) (Creutz sampler), vector part uniform on the
    sphere of radius sqrt(1-a0^2).  The new subgroup matrix is  R2 = X2 · V2^dag
    (so the updated W-block ∝ X2).
    """
    xi = (2.0 / 3.0) * beta * k
    xi = np.maximum(xi, 1e-12)
    a0 = _creutz_a0(xi, rng)
    nrm = np.sqrt(np.maximum(1.0 - a0 * a0, 0.0))
    # uniform direction on S^2
    cos_t = 2.0 * rng.random(a0.shape) - 1.0
    sin_t = np.sqrt(np.maximum(1.0 - cos_t * cos_t, 0.0))
    phi = 2.0 * np.pi * rng.random(a0.shape)
    a1 = nrm * sin_t * np.cos(phi)
    a2 = nrm * sin_t * np.sin(phi)
    a3 = nrm * cos_t
    X2 = _quat_to_mat(a0, a1, a2, a3)
    return _mm(X2, _dag(V2))


def _creutz_a0(xi, rng):
    """
    Vectorised sampler for a0 ~ P(a0) ∝ sqrt(1-a0^2) exp(xi a0) on [-1,1].

    Proposal: a0 from the truncated exponential e^{xi a0} (inverse-CDF, stable
    for large xi), accept with probability sqrt(1-a0^2).  Masked resampling
    until all accepted.  Works for all xi>0.
    """
    a0 = np.empty(xi.shape)
    todo = np.ones(xi.shape, dtype=bool)
    while todo.any():
        x = xi[todo]
        u = rng.random(x.shape)
        # a0 = 1 + (1/xi) ln( u + (1-u) e^{-2 xi} )
        prop = 1.0 + np.log(u + (1.0 - u) * np.exp(-2.0 * x)) / x
        acc = rng.random(x.shape) < np.sqrt(np.maximum(1.0 - prop * prop, 0.0))
        idx = np.where(todo)[0] if todo.ndim == 1 else np.where(todo)
        # assign accepted
        sel = np.zeros_like(todo)
        sel[todo] = acc
        a0[sel] = prop[acc]
        todo[sel] = False
    return a0


def _su2_overrelax(V2):
    """Microcanonical over-relaxation subgroup matrix R2 = (V2^dag)^2 (preserves the action)."""
    Vd = _dag(V2)
    return _mm(Vd, Vd)


# ══════════════════════════════════════════════════════════════════
#  Sweeps: heat-bath and over-relaxation (checkerboard-vectorised)
# ══════════════════════════════════════════════════════════════════

def _parity_mask(L, D):
    """Boolean (L,)*D mask of even-parity sites (sum of coords even)."""
    grids = np.indices((L,) * D)
    return (grids.sum(axis=0) % 2) == 0


def _update_direction(U, mu, beta, rng, kind, reunit):
    """Update all U_mu links via checkerboard; kind in {'heatbath','overrelax'}."""
    D = U.shape[0]
    L = U.shape[1]
    even = _parity_mask(L, D)
    for par in (even, ~even):
        # Recompute the staple for each parity: R_mu(x) depends on neighbouring
        # mu-links (the U_mu(x+nu) factor), so the second parity must see the
        # links updated in the first.
        Sigma_full = staple_field(U, mu)
        Sig = Sigma_full[par]                  # (M,3,3) staple completion R
        for (i, j) in _SUBGROUPS:
            Umu = U[mu]
            Up = Umu[par]                      # (M,3,3)
            W = _mm(Up, Sig)                   # (M,3,3) = U·R, weight ∝ exp((β/N)ReTr W)
            w = W[:, [i, j], :][:, :, [i, j]]  # (M,2,2) subgroup block
            V2, k = _su2_from_block(w)
            if kind == 'heatbath':
                R2 = _sample_su2_heatbath(V2, k, beta, rng)
            else:
                R2 = _su2_overrelax(V2)
            E = _embed_su2(R2, i, j, (Up.shape[0],))
            Up_new = _mm(E, Up)
            Umu[par] = Up_new
            U[mu] = Umu
    if reunit:
        U[mu] = su3_project(U[mu])
    return U


def heatbath_sweep(U, beta, rng, n_or=0, reunit_every=True):
    """
    One full lattice sweep: for each direction, a pseudo-heat-bath update of
    both parities, optionally followed by `n_or` over-relaxation updates.
    """
    D = U.shape[0]
    for mu in range(D):
        U = _update_direction(U, mu, beta, rng, 'heatbath', reunit_every)
        for _ in range(n_or):
            U = _update_direction(U, mu, beta, rng, 'overrelax', reunit_every)
    return U


def thermalise(U, beta, rng, n_sweeps, n_or=1, record=False):
    """Run n_sweeps heat-bath(+OR) sweeps.  Returns (U, plaq_history)."""
    hist = []
    for _ in range(n_sweeps):
        U = heatbath_sweep(U, beta, rng, n_or=n_or)
        if record:
            hist.append(mean_plaquette(U))
    return U, hist


# ══════════════════════════════════════════════════════════════════
#  Observables: Wilson loops, Polyakov loop & correlator
# ══════════════════════════════════════════════════════════════════

def wilson_loop_planar(U, mu, nu, R, T):
    """
    ⟨(1/3) Re Tr W(R×T)⟩ averaged over all sites, planar loop in the (mu,nu)
    plane: R steps in +mu, T steps in +nu, R back, T back.  The loop based at
    every site is built by accumulating shifted link matrices (correctness over
    speed); `off` tracks the current corner offset so each leg picks up the link
    at the right site.
    """
    Umu, Unu = U[mu], U[nu]
    eye = np.broadcast_to(np.eye(3, dtype=complex), Umu.shape).copy()

    def roll_to(A, off):
        out = A
        for ax, s in enumerate(off):
            if s:
                out = np.roll(out, -s, axis=ax)
        return out

    acc = eye
    off = np.zeros(U.shape[0], dtype=int)
    for _ in range(R):                       # +mu
        acc = _mm(acc, roll_to(Umu, off));  off[mu] += 1
    for _ in range(T):                       # +nu
        acc = _mm(acc, roll_to(Unu, off));  off[nu] += 1
    for _ in range(R):                       # -mu
        off[mu] -= 1;  acc = _mm(acc, _dag(roll_to(Umu, off)))
    for _ in range(T):                       # -nu
        off[nu] -= 1;  acc = _mm(acc, _dag(roll_to(Unu, off)))
    return float(np.real(np.trace(acc, axis1=-2, axis2=-1)).mean() / 3.0)


def polyakov_loop_field(U, t_axis=None):
    """
    Polyakov loop P(x_spatial) = Tr prod_t U_t(x,t) around the periodic time
    direction.  Returns a complex array over the spatial sublattice.
    t_axis defaults to the last lattice axis (D).
    """
    D = U.shape[0]
    if t_axis is None:
        t_axis = D - 1               # last lattice axis
    Ut = U[t_axis]                   # (L,)*D + (3,3)
    L = U.shape[1]
    # ordered product over the time axis
    prod = np.take(Ut, 0, axis=t_axis)
    for t in range(1, L):
        prod = _mm(prod, np.take(Ut, t, axis=t_axis))
    return np.trace(prod, axis1=-2, axis2=-1)


def polyakov_correlator_direct(Pfield, R, space_axis=0):
    """
    ⟨P(x) P*(x+R)⟩ averaged over the spatial lattice, separation R along
    `space_axis`.  Pfield is the (spatial) Polyakov-loop field.
    """
    Pc = np.conj(np.roll(Pfield, -R, axis=space_axis))
    return complex(np.mean(Pfield * Pc))


# ══════════════════════════════════════════════════════════════════
#  Lüscher–Weisz two-level estimator for the Polyakov correlator
# ══════════════════════════════════════════════════════════════════
#
#  P(x) = Tr prod_b L_b(x),  L_b(x) = prod_{t in block b} U_t(x,t).
#  Two-level:  ⟨P(x)P*(y)⟩ = Tr_9 [ prod_b M_b(x,y) ],
#    M_b[(i,j),(i',j')] = ⟨ L_b(x)[i,i'] * conj(L_b(y)[j,j']) ⟩_sublattice,
#  a 9×9 matrix on the doubled colour index (i,j).  The sublattice average
#  freezes the spatial links on the time-slice boundaries between blocks and
#  updates only the interior with `n_sub` heat-bath sweeps.  Variances of the
#  blocks multiply (not add), beating the exponential signal/noise wall.


def polyakov_correlator_twolevel(U, beta, rng, R, n_blocks, n_sub,
                                 space_axis=0, t_axis=None, reunit=True):
    """
    Two-level (Lüscher–Weisz) estimate of ⟨P(0)P*(R)⟩ for ALL spatial source
    positions along `space_axis`, returned as the lattice-averaged correlator.

    The time extent T is split into `n_blocks` equal blocks of thickness
    dt = T/n_blocks.  For each block we freeze the spatial links on the block
    boundaries and run `n_sub` interior heat-bath sweeps, accumulating the
    doubled-index block tensor M_b for every (x, x+R) pair, then take the
    9×9 product over blocks and the colour trace.

    Returns (corr_complex, ) — real part is the physical correlator.

    Implementation note: this is a faithful but modest two-level (interior =
    everything except the boundary spatial links).  It is meant to *demonstrate*
    variance reduction and feed V(R); production statistics live in
    `run_lgt_confinement.py`.
    """
    D = U.shape[0]
    L = U.shape[1]
    if t_axis is None:
        t_axis = D - 1
    T = L
    if T % n_blocks != 0:
        raise ValueError("n_blocks must divide the time extent")
    dt = T // n_blocks
    spatial_axes = [ax for ax in range(D) if ax != t_axis]
    # spatial shape
    sp_shape = tuple(L for _ in spatial_axes)

    # Accumulate block tensors M_b for each block, averaged over n_sub sweeps.
    # M_b stored as (n_blocks, *sp_shape, 9, 9): row (i,j), col (i',j').
    Macc = [np.zeros(sp_shape + (9, 9), dtype=complex) for _ in range(n_blocks)]

    for _ in range(n_sub):
        # interior heat-bath update freezing boundary spatial links:
        _interior_update(U, beta, rng, n_blocks, dt, t_axis, reunit)
        for b in range(n_blocks):
            Lb = _block_transporter_field(U, b * dt, dt, t_axis, spatial_axes)  # (*sp,3,3)
            LbR = np.roll(Lb, -R, axis=space_axis)  # partner shifted by R (its own axis)
            # M[(i,j),(i',j')] = Lb[i,i'] * conj(LbR[j,j'])
            M = np.einsum('...ix,...jy->...ijxy', Lb, np.conj(LbR))
            M = M.reshape(sp_shape + (9, 9))
            Macc[b] += M
    for b in range(n_blocks):
        Macc[b] /= n_sub

    # 9×9 product over blocks (per spatial site), then trace_9.
    G = Macc[0]
    for b in range(1, n_blocks):
        G = np.einsum('...ab,...bc->...ac', G, Macc[b])
    corr_site = np.trace(G, axis1=-2, axis2=-1)
    return complex(np.mean(corr_site))


def _block_transporter_field(U, t0, dt, t_axis, spatial_axes):
    """L_b(x) over [t0,t0+dt) for every spatial site, returned (*sp_shape,3,3)."""
    Ut = U[t_axis]
    prod = np.take(Ut, t0, axis=t_axis)
    for t in range(t0 + 1, t0 + dt):
        prod = _mm(prod, np.take(Ut, t, axis=t_axis))
    return prod


def _interior_update(U, beta, rng, n_blocks, dt, t_axis, reunit):
    """
    One sublattice heat-bath sweep that freezes the spatial links on block
    boundaries (time slices t = b*dt) and updates everything else.  Temporal
    links are always free; spatial links are frozen on the boundary slices.
    """
    D = U.shape[0]
    L = U.shape[1]
    boundary = set(b * dt for b in range(n_blocks))
    even = _parity_mask(L, D)
    for mu in range(D):
        # build a freeze-mask over sites: for spatial mu, freeze sites whose
        # time coordinate is a block boundary.
        if mu == t_axis:
            freeze = np.zeros((L,) * D, dtype=bool)     # temporal links always free
        else:
            tcoord = np.indices((L,) * D)[t_axis]
            freeze = np.isin(tcoord, list(boundary))
        for par in (even, ~even):
            Sigma_full = staple_field(U, mu)            # recompute per parity
            mask = par & (~freeze)
            if not mask.any():
                continue
            Sig = Sigma_full[mask]
            for (i, j) in _SUBGROUPS:
                Umu = U[mu]
                Up = Umu[mask]
                W = _mm(Up, Sig)
                w = W[:, [i, j], :][:, :, [i, j]]
                V2, k = _su2_from_block(w)
                R2 = _sample_su2_heatbath(V2, k, beta, rng)
                E = _embed_su2(R2, i, j, (Up.shape[0],))
                Umu[mask] = _mm(E, Up)
                U[mu] = Umu
        if reunit:
            U[mu] = su3_project(U[mu])
    return U


# ══════════════════════════════════════════════════════════════════
#  Static potential helpers
# ══════════════════════════════════════════════════════════════════

def static_potential_from_polyakov(corr_R, T):
    """V(R) = -(1/T) ln C(R)  from the Polyakov correlator (time extent T)."""
    c = np.real(corr_R)
    if c <= 0:
        return float('nan')
    return float(-np.log(c) / T)


def strong_coupling_sigma(beta):
    """Leading 4D strong-coupling string tension  sigma ≈ -ln(beta/18)."""
    return float(-np.log(beta / 18.0))


def fit_linear_plus_coulomb(Rs, Vs):
    """
    Least-squares fit  V(R) = mu + sigma R - e/R.  Returns dict(mu,sigma,e).
    Needs >=3 R points.  Pure-numpy normal equations.
    """
    Rs = np.asarray(Rs, dtype=float)
    Vs = np.asarray(Vs, dtype=float)
    A = np.vstack([np.ones_like(Rs), Rs, -1.0 / Rs]).T
    coef, *_ = np.linalg.lstsq(A, Vs, rcond=None)
    mu, sigma, e = coef
    resid = float(np.sqrt(np.mean((A @ coef - Vs) ** 2)))
    return {'mu': float(mu), 'sigma': float(sigma), 'e': float(e), 'rms': resid}
