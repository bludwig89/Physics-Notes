"""F398 -- Pryce's 1938 composite-boson objection, tested against the F69/F169 paired photon.

The photon (F69) is a bound pair of two spin-1/2 Weyl quanta; F169 supplies its explicit
relative-momentum bound-state wavefunction psi(p) at total momentum k, marginally bound at
threshold. Pryce (1938) showed a composite built from two fermionic constituents cannot satisfy
EXACT canonical Bose commutation -- Pauli exclusion among the shared constituent modes forces
[a, a^dagger] to deviate from 1 whenever more than one composite quantum is built from
overlapping fermion modes. This module builds the model's own composite creation operator

    a_k^dagger = sum_p psi_k(p) b^dagger_{+, k/2+p} b^dagger_{-, k/2-p}

directly on a finite fermionic Fock space (exact antisymmetrised many-body construction, no
mean-field or bosonisation approximation), using F169's own threshold wavefunction psi_k(p)
(`casim.engine.gauge.photon_bound_state.threshold_wavefunction`), and measures how the
two-composite-photon norm deviates from the ideal-boson value as a function of momentum-grid
resolution L (the model's own BZ discretisation of the same, already-normalizable, continuum
wavefunction -- NOT a real-space volume/dilute-limit sweep).

Two results, both closed-form and both verified against an independent brute-force construction:

  IDENTITY (exact, any real normalised psi):
      ||(a_k^dagger)^2|0>||^2 = 2 (1 - sum_p psi(p)^4)

  the deficit from the ideal-boson value 2 is therefore controlled entirely by the wavefunction's
  inverse participation ratio, sum_p psi(p)^4.

  SCALING (derived from the grid structure of the F169 threshold wavefunction near its gapless
  p=0 singularity, verified numerically): sum_p psi(p)^2 is bulk-normalised (grows as L^3, the
  ordinary Riemann-sum-to-integral limit of the Watson-finite continuum norm), while
  sum_p psi(p)^4 is dominated by the handful of innermost non-zero grid points nearest p=0 (grows
  as L^4, since the continuum integral of psi^4 itself diverges at the gapless point and only the
  grid's own finite spacing regularises it).  The ratio therefore falls as ~L^-2, so Pauli
  blocking between two composite photons vanishes as the grid is refined toward the continuum
  threshold equation -- Pryce's objection does NOT obstruct approximate Bose statistics for this
  specific marginally-bound construction, in the fine-resolution limit.

  The grid carries real, disclosed non-monotonic commensurability noise (the same class of
  artifact F169's own C2/C4-note documents for the finite-k threshold): a SINGLE L value can land
  anomalously close to a spurious near-degenerate grid point and spike the measured deficit (or
  the raw bulk ratio) by 1-4 orders of magnitude, and this is frequent enough that most L values
  within a few units of any "clean" point are themselves contaminated (see the F398
  attack-and-fix review, `docs/reviews/F398-review-2026-09-23.md`, attack 12) -- a two-point
  comparison at one fixed (L_lo, L_hi) is fragile, not merely "occasionally noisy". The fix used
  here is `deficit_robust_min`/`bulk_robust_min`: since a resonance can only ADD spurious weight
  (it never removes the generic contribution), the MINIMUM over a small window of L around the
  target is a principled lower-envelope estimator, verified stable to <1% (bulk ratio) or a
  factor of ~2 (deficit ratio, still two orders of magnitude tighter than the raw single-point
  value) across every (L_lo, L_hi) pair in [8,13] x [95,105] tested in the review -- not just the
  specific pair used as the gate's parameters.

Only real linear algebra + closed-form dispersion is used, matching the rest of the photon
sector's own discipline (`photon_bound_state`, no scipy, own bisection where needed) -- this
module needs neither since everything here reduces to sums of psi**2/4 and a small, exact,
brute-force Fock-space construction on a handful of modes for the cross-check leg.
"""

from casim.numerics import xp
from casim.engine.gauge.photon_bound_state import threshold_wavefunction, relative_dispersion

ZERO_K = (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Exact, brute-force many-body Fock-space construction (small grids only).
#
# A Fock basis state is a frozenset of occupied GLOBAL mode indices; a
# Fock-space vector is a dict {frozenset: amplitude}.  Modes are ordered
# (+, p_0 .. p_{N-1}, -, p_0 .. p_{N-1}) -> global index 0..2N-1.  This is
# exact fermion sign bookkeeping (canonical Jordan-Wigner ordering), not a
# mean-field or number-conserving approximation.
# ---------------------------------------------------------------------------
def _apply_creation(state, mode_index):
    """c^dagger_{mode_index} applied to a Fock-space state dict; exact fermion sign."""
    out = {}
    for occ, amp in state.items():
        if mode_index in occ:
            continue                       # c^dagger^2 = 0 (Pauli exclusion)
        n_less = sum(1 for m in occ if m < mode_index)
        sign = -1.0 if (n_less % 2) else 1.0
        new_occ = occ | frozenset((mode_index,))
        out[new_occ] = out.get(new_occ, 0.0) + sign * amp
    return out


def _neg_index_map(L):
    """Grid index of -p (mod L per axis) for the periodic BZ grid p in [0, 2pi)."""
    idx = xp.arange(L)
    neg = (-idx) % L
    IX, IY, IZ = xp.meshgrid(idx, idx, idx, indexing="ij")
    neg_flat = (neg[IX] * L + neg[IY]) * L + neg[IZ]
    return neg_flat.ravel()


def _apply_a_dagger_fock(state, psi, L, pairing="conserving"):
    """Apply a_0^dagger = sum_p psi[p] b^dagger_{+,p} b^dagger_{-,partner(p)} to a Fock state.

    pairing="conserving" (physical): partner(p) = -p mod L  (total momentum 0, F169's own
        constituent assignment).
    pairing="shared" (declared negative control): partner(p) = 0 for every p -- every term
        shares the SAME '-' constituent mode, so different p terms are no longer built from
        disjoint fermion modes and the closed-form identity below must fail.
    """
    N = psi.size
    if pairing == "conserving":
        partner = _neg_index_map(L)
    elif pairing == "shared":
        partner = xp.zeros(N, dtype=int)
    else:
        raise ValueError("pairing must be 'conserving' or 'shared'")
    out = {}
    for pidx in range(N):
        w = float(psi[pidx])
        if w == 0.0:
            continue
        mplus, mminus = pidx, N + int(partner[pidx])
        tmp = _apply_creation(state, mminus)
        tmp2 = _apply_creation(tmp, mplus)
        for occ, amp in tmp2.items():
            out[occ] = out.get(occ, 0.0) + w * amp
    return out


def _norm2(state):
    return sum(a * a for a in state.values())


def fock_two_photon_norm(k, L, pairing="conserving"):
    """||a_k^dagger|0>||^2 (n1) and ||(a_k^dagger)^2|0>||^2 (n2), by exact brute-force
    many-body construction. Small L only (Fock-term count grows as ~L^6 in the worst case)."""
    psi, _T = threshold_wavefunction(k, L)
    vac = {frozenset(): 1.0}
    s1 = _apply_a_dagger_fock(vac, psi, L, pairing)
    n1 = _norm2(s1)
    s2 = _apply_a_dagger_fock(s1, psi, L, pairing)
    n2 = _norm2(s2)
    return n1, n2


# ---------------------------------------------------------------------------
# Closed forms (any grid size; psi real and normalised, sum psi**2 = 1).
# ---------------------------------------------------------------------------
def deficit_closed_form(psi):
    """sum_p psi(p)^4 -- the inverse participation ratio's reciprocal, and (per the module
    docstring identity) exactly half of the two-composite-photon norm deficit from the ideal-
    boson value 2."""
    return float(xp.sum(psi ** 4))


def two_photon_norm_closed_form(psi):
    """||(a_k^dagger)^2|0>||^2 = 2 (1 - sum_p psi(p)^4), the exact identity this module
    verifies against `fock_two_photon_norm` for small grids."""
    return 2.0 * (1.0 - deficit_closed_form(psi))


def bulk_normalization_ratio(k, L):
    """sum_p (1/(E0(p;k)-T))^2 / L^3 -- the RAW (unnormalised) wavefunction-squared sum divided
    by the grid volume L^3. Diagnostic only: this ratio is the robust, non-commensurability-
    sensitive quantity confirming sum psi^2 is bulk/continuum-dominated (Watson-finite), which is
    the OTHER half of the L^-2 scaling argument alongside the innermost-shell-dominated psi^4."""
    E = relative_dispersion(k, L)
    T = E.min()
    m = E > T + 1e-9
    u2 = 1.0 / (E[m] - T) ** 2
    return float(xp.sum(u2)) / L ** 3


def deficit_at(k, L, wavefunction="threshold"):
    """sum_p psi(p)^4 for the requested wavefunction shape, AT THIS EXACT L (raw point value,
    not resonance-robust -- see `deficit_robust_min` for the estimator the gate check actually
    uses).

    wavefunction="threshold" (physical, default): F169's own marginally-bound psi(p) = 1/(E0-T).
    wavefunction="uniform" (declared negative control): psi(p) = 1/sqrt(N) for every occupied
        grid point -- a generic normalised pair wavefunction with NO near-threshold singularity,
        for which sum psi^4 = 1/N ~ L^-3, a DIFFERENT (faster) decay than the physical L^-2 law.
    """
    if wavefunction == "threshold":
        psi, _T = threshold_wavefunction(k, L)
    elif wavefunction == "uniform":
        E = relative_dispersion(k, L)
        T = E.min()
        m = E > T + 1e-9
        psi = xp.zeros_like(E)
        psi[m] = 1.0
        psi /= xp.sqrt(xp.sum(psi ** 2))
    else:
        raise ValueError("wavefunction must be 'threshold' or 'uniform'")
    return deficit_closed_form(psi)


# ---------------------------------------------------------------------------
# Resonance-robust estimators.
#
# The F398 attack-and-fix review (docs/reviews/F398-review-2026-09-23.md) found that a SINGLE
# grid point L can land anomalously close to a spurious near-degenerate point in the BZ and
# spike sum_p psi(p)^4 (and the raw bulk ratio) by 1-4 orders of magnitude -- the same class of
# grid-commensurability artifact F169's own C2/C4-note documents for the finite-k threshold.
# The review's own neighbour scan showed a two-point comparison at fixed (L_lo, L_hi) is
# fragile: most L values within a few units of a "clean" point are themselves contaminated.
#
# The fix used here, not a wider tolerance band: since a resonance can only ADD spurious weight
# to a near-degenerate point (it never removes the generic, non-resonant contribution), the
# MINIMUM of psi(p)^4 (or the bulk ratio) over a small window of L values around the target is a
# principled lower-envelope estimator of the true, non-resonant trend -- verified directly
# (see the review) to be stable to <1% across every L in [8,13] x [95,105] tested, versus 1-2
# orders of magnitude of scatter for the raw single-L value over the same range.
# ---------------------------------------------------------------------------
def deficit_robust_min(k, L, wavefunction="threshold", half_window=4):
    """min over L' in [L-half_window, L+half_window] (L'>=2) of `deficit_at`.  Returns
    (min_value, {L': value, ...}) -- the per-L' scan is returned so the gate's own results JSON
    carries a fully auditable trail (F398 review attack 2's finding: no such trail existed for
    the original single-point L=10,100 check)."""
    scan = {}
    for d in range(-half_window, half_window + 1):
        Lp = L + d
        if Lp < 2:
            continue
        scan[Lp] = deficit_at(k, Lp, wavefunction=wavefunction)
    return min(scan.values()), scan


def bulk_robust_min(k, L, half_window=4):
    """Same lower-envelope estimator as `deficit_robust_min`, for `bulk_normalization_ratio`."""
    scan = {}
    for d in range(-half_window, half_window + 1):
        Lp = L + d
        if Lp < 2:
            continue
        scan[Lp] = bulk_normalization_ratio(k, Lp)
    return min(scan.values()), scan


# ---------------------------------------------------------------------------
# Gate entry point
# ---------------------------------------------------------------------------
def check_pryce_composite_commutator(fock_L=4, small_L=(3, 4), scaling_L=(10, 100),
                                      pairing="conserving", wavefunction="threshold",
                                      half_window=4):
    """F398 gate entry.

    Legs:
      single_photon_exact       -- <0|a a^dagger|0> = 1 exactly, any grid, any real normalised psi.
      closed_form_matches_fock  -- the n2 identity, verified against brute-force Fock construction
                                    at two independent small grid sizes (the project's own
                                    "two solve routes" discipline, cf. F74/F122).  The declared
                                    control is pairing="shared".
      deficit_shrinks_with_L    -- the resonance-robust (lower-envelope, see `deficit_robust_min`)
                                    deficit(L=10) / deficit(L=100) is consistent with the derived
                                    ~L^2 law, within a [20, 200] band verified stable across every
                                    (L_lo, L_hi) pair in [8,13] x [95,105] (module docstring / the
                                    F398 attack-and-fix review). The declared control is
                                    wavefunction="uniform" (L^-3 law, ratio ~410 with the same
                                    estimator, well outside the band).
      bulk_norm_is_L3           -- the same lower-envelope estimator applied to sum psi^2
                                    (unnormalised) / L^3, stable to <1% (confirms the Watson-
                                    finite bulk normalisation half of the scaling argument,
                                    independent of the psi^4 leg above).
    """
    checks, meas = {}, {}

    # -- single-photon norm: exact for ANY normalised real psi (no Pauli blocking on vacuum) --
    psi0, _T0 = threshold_wavefunction(ZERO_K, fock_L)
    n1_closed = float(xp.sum(psi0 ** 2))
    checks["single_photon_exact"] = bool(abs(n1_closed - 1.0) < 1e-12)
    meas["n1_closed"] = n1_closed

    # -- closed form vs. brute-force Fock construction, two independent grid sizes --
    worst = 0.0
    for L in small_L:
        psi, _T = threshold_wavefunction(ZERO_K, L)
        n1_fock, n2_fock = fock_two_photon_norm(ZERO_K, L, pairing=pairing)
        n2_closed = two_photon_norm_closed_form(psi)
        worst = max(worst, abs(n1_fock - 1.0), abs(n2_fock - n2_closed))
    checks["closed_form_matches_fock"] = bool(worst < 1e-10)
    meas["fock_vs_closed_worst_residual"] = worst

    # -- scaling: resonance-robust deficit(L_lo)/deficit(L_hi), ~L^2 suppression law --
    L_lo, L_hi = scaling_L
    d_lo, scan_lo = deficit_robust_min(ZERO_K, L_lo, wavefunction=wavefunction, half_window=half_window)
    d_hi, scan_hi = deficit_robust_min(ZERO_K, L_hi, wavefunction=wavefunction, half_window=half_window)
    ratio = d_lo / d_hi if d_hi > 0 else float("inf")
    checks["deficit_shrinks_with_L"] = bool(20.0 <= ratio <= 200.0)
    meas["deficit_lo"] = d_lo
    meas["deficit_hi"] = d_hi
    meas["deficit_ratio"] = ratio
    meas["deficit_scan_lo"] = scan_lo
    meas["deficit_scan_hi"] = scan_hi

    # -- bulk normalisation is O(1) x L^3, resonance-robust, stable (no control) --
    b_lo, bscan_lo = bulk_robust_min(ZERO_K, L_lo, half_window=half_window)
    b_hi, bscan_hi = bulk_robust_min(ZERO_K, L_hi, half_window=half_window)
    rel = abs(b_hi - b_lo) / b_lo if b_lo else float("inf")
    checks["bulk_norm_is_L3"] = bool(rel < 0.1)
    meas["bulk_ratio_lo"] = b_lo
    meas["bulk_ratio_hi"] = b_hi
    meas["bulk_ratio_relchange"] = rel
    meas["bulk_scan_lo"] = bscan_lo
    meas["bulk_scan_hi"] = bscan_hi

    return {"checks": checks, "all_pass": all(checks.values()), "measured": meas}


def _results_dir():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        cand = os.path.join(here, "test-results")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(here)
        if parent == here:
            raise RuntimeError("cannot locate test-results/ above " + __file__)
        here = parent


if __name__ == "__main__":
    import json
    import os

    result = check_pryce_composite_commutator()
    out = os.path.join(_results_dir(), "F398_pryce_composite_commutator.json")
    with open(out, "w") as f:
        json.dump({"finding": "F398", "module": "gauge.photon_pryce_commutator", **result},
                  f, indent=2)
    print(f"wrote {out}: all_pass={result['all_pass']}")
