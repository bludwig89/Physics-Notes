#!/usr/bin/env python3
"""Build `test-results/manifest.json` — roadmap P1.4.

Replaces the prefix heuristic in `tools/regen_indexes.py` (gen_tests_index),
which matched a result file to a test by `result.startswith(test_stem)`, capped
at two matches, left 104 of 339 index rows with an empty Results cell, and —
because it only ever looked in one direction — could not see an orphaned result
file at all.

What this does instead:

  * reads each result JSON and takes its OWN declaration of where it came from
    where one exists, falling back to filename evidence;
  * resolves the mapping in **both** directions, so orphans (a result with no
    owning test) and silent tests (a test that emits nothing) are both visible;
  * records the git SHA and mtime, so a result can be tied to the tree state
    that produced it;
  * records a content fingerprint of the numeric payload, which is what the
    P1.2 baseline harness compares against.

Usage:
    python3 tools/gen_manifest.py            # write the manifest
    python3 tools/gen_manifest.py --check    # exit 1 if stale
    python3 tools/gen_manifest.py --report   # human summary, no write
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(_REPO, "test-results")
MANIFEST = os.path.join(RESULTS_DIR, "manifest.json")

TEST_DIRS = ("tests/findings", "tests/priority", "tests/casim", "tests/runners")
_SKIP_DIRS = ("__pycache__", ".pytest_cache", "figures", "logs", "suite")

# Finding IDs in this repo take the forms F107, FA03, FB09, FC07, FG7. The
# trailing boundary must NOT be \b: filenames read `F107_canonical_...`, and
# `_` is a word character, so \b never matches there. That single character is
# why the old index resolved almost nothing by finding ID and fell back to
# guessing from filename prefixes.
FINDING_RE = re.compile(r"(?<![A-Za-z0-9])(F[A-Z]{0,2}\d{1,3})(?![0-9])")


# ---------------------------------------------------------------------------
def git_sha() -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             cwd=_REPO, capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or None if out.returncode == 0 else None
    except Exception:
        return None


def _module_doc(path: str) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return ast.get_docstring(ast.parse(fh.read())) or ""
    except (SyntaxError, OSError):
        return ""


def _writes_results(src: str) -> bool:
    return "test-results" in src or "test_results" in src


def collect_tests() -> dict[str, dict]:
    """Every test file, with the findings it claims and whether it emits results."""
    tests: dict[str, dict] = {}
    for d in TEST_DIRS:
        full_dir = os.path.join(_REPO, d)
        if not os.path.isdir(full_dir):
            continue
        for fname in sorted(os.listdir(full_dir)):
            if not fname.endswith(".py") or fname == "conftest.py":
                continue
            rel = f"{d}/{fname}"
            path = os.path.join(_REPO, rel)
            with open(path, encoding="utf-8", errors="replace") as fh:
                src = fh.read()
            doc = _module_doc(path)
            head = doc.splitlines()[0] if doc else ""
            tests[rel] = {
                "suite": d.split("/", 1)[1],
                "findings": sorted(set(FINDING_RE.findall(fname + " " + doc)),
                                   key=lambda s: (s[1].isdigit(), s)),
                "summary": head[:160],
                "has_pytest_funcs": bool(re.search(
                    r"^\s*(?:async )?def test_|^\s*class Test", src, re.M)),
                "has_main": "__main__" in src,
                "has_assert": bool(re.search(r"^\s*assert\b", src, re.M)),
                "declares_results_write": _writes_results(src),
                "results": [],
            }
    return tests


def _numeric_fingerprint(obj) -> str:
    """Stable hash of the numeric content of a result, ignoring key order.

    Deliberately ignores non-numeric fields — timestamps, paths, wall-clock
    durations and host details change every run and are not physics.
    """
    acc: list[str] = []

    def walk(node, path=""):
        if isinstance(node, dict):
            for k in sorted(node):
                walk(node[k], f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")
        elif isinstance(node, bool):
            acc.append(f"{path}={node}")
        elif isinstance(node, (int, float)):
            acc.append(f"{path}={float(node):.12g}")

    walk(obj)
    return hashlib.sha256("\n".join(acc).encode()).hexdigest()[:16]


def collect_results() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not os.path.isdir(RESULTS_DIR):
        return out
    for dirpath, dirnames, filenames in os.walk(RESULTS_DIR):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
        for fname in sorted(filenames):
            if fname == "manifest.json" or not fname.endswith((".json", ".md")):
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, _REPO).replace(os.sep, "/")
            st = os.stat(full)
            rec: dict = {
                "bytes": st.st_size,
                "mtime": datetime.fromtimestamp(
                    st.st_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M"),
                "findings": sorted(set(FINDING_RE.findall(fname)),
                                   key=lambda s: (s[1].isdigit(), s)),
                "tests": [],
            }
            if fname.endswith(".json"):
                try:
                    with open(full, encoding="utf-8") as fh:
                        payload = json.load(fh)
                    rec["fingerprint"] = _numeric_fingerprint(payload)
                    rec["numeric_fields"] = rec["fingerprint"] != _numeric_fingerprint({})
                    if isinstance(payload, dict):
                        for key in ("source", "test", "script", "generated_by"):
                            if isinstance(payload.get(key), str):
                                rec["self_declared_source"] = payload[key]
                                break
                        # 117 of the 390 result JSONs carry a `finding` key.
                        # That is the artifact naming its own physics, which
                        # beats anything inferred from a filename.
                        for key in ("finding", "findings"):
                            v = payload.get(key)
                            if isinstance(v, str):
                                rec["declared_findings"] = sorted(
                                    set(FINDING_RE.findall(v)))
                            elif isinstance(v, list):
                                rec["declared_findings"] = sorted(
                                    {f for item in v if isinstance(item, str)
                                     for f in FINDING_RE.findall(item)})
                            if rec.get("declared_findings"):
                                break
                except (json.JSONDecodeError, OSError) as e:
                    rec["unreadable"] = str(e)[:120]
            out[rel] = rec
    return out


def link(tests: dict, results: dict) -> tuple[list[str], list[str]]:
    """Resolve result <-> test in both directions, strongest evidence wins.

    Evidence is ranked and the search STOPS at the first tier that produces a
    match. Ranking matters more than it looks: a naive finding-ID join produced
    825 links because every test that merely mentions F107 in its docstring
    matched every F107 result. A mapping that says a result belongs to nine
    tests is not a mapping. So finding-ID is only accepted when it identifies
    exactly one test; otherwise the result is recorded as AMBIGUOUS, which is
    an honest state and a to-do, rather than nine wrong edges.

    Returns (ambiguous, orphans).
    """
    by_stem = {re.sub(r"^test_", "", os.path.basename(t)[:-3]): t for t in tests}
    ambiguous: list[str] = []

    for rpath, rrec in results.items():
        stem = os.path.basename(rpath).rsplit(".", 1)[0]
        matched: list[tuple[str, str]] = []

        # 1. The result names its own producing script.
        decl = rrec.get("self_declared_source")
        if decl:
            for t in tests:
                if t == decl or os.path.basename(t) == os.path.basename(decl):
                    matched.append((t, "declared-source"))

        # 2. Exact stem identity: F107_x.json <-> test_F107_x.py.
        if not matched and stem in by_stem:
            matched.append((by_stem[stem], "exact-stem"))

        # 3. The result is a secondary artifact of one test: test_F107_x.py
        #    emitting F107_x_extra.json.
        if not matched:
            cands = [(t, "stem-prefix") for s, t in by_stem.items()
                     if len(s) > 4 and stem.startswith(s + "_")]
            if len(cands) == 1:
                matched = cands
            elif cands:                      # prefer the longest stem match
                best = max(cands, key=lambda c: len(
                    re.sub(r"^test_", "", os.path.basename(c[0])[:-3])))
                matched = [best]

        # 4. The result declares its finding and exactly one test owns it.
        if not matched and rrec.get("declared_findings"):
            cands = [(t, "declared-finding") for t, tr in tests.items()
                     if set(rrec["declared_findings"]) & set(tr["findings"])]
            if len(cands) == 1:
                matched = cands
            elif cands:
                ambiguous.append(rpath)

        # 5. Weakest: finding ID inferred from the filename. Unique only.
        if not matched and rrec["findings"] and rpath not in ambiguous:
            cands = [(t, "finding-id") for t, tr in tests.items()
                     if set(rrec["findings"]) & set(tr["findings"])]
            if len(cands) == 1:
                matched = cands
            elif cands:
                ambiguous.append(rpath)

        for t, how in matched:
            rrec["tests"].append({"path": t, "evidence": how})
            tests[t]["results"].append({"path": rpath, "evidence": how})

    orphans = sorted(p for p, r in results.items()
                     if not r["tests"] and p not in ambiguous)
    return sorted(set(ambiguous)), orphans


def build() -> dict:
    tests = collect_tests()
    results = collect_results()
    ambiguous, orphans = link(tests, results)

    silent = sorted(p for p, t in tests.items()
                    if not t["results"] and t["declares_results_write"])
    quiet = sorted(p for p, t in tests.items()
                   if not t["results"] and not t["declares_results_write"])
    # The number that matters: a test with no assertion AND no result artifact
    # to diff has no failure mode by any mechanism.
    unfalsifiable = sorted(
        p for p, t in tests.items()
        if not t["has_assert"] and not t["results"])

    return {
        "version": 1,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "git_sha": git_sha(),
        "summary": {
            "tests": len(tests),
            "results": len(results),
            "tests_with_results": sum(1 for t in tests.values() if t["results"]),
            "tests_with_assert": sum(1 for t in tests.values() if t["has_assert"]),
            "orphan_results": len(orphans),
            "ambiguous_results": len(ambiguous),
            "silent_tests": len(silent),
            "no_output_tests": len(quiet),
            "unfalsifiable_tests": len(unfalsifiable),
        },
        "orphan_results": orphans,
        "ambiguous_results": ambiguous,
        "silent_tests": silent,
        "unfalsifiable_tests": unfalsifiable,
        "tests": tests,
        "results": results,
    }


def report(m: dict) -> None:
    s = m["summary"]
    print(f"\ntest-results manifest  (git {m['git_sha']})")
    print(f"  tests                {s['tests']}")
    print(f"  result artifacts     {s['results']}")
    print(f"  tests -> results     {s['tests_with_results']}")
    print(f"  tests with assert    {s['tests_with_assert']}")
    print(f"  orphan results       {s['orphan_results']}  "
          f"(no owning test — invisible to the old index)")
    print(f"  ambiguous results    {s['ambiguous_results']}  "
          f"(finding ID matches >1 test; left unlinked rather than guessed)")
    print(f"  silent tests         {s['silent_tests']}  "
          f"(write results in code, none found on disk)")
    print(f"  no output at all     {s['no_output_tests']}")
    print(f"  UNFALSIFIABLE        {s['unfalsifiable_tests']}  "
          f"(no assert AND no result to diff — cannot fail by any means)")
    ev: dict[str, int] = {}
    for r in m["results"].values():
        for t in r["tests"]:
            ev[t["evidence"]] = ev.get(t["evidence"], 0) + 1
    print("  link evidence:       " +
          ", ".join(f"{v} {k}" for k, v in sorted(ev.items())))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the manifest on disk is missing or stale")
    ap.add_argument("--report", action="store_true", help="summarise, do not write")
    args = ap.parse_args()

    m = build()

    if args.report:
        report(m)
        return 0

    if args.check:
        if not os.path.exists(MANIFEST):
            print("manifest.json is missing — run `python3 tools/gen_manifest.py`")
            return 1
        with open(MANIFEST, encoding="utf-8") as fh:
            old = json.load(fh)
        # Compare structure, not the generated timestamp.
        a = {k: v for k, v in old.items() if k not in ("generated", "git_sha")}
        b = {k: v for k, v in m.items() if k not in ("generated", "git_sha")}
        if a != b:
            print("manifest.json is stale — run `python3 tools/gen_manifest.py`")
            return 1
        print("manifest.json is current")
        return 0

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, sort_keys=True)
        fh.write("\n")
    report(m)
    print(f"\nwrote {os.path.relpath(MANIFEST, _REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
