"""casim.particles.channel — particles as engine channels + sourced fields.

``ParticleChannel`` stacks a typed particle (a ``ParticleSpec`` wavepacket) on
the lattice.  Propagation and couplings call only audited ``ca-simulation``
kernels; this module is wiring, not physics:

  * propagation  — ``ca_bcc.weyl_step_3d_bcc`` (free) /
                   ``ca_wmu.covariant_weyl_step_3d_bcc`` (weak links)
  * weak loop    — ``ca_wmu.fermion_isospin_current`` + the existing
                   ``w_sourced`` channel + ``su2_expmap`` links (E2E B1)
  * EM source    — Noether U(1) Weyl current Q·ψ†σψ feeding
                   ``ca_charge_coupling.maxwell_curl_step`` (``photon_sourced``)
  * strong source— colour density q†T^a q (audited ``ca_strong.T_GEN``
                   generators) feeding ``ca_gluon.gluon_sourced_step_bcc``
                   (``gluon_sourced``)
  * gravity      — background F64 dielectric readout (potential energy,
                   local K at the packet centroid)

Coupling fidelity tiers (P2, 2026-06-05, see ``roadmap-particle-layer.md``):
weak / em / strong = coupled (two-way) · gravity = background.
P2 back-action kernels live in ``ca-simulation/ca_minimal_coupling.py``:
the U(1) Stueckelberg-form wrap (3D port of the audited F41/F42
``kinetic_half_step_chi_u1y`` architecture; exact gauge covariance, exact
unitarity) and the SU(3) site-local rotate-then-step (the audited SU(2)
``covariant_weyl_step_3d_bcc`` pattern).  The Coulomb sector accumulates the
A₀ Wilson-line angle α(x) from the audited open-boundary Poisson solver.
F27/F46 mass (P2c) uses the exact ``dirac_step_3d_bcc_splitstep`` for lepton
singlets; massive doublets/quarks are a later phase.

The force-applicability matrix is enforced at build time: requesting a
coupling the particle's charges forbid (e.g. a lepton → gluon) raises
``ValueError`` before the simulation is constructed.
"""
from __future__ import annotations

from typing import Dict

import numpy as np

from ..engine.channel import Channel, register
from ..engine.coupled import gaussian_packet, su2_expmap
from ..engine.observers import Observer, register_observer
from .spec import ParticleSpec, get_spec, doublet_specs, DOUBLETS

# P2 (2026-06-05): em and strong promoted from source-only to coupled —
# U(1) Stueckelberg wrap / SU(3) rotate-then-step (ca_minimal_coupling).
_TIERS = {"weak": "coupled", "em": "coupled",
          "strong": "coupled", "gravity": "background"}


# ----------------------------------------------------------------------
# Currents (bookkeeping over audited algebra)
# ----------------------------------------------------------------------
def weyl_vector_current(f, g):
    """Noether U(1) vector current of one Weyl species, J^i = ψ†σ^i ψ.

    Same σ-contraction as ``ca_wmu.fermion_current_isospin`` (the a=identity
    slot), written closed-form:  J^x = 2Re(f̄g), J^y = 2Im(f̄g),
    J^z = |f|²−|g|².  Returns (3, L, L, L) real.
    """
    fg = np.conj(f) * g
    return np.stack([2.0 * fg.real, 2.0 * fg.imag,
                     np.abs(f) ** 2 - np.abs(g) ** 2], axis=0)


def colour_charge_density(f_c, g_c):
    """Colour-octet charge density J^a_0 = q†T^a q summed over spin.

    ``f_c, g_c`` are colour-first (3, L, L, L) complex stacks.  Uses the
    audited Gell-Mann generators ``ca_strong.T_GEN`` and the same
    einsum contraction as ``ca_strong.noether_charge_density``.
    Returns (8, L, L, L) real.
    """
    from casim.fields.strong import ca_strong
    T = ca_strong.T_GEN                                   # (8, 3, 3)
    out = np.zeros((8,) + f_c.shape[1:], dtype=float)
    for comp in (f_c, g_c):
        # J^a = Σ_colour  conj(q_i) T^a_ij q_j
        Tq = np.einsum("aij,jxyz->aixyz", T, comp)
        out += np.real(np.einsum("ixyz,aixyz->axyz", np.conj(comp), Tq))
    return out


def _centroid(density, L):
    """Periodic-safe packet centroid via the angular mean per axis."""
    tot = float(density.sum())
    if tot <= 0.0:
        return np.zeros(3)
    ang = 2.0 * np.pi * np.arange(L) / L
    cen = np.empty(3)
    for ax in range(3):
        w = density.sum(axis=tuple(i for i in range(3) if i != ax))
        c = float(np.sum(w * np.cos(ang))) / tot
        s = float(np.sum(w * np.sin(ang))) / tot
        cen[ax] = (np.arctan2(s, c) % (2.0 * np.pi)) * L / (2.0 * np.pi)
    return cen


# ======================================================================
# ParticleChannel
# ======================================================================
@register
class ParticleChannel(Channel):
    """A typed particle wavepacket on the BCC lattice.

    Scenario config::

        {type: particle, name: electron, species: lepton_doublet_L,
         init: {center: [8,8,8], width: 1.5, k0: [0.5,0,0]},
         couplings: {weak: w_field, em: photon, gravity: gmass},
         sign: "+", eps: 0.05, colour: r}

    ``species`` is a registry singlet (``e_R``, ``u_L``, ...) or a left
    doublet (``lepton_doublet_L``, ``quark_doublet_L``).  ``couplings`` maps a
    force to the partner channel name; every requested force is validated
    against the spec's derived ``couples_to()`` matrix at build time.
    """
    type_name = "particle"
    propagator = "per-branch"
    topologies = ("bcc",)

    def __init__(self, name=None, **config):
        super().__init__(name=name, **config)
        species = config.get("species", "e_L")
        if species in DOUBLETS:
            self.specs = doublet_specs(species)
            self.is_doublet = True
        else:
            self.specs = (get_spec(species),)
            self.is_doublet = False
        self.species = species
        allowed = frozenset().union(*(s.couples_to() for s in self.specs))
        self.couplings: Dict[str, str] = dict(config.get("couplings", {}))
        for force, partner in self.couplings.items():
            if force not in _TIERS:
                raise ValueError(f"{self.name}: unknown force {force!r}")
            if force not in allowed:
                raise ValueError(
                    f"{self.name}: {species} does not couple to the "
                    f"{force} force (charges {[s.charges() for s in self.specs]}); "
                    f"allowed: {sorted(allowed)}")
        if "weak" in self.couplings and not self.is_doublet:
            raise ValueError(
                f"{self.name}: P1 wires the weak force through the W left-"
                f"doublet loop only; singlet Z/hypercharge coupling is P2. "
                f"Use a *_doublet_L species.")
        if "strong" in self.couplings and not all(s.colour for s in self.specs):
            raise ValueError(f"{self.name}: strong coupling needs colour")
        self.is_quark = all(s.kind == "quark" for s in self.specs)
        # P2c: F27/F46 mass via the exact BCC Dirac split-step — singlets only
        # for now (massive doublet/colour machinery is a later phase).
        self.mass = float(config.get("mass", 0.0))
        if self.mass:
            if self.is_doublet or self.is_quark:
                raise ValueError(
                    f"{self.name}: mass is wired for lepton singlets only "
                    f"(exact BCC Dirac step); massive doublets/quarks are a "
                    f"later phase")
            if not abs(self.mass) <= 1.0:
                raise ValueError(f"{self.name}: |mass| must be ≤ 1 (QCA "
                                 f"admissibility)")
        self.is_dirac = bool(self.mass)

    # ------------------------------------------------------------------
    def init_state(self, lattice, rng):
        L = lattice.L
        init = self.config.get("init", {}) or {}
        center = tuple(init.get("center", (L // 2, L // 2, L // 2)))
        width = float(init.get("width", 1.5))
        k0 = init.get("k0", None)
        k0 = tuple(k0) if k0 is not None else None

        if self.is_dirac:
            eta = gaussian_packet(L, center, width, k0=k0)
            st = {"eta_u": eta, "eta_d": np.zeros_like(eta),
                  "chi_u": np.zeros_like(eta), "chi_d": np.zeros_like(eta)}
        elif self.is_doublet:
            f_nu = gaussian_packet(L, center, width, k0=k0)
            c2 = (center[0] - 1, center[1], center[2])
            f_e = gaussian_packet(L, c2, width)
            st = {"f_nu": f_nu, "f_e": f_e,
                  "g_nu": np.zeros_like(f_nu), "g_e": np.zeros_like(f_e)}
        elif self.is_quark:
            psi = gaussian_packet(L, center, width, k0=k0)
            f = np.zeros((3, L, L, L), dtype=complex)
            idx = {"r": 0, "g": 1, "b": 2}[str(self.config.get("colour", "r"))]
            f[idx] = psi
            st = {"f": f, "g": np.zeros_like(f)}
        else:
            f = gaussian_packet(L, center, width, k0=k0)
            st = {"f": f, "g": np.zeros_like(f)}

        st["centroid_prev"] = _centroid(self._density(st), L)
        self._publish_currents(st)
        self._grav_readout(st, context=None)
        return st

    # ------------------------------------------------------------------
    def _density(self, state):
        if self.is_dirac:
            d = (np.abs(state["eta_u"]) ** 2 + np.abs(state["eta_d"]) ** 2
                 + np.abs(state["chi_u"]) ** 2 + np.abs(state["chi_d"]) ** 2)
        elif self.is_doublet:
            d = (np.abs(state["f_nu"]) ** 2 + np.abs(state["f_e"]) ** 2
                 + np.abs(state["g_nu"]) ** 2 + np.abs(state["g_e"]) ** 2)
        else:
            d = np.abs(state["f"]) ** 2 + np.abs(state["g"]) ** 2
            if d.ndim == 4:
                d = d.sum(axis=0)
        return d.real if np.iscomplexobj(d) else d

    def density_field(self, state):
        return np.asarray(self._density(state))

    # ------------------------------------------------------------------
    def _em_alpha(self, context):
        """Partner photon channel's accumulated U(1) angle α(x), or None."""
        if "em" not in self.couplings or not context:
            return None
        ps = context.get(self.couplings["em"])
        if ps is not None and "alpha" in ps and np.any(ps["alpha"]):
            return ps["alpha"]
        return None

    def step(self, state, lattice, context=None, rng=None):
        import ca_bcc
        import ca_minimal_coupling as mc
        sign = self.config.get("sign", "+")
        prev_centroid = _centroid(self._density(state), lattice.L)
        alpha = self._em_alpha(context)

        if self.is_dirac:
            q = float(self.specs[0].Q)
            a = alpha if alpha is not None else 0.0
            if alpha is not None and q:
                eu, ed, xu, xd = mc.u1_wrap_dirac_step_3d_bcc(
                    state["eta_u"], state["eta_d"],
                    state["chi_u"], state["chi_d"],
                    a, q, m=self.mass, sign=sign)
            else:
                from ca_dirac_bcc import dirac_step_3d_bcc_splitstep
                eu, ed, xu, xd = dirac_step_3d_bcc_splitstep(
                    state["eta_u"], state["eta_d"],
                    state["chi_u"], state["chi_d"],
                    m=self.mass, sign=sign)
            new = {"eta_u": eu, "eta_d": ed, "chi_u": xu, "chi_d": xd}
        elif self.is_doublet:
            # Optional U(1) wrap per isospin member (member charges differ);
            # the inner step is the audited SU(2)-covariant / free kernel.
            ph = {}
            if alpha is not None:
                for spec, k in zip(self.specs, ("nu", "e")):
                    ph[k] = (np.exp(-1j * float(spec.Q) * alpha)
                             if spec.Q != 0 else None)
            def _w(arr, k):       # phase-in
                p = ph.get(k)
                return arr if p is None else p * arr
            def _u(arr, k):       # phase-out
                p = ph.get(k)
                return arr if p is None else np.conj(p) * arr
            f_nu, f_e = _w(state["f_nu"], "nu"), _w(state["f_e"], "e")
            g_nu, g_e = _w(state["g_nu"], "nu"), _w(state["g_e"], "e")
            if "weak" in self.couplings and context:
                import ca_wmu
                eps = float(self.config.get("eps", 0.05))
                A = context[self.couplings["weak"]]["A"]
                U_a, U_b = su2_expmap(eps * A)
                f_nu, f_e, g_nu, g_e = ca_wmu.covariant_weyl_step_3d_bcc(
                    f_nu, f_e, g_nu, g_e, [(U_a, U_b)] * 8, sign=sign)
            else:
                f_nu, g_nu = ca_bcc.weyl_step_3d_bcc(f_nu, g_nu, sign=sign)
                f_e, g_e = ca_bcc.weyl_step_3d_bcc(f_e, g_e, sign=sign)
            new = {"f_nu": _u(f_nu, "nu"), "f_e": _u(f_e, "e"),
                   "g_nu": _u(g_nu, "nu"), "g_e": _u(g_e, "e")}
        elif self.is_quark:
            f_c, g_c = state["f"], state["g"]
            q = float(self.specs[0].Q)
            ph = (np.exp(-1j * q * alpha)
                  if (alpha is not None and q) else None)
            if ph is not None:
                f_c, g_c = ph * f_c, ph * g_c
            A_oct = None
            if "strong" in self.couplings and context:
                gs = context.get(self.couplings["strong"])
                if gs is not None and "A" in gs:
                    A_oct = gs["A"]
            eps_s = float(self.config.get("eps_strong", 0.05))
            f_c, g_c = mc.su3_rotate_weyl_step_3d_bcc(
                f_c, g_c, A_oct, eps=eps_s, sign=sign)
            if ph is not None:
                f_c, g_c = np.conj(ph) * f_c, np.conj(ph) * g_c
            new = {"f": f_c, "g": g_c}
        else:
            if alpha is not None and self.specs[0].Q != 0:
                f, g = mc.u1_wrap_weyl_step_3d_bcc(
                    state["f"], state["g"], alpha,
                    float(self.specs[0].Q), sign=sign)
            else:
                f, g = ca_bcc.weyl_step_3d_bcc(state["f"], state["g"],
                                               sign=sign)
            new = {"f": f, "g": g}

        new["centroid_prev"] = prev_centroid
        self._publish_currents(new)
        self._grav_readout(new, context)
        return new

    # ------------------------------------------------------------------
    def _publish_currents(self, state) -> None:
        """Write the source currents partner field channels read (state keys
        ``J_em`` / ``rho_em`` / ``J_colour``), per the active couplings."""
        if "em" in self.couplings:
            if self.is_dirac:
                q = float(self.specs[0].Q)
                # Dirac vector current: J^i = η†σ^iη − χ†σ^iχ; ρ = ψ†ψ.
                J = q * (weyl_vector_current(state["eta_u"], state["eta_d"])
                         - weyl_vector_current(state["chi_u"],
                                               state["chi_d"]))
                rho = q * self._density(state)
            elif self.is_doublet:
                J = np.zeros((3,) + state["f_nu"].shape)
                rho = np.zeros(state["f_nu"].shape)
                for spec, k in zip(self.specs, ("nu", "e")):
                    q = float(spec.Q)
                    if q:
                        J += q * weyl_vector_current(state[f"f_{k}"],
                                                     state[f"g_{k}"])
                        rho += q * (np.abs(state[f"f_{k}"]) ** 2
                                    + np.abs(state[f"g_{k}"]) ** 2)
            elif self.is_quark:
                q = float(self.specs[0].Q)
                J = np.zeros((3,) + state["f"].shape[1:])
                for c in range(3):
                    J += q * weyl_vector_current(state["f"][c], state["g"][c])
                rho = q * self._density(state)
            else:
                q = float(self.specs[0].Q)
                J = q * weyl_vector_current(state["f"], state["g"])
                rho = q * self._density(state)
            state["J_em"] = J
            state["rho_em"] = np.asarray(rho, float)
        if "strong" in self.couplings:
            state["J_colour"] = colour_charge_density(state["f"], state["g"])

    def _grav_readout(self, state, context) -> None:
        """Background F64 gravity: cache scalar readouts in state."""
        if "gravity" not in self.couplings or not context:
            state.setdefault("grav_potential", 0.0)
            state.setdefault("grav_K_centroid", 1.0)
            return
        gs = context.get(self.couplings["gravity"])
        if not gs or "phi" not in gs:
            return
        d = self._density(state)
        tot = float(d.sum()) or 1.0
        state["grav_potential"] = float(np.sum(d * gs["phi"]) / tot)
        c = np.rint(state["centroid_prev"]).astype(int) % d.shape[0]
        state["grav_K_centroid"] = float(gs["K"][c[0], c[1], c[2]])

    # ------------------------------------------------------------------
    def energy(self, state) -> float:
        return float(self._density(state).sum())

    def observables(self, state, lattice) -> dict:
        cen = _centroid(self._density(state), lattice.L)
        prev = np.asarray(state["centroid_prev"])
        # Periodic-safe per-tick displacement.
        vel = (cen - prev + lattice.L / 2.0) % lattice.L - lattice.L / 2.0
        out = {
            "species": self.species,
            "norm": self.energy(state),
            "centroid": [float(x) for x in cen],
            "velocity_per_tick": [float(v) for v in vel],
            "charges": [s.charges() for s in self.specs],
            "couplings": {f: {"partner": p, "tier": _TIERS[f]}
                          for f, p in self.couplings.items()},
        }
        if "gravity" in self.couplings:
            out["grav_potential"] = float(state.get("grav_potential", 0.0))
            out["grav_K_centroid"] = float(state.get("grav_K_centroid", 1.0))
        return out


# ======================================================================
# CompositeParticleChannel — a stacked multi-quark hadron (P4 / F71)
# ======================================================================
@register
class CompositeParticleChannel(Channel):
    """A composite hadron stacked from its constituent quark wavepackets.

    Scenario config::

        {type: composite, name: proton, composite: proton,
         init: {center: [8,8,8], width: 1.5, k0: [0.3,0,0]}}

    ``composite`` is a registry entry (``proton``, ``neutron``).  The three
    constituents are placed on the three colours (the single leading term of
    the F71 ``ε_abc`` singlet); each is propagated by the audited free BCC Weyl
    kernel.  Per F71 this is the **structural** hadron: exact aggregate quantum
    numbers and the colour-singlet invariant are reported, while the dynamical
    bound state (confining binding) is a later phase — flagged in the readout.
    """
    type_name = "composite"
    propagator = "per-branch"
    topologies = ("bcc",)

    def __init__(self, name=None, **config):
        super().__init__(name=name, **config)
        from .composite import get_composite
        self.composite = config.get("composite", "proton")
        self.spec = get_composite(self.composite)
        self.n = len(self.spec.constituents)

    def init_state(self, lattice, rng):
        L = lattice.L
        init = self.config.get("init", {}) or {}
        center = tuple(init.get("center", (L // 2, L // 2, L // 2)))
        width = float(init.get("width", 1.5))
        k0 = init.get("k0", None)
        k0 = tuple(k0) if k0 is not None else None
        # constituent c lives on colour c (leading ε_abc term)
        f = np.zeros((self.n, L, L, L), dtype=complex)
        for c in range(self.n):
            f[c] = gaussian_packet(L, center, width, k0=k0)
        st = {"f": f, "g": np.zeros_like(f)}
        st["centroid_prev"] = _centroid(self._density(st), L)
        return st

    def _density(self, state):
        d = (np.abs(state["f"]) ** 2 + np.abs(state["g"]) ** 2).sum(axis=0)
        return d.real if np.iscomplexobj(d) else d

    def density_field(self, state):
        return np.asarray(self._density(state))

    def step(self, state, lattice, context=None, rng=None):
        import ca_bcc
        sign = self.config.get("sign", "+")
        prev = _centroid(self._density(state), lattice.L)
        f, g = state["f"], state["g"]
        fn, gn = np.empty_like(f), np.empty_like(g)
        for c in range(self.n):
            fn[c], gn[c] = ca_bcc.weyl_step_3d_bcc(f[c], g[c], sign=sign)
        return {"f": fn, "g": gn, "centroid_prev": prev}

    def energy(self, state) -> float:
        return float(self._density(state).sum())

    def observables(self, state, lattice) -> dict:
        cen = _centroid(self._density(state), lattice.L)
        prev = np.asarray(state["centroid_prev"])
        vel = (cen - prev + lattice.L / 2.0) % lattice.L - lattice.L / 2.0
        return {
            "composite": self.composite,
            "content": self.spec.charges()["content"],
            "norm": self.energy(state),
            "centroid": [float(x) for x in cen],
            "velocity_per_tick": [float(v) for v in vel],
            "charges": self.spec.charges(),
            "colour_singlet": self.spec.is_colour_singlet,
            "colour_singlet_residual": self.spec.colour_singlet_residual(),
            "binding_tier": "structural",   # F71: dynamical bound state is later
        }


# ======================================================================
# Sourced field channels (read particle currents from context)
# ======================================================================
@register
class PhotonSourcedChannel(Channel):
    """Paired-photon (E,B) sourced by particle EM currents.

    Per tick: ``ca_charge_coupling.maxwell_curl_step(E, B, J=Σ J_em, dt)``
    where the sum runs over the particle channels named in ``sources``.
    The curl symbol is the model's BCC curl on the cubic FFT grid (same
    kernel and grid as the audited ``charge_photon`` channel), so this
    channel is registered for both topologies.
    """
    type_name = "photon_sourced"
    propagator = "even"
    topologies = ("cubic", "bcc")

    def init_state(self, lattice, rng):
        L = lattice.L
        return {"E": np.zeros((3, L, L, L)), "B": np.zeros((3, L, L, L)),
                "alpha": np.zeros((L, L, L))}

    def step(self, state, lattice, context=None, rng=None):
        import ca_charge_coupling as cc
        dt = float(self.config.get("dt", 0.1))
        g_em = float(self.config.get("g_em", 1.0))
        J, rho = None, None
        for src in self.config.get("sources", []):
            ps = (context or {}).get(src)
            if ps is not None and "J_em" in ps:
                J = ps["J_em"] if J is None else J + ps["J_em"]
            if ps is not None and "rho_em" in ps:
                rho = ps["rho_em"] if rho is None else rho + ps["rho_em"]
        if J is not None:
            J = g_em * J
        E, B = cc.maxwell_curl_step(state["E"], state["B"], J=J, dt=dt)
        # P2: Coulomb sector — accumulate the A₀ Wilson-line angle α(x).
        # φ_em = −φ_Poisson(ρ) so a positive charge sits in φ_em > 0 (like
        # charges repel under the wrap phase e^{-iqφdt}); the open-boundary
        # Poisson solver is the audited F64 kernel.
        alpha = state.get("alpha")
        if alpha is None:
            alpha = np.zeros(state["E"].shape[1:])
        if rho is not None and self.config.get("coulomb", True) \
                and np.any(rho):
            from casim.gravity import solve_poisson_3d_open
            g_c = float(self.config.get("g_coulomb", 1.0))
            phi_em = -solve_poisson_3d_open(rho, G_N=g_c / (4.0 * np.pi))
            alpha = alpha + phi_em * dt
        return {"E": E, "B": B, "alpha": alpha}

    def energy(self, state) -> float:
        return float(np.sum(state["E"] ** 2 + state["B"] ** 2))

    def observables(self, state, lattice) -> dict:
        return {"field_energy": self.energy(state),
                "alpha_max": float(np.max(np.abs(state.get(
                    "alpha", np.zeros(1)))))}


@register
class GluonSourcedChannel(Channel):
    """Colour-octet gluon field sourced by quark colour densities.

    Per tick: ``ca_gluon.gluon_sourced_step_bcc(E, B, J_a=Σ J_colour, g_lat)``
    — the audited F43 linearised Yang–Mills source step on the even BCC law
    (F91: colour coupling is branch-blind).
    """
    type_name = "gluon_sourced"
    propagator = "even"
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        L = lattice.L
        return {"E": np.zeros((8, L, L, L)), "B": np.zeros((8, L, L, L)),
                "A": np.zeros((8, L, L, L))}

    def step(self, state, lattice, context=None, rng=None):
        from casim.fields.strong import ca_gluon
        g_lat = float(self.config.get("g_lat", 0.5))
        dt = float(self.config.get("dt", 1.0))
        L = state["E"].shape[-1]
        J = np.zeros((8, L, L, L))
        for src in self.config.get("sources", []):
            ps = (context or {}).get(src)
            if ps is not None and "J_colour" in ps:
                J = J + ps["J_colour"]
        E, B = ca_gluon.gluon_sourced_step_bcc(
            state["E"], state["B"], J_a=J, dt=dt, g_lat=g_lat)
        # P2: accumulate the gluon potential (mirrors w_sourced's A += E),
        # consumed by quark ParticleChannels as SU(3) rotations.
        A = state.get("A")
        A = E if A is None else A + E
        return {"E": E, "B": B, "A": A}

    def energy(self, state) -> float:
        return float(np.sum(state["E"] ** 2 + state["B"] ** 2))

    def observables(self, state, lattice) -> dict:
        return {"field_energy": self.energy(state)}


# ======================================================================
# Sidebar feed: per-particle readouts every N ticks
# ======================================================================
@register_observer
class ParticleReadout(Observer):
    """Record each ParticleChannel's observables (norm, centroid, velocity,
    exact charges, active couplings + tier, gravity readouts).  This is the
    data feed for the GUI sidebar (roadmap P3)."""
    name = "particle_readout"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        rec = {"tick": sim.tick, "particles": {}}
        for cname, ch in sim.channels.items():
            if isinstance(ch, (ParticleChannel, CompositeParticleChannel)):
                rec["particles"][cname] = ch.observables(
                    sim.states[cname], sim.lattice)
        if rec["particles"]:
            self.records.append(rec)
