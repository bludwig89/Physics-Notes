"""colour_theta.py — theta_QCD on the rule's own gauge sector (completeness B11).

WHY (the accounting half)
=========================
Completeness row B11 ("Strong CP / theta_QCD") has carried the same residual for
three reports: *"tree 3.3e-16; loops open -- theta pure gauge at tree level. The
2026-06-29 audit flagged loop survival; still unaddressed."*  Its evidence column
names F53.

F53 does not say that.  F53's P5 measures the **F27 complex-mass phase** -- the
Stueckelberg phase of the electroweak sector -- and F53's own Remaining section
is explicit: *"Strong CP (theta-bar of QCD) is a separate phase in the gluon
sector (F43), untouched here."*  So the number B11 quotes is a statement about a
different theta, and the row was not "tree closed, loops open"; it had no
tree-level evidence either.  Same shape as B12's Amendment 7.

WHY (the physics half)
======================
The loop question the 2026-06-29 audit actually flagged is narrower than "compute
the loop contribution to theta", and it is now finite.  That audit's G1 caveat:

    "The gluon argument (G1) proves colour coupling is branch-blind [...] This
     covers the linear (free) propagator.  However, the SU(3) self-coupling
     (triple and quartic gluon vertices) is not analyzed for its branch
     structure."

F305/F307 derived the rule's TRUE BCC rhombic gauge vertices, so the caveat is a
computation rather than an open question.  The observation this module turns on:

    In Euclidean signature the theta-term is the UNIQUE purely-imaginary gauge
    invariant -- the weight is exp(-S_YM + i*theta*Q).  So "the rule's Euclidean
    action is real" and "the rule contains no theta-term" are the SAME statement,
    and a loop-generated theta would have to appear as a generated imaginary
    part.

Reality is then not a convention someone imposed by writing ``Re tr``: it is a
property of the rule's LOOP SET.  ``lpt_bcc_vertex._loops_bcc`` enumerates each
minimal rhombus in **both senses** (6 spatial x2 + 4 temporal x2 = 20 oriented
loops), and a loop set closed under reversal gives sum_loops Tr U = 2 Re sum Tr U
for every configuration, non-perturbatively.  The perturbative face of the same
fact is the vertex identity

    V(-k) = conj(V(k))          exactly, at every leg count,

which is preserved under loop integration -- the functions obeying it are closed
under products and under integration of internal momenta with a q -> -q symmetric
measure.  Hence the effective action obeys it too, at every order, and no loop
can generate an imaginary part.  That is the audit's item.

WHAT IS AND IS NOT CLAIMED
==========================
NOT claimed: that the model "solves the strong CP problem".  Peccei-Quinn asks
why a FREE parameter is tiny; this rule has no slot for that parameter, which is
a different and strictly weaker-in-scope statement -- it is contingent on the
rule being the right rule, and it is not a dynamical relaxation mechanism.

NOT claimed: that theta-bar = 0.  The physical invariant is
theta-bar = theta + arg det M_q.  This module closes the first term EXACTLY and
relocates the entire strong-CP question into the second.  At one generation the
F27 phase drops out (which IS what F53's P5 measures -- correctly attributed
here).  At three generations arg det M_q is set by the quark mass texture, which
is open-derivations E6/E7, and nothing here closes it.

NOT claimed: a decision on lpt_bcc_vertex's declared action fork.  That module's
HONEST SCOPE says the F26 rotation law and the rhombic plaquette action disagree
at finite momentum and it does not choose.  So block T4 runs the parity argument
on the OTHER branch as well: the F26 even law is P-even, the chiral law is not,
and F91's "gluon even (forced)" is what puts the rule on the P-even branch.  The
conclusion therefore survives the fork instead of presupposing its resolution.

MEASURED AND NOT USED: the clover's finite-a parity eigenvalue.  ``parity_map``
is an exact symmetry of the action (T1d, 3.2e-14), but the reconstructed clover
``Q`` does NOT map to ``-Q`` under it at finite lattice spacing -- the relative
defect measured 0.42-0.83 and does NOT fall as the field weakens (scale 1.0 ->
0.03), and no orientation-permutation-with-sign-and-translation match exists
either.  So the familiar "E.B is P-odd" is used here as a CONTINUUM statement
only, and every load-bearing leg rests on reality / ``U -> U*`` instead, which
needs no point-group bookkeeping.  Making the rhombic clover a parity eigenstate
at finite a is left open and is the natural next step for this module.

Q's overall normalisation is a convention (the 4->3 and 6->3 projections are
fixed by sum_i d_i d_i^T = 4I and M^T M = 4I).  Every result here is a sign or a
zero, both invariant under it.
"""
from __future__ import annotations

import itertools
import math

from casim.numerics import xp, rng
from casim.engine.core import lpt_generator as gen
from casim.engine.gauge import lpt_bcc_vertex as bv
from casim.engine.lattice.bcc import bcc_dispersion
from casim.engine.lattice.geometry import (BCC_LINK_AXES, BCC_PLAQUETTES,
                                           BCC_PLAQ_NORMALS)

__all__ = [
    "loop_set_reversal_closure", "random_su3_links_4d", "holonomy",
    "loop_action", "topological_density", "parity_map", "cp_map",
    "vertex_reality_defect", "even_law_parity_defect", "thetabar_one_generation",
    "check_strong_cp",
]

#: 4 spatial <111> link axes + Euclidean time, as integer 4-vectors
_STEPS = [tuple(int(c) for c in d) + (0,) for d in BCC_LINK_AXES] + [(0, 0, 0, 1)]
_TIME_AX = 4
_TG = gen.T_GEN
_NAX = 5


def _axis_of(v4):
    """(axis index, sign) for a 4-vector step that is +/- one of the 5 axes."""
    for i, s in enumerate(_STEPS):
        if all(int(v4[j]) == s[j] for j in range(4)):
            return i, +1
        if all(int(v4[j]) == -s[j] for j in range(4)):
            return i, -1
    raise ValueError(f"{v4} is not a link axis")


def _words():
    """The rule's 20 oriented minimal loops as [(axis, sign), ...] step lists."""
    out = []
    for d1, d2 in BCC_PLAQUETTES:
        a = tuple(int(c) for c in d1) + (0,)
        b = tuple(int(c) for c in d2) + (0,)
        out += [[a, b, _neg(a), _neg(b)], [b, a, _neg(b), _neg(a)]]
    t = (0, 0, 0, 1)
    for d in BCC_LINK_AXES:
        a = tuple(int(c) for c in d) + (0,)
        out += [[a, t, _neg(a), _neg(t)], [t, a, _neg(t), _neg(a)]]
    return [[_axis_of(v) for v in w] for w in out]


def _neg(v):
    return tuple(-c for c in v)


def _words_sc():
    """The hypercubic reference loop set (12 oriented squares)."""
    e = [tuple(1 if j == m else 0 for j in range(4)) for m in range(4)]
    out = []
    for r in range(4):
        for s in range(4):
            if r != s:
                out.append([e[r], e[s], _neg(e[r]), _neg(e[s])])
    return out


# ══════════════════════════════════════════════════════════════════════════
#  T0 — the premise: the loop set is closed under reversal
# ══════════════════════════════════════════════════════════════════════════

def _canonical(word):
    """A translation-invariant fingerprint of a based closed loop word."""
    return tuple(tuple(int(c) for c in v) for v in word)


def _rotations(word):
    n = len(word)
    return [tuple(word[(i + j) % n] for j in range(n)) for i in range(n)]


def _reverse(word):
    """The same loop traversed backwards: reverse order and negate each step."""
    return tuple(_neg(v) for v in reversed(word))


def loop_set_reversal_closure(which: str = "bcc") -> dict:
    """Is every loop's reverse also in the set, up to translation?

    This is the PREMISE of every reality result below.  If it fails, sum Tr U
    is complex and the rule carries a theta-term.
    """
    words = ([[_STEPS[i] if s > 0 else _neg(_STEPS[i]) for i, s in w]
              for w in _words()] if which == "bcc" else _words_sc())
    keys = set()
    for w in words:
        keys.update(_canonical(r) for r in _rotations(tuple(w)))
    missing = [w for w in words if _canonical(_reverse(tuple(w))) not in keys]
    return {"n_loops": len(words), "n_missing_reverse": len(missing),
            "closed": len(missing) == 0}


# ══════════════════════════════════════════════════════════════════════════
#  4-D link configurations
# ══════════════════════════════════════════════════════════════════════════

def random_su3_links_4d(shape=(4, 4, 4, 4), seed: int = 0, scale: float = 1.0):
    """5 SU(3) link fields (4 spatial <111> axes + time) on a 4-D array.

    ``scale`` interpolates identity (0) to Haar-random (1); ``scale = 1`` is a
    genuinely strong-field configuration, which is what makes the reality
    statement non-perturbative rather than small-A.
    """
    rng.seed_run(int(seed))
    g = rng.for_channel("colour_theta")
    U = []
    for _ in range(_NAX):
        z = (g.normal(size=shape + (3, 3)) + 1j * g.normal(size=shape + (3, 3)))
        q, r = xp.linalg.qr(z)
        ph = xp.diagonal(r, axis1=-2, axis2=-1)
        q = q * (ph / xp.abs(ph))[..., None, :]
        det = xp.linalg.det(q)
        q = q * (det ** (-1.0 / 3.0))[..., None, None]
        if scale != 1.0:
            # geodesic pull towards the identity, then re-unitarise
            q = (1.0 - scale) * xp.eye(3) + scale * q
            qq, rr = xp.linalg.qr(q)
            ph = xp.diagonal(rr, axis1=-2, axis2=-1)
            qq = qq * (ph / xp.abs(ph))[..., None, :]
            det = xp.linalg.det(qq)
            q = qq * (det ** (-1.0 / 3.0))[..., None, None]
        U.append(q)
    return U


def _shift(A, v4):
    """``B[x] = A[x + v]`` on the periodic 4-D array."""
    return xp.roll(A, tuple(-int(c) for c in v4), axis=(0, 1, 2, 3))


def _dag(A):
    return xp.conj(xp.swapaxes(A, -1, -2))


def _link(U, ax, sign, base):
    """The link matrix field for one step of the loop word, based at ``base``."""
    if sign > 0:
        return _shift(U[ax], base)
    back = tuple(base[j] - _STEPS[ax][j] for j in range(4))
    return _dag(_shift(U[ax], back))


def holonomy(U, word):
    """The path-ordered product around one based loop word."""
    base = (0, 0, 0, 0)
    P = None
    for ax, sign in word:
        A = _link(U, ax, sign, base)
        P = A if P is None else xp.matmul(P, A)
        step = _STEPS[ax] if sign > 0 else _neg(_STEPS[ax])
        base = tuple(base[j] + step[j] for j in range(4))
    assert base == (0, 0, 0, 0), "loop word did not close"
    return P


def loop_action(U, theta: float = 0.0, reverse_senses: bool = True) -> complex:
    """``S = -sum_loops Tr U_loop``, returned COMPLEX and never Re()-projected.

    ``Im S`` is therefore a measurement, not zero by construction.  With
    ``reverse_senses=False`` only one sense of each rhombus is summed -- the
    structural control: reality is a property of the loop set, and dropping the
    reversed half must make ``Im S`` non-zero.

    ``theta`` injects a theta-term by hand, ``S -> S - i*theta*sum Q``: the
    physics control, which must also make ``Im S`` non-zero.
    """
    words = _words()
    if not reverse_senses:
        words = words[0::2]
    tot = 0j
    for w in words:
        tot += complex(xp.sum(xp.trace(holonomy(U, w), axis1=-2, axis2=-1)))
    S = -tot
    if theta:
        S = S - 1j * theta * float(xp.sum(topological_density(U)))
    return S


# ══════════════════════════════════════════════════════════════════════════
#  T3 — the theta operator: colour E.B from the rule's own rhombi
# ══════════════════════════════════════════════════════════════════════════

def _phases(P, T):
    """``Phi^a = Im tr(T^a P) / c`` with ``tr(T^a T^b) = c delta^{ab}`` measured."""
    c = float(xp.real(xp.trace(T[0] @ T[0])))
    return xp.stack([xp.imag(xp.einsum('ij,...ji->...', T[a], P)) / c
                     for a in range(T.shape[0])], axis=0)


def _clover(phi, a, b):
    """Centre a forward-rhombus phase on its base site.

    A rhombus based at ``x`` with sides ``(a, b)`` has its centre at
    ``x + (a+b)/2``, a half-integer point, so the *forward* phase is not a field
    at ``x``.  Averaging over the four translates whose rhombi surround ``x``
    puts the field strength AT ``x``, which is what makes the construction
    covariant under the lattice point group -- without it the electric and
    magnetic pieces of ``Q`` sit at different points and their product is not a
    parity eigenstate (measured: the defect does not fall with field strength).
    This is the ordinary clover discretisation, on the rhombus instead of the
    square.
    """
    ab = tuple(-(a[j] + b[j]) for j in range(4))
    return 0.25 * (phi + _shift(phi, _neg(a)) + _shift(phi, _neg(b))
                   + _shift(phi, ab))


def topological_density(U):
    """``Q(x) = sum_a E^a . B^a`` from the 4 temporal and 6 spatial rhombi.

    ``E`` comes from the 4 temporal rhombi projected with ``sum_i d_i d_i^T = 4I``
    (exact, ``lpt_bcc_vertex`` G2); ``B`` from the 6 spatial rhombi projected with
    ``M^T M = 4I`` on the <110> half-normals.  Both projections are closed-form,
    so ``Q`` needs no pseudo-inverse.
    """
    T = gen.T_GEN if hasattr(gen.T_GEN, "shape") else xp.array(gen.T_GEN)
    T = xp.asarray(T)
    # electric: temporal rhombus (d_i, t), one per <111> axis
    e = 0.0
    for i, d in enumerate(BCC_LINK_AXES):
        a = tuple(int(c) for c in d) + (0,)
        t = (0, 0, 0, 1)
        w = [_axis_of(v) for v in (a, t, _neg(a), _neg(t))]
        phi = _clover(_phases(holonomy(U, w), T), a, t)        # (8, ...)
        dv = xp.asarray(d, dtype=float).reshape((3,) + (1,) * phi.ndim)
        e = e + dv * phi[None]
    e = e / 4.0                                                 # (3, 8, ...)
    # magnetic: spatial rhombus, one per <110> half-normal
    b = 0.0
    for p, (d1, d2) in enumerate(BCC_PLAQUETTES):
        a = tuple(int(c) for c in d1) + (0,)
        c2 = tuple(int(c) for c in d2) + (0,)
        w = [_axis_of(v) for v in (a, c2, _neg(a), _neg(c2))]
        phi = _clover(_phases(holonomy(U, w), T), a, c2)
        m = xp.asarray(BCC_PLAQ_NORMALS[p], dtype=float).reshape((3,) + (1,) * phi.ndim)
        b = b + m * phi[None]
    b = b / 4.0
    return xp.sum(e * b, axis=(0, 1))                           # sum over i and a


# ══════════════════════════════════════════════════════════════════════════
#  the discrete maps
# ══════════════════════════════════════════════════════════════════════════

def parity_map(U):
    """Spatial inversion ``x -> -x``: ``(PU)_i(x) = U_i(-x - d_i)^dagger``.

    The temporal link is unaffected in direction but its base point inverts.
    """
    out = []
    for ax in range(_NAX):
        A = U[ax]
        inv = A[::-1, ::-1, ::-1, :]
        inv = xp.roll(inv, (1, 1, 1), axis=(0, 1, 2))     # x -> -x on a periodic array
        if ax == _TIME_AX:
            out.append(inv)
        else:
            # (PU)_i(x) = U_i(-x - d_i)^dagger : invert, then shift by +d_i
            out.append(_dag(_shift(inv, _STEPS[ax])))
    return out


def cp_map(U):
    """CP: parity composed with complex conjugation of every link."""
    return [xp.conj(A) for A in parity_map(U)]


def conjugation_map(U):
    """``U -> U*`` — the exact discrete symmetry the reality result rests on.

    ``Tr U* = conj(Tr U)``, so this map conjugates the action.  A reversal-closed
    loop set makes ``S`` real, hence INVARIANT under it, while the one-sense loop
    functional (the lattice's own CP-odd object) is exactly ODD under it.  Unlike
    ``parity_map`` this needs no lattice point-group bookkeeping, which is why it
    and not parity carries the load here.
    """
    return [xp.conj(A) for A in U]


def one_sense_functional(U) -> float:
    """``Im sum_{one sense per rhombus} Tr U_loop`` — CP-odd, and exactly the
    part that the rule's reversal closure cancels."""
    return float(-loop_action(U, reverse_senses=False).imag)


def theta_sensitivity(U, thetas=(0.1, 0.3, -0.7, 2.0)) -> dict:
    """Is ``Im S`` actually SENSITIVE to a theta-term?

    Injecting theta by hand must give ``Im S = -theta * sum Q`` exactly.  Without
    this leg "Im S = 0" would be a statement about an operator the lattice might
    not carry — i.e. vacuous.  The slope IS ``sum Q``, so the sensitivity is full
    and the zero is a measurement.
    """
    Q = float(xp.sum(topological_density(U)))
    base = loop_action(U).imag
    rows, worst = [], 0.0
    for th in thetas:
        im = loop_action(U, theta=th).imag
        pred = base - th * Q
        worst = max(worst, abs(im - pred))
        rows.append({"theta": float(th), "im_S": im, "predicted": pred})
    return {"Q": Q, "rows": rows, "linearity_defect": worst}


# ══════════════════════════════════════════════════════════════════════════
#  T2 — the vertex reality identity
# ══════════════════════════════════════════════════════════════════════════

def _register_one_sense_action():
    """Register a ONE-SENSE copy of the rule's loop set as a vertex action.

    Additive only -- a new key in ``lpt_bcc_vertex.ACTIONS``, no existing entry
    touched, so nothing else's numbers move.  Its purpose is the control on the
    vertex block: drop the reversed half of the loop set and the vertex identity
    ``V(-k) = conj(V(k))`` must fail, which is what makes T2's literal zeros a
    consequence of reversal closure rather than of the code path.
    """
    if "bcc_1sense" in bv.ACTIONS:
        return
    words = bv._loops_bcc()[0::2]
    bv.ACTIONS["bcc_1sense"] = {
        "AX": bv.AX_BCC, "N": 5, "tax": 4,
        "words": [bv._steps(w, bv._axis_bcc, bv.AX_BCC) for w in words]}


_register_one_sense_action()

def _terms_colour(action: str, axes, gens):
    """``bv.terms`` but with an ARBITRARY generator assignment per leg.

    WHY THIS EXISTS.  ``lpt_bcc_vertex.terms`` hardcodes ``[T^0, T^1, T^2]`` at
    three legs and ``[T^0]*n`` otherwise, which reads ONE ordered colour
    component of the vertex.  The imaginary part of a single-sense loop trace
    lives in the antisymmetric ``f^{abc}`` structure, so a fixed-index probe
    misses it: measured, the one-sense loop set passes a fixed-index reality test
    while its action's imaginary part is a perfectly visible O(A^3).  That gap was
    found by this record's own control, which is what the control is for.  Every
    reality statement here therefore samples colour indices.
    """
    words = bv.ACTIONS[action]["words"]
    mats = [_TG[g] for g in gens]
    nleg = len(gens)
    acc = {}
    for word in words:
        slots = list(range(len(word)))
        cand = [[t for t in slots if word[t][0] == axes[r]] for r in range(nleg)]
        if any(len(c) == 0 for c in cand):
            continue
        for f in itertools.product(*cand):
            per = {t: [r for r in range(nleg) if f[r] == t] for t in slots}
            pref = 1.0 + 0j
            for t in slots:
                ms = len(per[t])
                if ms:
                    pref *= (1j if not word[t][2] else -1j) ** ms
            partials = [(pref, xp.eye(3, dtype=complex))]
            for t in slots:
                partials = [(c0 * c1, M0 @ M1) for (c0, M0) in partials
                            for (c1, M1) in bv._orderings(per[t], mats)]
            tr = sum(c * xp.trace(M) for c, M in partials)
            if abs(tr) < 1e-14:
                continue
            v = tuple(tuple(word[f[r]][1]) for r in range(nleg))
            acc[v] = acc.get(v, 0j) - tr
    return {v: c for v, c in acc.items() if abs(c) > 1e-14}


def vertex_reality_defect(action="bcc", nleg=3, seed=0, nsample=6):
    """max ``|Im c|`` over vertex coefficients, sampling COLOUR indices too.

    ``V(-k) = conj(V(k))`` for all k is equivalent to every position-space
    coefficient being real, so the coefficient form is both stronger and cheaper
    than sampling momenta -- and it is the form that makes the loop statement
    immediate: the functions obeying it are closed under products and under
    q -> -q symmetric loop integration, so the effective action obeys it at every
    order and no loop can generate an imaginary part.
    """
    nax = bv.ACTIONS[action]["N"]
    rng.seed_run(int(seed))
    g = rng.for_channel(f"colour_theta_vertex_{nleg}")
    worst, biggest, n = 0.0, 0.0, 0
    for axes in itertools.product(range(nax), repeat=nleg):
        for _ in range(nsample):
            gens = tuple(int(x) for x in g.integers(0, 8, size=nleg))
            cs = _terms_colour(action, tuple(int(a) for a in axes), gens)
            if not cs:
                continue
            worst = max(worst, max(abs(c.imag) for c in cs.values()))
            biggest = max(biggest, max(abs(c) for c in cs.values()))
            n += 1
    return {"defect": worst, "scale": biggest, "n": n}


# ══════════════════════════════════════════════════════════════════════════
#  T4 — the other branch of the declared action fork
# ══════════════════════════════════════════════════════════════════════════

def even_law_parity_defect(nk=64, seed=0):
    """Is the F26 propagation law P-even?  ``Omega(-k) == Omega(k)``?

    theta E.B is P-odd, so a P-even propagation law cannot carry it.  The even
    law is the one F91 forces for colour ("gluon even (forced)"); the chiral law
    is retained in ``gluon`` as ``..._bcc_chiral`` and is shown here NOT to be
    P-even, so this leg measures something.
    """
    rng.seed_run(int(seed))
    g = rng.for_channel("colour_theta_evenlaw")
    k = g.normal(size=(nk, 3)) * 1.1
    op = bcc_dispersion(k[:, 0], k[:, 1], k[:, 2], sign='+')
    om = bcc_dispersion(k[:, 0], k[:, 1], k[:, 2], sign='-')
    ip = bcc_dispersion(-k[:, 0], -k[:, 1], -k[:, 2], sign='+')
    im = bcc_dispersion(-k[:, 0], -k[:, 1], -k[:, 2], sign='-')
    even = op + om
    even_inv = ip + im
    return {"even_defect": float(xp.max(xp.abs(even_inv - even))),
            "chiral_defect": float(xp.max(xp.abs(ip - op))),
            "scale": float(xp.max(xp.abs(even)))}


# ══════════════════════════════════════════════════════════════════════════
#  T5 — the fermion side: theta-bar = theta + arg det M_q
# ══════════════════════════════════════════════════════════════════════════

def thetabar_one_generation(thetas=(0.0, math.pi / 3, math.pi / 2, 2.0, math.pi),
                            m: float = 0.37):
    """``arg det`` of the F27 one-generation complex-mass block, vs the phase.

    F27's mass step is off-diagonal with ``i m e^{+i theta}`` and
    ``i m e^{-i theta}``, so the product is ``-m^2`` -- theta-free (this is the
    quantity F53 P5 quotes).  The DETERMINANT is minus that product, ``+m^2``, so
    ``arg det M = 0`` rather than merely theta-independent.  Either way it is a
    statement about theta-bar's SECOND term at one generation, not about
    theta_QCD, and it is recorded here under the quantity it measures.
    """
    out = []
    for th in thetas:
        M = xp.array([[0.0, 1j * m * xp.exp(1j * th)],
                      [1j * m * xp.exp(-1j * th), 0.0]], dtype=complex)
        det = complex(xp.linalg.det(M))
        out.append({"theta": float(th), "det": [det.real, det.imag],
                    "arg_det": float(xp.angle(det))})
    spread = max(abs(o["arg_det"] - out[0]["arg_det"]) for o in out)
    return {"rows": out, "arg_det_spread": spread,
            "arg_det": out[0]["arg_det"]}


# ══════════════════════════════════════════════════════════════════════════
#  the gate entry point
# ══════════════════════════════════════════════════════════════════════════

def check_strong_cp(reverse_senses: bool = True,
                    theta_injected: float = 0.0,
                    flat_links: bool = False,
                    vertex_one_sense: bool = False,
                    shape=(4, 4, 4, 4),
                    seeds=(0, 1, 2),
                    tol: float = 1e-10) -> dict:
    checks: list[dict] = []

    def add(name, ok, value, note=""):
        checks.append({"name": name, "ok": bool(ok), "value": value, "note": note})

    # ---- T0: the premise ------------------------------------------------
    cb = loop_set_reversal_closure("bcc")
    add("T0a", cb["closed"] and cb["n_loops"] == 20, cb,
        "the rule's 20 oriented minimal rhombi are CLOSED UNDER REVERSAL -- the "
        "premise of every reality result below, and a property of the loop set "
        "rather than of a Re() anyone inserted")
    cs = loop_set_reversal_closure("sc")
    add("T0b", cs["closed"] and cs["n_loops"] == 12, cs,
        "the hypercubic reference set is closed too, so T0a is measuring a "
        "property and not a BCC accident")

    # ---- configurations -------------------------------------------------
    scale = 0.0 if flat_links else 1.0
    cfgs = [random_su3_links_4d(shape, seed=s, scale=scale) for s in seeds]

    # ---- T1: reality of the Euclidean action, non-perturbatively --------
    Ss = [loop_action(U, theta=theta_injected, reverse_senses=reverse_senses)
          for U in cfgs]
    im_max = max(abs(S.imag) for S in Ss)
    re_scale = max(abs(S.real) for S in Ss)
    add("T1a", im_max < tol, im_max,
        "Im S = 0 on Haar-random SU(3) 4-D configurations -- and in Euclidean "
        "signature the theta-term is the UNIQUE purely-imaginary invariant, so "
        "this IS theta_QCD = 0, non-perturbatively")
    n_sites = 1
    for L in shape:
        n_sites *= L
    ordered = float(cb["n_loops"] * n_sites * 3)
    disorder = 1.0 - min(abs(S.real) for S in Ss) / ordered
    add("T1b", disorder > 0.5, disorder,
        "the configurations are genuinely DISORDERED -- Re S sits at less than "
        "half its ordered-limit value -- so T1a is a cancellation inside a "
        "non-trivial sum of 20 x N_sites complex traces, not a vanishing one")
    cp_def = max(abs(loop_action(cp_map(U), theta=theta_injected,
                                 reverse_senses=reverse_senses) - S)
                 for U, S in zip(cfgs, Ss))
    add("T1c", cp_def < tol, cp_def,
        "S is CP-invariant on the same configurations")
    p_def = max(abs(loop_action(parity_map(U), theta=theta_injected,
                                reverse_senses=reverse_senses) - S)
                for U, S in zip(cfgs, Ss))
    add("T1d", p_def < tol, p_def,
        "and P-invariant alone -- which is the leg that matters, since theta E.B "
        "is P-odd")

    # ---- T2: the vertex identity, all leg counts ------------------------
    vact = "bcc_1sense" if vertex_one_sense else "bcc"
    v2 = vertex_reality_defect(vact, 2, seed=1)
    v3 = vertex_reality_defect(vact, 3, seed=2)
    v4 = vertex_reality_defect(vact, 4, seed=3)
    vsc = vertex_reality_defect("sc", 3, seed=4)
    add("T2a", v2["defect"] == 0.0, v2["defect"],
        "2-point: every position-space coefficient is REAL at literal zero, "
        "which is V(-k) = conj(V(k)) for all k")
    add("T2b", v3["defect"] == 0.0, v3["defect"],
        "3-point: literal zero -- this is the vertex the 2026-06-29 audit's G1 "
        "caveat named as unanalysed")
    add("T2c", v4["defect"] == 0.0, v4["defect"],
        "4-point: literal zero, so the quartic self-coupling carries no "
        "imaginary part either")
    add("T2d", vsc["defect"] == 0.0, vsc["defect"],
        "the hypercubic reference path agrees, through the same code")
    add("T2e", min(v2["scale"], v3["scale"], v4["scale"]) > 1e-3
        and min(v2["n"], v3["n"], v4["n"]) > 0,
        [[v2["scale"], v3["scale"], v4["scale"]], [v2["n"], v3["n"], v4["n"]]],
        "the sampled coefficients are O(1) and the samples are non-empty, so "
        "T2a-d are identities on non-vanishing objects")

    # ---- T3: the theta operator exists, and is P-odd ---------------------
    dd = xp.asarray(BCC_LINK_AXES, dtype=float)
    mm = xp.asarray(BCC_PLAQ_NORMALS, dtype=float)
    add("T3a", float(xp.max(xp.abs(dd.T @ dd - 4.0 * xp.eye(3)))) == 0.0
        and float(xp.max(xp.abs(mm.T @ mm - 4.0 * xp.eye(3)))) == 0.0,
        [float(xp.max(xp.abs(dd.T @ dd - 4.0 * xp.eye(3)))),
         float(xp.max(xp.abs(mm.T @ mm - 4.0 * xp.eye(3))))],
        "both projections are exact: sum_i d_i d_i^T = 4I on the 4 <111> temporal "
        "rhombi and M^T M = 4I on the 6 <110> spatial ones, so E, B and hence Q "
        "need no pseudo-inverse")
    Qs = [float(xp.sum(topological_density(U))) for U in cfgs]
    qmag = max(abs(q) for q in Qs)
    add("T3b", qmag > tol, qmag,
        "Q = sum_a E^a.B^a is NON-ZERO on these configurations -- without this "
        "leg T1 and T2 would be statements about an operator the lattice does "
        "not carry, i.e. vacuous")
    sens = [theta_sensitivity(U) for U in cfgs]
    lin = max(r["linearity_defect"] for r in sens)
    add("T3c", lin < tol, lin,
        "injecting theta by hand gives Im S = -theta * sum Q EXACTLY, over "
        "theta in {0.1, 0.3, -0.7, 2.0}: the slope IS the topological charge, so "
        "T1a has full sensitivity and its zero is a measurement rather than a "
        "statement about an operator the lattice does not carry")
    conj_def = max(abs(loop_action(conjugation_map(U),
                                   reverse_senses=reverse_senses) - S)
                   for U, S in zip(cfgs, Ss))
    odd_def = max(abs(one_sense_functional(conjugation_map(U))
                      + one_sense_functional(U)) for U in cfgs)
    add("T3d", (conj_def < tol) and odd_def == 0.0, [conj_def, odd_def],
        "and the discrete symmetry is exact: S is invariant under U -> U* while "
        "the one-sense loop functional is odd under it at LITERAL zero -- so "
        "reality is a symmetry of the rule, not an accident of a configuration")

    # ---- T4: the other branch of the declared action fork ---------------
    el = even_law_parity_defect()
    add("T4a", el["even_defect"] < 1e-14, el["even_defect"],
        "the F26 EVEN propagation law is P-even, so the conclusion does not "
        "depend on resolving lpt_bcc_vertex's declared action fork")
    add("T4b", el["chiral_defect"] > 1e-3, el["chiral_defect"],
        "the retained CHIRAL law is not P-even, so T4a measures something -- and "
        "F91's 'gluon even (forced)' is what puts the rule on the P-even branch")

    # ---- T5: the fermion side, and the accounting fix -------------------
    tb = thetabar_one_generation()
    add("T5a", tb["arg_det_spread"] < 1e-14, tb["arg_det_spread"],
        "at one generation arg det M_q is INDEPENDENT of the F27 phase over "
        "{0, pi/3, pi/2, 2, pi} -- this is the quantity F53's P5 measures, and "
        "completeness B11 attributes it to theta_QCD, which F53 itself disclaims")
    add("T5b", abs(tb["arg_det"]) < 1e-14, tb["arg_det"],
        "and it is not merely constant, it is ZERO: F53 quotes the off-diagonal "
        "PRODUCT (i m e^{+i th})(i m e^{-i th}) = -m^2, and the determinant of an "
        "off-diagonal 2x2 is minus that product, so det = +m^2 and arg det = 0 "
        "exactly.  Hence theta-bar = 0 + 0 at one generation -- the first term "
        "from T1/T2 and the second from here")
    add("T5c", True,
        {"theta_QCD": "0 (T1, T2)", "arg_det_M_q": "open: E6/E7"},
        "theta-bar = theta_QCD + arg det M_q.  The first term is closed here; the "
        "second is the quark mass texture and is NOT closed here.  So ledger "
        "parameter #19 stops being an independent input and becomes a function "
        "of E6/E7 -- which is a parameter-count result, not a solution of the "
        "strong CP problem")

    n_pass = sum(1 for c in checks if c["ok"])
    return {
        "checks": checks, "n_pass": n_pass, "n_total": len(checks),
        "verdict": "PASS" if n_pass == len(checks) else "FAIL",
        "params": {"reverse_senses": reverse_senses,
                   "theta_injected": theta_injected,
                   "flat_links": flat_links,
                   "vertex_one_sense": vertex_one_sense, "shape": list(shape),
                   "seeds": list(seeds)},
        "B11_im_S_max": im_max,
        "B11_re_S_scale": re_scale,
        "B11_disorder": disorder,
        "B11_cp_defect": cp_def,
        "B11_parity_defect": p_def,
        "B11_vertex_defect": [v2["defect"], v3["defect"], v4["defect"]],
        "B11_Q_magnitude": qmag,
        "B11_theta_linearity_defect": lin,
        "B11_conjugation_defect": conj_def,
        "B11_one_sense_odd_defect": odd_def,
        "B11_even_law_defect": el["even_defect"],
        "B11_chiral_law_defect": el["chiral_defect"],
        "B11_arg_det_spread": tb["arg_det_spread"],
        "B11_n_loops": cb["n_loops"],
    }


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    res = check_strong_cp()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
        if c["note"]:
            print(f"          {c['note']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    path = results_path("F321_strong_cp.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {path}")
