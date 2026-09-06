"""
derive_quark_mixed_koide_probe.py -- F347: the literature-favoured MIXED-generation-type
==========================================================================================
quark Koide tuples, checked against current data and against F175/F92's shape mechanism.

Direct follow-up to F346 (docs/reviews/F346-review-2026-09-02.md, Attack 11 -- prior-art
check). F346 tested only SAME-generation-type quark triplets (up-type u,c,t; down-type
d,s,b) against the charged-lepton E_g/T_1u circulant shape mechanism (F175's delta*=2/9
+ F92's eta^2=1/2) and found a leaning no-go. The literature instead has, since 1978,
repeatedly proposed MIXED-generation-type triplets -- crossing up-type and down-type
quarks across generations -- as the ones that satisfy a Koide-like relation:

  * Harari, Haut & Weyers, "Quark masses and Cabibbo angles," Phys. Lett. B 78 (1978)
    459-461 -- the earliest Koide-type formula in print, for (u, d, s), built on a
    MASSLESS up quark (m_u = 0), a since-superseded assumption (the up quark's mass is
    now measured, nonzero, PDG 2024: 2.16 +/- 0.07 MeV).
  * Rodejohann & Zhang, "Extended Empirical Fermion Mass Relation," arXiv:1101.5525 --
    states the relation "may be valid for the u,d,s quarks, and for the c,b,t quarks."
  * Rivero, "A new Koide tuple: strange-charm-bottom," arXiv:1111.7232 -- a THIRD tuple,
    (s, c, b), but only with a NEGATIVE sign on sqrt(m_s) -- a genuinely different,
    signed-square-root ansatz that F175's real-positive circulant does not cover. Noted
    for completeness; NOT fit with this module's pipeline (see "Scope" below).

This module re-checks the two REAL-POSITIVE-ansatz tuples -- (u, d, s) and (c, b, t) --
against CURRENT PDG 2024 masses (not the historical/assumed values the 1978-2011
literature used), first via the plain Koide Q, then via the SAME circulant-fit-vs-
single-irrep-O_h-weight pipeline F346 already built and validated:

    sqrt(m_a) = mu * (1 + eta*cos(delta + 2*pi*a/3)),   a = 0, 1, 2

Q depends ONLY on eta (Q = 1/3 + eta^2/6, an algebraic identity independent of delta --
checked directly below); it says nothing about the phase delta that F175's stronger
SHAPE claim also requires (eta^2 = 2 AND delta = 2/9, both from F80's EM/colour
selection story). This module's central question is whether a literature-flagged
Q ~ 2/3 coincidence also carries F175's phase information, or whether it is only the
weaker, eta-only statement the plain Koide criterion can see.

    C1  exact circulant reconstruction (pipeline sanity) for both tuples; the algebraic
        identity Q = 1/3 + eta^2/6 checked directly against the independently-computed
        koide_Q(); external check of the two literature Q-claims against CURRENT PDG
        2024 masses -- (u,d,s) is NOT close to 2/3 today (the historical near-hit relied
        on m_u=0), (c,b,t) IS close to 2/3 today (confirms Rodejohann-Zhang still holds).
    C2  Monte Carlo (PDG-uncertainty) measurement-precision sigma for each tuple's fitted
        delta (mod 2*pi/3) against the three single-irrep O_h weights (same candidate set
        as F346, same reasoning against subset-sum fishing).
    C3  a SEPARATE, correctly-scaled range-based look-elsewhere probability for delta
        (uniform domain [0, 2*pi/3)) -- built in from the start this time, not bolted on
        after a review catches the two questions conflated (F346's Attack 7).
    C4  (c,b,t) specifically: its fitted eta^2 sits within ~0.8% of the lepton's derived
        eta^2=2 (F92) in RELATIVE terms -- but PDG's c,b,t masses are precise enough that
        this is a decisively EXCLUDED value at measurement precision (many-sigma), not a
        measurement-compatible near-hit. Reported explicitly to keep "looks close" and
        "is close" separate, the same distinction F346's review had to retrofit.
    C5  (u,d,s) checked for completeness: neither its phase nor its amplitude approaches
        the lepton values either -- a second, independent negative, not merely "Q is far."
    C6  lepton-sector self-check: the identical fitting code recovers F175's delta*=2/9
        and F92's eta=sqrt(2) from the PDG charged-lepton masses -- confirming the method
        itself is a faithful inverse before it is trusted on these new tuples.

Scope -- what this module does NOT do: fit Rivero's signed (s,c,b) tuple (a different
ansatz, allowing a diagonal +/-1 sign matrix on the sqrt(mass) vector before the DFT --
generalizing F175's circulant to admit that would be its own derivation, not a rerun of
this one); attack the Harari et al. Cabibbo-angle claim (a CKM-sector statement, ledger
row E7, not E6); or re-attack F346's own same-generation-type result.

Real arithmetic throughout (stdlib cmath/math for the exact fit; casim.numerics for the
Monte Carlo draws, per D8).
"""

from __future__ import annotations

import cmath
import math

from casim.constants import delta_star_f
from casim.numerics import rng, xp

# ---------------------------------------------------------------------------
# Inputs: PDG 2024 current-quark masses (S. Navas et al. (Particle Data Group),
# Phys. Rev. D 110, 030001 (2024), "60. Quark Masses"), identical values to
# F346's derive_quark_shape_probe.py (u,d,s MS-bar at mu=2 GeV; c,b MS-bar at
# their own mass; t direct kinematic -- the same inherited scheme-consistency
# caveat as F346/F80-D4). Tuples ordered by ASCENDING mass, matching both the
# literature's own naming convention (u,d,s; c,b,t) and F346's established
# ordering convention for this ansatz.
MIXED_UDS_MEV = (2.16, 4.70, 93.5)              # u, d, s (Harari-Haut-Weyers 1978)
MIXED_UDS_SIGMA_MEV = (0.07, 0.07, 0.8)
MIXED_CBT_MEV = (1273.0, 4183.0, 172570.0)      # c, b, t (Rodejohann-Zhang 2011)
MIXED_CBT_SIGMA_MEV = (4.6, 7.0, 290.0)

# Charged leptons (PDG, MeV) -- reused verbatim from F346/F121 for the C6
# self-check, so it is a true regression against those findings.
CHARGED_LEPTONS_MEV = (0.51099895069, 105.6583755, 1776.86)

# The three single-irrep O_h weights in T_1u x T_1u = A_1g + E_g + T_1g + T_2g
# (F175 Sec. 2), identical candidate set to F346 (avoiding subset-sum fishing).
CANDIDATE_WEIGHTS = {
    "A_1g (1/9)": 1.0 / 9.0,
    "E_g (2/9)": delta_star_f,
    "T_1g_or_T_2g (1/3)": 1.0 / 3.0,
}

_DOMAIN_L = 2.0 * math.pi / 3.0
_LEPTON_ETA2_TARGET = 2.0


# ---------------------------------------------------------------------------
# The circulant fit (identical to F346's, reused verbatim -- not re-derived)
# ---------------------------------------------------------------------------

def fit_circulant(masses: tuple[float, float, float]) -> dict:
    """Exactly solve sqrt(m_a) = mu*(1 + eta*cos(delta + 2*pi*a/3)), a=0,1,2,
    for (mu, eta, delta), via the length-3 DFT of sqrt(masses). Any 3 positive
    numbers admit such a fit (3 real degrees of freedom in, 3 out) -- a
    coordinate change, not a prediction by itself."""
    y = [math.sqrt(m) for m in masses]
    w = cmath.exp(2j * math.pi / 3)
    Y0 = sum(y)
    Y1 = sum(y[a] * w ** (-a) for a in range(3))
    mu = Y0 / 3
    eta_complex = (2.0 / (3 * mu)) * Y1
    eta = abs(eta_complex)
    delta = cmath.phase(eta_complex)
    delta_mod = delta % (2 * math.pi / 3)
    recon = [mu * (1 + eta * math.cos(delta + 2 * math.pi * a / 3)) for a in range(3)]
    max_resid = max(abs(recon[a] - y[a]) for a in range(3))
    return {
        "mu": mu, "eta": eta, "eta2": eta * eta,
        "delta": delta, "delta_mod_2pi_over_3": delta_mod,
        "max_reconstruction_residual": max_resid,
    }


def koide_Q(masses: tuple[float, float, float]) -> float:
    y = [math.sqrt(m) for m in masses]
    return sum(v * v for v in y) / (sum(y)) ** 2


# ---------------------------------------------------------------------------
# C1 -- pipeline sanity + the Q=1/3+eta^2/6 identity + the literature checks
# ---------------------------------------------------------------------------

def c1_fit_both_tuples() -> dict:
    uds = fit_circulant(MIXED_UDS_MEV)
    cbt = fit_circulant(MIXED_CBT_MEV)
    uds["Q"] = koide_Q(MIXED_UDS_MEV)
    cbt["Q"] = koide_Q(MIXED_CBT_MEV)
    uds["Q_from_eta2_identity"] = 1.0 / 3.0 + uds["eta2"] / 6.0
    cbt["Q_from_eta2_identity"] = 1.0 / 3.0 + cbt["eta2"] / 6.0
    return {
        "check": "C1", "uds": uds, "cbt": cbt,
        "uds_Q_vs_two_thirds_rel_diff": abs(uds["Q"] - 2.0 / 3.0) / (2.0 / 3.0),
        "cbt_Q_vs_two_thirds_rel_diff": abs(cbt["Q"] - 2.0 / 3.0) / (2.0 / 3.0),
    }


# ---------------------------------------------------------------------------
# C2/C3 -- measurement-precision sigma AND the separate range-based
# look-elsewhere probability, kept apart from the very first line of this
# module (F346's review, Attack 7, is why these are never merged).
# ---------------------------------------------------------------------------

def _mc_stats(central, sigma, channel: str, n_samples: int = 20000) -> dict:
    gen = rng.for_channel(channel)
    draws = []
    for i in range(3):
        d = gen.normal(loc=central[i], scale=sigma[i], size=n_samples)
        d = xp.clip(d, 1e-9, None)
        draws.append(d)
    deltas = xp.empty(n_samples)
    eta2s = xp.empty(n_samples)
    for k in range(n_samples):
        m = (float(draws[0][k]), float(draws[1][k]), float(draws[2][k]))
        fit = fit_circulant(m)
        deltas[k] = fit["delta_mod_2pi_over_3"]
        eta2s[k] = fit["eta2"]
    return {
        "delta_mean": float(xp.mean(deltas)), "delta_sigma": float(xp.std(deltas)),
        "eta2_mean": float(xp.mean(eta2s)), "eta2_sigma": float(xp.std(eta2s)),
    }


def _two_sided_tail_prob(sigma: float) -> float:
    return 2.0 * (1.0 - 0.5 * (1.0 + math.erf(sigma / math.sqrt(2.0))))


def _uniform_domain_lookelsewhere_prob(central_distance: float,
                                        n_candidates: int = len(CANDIDATE_WEIGHTS),
                                        domain: float = _DOMAIN_L) -> float:
    return min(1.0, n_candidates * 2.0 * central_distance / domain)


def c2_c3_phase_analysis(n_samples: int = 20000) -> dict:
    out = {}
    for name, central, sigma, channel in [
        ("uds", MIXED_UDS_MEV, MIXED_UDS_SIGMA_MEV, "quark_mixed_koide_mc_uds"),
        ("cbt", MIXED_CBT_MEV, MIXED_CBT_SIGMA_MEV, "quark_mixed_koide_mc_cbt"),
    ]:
        fit = fit_circulant(central)
        d0 = fit["delta_mod_2pi_over_3"]
        mc = _mc_stats(central, sigma, channel, n_samples)
        distances = {}
        for cname, cval in CANDIDATE_WEIGHTS.items():
            dist = abs(d0 - cval)
            sig = dist / mc["delta_sigma"] if mc["delta_sigma"] > 0 else float("inf")
            distances[cname] = {"abs_diff_rad": dist, "sigma": sig,
                                 "two_sided_tail_p": _two_sided_tail_prob(sig)}
        nearest = min(distances.items(), key=lambda kv: kv[1]["sigma"])
        central_dist = nearest[1]["abs_diff_rad"]
        out[name] = {
            "delta_mod_2pi_over_3": d0, "mc_delta_sigma": mc["delta_sigma"],
            "eta2": fit["eta2"], "mc_eta2_sigma": mc["eta2_sigma"],
            "distances": distances,
            "nearest_candidate": nearest[0],
            "nearest_sigma_measurement_precision": nearest[1]["sigma"],
            "nearest_central_distance_rad": central_dist,
            "p_uniform_domain_lookelsewhere": _uniform_domain_lookelsewhere_prob(central_dist),
        }
    p_either = 1.0 - (1.0 - out["uds"]["p_uniform_domain_lookelsewhere"]) * \
                     (1.0 - out["cbt"]["p_uniform_domain_lookelsewhere"])
    return {"check": "C2_C3", **out,
            "p_at_least_one_of_2_tuples_this_extreme_by_chance": p_either,
            "note": ("nearest_sigma_measurement_precision answers 'is this candidate "
                     "excluded by current data' (small sigma = compatible, NOT 'found "
                     "by chance'); p_uniform_domain_lookelsewhere is the SEPARATE, "
                     "correctly-scaled range-based question 'is this central proximity "
                     "numerically unusual for a generic angle' -- see F346's review "
                     "(docs/reviews/F346-review-2026-09-02.md, Attack 7) for why these "
                     "must never be merged into one number.")}


# ---------------------------------------------------------------------------
# C4 -- (c,b,t)'s eta^2: relatively close to the lepton target, but
# decisively excluded at measurement precision -- reported as its own,
# explicit duality rather than picking one framing.
# ---------------------------------------------------------------------------

def c4_cbt_eta2_vs_lepton(n_samples: int = 20000) -> dict:
    fit = fit_circulant(MIXED_CBT_MEV)
    eta2 = fit["eta2"]
    mc = _mc_stats(MIXED_CBT_MEV, MIXED_CBT_SIGMA_MEV, "quark_mixed_koide_mc_cbt_eta2", n_samples)
    diff = abs(eta2 - _LEPTON_ETA2_TARGET)
    sigma = diff / mc["eta2_sigma"] if mc["eta2_sigma"] > 0 else float("inf")
    return {
        "check": "C4", "eta2_central": eta2, "eta2_mc_sigma": mc["eta2_sigma"],
        "lepton_target": _LEPTON_ETA2_TARGET,
        "absolute_diff": diff, "relative_diff": diff / _LEPTON_ETA2_TARGET,
        "sigma_measurement_precision": sigma,
    }


# ---------------------------------------------------------------------------
# C5 -- (u,d,s) checked for completeness (both phase and amplitude)
# ---------------------------------------------------------------------------

def c5_uds_completeness_check() -> dict:
    fit = fit_circulant(MIXED_UDS_MEV)
    return {
        "check": "C5", **fit,
        "eta2_diff_from_lepton_target": abs(fit["eta2"] - _LEPTON_ETA2_TARGET),
    }


# ---------------------------------------------------------------------------
# C6 -- lepton-sector self-check (method validation, identical to F346's C6)
# ---------------------------------------------------------------------------

def c6_lepton_selfcheck() -> dict:
    fit = fit_circulant(CHARGED_LEPTONS_MEV)
    delta_rel_err = abs(fit["delta_mod_2pi_over_3"] - delta_star_f) / delta_star_f
    eta_abs_err = abs(fit["eta"] - math.sqrt(2.0))
    return {
        "check": "C6", **fit,
        "delta_star_target_2_over_9": delta_star_f,
        "delta_relative_error": delta_rel_err,
        "eta_target_sqrt2": math.sqrt(2.0),
        "eta_absolute_error": eta_abs_err,
    }


def run_all(n_samples: int = 20000) -> dict:
    return {
        "C1": c1_fit_both_tuples(),
        "C2_C3": c2_c3_phase_analysis(n_samples),
        "C4": c4_cbt_eta2_vs_lepton(n_samples),
        "C5": c5_uds_completeness_check(),
        "C6": c6_lepton_selfcheck(),
    }


# ---------------------------------------------------------------------------
# Registry entry point (D9)
# ---------------------------------------------------------------------------

def check_quark_mixed_koide_probe_result() -> dict:
    """Entry point for tests/registry/particles.yaml (F347).

      C1_uds_Q_not_close_to_two_thirds_today  -- with CURRENT (nonzero-m_u) PDG
                                                   2024 masses, (u,d,s)'s Koide Q
                                                   is NOT close to 2/3 (>10% off),
                                                   correcting the historical
                                                   Harari-Haut-Weyers 1978 near-
                                                   hit, which relied on m_u=0.
      C1_cbt_Q_close_to_two_thirds_today      -- (c,b,t)'s Koide Q IS close to
                                                   2/3 (<1%) with current data --
                                                   Rodejohann-Zhang's claim holds.
      C1_Q_eta2_identity_holds                -- Q = 1/3 + eta^2/6 exactly, for
                                                   both tuples (delta-independent).
      C2_cbt_phase_decisively_excluded        -- (c,b,t)'s fitted delta is
                                                   incompatible (>50 sigma,
                                                   measurement precision) with
                                                   every single-irrep O_h weight.
      C3_cbt_phase_not_numerically_unusual    -- (c,b,t)'s absolute phase
                                                   proximity is NOT small under
                                                   the range-based look-elsewhere
                                                   estimate (p > 0.05) -- the
                                                   Q~2/3 coincidence carries NO
                                                   accompanying phase coincidence.
      C4_cbt_eta2_close_but_excluded          -- (c,b,t)'s eta^2 is within ~1%
                                                   of the lepton's eta^2=2 in
                                                   relative terms, but excluded
                                                   at measurement precision
                                                   (>5 sigma) -- close in percent,
                                                   not in the sense that matters.
      C5_uds_also_fails_both_axes             -- (u,d,s) matches neither the
                                                   lepton's eta^2 nor its delta
                                                   either -- a second, independent
                                                   negative alongside its failed
                                                   Q check.
      C6_method_validated_on_leptons          -- the identical fitting code
                                                   recovers F175's 2/9 and F92's
                                                   sqrt(2) from the PDG lepton
                                                   masses.

    Net verdict: the literature's Q~2/3 coincidence for (c,b,t) is REAL and
    holds under current data, but it is an eta-ONLY (amplitude-only) Koide
    coincidence -- it carries no accompanying delta (phase/shape) match, and
    even the eta^2 closeness itself is a measurement-precision miss, not a
    confirmed hit. F175/F92's stronger, TWO-parameter shape claim (both
    eta^2=2 AND delta=2/9) still finds no quark-sector face here either.
    """
    out = run_all()
    c1, cc, c4, c5, c6 = out["C1"], out["C2_C3"], out["C4"], out["C5"], out["C6"]

    checks = {
        "C1_uds_Q_not_close_to_two_thirds_today": c1["uds_Q_vs_two_thirds_rel_diff"] > 0.10,
        "C1_cbt_Q_close_to_two_thirds_today": c1["cbt_Q_vs_two_thirds_rel_diff"] < 0.01,
        "C1_Q_eta2_identity_holds": (
            abs(c1["uds"]["Q"] - c1["uds"]["Q_from_eta2_identity"]) < 1e-9
            and abs(c1["cbt"]["Q"] - c1["cbt"]["Q_from_eta2_identity"]) < 1e-9
        ),
        "C2_cbt_phase_decisively_excluded": cc["cbt"]["nearest_sigma_measurement_precision"] > 50.0,
        "C3_cbt_phase_not_numerically_unusual": cc["cbt"]["p_uniform_domain_lookelsewhere"] > 0.05,
        "C4_cbt_eta2_close_but_excluded": (
            c4["relative_diff"] < 0.02 and c4["sigma_measurement_precision"] > 5.0
        ),
        "C5_uds_also_fails_both_axes": (
            c5["eta2_diff_from_lepton_target"] > 0.3
            and cc["uds"]["nearest_sigma_measurement_precision"] > 5.0
        ),
        "C6_method_validated_on_leptons": (
            c6["delta_relative_error"] < 1e-4 and c6["eta_absolute_error"] < 1e-3
        ),
    }
    return {
        "checks": checks,
        "pass": all(checks.values()),
        "verdict": (
            "Leaning no-go, sharper than F346's: the literature's mixed-generation-type "
            "Koide tuples do not carry F175/F92's shape mechanism either. (u,d,s) "
            "(Harari-Haut-Weyers 1978) is not even close to Q=2/3 with current, nonzero "
            "up-quark mass data -- the historical near-hit relied on a since-superseded "
            "m_u=0 assumption. (c,b,t) (Rodejohann-Zhang) DOES reproduce Q~2/3 to <1% "
            "with current PDG 2024 data, a real and still-valid literature coincidence -- "
            "but Q depends only on eta (Q=1/3+eta^2/6, delta-independent, checked exactly), "
            "and decomposing it shows: the phase delta is a clean, decisive (>50 sigma) "
            "miss from every single-irrep O_h weight, and that miss is NOT numerically "
            "unusual in absolute terms either (range-based look-elsewhere p>5%) -- so the "
            "Q-coincidence carries no accompanying phase/shape coincidence. Even the "
            "eta^2 closeness that DOES drive the Q~2/3 value is itself a measurement-"
            "precision miss (many-sigma) despite looking close in percentage terms, "
            "since PDG's c,b,t masses are precise enough to resolve it. Combined with "
            "F346's same-generation-type no-go, this closes off the two literature-"
            "favoured 3-quark Koide groupings as carriers of the lepton's specific "
            "E_g/T_1u shape mechanism -- not a full closure of E6 (Rivero's signed "
            "(s,c,b) variant and other orderings/groupings remain untested), but the "
            "structurally-lepton-only reading strengthens further."
        ),
    }


if __name__ == "__main__":
    import json

    from casim.engine.particles._results_path import results_path

    out = run_all()
    out["verdict_record"] = check_quark_mixed_koide_probe_result()
    path = results_path("F347_quark_mixed_koide_probe.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"wrote {path}")
    print(out["verdict_record"]["verdict"])
