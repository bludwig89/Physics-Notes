#!/usr/bin/env python3
"""Route `np.fft.*` transform calls through the façade — roadmap C1.3 (D8).

179 transform call sites across 39 files. Doing that by hand invites a typo in
a physics kernel; doing it with `sed` invites a silent one. So this does the
substitution mechanically and then **proves** three things about the result:

  1. the file still parses;
  2. **no `np.fft.<transform>` remains** — the point of the exercise;
  3. every substituted name resolves on the façade, checked against the real
     module rather than a hard-coded list, so a rename in `casim.numerics.fft`
     cannot leave this tool silently rewriting calls to something that is not
     there.

Two deliberate non-targets:

  * **`fftfreq` and `rfftfreq` stay on numpy.** They are pure index arithmetic —
    no transform, no threads, no device. Routing them would add 84 diff lines
    and change nothing about the seam. The façade re-exports them for callers
    who want one import.
  * **`np.fft` inside `casim/numerics/` itself.** That is where numpy is
    supposed to be called.

Binding, by location:

  * `ca-simulation/**`  ->  `import ca_fft as _fft`
    the idiom already used by `ca_bcc`, `ca_gluon` and `ca_wmu`. Since C1.1,
    `ca_fft` is a shim onto `casim.numerics.fft` that also bootstraps `src/`
    onto `sys.path`, so this reaches the seam with no new failure mode. It
    becomes `from casim.numerics import fft` when the file moves at C3-C6.
  * `src/casim/**`      ->  `from casim.numerics import fft as _fft`

Usage:
    python3 tools/route_numerics.py --list
    python3 tools/route_numerics.py --file ca-simulation/poisson_open.py
    python3 tools/route_numerics.py --all --dry-run
    python3 tools/route_numerics.py --all
"""
from __future__ import annotations

import argparse
import ast
import os
import re
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "src"))

# Transforms that must route through the seam. NOT fftfreq/rfftfreq.
TRANSFORMS = ("fftn", "ifftn", "fft2", "ifft2", "rfftn", "irfftn",
              "rfft", "irfft", "fft", "ifft")

ROOTS = ("ca-simulation", "src/casim")
EXEMPT = ("src/casim/numerics/",)
_SKIP_DIRS = {"__pycache__", ".pytest_cache", "casim.egg-info"}

KERNEL_IMPORT = "import ca_fft as _fft"
PKG_IMPORT = "from casim.numerics import fft as _fft"

# `np.fft.fftn(` / `numpy.fft.fftn(`. The trailing `\b` with a negative
# lookahead on `freq` is what keeps `fftfreq` out: a plain `fft` alternative
# would match the first three characters of `fftfreq` and rewrite it.
_CALL = re.compile(
    r"\b(?:np|numpy)\.fft\.(" + "|".join(TRANSFORMS) + r")\b(?!freq)")


def _facade_names() -> set[str]:
    """What the façade actually exports, read from the module, not assumed."""
    from casim.numerics import fft as _f
    return {n for n in TRANSFORMS if callable(getattr(_f, n, None))}


def candidates() -> list[str]:
    out = []
    for root in ROOTS:
        base = os.path.join(_REPO, root)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn),
                                      _REPO).replace(os.sep, "/")
                if rel.startswith(EXEMPT):
                    continue
                with open(os.path.join(_REPO, rel), encoding="utf-8",
                          errors="replace") as fh:
                    if _CALL.search(fh.read()):
                        out.append(rel)
    return sorted(out)


def _binds_fft(tree: ast.Module) -> bool:
    """Is the name `_fft` already bound by an import in this module?"""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if (a.asname or a.name.split(".")[0]) == "_fft":
                    return True
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                if (a.asname or a.name) == "_fft":
                    return True
    return False


def _insert_import(src: str, rel: str) -> str:
    """Add the `_fft` binding after the last top-level import.

    Placed after the existing import block rather than at line 0 so it lands
    below any `sys.path` manipulation the file does — several kernels insert a
    directory onto the path before importing their siblings, and an import
    hoisted above that would fail.
    """
    stmt = PKG_IMPORT if rel.startswith("src/") else KERNEL_IMPORT
    tree = ast.parse(src)
    last = None
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last = node
    lines = src.splitlines(keepends=True)
    if last is None:                       # no imports: after the docstring
        doc_end = 0
        if (tree.body and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)):
            doc_end = tree.body[0].end_lineno
        at = doc_end
    else:
        at = last.end_lineno
    comment = "  # roadmap C1.3: route FFTs through casim.numerics\n"
    lines.insert(at, stmt + comment)
    return "".join(lines)


def route(rel: str, dry: bool, names: set[str]) -> tuple[int, str]:
    """Returns (sites rewritten, message)."""
    path = os.path.join(_REPO, rel)
    with open(path, encoding="utf-8") as fh:
        src = fh.read()

    found = set(_CALL.findall(src))
    missing = sorted(found - names)
    if missing:
        return 0, (f"REFUSED: façade has no {', '.join(missing)} — add them to "
                   f"casim.numerics.fft before routing this file")

    new, n = _CALL.subn(lambda m: f"_fft.{m.group(1)}", src)
    if n == 0:
        return 0, "no transform sites"

    tree = ast.parse(new, filename=rel)
    if not _binds_fft(tree):
        new = _insert_import(new, rel)

    try:
        ast.parse(new, filename=rel)
    except SyntaxError as e:
        return 0, f"REFUSED: result does not parse ({e.msg}, line {e.lineno})"
    if _CALL.search(new):
        return 0, "REFUSED: a transform site survived the rewrite"

    if not dry:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
    return n, f"{n} site(s)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    names = _facade_names()
    todo = candidates()

    if args.list:
        print(f"\n{len(todo)} file(s) with np.fft transform sites "
              f"(fftfreq excluded — pure index arithmetic)\n")
        total = 0
        for rel in todo:
            with open(os.path.join(_REPO, rel), encoding="utf-8") as fh:
                n = len(_CALL.findall(fh.read()))
            total += n
            print(f"  {n:>4d}  {rel}")
        print(f"\n  {total} transform site(s) total")
        return 0

    targets = [args.file] if args.file else (todo if args.all else [])
    if not targets:
        ap.print_help()
        return 1

    grand = 0
    refused = []
    for rel in targets:
        n, msg = route(rel, args.dry_run, names)
        grand += n
        mark = "would route" if args.dry_run else "routed"
        if msg.startswith("REFUSED"):
            refused.append(f"{rel}: {msg}")
            print(f"  !!  {rel}: {msg}")
        elif n:
            print(f"  {mark} {n:>3d}  {rel}")
    print(f"\n  {grand} site(s) {'would be ' if args.dry_run else ''}routed"
          + (f", {len(refused)} refused" if refused else ""))
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
