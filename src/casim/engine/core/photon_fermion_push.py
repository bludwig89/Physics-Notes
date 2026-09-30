"""casim.engine.core.photon_fermion_push — Stage 5 of
``docs/roadmaps/photon-fermion-coupling.md``: the scenario and the physics
claims.

Builds the roadmap's own scenario ("a beam packet plus a localized Weyl
packet at rest, one lattice, momentum observer on both") on top of Stage 4's
``EmPhotonChannel``/``FermionEmChannel`` (F388) with F389's radiative
current (``use_radiative_current=True``) so the loop can genuinely radiate,
and tests the roadmap's four claims, in the order it lists them, against
what the built engine actually does — not what a reader might hope it does.

**Read this module's docstrings alongside `findings/F390-photon-fermion-
push-scenario.md`** for the full derivation; this file's job is the
checklist that finding's tables report.

Summary of outcomes (full detail in the finding):

1. **Momentum conservation** — NOT achieved exactly at any coupling tested,
   confirming F389's own structural prediction extended to a genuinely
   dynamical, beam-driven scenario. But this stage finds something F389's
   self-sourced-only harness could not show: the field's momentum change and
   the matter's momentum change are **nearly exactly anti-parallel**
   (``cos≈-0.94`` to ``-0.999`` across every configuration swept), not just
   coincidentally similar in magnitude — a genuine, falsifiable, positive
   partial result, with the *magnitude* mismatch (not the *direction*) the
   only thing standing between this and exact conservation.
2. **Direction** — CONFIRMED. The fermion's momentum shift is strongly
   aligned with the beam's own wavevector (``cos≈0.97-0.999``), robust
   across every perturbation tested.
3. **Magnitude** (``Δp=ΔE/c``) — NOT achieved, and not merely by a small
   margin: the fermion's momentum gain is (to leading order) set by the
   *unconditional* field→fermion push (F385's per-link step, independent of
   the coupling constant that governs field sourcing), while the field's own
   energy loss is set entirely by the *separate*, coupling-dependent
   radiative-current mechanism (F389) — the two are not mediated by the same
   channel, so there is no reason for them to satisfy a shared ``E=pc``-type
   relation, and measured, they do not. Reported as a precisely
   characterized negative result, not forced to fit.
4. **Stretch — Thomson cross-section** — explicitly out of scope this
   session; see the finding's own §5 for why attempting it now would be
   premature given claim 1/3's structural gaps.
"""
from __future__ import annotations

from casim.numerics import xp as np
from casim.engine.core.coupled import EmPhotonChannel, FermionEmChannel
from casim.constants import c_lat

__all__ = ["build_push_run", "run_push_scenario", "check_photon_fermion_push"]


def build_push_run(L=16, g_lat=0.3, q=1.0, width=1.5, m_index=2, axis=0,
                   sigma=3.0, amp=0.15, use_radiative_current=True, seed=0,
                   beam_polarization="linear"):
    """Build the roadmap's Stage-5 scenario: a genuine, `Ĉ(k)`-transverse
    beam packet (``photon.build_beam_packet``, projected via
    ``em_photon_sourcing.split_transverse_longitudinal`` for the same reason
    F388/F389 project their own seeds — the helper polarizes transverse to
    the Euclidean `k̂`, not `Ĉ(k)`, F386 §6) seeded into ``em_photon``'s
    initial state, plus a localized Weyl packet **at rest** (``k0=(0,0,0)``,
    the roadmap's own "localized Weyl packet at rest") in ``fermion_em``.

    ``beam_polarization`` (default ``"linear"``, F392 backward-compat
    default): F390's original beam has ``E∥B`` pointwise and carries
    exactly zero field momentum (F392 §Part A) — ``"circular"`` is F392's
    null-Riemann–Silberstein fix, used by the Stage-5 re-run (F395).

    Returns a ready-to-step ``Simulation``.
    """
    from casim.engine.core.simulation import Simulation, LatticeSpec
    from casim.engine.gauge.photon import build_beam_packet
    from casim.engine.gauge.em_photon_sourcing import (
        split_transverse_longitudinal)

    lattice = LatticeSpec(L=L, dims=3, topology="bcc")
    em = EmPhotonChannel(name="em_photon", fermion="fermion_em", g_lat=g_lat,
                         q=q, use_radiative_current=use_radiative_current)
    fm = FermionEmChannel(name="fermion_em", photon="em_photon", q=q,
                          width=width, k0=[0.0, 0.0, 0.0])
    sim = Simulation(lattice=lattice, channels=[em, fm], seed=seed)

    E, B, k0vec = build_beam_packet(L, m_index=m_index, axis=axis, sigma=sigma,
                                    polarization=beam_polarization)
    E_T, _E_L = split_transverse_longitudinal(E)
    B_T, _B_L = split_transverse_longitudinal(B)
    sim.states["em_photon"]["E"] = sim.states["em_photon"]["E"] + amp * E_T
    sim.states["em_photon"]["B"] = sim.states["em_photon"]["B"] + amp * B_T
    sim._beam_k0vec = np.asarray(k0vec, dtype=float)   # stashed for the caller
    return sim


def run_push_scenario(L=16, ticks=20, g_lat=0.3, q=1.0, width=1.5,
                      m_index=2, axis=0, sigma=3.0, amp=0.15,
                      use_radiative_current=True, seed=0,
                      beam_polarization="linear"):
    """Run :func:`build_push_run` for ``ticks`` and return the measured
    quantities the four claims need: ``(dP_matter, dP_field, k0vec,
    dE_field)``, each a real vector/scalar over the whole run.
    """
    from casim.engine.core.observers import Momentum

    sim = build_push_run(L, g_lat, q, width, m_index, axis, sigma, amp,
                         use_radiative_current, seed,
                         beam_polarization=beam_polarization)
    mom = Momentum()
    mom.observe(sim)
    pm0 = np.array(mom.records[-1]["channels"]["fermion_em"]["P_matter"])
    pf0 = np.array(mom.records[-1]["channels"]["em_photon"]["P_field"])
    e0 = sim.channels["em_photon"].energy(sim.states["em_photon"])
    sim.step(ticks)
    mom.observe(sim)
    pm1 = np.array(mom.records[-1]["channels"]["fermion_em"]["P_matter"])
    pf1 = np.array(mom.records[-1]["channels"]["em_photon"]["P_field"])
    e1 = sim.channels["em_photon"].energy(sim.states["em_photon"])
    return pm1 - pm0, pf1 - pf0, sim._beam_k0vec, float(e1 - e0)


def _safe_cos(a, b):
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na < 1e-12 or nb < 1e-12:
        return float("nan")
    return float(np.dot(a, b) / (na * nb))


# ----------------------------------------------------------------------
# Gate entry — F390 (Stage 5 of the photon-fermion-coupling roadmap)
# ----------------------------------------------------------------------
def check_photon_fermion_push(L=16, ticks=20, g_lat=0.6, q=1.0, width=1.5,
                              m_index=2, sigma=3.0, amp=0.15,
                              use_radiative_current=True):
    """F390 gate entry.  See ``findings/F390-photon-fermion-push-
    scenario.md`` for the full derivation; this is the checklist its own
    result tables report.

    Two declared controls:

    ``use_radiative_current=False`` (surgical): reverts ``em_photon`` to
    F388's own current (``em_current.conserved_current`` alone, always
    ``Ĉ(k)``-transverse-null, F388 §2) — this must, and measured does, turn
    exactly ``field_gains_real_momentum_when_radiative_current_on``,
    ``field_and_matter_momentum_nearly_antiparallel``, ``closure_residual_
    has_interior_minimum``, and ``antiparallel_result_inverts_off_axis``
    red (``field_push_norm`` collapses to machine noise on- and off-axis
    alike, so there is nothing to be non-zero, anti-parallel, non-monotonic,
    or invertible), while ``push_direction_aligned_with_beam`` (the matter
    push is unconditional — F388 §2's own mechanism, it never depended on
    which current sources the field), ``field_momentum_zero_at_zero_
    coupling``, ``momentum_conservation_not_exact_at_default_coupling``
    (trivially still true — the residual becomes exactly `1.0`), and
    ``direction_correlation_breaks_down_off_axis`` (also unconditional,
    matter-push-only) all stay green.

    ``q=0`` (blunt): zeroes the fermion's U(1) charge entirely, which kills
    *all* momentum transfer in either direction (the per-link step reduces
    to the free step, F385's own ``A≡0``-equivalent reduction property, so
    even the ``g_lat=0`` baseline's matter push vanishes) — this must, and
    measured does, turn every single leg red or ill-defined, since nothing
    in this scenario has any physics left to measure without a charge.

    **The two axis-robustness legs (added in review, 2026-09-15) gate a
    genuine, previously-undisclosed failure mode rather than leave it
    invisible to the tier.** ``direction_correlation_breaks_down_off_axis``
    and ``antiparallel_result_inverts_off_axis`` assert — as an *expected*,
    disclosed limitation, not a bug — that an off-axis beam (``axis=1``,
    otherwise identical to the default) both loses the beam-direction
    correlation (``|cos_beam|<0.3``, measured `-0.0019`) and *inverts* the
    on-axis anti-parallel result into a near-exactly *parallel* one
    (``cos(ΔP_matter,ΔP_field)>0.5``, measured `+0.99995`). See
    `findings/F390-photon-fermion-push-scenario.md` §3 for the full account
    and the likely mechanism (F387's documented `Ĉ(k)` axis anisotropy).
    """
    # -- claims 1/2: default coupling run -----------------------------------
    dPm, dPf, k0vec, dE_field = run_push_scenario(
        L=L, ticks=ticks, g_lat=g_lat, q=q, width=width, m_index=m_index,
        sigma=sigma, amp=amp, use_radiative_current=use_radiative_current)
    npm, npf = float(np.linalg.norm(dPm)), float(np.linalg.norm(dPf))
    khat = k0vec / np.linalg.norm(k0vec)
    cos_beam = _safe_cos(dPm, khat)
    cos_mf = _safe_cos(dPm, dPf)
    residual = float(np.linalg.norm(dPm + dPf)) / npm if npm > 1e-12 else float("nan")

    # -- claim 1's zero-coupling baseline: the field cannot lose momentum
    #    at all through the per-link push alone (F388 Sec.2's own mechanism,
    #    now shown for a genuine external beam, not just a self-sourced
    #    current) -- deliberately NOT parameterized by `use_radiative_current`:
    #    at g_lat=0 no current-sourcing happens regardless of which current
    #    WOULD have been used, so this baseline is unaffected by that flag by
    #    construction, and the `use_radiative_current=False` control above
    #    correctly leaves this leg green. -----------------------------------
    dPm0, dPf0, _k0, _dE0 = run_push_scenario(
        L=L, ticks=ticks, g_lat=0.0, q=q, width=width, m_index=m_index,
        sigma=sigma, amp=amp, use_radiative_current=True)
    npm0, npf0 = float(np.linalg.norm(dPm0)), float(np.linalg.norm(dPf0))

    # -- the "sweet spot": a genuine, reproducible local minimum in the
    #    closure residual away from both ends of a coupling-strength sweep --
    dPm_hi, dPf_hi, _k, _e = run_push_scenario(
        L=L, ticks=ticks, g_lat=2.0 * g_lat, q=q, width=width,
        m_index=m_index, sigma=sigma, amp=amp,
        use_radiative_current=use_radiative_current)
    dPm_lo, dPf_lo, _k, _e = run_push_scenario(
        L=L, ticks=ticks, g_lat=0.5 * g_lat, q=q, width=width,
        m_index=m_index, sigma=sigma, amp=amp,
        use_radiative_current=use_radiative_current)
    res_mid = residual
    res_hi = float(np.linalg.norm(dPm_hi + dPf_hi)) / float(np.linalg.norm(dPm_hi))
    res_lo = float(np.linalg.norm(dPm_lo + dPf_lo)) / float(np.linalg.norm(dPm_lo))

    # -- axis robustness (found in review, F390-review-2026-09-15): the
    #    direction/anti-alignment claims above are measured ONLY for an
    #    on-axis beam (axis=0, this leg's own default). An off-axis beam
    #    (axis=1, same m_index) is used here to GATE the known breakdown as
    #    a disclosed, monitored fact, not leave it invisible to the tier --
    #    plausibly traced to F387's documented Ĉ(k)=(k_x,-k_y,k_z)/|k| axis
    #    anisotropy interacting with build_beam_packet's Euclidean-k-hat
    #    (not Ĉ(k)) polarization convention (F386 §6). -----------------------
    dPm_off, dPf_off, k0vec_off, _e_off = run_push_scenario(
        L=L, ticks=ticks, g_lat=g_lat, q=q, width=width, m_index=m_index,
        axis=1, sigma=sigma, amp=amp,
        use_radiative_current=use_radiative_current)
    khat_off = k0vec_off / np.linalg.norm(k0vec_off)
    cos_beam_off = _safe_cos(dPm_off, khat_off)
    cos_mf_off = _safe_cos(dPm_off, dPf_off)

    res = {
        "L": L, "ticks": ticks, "g_lat": g_lat, "q": q,
        "matter_push_norm": npm, "field_push_norm": npf,
        "cos_beam_direction": cos_beam, "cos_matter_field": cos_mf,
        "conservation_residual": residual,
        "matter_push_norm_zero_coupling": npm0,
        "field_push_norm_zero_coupling": npf0,
        "residual_at_half_g": res_lo, "residual_at_g": res_mid,
        "residual_at_2g": res_hi,
        "dE_field": dE_field,
        "cos_beam_direction_off_axis": cos_beam_off,
        "cos_matter_field_off_axis": cos_mf_off,
    }
    res["checks"] = {
        "push_direction_aligned_with_beam": bool(
            not np.isnan(cos_beam) and cos_beam > 0.9),
        "field_momentum_zero_at_zero_coupling": bool(
            npf0 < 1e-10 and npm0 > 1e-3),
        "field_gains_real_momentum_when_radiative_current_on": bool(
            npf > 1e-4),
        "field_and_matter_momentum_nearly_antiparallel": bool(
            not np.isnan(cos_mf) and cos_mf < -0.85),
        "momentum_conservation_not_exact_at_default_coupling": bool(
            not np.isnan(residual) and residual > 0.05),
        "closure_residual_has_interior_minimum": bool(
            res_mid < res_lo and res_mid < res_hi),
        "direction_correlation_breaks_down_off_axis": bool(
            not np.isnan(cos_beam_off) and abs(cos_beam_off) < 0.3),
        "antiparallel_result_inverts_off_axis": bool(
            not np.isnan(cos_mf_off) and cos_mf_off > 0.5),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


def _roll_state_dict(state, shift):
    """Translate every spatial field in a channel's ``state`` dict by
    ``shift=(sx,sy,sz)`` lattice sites (periodic).  Any array with 3 or more
    dimensions is assumed to carry its spatial axes last (``(...,L,L,L)`` —
    a bare scalar field, or a leading polarisation/spinor-component axis);
    a scalar or 0-d entry is passed through unchanged."""
    out = {}
    for key, val in state.items():
        arr = np.asarray(val)
        if arr.ndim >= 3:
            spatial_axes = tuple(range(arr.ndim - 3, arr.ndim))
            rolled = arr
            for ax, s in zip(spatial_axes, shift):
                if s:
                    rolled = np.roll(rolled, s, axis=ax)
            out[key] = rolled
        else:
            out[key] = arr
    return out


def check_stage5_circular_beam_rerun(L=16, ticks=20, g_lat=0.6, q=1.0,
                                     width=1.5, sigma=3.0, amp=0.15,
                                     use_radiative_current=True,
                                     beam_polarization="circular"):
    """F395 gate entry — Part D of `docs/roadmaps/photon-fermion-coupling-
    rerun-prompt.md`: re-run Stage 5 against F392's fixed beam and restate
    the roadmap's claim 1 per the audit's §6.2 crystal-momentum argument.
    See `findings/F395-stage5-circular-beam-rerun.md` for the full account.

    **Two re-measurements, done before any theorising** (per the rerun
    prompt's own instruction):

    - the `m_index=4` sign-flip anomaly F390 §3 found unexplained;
    - the off-axis (`axis=1`) decorrelation F390 §3 also found.

    Both are re-measured here with the genuinely null (`polarization=
    "circular"`) beam. Both persist essentially unchanged from F390's own
    (defective-beam) numbers, and from F391's own (Ĉ(k)-transverse-beam)
    numbers — a third, independent beam-construction fix that also changes
    nothing, converging on F391 §3's own conclusion: the mechanism lives in
    the matter-side coupling (the fermion's fixed internal spin state), not
    in the photon sector, and no beam-construction fix can touch it.

    **Claim 1, restated per the audit's §6.2** (a lattice has only discrete
    translation symmetry, so `ΔP_matter+ΔP_field≈0` for a continuum-style
    `P` is not achievable by any scheme — this is not a defect, it is what a
    lattice is):

    - **(A) exact charge conservation.** Measured via the fermion's own
      norm drift under the *actual* per-link covariant step (F385 fork a,
      the gate-level choice) in this live, beam-driven scenario. **Not
      delivered exactly by the existing bridged architecture** — F385
      already established `O(|qA|·a)` norm drift for this step in
      isolation; this leg confirms it is still nonzero (bounded, not zero)
      in the full Stage-5 loop. The audit's target (A) is a property of the
      *single-action* route (§6.1), which casim's actual bridged
      construction does not implement — disclosed here, not achieved.
    - **(B) exact crystal-momentum conservation**, checked directly as
      `Φ∘T=T∘Φ` to machine precision: translating the *entire* initial
      state (fields and fermion together) by one lattice site and then
      running the simulation must give the same result as running the
      simulation first and translating the result — because none of the
      per-tick update rules (the FFT-spectral photon rotation, the
      per-link covariant step's *shift-based* hop, the algebraic Gauss
      solve) reference an absolute lattice coordinate.
    - **(C) matched-order approach to the continuum.** Re-measures F389
      §4's `O(g_lat)`-vs-`O(g_lat²)` order mismatch (matter push linear,
      field push quadratic in the coupling) for the genuinely beam-driven
      (not self-sourced-only) case with the fixed beam. **Still mismatched**
      — the fix does not, and was never expected to, resolve a mismatch
      whose root cause (F389 §4) is that the two channels are independently
      derived, not two variations of one action.

    No declared control on the (A)/(B)/(C) legs — they are new measurements
    of the model's own dynamics, not a defect this finding introduces or
    could accidentally paper over; the `m4_anomaly_persists` and
    `offaxis_breakdown_persists` legs are controlled implicitly by their own
    comparison against F390/F391's independently-measured numbers.
    """
    # -- re-measure F390's own default/off-axis/m4 configs, circular beam --
    dPm, dPf, k0vec, _e = run_push_scenario(
        L=L, ticks=ticks, g_lat=g_lat, q=q, width=width, m_index=2, axis=0,
        sigma=sigma, amp=amp, use_radiative_current=use_radiative_current,
        beam_polarization=beam_polarization)
    khat = k0vec / np.linalg.norm(k0vec)
    cos_beam = _safe_cos(dPm, khat)
    cos_mf = _safe_cos(dPm, dPf)

    dPm4, dPf4, k0vec4, _e4 = run_push_scenario(
        L=L, ticks=ticks, g_lat=g_lat, q=q, width=width, m_index=4, axis=0,
        sigma=sigma, amp=amp, use_radiative_current=use_radiative_current,
        beam_polarization=beam_polarization)
    khat4 = k0vec4 / np.linalg.norm(k0vec4)
    cos_beam_m4 = _safe_cos(dPm4, khat4)

    dPm_off, dPf_off, k0vec_off, _eo = run_push_scenario(
        L=L, ticks=ticks, g_lat=g_lat, q=q, width=width, m_index=2, axis=1,
        sigma=sigma, amp=amp, use_radiative_current=use_radiative_current,
        beam_polarization=beam_polarization)
    khat_off = k0vec_off / np.linalg.norm(k0vec_off)
    cos_beam_off = _safe_cos(dPm_off, khat_off)
    cos_mf_off = _safe_cos(dPm_off, dPf_off)

    # -- disclosure only, not gated: the z-axis off-axis config F390/F391
    #    also measured (not the axis=1 default this finding's own legs use)
    dPm_off2, dPf_off2, k0vec_off2, _eo2 = run_push_scenario(
        L=L, ticks=ticks, g_lat=g_lat, q=q, width=width, m_index=2, axis=2,
        sigma=sigma, amp=amp, use_radiative_current=use_radiative_current,
        beam_polarization=beam_polarization)
    khat_off2 = k0vec_off2 / np.linalg.norm(k0vec_off2)
    cos_beam_off_z = _safe_cos(dPm_off2, khat_off2)
    cos_mf_off_z = _safe_cos(dPm_off2, dPf_off2)

    # -- target (A): is charge exactly conserved by the ACTUAL architecture? --
    sim_a = build_push_run(L=L, g_lat=g_lat, q=q, width=width, m_index=2,
                           axis=0, sigma=sigma, amp=amp,
                           use_radiative_current=use_radiative_current,
                           beam_polarization=beam_polarization)
    fs0 = sim_a.states["fermion_em"]
    n0 = float(np.sum(np.abs(fs0["f"]) ** 2 + np.abs(fs0["g"]) ** 2))
    sim_a.step(ticks)
    fs1 = sim_a.states["fermion_em"]
    n1 = float(np.sum(np.abs(fs1["f"]) ** 2 + np.abs(fs1["g"]) ** 2))
    charge_drift = abs(n1 - n0) / n0

    # -- target (B): Phi.T == T.Phi to machine precision -----------------
    sim_b1 = build_push_run(L=L, g_lat=g_lat, q=q, width=width, m_index=2,
                            axis=0, sigma=sigma, amp=amp,
                            use_radiative_current=use_radiative_current,
                            beam_polarization=beam_polarization, seed=0)
    sim_b2 = build_push_run(L=L, g_lat=g_lat, q=q, width=width, m_index=2,
                            axis=0, sigma=sigma, amp=amp,
                            use_radiative_current=use_radiative_current,
                            beam_polarization=beam_polarization, seed=0)
    shift = (1, 0, 0)
    for cname in ("em_photon", "fermion_em"):
        sim_b2.states[cname] = _roll_state_dict(sim_b2.states[cname], shift)
    sim_b1.step(ticks)
    sim_b2.step(ticks)
    residual_b = 0.0
    norm_b = 0.0
    for cname in ("em_photon", "fermion_em"):
        translated_1 = _roll_state_dict(sim_b1.states[cname], shift)
        for key, v2 in sim_b2.states[cname].items():
            v1t = np.asarray(translated_1[key])
            v2 = np.asarray(v2)
            residual_b += float(np.linalg.norm(v1t - v2) ** 2)
            norm_b += float(np.linalg.norm(v2) ** 2)
    translation_covariance_residual = (
        (residual_b ** 0.5) / (norm_b ** 0.5) if norm_b > 0 else float("nan"))

    # -- target (C): is the coupling order still mismatched, beam-driven? --
    dPm_g, dPf_g, _k, _e = run_push_scenario(
        L=L, ticks=ticks, g_lat=g_lat, q=q, width=width, m_index=2, axis=0,
        sigma=sigma, amp=amp, use_radiative_current=use_radiative_current,
        beam_polarization=beam_polarization)
    dPm_2g, dPf_2g, _k, _e = run_push_scenario(
        L=L, ticks=ticks, g_lat=2.0 * g_lat, q=q, width=width, m_index=2,
        axis=0, sigma=sigma, amp=amp,
        use_radiative_current=use_radiative_current,
        beam_polarization=beam_polarization)
    ratio_matter = (float(np.linalg.norm(dPm_2g)) /
                    float(np.linalg.norm(dPm_g)))
    ratio_field = (float(np.linalg.norm(dPf_2g)) /
                   float(np.linalg.norm(dPf_g)))

    res = {
        "cos_beam_direction_default": cos_beam,
        "cos_matter_field_default": cos_mf,
        "cos_beam_direction_m4": cos_beam_m4,
        "cos_beam_direction_offaxis": cos_beam_off,
        "cos_matter_field_offaxis": cos_mf_off,
        "cos_beam_direction_offaxis_z": cos_beam_off_z,
        "cos_matter_field_offaxis_z": cos_mf_off_z,
        "charge_drift_relative": charge_drift,
        "translation_covariance_residual": translation_covariance_residual,
        "doubling_ratio_matter": ratio_matter,
        "doubling_ratio_field": ratio_field,
    }
    res["checks"] = {
        "default_direction_still_confirmed": bool(
            not np.isnan(cos_beam) and cos_beam > 0.9),
        "m4_anomaly_persists": bool(
            not np.isnan(cos_beam_m4) and cos_beam_m4 < -0.5),
        # F390/F391 (both LINEAR-type polarization, differing only in
        # Ĉ(k)-vs-k̂ transversality convention) measured near-total
        # decorrelation here (cos~-0.002/-0.0019). The genuinely circular
        # beam does NOT reproduce that -- a real, new result, not a
        # threshold artifact (checked at axis=1 and axis=2, both nonzero
        # and axis-dependent; see the finding for the measured table).
        # This is disclosed as a MEASURED FACT, not a predicted one.
        "offaxis_correlation_changes_with_circular_beam": bool(
            not np.isnan(cos_beam_off) and abs(cos_beam_off) > 0.2),
        "target_A_charge_not_exact_but_bounded": bool(
            0.0 < charge_drift < 0.5),
        "target_B_translation_covariance_exact": bool(
            translation_covariance_residual < 1e-9),
        "target_C_order_still_mismatched": bool(
            abs(ratio_matter - ratio_field) > 0.3),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


if __name__ == "__main__":
    import json
    r = check_photon_fermion_push()
    print(json.dumps({k: v for k, v in r.items() if k != "checks"}, indent=2))
    print(json.dumps(r["checks"], indent=2))
