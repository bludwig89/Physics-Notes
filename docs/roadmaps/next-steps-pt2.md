# Continuing Next Research Steps

build out the NB-034 (p.25) — Combining the Variations: the Boxed Free EOM equations of motion and fully test against the structure of the current casim model.

can NB-088 (p.69) — Proposed $B_\mu$ Neutral-Current Field be explored more thoroughly and tested for structural stability?



## Project Status 

- I keep seeing this python message: " SyntaxWarning: "\_" is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\_"? A raw string is also an option." for many "\" escape messages. investigate the issue and propose solutions.

- **Two records are both a pytest file and an `entry:`** — `F305-bcc-rhombic-vertices` and
  `F307-action-consistent-d1`. `tests/casim/test_registry_entries.py::test_entry_driven_records_are_hidden_from_file_collection`
  fails on them ("Pick one contract"). **F305 was already red at HEAD**; F307 only became visible
  when F327's session had to run `tools/gen_test_registry.py` (the committed `evidence:` block was
  stale, so `pytest_funcs: true` had never been recorded for it). Both records carry rich
  `params:`/`control:` blocks, so the `entry:` contract is the one that actually runs and the
  pytest functions are the redundant half — but which half to drop is a decision for whoever owns
  the d1/LPT line, not for a passing session. Landing site: this row.
- **`CLAUDE.md`'s V-004 paragraph is stale.** It says the entry-driven route through
  `tests/casim/test_registry_entries.py` carries "today exactly one" record
  (`F276-curved-weyl-ordering-second-order`). That file now collects 60 tests, ~15 of them
  entry-driven. The 27-vs-24 arithmetic in the same paragraph should be re-measured with it.

## Skills Cheat Sheet

See .claude folder for our current skills.

- `/state-of-model` skill regens a new completeness file to see where we are on a complete model.
- `/review-finding` Run an adversarial, cold-context review of one finding and write a dated report to `docs/reviews/`. The point is not to summarise the finding. The point is to try to break it, starting from an independent re-derivation done by someone who has not read it.

  - Argument: the finding number (F253, or 253). Optional flags:

  - `--inline` — run in the current session instead of spawning subagents (cheaper, much weaker; the session that built the finding then reviews its own work — say so in the report header).
  - `--fast` — skip Attack 7 (the perturbation sweep) and Attack 12 (robustness), which are the two slow ones. Record them as NOT RUN, never as PASS. 

- `/remediate-finding` Takes the fixes and errors found by `/review-finding` and updates the finding to clarify and fix what was missed. Meant to run in a loop, `/review-finding` first then `/remediate-finding`. 
