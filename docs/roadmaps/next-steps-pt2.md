# Continuing Next Research Steps


- per completeness-2026-08-18 itme b7, 3+1d confinement is built but not proven within the model. If possible execute a full proof.

- ~~per completeness-1016-08-07 item b7, now that we have derived the +1 time dimension as the update rule, does this allow confinement to be built stronger?~~

- ~~per completeness-2026-08-07 item B10, now that we have derived the SU(3) gauge field from the model structure, does this answer the "why 3 colors" question or is there more work to be done?~~

- per completeness-2026-08-07 item g3, Hadronic VP, HLbL and EW are not claimed yet. build out each from within the model structure.

## Project Status 

- build a plan to go through all findings in the project, if they aren't set each one up correctly in the registry, make sure it is associated to it's tests, if it has any, if not mark it as no-test, and associate it with its claims card, if it has one. 

- the findings-index is not staying up to date, or organized by finding number, where are we currently keeping an active findings index?


## Skills Cheat Sheet

See .claude folder for our current skills.

- `/state-of-model` skill regens a new completeness file to see where we are on a complete model.
- `/review-finding` Run an adversarial, cold-context review of one finding and write a dated report to `docs/reviews/`. The point is not to summarise the finding. The point is to try to break it, starting from an independent re-derivation done by someone who has not read it.

  - Argument: the finding number (F253, or 253). Optional flags:

  - `--inline` — run in the current session instead of spawning subagents (cheaper, much weaker; the session that built the finding then reviews its own work — say so in the report header).
  - `--fast` — skip Attack 7 (the perturbation sweep) and Attack 12 (robustness), which are the two slow ones. Record them as NOT RUN, never as PASS. 

- `/remediate-finding` Takes the fixes and errors found by `/review-finding` and updates the finding to clarify and fix what was missed. Meant to run in a loop, `/review-finding` first then `/remediate-finding`. 
