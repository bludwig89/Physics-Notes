"""D12 — the claims layer holds together.

Three properties, and each one has a failure this test exists to catch:

1. **`tools/check_claims.py` passes.** Closed vocabularies, referential
   integrity, the debt ratchets, and THE rule (a `status: live` card whose every
   supporting finding is named in a `superseded:` list in the ledger). That last
   one is the machine-checkable form of "overstated" and it fired on seven cards
   the first time it ran.

2. **`registry.yaml` is a true projection of the cards.** The direction of
   generation is backwards here — the card's front matter is the record, the
   registry is generated from it — so the failure mode is a registry that has
   drifted from the cards it claims to summarise. `casim index --check` covers
   this; asserting it here means a bare `pytest` sees it too.

3. **The withdrawn set is not empty.** A `withdrawn` card is the retraction
   record for a claim that was published live, and the standing hazard is that
   someone "tidies up" by deleting them — at which point the project has no
   memory that it once predicted a horizon-free black hole, and nothing stops
   the claim being made again. This is a canary, not a coverage test.
"""
from __future__ import annotations

import os
import subprocess
import sys


def _repo():
    """Resolved on call, not at import.

    `tools/audit_tests.py --ratchet` counts module-scope work because anything
    computed at import runs on `pytest --collect-only`, and the standing rule
    (CLAUDE.md §"Result artifacts and paths") is that a test module does nothing
    when merely walked. A path join is cheap, but the ratchet counts statements,
    not cost, and the number may only fall.
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))


def _run(*args):
    repo = _repo()
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [os.path.join(repo, "src"), env.get("PYTHONPATH", "")])
    return subprocess.run([sys.executable, *args], cwd=repo, env=env,
                          capture_output=True, text=True)


def test_check_claims_passes():
    r = _run("tools/check_claims.py")
    assert r.returncode == 0, f"check_claims failed:\n{r.stdout}\n{r.stderr}"


def test_claims_registry_and_index_are_current():
    r = _run("-m", "casim.cli", "index", "--check", "--only", "claims")
    assert r.returncode == 0, (
        "docs/claims/registry.yaml or claims-index.md is stale — "
        f"run `make claims`.\n{r.stdout}\n{r.stderr}")


def test_withdrawn_cards_survive():
    """The retraction record must not be tidied away."""
    d = os.path.join(_repo(), "docs", "claims")
    withdrawn = []
    for fn in sorted(os.listdir(d)):
        if not (fn.startswith("CL") and fn.endswith(".md")):
            continue
        with open(os.path.join(d, fn), encoding="utf-8") as fh:
            head = fh.read(1200)
        if "\nstatus: withdrawn" in head:
            withdrawn.append(fn)
    assert withdrawn, (
        "no `status: withdrawn` claim cards remain. A withdrawn claim that is "
        "deleted is a claim that gets re-made — see docs/claims/README.md.")
    # The five revision-2 withdrawals are the ones that were published live.
    assert len(withdrawn) >= 5, f"expected >=5 withdrawn cards, found {withdrawn}"


if __name__ == "__main__":
    test_check_claims_passes()
    test_claims_registry_and_index_are_current()
    test_withdrawn_cards_survive()
    print("claims layer OK")
