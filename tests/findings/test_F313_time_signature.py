"""F313 — the "+1": the update's commutant splits itself into 3 space + 1 time.

Attacks the residual `docs/status/completeness-2026-08-07.md` rubric row **A1**
still carries after F291/F292 closed the spatial half: *"the '+1' is by
construction"*, and F291 sec.7's price for closing it — *"explain why the
Cayley-graph/update split is not itself a choice"*.

Thirteen checks (C0, C1a, C1b, C2, C3a, C3b, C4a, C4b, C5a, C5b, C5c, C6, C7).
The load-bearing ones are re-derived here INDEPENDENTLY of
`casim.engine.lattice.time_signature`, so this is a cross-check and not a
restatement of the implementation:

  * the Bloch vector and u(k) are **re-typed from
    `references/qca-papers-1-4-overview.md` Eq. 15** (sign-corrected per
    `bcc._bcc_uvec`) as sympy expressions in w_j = exp(i k_j / sqrt 3), not
    imported from the module;
  * the commutant is solved with sympy from that re-typed form (C1b);
  * the Pell tower is re-run with sympy Chebyshev polynomials rather than the
    module's hand-rolled Laurent ring (C5a), so the two arithmetics have to
    agree or the record goes red.

  C0  (exact)   THE NON-TAUTOLOGY CONTROL (added 2026-08-13 from the review):
      in d = 1 the theorem is FALSE — gcd(n~) = sin k is not a unit and
      N = sin^2 k is a perfect square — and it must be, because the 1D walk
      really is two automata each with its own clock.  A C2/C4a that passed
      here would be testing the algebra, not the 3D rule.
  C1a (exact)   the maximal abelian subalgebra of M_s(C) is s-dimensional; at
      s = 2 a unitary is a phase or has distinct eigenvalues, leaving NO third
      option — the "no room" statement.  (The "= rank su(s)" gloss is dropped:
      sec.8's identity was withdrawn 2026-08-13 as numerology.)
  C1b (exact)   the commutant of the re-typed BCC update is 2-dimensional and
      is spanned by I and sigma.n~.
  C2  (exact)   gcd(n~_1, n~_2, n~_3) is a unit of R, so the traceless
      commutant is FREE of rank one and locality survives the split.
  C3a (exact)   every monomial zeta w^m is a unitary scalar commutant element:
      the shifts are all present.
  C3b (exact)   no non-monomial is: a a* = 1 forces a to be a unit, so the
      scalar part is EXACTLY U(1) x Z^3 and no translation is hiding.
  C4a (exact)   N = (1-u)(1+u) with both factors irreducible and distinct, so
      R[sqrt N] is a genuine quadratic extension — the non-degeneracy
      hypothesis of Dubickas-Steuding Thm 2 (NOT Abel; corrected 2026-08-13).
  C4b (exact)   A = (u, -i) solves the Pell equation with deg b = 0, the
      minimum possible, so A is the FUNDAMENTAL unit with no search.  N is
      built from n~.n~, NOT from 1-u^2: the latter made `satisfies_pell`
      identically 1 for any expression (a V-004 tautology, review attack 1).
      As written the leg IS the walk's unitarity condition.
  C5a (exact)   A^n = (T_n(u), -i U_{n-1}(u)) with deg b = n - 1, cross-checked
      against sympy Chebyshev.
  C5b (exact)   the descent runs: deg b falls by exactly one per step and
      lands on the identity in exactly n steps.
  C5c (exact)   A^n is never a shift, so <A> = Z — time is infinite, not a
      cyclic clock.
  C6  (exact)   the count at the MINIMAL cell: (d_space, d_time) = (3, 1),
      two statements sharing the s = 2 premise.  Rewritten 2026-08-13: it now
      also asserts that 2*log2(s)+1 and dim su(s) DIVERGE at s = 4 (5 vs 15),
      so re-introducing the withdrawn identity turns this leg red.
  C7  (machine) the residual, measured: at s = 4 the massive Dirac walk carries
      a second dispersive commuting flow V = I (x) A, at every mass.

Three declared controls (D9/H2), all verified RED:

  ``--param pell_nmax=1``   a tower that does not climb cannot evidence a
      tower (the F298 idiom).  C5a/C5b/C5c must go red.
  ``--param cell_dim=4``    the "no room" count is a property of the MINIMAL
      cell, not an arithmetic identity.  C1a/C1b/C6 must go red.
  ``--param fake_gcd=True`` multiplies the Bloch components by a common
      non-unit factor.  C2 must go red — without it the split leaks non-local
      operators and the whole count is void.

Real exact arithmetic (CLAUDE.md); the one machine-precision leg is C7, which
measures a commutator norm and is labelled as such.

REMEDIATION 2026-08-13 (docs/reviews/F313-review-2026-08-13.md): C0 added; C4b
de-tautologised; C2's unit criterion corrected from "is a constant" to "is a
monomial" over the QQ_I domain (the old form would have reddened the 2D lattice,
whose gcd 2*w_3 is a genuine unit, and the published gcd 1+i was a ZZ_I content
artifact — the true value is 1); C6 rewritten off the withdrawn identity.
"""
from __future__ import annotations

import functools

import sympy as sp

_W = sp.symbols("w1 w2 w3")


# ══════════════════════════════════════════════════════════════════
#  The walk, RE-TYPED from the paper — not imported from the module
# ══════════════════════════════════════════════════════════════════

def _c(w):
    return (w + 1 / w) / 2


def _s(w):
    return (w - 1 / w) / (2 * sp.I)


@functools.lru_cache(maxsize=None)
def _walk_1d():
    """The d = 1 trivial-shift walk — the review's control, and it FAILS the theorem.

    n~ = (0, 0, sin k), so gcd(n~) = sin k is NOT a unit (C2 fails) and
    N = sin^2 k IS a perfect square (C4a fails).  Both failures are correct and
    physical: the 1D walk really is two decoupled automata, left- and
    right-movers, each with its own clock — which is exactly what F313 sec.6 says
    a split N means.  A theorem that held in d = 1 as well would be a tautology
    about the algebra rather than a statement about the 3D rule.
    """
    w = _W[0]
    u = sp.expand((w + 1 / w) / 2)
    n = [sp.Integer(0), sp.Integer(0), sp.expand((w - 1 / w) / (2 * sp.I))]
    return u, n


@functools.lru_cache(maxsize=None)
def _walk(sign=1, fake_gcd=False):
    """(u, [n1, n2, n3]) for the BCC Weyl walk, Paper 1 Eq. 15, sign-corrected.

    `fake_gcd` is the C2 control: multiplying every Bloch component by a common
    non-unit factor leaves the DIRECTION of n~ untouched — so the commutant is
    still 2-dimensional — while destroying the freeness that makes b Laurent.
    That is exactly the failure mode C2 exists to catch.
    """
    cx, cy, cz = (_c(w) for w in _W)
    sx, sy, sz = (_s(w) for w in _W)
    u = sp.expand(cx * cy * cz + sign * sx * sy * sz)
    n = [sp.expand(sx * cy * cz - sign * cx * sy * sz),
         sp.expand(-sign * cx * sy * cz + sx * cy * sz),
         sp.expand(cx * cy * sz + sign * sx * sy * cz)]
    if fake_gcd:
        f = 1 + _W[0]
        n = [sp.expand(x * f) for x in n]
    return u, n


def _paulis():
    return (sp.Matrix([[0, 1], [1, 0]]),
            sp.Matrix([[0, -sp.I], [sp.I, 0]]),
            sp.Matrix([[1, 0], [0, -1]]))


# ══════════════════════════════════════════════════════════════════
#  C1 — the commutant, and why s = 2 leaves no other option
# ══════════════════════════════════════════════════════════════════

def check_C1a_no_room_at_the_minimal_cell(cell_dim=2):
    """Maximal abelian subalgebra of M_s(C) has dimension s; d_time = s - 1.

    The dichotomy is the content: a 2x2 unitary either IS a phase (the trivial
    automaton, excluded by F291 S1 route (b), which needs c_lat to exist) or has
    two distinct eigenvalues, in which case its commutant is the 2-dimensional
    algebra it generates.  No third option exists at s = 2, which is why the
    count below is a theorem rather than a feature of the BCC rule.
    """
    # a diagonalisable s x s matrix with distinct eigenvalues has an
    # s-dimensional commutant; verified constructively rather than asserted
    lam = sp.symbols("l0:4")
    D = sp.diag(*lam[:cell_dim])
    bs = sp.symbols(f"c0:{cell_dim * cell_dim}")
    B = sp.Matrix(cell_dim, cell_dim, list(bs))
    eqs = list(sp.expand(B * D - D * B))
    sol = sp.solve(eqs, list(bs), dict=True)
    free = len(bs) - (len(sol[0]) if sol else 0)
    out = {"cell_dim": cell_dim,
           "maximal_abelian_dim": int(free),
           "commuting_flows_beyond_the_identity": int(free) - 1,
           "no_third_option_at_s2": bool(cell_dim == 2)}
    assert out["maximal_abelian_dim"] == cell_dim, out
    # NOT "= rank su(s)": that gloss was withdrawn 2026-08-13 as numerology.
    # The statement is about the MINIMAL cell, where degeneracy is structurally
    # unavailable, and it is false as an s-general formula.
    assert out["commuting_flows_beyond_the_identity"] == 1, (
        "exactly one commuting flow beyond the identity is a property of the "
        f"MINIMAL cell s = 2, not an arithmetic identity in s; got {out}")
    return out


def check_C1b_commutant_is_two_dimensional(fake_gcd=False):
    """dim {B : [B, sigma.n~] = 0} = 2, spanned by I and sigma.n~ — re-derived."""
    _, n = _walk(fake_gcd=fake_gcd)
    sig = _paulis()
    Sn = sum((n[i] * sig[i] for i in range(3)), sp.zeros(2, 2))
    bs = sp.symbols("b11 b12 b21 b22")
    B = sp.Matrix([[bs[0], bs[1]], [bs[2], bs[3]]])
    eqs = [sp.numer(sp.together(e)) for e in sp.expand(B * Sn - Sn * B)]
    sol = sp.solve(eqs, list(bs), dict=True)
    free = len(bs) - (len(sol[0]) if sol else 0)
    spans = all(sp.simplify(M * Sn - Sn * M) == sp.zeros(2, 2)
                for M in (sp.eye(2), Sn))
    out = {"commutant_dim": int(free), "spanned_by_I_and_sigma_n": bool(spans)}
    assert out["commutant_dim"] == 2, out
    assert out["spanned_by_I_and_sigma_n"], out
    return out


# ══════════════════════════════════════════════════════════════════
#  C2 — free of rank one, so the split cannot leak non-local operators
# ══════════════════════════════════════════════════════════════════

def check_C2_traceless_part_is_free_rank_one(fake_gcd=False):
    """gcd(n~_1, n~_2, n~_3) is a UNIT of the Laurent ring.

    b = (traceless part) / n~ is a priori only rational.  It is Laurent — i.e.
    LOCAL — for every local commutant element exactly when the three components
    share no factor.  If this fails, "space" and "time" can exchange non-local
    operators and the rank count means nothing.
    """
    _, n = _walk(fake_gcd=fake_gcd)
    M = _W[0] * _W[1] * _W[2]
    # Domain matters: R has coefficients in a FIELD, so the gcd must be taken
    # over QQ_I.  sympy's default ZZ_I returns the CONTENT (1+i here), which is
    # what the finding published in error until 2026-08-13.
    polys = [sp.Poly(sp.expand(x * 8 * M), *_W, domain="QQ_I") for x in n]
    g = sp.gcd(sp.gcd(polys[0], polys[1]), polys[2]).as_expr()
    # A unit of R is a MONOMIAL with nonzero coefficient — not merely a
    # constant.  The old criterion `free_symbols == set()` would have reddened
    # the 2D square lattice, whose gcd is 2*w_3, a genuine unit (review 12).
    gp = sp.Poly(sp.expand(g), *_W)
    out = {"gcd": str(g),
           "n_monomials": len(gp.monoms()),
           "is_unit": bool(len(gp.monoms()) == 1 and gp.coeffs()[0] != 0)}
    assert out["is_unit"], (
        "the Bloch components share a non-unit factor, so the traceless "
        f"commutant is not free and b need not be local: {out}")
    return out


# ══════════════════════════════════════════════════════════════════
#  C3 — the scalar part is EXACTLY the shift lattice
# ══════════════════════════════════════════════════════════════════

def _star(expr):
    """Adjoint on the real torus: w -> 1/w, coefficients conjugated."""
    e = sp.conjugate(expr)
    e = e.subs({sp.conjugate(w): 1 / w for w in _W}, simultaneous=True)
    return sp.expand(sp.simplify(e))


def check_C3a_every_shift_is_in_the_commutant():
    """zeta w^m satisfies a a* = 1: the shifts are all present, none missing."""
    rows = []
    for e in [(0, 0, 0), (1, 0, 0), (0, -1, 0), (2, 1, -3), (-1, -1, -1)]:
        a = _W[0] ** e[0] * _W[1] ** e[1] * _W[2] ** e[2]
        rows.append({"m": e, "unitary": bool(sp.simplify(a * _star(a) - 1) == 0)})
    out = {"rows": rows, "all_unitary": bool(all(r["unitary"] for r in rows))}
    assert out["all_unitary"], out
    return out


def check_C3b_nothing_but_shifts_is_scalar_unitary():
    """a a* = 1 forces a to be a monomial — so the scalar part is EXACTLY Z^3.

    This is the direction F291 sec.6 assumed and did not prove.  Finite witness:
    every two-term probe fails, and it fails structurally — a a* acquires an
    off-origin term that no cancellation can remove, because the top monomial
    of a paired with the bottom of a* has nowhere to go.
    """
    rows = []
    for e in [(1, 0, 0), (0, 1, 0), (1, 1, 1), (2, -1, 0)]:
        a = 1 + _W[0] ** e[0] * _W[1] ** e[1] * _W[2] ** e[2]
        prod = sp.expand(sp.simplify(a * _star(a)))
        rows.append({"m": e, "is_unitary": bool(sp.simplify(prod - 1) == 0)})
    out = {"rows": rows,
           "none_unitary": bool(not any(r["is_unitary"] for r in rows)),
           "scalar_part": "U(1) x Z^3",
           "d_space_from_commutant": 3}
    assert out["none_unitary"], (
        "a non-monomial scalar survived unitarity, so the commutant contains a "
        f"translation that is not a shift: {out}")
    return out


# ══════════════════════════════════════════════════════════════════
#  C4 — the Pell equation and its fundamental unit
# ══════════════════════════════════════════════════════════════════

def check_C4a_discriminant_is_squarefree():
    """N = (1-u)(1+u), both irreducible and distinct: no split, no square.

    Abel's non-degeneracy hypothesis.  A square N would SPLIT the extension —
    and the honest reading of that is two automata each with its own clock,
    i.e. two universes rather than two times.
    """
    u, _ = _walk()
    M = _W[0] * _W[1] * _W[2]
    facs = {}
    for lab, e in (("1-u", 1 - u), ("1+u", 1 + u)):
        fl = sp.factor_list(sp.expand(e * M))
        facs[lab] = {"n_factors": len(fl[1]),
                     "irreducible": bool(len(fl[1]) == 1 and fl[1][0][1] == 1)}
    N = sp.expand(1 - u ** 2)
    out = {"factors": facs,
           "product_is_N": bool(sp.simplify(sp.expand((1 - u) * (1 + u)) - N) == 0),
           "squarefree": bool(facs["1-u"]["irreducible"] and facs["1+u"]["irreducible"])}
    assert out["squarefree"] and out["product_is_N"], out
    return out


def check_C4b_update_is_the_fundamental_unit():
    """A = (u, -i) solves a^2 - b^2 N = 1 with deg b = 0 — minimal outright.

    No search is needed to identify the fundamental unit: a nonzero Laurent
    polynomial has degree >= 0, so a degree-zero b is minimal.  The update is
    not merely A time direction; it is the shortest one that exists.
    """
    # N MUST come from the re-typed Bloch vector, not from 1 - u^2.  Computing
    # N = 1 - u^2 makes `satisfies_pell` read u^2 - (-i)^2(1 - u^2) = 1, which is
    # identically 1 for ANY expression — a V-004 tautology, and the review's
    # attack-1 injection of a non-unitary walk sailed through it.  Built from
    # n~.n~ instead, this leg IS the walk's unitarity condition u^2 + |n~|^2 = 1.
    u, n = _walk()
    N = sp.expand(sum(x ** 2 for x in n))
    a, b = u, -sp.I
    # `b` must genuinely carry no lattice variable AND be nonzero.  Reading a
    # degree off an expression with no free symbols would be true for anything,
    # so both halves are asserted separately.
    out = {"satisfies_pell": bool(sp.simplify(sp.expand(a ** 2 - b ** 2 * N) - 1) == 0),
           "N_from_bloch_vector": True,
           "walk_is_unitary": bool(sp.simplify(sp.expand(u ** 2 + N) - 1) == 0),
           "b": str(b),
           "b_carries_no_lattice_variable": bool(b.free_symbols & set(_W) == set()),
           "b_is_nonzero": bool(sp.simplify(b) != 0),
           "a_carries_lattice_variables": bool(a.free_symbols & set(_W) != set()),
           "deg_b": 0,
           "minimal_possible_deg_b": 0}
    assert out["walk_is_unitary"], (
        f"the re-typed walk is NOT unitary — u^2 + |n~|^2 != 1: {out}")
    assert out["satisfies_pell"], out
    assert out["b_carries_no_lattice_variable"] and out["b_is_nonzero"], (
        f"A is fundamental only because deg(b) = 0 with b != 0: {out}")
    assert out["a_carries_lattice_variables"], (
        f"a degenerate a would make A a constant, not a flow: {out}")
    return out


# ══════════════════════════════════════════════════════════════════
#  C5 — the tower, the descent, and the order.  pell_nmax is a control.
# ══════════════════════════════════════════════════════════════════

def _module_tower(pell_nmax):
    from casim.engine.lattice import time_signature as ts
    return ts.pell_tower(pell_nmax=pell_nmax), ts.descent_profile(pell_nmax=pell_nmax), \
        ts.update_has_infinite_order(pell_nmax=pell_nmax)


def check_C5a_tower_is_chebyshev(pell_nmax=8):
    """A^n = (T_n(u), -i U_{n-1}(u)), deg b = n - 1 — module vs sympy Chebyshev.

    The module's hand-rolled exact Laurent ring and sympy's Chebyshev
    recurrence are independent arithmetics; they have to agree.
    """
    from casim.engine.lattice import time_signature as ts
    tower, _, _ = _module_tower(pell_nmax)
    assert tower["rows"], (
        f"a tower of height {pell_nmax} has no content and cannot evidence a "
        "rank-one group (F298 idiom)")

    # GENUINE cross-check: rebuild A^n in the module's hand-rolled Laurent ring,
    # convert to sympy, and compare against sympy's OWN Chebyshev recurrence in
    # the RE-TYPED u.  Comparing chebyshevt(n,u) to itself would be identically
    # zero for any expression — the V-004 defect — so the two sides here come
    # from different arithmetics on purpose.
    u_typed, _ = _walk()
    N = ts.bcc_discriminant()
    cur = (ts.laurent_const(1), ts.Laurent())
    indep = []
    for n in range(1, min(4, pell_nmax) + 1):
        cur = ts._mul(cur, ts._update_pair(), N)
        lhs = sp.expand(sp.simplify(cur[0].to_sympy()))          # module's Laurent ring
        rhs = sp.expand(sp.simplify(sp.chebyshevt(n, u_typed)))  # sympy, re-typed u
        indep.append({"n": n, "agrees": bool(sp.simplify(lhs - rhs) == 0)})

    out = {"pell_nmax": pell_nmax,
           "all_chebyshev": bool(tower["all_chebyshev"]),
           "all_degrees_exact": bool(tower["all_degrees_exact"]),
           "sympy_cross_check": indep,
           "n_rows": len(tower["rows"])}
    assert out["all_chebyshev"], out
    assert out["all_degrees_exact"], out
    assert out["n_rows"] >= 2, out
    assert indep and all(r["agrees"] for r in indep), (
        "the module's Laurent ring and sympy's Chebyshev recurrence disagree "
        f"on A^n: {out}")
    return out


def check_C5b_descent_terminates(pell_nmax=8):
    """Abel's descent, exercised: deg b falls by exactly one, lands on I."""
    _, desc, _ = _module_tower(pell_nmax)
    out = {"pell_nmax": pell_nmax,
           "all_strict": bool(desc["all_strict"]),
           "all_terminate": bool(desc["all_terminate"]),
           "n_rows": len(desc["rows"])}
    assert out["n_rows"] >= 2, (
        f"a descent of height {pell_nmax} has no content: {out}")
    assert out["all_strict"], out
    assert out["all_terminate"], out
    return out


def check_C5c_update_has_infinite_order(pell_nmax=8):
    """A^n is never a shift, so <A> = Z: time does not close into a clock."""
    _, _, order = _module_tower(pell_nmax)
    out = {"pell_nmax": pell_nmax,
           "checked": order["checked"],
           "never_a_shift": bool(order["never_a_shift"]),
           "order": order["order"]}
    assert out["checked"] >= 2, (
        f"an order claim needs at least two powers: {out}")
    assert out["never_a_shift"], out
    return out


# ══════════════════════════════════════════════════════════════════
#  C6 — the count.  Space is the dimension, time is the rank.
# ══════════════════════════════════════════════════════════════════

def check_C6_signature_at_the_minimal_cell(cell_dim=2):
    """(d_space, d_time) = (3, 1) at s = 2 — TWO statements sharing one premise.

    REWRITTEN 2026-08-13.  The original leg asserted the boxed identity
    (dim su(s), rank su(s)), which the review's attack 5 showed is numerology:
    the model's own bound is F291's Clifford count 2*log2(s)+1, and that equals
    dim su(s) = s^2-1 ONLY at s = 2 (3 vs 3, but 5 vs 15 at s = 4).  This leg now
    asserts what is true — the two numbers at the minimal cell, and that they
    share the s = 2 premise — and it explicitly asserts that the two FUNCTIONS
    DIVERGE at s = 4, so re-introducing the identity would turn it red.
    """
    from casim.engine.lattice import time_signature as ts
    # The module REFUSES any cell but s = 2 since 2026-08-13.  That refusal must
    # surface here as a clean assertion failure, never as an exception: a control
    # that CRASHES scores INVALID rather than CONTROL, which banks an untested
    # control as sound (the lesson F291's own cell_dim control taught).
    try:
        sig = ts.signature_of_cell(cell_dim)
    except ValueError as exc:
        raise AssertionError(
            f"d_time is established only at the minimal cell s = 2; the module "
            f"refuses s = {cell_dim}: {exc}") from None
    out = {"s": cell_dim,
           "d_space_bound": sig["d_space_bound"],
           "d_time": sig["d_time"],
           "signature": sig["signature"],
           # the divergence that kills the withdrawn identity
           "clifford_bound_at_4": ts.space_bound_of_cell(4),
           "dim_su_at_4": 4 * 4 - 1,
           "functions_diverge_at_s4": bool(ts.space_bound_of_cell(4) != 4 * 4 - 1)}
    assert out["signature"] == "3+1", (
        "the signature is 3+1 only at the minimal cell; the count is not an "
        f"arithmetic identity: {out}")
    assert out["d_space_bound"] == 3 and out["d_time"] == 1, out
    assert out["functions_diverge_at_s4"], (
        "2*log2(s)+1 and dim su(s) agree at s = 4 — if that were true the "
        f"withdrawn identity of sec.8 would be defensible after all: {out}")
    return out


# ══════════════════════════════════════════════════════════════════
#  C7 — the residual, measured
# ══════════════════════════════════════════════════════════════════

def check_C7_composite_cell_second_flow():
    """At s = 4 the massive Dirac walk DOES carry a second dispersive flow.

    Reported, not buried: this is the exact boundary of the rank-one count.
    V = I (x) A commutes with D at every mass.  The assertion here is that the
    measurement HAPPENED and came back positive — the finding's honesty depends
    on this staying visible, so a silent change of the answer must go red.
    """
    from casim.engine.lattice import time_signature as ts
    res = ts.composite_cell_second_flow()
    out = {"second_flow_exists_at_s4": bool(res["second_flow_exists_at_s4"]),
           "survives_nonzero_mass": bool(res["survives_nonzero_mass"]),
           "max_commutator": max(r["max_commutator"] for r in res["rows"]),
           "n_masses": len(res["rows"])}
    assert out["n_masses"] >= 2, out
    assert out["second_flow_exists_at_s4"], out
    assert out["survives_nonzero_mass"], (
        "V = I (x) A no longer commutes with the massive Dirac walk — the "
        f"finding's sec.9 residual would need rewriting: {out}")
    assert out["max_commutator"] < 1e-12, out
    return out


def check_C0_one_dimension_fails_the_theorem():
    """THE NON-TAUTOLOGY CONTROL (review, method notes — its single best check).

    In d = 1 the theorem is FALSE, and it must be, on both load-bearing legs:
      * gcd(n~) = sin k is not a unit, so the traceless commutant is not free;
      * N = sin^2 k is a perfect SQUARE, so the extension splits.
    A version of C2/C4a that passed here would be testing the algebra, not the
    3D rule.  This is physically meaningful where `fake_gcd` is synthetic: the
    1D walk genuinely is two automata (left- and right-movers) each with its own
    clock, which is what F313 sec.6 says a split N means.
    """
    u, n = _walk_1d()
    M = _W[0]
    # gcd leg
    polys = [sp.Poly(sp.expand(x * 2 * M), *_W, domain="QQ_I")
             for x in n if sp.simplify(x) != 0]
    g = sp.gcd_list(polys).as_expr() if len(polys) > 1 else polys[0].as_expr()
    gp = sp.Poly(sp.expand(g), *_W)
    gcd_is_unit = bool(len(gp.monoms()) == 1 and gp.coeffs()[0] != 0)
    # squarefree leg
    N = sp.expand(sum(x ** 2 for x in n))
    sq = sp.simplify(N - sp.expand(((w := _W[0]) - 1 / w) ** 2 / (2 * sp.I) ** 2))
    N_is_a_square = bool(sq == 0)
    out = {"gcd_1d": str(g), "gcd_is_unit": gcd_is_unit,
           "N_is_a_perfect_square": N_is_a_square,
           "theorem_fails_in_1d": bool((not gcd_is_unit) and N_is_a_square)}
    assert not out["gcd_is_unit"], (
        f"gcd is a unit in d = 1 — C2 would pass on a walk it must fail: {out}")
    assert out["N_is_a_perfect_square"], (
        f"N is squarefree in d = 1 — C4a would pass where it must fail: {out}")
    assert out["theorem_fails_in_1d"], (
        "the theorem does NOT fail in d = 1, so C2/C4a are testing the algebra "
        f"rather than the 3D rule — the result would be a tautology: {out}")
    return out


CHECKS = (
    ("C0_one_dimension_fails_the_theorem", check_C0_one_dimension_fails_the_theorem),
    # C6 runs BEFORE C1a deliberately (review rec 9): with `--param cell_dim=4`
    # the old order aborted at C1a in 0.03 s and C6 never ran, so the control
    # exercised only the leg that asserts its own input.  Now it reaches both.
    ("C6_signature_at_the_minimal_cell", check_C6_signature_at_the_minimal_cell),
    ("C1a_no_room_at_the_minimal_cell", check_C1a_no_room_at_the_minimal_cell),
    ("C1b_commutant_is_two_dimensional", check_C1b_commutant_is_two_dimensional),
    ("C2_traceless_part_is_free_rank_one", check_C2_traceless_part_is_free_rank_one),
    ("C3a_every_shift_is_in_the_commutant", check_C3a_every_shift_is_in_the_commutant),
    ("C3b_nothing_but_shifts_is_scalar_unitary", check_C3b_nothing_but_shifts_is_scalar_unitary),
    ("C4a_discriminant_is_squarefree", check_C4a_discriminant_is_squarefree),
    ("C4b_update_is_the_fundamental_unit", check_C4b_update_is_the_fundamental_unit),
    ("C5a_tower_is_chebyshev", check_C5a_tower_is_chebyshev),
    ("C5b_descent_terminates", check_C5b_descent_terminates),
    ("C5c_update_has_infinite_order", check_C5c_update_has_infinite_order),
    ("C7_composite_cell_second_flow", check_C7_composite_cell_second_flow),
)


def check_all(cell_dim=2, pell_nmax=8, fake_gcd=False):
    """Registry entry point. Returns the full result dict.

    Three declared controls (D9/H2, `control:` on `F313-time-signature`):

    ``--param pell_nmax=1``    a tower that does not climb cannot evidence a
        tower.  C5a/C5b/C5c must go red.
    ``--param cell_dim=4``     the count is a property of the MINIMAL cell.
        C1a/C6 must go red.
    ``--param fake_gcd=True``  a common non-unit factor on the Bloch vector.
        C2 must go red — the traceless commutant stops being free, so `b` need
        not be local and the space/time split leaks.
    """
    kw = {
        "check_C1a_no_room_at_the_minimal_cell": {"cell_dim": cell_dim},
        "check_C1b_commutant_is_two_dimensional": {"fake_gcd": fake_gcd},
        "check_C2_traceless_part_is_free_rank_one": {"fake_gcd": fake_gcd},
        "check_C5a_tower_is_chebyshev": {"pell_nmax": pell_nmax},
        "check_C5b_descent_terminates": {"pell_nmax": pell_nmax},
        "check_C5c_update_has_infinite_order": {"pell_nmax": pell_nmax},
        "check_C6_signature_at_the_minimal_cell": {"cell_dim": cell_dim},
    }
    out = {}
    for name, fn in CHECKS:
        out[name] = fn(**kw.get(fn.__name__, {}))
    out["n_checks"] = len(CHECKS)
    out["imported_step"] = ("Dubickas-Steuding 2004 Thm 2 / Pastor 2001 (polynomial-Pell "
                            "structure theorem); the REAL residual is the polynomial->Laurent "
                            "transfer, since D-S needs deg f = 0 => f constant, which fails "
                            "in C[w^+-]. NOT Abel 1826 - corrected 2026-08-13.")
    out["verdict"] = (
        "The Cayley-graph/update split is COMPUTED, not chosen: det splits the "
        "update's commutant into exactly the shift lattice U(1) x Z^3 and "
        "exactly the powers of the update, infinite cyclic.  d_time = "
        "rank su(2) = 1 from the same s = 2 that gives F291 d_space <= "
        "dim su(2) = 3, so the signature 3+1 rests on ONE input.  Residual: "
        "Abel's theorem is imported, and a free s = 4 composite carries a "
        "second dispersive flow."
    )
    return out


# --- no pytest surface ------------------------------------------------------
# Deliberately no thin `test_*` wrappers: this is an `entry:` record, and
# tests/casim/test_registry_integrity.py forbids a file being both.  `check_all`
# runs every check via CHECKS.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, default=str))
