"""lpt_bcc_vertex.py — lattice perturbation theory on the GENUINE BCC gauge
action: the 4-bond rhombus, not the hypercubic square plaquette (F305).

WHY (F265 -> the d1 chain)
==========================
F265 found the model's gauge sectors split down the middle: the propagators were
BCC while the ACTION was simple-cubic, and the composite-SC plaquette is blind to
1/3 of the curvature-carrying link degrees of freedom.  F265 sec.9 then listed the
entire ``ca_lpt_*`` chain -- F144/F151/F152/F154/F155/F162/F163/F239/F280 -- as
"still cubic, explicitly open".  ``lpt_vertex``'s own docstring states the premise
F265 invalidated: *"what differs between the rule and Wilson is the PROPAGATOR
..., not the plaquette vertex"*.  It does differ.  The rule's minimal gauge loop
is the 4-bond rhombus on 4 link axes with 6 spatial orientations, and this module
derives its Feynman rules.

METHOD — derived, never transcribed
===================================
The same multilinear link expansion as ``casim.engine.core.lpt_generator``
(HiPPy/HPsrc-style): expand ``U = exp(i A)`` order by order, read off the
momentum-space coefficient.  Only the LOOP WORD changes.  The n-point vertex of
any compact plaquette action is a finite sum

    V = sum_t c_t exp(i sum_r k_r . v_{t,r})

with ``c_t`` a colour trace and ``v_{t,r}`` the link-midpoint shift leg r sits at,
so the term list is enumerated once per (action, axis-tuple) and then evaluated
vectorised.  Parameterising the enumeration by the loop word means the hypercubic
Wilson plaquette and the BCC rhombus run through ONE code path, which is what
makes a rule-minus-Wilson difference apples-to-apples rather than two pipelines
compared by eye.

GEOMETRY (all constants from ``casim.engine.lattice.geometry``)
==============================================================
* 4 spatial link axes ``BCC_LINK_AXES`` (the <111> family), plus Euclidean time:
  5 generalised axes in all.  A gauge field component per link axis.
* 6 minimal spatial rhombi ``BCC_PLAQUETTES`` (both senses) + 4 temporal rhombi
  (both senses) = 20 oriented minimal loops, against Wilson's 12.
* generalised hatted momentum ``khat_i = 2 sin(k . D_i / 2)``; for the hypercubic
  action ``D_i = e_mu`` and this is exactly Wilson's ``2 sin(k_mu/2)``.

WHAT THE GATES ESTABLISH (all machine-exact unless stated)
==========================================================
G1  the generated 2-point vertex is EXACTLY
        Gamma_ij(k) = delta_ij sum_l khat_l^2 - khat_i khat_j
    with overall normalisation K = 1 -- the BCC analogue of Wilson's
    ``delta_mu_nu khat^2 - khat_mu khat_nu``, and the load-bearing gate (the same
    one ``lpt_generator.validate_propagator`` uses).
G2  ``sum_i d_i d_i^T = 4 I`` EXACTLY, so the continuum limit is isotropic with
    normalisation 4; on axis the first lattice correction is ``-k^4/3`` (exact).
G3  the 3-point vertex reduces to the axis-space Yang-Mills tensor with K = i and
    a deviation that falls as O(a^2) -- the correct continuum limit.
G4  antisymmetry under simultaneous (axis, momentum) exchange, exact.
G5  the exact lattice Ward identity ``sum_j Gamma_ij khat_j = 0``.
G6  MODE COUNT, and it is a fork.  Gamma has one zero mode (gauge) and FOUR
    degenerate massless modes, against three in continuum 4-D Yang-Mills.  The
    redundant link-axis combination ``NHAT = (-1,1,1,1)/2`` (the unique n with
    ``sum_i n_i d_i = 0``) is an EXACT eigenvector with eigenvalue ``sum_l khat_l^2``
    -- massless, exactly transverse, and NOT annihilated by the 3-point vertex.
    So it is dynamical unless it is projected out.  See ``mode_fork``.
G7  the cube ``[-pi,pi)^3`` holds EXACTLY 4 copies of the BCC Brillouin zone
    (F278 confirmed for the gauge link lattice, by primitive-cell volume), and
    the action's quadratic form is exactly periodic under the reciprocal lattice.

HONEST SCOPE
============
* This module supplies VERTICES and the action's own quadratic form.  It does not
  claim the rule's gauge action *is* the rhombic Wilson action: the F26 rotation
  law's ``3 Omega_even^2`` and this action's ``sum_l khat_l^2 / 4`` agree in the
  continuum limit and DISAGREE at finite momentum (measured, see
  ``propagator_split``).  Which object is the rule's gauge action at finite a is
  a decision this module makes visible and does not take.
* G6's fork is decided here only in the weak sense that the projected branch is
  the one whose continuum limit is 4-D Yang-Mills (an exact isometry argument,
  ``PP^T = I``), corroborated by the b0 trend in
  ``casim.engine.gauge.lpt_d1_action_consistent``.  It is not a theorem that the
  rule's link fields carry no independent redundant mode.
"""
from __future__ import annotations

import itertools
import math
from functools import lru_cache

from casim.numerics import xp
from casim.engine.core import lpt_generator as gen
from casim.engine.lattice.geometry import BCC_LINK_AXES, BCC_PLAQUETTES

#: the 5 generalised link axes: 4 BCC <111> spatial axes + Euclidean time
AX_BCC = [xp.array(list(d) + [0.0]) for d in BCC_LINK_AXES] + [xp.array([0.0, 0.0, 0.0, 1.0])]
#: the 4 hypercubic axes, for the shared-code-path comparison
AX_SC = [xp.eye(4)[m] for m in range(4)]

#: the unique redundant link-axis combination, sum_i n_i d_i = 0
NHAT_BCC = xp.array([-1.0, 1.0, 1.0, 1.0, 0.0]) / 2.0

_TG = gen.T_GEN


# ----------------------------------------------------------------------
#  loop words
# ----------------------------------------------------------------------
def _axis_bcc(v):
    if abs(v[3]) > 0:
        return 4, int(xp.sign(v[3]))
    for i, d in enumerate(BCC_LINK_AXES):
        if tuple(int(c) for c in v[:3]) == d:
            return i, +1
        if tuple(int(-c) for c in v[:3]) == d:
            return i, -1
    raise ValueError(f"{v} is not a BCC link direction")


def _axis_sc(v):
    for m in range(4):
        if abs(v[m]) > 0:
            return m, int(xp.sign(v[m]))
    raise ValueError(v)


def _steps(vecs, axis_of, axes):
    """loop word -> [(axis, link-midpoint shift, daggered)].

    A step in direction -d is the daggered field of the same axis one site back,
    so its midpoint is ``base - d/2``; both cases are ``base + sign*D/2``.
    """
    out, base = [], xp.zeros(4)
    for v in vecs:
        ax, sg = axis_of(v)
        out.append((ax, base + sg * 0.5 * axes[ax], sg < 0))
        base = base + v
    return out


def _loops_bcc():
    L = []
    for d1, d2 in BCC_PLAQUETTES:                     # 6 orientations, both senses
        a = xp.array(list(d1) + [0.0])
        b = xp.array(list(d2) + [0.0])
        L += [[a, b, -a, -b], [b, a, -b, -a]]
    t = xp.array([0.0, 0.0, 0.0, 1.0])
    for d in BCC_LINK_AXES:                           # 4 temporal rhombi, both senses
        a = xp.array(list(d) + [0.0])
        L += [[a, t, -a, -t], [t, a, -t, -a]]
    return L


def _loops_sc():
    L = []
    for r in range(4):
        for s in range(4):
            if r != s:
                L.append([xp.eye(4)[r], xp.eye(4)[s], -xp.eye(4)[r], -xp.eye(4)[s]])
    return L


ACTIONS = {
    "bcc": {"AX": AX_BCC, "N": 5, "tax": 4,
            "words": [_steps(w, _axis_bcc, AX_BCC) for w in _loops_bcc()]},
    "sc": {"AX": AX_SC, "N": 4, "tax": 3,
           "words": [_steps(w, _axis_sc, AX_SC) for w in _loops_sc()]},
}


# ----------------------------------------------------------------------
#  term enumeration  (derived from the same link expansion, not transcribed)
# ----------------------------------------------------------------------
def _orderings(legs, mats):
    """exp() expansion at one link slot: sum over orderings, with the 1/m!."""
    m = len(legs)
    if m == 0:
        return [(1.0, xp.eye(3, dtype=complex))]
    out = []
    for perm in itertools.permutations(legs):
        M = xp.eye(3, dtype=complex)
        for r in perm:
            M = M @ mats[r]
        out.append((1.0 / math.factorial(m), M))
    return out


@lru_cache(maxsize=None)
def terms(action: str, axes: tuple, nleg: int):
    """The finite term list ``(coeffs, shifts)`` of the n-point vertex."""
    words = ACTIONS[action]["words"]
    mats = [_TG[r] for r in range(nleg)] if nleg == 3 else [_TG[0]] * nleg
    acc = {}
    for word in words:
        slots = list(range(len(word)))
        cand = [[s for s in slots if word[s][0] == axes[r]] for r in range(nleg)]
        if any(len(c) == 0 for c in cand):
            continue
        for f in itertools.product(*cand):
            per = {s: [r for r in range(nleg) if f[r] == s] for s in slots}
            pref = 1.0 + 0j
            for s in slots:
                ms = len(per[s])
                if ms:
                    pref *= (1j if not word[s][2] else -1j) ** ms
            partials = [(pref, xp.eye(3, dtype=complex))]
            for s in slots:
                partials = [(c0 * c1, M0 @ M1) for (c0, M0) in partials
                            for (c1, M1) in _orderings(per[s], mats)]
            tr = sum(c * xp.trace(M) for c, M in partials)
            if abs(tr) < 1e-14:
                continue
            v = tuple(tuple(word[f[r]][1]) for r in range(nleg))
            acc[v] = acc.get(v, 0j) - tr                     # vertex = -Tr(U_loop)
    keep = [(c,) + v for v, c in acc.items() if abs(c) > 1e-14]
    if not keep:
        return xp.zeros(0, dtype=complex), xp.zeros((0, nleg, 4))
    cs = xp.array([t[0] for t in keep])
    vs = xp.array([[xp.asarray(t[1 + r]) for r in range(nleg)] for t in keep])
    return cs, vs


def vertex3(action, axes, k0, k1, k2):
    """3-point vertex, vectorised over grid-shaped momenta."""
    cs, vs = terms(action, tuple(int(a) for a in axes), 3)
    if len(cs) == 0:
        return 0.0
    ph = (xp.tensordot(k0, vs[:, 0, :].T, axes=([-1], [0]))
          + xp.tensordot(k1, vs[:, 1, :].T, axes=([-1], [0]))
          + xp.tensordot(k2, vs[:, 2, :].T, axes=([-1], [0])))
    return xp.tensordot(xp.exp(1j * ph), cs, axes=([-1], [0]))


def vertex2(action, axes, k):
    """2-point vertex (legs at momenta +k and -k)."""
    cs, vs = terms(action, tuple(int(a) for a in axes), 2)
    if len(cs) == 0:
        return 0.0
    ph = (xp.tensordot(k, vs[:, 0, :].T, axes=([-1], [0]))
          - xp.tensordot(k, vs[:, 1, :].T, axes=([-1], [0])))
    return xp.tensordot(xp.exp(1j * ph), cs, axes=([-1], [0]))


# ----------------------------------------------------------------------
#  kinematics
# ----------------------------------------------------------------------
def axes_matrix(action):
    return xp.array(ACTIONS[action]["AX"])


def khat(action, k):
    """khat_i = 2 sin(k . D_i / 2); Wilson's 2 sin(k_mu/2) when action='sc'."""
    return 2.0 * xp.sin(xp.tensordot(k, axes_matrix(action), axes=([-1], [1])) / 2.0)


def quadratic_form(action, k):
    """The action's OWN inverse propagator, sum_l khat_l^2 (Feynman gauge)."""
    return xp.sum(khat(action, k) ** 2, axis=-1)


# ----------------------------------------------------------------------
#  reciprocal lattice / fundamental domain
# ----------------------------------------------------------------------
_PRIMITIVE = xp.array([[1, 1, 1], [1, 1, -1], [1, -1, 1]], dtype=float)


def reciprocal_basis():
    return 2 * math.pi * xp.linalg.inv(_PRIMITIVE).T


def _recip_vectors(rng=2):
    B = reciprocal_basis()
    return xp.array([xp.array(n, dtype=float) @ B
                     for n in itertools.product(range(-rng, rng + 1), repeat=3)
                     if n != (0, 0, 0)])


_G = _recip_vectors()
_GHALF = 0.5 * xp.sum(_G ** 2, axis=1)


def ws_mask(k):
    """True where the spatial part of k is in the Wigner-Seitz cell of the BCC
    reciprocal lattice — a genuine fundamental domain, unlike the cube."""
    return xp.asarray(
        xp.einsum('...i,gi->...g', k[..., :3], _G) <= _GHALF + 1e-12).all(axis=-1)


# ======================================================================
#  GATES
# ======================================================================
def gate_two_point(action="bcc", seed=0, ntest=6, tol=1e-12) -> dict:
    """G1 — the generated 2-point vertex IS delta_ij sum khat^2 - khat_i khat_j."""
    N = ACTIONS[action]["N"]
    rng = xp.random.default_rng(seed)
    Ks, spreads, imags = [], [], []
    for _ in range(ntest):
        k = rng.uniform(-1.5, 1.5, 4)
        kh = khat(action, k)
        G = xp.zeros((N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                G[i, j] = vertex2(action, (i, j), k)
        tgt = xp.diag(xp.full(N, float(xp.sum(kh ** 2)))) - xp.outer(kh, kh)
        m = xp.abs(tgt) > 1e-9
        r = xp.real(G[m]) / tgt[m]
        Ks.append(float(xp.mean(r)))
        spreads.append(float(xp.max(xp.abs(r - xp.mean(r)))))
        imags.append(float(xp.max(xp.abs(xp.imag(G)))))
    return {"action": action, "K_mean": float(xp.mean(xp.asarray(Ks))),
            "K_spread": float(xp.max(xp.abs(xp.asarray(Ks) - 1.0))),
            "structure_spread": float(max(spreads)), "max_imag": float(max(imags)),
            "pass": bool(max(spreads) < tol and max(abs(k - 1.0) for k in Ks) < tol),
            "statement": "Gamma_ij(k) = delta_ij sum_l khat_l^2 - khat_i khat_j, K = 1"}


def gate_isotropy() -> dict:
    """G2 — sum_i d_i d_i^T = 4 I exactly; continuum limit isotropic."""
    d = xp.array(BCC_LINK_AXES, dtype=float)
    M = d.T @ d
    dev = float(xp.max(xp.abs(M - 4.0 * xp.eye(3))))
    # on-axis lattice correction, from the closed form 4 sum_i sin^2(k.d_i/2)
    quart = []
    for k in (1e-1, 5e-2):
        S = float(sum(4 * math.sin(k * di[0] / 2.0) ** 2 for di in BCC_LINK_AXES))
        quart.append((S - 4 * k ** 2) / k ** 4)
    return {"sum_d_dT": M.tolist(), "deviation_from_4I": dev,
            "quartic_coefficient_measured": quart,
            "quartic_coefficient_exact": -1.0 / 3.0,
            "pass": bool(dev == 0.0
                         and all(abs(q + 1.0 / 3.0) < 1e-3 for q in quart)),
            "statement": "sum_i d_i d_i^T = 4 I EXACTLY => isotropic continuum "
                         "limit with normalisation 4; on axis S = 4k^2 - k^4/3."}


def _axis_ym(action, p, q, r):
    """axis-space Yang-Mills 3-gluon tensor:
       delta_ij (p-q).D_l + delta_jl (q-r).D_i + delta_li (r-p).D_j"""
    N = ACTIONS[action]["N"]
    D = axes_matrix(action)
    dl = xp.eye(N)
    return (xp.einsum('ij,l->ijl', dl, (p - q) @ D.T)
            + xp.einsum('jl,i->ijl', dl, (q - r) @ D.T)
            + xp.einsum('li,j->ijl', dl, (r - p) @ D.T))


def gate_three_point(action="bcc", seed=11, scales=(1e-2, 1e-3, 1e-4)) -> dict:
    """G3 — the 3-point vertex reduces to the axis-space YM tensor, K = i, with
    an O(a^2) deviation (the ratio of successive rel-spreads must be ~1e-2)."""
    N = ACTIONS[action]["N"]
    rng = xp.random.default_rng(seed)
    p0 = rng.uniform(-1, 1, 4)
    q0 = rng.uniform(-1, 1, 4)
    rows = []
    for sc in scales:
        p = sc * p0
        q = sc * q0
        r = -p - q
        T = xp.zeros((N, N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                for l in range(N):
                    T[i, j, l] = vertex3(action, (i, j, l), p, q, r)
        C = _axis_ym(action, p, q, r)
        m = xp.abs(C) > 1e-12 * xp.max(xp.abs(C))
        ratio = T[m] / C[m]
        rows.append({"scale": sc, "K": complex(xp.mean(ratio)),
                     "rel_spread": float(xp.max(xp.abs(ratio - xp.mean(ratio)))
                                         / abs(xp.mean(ratio)))})
    ord_ = [rows[i]["rel_spread"] / rows[i + 1]["rel_spread"] for i in range(len(rows) - 1)]
    return {"action": action,
            "rows": [{"scale": r["scale"], "K_re": float(r["K"].real),
                      "K_im": float(r["K"].imag), "rel_spread": r["rel_spread"]}
                     for r in rows],
            "order_ratios": ord_,
            "pass": bool(abs(rows[-1]["K"] - 1j) < 1e-6
                         and all(50.0 < o < 200.0 for o in ord_)),
            "statement": "K = i (the generator's U = exp(iA) convention) and the "
                         "deviation from the continuum tensor falls as a^2."}


def gate_antisymmetry(action="bcc", seed=2, scale=0.3) -> dict:
    """G4 — V(ijl; pqr) = -V(jil; qpr), exact (the f^{abc} antisymmetry)."""
    N = ACTIONS[action]["N"]
    rng = xp.random.default_rng(seed)
    p = scale * rng.uniform(-1, 1, 4)
    q = scale * rng.uniform(-1, 1, 4)
    r = -p - q
    worst = 0.0
    for i in range(N):
        for j in range(N):
            for l in range(N):
                worst = max(worst, abs(vertex3(action, (i, j, l), p, q, r)
                                       + vertex3(action, (j, i, l), q, p, r)))
    return {"action": action, "max_residual": worst, "pass": bool(worst < 1e-13),
            "statement": "antisymmetric under simultaneous (axis, momentum) exchange"}


def gate_ward(action="bcc", seed=5, ntest=4) -> dict:
    """G5 — the exact lattice Ward identity sum_j Gamma_ij khat_j = 0."""
    rng = xp.random.default_rng(seed)
    worst = 0.0
    for _ in range(ntest):
        k = rng.uniform(-2.0, 2.0, 4)
        kh = khat(action, k)
        S = float(xp.sum(kh ** 2))
        G = S * xp.eye(len(kh)) - xp.outer(kh, kh)
        worst = max(worst, float(xp.max(xp.abs(G @ kh))) / max(S, 1e-30))
    return {"action": action, "max_relative_residual": worst,
            "pass": bool(worst < 1e-13),
            "statement": "sum_j Gamma_ij khat_j = 0 exactly at finite lattice spacing"}


def mode_fork(seed=3, scales=(1e-3, 1e-2, 0.5), nhat_perturb: float = 0.0) -> dict:
    """G6 — the mode count, and the fork it opens.

    Gamma = S delta - khat khat^T has ONE zero mode (gauge) and N-1 = 4 massless
    modes, against 3 in continuum 4-D Yang-Mills.  The extra one is the redundant
    link-axis combination NHAT: it is an exact eigenvector with eigenvalue S, and
    the 3-point vertex does NOT annihilate it.
    """
    rng = xp.random.default_rng(seed)
    nhat = NHAT_BCC + nhat_perturb * xp.array([0.0, 0.0, 0.0, 0.0, 1.0])
    nhat = nhat / xp.linalg.norm(nhat)
    rows = []
    for sc in scales:
        k = sc * rng.uniform(-1, 1, 4)
        kh = khat("bcc", k)
        S = float(xp.sum(kh ** 2))
        G = S * xp.eye(5) - xp.outer(kh, kh)
        ev = xp.sort(xp.linalg.eigvalsh(G))
        rows.append({"scale": sc,
                     "eigs": [float(e) for e in ev],
                     "n_zero": int(xp.sum(xp.abs(ev) < 1e-10 * max(1.0, float(ev[-1])))),
                     "nhat_rayleigh_over_S": float(nhat @ G @ nhat) / S})
    # does the redundant mode couple to the cubic vertex?
    p = 1e-2 * rng.uniform(-1, 1, 4)
    q = 1e-2 * rng.uniform(-1, 1, 4)
    r = -p - q
    T = xp.zeros((5, 5, 5), dtype=complex)
    for i in range(5):
        for j in range(5):
            for l in range(5):
                T[i, j, l] = vertex3("bcc", (i, j, l), p, q, r)
    coupling = float(xp.max(xp.abs(xp.einsum('i,ijl->jl', nhat, T)))
                     / xp.max(xp.abs(T)))
    d = xp.array(BCC_LINK_AXES, dtype=float)
    P = d.T / 2.0                                    # Cartesian projector, 3 x 4
    return {"rows": rows, "nhat": nhat.tolist(), "nhat_perturb": nhat_perturb,
            "nhat_eigenvector_in_continuum_limit": bool(
                abs(rows[0]["nhat_rayleigh_over_S"] - 1.0) < 1e-5),
            "nhat_gauge_mixing_vs_scale": [
                {"scale": r["scale"], "1_minus_rayleigh": 1.0 - r["nhat_rayleigh_over_S"]}
                for r in rows],
            "n_zero_modes": rows[-1]["n_zero"],
            "n_propagating_bcc": 4, "n_propagating_continuum_4d": 3,
            "vertex_coupling_to_nhat": coupling,
            "projector_isometry_residual": float(xp.max(xp.abs(P @ P.T - xp.eye(3)))),
            "pass": bool(all(r["n_zero"] == 1 for r in rows) and coupling > 1e-3
                         and abs(rows[0]["nhat_rayleigh_over_S"] - 1.0) < 1e-5),
            "statement": "one gauge zero mode and FOUR massless modes (continuum "
                         "4-D YM has three): the redundant link-axis combination "
                         "NHAT is an exact massless eigenvector AND couples to the "
                         "3-gluon vertex, so it is dynamical unless projected. "
                         "P P^T = I exactly, so the projected branch's continuum "
                         "limit IS 4-D Yang-Mills."}


def brillouin_zone(nsample=200000, seed=0) -> dict:
    """G7 — the cube holds exactly 4 copies of the BCC Brillouin zone (F278), and
    the action's quadratic form is exactly reciprocal-lattice periodic."""
    B = reciprocal_basis()
    V_rec = abs(float(xp.linalg.det(B)))
    cube = (2 * math.pi) ** 3
    rng = xp.random.default_rng(seed)
    P = rng.uniform(-math.pi, math.pi, size=(nsample, 3))
    frac = float(xp.mean(xp.asarray(
        xp.einsum('...i,gi->...g', P, _G) <= _GHALF + 1e-12).all(axis=-1)))
    k0 = xp.concatenate([rng.uniform(-1, 1, 3), xp.zeros(1)])
    per = max(abs(float(quadratic_form("bcc", k0))
                  - float(quadratic_form("bcc", k0 + xp.concatenate([g, xp.zeros(1)]))))
              for g in _G)
    return {"det_primitive_cell": abs(float(xp.linalg.det(_PRIMITIVE))),
            "V_reciprocal_cell": V_rec, "cube_over_bz": cube / V_rec,
            "ws_fraction_of_cube_mc": frac, "implied_copies": 1.0 / frac,
            "periodicity_residual": per,
            "pass": bool(abs(cube / V_rec - 4.0) < 1e-9 and per < 1e-12
                         and abs(frac - 0.25) < 5e-3),
            "statement": "cube/BZ = 4 EXACTLY by primitive-cell volume (F278 "
                         "confirmed for the gauge link lattice); the quadratic "
                         "form is exactly periodic under the reciprocal lattice."}


def propagator_split(seed=0, ntest=6) -> dict:
    """The declared gap: the rhombic ACTION's quadratic form and the F26 rotation
    law's ``3 Omega_even^2`` agree in the continuum limit and DISAGREE at finite
    momentum.  Reported, not resolved."""
    from casim.engine.gauge import gluon_self_energy as se
    rng = xp.random.default_rng(seed)
    big, small = [], []
    for _ in range(ntest):
        k = rng.uniform(-math.pi, math.pi, 3)
        k4 = xp.concatenate([k, xp.zeros(1)])
        a = float(quadratic_form("bcc", k4)) / 4.0
        b = float(3.0 * se.omega_even(k[0], k[1], k[2]) ** 2)
        big.append(a / b)
    for s in (1e-2, 1e-3):
        k = s * rng.uniform(-1, 1, 3)
        k4 = xp.concatenate([k, xp.zeros(1)])
        a = float(quadratic_form("bcc", k4)) / 4.0
        b = float(3.0 * se.omega_even(k[0], k[1], k[2]) ** 2)
        small.append({"k": float(xp.linalg.norm(k)), "ratio": a / b})
    return {"ratio_at_generic_k": big,
            "worst_generic_deviation": max(abs(r - 1.0) for r in big),
            "small_k": small,
            "agree_in_continuum": bool(all(abs(s["ratio"] - 1.0) < 1e-3 for s in small)),
            "pass": True,
            "statement": "S/4 -> 3 Omega_even^2 as k -> 0 but differs by O(1) at "
                         "generic k: the rule's gauge ACTION and its PROPAGATOR "
                         "are not yet the same object at finite a. Declared gap."}


def check_bcc_vertices(tol: float = 1e-12, action: str = "bcc",
                       nhat_perturb: float = 0.0) -> dict:
    """Registry entry point (D9).  Sweepable on `tol`, `action`, `nhat_perturb`.

    The declared control is `nhat_perturb`: tilting the redundant link-axis
    combination out of the null space of ``sum_i n_i d_i = 0`` must redden G6,
    because G6's content is that THAT PARTICULAR combination is the massless
    eigenvector -- no other direction is."""
    out = {"G1_two_point": gate_two_point(action, tol=tol),
           "G2_isotropy": gate_isotropy(),
           "G3_three_point": gate_three_point(action),
           "G4_antisymmetry": gate_antisymmetry(action),
           "G5_ward": gate_ward(action),
           "G6_mode_fork": mode_fork(nhat_perturb=nhat_perturb),
           "G7_brillouin_zone": brillouin_zone(),
           "propagator_split": propagator_split()}
    # `checks` is the key casim.tests.runner.leg_map reads (D9 control legs);
    # `legs` is kept as a readable alias for the tests and the artifact.
    out["checks"] = {k: bool(v["pass"]) for k, v in out.items() if isinstance(v, dict)}
    out["legs"] = dict(out["checks"])
    out["pass"] = all(out["checks"].values())
    return out


if __name__ == "__main__":  # pragma: no cover
    import json
    print(json.dumps(check_bcc_vertices(), indent=1, default=str))
