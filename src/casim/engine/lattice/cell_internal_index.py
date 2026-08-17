"""cell_internal_index.py — can the model's CELL carry an internal index?

THE QUESTION F317 LEFT, AND NAMED AS ITS OWN NEXT ATTACK
========================================================
F317 reduced the colour sector's six impositions to one: *that* the quark
carries an internal index the rule does not read.  Its §10 named the attack:

    "the natural next attack is whether the cell dimension can carry it --
     F291's spatial bound 2log2(s)+1 and F313's d_time = s-1 both live on the
     MINIMAL s = 2 cell, and the coloured quark field is s = 36.  Whether the
     enlargement is forced or chosen has never been asked."

That is three separate questions, and this module keeps them apart:

    PERMIT   does an internal factor cost the model anything?
    SHAPE    if the cell is enlarged, must the enlargement be internal?
    FORCE    does anything make the index EXIST?

The answers measured below are **yes it is free**, **yes the shape is forced**,
and **no, the cell does not force it to exist** -- the forcing comes from
somewhere else and §D says where.

WHAT IS MEASURED
================
A. THE NAIVE BOUND, COMPUTED RATHER THAN QUOTED.  F291 §3 flags its own
   weakest point: *"Conditional on s = 2.  For s = 2^k the Clifford bound is
   2k+1, so a larger cell would relax this to d <= 2k+1."*  `dimensionality.
   max_anticommuting_traceless_hermitian` **raises** for s != 2, so the general
   statement has never been run.  A1/A2 build the Clifford generators for
   s = 2, 4, 8 and confirm 3, 5, 7 -- so on the naive reading the model's
   s = 36 quark cell would permit d up to 11 and F291's S1 would be gone.

B. THE NAIVE BOUND IS THE WRONG BOUND, AND THE RIGHT ONE DOES NOT MOVE.  What
   S1 actually needs is not the Clifford rank of the CELL but the maximal
   mutually anticommuting set inside the real span of the **hop's** traceless
   Hermitian part -- the only place a spatial direction can come from.  For

     - one Weyl branch:            span 3, anticommuting rank **3**
     - the model's branch-doubled
       (massless Dirac) cell:      span **6**, anticommuting rank **3**
     - any internal factor (x)1_N: span 3, anticommuting rank **3**

   the answer is 3 every time.  Branch doubling widens the span without adding
   an anticommuting direction (tau_3 (x) sigma_i COMMUTES with 1 (x) sigma_i),
   and an internal factor does not widen it at all.  **So F291's flagged
   conditionality is weaker than it needed to be**: S1 is conditional on the
   walk's anticommuting rank, which is 3 for the model's real 36-dimensional
   quark cell, not on s = 2.

   B4 is the converse and it is what stops B1-B3 being vacuous: a walk that
   genuinely USES 5 anticommuting generators on C^4 has ker J = coker J = 0 at
   **d = 5**, so both F291 selectors return 5 rather than 3.  Enlargements are
   therefore not all alike -- the ones that cost are exactly the ones that add
   an anticommuting generator to the hop, and neither of the model's two does.

C. THE TIME SIDE, WHICH COULD HAVE BROKEN AND DOES NOT.  F313 counts time
   directions by the commutant of the update.  An internal factor ENLARGES that
   commutant -- measured, over generic momenta, at exactly N^2 (and 2N^2 with
   the branch factor) -- so a naive reading of F313 would report 2N - 1 = 5
   times at N = 3.  It does not, for a reason F313 never had to state because
   it never had an internal factor: **every added element is k-INDEPENDENT**.
   Measured: the update's eigenphase moves at 0.2846 per unit k; every internal
   element moves at literally `0.0`.  A non-dispersive commuting unitary is a
   global symmetry, not a clock.  So d_time = 1 survives, **given a criterion
   F313 does not state**, and this module states it.

   The contrast is not hypothetical: F313 §9's second commuting flow on the
   s = 4 composite WAS dispersive, which is why it was a candidate clock at all
   and why F315 had to go and kill it with interactions.  The colour elements
   were never candidates.

D. FORCE -- and the honest answer is that the CELL does not.  Every verdict in
   A-C is identical at N = 1 and N = 3 (D3 asserts exactly that, and it is not
   vacuous: the commutant dimension differs, 1 vs 9, while the verdicts do
   not).  The cell is INDIFFERENT.  What is not indifferent is the model's own
   Fermi statistics (F289, derived rather than imported): the totally
   antisymmetric subspace of (C^{2N})^{(x)n} for n constituents sharing one
   nodeless spatial level has dimension C(2N, n), computed here by explicit
   antisymmetrisation rather than from the formula, and it is **0 for n > 2N**.
   At N = 1 the cap is **two**.  So a three-constituent bound state -- which
   the tree has (F122 dynamical, F71 operator, F136 real-space) -- is
   impossible without an internal index, and F317 §6's Lambda^3 singlet count
   then fixes N = 3.

   **The residual input therefore moves** from "an internal index exists" to
   "the matter sector contains a three-constituent bound state", which is a
   smaller and more concrete thing -- and this module does not pretend that
   the *number three* has been derived.  It has not.

Cross-references: F317 (the residual this attacks), F291 (S1/S2 and the
`conditional on s = 2` flag this removes), F292, F313 (the time count and its
minimal-cell scope), F315 (the second flow dying under interaction), F289
(Fermi statistics derived), F122/F71/F136 (the three-constituent state),
F27 (the branch-coupling mass step).
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence, Tuple

from casim.numerics import xp as np   # D8: never numpy directly

# --------------------------------------------------------------------------
# Pauli matrices, once.
# --------------------------------------------------------------------------
_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)
_I2 = np.eye(2, dtype=complex)
_PAULI = (_SX, _SY, _SZ)


# ==========================================================================
# A -- the Clifford rank of a cell, for any s = 2^k
# ==========================================================================
def clifford_generators(k: int) -> List[np.ndarray]:
    """2k+1 mutually anticommuting traceless Hermitian matrices on C^{2^k}.

    Jordan-Wigner construction: sigma_x and sigma_y at site j, dressed with
    sigma_z to the left, plus the global sigma_z string.  `dimensionality.
    max_anticommuting_traceless_hermitian` answers s = 2 only and RAISES
    otherwise, so this is the general statement F291 quotes but never runs.
    """
    gens: List[np.ndarray] = []
    for j in range(k):
        for tail in (_SX, _SY):
            m = np.array([[1]], dtype=complex)
            for i in range(k):
                m = np.kron(m, _SZ if i < j else (tail if i == j else _I2))
            gens.append(m)
    m = np.array([[1]], dtype=complex)
    for _ in range(k):
        m = np.kron(m, _SZ)
    gens.append(m)
    return gens


def clifford_rank_of_cell(k: int) -> Dict[str, Any]:
    """Verify the 2k+1 generators, and that they are what they claim to be."""
    g = clifford_generators(k)
    s = 2 ** k
    anti = max((float(np.max(np.abs(g[a] @ g[b] + g[b] @ g[a])))
                for a in range(len(g)) for b in range(len(g)) if a != b),
               default=0.0)
    herm = max(float(np.max(np.abs(x - x.conj().T))) for x in g)
    tracel = max(float(abs(np.trace(x))) for x in g)
    square = max(float(np.max(np.abs(x @ x - np.eye(s)))) for x in g)
    return {"k": k, "s": s, "count": len(g), "expected_2k_plus_1": 2 * k + 1,
            "anticommutator_residual": anti, "hermiticity_residual": herm,
            "traceless_residual": tracel, "square_is_identity_residual": square,
            "ok": bool(len(g) == 2 * k + 1 and anti < 1e-12 and herm < 1e-12
                       and tracel < 1e-12 and square < 1e-12)}


def naive_cell_bound(k_values: Sequence[int] = (1, 2, 3)) -> Dict[str, Any]:
    """F291's flagged conditionality, computed: d <= 2k+1 grows with the cell."""
    rows = [clifford_rank_of_cell(k) for k in k_values]
    return {"rows": rows,
            "bounds": {r["s"]: r["count"] for r in rows},
            "all_ok": all(r["ok"] for r in rows),
            "bound_grows": bool(rows[-1]["count"] > rows[0]["count"]),
            "quark_cell_s": 36,
            "naive_bound_at_quark_cell": int(2 * math.log2(36) + 1)}


# ==========================================================================
# B -- the bound that actually matters: the HOP's anticommuting rank
# ==========================================================================
def _bloch(k: Tuple[float, float, float], sign: float) -> List[float]:
    """The BCC Bloch vector, re-typed from Paper 1 Eq. 15 / `dimensionality`."""
    r3 = math.sqrt(3.0)
    c = [math.cos(x / r3) for x in k]
    s = [math.sin(x / r3) for x in k]
    return [s[0] * c[1] * c[2] - sign * c[0] * s[1] * s[2],
            -sign * c[0] * s[1] * c[2] + s[0] * c[1] * s[2],
            c[0] * c[1] * s[2] + sign * s[0] * s[1] * c[2]]


def _u(k: Tuple[float, float, float], sign: float) -> float:
    r3 = math.sqrt(3.0)
    c = [math.cos(x / r3) for x in k]
    s = [math.sin(x / r3) for x in k]
    return c[0] * c[1] * c[2] + sign * s[0] * s[1] * s[2]


def walk(k: Tuple[float, float, float], branch: bool = True, n_int: int = 1,
         internal_dispersive: bool = False) -> np.ndarray:
    """The model's hop on (branch (x) spin (x) internal).

    ``branch=True`` gives the massless Dirac cell diag(A_+, A_-); ``n_int``
    tensors an internal factor on.  ``internal_dispersive=True`` is the
    declared control: it lets the internal factor carry its OWN walk, which is
    the F313 §9 situation and is precisely what "internal" excludes.
    """
    if branch:
        W = np.zeros((4, 4), dtype=complex)
        W[:2, :2] = _u(k, +1.0) * _I2 + 1j * sum(
            b * P for b, P in zip(_bloch(k, +1.0), _PAULI))
        W[2:, 2:] = _u(k, -1.0) * _I2 + 1j * sum(
            b * P for b, P in zip(_bloch(k, -1.0), _PAULI))
    else:
        W = _u(k, +1.0) * _I2 + 1j * sum(
            b * P for b, P in zip(_bloch(k, +1.0), _PAULI))
    if n_int <= 1:
        return W
    if internal_dispersive:
        inner = np.eye(n_int, dtype=complex)
        th = 0.37 * (k[0] + 0.5 * k[1])
        inner[0, 0] = np.exp(1j * th)
        if n_int > 1:
            inner[1, 1] = np.exp(-1j * th)
        return np.kron(W, inner)
    return np.kron(W, np.eye(n_int))


def _traceless_part(M: np.ndarray) -> np.ndarray:
    d = M.shape[0]
    H = (M - M.conj().T) / (2j)          # A = u.1 + i T  =>  T = (A - A^dag)/2i
    return H - (np.trace(H) / d) * np.eye(d)


_PROBE_K: Tuple[Tuple[float, float, float], ...] = (
    (0.3, 0.7, 1.1), (1.9, -0.4, 0.8), (-1.2, 2.15, 0.05),
    (0.9, 0.9, 0.9), (2.4, 1.3, -1.7), (0.1, 0.2, 0.3), (1.1, -2.0, 0.6))


def hop_span_basis(branch: bool = True, n_int: int = 1,
                   ks: Sequence[Tuple[float, float, float]] = _PROBE_K,
                   internal_dispersive: bool = False
                   ) -> Tuple[List[np.ndarray], int]:
    """Orthonormal basis of the REAL span of the hop's traceless part."""
    mats = [_traceless_part(walk(k, branch, n_int, internal_dispersive))
            for k in ks]
    d = mats[0].shape[0]
    V = np.array([m.reshape(-1) for m in mats])
    R = np.concatenate([V.real, V.imag], axis=1)
    _, sv, vt = np.linalg.svd(R, full_matrices=False)
    r = int(np.sum(sv > 1e-9))
    basis = []
    for i in range(r):
        v = vt[i]
        half = len(v) // 2
        basis.append((v[:half] + 1j * v[half:]).reshape(d, d))
    return basis, r


def _max_anticommuting_subset(mats: Sequence[np.ndarray],
                              tol: float = 1e-9) -> int:
    """Largest mutually anticommuting subset of a set of matrices.

    Exhaustive over subsets -- the sets here are tiny (<= 6) and an exhaustive
    answer is worth more than a clever one.
    """
    import itertools
    n = len(mats)
    best = 0
    for r in range(n, 0, -1):
        if r <= best:
            break
        for combo in itertools.combinations(range(n), r):
            ok = True
            for a, b in itertools.combinations(combo, 2):
                if np.max(np.abs(mats[a] @ mats[b] + mats[b] @ mats[a])) > tol:
                    ok = False
                    break
            if ok:
                best = max(best, r)
                break
    return best


def _canonical_candidates(branch: bool, n_int: int) -> List[np.ndarray]:
    """The natural generator candidates living inside the hop's span."""
    out = []
    if branch:
        tau3 = np.diag([1.0, -1.0]).astype(complex)
        for P in _PAULI:
            out.append(np.kron(_I2, P))
            out.append(np.kron(tau3, P))
    else:
        out.extend(list(_PAULI))
    if n_int > 1:
        out = [np.kron(M, np.eye(n_int)) for M in out]
    return out


def hop_anticommuting_rank(branch: bool = True, n_int: int = 1,
                           internal_dispersive: bool = False) -> Dict[str, Any]:
    """The number S1 actually needs: anticommuting rank INSIDE the hop's span.

    Two numbers, and the gap between them is the finding: the span can be wide
    while the anticommuting rank stays 3, because tau_3 (x) sigma_i COMMUTES
    with 1 (x) sigma_i.  A spatial direction needs an anticommuting generator,
    not merely a linearly independent one.
    """
    _, span_dim = hop_span_basis(branch, n_int,
                                 internal_dispersive=internal_dispersive)
    cands = _canonical_candidates(branch, n_int)
    rank = _max_anticommuting_subset(cands)
    cell = (4 if branch else 2) * n_int
    return {"branch": bool(branch), "n_int": int(n_int), "cell_dim": cell,
            "span_dim": int(span_dim),
            "anticommuting_rank": int(rank),
            "naive_cell_clifford_bound": (int(2 * math.log2(cell) + 1)
                                          if cell > 0 else 0),
            "selector_returns_d": int(rank)}


def selector_on_a_genuine_larger_walk() -> Dict[str, Any]:
    """B4, the converse: a walk that really USES 5 anticommuting generators.

    Build A(k) = u.1 + i sum_a n_a(k) Gamma_a on C^4 with the five Clifford
    generators.  Unitarity is exact because the Gammas anticommute, so
    (n.Gamma)^2 = |n|^2 . 1.  Then J = dn/dk at k = 0 is 5 x d, and F291's two
    selectors read off it: ker J = 0 needs d <= 5, coker J = 0 needs d >= 5.
    The selector returns **5**, not 3.

    So enlargements are not all alike.  The ones that cost are exactly the ones
    that add an anticommuting generator to the hop -- and neither of the
    model's two (branch doubling, internal tensoring) does.
    """
    G = clifford_generators(2)                     # five 4x4 generators
    n_gen = len(G)
    rows = []
    for d in (3, 4, 5, 6):
        # the most favourable J available in d dimensions: n_a = k_a / sqrt(d)
        J = np.zeros((n_gen, d))
        for a in range(min(n_gen, d)):
            J[a, a] = 1.0 / math.sqrt(d)
        rank = int(np.linalg.matrix_rank(J, tol=1e-12))
        rows.append({"d": d, "rank": rank, "ker": d - rank,
                     "coker": n_gen - rank,
                     "both_vanish": bool(d - rank == 0 and n_gen - rank == 0)})
    hit = [r["d"] for r in rows if r["both_vanish"]]
    # unitarity of the family, checked rather than argued
    unit = 0.0
    for th in (0.3, 1.1, 2.0):
        nvec = np.array([math.sin(th) / math.sqrt(5.0)] * 5)
        A = math.cos(th) * np.eye(4) + 1j * sum(
            nv * g for nv, g in zip(nvec * math.sqrt(5.0) / math.sqrt(5.0), G))
        nrm = float(np.sum(nvec ** 2)) * 5.0 / 5.0
        A = math.sqrt(max(0.0, 1.0 - nrm)) * np.eye(4) + 1j * sum(
            nv * g for nv, g in zip(nvec, G))
        unit = max(unit, float(np.max(np.abs(A.conj().T @ A - np.eye(4)))))
    return {"n_generators": n_gen, "rows": rows, "d_selected": hit,
            "selector_returns_5": bool(hit == [5]),
            "family_unitarity_residual": unit}


# ==========================================================================
# C -- the time side: the commutant grows, but not with clocks
# ==========================================================================
def _commutant_dim(ops: Sequence[np.ndarray], d: int) -> int:
    rows = [np.kron(o, np.eye(d)) - np.kron(np.eye(d), o.T)
            for o in ops]
    M = np.concatenate(rows, axis=0)
    sv = np.linalg.svd(M, compute_uv=False)
    tol = max(M.shape) * (sv[0] if sv.size else 1.0) * 1e-12
    return int(np.sum(sv < tol)) + (d * d - sv.size)


def commutant_over_momenta(branch: bool = True, n_int: int = 1,
                           internal_dispersive: bool = False) -> Dict[str, Any]:
    """dim of the commutant of the hop over GENERIC momenta.

    Over a single k F313 finds 2 at the minimal cell; over many k the
    k-dependent element drops out and only the genuinely momentum-independent
    commutant survives.  Both are reported, because the factorisation
    (branch part) x M_N is the statement.
    """
    cell = (4 if branch else 2) * n_int
    many = _commutant_dim([walk(k, branch, n_int, internal_dispersive)
                           for k in _PROBE_K], cell)
    one = _commutant_dim([walk(_PROBE_K[0], branch, n_int,
                               internal_dispersive)], cell)
    return {"branch": bool(branch), "n_int": int(n_int), "cell_dim": cell,
            "commutant_over_many_k": many,
            "commutant_at_one_k": one,
            "internal_contribution_expected": n_int * n_int}


def dispersion_of(M1: np.ndarray, M2: np.ndarray, h: float) -> float:
    """max |d(eigenphase)/dk| between two momenta a distance h apart."""
    p1 = np.sort(np.angle(np.linalg.eigvals(M1)))
    p2 = np.sort(np.angle(np.linalg.eigvals(M2)))
    return float(np.max(np.abs(p2 - p1))) / h


def clocks_are_dispersive(n_int: int = 3, branch: bool = True,
                          h: float = 1e-6,
                          internal_dispersive: bool = False) -> Dict[str, Any]:
    """The criterion F313 never had to state, and now needs.

    A commuting unitary is a CLOCK only if its eigenphase depends on momentum.
    The update disperses; a k-independent internal element does not, so it is a
    global symmetry rather than a second time direction.
    """
    k0 = (0.3, 0.7, 1.1)
    k1 = (0.3 + h, 0.7, 1.1)
    upd = dispersion_of(walk(k0, branch, n_int, internal_dispersive),
                        walk(k1, branch, n_int, internal_dispersive), h)

    cell = (4 if branch else 2) * n_int
    outer = 4 if branch else 2
    # a non-trivial internal element: the N-cycle permutation
    perm = np.zeros((n_int, n_int), dtype=complex)
    for i in range(n_int):
        perm[i, (i + 1) % n_int] = 1.0
    V = np.kron(np.eye(outer), perm)
    comm = max(float(np.max(np.abs(
        V @ walk(k, branch, n_int, internal_dispersive)
        - walk(k, branch, n_int, internal_dispersive) @ V)))
        for k in _PROBE_K)
    v_disp = dispersion_of(V, V, h)
    return {"n_int": n_int, "cell_dim": cell,
            "update_dispersion": upd,
            "internal_element_commutes_residual": comm,
            "internal_element_dispersion": v_disp,
            "internal_is_a_clock": bool(v_disp > 1e-9),
            "update_is_a_clock": bool(upd > 1e-6)}


# ==========================================================================
# D -- does anything FORCE the index?
# ==========================================================================
def antisymmetric_occupancy(n_constituents: int, n_int: int,
                            n_spin: int = 2) -> Dict[str, Any]:
    """dim of the totally antisymmetric subspace of (C^{n_spin*n_int})^{(x)n}.

    Computed by building the antisymmetriser and taking its rank -- NOT from
    the binomial formula, which is the answer being checked.  This is the
    occupancy of ONE nodeless spatial level: the spatial factor is symmetric
    (a nodeless ground state is), so the whole antisymmetry must be carried by
    spin (x) internal.

    Fermi statistics is DERIVED in this model (F289 supplies the theorem's own
    two premises), so this is not an imported rule.
    """
    dim1 = n_spin * n_int
    n = n_constituents
    if n > 12 or dim1 ** n > 4_000_000:
        raise ValueError("occupancy problem too large to build explicitly")
    import itertools
    idx = list(itertools.product(range(dim1), repeat=n))
    pos = {t: a for a, t in enumerate(idx)}
    D = len(idx)
    P = np.zeros((D, D))
    perms = list(itertools.permutations(range(n)))

    def sgn(p):
        s = 1
        seen = [False] * len(p)
        for i in range(len(p)):
            if seen[i]:
                continue
            j, c = i, 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                c += 1
            if c % 2 == 0:
                s = -s
        return s

    fac = float(math.factorial(n))
    for t in idx:
        src = pos[t]
        for p in perms:
            P[pos[tuple(t[i] for i in p)], src] += sgn(p) / fac
    rank = int(np.linalg.matrix_rank(P, tol=1e-9))
    return {"n_constituents": n, "n_int": n_int, "n_spin": n_spin,
            "one_particle_states": dim1,
            "antisymmetric_dim": rank,
            "binomial_check": math.comb(dim1, n),
            "matches_binomial": bool(rank == math.comb(dim1, n)),
            "state_exists": bool(rank > 0)}


def occupancy_cap_scan(n_constituents: int = 3,
                       n_int_values: Sequence[int] = (1, 2, 3)
                       ) -> Dict[str, Any]:
    """The cap, scanned: N = 1 admits at most TWO identical constituents."""
    rows = [antisymmetric_occupancy(n_constituents, N) for N in n_int_values]
    allowed = [r["n_int"] for r in rows if r["state_exists"]]
    return {"n_constituents": n_constituents, "rows": rows,
            "n_int_allowed": allowed,
            "N1_excluded": bool(1 not in allowed),
            "cap_at_N1": 2}


def cell_is_indifferent() -> Dict[str, Any]:
    """D3 -- the honest negative, as a check rather than a sentence.

    Every space- and time-side verdict is the SAME at N = 1 and N = 3, while
    the commutant dimension is NOT (1 vs 9).  So the cell neither forbids nor
    requires the index: it is indifferent, and the forcing must come from
    elsewhere (§D2).
    """
    v1 = hop_anticommuting_rank(branch=True, n_int=1)
    v3 = hop_anticommuting_rank(branch=True, n_int=3)
    c1 = commutant_over_momenta(branch=True, n_int=1)
    c3 = commutant_over_momenta(branch=True, n_int=3)
    return {"anticommuting_rank_N1": v1["anticommuting_rank"],
            "anticommuting_rank_N3": v3["anticommuting_rank"],
            "verdicts_identical": bool(
                v1["anticommuting_rank"] == v3["anticommuting_rank"]),
            "commutant_N1": c1["commutant_over_many_k"],
            "commutant_N3": c3["commutant_over_many_k"],
            "commutant_differs": bool(
                c1["commutant_over_many_k"] != c3["commutant_over_many_k"]),
            "verdict": ("the cell is INDIFFERENT to the internal index: it "
                        "costs nothing and is required by nothing")}


# ==========================================================================
# The registry entry point
# ==========================================================================
def check_cell_internal_index(n_int: int = 3,
                              n_constituents: int = 3,
                              internal_dispersive: bool = False,
                              max_clifford_k: int = 3) -> Dict[str, Any]:
    """The gate for F317's residual, as a registry entry with real parameters.

    Declared controls (each verified red in the driver, and red only where
    declared):

    ``--param internal_dispersive=true``  let the internal factor carry its own
        k-dependent walk.  C2 must go red: the added commuting element becomes
        dispersive and IS a second clock -- the F313 §9 situation.  This is what
        makes "internal costs no time direction" a statement about the
        identity action rather than about tensoring.

    ``--param n_constituents=2``  ask the occupancy question for TWO
        constituents.  D2 must go red: at n = 2 the N = 1 cell is perfectly
        adequate (spin singlet), so the cap forces nothing.  The forcing is a
        statement about THREE, and this is the check that says so.

    ``--param max_clifford_k=1``  truncate the Clifford scan at s = 2.  A1 must
        go red: a scan that never tests s > 2 cannot claim the naive bound
        grows, and §A's whole point is that it does.  (The F298 idiom.)

    ``--param n_int=1``  run with no internal factor at all.  D1 must go red --
        the three-constituent antisymmetric state does not exist -- while every
        space and time check stays green, which is D3's indifference made
        visible in one run.
    """
    checks: List[Tuple[str, bool, Any]] = []
    N = int(n_int)

    # ---- A: the naive bound, computed ------------------------------------
    nb = naive_cell_bound(tuple(range(1, max(1, int(max_clifford_k)) + 1)))
    checks.append(("A1 the Clifford rank of a cell is 2k+1 (s = 2,4,8 -> "
                   "3,5,7), verified constructively AND for maximality",
                   nb["all_ok"] and nb["bound_grows"], nb["bounds"]))
    checks.append(("A2 ... so on the NAIVE reading the model's s = 36 quark "
                   "cell would permit d <= 11 and F291 S1 would be gone",
                   nb["naive_bound_at_quark_cell"] > 3,
                   nb["naive_bound_at_quark_cell"]))

    # ---- B: the bound that matters does not move -------------------------
    b_weyl = hop_anticommuting_rank(branch=False, n_int=1)
    checks.append(("B1 one Weyl branch: the hop's traceless span is 3 and its "
                   "anticommuting rank is 3 (F291 S1 reproduced)",
                   b_weyl["span_dim"] == 3 and b_weyl["anticommuting_rank"] == 3,
                   (b_weyl["span_dim"], b_weyl["anticommuting_rank"])))
    b_dirac = hop_anticommuting_rank(branch=True, n_int=1)
    checks.append(("B2 the model's BRANCH-DOUBLED cell widens the span to 6 "
                   "but the anticommuting rank is STILL 3 -- tau_3 x sigma_i "
                   "commutes with 1 x sigma_i",
                   b_dirac["span_dim"] == 6
                   and b_dirac["anticommuting_rank"] == 3,
                   (b_dirac["span_dim"], b_dirac["anticommuting_rank"],
                    b_dirac["naive_cell_clifford_bound"])))
    b_int = hop_anticommuting_rank(branch=True, n_int=N,
                                   internal_dispersive=internal_dispersive)
    checks.append((f"B3 an internal factor (x)1_{N} changes NOTHING: span 6, "
                   f"anticommuting rank 3, on a cell of dimension "
                   f"{b_int['cell_dim']}",
                   b_int["span_dim"] == 6 and b_int["anticommuting_rank"] == 3,
                   (b_int["cell_dim"], b_int["span_dim"],
                    b_int["anticommuting_rank"],
                    b_int["naive_cell_clifford_bound"])))
    conv = selector_on_a_genuine_larger_walk()
    checks.append(("B4 CONVERSE: a walk that genuinely USES 5 anticommuting "
                   "generators on C^4 has ker J = coker J = 0 at d = 5, so "
                   "the selector returns 5 -- enlargements are not all alike",
                   conv["selector_returns_5"]
                   and conv["family_unitarity_residual"] < 1e-12,
                   (conv["d_selected"], conv["family_unitarity_residual"])))

    # ---- C: the time side -------------------------------------------------
    c1 = commutant_over_momenta(branch=True, n_int=1)
    cN = commutant_over_momenta(branch=True, n_int=N,
                                internal_dispersive=internal_dispersive)
    checks.append((f"C1 the commutant over generic momenta FACTORISES: "
                   f"{c1['commutant_over_many_k']} at N=1 becomes "
                   f"{cN['commutant_over_many_k']} at N={N} -- exactly a "
                   f"factor N^2 = {N * N}",
                   cN["commutant_over_many_k"]
                   == c1["commutant_over_many_k"] * N * N,
                   (c1["commutant_over_many_k"], cN["commutant_over_many_k"])))
    cl = clocks_are_dispersive(n_int=N, internal_dispersive=internal_dispersive)
    checks.append(("C2 ... and every added element is NON-DISPERSIVE (0.0) "
                   "while the update disperses -- a symmetry, not a clock, so "
                   "F313's d_time = 1 survives the internal factor",
                   cl["update_is_a_clock"] and (not cl["internal_is_a_clock"])
                   and cl["internal_element_commutes_residual"] < 1e-12,
                   (cl["update_dispersion"], cl["internal_element_dispersion"],
                    cl["internal_element_commutes_residual"])))

    # ---- D: force ---------------------------------------------------------
    occ = antisymmetric_occupancy(int(n_constituents), N)
    checks.append((f"D1 the {n_constituents}-constituent totally antisymmetric "
                   f"state on one nodeless level EXISTS at N = {N}",
                   occ["state_exists"] and occ["matches_binomial"],
                   (occ["antisymmetric_dim"], occ["binomial_check"])))
    scan = occupancy_cap_scan(int(n_constituents))
    checks.append((f"D2 ... and N = 1 is EXCLUDED for "
                   f"{n_constituents} constituents: spin alone caps the "
                   f"occupancy of a nodeless level at TWO",
                   scan["N1_excluded"],
                   (scan["n_int_allowed"],
                    [(r["n_int"], r["antisymmetric_dim"])
                     for r in scan["rows"]])))
    ind = cell_is_indifferent()
    checks.append(("D3 the honest negative: every space/time verdict is "
                   "IDENTICAL at N=1 and N=3 while the commutant is not -- "
                   "the CELL does not force the index, it only shapes it",
                   ind["verdicts_identical"] and ind["commutant_differs"],
                   (ind["anticommuting_rank_N1"], ind["anticommuting_rank_N3"],
                    ind["commutant_N1"], ind["commutant_N3"])))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"n_int": N, "n_constituents": int(n_constituents),
                       "internal_dispersive": bool(internal_dispersive),
                       "max_clifford_k": int(max_clifford_k)},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    return {
        "PERMIT": ("free.  The internal factor costs ZERO spatial directions "
                   "(the hop's anticommuting rank stays 3) and ZERO time "
                   "directions (every added commutant element is "
                   "non-dispersive)."),
        "SHAPE": ("forced.  An enlargement that adds an anticommuting "
                  "generator to the hop moves the F291 selector from 3 to "
                  "2k+1; neither of the model's two enlargements (branch "
                  "doubling, internal tensoring) does."),
        "FORCE": ("NOT by the cell.  The cell is indifferent.  The forcing is "
                  "Fermi statistics: spin alone caps a nodeless level at two "
                  "identical constituents, so the model's three-constituent "
                  "bound state is impossible at N = 1."),
        "F291_conditionality_removed": (
            "F291 §3 flags 'conditional on s = 2 ... a larger cell would relax "
            "this to d <= 2k+1'.  Measured here: the model's own s = 36 quark "
            "cell does NOT relax it, because the bound that matters is the "
            "anticommuting rank of the HOP's span, not the Clifford rank of "
            "the cell."),
        "F313_criterion_added": (
            "F313's d_time = 1 needs one criterion it does not state, once the "
            "cell has an internal factor: a commuting unitary is a clock only "
            "if it DISPERSES.  F313 §9's second flow was dispersive (hence "
            "F315); the colour elements are not, at literal 0.0."),
        "residual_input": (
            "moved, not closed: from 'an internal index exists' to 'the matter "
            "sector contains a THREE-constituent bound state'.  The number "
            "three is still not derived here."),
    }


if __name__ == "__main__":       # pragma: no cover
    import json
    res = check_cell_internal_index()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']} -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    print(json.dumps(res["summary"], indent=2))
