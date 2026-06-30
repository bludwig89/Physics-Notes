"""casim.particles.channel — particles as engine channels + sourced fields.

``ParticleChannel`` stacks a typed particle (a ``ParticleSpec`` wavepacket) on
the lattice.  Propagation and couplings call only audited ``ca-simulation``
kernels; this module is wiring, not physics:

  * propagation  — ``ca_bcc.weyl_step_3d_bcc`` (free) /
                   ``ca_wmu.covariant_weyl_step_3d_bcc`` (weak links)
  * weak loop    — ``ca_wmu.fermion_isospin_current`` + the existing
                   ``w_sourced`` channel + ``su2_expmap`` links (E2E B1)
  * EM source    — Noether U(1) Weyl current Q·ψ†σψ feeding the even
                   rotation-law photon ``ca_photon_pair.photon_step_spectral``
                   + source kick (``photon_sourced``)
  * strong source— colour density q†T^a q (audited ``ca_strong.T_GEN``
                   generators) feeding ``ca_gluon.gluon_sourced_step_bcc``
                   (``gluon_sourced``)
  * gravity      — F64 dielectric, **two-way** since the mainlining
                   (2026-06-06, audit B.2 #1): massive Dirac singlets read the
                   field through the F62 rest-leg lapse mix (√A(x)·m around
                   the audited spectral step, ``ca_gravity.lapse_mix_half``)
                   and source it per F106 via the dynamic
                   ``gravity_dielectric`` channel's ``sources:`` map; scalar
                   readouts (potential energy, local K at the packet centroid)
                   remain for all species.  Kinetic-leg c_eff variation
                   (massless deflection) stays fork-level — the spectral BCC
                   kernels are homogeneous.

Coupling fidelity tiers (P2, 2026-06-05, see ``roadmap-particle-layer.md``):
weak / em / strong = coupled (two-way) · gravity = coupled (massive Dirac
singlets, rest leg; background readout otherwise).
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

from typing import Any, Dict

import numpy as np

from ..engine.channel import Channel, register
from ..engine.coupled import gaussian_packet, su2_expmap
from ..engine.observers import Observer, register_observer
from .spec import ParticleSpec, get_spec, doublet_specs, DOUBLETS

# P2 (2026-06-05): em and strong promoted from source-only to coupled —
# U(1) Stueckelberg wrap / SU(3) rotate-then-step (ca_minimal_coupling).
# F64-mainline (2026-06-06): gravity promoted background → coupled (massive
# Dirac singlets: F62 lapse mix back-read + F106 T⁰⁰ sourcing).
_TIERS = {"weak": "coupled", "em": "coupled",
          "strong": "coupled", "gravity": "coupled"}


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
    label = "Particle"
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

    def _confine_potential(self, lattice, context):
        """F86/F70 linear confining string field

            V_i(x) = Σ_{j≠i} (σ/2) · |x − r_j|     (periodic minimal image)

        where r_j are the start-of-tick centroids of the colour-singlet
        partners (the pairwise Δ-string; matches F122's per-pair (σ/2)r
        Cornell confining term).  σ is the string tension (F70 area law /
        F86 dual-superconductor σ=2πv²n).  Returned as a real (L,L,L) array
        (or None when no ``confine`` block / partners).

        How it is APPLIED decides whether it confines (the U1 physics):
          * Lorentz-**scalar** (added to the Dirac mass, ``confine.mode:
            scalar``, the default) → MIT-bag / dual-superconductor
            confinement: it BINDS even a (near-)massless fermion.
          * **vector** (a phase kick e^{-iV dt} on a Weyl spinor,
            ``confine.mode: vector``) → Klein paradox: it only redirects,
            never slows, and does NOT bind (the documented null).
        """
        cfg = self.config.get("confine")
        if not cfg or context is None:
            return None
        # LIVE flux-tube field (F137): read the scalar bag mass S(x) from a
        # partner colour_bag channel instead of building a geometric string.
        if cfg.get("field"):
            ps = context.get(cfg["field"])
            if ps is not None and "S" in ps and np.any(ps["S"]):
                return np.asarray(ps["S"])
            return None
        sigma = float(cfg.get("sigma", 0.0))
        partners = cfg.get("partners", [])
        if sigma == 0.0 or not partners:
            return None
        L = lattice.L
        idx = np.indices((L, L, L))

        def _dist_to(r):
            d2 = np.zeros((L, L, L))
            for ax in range(3):
                dax = (idx[ax] - r[ax] + L / 2.0) % L - L / 2.0
                d2 = d2 + dax ** 2
            return np.sqrt(d2)

        anchor = cfg.get("anchor", "pairwise")
        if anchor == "com":
            # Y-string: a single conical well V=σ|x−R_cm| toward the colour-
            # singlet centre of mass (the string junction).  Full inward
            # gradient σ everywhere — the strong-binding geometry.
            cens = [np.asarray(context[p]["centroid_prev"], float)
                    for p in partners
                    if context.get(p) is not None
                    and "centroid_prev" in context[p]]
            if not cens:
                return None
            R = np.mean(cens, axis=0)
            return sigma * _dist_to(R)
        # pairwise Δ-string: V_i = Σ_{j≠i}(σ/2)|x−r_j| (matches F122 per-pair)
        V = np.zeros((L, L, L))
        n_used = 0
        for pname in partners:
            if pname == self.name:
                continue
            ps = context.get(pname)
            if ps is None or "centroid_prev" not in ps:
                continue
            V = V + 0.5 * sigma * _dist_to(np.asarray(ps["centroid_prev"],
                                                       float))
            n_used += 1
        return V if n_used else None

    def step(self, state, lattice, context=None, rng=None):
        import ca_bcc
        import ca_minimal_coupling as mc
        sign = self.config.get("sign", "+")
        prev_centroid = _centroid(self._density(state), lattice.L)
        alpha = self._em_alpha(context)

        if self.is_dirac:
            q = float(self.specs[0].Q)
            a = alpha if alpha is not None else 0.0
            # F64/F62 two-way gravity (massive singlets): rest-leg lapse mix
            # √A(x)·m around the audited spectral step (Strang; exactly
            # unitary; bit-identical when no gravity partner / K ≡ 1).
            sqrtA = self._grav_sqrtA(context)
            eu, ed, xu, xd = (state["eta_u"], state["eta_d"],
                              state["chi_u"], state["chi_d"])
            if sqrtA is not None:
                from casim.gravity import lapse_mix_half
                eu, ed, xu, xd = lapse_mix_half(eu, ed, xu, xd,
                                                sqrtA, self.mass)
            # F86/F70 confining string as a Lorentz-SCALAR potential (U1):
            # m_eff(x) = m + Σ_{j≠i}(σ/2)|x−r_j| added to the Dirac mass.
            # A scalar linear well confines (MIT bag / F86 dielectric ε_c→0 =
            # infinite effective mass in the vacuum) where the vector kick
            # Klein-tunnels.  Steps with the variable-mass BCC Dirac kernel.
            V_conf = (self._confine_potential(lattice, context)
                      if self.config.get("confine", {}).get(
                          "mode", "scalar") != "vector" else None)
            if V_conf is not None:
                from ca_dirac_bcc import dirac_step_3d_bcc_varm_splitstep
                m_field = self.mass + V_conf
                eu, ed, xu, xd = dirac_step_3d_bcc_varm_splitstep(
                    eu, ed, xu, xd, m_field=m_field, m0=self.mass, sign=sign)
                if alpha is not None and q:        # EM as a minimal-coupling phase
                    ph = np.exp(-1j * q * a)
                    eu, ed, xu, xd = ph * eu, ph * ed, ph * xu, ph * xd
            elif alpha is not None and q:
                eu, ed, xu, xd = mc.u1_wrap_dirac_step_3d_bcc(
                    eu, ed, xu, xd, a, q, m=self.mass, sign=sign)
            else:
                from ca_dirac_bcc import dirac_step_3d_bcc_splitstep
                eu, ed, xu, xd = dirac_step_3d_bcc_splitstep(
                    eu, ed, xu, xd, m=self.mass, sign=sign)
            if sqrtA is not None:
                from casim.gravity import lapse_mix_half
                eu, ed, xu, xd = lapse_mix_half(eu, ed, xu, xd,
                                                sqrtA, self.mass)
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
            # F86/F70 confining string (U1) applied to a Weyl spinor as a
            # VECTOR (phase) kick e^{-iV dt}: exactly unitary, but a vector
            # potential Klein-tunnels and does NOT bind a massless quark —
            # the documented null (the scalar/mass coupling on the Dirac path
            # is what confines).  Off unless confine.mode == "vector".
            V = self._confine_potential(lattice, context)
            if V is not None and \
                    self.config.get("confine", {}).get("mode") == "vector":
                dt_c = float(self.config["confine"].get("dt", 1.0))
                cphase = np.exp(-1j * V * dt_c)
                f_c = f_c * cphase[None, ...]
                g_c = g_c * cphase[None, ...]
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

    def _grav_sqrtA(self, context):
        """Lapse field √A = K^{-1/2} from the gravity partner, or None.

        Used by the massive-Dirac two-way coupling (F62 rest-leg mix).  Returns
        None when no gravity partner is wired, the partner has no K yet, or
        the field is exactly flat (K ≡ 1) — keeping the no-gravity path
        bit-identical."""
        if "gravity" not in self.couplings or not self.mass or not context:
            return None
        gs = context.get(self.couplings["gravity"])
        if not gs or "K" not in gs:
            return None
        K = gs["K"]
        if np.all(K == 1.0):
            return None
        return 1.0 / np.sqrt(K)

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
# ColourDiracQuarkChannel — a massive SU(3) colour-triplet Dirac quark
# (roadmap-unified-real-space.md U3, Part 1): the F135 scalar confining
# string applied to a genuine colour quark, with the SU(3) gluon loop live.
# ======================================================================
@register
class ColourDiracQuarkChannel(ParticleChannel):
    """A massive colour-triplet **Dirac** quark on the BCC lattice.

    State is a 4-component Dirac spinor (η↑,η↓,χ↑,χ↓) stacked on 3 colours,
    each component an (3,L,L,L) complex array.  Per tick:
      1. SU(3) colour rotation from the gluon octet potential A (the F43
         loop, ``su3`` via ``_su3_expmap_field``) — applied to every spinor
         component's colour axis;
      2. the **variable-mass** BCC Dirac step per colour with the F135
         Lorentz-scalar confining mass m_eff(x)=m+Σ(σ/2)|x−r| (``confine``
         block; colour-blind);
      3. the U(1) EM minimal-coupling phase if charged.

    It publishes ``J_colour`` (sources the gluon) and ``J_em``/``rho_em``
    (sources the photon), closing both loops on a real colour quark.  Unlike
    the Weyl ``particle`` quark, this one is massive, so the scalar string
    binds it (F135) — vector/Weyl confinement Klein-tunnels.
    """
    type_name = "quark_dirac"
    label = "Colour Dirac Quark"
    propagator = "per-branch"
    topologies = ("bcc",)

    def __init__(self, name=None, **config):
        Channel.__init__(self, name=name, **config)
        flavour = config.get("species", "u_L")
        self.specs = (get_spec(flavour),)
        if self.specs[0].kind != "quark":
            raise ValueError(f"{self.name}: quark_dirac needs a quark species")
        self.species = flavour
        self.is_doublet = False
        self.is_quark = True
        self.is_dirac = True
        self.mass = float(config.get("mass", 0.3))
        if abs(self.mass) > 1.0:
            raise ValueError(f"{self.name}: |mass| must be ≤ 1 (QCA)")
        self.colour = str(config.get("colour", "r"))
        allowed = self.specs[0].couples_to()
        self.couplings = dict(config.get("couplings", {}))
        for force in self.couplings:
            if force not in _TIERS:
                raise ValueError(f"{self.name}: unknown force {force!r}")
            if force == "weak":
                raise ValueError(f"{self.name}: weak coupling is doublet-only")
            if force not in allowed:
                raise ValueError(
                    f"{self.name}: {flavour} does not couple to {force}")

    def init_state(self, lattice, rng):
        L = lattice.L
        init = self.config.get("init", {}) or {}
        center = tuple(init.get("center", (L // 2, L // 2, L // 2)))
        width = float(init.get("width", 1.5))
        k0 = init.get("k0", None)
        k0 = tuple(k0) if k0 is not None else None
        idx = {"r": 0, "g": 1, "b": 2}[self.colour]
        pkt = gaussian_packet(L, center, width, k0=k0)
        z = np.zeros((3, L, L, L), dtype=complex)
        eu = z.copy()
        eu[idx] = pkt
        st = {"eta_u": eu, "eta_d": z.copy(),
              "chi_u": z.copy(), "chi_d": z.copy()}
        st["centroid_prev"] = _centroid(self._density(st), L)
        self._publish_currents(st)
        self._grav_readout(st, context=None)
        return st

    def _density(self, state):
        d = (np.abs(state["eta_u"]) ** 2 + np.abs(state["eta_d"]) ** 2
             + np.abs(state["chi_u"]) ** 2 + np.abs(state["chi_d"]) ** 2)
        d = d.sum(axis=0)
        return d.real if np.iscomplexobj(d) else d

    def density_field(self, state):
        return np.asarray(self._density(state))

    def step(self, state, lattice, context=None, rng=None):
        from ca_dirac_bcc import (dirac_step_3d_bcc_varm_splitstep,
                                  dirac_step_3d_bcc_splitstep)
        sign = self.config.get("sign", "+")
        prev = _centroid(self._density(state), lattice.L)
        eu = state["eta_u"].copy(); ed = state["eta_d"].copy()
        xu = state["chi_u"].copy(); xd = state["chi_d"].copy()

        # (1) SU(3) colour rotation from the gluon octet potential A
        if "strong" in self.couplings and context:
            gs = context.get(self.couplings["strong"])
            if gs is not None and "A" in gs and np.any(gs["A"]):
                from ca_gluon import _su3_expmap_field
                eps = float(self.config.get("eps_strong", 0.05))
                V = _su3_expmap_field(eps * gs["A"])
                eu = np.einsum('xyzij,jxyz->ixyz', V, eu)
                ed = np.einsum('xyzij,jxyz->ixyz', V, ed)
                xu = np.einsum('xyzij,jxyz->ixyz', V, xu)
                xd = np.einsum('xyzij,jxyz->ixyz', V, xd)

        # (2) variable-mass Dirac kinetic step per colour (scalar confinement)
        V_conf = (self._confine_potential(lattice, context)
                  if self.config.get("confine", {}).get(
                      "mode", "scalar") != "vector" else None)
        if V_conf is not None:
            m_field = self.mass + V_conf
            dt_c = float(self.config.get("confine", {}).get("dt", 1.0))
            for c in range(3):
                eu[c], ed[c], xu[c], xd[c] = dirac_step_3d_bcc_varm_splitstep(
                    eu[c], ed[c], xu[c], xd[c],
                    m_field=m_field, m0=self.mass, dt=dt_c, sign=sign)
        else:
            for c in range(3):
                eu[c], ed[c], xu[c], xd[c] = dirac_step_3d_bcc_splitstep(
                    eu[c], ed[c], xu[c], xd[c], m=self.mass, sign=sign)

        # (3) U(1) EM minimal-coupling phase
        alpha = self._em_alpha(context)
        q = float(self.specs[0].Q)
        if alpha is not None and q:
            ph = np.exp(-1j * q * alpha)[None, ...]
            eu, ed, xu, xd = ph * eu, ph * ed, ph * xu, ph * xd

        new = {"eta_u": eu, "eta_d": ed, "chi_u": xu, "chi_d": xd,
               "centroid_prev": prev}
        self._publish_currents(new)
        self._grav_readout(new, context)
        return new

    def _publish_currents(self, state) -> None:
        if "em" in self.couplings:
            q = float(self.specs[0].Q)
            J = np.zeros((3,) + state["eta_u"].shape[1:])
            for c in range(3):
                J += q * (weyl_vector_current(state["eta_u"][c],
                                              state["eta_d"][c])
                          - weyl_vector_current(state["chi_u"][c],
                                                state["chi_d"][c]))
            state["J_em"] = J
            state["rho_em"] = q * self._density(state)
        if "strong" in self.couplings:
            state["J_colour"] = (
                colour_charge_density(state["eta_u"], state["eta_d"])
                + colour_charge_density(state["chi_u"], state["chi_d"]))

    def observables(self, state, lattice) -> dict:
        out = ParticleChannel.observables(self, state, lattice)
        out["colour"] = self.colour
        out["mass"] = self.mass
        return out


# ======================================================================
# NonRelElectronChannel — the non-relativistic atomic electron (U2/U3).
# ----------------------------------------------------------------------
# The atomic electron is non-relativistic (v ~ αc ~ 0.007 c): the Dirac
# split-step kernel brings in the Klein/zitterbewegung dynamics that a bound
# atomic electron does NOT have, and on a tractable relativistic lattice a
# vector Coulomb well Klein-tunnels rather than binds (the F135 vector null;
# the Dirac–Coulomb Zα→1 collapse).  F125 already supplies the relativistic
# fine structure (Lamb shift, 2p split) from the *spectral* Dirac–Coulomb
# solve.  For the real-time *binding* demonstration (U2) and the neutral atom
# (U3) the correct, stable description is the Schrödinger evolution of the
# electron orbital in the proton's Coulomb potential, integrated by an
# exactly-unitary split-step (potential half-kick · spectral kinetic · half-
# kick).  This is the atomic-scale, non-relativistic complement to the Dirac
# matter channels — explicitly labelled so, not a relativistic claim.
# ======================================================================
@register
class NonRelElectronChannel(Channel):
    """Non-relativistic electron orbital ψ(x) bound by a Coulomb potential.

    Evolves  i ∂_t ψ = (−∇²/2m + V)ψ  with V(x) = q·φ_em(x), where
    φ_em = −Poisson(ρ_src) is the *same* open-boundary electrostatic
    convention the ``photon_sourced`` channel uses (F64 kernel).  ρ_src is the
    summed ``rho_em`` of the channels named in ``sources`` (the proton's
    quarks, self-consistently each tick) plus an optional static
    ``external_charge`` (the U2 de-risk: a fixed point charge).

    Integrator: Strang split-step ``e^{−iVdt/2} · F⁻¹ e^{−ik²dt/2m} F ·
    e^{−iVdt/2}`` — exactly unitary (norm conserved to the FFT floor).

    With ``init: {ground_state: true}`` the orbital is relaxed to the
    instantaneous ground state of V by imaginary-time propagation on the
    first step (so it starts stationary — the clean bound-vs-free control is
    then unambiguous).  Otherwise a Gaussian ``init: {center, width}``.

    Publishes ``rho_em`` = q·\|ψ\|² and the probability current ``J_em`` so it
    sources the photon and is counted in the neutrality / loop-liveness
    readout.  Charge defaults to the ``e_L`` electron (q = −1); set ``charge``
    to override.
    """
    type_name = "nr_electron"
    label = "Non-Rel Electron"
    propagator = "non-rel"          # Schrödinger; outside the F91 classes
    topologies = ("cubic", "bcc")

    def __init__(self, name=None, **config):
        super().__init__(name=name, **config)
        self.mass = float(config.get("mass", 1.0))
        self.charge = float(config.get("charge", -1.0))
        self.g_coulomb = float(config.get("g_coulomb", 1.0))
        self.dt = float(config.get("dt", 0.2))
        self.sources = list(config.get("sources", []))
        self.external_charge = config.get("external_charge")

    # --- potential assembly ------------------------------------------------
    def _source_density(self, lattice, context, state):
        """ρ_src(x): summed partner rho_em + static external charge (or None)."""
        rho = None
        for src in self.sources:
            ps = (context or {}).get(src)
            if ps is not None and ps.get("rho_em") is not None:
                rho = ps["rho_em"] if rho is None else rho + ps["rho_em"]
        ext = state.get("_rho_ext")
        if ext is not None:
            rho = ext if rho is None else rho + ext
        return rho

    def _potential(self, lattice, context, state):
        rho = self._source_density(lattice, context, state)
        if rho is None or not np.any(rho):
            return np.zeros((lattice.L,) * 3)
        from casim.gravity import solve_poisson_3d_open
        phi_em = -solve_poisson_3d_open(rho, G_N=self.g_coulomb / (4.0 * np.pi))
        return self.charge * phi_em

    # --- spectral kinetic helper ------------------------------------------
    @staticmethod
    def _k2(L):
        k = 2.0 * np.pi * np.fft.fftfreq(L)
        KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
        return KX ** 2 + KY ** 2 + KZ ** 2

    def _relax_ground_state(self, psi, V, L, dtau, steps):
        """Imaginary-time relaxation to the ground state of (−∇²/2m + V)."""
        k2 = self._k2(L)
        kin = np.exp(-k2 / (2.0 * self.mass) * dtau)
        pot = np.exp(-V * dtau / 2.0)
        for _ in range(int(steps)):
            psi = pot * psi
            psi = np.fft.ifftn(kin * np.fft.fftn(psi))
            psi = pot * psi
            nrm = np.sqrt(float((np.abs(psi) ** 2).sum()))
            if nrm > 0:
                psi = psi / nrm
        return psi

    def init_state(self, lattice, rng):
        L = lattice.L
        init = self.config.get("init", {}) or {}
        center = tuple(init.get("center", (L // 2, L // 2, L // 2)))
        width = float(init.get("width", 2.0))
        psi = gaussian_packet(L, center, width, k0=None).astype(complex)
        psi = psi / np.sqrt(float((np.abs(psi) ** 2).sum()))
        st = {"psi": psi, "_relaxed": not bool(init.get("ground_state", False)),
              "centroid_prev": _centroid(np.abs(psi) ** 2, L)}
        # build the static external point charge once (U2 de-risk)
        if self.external_charge is not None:
            ec = self.external_charge
            c = tuple(ec.get("center", center))
            w = float(ec.get("width", 1.0))
            qext = float(ec.get("q", 1.0))
            blob = gaussian_packet(L, c, w, k0=None)
            dens = np.abs(blob) ** 2
            dens = dens / dens.sum() * qext
            st["_rho_ext"] = dens
        self._publish_currents(st)
        return st

    def density_field(self, state):
        return np.asarray(np.abs(state["psi"]) ** 2)

    def step(self, state, lattice, context=None, rng=None):
        L = lattice.L
        psi = state["psi"]
        prev = _centroid(np.abs(psi) ** 2, L)
        V = self._potential(lattice, context, state)
        # lazy ground-state relaxation on the first live step
        if not state.get("_relaxed", True):
            init = self.config.get("init", {}) or {}
            psi = self._relax_ground_state(
                psi, V, L,
                dtau=float(init.get("relax_dtau", 0.05)),
                steps=int(init.get("relax_steps", 800)))
        # real-time Strang split-step (exactly unitary)
        k2 = self._k2(L)
        kin = np.exp(-1j * k2 / (2.0 * self.mass) * self.dt)
        pot = np.exp(-1j * V * self.dt / 2.0)
        psi = pot * psi
        psi = np.fft.ifftn(kin * np.fft.fftn(psi))
        psi = pot * psi
        new = {"psi": psi, "_relaxed": True, "centroid_prev": prev}
        if "_rho_ext" in state:
            new["_rho_ext"] = state["_rho_ext"]
        self._publish_currents(new)
        return new

    def _publish_currents(self, state) -> None:
        psi = state["psi"]
        state["rho_em"] = self.charge * np.abs(psi) ** 2
        # probability current J = q·Im(ψ* ∇ψ)/m (spectral gradient)
        ft = np.fft.fftn(psi)
        k = 2.0 * np.pi * np.fft.fftfreq(psi.shape[0])
        KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
        J = np.zeros((3,) + psi.shape)
        for ax, Kc in enumerate((KX, KY, KZ)):
            grad = np.fft.ifftn(1j * Kc * ft)
            J[ax] = self.charge * np.imag(np.conj(psi) * grad) / self.mass
        state["J_em"] = J

    def energy(self, state) -> float:
        return float((np.abs(state["psi"]) ** 2).sum())

    def observables(self, state, lattice) -> dict:
        L = lattice.L
        d = np.abs(state["psi"]) ** 2
        cen = _centroid(d, L)
        prev = np.asarray(state["centroid_prev"])
        vel = (cen - prev + L / 2.0) % L - L / 2.0
        return {
            "species": "e_NR",
            "norm": self.energy(state),
            "centroid": [float(x) for x in cen],
            "velocity_per_tick": [float(v) for v in vel],
            "rms_self": _rms_radius(d, cen, L),
            "charge": self.charge,
        }


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
    label = "Composite Particle"
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

    Per tick: the **even rotation-law** propagator
    ``ca_photon_pair.photon_step_spectral`` (F67/F68/F69, exactly unitary /
    norm-conserving) followed by a real-space source kick ``E += g·J·dt`` —
    the same rotation+kick structure the ``w_sourced`` and ``gluon_sourced``
    channels use.  The sum over ``J_em`` runs over the particle channels named
    in ``sources``.

    History: this channel originally propagated with
    ``ca_charge_coupling.maxwell_curl_step`` (the explicit linearized-Maxwell
    curl).  Per F25/F26 the curl equation is only the first-order Taylor
    expansion of this rotation law and the explicit scheme is only
    conditionally stable — under sustained sourcing it diverges (observed:
    photon energy ∝ 10^{0.0096·t}, reaching 1e119 by t=13k while the matter
    norms stayed exact).  The even rotation law is unconditionally stable;
    ``test_P5_*`` regression-locks photon energy boundedness over a long run.
    """
    type_name = "photon_sourced"
    label = "Photon Sourced"
    propagator = "even"
    topologies = ("cubic", "bcc")

    def init_state(self, lattice, rng):
        L = lattice.L
        return {"E": np.zeros((3, L, L, L)), "B": np.zeros((3, L, L, L)),
                "alpha": np.zeros((L, L, L))}

    def step(self, state, lattice, context=None, rng=None):
        from casim.fields.photon import photon_step_spectral
        dt = float(self.config.get("dt", 0.1))
        g_em = float(self.config.get("g_em", 1.0))
        J, rho = None, None
        for src in self.config.get("sources", []):
            ps = (context or {}).get(src)
            if ps is not None and "J_em" in ps:
                J = ps["J_em"] if J is None else J + ps["J_em"]
            if ps is not None and "rho_em" in ps:
                rho = ps["rho_em"] if rho is None else rho + ps["rho_em"]
        # Free even-law rotation (exactly unitary), then source kick.
        E, B = photon_step_spectral(state["E"], state["B"])
        if J is not None:
            E = E + g_em * J * dt
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
    label = "Gluon Sourced"
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
# ColourBagChannel — the LIVE colour-dielectric flux-tube field (F137).
# Replaces the geometric F135 string with a dynamical bag: the colour-magnetic
# condensate is MELTED where the quark colour charge/flux sits, and full in
# the vacuum.  The scalar confining mass the quarks read is the bag wall,
# S(x)=M_bag·f²(x) — large in the vacuum (ε_c→0, flux expelled, F86), ~0 in
# the dug-out core/tube.  Sourced each tick by the quark J_colour, so the bag
# tracks the quarks: a self-generated MIT bag / dual-superconductor tube.
# ======================================================================
def _gauss_smear(rho, lam):
    """Gaussian smear of a real (L,L,L) field by width ``lam`` (FFT).  Models
    the colour-field penetration: a point colour charge fills a region of
    radius ~λ (the F86 dual-London depth λ=1/ev), so two charges within ~2λ
    share a connected low-condensate channel — the flux tube."""
    L = rho.shape[0]
    k = 2.0 * np.pi * np.fft.fftfreq(L)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
    ker = np.exp(-0.5 * lam ** 2 * (KX ** 2 + KY ** 2 + KZ ** 2))
    return np.real(np.fft.ifftn(np.fft.fftn(rho) * ker))


@register
class ColourBagChannel(Channel):
    """Live colour-dielectric bag field S(x) sourced by quark colour charge.

    Per tick: ρ(x)=Σ_sources |J_colour|(x) (octet magnitude) → smear by the
    penetration depth λ → condensate f²(x)=exp(−φ/φ₀) (→1 vacuum, →0 where
    colour charge sits) → bag wall mass S(x)=M_bag·f²(x) and F86 dielectric
    ε_c(x)=1−f²(x) (→0 vacuum, →1 core).  Quarks with ``confine.field`` read
    S as their Lorentz-scalar confining mass (F135 mechanism), so the bag they
    dig confines them — no posited geometric string.

    Two modes:
      * **mean-field** (default) — the F137 fixed-smear map above; the
        condensate responds to the colour-charge density one-way, so the tube
        pinches off beyond ~2λ.
      * **self-consistent** (``backreaction: true``, F139) — the genuine dual-
        Ginzburg-Landau loop ``ca_dual_gl_backreaction.self_consistent_bag``:
        the confined colour-electric flux is itself what melts the condensate
        (∂f/∂τ has the −f|D|²/ε_c² back-reaction term), the two fields solved
        to mutual consistency each tick (warm-started from the previous tick).
        The tube stays connected and linear to arbitrary separation; λ emerges
        from the coherence length ξ instead of being posited.
    """
    type_name = "colour_bag"
    label = "Colour Bag (dielectric)"
    propagator = "dielectric"
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        L = lattice.L
        z = np.zeros((L, L, L))
        return {"S": z.copy(), "eps_c": z.copy(), "phi": z.copy(),
                "f": np.ones((L, L, L))}            # warm-start condensate (SC)

    def _octet_source(self, L, context):
        """Net signed octet colour-charge density ρ^a = Σ_sources J^a_colour
        (8, L, L, L), and the scalar octet-magnitude ρ used by the mean-field
        map.  Returns (rho_oct, rho_mag)."""
        rho_oct = np.zeros((8, L, L, L))
        rho_mag = np.zeros((L, L, L))
        for src in self.config.get("sources", []):
            ps = (context or {}).get(src)
            if ps is not None and "J_colour" in ps:
                Jc = np.asarray(ps["J_colour"], float)
                rho_oct = rho_oct + Jc
                rho_mag = rho_mag + np.sqrt((Jc ** 2).sum(axis=0))
        return rho_oct, rho_mag

    def step(self, state, lattice, context=None, rng=None):
        L = lattice.L
        M_bag = float(self.config.get("M_bag", 1.5))

        if self.config.get("backreaction", False):
            # --- self-consistent dual-GL back-reaction (F139) -------------
            from casim.fields.strong import ca_dual_gl_backreaction as gl
            rho_oct, _ = self._octet_source(L, context)
            # solve only the non-trivial octet directions (Cartan-dominated
            # for a definite-colour proton) — keeps the live loop cheap
            rho_oct = rho_oct * float(self.config.get("g_src", 1.0))  # colour coupling g_s on the source
            norms = np.sqrt((rho_oct ** 2).sum(axis=(1, 2, 3)))
            keep = norms > float(self.config.get("src_tol", 1e-3)) * (norms.max() + 1e-30)
            src = rho_oct[keep] if keep.any() else rho_oct[:1]
            res = gl.self_consistent_bag(
                src,
                xi=float(self.config.get("xi", 1.0)),
                eps_floor=float(self.config.get("eps_floor", 0.02)),
                dtau=float(self.config.get("dtau", 0.03)),
                n_out=int(self.config.get("sc_iters", 12)),
                poisson_maxit=int(self.config.get("poisson_maxit", 150)),
                tol=float(self.config.get("sc_tol", 1e-6)),
                f_init=state.get("f"))
            f = res["f"]
            return {"S": M_bag * f * f, "eps_c": res["eps_c"], "f": f,
                    "phi": -np.log(np.clip(f * f, 1e-12, 1.0))}

        # --- mean-field bag (F137 default) -------------------------------
        phi0 = float(self.config.get("phi0", 0.05))
        lam = float(self.config.get("lam", 2.0))
        _, rho = self._octet_source(L, context)
        phi = np.clip(_gauss_smear(rho, lam), 0.0, None)  # clip FFT round-off
        f2 = np.exp(-phi / max(phi0, 1e-12))
        return {"S": M_bag * f2, "eps_c": 1.0 - f2, "phi": phi,
                "f": np.sqrt(f2)}

    def energy(self, state) -> float:
        return float(state["S"].sum())

    def observables(self, state, lattice) -> dict:
        return {"S_max": float(state["S"].max()),
                "S_min": float(state["S"].min()),
                "eps_c_core": float(state["eps_c"].max())}


# ======================================================================
# Sidebar feed: per-particle readouts every N ticks
# ======================================================================
@register_observer
class ParticleReadout(Observer):
    """Record each ParticleChannel's observables (norm, centroid, velocity,
    exact charges, active couplings + tier, gravity readouts).  This is the
    data feed for the GUI sidebar (roadmap P3)."""
    name = "particle_readout"
    label = "Particle Readout"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        rec = {"tick": sim.tick, "particles": {}}
        for cname, ch in sim.channels.items():
            if isinstance(ch, (ParticleChannel, CompositeParticleChannel)):
                rec["particles"][cname] = ch.observables(
                    sim.states[cname], sim.lattice)
        if rec["particles"]:
            self.records.append(rec)


# ======================================================================
# Unification readout — the emergent-binding diagnostics for the
# real-space integration (roadmap-unified-real-space.md, U0).
# ======================================================================
def _rms_radius(density, center, L):
    """Periodic-safe RMS radius of a density about ``center`` (lattice units)."""
    tot = float(np.asarray(density).sum())
    if tot <= 0.0:
        return 0.0
    idx = np.indices(density.shape)
    r2 = np.zeros(density.shape)
    for ax in range(3):
        d = (idx[ax] - center[ax] + L / 2.0) % L - L / 2.0
        r2 = r2 + d ** 2
    return float(np.sqrt(float((density * r2).sum()) / tot))


def _min_image_sep(a, b, L):
    """Periodic-safe distance between two centroids (lattice units)."""
    d = (np.asarray(a) - np.asarray(b) + L / 2.0) % L - L / 2.0
    return float(np.sqrt(float(np.sum(d ** 2))))


def _field_norm(state, key):
    """L2 norm of a field array stored under ``key`` in ``state`` (or 0)."""
    if state is None or key not in state or state[key] is None:
        return 0.0
    return float(np.sqrt(float(np.sum(np.abs(state[key]) ** 2))))


@register_observer
class UnificationReadout(Observer):
    """Emergent-binding diagnostics for the unified real-space run (U0).

    Auto-detects the quark ParticleChannels (the proton constituents), the
    charged-lepton ParticleChannel (the electron), and the gluon / photon
    sourced-field channels, then records each tick:

      * ``proton_rms``       — RMS radius of the combined quark density about
        its own centroid (the confinement size proxy; bounded = confined,
        growing = dispersing).
      * ``electron_rms_self``— electron RMS radius about its own centroid.
      * ``electron_rms_about_p`` — electron RMS radius about the **proton**
        centroid (the orbit/binding proxy).
      * ``ep_separation``    — proton↔electron centroid separation.
      * ``net_charge``       — Σ q over all particle channels (neutrality).
      * ``loops``            — liveness norms ‖J_colour‖, ‖gluon A‖, ‖J_em‖,
        ‖photon α‖ (the currents are sourcing the fields, the fields exist).

    Config (all optional; auto-detected if absent): ``quarks`` (list of channel
    names), ``electron``, ``gluon``, ``photon``.
    """
    name = "unification_readout"
    label = "Unification Readout"
    exactness = "quantitative"

    def _resolve(self, sim):
        cfg = self.config
        # explicit constituent cluster (e.g. confined Dirac stand-ins) wins
        quarks = list(cfg.get("cluster", cfg.get("quarks", [])))
        if cfg.get("cluster"):
            return quarks, cfg.get("electron"), cfg.get("gluon"), \
                cfg.get("photon")
        electron = cfg.get("electron")
        gluon = cfg.get("gluon")
        photon = cfg.get("photon")
        for cname, ch in sim.channels.items():
            if isinstance(ch, ColourDiracQuarkChannel) or (
                    isinstance(ch, ParticleChannel)
                    and getattr(ch, "is_quark", False)):
                if not cfg.get("quarks") and cname not in quarks:
                    quarks.append(cname)
            elif isinstance(ch, NonRelElectronChannel):
                if electron is None:
                    electron = cname
            elif isinstance(ch, ParticleChannel) \
                    and electron is None and not getattr(ch, "is_doublet", False) \
                    and float(ch.specs[0].Q) != 0.0:
                electron = cname
            st = sim.states.get(cname)
            if gluon is None and st is not None and "A" in st \
                    and np.asarray(st["A"]).shape[0] == 8:
                gluon = cname
            if photon is None and st is not None and "alpha" in st:
                photon = cname
        return quarks, electron, gluon, photon

    def observe(self, sim) -> None:
        L = sim.lattice.L
        quarks, electron, gluon, photon = self._resolve(sim)
        rec = {"tick": sim.tick}

        # --- proton: combined quark density ---
        p_centroid = None
        if quarks:
            dens = None
            for q in quarks:
                ch = sim.channels[q]
                d = np.asarray(ch.density_field(sim.states[q]))
                dens = d if dens is None else dens + d
            p_centroid = _centroid(dens, L)
            rec["proton_rms"] = _rms_radius(dens, p_centroid, L)
            rec["proton_centroid"] = [float(x) for x in p_centroid]
            rec["proton_norm"] = float(dens.sum())

        # --- electron ---
        if electron is not None:
            ch = sim.channels[electron]
            de = np.asarray(ch.density_field(sim.states[electron]))
            e_centroid = _centroid(de, L)
            rec["electron_rms_self"] = _rms_radius(de, e_centroid, L)
            rec["electron_centroid"] = [float(x) for x in e_centroid]
            if p_centroid is not None:
                rec["electron_rms_about_p"] = _rms_radius(de, p_centroid, L)
                rec["ep_separation"] = _min_image_sep(e_centroid, p_centroid, L)

        # --- net charge over all particle channels ---
        q_tot = 0.0
        for cname, ch in sim.channels.items():
            if isinstance(ch, NonRelElectronChannel):
                q_tot += ch.charge
            elif isinstance(ch, ParticleChannel):
                q_tot += sum(float(s.Q) for s in ch.specs)
        rec["net_charge"] = q_tot

        # --- loop liveness ---
        loops = {}
        jc = 0.0
        for q in quarks:
            jc += _field_norm(sim.states.get(q), "J_colour")
        loops["J_colour"] = jc
        loops["gluon_A"] = _field_norm(sim.states.get(gluon), "A") \
            if gluon else 0.0
        jem = 0.0
        for cname, ch in sim.channels.items():
            if isinstance(ch, (ParticleChannel, NonRelElectronChannel)):
                jem += _field_norm(sim.states.get(cname), "J_em")
        loops["J_em"] = jem
        loops["photon_alpha"] = _field_norm(sim.states.get(photon), "alpha") \
            if photon else 0.0
        rec["loops"] = loops
        self.records.append(rec)

    def summary(self) -> Dict[str, Any]:
        if not self.records:
            return {}
        first, last = self.records[0], self.records[-1]
        out = {}
        for key in ("proton_rms", "electron_rms_about_p", "ep_separation",
                    "electron_rms_self"):
            if key in first and key in last:
                out[key] = {"first": first[key], "last": last[key],
                            "ratio": (last[key] / first[key]
                                      if first[key] else None)}
        out["net_charge"] = last.get("net_charge")
        out["loops_live"] = {k: (v > 0.0) for k, v in
                             last.get("loops", {}).items()}
        return out


# ======================================================================
# TwoGridAtomChannel — the LIVE two-grid multigrid (U4, F160)
# ----------------------------------------------------------------------
# A single engine channel that co-evolves BOTH grids in one Simulation.run():
#   * a FINE proton patch  — three colour Dirac quarks (uud) confined by the
#     F135 scalar Y-string (the audited `quark_dirac` kernel), resolving the
#     proton's internal structure;
#   * a COARSE atomic grid — the F156 non-relativistic electron orbital.
# Every tick: step the fine proton, R_b coarse-grain its charge to a point
# source on the coarse grid (the F133/F159 block-spin reduction), then step the
# electron in that well.  The block factor b carries the proton:orbit scale
# separation (~1e4–1e5) that no single tractable grid can hold — so the proton
# and the orbit live at their TRUE relative scale, not the U3 compressed scale.
# This is the live realisation of the F159 staged multigrid.
# ======================================================================
@register
class TwoGridAtomChannel(Channel):
    """Live two-grid hydrogen: fine confined proton + coarse bound electron,
    coupled by a per-tick block-spin (R_b) charge reduction (U4).

    Scenario config::

        {type: two_grid_atom, name: atom, b: 30000,
         fine:   {L: 16, sigma: 0.5, dt: 0.5, mass: 0.9},
         coarse: {L: 32, m: 1.0, k: 6.0, dt: 0.2, relax_steps: 600}}
    """
    type_name = "two_grid_atom"
    label = "Two-Grid Atom"
    propagator = "multigrid"
    topologies = ("bcc", "cubic")

    _FINE = (("u_r", "u_L", "r"), ("u_g", "u_L", "g"), ("d_b", "d_L", "b"))

    def __init__(self, name=None, **config):
        super().__init__(name=name, **config)
        self.b = int(config.get("b", 30000))
        fine = dict(config.get("fine", {}) or {})
        coarse = dict(config.get("coarse", {}) or {})
        self.Lf = int(fine.get("L", 16))
        self.f_sigma = float(fine.get("sigma", 0.5))
        self.f_dt = float(fine.get("dt", 0.5))
        self.f_mass = float(fine.get("mass", 0.9))
        self.Lc = int(coarse.get("L", 32))
        self.e_m = float(coarse.get("m", 1.0))
        self.e_k = float(coarse.get("k", 6.0))
        self.e_dt = float(coarse.get("dt", 0.2))
        self.e_relax = int(coarse.get("relax_steps", 600))
        self.e_charge = float(coarse.get("charge", -1.0))
        # build the fine proton quark channels (audited quark_dirac kernel)
        names = [n for (n, _, _) in self._FINE]
        c = self.Lf // 2
        offs = [(-2, 0, 0), (2, 0, 0), (0, 2, 0)]
        self._fine_names = names
        self._fine_chs = []
        for (nm, sp, col), off in zip(self._FINE, offs):
            ch = ColourDiracQuarkChannel(
                name=nm, species=sp, colour=col, mass=self.f_mass,
                init={"center": [c + off[0], c + off[1], c + off[2]],
                      "width": 1.3},
                couplings={"em": "photon"},          # publishes rho_em
                confine={"mode": "scalar", "anchor": "com", "sigma": self.f_sigma,
                         "dt": self.f_dt, "partners": names})
            self._fine_chs.append(ch)

    def _fine_lat(self):
        from ..engine.simulation import LatticeSpec
        return LatticeSpec(L=self.Lf, topology="bcc",
                           c_lat=1.0 / float(np.sqrt(3.0)))

    def _proton_charge_density(self, fine_states):
        """Summed quark rho_em on the fine grid (total ≈ +1)."""
        rho = None
        for st in fine_states:
            r = st.get("rho_em")
            if r is not None:
                rho = r if rho is None else rho + r
        return rho

    def _coarse_well(self, rho_fine):
        """R_b-reduce the fine proton charge to a point source on the coarse
        grid and return the electron Coulomb well V(x)=−k·Q/r (live coupling)."""
        import ca_multigrid as mg
        Q = float(np.sum(rho_fine))                 # total charge (R_b-conserved)
        rms_c = mg._rms(np.asarray(rho_fine, float)) / max(self.b, 1)
        cc = self.Lc // 2
        return mg.coarse_point_potential(self.Lc, (cc, cc, cc),
                                         k=self.e_k * Q,
                                         src_rms_cells=min(rms_c, 0.0)), Q

    def init_state(self, lattice, rng):
        import ca_multigrid as mg
        flat = self._fine_lat()
        fine = [ch.init_state(flat, rng) for ch in self._fine_chs]
        rho = self._proton_charge_density(fine)
        V, Q = self._coarse_well(rho)
        # electron relaxed into the initial proton well (starts bound)
        cc = self.Lc // 2
        ax = np.arange(self.Lc)
        X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
        psi = np.exp(-(((X - cc) ** 2 + (Y - cc) ** 2 + (Z - cc) ** 2))
                     / (2.0 * (self.Lc / 6.0) ** 2)).astype(complex)
        psi /= np.sqrt((np.abs(psi) ** 2).sum())
        psi = mg.schrodinger_relax(psi, V, self.e_m, 1.0, self.e_relax, 0.02)
        st = {"psi": psi, "proton_charge": Q}
        for nm, fs in zip(self._fine_names, fine):
            st[f"fine::{nm}"] = fs
        return st

    def _fine_states(self, state):
        return [state[f"fine::{nm}"] for nm in self._fine_names]

    def step(self, state, lattice, context=None, rng=None):
        import ca_multigrid as mg
        flat = self._fine_lat()
        fine = self._fine_states(state)
        ctx = {nm: fs for nm, fs in zip(self._fine_names, fine)}
        # 1. step the fine proton (each quark reads the shared pre-tick context)
        new_fine = [ch.step(ctx[nm], flat, context=ctx, rng=rng)
                    for nm, ch in zip(self._fine_names, self._fine_chs)]
        # 2. R_b: reduce the live proton charge to the coarse well (per tick)
        rho = self._proton_charge_density(new_fine)
        V, Q = self._coarse_well(rho)
        # 3. step the coarse electron in that well
        psi = mg.schrodinger_step(state["psi"], V, self.e_m, 1.0, self.e_dt)
        out = {"psi": psi, "proton_charge": Q}
        for nm, fs in zip(self._fine_names, new_fine):
            out[f"fine::{nm}"] = fs
        return out

    # --- diagnostics -------------------------------------------------------
    def _proton_density(self, state):
        d = None
        for nm in self._fine_names:
            fs = state[f"fine::{nm}"]
            dd = (np.abs(fs["eta_u"]) ** 2 + np.abs(fs["eta_d"]) ** 2
                  + np.abs(fs["chi_u"]) ** 2 + np.abs(fs["chi_d"]) ** 2).sum(axis=0)
            d = dd if d is None else d + dd
        return np.asarray(d.real if np.iscomplexobj(d) else d)

    def density_field(self, state):
        return np.asarray(np.abs(state["psi"]) ** 2)

    def energy(self, state) -> float:
        e = float((np.abs(state["psi"]) ** 2).sum())
        e += float(self._proton_density(state).sum())
        return e

    def observables(self, state, lattice) -> dict:
        import ca_multigrid as mg
        pd = self._proton_density(state)
        ed = np.abs(state["psi"]) ** 2
        rp = mg._rms(pd)                      # proton RMS (fine cells)
        re = mg._rms(ed)                      # electron RMS (coarse cells)
        Q = float(state.get("proton_charge", 0.0))
        ratio = re * self.b / rp if rp > 0 else 0.0
        return {
            "b": self.b,
            "proton_rms_fine": rp,
            "electron_rms_coarse": re,
            "proton_charge": Q,
            "electron_charge": self.e_charge,
            "net_charge": Q + self.e_charge,
            "represented_a0_over_rp": ratio,
            "represented_decades": float(np.log10(ratio)) if ratio > 0 else None,
            "proton_norm": float(pd.sum()),
            "electron_norm": float(ed.sum()),
        }


@register_observer
class TwoGridReadout(Observer):
    """Per-tick diagnostics for the live two-grid atom (U4): proton RMS (fine),
    electron RMS (coarse), net charge, and the represented proton:orbit ratio."""
    name = "two_grid_readout"
    label = "Two-Grid Readout"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        for cname, ch in sim.channels.items():
            if isinstance(ch, TwoGridAtomChannel):
                rec = {"tick": sim.tick}
                rec.update(ch.observables(sim.states[cname], sim.lattice))
                self.records.append(rec)
                return


# ======================================================================
# ElementAtomChannel — the F195 generalisation of the F160 two-grid atom
# to a general element (Z, N): multi-nucleon fine patch → +Z coarse point,
# multi-electron coarse grid with Pauli (Gram–Schmidt) filling in a live
# self-consistent Hartree mean field.
# ======================================================================
def _gram_schmidt(psis):
    """Modified Gram–Schmidt orthonormalisation of a list of complex orbital
    arrays (the live Pauli antisymmetriser).  ``np.vdot(a, b)`` conjugates the
    first argument, so this is the proper Hermitian inner product Σ ψ_a* ψ_b.
    Order is the binding order (lowest state first), so the reference set is the
    deeper orbitals and higher orbitals are projected orthogonal to them."""
    out = []
    for p in psis:
        q = np.asarray(p, dtype=complex).copy()
        for r in out:
            q = q - np.vdot(r, q) * r
        n = float(np.sqrt(np.vdot(q, q).real))
        if n > 0:
            q = q / n
        out.append(q)
    return out


def _max_offdiag_overlap(psis):
    """Largest |⟨ψ_i|ψ_j⟩| over i≠j (Pauli orthogonality residual)."""
    m = 0.0
    for i in range(len(psis)):
        for j in range(i + 1, len(psis)):
            m = max(m, abs(complex(np.vdot(psis[i], psis[j]))))
    return m


# real (m=0,±1) angular factors for the seed packets; only s,p are needed for
# the certified ladder H→He→Li→C.  d/f fall back to coordinate products and are
# wired-but-not-certified.
def _angular_seed(l, mi, X, Y, Z, cc):
    dx, dy, dz = X - cc, Y - cc, Z - cc
    if l == 0:
        return np.ones_like(dx, dtype=float)
    if l == 1:
        return (dx, dy, dz)[mi % 3]
    if l == 2:                                   # wired, not certified past C
        comps = (dx * dy, dy * dz, dz * dx, dx * dx - dy * dy, dz * dz)
        return comps[mi % 5]
    comps = (dx, dy, dz)                          # crude f fallback
    return comps[mi % 3]


def _spatial_orbitals(Z):
    """Decompose the Aufbau configuration of Z electrons into distinct SPATIAL
    orbitals with Hund's-rule occupancies.  Each spatial orbital holds ≤2
    electrons (a spin pair, automatically orthogonal in spin); within an open
    subshell the m-orbitals are singly filled first (Hund), then paired.

    Returns a list of dicts {n, l, mi, occ} ordered by Aufbau binding."""
    import ca_manybody as mb
    cfg = mb.aufbau_configuration(Z)              # [(n, 'l', occ)]
    L_OF = {"s": 0, "p": 1, "d": 2, "f": 3}
    orbs = []
    for (n, ll, occ) in cfg:
        l = L_OF[ll]
        nm = 2 * l + 1                            # m-orbitals in the subshell
        m_occ = [0] * nm
        e = occ
        for i in range(nm):                       # Hund: one each first
            if e <= 0:
                break
            m_occ[i] += 1
            e -= 1
        for i in range(nm):                       # then pair up
            if e <= 0:
                break
            m_occ[i] += 1
            e -= 1
        for i, mo in enumerate(m_occ):
            if mo > 0:
                orbs.append({"n": n, "l": l, "mi": i, "occ": mo})
    return orbs


@register
class ElementAtomChannel(Channel):
    """Live block-spin atom for a general element (Z, N) — the F195
    generalisation of the F160 ``two_grid_atom``.

    FINE sector (Tier A, default): A = Z+N nucleon charge blobs in a bound
    cluster whose net ``rho_em`` integrates to exactly +Z (the N neutrons carry
    zero net charge); this is R_b-reduced to a single +Z coarse point source.
    Faithful to F159 (the electron cannot resolve nuclear structure as
    a₀/r_nuc → ∞).  Tier B (``fine: {live_quarks: true}``, He-capped) runs
    3·A ``quark_dirac`` quarks as live confined nucleons instead.

    COARSE sector: Z electrons filled into the Aufbau configuration as distinct
    spatial orbitals (Hund's rule), each an exactly-unitary F156 split-step
    packet evolving in the self-consistent mean field = the +Z nuclear well
    plus the live Hartree potential of all *other* electrons.  Pauli
    antisymmetry is enforced by Gram–Schmidt orthonormalising the occupied
    orbitals every ``gs_every`` ticks.

    Scenario config::

        {type: element_atom, name: atom, Z: 2, N: 2, b: 30000,
         fine:   {L: 12, sigma: 0.5, spread: 2.0},
         coarse: {L: 24, m: 1.0, k: 0.3, dt: 0.5, relax_steps: 480,
                  scf_iters: 8, gs_every: 1, hartree_every: 2}}

    ``free: true`` builds the matched CONTROL (no nuclear well, no e–e field):
    the orbitals are seeded compact and propagate ballistically so the
    bounded-vs-dispersing contrast is exhibited, not asserted.
    """
    type_name = "element_atom"
    label = "Element Atom"
    propagator = "multigrid"
    topologies = ("bcc", "cubic")

    def __init__(self, name=None, **config):
        super().__init__(name=name, **config)
        self.Z = int(config.get("Z", 1))
        self.N = int(config.get("N", 0))
        self.A = self.Z + self.N
        self.b = int(config.get("b", 30000))
        self.free = bool(config.get("free", False))
        fine = dict(config.get("fine", {}) or {})
        coarse = dict(config.get("coarse", {}) or {})
        self.Lf = int(fine.get("L", 12))
        self.f_sigma = float(fine.get("sigma", 0.5))     # nucleon blob RMS (cells)
        self.f_spread = float(fine.get("spread", 2.0))   # cluster placement radius
        self.live_quarks = bool(fine.get("live_quarks", False))
        self.f_dt = float(fine.get("dt", 0.5))
        self.f_mass = float(fine.get("mass", 0.9))
        # Tier-B inter-nucleon binding (model NN one-boson-exchange, F104/F126/
        # F128/F113): on by default for live quarks; the matched control sets it
        # off to expose bound-vs-unbound.
        self.nn_binding = bool(fine.get("nn_binding", True))
        self.g_nn = float(fine.get("g_nn", 0.012))      # NN force → lattice momentum
        self.nn_scale = float(fine.get("r_fm_per_cell", 1.0))  # fine-cell → fm
        self.Lc = int(coarse.get("L", 24))
        self.e_m = float(coarse.get("m", 1.0))
        self.e_k = float(coarse.get("k", 0.3))
        self.e_dt = float(coarse.get("dt", 0.5))
        self.e_relax = int(coarse.get("relax_steps", 480))
        self.e_scf = int(coarse.get("scf_iters", 8))
        self.e_dtau = float(coarse.get("relax_dtau", 0.02))
        self.gs_every = max(1, int(coarse.get("gs_every", 1)))
        self.hartree_every = max(1, int(coarse.get("hartree_every", 2)))
        self.e_charge = -1.0
        self._orbs = _spatial_orbitals(self.Z)
        self._occ = [o["occ"] for o in self._orbs]
        # fine nucleon cluster geometry (Tier A static charge/matter densities)
        self._build_fine_nucleus()
        # Tier B: live quark nucleons (He-capped)
        self._fine_chs = []
        self._fine_names = []
        if self.live_quarks and not self.free:
            self._build_live_quarks()

    # -- fine nucleus -------------------------------------------------------
    def _nucleon_offsets(self):
        """A deterministic compact cluster of A nucleon centres (fine cells)."""
        cc = self.Lf // 2
        if self.A == 1:
            return [(cc, cc, cc)]
        # points on a small spherical shell (Fibonacci lattice) — compact, A-body
        pts = []
        phi = np.pi * (3.0 - np.sqrt(5.0))
        for i in range(self.A):
            y = 1.0 - 2.0 * (i + 0.5) / self.A
            r = np.sqrt(max(0.0, 1.0 - y * y))
            th = phi * i
            pts.append((cc + self.f_spread * r * np.cos(th),
                        cc + self.f_spread * y,
                        cc + self.f_spread * r * np.sin(th)))
        return pts

    def _blob(self, center):
        ax = np.arange(self.Lf)
        X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
        r2 = ((X - center[0]) ** 2 + (Y - center[1]) ** 2 + (Z - center[2]) ** 2)
        g = np.exp(-r2 / (2.0 * self.f_sigma ** 2))
        s = g.sum()
        return g / s if s > 0 else g           # normalised to total 1

    def _build_fine_nucleus(self):
        offs = self._nucleon_offsets()
        rho_q = np.zeros((self.Lf,) * 3)        # charge density (protons only)
        rho_m = np.zeros((self.Lf,) * 3)        # matter density (all nucleons)
        for i, c in enumerate(offs):
            blob = self._blob(c)
            rho_m += blob
            if i < self.Z:                      # first Z nucleons are protons
                rho_q += blob                   # each integrates to +1 → total +Z
        self._rho_charge_fine = rho_q
        self._rho_matter_fine = rho_m
        import ca_multigrid as mg
        self._nuc_rms_fine = mg._rms(rho_m)
        self._nuc_charge = float(rho_q.sum())   # ≈ Z to machine precision

    def _build_live_quarks(self):
        """Tier B: 3·A colour Dirac quarks (Z protons uud, N neutrons udd)."""
        offs = self._nucleon_offsets()
        protons = [(("u_r", "u_L", "r"), ("u_g", "u_L", "g"), ("d_b", "d_L", "b"))] * self.Z
        neutrons = [(("u_r", "u_L", "r"), ("d_g", "d_L", "g"), ("d_b", "d_L", "b"))] * self.N
        groups = protons + neutrons
        self._nuc_groups = []                  # [[quark names per nucleon], ...]
        self._fine_ch_by_name = {}
        for ni, (grp, ctr) in enumerate(zip(groups, offs)):
            names = [f"n{ni}_{nm}" for (nm, _, _) in grp]
            self._nuc_groups.append(names)
            qoff = [(-1, 0, 0), (1, 0, 0), (0, 1, 0)]
            for (nm, sp, col), off in zip(grp, qoff):
                full = f"n{ni}_{nm}"
                ch = ColourDiracQuarkChannel(
                    name=full, species=sp, colour=col, mass=self.f_mass,
                    init={"center": [ctr[0] + off[0], ctr[1] + off[1],
                                     ctr[2] + off[2]], "width": 1.1},
                    couplings={"em": "photon"},
                    confine={"mode": "scalar", "anchor": "com",
                             "sigma": self.f_sigma, "dt": self.f_dt,
                             "partners": names})
                self._fine_chs.append(ch)
                self._fine_names.append(full)
                self._fine_ch_by_name[full] = ch
        if self.nn_binding:
            self._setup_nn_potential()

    # -- model NN one-boson-exchange (F104/F126/F128/F113) -------------------
    def _setup_nn_potential(self):
        """Build the model NN central potential V_pair(r) = σ(F126) + ω(F128) +
        quark-Pauli core(F113) − V0·exp(−r²/2R0²), where the S=1,T=0 attraction
        (the F104 π-tensor, folded as in ca_manybody) has depth V0 fixed so the
        A=2 variational reproduces the MODEL deuteron binding — no experimental
        nucleus calibrates it.  Caches V_pair and its derivative for the live
        inter-nucleon force."""
        import ca_nuclear as ncl
        import ca_manybody as mb
        HBARC, M_PI, M_N = ncl.HBARC, ncl.M_PI_DEFAULT, ncl.M_N
        anchor = mb._model_deuteron_binding()
        R0 = HBARC / M_PI
        rr = np.linspace(1e-3, 9.0, 1800)
        dr = rr[1] - rr[0]
        Vcent = (ncl.sigma_exchange_potential(rr) + ncl.omega_exchange_potential(rr)
                 + ncl.derived_core_potential(rr))
        Vatt = np.exp(-rr ** 2 / (2.0 * R0 ** 2))

        def pair_V(b, V0):
            P = (2 * np.pi * b ** 2) ** -1.5 * np.exp(-rr ** 2 / (2 * b ** 2)) \
                * 4 * np.pi * rr ** 2
            return float(((Vcent - V0 * Vatt) * P).sum() * dr)

        def Emin2(V0):
            bs = np.linspace(0.7, 4.5, 200)
            return min(0.75 * HBARC ** 2 / (M_N * b ** 2) + pair_V(b, V0)
                       for b in bs)

        lo, hi = 0.0, 600.0
        target = -abs(anchor)
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if Emin2(mid) > target else (lo, mid)
        V0 = mid
        self._nn_r = rr
        self._nn_V = Vcent - V0 * Vatt
        self._nn_Vprime = np.gradient(self._nn_V, rr)
        self._nn_meta = {"anchor_Eb_MeV": anchor, "V0_MeV": V0, "R0_fm": R0,
                         "V_min_MeV": float(self._nn_V.min())}

    def _nucleon_coms(self, fine_states):
        coms = []
        for grp in self._nuc_groups:
            d = None
            for nm in grp:
                fs = fine_states[nm]
                dd = (np.abs(fs["eta_u"]) ** 2 + np.abs(fs["eta_d"]) ** 2
                      + np.abs(fs["chi_u"]) ** 2
                      + np.abs(fs["chi_d"]) ** 2).sum(axis=0)
                d = dd if d is None else d + dd
            d = np.asarray(d.real if np.iscomplexobj(d) else d)
            coms.append(_centroid(d, self.Lf))
        return coms

    def _apply_nn_binding(self, fine_states):
        """Bind the A nucleons with the model NN OBE applied as a **Lorentz-
        scalar potential** (the MIT-bag / F135 confinement mechanism, not a
        force impulse — a scalar mass binds to a standing state, a vector kick
        only heats / Klein-tunnels).  Each nucleon i feels, on top of its own
        F135 Y-string, the superposed OBE field of the OTHER nucleons,

            S_i(x) = g_nn · Σ_{j≠i} V_pair(|x − R_j|)   (V_pair in MeV, F104/
                     F126/F128/F113; the attractive σ/π well is LOW scalar mass
                     ⇒ favourable, the ω + quark-Pauli core is HIGH mass ⇒
                     excluded), R_j the live nucleon COMs.

        Applied as one exactly-unitary η↔χ scalar-mass rotation θ=S_i per tick
        (`_mix_eta_chi_3d`, the same "Mix" factor the intra-nucleon string uses)
        — an operator-split inter-nucleon factor after the channel's kinetic +
        intra-confine step.  Norm-preserving for any θ."""
        from ca_dirac_bcc import _mix_eta_chi_3d
        coms = self._nucleon_coms(fine_states)
        Lf = self.Lf
        ax = np.arange(Lf)
        X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
        for i, grp in enumerate(self._nuc_groups):
            S = np.zeros((Lf, Lf, Lf))
            for j in range(len(self._nuc_groups)):
                if j == i:
                    continue
                Rj = np.asarray(coms[j])
                dx = (X - Rj[0] + Lf / 2.0) % Lf - Lf / 2.0
                dy = (Y - Rj[1] + Lf / 2.0) % Lf - Lf / 2.0
                dz = (Z - Rj[2] + Lf / 2.0) % Lf - Lf / 2.0
                r_fm = np.sqrt(dx * dx + dy * dy + dz * dz) * self.nn_scale
                S += np.interp(r_fm, self._nn_r, self._nn_V)   # MeV
            theta = self.g_nn * S
            for nm in grp:
                fs = fine_states[nm]
                eu, ed, xu, xd = _mix_eta_chi_3d(
                    fs["eta_u"], fs["eta_d"], fs["chi_u"], fs["chi_d"], theta)
                fs["eta_u"], fs["eta_d"], fs["chi_u"], fs["chi_d"] = eu, ed, xu, xd
                self._fine_ch_by_name[nm]._publish_currents(fs)

    def _fine_lat(self):
        from ..engine.simulation import LatticeSpec
        return LatticeSpec(L=self.Lf, topology="bcc",
                           c_lat=1.0 / float(np.sqrt(3.0)))

    # -- coarse potentials --------------------------------------------------
    def _nuclear_well(self, Q):
        """V_nuc(x) = −k·Q/r on the coarse grid (R_b-reduced +Z point)."""
        import ca_multigrid as mg
        cc = self.Lc // 2
        return mg.coarse_point_potential(self.Lc, (cc, cc, cc), k=self.e_k * Q)

    def _poisson(self, rho_pos):
        from casim.gravity import solve_poisson_3d_open
        return solve_poisson_3d_open(np.asarray(rho_pos, float), G_N=self.e_k)

    def _ee_potentials(self, psis):
        """Live Hartree: for each orbital i, V_ee,i(x) = repulsion from all
        OTHER electrons.  ρ_others,i = ρ_tot − |ψ_i|² (one electron of orbital i
        removed, mirroring ca_manybody._hartree_potential).  Poisson is linear,
        so φ(ρ_others,i) = φ_tot − φ(|ψ_i|²): one total solve + one per orbital.
        Repulsive sign: V_ee = −φ (φ is the attractive-convention potential of a
        positive source)."""
        dens = [np.abs(p) ** 2 for p in psis]
        rho_tot = np.zeros((self.Lc,) * 3)
        for occ, d in zip(self._occ, dens):
            rho_tot += occ * d
        phi_tot = self._poisson(rho_tot)
        Vees = []
        for d in dens:
            phi_others = phi_tot - self._poisson(d)
            Vees.append(-phi_others)
        return Vees

    # -- initial orbital relaxation (SCF) -----------------------------------
    def _seed_orbitals(self):
        import ca_multigrid as mg
        cc = self.Lc // 2
        ax = np.arange(self.Lc)
        X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
        r2 = (X - cc) ** 2 + (Y - cc) ** 2 + (Z - cc) ** 2
        psis = []
        for o in self._orbs:
            w = (self.Lc / 7.0) * (1.0 + 0.6 * (o["n"] - 1))   # wider for higher n
            ang = _angular_seed(o["l"], o["mi"], X, Y, Z, cc)
            psi = (ang * np.exp(-r2 / (2.0 * w ** 2))).astype(complex)
            nrm = np.sqrt((np.abs(psi) ** 2).sum())
            psis.append(psi / nrm if nrm > 0 else psi)
        return _gram_schmidt(psis)

    def _scf_relax(self, V_nuc):
        import ca_multigrid as mg
        psis = self._seed_orbitals()
        block = max(1, self.e_relax // max(1, self.e_scf))
        for _ in range(self.e_scf):
            Vees = self._ee_potentials(psis)
            new = []
            for psi, Vee in zip(psis, Vees):
                V = V_nuc + Vee
                new.append(mg.schrodinger_relax(psi, V, self.e_m, 1.0,
                                                block, self.e_dtau))
            psis = _gram_schmidt(new)
        return psis

    # -- engine interface ---------------------------------------------------
    def init_state(self, lattice, rng):
        Q = self._nuc_charge
        if self.free:
            # control: no well, seed compact packets, propagate ballistically
            psis = self._seed_orbitals()
            V_nuc = np.zeros((self.Lc,) * 3)
        else:
            V_nuc = self._nuclear_well(Q)
            psis = self._scf_relax(V_nuc)
        st = {"psis": psis, "nuc_charge": Q, "V_nuc": V_nuc, "tick": 0}
        if self._fine_chs:
            flat = self._fine_lat()
            for nm, ch in zip(self._fine_names, self._fine_chs):
                st[f"fine::{nm}"] = ch.init_state(flat, rng)
        return st

    def step(self, state, lattice, context=None, rng=None):
        import ca_multigrid as mg
        psis = state["psis"]
        tick = int(state.get("tick", 0)) + 1
        V_nuc = state["V_nuc"]
        Q = state["nuc_charge"]
        # Tier B: advance the live quark nucleons and re-derive the +Z well
        new_fine = {}
        if self._fine_chs:
            flat = self._fine_lat()
            ctx = {nm: state[f"fine::{nm}"] for nm in self._fine_names}
            for nm, ch in zip(self._fine_names, self._fine_chs):
                ctx[nm] = ch.step(ctx[nm], flat, context=ctx, rng=rng)
            # inter-nucleon binding: model NN OBE force as a unitary momentum kick
            if self.nn_binding and getattr(self, "_nuc_groups", None):
                self._apply_nn_binding(ctx)
            rho = None
            for nm in self._fine_names:
                r = ctx[nm].get("rho_em")
                if r is not None:
                    rho = r if rho is None else rho + r
            if rho is not None:
                Q = float(np.sum(rho))
                cc = self.Lc // 2
                V_nuc = mg.coarse_point_potential(self.Lc, (cc, cc, cc),
                                                  k=self.e_k * Q)
            new_fine = {f"fine::{nm}": ctx[nm] for nm in self._fine_names}
        # live Hartree mean field (recomputed on cadence)
        if self.free:
            Vees = [np.zeros((self.Lc,) * 3)] * len(psis)
        elif (tick % self.hartree_every) == 0 or "Vees" not in state:
            Vees = self._ee_potentials(psis)
        else:
            Vees = state["Vees"]
        # step every orbital in its own mean field (exactly unitary)
        out = []
        for psi, Vee in zip(psis, Vees):
            V = V_nuc + Vee
            out.append(mg.schrodinger_step(psi, V, self.e_m, 1.0, self.e_dt))
        if (not self.free) and (tick % self.gs_every) == 0:
            out = _gram_schmidt(out)             # Pauli antisymmetriser
        new = {"psis": out, "nuc_charge": Q, "V_nuc": V_nuc, "tick": tick,
               "Vees": Vees}
        new.update(new_fine)
        return new

    # -- diagnostics --------------------------------------------------------
    def density_field(self, state):
        d = np.zeros((self.Lc,) * 3)
        for occ, psi in zip(self._occ, state["psis"]):
            d += occ * np.abs(psi) ** 2
        return np.asarray(d)

    def _nucleus_density_fine(self, state):
        if self._fine_chs:
            d = None
            for nm in self._fine_names:
                fs = state[f"fine::{nm}"]
                dd = (np.abs(fs["eta_u"]) ** 2 + np.abs(fs["eta_d"]) ** 2
                      + np.abs(fs["chi_u"]) ** 2
                      + np.abs(fs["chi_d"]) ** 2).sum(axis=0)
                d = dd if d is None else d + dd
            return np.asarray(d.real if np.iscomplexobj(d) else d)
        return self._rho_matter_fine

    def energy(self, state) -> float:
        e = 0.0
        for occ, psi in zip(self._occ, state["psis"]):
            e += occ * float((np.abs(psi) ** 2).sum())
        e += float(self._nucleus_density_fine(state).sum())
        return e

    def observables(self, state, lattice) -> dict:
        import ca_multigrid as mg
        psis = state["psis"]
        cc = self.Lc // 2
        nuc_d = self._nucleus_density_fine(state)
        nuc_rms = mg._rms(nuc_d)
        cloud = self.density_field(state)
        cloud_rms = mg._rms(cloud)
        cloud_cen = _centroid(cloud, self.Lc)
        sep = float(np.sqrt(sum((cloud_cen[i] - cc) ** 2 for i in range(3))))
        shell_rms = [mg._rms(np.abs(p) ** 2) for p in psis]
        shell_norm = [float((np.abs(p) ** 2).sum()) for p in psis]
        Q = float(state.get("nuc_charge", 0.0))
        e_charge = self.e_charge * sum(self._occ)            # = −Z
        # represented geometry: cloud radius carries the block factor b
        rep_ratio = (cloud_rms * self.b / nuc_rms) if nuc_rms > 0 else 0.0
        # Tier-B loop liveness: ‖J_em‖, ‖rho_em‖ summed over the live quarks
        loop_live = None
        if self._fine_chs:
            jem = 0.0
            rem = 0.0
            for nm in self._fine_names:
                fs = state[f"fine::{nm}"]
                if fs.get("J_em") is not None:
                    jem += float(np.abs(fs["J_em"]).sum())
                if fs.get("rho_em") is not None:
                    rem += float(np.abs(fs["rho_em"]).sum())
            loop_live = {"J_em_norm": jem, "rho_em_norm": rem}
        return {
            "Z": self.Z, "N": self.N, "A": self.A, "b": self.b,
            "tier": "B(live quarks)" if self._fine_chs else "A(coarse nucleus)",
            "nuc_charge": Q,
            "electron_charge": e_charge,
            "net_charge": Q + e_charge,
            "n_orbitals": len(psis),
            "occupations": list(self._occ),
            "nucleus_rms_fine": nuc_rms,
            "cloud_rms_coarse": cloud_rms,
            "shell_rms_coarse": shell_rms,
            "shell_norm": shell_norm,
            "cloud_centroid_sep": sep,
            "cloud_surrounds_nucleus": bool(rep_ratio > 1.0),
            "max_orbital_overlap": _max_offdiag_overlap(psis),
            "represented_a0_over_rnuc": rep_ratio,
            "represented_decades": float(np.log10(rep_ratio)) if rep_ratio > 0 else None,
            "cloud_norm": float(cloud.sum()),
            "loop_liveness": loop_live,
        }


@register_observer
class AtomStabilityReadout(Observer):
    """Whole-atom stability readout for the F195 element atom: net charge,
    nucleus/cloud/shell RMS, cloud-surrounds-nucleus + centroid tracking, the
    represented a₀/r_nuc decades, and the Pauli orthogonality residual."""
    name = "atom_stability_readout"
    label = "Atom Stability Readout"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        for cname, ch in sim.channels.items():
            if isinstance(ch, ElementAtomChannel):
                rec = {"tick": sim.tick}
                rec.update(ch.observables(sim.states[cname], sim.lattice))
                self.records.append(rec)
