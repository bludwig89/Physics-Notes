"""Reflection positivity for the BCC_3 x Z action -- human-readable driver.

This file defines no `test_*` functions deliberately: the CONTRACT is the
registry record `F335-reflection-positivity-bcc` (tier gate), which calls
`casim.engine.gauge.reflection_positivity.check_reflection_positivity_bcc`
directly via `entry:` -- `tests/conftest.py` hides entry-driven records from
file collection so nothing runs twice under two contracts (same pattern as
`test_bcc_gauge_mc_d4.py` for the confinement gate record).

    casim test --id F335-reflection-positivity-bcc
    casim test --id F335-reflection-positivity-bcc --param broken_dagger=true   # red on M1 only

THE LEGS (see reflection_positivity.check_reflection_positivity_bcc for the
full docstring of each):

  H1-H4  the three structural hypotheses the OS-Seiler/Menotti-Pelissetto
         link-reflection-positivity theorem needs: (a) rhombi have zero net
         time component, (b) mixed rectangles carry exactly two temporal
         legs entering linearly, (c) those two legs are one forward one
         reverse (a single time-step crossing), read directly off
         BCC4_LOOPS/_stored with no randomness.
  I1     theta o theta == identity (theta is an involution).
  M1     Tr(theta P_mixed(tau)) == conj(Tr P_mixed(tau_mirror)) exactly -- the
         cyclic-rotation trace identity; the ONE leg the broken_dagger
         control reddens (I1 cannot see that bug -- the bare index
         permutation is self-inverse regardless of the dagger; see the
         function's docstring for the four-line reason).
  S1     SU(2) Wilson character coefficients a_j(beta) > 0 for every sampled
         (beta, j) -- closed form via the Bessel recursion identity, an
         EXACT supplementary result not needed by the general H1-H4/I1/M1
         argument (Faizal, Ali & Alshal 2026, arXiv:2606.19362 Sec 2.1: the
         ordinary Wilson action's link-reflection-positivity does not need
         character-coefficient positivity at all), but a fully closed-form,
         independently checkable one for this sector.
  G1     the dominant (O_h-symmetric) eigenvalue of the reflection Gram
         matrix is positive at SMOKE statistics. The sub-leading near-zero
         directions are the honest residual of the numerical cross-check --
         see F335 Sec. 4 and the battery record `F335-reflection-positivity-gram`
         for the high-statistics reading, which does NOT resolve them and
         says so.

WHAT THIS DOES NOT CLOSE. This is a NECESSARY-ingredient result, not a
confinement proof: reflection positivity is what lets the Euclidean path
integral be reconstructed as a genuine Hilbert space with a self-adjoint
transfer matrix (Osterwalder-Schrader reconstruction) -- it does not by
itself supply a mass gap or an area law. Completeness row B7's residual
narrows from "no positivity machinery exists in the repo at all" to "the
positivity machinery exists and the model's own action satisfies it; a
strong-coupling / cluster-expansion argument on TOP of that transfer matrix
is the next step for an actual confinement proof." That next step is not
attempted here.
"""
