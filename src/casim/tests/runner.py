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
    "DEFAULT_TIMEOUT", "GATE_TIMEOUT", "STATUSES",
]

STATUSES = ("PASS", "FAIL", "ERROR", "SKIP", "DEBT", "SWEEP")

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
        """
        return self.status in ("PASS", "SKIP", "DEBT", "SWEEP")


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
         os.path.join(repo_root, "ca-simulation"),
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
