"""Fork: U(1) per-link unitarity/momentum-transfer adjudication
================================================================
Stage 2 of `docs/roadmaps/photon-fermion-coupling.md`. The primary
construction (`gauge.minimal_coupling.u1_link_weyl_step_3d_bcc`, fork **(a)**
— accept the drift) transfers momentum but is unitary only for A ≡ 0 or A
spatially uniform (that function's own docstring proves the uniform case
exactly). This module carries the two alternative constructions the roadmap
names and the harness compares them under:

  **(b)** Strang-split — half the per-link Peierls phase applied at the
          source site (before the fractional shift), half at the destination
          (after) — `u1_link_step_strang_split`.
  **(d)** per-site polar renormalisation — fork (a)'s output rescaled site by
          site to force exact local norm conservation (the same
          re-unitarisation `weak_wmu._u_eff_from_links` already applies to
          the SU(2) site-average construction, moved here from "site
          average" to "per-site output projection") — `u1_link_step_renormalized`.

Fork **(c)** (a link-dependent 2×2 unitary per mode) is not a separate
construction here: `minimal_coupling.u1_link_weyl_step_3d_bcc`'s own
docstring proves it collapses to fork (a) itself in the one case where a
per-mode unitary is well-defined at all — spatially uniform A, where the
"link-dependent unitary" is exactly `bcc_unitary(k+qA)`, a rigid momentum
shift. For genuinely non-uniform A there is no single k that a "per-mode"
unitary could be built at (translation invariance is broken by A(x)), so (c)
is not a distinct construction to adjudicate — this is itself part of the
finding, not an omission.

Not a candidate fix in the `curl_fork_*` sense (there is no single "right"
geometry to pick here) — a genuine three-way adjudication among constructions
that all reduce to the same free step and the same exact uniform-A limit, and
differ only in how they handle a spatially varying A.
"""
from casim.numerics import xp as np
from casim.numerics import fft as _fft
from casim.engine.lattice.geometry import make_kgrid_3d
from casim.engine.lattice.bcc import bcc_fractional_shift, weyl_step_3d_bcc
from casim.engine.gauge.weak_wmu import BCC_DIRS, _SPINOR_MATS
from casim.constants import c_lat
from casim.engine.gauge.minimal_coupling import u1_link_weyl_step_3d_bcc

FORK_NAME = "u1_link_unitarity"


def u1_link_step_strang_split(f, g, A, q, sign='+'):
    """Fork (b): half the Peierls phase at the source, half at the
    destination, for each of the 8 BCC directions independently (8
    direction-specific pre-multiplications, hence 8 forward FFTs instead of
    the 2 fork (a) needs — the same ~3.5x cost `covariant_weyl_step_3d_bcc_exact`
    already pays for the analogous SU(2) exactness upgrade).

    Symmetrising the phase around the kinetic step is the standard
    lattice-gauge-theory device for pushing a Peierls-substitution error up
    an order in the lattice spacing (Strang splitting: `e^{A/2}e^{B}e^{A/2}
    = e^{A+B} + O(commutator terms)` vs `e^{A}e^{B} = e^{A+B} + O(1st order)`).
    It is not expected to *restore* exact unitarity (the per-direction phases
    still act through a non-commuting sum of non-orthogonal shift operators)
    — the roadmap's own framing is `O(a²)`, an improvement in power, not a
    cure.
    """
    if q == 0 or A is None or not np.any(A):
        return weyl_step_3d_bcc(f, g, sign=sign)

    KX, KY, KZ = make_kgrid_3d(*f.shape)
    M_mats = _SPINOR_MATS[sign]
    inv_sqrt3 = c_lat

    f_new = np.zeros_like(f)
    g_new = np.zeros_like(g)
    for i, (dx, dy, dz) in enumerate(BCC_DIRS):
        half_phase = 0.5 * q * inv_sqrt3 * (A[0] * dx + A[1] * dy + A[2] * dz)
        half = np.exp(1j * half_phase)
        f_pre = half * f
        g_pre = half * g
        F_pre_k = _fft.fftn(f_pre)
        G_pre_k = _fft.fftn(g_pre)
        f_sh = _fft.ifftn(bcc_fractional_shift(F_pre_k, KX, KY, KZ, dx, dy, dz))
        g_sh = _fft.ifftn(bcc_fractional_shift(G_pre_k, KX, KY, KZ, dx, dy, dz))
        M = M_mats[i]
        f_rot = M[0, 0] * f_sh + M[0, 1] * g_sh
        g_rot = M[1, 0] * f_sh + M[1, 1] * g_sh
        # `half` is re-evaluated at the (post-shift) destination site — same
        # field, same array, applied a second time after the rotation.
        f_new += half * f_rot
        g_new += half * g_rot
    return f_new, g_new


def u1_link_step_renormalized(f, g, A, q, sign='+'):
    """Fork (d): fork (a)'s output, rescaled site by site so its local
    probability density matches **the free step's own local density**,
    ``|f'(x)|²+|g'(x)|² ≡ |f_free(x)|²+|g_free(x)|²`` — not the pre-step
    density (see caveat below). Global norm conservation follows
    automatically (the free step already conserves the total). This is a
    nonlinear, non-spectral fudge — a per-site polar/phase-preserving
    magnitude projection, not a unitary operator, not derived from any
    action principle — included because it is the cheapest construction
    that is *exactly* norm-conserving for any A, and the natural question is
    whether the directional push fork (a) carries survives it.

    **First version of this function renormalised against the pre-step
    density instead and was wrong**, not merely a design choice: the free
    step (A≡0) already redistributes local density (a moving packet's ρ(x)
    is not static even with no coupling at all), so forcing ρ'(x)≡ρ(x) at
    A=0 fights the free step's own correct physics and fails W1.2 (A≡0 must
    reduce exactly to `weyl_step_3d_bcc`) outright — measured, it does not:
    the pre-step-density version showed an O(1) reduction failure at A=0 and
    a spurious ~50-100x momentum kick relative to forks (a)/(b) at the same
    field amplitude, an artifact of fighting free propagation, not a
    genuine coupling effect. Renormalising onto the free step's *own*
    density (this version) reduces to it exactly at A≡0 by construction.
    """
    f2, g2 = u1_link_weyl_step_3d_bcc(f, g, A, q, sign=sign)
    f_free, g_free = weyl_step_3d_bcc(f, g, sign=sign)
    rho_target = np.abs(f_free) ** 2 + np.abs(g_free) ** 2
    rho1 = np.abs(f2) ** 2 + np.abs(g2) ** 2
    safe = rho1 > 1e-300
    scale = np.ones_like(rho1)
    scale[safe] = np.sqrt(rho_target[safe] / rho1[safe])
    return f2 * scale, g2 * scale


def matter_momentum(f, g):
    """⟨k⟩ = Σ_k k·(|f̃(k)|²+|g̃(k)|²) / N — the same spectral construction
    as `core.observers.Momentum`'s `P_matter` leg, standalone (no Simulation
    object needed) so the three forks can be compared directly."""
    shape = f.shape
    KX, KY, KZ = make_kgrid_3d(*shape)
    n = KX.size
    Fk = _fft.fftn(f)
    Gk = _fft.fftn(g)
    dens = np.abs(Fk) ** 2 + np.abs(Gk) ** 2
    return np.array([
        float(np.sum(KX * dens)) / n,
        float(np.sum(KY * dens)) / n,
        float(np.sum(KZ * dens)) / n,
    ])


def norm(f, g):
    return float(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2))


def gauge_covariance_residual(f, g, A, q, beta, sign='+'):
    """Ward-identity residual, mirroring the W1.x SU(2) suite: does
    ``S[A+∇β](e^{iqβ}ψ) == e^{iqβ}·S[A](ψ)`` (fork (a))? ``∇β`` is the
    genuine spectral gradient (``i*k·β̃(k)``, IFFT'd) — a well-defined
    lattice-independent object, not tied to the fractional-hop geometry, so
    the residual measured here is honestly the construction's own
    departure from covariance, not an artifact of how ``∇β`` was built.
    """
    KX, KY, KZ = make_kgrid_3d(*f.shape)
    beta_k = _fft.fftn(beta.astype(complex))
    grad_beta = np.array([
        np.real(_fft.ifftn(1j * KX * beta_k)),
        np.real(_fft.ifftn(1j * KY * beta_k)),
        np.real(_fft.ifftn(1j * KZ * beta_k)),
    ])
    phase = np.exp(1j * q * beta)
    f_lhs, g_lhs = u1_link_weyl_step_3d_bcc(phase * f, phase * g,
                                            A + grad_beta, q, sign=sign)
    f_rhs0, g_rhs0 = u1_link_weyl_step_3d_bcc(f, g, A, q, sign=sign)
    f_rhs, g_rhs = phase * f_rhs0, phase * g_rhs0
    return float(np.max(np.abs(f_lhs - f_rhs)) + np.max(np.abs(g_lhs - g_rhs)))


# ----------------------------------------------------------------------
# Gate entry — F385 (Stage 2 of the photon-fermion coupling roadmap)
# ----------------------------------------------------------------------
def check_u1_link_forks(L=16, seed=0, amp_A=0.2, amp_beta=0.3, sigma=3.0,
                        q=1.0, sign='+', corrupt_a0=False):
    """F385 gate entry. See the module docstring and
    `findings/F385-u1-link-covariant-step.md` for the full derivation;
    this is the checklist the finding's §2 table reports.

    ``corrupt_a0`` (the declared control): forces a tiny nonzero A into the
    "A≡0 must reduce to the free step" checks, which must — and, measured,
    does — turn exactly the three ``reduces_to_free_*`` legs red while
    leaving every other leg (which never uses that corrupted field) green.
    """
    rng = np.random.default_rng(seed)
    f = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    g = (rng.standard_normal((L, L, L)) + 1j * rng.standard_normal((L, L, L)))
    n0 = norm(f, g)

    x = np.arange(L)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    c = L // 2
    bump = np.exp(-(((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2))
                  / (2.0 * sigma ** 2))

    zeroA = np.zeros((3, L, L, L))
    if corrupt_a0:
        zeroA = zeroA + 1e-3   # a control-only perturbation: A is no longer 0

    # -- W1.2: A==0 reduces exactly to the free step, each fork -----------
    f_free, g_free = weyl_step_3d_bcc(f, g, sign=sign)
    fa0, ga0 = u1_link_weyl_step_3d_bcc(f, g, zeroA, q, sign=sign)
    fb0, gb0 = u1_link_step_strang_split(f, g, zeroA, q, sign=sign)
    fd0, gd0 = u1_link_step_renormalized(f, g, zeroA, q, sign=sign)
    err_a0 = float(np.max(np.abs(fa0 - f_free)) + np.max(np.abs(ga0 - g_free)))
    err_b0 = float(np.max(np.abs(fb0 - f_free)) + np.max(np.abs(gb0 - g_free)))
    err_d0 = float(np.max(np.abs(fd0 - f_free)) + np.max(np.abs(gd0 - g_free)))

    # -- exact special case: spatially UNIFORM A -> a rigid k-shift --------
    A0x, A0y, A0z = 0.3, -0.2, 0.5
    Aunif = np.zeros((3, L, L, L))
    Aunif[0], Aunif[1], Aunif[2] = A0x, A0y, A0z
    fu, gu = u1_link_weyl_step_3d_bcc(f, g, Aunif, q, sign=sign)
    from casim.engine.lattice.bcc import bcc_unitary
    KX, KY, KZ = make_kgrid_3d(L, L, L)
    Uff, Ufg, Ugf, Ugg = bcc_unitary(KX + q * A0x, KY + q * A0y, KZ + q * A0z,
                                     sign=sign)
    Fk, Gk = _fft.fftn(f), _fft.fftn(g)
    fu_ref = _fft.ifftn(Uff * Fk + Ufg * Gk)
    gu_ref = _fft.ifftn(Ugf * Fk + Ugg * Gk)
    uniform_shift_err = float(np.max(np.abs(fu - fu_ref))
                              + np.max(np.abs(gu - gu_ref)))
    uniform_drift = abs(norm(fu, gu) - n0) / n0

    # -- gauge covariance: global exact, local O(a)-shrinking --------------
    A = np.array([amp_A * bump, 0.3 * amp_A * bump, 0.0 * bump])
    beta_const = np.full((L, L, L), 0.7)
    ward_global = gauge_covariance_residual(f, g, A, q, beta_const, sign=sign)
    beta_m1 = amp_beta * np.sin(2.0 * np.pi * 1 * X / L)
    beta_m4 = amp_beta * np.sin(2.0 * np.pi * 4 * X / L)
    ward_m1 = gauge_covariance_residual(f, g, A, q, beta_m1, sign=sign)
    ward_m4 = gauge_covariance_residual(f, g, A, q, beta_m4, sign=sign)

    # -- fork (a) norm-drift scaling: O(|qA|) -------------------------------
    amps = np.array([0.005, 0.01, 0.02, 0.04, 0.08])
    drifts = []
    for a in amps:
        Aa = np.array([a * bump, 0.3 * a * bump, 0.0 * bump])
        f2, g2 = u1_link_weyl_step_3d_bcc(f, g, Aa, q, sign=sign)
        drifts.append(abs(norm(f2, g2) - n0) / n0)
    drifts = np.array(drifts)
    slope = float(np.polyfit(np.log(amps), np.log(drifts), 1)[0])

    # -- fork (d): exact conservation, momentum transfer survives ----------
    fd, gd = u1_link_step_renormalized(f, g, A, q, sign=sign)
    fork_d_drift = abs(norm(fd, gd) - n0) / n0

    p0 = matter_momentum(f, g)
    fa, ga = u1_link_weyl_step_3d_bcc(f, g, A, q, sign=sign)
    fb, gb = u1_link_step_strang_split(f, g, A, q, sign=sign)
    dp_a = matter_momentum(fa, ga) - p0
    dp_b = matter_momentum(fb, gb) - p0
    dp_d = matter_momentum(fd, gd) - p0
    mag_a, mag_b, mag_d = (float(np.linalg.norm(dp_a)),
                           float(np.linalg.norm(dp_b)),
                           float(np.linalg.norm(dp_d)))

    res = {
        "err_reduces_to_free_a": err_a0,
        "err_reduces_to_free_b": err_b0,
        "err_reduces_to_free_d": err_d0,
        "uniform_shift_err": uniform_shift_err,
        "uniform_drift": uniform_drift,
        "ward_global": ward_global,
        "ward_m1": ward_m1,
        "ward_m4": ward_m4,
        "norm_drift_slope_fork_a": slope,
        "fork_d_drift": fork_d_drift,
        "momentum_transfer_mag": {"a": mag_a, "b": mag_b, "d": mag_d},
    }
    res["checks"] = {
        "reduces_to_free_a": bool(err_a0 < 1e-10),
        "reduces_to_free_b": bool(err_b0 < 1e-10),
        "reduces_to_free_d": bool(err_d0 < 1e-10),
        "uniform_A_exact_unitary": bool(uniform_shift_err < 1e-10
                                        and uniform_drift < 1e-10),
        "ward_global_exact": bool(ward_global < 1e-10),
        "ward_local_shrinks_with_wavelength": bool(ward_m1 < ward_m4),
        "norm_drift_is_O_qA": bool(0.5 < slope < 1.5),
        "fork_d_exactly_conserves_norm": bool(fork_d_drift < 1e-10),
        "momentum_transfer_nonzero_all_forks": bool(
            mag_a > 0.1 and mag_b > 0.1 and mag_d > 0.1),
        "fork_d_preserves_momentum_signal": bool(
            0.1 * mag_a < mag_d < 10.0 * mag_a),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res
