"""
NB-044 (p.36): "dimensionality from connection number" -- claims: 2 connections -> 1D lines &
circles; 3 connections -> various 1D/2D structures (linear/circular/Mobius strip, or 2D lattice);
4 connections -> 2D lattice OR 3D lattice.

Verified by actually constructing standard periodic point lattices and computing each site's
coordination number (# of nearest neighbors) numerically from real 3D coordinates -- not just
citing crystallography by name.
"""
import numpy as np
import json, pathlib
from itertools import product


def nearest_neighbor_count(points, center_idx, tol=1e-6):
    center = points[center_idx]
    dists = np.linalg.norm(points - center, axis=1)
    dists[center_idx] = np.inf
    dmin = dists.min()
    return int(np.sum(dists < dmin + tol))


def make_supercell(basis_vectors, motif, n=3):
    """basis_vectors: list of lattice vectors (1,2,or 3 of them). motif: list of fractional
    offsets within the unit cell. Returns cartesian points for a supercell of size n along each
    lattice direction (centered), to give interior points a well-defined neighbor count."""
    dim = len(basis_vectors)
    pts = []
    ranges = [range(-n, n + 1)] * dim
    for cell in product(*ranges):
        origin = sum(c * np.array(bv) for c, bv in zip(cell, basis_vectors))
        for m in motif:
            m_cart = sum(mi * np.array(bv) for mi, bv in zip(m, basis_vectors)) if dim > 1 else m[0] * np.array(basis_vectors[0])
            pts.append(np.array(origin) + np.array(m_cart if dim > 1 else [m[0] * basis_vectors[0][k] for k in range(len(basis_vectors[0]))]))
    return np.array(pts)


results = {}

# 1D chain, 2 connections
line_pts = np.array([[float(i), 0.0, 0.0] for i in range(-10, 11)])
center_idx = 10  # i=0
results["1D_chain"] = nearest_neighbor_count(line_pts, center_idx)

# 2D square lattice (von Neumann neighbors), 4 connections
sq_pts = np.array([[float(i), float(j), 0.0] for i in range(-6, 7) for j in range(-6, 7)])
center_idx = list(map(tuple, sq_pts)).index((0.0, 0.0, 0.0))
results["2D_square_lattice"] = nearest_neighbor_count(sq_pts, center_idx)

# 2D triangular lattice, 6 connections
tri_pts = []
for i in range(-6, 7):
    for j in range(-6, 7):
        x = i + 0.5 * j
        y = j * np.sqrt(3) / 2
        tri_pts.append([x, y, 0.0])
tri_pts = np.array(tri_pts)
dists0 = np.linalg.norm(tri_pts, axis=1)
center_idx = int(np.argmin(dists0))
results["2D_triangular_lattice"] = nearest_neighbor_count(tri_pts, center_idx)

# 2D hexagonal / honeycomb lattice, 3 connections (two-atom basis)
hex_pts = []
a1 = np.array([1.5, np.sqrt(3) / 2, 0.0])
a2 = np.array([1.5, -np.sqrt(3) / 2, 0.0])
basis = [np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0])]
for i in range(-5, 6):
    for j in range(-5, 6):
        origin = i * a1 + j * a2
        for b in basis:
            hex_pts.append(origin + b)
hex_pts = np.array(hex_pts)
dists0 = np.linalg.norm(hex_pts, axis=1)
center_idx = int(np.argmin(dists0))
results["2D_honeycomb_lattice"] = nearest_neighbor_count(hex_pts, center_idx)

# 3D simple cubic, 6 connections
sc_pts = np.array([[float(i), float(j), float(k)] for i in range(-4, 5) for j in range(-4, 5) for k in range(-4, 5)])
center_idx = list(map(tuple, sc_pts)).index((0.0, 0.0, 0.0))
results["3D_simple_cubic"] = nearest_neighbor_count(sc_pts, center_idx)

# 3D BCC, 8 connections (cubic lattice + body-center)
bcc_pts = []
for i in range(-4, 5):
    for j in range(-4, 5):
        for k in range(-4, 5):
            bcc_pts.append([float(i), float(j), float(k)])
            bcc_pts.append([i + 0.5, j + 0.5, k + 0.5])
bcc_pts = np.array(bcc_pts)
dists0 = np.linalg.norm(bcc_pts, axis=1)
center_idx = int(np.argmin(dists0))
results["3D_BCC"] = nearest_neighbor_count(bcc_pts, center_idx)

# 3D diamond cubic, 4 connections (FCC lattice + 2-atom basis at (0,0,0) and (1/4,1/4,1/4))
diamond_pts = []
fcc_basis_vecs = [np.array([0, 0.5, 0.5]), np.array([0.5, 0, 0.5]), np.array([0.5, 0.5, 0])]
motif = [np.array([0.0, 0.0, 0.0]), np.array([0.25, 0.25, 0.25])]
for i in range(-4, 5):
    for j in range(-4, 5):
        for k in range(-4, 5):
            origin = i * fcc_basis_vecs[0] + j * fcc_basis_vecs[1] + k * fcc_basis_vecs[2]
            for m in motif:
                diamond_pts.append(origin + m)
diamond_pts = np.array(diamond_pts)
dists0 = np.linalg.norm(diamond_pts, axis=1)
center_idx = int(np.argmin(dists0))
results["3D_diamond_cubic"] = nearest_neighbor_count(diamond_pts, center_idx)

# --- assess notebook's specific claims
result = {
    "build": "NB-044",
    "coordination_numbers": results,
    "claim_2_connections_gives_1D": results["1D_chain"] == 2,
    "claim_3_connections_can_give_2D_lattice_honeycomb": results["2D_honeycomb_lattice"] == 3,
    "claim_4_connections_can_give_2D_lattice_square": results["2D_square_lattice"] == 4,
    "claim_4_connections_can_ALSO_give_3D_lattice_diamond": results["3D_diamond_cubic"] == 4,
    "note": "diamond-cubic coordination number 4 (verified numerically from real fractional-"
            "coordinate lattice points, not just cited) is exactly the notebook's claimed "
            "4-connections-can-give-3D case -- a real, standard crystallographic fact (diamond, "
            "silicon, germanium structure), not a coincidence.",
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-044_lattice_coordination.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
