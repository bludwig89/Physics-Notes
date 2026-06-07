"""casim.engine.tier3 — non-unitary / heavy channels (migration-map Tier-3).

Two channel types that don't fit the unitary CA tick loop:

  * ``gauge_mc`` — a 3+1D SU(3) lattice-gauge **Monte-Carlo** channel
    (``forks/lgt_fork_A_mc``).  A "tick" is one Cabibbo–Marinari pseudo-
    heat-bath sweep (+ optional over-relaxation): a *stochastic* update that
    draws from the engine's checkpointed RNG.  Energy is not conserved; the
    observable is the mean plaquette / Wilson action / Polyakov correlator.
    Pure numpy — fully reproducible and sandbox-verifiable.

  * ``refraction_2d`` — dynamical **variable-c** Weyl propagation
    (``ca_curved``), a 2-D wave packet refracting across a c(x) step (the F64
    dielectric in time-domain).  Exact-unitary (Strang/Cayley) but SciPy-
    dependent, so it is imported lazily; verify it with
    ``tools/verify_tier3_gravity.py`` where SciPy is installed.
"""
from __future__ import annotations

import numpy as np

from .channel import Channel, register

ROOT3 = float(np.sqrt(3.0))


# ======================================================================
# 1. Lattice-gauge Monte-Carlo channel (F94, Option A)
# ======================================================================
@register
class GaugeMonteCarloChannel(Channel):
    """SU(3) Wilson lattice gauge theory updated by heat-bath Monte-Carlo.

    State: the link field ``U`` (shape (D, L,…,L, 3, 3)) plus the inverse
    coupling ``beta``.  ``step`` performs one heat-bath sweep using the engine
    RNG, so checkpoint/resume reproduces a Markov chain exactly.
    """
    type_name = "gauge_mc"
    label = "Gauge Monte Carlo"
    propagator = "monte-carlo"        # non-unitary, stochastic
    topologies = ("cubic",)

    def _mc(self):
        import lgt_fork_A_mc as mc
        return mc

    def init_state(self, lattice, rng):
        mc = self._mc()
        L = lattice.L
        D = int(self.config.get("D", 4))
        beta = float(self.config.get("beta", 5.8))
        start = self.config.get("start", "cold")
        if start == "hot":
            seed = int(rng.integers(0, 2 ** 31 - 1))
            U = mc.hot_links(L, D, seed=seed)
        else:
            U = mc.cold_links(L, D)
        return {"U": U, "beta": beta, "D": D,
                "n_or": int(self.config.get("n_or", 1))}

    def step(self, state, lattice, context=None, rng=None):
        mc = self._mc()
        U = mc.heatbath_sweep(state["U"], state["beta"], rng,
                              n_or=state["n_or"])
        return {"U": U, "beta": state["beta"], "D": state["D"],
                "n_or": state["n_or"]}

    def energy(self, state) -> float:
        # Mean plaquette (∈[0,1] roughly) — the standard MC order parameter.
        return float(self._mc().mean_plaquette(state["U"]))

    def observables(self, state, lattice) -> dict:
        mc = self._mc()
        return {
            "mean_plaquette": float(mc.mean_plaquette(state["U"])),
            "wilson_action": float(mc.wilson_action(state["U"], state["beta"])),
            "beta": float(state["beta"]),
        }

    def density_field(self, state):
        raise NotImplementedError(
            "gauge_mc has no 3-D scalar density for the point-cloud GUI; "
            "inspect mean_plaquette / Polyakov observables instead.")


# ======================================================================
# 2. Dynamical variable-c refraction channel (F64 time-domain, ca_curved)
# ======================================================================
@register
class DynamicalRefractionChannel(Channel):
    """A 2-D Weyl wave packet propagating through a c(x) step via the
    exact-unitary variable-c stepper (``ca_curved.weyl_step_2d_varc_strang``).
    The c-field is the F64 dielectric in the time domain; a packet crossing the
    boundary refracts by Snell's law.  SciPy-dependent (lazy import)."""
    type_name = "refraction_2d"
    label = "Refraction 2D"
    propagator = "variable-c"
    topologies = ("cubic",)

    def _cv(self):
        import ca_curved as cv
        return cv

    def init_state(self, lattice, rng):
        cv = self._cv()
        L = lattice.L
        c_left = float(self.config.get("c_left", 0.5))
        c_right = float(self.config.get("c_right", 0.25))
        k_in = tuple(self.config.get("k_in", (0.4, 0.2)))
        sigma = float(self.config.get("sigma", 6.0))
        x_start_frac = float(self.config.get("x_start_frac", 0.2))
        xs = np.arange(L)
        X, Y = np.meshgrid(xs, xs, indexing="ij")
        cx0 = int(x_start_frac * L)
        cy0 = L // 2
        envelope = np.exp(-((X - cx0) ** 2 + (Y - cy0) ** 2) / (2.0 * sigma ** 2))
        phase = np.exp(1j * (k_in[0] * X + k_in[1] * Y))
        phi = np.exp(1j * np.arctan2(k_in[1], k_in[0]))
        h = np.array([1.0, phi], dtype=complex) / np.sqrt(2.0)
        f = h[0] * envelope * phase
        g = h[1] * envelope * phase
        c_field = cv.make_c_field_step(L, c_left=c_left, c_right=c_right,
                                       x_boundary=L // 2, transition_width=2.0)
        return {"f": f, "g": g, "c_field": c_field,
                "n_sub": int(self.config.get("n_sub", 4))}

    def step(self, state, lattice, context=None, rng=None):
        cv = self._cv()
        f, g = cv.weyl_step_2d_varc_strang(
            state["f"], state["g"], state["c_field"], n_sub=state["n_sub"])
        return {"f": f, "g": g, "c_field": state["c_field"],
                "n_sub": state["n_sub"]}

    def energy(self, state) -> float:
        return float(np.sum(np.abs(state["f"]) ** 2 + np.abs(state["g"]) ** 2))

    def density_field(self, state):
        return np.asarray((np.abs(state["f"]) ** 2 + np.abs(state["g"]) ** 2).real)
