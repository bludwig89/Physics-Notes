#!/usr/bin/env python3
"""Generate / refresh `tests/registry/*.yaml` — roadmap C7.1 (decision **D9**).

Every test file gets a record on the first run, so registry coverage is 100%
immediately and the remaining work is a countable `legacy_script` number rather
than a 345-file big bang.

Field ownership, same convention as the migration manifest:

  * **`evidence:` is generated.** Rewritten from the tree on every run.
  * **Everything else is human-owned** and preserved verbatim across
    regeneration, keyed by `path:`. Promoting a record from `legacy_script` to
    `assertion`/`result_dump` — adding `module:`, `entry:`, `params:`,
    `expect:` — is exactly the C7.4/C7.5 work, and re-running this tool must
    never undo it.

Kind assignment (first match wins), for records the tool creates fresh:

  1. the ledger marks the file `fully_superseded`     -> tier `archive`
  2. it has pytest functions **and** an `assert`      -> `assertion` (delegate)
  3. it writes a git-tracked result artifact          -> `result_dump`
  4. otherwise                                       -> `legacy_script`

Rule 3 is where most of C7's value comes from. P1 counted 70 tests with no
failure mode, but 57 of them *do* write numbers to `test-results/`; the results
manifest simply could not see it, because its strongest signal was filename
stem identity (`F107_x.json` <-> `test_F107_x.py`) and these files write under
unrelated names (`test_09_GR4_mercury.py` -> `top10_T09_GR4_mercury.json`).
Reading the artifact path out of the source, next to the call that writes it,
turns an inference into a declaration — and a declared, committed artifact is a
baseline diff, which is a real failure mode.

Usage:
    python3 tools/gen_test_registry.py            # write/refresh the registry
    python3 tools/gen_test_registry.py --check    # exit 1 if stale
    python3 tools/gen_test_registry.py --report   # summary, no write
"""
from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from typing import Any

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "src"))

REGISTRY_DIR = os.path.join(_REPO, "tests", "registry")
MANIFEST = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")
GRAPH = os.path.join(_REPO, "docs", "design", "module-graph.json")
LEDGER = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")

TEST_DIRS = ("tests/casim", "tests/findings", "tests/priority", "tests/runners")
_NOT_A_TEST = {"__init__.py", "conftest.py"}

# Same boundary fix as tools/gen_manifest.py: `\b` never matches before `_`,
# and every filename in this repo reads `F107_something`.
FINDING_RE = re.compile(r"(?<![A-Za-z0-9])(F[A-Z]{0,2}\d{1,3})(?![0-9])")

# An artifact literal: a .json/.md name, possibly with directories. f-string
# templates (`pt_{L}.json`) are per-run outputs, not baselines, so they are out.
_ARTIFACT_RE = re.compile(r"""['"]([A-Za-z0-9_./\-]+\.(?:json|md))['"]""")
_WRITE_CTX = re.compile(
    r"json\.dump|write_results|\.savez|\.savetxt|\.to_json|"
    r"open\([^)]*['\"](?:w|w\+|wb)['\"]|\.write\(")
_WRITE_WINDOW = 8            # lines either side of the literal

# Sector precedence when a test imports modules from several sectors: the more
# specific physics sector wins over the base layer it is built on. A gauge test
# imports the lattice; that does not make it a lattice test.
_SECTOR_PRIORITY = ("gauge", "particles", "interactions", "forks",
                    "lattice", "numerics", "core")


# ---------------------------------------------------------------------------
def _yaml(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _tracked_files() -> set[str]:
    """Everything git knows about. A baseline must be committed to be a baseline."""
    try:
        out = subprocess.run(["git", "ls-files"], cwd=_REPO,
                             capture_output=True, text=True, timeout=60)
        if out.returncode != 0:
            return set()
        return {ln.strip() for ln in out.stdout.splitlines() if ln.strip()}
    except Exception:
        return set()


def _sector_maps() -> dict[str, str]:
    """{repo-relative module path -> sector} for both migration endpoints."""
    m = _yaml(MANIFEST)
    out: dict[str, str] = {}
    for rec in m.get("modules") or []:
        sec = rec.get("sector")
        if not sec:
            continue
        for key in ("source", "target"):
            if rec.get(key):
                out[rec[key].replace(os.sep, "/")] = sec
    return out


def _graph_imports() -> dict[str, list[str]]:
    import json
    if not os.path.exists(GRAPH):
        return {}
    with open(GRAPH, encoding="utf-8") as fh:
        g = json.load(fh)
    out: dict[str, list[str]] = {}
    for key, node in (g.get("nodes") or {}).items():
        imports = list(node.get("imports") or [])
        imports += list(node.get("dynamic_refs") or [])
        out[key] = imports
    return out


def _ledger_test_status() -> dict[str, tuple[str, str]]:
    """{test path -> (status, superseding record id)} from the ledger."""
    led = _yaml(LEDGER)
    out: dict[str, tuple[str, str]] = {}
    for rec in led.get("supersessions") or []:
        for entry in rec.get("tests") or []:
            p = (entry.get("path") or "").replace(os.sep, "/")
            if p:
                out[p] = (entry.get("status", "live"), rec.get("id", ""))
    return out


# ---------------------------------------------------------------------------
def _scan_file(rel: str, tracked: set[str]) -> dict[str, Any]:
    """Evidence for one test file: what it defines, asserts, and writes."""
    full = os.path.join(_REPO, rel)
    with open(full, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    lines = src.splitlines()
    doc = ""
    defines: list[str] = []
    try:
        tree = ast.parse(src, filename=rel)
        doc = ast.get_docstring(tree) or ""
        defines = [n.name for n in tree.body
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef,
                                     ast.ClassDef))]
    except SyntaxError:
        pass

    # --- result artifacts -------------------------------------------------
    # Two acceptance rules, recorded separately so the evidence is auditable:
    #
    #   local — a write call sits within a few lines of the literal. Confident.
    #   file  — the literal is a module constant (the common style here:
    #           `RESULTS = os.path.join(..., "F106_psi_K_sourcing.json")`, dumped
    #           2000 lines later), so the only honest local signal is that the
    #           file writes *something* and the artifact is committed.
    #
    # Rule `file` is safe because of the runner's mtime guard: if a record names
    # an artifact the run does not actually rewrite, the result is SKIP ("nothing
    # was compared"), never PASS. A wrong guess costs a skipped record, not a
    # false green.
    file_writes = bool(_WRITE_CTX.search(src))
    by_rule: dict[str, str] = {}
    read_only: list[str] = []
    for i, line in enumerate(lines):
        for lit in _ARTIFACT_RE.findall(line):
            if "{" in lit or "%" in lit:
                continue
            norm = lit.lstrip("./")
            cand = (norm if norm.startswith("test-results/")
                    else "test-results/" + os.path.basename(norm))
            if cand not in tracked:
                continue
            lo, hi = max(0, i - _WRITE_WINDOW), min(len(lines), i + _WRITE_WINDOW + 1)
            if _WRITE_CTX.search("\n".join(lines[lo:hi])):
                by_rule[cand] = "local"
            elif file_writes:
                by_rule.setdefault(cand, "file")
            else:
                read_only.append(cand)
    written = sorted(by_rule)

    findings = sorted(set(FINDING_RE.findall(os.path.basename(rel) + " " + doc)),
                      key=lambda s: (len(s), s))
    return {
        "findings": findings,
        "pytest_funcs": bool(re.search(r"^\s*(?:async )?def test_|^\s*class Test",
                                       src, re.M)),
        "has_assert": bool(re.search(r"^\s*assert\b", src, re.M)),
        "has_main": "__main__" in src,
        "lines": len(lines),
        "test_funcs": sorted(n for n in defines if n.startswith("test_")),
        "writes": written,
        "write_rule": dict(sorted(by_rule.items())),
        "reads_only": sorted(set(read_only) - set(written)),
        "summary": (doc.splitlines()[0][:150] if doc else ""),
    }


def _finding_sectors() -> dict[str, set[str]]:
    """{finding id -> sectors of the modules that implement it} (D11 join).

    Needed because 96 test files import no model module at all — they are
    self-contained sympy/numpy derivations. Their sector is not "unknown": it is
    the sector of the code that owns the finding they verify, which the module
    registry already records.
    """
    out: dict[str, set[str]] = {}
    for rec in _yaml(MANIFEST).get("modules") or []:
        sec = rec.get("sector")
        if not sec:
            continue
        for f in rec.get("findings") or []:
            out.setdefault(str(f).upper(), set()).add(sec)
    return out


def _sector_for(rel: str, imports: dict[str, list[str]],
                sec_of: dict[str, str],
                finding_sectors: dict[str, set[str]] | None = None,
                findings: list[str] | None = None) -> str:
    if rel.startswith("tests/casim/"):
        return "suite"                     # the package's own gate suite
    hits: set[str] = set()
    for imp in imports.get(rel, ()):  # noqa: B007
        key = imp.replace(os.sep, "/")
        if key in sec_of:
            hits.add(sec_of[key])
            continue
        # `src/casim/engine/<sector>/x.py` names its own sector.
        m = re.search(r"src/casim/engine/([a-z]+)/", key)
        if m:
            hits.add(m.group(1))
        elif key.startswith("src/casim/numerics"):
            hits.add("numerics")
    for cand in _SECTOR_PRIORITY:
        if cand in hits:
            return cand
    # No import evidence: fall back to the sector that owns the finding.
    if finding_sectors and findings:
        for f in findings:
            hits |= finding_sectors.get(f.upper(), set())
        for cand in _SECTOR_PRIORITY:
            if cand in hits:
                return cand
    return "core"


def _id_for(rel: str, used: set[str]) -> str:
    stem = os.path.splitext(os.path.basename(rel))[0]
    stem = re.sub(r"^test_", "", stem)
    base = stem.replace("_", "-").strip("-") or "unnamed"
    if base not in used:
        return base
    suite = rel.split("/")[1]
    cand = f"{base}.{suite}"
    n = 2
    while cand in used:
        cand = f"{base}.{suite}{n}"
        n += 1
    return cand


# ---------------------------------------------------------------------------
def build(promote: bool = False) -> dict[str, list[dict[str, Any]]]:
    """{sector -> [record dict]}, merging human-owned fields from disk.

    `promote=True` performs the one-way C7.5 upgrade described inline below.
    """
    tracked = _tracked_files()
    sec_of = _sector_maps()
    imports = _graph_imports()
    ledger = _ledger_test_status()
    finding_sectors = _finding_sectors()

    # existing records, keyed by path, so human edits survive
    existing: dict[str, dict[str, Any]] = {}
    if os.path.isdir(REGISTRY_DIR):
        for fn in sorted(os.listdir(REGISTRY_DIR)):
            if fn.endswith((".yaml", ".yml")):
                for d in _yaml(os.path.join(REGISTRY_DIR, fn)).get("tests") or []:
                    if d.get("path"):
                        existing[d["path"]] = d
                    else:
                        existing[f"@{d['id']}"] = d      # registry-only record

    files: list[str] = []
    for d in TEST_DIRS:
        full = os.path.join(_REPO, d)
        if not os.path.isdir(full):
            continue
        files += [f"{d}/{fn}" for fn in sorted(os.listdir(full))
                  if fn.endswith(".py") and fn not in _NOT_A_TEST]
    files.sort()

    used_ids = {d["id"] for d in existing.values() if d.get("id")}
    out: dict[str, list[dict[str, Any]]] = {}

    for rel in files:
        ev = _scan_file(rel, tracked)
        prior = existing.get(rel)
        led_status, led_id = ledger.get(rel, ("", ""))

        if prior:
            rec = dict(prior)                            # human fields win
            # --promote is the ONE way this tool may change an existing record's
            # kind, and it only ever ADDS a failure mode: a `legacy_script`
            # record whose file writes a committed artifact becomes a
            # `result_dump` with that artifact as its baseline. It never demotes,
            # never touches a record that already has a failure mode, and never
            # runs unless asked (roadmap C7.5).
            if (promote and rec.get("kind") == "legacy_script"
                    and rec.get("tier") != "archive"
                    and not rec.get("results") and ev["writes"]):
                rec["kind"] = "result_dump"
                rec["results"] = ev["writes"]
                note = (f"promoted legacy_script -> result_dump by "
                        f"tools/gen_test_registry.py --promote (C7.5): the run "
                        f"rewrites {len(ev['writes'])} committed artifact(s), so "
                        f"the baseline diff vs HEAD is its failure mode")
                rec["notes"] = (rec.get("notes") + "; " if rec.get("notes")
                                else "") + note
        else:
            rec = {"id": _id_for(rel, used_ids), "path": rel}
            used_ids.add(rec["id"])
            if led_status == "fully_superseded":
                rec["kind"] = "legacy_script"
                rec["tier"] = "archive"
                rec["superseded_by"] = led_id
                rec["notes"] = ("fully superseded per docs/theory/"
                                "supersessions.yaml; retired at C7.6")
            elif ev["pytest_funcs"] and ev["has_assert"]:
                rec["kind"] = "assertion"
                rec["tier"] = "gate" if rel.startswith("tests/casim/") else "battery"
            elif ev["writes"]:
                rec["kind"] = "result_dump"
                rec["tier"] = "battery"
                rec["results"] = ev["writes"]
            else:
                rec["kind"] = "legacy_script"
                rec["tier"] = "battery"
            if ev["findings"]:
                rec["findings"] = ev["findings"]

        rec.setdefault("kind", "legacy_script")
        rec.setdefault("tier", "battery")
        rec["sector"] = rec.get("sector") or _sector_for(
            rel, imports, sec_of, finding_sectors, ev["findings"])
        if ev["findings"] and not rec.get("findings"):
            rec["findings"] = ev["findings"]

        # generated evidence, always refreshed
        rec["evidence"] = {
            "pytest_funcs": ev["pytest_funcs"],
            "has_assert": ev["has_assert"],
            "has_main": ev["has_main"],
            "lines": ev["lines"],
            "n_test_funcs": len(ev["test_funcs"]),
            "artifacts_written": ev["writes"],
            "artifact_rule": ev["write_rule"],
            "artifacts_read_only": ev["reads_only"],
            "summary": ev["summary"],
        }
        if led_status:
            rec["evidence"]["ledger_status"] = led_status
            rec["evidence"]["ledger_record"] = led_id
        out.setdefault(rec["sector"], []).append(rec)

    # carry registry-only records (scenarios etc.) that own no test file
    for key, d in existing.items():
        if key.startswith("@"):
            out.setdefault(d.get("sector", "suite"), []).append(dict(d))

    for sec in out:
        out[sec].sort(key=lambda r: r["id"])
    return out


_ABOUT = (
    "Roadmap C7.1, decision D9. One declarative record per test file: what it "
    "runs, at what parameters, and how it fails. `casim test` and `pytest` both "
    "execute THESE records (src/casim/tests/), so they cannot diverge. "
    "AUTO-SCAFFOLDED by tools/gen_test_registry.py: the `evidence:` block is "
    "generated and rewritten on every run; every other field is human-owned and "
    "preserved. Promote a record off `legacy_script` by adding `module:`/`entry:` "
    "(+ `params:`/`expect:`) — that is the C7.4/C7.5 work, and regeneration will "
    "not undo it."
)


def write(records: dict[str, list[dict[str, Any]]]) -> list[str]:
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    written = []
    for sector, recs in sorted(records.items()):
        path = os.path.join(REGISTRY_DIR, f"{sector}.yaml")
        doc = {"version": 1, "sector": sector, "about": _ABOUT, "tests": recs}
        text = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                              width=100)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        written.append(os.path.relpath(path, _REPO))
    return written


def _rendered(records: dict[str, list[dict[str, Any]]]) -> dict[str, str]:
    return {sector: yaml.safe_dump(
        {"version": 1, "sector": sector, "about": _ABOUT, "tests": recs},
        sort_keys=False, allow_unicode=True, width=100)
        for sector, recs in sorted(records.items())}


_DEBT_NOTES = {
    "absent_artifact": (
        "DEBT CATEGORY (C7 close-out): the file names a result artifact that is "
        "not committed and not on disk, so there is no baseline to diff — run it "
        "once, review the numbers, `git add` the artifact, then promote with "
        "`tools/gen_test_registry.py --promote`. Cheapest of the three debt "
        "categories to clear."),
    "emits_nothing": (
        "DEBT CATEGORY (C7 close-out): emits no result artifact at all, so a "
        "baseline diff cannot give it a failure mode. Needs either an `assert` or "
        "an entry function returning a dict that a `result_dump` record can "
        "write. Until then it runs and cannot fail, which is what "
        "`legacy_script` says."),
}


def classify_debt() -> int:
    """Write a measured debt category into every unannotated legacy_script record.

    Roadmap C7 close-out. The 47 debt records are not one problem: 9 were demoted
    by the arming pass (they already carry that note), 11 name an artifact nobody
    ever committed, and 27 emit nothing at all. Those need different work, so the
    record says which — otherwise the next session re-derives the split, which
    took a full scan to establish.

    One-way: a record that already has notes is left alone.
    """
    tracked = _tracked_files()
    records = build()
    changed = 0
    counts: dict[str, int] = {}
    for sector, recs in records.items():
        for rec in recs:
            if rec.get("kind") != "legacy_script" or rec.get("notes"):
                continue
            ev = rec.get("evidence") or {}
            src_path = rec.get("path")
            lits = set()
            if src_path and os.path.exists(os.path.join(_REPO, src_path)):
                with open(os.path.join(_REPO, src_path), encoding="utf-8",
                          errors="replace") as fh:
                    text = fh.read()
                for lit in _ARTIFACT_RE.findall(text):
                    if "{" in lit or "%" in lit:
                        continue
                    norm = lit.lstrip("./")
                    lits.add(norm if norm.startswith("test-results/")
                             else "test-results/" + os.path.basename(norm))
            cat = ("emits_nothing" if not lits
                   else "absent_artifact" if not (lits & tracked)
                   else None)
            if cat is None:
                continue                      # tracked artifact: not plain debt
            rec["notes"] = _DEBT_NOTES[cat]
            counts[cat] = counts.get(cat, 0) + 1
            changed += 1
    if changed:
        write(records)
    print(f"[test-registry] annotated {changed} debt record(s): "
          + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the registry on disk is stale")
    ap.add_argument("--report", action="store_true",
                    help="print a summary and exit without writing")
    ap.add_argument("--classify-debt", action="store_true",
                    help="C7 close-out: write a measured debt category into every "
                         "unannotated legacy_script record (one-way)")
    ap.add_argument("--promote", action="store_true",
                    help="C7.5: upgrade legacy_script records whose file writes "
                         "a committed artifact to result_dump (one-way; never "
                         "removes a failure mode)")
    args = ap.parse_args()

    if args.classify_debt:
        return classify_debt()
    records = build(promote=args.promote)
    n = sum(len(v) for v in records.values())
    kinds: dict[str, int] = {}
    tiers: dict[str, int] = {}
    for recs in records.values():
        for r in recs:
            kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
            tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1

    if args.check:
        want = _rendered(records)
        stale = []
        for sector, text in want.items():
            path = os.path.join(REGISTRY_DIR, f"{sector}.yaml")
            if not os.path.exists(path):
                stale.append(f"tests/registry/{sector}.yaml missing")
                continue
            with open(path, encoding="utf-8") as fh:
                if fh.read() != text:
                    stale.append(f"tests/registry/{sector}.yaml is stale")
        extra = [fn for fn in (os.listdir(REGISTRY_DIR)
                               if os.path.isdir(REGISTRY_DIR) else [])
                 if fn.endswith((".yaml", ".yml"))
                 and fn[:-5] not in want and fn[:-4] not in want]
        stale += [f"tests/registry/{fn} has no sector" for fn in extra]
        if stale:
            print("[test-registry] STALE — run tools/gen_test_registry.py")
            for s in stale:
                print(f"    {s}")
            return 1
        print(f"[test-registry] current: {n} record(s) across "
              f"{len(records)} sector file(s)")
        return 0

    print(f"[test-registry] {n} record(s), {len(records)} sector file(s)")
    print("  kinds: " + "  ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    print("  tiers: " + "  ".join(f"{k}={v}" for k, v in sorted(tiers.items())))
    print("  sectors: " + "  ".join(f"{k}={len(v)}"
                                    for k, v in sorted(records.items())))
    if args.report:
        return 0
    for p in write(records):
        print(f"  wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
