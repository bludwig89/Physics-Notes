"""
F141 — BCC Wigner-Seitz cell face counting and the on-shell 7:9 mass ratio.

Three exact blocks + one PDG comparison:

  V1  (exact, integer)    The Voronoi-relevant vectors of the BCC lattice are
                          exactly the 14 = 8 NN + 6 NNN vectors. All longer
                          vectors are irrelevant (integer check to |v|^2 <= 24,
                          closed by the covering-radius bound |v| <= 2*mu with
                          mu^2 = 5/4 from V2).
  V2  (exact, rational)   The WS cell is the truncated octahedron: 24 vertices,
                          14 facets = 8 hexagons (perp. NN body diagonals) +
                          6 squares (perp. NNN face axes); 7 facet-normal axes
                          mod inversion.  Circumradius^2 = 5/4 exactly.
  V3  (exact, rational)   Equal stiffness u per structural channel
                          (7 bond-axis + 2 sublattice) gives
                          g^2 : g'^2 = 7 : 2,  m_W^2 : m_Z^2 = 7 : 9,
                          m_Z/m_W = 3/sqrt(7), on-shell sin^2(theta_W) = 2/9,
                          and the F138 bridge (2/9)/(1/4) = 8/9.
  V4  (numeric)           PDG masses: m_Z/m_W vs 3/sqrt(7) and
                          1 - (m_W/m_Z)^2 vs 2/9.

BCC lattice realised as L = {x in Z^3 : x = (0,0,0) or (1,1,1) mod 2}
(conventional cube edge 2; NN = (+-1,+-1,+-1), |v|^2 = 3; NNN = (+-2,0,0)
permutations, |v|^2 = 4; third shell |v|^2 = 8).

Runtime < 5 s, stdlib only (fractions, itertools, json, math).
"""

import json
import math
import os
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.normpath(
    os.path.join(HERE, "..", "..", "test-results", "F141_ws_cell_mass_counting.json")
)

results = {"finding": "F141", "checks": {}}
failures = []


def check(name, ok, detail):
    results["checks"][name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures.append(name)


# ----------------------------------------------------------------------
# Lattice enumeration (exact integers)
# ----------------------------------------------------------------------
def bcc_points(rmax2, span):
    """All BCC lattice vectors v != 0 with |v|^2 <= rmax2."""
    pts = []
    for x in product(range(-span, span + 1), repeat=3):
        if x == (0, 0, 0):
            continue
        par = {xi % 2 for xi in x}
        if len(par) > 1:
            continue  # mixed parity: not in BCC
        n2 = sum(xi * xi for xi in x)
        if n2 <= rmax2:
            pts.append(x)
    return pts


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


# ----------------------------------------------------------------------
# V1 — Voronoi relevance, exact over Z
# ----------------------------------------------------------------------
# v is Voronoi-relevant  <=>  for all lattice w not in {0, v}:
#     |w - v/2|^2 > |v/2|^2   <=>   |w|^2 > w.v        (all-integer)
# Any violator w satisfies |w|^2 <= w.v <= |w||v|, hence |w| <= |v|,
# so it is enough to test w with |w|^2 <= |v|^2.
RMAX2 = 24
candidates = bcc_points(RMAX2, span=5)

relevant, ties = [], []
for v in candidates:
    v2 = dot(v, v)
    is_rel, has_tie = True, False
    for w in candidates:
        if w == v or dot(w, w) > v2:
            continue
        lhs, rhs = dot(w, w), dot(w, v)
        if lhs < rhs:
            is_rel = False
            break
        if lhs == rhs:
            has_tie = True  # degenerate contact, not a facet violator per se
    if is_rel:
        relevant.append(v)
        if has_tie:
            ties.append(v)

nn = sorted(v for v in relevant if dot(v, v) == 3)
nnn = sorted(v for v in relevant if dot(v, v) == 4)
other = [v for v in relevant if dot(v, v) not in (3, 4)]

check(
    "V1a_relevant_count",
    len(relevant) == 14 and len(nn) == 8 and len(nnn) == 6 and not other,
    f"relevant={len(relevant)} (NN={len(nn)}, NNN={len(nnn)}, other={len(other)}) "
    f"over window |v|^2<={RMAX2}",
)
check(
    "V1b_no_ties_on_facets",
    not ties,
    f"degenerate equidistance ties among relevant vectors: {ties}",
)

axes = sorted({tuple(-c for c in v) if (v[0], v[1], v[2]) < (0, 0, 0) or v < tuple(-c for c in v) else v
               for v in relevant})
# simpler canonicalisation: identify v with -v by lexicographic max
axes = sorted({max(v, tuple(-c for c in v)) for v in relevant})
check(
    "V1c_axes_mod_inversion",
    len(axes) == 7,
    f"unique facet axes mod inversion = {len(axes)} (expected 7 = 4 body-diagonal + 3 face)",
)

# ----------------------------------------------------------------------
# V2 — exact facet/vertex structure of the WS cell (rational arithmetic)
# ----------------------------------------------------------------------
# Cell = {x : x.v <= |v|^2/2 for the 14 relevant v}.  Vertices = solutions of
# 3 active bisector planes that satisfy all 14 inequalities.  Solve exactly
# with Fractions via Cramer's rule.
def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def solve3(A, b):
    D = det3(A)
    if D == 0:
        return None
    cols = []
    for j in range(3):
        M = [[A[i][k] if k != j else b[i] for k in range(3)] for i in range(3)]
        cols.append(Fraction(det3(M), D))
    return tuple(cols)


planes = [(v, Fraction(dot(v, v), 2)) for v in relevant]
verts = set()
for (p1, p2, p3) in combinations(planes, 3):
    A = [list(p1[0]), list(p2[0]), list(p3[0])]
    b = [p1[1], p2[1], p3[1]]
    x = solve3(A, b)
    if x is None:
        continue
    if all(sum(Fraction(vi) * xi for vi, xi in zip(v, x)) <= rhs for v, rhs in planes):
        verts.add(x)

verts = sorted(verts)
circum2 = max(sum(c * c for c in x) for x in verts) if verts else None
check(
    "V2a_vertices",
    len(verts) == 24 and circum2 == Fraction(5, 4),
    f"vertices={len(verts)} (expected 24), circumradius^2={circum2} (expected 5/4)",
)

facet_sizes = {}
for v, rhs in planes:
    on = [x for x in verts if sum(Fraction(vi) * xi for vi, xi in zip(v, x)) == rhs]
    facet_sizes[v] = len(on)

hexes = [v for v, n in facet_sizes.items() if n == 6]
squares = [v for v, n in facet_sizes.items() if n == 4]
hex_ok = len(hexes) == 8 and all(dot(v, v) == 3 for v in hexes)
sq_ok = len(squares) == 6 and all(dot(v, v) == 4 for v in squares)
check(
    "V2b_facet_classification",
    hex_ok and sq_ok and len(hexes) + len(squares) == 14,
    f"hexagonal facets={len(hexes)} (all perp NN: {all(dot(v,v)==3 for v in hexes)}), "
    f"square facets={len(squares)} (all perp NNN: {all(dot(v,v)==4 for v in squares)})",
)

# Covering-radius closure of V1: every relevant v has v/2 in the cell, so
# |v|^2 <= 4*circum2 = 5.  BCC shells: |v|^2 = 3, 4, 8, ... => the window
# |v|^2 <= 24 was already far more than sufficient; nothing beyond |v|^2 = 5
# can ever be relevant.
check(
    "V2c_covering_radius_closure",
    circum2 is not None and 4 * circum2 == 5 and all(dot(v, v) <= 5 for v in relevant),
    f"relevance bound |v|^2 <= 4*mu^2 = {4*circum2}; next BCC shell |v|^2=8 > 5 — "
    f"V1 window is rigorously closed",
)

# ----------------------------------------------------------------------
# V3 — exact rational algebra of equal-stiffness channel counting
# ----------------------------------------------------------------------
n_axes, n_sub = 7, 2  # from V1/V2 and F51
g2, gp2 = Fraction(n_axes), Fraction(n_sub)  # in units of the common quantum u

s2_onshell = gp2 / (g2 + gp2)
mw2_over_mz2 = g2 / (g2 + gp2)
bridge = s2_onshell / Fraction(1, 4)

check(
    "V3a_sin2_2over9",
    s2_onshell == Fraction(2, 9) and mw2_over_mz2 == Fraction(7, 9),
    f"sin^2(theta_W)_os = {s2_onshell}, m_W^2/m_Z^2 = {mw2_over_mz2}",
)
check(
    "V3b_mass_ratio_identity",
    Fraction(9, 7) == (g2 + gp2) / g2,  # (m_Z/m_W)^2 = 9/7 <=> m_Z/m_W = 3/sqrt7
    f"(m_Z/m_W)^2 = {(g2+gp2)/g2} = 9/7  <=>  m_Z/m_W = 3/sqrt(7)",
)
check(
    "V3c_f138_bridge",
    bridge == Fraction(8, 9),
    f"(2/9)/(1/4) = {bridge} — the F138 UV-cap -> on-shell correction factor, exact",
)

# ----------------------------------------------------------------------
# V4 — PDG comparison (numeric; PDG 2024 values as used in F138)
# ----------------------------------------------------------------------
MW, MZ = 80.3692, 91.1880  # GeV
ratio_pdg = MZ / MW
ratio_pred = 3.0 / math.sqrt(7.0)
res_ratio = ratio_pred / ratio_pdg - 1.0

s2_pdg = 1.0 - (MW / MZ) ** 2
res_s2 = (2.0 / 9.0) / s2_pdg - 1.0

check(
    "V4a_mZ_over_mW",
    abs(res_ratio) < 1e-3,
    f"3/sqrt7 = {ratio_pred:.6f} vs PDG {ratio_pdg:.6f}, residual {res_ratio:+.4%}",
)
check(
    "V4b_onshell_s2",
    abs(res_s2) < 5e-3,
    f"2/9 = {2/9:.6f} vs PDG on-shell {s2_pdg:.6f}, residual {res_s2:+.4%}",
)

# ----------------------------------------------------------------------
results["summary"] = {
    "n_pass": sum(1 for c in results["checks"].values() if c["pass"]),
    "n_total": len(results["checks"]),
    "relevant_vectors": [list(v) for v in sorted(relevant)],
    "vertices_exact": [[str(c) for c in x] for x in verts],
    "pdg_inputs": {"mW_GeV": MW, "mZ_GeV": MZ},
}
os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
with open(RESULTS, "w") as f:
    json.dump(results, f, indent=2)
print(f"\n{results['summary']['n_pass']}/{results['summary']['n_total']} PASS -> {RESULTS}")
if failures:
    raise SystemExit(f"FAILED: {failures}")
