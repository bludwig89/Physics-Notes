"""
derive_quark_shape_probe.py -- F346: does the charged-lepton E_g/T_1u shape mechanism
=======================================================================================
have ANY quark-sector face?

Ledger row E6 (docs/status/open-derivations.md): the six quark (current) masses are
graded ABSENT x6 -- F121 is explicit that the numbers currently attached to them are
"the measured values converted to kg -- a CONSISTENCY readout," not a derivation, and
F123's constituent scale m_c=309.5 MeV is a DIFFERENT quantity (constituent, not
current-quark mass). No route had been proposed. E6's own suggested first question:
does the E_g/T_1u machinery that gives the charged-lepton SHAPE to 0.007% (F175, F92)
have any quark-sector face, or is it structurally lepton-only -- using F80-D4's already
-flagged Koide-Q mismatch (0.849, 0.731 vs the lepton 2/3) as the starting evidence for
"lepton-only."

The charged-lepton shape (F175 D4-D5, using F92's derived equipartition amplitude) is

    sqrt(m_a) = mu * (1 + 2*sqrt(eta2) * cos(delta + 2*pi*a/3)),   a = 0, 1, 2

with TWO independently-derived numbers: eta2 = 1/2 (F92, the 45-degree Cooper-pair
equipartition) and delta* = 2/9 rad (F175, the exact E_g representation weight
dim(E_g)/dim(T_1u tensor T_1u) = 2/9 under O_h). Both numbers come with F80's own
explanation of WHY only charged leptons reach them: only the EM-coupled, colour-free
sector couples to the clean abelian rotation that saturates the Cooper-pair/condensate
dynamics at that critical point; quarks are QCD-contaminated (F80 Sec. 5) and neutrinos
have no EM coupling at all.

This module runs the smallest useful version of E6's question: invert the SAME
3-parameter circulant ansatz on the up-type (u, c, t) and down-type (d, s, b)
current-quark mass triplets (any 3 positive numbers admit an EXACT (mu, eta, delta) fit
-- this is a coordinate change, not yet a prediction) and ask whether the resulting
angle delta (mod 2*pi/3, the residual left over after the labelling/cyclic-permutation
gauge freedom) lands near ANY of the three single-irrep O_h weights that the SAME
9-dimensional T_1u x T_1u decomposition (F175 Sec. 2) makes available:

    A_1g:  dim/9 = 1/9      E_g:  dim/9 = 2/9      T_1g or T_2g:  dim/9 = 1/3

(Combinations of more than one irrep are deliberately excluded from the candidate set:
every integer 0..9 is some subset sum of {1,2,3,3}, so comparing against subset sums
would be pure multiple-comparisons fishing. Comparing against the three single-irrep
weights mirrors what F175 actually derived -- a NAMED channel's weight, not an
arbitrary combination.)

    C1  fit (mu, eta, delta) exactly from PDG 2024 current-quark masses for each
        triplet; recover eta^2 and the Koide Q, and cross-check Q against F80-D4's
        already-recorded values (0.849, 0.731) as a pipeline sanity/regression check.
    C2  Monte Carlo propagation of the PDG mass uncertainties into the fitted delta
        (mod 2*pi/3), giving an honest MEASUREMENT-PRECISION sigma for "is this
        candidate excluded by current data" -- rather than comparing bare central
        values, which invites overclaiming.
    C3  distance, in that measurement sigma, from each sector's delta to each of
        the three candidate weights; report the nearest candidate. Small sigma
        means the data CANNOT exclude the candidate -- it is not itself evidence
        of a coincidence (a sigma near zero would mean an increasingly PRECISE
        confirmation, the opposite of "found by chance").
    C4  a SEPARATE, correctly-scaled look-elsewhere calculation: how likely is a
        generic, unrelated angle to land this close to a candidate, using the
        natural domain [0, 2*pi/3) as the scale (not the measurement precision).
        This is the right tool for "is the central proximity numerologically
        suspicious," and is kept explicitly apart from C2/C3's different
        question after a review caught an earlier draft conflating the two
        (see docs/reviews/F346-review-2026-09-02.md, Attack 7).
    C5  a lepton-sector self-check: the identical fitting code recovers F175's own
        delta*=2/9 (to 0.003%) and F92's eta=sqrt(2) (to 5 decimal places) from the
        PDG charged-lepton masses -- confirming the method is a faithful inverse of
        F175's forward construction before it is trusted on quarks.

What this module does NOT do: re-derive F175's group theory, re-run F80-D4's Koide-Q
computation from scratch (C1 cross-checks against it), or attempt the generation-COUNT
question (F75's T_1u argument makes no reference to electric charge or colour -- it
rests only on the BCC nearest-neighbour shell's point-group content and the F27
scalar-mass parity rule -- so nothing in F75 itself forbids the quark generations from
being the same T_1u triplet; that is an existing hypothesis of F75's, not a new result
of this module, and is discussed in the finding text rather than computed here).

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
# Phys. Rev. D 110, 030001 (2024), "60. Quark Masses" / summary table). u, d, s
# are MS-bar at mu=2 GeV; c, b are MS-bar at their own mass; t is the direct
# kinematic (pole-adjacent) mass, NOT a current MS-bar mass -- an inherited
# scheme inconsistency, flagged exactly as F80's own D4 flags it ("PDG quark
# masses, scheme-rough; the point/conclusion is robust"). Central values (MeV)
# and 1-sigma uncertainties (MeV):
UP_TYPE_MEV = (2.16, 1273.0, 172570.0)          # u, c, t
UP_TYPE_SIGMA_MEV = (0.07, 4.6, 290.0)
DOWN_TYPE_MEV = (4.70, 93.5, 4183.0)            # d, s, b
DOWN_TYPE_SIGMA_MEV = (0.07, 0.8, 7.0)

# Charged leptons (PDG, MeV) -- F121/F80's own values, reused verbatim for the
# C5 self-check so it is a true regression against those findings.
CHARGED_LEPTONS_MEV = (0.51099895069, 105.6583755, 1776.86)

# The three single-irrep O_h weights available in T_1u x T_1u = A_1g + E_g +
# T_1g + T_2g (dim 1+2+3+3=9), F175 Sec. 2. T_1g and T_2g share the weight 1/3.
# E_g's weight IS casim.constants.delta_star (F175) -- imported, not re-typed,
# since this module compares directly against that registered quantity (D7).
CANDIDATE_WEIGHTS = {
    "A_1g (1/9)": 1.0 / 9.0,
    "E_g (2/9)": delta_star_f,
    "T_1g_or_T_2g (1/3)": 1.0 / 3.0,
}


# ---------------------------------------------------------------------------
# The circulant fit (exact inverse of F175's forward construction)
# ---------------------------------------------------------------------------

def fit_circulant(masses: tuple[float, float, float]) -> dict:
    """Exactly solve sqrt(m_a) = mu*(1 + eta*cos(delta + 2*pi*a/3)), a=0,1,2,
    for (mu, eta, delta), via the length-3 DFT of sqrt(masses).

    Any 3 positive numbers admit such a fit (3 real degrees of freedom in, 3
    out) -- this is a coordinate change, not a prediction, exactly like
    Koide's own (mu, eta, delta) parametrization of any 3 masses. What IS a
    prediction is F175's claim that (eta, delta) take the SPECIFIC derived
    values (sqrt(2), 2/9) for charged leptons; this function only performs
    the inversion so that other triplets' (eta, delta) can be inspected.
    """
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
# C1 -- exact fit + Koide-Q cross-check against F80-D4
# ---------------------------------------------------------------------------

def c1_fit_both_sectors() -> dict:
    up = fit_circulant(UP_TYPE_MEV)
    down = fit_circulant(DOWN_TYPE_MEV)
    up["Q"] = koide_Q(UP_TYPE_MEV)
    down["Q"] = koide_Q(DOWN_TYPE_MEV)
    return {
        "check": "C1", "up_type": up, "down_type": down,
        # F80-D4's own recorded values (test_F80_em_saturation_45deg.py D4),
        # rounded to 4 places there.
        "F80_D4_Q_up_recorded": 0.849, "F80_D4_Q_down_recorded": 0.731,
    }


# ---------------------------------------------------------------------------
# C2/C3 -- Monte Carlo uncertainty propagation and candidate-weight distances
# ---------------------------------------------------------------------------

def _mc_delta_mod_std(central, sigma, channel: str, n_samples: int = 20000) -> tuple[float, float]:
    """Monte Carlo std of delta_mod under independent Gaussian mass errors."""
    gen = rng.for_channel(channel)
    draws = xp.zeros(n_samples)
    for i in range(3):
        draws_i = gen.normal(loc=central[i], scale=sigma[i], size=n_samples)
        draws_i = xp.clip(draws_i, 1e-6, None)
        if i == 0:
            samples = [draws_i]
        else:
            samples.append(draws_i)
    deltas = xp.empty(n_samples)
    for k in range(n_samples):
        m = (float(samples[0][k]), float(samples[1][k]), float(samples[2][k]))
        deltas[k] = fit_circulant(m)["delta_mod_2pi_over_3"]
    return float(xp.mean(deltas)), float(xp.std(deltas))


def _two_sided_tail_prob(sigma: float) -> float:
    """P(|Z| > sigma) for standard normal Z, stdlib-only (math.erf)."""
    return 2.0 * (1.0 - 0.5 * (1.0 + math.erf(sigma / math.sqrt(2.0))))


def c2_c3_candidate_distances(n_samples: int = 20000) -> dict:
    out = {}
    for name, central, sigma, channel in [
        ("up_type", UP_TYPE_MEV, UP_TYPE_SIGMA_MEV, "quark_shape_probe_mc_up"),
        ("down_type", DOWN_TYPE_MEV, DOWN_TYPE_SIGMA_MEV, "quark_shape_probe_mc_down"),
    ]:
        fit = fit_circulant(central)
        d0 = fit["delta_mod_2pi_over_3"]
        mean_mc, std_mc = _mc_delta_mod_std(central, sigma, channel, n_samples)
        distances = {}
        for cname, cval in CANDIDATE_WEIGHTS.items():
            dist = abs(d0 - cval)
            sig = dist / std_mc if std_mc > 0 else float("inf")
            distances[cname] = {
                "abs_diff_rad": dist, "sigma": sig,
                "two_sided_tail_p": _two_sided_tail_prob(sig),
            }
        nearest = min(distances.items(), key=lambda kv: kv[1]["sigma"])
        out[name] = {
            "delta_mod_2pi_over_3": d0, "mc_mean": mean_mc, "mc_sigma": std_mc,
            "distances": distances,
            "nearest_candidate": nearest[0], "nearest_sigma": nearest[1]["sigma"],
            "nearest_tail_p": nearest[1]["two_sided_tail_p"],
        }
    return {"check": "C2_C3", **out}


# ---------------------------------------------------------------------------
# C4 -- two DIFFERENT statistical questions, kept explicitly separate after
# review (see docs/reviews/F346-review-2026-09-02.md, Attack 7): the
# measurement-precision sigma from C2/C3 answers "is the candidate EXCLUDED by
# current data" (small sigma = compatible, NOT "found by chance" -- a sigma
# near zero would mean an increasingly PRECISE confirmation, the opposite of
# what "found by chance" should mean). "Is this central value suspiciously
# close to a nice fraction, compared to a GENERIC unrelated number" is a
# different question and needs the natural domain [0, 2*pi/3) as its scale,
# not the measurement uncertainty. This function computes THAT one properly:
# for a candidate at distance d from a uniformly-random true value on
# [0, 2*pi/3), the chance of landing within d of ANY of the 3 candidates is
# ~3*2d/L (a union bound, valid since d is much smaller than the ~L/9 gaps
# between candidates and the domain boundary here).
# ---------------------------------------------------------------------------

_DOMAIN_L = 2.0 * math.pi / 3.0


def _uniform_domain_lookelsewhere_prob(central_distance: float,
                                        n_candidates: int = len(CANDIDATE_WEIGHTS),
                                        domain: float = _DOMAIN_L) -> float:
    """P(a uniformly-random value on [0, domain) lands within central_distance
    of at least one of n_candidates points), union-bound approximation."""
    return min(1.0, n_candidates * 2.0 * central_distance / domain)


def c4_lookelsewhere_context(n_samples: int = 20000) -> dict:
    cc = c2_c3_candidate_distances(n_samples)
    per_sector = {}
    for name in ("up_type", "down_type"):
        d0 = cc[name]["delta_mod_2pi_over_3"]
        nearest_cname = cc[name]["nearest_candidate"]
        d_central = abs(d0 - CANDIDATE_WEIGHTS[nearest_cname])
        per_sector[name] = {
            "central_distance_to_nearest_rad": d_central,
            "p_uniform_domain_single_sector": _uniform_domain_lookelsewhere_prob(d_central),
        }
    p_min = min(v["p_uniform_domain_single_sector"] for v in per_sector.values())
    p_either_sector = 1.0 - (1.0 - per_sector["up_type"]["p_uniform_domain_single_sector"]) * \
                            (1.0 - per_sector["down_type"]["p_uniform_domain_single_sector"])
    p_at_least_one_this_extreme = 1.0 - (1.0 - p_min) ** 2
    return {
        "check": "C4", "domain_L_rad": _DOMAIN_L, "per_sector": per_sector,
        "p_either_sector_within_its_own_observed_distance": p_either_sector,
        "p_at_least_one_of_2_sectors_this_extreme_by_chance": p_at_least_one_this_extreme,
        "note": ("Range-based (uniform-domain) look-elsewhere probability -- NOT "
                 "the measurement-precision sigma from C2/C3, which answers a "
                 "different question (data-compatibility with the candidate, "
                 "where SMALL sigma means the candidate is NOT excluded, not "
                 "that a match was 'found by chance'). This corrects an earlier "
                 "draft of this module that used the measurement sigma for the "
                 "chance-coincidence question, which inverts the wrong direction "
                 "(a tighter future measurement landing exactly on a candidate "
                 "would have been reported as 'not significant' by that "
                 "formula) -- see the review. Under the uniform-domain null, "
                 "down-type's proximity to 1/9 is NOT common (~0.3% for that "
                 "sector alone, ~0.6% for the more extreme of the two sectors) "
                 "-- a modest but real numerical coincidence, not something to "
                 "wave away as likely by pure chance. It is still not adopted "
                 "(see C1/finding for the two reasons that do not depend on "
                 "this number: no independent theoretical motivation, and no "
                 "matching behaviour in the up-type sector)."),
    }


# ---------------------------------------------------------------------------
# C5 -- lepton-sector self-check (method validation against F175/F92)
# ---------------------------------------------------------------------------

def c5_lepton_selfcheck() -> dict:
    fit = fit_circulant(CHARGED_LEPTONS_MEV)
    delta_rel_err = abs(fit["delta_mod_2pi_over_3"] - delta_star_f) / delta_star_f
    eta_abs_err = abs(fit["eta"] - math.sqrt(2.0))
    return {
        "check": "C5", **fit,
        "delta_star_target_2_over_9": delta_star_f,
        "delta_relative_error": delta_rel_err,
        "eta_target_sqrt2": math.sqrt(2.0),
        "eta_absolute_error": eta_abs_err,
    }


def run_all(n_samples: int = 20000) -> dict:
    return {
        "C1": c1_fit_both_sectors(),
        "C2_C3": c2_c3_candidate_distances(n_samples),
        "C4": c4_lookelsewhere_context(n_samples),
        "C5": c5_lepton_selfcheck(),
    }


# ---------------------------------------------------------------------------
# Registry entry point (D9)
# ---------------------------------------------------------------------------

def check_quark_shape_probe_leaning_null_result() -> dict:
    """Entry point for tests/registry/particles.yaml (F346).

    Revised after the F346 review (docs/reviews/F346-review-2026-09-02.md,
    Attack 7): the original C3/C4 conflated two different statistical
    questions -- "is the candidate excluded by current measurement
    precision" (small sigma = compatible, and a hypothetical future exact
    match with tight precision would have sigma -> 0, which the original
    "sigma < 3.0" condition would have WRONGLY still called "not
    significant") versus "is the central value's proximity to a nice
    fraction unusual for a generic, unrelated number" (needs the natural
    [0, 2*pi/3) domain as the scale, not the measurement uncertainty). The
    checks below now keep these separate and use each for what it actually
    answers.

      C1_pipeline_matches_F80_D4          -- this module's independently
                                              recomputed Koide Q for both
                                              quark sectors reproduces F80's
                                              already-recorded values, so the
                                              new circulant-angle computation
                                              rests on the same, checked, mass
                                              inputs.
      C2_up_type_decisively_excluded      -- the up-type triplet's fitted
                                              angle is incompatible (>50
                                              sigma, measurement precision)
                                              with EVERY single-irrep O_h
                                              weight available in the SAME
                                              T_1u x T_1u decomposition that
                                              supplies the lepton's 2/9.
      C3_down_type_not_excluded_by_data   -- the down-type triplet's fitted
                                              angle is NOT excluded (< 3
                                              sigma, measurement precision)
                                              from the A_1g weight 1/9 --
                                              current data cannot rule this
                                              out, which is a genuinely
                                              different (weaker) statement
                                              than "confirmed".
      C4_lookelsewhere_not_overwhelming_but_not_dismissible -- under the
                                              CORRECT range-based (uniform-
                                              domain) look-elsewhere
                                              calculation, down-type's
                                              central proximity to 1/9 is a
                                              real, if modest, numerical
                                              coincidence (roughly 0.1-5%
                                              per the relevant single- or
                                              combined-sector probability) --
                                              neither vanishingly rare nor
                                              "likely by pure chance" the way
                                              an earlier (retracted) version
                                              of this check claimed.
      C5_amplitudes_differ_from_lepton    -- neither quark sector's fitted
                                              eta^2 is within a wide band of
                                              the lepton's derived eta^2=2
                                              (F92), consistent with F80's
                                              claim that quarks never reach
                                              the EM-driven equipartition
                                              saturation point.
      C6_method_validated_on_leptons      -- the identical fitting code
                                              recovers F175's delta*=2/9 (to
                                              <0.01%) and F92's eta=sqrt(2)
                                              (to <1e-3) from the PDG lepton
                                              masses, so the null result on
                                              quarks is not an artefact of the
                                              fitting method itself.

    The overall "not adopted" verdict for down-type does NOT rest on C4 (the
    coincidence is real, not dismissible as common) -- it rests on two
    things C4 cannot supply: no independent theoretical motivation for the
    A_1g weight in the down-type sector specifically (unlike the lepton's
    E_g, which has F80's charge/colour selection story), and no matching
    behaviour in the up-type sector, which undermines any claim of a shared
    quark-sector mechanism.
    """
    out = run_all()
    c1, cc, c4, c5 = out["C1"], out["C2_C3"], out["C4"], out["C5"]

    checks = {
        "C1_pipeline_matches_F80_D4": (
            abs(c1["up_type"]["Q"] - c1["F80_D4_Q_up_recorded"]) < 1e-3
            and abs(c1["down_type"]["Q"] - c1["F80_D4_Q_down_recorded"]) < 1e-3
        ),
        "C2_up_type_decisively_excluded": cc["up_type"]["nearest_sigma"] > 50.0,
        "C3_down_type_not_excluded_by_data": cc["down_type"]["nearest_sigma"] < 3.0,
        "C4_lookelsewhere_not_overwhelming_but_not_dismissible": (
            1e-4 < c4["p_at_least_one_of_2_sectors_this_extreme_by_chance"] < 0.05
        ),
        "C5_amplitudes_differ_from_lepton": (
            abs(c1["up_type"]["eta2"] - 2.0) > 0.5
            and abs(c1["down_type"]["eta2"] - 2.0) > 0.2
        ),
        "C6_method_validated_on_leptons": (
            c5["delta_relative_error"] < 1e-4 and c5["eta_absolute_error"] < 1e-3
        ),
    }
    return {
        "checks": checks,
        "pass": all(checks.values()),
        "verdict": (
            "Leaning no-go for ledger E6's smallest-version question: the "
            "F175/F92 E_g/T_1u SHAPE mechanism (a specific delta and eta, not "
            "just the generation count) does not carry over to either quark "
            "sector. Up-type's fitted angle is incompatible (>50 sigma, "
            "measurement precision) with every single-irrep O_h weight -- a "
            "clean, decisive miss. Down-type's fitted angle is NOT excluded "
            "by current data from the A_1g weight 1/9, and the central "
            "proximity is a real, if modest, numerical coincidence under a "
            "uniform-domain look-elsewhere estimate (roughly 0.1-5%, not "
            "vanishingly rare but not common either -- see the review for the "
            "correction of an earlier, wrong framing of this number). It is "
            "flagged, not adopted, for two reasons that do NOT depend on that "
            "probability estimate: no independent theoretical motivation for "
            "the A_1g weight in the down-type sector (unlike the lepton's "
            "E_g, which has F80's charge/colour selection story), and no "
            "matching behaviour in the up-type sector, which undermines any "
            "claim of a shared quark-sector mechanism. Not a full closure: a "
            "different quark-sector mechanism has not been ruled out, only "
            "the direct transplant of the lepton mechanism."
        ),
    }


if __name__ == "__main__":
    import json

    from casim.engine.particles._results_path import results_path

    out = run_all()
    out["verdict_record"] = check_quark_shape_probe_leaning_null_result()
    path = results_path("F346_quark_shape_probe.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"wrote {path}")
    print(out["verdict_record"]["verdict"])
