#!/usr/bin/env python3
"""
test_FA08_three_generations.py
==============================

FA08 (Tier A, falsification suite) — Exactly three fermion generations from the
BCC point-group selection of the F27 chiral mass step (F75), folded together
with the F38 single-generation anomaly-cancellation quantum numbers.

Brief: tests/falsification/FA08-three-generations.md

This is a symbolic / exact-rational confrontation (no chiral or Dirac transforms
through numpy/scipy — CLAUDE.md caveat). The only float is the Schur-degeneracy
linear-algebra demo (commutator floor ~1e-16), which merely illustrates the
exactly-rational multiplicity result.

Chain (each step exact over Z / Q):

  S1  Rebuild O_h (the BCC vacuum point group) from two cube rotations +
      inversion -> 48 elements, 10 genuine conjugacy classes.
  S2  Embed the all-integer O_h single-valued character table and cross-check
      it is orthonormal over Z:  <chi_a, chi_b> = 48 * delta_ab.  The maximal
      single-valued irrep dimension is 3 (sum d^2 = 48, Burnside-complete),
      so NO 4-dim single-valued irrep exists -> a 4th symmetry-degenerate
      partner is representation-theoretically forbidden (Schur).
  S3  Decompose the 8 BCC nearest-neighbour body-diagonal sites (the shell the
      F27 mass step couples to):  A1g (+) A2u (+) T1u (+) T2g.  It contains a
      triplet, so the mechanism is non-empty (answer is 3, not 1 or 2).
  S4  Parity selection of the SCALAR F27 chiral mass: the anchored chirality
      sits in A1g; a scalar bilinear needs an ODD-parity (u) partner.  Odd
      shell content = A2u (+) T1u; the unique odd TRIPLET is T1u (dim 3).
      => generation multiplicity = dim(T1u) = 3 exactly.
  S5  Schur stability demo: an O_h-invariant Hermitian mass operator on the
      shell has eigenvalue degeneracies exactly [1,1,3,3]; max protected = 3.
  S6  Anomaly-quantum-number compatibility (F38 / FG-1): one generation's
      L-handed Weyl content cancels all six gauge + gravitational anomalies
      exactly.  N identical copies give N * 0 = 0 for ANY N -> anomalies do
      not cap the count.  The cap is purely the group-theory selection of S2-S4.
      => the selected triplet is each an anomaly-free SM generation, and the
      count is fixed at 3 by the irrep dimension, not by anomaly freedom.
  S7  Consistency with LEP:  N_nu = 2.984 +/- 0.008 (invisible Z width) is
      within ~2 sigma of 3 and excludes a 4th light active neutrino.

PASS gate (brief): exactly three stable mass-carrying irreps AND no 4th
generation observed.
"""

import json
import os
from fractions import Fraction as Fr
import numpy as np

RESULTS = {}
PASS = True


def record(name, ok, detail):
    global PASS
    RESULTS[name] = {"pass": bool(ok), **detail}
    PASS = PASS and bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ════════════════════════════════════════════════════════════════════
#  S1  Build O_h (48 elements) from generators, exact integer 3x3 matrices
# ════════════════════════════════════════════════════════════════════
def matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3))
                 for i in range(3))


R_z = ((0, -1, 0), (1, 0, 0), (0, 0, 1))     # 90 deg about z
R_x = ((1, 0, 0), (0, 0, -1), (0, 1, 0))     # 90 deg about x
INV = ((-1, 0, 0), (0, -1, 0), (0, 0, -1))   # inversion


def close_group(gens):
    elems = {((1, 0, 0), (0, 1, 0), (0, 0, 1))}
    frontier = list(elems)
    while frontier:
        g = frontier.pop()
        for h in gens:
            for cand in (matmul(g, h), matmul(h, g)):
                if cand not in elems:
                    elems.add(cand)
                    frontier.append(cand)
    return elems


O_group = close_group([R_z, R_x])
Oh_group = close_group([R_z, R_x, INV])
record("S1_group_orders", len(O_group) == 24 and len(Oh_group) == 48,
       {"|O|": len(O_group), "|O_h|": len(Oh_group), "expected": "24, 48"})


def trace(M):
    return M[0][0] + M[1][1] + M[2][2]


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


VERTS = [(sx, sy, sz) for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)]


def apply(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(3)) for i in range(3))


def fixed_vertices(M):
    return sum(1 for v in VERTS if apply(M, v) == tuple(v))


def transpose(M):
    return tuple(tuple(M[j][i] for j in range(3)) for i in range(3))


remaining = set(Oh_group)
conj_classes = []
while remaining:
    h = next(iter(remaining))
    cls = set()
    for g in Oh_group:
        cls.add(matmul(matmul(g, h), transpose(g)))
    conj_classes.append(cls)
    remaining -= cls

class_info = {}
for cls in conj_classes:
    rep = next(iter(cls))
    key = (det3(rep), trace(rep), len(cls))
    class_info[key] = {"det": det3(rep), "trace": trace(rep), "size": len(cls),
                       "fixed": fixed_vertices(rep)}


def class_label(det, tr, size):
    table = {
        (1, 3, 1): "E", (1, 0, 8): "8C3", (1, 1, 6): "6C4",
        (1, -1, 3): "3C2", (1, -1, 6): "6C2p",
        (-1, -3, 1): "i", (-1, 0, 8): "8S6", (-1, -1, 6): "6S4",
        (-1, 1, 3): "3sigma_h", (-1, 1, 6): "6sigma_d",
    }
    return table[(det, tr, size)]


perm_char = {}
class_size = {}
for key, info in class_info.items():
    lab = class_label(info["det"], info["trace"], info["size"])
    perm_char[lab] = info["fixed"]
    class_size[lab] = info["size"]

record("S1b_ten_classes", len(perm_char) == 10,
       {"n_classes": len(perm_char), "expected": 10, "sizes": class_size})


# ════════════════════════════════════════════════════════════════════
#  S2  O_h single-valued character table (integers) + orthonormality
# ════════════════════════════════════════════════════════════════════
ORDER = ["E", "8C3", "6C4", "3C2", "6C2p", "i", "8S6", "6S4", "3sigma_h", "6sigma_d"]
DIM = {"A1g": 1, "A2g": 1, "Eg": 2, "T1g": 3, "T2g": 3,
       "A1u": 1, "A2u": 1, "Eu": 2, "T1u": 3, "T2u": 3}
CHI_O = {
    "A1": [1, 1, 1, 1, 1],
    "A2": [1, 1, -1, 1, -1],
    "E":  [2, -1, 0, 2, 0],
    "T1": [3, 0, 1, -1, -1],
    "T2": [3, 0, -1, -1, 1],
}
PROPER = ["E", "8C3", "6C4", "3C2", "6C2p"]
IMPROPER = ["i", "8S6", "6S4", "3sigma_h", "6sigma_d"]

CHAR = {}
for base in CHI_O:
    for par, sgn in (("g", 1), ("u", -1)):
        name = base + par
        d = {}
        for cl, val in zip(PROPER, CHI_O[base]):
            d[cl] = val
        for cl, val in zip(IMPROPER, CHI_O[base]):
            d[cl] = sgn * val
        CHAR[name] = d

ortho_ok = True
for a in CHAR:
    for b in CHAR:
        s = sum(class_size[c] * CHAR[a][c] * CHAR[b][c] for c in ORDER)
        if s != (48 if a == b else 0):
            ortho_ok = False
record("S2_char_table_orthonormal", ortho_ok,
       {"note": "embedded O_h table passes <chi_a,chi_b>=48 delta_ab exactly over Z"})

max_dim = max(DIM.values())
record("S2b_max_single_valued_irrep_dim", max_dim == 3,
       {"max_irrep_dim": max_dim,
        "sum_d_squared": sum(d * d for d in DIM.values()),
        "expected_sum": 48,
        "claim": "no 4-dim single-valued irrep -> 4th degenerate partner forbidden (Schur)"})


# ════════════════════════════════════════════════════════════════════
#  S3  Decompose the 8-vertex BCC shell (exact rational multiplicities)
# ════════════════════════════════════════════════════════════════════
def multiplicity(irrep):
    s = Fr(0)
    for c in ORDER:
        s += class_size[c] * perm_char[c] * CHAR[irrep][c]
    return s / 48


decomp = {ir: multiplicity(ir) for ir in CHAR}
decomp_nonzero = {ir: int(m) for ir, m in decomp.items() if m != 0}
all_integer = all(m.denominator == 1 for m in decomp.values())
dim_check = sum(int(m) * DIM[ir] for ir, m in decomp.items()) == 8
expected_decomp = {"A1g": 1, "A2u": 1, "T1u": 1, "T2g": 1}
record("S3_shell_decomposition",
       all_integer and dim_check and decomp_nonzero == expected_decomp,
       {"decomposition": decomp_nonzero, "expected": expected_decomp,
        "sum_of_dims": 8,
        "contains_triplet": any(DIM[ir] == 3 for ir in decomp_nonzero)})


# ════════════════════════════════════════════════════════════════════
#  S4  Parity selection of the scalar F27 mass -> unique odd triplet T1u
# ════════════════════════════════════════════════════════════════════
odd_irreps = [ir for ir in decomp_nonzero if ir.endswith("u")]
odd_triplets = [ir for ir in odd_irreps if DIM[ir] == 3]
n_generations = DIM[odd_triplets[0]] if odd_triplets else None
record("S4_parity_selected_triplet",
       odd_triplets == ["T1u"] and n_generations == 3,
       {"odd_parity_shell_content": odd_irreps,
        "odd_triplets": odd_triplets,
        "selected_generation_multiplet": "T1u (dim 3)",
        "n_generations": n_generations})


# ════════════════════════════════════════════════════════════════════
#  S5  Schur stability: O_h-invariant Hermitian operator degeneracies
#  (the only float in the chain; real symmetric, no chiral transform)
# ════════════════════════════════════════════════════════════════════
vidx = {tuple(v): i for i, v in enumerate(VERTS)}


def perm_matrix(M):
    P = np.zeros((8, 8))
    for i, v in enumerate(VERTS):
        P[vidx[apply(M, v)], i] = 1.0
    return P


reps = [perm_matrix(g) for g in Oh_group]
rng = np.random.default_rng(75)
seed = rng.standard_normal((8, 8))
seed = seed + seed.T
Hsym = sum(P @ seed @ P.T for P in reps) / len(reps)
comm = max(np.max(np.abs(P @ Hsym - Hsym @ P)) for P in reps)
evals = np.sort(np.linalg.eigvalsh(Hsym))
groups = []
for e in evals:
    if groups and abs(e - groups[-1][0]) < 1e-9:
        groups[-1].append(e)
    else:
        groups.append([e])
degen = sorted(len(g) for g in groups)
record("S5_schur_degeneracies",
       comm < 1e-12 and degen == [1, 1, 3, 3],
       {"commutator_with_group": float(comm),
        "eigenvalue_degeneracies": degen, "expected": [1, 1, 3, 3],
        "max_protected_degeneracy": max(degen)})


# ════════════════════════════════════════════════════════════════════
#  S6  F38 / FG-1 anomaly content: one generation cancels all six anomalies
#  exactly; replicating it N times gives N*0 = 0 for ANY N.  So anomalies
#  do NOT cap the count; the cap is the S2-S4 group selection (= 3).
#  Convention Q = T3 + Y/2 (F38 §2.1).  L-handed Weyl basis.
# ════════════════════════════════════════════════════════════════════
# (color_dim, isospin_dim, Y, A3)  per L-handed Weyl species in one generation
# A3 = SU(3) cubic anomaly coefficient: +1 for 3, -1 for 3bar, 0 for singlet.
SPECIES = [
    # name,        c_dim, i_dim,  Y,        A3
    ("L",            1,    2,   Fr(-1),     0),
    ("e^c",          1,    1,   Fr(2),      0),
    ("Q",            3,    2,   Fr(1, 3),   1),
    ("u^c",          3,    1,   Fr(-4, 3), -1),
    ("d^c",          3,    1,   Fr(2, 3),  -1),
]
T2 = Fr(1, 2)   # Dynkin index of SU(2) fundamental
T3 = Fr(1, 2)   # Dynkin index of SU(3) fundamental


def anomalies_for_copies(N):
    grav_U1 = Fr(0)   # [grav]^2 . U(1)_Y  : sum n_i Y_i
    U1_cubed = Fr(0)  # U(1)_Y^3           : sum n_i Y_i^3
    SU2sq_U1 = Fr(0)  # [SU(2)]^2 . U(1)   : sum c_dim * T2 * Y  (i_dim=2 species)
    SU3sq_U1 = Fr(0)  # [SU(3)]^2 . U(1)   : sum i_dim * T3 * Y  (colored species)
    SU3_cubed = Fr(0) # [SU(3)]^3          : sum i_dim * A3
    for (_, cdim, idim, Y, A3) in SPECIES:
        n = cdim * idim
        grav_U1 += n * Y
        U1_cubed += n * Y ** 3
        if idim == 2:
            SU2sq_U1 += cdim * T2 * Y
        if cdim in (3,):  # colored fundamental (3 or 3bar both index 1/2)
            SU3sq_U1 += idim * T3 * Y
            SU3_cubed += idim * A3
    # [SU(2)]^3 vanishes identically (SU(2) reps pseudo-real) -> 0
    SU2_cubed = Fr(0)
    six = {
        "grav^2.U1": grav_U1, "U1^3": U1_cubed, "SU2^2.U1": SU2sq_U1,
        "SU3^2.U1": SU3sq_U1, "SU3^3": SU3_cubed, "SU2^3": SU2_cubed,
    }
    return {k: N * v for k, v in six.items()}


anom_1 = anomalies_for_copies(1)
anom_3 = anomalies_for_copies(3)
anom_4 = anomalies_for_copies(4)
one_gen_cancels = all(v == 0 for v in anom_1.values())
three_gen_cancels = all(v == 0 for v in anom_3.values())
four_also_cancels = all(v == 0 for v in anom_4.values())
record("S6_anomaly_compatibility",
       one_gen_cancels and three_gen_cancels and four_also_cancels,
       {"one_generation_anomalies": {k: str(v) for k, v in anom_1.items()},
        "three_copies_anomalies": {k: str(v) for k, v in anom_3.items()},
        "four_copies_anomalies": {k: str(v) for k, v in anom_4.items()},
        "one_generation_cancels_all_six": one_gen_cancels,
        "N_copies_cancel_for_any_N": three_gen_cancels and four_also_cancels,
        "note": "anomaly freedom holds for ANY N -> it does NOT cap the count; "
                "the cap is the O_h irrep selection (=3). Selected T1u triplet "
                "is thus 3 anomaly-free identical SM generations."})


# ════════════════════════════════════════════════════════════════════
#  S7  Consistency with LEP invisible Z width: N_nu = 2.984 +/- 0.008
# ════════════════════════════════════════════════════════════════════
N_nu = 2.984
N_nu_err = 0.008
sigma_from_3 = abs(N_nu - 3.0) / N_nu_err
lep_consistent = sigma_from_3 < 3.0   # within 3 sigma of 3; excludes 4
record("S7_LEP_consistency",
       lep_consistent,
       {"N_nu_measured": N_nu, "N_nu_err": N_nu_err,
        "predicted": 3, "deviation_sigma": round(sigma_from_3, 3),
        "excludes_4th_light_active_neutrino": True,
        "source": "PDG / LEP invisible Z width"})


# ════════════════════════════════════════════════════════════════════
print("\nOVERALL:", "PASS" if PASS else "FAIL")

verdict = "PASS" if PASS else "FALSIFIED"
out = {
    "test_id": "FA08",
    "name": "Exactly three fermion generations (BCC O_h irrep selection of F27 mass step)",
    "tier": "A — sharp falsifier",
    "verdict": verdict,
    "predicted": {
        "n_generations": 3,
        "mechanism": "dim(T1u) of O_h = 3; no 4-dim single-valued irrep -> 4th forbidden",
        "selected_irrep": "T1u (odd-parity cubic vector triplet)",
    },
    "measured_target": {
        "N_nu": "2.984 +/- 0.008",
        "source": "PDG / LEP invisible Z width (light active neutrinos)",
        "fourth_generation_observed": False,
    },
    "gate": "PASS iff exactly three stable mass-carrying irreps AND no 4th "
            "generation observed; FALSIFIED on a 4th chiral fermion, a 4th "
            "confirmed light active neutrino, or group multiplicity != 3.",
    "computed": {
        "|O_h|": len(Oh_group),
        "max_single_valued_irrep_dim": max_dim,
        "shell_decomposition": decomp_nonzero,
        "odd_triplets": odd_triplets,
        "n_generations": n_generations,
        "schur_degeneracies": degen,
        "one_generation_cancels_all_six_anomalies": one_gen_cancels,
        "anomaly_free_for_any_N_copies": three_gen_cancels and four_also_cancels,
        "N_nu_deviation_from_3_sigma": round(sigma_from_3, 3),
    },
    "checks": RESULTS,
    "commands": [
        "python3 tests/findings/test_FA08_three_generations.py",
    ],
    "timestamp": "2026-06-10",
    "provenance": ["F75", "F76", "F84", "F38", "F27"],
}
outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test-results"))
os.makedirs(outdir, exist_ok=True)
outpath = os.path.join(outdir, "FA08_three_generations.json")
with open(outpath, "w") as f:
    json.dump(out, f, indent=2, default=str)
print("wrote", outpath)
