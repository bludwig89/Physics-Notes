"""F325 — X1 resolved: branch A tested and closed, branch B adopted.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_x1_branch.check_x1_branch` (record `F325-x1-branch`,
tier gate), so this module deliberately defines no `test_*` functions --
`tests/conftest.py` hides entry-driven records from file collection so nothing
runs twice under two contracts.

    casim test --id F325-x1-branch
    casim test --id F325-x1-branch --param magnetic_scale=2.0   # must go red (X2)
    casim test --id F325-x1-branch --param su3_cut=2            # must go red (X2)

WHAT THIS SETTLES.  X1 (`docs/status/open-derivations.md` Part D) recorded a
fork the tree could not choose between and named a d_1 computation as the
decider.  It does not need d_1.  Branch A is closed two ways, and the two are
independent of each other:

  STRUCTURAL   F298's C_F comes from evaluating the C7 identity with the
               ABELIAN rotor's s(k)^2 against the SU(N) gauge theory's C_2(R_k).
               Under either self-consistent evaluation chi = 1/(4 g^2) for every
               N and every irrep -- leg L6 of `F298-casimir-ladder`, added with
               the operator control the record had been missing.
  QUANTITATIVE branch A needs Lambda_MSbar/Lambda_rule = 3.4e6, which is 5.63
               decades outside F280/CL252's committed [1, 7.98] -- leg N8 of
               `F303-coupling-normalisation`.

This record carries the THIRD leg, which no module held: the MAGNETIC side of
C7, named as X1's residual by the companion report and closed here negatively.

  X1   the magnetic term is -(lam/2) x (unit-entry adjacency + transpose) in
       BOTH theories -- U(1)'s cos(phi) shift and SU(N)'s fundamental fusion,
       which is multiplicity-free -- so the magnetic coefficient is lam in both
       and it adds NO factor to the chi-map.  C7 survives a full electric +
       magnetic audit against a genuine SU(N) link Hamiltonian.
  X2   at EQUAL n_links, s1_SU(N)/s1_U(1) -> 2/(N^2-1) as lam -> 0, independent
       of n, with the residual vanishing at least linearly in lam (measured:
       O(lam) at N=3, O(lam^2) at N>=4).  Setting the ratio to 1 needs N^2 = 3,
       so there is NO N_c selector in it.
  X3   DEFECT RECORDED.  F111b T7 reproduces (dev ~1.1e-3 against its own 5e-3
       tolerance) but compares a ONE-link SU(3) rotor against a FOUR-link U(1)
       one; the electric gaps differ by exactly n/C_F = 3.  Its agreement at
       N=3 is C_F d_F = (N^2-1)/2 = 4 coinciding with the four links, not a
       statement about the group.  T7 is therefore NOT independent confirmation
       of chi = 1/(4 g^2), and must not be quoted as one.
  X4   NEW AND EXACT.  sigma_1 carries a constant offset ln((N^2-1)/2) = ln 4 =
       1.386294 nats between the implemented Z_3/U(1) engine and the SU(3) one.
       That is a correction to F99/F100/F101, and it is orthogonal to g_s.
  X5   GAP RECORDED IN F144.  The circularity lemma's residual vanishes at a=b
       for EVERY b, so a = b = Omega(k) and chi = 1/Omega(k): chi = 1 requires
       Omega = 1, which the lemma does not supply.  chi = 1 is F101 section 7's
       normalisation, inherited rather than derived -- the SAME choice as the
       integer spectrum.  This does NOT restore branch A, whose chi = 3/4
       (Omega = 4/3) is not derived either.
  X6   branch A closed on both legs.
  X7   branch B adopted, inside the model's own Lambda bracket at 11%.

WHAT IT DOES NOT SETTLE.  Which Omega the single-plaquette rotor carries, on
the BCC dispersion (X5) -- that is X1's residual after this finding, and it is
plausibly the same object as F155's matching scale q_*.  And d_1 is unchanged
in method: it now PINS alpha_s inside branch B rather than choosing a branch,
and a completed vertex computation returning 3.4e6 would reinstate branch A.

COST.  CN19 falls, and F324's upper constraint with it -- see the finding.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from casim.engine.gauge import derive_x1_branch as m   # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "..",
                   "test-results", "F325_x1_branch.json")


def main() -> int:
    res = m.check_x1_branch()
    print("F325 — X1 resolved: branch A closed, branch B adopted")
    print("=" * 72)
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}")
        print(f"         {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F325 gate did not pass"

    controls = [
        ({"magnetic_scale": 2.0}, ("X2",)),
        ({"su3_cut": 2}, ("X2",)),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_x1_branch(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<28} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  verdict:")
    print(f"    branch A                         {s['branch_A_status']}")
    print(f"    branch B                         {s['branch_B_status']}")
    print(f"    g_s adopted                      {s['g_s_adopted']}")
    print(f"    alpha_0 adopted                  {s['alpha_0_adopted']:.8f}"
          "   (= 1/(16 pi))")
    print(f"    magnetic side of C7              {s['magnetic_side_of_C7']}")
    print("\n  cost:")
    for k, v in s["cost"].items():
        print(f"    {k:<24} {v}")
    print(f"\n  residual: {s['residual']}")

    with open(os.path.abspath(OUT), "w", encoding="utf-8") as fh:
        json.dump({"finding": "F325", "date": "2026-08-18",
                   "title": ("X1 resolved: branch A tested and closed, "
                             "branch B adopted"),
                   "checks": res["checks"],
                   "n_pass": res["n_pass"], "n_total": res["n_total"],
                   "summary": s}, fh, indent=2, default=str)
    print(f"\n  wrote {os.path.relpath(os.path.abspath(OUT))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
