"""casim.engine.core.coupled — Tier-2 sourced / coupled channels.

These channels read a *partner* channel's live state via the engine's coupling
context (see ``Channel.step``), so a gauge field can be sourced by a matter
current and act back on the matter within the same tick.  The migration map's
Tier-2 sectors:

  * ``fermion_doublet`` + ``w_sourced`` — the closed fermion↔W back-reaction
    loop (E2E B1): the doublet current sources the W field; the W potential,
    exponentiated into SU(2) links, acts back on the doublet.
  * ``charge_photon`` — F87 charge→field: the sourced paired-photon Maxwell
    curl driven by a (divergence-free) charge current, with a Gauss-law
    observable.
  * ``beta_decay`` — F54 d→u+W⁻: the quark charged current emits a W⁻ (the
    vertex), which then propagates as a massive Proca field.

Each wraps audited ``ca-simulation`` kernels; the small helpers below
(``su2_expmap``, ``gaussian_packet``, ``field_energy``) are the pure-math
utilities the E2E test defined locally, replicated here verbatim so the engine
reproduces it bit-for-bit.
"""
from __future__ import annotations

import numpy as np

from .channel import Channel, register

ROOT3 = float(np.sqrt(3.0))
_SQRT2 = float(np.sqrt(2.0))


# ----------------------------------------------------------------------
# Pure-math helpers (verbatim from test_E2E_nonabelian_bilinear.py).
# ----------------------------------------------------------------------
def field_energy(E, B) -> float:
    """U = ½ Σ (E² + B²)."""
    return 0.5 * float(np.sum(E ** 2) + np.sum(B ** 2))


def su2_expmap(A):
    """Site-wise SU(2) exponential U(x)=exp(i A^a τ^a/2), A:(3,L,L,L) real.
    Returns (U_a, U_b) in the make_w_link_field convention. Pure cos/sin."""
    theta = np.sqrt(A[0] ** 2 + A[1] ** 2 + A[2] ** 2)
    safe = np.where(theta > 1e-300, theta, 1.0)
    s = np.sin(theta / 2.0) / safe
    sn1, sn2, sn3 = A[0] * s, A[1] * s, A[2] * s
    U_a = np.cos(theta / 2.0) + 1j * sn3
    U_b = -sn2 + 1j * sn1
    return U_a, U_b


def gaussian_packet(L, center, width, k0=None):
    """Normalised complex Gaussian packet on an L³ lattice."""
    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r2 = ((X - center[0]) ** 2 + (Y - center[1]) ** 2 + (Z - center[2]) ** 2)
    psi = np.exp(-r2 / (2.0 * width ** 2)).astype(complex)
    if k0 is not None:
        psi = psi * np.exp(1j * (k0[0] * X + k0[1] * Y + k0[2] * Z))
    return psi / np.sqrt(np.sum(np.abs(psi) ** 2))


# ======================================================================
# 1. fermion ↔ W back-reaction (E2E B1) — two coupled channels
# ======================================================================
@register
class WSourcedChannel(Channel):
    """W triplet field sourced by a partner fermion doublet's isospin current.

    Per tick (matching ``_run_loop``): J = current(partner); free rotation of
    (E,B); E += g·J; the gauge potential A accumulates E.  Register this
    BEFORE the fermion channel so it consumes the *pre-tick* doublet and
    publishes the *updated* A for the fermion's covariant step this tick.
    """
    type_name = "w_sourced"
    label = "W Sourced"
    propagator = "chiral"          # W law (F37/F91)
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        L = lattice.L
        z = np.zeros((3, L, L, L))
        return {"E": z.copy(), "B": z.copy(), "A": z.copy()}

    def step(self, state, lattice, context=None, rng=None):
        from casim.engine.gauge import weak_wmu as ca_wmu

        partner = self.config.get("fermion", "fermion_doublet")
        g_lat = float(self.config.get("g_lat", 0.5))
        fs = context[partner]
        J = ca_wmu.fermion_isospin_current(fs["f_nu"], fs["f_e"])
        E_rot, B_rot = ca_wmu.w_propagation_step_spectral(state["E"], state["B"])
        E = E_rot + g_lat * J
        B = B_rot
        A = state["A"] + E
        return {"E": E, "B": B, "A": A}

    def energy(self, state) -> float:
        return field_energy(state["E"], state["B"])


@register
class FermionDoubletChannel(Channel):
    """Left-handed SU(2) doublet (ν,e) advanced by the covariant BCC Weyl step,
    with links built from the partner W channel's accumulated potential A.

    Register this AFTER the W channel so it reads the A updated this tick."""
    type_name = "fermion_doublet"
    label = "Fermion Doublet"
    propagator = "per-branch"
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        L = lattice.L
        width = float(self.config.get("width", 1.5))
        f_nu = gaussian_packet(L, (L // 2, L // 2, L // 2), width, k0=(0.5, 0, 0))
        f_e = gaussian_packet(L, (L // 2 - 1, L // 2, L // 2), width)
        return {"f_nu": f_nu, "f_e": f_e,
                "g_nu": np.zeros_like(f_nu), "g_e": np.zeros_like(f_e)}

    def step(self, state, lattice, context=None, rng=None):
        from casim.engine.gauge import weak_wmu as ca_wmu

        partner = self.config.get("w_field", "w_sourced")
        eps = float(self.config.get("eps", 0.05))
        sign = self.config.get("sign", "+")
        A = context[partner]["A"]
        U_a, U_b = su2_expmap(eps * A)
        U_links = [(U_a, U_b)] * 8
        f_nu, f_e, g_nu, g_e = ca_wmu.covariant_weyl_step_3d_bcc(
            state["f_nu"], state["f_e"], state["g_nu"], state["g_e"],
            U_links, sign=sign)
        return {"f_nu": f_nu, "f_e": f_e, "g_nu": g_nu, "g_e": g_e}

    def energy(self, state) -> float:
        return float(np.sum(np.abs(state["f_nu"]) ** 2 + np.abs(state["f_e"]) ** 2
                            + np.abs(state["g_nu"]) ** 2 + np.abs(state["g_e"]) ** 2))

    def density_field(self, state):
        d = (np.abs(state["f_nu"]) ** 2 + np.abs(state["f_e"]) ** 2
             + np.abs(state["g_nu"]) ** 2 + np.abs(state["g_e"]) ** 2)
        return np.asarray(d.real if np.iscomplexobj(d) else d)


# ======================================================================
# 2. F87 charge → field: sourced paired-photon Maxwell curl
# ======================================================================
@register
class ChargePhotonChannel(Channel):
    """Paired-photon (E,B) driven by a static, divergence-free charge current J
    via ``ca_charge_coupling.maxwell_curl_step``.  Self-coupled to its own
    fixed source (stored in state); a Gauss-law observable tracks ∇·E−ρ."""
    type_name = "charge_photon"
    label = "Charge Photon"
    propagator = "even"            # paired photon (F69)
    topologies = ("cubic",)

    def init_state(self, lattice, rng):
        from casim.engine.gauge import charge_coupling as cc
        from casim.numerics import fft as _fft  # C1.3: the seam
        from casim.engine.lattice.geometry import make_kgrid_3d
        L = lattice.L
        amp = float(self.config.get("amp", 0.2))
        sigma = float(self.config.get("sigma", 2.0))
        # Build a current that is divergence-free under the *model's* BCC curl
        # symbol C(k):  J = i C × A_src in k-space (so C·J ≡ 0 exactly), with a
        # localized real vector potential A_src.  For real A_src this J is also
        # exactly real (C is odd, i C× preserves Hermiticity).
        x = np.arange(L)
        X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
        c = L // 2
        blob = amp * np.exp(-(((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2)
                              / (2.0 * sigma ** 2)))
        A_src = np.array([blob, 0.5 * np.roll(blob, 1, 0), np.zeros_like(blob)])
        KX, KY, KZ = make_kgrid_3d(L, L, L)
        Cx, Cy, Cz = cc.bcc_curl_symbol(KX, KY, KZ)
        Ak = [_fft.fftn(A_src[a]) for a in range(3)]
        Jx, Jy, Jz = cc._cross_k(Cx, Cy, Cz, *Ak)        # C × A  (in k)
        J = np.array([_fft.ifftn(1j * comp).real for comp in (Jx, Jy, Jz)])
        return {"E": np.zeros((3, L, L, L)), "B": np.zeros((3, L, L, L)),
                "J": J}

    def step(self, state, lattice, context=None, rng=None):
        from casim.engine.gauge import charge_coupling as cc
        dt = float(self.config.get("dt", 0.1))
        E, B = cc.maxwell_curl_step(state["E"], state["B"], J=state["J"], dt=dt)
        return {"E": E, "B": B, "J": state["J"]}

    def energy(self, state) -> float:
        return float(np.sum(state["E"] ** 2 + state["B"] ** 2))

    def observables(self, state, lattice) -> dict:
        from casim.engine.gauge import charge_coupling as cc
        # Charge continuity: ρ should track −∫ i C·J dt; here we report the
        # divergence of the current (should be ~0 for the loop source) and the
        # field energy injected.
        divJ = cc.div_from_current(state["J"])
        return {"div_J_max": float(np.max(np.abs(divJ))),
                "field_energy": self.energy(state)}


# ======================================================================
# 3. F54 β-decay: d → u + W⁻ vertex, then Proca propagation
# ======================================================================
@register
class BetaDecayChannel(Channel):
    """A localized left-handed quark doublet (u,d) emits a W⁻ via the charged
    current (the d→u+W⁻ vertex, ``ca_charged_current.emit_w_minus``) on the
    first tick, after which the W⁻ propagates as a massive Proca field.
    Reproduces the field trajectory of ``run_beta_decay_pipeline``."""
    type_name = "beta_decay"
    label = "Beta Decay"
    propagator = "chiral"
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        from casim.engine.gauge import charged_current as cc
        L = lattice.L
        sigma = float(self.config.get("sigma", 1.5))
        site_A = (L // 4, L // 2, L // 2)
        profA = cc.gaussian_blob((L, L, L), site_A, sigma)
        f_u = profA.astype(complex) * (0.9 + 0.0j)
        f_d = profA.astype(complex) * (0.7 * np.exp(0.3j))
        return {"E_W": np.zeros((3, L, L, L)), "B_W": np.zeros((3, L, L, L)),
                "f_u": f_u, "f_d": f_d, "emitted": 0}

    def step(self, state, lattice, context=None, rng=None):
        from casim.engine.gauge import charged_current as cc
        g_lat = float(self.config.get("g_lat", 0.8))
        m_W = float(self.config.get("m_W", 0.6))
        if not state["emitted"]:
            E_W, B_W, _dE = cc.emit_w_minus(state["E_W"], state["B_W"],
                                            state["f_u"], state["f_d"],
                                            g_lat=g_lat, dt=1.0)
            emitted = 1
        else:
            E_W, B_W = cc.w_massive_propagation_step_spectral(
                state["E_W"], state["B_W"], m_W, dt=1.0)
            emitted = 1
        return {"E_W": E_W, "B_W": B_W,
                "f_u": state["f_u"], "f_d": state["f_d"], "emitted": emitted}

    def energy(self, state) -> float:
        return float(np.sum(state["E_W"] ** 2 + state["B_W"] ** 2))

    def density_field(self, state):
        d = (state["E_W"] ** 2 + state["B_W"] ** 2).sum(axis=0)
        return np.asarray(d)
