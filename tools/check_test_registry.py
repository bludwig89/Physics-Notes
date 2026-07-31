#!/usr/bin/env python3
"""C7 acceptance — the test registry is complete and valid (decision **D9**).

Three assertions, cheap enough for `make gate`:

  * **coverage** — every test file under tests/{casim,findings,priority,runners}
    has a record. A file with no record is a test the registry, `casim test`,
    and `casim index` (C8) cannot see.
  * **validity** — closed vocabularies, and no record claiming a real kind while
    having no way to fail.
  * **honesty** — the number still labelled `legacy_script` is printed on every
    run, so the debt is visible rather than inferred.

Exit 0 when the registry holds, 1 otherwise. The narrative version of these
checks lives in tests/casim/test_registry_integrity.py, which also asserts
pytest's scope equals the gate tier.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

from casim.tests import registry as treg  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="list the records still labelled legacy_script")
    args = ap.parse_args()

    missing = treg.check_coverage()
    errs = treg.validate_all(treg.all_records())
    c = treg.counts()

    if missing:
        print(f"[test-registry] {len(missing)} test file(s) with NO record:")
        for p in missing[:20]:
            print(f"    {p}")
        if len(missing) > 20:
            print(f"    … and {len(missing) - 20} more")
        print("[test-registry] run tools/gen_test_registry.py")
    if errs:
        print(f"[test-registry] {len(errs)} validation error(s):")
        for e in errs[:20]:
            print(f"    {e}")
        if len(errs) > 20:
            print(f"    … and {len(errs) - 20} more")

    if missing or errs:
        return 1

    print(f"[test-registry] {c['records']} record(s) cover "
          f"{c['files']} test file(s), all valid (D9).")
    print(f"    kinds: assertion={c['assertion']}  "
          f"result_dump={c['result_dump']}  scenario={c['scenario']}  "
          f"legacy_script={c['legacy_script']}")
    print(f"    tiers: gate={c['gate']}  archive={c['archive']}   "
          f"declared debt (no failure mode): {c['no_failure_mode']}")
    if args.verbose:
        for r in treg.all_records():
            if r.kind == "legacy_script":
                print(f"    debt: {r.id:44s} {r.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
