"""casim.index — CASIM owns the indexes (roadmap **C8**).

``casim index`` regenerates every generated index in the repo *from the
registries*, not from a filesystem scrape:

===========================  ==============================================
target                       source
===========================  ==============================================
``code-index.md``            module registry (D11) + the package/shim layers
``tests-index.md``           test registry (D9) — the declared mapping
``findings-index.md``        ``findings/`` + supersession ledger + D9
``docs-index.md``            prose scrape (no registry knows about prose)
``project-status-index.md``  prose scrape
``test-results/manifest.json`` result artifacts (the P1.4 builder, imported)
``docs/status/exactness-inventory.md``  artifacts ⨝ D9 (C8.4)
===========================  ==============================================

Two design rules that make ``--check`` meaningful:

1. **No volatile content in a generated file.** Every generated markdown file —
   the five ``*-index.md`` and the inventory's generated blocks — carries no
   timestamp, so ``--check`` is a byte comparison. The pre-C8 inventory
   generator stamped a date and had to strip it before comparing; dropping the
   stamp instead is simpler and makes idempotence checkable rather than
   approximated. Git records when. The one exception is ``manifest.json``, whose
   builder stamps ``generated`` and ``git_sha``; those two keys are excluded,
   exactly as ``gen_manifest.py --check`` excludes them.
2. **The manifest builder is imported, not re-implemented.** ``tools/
   gen_manifest.py`` is loaded by path and called, so ``casim index`` produces a
   byte-identical ``manifest.json`` and there is no second copy of the linking
   logic to drift. C5 set this precedent by importing ``migrate_module.py``'s
   templates rather than copying them.

``INDEX.md`` stays hand-maintained: it maps the directory layout, which no
registry knows.
"""
from __future__ import annotations

import importlib.util
import io
import os
import re
import sys
from contextlib import redirect_stdout

from .common import repo_root

__all__ = ["build", "check", "TARGETS", "repo_root"]

TARGETS = ("findings", "status", "tests", "code", "docs", "results",
           "exactness")

# Every generated markdown file is timestamp-free by construction, so `--check`
# is a byte comparison. The ONE exception is `test-results/manifest.json`:
#
#   * `generated` and `git_sha` — the two keys `tools/gen_manifest.py --check`
#     has always excluded;
#   * **`mtime`, per artifact** — added at C8 after `--check` went red on a
#     one-minute mtime difference. `gen_manifest.py --check` compared mtimes too,
#     which is why it reported "stale" after any test run that merely *touched*
#     an artifact without changing a number. mtime is a filesystem fact, not
#     content; the manifest already carries a numeric `fingerprint` for content,
#     and that is what should decide staleness.
_VOLATILE_JSON = re.compile(r'^\s*"(?:generated|git_sha|mtime)":.*$',
                            re.MULTILINE)


def _strip_stamp(text: str) -> str:
    return _VOLATILE_JSON.sub("", text)


def _gen_manifest_module(repo: str):
    """Import `tools/gen_manifest.py` as a module (see rule 2 above)."""
    path = os.path.join(repo, "tools", "gen_manifest.py")
    spec = importlib.util.spec_from_file_location("_casim_gen_manifest", path)
    if spec is None or spec.loader is None:                   # pragma: no cover
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_casim_gen_manifest"] = mod
    spec.loader.exec_module(mod)
    return mod


def _render(target: str, repo: str) -> tuple[str, str, int]:
    """(repo-relative path, full new text, entry count) for one target."""
    if target == "findings":
        from . import findings
        return findings.render(repo)
    if target == "status":
        from . import docs
        return docs.render_status(repo)
    if target == "tests":
        from . import tests
        return tests.render(repo)
    if target == "code":
        from . import code
        return code.render(repo)
    if target == "docs":
        from . import docs
        return docs.render_docs(repo)
    if target == "exactness":
        from . import exactness
        return exactness.render(repo)
    if target == "results":
        import json
        mod = _gen_manifest_module(repo)
        with redirect_stdout(io.StringIO()):                  # the builder is chatty
            payload = mod.build()
        text = json.dumps(payload, indent=1, sort_keys=True) + "\n"
        return os.path.join("test-results", "manifest.json"), text, \
            len(payload.get("tests", {}))
    raise ValueError(f"unknown index target {target!r}")


def build(targets: tuple[str, ...] = TARGETS, repo: str | None = None,
          check: bool = False) -> dict:
    """Regenerate (or, with `check=True`, compare) the generated indexes."""
    repo = repo or repo_root()
    out: dict = {"repo": repo, "targets": {}, "stale": [], "errors": []}
    for target in targets:
        try:
            rel, text, n = _render(target, repo)
        except Exception as exc:                              # noqa: BLE001
            out["errors"].append(f"{target}: {type(exc).__name__}: {exc}")
            continue
        full = os.path.join(repo, rel)
        current = None
        if os.path.exists(full):
            with open(full, encoding="utf-8") as fh:
                current = fh.read()
        changed = current is None or _strip_stamp(current) != _strip_stamp(text)
        out["targets"][target] = {"path": rel, "entries": n, "changed": changed}
        if check:
            if changed:
                out["stale"].append(rel)
            continue
        if changed:
            os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(text)

    # ---- the audits that make `casim index` able to say no -----------------
    from . import findings as _f
    from . import tests as _t
    from . import exactness as _e
    out["numbering"] = _f.audit_numbers(repo)
    out["tests_audit"] = _t.audit(repo)
    try:
        out["staleness"] = _e.staleness(repo)
    except Exception as exc:                                  # noqa: BLE001
        out["staleness"] = {"error": str(exc)}
    return out


def check(targets: tuple[str, ...] = TARGETS, repo: str | None = None) -> dict:
    return build(targets, repo, check=True)
