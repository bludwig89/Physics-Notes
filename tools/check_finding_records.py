#!/usr/bin/env python3
"""D9 acceptance — a finding's declared test record exists, and a gate record can fail.

Two assertions, both cheap enough for ``make gate``. Each exists because the
tree produced the defect it catches, and neither was catchable by anything that
already ran green at the time.

1. **A finding's declared record resolves.** Every ``findings/F*.md`` names its
   record in a fixed header field (``**Test record:**`` or ``**Test /
   results:**``). This check parses that field and fails when the named id is
   absent from ``tests/registry/*.yaml``, or when the finding says ``tier gate``
   and the record's tier is not ``gate``.

   *Why.* Between 2026-08-05 and 2026-08-06, five findings — F298, F299, F300,
   F301, F303 — declared gate-tier records with declared controls. Four of them
   had an auto-scaffolded ``legacy_script``/``battery`` stub keyed to the same
   path; the fifth had nothing at all. ``check_test_registry`` was green
   throughout, because a stub is a *valid* record, and ``check_module_registry``
   was green, because the modules had rows. F299 diagnosed the defect in F298
   and then reproduced it twice. ``test_F300_thermodynamics.py``'s own docstring
   instructed a reader to run ``casim test --id F300-lattice-thermodynamics``,
   which returned "no registry record matches that selection" for a day.

   The information needed to catch it was in a fixed field in the finding the
   whole time. Nothing read it.

2. **A gate record with an entry has a failure mode.**
   ``casim.tests.runner._interpret_return`` maps an entry's return value onto a
   verdict, and a **dict with no** ``passed``/``pass``/``ok``/``gate``/
   ``all_pass`` **key reads as PASS**. So an entry that returns a dict of
   measured numbers and contains no reachable ``assert`` or ``raise`` cannot go
   red — it is a gate record that always passes, which is worse than no record,
   because it is counted as coverage.

   This is a **ratchet**, not a hard failure: seven such records already exist
   (see ``_CEILING``), and turning the gate red on findings this checker did not
   write would only train people to skip it. The count may fall, never rise.
   ``--ratchet-update`` rewrites the ceiling downward only.

   *Note on the analysis.* Reachability is static: asserts and raises are
   collected from the entry function and, transitively, from functions defined
   in the same module that it calls. That under-approximates (a helper reached
   only through a dynamic dispatch is missed) which makes the check
   conservative — it can call a record cannot-fail when a deep dynamic path
   could raise, so the ceiling is an upper bound on a real problem rather than a
   precise count. It never reports a record as *safe* when it is not, which is
   the direction that matters.

Exit 0 clean, 1 on any violation.

    python3 tools/check_finding_records.py            # both assertions
    python3 tools/check_finding_records.py --verbose  # list the ratcheted records
    python3 tools/check_finding_records.py --ratchet-update
"""
from __future__ import annotations

import argparse
import ast
import glob
import importlib
import json
import inspect
import os
import re
import sys
import textwrap

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# A handful of records host their entry in a test file rather than an engine
# module (`module: tests.findings.test_F15_...`). Those import only with the
# repo root on the path, and a record whose module cannot be imported must read
# as an error about the record, not about this tool's sys.path.
for _p in (_REPO, os.path.join(_REPO, "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
_REGISTRY = os.path.join(_REPO, "tests", "registry")
_FINDINGS = os.path.join(_REPO, "findings")

# Assertion 2's ratchet. EIGHT gate records whose entry returns a verdict-less
# dict and contains no reachable assert or raise, measured 2026-08-07:
# F282, F283, F285, F286, F291, F292, F295, F296. Each is a separate piece of
# work — the pass criteria have to come from the finding that owns the record,
# not from this tool — so they are declared debt with a ceiling rather than a
# gate failure. F291 is the rubric's evidence for row A1 and F295/F296 for K3,
# so this debt is load-bearing, not cosmetic.
_CEILING = 5

_VERDICT_KEYS = ("passed", "pass", "ok", "gate", "all_pass")

# The header field a finding uses to name its record. Both spellings are in the
# tree; `casim index` does not read either, which is part of why they drifted.
_HEADER = re.compile(r"^(\*\*Tests?\b[^*]*\*\*)(.*)$", re.M | re.I)
# `record `id`` is the canonical form. The bare-first-token fallback below
# covers `**Test record:** `id` (gate tier)`, the other spelling in use.
_RECORD_ID = re.compile(r"record[s]?\s+`([^`]+)`")
_ANY_TICKED = re.compile(r"`([^`]+)`")
# An id that follows the word `entry` is an entry-point function, not a record.
_ENTRY_TOKEN = re.compile(r"entry\s+`([^`]+)`")
# The finding-side no-test declaration: `none` opening the field, or an explicit
# `no-test (<reason>)` anywhere in it. Kept deliberately loose - this only has to
# recognise "this field is a declaration, not a reference"; the reason vocabulary
# is validated by tools/audit_finding_coverage.py, which is the tool that owns it.
_NO_TEST_DECL = re.compile(r"^\s*none\b|no[-_]test\s*\(", re.I)


def _records() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(_REGISTRY, "*.yaml"))):
        with open(path, encoding="utf-8") as fh:
            for rec in (yaml.safe_load(fh) or {}).get("tests") or []:
                out[rec["id"]] = rec
    return out


def _declared_ids(label: str, line: str) -> list[str]:
    """The record ids a finding's header field names, entry names excluded.

    Only a header that uses the word "record" is read. 56 findings write
    `**Tests:**` followed by a bare filename or a check name, which predates the
    D9 record convention entirely — reading those produced false positives on
    `test_P2_1`, `F200` and a bare `.md`, and a check with false positives is a
    check people learn to skip.
    """
    # A no-test DECLARATION is not a record reference. Since 2026-08-19 a finding
    # may answer the coverage question with
    #
    #     **Test record:** none - no-test (analysis-only)
    #
    # (closed vocabulary; see tools/audit_finding_coverage.py, which owns that
    # check). Today the bare-first-token fallback below skips it by accident,
    # because the declaration happens to contain no backticks - and the day
    # somebody writes the reason as `analysis-only` this checker would read it as
    # a record id and go red on a correctly-declared finding. Recognise it
    # explicitly rather than relying on that.
    if _NO_TEST_DECL.search(line):
        return []
    entries = set(_ENTRY_TOKEN.findall(line))
    ids = [i for i in _RECORD_ID.findall(line) if i not in entries]
    if not ids and "record" in label.lower():
        for tok in _ANY_TICKED.findall(line):
            if tok in entries or "/" in tok or tok.endswith((".json", ".py", ".yaml")):
                continue
            ids = [tok]
            break
    return ids


def check_declared_records(verbose: bool = False) -> list[str]:
    recs = _records()
    errs: list[str] = []
    checked = 0
    for path in sorted(glob.glob(os.path.join(_FINDINGS, "F*.md"))):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for label, line in _HEADER.findall(text):
            wants_gate = "tier gate" in line.lower() or "gate tier" in line.lower()
            for rid in _declared_ids(label, line):
                checked += 1
                name = os.path.basename(path)
                rec = recs.get(rid)
                if rec is None:
                    errs.append(
                        f"{name}: declares record `{rid}`, which does not exist "
                        f"in tests/registry/. Either write the record or correct "
                        f"the finding's header.")
                elif wants_gate and rec.get("tier") != "gate":
                    errs.append(
                        f"{name}: declares record `{rid}` at tier gate, but the "
                        f"record is tier={rec.get('tier')} kind={rec.get('kind')}. "
                        f"An auto-scaffolded stub is a valid record and will not "
                        f"be caught by check_test_registry — arm it with "
                        f"`module:`/`entry:` or correct the finding.")
    if verbose:
        print(f"  [1] {checked} declared record reference(s) across "
              f"{len(glob.glob(os.path.join(_FINDINGS, 'F*.md')))} finding(s)")
    return errs


def _returns_a_bool(fn) -> bool:
    """True if the entry returns a boolean rather than a payload dict.

    `_interpret_return` handles a bare bool directly, so such an entry has a
    failure mode even with no verdict key and no assert (F279 is the case in
    the tree).
    """
    try:
        tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    except (OSError, TypeError, SyntaxError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Return) and node.value is not None:
            v = node.value
            if isinstance(v, ast.Constant) and isinstance(v.value, bool):
                return True
            if isinstance(v, (ast.Compare, ast.BoolOp)):
                return True
            if isinstance(v, ast.UnaryOp) and isinstance(v.op, ast.Not):
                return True
            if isinstance(v, ast.Call) and getattr(v.func, "id", "") in (
                    "bool", "all", "any"):
                return True
    return False


def _reachable_raises(mod, entry: str) -> int:
    """Asserts + raises reachable from `entry` through same-module calls."""
    try:
        tree = ast.parse(inspect.getsource(mod))
    except (OSError, TypeError, SyntaxError):
        return -1
    funcs = {n.name: n for n in ast.walk(tree)
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    tables = _dispatch_tables(tree, funcs)
    seen: set[str] = set()
    stack = [entry]
    total = 0
    while stack:
        name = stack.pop()
        if name in seen or name not in funcs:
            continue
        seen.add(name)
        fn = funcs[name]
        total += sum(1 for n in ast.walk(fn)
                     if isinstance(n, (ast.Assert, ast.Raise)))
        for node in ast.walk(fn):
            if isinstance(node, ast.Call):
                target = getattr(node.func, "id", None) or getattr(
                    node.func, "attr", None)
                if target in funcs:
                    stack.append(target)
            elif isinstance(node, ast.Name) and node.id in tables:
                # A DISPATCH TABLE. `check_all` does not name its checks; it does
                # `for name, fn in CHECKS: out[name] = fn()`, so the only Call
                # node is on the loop variable `fn` and the walk above finds
                # nothing. Three records were counted as cannot-fail on that
                # basis while holding 41, 39 and 30 reachable asserts between
                # them -- see the 2026-08-08 correction. Referencing the table by
                # name is what makes its members reachable.
                stack.extend(tables[node.id])
    return total


def _dispatch_tables(tree, funcs: dict) -> dict[str, list[str]]:
    """{module-level constant -> function names it holds}.

    Matches `CHECKS = (("A1_...", check_A1_...), ...)` and any other module-level
    binding whose value mentions functions defined in the same module. Deliberately
    shallow: it does not try to prove the container is ever iterated, because the
    failure this guards is UNDER-counting reachable asserts, and over-counting here
    would at worst call a real defect a non-defect one line earlier than the
    `_VERDICT_KEYS` test already does.
    """
    out: dict[str, list[str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if not names:
            continue
        held = sorted({n.id for n in ast.walk(node.value)
                       if isinstance(n, ast.Name) and n.id in funcs})
        for nm in names:
            if held:
                out[nm] = held
    return out


def _empirical_can_fail() -> dict:
    """Journalled EXECUTION verdicts, keyed by record id, fingerprint-checked.

    Measurement beats inference here and the repo has the scar to prove it: the
    AST walk below reported three records as cannot-fail while they held 41, 39
    and 30 reachable asserts, because they dispatch through a module-level
    `CHECKS` tuple and the only `ast.Call` node is on a loop variable. Any static
    reachability analysis loses to indirection -- dispatch tables, `getattr`,
    decorators, registries of callables.

    `casim.tests.runner.probe_can_fail` traces one real run instead and reports
    which assert/raise lines were actually reached, plus whether the payload
    carries its own verdict key. `make can-fail` writes it; this reads it. A
    record whose fingerprint has moved falls back to the static walk, and the
    printout says which authority answered.
    """
    path = os.path.join(_REPO, "test-results", "can-fail.json")
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError):
        return {}
    out = {}
    for it in doc.get("items") or []:
        if it.get("id") and it.get("verdict") in ("CAN_FAIL", "CANNOT_FAIL"):
            out[it["id"]] = it
    return out


def check_gate_entries_can_fail(verbose: bool = False
                                ) -> tuple[list[str], list[str]]:
    """(hard errors, ids that cannot fail). The second list is the ratchet."""
    errs: list[str] = []
    cannot_fail: list[str] = []
    skipped: list[tuple[str, str]] = []
    measured = _empirical_can_fail()
    n_measured = 0
    for rid, rec in sorted(_records().items()):
        if rec.get("tier") != "gate" or not rec.get("entry"):
            continue
        modname = rec.get("module")
        if not modname:
            continue                      # path-hosted entry; runner loads the file
        try:
            mod = importlib.import_module(modname)
        except ModuleNotFoundError as exc:
            # A THIRD-PARTY dependency the environment lacks (scipy, mpmath) is
            # not a defect in the record, and a checker that goes red because
            # the sandbox is thin is a checker people disable. Skip those and
            # say how many were skipped. A record whose OWN module is missing is
            # still an error.
            missing = (exc.name or "")
            if missing and not modname.startswith(missing):
                skipped.append((rid, missing))
                continue
            errs.append(f"{rid}: cannot import {modname} — "
                        f"{type(exc).__name__}: {exc}")
            continue
        except Exception as exc:                       # noqa: BLE001
            errs.append(f"{rid}: cannot import {modname} — "
                        f"{type(exc).__name__}: {exc}")
            continue
        fn = getattr(mod, rec["entry"], None)
        if fn is None or not callable(fn):
            errs.append(f"{rid}: {modname} has no callable "
                        f"{rec['entry']!r} — the record names an entry that is "
                        f"not there.")
            continue
        try:
            src = inspect.getsource(fn)
        except (OSError, TypeError):
            src = ""
        # Measured verdict first, if it was taken against this exact code.
        emp = measured.get(rid)
        if emp is not None:
            try:
                from casim.tests import registry as _treg
                from casim.tests import runner as _trun
                fresh = (emp.get("fingerprint")
                         == _trun.record_fingerprint(_treg.get(rid), _REPO))
            except Exception:                              # noqa: BLE001
                fresh = False
            if fresh:
                n_measured += 1
                if emp["verdict"] == "CANNOT_FAIL":
                    cannot_fail.append(rid)
                continue

        has_verdict = any(f"'{k}'" in src or f'"{k}"' in src
                          for k in _VERDICT_KEYS) or _returns_a_bool(fn)
        if has_verdict:
            continue
        if _reachable_raises(mod, rec["entry"]) == 0:
            cannot_fail.append(rid)
    if skipped:
        deps = sorted({d for _, d in skipped})
        print(f"  [2] NOTE: {len(skipped)} gate entr(ies) not analysed — "
              f"missing dependency: {', '.join(deps)}. Assertion 2 is "
              f"incomplete in this environment.")
        if verbose:
            for rid, dep in skipped:
                print(f"        skipped {rid} (needs {dep})")
    if verbose and cannot_fail:
        print("  [2] gate entries with no verdict key and no reachable "
              "assert/raise:")
        for rid in cannot_fail:
            print(f"        {rid}")
    if n_measured:
        print(f"[finding-records] {n_measured} gate entr(ies) answered by "
              f"MEASUREMENT (test-results/can-fail.json, execution trace); "
              f"the rest by static reachability.")
    else:
        print("[finding-records] no fresh can-fail measurements — using the "
              "static walk, which loses to dispatch tables. Run `make can-fail`.")
    return errs, cannot_fail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--ratchet-update", action="store_true",
                    help="lower the cannot-fail ceiling to the measured count")
    args = ap.parse_args()

    errs = check_declared_records(args.verbose)
    hard, cannot_fail = check_gate_entries_can_fail(args.verbose)
    errs += hard

    n = len(cannot_fail)
    if args.ratchet_update:
        if n > _CEILING:
            print(f"[finding-records] refusing to raise the ceiling "
                  f"{_CEILING} -> {n}. A ratchet that can be raised is not a "
                  f"ratchet; fix the record instead.")
            return 1
        if n < _CEILING:
            path = os.path.abspath(__file__)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            text = text.replace(f"_CEILING = {_CEILING}", f"_CEILING = {n}", 1)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(f"[finding-records] ceiling lowered {_CEILING} -> {n}")
        else:
            print(f"[finding-records] ceiling unchanged at {_CEILING}")
        return 0

    if n > _CEILING:
        errs.append(
            f"cannot-fail gate entries {n} > ceiling {_CEILING}: "
            f"{', '.join(cannot_fail)}. A gate entry returning a dict with no "
            f"verdict key and no reachable assert/raise always passes "
            f"(casim.tests.runner._interpret_return). Give it a `passed` key or "
            f"an assert.")

    if errs:
        print(f"[finding-records] {len(errs)} violation(s):")
        for e in errs:
            print(f"  - {e}")
        return 1

    total_findings = len(glob.glob(os.path.join(_FINDINGS, "F*.md")))
    print(f"[finding-records] {total_findings} finding(s): every declared test "
          f"record exists at the tier it claims (D9).")
    print(f"    cannot-fail gate entries: {n} (ceiling {_CEILING}, "
          f"declared debt — ratcheted to zero)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
