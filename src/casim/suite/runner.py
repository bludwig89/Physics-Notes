"""casim.suite.runner — the unified, user-run, grouped test suite.

One driver runs every runnable test in groups, with periodic reporting, at a
chosen scale tier (orders of magnitude over the shipped sandbox sizes):

  battery    the pytest correctness battery (tests/findings, tests/priority,
             tests/casim) — the algebraic/exactness gate.  Run as a pass/fail
             gate; the scale tiers do NOT change these (they assert exactness).
  scenarios  every committed CASIM YAML scenario, re-run at the tier's L/ticks.
  realspace  the block-spin / real-space scenarios, where the tier grows the
             represented physical patch (proton/neutron ~1 fm, hydrogen ~Bohr)
             while the tractable super-cell lattice stays fixed (F129–F133).
  numerical  (opt-in) the standalone tests/runners/run_*.py scale scripts.

Design points that matter for a *user-run, long, native* job:
  • Periodic reporting — long scenarios are driven in tick-chunks; a progress
    line is emitted on a wall-clock cadence (``--report-every`` s), and a
    partial report (JSON + Markdown) is rewritten after every item and group,
    so a multi-hour run is inspectable mid-flight.
  • Checkpoint-aware — scenarios keep their committed ``checkpoint:`` block (and
    a ``--checkpoint-every`` override), so a job that exceeds a wall-clock cap
    can ``casim resume`` and continue.
  • Graceful degradation — a missing pytest, a SciPy-only scenario, or a single
    scenario blow-up is recorded and the suite carries on.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional, Tuple

from .tiers import (TIERS, DEFAULT_TIER, OVERRIDES, plan_size, SizePlan,
                    base_L_of, lattice_dims)

# Group → test directory (relative to repo root).
#
# Roadmap P1.1 — three honest tiers:
#   gate     tests/casim, run by bare `pytest` and `make gate`. Fast, asserting.
#   battery  everything below. Hours; run explicitly via `casim test`.
#   archive  files the supersession ledger marks fully superseded. Excluded.
#
# `tests/runners` (45 files) was previously in an opt-in `numerical` group that
# was not in DEFAULT_GROUPS, so nothing ever ran it. It is in the battery now.
BATTERY_GROUPS = {
    "casim": "tests/casim",
    "priority": "tests/priority",
    "findings": "tests/findings",
    "runners": "tests/runners",
}

DEFAULT_GROUPS = ("battery", "scenarios", "realspace")


def _archived_paths(repo_root: str) -> set:
    """Fully-superseded files, from docs/theory/supersessions.yaml.

    Only `fully_superseded` is excluded. `partially_superseded` files keep
    running: their dead claims are named in a docstring banner, but the live
    checks around them are load-bearing (see the ledger's `retained:` fields).
    """
    path = os.path.join(repo_root, "docs", "theory", "supersessions.yaml")
    try:
        import yaml
        with open(path, encoding="utf-8") as fh:
            led = yaml.safe_load(fh)
    except Exception:
        return set()
    out = set()
    for rec in led.get("supersessions", []):
        for entry in rec.get("tests") or []:
            if entry.get("status") == "fully_superseded":
                out.add(os.path.normpath(os.path.join(repo_root, entry["path"])))
    return out

# Scenarios routed to the realspace group (block-spin / physical-patch).
REALSPACE_SCENARIOS = {
    "realspace_proton_1fm", "realspace_neutron_1fm",
    "realspace_hydrogen_bohr", "realspace_photon_patch", "blockspin_photon",
}


# ----------------------------------------------------------------------
# result records
# ----------------------------------------------------------------------
@dataclass
class ItemResult:
    group: str
    name: str
    status: str                       # PASS | FAIL | RAN | SKIP | ERROR
    seconds: float = 0.0
    detail: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)
    sizing: Dict[str, Any] = field(default_factory=dict)


# ----------------------------------------------------------------------
# reporter — periodic progress + partial report files
# ----------------------------------------------------------------------
class Reporter:
    def __init__(self, out_dir: str, scale: str, groups: Tuple[str, ...],
                 report_every: float):
        self.out_dir = out_dir
        self.scale = scale
        self.groups = groups
        self.report_every = report_every
        self.t0 = time.time()
        self._last_beat = self.t0
        self.items: List[ItemResult] = []
        os.makedirs(out_dir, exist_ok=True)
        self.json_path = os.path.join(out_dir, "suite_report.json")
        self.md_path = os.path.join(out_dir, "suite_report.md")

    # -- console --------------------------------------------------------
    def elapsed(self) -> str:
        return f"[+{time.time() - self.t0:7.1f}s]"

    def log(self, msg: str) -> None:
        print(f"{self.elapsed()} {msg}", flush=True)

    def heartbeat(self, msg: str, force: bool = False) -> None:
        now = time.time()
        if force or (now - self._last_beat) >= self.report_every:
            self._last_beat = now
            print(f"{self.elapsed()}   … {msg}", flush=True)

    # -- accumulate -----------------------------------------------------
    def add_prior(self, item: ItemResult) -> None:
        """Carry a verdict forward from a previous attempt (P2.6 resume).

        Kept separate from `add` deliberately: a resumed item is not work this
        process did, so it must not reset the heartbeat, must not be re-logged
        as if it just ran, and must not overwrite the report until at least one
        real item lands. It only has to appear in the final counts.
        """
        self.items.append(item)

    def add(self, item: ItemResult) -> None:
        self.items.append(item)
        tag = {"PASS": "PASS", "RAN": "ran ", "FAIL": "FAIL",
               "SKIP": "skip", "ERROR": "ERR "}.get(item.status, item.status)
        extra = ""
        if item.sizing:
            sz = item.sizing
            if sz.get("realspace"):
                extra = (f"  patch={sz.get('physical_L')}^{sz.get('dims')} "
                         f"(block {sz.get('block')}, ~{sz.get('represented_cells'):.2e} cells)")
            elif "L" in sz:
                extra = f"  L={sz.get('L')} ticks={sz.get('ticks')} ×{sz.get('cost_factor', 1):.0f}"
        self.log(f"[{tag}] {item.group}/{item.name}  ({item.seconds:.1f}s){extra}"
                 + (f"  — {item.detail}" if item.detail and item.status in
                    ("FAIL", "ERROR", "SKIP") else ""))
        self.flush()

    # -- counts ---------------------------------------------------------
    def counts(self) -> Dict[str, int]:
        c: Dict[str, int] = {}
        for it in self.items:
            c[it.status] = c.get(it.status, 0) + 1
        return c

    # -- partial / final report files -----------------------------------
    def flush(self) -> None:
        report = {
            "scale": self.scale,
            "groups": list(self.groups),
            "elapsed_s": round(time.time() - self.t0, 1),
            "counts": self.counts(),
            "items": [asdict(it) for it in self.items],
            "complete": False,
        }
        with open(self.json_path, "w") as fh:
            json.dump(report, fh, indent=2, default=str)
        self._write_md(report)

    def finalize(self) -> Dict[str, Any]:
        report = {
            "scale": self.scale,
            "groups": list(self.groups),
            "elapsed_s": round(time.time() - self.t0, 1),
            "counts": self.counts(),
            "items": [asdict(it) for it in self.items],
            "complete": True,
        }
        with open(self.json_path, "w") as fh:
            json.dump(report, fh, indent=2, default=str)
        self._write_md(report)
        return report

    def _write_md(self, report: Dict[str, Any]) -> None:
        c = report["counts"]
        order = ["PASS", "RAN", "FAIL", "ERROR", "SKIP"]
        head = "  ".join(f"{k}: {c[k]}" for k in order if k in c)
        lines = [
            f"# CASIM suite report — scale `{report['scale']}`",
            "",
            f"_{time.strftime('%Y-%m-%d - %H:%M')}_  ·  "
            f"elapsed {report['elapsed_s']:.0f}s  ·  "
            f"{'COMPLETE' if report['complete'] else 'IN PROGRESS'}",
            "",
            f"**{head}**",
            "",
            "| group | item | status | t (s) | sizing | detail |",
            "|---|---|---|---:|---|---|",
        ]
        for it in report["items"]:
            sz = it.get("sizing") or {}
            if sz.get("realspace"):
                szs = (f"patch {sz.get('physical_L')}^{sz.get('dims')} "
                       f"(block {sz.get('block')})")
            elif "L" in sz:
                szs = f"L={sz.get('L')}, ticks={sz.get('ticks')} (×{sz.get('cost_factor', 1):.0f})"
            else:
                szs = ""
            det = (it.get("detail") or "").replace("|", "\\|").replace("\n", " ")
            if len(det) > 80:
                det = det[:77] + "…"
            lines.append(f"| {it['group']} | {it['name']} | {it['status']} | "
                         f"{it['seconds']:.1f} | {szs} | {det} |")
        lines.append("")
        with open(self.md_path, "w") as fh:
            fh.write("\n".join(lines))


# ----------------------------------------------------------------------
# scenario discovery
# ----------------------------------------------------------------------
def discover_scenarios(scenarios_dir: str) -> Dict[str, str]:
    import glob
    out: Dict[str, str] = {}
    for path in sorted(glob.glob(os.path.join(scenarios_dir, "*.yaml"))):
        name = os.path.splitext(os.path.basename(path))[0]
        out[name] = path
    return out


# ----------------------------------------------------------------------
# scenario runner (chunked, with periodic reporting + gate)
# ----------------------------------------------------------------------
def run_scenario(name: str, path: str, plan: SizePlan, out_dir: str,
                 reporter: Reporter, checkpoint_every: int,
                 mem_limit_gb: Optional[float]) -> ItemResult:
    from casim.io import load_scenario, write_results
    from casim.engine import Simulation
    from casim import analysis

    sizing = {
        "tier": plan.tier, "dims": plan.dims, "L": plan.L, "ticks": plan.ticks,
        "block": plan.block, "physical_L": plan.physical_L,
        "represented_cells": plan.represented_cells,
        "compute_cells": plan.compute_cells, "cost_factor": plan.cost_factor,
        "mem_gb": round(plan.mem_gb, 3), "realspace": plan.realspace,
        "wall_estimate": plan.wall_human,
    }
    group = "realspace" if plan.realspace else "scenarios"

    if plan.skipped:
        return ItemResult(group, name, "SKIP", 0.0,
                          f"size-invariant at tier {plan.tier} ({plan.note})",
                          sizing=sizing)
    if mem_limit_gb is not None and plan.mem_gb > mem_limit_gb:
        return ItemResult(group, name, "SKIP", 0.0,
                          f"projected {plan.mem_gb:.1f} GB > --mem-gb {mem_limit_gb}",
                          sizing=sizing)

    t0 = time.time()
    try:
        scenario = load_scenario(path)
        # apply tier sizing
        lat = scenario.setdefault("lattice", {})
        if plan.realspace:
            # grow the represented physical patch; hold super-cell L fixed
            lat.pop("L", None)
            lat["block"] = plan.block
            lat["physical_patch"] = plan.physical_L
        else:
            lat["L"] = plan.L
        scenario["ticks"] = plan.ticks
        # redirect output into the suite folder (never clobber committed JSON)
        scenario.setdefault("output", {})["json"] = os.path.join(
            out_dir, "scenarios", f"{name}.json")
        # honour / override checkpointing for resumable long runs
        if checkpoint_every > 0:
            ck = scenario.setdefault("checkpoint", {})
            ck.setdefault("dir", os.path.join(out_dir, "checkpoints"))
            ck["every"] = checkpoint_every

        sim = Simulation.from_scenario(scenario)
        target = int(scenario["ticks"])

        # baseline observers (mirrors Simulation.run), then chunked stepping so
        # we can emit periodic progress on a wall-clock cadence.
        sim._run_observers()
        if target > 0:
            chunk = max(1, min(target, target // 20 or 1))
            done = 0
            while sim.tick < target:
                n = min(chunk, target - sim.tick)
                sim.step(n)
                done = sim.tick
                reporter.heartbeat(
                    f"{name}: tick {done}/{target} "
                    f"({100.0 * done / target:.0f}%)  L={sim.lattice.L}")
        results = sim.collect_results()
        write_results(results, scenario["output"]["json"])

        # gate: machine-precision / exact observers must sit under tolerance
        rows = analysis.exactness_rows(results)
        gated = [r for r in rows if r["tol"] is not None]
        fails = [r for r in gated if not r["pass"]]
        metrics = _scenario_metrics(results)
        secs = time.time() - t0
        if fails:
            worst = max(fails, key=lambda r: (r["value"] or 0.0))
            return ItemResult(group, name, "FAIL", secs,
                              f"{len(fails)} gated obs over tol "
                              f"(worst {worst['observer']}={worst['value']:.2e})",
                              metrics=metrics, sizing=sizing)
        status = "PASS" if gated else "RAN"
        return ItemResult(group, name, status, secs,
                          "" if gated else "completed; no hard gate (quantitative only)",
                          metrics=metrics, sizing=sizing)
    except Exception as exc:  # noqa: BLE001 — one scenario must not kill the suite
        secs = time.time() - t0
        tb = traceback.format_exc().strip().splitlines()
        return ItemResult(group, name, "ERROR", secs,
                          f"{type(exc).__name__}: {exc}  | {tb[-1] if tb else ''}",
                          sizing=sizing)


def _scenario_metrics(results: Dict[str, Any]) -> Dict[str, Any]:
    m: Dict[str, Any] = {}
    pp = results.get("physical_patch")
    if pp:
        m["physical_patch"] = pp
    for oname, ores in (results.get("observers") or {}).items():
        summ = ores.get("summary") or {}
        if "max_rel_drift" in summ:
            drifts = summ["max_rel_drift"]
            if isinstance(drifts, dict) and drifts:
                m["max_rel_drift"] = max(float(v) for v in drifts.values())
    return m


# ----------------------------------------------------------------------
# pytest battery runner (subprocess + JUnit XML; graceful if absent)
# ----------------------------------------------------------------------
def _pytest_available() -> bool:
    try:
        subprocess.run([sys.executable, "-m", "pytest", "--version"],
                       capture_output=True, check=True)
        return True
    except Exception:
        return False


import glob as _glob
import re as _re

_PYTEST_MARKER = _re.compile(r"^\s*(def test_|async def test_|class Test)",
                             _re.MULTILINE)
# stdout tokens the repo's standalone scripts print for their own gates
_FAIL_TOKEN = _re.compile(r"(?<![A-Za-z])(FAIL|FAILED)(?![A-Za-z])|❌")
_PASS_TOKEN = _re.compile(r"(?<![A-Za-z])(PASS|PASSED)(?![A-Za-z])|✅")


def _battery_env(repo_root: str, scale: str) -> Dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(repo_root, "src") + os.pathsep + \
        env.get("PYTHONPATH", "")
    env["CASIM_SCALE"] = scale          # scale-aware tests/scripts can read this
    env["MPLBACKEND"] = "Agg"           # never pop a plot window in a batch run
    return env


def _classify_battery_files(group_dir: str) -> Tuple[List[str], List[str]]:
    """Split a test dir into (pytest-collectable, standalone-script) files.

    A file is pytest-collectable iff it defines a ``test_`` function or a
    ``Test`` class; everything else in the repo is a standalone ``main()``
    script that signals pass/fail via its exit code and printed PASS/FAIL
    tokens (e.g. the whole tests/priority battery)."""
    pytest_files: List[str] = []
    script_files: List[str] = []
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(group_dir))) \
        if os.path.isabs(group_dir) else os.getcwd()
    archived = _archived_paths(repo_root)
    for path in sorted(_glob.glob(os.path.join(group_dir, "*.py"))):
        if os.path.basename(path) in ("__init__.py", "conftest.py"):
            continue
        if os.path.normpath(os.path.abspath(path)) in archived:
            continue                        # archive tier — see the ledger
        try:
            with open(path, "r", errors="replace") as fh:
                text = fh.read()
        except Exception:
            text = ""
        (pytest_files if _PYTEST_MARKER.search(text) else script_files).append(path)
    return pytest_files, script_files


def run_battery_pytest(sub: str, pytest_files: List[str], repo_root: str,
                       out_dir: str, reporter: Reporter, scale: str) -> ItemResult:
    """Run the pytest-collectable files of one group in a single subprocess."""
    if not pytest_files:
        return ItemResult("battery", f"{sub}::pytest", "SKIP", 0.0,
                          "no pytest-collectable files in group")
    if not _pytest_available():
        return ItemResult("battery", f"{sub}::pytest", "SKIP", 0.0,
                          f"{len(pytest_files)} pytest files — pytest not installed "
                          "(pip install pytest)")
    xml = os.path.join(out_dir, "junit", f"battery_{sub}.xml")
    os.makedirs(os.path.dirname(xml), exist_ok=True)
    cmd = [sys.executable, "-m", "pytest", *pytest_files,
           "-q", "--no-header", "--tb=line", f"--junit-xml={xml}",
           "-p", "no:cacheprovider", "--continue-on-collection-errors"]
    t0 = time.time()
    reporter.heartbeat(f"battery/{sub}: pytest on {len(pytest_files)} files", force=True)
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          env=_battery_env(repo_root, scale), cwd=repo_root)
    secs = time.time() - t0
    passed, failed, errors, skipped = _parse_junit(xml)
    metrics = {"passed": passed, "failed": failed, "errors": errors,
               "skipped": skipped, "n_files": len(pytest_files)}
    detail = f"{passed} passed, {failed} failed, {errors} errors, {skipped} skipped"
    # rc 5 = "no tests collected" (handled by pre-filter, but be safe);
    # rc 2/3/4 with nothing parsed = a real collection/usage error.
    if proc.returncode not in (0, 1, 5) and passed + failed + errors == 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        return ItemResult("battery", f"{sub}::pytest", "ERROR", secs,
                          f"pytest error (rc={proc.returncode}): "
                          f"{tail[-1] if tail else 'unknown'}", metrics=metrics)
    status = "PASS" if (failed == 0 and errors == 0) else "FAIL"
    return ItemResult("battery", f"{sub}::pytest", status, secs, detail,
                      metrics=metrics)


def _result_drift(repo_root: str, before_mtimes: Dict[str, float]) -> List[str]:
    """Result JSONs a script just rewrote whose NUMBERS moved against git.

    Roadmap P1.2. Most of the battery cannot fail: 232 of 344 test files have
    no `assert`, and a script that exits 0 without printing a PASS token lands
    in `RAN`, which reads like success. But those scripts do write their numbers
    to test-results/, and those files are committed — so HEAD is the baseline
    and drift is a real, checkable failure. No test file needs editing for this.
    """
    try:
        from casim.baselines import drift_report
    except Exception:
        return []
    touched = []
    for rel, was in before_mtimes.items():
        full = os.path.join(repo_root, rel)
        try:
            if os.path.getmtime(full) > was:
                touched.append(rel)
        except OSError:
            continue
    if not touched:
        return []
    report = drift_report(touched, ref="HEAD", cwd=repo_root)
    return [f"{p}: " + "; ".join(
        f"{d.path} {d.before!r}->{d.after!r}" for d in deltas[:3])
        for p, deltas in sorted(report.items())]


def _result_mtimes(repo_root: str) -> Dict[str, float]:
    out: Dict[str, float] = {}
    rdir = os.path.join(repo_root, "test-results")
    for dirpath, dirnames, filenames in os.walk(rdir):
        dirnames[:] = [d for d in dirnames
                       if d not in ("__pycache__", "figures", "logs", "suite")]
        for fn in filenames:
            if fn.endswith(".json") and fn != "manifest.json":
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, repo_root).replace(os.sep, "/")
                try:
                    out[rel] = os.path.getmtime(full)
                except OSError:
                    pass
    return out


def run_battery_script(sub: str, path: str, repo_root: str, reporter: Reporter,
                       scale: str, timeout: float,
                       check_drift: bool = True) -> ItemResult:
    """Run one standalone test script (``python file.py``).

    Classified by exit code, the PASS/FAIL tokens it prints, and — new in P1.2
    — whether the numbers in any result artifact it rewrote drifted from git.
    That last check is what gives the ~232 assertion-free scripts a failure
    mode without touching them.
    """
    name = f"{sub}::{os.path.splitext(os.path.basename(path))[0]}"
    t0 = time.time()
    reporter.heartbeat(f"battery/{name}: running script", force=True)
    before = _result_mtimes(repo_root) if check_drift else {}
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True,
                              text=True, env=_battery_env(repo_root, scale),
                              cwd=repo_root, timeout=timeout)
    except subprocess.TimeoutExpired:
        return ItemResult("battery", name, "ERROR", time.time() - t0,
                          f"timed out after {timeout:.0f}s (raise --script-timeout)")
    secs = time.time() - t0
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    n_fail = len(_FAIL_TOKEN.findall(out))
    n_pass = len(_PASS_TOKEN.findall(out))
    drift = _result_drift(repo_root, before) if check_drift else []
    metrics = {"exit": proc.returncode, "pass_tokens": n_pass,
               "fail_tokens": n_fail, "drifted_results": len(drift)}
    if proc.returncode != 0:
        tail = out.strip().splitlines()
        return ItemResult("battery", name, "ERROR", secs,
                          f"exit {proc.returncode}: {tail[-1] if tail else ''}",
                          metrics=metrics)
    if n_fail:
        fail_line = next((ln.strip() for ln in out.splitlines()
                          if _FAIL_TOKEN.search(ln)), "")
        return ItemResult("battery", name, "FAIL", secs,
                          f"{n_fail} FAIL token(s); first: {fail_line[:100]}",
                          metrics=metrics)
    if drift:
        # Numbers moved. This outranks a printed PASS: the script's own gates
        # may still be satisfied while a physical value has changed underneath.
        return ItemResult("battery", name, "FAIL", secs,
                          f"result drift vs HEAD — {drift[0][:160]}",
                          metrics=metrics)
    if n_pass:
        return ItemResult("battery", name, "PASS", secs,
                          f"{n_pass} PASS token(s), exit 0", metrics=metrics)
    if before and metrics["drifted_results"] == 0 and any(
            os.path.getmtime(os.path.join(repo_root, r)) > w
            for r, w in before.items()
            if os.path.exists(os.path.join(repo_root, r))):
        # No assertion, no token — but it reproduced its committed numbers.
        # That is a genuine pass, and naming it as one is the point of P1.2.
        return ItemResult("battery", name, "PASS", secs,
                          "no PASS token, but result artifact reproduced HEAD "
                          "exactly (baseline match)", metrics=metrics)
    return ItemResult("battery", name, "RAN", secs,
                      "exit 0; no PASS/FAIL token, no result artifact to diff "
                      "— this test has no failure mode", metrics=metrics)


def _parse_junit(xml_path: str) -> Tuple[int, int, int, int]:
    """Return (passed, failed, errors, skipped) from a JUnit XML."""
    if not os.path.exists(xml_path):
        return (0, 0, 0, 0)
    import xml.etree.ElementTree as ET
    try:
        root = ET.parse(xml_path).getroot()
    except Exception:
        return (0, 0, 0, 0)
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    tests = failures = errors = skipped = 0
    for s in suites:
        tests += int(s.get("tests", 0))
        failures += int(s.get("failures", 0))
        errors += int(s.get("errors", 0))
        skipped += int(s.get("skipped", 0))
    passed = tests - failures - errors - skipped
    return (passed, failures, errors, skipped)


# ----------------------------------------------------------------------
# top-level orchestration
# ----------------------------------------------------------------------
def find_repo_root(start: Optional[str] = None) -> str:
    here = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(here, "scenarios")) and \
           os.path.isdir(os.path.join(here, "tests")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            # fall back to two levels up from this file (src/casim/suite → repo)
            return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..", "..", ".."))
        here = parent


def build_plan(scale: str, groups: Tuple[str, ...], repo_root: str,
               only: Optional[List[str]] = None) -> Dict[str, Any]:
    """Dry-run plan: what would run, at what size, with cost/memory estimates."""
    from casim.io import load_scenario
    scenarios = discover_scenarios(os.path.join(repo_root, "scenarios"))
    plan: Dict[str, Any] = {"scale": scale, "groups": list(groups),
                            "battery": [], "scenarios": [], "realspace": []}
    if "battery" in groups:
        plan["battery"] = [{"group": g, "path": p} for g, p in BATTERY_GROUPS.items()]
    for name, path in scenarios.items():
        is_rs = name in REALSPACE_SCENARIOS or OVERRIDES.get(name, None) and \
            getattr(OVERRIDES.get(name), "realspace", False)
        grp = "realspace" if is_rs else "scenarios"
        if grp not in groups:
            continue
        if only and name not in only:
            continue
        try:
            sc = load_scenario(path)
        except Exception as exc:
            plan[grp].append({"name": name, "error": str(exc)})
            continue
        sp = plan_size(name, sc, scale)
        plan[grp].append({
            "name": name, "L": sp.L, "ticks": sp.ticks, "block": sp.block,
            "physical_L": sp.physical_L, "represented_cells": sp.represented_cells,
            "compute_cells": sp.compute_cells, "cost_factor": round(sp.cost_factor, 1),
            "mem_gb": round(sp.mem_gb, 3), "skipped": sp.skipped,
            "realspace": sp.realspace,
            # P2.6: the wall-time ESTIMATE, so `--list` can size a long run.
            "wall_seconds": (None if sp.wall_seconds is None
                             else round(sp.wall_seconds, 1)),
            "wall": sp.wall_human,
        })
    return plan


def _newest_suite_dir(repo_root: str, scale: str) -> Optional[str]:
    """The most recent `test-results/suite/{scale}_*` directory, or None.

    Sorted by name, not mtime: the names carry a `%Y%m%d-%H%M%S` stamp, so
    lexical order *is* chronological order, and a resumed run rewriting its own
    report would otherwise make an older directory look newest.
    """
    base = os.path.join(repo_root, "test-results", "suite")
    if not os.path.isdir(base):
        return None
    cands = sorted(d for d in os.listdir(base)
                   if d.startswith(f"{scale}_")
                   and os.path.isdir(os.path.join(base, d)))
    return os.path.join(base, cands[-1]) if cands else None


def _load_prior_items(out_dir: str) -> List[ItemResult]:
    """Verdicts already recorded in this out_dir's `suite_report.json`.

    The Reporter rewrites that file after every item, so it is already a
    journal; P2.6 just reads it. A malformed or absent report yields an empty
    list — resuming into a fresh run is correct behaviour, and refusing to start
    because a journal is unreadable would be the wrong trade for a long job.
    """
    path = os.path.join(out_dir, "suite_report.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        return []
    out: List[ItemResult] = []
    for rec in data.get("items", []) or []:
        try:
            out.append(ItemResult(
                group=str(rec["group"]), name=str(rec["name"]),
                status=str(rec["status"]), seconds=float(rec.get("seconds", 0.0)),
                detail=str(rec.get("detail", "")),
                sizing=rec.get("sizing") or None))
        except Exception:
            continue
    return out


def run_suite(scale: str = DEFAULT_TIER,
              groups: Optional[Tuple[str, ...]] = None,
              out_dir: Optional[str] = None,
              report_every: float = 15.0,
              checkpoint_every: int = 0,
              mem_limit_gb: Optional[float] = None,
              only: Optional[List[str]] = None,
              repo_root: Optional[str] = None,
              script_timeout: float = 900.0,
              run_scripts: bool = True,
              resume: bool = False,
              redo: Optional[List[str]] = None) -> Dict[str, Any]:
    groups = tuple(groups or DEFAULT_GROUPS)
    repo_root = repo_root or find_repo_root()

    # ---- P2.6: auto-resume -------------------------------------------------
    # The docstring promised a checkpoint-aware suite since it was written, and
    # the implementation was missing: a 1000x run that died at item 9 of 14
    # restarted from item 1, and because `out_dir` carried a fresh timestamp it
    # could not even find its own checkpoints. Two changes make it real —
    # `--resume` reuses the newest matching directory, and the per-item
    # `suite_report.json` the Reporter already rewrites after every item is
    # treated as the journal, so nothing new has to be persisted.
    prior: List[ItemResult] = []
    if resume and out_dir is None:
        out_dir = _newest_suite_dir(repo_root, scale)
        if out_dir is None:
            raise SystemExit(
                f"--resume: no previous test-results/suite/{scale}_* directory "
                f"to resume. Start a run normally, or pass --out explicitly.")
    if out_dir is None:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        out_dir = os.path.join(repo_root, "test-results", "suite", f"{scale}_{stamp}")
    os.makedirs(out_dir, exist_ok=True)
    if resume:
        prior = _load_prior_items(out_dir)

    # make the in-repo packages importable for this process & subprocesses
    p = os.path.join(repo_root, "src")
    if p not in sys.path:
        sys.path.insert(0, p)

    reporter = Reporter(out_dir, scale, groups, report_every)
    reporter.log(f"CASIM suite — scale={scale}  groups={list(groups)}")
    reporter.log(f"repo={repo_root}")
    reporter.log(f"out={out_dir}")
    reporter.log(f"tier: {TIERS[scale].blurb}")

    # Items already decided in a previous attempt at this out_dir. `redo` names
    # items to re-run anyway (a bare `--redo` re-runs every non-PASS).
    done: set = set()
    if prior:
        redo_set = set(redo or ())
        redo_all_failures = "" in redo_set or "failures" in redo_set
        for it in prior:
            key = f"{it.group}/{it.name}"
            if key in redo_set:
                continue
            if redo_all_failures and it.status != "PASS":
                continue
            done.add(key)
            reporter.add_prior(it)
        reporter.log(f"resuming: {len(done)} item(s) already decided, "
                     f"{len(prior) - len(done)} to re-run")

    def _skip_done(group: str, name: str) -> bool:
        return f"{group}/{name}" in done

    # ---- battery group (correctness gate) ----
    if "battery" in groups:
        reporter.log("=== group: battery (correctness gate — pytest + scripts) ===")
        have_pytest = _pytest_available()
        if not have_pytest:
            reporter.log("  (pytest not installed: pytest-style files SKIP; "
                         "standalone scripts still run)")
        for sub, tp in BATTERY_GROUPS.items():
            if _skip_done("battery", sub):
                continue
            group_dir = os.path.join(repo_root, tp)
            if not os.path.isdir(group_dir):
                reporter.add(ItemResult("battery", sub, "SKIP", 0.0, f"no dir {tp}"))
                continue
            pytest_files, script_files = _classify_battery_files(group_dir)
            reporter.log(f"  {sub}: {len(pytest_files)} pytest file(s), "
                         f"{len(script_files)} standalone script(s)")
            reporter.add(run_battery_pytest(sub, pytest_files, repo_root,
                                            out_dir, reporter, scale))
            if run_scripts:
                for path in script_files:
                    reporter.add(run_battery_script(sub, path, repo_root,
                                                    reporter, scale, script_timeout))
            elif script_files:
                reporter.add(ItemResult("battery", f"{sub}::scripts", "SKIP", 0.0,
                                        f"{len(script_files)} standalone scripts "
                                        "skipped (--no-scripts)"))

    # ---- scenario + realspace groups ----
    scenarios = discover_scenarios(os.path.join(repo_root, "scenarios"))
    for grp in ("scenarios", "realspace"):
        if grp not in groups:
            continue
        reporter.log(f"=== group: {grp} (scale tier {scale}) ===")
        for name, path in scenarios.items():
            ov = OVERRIDES.get(name)
            is_rs = name in REALSPACE_SCENARIOS or (ov and ov.realspace)
            if (grp == "realspace") != bool(is_rs):
                continue
            if only and name not in only:
                continue
            if _skip_done(grp, name):
                continue
            from casim.io import load_scenario
            try:
                sc = load_scenario(path)
            except Exception as exc:
                reporter.add(ItemResult(grp, name, "ERROR", 0.0, f"load: {exc}"))
                continue
            sp = plan_size(name, sc, scale)
            reporter.add(run_scenario(name, path, sp, out_dir, reporter,
                                      checkpoint_every, mem_limit_gb))

    report = reporter.finalize()
    c = report["counts"]
    reporter.log("=== suite complete ===")
    reporter.log("  " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())))
    reporter.log(f"  report: {reporter.md_path}")
    return report
