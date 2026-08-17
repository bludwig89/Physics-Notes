"""Scenario schema v2 — roadmap P4, finding F274.

*Created 2026-07-31 - 22:55.*

Every check has a real failure mode.  The load-bearing ones are the two P4
promised: a misspelled key is an error rather than a silent no-op, and every
shipped scenario validates strictly under v2 (so the migration is real, not a
version bump on files that would fail the schema).
"""
from __future__ import annotations

import glob
import os

import pytest

from casim.io import load_scenario, validate_scenario_file
from casim.io.schema import validate, validate_strict, ScenarioError
from casim.io.templates import resolve_extends, TEMPLATES


def _repo():
    here = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(os.path.dirname(here)))


def _base():
    return {"version": 2,
            "lattice": {"L": 16, "topology": "cubic"},
            "channels": [{"type": "photon_pair"}]}


# -- the two acceptance-gate checks -----------------------------------------
def test_every_shipped_scenario_validates_strictly():
    files = sorted(glob.glob(os.path.join(_repo(), "scenarios", "*.yaml")))
    assert files, "no scenarios found"
    bad = {f: validate_scenario_file(f) for f in files}
    bad = {f: e for f, e in bad.items() if e}
    assert not bad, f"{len(bad)} scenario(s) fail v2 validation: {bad}"


def test_misspelled_key_is_an_error():
    # top-level typo
    d = _base(); d["tickss"] = 40
    errs = validate(d)
    assert any("tickss" in e for e in errs)
    # lattice typo — the roadmap's `withd` case
    d = _base(); d["lattice"] = {"L": 16, "topology": "cubic", "withd": 1.5}
    assert any("withd" in e for e in validate(d))
    # and it raises through the strict loader
    with pytest.raises(ScenarioError):
        validate_strict(d, "x.yaml")


# -- type / vocabulary checks ----------------------------------------------
def test_bad_topology_and_channel_type_rejected():
    d = _base(); d["lattice"]["topology"] = "hex"
    assert any("topology" in e for e in validate(d))
    d = _base(); d["channels"] = [{"type": "not_a_channel"}]
    assert any("unknown channel type" in e for e in validate(d))


def test_dangling_channel_reference_is_caught():
    d = _base()
    d["observers"] = [{"type": "norm_conservation", "every": 5,
                       "channels": ["ghost"]}]
    assert any("ghost" in e for e in validate(d))


def test_float32_requires_explicit_optin():
    d = _base(); d["compute"] = {"dtype": "complex64"}
    assert any("1e-12 gate" in e for e in validate(d))
    d["compute"]["allow_float32"] = True
    assert not [e for e in validate(d) if "dtype" in e]


def test_valid_scenario_has_no_errors():
    assert validate(_base()) == []


# -- templates (extends) ----------------------------------------------------
def test_hydrogen_template_resolves_to_full_chain():
    d = {"version": 2, "extends": "hydrogen", "name": "h",
         "lattice": {"L": 16}}
    full = resolve_extends(d)
    names = [c.get("name", c["type"]) for c in full["channels"]]
    assert "electron" in names and "gluon_field" in names
    assert len(full["channels"]) == 7
    # override wins over the template's default L
    assert full["lattice"]["L"] == 16 and full["lattice"]["topology"] == "bcc"
    assert validate(full) == []


def test_unknown_template_is_an_error():
    with pytest.raises(KeyError):
        resolve_extends({"extends": "no_such_template"})


def test_shipped_hydrogen_scenario_is_short_and_valid():
    p = os.path.join(_repo(), "scenarios", "hydrogen.yaml")
    with open(p) as fh:
        n_lines = sum(1 for _ in fh)
    assert n_lines < 20, f"hydrogen.yaml is {n_lines} lines (P4 target: <20)"
    assert validate_scenario_file(p) == []


# -- events timeline --------------------------------------------------------
def test_timed_blockspin_event_fires_in_the_engine():
    from casim.engine import Simulation
    s = load_scenario(os.path.join(_repo(), "scenarios",
                                   "photon_pair_timed.yaml"))
    sim = Simulation.from_scenario(s)
    sim.run(40)
    ticks = [e["tick"] for e in sim.blockspin_events]
    assert 20 in ticks, f"block-spin event did not fire at tick 20: {ticks}"
    assert sim.lattice.L == 8  # 16 -> 8 after a factor-2 block-spin


def test_event_needs_a_known_action_and_a_time():
    d = _base()
    d["events"] = [{"do": "teleport", "at": 5}]
    assert any("teleport" in e for e in validate(d))
    d["events"] = [{"do": "blockspin"}]           # no `at`/`every`
    assert any("needs 'at'" in e for e in validate(d))


# -- v1 back-compat ---------------------------------------------------------
def test_v1_scenario_loads_with_deprecation_warning(tmp_path):
    p = tmp_path / "legacy.yaml"
    p.write_text("name: legacy\nlattice: {L: 8, topology: cubic}\n"
                 "channels:\n  - {type: photon_pair}\n")
    with pytest.warns(DeprecationWarning):
        data = load_scenario(str(p))
    assert data["name"] == "legacy"


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
