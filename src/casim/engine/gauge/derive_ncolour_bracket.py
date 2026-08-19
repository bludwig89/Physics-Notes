#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derive_ncolour_bracket.py — the N_c interval, closed from both sides
====================================================================

2026-08-17

F317 sec 10 ("Remains", item 2) named the shortest route to closing B10:

    A lattice-structural replacement for "baryons have three constituents"
    would make sec 6 a derivation; F298's N_c <= 3 is the only other
    structural leg the tree has, and pairing them is the shortest route to
    closing B10 without the F293 selector.

This module executes that.  It supplies the missing LOWER constraint, pairs it
with F298's upper one, and the pair leaves a single integer.

WHAT IS NEW HERE, STATED FIRST
------------------------------

**The parity argument is NOT new and is not claimed as new.**  Baer & Wiese,
"Can one see the number of colors?", Nucl. Phys. B609 (2001) 225
(hep-ph/0105258), write verbatim:

    "In order to cancel Witten's global anomaly, the number of colors must be
    odd in the standard model."

and obtain it UNCONDITIONALLY by imposing cancellation separately for each
generation, which is stronger than the total-count form used as the default
here.  What is new in this module is only:

  * that the group and the content it is evaluated on are DERIVED in this tree
    (F27 beta-gauging; the F279/F293 nullspace) rather than assumed;
  * the PAIRING with F298's C7 support, which is what turns a parity into a
    unique integer;
  * the consequence: F317 sec 6's empirical input is discharged.

The incremental content over F298 is ONE BIT.  F298 already left {2, 3}; this
selects between them.

THE TWO CONSTRAINTS
-------------------

**UPPER (F298, imported).**  A single level-independent chi requires
C_2(antisym k) proportional to the model's own rotor level s(k)^2.  That holds
at N = 2 (vacuously -- ONE level) and N = 3 (non-trivially -- two conjugate
levels) and fails for every N >= 4.  Support: {2, 3}.

  RESTRICTION INHERITED FROM F298, AND IT CUTS BOTH WAYS.  The tower is the
  k-string (totally antisymmetric) sector, not the full link Hilbert space --
  F110 deferred the rest and `casimir_ladder`'s own scope note says so.  The
  direction usually named is that mixed-symmetry irreps might RESTORE
  level-independence at N >= 4.  The direction that is not usually named, and
  that this module measures, is that they BREAK it at N = 3 as well: the
  sextet (2,0) carries N-ality 2, so the model's rotor rule gives s^2 = 1
  against C_2 = 10/3, i.e. chi = 3/10 against the tower's 3/4.  The support
  {2, 3} is a property of the truncation, not yet of the model.

**LOWER (prior art, evaluated on derived content).**  pi_4(SU(2)) = Z_2, so an
SU(2) gauge theory whose Weyl content contains an odd number of isospin-1/2
doublets has no well-defined path integral (Witten 1982).  The model carries
n_gen * (dim R_colour + 1) doublets.  Even => for odd n_gen, and for
R_colour = fundamental, N_c is ODD.

  AND THE SAME ANSWER ARRIVES LOCALLY.  If the model's true electroweak factor
  is U(2) rather than SU(2) x U(1) -- i.e. if hypercharge is quantised so the
  Z_2 quotient acts -- then Davighi/Gripaios/Lohitsiri's rule q = 2j (mod 2)
  makes the doublet parity a LOCAL condition instead of a global one
  (1910.11277, 2001.07731).  On this model's own nullspace y_Q = 1 and
  y_L = -N_c, so "every doublet carries odd hypercharge" reads exactly N_c
  odd.  Both readings give the same constraint, which is why the conclusion
  does not wait on the tree settling its global gauge-group structure.

    {N_c odd}  AND  {C7 support}  =  {3}, over N = 1..12.

WHAT IS CONSUMED — ALL OF IT
----------------------------

Six premises, not two, booked here rather than in a Remains section:

  (i)   n_gen is ODD (F75; only the parity is used).  Replaceable by Baer &
        Wiese's per-generation consistency assumption, which needs no
        generation count -- exposed as `per_generation`.
  (ii)  the colour sector exists, i.e. the C7 identity has an object.  F318's
        standing residual.  This is what excludes N = 1, and that exclusion is
        a RESTATEMENT of the premise, not an independent leg -- see
        `_c7_exists_on_ladder`'s convention switch.
  (iii) the rotor modulus is the centre Z_{N_c}.  The upper constraint is a
        function of N_c only through this identification (F97/F99), which was
        adopted in a tree already built at Z_3.
  (iv)  quarks sit in the DEFINING representation with multiplicity N_c.  A
        colour-sector fact, and the lower constraint consumes it: in the
        adjoint the parity inverts and the bracket returns {2}.  Exposed as
        `quark_colour_rep`.
  (v)   the chiral multiplet structure -- exactly one colour-singlet lepton
        doublet per generation, right-handers SU(2) singlets.  Posited in
        `derive_ncolour`'s six-row system; not derived anywhere in this chain.
  (vi)  no fermion doubling (f = 1).  CL020 is `narrowed`.  An even species
        multiplicity trivialises the mod-2 count outright -- and worse, a
        naively doubled spectrum is VECTOR-LIKE, so by Nielsen-Ninomiya there
        is no chiral gauge theory left to constrain.  The constraint survives
        only in a doubler-free (Ginsparg-Wilson) formulation, where Baer &
        Campos (hep-lat/0001025) exhibit the lattice analogue of Witten's
        obstruction.

What is NOT consumed: any measured NUMBER; the three-constituent baryon; and
either branch of the X1 colour-normalisation fork.  "No measured number" is not
the same as "no empirical input", and this module does not use them
interchangeably.

THE TRADE
---------
F317 sec 6 consumed "baryons are three-constituent bound states".  Given
premise (iv) and a totally antisymmetric singlet, the constituent count IS
N_c -- so that input was never information about the model independent of the
answer.  The premises above are more numerous but none is equivalent to the
answer.  The improvement is in PROXIMITY, not in empirical status and not in
premise count.

FALSIFIABILITY, THE COMPENSATING VIRTUE
---------------------------------------
At a true N_c >= 4 the bracket returns the EMPTY set -- the model would be
falsified, and F144's g_s derivation would lose its object with it.  This is
not an argument that can only succeed.

Cross-references: F317 (sec 10 item 2, the close this executes; sec 6, whose
input this discharges), F298 (the upper constraint, imported), F318 (premise
(ii); the double-count it flagged), F293 (R1 -- the local ANOMALY-CANCELLATION
system, measured blind here; sec 4.2's selector, no longer needed), F279 (the
six-row system), F27 (the chirality without which the parity is vacuous), F75
(premise (i)), F97/F99 (premise (iii)), F144/F110 (the C7 identity), CL020
(premise (vi)), F299/F303 (X1, untouched).
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Any, Dict, List, Sequence, Tuple

import sympy as sp

from casim.engine.gauge.casimir_ladder import (
    antisymmetric_ladder,
    c7_against_casimir_ladder,
    casimir_fundamental,
    su_n_casimir,
    zn_symmetric_residue_sq,
)
from casim.engine.gauge.derive_ncolour import hypercharge_nullspace_symbolic

# The model's generation count (F75).  Only its PARITY is ever used.
N_GEN_MODEL = 3

# Quark colour representations as dimension functions of N.  `fundamental` is
# premise (iv); the others exist so that premise can be broken by a control.
COLOUR_REPS = {
    "fundamental": lambda n: n,
    "adjoint": lambda n: n * n - 1,
    "two_index_antisym": lambda n: n * (n - 1) // 2,
    "symmetric": lambda n: n * (n + 1) // 2,
}


# ==========================================================================
# G0 — the mod-2 index rule, quoted so it can be disputed
# ==========================================================================
def witten_contributes(two_j: int) -> bool:
    """Does a Weyl fermion of isospin j = two_j/2 carry SU(2)'s Z_2 anomaly?

    Witten (1982): the obstruction is the mod-2 index of the Dirac operator in
    the isospin-j representation, non-trivial iff 2j = 1 (mod 4).  Verified on
    the lattice by Baer & Campos (hep-lat/0209098) at j = 1/2, 3/2, 5/2.

    CAVEAT that must not be omitted even though it does not bite here: on
    NON-SPIN manifolds carrying a spin-SU(2) structure there is a further
    obstruction at isospin 4r + 3/2 (Wang, Wen & Witten, 1810.00844).  The
    model has no isospin-3/2 field, so only the 2j = 1 clause is ever used --
    which is what G0 asserts rather than assumes.

    QUOTED, not derived.  Isolated in one function so a reader who disputes it
    can see exactly what is used and where.
    """
    return two_j % 4 == 1


def dynkin_index_normalised(two_j: int) -> Fraction:
    """T(j) normalised to T(1/2) = 1: T = (4/3) j (j+1) (2j+1) / 2.

    Gives 1, 4, 10, 20, 35 for 2j = 1..5.  Cross-check on
    `witten_contributes`: "2j = 1 mod 4" must agree with "T(j) odd" on every
    isospin tested, or one of the two forms is mis-stated.
    """
    j = Fraction(two_j, 2)
    return Fraction(2, 3) * j * (j + 1) * (2 * j + 1)


# ==========================================================================
# W1 — the model's own SU(2)_L content
# ==========================================================================
def su2L_doublet_content(n_c: int,
                         include_lepton_doublet: bool = True,
                         vector_like_su2: bool = False,
                         quark_colour_rep: str = "fundamental"
                         ) -> Dict[str, Any]:
    """The Weyl SU(2)_L doublets the model carries, per generation.

    From the content F279/F293's six-row system is written on:

        Q_L : (R_colour, 2)  -> dim R_colour doublets
        L_L : (1,        2)  -> 1  doublet
        u_R, d_R, e_R, nu_R : SU(2) singlets -> 0

    `quark_colour_rep` exists so premise (iv) can be broken: the count -- and
    with it the parity, and with it the answer -- depends on the quark's colour
    representation, and pretending otherwise would be the overclaim a referee
    finds first.

    The Higgs-free mass-step carrier phi is a BOSON and contributes nothing to
    a fermionic mod-2 index whatever its SU(2) transformation.  That is a
    statement about the INDEX; it does not mean a bosonic sector could never
    participate in anomaly matching against a 5d SPT.
    """
    quark_mult = COLOUR_REPS[quark_colour_rep](int(n_c))
    fields = [("Q_L", quark_mult, 1),
              ("L_L", 1 if include_lepton_doublet else 0, 1),
              ("u_R", 0, 0), ("d_R", 0, 0), ("e_R", 0, 0), ("nu_R", 0, 0)]
    per_gen = sum(mult for _n, mult, iso in fields if iso)
    if vector_like_su2:
        per_gen *= 2                     # a right-handed partner for each
    return {
        "n_c": int(n_c),
        "quark_colour_rep": quark_colour_rep,
        "fields": [(nm, int(mult)) for nm, mult, iso in fields if iso],
        "doublets_per_generation": int(per_gen),
        "isospins_present_two_j": [1, 2],   # matter doublets, adjoint gauge
        "only_doublet_clause_used": True,
    }


def witten_scan(n_values: Sequence[int] = tuple(range(1, 13)),
                n_gen: int = N_GEN_MODEL,
                include_lepton_doublet: bool = True,
                vector_like_su2: bool = False,
                doubler_multiplicity: int = 1,
                quark_colour_rep: str = "fundamental",
                per_generation: bool = False) -> Dict[str, Any]:
    """The parity, in both available readings.

    `per_generation=False` (default, conservative): the obstruction is a
    condition on the TOTAL content, D = f * n_gen * D_gen.  It constrains N_c
    only when f * n_gen is odd -- premise (i).

    `per_generation=True` (Baer & Wiese 2001): impose cancellation separately
    for each generation, D_gen even.  Stronger -- no generation count needed --
    at the cost of assuming each generation must be independently consistent.
    Recorded because it is the form the prior art actually proves, and because
    it retires premise (i) for anyone willing to grant it.
    """
    rows = []
    f = int(doubler_multiplicity)
    for n in n_values:
        d = su2L_doublet_content(n, include_lepton_doublet, vector_like_su2,
                                 quark_colour_rep)["doublets_per_generation"]
        total = f * d if per_generation else f * n_gen * d
        rows.append({"N_c": int(n),
                     "doublets_per_generation": int(d),
                     "counted": int(total),
                     "z2_invariant": int(total % 2),
                     "consistent": bool(total % 2 == 0)})
    allowed = [r["N_c"] for r in rows if r["consistent"]]
    bites = bool((f if per_generation else f * n_gen) % 2 == 1)
    return {
        "rows": rows,
        "n_gen": int(n_gen),
        "per_generation": bool(per_generation),
        "doubler_multiplicity": f,
        "allowed": allowed,
        "excluded": [r["N_c"] for r in rows if not r["consistent"]],
        "constraint_bites": bites,
        "allowed_are_exactly_the_odd": bool(
            allowed == [n for n in n_values if n % 2 == 1]),
    }


def colour_own_z2_at_n2(n_gen: int = N_GEN_MODEL) -> Dict[str, Any]:
    """If COLOUR were SU(2), would colour's OWN Z_2 anomaly exclude it?  No.

    Counting Weyl fermions in the colour doublet, all written left-handed:
    Q_L supplies 2 (one per weak component); (u_R)^c and (d_R)^c supply 1 each
    -- conjugating a Weyl field in a pseudoreal rep is count-preserving, since
    2bar = 2.  Four per generation, hence even at any n_gen.

    WHAT THIS DOES AND DOES NOT SHOW.  It shows the exclusion of N_c = 2 does
    not run through colour's own anomaly, so the argument is not circular in
    THAT way.  It does NOT show the lower constraint is free of colour-sector
    input: premise (iv) is a colour fact and the parity consumes it.  What the
    parity does not consume is the epsilon-singlet's index count -- the fact
    F317 sec 6 and F318 sec D share.
    """
    per_gen = 2 + 1 + 1
    return {"colour_doublets_per_generation": per_gen,
            "total": int(n_gen * per_gen),
            "z2_invariant": int((n_gen * per_gen) % 2),
            "colour_own_anomaly_satisfied": bool((n_gen * per_gen) % 2 == 0),
            "does_not_show": ("that the lower constraint is colour-input-free; "
                              "premise (iv) is a colour fact and is consumed")}


def rep_sensitivity(n_max: int = 12, n_gen: int = N_GEN_MODEL
                    ) -> Dict[str, Any]:
    """Premise (iv), measured: what the bracket returns for each quark colour
    representation.  The answer is a function of the assumed content, and this
    is where a reader sees how much of a function.
    """
    support = set(c7_identity_support()["support"])
    out = {}
    for rep in COLOUR_REPS:
        w = witten_scan(tuple(range(1, n_max + 1)), n_gen,
                        quark_colour_rep=rep)
        out[rep] = sorted(set(w["allowed"]) & support)
    return {"bracket_by_quark_rep": out,
            "fundamental_gives_three": bool(out["fundamental"] == [3]),
            "inverts_in_adjoint": bool(out["adjoint"] == [2]),
            "note": ("the bit's sign is set by the assumed multiplet content; "
                     "that is premise (iv), and it is empirically fixed")}


# ==========================================================================
# Y1 — the same constraint, read locally
# ==========================================================================
def local_u2_quantisation() -> Dict[str, Any]:
    """If the true electroweak factor is U(2) -- hypercharge quantised so the
    Z_2 quotient acts -- then Davighi/Gripaios/Lohitsiri's rule q = 2j (mod 2)
    makes "every doublet carries odd charge" a LOCAL condition, and the Witten
    anomaly is replaced by it (1910.11277, 2001.07731).

    On this model's own nullspace y_Q = 1 and y_L = -N_c, so the rule reads:
    y_Q odd (always) and y_L odd (iff N_c odd).  Same constraint, different
    mechanism -- which is why the conclusion survives without the tree having
    to settle whether its global gauge group carries the quotient.
    """
    ns = hypercharge_nullspace_symbolic(nc_values=(2, 3, 4, 5))
    ratios = ns["ratios_normalised_to_yQ"]
    probe = (1, 2, 3, 4, 5, 6, 7)
    rows = [{"N_c": n, "y_Q": 1, "y_L": -n,
             "all_doublets_odd": bool(1 % 2 == 1 and (-n) % 2 == 1)}
            for n in probe]
    allowed = [r["N_c"] for r in rows if r["all_doublets_odd"]]
    return {"imported_ratios": ratios,
            "y_L_is_minus_Nc": bool(ratios is not None
                                    and ratios[3] == "-N_c"),
            "rows": rows,
            "allowed": allowed,
            "agrees_with_global_reading": bool(
                allowed == [n for n in probe if n % 2 == 1])}


# ==========================================================================
# W4 — this is not a re-attack of F293's R1
# ==========================================================================
def local_system_is_blind(n_values: Sequence[int] = (1, 2, 3, 4, 5, 7)
                          ) -> Dict[str, Any]:
    """F293 R1 closed local anomaly CANCELLATION as a selector on N_c.  Neither
    reading of the parity lives in that system: the global one is a mod-2
    obstruction, and the local U(2) one is a QUANTISATION condition on charges,
    not an anomaly-cancellation equation.  F293's six rows contain neither.

    Measured rather than argued: the imported system has nullspace dimension 1
    at every N_c and its gravitational and cubic anomalies vanish identically
    in N_c, while the Z_2 invariant alternates.
    """
    ns = hypercharge_nullspace_symbolic(nc_values=tuple(n_values))
    z2 = [{"N_c": int(n),
           "z2_invariant": int((N_GEN_MODEL * (int(n) + 1)) % 2)}
          for n in n_values]
    return {
        "imported_from": "derive_ncolour.hypercharge_nullspace_symbolic",
        "nullspace_dim_one_for_every_Nc": bool(ns["dim_one_for_every_Nc"]),
        "grav_identically_zero": bool(ns["grav_identically_zero"]),
        "cubic_identically_zero": bool(ns["cubic_identically_zero"]),
        "ratios_normalised_to_yQ": ns["ratios_normalised_to_yQ"],
        "z2_by_Nc": z2,
        "local_blind_global_not": bool(ns["dim_one_for_every_Nc"]
                                       and len({r["z2_invariant"]
                                                for r in z2}) == 2),
        "scope": ("F293's rows are anomaly-CANCELLATION rows; the U(2) "
                  "quantisation condition of Y1 is not one of them either"),
    }


# ==========================================================================
# U1 — F298's constraint, imported
# ==========================================================================
def _c7_exists_on_ladder(n_int: int, g2: Fraction = Fraction(1, 4),
                         empty_tower_passes: bool = False) -> bool:
    """F298's criterion on the imported `antisymmetric_ladder`.

    `empty_tower_passes` is the convention switch, exposed because it decides
    the N = 1 edge on its own.  Read "level-independent" as "a unique chi is
    DETERMINED" (default, False) and the empty tower at N = 1 fails.  Read it
    as "no two levels disagree" (True) and N = 1 passes vacuously and the
    bracket returns {1, 3}.  Nothing in the mathematics chooses; premise (ii)
    chooses -- chi must be determined because the model has a colour coupling.
    The N = 1 exclusion is therefore a RESTATEMENT of premise (ii), not an
    independent leg, and this flag is where that is measured instead of
    admitted in prose.
    """
    chis = {Fraction(s2, 1) / (4 * g2 * c2)
            for _k, c2, s2 in antisymmetric_ladder(n_int) if s2}
    if not chis:
        return bool(empty_tower_passes)
    return len(chis) == 1


def mixed_symmetry_breaks_n3(g2: Fraction = Fraction(1, 4)) -> Dict[str, Any]:
    """The direction of F298's truncation that threatens N = 3, measured.

    The k-string tower is not the full link Hilbert space; the plaquette
    operator also produces mixed-symmetry irreps, and following them is what
    F110 deferred.  The usual worry is that they might restore
    level-independence at N >= 4.  The unusual one -- and the one that matters
    for a finding leaning on the support {2,3} -- is that they break it at
    N = 3: the sextet (2,0) carries N-ality 2, so the model's own rotor rule
    assigns it s^2 = 1 while its Casimir is 10/3.
    """
    c2_6 = su_n_casimir([2], 3)
    s2_6 = zn_symmetric_residue_sq(2, 3)
    chi_6 = Fraction(s2_6, 1) / (4 * g2 * c2_6)
    chi_tower = 1 / casimir_fundamental(3)
    return {"irrep": "sextet (2,0) of SU(3)",
            "C_2": str(c2_6), "N_ality": 2, "s_squared": s2_6,
            "chi_sextet": str(chi_6), "chi_kstring_tower": str(chi_tower),
            "breaks_level_independence_at_N3": bool(chi_6 != chi_tower),
            "consequence": ("the support {2,3} is a property of the k-string "
                            "truncation F110 deferred, not yet of the full "
                            "link Hilbert space")}


def c7_identity_support(n_max: int = 9, scan_from: int = 1,
                        empty_tower_passes: bool = False) -> Dict[str, Any]:
    """Where the model's C7 identity exists.  F298 scanned N = 2..7 and
    reported "N <= 3"; scanned from N = 1 the criterion also fails there,
    because `antisymmetric_ladder(1)` is empty.  Support: {2, 3}.

    Two honesties carried in the returned dict rather than in prose:
      * `n1_is_convention` -- flipping `empty_tower_passes` moves the support
        to {1,2,3}, so the lower edge is premise (ii) in the ladder's
        vocabulary, not an independent exclusion.
      * `n2_passes_vacuously` -- at N = 2 the tower has ONE level, so nothing
        is matched.  Over the whole scan the criterion has exactly one
        non-trivial pass, and it is N = 3.

    The criterion is re-evaluated here rather than calling F298's entry point
    at N = 1, because `c7_against_casimir_ladder` also runs its symmetric
    CONTROL tower, whose C_2([k], 1) = 0 -- it raises ZeroDivisionError there.
    Agreement with that entry point wherever both are defined is asserted, not
    assumed.
    """
    ns = tuple(range(scan_from, n_max + 1))
    support = [int(n) for n in ns
               if _c7_exists_on_ladder(n, empty_tower_passes=empty_tower_passes)]
    alt = [int(n) for n in ns
           if _c7_exists_on_ladder(n, empty_tower_passes=not empty_tower_passes)]

    ns_f298 = tuple(n for n in ns if n >= 2)
    f298 = c7_against_casimir_ladder(n_values=ns_f298) if ns_f298 else None
    agrees = (f298 is None
              or f298["N_with_identity"] == [n for n in support if n >= 2])

    return {
        "imported_from": "casimir_ladder.antisymmetric_ladder / su_n_casimir",
        "scanned": list(ns),
        "tower_sizes": {int(n): len(antisymmetric_ladder(n)) for n in ns},
        "support": support,
        "support_under_other_convention": alt,
        "n1_is_convention": bool(support != alt),
        "n2_passes_vacuously": bool(len(antisymmetric_ladder(2)) == 1),
        "one_tested": bool(1 in ns),
        "four_tested": bool(any(n >= 4 for n in ns)),
        "agrees_with_F298_entry_point_where_defined": bool(agrees),
        "support_is_two_three": bool(support == [2, 3]
                                     and 1 in ns
                                     and any(n >= 4 for n in ns)
                                     and agrees),
        "C_F_check": {int(n): str(su_n_casimir([1], n)) for n in ns},
    }


# ==========================================================================
# B1 — the bracket
# ==========================================================================
def bracket(n_max: int = 12, n_gen: int = N_GEN_MODEL,
            include_lepton_doublet: bool = True,
            vector_like_su2: bool = False,
            scan_from: int = 1,
            c7_n_max: int = 9,
            doubler_multiplicity: int = 1,
            quark_colour_rep: str = "fundamental",
            per_generation: bool = False,
            empty_tower_passes: bool = False) -> Dict[str, Any]:
    """{N_c odd} intersect {C7 support} over the scan."""
    ns = tuple(range(scan_from, n_max + 1))
    w = witten_scan(ns, n_gen, include_lepton_doublet, vector_like_su2,
                    doubler_multiplicity, quark_colour_rep, per_generation)
    c7 = c7_identity_support(n_max=c7_n_max, scan_from=scan_from,
                             empty_tower_passes=empty_tower_passes)
    support = set(c7["support"])
    rows = [{"N_c": r["N_c"], "z2_ok": r["consistent"],
             "c7_exists": bool(r["N_c"] in support),
             "allowed": bool(r["consistent"] and r["N_c"] in support)}
            for r in w["rows"]]
    allowed = [r["N_c"] for r in rows if r["allowed"]]
    return {
        "rows": rows,
        "scanned": list(ns),
        "allowed": allowed,
        "unique": bool(len(allowed) == 1),
        "closed_and_three": bool(allowed == [3] and 1 in ns and n_max >= 4),
        "premises": [
            "(i) n_gen odd (F75) -- or per-generation consistency (Baer-Wiese)",
            "(ii) the colour sector exists (F318's residual); this is what "
            "excludes N=1, restated in the ladder's vocabulary",
            "(iii) the rotor modulus is the centre Z_{N_c} (F97/F99)",
            "(iv) quarks in the defining rep with multiplicity N_c",
            "(v) one colour-singlet lepton doublet per generation, "
            "right-handers SU(2) singlets (posited in derive_ncolour)",
            "(vi) no fermion doubling, f = 1 (CL020 is `narrowed`)",
        ],
        # NOT checks: author declarations, reported and deliberately kept out
        # of the pass count.  A flag that cannot go red has no business
        # occupying a slot in an n/n.
        "declarations": {
            "consumes_measured_number": False,
            "consumes_three_constituent_baryon": False,
            "depends_on_X1_branch": False,
            "consumes_empirical_input": True,
        },
    }


def falsifiability_counterfactual(true_n_c: Sequence[int] = (4, 5, 6, 7)
                                  ) -> Dict[str, Any]:
    """If the world had N_c >= 4 the bracket returns the EMPTY set: the model
    would be falsified, and F144's g_s derivation would lose its object with
    it.  Recorded because an argument that cannot fail is not an argument.
    """
    support = set(c7_identity_support()["support"])
    w = witten_scan(tuple(range(1, 13)))
    ok = set(w["allowed"]) & support
    return {"bracket": sorted(ok),
            "would_be_empty_at": [int(n) for n in true_n_c if n not in ok],
            "model_falsified_if_true_Nc_ge_4": bool(
                all(n not in ok for n in true_n_c))}


# ==========================================================================
# P1 — the corollary: the constituent count IS N_c
# ==========================================================================
def _sort_sign(seq: Sequence[int]) -> int:
    order = sorted(range(len(seq)), key=lambda t: seq[t])
    seen = [False] * len(seq)
    par = 0
    for start in range(len(seq)):
        if seen[start]:
            continue
        length, x = 0, start
        while not seen[x]:
            seen[x] = True
            x = order[x]
            length += 1
        par += length - 1
    return (-1) ** par


def lambda_n_singlets(n_int: int, n_constituents: int) -> Tuple[int, int]:
    """(dim Lambda^n(C^N), dim of its SU(N)-invariant subspace), exact over Q,
    as the joint kernel of the su(N) generators on the wedge basis.

    This is a binomial coefficient and the answer is the epsilon tensor; it is
    computed rather than quoted only so F317 sec 6's float/SVD route has an
    exact partner to be checked against (P2).  Nobody should read it as a
    measurement.
    """
    N, n = int(n_int), int(n_constituents)
    if n > N or n < 1:
        return (0, 0)
    basis = list(combinations(range(N), n))
    idx = {b: i for i, b in enumerate(basis)}
    dim = len(basis)
    blocks: List[sp.Matrix] = []
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            M = sp.zeros(dim, dim)
            for b in basis:
                if j in b and i not in b:
                    nb = list(b)
                    nb[b.index(j)] = i
                    M[idx[tuple(sorted(nb))], idx[b]] += _sort_sign(nb)
            blocks.append(M)
    for a in range(N - 1):
        M = sp.zeros(dim, dim)
        for b in basis:
            M[idx[b], idx[b]] += (1 if a in b else 0) - (1 if a + 1 in b else 0)
        blocks.append(M)
    return dim, len(sp.Matrix.vstack(*blocks).nullspace())


def minimal_all_quark_singlet(n_int: int, n_max: int = 0) -> Dict[str, Any]:
    top = n_max or (n_int + 2)
    rows = []
    for n in range(1, top + 1):
        d, s = lambda_n_singlets(n_int, n)
        rows.append({"n_constituents": n, "dim_lambda_n": d, "singlets": s})
    hits = [r["n_constituents"] for r in rows if r["singlets"] == 1]
    return {"n_int": int(n_int), "rows": rows, "n_with_singlet": hits,
            "minimal": hits[0] if hits else None,
            "unique": bool(len(hits) == 1)}


def three_is_a_corollary(n_int: int = 3) -> Dict[str, Any]:
    """With N_c fixed independently, the minimal totally antisymmetric all-quark
    singlet has N_c constituents.  A COROLLARY of premise (iv), not a
    discovery: given quarks in the defining rep and the antisymmetric singlet,
    the constituent count IS N_c.

    Its value is the DIRECTION of the equivalence.  F317 sec 6's "baryons have
    three constituents" was never information about the model independent of
    N_c -- which is why discharging it costs nothing, and why F318's warning
    that the two findings double-count it loses its object.
    """
    m = minimal_all_quark_singlet(n_int)
    return {"n_int": int(n_int),
            "minimal_constituents": m["minimal"],
            "unique": m["unique"],
            "equals_n_int": bool(m["minimal"] == n_int),
            "rows": m["rows"],
            "status": "corollary of premise (iv) + antisymmetric singlet"}


# ==========================================================================
# the gate entry
# ==========================================================================
def check_ncolour_bracket(n_generations: int = N_GEN_MODEL,
                          include_lepton_doublet: bool = True,
                          vector_like_su2: bool = False,
                          quark_colour_rep: str = "fundamental",
                          per_generation: bool = False,
                          n_max: int = 12,
                          c7_n_max: int = 9,
                          scan_from: int = 1,
                          doubler_multiplicity: int = 1,
                          empty_tower_passes: bool = False,
                          cross_check_f317: bool = True) -> Dict[str, Any]:
    """The F324 gate.

    Declared controls (the record carries the MEASURED red sets):

    ``--param n_generations=2``               premise (i), made to fire.
    ``--param include_lepton_doublet=false``  premise (v): the parity INVERTS.
    ``--param vector_like_su2=true``          F27's chirality is load-bearing.
    ``--param quark_colour_rep=adjoint``      premise (iv): the bracket returns
        {2}.  The control that shows the lower constraint is NOT free of
        colour-sector input.
    ``--param c7_n_max=3``                    F298's own idiom: a scan that
        never tests N >= 4 cannot claim to have excluded it.
    ``--param scan_from=2``                   an untested edge is not an
        excluded one.
    ``--param doubler_multiplicity=2``        premise (vi), CL020's caveat.
    ``--param empty_tower_passes=true``       premise (ii): read the criterion
        as "no two levels disagree" and N = 1 passes vacuously, so the bracket
        returns {1,3}.  The N = 1 edge is a convention fixed by the premise,
        and this is where that is measured rather than merely admitted.
    """
    n_gen = int(n_generations)
    checks: List[Tuple[str, bool, Any]] = []

    rule = {tj: witten_contributes(tj) for tj in (1, 2, 3, 4, 5)}
    dynk = {tj: dynkin_index_normalised(tj) for tj in (1, 2, 3, 4, 5)}
    dynk_odd = {tj: bool(v.denominator == 1 and v.numerator % 2 == 1)
                for tj, v in dynk.items()}
    content = su2L_doublet_content(3, include_lepton_doublet, vector_like_su2,
                                   quark_colour_rep)
    checks.append((
        "G0 the mod-2 index rule (Witten 1982, QUOTED): 2j = 1 mod 4 agrees "
        "with the independent 'Dynkin index odd' form on every isospin "
        "tested, and the model's content exercises only the 2j = 1 clause",
        (rule == {1: True, 2: False, 3: False, 4: False, 5: True}
         and dynk_odd == rule
         and content["only_doublet_clause_used"]),
        {"rule": rule, "T_j": {k: str(v) for k, v in dynk.items()}}))

    ns_sym = hypercharge_nullspace_symbolic(nc_values=(2, 3, 4))
    ratios = ns_sym["ratios_normalised_to_yQ"]
    checks.append((
        "W1 the model's content is N_c quark doublets + 1 lepton doublet per "
        "generation -- the y_L = -N_c y_Q row, imported from derive_ncolour. "
        "NOT param-adaptive, so the content controls must break it",
        (content["doublets_per_generation"] == 3 + 1
         and ratios is not None and ratios[3] == "-N_c"),
        {"content": content["fields"], "y_ratios": ratios}))

    w = witten_scan(tuple(range(scan_from, n_max + 1)), n_gen,
                    include_lepton_doublet, vector_like_su2,
                    doubler_multiplicity, quark_colour_rep, per_generation)
    checks.append((
        "W2 the Z_2 parity: doublet count even <=> N_c ODD.  Exact over Z. "
        "PRIOR ART (Baer & Wiese 2001); what is new is the derived content it "
        "is evaluated on and the pairing in B1",
        bool(w["constraint_bites"] and w["allowed_are_exactly_the_odd"]),
        {"allowed": w["allowed"], "n_gen": n_gen,
         "per_generation": per_generation}))
    checks.append((
        "W2b ... and it is not vacuous: it excludes a non-empty set, exactly "
        "the even N_c",
        bool(len(w["excluded"]) > 0), w["excluded"]))

    own = colour_own_z2_at_n2(n_gen)
    checks.append((
        "W3 colour's OWN Z_2 anomaly at N_c = 2 is SATISFIED (4 doublets per "
        "generation; pseudoreal conjugation is count-preserving), so N_c = 2 "
        "does not fall to a colour anomaly.  This does NOT show the "
        "constraint is colour-input-free -- premise (iv) is consumed",
        bool(own["colour_own_anomaly_satisfied"]), own["total"]))

    rs = rep_sensitivity(n_max, n_gen)
    checks.append((
        "W3b premise (iv), measured: the bracket is a FUNCTION of the quark's "
        "colour rep -- fundamental {3}, adjoint {2}, two-index-antisym {2,3}, "
        "symmetric {2}.  The bit's sign is set by an empirically fixed content",
        bool(rs["fundamental_gives_three"] and rs["inverts_in_adjoint"]),
        rs["bracket_by_quark_rep"]))

    y1 = local_u2_quantisation()
    checks.append((
        "Y1 the SAME constraint arrives LOCALLY if the electroweak factor is "
        "U(2): the rule q = 2j mod 2 on the model's own y_L = -N_c reads N_c "
        "odd.  The conclusion does not wait on the global group structure",
        bool(y1["y_L_is_minus_Nc"] and y1["agrees_with_global_reading"]),
        y1["allowed"]))

    blind = local_system_is_blind()
    checks.append((
        "W4 F293's six ANOMALY-CANCELLATION rows contain neither reading: "
        "nullspace dim 1 at every N_c, grav and cubic identically zero in "
        "N_c, while the Z_2 invariant alternates.  R1 stays closed",
        bool(blind["local_blind_global_not"]),
        {"z2": [r["z2_invariant"] for r in blind["z2_by_Nc"]]}))

    sup = c7_identity_support(n_max=c7_n_max, scan_from=scan_from,
                              empty_tower_passes=empty_tower_passes)
    checks.append((
        "U1 the C7 identity's support is {2,3} -- F298's criterion imported "
        "and scanned down to N = 1, where the tower is EMPTY",
        bool(sup["support_is_two_three"]),
        {"support": sup["support"], "tower_sizes": sup["tower_sizes"]}))
    checks.append((
        "U1b ... and both edges are declared for what they are: N = 1 fails by "
        "CONVENTION (premise (ii); the other reading gives {1,2,3}) and N = 2 "
        "passes VACUOUSLY (one level).  Exactly one non-trivial pass, at N = 3",
        bool(sup["n1_is_convention"] and sup["n2_passes_vacuously"]),
        {"other_convention": sup["support_under_other_convention"]}))

    mix = mixed_symmetry_breaks_n3()
    checks.append((
        "U1c ... and the truncation cuts BOTH ways: under the model's own "
        "rotor rule the sextet (2,0) gives chi = 3/10 against the k-string "
        "tower's 3/4, so level-independence fails at N = 3 too outside the "
        "sector F110 deferred",
        bool(mix["breaks_level_independence_at_N3"]),
        {"chi_sextet": mix["chi_sextet"],
         "chi_tower": mix["chi_kstring_tower"]}))

    br = bracket(n_max=n_max, n_gen=n_gen,
                 include_lepton_doublet=include_lepton_doublet,
                 vector_like_su2=vector_like_su2, scan_from=scan_from,
                 c7_n_max=c7_n_max, doubler_multiplicity=doubler_multiplicity,
                 quark_colour_rep=quark_colour_rep,
                 per_generation=per_generation,
                 empty_tower_passes=empty_tower_passes)
    checks.append((
        "B1 {Z_2-consistent} AND {C7 support} = {3}, over the scanned range "
        "with both edges actually scanned",
        bool(br["closed_and_three"]),
        {"allowed": br["allowed"],
         "scanned": [br["scanned"][0], br["scanned"][-1]]}))

    fc = falsifiability_counterfactual()
    checks.append((
        "B1c the argument CAN fail: at a true N_c >= 4 the bracket returns the "
        "EMPTY set, falsifying the model and taking F144's g_s with it",
        bool(fc["model_falsified_if_true_Nc_ge_4"]), fc["would_be_empty_at"]))

    rev = three_is_a_corollary(3)
    checks.append((
        "P1 at N_c = 3 the minimal totally antisymmetric all-quark singlet has "
        "exactly 3 constituents -- a COROLLARY of premise (iv), not a "
        "discovery.  Its content is the DIRECTION: F317 sec 6's input was "
        "never independent of N_c, so discharging it costs nothing",
        bool(rev["equals_n_int"] and rev["unique"]), rev["rows"]))

    if cross_check_f317:
        from casim.engine.gauge.derive_su3_structure import multiplicity_squeeze
        sq = multiplicity_squeeze()
        exact_col = [(N, lambda_n_singlets(N, 3)[1]) for N in (2, 3, 4, 5, 6)]
        checks.append((
            "P2 the exact-over-Q kernel AGREES with F317 sec 6's float/SVD "
            "route on the n = 3 column -- agreement between implementations, "
            "explicitly NOT independent confirmation",
            bool(all(int(r["singlet_dim"]) == s
                     for r, (N, s) in zip(sq["rows"], exact_col))
                 and sq["unique_and_three"]), exact_col))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            # reported, NOT counted
            "declarations": br["declarations"],
            "premises": br["premises"],
            "params": {"n_generations": n_gen,
                       "include_lepton_doublet": include_lepton_doublet,
                       "vector_like_su2": vector_like_su2,
                       "quark_colour_rep": quark_colour_rep,
                       "per_generation": per_generation,
                       "n_max": n_max, "c7_n_max": c7_n_max,
                       "scan_from": scan_from,
                       "doubler_multiplicity": doubler_multiplicity,
                       "empty_tower_passes": empty_tower_passes,
                       "cross_check_f317": cross_check_f317},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    br = bracket()
    return {
        "N_c": br["allowed"],
        "lower_constraint": "Witten Z_2 (Baer & Wiese 2001) on the DERIVED "
                            "SU(2)_L and content => N_c odd; the same "
                            "constraint arrives locally under a U(2) embedding",
        "upper_constraint": "F298: C7 support = {2,3}, on the k-string "
                            "truncation",
        "incremental_content_over_F298": "one bit",
        "premises": br["premises"],
        "three_constituent_baryon": "corollary, not input",
        "X1_branch_independent": True,
        "falsifiable": "the bracket is EMPTY at a true N_c >= 4",
    }
