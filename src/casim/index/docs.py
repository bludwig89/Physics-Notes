"""`docs-index.md` and `project-status-index.md` — roadmap C8.1.

These two are honest filesystem scrapes and stay that way: no registry knows
about prose. Ported from ``tools/regen_indexes.py`` with one change — the docs
index now lists `deprecated/` as well, because "where did that superseded plan
go" is exactly the question an index should answer, and C0.5 made
`deprecated/` a real, rule-enforced destination rather than an attic.
"""
from __future__ import annotations

import os
import re

from .common import HEADER_NOTE, esc, md_title

_DOC_GROUPS = [
    ("docs/theory", "internal theory derivations & key decisions"),
    ("docs/roadmaps", "active roadmaps & next steps"),
    ("docs/status", "project status, changelog, completion overviews, exactness"),
    ("docs/audits", "one-off reviews & audits"),
    ("docs/design", "internal design docs, registries & manifests"),
    ("papers", "the paper series"),
    ("references", "summaries of external papers (PDFs alongside)"),
    ("deprecated", "superseded docs & plans (see deprecated/README.md for why)"),
]


def render_docs(repo: str) -> tuple[str, str, int]:
    lines = ["# Docs Index", "", HEADER_NOTE,
             "*One line per document. PDFs in `references/` are listed by their "
             "markdown summaries only. `deprecated/` is included on purpose: a "
             "superseded plan that cannot be found is a plan someone will "
             "rewrite.*", ""]
    n = 0
    for d, blurb in _DOC_GROUPS:
        full = os.path.join(repo, d)
        if not os.path.isdir(full):
            continue
        entries = [fn for fn in sorted(os.listdir(full))
                   if fn.endswith(".md") and fn != "README.md"]
        if not entries:
            continue
        lines += [f"## {d}/ — {blurb}", "", "| File | Title |", "|------|-------|"]
        for fname in entries:
            lines.append(f"| `{fname}` | "
                         f"{esc(md_title(os.path.join(full, fname)))} |")
            n += 1
        lines.append("")
    return "docs-index.md", "\n".join(lines), n


def render_status(repo: str) -> tuple[str, str, int]:
    src = "docs/status/project-status.md"
    with open(os.path.join(repo, src), encoding="utf-8") as fh:
        content = fh.read()
    entries = re.findall(r'^## (.+)$', content, re.MULTILINE)
    lines = ["# Project Status Index", "", HEADER_NOTE,
             f"*One line per entry; full narrative in `{src}`. Engineering "
             f"phases (P0–P6, C0–C9) are logged in `docs/status/changelog.md` "
             f"and their own `*-completion-overview.md` files, not here.*", "",
             "| Date | Summary |", "|------|---------|"]
    for e in entries:
        parts = e.split(" — ", 1)
        if len(parts) == 2:
            date, desc = parts
            lines.append(f"| {date.strip()} | {esc(desc.strip()[:140])} |")
        else:
            lines.append(f"| — | {esc(e[:140])} |")
    lines.append("")
    return "project-status-index.md", "\n".join(lines), len(entries)
