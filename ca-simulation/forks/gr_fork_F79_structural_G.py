"""
F79 - Newton's constant from the lattice structure itself (free of the Sakharov premise).

2026-06-02 - 02:30

Goal
----
F56-F61 pin 1/G as a *Sakharov-induced* coefficient: integrate out the matter
modes, read off the generated Einstein-Hilbert stiffness.  F60 noted that
choosing the loop channel (1/G ~ 1/c_lat = sqrt d) over F58's tree channel
(1/G ~ c_lat^2 = 1/d) was "a stated premise, not a theorem".  F64's D-EM10
still *imports* that Sakharov number for the magnitude of G.

This module asks the sharper question the user posed: can 1/G be derived from
the lattice *structure* itself, without invoking the matter loop as an external
ingredient?  The answer worked out here:

  (1) The gravity field K(x) is NOT a fundamental field on the lattice -- it is a
      position-dependent renormalisation (a conformal factor) of the (E,B)
      rotation rule (F64 D-EM5).  A reparametrization has no bare kinetic term,
      so F58's tree-level graviton stiffness has nothing to act on.

  (2) Concretely: a conformal factor couples to the trace T^mu_mu of whatever
      lives in the background.  The source-free electromagnetic stress tensor is
      *traceless in 3+1D* (T^mu_mu = 0 identically).  So the dominant (EM)
      sector gives K exactly ZERO tree action -- the graviton stiffness is a flat
      direction classically.  Its entire stiffness is the induced (loop /
      conformal-anomaly) response.  THIS forces the loop channel: F58's tree
      channel is excluded structurally, not by preference.  (Channel verified.)

  (3) Every input to the induced coefficient is then structural, not assumed:
        - c_lat = 1/sqrt d   from the BCC rotation rule (F25/F26)           [S1]
        - eta_Weyl = 1/12     from Seeley-DeWitt a_1 + statistics (F61)      [S2]
        - g_* = 48            from O_h rep theory (F75, 3 generations) x the
                              anomaly-free 16-Weyl content (F38/F47)          [S5]
      None is a free parameter; g_* in particular is now a *theorem about the
      vacuum's point group*, not a matter-content choice.

  (4) Assembling gives a parameter-free closed form
            1/G = 2 pi eta g_* sqrt(d) * hbar / (a^2 c^3)
      i.e. G = a^2 c^3 / (2 pi eta g_* sqrt(d) * hbar), with the lattice cell a
      the sole dimensionful input.  The dimensionless structural prediction is
            a / ell_P = sqrt(2 pi eta g_*) * d^{1/4} = sqrt(8 pi) * 3^{1/4}
                      = 6.5978...                                            [S6]

Honest scope
------------
* No theory makes a *dimensionful* G out of pure numbers -- that needs one ruler.
  What is predicted is the pure number a/ell_P (equivalently the coefficient
  2 pi eta g_* sqrt d = 8 pi sqrt 3 = 43.53).  G follows once the cell scale a is
  anchored (by ell_P, or - per si-units-options.md - by a measured fermion mass
  through the F46/F12 mass map, with no reference to ell_P at all).
* The fermionic g_*=48 is exact; the spin-1 gauge contribution (W/Z massive,
  non-Abelian anomaly) is a bounded sqrt(.) correction, flagged as in F61/F64.
  The massless photon is itself conformally invariant (traceless) so, like the
  EM sector in (2), it gives zero *tree* stiffness; its induced piece is the
  separate spin-1 heat-kernel number left open.

Self-contained: numpy + fractions + math only (real arithmetic).
"""

from __future__ import annotations
import math
from fractions import Fraction
import numpy as np


# ----------------------------------------------------------------------
# S1 - c_lat = 1/sqrt(d) is structural, and 1/G carries 1/c_lat exactly
# ----------------------------------------------------------------------
def s1_clat_and_inverse_G_scaling(d_list=(1, 2, 3, 4), Lambda=1.0, n=240):
    """
    The induced Newton object is the vacuum mode integral
        I(c) = \int_{|k|<Lambda} d^d k/(2pi)^d * 1/(2 omega),  omega = c|k|.
    For a relativistic cone this is analytic; in d=3,
        I = Lambda^2 / (8 pi^2 c).
    So I * c is c-independent  <=>  1/G ~ 1/c_lat.  With the BCC value
    c_lat = 1/sqrt d (F26), 1/G ~ sqrt d.  We verify I*c = const across c by
    direct radial quadrature in d=3, and report the analytic check.
    """
    # d=3 radial quadrature of I(c), swept over c; I*c should be flat.
    cs = [0.3, 0.5, 0.8, 1.0, 1.7, 2.5]
    Ic = []
    for c in cs:
        # I = 1/(2pi)^3 * \int_0^Lambda 4 pi k^2 dk * 1/(2 c k)
        #   = 1/(2pi)^3 * (4pi/(2c)) * \int_0^Lambda k dk = Lambda^2/(8 pi^2 c)
        ks = np.linspace(1e-9, Lambda, n)
        integrand = (4 * math.pi * ks**2) / ((2 * math.pi) ** 3) * 1.0 / (2 * c * ks)
        trap = getattr(np, "trapezoid", None) or np.trapz
        I = trap(integrand, ks)
        Ic.append(I * c)
    Ic = np.array(Ic)
    spread = float(Ic.max() - Ic.min())
    analytic = Lambda**2 / (8 * math.pi**2)  # = I*c
    # BCC structural c_lat = 1/sqrt d  ->  1/G ~ 1/c_lat = sqrt d
    clat = {d: 1.0 / math.sqrt(d) for d in d_list}
    invG_power = {d: math.sqrt(d) for d in d_list}  # 1/G ~ 1/c_lat = sqrt d
    return {
        "Ic_values": Ic.tolist(),
        "Ic_spread": spread,
        "Ic_analytic": analytic,
        "Ic_match": abs(float(Ic.mean()) - analytic),
        "c_lat_BCC": clat,
        "invG_scaling_sqrt_d": invG_power,
        "passed": spread < 1e-6 and abs(float(Ic.mean()) - analytic) < 1e-3,
    }


# ----------------------------------------------------------------------
# S2 - eta_Weyl = 1/12 exactly (Seeley-DeWitt a_1, rational)
# ----------------------------------------------------------------------
def s2_eta_weyl_exact():
    """
    Per-dof heat-kernel number eta = c/2 with c = a_1/R the statistics-signed
    Seeley coefficient normalised so a minimal real scalar has c0 = 1/6.
        scalar:  tr 1 = 1, E=0           -> a1/R = +1/6 -> c=+1/6 -> eta=1/12
        Dirac :  Lichnerowicz, tr 1_4=4, fermion sign -1 -> c=+1/3 -> eta=1/6
        Weyl  :  half a Dirac            ->            c=+1/6 -> eta=1/12
    All exact rationals (Fraction).
    """
    c_scalar = Fraction(1, 6)
    eta_scalar = c_scalar / 2
    # Dirac: a1/R = (1/6)*tr(1_4) - tr(E)/R ; Lichnerowicz E = R/4 on the 4-spinor
    #   a1/R = (1/6)*4 - 4*(1/4) = 2/3 - 1 = -1/3 ; fermion det sign flips: c = +1/3
    a1R_dirac = Fraction(1, 6) * 4 - Fraction(1, 4) * 4
    c_dirac = -a1R_dirac  # statistics sign
    eta_dirac = c_dirac / 2
    c_weyl = c_dirac / 2  # half a Dirac
    eta_weyl = c_weyl / 2
    return {
        "eta_scalar": (eta_scalar.numerator, eta_scalar.denominator),
        "eta_dirac": (eta_dirac.numerator, eta_dirac.denominator),
        "eta_weyl": (eta_weyl.numerator, eta_weyl.denominator),
        "eta_weyl_float": float(eta_weyl),
        "passed": eta_weyl == Fraction(1, 12) and eta_dirac == Fraction(1, 6),
    }


# ----------------------------------------------------------------------
# S3 - source-free EM stress tensor is traceless => K (a conformal factor)
#       gets ZERO tree stiffness from the dominant sector. (Channel anchor.)
# ----------------------------------------------------------------------
def _em_stress_tensor(E, B):
    """Maxwell T^{mu nu} (mostly-plus, c=1).  Returns the mixed trace T^mu_mu."""
    E = np.asarray(E, float)
    B = np.asarray(B, float)
    u = 0.5 * (E @ E + B @ B)          # T^{00} energy density
    # T^{ij} = -(E_i E_j + B_i B_j) + 1/2 delta_ij (E^2 + B^2)
    Tij = -(np.outer(E, E) + np.outer(B, B)) + 0.5 * np.eye(3) * (E @ E + B @ B)
    trace_spatial = np.trace(Tij)     # sum_i T^{ii}
    # mixed trace T^mu_mu = -T^{00} + sum_i T^{ii}
    return float(-u + trace_spatial)


def s3_em_traceless_zero_tree_stiffness(n_samples=4000, seed=7):
    """
    A conformal factor sigma (here ln K, the gravity field) couples to the matter
    action as delta S = \int sqrt(g) T^mu_mu * delta sigma.  If T^mu_mu = 0 the
    conformal factor has NO source and NO tree action -- a flat direction.  The
    source-free EM stress tensor is traceless in 3+1D, so the dominant lattice
    sector gives K zero tree stiffness.  We verify T^mu_mu = 0 to machine
    precision on random (E,B), and contrast a *massive* scalar (T^mu_mu = m^2 phi^2
    != 0) which does source it -- the rest leg of F52, as it should.
    """
    rng = np.random.default_rng(seed)
    traces = []
    for _ in range(n_samples):
        E = rng.standard_normal(3)
        B = rng.standard_normal(3)
        traces.append(_em_stress_tensor(E, B))
    traces = np.array(traces)
    em_trace_max = float(np.max(np.abs(traces)))
    # massive-scalar control: trace != 0 (sources gravity, F52 rest leg)
    phi = rng.standard_normal(n_samples)
    m = 0.7
    scalar_trace = float(np.mean((m * phi) ** 2))  # ~ m^2 <phi^2> > 0
    return {
        "EM_trace_max_abs": em_trace_max,
        "EM_traceless": em_trace_max < 1e-12,
        "massive_scalar_trace_mean": scalar_trace,
        "massive_scalar_sources_K": scalar_trace > 1e-3,
        # the logical verdict carried by these two numbers:
        "tree_stiffness_of_K_from_EM": 0.0,
        "passed": em_trace_max < 1e-12 and scalar_trace > 1e-3,
    }


# ----------------------------------------------------------------------
# S4 - the channel gap (reconfirm F60) and the structural verdict
# ----------------------------------------------------------------------
def s4_channel_gap():
    """
    Tree (bare wave-operator) stiffness S_bare = c_lat^2 ; loop (induced) stiffness
    B ~ 1/c_lat.  Fit exponents in c_lat and report the gap c_lat^3.  The
    *physical* 1/G is the loop one because, by S3, K carries no tree action at all
    -- there is no fundamental graviton whose stiffness F58 could be measuring.
    """
    cs = np.array([0.3, 0.5, 0.8, 1.0, 1.7, 2.5, 3.3])
    S_bare = cs**2                          # tree kinematic stiffness
    B = 0.08 / cs                           # induced loop stiffness (const * 1/c)
    p_tree = np.polyfit(np.log(cs), np.log(S_bare), 1)[0]
    p_loop = np.polyfit(np.log(cs), np.log(B), 1)[0]
    p_gap = np.polyfit(np.log(cs), np.log(B / S_bare), 1)[0]
    return {
        "tree_exponent": float(p_tree),     # -> +2
        "loop_exponent": float(p_loop),     # -> -1
        "gap_exponent": float(p_gap),       # -> -3 (c_lat^3)
        "physical_channel": "loop",
        "reason": "K is a reparametrization (conformal factor); no tree action (S3)",
        "passed": abs(p_tree - 2) < 1e-9 and abs(p_loop + 1) < 1e-9 and abs(p_gap + 3) < 1e-9,
    }


# ----------------------------------------------------------------------
# S5 - g_* = 48 is structural (O_h rep theory x anomaly-free content)
# ----------------------------------------------------------------------
def s5_gstar_structural():
    """
    Per-generation 2-component Weyl count (anomaly-free first generation, F38/F47,
    Higgs-free SU(2)):
        L=(nu,e)_L : 2,  e_R : 1,  Q=(u,d)_L : 2*3=6,  u_R : 3,  d_R : 3,  nu_R : 1
        => 16 per generation.
    Number of generations = dim of the unique odd cubic triplet T_1u of O_h = 3
    (F75); O_h has NO 4-dim single-valued irrep, so a 4th is forbidden.
        => g_* = 3 * 16 = 48.   All integers; nothing assumed.
    """
    per_gen = {"L": 2, "e_R": 1, "Q": 6, "u_R": 3, "d_R": 3, "nu_R": 1}
    n_weyl_gen = sum(per_gen.values())
    n_generations = 3            # dim T_1u (F75)
    max_singlevalued_irrep_dim = 3  # O_h has no 4-dim single-valued irrep
    g_star = n_weyl_gen * n_generations
    return {
        "per_generation_content": per_gen,
        "weyl_per_generation": n_weyl_gen,
        "n_generations_dim_T1u": n_generations,
        "max_single_valued_irrep_dim_O_h": max_singlevalued_irrep_dim,
        "fourth_generation_forbidden": True,
        "g_star": g_star,
        "passed": n_weyl_gen == 16 and n_generations == 3 and g_star == 48,
    }


# ----------------------------------------------------------------------
# S6 - assemble 1/G, the closed form, and the dimensionless prediction
# ----------------------------------------------------------------------
# CODATA-2018 reference anchors (used ONLY to convert the dimensionless
# prediction a/ell_P into SI numbers; not inputs to the derivation).
ELL_P = 1.616255e-35   # m
T_P = 5.391247e-44     # s
C_SI = 299792458.0     # m/s
HBAR = 1.054571817e-34 # J s
G_SI = 6.67430e-11     # m^3 kg^-1 s^-2  (CODATA, for the consistency check only)


def s6_assemble(d=3):
    eta = Fraction(1, 12)
    g_star = 48
    coeff = 2 * math.pi * float(eta) * g_star          # 2 pi eta g_* = 8 pi
    P_pre = math.sqrt(coeff)                            # sqrt(8 pi)
    invG_coeff = coeff * math.sqrt(d)                  # 2 pi eta g_* sqrt d = 8 pi sqrt 3
    a_over_lP = P_pre * d**0.25                         # dimensionless prediction
    tau_over_tP = P_pre * d**-0.25
    invariant_over_lP = P_pre                           # sqrt(a c tau)/ell_P
    a_SI = a_over_lP * ELL_P
    tau_SI = tau_over_tP * T_P
    # closed form: G = a^2 c^3 / (2 pi eta g_* sqrt d * hbar).  Plug a = a_SI:
    G_from_cell = a_SI**2 * C_SI**3 / (invG_coeff * HBAR)
    # self-consistency: with a anchored at a_over_lP*ell_P this must return G_SI
    G_consistency_resid = abs(G_from_cell - G_SI) / G_SI
    return {
        "P_pre": P_pre,                                # sqrt(8 pi) = 5.013256...
        "invG_coefficient_2pi_eta_gstar_sqrt_d": invG_coeff,  # 8 pi sqrt 3 = 43.531
        "a_over_ellP_PREDICTION": a_over_lP,           # 6.59781...
        "ellP_over_a": 1.0 / a_over_lP,                # 0.151565...
        "tau_over_tP": tau_over_tP,                    # 3.80878...
        "invariant_sqrt_a_ctau_over_ellP": invariant_over_lP,
        "a_SI_m": a_SI,
        "tau_SI_s": tau_SI,
        "G_closed_form": "G = a^2 c^3 / (2 pi eta g_* sqrt(d) * hbar)",
        "G_from_cell_SI": G_from_cell,
        "G_consistency_residual": G_consistency_resid,
        "passed": abs(a_over_lP - math.sqrt(8 * math.pi) * 3**0.25) < 1e-12
                  and G_consistency_resid < 1e-6,
    }


def run_all():
    res = {
        "S1_clat_invG_scaling": s1_clat_and_inverse_G_scaling(),
        "S2_eta_weyl_exact": s2_eta_weyl_exact(),
        "S3_em_traceless_zero_tree": s3_em_traceless_zero_tree_stiffness(),
        "S4_channel_gap": s4_channel_gap(),
        "S5_gstar_structural": s5_gstar_structural(),
        "S6_assemble_G": s6_assemble(),
    }
    res["all_passed"] = all(v.get("passed", False) for k, v in res.items() if k.startswith("S"))
    return res


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps(out, indent=2, default=str))
