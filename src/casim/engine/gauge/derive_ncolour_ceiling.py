#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derive_ncolour_ceiling.py — B10 after F325: the odd-N_c bracket does not
narrow further, checked against one new in-tree candidate route and against
the general (non-lattice, arbitrary-N_c) chiral-gauge-theory literature
====================================================================

2026-08-31

WHERE THIS PICKS UP
--------------------

F325 (2026-08-18) resolved the X1 colour-normalisation fork and, as a
consequence, WITHDREW F324's upper constraint: the C7 identity's "well-defined
only for N_c <= 3" (CN19) was a property of a mixed-operator matching, not a
selector.  What survives is F324's LOWER leg only -- the pi_4(SU(2)) = Z_2
Witten global anomaly on the model's own derived chiral SU(2)_L (prior art,
Baer & Wiese 2001) -- so B10 closes on

    {N_c odd, N_c != 1}  =  {3, 5, 7, 9, 11, ...}

with N_c = 3 favoured by F293 Sec 4's 28.3-decade confinement-scale lever and
by nothing structural.  This module is what this session's attack on that
residual produced: not a closure, and it is stated that plainly before
anything below.  Three things are new here, none of them a derivation of 3:

  G0  the current bracket recomputed directly from the surviving lower leg
      (`witten_scan`, unmodified, imported from F324's own module) rather
      than quoted from the ledger -- a regression/consistency check that the
      withdrawal is correctly reflected outside the finding's own prose.
  G1  a candidate route nobody in this tree had checked and closed: does the
      COLOUR gauge group SU(N_c) carry an analogous pi_4 global anomaly of
      its own (as opposed to the already-used SU(2)_L route)?  No -- pi_4(SU
      (N)) = 0 identically for every N >= 3 (Bott 1959; standard homotopy-of-
      Lie-groups table, e.g. Mimura & Toda, "Topology of Lie Groups I, II").
      This is a CITED mathematical fact, not computed in this tree, and it
      closes a previously-unexamined candidate rather than leaving it silent.
  G2  an exact, elementary dimension count: the model's own per-generation
      Weyl fermion content (N_c quark doublets, 2*N_c right-handed quark
      singlets, one lepton doublet, e_R, and a right-handed neutrino per
      F47's Majorana step) totals EXACTLY 4(N_c+1), which is 16 precisely at
      N_c = 3.  Exact over Z; not a topological claim by itself.
  G3  FLAGGED, NOT VERIFIED, NOT CLAIMED AS A RESULT.  If the mod-16
      Pin+/Dai-Freed anomaly of one Majorana-completed Standard-Model
      generation (Garcia-Etxebarria & Montero, "Dai-Freed anomalies in
      particle physics," 1808.00009; Wang, "Anomaly and Cobordism
      Constraints Beyond Grand Unification: Energy Hierarchy," 2008.06499 --
      the paper that actually defines X = 5(B-L) - 4Y; NOT 1810.00844,
      "A New SU(2) Anomaly," which is unrelated to the Standard Model and
      was misattributed here in the finding's first draft, corrected on
      review) generalises to the bare condition "the total Weyl-fermion
      count, summed over generations, is a multiple of 16" for this model's
      general-N_c content, the arithmetic consequence (n_gen odd, from F75)
      is N_c = 3 (mod 4) -- narrowing the odd bracket to {3, 7, 11, 15, ...}
      and excluding {5, 9, 13, ...}.  This is reported as an exact arithmetic
      consequence of a CITED BUT UNVERIFIED premise: the actual anomaly
      invariant is built from a specific discrete symmetry generator
      X = 5(B-L) - 4Y whose own N_c-dependence has not been recomputed for
      this model's nullspace in this session, and the "16" in the cited
      papers is derived for the N_c = 3 content specifically, not shown there
      to generalise as a bare fermion count for other N_c.  Recorded as a
      flagged coincidence in the sense F300 Sec 5 uses the term for its own
      2*pi*sqrt(3) reciprocal-lattice observation: kept OUT of the pass count
      (see `declarations`), and named as the single most concrete next step
      for a session with the primary references in hand.
  G4  (declaration, not a check -- see below) an external cross-check against
      the GENERAL (non-lattice, arbitrary-N_c) chiral-gauge-theory literature,
      2026-08-31: Baer & Wiese's own paper states that low-energy pion physics
      cannot distinguish N_c = 3 from 5, 7, ...; Tanizaki (JHEP08(2018)171)
      derives 't Hooft anomaly matching for GENERIC N_c with no N_c=3
      discrimination; and hep-ph/0009242 shows the textbook pi0 -> 2 gamma
      argument does not constrain N_c at all once colour-dependent quark
      charges are used correctly.  So the residual this session set out to
      close is not a defect of this lattice/CA construction -- it reproduces
      exactly in the general literature, where N_c is likewise pinned only by
      measured observables (the Drell ratio, hadronic decay rates; the
      model's own analogue is F293 Sec 4's confinement-scale lever).

WHAT THIS DOES NOT DO
----------------------

It does not narrow the bracket.  G3's arithmetic is exact but its physical
premise is unverified; it is excluded from the pass count for exactly that
reason, mirroring `derive_ncolour_bracket.bracket()`'s own `declarations`
convention (a flag that cannot go red has no business occupying a slot in an
n/n).  The bracket B10 carries after this module is unchanged from F325:

    {3, 5, 7, 9, 11, ...},  N_c = 3 favoured empirically, not structurally.

DO NOT RE-ATTACK from here: the anomaly-cancellation route (F293 R1, circular
-- Y_Q is not independently given in this model), the spatial-3 identification
(F293 R2, excluded by [C_3, lambda^a] != 0), the Z_3-centre route (F293 R3,
circular -- the centre is introduced AS SU(3)'s centre), F303's n*C_F=4
three-link-plaquette route (dead -- BCC nearest-neighbour hops cannot close a
3-hop loop, exhaustive over 8^3), or F325/CN19's withdrawn C7 upper bound.

Cross-references: F324 (the lower leg, `witten_scan` imported unmodified),
F325 (the withdrawal this module starts from), F293 (the three closed routes,
R1-R3), F298 (the withdrawn upper leg), F317 (Sec 10's "internal index is
still an input", untouched by anything here).
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

import sympy as sp

from casim.engine.gauge.derive_ncolour_bracket import N_GEN_MODEL, witten_scan

# ==========================================================================
# G1 -- pi_4(SU(N)), CITED, not computed.  Standard homotopy-of-Lie-groups
# fact (Bott 1959; tabulated e.g. Mimura & Toda, "Topology of Lie Groups I,
# II", Springer 1991).  |pi_4(SU(2))| = 2 (the group is Z_2, Witten's
# obstruction); pi_4(SU(N)) = 0 for every N >= 3.  SU(1) is the trivial group
# and carries no gauge field at all -- included only so the table is total
# over the scan range, with `carries_obstruction` correctly False there too.
# ==========================================================================
PI4_SUN_ORDER: Dict[int, int] = {n: (2 if n == 2 else 1) for n in range(1, 13)}


def colour_group_has_witten_obstruction(
    n_values: Sequence[int] = tuple(range(1, 11)),
    su3_pi4_order_override: int = None,
) -> Dict[str, Any]:
    """Does the COLOUR gauge group SU(N_c) itself carry a pi_4 global
    anomaly, independent of the already-used SU(2)_L route?

    `su3_pi4_order_override` exists only as a control: forcing a false claim
    at N_c = 3 (e.g. 2, pretending SU(3) carries the obstruction) must flip
    `only_n2_carries_it` to False, or this check is not reading the table.
    """
    table = dict(PI4_SUN_ORDER)
    if su3_pi4_order_override is not None:
        table[3] = int(su3_pi4_order_override)
    rows = [{"N_c": n, "pi4_order": table.get(n, 1),
             "carries_obstruction": table.get(n, 1) > 1}
            for n in n_values]
    only_n2 = all(r["carries_obstruction"] == (r["N_c"] == 2) for r in rows)
    return {
        "rows": rows,
        "only_n2_carries_it": bool(only_n2),
        "conclusion": (
            "no analogous global anomaly exists for the colour group at any "
            "N_c >= 3; pi_4(SU(N)) = 0 identically for N >= 3 (cited, "
            "standard fact -- not derived in this tree)."
        ),
    }


# ==========================================================================
# G2 -- the model's own per-generation Weyl fermion count.  Elementary
# dimension arithmetic on content already fixed by F27 (chirality), F47
# (the Majorana right-handed neutrino), and the F279/F293/F324 nullspace
# (N_c quark doublets, one lepton doublet, right-handers SU(2) singlets).
# ==========================================================================
def weyl_fermion_count_per_generation(n_c: int,
                                      include_nu_r: bool = True
                                      ) -> Dict[str, Any]:
    Nc = sp.Integer(n_c)
    # Q_L: N_c colours x 2 weak components.  u_R, d_R: N_c each (colour
    # triplet, weak singlet).  L: 2 weak components, colour singlet.
    # e_R: 1.  nu_R: 1, if included (F47's Majorana step).
    total = 2 * Nc + Nc + Nc + 2 + 1 + (1 if include_nu_r else 0)
    closed_form = 4 * (Nc + 1) if include_nu_r else 4 * Nc + 3
    return {
        "N_c": int(n_c),
        "include_nu_r": bool(include_nu_r),
        "total": int(total),
        "closed_form": str(closed_form),
        "matches_closed_form": bool(sp.simplify(total - closed_form) == 0),
    }


# ==========================================================================
# G3 -- FLAGGED.  See module docstring.  The arithmetic is exact; the
# physical premise it is conditioned on is explicitly NOT verified here.
# ==========================================================================
def mod16_flagged_condition(n_c: int, n_gen: int,
                            assumed_anomaly_modulus: int = 16
                            ) -> Dict[str, Any]:
    Nc, ng, mod = sp.Integer(n_c), sp.Integer(n_gen), sp.Integer(
        assumed_anomaly_modulus)
    per_gen = 4 * (Nc + 1)
    total = ng * per_gen
    return {
        "N_c": int(n_c),
        "n_gen": int(n_gen),
        "assumed_anomaly_modulus": int(assumed_anomaly_modulus),
        "per_generation_weyl_count": int(per_gen),
        "total_weyl_count": int(total),
        "total_is_multiple_of_modulus": bool(total % mod == 0),
        "verified": False,
        "caveat": (
            "arithmetic consequence of a literature formula (Garcia-Etxebarria "
            "& Montero, Dai-Freed anomalies in particle physics, 1808.00009; "
            "Wang, Anomaly and Cobordism Constraints Beyond Grand Unification: "
            "Energy Hierarchy, 2008.06499) NOT re-derived for general N_c in "
            "this tree -- the actual Pin+ invariant is built from a discrete "
            "symmetry generator X = 5(B-L) - 4Y (defined in 2008.06499, not "
            "in 1810.00844 which was misattributed in this finding's first "
            "draft) whose own N_c-dependence has not been recomputed here. "
            "Flagged per F300's own coincidence convention (Sec 5, "
            "`reciprocal_cube_coincidence`), not claimed as a derivation."
        ),
    }


def mod16_scan(n_max: int = 15, n_gen: int = N_GEN_MODEL,
               assumed_anomaly_modulus: int = 16) -> Dict[str, Any]:
    """The would-be narrowing IF G3's premise were confirmed, reported for
    transparency and excluded from the pass count.  At modulus 16 the
    necessary condition on odd N_c is exactly N_c = 3 (mod 4)."""
    odd_ns = [n for n in range(1, n_max + 1) if n % 2 == 1 and n != 1]
    rows = [mod16_flagged_condition(n, n_gen, assumed_anomaly_modulus)
            for n in odd_ns]
    if_verified = [r["N_c"] for r in rows if r["total_is_multiple_of_modulus"]]
    return {
        "odd_bracket_scanned": odd_ns,
        "rows": rows,
        "if_g3_premise_confirmed_bracket": if_verified,
        "necessary_condition_is_Nc_mod4_eq_3": bool(
            assumed_anomaly_modulus == 16
            and if_verified == [n for n in odd_ns if n % 4 == 3]),
    }


# ==========================================================================
# G4 -- external literature cross-check.  A citation ledger, not a
# computation.  Kept in the module (rather than only in the finding's prose)
# so `casim index`/coverage tooling and any later session see it alongside
# the exact checks. Excerpts are this session's own paraphrase of fetched
# sources, flagged as such where not a direct quotation.
# ==========================================================================
def external_literature_check() -> Dict[str, Any]:
    return {
        "bar_wiese_2001": {
            "cite": "Baer & Wiese, Nucl. Phys. B609 (2001) 225, hep-ph/0105258",
            "finding": (
                "low-energy pion physics alone cannot determine whether "
                "N_c = 3, 5, 7, or any odd number; only high-energy "
                "observables (the Drell ratio) or eta -> pi+ pi- gamma can "
                "distinguish them experimentally. The paper's own N_c-odd "
                "argument (this tree's prior art for the surviving lower "
                "leg) is offered as the theoretical ceiling, not a stepping "
                "stone to N_c=3."
            ),
        },
        "tanizaki_2018": {
            "cite": "Tanizaki, JHEP08(2018)171",
            "finding": (
                "the discrete 't Hooft anomaly of massless QCD is derived "
                "for GENERIC N_c and N_f; its no-go theorem on exotic "
                "chiral-symmetry-breaking phases applies uniformly and does "
                "not distinguish N_c=3 from other values."
            ),
        },
        "colour_pi0_2000": {
            "cite": "hep-ph/0009242, 'On the number of colours in QCD'",
            "finding": (
                "the textbook pi0 -> 2 gamma argument for N_c=3 does not, "
                "in fact, constrain N_c at all once the correct colour-"
                "dependent quark charges are used."
            ),
        },
        "conclusion": (
            "the residual this session set out to close -- no known "
            "mechanism narrows an odd N_c beyond {3,5,7,...} short of a "
            "measured observable -- is not a defect specific to this "
            "lattice/CA construction. It reproduces exactly in the general "
            "(non-lattice, arbitrary-N_c) chiral gauge theory literature, "
            "where N_c is likewise pinned only by experiment."
        ),
    }


# ==========================================================================
# Gate
# ==========================================================================
def check_ncolour_ceiling(n_gen: int = N_GEN_MODEL, n_max: int = 10,
                          mod16_n_max: int = 15,
                          su3_pi4_order_override: int = None,
                          include_nu_r: bool = True,
                          assumed_anomaly_modulus: int = 16
                          ) -> Dict[str, Any]:
    """The F338 gate.

    Declared controls (the record carries the MEASURED red sets):

    ``--param su3_pi4_order_override=2``   G1: falsely claim SU(3) carries
        the pi_4 obstruction -- the check must catch that this contradicts
        "only N=2 carries it".
    ``--param include_nu_r=false``         G2: drop the right-handed
        neutrino -- the per-generation count at N_c=3 becomes 15, not 16.
    ``--param assumed_anomaly_modulus=8``  G3's own necessary-condition
        arithmetic, compared against a FIXED expectation (N_c = 3 mod 4) --
        a different modulus must turn this red.
    ``--param n_gen=2``                    G0 and G3: F324's premise (i)
        broken -- the surviving lower leg stops selecting odd N_c at all
        (reusing `witten_scan`'s own, already-tested, control), and G3's
        arithmetic also reddens because n_gen=2 is no longer coprime to the
        modulus, breaking the exact n = 3 (mod 4) reduction used at n_gen
        odd.
    """
    checks: List[Tuple[str, bool, Any]] = []

    # G0 -- the current bracket, recomputed from the surviving leg only.
    # witten_scan ALONE allows N_c=1 too (D_gen = N_c+1 = 2 is even for any
    # n_gen, so the Z_2 parity is vacuously satisfied there) -- the parity
    # leg never excluded N=1 by itself.  N_c != 1 is a SEPARATE, STILL-
    # STANDING premise: that a non-trivial colour sector exists at all
    # (F317 Sec 0 item (i), "the quark carries an internal index at all --
    # still an input"; F318's residual).  F324 Sec 3 U1b implemented that
    # premise's N=1 edge THROUGH the C7 ladder convention, but the premise
    # itself is prior to and independent of that implementation, and F325
    # withdrew only the C7 identity's UPPER-bound content, not this premise.
    # So N_c=1 is dropped here on that still-standing ground, explicitly NOT
    # via the withdrawn C7 apparatus.
    w = witten_scan(tuple(range(1, n_max + 1)), n_gen)
    odd_allowed = sorted(n for n in w["allowed"] if n != 1)
    expected = sorted(n for n in range(3, n_max + 1) if n % 2 == 1)
    checks.append((
        "G0 the CURRENT bracket is exactly the odd N_c > 1 over the scanned "
        "range: witten_scan's own odd-parity set (F324's module, imported "
        "unmodified -- the withdrawn C7 leg is NOT reintroduced), MINUS "
        "N_c=1, which is excluded by the separate, still-standing premise "
        "that a non-trivial colour sector exists at all (F317 Sec.0 item "
        "(i); F318's residual) rather than by the withdrawn C7 identity. "
        "Confirms F325's withdrawal is correctly reflected outside the "
        "finding's own prose",
        bool(w["constraint_bites"] and odd_allowed == expected),
        {"allowed": w["allowed"], "n_gen": n_gen}))

    g1 = colour_group_has_witten_obstruction(
        range(1, n_max + 1), su3_pi4_order_override)
    checks.append((
        "G1 the colour group SU(N_c) ITSELF carries no analogous pi_4 "
        "global anomaly at any N_c >= 3 -- pi_4(SU(N)) = 0 identically for "
        "N >= 3 (cited, standard homotopy-of-Lie-groups fact), so this "
        "distinct candidate route (as opposed to the SU(2)_L doublet route "
        "F324/F325 already use) is closed by citation rather than left "
        "untested",
        bool(g1["only_n2_carries_it"]), g1["rows"]))

    n3 = weyl_fermion_count_per_generation(3, include_nu_r)
    all_n = [weyl_fermion_count_per_generation(n, include_nu_r)
             for n in range(1, 8)]
    # Fixed expectation (16, NOT conditional on include_nu_r): the model's
    # own content DOES include a right-handed neutrino (F47's Majorana
    # step), so the control `include_nu_r=false` must be seen as breaking
    # this check (count drops to 15), not as silently re-deriving a
    # different-but-still-matching target.
    checks.append((
        "G2 the model's own per-generation Weyl fermion count is EXACTLY "
        "4(N_c+1) for every N_c (elementary dimension count, exact over Z), "
        "and equals 16 precisely at N_c=3 given the model's own content "
        "(F47's right-handed neutrino included)",
        bool(all(c["matches_closed_form"] for c in all_n)
             and n3["total"] == 16),
        n3))

    scan = mod16_scan(mod16_n_max, n_gen, assumed_anomaly_modulus)
    fixed_mod4_pattern = [n for n in scan["odd_bracket_scanned"] if n % 4 == 3]
    checks.append((
        "G3 FLAGGED ARITHMETIC, NOT A DERIVATION (mod16_flagged_condition's "
        "own `verified: False`/`caveat` fields carry the full disclosure): "
        "AT THE CITED MODULUS 16, the scan's necessary-condition arithmetic "
        "reproduces exactly N_c = 3 (mod 4) among odd N_c, i.e. "
        "{3,7,11,15,...}, excluding {5,9,13,...}. The comparison is against "
        "a FIXED expectation (n = 3 mod 4), so the control below (a "
        "different assumed modulus) is expected to -- and does -- turn this "
        "red, confirming the scan actually reads the modulus rather than "
        "returning a hard-coded set",
        bool(scan["if_g3_premise_confirmed_bracket"] == fixed_mod4_pattern),
        scan))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {
        "checks": rows,
        "passed": all(r["ok"] for r in rows),
        "n_pass": sum(1 for r in rows if r["ok"]),
        "n_total": len(rows),
        # NOT checks: G3's physical premise is unverified and G4 is a
        # citation ledger, neither of which can go red -- kept out of the
        # pass count, mirroring derive_ncolour_bracket.bracket()'s own
        # `declarations` convention.
        "declarations": {
            "g3_mod16_premise_verified": False,
            "closes_bracket_to_three": False,
            "bracket_unchanged_from_F325": True,
            "external_literature_check": external_literature_check(),
        },
        "current_bracket": (
            "odd N_c, N_c != 1: {3,5,7,9,11,...} (F324/F325; the C7 upper "
            "bound is withdrawn). N_c=3 favoured empirically only (F293 "
            "Sec 4's 28.3-decade confinement-scale lever), by nothing "
            "structural. This module narrows nothing; it closes one more "
            "candidate route (G1) and flags one unverified lead (G3) for a "
            "future session."
        ),
        "params": {
            "n_gen": n_gen, "n_max": n_max, "mod16_n_max": mod16_n_max,
            "su3_pi4_order_override": su3_pi4_order_override,
            "include_nu_r": include_nu_r,
            "assumed_anomaly_modulus": assumed_anomaly_modulus,
        },
    }


def summary() -> Dict[str, Any]:
    return check_ncolour_ceiling()
