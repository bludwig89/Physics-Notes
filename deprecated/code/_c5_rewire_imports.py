#!/usr/bin/env python3
"""C5 — rewire every `src/` import of a migrated particles kernel.

Same job C4 did for the gauge sector, and it does NOT trust the substitution:
each edited file is re-parsed, and every rewritten line is checked to still
bind the same local names it bound before. Three shapes appear in the tree and
each has its own rule:

  from ca_X import a, b      ->  from casim.engine.particles.z import a, b
  import ca_X as A           ->  from casim.engine.particles import z as A
  import ca_X                ->  from casim.engine.particles import z as ca_X
                                 (bare form: call sites say `ca_X.foo()`, so the
                                  local name must survive verbatim)

The `importlib.import_module("ca_X")` string layer is handled separately and by
hand — the C3.4 shim checker is import-statement-based and cannot see it, which
is exactly the trap C4's handoff note warned about.
"""
from __future__ import annotations

import ast
import os
import re
import sys

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")


def dotted_targets(sector: str | None = None) -> dict[str, str]:
    """Already-migrated kernels, old bare name -> new dotted path.

    Two scopes, because ownership differs by where the *importing* file lives:

      * inside `engine/particles/` — this session owns the file outright, so
        every migrated kernel it imports is rewired. The newly migrated modules
        import `ca_bcc`, `ca_fft`, `ca_lattice` (C1/C3) and their own siblings
        by bare name, and the moment they live under `src/` those become shim
        imports from inside the package, which the C3.4 gate correctly refuses.
      * everywhere else — only imports OF a particles kernel are rewired.
        Rewiring someone else's kernel reference in a shared file means two
        sessions editing the same lines, which is the collision itself.
    """
    m = yaml.safe_load(open(MANIFEST, encoding="utf-8"))
    out = {}
    for r in m["modules"]:
        if not r.get("migrated"):
            continue
        if sector and r["sector"] != sector:
            continue
        target = r["target"]
        if not target.startswith("src/"):
            continue
        old = os.path.basename(r["source"])[:-3]
        out[old] = target[len("src/"):-3].replace("/", ".")
    return out


def foreign_sector_dirs(my_session: str) -> list[str]:
    """`engine/<sector>/` directories claimed by a DIFFERENT live session.

    A C6 session (`nifty-great-volta`) claimed `interactions` and `forks` three
    minutes after this session claimed `particles`, and is writing those trees
    right now. Rewiring a file another session is mid-migration on is how the
    F110/F129/F262 collisions happened. Their shim imports are their phase's
    acceptance gate, not this one's — so those directories are skipped, by
    reading the claim rather than by a hardcoded list.
    """
    m = yaml.safe_load(open(MANIFEST, encoding="utf-8"))
    dirs = []
    for sector, claim in (m.get("claims") or {}).items():
        if claim.get("session") == my_session:
            continue
        d = os.path.join("src", "casim", "engine", sector)
        if os.path.isdir(os.path.join(_REPO, d)):
            dirs.append(d + os.sep)
    return dirs


def bound_names(src: str) -> set[str]:
    """Every local name bound by an import statement in this file."""
    names = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return names
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                names.add(a.asname or a.name.split(".")[0])
    return names


def rewrite(text: str, mods: dict[str, str]) -> tuple[str, int]:
    n = 0
    out = []
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
            # Bare `import ca_X`, with or without a trailing comment. Call
            # sites say `ca_X.foo()`, so the local name must survive verbatim.
            m = re.match(rf"^(\s*)import\s+{old}\s*(#.*)?$", line.rstrip("\n"))
            if m:
                tail = f"  {m.group(2)}" if m.group(2) else ""
                new = f"{m.group(1)}from {pkg} import {leaf} as {old}{tail}\n"
                break
        if new != line:
            n += 1
        out.append(new)
    return "".join(out), n


MY_SECTOR = "particles"
MY_DIR = os.path.join("src", "casim", "engine", MY_SECTOR) + os.sep


def main() -> int:
    mine = dotted_targets(MY_SECTOR)          # imports OF a particles kernel
    everything = dotted_targets(None)         # only applied inside MY_DIR
    if not mine:
        print("no migrated particles records — nothing to rewire")
        return 1
    dry = "--dry-run" in sys.argv
    session = "gifted-nifty-euler"
    skip_dirs = foreign_sector_dirs(session)
    for d in skip_dirs:
        print(f"  skipping {d} — claimed by another live session")
    total_files = total_lines = 0
    skipped = 0
    failed = []

    for root, dirs, files in os.walk(os.path.join(_REPO, "src")):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in sorted(files):
            if not f.endswith(".py"):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, _REPO)
            with open(path, encoding="utf-8") as fh:
                before = fh.read()
            after, n = rewrite(before, everything if rel.startswith(MY_DIR)
                               else mine)
            if not n:
                continue
            if any(rel.startswith(d) for d in skip_dirs):
                skipped += 1
                continue
            # Proof obligations: still parses, and binds the same local names.
            try:
                ast.parse(after, filename=rel)
            except SyntaxError as e:
                failed.append(f"{rel}: rewritten copy does not parse ({e.msg})")
                continue
            lost = bound_names(before) - bound_names(after)
            if lost:
                failed.append(f"{rel}: rewrite dropped local name(s) {sorted(lost)}")
                continue
            total_files += 1
            total_lines += n
            print(f"  {'dry ' if dry else 'ok  '} {rel:<52s} {n} line(s)")
            if not dry:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(after)

    print(f"\n  {total_files} file(s), {total_lines} import line(s) rewired"
          + (f"; {skipped} file(s) left to their owning session" if skipped else ""))
    if failed:
        print("  REFUSED:")
        for x in failed:
            print("    " + x)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
