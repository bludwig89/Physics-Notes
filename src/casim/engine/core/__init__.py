"""casim.engine.core — the engine spine: clock, channels, observers, simulation.

The sector-neutral machinery every physics channel plugs into (F133/F134 wired
the block-spin RG in here as a first-class engine op). Migrated out of the flat
``casim.engine.*`` namespace into ``core/`` at roadmap phase C3 (D6 consolidation).
"""
from __future__ import annotations
