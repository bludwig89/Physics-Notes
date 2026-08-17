#!/usr/bin/env python3
"""Land the doc-ledger half of F279 follow-up 1.

The code half is three files (already written):

    src/casim/constants/electroweak.py                  Y_LEPTON_L / Y_E_R / Y_NU_R
    src/casim/engine/gauge/hypercharge.py               literals -> imports
    tests/findings/test_F279_hypercharge_attribution.py new gate check

This script does the paper trail, because five documents currently assert that
the follow-up is unactioned:

  1. findings/F279-...md            sections 8 and 9
  2. docs/theory/supersessions.yaml S13's code: note
  3. docs/status/completeness-2026-08-04.md  the H5 "one live contradiction"
  4. docs/roadmaps/next-steps-pt2.md the working bullet
  5. docs/status/changelog.md        a new entry, appended
  6. tests/registry/gauge.yaml       the F279 record's human-owned notes

Every edit is an exact-string replacement with an occurrence-count assertion,
so it either lands on the text it was written against or refuses. Nothing is
edited unless every replacement matches (checked first, written second).

    python3 tools/apply_F279_followup_docs.py            # from the repo root
    python3 apply_F279_followup_docs.py --repo /path/to/repo
    python3 apply_F279_followup_docs.py --check          # verify only

After it runs: `make indexes && make gate`, then replace the changelog's
pending-gate line with the actual result.
"""
from __future__ import annotations

import argparse
import os
import sys

# --------------------------------------------------------------------------
# 1. findings/F279 — section 8 "In the code." and section 9 follow-up 1
# --------------------------------------------------------------------------
F279 = "findings/F279-hypercharge-constraint-attribution.md"

F279_CODE_OLD = (
    "**In the code.** `hypercharge.py` still writes `Y_LEPTON_L`, `Y_E_R`, "
    "`Y_NU_R` as literals under a comment calling them SM values. They are "
    "derived values and should be registry constants with F279/F165 provenance. "
    "**Not done here** — this finding touches no module, and the "
    "constants-registry change is a separate, testable edit. Logged as the open "
    "follow-up."
)
F279_CODE_NEW = F279_CODE_OLD + (
    "\n\n**Update 2026-08-06 — done.** The three are `casim.constants` entries "
    "in the `electroweak` sector (`Y_LEPTON_L`, `Y_E_R`, `Y_NU_R`), and "
    "`hypercharge.py` imports them. The registry does not record them as three "
    "equally derived numbers, because they are not: `Y_NU_R = 0` is forced "
    "outright by the §4 Majorana row with no normalisation freedom; "
    "`Y_E_R = 2·Y_LEPTON_L` is derived and, by §5, holds for every $N_c$; and "
    "`Y_LEPTON_L = -1` **is** the residual normalisation this finding names — "
    "exact because it is a choice of unit, not because it was computed. `Y_E_R` "
    "resolves *from* `Y_LEPTON_L` in the registry rather than being typed as "
    "$-2$ (C2.1), so the derived ratio cannot drift away from the unit it "
    "depends on."
)

F279_FU_OLD = (
    "1. Promote the three hypercharge literals in "
    "`casim.engine.gauge.hypercharge` to `casim.constants` entries with "
    "`provenance: F165, F279` and `exactness: exact`, with `Site(...)` records. "
    "Until then the code and the finding disagree in the direction the register "
    "just stopped disagreeing."
)
F279_FU_NEW = (
    "1. ~~Promote the three hypercharge literals in "
    "`casim.engine.gauge.hypercharge` to `casim.constants` entries with "
    "`provenance: F165, F279` and `exactness: exact`, with `Site(...)` "
    "records.~~ **Done 2026-08-06.** Registered in the `electroweak` sector "
    "with `Site(...)` records for the module (`kind='import'`) and for "
    "`forks/electroweak/hypercharge_fork.py` (`kind='reexport'`), and guarded "
    "by `check_registry_values_are_on_the_derived_line` in this finding's own "
    "gate record — which solves the §4 system and reads the normalisation back "
    "out of the registry, so a value that drifts off this line fails the gate "
    "rather than merely disagreeing with prose.\n\n"
    "   The **quark** hypercharges stay in `hypercharge.py` on purpose, and the "
    "reason is §5: their *fractions* are quantisation plus $N_c = 3$, so "
    "registering them as `exact` on F165/F279 provenance would launder an "
    "underived input into a derived one. (There is a second, mechanical reason "
    "recorded at the site: $1/3$, $4/3$ and $-2/3$ are diagnostic values, so "
    "the C2.4 sweep cannot exclude them, and registering them would flag every "
    "unrelated third in `src/`.) Promoting them is blocked on follow-up 2, not "
    "on bookkeeping."
)

# --------------------------------------------------------------------------
# 2. supersessions.yaml — S13's code: note is now false
# --------------------------------------------------------------------------
SUP = "docs/theory/supersessions.yaml"

SUP_OLD = """      - path: src/casim/engine/gauge/hypercharge.py
        note: >
          UNCHANGED by this record, and now the remaining inconsistency: lines
          117-121 still write Y_LEPTON_L / Y_E_R / Y_NU_R as literals under a
          comment calling them SM values. They are derived values (F165+F279)
          and belong in casim.constants with that provenance. Logged as F279's
          open follow-up 1.
"""
SUP_NEW = """      - path: src/casim/engine/gauge/hypercharge.py
        note: >
          RECONCILED 2026-08-06 (F279 follow-up 1). Was: lines 117-121 wrote
          Y_LEPTON_L / Y_E_R / Y_NU_R as literals under a comment calling them
          SM values, which contradicted this record. They are now imported from
          casim.constants (electroweak sector) with F165+F279 provenance, and
          the registry keeps the three distinct: Y_NU_R = 0 forced by the F47
          Majorana row, Y_E_R = 2*Y_LEPTON_L derived and N_c-independent, and
          Y_LEPTON_L = -1 the residual normalisation. The quark hypercharges
          remain literals here deliberately -- their fractions carry the
          underived N_c = 3 (F279 A3), so registering them as exact would
          launder an input. No number moved.
"""

# --------------------------------------------------------------------------
# 3. completeness-2026-08-04 — a dated snapshot, so annotate, do not rewrite
# --------------------------------------------------------------------------
COMP = "docs/status/completeness-2026-08-04.md"

COMP_OLD = """F279 follow-up 1, unactioned. This is the one live code-vs-finding contradiction in H5."""
COMP_NEW = """F279 follow-up 1, unactioned. This is the one live code-vs-finding contradiction in H5.

> **Update 2026-08-06 — closed.** The three are `casim.constants` entries (`electroweak` sector,
> F165+F279 provenance) and `hypercharge.py` imports them; the F279 gate record gained
> `check_registry_values_are_on_the_derived_line`, which re-solves the six-row system and reads the
> normalisation back out of the registry. The grade above is left as the 2026-08-04 snapshot read it.
> What is *not* closed: the quark hypercharges are still literals, because their fractions carry the
> underived $N_c = 3$ (F279 A3) — that is B10's problem, not H5's."""

# --------------------------------------------------------------------------
# 4. next-steps-pt2 — the working bullet
# --------------------------------------------------------------------------
NEXT = "docs/roadmaps/next-steps-pt2.md"

NEXT_OLD = """- ~~hypercharge.py writes Y_LEPTON_L = -1, Y_E_R = -2, Y_NU_R = 0 as literals under a comment reading "SM hypercharge assignment". They are derived (F165, re-derived by F279) and belong in casim.constants with provenance. F279 follow-up 1, unactioned.~~"""
NEXT_NEW = """- ~~hypercharge.py writes Y_LEPTON_L = -1, Y_E_R = -2, Y_NU_R = 0 as literals under a comment reading "SM hypercharge assignment". They are derived (F165, re-derived by F279) and belong in casim.constants with provenance. F279 follow-up 1, unactioned.~~ **Done 2026-08-06** — registered in the electroweak sector (Y_E_R resolves from Y_LEPTON_L; Y_NU_R forced by the F47 Majorana row; Y_LEPTON_L is the residual normalisation), module imports them, F279's gate record now checks the values against the derived line. Quark hypercharges deliberately left as literals: their fractions carry the underived N_c = 3, so that promotion belongs to the "why three colours" item, not this one."""

# --------------------------------------------------------------------------
# 5. tests/registry/gauge.yaml — the F279 record's human-owned notes
# --------------------------------------------------------------------------
REG = "tests/registry/gauge.yaml"

REG_OLD = """    that the public register states: if the grav row ever becomes independent again, or the Majorana row
    stops closing the system, the derived status of charge quantisation has changed and the register is
    wrong again.'"""
REG_NEW = """    that the public register states: if the grav row ever becomes independent again, or the Majorana row
    stops closing the system, the derived status of charge quantisation has changed and the register is
    wrong again.

    2026-08-06, F279 follow-up 1: sixth check added, check_registry_values_are_on_the_derived_line.
    It re-solves the six-row system and asserts casim.constants Y_LEPTON_L / Y_E_R / Y_NU_R sit on
    that line, reading the normalisation back out of the registry rather than assuming y_Q = 1/6, and
    asserts casim.engine.gauge.hypercharge imports them instead of writing its own. This is the check
    that keeps the code and the register from drifting apart again -- the contradiction F279 section 8
    logged and could not fix in-finding. It is the only check in this record that imports casim.'"""

# --------------------------------------------------------------------------
# 6. changelog — appended
# --------------------------------------------------------------------------
CHANGELOG = "docs/status/changelog.md"

CHANGELOG_ENTRY = """
## 2026-08-06 — F279 follow-up 1: the lepton hypercharges are registry constants, and the code stops calling them the Standard Model's

**The one live code-vs-finding contradiction in the model is closed, and no number moved.** F279 (2026-08-02) rewrote the public register to say that hypercharge quantisation **is** derived — one normalisation, not five values, is the residual input — and recorded that `src/casim/engine/gauge/hypercharge.py:117-121` still wrote `Y_LEPTON_L = -1`, `Y_E_R = -2`, `Y_NU_R = 0` as literals under a comment reading *"SM hypercharge assignment"*. Both the finding's own follow-up 1 and `completeness-2026-08-04` (H5) carried it as unactioned. The three are now `casim.constants` entries in the `electroweak` sector with `provenance: (F165, F279)` and `exactness: exact`, and the module imports them.

**The registry does not flatten them into "the SM values", because they are not equally derived** — and recording that split is most of the value of the promotion. `Y_NU_R = 0` is forced outright, with no normalisation freedom, by the F47 Majorana bilinear ($2y_\\nu = 0$); that is the row F279 A2 showed actually closes the system, in place of the $[\\text{grav}]^2U(1)$ row F165 credited. `Y_E_R = 2\\,Y_\\text{LEPTON L}$ is derived and **$N_c$-independent** — F279 A3 gives $y_L : y_e = -N_c : -2N_c$ for every colour multiplicity — and it *resolves from* `Y_LEPTON_L` in the registry rather than being typed as $-2$ (C2.1), so the derived ratio cannot drift away from the unit it depends on. `Y_LEPTON_L = -1` **is** the residual: the unit of charge, the F49 question, exact because it is a choice of unit and not because it was computed. Provenance for the third is `(F279, F47, F266)`, since F266 records the same $Y = 0$ as structurally forced.

**The quark hypercharges are deliberately NOT registered, and the reason is physics, not scope.** `Y_QUARK_L`, `Y_U_R`, `Y_D_R` sit on the same solution line, but F279 A3 is explicit that their *fractions* are quantisation **plus** $N_c = 3$, and $N_c = 3$ is underived (F293 grades "why three colours" PARTIAL). Registering them as `exact` on F165/F279 provenance would launder an input into an output — the exact failure mode F279 was written to correct. A second, mechanical reason is recorded at the site: $1/3$, $4/3$ and $-2/3$ are diagnostic values, so `sweep=False` is unavailable to them and the C2.4 sweep would flag every unrelated third in `src/`. Both reasons are now comments in `hypercharge.py` where the literals live, so the next reader does not re-open the question blind.

**Guarded, not just moved.** `tests/findings/test_F279_hypercharge_attribution.py` gains a sixth check, `check_registry_values_are_on_the_derived_line`: it re-solves the six-row system over $\\mathbb{Q}$, computes the unit **from the registry's own `Y_LEPTON_L`** rather than assuming $y_Q = 1/6$ (so the assertion tests the derived ratios, not the free normalisation), asserts $Y = 2y$ on that line for all three, asserts `exactness == "exact"` and `F279 in provenance`, and asserts the engine module's names are the registry's and that the mass-step phases still come out $\\Delta Y_e = +1$, $\\Delta Y_\\nu = -1$ exactly. A value that drifts off the F279 line now fails a gate instead of merely disagreeing with prose. `Site` records: `kind='import'` for the module and `kind='reexport'` for `forks/electroweak/hypercharge_fork.py`; all three declare `sweep=False` with reasons (the values are $-1$, $-2$ and $0$ — the sweep-exclusion gate requires them to be undiagnostic, and they are).

**Behaviour is unchanged by construction.** The module keeps both faces per the C2 rule — the exact `Fraction` under the registry symbol for the rational algebra, `*_f` for the numpy phase factors — and the function defaults that used the int literals now use the float faces, so every F41 (Y1-Y7) and F42 (Y8-Y15) residual is arithmetically identical. `DELTA_Y_E` / `DELTA_Y_NU` stay computed in the module, not registered: they are the *differences* the F41 mass step absorbs, and F279's $y_\\phi = 3y_Q$ row is what makes them $\\pm 1$.

**Gate:** _pending — run `make constants` (registry integrity, import-site verification, C2.4 sweep at `rogue_gate` 0), `python3 tools/audit_constants.py --ratchet`, `casim test --tier gate --finding F279`, and `pytest tests/findings/test_hypercharge.py tests/findings/test_hypercharge_extension.py`, then replace this line with the result._ Docs updated: F279 sections 8-9, `supersessions.yaml` S13's `code:` note (which asserted the contradiction was still live), `completeness-2026-08-04` H5 (annotated, not rewritten — it is a dated snapshot), `next-steps-pt2`, and the F279 registry record's notes. `make registry-gen` will refresh that record's `evidence.lines` / check count.
"""

REPLACEMENTS = [
    (F279, F279_CODE_OLD, F279_CODE_NEW),
    (F279, F279_FU_OLD, F279_FU_NEW),
    (SUP, SUP_OLD, SUP_NEW),
    (COMP, COMP_OLD, COMP_NEW),
    (NEXT, NEXT_OLD, NEXT_NEW),
    (REG, REG_OLD, REG_NEW),
]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=".", help="repo root (default: cwd)")
    ap.add_argument("--check", action="store_true",
                    help="verify every target string is present; write nothing")
    args = ap.parse_args(argv)
    repo = os.path.abspath(args.repo)

    # ---- verify everything first; a half-applied paper trail is worse than none
    sources: dict[str, str] = {}
    problems: list[str] = []
    for rel, old, _new in REPLACEMENTS:
        full = os.path.join(repo, rel)
        if rel not in sources:
            if not os.path.exists(full):
                problems.append(f"{rel}: file not found")
                sources[rel] = ""
                continue
            sources[rel] = open(full, encoding="utf-8").read()
        n = sources[rel].count(old)
        if n != 1:
            head = " ".join(old.split())[:70]
            problems.append(f"{rel}: expected 1 occurrence, found {n} — {head}...")

    clog = os.path.join(repo, CHANGELOG)
    if not os.path.exists(clog):
        problems.append(f"{CHANGELOG}: file not found")
    elif "F279 follow-up 1: the lepton hypercharges are registry constants" in \
            open(clog, encoding="utf-8").read():
        problems.append(f"{CHANGELOG}: this entry is already present")

    if problems:
        print("REFUSED — nothing written:")
        for p in problems:
            print(f"  {p}")
        print("\nThe strings above were written against the files as of "
              "2026-08-06. If a file moved on, re-read it and re-target.")
        return 1

    if args.check:
        print(f"OK — all {len(REPLACEMENTS)} replacements match, changelog entry "
              f"absent. Re-run without --check to apply.")
        return 0

    # ---- apply
    for rel in dict.fromkeys(r for r, _o, _n in REPLACEMENTS):
        text = sources[rel]
        for r, old, new in REPLACEMENTS:
            if r == rel:
                text = text.replace(old, new, 1)
        with open(os.path.join(repo, rel), "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"updated  {rel}")

    with open(clog, "a", encoding="utf-8") as fh:
        fh.write(CHANGELOG_ENTRY)
    print(f"appended {CHANGELOG}")

    print("\nNext: make indexes && make gate, then replace the changelog's "
          "'**Gate:** _pending_' line with the result.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
