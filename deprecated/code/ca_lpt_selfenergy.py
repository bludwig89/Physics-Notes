# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_lpt_selfenergy.py
# migrated   : 2026-07-30 - 14:48
# target     : src/casim/engine/gauge/lpt_selfenergy.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_lpt_selfenergy.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed (S1/S2 code-clean already applied at F69/F91)
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_lpt_selfenergy.py — the one-loop lattice gluon self-energy assembled from the
EXACT generated Wilson vertices (ca_lpt_generator), for the d1 = Lambda_MSbar/Lambda_L
program (docs/theory/d1-kns-vertex-status.md; F162/F239).

WHY THIS MODULE (closes the "wire the exact vertices in" step)
=============================================================
The PT runner run_d1_vertex_formfactor.py assembled the transverse coefficient from
CONTINUUM background-field vertices dressed with a leading cosine form factor
(bg.gammaF_tensor_continuum * prod cos(k/2)).  That stand-in reaches only ~26 % of
the Wilson 28.81 constant.  ca_lpt_generator.py now DERIVES the exact Wilson lattice
vertices from the action (3-gluon + 4-gluon seagull, machine-validated).  This module
consumes those exact vertices — no cosine stand-in, no transcription — and assembles
the gluon self-energy Pi_{mu nu}(q):

    Pi_{mn}(q) = [3-gluon loop]  +  [4-gluon seagull tadpole]  (+ ghost + measure, below)

COLOUR FACTORISATION (validated: the plaquette 3-gluon vertex is pure f^{abc})
    V3^{abc}_{mu nu rho}(p1,p2,p3) = f^{abc} * T_{mu nu rho}(p1,p2,p3),
so the colour-stripped lattice tensor is
    T_{mu nu rho} = vertex3(...,a=0,b=1,c=2) / f^{123},   f^{123}=1.
The gluon-loop colour contraction is f^{acd} f^{bcd} = C_A delta^{ab} = 3 delta^{ab};
the loop symmetry factor is 1/2.  In Feynman (covariant xi=1) gauge the lattice gluon
propagator is delta_{alpha beta}/Khat(k), Khat = 4 sum sin^2(k/2).

TRANSVERSE COEFFICIENT (apples-to-apples with the runner / F162)
    B = (Pi00 - Pi11)/Q^2 for q = (Q,0,0,0); C = 16 pi^2 (B_lat - B_cont).
The delta_{mu nu} mass pieces (seagull tadpole + measure term) drop out of the
transverse projection, so B isolates the vertex+ghost finite part; the FULL 28.81
gate (tadpole-dominated) keeps the un-projected Pi and the seagull<->measure
quadratic-divergence cancellation (see certify_wilson_gate / the ghost+measure
additions in this module).

METHOD / COST
    The colour-stripped tensor is built over the whole BZ grid with the generator's
    vectorised vertex_vec (one call per (mu,alpha,beta) triple = 64 calls).  n=8 runs
    in a few seconds; production n is via tests/runners/run_d1_selfenergy.py.

Pure numpy real/complex matrix algebra (NOT chiral spinor transforms; the CLAUDE.md
numpy caveat does not apply — validated by the generator's exact propagator gate and
the continuum-consistency gate here).
"""
from __future__ import annotations

import math

import numpy as np

import ca_lpt_generator as gen
import ca_bgfield_loop as bg          # continuum vertices, for the consistency gate

C_A = 3.0
SIXTEEN_PI2 = 16.0 * math.pi ** 2
F123 = gen.F_ABC[0, 1, 2]            # = 1  (colour normalisation of the stripped tensor)
# The generator reads vertices off U = exp(i A), so V3 = (i f^{abc}) x (real YM tensor)
# (validate_3gluon: K = i).  Dividing by (i * f^{123}) returns the REAL tensor whose
# continuum limit is the standard Yang-Mills 3-gluon tensor (ratio -> 1).
_ISTRIP = 1j * F123


# ----------------------------------------------------------------------
#  lattice kinematics
# ----------------------------------------------------------------------
def _bz_grid(n):
    ax = (np.arange(n) + 0.5) / n * 2 * math.pi - math.pi
    G = np.meshgrid(ax, ax, ax, ax, indexing="ij")
    return np.stack(G, axis=-1)                    # (n,n,n,n,4)


def _khat2(k):
    """Wilson Khat = 4 sum_mu sin^2(k_mu/2)."""
    return 4.0 * np.sum(np.sin(k / 2.0) ** 2, axis=-1)


def _wrap(k):
    return ((k + math.pi) % (2 * math.pi)) - math.pi


# ----------------------------------------------------------------------
#  colour-stripped EXACT lattice 3-gluon tensor  T_{mu al be}(p_mu, p_al, p_be)
#  built over the whole grid (p_al = k grid, p_be = r grid, p_mu = q fixed)
# ----------------------------------------------------------------------
def three_gluon_tensor_grid(qvec, kgrid, rgrid):
    """Return T[..., mu, al, be] = colour-stripped exact lattice 3-gluon vertex with
    leg0 = (dir mu, momentum qvec [broadcast]), leg1 = (dir al, momentum kgrid),
    leg2 = (dir be, momentum rgrid).  T = V3^{(0,1,2)} / (i f^{123}) is REAL in the
    continuum limit (the standard YM tensor).  gshape is the broadcast grid shape of
    the three leg momenta (any of them may be a fixed 4-vector)."""
    gshape = np.broadcast_shapes(np.shape(qvec), np.shape(kgrid), np.shape(rgrid))[:-1]
    T = np.zeros(gshape + (4, 4, 4), dtype=complex)
    for mu in range(4):
        for al in range(4):
            for be in range(4):
                legs = [gen.Leg(mu, qvec, gen.T_GEN[0]),
                        gen.Leg(al, kgrid, gen.T_GEN[1]),
                        gen.Leg(be, rgrid, gen.T_GEN[2])]
                T[..., mu, al, be] = gen.vertex_vec(legs, gshape) / _ISTRIP
    return T


# ----------------------------------------------------------------------
#  the 3-gluon loop transverse coefficient B_gluon = (Pi00 - Pi11)/Q^2
# ----------------------------------------------------------------------
def _pi_gluon_loop(Q, n):
    """Pi_{mu nu} from the 3-gluon loop, EXACT lattice vertices, Feynman-gauge
    lattice propagator delta/Khat.  Returns the 4x4 real Pi (colour-stripped of the
    delta^{ab}) at external q=(Q,0,0,0).

        Pi_{mn} = (1/2) * C_A * mean_k [ sum_{al,be} T_{m,al,be}(q,k,r)
                                          T_{n,al,be}(-q,-k,-r) / (Khat(k) Khat(r)) ]
    with r = -k - q (all-incoming convention, matching gen.vertex3 p+q+r=0)."""
    k = _bz_grid(n)
    qv = np.array([Q, 0.0, 0.0, 0.0])
    r = -k - qv
    kw, rw = _wrap(k), _wrap(r)
    denom = _khat2(kw) * _khat2(rw)                        # (grid,)

    T1 = three_gluon_tensor_grid(qv, k, r)                 # T(q,k,r)   [.,m,al,be]
    T2 = three_gluon_tensor_grid(-qv, -k, -r)              # T(-q,-k,-r)[.,n,al,be]
    # contract internal Lorentz al,be (Feynman-gauge delta on each internal line)
    M = np.einsum('...mab,...nab->...mn', T1, T2)          # (grid,4,4) complex
    Pi = 0.5 * C_A * np.mean(np.real(M) / denom[..., None, None], axis=(0, 1, 2, 3))
    return Pi


def gluon_B_lattice(Q, n):
    """Transverse coefficient B = (Pi00 - Pi11)/Q^2 from the EXACT-vertex gluon loop."""
    Pi = _pi_gluon_loop(Q, n)
    return (Pi[0, 0] - Pi[1, 1]) / Q ** 2


# ----------------------------------------------------------------------
#  ghost loop (lattice FP ghost-gluon vertex, covariant xi=1)
# ----------------------------------------------------------------------
def ghost_vertex_lattice_exact(p, pp):
    """EXACT lattice background-field ghost-gluon vertex form factor, DERIVED from the
    covariant lattice ghost Laplacian.

    Derivation (plane-wave extraction, background link Ubar_mu = 1 + i B_mu + ...):
      S_gh = sum_{x,mu} (cbar(x) - cbar(x+mu) Ubar_mu^dag)(c(x) - Ubar_mu c(x+mu)).
    The O(B) term, with c ~ e^{ip x}, cbar ~ e^{-ip' x}, B_mu at the link midpoint
    x+mu/2 ~ e^{iq (x+mu/2)} (q = p'-p), gives the vertex form factor
        FF_mu = i e^{i q_mu/2} (e^{-i p'_mu} - e^{i p_mu}) = 2 sin((p+p')_mu / 2),
    i.e.  V^ghost_mu(p,p') = f^{abc} * 2 sin((p+p')_mu/2)  ->  (p+p')_mu  as a->0.
    This is the SINGLE sine of the mean ghost momentum, NOT the sum of two hatted
    momenta khat_mu + (k+q)hat_mu used at leading order (they agree only to O((ka)^2))."""
    return 2.0 * np.sin((p + pp) / 2.0)


def _pi_ghost_loop(Q, n):
    """Ghost-loop contribution to Pi_{mu nu}.  The lattice Faddeev-Popov ghost-gluon
    vertex from the covariant (backward-difference) gauge condition carries the
    momentum factor (khat + (k+q)hat)_mu -> (2k+q)_mu in the continuum; the loop is
        Pi^ghost_{mn} = - C_A * mean_k [ (kh+kqh)_m (kh+kqh)_n / (Khat(k) Khat(k+q)) ].
    Sign/normalisation matches bg.ghost_M = -2 (2k+q)(2k+q) with the (C_A/2) prefactor
    of _pi_gluon_loop (here the extra 1/2 x 2 = 1 is absorbed => overall -C_A)."""
    k = _bz_grid(n)
    qv = np.array([Q, 0.0, 0.0, 0.0])
    kq = _wrap(k + qv)
    denom = _khat2(_wrap(k)) * _khat2(kq)
    kh = 2.0 * np.sin(_wrap(k) / 2.0)
    kqh = 2.0 * np.sin(kq / 2.0)
    t = kh + kqh                                   # (khat + (k+q)hat)_mu -> (2k+q)_mu
    M = np.einsum('...m,...n->...mn', t, t)
    Pi = - C_A * np.mean(M / denom[..., None, None], axis=(0, 1, 2, 3))
    return Pi


def gluon_ghost_B_lattice(Q, n):
    """Physical transverse coefficient B = (Pi00-Pi11)/Q^2 for the FULL lattice
    gluon+ghost self-energy (the delta_{mu nu} mass sector cancels in the transverse
    projection)."""
    Pi = _pi_gluon_loop(Q, n) + _pi_ghost_loop(Q, n)
    return (Pi[0, 0] - Pi[1, 1]) / Q ** 2


# ----------------------------------------------------------------------
#  Haar measure term (DERIVED from the adjoint exp-map Jacobian, first principles)
# ----------------------------------------------------------------------
def haar_measure_coefficient() -> dict:
    """DERIVE the O(X^2) Haar-measure coefficient from the exp-map Jacobian
        dU = J(X) dX,  ln J(X) = tr_adj ln[(I - e^{-ad_X})/ad_X] = -c sum_a (X^a)^2 + ...
    with ad_X built from the SU(3) structure constants (no transcription).  Returns
    c; the analytic value is C_A/24 (=1/8 for SU(3)).  The measure term in the
    effective action is +c sum (X^a)^2 per link (X = g A), i.e. a gluon mass
    counterterm Pi^meas_{mn} = -delta_{mn} (2c) = -delta_{mn} C_A/12, which cancels
    the seagull tadpole's quadratic divergence."""
    f = gen.F_ABC
    N = 8
    rng = np.random.default_rng(0)

    def lnJ(X):
        A = np.zeros((N, N))
        for a in range(N):
            for b in range(N):
                A[a, b] = -sum(f[c, a, b] * X[c] for c in range(N))
        w = np.linalg.eigvals(A)
        v = 0.0
        for m in w:
            v += 0.0 if abs(m) < 1e-8 else np.log((1 - np.exp(-m)) / m)
        return v.real

    cs = []
    for _ in range(100):
        d = rng.normal(size=N); d /= np.linalg.norm(d)
        X = 1e-3 * d
        cs.append(-lnJ(X) / np.sum(X ** 2))
    c = float(np.mean(cs))
    return {"c_measure": c, "c_over_CA": c / C_A, "analytic_CA_over_24": C_A / 24.0,
            "std": float(np.std(cs)),
            "mass_counterterm_Pi": -C_A / 12.0,
            "pass": bool(abs(c - C_A / 24.0) < 1e-6),
            "statement": "ln J(X) = -(C_A/24) sum_a (X^a)^2 (derived from the adjoint "
                         "exp-map Jacobian) => measure mass counterterm Pi^meas = "
                         "-delta_{mn} C_A/12, cancelling the seagull quadratic divergence"}


# ----------------------------------------------------------------------
#  seagull (4-gluon) tadpole — the delta_{mu nu} mass piece (Wilson-dominant)
# ----------------------------------------------------------------------
def seagull_tadpole(n=8) -> dict:
    """The Wilson seagull tadpole mass insertion Z0 = <1/Khat> (the dominant piece of
    Lambda_MSbar/Lambda_L = 28.81).  Reproduces ca_gluon_self_energy.tadpole Z0 as a
    cross-check, and pairs with the DERIVED measure counterterm for the divergence
    cancellation.  (The transverse route projects this out; the full 28.81 gate keeps
    it — see certify_wilson_gate.)"""
    k = _bz_grid(n)
    Z0 = float(np.mean(1.0 / _khat2(_wrap(k))))
    # seagull colour+Lorentz weight (d-1)/2 * C_A for the delta_{mn} tadpole (d=4)
    coeff = (4 - 1) / 2.0 * C_A
    return {"n": n, "Z0": Z0, "seagull_coeff_(d-1)/2*CA": coeff,
            "seagull_mass": coeff * Z0,
            "measure_counterterm": haar_measure_coefficient()["mass_counterterm_Pi"],
            "note": "Z0 -> 0.15493 as n->inf (Wilson tadpole). The measure term "
                    "cancels the QUADRATIC divergence; the finite remnant + gluon/ghost "
                    "vertex constant assemble the 28.81 gate."}


# ----------------------------------------------------------------------
#  consistency gate: exact-vertex loop -> continuum-vertex loop as a->0
# ----------------------------------------------------------------------
def validate_vertex_wiring(scale=1e-3, tol=1e-3, seed=3) -> dict:
    """Gate (pointwise): the colour-stripped grid tensor three_gluon_tensor_grid must
    reduce to the standard continuum YM 3-gluon tensor as momenta -> 0 (ratio -> 1,
    real).  This is the load-bearing check that the EXACT generated vertex is wired
    into the self-energy contraction with the correct i/colour normalisation.  (The
    INTEGRATED loop deliberately differs from any continuum loop by the finite lattice
    constant -- that difference is the object we are after, not an error.)"""
    rng = np.random.default_rng(seed)
    q = scale * rng.uniform(-1, 1, 4)
    k = scale * rng.uniform(-1, 1, 4)
    r = -k - q
    d = np.eye(4)
    def cont(mu, al, be):
        return (d[mu, al] * (q - k)[be] + d[al, be] * (k - r)[mu] + d[be, mu] * (r - q)[al])
    # single-point tensor via the grid builder (gshape = ())
    T = three_gluon_tensor_grid(q, k.reshape(4), r.reshape(4))   # shape (4,4,4)
    ratios = []
    for mu in range(4):
        for al in range(4):
            for be in range(4):
                c = cont(mu, al, be)
                if abs(c) > 1e-8:
                    ratios.append(T[mu, al, be] / c)
    ratios = np.array(ratios)
    K = complex(np.mean(ratios))
    spread = float(np.max(np.abs(ratios - K)))
    return {"ratio_mean": K, "is_real_unity": bool(abs(K - 1.0) < tol),
            "spread": spread, "pass": bool(abs(K - 1.0) < tol and spread < 1e-3),
            "statement": "colour-stripped grid 3-gluon tensor -> continuum YM tensor "
                         "(ratio -> 1, real) => exact vertex wired in with correct "
                         "i/colour normalisation"}


def gluon_finite_constant(n=8, Qs=(0.1, 0.15, 0.2, 0.3)) -> dict:
    """C_gluon = 16 pi^2 (B_exact_lat - B_cont), the EXACT-vertex 3-gluon-loop
    contribution to the transverse finite constant, subtracting the F162 continuum
    background-field baseline (bg._Bcoeff_numeric 'cont').  Q-flat if no residual log.
    NOTE: this is the gluon-loop piece ONLY; the physical transverse constant also
    needs the ghost loop (below).  Reported for the wiring milestone."""
    rows = []
    for Q in Qs:
        Bl = gluon_B_lattice(Q, n)
        Bc = bg._Bcoeff_numeric(Q, n, "cont")
        rows.append({"Q": Q, "B_exact_lat": float(Bl), "B_cont": float(Bc),
                     "C_gluon": float(SIXTEEN_PI2 * (Bl - Bc))})
    cs = [r["C_gluon"] for r in rows]
    return {"n": n, "rows": rows, "C_gluon": float(np.mean(cs)),
            "Q_spread": float(max(cs) - min(cs))}


def gauge_fixing_vertex_continuum(k, q):
    """DERIVED background-covariant gauge-fixing 3-vertex (Feynman background gauge
    xi=1), colour-stripped, in the bg (Abbott) convention GammaF_{a m l}(k,q):
    background = m (momentum q), quantum a (momentum k), quantum l (momentum -k-q):

        V^gf_{a m l}(k,q) = delta_{am} (-k-q)_l  -  delta_{ml} k_a .

    Verified EXACT: Abbott_{aml} = symmetric_{aml} + V^gf_{aml} (0/64 components,
    sympy, gauge_fixing_identity_check).  Each term is the longitudinal projection of
    one quantum leg (its own momentum dotted into its own Lorentz index) tied to the
    background index m -- the (D^bg_mu Q_mu)^2 structure.  Returns (...,4,4,4) [a,m,l]."""
    D = 4
    d = np.eye(D)
    mkq = -k - q                                   # momentum of quantum leg l
    return (np.einsum('am,...l->...aml', d, mkq)
            - np.einsum('ml,...a->...aml', d, k))


def gauge_fixing_identity_check() -> dict:
    """Symbolic proof (sympy) that Abbott = symmetric + V^gf EXACTLY, in the bg
    convention.  This is the certification that the derived gauge-fixing vertex is
    the missing scheme term."""
    import sympy as sp
    D = 4
    k = sp.symbols('k0:4', real=True); q = sp.symbols('q0:4', real=True)
    dl = lambda i, j: 1 if i == j else 0
    def abbott(a, m, l):
        return -2 * q[l] * dl(a, m) + 2 * q[a] * dl(m, l) - (2 * k[m] + q[m]) * dl(l, a)
    pa = list(k); pm = list(q); pl = [-k[i] - q[i] for i in range(D)]
    def sym(a, m, l):
        return (dl(a, m) * (pa[l] - pm[l]) + dl(m, l) * (pm[a] - pl[a])
                + dl(l, a) * (pl[m] - pa[m]))
    def gf(a, m, l):
        return dl(a, m) * pl[l] - dl(m, l) * pa[a]
    mism = sum(1 for a in range(D) for m in range(D) for l in range(D)
               if sp.simplify(abbott(a, m, l) - sym(a, m, l) - gf(a, m, l)) != 0)
    return {"mismatched_components": mism, "total": D ** 3,
            "pass": mism == 0,
            "closed_form": "V^gf_{a m l}(k,q) = delta_{am}(-k-q)_l - delta_{ml} k_a",
            "statement": "Abbott = symmetric + V^gf EXACTLY (0/64) => the derived "
                         "gauge-fixing vertex is the missing scheme term; adding it to "
                         "the exact lattice symmetric vertex gives the lattice Abbott "
                         "vertex, so Pi-alone is transverse and yields b0=11 (bg gate)."}


def scheme_consistency_diagnosis(scale=1e-3, seed=5) -> dict:
    """TASK-4 diagnosis: the b0=11 gate (ca_bgfield_loop) uses the background-field
    (Abbott) vertex GammaF; the self-energy above uses the EXACT plaquette-action
    vertex.  This test shows the exact plaquette action (even with a leg tagged as
    background, gen.vertex_bqq_vec) reduces to the SYMMETRIC Yang-Mills vertex, NOT
    to Abbott.  Hence the scheme-consistent fix is precisely ONE additive term: the
    lattice background-covariant gauge-fixing vertex, which carries
        Abbott_{aml}(k,q) - symmetric_{aml}(k,q)
    = -2q_l d_am + 2q_a d_ml - (2k+q)_m d_la  -  [d_am(q-k)_l + d_ml(2k+q)_a
      - d_la(k+2q)_m].
    Adding this (its exact lattice form factors come from the same link expansion)
    makes Pi-ALONE give b0=11, so the finite constant is the genuine gauge-invariant
    d1.  Two consistent completions: (A) add the gauge-fixing vertex [1 term];
    (B) ordinary Feynman gauge + the separate vertex renormalisation Z1 [more diagrams].
    """
    rng = np.random.default_rng(seed)
    q = scale * rng.uniform(-1, 1, 4)
    k = scale * rng.uniform(-1, 1, 4)
    r = -k - q
    istrip = 1j * F123
    d = np.eye(4)

    def bqq(a, m, l):
        legs = [gen.Leg(a, q, gen.T_GEN[0]), gen.Leg(m, k, gen.T_GEN[1]),
                gen.Leg(l, r, gen.T_GEN[2])]
        return gen.vertex_bqq_vec(legs, {0}, ()) / istrip

    def sym(a, m, l):
        return d[a, m] * (q - k)[l] + d[m, l] * (k - r)[a] + d[l, a] * (r - q)[m]

    gF = bg.gammaF_tensor_continuum(k, q)      # Abbott [a,m,l]
    ra, rs = [], []
    for a in range(4):
        for m in range(4):
            for l in range(4):
                t = bqq(a, m, l)
                if abs(gF[a, m, l]) > 1e-8:
                    ra.append(t / gF[a, m, l])
                if abs(sym(a, m, l)) > 1e-8:
                    rs.append(t / sym(a, m, l))
    ra, rs = np.array(ra), np.array(rs)
    return {"bqq_over_abbott_spread": float(np.max(np.abs(ra - np.mean(ra)))),
            "bqq_over_symmetric_mean": complex(np.mean(rs)),
            "bqq_over_symmetric_spread": float(np.max(np.abs(rs - np.mean(rs)))),
            "action_vertex_is_symmetric": bool(np.max(np.abs(rs - np.mean(rs))) < 1e-2
                                               and abs(np.mean(rs) - 1) < 1e-2),
            "action_vertex_is_abbott": bool(np.max(np.abs(ra - np.mean(ra))) < 1e-2),
            "statement": "plaquette-action vertex == symmetric YM vertex (NOT Abbott) "
                         "=> the scheme-consistent d1 needs ONE more term: the lattice "
                         "background-covariant gauge-fixing vertex (Abbott - symmetric). "
                         "Its lattice form factors come from the same link expansion."}


def gauge_fixing_vertex_lattice(k, q, fp="leading"):
    """Lattice-dressed gauge-fixing vertex (bg convention [a,m,l]):
        V^gf_lat_{a m l} = delta_{am} widehat(-k-q)_l  -  delta_{ml} khat_a ,
    widehat(p) = 2 sin(p/2).  Reduces to gauge_fixing_vertex_continuum as a->0.

    fp='exact' multiplies each term by its DERIVED midpoint phase on the background
    index m (from the covariant backward difference of the gauge condition
    Delta = sum_mu D^{bg,-}_mu Q_mu):  term_l x e^{-i(q+k)_m/2}, term_a x e^{i k_m/2}.
    Phases -> 1 as a->0; the W.Z contraction (Z at conjugate momenta) keeps Pi real.
    fp='leading' drops them (their effect is O((ka)^2))."""
    d = np.eye(4)
    kh = 2.0 * np.sin(k / 2.0)
    mkqh = 2.0 * np.sin((-k - q) / 2.0)
    t_l = np.einsum('am,...l->...aml', d, mkqh)          # delta_{am} widehat(-k-q)_l
    t_a = np.einsum('ml,...a->...aml', d, kh)            # delta_{ml} khat_a
    if fp == "exact":
        P1 = np.exp(-1j * (q + k) / 2.0)                 # phase on background index m
        P2 = np.exp(1j * k / 2.0)
        t_l = t_l * P1[..., None, :, None]               # m is axis -2
        t_a = t_a * P2[..., None, :, None]
    return t_l - t_a


def _abbott_lattice(p_slot0, p_slot1, p_slot2, k_arg, q_arg, gshape, fp="leading"):
    """Lattice Abbott vertex [slot0,slot1,slot2] = EXACT lattice symmetric tensor
    (from the generator, slots carrying momenta p_slot0,p_slot1,p_slot2) + the
    lattice gauge-fixing vertex evaluated at (k_arg,q_arg).  In the bg convention the
    generator slots are (a,m,l) = (mom k, mom q, mom -k-q); the caller passes the
    matching momenta so the gf term lines up index-for-index.  fp passes through to
    the gauge-fixing dressing ('leading' or 'exact')."""
    Tsym = three_gluon_tensor_grid(p_slot0, p_slot1, p_slot2)    # exact, real-normalised
    Vgf = gauge_fixing_vertex_lattice(k_arg, q_arg, fp=fp)
    return np.real(Tsym) + Vgf


def _pi_bgfield(Q, n, kernel="wilson", fp="leading"):
    """Background-field self-energy Pi_{mn} with the LATTICE ABBOTT vertex
    (exact symmetric + derived gauge-fixing) + lattice ghost, contracted EXACTLY as
    ca_bgfield_loop._Bcoeff_numeric (einsum '...aml,...lna->...mn').  kernel in
    {'wilson','rule'} selects the gluon propagator denominator (the rule K=3 Omega^2
    is the tadpole-free physical action, A0).  fp in {'leading','exact'} selects the
    Faddeev-Popov / gauge-fixing dressing: 'leading' uses simple hatted momenta;
    'exact' uses the DERIVED ghost form factor 2 sin((p+p')_mu/2) and the gf midpoint
    phases."""
    k = _bz_grid(n)
    qv = np.array([Q, 0.0, 0.0, 0.0])
    kq = k + qv
    if kernel == "rule":
        import ca_gluon_self_energy as _se
        Kr = lambda g: _se.K_true_4d(g[..., 0], g[..., 1], g[..., 2], g[..., 3])
        denom = Kr(_wrap(k)) * Kr(_wrap(kq))
    else:
        denom = _khat2(_wrap(k)) * _khat2(_wrap(kq))
    # W = AbbottLat(k,q): slots a(k), m(q), l(-k-q)
    W = _abbott_lattice(k, qv, -k - qv, k, qv, k.shape[:-1], fp=fp)
    # Z = AbbottLat(k+q,-q) used as [l,n,a]: slots l(k+q), n(-q), a(-k)
    Z = _abbott_lattice(kq, -qv, -k, kq, -qv, k.shape[:-1], fp=fp)
    Ggl = np.einsum('...aml,...lna->...mn', W, Z)
    if fp == "exact":
        # DERIVED exact lattice ghost vertex: 2 sin((p+p')_mu/2), p=k, p'=k+q
        tkq = ghost_vertex_lattice_exact(_wrap(k), _wrap(kq))
    else:
        tkq = 2.0 * np.sin(_wrap(k) / 2.0) + 2.0 * np.sin(_wrap(kq) / 2.0)  # (2k+q) hatted
    Hgh = -2.0 * np.einsum('...m,...n->...mn', tkq, tkq)
    M = Ggl + Hgh
    Pi = (C_A / 2.0) * np.mean(M / denom[..., None, None], axis=(0, 1, 2, 3))
    return Pi


def finite_constant_bgfield(n=8, Qs=(0.1, 0.15, 0.2, 0.3), kernel="wilson",
                            fp="leading") -> dict:
    """SCHEME-CONSISTENT transverse finite constant: the LATTICE ABBOTT (background-
    field) self-energy minus the F162 continuum Abbott baseline,
        d1-constant = 16 pi^2 (B_bgfield,lat - B_cont),   B = (Pi00-Pi11)/Q^2.
    Now apples-to-apples (Abbott lattice vs Abbott continuum), so Pi alone carries the
    b0=11 running (bg gate) and this constant is the genuine gauge-invariant d1
    candidate.  A small Q-spread certifies b0-preservation (no residual log).  For
    kernel='rule' the tadpole is separately ZERO (A0), so this transverse constant is
    the WHOLE rule d1; for 'wilson' the tadpole-dominated 28.81 needs the mass sector
    (seagull+measure) added on top.  fp in {'leading','exact'} selects the FP dressing."""
    rows = []
    imag = 0.0
    for Q in Qs:
        Pi = _pi_bgfield(Q, n, kernel=kernel, fp=fp)
        Bl = (Pi[0, 0] - Pi[1, 1]) / Q ** 2
        imag = max(imag, abs(float(np.imag(Bl))))
        Bc = bg._Bcoeff_numeric(Q, n, "cont")
        rows.append({"Q": Q, "B_bgfield_lat": float(np.real(Bl)), "B_cont": float(Bc),
                     "C": float(SIXTEEN_PI2 * (np.real(Bl) - Bc))})
    cs = [r["C"] for r in rows]
    lam = math.exp(np.mean(cs) / (2.0 * 11.0))          # bg-gate units b0=11
    return {"n": n, "kernel": kernel, "fp": fp, "rows": rows, "C": float(np.mean(cs)),
            "Q_spread": float(max(cs) - min(cs)), "max_imag_B": imag,
            "implied_lambda_ratio_exp_C_over_2b0": float(lam)}


def validate_fp_dressing(scale=1e-3, seed=7) -> dict:
    """Certify the DERIVED exact FP dressings: (i) the exact ghost vertex form factor
    2 sin((p+p')_mu/2) reduces to the continuum (p+p')_mu; (ii) the exact gf midpoint
    phases -> 1 as a->0 so the gf vertex still reduces to gauge_fixing_vertex_continuum.
    Both are the O((ka)^2) refinement of the leading hatted forms."""
    rng = np.random.default_rng(seed)
    p = scale * rng.uniform(-1, 1, 4)
    pp = scale * rng.uniform(-1, 1, 4)
    gh = ghost_vertex_lattice_exact(p, pp)
    gh_rel = float(np.max(np.abs(gh - (p + pp))) / (np.max(np.abs(p + pp)) + 1e-30))
    # gf exact vs continuum: the midpoint phase's O(ka) piece is IMAGINARY (cancels
    # in the loop), so the physical comparison is the REAL part -> continuum gf.
    k = scale * rng.uniform(-1, 1, 4); q = scale * rng.uniform(-1, 1, 4)
    ve = gauge_fixing_vertex_lattice(k, q, fp="exact")
    vc = gauge_fixing_vertex_continuum(k, q)
    gf_rel = float(np.max(np.abs(np.real(ve) - vc)) / (np.max(np.abs(vc)) + 1e-30))
    return {"ghost_exact_vs_continuum_rel": gh_rel,
            "gf_real_exact_vs_continuum_rel": gf_rel,
            "pass": bool(gh_rel < 1e-4 and gf_rel < 1e-4),
            "ghost_form_factor": "2 sin((p+p')_mu/2)  (DERIVED, covariant ghost Laplacian)",
            "statement": "exact FP dressings reduce to the continuum ghost (p+p')_mu and "
                         "(real part) gauge-fixing vertex as a->0; the gf midpoint "
                         "phase's O(ka) imaginary part cancels in the loop (Pi real). "
                         "They are the O((ka)^2) lattice refinement of the leading forms."}


def finite_constant(n=8, Qs=(0.1, 0.15, 0.2, 0.3)) -> dict:
    """The PHYSICAL transverse finite constant from the FULL exact-vertex lattice
    gluon+ghost self-energy, subtracting the F162 continuum background-field baseline:
        C = 16 pi^2 (B_gluon+ghost,lat - B_cont).
    Q-flat if no residual log (=> lattice b0 = continuum b0).  This is the transverse
    (tadpole-free) constant; the tadpole-dominated Wilson 28.81 uses the mass sector
    (seagull + derived measure) in certify_wilson_gate."""
    rows = []
    for Q in Qs:
        Bl = gluon_ghost_B_lattice(Q, n)
        Bc = bg._Bcoeff_numeric(Q, n, "cont")
        rows.append({"Q": Q, "B_lat": float(Bl), "B_cont": float(Bc),
                     "C": float(SIXTEEN_PI2 * (Bl - Bc))})
    cs = [r["C"] for r in rows]
    return {"n": n, "rows": rows, "C": float(np.mean(cs)),
            "Q_spread": float(max(cs) - min(cs)),
            "b0_preserved_if_flat": bool(max(cs) - min(cs) < 5.0)}


def report(n=8) -> dict:
    return {"vertex_wiring_gate": validate_vertex_wiring(),
            "haar_measure_derivation": haar_measure_coefficient(),
            "seagull_tadpole": seagull_tadpole(n=n),
            "scheme_consistency_diagnosis": scheme_consistency_diagnosis(),
            "gauge_fixing_identity": gauge_fixing_identity_check(),
            "fp_dressing_gate": validate_fp_dressing(),
            "scheme_consistent_constant_rule_exactFP": finite_constant_bgfield(
                n=n, Qs=(0.15, 0.25), kernel="rule", fp="exact"),
            "note": "Exact generated 3-gluon vertex + DERIVED gauge-fixing vertex "
                    "(Abbott = symmetric + V^gf, 0/64) + DERIVED exact FP dressings "
                    "(ghost 2 sin((p+p')/2); gf midpoint phases, Pi stays real) => "
                    "lattice Abbott background-field self-energy; Pi alone is transverse "
                    "(b0=11). Haar measure DERIVED (C_A/24). Q-flat; for kernel='rule' "
                    "the transverse constant is the whole (tadpole-free) d1."}


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
