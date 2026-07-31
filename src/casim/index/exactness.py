"""The exactness inventory — roadmap C8.4, closing **P1.5**.

Why P1 could not finish this
----------------------------
P1 emitted 147 of 530 residual-bearing rows and said why: the class vocabulary in
the artifacts is not standardised. A survey found `exact` (61),
`machine-precision` (34), `machine` (31), `quantitative` (132), plus `Tier-B`,
`PREDICTION`, `structural`, and channel labels like `coupled` that are not
exactness classes at all. Generating a table from that would have produced a
confident-looking document with 383 silent holes.

What C8 changes
---------------
There are now **three** ways to class a row, tried in order, and **the rule that
fired is recorded per row**:

1. ``declared`` — the artifact entry's own label, canonicalised. P1's rule.
2. ``record`` — the ``expect.exactness`` of the test-registry record (D9) that
   owns the artifact. A record cannot declare a class outside
   ``EXACTNESS_CLASSES``, so this arrives pre-standardised by construction.
3. ``signature`` — the **numerical signature the inventory itself defines**: this
   document's "Reading the table" section says exact means "residual bounded by ε
   with no growth", machine means "10⁻¹⁵–10⁻¹² over the run", quantitative means
   "inside a declared tolerance". So residual ``== 0`` is exact, ``< 1e-12`` is
   machine, and anything larger is quantitative. This is not a guess about what
   the author meant; it is the document's own criterion applied to the number.

Coverage is then reported **per rule**, not as one figure, because "classified"
means something different in each case and collapsing them would hide exactly
what P1 refused to hide.

Two things this deliberately does not do
----------------------------------------
* It does not delete the hand-written Tier 1–3 tables. Those carry a *Predicted
  form* column — the physics claim, e.g. "$u^2+\\lVert\\tilde n\\rVert^2 = 1$
  (Paper 1 Eq. 15, sign-corrected)" — which no artifact records. Replacing them
  with machine labels like ``C1_derived_cos3delta`` would raise coverage and
  destroy information. The generated tables are **additive and complete**; the
  curated tables stay authoritative for the claim itself.
* It does not invent a residual. An entry with no numeric residual is not a row.
"""
from __future__ import annotations

import json
import os
import re
from .common import esc

BEGIN_HEAD = "<!-- BEGIN GENERATED: header + tally (casim index) -->"
END_HEAD = "<!-- END GENERATED: header + tally -->"
BEGIN_ROWS = "<!-- BEGIN GENERATED: exactness rows (casim index) -->"
END_ROWS = "<!-- END GENERATED -->"

INVENTORY_REL = os.path.join("docs", "status", "exactness-inventory.md")

# Canonicalise every class string observed in the artifacts. Anything unmapped
# falls through to rule 2 and then rule 3 — never to a guess.
_CANON = {
    "exact": "exact", "algebraic": "exact", "structural": "exact",
    "machine": "machine", "machine-precision": "machine",
    "machine_precision": "machine", "fft-floor": "machine",
    "quantitative": "quantitative", "numeric": "quantitative",
    "prediction": "quantitative", "bracketed": "bracketed",
    "external": "external",
}
# Labels that are channel/tier metadata, not exactness classes. Recorded so the
# reader can see that they were *identified* rather than silently dropped.
_NOT_EXACTNESS = {"coupled", "background", "source-only", "a(coarse nucleus)",
                  "tier-a", "tier-b", "tier-c"}

_RESIDUAL_KEYS = ("residual", "max_abs_err", "rel_err", "err", "delta")

MACHINE_FLOOR = 1e-12

_ORDER = {"exact": 0, "machine": 1, "quantitative": 2, "bracketed": 3,
          "external": 4}
_TIER_TITLE = {
    "exact": "Tier 1 — exact (residual algebraically zero)",
    "machine": "Tier 2 — machine precision (below the 1e-12 float/FFT floor)",
    "quantitative": "Tier 3 — quantitative (a number with a declared tolerance)",
    "bracketed": "Tier 4 — bracketed (the range IS the result)",
    "external": "Tier 5 — external (measured input from outside the model)",
}


def _walk(node, path=""):
    if isinstance(node, dict):
        yield path, node
        for k, v in node.items():
            yield from _walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk(v, f"{path}[{i}]")


def _by_signature(resid: float) -> str:
    if resid == 0.0:
        return "exact"
    return "machine" if abs(resid) < MACHINE_FLOOR else "quantitative"


def _record_classes(repo: str) -> dict[str, str]:
    """{artifact path -> owning record's declared exactness class} (D9)."""
    try:
        from casim.tests import registry as treg
    except Exception:                                        # pragma: no cover
        return {}
    out: dict[str, str] = {}
    for r in treg.all_records():
        if not r.exactness:
            continue
        for p in r.results:
            out[p] = r.exactness
    return out


def harvest(repo: str) -> tuple[list[dict], dict]:
    manifest_path = os.path.join(repo, "test-results", "manifest.json")
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    record_class = _record_classes(repo)

    rows: list[dict] = []
    stats = {"files": 0, "with_residual": 0, "declared": 0, "record": 0,
             "signature": 0, "not_exactness_labels": 0}

    for rpath, rrec in sorted((manifest.get("results") or {}).items()):
        if not rpath.endswith(".json"):
            continue
        try:
            with open(os.path.join(repo, rpath), encoding="utf-8") as fh:
                payload = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        stats["files"] += 1
        owner = rrec["tests"][0]["path"] if rrec.get("tests") else ""
        findings = rrec.get("declared_findings") or rrec.get("findings") or []

        for path, node in _walk(payload):
            if not isinstance(node, dict):
                continue
            resid = next((node[k] for k in _RESIDUAL_KEYS
                          if isinstance(node.get(k), (int, float))
                          and not isinstance(node.get(k), bool)), None)
            if resid is None:
                continue
            stats["with_residual"] += 1

            raw = None
            for key in ("exactness", "tier", "class"):
                if isinstance(node.get(key), str):
                    raw = node[key].strip().lower()
                    break
            canon, rule = None, None
            if raw is not None and raw not in _NOT_EXACTNESS:
                canon = _CANON.get(raw)
            if raw is not None and raw in _NOT_EXACTNESS:
                stats["not_exactness_labels"] += 1
            if canon:
                rule = "declared"
            elif rpath in record_class:
                canon, rule = record_class[rpath], "record"
            else:
                canon, rule = _by_signature(float(resid)), "signature"
            stats[rule] += 1

            label = (node.get("name") or node.get("check") or node.get("title")
                     or path.rsplit(".", 1)[-1])
            rows.append({
                "tier": canon,
                "rule": rule,
                "construct": str(label)[:70],
                "residual": float(resid),
                "findings": " ".join(findings[:3]),
                "result": rpath,
                "test": owner,
            })
    return rows, stats


# ---------------------------------------------------------------------------
def _newest_finding(repo: str) -> str:
    import re
    fdir = os.path.join(repo, "findings")
    nums = [int(m.group(1)) for f in os.listdir(fdir)
            if (m := re.match(r"F(\d+)", f))]
    return f"F{max(nums)}" if nums else "F0"


def render_header(repo: str, rows: list[dict], stats: dict) -> str:
    """The generated tally + freshness header (C8.4's staleness fix).

    Deliberately carries **no timestamp**. A date here would make every
    `casim index` run a diff and `--check` unusable as a byte comparison; and the
    freshness signal that actually matters is the newest finding covered, which
    is what the staleness metric reads. Git records when.
    """
    newest = _newest_finding(repo)
    counts = {t: sum(1 for r in rows if r["tier"] == t) for t in _ORDER}
    total = len(rows)
    classified_pct = 100.0 * total / stats["with_residual"] if stats["with_residual"] else 0.0
    return "\n".join([
        BEGIN_HEAD,
        "",
        f"*Tally generated by `casim index`; covers every committed "
        f"result artifact and findings through **{newest}**. This block used to "
        f"be hand-maintained and was 125 findings behind its own tree — the "
        f"staleness metric P1 surfaced. It is generated now, so it cannot drift.*",
        "",
        "| Class | Generated rows | What it means |",
        "|---|---:|---|",
        f"| **exact** | {counts['exact']} | residual algebraically zero |",
        f"| **machine** | {counts['machine']} | below the 1e-12 float/FFT floor |",
        f"| **quantitative** | {counts['quantitative']} | a number inside a "
        f"declared tolerance |",
        f"| **bracketed** | {counts['bracketed']} | the range is the result |",
        f"| **external** | {counts['external']} | measured input from outside "
        f"the model |",
        "",
        f"**Coverage: {total} of {stats['with_residual']} residual-bearing "
        f"entries ({classified_pct:.1f}%)**, across {stats['files']} result "
        f"artifacts. By classification rule: **{stats['declared']} declared** "
        f"(the entry labels its own class), **{stats['record']} by record** (the "
        f"owning test-registry record's `expect.exactness`, D9), "
        f"**{stats['signature']} by numerical signature** (this document's own "
        f"criterion: 0 → exact, <1e-12 → machine, larger → quantitative). "
        f"{stats['not_exactness_labels']} entries carry a label that is channel "
        f"or tier metadata rather than an exactness class (`coupled`, "
        f"`background`, `Tier-B`); those fall through to the later rules rather "
        f"than being dropped, which is what P1 could not do.",
        "",
        f"*The curated Tier 1–3 tables below are **not** generated and stay "
        f"authoritative for the physics claim: they carry a `Predicted form` "
        f"column that no artifact records. The generated tables at the end of "
        f"this file are the complete machine-derived view.*",
        "",
        END_HEAD,
    ])


def render_rows(rows: list[dict], stats: dict) -> str:
    lines = [
        BEGIN_ROWS, "",
        "## Generated tables *(by `casim index` — do not edit by hand)*",
        "",
        "Every residual-bearing entry in every committed result artifact, "
        "classified by the three-rule chain described in "
        "`casim/index/exactness.py`. The `Rule` column says which rule fired: "
        "`declared` (the entry's own label), `record` (its test-registry "
        "record's `expect.exactness`), or `signature` (the numerical criterion "
        "in *Reading the table*). Sort order within a tier is by residual.",
        "",
    ]
    for tier in sorted(_ORDER, key=lambda t: _ORDER[t]):
        trows = [r for r in rows if r["tier"] == tier]
        if not trows:
            continue
        lines += [
            f"### {_TIER_TITLE[tier]} — {len(trows)} rows", "",
            "| Construct | Residual | Rule | Findings | Result artifact |",
            "|-----------|----------|------|----------|-----------------|",
        ]
        for r in sorted(trows, key=lambda r: (abs(r["residual"]), r["construct"])):
            lines.append(
                f"| {esc(r['construct'])} | `{r['residual']:.3e}` | {r['rule']} | "
                f"{r['findings']} | `{os.path.basename(r['result'])}` |")
        lines.append("")
    lines += [
        f"*{len(rows)} generated rows from {stats['files']} artifacts. "
        f"Rules: {stats['declared']} declared, {stats['record']} by record, "
        f"{stats['signature']} by signature.*",
        "", END_ROWS,
    ]
    return "\n".join(lines)


def _splice(text: str, begin: str, end: str, block: str, at_end: bool) -> str:
    """Replace EVERY begin..end block with one copy of `block`.

    "Every", not "the first", because the pre-C8 generator used a different
    opener with the same closer, and a first-match splice left the old block in
    place and appended a second one — two generated tables in one document, both
    claiming to be authoritative. Stripping all matches first makes this
    self-healing and idempotent.
    """
    # Swallow the blank lines around an existing block too, so re-splicing does
    # not accumulate one every run (the first version was not idempotent for
    # exactly that reason, and `--check` caught it).
    pattern = re.compile(r"\n*" + re.escape(begin) + r".*?" + re.escape(end)
                         + r"\n*", re.DOTALL)
    existed = bool(pattern.search(text))
    text = pattern.sub("\n", text)
    if existed and not at_end:
        marker = "\n---\n"
        i = text.index(marker) + len(marker) if marker in text else 0
        return text[:i] + "\n" + block + "\n\n" + text[i:]
    if existed and at_end:
        return text.rstrip() + "\n\n" + block + "\n"
    if at_end:
        return text.rstrip() + "\n\n---\n\n" + block + "\n"
    marker = "\n---\n"
    i = text.index(marker) + len(marker) if marker in text else len(text)
    return text[:i] + "\n" + block + "\n" + text[i:]


_LEGACY_ROWS_OPENER = ("<!-- BEGIN GENERATED: exactness rows "
                       "(tools/gen_exactness_inventory.py) -->")


def render(repo: str) -> tuple[str, str, int]:
    rows, stats = harvest(repo)
    path = os.path.join(repo, INVENTORY_REL)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    # Rename the pre-C8 opener FIRST, so the old block is replaced in place
    # rather than left behind next to a freshly appended one.
    text = text.replace(_LEGACY_ROWS_OPENER, BEGIN_ROWS)
    text = _splice(text, BEGIN_HEAD, END_HEAD, render_header(repo, rows, stats),
                   at_end=False)
    text = _splice(text, BEGIN_ROWS, END_ROWS, render_rows(rows, stats),
                   at_end=True)
    return INVENTORY_REL, text, len(rows)


def staleness(repo: str) -> dict:
    """How far the inventory's freshness header is behind the tree.

    Reads the **generated** header, which is the C8.4 fix: the number used to be
    typed by hand and was 125 findings behind. A non-zero value here now means
    `casim index` has not been run, which `--check` also catches.
    """
    import re
    path = os.path.join(repo, INVENTORY_REL)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    head = text[text.index(BEGIN_HEAD):text.index(END_HEAD)] \
        if BEGIN_HEAD in text and END_HEAD in text else ""
    m = re.search(r"\*\*(F\d+)\*\*", head)
    have = int(m.group(1)[1:]) if m else 0
    newest = int(_newest_finding(repo)[1:])
    return {"header_finding": f"F{have}" if have else None,
            "newest_finding": f"F{newest}",
            "findings_behind": max(0, newest - have),
            "generated_header": bool(head)}
