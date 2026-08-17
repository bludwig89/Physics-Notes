#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dimensionality.py — why d = 3, from the model's own adopted structure (F291)
============================================================================

Attacks `docs/status/completeness-2026-08-02.md` rubric row **A1**, the first
entry of the ABSENT table: *"the BDPT uniqueness theorem forces the Weyl walk
**given** 3D; nothing selects 3. Assumed, never examined."*

That statement is correct about BDPT. Bisio–D'Ariano–Perinotti–Tosini derive
the Weyl walk from linearity + unitarity + locality + homogeneity + isotropy at
minimal internal dimension s = 2, and obtain a solution **in each** of d = 1, 2
and 3 (`references/qca-papers-1-4-overview.md` lines 26, 61–66). The theorem is
a uniqueness statement *within* a dimension, not a selection *between*
dimensions.

This module asks the different question the rubric row is really about: given
the structure the model has **already adopted** for other reasons — founding
decisions 1, 2 and 5 in `CLAUDE.md` — is d = 3 still free?

It is not. Three selectors are evaluated here, and they are **not** the same
argument in three costumes; two of them are independent of the cell dimension
s, and the pair (S1, S2) is independent of the photon.

  S1  UPPER BOUND, d <= 3.  The walk's generator is H(k) = sigma . n~(k) with
      n~ valued in R^3 — three components, because the traceless Hermitian part
      of a 2x2 matrix is 3-dimensional and no 2x2 algebra carries a fourth
      mutually anticommuting Hermitian generator. So the Jacobian
      J = d n~ / d k at k = 0 is a 3 x d matrix and rank(J) <= 3. For d >= 4,
      ker(J) is a nonzero subspace of R^d.  Two ways to close it: (a) isotropy
      makes the point group act irreducibly on R^d, so an invariant subspace is
      0 or everything, and ker(J) = R^d is the trivial automaton — this route
      ASSUMES irreducibility and is S1's weakest link; (b) ker(J) != 0 makes the
      leading-order dispersion vanish along a subspace, so the direction-
      independent limit c_lat = dOmega/d|k| that founding decision 2 defines
      does not exist — no representation theory needed. Hence d <= 3.

  S2  LOWER BOUND, d >= 3.  coker(J) = R^3 / im(J) is the set of internal spin
      axes that momentum never reaches. Every m_hat in coker(J) supplies an
      **isotropy-invariant intra-branch mass term** m sigma.m_hat: it commutes
      with the point-group action precisely because no momentum direction
      rotates it. Hermiticity then forces that m to be REAL — a diagonal mass
      block admits no phase. Founding decision 1 gauges the phase beta of the
      **complex** mass step m -> m e^{i beta} to obtain chiral SU(2)_L with no
      Higgs field (F27). That phase exists only when the mass block is
      OFF-diagonal, i.e. only when coker(J) = 0, i.e. only when d >= 3.
      dim coker(J) = 3 - d for d <= 3: two spare axes at d = 1, one at d = 2
      (the familiar parity-odd sigma_z mass of 2+1 dimensions), none at d = 3.

  S3  EXACT, and independent of s.  Founding decision 2 defines c_lat as the
      rotation rate of the real **(E, B) vector pair**, and Paper 1 Eq. 35
      writes the model's Maxwell law with a cross product,
      dE/dt = i 2 n_{k/2} x B. For B to be a vector rather than a bivector we
      need dim Lambda^2 R^d = dim R^d, i.e. d(d-1)/2 = d, whose only solutions
      over the integers are d = 0 and **d = 3**. There is no d = 7 loophole:
      the octonionic cross product is not the Hodge dual of a 2-form, and
      *B is the Hodge dual of a 2-form* is what the model uses. Equivalently
      and more natively: the paired-spinor photon (founding decision 5, F69) is
      a bilinear of two 2-spinors, so its field strength is the sigma-triplet
      of C^2 (x) C^2 = 1 + 3 — a 3-component object in any d — and it can be a
      spatial vector field only at d = 3.

  S1 and S2 together give d = 3 given s = 2. S3 gives d = 3 with no reference
  to s at all. So the result does not rest on BDPT's minimality postulate.

**+1.** Time is one-dimensional by the automaton's construction, not by a
theorem proved here: the update is a single unitary A, so the evolution it
generates is a Z-action. Any second commuting unitary flow would, under
homogeneity, be a further generator of the Cayley graph — that is, another
SPACE direction, which S1 then caps. This module records that as `structural`,
not `exact`, and the finding says so.

What is NOT closed: this derives d from adopted structure, and the adopted
structure is itself motivated (founding decision 6, elegance). What has moved
is that "why 3+1" is no longer a free integer — it is a consequence of the
(E, B) pair and the Higgs-free mass step, either of which alone forces it.

Exactness: S1, S2, S3 are exact over the integers / over Q. Every number this
module returns is an integer or a sympy exact form. No floats are used except
in the reporting cross-check against the registry value of c_lat.

F292 — WHY NOT A HIGHER MULTIPLE OF THREE
-----------------------------------------
The natural follow-up: if 3 is special, is 6 or 9? Neither, and they fail
differently, which is what makes the answer worth recording.

  S3'  BIVECTOR OVERCOUNT.  dim Lambda^2 R^d / d = (d-1)/2, which equals 1
       exactly at d = 3.  At d = 3n the factor is (3n-1)/2: it is 1 only at
       n = 1, so no higher multiple of three can carry a vector B.  Exact over
       the integers, and independent of the cell dimension s.

  S4   CHIRALITY PARITY (new here).  A chirality operator — the product of all
       gammas, traceless and squaring to the identity — exists only in EVEN
       spacetime dimension D = d + 1; in odd D that product is proportional to
       the identity and there is no projector to split the Dirac rep.  So
       founding decision 1, which needs a left/right pair to gauge (F27, and
       F91's right-branch weight identically zero), forces d ODD.  This kills
       d = 6 outright, and independently re-kills d = 2, where S2 had already
       found the parity-odd sigma_z mass — two unrelated routes agreeing at
       d = 2 is a cross-check on the machinery, not a coincidence.  Verified by
       explicit Clifford construction for D = 2..8, not asserted from the
       literature.

  So d = 6 fails twice (even d, and (d-1)/2 = 5/2), and d = 9 — the only
  multiple of three that survives S4, since D = 10 is even — fails S3' with
  (d-1)/2 = 4.

  THE REDUCIBLE CASE, which is the physics.  Reading d = 3n as n COPIES of R^3
  rather than one isotropic R^{3n} makes the point group act block-diagonally,
  so S1's irreducibility premise no longer applies and the question has to be
  asked again.  It has a sharp answer: there is only ONE sigma-triplet in a
  2-dimensional cell (dim su(2) = 3), so all n blocks map into the same
  internal R^3, giving

        rank J = 3,   dim ker J = 3(n-1),   dim coker J = 0.

  The walk sees exactly one R^3; the other 3(n-1) directions are exact zero
  modes at leading order.  This is NOT compactification — there is no radius,
  no tower, nothing to make small — it is degeneracy: the field is constant
  along them.  And should a residual dependence enter at O(k^2) or beyond, it
  is an IRRELEVANT operator by F130's measured Kadanoff spectrum
  (lambda_n = b^{-n}), so coarse-graining removes it.  Note coker J = 0, so S2
  and founding decision 1 are untouched: the reducible case fails on S1 and S3'
  only, which is evidence the selectors are independent rather than redundant.

  Raising the cell does not rescue any of this.  The minimal spinor dimension
  is 2^floor(d/2), so d = 6 needs s = 8 and d = 9 needs s = 16 — but S3' and S4
  never mention s.

Findings: F291, F292.
"""
from __future__ import annotations

from typing import Dict, List

import sympy as sp

from casim.constants import c_lat

__all__ = [
    "bloch_vector",
    "bloch_jacobian",
    "jacobian_ranks",
    "max_anticommuting_traceless_hermitian",
    "isotropic_intrabranch_mass_dim",
    "mass_phase_is_gaugeable",
    "bivector_dim",
    "magnetic_vector_dimensions",
    "hodge_vector_dimensions",
    "c_lat_of_dimension",
    "chirality_orientation",
    "bivector_overcount",
    "multiples_of_three_passing_S3",
    "minimal_spinor_dim",
    "euclidean_gammas",
    "has_chirality",
    "chirality_dimensions",
    "reducible_jacobian",
    "reducible_ranks",
    "higher_multiples_report",
    "select_dimension",
    "report",
]

# The internal (traceless Hermitian) dimension of an s = 2 cell.  Not a
# free parameter: it is dim su(2) = 3, proved by
# max_anticommuting_traceless_hermitian(2).
_INTERNAL_VECTOR_DIM = 3


# ══════════════════════════════════════════════════════════════════
#  The walk's Bloch vector n~(k), exactly, in d = 1, 2, 3
# ══════════════════════════════════════════════════════════════════

def bloch_vector(d: int, sign: str = "+"):
    """The BDPT Bloch vector n~(k) as an exact sympy 3-vector, plus the k symbols.

    d = 3 is the BCC walk of Paper 1 Eq. 15 (the sign-corrected form used by
    `casim.engine.lattice.bcc._bcc_uvec`); d = 2 is the square-lattice walk of
    Eq. 16; d = 1 is the trivial-shift walk.  Returns (n~, [k_1..k_d]).
    """
    if d not in (1, 2, 3):
        raise ValueError(
            f"BDPT gives an s=2 walk only for d in (1,2,3); got d={d}. "
            "For d >= 4 use jacobian_ranks(d), which needs no formula."
        )
    s = 1 if sign == "+" else -1
    ks = sp.symbols(f"k1:{d + 1}", real=True)
    scale = 1 / sp.sqrt(d)            # the lattice light speed, 1/sqrt(d)

    if d == 1:
        (k,) = ks
        n = sp.Matrix([0, 0, sp.sin(k)])
    elif d == 2:
        kx, ky = ks
        cx, cy = sp.cos(kx * scale), sp.cos(ky * scale)
        sx, sy = sp.sin(kx * scale), sp.sin(ky * scale)
        n = sp.Matrix([sx * cy, cx * sy, sx * sy])
    else:
        kx, ky, kz = ks
        cx, cy, cz = (sp.cos(kx * scale), sp.cos(ky * scale), sp.cos(kz * scale))
        sx, sy, sz = (sp.sin(kx * scale), sp.sin(ky * scale), sp.sin(kz * scale))
        n = sp.Matrix([
            sx * cy * cz - s * cx * sy * sz,
            -s * cx * sy * cz + sx * cy * sz,
            cx * cy * sz + s * sx * sy * cz,
        ])
    return n, list(ks)


def bloch_jacobian(d: int, sign: str = "+"):
    """J = d n~ / d k evaluated at k = 0 — an exact 3 x d sympy Matrix."""
    n, ks = bloch_vector(d, sign=sign)
    J = n.jacobian(sp.Matrix(ks))
    return sp.simplify(J.subs({k: 0 for k in ks}))


def jacobian_ranks(d: int, sign: str = "+") -> Dict[str, int]:
    """rank / ker / coker of J at k = 0, for any d >= 1.

    For d <= 3 these come from the explicit walk.  For d >= 4 no s = 2 walk
    exists to differentiate, and none is needed: n~ is valued in R^3 whatever
    the rule, so rank <= 3 and dim ker >= d - 3 > 0 by counting alone.
    """
    if d >= 4:
        return {"d": d, "rank": _INTERNAL_VECTOR_DIM,
                "ker": d - _INTERNAL_VECTOR_DIM, "coker": 0,
                "from_formula": 0}
    J = bloch_jacobian(d, sign=sign)
    r = J.rank()
    return {"d": d, "rank": r, "ker": d - r,
            "coker": _INTERNAL_VECTOR_DIM - r, "from_formula": 1}


# ══════════════════════════════════════════════════════════════════
#  S1 — the upper bound
# ══════════════════════════════════════════════════════════════════

def max_anticommuting_traceless_hermitian(s: int = 2) -> int:
    """Largest set of mutually anticommuting traceless Hermitian s x s matrices.

    For s = 2 this is 3, and the proof is two lines rather than a search: every
    traceless Hermitian 2x2 matrix is a . sigma for a unique real 3-vector a,
    and {a.sigma, b.sigma} = 2 (a . b) I, so anticommuting is exactly Euclidean
    orthogonality in R^3.  The maximum size of a pairwise-orthogonal set of
    nonzero vectors in R^3 is 3.  A fourth would have to be orthogonal to a
    basis, hence zero, hence not a generator.

    Only s = 2 is answered here; the general Clifford answer is 2*log2(s) + 1
    for s a power of two, and the model's cell is s = 2 (BDPT minimality,
    founding decision 6).
    """
    if s != 2:
        raise ValueError("only the model's s = 2 cell is answered here")
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])
    basis = [sx, sy, sz]
    # constructive: the three Pauli matrices are mutually anticommuting
    for i in range(3):
        for j in range(i + 1, 3):
            assert sp.simplify(basis[i] * basis[j] + basis[j] * basis[i]) == sp.zeros(2)
    # maximality: any traceless Hermitian X = a.sigma anticommuting with all
    # three forces a . e_i = 0 for every i, hence a = 0.
    a1, a2, a3 = sp.symbols("a1 a2 a3", real=True)
    X = a1 * sx + a2 * sy + a3 * sz
    sols = sp.solve([sp.simplify(X * B + B * X)[i, j]
                     for B in basis for i in range(2) for j in range(2)],
                    [a1, a2, a3], dict=True)
    assert sols in ([{a1: 0, a2: 0, a3: 0}], [], [{}]) or all(
        all(v == 0 for v in sol.values()) for sol in sols)
    return 3


def upper_bound_dimensions(d_max: int = 8) -> List[int]:
    """The d for which ker(J) = 0, i.e. no zero-energy propagating direction."""
    return [d for d in range(1, d_max + 1) if jacobian_ranks(d)["ker"] == 0]


# ══════════════════════════════════════════════════════════════════
#  S2 — the lower bound, via founding decision 1
# ══════════════════════════════════════════════════════════════════

def isotropic_intrabranch_mass_dim(d: int) -> int:
    """dim coker(J): the number of isotropy-invariant single-walk mass terms.

    An internal axis m_hat that no momentum direction reaches is fixed by the
    whole point-group action, so m sigma.m_hat is an admissible isotropic mass
    for a SINGLE Weyl walk.  Hermiticity forces m real, so such a mass carries
    no phase to gauge.
    """
    return jacobian_ranks(d)["coker"]


def mass_phase_is_gaugeable(d: int) -> bool:
    """True iff mass must be OFF-diagonal, so m -> m e^{i beta} exists (F27).

    Founding decision 1 derives chiral SU(2)_L by gauging exactly that beta.
    It is available only when no intra-branch isotropic mass exists.
    """
    return isotropic_intrabranch_mass_dim(d) == 0


def lower_bound_dimensions(d_max: int = 8) -> List[int]:
    return [d for d in range(1, d_max + 1) if mass_phase_is_gaugeable(d)]


# ══════════════════════════════════════════════════════════════════
#  S3 — the (E, B) vector pair.  Exact, and s-independent.
# ══════════════════════════════════════════════════════════════════

def bivector_dim(d: int) -> int:
    """dim Lambda^2 R^d = d(d-1)/2 — the component count of a magnetic field."""
    return d * (d - 1) // 2


def magnetic_vector_dimensions() -> List[int]:
    """Solve d(d-1)/2 = d over the integers.  Exact: {0, 3}."""
    d = sp.Symbol("d", integer=True)
    roots = sorted(int(r) for r in sp.solve(sp.Eq(d * (d - 1) / 2, d), d))
    return roots


def hodge_vector_dimensions() -> List[int]:
    """Where the Hodge dual of a 2-form is a 1-form: d - 2 = 1, so d = 3 only.

    This is the leg that closes the d = 7 cross-product loophole.  A cross
    product exists in d = 3 and d = 7, but in d = 7 it is not * of a 2-form,
    and the model's B is defined as the dual object in Paper 1 Eq. 35.
    """
    d = sp.Symbol("d", integer=True)
    return sorted(int(r) for r in sp.solve(sp.Eq(d - 2, 1), d))


# ══════════════════════════════════════════════════════════════════
#  Consequences — how d is measured once it is fixed
# ══════════════════════════════════════════════════════════════════

def c_lat_of_dimension(d: int):
    """c_lat = 1/sqrt(d) (Paper 1 Eq. 21).  Exact sympy."""
    return 1 / sp.sqrt(d)


def chirality_orientation(d: int, sign: str = "+"):
    """det J, when J is square — the walk's handedness as an orientation.

    A COROLLARY of S1 and S2, and the sharpest form of both.  J is 3 x d, so a
    determinant exists only at d = 3; there it is

        det J = -/+ 3^{-3/2} = -/+ c_lat^3,

    negative on the '+' branch and positive on the '-' branch.  So the helicity
    label that F91 treats as forced is literally an ORIENTATION of the map from
    momentum space to spin space — and an orientation exists only when that map
    is square.  At d != 3 there is no det, hence no two-valued handedness
    invariant, hence nothing for founding decision 1 to gauge.

    Returns None when d != 3.
    """
    if d != 3:
        return None
    return sp.simplify(bloch_jacobian(d, sign=sign).det())


# ══════════════════════════════════════════════════════════════════
#  The verdict
# ══════════════════════════════════════════════════════════════════

def select_dimension(d_max: int = 8) -> Dict[str, object]:
    """Intersect the three selectors.  Returns the surviving dimension(s)."""
    s1 = set(upper_bound_dimensions(d_max))
    s2 = set(lower_bound_dimensions(d_max))
    s3 = set(x for x in magnetic_vector_dimensions() if x >= 1)
    s3h = set(hodge_vector_dimensions())
    return {
        "S1_upper_bound_ker_zero": sorted(s1),
        "S2_lower_bound_phase_gaugeable": sorted(s2),
        "S3_magnetic_field_is_a_vector": sorted(s3),
        "S3_hodge_dual_is_a_vector": sorted(s3h),
        "S1_and_S2": sorted(s1 & s2),
        "S3_alone": sorted(s3 & s3h),
        "all_three": sorted(s1 & s2 & s3 & s3h),
    }


# ══════════════════════════════════════════════════════════════════
#  F292 — why not a higher multiple of three
# ══════════════════════════════════════════════════════════════════

def bivector_overcount(d: int):
    """dim Lambda^2 R^d / d = (d-1)/2.  Equals 1 exactly at d = 3."""
    return sp.Rational(d - 1, 2)


def multiples_of_three_passing_S3(n_max: int = 8) -> List[int]:
    """The d = 3n with dim Lambda^2 R^d = d.  Exactly [3]."""
    return [3 * n for n in range(1, n_max + 1) if bivector_overcount(3 * n) == 1]


def minimal_spinor_dim(d: int) -> int:
    """2^floor(d/2) — the smallest cell that can host a Weyl walk in d dims."""
    return 2 ** (d // 2)


# ── S4, chirality parity, by explicit Clifford construction ───────────────

def _kron(a, b):
    return sp.Matrix(sp.kronecker_product(a, b))


def euclidean_gammas(D: int) -> List[sp.Matrix]:
    """Gammas with {g_a, g_b} = 2 delta_ab, in dimension 2^floor(D/2).

    Built recursively rather than tabulated, so the chirality verdict below is
    a computation and not a quotation.
    """
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])
    if D <= 1:
        return [sp.Matrix([[1]])]
    if D == 2:
        return [sx, sy]
    if D % 2 == 0:
        g = euclidean_gammas(D - 2)
        n = g[0].shape[0]
        out = [_kron(x, sz) for x in g]
        out.append(_kron(sp.eye(n), sx))
        out.append(_kron(sp.eye(n), sy))
        return out
    g = euclidean_gammas(D - 1)
    P = g[0]
    for x in g[1:]:
        P = P * x
    c = sp.sqrt(sp.simplify(P * P)[0, 0])
    return g + [sp.simplify(P / c)]


def has_chirality(D: int) -> bool:
    """True iff a chirality projector exists in spacetime dimension D.

    The product of all gammas is proportional to the identity in ODD D (no
    projector, hence no Weyl splitting) and traceless in EVEN D.  Computed, not
    asserted.
    """
    g = euclidean_gammas(D)
    n = g[0].shape[0]
    P = g[0]
    for x in g[1:]:
        P = P * x
    P = sp.simplify(P)
    proportional_to_identity = sp.simplify(P - P[0, 0] * sp.eye(n)) == sp.zeros(n)
    return not proportional_to_identity


def chirality_dimensions(d_max: int = 12) -> List[int]:
    """Spatial d admitting chirality, i.e. those with D = d + 1 even."""
    return [d for d in range(1, d_max + 1) if has_chirality(d + 1)]


# ── the reducible d = 3n case ─────────────────────────────────────────────

def reducible_jacobian(n_blocks: int):
    """J for R^{3n} read as n copies of R^3, each mapping isomorphically.

    All n blocks land on the SAME internal sigma-triplet, because a 2-dim cell
    has only one.  Returns the exact 3 x 3n sympy matrix.
    """
    d = 3 * n_blocks
    J = sp.zeros(3, d)
    scale = 1 / sp.sqrt(3)
    for b in range(n_blocks):
        for i in range(3):
            J[i, 3 * b + i] = scale
    return J


def reducible_ranks(n_blocks: int) -> Dict[str, int]:
    """rank / ker / coker for the n-copies-of-R^3 reading of d = 3n."""
    J = reducible_jacobian(n_blocks)
    r = J.rank()
    return {"n_blocks": n_blocks, "d": 3 * n_blocks, "rank": r,
            "ker": 3 * n_blocks - r, "coker": _INTERNAL_VECTOR_DIM - r,
            "frozen_directions": 3 * (n_blocks - 1)}


def higher_multiples_report(n_max: int = 4) -> Dict[str, object]:
    """The full F292 verdict on d = 3n."""
    rows = {}
    for n in range(1, n_max + 1):
        d = 3 * n
        rows[d] = {
            "n": n,
            "bivector_dim": bivector_dim(d),
            "bivector_overcount": str(bivector_overcount(d)),
            "passes_S3": bivector_overcount(d) == 1,
            "spacetime_D": d + 1,
            "has_chirality": has_chirality(d + 1),
            "minimal_spinor_dim": minimal_spinor_dim(d),
            "reducible": reducible_ranks(n),
        }
    return {
        "rows": rows,
        "multiples_passing_S3": multiples_of_three_passing_S3(n_max),
        "chirality_dimensions": chirality_dimensions(3 * n_max),
        "verdict": "d = 3 is the only multiple of three; d = 3n reducible "
                   "freezes 3(n-1) directions and collapses to d = 3",
    }


def report() -> Dict[str, object]:
    """Everything F291 asserts, as a JSON-ready dict."""
    ranks = {d: jacobian_ranks(d) for d in (1, 2, 3, 4, 5)}
    sel = select_dimension()
    d_star = sel["all_three"][0]
    return {
        "finding": "F291",
        "question": "completeness-2026-08-02 rubric row A1 — why 3+1 dimensions",
        "internal_vector_dim": max_anticommuting_traceless_hermitian(2),
        "jacobian_ranks": ranks,
        "intrabranch_mass_dim": {d: isotropic_intrabranch_mass_dim(d)
                                 for d in (1, 2, 3)},
        "phase_gaugeable": {d: mass_phase_is_gaugeable(d) for d in (1, 2, 3)},
        "bivector_dim": {d: bivector_dim(d) for d in range(1, 8)},
        "selectors": sel,
        "d_selected": d_star,
        "time_dim": 1,
        "time_dim_status": "structural (single update unitary), not proved here",
        "signature": f"{1}+{d_star}",
        "det_J_plus_branch": str(chirality_orientation(3, "+")),
        "det_J_minus_branch": str(chirality_orientation(3, "-")),
        "det_J_equals_c_lat_cubed": bool(
            sp.simplify(abs(chirality_orientation(3, "+"))
                        - c_lat_of_dimension(3) ** 3) == 0),
        "c_lat_closed_form": str(c_lat_of_dimension(d_star)),
        "c_lat_registry": float(c_lat),
        "c_lat_agrees": bool(
            abs(float(c_lat_of_dimension(d_star)) - float(c_lat)) < 1e-15),
        "higher_multiples": higher_multiples_report(),
    }


if __name__ == "__main__":       # pragma: no cover — artifact write is guarded
    import json
    print(json.dumps(report(), indent=2, default=str))
