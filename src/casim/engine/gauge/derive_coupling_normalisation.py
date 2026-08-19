#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derive_coupling_normalisation.py — is F144's bare coupling centre-normalised?
=============================================================================

2026-08-06 - 19:58   (F303)

F299 left one open item and moved it from F110 to F144: **either an argument for
why the model's bare colour coupling is normalised on the centre while its
running uses the SU(N_c) beta function, or acceptance that 1/(16 pi)'s
agreement with the measured coupling is a coincidence.**

This module looks for that argument.  It does not find one, and the useful
output is *what it closes* — three candidate arguments, each killed by an exact
computation rather than by preference.

What survives of F144, and what breaks
--------------------------------------
F144's chain has three steps.  **Steps 1 and 2 survive intact.**  The rule's
per-mode (E, B) step is an exact circular rotation, and the rotor lemma says
H = (a/2)E^2 + (b/2)B^2 has an orthogonal one-tick flow **iff a = b**.  That is
a constraint on the *ratio* of electric to magnetic stiffness, so it is
**group-blind** — and by F91/decision-5 the gluon propagates by the same even
rotation law as the photon, so the lock transfers to colour legitimately rather
than being an EM result reused.

**Step 3 is the one that breaks.**  It reads the rotor's E^2 spectrum as the
integer m^2 of a compact U(1) / Z_N ladder.  For SU(3) the electric operator's
eigenvalue on a link carrying irrep R is C_2(R), and at N = 3 the two ladders
are **exactly proportional with constant C_F = 4/3** (F298).  So the dispute is
not interpretive: it is one rational number, and the model has two
irreconcilable determinations of it.

    chi = 1 (derived) AND no Casimir      ->  g_s = 1/2,     alpha_s(M_Z) = 0.1186
    chi = 1 (derived) AND the Casimir     ->  g_s = sqrt3/4, alpha_s(M_Z) = 0.0397

The measured coupling demands chi = 1.000828 — the derived chi = 1 to **0.083%**
— where the Casimir reading demands chi = 1/C_F = 0.75, 33% away.

The three candidate arguments, and why each fails
-------------------------------------------------
**(1) "The Casimir is absorbed in F144's scheme constant."**  No.  It shifts
1/alpha_0 by 16 pi (C_F - 1) = 16.755, which is **26x** F144's entire *measured*
A4 residual of 0.64, and demands Lambda_scheme/Lambda_rule = 3.4e6 against the
1.78 F144 measured and the 28.81 of the Wilson action.  (F298 said it is not
absorbable because it sits in the exponent; this is the number.)

**(2) "The colour plaquette has three links, not four."**  This is the only
reconciliation that would keep BOTH g_s = 1/2 and the Casimir, and it is
genuinely elegant: C7 reads chi = 1/(n g^2 C_F) with n the plaquette's exclusive
boundary links, so n C_F = 4 recovers the abelian answer exactly, and with
C_F = 4/3 that needs **n = 3**.  Solving n C_F(N) = 4 at n = 3 even returns
N = 3 *uniquely* (the other root is -1/3), which would have been a structural
N_c selector.  **The lattice refuses it.**  The BCC nearest-neighbour graph
admits **no closed 3-bond loop** — each component of a sum of three
(+-1, +-1, +-1) hops is a sum of three odd numbers, hence odd, hence never zero
— so the minimal gauge loop is the 4-bond rhombus, and `bcc_action.py` has said
so since F265.  Verified here both ways: the parity argument, and exhaustive
enumeration over all 8^3 hop triples (0 closed) against 8^4 quadruples (216
closed).  **n = 4 is derived geometry, not a convention, so it cannot be traded
for the Casimir.**  Recorded as a closed candidate so nobody re-derives it.

**(3) "The integer ladder is the abelian-projected Cartan charge."**  Also no,
and it fails in the opposite direction.  Every weight of the SU(3) fundamental
has |lambda|^2 = 1/3 exactly, so that reading gives alpha_0 = 3/(16 pi) and the
coupling hits a **Landau pole above M_Z** — it never reaches the Z.  So the
three candidate normalisations are 1 (integer flux), 4/3 (Casimir) and 1/3
(Cartan), and only the one with no group factor at all lands the data.

The honest conclusion
---------------------
**There is no argument, and this module now says what one would have to do.**
It would have to change the *geometric* factor in C7 without changing the
lattice (closed by (2)), or make the Casimir a scheme constant (closed by (1)),
or supply a fourth normalisation nobody has written down.  Failing that, one of
two things is true and the tree cannot currently choose: F144's 0.083% is a
coincidence, or the model's colour sector is not SU(N_c)-normalised and the
19-decade dimensional-transmutation story needs rebuilding on whatever beta
function the centre theory actually has.

Note the age of the caveat.  F101 section 7 already wrote, on 2026-06-05, that
"the precise centre projection at intermediate coupling carries the same
A-vs-C / Casimir caveat as F98-F100 (sigma_2 = 2 sigma_1 Abelian vs sigma_1
Casimir)."  F144 was built on top of that caveat a week later without resolving
it, and F294/F298/F299 rediscovered it as H1-vs-H2 two months on.  It has been
load-bearing the whole time.

Cross-references: F299 (the measurement that made this the open item, and the
engine that says Casimir), F298 (the exact proportionality of the two ladders at
N=3, constant C_F), F294 (H1/H2), F144 (the chain audited here; steps 1-2 stand,
step 3 breaks), F115 (CM3, the lock this traces), F101 (the rotor, and the
A-vs-C caveat named at the source), F110 (C7 and the integer electric field),
F91 (the gluon's even rotation law, which is why the chi = 1 lock transfers to
colour), F265 (the BCC minimal loop), CL022 (the alpha_s(M_Z) tension whose
2.1 sigma framing is contingent on H1), CL257 (the N_c card).
"""
from __future__ import annotations

import math
from fractions import Fraction
from itertools import product
from typing import Any, Dict, List, Sequence, Tuple

from casim.engine.gauge.su3_ladder import casimir2, triality
from casim.engine.gauge.derive_ncolour import (
    alpha_s_at_lattice_scale, MU0_GEV, MZ_GEV, ALPHA_S_MZ_PDG, N_F)

__all__ = [
    "circularity_lemma_is_group_blind", "ladder_proportionality",
    "plaquette_link_count", "n_that_would_rescue_gs", "scheme_absorption_test",
    "cartan_weight_norm_sq", "hypothesis_predictions", "chi_required_by_data",
    "casimir_branch_vs_f280_band",
    "check_coupling_normalisation", "summary",
]

#: F144 A4: the measured residual between the rule's 1/alpha_0 and the value the
#: measured alpha_s(M_Z) demands when run up to mu_0.  The scheme constant the
#: Casimir would have to hide inside.
F144_A4_RESIDUAL_INV_ALPHA = 0.64
#: F144 A4: the same thing as a Lambda ratio, and the Wilson-action comparison.
F144_A4_LAMBDA_RATIO = 1.78
WILSON_LAMBDA_RATIO = 28.81

# -- F280 / CL252 inputs, so the band is REBUILT here rather than quoted -------
#: Kawai-Nakayama-Seo, Nucl. Phys. B189 (1981) 40 -- SU(3) pure gauge.
#: External anchor (a target, not an input to the model's chain).
KNS_LAMBDA_RATIO_WILSON = 28.8086
#: F163, Wilson loops-only lattice constant (its Q->0 extrapolation is open;
#: it cannot move the total, only the leg1/leg3 split -- F280 S4).
F163_C_LAT_LOOPS = 6.138643
#: F163, analytic dim-reg MS-bar constant, 131/66.
F163_C_MSBAR = 131.0 / 66.0
#: F280 S5's required target on the no-C_F branch, derived there from F239's
#: exact e^(11/42) and the registered q_star_a, not written as a literal.
F280_TARGET_LAMBDA_RATIO = 1.773444


def _b0(n_c: float = 3.0, n_f: int = N_F) -> float:
    return (11.0 * n_c - 2.0 * n_f) / (12.0 * math.pi)


def _run_to_mz(alpha_0: float) -> float:
    """One-loop run of a bare coupling at mu_0 down to M_Z.  inf = Landau pole
    above M_Z (the coupling diverges before it gets there)."""
    inv = 1.0 / alpha_0 - _b0() * 2.0 * math.log(MU0_GEV / MZ_GEV)
    return 1.0 / inv if inv > 0.0 else math.inf


# ==========================================================================
# What survives: the circularity lemma constrains only a RATIO
# ==========================================================================
def circularity_lemma_is_group_blind() -> Dict[str, Any]:
    """F144 A1 step 2, re-derived symbolically, to locate what it does and does
    not fix.

    For H = (a/2)E^2 + (b/2)B^2 the one-tick flow is orthogonal **iff a = b**.
    The residual depends on a and b only through a/b, so the lemma is a
    statement about the electric/magnetic stiffness *ratio* and carries no
    representation content at all.  That is why chi = 1 survives H1-vs-H2 and
    step 3 does not.
    """
    import sympy as sp

    a, b, t = sp.symbols("a b t", positive=True)
    w = sp.sqrt(a * b)
    M = sp.Matrix([[sp.cos(w * t), b / w * sp.sin(w * t)],
                   [-a / w * sp.sin(w * t), sp.cos(w * t)]])
    resid = sp.simplify(M.T * M - sp.eye(2))
    e00 = sp.simplify(resid[0, 0] / sp.sin(w * t) ** 2)
    e11 = sp.simplify(resid[1, 1] / sp.sin(w * t) ** 2)
    e01 = sp.simplify(resid[0, 1])
    # The off-diagonal is cos*sin*(b-a)/sqrt(ab): it does NOT vanish for a != b.
    # So the orthogonality condition is the whole matrix vanishing, and that
    # happens exactly at a = b.
    vanishes_at_equal = all(sp.simplify(x.subs(b, a)) == 0
                            for x in (resid[0, 0], resid[0, 1],
                                      resid[1, 0], resid[1, 1]))
    nonzero_off_equal = sp.simplify(e00) != 0
    # The CONDITION -- not the residual -- is what must be scale-free.  Writing
    # a = r b, EVERY residual entry factorises exactly as (r - 1) times a sine
    # factor:
    #     [0,0] = (r-1) sin^2(b sqrt(r) t)      [0,1] = (1-r) sin(2 b sqrt(r) t)/(2 sqrt(r))
    # so orthogonality AT GENERIC t holds iff r = 1, whatever b is.  The lemma
    # therefore constrains the stiffness RATIO a/b and nothing else, and carries
    # no representation content.  (The residual itself is not scale-invariant --
    # omega = sqrt(ab) sets the time argument -- and the extra roots solve() finds
    # all contain t: they are ticks landing on a half-period, where the flow is
    # +-I for any stiffness, not conditions on the stiffness.)
    r = sp.symbols("r", positive=True)
    entries = [sp.simplify(x.subs(a, r * b))
               for x in (resid[0, 0], resid[0, 1], resid[1, 0], resid[1, 1])]
    divisible = all(sp.simplify(sp.expand(sp.cancel(x / (r - 1)) * (r - 1) - x))
                    == 0 for x in entries)
    vanishes_at_one = all(sp.simplify(x.subs(r, 1)) == 0 for x in entries)
    extra = set()
    for x in entries:
        for root in sp.solve(sp.Eq(x, 0), r):
            if sp.simplify(root - 1) != 0:
                extra.add(root)
    # every non-trivial root is a tick accident: it depends on t
    extras_are_tick_accidents = all(t in sp.simplify(x).free_symbols
                                    for x in extra)
    ratio_only = bool(divisible and vanishes_at_one and extras_are_tick_accidents)
    return {"residual_vanishes_at_a_equals_b": bool(vanishes_at_equal),
            "residual_nonzero_otherwise": bool(nonzero_off_equal),
            "E_residual_over_sin2": str(e00),
            "B_residual_over_sin2": str(e11),
            "offdiag_residual": str(e01),
            "depends_only_on_stiffness_ratio": bool(ratio_only),
            "condition_in_r_equals_a_over_b": "r = 1 (every residual entry "
                                              "factorises as (r-1) x sine)",
            "extra_roots_are_tick_accidents": bool(extras_are_tick_accidents),
            "n_extra_roots": len(extra),
            "vanishes_iff_a_equals_b": bool(vanishes_at_equal
                                            and nonzero_off_equal),
            "conclusion": ("the lemma fixes a/b = 1 and nothing else, so it is "
                           "group-blind: chi = 1 survives the H1/H2 dispute and "
                           "F144 step 3 (reading the E^2 spectrum) is the step "
                           "that carries the group")}


# ==========================================================================
# The dispute is one rational number
# ==========================================================================
def ladder_proportionality(n: int = 3) -> Dict[str, Any]:
    """At N = 3 the model's integer ladder and the SU(3) ladder are EXACTLY
    proportional, with constant C_F.

    The model's Z_N electric energy uses s(m)^2, which at N = 3 is 1 for both
    m = 1 and m = 2.  The lowest SU(3) irrep of each non-zero triality is the
    fundamental or its conjugate, both with C_2 = 4/3.  So the two ladders are
    the same shape and differ by the single factor 4/3 -- which is why this is
    not a matter of interpretation but of one number.
    """
    rows, ratios = [], set()
    for m in range(1, n):
        s2 = Fraction(((m + n // 2) % n) - n // 2) ** 2
        # lowest irrep of triality m: (m, 0) for m = 1, (0, 1) ~ conjugate for m = 2
        rep = (1, 0) if m == 1 else (0, 1)
        c2 = casimir2(*rep)
        rows.append({"m": m, "s_m_squared": str(s2), "lowest_irrep": rep,
                     "triality": triality(*rep), "C_2": str(c2),
                     "ratio": str(c2 / s2)})
        ratios.add(c2 / s2)
    cf = casimir2(1, 0)
    return {"rows": rows, "distinct_ratios": [str(r) for r in sorted(ratios)],
            "exactly_proportional": len(ratios) == 1,
            "constant_is_C_F": len(ratios) == 1 and ratios.pop() == cf,
            "C_F": str(cf)}


# ==========================================================================
# Candidate 2: the three-link plaquette the lattice does not have
# ==========================================================================
def plaquette_link_count(assume_three_bond_loop: bool = False) -> Dict[str, Any]:
    """Does the BCC nearest-neighbour graph admit a closed 3-bond loop?

    No, and the proof is a parity argument: each Cartesian component of a sum of
    three hops from {(+-1, +-1, +-1)} is a sum of three odd numbers, hence odd,
    hence never zero.  Checked here against exhaustive enumeration as well.

    ``assume_three_bond_loop=True`` is a declared CONTROL: it pretends the
    lattice supplies one, which must turn the no-go red.  A geometric exclusion
    that cannot fail is not an exclusion.
    """
    from casim.engine.lattice.geometry import BCC_HOP_DIRS

    dirs = [tuple(int(c) for c in d) for d in BCC_HOP_DIRS]
    n3 = sum(1 for c in product(dirs, repeat=3)
             if all(sum(v[i] for v in c) == 0 for i in range(3)))
    n4 = sum(1 for c in product(dirs, repeat=4)
             if all(sum(v[i] for v in c) == 0 for i in range(3)))
    parity = sorted({sum(s) for s in product((-1, 1), repeat=3)})
    if assume_three_bond_loop:
        n3 = 1
    return {"hop_dirs": dirs, "n_closed_3_bond": n3, "n_closed_4_bond": n4,
            "component_sums_of_three_hops": parity,
            "zero_reachable_in_three": 0 in parity,
            "minimal_loop_bonds": 3 if n3 else 4,
            "no_three_bond_loop": n3 == 0,
            "proof": ("each component of a sum of three (+-1,+-1,+-1) hops is a "
                      "sum of three odd numbers, hence odd, hence never 0")}


def n_that_would_rescue_gs(n_c: int = 3) -> Dict[str, Any]:
    """The reconciliation that would keep g_s = 1/2 *and* the Casimir.

    C7 with a Casimir reads chi = 1/(n g^2 C_F) for a plaquette with n exclusive
    boundary links, so n C_F = 4 reproduces the abelian answer exactly.  With
    C_F = 4/3 that forces n = 3, and inverting instead for N at n = 3 gives
    N = 3 *uniquely*.  Elegant, and closed by the lattice.
    """
    import sympy as sp

    cf = casimir2(1, 0)
    n_needed = Fraction(4) / cf
    N = sp.symbols("N", positive=True)
    roots = sp.solve(sp.Eq(3 * (N ** 2 - 1) / (2 * N), 4), N)
    all_roots = sp.solve(sp.Eq(3 * (N ** 2 - 1) / (2 * N) - 4, 0), N,
                         rational=True)
    return {"C_F": str(cf), "n_needed_for_gs_half": str(n_needed),
            "n_needed_is_three": n_needed == 3,
            "N_from_n3_positive_roots": [str(r) for r in roots],
            "N_from_n3_all_roots": [str(r) for r in all_roots],
            "N_is_uniquely_three": [str(r) for r in roots] == ["3"],
            "status": ("CLOSED — the BCC nearest-neighbour graph has no closed "
                       "3-bond loop, so n = 4 is derived geometry and cannot be "
                       "traded for the Casimir. Recorded so it is not "
                       "re-derived as live.")}


# ==========================================================================
# Candidate 1: can the Casimir be a scheme constant?
# ==========================================================================
def scheme_absorption_test(scheme_residual: float = F144_A4_RESIDUAL_INV_ALPHA
                           ) -> Dict[str, Any]:
    """Compare the Casimir shift in 1/alpha_0 against F144's MEASURED A4
    residual.  ``scheme_residual`` is a declared control knob."""
    cf = float(casimir2(1, 0))
    shift = 16.0 * math.pi * (cf - 1.0)
    lam = math.exp(shift / (2.0 * _b0()))
    return {"casimir_shift_inv_alpha": shift,
            "f144_A4_residual_inv_alpha": scheme_residual,
            "ratio": shift / scheme_residual,
            "lambda_ratio_demanded": lam,
            "f144_A4_lambda_ratio": F144_A4_LAMBDA_RATIO,
            "wilson_lambda_ratio": WILSON_LAMBDA_RATIO,
            "absorbable": shift <= scheme_residual,
            "conclusion": ("the shift is 26x the entire measured scheme residual "
                           "and demands a Lambda ratio of 3.4e6 against 1.78 "
                           "measured and 28.81 for the Wilson action, so it is "
                           "not a scheme constant")}


# ==========================================================================
# Candidate 3: the abelian-projected Cartan charge
# ==========================================================================
def cartan_weight_norm_sq() -> Dict[str, Any]:
    """|lambda|^2 for every weight of the SU(3) fundamental, exactly over Q.

    T^3 = diag(1,-1,0)/2 and T^8 = diag(1,1,-2)/(2 sqrt3), so the squared
    weights are rational even though T^8 is not.  All three come to 1/3.
    """
    t3 = [Fraction(1, 2), Fraction(-1, 2), Fraction(0)]
    t8_sq = [Fraction(1, 12), Fraction(1, 12), Fraction(1, 3)]  # (k/(2 sqrt3))^2
    norms = [t3[i] ** 2 + t8_sq[i] for i in range(3)]
    uniq = sorted(set(norms))
    alpha0 = float(Fraction(1, 1) / uniq[0]) / (16.0 * math.pi) if uniq else 0.0
    return {"weight_norms_sq": [str(x) for x in norms],
            "all_equal": len(uniq) == 1,
            "value": str(uniq[0]) if len(uniq) == 1 else None,
            "implied_alpha_0": alpha0,
            "alpha_s_MZ": _run_to_mz(alpha0),
            "landau_pole_above_MZ": math.isinf(_run_to_mz(alpha0)),
            "conclusion": ("|lambda|^2 = 1/3 gives alpha_0 = 3/(16 pi) and the "
                           "coupling never reaches M_Z, so the Cartan reading is "
                           "excluded outright and in the opposite direction "
                           "from the Casimir one")}


# ==========================================================================
# What the data requires
# ==========================================================================
def hypothesis_predictions() -> Dict[str, Any]:
    """alpha_s(M_Z) under each of the three normalisations."""
    cf = float(casimir2(1, 0))
    g_s = alpha_s_at_lattice_scale()["g_s"]
    out = {}
    for nm, a0, note in (
            ("H1_integer_flux", g_s ** 2 / (4.0 * math.pi), "chi=1, no Casimir"),
            ("H2_casimir", g_s ** 2 / (4.0 * math.pi * cf), "chi=1 + C_F"),
            ("H2p_cartan", 3.0 * g_s ** 2 / (4.0 * math.pi), "|lambda|^2 = 1/3")):
        a_mz = _run_to_mz(a0)
        out[nm] = {"alpha_0": a0, "g_s_eff": math.sqrt(4.0 * math.pi * a0),
                   "alpha_s_MZ": a_mz,
                   "relative_error": (math.inf if math.isinf(a_mz)
                                      else a_mz / ALPHA_S_MZ_PDG - 1.0),
                   "note": note}
    return {"per_hypothesis": out, "alpha_s_MZ_PDG": ALPHA_S_MZ_PDG}


def chi_required_by_data() -> Dict[str, Any]:
    """What chi the measured coupling demands, against the derived chi = 1 and
    the Casimir reading's chi = 1/C_F."""
    cf = float(casimir2(1, 0))
    a_req = 1.0 / (1.0 / ALPHA_S_MZ_PDG + _b0() * 2.0
                   * math.log(MU0_GEV / MZ_GEV))
    g2_req = 4.0 * math.pi * a_req
    chi_req = 1.0 / (4.0 * g2_req)
    return {"required_alpha_0": a_req, "required_g_s": math.sqrt(g2_req),
            "required_chi": chi_req,
            "derived_chi": 1.0,
            "chi_deviation_from_derived": abs(chi_req - 1.0),
            "casimir_reading_chi": 1.0 / cf,
            "chi_deviation_from_casimir_reading": abs(chi_req - 1.0 / cf),
            "chi_relative_deviation_from_casimir_reading":
                abs(chi_req / (1.0 / cf) - 1.0),
            "conclusion": ("the data wants the DERIVED chi = 1 to 0.083% and the "
                           "Casimir reading's chi = 3/4 misses by 33%")}


# ==========================================================================
# The Casimir branch against the model's OWN Lambda bracket (CL252 / F280 S5)
# ==========================================================================
def casimir_branch_vs_f280_band(casimir_on: bool = True) -> Dict[str, Any]:
    """Put the Casimir branch's required Lambda-ratio on F280's committed band.

    F303 4.1 converted the Casimir shift into a Lambda-ratio of 3.4e6 and
    compared it with two things that were available in June: F144's A4 residual
    and the Wilson action's 28.81.  It never compared it with the bracket the
    model's own d_1 apparatus had published the previous day.

    F280 S5 (record `F280-d1-subtracted`, 6/6 PASS, 2026-08-05; card CL252):

        0 <= dC_rule^loops <= dC_W^loops   =>   Lambda_MSbar/Lambda_rule in [1, 7.98]

    the lower edge from `dC >= 0`, the upper from the rule's action being nearer
    the continuum than Wilson's (F129/F130 near-perfect action; F287 4 MEASURES
    the rule's b_0 discretisation error at 5.3-5.7x smaller than Wilson's at
    every grid) together with the rule's seagull/Haar sector being exactly empty
    (F155-A0, u_0 == 1).  F280 labels the monotonicity step an assumption.

    The band is rebuilt here from the same three committed inputs rather than
    quoted, so this check moves if F163 or the KNS anchor moves.

    ``casimir_on=False`` is the declared control: with C_F -> 1 the shift
    vanishes, the Casimir branch's requirement collapses onto 1.0, which is
    INSIDE the band, and the exclusion must go red.  An exclusion that holds for
    a zero shift is not an exclusion.
    """
    cf = float(casimir2(1, 0)) if casimir_on else 1.0
    dC_W = 2.0 * math.log(KNS_LAMBDA_RATIO_WILSON)
    dC_W_loops = F163_C_LAT_LOOPS - F163_C_MSBAR
    T_W = dC_W - dC_W_loops                       # Wilson seagull + Haar
    band_lo, band_hi = 1.0, math.exp(dC_W_loops / 2.0)

    shift_inv_alpha = 16.0 * math.pi * (cf - 1.0)          # 16 pi (C_F - 1)
    lam_casimir = math.exp(shift_inv_alpha / (2.0 * _b0()))
    dC_casimir = 2.0 * math.log(lam_casimir)

    outside = lam_casimir > band_hi
    return {
        "band": [band_lo, band_hi],
        "dC_W": dC_W, "dC_W_loops": dC_W_loops, "T_W_seagull_haar": T_W,
        "casimir_shift_inv_alpha": shift_inv_alpha,
        "casimir_branch_lambda_ratio": lam_casimir,
        "casimir_branch_dC_required": dC_casimir,
        "casimir_branch_x_wilson_loops_only": (dC_casimir / dC_W_loops
                                               if dC_W_loops else math.inf),
        "casimir_branch_outside_band": bool(outside),
        "casimir_branch_decades_above_band": (math.log10(lam_casimir / band_hi)
                                              if outside else 0.0),
        "no_casimir_branch_lambda_ratio": F280_TARGET_LAMBDA_RATIO,
        "no_casimir_branch_inside_band": bool(
            band_lo <= F280_TARGET_LAMBDA_RATIO <= band_hi),
        "no_casimir_branch_position_in_band": (
            (F280_TARGET_LAMBDA_RATIO - band_lo) / (band_hi - band_lo)),
        "wilson_above_band_by": KNS_LAMBDA_RATIO_WILSON / band_hi,
        "conclusion": ("the Casimir branch needs the rule's own loops-only "
                       "one-loop constant to be ~7.2x Wilson's, for an action "
                       "F287 4 measures at 5.3-5.7x SMALLER discretisation "
                       "error than Wilson's; it lands 5.6 decades above the "
                       "band top, while the no-Casimir branch sits inside at "
                       "11% of the band.  The exclusion therefore does not "
                       "rest on F280's monotonicity assumption -- dropping it "
                       "still requires a 7.2x excess in the wrong direction"),
    }


# ==========================================================================
# Registry entry point
# ==========================================================================
def check_coupling_normalisation(assume_three_bond_loop: bool = False,
                                 scheme_residual: float
                                 = F144_A4_RESIDUAL_INV_ALPHA,
                                 casimir_on: bool = True,
                                 ) -> Dict[str, Any]:
    """The F303 gate.

    Declared controls:

    ``--param assume_three_bond_loop=True``  pretend the BCC graph supplies a
        closed 3-bond loop.  N3 must go red: the reconciliation would then work
        and the no-go would be false.  A geometric exclusion that cannot fail is
        not an exclusion.
    ``--param scheme_residual=20.0``         pretend F144's A4 residual were 20
        instead of the measured 0.64.  N4 must go red: the Casimir would then be
        absorbable, so N4 is a quantitative comparison and not a tautology.
    ``--param casimir_on=False``             (added 2026-08-18) set C_F -> 1 so
        the Casimir shift vanishes.  N8 must go red: the branch's requirement
        collapses onto Lambda = 1, which is inside F280's band, and an exclusion
        that survives a zero shift is not an exclusion.
    """
    checks: List[Tuple[str, bool, Any]] = []

    lem = circularity_lemma_is_group_blind()
    checks.append(("N1 the circularity lemma fixes only a/b, so chi = 1 is "
                   "group-blind and survives H1/H2",
                   lem["depends_only_on_stiffness_ratio"]
                   and lem["vanishes_iff_a_equals_b"],
                   lem["E_residual_over_sin2"]))

    lad = ladder_proportionality()
    checks.append(("N2 at N=3 the integer and SU(3) ladders are EXACTLY "
                   "proportional, constant C_F -- the dispute is one number",
                   lad["exactly_proportional"] and lad["constant_is_C_F"],
                   lad["distinct_ratios"]))

    geo = plaquette_link_count(assume_three_bond_loop=assume_three_bond_loop)
    resc = n_that_would_rescue_gs()
    checks.append(("N3 the BCC graph has NO closed 3-bond loop, so n = 4 is "
                   "derived geometry and cannot be traded for the Casimir",
                   geo["no_three_bond_loop"] and geo["minimal_loop_bonds"] == 4,
                   {"n3": geo["n_closed_3_bond"], "n4": geo["n_closed_4_bond"]}))
    checks.append(("N3b ... and the n it would have needed is exactly 3, which "
                   "would even have forced N_c = 3 uniquely -- recorded as a "
                   "CLOSED candidate",
                   resc["n_needed_is_three"] and resc["N_is_uniquely_three"],
                   {"n_needed": resc["n_needed_for_gs_half"],
                    "N_roots": resc["N_from_n3_positive_roots"]}))

    sch = scheme_absorption_test(scheme_residual=scheme_residual)
    checks.append(("N4 the Casimir is NOT absorbable into F144's scheme "
                   "constant (shift 16.76 vs measured residual 0.64)",
                   not sch["absorbable"] and sch["ratio"] > 10.0,
                   {"shift": sch["casimir_shift_inv_alpha"],
                    "ratio": sch["ratio"],
                    "lambda_demanded": sch["lambda_ratio_demanded"]}))

    car = cartan_weight_norm_sq()
    checks.append(("N5 the Cartan reading gives |lambda|^2 = 1/3 exactly and a "
                   "Landau pole above M_Z -- excluded outright",
                   car["all_equal"] and car["value"] == "1/3"
                   and car["landau_pole_above_MZ"],
                   car["value"]))

    hyp = hypothesis_predictions()
    h1 = hyp["per_hypothesis"]["H1_integer_flux"]
    h2 = hyp["per_hypothesis"]["H2_casimir"]
    checks.append(("N6 H1 lands alpha_s(M_Z) within 1% and H2 misses by >50% "
                   "-- the conflict is falsification-grade, not a tension",
                   abs(h1["relative_error"]) < 0.01
                   and abs(h2["relative_error"]) > 0.50,
                   {"H1": h1["alpha_s_MZ"], "H2": h2["alpha_s_MZ"]}))

    chi = chi_required_by_data()
    checks.append(("N7 the data demands the DERIVED chi = 1 to <0.1% while the "
                   "Casimir reading's chi = 3/4 misses by >30%",
                   chi["chi_deviation_from_derived"] < 0.001
                   and chi["chi_relative_deviation_from_casimir_reading"] > 0.30,
                   {"required_chi": chi["required_chi"],
                    "casimir_chi": chi["casimir_reading_chi"]}))

    bnd = casimir_branch_vs_f280_band(casimir_on=casimir_on)
    checks.append(("N8 the Casimir branch's required Lambda-ratio lies OUTSIDE "
                   "F280/CL252's committed band [1, 7.98] by >5 decades, while "
                   "the no-Casimir branch sits inside it",
                   bnd["casimir_branch_outside_band"]
                   and bnd["casimir_branch_decades_above_band"] > 5.0
                   and bnd["no_casimir_branch_inside_band"],
                   {"band": bnd["band"],
                    "casimir_lambda": bnd["casimir_branch_lambda_ratio"],
                    "decades_above": bnd["casimir_branch_decades_above_band"],
                    "x_wilson_loops_only":
                        bnd["casimir_branch_x_wilson_loops_only"]}))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"assume_three_bond_loop": assume_three_bond_loop,
                       "scheme_residual": scheme_residual,
                       "casimir_on": casimir_on},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    hyp = hypothesis_predictions()["per_hypothesis"]
    chi = chi_required_by_data()
    sch = scheme_absorption_test()
    geo = plaquette_link_count()
    return {
        "F303_argument_found": False,
        "F303_candidates_closed": ["scheme constant (26x too large)",
                                   "three-link plaquette (no 3-bond BCC loop)",
                                   "Cartan projection (Landau pole above M_Z)"],
        "F303_chi_required": chi["required_chi"],
        "F303_chi_derived": 1.0,
        "F303_chi_casimir_reading": chi["casimir_reading_chi"],
        "F303_alpha_s_MZ_H1": hyp["H1_integer_flux"]["alpha_s_MZ"],
        "F303_alpha_s_MZ_H2": hyp["H2_casimir"]["alpha_s_MZ"],
        "F303_casimir_shift_inv_alpha": sch["casimir_shift_inv_alpha"],
        "F303_scheme_ratio": sch["ratio"],
        "F303_lambda_ratio_demanded": sch["lambda_ratio_demanded"],
        "F303_n_closed_3_bond_loops": geo["n_closed_3_bond"],
        "F303_minimal_loop_bonds": geo["minimal_loop_bonds"],
    }


if __name__ == "__main__":
    import json
    import os
    from casim.engine.particles._results_path import results_path

    res = check_coupling_normalisation()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    out = results_path("F303_coupling_normalisation.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print("wrote", os.path.basename(out))
