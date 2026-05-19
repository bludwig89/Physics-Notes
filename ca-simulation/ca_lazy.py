"""
ca_lazy.py  —  Lazy-update / tick-counter wrapper for emergent-time work
=========================================================================
Implements Phase T1 of `ca-emergent-time-plan.md` (proposition file:
`ca-emergent-time-proposition.md`).

Two complementary tools live here:

  1. `TickCounter` — a per-cell int64 array recording how many times
     each cell has undergone a *nontrivial* state transition since
     initialization (the operational definition of N(x) in the
     proposition).

  2. `lazy_step(...)` — runs a v2 propagator step, then increments
     N(x) only at cells whose pre/post residual exceeds a threshold ε.
     For FFT-based steppers this is *bookkeeping-lazy*: the propagator
     still touches every cell (FFTs are global by construction), but
     the tick counter records the proper time of each cell honestly.

The wrapper is intentionally propagator-agnostic.  Callers pass a
"step function" that takes a state and returns the updated state plus
the per-cell pre/post fields used to compute the residual.

For the F-gate regression tests the residual is computed against the
*entire* per-cell state (all spinor / Φ / Π components), so a cell is
flagged as nontrivial if any of its components moved by more than ε.

The companion proposition file pins the threshold to the FFT round-off
floor (~1e-14).  The recommended default below is 1e-13 (one decade up
from the typical F1 vacuum drift residual) — change with the `eps`
keyword.

References
----------
- Plan:        ca-emergent-time-plan.md  (Phases T1.A, T1.B, T5.A, T5.B)
- Proposition: ca-emergent-time-proposition.md  (§4 threshold; §5 dep map)
"""

import time
import numpy as np


DEFAULT_EPS = 1.0e-13


# ══════════════════════════════════════════════════════════════════
#  TickCounter — per-cell N(x)
# ══════════════════════════════════════════════════════════════════

class TickCounter:
    """
    Per-cell tick counter N(x).  One int64 array of the lattice shape,
    incremented once per global step at cells whose state changed by
    more than ε in 2-norm across all components.

    Methods
    -------
    increment(mask)     : N[mask] += 1
    increment_from_residual(residual, eps) :
                           N[residual > eps] += 1
    reset()             : zero the counter
    proper_time(tau0)   : return N * tau0 (float array)
    occupied_fraction() : fraction of cells with N > 0
    """

    __slots__ = ('N', 'shape')

    def __init__(self, shape):
        self.shape = tuple(shape)
        self.N = np.zeros(self.shape, dtype=np.int64)

    def increment(self, mask):
        """In-place: N[mask] += 1.  `mask` is a bool array of self.shape."""
        if mask.shape != self.shape:
            raise ValueError(
                f"mask shape {mask.shape} != tick-counter shape {self.shape}")
        self.N += mask.astype(np.int64)

    def increment_from_residual(self, residual, eps=DEFAULT_EPS):
        """Convenience: build the bool mask from a real-valued residual."""
        self.increment(residual > eps)

    def reset(self):
        self.N.fill(0)

    def proper_time(self, tau0=1.0):
        """N(x) · τ_0.  Default τ_0 = 1 returns the tick count."""
        return self.N.astype(np.float64) * float(tau0)

    def occupied_fraction(self):
        """Fraction of cells that have ever been nontrivially updated."""
        if self.N.size == 0:
            return 0.0
        return float((self.N > 0).sum()) / float(self.N.size)

    def max_tick(self):
        return int(self.N.max()) if self.N.size > 0 else 0

    def mean_tick_on_support(self, support_mask):
        """Average N over a support mask (e.g. |ψ|² > threshold)."""
        if support_mask.shape != self.shape:
            raise ValueError("support mask shape mismatch")
        s = float(support_mask.sum())
        if s == 0.0:
            return 0.0
        return float((self.N * support_mask).sum()) / s


# ══════════════════════════════════════════════════════════════════
#  Residual helpers
# ══════════════════════════════════════════════════════════════════

def per_cell_residual_scalar(pre, post):
    """L2 per-cell residual for a single complex scalar field."""
    d = post - pre
    return np.abs(d)


def per_cell_residual_multi(pre_fields, post_fields):
    """
    L2 per-cell residual across multiple complex fields.

    pre_fields, post_fields : iterables of complex ndarrays, all same shape.

    Returns a real ndarray of that shape with
        r(x) = sqrt( sum_i |post_i(x) - pre_i(x)|^2 ).
    """
    pre_list  = list(pre_fields)
    post_list = list(post_fields)
    if len(pre_list) != len(post_list):
        raise ValueError("pre/post field count mismatch")
    if len(pre_list) == 0:
        raise ValueError("need at least one field")
    shape = pre_list[0].shape
    sq = np.zeros(shape, dtype=np.float64)
    for a, b in zip(pre_list, post_list):
        d = b - a
        sq = sq + (d.real * d.real + d.imag * d.imag)
    return np.sqrt(sq)


# ══════════════════════════════════════════════════════════════════
#  Lazy wrapper for arbitrary v2 propagator steps
# ══════════════════════════════════════════════════════════════════

def lazy_step(step_fn, state, tick_counter, eps=DEFAULT_EPS,
              extract_fields=None):
    """
    Bookkeeping-lazy wrapper.

    Runs `state = step_fn(state)`, then increments `tick_counter.N`
    at cells whose pre/post residual exceeds `eps`.

    Parameters
    ----------
    step_fn : callable(state) -> state_new
        Any propagator that consumes and returns the same state object
        (or returns a tuple matching the original shape — see the
        Weyl helper below for the tuple convention).
    state : the propagator's state (an UnifiedState, a (f, g) tuple,
        or a single complex array — caller-defined).
    tick_counter : TickCounter
    eps : float — nontriviality threshold.
    extract_fields : callable(state) -> list[ndarray]
        Pulls out the per-cell complex components used to compute the
        residual.  If None, assumes `state` is a single complex ndarray.

    Returns
    -------
    state_new — whatever step_fn returned.
    """
    if extract_fields is None:
        # default: state is a single complex ndarray
        pre = [state]
    else:
        pre = list(extract_fields(state))

    state_new = step_fn(state)

    if extract_fields is None:
        post = [state_new]
    else:
        post = list(extract_fields(state_new))

    residual = per_cell_residual_multi(pre, post)
    tick_counter.increment_from_residual(residual, eps=eps)
    return state_new


# ══════════════════════════════════════════════════════════════════
#  Convenience extractors for the v2 state types
# ══════════════════════════════════════════════════════════════════

def extract_weyl_2d(state):
    """state = (f, g)  — Weyl 2-spinor pair."""
    f, g = state
    return [f, g]


def extract_dirac_2d(state):
    """state = (eta_u, eta_d, chi_u, chi_d) — Dirac 4-spinor tuple."""
    return list(state)


def extract_unified(state):
    """state is an UnifiedState; pulls all six per-cell complex fields."""
    return [state.Phi, state.Pi,
            state.eta_u, state.eta_d,
            state.chi_u, state.chi_d]


# ══════════════════════════════════════════════════════════════════
#  Sync-vs-lazy regression utility
# ══════════════════════════════════════════════════════════════════

def sync_vs_lazy_residual(step_fn, state_init, n_steps,
                          eps=DEFAULT_EPS, extract_fields=None,
                          copier=None):
    """
    Run two copies of the same propagator for n_steps:
      - sync  : plain step_fn loop, no tick counting
      - lazy  : tick-counted wrapper (bookkeeping-lazy)

    Because lazy_step does NOT skip the propagator call (FFTs touch
    every cell), the two runs MUST be bit-for-bit identical.  This
    function verifies that and returns the max per-cell abs-difference
    summed across all extracted fields.

    Parameters
    ----------
    copier : callable(state) -> state
        How to deep-copy the propagator's state.  If None, uses
        `copy.deepcopy` (works for plain ndarrays and our UnifiedState
        thanks to its `.copy()` method).
    """
    import copy as _copy
    if copier is None:
        copier = lambda s: _copy.deepcopy(s)

    state_sync = copier(state_init)
    state_lazy = copier(state_init)
    shape = (extract_fields(state_lazy)[0].shape
             if extract_fields is not None
             else state_lazy.shape)
    tc = TickCounter(shape)

    for _ in range(n_steps):
        state_sync = step_fn(state_sync)
        state_lazy = lazy_step(step_fn, state_lazy, tc,
                               eps=eps, extract_fields=extract_fields)

    # Per-cell residual between the two runs
    pre  = (extract_fields(state_sync) if extract_fields else [state_sync])
    post = (extract_fields(state_lazy) if extract_fields else [state_lazy])
    diff = per_cell_residual_multi(pre, post)
    return float(np.max(diff)), tc, state_sync, state_lazy


# ══════════════════════════════════════════════════════════════════
#  Selected sub-step laziness (position-space only — T5.B)
# ══════════════════════════════════════════════════════════════════

def lazy_position_space_kick(field, kick_fn, eps=DEFAULT_EPS,
                              vacuum_mask=None):
    """
    Apply a position-space kick (e.g. Yukawa Π half-kick, KG nonlinear
    kick) only at cells outside the vacuum region.

    Parameters
    ----------
    field : complex ndarray (e.g. Π for the KG kick)
    kick_fn : callable(field_subset_view) -> field_subset_view_new
        Must broadcast across the masked subset.  In practice we wrap
        the cheap path: compute the full kick, then overwrite vacuum
        cells with their pre-kick values.  That avoids index gather/
        scatter overhead while still honouring the laziness contract.
    vacuum_mask : bool ndarray of field.shape
        True at cells whose state is vacuum (no kick applied).

    Returns
    -------
    field_new
    """
    field_new = kick_fn(field)
    if vacuum_mask is None:
        return field_new
    # Overwrite vacuum cells with their original values (no proper-time
    # advance, no state change).
    out = np.where(vacuum_mask, field, field_new)
    return out


# ══════════════════════════════════════════════════════════════════
#  Simple wall-clock timer for T5.B benchmark
# ══════════════════════════════════════════════════════════════════

def time_loop(step_fn, state, n_steps, copier=None):
    """Return wall-clock seconds for n_steps of step_fn applied to a copy."""
    import copy as _copy
    if copier is None:
        copier = lambda s: _copy.deepcopy(s)
    s = copier(state)
    t0 = time.perf_counter()
    for _ in range(n_steps):
        s = step_fn(s)
    return time.perf_counter() - t0


if __name__ == '__main__':
    # Quick smoke test: scalar field that updates trivially everywhere
    # except a central blob.  Verifies the residual mask is sane.
    L = 32
    np.random.seed(0)
    psi = np.zeros((L, L), dtype=complex)
    psi[L // 2, L // 2] = 1.0 + 0j  # one nonzero cell

    def trivial_step(p):
        # Identity update.  No cell should tick.
        return p.copy()

    tc = TickCounter((L, L))
    psi_new = lazy_step(trivial_step, psi, tc, eps=1e-15)
    print(f"trivial step → max N = {tc.max_tick()} (expect 0)")

    def hit_one_cell(p):
        q = p.copy()
        q[5, 5] += 0.1
        return q

    tc2 = TickCounter((L, L))
    psi2 = lazy_step(hit_one_cell, psi, tc2, eps=1e-15)
    print(f"single-cell step → max N = {tc2.max_tick()} (expect 1), "
          f"occupied frac = {tc2.occupied_fraction():.6f}")
