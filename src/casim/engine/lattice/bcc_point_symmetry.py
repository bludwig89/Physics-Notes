"""
bcc_point_symmetry.py — exact point-group covariance audit of the adopted
BCC free-Weyl walk (F344).
========================================================================

Object under test: the **adopted, BDPT-forced** single-step unitary of
`casim.engine.lattice.bcc._bcc_uvec` (Paper 1 Eq. 15),

    A^s(k) = u^s(k) I  -  i sigma . n^s(k),
    u^s    = alpha c_x c_y c_z + beta s_x s_y s_z          (module: alpha=1, beta=s)
    n^s_a  = p_a M1_a + q_a M2_a
    M1_a   = 's' in slot a, 'c' elsewhere      (the O(k)   / T_1u monomial)
    M2_a   = 'c' in slot a, 's' elsewhere      (the O(k^2) / T_2g monomial)
    c_i := cos(k_i/sqrt3), s_i := sin(k_i/sqrt3), s = +-1 the chirality branch.

The module's shipped convention is p = (+1, -s, +1), q = (-s, +1, +s).

Covariance criterion (BDPT Paper 1 Eq. 5 in momentum space):
    A(g k) = U(g) A(k) U(g)^dagger   <=>   n(g k) = R n(k),  R in O(3),
with the *branch label allowed to move*, since u^s(g k) = u^{tau_g(s)}(k).
R is not required to equal g: the SO(3) image of the spin lift is fixed only
up to a spin-frame change n -> S n, which conjugates R.  Existence of R is
therefore the frame-independent question, and it is the one answered here.

Everything except the final numeric leg is exact integer arithmetic on the
eight-dimensional monomial basis {c,s}^3 — no floats, no fitting.

Main results (see findings/F344-bcc-walk-point-symmetry-d4h.md):
  * unitarity forces every coefficient to be +-1 (rank-8 argument, C1);
  * u picks up the branch flip exactly when prod(eps_g) = -1, so 24 of the 48
    elements of O_h swap chirality — testing covariance at FIXED branch is the
    wrong test for half the group (C2);
  * for the shipped convention L = D_4h, |L| = 16 of 48, four-fold axis z (C3),
    with a unitarily-implementable subgroup D_2h of order 8 (C4);
  * NO admissible convention (all 576 unitary sign assignments) admits any of
    the eight body-diagonal C_3 rotations — unitarity and C_3 covariance of the
    T_2g sector are mutually exclusive (C5);
  * the defect has a closed form, n_x(C_3 k) - n_z(k) = (q_x - q_z) M2_z
    = -2s s_x s_y c_z, i.e. O(k^2) absolute / O(k) relative (C6);
  * the O(k) truncation is covariant under all 48 (C7), so O_h is an exact
    INFRARED symmetry of the walk and D_4h is its exact symmetry (C8).
"""

from __future__ import annotations

import json
import math
from itertools import permutations, product
from pathlib import Path

from casim.engine.lattice.bcc import _bcc_uvec

AX = (0, 1, 2)
C, S = 0, 1                      # monomial letters
MU1 = (C, C, C)                  # c_x c_y c_z
MU2 = (S, S, S)                  # s_x s_y s_z


def M1(a: int) -> tuple:
    """'s' in slot a, 'c' elsewhere — the O(k) (T_1u) monomial of n_a."""
    return tuple(S if i == a else C for i in AX)


def M2(a: int) -> tuple:
    """'c' in slot a, 's' elsewhere — the O(k^2) (T_2g) monomial of n_a."""
    return tuple(C if i == a else S for i in AX)


# ── coefficient conventions ────────────────────────────────────────────────
# A coefficient is a sign function of the branch label s in {+1,-1}; the four
# possibilities are exactly +1, -1, +s, -s.
COEF = {"+1": lambda s: 1, "-1": lambda s: -1, "+s": lambda s: s, "-s": lambda s: -s}

# The shipped convention, read off casim.engine.lattice.bcc._bcc_uvec:
#   nx =  s_x c_y c_z - s c_x s_y s_z      -> p_x=+1, q_x=-s
#   ny = -s c_x s_y c_z +   s_x c_y s_z    -> p_y=-s, q_y=+1
#   nz =  c_x c_y s_z + s s_x s_y c_z      -> p_z=+1, q_z=+s
MODULE_P = ("+1", "-s", "+1")
MODULE_Q = ("-s", "+1", "+s")

# Cyclic-symmetric q (used only as a negative control): C_3-covariant by
# construction, and therefore NOT unitary — that is the whole theorem.
CYCLIC_P = ("+1", "+1", "+1")
CYCLIC_Q = ("-s", "-s", "-s")


def _poly_walk(pn, qn, s, drop_M2=False):
    """u and n as integer monomial polynomials at branch s."""
    u = {MU1: 1, MU2: s}
    n = []
    for a in AX:
        d = {M1(a): COEF[pn[a]](s)}
        if not drop_M2:
            d[M2(a)] = COEF[qn[a]](s)
        n.append({m: v for m, v in d.items() if v != 0})
    return u, n


def is_unitary(pn, qn) -> bool:
    """u^2 + |n|^2 == 1 identically.  Given unit coefficients (C1) this is the
    single cross-term condition  alpha*beta + sum_a p_a q_a == 0,  i.e.
    sum_a p_a q_a == -s, checked on both branches."""
    return all(sum(COEF[pn[a]](s) * COEF[qn[a]](s) for a in AX) == -s
               for s in (1, -1))


# ── the point group ────────────────────────────────────────────────────────
# Same generators F342's module uses (derive_generation_identification_gap):
R_Z = ((0, -1, 0), (1, 0, 0), (0, 0, 1))
R_X = ((1, 0, 0), (0, 0, -1), (0, 1, 0))
INV = ((-1, 0, 0), (0, -1, 0), (0, 0, -1))
C3_111 = ((0, 0, 1), (1, 0, 0), (0, 1, 0))          # 120 deg about (1,1,1)
C4_X = ((1, 0, 0), (0, 0, -1), (0, 1, 0))


def _matmul3(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in AX) for j in AX) for i in AX)


def _close_group(gens):
    seen = {((1, 0, 0), (0, 1, 0), (0, 0, 1))}
    frontier = list(seen)
    while frontier:
        nxt = []
        for a in frontier:
            for g in gens:
                m = _matmul3(a, g)
                if m not in seen:
                    seen.add(m)
                    nxt.append(m)
        frontier = nxt
    return seen


def oh_group():
    """All 48 signed permutation matrices, verified equal to <R_z, R_x, INV>."""
    els = []
    for perm in permutations(AX):
        for eps in product((1, -1), repeat=3):
            g = [[0, 0, 0] for _ in AX]
            for i in AX:
                g[i][perm[i]] = eps[i]
            els.append(tuple(tuple(r) for r in g))
    return sorted(els)


def _gdata(g):
    """(j, eps) with (g k)_i = eps_i k_{j(i)}."""
    j, eps = [0, 0, 0], [0, 0, 0]
    for i in AX:
        for c in AX:
            if g[i][c]:
                j[i], eps[i] = c, g[i][c]
    return tuple(j), tuple(eps)


def _det3(g):
    return (g[0][0] * (g[1][1] * g[2][2] - g[1][2] * g[2][1])
            - g[0][1] * (g[1][0] * g[2][2] - g[1][2] * g[2][0])
            + g[0][2] * (g[1][0] * g[2][1] - g[1][1] * g[2][0]))


def _subst(poly, g):
    """f(g k), exactly, as a monomial polynomial."""
    j, eps = _gdata(g)
    out = {}
    for m, v in poly.items():
        new = [None, None, None]
        sgn = 1
        for i in AX:
            new[j[i]] = m[i]
            if m[i] == S:
                sgn *= eps[i]
        key = tuple(new)
        out[key] = out.get(key, 0) + sgn * v
        if out[key] == 0:
            del out[key]
    return out


def covariance_R(g, pn, qn, s, drop_M2=False):
    """Return (target_branch, R) with n^s(g k) = R n^{target}(k), R a signed
    permutation, or (target, None) if no such R exists."""
    u_s, n_s = _poly_walk(pn, qn, s, drop_M2)
    ug = _subst(u_s, g)
    tgt = None
    for st in (1, -1):
        if ug == _poly_walk(pn, qn, st, drop_M2)[0]:
            tgt = st
    if tgt is None:
        return None, None
    _, n_t = _poly_walk(pn, qn, tgt, drop_M2)
    j, _ = _gdata(g)
    R = [[0, 0, 0] for _ in AX]
    for a in AX:
        lhs, rhs = _subst(n_s[a], g), n_t[j[a]]
        rhos = set()
        for m in set(lhs) | set(rhs):
            lv, rv = lhs.get(m, 0), rhs.get(m, 0)
            if rv == 0 or lv % rv:
                return tgt, None
            rhos.add(lv // rv)
        if len(rhos) != 1:
            return tgt, None
        R[a][j[a]] = rhos.pop()
    return tgt, tuple(tuple(r) for r in R)


def covariance_group(pn, qn, s=1, drop_M2=False):
    """L = {g in O_h : some R exists}, with the R and target branch."""
    out = {}
    for g in oh_group():
        tgt, R = covariance_R(g, pn, qn, s, drop_M2)
        if R is not None:
            out[g] = (tgt, R)
    return out


# ── C1: unitarity forces unit coefficients ────────────────────────────────
def _unit_coefficient_rank():
    """The eight squared monomials, written in the multilinear basis of
    x_i := c_i^2 (so s_i^2 = 1 - x_i), are the eight products
    prod_i (x_i or 1-x_i) — the indicator basis.  Their rank over Q is 8, so
    sum_m lambda_m (monomial_m)^2 == 1 forces every lambda_m = 1, i.e. every
    coefficient of u and n has modulus 1.  Returned as an exact integer rank."""
    rows = []
    for m in product((C, S), repeat=3):
        # expand prod_i (x_i if c else 1-x_i) over subsets of {x_0,x_1,x_2}
        coef = {(): 1}
        for i in AX:
            new = {}
            for sub, cval in coef.items():
                if m[i] == C:                     # x_i
                    k = tuple(sorted(sub + (i,)))
                    new[k] = new.get(k, 0) + cval
                else:                             # 1 - x_i
                    new[sub] = new.get(sub, 0) + cval
                    k = tuple(sorted(sub + (i,)))
                    new[k] = new.get(k, 0) - cval
            coef = new
        subsets = [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
        rows.append([coef.get(t, 0) for t in subsets])
    # exact fraction-free Gaussian elimination
    import fractions
    M = [[fractions.Fraction(v) for v in r] for r in rows]
    rank, piv = 0, 0
    for col in range(8):
        sel = next((r for r in range(rank, 8) if M[r][col] != 0), None)
        if sel is None:
            continue
        M[rank], M[sel] = M[sel], M[rank]
        for r in range(8):
            if r != rank and M[r][col] != 0:
                f = M[r][col] / M[rank][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[rank])]
        rank += 1
    return rank


# ── the check ─────────────────────────────────────────────────────────────
def _fixed_k_sample(n=240):
    """Deterministic pseudo-random k sample, no RNG dependency."""
    out, x = [], 12345
    for _ in range(n):
        v = []
        for _ in AX:
            x = (1103515245 * x + 12345) % (1 << 31)
            v.append((x / (1 << 31)) * 2.0 - 1.0)
        out.append(tuple(v))
    return out


def _apply(g, k):
    return tuple(sum(g[i][j] * k[j] for j in AX) for i in AX)


def check_bcc_walk_point_symmetry(coefficient_source: str = "module",
                                  expansion_order: str = "exact") -> dict:
    """Every leg of F344.  Returns {"checks": {leg: bool}, ...} — the key the
    registry runner (`casim.tests.runner.leg_map`) reads to resolve control legs."""
    if coefficient_source == "module":
        pn, qn = MODULE_P, MODULE_Q
    elif coefficient_source == "cyclic":
        pn, qn = CYCLIC_P, CYCLIC_Q
    else:
        raise ValueError(f"unknown coefficient_source {coefficient_source!r}")
    drop = {"exact": False, "leading": True}[expansion_order]

    legs, detail = {}, {}

    # C0 — the convention under test is unitary
    legs["C0_convention_is_unitary"] = is_unitary(pn, qn)

    # C1 — unitarity forces |coefficient| = 1
    rank = _unit_coefficient_rank()
    detail["squared_monomial_rank"] = rank
    legs["C1_unitarity_forces_unit_coefficients"] = (rank == 8)

    # sanity: the enumerated 48 really are <R_z, R_x, INV>
    G = oh_group()
    legs["C1b_group_is_Oh_48"] = (set(G) == _close_group([R_Z, R_X, INV]) and len(G) == 48)

    # C2 — the branch map, exactly: tau_g(s) = s * prod(eps_g)
    bad, swap = 0, 0
    for g in G:
        _, eps = _gdata(g)
        pe = eps[0] * eps[1] * eps[2]
        if pe == -1:
            swap += 1
        for s in (1, -1):
            got = _subst(_poly_walk(pn, qn, s)[0], g)
            if got != _poly_walk(pn, qn, s * pe)[0]:
                bad += 1
    keepers = [g for g in G if math.prod(_gdata(g)[1]) == 1]
    detail["branch_swapping_elements"] = swap
    detail["branch_preserving_order"] = len(keepers)
    legs["C2_branch_map_exact"] = (bad == 0 and swap == 24 and len(keepers) == 24)
    # R_z (a PROPER rotation) is branch-swapping — the prior session's trap
    legs["C2b_proper_Rz_swaps_branch"] = (math.prod(_gdata(R_Z)[1]) == -1)

    # C3 — the covariance group of the shipped walk
    L = covariance_group(pn, qn, s=1, drop_M2=drop)
    Ls = set(L)
    closed = all(_matmul3(a, b) in Ls for a in Ls for b in Ls)
    axes = [a for a in AX if all(g[a][a] != 0 for g in Ls)]
    proper = sum(1 for g in Ls if _det3(g) == 1)
    detail["L_order"] = len(L)
    detail["L_closed"] = closed
    detail["L_invariant_axes"] = axes
    detail["L_proper_elements"] = proper
    legs["C3_L_is_D4h_order_16"] = (len(L) == 16 and closed and proper == 8 and len(axes) == 1)

    # C4 — unitarily implementable subgroup = ker(g -> det R), order 8 (D_2h)
    ker = [g for g, (_, R) in L.items() if _det3(R) == 1]
    kclosed = all(_matmul3(a, b) in set(ker) for a in ker for b in ker)
    detail["unitary_subgroup_order"] = len(ker)
    legs["C4_unitary_subgroup_order_8"] = (len(ker) == 8 and kclosed)

    # C5 — exhaustive sweep: no convention admits any body-diagonal C_3,
    #      and no convention exceeds |L| = 16.
    c3s = [g for g in G if _det3(g) == 1 and all(g[i][i] == 0 for i in AX)]
    n_conv, worst, with_c3 = 0, 0, 0
    for P in product(COEF, repeat=3):
        for Q in product(COEF, repeat=3):
            if not is_unitary(P, Q):
                continue
            n_conv += 1
            LL = covariance_group(P, Q, s=1, drop_M2=drop)
            worst = max(worst, len(LL))
            if any(g in LL for g in c3s):
                with_c3 += 1
    detail["admissible_conventions"] = n_conv
    detail["max_L_over_conventions"] = worst
    detail["conventions_admitting_a_C3"] = with_c3
    detail["n_body_diagonal_C3"] = len(c3s)
    legs["C5_no_C3_for_any_convention"] = (with_c3 == 0 and worst == 16 and n_conv == 576)

    # C6 — the defect has a closed form:  n_x(C_3 k) - n_z(k) = (q_x - q_z) M2_z
    okdef = True
    for s in (1, -1):
        _, n = _poly_walk(pn, qn, s)
        lhs = _subst(n[0], C3_111)
        rhs = dict(n[2])
        d = {m: lhs.get(m, 0) - rhs.get(m, 0) for m in set(lhs) | set(rhs)}
        d = {m: v for m, v in d.items() if v}
        want = COEF[qn[0]](s) - COEF[qn[2]](s)
        okdef &= (d == ({M2(2): want} if want else {}))
        detail[f"C3_defect_coefficient_branch_{'+' if s == 1 else '-'}"] = want
    legs["C6_defect_is_exactly_qx_minus_qz_times_T2g"] = okdef

    # C7 — the O(k) truncation is covariant under all 48 (O_h is exact in the IR)
    Llead = covariance_group(pn, qn, s=1, drop_M2=True)
    detail["L_order_leading"] = len(Llead)
    legs["C7_leading_order_covariant_under_all_48"] = (len(Llead) == 48)

    # C8 — machine-precision cross-check against the SHIPPED _bcc_uvec
    K = _fixed_k_sample()
    worst_in_L = 0.0
    for g, (tgt, R) in L.items():
        ts = "+" if tgt == 1 else "-"
        for k in K:
            a = _bcc_uvec(*_apply(g, k), sign="+")[1:]
            b = _bcc_uvec(*k, sign=ts)[1:]
            for i in AX:
                pred = sum(R[i][j] * float(b[j]) for j in AX)
                worst_in_L = max(worst_in_L, abs(float(a[i]) - pred))
    detail["max_residual_on_L_shipped_code"] = worst_in_L

    def _floor(gmat, scale):
        """min over all 48 signed permutations R and both target branches of the
        max relative residual — the obstruction, measured on the shipped code."""
        best = float("inf")
        Ks = [tuple(scale * c for c in k) for k in K[:60]]
        for ts in ("+", "-"):
            A = [_bcc_uvec(*_apply(gmat, k), sign="+")[1:] for k in Ks]
            B = [_bcc_uvec(*k, sign=ts)[1:] for k in Ks]
            norm = max(max(abs(float(x)) for x in row) for row in A)
            for R in G:
                m = 0.0
                for a_, b_ in zip(A, B):
                    for i in AX:
                        m = max(m, abs(float(a_[i]) - sum(R[i][j] * float(b_[j]) for j in AX)))
                best = min(best, m / norm)
        return best

    f1, f2 = _floor(C3_111, 0.1), _floor(C3_111, 0.01)
    detail["C3_residual_floor_k0.1"] = f1
    detail["C3_residual_floor_k0.01"] = f2
    detail["C3_residual_slope"] = f1 / f2 if f2 else float("inf")
    legs["C8_shipped_code_agrees"] = (
        worst_in_L < 1e-12 and f1 > 1e-3 and 8.0 < (f1 / f2) < 12.5)

    return {"checks": legs, "detail": detail,
            "params": {"coefficient_source": coefficient_source,
                       "expansion_order": expansion_order},
            "n_pass": sum(1 for v in legs.values() if v), "n_total": len(legs),
            "all_pass": all(legs.values())}


def _results_path(name: str) -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        cand = parent / "test-results"
        if cand.is_dir():
            return cand / name
    raise RuntimeError("test-results/ not found above " + str(here))


if __name__ == "__main__":                                   # pragma: no cover
    res = check_bcc_walk_point_symmetry()
    print(json.dumps(res, indent=2, default=str))
    p = _results_path("F344_bcc_walk_point_symmetry.json")
    p.write_text(json.dumps(res, indent=2, default=str) + "\n")
    print("wrote", p)
