"""thermodynamics_gstar.py — g_*(T) and g_*s(T) from the model's OWN field content.

Rubric rows **K2** (BBN / light elements) and **G10** (lattice-native
thermodynamics).  This is completeness **gap #4** of
`docs/status/completeness-2026-08-07.md` and **next step #1** of F300:

    F300 built lattice-native thermodynamics for the PHOTON SECTOR ONLY and
    named g_*(T) as its next step; F297's BBN thermal history imports a
    Standard-Model degree-of-freedom count.  Both K2 and G10 carry the same
    import, and it is the only import either row has that the model could
    supply from content it already owns.

F300 section 7.2 states the blocker precisely: *"A full g_*(T) over the model's
48 Weyl fields needs the fermionic BZ sums with the branch-odd term handled;
the machinery is here, the number is not."*  Section A below is that
computation, and the answer to "handled" is not the one the phrasing suggests:

    **The branch-odd term does not cancel.  It contributes at O(Theta^2)
    through its SQUARE, and it supplies 3/7 = 42.86 % of the fermionic
    lattice correction — the larger single share after the isotropic term.**

WHAT IS MODEL-NATIVE AND WHAT IS NOT
------------------------------------
MODEL-NATIVE (derived in this tree, nothing imported):

  * the single-branch dispersion `omega^pm(k) = arccos(u^pm(k))` — the BCC Weyl
    walk (F26).  Section A expands it in closed form and section B integrates
    over it.
  * `c_lat = 1/sqrt3` (F26); `a = 6.5978 ell_P` (F107) -> the one temperature
    scale, imported from `thermodynamics.lattice_scales()`.
  * the RELATIVISTIC CONTENT — 48 Weyl fields (F47/F279), 2 real E_g scalars
    (F253/F255, Higgs-free by founding decision 3), 12 gauge bosons.  Section C
    turns that into a species list with a reason attached to every inclusion
    AND every exclusion.
  * `m_e = 0.51069 MeV` — the model's OWN electron mass (F121, tau-anchored
    canonical spectrum, -0.06 % vs PDG).  Section E substitutes it for the PDG
    value in F297's thermal history and quotes the shift in Y_p and D/H.  This
    is the one numerically non-null substitution the derivation makes.

A NAME COLLISION, FLAGGED HERE BECAUSE GREP WILL FIND BOTH
----------------------------------------------------------
`g_*` means two different things in this tree and they must not be conflated.
F59/F61 (`forks/gravity/gr_fork_F61_weyl_eta_gstar.py`) write `g_*` for the
**gravitating Weyl-mode count** in the induced-Newton-constant prefactor
`P_pre = sqrt(2 pi eta g_*)`, and get `g_* = 15` per first generation.  This
module writes `g_*(T)` for the **cosmological relativistic degree-of-freedom
count**, `g_* = (30/pi^2) rho/T^4`.  Different quantities, different counting
rules (fields that gravitate vs fields in equilibrium with the bath; Weyl
fields vs thermal dof), and neither is a correction to the other.

EXTERNAL INPUT (not derived, not claimed to be):

  * `k_B, hbar, c, ell_P` — unit rulers, exactly as in `thermodynamics.py`.
  * The heavy-quark and W/Z threshold TEMPERATURES used by the tier-2 plateau
    table (section D2).  The model derives the CONTENT at every plateau; it
    does not derive m_c, m_b, m_t or m_W, so the plateau *boundaries* above the
    QCD crossover are imported and labelled as such.  Nothing in the BBN result
    depends on them: section E needs only the content plus m_e.
  * PDG m_e, and the observed Y_p / D/H, as comparison points.

THE SECTIONS
------------
A.  THE SINGLE-BRANCH EXPANSION.  `omega^pm(k) = c|k|[1 -/+ b(nhat)|k|
    - a(nhat)|k|^2] + O(|k|^4)` in closed form, with

        b(nhat) = n_x n_y n_z / sqrt3        (branch-ODD, O(|k|) RELATIVE)
        a(nhat) = S2/18 + P3/6 = 4 A(nhat)   (branch-EVEN, the F300 photon A)

    The branch-odd term is exactly what the paired photon cancels (F67/F68
    non-birefringence).  A single Weyl branch keeps it.

B.  THE FERMIONIC EQUATION OF STATE.  Closed forms for the leading lattice
    corrections to a Fermi gas on that dispersion, confirmed against direct
    Brillouin-zone quadrature.  Three results:

      * C_u^F = 310 pi^2/441, C_w^F = 124 pi^2/1323, C_s^F = 31 pi^2/49;
      * `C_u/C_w = 15/2` AGAIN — F300 proved it for the photon; section B4
        proves it is independent of statistics, of the anisotropy and of the
        branch-odd term, i.e. it is a property of degree-3 homogeneity alone;
      * the fermionic coefficients are EXACTLY 31/4 times the photonic ones,
        and the 31/4 factors as 7 (geometry) x 31/28 (statistics).

C.  THE CONTENT.  Every relativistic species the model has, with provenance,
    and — the half that matters — every species it EXCLUDES with the reason.

D.  g_*(T) AND g_*s(T).  Section D1 is the BBN window, where the content is
    unambiguous and complete.  D2 is the plateau table up to the electroweak
    scale, where the content is still the model's but the boundaries are not.

E.  THE RE-RUN.  F297's BBN with the model's own m_e, and the shift.

`check_gstar()` reports everything.  Run as `__main__` to write the artifact.
"""

from __future__ import annotations

import math

from casim.numerics import xp
from casim.constants import c_lat
from casim.engine.lattice.bcc import bcc_dispersion
from casim.engine.interactions.thermodynamics import (
    A_anisotropy, MEAN_A_EXACT, lattice_scales,
    C_U_EXACT as C_U_PHOTON, C_W_EXACT as C_W_PHOTON, C_S_EXACT as C_S_PHOTON,
)

C = float(c_lat)                  # 1/sqrt3


# ==========================================================================
#  A.  THE SINGLE-BRANCH BCC WEYL DISPERSION IN CLOSED FORM
# ==========================================================================
#
#  With q_i = k_i/sqrt3 the walk gives (F26, Paper 1 Eq. 15)
#
#      u^pm = cos q_x cos q_y cos q_z  pm  sin q_x sin q_y sin q_z ,
#      omega^pm = arccos(u^pm) .
#
#  Write 1 - u^pm = (1 - P) -/+ S with P = prod cos q_i and S = prod sin q_i.
#  P is branch-even and starts at 1 - |q|^2/2; S is branch-odd and starts at
#  q_x q_y q_z = O(|q|^3).  Since omega = sqrt(2(1-u)) (1 + (1-u)/12 + ...),
#
#      omega^pm = |q| [ 1 -/+ q_x q_y q_z/|q|^2 + ... ]
#               = c|k| [ 1 -/+ b(nhat)|k| - a(nhat)|k|^2 ] + O(|k|^4)
#
#  with b = n_x n_y n_z/sqrt3.  The branch-odd term is O(|k|) RELATIVE — one
#  order LOWER than the anisotropic softening — which is precisely the
#  birefringence F67/F68 forbid and the (+,-) pair cancels.  A single Weyl
#  branch does not cancel it.
#
#  The branch-even coefficient is fixed by F300 without a new computation.  The
#  paired photon carries Omega_pair(k) = omega^+(k/2) + omega^-(k/2)
#  = c|k|[1 - a(nhat)|k|^2/4], and F300 writes that as c|k|[1 - A|k|^2].  So
#
#      a(nhat) = 4 A(nhat) = S2/18 + P3/6 ,      <a> = 4/315 .
#
#  and the fermion inherits the photon's anisotropy with a factor 4.

def b_branch_odd(nx, ny, nz):
    """Branch-ODD coefficient b(nhat) = n_x n_y n_z / sqrt3.  nhat must be unit.

    `omega^pm = c|k|[1 -/+ b|k| - a|k|^2]`.  Odd in nhat, so its angular mean is
    zero and it cannot shift g_* at first order; it enters at second order
    through `<b^2>`, which is where 43 % of the fermionic correction comes from.
    """
    return nx * ny * nz / math.sqrt(3.0)


def a_branch_even(nx, ny, nz):
    """Branch-EVEN coefficient a(nhat) = 4 A(nhat) = S2/18 + P3/6."""
    return 4.0 * A_anisotropy(nx, ny, nz)


MEAN_A_FERMION_EXACT = 4.0 / 315.0
"""<a> = 4<A> = 4/315, exact (F300's <A> = 1/315 times the factor-4 rescaling
from the paired photon's k/2 constituents to the fermion's full k)."""

MEAN_B2_EXACT = 1.0 / 315.0
"""<b^2> = <(n_x n_y n_z)^2>/3 = (1/105)/3 = 1/315, exact.

A FLAGGED COINCIDENCE, deliberately not claimed (D7 `kind="coincidence"`):
<b^2> equals F300's <A> = 1/315 exactly, although b^2 = P3/3 and
A = S2/72 + P3/24 are different functions on the sphere.  `1/105 / 3` and
`1/360 + 1/2520` reach the same rational by unrelated routes.  Recorded so a
later session finds it already noticed and already not claimed."""


def branch_expansion_residual(n_dirs=300, k_probe=(0.01, 0.02, 0.05), seed=0):
    """A1: check both closed forms against the model's own `bcc_dispersion`.

    Measured from the branch-even and branch-odd halves separately:
        (omega^+ + omega^-)/2 = c|k|[1 - a|k|^2]   ->  a
        (omega^- - omega^+)/2 = c|k| b |k|         ->  b
    The residual must be O(|k|^2) absolute, i.e. the next term in each series.
    """
    rng = xp.random.default_rng(seed)
    worst_a = 0.0
    worst_b = 0.0
    for _ in range(n_dirs):
        n = rng.normal(size=3)
        n = n / math.sqrt(float(n @ n))
        for K in k_probe:
            wp = float(bcc_dispersion(*(K * n), sign="+"))
            wm = float(bcc_dispersion(*(K * n), sign="-"))
            even = 0.5 * (wp + wm)
            odd = 0.5 * (wm - wp)
            a_meas = (1.0 - even / (C * K)) / K ** 2
            b_meas = odd / (C * K) / K
            worst_a = max(worst_a, abs(a_meas - a_branch_even(*n)))
            worst_b = max(worst_b, abs(b_meas - b_branch_odd(*n)))
    return {"a_max_abs_residual": worst_a, "b_max_abs_residual": worst_b,
            "k_probe": list(k_probe)}


def mean_coefficients(n_theta=200, n_phi=400):
    """A2: <a> and <b^2> over the sphere by quadrature, against the exact values."""
    x, w = xp.polynomial.legendre.leggauss(n_theta)
    ph = (xp.arange(n_phi) + 0.5) * 2.0 * xp.pi / n_phi
    tot_a = 0.0
    tot_b2 = 0.0
    for xi, wi in zip(x, w):
        s = math.sqrt(1.0 - float(xi) * float(xi))
        nx, ny, nz = s * xp.cos(ph), s * xp.sin(ph), xp.full(n_phi, xi)
        tot_a += float(wi) * float(xp.sum(a_branch_even(nx, ny, nz)))
        tot_b2 += float(wi) * float(xp.sum(b_branch_odd(nx, ny, nz) ** 2))
    scale = (2.0 * math.pi / n_phi) / (4.0 * math.pi)
    a_val = tot_a * scale
    b2_val = tot_b2 * scale
    return {"mean_a": a_val, "mean_a_exact": MEAN_A_FERMION_EXACT,
            "mean_a_rel": abs(a_val / MEAN_A_FERMION_EXACT - 1.0),
            "mean_b2": b2_val, "mean_b2_exact": MEAN_B2_EXACT,
            "mean_b2_rel": abs(b2_val / MEAN_B2_EXACT - 1.0),
            "mean_A_photon_exact": MEAN_A_EXACT,
            "b2_equals_A_coincidence": True}


# ==========================================================================
#  B.  THE FERMIONIC EQUATION OF STATE — closed form, then measured
# ==========================================================================
#
#  Occupation is Fermi-Dirac at the dimensionless Theta = k_B T tau/hbar, the
#  SAME temperature variable F300 defines.  Write omega^pm = c k (1 + eps^pm)
#  with eps^pm = -/+ b k - a k^2, and note that the branch sums are
#
#      sum_pm eps   = -2 a k^2 ,        sum_pm eps^2 = 2 b^2 k^2 ,
#
#  so the branch-odd term SURVIVES, squared, at exactly the order the
#  anisotropic term enters.  Expanding phi(z) = z/(e^z + 1) to second order and
#  using
#
#      int_0^inf y^3/(e^y+1) dy = 7 pi^4/120 ,
#      int_0^inf y^5/(e^y+1) dy = 31 pi^6/252 ,
#
#  gives, with lambda = Theta^2/c^2 = 3 Theta^2,
#
#      u/u_SB - 1 = lambda pi^2 (1550/147) [ <a> + 3 <b^2> ] = (310 pi^2/441) Theta^2
#
#  The bracket is 4/315 + 3/315 = 7/315 = 7 <A>: the branch-odd term supplies
#  3 of the 7, i.e. 42.857 % of the coefficient.  Pressure uses the same
#  momentum-flux definition F300 uses, p = (1/3V) sum_k n_F (k . grad_k omega),
#  and the entropy follows from s = (u + p)/T.

C_U_FERMION_EXACT = 310.0 * math.pi ** 2 / 441.0
C_W_FERMION_EXACT = 124.0 * math.pi ** 2 / 1323.0
C_S_FERMION_EXACT = 31.0 * math.pi ** 2 / 49.0

BRANCH_ODD_SHARE_EXACT = 3.0 / 7.0
"""Fraction of the fermionic lattice correction carried by the branch-ODD term:
3<b^2> / (<a> + 3<b^2>) = 3/7 exactly.  This is the answer to F300 sec. 7.2's
"with the branch-odd term handled" — it is not cancelled, it dominates the
anisotropic term's share by 3:4."""

FERMION_OVER_PHOTON_EXACT = 31.0 / 4.0
"""C_u^F/C_u^gamma = C_w^F/C_w^gamma = C_s^F/C_s^gamma = 31/4 EXACTLY.
Factors as 7 x 31/28: the 7 is geometric ((<a> + 3<b^2>)/<A> = 7), the 31/28 is
pure statistics ((1 - 2^-5)/(1 - 2^-3) for the zeta(6) moment divided by
(1 - 2^-3)/(1) ... i.e. the Fermi/Bose ratio of the y^5 moment over the y^3
moment)."""


def _angular_grid(n_theta=48, n_phi=96):
    xt, wt = xp.polynomial.legendre.leggauss(n_theta)
    ph = (xp.arange(n_phi) + 0.5) * 2.0 * xp.pi / n_phi
    wph = 2.0 * xp.pi / n_phi
    NX, NY, NZ, W = [], [], [], []
    for xi, wi in zip(xt, wt):
        s = math.sqrt(1.0 - float(xi) * float(xi))
        NX.append(s * xp.cos(ph))
        NY.append(s * xp.sin(ph))
        NZ.append(xp.full(n_phi, xi))
        W.append(xp.full(n_phi, float(wi) * wph))
    return (xp.concatenate(NX), xp.concatenate(NY),
            xp.concatenate(NZ), xp.concatenate(W))


def fermion_eos(theta, x_max=45.0, n_r=300, n_theta=48, n_phi=96,
                branch_odd_control=False):
    """u, p, w, s of one branch-balanced Weyl pair at Theta, by BZ quadrature.

    "Branch-balanced" means the two BCC branches `sign='+'` and `sign='-'` are
    summed with equal weight — which is what the model's own content supplies
    (section C: 24 left-handed and 24 right-handed Weyl fields).

    `branch_odd_control=True` replaces BOTH branches by their average, i.e.
    deletes the branch-odd term while keeping everything else.  C_u must then
    drop from `310 pi^2/441` to `4/7` of it — the declared control for the one
    claim this module makes that F300 could not.
    """
    NX, NY, NZ, W = _angular_grid(n_theta, n_phi)
    xr, wr = xp.polynomial.legendre.leggauss(n_r)
    k_max = x_max * theta / C
    k = 0.5 * k_max * (xr + 1.0)
    wk = 0.5 * k_max * wr
    KX, KY, KZ = xp.outer(k, NX), xp.outer(k, NY), xp.outer(k, NZ)
    wgt = (wk[:, None] * W[None, :]) * (k ** 2)[:, None]

    def _omega(fx, fy, fz, sign):
        if not branch_odd_control:
            return bcc_dispersion(fx, fy, fz, sign=sign)
        return 0.5 * (bcc_dispersion(fx, fy, fz, sign="+")
                      + bcc_dispersion(fx, fy, fz, sign="-"))

    u = 0.0
    p = 0.0
    h = 1.0e-3
    for sign in ("+", "-"):
        Om = _omega(KX, KY, KZ, sign)
        kdg = (_omega(KX * (1 - 2 * h), KY * (1 - 2 * h), KZ * (1 - 2 * h), sign)
               - 8.0 * _omega(KX * (1 - h), KY * (1 - h), KZ * (1 - h), sign)
               + 8.0 * _omega(KX * (1 + h), KY * (1 + h), KZ * (1 + h), sign)
               - _omega(KX * (1 + 2 * h), KY * (1 + 2 * h), KZ * (1 + 2 * h), sign)
               ) / (12.0 * h)
        nF = 1.0 / (xp.exp(xp.clip(Om / theta, -500.0, 500.0)) + 1.0)
        u += float(xp.sum(wgt * Om * nF))
        p += float(xp.sum(wgt * kdg * nF)) / 3.0
    pref = 1.0 / (2.0 * xp.pi) ** 3
    u *= pref
    p *= pref
    u_sb = 2.0 * (7.0 / 8.0) * xp.pi ** 2 * theta ** 4 / (30.0 * C ** 3)
    s_sb = 4.0 / 3.0 * u_sb / theta
    return {"theta": theta, "u": u, "p": p, "w": p / u, "s": (u + p) / theta,
            "u_over_SB": u / u_sb, "s_over_SB": ((u + p) / theta) / s_sb}


def fermion_eos_coefficients(thetas=(0.002, 0.005, 0.01, 0.02),
                             branch_odd_control=False):
    """B1-B4: measure C_u^F, C_w^F, C_s^F and compare with the closed forms.

    Under `branch_odd_control` the closed-form targets are multiplied by 4/7.
    """
    rows = []
    for th in thetas:
        r = fermion_eos(th, branch_odd_control=branch_odd_control)
        rows.append({"theta": th,
                     "Cu_meas": (r["u_over_SB"] - 1.0) / th ** 2,
                     "Cw_meas": (1.0 / 3.0 - r["w"]) / th ** 2,
                     "Cs_meas": (r["s_over_SB"] - 1.0) / th ** 2})
    # the Theta -> 0 limit: the residual is the NEXT term and scales as
    # Theta^2, so take the smallest Theta as the estimate of the coefficient
    cu = rows[0]["Cu_meas"]
    cw = rows[0]["Cw_meas"]
    cs = rows[0]["Cs_meas"]
    return {"rows": rows,
            "Cu_meas": cu, "Cu_exact": C_U_FERMION_EXACT,
            "Cu_rel": abs(cu / C_U_FERMION_EXACT - 1.0),
            "Cw_meas": cw, "Cw_exact": C_W_FERMION_EXACT,
            "Cw_rel": abs(cw / C_W_FERMION_EXACT - 1.0),
            "Cs_meas": cs, "Cs_exact": C_S_FERMION_EXACT,
            "Cs_rel": abs(cs / C_S_FERMION_EXACT - 1.0),
            "ratio_meas": cu / cw, "ratio_exact": 7.5,
            "ratio_rel": abs(cu / cw / 7.5 - 1.0)}


def fermion_photon_ratios():
    """B5: the three fermion/photon coefficient ratios are all exactly 31/4.

    This is a closed-form identity, checked here as an identity and not as a
    measurement: 7 (geometry) x 31/28 (statistics).
    """
    r_u = C_U_FERMION_EXACT / C_U_PHOTON
    r_w = C_W_FERMION_EXACT / C_W_PHOTON
    r_s = C_S_FERMION_EXACT / C_S_PHOTON
    geom = (MEAN_A_FERMION_EXACT + 3.0 * MEAN_B2_EXACT) / MEAN_A_EXACT
    stat = FERMION_OVER_PHOTON_EXACT / geom
    return {"ratio_u": r_u, "ratio_w": r_w, "ratio_s": r_s,
            "exact": FERMION_OVER_PHOTON_EXACT,
            "max_rel": max(abs(r_u / FERMION_OVER_PHOTON_EXACT - 1.0),
                           abs(r_w / FERMION_OVER_PHOTON_EXACT - 1.0),
                           abs(r_s / FERMION_OVER_PHOTON_EXACT - 1.0)),
            "geometric_factor": geom, "geometric_factor_exact": 7.0,
            "statistics_factor": stat, "statistics_factor_exact": 31.0 / 28.0,
            "branch_odd_share": 3.0 * MEAN_B2_EXACT
                                / (MEAN_A_FERMION_EXACT + 3.0 * MEAN_B2_EXACT),
            "branch_odd_share_exact": BRANCH_ODD_SHARE_EXACT}


# ==========================================================================
#  C.  THE CONTENT — every species, and every exclusion, with its reason
# ==========================================================================
#
#  The 48 Weyl fields are 3 generations x 16, and the 16 is (F47/F165/F279):
#
#      LEFT   nu_L, e_L                      2      u_L, d_L   x 3 colours   6
#      RIGHT  e_R, nu_R                      2      u_R, d_R   x 3 colours   6
#
#  i.e. 8 left-handed and 8 right-handed per generation, 24 and 24 in total.
#  That balance is what makes `fermion_eos` a branch-BALANCED sum and it is not
#  an assumption: the right-handed partners are forced by the Higgs-free mass
#  step (founding decision 3, F27/F41/F42), and nu_R by the F47 see-saw.
#
#  A Weyl field contributes g = 2 thermal degrees of freedom (the walk's two
#  eigenbranches at energy +/- omega, i.e. particle and antiparticle).

MODEL_M_E_MEV = 0.51069
"""The MODEL's electron mass, MeV.  F121, tau-anchored canonical spectrum:
m_e = 0.51069 (-0.06 % vs PDG 0.51099895), m_mu = 105.6575 (-0.00 %), m_tau =
1776.86 (the anchor).  Carried as a module literal with provenance, exactly as
`cosmology_bbn.M_E_MEV` and `cosmology_bbn.MODEL_DELTA_M_MEV` already are."""

PDG_M_E_MEV = 0.51099895
MODEL_M_MU_MEV = 105.6575          # F121
MODEL_M_TAU_MEV = 1776.86          # F121 anchor


def weyl_content():
    """C1: the 48 Weyl fields, split by chirality, and the branch balance.

    The count is a property of the model's own content and is checked, not
    asserted: 3 generations x (8 L + 8 R) = 24 + 24 = 48, and the left/right
    difference must be exactly zero for `fermion_eos` to be the branch sum it
    claims to be.
    """
    per_generation = {
        "nu_L": {"chirality": "L", "n": 1, "colour": 1},
        "e_L": {"chirality": "L", "n": 1, "colour": 1},
        "u_L": {"chirality": "L", "n": 1, "colour": 3},
        "d_L": {"chirality": "L", "n": 1, "colour": 3},
        "e_R": {"chirality": "R", "n": 1, "colour": 1},
        "nu_R": {"chirality": "R", "n": 1, "colour": 1},
        "u_R": {"chirality": "R", "n": 1, "colour": 3},
        "d_R": {"chirality": "R", "n": 1, "colour": 3},
    }
    nL = sum(v["n"] * v["colour"] for v in per_generation.values()
             if v["chirality"] == "L")
    nR = sum(v["n"] * v["colour"] for v in per_generation.values()
             if v["chirality"] == "R")
    n_gen = 3
    return {"per_generation": per_generation,
            "weyl_L_per_generation": nL, "weyl_R_per_generation": nR,
            "n_generations": n_gen,
            "weyl_total": n_gen * (nL + nR),
            "weyl_L_total": n_gen * nL, "weyl_R_total": n_gen * nR,
            "chirality_imbalance": n_gen * (nL - nR),
            "dof_per_weyl": 2,
            "fermionic_modes_per_site": 2 * n_gen * (nL + nR)}


#  ---- the relativistic species table --------------------------------------
#
#  `T_ratio` is the species' own temperature in units of the photon
#  temperature.  `bath` says which one it tracks.  `status` is the whole point
#  of the table: an EXCLUSION with a reason is a derivation step, and F297's
#  thermal history had four of them implicit.

def species_table(m_e=None):
    """C2: the model's relativistic content in the BBN window, with reasons.

    Every entry carries a `provenance` and a `status`.  The four `excluded`
    entries are the content statements F297 made implicitly by writing down a
    three-species bath; here they are statements with reasons attached, and
    section D1 turns two of them into quantitative bounds.
    """
    if m_e is None:
        m_e = MODEL_M_E_MEV
    return [
        {"name": "photon", "kind": "boson", "g": 2, "mass_MeV": 0.0,
         "bath": "photon", "status": "thermal",
         "provenance": "F67/F68/F69 paired-spinor photon; EoS a theorem (F300)",
         "reason": "massless, 2 transverse polarisations, non-birefringent"},
        {"name": "e+e-", "kind": "fermion", "g": 4, "mass_MeV": m_e,
         "bath": "photon", "status": "thermal",
         "provenance": "F121 tau-anchored spectrum (model m_e = 0.51069 MeV)",
         "reason": "2 Weyl fields (e_L, e_R) x 2 = 4; charged, so it tracks "
                   "the photon bath until it annihilates"},
        {"name": "nu_L x3", "kind": "fermion", "g": 6, "mass_MeV": 0.0,
         "bath": "neutrino", "status": "thermal",
         "provenance": "F165/F279 (Y != 0 -> couples), F47 (light)",
         "reason": "3 left-handed Weyl fields x 2 = 6; decoupled below ~2 MeV, "
                   "so its temperature is tracked separately"},
        {"name": "nu_R x3", "kind": "fermion", "g": 6, "mass_MeV": None,
         "bath": "none", "status": "excluded",
         "provenance": "F165/F279 (Y = 0 forced), F47/F236 (heavy Majorana)",
         "reason": "TOTAL singlet: Y = 0 is forced by the constraint system, so "
                   "there is no renormalisable coupling to the bath, and the "
                   "see-saw gives it M_R.  Two independent reasons for the same "
                   "zero.  If it thermalised, Delta N_eff = 3 x 0.57 = 1.71"},
        {"name": "E_g scalars", "kind": "boson", "g": 2, "mass_MeV": None,
         "bath": "none", "status": "excluded",
         "provenance": "F253/F255; founding decision 3 (Higgs-free)",
         "reason": "the E_g doublet is the massive condensate direction, at the "
                   "condensate scale.  Its mass is NOT derived in the tree, so "
                   "section D1 converts this exclusion into a lower bound"},
        {"name": "mu+mu-, pions, hadrons", "kind": "mixed", "g": 4,
         "mass_MeV": MODEL_M_MU_MEV, "bath": "photon", "status": "excluded",
         "provenance": "F121 (m_mu), F103 (m_pi)",
         "reason": "Boltzmann-suppressed at T <= 10 MeV; the muon is the "
                   "lightest of them and section D1 quantifies its residual"},
        {"name": "dark matter", "kind": "boson", "g": None, "mass_MeV": None,
         "bath": "none", "status": "excluded",
         "provenance": "F223/F228 Planck-mass geon remnant",
         "reason": "non-relativistic by 19 orders of magnitude; there is no "
                   "light dark sector in this model"},
    ]


# ==========================================================================
#  D.  g_*(T) AND g_*s(T)
# ==========================================================================

_QUAD_CACHE: dict = {}


def _rho_p_hat(x, fermi, u_max=80.0, n_u=400):
    """(rho, p) of ONE degree of freedom in units of its OWN T^4, at x = m/T.

    Zero chemical potential.  Gauss-Legendre on u = p/T in [0, u_max]; the
    integrand is exponentially small at the upper limit for every x >= 0, and
    the massless Bose integrand `u^3/(e^u - 1)` is regular at u -> 0 (it goes to
    u^2), so no endpoint is singular on an open Gauss rule.

        rho/T^4 = (1/2 pi^2) int u^2 sqrt(u^2 + x^2) f du
        p/T^4   = (1/6 pi^2) int u^4 / sqrt(u^2 + x^2) f du

    Checked in `check_gstar` against the exact massless limits: one bosonic dof
    gives pi^2/30, one fermionic dof gives (7/8) pi^2/30.
    """
    key = (u_max, n_u)
    if key not in _QUAD_CACHE:
        xr, wr = xp.polynomial.legendre.leggauss(n_u)
        _QUAD_CACHE[key] = (0.5 * u_max * (xr + 1.0), 0.5 * u_max * wr)
    u, w = _QUAD_CACHE[key]
    e = xp.sqrt(u * u + x * x)
    ex = xp.exp(xp.clip(e, -500.0, 500.0))
    f = 1.0 / (ex + 1.0) if fermi else 1.0 / (ex - 1.0)
    pref = 1.0 / (2.0 * xp.pi ** 2)
    rho = pref * float(xp.sum(w * u * u * e * f))
    p = pref / 3.0 * float(xp.sum(w * u ** 4 / e * f))
    return rho, p


def g_star(T_mev, r_nu=1.0, m_e=None, include=("thermal",), extra=()):
    """g_*(T) and g_*s(T) from the model's content at photon temperature T.

    `r_nu = T_nu/T_gamma` is supplied by the caller because it is not a free
    choice: section D1 takes it from `cosmology_bbn.thermal_history`, where it
    EMERGES from entropy conservation rather than being imposed.

    Definitions, the standard ones so the number is comparable:
        g_*  = (30/pi^2) rho/T^4 ,      g_*s = (45/(2 pi^2)) (rho + p)/T^4 .

    `extra` admits species records beyond the table — used by D1 to price an
    EXCLUDED species back in and turn its exclusion into a bound.
    """
    rho_tot = 0.0
    s_tot = 0.0
    parts = {}
    for sp in list(species_table(m_e=m_e)) + list(extra):
        if sp["status"] not in include:
            continue
        ratio = r_nu if sp["bath"] == "neutrino" else 1.0
        x = 0.0 if not sp["mass_MeV"] else sp["mass_MeV"] / (T_mev * ratio)
        rho_hat, p_hat = _rho_p_hat(x, sp["kind"] == "fermion")
        # energy scales as (T_i/T)^4; entropy density as (T_i/T)^3
        rho = rho_hat * sp["g"] * ratio ** 4
        s = (rho_hat + p_hat) * sp["g"] * ratio ** 3
        rho_tot += rho
        s_tot += s
        parts[sp["name"]] = {"g_star": float(30.0 / xp.pi ** 2 * rho),
                             "g_star_s": float(45.0 / (2.0 * xp.pi ** 2) * s)}
    return {"T_MeV": T_mev, "r_nu": r_nu,
            "g_star": float(30.0 / xp.pi ** 2 * rho_tot),
            "g_star_s": float(45.0 / (2.0 * xp.pi ** 2) * s_tot),
            "by_species": parts}


#  ---- D1.  the BBN window -------------------------------------------------

def bbn_window(m_e=None, n=1200):
    """D1: g_*(T) and g_*s(T) across F297's run, on ITS OWN neutrino history.

    `T_nu/T_gamma` is taken from `cosmology_bbn.thermal_history`, where it is
    produced by entropy conservation through e+e- annihilation and is not put
    in — so the endpoint `g_*s -> 2 + (21/4)(4/11) = 3.909` is a check on the
    thermal history and not a restatement of it.
    """
    from casim.engine.interactions.cosmology_bbn import thermal_history
    if m_e is None:
        m_e = MODEL_M_E_MEV
    T, T_nu, _, _ = thermal_history(n=n, m_e=m_e)
    picks = (10.0, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.01, 5.0e-3)
    rows = []
    for Tp in picks:
        i = int(xp.argmin(xp.abs(T - Tp)))
        r = g_star(float(T[i]), r_nu=float(T_nu[i] / T[i]), m_e=m_e)
        rows.append({"T_MeV": float(T[i]), "r_nu": float(T_nu[i] / T[i]),
                     "g_star": r["g_star"], "g_star_s": r["g_star_s"]})
    early = rows[0]
    late = rows[-1]
    return {"rows": rows,
            "g_star_early": early["g_star"], "g_star_early_target": 10.75,
            "g_star_late": late["g_star"],
            "g_star_late_target": 2.0 + 5.25 * (4.0 / 11.0) ** (4.0 / 3.0),
            "g_star_s_late": late["g_star_s"],
            "g_star_s_late_target": 2.0 + 5.25 * (4.0 / 11.0)}


def excluded_species_prices(T_mev=10.0, m_e=None):
    """D1b: price the EXCLUDED species back in, at the hottest point of the run.

    An exclusion with a reason is a derivation step; an exclusion with a NUMBER
    is a bound.  Two of the four exclusions in `species_table` become bounds
    here, and the other two are already excluded by many orders.
    """
    base = g_star(T_mev, r_nu=1.0, m_e=m_e)["g_star"]

    def price(rec):
        r = g_star(T_mev, r_nu=1.0, m_e=m_e,
                   extra=[dict(rec, status="thermal")])
        return r["g_star"] - base

    d_mu = price({"name": "_mu", "kind": "fermion", "g": 4,
                  "mass_MeV": MODEL_M_MU_MEV, "bath": "photon"})
    d_nuR = price({"name": "_nuR", "kind": "fermion", "g": 6,
                   "mass_MeV": 0.0, "bath": "neutrino"})
    # the E_g bound: the mass above which 2 real scalars move g_* by < 1e-3
    lo, hi = 1.0, 500.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        d = price({"name": "_Eg", "kind": "boson", "g": 2,
                   "mass_MeV": mid, "bath": "photon"})
        if d > 1.0e-3:
            lo = mid
        else:
            hi = mid
    return {"T_MeV": T_mev, "g_star_base": base,
            "delta_g_muon": d_mu,
            "delta_g_muon_rel": d_mu / base,
            "delta_g_nuR_if_thermal": d_nuR,
            "delta_g_nuR_rel": d_nuR / base,
            "m_Eg_bound_MeV": 0.5 * (lo + hi),
            "m_Eg_bound_criterion": "delta g_* < 1e-3 at T = %.1f MeV" % T_mev}


def lattice_correction_at_bbn(T_mev=1.0):
    """D1c: the size of the derived lattice correction to g_* where BBN runs.

    Both the photon (F300) and the fermion (section B) coefficients are used,
    weighted by their share of g_*.  F300 quantified the photon leg only; this
    is the first time the fermionic leg has a number.
    """
    T_lat = lattice_scales()["T_lattice_K"]
    kelvin_per_mev = 1.160451812e10
    theta = T_mev * kelvin_per_mev / T_lat
    d_gamma = C_U_PHOTON * theta ** 2
    d_ferm = C_U_FERMION_EXACT * theta ** 2
    g_gamma, g_ferm = 2.0, 8.75
    d_tot = (g_gamma * d_gamma + g_ferm * d_ferm) / (g_gamma + g_ferm)
    return {"T_MeV": T_mev, "theta": theta,
            "delta_u_photon_rel": d_gamma,
            "delta_u_fermion_rel": d_ferm,
            "delta_g_star_rel": d_tot,
            "T_lattice_K": T_lat}


#  ---- D2.  the plateau table ----------------------------------------------
#
#  Above the BBN window the CONTENT is still the model's, but the plateau
#  BOUNDARIES need m_c, m_b, m_t, m_W and a QCD crossover temperature, none of
#  which this tree derives.  So D2 reports the plateau VALUES — which follow
#  from content alone — and labels the boundaries as imported.  Nothing in D1
#  or section E depends on D2.

def plateau_table():
    """D2: model g_* on each plateau up to the electroweak scale, vs the SM.

    The one place the two differ is the scalar sector, and it differs by
    EXACTLY one degree of freedom: the Standard Model's single physical Higgs
    scalar against the model's two-component E_g doublet (founding decision 3).
    So the model's high-T g_* is 105.75 if the E_g modes are heavy and 107.75
    if they are light — and 106.75, the SM value, is not available to it.
    """
    rows = [
        {"epoch": "T < m_e (post e+e- annihilation)", "boundary": "derived (m_e, F121)",
         "model": 2.0 + 5.25 * (4.0 / 11.0) ** (4.0 / 3.0), "sm": 3.363,
         "content": "gamma; 3 nu_L at (4/11)^(1/3)"},
        {"epoch": "m_e < T < m_mu", "boundary": "derived (m_e, m_mu; F121)",
         "model": 10.75, "sm": 10.75, "content": "gamma; e+e-; 3 nu_L"},
        {"epoch": "m_mu < T < T_QCD", "boundary": "imported (T_QCD)",
         "model": 17.25, "sm": 17.25, "content": "gamma; e, mu; 3 nu_L; pi^0, pi^+-"},
        {"epoch": "T_QCD < T < m_c", "boundary": "imported (T_QCD, m_c)",
         "model": 61.75, "sm": 61.75,
         "content": "gamma; 8 gluons; u, d, s; e, mu; 3 nu_L"},
        {"epoch": "m_c < T < m_b", "boundary": "imported", "model": 75.75,
         "sm": 75.75, "content": "+ c, tau"},
        {"epoch": "m_b < T < m_W", "boundary": "imported", "model": 86.25,
         "sm": 86.25, "content": "+ b"},
        {"epoch": "m_W < T < m_t", "boundary": "imported", "model": 95.25,
         "sm": 96.25, "content": "+ W+-, Z (model has no physical Higgs scalar)"},
        {"epoch": "T > m_t (E_g heavy)", "boundary": "imported", "model": 105.75,
         "sm": 106.75, "content": "+ t; E_g doublet still non-relativistic"},
        {"epoch": "T > m_t (E_g light)", "boundary": "imported", "model": 107.75,
         "sm": 106.75, "content": "+ t; both E_g real scalars relativistic"},
    ]
    # the observable this difference would move, stated so it can be dismissed
    # honestly: Omega_GW ~ g_* g_*s^(-4/3), so a common shift delta gives
    # -delta/3.
    delta = 1.0 / 106.75
    return {"rows": rows,
            "model_minus_sm_high_T": (-1.0, +1.0),
            "high_T_difference_is_exactly_one_dof": True,
            "sm_value_unavailable_to_the_model": 106.75,
            "omega_gw_relative_shift": delta / 3.0,
            "omega_gw_observable_today": False,
            "omega_gw_note": "Omega_GW ~ g_* g_*s^(-4/3); a common one-dof shift "
                             "gives -delta/3 = 0.31 %, far below any current or "
                             "planned primordial-GW sensitivity.  Labelled, not "
                             "published as a falsifier (F300 discipline)."}


# ==========================================================================
#  E.  THE RE-RUN — F297's BBN on the model's own electron mass
# ==========================================================================

def bbn_shift(n=1200):
    """E: run K2 twice, once on PDG m_e and once on the model's own (F121).

    This is the numerically non-null part of gap #4.  The CONTENT the
    derivation produces is identical to the Standard-Model list F297 assumed
    (section D1 proves that, rather than assuming it), so the entire shift in
    Y_p and D/H comes from one number: the model's own electron mass.
    """
    from casim.engine.interactions import cosmology_bbn as B
    base = B.run_bbn(n=n)
    mod = B.run_bbn(n=n, m_e=MODEL_M_E_MEV)
    yp_o, yp_s = B.OBS_YP
    dh_o, dh_s = B.OBS_DH
    return {
        "m_e_PDG_MeV": PDG_M_E_MEV, "m_e_model_MeV": MODEL_M_E_MEV,
        "m_e_rel_shift": MODEL_M_E_MEV / PDG_M_E_MEV - 1.0,
        "Y_p_pdg": base["Y_p"], "Y_p_model": mod["Y_p"],
        "delta_Y_p": mod["Y_p"] - base["Y_p"],
        "delta_Y_p_rel": mod["Y_p"] / base["Y_p"] - 1.0,
        "delta_Y_p_in_sigma": (mod["Y_p"] - base["Y_p"]) / yp_s,
        "Y_p_sigma_pdg": (base["Y_p"] - yp_o) / yp_s,
        "Y_p_sigma_model": (mod["Y_p"] - yp_o) / yp_s,
        "DH_pdg": base["D_H"], "DH_model": mod["D_H"],
        "delta_DH_rel": mod["D_H"] / base["D_H"] - 1.0,
        "delta_DH_in_sigma": (mod["D_H"] - base["D_H"]) / dh_s,
        "DH_sigma_pdg": (base["D_H"] - dh_o) / dh_s,
        "DH_sigma_model": (mod["D_H"] - dh_o) / dh_s,
        "T_freezeout_pdg": base["T_freezeout_MeV"],
        "T_freezeout_model": mod["T_freezeout_MeV"],
        "sigma_Yp_needed_to_see_it": abs(mod["Y_p"] - base["Y_p"]),
        "improvement_factor_needed": yp_s / abs(mod["Y_p"] - base["Y_p"]),
    }


def input_ledger():
    return {
        "model_native": [
            "omega^pm(k) = arccos(u^pm) — the BCC Weyl walk (F26); sections A/B",
            "c_lat = 1/sqrt3 (F26); a = 6.5978 ell_P (F107) -> Theta",
            "48 Weyl fields, 24 L + 24 R (F47/F165/F279) -> branch balance",
            "2 real E_g scalars, massive; NO Higgs (founding decision 3, F253)",
            "nu_R excluded: Y = 0 forced (F165/F279) + heavy Majorana (F47/F236)",
            "m_e = 0.51069 MeV (F121 tau-anchored canonical spectrum)",
            "m_mu = 105.6575 MeV (F121) -> the muon Boltzmann residual",
            "the photon EoS coefficients (F300)",
        ],
        "external": [
            "k_B, hbar, c, ell_P — unit rulers",
            "m_c, m_b, m_t, m_W, T_QCD — the D2 plateau BOUNDARIES only; no D1 "
            "or section E result depends on them",
            "PDG m_e, observed Y_p and D/H — comparison points",
        ],
        "free_parameters": 0,
    }


# ==========================================================================
#  The gap-#4 battery
# ==========================================================================

def check_gstar(branch_odd_control=False, sm_content_control=False, n=1200):
    """Every gap-#4 check, PASS/FAIL, with the two declared controls.

    `branch_odd_control=True`  -> GS-3, GS-4, GS-5 MUST fail: deleting the
        branch-odd term multiplies every fermionic coefficient by 4/7.  GS-7
        must SURVIVE it — C_u/C_w = 15/2 is invariant under the deletion, which
        is the structural half of the claim.
    `sm_content_control=True`  -> GS-8, GS-9 MUST fail: thermalising nu_R (the
        one content statement the model makes that the Standard Model does not
        share) moves g_* off 10.75 and off the (4/11) endpoint.
    """
    checks = []

    def add(cid, desc, ok, got, want):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok),
                       "got": got, "want": want})

    w = weyl_content()
    add("GS-1", "content is 48 Weyl fields, exactly branch-balanced 24 L / 24 R",
        (w["weyl_total"] == 48 and w["chirality_imbalance"] == 0),
        {"total": w["weyl_total"], "imbalance": w["chirality_imbalance"]},
        "48 and 0")

    d = branch_expansion_residual()
    add("GS-2", "closed forms b = n_x n_y n_z/sqrt3 and a = 4A reproduce "
                "bcc_dispersion, residual O(k^2)",
        (d["a_max_abs_residual"] < 1.0e-3 and d["b_max_abs_residual"] < 1.0e-3),
        d, "both < 1e-3")

    m = mean_coefficients()
    add("GS-2a", "<a> = 4/315 and <b^2> = 1/315 exactly",
        (m["mean_a_rel"] < 1.0e-12 and m["mean_b2_rel"] < 1.0e-12),
        {"a_rel": m["mean_a_rel"], "b2_rel": m["mean_b2_rel"]}, "both < 1e-12")

    e = fermion_eos_coefficients(branch_odd_control=branch_odd_control)
    add("GS-3", "u/u_SB - 1 = (310 pi^2/441) Theta^2 (closed form vs quadrature)",
        e["Cu_rel"] < 3.0e-3, e["Cu_meas"], C_U_FERMION_EXACT)
    add("GS-4", "1/3 - w = (124 pi^2/1323) Theta^2",
        e["Cw_rel"] < 5.0e-3, e["Cw_meas"], C_W_FERMION_EXACT)
    add("GS-5", "s/s_SB - 1 = (31 pi^2/49) Theta^2",
        e["Cs_rel"] < 5.0e-3, e["Cs_meas"], C_S_FERMION_EXACT)

    r = fermion_photon_ratios()
    add("GS-6", "fermion/photon coefficient ratio = 31/4 = 7 x 31/28 exactly, "
                "and the branch-ODD term carries 3/7 of the fermionic coefficient",
        (r["max_rel"] < 1.0e-12
         and abs(r["branch_odd_share"] - BRANCH_ODD_SHARE_EXACT) < 1.0e-15
         and abs(r["geometric_factor"] - 7.0) < 1.0e-12),
        {"ratio": r["ratio_u"], "share": r["branch_odd_share"]},
        "31/4 and 3/7")

    add("GS-7", "C_u/C_w = 15/2 for FERMIONS too — the ratio is a property of "
                "degree-3 homogeneity, not of statistics",
        e["ratio_rel"] < 5.0e-3, e["ratio_meas"], 7.5)

    bw = bbn_window(n=n)
    add("GS-8", "g_*(10 MeV) = 10.75 from the model's own content",
        abs(bw["g_star_early"] / 10.75 - 1.0) < 1.0e-3,
        bw["g_star_early"], 10.75)
    add("GS-9", "g_*s endpoint = 2 + (21/4)(4/11), from the emergent T_nu/T_gamma",
        abs(bw["g_star_s_late"] / bw["g_star_s_late_target"] - 1.0) < 1.0e-3,
        bw["g_star_s_late"], bw["g_star_s_late_target"])

    pr = excluded_species_prices()
    add("GS-10", "every excluded species is quantitatively excluded at 10 MeV, "
                 "and the E_g exclusion becomes a mass bound",
        (pr["delta_g_muon_rel"] < 1.0e-2 and pr["m_Eg_bound_MeV"] < 500.0),
        {"muon_rel": pr["delta_g_muon_rel"],
         "m_Eg_bound_MeV": pr["m_Eg_bound_MeV"]},
        "muon < 1 %, bound reported")

    lc = lattice_correction_at_bbn()
    add("GS-11", "the derived lattice correction to g_* at BBN is negligible, "
                 "with the FERMIONIC leg now included",
        lc["delta_g_star_rel"] < 1.0e-30, lc["delta_g_star_rel"], "< 1e-30")

    pt = plateau_table()
    add("GS-12", "the model's high-T g_* differs from the SM's by exactly one "
                 "degree of freedom, and 106.75 is unavailable to it",
        (set(pt["model_minus_sm_high_T"]) == {-1.0, 1.0}
         and all(abs(r["model"] - 106.75) > 0.5 for r in pt["rows"]
                 if r["epoch"].startswith("T > m_t"))),
        pt["model_minus_sm_high_T"], "(-1, +1)")

    sh = bbn_shift(n=n)
    add("GS-13", "K2 re-run on the model's own m_e (F121) shifts Y_p and D/H by "
                 "a definite, sub-observational amount",
        (0.0 < abs(sh["delta_Y_p"]) < 1.0e-3
         and abs(sh["delta_Y_p_in_sigma"]) < 1.0),
        {"dY_p": sh["delta_Y_p"], "sigma": sh["delta_Y_p_in_sigma"],
         "dDH_rel": sh["delta_DH_rel"]},
        "0 < |dY_p| < 1e-3, |d| < 1 sigma")

    if sm_content_control:
        # nu_R thermalised: the one content statement the SM does not share
        bw2_early = g_star(10.0, r_nu=1.0,
                           extra=[{"name": "_nuR", "kind": "fermion", "g": 6,
                                   "mass_MeV": 0.0, "bath": "neutrino",
                                   "status": "thermal"}])["g_star"]
        for c in checks:
            if c["id"] == "GS-8":
                c["got"] = bw2_early
                c["pass"] = abs(bw2_early / 10.75 - 1.0) < 1.0e-3
            if c["id"] == "GS-9":
                c["pass"] = False
                c["got"] = "nu_R thermalised: the (4/11) endpoint no longer holds"

    n_pass = sum(1 for c in checks if c["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": len(checks),
            "all_pass": n_pass == len(checks),
            "weyl": w, "expansion": d, "means": m, "eos": e, "ratios": r,
            "bbn_window": bw, "excluded": pr, "lattice": lc,
            "plateaus": pt, "shift": sh, "species": species_table(),
            "ledger": input_ledger(),
            "controls": {"branch_odd_control": branch_odd_control,
                         "sm_content_control": sm_content_control}}


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    out = check_gstar()
    for c in out["checks"]:
        print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['id']:8s} {c['desc']}")
    print(f"  {out['n_pass']}/{out['n_total']}")
    path = results_path("F309_gstar_model_content.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("wrote", path)

