#!/usr/bin/env python3
"""C5 — resumable, parallel runner for the particles sector's tests.

The sandbox kills background processes between shell calls and caps each call
at well under a minute, while the sector's 64 test files are individually heavy.
So this runs a **parallel pool with a wall-clock budget**, records each result to
/tmp/c5_results.json, and skips anything already recorded — call it repeatedly
until it reports nothing left. Invocation mode per file comes from
`migrate_module.how_to_run`, so a script is run as a script and a pytest-only
file is collected, exactly as the migration tool would.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from migrate_module import _REPO, how_to_run, load_manifest  # noqa: E402

SECTOR = "particles"
RESULTS = "/tmp/c5_results.json"


def load() -> dict:
    if os.path.exists(RESULTS):
        with open(RESULTS) as fh:
            return json.load(fh)
    return {}


def one(rel: str, timeout: int) -> dict:
    full = os.path.join(_REPO, rel)
    if not os.path.exists(full):
        return {"status": "missing"}
    with open(full, encoding="utf-8", errors="replace") as fh:
        src = fh.read()
    mode = how_to_run(src, rel)
    if mode == "skip":
        return {"status": "skip", "why": "no module-level work, no test functions"}
    env = dict(os.environ)
    # Prepend — see the same fix in migrate_module.run_tests. Replacing this
    # variable drops the vendored scipy/pytest directory and turns every
    # pytest-only test into a false ModuleNotFoundError failure.
    # `ca-simulation` is on the path deliberately: that directory now holds the
    # deprecation shims, and a test doing a bare `import ca_dirac` is supposed to
    # resolve through one (roadmap C3.4). Several tests compute their own
    # sys.path with an off-by-one `dirname` and point at directories that do not
    # exist (e.g. test_FG9 targets `<repo>/tests/ca-simulation`), so without this
    # they fail on the environment rather than on the physics — and they fail
    # that way at HEAD too, unmigrated. C7's registry is where that gets fixed.
    env["PYTHONPATH"] = os.pathsep.join(
        p for p in (os.path.join(_REPO, "src"),
                    os.path.join(_REPO, "ca-simulation"),
                    env.get("PYTHONPATH", "")) if p)
    argv = ([sys.executable, "-m", "pytest", rel, "-q"] if mode == "pytest"
            else [sys.executable, rel])
    t0 = time.time()
    try:
        p = subprocess.run(argv, cwd=_REPO, env=env, capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "mode": mode, "secs": timeout}
    tail = ((p.stdout or "") + (p.stderr or "")).strip().splitlines()[-6:]
    return {"status": "ok" if p.returncode == 0 else "fail", "mode": mode,
            "rc": p.returncode, "secs": round(time.time() - t0, 1),
            "tail": tail if p.returncode else []}


def main() -> int:
    budget = float(sys.argv[sys.argv.index("--budget") + 1]) \
        if "--budget" in sys.argv else 36.0
    timeout = int(sys.argv[sys.argv.index("--timeout") + 1]) \
        if "--timeout" in sys.argv else 100
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) \
        if "--workers" in sys.argv else 6

    m = load_manifest()
    recs = [r for r in m["modules"] if r["sector"] == SECTOR]
    tests = sorted({t for r in recs for t in r["tests"]})
    done = load()
    if "--retry-slow" in sys.argv:
        # One at a time, full timeout: several of these tests take 20-40 s of
        # single-threaded CPU and cannot finish three-abreast on a 4-core box.
        slow = [t for t in tests if done.get(t, {}).get("status") == "timeout"]
        n_at_once = int(sys.argv[sys.argv.index("--retry-slow") + 1])
        for t in slow[:n_at_once]:
            done[t] = one(t, timeout)
            print(f"  {done[t]['status']:<8s} {t}  {done[t].get('secs','')}")
            for line in done[t].get("tail", []):
                print("      " + line)
            with open(RESULTS, "w") as fh:
                json.dump(done, fh, indent=1)
        print(f"\n  {len([t for t in tests if done.get(t,{}).get('status')=='timeout'])}"
              f" still timing out")
        return 0
    todo = [t for t in tests if t not in done]
    print(f"{len(tests)} test(s); {len(done)} recorded; {len(todo)} left")
    if not todo:
        bad = {k: v for k, v in done.items()
               if v["status"] not in ("ok", "skip")}
        print("\nALL RECORDED. non-ok:", len(bad))
        for k, v in sorted(bad.items()):
            print(f"  {v['status'].upper():<8s} {k}")
            for line in v.get("tail", []):
                print("      " + line)
        return 1 if bad else 0

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {}
        for rel in todo:
            if time.time() - t0 > budget:
                break
            futs[pool.submit(one, rel, timeout)] = rel
        for fut, rel in futs.items():
            try:
                done[rel] = fut.result(timeout=max(5, timeout + 10))
            except Exception as e:                       # pragma: no cover
                done[rel] = {"status": "error", "why": repr(e)}
            s = done[rel]["status"]
            print(f"  {s:<8s} {rel}  {done[rel].get('secs', '')}")
            # Flush after every result: the sandbox kills this process at the
            # shell timeout, and a lost result means re-running a 90 s test.
            with open(RESULTS, "w") as fh:
                json.dump(done, fh, indent=1)
    with open(RESULTS, "w") as fh:
        json.dump(done, fh, indent=1)
    print(f"\n  recorded {len(done)}/{len(tests)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
