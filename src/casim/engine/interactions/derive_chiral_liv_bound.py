"""F327 - the chiral O(|k|^2) boost defect, converted to physical units and
confronted with the electron-sector Lorentz-violation bounds.

This is F301's recommended follow-up 1 and `docs/status/open-derivations.md`
row **L8**: F301 closed the *structure* of the finite-a Poincare defect
exactly (D_i = grad Phi, chirality-odd, coefficient -s c_lat (k_y k_z, ...))
and explicitly declined to confront it with data, because F28's GRB/AGN limit
constrains the *photon* |k|^3 term and is a different operator in a sector
with different bounds.  This module does the confrontation.

WHAT IS NOT RE-DERIVED HERE
---------------------------
D_i itself (F301, 10/10), the pairing classification that forces different
channels onto different LV orders (F91), and the even law's |k|^3 coefficient
(F246).  All three are taken as given and imported as closed forms.

THE THREE-PART RESULT
---------------------

A. **WHICH CHANNEL CARRIES IT.**  F301 gives the defect for "a single Weyl
   branch" and leaves open whether any *physical* particle rides one.  It
   does, and the reason is the mass:

     A1  The 4x4 BCC Dirac one-tick unitary D_k = [[n A_k, i m],[i m, n A_k^dag]]
         has eigenphases +-arccos(n u_+(k)), each TWO-FOLD DEGENERATE.  So a
         massive Dirac fermion carries ONE branch invariant u_s, and carries it
         SPIN-INDEPENDENTLY (both spin states get the same defect; the sign
         flips between particle and antiparticle, since u_+(k) = u_-(-k)).

     A2  Pairing the two chiralities the way the photon does - putting A_+(k)
         in the upper block and A_-(k) in the lower - is UNITARY AT m = 0 and
         NON-UNITARY FOR EVERY m != 0.  The mass term is exactly what locks a
         Dirac fermion onto a single branch.

     A3  and it is not an artifact of the i m . 1 ansatz.  For a general local
         (k-independent) unitary mass mixing D = [[n A, M],[M', n B]], unitarity
         forces M'^dag M' = m^2.1 and A^dag M = -M'^dag B, hence M = -m A V^dag B
         with M' = m V; requiring M and M' to be k-INDEPENDENT with A(0)=B(0)=1
         forces B(k) = V A(k)^dag V^dag, whose trace is tr A(k).  Same u.  QED.

     A4  The photon's escape is unavailable in principle, not just in this
         propagator: Omega_even(k) = omega_+(k/2) + omega_-(k/2) carries HALF
         the momentum on each constituent, so it is a two-quantum construction.
         An elementary one-quantum excitation has nothing to pair with.

B. **THE COEFFICIENT IN PHYSICAL UNITS.**  With E_a = hbar c / a the inverse
   lattice spacing in energy units (a = sqrt(8 pi) 3^(1/4) ell_P, F79/F107):

     E^2 = m^2 c^4 + c^2 p^2 - (2/sqrt3) (c p_x)(c p_y)(c p_z) / E_a

   - ANALYTIC in the momentum components, i.e. a genuine local dimension-5
   operator, not a non-analytic artifact.  In the Myers-Pospelov normalisation
   E^2 = p^2 + m^2 + eta p^3/M_Pl,

     eta(khat) = -(2/sqrt3) (a/ell_P) khat_x khat_y khat_z
     |eta|_max = 2 sqrt(8 pi) 3^(1/4) / 9 = 1.4661814811     (on <111>)
     E_LV,min  = M_Pl/|eta|_max = (9/2) E_a = 8.327e18 GeV   (exactly 9/2)

   The same number is the FERMION-PHOTON GROUP-VELOCITY DIFFERENCE, which is
   invariant under any momentum reparametrisation - so F301 section 4's second
   horn (close the algebra on a deformed P) does not remove it.  In SME
   language the angular function khat_x khat_y khat_z is a PURE j = 3, m = +-2
   spherical component: every other (j, m) projection is exactly zero, so the
   model predicts one nonzero nonminimal coefficient in the lattice frame.

C. **THE CONFRONTATION - THE COEFFICIENT IS OUTSIDE THE BOUND BY 7 DECADES.**
   Li & Ma (Phys. Lett. B 829 (2022) 137034, arXiv:2204.02956) use the
   1.12 +- 0.09 PeV LHAASO photon from the Crab Nebula and the absence of
   vacuum Cherenkov radiation to require E_LV^(sup) >= 9.4e25 GeV, equivalently
   |eta| <= 1.3e-7.  The model gives 8.327e18 GeV / |eta| = 1.466.

     superluminal: short by 1.13e7  = 7.05 decades
     subluminal:   short by 1.20e5  = 5.08 decades  (Crab synchrotron, 1e24 GeV)

   and the model's own vacuum-Cherenkov threshold sits at E_th ~ 13 TeV, while
   the Crab demonstrably accelerates electrons to >= 1.1 PeV.  Neither sign nor
   sky orientation escapes: the coefficient is odd under khat -> -khat and under
   particle <-> antiparticle, so a superluminal species always exists, and the
   solid-angle fraction on which |eta| falls below the bound is 6.2e-7.

   The RULER cannot absorb it either.  a would have to shrink by 1.13e7, and
   G = a^2 c^3/(8 pi sqrt3 hbar) would move by 1.27e14.

   So CL262's falsifier 1 has FIRED, and it fires on the physical assignment
   (leg A), not on F301's algebra, which is untouched.  What is excluded is
   "an elementary fermion of this model rides a single BCC chiral branch".

FREE INPUTS: zero from the model.  Two external numbers enter, both registered
and both BOUNDS rather than fitted values: E_LV_e_sup_min_GeV and
E_LV_e_sub_min_GeV.  m_e_GeV enters only the Cherenkov threshold.
"""
from __future__ import annotations

from typing import Any, Dict, List

import mpmath as mp

from casim.constants import (a_over_ellP, c_lat, ell_P_m, c_SI, hbar_SI,
                             J_per_GeV, m_e_GeV, E_crab_photon_max_GeV,
                             E_LV_e_sup_min_GeV, E_LV_e_sub_min_GeV)

__all__ = [
    "u_branch", "omega_branch", "omega_even", "eta_of_direction",
    "eta_max_closed", "E_a_GeV", "M_Planck_GeV", "check_chiral_liv_bound",
]

mp.mp.dps = 32

_R3 = mp.sqrt(3)
_C = mp.mpf(1) / _R3                      # c_lat as an mpf; cross-checked below
J_PER_GEV = J_per_GeV


# ---------------------------------------------------------------------------
# 0. the lattice, in mpmath
# ---------------------------------------------------------------------------
def u_branch(kv, s: int = 1):
    """The BCC branch invariant u_s(k) = c_x c_y c_z + s s_x s_y s_z."""
    c = [mp.cos(mp.mpf(x) * _C) for x in kv]
    sn = [mp.sin(mp.mpf(x) * _C) for x in kv]
    return c[0] * c[1] * c[2] + mp.mpf(s) * sn[0] * sn[1] * sn[2]


def _nvec(kv, s: int = 1):
    c = [mp.cos(mp.mpf(x) * _C) for x in kv]
    sn = [mp.sin(mp.mpf(x) * _C) for x in kv]
    S = mp.mpf(s)
    return (sn[0] * c[1] * c[2] - S * c[0] * sn[1] * sn[2],
            -S * c[0] * sn[1] * c[2] + sn[0] * c[1] * sn[2],
            c[0] * c[1] * sn[2] + S * sn[0] * sn[1] * c[2])


def _A(kv, s: int = 1):
    """The 2x2 BCC Weyl unitary U = u.1 - i (n.sigma)  (Paper 1 Eq. 15)."""
    u = u_branch(kv, s)
    nx, ny, nz = _nvec(kv, s)
    return mp.matrix([[u - 1j * nz, -1j * (nx - 1j * ny)],
                      [-1j * (nx + 1j * ny), u + 1j * nz]])


def _dag(M):
    return mp.matrix([[mp.conj(M[j, i]) for j in range(M.rows)]
                      for i in range(M.cols)])


def omega_branch(kv, s: int = 1, m=0):
    """omega^s(k, m) = arccos(n u_s(k)), n = sqrt(1 - m^2)  (F301 section 3.1)."""
    n = mp.sqrt(1 - mp.mpf(m) ** 2)
    return mp.acos(n * u_branch(kv, s))


def omega_even(kv):
    """The F26 even (paired-spinor photon) law: omega_+(k/2) + omega_-(k/2)."""
    h = [mp.mpf(x) / 2 for x in kv]
    return omega_branch(h, 1) + omega_branch(h, -1)


def _unit(d):
    n = mp.sqrt(sum(mp.mpf(x) ** 2 for x in d))
    return [mp.mpf(x) / n for x in d]


_DIRS = {"<111>": [1, 1, 1], "<211>": [2, 1, 1], "<321>": [3, 2, 1],
         "<110>": [1, 1, 0], "<100>": [1, 0, 0]}


# ---------------------------------------------------------------------------
# 1. the SI bridge
# ---------------------------------------------------------------------------
def E_a_GeV(a_over_lp=None) -> mp.mpf:
    """E_a = hbar c / a in GeV, with a = (a/ell_P) * ell_P."""
    r = mp.mpf(a_over_ellP if a_over_lp is None else a_over_lp)
    a_m = r * mp.mpf(ell_P_m)
    return mp.mpf(hbar_SI) * mp.mpf(c_SI) / a_m / mp.mpf(J_PER_GEV)


def M_Planck_GeV() -> mp.mpf:
    """M_Pl c^2 = hbar c / ell_P in GeV (the SAME bridge, ruler removed)."""
    return (mp.mpf(hbar_SI) * mp.mpf(c_SI) / mp.mpf(ell_P_m)
            / mp.mpf(J_PER_GEV))


def eta_of_direction(khat, a_over_lp=None) -> mp.mpf:
    """eta(khat) in the Myers-Pospelov normalisation E^2 = p^2 + m^2 + eta p^3/M_Pl."""
    r = mp.mpf(a_over_ellP if a_over_lp is None else a_over_lp)
    return -(2 / _R3) * r * khat[0] * khat[1] * khat[2]


def eta_max_closed(a_over_lp=None) -> mp.mpf:
    """|eta| on <111>: (2/sqrt3) * (a/ell_P) * 3^(-3/2) = 2 (a/ell_P) / 9."""
    r = mp.mpf(a_over_ellP if a_over_lp is None else a_over_lp)
    return 2 * r / 9


# ---------------------------------------------------------------------------
# 2. the legs
# ---------------------------------------------------------------------------
def _dirac_D(kv, m, pairing: str = "same"):
    """The 4x4 one-tick Dirac unitary, in three pairings.

    ``same``  -- the model's own (dirac_bcc.py): [[n A_+, i m], [i m, n A_+^dag]].
                 Its own module docstring already records that the A <-> A^dag
                 closure is *forced by unitarity*; F327 quotes that, it does not
                 discover it.
    ``naive`` -- the obvious escape, [[n A_+, i m], [i m, n A_-]]: put the two
                 chiralities on OPPOSITE branches with an ULTRALOCAL (k-independent)
                 mass. Unitary at m = 0, non-unitary for every m != 0.
    ``local`` -- the escape that DOES exist, found by the 2026-08-26 attack pass:
                 M = -m A_+(k) A_-(k)^dag, M' = m.1. A finite-range (trigonometric-
                 polynomial) mass mixing, exactly unitary at every m, with
                 omega(0) = arcsin m. It defeats the k-independent no-go - and
                 rescues nothing, for the two reasons legs A2c and A2d measure.
    """
    n = mp.sqrt(1 - mp.mpf(m) ** 2)
    Ap = _A(kv, 1)
    if pairing == "same":
        lower, M, Mp = _dag(Ap), 1j * mp.mpf(m) * mp.eye(2), 1j * mp.mpf(m) * mp.eye(2)
    elif pairing == "naive":
        lower, M, Mp = _A(kv, -1), 1j * mp.mpf(m) * mp.eye(2), 1j * mp.mpf(m) * mp.eye(2)
    elif pairing == "local":
        lower = _dag(_A(kv, -1))
        # M' = m.V with V = 1 (a REAL rotation, not the model's i m), which is
        # what unitarity forces once M = -m A V^dag B.
        M, Mp = -mp.mpf(m) * Ap * lower, mp.mpf(m) * mp.eye(2)
    else:
        raise ValueError(pairing)
    D = mp.zeros(4, 4)
    for i in range(2):
        for j in range(2):
            D[i, j] = n * Ap[i, j]
            D[2 + i, 2 + j] = n * lower[i, j]
            D[i, 2 + j] = M[i, j]
            D[2 + i, j] = Mp[i, j]
    return D


def _unitarity_defect(D) -> mp.mpf:
    U = _dag(D) * D
    return max(abs(U[i, j] - (1 if i == j else 0))
               for i in range(4) for j in range(4))


def _positive_phases(D):
    ev = mp.eig(D, left=False, right=False)
    return sorted(p for p in (mp.atan2(mp.im(e), mp.re(e)) for e in ev) if p > 0)


def _leading_k2(direction, branch: str):
    """(omega(k) - c_lat |k|)/|k|^2, Richardson-extrapolated in |k|."""
    uh = _unit(direction)
    law = (lambda v: omega_branch(v, 1)) if branch == "single" else omega_even
    vals = []
    for K in (mp.mpf("1e-5"), mp.mpf("1e-6")):
        kv = [K * x for x in uh]
        vals.append((law(kv) - _C * K) / K ** 2)
    return vals[1] + (vals[1] - vals[0]) / 9      # kill the O(|k|) remainder


def _group_velocity(law, kv):
    h = mp.mpf("1e-10")
    kn = mp.sqrt(sum(x ** 2 for x in kv))
    return (law([x * (1 + h) for x in kv]) - law([x * (1 - h) for x in kv])) / (2 * h * kn)


def _sky_fraction_below(eps) -> mp.mpf:
    """Solid-angle fraction of directions with |khat_x khat_y khat_z| < eps.

    Exact 1-D reduction: at fixed theta the phi-condition is
    |sin 2phi| < 2 eps / (sin^2 theta cos theta).
    """
    eps = mp.mpf(eps)

    def f(th):
        d = mp.sin(th) ** 2 * mp.cos(th)
        if abs(d) < mp.mpf("1e-40"):
            return mp.mpf(1)
        t = 2 * eps / abs(d)
        return mp.mpf(1) if t >= 1 else (2 / mp.pi) * mp.asin(t)

    return mp.quad(lambda th: mp.sin(th) * f(th) / 2, [0, mp.pi / 2, mp.pi])


def _ylm_identity_residual(n: int = 8) -> mp.mpf:
    """Worst pointwise residual of the exact spherical-harmonic identity

        khat_x khat_y khat_z = i sqrt(2 pi/105) ( Y_{3,-2} - Y_{3,2} ).

    A POINTWISE identity is stronger than a set of projections and costs two
    special-function calls instead of 49 two-dimensional quadratures: if the
    angular function IS a combination of (3,-2) and (3,2) alone, orthonormality
    makes every other (j, m) projection exactly zero with nothing left to
    integrate.  The physical content is that the model's dimension-5 anisotropy
    is a single SME spherical coefficient in the lattice frame - no isotropic
    (j = 0) piece, no dipole, no j = 2, and no other m within j = 3.
    """
    C = mp.sqrt(2 * mp.pi / 105)
    worst = mp.mpf(0)
    for i in range(n):
        th = mp.pi * (i + mp.mpf("0.5")) / n
        ph = 2 * mp.pi * mp.mpf(i * 7 % n + mp.mpf("0.3")) / n
        st, ct = mp.sin(th), mp.cos(th)
        f = st * mp.cos(ph) * st * mp.sin(ph) * ct
        g = 1j * C * (mp.spherharm(3, -2, th, ph) - mp.spherharm(3, 2, th, ph))
        worst = max(worst, abs(f - g))
    return worst


def summary(branch: str = "single", ruler: str = "f232") -> Dict[str, Any]:
    """Every quantity the checks read.  `branch`/`ruler` are the control knobs."""
    if branch not in ("single", "paired"):
        raise ValueError("branch must be 'single' (the model's fermion) or "
                         "'paired' (the control: the photon's even law)")
    if ruler == "f232":
        a_lp = mp.mpf(a_over_ellP)
    elif ruler == "tuned":
        # the control: shrink the ruler until eta sits a decade BELOW the bound
        a_lp = mp.mpf(a_over_ellP) / mp.mpf("1e8")
    else:
        raise ValueError("ruler must be 'f232' or 'tuned'")

    out: Dict[str, Any] = {"branch": branch, "ruler": ruler}
    out["a_over_ellP_used"] = a_lp
    out["E_a_GeV"] = E_a_GeV(a_lp)
    out["M_Planck_GeV"] = M_Planck_GeV()

    # -- A1: the 4x4 Dirac eigenphases ------------------------------------
    kv = [mp.mpf("0.31"), mp.mpf("0.72"), mp.mpf("-0.53")]
    a1 = []
    for m in ("0.3", "0.7"):
        ph = sorted(mp.atan2(mp.im(e), mp.re(e))
                    for e in mp.eig(_dirac_D(kv, m, "same"), left=False,
                                    right=False))
        w = omega_branch(kv, 1, m)
        a1.append(max(abs(ph[0] + w), abs(ph[1] + w), abs(ph[2] - w),
                      abs(ph[3] - w)))
    out["A1_eigenphase_residual"] = max(a1)

    # -- A2: the ULTRALOCAL branch-paired ansatz is non-unitary for m != 0 --
    out["A2_pairing_unitarity_violation"] = {
        m: _unitarity_defect(_dirac_D(kv, m, "naive"))
        for m in ("0", "1e-3", "0.3", "0.7")}

    # -- A2b: a LOCAL (k-dependent) mixing DOES escape that no-go -----------
    # Found by the 2026-08-26 attack pass. M = -m A_+(k) A_-(k)^dag is a
    # finite-range mass mixing, exactly unitary at every m, with the correct
    # rest phase arcsin(m). So the k-independent theorem below is NOT a
    # theorem about local mass terms, and F327 says so rather than hiding it.
    out["A2b_local_pairing_unitarity"] = {
        m: _unitarity_defect(_dirac_D(kv, m, "local"))
        for m in ("0", "1e-3", "0.3", "0.7")}
    out["A2b_rest_phase_dev"] = abs(
        _positive_phases(_dirac_D([mp.mpf("1e-9")] * 3, "0.3", "local"))[0]
        - mp.asin(mp.mpf("0.3")))

    # -- A2c: ...but its mass is not a Lorentz-scalar mass ------------------
    # A Dirac mass shifts an ultrarelativistic energy by m^2/(2c|k|). This
    # construction shifts it by ~0.4 m, LINEARLY and with OPPOSITE SIGNS on the
    # two states: an axial, chirality-odd, CPT-odd mass-like LV term, not a
    # mass. Its continuum limit is not E^2 = m^2 + c^2 p^2.
    uh = _unit(_DIRS["<111>"])
    K = mp.mpf("1e-4")
    kk = [K * x for x in uh]
    p0 = _positive_phases(_dirac_D(kk, "0", "local"))
    lin, dirac = [], []
    for m in ("1e-7", "1e-6"):
        pm = _positive_phases(_dirac_D(kk, m, "local"))
        lin.append(abs(pm[0] - p0[0]) / mp.mpf(m))                 # ~const if linear
        pred = mp.mpf(m) ** 2 / (2 * _C * K)
        dirac.append(abs((omega_branch(kk, 1, m)
                          - omega_branch(kk, 1, 0)) / pred - 1))
    out["A2c_local_mass_is_linear"] = abs(lin[1] / lin[0] - 1)      # -> 0
    out["A2c_local_shift_per_m"] = lin[1]
    out["A2c_model_dirac_is_quadratic"] = max(dirac)                # -> 0

    # -- A2d: and even granting it, it SPLITS b2 instead of cancelling it ---
    ext = []
    for Kv in (mp.mpf("1e-5"), mp.mpf("1e-6")):
        ph = _positive_phases(_dirac_D([Kv * x for x in uh], "0", "local"))
        ext.append([(q - _C * Kv) / Kv ** 2 for q in ph])
    split = [ext[1][i] + (ext[1][i] - ext[0][i]) / 9 for i in (0, 1)]
    b2c = -uh[0] * uh[1] * uh[2] / 3
    out["A2d_split_b2"] = split
    out["A2d_split_dev"] = max(abs(split[0] - b2c), abs(split[1] + b2c))
    out["A2d_sum_not_zero"] = abs(split[1] - split[0])

    # -- A3: no k-INDEPENDENT unitary mass mixing escapes -------------------
    # Stated honestly: the algebraic core is trace cyclicity, which holds for
    # any matrices. The PHYSICS is the second number - tr A_s = 2 u_s is real,
    # so conj(tr A) = tr A, and u_+ != u_- - which is what makes the identity
    # bite here rather than being vacuous.
    th = mp.mpf("0.9")
    V = mp.matrix([[mp.cos(th), -mp.sin(th)], [mp.sin(th), mp.cos(th)]])
    B = V * _dag(_A(kv, 1)) * _dag(V)
    trA = _A(kv, 1)[0, 0] + _A(kv, 1)[1, 1]
    out["A3_trace_residual"] = abs((B[0, 0] + B[1, 1]) - trA)
    out["A3_trace_is_real"] = abs(mp.im(trA))
    out["A3_branch_trace_gap"] = abs(2 * u_branch(kv, -1) - 2 * u_branch(kv, 1))

    # -- A4: the even law is a two-quantum construction -------------------
    a4, a4raw = {}, {}
    for lbl in ("<111>", "<211>", "<321>"):
        uh = _unit(_DIRS[lbl])
        v = []
        for K in (mp.mpf("1e-4"), mp.mpf("1e-5")):
            kk = [K * x for x in uh]
            v.append((omega_even(kk) - omega_branch(kk, 1)) / K ** 2)
        ext = v[1] + (v[1] - v[0]) / 9          # remove the O(|k|) remainder
        a4[lbl] = abs(ext - uh[0] * uh[1] * uh[2] / 3)
        a4raw[lbl] = (abs(v[0] - uh[0] * uh[1] * uh[2] / 3),
                      abs(v[1] - uh[0] * uh[1] * uh[2] / 3))
    out["A4_universality_gap_residual"] = max(a4.values())
    # order check: the un-extrapolated residual must fall 10x per 10x in |k|
    out["A4_order_ratio"] = max(abs(r[0] / r[1] / 10 - 1) for r in a4raw.values())

    # -- B1/B2: the closed form, per direction ----------------------------
    b = {}
    b1order = []
    for lbl, dd in _DIRS.items():
        uh = _unit(dd)
        meas = _leading_k2(dd, branch)
        # order check, the same discipline A4 carries: the UN-extrapolated
        # residual must fall 10x per 10x in |k|, so the agreement is a
        # convergence and not a choice of |k|.
        if branch == "single" and abs(uh[0] * uh[1] * uh[2]) > mp.mpf("1e-6"):
            cl = -uh[0] * uh[1] * uh[2] / 3
            r = []
            for K in (mp.mpf("1e-4"), mp.mpf("1e-5")):
                kk = [K * x for x in uh]
                r.append(abs((omega_branch(kk, 1) - _C * K) / K ** 2 - cl))
            b1order.append(abs(r[0] / r[1] / 10 - 1))
        closed = (-uh[0] * uh[1] * uh[2] / 3) if branch == "single" else mp.mpf(0)
        b[lbl] = {"khat_xyz": uh[0] * uh[1] * uh[2],
                  "b2_measured": meas, "b2_closed": closed,
                  "b2_abs_dev": abs(meas - closed),
                  "eta": (eta_of_direction(uh, a_lp) if branch == "single"
                          else mp.mpf(0))}
    out["B_by_direction"] = b
    out["B1_b2_worst_abs_dev"] = max(v["b2_abs_dev"] for v in b.values())
    out["B1_order_ratio"] = max(b1order) if b1order else mp.mpf(0)

    # B1b: the Cartesian dimension-5 operator, DIRECTION-DIFFERENCED so that
    # every isotropic term - including the F301 3.6 rho(m) velocity
    # renormalisation - cancels exactly and only the anisotropy survives:
    #     3[omega(K u1, m)^2 - omega(K u100, m)^2]
    #        = -(2/sqrt3) (K u1)_x (K u1)_y (K u1)_z + O(K^4)
    # in lattice units, which is E^2 - E_rest^2 - c^2 p^2
    #        = -(2/sqrt3) (c p_x)(c p_y)(c p_z)/E_a  in SI.
    law = (lambda v, mm: omega_branch(v, 1, mm)) if branch == "single" \
        else (lambda v, mm: omega_even(v))
    u1 = _unit(_DIRS["<111>"])
    u0 = _unit(_DIRS["<100>"])
    b1b, expo, bymass = [], [], {}
    for m in ("0", "1e-4", "1e-3"):
        d = []
        for K in (mp.mpf("1e-4"), mp.mpf("1e-5")):
            k1 = [K * x for x in u1]
            k0 = [K * x for x in u0]
            d.append(3 * (law(k1, m) ** 2 - law(k0, m) ** 2))
        expo.append(mp.log(abs(d[0] / d[1])) / mp.log(10))
        if branch == "single":
            pred = [-(2 / _R3) * (K ** 3) * u1[0] * u1[1] * u1[2]
                    for K in (mp.mpf("1e-4"), mp.mpf("1e-5"))]
            r = [d[i] / pred[i] for i in (0, 1)]
            bymass[m] = r[1] + (r[1] - r[0]) / 9 - 1
            if m == "0":
                b1b.append(abs(bymass[m]))
    out["B1b_differenced_rel_dev"] = max(b1b) if b1b else mp.mpf(0)
    out["B1b_by_mass"] = {k: str(v) for k, v in bymass.items()}
    # the whole mass dependence is a relative -m^2/3: the coefficient is
    # mass-INDEPENDENT for every ultrarelativistic fermion (m_lat ~ 1.6e-22
    # for the electron, so the correction is ~8.5e-45).
    if bymass:
        out["B1b_mass_law_dev"] = max(
            abs(bymass[m] / (-mp.mpf(m) ** 2 / 3) - 1)
            for m in ("1e-4", "1e-3"))
        out["B1b_electron_m_lat"] = mp.mpf(m_e_GeV) / (_R3 * E_a_GeV(a_lp))
    else:
        out["B1b_mass_law_dev"] = mp.mpf(0)
        out["B1b_electron_m_lat"] = mp.mpf(0)
    out["B1b_exponent"] = max(expo)
    out["B1b_exponent_expected"] = mp.mpf(3 if branch == "single" else 4)

    # B2: eta from the MEASURED b_2, not from its own closed form.
    #   omega = c|k| + b_2 |k|^2  =>  eta = 2 sqrt3 (a/ell_P) b_2   (E^2 form)
    # so this leg is a real comparison: the left side is extrapolated from the
    # exact arccos dispersion, the right side is 2 (a/ell_P)/9.
    b2_111 = b["<111>"]["b2_measured"]
    out["B2_eta_max_measured"] = abs(2 * _R3 * a_lp * b2_111)
    out["B2_eta_max_closed"] = (2 * a_lp / 9 if branch == "single" else mp.mpf(0))
    out["B2_eta_max"] = out["B2_eta_max_measured"]
    out["B2_eta_max_dev"] = abs(out["B2_eta_max_measured"]
                                - out["B2_eta_max_closed"])

    # -- B3: E_LV = (9/2) E_a ---------------------------------------------
    if branch == "single" and out["B2_eta_max"] > 0:
        out["B3_E_LV_GeV"] = out["M_Planck_GeV"] / out["B2_eta_max"]
        out["B3_ratio_to_E_a"] = out["B3_E_LV_GeV"] / out["E_a_GeV"]
    else:
        out["B3_E_LV_GeV"] = mp.inf
        out["B3_ratio_to_E_a"] = mp.inf

    # -- B4: parametrisation-free (group-velocity difference) -------------
    b4 = {}
    for lbl in ("<111>", "<211>", "<321>", "<110>"):
        uh = _unit(_DIRS[lbl])
        K = mp.mpf("1e-5")
        kk = [K * x for x in uh]
        law = (lambda v: omega_branch(v, 1)) if branch == "single" else omega_even
        dv = (_group_velocity(law, kk) - _group_velocity(omega_even, kk)) / _C
        pred = ((-2 / _R3) * uh[0] * uh[1] * uh[2] * K if branch == "single"
                else mp.mpf(0))
        b4[lbl] = abs(dv - pred)
    out["B4_velocity_gap_worst_abs_dev"] = max(b4.values())
    out["B4_dv_over_c_at_unit_k"] = {k: str(v) for k, v in b4.items()}

    # -- B5: pure j = 3, m = +-2 ------------------------------------------
    out["B5_identity_residual"] = _ylm_identity_residual()
    out["B5_amplitude"] = mp.sqrt(2 * mp.pi / 105)

    # -- C: the confrontation ---------------------------------------------
    sup = mp.mpf(E_LV_e_sup_min_GeV)
    sub = mp.mpf(E_LV_e_sub_min_GeV)
    out["C_bound_sup_GeV"] = sup
    out["C_bound_sub_GeV"] = sub
    out["C_eta_bound_sup"] = out["M_Planck_GeV"] / sup
    if mp.isinf(out["B3_E_LV_GeV"]):
        out["C1_decades_short_sup"] = mp.mpf(0)
        out["C2_decades_short_sub"] = mp.mpf(0)
    else:
        out["C1_decades_short_sup"] = mp.log10(sup / out["B3_E_LV_GeV"])
        out["C2_decades_short_sub"] = mp.log10(sub / out["B3_E_LV_GeV"])

    # C3: vacuum-Cherenkov threshold  E_th = (m_e^2 M_Pl / eta)^(1/3)
    me = mp.mpf(m_e_GeV)
    if branch == "single" and out["B2_eta_max"] > 0:
        out["C3_E_th_GeV"] = (me ** 2 * out["M_Planck_GeV"]
                              / out["B2_eta_max"]) ** (mp.mpf(1) / 3)
    else:
        out["C3_E_th_GeV"] = mp.inf
    # A CONSERVATIVE floor on the parent electron energy: inverse Compton hands
    # the photon at most the electron's energy, so E_e >= E_gamma. Li & Ma's own
    # inferred parent is higher; using the photon energy understates C3's margin
    # rather than overstating it.
    out["C3_crab_electron_GeV"] = mp.mpf(E_crab_photon_max_GeV)
    out["C3_decades_below_crab"] = (
        mp.log10(out["C3_crab_electron_GeV"] / out["C3_E_th_GeV"])
        if not mp.isinf(out["C3_E_th_GeV"]) else mp.mpf(-1))

    # C4: how much of the sky evades the bound
    if branch == "single":
        eps = out["C_eta_bound_sup"] / ((2 / _R3) * a_lp)
    else:
        eps = mp.mpf(1)
    out["C4_eps_khat_xyz"] = eps
    out["C4_sky_fraction"] = _sky_fraction_below(min(eps, mp.mpf(1)))

    # C5: the photon channel at the SAME ruler is one order softer
    E_crab = mp.mpf("1.12e6")
    out["C5_fermion_dv_over_c"] = ((2 / _R3) / (3 * _R3)) * (E_crab / out["E_a_GeV"])
    # even law: MEASURE the |k|^3 coefficient from omega_even rather than
    # re-typing F246's closed form, so this leg notices if F246 ever moves.
    u111 = _unit(_DIRS["<111>"])
    c3r = []
    for K in (mp.mpf("1e-3"), mp.mpf("1e-4")):
        kk = [K * x for x in u111]
        c3r.append((omega_even(kk) - _C * K) / K ** 3)
    c3 = abs(c3r[1] + (c3r[1] - c3r[0]) / 99)      # remainder is O(|k|^2)
    out["C5_c3_measured"] = c3
    out["C5_c3_F246_closed"] = (_R3 / 216) * (mp.mpf(4) / 9)
    out["C5_c3_dev"] = abs(c3 - out["C5_c3_F246_closed"])
    out["C5_photon_dv_over_c"] = 3 * c3 / _C * (E_crab / out["E_a_GeV"]) ** 2
    out["C5_channel_ratio"] = out["C5_fermion_dv_over_c"] / out["C5_photon_dv_over_c"]

    # C6: what the ruler escape costs G  (G = a^2 c^3 / (8 pi sqrt3 hbar))
    if branch == "single" and not mp.isinf(out["B3_E_LV_GeV"]):
        shrink = sup / out["B3_E_LV_GeV"]
    else:
        shrink = mp.mpf(1)
    out["C6_a_shrink_required"] = shrink
    out["C6_G_factor"] = shrink ** 2

    return out


def check_chiral_liv_bound(branch: str = "single",
                           ruler: str = "f232") -> Dict[str, Any]:
    """Registry entry point.  Returns {'checks': [...], 'pass': bool, ...}."""
    s = summary(branch=branch, ruler=ruler)
    checks: List[Dict[str, Any]] = []

    def add(cid, desc, ok, value):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok),
                       "value": str(value)})

    # --- sanity: the module's own c_lat matches the registry --------------
    add("A0-c_lat", "module c_lat matches casim.constants",
        abs(_C - mp.mpf(c_lat)) < mp.mpf("1e-15"), abs(_C - mp.mpf(c_lat)))

    add("A1-dirac-eigenphase",
        "4x4 BCC Dirac eigenphases = +-arccos(n u_+), two-fold degenerate: a "
        "massive Dirac fermion rides ONE branch, spin-independently",
        s["A1_eigenphase_residual"] < mp.mpf("1e-20"),
        s["A1_eigenphase_residual"])

    a2 = s["A2_pairing_unitarity_violation"]
    add("A2-ultralocal-pairing-fails",
        "the ULTRALOCAL branch-paired ansatz [[nA_+,im],[im,nA_-]] is unitary at "
        "m=0 and NOT for any m != 0 (the m=0 case is block-diagonal, i.e. two "
        "independent Weyl states, not a paired one)",
        a2["0"] < mp.mpf("1e-20") and a2["1e-3"] > mp.mpf("1e-6")
        and a2["0.3"] > mp.mpf("0.1") and a2["0.7"] > mp.mpf("0.1"),
        {k: str(v) for k, v in a2.items()})

    a2b = s["A2b_local_pairing_unitarity"]
    add("A2b-local-pairing-DOES-exist",
        "a LOCAL (finite-range, k-dependent) mixing M = -m A_+(k) A_-(k)^dag IS "
        "exactly unitary at every m and has the right rest phase arcsin(m) - so "
        "the k-independent theorem A3 is NOT a theorem about local mass terms",
        max(a2b.values()) < mp.mpf("1e-20")
        and s["A2b_rest_phase_dev"] < mp.mpf("1e-8"),
        ({k: str(v) for k, v in a2b.items()}, s["A2b_rest_phase_dev"]))

    add("A2c-local-mass-is-not-a-mass",
        "...but that construction's mass enters LINEARLY and with opposite signs "
        "on the two states (an axial CPT-odd LV term), where a Lorentz-scalar "
        "Dirac mass must shift an ultrarelativistic energy by m^2/(2c|k|) - which "
        "the model's own single-branch propagator does",
        s["A2c_local_mass_is_linear"] < mp.mpf("1e-2")
        and s["A2c_local_shift_per_m"] > mp.mpf("0.1")
        and s["A2c_model_dirac_is_quadratic"] < mp.mpf("1e-3"),
        (s["A2c_local_shift_per_m"], s["A2c_local_mass_is_linear"],
         s["A2c_model_dirac_is_quadratic"]))

    add("A2d-pairing-splits-it-does-not-cancel",
        "and even granting that construction, its two positive-energy eigenstates "
        "carry b_2 = -|b_2| and +|b_2| - a SPLIT, not a cancellation - so a "
        "superluminal eigenstate survives and vacuum Cherenkov still fires. This "
        "is why the photon's escape needs a SUM inside one eigenvalue (A4).",
        s["A2d_split_dev"] < mp.mpf("1e-11")
        and s["A2d_sum_not_zero"] > mp.mpf("0.1"),
        (s["A2d_split_b2"], s["A2d_split_dev"]))

    add("A3-k-independent-mass-forces-same-u",
        "no k-INDEPENDENT unitary mass mixing escapes: unitarity forces "
        "B(k) = V A(k)^dag V^dag, and tr(V A^dag V^dag) = conj(tr A) = tr A "
        "because tr A_s = 2 u_s is REAL. The trace identity itself is cyclicity "
        "and holds for any matrices; the physics is the reality of tr A_s and "
        "the nonzero u_+ - u_- gap that make it bite.",
        s["A3_trace_residual"] < mp.mpf("1e-25")
        and s["A3_trace_is_real"] < mp.mpf("1e-25")
        and s["A3_branch_trace_gap"] > mp.mpf("1e-3"),
        (s["A3_trace_residual"], s["A3_trace_is_real"],
         s["A3_branch_trace_gap"]))

    add("A4-even-law-needs-two-quanta",
        "Omega_even(k) - omega_+(k) = +(1/3) khat_x khat_y khat_z |k|^2 "
        "(F301 3.7) and the even law carries k/2 per constituent - a "
        "one-quantum channel has nothing to pair with",
        s["A4_universality_gap_residual"] < mp.mpf("1e-10")
        and s["A4_order_ratio"] < mp.mpf("1e-3"),
        (s["A4_universality_gap_residual"], s["A4_order_ratio"]))

    add("B1-b2-closed-form",
        "leading O(|k|^2) coefficient matches the closed form for this branch "
        "over five directions, with the un-extrapolated residual verified to fall "
        "10x per 10x in |k| (so the agreement is convergence, not a choice of |k|)",
        s["B1_b2_worst_abs_dev"] < mp.mpf("1e-11")
        and s["B1_order_ratio"] < mp.mpf("1e-3"),
        (s["B1_b2_worst_abs_dev"], s["B1_order_ratio"]))

    add("B1b-cartesian-dim5-operator",
        "direction-differenced (every isotropic term, rho(m) included, cancels): "
        "E^2 - E_rest^2 - c^2 p^2 = -(2/sqrt3)(c p_x)(c p_y)(c p_z)/E_a, "
        "analytic in the momentum components and mass-independent to O(m^2) - a "
        "genuine local dimension-5 operator. Exponent 3 (chiral) vs 4 (even).",
        s["B1b_differenced_rel_dev"] < mp.mpf("1e-10")
        and abs(s["B1b_exponent"] - s["B1b_exponent_expected"]) < mp.mpf("1e-3")
        and s["B1b_mass_law_dev"] < mp.mpf("1e-2"),
        (s["B1b_differenced_rel_dev"], s["B1b_exponent"],
         s["B1b_mass_law_dev"], s["B1b_electron_m_lat"]))

    add("B2-eta-from-measured-b2",
        "eta = 2 sqrt3 (a/ell_P) b_2 evaluated on the MEASURED b_2 reproduces the "
        "closed form |eta|_max = 2 (a/ell_P)/9 = 2 sqrt(8pi) 3^(1/4)/9 on <111>",
        s["B2_eta_max_dev"] < mp.mpf("1e-11"),
        (s["B2_eta_max_measured"], s["B2_eta_max_closed"], s["B2_eta_max_dev"]))

    add("B3-E_LV-is-9-halves-E_a",
        "E_LV = M_Pl/|eta|_max = (9/2) E_a. The 9/2 is the reciprocal of the 2/9 "
        "in |eta|_max and carries NO content beyond it - the leg is here because "
        "E_LV in GeV is what the published bounds are quoted in, and it is fed by "
        "the measured b_2 through B2",
        (mp.isinf(s["B3_ratio_to_E_a"])
         or abs(s["B3_ratio_to_E_a"] - mp.mpf(9) / 2) < mp.mpf("1e-10")),
        s["B3_ratio_to_E_a"])

    add("B4-parametrisation-free",
        "the fermion-photon group-velocity difference carries the SAME eta, so "
        "no momentum redefinition removes it (F301 section 4, second horn)",
        s["B4_velocity_gap_worst_abs_dev"] < mp.mpf("1e-11"),
        s["B4_velocity_gap_worst_abs_dev"])

    add("B5-pure-j3-m2",
        "khat_x khat_y khat_z = i sqrt(2pi/105) (Y_{3,-2} - Y_{3,2}) pointwise, "
        "so the model's dimension-5 anisotropy is a SINGLE SME spherical "
        "coefficient (j,m) = (3,+-2) in the lattice frame and every other "
        "(j, m) is exactly zero",
        s["B5_identity_residual"] < mp.mpf("1e-25"),
        (s["B5_identity_residual"], s["B5_amplitude"]))

    add("C1-superluminal-excluded",
        "model E_LV is BELOW the LHAASO/Crab superluminal bound by > 5 decades",
        s["C1_decades_short_sup"] > 5, s["C1_decades_short_sup"])

    add("C2-subluminal-excluded",
        "model E_LV is BELOW the Crab-synchrotron subluminal bound by > 3 "
        "decades - so neither sign of the chirality-odd coefficient survives",
        s["C2_decades_short_sub"] > 3, s["C2_decades_short_sub"])

    add("C3-vacuum-cherenkov-threshold",
        "the model's own vacuum-Cherenkov threshold sits > 1 decade BELOW a "
        "CONSERVATIVE floor on the parent-electron energy of the observed 1.12 PeV "
        "Crab photon (inverse Compton gives E_e >= E_gamma; the inferred parent is "
        "higher, so the margin is understated)",
        s["C3_decades_below_crab"] > 1, s["C3_decades_below_crab"])

    add("C4-orientation-escape-measured",
        "the solid-angle fraction on which |eta(khat)| falls under the bound is "
        "< 1e-5, so no lattice orientation makes the sky safe",
        s["C4_sky_fraction"] < mp.mpf("1e-5"), s["C4_sky_fraction"])

    add("C5-photon-channel-is-softer",
        "at the SAME ruler and the SAME 1.12 PeV, the even-law photon's "
        "fractional velocity shift is > 1e10 times smaller than the chiral "
        "fermion's - the exclusion is channel-specific, not a blanket ruler "
        "failure",
        s["C5_channel_ratio"] > mp.mpf("1e10"), s["C5_channel_ratio"])

    add("C6-ruler-escape-costs-G",
        "absorbing the exclusion in the ruler needs a -> a/1.1e7, and "
        "G ~ a^2 then moves by > 1e13 - the ruler leg cannot give",
        (s["C6_G_factor"] < mp.mpf("1.001")
         or s["C6_G_factor"] > mp.mpf("1e13")), s["C6_G_factor"])

    n_pass = sum(1 for c in checks if c["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": len(checks),
            "pass": n_pass == len(checks),
            "branch": branch, "ruler": ruler,
            "eta_max": str(s["B2_eta_max"]),
            "E_LV_model_GeV": str(s["B3_E_LV_GeV"]),
            "E_a_GeV": str(s["E_a_GeV"]),
            "M_Planck_GeV": str(s["M_Planck_GeV"]),
            "decades_short_superluminal": str(s["C1_decades_short_sup"]),
            "decades_short_subluminal": str(s["C2_decades_short_sub"]),
            "cherenkov_threshold_GeV": str(s["C3_E_th_GeV"]),
            "sky_fraction_evading": str(s["C4_sky_fraction"]),
            "G_factor_if_ruler_rescaled": str(s["C6_G_factor"]),
            "eta_by_direction": {k: str(v["eta"])
                                 for k, v in s["B_by_direction"].items()}}


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    out = check_chiral_liv_bound()
    for c in out["checks"]:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['id']:32s} -> {c['value']}")
    print(f"\n  {out['n_pass']}/{out['n_total']} PASS")
    print(f"  |eta|_max = {out['eta_max']}   E_LV = {out['E_LV_model_GeV']} GeV")
    print(f"  short by {out['decades_short_superluminal']} decades (superluminal)")
    dest = results_path("F327_chiral_liv_bound.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("wrote", os.path.basename(dest))
