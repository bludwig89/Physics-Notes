"""casim.numerics.rng — seeded generators, one per consumer. Roadmap C1.1.

Today the engine has **one global RNG** (`engine/simulation.py:108`), so every
channel draws from the same stream. That has two consequences nobody chose:

  * adding, removing or reordering a channel changes the numbers every *other*
    channel sees, so a run is not reproducible across a config edit;
  * a Monte-Carlo channel and an initial-condition draw are correlated for no
    physical reason.

This module gives each consumer its own independent stream derived from one
run seed, via `numpy.random.SeedSequence`. Two named consumers can never
collide, and adding a third does not disturb the first two — which is the
property the P4 roadmap row "per-channel seeds" is actually asking for.

    from casim.numerics import rng
    rng.seed_run(7)
    g = rng.for_channel("gauge_mc")     # same stream every run, given seed 7
"""
from __future__ import annotations

import hashlib

import numpy as np

__all__ = ["seed_run", "run_seed", "for_channel", "spawn", "default"]

_ROOT: list = [np.random.SeedSequence(0)]
_SEED: list = [0]
_CACHE: dict[str, np.random.Generator] = {}


def seed_run(seed: int) -> None:
    """Set the run seed. Clears every derived stream."""
    _SEED[0] = int(seed)
    _ROOT[0] = np.random.SeedSequence(int(seed))
    _CACHE.clear()


def run_seed() -> int:
    return _SEED[0]


def _tag(name: str) -> int:
    """Stable 64-bit tag for a consumer name.

    `hash()` is deliberately NOT used: Python salts string hashing per process
    unless PYTHONHASHSEED is pinned, so it would give a different stream on
    every run — the exact opposite of what a seeded generator is for.
    """
    return int.from_bytes(hashlib.blake2b(name.encode(), digest_size=8).digest(),
                          "big")


def for_channel(name: str) -> np.random.Generator:
    """An independent generator for `name`, stable across runs and config edits."""
    g = _CACHE.get(name)
    if g is None:
        g = np.random.default_rng(
            np.random.SeedSequence(entropy=_SEED[0], spawn_key=(_tag(name),)))
        _CACHE[name] = g
    return g


def spawn(n: int) -> list[np.random.Generator]:
    """`n` independent generators from the run seed (for ensembles/sweeps)."""
    return [np.random.default_rng(s) for s in _ROOT[0].spawn(n)]


def default() -> np.random.Generator:
    """The unnamed stream. Prefer `for_channel` — this one is shared."""
    return for_channel("__default__")
