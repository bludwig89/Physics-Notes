#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
casimir_scaling.py — the F294 discriminator, reinstated and then run
====================================================================

2026-08-06 - 12:05   (F299)

F294 named the computation that decides between its two readings of the F110
C7 matching:

    H1  the model's bare coupling is centre/abelian    alpha_0 = 1/(16 pi)
    H2  the matching carries the Casimir               alpha_0 = 1/(16 pi C_F)

and recommended a physical discriminator: measure sigma_R for higher
representations, because Casimir scaling favours H2 and dependence only on the
Z_N class favours H1.

F298 **withdrew** that recommendation as "degenerate at N = 3".  That
withdrawal is **too broad, and this module reverses it.**

Why the degeneracy is only the k-string restriction
---------------------------------------------------
F298 built the totally antisymmetric (k-string) tower and found that at N = 3
Casimir scaling, centre dominance and the sine law all give sigma_2/sigma_1 = 1.
That is correct, and the reason is structural: **inside the antisymmetric tower
at N = 3, irrep and N-ality are in bijection** (k = 1 <-> triality 1,
k = 2 <-> triality 2), so any law that is a function of N-ality is
automatically a function of the irrep, and vice versa.  A tower on which two
laws cannot disagree cannot discriminate between them.

F294 did not say "k-strings"; it said "higher representations".  Step outside
the antisymmetric tower and the degeneracy is gone at N = 3:

    the sextet (2,0):  triality 2 -- the SAME as the antitriplet (0,1)
                       C_2 = 10/3 -- 5/2 times the antitriplet's 4/3

so **Casimir scaling predicts sigma_6/sigma_3 = 5/2 and centre dominance
predicts 1.**  A factor of 2.5 is not a tolerance question.  The adjoint gives
9/4 against 0.  The test is live.

Then: the model's own analytic engine answers it
------------------------------------------------
`confinement.py` is an *exactly solvable* 2D SU(3) engine — in 2D axial gauge
the plaquettes are independent, so for ANY irrep R the Wilson loop factorises
and

    sigma_R = -ln w_R(beta),        w_R(beta) = < chi_R(U)/d_R >_beta

with the single-plaquette mean computed by deterministic Weyl-torus quadrature.
That engine has only ever been run in the fundamental.  This module generalises
it to arbitrary irrep characters (division-free Jacobi-Trudi, as
`su3_ladder.singlet_multiplicity_torus` already does, so there is no 0/0 at
degenerate torus points and the periodic rectangle rule stays spectral) and
runs it **at the model's own coupling**: F144's g_s = 1/2 gives
beta = 2N/g_s^2 = 24.

The answer is Casimir scaling, to sub-percent, on all seven rungs, converging
to exact as beta -> infinity.  Centre dominance is excluded on the sextet at
2.491 against 1.  **The model's own confinement sector says H2.**

The caveat, stated up front
---------------------------
d = 2 has no transverse gluons, hence no string breaking, hence centre
dominance *cannot* appear there even in principle.  So this engine cannot see
the infrared mechanism that makes centre dominance true asymptotically in
d = 4.  The reason that does not weaken the verdict: **C7 is a single-plaquette,
bare-normalisation identity.**  It fixes what one link in irrep R costs, not
what an infinitely long string costs.  Screening is an IR phenomenon and cannot
renormalise the UV cost of a link.  The regime C7 lives in is exactly the
regime where d = 2 and d = 4 agree and where the 2D computation is exact.

What that costs the B10 selector
--------------------------------
Under H2, F294's root-finding gives N_c = 1.28 — the F293/CL257 selector does
not survive.  It cannot be rescued by moving the lattice scale either:
`mu0_required_for_H2` shows H2 needs mu_0 ~ 6e24 GeV, about 5.7 decades ABOVE
the Planck mass.  So the 0.08% agreement of 1/(16 pi) with the bare coupling
the data demands is, on this evidence, a coincidence — unless someone supplies
the missing argument that the model's coupling is normalised on the centre
rather than on SU(3).  F298 said the model "cannot consistently have both";
this module says which one its own engine implements.

F298's structural leg is untouched: the C7 identity exists only for N_c <= 3
under BOTH readings, and that remains the one part of B10 that consumes no
measured number.

Cross-references: F294 (the discriminator recommended), F298 (the withdrawal
reversed here, and the N_c <= 3 leg left standing), F110/F111 (the C7 identity
and the SU(3) ladder), F144 (g_s = 1/2, hence beta = 24), F293/CL257 (the
selector this undermines), F70/F43 (the 2D-exact area law this engine is),
F94 (the 3+1D SU(3) Monte-Carlo, and what it would cost to ask it),
F86 (the BPS dual superconductor, which is a winding law, not a Casimir law).
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Dict, List, Sequence, Tuple

from casim.numerics import xp
from casim.engine.gauge.su3_ladder import casimir2, dim_irrep, triality
from casim.engine.gauge.derive_ncolour import (
    alpha_s_at_lattice_scale, MU0_GEV, MZ_GEV, ALPHA_S_MZ_PDG, N_F)

__all__ = [
    "REPS", "KSTRING_REPS", "model_wilson_beta",
    "casimir_law", "centre_law", "degeneracy_audit",
    "rep_character", "plaquette_rep_means", "sigma_ratios",
    "engine_verdict", "weak_coupling_trend",
    "mc_reach", "mu0_required_for_H2",
    "check_casimir_scaling", "summary",
]

#: (label, (p, q)) for the rungs used below.  ``3bar``, ``6`` and ``15`` are the
#: load-bearing ones: each shares its triality with a lower rung, so a
#: centre-only law is forced to predict the same tension and a Casimir law is
#: forced to predict a different one.
REPS: Tuple[Tuple[str, Tuple[int, int]], ...] = (
    ("3", (1, 0)), ("3bar", (0, 1)), ("6", (2, 0)), ("8", (1, 1)),
    ("10", (3, 0)), ("15", (2, 1)), ("15p", (4, 0)), ("27", (2, 2)),
)

#: The antisymmetric (k-string) tower at N = 3 — F298's sector, and the whole
#: extent of its degeneracy.
KSTRING_REPS: Tuple[Tuple[str, Tuple[int, int]], ...] = (
    ("3", (1, 0)), ("3bar", (0, 1)),
)

_FUND = (1, 0)


def model_wilson_beta(n_c: int = 3) -> float:
    """Wilson beta = 2N/g_s^2 at the model's own coupling.

    g_s is read from `derive_ncolour.alpha_s_at_lattice_scale` rather than
    written here, so the F144 provenance travels with the number.  g_s = 1/2
    gives beta = 24 at N = 3.
    """
    g_s = alpha_s_at_lattice_scale()["g_s"]
    return 2.0 * n_c / (g_s * g_s)


# ==========================================================================
# The two laws, exact over Q
# ==========================================================================
def casimir_law(reps: Sequence[Tuple[str, Tuple[int, int]]] = REPS
                ) -> Dict[str, Fraction]:
    """sigma_R/sigma_F = C_2(R)/C_F, exact Fractions."""
    cf = casimir2(*_FUND)
    return {nm: casimir2(p, q) / cf for nm, (p, q) in reps}


def centre_law(reps: Sequence[Tuple[str, Tuple[int, int]]] = REPS
               ) -> Dict[str, Fraction]:
    """sigma_R/sigma_F under centre dominance: a function of triality ALONE.

    Every non-zero triality is |N-ality| = 1 at N = 3, so it costs one
    fundamental string; triality 0 costs none (the source is screened).
    """
    return {nm: (Fraction(0) if triality(p, q) == 0 else Fraction(1))
            for nm, (p, q) in reps}


def degeneracy_audit(reps: Sequence[Tuple[str, Tuple[int, int]]] = REPS
                     ) -> Dict[str, Any]:
    """Is the F298 degeneracy a property of N = 3 or of the k-string tower?

    Answer: of the tower.  Inside it, irrep and triality are in bijection at
    N = 3, so the two laws are forced to agree.  Outside it they disagree by a
    factor of 5/2 on the very first rung.
    """
    cas, cen = casimir_law(reps), centre_law(reps)
    rows, splits = [], []
    for nm, (p, q) in reps:
        agree = cas[nm] == cen[nm]
        rows.append({"rep": nm, "pq": [p, q], "dim": dim_irrep(p, q),
                     "C2": str(casimir2(p, q)), "triality": triality(p, q),
                     "casimir_law": str(cas[nm]), "centre_law": str(cen[nm]),
                     "laws_agree": agree})
        if not agree:
            splits.append((nm, cas[nm], cen[nm]))

    # trialities that carry more than one Casimir -> the laws MUST separate
    by_t: Dict[int, set] = {}
    for _nm, (p, q) in reps:
        by_t.setdefault(triality(p, q), set()).add(casimir2(p, q))
    multi = {t: sorted(str(c) for c in cs) for t, cs in by_t.items()
             if len(cs) > 1}

    ks = tuple(nm for nm, _ in KSTRING_REPS)
    return {
        "rows": rows,
        "separating_reps": [nm for nm, _c, _z in splits],
        "trialities_with_several_casimirs": multi,
        "kstring_tower_is_degenerate":
            all(cas[nm] == cen[nm] for nm in ks),
        "outside_kstring_is_not_degenerate": len(splits) > 0,
        "sextet_casimir_vs_centre": (str(cas["6"]), str(cen["6"]))
        if "6" in cas else None,
        "verdict": ("the F298 degeneracy is exactly the antisymmetric-tower "
                    "restriction: at N=3 irrep <-> triality is a bijection "
                    "there, so no law that depends on one can disagree with a "
                    "law that depends on the other. The sextet shares the "
                    "antitriplet's triality and carries 5/2 its Casimir, so "
                    "outside that tower the laws separate by 5/2 vs 1"),
    }


# ==========================================================================
# The exactly solvable 2D SU(3) engine, generalised off the fundamental
# ==========================================================================
def _torus(n_grid: int):
    """Weyl-torus grid and normalised class measure on SU(3)."""
    phi = (xp.arange(n_grid) + 0.5) * 2.0 * math.pi / n_grid
    p1, p2 = xp.meshgrid(phi, phi, indexing="ij")
    p3 = -(p1 + p2)
    z = (xp.exp(1j * p1), xp.exp(1j * p2), xp.exp(1j * p3))
    meas = ((2.0 * (1.0 - xp.cos(p1 - p2)))
            * (2.0 * (1.0 - xp.cos(p1 - p3)))
            * (2.0 * (1.0 - xp.cos(p2 - p3))))
    return z, meas / meas.sum()


def _h_basis(z, k_max: int):
    """Complete homogeneous symmetric polynomials h_0..h_k_max in 3 variables.

    Division-free, so the Jacobi-Trudi determinant below never divides by a
    vanishing Weyl denominator -- that is what keeps the rectangle rule
    spectrally accurate instead of merely convergent.
    """
    h = [xp.ones_like(z[0])]
    for k in range(1, k_max + 1):
        hk = xp.zeros_like(z[0])
        for a in range(k + 1):
            m = k - a
            h12 = xp.zeros_like(z[0])
            for b in range(m + 1):
                h12 = h12 + z[0] ** b * z[1] ** (m - b)
            hk = hk + z[2] ** a * h12
        h.append(hk)
    return h


def rep_character(p: int, q: int, h):
    """chi_(p,q) on the torus as the Jacobi-Trudi determinant of h."""
    lam = (p + q, q, 0)

    def hh(k):
        return xp.zeros_like(h[0]) if k < 0 else h[k]

    m = [[hh(lam[i] - i + j) for j in range(3)] for i in range(3)]
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def plaquette_rep_means(beta: float,
                        reps: Sequence[Tuple[str, Tuple[int, int]]] = REPS,
                        n_grid: int = 240) -> Dict[str, float]:
    """w_R(beta) = <chi_R(U)/d_R> under dmu_beta ~ exp((beta/N) Re chi_F) dU."""
    z, meas = _torus(n_grid)
    k_max = max(p + q for _nm, (p, q) in reps) + 2
    h = _h_basis(z, k_max)
    # Shift by the max before exponentiating: at large beta the raw exponent
    # overflows float64 (measured: beta = 768), and the shift cancels exactly in
    # the ratio below, so this is numerically free.
    arg = (beta / 3.0) * xp.real(rep_character(*_FUND, h))
    wt = xp.exp(arg - arg.max()) * meas
    norm = wt.sum()
    return {nm: float(xp.real((rep_character(p, q, h) * wt).sum() / norm)
                      / dim_irrep(p, q))
            for nm, (p, q) in reps}


def sigma_ratios(beta: float,
                 reps: Sequence[Tuple[str, Tuple[int, int]]] = REPS,
                 n_grid: int = 240) -> Dict[str, Any]:
    """sigma_R = -ln w_R and the ratios to the fundamental.  Exact in 2D."""
    w = plaquette_rep_means(beta, reps, n_grid)
    sig = {nm: -math.log(abs(w[nm])) for nm in w}
    s_f = sig["3"]
    return {"beta": beta, "n_grid": n_grid, "w": w, "sigma": sig,
            "ratio": {nm: sig[nm] / s_f for nm in sig}}


def engine_verdict(beta: float | None = None, n_grid: int = 240,
                   reps: Sequence[Tuple[str, Tuple[int, int]]] = REPS
                   ) -> Dict[str, Any]:
    """Run the discriminator on the model's own analytic engine.

    Reports, per rung, the measured sigma_R/sigma_F against both laws, and
    cross-checks the fundamental against `confinement.string_tension` so the
    generalisation is anchored on the engine it generalises.
    """
    from casim.engine.gauge.confinement import string_tension

    if beta is None:
        beta = model_wilson_beta()
    meas = sigma_ratios(beta, reps, n_grid)
    cas, cen = casimir_law(reps), centre_law(reps)

    rows, worst_cas, worst_cen = [], 0.0, math.inf
    for nm, (p, q) in reps:
        r = meas["ratio"][nm]
        c = float(cas[nm])
        z = float(cen[nm])
        d_cas = abs(r / c - 1.0) if c else math.inf
        d_cen = abs(r - z)
        separates = cas[nm] != cen[nm]
        rows.append({"rep": nm, "triality": triality(p, q),
                     "measured": r, "casimir_law": c, "centre_law": z,
                     "rel_dev_from_casimir": d_cas,
                     "abs_dev_from_centre": d_cen,
                     "laws_separate_here": separates})
        worst_cas = max(worst_cas, d_cas)
        # Only rungs where the two laws actually DISAGREE can testify.  The
        # antitriplet agrees with both by conjugation symmetry, so including it
        # would let a rung that carries no information veto the verdict.
        if separates:
            worst_cen = min(worst_cen, d_cen)

    # No separating rung => nothing on this tower can testify against centre
    # dominance.  That is a failure to discriminate, not a clean exclusion, so
    # it must read as 0.0 rather than infinity.
    if worst_cen is math.inf:
        worst_cen = 0.0

    anchor = string_tension(beta, n_grid=n_grid)
    mine = meas["sigma"]["3"]
    return {
        "beta": beta,
        "rows": rows,
        "worst_relative_deviation_from_casimir": worst_cas,
        "smallest_deviation_from_centre_on_separating_rungs": worst_cen,
        "sextet_measured": meas["ratio"].get("6"),
        "engine_anchor_sigma_fundamental": anchor,
        "engine_anchor_residual": abs(mine - anchor),
        "law_selected": ("casimir" if worst_cas < 0.05 * worst_cen
                         else "inconclusive"),
        "verdict": ("at the model's own coupling the exactly solvable 2D SU(3) "
                    "engine follows Casimir scaling on every rung and excludes "
                    "centre dominance on the sextet; d=2 cannot show screening, "
                    "but C7 is a bare single-plaquette normalisation and "
                    "screening is an IR effect, so the regimes agree where C7 "
                    "lives"),
    }


def weak_coupling_trend(betas: Sequence[float] = (24.0, 48.0, 96.0, 192.0),
                        n_grid: int = 240) -> Dict[str, Any]:
    """Residual to exact Casimir scaling as beta grows.

    In the continuum limit of 2D lattice gauge theory sigma_R = (g_0^2/2)C_2(R)
    with g_0^2 = 2N/beta, so the residual must fall to zero -- the check that
    the sub-percent agreement at beta = 24 is the approach to an exact law and
    not a numerical coincidence at one coupling.
    """
    cas = casimir_law()
    out = []
    for b in betas:
        r = sigma_ratios(b, REPS, n_grid)["ratio"]
        worst = max(abs(r[nm] / float(cas[nm]) - 1.0) for nm in r)
        out.append({"beta": b, "worst_relative_deviation": worst})
    devs = [o["worst_relative_deviation"] for o in out]
    return {"rows": out,
            "monotone_decreasing": all(devs[i + 1] < devs[i]
                                       for i in range(len(devs) - 1)),
            "final": devs[-1]}


# ==========================================================================
# What it would cost to ask the Monte-Carlo engine
# ==========================================================================
def mc_reach(n_grid: int = 96) -> Dict[str, Any]:
    """Higher-rep Wilson loops are POLYNOMIAL in the fundamental loop matrix.

    F94's 3+1D SU(3) engine already measures planar Wilson loops as matrices,
    so measuring sigma_6, sigma_8, sigma_10 needs **no new sampling** -- only a
    different class function of the same W:

        chi_6(W)  = ( (Tr W)^2 + Tr W^2 ) / 2
        chi_8(W)  = |Tr W|^2 - 1
        chi_10(W) = ( (Tr W)^3 + 3 Tr W Tr W^2 + 2 Tr W^3 ) / 6

    Verified here on the maximal torus, which is a complete proof for class
    functions: every SU(3) element is conjugate to a torus element.
    """
    z, _meas = _torus(n_grid)
    h = _h_basis(z, 6)
    t1 = z[0] + z[1] + z[2]
    t2 = z[0] ** 2 + z[1] ** 2 + z[2] ** 2
    t3 = z[0] ** 3 + z[1] ** 3 + z[2] ** 3
    ids = {
        "6": (rep_character(2, 0, h), (t1 * t1 + t2) / 2.0),
        "8": (rep_character(1, 1, h), t1 * xp.conj(t1) - 1.0),
        "10": (rep_character(3, 0, h),
               (t1 ** 3 + 3.0 * t1 * t2 + 2.0 * t3) / 6.0),
    }
    resid = {nm: float(xp.max(xp.abs(a - b))) for nm, (a, b) in ids.items()}
    return {
        "identity_residuals": resid,
        "worst_residual": max(resid.values()),
        "extra_sampling_cost": "none — same loop matrices, different trace",
        "what_it_would_answer": ("the d=4 REGIME structure: Casimir scaling at "
                                 "intermediate R with the adjoint/decuplet "
                                 "string breaking asymptotically. That is a "
                                 "different question from C7's bare "
                                 "normalisation, and it is the one d=2 cannot "
                                 "be asked"),
        "run_parameters": {"engine": "forks/gauge/lgt_fork_A_mc.py (F94)",
                           "D": 4, "beta": [5.8, 6.0, 6.2],
                           "reps": ["3", "6", "8", "10"],
                           "estimator": "Luscher-Weisz two-level Polyakov",
                           "note": ("beta 5.8-6.2 is the scaling window; the "
                                    "model's beta = 24 is far weak-coupling "
                                    "and 2D-exact there, which is why the "
                                    "analytic engine settles C7 and the MC is "
                                    "for the IR question")},
    }


def mu0_required_for_H2() -> Dict[str, Any]:
    """Can H2 be rescued by moving the lattice scale?  No.

    One-loop: 1/alpha_0 = 1/alpha_s(M_Z) + 2 b_0 ln(mu_0/M_Z).  Feeding H2's
    bare coupling and demanding the measured alpha_s(M_Z) gives the mu_0 H2
    needs.  Compared against the Planck mass, which is the ceiling the lattice
    scale cannot exceed.
    """
    c_f = casimir2(*_FUND)                       # 4/3
    b0 = (11.0 * 3.0 - 2.0 * N_F) / (12.0 * math.pi)
    m_planck = 1.220890e19                       # GeV, CODATA
    out = {}
    for name, inv_a0 in (("H1", 16.0 * math.pi),
                         ("H2", 16.0 * math.pi * float(c_f))):
        ln_r = (inv_a0 - 1.0 / ALPHA_S_MZ_PDG) / (2.0 * b0)
        mu0 = MZ_GEV * math.exp(ln_r)
        out[name] = {"inv_alpha_0": inv_a0, "mu0_required_GeV": mu0,
                     "decades_above_planck": math.log10(mu0 / m_planck),
                     "decades_from_model_mu0": math.log10(mu0 / MU0_GEV)}
    return {"per_hypothesis": out,
            "C_F": str(c_f),
            "b0_Nf6_Nc3": b0,
            "verdict": ("H1 wants mu_0 within a few percent of the model's own "
                        "1.85e18 GeV; H2 wants ~6e24 GeV, several decades ABOVE "
                        "the Planck mass. H2 is not rescuable by rescaling the "
                        "lattice, so the conflict with the measured coupling is "
                        "structural")}


# ==========================================================================
# Registry entry point
# ==========================================================================
def check_casimir_scaling(tower: str = "full", beta: float | None = None,
                          n_grid: int = 240) -> Dict[str, Any]:
    """The F299 gate.

    Declared controls:

    ``--param tower=kstring``  restrict the discriminator to the antisymmetric
        tower.  S2 must go RED: that is F298's sector and the laws provably
        cannot disagree there, so a discriminator built on it discriminates
        nothing.  This control IS the finding — it shows the reinstatement is
        exactly about leaving the tower, not about disagreeing with F298's
        arithmetic.
    ``--param beta=2.0``       run the engine at strong coupling.  S4 must go
        RED: sigma_6/sigma_3 = 2.14 there, neither 5/2 nor 1.  The Casimir
        result is a statement about the model's OWN weak coupling, not a
        universal claim about 2D gauge theory.
    """
    reps = KSTRING_REPS if tower == "kstring" else REPS
    checks: List[Tuple[str, bool, Any]] = []

    # S1 -- the group theory, exact over Q
    ok1 = (casimir2(1, 0) == Fraction(4, 3) and casimir2(2, 0) == Fraction(10, 3)
           and casimir2(1, 1) == 3 and triality(2, 0) == triality(0, 1)
           and dim_irrep(2, 0) == 6)
    checks.append(("S1 sextet and antitriplet share triality 2 while C_2 = 10/3 "
                   "vs 4/3, exactly over Q", ok1,
                   {"C2_6": str(casimir2(2, 0)), "C2_3bar": str(casimir2(0, 1)),
                    "triality_both": triality(2, 0)}))

    # S2 -- the reinstatement
    deg = degeneracy_audit(reps)
    checks.append(("S2 the laws SEPARATE on this tower (F298's degeneracy is "
                   "the k-string restriction, not N=3)",
                   deg["outside_kstring_is_not_degenerate"],
                   deg["separating_reps"]))
    checks.append(("S2b control: inside the antisymmetric tower they provably "
                   "cannot separate", deg["kstring_tower_is_degenerate"], True))

    # S3 -- anchor the generalisation on the engine it generalises
    ev = engine_verdict(beta=beta, n_grid=n_grid, reps=reps)
    checks.append(("S3 the generalised quadrature reproduces "
                   "confinement.string_tension in the fundamental to <1e-12",
                   ev["engine_anchor_residual"] < 1e-12,
                   ev["engine_anchor_residual"]))

    # S4 -- the measurement
    checks.append(("S4 at the model's own beta the engine follows Casimir "
                   "scaling to <1.5% on every rung",
                   ev["worst_relative_deviation_from_casimir"] < 0.015,
                   ev["worst_relative_deviation_from_casimir"]))
    checks.append(("S4b ... and centre dominance is excluded: the nearest "
                   "SEPARATING rung misses its centre value by >0.4",
                   ev["smallest_deviation_from_centre_on_separating_rungs"] > 0.4,
                   ev["smallest_deviation_from_centre_on_separating_rungs"]))

    # S5 -- it is the approach to an exact law
    tr = weak_coupling_trend(n_grid=n_grid)
    checks.append(("S5 the residual to exact Casimir scaling falls "
                   "monotonically to zero as beta grows",
                   tr["monotone_decreasing"] and tr["final"] < 1e-3,
                   tr["final"]))

    # S6 -- the quadrature is spectral, not merely convergent
    a = sigma_ratios(ev["beta"], REPS, 160)["ratio"]["6"]
    b = sigma_ratios(ev["beta"], REPS, 480)["ratio"]["6"]
    checks.append(("S6 grid convergence: n=160 and n=480 agree to <1e-10",
                   abs(a - b) < 1e-10, abs(a - b)))

    # S7 -- the MC engine can be asked at zero extra sampling cost
    mc = mc_reach()
    checks.append(("S7 higher-rep loops are polynomial in the fundamental loop "
                   "matrix (residual < 1e-9), so F94 needs no new sampling",
                   mc["worst_residual"] < 1e-9, mc["worst_residual"]))

    # S8 -- H2 is not rescuable by the lattice scale
    mu = mu0_required_for_H2()
    checks.append(("S8 H2 needs mu_0 several decades ABOVE the Planck mass "
                   "while H1 lands on the model's own mu_0",
                   mu["per_hypothesis"]["H2"]["decades_above_planck"] > 3.0
                   and abs(mu["per_hypothesis"]["H1"]["decades_from_model_mu0"])
                   < 0.1,
                   {k: v["mu0_required_GeV"]
                    for k, v in mu["per_hypothesis"].items()}))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"tower": tower, "beta": beta, "n_grid": n_grid},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    ev = engine_verdict()
    deg = degeneracy_audit()
    mu = mu0_required_for_H2()
    return {
        "F299_beta_model": ev["beta"],
        "F299_separating_reps": deg["separating_reps"],
        "F299_kstring_degenerate": deg["kstring_tower_is_degenerate"],
        "F299_sextet_measured": ev["sextet_measured"],
        "F299_sextet_casimir_law": 2.5,
        "F299_sextet_centre_law": 1.0,
        "F299_worst_dev_from_casimir": ev["worst_relative_deviation_from_casimir"],
        "F299_law_selected": ev["law_selected"],
        "F299_mu0_required_H2_GeV":
            mu["per_hypothesis"]["H2"]["mu0_required_GeV"],
        "F299_mu0_required_H1_GeV":
            mu["per_hypothesis"]["H1"]["mu0_required_GeV"],
        "F299_ratios": {r["rep"]: r["measured"] for r in ev["rows"]},
    }


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    res = check_casimir_scaling()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    out = results_path("F299_casimir_scaling.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("wrote", os.path.basename(out))
