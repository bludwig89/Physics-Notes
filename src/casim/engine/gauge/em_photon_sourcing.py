"""casim.engine.gauge.em_photon_sourcing — the Ĉ(k) direction anisotropy and
the Ω_pair(k)/|C_odd(k)| sourcing mismatch (F387), and the Stage-4
``em_photon`` design fix.

The F386 review (``docs/reviews/F386-review-2026-09-14.md``) found two
previously-undisclosed structural facts about ``charge_coupling.bcc_curl_symbol``
and ``photon.pair_dispersion``, flagged as open items for whichever session
builds Stage 4 of ``docs/roadmaps/photon-fermion-coupling.md``.  This module
resolves the second one with a concrete design and demonstrates the fix to
machine precision; see ``findings/F387-curl-anisotropy-omega-pair-mismatch.md``
for the full derivation.

**Fact 1 — direction anisotropy (§1 below, no code fix needed).**
``bcc_curl_symbol``'s direction ``Ĉ(k)`` does not converge to ``k̂`` as
``k→0`` off the cubic axes: exactly ``Ĉ(k) → (k_x,−k_y,k_z)/|k|``.  This is
not a bug — it is the same sign correction ``lattice.bcc._bcc_uvec`` carries
for the Weyl walk's own spin–momentum locking (``bcc_spin_axis``'s docstring
already documents it *there*), inherited unchanged when the curl symbol reuses
that same ``n^+(k/2)`` vector as a Maxwell curl generator.  Nothing in this
module changes that: the anisotropy is a structural fact about ``Ĉ(k)``, not
a defect to be projected away — every function below (and every existing
consumer: ``solve_A_coulomb_3d``, ``magnetostatic_B``, ``maxwell_curl_step``)
already measures transversality against ``Ĉ(k)``, not the naive Euclidean
``k̂``, so it is unaffected by the anisotropy's existence.  What *was* missing
is the explicit statement, for the *photon/charge-coupling* context, that this
is happening — F87 only ever checked ``|C|/|k|`` (isotropic, MX1), never the
*direction*.

**Fact 2 — the Ω_pair(k)/|C_odd(k)| mismatch, and the actual (structural, not
value-driven) mechanism of the sourcing defect (§2, the code fix).**
``photon.photon_step_spectral`` rotates ``(E,B)`` by the *scalar* angle
``Ω_pair(k)`` identically across all three Cartesian components; it performs
no ``Ĉ(k)``-based projection at all.  ``maxwell_curl_step`` (and everything
that derives from ``bcc_curl_symbol``: F384's current, F386's ``solve``) is
built on the *vector* ``C_odd(k)``.  The two agree only as ``k→0``.  **This
value-mismatch is real but is not what breaks the no-monopole invariant** —
verified by elimination: substituting ``|C_odd(k)|`` itself for ``Ω_pair(k)``
in an otherwise-identical scalar rotation still produces the defect below, at
essentially the same size.  The actual mechanism is structural and
value-independent: a tick of *any* scalar per-mode rotation law (not just
``photon_step_spectral``'s ``Ω_pair``) sourced by ``E += g·J`` with a
``Ĉ(k)``-purely-longitudinal ``J`` (F384's own conserved current, always
purely longitudinal by construction) rotates that longitudinal ``E`` into an
equally longitudinal, *nonzero* ``B`` — ``i Ĉ·B ≠ 0``, a genuine violation of
this model's own no-monopole invariant, growing every tick (F386 §5, §6) —
because no scalar rotation, whatever angle it uses, has any ``Ĉ(k)``-aware
projection built in.

**The fix — a sector split, not a wholesale propagator swap.**  §3's key fact
makes this exact rather than heuristic: because ``photon_step_spectral``
applies the *same* 2×2 rotation independently to each Cartesian component, it
commutes exactly with the ``Ĉ(k)``-transverse/longitudinal projection
(:func:`split_transverse_longitudinal`) — verified to ``~3e-14`` on fields of
norm ``~70`` below (§3's control leg).  A purely-transverse sector therefore
stays purely transverse under the rotation forever, and a purely-longitudinal
sector stays purely longitudinal forever: the two sectors never mix under the
*free* propagator.  All the mixing in F386's broken scenario came from
sourcing, not from the rotation.  So: run ``Ω_pair`` rotation (decision 5's
canonical, non-birefringent photon law — unchanged) on the transverse sector
only, sourced by ``J``'s own transverse part; solve the longitudinal sector
algebraically from the accumulated charge density via the model's own Gauss
law ``iĈ·E_L=−ρ`` (engine sign, ∂_tE=…+gJ; the *same* ``Ĉ(k)`` machinery ``solve_A_coulomb_3d`` and
``em_current`` already use) — the lattice analogue of the continuum split
between a radiative transverse field (obeys the wave/rotation law) and a
non-propagating, instantaneous Coulomb field (obeys Gauss's law and never
touches ``B``).  ``B_L`` is then never populated at all, so ``iĈ·B=0`` holds
by construction, not by cancellation.
"""
from __future__ import annotations

from casim.numerics import xp as np
from casim.numerics import fft as _fft
from casim.engine.lattice.geometry import make_kgrid_3d
from casim.engine.gauge.charge_coupling import bcc_curl_symbol
from casim.engine.gauge.photon import photon_step_spectral

__all__ = [
    "curl_direction_angle", "split_transverse_longitudinal", "iC_dot_B_norm",
    "naive_sourced_scenario", "split_sourced_scenario",
    "check_em_photon_sourcing",
    "build_ck_transverse_beam_packet", "check_ck_transverse_beam_mechanism",
]


# ======================================================================
# §1 — Ĉ(k) direction anisotropy (measurement only; nothing to fix)
# ======================================================================

def curl_direction_angle(khat, L=64):
    """Angle (degrees) between ``Ĉ(k)`` and ``k̂`` for ``k`` along direction
    ``khat`` (a 3-tuple, need not be normalised), evaluated on an ``L``-grid
    at its smallest nonzero mode along that direction.  Exact and, per F387,
    independent of ``L`` (a continuum-limit property, not a finite-lattice
    artifact) — see :func:`check_em_photon_sourcing`'s stability leg.

    ``khat`` must be an integer triple (a valid BCC/FFT grid mode index) so
    the smallest nonzero mode along it lands exactly on a grid point.
    """
    khat = np.asarray(khat, dtype=int)
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    ix, iy, iz = khat[0] % L, khat[1] % L, khat[2] % L
    C = np.array([Cx[ix, iy, iz], Cy[ix, iy, iz], Cz[ix, iy, iz]])
    k = np.array([KX[ix, iy, iz], KY[ix, iy, iz], KZ[ix, iy, iz]])
    cosang = float(np.dot(C, k) / (np.linalg.norm(C) * np.linalg.norm(k)))
    return float(np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0))))


# ======================================================================
# §2 — the Ĉ(k)-transverse/longitudinal split (the reusable primitive)
# ======================================================================

def split_transverse_longitudinal(V):
    """Split a real ``(3,Lx,Ly,Lz)`` field into its ``Ĉ(k)``-transverse and
    ``Ĉ(k)``-longitudinal parts.  Same projector ``solve_A_coulomb_3d`` and
    ``magnetostatic_B`` already build inline; named here as a reusable
    primitive because Stage 4's sourcing recipe needs it applied to ``J``
    (this module) as well as to ``B`` (already in ``charge_coupling``).

    Returns ``(V_T, V_L)``, both real ``(3,Lx,Ly,Lz)``, ``V_T + V_L == V``
    to FFT round-off.  Zero on the disclosed Nyquist-corner modes where
    ``C(k)≡0`` exactly (F384 §3) — ``V`` is returned as-is (undecomposable)
    there and its whole content lands in ``V_T`` by convention (no
    longitudinal projector exists there to remove).
    """
    shape = V.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    C2 = Cx ** 2 + Cy ** 2 + Cz ** 2
    nz = C2 > 1e-14
    Vk = [_fft.fftn(V[a]) for a in range(3)]
    CdotV = Cx * Vk[0] + Cy * Vk[1] + Cz * Vk[2]
    VLk, VTk = [], []
    for a, C in enumerate((Cx, Cy, Cz)):
        proj = np.zeros_like(Vk[a])
        proj[nz] = C[nz] * CdotV[nz] / C2[nz]
        VLk.append(proj)
        VTk.append(Vk[a] - proj)
    VL = np.array([_fft.ifftn(VLk[a]).real for a in range(3)])
    VT = np.array([_fft.ifftn(VTk[a]).real for a in range(3)])
    return VT, VL


def iC_dot_B_norm(B):
    """``‖ i Ĉ·B ‖`` (Fourier ℓ² norm) — the no-monopole residual.  Zero to
    machine precision for any physically-consistent ``B``; F386 §5 measured
    ``0.399`` for the broken recipe's ``B`` at one snapshot."""
    shape = B.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    Bk = [_fft.fftn(B[a]) for a in range(3)]
    div = 1j * (Cx * Bk[0] + Cy * Bk[1] + Cz * Bk[2])
    return float(np.sqrt(np.sum(np.abs(div) ** 2)))


# ======================================================================
# §3 — the two sourcing recipes
# ======================================================================

def naive_sourced_scenario(L, n_ticks, J, g=1.0):
    """The roadmap's own Stage-4 sketch, literally (docs/roadmaps/
    photon-fermion-coupling.md §"Stage 4": ``E += g·J`` from the partner's
    Stage-1 current, applied to the *whole* Ω_pair-rotated field with no
    projection.  Demonstrates the defect (F386 §5): a purely-``Ĉ(k)``-
    longitudinal ``J`` rotates into a growing, nonzero, purely-longitudinal
    ``B`` with ``iĈ·B≠0``.  Kept as the control path, not deleted once the
    fix lands, so the no-monopole leg stays provably able to fail.

    ``J`` is a static ``(3,L,L,L)`` current (matches F386's own harness — a
    full coupled channel with a dynamical current is Stage 4's job).
    Returns the list of ``(B, iC_dot_B_norm)`` per tick.
    """
    E = np.zeros((3, L, L, L))
    B = np.zeros((3, L, L, L))
    history = []
    for _ in range(n_ticks):
        E, B = photon_step_spectral(E, B)
        E = E + g * J
        history.append((B, iC_dot_B_norm(B)))
    return history


def split_sourced_scenario(L, n_ticks, J, g=1.0):
    """The fix: split ``J`` into its ``Ĉ(k)``-transverse/longitudinal parts
    once (``J`` is static here); rotate only the transverse sector
    ``(E_T,B_T)`` by ``Ω_pair`` (``photon_step_spectral``, decision 5's
    canonical photon law, unchanged) and source it with ``J_T`` only; carry
    the longitudinal charge density ``ρ`` forward by the model's own
    continuity law ``∂_tρ = −iĈ·J`` (F384) and solve ``E_L`` *algebraically*
    each tick from the instantaneous Gauss law ``iĈ·E_L=−ρ`` (engine sign) — the lattice
    analogue of the continuum Coulomb field, which does not propagate and
    never touches ``B``.  ``B_L`` is therefore never populated: ``iĈ·B=0``
    holds by construction on every tick, not by cancellation.

    Returns the list of ``(B, iC_dot_B_norm, E_L_norm)`` per tick, mirroring
    :func:`naive_sourced_scenario`'s history shape (plus the Coulomb-field
    norm, so a caller can see it is doing real work, not silently discarding
    the charge's field).
    """
    shape = (L, L, L)
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    C2 = Cx ** 2 + Cy ** 2 + Cz ** 2
    nz = C2 > 1e-14

    JT, _JL = split_transverse_longitudinal(J)
    Jk = [_fft.fftn(J[a]) for a in range(3)]
    CdotJ = Cx * Jk[0] + Cy * Jk[1] + Cz * Jk[2]
    # ∂_tρ = −iĈ·(gJ) (F384), static J.  g now scales both sectors (was
    # missing here, which sourced the Coulomb sector at full strength while
    # the radiative sector got g — the inconsistency coupled.py already fixed).
    drho = g * _fft.ifftn(-1j * CdotJ).real

    E_T = np.zeros((3, L, L, L))
    B_T = np.zeros((3, L, L, L))
    rho = np.zeros((L, L, L))
    history = []
    for _ in range(n_ticks):
        E_T, B_T = photon_step_spectral(E_T, B_T)
        E_T = E_T + g * JT
        rho = rho + drho
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
        B = B_T                                  # B_L never populated
        history.append((B, iC_dot_B_norm(B), float(np.linalg.norm(E_L))))
    return history


# ======================================================================
# Gate entry — F387
# ======================================================================

def check_em_photon_sourcing(L=16, L_stability=64, n_ticks=6, g_lat=0.5,
                             use_split_for_no_monopole_check=True):
    """F387 gate entry.  See ``findings/F387-curl-anisotropy-omega-pair-
    mismatch.md`` for the full derivation of each leg.

    ``use_split_for_no_monopole_check`` (the declared control): swaps the
    naive (unprojected) sourcing recipe in for the leg that otherwise uses
    the fix, which — measured, not assumed — must turn exactly that leg red.
    """
    from casim.engine.gauge import em_current
    from casim.engine.core.coupled import gaussian_packet

    # -- §1: direction anisotropy -------------------------------------
    ang_axis = curl_direction_angle((1, 0, 0), L=L)
    ang_face = curl_direction_angle((1, 1, 0), L=L)
    ang_body = curl_direction_angle((1, 1, 1), L=L)
    ang_body_hiL = curl_direction_angle((1, 1, 1), L=L_stability)
    target_body = float(np.degrees(np.arccos(1.0 / 3.0)))

    # magnitude isotropy contrast (unaffected by the direction anisotropy).
    # This is a leading-order (k->0) statement -- the mismatch between axis
    # and body-diagonal |C|/|k| is O(k^2) and shrinks by 4x each time L
    # doubles (measured: 7.4e-3 at L=16 -> 4.6e-4 at L=64 -> 1.2e-4 at
    # L=128), so it is checked on the finer `L_stability` grid, not `L`.
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    Cmag = np.sqrt(Cx ** 2 + Cy ** 2 + Cz ** 2)
    KXh, KYh, KZh = make_kgrid_3d(L_stability, L_stability, L_stability)
    Cxh, Cyh, Czh = bcc_curl_symbol(KXh, KYh, KZh)
    Cmagh = np.sqrt(Cxh ** 2 + Cyh ** 2 + Czh ** 2)
    mag_axis = float(Cmagh[1, 0, 0] / abs(KXh[1, 0, 0]))
    mag_body = float(Cmagh[1, 1, 1] / np.sqrt(KXh[1, 1, 1] ** 2 + KYh[1, 1, 1] ** 2 + KZh[1, 1, 1] ** 2))

    # -- §2: Ω_pair(k) vs |C_odd(k)| mismatch ---------------------------
    from casim.engine.gauge.photon import pair_dispersion
    Om = pair_dispersion(KX, KY, KZ)
    Omh = pair_dispersion(KXh, KYh, KZh)
    ratio_small_k = float(Omh[1, 0, 0] / Cmagh[1, 0, 0])   # small-k: finer grid
    m_edge = L // 2 - 1
    ratio_edge_k = float(Om[m_edge, m_edge, m_edge] / Cmag[m_edge, m_edge, m_edge])

    # -- §3: rotation commutes with the Ĉ(k) T/L projection -------------
    rng = np.random.default_rng(0)
    E = rng.standard_normal((3, L, L, L))
    B = rng.standard_normal((3, L, L, L))
    E1, B1 = photon_step_spectral(E, B)
    E1T, E1L = split_transverse_longitudinal(E1)
    B1T, B1L = split_transverse_longitudinal(B1)
    ET, EL = split_transverse_longitudinal(E)
    BT, BL = split_transverse_longitudinal(B)
    E2T, B2T = photon_step_spectral(ET, BT)
    E2L, B2L = photon_step_spectral(EL, BL)
    commute_residual = float(max(
        np.linalg.norm(E1T - E2T), np.linalg.norm(B1T - B2T),
        np.linalg.norm(E1L - E2L), np.linalg.norm(B1L - B2L),
    )) / (np.linalg.norm(E) + np.linalg.norm(B))

    # -- §4: the fix, measured against the broken recipe -----------------
    c = L // 2
    f = gaussian_packet(L, (c, c, c), 2.0, k0=(0.4, 0, 0))
    zero = np.zeros_like(f)
    J, _res, _gap = em_current.conserved_current(f, zero, sign='+', q=1.0)

    naive_hist = naive_sourced_scenario(L, n_ticks, J, g=g_lat)
    naive_final_monopole = naive_hist[-1][1]

    if use_split_for_no_monopole_check:
        split_hist = split_sourced_scenario(L, n_ticks, J, g=g_lat)
    else:
        split_hist = [(b, m, 0.0) for b, m in naive_sourced_scenario(L, n_ticks, J, g=g_lat)]
    split_final_monopole = split_hist[-1][1]
    split_final_EL_norm = split_hist[-1][2]

    # sanity: uncharged (J=0) split recipe reduces to plain free rotation
    zeroJ = np.zeros((3, L, L, L))
    E0, B0 = np.zeros((3, L, L, L)), np.zeros((3, L, L, L))
    for _ in range(n_ticks):
        E0, B0 = photon_step_spectral(E0, B0)
    uncharged_hist = split_sourced_scenario(L, n_ticks, zeroJ, g=g_lat)
    uncharged_residual = float(np.linalg.norm(uncharged_hist[-1][0] - B0))

    res = {
        "L": L, "L_stability": L_stability, "n_ticks": n_ticks,
        "angle_cubic_axis_deg": ang_axis,
        "angle_face_diagonal_deg": ang_face,
        "angle_body_diagonal_deg": ang_body,
        "angle_body_diagonal_deg_hiL": ang_body_hiL,
        "target_body_diagonal_deg": target_body,
        "magnitude_over_k_axis": mag_axis,
        "magnitude_over_k_body": mag_body,
        "ratio_omega_pair_over_Codd_small_k": ratio_small_k,
        "ratio_omega_pair_over_Codd_edge_k": ratio_edge_k,
        "commute_residual_relative": commute_residual,
        "naive_final_monopole_residual": naive_final_monopole,
        "split_final_monopole_residual": split_final_monopole,
        "split_final_EL_norm": split_final_EL_norm,
        "uncharged_residual_vs_free_rotation": uncharged_residual,
    }
    res["checks"] = {
        "curl_direction_matches_cubic_axis": bool(ang_axis < 1e-6),
        "curl_direction_face_diagonal_90deg": bool(abs(ang_face - 90.0) < 1e-6),
        "curl_direction_body_diagonal_arccos_1_3": bool(
            abs(ang_body - target_body) < 1e-6),
        "curl_direction_anisotropy_stable_with_L": bool(
            abs(ang_body - ang_body_hiL) < 1e-9),
        "curl_magnitude_isotropic": bool(abs(mag_axis - mag_body) < 1e-3),
        "omega_pair_matches_curl_at_small_k": bool(abs(ratio_small_k - 1.0) < 5e-4),
        "omega_pair_diverges_from_curl_away_from_small_k": bool(ratio_edge_k > 1.3),
        "rotation_commutes_with_TL_projection": bool(commute_residual < 1e-12),
        "naive_sourcing_violates_no_monopole": bool(naive_final_monopole > 1e-2),
        "split_sourcing_preserves_no_monopole": bool(split_final_monopole < 1e-8),
        "split_sourcing_couples_charge_into_EL": bool(split_final_EL_norm > 1e-6),
        "split_sourcing_reduces_to_free_rotation_when_uncharged": bool(
            uncharged_residual < 1e-10),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


# ======================================================================
# §5 — F391: a genuinely Ĉ(k)-transverse beam, and the axis/m_index
# breakdown mechanism this was built to test
# ======================================================================
#
# F390 (Stage 5's push scenario) and its review found the direction/anti-
# alignment claims hold only for an on-axis beam at m_index<=3 (L=16), and
# named a "likely, not derived" mechanism: ``photon.build_beam_packet``
# polarizes transverse to the Euclidean k̂, not Ĉ(k) (§1 above), which
# combined with Ĉ(k)'s own axis anisotropy could plausibly scramble the
# recoil direction off-axis.  :func:`build_ck_transverse_beam_packet` below
# removes that specific mismatch by construction (every Fourier mode's
# polarization is built already-orthogonal to that mode's own Ĉ(k), not
# merely projected-and-discarded after the fact the way
# :func:`split_transverse_longitudinal` is used in ``photon_fermion_push``)
# and :func:`check_ck_transverse_beam_mechanism` re-tests F390's own
# axis/m_index grid against it.  **Result: the breakdown pattern is
# unchanged.**  See ``findings/F391-ck-transverse-beam-mechanism.md`` for
# the full account, including the sharper Ĉ(k) structural fact this module
# also gates (Ĉ(k) is exactly *anti-parallel* to k̂ along the lattice's own
# y-axis, not merely "anisotropic" — a fact F387's own direction table never
# tested) and the alternative candidate mechanism (the per-link step's
# sensitivity to the fermion's own fixed internal spin state) this finding
# identifies but does not derive.


def build_ck_transverse_beam_packet(L, m_index, axis=0, pol_axis=None,
                                    sigma=4.0, center=None):
    """A travelling Gaussian photon beam whose polarization is built
    exactly `Ĉ(k)`-transverse **mode by mode**, not merely transverse to
    the Euclidean `k̂` (:func:`casim.engine.gauge.photon.build_beam_packet`)
    nor projected-and-discarded after the fact
    (:func:`split_transverse_longitudinal`, which throws away ~27% of the
    beam's own norm at F390's default configuration, F387 §caveats).

    Same envelope/carrier construction as ``photon.build_beam_packet``
    (a one-sided analytic signal `F(x) = envelope(x)·exp(ik0(x_axis-x0))`,
    `E=Re F`, `B=Im F`), but instead of assigning `F(x)` to a single fixed
    Cartesian component, the reference polarization direction `v0`
    (defaulting to the same `pol_axis=(axis+1)%3` convention) is projected
    onto the plane orthogonal to `Ĉ(k)` **at every Fourier mode independently**
    and renormalized to unit length there:

        e(k) = normalize( v0 − Ĉ̂(k) (Ĉ̂(k)·v0) )

    so `e(k)·Ĉ(k) ≡ 0` exactly (for `Ĉ(k)≠0`) — no norm is discarded, the
    polarization direction simply follows `Ĉ(k)`'s own local transverse
    plane instead of a single fixed lab-frame direction.  On the disclosed
    Nyquist-corner modes where `Ĉ(k)≡0` (F384 §3) there is no transverse
    plane to project onto; `v0` itself is used there (an arbitrary, physically
    inert choice — those modes are the same ones every `bcc_curl_symbol`
    consumer already treats as undecomposable).

    Returns ``(E, B, k0vec)``, same shape/contract as ``build_beam_packet``.
    """
    axis = int(axis)
    if pol_axis is None:
        pol_axis = (axis + 1) % 3
    pol_axis = int(pol_axis)
    if pol_axis == axis:
        raise ValueError("beam polarization must be transverse (pol_axis != axis)")
    v0 = np.zeros(3)
    v0[pol_axis] = 1.0

    k0 = 2.0 * np.pi * float(m_index) / float(L)
    if center is None:
        center = [L / 4.0 if a == axis else L / 2.0 for a in range(3)]
    sig = np.broadcast_to(np.asarray(sigma, float), (3,))
    x = [np.arange(L, dtype=float) for _ in range(3)]
    X = np.meshgrid(*x, indexing="ij")
    d = [np.remainder(X[a] - center[a] + L / 2.0, L) - L / 2.0 for a in range(3)]
    r2 = sum((d[a] / sig[a]) ** 2 for a in range(3))
    envelope = np.exp(-r2 / 2.0)
    F = envelope * np.exp(1j * k0 * d[axis])
    Fk = _fft.fftn(F)

    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    Cmag = np.sqrt(Cx ** 2 + Cy ** 2 + Cz ** 2)
    nz = Cmag > 1e-14
    Chx = np.where(nz, np.divide(Cx, Cmag, out=np.zeros_like(Cx), where=nz), 0.0)
    Chy = np.where(nz, np.divide(Cy, Cmag, out=np.zeros_like(Cy), where=nz), 0.0)
    Chz = np.where(nz, np.divide(Cz, Cmag, out=np.zeros_like(Cz), where=nz), 0.0)

    dot = v0[0] * Chx + v0[1] * Chy + v0[2] * Chz
    ex, ey, ez = v0[0] - dot * Chx, v0[1] - dot * Chy, v0[2] - dot * Chz
    enorm = np.sqrt(ex ** 2 + ey ** 2 + ez ** 2)
    ok = enorm > 1e-10
    ex_u = np.where(ok, np.divide(ex, enorm, out=np.zeros_like(ex), where=ok), v0[0])
    ey_u = np.where(ok, np.divide(ey, enorm, out=np.zeros_like(ey), where=ok), v0[1])
    ez_u = np.where(ok, np.divide(ez, enorm, out=np.zeros_like(ez), where=ok), v0[2])

    Vx = _fft.ifftn(Fk * ex_u)
    Vy = _fft.ifftn(Fk * ey_u)
    Vz = _fft.ifftn(Fk * ez_u)
    E = np.array([Vx.real, Vy.real, Vz.real])
    B = np.array([Vx.imag, Vy.imag, Vz.imag])
    k0vec = np.zeros(3)
    k0vec[axis] = k0
    return E, B, k0vec


def _push_scenario(L, g_lat, q, width, m_index, axis, sigma, amp, ticks,
                   use_ck_beam, spin_state="f_only", seed=0):
    """Shared harness for the checks below: build the F388/F389/F390
    coupled ``em_photon``/``fermion_em`` scenario, seed a beam via either
    :func:`build_ck_transverse_beam_packet` (``use_ck_beam=True``) or the
    F390-original recipe (``photon.build_beam_packet`` + projected-and-
    discarded via :func:`split_transverse_longitudinal``, ``use_ck_beam=
    False``), run it, and return ``(dP_matter, k0vec)``.  ``spin_state``
    overrides ``FermionEmChannel``'s default fixed ``g≡0`` chirality
    eigenstate — see ``check_ck_transverse_beam_mechanism``'s spin-
    sensitivity leg.
    """
    from casim.engine.core.coupled import EmPhotonChannel, FermionEmChannel
    from casim.engine.core.simulation import Simulation, LatticeSpec
    from casim.engine.core.observers import Momentum
    from casim.engine.gauge.photon import build_beam_packet

    lattice = LatticeSpec(L=L, dims=3, topology="bcc")
    em = EmPhotonChannel(name="em_photon", fermion="fermion_em", g_lat=g_lat,
                         q=q, use_radiative_current=True)
    fm = FermionEmChannel(name="fermion_em", photon="em_photon", q=q,
                          width=width, k0=[0.0, 0.0, 0.0])
    sim = Simulation(lattice=lattice, channels=[em, fm], seed=seed)

    if spin_state != "f_only":
        f = sim.states["fermion_em"]["f"]
        if spin_state == "equal":
            sim.states["fermion_em"]["f"] = f / np.sqrt(2)
            sim.states["fermion_em"]["g"] = f.copy() / np.sqrt(2)
        else:
            raise ValueError(spin_state)

    if use_ck_beam:
        E, B, k0vec = build_ck_transverse_beam_packet(
            L, m_index=m_index, axis=axis, sigma=sigma)
    else:
        E_raw, B_raw, k0vec = build_beam_packet(
            L, m_index=m_index, axis=axis, sigma=sigma)
        E, _ = split_transverse_longitudinal(E_raw)
        B, _ = split_transverse_longitudinal(B_raw)

    sim.states["em_photon"]["E"] = sim.states["em_photon"]["E"] + amp * E
    sim.states["em_photon"]["B"] = sim.states["em_photon"]["B"] + amp * B

    mom = Momentum()
    mom.observe(sim)
    pm0 = np.array(mom.records[-1]["channels"]["fermion_em"]["P_matter"])
    sim.step(ticks)
    mom.observe(sim)
    pm1 = np.array(mom.records[-1]["channels"]["fermion_em"]["P_matter"])
    return pm1 - pm0, np.asarray(k0vec, dtype=float)


def _safe_cos(a, b):
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na < 1e-12 or nb < 1e-12:
        return float("nan")
    return float(np.dot(a, b) / (na * nb))


def check_ck_transverse_beam_mechanism(L=16, g_lat=0.6, q=1.0, width=1.5,
                                       sigma=3.0, amp=0.15, ticks=20,
                                       use_ck_beam=True):
    """F391 gate entry.  See ``findings/F391-ck-transverse-beam-
    mechanism.md`` for the full derivation; this is the checklist its own
    tables report.

    Three groups of legs:

    1. **The new beam is genuinely `Ĉ(k)`-transverse** (machine precision),
       unlike F390's original construction (~27.5% longitudinal leak at its
       own default config, F387 §caveats/F390 §1).
    2. **The `Ĉ(k)` direction structure is sharper than F387 characterized**:
       `Ĉ(k)` is not merely "anisotropic" off the cubic axes — it is exactly
       *anti-parallel* to `k̂` along the lattice's own y-axis (`180°`, not
       merely "some other angle"), while the z-axis (like the x-axis F387
       already checked) stays exactly aligned (`0°`). F387's own table never
       tested the y- or z-axis in isolation, only x, the face diagonal, and
       the body diagonal.
    3. **The breakdown pattern is unchanged by the fix** (the actual
       negative result this finding reports): re-running F390's own
       axis/m_index grid with :func:`build_ck_transverse_beam_packet` in
       place of the original construction reproduces the same on-axis
       correlation, the same `m_index=4` sign flip, and the same off-axis
       decorrelation — ruling out the beam-polarization/`Ĉ(k)`-anisotropy
       mismatch as the mechanism. A supplementary, non-gated measurement
       (`dPm_spin_state_differs`, informational) shows the push vector
       genuinely depends on the fermion's own fixed internal spin state,
       the alternative candidate this finding identifies but does not
       derive.

    **Declared control** (``use_ck_beam=False``): swaps the *original*
    F390 beam recipe in for every leg. This must, and measured does, turn
    exactly the group-1 transversality legs red (the original recipe's
    ~27.5% leak is far above the new construction's near-zero residual)
    while leaving every group-2 (pure `Ĉ(k)`-structure, beam-independent)
    and group-3 (both constructions tested explicitly, side by side) leg
    unaffected.
    """
    from casim.engine.gauge.photon import build_beam_packet

    # -- group 1: transversality of the new construction -------------------
    beam_builder = (build_ck_transverse_beam_packet if use_ck_beam
                    else build_beam_packet)
    E_test, B_test, _ = beam_builder(L, m_index=2, axis=0, sigma=sigma)
    monopole_residual = iC_dot_B_norm(B_test)
    _, EL_test = split_transverse_longitudinal(E_test)
    lon_leak = float(np.linalg.norm(EL_test) / (np.linalg.norm(E_test) + 1e-30))

    # -- group 2: the sharper Ĉ(k) direction structure (beam-independent) --
    ang_y = curl_direction_angle((0, 1, 0), L=64)
    ang_z = curl_direction_angle((0, 0, 1), L=64)
    ang_y_hiL = curl_direction_angle((0, 1, 0), L=128)

    # -- group 3: re-run F390's own axis/m_index grid with the new beam,
    #    side by side with the original recipe (both always computed, so
    #    this group is unaffected by the declared control) -----------------
    def _cos_beam(m_index, axis, ck):
        dPm, k0v = _push_scenario(L, g_lat, q, width, m_index, axis, sigma,
                                  amp, ticks, use_ck_beam=ck)
        khat = k0v / np.linalg.norm(k0v)
        return _safe_cos(dPm, khat)

    cos_onaxis_new = _cos_beam(2, 0, True)
    cos_onaxis_old = _cos_beam(2, 0, False)
    cos_m4_new = _cos_beam(4, 0, True)
    cos_m4_old = _cos_beam(4, 0, False)
    cos_offaxis_new = _cos_beam(2, 1, True)
    cos_offaxis_old = _cos_beam(2, 1, False)

    # -- informational: push-vector sensitivity to the fermion's own fixed
    #    internal spin state, at a fixed (off-axis) beam config -- the
    #    alternative candidate mechanism, not derived here. Not gated on
    #    a specific direction/value, only on "the vector genuinely changes"
    #    (i.e. the field/beam construction is not the whole story). --------
    dPm_f, _ = _push_scenario(L, g_lat, q, width, 2, 1, sigma, amp, ticks,
                              use_ck_beam=True, spin_state="f_only")
    dPm_eq, _ = _push_scenario(L, g_lat, q, width, 2, 1, sigma, amp, ticks,
                               use_ck_beam=True, spin_state="equal")
    spin_cos = _safe_cos(dPm_f, dPm_eq)

    res = {
        "L": L, "g_lat": g_lat, "ticks": ticks,
        "monopole_residual": monopole_residual,
        "longitudinal_leak_fraction": lon_leak,
        "angle_y_axis_deg": ang_y, "angle_z_axis_deg": ang_z,
        "angle_y_axis_deg_hiL": ang_y_hiL,
        "cos_beam_onaxis_new": cos_onaxis_new, "cos_beam_onaxis_old": cos_onaxis_old,
        "cos_beam_m4_new": cos_m4_new, "cos_beam_m4_old": cos_m4_old,
        "cos_beam_offaxis_new": cos_offaxis_new, "cos_beam_offaxis_old": cos_offaxis_old,
        "dPm_f_only": dPm_f.tolist(), "dPm_equal_spin": dPm_eq.tolist(),
        "spin_state_push_cos": spin_cos,
    }
    res["checks"] = {
        "beam_exactly_ck_transverse": bool(monopole_residual < 1e-8),
        "beam_near_zero_longitudinal_leak": bool(lon_leak < 0.05),
        "curl_y_axis_antiparallel_180deg": bool(abs(ang_y - 180.0) < 1e-6),
        "curl_z_axis_parallel_0deg": bool(ang_z < 1e-6),
        "curl_y_axis_antiparallel_stable_with_L": bool(
            abs(ang_y - ang_y_hiL) < 1e-9),
        "onaxis_correlation_holds_with_both_beams": bool(
            cos_onaxis_new > 0.9 and cos_onaxis_old > 0.9),
        "m4_sign_flip_persists_with_both_beams": bool(
            cos_m4_new < -0.5 and cos_m4_old < -0.5),
        "offaxis_decorrelation_persists_with_both_beams": bool(
            abs(cos_offaxis_new) < 0.3 and abs(cos_offaxis_old) < 0.3),
        "push_direction_sensitive_to_fermion_spin_state": bool(
            not np.isnan(spin_cos) and spin_cos < 0.98),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


if __name__ == "__main__":
    import json
    r = check_em_photon_sourcing()
    print(json.dumps({k: v for k, v in r.items() if k != "checks"}, indent=2))
    print(json.dumps(r["checks"], indent=2))
    r2 = check_ck_transverse_beam_mechanism()
    print(json.dumps({k: v for k, v in r2.items() if k != "checks"}, indent=2))
    print(json.dumps(r2["checks"], indent=2))
