"""F291 — three independent selectors fix d = 3; the model does not choose it.

Attacks completeness-2026-08-02 rubric row **A1** ("why 3+1 spacetime
dimensions", the first entry of the ABSENT table).

Eight checks. The load-bearing ones (S1, S2, S3, and the orientation corollary)
are re-derived here with sympy INDEPENDENTLY of
`casim.engine.lattice.dimensionality`, so this is a genuine cross-check rather
than a restatement of the implementation. In particular:

  * the Bloch vectors are re-typed from `references/qca-papers-1-4-overview.md`
    Eqs. 15/16 rather than imported from the module;
  * the d = 3 Jacobian is additionally cross-checked against the *engine*
    (`casim.engine.lattice.bcc._bcc_uvec`) by finite differences, so the walk
    being differentiated is the one the simulator actually runs.

  A1 (exact)   dim su(2) = 3: the Pauli triple is mutually anticommuting and
      maximal, so the walk's Bloch vector lives in R^3 for any d.
  A2 (exact)   J = dn~/dk at k=0 is 3 x d with rank min(d,3): rank 1, 2, 3 at
      d = 1, 2, 3, and rank <= 3 < d by counting for d >= 4.
  B1 (exact)   S1, the upper bound: ker(J) = 0 only for d <= 3.
  B2 (exact)   S2, the lower bound: coker(J) = 3 - d, so an isotropy-invariant
      intra-branch mass sigma.m_hat exists at d = 1 (2 of them) and d = 2 (the
      parity-odd sigma_z mass), and NOT at d = 3.  Checked by exhibiting the
      d=2 mass explicitly, verifying it commutes with the internal rotation
      that implements a spatial rotation, and verifying no such matrix exists
      at d = 3.
  B3 (exact)   S1 and S2 intersect in exactly {3}.
  C1 (exact)   S3, s-independently: d(d-1)/2 = d over the integers has roots
      {0, 3}, and the Hodge condition d - 2 = 1 gives {3}, closing the d = 7
      cross-product loophole.
  D1 (exact)   corollary: det J exists only at d = 3 and equals -/+ c_lat^3,
      so the two BDPT branches are the two ORIENTATIONS of a square map.
  D2 (machine) engine cross-check: finite differences of `bcc._bcc_uvec`
      reproduce the symbolic J to <= 1e-9, and |det J| = c_lat^3 against the
      constants registry.

Real arithmetic only (CLAUDE.md); the one machine-precision leg is the finite
difference in D2 and is labelled as such.
"""
from __future__ import annotations

import functools

import sympy as sp

from casim.constants import c_lat
from casim.engine.lattice import dimensionality as dim
from casim.engine.lattice import bcc as _bcc

FD_TOL = 1e-9


# ── independently re-typed walks (NOT imported from the module) ────────────

def _n_indep(d, sign=1):
    """BDPT Bloch vector, re-typed from the paper overview Eqs. 15/16."""
    ks = sp.symbols(f"q1:{d + 1}", real=True)
    r = 1 / sp.sqrt(d)
    if d == 1:
        return sp.Matrix([0, 0, sp.sin(ks[0])]), list(ks)
    if d == 2:
        cx, cy = sp.cos(ks[0] * r), sp.cos(ks[1] * r)
        sx, sy = sp.sin(ks[0] * r), sp.sin(ks[1] * r)
        return sp.Matrix([sx * cy, cx * sy, sx * sy]), list(ks)
    cx, cy, cz = (sp.cos(k * r) for k in ks)
    sx, sy, sz = (sp.sin(k * r) for k in ks)
    return sp.Matrix([
        sx * cy * cz - sign * cx * sy * sz,
        -sign * cx * sy * cz + sx * cy * sz,
        cx * cy * sz + sign * sx * sy * cz,
    ]), list(ks)


def _J_indep(d, sign=1):
    n, ks = _n_indep(d, sign)
    J = n.jacobian(sp.Matrix(ks))
    return sp.simplify(J.subs({k: 0 for k in ks}))


@functools.lru_cache(maxsize=None)
def _pauli():
    """Built on call, not at import. sympy work at module scope runs on
    `pytest --collect-only`, which is what the `import_time_work` ratchet in
    tools/audit_tests.py counts; the values are unchanged."""
    return (sp.Matrix([[0, 1], [1, 0]]),
            sp.Matrix([[0, -sp.I], [sp.I, 0]]),
            sp.Matrix([[1, 0], [0, -1]]))


# ── checks ────────────────────────────────────────────────────────────────

def check_A1_internal_vector_dim_is_three(cell_dim=2):
    """The traceless Hermitian part of a 2x2 matrix is exactly 3-dimensional."""
    _PAULI = _pauli()
    for i in range(3):
        for j in range(i + 1, 3):
            assert sp.simplify(_PAULI[i] * _PAULI[j]
                               + _PAULI[j] * _PAULI[i]) == sp.zeros(2)
    # maximality: X = a.sigma anticommuting with all three forces a = 0
    a = sp.symbols("a1 a2 a3", real=True)
    X = sum((a[i] * _PAULI[i] for i in range(3)), sp.zeros(2))
    eqs = []
    for B in _PAULI:
        eqs += list(sp.simplify(X * B + B * X))
    sol = sp.solve(eqs, list(a), dict=True)
    assert sol == [{a[0]: 0, a[1]: 0, a[2]: 0}] or all(
        all(v == 0 for v in s.values()) for s in sol)
    # `cell_dim` is a DECLARED CONTROL (D9/H2): the internal 3 is a statement
    # about the s = 2 cell, not an arithmetic identity. At s = 4 the maximal
    # anticommuting traceless-Hermitian set has 5 members, so this leg must go
    # red -- otherwise A1 would be claiming something it never tested.
    # The module REFUSES any cell but s = 2 (ValueError), which is itself the
    # content: 3 is not an arithmetic fact, it is what s = 2 supplies. Caught
    # and turned into an assertion failure on purpose -- an exception would be
    # scored INVALID by `casim test --control` ("the driver crashed rather than
    # failed"), which is the right verdict for a crash and the wrong one here.
    try:
        n_anti = dim.max_anticommuting_traceless_hermitian(cell_dim)
    except ValueError:
        n_anti = None
    assert n_anti == 3, (
        f"cell_dim={cell_dim} gives {n_anti}, not 3: the internal vector space "
        f"is 3-dimensional BECAUSE the cell is s = 2")
    return {"dim_su2": 3, "maximal": True, "cell_dim": cell_dim}


def check_A2_jacobian_shape_and_rank():
    out = {}
    for d in (1, 2, 3):
        J = _J_indep(d)
        assert J.shape == (3, d)
        assert J.rank() == min(d, 3)
        # agrees with the module
        assert sp.simplify(J - dim.bloch_jacobian(d)) == sp.zeros(3, d)
        out[d] = {"shape": list(J.shape), "rank": int(J.rank())}
    for d in (4, 5, 6):
        r = dim.jacobian_ranks(d)
        assert r["rank"] == 3 and r["ker"] == d - 3 > 0
        out[d] = {"shape": [3, d], "rank": 3, "ker": d - 3}
    return out


def check_B1_upper_bound(d_scan_max=8):
    """S1: ker(J) = 0 exactly for d <= 3."""
    # `d_scan_max` is a DECLARED CONTROL (D9/H2), the F298 pattern: a scan that
    # cannot see d >= 4 cannot claim an UPPER bound at 3. Truncating it to 3
    # leaves `ok == [1, 2, 3]` trivially true, which is exactly the false pass
    # this guard exists to make impossible.
    assert d_scan_max >= 4, (
        f"d_scan_max={d_scan_max}: an upper bound at 3 is unevidenced unless "
        f"the scan reaches d >= 4")
    ok = [d for d in range(1, d_scan_max + 1)
          if dim.jacobian_ranks(d)["ker"] == 0]
    assert ok == [1, 2, 3]
    for d in range(4, d_scan_max + 1):
        assert dim.jacobian_ranks(d)["ker"] == d - 3 > 0
    return {"ker_zero_dimensions": ok, "d_scan_max": d_scan_max}


def check_B2_lower_bound_intrabranch_mass():
    """S2: an isotropy-invariant single-walk mass exists iff coker(J) != 0."""
    _PAULI = _pauli()
    # d = 2: im(J) = span(e_x, e_y), so m_hat = e_z survives.  The internal
    # operator implementing a spatial rotation about z is exp(-i theta sigma_z/2),
    # and sigma_z commutes with it -- so m sigma_z is isotropy-invariant, and
    # Hermiticity forces m real (no phase to gauge).
    J2 = _J_indep(2)
    assert J2.rank() == 2
    assert J2[2, :] == sp.Matrix([[0, 0]])          # e_z unreached
    th = sp.Symbol("theta", real=True)
    U = sp.exp(-sp.I * th * _PAULI[2] / 2)
    assert sp.simplify(U * _PAULI[2] * U.H - _PAULI[2]) == sp.zeros(2)
    assert dim.isotropic_intrabranch_mass_dim(2) == 1
    assert dim.mass_phase_is_gaugeable(2) is False

    # d = 1: two spare axes
    assert dim.isotropic_intrabranch_mass_dim(1) == 2

    # d = 3: im(J) = R^3, so NO sigma direction is left fixed.  Concretely, the
    # three Pauli matrices are all reached, and a candidate mass a.sigma would
    # have to commute with all three internal rotations, forcing a = 0.
    J3 = _J_indep(3)
    assert J3.rank() == 3
    a = sp.symbols("b1 b2 b3", real=True)
    M = sum((a[i] * _PAULI[i] for i in range(3)), sp.zeros(2))
    eqs = []
    for B in _PAULI:                    # must commute with every generator
        eqs += list(sp.simplify(M * B - B * M))
    sol = sp.solve(eqs, list(a), dict=True)
    assert sol == [{a[0]: 0, a[1]: 0, a[2]: 0}] or all(
        all(v == 0 for v in s.values()) for s in sol)
    assert dim.isotropic_intrabranch_mass_dim(3) == 0
    assert dim.mass_phase_is_gaugeable(3) is True
    return {"coker_dim": {1: 2, 2: 1, 3: 0},
            "phase_gaugeable": {1: False, 2: False, 3: True}}


def check_B3_S1_and_S2_intersect_in_three():
    sel = dim.select_dimension()
    assert sel["S1_and_S2"] == [3]
    return {"S1_and_S2": sel["S1_and_S2"]}


def check_C1_magnetic_field_is_a_vector():
    """S3, independent of the cell dimension s."""
    d = sp.Symbol("d", integer=True)
    roots = sorted(int(r) for r in sp.solve(sp.Eq(d * (d - 1) / 2, d), d))
    assert roots == [0, 3]
    assert dim.magnetic_vector_dimensions() == [0, 3]
    # no d = 7 loophole: * of a 2-form is a 1-form only when d - 2 = 1
    assert dim.hodge_vector_dimensions() == [3]
    assert dim.bivector_dim(7) == 21 != 7
    # the paired-spinor photon is a sigma-triplet in ANY d
    assert dim.bivector_dim(3) == 3
    return {"bivector_eq_vector_roots": roots, "hodge_roots": [3]}


def check_D1_orientation_corollary():
    """det J exists only at d = 3, and equals -/+ c_lat^3."""
    assert dim.chirality_orientation(1) is None
    assert dim.chirality_orientation(2) is None
    dp = sp.simplify(_J_indep(3, sign=1).det())
    dm = sp.simplify(_J_indep(3, sign=-1).det())
    assert dp == -dm != 0
    c3 = (1 / sp.sqrt(3)) ** 3
    assert sp.simplify(sp.Abs(dp) - c3) == 0
    assert sp.simplify(dim.chirality_orientation(3, "+") - dp) == 0
    assert sp.simplify(dim.chirality_orientation(3, "-") - dm) == 0
    return {"det_plus": str(dp), "det_minus": str(dm),
            "abs_det_equals_c_lat_cubed": True}


def check_D2_engine_cross_check():
    """Finite-difference the ENGINE's own BCC walk and recover the same J."""
    h = 1e-6
    cols = []
    for axis in range(3):
        kp = [0.0, 0.0, 0.0]
        km = [0.0, 0.0, 0.0]
        kp[axis] = h
        km[axis] = -h
        _, nxp, nyp, nzp = _bcc._bcc_uvec(*kp, sign="+")
        _, nxm, nym, nzm = _bcc._bcc_uvec(*km, sign="+")
        cols.append([(nxp - nxm) / (2 * h),
                     (nyp - nym) / (2 * h),
                     (nzp - nzm) / (2 * h)])
    J_num = sp.Matrix(cols).T                      # columns are d/dk_axis
    J_sym = _J_indep(3, sign=1)
    resid = max(abs(float(J_num[i, j]) - float(J_sym[i, j]))
                for i in range(3) for j in range(3))
    assert resid <= FD_TOL, resid
    det_resid = abs(abs(float(J_num.det())) - float(c_lat) ** 3)
    assert det_resid <= FD_TOL, det_resid
    return {"max_abs_residual_vs_symbolic": resid,
            "abs_det_minus_c_lat_cubed": det_resid,
            "c_lat_registry": float(c_lat)}


def check_E1_verdict():
    sel = dim.select_dimension()
    assert sel["all_three"] == [3]
    assert sel["S3_alone"] == [3]          # holds with no reference to s = 2
    rep = dim.report()
    assert rep["d_selected"] == 3
    assert rep["signature"] == "1+3"
    assert rep["time_dim"] == 1
    assert rep["c_lat_agrees"] is True
    return {"d_selected": 3, "signature": "1+3",
            "routes_that_alone_give_three": ["S1&S2", "S3"]}


CHECKS = (
    ("A1_internal_vector_dim_is_three", check_A1_internal_vector_dim_is_three),
    ("A2_jacobian_shape_and_rank", check_A2_jacobian_shape_and_rank),
    ("B1_upper_bound", check_B1_upper_bound),
    ("B2_lower_bound_intrabranch_mass", check_B2_lower_bound_intrabranch_mass),
    ("B3_S1_and_S2_intersect_in_three", check_B3_S1_and_S2_intersect_in_three),
    ("C1_magnetic_field_is_a_vector", check_C1_magnetic_field_is_a_vector),
    ("D1_orientation_corollary", check_D1_orientation_corollary),
    ("D2_engine_cross_check", check_D2_engine_cross_check),
    ("E1_verdict", check_E1_verdict),
)


def check_all(cell_dim=2, d_scan_max=8):
    """Registry entry point. Returns the full result dict.

    Two declared controls (D9/H2, `control:` on `F291-dimension-selectors`):

    ``--param cell_dim=4``     the internal vector space is 3-dimensional
        because the cell is s = 2.  A1 must go red.
    ``--param d_scan_max=3``   an upper bound at 3 needs the scan to reach
        d >= 4.  B1 must go red.
    """
    kw = {"check_A1_internal_vector_dim_is_three": {"cell_dim": cell_dim},
          "check_B1_upper_bound": {"d_scan_max": d_scan_max}}
    out = {}
    for name, fn in CHECKS:
        out[name] = fn(**kw.get(fn.__name__, {}))
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "d = 3 is selected twice over by adopted structure: (S1 & S2) from the "
        "s = 2 cell plus the Higgs-free mass step, and (S3) from the (E,B) "
        "vector pair with no reference to s. Time is 1 by construction."
    )
    return out


# --- no pytest surface ------------------------------------------------------
# Deliberately no thin `test_*` wrappers: this record is an `entry:` record, and
# tests/casim/test_registry_integrity.py forbids a file being both. `check_all`
# runs every check via CHECKS.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
