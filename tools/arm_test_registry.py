#!/usr/bin/env python3
"""Arm the C7 `result_dump` promotions — roadmap C7.5 follow-through.

The problem this closes
-----------------------
C7 promoted 226 records from `legacy_script` to `result_dump` on *evidence* that
the test writes a committed artifact: the artifact path appears in the source and
the file writes something. Evidence is not proof. A record is **armed** only when
a run actually rewrites the baseline it declares — otherwise the runner compares
the committed file against itself and reports `SKIP` ("nothing was actually
compared"), which is honest but means the record still has no failure mode.

So the promotion has to be *tested*, one record at a time, and the verdict
written back. That is what this does.

Three verdicts
--------------
``armed``    the run rewrote at least one declared baseline and the numbers were
             diffed against git HEAD. PASS (reproduced) or FAIL (drifted) — both
             mean the record has a real failure mode.
``stale``    armed, and the supersession ledger declares the baseline
             `stale_by_design`: the numbers predate a deliberate model change, so
             a re-run is expected to differ. The record keeps its failure mode.
``unarmed``  the run finished but touched no declared baseline. The promotion was
             wrong; the record is demoted back to `legacy_script` with the reason
             recorded, which is the honest state, not a regression.
``timeout``  this sitting could not wait long enough. NOT a verdict about the
             record — re-attempted automatically when `--timeout` is raised.
``error``    the script crashed or needs something the environment lacks.
             Left as-is and reported: an error is not evidence either way.

Why it is resumable
-------------------
Some of these scripts run for minutes and the whole set runs for hours, while a
sandboxed shell call is capped at well under a minute. The journal
(`test-results/arming-journal.json`) records every verdict as it lands, so the
pass can be driven in as many sittings as it takes and picks up where it stopped.
`--budget` bounds one sitting in wall-clock seconds so a call never dies mid-record
and loses its verdict.

Usage
-----
    python3 tools/arm_test_registry.py --budget 35          # one sitting
    python3 tools/arm_test_registry.py --budget 35 --timeout 25
    python3 tools/arm_test_registry.py --status             # progress, no runs
    python3 tools/arm_test_registry.py --apply              # write verdicts back
    python3 tools/arm_test_registry.py --id <record-id>     # one record

`--apply` is deliberately separate from the runs: demoting 40 records is a change
to the registry, and it should happen once, deliberately, after the evidence is
in — not as a side effect of a timed-out sitting.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "src"))

JOURNAL = os.path.join(_REPO, "test-results", "arming-journal.json")


def _load_journal() -> dict:
    if os.path.exists(JOURNAL):
        with open(JOURNAL, encoding="utf-8") as fh:
            return json.load(fh)
    return {"version": 1, "about": (
        "Roadmap C7.5 arming pass. One entry per result_dump record: did a real "
        "run rewrite the baseline it declares? `armed` = yes (and the diff verdict "
        "follows); `unarmed` = no, so the promotion was wrong and the record is "
        "demoted back to legacy_script; `error` = could not be established. "
        "Written by tools/arm_test_registry.py; resumable."), "records": {}}


def _save_journal(j: dict) -> None:
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    with open(JOURNAL, "w", encoding="utf-8") as fh:
        json.dump(j, fh, indent=1, sort_keys=True)
        fh.write("\n")


def _pending(journal: dict, only_id: str | None,
             retry_timeouts: bool = False) -> list:
    from casim.tests import registry as treg
    recs = [r for r in treg.all_records() if r.kind == "result_dump"]
    if only_id:
        return [r for r in recs if r.id == only_id]
    # A `timeout` verdict is not a decision, but re-attempting it every sitting
    # burns the whole budget on the same two slow scripts. Retries are opt-in via
    # --retry-timeouts (with a bigger --timeout), so a sitting spends its seconds
    # on records that have never been tried.
    done = set(journal["records"])
    if retry_timeouts:
        done = {rid for rid, e in journal["records"].items()
                if e["verdict"] != "timeout"}
    # Cheapest first: a smaller file is usually a faster script, and getting
    # verdicts on the many quick ones beats stalling on one slow one.
    todo = [r for r in recs if r.id not in done]
    todo.sort(key=lambda r: r.evidence.get("lines") or 10 ** 6)
    return todo


def _run_one(rec, timeout: float) -> dict:
    from casim.tests import runner as trunner
    t0 = time.time()
    res = trunner.run_record(rec, timeout=timeout)
    verdict = {
        "PASS": "armed", "FAIL": "armed",
        # STALE is armed too: the record HAS a failure mode, and the ledger has
        # decided its committed numbers predate a model change. Folding it into
        # `armed` would hide the distinction the ledger exists to draw.
        "STALE": "stale",
        "SKIP": "unarmed", "ERROR": "error", "DEBT": "error",
        "SWEEP": "error",
    }.get(res.status, "error")
    # A timeout is NOT an error verdict: it says nothing about whether the record
    # is armed, only that this sandbox could not wait. Recorded separately so the
    # handoff can name the machine that should finish it, and so a re-run with a
    # bigger --timeout picks exactly these up.
    if "timed out" in res.detail:
        verdict = "timeout"
    return {
        "verdict": verdict,
        "status": res.status,
        "detail": res.detail[:300],
        "seconds": round(time.time() - t0, 1),
        "path": rec.path,
        "results": list(rec.results),
        "compared": res.metrics.get("compared"),
    }


def _apply(journal: dict) -> int:
    """Write the verdicts back into tests/registry/*.yaml."""
    import yaml
    from casim.tests import registry as treg

    demote = {rid: e for rid, e in journal["records"].items()
              if e["verdict"] == "unarmed"}
    if not demote:
        print("[arming] nothing to apply — no `unarmed` verdicts recorded.")
        return 0

    changed = 0
    by_file: dict[str, list[str]] = {}
    for rid in demote:
        try:
            by_file.setdefault(treg.get(rid).source_file, []).append(rid)
        except KeyError:
            print(f"[arming] {rid} is no longer in the registry; skipping")
    for src, ids in sorted(by_file.items()):
        path = os.path.join(_REPO, src)
        with open(path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        for r in doc["tests"]:
            if r["id"] not in ids or r.get("kind") != "result_dump":
                continue
            r["kind"] = "legacy_script"
            r.pop("results", None)
            note = ("DEMOTED result_dump -> legacy_script by "
                    "tools/arm_test_registry.py --apply (C7.5): a real run did "
                    "not rewrite the declared baseline, so the promotion gave it "
                    "no failure mode. Declared debt is the honest state.")
            r["notes"] = ((r.get("notes", "") + "; ") if r.get("notes") else "") + note
            changed += 1
        with open(path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(doc, fh, sort_keys=False, allow_unicode=True, width=100)
    print(f"[arming] demoted {changed} record(s) to legacy_script across "
          f"{len(by_file)} registry file(s).")
    print("[arming] now re-run: python3 tools/gen_test_registry.py && "
          "python3 -m casim.cli index")
    return 0


def _restore(journal: dict, keep: set[str]) -> int:
    """Put every artifact this pass rewrote-with-drift back to its HEAD content.

    An arming run is an experiment, not an acceptance: it rewrites the committed
    baseline in place (that is how P1.2's diff works) and a drifted record leaves
    a modified file behind. Leaving twelve of those in the tree would hand the
    next session a diff it did not make and cannot attribute, so the evidence
    lives in the journal and the working tree goes back to where it was.

    `keep` names artifacts that were ALREADY modified before the pass — those are
    somebody else's change and must not be touched.

    A `stale_by_design` baseline is restored like any other. Re-blessing it is a
    deliberate act (run, review, `git add`, flip the ledger entry to `live`), not
    a side effect of the pass that discovered it was stale.
    """
    import subprocess
    # EVERY artifact the pass rewrote, not just the ones that failed. The
    # floor-aware runner calls a sub-floor change "noise" and passes the record,
    # but `tools/check_result_drift.py` runs strict (floor 0) and reports the same
    # file as drift — so a passing run still leaves the tree dirty against the
    # project's other checker. Restoring only the failures left 14 sub-floor
    # rewrites behind, which is how this was found.
    drifted: set[str] = set()
    for e in journal["records"].values():
        drifted.update(e.get("results") or ())
    todo = sorted(drifted - keep)
    if not todo:
        print("[arming] nothing to restore.")
        return 0
    restored, failed = 0, []
    for rel in todo:
        proc = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=_REPO,
                              capture_output=True, text=True)
        if proc.returncode != 0:
            failed.append(rel)
            continue
        with open(os.path.join(_REPO, rel), "w", encoding="utf-8") as fh:
            fh.write(proc.stdout)
        restored += 1
        print(f"  restored {rel}")
    print(f"[arming] restored {restored} artifact(s) to HEAD; the drift is "
          f"recorded in {os.path.relpath(JOURNAL, _REPO)}, not in the tree.")
    if failed:
        print(f"[arming] could NOT restore (untracked at HEAD?): {failed}")
    if keep:
        print(f"[arming] left alone (modified before this pass): {sorted(keep)}")
    return 0


def _status(journal: dict) -> int:
    from casim.tests import registry as treg
    total = sum(1 for r in treg.all_records() if r.kind == "result_dump")
    recs = journal["records"]
    counts: dict[str, int] = {}
    for e in recs.values():
        counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
    print(f"\narming pass (C7.5)   {len(recs)} of {total} result_dump record(s) "
          f"decided ({100.0 * len(recs) / total:.0f}%)")
    for v in ("armed", "stale", "unarmed", "timeout", "error"):
        print(f"  {v:8s} {counts.get(v, 0)}")
    drifted = [rid for rid, e in recs.items() if e["status"] == "FAIL"]
    if drifted:
        print(f"\n  {len(drifted)} armed record(s) FAIL on drift vs HEAD — a real "
              f"failure mode doing its job:")
        for rid in sorted(drifted)[:10]:
            print(f"    {rid}: {recs[rid]['detail'][:90]}")
    slow = sorted(recs.items(), key=lambda kv: -kv[1]["seconds"])[:3]
    if slow:
        print("\n  slowest: " + ", ".join(f"{k} {v['seconds']}s" for k, v in slow))
    if len(recs) < total:
        print(f"\n  resume with: python3 tools/arm_test_registry.py --budget 35")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=35.0,
                    help="wall-clock seconds for this sitting (default 35)")
    ap.add_argument("--timeout", type=float, default=30.0,
                    help="per-record timeout (default 30)")
    ap.add_argument("--id", default=None, help="run exactly one record")
    ap.add_argument("--status", action="store_true", help="progress only, no runs")
    ap.add_argument("--retry-timeouts", action="store_true",
                    help="re-attempt records that previously timed out (pair "
                         "with a bigger --timeout)")
    ap.add_argument("--restore", action="store_true",
                    help="restore artifacts this pass rewrote-with-drift back to "
                         "their HEAD content (the drift stays in the journal)")
    ap.add_argument("--keep", default="",
                    help="comma list of artifacts that were already modified "
                         "before the pass; --restore will not touch them")
    ap.add_argument("--apply", action="store_true",
                    help="write recorded verdicts back into the registry")
    args = ap.parse_args()

    journal = _load_journal()
    if args.status:
        return _status(journal)
    if args.restore:
        keep = {k.strip() for k in args.keep.split(",") if k.strip()}
        return _restore(journal, keep)
    if args.apply:
        return _apply(journal)

    todo = _pending(journal, args.id, args.retry_timeouts)
    if not todo:
        print("[arming] nothing pending.")
        return _status(journal)

    t0 = time.time()
    ran = 0
    for rec in todo:
        if time.time() - t0 > args.budget:
            break
        entry = _run_one(rec, args.timeout)
        journal["records"][rec.id] = entry
        _save_journal(journal)                 # after EVERY record: resumability
        ran += 1
        print(f"  [{entry['verdict']:8s}] {rec.id:46s} "
              f"{entry['status']:6s} ({entry['seconds']:5.1f}s) "
              f"{entry['detail'][:70]}", flush=True)
    print(f"\n[arming] {ran} record(s) this sitting, "
          f"{len(journal['records'])} decided in total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
