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

# Group → list of pytest test directories (relative to repo root).
BATTERY_GROUPS = {
    "casim": "tests/casim",
    "priority": "tests/priority",
    "findings": "tests/findings",
}

DEFAULT_GROUPS = ("battery", "scenarios", "realspace")

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
        os.path.join(repo_root, "ca-simulation") + os.pathsep + env.get("PYTHONPATH", "")
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
    for path in sorted(_glob.glob(os.path.join(group_dir, "*.py"))):
        if os.path.basename(path) in ("__init__.py", "conftest.py"):
            continue
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


def run_battery_script(sub: str, path: str, repo_root: str, reporter: Reporter,
                       scale: str, timeout: float) -> ItemResult:
    """Run one standalone test script (``python file.py``); classify by exit
    code and the PASS/FAIL tokens it prints."""
    name = f"{sub}::{os.path.splitext(os.path.basename(path))[0]}"
    t0 = time.time()
    reporter.heartbeat(f"battery/{name}: running script", force=True)
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
    metrics = {"exit": proc.returncode, "pass_tokens": n_pass, "fail_tokens": n_fail}
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
    if n_pass:
        return ItemResult("battery", name, "PASS", secs,
                          f"{n_pass} PASS token(s), exit 0", metrics=metrics)
    return ItemResult("battery", name, "RAN", secs,
                      "exit 0; no PASS/FAIL token printed", metrics=metrics)


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
        })
    return plan


def run_suite(scale: str = DEFAULT_TIER,
              groups: Optional[Tuple[str, ...]] = None,
              out_dir: Optional[str] = None,
              report_every: float = 15.0,
              checkpoint_every: int = 0,
              mem_limit_gb: Optional[float] = None,
              only: Optional[List[str]] = None,
              repo_root: Optional[str] = None,
              script_timeout: float = 900.0,
              run_scripts: bool = True) -> Dict[str, Any]:
    groups = tuple(groups or DEFAULT_GROUPS)
    repo_root = repo_root or find_repo_root()
    if out_dir is None:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        out_dir = os.path.join(repo_root, "test-results", "suite", f"{scale}_{stamp}")
    os.makedirs(out_dir, exist_ok=True)

    # make the in-repo packages importable for this process & subprocesses
    for sub in ("src", "ca-simulation"):
        p = os.path.join(repo_root, sub)
        if p not in sys.path:
            sys.path.insert(0, p)

    reporter = Reporter(out_dir, scale, groups, report_every)
    reporter.log(f"CASIM suite — scale={scale}  groups={list(groups)}")
    reporter.log(f"repo={repo_root}")
    reporter.log(f"out={out_dir}")
    reporter.log(f"tier: {TIERS[scale].blurb}")

    # ---- battery group (correctness gate) ----
    if "battery" in groups:
        reporter.log("=== group: battery (correctness gate — pytest + scripts) ===")
        have_pytest = _pytest_available()
        if not have_pytest:
            reporter.log("  (pytest not installed: pytest-style files SKIP; "
                         "standalone scripts still run)")
        for sub, tp in BATTERY_GROUPS.items():
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
