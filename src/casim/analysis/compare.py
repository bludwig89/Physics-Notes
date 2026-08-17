"""casim.analysis.compare — a user-facing diff of two run-result JSONs.

Roadmap P5.4: "No *user-facing* diff of two arbitrary runs. … Add a compare
view over the P1.4 manifest: pick two runs, see which observables moved."

This is the headless half of that view.  It deliberately does **not** reinvent
the numeric diff: it reuses :func:`casim.baselines.compare`, the same routine
behind ``tests/runner._diff_against_head`` (the ``result_dump`` failure mode)
and ``tools/check_result_drift.py``.  That routine already skips volatile keys
(timestamps, paths, durations), compares only numbers, and classifies deltas
that sit under the 1e-12 machine floor as noise rather than change — so a
user-facing compare inherits exactly the project's own notion of "moved".
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional


def _load(path_or_obj: Any) -> Any:
    if isinstance(path_or_obj, str):
        with open(path_or_obj, encoding="utf-8") as fh:
            return json.load(fh)
    return path_or_obj


def compare_runs(a: Any, b: Any, *, floor: Optional[float] = None,
                 strict_floor: bool = False) -> Dict[str, Any]:
    """Compare two result payloads (paths or dicts) and report what moved.

    Returns ``{n_significant, n_floor, significant: [...], floor: [...],
    identical: bool}`` where each delta is ``{path, before, after, kind,
    rel}``.  ``floor`` defaults to the project machine floor (1e-12); pass
    ``strict_floor=True`` to treat every bit-level difference as significant.
    """
    from casim.baselines import compare, significant, MACHINE_FLOOR

    before = _load(a)
    after = _load(b)
    f = 0.0 if strict_floor else (MACHINE_FLOOR if floor is None else floor)
    all_deltas = compare(before, after, floor=f)
    sig = significant(all_deltas)
    below = [d for d in all_deltas if d.kind == "floor"]

    def _d(delta) -> Dict[str, Any]:
        return {"path": delta.path, "before": delta.before,
                "after": delta.after, "kind": delta.kind,
                "rel": getattr(delta, "rel", None)}

    return {
        "n_significant": len(sig),
        "n_floor": len(below),
        "significant": [_d(d) for d in sig],
        "floor": [_d(d) for d in below],
        "identical": not sig and not below,
    }


def format_comparison(a_name: str, b_name: str, result: Dict[str, Any],
                      limit: int = 40) -> str:
    """Render :func:`compare_runs` output as a compact table."""
    lines: List[str] = [f"compare  A={a_name}  B={b_name}"]
    sig = result["significant"]
    if not sig and not result["floor"]:
        lines.append("  identical (no numeric observable moved)")
        return "\n".join(lines)
    if sig:
        lines.append(f"\n  {result['n_significant']} observable(s) moved:")
        lines.append(f"    {'observable':44s} {'A':>14s} {'B':>14s}   rel")
        lines.append("    " + "-" * 78)
        for d in sig[:limit]:
            bef = "—" if d["before"] is None else f"{d['before']:.6g}"
            aft = "—" if d["after"] is None else f"{d['after']:.6g}"
            rel = "" if d["rel"] is None else f"{d['rel']:.2e}"
            lines.append(f"    {d['path'][:44]:44s} {bef:>14s} {aft:>14s}   "
                         f"{rel}")
        if len(sig) > limit:
            lines.append(f"    … and {len(sig) - limit} more")
    if result["floor"]:
        lines.append(f"\n  {result['n_floor']} sub-floor delta(s) "
                     f"(<1e-12 both sides) — noise, not drift")
    return "\n".join(lines)


__all__ = ["compare_runs", "format_comparison"]
