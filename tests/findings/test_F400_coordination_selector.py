"""F400 — BCC and diamond-cubic share a generator tetrahedron; only diamond's
missing Bravais property, not the F291/F292 S1/S2/S3 selectors, excludes it.

Attacks `docs/theory/notebook-v2/01-thread-map.md` row T01/T10: whether the
model's dimension-selector machinery (F291/F292/F313/F326/F377), run against
a coordination-4 diamond-cubic generator set instead of BCC's coordination-8,
reproduces or excludes 3+1D matter content.

Five checks. The geometric and lattice-membership legs are re-derived here
INDEPENDENTLY of `casim.engine.lattice.coordination_selector` (re-typed
integer/rational vectors, not imported), per this project's standing
practice (F291/F326's own precedent).

  A1 (exact) BCC's 8-vector coordination shell splits into two regular
      tetrahedra by sign parity; each has Gram matrix 4*delta_jk - 1 (diagonal
      3, off-diagonal -1 -- a regular-simplex shape matching Paper 2 Eq. 20
      exactly, not merely up to a convention).
  A2 (exact) The "positive-parity" tetrahedron is vertex-for-vertex IDENTICAL
      to the standard diamond-cubic nearest-neighbour bond set -- not merely
      isomorphic, the same four integer vectors.
  B1 (exact) The genuine diamond A->B vector (1/4,1/4,1/4) is not expressible
      as an integer combination of the FCC primitive vectors -- diamond's
      two sublattices are not related by any pure lattice translation.
      DECLARED CONTROL (D9/H2): passed a genuine FCC lattice vector
      (1/2,1/2,0) instead, the same assertion (orbit NOT invariant) must go
      RED, since a real lattice vector DOES return the basis to itself --
      proving the test can tell a lattice vector from a non-lattice one,
      not merely report a hard-coded False.
  C1 (exact) `dimensionality`'s S1/S2/S3 entry points take no lattice-type or
      coordination-number argument -- confirmed by signature inspection, not
      asserted.
"""
from __future__ import annotations

from itertools import product

import sympy as sp

from casim.engine.lattice import coordination_selector as cs
from casim.engine.lattice import dimensionality as dim


# ── independently re-typed geometry (NOT imported from the module) ─────────

def _bcc_shell_indep():
    return [v for v in product((1, -1), repeat=3)]


def _gram_indep(vectors):
    n = len(vectors)
    G = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            G[i, j] = sum(a * b for a, b in zip(vectors[i], vectors[j]))
    return G


def _fcc_primitives_indep():
    h = sp.Rational(1, 2)
    return sp.Matrix([0, h, h]), sp.Matrix([h, 0, h]), sp.Matrix([h, h, 0])


def _in_fcc_indep(v: sp.Matrix) -> bool:
    a1, a2, a3 = _fcc_primitives_indep()
    M = sp.Matrix.hstack(a1, a2, a3)
    coeffs = M.solve(sp.Matrix(v))
    return all(sp.nsimplify(c).is_integer for c in coeffs)


# ── checks ────────────────────────────────────────────────────────────────

def check_A1_dual_tetrahedra_are_regular():
    shell = _bcc_shell_indep()
    assert len(shell) == 8
    t_plus = [v for v in shell if v[0] * v[1] * v[2] == 1]
    t_minus = [v for v in shell if v[0] * v[1] * v[2] == -1]
    assert len(t_plus) == 4 and len(t_minus) == 4
    for T in (t_plus, t_minus):
        G = _gram_indep(T)
        diag = {G[i, i] for i in range(4)}
        offdiag = {G[i, j] for i in range(4) for j in range(4) if i != j}
        assert diag == {3}
        assert offdiag == {-1}
    # agrees with the module
    m_plus, m_minus = cs.split_into_dual_tetrahedra(cs.bcc_coordination_shell())
    assert sorted(m_plus) == sorted(t_plus)
    assert sorted(m_minus) == sorted(t_minus)
    return {"t_plus": t_plus, "t_minus": t_minus,
            "gram_diag": 3, "gram_offdiag": -1}


def check_A2_tetrahedron_equals_diamond_bonds():
    shell = _bcc_shell_indep()
    t_plus = [v for v in shell if v[0] * v[1] * v[2] == 1]
    diamond = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    assert sorted(t_plus) == sorted(diamond)
    out = cs.bcc_tetrahedron_equals_diamond_bonds()
    assert out["equal_as_sets"] is True
    assert out["grams_identical"] is True
    return {"equal_as_sets": True, "grams_identical": True}


def check_B1_diamond_shift_not_fcc_vector(shift=None):
    """The claim under test, fixed regardless of input: this shift is NOT a
    lattice symmetry of diamond-cubic (`orbit_invariant is False`).

    ``shift`` is a DECLARED CONTROL (D9/H2). Default (None -> the genuine
    diamond A->B vector, (1/4,1/4,1/4)): the claim holds -- no pure
    translation connects diamond's two sublattices.

    Control value ``shift=[1,2,1,2]`` (encoding the rational (1/2,1/2,0), a
    genuine FCC primitive vector, as [numerator_x, denominator_x,
    numerator_y, denominator_y] with z fixed at 0, so it survives the test
    registry's YAML/JSON params round-trip): the SAME claim ("not a
    symmetry") must go RED, because a real lattice vector DOES return the
    basis to itself. This proves the check is sensitive to its input rather
    than a hard-coded False -- the assertion is NOT re-derived from the
    input, only the input changes.
    """
    if shift is None:
        shift_vec = (sp.Rational(1, 4),) * 3
    else:
        nx, dx, ny, dy = shift[0], shift[1], shift[2], shift[3]
        shift_vec = (sp.Rational(nx, dx), sp.Rational(ny, dy), sp.Integer(0))

    assert _in_fcc_indep(sp.Matrix([sp.Rational(1, 4)] * 3)) is False
    assert _in_fcc_indep(sp.Matrix([sp.Rational(1, 2)] * 3)) is False

    out = cs.diamond_basis_orbit_under_shift(shift_vec)
    assert out["orbit_invariant"] is False, (
        f"shift={shift_vec}: expected this shift NOT to be a lattice "
        f"symmetry (orbit_invariant=False), got "
        f"{out['orbit_invariant']} instead")
    if shift is None:
        assert cs.diamond_is_bravais() is False
    return {"shift": [str(x) for x in shift_vec],
            "orbit_invariant": out["orbit_invariant"]}


def check_C1_selectors_take_no_lattice_argument():
    import inspect
    lattice_like = {"lattice", "coordination", "generator", "bcc", "diamond"}
    targets = ("bloch_vector", "bloch_jacobian", "jacobian_ranks",
               "isotropic_intrabranch_mass_dim", "mass_phase_is_gaugeable",
               "select_dimension")
    sigs = {}
    for name in targets:
        params = list(inspect.signature(getattr(dim, name)).parameters)
        sigs[name] = params
        assert not (set(p.lower() for p in params) & lattice_like)
    out = cs.selector_signature_has_no_lattice_argument()
    assert out["no_lattice_argument_anywhere"] is True
    return {"signatures": sigs}


CHECKS = (
    ("A1_dual_tetrahedra_are_regular", check_A1_dual_tetrahedra_are_regular),
    ("A2_tetrahedron_equals_diamond_bonds",
     check_A2_tetrahedron_equals_diamond_bonds),
    ("B1_diamond_shift_not_fcc_vector", check_B1_diamond_shift_not_fcc_vector),
    ("C1_selectors_take_no_lattice_argument",
     check_C1_selectors_take_no_lattice_argument),
)


def check_all(shift=None):
    """Registry entry point. Returns the full result dict.

    One declared control (D9/H2, `control:` on `F400-coordination-selector`):

    ``--param shift=[1,2,1,2]``  encodes the genuine FCC primitive vector
        (1/2,1/2,0) as [numerator_x, denominator_x, numerator_y,
        denominator_y] (z is fixed at 0). check_B1 must go RED: a real
        lattice vector returns the diamond basis to itself, which is the
        opposite of the finding's own claim about the true diamond shift.
    """
    kw = {"check_B1_diamond_shift_not_fcc_vector": {"shift": shift}}
    out = {}
    for name, fn in CHECKS:
        out[name] = fn(**kw.get(fn.__name__, {}))
    out["n_checks"] = len(CHECKS)
    out["verdict"] = cs.report()["verdict"]
    return out


# --- no pytest surface ------------------------------------------------------
# Deliberately no thin `test_*` wrappers: this record is an `entry:` record.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
