#!/usr/bin/env python3
"""The repository gate — roadmap P0.5.

Before P0 this project had **no automated enforcement of any kind**: no CI, no
Makefile, and `testpaths = ["tests/casim"]`, so a bare `pytest` exercised 6
files out of 340. This is the first thing that can say no.

Design constraints, each learned from the audit:

  * **Fast.** Under two minutes, so it can run on every change. Long physics
    belongs in `casim test`, not here.
  * **Cannot silently pass.** `casim test` SKIPS every pytest-style file when
    pytest is missing (runner.py:365-368) and still reports success. This gate
    runs its own checks standalone when pytest is absent, and says loudly which
    mode it is in.
  * **Asserts, never scrapes.** No counting PASS/FAIL tokens in stdout.

Usage:
    python3 tools/run_gate.py            # the gate
    python3 tools/run_gate.py --verbose  # show child output
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GREEN, RED, YELLOW, DIM, RESET = (
    "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
) if sys.stdout.isatty() else ("", "", "", "", "")


def _have_pytest() -> bool:
    return subprocess.run([sys.executable, "-c", "import pytest"],
                          capture_output=True).returncode == 0


class Gate:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.results: list[tuple[str, bool, float, str]] = []

    def run(self, label: str, argv: list[str], env: dict | None = None) -> bool:
        t0 = time.time()
        full_env = dict(os.environ)
        full_env.setdefault("PYTHONPATH", os.path.join(_REPO, "src"))
        if env:
            full_env.update(env)
        proc = subprocess.run(argv, cwd=_REPO, env=full_env,
                              capture_output=True, text=True)
        dt = time.time() - t0
        ok = proc.returncode == 0
        tail = (proc.stdout or "") + (proc.stderr or "")
        self.results.append((label, ok, dt, tail))
        mark = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
        print(f"  {mark}  {label:<42s} {dt:6.2f}s")
        if self.verbose or not ok:
            for line in tail.strip().splitlines()[-25:]:
                print(f"        {DIM}{line}{RESET}")
        return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    print(f"\n{'=' * 62}\n  casim gate\n{'=' * 62}")
    gate = Gate(args.verbose)
    py = sys.executable
    has_pytest = _have_pytest()

    # Roadmap P2.1: print the FFT backend on every gate run. This project spent
    # its whole history on single-threaded scipy while ca_fft advertised FFTW,
    # purely because nothing ever said which one was live.
    probe = subprocess.run(
        [py, "-c", "import sys; sys.path.insert(0, 'ca-simulation'); "
                   "import ca_fft; print(ca_fft.describe())"],
        cwd=_REPO, capture_output=True, text=True)
    if probe.returncode == 0:
        print(f"\n{DIM}fft backend: {probe.stdout.strip()}{RESET}")

    # -- 1. Provenance -----------------------------------------------------
    print("\nprovenance")
    gate.run("no unregistered constant literals (D7)",
             [py, "tests/casim/test_constants_consistency.py"])
    gate.run("supersession ledger is true",
             [py, "tests/casim/test_supersession_ledger.py"])
    gate.run("supersession banners are current",
             [py, "tools/apply_supersession_banners.py", "--check"])

    # -- 1b. Test-suite health (roadmap P1) --------------------------------
    print("\ntest-suite health")
    gate.run("test health has not regressed", [py, "tools/audit_tests.py", "--ratchet"])
    gate.run("numerics imports have not regressed (D8)",
             [py, "tools/audit_numerics.py", "--ratchet"])
    gate.run("constants sprawl has not regressed (D7)",
             [py, "tools/audit_constants.py", "--ratchet"])
    # Roadmap C7 / D9. Coverage first (every test file has a record), then
    # staleness (the generated `evidence:` blocks match the tree).
    gate.run("test registry covers every test file (D9)",
             [py, "tools/check_test_registry.py"])
    gate.run("test registry is current",
             [py, "tools/gen_test_registry.py", "--check"])
    # Roadmap C8. ONE check replaces three: the results manifest, the exactness
    # inventory section, and the five markdown indexes were each verified by
    # their own generator, and each could be stale while the others were clean.
    # `casim index --check` covers all seven targets, and also fails on an
    # undeclared duplicate finding number (C8.2) and on an inventory that has
    # fallen behind the newest finding.
    gate.run("indexes, manifest and inventory are current (C8)",
             [py, "-m", "casim.cli", "index", "--check"])

    # -- 1c. Migration readiness (roadmap C0) ------------------------------
    # The manifest check is the C0 acceptance gate as an assertion: full
    # coverage of every file under ca-simulation/, unique target paths, known
    # sectors and phases, and no accepted dead symbol that the supersession
    # ledger names in a `retained:` field. A file with no record does not move.
    print("\nmigration readiness")
    gate.run("module graph is current", [py, "tools/gen_module_graph.py", "--check"])
    gate.run("migration manifest covers every file",
             [py, "tools/gen_migration_manifest.py", "--check"])
    gate.run("migrate_module self-test",
             [py, "tools/migrate_module.py", "--self-test"])
    gate.run("deprecated/ has no unaccounted files",
             [py, "tools/check_deprecated.py"])
    gate.run("module registry covers every engine module (D11)",
             [py, "tools/check_module_registry.py"])
    gate.run("no src code imports a ca-simulation shim path (C3.4)",
             [py, "tools/check_shim_imports.py"])

    # -- 2. Package suite --------------------------------------------------
    print("\npackage suite")
    if has_pytest:
        gate.run("pytest tests/casim",
                 [py, "-m", "pytest", "tests/casim", "-q",
                  "-m", "not superseded and not slow"])
    else:
        print(f"  {YELLOW}NOTE{RESET}  pytest not installed — running the "
              f"standalone entry points instead.")
        print(f"        {DIM}This is a REDUCED gate: files without a "
              f"__main__ block are not exercised.{RESET}")
        for fn in sorted(os.listdir(os.path.join(_REPO, "tests", "casim"))):
            if not (fn.startswith("test_") and fn.endswith(".py")):
                continue
            rel = f"tests/casim/{fn}"
            with open(os.path.join(_REPO, rel), encoding="utf-8") as fh:
                if "__main__" not in fh.read():
                    print(f"  {YELLOW}SKIP{RESET}  {rel:<42s} (no __main__)")
                    continue
            if fn in ("test_constants_consistency.py",
                      "test_supersession_ledger.py"):
                continue                       # already run above
            gate.run(rel, [py, rel])

    # -- 3. Scenario smoke -------------------------------------------------
    # (The old fixed `/tmp/gate_<name>.json` output path is gone with the
    # hand-coded runs: the registry's scenario kind writes no artifact at all,
    # which also removes the two-sessions-on-one-machine PermissionError this
    # block used to guard against with a private temp dir.)
    #
    # Roadmap C7.2: these three runs used to be hard-coded here, with their tick
    # counts living in this file and nowhere else. They are now `kind: scenario`
    # registry records, so the gate and `casim test --tier gate` select the same
    # objects and the tick counts are declared where every other test parameter
    # is. `casim test` exits 1 if the selection is empty, so deleting the
    # records cannot quietly stop the smoke test.
    print("\nscenario smoke (registry: --tier gate --kind scenario)")
    gate.run("gate-tier scenario records",
             [py, "-m", "casim.cli", "test", "--tier", "gate",
              "--kind", "scenario"])

    # -- summary -----------------------------------------------------------
    failed = [r for r in gate.results if not r[1]]
    total = sum(r[2] for r in gate.results)
    print(f"\n{'=' * 62}")
    if failed:
        print(f"  {RED}GATE FAILED{RESET} — {len(failed)} of "
              f"{len(gate.results)} checks, {total:.1f}s")
        for label, _, _, _ in failed:
            print(f"    - {label}")
    else:
        print(f"  {GREEN}GATE PASSED{RESET} — {len(gate.results)} checks, "
              f"{total:.1f}s")
    if not has_pytest:
        print(f"  {YELLOW}reduced mode: pytest was not available{RESET}")
    print("=" * 62 + "\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
