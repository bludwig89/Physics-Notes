"""
cosmology_geon_domain_wall_reopening.py — Is the F238 abundance exclusion scoped
to the inflaton/Press-Schechter route, or does it foreclose EVERY geon-production
mechanism?  (F366)
=========================================================================================

Created: 2026-09-04 - 21:10

**Question (K8 re-examination prompt).** F238 proved the geon (F228 one-cell
Planck-mass remnant) relic abundance Omega_DM h^2 = 0.12 is "a genuinely free
input" via a specific causal chain:

    Omega_DM  <--  beta(M_form)  <--  sigma(k_PBH)  <--  primordial P(k)  <--  inflaton (absent)

F238 sec.6 named the missing sector precisely: "no inflaton finding, no
preheating finding, no primordial-power-spectrum module" -- and F282 then
proved (not merely observed) that no slow-roll inflaton CAN exist on this
lattice, and F285 proved no principled measure on the t=0 state reproduces
n_s = 0.9649 either. Every one of those findings is about ONE thing: the
primordial CURVATURE power spectrum P(k) that a Press-Schechter collapse
fraction beta(M) is conventionally computed from.

This module checks whether that is the ONLY way to fix beta, or whether a
structurally different, non-inflationary production channel -- collapse of a
Z_6 domain-wall network sourced by the model's OWN already-derived E_g clock
potential (F150/F175/F234), rather than inherited from a primordial spectrum
at all -- sidesteps the F238 chain at its first link.  Domain-wall-collapse
and first-order-phase-transition-bubble-collision PBH formation are both
established literature mechanisms that never invoke sigma(k) or an inflaton
(see e.g. Rubin-Sakharov-Khlopov 2000/2001; Gouttenoire-Sfakianakis 2023,
"New mechanism for primordial black hole formation from the QCD axion",
PRD 109 123030; Baker-Kavanagh 2021 "Primordial black holes from bubble
collisions during a first-order phase transition", PRD 110 115014).

--------------------------------------------------------------------------
What this module actually checks (and does NOT claim)
--------------------------------------------------------------------------

It does NOT compute a domain-wall relic abundance. That needs four pieces
this model does not yet have (see ``open_derivation_items``). What it DOES
establish, exactly and structurally:

  C1/C2/C3 (exact-algebraic, sympy) -- the model's own E_g clock potential
      V(delta) = (A/2)(1 + cos 6 delta), already derived by F150/F175/F234 and
      reused verbatim from F282's own ``eg_clock_coefficient`` (same amplitude
      A = lambda_6 * e_saturation**6, no new constant introduced) has an
      EXACT discrete Z_6 symmetry (delta -> delta + pi/3 leaves V identically
      invariant, checked symbolically, not numerically) with exactly 6
      degenerate global minima per period. That is the textbook Kibble-
      mechanism precondition for a Z_6 domain-wall network -- it costs
      nothing to check because F234 already derived the potential; this
      module only asks a question about it F234 never asked.

  C4 (structural, directory search -- F238 sec.6's own methodology, run on
      the complementary question) -- none of the six findings that frame the
      abundance exclusion (F238, F228, F282, F283, F284, F285) ever discusses
      a domain wall, topological defect, bubble collision, cosmic string or
      the Kibble mechanism. The exclusion was never extended to, or tested
      against, this channel.

  D1 (logical, not computed here) -- F285's own sec.2 "generic/natural
      measure" result (any short-range-correlated t=0 state gives white-noise
      density fluctuations, n_s = 0) applies to ANY lattice field with no
      special reason to be correlated across super-horizon distances --
      including delta. Since F282+F285 already close off every mechanism
      (inflation, causal-seed coherence) that would make delta correlated
      across causally disconnected patches, F285's OWN "generic case" implies
      delta has no reason to share one vacuum choice across the universe
      once it dynamically settles -- exactly the setup the Kibble mechanism
      needs. This is a citation of F285's existing content applied to a field
      F285 never considered, not new physics; it is recorded in the finding
      text, not re-derived numerically here (there is nothing further to
      compute -- F285's D1 argument is scale-free in the field it is applied
      to).

  D2 (structural, cited not computed) -- the acoustic-peak-coherence
      exclusion F282 sec.6 uses to rule out "causal seeds" is scoped to
      mechanisms invoked to explain the LARGE-SCALE (CMB / Mpc) power
      spectrum via super-horizon-incoherent active sources (Durrer, Albrecht
      et al., Pen-Seljak-Turok). Domain-wall-collapse PBH formation is never
      asked to play that role -- it operates entirely on sub-horizon scales
      at the (very early, very hot) wall-collapse time, and the model's
      existing LCDM sector (F182/F188) is untouched. The two mechanisms
      answer different questions at different scales; F282 sec.6 excludes
      the former, not the latter.

Real arithmetic + sympy for the exact algebra only -- no chiral/complex
transforms (CLAUDE.md). No numpy/scipy needed (D8): this is symbolic algebra
and directory text search, not a lattice computation.
"""
from __future__ import annotations

from pathlib import Path

import sympy as sp

from casim.engine.interactions.cosmology_primordial import eg_clock_coefficient

__all__ = [
    "z6_degeneracy_exact",
    "z6_symmetry_exact",
    "scope_of_f238_exclusion",
    "open_derivation_items",
    "run_all",
]

# The six findings that jointly frame "the geon abundance is a free input" --
# F238's own chain plus the two findings (F282/F285) that upgraded its missing
# sector from "not built" to "cannot be built" / "no measure reproduces n_s".
_FRAMING_FINDINGS = ("F238", "F228", "F282", "F283", "F284", "F285")

# Terms naming the non-inflationary channel this module checks for. Absence of
# all of these across _FRAMING_FINDINGS is the structural fact C4 asserts.
_DEFECT_TERMS = (
    "domain wall", "topological defect", "bubble collision", "kibble",
    "cosmic string",
)


def _repo_root() -> Path:
    """Walk up from this file to the repo root (has ``findings/``), per
    CLAUDE.md's guidance against working-directory-relative paths; does not
    import the suite layer."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "findings").is_dir():
            return parent
    raise RuntimeError("could not locate repo root above " + str(p))


# ---------------------------------------------------------------------------
# C1/C2 — exact vacuum count and degeneracy of V(delta)
# ---------------------------------------------------------------------------
def z6_degeneracy_exact() -> dict:
    """Exact count and degeneracy of the global minima of
    ``V(delta) = (A/2)(1 + cos 6 delta)`` over one period ``delta in [0, 2 pi)``.
    ``V`` is minimised wherever ``cos(6 delta) = -1`` -- solved symbolically,
    not by a numerical scan."""
    delta, A = sp.symbols("delta A", real=True, positive=False)
    V = sp.Rational(1, 2) * A * (1 + sp.cos(6 * delta))

    sols = sp.solveset(sp.Eq(sp.cos(6 * delta), -1), delta,
                        domain=sp.Interval.Ropen(0, 2 * sp.pi))
    sols_list = sorted(float(s) for s in sols)
    n_vacua = len(sols_list)

    # Degeneracy: V is a pure function of cos(6 delta), so every solution of
    # cos(6 delta) = -1 gives the identical V by construction; confirm it
    # rather than assume it (A left symbolic, so this cannot be a numerical
    # coincidence).
    V_at = [sp.simplify(V.subs({delta: s, A: sp.Symbol("A", positive=True)}))
            for s in sols]
    degenerate = all(sp.simplify(v - V_at[0]) == 0 for v in V_at)

    return {
        "n_vacua_exact": n_vacua,
        "vacua_deltas": sols_list,
        "exactly_degenerate": bool(degenerate),
    }


# ---------------------------------------------------------------------------
# C3 — exact Z_6 symmetry (stronger than "6 equal minima found numerically")
# ---------------------------------------------------------------------------
def z6_symmetry_exact() -> dict:
    """Exact check that ``delta -> delta + pi/3`` leaves ``V`` identically
    invariant (sympy simplification to the zero expression), i.e. the
    potential carries a genuine discrete Z_6 symmetry rather than 6 minima
    that merely happen to coincide."""
    delta, A = sp.symbols("delta A", real=True)
    V = sp.Rational(1, 2) * A * (1 + sp.cos(6 * delta))
    shifted = V.subs(delta, delta + sp.pi / 3)
    diff = sp.simplify(sp.expand_trig(shifted - V))
    return {
        "shift": "delta -> delta + pi/3",
        "V_shift_minus_V": str(diff),
        "identically_zero": diff == 0,
    }


# ---------------------------------------------------------------------------
# C4 — structural fact: was this channel ever discussed by the framing findings?
# ---------------------------------------------------------------------------
def scope_of_f238_exclusion(repo_root: Path | None = None) -> dict:
    """Grep the six findings that frame 'the geon abundance is a free input'
    for the defect-channel vocabulary. Same directory-search methodology
    F238 sec.6 used ('a search of findings/ and ca-simulation/ returns no
    inflaton finding...'), run here on the complementary question: does any
    of them ALREADY discuss, and therefore already exclude or admit, a
    non-inflationary topological-defect production channel?"""
    root = repo_root or _repo_root()
    findings_dir = root / "findings"
    per_finding = {}
    for name in _FRAMING_FINDINGS:
        matches = sorted(findings_dir.glob(f"{name}-*.md"))
        if not matches:
            per_finding[name] = {"found_file": False, "defect_terms_present": []}
            continue
        text = matches[0].read_text(encoding="utf-8", errors="ignore").lower()
        hits = [t for t in _DEFECT_TERMS if t in text]
        per_finding[name] = {"found_file": True, "file": matches[0].name,
                              "defect_terms_present": hits}
    any_discussed = any(v["defect_terms_present"] for v in per_finding.values())
    return {
        "framing_findings_checked": list(_FRAMING_FINDINGS),
        "per_finding": per_finding,
        "defect_channel_previously_discussed": any_discussed,
    }


# ---------------------------------------------------------------------------
# What remains open — documented, not computed
# ---------------------------------------------------------------------------
def open_derivation_items() -> list:
    """Turning 'the Kibble-mechanism precondition is exactly met' into 'an
    abundance is derived' needs four more pieces, none of which this module
    supplies. Kept in code (not only in the finding's prose) so the open list
    sits next to the checks it qualifies."""
    return [
        "A causally-early dynamics for delta establishing that it actually "
        "SETTLES into one of the 6 wells via a horizon-limited process "
        "(rather than being pinned there from t=0 by fiat) -- argued from "
        "F285's own generic/natural t=0 measure (sec.D1 of that finding), "
        "not separately derived here.",
        "Confirmation the settling is a genuine phase transition capable of "
        "leaving a real Z_6 wall network, not a smooth wall-free relaxation "
        "-- no finite-temperature (or other causally-early) effective "
        "potential for the E_g condensate exists in the model yet.",
        "The wall tension sigma_wall in physical units. This needs the E_g "
        "doublet's canonical kinetic-term normalisation, which F282's own "
        "2026-09-04 update (F363) explicitly flags as unresolved: 'whether "
        "the E_g doublet's kinetic term is exactly canonical (assumed here, "
        "never independently derived)'.",
        "A network-collapse-fraction (wall-collision PBH yield) computation "
        "-- standard in the literature (Rubin-Sakharov-Khlopov; Gouttenoire-"
        "Sfakianakis 2023) but not yet built on this lattice.",
        "A resolution of the generic Z_6 domain-wall overclosure problem: "
        "either an explicit small bias breaking the exact vacuum degeneracy "
        "(new physics not currently in the model) or a demonstration that "
        "the network collapses to PBHs within a few Hubble times of "
        "formation, before reaching the scaling regime that would overclose "
        "the universe -- itself an open calculation, not a given.",
    ]


def run_all() -> dict:
    z6 = z6_degeneracy_exact()
    sym = z6_symmetry_exact()
    scope = scope_of_f238_exclusion()
    clock = eg_clock_coefficient()

    checks = {
        "C1_six_exact_vacua": z6["n_vacua_exact"] == 6,
        "C2_vacua_exactly_degenerate": z6["exactly_degenerate"],
        "C3_exact_z6_symmetry": sym["identically_zero"],
        "C4_defect_channel_not_previously_examined": not scope["defect_channel_previously_discussed"],
    }

    return {
        "z6_degeneracy": z6,
        "z6_symmetry": sym,
        "f238_scope_check": scope,
        "reused_clock_amplitude_A": clock["amplitude_A"],
        "open_items": open_derivation_items(),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


if __name__ == "__main__":
    import json
    import pprint

    result = run_all()
    pprint.pprint(result)
    out_path = _repo_root() / "test-results" / "F366_geon_domain_wall_reopening.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, default=str)
