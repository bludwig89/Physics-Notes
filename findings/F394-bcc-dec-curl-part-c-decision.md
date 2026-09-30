# F394 — Part C decision: the 3D BCC discrete-exterior-calculus curl complex is deferred, not attempted, this session

*2026-09-16 - 02:00 · sector `gauge` · scope: a scoping decision, no module written · analysis-only, no test record (reason below)*

**Status:** Decision recorded — Part C of `docs/roadmaps/photon-fermion-coupling-rerun-prompt.md` is explicitly **deferred**, per that document's own §9/Part C permission to stop after Part B and say so.
**Reviewed:** 2026-09-16 — **CONFIRMED** ([independent review](../docs/reviews/F394-review-2026-09-16.md))

**Target.** Part C asks whether to build a genuine discrete-exterior-calculus (DEC) curl on the 3D BCC lattice — sites/bonds/plaquettes/cells with `d0,d1,d2` and their adjoints, extending `charge_coupling.discrete_curl_z`/`discrete_div` from the existing 2D construction — as a new object alongside (not replacing) `bcc_curl_symbol`, whose defect [[F393-curl-grad-identity-diagnostic]] just made visible and gated.

**The decision.** **Not attempted this session.** The rerun-prompt's own text names this decision point explicitly and pre-authorizes stopping here: *"If the BCC DEC complex turns out to be more than this session can carry, stop after Part B and say so. A correctly-scoped negative result here is worth more than a rushed replacement, and the audit's §9 explicitly says deciding what to do about this symbol is a research session of its own."* Three reasons converge on taking that option:

1. **The construction is genuinely novel, not a mechanical extension.** The existing 2D precedent (`discrete_curl_z`/`discrete_div`) is a simple-cubic plaquette curl on a square lattice with an obvious oriented-boundary convention. The BCC lattice's own neighbour structure is 8 fractional shifts (`lattice.bcc.py`'s `BCC_DIRS`, each a shift of `d/√3` for one of 8 body-diagonal directions), not axis-aligned integer bonds — so "the plaquette" is not a re-use of the 2D convention's geometry; it requires an independent choice of which loops of fractional-shift bonds bound a 2-cell on this lattice, consistent orientation, and a proof that the resulting `d1∘d0=0`/`d2∘d1=0` hold not just algebraically but for the *specific* cell complex chosen — exactly the kind of derivation `references/lattice-conservation-laws-research-review.md` §2 names a genuine open research question (its own nearest citation, the FCC/BCC DEC-FDTD paper, is flagged `[unverified]` there, not read).
2. **Downstream verification is expensive and this session's remaining scope is large.** Part C's own text requires, before landing anything: gating both `d∘d=0` identities to machine precision (matching the 2+1D prototype's `8.9×10^{-16}`) on the new 3D complex, *then* measuring the blast radius against every existing consumer (`solve_A_coulomb_3d`, `magnetostatic_B`, `maxwell_curl_step`, `em_current.conserved_current`, `em_photon_sourcing.split_transverse_longitudinal`) and reporting what moves **before switching anything** — a multi-step verification program in its own right, on top of Part D's six-stage re-run, which is "the point of the exercise" per the rerun prompt's own framing and should not be starved of session budget to make room for a rushed Part C.
3. **Nothing in Part D requires Part C to have landed.** The rerun-prompt's own Part D instructions are explicit: *"Only after Part A lands (Part C optional — if it does not land, say so explicitly in every finding and note that the re-run still carries the curl defect)."* Every Part D finding in this session states this explicitly.

**What this decision is not.** It is not a claim that the DEC route is wrong, unnecessary, or unlikely to work — §6.3 of the audit lists what already exists to build on (`minimal_coupling.u1_link_weyl_step_3d_bcc`'s Peierls phases, `gauge.bcc_action`/`link_hamiltonian`'s Wilson plaquette action, `photon.build_pair_mode`'s correct `E⊥B` construction, `core.observers.Momentum`'s verified-sound observer), and a future session picking this up starts from that inventory, not from nothing.

## What a future session needs, in order

1. **Settle the Weyl-vs-Dirac question first** (audit §5, `references/lattice-conservation-laws-research-review.md` §7.1) — Nielsen–Ninomiya bites the Weyl-only scope F384–F391 all declare, and the clean single-action route runs through the Dirac sector instead. This changes what `S_matter` is and should be decided *before* the DEC complex is built, per the rerun-prompt's own "FLAG FOR A LATER SESSION" note. Cross-check against F328 and F378.
2. **Define the BCC 2-cell (plaquette) geometry** — which minimal loops of the 8 fractional-shift bonds bound a face of the BCC's own cell complex, with a consistent orientation, before writing any `d0`/`d1`/`d2` code.
3. **Gate `d∘d=0` on the new complex to machine precision** before doing anything else with it — a red flag at this step means the geometry chosen in step 2 was wrong, not that BCC is unsuitable for DEC.
4. **Only then** measure the blast radius against every existing `bcc_curl_symbol` consumer, and report before switching anything, exactly as the rerun-prompt's own Part C text requires.

## Caveats

- **This is a scoping decision, not a physics result** — no module was written, no number was measured, and no existing code path was touched. It exists so a future session (or the same session, if the user wants to continue after Part D) has a recorded, reasoned starting point rather than re-deriving the same "should we build this now" question from scratch.
- `bcc_curl_symbol` remains unchanged and its [[F393-curl-grad-identity-diagnostic]] gate leg remains a monitored, known defect, not a resolved one.

**Test record:** none — no-test (analysis-only). A scoping/deferral decision; nothing was built to test.
**Claim:** none — no assertion against established physics is made or withdrawn here; the question of whether a BCC DEC curl is achievable is left genuinely open per the audit's own §9.

**Cross-references:** [[F393-curl-grad-identity-diagnostic]] (the gate leg this decision leaves unresolved), [[F387-curl-anisotropy-omega-pair-mismatch]], [[F328]], [[F378-discrete-cpt-gauged-kinetic-theorem-mass-sector-no-go]] (the Weyl/Dirac findings a future session should read first, per the audit's own flagged item).
