#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coordination_selector.py — why BCC and not diamond-cubic (F400)
=================================================================

Attacks `docs/theory/notebook-v2/01-thread-map.md` row **T01** (and its T10
companion): the notebook's earliest reasoning (pp.3, 36 — NB-005/006/044,
"connection number sets dimension") asks whether a lower-coordination lattice
was ever a live alternative to BCC's coordination-8 shell, and whether the
F291/F292 dimension-selector machinery, run against a coordination-4
diamond-cubic generator set, would exclude it or not.

**The short answer, checked below rather than assumed.** `dimensionality.py`'s
S1/S2/S3 selectors are pure functions of `(s, d)` — inspect their signatures:
`bloch_vector(d, sign)`, `jacobian_ranks(d, sign)`, `select_dimension(d_max)`.
None takes a lattice type or a coordination number. So they cannot be "run
against diamond-cubic instead of BCC" in the sense of producing a different
verdict, because they have no input slot for which lattice realizes d = 3 —
they only ever see d = 3 and s = 2, from BDPT's own d = 3 walk (Paper 1
Eq. 15), which the model uses because it is the model's own founding decision
6 lattice. This is not an oversight to patch; it is what §1 below explains.

**What this module actually does instead: it locates diamond-cubic in the
axiom tree BDPT/F291 already stand on, before dimension-counting is reached.**

1. **The geometric coincidence.** BDPT's own d = 3 walk (Paper 2's
   Gram-matrix re-derivation, `references/qca-papers-1-4-overview.md`,
   "four ... BCC tetrahedron vectors", Eq. 20) is built from exactly ONE
   regular tetrahedron of BCC's 8-vector coordination shell — the other four
   are the point-reflected dual tetrahedron, not an independent choice.
   Checked exactly (integer vectors, exact Gram matrices): that tetrahedron
   is vertex-for-vertex identical to the standard diamond-cubic
   nearest-neighbor bond set (the tetrahedral bonds of silicon/germanium/
   carbon-diamond, already measured as coordination 4 in NB-044). So the
   model's own d = 3 walk is not "coordination-8, as opposed to a leaner
   coordination-4 alternative that was never tried" — its own directional
   content is the *same* tetrahedron diamond uses. What differs is not the
   generator geometry; it is the GROUP the generator set is asked to tile.

2. **Diamond-cubic is not a Bravais lattice.** BDPT's theorem (Paper 1,
   `references/qca-papers-1-4-overview.md`: "For G = Z^3 ... only BCC lattice
   admits a nontrivial s = 2 automaton") is stated for a SINGLE abelian
   group G acting on a single orbit of sites — a Bravais lattice. Diamond
   structure has a genuine 2-point basis (two inequivalent sublattices, each
   individually FCC), and the vector connecting them, (1/4,1/4,1/4) in the
   conventional cubic cell, is not an FCC lattice vector: shifting the
   2-point basis {(0,0,0), (1/4,1/4,1/4)} by itself lands on
   {(1/4,1/4,1/4), (1/2,1/2,1/2)} mod the FCC lattice, not back on the
   original set (checked exactly in rational arithmetic below). Pure
   translations connect each sublattice only to itself; reaching the other
   sublattice needs a point-group operation (an inversion centred on a bond
   midpoint), not a translation. So diamond-cubic is outside BDPT's own
   single-orbit-under-G premise before "which d does the walk select" is
   even asked.

3. **The two ways around that, and why neither is in this project's tree.**
   A genuine coordination-4 QCA would need either (a) doubling the internal
   cell to s = 4 — one qubit per sublattice, exactly the shape of the
   model's own Dirac construction (Paper 1 Eq. 23, two coupled s = 2
   branches) — which BDPT's own minimality axiom (smallest s admitting
   nontrivial dynamics) disfavours unless s = 2 fails, and s = 2 already
   works for BCC; or (b) a non-abelian generator group extending Z^3 by the
   point-group element that connects the sublattices, which Paper 1 only
   sketches ("Non-Abelian extension") and never solves for d = 3, here or
   in the cited literature.

**Consequence for T01.** "Why BCC not diamond" is not a question S1/S2/S3
answer (they are blind to coordination number by construction, not by
oversight — see (1)). It is answered one level down: diamond-cubic was never
a competing (s = 2, G = Z^3) candidate for F291's selectors to choose between
in the first place. The notebook's own isomer-counting intuition (NB-005,
"only 2" colourings of K_4) and its coordination-number claim (NB-044,
diamond measured at exactly 4) are both independently confirmed elsewhere in
this tree; what was missing, and what this module supplies, is the link
between "diamond has coordination 4" and "the model's own BCC walk already
contains that same tetrahedron, one level below the Bravais-lattice premise
that the F291 selectors take for granted."

Exactness: every claim here is exact integer/rational arithmetic (Gram
matrices, the FCC-lattice-membership test, the basis-orbit computation). No
floats.

Findings: F400.
"""
from __future__ import annotations

from itertools import product
from typing import Dict, List, Tuple

import sympy as sp

__all__ = [
    "bcc_coordination_shell",
    "split_into_dual_tetrahedra",
    "gram_matrix",
    "is_regular_simplex_gram",
    "diamond_bond_vectors",
    "bcc_tetrahedron_equals_diamond_bonds",
    "fcc_primitive_vectors",
    "vector_in_fcc_lattice",
    "diamond_basis_orbit_under_shift",
    "diamond_is_bravais",
    "selector_signature_has_no_lattice_argument",
    "report",
]

Vec = Tuple[int, int, int]


# ══════════════════════════════════════════════════════════════════
#  The BCC coordination shell and its dual-tetrahedron split
# ══════════════════════════════════════════════════════════════════

def bcc_coordination_shell() -> List[Vec]:
    """The 8 nearest neighbours of a BCC site, (+-1,+-1,+-1) — coordination 8."""
    return [v for v in product((1, -1), repeat=3)]


def split_into_dual_tetrahedra(shell: List[Vec]) -> Tuple[List[Vec], List[Vec]]:
    """Split the 8-shell by sign parity into two regular tetrahedra.

    T_plus (product of signs = +1) is exactly the tetrahedron the walk's own
    Gram-matrix derivation (Paper 2 Eq. 20) is built from; T_minus is its
    point-reflected dual, reached as the OTHER four BCC neighbours.
    """
    t_plus = [v for v in shell if v[0] * v[1] * v[2] == 1]
    t_minus = [v for v in shell if v[0] * v[1] * v[2] == -1]
    return t_plus, t_minus


def gram_matrix(vectors: List[Vec]) -> sp.Matrix:
    """Exact integer Gram matrix G_jk = v_j . v_k."""
    n = len(vectors)
    G = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            G[i, j] = sum(a * b for a, b in zip(vectors[i], vectors[j]))
    return G


def is_regular_simplex_gram(G: sp.Matrix) -> bool:
    """True iff G has one diagonal value and one (equal) off-diagonal value.

    That constant-diagonal / constant-off-diagonal shape is exactly what a
    regular tetrahedron's vertex-vector Gram matrix has, and is what Paper 2
    Eq. 20 asserts (h_j . h_k = 4 delta_jk - 1) for the BCC walk's own
    generator tetrahedron.
    """
    n = G.shape[0]
    diag = {G[i, i] for i in range(n)}
    offdiag = {G[i, j] for i in range(n) for j in range(n) if i != j}
    return len(diag) == 1 and len(offdiag) == 1


# ══════════════════════════════════════════════════════════════════
#  Diamond-cubic's own coordination-4 bonds
# ══════════════════════════════════════════════════════════════════

def diamond_bond_vectors() -> List[Vec]:
    """The standard tetrahedral nearest-neighbour bonds of diamond-cubic.

    In units of a/4 (a = the conventional cubic cell edge): the four vectors
    from a type-A site to its four type-B neighbours. This is the textbook
    silicon/germanium/carbon-diamond bond set, independently measured at
    coordination 4 by direct lattice-geometry construction in NB-044.
    """
    return [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def bcc_tetrahedron_equals_diamond_bonds() -> Dict[str, object]:
    """Checks the geometric coincidence: BCC's T_plus IS diamond's bond set.

    Not "isomorphic up to relabelling" — literally the same four integer
    vectors, and hence the same exact Gram matrix.
    """
    shell = bcc_coordination_shell()
    t_plus, t_minus = split_into_dual_tetrahedra(shell)
    diamond = diamond_bond_vectors()
    equal_as_sets = sorted(t_plus) == sorted(diamond)
    g_bcc = gram_matrix(t_plus)
    g_dia = gram_matrix(diamond)
    return {
        "t_plus": t_plus,
        "t_minus": t_minus,
        "diamond_bonds": diamond,
        "equal_as_sets": equal_as_sets,
        "gram_bcc_tplus": g_bcc.tolist(),
        "gram_diamond": g_dia.tolist(),
        "grams_identical": g_bcc == g_dia,
        "is_regular_tetrahedron_bcc": is_regular_simplex_gram(g_bcc),
        "is_regular_tetrahedron_diamond": is_regular_simplex_gram(g_dia),
    }


# ══════════════════════════════════════════════════════════════════
#  Diamond-cubic is not a Bravais lattice
# ══════════════════════════════════════════════════════════════════

def fcc_primitive_vectors() -> Tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """FCC primitive translation vectors, in units of the conventional cell edge."""
    half = sp.Rational(1, 2)
    a1 = sp.Matrix([0, half, half])
    a2 = sp.Matrix([half, 0, half])
    a3 = sp.Matrix([half, half, 0])
    return a1, a2, a3


def vector_in_fcc_lattice(v: sp.Matrix) -> bool:
    """Exact rational test: is v an INTEGER combination of the FCC primitives?"""
    a1, a2, a3 = fcc_primitive_vectors()
    M = sp.Matrix.hstack(a1, a2, a3)
    coeffs = M.solve(sp.Matrix(v))
    return all(sp.nsimplify(c).is_integer for c in coeffs)


def diamond_basis_orbit_under_shift(
    shift: Tuple[sp.Rational, sp.Rational, sp.Rational] = (
        sp.Rational(1, 4), sp.Rational(1, 4), sp.Rational(1, 4)),
) -> Dict[str, object]:
    """Shift the diamond 2-point basis by `shift`, test equivalence mod FCC.

    Two points represent the same crystallographic site iff their difference
    is an FCC lattice vector (`vector_in_fcc_lattice`) -- NOT "each Cartesian
    coordinate reduced mod 1", which is only the right equivalence for an
    axis-aligned (simple-cubic-type) lattice. FCC's primitive vectors are not
    axis-aligned, so the coordinate-wise reduction is the wrong test here and
    is not used.

    The genuine diamond A->B vector, (1/4,1/4,1/4), does NOT return the basis
    to itself: neither shifted point is FCC-equivalent to both original
    points (checked below is that (1/2,1/2,1/2), the second shifted point's
    would-be match, is not an FCC lattice vector). This is the exact
    statement that no pure translation connects the two diamond sublattices
    -- diamond-cubic is not a single-orbit (Bravais) lattice under
    translations alone.

    `shift` is a DECLARED CONTROL (D9/H2): passed a genuine FCC lattice
    vector instead (e.g. (1/2,1/2,0) = a1), the basis orbit MUST come back to
    itself -- translating by a lattice vector cannot move the lattice.
    """
    basis = [sp.Matrix([0, 0, 0]),
             sp.Matrix([sp.Rational(1, 4)] * 3)]
    s = sp.Matrix(shift)
    shifted = [b + s for b in basis]
    matched_to = []
    for sp_pt in shifted:
        match = next((i for i, b in enumerate(basis)
                      if vector_in_fcc_lattice(sp_pt - b)), None)
        matched_to.append(match)
    orbit_invariant = (None not in matched_to
                       and len(set(matched_to)) == len(basis))
    return {
        "shift": [str(x) for x in shift],
        "original_basis": [tuple(b) for b in basis],
        "shifted_basis": [tuple(b) for b in shifted],
        "matched_to_original_index": matched_to,
        "orbit_invariant": orbit_invariant,
    }


def diamond_is_bravais() -> bool:
    """False: no pure translation connects diamond's two sublattices."""
    return diamond_basis_orbit_under_shift()["orbit_invariant"]


# ══════════════════════════════════════════════════════════════════
#  The selector machinery is blind to coordination number BY CONSTRUCTION
# ══════════════════════════════════════════════════════════════════

def selector_signature_has_no_lattice_argument() -> Dict[str, object]:
    """Introspects `dimensionality`'s public selector functions.

    Confirms, by inspection rather than assertion, that S1/S2/S3 take only
    `d` (and, for the walk itself, a chirality `sign`) -- no lattice type, no
    coordination number, no generator-set argument anywhere. This is why
    "rerun F291 on a diamond-cubic generator set" cannot change S1/S2/S3's
    verdict: there is no slot in their signature for which real-space lattice
    realizes d = 3.
    """
    import inspect

    from casim.engine.lattice import dimensionality as dim

    targets = ("bloch_vector", "bloch_jacobian", "jacobian_ranks",
               "isotropic_intrabranch_mass_dim", "mass_phase_is_gaugeable",
               "select_dimension")
    sigs = {}
    lattice_like = {"lattice", "coordination", "generator", "bcc", "diamond"}
    for name in targets:
        params = list(inspect.signature(getattr(dim, name)).parameters)
        sigs[name] = params
        assert not (set(p.lower() for p in params) & lattice_like), (
            f"{name} has a lattice-like parameter {params}; the 'selector "
            f"blind to coordination number' claim would be false")
    return {"signatures": sigs, "no_lattice_argument_anywhere": True}


# ══════════════════════════════════════════════════════════════════
#  The verdict
# ══════════════════════════════════════════════════════════════════

def report() -> Dict[str, object]:
    """Everything F400 asserts, as a JSON-ready dict."""
    coincidence = bcc_tetrahedron_equals_diamond_bonds()
    orbit = diamond_basis_orbit_under_shift()
    sig = selector_signature_has_no_lattice_argument()
    return {
        "finding": "F400",
        "question": (
            "notebook-v2 T01/T10 -- run F291/F292's dimension selector on a "
            "coordination-4 diamond-cubic generator set instead of BCC's"
        ),
        "geometric_coincidence": coincidence,
        "diamond_bravais_orbit_check": orbit,
        "diamond_is_bravais": orbit["orbit_invariant"],
        "selector_signatures": sig["signatures"],
        "selector_has_no_coordination_number_input": sig[
            "no_lattice_argument_anywhere"],
        "verdict": (
            "S1/S2/S3 cannot distinguish BCC from diamond-cubic because they "
            "take only (s, d) -- diamond-cubic fails BDPT's own single-orbit "
            "(Bravais, G = Z^3) premise before dimension-counting is reached, "
            "so it was never a competing (s=2, G=Z^3) candidate. The model's "
            "own BCC walk generator tetrahedron IS diamond's bond tetrahedron "
            "-- what differs is the group being tiled, not the local bond "
            "geometry."
        ),
    }


if __name__ == "__main__":       # pragma: no cover — artifact write is guarded
    import json
    print(json.dumps(report(), indent=2, default=str))
