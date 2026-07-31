#!/usr/bin/env python3
"""Build `docs/design/module-graph.json` — roadmap C0.1.

The dependency map that phases C1-C9 execute against. Every later phase asks the
same three questions of a file — *what imports it, what does it import, and is
anything actually driving it* — and before this tool the answers were prose.

**AST inspection, never import.** This is P0.2's rule and it holds for the same
reason: importing a `tests/findings` module executes its physics and rewrites
JSON artifacts, so a graph builder that imported its subjects would be slow,
destructive, and would corrupt the very baselines C0.4 relies on.

Three things this handles that a naive import scan gets wrong:

  1. **The kernels are imported flat.** `casim/__init__.py` puts
     `ca-simulation/` on `sys.path`, so `import ca_bcc` inside `src/` resolves
     to a file the scanner must know is a repo module, not a third-party one.

  2. **The `casim.fields.*` shims import by string.** They do
     `importlib.import_module(_m)` over a `_MODULES` list of literals, so an
     `ast.Import` walk sees *nothing*. String literals matching a known module
     name are therefore collected as a separate, weaker evidence class —
     recorded as `dynamic`, never merged with `static`.

  3. **Forks are imported under two different names.** `tests/findings` does
     both `import forks.lgt_fork_A_mc` and bare `import lgt_fork_A_mc` (after
     `sys.path.insert(0, FORKS)`). Both are registered as keys for the same
     node; without the alias, 46 of 47 forks scan as unreferenced, which is
     false.

  4. **Reachability has three defensible definitions and they disagree.**
     `ca_cooling` executes during a `casim run` via `forks/lgt_fork_A_mc` while
     being invisible to a direct-reference scan. Rather than pick silently, this
     reports all three and names `driven` — the least flattering — as the
     headline. (Recommended by `docs/audits/2026-07-29-kernel-coverage-addendum.md`.)

  5. **A `derive_*.py` script is not a library.** The ten derivation scripts and
     the `run_*` / `benchmark_*` entry points are meant to be executed, not
     imported, so "nothing imports it" is their normal state and not evidence of
     death. They carry role `derivation` and are counted separately, so the
     `unreferenced` bucket stays a list of genuine suspects.

Usage:
    python3 tools/gen_module_graph.py             # write the graph
    python3 tools/gen_module_graph.py --check     # exit 1 if stale
    python3 tools/gen_module_graph.py --report    # human summary, no write
    python3 tools/gen_module_graph.py --why ca_cooling   # explain one module
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(_REPO, "docs", "design", "module-graph.json")
MANIFEST = os.path.join(_REPO, "test-results", "manifest.json")

# Roots scanned, in the order their nodes are keyed.
KERNEL_DIRS = ("ca-simulation", "ca-simulation/forks")
PKG_ROOT = "src"
TEST_DIRS = ("tests/findings", "tests/priority", "tests/casim",
             "tests/runners", "tests/falsification")
TOOL_DIR = "tools"

_SKIP = {"__pycache__", ".pytest_cache", "casim.egg-info"}

# The roles that live under `ca-simulation/` and therefore migrate under D6.
# Every one of these needs a manifest record at C0.3.
MIGRATABLE = ("kernel", "fork", "derivation", "support")

# A bare `ca_foo` / `derive_foo` name appearing as a string literal is treated as
# a dynamic module reference. Deliberately narrow: it must be the WHOLE literal,
# so a docstring mentioning ca_gluon in a sentence does not count.
_MODULE_LITERAL = re.compile(r"^(ca_[a-z0-9_]+|derive_[a-z0-9_]+|poisson_open|"
                             r"spinor_color|live_display|viz|tick_heatmap)$")

# Call-site counts. Regex, not AST, and labelled as such in the output: these
# are sizing numbers for C1/C2 planning, not correctness claims.
#
# `scipy` deliberately does NOT match a bare `sp.`. It did in the first
# version, which reported 1,124 scipy sites in `ca-simulation/` — against 13
# actual scipy imports in the whole tree. The repo aliases **sympy** as `sp`
# (63 files do `import sympy as sp`), so nearly every hit was symbolic algebra
# counted as a numerical dependency. C1 sizes its work from these numbers, so
# an inflated one is worse than an absent one.
_NP_SITE = re.compile(r"\b(?:np|numpy)\.")
_SP_SITE = re.compile(r"\bscipy\b")
_FFT_SITE = re.compile(r"\b(?:np|numpy)\.fft\.|\bca_fft\.")

# Finding IDs: F107, FA03, FG7. The trailing boundary must NOT be \b —
# filenames read `F107_canonical_...` and `_` is a word character, so \b never
# matches there. Same fix as gen_manifest.py:50.
_FINDING_RE = re.compile(r"(?<![A-Za-z0-9])(F[A-Z]{0,2}\d{1,3})(?![0-9])")


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------
def git_sha() -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             cwd=_REPO, capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or None if out.returncode == 0 else None
    except Exception:
        return None


def _py_files(reldir: str, recurse: bool) -> list[str]:
    base = os.path.join(_REPO, reldir)
    if not os.path.isdir(base):
        return []
    out = []
    if recurse:
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in _SKIP]
            for fn in filenames:
                if fn.endswith(".py"):
                    out.append(os.path.relpath(os.path.join(dirpath, fn), _REPO))
    else:
        for fn in os.listdir(base):
            full = os.path.join(base, fn)
            if fn.endswith(".py") and os.path.isfile(full):
                out.append(os.path.relpath(full, _REPO))
    return sorted(p.replace(os.sep, "/") for p in out)


def _keys_for(rel: str) -> list[str]:
    """Every name another file could use to import this one, best first.

    Kernels are flat (`ca_bcc`); the package is dotted
    (`casim.engine.channels`); tests and tools are keyed by path because nothing
    imports them by name.

    Forks get **two** keys — `forks.lgt_fork_A_mc` and bare `lgt_fork_A_mc` —
    because `tests/findings` uses both spellings depending on whether the file
    put `ca-simulation/` or `ca-simulation/forks/` on `sys.path`. Registering
    only the dotted form makes 46 of 47 forks scan as unreferenced.
    """
    if rel.startswith("ca-simulation/forks/"):
        stem = os.path.basename(rel)[:-3]
        return [f"forks.{stem}", stem]
    if rel.startswith("ca-simulation/"):
        return [os.path.basename(rel)[:-3]]
    if rel.startswith("src/"):
        dotted = rel[len("src/"):-3].replace("/", ".")
        if dotted.endswith(".__init__"):
            dotted = dotted[:-len(".__init__")]
        return [dotted]
    return [rel]


def _key_for(rel: str) -> str:
    return _keys_for(rel)[0]


def _role_for(rel: str) -> str:
    """A file's role. `derivation` matters: a `derive_*.py` is meant to be RUN,
    not imported, so 'nothing imports it' is its normal state rather than
    evidence of death. Keeping them out of the `kernel` bucket is what stops the
    `unreferenced` list from being padded with ten healthy scripts."""
    base = os.path.basename(rel)
    if rel.startswith("ca-simulation/forks/"):
        return "fork"
    if rel.startswith("ca-simulation/"):
        if base.startswith(("derive_", "run_", "benchmark_")):
            return "derivation"
        if base.startswith("ca_"):
            return "kernel"
        return "support"          # poisson_open, viz, live_display, spinor_color...
    if rel.startswith("src/"):
        return "package"
    if rel.startswith("tools/"):
        return "tool"
    return "test"


class Visitor(ast.NodeVisitor):
    """One pass: imports, dynamic literals, definitions, channel registrations."""

    def __init__(self, module_key: str) -> None:
        self.key = module_key
        self.static: set[str] = set()
        self.dynamic: set[str] = set()
        self.defines: set[str] = set()
        self.channel_types: set[str] = set()
        self._depth = 0

    # -- imports ----------------------------------------------------------
    def visit_Import(self, node: ast.Import) -> None:
        for a in node.names:
            self.static.add(a.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level:                      # relative: resolve against our key
            parts = self.key.split(".")
            base = parts[:max(0, len(parts) - node.level)]
            mod = ".".join(base + ([node.module] if node.module else []))
            self.static.add(mod)
            for a in node.names:            # `from . import x` -> pkg.x
                if not node.module:
                    self.static.add(f"{mod}.{a.name}" if mod else a.name)
        elif node.module:
            self.static.add(node.module)
            for a in node.names:
                self.static.add(f"{node.module}.{a.name}")
        self.generic_visit(node)

    # -- dynamic references ------------------------------------------------
    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, str) and _MODULE_LITERAL.match(node.value):
            self.dynamic.add(node.value)
        self.generic_visit(node)

    # -- definitions and channel registration ------------------------------
    def _record_def(self, node) -> None:
        if self._depth == 0:
            self.defines.add(node.name)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record_def(node)
        self._depth += 1
        self.generic_visit(node)
        self._depth -= 1

    visit_AsyncFunctionDef = visit_FunctionDef        # type: ignore[assignment]

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._record_def(node)
        registered = any(
            (isinstance(d, ast.Name) and d.id == "register")
            or (isinstance(d, ast.Attribute) and d.attr == "register")
            for d in node.decorator_list)
        if registered:
            for stmt in node.body:
                if (isinstance(stmt, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == "type_name"
                                for t in stmt.targets)
                        and isinstance(stmt.value, ast.Constant)
                        and isinstance(stmt.value.value, str)):
                    self.channel_types.add(stmt.value.value)
        self._depth += 1
        self.generic_visit(node)
        self._depth -= 1

    def visit_Assign(self, node: ast.Assign) -> None:
        if self._depth == 0:
            for t in node.targets:
                if isinstance(t, ast.Name):
                    self.defines.add(t.id)
        self.generic_visit(node)


def scan_file(rel: str) -> dict:
    path = os.path.join(_REPO, rel)
    with open(path, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    key = _key_for(rel)
    rec: dict = {
        "path": rel,
        "key": key,
        "lines": src.count("\n") + 1,
        "static_imports": [],
        "dynamic_refs": [],
        "defines": [],
        "channel_types": [],
        "reachable_from": [],
        "doc": "",
        "findings": [],
        "np_sites": len(_NP_SITE.findall(src)),
        "scipy_sites": len(_SP_SITE.findall(src)),
        "fft_sites": len(_FFT_SITE.findall(src)),
        "has_main": "__main__" in src,
    }
    try:
        tree = ast.parse(src, filename=rel)
    except SyntaxError as e:
        rec["unparseable"] = f"{e.msg} (line {e.lineno})"
        return rec
    doc = ast.get_docstring(tree) or ""
    rec["doc"] = doc.splitlines()[0][:180] if doc else ""
    # Findings come from the WHOLE docstring, not just its first line: the
    # convention here is a title line followed by a body that cites the
    # findings, so first-line-only leaves ca_bcc.py and ca_gluon.py — two of
    # the most finding-dense modules in the tree — recorded as citing none.
    rec["findings"] = sorted(
        set(_FINDING_RE.findall(os.path.basename(rel) + " " + doc)),
        key=lambda s: (s[1].isdigit(), s))
    v = Visitor(key)
    v.visit(tree)
    rec["static_imports"] = sorted(v.static)
    rec["dynamic_refs"] = sorted(v.dynamic)
    rec["defines"] = sorted(v.defines)
    rec["channel_types"] = sorted(v.channel_types)
    return rec


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------
def _resolve(name: str, nodes: dict[str, dict], by_key: dict[str, str]) -> str | None:
    """Longest-prefix resolution of an imported name onto a node key.

    `from casim.fields.photon import build_pair_mode` yields the candidate
    `casim.fields.photon.build_pair_mode`; the owning module is the longest
    dotted prefix that is a real node.
    """
    if name in by_key:
        return by_key[name]
    parts = name.split(".")
    for n in range(len(parts) - 1, 0, -1):
        cand = ".".join(parts[:n])
        if cand in by_key:
            return by_key[cand]
    return None


def build() -> dict:
    files: list[str] = []
    for d in KERNEL_DIRS:
        files += _py_files(d, recurse=False)
    files += _py_files(PKG_ROOT, recurse=True)
    for d in TEST_DIRS:
        files += _py_files(d, recurse=False)
    files += _py_files(TOOL_DIR, recurse=False)
    files = [f for f in files if "egg-info" not in f]

    nodes: dict[str, dict] = {}
    for rel in files:
        rec = scan_file(rel)
        rec["role"] = _role_for(rel)
        nodes[rel] = rec

    by_key: dict[str, str] = {}
    for rel, rec in nodes.items():
        for k in _keys_for(rel):
            by_key.setdefault(k, rel)

    # -- edges -------------------------------------------------------------
    for rel, rec in nodes.items():
        edges: dict[str, str] = {}
        for name in rec["static_imports"]:
            tgt = _resolve(name, nodes, by_key)
            if tgt and tgt != rel:
                edges[tgt] = "static"
        for name in rec["dynamic_refs"]:
            tgt = by_key.get(name)
            if tgt and tgt != rel and tgt not in edges:
                edges[tgt] = "dynamic"
        rec["imports"] = sorted(edges)
        rec["import_evidence"] = edges

    for rel, rec in nodes.items():
        rec["imported_by"] = sorted(
            other for other, orec in nodes.items() if rel in orec["imports"])

    # -- reachability, three ways -----------------------------------------
    channel_modules = sorted(r for r, n in nodes.items() if n["channel_types"])
    pkg_entry = sorted(r for r, n in nodes.items() if n["role"] == "package")

    def closure(seed: list[str], skip_roles=("test", "tool")) -> set[str]:
        seen, stack = set(seed), list(seed)
        while stack:
            cur = stack.pop()
            for tgt in nodes[cur]["imports"]:
                if tgt in seen or nodes[tgt]["role"] in skip_roles:
                    continue
                seen.add(tgt)
                stack.append(tgt)
        return seen

    driven = closure(channel_modules)
    pkg_reachable = closure(pkg_entry)
    test_referenced = {t for r, n in nodes.items() if n["role"] == "test"
                       for t in n["imports"]}

    # -- WHICH channels reach each module (roadmap C6) ----------------------
    # `driven` above is a single boolean over the union of all channel closures,
    # which answers "is anything driving this?" but not "what?". The registry's
    # `reachable_from` field (D11) needs the attribution, because that is what
    # turns P6's kernel-coverage survey into a query: one closure per channel
    # module, then the channel TYPES it registers are credited to everything in
    # its closure.
    reach_from: dict[str, set[str]] = {rel: set() for rel in nodes}
    for cm in channel_modules:
        types = nodes[cm]["channel_types"]
        for rel in closure([cm]):
            reach_from[rel].update(types)

    for rel, rec in nodes.items():
        rec["driven"] = rel in driven
        rec["reachable_from"] = sorted(reach_from[rel])
        rec["package_reachable"] = rel in pkg_reachable
        rec["test_referenced"] = rel in test_referenced
        if rec["role"] in MIGRATABLE:
            rec["reach"] = ("driven" if rec["driven"]
                            else "package-only" if rec["package_reachable"]
                            else "test-only" if rec["test_referenced"]
                            else "entry-script" if rec["role"] == "derivation"
                            and rec["has_main"]
                            else "unreferenced")

    # -- tests and result artifacts per module ----------------------------
    manifest = {}
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = json.load(fh)
    mtests = manifest.get("tests", {})
    for rel, rec in nodes.items():
        if rec["role"] not in MIGRATABLE:
            continue
        tests = sorted(t for t in rec["imported_by"] if nodes[t]["role"] == "test")
        rec["tests"] = tests
        res: set[str] = set()
        for t in tests:
            for r in mtests.get(t, {}).get("results", []):
                res.add(r["path"])
        rec["results"] = sorted(res)

    tally: dict[str, dict[str, int]] = {}
    for n in nodes.values():
        if n["role"] not in MIGRATABLE:
            continue
        tally.setdefault(n["role"], {})
        tally[n["role"]][n["reach"]] = tally[n["role"]].get(n["reach"], 0) + 1

    return {
        "version": 1,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "git_sha": git_sha(),
        "criterion": {
            "driven": "in the transitive import closure of a module that "
                      "registers a Channel (the headline; least flattering)",
            "package-only": "reachable from src/casim but not from any "
                            "registered channel — CLI, suite, analysis, shims",
            "test-only": "referenced only by tests",
            "entry-script": "a derive_*/run_* script with a __main__ that "
                            "nothing imports — meant to be RUN, not a defect",
            "unreferenced": "nothing in the tree references it",
            "note": "Edges are `static` (an ast.Import) or `dynamic` (a string "
                    "literal naming a module — how casim.fields.* shims work). "
                    "np/scipy/fft site counts are REGEX, for C1/C2 sizing only.",
        },
        "summary": {
            "files": len(nodes),
            "migratable": sum(1 for n in nodes.values() if n["role"] in MIGRATABLE),
            "kernels": sum(1 for n in nodes.values() if n["role"] == "kernel"),
            "forks": sum(1 for n in nodes.values() if n["role"] == "fork"),
            "derivations": sum(1 for n in nodes.values() if n["role"] == "derivation"),
            "support": sum(1 for n in nodes.values() if n["role"] == "support"),
            "package": sum(1 for n in nodes.values() if n["role"] == "package"),
            "tests": sum(1 for n in nodes.values() if n["role"] == "test"),
            "channel_modules": len(channel_modules),
            "channel_types": sorted(
                {t for n in nodes.values() for t in n["channel_types"]}),
            "reach": tally,
            "np_sites_total": sum(n["np_sites"] for n in nodes.values()),
            "fft_sites_total": sum(n["fft_sites"] for n in nodes.values()),
            "dynamic_edges": sum(
                1 for n in nodes.values()
                for e in n["import_evidence"].values() if e == "dynamic"),
            "unparseable": sorted(r for r, n in nodes.items() if "unparseable" in n),
        },
        "nodes": nodes,
    }


# ---------------------------------------------------------------------------
def report(g: dict) -> None:
    s = g["summary"]
    print(f"\nmodule graph  (git {g['git_sha']})")
    print(f"  files scanned        {s['files']}")
    print(f"    MIGRATABLE         {s['migratable']}   "
          f"(everything under ca-simulation/ — needs a C0.3 manifest record)")
    print(f"      kernels          {s['kernels']}")
    print(f"      forks            {s['forks']}")
    print(f"      derivations      {s['derivations']}")
    print(f"      support          {s['support']}")
    print(f"    package            {s['package']}")
    print(f"    tests              {s['tests']}")
    print(f"  channel modules      {s['channel_modules']} "
          f"({len(s['channel_types'])} channel types)")
    print(f"  dynamic edges        {s['dynamic_edges']}  "
          f"(string-literal imports an AST walk alone would miss)")
    print(f"  np. sites            {s['np_sites_total']}  "
          f"(regex; C1 sizing)")
    print(f"  fft sites            {s['fft_sites_total']}")
    print("\n  reachability, by role")
    cols = ("driven", "package-only", "test-only", "entry-script", "unreferenced")
    print(f"    {'':<12s}" + "".join(f"{c:>14s}" for c in cols))
    for role in MIGRATABLE:
        row = s["reach"].get(role, {})
        print(f"    {role:<12s}" + "".join(f"{row.get(c, 0):>14d}" for c in cols))
    if s["unparseable"]:
        print(f"\n  UNPARSEABLE ({len(s['unparseable'])}):")
        for p in s["unparseable"]:
            print(f"    {p}  — {g['nodes'][p]['unparseable']}")


def why(g: dict, name: str) -> int:
    nodes = g["nodes"]
    hits = [r for r, n in nodes.items()
            if n["key"] == name or os.path.basename(r) in (name, name + ".py")]
    if not hits:
        print(f"no module matching {name!r}")
        return 1
    for rel in hits:
        n = nodes[rel]
        print(f"\n{rel}   [{n['role']}]  {n['lines']} lines")
        if n["doc"]:
            print(f"  {n['doc']}")
        if n["role"] in ("kernel", "fork"):
            print(f"  reach          {n['reach']}"
                  f"   (driven={n['driven']}, pkg={n['package_reachable']},"
                  f" tests={n['test_referenced']})")
        print(f"  np/scipy/fft   {n['np_sites']}/{n['scipy_sites']}/{n['fft_sites']}")
        if n["channel_types"]:
            print(f"  registers      {', '.join(n['channel_types'])}")
        print(f"  imports        {len(n['imports'])}")
        for t in n["imports"]:
            print(f"    -> {t}  [{n['import_evidence'][t]}]")
        print(f"  imported by    {len(n['imported_by'])}")
        for t in n["imported_by"][:20]:
            print(f"    <- {t}")
        if len(n["imported_by"]) > 20:
            print(f"    ... and {len(n['imported_by']) - 20} more")
        if n.get("results"):
            print(f"  result artifacts  {len(n['results'])}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the graph on disk is missing or stale")
    ap.add_argument("--report", action="store_true", help="summarise, do not write")
    ap.add_argument("--why", metavar="MODULE",
                    help="explain one module's edges and reachability")
    args = ap.parse_args()

    g = build()

    if args.why:
        return why(g, args.why)
    if args.report:
        report(g)
        return 0
    if args.check:
        if not os.path.exists(OUT):
            print("module-graph.json is missing — run "
                  "`python3 tools/gen_module_graph.py`")
            return 1
        with open(OUT, encoding="utf-8") as fh:
            old = json.load(fh)
        a = {k: v for k, v in old.items() if k not in ("generated", "git_sha")}
        b = {k: v for k, v in g.items() if k not in ("generated", "git_sha")}
        if a != b:
            print("module-graph.json is stale — run "
                  "`python3 tools/gen_module_graph.py`")
            return 1
        print("module-graph.json is current")
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(g, fh, indent=1, sort_keys=True)
        fh.write("\n")
    report(g)
    print(f"\nwrote {os.path.relpath(OUT, _REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
