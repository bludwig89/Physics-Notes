#!/usr/bin/env python3
"""Plain (no-pytest) runner for the F206 certification battery + results dump."""
import os, sys, traceback
_REPO = "/sessions/jolly-upbeat-meitner/mnt/Physics Notes"
sys.path.insert(0, os.path.join(_REPO, "tests", "findings"))
import test_F206_internucleon_nn_binding as T

tests = [n for n in dir(T) if n.startswith("test_")]
results = {}
for n in sorted(tests):
    try:
        getattr(T, n)()
        results[n] = "PASS"
        print(f"{n}: PASS", flush=True)
    except Exception as e:
        results[n] = f"FAIL: {e}"
        print(f"{n}: FAIL: {e}", flush=True)
        traceback.print_exc()

p = T._dump_results()
print("results JSON ->", p, flush=True)
npass = sum(1 for v in results.values() if v == "PASS")
print(f"\n{npass}/{len(results)} PASS", flush=True)
