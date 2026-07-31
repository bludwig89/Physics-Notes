#!/usr/bin/env python3
"""C3.2 acceptance — every engine module has a registry record (decision D11).

Imports ``casim.engine.registry`` (which self-populates from the migration
manifest for migrated kernels and from a hand-declared list for the engine
spine) and asserts that every real module on disk under ``src/casim/engine/``
has a record. A file with no record is a module the registry — and therefore
``casim index`` at C8 — cannot see.

Exit 0 when coverage is complete, 1 (with the offending paths) otherwise.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

from casim.engine import registry as reg  # noqa: E402


def main() -> int:
    missing = reg.check_coverage()
    n = len(reg.MODULES)
    if missing:
        print(f"[module-registry] {len(missing)} engine module(s) with NO record:")
        for m in missing:
            print(f"    {m}")
        print(f"[module-registry] {n} registered; add records in "
              f"src/casim/engine/registry.py or migrate via the manifest.")
        return 1
    files = len(reg.engine_module_files())
    print(f"[module-registry] {n} modules registered; "
          f"{files} module file(s) on disk, all covered (D11).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
