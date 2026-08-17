"""`docs/claims/registry.yaml` and `claims-index.md` — decision **D12**.

**Generation runs backwards here, on purpose.** Everywhere else in this repo the
registry is hand-owned and the index is generated: ``_SPINE`` →
``code-index.md``, ``tests/registry/*.yaml`` → ``tests-index.md``. For claims the
**card is the record**, ``registry.yaml`` is generated from the cards, and
``claims-index.md`` is generated from the registry.

The reason is that a module cannot carry its own metadata — the code is the
artifact and the registry has to live beside it — whereas a claim's prose and
its metadata are the same object. Splitting them would create exactly one thing:
a card whose status line disagrees with its registry row. Since nothing can be
true in two places, the card wins and the registry is a projection.

Both outputs are timestamp-free so ``casim index --check`` is a byte comparison,
the same rule the other six targets follow.
"""
from __future__ import annotations

import os

from .common import HEADER_NOTE, esc, truncate

CLAIMS_REL = os.path.join("docs", "claims")

#: Order the index groups claims in. Withdrawn last — it is the retraction
#: record and belongs where a reader lands after the live material, not first.
_STATUS_ORDER = ("live", "narrowed", "contingent", "open", "not_claimed",
                 "withdrawn")


def _cards(repo: str) -> list[dict]:
    """Parse every card's front matter. Imports the gate checker's reader so
    there is exactly one front-matter parser in the repo — a second one would
    be a second thing to disagree with the cards."""
    import importlib.util
    import sys

    path = os.path.join(repo, "tools", "check_claims.py")
    spec = importlib.util.spec_from_file_location("_casim_check_claims", path)
    if spec is None or spec.loader is None:                    # pragma: no cover
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_casim_check_claims"] = mod
    spec.loader.exec_module(mod)

    full = os.path.join(repo, CLAIMS_REL)
    out = []
    for fn in sorted(os.listdir(full)):
        if not (fn.startswith("CL") and fn.endswith(".md")):
            continue
        with open(os.path.join(full, fn), encoding="utf-8") as fh:
            fm = mod.parse_front_matter(fh.read(), fn, [])
        if not fm:
            continue
        fm["_file"] = fn
        out.append(fm)
    out.sort(key=lambda c: c.get("id", ""))
    return out


def _yaml_list(v) -> str:
    return "[" + ", ".join(str(x) for x in (v or [])) + "]"


def _yaml_str(v) -> str:
    """SINGLE-quoted, always — the only escape is '' for a quote.

    Claim titles carry LaTeX. A double-quoted YAML scalar processes escape
    sequences, so `\\dim(E_g)` in a double-quoted string is an invalid-escape
    parse error; getting it right requires an escaping table that must not drift
    from the card writer's. Single quotes need no table.
    """
    if v is None:
        return "null"
    return "'" + str(v).replace("'", "''") + "'"


def render_registry(repo: str) -> tuple[str, str, int]:
    """docs/claims/registry.yaml — the machine-readable projection."""
    cards = _cards(repo)
    lines = [
        "# ---------------------------------------------------------------------------",
        "# GENERATED from docs/claims/CL*.md by `casim index --only claims` (D12).",
        "# DO NOT HAND-EDIT. The card's front matter is the record; this file is a",
        "# projection of it. Editing here changes nothing and will be overwritten.",
        "# ---------------------------------------------------------------------------",
        "version: 1",
        f"count: {len(cards)}",
        f"next_claim: CL{(max((int(c['id'][2:]) for c in cards), default=0) + 1):03d}",
        "",
        "claims:",
    ]
    for c in cards:
        lines += [
            f"  - id: {c['id']}",
            f"    file: docs/claims/{c['_file']}",
            f"    title: {_yaml_str(c.get('title'))}",
            f"    tier: {c.get('tier')}",
            f"    kind: {c.get('kind')}",
            f"    status: {c.get('status')}",
            f"    domain: {_yaml_list(c.get('domain'))}",
            f"    exactness: {c.get('exactness')}",
            f"    falsifier: {c.get('falsifier')}",
            f"    review_state: {c.get('review_state')}",
            f"    confidence: {c.get('confidence')}",
            f"    findings: {_yaml_list(c.get('findings'))}",
            f"    tests: {_yaml_list(c.get('tests'))}",
            f"    modules: {_yaml_list(c.get('modules'))}",
            f"    constants: {_yaml_list(c.get('constants'))}",
            f"    supersessions: {_yaml_list(c.get('supersessions'))}",
            f"    rolls_up_to: {c.get('rolls_up_to') or 'null'}",
            f"    first_issued: {_yaml_str(c.get('first_issued'))}",
        ]
    return os.path.join(CLAIMS_REL, "registry.yaml"), "\n".join(lines) + "\n", len(cards)


def render_index(repo: str) -> tuple[str, str, int]:
    """claims-index.md — one line per claim, grouped so the answer to
    'what does the project assert?' is the first table."""
    cards = _cards(repo)
    by_id = {c["id"]: c for c in cards}

    head = [c for c in cards if c.get("tier") == "headline"]
    seeds = [c for c in cards if c.get("tier") != "headline"]

    n_seed = sum(1 for c in cards if c.get("review_state") == "unreviewed-seed")
    counts = {}
    for c in cards:
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    tally = ", ".join(f"**{counts[s]}** {s}" for s in _STATUS_ORDER if s in counts)

    lines = [
        "# Claims Index", "", HEADER_NOTE,
        "",
        "*One line per claim card (**D12**). A **claim** is what the project "
        "asserts *right now*; a **finding** is what a session did. The two move "
        "independently — a finding may be superseded without any claim changing, "
        "and a claim may be narrowed without any finding changing. "
        "See `docs/claims/README.md` for the contract and the closed "
        "vocabularies; `tools/check_claims.py` enforces them at `make gate`.*",
        "",
        f"**{len(cards)} cards** — {tally}. "
        f"**{n_seed}** are `unreviewed-seed`: mechanically extracted from a "
        "finding, classification **not confirmed by a reviewer**, and not "
        "citable as independent support.",
        "",
    ]

    def table(rows, show_seed=False):
        out = ["| ID | Claim | Kind | Status | Exact | Falsifier | Findings |",
               "|---|---|---|---|---|---|---|"]
        for c in rows:
            up = c.get("rolls_up_to")
            title = esc(truncate(str(c.get("title", "")), 96))
            if up and up in by_id:
                title += f" *(→ {up})*"
            out.append(
                f"| [{c['id']}](docs/claims/{c['_file']}) | {title} | "
                f"{c.get('kind')} | {c.get('status')} | {c.get('exactness')} | "
                f"{c.get('falsifier')} | {', '.join(c.get('findings') or []) or '—'} |")
        return out

    lines += ["## Headline claims", "",
              "*The claims the project makes publicly — the rows of "
              "`papers/Claims-and-Falsifiers-Summary.md`, plus what has been "
              "authored since. Every one is `review_state: authored`.*", ""]
    for st in _STATUS_ORDER:
        group = [c for c in head if c.get("status") == st]
        if not group:
            continue
        lines += [f"### {st} ({len(group)})", ""] + table(group) + [""]

    lines += ["## Supporting claims", "",
              "*One per qualifying finding not already carried by a headline "
              "card. Findings judged not to clear the bar are listed with their "
              "reason in `docs/audits/consolidation-plan-2026-08-04.md` §5, so "
              "\"no card\" is a recorded decision rather than an omission.*", ""]
    for st in _STATUS_ORDER:
        group = [c for c in seeds if c.get("status") == st]
        if not group:
            continue
        lines += [f"### {st} ({len(group)})", ""] + table(group) + [""]

    return "claims-index.md", "\n".join(lines), len(cards)
