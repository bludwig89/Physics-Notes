#!/usr/bin/env python3
"""C9 blocker 1 — repoint the whole ``tests/`` tree off ``ca-simulation/``.

Fourth tool of this shape (after ``route_numerics.py`` C1, ``_c5_repoint_sites.py``
C5 and C6's re-router), and the last: its subject stops existing at C9. Every one
of the 106 legacy module names the tests import has a manifest ``target:``, so the
rewrite is a table lookup with no judgment in it — see
``docs/status/C9-readiness.md`` §"Blocker 1".

Four passes, each with its own proof obligation:

  A. **import statements** — ``import ca_X as A`` / ``import ca_X`` /
     ``from ca_X import a, b``.  The local name must survive verbatim: 218 files
     use the alias form and their call sites say ``bcc.foo()``. Rewritten files
     are re-parsed and the set of names bound by imports must be unchanged.

  B. **fork file-path loads** — six tests reach a fork with
     ``spec_from_file_location(..., ".../ca-simulation/forks/gr_fork_X.py")``.
     Invisible to an import rewriter (C6 learned this the hard way, twice
     silently inside ``try/except -> None``), so the path *literals* are
     rewritten from the same manifest.

  C. **sys.path plumbing** — the ``ca-simulation`` preamble is now dead. It is
     removed statement-by-statement off the AST (not by line regex: 24 of them
     are multi-line), and a self-contained ``src`` bootstrap is substituted so
     standalone ``python3 tests/findings/test_X.py`` keeps working exactly as it
     did. Files that already bootstrap ``src`` get the block dropped outright.

  D. **prose** — docstrings and comments naming ``ca-simulation/...`` are
     repointed to the module's new home, because C9's acceptance gate greps
     ``--include=*.md --include=*.py`` and does not care that a hit is a comment.

Usage::

    python3 tools/repoint_tests.py --dry-run       # report only
    python3 tools/repoint_tests.py                 # apply
    python3 tools/repoint_tests.py --check         # exit 1 if any hit remains
"""
from __future__ import annotations

import ast
import os
import re
import sys

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")
TESTS = os.path.join(_REPO, "tests")

# Self-contained `src` bootstrap. Underscore aliases so it cannot collide with
# whatever the file already imports, and so a later reader can see at a glance
# that these two lines are plumbing and not part of the test.
BOOTSTRAP = (
    "import os as _os, sys as _sys  # noqa: E401\n"
    "_sys.path.insert(0, _os.path.join(\n"
    "    _os.path.dirname(_os.path.abspath(__file__)), \"..\", \"..\", \"src\"))\n"
)


# --------------------------------------------------------------------------- #
# the table
# --------------------------------------------------------------------------- #
def load_manifest() -> list[dict]:
    with open(MANIFEST, encoding="utf-8") as fh:
        return yaml.safe_load(fh)["modules"]


def module_map(recs: list[dict]) -> dict[str, str]:
    """bare legacy module name -> dotted ``casim`` path (top-level kernels)."""
    out: dict[str, str] = {}
    for r in recs:
        src, tgt = r["source"], r["target"]
        if "/forks/" in src or not tgt.startswith("src/"):
            continue
        out[os.path.basename(src)[:-3]] = tgt[len("src/"):-3].replace("/", ".")
    out.pop("__init__", None)
    return out


def path_map(recs: list[dict]) -> dict[str, str]:
    """repo-relative source path -> repo-relative target path (all 171)."""
    return {r["source"]: r["target"] for r in recs}


# --------------------------------------------------------------------------- #
# pass A — import statements
# --------------------------------------------------------------------------- #
def bound_names(src: str) -> set[str]:
    names: set[str] = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return names
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                names.add(a.asname or a.name.split(".")[0])
    return names


def pass_a(text: str, mods: dict[str, str]) -> tuple[str, int]:
    out, n = [], 0
    for line in text.splitlines(keepends=True):
        new = line
        for old, dotted in mods.items():
            pkg, leaf = dotted.rsplit(".", 1)
            m = re.match(rf"^(\s*)from\s+{old}\s+import\s+(.*)$", line, re.S)
            if m:
                new = f"{m.group(1)}from {dotted} import {m.group(2)}"
                break
            m = re.match(rf"^(\s*)import\s+{old}\s+as\s+(\w+)(.*)$", line, re.S)
            if m:
                new = (f"{m.group(1)}from {pkg} import {leaf} as "
                       f"{m.group(2)}{m.group(3)}")
                break
            m = re.match(rf"^(\s*)import\s+{old}\s*(#.*)?$", line.rstrip("\n"))
            if m:
                tail = f"  {m.group(2)}" if m.group(2) else ""
                new = f"{m.group(1)}from {pkg} import {leaf} as {old}{tail}\n"
                break
        if new != line:
            n += 1
        out.append(new)
    return "".join(out), n


# --------------------------------------------------------------------------- #
# pass B/D — path and prose literals
# --------------------------------------------------------------------------- #
_FLAT = re.compile(r"ca-simulation/[\w./-]+\.py")
_JOIN = re.compile(
    r"""(?P<q>["'])ca-simulation\1(?P<rest>(?:\s*,\s*["'][\w.\-]+["'])+)""")
_PART = re.compile(r"""["']([\w.\-]+)["']""")


def pass_bd(text: str, paths: dict[str, str]) -> tuple[str, int]:
    """Rewrite every ``ca-simulation/...`` *path literal* to its target.

    Covers both the ``os.path.join(..., "ca-simulation", "forks", "x.py")``
    spelling and the flat ``ca-simulation/forks/x.py`` one used in prose. Two
    regexes rather than 171, because this runs over 347 files.
    """
    if "ca-simulation" not in text:
        return text, 0
    n = 0

    def _flat(m: re.Match) -> str:
        nonlocal n
        tgt = paths.get(m.group(0))
        if not tgt:
            return m.group(0)
        n += 1
        return tgt

    text = _FLAT.sub(_flat, text)

    def _join(m: re.Match) -> str:
        nonlocal n
        parts = ["ca-simulation"] + _PART.findall(m.group("rest"))
        tgt = paths.get("/".join(parts))
        if not tgt:
            return m.group(0)
        n += 1
        return ", ".join(f'"{p}"' for p in tgt.split("/"))

    return _JOIN.sub(_join, text), n


# --------------------------------------------------------------------------- #
# pass C — sys.path plumbing
# --------------------------------------------------------------------------- #
def _seg(text_lines: list[str], node: ast.AST) -> str:
    return "".join(text_lines[node.lineno - 1:node.end_lineno])


def _is_path_stmt(seg: str) -> bool:
    return "sys.path" in seg or "_sys.path" in seg


def _is_syspath(node: ast.AST) -> bool:
    """``sys.path`` / ``_sys.path`` as an expression."""
    return (isinstance(node, ast.Attribute) and node.attr == "path"
            and isinstance(node.value, ast.Name)
            and node.value.id in ("sys", "_sys"))


def _is_pathcall(node: ast.AST) -> bool:
    """``sys.path.insert(...)`` / ``sys.path.append(...)`` as a statement."""
    if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
        return False
    f = node.value.func
    return (isinstance(f, ast.Attribute) and f.attr in ("insert", "append")
            and _is_syspath(f.value))


def _is_path_test(node: ast.AST) -> bool:
    """``x not in sys.path`` — possibly one half of a ``BoolOp``."""
    if isinstance(node, ast.BoolOp):
        return any(_is_path_test(v) for v in node.values)
    return isinstance(node, ast.Compare) and any(
        _is_syspath(c) for c in node.comparators)


def _plumbing_only(st: ast.stmt) -> bool:
    """Is this statement nothing but path scaffolding?

    Used for the ``for cand in (…): if cand not in sys.path: insert`` shape
    (35 files). A bare ``Assign`` counts as scaffolding only *inside* such a
    loop, which is why this is never applied to a statement on its own — the
    caller additionally requires a real ``sys.path`` call somewhere below.
    """
    if _is_pathcall(st):
        return True
    if isinstance(st, ast.If) and not st.orelse and st.body:
        return all(_plumbing_only(x) for x in st.body)
    if isinstance(st, ast.Assign) and len(st.targets) == 1 \
            and isinstance(st.targets[0], ast.Name):
        return True
    return isinstance(st, ast.Pass)


def _has_pathcall(st: ast.stmt) -> bool:
    return any(_is_pathcall(x) for x in ast.walk(st))


def _mentions(lines: list[str], st: ast.stmt, plumb: set[str]) -> bool:
    seg = _seg(lines, st)
    return "ca-simulation" in seg or any(
        re.search(rf"\b{re.escape(p)}\b", seg) for p in plumb)


def pass_c(text: str) -> tuple[str, int, bool]:
    """Delete the dead ``ca-simulation`` sys.path preamble.

    Returns ``(new_text, statements_removed, needs_bootstrap)``. Only
    module-level statements and the bodies of module-level ``if`` blocks are
    considered — that is where all 262 preambles live, and anything else is
    reported rather than guessed at.
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return text, 0, False
    lines = text.splitlines(keepends=True)

    # 1. names whose *value* is the legacy directory (SIM, FORKS, _cand, ...)
    plumb: set[str] = set()
    for _ in range(4):                          # transitive: FORKS = join(SIM,…)
        grew = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            t = node.targets[0]
            if not isinstance(t, ast.Name):
                continue
            seg = _seg(lines, node)
            hit = "ca-simulation" in seg or any(
                re.search(rf"\b{re.escape(p)}\b", seg) for p in plumb)
            if hit and t.id not in plumb:
                plumb.add(t.id)
                grew = True
        if not grew:
            break

    # 2. a plumbing name used for anything but sys.path disqualifies deletion.
    #    One pass: map each line to the innermost statement covering it, then
    #    ask whether every statement mentioning the name is path plumbing.
    owner: dict[int, ast.stmt] = {}
    for s in ast.walk(tree):
        if not isinstance(s, ast.stmt):
            continue
        for ln in range(s.lineno, (s.end_lineno or s.lineno) + 1):
            prev = owner.get(ln)
            if prev is None or (s.end_lineno or s.lineno) - s.lineno <= \
                    (prev.end_lineno or prev.lineno) - prev.lineno:
                owner[ln] = s
    for name in sorted(plumb):
        pat = re.compile(rf"\b{re.escape(name)}\b")
        for node in ast.walk(tree):
            if not isinstance(node, ast.Name) or node.id != name:
                continue
            st = owner.get(node.lineno)
            if st is None:
                continue
            seg = _seg(lines, st)
            if not (_is_path_stmt(seg) or pat.match(seg.strip())):
                plumb.discard(name)
                break

    # 3. statements to drop. **Structural, never "the text contains
    #    sys.path".** The text test deletes the enclosing `def` or `try` when a
    #    plumbing line sits inside one — 2 files in this tree, and it silently
    #    removes a whole assertion, which is the worst possible failure here.
    drop: list[tuple[int, int]] = []
    toplevel = {id(st) for st in tree.body}
    for st in ast.walk(tree):
        if not isinstance(st, ast.stmt):
            continue
        legacy_or_plumb = _mentions(lines, st, plumb)
        if _is_pathcall(st):
            if legacy_or_plumb:
                drop.append((st.lineno, st.end_lineno, id(st) in toplevel))
        elif isinstance(st, ast.Assign) and len(st.targets) == 1 \
                and isinstance(st.targets[0], ast.Name) \
                and st.targets[0].id in plumb:
            drop.append((st.lineno, st.end_lineno, id(st) in toplevel))
        elif isinstance(st, ast.If) and st.body and not st.orelse \
                and all(_is_pathcall(x) for x in st.body) \
                and _is_path_test(st.test) and legacy_or_plumb:
            drop.append((st.lineno, st.end_lineno, id(st) in toplevel))
        elif isinstance(st, ast.For) and not st.orelse and st.body \
                and all(_plumbing_only(x) for x in st.body) \
                and _has_pathcall(st) and legacy_or_plumb:
            # `for cand in (…, ".../ca-simulation"): … sys.path.insert(…)`,
            # and `for p in (SIM, FORKS):` whose names this pass just deleted —
            # leaving that loop behind is a NameError, not a stale comment.
            drop.append((st.lineno, st.end_lineno, id(st) in toplevel))

    if not drop:
        return text, 0, False

    # A nested drop must not pull a module-level bootstrap into a function body.
    tops = [a for a, _, top in drop if top]
    first = min(tops) if tops else -1
    kill: set[int] = set()
    for a, b, _ in drop:
        kill.update(range(a, (b or a) + 1))

    # `src` may have been *inside* the block just deleted (four files put both
    # directories in one tuple), so ask the survivors, not the original.
    survivors = "".join(l for i, l in enumerate(lines, start=1) if i not in kill)
    keeps_src = bool(re.search(r"[\"']src[\"']", survivors))

    out: list[str] = []
    inserted = False
    for i, line in enumerate(lines, start=1):
        if i in kill:
            if i == first and not keeps_src and not inserted:
                out.append(BOOTSTRAP)
                inserted = True
            continue
        out.append(line)
    return "".join(out), len(drop), inserted


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #
def test_files() -> list[str]:
    found = []
    for root, dirs, files in os.walk(TESTS):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in sorted(files):
            if f.endswith(".py"):
                found.append(os.path.join(root, f))
    return sorted(found)


def main() -> int:
    dry = "--dry-run" in sys.argv
    check = "--check" in sys.argv
    recs = load_manifest()
    mods, paths = module_map(recs), path_map(recs)

    if check:
        bad = [os.path.relpath(p, _REPO) for p in test_files()
               if "ca-simulation" in open(p, encoding="utf-8").read()]
        for b in bad:
            print(f"  STALE {b}")
        print(f"\n  {len(bad)} test file(s) still reference ca-simulation")
        return 1 if bad else 0

    touched = refused = 0
    counts = {"A": 0, "B": 0, "C": 0}
    residual: list[str] = []
    for path in test_files():
        rel = os.path.relpath(path, _REPO)
        # conftest.py is the tree's own bootstrap and is edited by hand: it
        # must put `src` on sys.path for every subtree, which pass C would
        # read as plumbing to delete.
        if rel == "tests/conftest.py":
            continue
        with open(path, encoding="utf-8") as fh:
            before = fh.read()
        text, na = pass_a(before, mods)
        text, nb = pass_bd(text, paths)
        text, nc, _ = pass_c(text)
        if text == before:
            continue

        try:
            ast.parse(text, filename=rel)
        except SyntaxError as e:
            print(f"  REFUSED {rel}: rewritten copy does not parse ({e.msg} "
                  f"line {e.lineno})")
            refused += 1
            continue
        lost = bound_names(before) - bound_names(text)
        lost -= set(mods)          # a bare `import ca_X` keeps its name via `as`
        if lost:
            print(f"  REFUSED {rel}: rewrite dropped local name(s) {sorted(lost)}")
            refused += 1
            continue

        counts["A"] += na
        counts["B"] += nb
        counts["C"] += nc
        touched += 1
        if "ca-simulation" in text:
            residual.append(rel)
        print(f"  {'dry ' if dry else 'ok  '} {rel:<58s} "
              f"A={na} B={nb} C={nc}")
        if not dry:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)

    print(f"\n  {touched} file(s) repointed — "
          f"{counts['A']} import line(s), {counts['B']} path literal(s), "
          f"{counts['C']} plumbing statement(s) removed")
    if residual:
        print(f"  {len(residual)} file(s) still mention ca-simulation "
              f"(fix by hand):")
        for r in residual:
            print("    " + r)
    if refused:
        print(f"  {refused} file(s) REFUSED — left untouched")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
