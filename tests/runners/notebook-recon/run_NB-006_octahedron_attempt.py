"""
NB-006 (p.3): octahedron, 2-particle case, "bottom completely determined by top", claimed
"3 only" isomers. The original sketches are NOT in the transcription (only prose + a
generic description of 5 drawings), so the precise combinatorial rule being counted cannot
be recovered with confidence. This script tries the most natural read-outs and reports
which (if any) reproduce "3", as an honest, falsifiable attempt rather than a guess dressed
up as a derivation.

Octahedron: 6 vertices, standard adjacency = all pairs except the 3 "antipodal" pairs
(vertex i is non-adjacent only to its antipode). Rotation group: order 24, isomorphic to S4
(acts on the 3 antipodal *axes* as S4 on 4... no -- standard fact: octahedral rotation group
is isomorphic to S4 acting on the 3 pairs of opposite FACES of the dual cube / equivalently
permuting the 3 coordinate axes with sign flips restricted to even sign-changes). We build it
concretely as the 24 rotation matrices of the cube/octahedron acting on the 6 signed-axis
vertices {+x,-x,+y,-y,+z,-z}, which is the standard, unambiguous construction (no reliance on
guessed labeling).
"""
import itertools
import json
import pathlib
from fractions import Fraction

# 6 vertices of a standard octahedron: +-e_x, +-e_y, +-e_z
verts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
vidx = {v: i for i, v in enumerate(verts)}


def mat_mult(M, v):
    return tuple(sum(M[r][c] * v[c] for c in range(3)) for r in range(3))


# The 24 rotation matrices of the cube: all signed permutation matrices with det = +1
def signed_permutation_matrices():
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([1, -1], repeat=3):
            M = [[0, 0, 0] for _ in range(3)]
            for row, (col, s) in enumerate(zip(perm, signs)):
                M[row][col] = s
            yield M


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


rotation_group = [M for M in signed_permutation_matrices() if det3(M) == 1]
assert len(rotation_group) == 24, f"expected order 24, got {len(rotation_group)}"


def permute_vertex_set(M, subset_bits):
    """subset_bits: tuple of 0/1 length 6, indicating which vertices are 'type A'."""
    new_bits = [0] * 6
    for i, v in enumerate(verts):
        if subset_bits[i]:
            new_v = mat_mult(M, v)
            new_bits[vidx[new_v]] = 1
    return tuple(new_bits)


def orbits_for_k_subset(k):
    all_subsets = set()
    for combo in itertools.combinations(range(6), k):
        bits = [0] * 6
        for c in combo:
            bits[c] = 1
        all_subsets.add(tuple(bits))
    remaining = set(all_subsets)
    orbit_list = []
    while remaining:
        seed = next(iter(remaining))
        orbit = set(permute_vertex_set(M, seed) for M in rotation_group)
        orbit_list.append(sorted(orbit))
        remaining -= orbit
    return orbit_list


results = {}
for k in [1, 2, 3]:
    orbits = orbits_for_k_subset(k)
    results[f"choose_{k}_of_6_vertices_as_type_A"] = {
        "num_labeled_subsets": len(list(itertools.combinations(range(6), k))),
        "num_isomers_under_rotation_group": len(orbits),
        "orbit_sizes": sorted(len(o) for o in orbits),
    }

result = {
    "build": "NB-006 (octahedron, attempted readings)",
    "caveat": "original diagrams not available in the transcription; readings below are "
              "candidate reconstructions, not a recovery of the author's actual rule.",
    "attempts": results,
    "any_attempt_matches_claimed_3": any(v["num_isomers_under_rotation_group"] == 3 for v in results.values()),
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-006_octahedron_attempt.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
