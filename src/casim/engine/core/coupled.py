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
  * ``fermion_em`` + ``em_photon`` — Stage 4 of ``docs/roadmaps/photon-
    fermion-coupling.md``: the closed fermion↔photon U(1) back-reaction
    loop, mirroring ``fermion_doublet``/``w_sourced`` exactly. The charged
    Weyl fermion's F384 conserved current sources the paired-photon
    ``(E,B)``; the photon's F386 Coulomb-gauge-solved potential ``A`` acts
    back on the fermion via F385's per-link covariant step.

Each wraps audited engine kernels; the small helpers below
(``su2_expmap``, ``gaussian_packet``, ``field_energy``) are the pure-math
utilities the E2E test defined locally, replicated here verbatim so the engine
reproduces it bit-for-bit.
"""
from __future__ import annotations

import numpy as np

from .channel import Channel, register, registered_channels

ROOT3 = float(np.sqrt(3.0))
_SQRT2 = float(np.sqrt(2.0))


# ----------------------------------------------------------------------
# Pure-math helpers (verbatim from test_E2E_nonabelian_bilinear.py).
# ----------------------------------------------------------------------
#: The engine's one gauge-field energy convention (P3.5).  This module used to
#: define it and the four ``channels.py`` gauge channels used the other one; the
#: definition now lives in ``channel.py`` so there is exactly one, and this name
#: is kept because it is the one the E2E bilinear tests import.
from .channel import field_energy  # noqa: F401  (re-export, P3.5)


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
        from casim.engine.gauge import photon as _ph
        from casim.engine.lattice.geometry import make_kgrid_3d
        dt = float(self.config.get("dt", 0.1))
        # Even law (F69/F91): rotate at the paired-photon Ω_pair(k), not |C(k)|
        # (they agree only to O(k³)); changed 2026-09-29 so `propagator =
        # "even"` is true.  config `rate: curl` restores the |C| step.
        rate = None
        if self.config.get("rate", "pair") == "pair":
            KX, KY, KZ = make_kgrid_3d(*state["E"].shape[1:])
            rate = _ph.pair_dispersion(KX, KY, KZ)
        E, B = cc.maxwell_curl_step(state["E"], state["B"], J=state["J"], dt=dt,
                                    rate=rate)
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
            # W± propagate on the chiral law (F91, forced); was the even
            # Proca step before 2026-09-29.
            E_W, B_W = cc.w_massive_propagation_step_chiral(
                state["E_W"], state["B_W"], m_W, dt=1.0)
            emitted = 1
        return {"E_W": E_W, "B_W": B_W,
                "f_u": state["f_u"], "f_d": state["f_d"], "emitted": emitted}

    def energy(self, state) -> float:
        return float(np.sum(state["E_W"] ** 2 + state["B_W"] ** 2))

    def density_field(self, state):
        d = (state["E_W"] ** 2 + state["B_W"] ** 2).sum(axis=0)
        return np.asarray(d)


# ======================================================================
# 4. Stage 4 of docs/roadmaps/photon-fermion-coupling.md: fermion <-> photon
#    (U(1)) back-reaction -- two coupled channels, mirroring #1 exactly.
# ======================================================================
@register
class EmPhotonChannel(Channel):
    """Paired-spinor photon (E,B) sourced by a partner charged Weyl fermion's
    F384 conserved U(1) current.  Mirrors ``WSourcedChannel``'s pattern for
    the transverse (radiative) sector, U(1) in place of SU(2) -- but sources
    it via **F387's split-sourcing fix**, not the roadmap's own naive
    ``E += g·J`` sketch (see below for why).

    Per tick (matching ``_run_loop``): ``J = conserved_current(partner)``
    (F384, always purely ``Ĉ(k)``-longitudinal by construction), split into
    ``(J_T, J_L)`` (``gauge.em_photon_sourcing.split_transverse_longitudinal``
    -- the *same* ``Ĉ(k)`` projector ``solve_A_coulomb_3d`` builds inline, F387).
    Free rotation of ``(E,B)`` at ``Ω_pair`` (``gauge.photon
    .photon_step_spectral``, the canonical paired-photon law, decision 5);
    ``E += g_lat·J_T`` (transverse source only); the accumulated charge
    density ``ρ`` is advanced by the model's own continuity law
    ``∂_tρ=−iĈ·J`` (F384) and the longitudinal Coulomb field ``E_L`` solved
    **algebraically** each tick from the instantaneous Gauss law
    ``iĈ·E_L=−ρ`` (engine sign, ∂_tE=…+gJ) -- ``B_L`` is never populated, so ``iĈ·B=0`` holds by
    construction, not cancellation (F387 §3-4).  The gauge potential ``A`` is
    **solved**, not accumulated -- F386's Coulomb-gauge
    ``charge_coupling.solve_A_coulomb_3d(B)``, a pure function of the
    *current* ``B`` recomputed fresh every tick (F386's own decisive
    argument: an accumulated ``A`` cannot filter out longitudinal content a
    real current deposits; a solved one discards it by construction -- and
    now, post-F387, ``B`` never carries any in the first place). Register
    this BEFORE the fermion channel so it consumes the *pre-tick* fermion
    and publishes the *updated* ``A`` for the fermion's covariant step this
    tick.

    **Why not the roadmap's literal ``E += g·J`` sketch.** F386 §5 found that
    recipe drives a genuine ``iĈ·B≠0`` ("no magnetic monopoles") violation.
    The cause is **structural, not a value-mismatch** (F387's own review
    corrected this by elimination, 2026-09-15: substituting ``|Ĉ_odd(k)|``
    exactly for ``Ω_pair(k)`` does not shrink the defect) — ``Ω_pair(k)``
    performs **no ``Ĉ(k)``-projection whatsoever**, a property of *any*
    scalar per-mode rotation law regardless of whether its value happens to
    match ``|Ĉ_odd(k)|``, so a purely-``Ĉ``-longitudinal current sourced
    through it rotates into an equally longitudinal, nonzero ``B`` either
    way. F387 traced the *fix* to an exact structural fact — the ``Ω_pair``
    rotation commutes exactly with the ``Ĉ(k)``-transverse/longitudinal
    split (verified `~3e-14`, ``rotation_commutes_with_TL_projection``) — so
    the transverse and longitudinal sectors never mix under free propagation; splitting the
    *source* once, at sourcing time, is therefore an exact fix, not a
    heuristic patch. This channel is the first place that fix is wired into
    a live, dynamical (not F386/F387's static-current-harness) coupled loop:
    ``J`` is recomputed from the partner's *live* state every tick, so
    ``ρ``'s continuity update genuinely tracks a changing current.

    **Scope limitation, disclosed not fixed here.** ``E_L`` (the Coulomb
    field the fermion's own charge sources) is computed and exposed
    (``observables``, state key ``"E_L"``) but is **not** fed back to the
    fermion this stage — Stage 2's per-link step (F385) is a vector-
    potential-only (magnetic-type, Peierls-phase) mechanism; the roadmap's
    own §1.2 diagnosis names the *scalar*-potential/electrostatic force as
    the site-local wrap's (``minimal_coupling.u1_wrap_weyl_step_3d_bcc``)
    job, not Stage 2's. Wiring ``E_L`` back in (e.g. via a time-varying
    ``u1_wrap`` angle, matching the "Bloch acceleration" mechanism F385 §5b
    already found exact for a uniform gradient) is future work, not
    attempted here.

    **F389 — ``use_radiative_current`` (default ``False``, backward
    compatible).** F388's own review found ``J``'s transverse projection is
    always ``2×10⁻¹⁶`` (floating-point noise) because F384's
    ``conserved_current`` is purely ``Ĉ(k)``-longitudinal *by construction*
    — so with the default config this channel cannot radiate, and this is
    unchanged (every existing scenario/test that does not pass this flag
    gets bit-identical behaviour to F388). Passing ``use_radiative_current=
    True`` sources ``E_T`` from ``gauge.em_current.full_current`` instead of
    ``conserved_current`` — F384's exact longitudinal solution plus
    ``noether_transverse_current``'s addition (the continuum Noether
    current's own transverse projection, which continuity leaves completely
    unconstrained). See ``findings/F389-radiative-transverse-em-current.md``
    for the derivation and its own disclosed limitation: this lets the loop
    radiate and lets ``core.observers.Momentum`` see genuine field momentum
    for the first time, but does not make the loop exactly momentum-
    conserving (the fermion's per-link recoil and this current's field-
    sourcing were derived independently, not as two halves of one covariant
    action, so they are not order-matched in ``g_lat``).
    """
    type_name = "em_photon"
    label = "EM Photon"
    propagator = "even"            # paired photon (F69), Ω_pair law
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        L = lattice.L
        z = np.zeros((3, L, L, L))
        E, B = z.copy(), z.copy()
        # Optional Stage-5 (F390) beam seed, config `beam_amp` (default 0 --
        # no beam, F388/F389's own self-sourced-only convention).  Projected
        # onto the Ĉ(k)-transverse subspace before injection, same reason
        # F388/F389/F390's own harnesses do: `photon.build_beam_packet`
        # polarizes transverse to Euclidean k-hat, not Ĉ(k) (F386 §6).
        # `beam_polarization` (default "linear", F392 backward-compat
        # default): F390's original beam has E and B in the SAME Cartesian
        # component (E||B pointwise, Sigma ExB==0 identically, F392 §Part A)
        # -- "circular" is F392's fix, a genuine null Riemann-Silberstein
        # field carrying real Poynting momentum.
        beam_amp = float(self.config.get("beam_amp", 0.0))
        if beam_amp:
            from casim.engine.gauge.photon import build_beam_packet
            from casim.engine.gauge.em_photon_sourcing import (
                split_transverse_longitudinal)
            m_index = int(self.config.get("beam_m_index", 2))
            axis = int(self.config.get("beam_axis", 0))
            sigma = float(self.config.get("beam_sigma", 3.0))
            beam_polarization = self.config.get("beam_polarization", "linear")
            Eb, Bb, _k0vec = build_beam_packet(L, m_index=m_index, axis=axis,
                                               sigma=sigma,
                                               polarization=beam_polarization)
            Eb_T, _EbL = split_transverse_longitudinal(Eb)
            Bb_T, _BbL = split_transverse_longitudinal(Bb)
            E = E + beam_amp * Eb_T
            B = B + beam_amp * Bb_T
        return {"E": E, "B": B, "A": z.copy(), "rho": np.zeros((L, L, L))}

    def step(self, state, lattice, context=None, rng=None):
        from casim.engine.gauge import photon as ca_photon
        from casim.engine.gauge import em_current
        from casim.engine.gauge import charge_coupling as cc
        from casim.engine.gauge.em_photon_sourcing import (
            split_transverse_longitudinal)
        from casim.engine.lattice.geometry import make_kgrid_3d
        from casim.numerics import fft as _fft

        partner = self.config.get("fermion", "fermion_em")
        g_lat = float(self.config.get("g_lat", 0.5))
        q = float(self.config.get("q", 1.0))
        sign = self.config.get("sign", "+")
        # Declared control for F387-style adjudication (`use_naive_sourcing`):
        # revert to the roadmap's own, F386/F387-broken, unsplit `E += g.J`
        # recipe -- lets the coupled-channel no-monopole leg prove it CAN
        # fail under a genuinely dynamical current, not just F387's static
        # harness.
        use_naive_sourcing = bool(self.config.get("use_naive_sourcing", False))
        # F389: fixes F384's declared-open transverse gauge freedom with the
        # continuum Noether current's own Ĉ(k)-transverse projection, which
        # continuity leaves completely unconstrained. Default False keeps
        # this channel bit-identical to F388 for every caller that does not
        # opt in (see class docstring).
        use_radiative_current = bool(
            self.config.get("use_radiative_current", False))
        fs = context[partner]
        if use_radiative_current:
            J, _res, _gap = em_current.full_current(fs["f"], fs["g"],
                                                     sign=sign, q=q)
        else:
            J, _res, _gap = em_current.conserved_current(fs["f"], fs["g"],
                                                          sign=sign, q=q)
        J_T, _J_L = split_transverse_longitudinal(J)
        J_source = J if use_naive_sourcing else J_T

        E_rot, B_rot = ca_photon.photon_step_spectral(state["E"], state["B"])
        # Engine sign convention ∂_tE = … + g·J.  This is the sign the fermion
        # side's Peierls phase is paired with: flipping it alone makes field and
        # matter momenta parallel (F390 fails).  The Gauss-law sector below is
        # aligned to it (2026-09-29).
        E = E_rot + g_lat * J_source
        B = B_rot                  # B_L never populated (F387 §3-4)

        # rho advanced by the model's own continuity law (F384); E_L solved
        # algebraically from the instantaneous Gauss law i.C.E_L = -rho (engine sign) --
        # same C(k) machinery solve_A_coulomb_3d/em_current already use.
        shape = J.shape[1:]
        KX, KY, KZ = make_kgrid_3d(*shape)
        Cx, Cy, Cz = cc.bcc_curl_symbol(KX, KY, KZ)
        C2 = Cx ** 2 + Cy ** 2 + Cz ** 2
        nz = C2 > 1e-14
        # `g_lat` scales the SAME physical current for both sectors -- using
        # it only on E_T's source and not here would source the Coulomb
        # sector at full strength while under-sourcing the radiative sector,
        # an inconsistency caught in review (a blind re-derivation used a
        # different, consistent convention independently; F387's own static-
        # current harness has this same inconsistency, undisclosed there).
        Jk = [_fft.fftn(J[a]) for a in range(3)]
        CdotJ = Cx * Jk[0] + Cy * Jk[1] + Cz * Jk[2]
        drho = g_lat * _fft.ifftn(-1j * CdotJ).real
        rho = state["rho"] + drho
        rho_k = _fft.fftn(rho.astype(complex))
        EL_k = []
        for a, C in enumerate((Cx, Cy, Cz)):
            v = np.zeros_like(rho_k)
            # E_L = +iĈρ/|Ĉ|² ⇒ iĈ·E_L = −ρ, so ∂_tE_L = +g·J_L: the same
            # sign as the transverse +g·J_T kick (was −iĈρ/|Ĉ|², which gave
            # ∂_tE_L = −g·J_L — the two sectors disagreed; fixed 2026-09-29).
            v[nz] = 1j * C[nz] * rho_k[nz] / C2[nz]
            EL_k.append(v)
        E_L = np.array([_fft.ifftn(EL_k[a]).real for a in range(3)])

        A, _lon_frac = cc.solve_A_coulomb_3d(B)
        return {"E": E, "B": B, "A": A, "rho": rho, "E_L": E_L}

    def energy(self, state) -> float:
        return field_energy(state["E"], state["B"])

    def observables(self, state, lattice) -> dict:
        from casim.engine.gauge.em_photon_sourcing import iC_dot_B_norm
        return {"gauss_for_b_residual": iC_dot_B_norm(state["B"]),
                "field_energy": self.energy(state),
                "coulomb_field_norm": float(np.linalg.norm(
                    state.get("E_L", np.zeros_like(state["E"]))))}


@register
class FermionEmChannel(Channel):
    """Charged Weyl fermion advanced by F385's per-link U(1) covariant BCC
    step (fork a, the primary construction -- accept the norm drift, the
    roadmap's own declared choice for the gate-level coupling), with ``A``
    read from the partner ``EmPhotonChannel``'s F386 Coulomb-gauge solve.

    Register this AFTER the photon channel so it reads the ``A`` updated
    this tick (matching ``FermionDoubletChannel``'s own convention)."""
    type_name = "fermion_em"
    label = "Fermion EM"
    propagator = "per-link"        # F385 fork (a)
    topologies = ("bcc",)

    def init_state(self, lattice, rng):
        L = lattice.L
        width = float(self.config.get("width", 1.5))
        k0 = tuple(self.config.get("k0", (0.0, 0.0, 0.0)))
        center = tuple(self.config.get("center", (L // 2, L // 2, L // 2)))
        f = gaussian_packet(L, center, width, k0=k0)
        g = np.zeros_like(f)
        return {"f": f, "g": g}

    def step(self, state, lattice, context=None, rng=None):
        from casim.engine.gauge import minimal_coupling as mc

        partner = self.config.get("photon", "em_photon")
        q = float(self.config.get("q", 1.0))
        sign = self.config.get("sign", "+")
        A = context[partner]["A"]
        f, g = mc.u1_link_weyl_step_3d_bcc(state["f"], state["g"], A, q,
                                           sign=sign)
        return {"f": f, "g": g}

    def energy(self, state) -> float:
        return float(np.sum(np.abs(state["f"]) ** 2 + np.abs(state["g"]) ** 2))

    def density_field(self, state):
        d = np.abs(state["f"]) ** 2 + np.abs(state["g"]) ** 2
        return np.asarray(d.real if np.iscomplexobj(d) else d)


# ----------------------------------------------------------------------
# Gate entry — F387 (Stage 4 of the photon-fermion-coupling roadmap)
# ----------------------------------------------------------------------
def check_fermion_photon_backreaction(L=16, ticks=20, g_lat=0.5, q=1.0,
                                      width=1.5, k0=(0.5, 0.0, 0.0),
                                      photon_amp=0.15, seed=0,
                                      use_naive_sourcing=False):
    """F388 gate entry.  See ``findings/F388-fermion-photon-coupled-
    channels.md`` for the full account; this is the checklist its §2 table
    reports.

    Two declared controls:

    ``q=0``: zeroes the fermion's U(1) charge, which makes
    ``u1_link_weyl_step_3d_bcc`` reduce to the free step regardless of ``A``
    (F385's own ``A≡0``-equivalent reduction property) — this must, and
    measured does, turn exactly ``seeded_photon_gives_sustained_push`` red
    while leaving every other leg green.

    ``use_naive_sourcing=True``: reverts ``EmPhotonChannel`` to the
    roadmap's own literal, F386/F387-broken ``E += g·J`` sourcing recipe
    (no transverse/longitudinal split) — this must, and measured does, turn
    exactly ``no_monopole_fix_holds_with_dynamical_current`` red (this is
    the first place that leg is exercised under a genuinely dynamical
    current at all, so this control is also this leg's can-fail proof).
    """
    from casim.engine.core.simulation import Simulation, LatticeSpec
    from casim.engine.core.observers import Momentum
    from casim.engine.core import channels as core_channels
    from casim.engine.gauge.photon import build_pair_mode

    reg = registered_channels()
    channels_registered = ("em_photon" in reg) and ("fermion_em" in reg)

    # -- topology fix: the existing PhotonPairChannel now accepts "bcc" too,
    #    which is what let it be exiled to a companion scenario per the
    #    roadmap's own Sec.1.4 diagnosis -----------------------------------
    photon_pair_accepts_bcc = True
    try:
        LatticeSpec(L=L, topology="bcc").validate_channel(
            core_channels.PhotonPairChannel(name="photon_pair"))
    except Exception:
        photon_pair_accepts_bcc = False

    def _build(seed_photon: bool):
        lattice = LatticeSpec(L=L, dims=3, topology="bcc")
        em = EmPhotonChannel(name="em_photon", fermion="fermion_em",
                             g_lat=g_lat, q=q,
                             use_naive_sourcing=use_naive_sourcing)
        fm = FermionEmChannel(name="fermion_em", photon="em_photon", q=q,
                              width=width, k0=list(k0))
        sim = Simulation(lattice=lattice, channels=[em, fm], seed=seed)
        if seed_photon:
            # build_pair_mode polarizes transverse to the EUCLIDEAN k-hat,
            # not Ĉ(k) (the F386/F387-disclosed helper mismatch) -- project
            # onto the Ĉ(k)-transverse subspace before injecting, so the
            # seed is a genuinely divergence-free (i.C.B=0) photon and the
            # no-monopole leg below tests the SOURCING recipe, not this
            # test helper's own known imperfection.
            from casim.engine.gauge.em_photon_sourcing import (
                split_transverse_longitudinal)
            n = np.array([1.0, 1.0, 1.0]) / ROOT3
            Ep, Bp, _e1, _e2 = build_pair_mode(L, 2, n, (1.0, -1.0, 0.0))
            Ep_T, _Ep_L = split_transverse_longitudinal(Ep)
            Bp_T, _Bp_L = split_transverse_longitudinal(Bp)
            sim.states["em_photon"]["E"] = sim.states["em_photon"]["E"] \
                + photon_amp * Ep_T
            sim.states["em_photon"]["B"] = sim.states["em_photon"]["B"] \
                + photon_amp * Bp_T
        return sim

    # -- registration-order contract: em_photon (registered first) reads
    #    the fermion's PRE-tick state; fermion_em (registered second) reads
    #    the photon's POST-tick (this-tick) A ------------------------------
    #    Call each channel's own step() by hand, in the documented order, on
    #    plain copies of the PRE-tick states -- this stays correct under any
    #    future refactor of either step()'s internals (no hand-duplicated
    #    physics to drift out of sync), and directly tests the contract
    #    itself: em_photon's step must see fermion_em's pre-tick (f0,g0),
    #    and fermion_em's step must see the A em_photon JUST published. -----
    sim1 = _build(seed_photon=True)
    fermion_state0 = {k: v.copy() for k, v in sim1.states["fermion_em"].items()}
    photon_state0 = {k: v.copy() for k, v in sim1.states["em_photon"].items()}
    sim1.step(1)
    photon_state1_expected = sim1.channels["em_photon"].step(
        photon_state0, sim1.lattice, context={"fermion_em": fermion_state0})
    fermion_state1_expected = sim1.channels["fermion_em"].step(
        fermion_state0, sim1.lattice, context={"em_photon": photon_state1_expected})
    ordering_err = float(
        np.max(np.abs(sim1.states["fermion_em"]["f"]
                     - fermion_state1_expected["f"]))
        + np.max(np.abs(sim1.states["fermion_em"]["g"]
                       - fermion_state1_expected["g"]))
        + np.max(np.abs(sim1.states["em_photon"]["A"]
                       - photon_state1_expected["A"])))

    # -- self-sourced only (no seeded photon): P_field is IDENTICALLY zero
    #    by construction whenever the whole (E,B) content is confined to a
    #    single direction Ĉ(k) per mode (E_k x conj(B_k) of two parallel
    #    vectors vanishes) -- F384's current sources exactly along Ĉ(k),
    #    and the free rotation preserves that (F386 Sec.5) -- so this is
    #    an EXPECTED null, not a defect, the same class of "zero by
    #    construction" pitfall core.observers.Momentum's own docstring
    #    already documents for build_beam_packet ----------------------------
    sim2 = _build(seed_photon=False)
    mom = Momentum()
    mom.observe(sim2)
    sim2.step(ticks)
    mom.observe(sim2)
    pfield_final = np.array(mom.records[-1]["channels"]["em_photon"]["P_field"])
    pfield_norm = float(np.linalg.norm(pfield_final))

    # -- seeded genuine transverse photon: a real, sustained (non-oscillating,
    #    non-reverting) push -- NOT the F385-style unboundedly-growing secular
    #    push measured there against a STATIC test field: here the photon's
    #    own (E,B) evolves and the finite pulse's momentum content is what it
    #    is, so the physically sensible signature is a rise to, and hold at,
    #    a nonzero plateau (measured directly, F387 Sec.2) rather than
    #    unbounded growth -- checked as "end is not smaller than half of mid"
    #    (rules out decay/oscillation back toward zero, not literal secularity)
    # -----------------------------------------------------------------------
    sim3 = _build(seed_photon=True)
    mom3 = Momentum()
    mom3.observe(sim3)
    pm0 = np.array(mom3.records[-1]["channels"]["fermion_em"]["P_matter"])
    sim3.step(ticks // 2)
    mom3.observe(sim3)
    pm_mid = np.array(mom3.records[-1]["channels"]["fermion_em"]["P_matter"])
    sim3.step(ticks - ticks // 2)
    mom3.observe(sim3)
    pm_end = np.array(mom3.records[-1]["channels"]["fermion_em"]["P_matter"])
    d_mid = float(np.linalg.norm(pm_mid - pm0))
    d_end = float(np.linalg.norm(pm_end - pm0))

    # -- norm-drift stability check (a fresh, unstepped-observer run so the
    #    energy() calls above never perturb this measurement) --------------
    sim4 = _build(seed_photon=True)
    n0 = sim4.channels["fermion_em"].energy(sim4.states["fermion_em"])
    sim4.step(ticks)
    n1 = sim4.channels["fermion_em"].energy(sim4.states["fermion_em"])
    norm_drift = abs(n1 - n0) / n0

    # -- Gauss-for-B diagnostic: F387's split-sourcing fix, verified here
    #    for the first time under a genuinely DYNAMICAL (live, changing-
    #    every-tick) current -- F387's own harness only exercised it against
    #    a static current (its Sec.6 caveat says exactly this is unverified
    #    there).  Checked in both the self-sourced-only (sim2) and the
    #    seeded-photon (sim3, exercised over the full `ticks` run) cases. ---
    gauss_b_self_sourced = sim2.channels["em_photon"].observables(
        sim2.states["em_photon"], sim2.lattice)["gauss_for_b_residual"]
    gauss_b_seeded = sim3.channels["em_photon"].observables(
        sim3.states["em_photon"], sim3.lattice)["gauss_for_b_residual"]

    res = {
        "L": L, "ticks": ticks, "g_lat": g_lat, "q": q,
        "channels_registered": bool(channels_registered),
        "photon_pair_accepts_bcc": bool(photon_pair_accepts_bcc),
        "ordering_err": ordering_err,
        "pfield_norm_self_sourced": pfield_norm,
        "matter_push_mid": d_mid,
        "matter_push_end": d_end,
        "norm_drift": norm_drift,
        "gauss_for_b_residual_self_sourced": gauss_b_self_sourced,
        "gauss_for_b_residual_seeded": gauss_b_seeded,
    }
    res["checks"] = {
        "channels_registered": bool(channels_registered),
        "photon_pair_accepts_bcc": bool(photon_pair_accepts_bcc),
        "ordering_pretick_posttick_exact": bool(ordering_err < 1e-10),
        "self_sourced_field_momentum_trivially_zero": bool(pfield_norm < 1e-8),
        "seeded_photon_gives_sustained_push": bool(
            d_end > 1e-6 and d_end >= 0.5 * d_mid),
        "norm_drift_bounded": bool(norm_drift < 0.5),
        "no_monopole_fix_holds_with_dynamical_current": bool(
            gauss_b_self_sourced < 1e-8 and gauss_b_seeded < 1e-8),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


# ----------------------------------------------------------------------
# Gate entry — F389 (fixing F384's declared-open transverse gauge freedom)
# ----------------------------------------------------------------------
def _self_sourced_momentum_run(L, ticks, g_lat, q, width, k0,
                               use_radiative_current):
    """One self-sourced (no seeded photon) coupled run — the same scenario
    F388's own ``self_sourced_field_momentum_trivially_zero`` leg used, now
    exercised with F389's current option. Returns ``(dP_matter, dP_field,
    gauss_for_b_residual)``."""
    from casim.engine.core.simulation import Simulation, LatticeSpec
    from casim.engine.core.observers import Momentum

    lattice = LatticeSpec(L=L, dims=3, topology="bcc")
    em = EmPhotonChannel(name="em_photon", fermion="fermion_em", g_lat=g_lat,
                         q=q, use_radiative_current=use_radiative_current)
    fm = FermionEmChannel(name="fermion_em", photon="em_photon", q=q,
                          width=width, k0=list(k0))
    sim = Simulation(lattice=lattice, channels=[em, fm], seed=0)
    mom = Momentum()
    mom.observe(sim)
    pm0 = np.array(mom.records[-1]["channels"]["fermion_em"]["P_matter"])
    pf0 = np.array(mom.records[-1]["channels"]["em_photon"]["P_field"])
    sim.step(ticks)
    mom.observe(sim)
    pm1 = np.array(mom.records[-1]["channels"]["fermion_em"]["P_matter"])
    pf1 = np.array(mom.records[-1]["channels"]["em_photon"]["P_field"])
    gauss_b = sim.channels["em_photon"].observables(
        sim.states["em_photon"], sim.lattice)["gauss_for_b_residual"]
    return pm1 - pm0, pf1 - pf0, float(gauss_b)


def check_radiative_current_backreaction(L=16, ticks=20, g_lat=0.3, q=1.0,
                                         width=1.5, k0=(0.5, 0.0, 0.0),
                                         use_radiative_current=True):
    """F389 gate entry. See ``findings/F389-radiative-transverse-em-
    current.md`` for the derivation; this is the checklist its own results
    table reports.

    Exercises the *self-sourced-only* scenario F388's own
    ``self_sourced_field_momentum_trivially_zero`` leg used (no seeded
    photon — the genuine "does the fermion's own current excite the field"
    question), at ``g_lat`` and ``2·g_lat``, with F389's
    ``use_radiative_current`` option.

    ``field_momentum_genuinely_nonzero``
        ``‖ΔP_field‖ > 1e-8`` at ``g_lat`` — under F388's own current this
        was, and remains by default, machine zero (``self_sourced_field_
        momentum_trivially_zero``, unchanged); this leg is the direct
        demonstration that F389's current breaks that triviality.
    ``no_monopole_holds``
        F387's split-sourcing fix (``iĈ·B``) still holds at both ``g_lat``
        and ``2·g_lat`` — the transverse addition must not reopen F386/F387's
        no-magnetic-monopole defect.
    ``momentum_partially_but_not_exactly_conserved``
        ``0.01 < ‖ΔP_field‖/‖ΔP_matter‖ < 0.9`` — a genuine, bounded-away-
        from-both-ends fraction of the matter's momentum loss is recovered
        by the field, but *not* all of it. This is the honest, falsifiable
        form of the finding's own headline result: not "conserved" and not
        "still zero", a specific partial number (see the finding for why:
        the fermion's per-link recoil and this current's field-sourcing are
        independently-derived constructions, not order-matched in
        ``g_lat``).
    ``matter_push_scales_linearly_field_push_scales_quadratically``
        ``‖ΔP_matter(2g)‖/‖ΔP_matter(g)‖ ∈ (1.6, 2.4)`` (linear — a
        Lorentz-force-like leading-order response to the self-sourced ``A``)
        and ``‖ΔP_field(2g)‖/‖ΔP_field(g)‖ ∈ (3.0, 5.4)`` (quadratic — ``E×B``
        needs both factors sourced) — the measured, quantified form of the
        order-mismatch that keeps this loop from being exactly momentum-
        conserving at any coupling strength, not merely a qualitative
        impression from one run.

    ``use_radiative_current=False`` (the declared control) reverts to
    F388's own current (``conserved_current`` alone, always
    ``Ĉ(k)``-transverse-null) — measured to redden
    ``field_momentum_genuinely_nonzero``,
    ``momentum_partially_but_not_exactly_conserved`` (``ΔP_field``, and
    hence ``ΔP_matter`` too — §F388 §2's finding that ``A`` then never
    leaves zero, so the fermion's own per-link step reduces to the free
    step — both collapse to machine noise, so the recovered fraction is
    ill-defined/zero rather than in the declared band) and the scaling leg
    (both ratios become noise-dominated, no longer 2×/4×) — three of the
    four legs, leaving only ``no_monopole_holds`` green (F387's fix does not
    depend on which current sources it).
    """
    dPm, dPf, gauss_b = _self_sourced_momentum_run(
        L, ticks, g_lat, q, width, k0, use_radiative_current)
    dPm2, dPf2, gauss_b2 = _self_sourced_momentum_run(
        L, ticks, 2.0 * g_lat, q, width, k0, use_radiative_current)

    norm_dPm, norm_dPf = float(np.linalg.norm(dPm)), float(np.linalg.norm(dPf))
    norm_dPm2, norm_dPf2 = float(np.linalg.norm(dPm2)), float(np.linalg.norm(dPf2))
    recovered_frac = norm_dPf / norm_dPm if norm_dPm > 1e-12 else 0.0
    dPm_ratio = norm_dPm2 / norm_dPm if norm_dPm > 1e-12 else float("nan")
    dPf_ratio = norm_dPf2 / norm_dPf if norm_dPf > 1e-12 else float("nan")

    res = {
        "L": L, "ticks": ticks, "g_lat": g_lat, "q": q,
        "use_radiative_current": use_radiative_current,
        "dP_matter_norm": norm_dPm, "dP_field_norm": norm_dPf,
        "dP_matter_norm_2g": norm_dPm2, "dP_field_norm_2g": norm_dPf2,
        "recovered_fraction": recovered_frac,
        "dPm_doubling_ratio": dPm_ratio, "dPf_doubling_ratio": dPf_ratio,
        "gauss_for_b_residual": gauss_b, "gauss_for_b_residual_2g": gauss_b2,
    }
    res["checks"] = {
        "field_momentum_genuinely_nonzero": bool(norm_dPf > 1e-8),
        "no_monopole_holds": bool(gauss_b < 1e-8 and gauss_b2 < 1e-8),
        "momentum_partially_but_not_exactly_conserved": bool(
            0.01 < recovered_frac < 0.9),
        "matter_push_scales_linearly_field_push_scales_quadratically": bool(
            1.6 < dPm_ratio < 2.4 and 3.0 < dPf_ratio < 5.4),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res
