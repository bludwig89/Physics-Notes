"""F308 — the refold in ``lpt_selfenergy`` is repaired, and the audit found two
independent folds where F307 reported one.

Legs (all measured, none inferred from reading the code):

  R1  the repaired default equals F307's INDEPENDENT refold-free ``pi_loop`` — the
      whole content of "repaired" is that two code paths written from different
      actions now agree.
  R2  the fold fires iff Q >= pi/n, checked against a direct count of grid points
      leaving [-pi, pi) rather than against the formula that predicts it.
  R3  fp='exact' + kernel='wilson' is EXACTLY fold-invariant (the global-sign
      cancellation), which is why the defect was invisible on the published branch.
  R4  fp='leading' carries the LARGE fold (the sum-vs-difference mechanism) and
      kernel='rule' at fp='exact' carries a SMALL but nonzero one (the unperiodic
      propagator) — two mechanisms, not one.
  R5  K_true_4d has no axis-wise period at 2 pi, 4 pi or 8 pi, which is what makes
      the rule-branch fold illegal rather than merely inelegant.
  R6  the n=8 rows of the committed sweep are bit-unchanged by the repair.

Run:  casim test --id F308-refold-repaired
"""
from __future__ import annotations

# The entry point itself lives in the engine module (D9: a record names a
# ``module:`` and an ``entry:``; the test file is the pytest-collectable handle).
from casim.engine.gauge.lpt_selfenergy import (          # noqa: F401
    check_refold_repaired, TOL_AGREE, TOL_EXACT,
)

if __name__ == "__main__":  # pragma: no cover
    import json
    print(json.dumps(check_refold_repaired(), indent=1, default=str))
