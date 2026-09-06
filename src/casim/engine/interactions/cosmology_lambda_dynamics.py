"""
cosmology_lambda_dynamics.py — is the F164 zero-point sum DYNAMICALLY made to
respect the F183/F190 capacity ceiling, or is it not?  (F332; rubric K9,
ledger G1, completeness-2026-08-18 Amendment 4)
=============================================================================

Created: 2026-08-28

**The question this closes** (Amendment 4's own named next step, restated by
the ledger's G1 addendum): F193 Part A (the "beable vacuum = 0" argument) is
EXCLUDED (CL275) because it is *uniform* -- it deletes the same per-mode 1/2
that F59 uses to build 1/G, so it cannot zero rho_vac without also zeroing G.
Two candidate routes of the right *shape* remain, neither closed: F164
channel (ii) (AB=1 dielectric sequestering, "no number") and F193 Part
B/F196/F241 (the capacity ceiling rho <= 3c^4/(8 pi G L^2), "the number to
0.10 dex, no dynamics").  This module runs three genuinely dynamical checks
against those two routes plus the ceiling's own origin, using machinery the
tree already owns (F182's Friedmann-I, F178's vacuum-only dielectric scope,
F130's proven block-spin transform) rather than restating the ceiling as a
consistency requirement.

**Result, in one line: negative on all three, and each failure is
informative.**

K1  The ceiling formula is not an import from black-hole/holographic physics
    bolted onto the model -- it IS F182's Friedmann-I constraint (itself the
    FRW reduction of the CLAUDE.md decision-4 induced Einstein equation),
    evaluated at L = R_H.  Solving that SAME equation self-consistently with
    F164's BARE (unsuppressed) zero-point density as the sole source gives a
    closed-form horizon R_H(rho_vac) = a * sqrt(3 / (g_star * I_cc)) = 0.606 a
    -- sub-lattice-cell, exact algebraic identity (matches a direct numeric
    Friedmann solve to machine precision).  This restates the problem in the
    model's own closed form; it supplies no suppression.

K2  F164 channel (ii) cannot mechanistically act on a homogeneous source at
    all.  The AB=1 lock's own field equation (F106's static Poisson law,
    which F193's brief note already flagged as blind to a constant source) is
    demonstrated here to have an EXACT Fredholm obstruction: on a periodic
    domain the equation's k=0 Fourier mode is unsolvable for any nonzero
    source mean, to machine precision -- the constant/homogeneous piece is
    not merely unabsorbed by choice, it has nowhere in the equation to go.
    Combined with F178's own restriction of the AB=1 representation to
    vacuum (T_mu_nu=0) regions -- a homogeneous vacuum-energy density is by
    definition T_mu_nu != 0 everywhere, i.e. always the "interior" case F178
    hands to the full two-function tensor treatment, never the vacuum case --
    channel (ii) is CLOSED, not merely "unevidenced."

K3/K4  Reuses F130's proven, gate-tier-verified blocking transform
    Omega_coarse(kappa) = Omega(kappa/b) -- the same tool F193's own text
    pointed at ("a block-spin / F130-style RG statement of how far the
    excitation back-reaction propagates") -- applied directly to the two
    Sakharov moments (F59/F164's I_g, I_cc), and benchmarked against F319
    U8's order-selectivity requirement.  This is NOT a derivation of F193's
    own dilution exponent p=2 (this construction's natural density scaling
    is b^-4, not F193's b^-2, so it could not produce that number even in
    principle -- reviewed 2026-08-28, see the finding's Sec.4 note); it is a
    different, related question asked with the same machinery.  K3 confirms the asymptotic power laws
    I_cc(b) ~ C_cc/b, I_g(b) ~ C_g*b (machine, exponents -1.000/+1.000).  K4
    then shows this is excluded as an order-selective mechanism: closing
    F319 U8's required 120.76-decade a0 suppression via this channel demands
    a block size that perturbs a1 (1/G) by MANY tens of orders of magnitude
    above the CODATA budget of 2.2e-5 -- an even worse failure mode than
    F319's uniform-lambda "enhancement", because here a0 falls (~b^-4) while
    a1 simultaneously RISES (~b), so no b helps both.  This is also
    diagnostic: F130's OWN correct treatment of the gravity sector (T3b, via
    real-space averaging of the log-variable u on an EXISTING field
    configuration) already showed the dielectric's source law is IR-form-
    invariant to O(b^-2) -- i.e. G does not run this way under legitimate
    coarse-graining.  The naive "recompute the coupling from a truncated BZ
    integral" move this module tests is therefore not just excluded but
    diagnosed as the WRONG tool, which sharpens what "dynamical mechanism"
    would have to mean.

**What this does not do.**  It does not derive Omega_Lambda, does not exhibit
a mechanism that supplies F319's required >=1.27e116 order-selectivity, and
does not reopen p=2 (F196) or CL275 (F311/F319's uniform-lambda exclusion,
unchanged).  Two named candidate channels are eliminated with computed,
falsifiable content (one structural/exact, one quantitative); the ceiling's
own origin is clarified as the model's cosmological law rather than an
import.  Weinberg's 1989 no-go theorem (Rev. Mod. Phys. 61, 1; see also
Padilla's review, arXiv:1502.05296) is cited for context, not derived: it
shows essentially any LOCAL, Lorentz-invariant adjustment mechanism cannot
dynamically relax a large bare CC without reintroducing the same fine-
tuning, which is exactly the failure mode of both K1's self-consistent
back-reaction and K4's naive coarse-graining (both local constructions);
the one channel of the right TYPE to evade the theorem is a non-local/
global one tied to a horizon-scale quantity, which is what the SURVIVING
F193B/F196/F241 ceiling route already is (Kaloper & Padilla, PRD 90, 103523
(2014), is the literature's own analogous move -- a global constraint, not a
local field).  That route remains open and undynamicised; this module closes
two others.
"""
from __future__ import annotations

import math

from casim.constants import a_over_ellP, c_SI, ell_P_m, hbar_SI
from casim.numerics import xp as np
from casim.numerics import fft as _fft

from casim.engine.interactions.qed_uv_completion import (
    G_REL_UNCERTAINTY,
    RHO_LAMBDA_SI,
    sakharov_moments,
    two_sector_solve,
)
from casim.engine.lattice.bcc import bcc_dispersion

__all__ = [
    "structural_G_SI",
    "ceiling_is_friedmann",
    "bare_source_horizon",
    "homogeneous_source_blind",
    "blockspin_moment",
    "blockspin_asymptotics",
    "blockspin_selectivity",
    "run",
]

GPC_M = 3.0856775814913673e25  # 1 Gpc in metres, for reporting only


# ---------------------------------------------------------------------------
# K1 -- the ceiling IS Friedmann-I; the bare source's own self-consistent
#        horizon is sub-lattice-cell
# ---------------------------------------------------------------------------
def structural_G_SI() -> float:
    """F79's structural Newton constant, G = a^2 c^3 / (8 pi sqrt3 hbar)."""
    a_m = float(a_over_ellP) * float(ell_P_m)
    return a_m ** 2 * float(c_SI) ** 3 / (8.0 * math.pi * math.sqrt(3.0) * float(hbar_SI))


def ceiling_is_friedmann(R_H_m: float) -> dict:
    """F196's ceiling rho_crit = 3 c^4/(8 pi G R_H^2) IS F182's Friedmann-I
    constraint H^2 = 8 pi G rho /(3 c^2) at H = c/R_H -- a pure substitution,
    checked here to the float floor rather than asserted."""
    G = structural_G_SI()
    c = float(c_SI)
    rho_ceiling = 3.0 * c ** 4 / (8.0 * math.pi * G * R_H_m ** 2)
    H = c / R_H_m
    rho_friedmann = 3.0 * H ** 2 * c ** 2 / (8.0 * math.pi * G)
    resid = abs(rho_ceiling - rho_friedmann) / rho_ceiling
    return {"G_SI": G, "rho_ceiling": rho_ceiling, "rho_friedmann": rho_friedmann,
            "relative_residual": resid}


def bare_source_horizon(g_star: float = 2.0, n: int = 90) -> dict:
    """Solve the model's OWN Friedmann-I constraint self-consistently with
    F164's bare (unsuppressed) zero-point density as the sole source, and
    compare the result against the closed form R_H(rho_vac) =
    a * sqrt(3/(g_star * I_cc)) -- an exact algebraic identity given F79's
    G ~ a^2 and F164's rho_vac ~ 1/a^4 share the one lattice length a."""
    I_cc, I_g = sakharov_moments(n=n)
    a_m = float(a_over_ellP) * float(ell_P_m)
    tau_s = a_m / (float(c_SI) * math.sqrt(3.0))
    rho_vac = g_star * (float(hbar_SI) / (tau_s * a_m ** 3)) * I_cc

    G = structural_G_SI()
    c = float(c_SI)
    H = math.sqrt(8.0 * math.pi * G * rho_vac / (3.0 * c ** 2))
    R_H_direct = c / H

    R_H_closed = a_m * math.sqrt(3.0 / (g_star * I_cc))
    resid = abs(R_H_direct - R_H_closed) / R_H_closed

    return {
        "I_cc": I_cc, "a_m": a_m, "rho_vac_bare_SI": rho_vac,
        "R_H_direct_m": R_H_direct, "R_H_closed_m": R_H_closed,
        "R_H_over_a": R_H_closed / a_m,
        "closed_form_relative_residual": resid,
        "ratio_to_observed_RH_dex": math.log10(1.3807e26 / R_H_direct),
    }


# ---------------------------------------------------------------------------
# K2 -- the static dielectric is exactly Fredholm-blind to a homogeneous
#        source (F164 channel (ii) has no hook)
# ---------------------------------------------------------------------------
def homogeneous_source_blind(N: int = 48, S0: float = 1.0,
                             subtract_source_mean: bool = False) -> dict:
    """F106's static weak-field law is nabla^2 u = -S.  On a periodic domain
    that has NO solution unless the source mean is zero (Fredholm
    alternative): the k=0 Fourier component of (nabla^2 u + S), for any u,
    is exactly the source mean -- there is no freedom in u to cancel it.

    Default (`subtract_source_mean=False`): feed a spatially UNIFORM source
    S = S0 (the cosmological-constant case).  Its mean is S0, so the DC
    residual/S0 must equal 1.000... to machine precision -- confirmed, not
    assumed.  Control (`subtract_source_mean=True`): the same source with its
    mean removed before solving (equivalent to feeding a genuinely
    inhomogeneous, zero-mean source) -- the DC residual/S0 collapses to ~0,
    i.e. the equation is fully solved.  The two must differ by 1.000.
    """
    S = np.full((N, N, N), S0, dtype=float)
    if subtract_source_mean:
        S = S - S.mean()
    S_hat = _fft.fftn(S)
    k = 2.0 * np.pi * np.fft.fftfreq(N)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    k2 = KX ** 2 + KY ** 2 + KZ ** 2
    u_hat = np.zeros_like(S_hat)
    nonzero = k2 > 1e-300
    u_hat[nonzero] = S_hat[nonzero] / k2[nonzero]
    u_hat[~nonzero] = 0.0  # gauge choice: no freedom to fix the DC mode
    u = _fft.ifftn(u_hat).real
    lap_u = _fft.ifftn(-k2 * u_hat).real
    residual = lap_u + S
    dc_residual_over_S0 = float(residual.mean()) / S0
    return {"S0": S0, "subtract_source_mean": subtract_source_mean,
            "dc_residual_over_S0": dc_residual_over_S0,
            "max_offdiagonal_residual": float(np.max(np.abs(residual - residual.mean())))}


# ---------------------------------------------------------------------------
# K3/K4 -- F130's own blocking transform applied to the two Sakharov moments
# ---------------------------------------------------------------------------
# Reviewed & corrected 2026-08-28 (attack 12, outside the 13-attack list):
# bcc_dispersion(kappa/b, ...) silently underflows to a spurious exact
# (0.0, 0.0) once kappa/b drops below float64's ability to resolve
# cos(x) != 1 (empirically b >~ 3e8) -- no error, no NaN.  This function is
# never called at b this large by blockspin_selectivity (which uses the
# closed-form power-law fit instead, verified in blockspin_asymptotics), but
# a direct call was a live landmine for exactly the kind of independent
# sanity check this review pass tried to run.  Guarded explicitly.
_BLOCKSPIN_MOMENT_B_MAX = 1.0e6


def blockspin_moment(b: float, n: int = 90, sign: str = "+") -> tuple[float, float]:
    """I_cc(b), I_g(b): the F164/F59 heat-kernel moments recomputed with
    F130's proven coarse dispersion Omega_coarse(kappa) = Omega(kappa/b),
    integrated over the SAME (fixed-size) Brillouin zone the fine theory
    uses.  b=1 reproduces sakharov_moments exactly (same grid convention).

    Valid for b <= 1e6 (float64 resolves kappa/b there); beyond that the
    dispersion evaluation underflows silently -- use blockspin_asymptotics'
    fitted closed form C_cc*b^p_cc / C_g*b^p_g instead, as
    blockspin_selectivity already does."""
    if b > _BLOCKSPIN_MOMENT_B_MAX:
        raise ValueError(
            f"blockspin_moment(b={b:.3e}) exceeds the validated range "
            f"(b <= {_BLOCKSPIN_MOMENT_B_MAX:.0e}); bcc_dispersion(kappa/b) "
            "underflows silently past this point.  Use "
            "blockspin_asymptotics()'s fitted C_cc*b^p_cc / C_g*b^p_g "
            "closed form instead (what blockspin_selectivity does).")
    L = 2.0 * math.pi * math.sqrt(3.0)
    g = (np.arange(n) + 0.5) / n * L - L / 2.0
    kx, ky, kz = np.meshgrid(g, g, g, indexing="ij")
    w = bcc_dispersion(kx / b, ky / b, kz / b, sign)
    dv = (L / n) ** 3 / (2.0 * math.pi) ** 3
    I_cc = float(np.sum(w / 2.0) * dv)
    inv = np.where(w > 1e-12, 1.0 / (2.0 * np.maximum(w, 1e-300)), 0.0)
    I_g = float(np.sum(inv) * dv)
    return I_cc, I_g


def blockspin_asymptotics(n: int = 200) -> dict:
    """Fit the large-b power laws I_cc(b) ~ C_cc * b^p_cc, I_g(b) ~ C_g * b^p_g
    from two decades of directly-computed b well into the asymptotic regime
    (no extrapolation), then read off the exponents.  Expectation (linear
    small-q dispersion dominates the whole coarse BZ as b grows): p_cc -> -1,
    p_g -> +1 exactly."""
    bs = [100.0, 300.0, 1000.0, 3000.0, 10000.0]
    Icc, Ig = [], []
    for b in bs:
        icc, ig = blockspin_moment(b, n=n)
        Icc.append(icc)
        Ig.append(ig)
    lb = np.log(bs)
    p_cc, log_Ccc = np.polyfit(lb, np.log(Icc), 1)
    p_g, log_Cg = np.polyfit(lb, np.log(Ig), 1)
    return {"b_values": bs, "I_cc_values": Icc, "I_g_values": Ig,
            "p_cc": float(p_cc), "C_cc": float(math.exp(log_Ccc)),
            "p_g": float(p_g), "C_g": float(math.exp(log_Cg))}


def blockspin_selectivity(required_dex: float | None = None, g_star: float = 2.0,
                          n: int = 200,
                          allowed_delta_G_over_G: float | None = None) -> dict:
    """Ask: what block size b closes F319 U8's required a0 suppression via
    THIS channel, and what does it do to a1 (1/G)?  Uses the b -> infinity
    closed forms I_cc(b) = C_cc/b, I_g(b) = C_g*b (K3's exponents, confirmed
    exact to the fit floor), which are excellent at any b this large.
    `required_dex` overrides F319 U8's own 120.76-decade requirement.
    `allowed_delta_G_over_G` overrides the CODATA relative-uncertainty budget
    (2.2e-5) the perturbation is judged against -- the control: loosening the
    budget far enough must flip `excluded` to False, proving the leg is
    reading the comparison rather than hard-coded."""
    asym = blockspin_asymptotics(n=n)
    two_sec = two_sector_solve(g_star=g_star)
    dex = required_dex if required_dex is not None else two_sec["log10_overshoot"]
    budget = (allowed_delta_G_over_G if allowed_delta_G_over_G is not None
              else G_REL_UNCERTAINTY)

    # I_cc(b)/I_cc(1) = a0(b)/a0(1) * b^3  [a0 density also divides by
    # a_coarse^3 = (b a)^3]; combined with I_cc(b) ~ C_cc/b this makes the
    # coarse DENSITY scale as b^-4 -- solve for b at the required suppression.
    p_cc = asym["p_cc"]
    b_star = 10.0 ** (dex / (3.0 - p_cc))  # density exponent = 3 - p_cc (~4)

    Icc1, Ig1 = blockspin_moment(1.0, n=n)
    C_g, p_g = asym["C_g"], asym["p_g"]
    Ig_bstar = C_g * b_star ** p_g
    # 1/G_coarse ~ I_g(b)/a_coarse^2 = I_g(b)/(b^2 a^2); relative to bare:
    G_ratio = (Ig1 / (Ig_bstar / b_star ** 2)) if b_star > 0 else float("inf")
    delta_G_over_G = abs(G_ratio - 1.0)

    excluded = delta_G_over_G > budget
    return {
        "required_dex": dex, "density_exponent_3_minus_p_cc": 3.0 - p_cc,
        "b_star": b_star, "G_ratio_coarse_over_bare": G_ratio,
        "delta_G_over_G": delta_G_over_G, "allowed_delta_G_over_G": budget,
        "excess_orders_of_magnitude": (math.log10(delta_G_over_G / budget)
                                       if delta_G_over_G > 0 else float("-inf")),
        "excluded": bool(excluded),
    }


# ---------------------------------------------------------------------------
# registry entry point
# ---------------------------------------------------------------------------
def run(**kw) -> dict:
    g_star = float(kw.get("g_star", 2.0))
    n = int(kw.get("n", 90))
    subtract_source_mean = bool(kw.get("subtract_source_mean", False))
    required_dex = kw.get("required_dex", None)
    if required_dex is not None:
        required_dex = float(required_dex)
    allowed_delta_G_over_G = kw.get("allowed_delta_G_over_G", None)
    if allowed_delta_G_over_G is not None:
        allowed_delta_G_over_G = float(allowed_delta_G_over_G)

    bare = bare_source_horizon(g_star=g_star, n=n)
    ceiling = ceiling_is_friedmann(bare["R_H_direct_m"])
    homog = homogeneous_source_blind(subtract_source_mean=subtract_source_mean)
    # Reviewed & corrected 2026-08-28 (attack 7): `n` used to stop at K1 --
    # a `casim test --param n=...` sweep silently left K3/K4 untested.
    # Threaded through here so every leg is exercised by the same lever;
    # attack 12 independently confirmed p_cc/p_g are stable under n=20..90.
    blockspin_n = max(n, 90)
    asym = blockspin_asymptotics(n=blockspin_n)
    sel = blockspin_selectivity(required_dex=required_dex, g_star=g_star,
                                n=blockspin_n,
                                allowed_delta_G_over_G=allowed_delta_G_over_G)

    checks = {
        "K1-ceiling-is-friedmann": ceiling["relative_residual"] < 1e-10,
        "K1-bare-source-subcell-horizon": (bare["closed_form_relative_residual"] < 1e-10
                                            and 0.1 < bare["R_H_over_a"] < 1.0),
        # Fixed claim under test: a homogeneous (uniform) source is fully
        # UNABSORBED by the static equation (dc residual/S0 == 1.000...).
        # The `subtract_source_mean` control feeds a de-meaned source instead
        # (which the equation DOES solve, dc residual -> 0), so this leg must
        # go red under that control -- it is not re-targeted to expect it.
        "K2-homogeneous-source-blind": abs(homog["dc_residual_over_S0"] - 1.0) < 1e-8,
        "K3-blockspin-asymptotic-exponents": (
            abs(asym["p_cc"] - (-1.0)) < 1e-3 and abs(asym["p_g"] - 1.0) < 1e-3
        ),
        "K4-blockspin-order-selectivity-excluded": sel["excluded"],
    }
    all_pass = all(checks.values())

    return {
        "finding": "F332",
        "params": {"g_star": g_star, "n": n,
                   "subtract_source_mean": subtract_source_mean,
                   "required_dex": required_dex,
                   "allowed_delta_G_over_G": allowed_delta_G_over_G},
        "checks": checks,
        "all_pass": all_pass,
        "bare_source_horizon": bare,
        "ceiling_is_friedmann": ceiling,
        "homogeneous_source_blind": homog,
        "blockspin_asymptotics": asym,
        "blockspin_selectivity": sel,
    }


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    r = run()
    assert r["all_pass"], [k for k, v in r["checks"].items() if not v]
    path = results_path("F332_cc_dynamics.json")
    with open(path, "w") as fh:
        json.dump(r, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(r, indent=2, sort_keys=True, default=str))
    print("\nwrote", path)
