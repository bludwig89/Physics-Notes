#!/usr/bin/env python3
"""FA02 — Vacuum birefringence is exactly zero.

Falsification brief: tests/falsification/FA02-vacuum-birefringence.md

Hypothesis (parameter-free): the physical photon is the chirality-EVEN
paired-spinor object (F67/F68/F69). The two polarisations (helicities) share
one dispersion branch, so the vacuum-birefringence parameter

    eta = 0  exactly, at any lattice spacing a.

This test verifies the structural prediction three ways:

  (1) SYMBOLIC (sympy): the even-law pair rate
          Omega_pair(k) = omega+(k/2) + omega-(k/2)
      carries NO helicity argument. The F26 / photon-pair rotation step
      R(Omega_pair) is applied identically to BOTH transverse polarisations,
      so Omega_+(k) == Omega_-(k) == Omega_pair(k) by construction.
      We also confirm omega+(-k) = omega-(k) (the BCC chirality relation),
      which makes the even sum manifestly even in k.

  (2) NUMERIC ON THE LIVE PROPAGATOR (ca_photon_pair.photon_step_spectral):
      plant a +helicity (right-circular) and a -helicity (left-circular)
      eigenmode at a sweep of momenta, advance one tick through the SHIPPED
      propagator, and read off the per-tick rotation rate Omega_meas for each.
      Gate: max|Omega_+ - Omega_-| < 1e-13 for all k.

  (3) CONTRAST: the retired chiral / sigma-bilinear channel (2*omega+ vs
      2*omega-) DOES split. We confirm pair_birefringence(k) != 0 there, i.e.
      the even law is what removes the split (regression that the right object
      was retired).

CLAUDE.md caveat: no numpy/scipy chiral eigen-decomposition is pushed blind.
The helicity eigenmodes are built by hand in real arithmetic; the symbolic
leg uses sympy.
"""
import os
import sys

import numpy as np

CA = os.path.join(os.path.dirname(__file__), "..", "..", "ca-simulation")
sys.path.insert(0, os.path.abspath(CA))

import ca_photon_pair as cpp          # noqa: E402
from ca_bcc import bcc_dispersion     # noqa: E402
from ca_lattice import make_kgrid_3d  # noqa: E402

GATE = 1e-13


# ----------------------------------------------------------------------
# (1) Symbolic helicity-blindness of the even pair rate
# ----------------------------------------------------------------------
def symbolic_check():
    import sympy as sp

    kx, ky, kz = sp.symbols("kx ky kz", real=True)
    r3 = sp.sqrt(3)

    def u_of(kvecx, kvecy, kvecz, s):
        cx, cy, cz = sp.cos(kvecx / r3), sp.cos(kvecy / r3), sp.cos(kvecz / r3)
        sx, sy, sz = sp.sin(kvecx / r3), sp.sin(kvecy / r3), sp.sin(kvecz / r3)
        # u from _bcc_uvec: u = cx cy cz + s sx sy sz
        return cx * cy * cz + s * sx * sy * sz

    # omega+/-(k) = arccos(u(k, +/-1)). Chirality relation: u(-k,+1) == u(k,-1).
    u_plus_negk = u_of(-kx, -ky, -kz, +1)
    u_minus_k = u_of(kx, ky, kz, -1)
    chirality_relation = sp.simplify(u_plus_negk - u_minus_k)  # expect 0

    # Even pair rate at half-momentum: Omega_pair = acos(u(k/2,+)) + acos(u(k/2,-))
    up_half = u_of(kx / 2, ky / 2, kz / 2, +1)
    um_half = u_of(kx / 2, ky / 2, kz / 2, -1)
    Omega_pair = sp.acos(up_half) + sp.acos(um_half)

    # Evenness in k: Omega_pair(-k) - Omega_pair(k) == 0
    Omega_neg = Omega_pair.subs({kx: -kx, ky: -ky, kz: -kz})
    evenness = sp.simplify(Omega_neg - Omega_pair)  # expect 0

    return {
        "chirality_relation_u_plus_negk_minus_u_minus_k": str(chirality_relation),
        "chirality_relation_is_zero": (chirality_relation == 0),
        "Omega_pair_evenness_residual": str(evenness),
        "Omega_pair_is_even_in_k": (evenness == 0),
        "note": ("photon_step_spectral has NO helicity argument; R(Omega_pair) "
                 "is applied to both transverse polarisations identically, so "
                 "Omega_+ == Omega_- == Omega_pair structurally."),
    }


# ----------------------------------------------------------------------
# (2) Per-helicity rate measured on the SHIPPED propagator
# ----------------------------------------------------------------------
def _orthonormal_triad(khat):
    khat = np.asarray(khat, float)
    khat = khat / np.linalg.norm(khat)
    ref = np.array([1.0, 0.0, 0.0]) if abs(khat[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = ref - np.dot(ref, khat) * khat
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(khat, e1)
    return e1, e2


def _plant_circular_mode(L, m_index, khat, helicity):
    """Build a single-Fourier-mode circularly polarised (E,B) photon.

    For a transverse EM mode with B = khat x E, a circular polarisation is
    E = (e1 + i*h*e2) so that the real field is a rotating transverse vector.
    helicity h = +1 (right) / -1 (left).  Built by hand in real arithmetic:
    we set the real-space field directly as cos/sin standing components so the
    FFT bin at +m and its conjugate at -m carry the circular structure.
    """
    khat = np.asarray(khat, float)
    khat = khat / np.linalg.norm(khat)
    e1, e2 = _orthonormal_triad(khat)

    # spatial phase phi(x) = k . x with k = (2pi m / L) * khat-aligned indices.
    n = np.arange(L)
    # build k.x grid for the chosen integer mode vector m_vec
    m_vec = np.round(m_index * khat).astype(int)
    X, Y, Z = np.meshgrid(n, n, n, indexing="ij")
    phase = 2.0 * np.pi * (m_vec[0] * X + m_vec[1] * Y + m_vec[2] * Z) / L

    cosw = np.cos(phase)
    sinw = np.sin(phase)
    # Real circular E-field: E(x) = e1 cos(phase) - h e2 sin(phase)
    E = np.zeros((3, L, L, L))
    B = np.zeros((3, L, L, L))
    for a in range(3):
        E[a] = e1[a] * cosw - helicity * e2[a] * sinw
        # B = khat x E (transverse, |B|=|E|)
    khat_x_e1 = np.cross(khat, e1)
    khat_x_e2 = np.cross(khat, e2)
    for a in range(3):
        B[a] = khat_x_e1[a] * cosw - helicity * khat_x_e2[a] * sinw
    return E, B


def _measure_rate(E0, B0):
    """One tick through the shipped photon propagator; return the per-tick
    rotation angle Omega of the (E,B) pair, recovered from the field overlap.

    The propagator rotates [E;B] -> [cosO E + sinO B ; -sinO E + cosO B].
    So <E0,E1> + <B0,B1> = cosO (|E0|^2+|B0|^2) and
       <B0,E1> - <E0,B1> = sinO (|E0|^2+|B0|^2).  We recover O = atan2(sin,cos).
    """
    E1, B1 = cpp.photon_step_spectral(E0, B0)
    norm = np.sum(E0 * E0) + np.sum(B0 * B0)
    c = (np.sum(E0 * E1) + np.sum(B0 * B1)) / norm
    s = (np.sum(B0 * E1) - np.sum(E0 * B1)) / norm
    return np.arctan2(s, c)


def numeric_check(L=24):
    # sweep several momenta / directions
    khats = [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 1.0, 0.0),
        (1.0, 1.0, 1.0),
    ]
    m_indices = [1, 2, 3]
    rows = []
    max_diff = 0.0
    for khat in khats:
        for m in m_indices:
            Ep, Bp = _plant_circular_mode(L, m, khat, +1)
            Em, Bm = _plant_circular_mode(L, m, khat, -1)
            Op = _measure_rate(Ep, Bp)
            Om = _measure_rate(Em, Bm)
            d = abs(Op - Om)
            max_diff = max(max_diff, d)
            rows.append({
                "khat": list(khat), "m_index": m,
                "Omega_plus": float(Op), "Omega_minus": float(Om),
                "abs_diff": float(d),
            })
    return rows, float(max_diff)


# ----------------------------------------------------------------------
# (3) Contrast: the retired chiral / sigma-bilinear split is NONZERO
# ----------------------------------------------------------------------
def contrast_check(L=24):
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    split = cpp.pair_birefringence(KX, KY, KZ)   # 2 w+ - 2 w- (the retired split)
    # exclude k=0 where everything degenerates
    nz = np.abs(split) > 0
    return {
        "max_abs_chiral_split": float(np.max(np.abs(split))),
        "mean_abs_chiral_split_nonzero": float(np.mean(np.abs(split[nz]))) if nz.any() else 0.0,
        "split_is_nontrivial": bool(np.max(np.abs(split)) > 1e-3),
        "note": "2*omega+ - 2*omega- : the split the retired sigma-bilinear photon WOULD have.",
    }


def main():
    sym = symbolic_check()
    rows, max_diff = numeric_check(L=24)
    contrast = contrast_check(L=24)

    even_pass = (max_diff < GATE) and sym["Omega_pair_is_even_in_k"] \
        and sym["chirality_relation_is_zero"]
    contrast_ok = contrast["split_is_nontrivial"]

    verdict = "PASS" if (even_pass and contrast_ok) else "FLAGGED"

    result = {
        "symbolic": sym,
        "numeric_max_abs_diff": max_diff,
        "numeric_rows": rows,
        "contrast_sigma_bilinear": contrast,
        "gate": f"max|Omega_+ - Omega_-| < {GATE:g} AND no measured birefringence",
        "even_law_birefringence_eta": 0.0,
        "verdict": verdict,
    }
    import json
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    r = main()
    assert r["numeric_max_abs_diff"] < GATE, "even-law photon split exceeded gate!"
    assert r["symbolic"]["Omega_pair_is_even_in_k"]
    assert r["contrast_sigma_bilinear"]["split_is_nontrivial"]
    print("\nFA02 even-law photon: PASS (eta = 0 exactly)")
