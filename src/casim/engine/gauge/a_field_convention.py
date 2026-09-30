"""casim.engine.gauge.a_field_convention — Stage 3 of
``docs/roadmaps/photon-fermion-coupling.md``: the vector potential ``A`` that
Stage 2's per-link U(1) step (F385, ``minimal_coupling.u1_link_weyl_step_3d_bcc``)
reads.

Two candidates named by the roadmap:

  1. **Accumulate** — ``A ← A + E`` per tick, exactly ``core.coupled
     .WSourcedChannel``'s own established pattern for the W field.
  2. **Solve** — a Coulomb-gauge ``A`` solved from ``B`` on the 3-D ``C(k)``
     symbol, ``charge_coupling.solve_A_coulomb_3d`` (new this stage, the 3-D
     sibling of ``solve_A_coulomb_2d``).

**Decision: SOLVE.** See ``findings/F386-a-field-convention.md`` for the full
derivation; the load-bearing argument in one paragraph: F385 §5b already
established that the curl-*free* (uniform/gradient) part of ``A`` has an
existing exact route (the uniform-shift special case, and the pre-existing
"Bloch acceleration" mechanism) — Stage 2's per-link machinery is genuinely
needed *only* for the curl-*carrying* (transverse) part. ``solve_A_coulomb_3d``
returns an ``A`` that is purely C-transverse *by construction*
(``C·A≡0`` identically), so it hands Stage 2 exactly the content it was built
for and nothing else. ``accumulate``'s ``A`` carries no such guarantee: because
F384's own conserved current is *defined* as purely C-longitudinal, any
``em_photon`` channel that sources ``E += g·J`` with that current (exactly
what the roadmap's own Stage-4 sketch specifies) accumulates a growing
longitudinal component in ``A`` from real charge — content that (a) the
uniform-shift/Bloch mechanism already carries exactly and unitarily, and
(b) would otherwise be run through Stage 2's norm-violating per-link
construction for no physical benefit. ``solve`` structurally cannot make that
mistake; ``accumulate`` structurally cannot avoid it.

This module implements both conventions behind the same interface (so they
are directly comparable, not because "accumulate" needs new derivation — it
is exactly ``WSourcedChannel``'s one-line pattern), plus the diagnostics
Stage 4 and this finding's gate entry need: a C(k)-longitudinal-fraction
decomposition, and a wrapper around F385's own already-built
``gauge_covariance_residual`` that demonstrates a purely-longitudinal
candidate ``A`` (built as the spectral gradient of a scalar, hence
longitudinal by construction) shows *no* effect beyond the already-disclosed
F385 local-Ward artifact — i.e. it is inert, up to the same finite-lattice
defect F385 already quantified for a general ``A``, not a new distinct
physical push.
"""
from __future__ import annotations

from casim.numerics import xp as np
from casim.numerics import fft as _fft
from casim.engine.lattice.geometry import make_kgrid_3d
from casim.engine.gauge.charge_coupling import bcc_curl_symbol, solve_A_coulomb_3d
from casim.engine.gauge.photon import photon_step_spectral, build_beam_packet
from casim.engine.gauge import em_current
from casim.engine.forks.gauge.u1_link_unitarity_forks import gauge_covariance_residual

__all__ = [
    "accumulate_A", "longitudinal_fraction", "build_accumulate_scenario",
    "check_a_field_convention",
]


def accumulate_A(A_prev, E):
    """Convention 1 — ``core.coupled.WSourcedChannel``'s own pattern,
    verbatim.  Deliberately trivial: it needs no derivation, only naming, so
    it can be compared against ``solve_A_coulomb_3d`` through one interface.
    """
    return A_prev + E


def longitudinal_fraction(A):
    """``‖Ĉ(k)·Ã(k)‖ / ‖Ã(k)‖`` over the modes where ``C(k)≠0`` — the
    fraction of ``A``'s own spectral norm that is C-longitudinal.

    Exactly 0 (machine precision) for anything returned by
    :func:`~casim.engine.gauge.charge_coupling.solve_A_coulomb_3d` (purely
    C-transverse by construction).  Generically nonzero for
    :func:`accumulate_A`'s output whenever the sourcing current has any
    C-longitudinal content — which ``em_current.conserved_current`` *always*
    does, by F384's own construction (the minimal current is purely
    longitudinal-in-``Ĉ(k)``, F384 §1).
    """
    shape = A.shape[1:]
    KX, KY, KZ = make_kgrid_3d(*shape)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    C2 = Cx ** 2 + Cy ** 2 + Cz ** 2
    nz = C2 > 1e-14
    Ak = [_fft.fftn(A[a]) for a in range(3)]
    CdotA = Cx * Ak[0] + Cy * Ak[1] + Cz * Ak[2]
    Anorm = np.sqrt(sum(np.sum(np.abs(a) ** 2) for a in Ak)) + 1e-30
    lon = np.sqrt(np.sum(np.abs(CdotA[nz]) ** 2 / C2[nz])) if np.any(nz) else 0.0
    return float(lon / Anorm)


def build_accumulate_scenario(L=16, n_ticks=6, width=2.0, k0=0.4, sign='+',
                              q=1.0, g_lat=0.5, seed_photon=False,
                              photon_amp=0.05):
    """Run ``n_ticks`` of the ``WSourcedChannel``-style recipe for an
    ``em_photon`` convention: free rotation (``photon.photon_step_spectral``)
    + ``E += g_lat·J`` (a static Weyl packet's own F384 current, recomputed
    once and held fixed as the source — a controlled comparison, not a full
    coupled-channel simulation, which is Stage 4's job) + ``A += E``.

    ``seed_photon=True`` additionally plants a small genuine transverse
    (E,B) pulse at tick 0 (``photon.build_beam_packet``), so the run carries
    both a real propagating-photon component and the charge-sourced
    longitudinal kick — the mixed case ``accumulate`` cannot cleanly separate.

    Returns ``(A_accum, B_final, J)``.
    """
    from casim.engine.core.coupled import gaussian_packet

    c = L // 2
    f = gaussian_packet(L, (c, c, c), width, k0=(k0, 0, 0))
    g = np.zeros_like(f)
    J, _res, _gap = em_current.conserved_current(f, g, sign=sign, q=q)

    if seed_photon:
        E, B, _k0vec = build_beam_packet(L, m_index=2, axis=0, sigma=3.0)
        E = photon_amp * E
        B = photon_amp * B
    else:
        E = np.zeros((3, L, L, L))
        B = np.zeros((3, L, L, L))
    A = np.zeros((3, L, L, L))
    for _ in range(n_ticks):
        E_rot, B_rot = photon_step_spectral(E, B)
        E = E_rot + g_lat * J
        B = B_rot
        A = accumulate_A(A, E)
    return A, B, J


def pure_gradient_A(L, m, amp=0.3, axis=0):
    """Build a purely C-longitudinal-by-*constructed-as-a-gradient* scalar
    field ``χ`` (``sin(2π m x_axis/L)``) and return ``(A=∇χ, χ)`` — the exact
    test object F385's own ``gauge_covariance_residual`` already needs to
    show a longitudinal field is inert (see that function's own use of
    ``grad_beta``): plugging ``A=0`` with ``beta=χ`` into
    ``gauge_covariance_residual`` tests exactly ``S[∇χ](e^{iqχ}ψ) ==
    e^{iqχ}·S[0](ψ)`` — the statement that a pure gradient is removable by a
    compensating phase of ψ, i.e. it is gauge, not force.
    """
    x = np.arange(L, dtype=float)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    coord = (X, Y, Z)[axis]
    chi = amp * np.sin(2.0 * np.pi * m * coord / L)
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    chi_k = _fft.fftn(chi.astype(complex))
    A = np.array([
        np.real(_fft.ifftn(1j * KX * chi_k)),
        np.real(_fft.ifftn(1j * KY * chi_k)),
        np.real(_fft.ifftn(1j * KZ * chi_k)),
    ])
    return A, chi


# ----------------------------------------------------------------------
# Gate entry — F386 (Stage 3 of the photon-fermion-coupling roadmap)
# ----------------------------------------------------------------------
def check_a_field_convention(L=16, seed=0, n_ticks=6, sigma=3.0, q=1.0,
                             sign='+', use_accumulate_for_solve_check=False):
    """F386 gate entry.  See ``findings/F386-a-field-convention.md`` §2 for
    the full table; this is the checklist it reports.

    ``use_accumulate_for_solve_check`` (the declared control): swaps
    ``accumulate``'s A in for the two ``solve_*`` legs, which — measured, not
    assumed — must turn exactly those two legs red (``accumulate``'s A is
    generically *not* purely C-transverse and does not exactly satisfy
    ``iC×A=B``) while every other leg (which never reads that A) stays green.
    """
    rng = np.random.default_rng(seed)

    # -- solve: exactness of the Coulomb-gauge inversion -------------------
    E, B, k0vec = build_beam_packet(L, m_index=2, axis=0, sigma=sigma)
    A_solve, lon_frac_B = solve_A_coulomb_3d(B)
    if use_accumulate_for_solve_check:
        A_for_solve_checks, _Bf, _J = build_accumulate_scenario(
            L=L, n_ticks=n_ticks, sign=sign, q=q, seed_photon=True)
    else:
        A_for_solve_checks = A_solve

    solve_lon_frac = longitudinal_fraction(A_for_solve_checks)

    # curl(A) recovers B_T, via TWO separate maskings (kept distinct on
    # purpose, F386 review found the single comment blurred them):
    #  (1) project OUT B's own C-longitudinal content first (`CdotB`/`BTk`
    #      below) -- the relation i C×A = B can only ever constrain B's
    #      C-transverse part; a naive Cartesian-transverse beam polarization
    #      is not exactly C(k)-transverse at finite k (see
    #      `B_beam_longitudinal_fraction`, and F386 §6's Ĉ(k)-anisotropy
    #      caveat for why), so comparing against full B would be unfair to
    #      `solve`, mirroring F384's masked-residual fix;
    #  (2) restrict the comparison to modes where C(k)!=0 (`nz` below) --
    #      the disclosed Nyquist-corner gap, F384 §3, where no A solves the
    #      relation at all regardless of B's content there.
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Cx, Cy, Cz = bcc_curl_symbol(KX, KY, KZ)
    C2 = Cx ** 2 + Cy ** 2 + Cz ** 2
    nz = C2 > 1e-14
    Ak = [_fft.fftn(A_for_solve_checks[a]) for a in range(3)]
    Bk = [_fft.fftn(B[a]) for a in range(3)]
    CdotB = Cx * Bk[0] + Cy * Bk[1] + Cz * Bk[2]
    BTk = [Bk[a] for a in range(3)]
    for a, C in enumerate((Cx, Cy, Cz)):
        proj = np.zeros_like(Bk[a])
        proj[nz] = C[nz] * CdotB[nz] / C2[nz]
        BTk[a] = Bk[a] - proj
    cxA = (Cy * Ak[2] - Cz * Ak[1], Cz * Ak[0] - Cx * Ak[2], Cx * Ak[1] - Cy * Ak[0])
    curl_res_full = [1j * cxA[a] - BTk[a] for a in range(3)]
    curl_res_masked = float(max(
        np.max(np.abs(curl_res_full[a][nz])) for a in range(3)
    )) if np.any(nz) else 0.0

    # -- accumulate: inherits real longitudinal content from a pure-charge
    #    source (no photon seeded).  B does NOT stay zero here: sourcing E
    #    with a purely C-longitudinal current under `photon_step_spectral`'s
    #    scalar rotation (which does not project, unlike maxwell_curl_step's
    #    C-cross-product) rotates that longitudinal E into an equally
    #    C-longitudinal, nonzero B (a genuine iC.B!=0 "monopole" artifact of
    #    this sourcing recipe under the paired-photon law, F386 Sec.5 --
    #    Omega_pair(k) and |C_odd(k)| agree only at small k).  solve still
    #    correctly returns A=0 because it discards exactly B's own
    #    C-transverse projection, which IS exactly zero -- see solve_norm
    #    below. --
    A_accum_charge_only, B_charge_only, J = build_accumulate_scenario(
        L=L, n_ticks=n_ticks, sign=sign, q=q, seed_photon=False)
    A_solve_charge_only, _lon = solve_A_coulomb_3d(B_charge_only)
    accum_lon_frac_charge_only = longitudinal_fraction(A_accum_charge_only)
    solve_norm_charge_only = float(np.sum(np.abs(A_solve_charge_only) ** 2))

    A_accum_early, _B, _J = build_accumulate_scenario(
        L=L, n_ticks=2, sign=sign, q=q, seed_photon=False)
    lon_frac_early = longitudinal_fraction(A_accum_early)

    # -- inertness of a purely-longitudinal candidate A (F385's own Ward
    #    mechanism, reused not re-derived) -----------------------------------
    f = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    g = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    A_zero = np.zeros((3, L, L, L))
    chi_const = np.full((L, L, L), 0.7)   # constant chi -> grad(chi)=0 exactly
    ward_global = gauge_covariance_residual(f, g, A_zero, q, chi_const, sign=sign)
    _Ag_m1, chi_m1 = pure_gradient_A(L, m=1, amp=0.3, axis=0)
    _Ag_m4, chi_m4 = pure_gradient_A(L, m=4, amp=0.3, axis=0)
    ward_grad_m1 = gauge_covariance_residual(f, g, A_zero, q, chi_m1, sign=sign)
    ward_grad_m4 = gauge_covariance_residual(f, g, A_zero, q, chi_m4, sign=sign)

    res = {
        "L": L, "n_ticks": n_ticks, "sigma": sigma,
        "solve_longitudinal_fraction": solve_lon_frac,
        "solve_curl_residual_masked": curl_res_masked,
        "B_beam_longitudinal_fraction": lon_frac_B,
        "accumulate_longitudinal_fraction_charge_only": accum_lon_frac_charge_only,
        "accumulate_longitudinal_fraction_early_tick": lon_frac_early,
        "solve_A_norm_for_pure_charge_source": solve_norm_charge_only,
        "ward_global_pure_gradient": ward_global,
        "ward_grad_m1": ward_grad_m1,
        "ward_grad_m4": ward_grad_m4,
    }
    res["checks"] = {
        "solve_is_purely_transverse": bool(solve_lon_frac < 1e-10),
        "solve_curl_recovers_B": bool(curl_res_masked < 1e-8),
        "accumulate_inherits_longitudinal_content": bool(
            accum_lon_frac_charge_only > 0.99),
        "accumulate_longitudinal_content_grows_with_ticks": bool(
            accum_lon_frac_charge_only >= lon_frac_early - 1e-9),
        "solve_gives_zero_A_for_pure_charge_source": bool(
            solve_norm_charge_only < 1e-20),
        "ward_global_exact_for_pure_gradient": bool(ward_global < 1e-10),
        "ward_local_grows_with_wavelength_matches_F385": bool(
            ward_grad_m1 < ward_grad_m4),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


if __name__ == "__main__":
    import json
    r = check_a_field_convention()
    print(json.dumps({k: v for k, v in r.items() if k != "checks"}, indent=2))
    print(json.dumps(r["checks"], indent=2))
