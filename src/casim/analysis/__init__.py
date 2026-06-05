"""casim.analysis — post-run analysis over result JSON.

Extracted from the inline diagnostics of the historical ``run_*`` scripts:
summarise norm drift, dispersion/unitarity residuals, and classify each
observer's exactness so reports (and eventually ``exactness-inventory.md``,
roadmap Phase F) can be generated rather than hand-maintained.
"""
from __future__ import annotations

from typing import Any, Dict, List


# Tolerances by exactness class.  "exact" quantities are algebraically zero;
# when evaluated numerically (closed form in float64) they sit at the round-off
# floor, so the gate accepts that floor rather than a literal 0.0.
TOL = {
    "exact": 1e-12,
    "machine-precision": 1e-10,
    "quantitative": None,   # no hard gate
}


def summarize(results: Dict[str, Any]) -> Dict[str, Any]:
    """Produce a compact, human-readable summary of a results dict."""
    out: Dict[str, Any] = {
        "name": results.get("name"),
        "ticks": results.get("ticks"),
        "lattice": results.get("lattice"),
        "channels": results.get("channels"),
        "observers": {},
    }
    for oname, ores in results.get("observers", {}).items():
        out["observers"][oname] = {
            "exactness": ores.get("exactness"),
            "summary": ores.get("summary", {}),
            "n_records": len(ores.get("records", [])),
        }
    return out


def exactness_rows(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Rows for an exactness table: (observer, channel, exactness, value, tol, pass)."""
    rows: List[Dict[str, Any]] = []
    for oname, ores in results.get("observers", {}).items():
        cls = ores.get("exactness", "quantitative")
        tol = TOL.get(cls)
        recs = ores.get("records", [])
        if not recs:
            continue
        last = recs[-1]
        chans = last.get("channels", {})
        if isinstance(chans, dict):
            for cname, val in chans.items():
                v = _scalarize(val)
                rows.append({
                    "observer": oname, "channel": cname, "exactness": cls,
                    "value": v, "tol": tol,
                    "pass": (tol is None) or (v is not None and v <= tol),
                })
    return rows


def _scalarize(val: Any):
    """Pull a representative scalar residual/drift out of a record entry."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, dict):
        for key in ("rel_drift", "residual", "rel_error", "value"):
            if key in val and isinstance(val[key], (int, float)):
                return float(val[key])
    return None


def format_table(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return "(no exactness rows)"
    hdr = f"{'observer':22s} {'channel':16s} {'class':18s} {'value':>12s}  pass"
    lines = [hdr, "-" * len(hdr)]
    for r in rows:
        v = "n/a" if r["value"] is None else f"{r['value']:.3e}"
        ok = "—" if r["tol"] is None else ("PASS" if r["pass"] else "FAIL")
        lines.append(f"{r['observer']:22s} {r['channel']:16s} "
                     f"{r['exactness']:18s} {v:>12s}  {ok}")
    return "\n".join(lines)


__all__ = ["TOL", "summarize", "exactness_rows", "format_table"]
