"""casim.analysis.inventory — auto-generate the casim exactness inventory.

Roadmap Phase F: rather than hand-maintaining an exactness table, run the
canonical checks (``casim.verify``) and emit a markdown table classifying each
by exactness (exact / machine-precision / quantitative), its residual, and
pass/fail vs tolerance.

Writes to a *casim-scoped* file (``test-results/casim-exactness-inventory.md``)
so it never clobbers the repository's large hand-maintained
``docs/status/exactness-inventory.md``.
"""
from __future__ import annotations

import datetime as _dt
import os
from typing import List

from ..verify import run_all, Check

DEFAULT_PATH = "test-results/casim-exactness-inventory.md"


def _stamp() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d - %H:%M")


def build_markdown(checks: List[Check]) -> str:
    n_pass = sum(1 for c in checks if c.passed)
    lines = [
        "# casim exactness inventory (auto-generated)",
        "",
        f"_Generated {_stamp()} by `casim inventory` "
        f"(casim.analysis.inventory). {n_pass}/{len(checks)} checks pass._",
        "",
        "Auto-generated from `casim.verify.run_all()`; do not edit by hand. "
        "This is scoped to the `casim` engine and does **not** replace the "
        "repository's hand-maintained `docs/status/exactness-inventory.md`.",
        "",
        "| check | channel | class | residual | tolerance | pass |",
        "|---|---|---|---|---|---|",
    ]
    for c in checks:
        tol = "—" if c.tol is None else f"{c.tol:.0e}"
        lines.append(
            f"| {c.name} | {c.channel} | {c.exactness} | {c.residual:.3e} | "
            f"{tol} | {'✅' if c.passed else '❌'} |")
    lines += [
        "",
        "## Classes",
        "",
        "- **exact** — algebraically zero; evaluated in float64 it sits at the "
        "round-off floor (gate 1e-12).",
        "- **machine-precision** — converges to the FFT/float floor (gate 1e-10).",
        "- **quantitative** — a measured physical agreement with its own gate "
        "(e.g. eikonal-vs-GR < 1%).",
        "",
    ]
    return "\n".join(lines)


def generate(path: str = DEFAULT_PATH) -> str:
    checks = run_all()
    md = build_markdown(checks)
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w") as fh:
        fh.write(md)
    return os.path.abspath(path)


if __name__ == "__main__":
    p = generate()
    print(f"wrote {p}")
