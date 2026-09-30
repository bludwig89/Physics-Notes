"""
casim.engine.particles.derive_oh_residual_pmns
==============================================

F403 -- Can ANY residual symmetry drawn from the lattice point group O_h fix
lepton mixing (PMNS), given the model's charged-lepton frame?

Setting.  Generations are the T_1u triplet of O_h (F75); in T_1u the 48 group
elements are the signed 3x3 permutation matrices.  A Majorana (or Dirac)
neutrino mass term is a bilinear, so g and -g act identically on it: the
effective group is the rotation group O (24 elements, ~ S4).  The charged-
lepton frame is either

  cube_axes   -- the adopted E_g reading (F76/F93): the E_g condensate is
                 diagonal on the cube axes, so the charged-lepton eigenvectors
                 are e_x, e_y, e_z (in some order) and U_PMNS = U_nu;
  trimaximal  -- the alternative [111]-circulant reading of the SAME Koide
                 spectrum (research report 2026-09-24): charged-lepton
                 eigenvectors are the Z3 Fourier columns (1, w^k, w^2k)/sqrt3,
                 and U_PMNS = F^dagger U_nu.

Unitary residuals.  If R in O leaves the neutrino mass term invariant,
R^T M R = M, then H = M^dagger M commutes with R.  Light masses are
non-degenerate, so every eigenline of H is an eigenline of R: each 1-dim
eigenspace of R IS a PMNS column (up to phase).  The whole question is then
finite and exact: list the 1-dim eigenspaces of the 23 non-identity
rotations, map them through the charged-lepton frame, and compare the
resulting column moduli with data (all row assignments e/mu/tau, all column
labels 1/2/3).  A subgroup imposes at least the constraint of each of its
elements, so the element-wise verdict covers every residual subgroup -- and
legs S1-S3 check that by brute force: all 98 subgroups of O_h are built by
closure, and a subgroup admits a non-degenerate invariant mass matrix iff it is
an elementary abelian 2-group (49 of them).  Leg S4 is the BCC reading: same
O_h, same T_1u; the [111] nearest-neighbour directions are not orthogonal, so
the O_h-distinguished orthonormal frames are cube axes, face diagonals
(face_diagonal, also a no-go) and the C3[111] eigenbasis (= trimaximal).

Generalised-CP residuals (cube_axes frame only).  X in O_h with X X* = 1
(X real => X^2 = 1: the involutions) imposes U* = X U K.  For signed-
permutation X this forces |U_ai| = |U_pi(a) i|, and phase constraints
derived exactly below (J = 0 for diagonal X; mu-tau reflection for the
face-diagonal C2').

Exact parts: the group, eigenspaces, column moduli, invariant-matrix
degeneracies, and the gCP algebra are sympy-exact.  The comparison with data
is quantitative (NuFIT 6.0 NO 3-sigma ranges, arXiv:2410.05380; optionally
the JUNO-inclusive NuFIT 6.1 sin^2 theta12, arXiv:2601.09791, whose 3-sigma
band is a Gaussian extrapolation of the published 1-sigma errors and is
labelled as such).
"""

from __future__ import annotations

import itertools
import math

import sympy as sp

# ---- data (NuFIT 6.0, normal ordering, with SK atmospheric; 3-sigma) --------
# arXiv:2410.05380 Table (fetched 2026-09-24 via the research notes).
NUFIT60_3SIG = {
    "s12sq": (0.275, 0.345),
    "s23sq": (0.435, 0.585),
    "th13_deg": (8.19, 8.89),
    "delta_deg": (124.0, 364.0),
}
NUFIT60_TH13_BF_DEG = 8.56
# NuFIT 6.1 + JUNO first data: sin^2 th12 = 0.3096 +0.0057 / -0.0073 (1 sigma).
# The 3-sigma band below is a Gaussian 3x extrapolation, NOT a published range.
NUFIT61_S12SQ_3SIG_APPROX = (0.3096 - 3 * 0.0073, 0.3096 + 3 * 0.0057)

W = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2          # primitive cube root of 1


# ---- the group -------------------------------------------------------------

def _rotations():
    """The 24 proper rotations of the cube as sympy matrices (det +1 signed perms)."""
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = sp.zeros(3, 3)
            for i, j in enumerate(perm):
                M[i, j] = signs[i]
            if M.det() == 1:
                out.append(M)
    return out


def _full_oh():
    rots = _rotations()
    return rots + [-R for R in rots]


def _class_label(R):
    """Conjugacy-class label of a proper rotation from (trace, order)."""
    tr = R.trace()
    if R == sp.eye(3):
        return "E"
    if tr == 0:
        return "C3"
    if tr == 1:
        return "C4"
    # tr == -1: a C2; axis C2 are diagonal, face-diagonal C2' are not
    return "C2" if all(R[i, j] == 0 for i in range(3) for j in range(3) if i != j) else "C2'"


def _one_dim_eigenlines(R):
    """Normalised eigenvectors spanning the 1-dimensional eigenspaces of R."""
    lines = []
    for val, mult, vecs in R.eigenvects():
        if mult == 1 and len(vecs) == 1:
            v = vecs[0]
            n = sp.sqrt(sp.simplify(sum(sp.Abs(x) ** 2 for x in v)))
            lines.append((sp.nsimplify(val), sp.simplify(v / n)))
    return lines


def _frame(frame: str):
    if frame == "cube_axes":
        return sp.eye(3)
    if frame == "face_diagonal":
        # the C2' eigenbasis: (1,1,0)/sqrt2, (1,-1,0)/sqrt2, (0,0,1)
        return sp.Matrix([[1, 1, 0], [1, -1, 0], [0, 0, sp.sqrt(2)]]) / sp.sqrt(2)
    if frame == "trimaximal":
        return sp.Matrix(3, 3, lambda a, k: W ** (a * k)) / sp.sqrt(3)
    raise ValueError(f"unknown frame {frame!r}")


def _col_moduli(Uc, v):
    """|U_c^dagger v|^2 as exact rationals (the PMNS column's squared moduli)."""
    c = Uc.H * v
    return tuple(sp.nsimplify(sp.simplify(sp.expand(sp.Abs(x) ** 2))) for x in c)


# ---- data-side viability (quantitative) ------------------------------------

def _grid(lo, hi, n):
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]


def _cos_range(delta_deg):
    """[min, max] of cos(delta) over the delta window (degrees)."""
    lo, hi = delta_deg
    vals = [math.cos(math.radians(lo)), math.cos(math.radians(hi))]
    for k in range(-2, 4):                     # interior extrema at multiples of 180 deg
        x = 180.0 * k
        if lo <= x <= hi:
            vals.append(math.cos(math.radians(x)))
    return min(vals), max(vals)


def _column_viable(p, data, n=121, tol=1e-9):
    """Does SOME PMNS matrix inside the 3-sigma box have a column with squared
    moduli p (for SOME assignment of rows to e/mu/tau and SOME column label)?

    Standard parametrisation.  For fixed angles |U_mu1|^2 and |U_mu2|^2 are
    a^2 + b^2 -+ 2ab cos(delta); the reachable interval is read from the
    delta window (for NuFIT 6.0 NO, [124, 364] deg covers all of [-1, 1]).
    """
    cmin, cmax = _cos_range(data["delta_deg"])
    s12lo, s12hi = data["s12sq"]
    s23lo, s23hi = data["s23sq"]
    t13lo, t13hi = (math.radians(x) for x in data["th13_deg"])
    pf = [float(x) for x in p]
    for pe, pm, pt in set(itertools.permutations(pf)):
        # column 3: (s13^2, c13^2 s23^2, c13^2 c23^2)
        s13 = pe
        if math.sin(t13lo) ** 2 - tol <= s13 <= math.sin(t13hi) ** 2 + tol and s13 < 1:
            s23 = pm / (1 - s13)
            if s23lo - tol <= s23 <= s23hi + tol:
                return True
        # columns 1 and 2
        for t13 in _grid(t13lo, t13hi, 21):
            c13sq = math.cos(t13) ** 2
            s13 = math.sin(t13)
            for col in (1, 2):
                # col1: |U_e1|^2 = c12^2 c13^2 ; col2: |U_e2|^2 = s12^2 c13^2
                x = pe / c13sq
                if not (0 <= x <= 1):
                    continue
                s12sq = 1 - x if col == 1 else x
                if not (s12lo - tol <= s12sq <= s12hi + tol):
                    continue
                s12, c12 = math.sqrt(s12sq), math.sqrt(1 - s12sq)
                for s23sq in _grid(s23lo, s23hi, n):
                    s23, c23 = math.sqrt(s23sq), math.sqrt(1 - s23sq)
                    if col == 1:
                        a, b = s12 * c23, c12 * s23 * s13
                    else:
                        a, b = c12 * c23, s12 * s23 * s13
                    # col1: |U_mu1|^2 = a^2 + b^2 + 2ab cos d ; col2: a^2 + b^2 - 2ab cos d
                    sgn = 1.0 if col == 1 else -1.0
                    ends = (a * a + b * b + sgn * 2 * a * b * cmin, a * a + b * b + sgn * 2 * a * b * cmax)
                    if min(ends) - 1e-4 <= pm <= max(ends) + 1e-4:
                        return True
    return False


def _min_modulus_sq(data, n=41):
    """Smallest |U_ai|^2 anywhere in the 3-sigma box (grid scan)."""
    best = 1.0
    t13s = _grid(*(math.radians(x) for x in data["th13_deg"]), 9)
    ds = _grid(*(math.radians(x) for x in data["delta_deg"]), 25)
    for s12sq in _grid(*data["s12sq"], n):
        for s23sq in _grid(*data["s23sq"], n):
            for t13 in t13s:
                s12, c12 = math.sqrt(s12sq), math.sqrt(1 - s12sq)
                s23, c23 = math.sqrt(s23sq), math.sqrt(1 - s23sq)
                s13, c13 = math.sin(t13), math.cos(t13)
                for d in ds:
                    e = complex(math.cos(d), math.sin(d))
                    U = [[c12 * c13, s12 * c13, s13],
                         [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                         [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]]
                    best = min(best, min(abs(x) ** 2 for row in U for x in row))
    return best


def _full_matrix_viable(P, data):
    """All three columns fixed: P is the full |U|^2 matrix up to row/col perms."""
    for rp in itertools.permutations(range(3)):
        for cp in itertools.permutations(range(3)):
            Q = [[float(P[rp[a]][cp[i]]) for i in range(3)] for a in range(3)]
            s13 = Q[0][2]
            if s13 >= 1:
                continue
            s12 = Q[0][1] / (1 - s13)
            s23 = Q[1][2] / (1 - s13)
            t13 = math.degrees(math.asin(math.sqrt(s13)))
            if (data["th13_deg"][0] <= t13 <= data["th13_deg"][1]
                    and data["s12sq"][0] <= s12 <= data["s12sq"][1]
                    and data["s23sq"][0] <= s23 <= data["s23sq"][1]):
                return True
    return False


# ---- the full subgroup lattice (S legs) --------------------------------------

def _subgroups():
    """Every subgroup of O_h, as frozensets of indices into _full_oh().

    Closure from the cyclic subgroups upward; exact (integer matrices)."""
    G = _full_oh()
    idx = {tuple(g): i for i, g in enumerate(G)}
    mul = [[idx[tuple(a * b)] for b in G] for a in G]
    e = idx[tuple(sp.eye(3))]

    def close(gens):
        S = {e} | set(gens)
        frontier = list(S)
        while frontier:
            new = []
            for a in frontier:
                for b in list(S):
                    for c in (mul[a][b], mul[b][a]):
                        if c not in S:
                            S.add(c)
                            new.append(c)
            frontier = new
        return frozenset(S)

    subs = {close([g]) for g in range(len(G))}
    grown = True
    while grown:
        grown = False
        for H in list(subs):
            for g in range(len(G)):
                if g not in H:
                    K = close(list(H) + [g])
                    if K not in subs:
                        subs.add(K)
                        grown = True
    return G, idx, mul, e, subs


def _invariant_symmetric_group(G, H):
    """General symmetric M with g^T M g = M for every g in H (exact linear solve)."""
    syms = sp.symbols("m0:6")
    m = sp.Matrix([[syms[0], syms[1], syms[2]],
                   [syms[1], syms[3], syms[4]],
                   [syms[2], syms[4], syms[5]]])
    eqs = []
    for h in H:
        eqs += list(G[h].T * m * G[h] - m)
    sol = sp.solve(eqs, syms, dict=True)
    return m.subs(sol[0]) if sol else m


def _generic_nondegenerate(M):
    """True iff the characteristic-polynomial discriminant of the invariant
    family is not identically zero (i.e. a generic member has 3 distinct
    eigenvalues).  Exact."""
    x = sp.Symbol("x")
    return sp.simplify(sp.discriminant(M.charpoly(x).as_expr(), x)) != 0


def _joint_eigenlines(G, H):
    """1-dim joint eigenspaces of a group of real involutions (exact)."""
    spaces = [sp.eye(3)]
    for h in H:
        new = []
        for S in spaces:
            for val in (1, -1):
                ns = ((G[h] - val * sp.eye(3)) * S).nullspace()
                if ns:
                    new.append(sp.Matrix.hstack(*[S * n for n in ns]))
        spaces = new
    return [S / sp.sqrt((S.T * S)[0]) for S in spaces if S.shape[1] == 1]


def subgroup_table(frame: str = "cube_axes"):
    """For every subgroup H of O_h: order, proper?, elementary-abelian-2?,
    admits a non-degenerate invariant mass matrix?, forced PMNS columns."""
    G, idx, mul, e, subs = _subgroups()
    rot = {idx[tuple(R)] for R in _rotations()}
    neg = idx[tuple(-sp.eye(3))]
    Uc = _frame(frame)
    rows = []
    for H in subs:
        nondeg = _generic_nondegenerate(_invariant_symmetric_group(G, H))
        el2 = all(mul[h][h] == e for h in H)
        trivial = H <= {e, neg}                    # acts trivially on a bilinear
        cols = []
        if nondeg and el2 and not trivial:
            cols = [_col_moduli(Uc, v) for v in _joint_eigenlines(G, H)]
        rows.append({"H": H, "order": len(H), "proper": H <= rot, "el2": el2,
                     "nondeg": nondeg, "trivial": trivial, "columns": cols,
                     "all_fixed": len(cols) == 3})
    return rows


# ---- the analysis ------------------------------------------------------------

def residual_table(frame: str = "cube_axes"):
    """For each non-identity rotation: its class, its fixed PMNS columns (exact
    squared moduli), whether it fixes all three columns."""
    Uc = _frame(frame)
    rows = []
    for R in _rotations():
        if R == sp.eye(3):
            continue
        lines = _one_dim_eigenlines(R)
        cols = [_col_moduli(Uc, v) for _, v in lines]
        rows.append({"R": R, "class": _class_label(R), "columns": cols,
                     "all_fixed": len(lines) == 3})
    return rows


def _verdict(row, data):
    if row["all_fixed"]:
        P = [[row["columns"][i][a] for i in range(3)] for a in range(3)]
        return _full_matrix_viable(P, data)
    return all(_column_viable(c, data) for c in row["columns"])


def _invariant_symmetric(R):
    """General complex symmetric M with R^T M R = M (exact linear solve)."""
    syms = sp.symbols("m0:6")
    m = sp.Matrix([[syms[0], syms[1], syms[2]],
                   [syms[1], syms[3], syms[4]],
                   [syms[2], syms[4], syms[5]]])
    sol = sp.solve(list(R.T * m * R - m), syms, dict=True)
    return m.subs(sol[0]) if sol else m


def check_oh_residual_pmns(frame: str = "cube_axes",
                           theta13_lo_deg: float = 8.19,
                           s12sq_band: str = "nufit60") -> dict:
    """F403.  See module docstring.

    frame          -- charged-lepton frame for the no-go legs (N1, S2):
                      cube_axes | face_diagonal | trimaximal
    theta13_lo_deg -- lower 3-sigma edge used for theta13 (data input)
    s12sq_band     -- 'nufit60' (published 3 sigma) or 'nufit61_juno_approx'
    """
    checks = {}
    ok_all = True

    def rec(name, ok, detail=None):
        nonlocal ok_all
        checks[name] = {"pass": bool(ok), **{k: str(v) for k, v in (detail or {}).items()}}
        ok_all = ok_all and bool(ok)

    data = dict(NUFIT60_3SIG)
    data["th13_deg"] = (float(theta13_lo_deg), NUFIT60_3SIG["th13_deg"][1])
    if s12sq_band == "nufit61_juno_approx":
        data["s12sq"] = NUFIT61_S12SQ_3SIG_APPROX

    # G1 -- the group: 48 signed perms, 24 rotations, class sizes 1+3+6+8+6
    Oh = _full_oh()
    rots = _rotations()
    classes = {}
    for R in rots:
        classes[_class_label(R)] = classes.get(_class_label(R), 0) + 1
    rec("G1_group_and_classes",
        len({tuple(g) for g in Oh}) == 48 and len(rots) == 24
        and classes == {"E": 1, "C2": 3, "C2'": 6, "C3": 8, "C4": 6},
        {"|O_h|": len(Oh), "|O|": len(rots), "classes": classes})

    # G2 -- -g acts like g on any bilinear: (-g)^T M (-g) = g^T M g  (exact)
    m = sp.Matrix(3, 3, sp.symbols("a0:9"))
    rec("G2_sign_blind_on_bilinear",
        all(sp.simplify((-g).T * m * (-g) - g.T * m * g) == sp.zeros(3, 3) for g in rots[:4]))

    # E1 -- exact eigen-structure in the cube-axes frame, by class
    cube = residual_table("cube_axes")
    by_class = {}
    for r in cube:
        by_class.setdefault(r["class"], []).append(r)

    def has_zero(col):
        return any(x == 0 for x in col)

    e1 = (all(len(r["columns"]) == 1 and has_zero(r["columns"][0]) for r in by_class["C2"])
          and all(len(r["columns"]) == 1 and has_zero(r["columns"][0]) for r in by_class["C2'"])
          and all(r["all_fixed"] and all(x == sp.Rational(1, 3) for c in r["columns"] for x in c)
                  for r in by_class["C3"])
          and all(r["all_fixed"] and all(has_zero(c) for c in r["columns"]) for r in by_class["C4"]))
    rec("E1_cube_frame_fixed_columns_exact", e1,
        {"C2": sorted({r["columns"][0] for r in by_class["C2"]}),
         "C2'": sorted({r["columns"][0] for r in by_class["C2'"]}),
         "C3": "all |U|^2 = 1/3 (trimaximal)",
         "C4": sorted({c for r in by_class["C4"] for c in r["columns"]})})

    # E2 -- Majorana bonus: C3 / C4 invariant symmetric M has a degenerate pair
    Rc3 = by_class["C3"][0]["R"]
    Rc4 = by_class["C4"][0]["R"]
    deg = True
    for R in (Rc3, Rc4):
        Minv = _invariant_symmetric(R)
        ev = list(Minv.eigenvals(multiple=True))
        deg = deg and any(sp.simplify(ev[i] - ev[j]) == 0
                          for i in range(3) for j in range(i + 1, 3))
    rec("E2_majorana_C3_C4_force_degenerate_pair", deg)

    # N1 -- THE NO-GO: in `frame`, no non-identity unitary O residual is viable
    tab = cube if frame == "cube_axes" else residual_table(frame)
    viable = [(r["class"], r["columns"]) for r in tab if _verdict(r, data)]
    rec("N1_no_viable_unitary_residual", len(viable) == 0,
        {"frame": frame, "theta13_lo_deg": theta13_lo_deg, "viable": viable})

    # N2 -- the no-go rests on theta13 != 0: min |U|^2 over the box is s13^2 > 0
    #      (grid scan over the whole box, not just the theta13 edge)
    minmod = _min_modulus_sq(data)
    rec("N2_minimum_modulus_positive", minmod > 1e-3,
        {"min_abs_U_sq_in_box": round(minmod, 5),
         "s13sq_lower_edge": round(math.sin(math.radians(data["th13_deg"][0])) ** 2, 5)})

    # B1 -- picture (b): trimaximal frame.  Exact column moduli per class
    tri = residual_table("trimaximal")
    tm1 = (sp.Rational(2, 3), sp.Rational(1, 6), sp.Rational(1, 6))
    tm2 = (sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(1, 3))
    c2p_cols = sorted(tuple(sorted(r["columns"][0])) for r in tri if r["class"] == "C2'")
    c2_cols = [tuple(sorted(r["columns"][0])) for r in tri if r["class"] == "C2"]
    rec("B1_trimaximal_frame_C2prime_gives_TM1_exact",
        c2p_cols.count(tuple(sorted(tm1))) == 3
        and c2p_cols.count((0, sp.Rational(1, 2), sp.Rational(1, 2))) == 3
        and all(c == tm2 for c in c2_cols),
        {"C2'": c2p_cols, "C2": c2_cols})

    # B2 -- which trimaximal-frame residuals survive the data (quantitative)
    viable_tri = {}
    for r in tri:
        viable_tri.setdefault(r["class"], []).append(_verdict(r, data))
    surv = {k: sum(v) for k, v in viable_tri.items()}
    rec("B2_trimaximal_frame_TM1_viable", surv.get("C2'", 0) == 3
        and surv.get("C3", 0) == 0 and surv.get("C4", 0) == 0,
        {"survivors_by_class": surv, "s12sq_band": s12sq_band})

    # B3 -- TM1 sum rule: s12^2 = 1 - 2/(3 c13^2), and its value on the theta13 band
    th = sp.symbols("theta13", positive=True)
    s12_tm1 = 1 - sp.Rational(2, 3) / sp.cos(th) ** 2
    ends = [float(s12_tm1.subs(th, sp.rad(sp.nsimplify(x)))) for x in data["th13_deg"]]
    lo, hi = min(ends), max(ends)
    tm2_val = float((sp.Rational(1, 3) / sp.cos(th) ** 2).subs(th, sp.rad(sp.nsimplify(NUFIT60_TH13_BF_DEG))))
    rec("B3_TM1_s12sq_prediction", data["s12sq"][0] <= lo and hi <= data["s12sq"][1],
        {"TM1_s12sq_range": (round(lo, 5), round(hi, 5)), "TM2_s12sq_at_bf": round(tm2_val, 5),
         "s12sq_band": data["s12sq"]})

    # B4 -- TM1's (theta23, delta) correlation.  With column 1 = (2/3,1/6,1/6),
    #   |U_mu1|^2 = 1/6 gives (PDG parametrisation)
    #   cos d = -(s12^2 - c12^2 s13^2) cos 2t23 / (2 s12 c12 s13 sin 2t23),
    #   s12^2 fixed by the sum rule.  Verified symbolically, then scanned.
    t12s, t13s_, t23s, ds_ = sp.symbols("t12 t13 t23 d", real=True)
    cd_sym = sp.symbols("cd", real=True)
    ee = sp.exp(sp.I * ds_)
    Um1 = -sp.sin(t12s) * sp.cos(t23s) - sp.cos(t12s) * sp.sin(t23s) * sp.sin(t13s_) * ee
    Ut1 = sp.sin(t12s) * sp.sin(t23s) - sp.cos(t12s) * sp.cos(t23s) * sp.sin(t13s_) * ee
    gap = sp.trigsimp(sp.expand_complex(Um1 * sp.conjugate(Um1) - Ut1 * sp.conjugate(Ut1)))
    # |U_mu1| = |U_tau1| is linear in cos d: solve it and compare with the closed form
    cd_solved = sp.solve(gap.subs(sp.cos(ds_), cd_sym), cd_sym)
    cosd_expr = -(sp.sin(t12s) ** 2 - sp.cos(t12s) ** 2 * sp.sin(t13s_) ** 2) * sp.cos(2 * t23s) / (
        2 * sp.sin(t12s) * sp.cos(t12s) * sp.sin(t13s_) * sp.sin(2 * t23s))
    b4_identity = len(cd_solved) == 1 and sp.simplify(sp.expand_trig(cd_solved[0] - cosd_expr)) == 0
    dmin, dmax = 400.0, -400.0
    for t13 in _grid(*(math.radians(x) for x in data["th13_deg"]), 15):
        s12sq = 1 - 2 / (3 * math.cos(t13) ** 2)
        s12, c12, s13 = math.sqrt(s12sq), math.sqrt(1 - s12sq), math.sin(t13)
        if s13 < 1e-9 or s12sq <= 0:
            continue                               # theta13 = 0: delta undefined
        for s23sq in _grid(*data["s23sq"], 121):
            t23 = math.asin(math.sqrt(s23sq))
            cd = -(s12sq - c12 ** 2 * s13 ** 2) * math.cos(2 * t23) / (
                2 * s12 * c12 * s13 * math.sin(2 * t23))
            if abs(cd) > 1:
                continue
            for dd in (math.degrees(math.acos(cd)), 360 - math.degrees(math.acos(cd))):
                if data["delta_deg"][0] <= dd <= data["delta_deg"][1]:
                    dmin, dmax = min(dmin, dd), max(dmax, dd)
    rec("B4_TM1_delta_correlation", b4_identity and dmin < dmax and dmin > 180,
        {"TM1_delta_deg_range": (round(dmin, 1), round(dmax, 1)), "cos_delta_closed_form": b4_identity})

    # S1 -- the whole subgroup lattice, exact.  O_h has 98 subgroups (O: 30).
    #   A subgroup admits an invariant mass matrix with non-degenerate spectrum
    #   iff it is an elementary abelian 2-group (all h^2 = 1): 49 of them, of
    #   order 1, 2, 4, 8.  Every forced column of such a subgroup is already a
    #   1-dim eigenline of one of its elements, so the element-wise legs cover it.
    sub_cube = subgroup_table("cube_axes")
    el_cols = {c for r in cube for c in r["columns"]}
    admissible = [r for r in sub_cube if r["nondeg"]]
    covered = all(c in el_cols for r in admissible for c in r["columns"])
    rec("S1_subgroup_lattice_admissible_iff_el2_exact",
        len(sub_cube) == 98 and sum(r["proper"] for r in sub_cube) == 30
        and all(r["nondeg"] == r["el2"] for r in sub_cube)
        and len(admissible) == 49
        and max(r["order"] for r in admissible) == 8
        and all(r["columns"] for r in admissible if not r["trivial"]) and covered,
        {"n_subgroups_Oh": len(sub_cube), "n_subgroups_O": sum(r["proper"] for r in sub_cube),
         "n_admissible": len(admissible),
         "admissible_orders": sorted({r["order"] for r in admissible}),
         "forced_columns_covered_by_elements": covered})

    # S2 -- THE NO-GO over subgroups: in `frame`, no non-trivial admissible
    #   residual subgroup of O_h fixes a viable PMNS column set
    sub_tab = sub_cube if frame == "cube_axes" else subgroup_table(frame)
    nontriv = [r for r in sub_tab if r["nondeg"] and not r["trivial"]]
    viable_sub = [(r["order"], r["columns"]) for r in nontriv if _verdict(r, data)]
    rec("S2_no_viable_residual_subgroup", len(viable_sub) == 0,
        {"frame": frame, "n_nontrivial_admissible": len(nontriv), "viable": viable_sub})

    # S3 -- trimaximal frame, over subgroups: survivors fix exactly ONE column,
    #   TM1 (2/3,1/6,1/6) or TM2 (1/3,1/3,1/3); no three-column (Z2 x Z2)
    #   residual survives in either frame
    sub_tri = sub_tab if frame == "trimaximal" else subgroup_table("trimaximal")
    surv_tri = [r for r in sub_tri if r["nondeg"] and not r["trivial"] and _verdict(r, data)]
    surv_cols = {tuple(sorted(r["columns"][0])) for r in surv_tri if len(r["columns"]) == 1}
    full_dead = not any(r["all_fixed"] and _verdict(r, data)
                        for r in sub_cube + sub_tri if r["nondeg"] and not r["trivial"])
    rec("S3_trimaximal_subgroup_survivors_single_column",
        bool(surv_tri) and all(len(r["columns"]) == 1 for r in surv_tri)
        and surv_cols == {tuple(sorted(tm1)), tm2} and full_dead,
        {"n_survivors": len(surv_tri), "survivor_orders": sorted(r["order"] for r in surv_tri),
         "survivor_columns": sorted(surv_cols), "no_three_column_residual": full_dead})

    # S4 -- the BCC reading.  The BCC point group is O_h and generations are
    #   the same T_1u, so S1 holds verbatim; only the charged-lepton frame can
    #   change.  The 4 nearest-neighbour [111] directions are not mutually
    #   orthogonal (Gram off-diagonal -1/3), so no real orthonormal "[111]
    #   frame" exists; the O_h-distinguished orthonormal frames are the cube
    #   axes (C4 eigenbasis), the face diagonals (C2' eigenbasis) and the
    #   complex C3[111] eigenbasis (= trimaximal).  The face-diagonal frame
    #   is a no-go too; only the trimaximal one opens.
    bd = [sp.Matrix([1, 1, 1]), sp.Matrix([1, -1, -1]), sp.Matrix([-1, 1, -1]),
          sp.Matrix([-1, -1, 1])]
    gram = {(bd[i].T * bd[j])[0] / 3 for i in range(4) for j in range(i + 1, 4)}
    sub_face = subgroup_table("face_diagonal")
    viable_face = [(r["order"], r["columns"]) for r in sub_face
                   if r["nondeg"] and not r["trivial"] and _verdict(r, data)]
    rec("S4_bcc_nn_frame_nonorthogonal_face_frame_no_go",
        gram == {sp.Rational(-1, 3)} and len(viable_face) == 0,
        {"bcc_111_gram_offdiag": sorted(gram), "face_diagonal_viable": viable_face})

    # C1 -- gCP (cube frame): involutive X in O (mod sign) and their constraints
    #   diagonal X: U* = X U K  =>  the rephasing invariant Q = U_e1 U_m2 U_e2* U_m1*
    #   satisfies Q* = Q  => J = 0.   Exact with symbolic phases.
    # Treat U entries and their conjugates as independent symbols u, cu and
    # impose cu_ai = s_a u_ai k_i (s_a = +-1 the diagonal X, |k_i| = 1).
    u = sp.Matrix(3, 3, sp.symbols("u0:9"))
    cu = sp.Matrix(3, 3, sp.symbols("cu0:9"))
    s = sp.symbols("s0:3")
    k = sp.symbols("k0:3")
    Q = u[0, 0] * u[1, 1] * cu[0, 1] * cu[1, 0]
    Qstar = cu[0, 0] * cu[1, 1] * u[0, 1] * u[1, 0]
    imp = {cu[a, i]: s[a] * u[a, i] * k[i] for a in range(3) for i in range(3)}
    j_zero = sp.expand((Qstar.subs(imp) - Q.subs(imp)).subs({s[0] ** 2: 1, s[1] ** 2: 1})) == 0
    # mu-tau (y<->z) reflection: |U_m3| = |U_t3| forces s23 = c23 (column 3),
    # and then |U_m1|^2 - |U_t1|^2 = sin(2 t12) sin(t13) cos(delta): delta = +-pi/2.
    t12, t13, t23, d = sp.symbols("t12 t13 t23 delta", real=True)
    c12, s12_, c13, s13_ = sp.cos(t12), sp.sin(t12), sp.cos(t13), sp.sin(t13)
    c23, s23_ = sp.cos(t23), sp.sin(t23)
    e = sp.exp(sp.I * d)
    Um1 = -s12_ * c23 - c12 * s23_ * s13_ * e
    Ut1 = s12_ * s23_ - c12 * c23 * s13_ * e
    dm = sp.simplify(sp.expand_complex(
        (Um1 * sp.conjugate(Um1) - Ut1 * sp.conjugate(Ut1)).subs(t23, sp.pi / 4)))
    mutau_ok = sp.simplify(dm - sp.sin(2 * t12) * s13_ * sp.cos(d)) == 0
    col3_sols = sp.solve(sp.Eq(sp.sin(t23) ** 2, sp.cos(t23) ** 2), t23)
    col3_ok = any(sp.simplify(x - sp.pi / 4) == 0 for x in col3_sols)
    # data: mu-tau reflection needs s23^2 = 1/2 and delta = 270 deg in the box
    mutau_data = (data["s23sq"][0] <= 0.5 <= data["s23sq"][1]
                  and data["delta_deg"][0] <= 270 <= data["delta_deg"][1])
    # e<->mu / e<->tau reflections force |U_e3| = |U_mu3| or |U_tau3|:
    # max |U_e3|^2 = s13^2(hi) vs min c13^2 * min(s23^2, c23^2) over the box
    s13hi = math.sin(math.radians(data["th13_deg"][1])) ** 2
    min_mt3 = (1 - s13hi) * min(data["s23sq"][0], 1 - data["s23sq"][1])
    e_swap_excluded = s13hi < min_mt3
    rec("C1_gCP_diag_gives_J0_and_mutau_reflection", bool(j_zero) and bool(mutau_ok) and col3_ok
        and mutau_data and e_swap_excluded,
        {"J0_diag": j_zero, "mutau_dm_at_pi4": dm, "mutau_in_box": mutau_data,
         "max_Ue3sq": round(s13hi, 5), "min_Umu3_or_Utau3_sq": round(min_mt3, 5),
         "note": "e<->mu or e<->tau reflections need |U_e3|=|U_mu3| or |U_tau3|: excluded"})

    return {"pass": ok_all, "checks": checks, "frame": frame, "data": data}


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path
    res = check_oh_residual_pmns()
    for name, c in res["checks"].items():
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {name}")
    with open(results_path("F403_oh_residual_pmns.json"), "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("OVERALL", "PASS" if res["pass"] else "FAIL")
