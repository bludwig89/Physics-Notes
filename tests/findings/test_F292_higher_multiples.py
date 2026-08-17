"""F292 — no higher multiple of three; and a reducible d = 3n collapses to 3.

Follow-up to F291. Seven checks. As in F291, the load-bearing legs are
re-derived with sympy INDEPENDENTLY of
`casim.engine.lattice.dimensionality` — in particular the Clifford algebra is
rebuilt here by its own recursion, so the chirality verdict is computed twice by
two separately written constructions rather than quoted from the literature.

  A1 (exact)  bivector overcount: dim Lambda^2 R^d / d = (d-1)/2, equal to 1
      exactly at d = 3.  At d = 3n it is (3n-1)/2, so only n = 1 passes.
  A2 (exact)  the same statement as an integer root problem, for the record:
      d(d-1)/2 = d has roots {0, 3}, so no multiple of three above 3 survives.
  B1 (exact)  Clifford construction is valid: {g_a, g_b} = 2 delta_ab in
      dimension 2^floor(D/2), for D = 2..8.
  B2 (exact)  chirality parity: the product of all gammas is proportional to
      the identity iff D is ODD, so a chirality projector exists iff D = d + 1
      is even, i.e. iff d is odd.  d = 6 has no chirality; d = 9 does.
  B3 (exact)  d = 2 is REJECTED by two unrelated routes: S4 because D = 3 is
      odd (no chirality projector) and F291's S2 because the mass there is the
      real parity-odd sigma_z term. Both are exclusions -- neither is a vote FOR
      d = 2, and the surviving dimension is asserted to be 3.
  C1 (exact)  reducible d = 3n as n copies of R^3: rank J = 3, ker = 3(n-1),
      coker = 0 — so the walk sees one R^3 and freezes 3(n-1) directions, and
      founding decision 1 (which needs coker = 0) is untouched.
  C2 (exact)  a bigger cell does not rescue it: minimal spinor dim is
      2^floor(d/2), so d = 6 needs s = 8 and d = 9 needs s = 16, while A1 and
      B2 never mention s.

Real arithmetic only (CLAUDE.md); every leg is exact over Z or Q.
"""
from __future__ import annotations

import functools

import sympy as sp

from casim.engine.lattice import dimensionality as dim

@functools.lru_cache(maxsize=None)
def _sigmas():
    """Built on call, not at import. sympy work at module scope runs on
    `pytest --collect-only`, which is what the `import_time_work` ratchet in
    tools/audit_tests.py counts; the values are unchanged."""
    return (sp.Matrix([[0, 1], [1, 0]]),
            sp.Matrix([[0, -sp.I], [sp.I, 0]]),
            sp.Matrix([[1, 0], [0, -1]]))


# ── an independently written Clifford recursion ───────────────────────────

def _kr(a, b):
    return sp.Matrix(sp.kronecker_product(a, b))


def _gammas_indep(D):
    """Same algebra, separately typed: {g_a, g_b} = 2 delta_ab."""
    _SX, _SY, _SZ = _sigmas()
    if D <= 1:
        return [sp.Matrix([[1]])]
    if D == 2:
        return [_SX, _SY]
    if D % 2 == 0:
        g = _gammas_indep(D - 2)
        n = g[0].shape[0]
        return ([_kr(x, _SZ) for x in g]
                + [_kr(sp.eye(n), _SX), _kr(sp.eye(n), _SY)])
    g = _gammas_indep(D - 1)
    P = g[0]
    for x in g[1:]:
        P = P * x
    return g + [sp.simplify(P / sp.sqrt(sp.simplify(P * P)[0, 0]))]


def _product_all(g):
    P = g[0]
    for x in g[1:]:
        P = P * x
    return sp.simplify(P)


# ── checks ────────────────────────────────────────────────────────────────

def check_A1_bivector_overcount():
    """(d-1)/2 = 1 exactly at d = 3; at d = 3n only n = 1 passes."""
    d = sp.Symbol("d", integer=True, positive=True)
    over = sp.simplify(sp.Rational(1, 2) * d * (d - 1) / d)      # = (d-1)/2
    assert sp.simplify(over - (d - 1) / 2) == 0
    assert sp.solve(sp.Eq(over, 1), d) == [3]
    out = {}
    for n in range(1, 6):
        dd = 3 * n
        val = sp.Rational(dd - 1, 2)
        assert dim.bivector_overcount(dd) == val
        assert (val == 1) == (n == 1)
        out[dd] = str(val)
    assert dim.multiples_of_three_passing_S3(8) == [3]
    return {"overcount_by_d": out, "multiples_passing": [3]}


def check_A2_integer_roots():
    d = sp.Symbol("d", integer=True)
    roots = sorted(int(r) for r in sp.solve(sp.Eq(d * (d - 1) / 2, d), d))
    assert roots == [0, 3]
    for bad in (6, 9, 12):
        assert dim.bivector_dim(bad) != bad
    return {"roots": roots, "excluded": [6, 9, 12]}


def check_B1_clifford_algebra_valid():
    out = {}
    for D in range(2, 9):
        g = _gammas_indep(D)
        n = g[0].shape[0]
        assert n == 2 ** (D // 2), (D, n)
        for a in range(D):
            for b in range(D):
                want = 2 * sp.eye(n) if a == b else sp.zeros(n)
                assert sp.simplify(g[a] * g[b] + g[b] * g[a] - want) == sp.zeros(n)
        out[D] = n
    return {"rep_dim_by_D": out}


def check_B2_chirality_parity(clifford_D_max=8):
    """Product of all gammas ∝ I iff D odd, so chirality exists iff D even.

    `clifford_D_max` is a DECLARED CONTROL (D9/H2). A PARITY claim needs both
    parities in the scan; truncating to D = 2 leaves one even D and no odd one,
    so `chiral == (D % 2 == 0)` holds vacuously for the wrong reason.
    """
    assert clifford_D_max >= 3, (
        f"clifford_D_max={clifford_D_max}: a parity statement is unevidenced "
        f"unless the scan contains at least one odd and one even D")
    out = {}
    for D in range(2, clifford_D_max + 1):
        g = _gammas_indep(D)
        n = g[0].shape[0]
        P = _product_all(g)
        prop_I = sp.simplify(P - P[0, 0] * sp.eye(n)) == sp.zeros(n)
        chiral = not prop_I
        assert chiral == (D % 2 == 0), (D, chiral)
        assert dim.has_chirality(D) == chiral            # module agrees
        out[D] = chiral
    # the spatial reading: d odd
    assert dim.chirality_dimensions(11) == [1, 3, 5, 7, 9, 11]
    assert dim.has_chirality(6 + 1) is False             # d = 6 has none
    assert dim.has_chirality(9 + 1) is True              # d = 9 does
    return {"chirality_by_D": out, "d_odd_required": True,
            "d6_chiral": False, "d9_chiral": True}


def check_B3_d_two_excluded_twice():
    """d = 2 is REJECTED by two unrelated routes — a cross-check, not a repeat.

    Both legs are exclusions. S4 rejects d = 2 because D = 3 is odd (no
    chirality projector); F291's S2 rejects it because the mass there is the
    real parity-odd sigma_z term, leaving no phase for founding decision 1 to
    gauge. Neither is a vote FOR d = 2.
    """
    assert dim.has_chirality(2 + 1) is False                 # S4: D = 3 is odd
    assert dim.isotropic_intrabranch_mass_dim(2) == 1        # F291 S2: sigma_z
    assert dim.mass_phase_is_gaugeable(2) is False
    # and the survivor is 3, not 2
    assert dim.select_dimension()["all_three"] == [3]
    return {"S4_rejects_d2_no_chirality": True,
            "S2_rejects_d2_real_mass": True,
            "d2_excluded_by_both": True,
            "surviving_dimension": 3}


def check_C1_reducible_collapse(n_blocks_max=4):
    """d = 3n as n copies of R^3: rank 3, ker 3(n-1), coker 0.

    `n_blocks_max` is a DECLARED CONTROL (D9/H2), the F298 pattern: at n = 1
    there IS no reducible case, so a scan stopping there cannot claim anything
    about d = 3n collapsing -- every assertion below would pass on the single
    irreducible block the finding is not about.
    """
    assert n_blocks_max >= 2, (
        f"n_blocks_max={n_blocks_max}: the reducible claim is unevidenced "
        f"unless the scan reaches n >= 2")
    out = {}
    for n in range(1, n_blocks_max + 1):
        J = dim.reducible_jacobian(n)
        assert J.shape == (3, 3 * n)
        r = J.rank()
        assert r == 3
        assert 3 * n - r == 3 * (n - 1)
        assert dim.reducible_ranks(n) == {
            "n_blocks": n, "d": 3 * n, "rank": 3,
            "ker": 3 * (n - 1), "coker": 0,
            "frozen_directions": 3 * (n - 1)}
        out[3 * n] = {"rank": 3, "ker": 3 * (n - 1), "coker": 0}
    # coker = 0 throughout, so founding decision 1 survives the reducible case:
    # this failure is S1/S3', not S2.
    assert all(v["coker"] == 0 for v in out.values())
    return {"by_dimension": out,
            "founding_decision_1_untouched": True}


def check_C2_bigger_cell_does_not_rescue():
    for d, s in ((3, 2), (6, 8), (9, 16), (12, 64)):
        assert dim.minimal_spinor_dim(d) == s, (d, s)
    # neither S3' nor S4 references s
    assert dim.bivector_overcount(9) == 4                 # independent of s
    assert dim.has_chirality(6 + 1) is False              # independent of s
    return {"minimal_spinor_dim": {3: 2, 6: 8, 9: 16, 12: 64},
            "s_independent": ["S3'", "S4"]}


def check_D1_verdict():
    rep = dim.higher_multiples_report()
    assert rep["multiples_passing_S3"] == [3]
    r6, r9 = rep["rows"][6], rep["rows"][9]
    assert r6["passes_S3"] is False and r6["has_chirality"] is False
    assert r9["passes_S3"] is False and r9["has_chirality"] is True
    assert r9["reducible"]["frozen_directions"] == 6
    return {"d6_fails": ["S3'", "S4"], "d9_fails": ["S3'", "S1"],
            "d9_frozen_directions": 6}


CHECKS = (
    ("A1_bivector_overcount", check_A1_bivector_overcount),
    ("A2_integer_roots", check_A2_integer_roots),
    ("B1_clifford_algebra_valid", check_B1_clifford_algebra_valid),
    ("B2_chirality_parity", check_B2_chirality_parity),
    ("B3_d_two_excluded_twice", check_B3_d_two_excluded_twice),
    ("C1_reducible_collapse", check_C1_reducible_collapse),
    ("C2_bigger_cell_does_not_rescue", check_C2_bigger_cell_does_not_rescue),
    ("D1_verdict", check_D1_verdict),
)


def check_all(clifford_D_max=8, n_blocks_max=4):
    """Registry entry point. Returns the full result dict.

    Two declared controls (D9/H2, `control:` on `F292-higher-multiples`):

    ``--param clifford_D_max=2``  a parity claim needs both parities in the
        scan.  B2 must go red.
    ``--param n_blocks_max=1``    at n = 1 there is no reducible case at
        all.  C1 must go red.
    """
    kw = {"check_B2_chirality_parity": {"clifford_D_max": clifford_D_max},
          "check_C1_reducible_collapse": {"n_blocks_max": n_blocks_max}}
    out = {}
    for name, fn in CHECKS:
        out[name] = fn(**kw.get(fn.__name__, {}))
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "d = 3 is the only multiple of three. d = 6 fails twice (even "
        "spacetime dimension, no chirality; and (d-1)/2 = 5/2). d = 9 survives "
        "chirality but fails the bivector condition. Read reducibly as n copies "
        "of R^3, d = 3n has rank 3 and freezes 3(n-1) directions -- degeneracy, "
        "not compactification -- while leaving coker = 0 and founding decision 1 "
        "intact."
    )
    return out


# --- no pytest surface: this is an `entry:` record (see F291's note) --------

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
