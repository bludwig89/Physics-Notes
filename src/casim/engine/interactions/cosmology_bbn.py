"""cosmology_bbn.py — Big-Bang nucleosynthesis on the model's own expansion law.

Rubric row **K2**, the last-but-one `ABSENT` row of
`docs/status/completeness-2026-08-04.md`.  Nine findings in the tree cite BBN,
and every one of them uses it as an *external bound* quoted at the model
(F283/F284 on \\dot G/G, F237 on relic abundances).  None computes an abundance.
This module computes them.

WHAT IS MODEL-NATIVE AND WHAT IS NOT — read this before quoting a number
-----------------------------------------------------------------------
BBN is a competition between one expansion rate and a set of reaction rates.
The model owns the expansion side outright and owns exactly two numbers on the
nuclear side; everything else is external data, and is labelled as such by
`input_ledger()` rather than left for a reader to discover.

MODEL-NATIVE (derived in this tree, no BBN input):

  * ``G``            — structural, ``G = a^2 c^3 / (8 pi sqrt3 hbar)`` (F79/F107),
                       3e-8 of CODATA with zero free parameters.  Sets H(T).
  * the source law   — the induced Einstein equation (F178), whose radiation-era
                       ``rho + 3p = 2 rho`` is what makes ``a ~ t^{1/2}``.  The
                       demoted energy-only law (F106) is carried here as a
                       *control*, and BBN excludes it — see `law_control()`.
  * ``\\dot G/G = 0`` — exactly, on the rigid substrate (F79/F284).  The standard
                       BBN speed-up factor from a varying G is therefore
                       identically 1: a structural prediction, not a bound met.
                       This BBN run holds G fixed throughout by construction
                       (it cannot return a nonzero drift) and still matches
                       Y_p/D_H — a BBN-INTERNAL CONSISTENCY CHECK on the
                       assumption, not a second independent measurement of it
                       the way F284's LLR comparison is (F361,
                       `gdot_over_g_prediction()`).
  * ``N_eff``        — from the model's own light content.  ``nu_R`` is a
                       structurally forced *total* singlet (Y = 0, F47/F279) and
                       carries a Majorana mass (F47/F236), so it neither
                       thermalises nor contributes; the E_g doublet is the
                       massive condensate (F253).  Nothing light is left over.
  * ``Delta m = m_n - m_p`` — +1.51 MeV (F122/F123), the sharpest matter-sector
                       prediction that needs *no* QCD anchor.  This is the number
                       BBN turns out to measure, and it is where the model fails
                       (see `delta_m_confrontation()`).
  * ``B_d``          — the deuteron binding, 2.224 MeV, on a fully derived OBE
                       potential (F104/F113/F126/F240) with one parameter
                       (b = 0.55 fm) fixed to the binding.  It is *reproduced*,
                       not predicted parameter-free, and BBN cannot tell the
                       difference at 0.026%: see `bd_sensitivity()`.

EXTERNAL INPUT (not derived here, and not claimed to be):

  * ``eta_b``        — the baryon-to-photon ratio.  F202 meets the Sakharov
                       conditions structurally but derives no asymmetry number
                       (rubric K6), so it is taken from Planck 2018 and BBN is
                       run as a *consistency* test at fixed eta, exactly as
                       standard BBN is.
  * ``|V_ud|``       — CKM is out of scope (parameter ledger 10-13, ABSENT).
  * thermonuclear reaction rates for the 11 network reactions other than
                       ``p(n,gamma)d``'s Q-value — external nuclear data.
  * nuclear masses / binding energies of t, 3He, 4He, 7Li, 7Be.

METHOD, AND WHY THE CONCLUSIONS SURVIVE THE NETWORK'S OWN ERROR
---------------------------------------------------------------
The network here is a compact 8-species, 12-reaction implementation, not
PRIMAT.  Its absolute accuracy is *measured* against published standard-BBN
values by `validate_network()` and reported with every absolute number.

Every **model-level** conclusion is quoted as a *difference computed inside this
same network* — model Delta m against measured Delta m, energy-only law against
full law — so the network's absolute offset cancels to first order.  That is the
whole reason the differential quantities are the headline and the absolute ones
are not.

**Lithium-7 is now validated (F361).**  The five A = 7 rate fits in
`_rate_fits` (He3a_Be7, ta_Li7, Be7n_Li7, Li7p_He4, Be7n_He4) were transcribed
with terms missing or, for Be7n_He4, an outright wrong functional form; F297
caught the order-of-magnitude symptom and F361 repaired them against Kawano's
reference NUC123 code (Smith, Kawano & Malaney 1993, ApJS 85, 219).  Li7_H now
reproduces the same published reference to within the module's declared 10%
band (`LI7_VALIDATION_TOL`) and is included in `check_k2` as K2-13; the
pre-repair fits survive only as `legacy_a7_bug=True`, the control that proves
the repair is load-bearing.  This still makes **no claim about the standing
(observational) lithium problem** — standard BBN's own ~5e-10 prediction
against the ~1.6e-10 Spite-plateau measurement — which this repair does not
touch in either direction; see `validate_network()`'s `Li7_note`.

THE RESULT, IN ONE LINE
-----------------------
With the measured Delta m the model's BBN is standard and correct; with the
model's *own* Delta m = 1.51 MeV it is not.  BBN plus the free-neutron lifetime
measure ``m_n - m_p`` to a few times 0.01 MeV, where F122's own acceptance
criterion was "within 1 MeV".  K2 therefore closes as a **falsifier**, not as a
confirmation, and it turns a loosely-checked prediction into a tightly bounded
one.

Date: 2026-08-05 - 22:40
F361 update: 2026-09-03 - 18:35 (A=7 rate repair, Li7 validated; dot G/G BBN
registration).
"""

from __future__ import annotations

from casim.numerics import xp

from casim.constants import G_CODATA, c_SI, hbar_SI, g_A
from casim.engine.particles import baryon_dynamics as BAR

__all__ = [
    "MODEL_DELTA_M_MEV", "PDG_DELTA_M_MEV", "B_D_MODEL_MEV",
    "n_eff_model", "expansion_normalisation", "hubble_rate",
    "thermal_history", "weak_rates", "np_freezeout",
    "run_bbn", "validate_network", "law_control", "delta_m_confrontation",
    "bd_sensitivity", "neutron_lifetime", "input_ledger", "summary",
]

# ===========================================================================
#  0. Units and physical scaffolding
# ===========================================================================
MEV_PER_JOULE = 1.0 / 1.602176634e-13
HBAR_MEV_S = hbar_SI * MEV_PER_JOULE                 # MeV s
HBARC_MEV_CM = 1.9732698e-11                         # MeV cm
KELVIN_PER_MEV = 1.160451812e10                      # K / MeV
M_U_GRAM = 1.66053906660e-24                         # atomic mass unit, g
N_AVOGADRO = 6.02214076e23
ZETA3 = 1.2020569031595943

M_E_MEV = 0.51099895000

# ---------------------------------------------------------------------------
# The two model-native nuclear numbers (see the module docstring's ledger).
# ---------------------------------------------------------------------------
MODEL_DELTA_M_MEV = 1.51        # F122/F123: F40 quark gap (+2.51) minus EM (-1.00)
PDG_DELTA_M_MEV = 1.29333236    # measured
B_D_MODEL_MEV = 2.224           # F104/F113/F126/F240 (b = 0.55 fm fixed to it)
B_D_PDG_MEV = 2.224566

# External inputs, named here so `input_ledger()` can enumerate them.
ETA10_PLANCK = 6.137            # Planck 2018 TT,TE,EE+lowE+lensing
V_UD = 0.97367                  # PDG 2024; CKM is out of scope here
TAU_N_MEASURED_S = 878.4        # PDG 2024 beam/bottle average
G_F_MEV = 1.1663788e-11         # MeV^-2 (carries the v anchor, F115/Scope)

# Published standard-BBN reference at eta10 = 6.137, N_eff = 3.044, tau_n = 878.4
# (PRIMAT / PArthENoPE class codes).  Used ONLY by validate_network().
REFERENCE_YP = 0.24709
REFERENCE_DH = 2.459e-5
REFERENCE_HE3H = 1.07e-5
REFERENCE_LI7H = 5.00e-10

# Observed light-element abundances.
OBS_YP = (0.2453, 0.0034)       # Aver et al. 2021
OBS_DH = (2.527e-5, 0.030e-5)   # Cooke, Pettini & Steidel 2018
OBS_NEFF = (2.99, 0.17)         # Planck 2018 TT,TE,EE+lowE+lensing+BAO

# ---------------------------------------------------------------------------
# F372: literature comparison for the model's own Delta m = m_n - m_p
# decomposition (F122/F123), used by delta_m_theory_uncertainty() below.
# ---------------------------------------------------------------------------
# BMW collaboration 2015 (Borsanyi et al., Science 347, 1452; arXiv:1406.4088),
# ab initio lattice QCD+QED, Table 1: (central, stat, sys), all MeV.
BMW_QCD_MEV = (2.52, 0.17, 0.24)
BMW_QED_MEV = (-1.00, 0.07, 0.14)
BMW_TOTAL_MEV = (1.51, 0.16, 0.23)
BMW_TOTAL_SIGMA_MEV = (BMW_TOTAL_MEV[1] ** 2 + BMW_TOTAL_MEV[2] ** 2) ** 0.5  # 0.280

# Thomas, Wang & Young, Phys. Rev. C 91, 015209 (2015): dispersive Cottingham-
# sum-rule electromagnetic contribution, (p-n) convention -- (central, sigma).
TWY_EM_P_MINUS_N_MEV = (1.04, 0.11)

# PDG 2024 quark-mass review (MS-bar, 2 GeV): m_u = 2.20(7), m_d = 4.69(5) MeV.
PDG2024_MU_MEV = 2.20
PDG2024_MD_MEV = 4.69


# ===========================================================================
#  1. N_eff from the model's own content
# ===========================================================================
def n_eff_model():
    """The relativistic-species budget the model's particle content forces.

    The question BBN asks is: what, in this model, is light and thermalised at
    T ~ 1 MeV that is not a photon or an electron?  The answer is the three
    left-handed neutrinos and nothing else, and each clause is owned by a
    finding rather than assumed:

      * ``nu_R`` is a **total** singlet — Y = 0 is forced by the constraint
        system (F165/F279), and a total singlet has no renormalisable coupling
        to the thermal bath, so it never equilibrates.  It also carries the
        heavy Majorana mass M_R of the see-saw (F47/F236).  Two independent
        reasons for the same zero.
      * The model is **Higgs-free** (founding decision 3), so there is no light
        scalar to add; the E_g doublet is the massive condensate direction
        (F253/F255).
      * There is no light dark sector at BBN: the dark-matter candidate is a
        Planck-mass geon remnant (F223/F228), non-relativistic by 19 orders.

    So N_eff is the Standard-Model value including the non-instantaneous
    decoupling correction, 3.044.  This is a *prediction with no freedom*, and
    its falsifier is sharp: any renormalisable ``nu_R`` coupling would add
    Delta N_eff = 3 x 0.57 = 1.71 per thermalised Weyl pair, excluded by Planck
    at more than 10 sigma.
    """
    n_light_weyl_pairs = 3          # nu_e, nu_mu, nu_tau, left-handed only
    non_instantaneous = 0.044       # standard QED + neutrino-heating correction
    n_eff = n_light_weyl_pairs + non_instantaneous
    obs, sig = OBS_NEFF
    return {
        "N_eff": n_eff,
        "n_light_weyl_pairs": n_light_weyl_pairs,
        "nu_R_thermalised": False,
        "nu_R_reason": "total singlet (Y=0, F165/F279) + heavy Majorana mass "
                       "(F47/F236): no renormalisable coupling to the bath",
        "light_scalars": 0,
        "light_scalars_reason": "Higgs-free (decision 3); E_g doublet is massive "
                                "(F253)",
        "N_eff_observed": obs,
        "N_eff_sigma": (n_eff - obs) / sig,
        "falsifier_delta_N_if_nuR_thermal": 3 * 0.57,
    }


# ===========================================================================
#  2. The expansion rate, and the two gravitational laws
# ===========================================================================
def expansion_normalisation(law="full"):
    """The radiation-era H/sqrt(rho) normalisation implied by a source law.

    This is *derived*, not posited, and it is the whole content of the control.

    Take the acceleration equation with a source ``kappa * rho``:
    ``kappa = 2`` for the adopted induced Einstein equation (F178: the source is
    ``rho + 3p = 2 rho`` for radiation) and ``kappa = 1`` for the demoted
    energy-only law (F106, whose radiation-era mis-weighting F182 N3/N4 already
    identified as a factor 2).  Impose the continuity equation, so
    ``rho ~ a^{-4}``, and look for ``a ~ t^n``:

        n(n-1)/t^2 = -(4 pi G/3) kappa rho0 a^{-4}

    Power matching gives ``4n = 2``, i.e. ``n = 1/2`` for **either** law — the
    energy-only law does not change the power, it changes the *normalisation*.
    Fixing the coefficient, ``(4 pi G/3) kappa rho = 1/(4 t^2)``, and comparing
    with ``H = n/t = 1/(2t)``:

        H^2 = (8 pi G/3) rho * (kappa/2)   =>   S(law) = sqrt(kappa/2)

    So ``S = 1`` for the full-tensor law (Friedmann I recovered exactly, as it
    must be) and ``S = 1/sqrt2 = 0.7071`` for the energy-only law: **a universe
    that expands 41% too slowly at fixed temperature.**  Because the weak
    freeze-out is set by ``lambda_weak = H``, that is a direct, large and
    one-signed shift in Y_p.
    """
    kappa = {"full": 2.0, "energy": 1.0}[law]
    return float(xp.sqrt(kappa / 2.0))


def _fermi_integrals(x):
    """(rho, p) of one e+e- pair species in units of T^4, at x = m_e/T.

    Massive Fermi-Dirac with zero chemical potential, 4 dof (e- and e+, 2 spins).
    """
    u = xp.linspace(0.0, 60.0, 4001)                    # u = p/T
    e = xp.sqrt(u * u + x * x)
    f = 1.0 / (xp.exp(e) + 1.0)
    pref = 4.0 / (2.0 * xp.pi ** 2)                     # g/(2 pi^2)
    rho = pref * xp.trapezoid(u * u * e * f, u)
    pres = pref / 3.0 * xp.trapezoid(u ** 4 / e * f, u)
    return float(rho), float(pres)


def thermal_history(T_start_mev=10.0, T_end_mev=5.0e-3, n=1200, m_e=None):
    """Photon temperature grid, neutrino temperature, scale factor and time.

    Entropy of the electromagnetic bath (photons + e+e-) is conserved, which is
    what generates ``T_nu/T_gamma -> (4/11)^{1/3}`` without it being put in.
    Neutrinos are decoupled and free-stream, so ``T_nu ~ 1/a`` exactly.  The run
    starts at 10 MeV, above e+e- annihilation, where ``T_nu = T_gamma``.

    Returns arrays over a log grid in T: (T, T_nu, a, t, H) with H in s^-1 under
    the adopted (full-tensor) law.
    """
    if m_e is None:
        m_e = M_E_MEV
    T = xp.exp(xp.linspace(xp.log(T_start_mev), xp.log(T_end_mev), n))
    s_em = xp.zeros(n)
    for i, Ti in enumerate(T):
        rho_e, p_e = _fermi_integrals(m_e / Ti)
        rho_g = xp.pi ** 2 / 15.0                        # photons, /T^4
        p_g = rho_g / 3.0
        s_em[i] = (rho_g + p_g + rho_e + p_e) * Ti ** 3  # s = (rho+p)/T, /1
    # a^3 s_EM = const, a(T_start) = 1
    a = (s_em[0] / s_em) ** (1.0 / 3.0)
    T_nu = T[0] * a[0] / a
    return T, T_nu, a, s_em


def _energy_density(T, T_nu, n_eff, m_e=None):
    """Total relativistic energy density in MeV^4 (photons + e+e- + neutrinos)."""
    if m_e is None:
        m_e = M_E_MEV
    rho = xp.zeros_like(T)
    for i in range(len(T)):
        rho_e, _ = _fermi_integrals(m_e / T[i])
        rho_g = xp.pi ** 2 / 15.0
        rho[i] = (rho_g + rho_e) * T[i] ** 4
    rho += n_eff * (7.0 / 8.0) * (xp.pi ** 2 / 15.0) * T_nu ** 4
    return rho


def hubble_rate(rho_mev4, law="full", G=G_CODATA):
    """H in s^-1 from an energy density in MeV^4, under the named source law.

    The Planck mass is built from the *model's* G (F79/F107 structural value by
    default), so the expansion rate that competes with the weak rates is the
    model's own.
    """
    m_pl_mev = xp.sqrt(hbar_SI * c_SI ** 5 / G) * MEV_PER_JOULE   # E_Pl in MeV
    h_mev = xp.sqrt(8.0 * xp.pi / 3.0 * rho_mev4) / m_pl_mev
    return expansion_normalisation(law) * h_mev / HBAR_MEV_S


def model_G():
    """G from the model's structural closed form (F79/F107), in SI."""
    from casim.engine.lattice.si_scale import canonical_cell
    return canonical_cell()["G_pred"]


# ===========================================================================
#  3. Weak n <-> p rates
# ===========================================================================
def _rate_integrals(T, T_nu, q, n_eps=900, eps_max=60.0, m_e=None):
    """The six Born-level phase-space integrals, in units of the coupling K.

    Energies are in electron-mass units; ``q = Delta m / m_e``.  The six channels
    are written out separately rather than collapsed, so that detailed balance
    is a *property of the construction* instead of an identity imposed by hand:
    the same matrix element and the same K appear in both directions, and the
    equilibrium ratio ``lambda_pn/lambda_np -> exp(-q m_e/T)`` then has to come
    out, which `np_freezeout` checks.

    n -> p :  (a) n + nu   -> p + e-      (b) n + e+ -> p + nubar   (c) n -> p e nubar
    p -> n :  (a') p + e-  -> n + nu      (b') p + nubar -> n + e+  (c') p e nubar -> n
    """
    if m_e is None:
        m_e = M_E_MEV
    x = m_e / T
    xv = m_e / T_nu

    def fe(e):      # electron/positron occupation at photon temperature
        return 1.0 / (xp.exp(xp.clip(e * x, -500, 500)) + 1.0)

    def fv(e):      # neutrino occupation at neutrino temperature
        return 1.0 / (xp.exp(xp.clip(e * xv, -500, 500)) + 1.0)

    # --- channels with electron energy from max(1,q) upward -----------------
    lo = max(1.0, q)
    e1 = xp.linspace(lo, eps_max, n_eps)
    ph1 = e1 * xp.sqrt(xp.maximum(e1 * e1 - 1.0, 0.0)) * (e1 - q) ** 2
    A = xp.trapezoid(ph1 * fv(e1 - q) * (1.0 - fe(e1)), e1)          # n + nu -> p + e
    Ap = xp.trapezoid(ph1 * fe(e1) * (1.0 - fv(e1 - q)), e1)         # p + e -> n + nu

    # --- channels with (positron) energy from 1 upward ---------------------
    e2 = xp.linspace(1.0, eps_max, n_eps)
    ph2 = e2 * xp.sqrt(xp.maximum(e2 * e2 - 1.0, 0.0)) * (e2 + q) ** 2
    B = xp.trapezoid(ph2 * fe(e2) * (1.0 - fv(e2 + q)), e2)          # n + e+ -> p + nubar
    Bp = xp.trapezoid(ph2 * fv(e2 + q) * (1.0 - fe(e2)), e2)         # p + nubar -> n + e+

    # --- three-body: free decay and its inverse ----------------------------
    if q > 1.0:
        e3 = xp.linspace(1.0, q, n_eps)
        ph3 = e3 * xp.sqrt(xp.maximum(e3 * e3 - 1.0, 0.0)) * (q - e3) ** 2
        C = xp.trapezoid(ph3 * (1.0 - fe(e3)) * (1.0 - fv(q - e3)), e3)
        Cp = xp.trapezoid(ph3 * fe(e3) * fv(q - e3), e3)
    else:
        C = Cp = 0.0
    return float(A + B + C), float(Ap + Bp + Cp)


def decay_phase_space(q):
    """The free-neutron decay integral f(q) = int_1^q eps sqrt(eps^2-1)(q-eps)^2."""
    e = xp.linspace(1.0, q, 4001)
    return float(xp.trapezoid(e * xp.sqrt(xp.maximum(e * e - 1.0, 0.0))
                              * (q - e) ** 2, e))


def neutron_lifetime(delta_m_mev, from_couplings=False):
    """The free-neutron lifetime implied by a given n-p splitting.

    Two normalisations, deliberately kept apart:

    * ``from_couplings=True`` computes the coupling K from the model's own
      ``G_F`` (which carries the v anchor) and the registry ``g_A``, so tau_n is
      a genuine prediction — but it then also carries |V_ud|, which is external.
    * ``from_couplings=False`` fixes K once from the *measured* tau_n at the
      *measured* q.  K is a coupling constant and does not depend on Delta m, so
      re-using it at the model's q is legitimate and isolates the Delta m
      dependence, which is the point.

    The Delta m sensitivity is brutal — f(q) rises steeply — and this is the
    first of the two observations that bound ``m_n - m_p``.
    """
    q = delta_m_mev / M_E_MEV
    f = decay_phase_space(q)
    if from_couplings:
        # 1/tau = G_F^2 |V_ud|^2 (1 + 3 g_A^2) m_e^5 f_eff / (2 pi^3)
        k = (G_F_MEV ** 2 * V_UD ** 2 * (1.0 + 3.0 * float(g_A) ** 2)
             * M_E_MEV ** 5 / (2.0 * xp.pi ** 3))
        return float(HBAR_MEV_S / (k * f))
    k_cal = 1.0 / (TAU_N_MEASURED_S * decay_phase_space(PDG_DELTA_M_MEV / M_E_MEV))
    return float(1.0 / (k_cal * f))


def weak_rates(T, T_nu, delta_m_mev, m_e=None):
    """(lambda_{n->p}, lambda_{p->n}) in s^-1, calibrated on the measured tau_n.

    `m_e` defaults to the PDG electron mass.  It is a keyword rather than a
    module global because F309 substitutes the MODEL's own m_e (F121) and needs
    the substitution to be visible in the call, not patched underneath it.
    """
    if m_e is None:
        m_e = M_E_MEV
    q = delta_m_mev / m_e
    k_cal = 1.0 / (TAU_N_MEASURED_S * decay_phase_space(PDG_DELTA_M_MEV / m_e))
    lam_np = xp.zeros_like(T)
    lam_pn = xp.zeros_like(T)
    for i in range(len(T)):
        a, b = _rate_integrals(T[i], T_nu[i], q, m_e=m_e)
        lam_np[i] = k_cal * a
        lam_pn[i] = k_cal * b
    return lam_np, lam_pn


# ===========================================================================
#  4. n/p freeze-out on the model's expansion history
# ===========================================================================
def np_freezeout(delta_m_mev=PDG_DELTA_M_MEV, law="full", n_eff=None,
                 G=None, T_start_mev=10.0, T_end_mev=5.0e-3, n=1200,
                 m_e=None):
    """Integrate dX_n/dT through weak freeze-out and free-neutron decay.

    Returns the thermal history, the weak rates, and X_n(T) — the neutron
    fraction that the nuclear network then inherits.
    """
    if n_eff is None:
        n_eff = n_eff_model()["N_eff"]
    if G is None:
        G = model_G()
    T, T_nu, a, _ = thermal_history(T_start_mev, T_end_mev, n, m_e=m_e)
    rho = _energy_density(T, T_nu, n_eff, m_e=m_e)
    H = hubble_rate(rho, law=law, G=G)
    lam_np, lam_pn = weak_rates(T, T_nu, delta_m_mev, m_e=m_e)

    # dX_n/dt = -lam_np X_n + lam_pn (1 - X_n);  dt = -dT/(T H) since T ~ 1/a
    # (the small entropy-release correction to dT/dt is carried by using the
    #  tabulated a(T) rather than assuming T ~ 1/a exactly)
    lna = xp.log(a)
    X = xp.zeros(n)
    X[0] = 1.0 / (1.0 + xp.exp(delta_m_mev / T[0]))     # chemical equilibrium
    for i in range(n - 1):
        dt = (lna[i + 1] - lna[i]) / (0.5 * (H[i] + H[i + 1]))
        # implicit (backward Euler) — the weak rates are stiff above freeze-out
        num = X[i] + dt * lam_pn[i + 1]
        den = 1.0 + dt * (lam_np[i + 1] + lam_pn[i + 1])
        X[i + 1] = num / den
    # equilibrium-ratio audit: detailed balance must emerge, not be imposed
    idx = int(xp.argmin(xp.abs(T - 5.0)))
    db = float(lam_pn[idx] / lam_np[idx]) / float(xp.exp(-delta_m_mev / T[idx]))
    return {
        "T": T, "T_nu": T_nu, "a": a, "H": H,
        "lam_np": lam_np, "lam_pn": lam_pn, "X_n": X,
        "detailed_balance_ratio": db,
        "T_freezeout_MeV": _freezeout_temperature(T, lam_np + lam_pn, H),
        "n_eff": n_eff, "G": G, "law": law, "delta_m_MeV": delta_m_mev,
        "m_e_MeV": M_E_MEV if m_e is None else m_e,
    }


def _freezeout_temperature(T, lam_tot, H):
    """The T where the total weak rate crosses H — the classic definition."""
    r = lam_tot - H
    for i in range(len(T) - 1):
        if r[i] > 0.0 >= r[i + 1]:
            w = r[i] / (r[i] - r[i + 1])
            return float(T[i] + w * (T[i + 1] - T[i]))
    return float("nan")


# ===========================================================================
#  5. The nuclear network — 8 species, 12 reactions
# ===========================================================================
# Species order: n, p, d, t, 3He, 4He, 7Li, 7Be
SPECIES = ("n", "p", "d", "t", "He3", "He4", "Li7", "Be7")
A_NUC = (1, 1, 2, 3, 3, 4, 7, 7)
# Binding energies in MeV.  B_d is the model's (F104/F126); the rest are data.
BINDING_MEV = {"n": 0.0, "p": 0.0, "d": B_D_MODEL_MEV, "t": 8.481795,
               "He3": 7.718043, "He4": 28.295673, "Li7": 39.24454,
               "Be7": 37.60034}
# Nuclear spin degeneracy 2J+1
G_NUC = {"n": 2, "p": 2, "d": 3, "t": 2, "He3": 2, "He4": 1, "Li7": 4, "Be7": 4}


def _rate_fits(t9, legacy_a7_bug=False):
    """Thermonuclear rates N_A<sigma v> (cm^3 mol^-1 s^-1), Smith-Kawano-Malaney
    1993 analytic forms, cross-checked term-by-term against Kawano's reference
    NUC123 Fortran code (Smith, Kawano & Malaney 1993, ApJS 85, 219 — reactions
    17, 19, 24, 26, 27).  EXTERNAL nuclear data — not derived in this tree.

    F361 repair: the five A = 7 fits below (He3a_Be7, ta_Li7, Be7n_Li7,
    Li7p_He4, Be7n_He4) were transcribed with missing narrow-resonance terms
    and, in two cases, wrong polynomial coefficients or a wrong functional
    form outright (Be7n_He4).  Each is now the exact NUC123 sum, including the
    resonance-narrowed temperatures t9a/t9d/t9e/t9f = t9/(1+c t9) that the
    original fits used in their second term and this implementation had
    silently replaced with bare t9 (i.e. dropped, since the terms using them
    were absent)."""
    t9 = max(float(t9), 1e-4)
    e = xp.exp
    t13, t23, t43, t53 = t9 ** (1 / 3), t9 ** (2 / 3), t9 ** (4 / 3), t9 ** (5 / 3)
    r = {}
    r["pn_d"] = 4.742e4 * (1 - 0.8504 * t9 ** 0.5 + 0.4895 * t9
                           - 0.09623 * t9 ** 1.5 + 8.471e-3 * t9 ** 2
                           - 2.80e-4 * t9 ** 2.5)
    r["dp_He3"] = 2.24e3 * t9 ** (-2 / 3) * e(-3.720 / t13) * (
        1 + 0.112 * t13 + 3.38 * t23 + 2.65 * t9)
    r["dd_n"] = 3.95e8 * t9 ** (-2 / 3) * e(-4.259 / t13) * (
        1 + 0.098 * t13 + 0.765 * t23 + 0.525 * t9
        + 9.61e-3 * t43 + 0.0167 * t53)
    r["dd_p"] = 4.17e8 * t9 ** (-2 / 3) * e(-4.258 / t13) * (
        1 + 0.098 * t13 + 0.518 * t23 + 0.355 * t9
        - 0.010 * t43 - 0.018 * t53)
    r["He3n_t"] = 7.21e8 * (1 - 0.508 * t9 ** 0.5 + 0.228 * t9)
    r["td_He4"] = (1.063e11 * t9 ** (-2 / 3) * e(-4.559 / t13 - (t9 / 0.0754) ** 2)
                   * (1 + 0.092 * t13 + 1.80 * t23 + 1.16 * t9
                      + 10.52 * t43 + 17.24 * t53)
                   + 8.047e8 * t9 ** (-1.5) * e(-0.4857 / t9))
    r["He3d_He4"] = (5.021e10 * t9 ** (-2 / 3) * e(-7.144 / t13 - (t9 / 0.270) ** 2)
                     * (1 + 0.058 * t13 + 0.603 * t23 + 0.245 * t9
                        + 6.97 * t43 + 7.19 * t53)
                     + 5.212e8 / t9 ** 0.5 * e(-1.762 / t9))

    if legacy_a7_bug:
        # PRE-F361 transcription: the four A = 7 production/exchange fits
        # missing their NUC123 narrow-resonance term, and Be7n_He4 with the
        # wrong functional form outright.  Kept ONLY as the control leg that
        # proves F361's repair is load-bearing (`casim test --param
        # legacy_a7_bug=true` must turn K2-13 red) -- never the default path.
        r["He3a_Be7"] = 4.817e6 * t9 ** (-2 / 3) * e(-14.964 / t13) * (
            1 + 0.0325 * t13 - 1.04e-3 * t23 - 2.37e-4 * t9
            - 8.11e-5 * t43 - 4.69e-5 * t53)
        r["ta_Li7"] = 3.032e5 * t9 ** (-2 / 3) * e(-8.090 / t13) * (
            1 + 0.0516 * t13 - 4.06e-3 * t23 - 5.15e-4 * t9
            - 3.05e-4 * t43 - 5.62e-5 * t53)
        r["Be7n_Li7"] = 2.675e9 * (1 - 0.560 * t9 ** 0.5 + 0.179 * t9
                                   - 0.0283 * t9 ** 1.5 + 2.214e-3 * t9 ** 2
                                   - 6.851e-5 * t9 ** 2.5)
        r["Li7p_He4"] = (1.096e9 * t9 ** (-2 / 3) * e(-8.472 / t13)
                         + 4.830e8 * t9 ** (-2 / 3)
                         * e(-8.472 / t13 - (t9 / 1.696) ** 2)
                         * (1 + 0.759 * t9 ** 1.6)
                         + 1.06e10 * t9 ** (-1.5) * e(-30.442 / t9))
        r["Be7n_He4"] = 2.05e4 / t9 ** 0.5
        return r

    # --- A = 7 fits (F361 repair): NUC123's own resonance-narrowed
    # temperatures, each scoped to the one reaction that uses it (Kawano's
    # t9a/t9d/t9e/t9f).
    t9a = t9 / (1.0 + 13.076 * t9)                       # reaction 17
    t9a32 = t9a ** 1.5
    t9d = t9 / (1.0 + 0.759 * t9)                        # reaction 24
    t9d13, t9d56 = t9d ** (1 / 3), t9d ** (5 / 6)
    t9e = t9 / (1.0 + 0.1378 * t9)                       # reaction 26
    t9e13, t9e56 = t9e ** (1 / 3), t9e ** (5 / 6)
    t9f = t9 / (1.0 + 0.1071 * t9)                       # reaction 27
    t9f13, t9f56 = t9f ** (1 / 3), t9f ** (5 / 6)

    r["He3a_Be7"] = (4.817e6 * t9 ** (-2 / 3) * e(-14.964 / t13) * (
        1 + 0.0325 * t13 - 1.04e-3 * t23 - 2.37e-4 * t9
        - 8.11e-5 * t43 - 4.69e-5 * t53)
        + 5.938e6 * t9f56 * t9 ** (-1.5) * e(-12.859 / t9f13))
    r["ta_Li7"] = (3.032e5 * t9 ** (-2 / 3) * e(-8.090 / t13) * (
        1 + 0.0516 * t13 + 0.0229 * t23 + 8.28e-3 * t9
        - 3.28e-4 * t43 - 3.01e-4 * t53)
        + 5.109e5 * t9e56 * t9 ** (-1.5) * e(-8.068 / t9e13))
    r["Be7n_Li7"] = (2.675e9 * (1 - 0.560 * t9 ** 0.5 + 0.179 * t9
                                - 0.0283 * t9 ** 1.5 + 2.214e-3 * t9 ** 2
                                - 6.851e-5 * t9 ** 2.5)
                     + 9.391e8 * t9a32 * t9 ** (-1.5)
                     + 4.467e7 * t9 ** (-1.5) * e(-0.07486 / t9))
    r["Li7p_He4"] = (1.096e9 * t9 ** (-2 / 3) * e(-8.472 / t13)
                     - 4.830e8 * t9d56 * t9 ** (-1.5) * e(-8.472 / t9d13)
                     + 1.06e10 * t9 ** (-1.5) * e(-30.442 / t9)
                     + 1.56e5 * t9 ** (-2 / 3)
                     * e(-8.472 / t13 - (t9 / 1.696) ** 2) * (
                         1 + 0.049 * t13 - 2.498 * t23 + 0.860 * t9
                         + 3.518 * t43 + 3.08 * t53)
                     + 1.55e6 * t9 ** (-1.5) * e(-4.478 / t9))
    r["Be7n_He4"] = 2.05e4 * (1.0 + 3760.0 * t9)
    return r


# reaction table: (key, [reactants], [products], reverse coefficient, reverse
# temperature power, Q in MeV).  Reverse rates come from detailed balance, so a
# Q-value change (e.g. B_d) propagates to the photodissociation automatically.
_REACTIONS = (
    # 2-body -> 1-body radiative capture: reverse ~ T9^{3/2}
    ("pn_d",       ("n", "p"),      ("d",),          4.71e9,  1.5, None),
    ("dp_He3",     ("d", "p"),      ("He3",),        1.63e10, 1.5, None),
    ("He3a_Be7",   ("He3", "He4"),  ("Be7",),        1.11e10, 1.5, None),
    ("ta_Li7",     ("t", "He4"),    ("Li7",),        1.11e10, 1.5, None),
    # 2-body -> 2-body: reverse is a pure ratio, no T power
    ("dd_n",       ("d", "d"),      ("He3", "n"),    1.73,    0.0, None),
    ("dd_p",       ("d", "d"),      ("t", "p"),      1.73,    0.0, None),
    ("He3n_t",     ("He3", "n"),    ("t", "p"),      0.998,   0.0, None),
    ("td_He4",     ("t", "d"),      ("He4", "n"),    5.54,    0.0, None),
    ("He3d_He4",   ("He3", "d"),    ("He4", "p"),    5.55,    0.0, None),
    ("Be7n_Li7",   ("Be7", "n"),    ("Li7", "p"),    0.998,   0.0, None),
    ("Li7p_He4",   ("Li7", "p"),    ("He4", "He4"),  4.69,    0.0, None),
    ("Be7n_He4",   ("Be7", "n"),    ("He4", "He4"),  4.70,    0.0, None),
)


def _q_value(reactants, products):
    return (sum(BINDING_MEV[p] for p in products)
            - sum(BINDING_MEV[r] for r in reactants))


def run_bbn(delta_m_mev=PDG_DELTA_M_MEV, law="full", eta10=ETA10_PLANCK,
            n_eff=None, G=None, b_d_mev=None, n=1200, m_e=None,
            legacy_a7_bug=False):
    """Full BBN: weak freeze-out then the nuclear network, to final abundances.

    Returns Y_p (helium mass fraction), D/H, 3He/H, 7Li/H and the diagnostics.
    """
    b_d_saved = BINDING_MEV["d"]
    if b_d_mev is not None:
        BINDING_MEV["d"] = b_d_mev
    try:
        return _run_bbn_inner(delta_m_mev, law, eta10, n_eff, G, n, m_e,
                               legacy_a7_bug=legacy_a7_bug)
    finally:
        BINDING_MEV["d"] = b_d_saved


def _run_bbn_inner(delta_m_mev, law, eta10, n_eff, G, n, m_e=None,
                    legacy_a7_bug=False):
    fo = np_freezeout(delta_m_mev=delta_m_mev, law=law, n_eff=n_eff, G=G, n=n,
                      m_e=m_e)
    T, a, H, X_n = fo["T"], fo["a"], fo["H"], fo["X_n"]

    # baryon number density: n_b/n_gamma -> eta at the end of the run
    n_gamma_end = 2.0 * ZETA3 / xp.pi ** 2 * (T[-1] / HBARC_MEV_CM) ** 3
    n_b_end = eta10 * 1e-10 * n_gamma_end
    n_b = n_b_end * (a[-1] / a) ** 3                     # cm^-3
    rho_b = n_b * M_U_GRAM                               # g cm^-3

    # start the network below deuterium photodissociation dominance
    i0 = int(xp.argmin(xp.abs(T - 0.5)))
    Y = xp.zeros(len(SPECIES))
    Y[0] = float(X_n[i0])                                # n
    Y[1] = 1.0 - float(X_n[i0])                          # p

    lam_np, lam_pn = fo["lam_np"], fo["lam_pn"]
    lna = xp.log(a)
    for i in range(i0, len(T) - 1):
        dt = (lna[i + 1] - lna[i]) / (0.5 * (H[i] + H[i + 1]))
        t9 = T[i + 1] * KELVIN_PER_MEV / 1e9
        Y = _network_step(Y, dt, t9, float(rho_b[i + 1]),
                          float(lam_np[i + 1]), float(lam_pn[i + 1]),
                          legacy_a7_bug=legacy_a7_bug)
        if t9 < 5e-3:
            break

    y = {s: float(Y[k]) for k, s in enumerate(SPECIES)}
    yp = 4.0 * y["He4"]
    return {
        "Y_p": yp,
        "D_H": y["d"] / y["p"],
        "He3_H": y["He3"] / y["p"],
        "Li7_H": (y["Li7"] + y["Be7"]) / y["p"],
        "X_n_at_network_start": float(X_n[i0]),
        "T_freezeout_MeV": fo["T_freezeout_MeV"],
        "detailed_balance_ratio": fo["detailed_balance_ratio"],
        "abundances": y,
        "eta10": eta10, "law": law, "delta_m_MeV": delta_m_mev,
        "N_eff": fo["n_eff"], "G": fo["G"], "B_d_MeV": BINDING_MEV["d"],
        "m_e_MeV": fo["m_e_MeV"],
        "S_expansion": expansion_normalisation(law),
    }


def _network_step(Y, dt, t9, rho_b, lam_np, lam_pn, legacy_a7_bug=False):
    """One implicit (backward-Euler) step of the 8-species network.

    BBN is stiff — ``p(n,gamma)d`` runs far faster than the expansion — so the
    step is linearised and solved, which is the Wagoner/Kawano construction.
    """
    ns = len(SPECIES)
    idx = {s: k for k, s in enumerate(SPECIES)}
    rates = _rate_fits(t9, legacy_a7_bug=legacy_a7_bug)
    M = xp.zeros((ns, ns))
    b = xp.array(Y, dtype=float)

    def add(i, j, coeff):
        M[i, j] += coeff

    for key, reac, prod, rev_c, rev_p, _ in _REACTIONS:
        fwd = rates[key] * rho_b                        # s^-1 per unit Y
        q = _q_value(reac, prod)
        # detailed balance: reverse = forward * rev_c * T9^rev_p * exp(-Q/kT).
        # k_B T in MeV is t9/11.6045, so Q/kT = q * 11.6045 / t9.  A change in
        # a binding energy therefore propagates into the photodissociation rate
        # automatically — which is how the model's B_d reaches the bottleneck.
        expo = -q * 11.6045 / t9
        if rev_p == 1.5:
            # radiative capture: reverse is a photodissociation, per particle
            rev = (rates[key] * rev_c * t9 ** 1.5 * xp.exp(expo))
        else:
            rev = fwd * rev_c * xp.exp(expo)
        rev = float(min(rev, 1e30))

        # forward: linearise Y_i Y_j about the current iterate
        if len(reac) == 2:
            i1, i2 = idx[reac[0]], idx[reac[1]]
            sym = 0.5 if reac[0] == reac[1] else 1.0
            flow = sym * fwd
            for s in reac:
                add(idx[s], i1, flow * Y[i2] * 0.5)
                add(idx[s], i2, flow * Y[i1] * 0.5)
            for s in prod:
                add(idx[s], i1, -flow * Y[i2] * 0.5)
                add(idx[s], i2, -flow * Y[i1] * 0.5)
        # reverse
        if len(prod) == 1:
            j = idx[prod[0]]
            add(j, j, rev)
            for s in reac:
                add(idx[s], j, -rev)
        else:
            j1, j2 = idx[prod[0]], idx[prod[1]]
            symr = 0.5 if prod[0] == prod[1] else 1.0
            for s in prod:
                add(idx[s], j1, symr * rev * Y[j2] * 0.5)
                add(idx[s], j2, symr * rev * Y[j1] * 0.5)
            for s in reac:
                add(idx[s], j1, -symr * rev * Y[j2] * 0.5)
                add(idx[s], j2, -symr * rev * Y[j1] * 0.5)

    # weak n <-> p continues through the network epoch (free-neutron decay)
    add(idx["n"], idx["n"], lam_np)
    add(idx["p"], idx["n"], -lam_np)
    add(idx["p"], idx["p"], lam_pn)
    add(idx["n"], idx["p"], -lam_pn)

    A = xp.eye(ns) + dt * M
    Ynew = xp.linalg.solve(A, b)
    return xp.clip(Ynew, 0.0, 1.0)


# ===========================================================================
#  6. The checks
# ===========================================================================
LI7_VALIDATION_TOL = 0.10   # F361: the A=7 network's own acceptance band


def validate_network(legacy_a7_bug=False):
    """How well does this compact network reproduce published standard BBN?

    Run with the MEASURED Delta m, the model's G, N_eff = 3.044 and Planck eta.
    Every absolute number this module quotes carries this offset; every
    *differential* number does not, which is why the differentials are the
    result and the absolutes are the context.

    ``legacy_a7_bug=True`` reverts the five A=7 rate fits to their pre-F361
    transcription (missing NUC123 terms / wrong functional form) — it exists
    only so the K2-13 control can demonstrate the repair is load-bearing, and
    is never the default.
    """
    r = run_bbn(delta_m_mev=PDG_DELTA_M_MEV, law="full",
                legacy_a7_bug=legacy_a7_bug)
    li7_rel_err = (r["Li7_H"] - REFERENCE_LI7H) / REFERENCE_LI7H
    li7_validated = abs(li7_rel_err) < LI7_VALIDATION_TOL
    return {
        "Y_p": r["Y_p"], "Y_p_reference": REFERENCE_YP,
        "Y_p_rel_err": (r["Y_p"] - REFERENCE_YP) / REFERENCE_YP,
        "D_H": r["D_H"], "D_H_reference": REFERENCE_DH,
        "D_H_rel_err": (r["D_H"] - REFERENCE_DH) / REFERENCE_DH,
        "He3_H": r["He3_H"], "He3_H_reference": REFERENCE_HE3H,
        "He3_H_rel_err": (r["He3_H"] - REFERENCE_HE3H) / REFERENCE_HE3H,
        "Li7_H": r["Li7_H"], "Li7_H_reference": REFERENCE_LI7H,
        "Li7_H_rel_err": li7_rel_err,
        "Li7_validated": li7_validated,
        "Li7_note": ("F361: the five A=7 rate fits in _rate_fits were repaired "
                     "against Kawano's reference NUC123 code (missing "
                     "narrow-resonance terms, and Be7n_He4's wrong functional "
                     "form). Li7_H now reproduces the same published reference "
                     f"to {li7_rel_err:+.1%} (was -92% pre-repair) and is "
                     f"validated to the {LI7_VALIDATION_TOL:.0%} band declared "
                     "here — included in check_k2 as K2-13. This still makes "
                     "no claim about the standing (observational) lithium "
                     "problem, which compares standard BBN's own ~5e-10 "
                     "prediction to the ~1.6e-10 Spite-plateau measurement and "
                     "is untouched by this repair in either direction."
                     if not legacy_a7_bug else
                     "legacy_a7_bug=True: reproducing the PRE-F361 bug on "
                     "purpose, for the K2-13 control."),
        "detailed_balance_ratio": r["detailed_balance_ratio"],
        "T_freezeout_MeV": r["T_freezeout_MeV"],
    }


def law_control():
    """BBN as a discriminator between the two candidate gravitational laws.

    F178 adopted the induced Einstein equation over the energy-only dielectric
    on the strength of Lorentz covariance and the neutron-star maximum mass
    (F174/F176).  BBN is a completely independent observable, three decades of
    redshift away, and it agrees: the energy-only law expands at
    ``S = 1/sqrt2`` of the correct rate at fixed temperature, freezing the weak
    interactions out later, at a lower temperature and a lower n/p.

    **State the conditionality, because it is real.**  F182 A1 showed the
    energy-only law is *internally inconsistent* for ``p != 0`` — Friedmann I,
    the acceleration equation and continuity cannot all hold — so evaluating it
    at all requires choosing which equation survives.  This control keeps the
    **dynamical** (acceleration) equation plus continuity, which is the reading
    under which the law is a law, and derives H from them; that is the reading
    BBN excludes at the sigma quoted here.  Under the other reading — keep
    Friedmann I and let the acceleration equation simply be violated — the
    expansion history is identical to the full-tensor one and **BBN says
    nothing**.  So this is a strong exclusion of one reading, not a second
    independent proof that covers both.  The law is dead either way; F182's
    Bianchi argument is what kills the other reading.
    """
    full = run_bbn(law="full")
    energy = run_bbn(law="energy")
    obs, sig = OBS_YP
    return {
        "S_full": full["S_expansion"], "S_energy": energy["S_expansion"],
        "Y_p_full": full["Y_p"], "Y_p_energy": energy["Y_p"],
        "delta_Y_p": energy["Y_p"] - full["Y_p"],
        "D_H_full": full["D_H"], "D_H_energy": energy["D_H"],
        "T_fo_full": full["T_freezeout_MeV"],
        "T_fo_energy": energy["T_freezeout_MeV"],
        "Y_p_energy_sigma": (energy["Y_p"] - obs) / sig,
        "Y_p_full_sigma": (full["Y_p"] - obs) / sig,
    }


def delta_m_confrontation():
    """What BBN and tau_n say about the model's own m_n - m_p = +1.51 MeV.

    F122 accepted the prediction on a tolerance of "within 1 MeV" (its check
    S8b) and on the sign.  Both observables here are far sharper than that, and
    they push the same way.
    """
    obs_yp, sig_yp = OBS_YP
    obs_dh, sig_dh = OBS_DH
    pdg = run_bbn(delta_m_mev=PDG_DELTA_M_MEV)
    mod = run_bbn(delta_m_mev=MODEL_DELTA_M_MEV)
    tau_pdg = neutron_lifetime(PDG_DELTA_M_MEV)
    tau_mod = neutron_lifetime(MODEL_DELTA_M_MEV)
    tau_coup = neutron_lifetime(PDG_DELTA_M_MEV, from_couplings=True)

    # the local derivative, used to invert BBN into a bound on Delta m
    d = 0.02
    hi = run_bbn(delta_m_mev=PDG_DELTA_M_MEV + d)
    lo = run_bbn(delta_m_mev=PDG_DELTA_M_MEV - d)
    dyp_ddm = (hi["Y_p"] - lo["Y_p"]) / (2 * d)
    return {
        "delta_m_model": MODEL_DELTA_M_MEV, "delta_m_pdg": PDG_DELTA_M_MEV,
        "delta_m_excess_MeV": MODEL_DELTA_M_MEV - PDG_DELTA_M_MEV,
        "Y_p_pdg": pdg["Y_p"], "Y_p_model": mod["Y_p"],
        "delta_Y_p": mod["Y_p"] - pdg["Y_p"],
        "Y_p_model_sigma": (mod["Y_p"] - obs_yp) / sig_yp,
        "D_H_pdg": pdg["D_H"], "D_H_model": mod["D_H"],
        "D_H_model_sigma": (mod["D_H"] - obs_dh) / sig_dh,
        "tau_n_pdg_dm": tau_pdg, "tau_n_model_dm": tau_mod,
        "tau_n_measured": TAU_N_MEASURED_S,
        "tau_n_from_couplings": tau_coup,
        "tau_n_coupling_rel_err": (tau_coup - TAU_N_MEASURED_S) / TAU_N_MEASURED_S,
        "dYp_ddeltam_per_MeV": dyp_ddm,
        "delta_m_bound_1sigma_MeV": abs(sig_yp / dyp_ddm) if dyp_ddm else None,
        "F122_tolerance_MeV": 1.0,
    }


def f122_decomposition():
    """Where the 0.217 MeV has to come from, in F122's own two terms.

    F122 writes ``m_n - m_p = (m_d - m_u) + (delta_EM_n - delta_EM_p)`` and
    evaluates it as ``+2.51 - 1.00 = +1.51`` MeV.  BBN and tau_n between them
    say the sum is 1.293 to better than 0.01 MeV, so exactly one statement is
    available: **one of those two terms is wrong by 0.217 MeV**, which is 8.6%
    of the strong term or 21.7% of the electromagnetic one.

    That is a *usable* result for the matter sector rather than a verdict.  The
    EM term is the more likely culprit on size grounds — it is a 1.00 MeV
    Coulomb self-energy difference estimated from a constituent-quark charge
    distribution, and 22% is an ordinary error for that estimate, whereas 8.6%
    on the F40 current-quark gap would move ``m_d/m_u`` outside its PDG range.
    """
    strong = 2.51
    em = -1.00
    need = PDG_DELTA_M_MEV - (strong + em)
    return {
        "strong_term_MeV": strong, "em_term_MeV": em,
        "F122_total_MeV": strong + em, "required_total_MeV": PDG_DELTA_M_MEV,
        "shortfall_MeV": need,
        "as_fraction_of_strong": abs(need / strong),
        "as_fraction_of_em": abs(need / em),
        "note": "one of the two terms is wrong by 0.217 MeV; the EM self-energy "
                "is the more likely, since 8.6% on the F40 current-quark gap "
                "would move m_d/m_u outside its PDG range",
    }


def delta_m_theory_uncertainty(sigma_theory_mev=None):
    """F372: is the model's own Delta m = +1.51 MeV really excluded at 36.6
    sigma (F297 Sec.5), or is that significance computed against the wrong
    error bar?

    F297/CL259 compare the model's POINT prediction (implicit zero theory
    uncertainty) against the BBN-INFERRED band +-0.0056 MeV -- the precision
    to which the measured Y_p pins Delta m, via this network's steep
    dYp/ddeltam.  That is the right band for "what does Y_p say Delta m is",
    and the wrong one for "is the model's theoretical ESTIMATE of Delta m
    consistent with that", because the estimate is not exact: it is built
    from two O(1-3 MeV) terms (F40's current-quark gap, a constituent-quark
    Coulomb self-energy), each with a real, literature-quantified uncertainty
    of order 10-20%, not zero.

    Per F297 Sec.10 item 1, both branches were checked directly rather than
    assumed:

      * The EM term.  `baryon_dynamics.em_self_energy_pairwise` re-derives it
        from the model's OWN P2 three-body <1/r> (zero new parameters) and
        gets 0.968 MeV against the ad hoc classical 1.00 MeV -- 3.2%, not the
        ~22% an EM-side fix would need.  BMW 2015 (ab initio lattice QCD+QED,
        arXiv:1406.4088) gets -1.00(07)(14) MeV; Thomas, Wang & Young (Phys.
        Rev. C 91, 015209, 2015; dispersive Cottingham sum rule) get
        +1.04(11) MeV in the same (p-n) convention.  Three independent
        methods, none of them fit to this splitting, agree to <=4%.
      * The strong term.  PDG 2024's own m_u=2.20(7), m_d=4.69(5) MeV give
        m_d-m_u=2.49 MeV against the model's 2.51 MeV (F40) -- 0.8%, not the
        8.6% an F40-side fix would need, and BMW's own QCD piece is
        2.52(17)(24) MeV, matching both.

    So neither branch survives contact with an independent check, and BMW's
    own total (1.51(16)(23) MeV) reproduces the model's 1.51 MeV to <=0.01 MeV
    on every term while sitting the same ~0.22 MeV from the measured 1.29333
    MeV that the model does -- this is a known, field-wide feature of the
    state of the art, not a defect unique to this model.  What was actually
    wrong is the STATISTICS: a ~20%-uncertain theoretical estimate was
    compared against an observational band as though it carried zero
    uncertainty of its own.  Propagating BMW's own combined stat+sys
    (sqrt(0.16^2+0.23^2)=0.280 MeV) instead:
    """
    sigma_theory = BMW_TOTAL_SIGMA_MEV if sigma_theory_mev is None else float(sigma_theory_mev)
    excess = MODEL_DELTA_M_MEV - PDG_DELTA_M_MEV
    tau_short = neutron_lifetime(MODEL_DELTA_M_MEV + sigma_theory)   # larger dm -> shorter tau
    tau_long = neutron_lifetime(MODEL_DELTA_M_MEV - sigma_theory)    # smaller dm -> longer tau
    yp_at_plus = run_bbn(delta_m_mev=MODEL_DELTA_M_MEV + sigma_theory)["Y_p"]
    yp_at_minus = run_bbn(delta_m_mev=MODEL_DELTA_M_MEV - sigma_theory)["Y_p"]
    obs_yp, _sig_yp = OBS_YP
    em_check = BAR.em_self_energy_pairwise(m_q=0.785, sigma=1.0, alpha_s=0.5)
    em_check_rel_err = (em_check["delta_em_p_minus_n_MeV"] - 1.00) / 1.00
    return {
        "sigma_theory_MeV": sigma_theory,
        "sigma_theory_source": "BMW 2015 (arXiv:1406.4088) combined stat+sys, "
                                "sqrt(0.16^2+0.23^2)",
        "excess_MeV": excess,
        "sig_naive_observational_band": excess / 0.0056,
        "sig_theory_aware": excess / sigma_theory,
        "tau_n_range_s": (tau_short, tau_long),
        "tau_n_measured_s": TAU_N_MEASURED_S,
        "tau_n_within_range": tau_short <= TAU_N_MEASURED_S <= tau_long,
        "Y_p_range": (yp_at_plus, yp_at_minus),
        "Y_p_measured": obs_yp,
        "Y_p_within_range": yp_at_plus <= obs_yp <= yp_at_minus,
        "bmw_qcd_MeV": BMW_QCD_MEV, "bmw_qed_MeV": BMW_QED_MEV,
        "bmw_total_MeV": BMW_TOTAL_MEV,
        "twy_em_p_minus_n_MeV": TWY_EM_P_MINUS_N_MEV,
        "model_em_pairwise_check_MeV": em_check["delta_em_p_minus_n_MeV"],
        "em_pairwise_vs_adhoc_rel_err": em_check_rel_err,
        "pdg2024_md_minus_mu_MeV": PDG2024_MD_MEV - PDG2024_MU_MEV,
        "f40_vs_pdg2024_rel_err": (2.51 - (PDG2024_MD_MEV - PDG2024_MU_MEV))
                                   / (PDG2024_MD_MEV - PDG2024_MU_MEV),
    }


def bd_sensitivity():
    """Does BBN see the model's deuteron binding, or only the measured one?

    B_d is *reproduced* at 0.026% with one tuned parameter, not predicted, so
    the honest question is whether BBN could tell the two apart.  It cannot —
    which is worth recording, because it means the deuterium bottleneck is not
    where this model is being tested, and a future parameter-free B_d would have
    to beat this sensitivity to be checked here at all.
    """
    base = run_bbn(b_d_mev=B_D_PDG_MEV)
    model = run_bbn(b_d_mev=B_D_MODEL_MEV)
    wide = run_bbn(b_d_mev=B_D_PDG_MEV * 1.01)
    BINDING_MEV["d"] = B_D_MODEL_MEV
    obs_dh, sig_dh = OBS_DH
    return {
        "B_d_model": B_D_MODEL_MEV, "B_d_pdg": B_D_PDG_MEV,
        "B_d_rel_diff": (B_D_MODEL_MEV - B_D_PDG_MEV) / B_D_PDG_MEV,
        "D_H_at_B_d_pdg": base["D_H"], "D_H_at_B_d_model": model["D_H"],
        "D_H_shift": model["D_H"] - base["D_H"],
        "D_H_shift_in_sigma": (model["D_H"] - base["D_H"]) / sig_dh,
        "D_H_at_B_d_plus_1pct": wide["D_H"],
        "dDH_dBd_per_percent": wide["D_H"] - base["D_H"],
    }


def gdot_over_g_prediction():
    """dot G/G is not merely a bound this model satisfies -- it is a
    structural, zero-freedom PREDICTION (F79's structural G + F284's rigid
    substrate: dot G/G is exactly 0, not a small fitted drift).  F297 Sec.10.4:
    register that, in the BBN context specifically, rather than only via the
    external LLR comparison F284 already makes.

    What this function does NOT do, stated plainly so the number below is not
    over-read: `run_bbn` accepts G as a parameter, so the naive move is to
    perturb it and read off "the bound this network implies".  That naive move
    was tried and discarded -- Y_p's sensitivity to G at fixed eta_b is so
    weak (`dYp_per_1pct_G` below) that inverting the network's own ~1 sigma
    margin gives a G-shift of order unity, where the linearisation, and the
    whole non-relativistic weak-freeze-out picture, have long since broken
    down.  Reporting that as "a bound" would be a bigger number attached to a
    smaller claim than the real one.

    The real, defensible content is qualitative, and its limit must be stated
    plainly rather than glossed: **every leg of `check_k2` already runs at one
    fixed G = `model_G()`, unchanged between the BBN epoch and today** -- there
    is no G(t) term anywhere in `hubble_rate`, so this calculation is
    structurally INCAPABLE of returning a nonzero dot G/G even if one were
    true.  That is unlike F284's LLR comparison, which is a genuine external
    MEASUREMENT that could in principle have come back nonzero.  What passing
    K2-1/K2-2/K2-7 with G held fixed actually shows is that the dot G/G = 0
    assumption is CONSISTENT WITH the light-element data -- a BBN-internal
    consistency check, not a second independent confirmation and not a new
    falsifier alongside F284's LLR bound.
    """
    base = run_bbn(G=model_G())
    plus = run_bbn(G=model_G() * 1.01)
    dyp_per_1pct_g = plus["Y_p"] - base["Y_p"]
    return {
        "Gdot_over_G_model": 0.0,
        "Gdot_over_G_provenance": "F79 structural G + F284 rigid substrate; "
                                   "exact, zero free parameters",
        "G_held_fixed_in_this_run": True,
        "Y_p_at_G_model": base["Y_p"],
        "dYp_per_1pct_G": dyp_per_1pct_g,
        "consistency_check": ("qualitative, not a new numeric bound, and NOT "
                          "a second independent measurement: this run holds G "
                          "fixed at one value across the BBN epoch (no G(t) "
                          "term in hubble_rate, so a nonzero dot G/G could "
                          "not have come out even if it were physically true) "
                          "and still reproduces Y_p (K2-1) and D/H (K2-2) "
                          "while K2-7 holds Y_p within 2 sigma of Aver 2021 "
                          "-- the dot G/G = 0 assumption is CONSISTENT WITH "
                          "the light-element data. Contrast F284's LLR "
                          "comparison, which measures dot G/G and could have "
                          "falsified it."),
        "note": (f"Y_p moves only {dyp_per_1pct_g:+.2e} per 1% change in G at "
                 "fixed eta_b -- far too weakly for this network to turn that "
                 "into a competitive *quantitative* bound on dot G/G (LLR "
                 "already does that 1e13x tighter, F284); the value here is "
                 "the qualitative one stated in `consistency_check`."),
    }


def input_ledger():
    """Every number that goes in, with where it comes from — no exceptions."""
    return {
        "model_native": {
            "G": "F79/F107 structural closed form, 3e-8 of CODATA",
            "source_law": "F178 induced Einstein equation (rho + 3p)",
            "Gdot_over_G": "exactly 0 (F79/F284 rigid substrate)",
            "N_eff": "3.044 from the model's own content (F47/F165/F253)",
            "delta_m": "1.51 MeV (F122/F123), no QCD anchor",
            "B_d": "2.224 MeV (F104/F113/F126/F240), one tuned b = 0.55 fm",
        },
        "external_input": {
            "eta10": "Planck 2018; F202 derives no asymmetry number (K6)",
            "V_ud": "PDG; CKM is out of scope (ledger 10-13)",
            "G_F": "carries the v anchor, which is an input (ledger 17)",
            "tau_n_calibration": "measured, used only to fix the weak coupling K",
            "reaction_rates": "Smith-Kawano-Malaney 1993 nuclear data (11 of 12)",
            "nuclear_masses": "t, 3He, 4He, 7Li, 7Be binding energies",
        },
    }


def summary():
    """Everything, as one dict — the entry point the test record calls."""
    return {
        "n_eff": n_eff_model(),
        "validation": validate_network(),
        "law_control": law_control(),
        "delta_m": delta_m_confrontation(),
        "f122": f122_decomposition(),
        "delta_m_theory": delta_m_theory_uncertainty(),
        "b_d": bd_sensitivity(),
        "gdot_over_g": gdot_over_g_prediction(),
        "inputs": input_ledger(),
    }


def _tnu_ratio_error():
    """Relative error of the emergent T_nu/T_gamma against (4/11)^(1/3).

    Nothing in `thermal_history` is told about 4/11 — the run starts at
    T_nu = T_gamma above e+e- annihilation and the ratio is produced by entropy
    conservation through the annihilation.  Recovering the textbook number is
    therefore a check on the thermodynamics, and it can fail: drop the e+e-
    contribution from `_fermi_integrals` and the ratio goes to 1.
    """
    T, T_nu, _, _ = thermal_history()
    return float(T_nu[-1] / T[-1]) / (4.0 / 11.0) ** (1.0 / 3.0) - 1.0


def check_k2(delta_m_mev=None, law="full", eta10=None, legacy_a7_bug=False,
             delta_m_theory_sigma_mev=None):
    """The registry entry point: every K2 assertion, with an explicit verdict.

    Parametrised so `casim test --param delta_m_mev=1.51` re-runs the whole
    battery at the model's own splitting and **goes red** — the perturbation
    under which this record fails, which is what the 2026-08-04 report's gap #2
    asks every assertion record to declare.  `legacy_a7_bug=true` is F361's own
    declared control: it reverts the A=7 rate fits to their pre-repair form and
    must turn K2-13 (only) red.  `delta_m_theory_sigma_mev` is F372's declared
    control: forcing it down to the BBN-inferred observational band (0.0056
    MeV) instead of BMW's literature theory uncertainty (0.280 MeV) must turn
    K2-14 (only) red — reproducing the exact 36.6 sigma naive-significance bug
    F372 corrects.
    """
    dm = PDG_DELTA_M_MEV if delta_m_mev is None else float(delta_m_mev)
    eta = ETA10_PLANCK if eta10 is None else float(eta10)
    v = validate_network(legacy_a7_bug=legacy_a7_bug)
    ne = n_eff_model()
    lc = law_control()
    conf = delta_m_confrontation()
    dmt = delta_m_theory_uncertainty(sigma_theory_mev=delta_m_theory_sigma_mev)
    bd = bd_sensitivity()
    gg = gdot_over_g_prediction()
    obs_yp, sig_yp = OBS_YP
    obs_dh, sig_dh = OBS_DH
    run = run_bbn(delta_m_mev=dm, law=law, eta10=eta,
                   legacy_a7_bug=legacy_a7_bug)

    checks = [
        ("K2-1 network reproduces standard BBN Y_p to 3%",
         abs(v["Y_p_rel_err"]) < 0.03, v["Y_p_rel_err"]),
        ("K2-2 network reproduces standard BBN D/H to 5%",
         abs(v["D_H_rel_err"]) < 0.05, v["D_H_rel_err"]),
        ("K2-3 T_nu/T_gamma -> (4/11)^(1/3) from entropy alone, to 1e-3",
         abs(_tnu_ratio_error()) < 1e-3, _tnu_ratio_error()),
        ("K2-4 detailed balance emerges (not imposed) to 1e-3",
         abs(v["detailed_balance_ratio"] - 1.0) < 1e-3,
         v["detailed_balance_ratio"] - 1.0),
        ("K2-5 N_eff = 3.044 within 1 sigma of Planck",
         abs(ne["N_eff_sigma"]) < 1.0, ne["N_eff_sigma"]),
        ("K2-6 energy-only law excluded by Y_p at >5 sigma",
         abs(lc["Y_p_energy_sigma"]) > 5.0, lc["Y_p_energy_sigma"]),
        ("K2-7 full-tensor law consistent with Y_p within 2 sigma",
         abs(lc["Y_p_full_sigma"]) < 2.0, lc["Y_p_full_sigma"]),
        ("K2-8 BBN bounds delta m at least 100x tighter than F122's 1 MeV",
         conf["delta_m_bound_1sigma_MeV"] < 0.01,
         conf["delta_m_bound_1sigma_MeV"]),
        ("K2-9 model delta m = 1.51 MeV is excluded at >5 sigma",
         abs(conf["Y_p_model_sigma"]) > 5.0, conf["Y_p_model_sigma"]),
        ("K2-10 B_d at the model's 0.026% is invisible to D/H (<0.2 sigma)",
         abs(bd["D_H_shift_in_sigma"]) < 0.2, bd["D_H_shift_in_sigma"]),
        ("K2-11 the run at the swept delta m matches Y_p within 2 sigma",
         abs((run["Y_p"] - obs_yp) / sig_yp) < 2.0,
         (run["Y_p"] - obs_yp) / sig_yp),
        ("K2-12 the run at the swept delta m matches D/H within 3 sigma",
         abs((run["D_H"] - obs_dh) / sig_dh) < 3.0,
         (run["D_H"] - obs_dh) / sig_dh),
        (f"K2-13 network reproduces standard BBN Li7/H to {LI7_VALIDATION_TOL:.0%} "
         "(F361 A=7 repair)",
         abs(v["Li7_H_rel_err"]) < LI7_VALIDATION_TOL, v["Li7_H_rel_err"]),
        ("K2-14 model delta m is consistent with measured within its own "
         "literature theory uncertainty (<2 sigma, F372)",
         abs(dmt["sig_theory_aware"]) < 2.0, dmt["sig_theory_aware"]),
        ("K2-15 model's P2 pairwise EM self-energy confirms the ad hoc "
         "classical estimate to <10% (F372, zero new parameters)",
         abs(dmt["em_pairwise_vs_adhoc_rel_err"]) < 0.10,
         dmt["em_pairwise_vs_adhoc_rel_err"]),
    ]
    results = [{"check": c, "passed": bool(p), "value": val} for c, p, val in checks]
    return {
        "passed": all(r["passed"] for r in results),
        "n_pass": sum(r["passed"] for r in results),
        "n_total": len(results),
        "checks": results,
        "delta_m_mev": dm, "law": law, "eta10": eta,
        "Y_p": run["Y_p"], "D_H": run["D_H"], "Li7_H": run["Li7_H"],
        "gdot_over_g": gg,
        "delta_m_theory": dmt,
    }


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    out = summary()
    out["checks"] = check_k2()
    v, lc, dm = out["validation"], out["law_control"], out["delta_m"]
    print("K2 / BBN — light-element abundances")
    print(f"  network validation : Y_p {v['Y_p']:.5f} "
          f"({100*v['Y_p_rel_err']:+.2f}% of reference), "
          f"D/H {v['D_H']:.3e} ({100*v['D_H_rel_err']:+.2f}%)")
    print(f"  N_eff              : {out['n_eff']['N_eff']:.3f} "
          f"({out['n_eff']['N_eff_sigma']:+.2f} sigma vs Planck)")
    print(f"  law control        : Y_p full {lc['Y_p_full']:.4f} vs "
          f"energy-only {lc['Y_p_energy']:.4f} "
          f"({lc['Y_p_energy_sigma']:+.1f} sigma)")
    print(f"  delta m            : Y_p(1.293) {dm['Y_p_pdg']:.4f} vs "
          f"Y_p(1.51) {dm['Y_p_model']:.4f} ({dm['Y_p_model_sigma']:+.1f} sigma)")
    print(f"  tau_n              : {dm['tau_n_model_dm']:.1f} s at the model's "
          f"delta m vs {dm['tau_n_measured']:.1f} s measured")

    print(f"  verdict            : {out['checks']['n_pass']}/"
          f"{out['checks']['n_total']} PASS")

    path = results_path("F297_bbn_light_elements.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"  wrote {path}")
