"""casim.tests.runner — the one test executor (roadmap C7.2/C7.3, **D9**).

Every path into the suite ends here: ``casim test`` calls :func:`run_selection`,
and ``pytest`` collects items that call :func:`run_record`. The two cannot
diverge, because there is only one object being run.

Status vocabulary — deliberately not four synonyms for "fine":

  ``PASS``   the record's declared failure mode was exercised and did not trip
  ``FAIL``   it tripped: an assertion, a gated observable, or numeric drift
  ``ERROR``  the test could not be run (import error, crash, timeout)
  ``SKIP``   not runnable in this environment (missing pytest, no baseline)
  ``DEBT``   a ``legacy_script`` record ran and exited 0. **This is not a pass.**
             It is P1's `RAN` limbo, renamed to what it is and counted.
  ``SWEEP``  a ``--param`` run at a perturbed value; the drift IS the output, so
             calling it pass or fail would be a category error.
  ``STALE``  the numbers moved, and the supersession ledger says this baseline
             predates a deliberate model change (``baselines:`` /
             ``stale_by_design``). Not a pass and not a failure: the physics was
             replaced on purpose and the committed value was never re-blessed.
             Only a DECIDED ledger entry produces this; a ``candidate`` still
             reports ``FAIL``.

Two rules worth stating because they were easy to get wrong:

1. **A sweep never writes a baseline.** ``--param`` runs land in a temp dir and
   diff against the committed artifact. Overwriting ``test-results/*.json`` from
   a perturbed run would silently move the project's accepted values.
2. **No stdout scraping.** ``tools/run_gate.py`` rejected token counting for a
   reason (a script that prints "FAILURE MODE" in a heading is not failing).
   Status comes from exit codes, exceptions, JUnit XML and numeric diffs.
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from dataclasses import dataclass, field, asdict
from fractions import Fraction
from typing import Any, Callable, Iterable, Sequence

from . import registry as treg

__all__ = [
    "RunResult", "run_record", "run_selection", "format_report",
    "run_control", "control_selection", "format_control_report",
    "record_fingerprint", "leg_map", "resolve_leg", "probe_can_fail",
    "DEFAULT_TIMEOUT", "GATE_TIMEOUT", "STATUSES", "CONTROL_STATUSES",
]

STATUSES = ("PASS", "FAIL", "ERROR", "SKIP", "DEBT", "SWEEP", "STALE",
            "CONTROL", "LEAK", "SPILL", "INVALID", "NOCTRL")

# The control verdicts, which are a different question from the run statuses.
# A run asks "did this record's failure mode trip?"; a control asks "CAN it?"
#
#   ``CONTROL``  the declared perturbation reddened exactly the declared legs.
#                The check is sound: it has a demonstrated way to fail.
#   ``LEAK``     the perturbation was applied and the record stayed green. This
#                is the H2 defect, caught: whatever the record asserts, it does
#                not assert it against this. **Not ok.**
#   ``SPILL``    it reddened legs it did not declare. The prose form of this
#                contract has always said "and only where declared", because a
#                perturbation that breaks the whole run is a broken run and is
#                also the cheapest way to fake a red. **Not ok.**
#   ``INVALID``  the control could not be judged — a declared leg does not
#                exist, or was already red before the perturbation, or the run
#                crashed rather than failing. A control that proves nothing is
#                reported, never rounded to sound. **Not ok.**
#   ``NOCTRL``   the record declares no control. Counted debt, not a verdict;
#                `ok` so it cannot wall the gate, and ratcheted to zero.
CONTROL_STATUSES = ("CONTROL", "LEAK", "SPILL", "INVALID", "NOCTRL")

DEFAULT_TIMEOUT = 900.0
GATE_TIMEOUT = 300.0

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))


# ---------------------------------------------------------------------------
@dataclass
class RunResult:
    id: str
    kind: str
    status: str
    seconds: float = 0.0
    detail: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    swept: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """True when this result should not stop a gate.

        ``DEBT`` is deliberately included: a legacy_script record has no failure
        mode, so it cannot fail, and pretending otherwise would make the gate
        red for 200 files that C7 has not reached yet. The ratchet — not the
        gate's colour — is what drives that count to zero.

        ``STALE`` likewise: the ledger has *decided* that these numbers predate a
        model change, so failing the gate on them would punish the project for
        improving its own physics. The countable pressure is the ledger entry and
        its `clears_by:`, not a red gate.
        """
        return self.status in ("PASS", "SKIP", "DEBT", "SWEEP", "STALE",
                              "CONTROL", "NOCTRL")


def _jsonable(v: Any) -> Any:
    if isinstance(v, Fraction):
        return f"{v.numerator}/{v.denominator}"
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    return v


# ---------------------------------------------------------------------------
# entry-point resolution
# ---------------------------------------------------------------------------
def _load_callable(rec: treg.TestRecord) -> Callable[..., Any]:
    """Resolve ``module``/``entry`` (or ``path``/``entry``) to a callable."""
    if rec.module:
        mod = importlib.import_module(rec.module)
    else:
        full = os.path.join(_REPO, rec.path or "")
        name = "casim_regtest_" + os.path.basename(full)[:-3]
        spec = importlib.util.spec_from_file_location(name, full)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load {rec.path}")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    fn = getattr(mod, rec.entry or "", None)
    if fn is None or not callable(fn):
        raise AttributeError(
            f"{rec.module or rec.path} has no callable {rec.entry!r}")
    return fn


def _call(fn: Callable[..., Any], params: dict[str, Any]) -> Any:
    """Call `fn` with `params`, dropping keys the signature does not accept.

    A registry record may carry a parameter for documentation (`delta_star: 2/9`
    on a function that hard-codes nothing) or for a sibling entry point. Passing
    an unexpected keyword would turn that into a TypeError and read as a physics
    failure, which it is not.
    """
    import inspect
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return fn()
    accepts_kwargs = any(p.kind is inspect.Parameter.VAR_KEYWORD
                         for p in sig.parameters.values())
    if accepts_kwargs:
        return fn(**params)
    usable = {k: v for k, v in params.items() if k in sig.parameters}
    return fn(**usable)


def _interpret_return(value: Any) -> tuple[bool, str, dict]:
    """Map an entry point's return value onto (passed, detail, metrics)."""
    if value is None or value is True:
        return True, "", {}
    if value is False:
        return False, "entry point returned False", {}
    if isinstance(value, dict):
        # A dict is the result_dump payload; if it carries its own verdict,
        # honour it. `passed`/`pass`/`ok`/`gate` are the four spellings in use.
        for key in ("passed", "pass", "ok", "gate", "all_pass"):
            if isinstance(value.get(key), bool):
                return value[key], ("" if value[key]
                                    else f"{key}=False in the returned payload"), {}
        return True, "", {}
    if isinstance(value, (int, float)):
        return True, f"returned {value!r}", {}
    return True, "", {}


# ---------------------------------------------------------------------------
# baseline diffing (P1.2's engine, unchanged)
# ---------------------------------------------------------------------------
def _diff_against_head(paths: Sequence[str], repo_root: str,
                       payload_by_path: dict[str, Any] | None = None,
                       strict_floor: bool = False
                       ) -> tuple[list[str], int, list[str]]:
    """(drift lines, artifacts compared, round-off-floor lines).

    ``floor=MACHINE_FLOOR`` is on by default, per ``casim.baselines``: two values
    that are *both* under 1e-12 cannot be told apart by this project's own
    exactness standard, so reporting their difference as drift is incoherent.
    A residual moving 4.4e-16 -> 0.0 or 6.0e-15 -> 4.9e-15 is a different FFT
    thread count, not physics, and counting it as a failure is how a checker
    teaches people to ignore it.

    Floor deltas are **returned separately, never dropped**. A record that
    genuinely cares about sub-floor bits sets ``expect: {strict_floor: true}``.
    """
    from casim.baselines import (compare, git_show, significant, MACHINE_FLOOR)

    lines: list[str] = []
    floor_lines: list[str] = []
    n = 0
    for rel in paths:
        before = git_show(rel, "HEAD", cwd=repo_root)
        if before is None:
            continue                        # untracked: nothing to drift from
        if payload_by_path is not None and rel in payload_by_path:
            after = payload_by_path[rel]
        else:
            full = os.path.join(repo_root, rel)
            try:
                with open(full, encoding="utf-8") as fh:
                    after = json.load(fh)
            except (OSError, json.JSONDecodeError):
                continue
        n += 1
        all_deltas = compare(before, after,
                             floor=0.0 if strict_floor else MACHINE_FLOOR)
        deltas = significant(all_deltas)
        below = [d for d in all_deltas if d.kind == "floor"]
        if deltas:
            head = "; ".join(str(d).strip() for d in deltas[:3])
            lines.append(f"{rel}: {len(deltas)} delta(s) — {head}")
        if below:
            floor_lines.append(f"{rel}: {len(below)} sub-floor delta(s) "
                               f"(<1e-12, both sides) — noise, not drift")
    return lines, n, floor_lines


# ---------------------------------------------------------------------------
# subprocess helpers
# ---------------------------------------------------------------------------
def _child_env(repo_root: str) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [os.path.join(repo_root, "src"),
         env.get("PYTHONPATH", "")]).strip(os.pathsep)
    env["MPLBACKEND"] = "Agg"
    env.setdefault("CASIM_TEST_REGISTRY", "1")
    return env


def _mtime(path: str) -> float:
    try:
        return os.path.getmtime(path)
    except OSError:
        return -1.0


def _pytest_available() -> bool:
    return subprocess.run([sys.executable, "-c", "import pytest"],
                          capture_output=True).returncode == 0


def _run_pytest_file(rel_path: str, repo_root: str,
                     timeout: float) -> tuple[str, str, dict]:
    """Delegate one file to pytest; status from the JUnit XML, never stdout."""
    tmp = tempfile.mkdtemp(prefix="casim_reg_")
    xml = os.path.join(tmp, "j.xml")
    cmd = [sys.executable, "-m", "pytest", rel_path, "-q", "--no-header",
           "--tb=line", f"--junit-xml={xml}", "-p", "no:cacheprovider",
           "-m", "not superseded and not slow"]
    try:
        proc = subprocess.run(cmd, cwd=repo_root, env=_child_env(repo_root),
                              capture_output=True, text=True, timeout=timeout)
        from casim.suite.runner import _parse_junit
        passed, failed, errors, skipped = _parse_junit(xml)
        metrics = {"passed": passed, "failed": failed, "errors": errors,
                   "skipped": skipped}
        if passed + failed + errors + skipped == 0:
            if proc.returncode == 5:
                return "SKIP", "pytest collected nothing from this file", metrics
            tail = (proc.stdout or proc.stderr or "").strip().splitlines()
            return "ERROR", f"pytest rc={proc.returncode}: " \
                            f"{tail[-1] if tail else 'no output'}", metrics
        if failed or errors:
            tail = [ln for ln in (proc.stdout or "").splitlines()
                    if "assert" in ln.lower() or "Error" in ln]
            return "FAIL", f"{failed} failed, {errors} errors" + (
                f" — {tail[0][:120]}" if tail else ""), metrics
        return "PASS", f"{passed} passed" + (f", {skipped} skipped"
                                             if skipped else ""), metrics
    except subprocess.TimeoutExpired:
        return "ERROR", f"pytest timed out after {timeout:.0f}s", {}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _run_script(rel_path: str, repo_root: str,
                timeout: float) -> tuple[int, str]:
    try:
        proc = subprocess.run([sys.executable, rel_path], cwd=repo_root,
                              env=_child_env(repo_root), capture_output=True,
                              text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout:.0f}s"
    tail = ((proc.stdout or "") + (proc.stderr or "")).strip().splitlines()
    return proc.returncode, (tail[-1][:200] if tail else "")


# ---------------------------------------------------------------------------
# the four kinds
# ---------------------------------------------------------------------------
def _run_assertion(rec: treg.TestRecord, repo_root: str, timeout: float,
                   swept: bool) -> RunResult:
    if rec.entry:
        t0 = time.time()
        try:
            fn = _load_callable(rec)
            value = _call(fn, rec.params)
        except AssertionError as exc:
            return RunResult(rec.id, rec.kind, "FAIL", time.time() - t0,
                             f"AssertionError: {exc}"[:300])
        except Exception as exc:                       # noqa: BLE001
            tb = traceback.format_exc().strip().splitlines()
            return RunResult(rec.id, rec.kind, "ERROR", time.time() - t0,
                             f"{type(exc).__name__}: {exc} | "
                             f"{tb[-1] if tb else ''}"[:300])
        ok, detail, metrics = _interpret_return(value)
        status = "SWEEP" if swept else ("PASS" if ok else "FAIL")
        return RunResult(rec.id, rec.kind, status, time.time() - t0, detail,
                         metrics)
    # Delegate: the file's own pytest functions are the entry point.
    if not rec.path:
        return RunResult(rec.id, rec.kind, "ERROR", 0.0,
                         "assertion record with neither `entry:` nor `path:`")
    t0 = time.time()
    if _pytest_available():
        status, detail, metrics = _run_pytest_file(rec.path, repo_root, timeout)
        return RunResult(rec.id, rec.kind, status, time.time() - t0, detail,
                         metrics)
    rc, tail = _run_script(rec.path, repo_root, timeout)
    if rc == 0:
        return RunResult(rec.id, rec.kind, "PASS", time.time() - t0,
                         "pytest absent; __main__ exited 0 (reduced check)")
    return RunResult(rec.id, rec.kind, "FAIL" if rc == 1 else "ERROR",
                     time.time() - t0, f"exit {rc}: {tail}")


def _run_result_dump(rec: treg.TestRecord, repo_root: str, timeout: float,
                     swept: bool, sweep_dir: str | None) -> RunResult:
    """Emit numbers, then diff them against the committed baseline."""
    t0 = time.time()
    strict = bool(rec.expect.get("strict_floor"))

    if rec.entry:
        try:
            fn = _load_callable(rec)
            payload = _call(fn, rec.params)
        except Exception as exc:                       # noqa: BLE001
            tb = traceback.format_exc().strip().splitlines()
            return RunResult(rec.id, rec.kind, "ERROR", time.time() - t0,
                             f"{type(exc).__name__}: {exc} | "
                             f"{tb[-1] if tb else ''}"[:300])
        if not isinstance(payload, dict):
            return RunResult(rec.id, rec.kind, "ERROR", time.time() - t0,
                             f"kind=result_dump entry returned "
                             f"{type(payload).__name__}, not a dict")
        target = rec.results[0] if rec.results else None
        if target is None:
            return RunResult(rec.id, rec.kind, "ERROR", time.time() - t0,
                             "kind=result_dump needs a `results:` path to write")
        if swept:
            # Rule 1: a sweep never writes a baseline.
            out_dir = sweep_dir or tempfile.mkdtemp(prefix="casim_sweep_")
            os.makedirs(out_dir, exist_ok=True)
            side = os.path.join(out_dir, os.path.basename(target))
            with open(side, "w", encoding="utf-8") as fh:
                json.dump(_jsonable(payload), fh, indent=2, default=str)
            lines, n, floor = _diff_against_head(
                [target], repo_root, {target: _jsonable(payload)}, strict)
            return RunResult(rec.id, rec.kind, "SWEEP", time.time() - t0,
                             (f"{len(lines)} drifted artifact(s) vs HEAD"
                              if lines else "no drift vs HEAD"),
                             {"compared": n, "drift": lines, "floor": floor,
                              "written": os.path.relpath(side, repo_root)
                              if side.startswith(repo_root) else side})
        full = os.path.join(repo_root, target)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            json.dump(_jsonable(payload), fh, indent=2, default=str)
        lines, n, floor = _diff_against_head(list(rec.results), repo_root,
                                             strict_floor=strict)
    else:
        if swept:
            return RunResult(rec.id, rec.kind, "SKIP", 0.0,
                             "cannot inject --param into a path-only record; "
                             "give it a `module:`/`entry:` first (C7.4)")
        if not rec.path:
            return RunResult(rec.id, rec.kind, "ERROR", 0.0,
                             "result_dump record with neither entry nor path")
        # Mtime guard. Without it a script that never touches its declared
        # artifact still "reproduces HEAD exactly" — the working-tree copy is
        # simply the committed one, unchanged — and that reads as a pass while
        # testing nothing. Only artifacts this run actually rewrote are diffed.
        before = {r: _mtime(os.path.join(repo_root, r)) for r in rec.results}
        rc, tail = _run_script(rec.path, repo_root, timeout)
        if rc != 0:
            return RunResult(rec.id, rec.kind, "ERROR", time.time() - t0,
                             f"exit {rc}: {tail}")
        rewritten = [r for r in rec.results
                     if _mtime(os.path.join(repo_root, r)) > before[r]]
        if not rewritten:
            return RunResult(rec.id, rec.kind, "SKIP", time.time() - t0,
                             "the run did not rewrite any declared baseline — "
                             "nothing was actually compared (fix `results:` or "
                             "give the record an `entry:`)",
                             {"declared": list(rec.results)})
        lines, n, floor = _diff_against_head(rewritten, repo_root,
                                             strict_floor=strict)

    secs = time.time() - t0
    if not rec.results:
        return RunResult(rec.id, rec.kind, "SKIP", secs,
                         "no `results:` baseline declared")
    if n == 0:
        return RunResult(rec.id, rec.kind, "SKIP", secs,
                         "declared baselines are untracked at HEAD — nothing to "
                         "diff against yet (commit them to arm this record)")
    if lines:
        # Ledger-declared supersession (2026-07-31). A baseline the ledger marks
        # `stale_by_design` is EXPECTED to differ, so the verdict is STALE — but
        # only if EVERY drifted artifact is declared, otherwise the undeclared one
        # is still a real failure and must stay red.
        from . import ledger as _led
        drifted_paths = [ln.split(":", 1)[0] for ln in lines]
        if _led.all_stale(drifted_paths, repo_root):
            b = _led.status_of(drifted_paths[0], repo_root)
            return RunResult(rec.id, rec.kind, "STALE", secs,
                             f"baseline predates {b.record} "
                             f"(stale_by_design) — {lines[0][:150]}",
                             {"compared": n, "drift": lines, "floor": floor,
                              "ledger_record": b.record,
                              "clears_by": b.clears_by})
        return RunResult(rec.id, rec.kind, "FAIL", secs,
                         f"result drift vs HEAD — {lines[0][:200]}",
                         {"compared": n, "drift": lines, "floor": floor})
    detail = f"{n} artifact(s) reproduced HEAD"
    detail += (f"; {len(floor)} sub-floor delta(s) below 1e-12 (noise)"
               if floor else " exactly")
    return RunResult(rec.id, rec.kind, "PASS", secs, detail,
                     {"compared": n, "floor": floor})


def _run_scenario(rec: treg.TestRecord, repo_root: str,
                  timeout: float, swept: bool) -> RunResult:
    t0 = time.time()
    try:
        from casim.io import load_scenario
        from casim.engine import Simulation
        from casim import analysis
        sc = load_scenario(os.path.join(repo_root, rec.scenario or ""))
        for key in ("ticks", "seed"):
            if key in rec.params:
                sc[key] = rec.params[key]
        if "L" in rec.params:
            sc.setdefault("lattice", {})["L"] = rec.params["L"]
        sc.pop("output", None)                  # never clobber a committed JSON
        sim = Simulation.from_scenario(sc)
        results = sim.run(int(sc.get("ticks", 0)))
        rows = analysis.exactness_rows(results)
        gated = [r for r in rows if r["tol"] is not None]
        gates_spec = rec.expect.get("gates")
        want = set() if gates_spec in (None, "all") else set(gates_spec or ())
        if want:
            gated = [r for r in gated if r["observer"] in want]
        fails = [r for r in gated if not r["pass"]]
        tol = rec.tol
        if tol is not None:
            fails = [r for r in gated
                     if r["value"] is not None and float(r["value"]) > tol]
        secs = time.time() - t0
        metrics = {"gated": len(gated),
                   "worst": max((float(r["value"]) for r in gated
                                 if r["value"] is not None), default=0.0)}
        if swept:
            return RunResult(rec.id, rec.kind, "SWEEP", secs,
                             f"{len(fails)} of {len(gated)} gated observables "
                             f"outside tolerance at the swept value", metrics)
        if not gated:
            return RunResult(rec.id, rec.kind, "SKIP", secs,
                             "no gated observable in this scenario", metrics)
        if fails:
            worst = max(fails, key=lambda r: float(r["value"] or 0.0))
            return RunResult(rec.id, rec.kind, "FAIL", secs,
                             f"{len(fails)} gated obs over tol (worst "
                             f"{worst['observer']}={worst['value']:.2e})", metrics)
        return RunResult(rec.id, rec.kind, "PASS", secs,
                         f"{len(gated)} gated observable(s) within tolerance",
                         metrics)
    except Exception as exc:                           # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return RunResult(rec.id, rec.kind, "ERROR", time.time() - t0,
                         f"{type(exc).__name__}: {exc} | "
                         f"{tb[-1] if tb else ''}"[:300])


def _run_legacy(rec: treg.TestRecord, repo_root: str,
                timeout: float) -> RunResult:
    t0 = time.time()
    if not rec.path:
        return RunResult(rec.id, rec.kind, "ERROR", 0.0,
                         "legacy_script record with no `path:`")
    rc, tail = _run_script(rec.path, repo_root, timeout)
    secs = time.time() - t0
    if rc == 0:
        return RunResult(rec.id, rec.kind, "DEBT", secs,
                         "exit 0, no declared failure mode — this record is "
                         "debt, not a pass (C7 ratchet)")
    return RunResult(rec.id, rec.kind, "ERROR", secs, f"exit {rc}: {tail}")


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------
def run_record(rec: treg.TestRecord, repo_root: str | None = None,
               overrides: dict[str, Any] | None = None,
               timeout: float | None = None,
               sweep_dir: str | None = None) -> RunResult:
    """Run one registry record. `overrides` makes it a sweep (C7.2 `--param`)."""
    repo_root = repo_root or _REPO
    swept = bool(overrides)
    if swept:
        rec = treg.with_params(rec, overrides or {})
    if rec.tier == "archive":
        return RunResult(rec.id, rec.kind, "SKIP", 0.0,
                         f"archive tier (superseded_by "
                         f"{rec.superseded_by or 'ledger'})")
    limit = timeout or rec.timeout or (
        GATE_TIMEOUT if rec.tier == "gate" else DEFAULT_TIMEOUT)

    if rec.kind == "assertion":
        res = _run_assertion(rec, repo_root, limit, swept)
    elif rec.kind == "result_dump":
        res = _run_result_dump(rec, repo_root, limit, swept, sweep_dir)
    elif rec.kind == "scenario":
        res = _run_scenario(rec, repo_root, limit, swept)
    elif rec.kind == "legacy_script":
        if swept:
            return RunResult(rec.id, rec.kind, "SKIP", 0.0,
                             "legacy_script takes no parameters; migrate it to "
                             "an `entry:` first (C7.4)")
        res = _run_legacy(rec, repo_root, limit)
    else:
        res = RunResult(rec.id, rec.kind, "ERROR", 0.0,
                        f"unknown kind {rec.kind!r}")
    if swept:
        res.swept = _jsonable(dict(overrides or {}))
    return res


def run_selection(records: Iterable[treg.TestRecord],
                  repo_root: str | None = None,
                  overrides: dict[str, Any] | None = None,
                  timeout: float | None = None,
                  on_result: Callable[[RunResult], None] | None = None,
                  out_dir: str | None = None) -> dict[str, Any]:
    """Run a selection and return a report dict (also written if `out_dir`)."""
    repo_root = repo_root or _REPO
    recs = list(records)
    t0 = time.time()
    sweep_dir = None
    if overrides and out_dir:
        sweep_dir = os.path.join(out_dir, "sweep")
    results: list[RunResult] = []
    for rec in recs:
        res = run_record(rec, repo_root, overrides, timeout, sweep_dir)
        results.append(res)
        if on_result:
            on_result(res)
    counts: dict[str, int] = {}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    report = {
        "generated": time.strftime("%Y-%m-%d - %H:%M"),
        "elapsed_s": round(time.time() - t0, 2),
        "n": len(results),
        "counts": counts,
        "overrides": _jsonable(dict(overrides or {})),
        "failed": [r.id for r in results if not r.ok],
        "items": [asdict(r) for r in results],
    }
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "test_registry_report.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, default=str)
    return report


def format_report(report: dict[str, Any]) -> str:
    c = report["counts"]
    order = [s for s in STATUSES if s in c]
    head = "  ".join(f"{s}: {c[s]}" for s in order)
    lines = [f"\n{report['n']} record(s), {report['elapsed_s']:.1f}s   {head}"]
    if report["failed"]:
        lines.append("\nnot ok:")
        by_id = {i["id"]: i for i in report["items"]}
        for rid in report["failed"]:
            it = by_id[rid]
            lines.append(f"  {it['status']:6s} {rid}  — {it['detail'][:110]}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Negative controls — gap #3 of docs/status/completeness-2026-08-07.md, row H2.
#
# The report's smallest next step, verbatim: "Make a declared-and-verified
# perturbation a D9 requirement for `kind: assertion` records, retro-fitted to
# the 58 gate-tier records rather than all 400."
#
# What is being closed is narrow and specific. `check_test_registry` already
# refuses a record with no *declared* failure mode. Nothing checked whether the
# declared one can actually trip — and the repo has one worked example of the
# difference: F22's headline verification was `x - (1 - 2(1-x)/2)`, identically
# zero for any expression at all, which returned residual 0 from a deliberately
# wrong rho and then from rho = 42. It was green for months. Everything below
# exists to make that class of green impossible to hold.
# ---------------------------------------------------------------------------
_LEG_ID_KEYS = ("id", "name", "key", "leg", "label", "check")
_LEG_OK_KEYS = ("pass", "passed", "ok", "gate", "holds")


def leg_map(payload: Any) -> dict[str, bool]:
    """``{leg id -> passed}`` from an entry point's return value.

    Three shapes are in use in this repo and all three are read, because the
    alternative is a checker that quietly sees no legs and reports the record
    sound on the strength of its overall verdict:

      * ``{"checks": [{"id": "G10-3", "pass": True}, ...]}``  (F300, F298, F299)
      * ``{"checks": {"symbolic_identity": True, ...}}``       (F22)
      * a flat payload with no ``checks`` at all -> ``{}``, and the caller falls
        back to the overall verdict.
    """
    if not isinstance(payload, dict):
        return {}
    checks = payload.get("checks")
    out: dict[str, bool] = {}
    if isinstance(checks, dict):
        for k, v in checks.items():
            if isinstance(v, bool):
                out[str(k)] = v
            elif isinstance(v, dict):
                for ok_key in _LEG_OK_KEYS:
                    if isinstance(v.get(ok_key), bool):
                        out[str(k)] = v[ok_key]
                        break
    elif isinstance(checks, (list, tuple)):
        for i, c in enumerate(checks):
            if not isinstance(c, dict):
                continue
            lid = next((str(c[k]) for k in _LEG_ID_KEYS if c.get(k) is not None),
                       f"#{i}")
            ok = next((c[k] for k in _LEG_OK_KEYS
                       if isinstance(c.get(k), bool)), None)
            if ok is not None:
                out[lid] = bool(ok)
    return out


def resolve_leg(declared: str, legs: dict[str, bool]) -> tuple[str | None, str]:
    """Match a declared leg tag against the payload's leg keys.

    Half these drivers emit the tag and its description as one string —
    ``"L2 the C7 identity exists ONLY for N <= 3"`` — so requiring an exact key
    would mean pasting a sentence into the registry and re-pasting it whenever the
    wording changed. A control block names the tag the finding already uses in
    prose (``L2``, ``G10-3``, ``M1a``) and it is resolved here.

    The boundary is deliberate rather than a prefix test: ``S4`` must not match
    ``S4b``, which is a different leg in F299 and one that its second control
    declares on its own. An ambiguous tag is reported, never guessed — silently
    picking one of two legs would be a checker inventing the thing it audits.
    """
    if declared in legs:
        return declared, ""
    hits = [k for k in legs
            if k.startswith(declared)
            and (len(k) == len(declared) or not (k[len(declared)].isalnum()
                                                 or k[len(declared)] in "_-."))]
    if len(hits) == 1:
        return hits[0], ""
    if len(hits) > 1:
        return None, (f"leg tag {declared!r} is ambiguous — it matches "
                      f"{len(hits)}: {sorted(hits)[:4]}")
    return None, ""


def _overall(payload: Any) -> bool | None:
    """The record's own verdict, if it states one."""
    if isinstance(payload, dict):
        for key in ("all_pass", "passed", "pass", "ok", "gate"):
            if isinstance(payload.get(key), bool):
                return payload[key]
    if isinstance(payload, bool):
        return payload
    return None


def _sha(path: str) -> str:
    import hashlib
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()[:16]
    except OSError:
        return "missing"


def record_fingerprint(rec: treg.TestRecord, repo_root: str | None = None) -> str:
    """A hash over everything a control verdict depends on.

    This is what lets `make gate` stay fast and still have teeth. Verifying a
    control costs a baseline run plus one perturbed run per control — far past a
    two-minute barrier at 55 records. So the verdicts are journalled, and the
    gate checks the journal against this fingerprint instead of re-running.
    Change the physics module, the test file, the params or the control block and
    the fingerprint moves, the journal entry goes stale, and the gate says so.

    It is the `result_dump` contract applied one level up: a `result_dump` record
    is armed by committing its baseline, and a control is armed by committing a
    verdict that names the code it was measured against.
    """
    import hashlib
    repo_root = repo_root or _REPO
    parts = [rec.id, rec.kind, rec.tier, str(rec.entry), str(rec.module),
             json.dumps(_jsonable(dict(rec.params)), sort_keys=True),
             json.dumps(_jsonable([dict(c) for c in rec.control]),
                        sort_keys=True, default=str)]
    if rec.path:
        parts.append(_sha(os.path.join(repo_root, rec.path)))
    if rec.module:
        try:
            mod = importlib.import_module(rec.module)
            src = getattr(mod, "__file__", None)
            parts.append(_sha(src) if src else "nofile")
        except Exception:                                  # noqa: BLE001
            parts.append("unimportable")
    # This file too. A verdict is only as good as the machinery that reached it,
    # and the first re-run of this pass replayed four stale INVALIDs from the
    # journal *because the checker had been fixed and the fingerprint had not
    # noticed* — which is the same class of defect the whole layer exists to
    # catch, one level up again. Editing the runner therefore invalidates every
    # banked verdict, which is the conservative direction.
    parts.append(_sha(os.path.abspath(__file__).replace(".pyc", ".py")))
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


_GUARD_LINE_CACHE: dict[str, frozenset[int] | None] = {}


def _guard_lines(path: str) -> frozenset[int] | None:
    """Line numbers of every ``assert``/``raise`` in one file, or None."""
    if path in _GUARD_LINE_CACHE:
        return _GUARD_LINE_CACHE[path]
    result: frozenset[int] | None = None
    try:
        import ast as _ast
        with open(path, encoding="utf-8", errors="replace") as fh:
            tree = _ast.parse(fh.read(), filename=path)
        result = frozenset(n.lineno for n in _ast.walk(tree)
                           if isinstance(n, (_ast.Assert, _ast.Raise)))
    except (OSError, SyntaxError, ValueError):
        result = None
    _GUARD_LINE_CACHE[path] = result
    return result


def _record_own_files(rec: treg.TestRecord, repo_root: str) -> dict[str, frozenset[int]]:
    """{file -> guard lines} for the record's OWN file and module file only.

    Scope, and it is a correctness decision as much as a speed one. A first cut
    traced every file under the repo, which is unusable — a heavy record calls
    into engine code inside inner loops and the tracer never finished. Narrowing
    it here is also the right question: "can THIS record fail?" is about the
    guards the record owns. A guard deep in a shared kernel fires for reasons that
    have nothing to do with what this record asserts, and counting it would let a
    record inherit a failure mode it never wrote.

    Consequence to keep in mind: a record whose entry is a thin wrapper delegating
    all its asserts to another module reads as cannot-fail here. That is a real
    property worth seeing, not a false positive — the record does not own a
    failure mode, its callee does.
    """
    out: dict[str, frozenset[int]] = {}
    cands: list[str] = []
    if rec.path:
        cands.append(os.path.join(repo_root, rec.path))
    if rec.module:
        try:
            mod = importlib.import_module(rec.module)
            src = getattr(mod, "__file__", None)
            if src:
                cands.append(src)
        except Exception:                                  # noqa: BLE001
            pass
    for c in cands:
        real = os.path.realpath(c)
        gl = _guard_lines(real)
        if gl is not None:
            out[real] = gl
    return out


def probe_can_fail(rec: treg.TestRecord, repo_root: str | None = None,
                   timeout: float | None = None) -> dict[str, Any]:
    """Run the record's entry and report whether a guard actually EXECUTED.

    The empirical answer to "can this check fail?", and it exists because the
    static answer was wrong. `check_finding_records.py` walked the call graph from
    the entry through `ast.Call` nodes; three records dispatch through a
    module-level table —

        for name, fn in CHECKS:      # the only Call node is on a loop variable
            out[name] = fn()

    — so the walk returned zero reachable guards for files holding 41, 39 and 30
    of them, and the 2026-08-07 report concluded that A1's evidence was
    "unfalsifiable in the mechanical sense". It was not. Any static reachability
    analysis loses to indirection: dispatch tables, ``getattr``, decorators,
    registries of callables, ``functools.partial``.

    Execution does not. This traces one real run and asks which ``assert``/
    ``raise`` lines the interpreter actually reached, which is both stricter and
    laxer than the AST in the right directions:

      * an ``assert`` behind a branch nothing takes is **dead**, and the AST
        counts it as reachable;
      * an ``assert`` reached through a dispatch table is **live**, and the AST
        counts it as absent.

    Returns ``{can_fail, guards_executed, guard_lines_total, status, seconds,
    …}``. ``guards_executed`` stops counting at the first hit — one executed
    guard is the whole question, and continuing to trace after that is a tax on
    the healthy case.
    """
    repo_root = repo_root or _REPO
    t0 = time.time()
    files = _record_own_files(rec, repo_root)
    total = sum(len(v) for v in files.values())
    limit = timeout or 120.0

    found: list[tuple[str, int]] = []
    timed_out: list[bool] = []

    def tracer(frame, event, arg):                         # noqa: ANN001
        if found or timed_out:
            return None
        if event == "call":
            return tracer if os.path.realpath(
                frame.f_code.co_filename) in files else None
        if event == "line":
            gl = files.get(os.path.realpath(frame.f_code.co_filename))
            if gl and frame.f_lineno in gl:
                found.append((frame.f_code.co_filename, frame.f_lineno))
                return None
            if time.time() - t0 > limit:
                timed_out.append(True)
                return None
        return tracer

    status, detail = "PASS", ""
    verdict_route = False
    prior = sys.gettrace()
    try:
        fn = _load_callable(rec)
        if not files:
            return {"id": rec.id, "can_fail": None,
                    "verdict": "INCONCLUSIVE",
                    "guards_executed": 0, "guard_lines_total": 0,
                    "status": "SKIP",
                    "detail": "no own file to trace (no `path:` and no importable "
                              "`module:`)",
                    "seconds": round(time.time() - t0, 2),
                    "fingerprint": record_fingerprint(rec, repo_root)}
        sys.settrace(tracer)
        try:
            value = _call(fn, rec.params)
        finally:
            sys.settrace(prior)
        ok, detail, _ = _interpret_return(value)
        status = "PASS" if ok else "FAIL"
        # THE SECOND ROUTE. `_interpret_return` scores a run FAIL either because
        # something raised or because the payload carries its own verdict key
        # (`all_pass`/`passed`/`pass`/`ok`/`gate`). A leg-based driver like F300
        # asserts nothing and returns `all_pass`; tracing alone called it
        # cannot-fail, which is as wrong as the AST walk was and in the mirror
        # direction. The question is "has the harness ANY way to score this FAIL",
        # and there are exactly two.
        if _overall(value) is not None:
            verdict_route = True
        else:
            verdict_route = False
    except AssertionError as exc:
        # An AssertionError IS the answer, whether or not the tracer saw the line.
        found.append(("<raised>", 0))
        status, detail = "FAIL", f"AssertionError: {exc}"[:200]
    except Exception as exc:                               # noqa: BLE001
        status, detail = "ERROR", f"{type(exc).__name__}: {exc}"[:200]
    finally:
        sys.settrace(prior)

    # A timeout is NOT evidence of anything, and must never be recorded as
    # cannot-fail. That conflation is how the defect this tool replaces got into
    # a status report in the first place: an absence of evidence written down as
    # evidence of absence.
    if found or verdict_route:
        verdict, can = "CAN_FAIL", True
    elif timed_out:
        verdict, can = "INCONCLUSIVE", None
        detail = (f"tracing exceeded {limit:.0f}s with no guard reached — "
                  f"inconclusive, NOT cannot-fail. Re-run with a longer "
                  f"--timeout, or read the record by hand.")
    else:
        verdict, can = "CANNOT_FAIL", False

    return {
        "id": rec.id,
        "can_fail": can,
        "verdict": verdict,
        "guards_executed": len(found),
        "guard_line_hit": (f"{os.path.relpath(found[0][0], repo_root)}"
                           f":{found[0][1]}") if found and found[0][0] != "<raised>"
        else ("<AssertionError raised>" if found else None),
        "guard_lines_total": total,
        "route": ("guard" if found else ("verdict_key" if verdict_route else None)),
        "traced_files": [os.path.relpath(f, repo_root) for f in files],
        "status": status,
        "detail": detail,
        "seconds": round(time.time() - t0, 2),
        "fingerprint": record_fingerprint(rec, repo_root),
    }


def _entry_payload(rec: treg.TestRecord, overrides: dict[str, Any] | None
                   ) -> tuple[str, Any, str]:
    """``(status, payload, detail)`` for one entry-point call.

    Unlike :func:`_run_assertion` this hands back the payload, because a leg map
    is the whole point: "the perturbation reddens L2 and L3" is a claim about
    legs and cannot be judged from a single boolean.
    """
    r = treg.with_params(rec, overrides or {})
    try:
        fn = _load_callable(r)
        value = _call(fn, r.params)
    except AssertionError as exc:
        return "FAIL", None, f"AssertionError: {exc}"[:300]
    except Exception as exc:                               # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return "ERROR", None, (f"{type(exc).__name__}: {exc} | "
                               f"{tb[-1] if tb else ''}")[:300]
    ok, detail, _ = _interpret_return(value)
    return ("PASS" if ok else "FAIL"), value, detail


def _accepts_param(rec: treg.TestRecord, key: str) -> bool | None:
    """Does the entry point actually take this keyword? ``None`` if unknowable.

    ``_call`` drops keywords a signature does not accept, on purpose — a record
    may carry a param for documentation. That kindness is a hazard here: an
    override the entry point ignores is a perturbation that perturbs nothing, and
    the record would stay green and be scored a LEAK, blaming the physics for a
    typo in the control. Naming the real cause is cheap, so it is named.
    """
    import inspect
    try:
        fn = _load_callable(rec)
        sig = inspect.signature(fn)
    except Exception:                                      # noqa: BLE001
        return None
    if any(p.kind is inspect.Parameter.VAR_KEYWORD
           for p in sig.parameters.values()):
        return True
    return key in sig.parameters


def _run_pytest_k(rel_path: str, k: str, repo_root: str,
                  timeout: float) -> tuple[str, str, dict]:
    """Run one named pytest function. Status from JUnit XML, never stdout."""
    tmp = tempfile.mkdtemp(prefix="casim_ctl_")
    xml = os.path.join(tmp, "j.xml")
    cmd = [sys.executable, "-m", "pytest", rel_path, "-q", "--no-header",
           "--tb=line", f"--junit-xml={xml}", "-p", "no:cacheprovider",
           "-k", k, "-m", "not superseded and not slow"]
    try:
        proc = subprocess.run(cmd, cwd=repo_root, env=_child_env(repo_root),
                              capture_output=True, text=True, timeout=timeout)
        from casim.suite.runner import _parse_junit
        passed, failed, errors, skipped = _parse_junit(xml)
        metrics = {"passed": passed, "failed": failed, "errors": errors,
                   "skipped": skipped}
        if passed + failed + errors == 0:
            return "INVALID", (f"pytest collected no test matching "
                               f"-k {k!r} in {rel_path} (rc={proc.returncode})"
                               ), metrics
        if failed or errors:
            return "INVALID", (f"the named negative control is itself red "
                               f"({failed} failed, {errors} errors) — it cannot "
                               f"witness anything until it passes"), metrics
        return "CONTROL", f"{passed} negative-control test(s) passed", metrics
    except subprocess.TimeoutExpired:
        return "INVALID", f"pytest timed out after {timeout:.0f}s", {}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_control(rec: treg.TestRecord, repo_root: str | None = None,
                timeout: float | None = None,
                baseline: tuple[str, Any] | None = None) -> list[RunResult]:
    """Verify every control this record declares. One RunResult per control.

    Pass ``baseline`` to reuse an unperturbed run across several controls on the
    same record — four controls on F304 would otherwise pay for five runs of the
    same driver instead of five total.
    """
    repo_root = repo_root or _REPO
    limit = timeout or rec.timeout or (
        GATE_TIMEOUT if rec.tier == "gate" else DEFAULT_TIMEOUT)
    fp = record_fingerprint(rec, repo_root)

    if not rec.control:
        return [RunResult(rec.id, rec.kind, "NOCTRL", 0.0,
                          "no `control:` declared — this record asserts, and "
                          "nothing shows it can fail (D9/H2 debt)",
                          {"fingerprint": fp})]

    out: list[RunResult] = []
    base_status = base_payload = None
    base_legs: dict[str, bool] = {}

    for i, ctl in enumerate(rec.control):
        t0 = time.time()
        tag = f"{rec.id}#control{i}"
        reason = str(ctl.get("reason") or "").strip()
        params = ctl.get("params") or {}
        meta = {"fingerprint": fp, "control_index": i, "reason": reason,
                "params": _jsonable(dict(params)),
                "reds": list(ctl.get("reds") or ()),
                "strength": "strong" if params else "weak"}

        # -- weak form: an in-file pytest function that IS the control --------
        if not params:
            name = str(ctl.get("test") or "")
            if not rec.path:
                out.append(RunResult(tag, rec.kind, "INVALID", 0.0,
                                     "`test:` control on a record with no "
                                     "`path:` to collect it from", meta))
                continue
            if not _pytest_available():
                out.append(RunResult(tag, rec.kind, "SKIP", 0.0,
                                     "pytest absent; cannot run the named "
                                     "negative control", meta))
                continue
            status, detail, m = _run_pytest_k(rec.path, name, repo_root, limit)
            meta.update(m)
            out.append(RunResult(tag, rec.kind, status, time.time() - t0,
                                 detail, meta))
            continue

        # -- strong form: the harness applies the perturbation itself ---------
        if not rec.entry:
            out.append(RunResult(tag, rec.kind, "INVALID", 0.0,
                                 "`params:` control needs an `entry:` — the "
                                 "runner cannot inject into a path-only record "
                                 "(C7.4)", meta))
            continue
        unaccepted = [k for k in params if _accepts_param(rec, k) is False]
        if unaccepted:
            out.append(RunResult(
                tag, rec.kind, "INVALID", time.time() - t0,
                f"{rec.entry}() does not take {unaccepted} — the override would "
                f"be dropped and the 'perturbed' run would be the unperturbed "
                f"one", meta))
            continue

        if base_status is None:
            b0 = time.time()
            base_status, base_payload, base_detail = _entry_payload(rec, None)
            base_legs = leg_map(base_payload)
            meta["baseline_seconds"] = round(time.time() - b0, 2)
            if base_status != "PASS":
                out.append(RunResult(
                    tag, rec.kind, "INVALID", time.time() - t0,
                    f"the record is {base_status} BEFORE the perturbation "
                    f"({base_detail[:120]}) — a control cannot be read off a "
                    f"run that is already red", meta))
                continue
        meta["baseline_legs"] = len(base_legs)

        p_status, p_payload, p_detail = _entry_payload(rec, dict(params))
        p_legs = leg_map(p_payload)
        want_red = [str(x) for x in (ctl.get("reds") or ())]
        only = bool(ctl.get("only", True))
        secs = time.time() - t0

        if p_status == "ERROR":
            out.append(RunResult(
                tag, rec.kind, "INVALID", secs,
                f"the perturbed run CRASHED rather than failing its checks "
                f"({p_detail[:140]}) — an exception is not a negative control; "
                f"it shows the driver cannot reach the perturbed point",
                meta))
            continue

        # No named legs: the weaker, still-real claim that the verdict flips.
        if not want_red:
            if p_status == "FAIL":
                out.append(RunResult(tag, rec.kind, "CONTROL", secs,
                                     "verdict flipped PASS -> FAIL under the "
                                     "perturbation (no legs named)", meta))
            else:
                out.append(RunResult(
                    tag, rec.kind, "LEAK", secs,
                    "the perturbation was applied and the record stayed GREEN — "
                    "whatever it asserts, it does not assert it against this",
                    meta))
            continue

        resolved: list[str] = []
        missing: list[str] = []
        ambiguous: list[str] = []
        for lg in want_red:
            hit, why = resolve_leg(lg, p_legs)
            if hit is None:
                (ambiguous if why else missing).append(why or lg)
            else:
                resolved.append(hit)
        if ambiguous:
            out.append(RunResult(tag, rec.kind, "INVALID", secs,
                                 "; ".join(ambiguous), meta))
            continue
        if missing:
            shown = [k.split()[0] if " " in k else k for k in sorted(p_legs)]
            out.append(RunResult(
                tag, rec.kind, "INVALID", secs,
                f"declared leg(s) {missing} do not exist in the payload; legs "
                f"present: {shown[:12]}{'...' if len(shown) > 12 else ''}"
                f" — a control naming a leg the driver no longer emits has "
                f"silently stopped testing anything", meta))
            continue
        want_red = resolved
        meta["reds_resolved"] = resolved
        already = [lg for lg in want_red if base_legs.get(lg) is False]
        if already:
            out.append(RunResult(
                tag, rec.kind, "INVALID", secs,
                f"leg(s) {already} are red WITHOUT the perturbation, so their "
                f"redness is not evidence about it", meta))
            continue

        still_green = [_tag(lg) for lg in want_red
                       if p_legs.get(lg) is not False]
        spilled = sorted(_tag(lg) for lg, ok in p_legs.items()
                         if ok is False and lg not in want_red
                         and base_legs.get(lg) is not False)
        meta.update({"legs_total": len(p_legs), "reddened": len(want_red),
                     "spilled": spilled})

        if still_green:
            out.append(RunResult(
                tag, rec.kind, "LEAK", secs,
                f"leg(s) {still_green} stayed GREEN under `{_fmt(params)}` — "
                f"declared as the thing this control reddens. {reason[:90]}",
                meta))
        elif spilled and only:
            out.append(RunResult(
                tag, rec.kind, "SPILL", secs,
                f"reddened {len(spilled)} undeclared leg(s) {spilled[:6]} as "
                f"well — 'and only where declared' is part of the contract, "
                f"because a perturbation that breaks everything is a broken run "
                f"and is also the cheapest way to fake a red. Widen `reds:` if "
                f"they belong, or set `only: false` and say why in `reason:`",
                meta))
        else:
            out.append(RunResult(
                tag, rec.kind, "CONTROL", secs,
                f"`{_fmt(params)}` reddens exactly "
                f"{[_tag(x) for x in want_red]} of {len(p_legs)} leg(s)"
                + (f"; {len(spilled)} other(s) also red, allowed by "
                   f"`only: false`" if spilled else ""), meta))
    return out


def _fmt(params: dict[str, Any]) -> str:
    return " ".join(f"--param {k}={_jsonable(v)}" for k, v in params.items())


def _tag(leg: str) -> str:
    """``"L2 the C7 identity exists ONLY for N <= 3"`` -> ``"L2"``, for messages."""
    return leg.split()[0] if " " in leg else leg


def control_selection(records: Iterable[treg.TestRecord],
                      repo_root: str | None = None,
                      timeout: float | None = None,
                      on_result: Callable[[RunResult], None] | None = None,
                      journal: str | None = None) -> dict[str, Any]:
    """Verify controls across a selection, journalling as it goes.

    The journal is written after **every** record, not at the end. A single bash
    call in this sandbox is killed at ~45 s (CLAUDE.md), and the barrier this
    feeds has to be resumable rather than all-or-nothing: a pass that loses its
    work on the timeout is a pass nobody runs twice.
    """
    repo_root = repo_root or _REPO
    recs = list(records)
    t0 = time.time()
    results: list[RunResult] = []
    prior = _read_journal(journal) if journal else {}
    prior_items = list(prior.get("items") or [])
    selected = {r.id for r in recs}
    # Verdicts for records OUTSIDE this selection are carried forward, not
    # dropped. The 45 s sandbox ceiling means this pass is run in slices —
    # `--id F298,F303`, then `--id F300` — and a journal that kept only the last
    # slice would make the gate demand a re-verify of everything but the slice
    # just run, which is a resumable pass that never finishes.
    carried = [it for it in prior_items
               if str(it.get("id", "")).split("#")[0] not in selected]

    for rec in recs:
        fp = record_fingerprint(rec, repo_root)
        cached = [RunResult(**it) for it in prior_items
                  if str(it.get("id", "")).split("#")[0] == rec.id
                  and it.get("metrics", {}).get("fingerprint") == fp]
        got = cached or run_control(rec, repo_root, timeout)
        for r in got:
            if cached:
                r.detail = (r.detail + "  [journalled]").strip()
            results.append(r)
            if on_result:
                on_result(r)
        if journal:
            _write_journal(journal, results, t0, carried=carried)

    counts: dict[str, int] = {}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    unsound = [r.id for r in results if not r.ok]
    report = {
        "generated": time.strftime("%Y-%m-%d - %H:%M"),
        "elapsed_s": round(time.time() - t0, 2),
        "n_records": len(recs),
        "n": len(results),
        "counts": counts,
        "unsound": unsound,
        "no_control": [r.id for r in results if r.status == "NOCTRL"],
        "items": [asdict(r) for r in results],
    }
    if journal:
        _write_journal(journal, results, t0, report, carried=carried)
    return report


def _read_journal(path: str) -> dict[str, Any]:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def _write_journal(path: str, results: list[RunResult], t0: float,
                   report: dict[str, Any] | None = None,
                   carried: list[dict] | None = None) -> None:
    items = [asdict(r) for r in results] + list(carried or [])
    payload = dict(report or {})
    payload.update({
        "generated": payload.get("generated") or time.strftime("%Y-%m-%d - %H:%M"),
        "elapsed_s": payload.get("elapsed_s", round(time.time() - t0, 2)),
        "n": payload.get("n", len(results)),
        "n_journalled": len(items),
        "items": items,
    })
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)
    os.replace(tmp, path)


def format_control_report(report: dict[str, Any]) -> str:
    c = report["counts"]
    order = [s for s in CONTROL_STATUSES + ("SKIP",) if s in c]
    head = "  ".join(f"{s}: {c[s]}" for s in order)
    lines = [f"\n{report['n']} control(s) over {report['n_records']} record(s), "
             f"{report['elapsed_s']:.1f}s   {head}"]
    if report["unsound"]:
        lines.append("\nNOT SOUND — these checks are not shown to be able to "
                     "fail:")
        by_id = {i["id"]: i for i in report["items"]}
        for rid in report["unsound"]:
            it = by_id[rid]
            lines.append(f"  {it['status']:8s} {rid}\n"
                         f"           {it['detail'][:190]}")
    return "\n".join(lines)
