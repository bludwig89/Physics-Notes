"""BCC 3+1D gauge Monte-Carlo: sampler + Wilson loops on the model's own lattice.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.bcc_action.check_bcc_gauge_mc` (record `gauge-bcc-mc-d4`,
tier gate), so this module deliberately defines no `test_*` functions --
`tests/conftest.py` hides entry-driven records from file collection so nothing
runs twice under two contracts.

    casim test --id gauge-bcc-mc-d4
    casim test --id gauge-bcc-mc-d4 --param include_mixed=false        # red
    casim test --id gauge-bcc-mc-d4 --param skip_checkerboard=true     # red
    casim test --id gauge-bcc-mc-d4 --param bad_reverse_shift=true     # red

WHAT THIS CLOSES.  `bcc_action.py` held the genuine BCC action since F265 but
had no sampler and no Wilson-loop observable, so every 3+1D confinement
statement in the tree (F94) was measured on a SIMPLE-HYPERCUBIC ensemble in
`forks/gauge/lgt_fork_A_mc.py` with the textbook Wilson action -- i.e. not on
the model's lattice at all.  This adds the missing engine.

WHAT THIS DOES NOT CLAIM.  No area law, no string tension, no confinement
verdict.  Those need production statistics and live in the battery record
`run-bcc-confinement-d4`; equilibrium validation (hot/cold hysteresis) is a
battery leg too, because it costs ~120 sweeps and the gate budget is <2 min.
No finding number is taken and no claim card is written.

GEOMETRY, and why it is not a 4D BCC.  The lattice is the BCC spatial graph
(4 <111> link axes) times an integer Euclidean time: 6 minimal 4-bond rhombi
(area 2 sqrt 2) plus 4 mixed space-time rectangles (area sqrt 3 a_t), ten
plaquettes per site rather than the hypercubic six.  A genuine 4D BCC/D4
lattice would make Euclidean time a fourth Cayley generator, which F291 S1
(space capped at 3) and F313 (the "+1" is the update's commutant, a commuting
flow and NOT another graph generator) both forbid.  The anisotropy
xi = a_s/a_t is NOT derived: beta_s and beta_t are independent arguments and
beta_t = beta_s is a convention, flagged in the module and here.

THE LEGS

  C1a  every one of the 10 loops is the identity on the ordered start
  C1b  the Wilson action vanishes identically at zero field strength
  C1c  the loop count is 10 = 6 rhombi + 4 mixed rectangles, not 6

  H1a  all 5 stored fields are in SU(N) on the disordered start
  H1b  every loop is a unitary holonomy, so the reversal identity closes

  G1a  all 10 plaquette traces are invariant under a random SU(N) gauge rotation
  G1b  every R x T Wilson loop is gauge invariant

  S1a  sum_links Re tr(U A) == 4 sum_loops beta Re tr P, isotropic couplings.
       THE load-bearing leg: every loop has four bonds, so summing Re tr(U A)
       over the five stored fields counts each plaquette exactly four times.
       It is the only check that the 40-slot enumeration, the reversal identity
       and the reversed-loop handling of backward hops are all correct
       TOGETHER, and a wrong staple fails it at O(1).
  S1b  the same identity with beta_t != beta_s -- anisotropy carried correctly
  S1c  exact bond counting, and the SPLIT not just the total: a spatial axis
       sits in 6 rhombi and 2 mixed rectangles, the time field in 8 mixed and
       no rhombus.  40 slots over 5 fields

  B1a  genuine BCC sites are 1/4 of the cubic array (index 4 in Z^3)
  B1b  every <111> hop maps the even class into the odd class.  This is the
       licence for a local heat-bath on a rhombic lattice at all: a rhombus
       with sides {a, e} carries two a-bonds stored one hop apart, and a
       bipartite nearest-neighbour graph puts them in opposite classes

  O1a  the microcanonical reflection R2 = (V2^dag)^2 leaves the action
       invariant.  Exact, and the sharpest test that the staple is dS/dU

  W1a  W(1,1) IS the mixed rectangle of the action -- the loop builder and the
       action are the same object, not two implementations that agree
  W1b  all R x T loops are 1 on the ordered start
  W1c  |Re tr W / N| <= 1 for every measured loop

  P1a  straight <111> walks preserve coordinate parity, so an R x T rectangle
       closes on the BCC site set for every R
  T1a  the staple construction is translation covariant

THE THREE CONTROLS REDDEN DIFFERENT LEG SETS, and the sets are MEASURED.

  include_mixed=false     -> S1a, S1b, O1a.  The staple drops the mixed
                             rectangles while the action keeps them, so it stops
                             being dS/dU and over-relaxation stops preserving S.
  skip_checkerboard=true  -> O1a only.  One colour class instead of four, so a
                             staple is reused for links that share a plaquette.
                             Clean and single-legged: the checkerboard's whole
                             job is the microcanonical identity.
  bad_reverse_shift=true  -> G1a, S1a, S1b, W1a.  The "- d" of
                             U_{-d}(x) = U_d(x-d)^dag is dropped.  Nothing
                             leaves SU(N), so H1a/H1b CANNOT see it -- that is
                             why gauge invariance is in this file.  G1b stays
                             GREEN, measured not expected: `_transporter` builds
                             R x T loops from forward hops only and daggers the
                             whole leg, so it never calls the corrupted path.
                             That asymmetry is also why W1a reddens -- the
                             action is corrupted and the loop is not, so the two
                             disagree.
"""

import json
import os
import sys


def _bootstrap():
    here = os.path.dirname(os.path.abspath(__file__))
    root = here
    for _ in range(6):
        root = os.path.dirname(root)
        if os.path.isdir(os.path.join(root, "src", "casim")):
            break
    src = os.path.join(root, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    return root


def _results_path(root, name):
    return os.path.join(root, "test-results", name)


def main():
    root = _bootstrap()
    from casim.engine.gauge.bcc_action import check_bcc_gauge_mc

    res = check_bcc_gauge_mc()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']:<5} "
              f"{c['value']}\n        {c['note']}")
    print(f"\n  {res['verdict']}: {res['n_pass']}/{res['n_total']}")

    out = _results_path(root, "bcc_gauge_mc_d4.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")
    return res


if __name__ == "__main__":
    _res = main()
    assert _res["n_pass"] == _res["n_total"], (
        f"{_res['n_total'] - _res['n_pass']} leg(s) red: "
        + ", ".join(c["name"] for c in _res["checks"] if not c["ok"])
    )
