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

Registry: the gate contract is the entry-driven record ``F308-refold-repaired``
(``module:``/``entry:``, no ``path:``); this file is its battery-tier companion,
scaffolded by ``tools/gen_test_registry.py``. Physics in
``casim.engine.gauge.lpt_selfenergy``.

Why this file has test functions at all (2026-08-19)
---------------------------------------------------
It used to be a bare import shim: two imports, a ``__main__`` block that printed
JSON, and nothing else. That made it the only file in ``tests/findings/`` with no
assert and no result artifact, i.e. UNFALSIFIABLE by ``tools/audit_tests.py`` —
and it could not have been fixed in place, because the gate record named both a
``path:`` and an ``entry:``, so ``tests/conftest.py`` hid the file from
collection and any test written here would have been dead code. Dropping
``path:`` from the gate record is the same repair F24 and F306 already carry, and
these functions now actually run.

Run:  casim test --id F308-refold-repaired    (the gate contract)
      pytest tests/findings/test_F308_refold_repaired.py
"""
from __future__ import annotations

from casim.engine.gauge.lpt_selfenergy import (
    check_refold_repaired, TOL_AGREE, TOL_EXACT,
)


def test_F308_all_legs():
    r = check_refold_repaired()
    assert r["passed"], r["checks"]
    assert r["n_pass"] == r["n_total"] == 6


def test_F308_R1_repaired_matches_the_independent_path():
    """The content of "repaired": two paths written from different actions agree."""
    leg = check_refold_repaired()["checks"]["R1_repaired_matches_F307_path"]
    assert leg["pass"], leg
    assert leg["max_abs_diff"] < TOL_AGREE


def test_F308_R2_fold_fires_iff_Q_ge_pi_over_n():
    """Counted against grid points leaving [-pi, pi), not against the formula."""
    leg = check_refold_repaired()["checks"]["R2_fires_iff_Q_ge_pi_over_n"]
    assert leg["pass"], leg
    assert leg["rows"] >= 24


def test_F308_R3_exact_wilson_is_fold_invariant():
    """Why the defect was invisible on the published branch."""
    leg = check_refold_repaired()["checks"]["R3_exact_wilson_fold_invariant"]
    assert leg["pass"], leg
    assert leg["max_abs_diff"] < TOL_EXACT


def test_F308_R4_two_mechanisms_not_one():
    """THE POINT OF THE AUDIT. F307 reported one fold; there are two, and they
    differ by more than an order of magnitude — so a single repair to the
    `leading` branch would have left the `rule`/`exact` one in place."""
    leg = check_refold_repaired()["checks"]["R4_two_distinct_mechanisms"]
    assert leg["pass"], leg
    assert leg["leading_defect"] > 10.0 * leg["rule_exact_defect"] > 0.0


def test_F308_R5_rule_kernel_has_no_axis_period():
    """What makes the rule-branch fold illegal rather than merely inelegant."""
    leg = check_refold_repaired()["checks"]["R5_rule_kernel_has_no_axis_period"]
    assert leg["pass"], leg
    assert leg["min_over_shifts_of_max_dev"] > 1.0


def test_F308_R6_committed_n8_rows_are_bit_unchanged():
    leg = check_refold_repaired()["checks"]["R6_inert_below_threshold"]
    assert leg["pass"], leg
    assert leg["n8_grid_never_leaves_cube"]


def test_F308_control_unrepairing_reddens_R1_and_only_R1():
    """THE CONTROL, as a test rather than as a sentence in `notes:`.

    Putting the fold back into the production default must break R1 — and must
    break *nothing else*, because R3/R4 compare refold=False against refold=True
    explicitly and so are blind to the default, and R6 runs below the Q >= pi/n
    threshold where the two are equal by construction. That measured set (R1
    alone, not the R1/R3/R6 the finding's first draft expected) is the record's
    declared `reds:`; this asserts it at the same time as the physics.
    """
    r = check_refold_repaired(unrepair_control=True)
    red = {k for k, v in r["checks"].items() if not v["pass"]}
    assert red == {"R1_repaired_matches_F307_path"}, red


if __name__ == "__main__":  # pragma: no cover
    import json
    print(json.dumps(check_refold_repaired(), indent=1, default=str))
