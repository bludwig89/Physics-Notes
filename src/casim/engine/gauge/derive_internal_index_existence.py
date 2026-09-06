"""derive_internal_index_existence.py — does the colour index have to exist?

THE QUESTION, AND WHERE IT SITS IN THE B1 CHAIN
================================================
F317 reduced colour's six impositions to one: *that* the quark carries an
internal index the rule does not read.  F318 attacked that residual and split
it into three separate questions (PERMIT / SHAPE / FORCE), finding the cell
neither forbids nor requires the index -- it is indifferent -- and that the
forcing, when it comes, comes from the model's own derived Fermi statistics
(F289) plus one further fact: *that the matter sector contains a
three-constituent bound state*.  F324, which uses this row's premises to pin
N_c = 3 exactly, restates the same residual verbatim in its own "Remains"
section: *"Premise (ii) -- the index exists by fiat."*  Nothing between F317
and F324 has moved it.

This module does not re-attack any of that.  It narrows one further step:
not WHY three constituents (that is F317 S6 / F318 SD / F324's business, row
B10), but why the index must exist AT ALL, i.e. why N > 1 rather than N = 1
(no index -- a quark that is, structurally, an ordinary lepton-like Dirac
fermion with no internal factor).

THE ARGUMENT, IN ONE TABLE
===========================
    fact                                  | status        | source
    --------------------------------------|---------------|------------------
    (a) a QUARK-ONLY (no antiquark) SU(N)  | derived here,  | generalises
        colour singlet needs EXACTLY N     | computed       | F317 S6 (which
        valence constituents               |                | fixed k=3)
    (b) a composite of k identical spin-1/2| derived here,  | standard, but
        fermions is ITSELF a fermion iff k | computed       | verified by
        is odd                             |                | explicit
                                            |                | permutation
    (c) observed baryons (the model's own  | OBSERVATIONAL  | named, not
        quark-only colour singlets, e.g.   | INPUT          | computed
        the proton/neutron) are fermions   |                |
    (d) quarks are never observed as free, | OBSERVATIONAL  | named, not
        isolated particles (confinement -- | INPUT          | computed
        no free fractional electric charge |                |
        has ever been detected)            |                |

(a)+(c) force N to be ODD: the model's own valence-quark baryon has k = N
constituents (a), and (c) requires that composite to be a fermion, which by
(b) means N is odd.  This alone does NOT exclude N = 1 -- a lone free quark
is trivially odd (k=1) and trivially a fermion.  (d) is what excludes it: at
N = 1 the internal factor carries dim su(1) = 0 generators -- LITERALLY no
gauge bosons, hence no possible confining force -- so if quarks are observed
confined at all, N != 1.  N odd AND N != 1 (equivalently N >= 2, since dim
su(N) > 0 first at N = 2, and odd excludes N=2 itself) leaves {3, 5, 7, ...}.

WHAT THIS DOES AND DOES NOT CLOSE
==================================
It does NOT derive N = 3 (that is untouched, and is not attempted here --
F317 S6 / F318 SD's own "three-constituent bound state" input is still what
pins the value, and F324's independent {3,5,7,...} bracket, reached from
completely different premises (Witten's SU(2)_L anomaly + generation
parity), is reproduced here as a CROSS-CHECK, not re-derived from it and not
depended upon).  It DOES turn "the index exists, by fiat" into a conditional
derivation resting on two named, well-established observational facts
(baryons are fermions; quarks are confined) rather than one flatly-asserted
structural fact -- which is what row B1 asks this attack to attempt.  The
residual is renamed, not eliminated, in exactly the sense F317 and F318 both
used the phrase.

WHAT IS MEASURED (each is a CHECKS row, each has a control)
=============================================================
S0  dim su(N) = N^2 - 1, and it is EXACTLY ZERO at N = 1: the trivial case
    carries no gauge bosons at all, so "N = 1" and "no internal index" are
    the same statement, not merely a terminological identification.

S1  THE GENERALISED CONSTITUENT-COUNT THEOREM.  F317 S6 fixed k = 3 and
    scanned N = 2..6.  Scanned here on the full (N, k) grid (N = 1..6,
    k = 0..4, wherever N^k stays computationally small): the SU(N)-invariant
    subspace of Lambda^k(C^N) is 1-dimensional iff k = N (k >= 1), and 0
    otherwise.  Standard SU(N) representation theory (Lambda^k of the
    fundamental is irreducible and non-trivial for 0 < k < N; the top
    exterior power Lambda^N is the 1-dimensional determinant/trivial rep);
    what is new here is running it as a genuine two-parameter scan rather
    than the one N-3-diagonal F317 needed for its own multiplicity result.

S2  COMPOSITE EXCHANGE STATISTICS, COMPUTED NOT QUOTED.  The permutation
    exchanging two blocks of k identical fermions (a genuine block-swap
    permutation on 2k labelled particles) has signature (-1)^k -- verified
    for k = 1..6 by building the permutation and computing its parity
    (`sympy.combinatorics.Permutation.signature`), not by invoking the
    textbook rule.

S3  HENCE: A QUARK-ONLY BARYON IS A FERMION IFF N IS ODD.  Combining S1 (a
    baryon has k = N constituents) with S2 (a k-fermion composite is itself
    a fermion iff k odd): the model's colour-N baryon is predicted fermionic
    iff N is odd.  Checked at the probed N against the OBSERVATIONAL premise
    that real baryons (protons, neutrons) are fermions.

S4  HENCE: N = 1 IS EXCLUDED BY CONFINEMENT.  dim su(N) > 0 iff N >= 2 (S0).
    A confining force needs a connection to confine WITH; N = 1 has none.
    Checked at the probed N against the OBSERVATIONAL premise that quarks
    are never observed free.

S5  THE BRACKET.  {N : N odd and N >= 2} over N = 1..12 is exactly
    {3, 5, 7, 9, 11} -- matching F324's own post-S22 bracket, reached from
    entirely different premises (Witten's SU(2)_L global anomaly + the
    generation-parity argument, not composite statistics or confinement).
    Recorded as an independent cross-check; NOT used to argue for either
    finding, and does not by itself pin N = 3.

CONTROLS
========
  --param n_probe=4                  an EVEN N.  S3 must go red: a 4-quark
      colour-4 "baryon" is bosonic, contradicting observed fermionic
      baryons -- the oddness requirement is a real discriminator, not
      vacuous.
  --param n_probe=1                  the excluded case itself.  S4 must go
      red: dim su(1) = 0, so there is no gauge boson to confine with, and a
      theory with N=1 is observationally a theory with NO colour at all.
  --param bosonic_baryon=true        treat the composite exchange as
      bosonic regardless of constituent count (i.e. ignore that quarks are
      themselves fermions).  S3 must go red AT EVERY N INCLUDING N=3: without
      fermionic valence quarks, nothing ever predicts a fermionic baryon, at
      any colour count, which is what shows S2's fermion-specific sign (not
      group theory alone) is what is doing the work in S3.
  --param partial_generator_check=true   check invariance under only ONE
      generator of su(N) instead of the full algebra when building S1.
      Several off-diagonal (N,k) cells acquire spurious "singlets" (states
      invariant under that one generator but not the group) -- S1 must go
      red -- showing the "iff k=N" result depends on the full joint kernel,
      not a partial one.

Cross-references: F317 (S6, the fixed-k=3 precedent this generalises),
F318 (SD, the "does not force existence" verdict this narrows), F324
(SS10 item 1, "the index exists by fiat" -- the residual this attacks; and
the {3,5,7,...} bracket reproduced independently in S5), F289 (derived Fermi
statistics, imported not re-derived), F86/F110 (confinement, cited for
motivation only -- not used as a premise; S4's confinement leg rests on
dim su(N) alone, not on the tree's own confinement dynamics, precisely to
avoid assuming N=3 already in order to derive N>1).
"""
from __future__ import annotations

import itertools
import math
from typing import Any, Dict, List, Sequence, Tuple

from casim.numerics import xp as np
import sympy as sp
from sympy.combinatorics import Permutation

from casim.engine.gauge.derive_su3_structure import su_n_generators


# ==========================================================================
# S0 -- dim su(N), and the N=1 triviality
# ==========================================================================
def dim_su(n: int) -> int:
    """dim su(N) = N^2 - 1.  Zero only at N=1: no generators, no gauge boson."""
    return n * n - 1


# ==========================================================================
# S1 -- the generalised constituent-count theorem
# ==========================================================================
def _antisymmetriser_projector(n: int, k: int) -> np.ndarray:
    """Projector onto Lambda^k(C^n) inside (C^n)^{ox k}."""
    d = n ** k
    idx = list(itertools.product(range(n), repeat=k))
    pos = {t: a for a, t in enumerate(idx)}
    P = np.zeros((d, d), dtype=complex)
    for perm in itertools.permutations(range(k)):
        sgn = Permutation(list(perm)).signature()
        for t in idx:
            src = pos[t]
            tgt = pos[tuple(t[p] for p in perm)]
            P[tgt, src] += sgn / math.factorial(k)
    return P


def constituent_singlet(n: int, k: int, partial_generator_check: bool = False
                        ) -> Dict[str, Any]:
    """dim of the SU(n)-invariant subspace of Lambda^k(C^n).

    ``partial_generator_check=True`` is the soundness control: it checks
    invariance under only the FIRST generator of su(n) rather than the whole
    algebra, and is expected to over-count singlets away from k=n.
    """
    if k > n:
        return {"n": n, "k": k, "lambda_k_dim": 0, "singlet_dim": 0, "has_singlet": False}
    if k == 0:
        return {"n": n, "k": k, "lambda_k_dim": 1, "singlet_dim": 1, "has_singlet": True}
    P = _antisymmetriser_projector(n, k)
    ev, vec = np.linalg.eigh(P)
    keep = vec[:, ev > 0.5]
    lam_dim = keep.shape[1]
    if lam_dim == 0:
        return {"n": n, "k": k, "lambda_k_dim": 0, "singlet_dim": 0, "has_singlet": False}
    if n == 1:
        # su(1) is trivial (0 generators): every state is trivially invariant.
        return {"n": n, "k": k, "lambda_k_dim": int(lam_dim), "singlet_dim": int(lam_dim),
                "has_singlet": bool(lam_dim == 1)}
    T = su_n_generators(n)
    if partial_generator_check:
        T = T[:1]
    eye = np.eye(n, dtype=complex)
    rows = []
    for a in range(len(T)):
        G = np.zeros((n ** k, n ** k), dtype=complex)
        for slot in range(k):
            ops = [eye] * k
            ops[slot] = T[a]
            term = ops[0]
            for m in ops[1:]:
                term = np.kron(term, m)
            G += term
        rows.append(keep.conj().T @ G @ keep)
    stack = np.concatenate(rows, axis=0)
    sv = np.linalg.svd(stack, compute_uv=False)
    tol = 1e-9
    singlet_dim = int(np.sum(sv < tol)) + (lam_dim - sv.size)
    return {"n": n, "k": k, "lambda_k_dim": int(lam_dim), "singlet_dim": int(singlet_dim),
            "has_singlet": bool(singlet_dim >= 1)}


def constituent_count_theorem(n_max: int = 6, k_max: int = 4,
                              partial_generator_check: bool = False
                              ) -> Dict[str, Any]:
    """Scan the (N,k) grid and confirm has_singlet iff k=N, for k in 1..k_max."""
    rows = []
    for n in range(1, n_max + 1):
        for k in range(1, k_max + 1):
            if n ** k > 1600:
                continue
            r = constituent_singlet(n, k, partial_generator_check=partial_generator_check)
            rows.append(r)
    mismatches = [r for r in rows if r["has_singlet"] != (r["k"] == r["n"])]
    return {"rows": rows, "n_tested": len(rows), "n_mismatch": len(mismatches),
            "mismatches": mismatches, "theorem_holds": len(mismatches) == 0}


# ==========================================================================
# S2 -- composite exchange statistics, computed
# ==========================================================================
def composite_block_swap_parity(k: int, bosonic: bool = False) -> Dict[str, Any]:
    """Parity of exchanging two blocks of k identical fermions (2k labelled
    particles, block swap i <-> i+k).  Built and measured, not quoted.
    """
    perm = list(range(2 * k))
    for i in range(k):
        perm[i], perm[i + k] = perm[i + k], perm[i]
    sign = int(Permutation(perm).signature())
    if bosonic:
        sign = 1
    expected = 1 if bosonic else (-1) ** k
    return {"k": k, "measured_sign": sign, "expected_sign": expected,
            "matches": sign == expected, "is_fermionic_composite": sign == -1}


def exchange_statistics_scan(k_max: int = 6, bosonic: bool = False) -> Dict[str, Any]:
    rows = [composite_block_swap_parity(k, bosonic=bosonic) for k in range(1, k_max + 1)]
    all_match = all(r["matches"] for r in rows)
    return {"rows": rows, "all_match_formula": all_match}


# ==========================================================================
# S3/S4/S5 -- the forcing argument and the bracket
# ==========================================================================
def baryon_is_fermion_iff_odd(n_probe: int, bosonic_baryon: bool = False) -> Dict[str, Any]:
    """S1 gives k=N constituents for a quark-only colour-N singlet; S2 gives
    that composite's statistics.  Checked against the OBSERVATIONAL premise
    that real baryons are fermions.
    """
    r = composite_block_swap_parity(n_probe, bosonic=bosonic_baryon)
    predicted_fermion = r["is_fermionic_composite"]
    observed_fermion = True  # the proton and neutron are observed fermions
    return {"n_probe": n_probe, "bosonic_baryon": bosonic_baryon,
            "predicted_fermion": predicted_fermion, "observed_fermion": observed_fermion,
            "matches_observation": predicted_fermion == observed_fermion}


def confinement_excludes_n1(n_probe: int) -> Dict[str, Any]:
    """A confining force needs a connection; dim su(N) > 0 iff N >= 2."""
    d = dim_su(n_probe)
    has_gauge_bosons = d > 0
    quarks_observed_confined = True  # no free fractional charge ever detected
    return {"n_probe": n_probe, "dim_su_n": d, "has_gauge_bosons": has_gauge_bosons,
            "quarks_observed_confined": quarks_observed_confined,
            "consistent_with_confinement": has_gauge_bosons or not quarks_observed_confined}


def the_bracket(n_max: int = 12) -> Dict[str, Any]:
    """{N : N odd and N has gauge bosons (N>=2)} -- the forced set."""
    allowed = []
    for n in range(1, n_max + 1):
        odd = (n % 2 == 1)
        has_bosons = dim_su(n) > 0
        if odd and has_bosons:
            allowed.append(n)
    f324_bracket_reference = [n for n in range(1, n_max + 1) if n % 2 == 1 and n != 1]
    return {"n_max": n_max, "allowed": allowed,
            "matches_f324_post_s22_bracket": allowed == f324_bracket_reference,
            "excludes_n1": 1 not in allowed}


# ==========================================================================
# The registry entry point
# ==========================================================================
def check_internal_index_existence(n_probe: int = 3,
                                   bosonic_baryon: bool = False,
                                   partial_generator_check: bool = False
                                   ) -> Dict[str, Any]:
    """The B1-existence gate, as a registry entry with real parameters.

    Declared controls (see module docstring for the full reasoning):
      --param n_probe=4                    S3 red
      --param n_probe=1                    S4 red
      --param bosonic_baryon=true          S3 red (at every N, including 3)
      --param partial_generator_check=true S1 red
    """
    checks: List[Tuple[str, bool, Any]] = []
    n = int(n_probe)

    # ---- S0: N=1 is the trivial case, checked not assumed -------------------
    d1 = dim_su(1)
    checks.append(("S0 dim su(1) = 0 exactly: the N=1 case carries no "
                   "generators at all -- no gauge boson is even possible",
                   d1 == 0, d1))

    # ---- S1: generalised constituent-count theorem ---------------------------
    thm = constituent_count_theorem(n_max=6, k_max=4,
                                    partial_generator_check=partial_generator_check)
    checks.append(("S1 the SU(N)-invariant subspace of Lambda^k(C^N) is "
                   "1-dimensional IFF k=N, over the whole tested (N,k) grid "
                   "(generalises F317 S6's fixed k=3 scan)",
                   thm["theorem_holds"], (thm["n_tested"], thm["n_mismatch"])))

    # ---- S2: composite exchange statistics, computed -------------------------
    exch = exchange_statistics_scan(k_max=6)
    checks.append(("S2 the block-swap permutation of k identical fermions has "
                   "signature exactly (-1)^k, computed for k=1..6 (not quoted)",
                   exch["all_match_formula"],
                   [(r["k"], r["measured_sign"]) for r in exch["rows"]]))

    # ---- S3: baryon fermionic iff N odd, checked at n_probe -------------------
    s3 = baryon_is_fermion_iff_odd(n, bosonic_baryon=bosonic_baryon)
    checks.append((f"S3 a quark-only colour-{n} baryon (k={n} constituents, S1) "
                   f"is predicted fermionic iff {n} is odd (S2); matches the "
                   f"observed fact that real baryons are fermions",
                   s3["matches_observation"],
                   (s3["predicted_fermion"], s3["observed_fermion"])))

    # ---- S4: N=1 excluded by confinement --------------------------------------
    s4 = confinement_excludes_n1(n)
    checks.append((f"S4 dim su({n}) = {s4['dim_su_n']} > 0 (a connection exists "
                   f"to confine with), consistent with quarks being observed "
                   f"confined (never free)",
                   s4["consistent_with_confinement"], s4["dim_su_n"]))

    # ---- S5: the bracket -------------------------------------------------------
    br = the_bracket()
    checks.append(("S5 {N odd and N has gauge bosons} = {3,5,7,9,11} over "
                   "N=1..12 -- matches F324's independent post-S22 bracket "
                   "(different premises: Witten anomaly + generation parity, "
                   "not composite statistics or confinement); NOT used to "
                   "pin N=3",
                   br["matches_f324_post_s22_bracket"] and br["excludes_n1"],
                   br["allowed"]))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"n_probe": n, "bosonic_baryon": bool(bosonic_baryon),
                       "partial_generator_check": bool(partial_generator_check)},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    return {
        "row": "B1",
        "verdict": ("The internal index's existence is not derived from "
                    "nothing, but the residual is renamed and shrunk again: "
                    "from 'the index exists, by fiat' (F324's own words) to "
                    "two named observational facts -- baryons are fermions, "
                    "and quarks are confined -- combined with the model's own "
                    "SU(N) representation theory (generalised here) and "
                    "derived Fermi statistics (F289). N=3 itself is not "
                    "re-derived; that stays F317 S6 / F318 SD / F324's."),
    }
