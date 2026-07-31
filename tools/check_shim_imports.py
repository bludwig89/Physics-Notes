#!/usr/bin/env python3
"""C3.4 shim-import discipline — no `src/casim/` code imports a migrated shim.

Every migration leaves a `DeprecationWarning` shim at the old `ca-simulation/`
path (and C3 leaves nine flat-engine shims at `src/casim/engine/<name>.py`).
Shims exist so *unmigrated tests* keep importing; they are removed wholesale at
C9. The acceptance rule for the package layer is stronger: **`src/casim/` has
already moved off the old paths**, so deleting every shim breaks nothing in
`src/`.

This check enforces exactly that, and only that. A file under `src/casim/` may
not import:

  * a migrated ``ca-simulation`` kernel by its old bare name (``import ca_bcc``,
    ``from ca_bcc import ...``) once that kernel's manifest record is stamped
    ``migrated:`` — i.e. once a new engine path exists to use instead; or
  * a flat-engine shim (``casim.engine.channel`` and the eight siblings), which
    moved to ``casim.engine.core.*`` at C3.

Deliberately **not** flagged, because these are the roadmap's intended
transitional state and clear at their own phase:

  * a not-yet-migrated ``ca-simulation`` kernel importing a sibling shim
    (it is not under ``src/casim/`` and moves at C4–C6); and
  * the flat-engine shim files themselves, which alias onto ``core`` on purpose.

The set of forbidden names is read from the manifest, so the check tightens
automatically as C4–C6 migrate more kernels.
"""
from __future__ import annotations

import os
import re
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC_PKG = os.path.join(_REPO, "src", "casim")
_MANIFEST = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")

# The nine flat-engine shims created at C3 (old flat name -> where it moved).
_FLAT = ("channel", "observers", "simulation", "coupled", "channels",
         "tier3", "spectral_matter", "blockspin", "manybody")
_FLAT_SHIM_FILES = {os.path.join(_SRC_PKG, "engine", f + ".py") for f in _FLAT}


def _migrated_kernel_names() -> set[str]:
    """Old bare module names of every kernel whose migration is stamped."""
    import yaml
    with open(_MANIFEST, encoding="utf-8") as fh:
        recs = (yaml.safe_load(fh) or {}).get("modules", [])
    names = set()
    for r in recs:
        if r.get("migrated"):
            base = os.path.basename(r["source"])
            if base.endswith(".py"):
                names.add(base[:-3])
    return names


def _violations() -> list[str]:
    kernels = _migrated_kernel_names()
    kernel_alt = sorted(kernels, key=len, reverse=True)
    out: list[str] = []
    for root, _dirs, files in os.walk(_SRC_PKG):
        if "__pycache__" in root:
            continue
        for fn in sorted(files):
            if not fn.endswith(".py"):
                continue
            path = os.path.join(root, fn)
            if path in _FLAT_SHIM_FILES:
                continue                                   # the shims themselves
            rel = os.path.relpath(path, _REPO)
            with open(path, encoding="utf-8") as fh:
                for i, line in enumerate(fh, 1):
                    s = line.rstrip("\n")
                    # flat-engine shim imports (absolute or relative)
                    m = re.search(
                        r"(?:from\s+(?:casim\.engine|\.+engine)\.([a-z_]+)\s+import"
                        r"|import\s+casim\.engine\.([a-z_]+)\b)", s)
                    if m:
                        name = m.group(1) or m.group(2)
                        if name in _FLAT:
                            out.append(f"{rel}:{i}: flat-engine shim "
                                       f"`engine.{name}` -> use `engine.core.{name}`"
                                       f"\n      {s.strip()}")
                            continue
                    # migrated ca-simulation kernel by old bare name
                    for k in kernel_alt:
                        if re.search(rf"^\s*(?:from\s+{re.escape(k)}\s+import"
                                     rf"|import\s+{re.escape(k)}\b)", s):
                            out.append(f"{rel}:{i}: migrated shim `{k}` "
                                       f"-> import from its casim.engine path"
                                       f"\n      {s.strip()}")
                            break
    return out


def main() -> int:
    v = _violations()
    if v:
        print(f"[shim-imports] {len(v)} src/casim import(s) still on a shim path (C3.4):")
        for line in v:
            print("    " + line)
        return 1
    print("[shim-imports] no src/casim file imports a migrated shim path (C3.4).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
