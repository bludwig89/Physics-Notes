"""Engine clock — roadmap P3.2, blocker B2, finding F268.

*Created 2026-07-31 - 23:40.*

Every check here has a real failure mode; none of them is a smoke test.  The
central assertion is the one the pre-P3.2 engine could not make: that a
scenario's channels either agree on how much physical time a tick is, or say out
loud that they do not.
"""
from __future__ import annotations

import numpy as np
import pytest

from casim.engine.core.channel import Channel, register, registered_channels
from casim.engine.core.clock import Clock, ClockError, reconcile
from casim.engine.core.simulation import LatticeSpec, Simulation


# ----------------------------------------------------------------------
# Minimal channels, defined once and reused. They count their own step()
# calls, which is how sub-cycling is measured rather than assumed.
# ----------------------------------------------------------------------
class _Counter(Channel):
    type_name = "_clock_counter"
    topologies = ("cubic", "bcc")

    def init_state(self, lattice, rng):
        return {"n": 0}

    def step(self, state, lattice, context=None, rng=None):
        return {"n": state["n"] + 1}

    def energy(self, state) -> float:
        return 1.0


class _Fine(_Counter):
    type_name = "_clock_fine"
    dt_native = 0.1


class _Rigid(_Counter):
    type_name = "_clock_rigid"
    dt_native = 0.25
    subcyclable = False


class _Agnostic(_Counter):
    type_name = "_clock_agnostic"
    dt_native = None


class _Fragile(_Counter):
    type_name = "_clock_fragile"
    dt_native = 0.25
    dt_max = 0.5


@pytest.fixture(autouse=True, scope="module")
def _register_probe_channels():
    """Register the probe channels for the duration of this module.

    In a fixture rather than at module scope on purpose: P1.3's
    ``import_time_work`` ratchet counts work performed at import, and the
    registry mutation here is exactly that — a side effect on global state that
    fires merely because something walked the package (``pkgutil``, pytest
    collection, coverage, ``casim index``). T9 resumes from a checkpoint, which
    goes through ``build_channel``, so the registration is genuinely needed —
    just not at import.
    """
    for c in (_Counter, _Fine, _Rigid, _Agnostic, _Fragile):
        if c.type_name not in registered_channels():
            register(c)
    yield


def _sim(channels, clock=None, L=4):
    return Simulation(LatticeSpec(L=L, dims=3, topology="cubic"),
                      channels, clock=clock, seed=0)


# ----------------------------------------------------------------------
# T1 — the ratio is exact, not floating point
# ----------------------------------------------------------------------
def test_T1_ratio_is_exact_decimal_not_binary():
    """1.0/0.1 must resolve to 10, not 9.999999999999998.

    This is the whole reason :func:`clock._exact` reads the decimal repr.  A
    float division here would leave a non-integer ratio and the reconciler would
    reject a scenario that is obviously fine — and the failure would look like a
    physics error, not a floating-point one.
    """
    ck = reconcile([_Counter("coarse"), _Fine("fine")], {"mode": "strict"})
    assert ck.dt == 1.0
    assert ck.timings["fine"].n_sub == 10
    assert ck.timings["coarse"].n_sub == 1
    # 0.2 and 0.5 are the other two values in the tree; both must divide 1.0.
    for dt, n in ((0.2, 5), (0.5, 2), (0.25, 4)):
        c = reconcile([_Counter("a"), _Counter("b", dt=dt)], {"mode": "strict"})
        assert c.timings["b"].n_sub == n, (dt, c.timings["b"].n_sub)


# ----------------------------------------------------------------------
# T2 — sub-cycling actually happens
# ----------------------------------------------------------------------
def test_T2_strict_mode_subcycles_the_fine_channel():
    """The fine channel takes 10 steps per engine tick, the coarse one 1.

    Measured by counting ``step()`` calls, so it cannot pass by declaration.
    """
    sim = _sim([_Counter("coarse"), _Fine("fine")], clock={"mode": "strict"})
    sim.step(7)
    assert sim.states["coarse"]["n"] == 7
    assert sim.states["fine"]["n"] == 70
    assert sim.clock.synchronous
    assert sim.clock.time == pytest.approx(7.0)


def test_T3_legacy_mode_is_bit_identical_to_the_old_engine():
    """``legacy`` forces n_sub=1 — the pre-P3.2 behaviour — but *records* it.

    This is what lets P3.2 land without moving a committed baseline. The
    assertion that matters is the second one: the desync must be visible.
    """
    sim = _sim([_Counter("coarse"), _Fine("fine")], clock={"mode": "legacy"})
    sim.step(7)
    assert sim.states["fine"]["n"] == 7        # not 70 — old behaviour
    assert not sim.clock.synchronous
    assert sim.clock.timings["fine"].desynchronised
    assert "fine" in sim.clock.to_dict()["desynchronised"]


def test_T4_auto_picks_legacy_only_when_it_must():
    """``auto`` is strict for a synchronous scenario and legacy otherwise."""
    sync = _sim([_Counter("a"), _Counter("b")])
    assert sync.clock.resolved_mode == "strict"
    assert sync.clock.synchronous

    desync = _sim([_Counter("a"), _Fine("b")])
    assert desync.clock.resolved_mode == "legacy"
    assert not desync.clock.synchronous


# ----------------------------------------------------------------------
# T5–T7 — the build-time errors. Each must name the offending channel.
# ----------------------------------------------------------------------
def test_T5_non_dividing_dt_is_a_build_error():
    """0.3 does not divide 1.0, so the scenario cannot be put on one clock."""
    with pytest.raises(ClockError, match="does not divide"):
        reconcile([_Counter("a"), _Counter("b", dt=0.3)], {"mode": "strict"})


def test_T6_a_channel_that_forbids_subcycling_says_so():
    """``subcyclable=False`` + a needed n_sub>1 is an error, not a silent lag."""
    with pytest.raises(ClockError, match="subcyclable=False"):
        reconcile([_Counter("a"), _Rigid("b")], {"mode": "strict"})
    # ...and it is fine when the whole engine runs at its step.
    ck = reconcile([_Rigid("b")], {"mode": "strict"})
    assert ck.dt == 0.25 and ck.timings["b"].n_sub == 1


def test_T7_a_config_may_lower_a_cfl_ceiling_but_never_raise_it():
    """Raising a stability limit from YAML is the silent-instability path."""
    ok = reconcile([_Fragile("a", dt_max=0.25)])           # lowering is allowed
    assert ok.timings["a"].dt_max == 0.25

    with pytest.raises(ClockError, match="never raise it"):  # raising is not
        reconcile([_Fragile("a", dt_max=2.0)])

    # A declared step above its own ceiling is refused...
    with pytest.raises(ClockError, match="exceeds its stability ceiling"):
        reconcile([_Fragile("a", dt=1.0)])
    # ...and so is a *global* dt above it, which is the case a single channel
    # cannot see for itself.
    with pytest.raises(ClockError, match="exceeds the stability ceiling"):
        reconcile([_Fragile("a")], {"dt": 2.0})


def test_T8_time_agnostic_channels_are_exempt_not_forced():
    """A compute-once channel steps once and takes no part in reconciliation."""
    sim = _sim([_Counter("a"), _Fine("f"), _Agnostic("mc")],
               clock={"mode": "strict"})
    sim.step(3)
    assert sim.states["mc"]["n"] == 3          # once per tick, never sub-cycled
    assert sim.states["f"]["n"] == 30
    assert sim.clock.timings["mc"].dt_native is None


# ----------------------------------------------------------------------
# T9 — round-trip. The blockspin bug this mirrors was silent-wrong.
# ----------------------------------------------------------------------
def test_T9_clock_survives_checkpoint_resume(tmp_path):
    """A resumed run must not silently revert to a different clock.

    Exactly the failure mode P2.6 found in ``blockspin_schedule``: the run
    completes, the results file looks normal, and the physics asked for did not
    happen. Asserted rather than trusted.
    """
    sim = _sim([_Counter("coarse"), _Fine("fine")], clock={"mode": "strict"})
    sim.step(3)
    p = sim.checkpoint(str(tmp_path / "ck.npz"))
    back = Simulation.resume(p)
    assert back.clock.resolved_mode == "strict"
    assert back.clock.n_sub("fine") == 10
    assert back.clock.tick == 3 == back.tick
    back.step(2)
    assert back.states["fine"]["n"] == 50      # 30 restored + 2*10
