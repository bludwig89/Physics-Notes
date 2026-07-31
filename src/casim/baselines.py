"""Numeric drift detection for result artifacts — roadmap P1.2.

The problem this solves: of 344 test files, only 112 contain an `assert`. The
rest print `PASS`/`FAIL` tokens that the suite runner scrapes from stdout, or
they just build a dict and dump it. An exit-0 run with no token scores as
`RAN` — neither pass nor fail. **Roughly 70 tests have no failure mode by any
mechanism at all.**

The fix does not require editing 173 files. Those tests already write their
numbers to `test-results/*.json`, and those files are **already committed to
git**. So the accepted values are whatever is at HEAD, and a test acquires a
failure mode the moment we compare its fresh output against that — no new
storage, no duplicated baselines to drift out of sync, and the review workflow
for accepting a change is the one that already exists: look at the diff, commit
it deliberately.

What counts as drift is deliberately narrow:

  * only numbers are compared. Timestamps, paths, hostnames, durations and
    free text change every run and are not physics;
  * comparison is relative-with-absolute-floor, so a residual moving from
    1e-16 to 2e-16 is noise, while 1e-16 to 1e-6 is a finding;
  * a changed *structure* (a key appearing or vanishing) is reported
    separately from a changed *value*, because they usually mean different
    things — one is a code change, the other is a physics change.
"""
from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass
from typing import Any, Iterable

__all__ = [
    "numeric_leaves", "Delta", "compare", "git_show", "drift_report",
    "DEFAULT_REL", "DEFAULT_ABS", "MACHINE_FLOOR",
]

# A residual at the FFT floor bouncing between 1e-16 and 3e-16 is not news.
# A quantitative result moving in its 6th significant figure is.
DEFAULT_REL = 1e-9
DEFAULT_ABS = 1e-15

# The `machine` exactness class, quoted from casim.constants.EXACTNESS_CLASSES:
# "holds to the float/FFT round-off floor (<1e-12)".
#
# Two values that are BOTH below this cannot be told apart by the project's own
# standard, so reporting their difference as drift is incoherent — and it
# happens constantly, because a relative test at the round-off floor is
# meaningless: a residual moving 2.1e-14 -> 2.9e-14 is a 27% relative change
# and pure noise. C1 hit exactly this. Passing `floor=MACHINE_FLOOR` classifies
# such pairs as `floor` rather than `changed`.
#
# The default is 0.0, so nothing is weakened unless a caller opts in. Callers
# that opt in are comparing across environments (different FFT library, different
# CPU), where the last bits are expected to differ by construction.
MACHINE_FLOOR = 1e-12

# Keys whose values are environmental, not physical. Skipped entirely.
#
# Matched by regex rather than a literal set because these names carry prefixes
# in practice: the first run of this tool flagged `total_elapsed_s` as physics
# drift, which is exactly the kind of false positive that trains people to
# ignore a checker.
_VOLATILE_RE = __import__("re").compile(
    r"^(?:total_|avg_|mean_|max_|min_|sum_)*"
    r"(?:timestamp|date|datetime|generated(?:_at)?|created(?:_at)?|mtime"
    # `wall_seconds` slipped through the first version: the alternation had
    # `wall(_time|_s|_clock)?` but not `_seconds`, so a pure timing field was
    # reported as physics drift in C1.
    r"|wall(?:_time|_s|_sec|_secs|_seconds|_clock)?"
    r"|elapsed(?:_s|_sec|_secs|_seconds|_time)?|duration(?:_s|_seconds)?"
    r"|runtime(?:_s)?|cpu(?:_s|_time)?|t_wall|seconds|secs?"
    r"|host(?:name)?|user|platform|python(?:_version)?"
    r"|path|filepath|outfile|out_path|outdir|filename"
    r"|git_sha|commit|version)$",
    __import__("re").IGNORECASE)


def numeric_leaves(obj: Any, prefix: str = "") -> dict[str, float]:
    """Flatten to {dotted.path: number}, skipping volatile and non-numeric data.

    Booleans are included (as 0.0/1.0) — a gate flipping from pass to fail is
    exactly the kind of drift worth catching.
    """
    out: dict[str, float] = {}

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for k in sorted(node):
                if _VOLATILE_RE.match(str(k)):
                    continue
                walk(node[k], f"{path}.{k}" if path else str(k))
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")
        elif isinstance(node, bool):
            out[path] = 1.0 if node else 0.0
        elif isinstance(node, (int, float)):
            if isinstance(node, float) and (math.isnan(node) or math.isinf(node)):
                out[path] = float("nan") if math.isnan(node) else node
            else:
                out[path] = float(node)

    walk(obj, prefix)
    return out


@dataclass(frozen=True)
class Delta:
    path: str
    before: float | None
    after: float | None
    kind: str            # "changed" | "added" | "removed"
    rel: float | None = None

    def __str__(self) -> str:
        if self.kind == "added":
            return f"    + {self.path} = {self.after!r}"
        if self.kind == "removed":
            return f"    - {self.path} (was {self.before!r})"
        if self.kind == "floor":
            return (f"    . {self.path}: {self.before!r} -> {self.after!r}"
                    f"  (both below the machine floor — noise)")
        return (f"    ~ {self.path}: {self.before!r} -> {self.after!r}"
                f"  (rel {self.rel:.2e})" if self.rel is not None else
                f"    ~ {self.path}: {self.before!r} -> {self.after!r}")


def _close(a: float, b: float, rel: float, abs_: float) -> tuple[bool, float]:
    if math.isnan(a) and math.isnan(b):
        return True, 0.0
    if math.isnan(a) or math.isnan(b):
        return False, float("inf")
    diff = abs(a - b)
    scale = max(abs(a), abs(b))
    if diff <= abs_:
        return True, 0.0
    r = diff / scale if scale else float("inf")
    return r <= rel, r


def compare(before: Any, after: Any, rel: float = DEFAULT_REL,
            abs_: float = DEFAULT_ABS, floor: float = 0.0) -> list[Delta]:
    """Numeric deltas between two decoded result payloads.

    `floor` (default 0.0, i.e. off) classifies a pair whose *both* values sit
    below it as `kind="floor"` instead of `"changed"`. Pass
    ``floor=MACHINE_FLOOR`` when comparing across environments — a different
    FFT library or CPU changes the last bits by construction, and a relative
    test at the round-off floor turns that into a stream of 27%-looking
    "regressions" that are pure noise.

    `floor` deltas are still RETURNED, so a caller can print them; they simply
    carry a kind that says what they are. Nothing is silently dropped.
    """
    a = numeric_leaves(before)
    b = numeric_leaves(after)
    deltas: list[Delta] = []

    for path in sorted(set(a) | set(b)):
        if path not in b:
            deltas.append(Delta(path, a[path], None, "removed"))
        elif path not in a:
            deltas.append(Delta(path, None, b[path], "added"))
        else:
            ok, r = _close(a[path], b[path], rel, abs_)
            if ok:
                continue
            kind = ("floor" if floor > 0.0
                    and abs(a[path]) < floor and abs(b[path]) < floor
                    else "changed")
            deltas.append(Delta(path, a[path], b[path], kind, r))
    return deltas


def significant(deltas: Iterable["Delta"]) -> list["Delta"]:
    """Just the deltas that are not round-off-floor noise."""
    return [d for d in deltas if d.kind != "floor"]


def git_show(rel_path: str, ref: str = "HEAD", cwd: str | None = None) -> Any:
    """Decode `rel_path` as of `ref`. Returns None if untracked at that ref."""
    proc = subprocess.run(["git", "show", f"{ref}:{rel_path}"],
                          cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def drift_report(paths: Iterable[str], ref: str = "HEAD",
                 cwd: str | None = None, rel: float = DEFAULT_REL,
                 abs_: float = DEFAULT_ABS) -> dict[str, list[Delta]]:
    """Compare each working-tree result JSON against `ref`.

    Untracked files are skipped, not failed: a brand-new result has nothing to
    drift from, and it becomes a baseline the moment it is committed.
    """
    report: dict[str, list[Delta]] = {}
    for p in paths:
        before = git_show(p, ref, cwd)
        if before is None:
            continue
        try:
            with open(p if cwd is None else f"{cwd}/{p}", encoding="utf-8") as fh:
                after = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        deltas = compare(before, after, rel, abs_)
        if deltas:
            report[p] = deltas
    return report
