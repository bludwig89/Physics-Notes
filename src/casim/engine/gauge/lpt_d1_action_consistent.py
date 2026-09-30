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


# ======================================================================
#  F382 -- d1 leg 3, next candidate after F350: does the vertex-derived
#  numerator M share the propagator's own periodicity under the BCC
#  reciprocal lattice (the group G7/F305 uses to justify the WS-cell as
#  THE fundamental domain), and if it does not, does integrating over the
#  full cube instead of the WS quarter fix (rather than worsen) the slow
#  convergence?
# ======================================================================
def _axis_kernel_at_point(action, k4, qv, branch="phys"):
    """M/den, the exact per-point integrand ``pi_loop`` sums (before the
    domain mask), evaluated at ONE 4-momentum.  Deliberately duplicated from
    ``pi_loop`` rather than factored out, matching this module's own house
    style (``pi_loop`` vs ``pi_loop_chunked``) so the tested production path
    is never touched by this diagnostic."""
    from casim.engine.core import lpt_generator as gen
    N = bv.ACTIONS[action]["N"]
    k = xp.asarray(k4, dtype=float).reshape(1, 4)
    kq = k + qv
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
    return M[0] / den[0]


#: fixed deterministic test points, spatial (kx,ky,kz) + temporal kt, chosen
#: generic (irrational-ratio, no accidental symmetry) so the periodicity
#: measurement below is reproducible without depending on an RNG stream.
_G382_POINTS = (
    (0.37, -0.52, 0.61, 0.28), (-0.44, 0.19, -0.33, 0.55),
    (0.58, 0.41, -0.17, -0.36), (-0.22, -0.63, 0.48, 0.14),
)


def vertex_g_periodicity(branch: str = "phys", control_use_propagator: bool = False,
                         shell_size: int = 6) -> dict:
    """Does the axis-space kernel M (numerator of ``pi_loop``'s integrand)
    share the propagator's own exact invariance (G7, F305) under a shift of
    the loop momentum by a BCC reciprocal-lattice vector?  G7 establishes
    this ONLY for the quadratic form (the propagator sector); F305/F280/F337
    all use the WS cell (one quarter of the cube) as THE fundamental domain
    for the FULL loop integral, vertex and propagator together, on the
    strength of that same G7 argument.  This checks whether the argument
    actually extends to the vertex-derived numerator, which G7 never claimed.

    ``control_use_propagator=True`` runs the identical measurement on
    ``bv.quadratic_form`` alone instead of the M-kernel -- the propagator
    sector G7 already proves invariant -- so the check can register the
    opposite (small-deviation) verdict under a real toggle, not just always
    report "violated" (D9)."""
    qv = xp.zeros(4)
    qv[3] = 0.9
    G = bv._recip_vectors(rng=1)[:shell_size]
    rows = []
    for k4 in _G382_POINTS:
        k = xp.asarray(k4)
        if control_use_propagator:
            base = float(bv.quadratic_form("bcc", k.reshape(1, 4))[0])
        else:
            base = _axis_kernel_at_point("bcc", k, qv, branch)
        for g3 in G:
            kshift = k.copy()
            kshift[:3] = kshift[:3] + g3
            if control_use_propagator:
                shifted = float(bv.quadratic_form("bcc", kshift.reshape(1, 4))[0])
                dev = abs(shifted - base) / max(abs(base), 1e-300)
            else:
                shifted = _axis_kernel_at_point("bcc", kshift, qv, branch)
                denom = max(float(xp.max(xp.abs(base))), 1e-300)
                dev = float(xp.max(xp.abs(shifted - base))) / denom
            rows.append({"k": k4, "|G|": float(xp.linalg.norm(g3)), "rel_dev": dev})
    worst = max(r["rel_dev"] for r in rows)
    return {"rows": rows, "worst_rel_dev": worst,
            "control_use_propagator": control_use_propagator,
            "pass": bool(worst < 1e-8 if control_use_propagator else worst > 0.05),
            "statement": "the propagator's exact invariance under the BCC "
                         "reciprocal lattice (G7) does not extend to the "
                         "vertex-derived numerator M -- the same shift that "
                         "leaves quadratic_form invariant to machine "
                         "precision changes M by tens of percent."}


def domain_choice_divergence(ns=(6, 8, 10, 12, 14, 16, 18, 20), branch: str = "phys",
                             swap_control: bool = False) -> dict:
    """Does summing the loop over the FULL cube (rather than G7's WS quarter)
    fix d1 leg 3's anomalously slow convergence (F337/F350), on the theory
    that ``vertex_g_periodicity`` above shows the WS restriction may be
    dropping vertex contributions the propagator sector alone does not need
    dropped?  Tested directly rather than argued: if the cube captures
    vertex information the WS cell wrongly discards, ``b0_recovery`` under
    ``domain='cube'`` should approach 1 at least as well as ``domain='ws'``.

    ``bad_diverges`` is a MONOTONICITY test on ``b0_recovery`` itself (not on
    ``|1 - b0_recovery|``): the deviation-from-1 metric is non-monotonic near
    a sign crossing (``b0_recovery`` passing through exactly 1), which the
    'cube' domain does between n=8 and n=10 (F382 review, 2026-09-10 -- an
    endpoint-only deviation comparison over a range starting at n=8 missed
    this and gave a false 'converges' reading at ns=(6,8,10)).
    ``b0_recovery`` itself is strictly increasing at every consecutive n from
    6 through 20 for BOTH branches under domain='cube' (verified directly,
    no crossing-induced ambiguity), which is what a genuine, unbounded
    divergence looks like; requiring that plus a healthy final margin past 1
    is robust to which sub-range of n happens to be swept.

    ``swap_control=True`` swaps which domain is asserted to behave well --
    a real measurement (not a hardcoded verdict) must fail under the swap,
    because it is ``domain='cube'`` that actually diverges (D9)."""
    good_domain, bad_domain = ("cube", "ws") if swap_control else ("ws", "cube")
    rows = []
    for n in ns:
        sp = 2 * math.pi / n
        Qs = [r * sp for r in CELL_RATIOS]
        good_m, _ = _side_domain(good_domain, Qs, n, branch)
        bad_m, _ = _side_domain(bad_domain, Qs, n, branch)
        rows.append({"n": n, f"b0_recovery_{good_domain}": good_m["b0_recovery"],
                     f"b0_recovery_{bad_domain}": bad_m["b0_recovery"],
                     "dev_good": abs(good_m["b0_recovery"] - 1.0),
                     "dev_bad": abs(bad_m["b0_recovery"] - 1.0)})
    dev_good = [r["dev_good"] for r in rows]
    bad_seq = [r[f"b0_recovery_{bad_domain}"] for r in rows]
    good_bounded = max(dev_good) < 1.0            # ws never leaves the [0,2) band, at ANY n tested
    bad_monotonic = all(bad_seq[i + 1] > bad_seq[i] for i in range(len(bad_seq) - 1))
    bad_diverges = bad_monotonic and bad_seq[-1] > 1.5
    return {"rows": rows, "good_domain": good_domain, "bad_domain": bad_domain,
            "good_bounded": good_bounded, "bad_diverges": bad_diverges,
            "swap_control": swap_control,
            "pass": bool(good_bounded and bad_diverges),
            "statement": "domain='cube' does not fix d1 leg 3's slow "
                         "convergence -- its own b0_recovery climbs "
                         "strictly monotonically past 1 without turning "
                         "over (both phys and raw branches, n=6-20), the "
                         "same qualitative signature F337 measured for the "
                         "raw (unprojected) branch under domain='ws'. This "
                         "corroborates the WS-cell restriction G7 (F305) "
                         "already licenses for the propagator sector; it "
                         "does not itself re-decide L6 (F337), whose two "
                         "litigated legs were the propagator scheme and the "
                         "branch fork, not the domain choice."}


def _side_domain(domain, Qs, n, branch):
    """``_side_chunked``, but with an explicit forced integration domain
    (F382) rather than the action's default.  ``action`` is always 'bcc' --
    the Wilson/'sc' side has no WS cell and is not part of this question."""
    B = [transverse_B_chunked("bcc", Q, n, branch, domain=domain) for Q in Qs]
    x = [math.log(1.0 / Q) for Q in Qs]
    P = B if float(xp.polyfit(xp.asarray(x), xp.asarray(B), 1)[0]) > 0 else [-b for b in B]
    return (slope_normalised_constant(Qs, P),
            slope_normalised_constant(Qs, P, slope=SLOPE_ANALYTIC))


def check_d1_vertex_domain_f382(ns=(6, 8, 10, 12, 14, 16, 18, 20),
                                swap_control: bool = False) -> dict:
    """Registry entry point (D9), gate tier.  F350 Sec.5/7 named two untested
    candidates for d1 leg 3's anomalous convergence rate after the WS-mask
    discretisation hypothesis was excluded: the vertex form factors' own
    behaviour / the phys-branch projection, and the g_s=1/2 monotonicity
    assumption.  This record attacks the first, in the sharpest form
    available: does the WS-cell domain (correct for the propagator by G7,
    but never shown correct for the vertex-derived numerator) actually
    account for the vertex sector too?  ``vertex_g_periodicity`` measures
    that the propagator's invariance does NOT extend to the vertex kernel;
    ``domain_choice_divergence`` then tests the natural remedy (integrate
    over the full cube instead) directly and finds it makes convergence
    WORSE, not better -- ruling this candidate out rather than confirming
    it, and corroborating (not re-deciding -- see ``domain_choice_divergence``'s
    own docstring) the WS-cell restriction F337's L6 decision (domain='ws',
    branch='phys') already rests on.

    FALSIFIABILITY (added on review, 2026-09-10): this record's own exclusion
    of the domain-choice candidate is overturned if a future sweep at n > 20
    measures ``domain='cube'``'s b0_recovery turning over (ceasing to
    increase monotonically) and settling below ``domain='ws'``'s own
    deviation from 1 -- no such turnover has been measured across n=6-20
    for either branch (strictly monotonic throughout, verified directly)."""
    pg = vertex_g_periodicity()
    pg_ctrl = vertex_g_periodicity(control_use_propagator=True)
    dd = domain_choice_divergence(ns, swap_control=swap_control)
    out = {"vertex_not_G_periodic": pg,
           "propagator_is_G_periodic_control": pg_ctrl,
           "cube_domain_does_not_fix_it": dd}
    out["checks"] = {k: bool(v["pass"]) for k, v in out.items()
                     if isinstance(v, dict) and "pass" in v}
    out["legs"] = dict(out["checks"])
    out["pass"] = all(out["checks"].values())
    return out


if __name__ == "__main__":  # pragma: no cover
    import json
    print(json.dumps(check_action_consistent_d1(), indent=1, default=str))
