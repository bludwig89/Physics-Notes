"""F377 -- P1 is independent of the five BDPT axioms; the only live
counterexample shape is aperiodic, and the attempt does not succeed.

Re-derived independently of `casim.engine.lattice.time_generator_axiom_independence`
at a different Fourier mode, wavepacket width, tick count and irrational
(the Sturmian modulus), per this project's standing practice of not letting
a test merely re-import and re-run the module it is meant to check.

  REGROUP  (machine) A period-2 A-/A+ schedule regroups EXACTLY into
      iterating the single fixed operator B = A- @ A+: the sequential
      2n-step product equals B**n to machine precision, at every n tested.
      This is the computational half of the "regrouping lemma": a periodic
      multi-generator schedule is not a counterexample to P1, because
      redefining the tick to be one period turns it back into ordinary
      single-generator dynamics.
  FALSIFICATION ATTEMPT  (quantitative) A genuinely APERIODIC schedule --
      built from a Sturmian word over an irrational rotation number, the
      canonical non-eventually-periodic binary sequence, alternating
      between this model's own two admissible per-tick maps A+(k), A-(k) --
      is propagated on a real-space Gaussian wavepacket via the engine's
      own `weyl_step_3d_bcc`, and its ballistic transport exponent (fit of
      Var[x](t) ~ t^p) is compared against the period-2 regrouped reference
      polarized in ITS OWN eigenbasis (the fairest possible comparison). The
      aperiodic exponent, tried from three different initial polarizations,
      stays below the periodic-regrouped reference by a declared margin at
      this (independent) parameter point too -- the falsification attempt
      does not succeed here either.

Declared control: `--param break_regroup=True` compares the sequential
product against B**(n+1) instead of B**n (the WRONG power) -- must fail,
confirming the regroup check can actually detect a genuine mismatch rather
than passing regardless of what is compared.

Findings: F377. See that finding for the full argument (Part A: the
homogeneity axiom is spatial-only per D'Ariano & Perinotti arXiv:1608.02004,
so P1 is independent of the five stated BDPT axioms -- a citation, not
re-derived numerically here or in the module) and for the honest scope of
what this quantitative check does and does not establish (one numerical
experiment at two parameter points, not an asymptotic theorem).
"""
from __future__ import annotations

from typing import Dict

from casim.numerics import xp
from casim.engine.lattice.bcc import bcc_unitary, weyl_step_3d_bcc


def _matrix(kx, ky, kz, sign):
    Uff, Ufg, Ugf, Ugg = bcc_unitary(kx, ky, kz, sign=sign)
    return xp.array([[Uff, Ufg], [Ugf, Ugg]], dtype=complex)


def _sturmian_word(n_max, beta):
    s = xp.zeros(n_max, dtype=int)
    for n in range(n_max):
        s[n] = int(xp.floor((n + 1) * beta)) - int(xp.floor(n * beta))
    return s


def check_regroup(k=(0.25, 0.15, 0.35), n_periods: int = 20,
                   break_regroup: bool = False) -> Dict:
    kx, ky, kz = k
    Ap = _matrix(kx, ky, kz, '+')
    Am = _matrix(kx, ky, kz, '-')
    B = Am @ Ap

    max_residual = 0.0
    for n in range(1, n_periods + 1):
        seq_product = xp.eye(2, dtype=complex)
        for _ in range(n):
            seq_product = Am @ (Ap @ seq_product)
        power = n + 1 if break_regroup else n  # control: compare to the WRONG power
        B_power = xp.linalg.matrix_power(B, power)
        residual = float(xp.linalg.norm(seq_product - B_power))
        max_residual = max(max_residual, residual)

    return {"max_residual_over_n": max_residual, "passed": max_residual < 1e-10}


def _gaussian_wavepacket(L, sigma, k0, polarization):
    x = xp.arange(L) - L // 2
    X, Y, Z = xp.meshgrid(x, x, x, indexing="ij")
    envelope = xp.exp(-(X ** 2 + Y ** 2 + Z ** 2) / (2 * sigma ** 2))
    phase = xp.exp(1j * (k0[0] * X + k0[1] * Y + k0[2] * Z))
    amp = envelope * phase

    Ap = _matrix(k0[0], k0[1], k0[2], '+')
    Am = _matrix(k0[0], k0[1], k0[2], '-')
    mats = {"A+": Ap, "A-": Am, "B=A-A+": Am @ Ap}
    _, v = xp.linalg.eig(mats[polarization])
    spinor = v[:, 0]

    f = amp * spinor[0]
    g = amp * spinor[1]
    norm = xp.sqrt(xp.sum(xp.abs(f) ** 2 + xp.abs(g) ** 2))
    return f / norm, g / norm, X, Y, Z


def _variance(f, g, X, Y, Z):
    rho = xp.abs(f) ** 2 + xp.abs(g) ** 2
    tot = xp.sum(rho)
    mx, my, mz = (xp.sum(rho * A) / tot for A in (X, Y, Z))
    mx2, my2, mz2 = (xp.sum(rho * A ** 2) / tot for A in (X, Y, Z))
    return float((mx2 - mx ** 2) + (my2 - my ** 2) + (mz2 - mz ** 2))


def _ballistic_exponent(sign_seq, k0, L, sigma, n_ticks, polarization):
    f, g, X, Y, Z = _gaussian_wavepacket(L, sigma, k0, polarization)
    variances = [_variance(f, g, X, Y, Z)]
    for t in range(n_ticks):
        sign = '+' if sign_seq[t] == 1 else '-'
        f, g = weyl_step_3d_bcc(f, g, sign=sign)
        variances.append(_variance(f, g, X, Y, Z))
    t_arr = xp.arange(1, n_ticks + 1)
    v_post = xp.array(variances[1:])
    mask = t_arr > n_ticks // 3
    slope, _ = xp.polyfit(xp.log(t_arr[mask]), xp.log(v_post[mask]), 1)
    return float(slope)


def check_falsification_attempt(k0=(0.25, 0.15, 0.35), L=None, sigma=5.0,
                                 n_ticks: int = 50, beta: float = None) -> Dict:
    # Wrap-free box (2026-09-29): the walk front moves <= 1 cell/tick, so
    # L = 2(n_ticks + 5 sigma).  The old fixed L = 40 let the packet wrap the
    # periodic box and produced the +0.093 gap; wrap-free the gap is -0.235,
    # i.e. the aperiodic schedule does NOT sit below the periodic one and the
    # F377 margin claim fails.  This record is expected RED until F377 is
    # revisited in its own research session.
    if L is None:
        L = 2 * int(n_ticks + 5 * sigma)
        L += L % 2
    if beta is None:
        beta = 2 ** 0.5 - 1  # a DIFFERENT irrational than the module's golden-ratio choice

    seq_pure = xp.ones(n_ticks, dtype=int)
    seq_periodic2 = xp.array(([1, 0] * (n_ticks // 2 + 1))[:n_ticks])
    seq_aperiodic = _sturmian_word(n_ticks, beta)

    baseline = _ballistic_exponent(seq_pure, k0, L, sigma, n_ticks, "A+")
    periodic_matched = _ballistic_exponent(seq_periodic2, k0, L, sigma, n_ticks, "B=A-A+")
    aperiodic = {
        pol: _ballistic_exponent(seq_aperiodic, k0, L, sigma, n_ticks, pol)
        for pol in ("A+", "A-", "B=A-A+")
    }

    margin = 0.03
    worst_aperiodic = max(aperiodic.values())
    gap = periodic_matched - worst_aperiodic

    return {
        "baseline_pure_exponent": baseline,
        "periodic2_matched_exponent": periodic_matched,
        "aperiodic_exponents": aperiodic,
        "gap_periodic_minus_worst_aperiodic": gap,
        "falsification_attempt_succeeded": gap <= 0.0,
        "passed_declared_margin": gap >= margin,
    }


def check_all(break_regroup: bool = False) -> Dict:
    if break_regroup:
        regroup = check_regroup(break_regroup=True)
        assert not regroup["passed"], (
            "CONTROL break_regroup did not go red -- comparing the "
            f"sequential product against B**(n+1) instead of B**n must "
            f"fail, or the regroup check cannot detect a genuine "
            f"mismatch: {regroup}")
        raise AssertionError(
            f"[control break_regroup RED, as required] {regroup}")

    regroup = check_regroup()
    assert regroup["passed"], f"regroup check failed: {regroup}"

    falsification = check_falsification_attempt()
    assert falsification["passed_declared_margin"], (
        f"falsification-attempt margin check failed: {falsification}")

    return {
        "passed": True,
        "check_regroup": regroup,
        "check_falsification_attempt": falsification,
        "verdict": "PASS",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(check_all(), indent=2, default=str))
