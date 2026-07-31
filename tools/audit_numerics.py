#!/usr/bin/env python3
"""Numerics-import ratchet — roadmap C1.5 (decision D8).

D8 says no physics module imports `numpy`, `scipy` or `ca_fft` directly; they
go through `casim.numerics`. That cannot be done in one pass — it is 169 files
— and a migration with no instrument is a migration nobody can tell is
progressing. So, exactly the shape P1.3 used for import-time side effects:
**measure, record a high-water mark, and fail if it rises.**

The numbers can only go down. `--list` names the files still to do.

Three exemptions, and each is a real distinction rather than a convenience:

  * `casim/numerics/**` — the façade IS the place numpy is imported. Banning it
    there would be incoherent.
  * `tools/**`, `tests/**` — these are not physics modules. A test may import
    numpy to build a fixture, and every tool here does AST work on the tree.
  * `sympy` — symbolic algebra, not a numerical backend. 63 files do
    `import sympy as sp`, and an earlier version of the module-graph regex
    counted every `sp.` as scipy and reported 1,124 scipy sites against 13 real
    ones. Miscounting is how a ratchet loses its authority.

Usage:
    python3 tools/audit_numerics.py                 # report
    python3 tools/audit_numerics.py --list          # name the files
    python3 tools/audit_numerics.py --ratchet       # exit 1 on regression
    python3 tools/audit_numerics.py --update        # accept a new low-water mark
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(_REPO, "tools", "numerics_health_baseline.json")

# Scanned: everything that is or will become a physics module.
ROOTS = ("ca-simulation", "src/casim")

# Not physics modules, or the façade itself.
EXEMPT_PREFIXES = (
    "src/casim/numerics/",
    "tools/",
    "tests/",
)

BANNED_ROOTS = {"numpy", "scipy", "ca_fft"}

# `np.fft.<transform>(` — NOT fftfreq/rfftfreq (pure index arithmetic).
_FFT_CALL = __import__("re").compile(
    r"\b(?:np|numpy)\.fft\.(fftn|ifftn|fft2|ifft2|rfftn|irfftn|rfft|irfft|fft|ifft)\b(?!freq)")

# `ca_fft` is TRANSITIONAL, not a violation of the same kind as the others.
# Since C1.1 it is a shim onto `casim.numerics.fft`, so a call through it DOES
# reach the seam. C1.3 deliberately raised this count from 17 to 42 by
# converting 161 direct `np.fft.*` transform calls in 25 kernels into
# seam-routed ones — trading a worse dependency for a better one. It becomes
# `from casim.numerics import fft` when each file moves at C3-C6.
#
# Tracked separately and ratcheted separately, because a single number that
# went UP while the tree got BETTER is a number nobody would trust again.
TRANSITIONAL = {"ca_fft"}
_SKIP_DIRS = {"__pycache__", ".pytest_cache", "casim.egg-info"}


def _py_files() -> list[str]:
    out: list[str] = []
    for root in ROOTS:
        base = os.path.join(_REPO, root)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), _REPO)
                rel = rel.replace(os.sep, "/")
                if rel.startswith(EXEMPT_PREFIXES):
                    continue
                out.append(rel)
    return sorted(out)


def _offending_imports(path: str) -> list[str]:
    """Banned module roots imported by this file. AST, never import."""
    with open(os.path.join(_REPO, path), encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError:
        return []
    hits: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                root = a.name.split(".")[0]
                if root in BANNED_ROOTS:
                    hits.add(root)
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in BANNED_ROOTS:
                hits.add(root)
    return sorted(hits)


def _fft_call_sites(path: str) -> int:
    """Direct `np.fft.<transform>` calls — the thing C1.3 removed.

    Excludes `fftfreq`/`rfftfreq`: pure index arithmetic, no transform, no
    threads, no device. Routing them would add diff noise and change nothing
    about the seam.
    """
    with open(os.path.join(_REPO, path), encoding="utf-8", errors="replace") as fh:
        return len(_FFT_CALL.findall(fh.read()))


def scan() -> dict:
    per_file: dict[str, list[str]] = {}
    calls: dict[str, int] = {}
    for rel in _py_files():
        hits = _offending_imports(rel)
        if hits:
            per_file[rel] = hits
        n = _fft_call_sites(rel)
        if n:
            calls[rel] = n
    by_root: dict[str, int] = {}
    for hits in per_file.values():
        for h in hits:
            by_root[h] = by_root.get(h, 0) + 1
    return {
        "files_with_direct_imports": len(per_file),
        "by_module": by_root,
        "fft_call_sites": sum(calls.values()),
        "scanned": len(_py_files()),
        "_per_file": per_file,
        "_calls": calls,
    }


def load_baseline() -> dict:
    if not os.path.exists(BASELINE):
        return {}
    with open(BASELINE, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="name the files")
    ap.add_argument("--ratchet", action="store_true", help="exit 1 on regression")
    ap.add_argument("--update", action="store_true",
                    help="record the current counts as the new high-water mark")
    args = ap.parse_args()

    cur = scan()
    base = load_baseline()

    print(f"\nnumerics (D8)   {cur['scanned']} physics modules scanned")
    was_calls = base.get("fft_call_sites")
    print(f"  direct np.fft transform calls   {cur['fft_call_sites']:>5d}"
          + (f"   (was {was_calls})" if was_calls is not None else "")
          + "   <- C1.3's metric; must be 0")
    print(f"  files importing numpy/scipy/ca_fft   "
          f"{cur['files_with_direct_imports']:>5d}"
          + (f"   (was {base['files_with_direct_imports']})" if base else ""))
    for k in sorted(cur["by_module"], key=lambda x: -cur["by_module"][x]):
        was = (base.get("by_module") or {}).get(k)
        tag = "  (transitional: routes through the seam)" if k in TRANSITIONAL else ""
        print(f"    {k:<8s} {cur['by_module'][k]:>5d}"
              + (f"   (was {was})" if was is not None else "") + tag)

    if args.list:
        if cur["_calls"]:
            print("\n  files STILL calling np.fft directly:")
            for rel, n in sorted(cur["_calls"].items(), key=lambda x: -x[1]):
                print(f"    {n:>4d}  {rel}")
        print("\n  still importing numpy/scipy/ca_fft:")
        for rel, hits in sorted(cur["_per_file"].items()):
            print(f"    {','.join(hits):<16s} {rel}")

    if args.update:
        rec = {k: v for k, v in cur.items() if not k.startswith("_")}
        with open(BASELINE, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print(f"\nrecorded new high-water mark in "
              f"{os.path.relpath(BASELINE, _REPO)}")
        return 0

    if args.ratchet:
        if not base:
            print("\nno baseline yet — run `--update` once to record one")
            return 1
        bad = []
        # The hard one: a direct np.fft transform call must never come back.
        if cur["fft_call_sites"] > base.get("fft_call_sites", 0):
            bad.append(f"direct np.fft transform calls "
                       f"{base.get('fft_call_sites', 0)} -> "
                       f"{cur['fft_call_sites']}")
        if cur["files_with_direct_imports"] > base["files_with_direct_imports"]:
            bad.append(f"files_with_direct_imports "
                       f"{base['files_with_direct_imports']} -> "
                       f"{cur['files_with_direct_imports']}")
        for k, v in cur["by_module"].items():
            if k in TRANSITIONAL:
                continue          # see the TRANSITIONAL note; ratcheted by C9
            was = (base.get("by_module") or {}).get(k, 0)
            if v > was:
                bad.append(f"{k} {was} -> {v}")
        if bad:
            print(f"\nRATCHET FAILED — D8 regressed:")
            for b in bad:
                print(f"  - {b}")
            print("  A new direct numpy/scipy/ca_fft import was added. Route it "
                  "through casim.numerics, or if it is genuinely exempt, add "
                  "the reason to EXEMPT_PREFIXES in this file.")
            return 1
        print("\nratchet OK — D8 has not regressed")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
