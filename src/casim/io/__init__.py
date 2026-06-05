"""casim.io — scenario loading and result writing.

A scenario is a YAML file; one driver + a committed config + seed reproduces a
historical run.  Results are written as JSON into ``test-results/`` (the schema
the repository already uses).
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict

import yaml


def load_scenario(path: str) -> Dict[str, Any]:
    """Load and lightly validate a scenario YAML file."""
    with open(path, "r") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"scenario {path!r} did not parse to a mapping")
    data.setdefault("name", os.path.splitext(os.path.basename(path))[0])
    data.setdefault("channels", [])
    data.setdefault("observers", [])
    data.setdefault("seed", 0)
    data.setdefault("ticks", 0)
    if not data["channels"]:
        raise ValueError(f"scenario {path!r} declares no channels")
    return data


def dump_scenario(scenario: Dict[str, Any], path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as fh:
        yaml.safe_dump(scenario, fh, sort_keys=False)


def write_results(results: Dict[str, Any], path: str) -> str:
    """Write a results dict to JSON, creating parent directories."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    return os.path.abspath(path)


def read_results(path: str) -> Dict[str, Any]:
    with open(path, "r") as fh:
        return json.load(fh)


__all__ = [
    "load_scenario", "dump_scenario",
    "write_results", "read_results",
]
