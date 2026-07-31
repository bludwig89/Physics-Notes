"""`tests-index.md` from the test registry — roadmap C8.1 (**D9**).

What this replaces, and why "the heuristic is deleted, not improved":

``tools/regen_indexes.py`` matched a result artifact to a test by
``result.startswith(test_stem)``, **capped the list at two**, and left 104 of 339
rows with an empty Results cell. It could not see a test that writes
``top10_T09_GR4_mercury.json`` from ``test_09_GR4_mercury.py``, and it could not
see a third artifact at all. Every row here is instead a registry record, so the
mapping is **declared**: exact, uncapped, and wrong only if a human wrote it
wrong — in which case `casim test` says so, because the same field is what the
runner diffs against.

Two artifact columns, on purpose:

* **Baselines** — the record's ``results:``. These are what the record *fails
  on*.
* **Other artifacts** — files the results manifest links to the same test that
  the record does *not* declare. Not a fallback and not evidence of anything: it
  is the C7 arming to-do list, in the open, where the next session can see it.

The row also carries `kind`, `tier` and `exactness`, which is what makes the
index usable for context loading: "which exact assertions cover F234" is now a
table lookup instead of a grep.
"""
from __future__ import annotations

import json
import os

from .common import HEADER_NOTE, esc, truncate

_SUITE_OF = {
    "tests/casim": "casim",
    "tests/findings": "findings",
    "tests/priority": "priority",
    "tests/runners": "runners",
}


def _manifest_links(repo: str) -> dict[str, list[str]]:
    path = os.path.join(repo, "test-results", "manifest.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        m = json.load(fh)
    out: dict[str, list[str]] = {}
    for rpath, rec in (m.get("results") or {}).items():
        for t in rec.get("tests") or []:
            out.setdefault(t["path"], []).append(rpath)
    return {k: sorted(v) for k, v in out.items()}


def render(repo: str) -> tuple[str, str, int]:
    from casim.tests import registry as treg

    links = _manifest_links(repo)
    rows = []
    stats = {"declared": 0, "linked_only": 0, "no_artifact": 0}
    for r in treg.all_records():
        suite = ("registry" if not r.path
                 else _SUITE_OF.get(r.path.rsplit("/", 1)[0], "other"))
        name = os.path.basename(r.path) if r.path else (r.scenario or r.id)
        baselines = ", ".join(f"`{os.path.basename(p)}`" for p in r.results)
        extra = [p for p in links.get(r.path or "", ()) if p not in r.results]
        other = ", ".join(f"`{os.path.basename(p)}`" for p in extra)
        if r.results:
            stats["declared"] += 1
        elif extra:
            stats["linked_only"] += 1
        else:
            stats["no_artifact"] += 1
        summary = truncate(str(r.evidence.get("summary") or ""), 120)
        kind = r.kind if r.has_failure_mode else f"{r.kind} ⚠"
        rows.append((suite, name, r.id, " ".join(r.findings), kind, r.tier,
                     r.exactness or "", summary, baselines, other))

    lines = [
        "# Tests Index", "", HEADER_NOTE,
        "*One line per **test-registry record** (`tests/registry/*.yaml`, "
        "decision D9) — not per file, because three records own no file (the "
        "`scenario` kind) and the registry is what `casim test` and `pytest` both "
        "execute. `Baselines` is the record's declared `results:`, which is what "
        "it fails on; `Other artifacts` are files the results manifest links to "
        "the same test that the record does not declare — the C7 arming to-do "
        "list, not a fallback. A `⚠` on the kind means the record declares no "
        "failure mode (`legacy_script`: debt). Specs for future falsification "
        "tests live in `tests/falsification/`.*", "",
        "| Suite | File | Record | Findings | Kind | Tier | Exactness | Summary "
        "| Baselines | Other artifacts |",
        "|-------|------|--------|----------|------|------|-----------|---------"
        "|-----------|-----------------|",
    ]
    for suite, name, rid, finds, kind, tier, exact, summary, base, other in rows:
        lines.append(
            f"| {suite} | `{name}` | `{rid}` | {finds} | {kind} | {tier} | "
            f"{exact} | {esc(summary)} | {base} | {other} |")
    lines += [
        "",
        f"*{len(rows)} record(s): {stats['declared']} declare a baseline, "
        f"{stats['linked_only']} have manifest-linked artifacts they do not yet "
        f"declare, {stats['no_artifact']} emit nothing. Every empty `Baselines` "
        f"cell is a record with no declared `results:` — the registry has "
        f"nothing to fill it with, which is a different statement from the old "
        f"index's silence.*",
        "",
    ]
    return "tests-index.md", "\n".join(lines), len(rows)


def audit(repo: str) -> dict:
    """Rows the registry could fill but did not — the C8 acceptance criterion."""
    from casim.tests import registry as treg

    links = _manifest_links(repo)
    unfilled = [r.id for r in treg.all_records()
                if not r.results and links.get(r.path or "")]
    return {"records": len(treg.all_records()),
            "empty_but_linked": unfilled}
