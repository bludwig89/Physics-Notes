"""P2.6 — long-run operations: atomic, compressed, rotating, resumable.

The bug that made this file necessary
-------------------------------------
`Simulation.resume()` did not pass ``blockspin_schedule`` to the constructor, so
a resumed run had an **empty** schedule and skipped every remaining scheduled
$R_b$ event — while completing normally and writing a results file that looked
fine. A crash is cheap; a run that quietly does different physics than the
scenario asked for is not, and nothing in the suite could have caught it.

The other three items are the same class of problem one step removed: a
non-atomic checkpoint written from inside the tick loop means a kill during the
write destroys the *previous* good snapshot too, because the truncated file sits
at the name the resume path looks for.

So each of the four is asserted here rather than described in a docstring.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pytest

from casim.engine.core.simulation import Simulation
from casim.suite.tiers import plan_size

_SCENARIO = {
    "name": "p26_probe",
    "lattice": {"L": 8, "dims": 3, "topology": "cubic"},
    "channels": [{"type": "photon_pair", "name": "g"}],
    "observers": [],
    "seed": 3,
    "ticks": 20,
    "blockspin": [{"at": 4, "factor": 2}, {"at": 8, "factor": 2}],
}


def _sim(tmp_path, **kw):
    sc = dict(_SCENARIO)
    sc["checkpoint"] = {"every": 0, "dir": str(tmp_path)}
    sim = Simulation.from_scenario(sc)
    for k, v in kw.items():
        setattr(sim, k, v)
    return sim


# --------------------------------------------------------------------------
# 1. The schedule must survive a round-trip
# --------------------------------------------------------------------------
@pytest.mark.exact
def test_resume_restores_the_blockspin_schedule(tmp_path):
    """The P2.6 bug, asserted. An empty schedule after resume is silent-wrong."""
    sim = _sim(tmp_path)
    assert sim._blockspin_schedule == {4: 2, 8: 2}, "fixture is wrong"
    sim.step(2)
    path = sim.checkpoint(str(tmp_path / "p26_probe_t2.npz"))

    back = Simulation.resume(path)
    assert back._blockspin_schedule == sim._blockspin_schedule, (
        "resume() dropped the block-spin schedule — a resumed run would skip "
        "every remaining R_b event and still report success")
    assert back.tick == sim.tick


@pytest.mark.exact
def test_resume_tolerates_a_pre_p26_checkpoint(tmp_path):
    """A checkpoint written before P2.6 has no schedule key; it must still load.

    Refusing an old checkpoint would trade a silent bug for a loud one on files
    that already exist, which is not an improvement for anyone holding a
    week-old run.
    """
    sim = _sim(tmp_path)
    sim.step(1)
    path = sim.checkpoint(str(tmp_path / "old_t1.npz"))

    # Strip the key, the way a pre-P2.6 file would be.
    with np.load(path, allow_pickle=False) as data:
        arrays = {k: data[k] for k in data.files}
    meta = json.loads(bytes(arrays["__meta__"]).decode("utf-8"))
    meta.pop("blockspin_schedule", None)
    meta.pop("blockspin_events", None)
    arrays["__meta__"] = np.frombuffer(
        json.dumps(meta).encode("utf-8"), dtype=np.uint8)
    stripped = str(tmp_path / "stripped_t1.npz")
    with open(stripped, "wb") as fh:
        np.savez(fh, **arrays)

    back = Simulation.resume(stripped)
    assert back._blockspin_schedule == {}
    assert back.tick == 1


# --------------------------------------------------------------------------
# 2. Atomic
# --------------------------------------------------------------------------
@pytest.mark.exact
def test_checkpoint_is_atomic_and_leaves_no_temp(tmp_path):
    sim = _sim(tmp_path)
    sim.step(1)
    path = sim.checkpoint(str(tmp_path / "atomic_t1.npz"))
    assert os.path.exists(path)
    assert not [p for p in os.listdir(tmp_path) if ".tmp-" in p], (
        "a temp file survived a successful checkpoint")


@pytest.mark.exact
def test_failed_checkpoint_does_not_destroy_the_previous_one(tmp_path, monkeypatch):
    """The whole point of the atomic write.

    Simulates a kill mid-write by making the saver raise, then asserts the
    earlier good checkpoint is still loadable — which is exactly what the
    pre-P2.6 in-place `np.savez` could not promise.
    """
    sim = _sim(tmp_path)
    sim.step(1)
    good = sim.checkpoint(str(tmp_path / "keep_t1.npz"))
    before = os.path.getsize(good)

    import casim.engine.core.simulation as simmod

    def boom(*a, **kw):
        raise OSError("simulated kill during write")

    monkeypatch.setattr(simmod.np, "savez_compressed", boom)
    sim.step(1)
    with pytest.raises(OSError):
        sim.checkpoint(good)                    # same path as the good one

    assert os.path.getsize(good) == before, "the good checkpoint was clobbered"
    Simulation.resume(good)                     # and it still loads
    assert not [p for p in os.listdir(tmp_path) if ".tmp-" in p], (
        "a failed write left its temp file behind")


# --------------------------------------------------------------------------
# 3. Compressed
# --------------------------------------------------------------------------
@pytest.mark.exact
def test_compression_is_on_by_default_and_round_trips(tmp_path):
    """Compression must not change a single number.

    The ratio itself is deliberately NOT asserted: `savez_compressed` on a
    random-noise fixture barely helps (measured ~1.06x), while a smooth physical
    field compresses well. Asserting a ratio here would encode the fixture, not
    the behaviour.
    """
    sim = _sim(tmp_path)
    sim.step(2)
    assert sim.checkpoint_compress is True

    comp = sim.checkpoint(str(tmp_path / "comp_t2.npz"))
    sim.checkpoint_compress = False
    raw = sim.checkpoint(str(tmp_path / "raw_t2.npz"))

    a, b = Simulation.resume(comp), Simulation.resume(raw)
    for cname in a.states:
        for key, va in a.states[cname].items():
            vb = b.states[cname][key]
            if isinstance(va, np.ndarray):
                assert np.array_equal(va, vb), f"{cname}.{key} moved"
            else:
                assert va == vb


# --------------------------------------------------------------------------
# 4. Rotating
# --------------------------------------------------------------------------
@pytest.mark.exact
def test_rotation_keeps_the_newest_by_tick(tmp_path):
    """Rotation must sort by tick, not mtime.

    A resumed run rewrites old ticks with *new* mtimes, so mtime order would
    delete the newest snapshots — the opposite of the intent.
    """
    sim = _sim(tmp_path, checkpoint_dir=str(tmp_path), checkpoint_keep=3)
    sim.step(1)
    for tick in (50, 40, 30, 20, 10):           # deliberately newest-first
        sim.tick = tick
        sim.checkpoint(sim._auto_checkpoint_path())

    kept = sorted(p for p in os.listdir(tmp_path) if p.startswith("p26_probe_t"))
    assert kept == ["p26_probe_t30.npz", "p26_probe_t40.npz",
                    "p26_probe_t50.npz"], kept


@pytest.mark.exact
def test_rotation_never_touches_an_explicit_checkpoint(tmp_path):
    """An explicitly-named checkpoint is the user's, not the rotation's."""
    sim = _sim(tmp_path, checkpoint_dir=str(tmp_path), checkpoint_keep=1)
    sim.step(1)
    mine = sim.checkpoint(str(tmp_path / "please_keep_me.npz"))
    for tick in (10, 20, 30):
        sim.tick = tick
        sim.checkpoint(sim._auto_checkpoint_path())
    assert os.path.exists(mine), "rotation deleted an explicitly-named snapshot"


@pytest.mark.exact
def test_rotation_can_be_disabled(tmp_path):
    sim = _sim(tmp_path, checkpoint_dir=str(tmp_path), checkpoint_keep=0)
    sim.step(1)
    for tick in (10, 20, 30):
        sim.tick = tick
        sim.checkpoint(sim._auto_checkpoint_path())
    kept = [p for p in os.listdir(tmp_path) if p.startswith("p26_probe_t")]
    assert len(kept) == 3, kept


# --------------------------------------------------------------------------
# 5. The wall-time model
# --------------------------------------------------------------------------
@pytest.mark.quantitative
def test_wall_time_estimate_exists_and_grows_with_cost():
    """`--list` predicted memory but not duration; P2.6 added the estimate.

    Asserted as a *monotone* property, not a value: the estimate is calibrated
    off one machine's measured anchors, so pinning a number would make this test
    a hardware assertion. What must hold is that a bigger tier reads longer, and
    that a scenario with no anchor reports nothing rather than a guess.
    """
    from casim.io import load_scenario

    sc = load_scenario("scenarios/photon_pair.yaml")
    walls = [plan_size("photon_pair", sc, t).wall_seconds
             for t in ("smoke", "10x", "100x", "1000x")]
    assert all(w is not None for w in walls), walls
    assert walls == sorted(walls), f"estimate not monotone in tier: {walls}"
    assert walls[-1] > 100 * walls[0], "1000x should not read like 100x"


@pytest.mark.exact
def test_unanchored_scenario_reports_no_estimate_rather_than_a_guess():
    from casim.io import load_scenario

    sc = load_scenario("scenarios/proton_bag.yaml")
    plan = plan_size("proton_bag", sc, "100x")
    assert plan.wall_seconds is None
    assert plan.wall_human == "?"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
