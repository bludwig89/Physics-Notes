"""F326 — the "+1" closes: no second candidate generator to close it against.

F313 asked what else commutes with the update A. This asks where A, as the
ONLY candidate, comes from: BDPT uniqueness (cited, not re-derived) gives no
second solution to start from at (s, d) = (2, 3), and F313 sec.3-4's own
commutant closure (cited, not re-derived; sec.5/sec.8's WITHDRAWN content is
not reused) leaves no room for a second one to hide as a symmetry of the
first. What is genuinely new here is two grounding checks tying that argument
to the running engine, re-derived independently of
`casim.engine.lattice.time_single_generator` where practical.

  G1  (machine) THE ENGINE'S OWN CLOCK IS ONE INTEGER. Re-implemented here via
      a second, independent probe channel and a second Simulation instance
      (not imported from the module): `Clock` carries exactly one persisted
      time-state field; `Channel` exposes none; a channel running at twice
      the native resolution (`dt_native` half the global `dt`, forcing
      `n_sub == 2` under `clock={"mode": "strict"}`) is sub-stepped an EXACT,
      engine-determined multiple of the one outer tick count, not an
      independently drifting counter.
  G2  (machine) THE COUPLED TWO-BRANCH COMPOSITE IS ONE MATRIX, ITERATED. On
      the model's own s=4 composite at non-zero mass (F313 sec.9's own
      object, where BOTH chirality branches are genuinely coupled), n calls
      to the production stepper `dirac_step_3d_bcc_splitstep` reproduce
      `build_D_k_matrix(...) ** n` applied once to a single isolated Fourier
      mode, to machine precision -- for one SHARED n, not an independent one
      per branch. CAVEAT (review pass, 2026-08-20): the stepper and the
      matrix builder both bottom out in the same `_kinetic_n`/`bcc_unitary`
      primitives, so this machine-precision agreement is closer to a code
      self-consistency check than independent physical evidence against a
      second generator -- it mainly certifies the FFT round-trip and the
      stepper's own bookkeeping. What actually bears on "single generator"
      is that the stepper's signature carries no per-branch dt parameter,
      not the size of the residual.

Two declared controls (D9/H2), both verified RED:

  ``--param break_single_clock=True``   asserts the WRONG relation (that the
      finer channel's call count equals the outer tick count, i.e. n_sub=1)
      on a channel actually running at n_sub=2. Must fail -- if it passed, G1
      would not be able to detect a channel silently running on its own
      clock.
  ``--param break_composite_single_generator=True``  compares n engine ticks
      against n-1 applications of D_k, which must NOT agree. Must fail --
      otherwise G2's comparison would pass vacuously regardless of n.
"""
from __future__ import annotations

import dataclasses

from casim.numerics import xp

from casim.engine.core.clock import Clock
from casim.engine.core.channel import Channel
from casim.engine.core.simulation import Simulation, LatticeSpec
from casim.engine.lattice.geometry import make_kgrid_3d
from casim.engine.particles.dirac_bcc import (
    dirac_step_3d_bcc_splitstep, build_D_k_matrix,
)


class _ProbeChannelIndependent(Channel):
    """Re-implemented independently of the module's own `_ProbeChannel`."""
    type_name = "F326_test_probe"

    def __init__(self, name=None, dt_native=1.0, **config):
        super().__init__(name=name, dt_native=dt_native, **config)
        self.dt_native = dt_native

    def init_state(self, lattice, rng):
        return {"n": 0}

    def step(self, state, lattice, context=None, rng=None):
        return {"n": state["n"] + 1}

    def energy(self, state) -> float:
        return float(state["n"])


def check_G1_engine_single_clock(n_ticks=3, break_single_clock=False):
    """Independent re-derivation of the module's G1."""
    clock_fields = {f.name for f in dataclasses.fields(Clock)}
    assert clock_fields == {"dt", "mode", "resolved_mode", "timings", "tick"}, (
        f"Clock's field set changed shape: {clock_fields}")

    time_like = {"tick", "time", "clock", "n_sub", "elapsed"}
    stray = time_like & set(dir(Channel))
    assert stray == set(), f"Channel exposes its own time field(s): {stray}"

    lattice = LatticeSpec(L=4, dims=3, topology="cubic", c_lat=1.0 / (3 ** 0.5))
    fast = _ProbeChannelIndependent(name="fast326", dt_native=0.5)
    slow = _ProbeChannelIndependent(name="slow326", dt_native=1.0)
    sim = Simulation(lattice=lattice, channels=[slow, fast], seed=1,
                      name="F326-test-probe", clock={"mode": "strict"})
    sim.step(n_ticks)

    n_sub = sim.clock.n_sub("fast326")
    fast_n = sim.states["fast326"]["n"]
    slow_n = sim.states["slow326"]["n"]

    out = {"n_ticks": n_ticks, "sim_tick": sim.tick, "n_sub_fast": n_sub,
           "fast_n": fast_n, "slow_n": slow_n}
    assert sim.tick == n_ticks, out
    assert slow_n == sim.tick, (
        f"the native-resolution channel's own count drifted from tick: {out}")

    if break_single_clock:
        # Deliberately assert the wrong relation (n_sub == 1) on a channel
        # that is actually running at n_sub == 2 under strict mode.
        assert fast_n == n_ticks, (
            "CONTROL break_single_clock: asserting fast_n == n_ticks (i.e. "
            f"n_sub == 1), which must be false when the engine truly "
            f"sub-cycles: {out}")
    else:
        assert n_sub == 2, (
            f"expected the fast channel to sub-cycle at n_sub=2: {out}")
        assert fast_n == n_sub * n_ticks, (
            "the finer channel's own step count is not the deterministic "
            f"multiple n_sub * n_ticks the engine promises: {out}")
    return out


def check_G2_dirac_composite_single_generator(
        n=4, m=0.41, sign="+", direct_n_offset=0):
    """Independent re-derivation of the module's G2, at a DIFFERENT mass and
    Fourier mode than the module uses, and re-implementing the matrix power
    by hand rather than importing it.

    CAVEAT (review pass, 2026-08-20): both computations still call
    `build_D_k_matrix`/`dirac_step_3d_bcc_splitstep`, which share the same
    underlying primitives -- re-deriving the mode/mass does not make this an
    independent physical check, only an independent implementation of the
    same comparison. See the module's own G2 caveat.
    """
    assert 0.0 < abs(m) < 1.0
    L = 4
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    ix, iy, iz = (2, 1, 3)                      # a different mode than the module
    kx, ky, kz = float(KX[ix, iy, iz]), float(KY[ix, iy, iz]), float(KZ[ix, iy, iz])

    psi0 = xp.array([0.2 - 0.7j, 0.9 + 0.1j, -0.3 + 0.4j, 0.6 - 0.2j],
                     dtype=complex)

    D = build_D_k_matrix(kx, ky, kz, m, sign=sign)
    unit_res = float(xp.max(xp.abs(D.conj().T @ D - xp.eye(4, dtype=complex))))

    n_direct = max(n + direct_n_offset, 0)
    psi_direct = psi0.copy()
    for _ in range(n_direct):
        psi_direct = D @ psi_direct

    from casim.numerics import fft as _fft

    def _delta(amp):
        F = xp.zeros((L, L, L), dtype=complex)
        F[ix, iy, iz] = amp
        return _fft.ifftn(F)

    eu, ed, cu, cd = (_delta(psi0[0]), _delta(psi0[1]),
                      _delta(psi0[2]), _delta(psi0[3]))
    for _ in range(n):
        eu, ed, cu, cd = dirac_step_3d_bcc_splitstep(eu, ed, cu, cd,
                                                       m=m, dt=1.0, sign=sign)
    psi_engine = xp.array([_fft.fftn(eu)[ix, iy, iz], _fft.fftn(ed)[ix, iy, iz],
                            _fft.fftn(cu)[ix, iy, iz], _fft.fftn(cd)[ix, iy, iz]])

    residual = float(xp.max(xp.abs(psi_engine - psi_direct)))
    out = {"n": n, "n_direct": n_direct, "m": m, "unitarity_residual": unit_res,
           "residual": residual}
    assert unit_res < 1e-10, out
    if direct_n_offset == 0:
        assert residual < 1e-8, (
            "n engine ticks does not reproduce D_k^n applied once -- the "
            f"coupled composite is not a single generator: {out}")
    return out


def check_all(n_ticks=3, n_dirac=4, m=0.41,
              break_single_clock=False,
              break_composite_single_generator=False):
    out = {}
    if break_single_clock:
        try:
            check_G1_engine_single_clock(n_ticks=n_ticks, break_single_clock=True)
        except AssertionError as exc:
            raise AssertionError(f"[control break_single_clock RED, as required] {exc}")
        else:
            raise AssertionError(
                "CONTROL break_single_clock did not go red -- it cannot "
                "detect a channel silently running on its own clock")
    else:
        out["G1"] = check_G1_engine_single_clock(n_ticks=n_ticks)

    if break_composite_single_generator:
        baseline = check_G2_dirac_composite_single_generator(
            n=n_dirac, m=m, direct_n_offset=0)          # honest: agrees
        assert baseline["residual"] < 1e-8, (
            "control precondition failed -- the honest n=n comparison should "
            f"agree before the control deliberately breaks it: {baseline}")
        broken = check_G2_dirac_composite_single_generator(
            n=n_dirac, m=m, direct_n_offset=-1)         # n vs n-1: must disagree
        assert broken["residual"] > 1e-6, (
            "CONTROL break_composite_single_generator did not go red -- "
            f"comparing n ticks against n-1 applications of D_k must "
            f"disagree, or the comparison proves nothing about n: {broken}")
        raise AssertionError(
            "[control break_composite_single_generator RED, as required] "
            f"n={n_dirac} ticks vs n-1 applications of D_k: residual="
            f"{broken['residual']:.6g} (baseline residual="
            f"{baseline['residual']:.3g})")
    else:
        out["G2"] = check_G2_dirac_composite_single_generator(n=n_dirac, m=m)

    out["n_checks"] = 2
    return out


# --- no pytest surface -------------------------------------------------------
# `entry:` record; tests/casim/test_registry_integrity.py forbids both contracts.

if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, default=str))
