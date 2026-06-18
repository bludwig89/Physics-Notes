"""casim.suite — the unified, user-run, grouped test suite.

Runs the whole repo's runnable tests in groups (battery / scenarios /
realspace), with periodic reporting, at a chosen scale tier
(``smoke`` | ``10x`` | ``100x`` | ``1000x``).  See ``casim test --help`` and
``scenarios/SUITE-GUIDE.md``.
"""
from __future__ import annotations

from .tiers import TIERS, DEFAULT_TIER, tier_names, plan_size, SizePlan
from .runner import (run_suite, build_plan, discover_scenarios,
                     DEFAULT_GROUPS, BATTERY_GROUPS, REALSPACE_SCENARIOS,
                     ItemResult, Reporter)

__all__ = [
    "TIERS", "DEFAULT_TIER", "tier_names", "plan_size", "SizePlan",
    "run_suite", "build_plan", "discover_scenarios",
    "DEFAULT_GROUPS", "BATTERY_GROUPS", "REALSPACE_SCENARIOS",
    "ItemResult", "Reporter",
]
