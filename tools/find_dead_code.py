#!/usr/bin/env python3
"""Propose dead and superseded code — roadmap C0.2.

**This tool proposes. It never acts.** Nothing here writes to a source file,
and nothing here is automatically accepted into
`docs/design/module-migration-manifest.yaml`. A human moves a line from
`dead_symbols_proposed` to `dead_symbols`, and only then does
the C0.4 migration tool strip it.

That constraint is not politeness, it is the P0.4 lesson stated as a rule. An
audit flagged ~14 test files as covering superseded physics; on inspection
**exactly one was superseded wholesale**. Eleven were a dead verdict wrapped
around live, load-bearing algebra — F62's lapse-mix *sign convention* is
production code, F52's factor-2 discriminator is still canonical under F178 —
and `test_F91_pairing_classification.py`, flagged as superseded, *is* the
supersession authority. Auto-applying that proposal would have silently retired
working coverage while looking tidy.

Three signals, reported separately and **never merged into one score**:

  1. `structurally_unreachable` — a file nothing imports and that has no
     `__main__`, or a top-level symbol no file references by name.
  2. `superseded_by_ledger` — paths and identifiers named in the `scope:` /
     `also_superseded:` fields of `docs/theory/supersessions.yaml`. Identifiers
     named in a `retained:` field are listed as **PROTECTED** in the same
     report, because in this project the two almost always appear in the same
     record.
  3. `suspected_dead` — reachable only from tests that are themselves
     `fully_superseded` in the ledger.

A symbol whose name is defined in more than one module is reported as
`ambiguous`, not dead: references cannot be attributed to one definition, so
claiming it is unused would be a guess. Same discipline as `gen_manifest.py`'s
evidence ranking.

Usage:
    python3 tools/find_dead_code.py                # write proposal + report
    python3 tools/find_dead_code.py --report       # report only, no write
    python3 tools/find_dead_code.py --module ca_maxwell   # one module
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from datetime import datetime, timezone

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(_REPO, "docs", "design", "module-graph.json")
LEDGER = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")
OUT_JSON = os.path.join(_REPO, "docs", "design", "dead-code-proposal.json")
OUT_MD = os.path.join(_REPO, "docs", "design", "dead-code-proposal.md")

# Names too generic to attribute. A reference to `main` or `step` somewhere in
# the tree says nothing about which definition it reaches.
_GENERIC = {
    "main", "run", "step", "build", "setup", "solve", "test", "check", "plot",
    "load", "save", "init", "reset", "update", "apply", "make", "get", "set",
    "demo", "report", "summary", "result", "results", "state", "data", "cfg",
    "config", "params", "args", "kwargs", "self", "cls", "np", "sp",
}
_MIN_LEN = 4

# Identifier-shaped tokens inside ledger prose: `ca_gravity.lapse_mix_half`,
# `F114_enlargement_pct`, `gluon_rotation_step_spectral_bcc_chiral`.
#
# The first version of this matched any word that was also an identifier
# somewhere in the tree. It proposed `Omega`, `energy`, `metric`, `shape`,
# `delta`, `weight`, `series` and `order` as candidate dead symbols — every one
# an ordinary English word in a sentence that happened to collide with a local
# variable in some test. That is precisely the false-positive class P1 named:
# the kind that trains people to ignore the checker. A token now has to LOOK
# like a deliberate code reference, by one of two routes:
#
#   * dotted     `ca_gravity.lapse_mix_half`  — the module qualifies it, or
#   * multi-snake `gluon_rotation_step_spectral_bcc_chiral` (>= 2 underscores)
#
# and it must additionally be DEFINED in a migratable file. A symbol that only
# exists inside `tests/` is not what a ledger `code:` field is talking about.
_DOTTED = re.compile(r"\b([a-z_][a-z0-9_]{2,})\.([A-Za-z_][A-Za-z0-9_]{2,})\b")
_SNAKE = re.compile(r"\b([A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+){2,})\b")


# ---------------------------------------------------------------------------
def load_graph() -> dict:
    if not os.path.exists(GRAPH):
        sys.exit("module-graph.json is missing — run "
                 "`python3 tools/gen_module_graph.py` first (C0.1 before C0.2)")
    with open(GRAPH, encoding="utf-8") as fh:
        return json.load(fh)


def load_ledger() -> dict:
    with open(LEDGER, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _used_names(path: str) -> tuple[set[str], set[str]]:
    """(names referenced, names exported via __all__) in one file."""
    with open(os.path.join(_REPO, path), encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError:
        return set(), set()
    used: set[str] = set()
    exported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            used.add(node.attr)
        elif isinstance(node, ast.alias):
            used.add(node.name.rsplit(".", 1)[-1])
            if node.asname:
                used.add(node.asname)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            # getattr(mod, "name") and __all__ entries both live in strings.
            if node.value.isidentifier():
                used.add(node.value)
        elif (isinstance(node, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == "__all__"
                      for t in node.targets)):
            for elt in ast.walk(node.value):
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    exported.add(elt.value)
    return used, exported


# ---------------------------------------------------------------------------
# Signal 1 — structural
# ---------------------------------------------------------------------------
def signal_structural(g: dict) -> dict:
    nodes = g["nodes"]
    migratable = [r for r, n in nodes.items()
                  if n["role"] in ("kernel", "fork", "derivation", "support")]

    # Where is each top-level name defined? Multiply-defined names cannot be
    # attributed, so they are reported ambiguous rather than dead.
    definers: dict[str, list[str]] = {}
    for rel in migratable:
        for sym in nodes[rel]["defines"]:
            definers.setdefault(sym, []).append(rel)

    used_by_file: dict[str, set[str]] = {}
    exported_by_file: dict[str, set[str]] = {}
    for rel in nodes:
        u, e = _used_names(rel)
        used_by_file[rel] = u
        exported_by_file[rel] = e

    files: list[dict] = []
    symbols: list[dict] = []
    module_private: list[dict] = []
    ambiguous: list[dict] = []

    for rel in sorted(migratable):
        n = nodes[rel]
        if n["reach"] == "unreferenced" and not n["has_main"]:
            files.append({
                "path": rel, "role": n["role"], "lines": n["lines"],
                "reason": "nothing imports it and it has no __main__",
            })

        own_uses = used_by_file.get(rel, set())
        exported = exported_by_file.get(rel, set())
        for sym in sorted(n["defines"]):
            if sym.startswith("__") or len(sym) < _MIN_LEN or sym in _GENERIC:
                continue
            if sym in exported:
                continue
            if len(definers.get(sym, [])) > 1:
                ambiguous.append({
                    "path": rel, "symbol": sym,
                    "also_defined_in": [p for p in definers[sym] if p != rel],
                })
                continue
            external = sorted(
                other for other, u in used_by_file.items()
                if other != rel and sym in u)
            if external:
                continue
            # Referenced inside its own module? An ast.FunctionDef binds its
            # name without emitting an ast.Name, so a hit here is a genuine
            # call site, not the definition. A symbol used internally is a
            # PRIVATE HELPER, not dead code — removing it means removing its
            # callers too, which is a refactor and not a cleanup. Reported
            # separately and NOT proposed.
            if sym in own_uses:
                module_private.append({"path": rel, "symbol": sym})
                continue
            symbols.append({
                "path": rel, "symbol": sym,
                "reason": "defined, and referenced by no file in the tree — "
                          "including its own",
            })

    return {"files": files, "symbols": symbols,
            "module_private": module_private, "ambiguous": ambiguous}


# ---------------------------------------------------------------------------
# Signal 2 — the ledger
# ---------------------------------------------------------------------------
def _idents(text: str, known: set[str], modules: set[str]) -> list[str]:
    """Deliberate code references in ledger prose. See the _DOTTED/_SNAKE note."""
    text = text or ""
    out: set[str] = set()
    for mod, attr in _DOTTED.findall(text):
        if mod in modules and attr in known:
            out.add(attr)
        elif mod in known and attr in ("py",):        # `ca_maxwell.py`
            out.add(mod)
    for tok in _SNAKE.findall(text):
        if tok in known and tok not in _GENERIC:
            out.add(tok)
    # A bare module name is a legitimate reference too, but only if the ledger
    # spelled it exactly and it is a real module.
    for tok in re.findall(r"\b(ca_[a-z0-9_]+|derive_[a-z0-9_]+)\b", text):
        if tok in modules:
            out.add(tok)
    return sorted(out)


def signal_ledger(g: dict, ledger: dict) -> dict:
    nodes = g["nodes"]
    migratable = {r: n for r, n in nodes.items()
                  if n["role"] in ("kernel", "fork", "derivation", "support")}
    # Only symbols DEFINED in a migratable file count. A name that exists only
    # in tests/ is not what a ledger `code:` field is describing.
    known = {s for n in migratable.values() for s in n["defines"]}
    modules = {n["key"] for n in migratable.values()}
    modules |= {os.path.basename(r)[:-3] for r in migratable}

    paths: list[dict] = []
    candidates: list[dict] = []
    protected: list[dict] = []

    for rec in ledger.get("supersessions", []):
        rid = rec["id"]
        code_notes = " ".join((c.get("note") or "")
                              for c in (rec.get("code") or []))
        # `code:` notes carry the sharpest references in the whole ledger —
        # "STALE: still computes F114_enlargement_pct" names the exact symbol.
        dead_text = " ".join(filter(None, [
            rec.get("scope", ""),
            " ".join(rec.get("also_superseded", []) or []),
            code_notes,
        ]))
        live_text = " ".join(filter(None, [
            rec.get("retained", ""), rec.get("entails", "")]))

        for c in rec.get("code", []) or []:
            p = c.get("path")
            if not p:
                continue
            paths.append({
                "path": p, "record": rid, "kind": rec.get("kind"),
                "by": rec.get("by", []), "note": (c.get("note") or "").strip(),
                "exists": os.path.exists(os.path.join(_REPO, p)),
            })

        scope_syms = set(_idents(" ".join(filter(None, [
            rec.get("scope", ""),
            " ".join(rec.get("also_superseded", []) or [])])), known, modules))
        for sym in _idents(dead_text, known, modules):
            where = sorted(r for r, n in migratable.items() if sym in n["defines"])
            candidates.append({
                "symbol": sym, "record": rid, "defined_in": where,
                # `scope:` states what died. A `code:` note often names the
                # canonical survivor and the dead one in the SAME sentence, so
                # a candidate sourced only from a note is weaker evidence.
                "source_field": "scope" if sym in scope_syms else "code-note",
            })
        for sym in _idents(live_text, known, modules):
            where = sorted(r for r, n in migratable.items() if sym in n["defines"])
            protected.append({
                "symbol": sym, "record": rid, "defined_in": where,
                "context": "retained/entails",
            })

    prot_names = {p["symbol"] for p in protected}
    for c in candidates:
        c["also_in_retained"] = c["symbol"] in prot_names
        # A superseded symbol and its replacement almost always share a prefix
        # in this codebase: `gluon_rotation_step_spectral_bcc` (canonical, even)
        # vs `..._bcc_chiral` (retained for comparison). Prose extraction cannot
        # tell which of a sibling pair the sentence meant, and the first version
        # of this tool got that exact pair BACKWARDS — proposing the canonical
        # even step as dead. Flagging the collision is honest; guessing is not.
        sibs = sorted(
            p["symbol"] for p in protected
            if p["record"] == c["record"] and p["symbol"] != c["symbol"]
            and (p["symbol"].startswith(c["symbol"])
                 or c["symbol"].startswith(p["symbol"])))
        c["sibling_of_protected"] = sibs

    ledger_paths = {p["path"] for p in paths}
    return {"paths": paths, "candidates": candidates, "protected": protected,
            "ledger_paths": sorted(ledger_paths)}


# ---------------------------------------------------------------------------
# Signal 3 — reachable only from tombstoned tests
# ---------------------------------------------------------------------------
def signal_tombstoned(g: dict, ledger: dict) -> list[dict]:
    nodes = g["nodes"]
    tombstoned = {t["path"] for rec in ledger.get("supersessions", [])
                  for t in (rec.get("tests") or [])
                  if t.get("status") == "fully_superseded"}
    out: list[dict] = []
    for rel, n in nodes.items():
        if n["role"] not in ("kernel", "fork", "derivation", "support"):
            continue
        if n["reach"] != "test-only":
            continue
        importers = [t for t in n["imported_by"] if nodes[t]["role"] == "test"]
        if importers and all(t in tombstoned for t in importers):
            out.append({"path": rel, "only_importers": importers})
    return {"modules": out, "tombstoned_tests": sorted(tombstoned)}


# ---------------------------------------------------------------------------
def build() -> dict:
    g = load_graph()
    ledger = load_ledger()
    return {
        "version": 1,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "graph_sha": g.get("git_sha"),
        "contract": (
            "PROPOSAL ONLY. Nothing here is applied. A human moves a line into "
            "`dead_symbols` in docs/design/module-migration-manifest.yaml, and "
            "only then did the C0.4 migration tool strip it. Signals are "
            "reported separately and are NOT to be summed: P0.4 found that of "
            "14 files an audit called superseded, exactly one was superseded "
            "wholesale."),
        "signal_1_structural": signal_structural(g),
        "signal_2_ledger": signal_ledger(g, ledger),
        "signal_3_tombstoned": signal_tombstoned(g, ledger),
    }


def render_md(p: dict) -> str:
    s1, s2, s3 = (p["signal_1_structural"], p["signal_2_ledger"],
                  p["signal_3_tombstoned"])
    L = [
        "# Dead-code proposal",
        "",
        f"*Generated {p['generated']} by `tools/find_dead_code.py` "
        f"(roadmap C0.2) at graph `{p['graph_sha']}`. "
        "**Do not edit by hand** — regenerate.*",
        "",
        "> **This is a proposal, not a verdict.** Nothing here has been applied.",
        "> A human accepts a line by moving it into `dead_symbols` in",
        "> `docs/design/module-migration-manifest.yaml`; only accepted lines are",
        "> stripped by the C0.4 migration tool. The three signals below are",
        "> independent and must not be summed — P0.4 found that of 14 files an",
        "> audit called superseded, exactly **one** was superseded wholesale.",
        "",
        "| Signal | Count |",
        "|---|---|",
        f"| 1. unreferenced files | {len(s1['files'])} |",
        f"| 1. unreferenced symbols **(proposed)** | {len(s1['symbols'])} |",
        f"| 1. module-private helpers (used internally — NOT dead) | {len(s1['module_private'])} |",
        f"| 1. ambiguous (name defined in >1 module — NOT dead) | {len(s1['ambiguous'])} |",
        f"| 2. ledger-named paths | {len(s2['paths'])} |",
        f"| 2. candidate dead symbols (from `scope:`) | {len(s2['candidates'])} |",
        f"| 2. PROTECTED symbols (from `retained:`) | {len(s2['protected'])} |",
        f"| 3. modules reachable only from tombstoned tests | {len(s3['modules'])} |",
        "",
        "---",
        "",
        "## Signal 1 — structurally unreachable",
        "",
        "### Files nothing imports, with no `__main__`",
        "",
    ]
    if s1["files"]:
        lp = set(s2["ledger_paths"])
        L += ["| Path | Role | Lines | Why | Ledger |", "|---|---|---|---|---|"]
        for f in s1["files"]:
            flag = ("**named in the ledger — read the record first**"
                    if f["path"] in lp else "—")
            L.append(f"| `{f['path']}` | {f['role']} | {f['lines']} | "
                     f"{f['reason']} | {flag} |")
        L += ["", "Two entries here are the roadmap's own worked example. "
              "`derive_generator_norm_from_F118.py` has no `__main__` and "
              "nothing imports it, so it lands in this table — and it must "
              "**not** be deleted: P0.4 gave it a `PRE-DECISION FRAMING` "
              "banner because its Schur-isotropy proof *is* the F255 content, "
              "and its circularity argument is precisely *why* the F234 arrow "
              "was reversed. It migrates with the banner intact (roadmap C5). "
              "This is what \"a signal is not a verdict\" looks like in "
              "practice."]
    else:
        L.append("*(none)*")

    L += ["", "### Top-level symbols nothing in the tree references", "",
          f"**{len(s1['symbols'])} proposed.** A separate "
          f"**{len(s1['module_private'])}** are referenced inside their own "
          f"module and are therefore private helpers, not dead code — removing "
          f"one means removing its callers too, which is a refactor. Those are "
          f"in the JSON under `module_private` and are NOT proposed.", ""]
    if s1["symbols"]:
        L += ["| Path | Symbol |", "|---|---|"]
        L += [f"| `{s['path']}` | `{s['symbol']}` |" for s in s1["symbols"][:200]]
        if len(s1["symbols"]) > 200:
            L.append(f"| … | *{len(s1['symbols']) - 200} more — see the JSON* |")
    else:
        L.append("*(none)*")
    L += ["", "### Ambiguous — name defined in more than one module", "",
          "These are **not** proposed as dead. A reference to the name cannot "
          "be attributed to one definition, so calling it unused would be a "
          "guess. Same discipline as `gen_manifest.py`'s evidence ranking.", ""]
    L.append(f"*{len(s1['ambiguous'])} symbols — see the JSON.*")

    L += ["", "---", "", "## Signal 2 — named by the supersession ledger", "",
          "### Paths", ""]
    if s2["paths"]:
        L += ["| Path | Record | Kind | Note |", "|---|---|---|---|"]
        for f in s2["paths"]:
            note = (f["note"] or "").replace("\n", " ").replace("|", "\\|")[:110]
            miss = "" if f["exists"] else " **(MISSING)**"
            L.append(f"| `{f['path']}`{miss} | {f['record']} | {f['kind']} | {note} |")
    else:
        L.append("*(none)*")

    L += ["", "### Candidate dead symbols", "",
          "Extracted from each record's `scope:`, `also_superseded:` and "
          "`code:` notes. The **From** column matters: `scope` states what "
          "died, whereas a `code-note` routinely names the survivor and the "
          "casualty in one sentence, so it is weaker evidence. The "
          "**Conflict** column is the safety rail — it fires when the same "
          "record's `retained:` field names the identifier, or names a "
          "prefix-sibling of it. Read the record before accepting either.", ""]
    if s2["candidates"]:
        L += ["| Symbol | Record | From | Defined in | Conflict |",
              "|---|---|---|---|---|"]
        for c in s2["candidates"]:
            where = ", ".join(f"`{w}`" for w in c["defined_in"]) or "—"
            if c["also_in_retained"]:
                flag = "**PROTECTED — also in `retained:`**"
            elif c["sibling_of_protected"]:
                sib = ", ".join(f"`{x}`" for x in c["sibling_of_protected"])
                flag = f"**sibling of protected {sib} — DO NOT GUESS**"
            else:
                flag = "—"
            L.append(f"| `{c['symbol']}` | {c['record']} | `{c['source_field']}` "
                     f"| {where} | {flag} |")
        L += ["", "**On the sibling flag.** A superseded symbol and its "
              "replacement almost always share a prefix here. "
              "`gluon_rotation_step_spectral_bcc` (canonical, even, F91) and "
              "`gluon_rotation_step_spectral_bcc_chiral` (retained for "
              "historical comparison) are named in the *same* ledger sentence, "
              "and the first version of this tool extracted them the wrong way "
              "round — proposing the canonical propagator as dead. It cannot "
              "be resolved from prose, so it is flagged, not guessed."]
    else:
        L.append("*(none)*")

    L += ["", "### Protected symbols (named in `retained:`)", "",
          "Explicitly survived a supersession. **Never strip these** without "
          "re-reading the ledger record.", ""]
    if s2["protected"]:
        L += ["| Symbol | Record | Defined in |", "|---|---|---|"]
        for c in s2["protected"]:
            where = ", ".join(f"`{w}`" for w in c["defined_in"]) or "—"
            L.append(f"| `{c['symbol']}` | {c['record']} | {where} |")
    else:
        L.append("*(none)*")

    L += ["", "---", "",
          "## Signal 3 — reachable only from tombstoned tests", "",
          f"Tombstoned tests (`status: fully_superseded` in the ledger): "
          f"{len(s3['tombstoned_tests'])}.", ""]
    if s3["modules"]:
        L += ["| Module | Only importers |", "|---|---|"]
        for m in s3["modules"]:
            L.append(f"| `{m['path']}` | "
                     f"{', '.join('`' + i + '`' for i in m['only_importers'])} |")
    else:
        L += ["*(none — no module depends solely on a fully-superseded test.)*",
              "", "That is the expected result today: exactly one test in the "
              "project is fully superseded, and it tests a fork, not a kernel."]
    L.append("")
    return "\n".join(L)


def report(p: dict) -> None:
    s1, s2, s3 = (p["signal_1_structural"], p["signal_2_ledger"],
                  p["signal_3_tombstoned"])
    print("\ndead-code proposal  (PROPOSAL ONLY — nothing applied)")
    print("\n  signal 1  structural")
    print(f"    unreferenced files            {len(s1['files'])}")
    print(f"    unreferenced symbols          {len(s1['symbols'])}  (proposed)")
    print(f"    module-private (NOT dead)     {len(s1['module_private'])}")
    print(f"    ambiguous (NOT dead)          {len(s1['ambiguous'])}")
    print("\n  signal 2  supersession ledger")
    print(f"    named paths                   {len(s2['paths'])}"
          + (f"  ({sum(1 for f in s2['paths'] if not f['exists'])} missing)"
             if any(not f["exists"] for f in s2["paths"]) else ""))
    prot = sum(1 for c in s2["candidates"] if c["also_in_retained"])
    print(f"    candidate dead symbols        {len(s2['candidates'])}  "
          f"({prot} ALSO named in retained: — read the record)")
    print(f"    protected symbols             {len(s2['protected'])}")
    print("\n  signal 3  tombstoned-test-only")
    print(f"    modules                       {len(s3['modules'])}")
    print(f"    tombstoned tests              {len(s3['tombstoned_tests'])}")


def one_module(p: dict, name: str) -> int:
    s1, s2 = p["signal_1_structural"], p["signal_2_ledger"]
    hits = lambda seq, key: [x for x in seq if name in x.get(key, "")]
    print(f"\n{name}")
    for f in hits(s1["files"], "path"):
        print(f"  FILE unreferenced: {f['reason']}")
    syms = hits(s1["symbols"], "path")
    print(f"  unreferenced symbols: {len(syms)}")
    for s in syms:
        print(f"    {s['symbol']}")
    priv = hits(s1["module_private"], "path")
    if priv:
        print(f"  module-private (not dead): "
              f"{', '.join(x['symbol'] for x in priv)}")
    for f in hits(s2["paths"], "path"):
        print(f"  LEDGER {f['record']} ({f['kind']}): {f['note'][:100]}")
    amb = hits(s1["ambiguous"], "path")
    if amb:
        print(f"  ambiguous (not dead): {', '.join(a['symbol'] for a in amb)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="do not write files")
    ap.add_argument("--module", metavar="NAME", help="filter to one module")
    args = ap.parse_args()

    p = build()
    if args.module:
        return one_module(p, args.module)
    if args.report:
        report(p)
        return 0

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(p, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write(render_md(p))
    report(p)
    print(f"\nwrote {os.path.relpath(OUT_JSON, _REPO)}")
    print(f"wrote {os.path.relpath(OUT_MD, _REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
