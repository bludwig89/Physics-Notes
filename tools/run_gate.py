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
    # C9: the probe used to reach `ca_fft` through the legacy directory. After
    # deletion that import fails — and because the return code was never
    # checked, the gate would have gone quietly back to not reporting which
    # backend is live, which is the exact defect P2.1 existed to fix. So the
    # probe now imports the façade (D8) and a failure is *reported*.
    probe = subprocess.run(
        [py, "-c", "from casim.numerics import fft; print(fft.describe())"],
        cwd=_REPO, capture_output=True, text=True,
        env={**os.environ, "PYTHONPATH": os.pathsep.join(
            ["src", os.environ.get("PYTHONPATH", "")])})
    if probe.returncode == 0:
        print(f"\n{DIM}fft backend: {probe.stdout.strip()}{RESET}")
    else:
        print(f"\n{DIM}fft backend: UNKNOWN — probe failed: "
              f"{(probe.stderr or '').strip().splitlines()[-1:]}{RESET}")

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
    # D9, added 2026-08-07 - 17:05 by the gap #2 pass: every test record a
    # finding DECLARES in its header exists, at the tier it claims, and the count
    # of gate entries that cannot fail at all is a ratchet at ceiling 8. Restored
    # here at 17:45 after a concurrent session (gap #3) committed a copy of this
    # file staged before 17:05 and dropped the line -- the collision CLAUDE.md's
    # concurrency section warns about, in the file that enforces the rest.
    gate.run("findings' declared records exist and can fail (D9)",
             [py, "tools/check_finding_records.py"])
    # Gap #3 / rubric row H2 (2026-08-07). The three checks above ask whether a
    # failure mode is DECLARED. This one asks whether it can trip. It is static —
    # shape of every `control:` block, plus a journalled CONTROL verdict at the
    # current code fingerprint — because verifying 55 records for real costs
    # minutes and this barrier costs seconds. `make control` does the running and
    # commits the journal; touching a driver moves its fingerprint and turns this
    # red with the record named, which is the same bargain `result_dump` records
    # already make with their committed baselines.
    gate.run("declared negative controls are sound (D9/H2)",
             [py, "tools/check_control_soundness.py", "--gate"])
    # Roadmap C8. ONE check replaces three: the results manifest, the exactness
    # inventory section, and the five markdown indexes were each verified by
    # their own generator, and each could be stale while the others were clean.
    # `casim index --check` covers all seven targets, and also fails on an
    # undeclared duplicate finding number (C8.2) and on an inventory that has
    # fallen behind the newest finding.
    gate.run("indexes, manifest and inventory are current (C8)",
             [py, "-m", "casim.cli", "index", "--check"])

    # -- 1c. Structure (roadmap C0-C9) -------------------------------------
    # Four checks were retired at C9 with the tree they guarded: the migration
    # manifest's coverage assertion, migrate_module's self-test, and the C3.4
    # shim-import check. The legacy tree no longer exists, so nothing can move
    # out of it, no manifest coverage can regress, and no shim can be imported.
    # The manifest itself stays live as the migration's provenance record —
    # `check_deprecated.py` reads it to verify all 171 backups.
    print("\nstructure")
    gate.run("module graph is current", [py, "tools/gen_module_graph.py", "--check"])
    gate.run("deprecated/ has no unaccounted files",
             [py, "tools/check_deprecated.py"])
    gate.run("module registry covers every engine module (D11)",
             [py, "tools/check_module_registry.py"])
    # Roadmap D12. The claims layer: closed vocabularies, referential
    # integrity, the debt ratchets, and THE rule -- a `status: live` card whose
    # every supporting finding is named in a `superseded:` list in the ledger.
    # That last one is the machine-checkable form of "overstated"; it is what
    # Claims-and-Falsifiers revisions 2 and 3 corrected by hand, months late.
    gate.run("claim cards are well-formed and not overstated (D12)",
             [py, "tools/check_claims.py"])

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
