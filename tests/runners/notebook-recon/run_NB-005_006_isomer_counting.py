"""
NB-005 (p.3): "Tetrahedron with 3 types of particles -- how many isomers? Only 2 -- cannot
have anything else if all must join each vertex."
NB-006 (p.3): "With octahedron ... For 2-particle, bottom is completely determined by top.
How many isomers? 3 only."

Reading adopted for NB-005 (stated explicitly in the write-up; this is the one place in this
batch where the notebook's own diagrams -- not transcribed -- must be guessed at, so the
reading is made explicit and testable on its own terms):
  - Tetrahedron = K4 (4 vertices, 6 edges, each vertex has degree 3).
  - "3 types of particles ... join each vertex" = a proper 3-edge-colouring of K4 in which
    every vertex sees all 3 colours (forced automatically since degree = 3 = number of colours).
  - "Isomers" = such colourings counted up to the ROTATION group of the tetrahedron (order 12,
    i.e. the alternating group A4 acting on the 4 vertices), not the full symmetry group
    including reflections (order 24) -- both are tried below and reported, since a real physical
    model of chiral objects usually only allows proper rotations.

Brute-force enumeration (no shortcuts): enumerate all edge-colourings of K4 with 3 colours
that are proper at every vertex, then count orbits under (a) the rotation group A4 and
(b) the full symmetry group S4, via explicit orbit enumeration (not just Burnside's formula,
so the actual orbit representatives are also recoverable for the write-up).
"""
import itertools
import json
import pathlib

# --- K4 vertices and edges
vertices = [0, 1, 2, 3]
edges = list(itertools.combinations(vertices, 2))  # 6 edges
edge_index = {e: i for i, e in enumerate(edges)}


def edge_key(a, b):
    return edges[edge_index[tuple(sorted((a, b)))]]


# --- proper 3-edge-colourings of K4: every vertex (degree 3) sees all 3 colours exactly once
def is_proper(coloring):
    for v in vertices:
        colors_at_v = set()
        for e in edges:
            if v in e:
                colors_at_v.add(coloring[edge_index[e]])
        if colors_at_v != {0, 1, 2}:
            return False
    return True


all_colorings = []
for coloring in itertools.product([0, 1, 2], repeat=6):
    if is_proper(coloring):
        all_colorings.append(coloring)

# --- symmetric group S4 acting on vertices 0..3 -> induces a permutation of the 6 edges
S4 = list(itertools.permutations(vertices))


def permute_coloring(perm, coloring):
    new_coloring = [None] * 6
    for e_idx, (a, b) in enumerate(edges):
        pa, pb = perm[a], perm[b]
        new_e_idx = edge_index[tuple(sorted((pa, pb)))]
        new_coloring[new_e_idx] = coloring[e_idx]
    return tuple(new_coloring)


def is_even_permutation(perm):
    # count inversions
    inv = 0
    n = len(perm)
    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                inv += 1
    return inv % 2 == 0


A4 = [perm for perm in S4 if is_even_permutation(perm)]  # rotation group, order 12

coloring_set = set(all_colorings)
assert len(coloring_set) == len(all_colorings), "unexpected duplicate colorings"


def orbits_under(group):
    remaining = set(coloring_set)
    orbit_list = []
    while remaining:
        seed = next(iter(remaining))
        orbit = set(permute_coloring(perm, seed) for perm in group)
        assert orbit <= coloring_set, "orbit left the coloring set -- group action bug"
        orbit_list.append(sorted(orbit))
        remaining -= orbit
    return orbit_list


orbits_A4 = orbits_under(A4)
orbits_S4 = orbits_under(S4)

result = {
    "build": "NB-005 (tetrahedron)",
    "num_proper_3edge_colorings_labeled": len(all_colorings),
    "num_isomers_under_rotation_group_A4_order12": len(orbits_A4),
    "orbit_sizes_under_A4": sorted(len(o) for o in orbits_A4),
    "num_isomers_under_full_symmetry_group_S4_order24": len(orbits_S4),
    "orbit_sizes_under_S4": sorted(len(o) for o in orbits_S4),
    "matches_notebook_claim_of_2_under_rotation_only": len(orbits_A4) == 2,
    "matches_notebook_claim_of_2_under_full_symmetry": len(orbits_S4) == 2,
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-005_006_isomer_counting.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
