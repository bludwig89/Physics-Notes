"""
hypercharge_fork.py — Higgs-free hypercharge fork + Majorana branch
====================================================================
2026-05-26 - 17:45  F41 hypercharge fork (lepton sector, Y1–Y7)
2026-05-27 - 09:00  F42 quark + dynamical χ kinetic (Y8–Y14)
2026-05-28 - 14:00  F43 Majorana branch for ν_R (M1–M6, see-saw test)

Status
------
F41 was promoted to `ca-simulation/ca_hypercharge.py` after 7/7
verification.  F42 extended that production file in-place.  This fork
file is the **experimental staging area** for the next layer.  It
re-exports the production primitives from `ca_hypercharge` so callers
treat the fork as a drop-in superset, then adds:

    F43  →  bare Majorana mass step for the right-handed neutrino ν_R
            and the analytic see-saw mass operator.

If F43 verifies cleanly, the Majorana primitives are eligible for
promotion to `ca_hypercharge.py` (or a sibling `ca_majorana.py`).

F43 — Majorana extension (2026-05-28)
-------------------------------------
The right-handed neutrino carries Y_ν_R = 0 in the Standard Model.
This is the unique hypercharge assignment for which a Majorana mass

    L_M  =  −½ M_R ( ν_R^T ε ν_R  +  h.c. ),     ε = i σ²

is U(1)_Y-invariant — the bilinear ν_R^T ε ν_R carries hypercharge
2 Y_ν_R, which only vanishes at Y = 0.  In the SM this selection rule
is enforced by U(1)_Y; here, in the Higgs-free Dirac CA, it follows
from exactly the same U(1)_Y gauge constraint, with **no Higgs field
anywhere in the construction**.

Combined with the F27/F41 Dirac mass M_D from the η ↔ χ coupling, the
(ν_L, ν_R^c) mass matrix takes the canonical see-saw form

        M  =  [[ 0 ,   M_D ],
               [ M_D,  M_R ]]

with eigenvalues  λ_± = (M_R ± √(M_R² + 4 M_D²)) / 2.   In the limit
M_R ≫ M_D:

    light: |λ_-| = (√(M_R²+4M_D²) − M_R) / 2  →  M_D² / M_R
    heavy: |λ_+| =                              →  M_R + M_D²/M_R

That is the see-saw I mechanism, here arising without a Higgs.  The
Dirac mass M_D is set by the F27 chiral-SU(2)_L step (gauge-frozen),
the Majorana mass M_R is set by a *bare* singlet self-coupling allowed
only because Y_ν_R = 0.  The hierarchy m_ν ≪ m_e is then a consequence
of a single large scale M_R, not of an unnaturally small Yukawa
coupling.

What this module adds
---------------------
1. `mass_step_majorana_chi(chi_u, chi_d, M_R, dt)` — bare Majorana mass
   step on a single 2-component Weyl singlet.  Anti-linear in χ
   (couples χ to χ*).  R-unitary on the 4 real DOFs.

2. `mass_step_dirac_majorana_nu(eta_u, eta_d, chi_u, chi_d,
                                M_D, M_R, dt)` — Strang-split
   Majorana(dt/2) ∘ Dirac(dt) ∘ Majorana(dt/2) on the ν sector, used
   for the see-saw eigenvalue extraction (no SU(2)_L, no kinetic).

3. Analytic see-saw mass operator:
       `seesaw_2x2_matrix(M_D, M_R)`
       `seesaw_eigenvalues(M_D, M_R)`             — exact closed form
       `seesaw_light_mass_approx(M_D, M_R)`       — leading order M_D²/M_R

4. `bdg_hamiltonian_nu(M_D, M_R)` — 8×8 BdG-form Hermitian effective
   Hamiltonian on the (ν_L, ν_R, ν_L*, ν_R*) extended space, derived
   directly from the dt → 0 limit of the combined Dirac+Majorana mass
   step in this file.  Its spectrum doubles the 2×2 see-saw spectrum
   (each physical mass appears with its ±-partner from the doubling
   plus a spin-↑/↓ degeneracy).

What the M-tests verify
-----------------------
M1  Bare Majorana step preserves |χ_u|² + |χ_d|² exactly (R-unitarity).
M2  Bare Majorana step is invariant under U(1)_Y with Y_ν_R = 0
    (the SM ν_R assignment) — the Higgs-free realisation of the
    standard selection rule.
M3  Bare Majorana step is NOT invariant for Y_ν_R ≠ 0 — residual
    scales as |sin(β Y/2)| · M_R · ‖χ‖, hence non-zero.  This *is*
    the selection rule.
M4  BdG infinitesimal extraction: in the dt → 0 limit, the per-cell
    Jacobian of `mass_step_dirac_majorana_nu` reproduces
    `bdg_hamiltonian_nu(M_D, M_R)` to machine precision.
M5  Analytic see-saw eigenvalues equal (M_R ± √(M_R²+4M_D²))/2 to
    machine precision (closed form, no approximation).
M6  See-saw scaling: across the ratio sweep M_R/M_D ∈ {3 … 10⁵},
    light eigenvalue · M_R / M_D² → 1 with residual O((M_D/M_R)²).
    This is the natural Higgs-free explanation for the smallness of
    the active neutrino mass.

References
----------
F27  chiral SU(2)              — findings/F27-complex-mass-chiral-su2.md
F41  hypercharge fork          — findings/F41-hypercharge-higgs-free-su2.md
F42  quark + dyn-χ kinetic     — findings/F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md
ca_hypercharge.mass_step_doublet_su2xu1y   — Dirac side of the see-saw
"""

from __future__ import annotations
import numpy as np

# Re-export the production primitives so the fork file is a drop-in
# superset of the promoted `ca_hypercharge` module.
from ca_hypercharge import (        # noqa: F401
    Y_LEPTON_L, Y_E_R, Y_NU_R, DELTA_Y_E, DELTA_Y_NU,
    Y_QUARK_L, Y_U_R, Y_D_R, DELTA_Y_U, DELTA_Y_D,
    make_u1y_field,
    mass_step_doublet_su2xu1y,
    mass_step_quark_doublet_su2xu1y,
    apply_u1y_transform,
    apply_u1y_transform_quark,
    apply_u1y_transform_chi,
    u1y_shift_alpha,
    covariant_phase_per_chirality,
    kinetic_half_step_chi_u1y,
    kinetic_half_step_chi_singlets_all,
)


# ══════════════════════════════════════════════════════════════════════
#  F43 — Bare Majorana mass step on the right-handed neutrino ν_R
# ══════════════════════════════════════════════════════════════════════
def mass_step_majorana_chi(chi_u, chi_d, M_R, dt=1.0):
    """
    Bare Majorana mass step for a single 2-component Weyl singlet (ν_R).

    The Majorana bilinear

        L_M  =  −½ M_R ( χ^T ε χ  +  h.c. ),     ε = i σ²

    gives the one-particle BdG-form EOM

        i ∂_t χ_u  =  + M_R χ_d*
        i ∂_t χ_d  =  − M_R χ_u*

    Closed-form integration over a finite step dt:

        χ_u'  =  c_M χ_u  −  i s_M χ_d*
        χ_d'  =  c_M χ_d  +  i s_M χ_u*

    with c_M = cos(M_R·dt), s_M = sin(M_R·dt).

    Properties
    ----------
    • R-unitary:  |χ_u'|² + |χ_d'|²  =  |χ_u|² + |χ_d|²  exactly
      (verified algebraically in the docstring of `_majorana_norm_check`
      and numerically by test M1).
    • U(1)_Y invariant iff Y_χ = 0  (the SM ν_R assignment).  For any
      Y ≠ 0 the bilinear χ^T ε χ carries charge 2Y and is forbidden by
      U(1)_Y.  See tests M2 / M3.
    • Anti-linear: the step is R-linear (not C-linear) because of the
      χ*.  This is intrinsic to Majorana mass and is the source of
      lepton-number violation.
    • dt → 0 limit gives `bdg_hamiltonian_nu(0, M_R)` exactly.
    """
    c_M = np.cos(M_R * dt)
    s_M = np.sin(M_R * dt)
    chi_u_new = c_M * chi_u - 1j * s_M * np.conj(chi_d)
    chi_d_new = c_M * chi_d + 1j * s_M * np.conj(chi_u)
    return chi_u_new, chi_d_new


# ══════════════════════════════════════════════════════════════════════
#  Combined Dirac + Majorana ν-sector mass step
#  (single isospin, U = I, Y_ν_R = 0 — the see-saw probe step)
# ══════════════════════════════════════════════════════════════════════
def mass_step_dirac_majorana_nu(eta_u, eta_d, chi_u, chi_d,
                                M_D, M_R, dt=1.0):
    """
    Strang-split mass step on the ν sector:

        S(dt)  =  Majorana(dt/2)  ∘  Dirac(dt)  ∘  Majorana(dt/2)

    This is the *mass-only* step (no SU(2)_L gauge factor, no kinetic
    propagator) used to verify see-saw eigenvalue scaling, BdG
    Hamiltonian consistency, and unitarity of the combined operator.

    The Dirac sub-step is F27 with U = I:

        η_new = c_D η  +  i s_D χ
        χ_new = c_D χ  +  i s_D η

    The Majorana sub-step is `mass_step_majorana_chi`.

    Parameters
    ----------
    eta_u, eta_d : ν_L spinor    (Lx, Ly)  complex
    chi_u, chi_d : ν_R spinor    (Lx, Ly)  complex
    M_D          : Dirac mass    (η ↔ χ coupling)
    M_R          : Majorana mass on χ
    dt           : time step

    Returns
    -------
    eta_u, eta_d, chi_u, chi_d — updated arrays.
    """
    # Majorana half-step on χ
    chi_u, chi_d = mass_step_majorana_chi(chi_u, chi_d, M_R, 0.5 * dt)
    # Dirac full step  (F27 sign convention)
    c_D = np.cos(M_D * dt)
    s_D = np.sin(M_D * dt)
    eu_n = c_D * eta_u + 1j * s_D * chi_u
    ed_n = c_D * eta_d + 1j * s_D * chi_d
    xu_n = c_D * chi_u + 1j * s_D * eta_u
    xd_n = c_D * chi_d + 1j * s_D * eta_d
    eta_u, eta_d, chi_u, chi_d = eu_n, ed_n, xu_n, xd_n
    # Majorana half-step on χ
    chi_u, chi_d = mass_step_majorana_chi(chi_u, chi_d, M_R, 0.5 * dt)
    return eta_u, eta_d, chi_u, chi_d


# ══════════════════════════════════════════════════════════════════════
#  Analytic see-saw mass operator (2×2 in the (ν_L, ν_R^c) basis)
# ══════════════════════════════════════════════════════════════════════
def seesaw_2x2_matrix(M_D, M_R):
    """
    Canonical 2×2 see-saw mass matrix in the (ν_L, ν_R^c) basis:

        M  =  [[ 0 ,   M_D ],
               [ M_D,  M_R ]]

    Its eigenvalues are the physical neutrino masses.  Real symmetric.
    """
    return np.array([[0.0, M_D],
                     [M_D, M_R]], dtype=float)


def seesaw_eigenvalues(M_D, M_R):
    """
    Closed-form eigenvalues of the 2×2 see-saw matrix:

        λ_±  =  (M_R  ±  √(M_R² + 4·M_D²)) / 2

    Returns `(lam_light, lam_heavy)` where |lam_light| ≤ |lam_heavy|.

    Sign of lam_light: −M_D²/M_R + O((M_D/M_R)⁴) in the see-saw limit
    (the active neutrino acquires its sign from the off-diagonal term).

    Numerical note
    --------------
    The raw form  (M_R − √(M_R²+4M_D²))/2  suffers catastrophic
    cancellation for M_R ≫ M_D.  We always compute one root from the
    explicit formula and the other via Vieta — for a real-symmetric
    2×2 with trace M_R and det −M_D² we have

        λ_+ · λ_-  =  −M_D²     and     λ_+ + λ_-  =  M_R.

    So whichever root is the *non-cancelling* one is computed directly
    and the other is recovered as `−M_D² / (the first root)`.  This is
    machine-precision exact across all ratios M_R/M_D we sweep in M6.
    """
    disc = float(np.sqrt(M_R * M_R + 4.0 * M_D * M_D))
    # Non-cancelling branch of the quadratic formula:
    if M_R >= 0.0:
        # λ_+ = (M_R + disc)/2  is large and well-conditioned.
        lam_plus  = 0.5 * (M_R + disc)
        # λ_- = -M_D² / λ_+  via Vieta (avoids cancellation).
        lam_minus = -(M_D * M_D) / lam_plus if lam_plus != 0.0 else 0.0
    else:
        # M_R < 0: λ_- = (M_R - disc)/2 is large negative, λ_+ is small.
        lam_minus = 0.5 * (M_R - disc)
        lam_plus  = -(M_D * M_D) / lam_minus if lam_minus != 0.0 else 0.0
    if abs(lam_minus) <= abs(lam_plus):
        return lam_minus, lam_plus
    return lam_plus, lam_minus


def seesaw_light_mass_approx(M_D, M_R):
    """
    Leading-order see-saw approximation:  m_ν  ≈  M_D² / M_R  (M_R ≫ M_D).
    """
    return (M_D * M_D) / M_R


# ══════════════════════════════════════════════════════════════════════
#  BdG-form effective Hamiltonian on the ν sector
# ══════════════════════════════════════════════════════════════════════
def bdg_hamiltonian_nu(M_D, M_R):
    """
    8×8 Hermitian BdG Hamiltonian for the (ν_L, ν_R) sector with both
    Dirac (M_D) and Majorana (M_R) mass terms.  No kinetic, no SU(2)_L.

    State ordering (8 complex DOFs, with constraint z[i+4] = z[i]*):

        z = (η_u, η_d, χ_u, χ_d,   η_u*, η_d*, χ_u*, χ_d*)

    The matrix is built from the EOM dictated by the dt → 0 limit of
    `mass_step_dirac_majorana_nu` (F27 sign convention):

        i ∂_t η_u  =  − M_D χ_u                       (Dirac, F27 sign)
        i ∂_t η_d  =  − M_D χ_d
        i ∂_t χ_u  =  − M_D η_u  +  M_R χ_d*          (+ Majorana)
        i ∂_t χ_d  =  − M_D η_d  −  M_R χ_u*

    H decomposes into two independent 4×4 blocks:
        Block A on indices {0, 2, 7, 5}  =  {η_u, χ_u, χ_d*, η_d*}
        Block B on indices {1, 3, 6, 4}  =  {η_d, χ_d, χ_u*, η_u*}
    Each block has eigenvalues  (±M_R ± √(M_R²+4M_D²))/2 — the see-saw
    spectrum.  So the 8 eigenvalues of H are the see-saw 4 eigenvalues
    each doubled (spin degeneracy).

    Returns
    -------
    H : (8, 8) complex Hermitian numpy array
    """
    H = np.zeros((8, 8), dtype=complex)
    # ── Dirac couplings (F27 sign:  i ∂_t η = − M_D χ) ──
    H[0, 2] = -M_D;  H[2, 0] = -M_D            # η_u ↔ χ_u
    H[1, 3] = -M_D;  H[3, 1] = -M_D            # η_d ↔ χ_d
    H[4, 6] = +M_D;  H[6, 4] = +M_D            # η_u* ↔ χ_u*
    H[5, 7] = +M_D;  H[7, 5] = +M_D            # η_d* ↔ χ_d*
    # ── Majorana couplings on χ ──
    H[2, 7] = +M_R;  H[7, 2] = +M_R            # χ_u ↔ χ_d*
    H[3, 6] = -M_R;  H[6, 3] = -M_R            # χ_d ↔ χ_u*
    return H


def bdg_spectrum_nu(M_D, M_R):
    """
    Eigenvalues of `bdg_hamiltonian_nu(M_D, M_R)`, sorted by |λ|.

    Returns
    -------
    w : (8,) real array of mass eigenvalues, sorted by absolute value.

    In the see-saw limit M_R ≫ M_D, the four smallest |λ| come out as
    a doublet of ±(√(M_R²+4M_D²) − M_R)/2  ≈  ±M_D²/M_R (light), and
    the four largest as a doublet of ±(√(M_R²+4M_D²) + M_R)/2  ≈  ±M_R.
    """
    H = bdg_hamiltonian_nu(M_D, M_R)
    w = np.linalg.eigvalsh(H)
    idx = np.argsort(np.abs(w))
    return w[idx].real
