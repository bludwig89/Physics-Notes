"""Baseline provenance from the supersession ledger (added 2026-07-31).

The gap this closes
-------------------
A committed ``test-results/*.json`` is the accepted value, and C7's baseline diff
fails when a run stops reproducing it. But **a baseline that predates a model
change looks exactly like one that just broke.** Accepting a drift was a bare
``git add`` with no recorded reason — indistinguishable from accepting a
regression — and 7 of the 26 drift failures the C7.5 arming pass found are tests
whose physics a later finding deliberately replaced.

``docs/theory/supersessions.yaml`` already carries provenance for *code* and
*tests*. Artifacts were the missing third. A ``baselines:`` entry lives on the
supersession record whose physics moved, so the reason a number is out of date is
the same object that records what replaced it.

Three statuses, and only one of them changes a verdict
-----------------------------------------------------
``stale_by_design``  decided — the numbers predate this supersession, so a re-run
                     is *expected* to differ. The runner reports ``STALE``.
``candidate``        triage flagged it; **not** decided. The runner still reports
                     ``FAIL``. A candidate excuses nothing; it makes the queue
                     countable so nobody re-derives the triage.
``live``             re-blessed — the numbers are current and drift is a real
                     regression. ``accepted_by`` names the finding they encode.

That asymmetry is the whole design. If ``candidate`` suppressed failures, the
category would become a place to park inconvenient reds, which is the failure
mode P0.4 documented for test-level supersession claims (of 14 files an audit
called superseded, exactly one was).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable

import yaml

__all__ = [
    "BaselineRecord", "BASELINE_STATUSES", "load", "status_of",
    "stale_by_design", "candidates", "validate",
]

BASELINE_STATUSES = ("stale_by_design", "candidate", "live")

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
LEDGER_REL = os.path.join("docs", "theory", "supersessions.yaml")


@dataclass(frozen=True)
class BaselineRecord:
    """One artifact's provenance under one supersession record."""

    path: str                       # repo-relative artifact
    status: str
    record: str                     # ledger record id, e.g. S3-F64-dielectric-gravity
    reason: str = ""
    clears_by: str = ""
    committed: str = ""
    accepted_by: tuple[str, ...] = ()

    @property
    def suppresses_drift(self) -> bool:
        """Only a DECIDED entry changes a verdict. See the module docstring."""
        return self.status == "stale_by_design"


_CACHE: dict[str, BaselineRecord] = {}
_LOADED = False


def load(repo: str | None = None, force: bool = False) -> dict[str, BaselineRecord]:
    """{artifact path -> BaselineRecord}. Cached; never raises on a bad ledger."""
    global _LOADED
    if _LOADED and not force:
        return _CACHE
    _CACHE.clear()
    path = os.path.join(repo or _REPO, LEDGER_REL)
    try:
        with open(path, encoding="utf-8") as fh:
            led = yaml.safe_load(fh) or {}
    except (OSError, yaml.YAMLError):
        _LOADED = True
        return _CACHE
    for rec in led.get("supersessions") or []:
        for b in rec.get("baselines") or []:
            if not b.get("path"):
                continue
            _CACHE[b["path"]] = BaselineRecord(
                path=b["path"],
                status=str(b.get("status", "candidate")),
                record=str(rec.get("id", "")),
                reason=str(b.get("reason", "")),
                clears_by=str(b.get("clears_by", "")),
                committed=str(b.get("committed", "")),
                accepted_by=tuple(b.get("accepted_by") or ()),
            )
    _LOADED = True
    return _CACHE


def status_of(artifact: str, repo: str | None = None) -> BaselineRecord | None:
    return load(repo).get(artifact)


def stale_by_design(repo: str | None = None) -> list[BaselineRecord]:
    return [b for b in load(repo).values() if b.status == "stale_by_design"]


def candidates(repo: str | None = None) -> list[BaselineRecord]:
    return [b for b in load(repo).values() if b.status == "candidate"]


def all_stale(paths: Iterable[str], repo: str | None = None) -> bool:
    """True when EVERY given artifact is declared `stale_by_design`.

    Deliberately all, not any: a record whose drift spans one superseded artifact
    and one live one is still failing on the live one, and reporting the whole
    record as STALE would hide that.
    """
    paths = list(paths)
    return bool(paths) and all(
        (b := status_of(p, repo)) is not None and b.suppresses_drift
        for p in paths)


def validate(repo: str | None = None) -> list[str]:
    """Problems with the `baselines:` blocks. Empty list means well formed."""
    repo = repo or _REPO
    errs: list[str] = []
    for b in load(repo).values():
        if b.status not in BASELINE_STATUSES:
            errs.append(f"{b.path}: status {b.status!r} not in "
                        f"{list(BASELINE_STATUSES)}")
        if not os.path.exists(os.path.join(repo, b.path)):
            errs.append(f"{b.path}: artifact does not exist ({b.record})")
        if not b.reason.strip():
            errs.append(f"{b.path}: no reason given ({b.record})")
        if b.status in ("stale_by_design", "candidate") and not b.clears_by.strip():
            errs.append(f"{b.path}: status {b.status} with no `clears_by:` — "
                        f"an entry that cannot be cleared is a permanent excuse")
        if b.status == "live" and not b.accepted_by:
            errs.append(f"{b.path}: status live with no `accepted_by:` — a "
                        f"re-blessed baseline must name the finding it encodes")
    return errs
