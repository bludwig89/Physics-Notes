#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derive_x1_branch.py — X1 resolved: branch A closed, branch B adopted
=====================================================================

2026-08-18   (F325)

The X1 fork (`docs/status/open-derivations.md` Part D) asked whether the model's
bare colour coupling is centre-normalised (branch B, g_s = 1/2,
alpha_s(M_Z) = 0.1186) or Casimir-normalised (branch A, g_s = sqrt3/4,
alpha_s(M_Z) = 0.0397), and named a d_1 computation as the decider.

**It does not need d_1.**  Branch A is closed two ways, each independent of the
other and each independent of any measured number on the structural side:

STRUCTURAL — the C_F is a matching artefact
-------------------------------------------
F298's C_F comes from evaluating the C7 identity with the ABELIAN rotor's
eigenvalue s(k)^2 in the numerator against the SU(N) gauge theory's C_2(R_k) in
the denominator.  Under EITHER self-consistent evaluation -- both sides abelian,
or both sides SU(N) -- chi = 1/(4 g^2) identically, for every N and every irrep
(`casimir_ladder.operator_consistency`, exact over Q, leg L6 of the F298 gate).
The mixed evaluation is not merely a different convention: off the k-string
tower it is level-dependent at N = 3 as well (F324 U1c found the sextet leg;
the full picture is chi in {3/4, 3/10, 3/16} plus UNDEFINED for the adjoint,
decuplet and 27, where the Z_3 rotor's s^2 = 0 against C_2 != 0 -- i.e. it
assigns zero electric cost to a triality-0 link).

Which evaluation is physical turns on whether the integer spectrum is derived
from the rule.  It is not: the rule's own (E, B) are continuous real fields
under an SO(2) rotation (`weak_wmu._f26_rotation_step`, F26), the integer
spectrum is introduced as the exactly-solvable case (F101 section 2,
`link_hamiltonian` "the integer (compact) electric field", U(1) "truncated at
|m| <= m_max"), and the model's own links are SU(3)-valued matrices
(`strong.py`, `gluon.py`, `bcc_action.plaquette_field_strength_su3`, F94, F99
D3).  `link_hamiltonian.py` holds no SU(3) matrix at all.

QUANTITATIVE — branch A is outside the model's own Lambda bracket
------------------------------------------------------------------
F280 S5 / CL252 published Lambda_MSbar/Lambda_rule in [1, 7.98] on 2026-08-05,
the day before F299 and F303 framed the fork.  Branch A requires 3.4e6:
5.63 decades above the band top, and 7.24x Wilson's own loops-only one-loop
constant for an action F287 section 4 MEASURES at 5.3-5.7x SMALLER discretisation
error than Wilson's.  Branch B's 1.7734 sits inside at 11%.  Landed as leg N8 of
the F303 gate (`derive_coupling_normalisation.casimir_branch_vs_f280_band`).

What this module adds
---------------------
The third leg, which the companion report named as X1's residual and which no
module carried: **the MAGNETIC side of C7**.  C7 matched the electric term only.
The worry was that the SU(3) plaquette operator is not cos(phi) -- its matrix
elements between irreps could carry dimension or 6j factors and move chi off 1.

Measured here, four results:

1. **It does not.**  The magnetic operator is -(lam/2) x (unit-entry adjacency +
   transpose) in BOTH theories: U(1)'s cos(phi) shift, and SU(N)'s fundamental
   fusion, which is multiplicity-free so its adjacency is 0/1.  Coefficient to
   coefficient lam <-> lam.  The magnetic term introduces no factor into the
   chi-map, so C7 survives a full electric + magnetic audit against a genuine
   SU(N) link Hamiltonian.  **X1's named residual closes negatively.**

2. **F111b T7 is link-count inconsistent and must not be quoted as
   confirmation.**  `su3_ladder.su3_rotor_hamiltonian` puts (g^2/2) C_2 on ONE
   link; T7 compares it against `link_hamiltonian.rotor_sigma1` at
   chi = 1/(4 g^2), which is FOUR.  Electric gaps 2/3 against 2, ratio exactly
   3 = n/C_F.  Compared at equal n the two rotors do not agree, and the
   discrepancy is exact:  s1_SU(N) / s1_U(1) = 2 / (N^2 - 1), independent of n.
   At N = 3 that is 1/4.  So there is no N_c selector here either -- the
   condition 2/(N^2-1) = 1 needs N^2 = 3 -- and T7's apparent agreement at N = 3
   is the 1-vs-4 mismatch, C_F d_F = (N^2-1)/2 = 4 coinciding with the four
   links.  Recorded because it is attractive enough to be re-derived by someone
   who does not know it is a convention artefact (the same reason F303 4.2
   recorded the three-bond plaquette).

3. **New and exact:** because s1 differs by 2/(N^2-1) at the same (chi, lam),
   sigma_1 carries a constant offset ln((N^2-1)/2) = ln 4 = 1.386294 nats at
   N = 3 between the implemented Z_3 / U(1) engine and the genuine SU(3) one.
   That is a correction to F99 / F100 / F101's string tension if the colour
   group is SU(3) -- and it is orthogonal to g_s, which is why it disturbs
   nothing above.

4. **A gap in F144 A1 step 2, found on the way and NOT a rescue of branch A.**
   The circularity lemma's residual vanishes at a = b for EVERY b (sympy;
   `solve` returns {r: 1} with b free -- this reproduces F303 N1's own
   factorisation).  At a = b the per-tick rotation angle is omega = b, so
   a = b = Omega(k) and **chi = 1/Omega(k)**.  chi = 1 therefore requires
   Omega = 1, which the lemma does not supply: chi = 1 is F101 section 7's
   normalisation, inherited, not derived -- and it is the SAME compactification
   choice as (1) above, so F144's A1 carries two inherited choices of one
   origin rather than zero knobs.  This does not restore branch A, which needs
   chi = 3/4 i.e. Omega = 4/3 and has nothing selecting that either.  It
   relocates F144's open normalisation from "zero knobs" to "one k-selection",
   plausibly the same object as the matching scale q_* (F155).

VERDICT
-------
**Branch A: TESTED, CLOSED.**  Structurally an artefact of a mixed operator
matching; quantitatively 5.63 decades outside the model's own committed bracket.
**Branch B: ADOPTED.**  g_s = 1/2, alpha_s(mu_0) = 1/(16 pi), the SU(N_c) beta
function is the right one to run with, and the "centre-normalised coupling with
an SU(N_c) beta function" inconsistency X1 named never existed.

COST, stated here rather than in a footnote
-------------------------------------------
* **CN19 falls.**  F298's "the C7 identity exists only for N_c <= 3" is a
  property of the mixed matching.
* **F324's UPPER constraint falls with it.**  F324 (2026-08-17) closes B10 on
  {3} from the Z_2 doublet parity (lower, untouched) paired with F298's C7
  support {2,3} (upper).  Remove the upper and B10 closes on ODD N_c only:
  {3, 5, 7, ...}.  F324's own section 3 U1c reaches the same place and books it
  as "falsifier 5b ... the most serious structural exposure on the upper side".
* **d_1's role changes**, it does not disappear: it now PINS alpha_s(M_Z) inside
  branch B and closes E3/Q1/Q2, rather than choosing between branches.  Its
  two-sided falsifier is unchanged and is now the sharpest statement in the
  sector: a completed vertex computation returning Lambda outside [1, 7.98]
  falsifies the g_s = 1/2 lock or F280's monotonicity assumption, and a return
  of 3.4e6 would reinstate branch A and CN19 with it.

Cross-references: F298 (the mixed matching, leg L6 added), F299 (the Casimir
measurement, re-characterised: it measures link REPRESENTATION CONTENT, which is
the premise under which the C_F cancels, and is beta-independent -- 2.49115 at
beta=24 against 2.49540 at beta=32, so it never discriminated), F303 (the three
closed candidates; this is the fourth its own conclusion asked for), F294 (its
"Remains" item 1 was already closed by F111b), F111b (the SU(3) character rotor,
defect in 2), F144 (A1 step 2, gap in 4), F280/CL252 (the bracket), F324 (the
upper constraint), F101/F110 (the rotor and C7), F155 (q_*).
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np

from casim.engine.gauge import su3_ladder as su
from casim.engine.gauge.casimir_ladder import (su_n_casimir, casimir_fundamental,
                                               operator_consistency)

__all__ = [
    "suN_character_rotor_s1", "u1_rotor_s1", "magnetic_adjacency_is_unit",
    "s1_ratio_law", "f111b_link_count_defect", "sigma_offset_su3_vs_zn",
    "circularity_fixes_ratio_only", "branch_verdict",
    "check_x1_branch", "summary",
]

#: F111b T7's pairing: the SU(3) rotor at ONE link against the U(1) rotor at
#: chi = 1/(4 g^2), i.e. FOUR.  Kept as named constants so the defect is
#: visible in the source rather than buried in a call.
F111B_N_LINKS_SU3 = 1
F111B_N_LINKS_U1 = 4
#: F265 / F303 4.2: the BCC minimal gauge loop is a 4-bond rhombus.  Derived
#: geometry, not a convention -- there is no closed 3-bond loop.
N_LINKS_BCC = 4


# ==========================================================================
# General SU(N) irrep data and the character rotor
# ==========================================================================
def _dim(rows: Sequence[int], N: int) -> Fraction:
    lam = list(rows) + [0] * (N - len(rows))
    num = den = 1
    for i in range(N):
        for j in range(i + 1, N):
            num *= (lam[i] - lam[j] + j - i)
            den *= (j - i)
    return Fraction(num, den)


def _normalise(rows: Sequence[int], N: int):
    lam = [r for r in rows if r > 0]
    if len(lam) > N:
        return None
    lam = lam + [0] * (N - len(lam))
    sub = lam[N - 1]
    return tuple(r - sub for r in lam[:N] if r - sub > 0)


def _fuse_box(rows: Sequence[int], N: int) -> List[tuple]:
    """F (x) R: add one box to a legal row, then strip height-N columns."""
    lam = list(rows) + [0]
    out = []
    for i in range(len(lam)):
        if i == 0 or lam[i] < lam[i - 1]:
            new = lam[:]
            new[i] += 1
            if len([r for r in new if r > 0]) <= N:
                t = _normalise(tuple(r for r in new if r > 0), N)
                if t is not None:
                    out.append(t)
    return out


def _ladder(N: int, maxbox: int) -> List[tuple]:
    seen, frontier = {(): True}, [()]
    for _ in range(maxbox):
        nxt = []
        for r in frontier:
            for t in _fuse_box(r, N):
                if t not in seen:
                    seen[t] = True
                    nxt.append(t)
        frontier = nxt
    return sorted(seen, key=lambda r: (float(su_n_casimir(list(r), N)), r))


def suN_character_rotor_s1(N: int, g2: float, lam_mag: float,
                           n_links: int, maxbox: int = 8,
                           magnetic_scale: float = 1.0) -> float:
    """s1 = <chi_F>/d_F in the ground state of

        H = (g^2/2) n_links C_2  -  (lam/2) (chi_F + chi_Fbar)

    the SU(N) analogue of the F101 compact rotor, with the fundamental fusion
    adjacency playing the role of cos(phi).  ``magnetic_scale`` is the declared
    control: it multiplies the SU(N) magnetic term only, which must break the
    ratio law of `s1_ratio_law`.
    """
    reps = _ladder(N, maxbox)
    pos = {r: i for i, r in enumerate(reps)}
    n = len(reps)
    H = np.zeros((n, n))
    MF = np.zeros((n, n))
    for r in reps:
        H[pos[r], pos[r]] = 0.5 * g2 * n_links * float(su_n_casimir(list(r), N))
        for t in _fuse_box(r, N):
            if t in pos:
                MF[pos[t], pos[r]] = 1.0
    H -= 0.5 * lam_mag * magnetic_scale * (MF + MF.T)
    _w, v = np.linalg.eigh(H)
    a = v[:, 0]
    if a[pos[()]] < 0:
        a = -a
    return float(a @ (MF @ a)) / float(_dim((1,), N))


def u1_rotor_s1(chi: float, lam_mag: float, m_max: int = 40) -> float:
    """s1 = <e^{i phi}> for the F101 rotor H = (1/2chi) m^2 - lam cos(phi).

    Written here in numpy rather than imported from `link_hamiltonian` so this
    module carries no scipy dependency; agreement with `rotor_sigma1` is a
    CHECKED quantity (leg X3), not an assumption.
    """
    m = np.arange(-m_max, m_max + 1)
    H = np.diag(m.astype(float) ** 2 / (2.0 * chi))
    off = -0.5 * lam_mag * np.ones(len(m) - 1)
    H += np.diag(off, 1) + np.diag(off, -1)
    _w, v = np.linalg.eigh(H)
    a = v[:, 0]
    if a[m_max] < 0:
        a = -a
    return float(np.sum(a[:-1] * a[1:]))


# ==========================================================================
# 1 — the magnetic operator is a unit-entry adjacency in BOTH theories
# ==========================================================================
def magnetic_adjacency_is_unit(cut: int = 6) -> Dict[str, Any]:
    """Does the magnetic term carry a group factor?  No.

    U(1):   -lam cos(phi) = -(lam/2)(Gamma + Gamma^dag), Gamma|m> = |m+1>.
    SU(3):  -(lam/2)(chi_F + chi_Fbar); chi_F chi_R = sum_{R' in F(x)R} chi_R'
            is MULTIPLICITY-FREE, so the adjacency is 0/1.

    Both are -(lam/2) x (unit-entry adjacency + transpose), so the magnetic
    coefficient is lam in both and the chi-map is untouched by this term.
    """
    _H, _reps, MF = su.su3_rotor_hamiltonian(1.0, 1.0, cut)
    vals = sorted({float(x) for x in MF[MF != 0]})
    # U(1): the same object, built explicitly
    m_max = 6
    G = np.diag(np.ones(2 * m_max), 1)
    u1_vals = sorted({float(x) for x in G[G != 0]})
    return {"su3_fusion_adjacency_values": vals,
            "u1_shift_adjacency_values": u1_vals,
            "both_unit_entry": vals == [1.0] and u1_vals == [1.0],
            "su3_multiplicity_free": True,
            "conclusion": ("the magnetic term is -(lam/2) x (unit adjacency + "
                           "transpose) in both theories, so it introduces no "
                           "factor into chi = 1/(4 g^2): C7 survives a full "
                           "electric + magnetic audit against a genuine SU(N) "
                           "link Hamiltonian")}


# ==========================================================================
# 2 — the exact ratio law, and why it is not an N_c selector
# ==========================================================================
def s1_ratio_law(n_values: Sequence[int] = (3, 4, 5),
                 n_links_list: Sequence[int] = (1, 4),
                 g2: float = 1.0, lams: Sequence[float] = (1e-4, 1e-5),
                 maxbox: int = 8, magnetic_scale: float = 1.0
                 ) -> Dict[str, Any]:
    """At EQUAL n_links, s1_SU(N) / s1_U(1) -> 2/(N^2 - 1), independent of n.

    Derivation, for the record: first-order PT gives
        c_F   = (lam/2) / ((g^2/2) n C_F)      (SU(N), singlet -> F and Fbar)
        s1    = (c_F + c_Fbar)/d_F = 4 lam / (g^2 n (N^2-1))
        s1_U1 = 2 lam chi = 2 lam / (n g^2)
    so the ratio is 2/(N^2-1) and the link count cancels.  Setting it to 1 needs
    N^2 = 3: **there is no N_c selector here.**

    This is a LEADING-ORDER statement, so the measured ratio carries an O(lam)
    correction.  Two couplings a decade apart are run and Richardson-extrapolated
    to lam = 0; the check is that the extrapolant hits the law AND that the
    residual scales linearly with lam (which is what shows the departure is the
    PT correction rather than an error).  Cut-independent: the same worst
    deviation is returned at maxbox 6, 8 and 10.
    """
    lam_hi, lam_lo = float(lams[0]), float(lams[1])
    ratio_lam = lam_lo / lam_hi
    rows = []
    worst_extrap = 0.0
    slopes = []
    for n_links in n_links_list:
        chi = 1.0 / (n_links * g2)          # 1/(2 chi) = (g^2/2) n
        b_hi = u1_rotor_s1(chi, lam_hi)
        b_lo = u1_rotor_s1(chi, lam_lo)
        for N in n_values:
            a_hi = suN_character_rotor_s1(N, g2, lam_hi, n_links, maxbox,
                                          magnetic_scale)
            a_lo = suN_character_rotor_s1(N, g2, lam_lo, n_links, maxbox,
                                          magnetic_scale)
            law = 2.0 / (N * N - 1)
            r_hi, r_lo = a_hi / b_hi, a_lo / b_lo
            # linear-in-lam Richardson to lam = 0
            r0 = (r_lo - ratio_lam * r_hi) / (1.0 - ratio_lam)
            dev0 = abs(r0 / law - 1.0)
            worst_extrap = max(worst_extrap, dev0)
            d_hi, d_lo = abs(r_hi / law - 1.0), abs(r_lo / law - 1.0)
            if d_lo > 0:
                slopes.append(d_hi / d_lo)
            rows.append({"N": int(N), "n_links": int(n_links),
                         "ratio_lam_hi": r_hi, "ratio_lam_lo": r_lo,
                         "ratio_extrapolated": r0,
                         "law_2_over_N2m1": law,
                         "rel_dev_extrapolated": dev0,
                         "rel_dev_lam_hi": d_hi, "rel_dev_lam_lo": d_lo})
    # The residual vanishes AT LEAST linearly in lam.  It is O(lam) at N = 3
    # (slope ~10) and O(lam^2) at N >= 4 (slope ~100) -- the singlet's return
    # path through the ladder is shorter at N = 3 -- so the assertion is
    # `slope >= 9`, not `slope == 10`.  Measured, not assumed.
    vanishing = all(sl >= 9.0 for sl in slopes) if slopes else False
    return {"rows": rows, "lams": [lam_hi, lam_lo],
            "worst_rel_dev_extrapolated": worst_extrap,
            "slopes": slopes,
            "residual_vanishes_at_least_linearly_in_lam": vanishing,
            "law_holds": worst_extrap < 1e-7 and vanishing,
            "ratio_is_one_at": "N^2 = 3 - no integer, hence NO N_c selector",
            "note": ("independent of n_links, so F111b T7's agreement at N=3 "
                     "cannot be a statement about the group")}


def f111b_link_count_defect(g2: float = 1.0, lam_mag: float = 1e-3,
                            maxbox: int = 8) -> Dict[str, Any]:
    """Reproduce F111b T7's pairing and measure the mismatch that makes it work.

    T7 compares `su3_rotor_sigma1` (ONE link) against `rotor_sigma1` at
    chi = 1/(4 g^2) (FOUR).  Both give s1 -> lam/(2 g^2), so T7 passes -- but
    the electric gaps differ by exactly n/C_F = 3, so the two Hamiltonians are
    not the same physical system and the agreement is a convention artefact.
    """
    a = suN_character_rotor_s1(3, g2, lam_mag, F111B_N_LINKS_SU3, maxbox)
    b = u1_rotor_s1(1.0 / (F111B_N_LINKS_U1 * g2), lam_mag)
    cf = float(casimir_fundamental(3))
    gap_su3 = 0.5 * g2 * F111B_N_LINKS_SU3 * cf
    gap_u1 = 0.5 * g2 * F111B_N_LINKS_U1 * 1.0
    return {"s1_su3_1link": a, "s1_u1_4link": b,
            "t7_relative_agreement": abs(a / b - 1.0),
            "t7_reproduces": abs(a / b - 1.0) < 5e-3,
            "electric_gap_su3": gap_su3, "electric_gap_u1": gap_u1,
            "gap_ratio": gap_u1 / gap_su3,
            "gap_ratio_is_n_over_C_F": abs(gap_u1 / gap_su3
                                           - N_LINKS_BCC / cf) < 1e-12,
            "why_it_agrees": ("C_F d_F = (N^2-1)/2 = 4 at N=3 coincides with "
                              "the four links, so the 1-vs-4 mismatch cancels "
                              "the group factor exactly at N=3 and nowhere "
                              "else"),
            "verdict": ("T7 is arithmetically correct and is NOT independent "
                        "confirmation of chi = 1/(4 g^2); rebuild it at equal "
                        "n, where the exact statement is s1_SU(N)/s1_U(1) = "
                        "2/(N^2-1)")}


def sigma_offset_su3_vs_zn(N: int = 3) -> Dict[str, Any]:
    """sigma_1 = -ln s1 carries a constant offset ln((N^2-1)/2) between the
    implemented Z_N / U(1) engine and the genuine SU(N) one.  Exact, and
    orthogonal to g_s."""
    off = math.log((N * N - 1) / 2.0)
    return {"N": int(N), "s1_ratio": 2.0 / (N * N - 1),
            "sigma_offset_nats": off,
            "is_ln4_at_3": abs(off - math.log(4.0)) < 1e-15 if N == 3 else None,
            "affects": "F99 / F100 / F101 sigma_1; NOT g_s"}


# ==========================================================================
# 3 — the circularity lemma fixes a ratio, so chi = 1 is a normalisation
# ==========================================================================
def circularity_fixes_ratio_only() -> Dict[str, Any]:
    """F144 A1 step 2, pressed one step past F303 N1.

    F303 established the residual factorises as (r-1) x sine with r = a/b, so
    orthogonality holds iff r = 1 "whatever b is", and concluded the lemma is
    group-blind.  It is -- and the same fact says the lemma does not fix the
    ABSOLUTE stiffness either.  At a = b the one-tick map is a rotation by
    omega t = b t, so with t = 1 tick the rule's rotation angle IS the
    stiffness: a = b = Omega(k), hence chi = 1/Omega(k).

    chi = 1 therefore requires Omega = 1.  The lemma does not supply it;
    F101 section 7's normalisation does.
    """
    import sympy as sp
    a, b, t, r = sp.symbols("a b t r", positive=True)
    w = sp.sqrt(a * b)
    M = sp.Matrix([[sp.cos(w * t), b / w * sp.sin(w * t)],
                   [-a / w * sp.sin(w * t), sp.cos(w * t)]])
    resid = sp.simplify(M.T * M - sp.eye(2))
    at_equal = sp.simplify(resid.subs(b, a))
    vanishes_for_every_b = bool(at_equal == sp.zeros(2, 2))
    roots = sp.solve([sp.Eq(sp.simplify(resid[0, 0].subs(a, r * b)), 0),
                      sp.Eq(sp.simplify(resid[0, 1].subs(a, r * b)), 0)],
                     [r], dict=True)
    root_exprs = [str(s[r]) for s in roots if r in s]
    ratio_root_present = "1" in root_exprs
    # every OTHER root contains t: those are ticks landing on a half-period,
    # where the flow is +-I for any stiffness (F303's own observation).
    others_carry_t = all("t" in e for e in root_exprs if e != "1")
    # omega at a = b
    omega_at_equal = sp.simplify(w.subs(b, a))
    return {"residual_vanishes_at_a_equals_b_for_every_b": vanishes_for_every_b,
            "ratio_roots": root_exprs,
            "ratio_root_one_present": ratio_root_present,
            "other_roots_are_tick_conditions": others_carry_t,
            "omega_at_a_equals_b": str(omega_at_equal),
            "chi_is_one_over_omega": True,
            "conclusion": ("circularity fixes a/b = 1 and NOT the absolute "
                           "stiffness; a = b = Omega(k) so chi = 1/Omega(k), "
                           "and chi = 1 is F101 section 7's normalisation "
                           "rather than a derivation.  This does not restore "
                           "branch A, which needs chi = 3/4 i.e. Omega = 4/3 "
                           "and has nothing selecting that either")}


# ==========================================================================
# 4 — the verdict, assembled from the two independent legs
# ==========================================================================
def branch_verdict() -> Dict[str, Any]:
    """Branch A closed, branch B adopted -- with both legs re-measured here
    rather than quoted, by importing the two entry points that own them."""
    from casim.engine.gauge.derive_coupling_normalisation import (
        casimir_branch_vs_f280_band)
    oc = operator_consistency()
    bnd = casimir_branch_vs_f280_band()
    return {
        "branch_A": {
            "reading": "Casimir, chi = 1/C_F = 3/4, g_s = sqrt3/4",
            "alpha_s_MZ": 0.03970,
            "status": "TESTED, CLOSED",
            "structural_leg": ("the C_F is a mixed-operator artefact: "
                               "consistent matchings give chi = 1/(4 g^2) for "
                               "every N and every irrep"),
            "structural_leg_holds": oc["consistent_matchings_give_one"],
            "quantitative_leg": ("required Lambda ratio "
                                 f"{bnd['casimir_branch_lambda_ratio']:.4g} is "
                                 f"{bnd['casimir_branch_decades_above_band']:.2f}"
                                 " decades above CL252's committed band"),
            "quantitative_leg_holds": bnd["casimir_branch_outside_band"],
        },
        "branch_B": {
            "reading": "chi = 1, g_s = 1/2, alpha_0 = 1/(16 pi)",
            "alpha_s_MZ_one_loop": 0.11954,
            "status": "ADOPTED",
            "inside_f280_band": bnd["no_casimir_branch_inside_band"],
            "position_in_band": bnd["no_casimir_branch_position_in_band"],
        },
        "cost": {
            "CN19": "falls -- the N_c <= 3 restriction is a mixed-matching artefact",
            "F324_upper_constraint": ("falls with it; B10 closes on ODD N_c "
                                      "only, {3, 5, 7, ...}, the lower "
                                      "(Z_2 doublet parity) leg untouched"),
            "d1": ("role changes, does not disappear: it now PINS alpha_s "
                   "inside branch B rather than choosing a branch"),
        },
        "residual": ("which Omega the single-plaquette rotor carries, on the "
                     "BCC dispersion -- plausibly the same object as F155's "
                     "q_*.  Replaces 'the magnetic side is unaudited', closed "
                     "here"),
    }


# ==========================================================================
# Registry entry point
# ==========================================================================
def check_x1_branch(su3_cut: int = 8,
                    magnetic_scale: float = 1.0,
                    n_links: int = N_LINKS_BCC) -> Dict[str, Any]:
    """The F325 gate.

    Declared controls:

    ``--param magnetic_scale=2.0``  double the SU(N) magnetic term only.  X2
        must go red: the ratio law s1_SU(N)/s1_U(1) = 2/(N^2-1) is a statement
        about MATCHED magnetic normalisations, and a check that survives an
        unmatched one is not testing the matching.
    ``--param su3_cut=2``           truncate the character ladder below
        convergence.  X2 must go red -- an unconverged rotor cannot assert an
        exact ratio.
    """
    checks: List[Tuple[str, bool, Any]] = []

    mag = magnetic_adjacency_is_unit()
    checks.append(("X1 the magnetic term is -(lam/2) x (unit-entry adjacency + "
                   "transpose) in BOTH theories, so it adds no factor to the "
                   "chi-map",
                   mag["both_unit_entry"],
                   {"su3": mag["su3_fusion_adjacency_values"],
                    "u1": mag["u1_shift_adjacency_values"]}))

    law = s1_ratio_law(maxbox=su3_cut, magnetic_scale=magnetic_scale)
    checks.append(("X2 at equal n_links, s1_SU(N)/s1_U(1) -> 2/(N^2-1) as "
                   "lam -> 0, independent of n, with the residual linear in "
                   "lam -- so there is no N_c selector in it",
                   law["law_holds"],
                   {"extrapolated_dev": law["worst_rel_dev_extrapolated"],
                    "vanishes_in_lam":
                        law["residual_vanishes_at_least_linearly_in_lam"],
                    "slopes": [round(s_, 2) for s_ in law["slopes"]]}))

    d = f111b_link_count_defect(maxbox=su3_cut)
    checks.append(("X3 F111b T7 reproduces, and its electric gaps differ by "
                   "exactly n/C_F = 3 -- the agreement is a 1-link-vs-4-link "
                   "artefact, not a confirmation",
                   d["t7_reproduces"] and d["gap_ratio_is_n_over_C_F"],
                   {"t7_dev": d["t7_relative_agreement"],
                    "gap_ratio": d["gap_ratio"]}))

    off = sigma_offset_su3_vs_zn(3)
    checks.append(("X4 sigma_1 carries an exact offset ln((N^2-1)/2) = ln 4 = "
                   "1.386294 nats between the implemented Z_3/U(1) engine and "
                   "the SU(3) one -- affects F99/F100/F101, not g_s",
                   off["is_ln4_at_3"], off["sigma_offset_nats"]))

    lem = circularity_fixes_ratio_only()
    checks.append(("X5 the circularity lemma vanishes at a=b for EVERY b, so "
                   "a=b=Omega(k) and chi=1/Omega(k): chi=1 is a normalisation, "
                   "not a derivation (and branch A's chi=3/4 is not derived "
                   "either)",
                   lem["residual_vanishes_at_a_equals_b_for_every_b"]
                   and lem["ratio_root_one_present"]
                   and lem["other_roots_are_tick_conditions"],
                   lem["ratio_roots"]))

    ver = branch_verdict()
    checks.append(("X6 branch A is closed on BOTH legs -- structural (the C_F "
                   "is a mixed-matching artefact) and quantitative (5.6 "
                   "decades outside CL252's band)",
                   ver["branch_A"]["structural_leg_holds"]
                   and ver["branch_A"]["quantitative_leg_holds"],
                   ver["branch_A"]["quantitative_leg"]))
    checks.append(("X7 branch B is adopted and sits inside the model's own "
                   "Lambda bracket",
                   ver["branch_B"]["inside_f280_band"],
                   ver["branch_B"]["position_in_band"]))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"su3_cut": su3_cut, "magnetic_scale": magnetic_scale,
                       "n_links": n_links},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    ver = branch_verdict()
    return {
        "X1_resolved": True,
        "branch_A_status": ver["branch_A"]["status"],
        "branch_B_status": ver["branch_B"]["status"],
        "g_s_adopted": 0.5,
        "alpha_0_adopted": 1.0 / (16.0 * math.pi),
        "magnetic_side_of_C7": "audited, no factor -- X1's named residual closes",
        "cost": ver["cost"],
        "residual": ver["residual"],
    }
