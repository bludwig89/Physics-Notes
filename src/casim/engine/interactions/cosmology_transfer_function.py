"""
cosmology_transfer_function.py -- toward a model-native replacement for the
                                   EH98 no-wiggle transfer function (K11/S2)
==============================================================================

Created: 2026-09-05 - 02:20
Claims topic: docs/design/session-claims.yaml,
              session cowork-k11-radiation-era-transfer-function
Attacks: docs/status/open-derivations.md row S2 ("THREE NAMED IMPORTS, EACH
         PRICED"), item (i): [[F288-structure-formation-zero-free-functions]]
         section 7's own open item -- "the sigma_8 residual IS the EH98
         no-wiggle fit ... replacing it needs the model's own radiation-era
         Boltzmann hierarchy ... a real piece of work, not a tightening."

--------------------------------------------------------------------------
What this module is, and is careful not to overclaim
--------------------------------------------------------------------------
F288 (S1/S2/S3) already forces mu = Sigma = 1 EXACTLY in the sub-horizon
quasi-static regime -- so the model needs NO new gravitational physics to
treat linear photon-baryon-CDM perturbations: the governing equations are
the ordinary GR-identical Einstein-Boltzmann system, sourced by ordinary
matter, exactly as in LCDM.  What the model does NOT yet carry is the
radiation-era MATTER content's own dynamics: the coupled photon monopole/
dipole + baryon-velocity tight-coupling system whose solution sets the
sound horizon, the acoustic-oscillation phase, and the Silk damping scale
that a full transfer function needs.  Building the complete multipole
Boltzmann hierarchy (a CAMB/CLASS-equivalent solver, l_max ~ O(10) with a
non-equilibrium (Peebles) recombination history) is genuinely out of scope
for one session -- this is the finding's own "real piece of work" line, not
a tightening.

This module does the two things that scoping shows ARE tractable without
that full solver, using ONLY physics and constants the model already owns:

  1. SOUND HORIZON, by direct numerical integration of the model's own
     multi-component Friedmann background (cosmology_growth.background/E2,
     which is F182/F188's own confirmed result) -- replacing EH98's internal
     CLOSED-FORM FITTING FORMULA for the sound horizon (their eq. 26-style
     approximation, already the one line item ``cosmology_growth.py`` uses)
     with a genuine integral of the model's own H(a).

  2. HYDROGEN RECOMBINATION REDSHIFT, via the Saha equation, using the
     model's own machine-precision Rydberg energy (F125,
     ``casim.engine.particles.atom.rydberg_eV`` at the physical e-p reduced
     mass) instead of Hu & Sugiyama's fitted z_d(omega_b h^2, omega_0 h^2)
     formula (EH98 eq. 4).

Both are genuinely NEW model content (nothing here is asserted anywhere else
in the tree).  Both are honestly bounded: (1) is checked against Planck's
own numerically-computed r_drag: D1.  (2) reproduces the textbook ~25-30%
Saha-vs-true bias (the recombination is NOT instantaneous equilibrium; the
2s-1s two-photon bottleneck delays it -- Peebles 1968) -- reported, not
hidden: D4.

What remains imported, named exactly: the CDM/baryon suppression envelope
(EH98's alpha_c, beta_c) and the baryon-oscillation envelope G(y) -- EH98's
own paper states these ARE calibrated against a numerical Boltzmann code
(CMBFAST) and are not closed-form.  Silk damping (k_Silk) is SCOPED but not
implemented here: the exact coefficient depends on the quadrupole/
polarization feedback convention (Hu & Sugiyama 1995 vs later refinements),
and getting it right to better than EH98's own admitted +/-20% correction
needs the diffusion-order Boltzmann expansion this session does not build.

D3 measures what substituting (1) into the (otherwise-still-EH98) shape
formula actually does to sigma_8 -- and the answer is informative: it
barely moves it (see D3's own note).  That LOCALISES the ~1.15% sigma_8
residual away from the sound-horizon scale and onto the missing acoustic
wiggles / envelope calibration -- a genuine diagnostic, not a fix.

Real arithmetic, hand-rolled Simpson quadrature and bisection; sympy for the
two exact legs.  No scipy integrator (D8).
"""
from __future__ import annotations

import math

import sympy as sp

from casim.engine.interactions import cosmology_growth as cg
from casim.engine.interactions import cosmology_bbn as bbn
from casim.engine.particles import atom

# ===========================================================================
# External inputs NOT already declared in cg.EXTERNAL.  Every number this
# module depends on that the model does not produce is HERE, once, with its
# source -- same discipline as cosmology_growth.EXTERNAL.
# ===========================================================================
EXTERNAL_TF = {
    # Planck 2018 VI (TT,TE,EE+lowE+lensing), Table 2 -- standard citation,
    # quoted in essentially every post-2018 cosmology paper.
    "z_drag": (1059.94, "Planck 2018 VI, Table 2 -- baryon drag redshift"),
    "r_drag_planck_Mpc": (147.09, "Planck 2018 VI, Table 2 -- comoving sound "
                                  "horizon at the drag epoch"),
    "z_star_planck": (1089.92, "Planck 2018 VI, Table 2 -- photon "
                                "decoupling / recombination redshift"),
}

C_KM_S = cg.C_KM_S
K_B_EV_PER_K = 8.617333262e-5   # eV/K -- exact (SI 2019 kB is exact)
ZETA3 = 1.2020569031595943      # Riemann zeta(3), for the photon number density


# ===========================================================================
# 1 -- the photon-baryon sound speed, and the sound horizon it integrates to
# ===========================================================================
def omega_gamma(h: float, T_cmb: float) -> float:
    """Photon-only density parameter (no neutrinos) -- the piece of
    ``cosmology_growth._omega_r`` that couples to baryons via Thomson
    scattering.  Same 2.47282e-5 normalisation cg.py already uses."""
    return 2.47282e-5 * (T_cmb / 2.7255) ** 4 / h ** 2


def R_of_a(a: float, Omega_b: float, Omega_gamma_: float) -> float:
    """Baryon-to-photon momentum-density ratio R = 3 rho_b / (4 rho_gamma).
    rho_b ~ a^-3, rho_gamma ~ a^-4  =>  R is EXACTLY LINEAR in a."""
    return 3.0 * Omega_b * a / (4.0 * Omega_gamma_)


def sound_speed(a: float, Omega_b: float, Omega_gamma_: float) -> float:
    """c_s(a)/c = 1/sqrt(3(1+R(a))) -- the standard photon-baryon fluid
    sound speed in the tight-coupling limit (adiabatic, single fluid)."""
    R = R_of_a(a, Omega_b, Omega_gamma_)
    return 1.0 / math.sqrt(3.0 * (1.0 + R))


def check_S1_sound_speed_radiation_limit() -> dict:
    """EXACT: as a -> 0, R -> 0 and c_s -> 1/sqrt(3) exactly (the pure
    radiation-fluid sound speed) -- a sympy literal limit, not a numeric
    approach."""
    a, Ob, Og = sp.symbols("a Omega_b Omega_gamma", positive=True)
    R = 3 * Ob * a / (4 * Og)
    cs = 1 / sp.sqrt(3 * (1 + R))
    limit = sp.limit(cs, a, 0)
    target = 1 / sp.sqrt(3)
    residual = sp.simplify(limit - target)
    return {
        "c_s_a_to_0_symbolic": str(limit),
        "target_1_over_sqrt3": str(target),
        "residual": str(residual),
        "pass": residual == 0,
    }


def check_S2_R_exactly_linear_in_a() -> dict:
    """EXACT: R(a) = (3 Omega_b / 4 Omega_gamma) a identically -- d/da of
    R(a)/a is a sympy literal zero (rho_b ~ a^-3, rho_gamma ~ a^-4, so their
    ratio is forced linear; no fit, no approximation)."""
    a, Ob, Og = sp.symbols("a Omega_b Omega_gamma", positive=True)
    R = 3 * Ob * a / (4 * Og)
    ratio = sp.simplify(R / a)
    d_ratio_da = sp.simplify(sp.diff(ratio, a))
    return {
        "R_over_a_symbolic": str(ratio),
        "d(R_over_a)/da": str(d_ratio_da),
        "pass": d_ratio_da == 0,
    }


def sound_horizon_mpc(a_end: float, bg: dict, Omega_b: float, Omega_gamma_: float,
                       n: int = 200_000) -> float:
    """r_s(a_end) = D_H * integral_0^{a_end} c_s(a) / (a^2 E(a)) da, D_H = c/H0.

    This is the model's OWN sound horizon: the integrand uses
    ``cosmology_growth.E2`` (F182/F188's confirmed multi-component E(a)^2,
    i.e. the model's actual background, radiation+matter+Lambda) rather than
    EH98's closed-form approximation (which drops Lambda and fits the
    radiation/matter transition).  Simpson's rule, D8-compliant (hand-rolled,
    no scipy); the integrand is finite and smooth as a -> 0 (c_s -> 1/sqrt3,
    a^2 E(a) -> sqrt(Or)), so a plain linear grid from a ~ 0 is safe.
    """
    D_H_Mpc = C_KM_S / (100.0 * bg["h"])
    a0 = 1.0e-10
    if n % 2:
        n += 1
    step = (a_end - a0) / n
    total = 0.0
    for i in range(n + 1):
        a = a0 + i * step
        cs = sound_speed(a, Omega_b, Omega_gamma_)
        f = cs / (a * a * math.sqrt(cg.E2(a, bg)))
        w = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        total += w * f
    return D_H_Mpc * total * step / 3.0


def check_D1_sound_horizon_vs_planck(z_drag_multiplier: float = 1.0) -> dict:
    """QUANTITATIVE: integrate the model's OWN background to the (imported)
    Planck drag redshift and compare to Planck's own r_drag.

    HONEST SCOPE (added after adversarial review, 2026-09-05): Omega_b,
    Omega_m, h and T_cmb here are THE SAME Planck-2018-fit values that
    Planck's own analysis also used to derive r_drag=147.09 Mpc (via its
    own Boltzmann code). So this comparison is substantially an
    INTERNAL-CONSISTENCY check -- does the model's sound-horizon
    integrator, fed Planck's own background parameters, reproduce Planck's
    own reported scale? -- not an independent validation of the model
    against an external measurement. A disagreement here would indicate an
    integration or background bug, not new physics. It is still a
    meaningful, genuinely falsifiable check (a wrong integrator or a wrong
    E(a) WOULD move this number, and by a lot -- see the z_drag_multiplier
    control), just not the "independent nature-test" framing a careless
    reading of the residual invites.

    ``z_drag_multiplier`` is a control handle (D9/H2): perturbing the epoch
    the integral is carried to away from the true drag redshift must, and
    does, blow the 1% tolerance (see the registry ``control:`` block)."""
    bg = cg.background(radiation=True)
    Omega_b = cg.EXTERNAL["Omega_b"][0]
    Og = omega_gamma(bg["h"], cg.EXTERNAL["T_cmb_K"][0])
    z_drag = EXTERNAL_TF["z_drag"][0] * z_drag_multiplier
    a_drag = 1.0 / (1.0 + z_drag)
    r_s_model = sound_horizon_mpc(a_drag, bg, Omega_b, Og)
    r_drag_planck = EXTERNAL_TF["r_drag_planck_Mpc"][0]
    rel = r_s_model / r_drag_planck - 1.0
    return {
        "z_drag_multiplier": z_drag_multiplier,
        "z_drag_used": z_drag,
        "z_drag_source": EXTERNAL_TF["z_drag"][1],
        "r_s_model_Mpc": r_s_model,
        "r_drag_planck_Mpc": r_drag_planck,
        "relative_residual": rel,
        "scope_caveat": ("Omega_b/Omega_m/h/T_cmb feeding this integral are "
                         "the SAME Planck-fit values Planck's own analysis "
                         "used to derive r_drag -- this is substantially an "
                         "internal-consistency check of the model's own "
                         "integrator, not an independent nature-test."),
        "pass": abs(rel) < 0.01,
    }


def eh98_internal_fitting_s(Om: float, Omega_b: float, h: float) -> float:
    """The closed-form fitting formula ``cosmology_growth.transfer_eh98``
    already uses internally for the sound-horizon scale (its own local
    variable ``s``) -- reproduced here, unchanged, ONLY so D2 can quantify
    the gap between it and the model-native integral. Not a new import: it
    is the exact expression already live in the tree."""
    omh2 = Om * h ** 2
    obh2 = Omega_b * h ** 2
    return 44.5 * math.log(9.83 / omh2) / math.sqrt(1.0 + 10.0 * obh2 ** 0.75)


def check_D2_model_native_vs_eh98_internal_fit(z_drag_multiplier: float = 1.0) -> dict:
    """QUANTITATIVE: how much better is the model-native sound-horizon
    integral than the fitting formula already coded in transfer_eh98?
    Shares the D1 control handle: a wrong z_drag degrades the model integral
    but leaves EH98's own (z_drag-independent) internal fit untouched, so
    the comparison itself is part of what the control tests."""
    bg = cg.background(radiation=True)
    Omega_b = cg.EXTERNAL["Omega_b"][0]
    Og = omega_gamma(bg["h"], cg.EXTERNAL["T_cmb_K"][0])
    z_drag = EXTERNAL_TF["z_drag"][0] * z_drag_multiplier
    a_drag = 1.0 / (1.0 + z_drag)
    r_s_model = sound_horizon_mpc(a_drag, bg, Omega_b, Og)
    s_eh98 = eh98_internal_fitting_s(bg["Om"], Omega_b, bg["h"])
    r_drag_planck = EXTERNAL_TF["r_drag_planck_Mpc"][0]
    resid_model = r_s_model / r_drag_planck - 1.0
    resid_eh98 = s_eh98 / r_drag_planck - 1.0
    return {
        "r_s_model_Mpc": r_s_model,
        "s_eh98_internal_fit_Mpc": s_eh98,
        "residual_model_vs_planck": resid_model,
        "residual_eh98_fit_vs_planck": resid_eh98,
        "improvement_factor": abs(resid_eh98) / max(abs(resid_model), 1e-12),
        "pass": abs(resid_model) < abs(resid_eh98),
    }


# ===========================================================================
# 2 -- transfer function with the model-native sound horizon substituted,
#      and its effect on sigma_8 (everything else in EH98's shape held fixed
#      and named as still-imported)
# ===========================================================================
def transfer_eh98_with_sound_horizon(k_invMpc: float, Om: float, h: float,
                                      Omega_b: float, T_cmb: float,
                                      s_Mpc: float) -> float:
    """EH98 no-wiggle shape, IDENTICAL to cosmology_growth.transfer_eh98,
    except the sound-horizon scale ``s`` is passed in rather than computed
    from the internal fitting formula. The alpha_gamma/gamma_eff envelope
    (EH98's own Boltzmann-calibrated pieces) is UNCHANGED and still
    imported -- named, not hidden."""
    omh2 = Om * h ** 2
    theta = T_cmb / 2.7
    fb = Omega_b / Om
    a_gam = (1.0 - 0.328 * math.log(431.0 * omh2) * fb
             + 0.38 * math.log(22.3 * omh2) * fb ** 2)
    gam_eff = Om * h * (a_gam + (1.0 - a_gam) / (1.0 + (0.43 * k_invMpc * s_Mpc) ** 4))
    q = k_invMpc / h * theta ** 2 / gam_eff
    L0 = math.log(2.0 * math.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q ** 2)


def sigma8_model_native_sound_horizon(s_Mpc: float, n: int = 2000) -> dict:
    """Re-run F288's own sigma_R integral (D4) with ONLY the sound-horizon
    scale replaced by the model-native integral -- A_s, n_s, D(1), the
    growth factor, and every EH98 envelope coefficient are exactly what
    ``cosmology_growth.sigma8_from_As`` uses, so this isolates the effect
    of the ONE substitution this module makes."""
    bg = cg.background(radiation=False)
    n_s = cg.ad.NS_OBS
    A_s = cg.EXTERNAL["A_s"][0]
    _, D, _ = cg.growth_factor(bg, mu=1.0)
    D1 = float(D[-1])
    c_over_H0 = C_KM_S / (100.0 * bg["h"])
    kp = cg.EXTERNAL["k_pivot_invMpc"][0]
    R8 = cg.R8_H_INV_MPC / bg["h"]

    lk0, lk1 = math.log(1.0e-5), math.log(1.0e3)
    hstep = (lk1 - lk0) / n
    total = 0.0
    for i in range(n + 1):
        k = math.exp(lk0 + i * hstep)
        T = transfer_eh98_with_sound_horizon(k, bg["Om"], bg["h"],
                                              cg.EXTERNAL["Omega_b"][0],
                                              cg.EXTERNAL["T_cmb_K"][0], s_Mpc)
        d2 = (4.0 / 25.0) * A_s * (k / kp) ** (n_s - 1.0) \
            * (c_over_H0 * k) ** 4 / bg["Om"] ** 2 * T ** 2 * D1 ** 2
        w = cg._window_tophat(k * R8)
        term = d2 * w * w
        wt = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        total += wt * term
    s8_massless = math.sqrt(total * hstep / 3.0)

    f_nu = (cg.EXTERNAL["sum_mnu_eV"][0] / 93.14 / bg["h"] ** 2) / bg["Om"]
    s8 = s8_massless * (1.0 - 4.0 * f_nu)
    return {"sigma_8": s8, "sigma_8_massless_nu": s8_massless}


def check_D3_sigma8_shift_localises_residual() -> dict:
    """QUANTITATIVE / DIAGNOSTIC: swap the model-native sound horizon into
    the (otherwise unchanged) EH98 shape and re-measure sigma_8. The result
    is informative precisely because it is small: it shows the ~1.15%
    sigma_8-vs-Planck residual F288 reports is NOT located in the
    sound-horizon scale (which the model reproduces to 0.11%, D1) -- it is
    localised to EH98's missing acoustic wiggles / envelope calibration,
    which stays imported (see module docstring)."""
    bg = cg.background(radiation=True)
    Omega_b = cg.EXTERNAL["Omega_b"][0]
    Og = omega_gamma(bg["h"], cg.EXTERNAL["T_cmb_K"][0])
    z_drag = EXTERNAL_TF["z_drag"][0]
    a_drag = 1.0 / (1.0 + z_drag)
    r_s_model = sound_horizon_mpc(a_drag, bg, Omega_b, Og)

    old = cg.sigma8_from_As()
    new = sigma8_model_native_sound_horizon(r_s_model)

    ref = cg.EXTERNAL["sigma8_planck"][0]
    resid_old = old["sigma_8"] / ref - 1.0
    resid_new = new["sigma_8"] / ref - 1.0
    return {
        "sigma_8_eh98_fitting_s": old["sigma_8"],
        "sigma_8_model_native_s": new["sigma_8"],
        "relative_shift": new["sigma_8"] / old["sigma_8"] - 1.0,
        "residual_vs_planck_eh98_fitting_s": resid_old,
        "residual_vs_planck_model_native_s": resid_new,
        "diagnosis": ("the shift is two orders of magnitude smaller than the "
                      "residual itself -- the sound-horizon SCALE is not "
                      "where the ~1% sigma_8 residual lives; it is in EH98's "
                      "missing acoustic wiggles / Boltzmann-calibrated "
                      "envelope, both still imported."),
        "narrowing_caveat": ("added after adversarial review, 2026-09-05: "
                             "this small shift holds ONLY because both "
                             "candidate s values (146.9, 149.8 Mpc) sit "
                             "close together on a locally flat part of "
                             "sigma_8(s) -- the true sensitivity is "
                             "ASYMMETRIC (halving s shifts sigma_8 by "
                             "+1.23%, comparable to the whole residual; "
                             "doubling s shifts it by only -0.21%). This "
                             "demonstrates sigma_8 is insensitive to the "
                             "narrow ~2% band the two estimates occupy -- "
                             "not that sigma_8 is generically insensitive "
                             "to the sound-horizon scale."),
        "pass": abs(new["sigma_8"] / old["sigma_8"] - 1.0) < 0.01,
    }


# ===========================================================================
# 3 -- hydrogen recombination via Saha, from the model's OWN Rydberg energy
# ===========================================================================
def _model_native_B_ion_eV() -> float:
    """The model's own hydrogen ionisation energy: F125's Rydberg formula
    (casim.engine.particles.atom.rydberg_eV) at the physical e-p reduced
    mass. Same function F125 uses to reproduce -13.6 eV from m_e + alpha;
    imported here as the atomic-physics INPUT to Saha, not re-derived."""
    mu = atom.reduced_mass_MeV(atom.M_E_MEV, atom.M_P_MEV)
    return atom.rydberg_eV(mu)


def _n_gamma_per_nm3(T_eV: float) -> float:
    """Photon number density (2 zeta(3)/pi^2) T^3/(hbar c)^3, in nm^-3."""
    return (2.0 * ZETA3 / math.pi ** 2) * (T_eV / atom.HBARC_EVNM) ** 3


def saha_xe(z: float, T_cmb_K: float, eta10: float, B_ion_eV: float) -> float:
    """Equilibrium (Saha) hydrogen ionisation fraction X_e(z), from
    X_e^2/(1-X_e) = S(T)/n_b(z), S(T) = (m_e T / 2 pi hbar^2)^(3/2) exp(-B/T).
    Helium and non-equilibrium (Peebles 1968) corrections are NOT included --
    this is exactly why D4 shows the well-known Saha-vs-true bias."""
    T_eV = K_B_EV_PER_K * T_cmb_K * (1.0 + z)
    m_e_eV = atom.M_E_MEV * 1.0e6
    S = ((m_e_eV * T_eV) / (2.0 * math.pi * atom.HBARC_EVNM ** 2)) ** 1.5 \
        * math.exp(-B_ion_eV / T_eV)
    n_b = eta10 * 1.0e-10 * _n_gamma_per_nm3(T_eV)
    ratio = S / n_b
    return (-ratio + math.sqrt(ratio * ratio + 4.0 * ratio)) / 2.0


def find_z_recombination_saha(T_cmb_K: float, eta10: float, B_ion_eV: float,
                               target: float = 0.5, zlo: float = 400.0,
                               zhi: float = 3000.0, tol: float = 1.0e-7,
                               itmax: int = 200) -> float:
    """Bisect for X_e(z) = target (the standard z_* convention).

    Requires the bracket to actually straddle the root (flagged after
    adversarial review, 2026-09-05: an out-of-range B_ion/eta10 previously
    made this silently return the ``zhi`` boundary instead of erroring)."""
    flo = saha_xe(zlo, T_cmb_K, eta10, B_ion_eV) - target
    fhi = saha_xe(zhi, T_cmb_K, eta10, B_ion_eV) - target
    if (flo > 0) == (fhi > 0):
        raise ValueError(
            f"find_z_recombination_saha: [zlo={zlo}, zhi={zhi}] does not "
            f"bracket X_e={target} (f(zlo)={flo:+.4g}, f(zhi)={fhi:+.4g}) -- "
            "widen the search range rather than trust an extrapolated root.")
    for _ in range(itmax):
        zmid = 0.5 * (zlo + zhi)
        fmid = saha_xe(zmid, T_cmb_K, eta10, B_ion_eV) - target
        if abs(fmid) < tol:
            return zmid
        if (fmid > 0) == (flo > 0):
            zlo, flo = zmid, fmid
        else:
            zhi = zmid
    return 0.5 * (zlo + zhi)


def check_D4_saha_recombination_redshift(eta10: float = None,
                                          b_ion_multiplier: float = 1.0) -> dict:
    """QUANTITATIVE: the model's own Rydberg energy + the imported eta10
    (unchanged BBN external input, S2 item iii) plugged into the plain
    (equilibrium) Saha equation. Reproduces the textbook ~25-30% high bias
    of pure Saha against the true (Peebles, non-equilibrium) recombination
    redshift -- the 2s-1s two-photon bottleneck delays recombination below
    what instantaneous equilibrium predicts. Closing this needs the Peebles
    effective 3-level atom (standard atomic physics, not model-specific;
    named as the next tractable piece, not built here).

    ``b_ion_multiplier`` is the control handle (D9/H2): the ionisation
    energy enters Saha exponentially (exp(-B/T)), so an unphysical B_ion
    moves z_saha sharply -- either far above the known-bias band (B too
    large) or spuriously down to ~0 bias (B too small, which would look
    like an improvement but is actually the check losing its grip on the
    real physics), and either direction must be caught."""
    eta10 = bbn.ETA10_PLANCK if eta10 is None else eta10
    T_cmb_K = cg.EXTERNAL["T_cmb_K"][0]
    B_ion = _model_native_B_ion_eV() * b_ion_multiplier
    z_saha = find_z_recombination_saha(T_cmb_K, eta10, B_ion)
    z_star_planck = EXTERNAL_TF["z_star_planck"][0]
    rel = z_saha / z_star_planck - 1.0
    return {
        "B_ion_eV_model_native": B_ion,
        "B_ion_eV_codata": atom.RY_EV_CODATA,
        "b_ion_multiplier": b_ion_multiplier,
        "eta10_used": eta10,
        "z_recombination_saha_Xe_0.5": z_saha,
        "z_star_planck": z_star_planck,
        "relative_bias": rel,
        "known_mechanism": ("plain Saha assumes instantaneous equilibrium; "
                             "the true 2s-1s two-photon decay bottleneck "
                             "(Peebles 1968) delays recombination, giving "
                             "z_true < z_Saha. The ~26% bias measured here "
                             "matches the well-known Saha-vs-RECFAST gap."),
        # the textbook ~25-30% band: a correct calc must land IN this band,
        # not at 0 (that would mean the known-physics omission silently
        # vanished -- a bug, not an improvement) and not far above it
        # (that would mean the input atomic energy is wrong).
        "pass": 0.15 < rel < 0.40,
    }


# ===========================================================================
# Registry entry point
# ===========================================================================
SCOPE = {
    "already_model_native_no_new_physics_needed": [
        "gravity sector: mu = Sigma = 1 exactly (F288 S1-S3) -- perturbation "
        "equations are GR-identical, nothing to derive there",
        "background H(a): full multi-component Friedmann, F182/F188",
        "CDM long-wavelength growth shape (Meszaros stagnation): F288 D2, "
        "exact sympy zero",
    ],
    "built_here_partial": [
        "sound horizon r_s(z_drag): direct integral on the model's own "
        "background (D1, D2) -- replaces a closed-form fitting formula",
        "recombination redshift: Saha equation with the model's own "
        "Rydberg energy (D4) -- replaces a fitted Hu-Sugiyama formula, with "
        "its known equilibrium-approximation bias reported rather than hidden",
    ],
    "scoped_but_not_built": [
        "Silk damping k_Silk: needs the diffusion-order (quadrupole/"
        "polarization) tight-coupling expansion; EH98's own coefficient is "
        "itself only a phenomenological fit (+/-20%), so no closed form "
        "exists to derive against -- the target would be a genuine "
        "numerical diffusion integral, not a formula lookup",
        "non-equilibrium (Peebles effective 3-level atom) recombination: "
        "standard atomic physics, would close most of D4's bias -- tractable "
        "but not attempted this session",
    ],
    "still_imported_named": [
        "CDM/baryon envelope alpha_c, beta_c (EH98 eqs 11-12): calibrated "
        "against a numerical Boltzmann code (CMBFAST) by EH98's own account, "
        "no closed form to derive",
        "baryon acoustic envelope G(y) (EH98 eq 14): same",
        "the acoustic OSCILLATIONS themselves (EH98's full, non-no-wiggle "
        "eqs 15-19): needs the actual multipole hierarchy solved as a "
        "function of k, not a scale",
    ],
    "requires_full_multipole_boltzmann_solver": (
        "a minimal but genuine replacement of EH98's shape (not just its "
        "scale-setting numbers) needs: photon monopole/dipole (Theta_0, "
        "Theta_1) + baryon velocity in the tight-coupling approximation, "
        "transitioning to a truncated free-streaming hierarchy (l_max ~ "
        "6-10) at recombination, sourced by the model's own Phi/Psi "
        "(already GR-identical, F288), with the Peebles recombination "
        "history above. This is the F288 sec. 7 'real piece of work' -- "
        "estimated at several sessions of numerical development and "
        "validation against known Boltzmann-code output, not a single-session "
        "task, which is why this session scoped it and delivered the two "
        "tractable pieces above rather than a rushed partial solver."
    ),
}


def run(z_drag_multiplier: float = 1.0, b_ion_multiplier: float = 1.0) -> dict:
    """Registry entry point. Two independent control handles (D9/H2):

      ``z_drag_multiplier`` != 1  ->  MUST redden D1 and D2 (the sound-
      horizon integral is carried to the wrong epoch and drifts off both
      Planck's r_drag and, differentially, EH98's own z_drag-independent
      internal fit).

      ``b_ion_multiplier`` != 1  ->  MUST redden D4 (an unphysical
      ionisation energy pushes the Saha bias out of the known ~15-40%
      band, in either direction).

    Both default to 1.0 for the physical run."""
    out = {
        "S1_sound_speed_radiation_limit": check_S1_sound_speed_radiation_limit(),
        "S2_R_exactly_linear_in_a": check_S2_R_exactly_linear_in_a(),
        "D1_sound_horizon_vs_planck": check_D1_sound_horizon_vs_planck(z_drag_multiplier),
        "D2_model_native_vs_eh98_internal_fit": check_D2_model_native_vs_eh98_internal_fit(z_drag_multiplier),
        "D3_sigma8_shift_localises_residual": check_D3_sigma8_shift_localises_residual(),
        "D4_saha_recombination_redshift": check_D4_saha_recombination_redshift(b_ion_multiplier=b_ion_multiplier),
        "scope": SCOPE,
    }
    is_control = (z_drag_multiplier != 1.0) or (b_ion_multiplier != 1.0)
    if is_control:
        out["control"] = {
            "z_drag_multiplier": z_drag_multiplier,
            "b_ion_multiplier": b_ion_multiplier,
            "D1_pass": out["D1_sound_horizon_vs_planck"]["pass"],
            "D2_pass": out["D2_model_native_vs_eh98_internal_fit"]["pass"],
            "D4_pass": out["D4_saha_recombination_redshift"]["pass"],
            "pass": False,
            "note": ("this is the control leg, not a model this project "
                     "holds -- it is False by construction whenever either "
                     "multiplier != 1, and exists to prove D1/D2/D4 can "
                     "go red."),
        }
    # ``checks``: the shape casim.tests.runner's control-soundness resolver
    # looks for (a dict of leg-id -> {"pass": bool, ...}), so the registry
    # ``control:`` block's declared leg IDs are resolvable. Built from the
    # six named checks ONLY (not the "control" summary or "scope" prose),
    # so the control summary itself is never mistaken for an undeclared,
    # spilled leg. Kept alongside the flat top-level keys (unchanged) for
    # this module's own callers/tests.
    _leg_names = ("S1_sound_speed_radiation_limit", "S2_R_exactly_linear_in_a",
                  "D1_sound_horizon_vs_planck", "D2_model_native_vs_eh98_internal_fit",
                  "D3_sigma8_shift_localises_residual", "D4_saha_recombination_redshift")
    out["checks"] = {name: out[name] for name in _leg_names}
    out["n_checks"] = len(out["checks"])
    out["z_drag_multiplier"] = z_drag_multiplier
    out["b_ion_multiplier"] = b_ion_multiplier
    out["verdict"] = (
        "K11/S2: TWO of EH98's imported scale-setting numbers replaced with "
        "model-native derivations -- the sound horizon (direct integral on "
        "the model's own F182/F188 background, 0.11% vs Planck's own "
        "r_drag -- an INTERNAL-CONSISTENCY check, since the same Planck-fit "
        "background inputs feed both sides -- and 16.4x closer than the "
        "internal fitting formula already in cosmology_growth.py) and the "
        "recombination redshift (Saha with the model's own F125 Rydberg "
        "energy, reproducing the textbook ~26% equilibrium-approximation "
        "bias honestly). Swapping the model-native sound horizon into "
        "sigma_8 shifts it by <0.02%, DIAGNOSING that the ~1.15% sigma_8 "
        "residual is not the sound-horizon scale but EH98's missing "
        "acoustic wiggles and Boltzmann-calibrated envelope -- which remain "
        "imported, named, and scoped as needing a full multipole Boltzmann "
        "solver this session does not build. CAVEAT (post-review): the "
        "sigma_8 shift is small only because both candidate sound-horizon "
        "values sit close together on a locally flat part of sigma_8(s) -- "
        "the true sensitivity is asymmetric (halving s moves sigma_8 by "
        "+1.23%), so this shows sigma_8 is insensitive to the narrow band "
        "the two estimates occupy, not generically insensitive to the "
        "sound-horizon scale."
    )
    out["pass"] = all(v.get("pass", True) for v in out.values() if isinstance(v, dict))
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(run(), indent=2, sort_keys=True, default=str))
