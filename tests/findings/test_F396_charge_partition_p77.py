"""F396 -- the p.77 charge-partition hypothesis: Leg A (J = L + S) and Leg B (per-tick
charge bookkeeping of the F27/F41 beta-gauged mass step).

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_charge_partition.check_charge_partition`
(record `F396-charge-partition-p77`, tier gate), so this file defines no `test_*`
functions.

    casim test --id F396-charge-partition-p77
    casim test --id F396-charge-partition-p77 --param spin_frame=raw       # red (Jz leg)
    casim test --id F396-charge-partition-p77 --param charge_frame=raw     # red (Q-conservation leg)
"""
import json
import os
import sys


def main() -> int:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge.derive_charge_partition import check_charge_partition
    res = check_charge_partition()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results", "F396_charge_partition_p77.json")
    with open(out, "w") as fh:
        json.dump({k: (v if not hasattr(v, "item") else v.item()) for k, v in res.items()}, fh, indent=2, default=float)
    assert res["n_pass"] == res["n_checks"], res["checks"]
    return 0


if __name__ == "__main__":
    sys.exit(main())
