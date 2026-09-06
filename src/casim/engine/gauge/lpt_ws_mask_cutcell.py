"""lpt_ws_mask_cutcell.py -- an anti-aliased (cut-cell) Wigner-Seitz-cell mask
for the BCC gauge loop integral (F337's named next step).

WHY (F337 Sec.4/Sec.6 -> this module)
======================================
F337 ran the native n=28-40 sweep the ledger called for and found d1 leg 3
does NOT close: the two dLoops normalisations diverge instead of converging,
and the fitted convergence power on the BCC/rule side (~n^-1.1 to -1.35) is
far slower than the Wilson/cube side's own ~n^-2.8 (close to the assumed
1/n^2). F337 named a specific, checkable mechanism: ``lpt_bcc_vertex.ws_mask``
is a SHARP 0/1 indicator of Wigner-Seitz-cell membership, evaluated
POINTWISE at each grid cell's center. A hard boundary sampled this way is a
textbook source of O(1/n) "staircase" domain-integration error (boundary
cells contribute a full misclassified cell, and the number of boundary cells
scales as the surface-to-volume ratio, ~n^2 out of ~n^3) -- exactly the kind
of error the Wilson/cube side never has, because the cube already is its own
Brillouin zone and needs no domain mask at all.

WHAT THIS MODULE DOES
======================
Replaces the pointwise sharp indicator with the FRACTIONAL VOLUME of the WS
cell inside each grid voxel (a "cut-cell" or anti-aliased mask), computed by
adaptive octree refinement of the same half-space test ``lpt_bcc_vertex.ws_mask``
already uses (k.G <= |G|^2/2 for every reciprocal vector G within the first
shell -- see ``_shell1_planes`` below; VERIFIED to reproduce ``ws_mask``
exactly, i.e. the second shell in ``lpt_bcc_vertex._recip_vectors(rng=2)`` is
provably non-binding, see Sec.1).

METHOD -- exact-in-the-limit, not fixed-order supersampling
=============================================================
A first attempt at fixed-resolution supersampling (evaluate the sharp
indicator at Sx S x S sub-points per boundary voxel, average) was tried and
REJECTED: for constant sub-sample count S, the per-cell fractional-coverage
bias does not shrink with n, so the TOTAL domain-integral error stays
O(1/(n S)) -- still first order in n, just with a smaller constant. (Measured
directly: S=16 fixed supersampling reproduces the SAME log-log slope,
~-1.00, as the sharp mask, only ~16x smaller in magnitude -- Sec.2.)

The adopted method instead uses ADAPTIVE octree refinement per boundary
voxel: a voxel is classified, per half-space, as provably-fully-inside,
provably-fully-outside, or ambiguous, using an interval (Lipschitz) bound --
the maximum/minimum of k.G over the voxel is k0.G +/- (half_width * sum_i
|G_i|), an exact bound (not an approximation) since G is linear. Ambiguous
voxels are split into 8 octants and re-classified recursively; a voxel is
"resolved" fully-inside or fully-outside as soon as EITHER test fires for
ANY half-space (the "fully outside" test is per-plane and therefore itself
conservative -- see the honest-scope note in Sec.3 -- but the residual
converges rapidly under refinement regardless, since it is bounded by the
volume still ambiguous, which shrinks every level). This makes the returned
fraction converge toward the TRUE cut-cell volume fraction as depth_max
grows, with a bias controlled by depth_max ALONE, independent of the grid
resolution n -- unlike fixed supersampling. FIXED 2026-09-02, on adversarial review of the finding this module
supports (F350): an earlier version shared ONE node-count safety budget
across the WHOLE array of ambiguous voxels refined together. Since the
per-level cost scales with the array's OWN size, this made the depth
actually reached SHRINK as the array grew -- and more ambiguous voxels at
larger n is the normal case, so the bug made the mask get LESS accurate
exactly as n grew, the opposite of the design goal (measured before the
fix: effective depth fell from 6 at n=8 to 3 at n=40, even though the
AGGREGATE isolation error happened to stay flat regardless -- see Sec.2's
note on that near miss). Fixed by batching: ``_cutcell_fraction`` now
splits its input into batches sized so any ONE batch can run to the full
``depth_max`` within a fixed memory budget, and runs each batch to
completion independently -- so every voxel reaches the same depth_max,
and only the NUMBER of batches (not the depth any one reaches) grows with
the ambiguous-voxel count. Verified post-fix: the mask's output is
IDENTICAL regardless of the memory-budget parameter, at every n tested.
Measured (Sec.2, post-fix): at depth_max=5 the total WS-cell volume
estimate is accurate to ~4e-5-5e-4 (relative) and does NOT degrade with
n (n=40's error is in fact the smallest of the nine n tested) -- i.e.
this mask's own error floor is already below the ~n^-2.5-to-n^-2.8,
O(1/n^2)-class error the Wilson side itself carries at these n, so it
does not dominate the physics integral's error budget.

HONEST SCOPE
============
* The "fully outside" per-voxel test uses a SINGLE half-space's worst case
  across the whole voxel; a voxel that is fully outside via DIFFERENT
  half-spaces in different sub-regions (this happens near edges/vertices of
  the WS cell, where multiple faces meet) is not resolved by this test alone
  and is kept "ambiguous" until refined enough that some sub-voxel clears a
  single half-space on its own. This makes the test conservative (some truly
  resolved voxels are refined further than strictly necessary) but never
  WRONG -- a voxel this test calls fully-inside or fully-outside really is.
* This does not attempt an exact (e.g. polytope-clipping) per-cell volume.
  The octree residual (voxels still ambiguous when the node-count safety
  budget is hit) is assigned weight 0.5 of their own tiny remaining volume;
  Sec.2 measures the resulting bias directly rather than assuming it away.
* Only the first shell of ``lpt_bcc_vertex._recip_vectors`` (26 half-spaces)
  is used, VERIFIED (Sec.1, gate-tier) to reproduce ``ws_mask``'s boundary
  exactly at several n -- this is what keeps the octree numerically well
  behaved (the second shell's extra, non-binding half-spaces created
  spurious near-degenerate "ambiguous" classifications when included, an
  early version of this module measured and discarded).
* This module supplies the MASK only. Whether using it in the actual
  ``lpt_d1_action_consistent`` loop integral changes the measured
  convergence rate / extrapolated Lambda is Sec.5's job, in a separate
  module -- this file makes no claim about that on its own.
"""
from __future__ import annotations

import itertools
import math

from casim.numerics import xp
from casim.engine.gauge import lpt_bcc_vertex as bv

_PRIMITIVE = xp.array([[1, 1, 1], [1, 1, -1], [1, -1, 1]], dtype=float)


def _reciprocal_basis():
    return 2 * math.pi * xp.linalg.inv(_PRIMITIVE).T


def _shell1_planes():
    """The 26 first-shell reciprocal vectors (rng=1), and |G|^2/2 per plane."""
    B = _reciprocal_basis()
    G = xp.array([xp.array(n, dtype=float) @ B
                  for n in itertools.product(range(-1, 2), repeat=3)
                  if n != (0, 0, 0)])
    return G, 0.5 * xp.sum(G ** 2, axis=1)


_G1, _GHALF1 = _shell1_planes()
_GSUM1 = xp.sum(xp.abs(_G1), axis=1)

_OFFSETS = xp.array([[sx, sy, sz] for sx in (-1.0, 1.0)
                     for sy in (-1.0, 1.0) for sz in (-1.0, 1.0)])


def shell1_matches_ws_mask(n=16, tol=0.0) -> dict:
    """Gate G1 -- the first-shell-only half-space test reproduces
    ``lpt_bcc_vertex.ws_mask`` exactly (rng=2's second shell is non-binding).
    """
    ax = (xp.arange(n) + 0.5) / n * 2 * math.pi - math.pi
    X, Y, Z = xp.meshgrid(ax, ax, ax, indexing='ij')
    k3 = xp.stack([X, Y, Z], axis=-1).reshape(-1, 3)
    full = xp.asarray(bv.ws_mask(
        xp.concatenate([k3, xp.zeros((k3.shape[0], 1))], axis=-1)))
    shell1 = xp.all(k3 @ _G1.T <= _GHALF1 + 1e-12, axis=-1)
    n_mismatch = int(xp.sum(full != shell1))
    return {"n": n, "n_mismatch": n_mismatch, "n_total": int(k3.shape[0]),
            "pass": bool(n_mismatch == 0),
            "statement": "the first reciprocal shell (26 vectors) alone "
                         "reproduces ws_mask's boundary exactly"}


def _classify(k0, half_width):
    """-1 outside, 0 ambiguous, +1 inside, EXACT interval bound (not a
    numerical approximation): the max/min of k.G over an axis-aligned voxel
    of half-width ``half_width`` is k0.G +/- half_width*sum_i|G_i| exactly,
    since G is linear."""
    dot = k0 @ _G1.T
    slack = _GHALF1 - dot
    fully_inside = xp.all(slack - half_width * _GSUM1 >= 0, axis=-1)
    fully_outside = xp.any(slack + half_width * _GSUM1 < 0, axis=-1)
    out = xp.zeros(k0.shape[:-1], dtype=xp.int8)
    out[fully_inside] = 1
    out[fully_outside & ~fully_inside] = -1
    return out


def _cutcell_fraction_batch(centers, half_width, depth_max):
    """One batch's worth of octree refinement, run to the FULL depth_max --
    no early termination. Peak memory for a batch of size B is bounded by
    B * 8**depth_max in the worst case (every cell still ambiguous at the
    deepest level), which is why ``_cutcell_fraction`` below chooses B from
    ``depth_max`` rather than fixing a single global node cap (see Sec.2/7:
    a SHARED global cap was tried first and found, on review, to silently
    reach FEWER levels as the batch's own initial count grows -- exactly
    backwards, since more initial ambiguous cells at larger n is normal, not
    a sign more resource is available. Per-batch, depth-first-in-spirit
    processing fixes this: every batch reaches the same depth_max,
    independent of how many batches the full input needed)."""
    M = centers.shape[0]
    accum = xp.zeros(M)
    frontier_centers, frontier_hw, frontier_orig = centers, half_width, xp.arange(M)
    depth = 0
    while frontier_centers.shape[0] > 0 and depth < depth_max:
        child_hw = frontier_hw / 2.0
        weight_d = 1.0 / 8 ** (depth + 1)
        children = (frontier_centers[:, None, :]
                    + _OFFSETS[None, :, :] * child_hw).reshape(-1, 3)
        child_orig = xp.repeat(frontier_orig, 8)
        cls = _classify(children, child_hw)
        inside_mask = cls == 1
        xp.add.at(accum, child_orig[inside_mask], weight_d)
        amb_mask = cls == 0
        frontier_centers, frontier_orig, frontier_hw = (
            children[amb_mask], child_orig[amb_mask], child_hw)
        depth += 1
    if frontier_centers.shape[0] > 0:
        xp.add.at(accum, frontier_orig, 0.5 / 8 ** depth)
    return accum


def _cutcell_fraction(centers, half_width, depth_max=6, node_budget=2_000_000):
    """Adaptive octree refinement of the ambiguous voxels in ``centers``, to
    the FULL ``depth_max`` for every voxel (fixed 2026-09-02 on adversarial
    review of this finding: an earlier version shared one node budget across
    the WHOLE input array and broke out of the refinement loop early once
    that shared budget was exceeded -- since the loop's per-level cost scales
    with the CURRENT array size, this made the depth actually reached shrink
    as the input got bigger, exactly backwards (more ambiguous cells at
    larger n is the normal case, not a sign of less headroom). Fix: split
    ``centers`` into batches sized so a single batch can run
    ``_cutcell_fraction_batch`` to depth_max without exceeding
    ``node_budget`` in the worst case (every voxel in the batch still
    ambiguous at the deepest level) -- ``batch = max(1, node_budget //
    8**depth_max)`` -- and run each batch to completion independently. This
    guarantees depth_max is reached uniformly regardless of how many
    ambiguous voxels there are in total; only the NUMBER of batches (not the
    depth reached by any one of them) grows with n."""
    M = centers.shape[0]
    batch = max(1, node_budget // 8 ** depth_max)
    accum = xp.zeros(M)
    for i0 in range(0, M, batch):
        i1 = min(i0 + batch, M)
        accum[i0:i1] = _cutcell_fraction_batch(centers[i0:i1], half_width, depth_max)
    return accum


def bz_grid3(n):
    ax = (xp.arange(n) + 0.5) / n * 2 * math.pi - math.pi
    X, Y, Z = xp.meshgrid(ax, ax, ax, indexing='ij')
    return xp.stack([X, Y, Z], axis=-1)


def smoothed_ws_mask(n, depth_max=5, node_budget=4_000_000):
    """The anti-aliased WS-cell mask on the ``n``x``n``x``n`` spatial grid
    ``bz_grid3(n)`` uses -- shape (n, n, n), values in [0, 1]. Cells not
    touching the boundary keep the EXACT 0/1 value (proved, not measured,
    via ``_classify``'s interval bound); only boundary cells are refined, to
    the SAME ``depth_max`` regardless of how many boundary cells there are
    (see ``_cutcell_fraction``'s docstring for the batching fix this
    guarantee depends on)."""
    k3 = bz_grid3(n).reshape(-1, 3)
    h = (2 * math.pi / n) / 2.0
    cls = _classify(k3, h)
    w = xp.where(cls == 1, 1.0, 0.0)
    amb = cls == 0
    n_amb = int(xp.sum(amb))
    if n_amb:
        w[amb] = _cutcell_fraction(k3[amb], h, depth_max=depth_max, node_budget=node_budget)
    return w.reshape(n, n, n), n_amb


def mask_isolation_convergence(ns=(8, 12, 16, 20, 24, 28, 32, 36, 40),
                                depth_max=5) -> dict:
    """Gate G2 -- isolated (no loop-integral physics) test of the mask's own
    accuracy, against the EXACT target volume fraction V_WS/V_cube = 1/4
    (F305 G7: the cube holds exactly 4 copies of the BCC Brillouin zone).
    Reports both the sharp mask's error (expect ~n^-1, the F337-diagnosed
    staircase order) and this module's smoothed mask's error (expect much
    smaller and roughly FLAT in n, i.e. this mask's own floor is well below
    the target O(1/n^2) grid-discretisation scale for n in this range)."""
    target = 0.25
    rows = []
    for n in ns:
        ax = (xp.arange(n) + 0.5) / n * 2 * math.pi - math.pi
        X, Y, Z = xp.meshgrid(ax, ax, ax, indexing='ij')
        k3 = xp.stack([X, Y, Z], axis=-1).reshape(-1, 3)
        hard = float(xp.mean(xp.asarray(bv.ws_mask(
            xp.concatenate([k3, xp.zeros((k3.shape[0], 1))], axis=-1)), dtype=float)))
        smooth, n_amb = smoothed_ws_mask(n, depth_max=depth_max)
        est_smooth = float(xp.mean(smooth))
        rows.append({"n": n, "n_ambiguous": n_amb,
                     "hard_estimate": hard, "hard_err": abs(hard - target),
                     "smooth_estimate": est_smooth,
                     "smooth_err": abs(est_smooth - target)})
    logn = xp.log(xp.asarray([r["n"] for r in rows]))
    slope_hard = float(xp.polyfit(logn, xp.log(xp.asarray([r["hard_err"] for r in rows])), 1)[0])
    slope_smooth = float(xp.polyfit(logn, xp.log(xp.asarray([r["smooth_err"] for r in rows])), 1)[0])
    return {"rows": rows, "target": target,
            "slope_hard": slope_hard, "slope_smooth": slope_smooth,
            "pass": bool(max(r["smooth_err"] for r in rows) < 5e-3
                         and slope_hard < -0.7),
            "statement": "hard mask's own volume-estimate error falls as "
                         "~n^slope_hard (staircase, ~-1); the smoothed mask's "
                         "error is far smaller and does not need to fall "
                         "with n at all to already be sub-dominant to the "
                         "physics integral's own O(1/n^2) floor"}
