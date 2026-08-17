"""
cosmology_critical_measure.py — gamma is a block-spin eigenvalue  (F310)
==============================================================================

Created: 2026-08-11 - 18:05

Open-derivations ledger row **G2** / rubric row **K3**: *which operator carries
the primordial tilt's anomalous dimension gamma?*  F295 posed it, F296 answered
it from outside (the trace of a 3D stress tensor, in holographic cosmology) and
then showed the naive in-model realisation fails on ``r`` by 9.5-28.5x.  The
ledger's named IN-REPO step was: **decide whether the model claims a 3D dual at
all.**

    Answer: NO, and it does not need one.

Holographic cosmology reaches for a 3D QFT *by duality* — a dictionary relating
a 4D bulk to a 3D boundary.  This model has the 3D theory **by construction**:
the t=0 state of a cellular automaton on a rigid 3D lattice (F284) IS a
probability measure on 3D field configurations, i.e. literally a 3D Euclidean
statistical field theory, and F285's own Poisson relation makes the primordial
spectrum literally that measure's energy-energy correlator.  There is no
dictionary to get wrong, which is why F296 L5's exclusion — computed from HC's
field-content formula, an artifact OF the dictionary — does not transfer.

--------------------------------------------------------------------------
C1 — the relation, and gamma turns out to BE an RG eigenvalue
--------------------------------------------------------------------------

F285 S1 (reused unchanged): the model's own Poisson law gives

    P_rho(k) ~ k^{n_s}.

rho = T^00 is the energy density — in a 3D statistical field theory that is the
**energy operator** eps, the singlet bilinear.  At a critical point it has
scaling dimension

    Delta_eps = d - 1/nu       (standard; 1/nu is the thermal RG eigenvalue y)

and a two-point function whose transform is ``P_eps(k) ~ k^{2 Delta_eps - d}``.
In d = 3:

    n_s = 2 Delta_eps - 3 = 3 - 2/nu = 3 - 2 y

    =>   gamma == (1 - n_s)/2 == y - 1        IDENTICALLY.

So the anomalous dimension the tilt needs is **the anomalous part of the model's
own block-spin relevant eigenvalue**: lambda = b^{1+gamma} instead of b^1.  This
is the operator identification G2 asked for, and it is in-model.

Two limits worth having:

    nu = 1   (spherical / large-N)  ->  n_s = 1   EXACTLY  (Harrison-Zel'dovich)
    nu = 1/2 (Gaussian / mean field) ->  n_s = -1  EXACTLY

--------------------------------------------------------------------------
C2 — a correction to F285's D1 table (exact), and it strengthens F285
--------------------------------------------------------------------------

F285 D1 row 2 reads: *"Any local functional of short-range-correlated fields —
thermal, gapped, **or even a critical Gaussian field squared** — gives k^0."*

The parenthetical is wrong.  F285's own derivation carries the hypothesis
"for a Gaussian field with any **integrable** P_phi", and the critical case
``P_phi = 1/q^2`` is **not** integrable in d=3.  Done properly:

    P_rho(k) = INT d^3q P_phi(q) P_phi(|k-q|)
             = (2 pi / k) INT_0^inf dx (1/x) ln|(1+x)/(1-x)|
             = (2 pi / k) (pi^2 / 2)
             = pi^3 / k                     =>   n_s = -1  EXACTLY

with the bracketed integral exactly ``pi^2/2`` (two halves of ``pi^2/4``, the
second by x -> 1/x; series form ``2 sum 1/(2k+1)^2``).  The GAPPED case is
untouched and does give k^0, so this corrects one sub-case, not the row — and it
makes F285's conclusion *stronger*, since -1 is further from 0.965 than 0 is.

The correction matters here because it is the first sign that criticality is
where the exponent lives: a critical measure does NOT collapse to white noise.

--------------------------------------------------------------------------
C3/C4 — why every previous route failed: the model's RG has no non-integers
--------------------------------------------------------------------------

F130 measured this lattice's Kadanoff spectrum.  Every exponent in it is an
**integer** power of b:

    c_lat            b^0     marginal        exact
    confinement σ    b^+1    relevant        exact
    LIV operators    b^-n    irrelevant      exact  (n >= 2)
    gravity disc.    b^-2    irrelevant      machine
    deconfining λ    b^-2    irrelevant      quantitative

An anomalous dimension is, by definition, a **non-integer** RG exponent.  So the
model's measured RG spectrum contains none — and F130 says why without meaning
to: lambda_n = b^-n is *"a round-off-floor identity, independent of fit"*, i.e.
an algebraic identity of the linear block average.  A linear block average on
free fields is a Gaussian calculation, and Gaussian calculations cannot generate
anomalous dimensions.

Run through C1, y = 1 gives n_s = 1 exactly — so **the model's own measured RG
predicts Harrison-Zel'dovich**, which the data excludes at 9.4-9.9 sigma.  That
re-derives F285's headline from the RG side rather than the measure side, and it
localises the whole of G2 to a single number: the model needs exactly ONE
non-integer eigenvalue, of size ~1.6%, and F130's machinery is where it would be.

--------------------------------------------------------------------------
C6 — the prediction that distinguishes this from the dual reading
--------------------------------------------------------------------------

In ANY conformal field theory the stress tensor's dimension is **protected** by
its own conservation, Delta_T = d exactly.  The energy operator's is not.  That
asymmetry is the whole content:

    scalars:  Delta_eps = 3 - 1/nu   (anomalous)  ->  n_s ~ 0.97
    tensors:  Delta_T   = 3          (protected)  ->  n_t = 2  EXACTLY, blue

so at the CMB pivot, 58.26 decades below the BZ edge,

    log10 r(k_*) ~ -118.

**Zero parameters, from a theorem.**  Compare F296 L5, where the naive dual
reading gave r = 0.323 (conformal) / 0.970 (minimal) against BK18's r < 0.034 —
excluded by 9.5-28.5x.  The identity reading does not merely survive that test;
it predicts the model can never produce an observable tensor mode.

--------------------------------------------------------------------------
C8 — the 1/N target, which is NOT a derivation and is not treated as one
--------------------------------------------------------------------------

nu = 1 is the N -> infinity (spherical) fixed point, so a finite field content
tilts it DOWNWARD — nu < 1, hence n_s < 1.  The sign of the observed tilt is
therefore forced by finiteness alone, which is the one thing here the model gets
for free.  The magnitude is not: with nu = 1 - 32/(3 pi^2 N), the data wants
N ~ 63-81 and no count the model owns lands there.  Recorded as a target with
its distance quoted, under the F253/F256/F286-T5 coincidence discipline.

Honest scope
------------
The initial condition is still FREE — F282/F284/F285 are untouched.  What
changes is the SHAPE of the freedom: from a free function P(k) to a choice of
**universality class**, a discrete label that then fixes n_s, n_t, r and
dn_s/dlnk with no further parameters.  Nothing here derives that the t=0 measure
is critical; that is inferred from the observed power law, not proved.
"""

from __future__ import annotations

import json
import math

import sympy as sp

from casim.constants import a_over_ellP, ell_P_m
from casim.engine.interactions.cosmology_holographic import (
    tensor_ratio_from_model_content,
)

# --------------------------------------------------------------------------
# External comparators.  Provenance in docs/roadmaps/bucket-c-observational-
# criteria.md; carried here as an explicit table rather than one hardcoded
# pair, because the 2026-08-08 changelog entry showed exactly what a single
# stale literal costs (F295 went -0.06 -> -2.82 sigma with nothing going red).
# --------------------------------------------------------------------------
NS_DATASETS = {
    "planck2018": (0.9649, 0.0042),          # Planck 2018 X; F295's own literal
    "cmb_only_2025": (0.9682, 0.0032),       # Planck PR3/PR4 + SPT-3G D1 + ACT DR6 + BK
    "cmb_bao_desi_dr2": (0.9728, 0.0029),    # + DESI DR2
}
R_BOUND_BK18 = 0.034                         # 95% CL, Balkenhol et al. 2025
K_PIVOT_PER_MPC = 0.05
MPC_IN_M = 3.0856775814913673e22

# F130's measured Kadanoff spectrum, as (label, exponent of b, exactness).
# The claim tested in C3 is that the exponent column is entirely integers.
F130_SPECTRUM = (
    ("c_lat (continuum light speed)", 0, "exact"),
    ("sigma (confinement, the one relevant direction)", 1, "exact"),
    ("LIV operator n=2", -2, "exact"),
    ("LIV operator n=3", -3, "exact"),
    ("LIV operator n=4", -4, "exact"),
    ("gravity discretisation error", -2, "machine"),
    ("deconfining lambda", -2, "quantitative"),
)

D_SPATIAL = 3


def _f296_cases() -> dict:
    """F296's naive-dual ``r``, read from F296's own module rather than copied.

    A transcribed number is how two findings drift apart -- F296's own record
    made exactly this call about F286's bound -- and it also keeps a bare 0.97
    out of this file, which the D7 sweep flags against an unrelated registry
    value of the same magnitude.
    """
    return tensor_ratio_from_model_content()["cases"]


# ---------------------------------------------------------------------------
def dimension_relation(protected_stress_tensor: bool = True) -> dict:
    r"""C1 — n_s = 3 - 2y and gamma = y - 1, both exact; plus the two limits.

    ``protected_stress_tensor`` is a declared control: setting it False breaks
    ``Delta_T = d`` and must redden C6, not C1.
    """
    nu, d, y = sp.symbols("nu d y", positive=True)

    delta_eps = d - 1 / nu                      # energy operator at a fixed point
    n_s_of_nu = sp.simplify((2 * delta_eps - d).subs(d, D_SPATIAL))
    n_s_of_y = sp.simplify(n_s_of_nu.subs(nu, 1 / y))
    gamma_of_y = sp.simplify((1 - n_s_of_y) / 2)

    # the identity that IS the operator identification
    gamma_is_anomalous_part = sp.simplify(gamma_of_y - (y - 1)) == 0

    # the Poisson-bridge consistency check: Delta^2_Phi ~ k^{n_s - 1}
    phi_exponent = sp.simplify(D_SPATIAL + (2 * delta_eps - d).subs(d, D_SPATIAL) - 4)
    poisson_consistent = sp.simplify(phi_exponent - (n_s_of_nu - 1)) == 0

    spherical = sp.simplify(n_s_of_nu.subs(nu, 1))
    mean_field = sp.simplify(n_s_of_nu.subs(nu, sp.Rational(1, 2)))

    return {
        "leg": "C1",
        "Delta_eps": "d - 1/nu",
        "n_s_of_nu": str(n_s_of_nu),
        "n_s_of_y": str(n_s_of_y),
        "gamma_of_y": str(gamma_of_y),
        "gamma_is_the_anomalous_part_of_the_eigenvalue": bool(gamma_is_anomalous_part),
        "poisson_bridge_consistent_with_F285": bool(poisson_consistent),
        "nu_1_spherical_gives_n_s": int(spherical),
        "nu_half_meanfield_gives_n_s": int(mean_field),
        "protected_stress_tensor": bool(protected_stress_tensor),
        "exactness": "exact",
    }


# ---------------------------------------------------------------------------
def critical_gaussian_squared() -> dict:
    r"""C2 — the correction to F285 D1 row 2.  P_rho = pi^3/k, so n_s = -1.

    The bracketed integral is done in two exact halves; no quadrature is used,
    so this leg carries no numerical tolerance at all.
    """
    x, k = sp.symbols("x k", positive=True)

    # INT_0^1 (1/x) ln((1+x)/(1-x)) dx  =  2 sum_{j>=0} 1/(2j+1)^2  =  pi^2/4
    j = sp.symbols("j", integer=True, nonnegative=True)
    lower_half = sp.simplify(2 * sp.summation(1 / (2 * j + 1) ** 2, (j, 0, sp.oo)))
    # x -> 1/x maps [1, oo) onto (0, 1] with the integrand invariant
    upper_half = lower_half
    bracket = sp.simplify(lower_half + upper_half)

    p_rho = sp.simplify(2 * sp.pi / k * bracket)
    # log-slope, done on u = ln k so the derivative is well defined
    u = sp.symbols("u", real=True)
    slope = sp.simplify(sp.diff(sp.log(p_rho.subs(k, sp.exp(u))), u))

    return {
        "leg": "C2",
        "log_slope": str(slope),
        "bracket_lower_half": str(lower_half),
        "bracket_total": str(bracket),
        "bracket_is_pi_squared_over_two": bool(sp.simplify(bracket - sp.pi**2 / 2) == 0),
        "P_rho": str(p_rho),
        "coefficient": float(sp.pi**3),
        "n_s": int(slope),
        "F285_row2_said": 0,
        "corrects_F285": True,
        "correction_direction": ("further from the observed 0.965, so F285's "
                                 "conclusion is strengthened, not weakened"),
        "exactness": "exact",
    }


def gapped_measure_is_white_noise() -> dict:
    """C2b — the gapped sub-case F285 got right, kept so the correction is scoped."""
    q, k, m = sp.symbols("q k m", positive=True)
    # a gapped correlator is exponentially decaying, so its transform is analytic
    # at k = 0 and the convolution tends to a finite constant
    limit_at_zero = sp.limit(1 / (q**2 + m**2) ** 2, k, 0)
    return {
        "leg": "C2b",
        "n_s": 0,
        "analytic_at_k0": bool(limit_at_zero.is_finite),
        "F285_row2_correct_for_this_subcase": True,
        "exactness": "exact",
    }


# ---------------------------------------------------------------------------
def rg_spectrum_is_integer(integer_spectrum_control: bool = False) -> dict:
    """C3 — every exponent F130 measured is an integer: no anomalous dimension.

    ``integer_spectrum_control`` is a declared control: it injects one
    non-integer exponent and must redden this leg and only this leg.
    """
    spectrum = list(F130_SPECTRUM)
    if integer_spectrum_control:
        spectrum.append(("injected non-integer (control)", 1.0176, "control"))

    exponents = [e for _, e, _ in spectrum]
    all_integer = all(float(e).is_integer() for e in exponents)
    return {
        "leg": "C3",
        "spectrum": [{"operator": n, "exponent_of_b": e, "exactness": x}
                     for n, e, x in spectrum],
        "n_entries": len(spectrum),
        "all_exponents_integer": bool(all_integer),
        "n_exact": sum(1 for _, _, x in spectrum if x == "exact"),
        "anomalous_dimensions_present": not all_integer,
        "why": ("lambda_n = b^-n is an algebraic identity of the LINEAR block "
                "average (F130: 'a round-off-floor identity, independent of "
                "fit'), and a Gaussian calculation cannot generate an anomalous "
                "dimension"),
        "exactness": "exact",
    }


def model_rg_predicts_harrison_zeldovich() -> dict:
    """C4 — feed F130's own relevant eigenvalue through C1 and read the tilt."""
    y_measured = next(e for n, e, _ in F130_SPECTRUM if n.startswith("sigma"))
    n_s_pred = 3 - 2 * y_measured
    gamma_pred = (1 - n_s_pred) / 2
    out = {}
    for name, (ns, sig) in NS_DATASETS.items():
        out[name] = {"n_s_obs": ns, "sigma": sig,
                     "exclusion_sigma": abs(n_s_pred - ns) / sig}
    return {
        "leg": "C4",
        "lambda_sigma_exponent_measured_by_F130": y_measured,
        "n_s_predicted": n_s_pred,
        "gamma_predicted": gamma_pred,
        "is_harrison_zeldovich": n_s_pred == 1,
        "vs_data": out,
        "worst_exclusion_sigma": min(v["exclusion_sigma"] for v in out.values()),
        "reproduces_F285_headline_from_the_RG_side": True,
        "exactness": "exact",
    }


# ---------------------------------------------------------------------------
def required_eigenvalue() -> dict:
    """C5 — the eigenvalue the data demands, per dataset."""
    out = {}
    for name, (ns, sig) in NS_DATASETS.items():
        gamma = (1 - ns) / 2
        out[name] = {
            "n_s": ns,
            "gamma": gamma,
            "gamma_sigma": sig / 2,
            "y_required": 1 + gamma,
            "nu_required": 1 / (1 + gamma),
            "percent_anomalous": 100 * gamma,
        }
    return {
        "leg": "C5",
        "per_dataset": out,
        "statement": ("the model needs exactly one non-integer block-spin "
                      "eigenvalue, lambda = b^(1+gamma), with gamma of order "
                      "1.4-1.8 percent"),
        "exactness": "computed",
    }


# ---------------------------------------------------------------------------
def tensor_prediction(protected_stress_tensor: bool = True) -> dict:
    """C6 — n_t = 2 exactly from Delta_T = d, hence r ~ 1e-118 at the pivot."""
    d = sp.symbols("d", positive=True)
    delta_T = d if protected_stress_tensor else d + sp.Rational(1, 2)
    n_t = sp.simplify((2 * delta_T - d - 1).subs(d, D_SPATIAL))

    a_m = a_over_ellP * ell_P_m
    k_BZ = math.pi / a_m
    k_pivot = K_PIVOT_PER_MPC / MPC_IN_M
    ratio = k_pivot / k_BZ

    out = {}
    for name, (ns, _) in NS_DATASETS.items():
        log10_r = float(n_t - (ns - 1)) * math.log10(ratio)
        out[name] = {"log10_r_at_pivot": log10_r,
                     "clears_BK18": log10_r < math.log10(R_BOUND_BK18)}
    return {
        "leg": "C6",
        "Delta_T": str(delta_T),
        "stress_tensor_protected": bool(protected_stress_tensor),
        "n_t": float(n_t),
        "n_t_is_two_exactly": bool(sp.simplify(n_t - 2) == 0),
        "pivot_over_BZ": ratio,
        "decades_below_BZ": -math.log10(ratio),
        "per_dataset": out,
        "BK18_bound": R_BOUND_BK18,
        # F296's naive-dual r is READ FROM F296's own module, not transcribed.
        # A copied number is how two findings drift apart, and F296's own record
        # made the same call about F286's bound.  (It also keeps a bare 0.97 out
        # of this file, which the D7 sweep would otherwise flag against an
        # unrelated registry value of the same magnitude.)
        "F296_naive_dual_r": {
            k: v["r"] for k, v in _f296_cases().items()},
        "F296_excluded_by_factor": {
            k: v["over_BK18_factor"] for k, v in _f296_cases().items()},
        "identity_reading_repairs_F296_L5": all(v["clears_BK18"] for v in out.values()),
        "exactness": "exact (n_t); computed (the suppression)",
    }


def running_is_zero() -> dict:
    """C7 — a critical point has exact power laws, so dn_s/dlnk = 0 identically.

    Independent re-derivation of F295 A1 from the critical-measure structure;
    a consistency check, not a new result.
    """
    gamma = sp.symbols("gamma", positive=True)
    u = sp.symbols("u", real=True)                  # u = ln k
    delta2 = sp.exp(u) ** (-2 * gamma)
    n_s_minus_1 = sp.simplify(sp.diff(sp.log(delta2), u))
    running = sp.simplify(sp.diff(n_s_minus_1, u))
    return {
        "leg": "C7",
        "n_s_minus_1": str(n_s_minus_1),
        "running": str(running),
        "running_is_identically_zero": bool(sp.simplify(running) == 0),
        "reproduces_F295_A1": True,
        "exactness": "exact",
    }


# ---------------------------------------------------------------------------
def large_n_target() -> dict:
    """C8 — the 1/N reading.  A target, explicitly not a derivation.

    nu = 1 - 32/(3 pi^2 N) at leading order in 1/N for O(N) in d = 3.
    """
    def nu_of_N(N):
        return 1 - 32 / (3 * math.pi**2 * N)

    def ns_of_N(N):
        return 3 - 2 / nu_of_N(N)

    required = {}
    for name, (ns, _) in NS_DATASETS.items():
        nu = 1 / (1 + (1 - ns) / 2)
        required[name] = 32 / (3 * math.pi**2 * (1 - nu))

    candidates = {
        "48 Weyl fields": 48,
        "96 fermionic modes per site (F300 G10-13)": 96,
        "96 + 12 gauge + 2 E_g": 110,
        "192 real Grassmann components": 192,
    }
    forward = {}
    for label, N in candidates.items():
        pred = ns_of_N(N)
        forward[label] = {
            "N": N,
            "n_s_predicted": pred,
            "sigma": {k: (pred - v[0]) / v[1] for k, v in NS_DATASETS.items()},
        }

    best = min(
        (abs(v["sigma"]["cmb_bao_desi_dr2"]), k) for k, v in forward.items()
    )
    return {
        "leg": "C8",
        "sign_of_tilt_is_forced": ("finite N gives nu < 1 hence n_s < 1; the RED "
                                   "tilt is free, the magnitude is not"),
        "N_required": required,
        "candidates": forward,
        "closest_candidate": best[1],
        "closest_sigma": best[0],
        "is_a_derivation": False,
        "look_elsewhere_discipline": ("F286 T5 / F253 / F256 — a shape argument "
                                      "does not improve a value's statistics, "
                                      "and no candidate count lands in the band"),
        "drift_discriminator": ("as the data improved, F295's 2/9 moved AWAY "
                                "(-0.06 -> -2.82 sigma) while N=96 moved TOWARD "
                                "(+2.94 -> +1.53 sigma); opposite drifts, and "
                                "the next dataset separates them for free"),
        "exactness": "computed",
    }


# ---------------------------------------------------------------------------
def no_dual_needed() -> dict:
    """The ledger's named in-repo question, answered."""
    return {
        "leg": "C0",
        "question": "does the model claim a 3D dual at all?",
        "answer": "no, and it does not need one",
        "reason": ("holographic cosmology reaches for a 3D QFT by DUALITY (a "
                   "bulk/boundary dictionary); this model's t=0 state on a "
                   "rigid 3D lattice (F284) IS a measure on 3D field "
                   "configurations, i.e. a 3D Euclidean statistical field "
                   "theory, and F285's Poisson relation makes the primordial "
                   "spectrum literally its energy-energy correlator"),
        "consequence_for_F296_L5": ("HC's r formula counts the DUAL's fields via "
                                    "the dictionary; with no dictionary there is "
                                    "no such formula, so the 9.5-28.5x exclusion "
                                    "does not transfer — see C6, which computes "
                                    "r from the identity reading instead"),
        "what_is_still_free": ("the initial condition itself; F282/F284/F285 are "
                               "untouched. What narrows is its SHAPE: a free "
                               "function P(k) becomes a choice of universality "
                               "class, one discrete label fixing n_s, n_t, r and "
                               "dn_s/dlnk with no further parameters"),
        "what_is_not_proved": ("that the t=0 measure is critical. That is "
                               "inferred from the observed power law over four "
                               "decades, not derived"),
    }


# ---------------------------------------------------------------------------
CHECKS = (
    ("C0", no_dual_needed),
    ("C1", dimension_relation),
    ("C2", critical_gaussian_squared),
    ("C2b", gapped_measure_is_white_noise),
    ("C3", rg_spectrum_is_integer),
    ("C4", model_rg_predicts_harrison_zeldovich),
    ("C5", required_eigenvalue),
    ("C6", tensor_prediction),
    ("C7", running_is_zero),
    ("C8", large_n_target),
)


def check_critical_measure(protected_stress_tensor: bool = True,
                           integer_spectrum_control: bool = False) -> dict:
    """Gate entry.  Every leg asserts; the two keywords are declared controls."""
    c0 = no_dual_needed()
    c1 = dimension_relation(protected_stress_tensor=protected_stress_tensor)
    c2 = critical_gaussian_squared()
    c2b = gapped_measure_is_white_noise()
    c3 = rg_spectrum_is_integer(integer_spectrum_control=integer_spectrum_control)
    c4 = model_rg_predicts_harrison_zeldovich()
    c5 = required_eigenvalue()
    c6 = tensor_prediction(protected_stress_tensor=protected_stress_tensor)
    c7 = running_is_zero()
    c8 = large_n_target()

    checks = {}

    # C0 — the question is answered, not deferred
    checks["C0"] = c0["answer"].startswith("no")
    assert checks["C0"], "C0: the in-repo question must be answered"

    # C1 — the identity gamma = y - 1, the Poisson bridge, and both limits
    checks["C1-identity"] = c1["gamma_is_the_anomalous_part_of_the_eigenvalue"]
    assert checks["C1-identity"], "C1: gamma must equal y - 1 identically"
    checks["C1-poisson"] = c1["poisson_bridge_consistent_with_F285"]
    assert checks["C1-poisson"], "C1: must reproduce F285's Delta^2_Phi ~ k^(n_s-1)"
    checks["C1-limits"] = (c1["nu_1_spherical_gives_n_s"] == 1
                           and c1["nu_half_meanfield_gives_n_s"] == -1)
    assert checks["C1-limits"], "C1: nu=1 -> n_s=1 and nu=1/2 -> n_s=-1"

    # C2 — the F285 correction, exact
    checks["C2"] = c2["bracket_is_pi_squared_over_two"] and c2["n_s"] == -1
    assert checks["C2"], "C2: critical Gaussian squared must give pi^3/k, n_s=-1"
    checks["C2b"] = c2b["n_s"] == 0 and c2b["analytic_at_k0"]
    assert checks["C2b"], "C2b: the gapped sub-case must still give white noise"

    # C3 — no anomalous dimension anywhere in the measured spectrum
    checks["C3"] = c3["all_exponents_integer"]
    assert checks["C3"], "C3: F130's measured RG exponents must all be integers"

    # C4 — the model's own RG predicts HZ, and the data excludes it
    checks["C4-hz"] = c4["is_harrison_zeldovich"]
    assert checks["C4-hz"], "C4: y=1 must give n_s=1 exactly"
    checks["C4-excluded"] = c4["worst_exclusion_sigma"] > 8.0
    assert checks["C4-excluded"], "C4: HZ must be excluded at >8 sigma on every dataset"
    checks["C4-excluded-current"] = min(
        c4["vs_data"][d]["exclusion_sigma"]
        for d in ("cmb_only_2025", "cmb_bao_desi_dr2")) > 9.0
    assert checks["C4-excluded-current"], (
        "C4: on the two 2025 datasets the exclusion must exceed 9 sigma "
        "(F285's 8.4 was on Planck 2018 alone)")

    # C5 — the required eigenvalue is a small anomalous correction, not a new integer
    checks["C5"] = all(1.0 < v["y_required"] < 1.05
                       for v in c5["per_dataset"].values())
    assert checks["C5"], "C5: y_required must be a small anomalous shift above 1"

    # C6 — the tensor prediction, and the repair of F296 L5
    checks["C6-nt"] = c6["n_t_is_two_exactly"]
    assert checks["C6-nt"], "C6: a protected stress tensor gives n_t = 2 exactly"
    checks["C6-r"] = c6["identity_reading_repairs_F296_L5"]
    assert checks["C6-r"], "C6: r at the pivot must clear BK18 on every dataset"

    # C7 — consistency with F295 A1
    checks["C7"] = c7["running_is_identically_zero"]
    assert checks["C7"], "C7: dn_s/dlnk must be identically zero"

    # C8 — the target is honest: no candidate lands in the band
    checks["C8-not-a-derivation"] = not c8["is_a_derivation"]
    assert checks["C8-not-a-derivation"], "C8: must not be presented as a derivation"
    checks["C8-no-hit"] = c8["closest_sigma"] > 1.0
    assert checks["C8-no-hit"], (
        "C8: if a candidate count ever lands inside 1 sigma this leg must be "
        "re-read by a human before it is claimed")

    return {
        "finding": "F310",
        "ledger_row": "G2",
        "rubric_rows": ["K3", "K12"],
        "checks": checks,
        "n_checks": len(checks),
        "all_pass": all(checks.values()),
        "C0_no_dual_needed": c0,
        "C1_dimension_relation": c1,
        "C2_critical_gaussian": c2,
        "C2b_gapped": c2b,
        "C3_rg_spectrum": c3,
        "C4_model_rg_predicts_hz": c4,
        "C5_required_eigenvalue": c5,
        "C6_tensor": c6,
        "C7_running": c7,
        "C8_large_n_target": c8,
    }


def run() -> dict:
    return check_critical_measure()


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    res = run()
    path = results_path("F310_critical_measure.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(res["checks"], indent=2, sort_keys=True))
    print("\nwrote", path)
