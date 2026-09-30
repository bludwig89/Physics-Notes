"""
derive_quark_B_colour_charge.py -- F405: F95's Dirac-sea cubic B with quark
colour and charge factors, and whether that dressing can move the Koide
equipartition point to the quark values.

Report "Quark neutrino hierarchy lattice fit" (2026-09-24), derivation four:

    compute F95's cubic coefficient B with quark colour and charge factors.
    The test is whether the equipartition point shifts to k^2 = 1.55 (up)
    and 1.19 (down).  The derivation fails if the shift is sector-blind.

Parametrization (F76-C6 / F93-O4 / F95, Zenczykowski's k):

    y_a = ybar + A cos(delta + 2 pi a/3),   A = sqrt2 k ybar,   m_a = y_a^2
    Q   = sum m / (sum y)^2 = (1 + k^2)/3        (k = 1 <=> Q = 2/3)

Legs (every leg prints its residual in the returned dict):

  E1  exact   sum y and sum y^2 are delta-blind, so Q = (1+k^2)/3 carries no
              delta and no B.  Rescaling B by ANY factor cannot move k.
  E2  exact   cos3delta coefficient of sum y^4 is 3 ybar A^3 (F95 D2), so
              B(k) = k^3 B(1) and B_q = g_f k_f^3 B_lepton at common ybar.
  U1  exact   colour (N_c, C_F) and charge (Q_f) are the SAME on all three
              generations of a sector.  A dressing proportional to the
              identity on the masses (m_a -> lambda_f m_a) leaves Q unchanged;
              an overall factor g_f on the loop leaves its argmin unchanged.
              These are identities (Q is homogeneous of degree 0), checked,
              not discovered.  (Control: generation-dependent charges -> red.)
  U2  exact   the same for mass-independent gauge running: gamma_m has no
              generation index, so intra-sector ratios and Q are RG-invariant
              (textbook).  Zero by construction here.
              (Control: mass-dependent power-law dressing -> red.)
  L1  numeric the F95 loop's own k-preference on the F80 circle (fixed
              sum y^2), leading order: k^2 = 1.896 at delta*=2/9, ~1.98 at
              the quark angles -- not k^2 = 1, and g_f-blind.
  L2  numeric same with the full nonperturbative BCC sea at R = 0.5 (n=400).
  L3  numeric the unitarity-cap loophole: above R ~ 1.015 the clamp m <= 1
              makes the argmin sweep with R (1.37 at 1.02, 0.38 at 1.10).
              g_f-blind, so not colour/charge -- but a sector-dependent
              internal amplitude could reach any quark k^2.  OPEN.
  S1  quant.  finite-stiffness selector E = K(k^2-1)^2 + g R^4 V_loop: the
              lepton k^2 (PDG 2024 m_tau, 2 sigma) bounds g/K, so the quark
              shifts need (g R^4)_q/(g R^4)_l > 4.6e3 (down), 1.3e4 (up)
              in linear response -- not N_c = 3.
  K1  data    required k^2 per sector and scheme (mixed PDG 2025 / M_Z).
  P1  quant.  the power-law loophole m -> m^(1+eps): eps_U/eps_D = 3.885
              +/- 0.047 (independent errors, 2.4 sigma from Q_u^2/Q_d^2 = 4)
              or 3.878 +/- 0.068 (correlated light-quark ratios, 1.8 sigma).
              Asserted: the coefficient is O(1), > 1e3 x any perturbative
              colour x charge loop.  The ratio is a coincidence candidate.
  P2  quant.  undressed angles 0.188 / 0.139 rad: > 3 sigma from 2/9 and
              from each other (correlated MC).

Verdict: FAIL as the report posed it -- colour/charge dressing of B, and any
identity-class dressing, is sector-blind and k-blind.  Not covered: dressings
that weight the A_1g and E_g components differently (inter-generation
stiffness), generation-dependent (family) charges, and the L3 amplitude route.  Real arithmetic only; no chiral
transforms.
"""
from __future__ import annotations

import cmath
import math

import sympy as sp

from casim.constants import B_sea_cubic, delta_star_f
from casim.numerics import rng, xp

# ---------------------------------------------------------------------------
# Inputs (MeV).  PDG 2025 quark summary (the report's "mixed" scheme: u,d,s
# MS-bar at 2 GeV; c,b at m(m); t direct/kinematic) and the M_Z running
# masses the report's notes computed from Antusch-Hinze-Saad
# arXiv:2510.01312 (research_notes/.../cubic_group_crystal_field.md).
# ---------------------------------------------------------------------------
UP_MIXED_MEV = (2.16, 1273.0, 172560.0)
UP_MIXED_SIGMA_MEV = (0.07, 4.6, 310.0)
DOWN_MIXED_MEV = (4.70, 93.5, 4183.0)
DOWN_MIXED_SIGMA_MEV = (0.07, 0.8, 7.0)
UP_MZ_MEV = (1.23, 620.0, 168260.0)
DOWN_MZ_MEV = (2.67, 53.16, 2839.0)
CHARGED_LEPTONS_MEV = (0.51099895069, 105.6583755, 1776.93)   # PDG 2024 m_tau
TAU_SIGMA_MEV = 0.09
# Correlated light-quark error model (FLAG-style ratios): m_ud = (m_u+m_d)/2 at
# +/-1%, m_u/m_d, m_s/m_ud.  Used alongside the independent-error model in P1.
MU_OVER_MD = (0.462, 0.020)
MS_OVER_MUD = (27.23, 0.10)

SCHEMES = {"mixed": (UP_MIXED_MEV, DOWN_MIXED_MEV), "MZ": (UP_MZ_MEV, DOWN_MZ_MEV)}

# Gauge factors.  Electric charges per generation (u,c,t) and (d,s,b).
Q_UP = (sp.Rational(2, 3),) * 3
Q_DOWN = (sp.Rational(-1, 3),) * 3
N_COLOUR = 3
C_F = sp.Rational(4, 3)
ALPHA_EM = 1 / 137.035999        # PDG, Thomson limit (only for the P1 size estimate)
ALPHA_S_MZ = 0.1180              # PDG world average (only for the P1 size estimate)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def koide_Q(m) -> float:
    s = [math.sqrt(x) for x in m]
    return sum(m) / sum(s) ** 2


def circulant_delta(m) -> float:
    """delta mod 2pi/3, folded to [0, pi/3] (F346/F347 convention)."""
    y = [math.sqrt(x) for x in m]
    w = cmath.exp(2j * math.pi / 3)
    Y1 = sum(y[a] * w ** (-a) for a in range(3))
    d = cmath.phase(Y1) % (2 * math.pi / 3)
    return min(d, 2 * math.pi / 3 - d)


def undress_exponent(m, lo: float = 0.2, hi: float = 1.5, it: int = 80) -> float:
    """p such that Q(m^p) = 2/3 (bisection; Q(m^p) rises with p)."""
    f = lambda p: koide_Q([x ** p for x in m]) - 2.0 / 3.0  # noqa: E731
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def _undress_exponent_vec(M, it: int = 70):
    """Vectorised bisection over rows of M (N x 3)."""
    lo = xp.full(M.shape[0], 0.2)
    hi = xp.full(M.shape[0], 1.5)
    L = xp.log(M)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        mp = xp.exp(mid[:, None] * L)
        q = mp.sum(1) / xp.sqrt(mp).sum(1) ** 2 - 2.0 / 3.0
        hi = xp.where(q > 0, mid, hi)
        lo = xp.where(q > 0, lo, mid)
    return 0.5 * (lo + hi)


def _S4_circle(phi: float, c3: float) -> float:
    """sum y^4 / R^4 on the F80 circle sum y^2 = R^2 (exact, E-leg algebra)."""
    c, s = math.cos(phi), math.sin(phi)
    return c ** 4 / 3 + 2 * c * c * s * s + s ** 4 / 2 + 2 * math.sqrt(2) / 3 * c * s ** 3 * c3


def loop_k2_preference(delta: float, g: float = 1.0, n: int = 4000) -> float:
    """Leading-order F95 loop energy on the F80 circle, E = -g (I2/2) R^4 S4.
    Returns k^2 = tan^2 phi at its minimum over phi in (0, arccos(1/sqrt3))."""
    pmax = math.atan(math.sqrt(2))   # Q = 1 edge: arccos(1/sqrt3), the single-axis angle
    best, arg = None, None
    for i in range(1, n):
        p = pmax * i / n
        e = -g * _S4_circle(p, math.cos(3 * delta))
        if best is None or e < best:
            best, arg = e, p
    return math.tan(arg) ** 2


def loop_k2_nonperturbative(delta: float, R: float, L: int = 16, g: float = 1.0,
                            n: int = 120) -> float:
    """Full BCC Dirac sea (F95 f(m) = -<Omega>, cos Omega = sqrt(1-m^2) cos w)."""
    from casim.engine.lattice.bcc import bcc_dispersion
    k = 2 * math.pi * xp.fft.fftfreq(L)
    KX, KY, KZ = xp.meshgrid(k, k, k, indexing="ij")
    cws = [xp.cos(bcc_dispersion(KX, KY, KZ, sign=s)).ravel() for s in "+-"]

    def f(mm):
        nn = math.sqrt(max(0.0, 1 - mm * mm))
        return -sum(float(xp.arccos(xp.clip(nn * c, -1, 1)).mean()) for c in cws) / 2

    pmax = math.atan(math.sqrt(2))   # Q = 1 edge: arccos(1/sqrt3), the single-axis angle
    best, arg = None, None
    for i in range(1, n):
        p = pmax * i / n
        yb = R * math.cos(p) / math.sqrt(3)
        A = R * math.sin(p) * math.sqrt(2 / 3)
        ys = [yb + A * math.cos(delta + 2 * math.pi * a / 3) for a in range(3)]
        e = g * sum(f(y * y) for y in ys)
        if best is None or e < best:
            best, arg = e, p
    return math.tan(arg) ** 2


# ---------------------------------------------------------------------------
# entry point (D9)
# ---------------------------------------------------------------------------

def check_quark_B_colour_charge(generation_charges_up=None,
                                mass_dependent_dressing: bool = False,
                                n_samples: int = 20000) -> dict:
    """F405.  See module docstring.

    generation_charges_up   -- charges used for the U1 dressing on (u,c,t).
                               Default: the physical (2/3, 2/3, 2/3).  The
                               control passes a generation-NONuniform set.
    mass_dependent_dressing -- U2 control: replace the mass-independent
                               (MS-bar-like) gauge running by m -> m^(1+eps).
    """
    checks = {}
    ok_all = True

    def rec(name, ok, detail=None):
        nonlocal ok_all
        checks[name] = {"pass": bool(ok), **{k: (v if isinstance(v, (int, float, str, bool)) else str(v))
                                             for k, v in (detail or {}).items()}}
        ok_all = ok_all and bool(ok)

    yb, A, d, kk, lam, g = sp.symbols("ybar A delta k lambda g", positive=True)
    y = [yb + A * sp.cos(d + 2 * sp.pi * a / 3) for a in range(3)]

    # E1 -- Q is delta-blind and B-blind
    S1 = sp.simplify(sp.expand_trig(sum(y)))
    S2 = sp.simplify(sp.expand_trig(sum(v ** 2 for v in y)))
    Qk = sp.simplify((S2 / S1 ** 2).subs(A, sp.sqrt(2) * kk * yb))
    rec("E1_Q_depends_on_k_only",
        sp.simplify(S1 - 3 * yb) == 0
        and sp.simplify(S2 - 3 * yb ** 2 - sp.Rational(3, 2) * A ** 2) == 0
        and sp.simplify(Qk - (1 + kk ** 2) / 3) == 0
        and sp.diff(Qk, d) == 0,
        {"sum_y": S1, "sum_y2": S2, "Q(k)": Qk})

    # E2 -- B(k) = k^3 B(1): cos3delta coefficient of sum y^4 is 3 ybar A^3
    S4 = sp.expand(sp.expand_trig(sum(v ** 4 for v in y)))
    coeff = sp.simplify(sp.integrate(S4 * sp.cos(3 * d), (d, 0, 2 * sp.pi)) / sp.pi)  # exact Fourier projection
    Bk_ratio = sp.simplify((coeff.subs(A, sp.sqrt(2) * kk * yb)) / (coeff.subs(A, sp.sqrt(2) * yb)))
    rec("E2_B_scales_as_k_cubed",
        sp.simplify(coeff - 3 * yb * A ** 3) == 0 and sp.simplify(Bk_ratio - kk ** 3) == 0,
        {"cos3d_coeff_of_sum_y4": coeff, "B(k)/B(1)": Bk_ratio})

    # K1 -- required k^2 (data), both schemes, and the lepton control value
    k2_req = {}
    for sch, (U, D) in SCHEMES.items():
        k2_req[sch] = {"up": 3 * koide_Q(U) - 1, "down": 3 * koide_Q(D) - 1}
    k2_lep = 3 * koide_Q(CHARGED_LEPTONS_MEV) - 1
    rec("K1_required_k2",
        abs(k2_lep - 1) < 1e-4
        and abs(k2_req["mixed"]["up"] - 1.546) < 2e-3 and abs(k2_req["mixed"]["down"] - 1.194) < 2e-3,
        {"k2_lepton": k2_lep, "k2_up_mixed": k2_req["mixed"]["up"],
         "k2_down_mixed": k2_req["mixed"]["down"], "k2_up_MZ": k2_req["MZ"]["up"],
         "k2_down_MZ": k2_req["MZ"]["down"]})

    # B with colour (and the free sea's charge factor, which is 1) at common ybar
    k_up, k_dn = math.sqrt(k2_req["mixed"]["up"]), math.sqrt(k2_req["mixed"]["down"])
    B_up = N_COLOUR * k_up ** 3 * B_sea_cubic
    B_dn = N_COLOUR * k_dn ** 3 * B_sea_cubic

    # U1 -- generation-uniform dressing leaves Q invariant exactly
    qs = generation_charges_up if generation_charges_up is not None else Q_UP
    if isinstance(qs, str):                       # CLI form "[2/3,2/3,-1/3]"
        qs = [t for t in qs.strip("[]() ").split(",") if t.strip()]
    qs = tuple(sp.Rational(str(q).strip().strip("'\"")) for q in qs)
    msym = sp.symbols("m0:3", positive=True)
    lam_a = [1 + g * C_F * q ** 2 for q in qs]          # any uniform functional of (C_F, Q_f)
    Qs = lambda mm: sum(mm) / sum(sp.sqrt(x) for x in mm) ** 2  # noqa: E731
    dQ_sym = sp.simplify(Qs([lam_a[a] * msym[a] for a in range(3)]) - Qs(list(msym)))
    # numeric residual on physical up masses with an O(1) dressing strength
    dressed = [float((1 + sp.Rational(1, 2) * C_F * qs[a] ** 2) * UP_MIXED_MEV[a]) for a in range(3)]
    dQ_num = abs(koide_Q(dressed) - koide_Q(UP_MIXED_MEV))
    rec("U1_uniform_dressing_Q_invariant", dQ_sym == 0 and dQ_num < 1e-14,
        {"charges": [str(q) for q in qs], "dQ_symbolic": dQ_sym, "dQ_numeric": dQ_num,
         "B_up_over_B_lepton(N_c k^3)": B_up / B_sea_cubic,
         "B_down_over_B_lepton(N_c k^3)": B_dn / B_sea_cubic,
         "B_up": B_up, "B_down": B_dn})

    # U2 -- gauge running from 2 GeV to M_Z, one loop, generation-blind gamma_m
    # (QCD 6 C_F alpha_s/(4pi) + QED 3 Q_f^2 alpha/(2pi); log range ln(M_Z/2 GeV)).
    ell = math.log(91187.6 / 2000.0)
    gam = 6 * float(C_F) * ALPHA_S_MZ / (4 * math.pi) + 3 * float(Q_UP[0]) ** 2 * ALPHA_EM / (2 * math.pi)
    if mass_dependent_dressing:
        run = [x ** (1 + gam) for x in UP_MIXED_MEV]
    else:
        run = [x * math.exp(-gam * ell) for x in UP_MIXED_MEV]
    dQ_run = abs(koide_Q(run) - koide_Q(UP_MIXED_MEV))
    rec("U2_gauge_running_Q_invariant", dQ_run < 1e-14,
        {"gamma_m_one_loop": gam, "log_range": ell, "dQ": dQ_run,
         "mode": "mass_dependent" if mass_dependent_dressing else "mass_independent"})

    # L1 -- the loop's own k preference, leading order, g-independent
    pref = {name: loop_k2_preference(dl) for name, dl in
            (("delta_star", delta_star_f), ("delta_up_mixed", circulant_delta(UP_MIXED_MEV)),
             ("delta_down_mixed", circulant_delta(DOWN_MIXED_MEV)))}
    g_blind = abs(loop_k2_preference(delta_star_f, g=N_COLOUR * 4 / 9) - pref["delta_star"]) < 1e-12
    far = all(abs(v - t) > 0.3 for v in pref.values()
              for t in (1.0, k2_req["mixed"]["up"], k2_req["mixed"]["down"]))
    rec("L1_loop_k_preference_sector_blind_and_wrong", g_blind and far and abs(pref["delta_star"] - 1.896) < 5e-3,
        {**{f"k2_pref_{a}": b for a, b in pref.items()}, "g_blind": g_blind})

    # L2 -- nonperturbative BCC sea, small internal amplitude (R = 0.5)
    k2_np = loop_k2_nonperturbative(delta_star_f, R=0.5, n=400)
    k2_np_g = loop_k2_nonperturbative(delta_star_f, R=0.5, g=N_COLOUR * 4 / 9, n=400)
    # phi-grid step near k^2 ~ 1.9 at n=400 is dk^2 ~ 0.02; tolerance = one step
    rec("L2_nonperturbative_agrees", abs(k2_np - pref["delta_star"]) < 0.02 and abs(k2_np - k2_np_g) < 1e-12,
        {"k2_np_R0.5": k2_np, "k2_np_dressed": k2_np_g, "grid_n": 400})

    # L3 -- the unitarity-cap loophole: above R ~ 1.015 the clamp m <= 1 cuts
    # the circle and the argmin sweeps continuously with R.  It is g-blind
    # (colour/charge cannot drive it) but a sector-dependent INTERNAL
    # AMPLITUDE could; nothing in the model fixes ybar_q.  Recorded, open.
    sweep = {R: loop_k2_nonperturbative(delta_star_f, R=R, n=200) for R in (1.0, 1.02, 1.03, 1.05, 1.10)}
    sweep_g = loop_k2_nonperturbative(delta_star_f, R=1.05, n=200, g=N_COLOUR * 4 / 9)
    rec("L3_cap_loophole_is_amplitude_not_colour",
        abs(sweep[1.0] - pref["delta_star"]) < 0.05 and sweep[1.10] < 1.0 < sweep[1.02]
        and abs(sweep_g - sweep[1.05]) < 1e-12,
        {**{f"k2_np_R{R}": v for R, v in sweep.items()}, "k2_np_R1.05_dressed": sweep_g})

    # S1 -- finite-stiffness selector: E = K (k^2-1)^2 + g R^4 V_loop(k^2, delta).
    # Linear response dk^2 = -g R^4 V'(1)/(2K).  The lepton k^2 (PDG 2024 m_tau)
    # bounds (g R^4/K)_lepton; the quark shifts then need (g R^4)_q/(g R^4)_l of
    # at least  dk2_q / bound_l * V'(delta_l)/V'(delta_q).
    def _dS4_dk2(dl, h=1e-6):
        p1 = math.atan(math.sqrt(1 + h)); p0 = math.atan(math.sqrt(1 - h))
        return (_S4_circle(p1, math.cos(3 * dl)) - _S4_circle(p0, math.cos(3 * dl))) / (2 * h)
    lep = list(CHARGED_LEPTONS_MEV)
    k2l = 3 * koide_Q(lep) - 2
    lep_hi = lep[:2] + [lep[2] + TAU_SIGMA_MEV]
    sig_k2l = abs(3 * koide_Q(lep_hi) - 2 - k2l)
    bound_l = abs(k2l) + 2 * sig_k2l
    need = {}
    for sec, M, dk2 in (("up", UP_MIXED_MEV, k2_req["mixed"]["up"] - 1),
                        ("down", DOWN_MIXED_MEV, k2_req["mixed"]["down"] - 1)):
        need[sec] = dk2 / bound_l * _dS4_dk2(delta_star_f) / _dS4_dk2(circulant_delta(M))
    rec("S1_finite_stiffness_needs_huge_weight",
        min(need.values()) > 1e3 and _dS4_dk2(delta_star_f) > 0,
        {"k2_lepton_minus_1": k2l, "sigma_k2_lepton(m_tau)": sig_k2l, "lepton_bound_2sigma": bound_l,
         "required_gR4_ratio_up": need["up"], "required_gR4_ratio_down": need["down"],
         "loop_pushes_k2_up(sign right)": _dS4_dk2(delta_star_f) > 0})

    # P1 -- the loophole: mass-dependent power-law dressing
    eps = {}
    for sch, (U, D) in SCHEMES.items():
        eU, eD = 1 / undress_exponent(U) - 1, 1 / undress_exponent(D) - 1
        eps[sch] = {"up": eU, "down": eD, "ratio": eU / eD,
                    "kappaCF_from_up": eU / float(Q_UP[0] ** 2), "kappaCF_from_down": eD / float(Q_DOWN[0] ** 2)}
    eps_lep = 1 / undress_exponent(CHARGED_LEPTONS_MEV) - 1
    gen = rng.for_channel("F405_quark_B_colour_charge")
    Um = xp.abs(xp.array(UP_MIXED_MEV) + xp.array(UP_MIXED_SIGMA_MEV) * gen.standard_normal((n_samples, 3)))
    Dm = xp.abs(xp.array(DOWN_MIXED_MEV) + xp.array(DOWN_MIXED_SIGMA_MEV) * gen.standard_normal((n_samples, 3)))
    ratio_mc = (1 / _undress_exponent_vec(Um) - 1) / (1 / _undress_exponent_vec(Dm) - 1)
    r_mean, r_sd = float(ratio_mc.mean()), float(ratio_mc.std())
    # correlated light-quark model
    mud = 0.5 * (DOWN_MIXED_MEV[0] + UP_MIXED_MEV[0]) * (1 + 0.01 * gen.standard_normal(n_samples))
    r_ud = MU_OVER_MD[0] + MU_OVER_MD[1] * gen.standard_normal(n_samples)
    ms = mud * (MS_OVER_MUD[0] + MS_OVER_MUD[1] * gen.standard_normal(n_samples))
    md_c = 2 * mud / (1 + r_ud); mu_c = r_ud * md_c
    heavyU = xp.array(UP_MIXED_MEV[1:]) + xp.array(UP_MIXED_SIGMA_MEV[1:]) * gen.standard_normal((n_samples, 2))
    heavyD = xp.array(DOWN_MIXED_MEV[2:]) + xp.array(DOWN_MIXED_SIGMA_MEV[2:]) * gen.standard_normal((n_samples, 1))
    Uc = xp.column_stack([mu_c, heavyU]); Dc = xp.column_stack([md_c, ms, heavyD])
    ratio_c = (1 / _undress_exponent_vec(Uc) - 1) / (1 / _undress_exponent_vec(Dc) - 1)
    rc_mean, rc_sd = float(ratio_c.mean()), float(ratio_c.std())
    charge_ratio = float((Q_UP[0] / Q_DOWN[0]) ** 2)
    pert = float(C_F) * ALPHA_EM * ALPHA_S_MZ / math.pi ** 2
    rec("P1_power_law_loophole_nonperturbative",
        abs(eps_lep) < 1e-4 and eps["mixed"]["kappaCF_from_up"] / pert > 1e3
        and eps["MZ"]["kappaCF_from_up"] / pert > 1e3,
        {"eps_lepton": eps_lep, **{f"{s}_{k}": v for s, e in eps.items() for k, v in e.items()},
         "ratio_mc_mean": r_mean, "ratio_mc_sd": r_sd, "Qu2_over_Qd2": charge_ratio,
         "sigma_from_4": (charge_ratio - r_mean) / r_sd,
         "ratio_mc_correlated_mean": rc_mean, "ratio_mc_correlated_sd": rc_sd,
         "sigma_from_4_correlated": (charge_ratio - rc_mean) / rc_sd,
         "note": "coincidence candidate; sigma depends on error model (not asserted)", "perturbative_CF_alpha_alphas_over_pi2": pert})

    # P2 -- the undressed triples are not a common lepton-shaped parent
    und = {}
    for sch, (U, D) in SCHEMES.items():
        pU, pD = undress_exponent(U), undress_exponent(D)
        und[sch] = (circulant_delta([x ** pU for x in U]), circulant_delta([x ** pD for x in D]))
    def _und_delta_vec(M):
        p = _undress_exponent_vec(M)
        Y = xp.exp(0.5 * p[:, None] * xp.log(M))
        c = Y[:, 0] + Y[:, 1] * math.cos(2 * math.pi / 3) + Y[:, 2] * math.cos(4 * math.pi / 3)
        s_ = -(Y[:, 1] * math.sin(2 * math.pi / 3) + Y[:, 2] * math.sin(4 * math.pi / 3))
        d_ = xp.mod(xp.arctan2(s_, c), 2 * math.pi / 3)
        return xp.minimum(d_, 2 * math.pi / 3 - d_)
    dU, dD = _und_delta_vec(Uc), _und_delta_vec(Dc)
    zU = abs(float(dU.mean()) - delta_star_f) / float(dU.std())
    zD = abs(float(dD.mean()) - delta_star_f) / float(dD.std())
    zUD = abs(float((dU - dD).mean())) / float((dU - dD).std())
    rec("P2_undressed_not_lepton_shaped", min(zU, zD, zUD) > 3.0,
        {**{f"undressed_delta_{s}_{w}": v[i] for s, v in und.items() for i, w in enumerate(("up", "down"))},
         "sigma_undressed_up_from_2_9": zU, "sigma_undressed_down_from_2_9": zD,
         "sigma_up_vs_down": zUD, "error_model": "correlated, mixed scheme"})

    return {
        "checks": checks,
        "pass": ok_all,
        "verdict": ("FAIL as posed: colour/charge dressing of F95's B is sector-blind and k-blind. "
                    "Q depends only on k; B multiplies only cos3delta; an identity-class dressing (uniform "
                    "mass rescale, overall loop factor, mass-independent running) cannot move k. The loop "
                    "prefers k^2 ~ 1.9, not 1; a finite-stiffness selector bounded by lepton Koide needs a "
                    "quark loop weight > 4.6e3 x the lepton one. Open: A_1g/E_g-differential stiffness, "
                    "family charges, and the unitarity-cap amplitude route (L3). The power-law loophole "
                    "gives eps_U/eps_D = 3.88 vs Q_u^2/Q_d^2 = 4 (1.8-2.4 sigma, error-model dependent) "
                    "with an O(1) coefficient: coincidence candidate."),
    }


if __name__ == "__main__":
    import json

    from casim.engine.particles._results_path import results_path

    out = check_quark_B_colour_charge()
    with open(results_path("F405_quark_B_colour_charge.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    for k, v in out["checks"].items():
        print(f"  [{'PASS' if v['pass'] else 'FAIL'}] {k}")
    print("OVERALL", "PASS" if out["pass"] else "FAIL")
