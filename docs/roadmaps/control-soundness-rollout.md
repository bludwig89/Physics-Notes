# Control soundness — the rollout, 50 → 0

*Opened 2026-08-08. Owner: unassigned. Mechanism landed 2026-08-07 - 17:45
(`docs/status/completeness-2026-08-07.md` Amendment 2, changelog 17:40).
Ratchet: `gate_assertion_no_control`, armed at **50 of 61**, end state **0**.*

The `control:` layer is built and green. It is not yet *functional*, and the distinction is
the same one gap #3 was about: a mechanism 11 records use is a mechanism, not a barrier.
This is the drain.

---

## 0. Do these three first — they are not the drain, they block it

| # | What | Why it blocks |
|---|---|---|
| **0a** | **Commit `test-results/control-soundness.json`.** | The gate reads the journal instead of re-running. Uncommitted, every clone starts with 25 unverified controls and the static check has nothing to check. This is the same act as committing a `result_dump` baseline — it is what arms the record. |
| **0b** | **Run `make gate` once, end to end.** | Never verified against the 45 s sandbox ceiling — this is the third consecutive report carrying that. Two checks were added to `run_gate.py` yesterday (`check_finding_records`, `check_control_soundness`) by two different sessions, and one of them was briefly deleted by the other. Nobody has seen the assembled barrier run. |
| **0c** | **Fix the `test_registry_entries` stall.** | It hangs on `F288-structure-formation-growth`, which takes **7 s standalone** and never returns as the 18th driver in one process. So it is accumulated in-process state — memory, or BLAS thread oversubscription — not F288. This is the `registry-entries` record the 2026-08-07 report already logs as NOT COMPLETED, twice. While it stalls, `pytest tests/casim` cannot finish, so neither can the gate's package-suite step. Likely fix: run each entry record in a subprocess, as `_run_pytest_file` already does for file-based records. |

`0c` is worth more than its position suggests: it is the only reason the barrier cannot
currently be seen green in one command.

---

## 1. The steady state — what a session does from now on

This is the part that is already functional. It is six lines.

```bash
casim index                      # NEXT FREE NUMBER, as always
# ... write the module, the finding, the test record ...
make control ID=<record-id>      # verify the control; writes the journal
make gate                        # static check reads the journal
git add test-results/control-soundness.json
```

Writing the record, a `control:` block is now part of the record and not a sentence in
`notes:`:

```yaml
control:
  - params: {linear_control: true}       # applied exactly as `casim test --param` would
    reds:   [G10-3, G10-4, G10-5, G10-6] # leg TAGS, resolved by token boundary
    reason: dispersion replaced by exactly linear c|k|, so every lattice correction must vanish
```

Four rules, each of which cost something to learn:

1. **Write the MEASURED `reds:` set, not the expected one.** Run it, read the verdict,
   write down what actually went red. The seeding pass corrected two findings' own prose
   this way — F290's `mass=0.0` reddens C3/C3b/C3d where the docstring said C3, and F281's
   `coupling=nonminimal` reddens M1a/M1b/M1f where the notes said M1a/M1b. Both surfaced as
   `SPILL`.
2. **`SPILL` is not a nuisance, it is the finding.** A perturbation that reddens everything
   is a broken run, and it is also the cheapest way to make a control look green. Widen
   `reds:` only if the extra legs genuinely belong; otherwise the perturbation is too blunt.
3. **`reds:` is optional.** Without it the claim degrades to "the verdict flips PASS → FAIL",
   which is real but weaker, and is all you can say for a driver that emits no `checks`
   list. Prefer legs.
4. **The journal goes stale when the code moves** — driver, test file, record, control block,
   or `runner.py` itself. That is the point. Re-run `make control ID=…` and re-commit.

---

## 2. The drain — 50 records, three buckets, and the order is forced

`make control-todo` prints this live. The buckets are not equal work and, more importantly,
**one of them cannot be started until physics happens.**

### Bucket A — 12 records, strong control today, no code change (~1 session)

Their entry points already take real parameters. Perturb one, run, read the legs, write them
down.

```
F15-closed-form-lv-coefficients     lead_denom=6, next_num=11, next_denom=90, tol=1e-4
F20-bcc-onaxis-dispersion-exact     k0=0.8, m=0.3, n_k=500, h=1e-05
F20-wavepacket-group-velocity       m=0.3, seed='branch-pure', shape=(256,64,64), n_steps=44
F22-rho-identity-and-offshell       m=0.5, k=0.001, v=1e-06, tol=1e-14
F24-sl2c-covariance-full            n_draws=2000, zeta_scale=2.0, seed=24
F276-curved-weyl-ordering-2nd-order L=48, ticks=10, dc_amp=0.05
F280-d1-subtracted                  lambda_wilson=28.8086, C_lat_wilson_loops=6.1386…, ns=(16,20,24)
F288-structure-formation-growth     mu=1.0, A_s=None
F302-bilinear-so3-covariance        n_trials=40, seed=7, k_mag=0.05
F306-curl-closes-at-k3              k_values=(0.1,0.01,0.001), n_dirs=8, seed=0
F314-pair-group-velocity-closed-form n_k=500, k0=0.8, h=1e-05, seed=314
F314-photon-packet-propagation      shape=(128,48,48), m_index=24, n_steps=24
```

Two of these deserve a moment rather than a tolerance-nudge, because the wrong control here
is worse than none:

- **F22** is the record this whole layer exists because of. Its `test_F22_negative_control_fails`
  already asserts the repaired check rejects `rho_override="42"`; the registry should say so
  in `control:` rather than leaving it as the one worked example nothing reads.
- **F280** carries `lambda_wilson=28.8086`, the anchor gap #1 turns on. A control that moves
  it and shows the subtracted formulation follows is worth more than a tolerance control.

**Anti-pattern to avoid in this bucket:** shrinking `tol` until the check fails. That proves
the tolerance is a number, not that the physics is tested. Perturb the *physics* parameter.

### Bucket B — 7 records, driver needs a switch written (~1 session)

```
F245-l1-curl-coefficient      F279-hypercharge-attribution
F246-l2-curl-coefficient      F282-inflaton-candidate-slowroll   (moved from C, 2026-08-08)
F247-q3-omega-degeneracy      F301-boost-covariance-defect
F278-bcc-lattice-constant
```

Add one keyword argument that breaks the thing the finding claims — the shape every seeded
driver already has (`linear_control`, `assume_three_bond_loop`, `tower`, `jw_string`).
**F301 is called out in Amendment 1** as having *"no parameter control … its six declared
controls are internal legs of the same run"*, and it is this rubric's evidence for A2, so it
is the one to do first. **F279** closed H5's code-vs-finding contradiction; a control that
perturbs one hypercharge row and watches the six-row solve go red is the natural one.

### Bucket C — 5 records, BLOCKED on physics *(CORRECTED 2026-08-08: was 8)*

```
F283-elastic-lattice-excluded      F295-tilt-is-an-anomalous-dimension
F285-initial-condition-measure     F296-holographic-anomalous-dimension
F286-second-scale-classification
```

> **Corrected 2026-08-08.** This bucket was 8. **F282, F291 and F292 were false positives** — they
> hold 41, 39 and 30 reachable asserts and always could fail; `_reachable_raises` could not follow
> their `CHECKS` dispatch table (a `for name, fn in CHECKS` loop presents one Call node, on a loop
> variable). Detector fixed, ceiling 8 → 5. **F291 and F292 are now armed** with two declared controls
> each, all verified RED. **F282 moves to bucket B** — it can fail, it just has no `--param` switch
> yet. See Amendment 3. The practical lesson: *check whether a record can fail by breaking it, not by
> reading its AST.*

The five that remain are all cosmology and all genuine — zero asserts and zero raises, F283 being
35 floats and 14 prose strings with fields called `verdict` and `answer_to_ben` holding paragraphs.
The ordering argument is unchanged for them:

> An entry with no pass criteria has no legs to redden. You cannot declare a control on it,
> because there is nothing for the perturbation to turn red. `--suggest` puts them in
> "needs a switch"; that is the tool being literal. They need **pass criteria first**, taken
> from the finding that owns each one — which Amendment 1 correctly left for Ben rather than
> guessing.

The control then falls out of the same edit, for free: the moment a driver has legs, the
switch that breaks one is obvious. **So this is one job, not two**, and doing it in the other
order wastes the work. It also retires the other ratchet — `check_finding_records.py`'s
cannot-fail ceiling, now **5** — at the same time.

Weight: this is the primordial arc — **K3, K5, K12, and K4's F283 leg**. The dimensionality pair is
no longer in it: **A1's evidence is not mechanically unfalsifiable**, which is the half of Amendment
1's sentence that did not survive checking. K3 in particular still rests on two records (F295, F296)
that cannot go red, and that is the strongest argument here for doing bucket C before A or B.

### Bucket D — 24 records, weak `test:` form (~1 session, mechanical)

20 `suite`-sector and 4 `core`: `index-integrity`, `supersession-ledger`,
`constants-consistency`, `backend`, `viz-api`, `registry-entries`, `P3.2-engine-clock`,
`F272-F273-bz-period-lattices`, and so on. These delegate to pytest and have no `entry:` to
inject into. Two honest options, and the choice is per record:

- **Weak `test:` form** — name the in-file function that IS the negative control, writing it
  where it does not exist. `check_finding_records.py` shows the pattern for infra: its
  controls are *fixture-level* (demote a record to a stub → red; point a finding at a
  nonexistent id → red), which is exactly right for a checker.
- **C7.4 promotion** — give the record a `module:`/`entry:` and get a strong control. Worth
  it only where the test is really a function with parameters wearing a file as a costume.

Do this bucket **last**. It is the largest count and the least evidence per record, and
finishing it first would drive the ratchet to a small number while A1 and K3 were still
mechanically unfalsifiable — the count improving faster than the tree, which is the failure
mode this repo's own H7 row keeps catching.

---

## 3. Definition of done

| | |
|---|---|
| `gate_assertion_no_control` | **0**  *(48 as of 2026-08-08, was 50)* |
| `check_finding_records` cannot-fail ceiling | **0** (bucket C retires it; **5** as of 2026-08-08, was 8) |
| every declared control | `CONTROL` at the current fingerprint, journal committed |
| `make gate` | seen green end to end, in one command |
| H2 | still not `EXACT` — this is a process row. `QUANT` is the honest ceiling, and only once `falsifier_unset` (226/226, the **register** half, a different object) has been touched too |

**Suggested order: 0a → 0c → 0b → C → B → A → D.** Bucket C first because it is the only one
that changes what the model can claim; D last because it is the only one that mostly changes
a number.

---

## 4. One thing to decide, not to do

Whether `only: true` should stay the default. Two of eleven seeded records tripped `SPILL` on
first run and both were legitimate widenings, not defects. If that ratio holds across the
remaining 50, the strictness is buying a re-run per record and catching nothing — and if it
does not hold, it is catching exactly what it was built to catch. **Revisit after bucket A**,
when there are ~23 measured controls rather than 11, and record the decision either way.
