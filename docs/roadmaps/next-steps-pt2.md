# Continuing Next Research Steps

- ~~hypercharge.py writes Y_LEPTON_L = -1, Y_E_R = -2, Y_NU_R = 0 as literals under a comment reading "SM hypercharge assignment". They are derived (F165, re-derived by F279) and belong in casim.constants with provenance. F279 follow-up 1, unactioned.~~ **Done 2026-08-06** — registered in the electroweak sector (Y_E_R resolves from Y_LEPTON_L; Y_NU_R forced by the F47 Majorana row; Y_LEPTON_L is the residual normalisation), module imports them, F279's gate record now checks the values against the derived line. Quark hypercharges deliberately left as literals: their fractions carry the underived N_c = 3, so that promotion belongs to the "why three colours" item, not this one.

- ~~ per completeness-2026-08-04 item A6, the Born rule is reproduced in tests, but not derived, build out a derivation for the born rule within the model.~~

- ~~per completeness-2026-08-07 item A11, F116, f164, f264, f284 we have some some UV completeness issues that are not reconciled or resolved. Attempt to round out the uv sector completeness within the model.~~

- ~~per completeness-2026-08-04 item B12, gauge boson masses p, m_z, and m_w are not predicted yet. Execute the calculation and prediction of their masses within the model if possible.~~

- ~~per completeness-2026-08-07 item b11, flagged loops are open in the theta/strong cp area.~~ 
- per completeness-2026-08-07 gap #1b, can we build within the model an order-selective vacuum-energy mechanism that allows for the current energy constraints?

- ~~per completeness-2026-08-07 item b9, running of α, EW couplings again as a re-derivation post f277. rerun this again.~~ **F322, 2026-08-17 - 21:55.** Two answers, and they are different. (a) Accounting: the 0.24% never touched the refolded path — `leptonic_running`'s call closure is disjoint from `_fermion_B`, measured bitwise under a 7.3×+0.5 kernel perturbation. Fourth consecutive residual that was mis-stated rather than hard (A11, B12, B11, now B9). (b) Physics: q-flatness of Δ = B_rule − B_cont **is** Δα invariance, with the exact model-internal conversion δ(Δα) = 4πα·δB from b₀ = 4/3. Post-F277 the lattice bound is 6.8e-6 at n=28, 0.088× the PDG shortfall, and *falls* with n; with the refold restored it is 1.4e-2, 183–190× the shortfall and n-independent. **So F277 did not change the number, it created its warrant.** Then the shortfall is attributed: F261's sympy-exact b₁ = 1, never fed into the running, closes 79.8% of it — 0.245% → **0.0495%**. EW leg: F138's +0.222% reproduced, and it doubles to +0.450% on the model's own leptonic-only α, which is what B9 pays for deferring the hadronic piece to row G3.

- ~~per completeness-1016-08-07 item b7, now that we have derived the +1 time dimension as the update rule, does this allow confinement to be built stronger?~~

- per completeness-2026-08-07 item B10, now that we have derived the SU(3) gauge field from the model structure, does this answer the "why 3 colors" question or is there more work to be done?

- per completeness-2026-08-07 item g3, Hadronic VP, HLbL and EW are not claimed yet. build out each from within the model structure.

**(F22 remediation 2026-08-04 ESCALATED and DEFERRED items)** 
- ESCALATED (2)
  -  Retract claims 1 and 3 from F22's headline and re-title the finding. Claim 1 goes from EXACT to false; claim 3 from "deformed formula" to "the composition law is undeformed Einstein addition in the nonlinear variables". This moves a headline claim by more than two exactness classes, which is Step-3 territory. The corrected physics is already written into the finding's ## Corrections and measured in the gate record — only the headline and the title are held.
  - Dispose of exactness-inventory rows 45, 46 and 47. Rows 46 and 47 are identities whose checked expressions never touch the dispersion. They should be deleted or moved out of Tier 1, which is tied to decision 1.
- DEFERRED (2). Adding F22 to papers/Claims-and-Falsifiers-Summary.md (should follow the retraction, not precede it); and whether any of this survives on the canonical BCC lattice.

**(F25 remediation 2026-08-04 DEFERRED item)** **Withdraw `## Physical interpretation` items 3 and 4.** Maxwell is *not*
   recovered as $\Delta t\to0$ ($B = \hat n\times E$ exactly, so
   $\hat n\times B = -E$ and the two sides are orthogonal at every $\Delta t$), and
   the $O(k)$ residual is not a Planck-scale signature — it is quadrature between two
   vectors that agree in magnitude to 1 part in $10^8$.
1. **Correct `exactness-inventory.md:526` row 3**, which records both of those claims
   as settled and cites F25 for them. Shared with F23 — fix once.
2. **Publish the positive result F25 was one step from:** under analytic amplitudes
   the curl equation closes at $O(k^3)$ with coefficient $c_\text{lat}^3/48$, and the
   whole discrepancy reduces to $\omega = \sin\omega$, i.e. $\Omega - 2\lvert n\rvert = k^3/(72\sqrt3)$.
   That is a genuine, exact, falsifiable lattice statement, and it is what this
   finding should be about.
3. **Reclassify P1 as an identity rather than a prediction.** Keep Tier-1 #51 — it
   *is* exact — but stop presenting it in `## Results` as beating Maxwell by five
   orders of magnitude. They are not competing hypotheses.

## Project Status 




## Skills Cheat Sheet

See .claude folder for our current skills.

- `/state-of-model` skill regens a new completeness file to see where we are on a complete model.d
- `/review-finding` Run an adversarial, cold-context review of one finding and write a dated report to `docs/reviews/`. The point is not to summarise the finding. The point is to try to break it, starting from an independent re-derivation done by someone who has not read it.

  - Argument: the finding number (F253, or 253). Optional flags:

  - `--inline` — run in the current session instead of spawning subagents (cheaper, much weaker; the session that built the finding then reviews its own work — say so in the report header).
  - `--fast` — skip Attack 7 (the perturbation sweep) and Attack 12 (robustness), which are the two slow ones. Record them as NOT RUN, never as PASS. 

- `/remediate-finding` Takes the fixes and errors found by `/review-finding` and updates the finding to clarify and fix what was missed. Meant to run in a loop, `/review-finding` first then `/remediate-finding`. 
