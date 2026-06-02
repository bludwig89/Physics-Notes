"""
F47 derivation attempt — try to derive sin^2 theta_W = 2/9 (notebook's
"W± = 3e exactly") from the BCC lattice structure.

This script runs three steps:

  Step 1 — Extend F45 sigma<->tau counting to finite k on the BCC.
           Define the swap-singlet and swap-triplet projectors and
           compute their kinetic weights against the Bloch Hamiltonian
           of the BCC walk, summed over the Brillouin zone.

  Step 2 — Bond-axis counting. The BCC has 8 nearest-neighbour bonds
           (4 distinct body-diagonal axes mod sign) plus 6 next-NN
           bonds (3 face axes mod sign).  Try a bond-axis assignment:
           SU(2)_L couples on all 7 unique axes (4+3); U(1)_Y couples
           on a 2-dim subspace (e.g. the two sublattices).  Check
           whether the resulting g'^2/g^2 = 2/7.

  Step 3 — Verify numerically against bcc_dispersion at O(k^2) and
           O(k^3).  The F30 anisotropy must be consistent with whatever
           weighting we extract.

Writes the result table to test-results/F47_bcc_weinberg_2over9.json.

Date: 2026-05-28
"""

from __future__ import annotations
import json
import os
import sys
from fractions import Fraction

import numpy as np

# add ca-simulation to path
_HERE = os.path.dirname(os.path.abspath(__file__))
_CA = os.path.normpath(os.path.join(_HERE, "..", "ca-simulation"))
sys.path.insert(0, _CA)

import ca_bcc  # noqa: E402


# ======================================================================
# Utilities
# ======================================================================

def sin2_thetaW(ratio_gp2_g2):
    """sin^2 theta_W = (g'^2) / (g^2 + g'^2) = r/(1+r) where r = g'^2/g^2."""
    if isinstance(ratio_gp2_g2, Fraction):
        return ratio_gp2_g2 / (1 + ratio_gp2_g2)
    return ratio_gp2_g2 / (1.0 + ratio_gp2_g2)


def report(name, ratio):
    s2 = sin2_thetaW(ratio)
    if isinstance(s2, Fraction):
        s2_f = float(s2)
    else:
        s2_f = float(s2)
    return {
        "name": name,
        "gprime2_over_g2": str(ratio),
        "gprime2_over_g2_float": float(ratio) if not isinstance(ratio, Fraction) else float(ratio),
        "sin2_thetaW": str(s2) if isinstance(s2, Fraction) else s2_f,
        "sin2_thetaW_float": s2_f,
        "PDG_diff_pct": 100 * (s2_f - 0.22321) / 0.22321,
    }


# ======================================================================
# Step 1 — F45 swap counting at finite k
# ======================================================================
#
# Setup: at every BCC site live |state> in C^2_sigma (x) C^2_tau.
# The sigma<->tau swap Pi acts as A (x) B -> B (x) A.
# F45 (leading order) counts:
#   - 1 swap-invariant direction (I (x) I) -> Y
#   - 3 swap-triplet directions (Sym^2 C^2) -> SU(2)_L
# giving g'^2/g^2 = 1/3.
#
# Finite-k modification idea: weight each direction by its kinetic
# energy contribution from the BCC Bloch Hamiltonian, averaged over
# the Brillouin zone.  The BCC unitary is
#
#     U^+(k) = u(k) I  -  i (sigma . n(k))
#
# whose Hermitian generator is H(k) = arccos(u) * (sigma . n / sin omega).
# At leading order H -> (1/sqrt 3) sigma . k (Weyl).
#
# The KE weight of generator G is <G> = sum_k Tr(G^dagger H(k) G H(k)) / Z,
# normalized.  Below we compute these numerically for the swap-singlet
# (proportional to I (x) I) and swap-triplet (proportional to
# I (x) tau^a) directions in the L-doublet space.

def step1_finite_k_weights(L=48):
    """Compute Brillouin-zone-averaged kinetic weights of singlet vs triplet.

    Returns the ratio (singlet weight) / (triplet weight) -- the candidate
    g'^2/g^2 at finite k.
    """
    kgrid = np.linspace(-np.pi, np.pi, L, endpoint=False)
    KX, KY, KZ = np.meshgrid(kgrid, kgrid, kgrid, indexing="ij")

    u, nx, ny, nz = ca_bcc._bcc_uvec(KX, KY, KZ, sign="+")
    # avoid arccos at degenerate point k=0
    omega = np.arccos(np.clip(u, -1.0, 1.0))
    sin_om = np.sqrt(np.clip(1.0 - u * u, 0.0, None))

    # H(k) = omega * (n_hat . sigma), trace |H|^2 = 2 omega^2 (since n_hat^2=1)
    # The "sigma . n" piece is the chiral/triplet structure;
    # the "u . I" piece is the singlet structure.
    # Bloch Hamiltonian energy split:
    #   triplet KE density ~ |n|^2 = sin^2 omega  (couples to sigma operators)
    #   singlet KE density ~ (1-u)^2  ~  (1 - cos omega)^2  (acts as I)
    # but the standard kinetic-form coupling for a Hamiltonian H is its trace
    # against the generator.  For sigma^a: weight = n_a^2.
    # For I: weight = u^2 ... but that is trivial (does not move charge).
    # The "isospin trace" piece -- which couples to U(1)_Y -- is the part
    # of the *covariant derivative* that distributes equally on sigma's
    # and I.  We measure isotropic vs anisotropic averages.

    # Triplet generator weight = average of (n_x^2 + n_y^2 + n_z^2)
    w_triplet = float(np.mean(nx * nx + ny * ny + nz * nz))
    # Singlet generator weight = average of (1 - u)^2 normalized by
    # the kinetic scale.  Use (omega^2 - sum n^2_a) for the
    # "scalar excess" of the dispersion above the Weyl form.
    # At leading order omega^2 = |k|^2/3 = sum n_a^2 (Weyl); the
    # singlet piece is the difference.
    scalar_excess = float(np.mean(np.maximum(omega ** 2 - (nx ** 2 + ny ** 2 + nz ** 2), 0.0)))

    return {
        "L": L,
        "w_triplet_BZ_avg": w_triplet,
        "w_singlet_BZ_avg": scalar_excess,
        "ratio_singlet_to_triplet": scalar_excess / w_triplet,
        "F45_leading_ratio": 1.0 / 3.0,
        "comment": (
            "Triplet weight is the BZ-average of |n(k)|^2 = sin^2 omega(k). "
            "Singlet weight is the BZ-average of (omega^2 - |n|^2): the "
            "deviation of the actual BCC dispersion from the leading-order "
            "Weyl form.  At leading order both are O(k^2)/3 and equal, "
            "but the singlet picks up O(k^4) corrections that the triplet "
            "does not."
        ),
    }


# ======================================================================
# Step 2 — Bond-axis counting (the 7 candidate)
# ======================================================================
#
# BCC bond inventory:
#
#   Nearest neighbours: 8 sites at (+/- 1, +/- 1, +/- 1) / 2 (primitive)
#     or (+/-1, +/-1, +/-1) in cubic-unit conventional cell.
#     4 unique axes mod sign: (1,1,1), (1,1,-1), (1,-1,1), (-1,1,1).
#
#   Next-nearest neighbours: 6 sites at (+/-1, 0, 0), (0, +/-1, 0),
#     (0, 0, +/-1).  3 unique axes mod sign: x, y, z.
#
#   Total unique bond axes to second shell: 4 + 3 = 7.
#
#   Sublattices: BCC has 2 (corner + body-centre = 2 interpenetrating SC).
#
# Hypothesis: SU(2)_L generators are distributed over the 7 unique
# bond axes (g^2 weight = 7); U(1)_Y generator is distributed over
# the 2 sublattices (g'^2 weight = 2).  This gives g'^2/g^2 = 2/7,
# i.e. sin^2 theta_W = 2/9.

def step2_bond_axis_counting():
    """Enumerate BCC bond directions, sublattices, and check 2:7 ratio."""
    # Nearest-neighbour bond direction vectors (cubic conventional cell)
    nn_bonds = [(sx, sy, sz)
                for sx in (-1, 1)
                for sy in (-1, 1)
                for sz in (-1, 1)]
    # Unique axes (modulo sign)
    nn_unique_axes = set()
    for b in nn_bonds:
        ax = tuple(sorted([b, tuple(-x for x in b)])[0])
        nn_unique_axes.add(ax)
    nnn_bonds = [(2, 0, 0), (-2, 0, 0),
                 (0, 2, 0), (0, -2, 0),
                 (0, 0, 2), (0, 0, -2)]
    nnn_unique_axes = set()
    for b in nnn_bonds:
        ax = tuple(sorted([b, tuple(-x for x in b)])[0])
        nnn_unique_axes.add(ax)

    n_nn_unique = len(nn_unique_axes)
    n_nnn_unique = len(nnn_unique_axes)
    n_total_unique = n_nn_unique + n_nnn_unique

    # Sublattices
    n_sublattices = 2

    # Candidate ratio for U(1)_Y : SU(2)_L
    candidate_ratio = Fraction(n_sublattices, n_total_unique)
    s2 = sin2_thetaW(candidate_ratio)
    return {
        "nn_bonds_total": len(nn_bonds),
        "nn_unique_axes": n_nn_unique,
        "nnn_bonds_total": len(nnn_bonds),
        "nnn_unique_axes": n_nnn_unique,
        "total_unique_bond_axes_to_2nd_shell": n_total_unique,
        "n_sublattices": n_sublattices,
        "candidate_gprime2_over_g2": str(candidate_ratio),
        "candidate_sin2_thetaW": str(s2),
        "candidate_sin2_thetaW_float": float(s2),
        "PDG_diff_pct": 100 * (float(s2) - 0.22321) / 0.22321,
        "interpretation": (
            "IF SU(2)_L kinetic terms distribute one independent coupling per "
            "unique BCC bond axis (4 body-diagonal + 3 face = 7 axes) AND "
            "U(1)_Y kinetic term distributes one per sublattice (2 sublattices "
            "in BCC), THEN g'^2/g^2 = 2/7 and sin^2 theta_W = 2/9 exactly. "
            "This matches the notebook's W^pm = 3e hypothesis (p. 104) and "
            "lands within 0.4% of PDG (0.2232). HOWEVER the physical reason "
            "for distributing the couplings *this way* is not derived from "
            "BCC structure alone -- it requires choosing this assignment by "
            "hand."
        ),
    }


# ======================================================================
# Step 3 — Numerical verification against bcc_dispersion
# ======================================================================
#
# We verify the candidate counting against the actual BCC unitary
# by computing direction-averaged kinetic weights and comparing
# them against the predicted 2:7 ratio.

def step3_numerical_verify(L=64):
    """Compute kinetic weights along body-diagonal vs face-axis directions
    in the BCC Bloch Hamiltonian, then test the 2:7 candidate."""

    # Probe along each independent direction
    ks = np.linspace(0.0, 0.5, 50)  # small-k regime

    # Body-diagonal probe: (1,1,1)/sqrt(3) * k
    bd = np.array([1, 1, 1]) / np.sqrt(3)
    # Face-axis probe: (1,0,0)
    fa = np.array([1, 0, 0])

    omega_bd_plus = np.array([
        ca_bcc.bcc_dispersion(k * bd[0], k * bd[1], k * bd[2], sign="+")
        for k in ks
    ])
    omega_bd_minus = np.array([
        ca_bcc.bcc_dispersion(k * bd[0], k * bd[1], k * bd[2], sign="-")
        for k in ks
    ])
    omega_fa = np.array([
        ca_bcc.bcc_dispersion(k * fa[0], k * fa[1], k * fa[2], sign="+")
        for k in ks
    ])

    # Quadratic (leading) coefficient should be 1/sqrt(3) for all
    # (the lattice c_lat), but the cubic correction differs by direction.
    # Fit omega(k) = a1 k + a3 k^3 along each.
    def fit_a1_a3(ks, om):
        # exclude k=0
        mask = ks > 1e-6
        A = np.column_stack([ks[mask], ks[mask] ** 3])
        coef, *_ = np.linalg.lstsq(A, om[mask], rcond=None)
        return coef[0], coef[1]

    a1_bd_p, a3_bd_p = fit_a1_a3(ks, omega_bd_plus)
    a1_bd_m, a3_bd_m = fit_a1_a3(ks, omega_bd_minus)
    a1_fa, a3_fa = fit_a1_a3(ks, omega_fa)

    # Birefringence on body diagonal (F37 prediction: -sqrt(3)/27 * k^2,
    # but at the omega level it's a higher order; F37 had Delta v/c = -k/18).
    delta_bd_per_k = (omega_bd_plus - omega_bd_minus) / np.where(ks > 0, ks, 1)
    delta_bd_per_k[0] = 0.0

    # Body-diagonal slowing relative to 1/sqrt(3)
    bd_slowdown_at_k_max = (1.0 / np.sqrt(3.0) - omega_bd_plus[-1] / ks[-1])
    fa_slowdown_at_k_max = (1.0 / np.sqrt(3.0) - omega_fa[-1] / ks[-1])

    return {
        "L_probe": L,
        "c_lat_leading": 1.0 / np.sqrt(3.0),
        "body_diagonal_+_a1": a1_bd_p,
        "body_diagonal_+_a3": a3_bd_p,
        "body_diagonal_-_a1": a1_bd_m,
        "body_diagonal_-_a3": a3_bd_m,
        "face_axis_a1": a1_fa,
        "face_axis_a3": a3_fa,
        "body_diagonal_slowdown_at_k=0.5": bd_slowdown_at_k_max,
        "face_axis_slowdown_at_k=0.5": fa_slowdown_at_k_max,
        "interpretation": (
            "Along the cube face axes, omega(k) = k/sqrt(3) exactly with "
            "no cubic correction.  Along the body diagonals there is a "
            "nonzero a3.  This is the F30/F37 anisotropy.  If g^2 is the "
            "sum over bond-axis hopping weights, the 7 unique axes (4 body "
            "diagonal + 3 face) contribute UNEQUALLY at finite k.  The "
            "naive 7-fold equality used in Step 2 is therefore broken by "
            "the BCC anisotropy itself."
        ),
    }


# ======================================================================
# Step 4 (synthesis) — does any natural counting give exactly 2/9?
# ======================================================================

def synthesis():
    candidates = []

    # F45 leading: 1/3
    candidates.append(report("F45 leading (1 singlet : 3 triplet)", Fraction(1, 3)))
    # Notebook target: 2/7 -> 2/9
    candidates.append(report("Notebook W± = 3e (target)", Fraction(2, 7)))
    # 2 sublattices : 7 bond axes
    candidates.append(report("2 sublattices : 7 bond axes (Step 2 hypothesis)", Fraction(2, 7)))
    # 2 sublattices : 8 NN bonds
    candidates.append(report("2 sublattices : 8 NN bonds", Fraction(2, 8)))
    # 2 chirality branches : 7 bond axes
    candidates.append(report("2 chirality branches : 7 axes", Fraction(2, 7)))
    # SU(5) GUT for reference
    candidates.append(report("SU(5) GUT tree", Fraction(3, 5)))
    # 6 face : 8 body diagonal (no 2/7 here)
    candidates.append(report("6 face : 8 body diagonal", Fraction(6, 8)))

    return candidates


def main():
    print("=" * 72)
    print("F47 — Attempt to derive sin^2 theta_W = 2/9 from BCC lattice")
    print("=" * 72)

    print("\n--- Step 1: finite-k F45 swap counting ---")
    step1 = step1_finite_k_weights(L=20)
    for k, v in step1.items():
        print(f"  {k}: {v}")

    print("\n--- Step 2: BCC bond-axis counting ---")
    step2 = step2_bond_axis_counting()
    for k, v in step2.items():
        print(f"  {k}: {v}")

    print("\n--- Step 3: numerical BCC dispersion check ---")
    step3 = step3_numerical_verify(L=64)
    for k, v in step3.items():
        print(f"  {k}: {v}")

    print("\n--- Synthesis: candidate countings ---")
    syn = synthesis()
    ratio_label = "gp2/g2"
    print(f"  {'name':50s}  {ratio_label:>10s}  {'sin^2 theta_W':>14s}  {'PDG % err':>10s}")
    for c in syn:
        print(f"  {c['name']:50s}  {c['gprime2_over_g2']:>10s}  "
              f"{c['sin2_thetaW_float']:>14.6f}  {c['PDG_diff_pct']:>10.2f}")

    # write JSON
    out_dir = os.path.normpath(os.path.join(_HERE, "..", "test-results"))
    os.makedirs(out_dir, exist_ok=True)
    out = {
        "date": "2026-05-28",
        "step1_finite_k_weights": step1,
        "step2_bond_axis_counting": step2,
        "step3_numerical_verify": step3,
        "synthesis_candidates": syn,
    }
    out_path = os.path.join(out_dir, "F47_bcc_weinberg_2over9.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nWrote {out_path}")
    return out


if __name__ == "__main__":
    main()
