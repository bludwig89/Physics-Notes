"""
reflection_positivity.py -- Osterwalder-Seiler link reflection positivity for
the BCC_3 x Z lattice gauge action (F335).

Completeness row B7 (confinement) named a genuine transfer-matrix/positivity
proof as its remaining residual for the 3+1D leg: a repo-wide grep for
"reflection positiv", "Osterwalder", "Schrader", "cluster expansion" returned
zero hits (F323 Sec 4, completeness-2026-08-20-prompts.md B7). This module is
the first content at those grep targets.

What is established here (F335):

1. `loop_structure_reflection_hypotheses` -- an EXACT, randomness-free check,
   read directly off `bcc_action.BCC4_LOOPS`/`_stored`, that the BCC_3 x Z
   action satisfies the three structural hypotheses the general Wilson-action
   link-reflection-positivity theorem needs (Osterwalder & Seiler 1978 Ann.
   Phys. 110, 440; extended to site reflections and all observables by
   Menotti & Pelissetto 1987 Commun. Math. Phys. 113, 369; the modern
   character-coefficient-free "sum of squares" factorization form used here
   follows the exposition in Faizal, Ali & Alshal 2026, arXiv:2606.19362
   Sec. 2.1): (a) the only temporal hop is the nearest-neighbour +-t_hat,
   (b) every purely-spatial loop (rhombus) has zero net time component and
   so lies entirely within one time-slice, (c) every mixed loop crosses
   exactly one time-step and contains its two temporal-link legs linearly
   (degree 1, one forward one reverse, never repeated or squared). NOTHING
   in this hypothesis list, or in the OS-Seiler/Menotti-Pelissetto proof
   itself, references the spatial lattice's connectivity -- the argument is
   topological in the time direction alone. That is the load-bearing
   observation of F335: it is what lets a hypercubic-lattice theorem carry
   over to a BCC-spatial x Z-time lattice with NO new machinery.

2. `theta_reflect_config` -- the concrete time-reflection map for this
   lattice (site tau -> Lt-1-tau for spatial fields, no dagger; tau ->
   (Lt-2-tau) mod Lt WITH a dagger for the single temporal field), plus
   `reflection_involution_residual` (theta o theta == identity, exact) and
   `mixed_plaquette_reflection_trace_residual` (Tr(theta P(tau)) ==
   conj(Tr P(tau_mirror)) exactly -- a cyclic-permutation identity, NOT a
   raw-matrix identity; see the module docstring of that function for why).

3. `su2_character_coeff_numeric` / `su2_character_positivity_residual` -- an
   independent, exact SUPPLEMENTARY result for the SU(2) sector: the Wilson
   Boltzmann weight's character-expansion coefficients a_j(beta) are
   strictly positive for all beta > 0 and all spin j, via the classical
   Bessel-function identity a_j(beta) = I_2j(2 beta) - I_2j+2(2 beta) =
   ((2j+1)/beta) I_2j+1(2 beta) > 0 (Bessel recursion I_{n-1}(x)-I_{n+1}(x)
   = (2n/x) I_n(x), all modified Bessel I_n(x) > 0 for x > 0). This is NOT
   needed by the general link-reflection proof used in (1) -- Faizal et al.
   2026 Sec. 2.1 explicitly note link reflection positivity for the ordinary
   (non-heat-kernel) Wilson action holds "without requiring b_rho >= 0" via
   direct Peter-Weyl factorization -- but it is a fully closed-form,
   independently-checkable exact result for one sector, computed here by
   direct numerical quadrature against the SU(2) Haar/Weyl measure (no scipy
   dependency, D8-compliant: numpy quadrature only, matching the closed-form
   Bessel identity to the achieved quadrature precision).

4. `reflection_positivity_gram_check` -- a numerical cross-check, NOT a
   proof and NOT a re-attack of confinement-measure (string-tension) MC
   sampling. It Monte-Carlo-samples the Gram matrix G_ij =
   <F_i(mirrored slice) F_j(positive slice)> built from the ten local
   plaquette traces (6 rhombi + 4 mixed rectangles) and checks it comes out
   Hermitian positive-semi-definite, which is the direct numerical
   signature RP predicts. See Sec. 4 of F335 for the honest reading of the
   result: the dominant (O_h-symmetric) eigenvalue is unambiguously and
   overwhelmingly positive; the nine near-degenerate residual directions are
   statistically consistent with zero at the achieved statistics and do NOT
   show a stable, growing violation, but are not separately resolved either
   -- reported as inconclusive-but-not-contradicting, not as confirmation.
"""

from casim.numerics import xp as np

from casim.engine.gauge.bcc_action import (
    BCC_LINK_AXES, BCC4_LOOPS, TIME_AXIS, _T_HOP, _stored,
    hot_links_4d, thermalise_4d, sweep_4d, plaquette_4d, _site_masks,
    _dagger,
)
from casim.numerics import rng as _rng

__all__ = [
    'loop_structure_reflection_hypotheses',
    'theta_reflect_config', 'reflection_involution_residual',
    'mixed_plaquette_reflection_trace_residual',
    'su2_character_coeff_numeric', 'su2_character_positivity_residual',
    'local_plaquette_observable_batch', 'reflection_positivity_gram_check',
    'check_reflection_positivity_bcc',
]


# ══════════════════════════════════════════════════════════════════════════
#  1. Structural hypothesis check (exact, no randomness)
# ══════════════════════════════════════════════════════════════════════════

def loop_structure_reflection_hypotheses() -> dict:
    """Verify, from `BCC4_LOOPS` alone, the three hypotheses the general
    link-reflection-positivity theorem needs. Every field here is an exact
    integer/boolean count, not a measurement."""
    rhombus_dt_zero = True
    mixed_two_temporal_linear = True
    mixed_one_forward_one_reverse = True
    only_nn_time_hop = True

    for lab, bk, legs in BCC4_LOOPS:
        temporal_legs = [(h, off) for (h, off) in legs if h[TIME_AXIS] != 0]
        if bk == 's':
            if temporal_legs:
                rhombus_dt_zero = False
            continue
        # bk == 't': the mixed rectangle
        if len(temporal_legs) != 2:
            mixed_two_temporal_linear = False
            continue
        signs = sorted(h[TIME_AXIS] for h, _off in temporal_legs)
        if signs != [-1, 1]:
            mixed_one_forward_one_reverse = False
        for h, _off in temporal_legs:
            if h[:3] != (0, 0, 0) or abs(h[TIME_AXIS]) != 1:
                only_nn_time_hop = False

    return {
        'rhombus_dt_zero': rhombus_dt_zero,
        'mixed_two_temporal_linear': mixed_two_temporal_linear,
        'mixed_one_forward_one_reverse': mixed_one_forward_one_reverse,
        'only_nn_time_hop': only_nn_time_hop,
        'n_rhombi': sum(1 for _l, bk, _g in BCC4_LOOPS if bk == 's'),
        'n_mixed': sum(1 for _l, bk, _g in BCC4_LOOPS if bk == 't'),
        'all_hypotheses_hold': (rhombus_dt_zero and mixed_two_temporal_linear
                                 and mixed_one_forward_one_reverse
                                 and only_nn_time_hop),
    }


# ══════════════════════════════════════════════════════════════════════════
#  2. The reflection map and its exact identities
# ══════════════════════════════════════════════════════════════════════════

def theta_reflect_config(links: dict, broken_dagger: bool = False) -> dict:
    """Time-reflection theta through the plane between slice Lt-1 and slice
    0. Spatial fields: tau -> Lt-1-tau, no dagger (a purely spatial link
    never crosses a time-slice, so reflection just relabels its slice).
    Temporal field: tau -> (Lt-2-tau) mod Lt, WITH a dagger (the directed
    bond tau->tau+1 becomes, after t -> -1-t, a bond running backwards in
    time, i.e. the dagger of the forward-stored bond at the new base site).

    ``broken_dagger=True`` is the declared control: drop the dagger on the
    temporal field.  Every field stays in SU(N) (a link is still unitary),
    so no unitarity leg can see it.  Measured, not assumed: the underlying
    time-index permutation tau -> (Lt-2-tau) mod Lt is ALREADY self-inverse
    (a pure reflection of the index), so dropping the dagger leaves
    ``reflection_involution_residual`` at exactly 0 -- undaggered-theta is
    still an involution on the index, just not the physically correct map --
    while ``mixed_plaquette_reflection_trace_residual`` (which depends on
    the dagger, not just the index map) reddens to O(1).  That asymmetry is
    itself informative: it is why the trace identity, not the involution
    check, is the leg that actually certifies the dagger convention.
    """
    Lt = links['t'].shape[TIME_AXIS]
    N = links['N']
    new_s = [a_field[:, :, :, ::-1, :, :].copy() for a_field in links['s']]
    idx = [(Lt - 2 - t) % Lt for t in range(Lt)]
    t_reflected = links['t'][:, :, :, idx, :, :]
    new_t = t_reflected.copy() if broken_dagger else _dagger(t_reflected)
    return {'s': new_s, 't': new_t, 'N': N}


def reflection_involution_residual(shape4, N: int = 2,
                                   channel: str = 'F335_involution',
                                   broken_dagger: bool = False) -> float:
    """``theta(theta(links)) == links`` exactly (theta is an involution)."""
    links = hot_links_4d(shape4, N=N, channel=channel)
    twice = theta_reflect_config(theta_reflect_config(links, broken_dagger),
                                 broken_dagger)
    worst = max(float(np.abs(a0 - a2).max())
                for a0, a2 in zip(links['s'], twice['s']))
    worst = max(worst, float(np.abs(links['t'] - twice['t']).max()))
    return worst


def mixed_plaquette_reflection_trace_residual(shape4, N: int = 2, tau: int = 1,
                                              channel: str = 'F335_trace_map',
                                              broken_dagger: bool = False) -> float:
    """``Tr(theta(P_mixed)(tau)) == conj(Tr(P_mixed(tau_mirror)))`` exactly.

    NOT a raw-matrix identity: the mixed rectangle is the 4-cycle
    ``U_a U_t U_a^dag U_t^dag``, and theta's action on it works out to a
    CYCLIC ROTATION of the daggered original loop rather than the same
    matrix -- trace is cyclic-invariant, the raw matrix need not be equal
    (and generically is not; a caller who checks the raw matrix instead of
    the trace will see an O(1) "residual" that is not a bug -- see F335
    Sec. 2 for the four-line derivation of the cyclic-rotation identity).
    """
    links = hot_links_4d(shape4, N=N, channel=channel)
    tlinks = theta_reflect_config(links, broken_dagger)
    Lt = shape4[TIME_AXIS]
    mixed_label = next(lab for lab, bk, _ in BCC4_LOOPS if bk == 't')
    tau_m = (Lt - 2 - tau) % Lt
    P_theta = plaquette_4d(tlinks, mixed_label)
    P_orig = plaquette_4d(links, mixed_label)
    tr_theta = np.trace(P_theta[:, :, :, tau], axis1=-2, axis2=-1)
    tr_orig_conj = np.conj(np.trace(P_orig[:, :, :, tau_m], axis1=-2, axis2=-1))
    return float(np.abs(tr_theta - tr_orig_conj).max())


# ══════════════════════════════════════════════════════════════════════════
#  3. SU(2) Wilson-action character-coefficient positivity (exact, closed
#     form; verified here by direct numpy quadrature -- no scipy, D8)
# ══════════════════════════════════════════════════════════════════════════

def _su2_character(theta: np.ndarray, j: float) -> np.ndarray:
    """The spin-j SU(2) character as a function of the rotation angle theta
    (Tr_F U = 2 cos(theta/2))."""
    num = np.sin((2 * j + 1) * theta / 2.0)
    den = np.sin(theta / 2.0)
    return np.where(np.abs(den) < 1e-10, 2 * j + 1, num / den)


def su2_character_coeff_numeric(j: float, beta: float, n: int = 200_001) -> float:
    """``a_j(beta) = integral over Haar measure of exp(beta Re Tr U) chi_j(U)``.

    Weyl integration formula for SU(2): ``dmu(theta) = (1/pi) sin^2(theta/2)
    dtheta``, ``theta in [0, 2 pi)``. Plain Riemann-sum quadrature (odd `n`
    for a symmetric midpoint grid) -- no scipy, matching D8. The closed form
    is ``a_j(beta) = I_{2j}(2 beta) - I_{2j+2}(2 beta)`` (modified Bessel
    functions); this function verifies it numerically without importing it.
    """
    theta = (np.arange(n) + 0.5) * (2 * np.pi / n)
    weight = (1.0 / np.pi) * np.sin(theta / 2.0) ** 2
    integrand = np.exp(2 * beta * np.cos(theta / 2.0)) * _su2_character(theta, j) * weight
    return float(np.sum(integrand) * (2 * np.pi / n))


def su2_character_positivity_residual(betas=(0.3, 1.0, 3.0),
                                      js=(0, 0.5, 1, 1.5, 2, 3)) -> dict:
    """``min over (beta, j) of a_j(beta)``; positive means every sampled
    coefficient came out on the correct side. Not a proof for all
    (beta, j) -- the closed-form Bessel-recursion argument in the module
    docstring is the actual proof; this is its numerical witness."""
    vals = {(b, j): su2_character_coeff_numeric(j, b) for b in betas for j in js}
    worst = min(vals.values())
    return {'min_coefficient': worst, 'all_positive': worst > 0.0,
            'coefficients': {f'beta={b}_j={j}': v for (b, j), v in vals.items()}}


# ══════════════════════════════════════════════════════════════════════════
#  4. Numerical Gram-matrix cross-check (Monte Carlo support evidence, not a
#     proof; NOT the confinement-measure sampling named as unable to close
#     this residual -- a different target, see module docstring item 4)
# ══════════════════════════════════════════════════════════════════════════

def local_plaquette_observable_batch(links: dict, tau: int, N: int) -> np.ndarray:
    """The ten real, gauge-invariant ``Re tr P / N`` values (6 rhombi + 4
    mixed rectangles) at one time-slice, site-averaged. Every loop is read
    at the SAME `tau` here -- the caller is responsible for choosing which
    slice each loop type belongs at when building a reflected partner (see
    `reflection_positivity_gram_check`, which does NOT call this with one
    shared tau_neg for rhombi and mixed rectangles -- they mirror to
    DIFFERENT slices, `Lt-1-tau` vs `(Lt-2-tau) mod Lt` respectively; an
    earlier version of this function's caller used one shared tau_neg for
    both loop types, which is wrong for the mixed-rectangle entries by one
    time-slice -- caught by review-finding's attack 12/unprompted item 4 on
    F335, fixed here)."""
    sites, _, _ = _site_masks(links['t'].shape[:4])
    vals = []
    for lab, _bk, _legs in BCC4_LOOPS:
        P = plaquette_4d(links, lab)
        tr = np.real(np.trace(P[:, :, :, tau], axis1=-2, axis2=-1)) / N
        vals.append(float(tr[sites[:, :, :, tau]].mean()))
    return np.array(vals)


def _mixed_reflection_observable_batch(links: dict, tau_rhombus: int,
                                       tau_mixed: int, N: int) -> np.ndarray:
    """Ten observables at the REFLECTED slice, with the rhombus entries read
    at `tau_rhombus` (the spatial mirror `Lt-1-tau_pos`) and the mixed-
    rectangle entries read at `tau_mixed` (the mixed mirror
    `(Lt-2-tau_pos) mod Lt`) -- the correct partner for each loop type per
    Sec. 2.1/2.2 of F335, not one shared index for both."""
    sites, _, _ = _site_masks(links['t'].shape[:4])
    vals = []
    for lab, bk, _legs in BCC4_LOOPS:
        tau = tau_rhombus if bk == 's' else tau_mixed
        P = plaquette_4d(links, lab)
        tr = np.real(np.trace(P[:, :, :, tau], axis1=-2, axis2=-1)) / N
        vals.append(float(tr[sites[:, :, :, tau]].mean()))
    return np.array(vals)


def reflection_positivity_gram_check(L: int, Lt: int, N: int, beta_s: float,
                                     beta_t: float, n_therm: int, n_sweeps: int,
                                     n_or: int, tau_pos: int, seed: int,
                                     sample_every: int = 4) -> dict:
    """Monte-Carlo estimate of the Gram matrix ``G_ij = <F_i(reflected)
    F_j(tau_pos)>`` over the ten local plaquette traces, plus its
    eigenvalues and a bootstrap error bar on the smallest one.

    The "negative"/reflected sample uses the CORRECT per-loop-type mirror
    slice: `Lt-1-tau_pos` for the 6 rhombus entries (spatial reflection, no
    dagger needed on a real trace), `(Lt-2-tau_pos) mod Lt` for the 4 mixed-
    rectangle entries (Sec. 2.2's cyclic-trace identity). These differ by
    one time-slice and using one shared index for both loop types -- an
    earlier version of this function did -- is wrong for the mixed entries.
    """
    shape4 = (L, L, L, Lt)
    gen = _rng.for_channel(f'F335_rp_gram_{seed}')
    links = hot_links_4d(shape4, N=N, channel=f'F335_rp_init_{seed}')
    thermalise_4d(links, beta_s, beta_t, n_therm, n_or=n_or,
                  channel=f'F335_rp_therm_{seed}')

    tau_neg_rhombus = (Lt - 1 - tau_pos) % Lt
    tau_neg_mixed = (Lt - 2 - tau_pos) % Lt
    samples_pos, samples_neg = [], []
    for i in range(n_sweeps):
        sweep_4d(links, beta_s, beta_t, gen, n_or=n_or)
        if i % sample_every == 0:
            samples_pos.append(local_plaquette_observable_batch(links, tau_pos, N))
            samples_neg.append(_mixed_reflection_observable_batch(
                links, tau_neg_rhombus, tau_neg_mixed, N))
    samples_pos = np.array(samples_pos)
    samples_neg = np.array(samples_neg)
    M = samples_pos.shape[0]

    G = samples_neg.T @ samples_pos / M
    G = 0.5 * (G + G.T)
    eigs = np.linalg.eigvalsh(G)

    rng2 = np.random.default_rng(12345 + seed)
    boot_mins = []
    for _ in range(200):
        idx = rng2.integers(0, M, size=M)
        Gb = samples_neg[idx].T @ samples_pos[idx] / M
        Gb = 0.5 * (Gb + Gb.T)
        boot_mins.append(np.linalg.eigvalsh(Gb)[0])
    boot_mins = np.array(boot_mins)

    return {
        'shape4': shape4, 'N': N, 'beta_s': beta_s, 'beta_t': beta_t,
        'n_sweeps_sampled': M, 'tau_pos': tau_pos,
        'tau_neg_rhombus': tau_neg_rhombus, 'tau_neg_mixed': tau_neg_mixed,
        'eigenvalues': eigs.tolist(), 'min_eig': float(eigs[0]),
        'max_eig': float(eigs[-1]),
        'min_eig_bootstrap_std': float(boot_mins.std()),
        'min_eig_bootstrap_mean': float(boot_mins.mean()),
    }


# ══════════════════════════════════════════════════════════════════════════
#  gate entry
# ══════════════════════════════════════════════════════════════════════════

def check_reflection_positivity_bcc(L: int = 4, Lt: int = 4, N: int = 2,
                                    gram_n_sweeps: int = 24,
                                    broken_dagger: bool = False) -> dict:
    """Fast, gate-tier bundle: the exact structural and identity checks plus
    a SMALL-statistics Gram smoke check (a handful of sweeps -- exercises the
    machinery, asserts nothing about the near-zero subleading eigenvalues,
    which need the heavier battery run in test-results/F335_* to resolve
    even approximately).

    ``broken_dagger=True`` is the declared control (see
    :func:`theta_reflect_config`): must redden ``M1`` (the mixed-rectangle
    trace identity) to O(1). ``I1`` (the involution check) stays green even
    under the control -- the bare time-index permutation is self-inverse
    regardless of the dagger, so it cannot see this particular bug; that is
    a measured fact about this control, not a flaw in the leg, and is why
    ``M1`` and not ``I1`` is the leg that actually certifies the dagger
    convention. ``H1``-``H4`` and ``S1`` do not touch theta and must stay
    green too.
    """
    shape4 = (L, L, L, Lt)
    checks = []

    def add(name, ok, value, note=""):
        checks.append({"name": name, "ok": bool(ok), "value": value, "note": note})

    hyp = loop_structure_reflection_hypotheses()
    add("H1", hyp["rhombus_dt_zero"], hyp["rhombus_dt_zero"],
        "every rhombus has zero net time component -- lies entirely within one time-slice")
    add("H2", hyp["mixed_two_temporal_linear"], hyp["mixed_two_temporal_linear"],
        "every mixed rectangle contains exactly two temporal-link legs, degree 1 each")
    add("H3", hyp["mixed_one_forward_one_reverse"], hyp["mixed_one_forward_one_reverse"],
        "the two temporal legs of a mixed rectangle are one forward, one reverse -- a "
        "single time-step crossing, not two")
    add("H4", hyp["only_nn_time_hop"] and hyp["n_rhombi"] == 6 and hyp["n_mixed"] == 4,
        {"only_nn_time_hop": hyp["only_nn_time_hop"], "n_rhombi": hyp["n_rhombi"],
         "n_mixed": hyp["n_mixed"]},
        "the only temporal hop is the nearest-neighbour +-t_hat, and the loop count is "
        "6 rhombi + 4 mixed rectangles -- the three OS-Seiler/Menotti-Pelissetto "
        "hypotheses this module exists to verify")

    i1 = reflection_involution_residual(shape4, N, broken_dagger=broken_dagger)
    add("I1", i1 < 1e-11, i1, "theta o theta == identity")

    m1 = mixed_plaquette_reflection_trace_residual(shape4, N, broken_dagger=broken_dagger)
    add("M1", m1 < 1e-11, m1,
        "Tr(theta P_mixed(tau)) == conj(Tr P_mixed(tau_mirror)) -- the cyclic-rotation "
        "trace identity that certifies the dagger convention")

    su2 = su2_character_positivity_residual()
    add("S1", su2["all_positive"], su2["min_coefficient"],
        "SU(2) Wilson character coefficients a_j(beta) > 0 for every sampled (beta, j), "
        "closed form a_j = I_2j(2 beta) - I_2j+2(2 beta) via Bessel recursion")

    gram = reflection_positivity_gram_check(
        L=L, Lt=Lt, N=N, beta_s=2.0, beta_t=8.0, n_therm=10,
        n_sweeps=gram_n_sweeps, n_or=1, tau_pos=1, seed=0, sample_every=2)
    add("G1", gram["max_eig"] > 0.0, gram["max_eig"],
        "the dominant (O_h-symmetric) Gram-matrix eigenvalue is positive at smoke "
        "statistics -- the sub-leading near-zero directions are NOT asserted here, "
        "see the battery record for the honest high-statistics reading")

    n_pass = sum(1 for c in checks if c["ok"])
    return {
        "checks": checks,
        "n_pass": n_pass,
        "n_total": len(checks),
        "verdict": "PASS" if n_pass == len(checks) else "FAIL",
        "hypotheses": hyp,
        "su2_positivity": su2,
        "gram_smoke": gram,
        "params": {"L": L, "Lt": Lt, "N": N, "gram_n_sweeps": gram_n_sweeps,
                   "broken_dagger": broken_dagger},
    }
