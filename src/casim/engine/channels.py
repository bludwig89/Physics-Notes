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
    propagator = "even"          # forced (F91)
    topologies = ("cubic",)      # spectral (E,B) on a cubic FFT grid

    def init_state(self, lattice, rng):
        from casim.fields.photon import build_pair_mode
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
# 6. F64 dielectric gravity — canonical K = exp(2GM/rc²) lens
# ======================================================================
@register
class GravityDielectricChannel(Channel):
    """A static lattice dielectric K(x) built from an open-boundary Poisson
    potential of a Gaussian mass (pure numpy).  The channel's payload is the
    eikonal light-deflection observable, compared to GR's 4GM/(c²b).

    This is the F64 fork's go/no-go (D-EM2): a single impedance-matched
    dielectric (A=1/K, B=K) gives the factor-2 (Einstein) bend.  The dynamical
    variable-c Weyl propagation (``ca_curved``, SciPy) is available as a
    separate path; this pilot stays numpy-only so it is reproducible anywhere.
    """
    type_name = "gravity_dielectric"
    propagator = "dielectric"
    # The static Poisson K(x) background is topology-agnostic; allowing "bcc"
    # lets particle scenarios (BCC matter kernels) carry a gravity background.
    topologies = ("cubic", "bcc")

    def init_state(self, lattice, rng):
        from casim.gravity import gaussian_mass_3d, solve_poisson_3d_open
        L = lattice.L
        M = float(self.config.get("M", 1.0))
        sigma = float(self.config.get("sigma", 3.0))
        G = float(self.config.get("G", 1.0))
        c = float(getattr(lattice, "c_lat", 1.0 / ROOT3))
        rho = gaussian_mass_3d(L, M=M, sigma=sigma)
        phi = solve_poisson_3d_open(rho, G_N=G)
        # Newtonian φ < 0; canonical index K = exp(2GM/rc²) = exp(-2φ/c²).
        K = np.exp(-2.0 * phi / (c ** 2))
        return {"phi": phi, "K": K, "M": M, "G": G, "c": c}

    def step(self, state, lattice, context=None, rng=None):
        # Static background — the lens does not evolve.
        return state

    def energy(self, state) -> float:
        # "Energy" proxy: the dielectric excess ∫(K−1), a conserved background.
        return float(np.sum(state["K"] - 1.0))

    def observables(self, state, lattice) -> dict:
        """Eikonal deflection of a ray with impact parameter b, vs GR.

        For a thin lens the photon picks up a transverse bend
        Δθ = ∫ ∂_⊥ (2φ/c²) dl along the line of sight.  For a point mass this
        integrates to the Einstein value 4GM/(c²b).  We integrate the actual
        lattice potential along a line at impact parameter b and report the
        measured deflection and the analytic GR value.
        """
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
        }
