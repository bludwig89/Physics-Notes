"""lpt_d1_action_consistent.py — the F280 subtracted estimator run on ONE code
path with each side on its OWN action and its OWN Brillouin zone (F307).

WHAT THIS IS FOR
================
F280 formulated ``d_1`` as a difference against the Wilson
``Lambda_MSbar/Lambda_L = 28.8086`` anchor and reduced the open piece to one leg
of three: the rule's own 3-gluon + ghost vertex form factors, required to supply
``dC_vertex = -2.0160``.  Two things blocked filling that slot:

1. F287 sec.6 forbids reading an ABSOLUTE constant off the cubic quadrature.
   F280's answer is the slope-normalised estimator, exactly invariant under an
   overall measure factor.  This module reuses it verbatim
   (``lpt_d1_subtracted.slope_normalised_constant``).
2. F265: the rule's vertices are not Wilson's.  ``lpt_bcc_vertex`` (F305) now
   derives them from the genuine BCC rhombus.

So the estimator can finally be run action-consistently: vertices and propagator
from the SAME action on each side, each integrated over its own genuine
fundamental domain (the cube is the hypercubic BZ; the BCC BZ is the Wigner-Seitz
cell of the reciprocal lattice, one quarter of the cube).

    dLoops = C_hat(rule) - C_hat(wilson)

is then the FULL loops difference — propagator face and vertex face together —
which is the quantity F280's budget wants, not just its leg 2.

STATUS — the machinery is closed, the NUMBER IS NOT
===================================================
Run to n = 20 the estimator does not meet the project's own standard for quoting
a constant.  The diagnostic is ``b0_recovery`` (the measured log slope over the
analytic ``2 b0 / 16 pi^2``): the Wilson side sits at 1.11-1.14, the BCC side at
0.41-0.49 and still moving, and the slope-normalised and analytic-normalised
readings do NOT converge towards each other the way F280's leg 2 did.  A constant
read off that is a number with no error bar, which is the move F287 sec.6 exists
to prevent.  ``delta_loops`` therefore reports the series, both normalisations,
the b0 recoveries and the extrapolation, and ``check_action_consistent_d1``
FAILS its quoting leg by design until the recovery is near 1.

The Q window is bounded below by the F287 sec.5 resolution floor (>= 2 grid
cells) and above by the onset of O(Q^2) lattice contamination; on the BCC side
those two bounds have not yet opened far enough apart at n <= 20.  The remedy is
grid, not physics: a native sweep at n = 28-40.

WHAT THIS MODULE ALSO FOUND
===========================
``refold_defect`` demonstrates an F272/F277-class refold surviving in
``lpt_selfenergy._pi_bgfield``: it wraps the ghost and propagator momenta into
``[-pi, pi)`` while the vertex form factors, built from half-integer link-midpoint
shifts, have period ``4 pi``.  The wrap changes ``2 sin(k/2)`` by a sign.  The
transverse components are untouched; the LONGITUDINAL one is not.

NARROWED 2026-08-08: the reach is conditional, not universal.  On a midpoint grid
k+q leaves the cube only when Q > pi/n, and the wrap flips the sign of ONE
component of the ghost form factor -- to which a transverse projection built from
t_0^2 and t_1^2 is blind.  Measured at n=12, Q=0.3 (which does clear pi/12): the
wrapped and refold-free paths agree BITWISE.  So the defect bites only where the Q
window clears pi/n AND the observable is not quadratic in the flipped factor; it
does not contaminate `d1_selfenergy_sweep`.
"""
from __future__ import annotations

import math
from functools import lru_cache

from casim.numerics import xp
from casim.engine.gauge import lpt_bcc_vertex as bv
from casim.engine.gauge.lpt_d1_subtracted import (
    CELL_RATIOS, SLOPE_ANALYTIC, budget, lambda_from_dc,
    lambda_ratio_rule_target, slope_normalised_constant,
    F163_C_LAT_WILSON_LOOPS, C_MSBAR,
)

C_A = 3.0
SIXTEEN_PI2 = 16.0 * math.pi ** 2


def bz_grid(n):
    ax = (xp.arange(n) + 0.5) / n * 2 * math.pi - math.pi
    return xp.stack(xp.meshgrid(ax, ax, ax, ax, indexing='ij'), axis=-1)


def _T3grid(action, kgrid, qfix, which):
    N = bv.ACTIONS[action]["N"]
    out = xp.zeros(kgrid.shape[:-1] + (N, N, N), dtype=complex)
    a, b, c = ((kgrid, qfix, -kgrid - qfix) if which == 'W'
               else (kgrid + qfix, -qfix, -kgrid))
    for i in range(N):
        for j in range(N):
            for l in range(N):
                out[..., i, j, l] = bv.vertex3(action, (i, j, l), a, b, c)
    return out


def _Vgf(action, k, q):
    """background-covariant gauge-fixing vertex, axis space, bg convention [a,m,l]
    (F162/F163's ``V^gf`` with the hatted momentum generalised to khat_i)."""
    N = bv.ACTIONS[action]["N"]
    d = xp.eye(N)
    return (xp.einsum('am,...l->...aml', d, bv.khat(action, -k - q))
            - xp.einsum('ml,...a->...aml', d, bv.khat(action, k)))


def _domain_weight(k, domain, mask_grid=None):
    """The Pi_loop integration-domain weight. ``mask_grid`` (F337 Sec.4/6's
    named remedy, ``lpt_ws_mask_cutcell.smoothed_ws_mask``) is an (n,n,n)
    anti-aliased fractional-coverage array over the SPATIAL grid only; it is
    broadcast along the temporal axis (the mask does not depend on k_t) to
    match k's shape. ``mask_grid=None`` (the default, unchanged since F337)
    uses the sharp pointwise ``lpt_bcc_vertex.ws_mask`` instead."""
    if domain == "cube":
        return xp.ones(k.shape[:-1])
    if mask_grid is not None:
        return xp.broadcast_to(mask_grid[..., None], k.shape[:-1]).astype(float)
    return xp.asarray(bv.ws_mask(k), dtype=float)


def pi_loop(action, Q, n, branch="phys", domain=None, wrap_control: bool = False,
            mask_grid=None):
    """One-loop background-field Pi_{mn} in axis space, external q temporal.

    No momentum is refolded anywhere: the vertex form factors have period 4 pi
    and wrapping them into the cube is the F272/F277 defect (see
    ``refold_defect``). ``mask_grid`` overrides the WS-cell domain mask (see
    ``_domain_weight``); default ``None`` reproduces F337 exactly.
    """
    from casim.engine.core import lpt_generator as gen
    N = bv.ACTIONS[action]["N"]
    tax = bv.ACTIONS[action]["tax"]
    k = bz_grid(n)
    qv = xp.zeros(4)
    qv[3] = Q
    kq = k + qv
    if wrap_control:                  # the F272/F277 defect, re-introduced
        kq = ((kq + math.pi) % (2 * math.pi)) - math.pi
    istrip = 1j * gen.F_ABC[0, 1, 2]
    W = xp.real(_T3grid(action, k, qv, 'W') / istrip) + _Vgf(action, k, qv)
    Z = xp.real(_T3grid(action, k, qv, 'Z') / istrip) + _Vgf(action, kq, -qv)
    t = bv.khat(action, k) + bv.khat(action, kq)
    if action == "bcc" and branch == "phys":
        P = xp.eye(N) - xp.outer(bv.NHAT_BCC, bv.NHAT_BCC)
        W = xp.einsum('...aml,lb->...amb', W, P)
        Z = xp.einsum('...aml,ab->...bml', Z, P)
        t = t @ P
    M = xp.real(xp.einsum('...aml,...lna->...mn', W, Z)
                - 2.0 * xp.einsum('...m,...n->...mn', t, t))
    den = bv.quadratic_form(action, k) * bv.quadratic_form(action, kq)
    if domain is None:
        domain = "ws" if action == "bcc" else "cube"
    w = _domain_weight(k, domain, mask_grid=mask_grid)
    Pi = (C_A / 2.0) * xp.tensordot(w, M / den[..., None, None],
                                    axes=([0, 1, 2, 3], [0, 1, 2, 3])) / xp.sum(w)
    return Pi, tax


def transverse_B(action, Q, n, branch="phys", domain=None):
    """B = (Pi_LL - <Pi_TT>)/Q^2 with L the temporal axis."""
    Pi, tax = pi_loop(action, Q, n, branch, domain)
    trans = xp.mean(xp.asarray([Pi[i, i] for i in range(Pi.shape[0]) if i != tax]))
    return float((Pi[tax, tax] - trans) / Q ** 2)


def _side(action, Qs, n, branch="phys"):
    B = [transverse_B(action, Q, n, branch) for Q in Qs]
    x = [math.log(1.0 / Q) for Q in Qs]
    P = B if float(xp.polyfit(xp.asarray(x), xp.asarray(B), 1)[0]) > 0 else [-b for b in B]
    return (slope_normalised_constant(Qs, P),
            slope_normalised_constant(Qs, P, slope=SLOPE_ANALYTIC))


def delta_loops(ns=(12, 16, 20), b0_recovery_tol=0.15) -> dict:
    """Thin hashable-arg wrapper (registry params arrive as lists)."""
    return _delta_loops(tuple(ns), float(b0_recovery_tol))


@lru_cache(maxsize=None)
def _delta_loops(ns, b0_recovery_tol) -> dict:
    """dLoops = C_hat(rule) - C_hat(wilson), both slope-normalised, on a Q window
    that clears the F287 sec.5 resolution floor at every n.

    Reports both normalisations and the 1/n^2 extrapolation, AND the b0 recovery
    that says whether either may be quoted.  `quotable` is the gate.
    """
    rows = []
    for n in ns:
        sp = 2 * math.pi / n
        Qs = [r * sp for r in CELL_RATIOS]
        w_m, w_a = _side("sc", Qs, n)
        r_m, r_a = _side("bcc", Qs, n, "phys")
        a_m, _ = _side("bcc", Qs, n, "raw")
        rows.append({"n": n, "Qs": Qs,
                     "b0_recovery_wilson": w_m["b0_recovery"],
                     "b0_recovery_rule_phys": r_m["b0_recovery"],
                     "b0_recovery_rule_raw": a_m["b0_recovery"],
                     "dLoops_slope_normalised": r_m["C_hat"] - w_m["C_hat"],
                     "dLoops_analytic_normalised": r_a["C_hat"] - w_a["C_hat"]})

    def ext(key):
        v = [r[key] for r in rows]
        u = [1.0 / r["n"] ** 2 for r in rows]
        b, a = (float(t) for t in xp.polyfit(xp.asarray(u), xp.asarray(v), 1))
        return a, v

    a_m, v_m = ext("dLoops_slope_normalised")
    a_a, v_a = ext("dLoops_analytic_normalised")
    worst_rec = max(abs(r["b0_recovery_rule_phys"] - 1.0) for r in rows)
    worst_rec = max(worst_rec, max(abs(r["b0_recovery_wilson"] - 1.0) for r in rows))
    return {"ns": list(ns), "rows": rows,
            "series_slope_normalised": v_m, "limit_slope_normalised": a_m,
            "series_analytic_normalised": v_a, "limit_analytic_normalised": a_a,
            "dLoops": 0.5 * (a_m + a_a), "halfwidth": 0.5 * abs(a_m - a_a),
            "worst_b0_recovery_deviation": worst_rec,
            "quotable": bool(worst_rec < b0_recovery_tol),
            "statement": "dLoops is the FULL loops difference (propagator AND "
                         "vertex faces) on one code path, each side on its own "
                         "action and its own Brillouin zone. It is NOT quotable "
                         "until the b0 recovery is near 1 on both sides."}


def budget_with_full_dloops(dl: dict | None = None) -> dict:
    """Feed the measured full dLoops into F280's leg-2 slot.  The residual left
    in the leg-3 slot is then what the computation has NOT accounted for; a
    complete and converged measurement drives it to zero."""
    dl = dl or delta_loops()
    b = budget(dl["dLoops"], dl["halfwidth"])
    dC_rule = (F163_C_LAT_WILSON_LOOPS - C_MSBAR) - dl["dLoops"]
    b["fed_dLoops"] = dl["dLoops"]
    b["residual_in_leg3_slot"] = b["legs"][2]["dC"]
    b["implied_dC_rule_loops"] = dC_rule
    b["implied_lambda_rule"] = lambda_from_dc(dC_rule)
    b["lambda_rule_target"] = lambda_ratio_rule_target()
    b["quotable"] = dl["quotable"]
    b["note"] = ("the residual is meaningful only when dLoops is quotable; with "
                 "b0 recovery far from 1 it measures the grid, not the physics.")
    return b


@lru_cache(maxsize=None)
def _ls_pi_ll(Q, n, wrapped):
    """Pi_LL from the established lpt_selfenergy path, with its 2-pi refold left
    in or taken out.  Cached: it is the expensive brute-force generator and it is
    identical under this module's own `wrap_control`."""
    from casim.engine.gauge import lpt_selfenergy as ls
    # Post-repair `lpt_selfenergy` defaults to refold=False and exposes the fold as
    # an explicit switch, so this no longer monkeypatches the module's `_wrap`.
    # `wrapped=True` reproduces the pre-repair path exactly, which is what keeps
    # F307's demonstration of the defect reproducible after the repair.
    return float(xp.real(ls._pi_bgfield(Q, n, kernel='wilson', fp='leading',
                                        refold=wrapped))[0, 0])


@lru_cache(maxsize=None)
def refold_defect(n: int = 6, Qs=(0.8,), wrap_control: bool = False) -> dict:
    """An F272/F277-class refold surviving in ``lpt_selfenergy._pi_bgfield``.

    That module wraps the ghost/propagator momenta into ``[-pi, pi)``.  The
    propagator ``khat^2`` is 2-pi periodic so the wrap is harmless there, but the
    ghost form factor ``2 sin(k/2)`` has period 4 pi and the wrap flips its sign.
    Removing the wrap makes its longitudinal component agree with this module's
    refold-free path to round-off; the transverse components never disagreed,
    which is why the defect has been invisible.
    """
    rows = []
    for Q in Qs:
        wrapped = _ls_pi_ll(Q, n, True)
        unwrapped = _ls_pi_ll(Q, n, False)
        mine, _ = pi_loop("sc", Q, n, domain="cube", wrap_control=wrap_control)
        rows.append({"Q": Q, "lpt_selfenergy_wrapped": wrapped,
                     "lpt_selfenergy_unwrapped": unwrapped,
                     "refold_free_path": float(mine[3, 3]),
                     "unwrapped_matches": abs(unwrapped - float(mine[3, 3]))})
    return {"rows": rows,
            "max_mismatch_when_unwrapped": max(r["unwrapped_matches"] for r in rows),
            "defect_size": max(abs(r["lpt_selfenergy_wrapped"]
                                   - r["lpt_selfenergy_unwrapped"]) for r in rows),
            "pass": bool(max(r["unwrapped_matches"] for r in rows) < 1e-12
                         and max(abs(r["lpt_selfenergy_wrapped"]
                                     - r["lpt_selfenergy_unwrapped"])
                                 for r in rows) > 1e-3),
            "statement": "lpt_selfenergy._pi_bgfield refolds the ghost momenta by "
                         "2 pi while the vertex form factors have period 4 pi. "
                         "Longitudinal only, and the transverse projection "
                         "subtracts the longitudinal part, so it propagates."}


def check_action_consistent_d1(ns=(8, 10), b0_recovery_tol: float = 0.15,
                               wrap_control: bool = False) -> dict:
    """Registry entry point (D9).  Sweepable on `ns` and `b0_recovery_tol`.

    S1  the shared code path reproduces the established Wilson pipeline once the
        refold is removed (this is also the refold-defect demonstration)
    S2  dLoops runs end to end and returns finite numbers on both normalisations
    S3  the QUOTING leg: b0 recovery near 1 on both sides.  Expected RED today.
    """
    rf = refold_defect(wrap_control=bool(wrap_control))
    dl = delta_loops(tuple(ns), b0_recovery_tol)
    out = {"S1_refold_defect_demonstrated": rf,
           "S2_estimator_runs": {
               "dLoops": dl["dLoops"], "halfwidth": dl["halfwidth"],
               "series_slope_normalised": dl["series_slope_normalised"],
               "series_analytic_normalised": dl["series_analytic_normalised"],
               "pass": bool(all(math.isfinite(v)
                                for v in dl["series_slope_normalised"]
                                + dl["series_analytic_normalised"]))},
           "S3_quotable": {"worst_b0_recovery_deviation":
                           dl["worst_b0_recovery_deviation"],
                           "tol": b0_recovery_tol, "pass": dl["quotable"]},
           "budget": budget_with_full_dloops(dl)}
    out["checks"] = {k: bool(v["pass"]) for k, v in out.items()
                     if isinstance(v, dict) and "pass" in v}
    out["legs"] = dict(out["checks"])
    out["pass"] = (out["checks"]["S1_refold_defect_demonstrated"]
                   and out["checks"]["S2_estimator_runs"])
    return out



# ======================================================================
#  F337 -- L6 decision: which object is the propagator, and is the
#  redundant link-axis mode dynamical? Plus a memory-bounded evaluator so
#  the native sweep can reach n = 28-40 on a resource-constrained machine.
# ======================================================================
def pi_loop_chunked(action, Q, n, branch="phys", domain=None,
                     wrap_control: bool = False, chunk: int | None = None,
                     quadratic_form_fn=None, mask_grid=None):
    """Bit-identical reimplementation of ``pi_loop`` that streams over the
    first grid axis in slices of size ``chunk`` instead of building the full
    (n, n, n, n, N, N, N) tensor at once.  The unchunked path needs ~4 GB at
    n=32 and is OOM-killed by n=32 on a 4 GB machine (measured); this path
    peaks under 1 GB through n=40 with ``chunk`` picked by ``_chunk_for``.

    ``quadratic_form_fn(action, k)`` overrides ``bv.quadratic_form`` for this
    call only (used by ``propagator_scheme_divergence`` to swap in the F26/
    Omega_even kinetic form without monkeypatching the shared module state).
    Verified bit-identical to ``pi_loop`` at n=8 for both branches (max|diff|
    ~1e-16), 2026-08-30.
    """
    from casim.engine.core import lpt_generator as gen
    qf = quadratic_form_fn or bv.quadratic_form
    N = bv.ACTIONS[action]["N"]
    tax = bv.ACTIONS[action]["tax"]
    if domain is None:
        domain = "ws" if action == "bcc" else "cube"
    if chunk is None:
        chunk = _chunk_for(n)
    qv = xp.zeros(4)
    qv[3] = Q
    istrip = 1j * gen.F_ABC[0, 1, 2]
    ax1d = (xp.arange(n) + 0.5) / n * 2 * math.pi - math.pi

    Msum = xp.zeros((N, N), dtype=complex)
    wsum = 0.0
    for i0 in range(0, n, chunk):
        i1 = min(i0 + chunk, n)
        k0slice = ax1d[i0:i1]
        k = xp.stack(xp.meshgrid(k0slice, ax1d, ax1d, ax1d, indexing='ij'), axis=-1)
        kq = k + qv
        if wrap_control:
            kq = ((kq + math.pi) % (2 * math.pi)) - math.pi
        W = xp.real(_T3grid(action, k, qv, 'W') / istrip) + _Vgf(action, k, qv)
        Z = xp.real(_T3grid(action, k, qv, 'Z') / istrip) + _Vgf(action, kq, -qv)
        t = bv.khat(action, k) + bv.khat(action, kq)
        if action == "bcc" and branch == "phys":
            P = xp.eye(N) - xp.outer(bv.NHAT_BCC, bv.NHAT_BCC)
            W = xp.einsum('...aml,lb->...amb', W, P)
            Z = xp.einsum('...aml,ab->...bml', Z, P)
            t = t @ P
        M = xp.real(xp.einsum('...aml,...lna->...mn', W, Z)
                    - 2.0 * xp.einsum('...m,...n->...mn', t, t))
        den = qf(action, k) * qf(action, kq)
        mg_slice = mask_grid[i0:i1] if mask_grid is not None else None
        w = _domain_weight(k, domain, mask_grid=mg_slice)
        Msum = Msum + xp.tensordot(w, M / den[..., None, None],
                                   axes=([0, 1, 2, 3], [0, 1, 2, 3]))
        wsum += float(xp.sum(w))
    Pi = (C_A / 2.0) * Msum / wsum
    return Pi, tax


def _chunk_for(n: int, target: int = 131072) -> int:
    """Pick a first-axis chunk size so peak memory stays roughly constant
    (~1 GB) from n=28 through n=40: chunk * n^3 ~= target."""
    return max(1, round(target / n ** 3))


def transverse_B_chunked(action, Q, n, branch="phys", domain=None,
                         chunk: int | None = None, quadratic_form_fn=None,
                         mask_grid=None):
    Pi, tax = pi_loop_chunked(action, Q, n, branch, domain,
                              chunk=chunk, quadratic_form_fn=quadratic_form_fn,
                              mask_grid=mask_grid)
    trans = xp.mean(xp.asarray([Pi[i, i] for i in range(Pi.shape[0]) if i != tax]))
    return float(xp.real((Pi[tax, tax] - trans) / Q ** 2))


def _side_chunked(action, Qs, n, branch="phys", chunk: int | None = None,
                  quadratic_form_fn=None, mask_grid=None):
    """Chunked analogue of ``_side``, bit-identical output at shared n when
    ``mask_grid=None`` (default, unchanged since F337). ``mask_grid`` (F337
    Sec.4/6's named remedy) overrides the WS-cell domain mask -- see
    ``lpt_ws_mask_cutcell.smoothed_ws_mask``; has no effect for action='sc'
    (domain='cube', no mask)."""
    B = [transverse_B_chunked(action, Q, n, branch, chunk=chunk,
                              quadratic_form_fn=quadratic_form_fn,
                              mask_grid=mask_grid) for Q in Qs]
    x = [math.log(1.0 / Q) for Q in Qs]
    P = B if float(xp.polyfit(xp.asarray(x), xp.asarray(B), 1)[0]) > 0 else [-b for b in B]
    return (slope_normalised_constant(Qs, P),
            slope_normalised_constant(Qs, P, slope=SLOPE_ANALYTIC))


def _omega_even_quadratic_form(action, k):
    """L6 leg 1, the rejected candidate: the F26/Omega_even rotation-law
    propagator, generalised to 4D (F308's K_true_4d = 3 Omega_even^2 + kt^2),
    substituted for the rhombic action's own quadratic form on the BCC side
    only (the Wilson/'sc' reference is untouched in either scheme)."""
    from casim.engine.gauge import gluon_self_energy as se
    if action != "bcc":
        return bv.quadratic_form(action, k)
    kx, ky, kz, kt = k[..., 0], k[..., 1], k[..., 2], k[..., 3]
    return se.K_true_4d(kx, ky, kz, kt)


def propagator_scheme_divergence(ns=(6, 8, 10, 12), swap_control: bool = False) -> dict:
    """L6 leg 1, decided empirically (F305 Sec.7.4: 'the machinery is
    action-agnostic ... costs one function').  Runs the SAME rhombic
    vertices against two propagator choices -- the action's own quadratic
    form (default, action-consistent) and the F26/Omega_even K_true_4d
    (the alternative L6 names) -- and reports the b0-recovery trend for each.

    G_OWN must not get WORSE with n (its |1 - b0_recovery| trend should be
    non-increasing, matching the established slow monotonic approach); the
    swapped scheme must get WORSE (b0_recovery must diverge AWAY from 1,
    not toward it), because K_true_4d is aperiodic under the reciprocal
    lattice the rhombic vertices are exactly periodic under (F308 Sec.3),
    so pairing it with those vertices is not a lattice Feynman rule on this
    Brillouin zone at all.

    Control (D9): ``swap_control=True`` uses the OWN quadratic form for
    BOTH branches (the swap is a no-op), which must equalise the two
    sequences and kill the measured divergence gap.
    """
    own_fn = _omega_even_quadratic_form if swap_control else bv.quadratic_form
    swap_fn = bv.quadratic_form if swap_control else _omega_even_quadratic_form
    rows = []
    for n in ns:
        sp = 2 * math.pi / n
        Qs = [r * sp for r in CELL_RATIOS]
        own_m, _ = _side_chunked("bcc", Qs, n, "phys", quadratic_form_fn=own_fn)
        swap_m, _ = _side_chunked("bcc", Qs, n, "phys", quadratic_form_fn=swap_fn)
        rows.append({"n": n, "b0_recovery_own": own_m["b0_recovery"],
                     "b0_recovery_swapped": swap_m["b0_recovery"],
                     "dev_own": abs(own_m["b0_recovery"] - 1.0),
                     "dev_swapped": abs(swap_m["b0_recovery"] - 1.0)})
    dev_own = [r["dev_own"] for r in rows]
    dev_swap = [r["dev_swapped"] for r in rows]
    own_nonincreasing = all(dev_own[i + 1] <= dev_own[i] + 1e-9
                            for i in range(len(dev_own) - 1))
    swap_diverges = dev_swap[-1] > dev_swap[0]
    # No XOR here: under swap_control the two quadratic_form choices trade
    # places, so a genuine measurement naturally REDDENS this leg (the
    # diverging K_true_4d kernel now occupies the "own" slot) rather than
    # needing to be forced back to green -- that is the point of a D9
    # control, and it is what makes this leg falsifiable (make can-fail).
    return {"rows": rows, "own_dev_nonincreasing": own_nonincreasing,
            "swap_diverges": swap_diverges, "swap_control": swap_control,
            "pass": bool(own_nonincreasing and swap_diverges),
            "statement": "the rhombic vertices paired with the action's OWN "
                         "quadratic form converge monotonically; paired with "
                         "the F26/Omega_even K_true_4d they diverge, because "
                         "that kernel is not periodic on the vertices' own "
                         "reciprocal lattice (F308 Sec.3). Decides L6 leg 1."}


def branch_fork_native_sweep(ns=(28, 32, 36, 40), mask_kind="sharp",
                             mask_depth_max=5) -> dict:
    """L6 leg 2, the native n=28-40 sweep the ledger called for -- run with
    ``pi_loop_chunked`` so it fits in 4 GB.  Reports the extended b0-recovery
    trend for BOTH branches (phys/raw) and the full dLoops series.  This is
    a NATIVE, multi-minute computation (see ``tests/runners/run_l6_native_sweep.py``);
    it is committed as a result_dump artifact, not re-run at gate tier.

    ``mask_kind="sharp"`` (default) reproduces F337 exactly (the pointwise
    ``lpt_bcc_vertex.ws_mask``). ``mask_kind="smoothed"`` swaps in F337's
    named next step -- ``lpt_ws_mask_cutcell.smoothed_ws_mask``, the
    anti-aliased cut-cell mask -- for the BCC/'phys' and BCC/'raw' rows only
    (the Wilson/'sc' row never uses a mask, domain='cube')."""
    rows = {"phys": [], "raw": [], "sc": []}
    for n in ns:
        sp = 2 * math.pi / n
        Qs = [r * sp for r in CELL_RATIOS]
        mask_grid = None
        if mask_kind == "smoothed":
            from casim.engine.gauge import lpt_ws_mask_cutcell as wsm
            mask_grid, _ = wsm.smoothed_ws_mask(n, depth_max=mask_depth_max)
        elif mask_kind != "sharp":
            raise ValueError(f"unknown mask_kind {mask_kind!r}")
        w_m, w_a = _side_chunked("sc", Qs, n)
        rows["sc"].append({"n": n, **w_m})
        for branch in ("phys", "raw"):
            m, a = _side_chunked("bcc", Qs, n, branch, mask_grid=mask_grid)
            rows[branch].append({"n": n, "b0_recovery": m["b0_recovery"],
                                 "dLoops_slope": m["C_hat"] - w_m["C_hat"],
                                 "dLoops_analytic": a["C_hat"] - w_a["C_hat"]})
    return rows


def check_l6_decision(ns=(6, 8, 10, 12), swap_control: bool = False) -> dict:
    """Registry entry point (D9), gate tier, cheap.  Decides L6 leg 1
    empirically (``propagator_scheme_divergence``).  Leg 2 (is the redundant
    link-axis mode dynamical) rests on F305's own exact isometry gate
    (``lpt_bcc_vertex.mode_fork``, already gated there) PLUS the native
    n=28-40 sweep this record does not re-run at gate speed (see
    ``branch_fork_native_sweep`` / ``test-results/F337_l6_native_sweep.json``)."""
    prop = propagator_scheme_divergence(ns, swap_control=swap_control)
    out = {"L6_leg1_propagator_divergence": prop}
    out["checks"] = {k: bool(v["pass"]) for k, v in out.items()
                     if isinstance(v, dict) and "pass" in v}
    out["legs"] = dict(out["checks"])
    out["pass"] = all(out["checks"].values())
    return out


if __name__ == "__main__":  # pragma: no cover
    import json
    print(json.dumps(check_action_consistent_d1(), indent=1, default=str))
