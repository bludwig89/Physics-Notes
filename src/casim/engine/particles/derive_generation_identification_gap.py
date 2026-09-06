"""
casim.engine.particles.derive_generation_identification_gap
==============================================================

F342 -- Does F75's own defining criterion for a "generation multiplet"
(Sec.1, condition (i): "carry identical gauge quantum numbers") have any
power to SELECT the T_1u triplet -- specifically, as against any other
3-dimensional subspace of the same 8-site BCC nearest-neighbour shell,
including the T_2g triplet that F75 Step 3 excludes only by a *different*
argument (the parity of the chiral mass)?

Answer: no, under the charge structure this project's engine actually
implements, and that "no" is forced by one geometric fact about the shell --
its 8 vertices form a SINGLE orbit under the full O_h vacuum symmetry (the
action is transitive).  Any O_h-invariant charge operator that is diagonal
in the site basis (a per-site scalar assignment -- the minimal-coupling
ansatz `charge_coupling.py` / `minimal_coupling.py` actually implement, which
carry no site or shell index anywhere) is forced by transitivity to be a
multiple of the identity.  Condition (i) is then satisfied identically by
EVERY subspace of the shell, T_1u and T_2g alike, with the identical charge
value -- it supplies zero bits of selecting power beyond F75's own group
theory.

What WOULD select T_1u over T_2g is an operator that is O_h-invariant but
NOT diagonal in the site basis (an irrep-block-dependent coupling).  Such an
operator is exhibited here exactly, in Fraction arithmetic, built from
explicit linear embeddings of the shell into R^3 (T_1u: the vertex
coordinates themselves; T_2g: their pairwise products) that independently
reproduce F75 T2's A1g (+) A2u (+) T1u (+) T2g decomposition by a different
method (equivariant embedding, not character-table projection) -- a genuine
cross-check of F75 T2, not a re-use of it.  No coupling of that (non-diagonal)
kind exists anywhere in the adopted (non-fork) engine.
"""

from fractions import Fraction as Fr

# ---- O_h from generators (same generators F75's test uses) -----------------
R_z = ((0, -1, 0), (1, 0, 0), (0, 0, 1))
R_x = ((1, 0, 0), (0, 0, -1), (0, 1, 0))
INV = ((-1, 0, 0), (0, -1, 0), (0, 0, -1))
I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

VERTS = [(sx, sy, sz) for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)]


def _matmul3(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3))
                 for i in range(3))


def _close_group(gens):
    elems = {I3}
    frontier = [I3]
    while frontier:
        g = frontier.pop()
        for h in gens:
            for cand in (_matmul3(g, h), _matmul3(h, g)):
                if cand not in elems:
                    elems.add(cand)
                    frontier.append(cand)
    return elems


def _apply3(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(3)) for i in range(3))


def _perm_of(M, verts):
    idx = {v: i for i, v in enumerate(verts)}
    return tuple(idx[_apply3(M, v)] for v in verts)


def _perm_matrix(perm, n=8):
    P = [[Fr(0)] * n for _ in range(n)]
    for i, j in enumerate(perm):
        P[i][j] = Fr(1)
    return tuple(tuple(row) for row in P)


def _mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return tuple(tuple(sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m))
                 for i in range(n))


def _transpose(A):
    return tuple(zip(*A))


def _mat_sub(A, B):
    return tuple(tuple(A[i][j] - B[i][j] for j in range(len(A[0]))) for i in range(len(A)))


def _mat_add(A, B):
    return tuple(tuple(A[i][j] + B[i][j] for j in range(len(A[0]))) for i in range(len(A)))


def _scal(A, c):
    return tuple(tuple(c * x for x in row) for row in A)


def _identity(n):
    return tuple(tuple(Fr(1) if i == j else Fr(0) for j in range(n)) for i in range(n))


def _zero(n):
    return tuple(tuple(Fr(0) for _ in range(n)) for _ in range(n))


def _is_zero(A):
    return all(all(x == 0 for x in row) for row in A)


def _rank_via_gauss(A):
    M = [list(row) for row in A]
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pivval = M[r][c]
        M[r] = [x / pivval for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def _build_group_and_shell(symmetry_group):
    if symmetry_group == "full_Oh":
        gens = [R_z, R_x, INV]
    elif symmetry_group == "C4z_only":
        gens = [R_z]
    else:
        raise ValueError(symmetry_group)
    G = sorted(_close_group(gens))
    perms = [_perm_of(M, VERTS) for M in G]
    Pmats = [_perm_matrix(p) for p in perms]
    return G, perms, Pmats


def check_generation_identification_gap(
    charge_locality: str = "site_diagonal",
    symmetry_group: str = "full_Oh",
    charge_value: str = "7/3",
    block_charges=("1", "2", "3", "5"),
) -> dict:
    """F342.  See module docstring.  All arithmetic exact (Fraction)."""
    checks = {}
    ok_all = True

    def rec(name, ok, detail):
        nonlocal ok_all
        checks[name] = {"pass": bool(ok), **{k: str(v) for k, v in detail.items()}}
        ok_all = ok_all and ok

    # G1 -- the group itself (cross-check against F75 G1)
    Ofull = sorted(_close_group([R_z, R_x]))
    Ohfull = sorted(_close_group([R_z, R_x, INV]))
    rec("G1_group_orders", len(Ofull) == 24 and len(Ohfull) == 48,
        {"|O|": len(Ofull), "|O_h|": len(Ohfull)})

    G, perms, Pmats = _build_group_and_shell(symmetry_group)
    n = 8

    # G2 -- orbits of the (sub)group's action on the 8-vertex shell
    remaining = set(range(n))
    orbits = []
    while remaining:
        i = next(iter(remaining))
        orb = {i}
        frontier = [i]
        while frontier:
            k = frontier.pop()
            for p in perms:
                j = p[k]
                if j not in orb:
                    orb.add(j)
                    frontier.append(j)
        orbits.append(orb)
        remaining -= orb
    n_orbits = len(orbits)
    rec("G2_orbit_structure", True, {"symmetry_group": symmetry_group,
                                      "n_orbits": n_orbits, "orbit_sizes": sorted(len(o) for o in orbits)})

    # H1 -- diagonal O_h-invariant charge is forced constant  <=>  transitive
    #   (fixed claim: under full_Oh it IS forced constant; the C4z_only
    #    control has two orbits and must turn this red)
    rec("H1_diagonal_forced_constant", n_orbits == 1,
        {"symmetry_group": symmetry_group, "n_orbits": n_orbits})

    # H2 -- exact equivariant embeddings of T_1u, T_2g inside the shell rep
    M = tuple(tuple(Fr(c) for c in v) for v in VERTS)                          # T_1u embed (vertex coords)
    N = tuple((Fr(v[1] * v[2]), Fr(v[2] * v[0]), Fr(v[0] * v[1])) for v in VERTS)  # T_2g embed (pairwise products)
    Mt, Nt = _transpose(M), _transpose(N)
    MtM, NtN, MtN = _mat_mul(Mt, M), _mat_mul(Nt, N), _mat_mul(Mt, N)
    rec("H2a_MtM_is_8I3", MtM == _scal(_identity(3), Fr(8)), {})
    rec("H2b_NtN_is_8I3", NtN == _scal(_identity(3), Fr(8)), {})
    rec("H2c_MtN_is_zero", _is_zero(MtN), {})

    Pi_T1u = _scal(_mat_mul(M, Mt), Fr(1, 8))
    Pi_T2g = _scal(_mat_mul(N, Nt), Fr(1, 8))
    I8 = _identity(8)
    Pi_A1g = _scal(tuple(tuple(Fr(1) for _ in range(n)) for _ in range(n)), Fr(1, 8))
    Pi_A2u = _mat_sub(_mat_sub(_mat_sub(I8, Pi_A1g), Pi_T1u), Pi_T2g)

    ranks = {"A1g": _rank_via_gauss(Pi_A1g), "A2u": _rank_via_gauss(Pi_A2u),
             "T1u": _rank_via_gauss(Pi_T1u), "T2g": _rank_via_gauss(Pi_T2g)}
    rec("H2d_ranks_1_1_3_3", sorted(ranks.values()) == [1, 1, 3, 3],
        {**ranks, "note": "cross-checks F75 T2 by explicit equivariant embedding, "
                           "not character-table projection"})

    sum_proj = _mat_add(_mat_add(_mat_add(Pi_A1g, Pi_A2u), Pi_T1u), Pi_T2g)
    rec("H2e_partition_of_unity", sum_proj == I8, {})

    idem_ok = all(_mat_sub(_mat_mul(Pi, Pi), Pi) == _zero(n)
                  for Pi in (Pi_A1g, Pi_A2u, Pi_T1u, Pi_T2g))
    orth_ok = all(_is_zero(_mat_mul(Pi_i, Pi_j))
                  for idx_i, Pi_i in enumerate((Pi_A1g, Pi_A2u, Pi_T1u, Pi_T2g))
                  for idx_j, Pi_j in enumerate((Pi_A1g, Pi_A2u, Pi_T1u, Pi_T2g))
                  if idx_i != idx_j)
    rec("H2f_idempotent_and_orthogonal", idem_ok and orth_ok,
        {"idempotent": idem_ok, "mutually_orthogonal": orth_ok})

    commute_T1u = all(_is_zero(_mat_sub(_mat_mul(Pi_T1u, P), _mat_mul(P, Pi_T1u))) for P in Pmats)
    commute_T2g = all(_is_zero(_mat_sub(_mat_mul(Pi_T2g, P), _mat_mul(P, Pi_T2g))) for P in Pmats)
    rec("H2g_projectors_commute_with_group", commute_T1u and commute_T2g,
        {"T1u": commute_T1u, "T2g": commute_T2g, "symmetry_group": symmetry_group})

    # H3 -- fixed claim: condition (i) does NOT discriminate T_1u from T_2g,
    #   under the charge structure minimal coupling actually implements
    #   (charge_locality="site_diagonal").  The control (charge_locality=
    #   "block") uses a hypothetical non-diagonal, irrep-block-dependent
    #   charge instead, and turns this red -- demonstrating the claim is not
    #   vacuous, it tracks a real, checkable structural assumption.
    def _to_fr(x):
        if isinstance(x, Fr):
            return x
        if isinstance(x, int):
            return Fr(x)
        if isinstance(x, float):
            return Fr(x).limit_denominator(10**6)
        s = str(x)
        if "/" in s:
            p, r = s.split("/")
            return Fr(int(p), int(r))
        return Fr(int(s))

    q = _to_fr(charge_value)

    if charge_locality == "site_diagonal":
        Q = _scal(I8, q)
    elif charge_locality == "block":
        a, b, c_, d = (_to_fr(x) for x in block_charges)
        Q = _mat_add(_mat_add(_mat_add(_scal(Pi_A1g, a), _scal(Pi_A2u, b)),
                               _scal(Pi_T1u, c_)), _scal(Pi_T2g, d))
    else:
        raise ValueError(charge_locality)

    def _scalar_on_image(Q, Pi):
        QPi = _mat_mul(Q, Pi)
        lam = None
        for i in range(n):
            for j in range(n):
                if Pi[i][j] != 0:
                    lam = QPi[i][j] / Pi[i][j]
                    break
            if lam is not None:
                break
        ok = QPi == _scal(Pi, lam)
        return ok, lam

    T1u_scalar, lam_T1u = _scalar_on_image(Q, Pi_T1u)
    T2g_scalar, lam_T2g = _scalar_on_image(Q, Pi_T2g)

    rec("H3_condition_i_no_selecting_power",
        T1u_scalar and T2g_scalar and (lam_T1u == lam_T2g),
        {"charge_locality": charge_locality,
         "condition_i_holds_T1u": T1u_scalar, "condition_i_holds_T2g": T2g_scalar,
         "lambda_T1u": lam_T1u, "lambda_T2g": lam_T2g,
         "reads": ("site-diagonal: both triplets carry the SAME charge -- zero "
                   "selecting power" if charge_locality == "site_diagonal" else
                   "block (hypothetical, non-diagonal in the site basis): the two "
                   "triplets now carry DIFFERENT charges -- this is what selecting "
                   "power would require, and no coupling of this kind exists in the "
                   "adopted engine")})

    return {"pass": ok_all, "checks": checks,
            "params": {"charge_locality": charge_locality, "symmetry_group": symmetry_group,
                       "charge_value": str(q), "block_charges": list(block_charges)}}


if __name__ == "__main__":
    import json
    result = check_generation_identification_gap()
    print(json.dumps(result, indent=2, default=str))
    print("OVERALL:", "PASS" if result["pass"] else "FAIL")
