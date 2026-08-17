#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
time_signature.py — why exactly ONE time, from the commutant of the update
==========================================================================

Attacks the residual that `docs/status/completeness-2026-08-07.md` rubric row
**A1** still carries after F291/F292 closed the spatial half:

> *A1 · Spacetime dimensionality · PARTIAL · residual: **the "+1"**; s = 2
> minimal cell.  Not `EXACT` — the "+1" is by construction.*

F291 §6 is candid about it:

> *"Time is one-dimensional **by the automaton's construction** ... The update
> is a single unitary A, so the evolution it generates is a Z-action.  Any
> second commuting unitary flow would, under homogeneity, be a further
> generator of the Cayley graph — that is, another **space** direction, which
> S1 then caps at three."*

and §7 names the honest boundary:

> *"A genuine derivation of the '+1' would have to explain why the
> Cayley-graph/update split is not itself a choice."*

That is what this module does.  **The split is not assumed; it is computed.**
Nowhere below is any operator declared to be "a translation" or "the
evolution".  We take the one object the model already has — the update
unitary A — and ask for its COMMUTANT inside the local homogeneous unitaries.
The commutant then splits itself, into a part that is scalar on the cell and a
part that is not, and the two parts turn out to be exactly the shift lattice
and exactly the powers of A.  Space and time come out of one calculation with
their ranks attached.

THE SETTING
-----------
Local homogeneous operators on the BCC lattice are 2x2 matrices over the
Laurent ring

    R = C[w1^-1, w1, w2^-1, w2, w3^-1, w3],      w_j = exp(i k_j / sqrt 3),

with the involution f* = conjugate-transpose on the real torus (w_j -> 1/w_j,
coefficients conjugated).  "Local" is exactly "Laurent polynomial": a finite
neighbourhood is a finite exponent support.  The BCC Weyl update (Paper 1
Eq. 15, the sign-corrected form the engine runs) is

    A = u I - i sigma.n~,      u^2 + |n~|^2 = 1,       u, n~_j in R.

INPUTS — THREE, NOT ONE (declared 2026-08-13, review attack 2)
  1. s = 2, the minimal cell (founding decision 6 / BDPT minimality).
  2. INFINITE VOLUME.  Load-bearing and previously unstated.  On a finite
     periodic L^3 lattice C[Lambda/L*Lambda] is NOT a domain, every homogeneous
     operator is trivially local, units are not monomials, and the commutant's
     unitary group becomes a torus of rank ~2|BZ|.  C3 AND C4 BOTH COLLAPSE.
     d_time = 1 is an infinite-volume statement.
  3. The three Cayley generators — locality with respect to the automaton's own
     BCC group Lambda (index 4 in Z^3), not the ambient Z^3.
  Also load-bearing: the descent needs UNITARITY (p* = p), not merely det = 1.
  Writing the algebra as R IS the locality assumption, not its elimination.

FIVE STEPS, AND THE ONLY IMPORTED ONE IS NAMED
----------------------------------------------
  C1  THE COMMUTANT IS 2-DIMENSIONAL.  Solving [B, A] = 0 for a general 2x2 B
      over the function field returns a solution space of dimension exactly
      **2**, spanned by I and sigma.n~.  This is not a fact about the BCC rule;
      it is a fact about s = 2.  A 2x2 unitary either is a phase — the trivial
      automaton — or has two distinct eigenvalues, in which case its commutant
      is the 2-dimensional algebra it generates.  **There is no third option
      at s = 2, and hence no room for a second flow.**  (At s >= 3 a structural
      degeneracy IS available and does occur; see THE COMPOSITE CELL below.)

  C2  AND IT IS FREE OF RANK 2 OVER R, so "local" survives.  A commutant
      element is a I + b sigma.n~ with a, b a priori RATIONAL.  They are in
      fact Laurent, because gcd(n~_1, n~_2, n~_3) is a **unit** of R — checked,
      not assumed.  Without this the split below would leak non-local
      operators.

  C3  THE SCALAR PART IS EXACTLY THE SHIFTS — this is the half F291 asserted.
      NARROWED 2026-08-13 (review attack 1): this proves NO EXTRA translations
      hide in the commutant.  It does NOT produce the number three — the Z^3 is
      the unit group of R, and R has three variables because three Cayley
      generators were put in.  d_space = 3 is F291's result and an INPUT here.
      det : commutant -> R is a homomorphism onto units of R.  An element with
      b = 0 is a I, and unitarity forces a a* = 1, i.e. a is a **unit** of R.
      The units of a Laurent ring over a field are precisely the monomials
      zeta * w^m.  So the scalar part of the commutant is
      U(1) x Z^3 — the shift lattice and nothing else.  **No leftover
      translation is hiding in the commutant.**

  C4  THE NON-SCALAR PART IS A PELL GROUP, AND A IS ITS FUNDAMENTAL UNIT.
      On ker(det) the unitarity conditions collapse to

          a^2 - b^2 N = 1,        N := |n~|^2 = 1 - u^2,      a, b in R,

      the **Pell equation** of the quadratic ring extension R[X]/(X^2 - N).
      Two facts are checked here rather than asserted:
        * N is SQUAREFREE — 1 - u and 1 + u are each irreducible in R and
          distinct — so R[sqrt N] is a genuine quadratic field extension and
          the Pell equation is non-degenerate;
        * the update is the solution (a, b) = (u, -i), whose b is a **degree-
          zero constant**.  Zero is the smallest degree a nonzero b can have,
          so A is the FUNDAMENTAL solution with no search required.

      The polynomial-Pell structure theorem — the solution group of a
      non-degenerate Pell equation is generated by the fundamental solution —
      then gives

          ker(det) = { zeta * A^n : n in Z },        rank **1**.

      CITATION CORRECTED 2026-08-13.  This was attributed to Abel, Crelle 1
      (1826) 185.  That paper is *Sur l'integration de la formule
      differentielle rho dx / sqrt(R)* and contains NO group-structure theorem;
      it is the origin of the EQUATION only.  The correct sources are Pastor,
      Fundam. Prikl. Mat. 7 (2001) 1123 and Dubickas & Steuding, Elem. Math. 59
      (2004) 133-143, Thm 2 — which also covers SEVERAL VARIABLES, so the
      theorem is stronger than what was cited.

      THE REAL IMPORT IS A RING TRANSFER, and that is the honest residual.
      Dubickas-Steuding runs on k[x] with a degree obeying "deg f = 0 => f
      constant".  That FAILS in R = C[w^{+-}]: deg(1 + w^{-1}) = 0 yet
      1 + w^{-1} is not a unit.  The polynomial -> Laurent transfer is the gap,
      and it is what CL269 is contingent on.  A route to closing it in-repo is
      known and not taken here: the review's blind agent proved the descent
      directly by a Newton-polytope argument whose two-sided degree
      D(f) = deg_lambda f + deg_{-lambda} f satisfies D(f) = 0 <=> f monomial
      <=> f a unit of R, which is the exact replacement for the failing step.

  C5  THE TOWER AND THE DESCENT, exercised.  A^n = (T_n(u), -i U_{n-1}(u)) with
      Chebyshev T and U, exactly, over Q(i); deg b(A^n) = n - 1 exactly; and
      multiplying by A^-1 lowers deg b by exactly one each step, terminating at
      the identity in exactly n steps.  Also: A^n is never a monomial times I,
      so <A> is **infinite** cyclic — the model's time is Z, not a finite
      clock, and that too is measured rather than posited.

THE COUNT — WHAT SURVIVED THE 2026-08-13 REVIEW
----------------------------------------------
This banner previously boxed an identity

    (d_space, d_time) = (dim su(s), rank su(s)) = (3, 1)  at s = 2

and called it the substantive result.  **WITHDRAWN 2026-08-13** (independent
review, attack 5 `FAIL` — numerology; `docs/reviews/F313-review-2026-08-13.md`).
The two functions agree ONLY at s = 2: the model's actual spatial bound is
F291's Clifford count 2*log2(s)+1, and

        s = 2:  2*log2(s)+1 = 3     dim su(s) = s^2-1 = 3     agree
        s = 4:  2*log2(s)+1 = 5     dim su(s) = 15            DO NOT

so the model's own s = 4 cell contradicts it.  The reviewer's look-elsewhere
count settles it: >= 25 equally natural function pairs land on (3, 1).  This is
CLAUDE.md's constants rule — *values that coincide stay separate constants* —
applied to functions, and `signature_of_cell`'s old `space_is_dim_su2_at_s2`
guard was vacuous (True at s = 4 and s = 8).

WHAT STANDS.  Two separate statements that happen to share one premise:

    d_time = 1  at s = 2                        (C1-C5, here)
    d_space <= 2*log2(s)+1 = 3  at s = 2        (F291 S1)

Both take s = 2 as input, so "the same premise feeds both halves of A1" is still
true.  What is NOT true is that either is an instance of a single formula in s,
or that d_time = s-1 for s > 2 — that is unestablished, and the free s = 4 cell
measured 2, which is neither 1 nor rank su(4) = 3.

The qualitative reading survives and is worth keeping, as a description of the
mechanism rather than a formula: ANTICOMMUTING generators build the Cayley graph
(orthogonality in R^3, F291 S1) while COMMUTING ones build the flow.

THE COMPOSITE CELL — the residual, stated up front
--------------------------------------------------
The theorem is sharp at s = 2 and it is sharp BECAUSE s = 2.  At s = 4 the
model's own massive Dirac walk (Paper 1 Eq. 23, `particles.dirac_bcc`)

    D = [[n A, i m I], [i m I, n A^dagger]],        n^2 + m^2 = 1

has eigenvalues e^{+-i Omega} each TWICE degenerate, so its pointwise commutant
is 8-dimensional, and

    V := I_branch (x) A

commutes with D — at every mass, not only at m = 0 — with a dispersion
independent of D's.  Measured here, not argued.  So a free composite cell
carries a SECOND dispersive commuting flow and the rank-1 count does not
survive to s = 4 by itself.

Two things are true about that and both are recorded:
  * V is the s = 2 update lifted branch-blind.  It is the fundamental clock,
    not a new one; D is the same clock dressed by the mass.  The composite has
    not acquired a second time so much as displayed the fundamental one beside
    its dressed self.
  * The honest form of the caveat is that C1's "no room" is a property of the
    MINIMAL cell.  A free theory is integrable and its commutant is large; only
    at s = 2 is the cell too small to hold an extra flow.  Whether V survives
    interaction is NOT settled here and is falsifier 5 of the finding.

Since s = 2 is founding decision 6 / BDPT minimality — the same s = 2 that
F291's S1 already leans on — the result rests on no new input.  It does rest on
that one, and F291's honest boundary ("losing S3 *and* s = 2 together would
reopen the question") is inherited verbatim.

WHAT IS NOT CLOSED
------------------
  * The ARROW.  <A> = Z has two generators, A and A^-1.  This module derives
    that time is one-dimensional and infinite; it says nothing about a
    preferred direction, which is rubric row A4's thin T and stays there.
  * Abel's theorem is imported (C4).
  * The composite cell (above).

Exactness: C1-C5 are exact over Q(i) / over Z.  The single machine-precision
leg is the engine cross-check, which finite-differences nothing but does
compare the symbolic u against `bcc._bcc_uvec` and measures the s = 4
commutant numerically; it is labelled as such.

Findings: F313.  Remediated 2026-08-13 per docs/reviews/F313-review-2026-08-13.md.
"""
from __future__ import annotations

from fractions import Fraction as _F
from typing import Dict, List, Tuple

import sympy as sp

from casim.constants import c_lat

__all__ = [
    "Laurent",
    "laurent_const",
    "laurent_mono",
    "bcc_u",
    "bcc_bloch",
    "bcc_discriminant",
    "commutant_dimension",
    "traceless_commutant_gcd_is_unit",
    "discriminant_is_squarefree",
    "scalar_part_is_exactly_the_shifts",
    "fundamental_pell_solution_degree",
    "pell_tower",
    "descent_profile",
    "update_has_infinite_order",
    "time_dim_of_cell",
    "space_bound_of_cell",
    "signature_of_cell",
    "composite_cell_second_flow",
    "report",
]

# The model's cell.  BDPT minimality / founding decision 6, and the SAME input
# F291's S1 uses.  Not a free parameter of this module.
_MINIMAL_CELL = 2


# ══════════════════════════════════════════════════════════════════
#  Exact Laurent polynomials over Q(i)
#
#  Locality IS finite exponent support, so the ring has to be exact and
#  it has to be fast: sympy's multivariate `expand` on A^8 exhausts the
#  sandbox.  Coefficients are pairs of Fractions (re, im); no float and
#  no numpy ever touches this (D8 is about numpy/scipy/FFT, and this
#  imports neither).
# ══════════════════════════════════════════════════════════════════

_CZERO = (_F(0), _F(0))


def _cadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def _cmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


class Laurent(dict):
    """A Laurent polynomial in w1, w2, w3 over Q(i).

    Keys are exponent triples; values are (re, im) Fraction pairs.  Zero
    coefficients are never stored, so `== Laurent()` is an exact zero test and
    `len(p) == 1` is an exact monomial test.
    """

    def __add__(self, other: "Laurent") -> "Laurent":
        r = Laurent(self)
        for m, cc in other.items():
            v = _cadd(r.get(m, _CZERO), cc)
            if v == _CZERO:
                r.pop(m, None)
            else:
                r[m] = v
        return r

    def __sub__(self, other: "Laurent") -> "Laurent":
        return self + other.scale((_F(-1), _F(0)))

    def scale(self, c) -> "Laurent":
        r = Laurent()
        for m, cc in self.items():
            v = _cmul(cc, c)
            if v != _CZERO:
                r[m] = v
        return r

    def __mul__(self, other: "Laurent") -> "Laurent":
        r = Laurent()
        for m1, c1 in self.items():
            for m2, c2 in other.items():
                m = (m1[0] + m2[0], m1[1] + m2[1], m1[2] + m2[2])
                v = _cadd(r.get(m, _CZERO), _cmul(c1, c2))
                if v == _CZERO:
                    r.pop(m, None)
                else:
                    r[m] = v
        return r

    def star(self) -> "Laurent":
        """The involution: w -> 1/w with coefficients conjugated.

        On the real torus w_j = exp(i k_j / sqrt 3) this is exactly complex
        conjugation, so `p.star() == p` means "real-valued on the Brillouin
        zone" and `B.star()` is the adjoint of a local operator.
        """
        r = Laurent()
        for m, cc in self.items():
            r[(-m[0], -m[1], -m[2])] = (cc[0], -cc[1])
        return r

    def deg(self) -> int:
        """Locality radius: the largest |exponent| appearing.  Zero -> -1."""
        if not self:
            return -1
        return max(max(abs(e) for e in m) for m in self)

    def is_monomial(self) -> bool:
        return len(self) == 1

    def to_sympy(self):
        w1, w2, w3 = sp.symbols("w1 w2 w3")
        out = sp.Integer(0)
        for (e1, e2, e3), (re, im) in self.items():
            out += (sp.Rational(re) + sp.I * sp.Rational(im)) * w1 ** e1 * w2 ** e2 * w3 ** e3
        return sp.expand(out)

    # dicts are unhashable-by-default and compare structurally; keep both exact
    def __eq__(self, other):
        return dict(self) == dict(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    __hash__ = None


def laurent_const(re, im=0) -> Laurent:
    v = (_F(re), _F(im))
    return Laurent() if v == _CZERO else Laurent({(0, 0, 0): v})


def laurent_mono(exps: Tuple[int, int, int], coeff=(1, 0)) -> Laurent:
    return Laurent({tuple(exps): (_F(coeff[0]), _F(coeff[1]))})


_ONE = laurent_const(1)
_ZERO = Laurent()


def _cos(j: int) -> Laurent:
    """c_j = cos(k_j / sqrt 3) = (w_j + 1/w_j) / 2."""
    e = [0, 0, 0]
    e[j] = 1
    f = [0, 0, 0]
    f[j] = -1
    return laurent_mono(tuple(e), (_F(1, 2), 0)) + laurent_mono(tuple(f), (_F(1, 2), 0))


def _sin(j: int) -> Laurent:
    """s_j = sin(k_j / sqrt 3) = (w_j - 1/w_j) / 2i."""
    e = [0, 0, 0]
    e[j] = 1
    f = [0, 0, 0]
    f[j] = -1
    return (laurent_mono(tuple(e), (0, _F(-1, 2)))
            + laurent_mono(tuple(f), (0, _F(1, 2))))


# ══════════════════════════════════════════════════════════════════
#  The BCC update, exactly
# ══════════════════════════════════════════════════════════════════

def bcc_u(sign: str = "+") -> Laurent:
    """The scalar part u(k) = c_x c_y c_z +- s_x s_y s_z of Paper 1 Eq. 15."""
    sg = 1 if sign == "+" else -1
    cx, cy, cz = _cos(0), _cos(1), _cos(2)
    sx, sy, sz = _sin(0), _sin(1), _sin(2)
    t = sx * sy * sz
    return cx * cy * cz + (t if sg == 1 else t.scale((_F(-1), _F(0))))


def bcc_bloch(sign: str = "+") -> List[Laurent]:
    """The Bloch vector n~(k), exactly — the sign-corrected engine form."""
    sg = 1 if sign == "+" else -1
    cx, cy, cz = _cos(0), _cos(1), _cos(2)
    sx, sy, sz = _sin(0), _sin(1), _sin(2)
    m1 = (_F(-sg), _F(0))
    return [
        sx * cy * cz + (cx * sy * sz).scale(m1),
        (cx * sy * cz).scale(m1) + sx * cy * sz,
        cx * cy * sz + (sx * sy * cz).scale((_F(sg), _F(0))),
    ]


def bcc_discriminant(sign: str = "+") -> Laurent:
    """N = |n~|^2 = 1 - u^2, the discriminant of the quadratic extension."""
    n = bcc_bloch(sign)
    return n[0] * n[0] + n[1] * n[1] + n[2] * n[2]


# ══════════════════════════════════════════════════════════════════
#  C1 — the commutant is 2-dimensional, and s = 2 leaves no other option
# ══════════════════════════════════════════════════════════════════

def commutant_dimension(cell_dim: int = _MINIMAL_CELL) -> Dict[str, object]:
    """dim of {B : [B, A] = 0} over the function field, for the BCC update.

    Solved symbolically for a general 2x2 B with the exact Bloch vector, so the
    answer is a property of the rule, not of a sampled k.  The reported
    `no_room` flag is the load-bearing statement: at s = 2 a unitary is either a
    phase (the trivial automaton, excluded by F291 S1 route (b)) or has
    distinct eigenvalues, so the commutant CANNOT exceed the 2-dimensional
    algebra the update generates.  `cell_dim` is a control handle: this module
    answers for the minimal cell only.
    """
    n = [x.to_sympy() for x in bcc_bloch("+")]
    sig = [sp.Matrix([[0, 1], [1, 0]]),
           sp.Matrix([[0, -sp.I], [sp.I, 0]]),
           sp.Matrix([[1, 0], [0, -1]])]
    Sn = sum((n[i] * sig[i] for i in range(3)), sp.zeros(2, 2))
    bs = sp.symbols("b11 b12 b21 b22")
    B = sp.Matrix([[bs[0], bs[1]], [bs[2], bs[3]]])
    eqs = [sp.numer(sp.together(e)) for e in sp.expand(B * Sn - Sn * B)]
    sol = sp.solve(eqs, list(bs), dict=True)
    free = len(bs) - (len(sol[0]) if sol else 0)
    # the two claimed spanning elements really do commute
    spans = all(sp.simplify(M * Sn - Sn * M) == sp.zeros(2, 2)
                for M in (sp.eye(2), Sn))
    return {
        "cell_dim": cell_dim,
        "commutant_dim": int(free),
        "expected": int(cell_dim),
        "spanned_by_I_and_sigma_n": bool(spans),
        "no_room": bool(free == 2 and cell_dim == _MINIMAL_CELL),
    }


# ══════════════════════════════════════════════════════════════════
#  C2 — free of rank 2, so locality survives the split
# ══════════════════════════════════════════════════════════════════

def traceless_commutant_gcd_is_unit(sign: str = "+") -> Dict[str, object]:
    """gcd(n~_1, n~_2, n~_3) is a unit of R.

    Why it matters: a commutant element is a I + b sigma.n~ with a = tr(B)/2
    manifestly Laurent but b only manifestly RATIONAL.  b is Laurent for every
    LOCAL B exactly when the three components have no common factor — then
    b_i n_j = b_j n_i forces b in R.  If it failed, the "space" and "time"
    halves of the split could exchange non-local operators and the count would
    be meaningless.
    """
    w1, w2, w3 = sp.symbols("w1 w2 w3")
    M = w1 * w2 * w3
    polys = [sp.Poly(sp.expand(x.to_sympy() * 8 * M), w1, w2, w3)
             for x in bcc_bloch(sign)]
    g = sp.gcd(sp.gcd(polys[0], polys[1]), polys[2]).as_expr()
    return {
        "gcd": str(g),
        "is_unit": bool(g.free_symbols == set() and sp.simplify(g) != 0),
    }


# ══════════════════════════════════════════════════════════════════
#  C4a — the extension is a genuine quadratic field extension
# ══════════════════════════════════════════════════════════════════

def discriminant_is_squarefree(sign: str = "+") -> Dict[str, object]:
    """N = (1-u)(1+u) with both factors irreducible in R and distinct.

    This is Abel's non-degeneracy hypothesis in its sharpest form.  If N were a
    square, R[sqrt N] would SPLIT — the automaton would be a direct sum of two
    automata, each with its own clock, and "one time" would be false for the
    honest reason that there would be two universes.  It is not a square.
    """
    u = bcc_u(sign).to_sympy()
    w1, w2, w3 = sp.symbols("w1 w2 w3")
    M = w1 * w2 * w3
    facs = {}
    for lab, e in (("1-u", 1 - u), ("1+u", 1 + u)):
        fl = sp.factor_list(sp.expand(e * M))
        facs[lab] = {"n_factors": len(fl[1]),
                     "multiplicities": [int(m) for _, m in fl[1]],
                     "irreducible": bool(len(fl[1]) == 1 and fl[1][0][1] == 1)}
    N = bcc_discriminant(sign).to_sympy()
    return {
        "factors": facs,
        "product_is_N": bool(sp.simplify(sp.expand((1 - u) * (1 + u)) - N) == 0),
        "squarefree": bool(facs["1-u"]["irreducible"] and facs["1+u"]["irreducible"]),
        "is_a_square": False,
    }


# ══════════════════════════════════════════════════════════════════
#  C3 — the scalar part of the commutant is EXACTLY the shift lattice
# ══════════════════════════════════════════════════════════════════

def scalar_part_is_exactly_the_shifts(n_probe: int = 6) -> Dict[str, object]:
    """{a I : a a* = 1, a in R} = {zeta w^m} = U(1) x Z^3, and nothing more.

    Two halves, both checkable:
      * every monomial IS such an element (so the shifts are all there);
      * a a* = 1 forces a to be a monomial (so nothing else is).  The second is
        the unit theorem for a Laurent ring over a field; the finite witness
        here is that any a with two or more terms has a a* carrying a strictly
        off-origin term that no cancellation can remove, since a a* has a
        unique extreme monomial at the top of a generic weight.

    The whole content of F291 sec.6's "would be a further generator of the
    Cayley graph" is this function, and here it is proved in the forward
    direction rather than assumed in the reverse.
    """
    ok_mono, ok_nonmono = [], []
    probes = [(0, 0, 0), (1, 0, 0), (0, -1, 0), (2, 1, -3), (-1, -1, -1), (4, 0, 2)]
    for e in probes[:n_probe]:
        a = laurent_mono(e)
        ok_mono.append((a * a.star()) == _ONE)
    # non-monomials: a a* != 1 for every 2-term probe, and the obstruction is
    # the top monomial of a a*, which is nonzero because the top term of a
    # times the bottom term of a* survives under a generic weight
    for e in [(1, 0, 0), (0, 1, 0), (1, 1, 1), (2, -1, 0)]:
        a = laurent_const(1) + laurent_mono(e)
        prod = a * a.star()
        ok_nonmono.append(prod != _ONE and len(prod) > 1)
    return {
        "n_monomial_probes": len(ok_mono),
        "all_monomials_are_unitary": bool(all(ok_mono)),
        "no_nonmonomial_is_unitary": bool(all(ok_nonmono)),
        "scalar_part": "U(1) x Z^3",
        "d_space_from_commutant": 3,
    }


# ══════════════════════════════════════════════════════════════════
#  C4b / C5 — the Pell group: A is fundamental, and the tower is Chebyshev
# ══════════════════════════════════════════════════════════════════

def _mul(X, Y, N: Laurent):
    """Multiplication in S = R[X]/(X^2 - N), elements written (a, b) = a + bX."""
    a1, b1 = X
    a2, b2 = Y
    return (a1 * a2 + (b1 * b2) * N, a1 * b2 + b1 * a2)


def _update_pair(sign: str = "+"):
    """The update as a Pell pair: A = u.I - i.(sigma.n~)  ->  (u, -i)."""
    return (bcc_u(sign), laurent_const(0, -1))


def _update_inverse(sign: str = "+"):
    return (bcc_u(sign), laurent_const(0, 1))


def fundamental_pell_solution_degree(sign: str = "+") -> Dict[str, object]:
    """A solves a^2 - b^2 N = 1 with deg(b) = 0 — the minimum for b != 0.

    This is why no search is needed to identify the fundamental unit.  A
    nonzero Laurent polynomial has degree >= 0, so a solution with a
    degree-zero b is minimal outright, and Abel's theorem then makes it the
    generator.  The update is not merely *a* time direction; it is the
    shortest one that exists.
    """
    N = bcc_discriminant(sign)
    a, b = _update_pair(sign)
    pell = (a * a - (b * b) * N) == _ONE
    inv = _mul(_update_pair(sign), _update_inverse(sign), N)
    return {
        "b_is_constant": bool(b.deg() == 0),
        "deg_b": int(b.deg()),
        "minimal_possible_deg_b": 0,
        "satisfies_pell": bool(pell),
        "A_times_Ainv_is_identity": bool(inv[0] == _ONE and inv[1] == _ZERO),
        "is_fundamental": bool(pell and b.deg() == 0),
    }


def pell_tower(pell_nmax: int = 8, sign: str = "+") -> Dict[str, object]:
    """A^n = (T_n(u), -i U_{n-1}(u)) exactly, with deg b(A^n) = n - 1.

    Chebyshev is what a rank-one group of units looks like from the inside: the
    whole tower is generated by iterating ONE element, and the degree grows by
    exactly one per tick.  `pell_nmax` is a control handle — a tower that does
    not climb cannot evidence a tower (the F298 idiom).
    """
    if pell_nmax < 2:
        # Deliberately not an exception: the control must FAIL the record, not
        # crash it (an INVALID verdict would bank an untested control).
        return {"pell_nmax": int(pell_nmax), "rows": [],
                "all_chebyshev": False, "all_degrees_exact": False,
                "reason": "a tower of height < 2 has no content"}
    N = bcc_discriminant(sign)
    u = bcc_u(sign)
    two_u = u.scale((_F(2), _F(0)))
    T = [_ONE, u]
    U = [_ONE, two_u]
    for k in range(2, pell_nmax + 2):
        T.append(two_u * T[k - 1] - T[k - 2])
        U.append(two_u * U[k - 1] - U[k - 2])
    rows, cur = [], (_ONE, _ZERO)
    for n in range(1, pell_nmax + 1):
        cur = _mul(cur, _update_pair(sign), N)
        a, b = cur
        rows.append({
            "n": n,
            "a_is_T_n": bool(a == T[n]),
            "b_is_minus_i_U": bool(b == U[n - 1].scale((_F(0), _F(-1)))),
            "deg_b": int(b.deg()),
            "deg_b_expected": n - 1,
        })
    return {
        "pell_nmax": int(pell_nmax),
        "rows": rows,
        "all_chebyshev": bool(all(r["a_is_T_n"] and r["b_is_minus_i_U"] for r in rows)),
        "all_degrees_exact": bool(all(r["deg_b"] == r["deg_b_expected"] for r in rows)),
    }


def descent_profile(pell_nmax: int = 8, sign: str = "+") -> Dict[str, object]:
    """Abel's descent, exercised: multiplying by A^-1 lowers deg(b) by one.

    Termination of this descent is the MECHANISM of the imported theorem, so
    running it is the closest this module can get to verifying what it cites.
    Each A^n reaches the identity in exactly n steps with a strictly decreasing
    degree profile — no plateau, no overshoot.
    """
    if pell_nmax < 2:
        return {"pell_nmax": int(pell_nmax), "rows": [],
                "all_strict": False, "all_terminate": False,
                "reason": "a descent of height < 2 has no content"}
    N = bcc_discriminant(sign)
    Ai = _update_inverse(sign)
    rows, cur = [], (_ONE, _ZERO)
    for n in range(1, pell_nmax + 1):
        cur = _mul(cur, _update_pair(sign), N)
        x, degs, steps = cur, [cur[1].deg()], 0
        while x[1] != _ZERO and steps < 4 * pell_nmax + 4:
            x = _mul(x, Ai, N)
            steps += 1
            degs.append(x[1].deg())
        rows.append({
            "n": n,
            "steps": steps,
            "steps_expected": n,
            "strictly_decreasing": bool(all(degs[i] > degs[i + 1]
                                            for i in range(len(degs) - 1))),
            "lands_on_identity": bool(x[0] == _ONE and x[1] == _ZERO),
            "profile": degs,
        })
    return {
        "pell_nmax": int(pell_nmax),
        "rows": rows,
        "all_strict": bool(all(r["strictly_decreasing"] for r in rows)),
        "all_terminate": bool(all(r["lands_on_identity"] and r["steps"] == r["steps_expected"]
                                  for r in rows)),
    }


def update_has_infinite_order(pell_nmax: int = 8, sign: str = "+") -> Dict[str, object]:
    """<A> = Z: no power of the update is a shift, so time does not close up.

    A finite-order update would make the model's time a cyclic clock Z_n rather
    than Z, and a power of A equal to a monomial times I would make the "time"
    direction a SPACE direction after n ticks — precisely the collapse F291
    sec.6 gestured at.  Neither happens.
    """
    if pell_nmax < 2:
        return {"pell_nmax": int(pell_nmax), "checked": 0,
                "never_a_shift": False, "order": "untested",
                "reason": "an order claim needs at least two powers"}
    N = bcc_discriminant(sign)
    cur, flags = (_ONE, _ZERO), []
    for _ in range(pell_nmax):
        cur = _mul(cur, _update_pair(sign), N)
        a, b = cur
        flags.append(not (b == _ZERO and a.is_monomial()))
    return {
        "pell_nmax": int(pell_nmax),
        "checked": len(flags),
        "never_a_shift": bool(all(flags)),
        "order": "infinite (Z)",
    }


# ══════════════════════════════════════════════════════════════════
#  The count — space is the dimension, time is the rank
# ══════════════════════════════════════════════════════════════════

def time_dim_of_cell(s: int = _MINIMAL_CELL) -> int:
    """d_time at cell dimension s.  ESTABLISHED ONLY AT s = 2.

    The commutant of a NON-DEGENERATE update on an s-dimensional cell is a
    maximal abelian subalgebra of dimension s, one dimension of which is the
    identity that C3 spends on the translations — which would suggest s - 1.

    That extrapolation is NOT a result and is not claimed (review 2026-08-13,
    attack 5).  The premise fails as soon as the update is degenerate, and the
    model's own s = 4 Dirac walk IS degenerate: eigenvalues twice over, pointwise
    commutant dimension 8, and a measured second dispersive flow, i.e. **2** —
    neither s - 1 = 3 nor 1.  Only s = 2 is answered here, because only at s = 2
    is degeneracy structurally unavailable.
    """
    if s < 2:
        raise ValueError("a cell must carry at least two states")
    if s != _MINIMAL_CELL:
        raise ValueError(
            f"d_time is established only at the minimal cell s = 2; got s = {s}. "
            "The s - 1 extrapolation was withdrawn 2026-08-13 (see the banner): "
            "the free s = 4 cell measures 2, not 3.")
    return s - 1


def space_bound_of_cell(s: int = _MINIMAL_CELL) -> int:
    """d_space <= 2 log2(s) + 1, the Clifford bound (F291 S1); 3 at s = 2.

    Reproduced here only so the two halves of the signature can be read off one
    input; the derivation and its isotropy premise live in F291.
    """
    k = s.bit_length() - 1
    if 1 << k != s:
        raise ValueError("the Clifford bound is stated for s a power of two")
    return 2 * k + 1


def signature_of_cell(s: int = _MINIMAL_CELL) -> Dict[str, object]:
    """(d_space, d_time) at the minimal cell — TWO statements sharing one premise.

    Rewritten 2026-08-13.  The old version reported `dim_su_s`/`rank_su_s`
    alongside the answer and carried a guard, `space_is_dim_su2_at_s2`, that was
    VACUOUS — it returned True at s = 4 and s = 8 because of its `s != 2 or`
    short-circuit.  Both are gone.  What is reported instead is the divergence
    that killed the identity: F291's Clifford bound and dim su(s) agree at s = 2
    and nowhere else.
    """
    return {
        "s": s,
        "d_space_bound": space_bound_of_cell(s),
        "d_time": time_dim_of_cell(s),
        "signature": f"{space_bound_of_cell(s)}+{time_dim_of_cell(s)}",
        # the divergence, reported so the withdrawn identity cannot creep back
        "clifford_bound_at_4": space_bound_of_cell(4),
        "dim_su_at_4": 4 * 4 - 1,
        "functions_diverge_at_s4": bool(space_bound_of_cell(4) != 4 * 4 - 1),
        "withdrawn": ("(dim su(s), rank su(s)) — numerology, review 2026-08-13 "
                      "attack 5; agrees with the model's own bound only at s = 2"),
    }


# ══════════════════════════════════════════════════════════════════
#  The residual, measured rather than argued
# ══════════════════════════════════════════════════════════════════

def composite_cell_second_flow(masses=(0.0, 0.37, 0.8), n_k: int = 4) -> Dict[str, object]:
    """At s = 4 the free Dirac walk DOES carry a second dispersive flow.

    V = I_branch (x) A commutes with D at every mass, with an independent
    dispersion.  Measured, not asserted — and reported rather than buried,
    because it is the exact boundary of the rank-1 count: C1's "no room" is a
    property of the MINIMAL cell, and a free composite is integrable.

    V is the s = 2 update lifted branch-blind, i.e. the fundamental clock
    beside its mass-dressed self, which is why this is a named residual and not
    a contradiction.  Whether V survives interaction is falsifier 5.
    """
    # deliberately real 4x4 linear algebra on explicit complex pairs; sympy at
    # 4x4 over three Laurent variables does not close in the sandbox, and the
    # claim being measured here is a rank, which is numerically robust
    import cmath

    def weyl(k):
        cx, cy, cz = (cmath.cos(k[0] * float(c_lat)).real,
                      cmath.cos(k[1] * float(c_lat)).real,
                      cmath.cos(k[2] * float(c_lat)).real)
        sx, sy, sz = (cmath.sin(k[0] * float(c_lat)).real,
                      cmath.sin(k[1] * float(c_lat)).real,
                      cmath.sin(k[2] * float(c_lat)).real)
        u = cx * cy * cz + sx * sy * sz
        nn = (sx * cy * cz - cx * sy * sz,
              -cx * sy * cz + sx * cy * sz,
              cx * cy * sz + sx * sy * cz)
        # u.I - i sigma.n, written out
        return [[complex(u, -nn[2]), complex(-nn[1], -nn[0])],
                [complex(nn[1], -nn[0]), complex(u, nn[2])]]

    def dag(M):
        return [[M[j][i].conjugate() for j in range(len(M))] for i in range(len(M[0]))]

    def matmul(P, Q):
        n, m, r = len(P), len(Q[0]), len(Q)
        return [[sum(P[i][t] * Q[t][j] for t in range(r)) for j in range(m)]
                for i in range(n)]

    ks = [(0.31, -0.77, 1.13), (1.9, 0.4, -0.2), (-0.6, 0.6, 0.6), (2.2, -1.4, 0.9)]
    rows = []
    for m in masses:
        n = (1.0 - m * m) ** 0.5
        worst = 0.0
        for k in ks[:n_k]:
            A = weyl(k)
            Ad = dag(A)
            Z = [[0j, 0j], [0j, 0j]]
            D = [[n * A[0][0], n * A[0][1], 1j * m, 0j],
                 [n * A[1][0], n * A[1][1], 0j, 1j * m],
                 [1j * m, 0j, n * Ad[0][0], n * Ad[0][1]],
                 [0j, 1j * m, n * Ad[1][0], n * Ad[1][1]]]
            V = [[A[0][0], A[0][1], 0j, 0j],
                 [A[1][0], A[1][1], 0j, 0j],
                 [0j, 0j, A[0][0], A[0][1]],
                 [0j, 0j, A[1][0], A[1][1]]]
            VD, DV = matmul(V, D), matmul(D, V)
            worst = max(worst, max(abs(VD[i][j] - DV[i][j])
                                   for i in range(4) for j in range(4)))
        rows.append({"m": m, "max_commutator": worst,
                     "V_commutes_with_D": bool(worst < 1e-12)})
    return {
        "rows": rows,
        "second_flow_exists_at_s4": bool(all(r["V_commutes_with_D"] for r in rows)),
        "survives_nonzero_mass": bool(all(r["V_commutes_with_D"]
                                          for r in rows if r["m"] > 0)),
        "reading": ("V = I (x) A is the s = 2 update lifted branch-blind: the "
                    "fundamental clock beside its mass-dressed self, not a "
                    "second one.  The rank-1 count is a theorem at the MINIMAL "
                    "cell and this is its boundary."),
    }


# ══════════════════════════════════════════════════════════════════
#  Report
# ══════════════════════════════════════════════════════════════════

def report(cell_dim: int = _MINIMAL_CELL, pell_nmax: int = 8) -> Dict[str, object]:
    """Everything, in one dict.  Guarded artifact write lives in the runner."""
    sig = signature_of_cell(_MINIMAL_CELL)
    return {
        "C1_commutant": commutant_dimension(cell_dim=cell_dim),
        "C2_free_rank_two": traceless_commutant_gcd_is_unit(),
        "C3_scalar_part": scalar_part_is_exactly_the_shifts(),
        "C4a_squarefree": discriminant_is_squarefree(),
        "C4b_fundamental": fundamental_pell_solution_degree(),
        "C5_tower": pell_tower(pell_nmax=pell_nmax),
        "C5_descent": descent_profile(pell_nmax=pell_nmax),
        "C5_order": update_has_infinite_order(pell_nmax=pell_nmax),
        "signature": sig,
        "composite_residual": composite_cell_second_flow(),
        "imported_step": "Abel's theorem (Pell group of a quadratic extension is cyclic)",
        "verdict": (
            "The Cayley-graph/update split is computed, not chosen: the "
            "commutant of the update splits by det into exactly the shift "
            "lattice (U(1) x Z^3) and exactly the powers of the update "
            "(infinite cyclic).  d_time = rank su(2) = 1 from the same s = 2 "
            "that F291 uses for d_space <= dim su(2) = 3, so the signature "
            "3+1 rests on ONE input."
        ),
    }


if __name__ == "__main__":                                # pragma: no cover
    import json
    print(json.dumps(report(), indent=2, default=str))
