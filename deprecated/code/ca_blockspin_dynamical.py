# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_blockspin_dynamical.py
# migrated   : 2026-07-30 - 13:53
# target     : src/casim/engine/lattice/blockspin_dynamical.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_blockspin_dynamical.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_blockspin_dynamical.py — coarse-graining the dynamical / relativistic bound
states (F132)
===============================================================================

`2026-06-11`

F131 showed the block-spin RG (F130) commutes with binding for a *smooth-well*
Schrödinger state.  This module carries the programme onto the model's actual
DYNAMICAL bound states — the F74-engine pion (F103), the deuteron (F104), and the
confined three-quark baryon (F122) — and exposes the Wilsonian distinction that
the smooth-well toy hid:

  * **Contact bound state (pion, F74/F103).**  The q̄q binding is a single-site
    contact well of depth g on the tight-binding relative lattice.  A contact
    interaction is a RELEVANT operator: under R_b the coupling must RUN
    (g_coarse ≠ g_fine) to hold the physical binding energy E_b fixed.  The flow
    is fixed by proximity to the Watson threshold g_c = 2t/W₃ (F74): the
    RG-invariant is the dimensionless ratio g/g_c, and holding it fixed predicts
    g_coarse.  Once run, E_b, the bound-state wavefunction and its size are
    reproduced on b³× fewer cells.

  * **Finite-range bound state (deuteron, F104).**  The NN force is a SMOOTH
    Yukawa/OBE potential — an irrelevant operator.  Its physical coupling is held
    fixed; coarse-graining is just decimating the radial grid, and the shallow
    halo (E_b = 2.224 MeV, very IR) is reproduced with the irrelevant O((h)²)
    discretisation error, no running.

  * **Confined three-body baryon (F122).**  The baryon is confinement-dominated
    (quark KE ≈ 0.1 % of M).  Its two binding ingredients are already proven
    RG-covariant: the string tension σ (F130-C1, relevant, eigenvalue b, physical
    V invariant) and the kinetic dispersion (F130 T1/T2).  So the baryon mass is
    an RG-invariant *string scale*: E_rel ∝ σ^{2/3} (linear-potential virial),
    carried by the C1-covariant σ.

Net picture (the elegant unification):
    relevant   couplings — confinement σ (eigenvalue b), the CONTACT coupling
               (runs, set by g/g_c);
    irrelevant operators — the LIV/lattice artifacts (b^{-n}), the deconfining
               magnetic coupling (b^{-2}), and SMOOTH finite-range potentials.
Coarse-graining reproduces every bound state once the relevant couplings are run.

Real-symmetric / Hermitian operators throughout (tight-binding, radial FD, ECG
generalised eigenproblem) — no chiral transforms, so numpy/scipy is safe
(CLAUDE.md).  Wraps `ca_meson` (F74 engine), `ca_nuclear` (deuteron),
`ca_baryon_dynamics` (ECG baryon) read-only.
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from scipy.optimize import brentq

from ca_blockspin import block_average

# Watson 3-D contact-binding integral (F74): g_c = 2t / W3.
WATSON3 = 0.5054620197

__all__ = [
    "WATSON3", "watson_gc",
    # contact (pion)
    "contact_ground", "contact_binding_energy", "contact_coarse_grain",
    # finite-range (deuteron)
    "deuteron_coarse_grain",
    # confined baryon
    "baryon_confinement_scaling", "baryon_harmonic_validation",
]


# ══════════════════════════════════════════════════════════════════
#  Contact bound state — the pion (F74/F103): the coupling RUNS
# ══════════════════════════════════════════════════════════════════
def watson_gc(t):
    """3-D contact-binding threshold g_c = 2t / W₃ (F74 Watson integral).
    A contact well binds only for g > g_c; g/g_c sets the distance above
    threshold, the RG-invariant of the contact coupling."""
    return 2.0 * t / WATSON3


def _contact_H(L, t, g):
    """3-D tight-binding relative Hamiltonian + single-site contact well −g at
    the origin (the F74 engine, parametrised in the hopping t)."""
    N = L ** 3

    def idx(x, y, z):
        return ((x % L) * L + (y % L)) * L + (z % L)

    rows, cols, vals = [], [], []
    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = idx(x, y, z)
                rows.append(i); cols.append(i); vals.append(6.0 * t)
                for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0),
                                   (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    rows.append(i); cols.append(idx(x + dx, y + dy, z + dz))
                    vals.append(-t)
    H = sp.csr_matrix((vals, (rows, cols)), shape=(N, N)).tolil()
    H[idx(0, 0, 0), idx(0, 0, 0)] += -g
    return H.tocsr()


def contact_ground(L, t, g):
    """Lowest eigenpair (E0, ψ0) of the contact relative Hamiltonian.  E0 < 0 ⇒
    bound (band bottom is 0); binding energy E_b = −E0."""
    w, v = eigsh(_contact_H(L, t, g), k=1, which="SA")
    return float(w[0]), v[:, 0]


def contact_binding_energy(L, t, g):
    """E_b = −E0 (≥ 0); 0 if unbound."""
    E0, _ = contact_ground(L, t, g)
    return max(0.0, -E0)


def _rms_radius(psi, L, spacing=1.0):
    """RMS relative radius of a lattice state (periodic distance), in physical
    units (× spacing)."""
    p = np.abs(np.asarray(psi).reshape(L, L, L)) ** 2
    p = p / p.sum()
    ax = np.arange(L)
    ax = np.minimum(ax, L - ax)            # periodic distance to origin
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    return float(spacing * np.sqrt((p * (X ** 2 + Y ** 2 + Z ** 2)).sum()))


def contact_coarse_grain(L_fine, t, g, b):
    """Coarse-grain the contact (pion) bound state by R_b and run the coupling.

    Kinetic coarse-graining (F131/F130): the physical effective mass fixes the
    coarse hopping t_coarse = t / b² (so the small-k dispersion t k² is preserved
    on the coarse spacing b).  The contact coupling is RELEVANT and must run; we
    (a) PREDICT g_coarse by holding the Watson ratio g/g_c fixed, and (b) find the
    EXACT g_coarse that reproduces the fine binding energy E_b — then check the
    two agree and that the wavefunction and size are reproduced.

    Returns a dict of the running coupling, energies, overlap and radii.
    """
    assert L_fine % b == 0
    L_c = L_fine // b
    t_c = t / b ** 2

    E0_f, psi_f = contact_ground(L_fine, t, g)
    E_b = -E0_f
    assert E_b > 0, "fine state is not bound — raise g above g_c"

    gc_f, gc_c = watson_gc(t), watson_gc(t_c)
    g_pred = (g / gc_f) * gc_c                       # hold g/g_c fixed

    # exact coarse coupling that reproduces E_b (bracket around the prediction)
    def mismatch(gc):
        return contact_binding_energy(L_c, t_c, gc) - E_b
    lo, hi = 0.5 * g_pred, 1.8 * g_pred
    # ensure a sign change (the coarse threshold is gc_c)
    lo = max(lo, gc_c * 1.0001)
    g_exact = brentq(mismatch, lo, hi, xtol=1e-6)

    E0_c, psi_c = contact_ground(L_c, t_c, g_exact)

    psi_f_blocked = block_average(np.abs(psi_f).reshape([L_fine] * 3), b).ravel()
    psi_c_abs = np.abs(psi_c).ravel()
    overlap = float(abs(psi_f_blocked @ psi_c_abs)
                    / (np.linalg.norm(psi_f_blocked) * np.linalg.norm(psi_c_abs)))

    return {
        "g_fine": g, "g_coarse_predicted": g_pred, "g_coarse_exact": g_exact,
        "coupling_ran": abs(g_exact - g) > 0.1 * g,   # the relevant-flow flag
        "g_over_gc_fine": g / gc_f, "g_over_gc_coarse": g_exact / gc_c,
        "E_b_fine": E_b, "E_b_coarse": -E0_c,
        "ground_overlap": overlap,
        "rms_fine": _rms_radius(psi_f, L_fine, 1.0),
        "rms_coarse": _rms_radius(psi_c, L_c, float(b)),   # physical units
        "n_cells_fine": L_fine ** 3, "n_cells_coarse": L_c ** 3,
    }


# ══════════════════════════════════════════════════════════════════
#  Finite-range bound state — the deuteron (F104): coupling FIXED
# ══════════════════════════════════════════════════════════════════
def deuteron_coarse_grain(N_fine, b_block, R_max=25.0, **cfg):
    """Coarse-grain the deuteron by decimating the radial grid by `b_block`
    (h → b_block·h), holding the PHYSICAL OBE couplings fixed (a smooth,
    irrelevant potential).

    `cfg` is passed to `ca_nuclear.solve_deuteron` (e.g. core='derived', b=…
    [the quark size — distinct from the block factor], sigma=True,
    sigma_g2_4pi=…).  Returns the fine/coarse E_b, deuteron radius and D-state
    probability with their relative errors — reproduced with the irrelevant
    O(h²) discretisation error, no coupling run.
    """
    import ca_nuclear as _nuc

    assert N_fine % b_block == 0
    rf = _nuc.solve_deuteron(R_max=R_max, N=N_fine, vectors=True, **cfg)
    rc = _nuc.solve_deuteron(R_max=R_max, N=N_fine // b_block, vectors=True, **cfg)
    rel = lambda a, c: abs(c - a) / max(abs(a), 1e-30)
    return {
        "E_b_fine": rf["E_b"], "E_b_coarse": rc["E_b"],
        "E_b_rel_err": rel(rf["E_b"], rc["E_b"]),
        "r_d_fine": rf["r_d"], "r_d_coarse": rc["r_d"],
        "r_d_rel_err": rel(rf["r_d"], rc["r_d"]),
        "P_D_fine": rf["P_D"], "P_D_coarse": rc["P_D"],
        "h_fine": rf["h"], "h_coarse": rc["h"],
        "bound_fine": rf["bound"], "bound_coarse": rc["bound"],
        "N_fine": N_fine, "N_coarse": N_fine // b_block,
    }


# ══════════════════════════════════════════════════════════════════
#  Confined three-body baryon (F122): mass = C1-covariant string scale
# ══════════════════════════════════════════════════════════════════
def baryon_confinement_scaling(sigmas, m=1.0, alpha_s=0.0):
    """Three-body confined ground energy vs the string tension σ.

    For a linear (confining) potential the virial fixes E_rel ∝ (σ²/m)^{1/3} ∝
    σ^{2/3}; the measured log-log slope confirms the baryon mass IS the string
    scale.  Because σ is RG-covariant (F130-C1, the physical string energy is
    invariant under R_b) the confinement-dominated baryon mass is reproduced
    under coarse-graining.  Returns (energies, slope)."""
    import ca_baryon_dynamics as _bd

    E = np.array([_bd.ground_state_relative_energy(m=m, sigma=s,
                  alpha_s=alpha_s)["E_rel_cholesky"] for s in sigmas])
    slope = float(np.polyfit(np.log(sigmas), np.log(E), 1)[0])
    return E, slope


def baryon_harmonic_validation(k=0.7, m=1.3):
    """ECG engine validation: the three-body harmonic ground energy
    E = 3√(3k/m) is reproduced by the correlated-Gaussian solver (the F122
    machine-precision self-test the coarse-graining argument rests on).
    Returns (exact, ecg, rel_err)."""
    import ca_baryon_dynamics as _bd

    exact = _bd.harmonic_ground_energy_exact(k, m)
    ecg = _bd.harmonic_ground_energy_ecg(k, m)
    return exact, ecg, abs(ecg - exact) / abs(exact)
