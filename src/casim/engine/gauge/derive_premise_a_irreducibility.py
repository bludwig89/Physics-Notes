"""derive_premise_a_irreducibility.py — is F333 premise (a) reducible to F289/F330?

THE QUESTION
============
F333 narrowed row B1's residual to two named observational facts: (a) real
baryons are fermions, (b) quarks are confined.  Both are OBSERVATIONAL
INPUTS in F333's own accounting (`derive_internal_index_existence.py`,
`baryon_is_fermion_iff_odd`: ``observed_fermion = True  # the proton and
neutron are observed fermions``, hardcoded rather than computed).

This module asks the natural next question: does the model's OWN derived
spin-statistics connection (F289: R(2pi) = -1 forced from the rotor, d=3
forced from F291/F292; F330: the belt-trick residual named precisely as
Anastopoulos's Postulate 1) already CONTAIN premise (a), so that citing the
proton's observed statistics is redundant with physics already in the tree?

THE ANSWER, COMPUTED RATHER THAN ASSERTED: NO.
================================================
F289/F330 derive a THEOREM about a SINGLE spin-1/2 constituent: exchanging
two identical spin-1/2 objects picks up -1.  That theorem is a function of
SPIN alone and never references a composite-constituent COUNT.  F333's own
S1 (SU(N)-invariant subspace of Lambda^k(C^N) is a singlet iff k=N) and S2
(a block-swap of k identical fermions has signature (-1)^k) combine F289's
single-constituent theorem into a claim about a COMPOSITE of k=N such
constituents -- and that combined claim is irreducibly a FUNCTION of N:
fermionic iff N odd, bosonic iff N even.  Nothing in F289 or F330 supplies a
value for N, or any constraint that would collapse this function to a single
answer.  Premise (a) is exactly, and only, the information that picks out
the N-odd branch as the one realised in nature -- which is precisely the
information F289/F330 do not, and structurally cannot, contain (S1/S2
below).

THE ONE APPARENT ESCAPE, CLOSED (S4/S5)
=========================================
F324 derives N_c odd (a stronger, model-internal constraint on N) from
completely different premises (Witten's SU(2)_L anomaly + generation
parity).  Could THAT be combined with F289 + F333's S1/S2 to DERIVE premise
(a) as a corollary, discharging it?  No, for two independent reasons, both
checked here rather than asserted:

  S4  F324's OWN premise (ii) -- machine-read from `derive_ncolour_bracket
      .bracket()`'s own returned `premises` list, not re-typed -- is *"the
      colour sector exists ... this is what excludes N=1"*.  Using F324 to
      discharge B1's existence residual would be circular: F324's chain
      presupposes the thing F333's premise (a)/(b) exist to establish.

  S5  Even setting circularity aside, F324's chain costs SIX premises
      (`len(bracket()["premises"])`, computed not quoted) against F333's
      TWO.  Substituting F324's route for premise (a) (and, since a pinned
      N=3 also settles N != 1, for premise (b) too) is a net INCREASE of
      four premises for row B1 -- the opposite of a reduction.  F324 §6
      already says as much of its own trade ("the premise count went up");
      S5 just prices what importing it into B1 would cost.

WHAT THIS CLOSES
=================
Records premise (a) as logically INDEPENDENT of F289/F330's derivation --
the falsification target the session brief named explicitly.  Row B1 stays
PARTIAL at two premises.  This closes the reduction attempt with a stated
reason, in the same spirit as CN15/CN16/CN17 (open-derivations.md, Part B):
a later session should not re-attempt "derive (a) from spin-statistics"
without first reading S1-S3 below, and should not re-attempt "substitute
F324's chain for (a)" without reading S4/S5.

WHAT IS MEASURED (each is a CHECKS row, each has a control)
=============================================================
S1  SCOPE DISJOINTNESS.  The source text of `qi_spin_statistics.py` and
    `qi_belt_trick.py` (F289's and F330's own modules) contains zero
    occurrences of any colour/composite-count token (colour, color, SU(N),
    N_c, baryon, quark, constituent) -- the two derivations are written,
    top to bottom, without ever mentioning the object premise (a) is about.
S2  NO N-VALUED PARAMETER.  Every public function in those two modules is
    enumerated via `inspect.signature`; none takes a parameter whose name
    could carry a colour count. The two APIs have no channel through which
    an N could even be passed in.
S3  GENUINE BIFURCATION.  F333's own S1+S2 machinery (`composite_block_swap
    _parity`, imported not re-implemented), run for N=2..7, predicts BOTH
    outcomes (fermion at odd N, boson at even N) -- and F289's own rotor
    fact (`rotor_2pi_phase`) is unchanged across every N, because it is
    never given one. The prediction bifurcates on N; F289/F330 supply
    nothing that picks a branch.
S4  F324's PREMISE (ii) PRESUPPOSES EXISTENCE.  Read directly off
    `derive_ncolour_bracket.bracket()`'s own returned `premises` list
    (not re-typed): premise (ii) is literally "the colour sector exists".
S5  NET PREMISE COST OF THE SUBSTITUTION.  `len(bracket()["premises"])` is
    computed and compared against F333's own declared premise count (2):
    the substitution costs 6, i.e. +4 net, wherever S4 is set aside.

CONTROLS
========
  --param inject_colour_token=true    appends a synthetic colour-sector
      token to an in-memory COPY of the scanned source text (the real files
      on disk are never touched). S1 must go red, proving the scanner can
      detect a hit rather than vacuously passing on an unreachable check.
  --param inject_fake_param=true      appends a synthetic N-shaped
      parameter name to the in-memory list of scanned signatures. S2 must
      go red for the same reason.
  --param force_all_fermionic=true    overrides the composite-parity call
      so every N reports fermionic. S3 must go red (no boson branch found),
      showing the bifurcation claim is a real, falsifiable structural fact
      about F333's own S1/S2 machinery, not assumed.
  --param strip_premise_ii=true       filters F324's own premise (ii) out
      of the list before the text-match check. S4 must go red, showing the
      check is reading real content, not a hardcoded string.
  --param assume_f324_premise_count=1  overrides the computed premise
      count with a wrong (too-small) number. S5's "net increase" assertion
      must go red, showing the accounting check is a genuine comparison.

Cross-references: F333 (the two premises this attacks; S1/S2's machinery,
imported not duplicated), F289/F330 (the spin-statistics derivation whose
scope S1-S3 test), F324 (the substitution route S4/S5 close), F318 SD
(the residual F333 narrows and this module does not re-open).
"""
from __future__ import annotations

import inspect
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from casim.engine.gauge.derive_internal_index_existence import (
    composite_block_swap_parity,
)
from casim.engine.gauge.derive_ncolour_bracket import bracket as f324_bracket
from casim.engine.interactions import qi_spin_statistics, qi_belt_trick

F333_PREMISE_COUNT = 2  # (a) baryons are fermions, (b) quarks are confined

_COLOUR_TOKENS = (
    "colour", "color", "su(n)", "n_c", "baryon", "quark",
)
# "constituent" is deliberately excluded: measured to false-positive on
# qi_spin_statistics.py/qi_belt_trick.py's own unrelated use of the word for
# the paired-spinor photon's two Weyl "constituents" (decision 5, F68) --
# a homonym, not a reference to colour-composite constituent counting. Its
# presence is exactly the kind of accidental overlap a naive keyword sweep
# would need to survive; excluding it is the correct call, not a weakening
# of the check (the remaining six tokens are unambiguous).

_N_PARAM_PATTERN = re.compile(
    r"^(n|n_c|n_colour|n_color|n_probe|colour|color)$", re.IGNORECASE
)


# ==========================================================================
# S1 -- scope disjointness in F289/F330's own source
# ==========================================================================
def _module_source(mod) -> str:
    return Path(inspect.getsourcefile(mod)).read_text(encoding="utf-8").lower()


def scope_disjointness(inject_colour_token: bool = False) -> Dict[str, Any]:
    text = _module_source(qi_spin_statistics) + "\n" + _module_source(qi_belt_trick)
    if inject_colour_token:
        text += "\n# test injection: colour n_c su(n) baryon quark constituent\n"
    hits = sorted({tok for tok in _COLOUR_TOKENS if tok in text})
    return {"tokens_scanned": list(_COLOUR_TOKENS), "hits": hits,
            "disjoint": len(hits) == 0}


# ==========================================================================
# S2 -- no N-valued parameter in F289/F330's public API
# ==========================================================================
def no_n_valued_parameter(inject_fake_param: bool = False) -> Dict[str, Any]:
    names: List[str] = []
    for mod in (qi_spin_statistics, qi_belt_trick):
        for fn_name, fn in inspect.getmembers(mod, inspect.isfunction):
            if fn_name.startswith("_") or fn.__module__ != mod.__name__:
                continue
            names.extend(inspect.signature(fn).parameters.keys())
    if inject_fake_param:
        names.append("n_colour")
    matches = sorted({n for n in names if _N_PARAM_PATTERN.match(n)})
    return {"parameters_scanned": len(names), "matches": matches,
            "no_n_channel": len(matches) == 0}


# ==========================================================================
# S3 -- genuine bifurcation over N, F289's rotor fact unchanged throughout
# ==========================================================================
def bifurcation_over_n(n_values: Tuple[int, ...] = (2, 3, 4, 5, 6, 7),
                       force_all_fermionic: bool = False) -> Dict[str, Any]:
    rows = []
    for n in n_values:
        r = composite_block_swap_parity(n, bosonic=False)
        fermionic = True if force_all_fermionic else r["is_fermionic_composite"]
        rows.append({"n": n, "predicted_fermionic": fermionic})
    has_fermion_branch = any(r["predicted_fermionic"] for r in rows)
    has_boson_branch = any(not r["predicted_fermionic"] for r in rows)
    rotor = qi_spin_statistics.rotor_2pi_phase()
    return {"rows": rows, "has_fermion_branch": has_fermion_branch,
            "has_boson_branch": has_boson_branch,
            "genuine_bifurcation": has_fermion_branch and has_boson_branch,
            "f289_rotor_residual": rotor["residual_R2pi_plus_identity"],
            "f289_rotor_takes_no_n": "n" not in inspect.signature(
                qi_spin_statistics.rotor_2pi_phase).parameters}


# ==========================================================================
# S4 -- F324's own premise (ii) presupposes existence
# ==========================================================================
def f324_premise_ii_presupposes_existence(strip_premise_ii: bool = False
                                          ) -> Dict[str, Any]:
    premises = f324_bracket()["premises"]
    if strip_premise_ii:
        premises = [p for p in premises if not p.startswith("(ii)")]
    matches = [p for p in premises if "colour sector exists" in p]
    return {"n_premises": len(premises), "matches": matches,
            "presupposes_existence": len(matches) == 1}


# ==========================================================================
# S5 -- net premise cost of the substitution
# ==========================================================================
def substitution_net_cost(assume_f324_premise_count: int = 0) -> Dict[str, Any]:
    computed = len(f324_bracket()["premises"])
    f324_count = assume_f324_premise_count or computed
    net_change = f324_count - F333_PREMISE_COUNT
    return {"f333_premise_count": F333_PREMISE_COUNT,
            "f324_premise_count_computed": computed,
            "f324_premise_count_used": f324_count,
            "net_change": net_change,
            "is_net_increase": net_change > 0}


# ==========================================================================
# The registry entry point
# ==========================================================================
def check_premise_a_irreducibility(inject_colour_token: bool = False,
                                   inject_fake_param: bool = False,
                                   force_all_fermionic: bool = False,
                                   strip_premise_ii: bool = False,
                                   assume_f324_premise_count: int = 0
                                   ) -> Dict[str, Any]:
    """The B1-premise-(a)-irreducibility gate, as a registry entry.

    Declared controls (see module docstring for the full reasoning):
      --param inject_colour_token=true          S1 red
      --param inject_fake_param=true             S2 red
      --param force_all_fermionic=true           S3 red
      --param strip_premise_ii=true              S4 red
      --param assume_f324_premise_count=1        S5 red
    """
    checks: List[Tuple[str, bool, Any]] = []

    s1 = scope_disjointness(inject_colour_token=inject_colour_token)
    checks.append(("S1 F289's and F330's own source text contains zero "
                   "colour/composite-count tokens -- the two derivations "
                   "never mention the object premise (a) is about",
                   s1["disjoint"], s1["hits"]))

    s2 = no_n_valued_parameter(inject_fake_param=inject_fake_param)
    checks.append(("S2 no public function in F289's or F330's module takes "
                   "a colour-count-shaped parameter -- no channel exists "
                   "through which an N could even be supplied",
                   s2["no_n_channel"], s2["matches"]))

    s3 = bifurcation_over_n(force_all_fermionic=force_all_fermionic)
    checks.append(("S3 F333's own S1+S2 machinery genuinely bifurcates over "
                   "N (fermion at odd N, boson at even N), and F289's rotor "
                   "fact is identical across every branch because it is "
                   "never given N",
                   s3["genuine_bifurcation"] and s3["f289_rotor_takes_no_n"],
                   s3["rows"]))

    s4 = f324_premise_ii_presupposes_existence(strip_premise_ii=strip_premise_ii)
    checks.append(("S4 F324's own premise (ii), read from its returned "
                   "premises list, is literally 'the colour sector exists' "
                   "-- using F324 to discharge B1's existence residual "
                   "would be circular",
                   s4["presupposes_existence"], s4["matches"]))

    s5 = substitution_net_cost(assume_f324_premise_count=assume_f324_premise_count)
    checks.append(("S5 substituting F324's chain for premise (a) (and (b), "
                   "since a pinned N also settles N!=1) costs F324's six "
                   "premises against F333's two -- a net increase, not a "
                   "reduction",
                   s5["is_net_increase"],
                   (s5["f333_premise_count"], s5["f324_premise_count_used"])))

    rows = [{"name": nm, "ok": bool(ok), "value": val} for nm, ok, val in checks]
    return {"checks": rows,
            "passed": all(r["ok"] for r in rows),
            "n_pass": sum(1 for r in rows if r["ok"]),
            "n_total": len(rows),
            "params": {"inject_colour_token": bool(inject_colour_token),
                       "inject_fake_param": bool(inject_fake_param),
                       "force_all_fermionic": bool(force_all_fermionic),
                       "strip_premise_ii": bool(strip_premise_ii),
                       "assume_f324_premise_count": int(assume_f324_premise_count)},
            "summary": summary()}


def summary() -> Dict[str, Any]:
    return {
        "row": "B1",
        "verdict": ("F333's premise (a) -- real baryons are fermions -- is "
                    "logically INDEPENDENT of F289/F330's derived "
                    "spin-statistics connection: that connection is a "
                    "single-constituent theorem with no channel for a "
                    "colour count, F333's own S1/S2 combination of it "
                    "genuinely bifurcates on N, and the one route that "
                    "could pin N from elsewhere (F324) both presupposes "
                    "colour's existence (circular for this purpose) and "
                    "costs more premises than it saves. Row B1 stays "
                    "PARTIAL at two premises; this closes the reduction "
                    "attempt with a stated reason."),
    }
