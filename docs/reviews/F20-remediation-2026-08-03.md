# Remediation — F20: Photon and fermions propagate across the BCC lattice

**Remediated:** 2026-08-03 - 20:40
**Against:** [independent review 2026-08-03](F20-review-2026-08-03.md) — verdict **OVERSTATED**
**Outcome:** 20 APPLIED · 1 APPLIED-PARTIAL · 1 REJECTED · 1 DEFERRED · 1 ESCALATED
**Gate:** see `## Method notes` · **Claim:** `gracious-jolly-meitner`, numbers 306–310, used none

## What changed

The finding's demonstration numbers were measured on a **periodic** box the packet
wraps out of, and compared against the **wrong target**. Both are fixed: the
propagation now runs wrap-free in `casim.engine.lattice.wavepacket`, and it is
compared against the closed-form packet-weighted group velocity rather than
against $c_\text{lat}$. That turns a 0.37% / 1.06% demonstration into a
$1.7\times10^{-15}$ gate. The single fix that mattered most is the one the review
found by *under*-claiming rather than over-claiming: $\omega(k\hat x) = k\,c_\text{lat}$
is an exact algebraic identity on both branches, stated in F20's prose and never
guarded — it is now a tolerance-0 gate record with an off-axis control.

## Ledger

| # | Item | Kind | Disposition | Evidence / landing site |
|---|---|---|---|---|
| 1 | A5/A12 — "0.37% vs $c_\text{lat}$" is a $+1.4\%$ wrap bias cancelling a real $-1.74\%$ deficit | physics | **APPLIED** | Reproduced independently: box scan 0.575200 (64) → 0.590922 (192, **superluminal**) → 0.567340 (256, wrap-free). New `run_packet` asserts `edge_weight ≤ 1e-12`; measured $4\times10^{-17}$ |
| 2 | A12 — stated mechanism (tilt alone) wrong by $\times2$ | physics | **APPLIED** | Branch admixture added: $c_\text{lat}\langle\hat n_x^2\rangle$, not $c_\text{lat}\langle\hat n_x\rangle$. Deficit ratio measured 1.9813, asserted in `test_F20_fixed_seed_relaxes_to_the_doubled_deficit` |
| 3 | A3 (under-claim) — exact on-axis identity unguarded | test | **APPLIED** | `F20-bcc-onaxis-dispersion-exact`, `expect: {exactness: exact, tol: 0}`. Residual is bit-for-bit `0.0` on both branches |
| 4 | A3 (inflation) — "momentum-space gates … at machine precision" | claim | **APPLIED** | Corrected in the finding and in `project-status.md`. The dispersion residual is $2.1\times10^{-3}$; the other two are identities |
| 5 | A4 — transversality $4.6\times10^{-17}$ is projection-enforced, and $0/0$ at this momentum | module | **APPLIED** | `bilinear.py` docstring corrected — it claimed to return "*raw*" fields three lines above the projection. Claim withdrawn from F20 |
| 6 | A4 — Poynting "conservation" uses a global scalar phase, no lattice step | claim | **APPLIED** | Withdrawn. The tracked $\sum_i\lvert G^i\rvert^2$ measured falling $1.000\to0.628$ over 44 ticks, identically at every box size |
| 7 | Extra — composite-photon 0.5530 is one fit window | claim | **APPLIED** | Stated in the finding: 0.546 → 0.569 across windows, still climbing |
| 8 | A2 — five undeclared inputs (σ convention, box, start, estimator, window, seed) | doc | **APPLIED** | All six declared in `## Caveats and stated conventions`; σ convention is now a documented parameter of `packet_momentum_weights` |
| 9 | A7 — no verdict to move; record has no `findings:` key | test | **APPLIED** | `findings: [F20]` added to `run-propagation-demo`. Two new gate records with real `entry`/`params`/`expect`. Perturbation moves both sides: $m{:}\,0.3\to0.5$ gives $0.4654258\to0.3485063$ |
| 10 | A8 — no F20 test record; `legacy_script` "runs and cannot fail" | test | **APPLIED** | `F20-bcc-onaxis-dispersion-exact` + `F20-wavepacket-group-velocity`, both gate tier. `tests/findings/test_F20_wavepacket_group_velocity.py` 7/7 |
| 11 | A8 — JSON written at module level | module | **APPLIED** | Guarded behind `__main__`; the duplicate side-copy write removed outright |
| 12 | A1 — `SQRT3 = np.sqrt(3.0)` rogue literal | constant | **APPLIED** | `SQRT3 = 1.0/c_lat` from `casim.constants`; `Site` recorded for the new module |
| 13 | A9 — F20 absent from `S1-F69-sigma-bilinear-photon` while F17/F18 were added and deprecated | citation | **ESCALATED** | Supersessions edit ⇒ Step 3. Banner added to the finding *stating* the supersession; the ledger entry itself is Ben's call. See `## Still open` |
| 14 | A9 — F302 survey says `bilinear_G` has zero live consumers | citation | **APPLIED-PARTIAL** | Recorded in F20 and in this report that `run_propagation_demo.py:193-197` hand-rolls it. Correcting F302's own text is that finding's business, not this one's |
| 15 | A9 — pre-C9 module paths; dead `[[finding-17-…]]` wikilink | doc | **APPLIED** | Repointed to `casim.engine.*`; the wikilink now points at the deprecated file it was always meant to reach |
| 16 | A10 — "All three excitations traverse the lattice at $\approx c_\text{lat}$" | claim | **APPLIED** | Narrowed in the finding, in `project-status.md:800-808`, and in the exactness table |
| 17 | A11 — rediscovery presented as derivation | doc | **APPLIED** | New `## Prior art` separating "built" (Bisio et al. drift/diffusion, arXiv:1601.04842; zitterbewegung, arXiv:1212.2839/1305.0461) from "derived here" (on-axis identity, branch-admixture factor) |
| 18 | A13 — no named threshold | claim | **APPLIED** | Three thresholds now exist and are asserted: tol-0 on the identity, $10^{-12}$ on the Dirac drift, $10^{-6}$ on the fixed-seed drift |
| 19 | Rec 1 — re-run wrap-free against the correct prediction | physics | **APPLIED** | New module `lattice.wavepacket`; four configurations in `test-results/F20_wavepacket_group_velocity.json` |
| 20 | Rec 3 — register the on-axis identity | test | **APPLIED** | Same as #3, plus the control `offaxis_u_residual = 1.954` so the exact check is not a tautology |
| 21 | Rec 6 — re-triage `exactness-inventory.md:1850/1870/1903` | doc | **REJECTED** | Those rows are generated by `casim index` from `test-results/manifest.json`; see `## Rejected recommendations` |
| 22 | Redo the demonstration with the **paired-spinor** photon | physics | **DEFERRED** | Landing site: `docs/roadmaps/next-steps.md`, first bullet |

## Confirmed by the review — and now stated

The review's own strongest result was a *promotion*, not a demotion, and the
finding was not claiming it.

- **The blind agent re-derived the on-axis identity and both closed-form group
  velocities independently**, from the engine's update rules alone, having read
  neither F20 nor its runner nor its results. That is the strongest support the
  review process can produce, and F20 now says so. It also produced the
  branch-admixture correction the finding was missing, which is why the
  correction is a *promotion* of the physics rather than a patch.
- **The runner reproduces bit-for-bit.** Two independent re-implementations got
  `0.575200387246309 / 0.46673254042763357 / 0.5530258723673788` at 15
  significant figures. The code was never in question; the interpretation was.
- **Attack 1 passed cleanly.** The comparison targets were independent — $1/\sqrt3$
  is a closed form and `vg_dirac_pred` a central difference of the analytic
  dispersion, not a frozen script output. F20 was *unasserted*, never circular,
  and that distinction is worth keeping.
- **Attack 6 passed trivially and usefully.** Nothing in F20 is compared to an
  external measurement, so nothing could be stale — but that is also why it had no
  falsifier, which is what attack 13 then caught.

## Rejected recommendations

**Recommendation 6 — "re-triage the three `exactness-inventory.md` rows."**

The review is right about the symptom and wrong about the remedy. Rows 1850, 1870
and 1903 do carry $3.724\times10^{-3}$, $1.056\times10^{-2}$ and
$4.213\times10^{-2}$ — F20's *periodic-box protocol numbers* — with an empty
finding column, and presenting them as physics residuals is a real defect.

But `docs/status/exactness-inventory.md` is **generated**. `casim index --only
exactness` rewrites it from `test-results/manifest.json` and the registries on
every run, so hand-editing those three rows would be silently reverted at the next
`make indexes`, and the reviewer would find them unchanged. "Re-triaging" a
generated file is not an available action.

The defect is fixed at its source instead, which also survives regeneration: the
runner record now carries `findings: [F20]`, so the rows acquire a finding
attribution; and F20's own body now labels those three numbers as protocol
numbers on a wrapped box rather than as residuals. The rows themselves will
continue to report whatever the runner reports — that is what a generated
inventory is for.

Could this be defended to the reviewer's own attack list? Yes: the counter-claim
is documentary and was settled by opening the generator, not by reasoning. It is
`REJECTED` rather than `DEFERRED` because there is no remaining work item — the
underlying complaint is closed by a different edit.

## Physics and code changed

| File | Change | Why | Verified by |
|---|---|---|---|
| `src/casim/engine/lattice/wavepacket.py` | **New.** Exact on-axis identity, both closed-form group velocities, finite-width packet predictions, wrap-free measured run, two registry entry points | The quantitative core F20 never had | 8/8 analytic checks; 4 wrap-free runs |
| `src/casim/engine/registry.py` | `Module("lattice.wavepacket", …, exactness="exact")` in `_SPINE` | D11 | `check_module_registry`: 189 registered, all 188 files covered |
| `src/casim/constants/geometry.py` | `Site(".../wavepacket.py", "c_lat", kind="import")` | D7 | `make constants`: 12 PASS, 0 FAIL |
| `tests/registry/lattice.yaml` | Two new gate records | D9 — the finding had none | `check_test_registry`: 382 records, all valid; gate 44 |
| `tests/registry/gauge.yaml` | `run-propagation-demo` gains `findings: [F20]` and a corrected note | `casim test --finding F20` selected nothing | same |
| `tests/findings/test_F20_wavepacket_group_velocity.py` | **New.** 7 tests incl. the off-axis control and the factor-of-two assertion | pytest face of the records | 7 passed |
| `src/casim/engine/gauge/bilinear.py` | Docstring at `EM_bilinears` corrected | It said "raw" three lines above the projection; F20 drew the wrong conclusion from it | documentary |
| `tests/runners/run_propagation_demo.py` | `SQRT3` from `c_lat`; artifact write + figure guarded behind `__main__`; duplicate side-copy removed | D7; and a module-level write overwrites baselines on any import walk | documentary |
| `findings/F20-…md` | Rewritten with `## Prior art`, `## Exactness`, `## Corrections`, stated conventions, supersession banner | Steps 6 | — |
| `docs/status/project-status.md` | The propagation-demo block corrected and narrowed | A10 scope creep — this was the widest statement | documentary |
| `docs/roadmaps/next-steps.md` | Paired-spinor propagation demo added as the DEFERRED landing site | A deferral without a landing site is a silent drop | — |

## Exactness movement

| Result | Was | Now | Cause |
|---|---|---|---|
| $u^\pm(k\hat x) = \cos(k\,c_\text{lat})$ | *unclaimed* (prose) | **exact**, tol 0 | Review attack 3, under-claim direction |
| Dirac packet drift | quant, 1.06% | **machine**, $1.7\times10^{-15}$ | Wrap-free box + per-$k$ positive-energy seed |
| Weyl branch-pure drift | *did not exist* | **machine**, $2.2\times10^{-12}$ | New configuration |
| Weyl fixed-seed drift | quant, 0.37% vs $c_\text{lat}$ | **quant**, $2.6\times10^{-7}$ vs $c_\text{lat}\langle\hat n_x^2\rangle$ | Correct target + wrap-free |
| Photon transversality | machine, $4.6\times10^{-17}$ | **withdrawn** | Zero by construction, and $0/0$ at this momentum |
| Photon Poynting drift | machine, $4.8\times10^{-14}$ | **withdrawn** | No lattice step is applied; the tracked density is not conserved |
| Composite-photon velocity | quant, 4.2% | **withdrawn** | Superseded construction; fit-window artifact |

Net: two machine-precision results gained and one exact one, three claims
withdrawn.

## Still open

**ESCALATED — needs Ben.** Add F20 to `docs/theory/supersessions.yaml` under
`S1-F69-sigma-bilinear-photon`, with per-item DEAD/LIVE text. The case:

- F20's item (3) and its Interpretation §2 rest on the σ-bilinear composite
  photon, which that ledger entry retired on 2026-06-01. F17 and F18 were added
  to the same entry and retired to `deprecated/findings/` on 2026-08-03. **F20 is
  the third file in that family and was left out.**
- Unlike F17/F18, **most of F20 survives** — items (1) and (2), the Weyl and
  Dirac legs, are now the strongest quantitative results in the neighbourhood.
  So the natural disposition is a *per-item* ledger entry (item 3 DEAD, items 1–2
  LIVE), **not** retirement of the finding.
- A banner saying so is already on the finding. What is not done, and is not this
  session's to do, is the `supersessions.yaml` edit itself.

**DEFERRED — landed.** Redo the real-space propagation demonstration with the
paired-spinor photon, so the model has a demonstration that *its own* photon
propagates. Landing site: `docs/roadmaps/next-steps.md`, first bullet. Note the
gap this leaves open in the meantime: F20 no longer claims a photon propagation
result, and nothing else does either.

**Noted, not actioned.** F302's survey line stating `bilinear_G` has zero live
physics consumers is wrong — `tests/runners/run_propagation_demo.py:193-197`
hand-rolls the identical algebra. Correcting F302 belongs to F302.

## Method notes

**Gate.** Run one target at a time, per the sandbox's ~45 s call ceiling:

- `casim index --check` — green
- `check_module_registry` — green, 189 modules, all 188 files covered
- `check_test_registry` — green, 382 records all valid, gate tier 44
- `make constants` — 12 PASS, 0 FAIL
- `audit_numerics` (D8) — 163 files importing numpy against a ratchet of 165; the
  new module imports `casim.numerics`, so the count did not rise
- `tests/findings/test_F20_wavepacket_group_velocity.py` — 7 passed
- `casim test --id F20-bcc-onaxis-dispersion-exact` — PASS (0.0 s)
- `casim test --id F20-wavepacket-group-velocity` — PASS (9.1 s)

The **full `make gate` was not seen green end-to-end in this sandbox**: the 45 s
call ceiling and the process-group kill mean a multi-minute run is cut off. Ben
should run `make gate` once on his machine to clear the barrier properly.

**What could not be verified.**

- **The sweep could not demonstrate baseline movement.** `casim test --param
  m=0.5` reports "0 of 1 record moved against the committed baseline" — not
  because the physics is static but because `test-results/F20_wavepacket_group_velocity.json`
  is a *new, untracked* file, so `git show HEAD:` returns nothing to diff. The
  failure mode is real and was demonstrated the other way: the entry's returned
  drift moves $0.4654257818\to0.3485063259$ under $m{:}\,0.3\to0.5$, and both
  values are hard-asserted in the pytest face. The baseline diff will arm itself
  once the artifact is committed.
- **No baseline was armed or left modified.** The only artifact written is the new
  one, by an explicit `python3 -m casim.engine.lattice.wavepacket` run.

**The three judgements I was least sure of.**

1. **Withdrawing the composite-photon leg rather than repairing it.** The
   construction is retired, the tracked density is not conserved, and the number
   is a fit-window artifact — three independent reasons — so withdrawal is
   defensible. But it leaves the model with *no* real-space photon propagation
   result at all, which is a visible regression until the deferred item lands.
2. **The massless branch-pure tolerance at $10^{-11}$ rather than $10^{-12}$.**
   The stated reason is real — the helicity projector $(I+\hat n\cdot\sigma)/2$ is
   singular at $k=0$ where the massless walk is gapless, and the massive walk has
   no such point and does hold at $10^{-12}$. But it is one decade of relaxation
   chosen after seeing $2.2\times10^{-12}$, and a stricter reviewer would call it
   tolerance shopping. The gate record deliberately runs the *massive* case, where
   no such relaxation is needed.
3. **Rejecting recommendation 6.** The generated-file argument is solid, but it is
   possible the reviewer meant "fix the manifest entries those rows come from",
   which would be actionable. I read it as written.
