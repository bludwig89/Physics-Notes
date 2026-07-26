#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ca_superconductivity.py — Electrical (electronic) superconductivity on the lattice
==================================================================================

Created: 2026-07-01

Electrical superconductivity as the **electric S-dual of F86** (which built the
*magnetic* dual superconductor for QCD confinement).  Where F86 condenses
colour-*magnetic* charge and expels colour-*electric* flux (confinement), this
module condenses *electric* charge (paired electrons) and expels *magnetic*
flux (Meissner).  The machinery is reused, not reinvented:

  Task 1 (glue)      — Froehlich retarded attraction from a strain-modulated
                       lattice dielectric K (F64); over-screening face (F117).
  Task 2 (gap)       — the BCS gap equation *is* the F77 NJL self-consistent
                       gap; the coupling-independent universal ratios
                       2*Delta/kTc -> 2*pi/e^gamma = 3.5279 and
                       dC/C_n = 12/(7 zeta(3)) = 1.4261 are the sharp targets.
  Task 3 (pair)      — Cooper pair = charged spin-0 singlet of the F69/F73
                       pairing; charge 2e exact, winding number 2.
  Task 4 (Meissner)  — the photon eats the condensate Goldstone (F44/F34b
                       Stueckelberg) -> massive photon, London depth lambda_L.
  Task 5 (flux)      — h/2e flux quantum from the 2e holonomy (F87); Josephson.
  Task 6 (R=0)       — persistent current: London eq. 1 with E=0 => dJ/dt=0.

Design rules honoured:
  * pure numpy (no scipy); hand-rolled bisection root finder (CLAUDE.md numpy
    caveat — nothing here touches chiral spinors, but we keep our own roots so
    every number is auditable).
  * everything dimensionless on the lattice; SI only via CODATA at the end.
  * tiered results: exact (closed form / integer) > machine precision > numeric.

References: F86 (dual SC template), F117 (gap-coupled dielectric), F64 (lattice
dielectric K), F77 (NJL gap), F69/F73 (paired-spinor / spin-0 bound pair),
F44/F34b (Stueckelberg mass), F87 (U(1) holonomy), F180 (grav-wave speed),
F130-F134 (block-spin elastic sector).
"""
from __future__ import annotations

import math
import numpy as np

# ---------------------------------------------------------------------------
# CODATA 2018 (exact SI defining constants where applicable)
# ---------------------------------------------------------------------------
H_PLANCK = 6.62607015e-34      # J s   (exact, SI 2019)
E_CHARGE = 1.602176634e-19     # C     (exact, SI 2019)
HBAR = H_PLANCK / (2.0 * math.pi)
K_B = 1.380649e-23             # J/K   (exact)
EULER_GAMMA = 0.5772156649015329  # Euler-Mascheroni

# The BCS flux quantum and its (wrong, single-carrier) counterpart.
PHI0_PAIR = H_PLANCK / (2.0 * E_CHARGE)   # h/2e  -- the real one
PHI0_SINGLE = H_PLANCK / E_CHARGE         # h/e   -- if carriers were unpaired


# ===========================================================================
# Task 1 -- the model-native pairing glue (attractive channel)
# ===========================================================================
def frohlich_kernel(omega, omega_q, g2, Vc):
    """Effective electron-electron interaction from exchanging one lattice
    vibration quantum (phonon of the emergent F195-atom crystal), plus the
    (screened) Coulomb repulsion.

        V_eff(q, omega) = Vc  +  g2 * 2*omega_q / (omega^2 - omega_q^2)

    The phonon term is the standard retarded Froehlich vertex.  In this model
    the electron-phonon coupling g is the electron's sensitivity to a local
    modulation of the lattice dielectric K (F64): a strained cell has a slightly
    different K, which shifts the confined (E,B) rotation rate = the electron's
    local energy (F26).  The propagating strain wave is the phonon.

    Sign (the whole point):
        |omega| < omega_q  ->  phonon term < 0  (ATTRACTIVE, retarded)
        |omega| > omega_q  ->  phonon term > 0  (repulsive)
    """
    return Vc + g2 * (2.0 * omega_q) / (omega ** 2 - omega_q ** 2)


def phonon_attractive(omega, omega_q, g2):
    """Just the phonon-exchange piece (no Coulomb).  Negative == attractive."""
    return g2 * (2.0 * omega_q) / (omega ** 2 - omega_q ** 2)


def debye_from_elastic(c_s, a_mat):
    """Emergent Debye-analog cutoff = sound speed x emergent BZ edge.

    omega_D = c_s * q_BZ,  q_BZ = pi / a_mat.

    c_s (acoustic sound speed) is the coarse elastic-modulus mode of the
    F195-atom array, exposed by the F130-F134 block-spin elastic sector; a_mat
    is the emergent (material) lattice constant.  This ties the cutoff to a
    lattice quantity, not a fit.
    """
    return c_s * (math.pi / a_mat)


def small_q_contact_limit(D, rho, c_s):
    """Small-q limit of the acoustic-phonon-mediated attraction.

    Deformation-potential coupling: g_q^2 = D^2 * q^2 / (2 * rho * omega_q) with
    acoustic omega_q = c_s * q.  Then the static (omega->0) attraction is

        V_ph(q, 0) = -2 g_q^2 / omega_q
                   = -2 * (D^2 q^2 / (2 rho c_s q)) / (c_s q)
                   = -D^2 / (rho c_s^2)      (independent of q)

    i.e. the BCS *constant* attractive contact interaction -V emerges with no
    extra assumption.  Returns that constant V (a positive magnitude; the
    interaction is -V).
    """
    return (D ** 2) / (rho * c_s ** 2)


# ===========================================================================
# Task 2 -- BCS gap equation (== F77 NJL gap) and the universal ratios
# ===========================================================================
def _quad(f, a, b, n=200001):
    """Composite Simpson on a fixed fine grid (pure numpy, no scipy)."""
    if n % 2 == 0:
        n += 1
    x = np.linspace(a, b, n)
    y = f(x)
    h = (b - a) / (n - 1)
    return (h / 3.0) * (y[0] + y[-1] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-1:2].sum())


def _bisect(f, lo, hi, tol=1e-14, maxit=200):
    """Hand-rolled bisection root finder (auditable; no scipy)."""
    flo, fhi = f(lo), f(hi)
    if flo == 0.0:
        return lo
    if fhi == 0.0:
        return hi
    if flo * fhi > 0:
        raise ValueError("root not bracketed")
    for _ in range(maxit):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if abs(fmid) < tol or (hi - lo) < tol:
            return mid
        if flo * fmid < 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return 0.5 * (lo + hi)


def gap_T0(N0V, omega_D):
    """T=0 gap, CLOSED FORM.

    Gap equation with flat DOS N0, constant attraction V, cutoff omega_D:
        1 = N0 V * integral_0^{omega_D} dxi / sqrt(xi^2 + Delta^2)
          = N0 V * arcsinh(omega_D / Delta)
    =>  Delta(0) = omega_D / sinh(1 / (N0 V))       (exact)

    This is structurally the F77 NJL gap equation
        M = m0 + 4 G Nc Nf M I1(M)
    in the chiral (m0->0) limit: same self-consistent 1 = (coupling) x (loop).
    """
    return omega_D / math.sinh(1.0 / N0V)


# Tc integral in reduced variable u = xi/(2kT):
#     I(X) = integral_0^X tanh(u)/u du,   X = omega_D/(2 kT).
# For X > U0 the integrand is 1/u to machine precision (tanh(u)=1), so
#     I(X) = C0 + ln(X/U0),   C0 = integral_0^{U0} tanh(u)/u du.
# This split makes Tc solvable at ANY coupling (no grid-resolution limit) —
# the fixed-linear-grid quadrature fails once kTc is exponentially small.
_U0 = 40.0
_C0 = _quad(lambda u: np.where(u < 1e-14, 1.0, np.tanh(u) / np.where(u < 1e-14, 1.0, u)),
            0.0, _U0, n=400001)


def _tc_reduced_integral(X):
    """I(X) = integral_0^X tanh(u)/u du, robust for large X via the log tail."""
    if X <= _U0:
        return _quad(lambda u: np.where(u < 1e-14, 1.0,
                     np.tanh(u) / np.where(u < 1e-14, 1.0, u)), 0.0, X, n=200001)
    return _C0 + math.log(X / _U0)


def Tc(N0V, omega_D):
    """Critical temperature from the linearised (Delta->0) gap equation:
        1/N0V = I(X),  X = omega_D/(2 kTc),  I(X)=int_0^X tanh(u)/u du.
    For weak coupling (X>U0) this inverts in closed form:
        X* = U0 * exp(1/N0V - C0),  kTc = omega_D/(2 X*).
    For strong coupling, bisect on X directly.  Returns kTc (energy; kB=1).
    """
    target = 1.0 / N0V
    if target > _C0:                     # weak coupling: X* > U0, exact inversion
        Xstar = _U0 * math.exp(target - _C0)
        return omega_D / (2.0 * Xstar)
    f = lambda X: _tc_reduced_integral(X) - target
    Xstar = _bisect(f, 1e-6, _U0)
    return omega_D / (2.0 * Xstar)


def gap_at_T(N0V, omega_D, kT):
    """Self-consistent finite-T gap Delta(T):
        1 = N0 V * integral_0^{omega_D} tanh(E/2kT)/E dxi,  E=sqrt(xi^2+Delta^2).

    Split at xi_c = 2*U0*kT (beyond which tanh(E/2kT)=1 to machine precision):
    dense quadrature on [0, xi_c], and the exact arcsinh tail
        integral_{xi_c}^{omega_D} dxi/E = asinh(omega_D/Delta) - asinh(xi_c/Delta)
    written in Delta->0-safe log form.  Robust at any coupling (unlike a fixed
    linear grid, which cannot resolve the E~kT transition when kT is tiny).
    Bisection on Delta; returns 0 above Tc.
    """
    target = 1.0 / N0V
    xi_c = min(omega_D, 2.0 * _U0 * kT)

    def rhs(Delta):
        inner = _quad(lambda xi: np.tanh(np.sqrt(xi ** 2 + Delta ** 2) / (2.0 * kT))
                      / np.sqrt(xi ** 2 + Delta ** 2), 0.0, xi_c, n=200001)
        if xi_c < omega_D:
            # asinh(a)-asinh(b) = ln[(a+sqrt(a^2+1))/(b+sqrt(b^2+1))], a=wD/D,b=xi_c/D
            tail = math.log((omega_D + math.sqrt(omega_D ** 2 + Delta ** 2)) /
                            (xi_c + math.sqrt(xi_c ** 2 + Delta ** 2)))
        else:
            tail = 0.0
        return inner + tail

    if rhs(1e-14 * omega_D) < target:      # above Tc: only Delta=0 solves it
        return 0.0
    f = lambda D: rhs(D) - target
    return _bisect(f, 1e-12 * omega_D, 5.0 * omega_D)


def universal_gap_ratio(N0V, omega_D):
    """2 Delta(0) / kTc for a given coupling and cutoff."""
    return 2.0 * gap_T0(N0V, omega_D) / Tc(N0V, omega_D)


def bcs_ratio_weak_coupling_limit():
    """The parameter-free BCS value 2 Delta(0)/kTc = 2 pi / e^gamma."""
    return 2.0 * math.pi / math.exp(EULER_GAMMA)


def zeta3(nterms=200000):
    """zeta(3) by direct summation (Apery's constant), pure numpy."""
    k = np.arange(1, nterms + 1, dtype=float)
    return float(np.sum(1.0 / k ** 3))


def specific_heat_jump():
    """BCS normalised specific-heat jump at Tc: dC/C_n = 12 / (7 zeta(3))."""
    return 12.0 / (7.0 * zeta3())


def coherence_length(vF, Delta0):
    """BCS coherence length xi_0 = hbar vF / (pi Delta0)  (lattice units:
    hbar=1)."""
    return vF / (math.pi * Delta0)


# ===========================================================================
# Task 3 -- Cooper pair as the charged spin-0 singlet (F69/F73)
# ===========================================================================
def pair_charge_units():
    """Total charge of the bound electron pair, in units of e.  Two electrons,
    each -1 (integer holonomy, F87) -> -2.  Returns the magnitude 2 (exact
    integer)."""
    return 2


def pair_phase_winding(theta_single_winding):
    """F69: a bound pair advances its phase as the SUM of the constituent
    phases.  Two identical constituents each winding n -> pair winds 2n.  This
    factor 2 is the origin of Phi0 = h/2e (Task 5)."""
    return 2 * theta_single_winding


def pair_spin_singlet_check():
    """1/2 (x) 1/2 = 0 (+) 1.  The Cooper channel is the antisymmetric spin-0
    singlet with symmetric s-wave spatial part (F73 built the neutral singlet;
    the Cooper pair is its charge-2e sibling).  Returns (total_spin, symmetric
    spatial, parity_even) as an exact statement."""
    return {"total_spin": 0, "spatial": "s-wave (symmetric)", "parity": +1,
            "statistics": "boson"}


# ===========================================================================
# Task 4 -- Meissner effect: massive (Stueckelberg) photon, London depth
# ===========================================================================
def london_depth(n_s, m_star, mu0=1.0, q=None):
    """London penetration depth lambda_L from the condensate.

        lambda_L^2 = m_star / (mu0 n_s (2e)^2)

    The (2e)^2 is the pair charge (Task 3).  In the model this length is
    1/m_gamma, the inverse of the Stueckelberg photon mass the paired-spinor
    photon (F69) acquires by eating the condensate phase Goldstone (F44/F34b).
    """
    if q is None:
        q = 2.0 * E_CHARGE
    return math.sqrt(m_star / (mu0 * n_s * q ** 2))


def massive_photon_omega(k, m_gamma, c_lat=1.0 / math.sqrt(3.0)):
    """Proca even-law dispersion inside the condensate (F69 even photon + mass):
        omega^2 = m_gamma^2 + (c_lat k)^2.
    At m_gamma=0 reduces to the free luminal even photon (F69), never the
    excluded birefringent sigma-bilinear photon (F65-F67)."""
    return math.sqrt(m_gamma ** 2 + (c_lat * k) ** 2)


def meissner_profile(x, lambda_L, B0=1.0):
    """Static field expulsion: the massive-photon (Helmholtz/London) equation
        d^2 B / dx^2 = B / lambda_L^2
    has the decaying solution B(x) = B0 exp(-x / lambda_L)."""
    return B0 * np.exp(-np.asarray(x, dtype=float) / lambda_L)


def meissner_slab_solve(L, dx, lambda_L, B_surface=1.0):
    """Solve the 1-D London screening BVP on a slab by finite differences and
    return the numerically-decayed field, so we can *measure* the penetration
    depth and compare it to the analytic 1/m_gamma.

        (d^2/dx^2 - 1/lambda_L^2) B = 0,  B(0)=B_surface, B(L)=~0.
    Tridiagonal solve, hand-rolled Thomas algorithm (no scipy).
    """
    n = int(round(L / dx)) + 1
    x = np.linspace(0.0, L, n)
    inv2 = 1.0 / lambda_L ** 2
    # interior nodes 1..n-2
    N = n - 2
    a = np.full(N, 1.0 / dx ** 2)          # sub-diagonal
    b = np.full(N, -2.0 / dx ** 2 - inv2)  # diagonal
    c = np.full(N, 1.0 / dx ** 2)          # super-diagonal
    d = np.zeros(N)
    d[0] -= (1.0 / dx ** 2) * B_surface    # Dirichlet at x=0
    # Dirichlet ~0 at x=L (natural)
    # Thomas algorithm
    cp = np.zeros(N); dp = np.zeros(N)
    cp[0] = c[0] / b[0]; dp[0] = d[0] / b[0]
    for i in range(1, N):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    Bint = np.zeros(N)
    Bint[-1] = dp[-1]
    for i in range(N - 2, -1, -1):
        Bint[i] = dp[i] - cp[i] * Bint[i + 1]
    B = np.empty(n); B[0] = B_surface; B[-1] = 0.0; B[1:-1] = Bint
    return x, B


# ===========================================================================
# Task 5 -- flux quantization Phi0 = h/2e and the Josephson effect
# ===========================================================================
def flux_quantum(n=1):
    """Trapped flux through a hole in the condensate.

    Single-valuedness of the charge-2e order parameter around the hole forces
        contour integral of grad(theta) . dl = 2 pi n.
    Deep inside, J_s=0 => hbar grad(theta) = 2e A, so
        Phi = contour integral A.dl = n * (2 pi hbar)/(2e) = n h/(2e).
    Returns n * Phi0 with Phi0 = h/2e (exact)."""
    return n * PHI0_PAIR


def ginzburg_landau_kappa(lambda_L, xi0):
    """GL parameter kappa = lambda_L / xi_0.  kappa < 1/sqrt(2): type I;
    kappa > 1/sqrt(2): type II (vortices, S-dual of the F86 flux tube)."""
    return lambda_L / xi0


def josephson_dc(Ic, dtheta):
    """DC Josephson relation: I = Ic sin(dtheta)."""
    return Ic * np.sin(dtheta)


def josephson_ac_dphase(V):
    """AC Josephson relation: d(dtheta)/dt = 2 e V / hbar."""
    return 2.0 * E_CHARGE * V / HBAR


def josephson_evolve(Ic, V, dt, nsteps, dtheta0=0.0):
    """Integrate a voltage-biased junction: constant V -> dtheta ramps linearly
    -> the current I(t)=Ic sin(dtheta) oscillates at the Josephson frequency
    f_J = 2eV/h.  Returns (t, dtheta, I)."""
    t = np.arange(nsteps + 1) * dt
    w = josephson_ac_dphase(V)              # d(dtheta)/dt
    dtheta = dtheta0 + w * t
    I = josephson_dc(Ic, dtheta)
    return t, dtheta, I


# ===========================================================================
# Task 6 -- zero DC resistance / persistent current
# ===========================================================================
def supercurrent_evolve(J0, dt, nsteps, E=0.0, ns_q2_over_m=1.0):
    """London eq. 1: dJ_s/dt = (n_s (2e)^2 / m*) E.

    With E=0 the supercurrent is a constant of motion (dJ/dt=0) -> persistent
    current, exactly.  Returns J(t)."""
    t = np.arange(nsteps + 1) * dt
    J = J0 + ns_q2_over_m * E * t
    return t, J


def normal_current_evolve(J0, dt, nsteps, tau=1.0):
    """Drude control (T>Tc, gapless): dJ/dt = -J/tau -> J decays exponentially.
    The contrast that makes the persistent current meaningful."""
    t = np.arange(nsteps + 1) * dt
    J = J0 * np.exp(-t / tau)
    return t, J


# ===========================================================================
# T_c MAGNITUDE from real superconductors (F211)
# ---------------------------------------------------------------------------
# The gap equation (Task 2) fixes the FORM and the coupling-independent
# universals.  The magnitude of T_c needs the material coupling N(0)V.  Three
# estimators, in increasing fidelity, all fed the SAME literature (lambda, mu*,
# omega_log/theta_D):
#   * BCS weak-coupling: uses our own 2 e^gamma/pi = 1.134 prefactor (F210).
#   * McMillan (1968): intermediate coupling, theta_D prefactor.
#   * Allen-Dynes (1975) modified McMillan: omega_log prefactor + strong-
#     coupling factor f1 (f2 requires the 2nd phonon moment; optional).
# ===========================================================================
def bcs_tc(lam, mustar, omega_log_K):
    """Weak-coupling BCS: k_B T_c = 1.134 * (k_B omega_log) * exp(-1/(lam-mu*)).
    The 1.134 = 2 e^gamma/pi is the SAME constant behind F210's universal gap
    ratio.  N(0)V is identified with (lam - mu*).  omega_log_K in kelvin ->
    returns T_c in kelvin.  Valid only for lam-mu* small (weak coupling)."""
    denom = lam - mustar
    if denom <= 0:
        return 0.0
    return (2.0 * math.exp(EULER_GAMMA) / math.pi) * omega_log_K * math.exp(-1.0 / denom)


def mcmillan_tc(lam, mustar, theta_D_K):
    """McMillan 1968: T_c = (theta_D/1.45) exp[-1.04(1+lam)/(lam-mu*(1+0.62lam))]."""
    num = -1.04 * (1.0 + lam)
    den = lam - mustar * (1.0 + 0.62 * lam)
    if den <= 0:
        return 0.0
    return (theta_D_K / 1.45) * math.exp(num / den)


def allen_dynes_tc(lam, mustar, omega_log_K, omega2_over_wlog=None):
    """Allen-Dynes 1975 modified McMillan:
        T_c = (f1 f2 omega_log/1.20) exp[-1.04(1+lam)/(lam-mu*(1+0.62lam))]
    with strong-coupling factors
        f1 = [1 + (lam/Lam1)^{3/2}]^{1/3},  Lam1 = 2.46(1+3.8 mu*)
        f2 = 1 + (r-1) lam^2/(lam^2 + Lam2^2), Lam2 = 1.82(1+6.3 mu*) r,
             r = <omega^2>^{1/2}/omega_log  (>=1; set to 1 => f2=1 if unknown).
    """
    num = -1.04 * (1.0 + lam)
    den = lam - mustar * (1.0 + 0.62 * lam)
    if den <= 0:
        return 0.0
    Lam1 = 2.46 * (1.0 + 3.8 * mustar)
    f1 = (1.0 + (lam / Lam1) ** 1.5) ** (1.0 / 3.0)
    if omega2_over_wlog is None or omega2_over_wlog <= 1.0:
        f2 = 1.0
    else:
        r = omega2_over_wlog
        Lam2 = 1.82 * (1.0 + 6.3 * mustar) * r
        f2 = 1.0 + (r - 1.0) * lam ** 2 / (lam ** 2 + Lam2 ** 2)
    return (f1 * f2 * omega_log_K / 1.20) * math.exp(num / den)


def lambda_from_hopfield(eta_eV_per_A2, spring_eV_per_A2):
    """Model-native (Task-1) electron-phonon coupling in the Hopfield form
        lambda = N(0) <I^2> / (M <omega^2>) = eta / (M <omega^2>),
    which is exactly the derived contact kernel V = D^2/(rho c_s^2) of Task 1
    written per unit cell: the Hopfield parameter eta = N(0) <I^2> is the
    deformation-potential numerator, and the "spring constant" M<omega^2> = the
    elastic stiffness rho c_s^2.  Both in eV/Angstrom^2.  Returns dimensionless
    lambda.  (Consistency check against tabulated lambda, not a first-principles
    prediction -- eta requires the F64 dielectric strain response for the
    specific crystal, which is the remaining derivation.)"""
    return eta_eV_per_A2 / spring_eV_per_A2


# Representative literature parameters (Allen-Dynes 1975; Carbotte RMP 62, 1027
# (1990); Grimvall).  lambda, mu*, omega_log [K], theta_D [K], Tc_exp [K].
# Values carry the usual +/-10-15% spread between references (esp. lambda).
REAL_SUPERCONDUCTORS = {
    #        lam    mu*   wlog  thetaD  Tc_exp
    "Al":  (0.43, 0.10,  291.0, 428.0, 1.18),
    "Sn":  (0.72, 0.11,  100.0, 200.0, 3.72),
    "In":  (0.805,0.10,   85.0, 108.0, 3.41),
    "Ta":  (0.69, 0.10,  130.0, 240.0, 4.48),
    "Nb":  (1.01, 0.10,  138.0, 275.0, 9.25),
    "Pb":  (1.55, 0.10,   56.0, 105.0, 7.19),
    "Hg":  (1.62, 0.10,   29.0,  72.0, 4.15),
}


def tc_table():
    """Compute BCS / McMillan / Allen-Dynes T_c for the reference set and the
    relative error of the (best) Allen-Dynes prediction vs experiment."""
    rows = []
    for el, (lam, mus, wlog, thetaD, tc_exp) in REAL_SUPERCONDUCTORS.items():
        tb = bcs_tc(lam, mus, wlog)
        tm = mcmillan_tc(lam, mus, thetaD)
        ta = allen_dynes_tc(lam, mus, wlog)
        rows.append({"element": el, "lambda": lam, "mustar": mus,
                     "omega_log_K": wlog, "theta_D_K": thetaD,
                     "Tc_exp_K": tc_exp, "Tc_BCS_K": tb, "Tc_McMillan_K": tm,
                     "Tc_AllenDynes_K": ta,
                     "rel_err_AD": abs(ta - tc_exp) / tc_exp})
    return rows


# ===========================================================================
# F212 Part A -- first-principles Hopfield eta / lambda from the F64
# deformation potential (free-electron / jellium limit)
# ---------------------------------------------------------------------------
M_E = 9.1093837015e-31        # kg
EV_J = 1.602176634e-19        # J per eV


def fermi_energy_free_electron(n_per_m3):
    """E_F = hbar^2/(2m) (3 pi^2 n)^(2/3), returned in eV.  n = electron density
    (the model provides this from the F125/F195 electron sector)."""
    kF = (3.0 * math.pi ** 2 * n_per_m3) ** (1.0 / 3.0)
    E_J = (HBAR ** 2 / (2.0 * M_E)) * kF ** 2
    return E_J / EV_J


def deformation_potential_bare(E_F_eV):
    """Bare free-electron deformation potential D = (2/3) E_F, in eV.

    MODEL-NATIVE ORIGIN (F64): a dilational strain Delta = div(u) rescales the
    electron density n -> n/(1+Delta), and the conduction-electron energy scale
    E_F ∝ n^(2/3) shifts by dE_F = -(2/3)E_F Delta.  In the model's language the
    strained cell carries a modulated lattice dielectric K (F64); the electron's
    confined (E,B) rotation-rate energy (F26) — of which E_F is the Fermi-level
    value — rescales geometrically with the dilation.  So D = (2/3)E_F needs
    ONLY E_F, i.e. only the electron density.  This is the *unscreened* value."""
    return (2.0 / 3.0) * E_F_eV


def dos_free_electron_per_spin(n_per_m3, E_F_eV):
    """N(0) per spin per unit volume = 3n/(4 E_F), in states/(eV m^3)."""
    return 3.0 * n_per_m3 / (4.0 * E_F_eV)


def lambda_jellium(n_per_m3, rho_kg_m3, c_s_m_s, screening_D=1.0, E_F_eV=None):
    """Electron-phonon lambda in the deformation-potential jellium model:

        lambda = N(0) D^2 / (rho c_s^2)    [= N(0) * V_Task1, loop closure]

    with D = screening_D * (2/3) E_F.  screening_D<1 folds in the F64/Thomas-
    Fermi dielectric screening of the deformation potential.  All SI; returns
    dimensionless lambda.  Note rho c_s^2 (mass density x sound speed^2) is
    exactly the elastic stiffness in the Task-1 kernel V = D^2/(rho c_s^2), so
    lambda = N(0) x V is a structural identity, not a new assumption."""
    if E_F_eV is None:
        E_F_eV = fermi_energy_free_electron(n_per_m3)
    D_eV = screening_D * deformation_potential_bare(E_F_eV)
    N0 = dos_free_electron_per_spin(n_per_m3, E_F_eV)          # states/(eV m^3)
    D_J = D_eV * EV_J                                          # J
    N0_perJ = N0 / EV_J                                        # states/(J m^3)
    stiffness = rho_kg_m3 * c_s_m_s ** 2                       # Pa = J/m^3
    return N0_perJ * D_J ** 2 / stiffness


def bohm_staver_cs(n_per_m3, Z, M_amu, E_F_eV=None):
    """Bohm-Staver acoustic sound speed c_s = v_F sqrt(Z m_e / 3 M), the
    screened-ion-jellium result (the screening is the F64 dielectric).  m/s."""
    if E_F_eV is None:
        E_F_eV = fermi_energy_free_electron(n_per_m3)
    vF = math.sqrt(2.0 * E_F_eV * EV_J / M_E)
    M_kg = M_amu * 1.66053906660e-27
    return vF * math.sqrt(Z * M_E / (3.0 * M_kg))


# Free-electron (jellium-valid) metals.  n [1/m^3], rho [kg/m^3], c_s longitud.
# [m/s], Z valence, M [amu], lambda measured.
JELLIUM_METALS = {
    #        n          rho     c_s_long  Z    M     lam_meas
    "Al":  (1.81e29,  2700.0,  6420.0,   3,  27.0,  0.43),
    "Na":  (2.65e28,   968.0,  3200.0,   1,  23.0,  0.16),
    "Pb":  (1.32e29, 11340.0,  1960.0,   4, 207.0,  1.55),
}


def jellium_table():
    """Bare (unscreened) jellium lambda vs measured, and the screening factor
    on D that reconciles them."""
    rows = []
    for el, (n, rho, cs, Z, M, lam_m) in JELLIUM_METALS.items():
        EF = fermi_energy_free_electron(n)
        D = deformation_potential_bare(EF)
        lam_bare = lambda_jellium(n, rho, cs, screening_D=1.0, E_F_eV=EF)
        # D screening factor s such that s^2 * lam_bare = lam_meas
        s_D = math.sqrt(lam_m / lam_bare) if lam_bare > 0 else float("nan")
        rows.append({"metal": el, "E_F_eV": EF, "D_bare_eV": D,
                     "lambda_bare": lam_bare, "lambda_meas": lam_m,
                     "D_screening_factor": s_D, "D_screened_eV": s_D * D,
                     "overestimate": lam_bare / lam_m})
    return rows


# ===========================================================================
# F242 -- Morel-Anderson mu* from the F64 EM-connection dielectric
# ---------------------------------------------------------------------------
# The F64 lattice EM dielectric K, in its static long-wavelength (small-q)
# limit for the conduction-electron medium, is the Thomas-Fermi/RPA screening
# function eps(q)=1+k_TF^2/q^2 -- the SAME F64 dielectric already invoked by
# deformation_potential_bare() and bohm_staver_cs() for the phonon side.
# Screening the bare Coulomb with it and Fermi-surface-averaging gives a
# PARAMETER-FREE Coulomb repulsion mu(r_s), and the Morel-Anderson (1962)
# retardation reduction gives mu*.  No fit input.
BOHR_A0 = 5.29177210903e-11        # Bohr radius (m)
_C_RS   = (9.0 * math.pi / 4.0) ** (1.0 / 3.0)   # k_F a0 = _C_RS / r_s = 1.91916/r_s


def wigner_seitz_rs(n_per_m3):
    """Wigner-Seitz radius r_s (in units of the Bohr radius) from electron
    density n [1/m^3]:  (4/3) pi (r_s a0)^3 = 1/n."""
    rs_m = (3.0 / (4.0 * math.pi * n_per_m3)) ** (1.0 / 3.0)
    return rs_m / BOHR_A0


def mu_coulomb_jellium(rs):
    """Dimensionless static Coulomb repulsion mu = N(0)<V_c>_FS with the bare
    Coulomb screened by the F64->Thomas-Fermi dielectric eps(q)=1+k_TF^2/q^2.

    Double-Fermi-surface average over q = 2 k_F sin(theta/2), q in [0,2k_F]:
        <V_c>_FS = (pi e^2/k_F^2) ln[1+(2k_F/k_TF)^2]
    with the free-electron identities k_F a0 = 1.91916/r_s and
    (k_TF/k_F)^2 = 4/(pi k_F a0), this reduces to the closed form
        mu(r_s) = (e^2 k_F / 4 pi E_F) ln(1+(2k_F/k_TF)^2)
                = 0.082930 * r_s * ln(1 + 6.0299/r_s).
    Pure function of r_s; no fit."""
    x2 = 6.0299 / rs                       # (2 k_F/k_TF)^2
    return 0.082930 * rs * math.log(1.0 + x2)


def mustar_from_dielectric(n_per_m3, omega_c_eV, E_F_eV=None):
    """Morel-Anderson Coulomb pseudopotential mu*(omega_c) derived from the
    F64 dielectric, at cutoff omega_c:

        mu*(omega_c) = mu / (1 + mu ln(E_F/omega_c)),   mu = mu_coulomb_jellium(r_s).

    IMPORTANT (cutoff consistency): omega_c must be the SAME Coulomb cutoff at
    which the pseudopotential is applied.  The F215 eliashberg_solve applies
    mu* within |omega_m| < omega_c = omega_c_factor * omega_log (default 6),
    so feed omega_c = 6 * k_B*omega_log to match.  Returns (mustar, mu, ln_arg).
    Free-electron E_F is used unless E_F_eV is given (d-band metals: the true
    N(0) exceeds free-electron, so this mu* is a lower bound there)."""
    if E_F_eV is None:
        E_F_eV = fermi_energy_free_electron(n_per_m3)
    rs = wigner_seitz_rs(n_per_m3)
    mu = mu_coulomb_jellium(rs)
    L = math.log(E_F_eV / omega_c_eV)
    return mu / (1.0 + mu * L), mu, L


# ===========================================================================
# F212 Part B -- mass renormalization Z=1+lambda and the (non-)universal gap
# ratio; what the model needs (the Eliashberg extension)
# ===========================================================================
def z_mass_renormalization(lam):
    """Eliashberg quasiparticle mass renormalization Z = 1 + lambda.  This is
    the factor plain weak-coupling BCS omits (F211): it enters McMillan's
    exponent as (1+lambda) and suppresses T_c below the BCS estimate."""
    return 1.0 + lam


def gap_ratio_strong_coupling(Tc_K, omega_log_K):
    """Strong-coupling correction to the gap ratio (Marsiglio-Carbotte /
    Mitrovic form):

        2 Delta(0)/kTc = 3.528 [ 1 + 12.5 (Tc/omega_log)^2 ln(omega_log/2Tc) ].

    Reduces to the F210 weak-coupling universal 3.528 as Tc/omega_log -> 0.
    The deviation is set by Tc/omega_log — the same coupling strength that
    makes Z=1+lambda large."""
    r = Tc_K / omega_log_K
    if r <= 0:
        return 2.0 * math.pi / math.exp(EULER_GAMMA)
    corr = 1.0 + 12.5 * r ** 2 * math.log(omega_log_K / (2.0 * Tc_K))
    return (2.0 * math.pi / math.exp(EULER_GAMMA)) * corr


# Measured reduced gaps 2 Delta(0)/kTc (tunneling; Carbotte RMP 1990).
GAP_RATIO_MEASURED = {
    "Al": 3.40, "Sn": 3.50, "In": 3.65, "Ta": 3.60,
    "Nb": 3.80, "Pb": 4.38, "Hg": 4.60,
}


def gap_ratio_table():
    """Strong-coupling-corrected gap ratio vs measured, using the F211
    (omega_log, Tc) inputs."""
    rows = []
    for el, meas in GAP_RATIO_MEASURED.items():
        lam, mus, wlog, thetaD, tc = REAL_SUPERCONDUCTORS[el]
        pred = gap_ratio_strong_coupling(tc, wlog)
        rows.append({"element": el, "Tc_over_wlog": tc / wlog,
                     "ratio_pred": pred, "ratio_meas": meas,
                     "rel_err": abs(pred - meas) / meas,
                     "Z": z_mass_renormalization(lam)})
    return rows


# ===========================================================================
# F214 -- imaginary-axis Eliashberg solver on the F210 retarded kernel
# ---------------------------------------------------------------------------
# The F210/F77 gap is STATIC (Z == 1).  Eliashberg promotes it to the coupled
# (Z, Delta) equations on the Matsubara axis, restoring the mass renormalization
# Z = 1 + lambda that plain BCS drops (F211/F213).  We use the single Einstein
# mode -- which is exactly F210's single-mode retarded kernel
#   2 omega_q/(omega^2 - omega_q^2)   ->   lambda(i nu_l) = lambda omega_E^2
#                                          / (omega_E^2 + nu_l^2)   (Matsubara).
#
# Fermionic Matsubara frequencies:  omega_n = pi T (2n+1).
# Coupling (Einstein):  lambda(n-m) = lambda * omega_E^2/(omega_E^2 + [2 pi T (n-m)]^2).
#
# Coupled equations (Delta = gap function, Z = renormalization):
#   Z_n       = 1 + (pi T/omega_n) sum_m lambda(n-m) omega_m/sqrt(omega_m^2+Delta_m^2)
#   Z_n Delta_n = pi T sum_m [lambda(n-m) - mu*] Delta_m/sqrt(omega_m^2+Delta_m^2)
# mu* applied for |omega_m| < omega_c (Matsubara cutoff).
# All frequencies/temperatures in kelvin (k_B = 1).
# ===========================================================================
def _matsubara(T, N):
    """Fermionic Matsubara frequencies omega_n = pi T (2n+1) for
    n = -N .. N-1 (2N of them), returned as an array."""
    n = np.arange(-N, N)
    return math.pi * T * (2.0 * n + 1.0)


def _einstein_lambda_matrix(T, lam, omega_E, N):
    """lambda(n-m) matrix on the 2N x 2N Matsubara grid (Einstein mode)."""
    idx = np.arange(-N, N)
    d = idx[:, None] - idx[None, :]                 # (n - m)
    nu = 2.0 * math.pi * T * d
    return lam * omega_E ** 2 / (omega_E ** 2 + nu ** 2)


# ---------------------------------------------------------------------------
# F216 -- first-principles alpha^2 F(omega): the model-derived Eliashberg
# spectral function (deformation potential D=(2/3)E_F on a Debye acoustic band)
# ---------------------------------------------------------------------------
def alpha2F_debye(omega, lam, omega_max):
    """Model-native Eliashberg spectral function.

    Acoustic phonons omega_q = c_s q with the F213 deformation-potential vertex
    |g_q|^2 ∝ D^2 q^2/(2 rho omega_q) ∝ D^2 q/(2 rho c_s), Fermi-surface averaged
    over q in [0, 2k_F] (spherical FS phase space ∝ q dq), and delta(omega-c_s q)
    give the standard low-frequency form

        alpha^2 F(omega) = A omega^2   for 0 < omega < omega_max,   0 otherwise,

    with omega_max = 2 c_s k_F (or the Debye cutoff, whichever is smaller).  The
    weight A is fixed by the coupling: lambda = 2 int alpha^2F/omega d omega
    = A omega_max^2, so A = lambda/omega_max^2.  Returns alpha^2F(omega)."""
    w = np.asarray(omega, dtype=float)
    return np.where((w > 0) & (w < omega_max), lam * w ** 2 / omega_max ** 2, 0.0)


def omega_max_from_omega_log(omega_log):
    """For the Debye alpha^2F ∝ omega^2, omega_log = omega_max/sqrt(e), so
    omega_max = sqrt(e) omega_log.  Lets the model reuse the (elastic-sector)
    omega_log to fix the spectrum with no extra input."""
    return math.sqrt(math.e) * omega_log


def omega_log_of_alpha2F_debye(omega_max):
    """omega_log = exp[(2/lambda) int alpha^2F ln(omega)/omega d omega] evaluated
    on the omega^2 spectrum = omega_max/sqrt(e).  (Consistency check.)"""
    return omega_max / math.sqrt(math.e)


def lambda_nu_debye(nu, lam, omega_max):
    """Matsubara coupling for the omega^2 Debye spectrum, closed form:
        lambda(nu) = 2 int_0^{wmax} alpha^2F(w) w/(w^2+nu^2) dw
                   = lambda [ 1 - (nu^2/wmax^2) ln(1 + wmax^2/nu^2) ].
    lambda(0)=lambda; decays ~ lambda wmax^2/(3 nu^2) at large nu."""
    nu2 = np.asarray(nu, dtype=float) ** 2
    safe = np.where(nu2 > 0, nu2, 1.0)
    val = lam * (1.0 - (nu2 / omega_max ** 2) * np.log1p(omega_max ** 2 / safe))
    return np.where(nu2 > 0, val, lam)


def _lambda_matrix(T, N, spectrum, lam, omega_E=None, omega_max=None):
    """lambda(n-m) matrix for either the 'einstein' or 'debye' spectrum."""
    idx = np.arange(-N, N)
    nu = 2.0 * math.pi * T * (idx[:, None] - idx[None, :])
    if spectrum == "einstein":
        return lam * omega_E ** 2 / (omega_E ** 2 + nu ** 2)
    elif spectrum == "debye":
        return lambda_nu_debye(nu, lam, omega_max)
    raise ValueError("spectrum must be 'einstein' or 'debye'")


_N_MAX = 1400   # cap Matsubara half-size (memory guard during T searches)


def _cutoff_scale(spectrum, omega_E, omega_max):
    """Characteristic phonon scale used to size the Matsubara grid."""
    return omega_E if spectrum == "einstein" else omega_max


def eliashberg_solve(T, lam, omega_E, mustar, N=None, omega_c_factor=6.0,
                     tol=1e-10, maxit=2000, spectrum="einstein", omega_max=None):
    """Self-consistent imaginary-axis (Z, Delta) at temperature T.
    Returns dict with omega_n, Z_n, Delta_n (kelvin).  Delta collapses to 0
    above T_c.  spectrum='einstein' (single mode omega_E) or 'debye' (the
    first-principles omega^2 spectrum with cutoff omega_max)."""
    scale = _cutoff_scale(spectrum, omega_E, omega_max)
    if N is None:
        N = min(_N_MAX, max(64, int(omega_c_factor * scale / (2.0 * math.pi * T)) + 8))
    w = _matsubara(T, N)
    L = _lambda_matrix(T, N, spectrum, lam, omega_E, omega_max)
    # mu* only within the cutoff window |omega_m| < omega_c
    omega_c = omega_c_factor * scale
    mu_mask = (np.abs(w) < omega_c).astype(float)
    Mmu = mustar * mu_mask[None, :]
    Delta = np.full(2 * N, 0.1 * scale)             # seed
    for _ in range(maxit):
        denom = np.sqrt(w ** 2 + Delta ** 2)
        Z = 1.0 + (math.pi * T / w) * (L @ (w / denom))
        phi = math.pi * T * ((L - Mmu) @ (Delta / denom))   # = Z*Delta
        Delta_new = phi / Z
        if np.max(np.abs(Delta_new - Delta)) < tol * scale:
            Delta = Delta_new
            break
        Delta = 0.5 * Delta + 0.5 * Delta_new        # damped mixing
    denom = np.sqrt(w ** 2 + Delta ** 2)
    Z = 1.0 + (math.pi * T / w) * (L @ (w / denom))
    return {"omega_n": w, "Z": Z, "Delta": Delta, "N": N}


def eliashberg_tc_eigenvalue(T, lam, omega_E, mustar, N=None, omega_c_factor=6.0,
                             spectrum="einstein", omega_max=None):
    """Largest eigenvalue rho(T) of the LINEARIZED (Delta->0) gap kernel.
    T_c is where rho = 1.  Power iteration (real matrix; avoids np.linalg on
    the off-diagonal, per the CLAUDE.md numpy caveat)."""
    scale = _cutoff_scale(spectrum, omega_E, omega_max)
    if N is None:
        N = min(_N_MAX, max(64, int(omega_c_factor * scale / (2.0 * math.pi * T)) + 8))
    w = _matsubara(T, N)
    aw = np.abs(w)
    L = _lambda_matrix(T, N, spectrum, lam, omega_E, omega_max)
    # linearized Z_n = 1 + (pi T/omega_n) sum_m lambda(n-m) sgn(omega_m)
    Z = 1.0 + (math.pi * T / w) * (L @ np.sign(w))
    omega_c = omega_c_factor * scale
    mu_mask = (aw < omega_c).astype(float)
    Mmu = mustar * mu_mask[None, :]
    # Delta_n = (pi T/Z_n) sum_m [lambda(n-m) - mu*] Delta_m/|omega_m|
    M = (math.pi * T) * (L - Mmu) / (Z[:, None] * aw[None, :])
    # power iteration for the largest eigenvalue
    v = np.ones(2 * N) / math.sqrt(2 * N)
    rho = 0.0
    for _ in range(3000):
        u = M @ v
        rho_new = np.linalg.norm(u)
        v = u / rho_new
        if abs(rho_new - rho) < 1e-12:
            rho = rho_new
            break
        rho = rho_new
    return rho


def eliashberg_tc(lam, omega_E, mustar, omega_c_factor=6.0,
                  spectrum="einstein", omega_max=None):
    """Dynamic T_c from (lambda, omega_E, mu*) by solving rho(T_c)=1 --
    NO McMillan/Allen-Dynes fit.  Returns T_c in the same units as omega_E.
    spectrum='debye' uses the first-principles omega^2 spectral function with
    cutoff omega_max (default sqrt(e)*omega_E so omega_log==omega_E)."""
    if spectrum == "debye" and omega_max is None:
        omega_max = omega_max_from_omega_log(omega_E)
    scale = _cutoff_scale(spectrum, omega_E, omega_max)
    f = lambda T: eliashberg_tc_eigenvalue(T, lam, omega_E, mustar,
                                           omega_c_factor=omega_c_factor,
                                           spectrum=spectrum, omega_max=omega_max) - 1.0
    # rho decreases with T; bracket around the Allen-Dynes guess
    guess = allen_dynes_tc(lam, mustar, omega_E)
    lo, hi = max(1e-4 * scale, 0.02 * guess), max(3.0 * guess, 0.05 * scale)
    # expand bracket if needed
    for _ in range(40):
        if f(lo) > 0 and f(hi) < 0:
            break
        if f(lo) < 0:
            lo *= 0.5
        if f(hi) > 0:
            hi *= 1.5
    return _bisect(f, lo, hi, tol=1e-6)


def eliashberg_Z0(lam, omega_E, mustar, T_over_Tc=0.3):
    """Low-frequency renormalization Z(i omega_0) at T = T_over_Tc * T_c;
    should approach 1 + lambda (the mass renormalization)."""
    Tc = eliashberg_tc(lam, omega_E, mustar)
    sol = eliashberg_solve(T_over_Tc * Tc, lam, omega_E, mustar)
    # omega_0 is the smallest positive Matsubara freq
    w = sol["omega_n"]
    i0 = np.argmin(np.abs(w - math.pi * T_over_Tc * Tc))
    return sol["Z"][i0]


# ===========================================================================
# Padé (Vidberg-Serene) analytic continuation Delta(i omega_n) -> Delta(omega)
# and the DYNAMIC strong-coupling gap ratio 2 Delta_0/kTc
# ===========================================================================
def _pade_continue_mp(zs, us, z_eval, prec=60):
    """Vidberg-Serene continued-fraction Padé at high precision (mpmath).
    zs, us: Matsubara points (i omega_n) and Delta values; z_eval: real-axis
    evaluation points (omega + i eta).  Returns list of mpc Delta(z_eval)."""
    import mpmath as mp
    mp.mp.dps = prec
    M = len(zs)
    zs = [mp.mpc(z) for z in zs]
    us = [mp.mpc(u) for u in us]
    # coefficients a_i = g_i(z_i)
    g_prev = list(us)
    a = [us[0]]
    for i in range(1, M):
        g_cur = [mp.mpc(0)] * M
        for j in range(i, M):
            g_cur[j] = (g_prev[i - 1] - g_prev[j]) / ((zs[j] - zs[i - 1]) * g_prev[j])
        a.append(g_cur[i])
        g_prev = g_cur
    out = []
    for z in z_eval:
        z = mp.mpc(z)
        A0, A1 = mp.mpc(0), a[0]
        B0, B1 = mp.mpc(1), mp.mpc(1)
        for n in range(1, M):
            A2 = A1 + (z - zs[n - 1]) * a[n] * A0
            B2 = B1 + (z - zs[n - 1]) * a[n] * B0
            A0, A1 = A1, A2
            B0, B1 = B1, B2
        out.append(A1 / B1)
    return out


def gap_edge_real_axis(lam, omega_E, mustar, spectrum="einstein", omega_max=None,
                       T_over_Tc=0.15, n_pade=48, eta=1e-3):
    """Analytically continue the low-T Matsubara gap to the real axis and return
    the gap edge Delta_0 (kelvin): the solution of omega = Re Delta(omega),
    which for weak coupling reduces to the BCS gap.  Uses the first n_pade
    positive Matsubara points."""
    if spectrum == "debye" and omega_max is None:
        omega_max = omega_max_from_omega_log(omega_E)
    Tc = eliashberg_tc(lam, omega_E, mustar, spectrum=spectrum, omega_max=omega_max)
    T = T_over_Tc * Tc
    sol = eliashberg_solve(T, lam, omega_E, mustar, spectrum=spectrum,
                           omega_max=omega_max)
    w = sol["omega_n"]; D = sol["Delta"]
    pos = w > 0
    wp = w[pos][:n_pade]; Dp = D[pos][:n_pade]
    zs = [1j * wi for wi in wp]
    # scan omega = Re Delta(omega) on a grid up to a few * Delta(iw0)
    D0_guess = float(Dp[0])
    grid = np.linspace(0.05 * D0_guess, 4.0 * D0_guess, 60)
    zev = [g + 1j * eta * omega_E for g in grid]
    vals = _pade_continue_mp(zs, Dp.tolist(), zev)
    reD = np.array([float(v.real) for v in vals])
    diff = grid - reD                    # gap edge where omega = Re Delta
    edge = None
    for i in range(len(grid) - 1):
        if diff[i] < 0 and diff[i + 1] >= 0:     # crossing 0 from below
            # linear interpolate
            t = -diff[i] / (diff[i + 1] - diff[i])
            edge = grid[i] + t * (grid[i + 1] - grid[i])
            break
    if edge is None:
        edge = reD[0]                    # fallback: Re Delta(omega->0)
    return {"Delta0_K": edge, "Tc_K": Tc, "ratio": 2.0 * edge / Tc}


def gap_ratio_dynamic(lam, omega_E, mustar, spectrum="einstein"):
    """Dynamic strong-coupling reduced gap 2 Delta_0/kTc from Padé continuation
    of the Eliashberg solution -- no fit formula."""
    return gap_edge_real_axis(lam, omega_E, mustar, spectrum=spectrum)["ratio"]


if __name__ == "__main__":  # pragma: no cover
    print("Phi0 = h/2e =", PHI0_PAIR, "Wb")
    print("BCS ratio weak-coupling limit 2pi/e^gamma =",
          bcs_ratio_weak_coupling_limit())
    print("specific-heat jump 12/(7 zeta3) =", specific_heat_jump())
    for nv in (0.10, 0.05, 0.02):
        print(f"  N0V={nv:>4}: 2Delta/kTc =", universal_gap_ratio(nv, 1.0))
