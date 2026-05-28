"""
ca_hypercharge.py  —  U(1)_Y hypercharge gauging on the F27 chiral-SU(2)
                      Higgs-free Dirac CA
========================================================================
2026-05-26 - 17:45  — F41 lepton-sector mass step (Y1–Y7)
2026-05-27 - 09:00  — F42 quark-sector mass step + dynamical χ kinetic
                      (Y8–Y14)

Status: promoted from `forks/hypercharge_fork.py` after 7/7 verification
(F41).  Kept in its own file (per design decision) so the chiral-mass /
Y-coupling layer stays modular and orthogonal to `ca_dirac.py` and
`ca_wmu.py`; other modules import from here.

F42 extension (2026-05-27)
--------------------------
F41 left two follow-up items:
  (a) quark-sector mass step with the same Y-extended U(x) trick,
  (b) right-handed singlets (e_R, u_R, d_R) promoted from passive
      spectators to dynamically U(1)_Y-coupled fields *in the kinetic
      step*.

For (a): the SM hypercharge assignment gives
    Y_QUARK_L = +1/3,  Y_u_R = +4/3,  Y_d_R = −2/3,
so
    ΔY_u = Y_QUARK_L − Y_u_R = −1   (conjugate-Higgs branch, same as ν)
    ΔY_d = Y_QUARK_L − Y_d_R = +1   (Higgs branch, same as e).
The Higgs-equivalent diagonal D(α) = diag(e^{+iαΔY_u/2}, e^{+iαΔY_d/2})
absorbed into U(x) is therefore *numerically identical* to the lepton
diagonal — the quark mass step inherits F41's Y-extension verbatim,
exactly as F41 §"Implications for the model" point 4 predicted.

For (b): the spectral kinetic half-step on χ is made U(1)_Y-covariant by
a site-centred Stueckelberg wrap

    χ(x)  →  e^{-iα(x)Y_R/2} χ(x)                 [gauge-fix]
    χ̃(k) →  U_W(k, dt/2) · χ̃(k)                  [exact-QCA spectral step]
    χ'(x) →  e^{+iα(x)Y_R/2} χ̃'(x)                [restore gauge frame]

This construction satisfies the U(1)_Y gauge transformation law
*exactly* (not just to first order):
    S[α+β]( e^{iβY/2} χ )  =  e^{iβY/2}  S[α](χ).
At α(x) ≡ 0 it is bit-for-bit equal to `ca_dirac._weyl_half_step_2c`,
so every existing F41/F27 test that does not switch on α still passes
unchanged.

Question this module answers
----------------------------
The Standard Model Higgs serves three roles:
  (a) Yukawa fermion masses
  (b) W/Z masses via VEV
  (c) symmetry-breaking direction for SU(2)_L × U(1)_Y → U(1)_EM
F27 replaces (a) with β-gauging (chiral SU(2)_L mass step) and F34b
replaces (b) with the Stueckelberg mechanism.  Role (c) hides a subtle
U(1)_Y interaction: the F27 mass step couples η_L (Y=−1) directly to
χ_R (Y=−2 for e_R, Y=0 for ν_R).  Under U(1)_Y the term η†χ carries a
non-trivial phase α·(Y_R − Y_L)/2 ≠ 0, so the *bare* F27 mass step is
NOT U(1)_Y-invariant.  In the SM this is absorbed by Y_Φ = +1.

Resolution implemented here
---------------------------
U(x), already a pure-gauge SU(2)_L direction in F27, is extended to
carry the Higgs hypercharge:

     U(x) → U(x) · e^{i α(x) (Y_L − Y_R)/2}                        (*)

This is the minimal change that preserves both the F27 chiral-SU(2)_L
Ward identity AND restores exact U(1)_Y invariance of the mass step,
without re-introducing a Higgs boson (U is still pure gauge in
*combined* SU(2)_L × U(1)_Y, with one extra phase d.o.f. that becomes
the longitudinal mode of the Z under Stueckelberg).

Conjugate-Higgs trick
---------------------
For e_R (Y_R = −2): Y_L − Y_R = +1   → U gets phase e^{+iα/2}
For ν_R (Y_R =  0): Y_L − Y_R = −1   → ν-branch gets phase e^{−iα/2}
                                       (conjugate-Higgs, like  iσ²Φ*)

We implement this by allowing TWO Y-phases on the mass step,
α_e(x) coupling η ↔ χ_e and α_ν(x) coupling η ↔ χ_ν, related by
α_ν = −α_e in the gauge-aligned frame (the SM's iσ²Φ* operates
on the *isospin* index, exactly).

Independent of mass step:
  • The kinetic Weyl step is Abelian-covariantised by a single
    e^{i α(x) Y/2} phase per chirality (Y_L for η, Y_R for χ).
  • SU(2)_L kinetic gauging (F34) is orthogonal — U(1)_Y phase
    commutes with SU(2)_L since both isospin components share Y_L.

What the tests verify
---------------------
Y1: U(1)_Y Ward identity, mass step alone, e_R branch
    V_Y(x) · mass(ψ; U)  ==  mass(V_Y·ψ;  V_Y·U·V_Y_R⁻¹)
    where V_Y_R is the right-sector U(1)_Y phase.
Y2: U(1)_Y Ward identity, mass step alone, ν_R branch (conjugate)
Y3: F27 reduction — with α(x)=0 (B-field identity) the mass step is
    bit-for-bit equal to the original ca_dirac.mass_step_doublet_su2.
Y4: SU(2)_L Ward identity (F27 T5) preserved with α(x) nontrivial
Y5: Kinetic step U(1)_Y covariance (Abelian phase factors out exactly)
Y6: ν-doublet field is unaffected by switching on B-links when U is
    identity (no isolated SU(2)_L breaking).
Y7: Hermiticity / unitarity of the combined SU(2)_L × U(1)_Y mass step.

References
----------
F27 chiral SU(2)         — findings/F27-complex-mass-chiral-su2.md
F35 electroweak mixing   — findings/F35-electroweak-mixing.md
ca_dirac.mass_step_doublet_su2  — base step we extend
"""

from __future__ import annotations
import numpy as np

# ca_dirac lives in the same directory now (sibling module after promotion).
import ca_dirac as _ca_dirac  # noqa: F401  — kept as a sanity-import reference


# ──────────────────────────────────────────────────────────────────────
# SM hypercharge assignment (Gell-Mann–Nishijima Q = T_3 + Y/2)
# ──────────────────────────────────────────────────────────────────────
Y_LEPTON_L = -1    # left-handed lepton doublet (ν_L, e_L)
Y_E_R      = -2    # right-handed charged lepton
Y_NU_R     =  0    # right-handed neutrino (sterile in minimal SM)

# Higgs-equivalent hypercharges absorbed into U(x):
#   ΔY_e  = Y_L − Y_e_R   = +1   (the SM Higgs hypercharge)
#   ΔY_ν  = Y_L − Y_ν_R   = −1   (conjugate Higgs, iσ²Φ*)
DELTA_Y_E  = Y_LEPTON_L - Y_E_R       # +1
DELTA_Y_NU = Y_LEPTON_L - Y_NU_R      # -1


# ──────────────────────────────────────────────────────────────────────
#  U(1)_Y field generators
# ──────────────────────────────────────────────────────────────────────
def make_u1y_field(Lx, Ly, mode='identity', seed=11):
    """
    Site-centred U(1)_Y gauge angle α(x).  Returns a real array α(x).

    The field is pure gauge: under V_Y(x) = e^{i β(x) Y/2}, α(x) → α(x) + β(x).
    """
    if mode == 'identity':
        return np.zeros((Lx, Ly), dtype=float)
    elif mode == 'random':
        rng = np.random.default_rng(seed=seed)
        return rng.uniform(-np.pi, np.pi, (Lx, Ly))
    elif mode == 'plane':
        x = np.arange(Lx)[:, None]
        y = np.arange(Ly)[None, :]
        return 0.3 * x + 0.17 * y
    else:
        raise ValueError(f"Unknown U(1)_Y mode {mode!r}")


# ──────────────────────────────────────────────────────────────────────
#  Mass step with hypercharge absorbed in U(x)
# ──────────────────────────────────────────────────────────────────────
def mass_step_doublet_su2xu1y(eta_nu_u, eta_nu_d, eta_e_u, eta_e_d,
                              chi_nu_u, chi_nu_d, chi_e_u, chi_e_d,
                              U_a, U_b, alpha,
                              m, dt=1.0,
                              delta_y_e: float = DELTA_Y_E,
                              delta_y_nu: float = DELTA_Y_NU):
    """
    Extended F27 mass step that is BOTH SU(2)_L AND U(1)_Y Ward-invariant.

    Mass coupling at each cell — per-isospin Higgs-equivalent phase:

        M = c_m·I  +  i s_m · [[ 0,           U·E_phase ],
                               [ U†·E_phase†, 0         ]]

    where  E_phase = diag(e^{+iα·ΔY_ν/2},  e^{+iα·ΔY_e/2})   acts on
    the isospin index AFTER U.  This makes the η_ν↔χ_ν and η_e↔χ_e
    couplings each Y-balanced (they absorb +ΔY_ν/2 and +ΔY_e/2 of
    hypercharge respectively, just as a Higgs (ΔY_e/2) and conjugate-
    Higgs (ΔY_ν/2 = −ΔY_e/2) would).

    Reduces to the original F27 step exactly when α(x) ≡ 0.

    Parameters
    ----------
    eta_*, chi_* : (Lx, Ly) — left- and right-handed Weyl components
                              for the (ν, e) doublet (F27 conventions).
    U_a, U_b     : (Lx, Ly) — pure-gauge SU(2)_L field, |Ua|²+|Ub|²=1.
    alpha        : (Lx, Ly) — pure-gauge U(1)_Y angle α(x).
    m, dt        :         — dimensionless mass, time step.
    delta_y_e    : Higgs hypercharge absorbed by η↔χ_e branch (+1 in SM).
    delta_y_nu   : conjugate-Higgs hypercharge for η↔χ_ν (−1 in SM).
    """
    c_m = np.cos(m * dt)
    s_m = np.sin(m * dt)
    Ua  = U_a;  Ub  = U_b
    Uac = np.conj(Ua);  Ubc = np.conj(Ub)

    # Per-branch Higgs-equivalent phases.  Sign convention: a phase of
    # +ΔY/2 sits in the η→χ direction; the conjugate sits on χ→η.
    ph_nu  = np.exp(0.5j * delta_y_nu * alpha)
    ph_e   = np.exp(0.5j * delta_y_e  * alpha)
    ph_nuc = np.conj(ph_nu)
    ph_ec  = np.conj(ph_e)

    # η_new = c_m η  +  i s_m · (U · diag(ph_nu, ph_e)) χ
    #
    # The diag(ph_nu, ph_e) factor is applied to χ before U·.  Equivalently,
    # define χ̃_ν = ph_nu·χ_ν, χ̃_e = ph_e·χ_e, then apply U.
    chi_tilde_nu_u = ph_nu * chi_nu_u
    chi_tilde_nu_d = ph_nu * chi_nu_d
    chi_tilde_e_u  = ph_e  * chi_e_u
    chi_tilde_e_d  = ph_e  * chi_e_d

    eu_nu_n = c_m * eta_nu_u + 1j * s_m * (Ua * chi_tilde_nu_u - Ubc * chi_tilde_e_u)
    ed_nu_n = c_m * eta_nu_d + 1j * s_m * (Ua * chi_tilde_nu_d - Ubc * chi_tilde_e_d)
    eu_e_n  = c_m * eta_e_u  + 1j * s_m * (Ub * chi_tilde_nu_u + Uac * chi_tilde_e_u)
    ed_e_n  = c_m * eta_e_d  + 1j * s_m * (Ub * chi_tilde_nu_d + Uac * chi_tilde_e_d)

    # χ_new = i s_m · diag(ph_nuc, ph_ec) · U† · η  +  c_m χ
    # Equivalently: η̃ = U†η, then χ_new[isospin] = i s_m · ph*_iso · η̃[iso].
    # U† · η in isospin: [Ua*, Ub*; -Ub, Ua] · (η_ν, η_e)
    Ud_eta_nu_u = Uac * eta_nu_u + Ubc * eta_e_u
    Ud_eta_nu_d = Uac * eta_nu_d + Ubc * eta_e_d
    Ud_eta_e_u  = -Ub * eta_nu_u + Ua  * eta_e_u
    Ud_eta_e_d  = -Ub * eta_nu_d + Ua  * eta_e_d

    xu_nu_n = 1j * s_m * ph_nuc * Ud_eta_nu_u + c_m * chi_nu_u
    xd_nu_n = 1j * s_m * ph_nuc * Ud_eta_nu_d + c_m * chi_nu_d
    xu_e_n  = 1j * s_m * ph_ec  * Ud_eta_e_u  + c_m * chi_e_u
    xd_e_n  = 1j * s_m * ph_ec  * Ud_eta_e_d  + c_m * chi_e_d

    return (eu_nu_n, ed_nu_n, eu_e_n, ed_e_n,
            xu_nu_n, xd_nu_n, xu_e_n, xd_e_n)


# ──────────────────────────────────────────────────────────────────────
#  Abelian U(1)_Y gauge transformation
# ──────────────────────────────────────────────────────────────────────
def apply_u1y_transform(eta_nu_u, eta_nu_d, eta_e_u, eta_e_d,
                        chi_nu_u, chi_nu_d, chi_e_u, chi_e_d,
                        beta,
                        y_lepton_L: float = Y_LEPTON_L,
                        y_e_R: float = Y_E_R,
                        y_nu_R: float = Y_NU_R):
    """
    Apply ψ → e^{i β(x) Y_ψ / 2} ψ to each Weyl field.  Returns the
    transformed 8-tuple.
    """
    phL = np.exp(0.5j * y_lepton_L * beta)
    phE = np.exp(0.5j * y_e_R      * beta)
    phN = np.exp(0.5j * y_nu_R     * beta)
    return (phL * eta_nu_u, phL * eta_nu_d, phL * eta_e_u, phL * eta_e_d,
            phN * chi_nu_u, phN * chi_nu_d, phE * chi_e_u, phE * chi_e_d)


def u1y_shift_alpha(alpha, beta):
    """
    Compensating shift of the U(x) U(1)_Y phase α(x) under V_Y(x) = e^{iβ Y/2}:
        α(x)  →  α(x) + β(x)
    so that the mass step's per-branch e^{i α ΔY/2} absorbs the field rotation.
    """
    return alpha + beta


# ──────────────────────────────────────────────────────────────────────
#  Convenience: covariant U(1)_Y phase for kinetic steps
# ──────────────────────────────────────────────────────────────────────
def covariant_phase_per_chirality(beta,
                                  y_lepton_L: float = Y_LEPTON_L,
                                  y_e_R: float = Y_E_R,
                                  y_nu_R: float = Y_NU_R):
    """
    Return (phL, phN, phE) site-centred U(1)_Y phases for the three
    chirality/charge eigenstates.  Multiplying these onto the spinor
    fields before the BCC kinetic step gauge-covariantises that step
    to first order in α (and exactly for global U(1)_Y).
    """
    return (np.exp(0.5j * y_lepton_L * beta),
            np.exp(0.5j * y_nu_R     * beta),
            np.exp(0.5j * y_e_R      * beta))


# ══════════════════════════════════════════════════════════════════════
#  F42 — Quark sector hypercharge (mass step) + dynamical χ kinetic step
#  Added 2026-05-27 - 09:00
# ══════════════════════════════════════════════════════════════════════

# ─ Standard-Model hypercharges for the first-generation quark sector ─
Y_QUARK_L =  1.0 / 3.0     # left-handed quark doublet (u_L, d_L)
Y_U_R     =  4.0 / 3.0     # right-handed up quark
Y_D_R     = -2.0 / 3.0     # right-handed down quark

# Higgs-equivalent hypercharges absorbed into U(x) for the quark mass step.
#   ΔY_u  = Y_QUARK_L − Y_u_R   = −1   (conjugate-Higgs, like the ν branch)
#   ΔY_d  = Y_QUARK_L − Y_d_R   = +1   (the SM Higgs hypercharge)
DELTA_Y_U = Y_QUARK_L - Y_U_R       # -1
DELTA_Y_D = Y_QUARK_L - Y_D_R       # +1


def mass_step_quark_doublet_su2xu1y(eta_u_u, eta_u_d, eta_d_u, eta_d_d,
                                    chi_u_u, chi_u_d, chi_d_u, chi_d_d,
                                    U_a, U_b, alpha,
                                    m, dt=1.0,
                                    delta_y_u: float = DELTA_Y_U,
                                    delta_y_d: float = DELTA_Y_D):
    """
    F41 mass-step Y-coupling extended to the (u, d) quark doublet.

    Acts on a single colour at a time — the caller is expected to loop
    over colour (see `ca_strong.quark_doublet_mass_step_su2` for the
    colour-major wrapper that uses this primitive).

    Per-cell unitary  (same algebraic form as the lepton case, swapping
    ΔY_ν → ΔY_u and ΔY_e → ΔY_d):

        M = c_m · I  +  i s_m · [[ 0,           U · D(α) ],
                                 [ D†(α) · U†,  0        ]]

    with  D(α) = diag(e^{+i α ΔY_u/2},  e^{+i α ΔY_d/2}).

    Reduces to `ca_dirac.mass_step_doublet_su2` *bit-for-bit* at
    α(x) ≡ 0 — so the F40 quark mass step (FG-2 / Q1–Q10) is preserved.

    Parameters
    ----------
    eta_u_*, chi_u_* : (Lx, Ly) — left- and right-handed up quark
    eta_d_*, chi_d_* : (Lx, Ly) — left- and right-handed down quark
    U_a, U_b         : (Lx, Ly) — pure-gauge SU(2)_L field, |Ua|²+|Ub|²=1
    alpha            : (Lx, Ly) — pure-gauge U(1)_Y angle α(x)
    m, dt            :         — dimensionless mass, time step
    delta_y_u, delta_y_d : Higgs-equivalent ΔY absorbed into the up- and
                           down-branch of U.  Defaults are the SM values
                           (−1, +1), numerically identical to (ΔY_ν, ΔY_e).
    """
    c_m = np.cos(m * dt)
    s_m = np.sin(m * dt)
    Ua  = U_a;  Ub  = U_b
    Uac = np.conj(Ua);  Ubc = np.conj(Ub)

    ph_u  = np.exp(0.5j * delta_y_u * alpha)
    ph_d  = np.exp(0.5j * delta_y_d * alpha)
    ph_uc = np.conj(ph_u)
    ph_dc = np.conj(ph_d)

    chi_tilde_u_u = ph_u * chi_u_u
    chi_tilde_u_d = ph_u * chi_u_d
    chi_tilde_d_u = ph_d * chi_d_u
    chi_tilde_d_d = ph_d * chi_d_d

    # η_new = c_m η + i s_m · (U · diag(ph_u, ph_d)) χ
    eu_u_n = c_m * eta_u_u + 1j * s_m * (Ua * chi_tilde_u_u - Ubc * chi_tilde_d_u)
    ed_u_n = c_m * eta_u_d + 1j * s_m * (Ua * chi_tilde_u_d - Ubc * chi_tilde_d_d)
    eu_d_n = c_m * eta_d_u + 1j * s_m * (Ub * chi_tilde_u_u + Uac * chi_tilde_d_u)
    ed_d_n = c_m * eta_d_d + 1j * s_m * (Ub * chi_tilde_u_d + Uac * chi_tilde_d_d)

    # χ_new = i s_m · diag(ph_uc, ph_dc) · U† · η + c_m χ
    Ud_eta_u_u = Uac * eta_u_u + Ubc * eta_d_u
    Ud_eta_u_d = Uac * eta_u_d + Ubc * eta_d_d
    Ud_eta_d_u = -Ub * eta_u_u + Ua  * eta_d_u
    Ud_eta_d_d = -Ub * eta_u_d + Ua  * eta_d_d

    xu_u_n = 1j * s_m * ph_uc * Ud_eta_u_u + c_m * chi_u_u
    xd_u_n = 1j * s_m * ph_uc * Ud_eta_u_d + c_m * chi_u_d
    xu_d_n = 1j * s_m * ph_dc * Ud_eta_d_u + c_m * chi_d_u
    xd_d_n = 1j * s_m * ph_dc * Ud_eta_d_d + c_m * chi_d_d

    return (eu_u_n, ed_u_n, eu_d_n, ed_d_n,
            xu_u_n, xd_u_n, xu_d_n, xd_d_n)


def apply_u1y_transform_quark(eta_u_u, eta_u_d, eta_d_u, eta_d_d,
                              chi_u_u, chi_u_d, chi_d_u, chi_d_d,
                              beta,
                              y_quark_L: float = Y_QUARK_L,
                              y_u_R: float = Y_U_R,
                              y_d_R: float = Y_D_R):
    """
    Apply ψ → e^{i β(x) Y_ψ / 2} ψ to each Weyl quark field.

    Returns the transformed 8-tuple in the same ordering as
    `mass_step_quark_doublet_su2xu1y`.
    """
    phL = np.exp(0.5j * y_quark_L * beta)
    phU = np.exp(0.5j * y_u_R     * beta)
    phD = np.exp(0.5j * y_d_R     * beta)
    return (phL * eta_u_u, phL * eta_u_d, phL * eta_d_u, phL * eta_d_d,
            phU * chi_u_u, phU * chi_u_d, phD * chi_d_u, phD * chi_d_d)


# ──────────────────────────────────────────────────────────────────────
#  Dynamical U(1)_Y kinetic half-step for a right-handed singlet
# ──────────────────────────────────────────────────────────────────────
def kinetic_half_step_chi_u1y(chi_u, chi_d, alpha, y_charge, dt_half):
    """
    U(1)_Y-covariant kinetic half-step for a single right-handed Weyl
    singlet (e_R, u_R, or d_R), promoting it from a passive spectator
    (F41) to a dynamically Y-coupled field.

    Construction (site-centred Stueckelberg-form wrap):

        χ̃(x) = e^{-i α(x) Y_R/2} · χ(x)            [gauge-fix to invariant frame]
        χ̃'(x) = (spectral half-step Δt/2) χ̃(x)     [exact-QCA Weyl propagator]
        χ'(x) = e^{+i α(x) Y_R/2} · χ̃'(x)          [restore physical gauge frame]

    Gauge covariance under U(1)_Y is **exact**, not just first-order:
    for any α(x), β(x),

        S[α+β]( e^{iβ Y/2} χ )  =  e^{iβ Y/2}  S[α](χ).

    Properties
    ----------
    • α(x) ≡ 0 ⇒ bit-for-bit equal to ca_dirac._weyl_half_step_2c
      (so every F27/F41 test that does not switch on α still passes).
    • Global / constant α ⇒ the per-site phase commutes with the
      spectral kinetic operator and factors out — physically unobservable
      for a single isolated field, exactly as a global U(1) phase should
      be.  (Verified in test Y13's "constant α" sub-residual.)
    • Local / varying α(x) ⇒ the spectral step propagates the gauge-
      invariant scalar χ̃; the field χ then *sees* α(x) at the wrap-around
      phases.  This is the spectral analog of a Wilson line and is the
      site-centred counterpart of F31/F34's link-based covariantisation.

    Parameters
    ----------
    chi_u, chi_d : (Lx, Ly) complex — spin (↑, ↓) of the singlet
    alpha        : (Lx, Ly) real    — U(1)_Y angle field α(x)
    y_charge     : float            — hypercharge Y (e.g. Y_E_R, Y_U_R, Y_D_R)
    dt_half      : float            — half time step

    Returns
    -------
    Updated (chi_u, chi_d).
    """
    ph_in  = np.exp(-0.5j * y_charge * alpha)
    ph_out = np.exp(+0.5j * y_charge * alpha)
    chi_u_g = ph_in * chi_u
    chi_d_g = ph_in * chi_d
    chi_u_n, chi_d_n = _ca_dirac._weyl_half_step_2c(chi_u_g, chi_d_g, dt_half)
    return ph_out * chi_u_n, ph_out * chi_d_n


def kinetic_half_step_chi_singlets_all(chi_e_u, chi_e_d,
                                       chi_u_u, chi_u_d,
                                       chi_d_u, chi_d_d,
                                       alpha, dt_half,
                                       y_e_R: float = Y_E_R,
                                       y_u_R: float = Y_U_R,
                                       y_d_R: float = Y_D_R):
    """
    Convenience: apply `kinetic_half_step_chi_u1y` to all three
    first-generation right-handed singlets (e_R, u_R, d_R) with their
    canonical hypercharges.

    Returns 6-tuple (chi_e_u, chi_e_d, chi_u_u, chi_u_d, chi_d_u, chi_d_d).
    """
    ceu_n, ced_n = kinetic_half_step_chi_u1y(chi_e_u, chi_e_d, alpha, y_e_R, dt_half)
    cuu_n, cud_n = kinetic_half_step_chi_u1y(chi_u_u, chi_u_d, alpha, y_u_R, dt_half)
    cdu_n, cdd_n = kinetic_half_step_chi_u1y(chi_d_u, chi_d_d, alpha, y_d_R, dt_half)
    return (ceu_n, ced_n, cuu_n, cud_n, cdu_n, cdd_n)


def apply_u1y_transform_chi(chi_u, chi_d, beta, y_charge):
    """Apply ψ → e^{i β(x) Y/2} ψ to a single right-handed Weyl singlet."""
    ph = np.exp(0.5j * y_charge * beta)
    return ph * chi_u, ph * chi_d
