"""casim.engine.channels — concrete field channels.

Each channel is a thin, faithful wrapper over an audited ``ca-simulation``
kernel.  Wrapping (not reimplementing) is what guarantees the engine reproduces
the original scripts to machine precision: ``Channel.step`` calls exactly the
same pure function the historical scripts called.

Pilots (roadmap Phase C):
    photon_pair        γ even-law (F69)      ca_photon_pair.photon_step_spectral
    weyl_bcc           Weyl walk (per-branch) ca_bcc.weyl_step_3d_bcc
    gravity_dielectric F64 dielectric lens    poisson_open + canonical K=exp(2GM/rc²)
"""
from __future__ import annotations

import numpy as np

from .channel import Channel, register

ROOT3 = float(np.sqrt(3.0))


# ======================================================================
# 1. Paired-spinor photon — even law (F67/F68/F69)
# ======================================================================
@register
class PhotonPairChannel(Channel):
    type_name = "photon_pair"
    label = "Photon Pair"
    propagator = "even"          # forced (F91)
    topologies = ("cubic",)      # spectral (E,B) on a cubic FFT grid

    def init_state(self, lattice, rng):
        from casim.fields.photon import build_pair_mode, build_beam_packet
        L = lattice.L
        init = self.config.get("init", "random")
        if init == "random":
            E = rng.standard_normal((3, L, L, L))
            B = rng.standard_normal((3, L, L, L))
        elif init == "pair_mode":
            khat = self.config.get("khat", [1.0, 1.0, 1.0])
            e1 = self.config.get("e1", [1.0, -1.0, 0.0])
            m = int(self.config.get("m_index", 1))
            E, B, _e1, _e2 = build_pair_mode(L, m, khat, e1)
        elif init == "beam":
            # Travelling axis-aligned Gaussian packet (2026-06-06): one-sided
            # F = E + iB ⇒ moves in +axis at dΩ_pair/dk|k0 (see kernel doc).
            axis = self.config.get("axis", "x")
            axis = {"x": 0, "y": 1, "z": 2}.get(axis, axis)
            m = int(self.config.get("m_index", max(1, L // 8)))
            sigma = self.config.get("sigma", max(2.0, L / 8.0))  # scalar or [σx,σy,σz]
            pol = self.config.get("pol_axis")
            center = self.config.get("center")
            E, B, _k0 = build_beam_packet(
                L, m, axis=axis, pol_axis=pol, sigma=sigma, center=center)
        else:
            raise ValueError(f"photon_pair: unknown init {init!r}")
        return {"E": np.asarray(E, float), "B": np.asarray(B, float)}

    def step(self, state, lattice, context=None, rng=None):
        from casim.fields.photon import photon_step_spectral
        E, B = photon_step_spectral(state["E"], state["B"])
        return {"E": E, "B": B}

    def energy(self, state) -> float:
        return float(np.sum(state["E"] ** 2 + state["B"] ** 2))

    # F69 PP1: pair dispersion equals the even-law rotation rate (algebraic).
    def dispersion_residual(self, lattice, rng) -> float:
        from casim.fields.photon import pair_dispersion
        from casim.lattice import bcc_dispersion
        worst = 0.0
        for _ in range(2000):
            k = rng.standard_normal(3) * rng.uniform(0.01, 1.0)
            wp = bcc_dispersion(k[0] / 2, k[1] / 2, k[2] / 2, sign="+")
            wm = bcc_dispersion(k[0] / 2, k[1] / 2, k[2] / 2, sign="-")
            worst = max(worst, abs(pair_dispersion(*k) - (wp + wm)))
        return float(worst)


# ======================================================================
# 2. BCC Weyl walk — per-branch (exact unitary QCA)
# ======================================================================
@register
class WeylBCCChannel(Channel):
    type_name = "weyl_bcc"
    label = "Weyl BCC"
    propagator = "per-branch"
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        L = lattice.L
        f = (rng.standard_normal((L, L, L)) +
             1j * rng.standard_normal((L, L, L))).astype(np.complex128)
        g = (rng.standard_normal((L, L, L)) +
             1j * rng.standard_normal((L, L, L))).astype(np.complex128)
        return {"f": f, "g": g}

    def step(self, state, lattice, context=None, rng=None):
        from casim.lattice import weyl_step_3d_bcc
        sign = self.config.get("sign", "+")
        f, g = weyl_step_3d_bcc(state["f"], state["g"], sign=sign)
        return {"f": f, "g": g}

    def energy(self, state) -> float:
        return float(np.sum(np.abs(state["f"]) ** 2 + np.abs(state["g"]) ** 2))

    # Analytic dispersion check (ca_bcc.measure_bcc_dispersion).
    def dispersion_residual(self, lattice, rng) -> float:
        from casim.lattice import measure_bcc_dispersion
        sign = self.config.get("sign", "+")
        n_modes = int(self.config.get("n_modes", 12))
        return float(measure_bcc_dispersion(
            L=lattice.L, n_modes=n_modes, sign=sign, rng=rng))

    # ||U†U − I|| per mode (should be 0 analytically).
    def unitarity_residual(self, lattice, rng) -> float:
        from casim.lattice import bcc_unitarity_residual, make_kgrid_3d
        sign = self.config.get("sign", "+")
        KX, KY, KZ = make_kgrid_3d(lattice.L, lattice.L, lattice.L)
        return float(np.max(bcc_unitarity_residual(KX, KY, KZ, sign=sign)))


# ======================================================================
# 3. W± gauge field — chiral law (forced, F91)
# ======================================================================
@register
class WChiralChannel(Channel):
    """SU(2) W-field component propagated by the chirally-faithful F37 law
    (``ca_wmu.w_propagation_step_chiral``): F^± ride their own branch
    Ω^± = 2ω_±(k/2).  Chiral is *forced* (F91): the left-projector coupling
    has identically zero right-branch weight.  Birefringent, but the W is
    massive and not under the GRB/AGN polarimetry bound.
    """
    type_name = "w_chiral"
    label = "W Chiral"
    propagator = "chiral"
    topologies = ("cubic",)

    def init_state(self, lattice, rng):
        L = lattice.L
        E = rng.standard_normal((3, L, L, L))
        B = rng.standard_normal((3, L, L, L))
        return {"E": E, "B": B}

    def step(self, state, lattice, context=None, rng=None):
        from casim.fields.electroweak import w_propagation_step_chiral
        E, B = w_propagation_step_chiral(state["E"], state["B"])
        return {"E": E, "B": B}

    def energy(self, state) -> float:
        return float(np.sum(state["E"] ** 2 + state["B"] ** 2))


# ======================================================================
# 4. Z boson — even law (vector part; mass-suppressed axial split, F91)
# ======================================================================
@register
class ZEvenChannel(Channel):
    """Massless Z propagation via the even F26 rotation
    (``ca_z_field.z_propagation_step_spectral``) — the same law as γ.  The Z
    field here is a single real (E_Z, B_Z) pair."""
    type_name = "z_even"
    label = "Z Even"
    propagator = "even"
    topologies = ("cubic",)

    def init_state(self, lattice, rng):
        L = lattice.L
        return {"E": rng.standard_normal((L, L, L)),
                "B": rng.standard_normal((L, L, L))}

    def step(self, state, lattice, context=None, rng=None):
        from casim.fields.electroweak import ca_z_field
        E, B = ca_z_field.z_propagation_step_spectral(state["E"], state["B"])
        return {"E": E, "B": B}

    def energy(self, state) -> float:
        return float(np.sum(state["E"] ** 2 + state["B"] ** 2))


# ======================================================================
# 5. Gluon — even law on the BCC lattice (forced, F91; migrated 2026-06-04)
# ======================================================================
@register
class GluonBCCChannel(Channel):
    """Colour-octet (8,L,L,L) gluon field propagated by the even BCC law
    (``ca_gluon.gluon_rotation_step_spectral_bcc``).  Even is *forced* (F91):
    the colour coupling is branch-blind, so it can source only the
    helicity-symmetric dispersion."""
    type_name = "gluon_bcc"
    label = "Gluon BCC"
    propagator = "even"
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        L = lattice.L
        return {"E": rng.standard_normal((8, L, L, L)),
                "B": rng.standard_normal((8, L, L, L))}

    def step(self, state, lattice, context=None, rng=None):
        from casim.fields.strong import ca_gluon
        E, B = ca_gluon.gluon_rotation_step_spectral_bcc(state["E"], state["B"])
        return {"E": E, "B": B}

    def energy(self, state) -> float:
        return float(np.sum(state["E"] ** 2 + state["B"] ** 2))


# ======================================================================
# 6. F64 dielectric gravity — the gravity field element (mainlined)
# ======================================================================
@register
class GravityDielectricChannel(Channel):
    """The gravity field element: a lattice dielectric K(x[,t]) (F64).

    Two modes, selected by the ``dynamic`` config key:

    * ``dynamic: false`` (default, back-compat) — the original static lens:
      K(x) built once from an open-boundary Poisson potential of a Gaussian
      mass; the eikonal deflection observable compares against GR's 4GM/(c²b).
      Bit-identical to the pre-merge channel.

    * ``dynamic: true`` — the F64 fork mainlined (audit B.2 #1).  Φ is a
      genuine dynamical field (D-EM8 leapfrog, ``ca_gravity.phi_wave_step``):
      causal at ``c_g``, energy-carrying, static limit = the Poisson well.
      It is **sourced by matter channels** per the F106 law

          ∇²ln K = −(8πG/c⁴)·T⁰⁰[ψ]   (= −T⁰⁰ in lattice units, coupling 1)

      via ``sources: {channel_name: mass}`` — each named partner's state is
      read from the engine context and its rest-leg energy density
      ``mass·|Ψ|²`` (F106-E5; spinor states) or field energy ``(E²+B²)/2``
      (set mass 1.0; gauge states) accumulated into T⁰⁰.  ``coupling``
      defaults to the structural F106 value 1.0 (lattice units; equivalently
      G_LATTICE = 1/(72π)); overriding it is a scenario *scale* choice, not
      free physics.  An optional static Gaussian lens (``M > 0``) seeds the
      initial well; ``M: 0`` starts flat.

    Matter reads the field back through ``ParticleChannel``'s gravity
    coupling: scalar readouts always, and (massive Dirac singlets) the F62
    sign-corrected local lapse mix — two-way gravity in the production
    engine.  The kinetic-leg c_eff variation (deflection of *massless*
    packets) remains fork-level (`forks/gr_fork_F64_em_connection.py`):
    the spectral BCC kernels are homogeneous.
    """
    type_name = "gravity_dielectric"
    label = "Gravity Dielectric"
    propagator = "dielectric"
    # The Poisson/dielectric K(x) field is topology-agnostic; allowing "bcc"
    # lets particle scenarios (BCC matter kernels) carry a gravity field.
    topologies = ("cubic", "bcc")

    def init_state(self, lattice, rng):
        from casim.gravity import gaussian_mass_3d, solve_poisson_3d_open
        L = lattice.L
        M = float(self.config.get("M", 1.0))
        sigma = float(self.config.get("sigma", 3.0))
        G = float(self.config.get("G", 1.0))
        c = float(getattr(lattice, "c_lat", 1.0 / ROOT3))
        if M:
            rho = gaussian_mass_3d(L, M=M, sigma=sigma)
            phi = solve_poisson_3d_open(rho, G_N=G)
        else:
            phi = np.zeros((L, L, L))
        # Newtonian φ < 0; canonical index K = exp(2GM/rc²) = exp(-2φ/c²).
        K = np.exp(-2.0 * phi / (c ** 2))
        state = {"phi": phi, "K": K, "M": M, "G": G, "c": c}
        if self.config.get("dynamic", False):
            state["phi_prev"] = phi.copy()      # leapfrog memory (D-EM8)
        return state

    # -- F106 source assembly (dynamic mode) ---------------------------
    def _source_T00(self, context, shape):
        """Accumulate T⁰⁰ from the configured matter channels (F106)."""
        from casim.gravity import T00_dirac_rest, T00_field_energy
        T00 = np.zeros(shape)
        sources = self.config.get("sources", {}) or {}
        if not context:
            return T00
        for name, weight in sources.items():
            st = context.get(name)
            if not st:
                continue
            w = float(weight)
            if "eta_u" in st:                   # massive Dirac singlet
                T00 = T00 + T00_dirac_rest(st["eta_u"], st["eta_d"],
                                           st["chi_u"], st["chi_d"], m=w)
            elif "f" in st and "g" in st:       # Weyl/quark packet
                d = np.abs(st["f"]) ** 2 + np.abs(st["g"]) ** 2
                while d.ndim > 3:
                    d = d.sum(axis=0)
                T00 = T00 + w * d.real
            elif "f_nu" in st:                  # left doublet
                d = (np.abs(st["f_nu"]) ** 2 + np.abs(st["f_e"]) ** 2
                     + np.abs(st["g_nu"]) ** 2 + np.abs(st["g_e"]) ** 2)
                T00 = T00 + w * d.real
            elif "E" in st and "B" in st:       # gauge field energy (D-EM3)
                T00 = T00 + w * T00_field_energy(st["E"], st["B"])
        return T00

    def step(self, state, lattice, context=None, rng=None):
        if not self.config.get("dynamic", False):
            # Static background — the lens does not evolve (back-compat).
            return state
        from casim.gravity import (F106_COEFF_LATTICE, phi_source,
                                   phi_wave_step)
        c = state["c"]
        c_g = float(self.config.get("c_g", c))
        dt = float(self.config.get("dt", 1.0))
        coupling = float(self.config.get("coupling", F106_COEFF_LATTICE))
        T00 = self._source_T00(context, state["phi"].shape)
        src = phi_source(T00, c, coupling=coupling)
        phi_new, phi_old = phi_wave_step(state["phi"], state["phi_prev"],
                                         src, c_g, dt)
        new = dict(state)
        new["phi"], new["phi_prev"] = phi_new, phi_old
        new["K"] = np.exp(-2.0 * phi_new / (c ** 2))
        return new

    def energy(self, state) -> float:
        if self.config.get("dynamic", False) and "phi_prev" in state:
            # Dynamical field energy ½Σ(∂_tΦ)² + ½c_g²Σ|∇Φ|² (D-EM8).
            from casim.gravity import phi_field_energy
            c_g = float(self.config.get("c_g", state["c"]))
            dt = float(self.config.get("dt", 1.0))
            return phi_field_energy(state["phi"], state["phi_prev"], c_g, dt)
        # "Energy" proxy: the dielectric excess ∫(K−1), a conserved background.
        return float(np.sum(state["K"] - 1.0))

    def observables(self, state, lattice) -> dict:
        """Eikonal deflection of a ray with impact parameter b, vs GR.

        For a thin lens the photon picks up a transverse bend
        Δθ = ∫ ∂_⊥ (2φ/c²) dl along the line of sight.  For a point mass this
        integrates to the Einstein value 4GM/(c²b).  We integrate the actual
        lattice potential along a line at impact parameter b and report the
        measured deflection and the analytic GR value.

        Dynamic mode adds the field diagnostics (well depth, K extrema,
        Φ-field energy); the GR-lens comparison is reported only when a
        static seed mass M > 0 gives it meaning.
        """
        extra = {}
        if self.config.get("dynamic", False):
            extra = {
                "dynamic": True,
                "phi_min": float(np.min(state["phi"])),
                "phi_max": float(np.max(state["phi"])),
                "K_max": float(np.max(state["K"])),
                "K_min": float(np.min(state["K"])),
                "field_energy": self.energy(state),
            }
            if not state["M"]:
                return extra
            # fall through: with a static seed the lens numbers stay meaningful
        phi = state["phi"]
        c = state["c"]
        L = lattice.L
        b = int(self.config.get("impact_parameter", max(4, L // 6)))
        cen = L // 2
        # Line of sight along +x at (y = cen + b, z = cen); central difference
        # in y of the path-integrated 2φ/c² gives the transverse deflection.
        def path_integral(y):
            col = phi[:, y, cen]                       # φ along x at fixed (y,z)
            return np.sum(2.0 * col / (c ** 2))        # ∫ 2φ/c² dx  (dx=1)
        yb = cen + b
        # Deflection points toward the mass; the physical observable is the
        # magnitude. Central difference of the path-integrated index in b.
        dtheta_meas = abs((path_integral(yb + 1) - path_integral(yb - 1)) / 2.0)
        GM = state["G"] * state["M"]
        dtheta_gr = 4.0 * GM / (c ** 2 * b)
        # The line integral spans a finite aperture X (centre→edge), so the
        # exact lattice prediction is GR scaled by X/sqrt(X²+b²) (the tails of
        # ∫ 2GMb/r³ dx that the finite box omits). Compare against that.
        X = float(cen)
        aperture = X / np.sqrt(X ** 2 + b ** 2)
        dtheta_gr_box = dtheta_gr * aperture
        rel = abs(dtheta_meas - dtheta_gr_box) / abs(dtheta_gr_box) if dtheta_gr_box else float("nan")
        return {
            "impact_parameter": b,
            "deflection_measured": float(dtheta_meas),
            "deflection_GR_4GM_over_c2b": float(dtheta_gr),
            "deflection_GR_finite_aperture": float(dtheta_gr_box),
            "aperture_factor": float(aperture),
            "rel_error": float(rel),
            "K_max": float(np.max(state["K"])),
            **extra,
        }
