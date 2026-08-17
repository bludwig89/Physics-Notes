#!/usr/bin/env python3
"""Check soundness — a check that cannot go red is not a check (D9, row **H2**).

Gap #3 of `docs/status/completeness-2026-08-07.md`, whose complaint was not that
the norm was missing but that it was *unmechanised*: ten gate records state their
negative controls in an English sentence in `notes:` ("`--param tower=symmetric`
reds L2 and L3", "all four controls verified red on their own legs"), the norm
propagated to every new session, and the instrument numbers — `unfalsifiable 72`,
`no_assert 233`, `import_time 328` — came back **bit-identical** across three
days and fourteen findings. The report's own diagnosis: *"the norm propagated,
the mechanism did not."*

What this tool adds is the mechanism, and only that. `check_test_registry.py`
already refuses a record with no *declared* failure mode; nothing established
that the declared one can trip. The repo's worked example of the gap is F22,
whose headline verification reduced to ``x - (1 - 2(1-x)/2)`` — identically zero
for any expression at all. It returned residual 0 from a deliberately wrong rho,
then from ``rho = 42``, and it was green for months.

Three modes, because the cost of the answer varies by three orders of magnitude
-------------------------------------------------------------------------------
``--gate`` (in ``make gate``, <1 s)
    Static. Every gate-tier ``kind: assertion`` record's control block is
    well-formed, and every control has a **journalled CONTROL verdict whose
    fingerprint matches the code as it stands now**. Nothing is executed. This is
    the `result_dump` bargain one level up: that kind is armed by committing a
    baseline, and a control is armed by committing a verdict that names the code
    it was measured against. Touch the driver and the fingerprint moves, the
    verdict goes stale, and the gate says which record to re-verify.

``--run`` (minutes; ``make control``)
    Executes them. One unperturbed run per record plus one perturbed run per
    control, judged on legs. Journals after every record, so the ~45 s sandbox
    ceiling costs a resume rather than the pass.

``--suggest``
    The retrofit worklist: gate assertions with no control, each with the
    keyword arguments its entry point already accepts — which is usually where
    the perturbation is hiding, since these drivers were written with control
    switches (``linear_control``, ``tower``, ``rho_override``) and then only ever
    exercised by hand.

Why a missing control is debt and a malformed one is an error
------------------------------------------------------------
Requiring all 55 gate assertions to declare a control on day one turns the gate
red for a week, and a gate that is red for a week is a gate people learn to run
with ``|| true``. So absence is a counted number that may only fall
(``gate_assertion_no_control`` in ``tools/audit_tests.py``) and malformation is
immediate. That is the ``legacy_script`` shape — the one migration ramp in this
repo that actually drained, 345 files to a countable remainder — rather than the
big-bang alternative that has never worked here once.

Usage:
    python3 tools/check_control_soundness.py --gate         # the barrier
    python3 tools/check_control_soundness.py --run          # verify + journal
    python3 tools/check_control_soundness.py --run --tier battery
    python3 tools/check_control_soundness.py --run --id F300-lattice-thermodynamics
    python3 tools/check_control_soundness.py --suggest
    python3 tools/check_control_soundness.py --status       # counts only
"""
from __future__ import annotations

import argparse
import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BOTH, and the repo root is not optional. 31 gate records name a `module:` under
# `tests.findings.*` rather than `casim.*`; with only `src` on the path they raise
# ModuleNotFoundError, which `--suggest` reported as "could not import" for five
# records and which would make `run_control` return INVALID for any control
# declared on them. Running from the repo root does not fix it either — Python
# puts the SCRIPT's directory on sys.path, i.e. `tools/`, never the cwd.
sys.path.insert(0, os.path.join(_REPO, "src"))
sys.path.insert(0, _REPO)

from casim.tests import registry as treg          # noqa: E402
from casim.tests import runner as trunner         # noqa: E402

JOURNAL = os.path.join(_REPO, "test-results", "control-soundness.json")
CAN_FAIL_JOURNAL = os.path.join(_REPO, "test-results", "can-fail.json")


# ---------------------------------------------------------------------------
def _load_journal(path: str) -> dict[str, list[dict]]:
    """``{record id -> [verdict item]}`` from the committed journal."""
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}
    out: dict[str, list[dict]] = {}
    for it in doc.get("items") or []:
        out.setdefault(str(it.get("id", "")).split("#")[0], []).append(it)
    return out


def _select(args) -> list[treg.TestRecord]:
    ids = ([s.strip() for s in args.id.split(",") if s.strip()]
           if args.id else None)
    recs = treg.select(ids=ids, finding=args.finding, sector=args.sector,
                       tier=args.tier, kind=args.kind)
    if ids or args.finding or args.sector or args.tier or args.kind:
        return [r for r in recs if r.needs_control or r.control]
    return [r for r in recs if r.needs_control or r.control]


# ---------------------------------------------------------------------------
def static_check(verbose: bool = False) -> int:
    """The gate. Declaration shape + journal freshness. Executes nothing."""
    recs = treg.all_records()
    c = treg.counts()
    journal = _load_journal(JOURNAL)

    # 1. Malformed control blocks are an immediate error. `validate()` owns the
    #    rules; this surfaces only the control half so the message names the
    #    right file.
    malformed: list[str] = []
    for r in recs:
        if not r.control:
            continue
        errs = treg._validate_controls(r)
        malformed += [f"{r.id}: {e}" for e in errs]

    # 2. Every declared control needs a journalled CONTROL verdict at the
    #    current fingerprint. Unverified and stale are reported apart, because
    #    they are different jobs: one is "run it once", the other is "the code
    #    moved under a verdict somebody already banked".
    unverified: list[str] = []
    stale: list[str] = []
    unsound: list[str] = []
    verified = 0
    for r in recs:
        if not r.control:
            continue
        fp = trunner.record_fingerprint(r, _REPO)
        items = journal.get(r.id) or []
        by_ix = {it.get("metrics", {}).get("control_index"): it for it in items}
        for i, ctl in enumerate(r.control):
            it = by_ix.get(i)
            label = f"{r.id}#control{i}  ({trunner._fmt(ctl.get('params') or {}) or ctl.get('test', '?')})"
            if it is None:
                unverified.append(label)
            elif it.get("metrics", {}).get("fingerprint") != fp:
                stale.append(f"{label}\n        verdict was measured against "
                             f"different code — re-run `make control`")
            elif it.get("status") not in ("CONTROL",):
                unsound.append(f"{label}\n        journalled "
                               f"{it.get('status')}: "
                               f"{str(it.get('detail'))[:150]}")
            else:
                verified += 1

    need = c["needs_control"]
    missing = c["gate_assertion_no_control"]
    print(f"[control-soundness] gate-tier assertion records: {need}")
    print(f"    with a declared control   {need - missing}  "
          f"(strong {c['control_strong']}, weak {c['control_weak']})")
    print(f"    NO CONTROL                {missing}  "
          f"(declared debt — ratcheted to zero, `make health`)")
    print(f"    controls declared         {c['controls_declared']}, "
          f"of which {verified} verified RED at the current fingerprint")

    bad = malformed + stale + unsound
    if malformed:
        print(f"\n[control-soundness] {len(malformed)} malformed control "
              f"block(s):")
        for e in malformed[:20]:
            print(f"    {e}")
    if unsound:
        print(f"\n[control-soundness] {len(unsound)} control(s) journalled NOT "
              f"SOUND — the perturbation did not redden what it declared:")
        for e in unsound[:20]:
            print(f"    {e}")
    if stale:
        print(f"\n[control-soundness] {len(stale)} control verdict(s) STALE — "
              f"the code changed since they were measured:")
        for e in stale[:20]:
            print(f"    {e}")
        print("    run: make control")
    if unverified:
        # Not fatal on its own: a control that is declared but never run is the
        # same category as a `result_dump` whose baseline is untracked — armed on
        # paper, not yet proved. It is printed every run so it cannot sit.
        print(f"\n[control-soundness] {len(unverified)} control(s) declared but "
              f"never verified (run `make control` to arm them):")
        for e in unverified[:20]:
            print(f"    {e}")
    if verbose:
        for r in recs:
            if r.needs_control and not r.control:
                print(f"    debt: {r.id:46s} {r.entry or r.path}")

    if bad:
        print(f"\n[control-soundness] FAILED — {len(bad)} problem(s).")
        return 1
    print(f"\n[control-soundness] OK — every declared control is well-formed "
          f"and no verdict is stale.")
    return 0


def run_check(args) -> int:
    recs = _select(args)
    if not recs:
        print("[control-soundness] no record matches that selection.")
        return 1
    print(f"[control-soundness] verifying controls on {len(recs)} record(s)")

    def echo(res: trunner.RunResult) -> None:
        print(f"  [{res.status:8s}] {res.id:46s} ({res.seconds:6.1f}s)"
              + (f"  — {res.detail[:100]}" if res.detail else ""), flush=True)

    rep = trunner.control_selection(recs, repo_root=_REPO,
                                    timeout=args.timeout, on_result=echo,
                                    journal=args.journal or JOURNAL)
    print(trunner.format_control_report(rep))
    print(f"\n[control-soundness] journal: "
          f"{os.path.relpath(args.journal or JOURNAL, _REPO)} — commit it; the "
          f"gate reads it instead of re-running these.")
    return 1 if rep["unsound"] else 0


def can_fail(args) -> int:
    """Measure can-fail by EXECUTION, one traced run per gate entry record.

    Replaces a static reachability walk that three records defeated by dispatching
    through a module-level table. Journalled to `test-results/can-fail.json` with a
    fingerprint per record, so `check_finding_records.py` can prefer a measurement
    over an inference and say which it used.
    """
    recs = [r for r in treg.select(tier="gate") if r.entry]
    if args.id:
        want = {s.strip() for s in args.id.split(",") if s.strip()}
        recs = [r for r in recs if r.id in want]
    prior = {}
    if os.path.exists(CAN_FAIL_JOURNAL) and not args.no_resume:
        try:
            with open(CAN_FAIL_JOURNAL, encoding="utf-8") as fh:
                prior = {it["id"]: it for it in (json.load(fh).get("items") or [])}
        except (OSError, json.JSONDecodeError, KeyError):
            prior = {}

    print(f"[can-fail] tracing {len(recs)} gate entry record(s); a record CAN "
          f"fail when an assert/raise line actually executes")
    items: list[dict] = []
    for r in recs:
        fp = trunner.record_fingerprint(r, _REPO)
        cached = prior.get(r.id)
        if cached and cached.get("fingerprint") == fp:
            it = dict(cached)
            it["journalled"] = True
        else:
            it = trunner.probe_can_fail(r, _REPO, args.timeout)
        items.append(it)
        mark = {"CAN_FAIL": "CAN FAIL", "CANNOT_FAIL": "cannot fail",
                "INCONCLUSIVE": "?INCONCL?"}.get(it.get("verdict"), "?")
        print(f"  [{mark:>11}] {r.id:<46} "
              f"guards {it['guards_executed']}/{it['guard_lines_total']:<4} "
              f"{it['status']:<6} ({it['seconds']:>5.1f}s)"
              + ("  [journalled]" if it.get("journalled") else ""), flush=True)
        _write_can_fail(items, prior, {r2.id for r2 in recs})

    cannot = [it["id"] for it in items if it.get("verdict") == "CANNOT_FAIL"]
    unknown = [it["id"] for it in items if it.get("verdict") == "INCONCLUSIVE"]
    print(f"\n[can-fail] {sum(1 for i in items if i.get('verdict') == 'CAN_FAIL')} "
          f"of {len(items)} can fail; {len(cannot)} cannot; "
          f"{len(unknown)} inconclusive.")
    if cannot:
        print("  CANNOT FAIL (a gate record with no demonstrated failure path):")
        for cid in cannot:
            print(f"    {cid}")
    if unknown:
        print("  INCONCLUSIVE — timed out before reaching a guard. This is NOT "
              "cannot-fail;\n  an absence of evidence recorded as evidence of "
              "absence is the original defect:")
        for cid in unknown:
            print(f"    {cid}")
    print(f"\n[can-fail] journal: "
          f"{os.path.relpath(CAN_FAIL_JOURNAL, _REPO)} — commit it; "
          f"check_finding_records.py prefers it over its AST walk.")
    return 0


def _write_can_fail(items: list[dict], prior: dict, selected: set) -> None:
    import time
    carried = [it for cid, it in prior.items() if cid not in selected]
    payload = {"generated": time.strftime("%Y-%m-%d - %H:%M"),
               "method": "execution trace (sys.settrace): a record can fail when "
                         "an assert/raise line is actually reached",
               "n": len(items) + len(carried),
               "items": items + carried}
    os.makedirs(os.path.dirname(CAN_FAIL_JOURNAL), exist_ok=True)
    tmp = CAN_FAIL_JOURNAL + ".part"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)
    os.replace(tmp, CAN_FAIL_JOURNAL)


def suggest(args) -> int:
    """The retrofit worklist, with each entry point's own switches named."""
    import inspect
    rows: list[tuple[str, str, str]] = []
    for r in treg.all_records():
        if not r.needs_control or r.control:
            continue
        hint = ""
        if r.entry:
            try:
                fn = trunner._load_callable(r)
                sig = inspect.signature(fn)
                kw = [f"{p.name}={p.default!r}"
                      for p in sig.parameters.values()
                      if p.default is not inspect.Parameter.empty]
                hint = ", ".join(kw) or "(no keyword arguments — add one)"
            except Exception as exc:                       # noqa: BLE001
                hint = f"<could not import: {type(exc).__name__}>"
        else:
            hint = ("no `entry:` — pytest-delegating. Either promote it (C7.4) "
                    "or declare the weak `test:` form")
        rows.append((r.id, r.entry or r.path or "?", hint))

    print(f"[control-soundness] {len(rows)} gate-tier assertion record(s) with "
          f"no declared control.\n")
    print("The perturbation is usually already there: these drivers were "
          "written with\ncontrol switches and then only ever flipped by hand.\n")
    for rid, where, hint in rows:
        print(f"  {rid}")
        print(f"      {where}")
        print(f"      accepts: {hint}")
    print("\nDeclare one like this, in the record's tests/registry/*.yaml:\n")
    print("  control:\n"
          "    - params: {linear_control: true}\n"
          "      reds:   [G10-3, G10-4, G10-5, G10-6]\n"
          "      reason: dispersion replaced by exactly linear c|k|, so every\n"
          "              lattice correction must vanish\n")
    print("then `make control` to verify and journal it.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="negative-control soundness for test-registry records "
                    "(D9 / rubric row H2)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--gate", action="store_true",
                      help="static barrier: shape + journal freshness, runs "
                           "nothing (this is what `make gate` calls)")
    mode.add_argument("--run", action="store_true",
                      help="execute the declared controls and journal verdicts")
    mode.add_argument("--can-fail", dest="can_fail", action="store_true",
                      help="measure can-fail by EXECUTION: trace one run per gate "
                           "entry record and report which assert/raise lines were "
                           "actually reached (beats any AST walk on indirection)")
    mode.add_argument("--suggest", action="store_true",
                      help="list gate records with no control, with hints")
    mode.add_argument("--status", action="store_true",
                      help="counts only, exit 0")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="with --gate: also name every record still in debt")
    ap.add_argument("--id", default=None, help="comma list of record ids")
    ap.add_argument("--finding", default=None)
    ap.add_argument("--sector", default=None)
    ap.add_argument("--tier", default=None)
    ap.add_argument("--kind", default=None)
    ap.add_argument("--timeout", type=float, default=None)
    ap.add_argument("--journal", default=None,
                    help=f"default {os.path.relpath(JOURNAL, _REPO)}")
    ap.add_argument("--no-resume", action="store_true",
                    help="with --can-fail: re-trace every record, ignoring the "
                         "journalled verdicts")
    args = ap.parse_args()

    if args.can_fail:
        return can_fail(args)
    if args.run:
        return run_check(args)
    if args.suggest:
        return suggest(args)
    if args.status:
        static_check(args.verbose)
        return 0
    return static_check(args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
