# Audit V — Tier-B manifest

*Written 2026-08-01 by the audit session (claim `audit-v`).*
*Runner: `tools/audit_v_battery.sh`. Report: `docs/audits/physics-audit-report-2026-08-01.md`.*

Everything Physics Audit V could not run in the sandbox, because a single bash call there is
killed at ~45 s. **One JSON per item**, so the next session completes the report by reading
files rather than re-deriving the plan.

Run it, then read the JSONs, then fill the matching report sections. Nothing here is
reported as verified until its JSON exists and has been read.

```bash
bash tools/audit_v_battery.sh            # everything safe, resumable
bash tools/audit_v_battery.sh --only B5  # one item
bash tools/audit_v_battery.sh --arm      # include the destructive baseline re-run
```

---

## The items

| ID | JSON | Closes | Est. | Destructive? |
|---|---|---|---:|---|
| **B1** | `B1_full_smoke_battery.json` | V5 (the 361-record sweep the 45 s cap made impossible) | ~150 min | no |
| **B2** | `B2_gauge_mc_production.json` | V5/`gauge_mc` at production $L$ | ~60 min | no |
| **B3** | `B3_doublers_large_L.json` | V2.4 at $L=96,128$ | ~10 min | no |
| **B4** | *(specified, not written)* | **V4.3 — the decisive test** | — | no |
| **B5** | `B5_refold_defect_quantified.json` | V-023 | ~20 min | no |
| **B6** | `B6_su3_gauss_and_three_sector.json` | V6.4's open half | ~45 min | no |
| **B7** | `B7_f270_2x_dumps.json` | V3.4 (the 55 F270 dumps) | ~90 min | **YES — `--arm` only** |
| **B8** | `B8_drift_after_reruns.json` | V0's drift row, honestly | ~10 min | no |

**Total: ~3.5 h without `--arm`, ~6 h with.**

---

## What each JSON should contain, and what to conclude

### B1 — the full grouped battery
Per-record status across all 361 registry records. **Read for:** any record that FAILs which
the sandbox reported PASS, and the true count of drift FAILs (the report's 28 is from the
arming journal, not a fresh run). Feeds the V5 coverage table, which is currently marked
**PARTIAL** and names exactly what ran.

### B2 — `gauge_mc` at production $L$
The one channel the sandbox cannot size. **Read for:** whether the F94/F146 Monte-Carlo
results reproduce at production volume. Note V4.2 item 4: these actions are still cubic and
unstarted on the rhombic action, so a clean reproduction here is *not* evidence the action
is right — it is evidence the cubic action is self-consistent.

### B3 — doublers at large $L$
`{L: {branch: {n_zero, n_pi, zero_at_origin, omega_max}}}`. **Expected:** `n_zero == 1`,
`n_pi == 0`, `zero_at_origin == true`, `omega_max < π` at every $L$ and both branches — the
sandbox confirmed this at $L=24,36,48,64$ and odd $L=25,33$.

> **If a doubler appears at any $L$: STOP.** F250's all-$k$ gauge pole and the F69
> paired-spinor photon both rest on its absence, and D1 re-opens. That is an escalation, not
> a report line.

### B4 — the V4.3 discriminator (**specified here, deliberately not written**)

This is the single most valuable outstanding experiment and it should be built deliberately,
not lifted from a battery script the audit wrote in passing.

**The question.** Reading 1 says the $L^3$ array *is* the physical lattice, so its $L^3$
Fourier modes are the mode set and every mode sum is correct. Reading 2 says the BCC crystal
is physical and the array is an unfaithful discretisation, in which case $I_2=\langle\cot\omega\rangle$
— and hence $B$, $C$, $\lambda_6$ — is a sampling artifact whose unbiased value is exactly zero.

**Why no measurement on the current code can decide it.** The code *is* the array. Any trace
it computes is the cube sum by construction. The question is whether the array is faithful to
the crystal, which is a question *about* the code, not one the code can answer.

**What the audit established that sharpens it (V4.3a).** The walk is a *bona fide* BCC crystal
walk with lattice constant $a=2/\sqrt3$: at that $a$ the body-diagonal half-vector has length
exactly 1, the primitive cell volume is $a^3/2 = 0.7698003589 = 4/(3\sqrt3)$ — **exactly**
F267's measured cube/BZ ratio — and the reciprocal lattice constant is $4\pi/a = 2\pi\sqrt3$,
**exactly** F273's "$\sqrt3\cdot$fcc". So both readings' premises are individually correct:
Reading 1 about the computation, Reading 2 about the crystal. The cube covers 76.98% of the
true zone, and by F273 a *biased* 76.98%.

**The construction to build.**

1. Represent the BCC crystal explicitly as **two interpenetrating simple-cubic sublattices**
   (A at cubic sites, B offset by $(a/2)(1,1,1)$), each an $L^3$ array — so the state is
   $2L^3$ amplitudes, not $L^3$.
2. Implement the walk's four **tetrahedral** hops as **integer `np.roll` shifts** between the
   sublattices. No `bcc_fractional_shift`. (F267 S5: the current fractional shift spreads a
   delta over 2274 of 4096 cells at $L=16$ — it is a band-limited fractional translation, not
   a nearest-neighbour hop, which is the concrete reason the array's sites are not the walk's
   sites.)
3. Diagonalise the resulting $2\times2$ Bloch problem over the **cubic** BZ of the *sublattice*
   — which, with the 2-site basis, correctly tiles the full truncated octahedron.
4. Measure $\langle\cot\omega\rangle$ and $\langle1/\omega\rangle$ over that mode set, at
   several $L$, and check convergence.

**The verdict rule.**

| Measured $\langle\cot\omega\rangle$ | Conclusion |
|---|---|
| converges to $\approx0.221$ (the cube value) | **Reading 1** — the array is faithful, every mode sum stands, and "Brillouin zone" should be retired from the docstrings |
| converges to $0$ | **Reading 2** — $I_2$'s nonzero value is a sampling artifact; $B\to0$, $C\to0$, $\lambda_6\to0$ |

**Cross-check to run alongside:** $\langle\omega\rangle$ and $\langle1/\omega\rangle$ against
F267 S4's cube-vs-true-domain figures (1.402645 vs 1.570815, and 0.891861 vs 0.763011).

**What is at stake, quantified (V4.3c/d).** Under Reading 2: `i2_lattice` $\to0$, F95's
$B\to0$ (it is *exactly linear* in $I_2$, no residue), $C\to0$, $\lambda_6\to0$ — so
F150/F234's angle→brake arrow would return 0 against the required 0.243 and the dynamical
Landau route would be **falsified**, not merely unconstrained; F118's stabilising sextic
would vanish; F100's $\gamma(\Omega)$ chain and `photon_bound_state`'s $g_c$ would move
$\sim17\%$.

> **But the charged-lepton mass ratios survive either way, and F273 does not say so.**
> `derive_weight_as_phase.py` imports neither `i2_lattice` nor `eg_sextic`; the spectrum rests
> on $\delta^*=\tfrac29$ (exact $O_h$ representation theory) and $\eta^2=\tfrac12$, and re-ran
> live at **0.003%**. Design Decision 7 — $\delta^*$ primary, $\lambda_6$ an output — is what
> insulates it. **Reading 2 is survivable.** Build the test knowing that.

### B5 — V-023, the three live F272 refold sites
`{kernel_periodicity_2pi, vacuum_polarization_Q0.3[], self_energy_P0.2[]}`. **Read for:**
confirmation at larger $n$ that the shipped `rule−cont` and the un-refolded one diverge.

Sandbox result, for comparison — vacuum polarization at $Q=0.3$:

| $n$ | shipped | no refold |
|---:|---|---|
| 10 | $-2.018\times10^{-3}$ | $-2.018\times10^{-3}$ |
| 14 | $\mathbf{+8.578\times10^{-3}}$ ← sign flip | $-2.092\times10^{-3}$ |
| 18 | $+1.193\times10^{-2}$ | $-2.115\times10^{-3}$ |
| 22 | $+1.245\times10^{-2}$ | $-2.121\times10^{-3}$ |
| 26 | $+1.205\times10^{-2}$ | $-2.121\times10^{-3}$ |

The un-refolded branch converges monotonically to $-2.1214\times10^{-3}$; the shipped one is
**opposite in sign and 5.7× the magnitude**. Kernel periodicity residual under
$k\to k+2\pi\hat e_x$: **63.05**, not zero.

**This item measures; it does not fix.** Fixing is one line at each of
`qed_vacuum_polarization.py:292`, `qed_electron_self_energy.py:430`,
`gluon_self_energy.py:173`, with F272 as the worked precedent — then re-run F251, F258, F261,
F264, F249 and the `gluon_self_energy` leg of the $d_1$/F155/F239 chain and triage what moves.

### B6 — SU(3) Gauss law and a live three-sector run
V6.4 answered the U(1) half in the sandbox: with the state started exactly on the constraint
(E projected with the **BCC curl symbol**), the sourced residual is $1.4$–$2.5\times10^{-14}$
and **flat in $L$** from 8 to 48. **Read for:** whether the same holds for the SU(3) Gauss law
(F43/FG-7) and in a live `quark_dirac` + `gluon_sourced` + `photon_sourced` scenario.

*Hazard when writing the check:* `div_from_current(J)` returns a **Fourier-space** array while
`gauss_residual(E, rho)` expects **position-space** $\rho$. Mixing them yields a silently
meaningless number.

### B7 — the 55 F270-affected dumps (**destructive**)
F270 records that 55 tracked dumps carry an absolute gauge energy and move by **exactly 2×**
when re-run, because the ½ in $\tfrac12\sum(E^2+B^2)$ won. **Read for:** whether every one of
the 55 moves by exactly 2×. **Any dump that moves by something other than 2× is a finding.**

> **Order is always run → `--restore` → `--apply`.** An arming run rewrites committed
> baselines in place; forgetting `--restore` has silently left modified baselines twice. The
> script restores before *and* after and deliberately does **not** call `--apply` — inspect
> the journal and accept per record.

### B8 — `make drift` after the re-runs
Only meaningful once B1/B2/B7 have actually run (trap #1: never diff an artifact you did not
re-run). **Read for:** the true drift set. The sandbox's 4 files / 48 values were characterised
*without* re-running and are all explained — F162 is F272's documented single move, FG7 and
FG7b drift only below the $10^{-12}$ floor, and FA_lgt_mc moved 1.25e-3 against its own
`sem_rel` of 3.11e-3.

---

## Not in this script, and why

| Item | Why not |
|---|---|
| The `cubic.py` rename (V2.5 / P3.1 item 6) | A `git mv` is a deliberate act, not a battery step. Commands and the **corrected** blast radius are in the script's trailing comment block — the documented "8 importers plus the aliases" is right for `src/` but omits **27 import sites across 23 test files** (**V-018**) |
| Fixing V-023 | Physics. The audit's authority (§0.1) is plumbing only; B5 quantifies it instead |
| Populating `exactness` on the module registry | P6 work — needs C8.4's classification ladder. Unlike `reach` (fixed in V7.4) there is no generated artifact to read it from |
| V9.5's verification subagent | Belongs with the report, not the battery |

---

## Sandbox constraints these items exist to work around

1. **~45 s per bash call.** Everything above exceeded it. `pytest tests/casim` had to be split
   into four file groups and the gate tier into five single-`--id` batches.
2. **`casim test --id` does not accumulate** — repeating the flag silently keeps only the last
   value. Use a shell loop, not multiple flags.
3. **`git checkout -- <path>` fails on this mount** (needs `unlink`). Restore with
   `git show HEAD:<path> > <path>`.
4. **`pytest --collect-only` rewrites a tracked artifact** (`test-results/casim-exactness-inventory.md`,
   via `pytest_sessionfinish`) — **V-011**.
5. **Loading the forks runs physics and writes result JSONs** — the V5 fork-load pass rewrote
   two and they had to be restored. A live instance of `import_time_work = 320`.
