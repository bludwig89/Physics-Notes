#!/usr/bin/env python3
"""Test-suite health audit and ratchet — roadmap P1.1 / P1.2 / P1.3.

Three numbers this project could not previously see:

  1. **Unfalsifiable tests** — no `assert`, and no result artifact to diff, so
     no failure mode by any mechanism. The suite runner scores these `RAN`,
     which reads like a pass.
  2. **Import-time physics** — every finding test does real work at module
     level, so `pytest --collect-only` executes the suite. This is why `-k`
     filtering and parallel runs are unusable, and why collection is not free.
  3. **Tier assignment** — which of gate / battery / archive each file is in.

`--ratchet` is the point of the file. Fixing 272 tests is a long job; making
sure the numbers only ever move in the right direction is a short one. The
gate runs `--ratchet`, which fails if any count regresses past the recorded
high-water mark in `tools/test_health_baseline.json`.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(_REPO, "tools", "test_health_baseline.json")
MANIFEST = os.path.join(_REPO, "test-results", "manifest.json")

TIERS = {
    "tests/casim": "gate",
    "tests/findings": "battery",
    "tests/priority": "battery",
    "tests/runners": "battery",
}


def _has_import_time_work(tree: ast.Module) -> bool:
    """True if the module does anything beyond definitions at top level.

    NOTE (roadmap C1.4, 2026-07-30): this metric has a blunt edge worth knowing
    about. Every test file in this repo needs a module-level `sys.path` preamble
    before it can import a kernel, so ADDING ANY NEW TEST raises the count by
    one even when the file is a model citizen — asserting, falsifiable, no
    physics at import. That happened when `test_chiral_core_caching.py` landed
    (320 -> 321), and the baseline was moved deliberately rather than the file
    being contorted to dodge a proxy.
    The two counts that carry the real signal, `unfalsifiable` and `no_assert`,
    did not move. If `import_time_work` ever rises WITH them, that is the case
    this ratchet is actually for.


    Imports, defs, classes, docstrings, constant assignments and the
    `if __name__ == "__main__"` guard are all free. Loops, calls, `with`, and
    bare expressions at module scope are not — those execute on import.
    """
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef, ast.Pass)):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue                                   # docstring
        if isinstance(node, ast.If):
            test = node.test
            # the __main__ guard is not import-time work
            if (isinstance(test, ast.Compare)
                    and isinstance(test.left, ast.Name)
                    and test.left.id == "__name__"):
                continue
            return True
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            value = node.value
            if value is None:
                continue
            # A literal or simple arithmetic constant is fine; a CALL is work.
            if any(isinstance(n, (ast.Call, ast.ListComp, ast.DictComp,
                                  ast.SetComp, ast.GeneratorExp))
                   for n in ast.walk(value)):
                return True
            continue
        if isinstance(node, (ast.Try, ast.For, ast.While, ast.With,
                             ast.AsyncFor, ast.AsyncWith, ast.Expr)):
            return True
    return False


def _registry_counts() -> dict:
    """Test-registry counts (roadmap C7). Empty dict if the registry is absent.

    This is the fourth ratchet counter the C7 phase adds. `legacy_script` is
    declared debt: a record that wraps an unmigrated file and inherits whatever
    failure mode that file had, which is often none. Coverage is 100% from day
    one *by construction*, so the honest progress metric is not "how many tests
    are registered" but "how many are still only registered".
    """
    src = os.path.join(_REPO, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    try:
        from casim.tests import registry as treg
        return treg.counts()
    except Exception:                                    # pragma: no cover
        return {}


def audit() -> dict:
    with open(MANIFEST, encoding="utf-8") as fh:
        manifest = json.load(fh)

    rows = []
    for rel, trec in sorted(manifest["tests"].items()):
        path = os.path.join(_REPO, rel)
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                tree = ast.parse(fh.read(), filename=rel)
            import_work = _has_import_time_work(tree)
        except (SyntaxError, OSError):
            import_work = False

        suite_dir = rel.rsplit("/", 1)[0]
        rows.append({
            "path": rel,
            "tier": TIERS.get(suite_dir, "battery"),
            "has_assert": trec["has_assert"],
            "has_results": bool(trec["results"]),
            "pytest_style": trec["has_pytest_funcs"],
            "import_time_work": import_work,
            "falsifiable": trec["has_assert"] or bool(trec["results"]),
        })

    def n(pred) -> int:
        return sum(1 for r in rows if pred(r))

    reg = _registry_counts()
    totals = {
        "tests": len(rows),
        "gate": n(lambda r: r["tier"] == "gate"),
        "battery": n(lambda r: r["tier"] == "battery"),
        "unfalsifiable": n(lambda r: not r["falsifiable"]),
        "import_time_work": n(lambda r: r["import_time_work"]),
        "no_assert": n(lambda r: not r["has_assert"]),
        "pytest_style": n(lambda r: r["pytest_style"]),
    }
    if reg:
        # C7: the registry's own numbers. `legacy_script` is the ratcheted one.
        totals["legacy_script"] = reg["legacy_script"]
        totals["registry_records"] = reg["records"]
        totals["registry_unregistered"] = reg["unregistered"]
        totals["registry_result_dump"] = reg["result_dump"]
        totals["registry_assertion"] = reg["assertion"]

    return {
        "totals": totals,
        "unfalsifiable": sorted(r["path"] for r in rows if not r["falsifiable"]),
        "import_time_work": sorted(r["path"] for r in rows
                                   if r["import_time_work"]),
        "rows": rows,
    }


# Only these may never get worse. Lower is better for all four.
#
# `legacy_script` (roadmap C7) is the newest and the one with a defined end
# state: zero. Every test file has a registry record from day one, so the debt
# is not "unregistered tests" but "records that only wrap a script". The other
# three are P1's, and `unfalsifiable` keeps its manifest-derived definition on
# purpose — relabelling it against the registry would make the number improve
# without any test improving.
_RATCHET_KEYS = ("unfalsifiable", "import_time_work", "no_assert",
                 "legacy_script")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratchet", action="store_true",
                    help="fail if any tracked count regressed")
    ap.add_argument("--update-baseline", action="store_true",
                    help="record current counts as the new high-water mark")
    ap.add_argument("--list", choices=["unfalsifiable", "import_time_work"],
                    help="print the offending files")
    args = ap.parse_args()

    if not os.path.exists(MANIFEST):
        print("test-results/manifest.json missing — run tools/gen_manifest.py",
              file=sys.stderr)
        return 2

    a = audit()
    t = a["totals"]

    if args.list:
        for p in a[args.list]:
            print(p)
        return 0

    print(f"\ntest-suite health   ({t['tests']} files)")
    print(f"  gate tier            {t['gate']}")
    print(f"  battery tier         {t['battery']}")
    print(f"  pytest-style         {t['pytest_style']}")
    print(f"  no assert            {t['no_assert']}")
    print(f"  UNFALSIFIABLE        {t['unfalsifiable']}  "
          f"(no assert AND no result artifact — cannot fail)")
    print(f"  import-time physics  {t['import_time_work']}  "
          f"(executes on `pytest --collect-only`)")
    if "legacy_script" in t:
        print(f"\ntest registry (C7 / D9)   "
              f"{t['registry_records']} record(s), "
              f"{t['registry_unregistered']} file(s) unregistered")
        print(f"  assertion            {t['registry_assertion']}")
        print(f"  result_dump          {t['registry_result_dump']}  "
              f"(failure mode = baseline diff vs HEAD)")
        print(f"  LEGACY_SCRIPT        {t['legacy_script']}  "
              f"(declared debt — ratcheted to zero)")

    if args.update_baseline:
        with open(BASELINE, "w", encoding="utf-8") as fh:
            json.dump({k: t[k] for k in _RATCHET_KEYS}, fh, indent=1,
                      sort_keys=True)
            fh.write("\n")
        print(f"\nrecorded high-water mark in "
              f"{os.path.relpath(BASELINE, _REPO)}")
        return 0

    if args.ratchet:
        if not os.path.exists(BASELINE):
            print("\nno baseline recorded; run --update-baseline once.",
                  file=sys.stderr)
            return 2
        with open(BASELINE, encoding="utf-8") as fh:
            base = json.load(fh)
        regressions = [(k, base[k], t[k]) for k in _RATCHET_KEYS
                       if t[k] > base.get(k, 10 ** 9)]
        improvements = [(k, base[k], t[k]) for k in _RATCHET_KEYS
                        if t[k] < base.get(k, 0)]
        for k, was, now in improvements:
            print(f"  improved: {k} {was} -> {now}  "
                  f"(run --update-baseline to lock it in)")
        if regressions:
            print("\nRATCHET FAILED — these may not get worse:")
            for k, was, now in regressions:
                print(f"  {k}: {was} -> {now}  (+{now - was})")
            print("\nAdd an assert, emit a result artifact, or move the work "
                  "out of module scope.")
            return 1
        print("\n  ratchet OK — nothing regressed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
