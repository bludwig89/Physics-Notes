"""`code-index.md` from the module registry — roadmap C8.1 (**D11**).

The old index was a one-line docstring scrape over two directories. Everything
that made it *useful for context loading* had to be looked up elsewhere: which
sector a module belongs to, which findings it implements, whether anything
reaches it, which tests depend on it.

All four are registry fields now, so each row answers them:

* **Sector** — the engine subpackage (`casim.engine.registry`'s seven).
* **Findings** — from the migration manifest, carried into the registry.
* **Reach** — `driven` (in the transitive closure of a module that registers a
  channel), `entry-script`, `test-only`, `package-only`, `unreferenced`. This is
  P6's "67 of 106 kernels are unreachable" as a *field* rather than a survey.
* **Tests** — how many registry records (D9) depend on the module.

`ca-simulation/` still appears, as a shim column: 169 of its 171 files are now
`DeprecationWarning` shims onto `casim.engine`, and pretending they are gone
before C9 deletes them would make the index lie in the other direction.
"""
from __future__ import annotations

import os

from .common import HEADER_NOTE, esc, first_doc_line


def _test_dependents() -> dict[str, int]:
    """{module path -> number of test-registry records naming it}."""
    try:
        from casim.tests import registry as treg
    except Exception:                                        # pragma: no cover
        return {}
    counts: dict[str, int] = {}
    for r in treg.all_records():
        if r.module:
            counts[r.module] = counts.get(r.module, 0) + 1
    return counts


def _dotted(path: str) -> str:
    """`src/casim/engine/lattice/bcc.py` -> `casim.engine.lattice.bcc`."""
    p = path[len("src/"):] if path.startswith("src/") else path
    return p[:-3].replace("/", ".") if p.endswith(".py") else p.replace("/", ".")


def render(repo: str) -> tuple[str, str, int]:
    from casim.engine import registry as mreg

    dependents = _test_dependents()
    mods = mreg.all_modules()

    lines = [
        "# Code Index", "", HEADER_NOTE,
        "*One line per module. The `engine` section is generated from the "
        "**module registry** (`casim.engine.registry`, decision D11), so it "
        "carries sector, findings, exactness class, reachability and test "
        "dependents — the fields that make an index useful for deciding what to "
        "load. `Reach`: `driven` = in the transitive closure of a module that "
        "registers a channel; `entry-script` = has a `__main__` and is meant to "
        "be run; `test-only` / `package-only` / `unreferenced` mean what they "
        "say. `Tests` counts test-registry records (D9) that name the module as "
        "an entry point.*", "",
        "## `casim.engine` — the registered modules (D11)", "",
        "| Module | Sector | Status | Reach | Findings | Exactness | Tests | Summary |",
        "|--------|--------|--------|-------|----------|-----------|-------|---------|",
    ]
    for m in mods:
        full = os.path.join(repo, m.path)
        summary = first_doc_line(full) if os.path.exists(full) else ""
        n_tests = dependents.get(_dotted(m.path), 0)
        chans = f" ({len(m.reachable_from)} ch)" if m.reachable_from else ""
        lines.append(
            f"| `{m.name}` | {m.sector} | {m.status} | {m.reach}{chans} | "
            f"{' '.join(m.findings)} | {m.exactness or ''} | "
            f"{n_tests or ''} | {esc(summary)} |")

    n = len(mods)
    driven = sum(1 for m in mods if m.reach == "driven")
    lines += [
        "",
        f"*{n} registered module(s); **{driven} are channel-driven** "
        f"({100.0 * driven / n:.0f}%), which is P6's kernel-coverage question as "
        f"a value rather than a survey. Fork status: "
        f"{sum(1 for m in mods if m.status == 'fork_live')} `fork_live`, "
        f"{sum(1 for m in mods if m.status == 'fork_unclaimed')} "
        f"`fork_unclaimed` — a recorded negative result, not dead code.*",
        "",
    ]

    # ---- the package layer that is not migrated engine code ---------------
    pkg = os.path.join(repo, "src", "casim")
    lines += [
        "## `casim` — the package layer (CLI, suite, io, analysis, viz, gui)", "",
        "| Module | Summary |", "|--------|---------|",
    ]
    n_pkg = 0
    for entry in sorted(os.listdir(pkg)):
        sub = os.path.join(pkg, entry)
        if entry in ("engine", "__pycache__"):
            continue
        if os.path.isdir(sub) and os.path.exists(os.path.join(sub, "__init__.py")):
            lines.append(f"| `{entry}/` | "
                         f"{esc(first_doc_line(os.path.join(sub, '__init__.py')))} |")
            n_pkg += 1
        elif entry.endswith(".py") and entry != "__init__.py":
            lines.append(f"| `{entry}` | {esc(first_doc_line(sub))} |")
            n_pkg += 1

    # ---- the shim layer, until C9 -----------------------------------------
    sim = os.path.join(repo, "ca-simulation")
    shims, non_shims = 0, []
    if os.path.isdir(sim):
        for dirpath, dirnames, filenames in os.walk(sim):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in sorted(filenames):
                if not fn.endswith(".py"):
                    continue
                head = ""
                try:
                    with open(os.path.join(dirpath, fn), encoding="utf-8",
                              errors="replace") as fh:
                        head = fh.read(600)
                except OSError:
                    pass
                if "DeprecationWarning" in head and "has moved to" in head:
                    shims += 1
                else:
                    rel = os.path.relpath(os.path.join(dirpath, fn), sim)
                    non_shims.append(rel)
    lines += [
        "",
        "## `ca-simulation/` — the shim layer (deleted at C9)", "",
        f"**{shims} deprecation shim(s)** onto `casim.engine`, plus "
        f"{len(non_shims)} file(s) that are not shims: "
        + (", ".join(f"`{p}`" for p in sorted(non_shims)) if non_shims else "none")
        + ". Nothing new should import a `ca-simulation` path — "
          "`tools/check_shim_imports.py` is the gate for that (C3.4).",
        "",
    ]
    return "code-index.md", "\n".join(lines), n + n_pkg
