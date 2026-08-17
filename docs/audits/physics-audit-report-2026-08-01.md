# Physics Audit V — Report

*Opened 2026-07-31 - 23:40. Session `modest-beautiful-wright`, claim `audit-v` on the board.*
*Against `docs/audits/physics-audit-2026-08-01-full-rerun-prompt.md` (items V0–V9).*

**Status of this document: V0–V9 are COMPLETE. V5 is partial with its coverage stated; V4.3
is deliberately *not decided* (the audit's job was to specify the decisive test, not run it).
Two repairs were made: F276 (the `curved.py` port, under Ben's direction) and V7.4 (the
`Reach` column, which §0.1 authorises as plumbing).**

**V9.5 was run.** A verification subagent was given this report and told to find every claim
the evidence does not support. It found **16**, of which one was a genuine internal
contradiction, three were wrong numbers or wrong evidence, and the rest were overstatements
or nitpicks. **All 16 are folded in below**, each marked `[V9.5]` at the point of
correction, and its "verified and held" list is summarised at the end. The corrections it
forced are part of this report, not an appendix to it.
Every section below carries its own coverage statement. Sections with partial coverage
carry their own coverage statement, so nothing here is mistaken for a verdict that was not
taken.

---

## Executive summary

**V-Q1 and V-Q2 are both answered in the affirmative, and the evidence is algebraic rather
than sampled.** The foundation closes as a derivation with no free step — four tetrahedral
BCC hops give $u(k)$; $\det U=1$ and $\operatorname{tr}U=2u$ force $\omega=\arccos u$; the
IR slope is $1/\sqrt3$ exactly and isotropically; there are no doublers at $L=24,36,48,64$
or at odd $L=25,33$. The paired-spinor photon is massless, on-axis-luminal at every $k$
including the zone edge, transversality-preserving to $3\times10^{-16}$, and
non-birefringent **by construction** rather than within a tolerance. An independent
re-derivation reproduced F30's exact rational coefficients term for term.

The barrier reproduces: all gate-tier records pass (**26** at audit open, **27** after the F276 record), `pytest tests/casim` is
**209 passed / 2 skipped** over **211** collected, every ratchet is at or below baseline.
**No physics number was changed and no baseline was staged**; the six that this audit's
re-runs rewrote were restored from `HEAD`.

**The most serious finding is in the QED sector, and it is a repeat offence.** F272's
`% 2π` refold defect — applying a $2\pi$ wrap to a kernel whose period lattice is
$\sqrt3\cdot$fcc — was fixed in `bgfield_loop` and is **still live in three more modules**:
`qed_vacuum_polarization`, `qed_electron_self_energy` and `gluon_self_energy` (V-023). In
vacuum polarization it is not a small error: the shipped $\Delta=\text{rule}-\text{cont}$
**changes sign between $n=10$ and $n=14$** and settles at $+1.2\times10^{-2}$, where the
un-refolded calculation converges monotonically to $-2.12\times10^{-3}$ — opposite sign,
six times the magnitude. It reproduces F272's diagnostic signature exactly, at the same
$Q=0.3$. Affects F251, F258, F261, F264, F249 and the $d_1$ chain's gluon leg. Recorded,
not fixed.

**V-014 is fixed.** `lattice.curved._half_step_dH` carried both defects F271 repaired in
the production path; this audit quantified the cost (a **6.1% norm violation that 32×
sub-stepping reduced by 0.23%**) and, under Ben's direction, ported the fix. **Global order
0.00 → 2.00**; norm drift at the default $n_\text{sub}=4$ went
$4.18\times10^{-2}\to6.66\times10^{-10}$; `verify.run_all()` stays 14/14 with the
`refraction_2d` fidelity residual still exactly 0.0; **zero committed baselines move.**
Recorded as **F276**, with a gate-tier registry record — only the second in 361 to use an
`entry:` point, which incidentally un-empties the D9 bridge V-003 found vacuous.

**On the BZ question (V4.3), the audit adds an exact result and a survivability verdict it
was asked for.** The walk *is* a faithful BCC crystal walk with $a=2/\sqrt3$, and F267's
measured "cube $=4/(3\sqrt3)$ of one zone" is **not empirical — it is the primitive cell
volume**, $a^3/2=0.7698003589$ exactly. So Reading 1 is right about the computation and
Reading 2 is right about the crystal. Critically: the **charged-lepton mass ratios do not
depend on any $k$-space average** (`derive_weight_as_phase.py` imports neither `i2_lattice`
nor `eg_sextic`; re-run live at **0.003%**), so a Reading-2 outcome would falsify the
dynamical Landau route — $B$, $C$, $\lambda_6$ all → 0 — while leaving the spectrum
untouched. Design Decision 7 is what insulates it.

Two architectural findings are worth naming because they are the same defect class the
project has already decided against. `gauge.photon` **imports the canonical propagator and
never calls it**, re-implementing it inline — bit-identical, so nothing moves, but three
documents assert it *is* the shared object (V-012), which is exactly what F270 fixed for
`field_energy` six hours earlier. And result baselines **store wall-clock time**, so
`F100`'s entire measured drift was `runtime_s: 0.056 → 0.083` (V-021).

Three further things are worth Ben's attention.

**First, the tree is live under the audit.** The `cowork-p4-p5` session claimed the
program layer at 2026-07-31 - 22:45 and is actively writing to it. The constants gate was
**red** when this audit opened (V-001) and **green** forty minutes later because that
session fixed its own file mid-run; `docs/design/module-graph.json` was stale at 23:10 and
current at 23:26 for the same reason. Every measurement in this report therefore carries a
timestamp, and V9's "leave the tree clean" check will need a different formulation than
`git status` (V-010).

**Second, D9's headline mechanism is carrying almost nothing.** The claim that `pytest`
and `casim test --tier gate` "cannot diverge by construction" rests on entry-driven
registry records reaching pytest through `test_registry_entries.py`. Exactly **1 record of
360** names an `entry:`, and it is battery tier, so that parametrisation is **empty** and
the bridge is vacuous (V-003). Separately the two selections genuinely do differ: the three
`scenario` gate records — `scenario-bcc-weyl`, `scenario-gluon-bcc`, `scenario-photon-pair`
— have no path and are invisible to pytest (V-004). Those three are the *physics* gates in
the gate tier.

**Third, V1.3 closes cleanly and `check_module_registry.py` has no hole.** The roadmap's
"194 `.py` vs 178 records, 6 explained as fork `__init__` files" is stale *and* its
explanation was wrong. Measured: 194 = 181 modules + 13 `__init__.py`; the registry holds
181 records = 180 modules + `forks/__init__.py`; and the single unregistered non-init file
is `registry.py` itself, which cannot register itself. Every file is accounted for by name.

**V6 and V7 close two questions previous audits left open and find nothing that breaks.**
Gauss's law is conserved to machine precision in the **sourced** U(1) sector with a residual
that is **flat in $L$** (1.4→2.5e-14 across a 6× range) — the 2026-06-29 audit's open
question, answered. One $c$ is one object, not four agreeing numbers. One energy: `energy`
and `energy_density` return the same number and **zero of 20 channels override** the base
definition. `T00_dirac_kinetic` matches its closed form with a $k$-spread of
$4.8\times10^{-5}$, and the colour-axis fix gives exactly $3.000000\times$ — three colours
of charge, one gravitational field. Two honest "input, not derived" answers: **charge
quantisation is the SM's own $Y$ assignment written as literals** (`hypercharge.py:117-122`,
anomaly-checked but not anomaly-derived), and the **3 generations are derived** as
$\dim T_{1u}$ but conditional on a Candidate-status identification that F79 calls a
"theorem".

**V8 finds no hidden claims — but a stale public register.** Every row the 2026-06-29 audit
flagged as an omission is now **open and acknowledged**, which is the acceptable category;
`qed_amu.py`'s explicit `SCOPE — what is NOT claimed` block is the model for how the rest
should read. Two residuals moved because the *measurement* moved (V-029), and
`Claims-and-Falsifiers-Summary.md` is stale in three separate places (V-024, V-030).

**Coverage: V0–V9 complete.** V5 is partial with its coverage stated, V4.3 is specified
rather than decided by design, and the Tier-B handoff is `tools/audit_v_battery.sh` +
`test-results/audit-v/MANIFEST.md`.

---

## V-Q1 verdict — the foundation

> **SOUND. The foundation is exact, self-consistent, and is what the code computes.**
> Every link in the chain was re-derived symbolically in this session, not sampled.

The chain **4 tetrahedral hops → $u(k)$ → $\det U=1,\ \operatorname{tr}U=2u$ →
$\omega=\arccos u$ → $c_\text{lat}=1/\sqrt3$** closes with no free step:

| Link | Status | Evidence |
|---|---|---|
| $u^2+\lvert\tilde n\rvert^2=1$ | **algebraic identity**, both branches | sympy `simplify` → exactly `1` |
| $u^\pm$ is the BCC hop sum | **exact** | $\tfrac14\sum_{j}\cos(d_j\!\cdot\!k/\sqrt3)=c_xc_yc_z$ and $\tfrac14\sum_j\sin(\cdot)=-s_xs_ys_z$ over the 4 even-parity body diagonals |
| $U$ unitary, $U\in SU(2)$ | **exact** | $U^\dagger U=\mathbb 1$ symbolically; $\det U=1$; $\operatorname{tr}U=2u$ |
| $\omega=\arccos u$ **forced** | **derived, not posited** | $\lambda_+\lambda_-=1,\ \lambda_++\lambda_-=2u\Rightarrow\lambda_\pm=e^{\pm i\arccos u}$ |
| $c_\text{lat}=1/\sqrt3$ | **exact and isotropic** | $\lim_{k\to0}d\Omega/dk=\sqrt3/3$ for *every* $(\theta,\varphi)$ |
| F105 on-axis all-$k$ | **exact** | $u(k\hat x/2)=\cos\!\big(k/(2\sqrt3)\big)$, so $\arccos$ inverts it identically |
| No doublers | **confirmed on the cube, strengthened — but conditional, see `[V9.5]` below** | 1 zero (at $k=0$), 0 $\omega{=}\pi$, both branches, at $L=24,36,48,64,96,128$ **and odd $L=25,33$** |

**D1 does not re-open. F250's all-$k$ gauge pole and the F69 photon are untouched.** No
escalation.

Two things the audit adds that were not previously established:

- The unitarity identity is now **algebraic**, where `bcc.py` only claimed numerical
  evidence ("100 random k's give max residual 4.4e-16"). The transcription typo the code
  guards against is likewise shown to fail *identically*, not just numerically.
- `bcc_dispersion` is **the algebraic consequence**, not a separately-written expression
  that merely agrees: it computes $\arccos$ of the same $u$ the unitary is built from, and
  `bcc_dispersion` $\equiv\arccos(\tfrac12\operatorname{tr}U)$ to **0.0 exactly** over 2000
  random $k$ on both branches.

**One qualification on the prompt's framing.** V2.3 is described as "what makes the photon
luminal at every wavenumber rather than only in the IR". Measured, that is true **only
along a lattice axis**. Off-axis the photon is subluminal at $O(k^2)$: $-8.7\times10^{-4}$
on the face diagonal and $-1.5\times10^{-3}$ on the body diagonal at $\lvert k\rvert=0.5$,
rising to $-3.3\times10^{-2}$ and $-5.6\times10^{-2}$ at $\lvert k\rvert=3$. F105's own
consequence #3 states this correctly; the gloss overreaches.

## V-Q2 verdict — the photon construction

> **SOUND on physics. One architectural defect and one drifting baseline, neither of
> which moves a number.** The paired-spinor photon is massless, on-axis-luminal,
> transversality-preserving and non-birefringent *by construction*, and survives
> F265/F270/F271/F272/F273 intact.

| Property | Verdict | Evidence |
|---|---|---|
| $\Omega_\text{pair}=\Omega_\text{even}$ | **exact, symbolically, all $k$** | $\Omega_\text{pair}-\Omega_\text{even}$ simplifies to `0`; rests on $\omega^+(-k)=\omega^-(k)$, also verified symbolically |
| massless | **exact** | $\Omega(0)=$ `0.0` exactly; exactly one $\Omega{=}0$ mode at every $L\in\{8,16,24,32,48\}$ |
| luminal | **exact on-axis, all $k$ incl. zone edge** | $\max\lvert\Omega-\lvert k\rvert/\sqrt3\rvert=6.7\times10^{-16}$ at $L{=}16,32$; $9.2\times10^{-16}$ at $L{=}64$ |
| transverse | **preserved exactly** | $(\operatorname{div}E,\operatorname{div}B)$ obeys the *same* $R(\Omega)$, residual $3.0\times10^{-16}$ |
| non-birefringent | **derived, not measured** | the pair has **one** single-valued $\Omega$; there is no second branch to split from |
| norm conservation | **machine** | $1.2\times10^{-14}$–$5.6\times10^{-14}$ over 200 ticks, $L=13,17,25$ |

**Non-birefringence is structural, and that is the right kind of claim.** It does not need
a tolerance because there is no quantity to bound: a single-valued $\Omega_\text{pair}(k)$
admits no splitting. What *would* make it birefringent is the retired assignment
helicity↔branch, which gives $\Omega^\pm=2\omega^\pm(k/2)$ and a genuine split. The module
keeps that as an explicit contrast diagnostic, `pair_birefringence()`, which on the $L{=}32$ cube ranges over $[-2.03,\,+2.13]$ `[V9.5]` — good practice: the excluded alternative is kept computable next to
the adopted one.

**Independent confirmation of F30.** Expanding the single branch along the body diagonal
this session gives $\omega^\pm=\tfrac{\sqrt3 k}{243}(81\mp9k-2k^2)$; substituting into
$\Omega^\pm=2\omega^\pm(k/2)$ reproduces F30's exact rationals
$\tfrac{k}{\sqrt3}-\tfrac{\sqrt3}{54}k^2-\tfrac{\sqrt3}{486}k^3$ **term for term**. The
mechanism is worth stating plainly because it is the quantitative content of "the pair is
the photon": the branch-odd terms are **equal and opposite**, so they cancel exactly in the
sum. Measured convergence orders on the body diagonal — single branch $1.02$–$1.06$, pair
**$2.000$ at every refinement**.

**The two things that are wrong, and neither is a number:**

- **V-012 (architectural).** `gauge.photon` **imports `_f26_rotation_step` and never calls
  it**; `photon_step_spectral` re-implements the rotation inline. The two are
  **bit-identical** (`array_equal` → `True`), so no result moves — but Design Decision 5,
  `key-decisions.md` and the module's own docstring all assert the propagator *is*
  `_f26_rotation_step`, and at code level it is an agreeing copy. This is precisely the
  defect class F270 fixed for `field_energy` six hours earlier, surviving in the more
  load-bearing of the two objects.
- **V-013 (baseline).** `F87-charge-coupling-paired-photon` **FAILS** on re-run. Fully
  characterised below: all 26 deltas are FFT round-off or **stored wall-clock time**. Every
  physics observable reproduces to $10^{-16}$. Recommended verdict: **accept**.

---

## Starting state (measured, vs claimed)

All measurements 2026-07-31, 23:00–23:30 local, at git `HEAD = 5b5c307` with the C9
restructure **uncommitted** in the working tree. Environment: CPython 3.10.12, numpy
2.2.6, scipy 1.15.3, from `.vendor/py310-linux-aarch64`.

| Quantity | Claimed | Measured | Verdict |
|---|---|---|---|
| `make gate` checks green | 14 | **13 green, 1 red at open → 14 green at 23:14** | see **V-001** |
| `pytest tests/casim` | 176 passed / 2 skipped | **209 passed / 2 skipped**, 211 collected | drifted up; 23 files |
| `casim test --tier gate` | — | **26 records, 26 PASS** (run in slices) | ✔ |
| `casim index --check` | clean | **clean** (rc=0, 5.2 s) | ✔ |
| `make drift` | no tracked JSON differs | **4 files, 48 values differ** | all four explained — see below |
| engine modules registered (D11) | 178 (194 `.py`, reconcile) | **181 records; 194 `.py` = 181 modules + 13 `__init__`** | ✔ reconciled, **V1.3** |
| module graph engine nodes | 184 | **187** | **V-006** |
| test registry records | 356 | **360** | drifted up |
| gate-tier records | 22 | **26** | drifted up |
| findings / max / duplicates | 268 / F273 / 0 | **268 / F273 / 0** at 23:05 → **270 / F275 / 0** at 23:33 | matched at open; **moved during the audit** — see V-001 |
| scenarios | 46 | **48** `.yaml` | drifted up |
| result artifacts | 394 | **396 git-tracked** (+2 untracked, +58 ignored) | ✔ |
| constants registered (D7) | 43 + 10 `MeasuredConstant` | **43 + 10** (strong 25, geometry 7, lepton 7, EW 2, gravity 2) | ✔ exact match |
| rogue literals in `src/` | 0 | **2 at 23:05 → 0 at 23:14** | **V-001** |
| `import_time_work` | 320 | **320** | ✔ unmoved, still unmet |
| `legacy_script` (declared debt) | 47 | **47** | ✔ |
| drift FAILs outstanding (P1r.2) | 28 (+23 undecided) | **28 FAIL / 174 PASS / 12 ERROR / 11 SKIP / 1 STALE** over 226 journalled | ✔ exact match |

Supplementary ratchet readings, all `ratchet OK`:

| Ratchet | Value | Baseline |
|---|---:|---:|
| direct `np.fft` transform calls in `src/` | 0 | 0 |
| device-namespace fft calls | 8 | 8 |
| files importing numpy | 165 | 165 |
| files importing scipy | 7 | 7 |
| `no_assert` | 231 | 231 |
| `unfalsifiable` | 70 | 70 |
| `import_time_work` | 320 | 320 |
| rogue literals, `tests/` backlog | 272 | counted, not gated |
| recorded `literal` sites | 13 | all in `tests/` |

### `make drift` — the four files, characterised

Applying trap #1 (**nothing here was re-run by this audit**; these are pre-existing
working-tree states relative to `HEAD`) and trap #2 (the `machine` floor is $10^{-12}$;
`check_result_drift.py` is strict at $10^{-15}$ and disagrees on purpose).

| File | Move | Reading |
|---|---|---|
| `F162_bgfield_loop.json` | `G2…rule_shift_mean` −0.005071300575511986 → −0.012591048743328725 | **Documented.** Exactly the single number F272 says moves. Awaiting a deliberate `git add` by Ben — not this audit's to stage |
| `FG7_gluon_dynamics.json` | 3 residuals, 2.6e-15 → 3.4e-16, 7.1e-15 → 8.2e-15, 1.8e-13 → 1.1e-13 | **Below the machine floor.** Relative deltas of 13–87 % on absolute magnitudes of $10^{-13}$–$10^{-16}$. Noise, not physics |
| `FG7b_gradient_flow.json` | 3 residuals at $10^{-14}$, plus `results[5].residual` 4.941846e-10 → 4.942069e-10 | First three below the floor. The fourth is above it in absolute terms but moves by **4.5e-5 relative** — flagged, not adjudicated |
| `FA_lgt_mc.json` | 18 changed, 22 added | **Statistically consistent re-run.** The added keys are a 6-chain ensemble with `sem`/`sem_rel`; `beta=5.7.plaq` moves 1.25e-3 relative against a new `sem_rel` of 3.11e-3 — inside one standard error |

No baseline was staged, restored or rewritten by this audit.

---

## Critical issues — blocks a physics claim

### V-023 — F272's refold defect is live in three more modules; in vacuum polarization it flips the sign of the measured quantity

Full characterisation under **V4.4**. In brief: `((k+π) % 2π) − π` is applied to kernels
that are **not** $2\pi$-periodic (measured residual **63.05**) in
`qed_vacuum_polarization.py:292`, `qed_electron_self_energy.py:430` and
`gluon_self_energy.py:173`. The shipped $\Delta=\text{rule}-\text{cont}$ for vacuum
polarization **changes sign between $n=10$ and $n=14$** and settles at
$+1.2\times10^{-2}$; with F272's fix applied in memory it converges monotonically to
$-2.1214\times10^{-3}$ — **opposite sign, ~6× the magnitude**. Affects F251, F258, F261,
F264, F249 and the `gluon_self_energy` leg of the $d_1$ chain. **Not fixed** — the fix is
physics and only the `curved.py` port was authorised. Highest-priority item found.

### V-014 — resolved this session (F276)

Was: a 6.1% norm violation that sub-stepping could not remove, under every F64-fork
variable-$c$ result. **Fixed under Ben's direction** — see the F276 section. Global order
went **0.00 → 2.00** and norm drift at the default `n_sub=4` went
$4.18\times10^{-2}\to6.66\times10^{-10}$.

### V-024 — a superseded prediction is still live in the claim register

`papers/Claims-and-Falsifiers-Summary.md` still lists the horizon-free black hole and the
+4.63% shadow as current claims **and as live falsifiers**, three weeks after F178
superseded them and while the engine modules carry the F178 banner. Detail under **V5**.

Remaining, neither of which moves a number: **V-012** (the duplicated photon propagator,
bit-identical) and **V-013** (a drifting baseline that is noise, recommended verdict
*accept*).

---

## Algebraic and mathematical errors

**None found in V2 or V3.** Every algebraic claim checked reproduced, and two were
*upgraded* from numerical to algebraic:

- `bcc.py`'s unitarity correction (the $n_y$ sign typo) is now shown to fail
  **identically**, not merely at $4.7\times10^{-1}$ on 100 samples.
- F105's on-axis exactness is now a one-line algebraic inversion,
  $u(k\hat x/2)=\cos(k/(2\sqrt3))$, valid for $k\le 2\sqrt3\pi\approx10.88$ — the whole FFT
  cube and well beyond it.

An independent re-derivation of F30's body-diagonal series reproduced its exact rational
coefficients term for term.

V4 and V7 are covered in their own sections below; nothing there adds an algebraic error `[V9.5]`.

### V-015 — a numerical-conditioning hazard at the exact point $c_\text{lat}$ is defined

`bcc_dispersion` returns `arccos(u)`, and $\arccos$ is ill-conditioned as $u\to1$, which is
$k\to0$ — the IR limit in which $c_\text{lat}=d\Omega/d\lvert k\rvert$ is *defined*.
Measured on-axis, where the exact answer is known:

| $k$ | $1-u$ | $\arccos$ route error | `atan2(\|n\|,u)` route error |
|---|---|---|---|
| $10^{-6}$ | $4.2\times10^{-14}$ | $2.3\times10^{-10}$ | **0.0** |
| $10^{-4}$ | $4.2\times10^{-10}$ | $2.4\times10^{-12}$ | **0.0** |
| $10^{-2}$ | $4.2\times10^{-6}$ | $2.0\times10^{-14}$ | **0.0** |
| $10^{-1}$ | $4.2\times10^{-4}$ | $3.5\times10^{-15}$ | **0.0** |

At $k=10^{-6}$ the error is **three orders above the $10^{-12}$ machine gate**. The
`atan2` form uses the same $u$ and $n$ the module already computes and is exact at every
$k$ tested.

**Exposure is real but currently bounded.** On an FFT grid the smallest non-zero mode is
$2\pi/L$, so at $L=16..64$ the error is $6.7\times10^{-16}$–$1.5\times10^{-15}$ — below the
floor, and no shipped result I could identify is affected. The exposure is in *analytic*
small-$k$ sweeps and slope fits, which is where a $c_\text{lat}$ determination would live.
Recorded as a latent hazard with a derived fix, not as a defect in a result. This is
exactly the case D8's "own the primitive when the vendored one misbehaves" was written for.

---

## Logical gaps — "derived" claims that are assumed

### V-003 — D9's `entry:` contract is carried by 1 record in 360, and the pytest bridge it feeds is empty

`CLAUDE.md`, D9 in `key-decisions.md`, and roadmap §2.2 all describe entry-driven records
as the working convention: *"A new test is a **record**, not a file that executes physics
at import. Give it a `module:`, an `entry:` function, `params:`, a `kind:` …"* and
*"`tests/casim/test_registry_entries.py` **parametrises** over the same records `casim
test` runs, so the two cannot diverge."*

Measured:

```
records with entry:  1  of 360   (tier: battery)
gate-tier records with entry:  0
```

`test_registry_entries.py::pytest_generate_tests` selects
`[r for r in select(tier="gate") if r.entry]` — an **empty list**. Pytest reports the
resulting item as *skipped*; the file contributes `1 passed, 1 skipped`, and the one that
passes is the unrelated ambiguity check. So the bridge that is supposed to make the two
runners identical **carries zero records today**.

This is not a broken test — it is a claim about the architecture that the tree does not
support. The 360 records break down as 217 `result_dump`, 93 `assertion` (all of which are
ordinary pytest files), 47 `legacy_script` and 3 `scenario`. "Physics-at-import is
impossible by construction" is therefore not what is holding `import_time_work` at 320;
that number is held by ordinary pytest files, which is consistent with its being stuck.

**Recommended:** either populate `entry:` on the records that would benefit, or amend the
three documents to say what the tree actually does. The audit has no authority to choose;
the misleading part is that all three read as description rather than aspiration.

### V-004 — `pytest` and `casim test --tier gate` do not select the same objects

The prompt (V1.2) asks for this to be verified empirically rather than accepted
structurally. Done, by set comparison of collected file paths against gate-record paths:

```
pytest tests/casim  → 23 files
gate-tier records   → 26 records
in gate, not in pytest:  scenario-bcc-weyl, scenario-gluon-bcc, scenario-photon-pair
in pytest, not in gate:  (none)
```

The 23 pytest files map one-to-one onto the 23 `assertion` gate records. The three missing
records have `path: None` because they are `kind: scenario` — a YAML run with `expect:`
gates, which pytest has no way to collect. `pytest` therefore runs **23 of 26** gate
records, and the three it omits are precisely the ones that run the engine on a lattice
(`bcc_weyl`, `gluon_bcc`, `photon_pair`).

**Consequence:** `pytest` alone is not the barrier. `make gate` is, because it invokes
`casim test --tier gate`. Anyone relying on a bare `pytest` — the documented default
target — is skipping the three physics gates. This should be stated in `CLAUDE.md`, which
currently says *"`casim test --tier gate` — what `pytest` runs, by construction."*

---

## V2 — the foundation, item by item

### V2.1 — unitarity forces the dispersion ✔

Re-derived in sympy, not numerically.

1. **$u^2+\lvert\tilde n\rvert^2=1$ is an identity**, both branches — `simplify` returns
   exactly `1`. The code's own comment claims only numerical evidence; this upgrades it.
2. **The transcribed $n_y$ fails identically.** With the overview's typo, the residual
   simplifies to a non-zero sum of four sines, so the correction `bcc.py` applies is
   forced, not fitted.
3. **$U^\dagger U=\mathbb 1$ symbolically; $\det U=1$; $\operatorname{tr}U=2u$.** Hence
   $\lambda_\pm$ satisfy $\lambda_+\lambda_-=1$ and $\lambda_++\lambda_-=2u$, so
   $\lambda_\pm=u\pm i\sqrt{1-u^2}=e^{\pm i\arccos u}$. **$\omega=\arccos u$ is forced.**
4. **$u$ is a genuine BCC hop sum.** Over the four even-parity body diagonals $d_j$,
   $\tfrac14\sum_j\cos(d_j\!\cdot\!k/\sqrt3)=c_xc_yc_z$ and
   $\tfrac14\sum_j\sin(d_j\!\cdot\!k/\sqrt3)=-s_xs_ys_z$, so
   $u^\pm=\tfrac14\sum_j\big[\cos(d_j\!\cdot\!k/\sqrt3)\mp\sin(d_j\!\cdot\!k/\sqrt3)\big]$.
   The $1/\sqrt3$ in the argument is exactly what makes the body diagonal a **unit-length
   hop**. Verified against the code to $9.2\times10^{-16}$.

Cross-checks against the shipped code, 2000 random $k$, both branches: sympy vs
`_bcc_uvec` $1.3\times10^{-15}$; $\lvert U^\dagger U-\mathbb 1\rvert$ $5.6\times10^{-16}$;
$\lvert\det U-1\rvert$ $5.6\times10^{-16}$; `bcc_dispersion` vs
$\arccos(\tfrac12\operatorname{tr}U)$ **exactly 0.0**.

**Verdict: `bcc_dispersion` is the algebraic consequence.** Sign convention matches F26.

### V2.2 — $c_\text{lat}=1/\sqrt3$ ✔ with one gap in the guardrails

$\lim_{k\to0}\tfrac{d}{dk}\big[2\omega^+(k\hat n/2)\big]=\sqrt3/3$ symbolically **for a
generic direction $(\theta,\varphi)$** — so the IR limit is not merely correct on-axis, it
is exactly **isotropic**. Same for the $-$ branch and for $\Omega_\text{even}$.

Registry: `c_lat` resolves from `1.0 / math.sqrt(3.0)` — closed form, not a truncated
decimal — with `exactness=exact`, `provenance=('F26',)`, a full derivation string, and 23
recorded sites. ✔

**The two deliberately-separate $1/\sqrt3$ constants are still separate** — `c_lat`
(geometry, a speed) and `q_star_a_band_lo` (strong, a momentum scale), each with its own
provenance and derivation, and **two of the four** call sites that import the latter carry the comment "1/sqrt3, **not** c_lat" `[V9.5]` — so the separation is held by discipline on half the sites. ✔

### V-016 — but no test guards the $1/\sqrt3$ pair, and the prompt assumed one does

V2.2 asks to "confirm that test runs". It does not exist.
`test_the_three_hard_cases_stay_separate` asserts the three $f_\pi$, the two
$\sin^2\theta_W$, the two $\cos3\delta^*$ and — with a dedicated set comparison — the
**three-fold $2/9$ split**. It says nothing about $1/\sqrt3$. Grepping the whole tree,
`q_star_a_band_lo` appears in **zero** test files.

So of the five deliberate pluralities, four are gated and one is held by discipline alone.
Collapsing `q_star_a_band_lo` into `c_lat` would turn an F151 matching-scale *prediction*
into the lattice light speed *by definition*, and nothing would go red. Recommended fix is
one assertion; **not applied here**, because a gate-tier test file is the `tests` claim's
and the audit's authority to add tests should not be exercised silently on the barrier.

### V2.3 — F105, all-$k$ on-axis ✔ and now algebraic

On-axis $c_y=c_z=1$, $s_y=s_z=0$, so $u(k\hat x/2)=\cos\!\big(k/(2\sqrt3)\big)$ and
$\arccos$ inverts it exactly for $k\le2\sqrt3\pi\approx10.88$. Measured:

| Check | Result |
|---|---|
| dense sweep, $k\in[0,\pi]$, 20001 pts | max abs err $2.1\times10^{-12}$ (all of it at the single point $k=1.6\times10^{-4}$ — see **V-015**); median $2.2\times10^{-16}$ |
| dense sweep, $k\in[0,10.87]$ | max abs err $1.2\times10^{-13}$ |
| the FFT axis grid, $L=16,24,32,48,64$ | $6.7\times10^{-16}$ – $1.5\times10^{-15}$ |
| each branch separately | $2.4\times10^{-13}$ |

**Exactness class: `exact` algebraically, `machine` numerically.**

### V-017 — F105 has no test of its own

The prompt calls this "the single most load-bearing exactness claim in the lattice sector".
It has **no registry record**. `F105` appears only as a *finding tag* on
`F129-blockspin-free-photon` and `F227-decoherence-floor`, neither of which asserts the
on-axis identity. The claim reproduces (above), but nothing in the suite would notice if it
stopped. A one-record `assertion` with `expect: {exactness: machine}` would close it.

### V2.4 — doublers ✔ and the check was strengthened

F267's S3 reproduces exactly: **1 zero, 0 $\omega{=}\pi$**, both branches, $L=24,36,48$.
This audit extended it three ways, all clean:

- **$L=64$** — same.
- **odd $L=25,33$** — same, so the count is not an even-$L$ artifact.
- **the zero is *located*, not just counted** — it is at $k=(0,0,0)$ in every case. The
  shipped `s3_weyl_points` only counts; a single zero in the *wrong* place would pass it.

Two structural readings fall out, both supporting F267/F273:

- Max $\omega$ on the $L=48$ cube is **3.1136 $<\pi$** — the zone-edge value is approached
  but never reached inside the cube.
- $\omega^\pm=\pi$ **exactly** at $k=(\sqrt3\pi,0,0)$, which is **outside** the cube.

### `[V9.5]` — and the second of those is a caveat, not just confirmation

The verification pass caught what the first draft of this section missed, and it is
material. At $a=2/\sqrt3$ the BCC $\Gamma$–H distance is $2\pi/a$, and

$$\frac{2\pi}{a}=\pi\sqrt3=5.441398\ldots=\text{the }k\text{ at which }\omega^\pm=\pi.$$

Verified to $<10^{-12}$. So the $\omega=\pi$ point is not merely "outside the cube" — **it
sits exactly on the H point of the walk's true Brillouin-zone boundary**.

**Therefore the no-doubler verdict is conditional on Reading 1.** Counting $\omega=\pi$
modes *over the cube* returns zero, and that is the correct count if the cube is the mode
set. Over the **true** zone there is a zone-boundary $\pi$-mode at H, which under the same
criterion this audit applied is exactly what a doubler check is looking for.

This does **not** change the operational conclusion — every observable in the tree is
computed on the cube, so F250's all-$k$ gauge pole and the F69 photon are untouched **as
computed** — and it is not an escalation. But "there are no doublers" should be written as
**"there are no doublers on the FFT cube"**, and whether that is the physically meaningful
statement is V4.3's undecided question. The two items are not independent, and the first
draft treated them as if they were.

**No escalation. Caveat recorded.**

### V2.5 — the cubic reference layer

| Sub-item | Verdict |
|---|---|
| Banner present and accurate | ✔ at module level on `core.py` and `core_exact.py`, and on `geometry.cubic()`. `geometry.square()` carries only an indirect pointer ("reference geometry; see cubic()"). **No per-function banner** on `core.py`'s 20 public entry points, so `from …core import weyl_step_3d` shows a caller nothing |
| Cubic kernels reproduce their regression targets | ✔ `exact2d_unitarity_residual` = **0.0 exactly**; `exact2d_a0_check` = identity; norm drift $1.8\times10^{-14}$/200 steps; small-$k$ Weyl residual converges at order **2.000** |
| BCC side, same checks | ✔ `bcc_unitarity_residual` = **0.0 exactly**; `a0_check` identity; norm drift $4.1\times10^{-14}$/200 steps |
| Rename to `cubic.py` still outstanding | ✔ confirmed outstanding |

### V-018 — the `git mv` handoff undercounts its own blast radius by a factor of four

The prompt (and the F272 session's handback) name "**8 importers** plus the
`ca_core`/`ca_core_exact` aliases". Measured, that is exactly right **for `src/`**: 8
importers under `src/casim/engine/` plus 2 alias lines in `src/casim/lattice/__init__.py`.

It omits **`tests/`, which holds 27 import sites across 23 files** — 11 in `tests/findings/`, 2 in `tests/priority/`, 14 in `tests/runners/` `[V9.5]`. A `git mv` that repoints only the
documented 8+2 leaves 23 test files broken on the next run. `tools/` is clean (0).

Corrected handoff is in `tools/audit_v_battery.sh`.

### V-019 — `bcc_smallk_to_weyl_residual`'s docstring contradicts F30

It says: *"Expected to scale as O(\|k\|²) — the leading correction … is the diffusion
term."* Measured, the **single-branch** residual it computes scales as **O(\|k\|¹)**:
orders $0.967,\ 0.984,\ 0.992$ over $k=0.2\to0.025$. The $O(k^2)$ statement is true of the
**pair**, not of a branch — which is F30's entire result. The 2D reference converges at
order **2.000**, which is presumably where the expectation came from.

Documentation defect inside the canonical lattice module; fix is one sentence.

### V2.6 — cubic ↔ BCC where they overlap

They do not overlap in observables — the 2D square core runs at $1/\sqrt2$ and BCC at
$1/\sqrt3$. The genuine shared target is the **continuum limit**, and both reach it:

| Layer | emergent $\omega/\lvert k\rvert$ at $\lvert k\rvert=10^{-4}$ | target | dev |
|---|---|---|---|
| 2D square | $0.7071067792$ | $1/\sqrt2=0.7071067812$ | $2.0\times10^{-9}$ |
| BCC 3D (body diag) | $0.5773438704$ | $1/\sqrt3=0.5773502692$ | $6.4\times10^{-6}$ |

The BCC deviation is **not** round-off: it is the genuine $O(k)$ body-diagonal term,
$-a/3$ with $a=k/3$, predicting $-1.1\times10^{-5}$ against $-1.1\times10^{-5}$ measured.

**The pattern is $1/\sqrt d$** — $d=2\to1/\sqrt2$, $d=3\to1/\sqrt3$ — as `bcc.py`'s own
docstring says ("$H_W=(1/\sqrt d)\,\sigma\cdot k$").

Where they genuinely disagree, the registry already records it as a **negative result**:
`curl_fork_cubic.py` carries a `MeasuredConstant` of value $1.0$ with the reason *"this
fork exists to check whether cubic reproduces the BCC $1/\sqrt3$, and the finding is that
it does not."* That is the right way to hold it, and the physics claim rests on BCC (D1).

### V-020 — a `MeasuredConstant`'s justification does not reproduce its own value

`measured.py`, the `derive_velocity_addition.py` record: *"the emergent speed is
**1/sqrt(2d)** with d = 2"*. But $1/\sqrt{2\cdot2}=0.5$, while the registered value is
$1/\sqrt2=0.7071$. The correct formula is $1/\sqrt d$, which is what every other document
uses and what reproduces both registered values. The same wording is repeated in the
sibling `test_SR5_photon_frame_invariance.py` record by reference.

The *value* is right; the *reason string* is wrong, and under D7 the reason string is the
justification that makes the plurality legitimate. One-word fix.

---

## V3 — the photon, item by item

### V3.1 — $\Omega_\text{pair}=\Omega_\text{even}$ ✔; the propagator identity ✘

**Symbolically exact.** $\Omega_\text{pair}-\Omega_\text{even}$ simplifies to `0` for all
$k$, resting on $\omega^+(-k)=\omega^-(k)$, itself verified symbolically. Not sampled.

**The propagator is a copy, not the object** — see **V-012**. `photon_step_spectral` does
not call `_f26_rotation_step`; the import at `photon.py:53` is never used. On a random
$L=12$ field the two agree **bit-identically**, so no result moves.

### V3.2 — non-birefringence is *derived* ✔

Established structurally, not numerically: the pair carries a **single-valued**
$\Omega_\text{pair}(k)$, so no splitting exists to bound. The correct assertion is
therefore not "zero within tolerance" but "there is one dispersion", and that is what the
construction gives.

What would make it birefringent is precisely the retired helicity↔branch assignment,
$\Omega^\pm=2\omega^\pm(k/2)$, whose split is $-\sqrt3k^2/27$, i.e. $\Delta v/c=-k/9$,
**linear in $k$** — the F30/F65/F66/F67 exclusion. The module retains this as an explicit
diagnostic (`pair_birefringence`, $[-2.03,+2.13]$ on the $L{=}32$ cube) `[V9.5]`, correctly labelled as "what
the pair does NOT have".

### V3.3 — massless, luminal, transverse ✔

- **Massless.** $\Omega_\text{pair}(0)=$ `0.0` exactly; exactly one zero mode at
  $L=8,16,24,32,48$; $\Omega_\max=2.5916<\pi$ on the cube at every $L$.
- **Luminal on-axis at all $k$ including the zone edge.** At $k=-\pi$ (the edge bin),
  $\Omega=1.8137993642$ against $\lvert k\rvert/\sqrt3=1.8137993642$.
- **Off-axis it is not**, and this is the honest statement: $-8.7\times10^{-4}$ (face diag) / $-1.5\times10^{-3}$ (body diag) at $\lvert k\rvert=0.5$, growing to
  $-3.3\times10^{-2}$ / $-5.6\times10^{-2}$ at $\lvert k\rvert=3$. All **subluminal**,
  consistent with F30.
- **Transversality is preserved exactly, and structurally.** In $k$-space the step is
  $R(\Omega(k))\otimes\mathbb 1_3$ — a scalar rotation identical on all three polarisation
  components — so $(\operatorname{div}E,\operatorname{div}B)$ obeys the *same* rotation.
  Verified directly: $\lvert\operatorname{div}_\text{after}-R(\Omega)\operatorname{div}_\text{before}\rvert$
  $=3.0\times10^{-16}$ at $L=13$ and $L=16$. Transverse initial data at odd $L=13,17,25$
  stays transverse ($1.3\times10^{-15}\to6.6\times10^{-14}$ over 200 ticks) with norm drift
  $1.2$–$5.6\times10^{-14}$.

  **The propagator preserves transversality; it does not enforce it.** A longitudinal seed
  stays longitudinal. That is correct behaviour for a scalar rotation and is worth stating,
  because "the photon is transverse" is a property of the initial data plus Gauss's law,
  not of this step.

  *Harness note, recorded because it cost time and is a real lattice hazard:* at **even
  $L$** a naive $k$-space transverse projection breaks Hermitian symmetry at the Nyquist
  bin ($k_x=-\pi$ has no $+\pi$ partner, and the projector $k_ik_j$ changes sign across the
  aliasing), so taking `.real` leaks $\sim0.75$ of the field. This is the same "Nyquist-bin
  correction for even-length grids" that `weak_wmu._chiral_dispersions` already names. The
  engine handles it; an ad-hoc analysis script will not.

### V3.4 — the four things that changed under the photon

**F270 (energy convention) — ✔ all three sub-claims.**
(a) `coupled.field_energy` **is** `channel.field_energy` — the same function object
(`is` → `True`), defined once at `channel.py:19`. Not two agreeing copies.
(b) The 55-dump $2\times$ claim is **Tier B**, deliberately not re-run here: re-running
would rewrite 55 committed baselines, and the audit may not stage them. In the handoff.
(c) The supersession record `S9-P3.5-one-gauge-energy-convention` exists and is accurate,
including the deliberately-empty `superseded:` list and its explanation.

**F271 (k-resolved dielectric) — ✔ all four claims, re-measured independently.**

| Claim | Claimed | Measured |
|---|---|---|
| uniform $K$ is exact | $\sim4\times10^{-15}$ | **0.0** at $K=1.0$ and $K=2.0$; $4.0\times10^{-15}$ at $K=1.3$ |
| norm drift converges as $1/n^3$ | converges | ratios per doubling **8.01, 8.00, 8.00, 8.00** — $6.7\times10^{-6}\to1.6\times10^{-9}$ |
| Strang order | 2.00 | **1.945, 1.974, 1.988, 1.997** → 2 |
| no free parameter | none | signature is `(E, B, K, dt=1.0, n_sub=4)` — no $\omega_0$ ✔ |

The honest refusals held: the gradient-index test still asserts direction, linearity and
the exact-zero baseline only, and has **not** been tightened onto 1.25.

**F271 handoff (unfixed) — ✘ confirmed still present, and now quantified. → V-014.**

**F272/F273 (BZ reclassification) — `photon_bound_state`'s two sites, classified.**
Both are `np.mean(1/(E-T))` and `np.mean(1/(E-E_b))`, at `photon_bound_state.py:105` and
`:142`, and both are labelled $\langle\cdot\rangle_\text{BZ}$ in the docstring.
**Classification: mode sum.** The bound-state condition
$1=g\sum_p 1/(E_0(p)-E_b)$ is a sum over the *available intermediate two-particle states*
of a Hamiltonian defined on the $L^3$ array; each grid mode is one distinct state, counted
once. The cube is correct by construction and **nothing should be multiplied**. The label
is wrong — "BZ" should be retired from both docstrings, exactly as F273 predicted for
F100 and confirmed for `i2_lattice`. This is a third independent chain showing the same
mislabelling, and it closes the two sites the prompt asked for first.

**Note on stakes:** these are $\langle1/E\rangle$ moments, and F267 measured the cube
grid-mean carrying **16.9% high** on $\langle1/\omega\rangle$ against a true
fundamental-domain mean. So under Reading 2 the critical coupling $g_c$ would move by
$\sim17\%$. Under Reading 1 — which the mode-sum classification selects — it does not move
at all.

### V-014 — the F64 fork's variable-$c$ stepper is not unitary, and sub-stepping cannot fix it

F271 handed back that both defects it fixed are still in `lattice.curved._half_step_dH`.
**Confirmed by reading and by measurement**, and the second half is new:

- **Defect (i), asymmetric ordering.** The code applies `dc * dt * sg_f` — $\delta c(x)$
  *after* the derivative — which is the non-self-adjoint ordering. F271's fix is the
  Weyl-symmetric $\tfrac12(\delta\Omega+\Omega\delta)$.
- **Defect (ii), first-order Taylor.** `ψ → ψ − iδH dt ψ`. The module's own docstring
  concedes *"not exactly unitary"*. The exact form $\exp(hMJ)=\cos(hM)+\sin(hM)J$ is
  derivable, as F271 showed.

Measured on `weyl_step_2d_varc_strang`, $L=64$, 20 ticks, $\delta c=0.05\tanh(x/8)$, from a
**zero-momentum** Gaussian packet:

| `n_sub` | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| norm drift | 6.082e-2 | 6.075e-2 | 6.072e-2 | 6.070e-2 | 6.069e-2 | 6.068e-2 |

**A 6.1% norm violation that 32× sub-stepping reduces by 0.23%** — the plateau signature of
defect (i), and three to four orders worse than the $1.1\times10^{-5}$ plateau F271
measured in the production path before fixing it.

> `[V9.5] — reconciling this with the F276 table.` The F276 section's pre-F276 column reads
> **4.314e-2 → 4.146e-2** for a configuration described identically. The two are not the
> same run: this table starts from a **zero-momentum** packet, the F276 table from the same
> packet carrying $e^{i0.4x}$ (which is what `f276_convergence_check` uses, so that the
> registry record and the reported table agree). Both plateau — ratios 1.00 either way —
> and the plateau, not the magnitude, is the diagnostic. The first draft implied one
> measurement where there were two, and the "6.1%" headline in the executive summary and
> the F276 finding file inherits that ambiguity. **The magnitude is configuration-dependent
> and should always be quoted with its initial data.**

**What it means for the published numbers.** Every F64-fork variable-$c$ result — Snell,
the gradient-index bend, and the unstarted deflection-coefficient confrontation against
$4GM/c^2b$ — runs on a stepper that does not conserve norm and is first order in the
perturbation where second order is derivable. Those results are not thereby wrong; they are
**unquantified**, because no F64-fork result reports the norm drift of the run that
produced it. The fix already exists in the tree, in `gauge.photon`. This is the highest
item on my recommended list.

### V3.5 — block-spin ✔ the refusal is intact; the sourced question stays open

The F271 honest refusal is a **hard `NotImplementedError`**, not softened to a warning, at
`core/channels.py:75`, firing whenever `read_K` is non-`None` and `block > 1`, with a
message that names why ($\Omega_b(\kappa)=\Omega(\kappa/b)$ and the dielectric's
coarse-graining have not been shown to commute; F133 covers the free rule only). ✔

**The 2026-06-29 audit's open question — does $[R_b,\text{evolution}]=0$ hold for the
*sourced* propagators? — remains open and I did not close it.** What is established
(F129/F130/F133/F134) covers the free even law, the free chiral law and the per-branch Weyl
law. Nothing in the tree tests a matter-coupled channel under $R_b$, and the one case that
would exercise it (gravity) is the case the engine now explicitly refuses. Carried to the
UNVERIFIED list.

*Minor `[V9.5]`:* `channels.py:86` (one of **four** `casim.fields.photon` imports in the file — 34, 86, 98, 107) uses `from casim.fields.photon import photon_step_dielectric`
— the thin compatibility re-export — where `CLAUDE.md` says new code should import from
`casim.engine.*` directly.

### V3.6 — the σ-bilinear boundary holds ✔

`gauge/photon.py` imports `bcc_dispersion`, `_f26_rotation_step`, `make_kgrid_3d`, `c_lat`
and the FFT façade. **No bilinear import, direct or transitive through its imports.**

Every consumer of `bilinear`/`bilinear_2d` in `src/` is inside the permitted set:

| Importer | Sector | Permitted? |
|---|---|---|
| `gauge/gluon.py` | strong | ✔ F65–F69 allows W/Z/gluon |
| `gauge/colour_dielectric.py` (2 sites) | strong | ✔ |
| `forks/lattice/smearing_fork_harness.py` | fork | ✔ falsification record |
| `forks/gauge/curl_fork_harness.py` | fork | ✔ falsification record |
| `fields/em.py` | compat shim | ✔ a **name-mapping table** (`ca_maxwell` → `gauge.bilinear`), and its docstring states the retirement correctly |

**No critical finding.** The banner is load-bearing and it is holding.

---

## F276 — the one repair made, under Ben's direction

**Authority note.** §0.1 forbids the audit from changing physics. Ben directed this specific
repair after reading V-014, which supersedes that constraint for this item and this item
only. Everything else found in V2–V5 was recorded and left alone.

Ported from `gauge.photon` into `lattice.curved._half_step_dH`: **(i)** Weyl-symmetric
ordering $W=\tfrac12\{\delta c,\ \sigma\cdot\nabla\}$, which is anti-Hermitian where the
shipped $\delta c\,(\sigma\cdot\nabla)$ was neither Hermitian nor anti-Hermitian;
**(ii)** the $\tfrac{h^2}{2}W^2$ term from $e^{-hW}$. A third correction the port forced:
**(iii)** the spectral derivative's Nyquist bin must be zeroed, or it reintroduces the very
non-unitarity (i) removes.

The three columns separate the two corrections cleanly ($L=64$, 20 ticks):

| $n_\text{sub}$ | asymmetric, 1st (**pre-F276**) | ratio | Weyl, 1st | ratio | **Weyl, 2nd (F276)** | ratio |
|---:|---|---:|---|---:|---|---:|
| 1 | 4.314e-2 | — | 1.732e-3 | — | 4.263e-8 | — |
| 4 | 4.184e-2 | 1.01 | 4.325e-4 | 2.00 | 6.659e-10 | 8.00 |
| 32 | 4.146e-2 | **1.00** | 5.404e-5 | 2.00 | **1.335e-12** | 7.81 |

Ordering alone turns the plateau into $1/n$; adding the $h^2$ term turns $1/n$ into
$1/n^3$, reaching the machine gate. **Global order 0.00 → 2.00** against a refined
reference — the pre-F276 scheme did not converge to the true operator at all, it converged
to a fixed $\approx2.4\times10^{-2}$ offset.

**Nothing moved that should not have.** `casim.verify.run_all()` is **14/14 PASS** with the
`refraction_2d` kernel-fidelity residual still **exactly 0.0** (engine and kernel share the
function, so they moved together). **Zero committed baselines move** — the only records
reaching this stepper are three `legacy_script` records with no declared artifacts.
`scenarios/refraction_2d` norm drift: $9.15\times10^{-2}\to6.80\times10^{-7}$.

Registered as `findings/F276-curved-weyl-ordering-second-order.md` plus a **gate-tier
`entry:`-driven registry record**, `F276-curved-weyl-ordering-second-order`, asserting both
sharp claims (order 2 to within 0.1; norm-error ratio ≥ 6). Neither can pass by accident:
the pre-F276 scheme measures 0.00 and 1.00 respectively.

**Side effect worth naming: this closes half of V-003.** The new record is only the
**second** of 361 to use `entry:`, and the first at gate tier — so
`test_registry_entries.py`'s parametrisation is no longer empty. It now reports
`2 passed` where it previously reported `1 passed, 1 skipped`.

**Two false claims corrected on the way** (documentation, in scope):
`scenarios/refraction_2d.yaml` described the stepper as "exact-unitary" — it had 9.2% norm
drift — and as demonstrating Snell's law, which nothing measures. See **V-025**.

### V-025 — the "reproduces Snell's law" claim is not backed by a measurement

`curved.measure_refraction`'s outgoing-angle diagnostic returns $\theta_\text{out}\approx165°$
against $\theta^\text{pred}\approx13°$, **under every stepper including the exactly-unitary
Cayley one** ($\approx172°$). A quantity equally wrong under an exact stepper is not
measuring the stepper — the cause is that the lattice is periodic, so the packet wraps and
the late-time right-region centroid mixes transmitted, reflected and wrapped amplitude.

Nothing in the registry asserts these angles (the only callers are two `legacy_script`
runners), so no published claim *rests* on it — **but none is *supported* by it either**.
The statement "the construction that already reproduces Snell's law in this codebase"
(F271, and now several docstrings) has no measurement behind it. A quantitative Snell
confrontation needs open/absorbing boundaries and a transmitted-component projection, and
is unbuilt. Warning banner added; not repaired.

---

## V4 — the cubic/BCC partition and the BZ question

### V4.1 — the partition re-measured ✔, and the `photon_pair` contradiction resolved

Measured from the authority (`Channel.topologies`, which `simulation.py:111` enforces),
not by heuristic. **Unchanged from the roadmap, exactly:**

| | count | members |
|---|---:|---|
| cubic-only | **6** | `charge_photon`, `gauge_mc`, `photon_pair`, `refraction_2d`, `w_chiral`, `z_even` |
| bcc-only | **10** | `beta_decay`, `colour_bag`, `composite`, `fermion_doublet`, `gluon_bcc`, `gluon_sourced`, `particle`, `quark_dirac`, `w_sourced`, `weyl_bcc` |
| agnostic | **13** | `element_atom`, `entanglement_register`, `error_correction`, `fermion_algorithm`, `fermion_chain`, `gravity_dielectric`, `njl_meson`, `njl_nucleon`, `nr_electron`, `photon_sourced`, `quantum_circuit`, `string_tension`, `two_grid_atom` |

29 channel types, 6+10+13 = 29. ✔

**The apparent contradiction is resolved, and the resolution is the interesting part.**
`PhotonPairChannel` declares, at `core/channels.py:31`:

```python
topologies = ("cubic",)      # spectral (E,B) on a cubic FFT grid
```

while its propagation path is `step()` → `photon_step_spectral` (imported at line 98) →
`pair_dispersion` → **`bcc_dispersion`**.

> `[V9.5]` The first draft quoted the `bcc_dispersion(k/2, …)` calls as sitting "four lines
> apart" from the `topologies` line. They are 81 lines apart (**112–113**), and they are
> inside `dispersion_residual()` — an F69 *verification* method that samples 2000 random
> $k$ — **not** the propagator. The conclusion is unchanged and reached by the route above;
> the evidence originally cited for it was wrong.

So it is **the label that is cubic, not the physics**. `topologies` describes the *array
the state lives on*; the propagator is `bcc_dispersion`, exactly as F265 says every gauge
propagator always was. Neither the roadmap nor F265 is wrong — they are answering different
questions with the same word.

**That is B1's actual content, and it is an API defect rather than a physics one.**
`LatticeSpec.topology` conflates "which array" with "which lattice", and
`simulation.py:111` rejects mixing on the former. A scenario therefore *cannot* place
`photon_pair` on a `topology: bcc` lattice even though its propagator is BCC. Splitting the
field into `state_layout` and `physics_lattice` would dissolve most of B1 without touching
a number. Recorded as **V-022**.

### V4.2 — the five residual cubic layers

| # | Layer | Verified |
|---|---|---|
| 1 | `gauge/lpt_*` | Still 4D hypercubic Wilson. **Its BZ measure is fine as written** — the Wilson kernel $4\sum\sin^2(k_\mu/2)$ *is* $2\pi$-periodic per axis, so the cube is its true zone. The open problem is the *action*, not the measure |
| 2 | `gauge/bgfield_loop` | **Fixed, F272** — verified: `b0 = 11` untouched, and exactly one committed number moved (`F162.G2.rule_shift_mean` −0.005071 → −0.012591, still the only F162 delta) |
| 3 | `gauge/hypercharge` | **Still 2D.** `hypercharge.py:433` calls `_ca_dirac._weyl_half_step_2c`, confirmed. U(1)$_Y$ lives on the 2D $1/\sqrt2$ lattice; F41/F42/F138/F143 inherit that |
| 4 | The MC actions | **Unstarted**, confirmed — no `bcc_action` import in the MC path |
| 5 | The $\sqrt3$ question | See V4.3 |

**F265's rhombic plaquette construction re-derived independently and it is exact:**
`BCC_PLAQUETTES` has **6** entries; `BCC_PLAQ_AREA` $=2.8284271247461903=2\sqrt2$; all six
normals are $\langle110\rangle$-type (the set of $|{\cdot}|$-multisets is the single
$\{0,1,1\}$); the $O_h$ orbit closes on **one** class; and

$$\sum_p m_p m_p^{\mathsf T} = 4\,\mathbb 1 \qquad\text{residual } \mathbf{0.000\times10^{0}}$$

in exact integer arithmetic. ✔

### V4.3 — the mode-sum question

**This audit does not decide it. It does three things the prompt asked for, and adds a
fourth that changes the stakes.**

#### (a) A new exact result: the walk *is* a faithful BCC crystal walk, and F267's 4/(3√3) is its primitive-cell volume

`bcc.py`'s argument $k_i/\sqrt3$ is $k_i a/2$ with **$a=2/\sqrt3$**. At that lattice
constant the body-diagonal half-vector has length exactly $1$ — the unit hop V2.1 found —
and then, with two lattice points per cubic cell:

| quantity | value |
|---|---|
| primitive cell volume $a^3/2$ | $0.7698003589$ |
| true BZ volume $(2\pi)^3/V_\text{cell}$ | $322.226679$ |
| FFT cube volume $(2\pi)^3$ | $248.050213$ |
| **cube / BZ** | $\mathbf{0.7698003589}$ |
| $4/(3\sqrt3)=4\sqrt3/9$ | $0.7698003589$ |
| reciprocal lattice constant $4\pi/a$ | $10.882796=2\pi\sqrt3$ |

So F267's measured "the cube is $4/(3\sqrt3)$ of one zone" is **not an empirical
coincidence — it is the primitive cell volume**, and F273's "$\sqrt3\cdot$fcc period
lattice" is exactly the reciprocal lattice of a BCC crystal with $a=2/\sqrt3$. Both
measurements now have a closed-form origin.

**Consequence for the two readings: each is right about a different thing.**

- **Reading 1 is right about the computation.** An $L^3$ array has $L^3$ modes and the code
  sums exactly those.
- **Reading 2 is right about the crystal.** The walk is a bona-fide BCC crystal walk whose
  BZ is a truncated octahedron **$1.2990\times$ larger** than the cube it is sampled on.

The array does not *tile* the crystal's zone — it covers $76.98\%$ of it, and by F273 a
**biased** $76.98\%$.

#### (b) What would settle it — and an honest statement of what cannot

**No measurement on the existing code can decide this**, because the code *is* the array:
any trace it computes is by construction the cube sum. The question is whether the array is
faithful to the crystal, which is a question *about* the code.

**The decisive test is constructive:** build the same walk on an **explicit BCC site set** —
a two-sublattice decomposition with integer `np.roll` hops and no fractional shift — so
that the momentum space genuinely tiles the truncated octahedron. Then measure
$\langle\cot\omega\rangle$ and $\langle1/\omega\rangle$ there.

- If the explicit-crystal walk reproduces the cube numbers ($\langle\cot\omega\rangle\to0.221$), **Reading 1**.
- If it gives $0$, **Reading 2**.

This is cheap (a few hundred lines), needs no new physics, and is the one experiment that
discriminates. It is the recommended next action on P3.1 and is in the Tier-B handoff.

Supporting evidence already in the tree, which this audit did not need to re-run:
F267 S5 — translating a delta by **one BCC hop** at $L=16$ spreads it over **2274 of 4096
cells**. The array's sites are demonstrably not the walk's lattice sites.

#### (c) What hangs on each reading

| Result | Reading 1 | Reading 2 |
|---|---|---|
| $I_2=\langle\cot\omega\rangle$ (`eg_sextic.i2_lattice`) | $0.2202$ at $L{=}32$, converging | **exactly 0** |
| $B=-3\sqrt2\,I_2\bar y^4$ (F95 sea cubic) | $-0.0569$ | **0** — `B_leadingform` is *exactly linear* in $I_2$, no residue |
| $C=\vert B\vert/(2\cos3\delta^*)$ (F150) | $0.0362$ | **0** |
| $\lambda_6=C/e^6$, $W=6\lambda_6$ (F234) | $0.243$ / $1.46$ | **0** / **0** |
| F118 self-consistent $(W,v,c)$ triple | closed | the sextic **brake vanishes**; the Mexican hat loses its stabiliser |
| **Charged-lepton mass ratios** | ≤0.007% | **UNCHANGED** — see (d) |
| F100 $\sigma_\phi^2\to\gamma(\Omega)$ | as published | $\langle1/\omega\rangle$ moves 16.9% (F267 S4) |
| `photon_bound_state` $g_c$ | as published | moves $\sim17\%$ |

#### (d) Reading 2 is survivable for the spectrum, and F273 does not say so

The prompt asks whether Design Decision 7 makes a Reading-2 outcome survivable. **Measured:
yes, and cleanly.**

```
'i2_lattice' in derive_weight_as_phase.py : False
'eg_sextic'  in derive_weight_as_phase.py : False
imports delta_star (Fraction 2/9)         : True
```

The charged-lepton shape derivation **does not touch a $k$-space average at all**. It rests
on $\delta^*=\tfrac29$ (exact $O_h$ representation theory — group multiplicity, no lattice
sum) and $\eta^2=\tfrac12$. Re-run live this session: $\delta_\text{meas}=0.22223$ against
$2/9=0.222222$, **0.003%**, with $Q=0.666661$ vs $3\delta=0.666689$.

**What Reading 2 would destroy is the dynamical justification, not the predictions.** $B$,
$C$ and $\lambda_6$ all go to zero, so F150/F234's angle→brake arrow would return
$\lambda_6=0$ against the required $0.243$ — the Landau route would be **falsified**, not
merely unconstrained, and F118's stabilising sextic would vanish.

Which makes Design Decision 7 look prescient rather than merely convenient: it made
$\delta^*$ **primary** and $\lambda_6$ an **output** precisely because F256 showed the
dynamical route could not deliver exactness. That decision is what insulates the spectrum
from this question. **F273's "Reading 2 would demolish the lepton sextic chain" is true of
the *chain* and false of the *spectrum*, and the report should say which.**

### V4.4 — completing F273's coverage, and a critical finding

40 candidate $k$-space average sites located across the named files. Classifications:

| Site | Class | Note |
|---|---|---|
| `photon_bound_state.py:105,142` | **mode sum** | Closed in V3.4. Sum over intermediate two-particle states of a Hamiltonian on the $L^3$ array |
| `eg_sextic.py:87,112,113` | **mode sum** | Dirac-sea trace |
| `eg_sextic.py:137,138` (`i2_lattice`) | **mode sum** (F273) | The contested one — V4.3 |
| `qed_casimir.py:202` | **mode sum** | Cavity modes, definitionally |
| `lpt_wilson.py:64`, `lpt_selfenergy.py:76`, `lpt_wilson_selfenergy.py:186` | **BZ integral, correct zone** | Wilson kernel **is** $2\pi$-periodic; the cube is its true zone and the wrap is an exact no-op |
| `bgfield_loop.py:261` | **BZ integral, biased cube** | Refold fixed by F272; the *domain* was not re-derived. Open |
| `qed_vacuum_polarization.py:292` | **BZ integral, biased + F272 defect LIVE** | **V-023** |
| `qed_electron_self_energy.py:430` | same | **V-023** |
| `gluon_self_energy.py:173` | same | **V-023** |

### V-023 — F272's refold defect is still live in three modules, and in one it flips a sign

F272 found that `((k+π) % 2π) − π` maps $k+q$ to a **genuinely inequivalent momentum**
whenever the kernel is not $2\pi$-periodic, and removed it from `bgfield_loop`. **The same
line, on the same kind of kernel, is still present in three other modules:**

```
src/casim/engine/interactions/qed_vacuum_polarization.py:292
src/casim/engine/interactions/qed_electron_self_energy.py:430
src/casim/engine/gauge/gluon_self_energy.py:173
```

Two sit in the `kernel='rule'` branch; **`gluon_self_energy.py:173` is unconditional** — it computes `lat` and `cont` in one pass and takes no `kernel` argument, so it is contaminated on every call `[V9.5]`. All three feed a rule kernel. Measured periodicity of
those kernels under $k\to k+2\pi\hat e_x$:

| kernel | $\max\lvert K(k+2\pi\hat e_x)-K(k)\rvert$ | verdict |
|---|---|---|
| `qed _K_lat` (rule) | **63.05** | not periodic — wrap is the F272 defect |
| `gluon_self_energy.K_true_4d` | **63.05** | not periodic — wrap is the F272 defect |
| `lpt_*` Wilson $\hat k^2$ | $\sim10^{-14}$ | periodic — wrap benign |

**And it reproduces F272's exact diagnostic signature.** Vacuum polarization,
$\Delta=\text{rule}-\text{cont}$ at $Q=0.3$:

| $n$ | shipped (with refold) | with the F272 fix applied in memory |
|---:|---|---|
| 10 | $-2.018\times10^{-3}$ | $-2.018\times10^{-3}$ |
| 14 | $\mathbf{+8.578\times10^{-3}}$ ← **sign flip** | $-2.092\times10^{-3}$ |
| 18 | $+1.193\times10^{-2}$ | $-2.115\times10^{-3}$ |
| 22 | $+1.245\times10^{-2}$ | $-2.121\times10^{-3}$ |
| 26 | $+1.205\times10^{-2}$ | $-2.121\times10^{-3}$ |

Without the refold the quantity **converges monotonically** to $-2.1214\times10^{-3}$
(0.02% between $n=22$ and $n=26$). With it, the result changes sign between $n=10$ and
$n=14$ and settles on a value of the **opposite sign and ~6× the magnitude** — "the opposite
of a convergent scheme", in F272's own words, at the same $Q=0.3$ and the same threshold
$n\approx\pi/Q$.

The electron self-energy is contaminated more mildly (its shift is $KX-P$ with small $P$,
so fewer points cross the face): $\mathrm{d}A$ drifts $2.36\times10^{-4}\to4.71\times10^{-4}$
over $n=10\to26$ while $\mathrm{d}B$ is stable at $\approx2.0\times10^{-3}$.

**Affected records:** `F251-vacuum-polarization`, `F258-electron-self-energy`,
`F264-qed-allorders-anomaly`, `run-F261-twoloop-qed`, `F249-qed-comparison-battery`, plus
the `gluon_self_energy` leg of the $d_1$/F155/F239 chain.

**Not fixed by this audit** — §0.1 permits fixing plumbing, not physics, and Ben authorised
only the `curved.py` port. The fix is known, is one line per site, and F272 is the worked
precedent. **This is the highest-priority physics item this audit found.**

> **CLOSED 2026-08-02 - 07:45 by F277** (session `pensive-friendly-pascal`, under Ben's
> direction). All three sites fixed, and a full-tree sweep found a **fourth** this audit did
> not scan — `tests/runners/run_d1_vertex_formfactor._Bcoeff_lattice_ff:135`, same rule
> kernel, same line — fixed under the same record. Every number in the table above
> reproduced. The un-refolded vacuum polarization converges monotonically to
> $-2.1214\times10^{-3}$; at the shipped $n=24$ the flatness spread goes
> $1.4484\times10^{-2}\to1.685\times10^{-5}$ and `delta_mean`'s sign flips. The gluon
> bubble's $b_0$ log-slope ratio goes $0.9933\to1.0000542$. $b_0^\text{QED}=4/3$ and
> $b_0=11$ untouched; all 33 checks re-run green; the Wilson control unchanged to
> $2\times10^{-13}$. Three baselines regenerated, `d1_vertex_formfactor.json` filed
> `stale_by_design` (its $n=48$ leg OOMs the sandbox). Guarded at gate tier by
> `test_bz_period_lattices.py` T6–T9. See `findings/F277-qed-gluon-refold-period.md` and
> supersession **S12**. The *domain* question (the biased cube) remains open, at all five
> sites including `bgfield_loop`.

### V4.5 — the re-scoped middle bucket

Spot-checked rather than exhaustively verified (recorded as partial). The `src/` side is in
good order: `raytrace`, `blackhole`, `interior_metric` and `qnm` carry 4, 12, 2 and 1
F178 references respectively. The defect is on the paper side — **V-024**.

---

## V5 — sector-by-sector

**Coverage is partial and the split is stated.** 361 registry records across 7 sectors;
the 45 s cap makes a full sweep Tier B by construction (a single sector's assertion set
alone exceeds it). What ran:

| Sector | Records | This session |
|---|---:|---|
| lattice | 36 (9 assertion) | 7 of 9 assertions PASS: `F127`, `F130` (38 checks), `F131`, `F132`, `F133`, `F159`, `F250` |
| core | 64 (14 assertion) | 3 of 14 + all 4 core gate records PASS |
| gauge | 80 (7 assertion) | `bcc_action` re-derived exactly; the 3 scenario gates PASS; V3/V4 cover the photon and the actions |
| particles | 58 (16 assertion) | lepton shape re-run: **0.003%** on $\delta^*$ (V4.3d) |
| interactions | 55 (21 assertion) | `F244` PASS (reproduced HEAD exactly); the QED pair measured under V-023 |
| forks | 49 | **all 46 fork modules load, 0 failures** |
| suite | 19 | all PASS (the gate tier) |

Sector-specific results:

- **forks ✔ with a caveat.** All 46 load. But *loading them runs physics and writes result
  JSONs* — the load pass rewrote `F228_geon_production_stability.json` and
  `F238_geon_relic_abundance.json` and printed seven `[PASS]` verdicts. Merely checking that
  a fork imports mutates the repo. Restored; recorded as a live instance of
  `import_time_work = 320`, which the same pass demonstrated again when importing
  `casim.engine.particles` ran the F253/F255/F256 derivations and printed their verdicts.
- **gauge — `charged_current`.** Grep for `CKM`/`Cabibbo` in `charged_current.py`:
  **zero hits.** The CKM matrix is neither implemented nor mentioned there. Whether that is
  "absent and stated" is answered in V6.7: it is absent **and** stated, by F53.
- **gauge — `hypercharge` is still 2D**, confirmed at `hypercharge.py:433`.

### V-024 — F114's horizon-free black hole is withdrawn in the code and still current in the claim register

Design Decision 4 and `key-decisions.md` are explicit: *"F114's horizon-free black hole is
**superseded**; the exact vacuum solution is Schwarzschild."* The engine modules agree —
they carry F178 banners.

`papers/Claims-and-Falsifiers-Summary.md` does not. It still lists, with **no supersession
note anywhere in the file**:

- line 19 — *"**Black holes are horizon-free** dielectric condensates (exponential metric):
  no event horizon, no standard Hawking glow, an information-paradox-free unitary
  substrate."* — as numbered claim **9**;
- line 29 — the BH shadow table row $2e/3\sqrt3=1.0463$, **+4.63%**;
- line 34 — *"A horizon-scale shadow excluding +4.63% … **falsifies the model**"*;
- line 38 — second-order deflection coefficient $4\pi$ vs Schwarzschild $15\pi/4$.

This directly answers a V8 row from inside V5: **no, the claim is not withdrawn
everywhere.** It survives in the one document that functions as the model's public claim
register, and it is stated there as a *live falsifier* — so an observation matching
Schwarzschild would be recorded as falsifying a model that no longer predicts otherwise.
`papers/Outreach-Emails.md` repeats it in three places (arguably historical correspondence,
but it is drafted-to-send).

Documentation defect, high severity because of what the document is for.

---

## V6 — cross-sector consistency

### V6.1 — one $c$ ✔ (one object, not four agreeing numbers)

| consumer | value | `is casim.constants.c_lat` |
|---|---|---|
| `lattice.bcc.BCC_C` | 0.5773502691896258 | **True** |
| `gauge.photon` | 0.5773502691896258 | **True** |
| `interactions.gravity` | 0.5773502691896258 | **True** |
| `constants.c_lat` | 0.5773502691896258 | — |

29 modules import `c_lat` from the registry. The only two textual occurrences of
`0.5773502691896258` left in `src/` are a **comment** on the closed-form line and a
**docstring** recounting the C2 history, both inside the D7-exempt
`src/casim/constants/` prefix — so the "0 rogue literals" reading is genuine.

F180's $c_\text{grav}$ is stated as *identically* $c_\text{lat}$ by construction (the GW
equation inherits the same light cone), not as a separately computed agreeing number.

### V6.2 — one energy ✔ on every sub-claim

- **Conservation gate re-run**: free photon, $L=16$, 1000 ticks →
  `max_rel_drift` $=1.70\times10^{-13}$, class **machine**. (The shipped gate reports
  $3.4\times10^{-14}$; the $5\times$ difference is initial-data normalisation, not a
  discrepancy — both are machine class.)
- **`energy` and `energy_density` are the same number in the same convention**:
  `Channel.energy(state)` $=12202.8439938268$, `sum(energy_density(state))`
  $=12202.8439938268$, and `energy_density` **is** `T00_field_energy`.
- **Zero of 29 channels override `energy_density`** `[V9.5]` (29 is the same population as V4.1's 6+10+13 partition; an earlier draft said 20 after scanning fewer modules). One definition on the base class,
  no agreeing copies — the strongest possible form of F270's intent.
- **A channel with no expressible energy leg reports `None`, not zero**: `weyl_bcc`
  without a declared mass returns `None`, and `TotalEnergy` carries the string `missing`
  (`EnergyTrace` does not, correctly — it is a per-channel trace, not a total).

### V6.3 — one clock ✔ with a latent trap

The reconciliation, the exact-rational arithmetic and the mode machinery are all present
and correct. Two observations:

### V-026 — three channels declare a `dt_native` that disagrees with the `dt` they step at

| channel | declares `dt_native` | `step()` config default | |
|---|---:|---:|---|
| `charge_photon` | 1.0 | **0.1** | MISMATCH |
| `nr_electron` | 1.0 | **0.2** | MISMATCH |
| `photon_sourced` | 1.0 | **0.1** | MISMATCH |
| `gluon_sourced`, `gravity_dielectric` | 1.0 | 1.0 | ok |

`_channel_timing_spec` reads `cfg["dt"]` **if present** and falls back to the class
attribute otherwise. So a scenario that sets `dt` explicitly gives the clock the truth —
and **all 16 shipped scenarios that use these channels do set it** (verified:
`charge_photon.yaml` dt=0.1, `unified_hydrogen.yaml` dt=0.1, `realspace_electron_*` dt=0.2,
etc.; **zero** scenarios omit it).

**So this is latent, not live.** But a *new* scenario that omits `dt` on `photon_sourced`
would be silently desynchronised by $10\times$ **and reported as synchronous**, because the
clock would reconcile on the declared 1.0 while `step()` used 0.1 — the original B2 defect,
now wearing a correct-looking declaration. One-line fix per channel: set `dt_native` to the
same value as the step's own default.

### V-027 — no channel declares a `dt_max`, so both CFL guards are unreachable

`dt_max` is `None` on **all 29** channels `[V9.5]`. Consequently the build-time error
`dt_native exceeds its stability ceiling` can never fire, and the "a config may lower a CFL
limit, never raise it" guard at `clock.py:221` is behind `if dt_max is not None`, so a
scenario may set any `dt_max` it likes without tripping it. Both checks are correctly
written and structurally armed; nothing arms them with data. Not a defect today — a
gap between a documented protection and an enforced one.

### V6.4 — Gauss's law in the coupled theory ✔, and the residual is bounded in $L$

**Both halves of a question the 2026-06-29 audit left open.** Setup: $E$ projected
transverse with the **BCC curl symbol** (so the state starts exactly on the constraint),
100 ticks, residual normalised to the field scale $|E_k|_\max$.

| $L$ | free ($\rho=0$, $J=0$) | **sourced** (live $J$, $\rho$ by continuity) |
|---:|---|---|
| 8 | $1.97\times10^{-15}$ | $1.36\times10^{-14}$ |
| 12 | $1.66\times10^{-15}$ | — |
| 16 | $1.77\times10^{-15}$ | $1.50\times10^{-14}$ |
| 24 | $2.45\times10^{-15}$ | $1.98\times10^{-14}$ |
| 32 | $2.15\times10^{-15}$ | $1.75\times10^{-14}$ |
| 48 | $2.17\times10^{-15}$ | $2.48\times10^{-14}$ |

**Gauss's law is conserved to machine precision in the sourced U(1) sector, not merely
sector by sector**, and the relative residual is **bounded and sub-linear in $L$** — it
rises $1.82\times$ across a $6\times$ range in $L$ `[V9.5]`; the first draft called that
"flat", which the numbers do not quite support, and stacked "exactly conserved" on top of
"to machine precision", which are two different claims. So the F87 residual
(~$2\times10^{-12}$ absolute over 100 ticks) is FFT round-off scaling with the field norm,
and **is bounded**.

**Scope, stated honestly:** this is EM + current at the kernel level. The **SU(3)** Gauss
law (F43/FG-7) and a full three-sector engine scenario (`quark_dirac` + `gluon_sourced` +
`photon_sourced` together) were **not** tested. The U(1) half is answered; the
non-Abelian half remains open.

*Minor API hazard found while doing this:* `div_from_current(J)` returns a **Fourier-space**
array while `gauss_residual(E, rho)` expects a **position-space** $\rho$. Neither name says
so, and mixing them produces a silently meaningless number (it did, for me, before I
checked). Worth a docstring line or a suffix.

### V6.5 — charge quantisation is **input**, at a named line

```python
# src/casim/engine/gauge/hypercharge.py:117-122
# SM hypercharge assignment (Gell-Mann–Nishijima Q = T_3 + Y/2)
Y_LEPTON_L = -1    # left-handed lepton doublet (ν_L, e_L)
Y_E_R      = -2    # right-handed charged lepton
Y_NU_R     =  0    # right-handed neutrino (sterile in minimal SM)
```

plus the quark assignment in the module docstring at line 23
($Y_{Q_L}=+\tfrac13,\ Y_{u_R}=+\tfrac43,\ Y_{d_R}=-\tfrac23$).

So the quark charges $\pm\tfrac13,\pm\tfrac23$ and lepton charges $0,\pm1$ follow from
$Q=T_3+Y/2$ **with the Standard Model's own $Y$ assignment written in as literals**.
Charge quantisation is therefore **inherited, not derived**.

There is a partial defence, and it should be stated: F41's table records *"F38 anomaly
cancellation — Y values used here are exactly the FG-1 anomaly-cancelling set"*. The model
**checks** the assignment is anomaly-free; it does not **derive** it from anomaly
cancellation. Verified-consistent, not derived.

Worth flagging against Design Decision 1 ("Ludwig's SU(2) derivation, **not** the Standard
Model"): this is a place the model leans on the SM more than that decision implies.

### V6.6 — gravity closes on matter ✔, verified against the closed form

Run through F270's own construction (which subtracts the $k=0$ baseline — my first attempt
omitted that and got nonsense, recorded so the method is reproducible):

**(a) the $\sin^2k$ law is exact.** Ratio to $\tfrac12c^2\sin^2k\sum|\psi|^2$ at fixed
envelope:

| $k$ | ratio |
|---|---|
| 0.4 | 0.9725376374 |
| 0.8 | 0.9725536279 |
| 1.2 | 0.9725857683 |

**spread $=4.813\times10^{-5}$** — under the claimed $10^{-4}$, so the $\sin^2k$ law holds
exactly and the offset is a constant.

**(b) the residual is the envelope**, not the coefficient: widening $(L,w)$ from
$(32,72)\to(40,128)\to(48,200)$ moves the ratio $0.972554\to0.984344\to0.989800$,
monotonically toward 1.

**(c) the colour-axis bug is fixed.** A rank-4 (3-colour) input to `T00_dirac_rest`
returns shape $(16,16,16)$ — **rank 3, summed** — not a three-copy rank-4 field, and the
total is exactly $3.000000\times$ the single-colour result: three colours of charge, **one**
gravitational field.

### V6.7 — CP and CKM: a consequence, and F53 already says so ✔

$J(1)=0$ is **not** a prediction that the CKM phase vanishes. It is the arithmetic
consequence of a one-generation model: $N_\text{phase}=(n-1)(n-2)/2=0$ at $n=1$, so there
is no CP-odd parameter to have. F53 §"does not address" states this explicitly and
correctly:

> *"Observed CP violation ($\epsilon_K$, $\sin2\beta$, the Jarlskog $J\approx3\times10^{-5}$)
> requires **three** generations — out of scope for a single-generation model by
> construction. FG-9's $J=0$ is the correct one-generation answer, not a deficiency."*

**No open conflict.** The honest residual is that the model has **no three-generation CKM
sector at all**, so measured CP violation is *unaddressed* — which belongs in V8's omissions
list under "open **and acknowledged**", the category that is fine.

### V6.8 — three generations: **derived, conditionally** — and one word overstates it

The chain is exact where it is group theory. F75's checks: $|O|=24$, $|O_h|=48$; the
maximum single-valued irrep dimension is **3** (from $\sum d^2=48$); the BCC
nearest-neighbour shell decomposes as $A_{1g}\oplus A_{2u}\oplus T_{1u}\oplus T_{2g}$; and
the **unique parity-odd triplet is $T_{1u}$, dim 3**. All multiplicities are exact
rationals; the only float in the chain is a $4.4\times10^{-16}$ commutator.

F79 then builds $g_*=16\times\dim T_{1u}=48$ and says of it: *"There it was 'assumed three
generations'; F75 makes the generation count a **theorem** about the BCC point group."*

**But F75's own status line says otherwise:**

> *"Candidate finding … The **group theory** is exact; the **physical identification**
> (generation index = orbital shell irrep) is a **stated hypothesis, not a theorem**."*

So the precise answer to V6.8: the **3 is derived, not input** — it is $\dim T_{1u}$, and
that is a genuine advance over the SM where 3 is simply put in. But it is derived
**conditional on a Candidate-status identification**, and F79's word "theorem" applies to
$\dim T_{1u}=3$ (true) and not to "a generation *is* that triplet" (hypothesis).

**F79's structural $G$ therefore inherits `Candidate`, not `input`** — which is consistent,
since F79 is itself labelled Candidate. Only the one word overstates.

Cross-link worth recording: the *other* factor in $g_*=16\times3$ is "16 anomaly-free Weyl
fields per generation" from F38/F47 — and V6.5 just established that the hypercharges
making that content anomaly-free are the SM assignment put in by hand. So $g_*$ is
$3_\text{derived}\times16_\text{inherited}$.

---

## V7 — constants, exactness, and the empty field

### V7.1 — all 43 constants walked

| Property | Result |
|---|---|
| `provenance` finding | **43/43** present |
| `exactness` class | **43/43** present — exact 12, external 16, quantitative 14, bracketed 1 |
| `derivation` string | **43/43** present |
| recorded `Site` | **40/43** — see V-028 |
| rationals export `Fraction` **and** `<symbol>_f` | **4/4** (`delta_star`, `sin2_thetaW_onshell`, `sin2_thetaW_uv`, `c_fierz_colour`), `_f` is `float` in every case |
| bracketed exports **no** scalar | ✔ `alpha_eff_star` has `value=None`, **no module attribute**, and resolves only via `endpoint(..., 'lo'\|'hi')` → 0.376 / 0.411 |
| exact constants resolve from closed form | ✔ asserted by `test_exact_constants_resolve_from_closed_form`, which ran and passed; independently confirmed for `c_lat` in V2.2 |

### V-028 — three constants have no recorded `Site`, and two of them are actually used

D7 requires a `Site(path, name, kind=...)` when a module binds a constant. Three have none:

| symbol | actually used in | verdict |
|---|---|---|
| `cos3_delta_star` | `engine/particles/eg_sextic.py` | **unrecorded consumer** — the registry understates its reach |
| `e_saturation` | `engine/particles/derive_weight_as_phase.py` | **unrecorded consumer** |
| `M0_constituent_GeV` | *nothing outside `constants/`* | **orphaned constant** |

The first two are the load-bearing case: `cos3_delta_star` is one half of the F256
near-coincidence pair and `e_saturation` feeds the weight-as-phase derivation, so a future
migration that moves either file would not be caught by the site check — which is exactly
what went red after C5 and C6.

### V7.2 — the pluralities, and the collapse test ✔

All five are registered separately, in the sectors they belong to:

| plurality | members |
|---|---|
| $f_\pi$ | `f_pi_anchor_MeV` 92.07 · `f_pi_pdg_target_MeV` 92.4 · `f_pi_gamma_convention_MeV` 92.28 (all `strong`) |
| $\sin^2\theta_W$ | `sin2_thetaW_uv` 0.25 · `sin2_thetaW_onshell` 0.222222 (both `electroweak`) |
| $\cos3\delta$ | `cos3_delta_star` 0.785887 · `cos3_delta_data` 0.785874 (both `lepton`) |
| **2/9 triple** | `delta_star` (lepton) · `sin2_thetaW_onshell` (electroweak) · `c_fierz_colour` (strong) |
| **$1/\sqrt3$ pair** | `c_lat` (geometry) · `q_star_a_band_lo` (strong) |

**The deliberate-collapse test, which the prompt asks for explicitly:**

```
1) baseline, unmodified tree:                     PASSES
2) c_fierz_colour removed from the registry:      FAILS as it must —
   "expected exactly three registered 2/9s in three sectors,
    got ['delta_star', 'sin2_thetaW_onshell']"
3) restored, re-run baseline:                     PASSES
```

**The guard is real, not decorative.** But V-016 stands: of the five pluralities, **four
are gated and the $1/\sqrt3$ pair is not** — `q_star_a_band_lo` appears in zero test files.

### V7.3 — every declared import site resolves ✔

`unverified_import_sites()` → **0**. 13 recorded `literal` sites remain, all under
`tests/`, matching the C2 target state (`test_literal_sites_are_confined_to_tests` passes).

### V7.4 — the `Reach` column: **fixed** (plumbing, as the prompt authorised)

`registry.py` took `reach` as a frozen manifest string. It now reads the **module graph**,
which is the thing that actually computes reachability, with the manifest value retained as
a fallback so the registry never hard-depends on a generated artifact.

| | before | after |
|---|---|---|
| distinct values in `code-index.md` | **2** | **5** |
| driven | 47 | **51** |
| package-only | 131 | **4** |
| test-only | 0 | **90** |
| unreferenced | 0 | **26** |
| entry-script | 0 (1 in registry) | **10** |

The artifact a reader is pointed at now agrees with the graph. The residual 181 vs 187 is
the 6 fork `__init__.py` files the graph types and the registry does not hold — accounted
for in V1.3. `casim index --check` clean, `check_module_registry` green,
`gen_module_graph --check` current.

**`exactness` is still populated on 3 of 181** (V-007). Not fixed: unlike `reach`, there is
no generated artifact to read it from — populating it means running C8.4's three-rule
ladder over the modules, which is a P6 work item, not plumbing.

### V7.5 — ratchets, measured

| Ratchet | Value | Baseline | Verdict |
|---|---:|---:|---|
| direct `np.fft` transform calls in `src/` | 0 | 0 | OK |
| device-namespace fft calls | 8 | 8 | OK |
| files importing numpy | 165 | 165 | OK |
| files importing scipy | 7 | 7 | OK |
| rogue literals in `src/` | 0 | 0 | OK |
| rogue literals in `tests/` (backlog) | 272 | counted | OK |
| recorded `literal` sites | 13 | — | all in `tests/` |
| `no_assert` | 231 | 231 | OK |
| `unfalsifiable` | 70 | 70 | OK |
| **`import_time_work`** | **320** | **320** | **OK — not re-baselined** |
| `legacy_script` | 47 | 47 | OK |
| gate-tier records | **27** | 26 | rose by the F276 record |
| test registry records | **361** | 360 | rose by the F276 record |
| assertion records | **94** | 93 | rose by the F276 record |

**`import_time_work` is confirmed still 320 and still declared NOT MET** — it has not been
silently re-baselined, which was the specific thing V7.5 asks. V5 demonstrated it live:
importing `casim.engine.particles` runs the F253/F255/F256 derivations and prints their
verdicts, and loading the forks wrote two result JSONs.

---

## V8 — claims against measurement

Rebuilt from the current tree, with the measured column re-checked against 2025 sources
rather than copied forward. **Two residuals moved because the *measurement* moved, not the
model** — that is exactly what this item exists to catch.

| Quantity | Finding | Model | Measured (2025) | Residual | Zero-parameter? | Moved? |
|---|---|---|---|---|---|---|
| $c_\text{lat}=1/\sqrt3$ | F25/F26 | $0.5773502691896258$ | — | exact | **definition**, not a prediction — see below | no |
| $c_\text{grav}=c_\text{lat}$ | F180 | slope residual $c_g-c_\gamma=$ **0.0 exactly** | GW170817 $\lvert\Delta c/c\rvert<10^{-15}$ | 0 | yes | no |
| $\sin^2\theta_W(M_Z)$ | F138 | $0.23173$ | $\approx0.23122$ | **+0.22%** | yes, given the $\mu_\star=4\pi v$ matching | no |
| $m_Z/m_W$ (on-shell) | F138/F49 | $1.13389$ ($3/\sqrt7$) | $91.1880/80.3692=1.13462$ | **−0.064%** | yes | **no — and this is notable**, see below |
| $\alpha_s(M_Z)$ | F144 | $0.11955$ (1-loop) | $0.1175\pm0.0010$ | **+1.7%** | one scheme-matching input | **YES: was +1.3%** |
| $\alpha_s(M_Z)$ 4-loop | F144 | $0.12798$ | $0.1175$ | $+8.9\%$ | " | " |
| Charged-lepton spectrum | F253/F255/F256+F234 | $\delta_\text{meas}=0.22223$ vs $2/9$ | $Q=0.666661$ | **0.003%** | **yes — zero shape parameters** | no (re-run in V4.3) |
| $\lambda_6=0.243$, $W=1.46$ | F234 | output of $\delta^*$ | — | — | output, not fit | **hangs on V4.3** |
| $m_n-m_p$ | F122 | $+1.51$ MeV | $+1.293$ MeV | **+17%** | sign correct, magnitude not | no |
| Nucleon at $3m_c$ | F123 | $928.5$ MeV | $938.27$ MeV | **−1.05%** | one $f_\pi$ anchor | no |
| H ground state | F125 | $-13.596$ eV | $-13.5984$ eV; Ry to $1.1\times10^{-12}$ | $\sim10^{-12}$ | $\alpha$ is the one EM input | no |
| **Deuteron $E_b$** | F104/F113/F126 | **$2.224$ MeV** | $2.22457$ MeV | **0.026%** | see below | **YES: was 0.34%** |
| $\sqrt\sigma/f_\pi$ | F124 | $4.0032$ | $4.5617$ | **12.24%** | yes | no |
| $2\Delta/kT_c$, $\Delta C/C_n$ | F210 | $2\pi/e^\gamma$, $12/7\zeta(3)$ | BCS | machine | yes | no |
| $T_c$, 7 elements | F211 | — | — | **mean 14.26%** | Allen–Dynes inputs | no |
| $\rho_\Lambda$ | F193/F196 | $7.578\times10^{-10}$ J/m³ | $6\times10^{-10}$ | **0.101 dex** | yes, given $p=2$ | no |
| BH shadow $+4.63\%$ | F114 | $2e/3\sqrt3=1.0463$ | — | — | — | **SUPERSEDED by F178 — and still published (V-024)** |
| Alcubierre warp | F204 | structurally excluded | — | — | yes | no |
| $m_W$, $m_Z$ absolute | — | **not predicted** — only the *ratio* | — | — | — | open, see below |
| $g-2$ | `qed_amu` | QED 2-loop $A_2(\mu)=0.765857$ | known QED $0.765857410$ | $\sim5\times10^{-7}$ | yes for the QED piece | **open and acknowledged** |
| CKM matrix | — | absent | — | — | — | **open and acknowledged** (V6.7) |
| Neutrino masses | F47 + F216 | see-saw $M_D^2/M_R$, Higgs-free | — | — | scale not fixed | **open and acknowledged** |

### V-029 — two residuals moved because the measurement moved

- **$\alpha_s(M_Z)$: +1.3% → +1.7%.** The model number is unchanged at $0.11955$; the PDG
  world average fell from $\approx0.1180$ to $0.1175\pm0.0010$. The residual is now
  $\approx2\sigma$ of the experimental error rather than $\approx1.4\sigma$. Not a
  regression, but the recorded "+1.3%" is stale and should be re-stamped.
- **$m_Z/m_W$ is *unmoved* by the 2025 $m_W$ shift, and that is worth saying.** The PDG
  2025 average is $80.3692\pm0.0133$ GeV with **the CDF-II result excluded for low
  compatibility**. Against that, F138/F49's $3/\sqrt7=1.13389$ gives $-0.064\%$ — the same
  residual the tree records. Had the model been tuned to the CDF value it would now be
  visibly worse; it was not, and it survives the exclusion cleanly.

### V-030 — the Claims register quotes the model's *worst* Weinberg number as its headline

`papers/Claims-and-Falsifiers-Summary.md` headline table:

> $\sin^2\theta_W\to m_Z/m_W$ | $\tfrac14\to2/\sqrt3=1.1547$ | zero parameters; **1.77% from PDG**

That is the **UV** value at $\mu_\star$, carried straight to $M_Z$ with no running. F138's
actual result — the same claim after the matching the model itself derives — is
$m_Z/m_W=3/\sqrt7=1.13389$, **−0.064%**, i.e. **27× better**, and $\sin^2\theta_W(M_Z)=0.23173$
at **+0.22%**. The register advertises 1.77% while the tree computes 0.064%.

Combined with V-024 (the horizon-free black hole still listed as claim 9 and as a live
falsifier) and claim 4's "**a theorem** about the cubic point group" — which V6.8 showed
F75 itself calls a *stated hypothesis* — the claim register is **stale in three separate
places** and is the document most likely to be read as the model's public position. It was
last dated 2026-06-08, before F138's promotion, before F178, and before F253–F256.

### The four rows the 2026-06-29 audit flagged as omissions

| Row | Status now |
|---|---|
| $m_W$, $m_Z$ absolute | **Open, and now acknowledged in effect** — the model predicts the *ratio* only. The absolute scale needs $v$, which is an anchor, not a prediction. No document claims otherwise, but none states the limitation plainly either. Recommend one line in the claims register |
| $g-2$ | **Open and acknowledged, exemplarily.** `qed_amu.py` computes the QED piece through two loops (reproducing $A_2(\mu)=0.765857$ against the known $0.765857410$) and its `SCOPE — what is NOT claimed` block explicitly defers hadronic VP, hadronic light-by-light and electroweak pieces, storing `A_MU_MEASURED` as *"reference only; NOT a claim"*. It even names the 2025 Theory Initiative situation. **This is the model for how the other rows should read** |
| CKM | **Open and acknowledged** — F53 states that observed CP violation needs three generations and is out of scope; `charged_current.py` has zero CKM references (V6.7) |
| Neutrino masses | **Open and partly acknowledged.** F47 supplies the Higgs-free see-saw *mechanism* ($m_\nu\sim M_D^2/M_R$) and F216 the dark-sector context, but nothing fixes $M_R$, so no mass or ordering is predicted. The mechanism is a genuine result; the scale is not addressed and the finding does not foreground that |

**No row is open-and-unacknowledged**, which is the category that would have mattered. The
weakness is not hidden claims — it is a **stale public register** (V-024, V-030).

### On $c_\text{lat}$: prediction or definition?

The prompt asks. **It is a derived consequence, not a definition** — V2.1/V2.2 showed
$\omega=\arccos u$ is *forced* by $\det U=1$ and $\operatorname{tr}U=2u$, and
$\lim_{k\to0}d\Omega/d\lvert k\rvert=1/\sqrt3$ follows for every direction. What it is
*not* is a **falsifiable** prediction on its own: $c_\text{lat}$ is dimensionless in
lattice units and only acquires empirical content through the cell $a$ (F107), which is
where the falsification handles actually live (the GRB $n=2$ bound). Recording it in a
"claims vs measurement" table without that qualifier overstates it.

### On the deuteron: how many parameters?

The prompt asks. The chain is $\sigma$-exchange with $m_\sigma=2m_c$ (F126, derived from
the NJL constituent mass) plus the F113 quark-Pauli repulsive core plus the F103 pion
tensor force. `FB07_deuteron.json` records `m_sigma_MeV = 622.4` and a physical
$b=0.55$ fm. **$E_b=2.224$ vs $2.22457$ MeV is 0.026%** — but that agreement is achieved at
a chosen $b$, so it is a *one-parameter* fit of a quantity the model gets structurally
right (bound only via the tensor force, F104's actual result), not a zero-parameter
prediction. The table above says "see below" rather than "yes" for that reason.

---

## Inconsistencies between findings

- **V-030** — the claims register advertises $m_Z/m_W$ at 1.77% while F138 computes 0.064%.
- **V-023** — F272 fixed a defect in one module and left it live in three others.
- **V-024** — `key-decisions.md` (F178) and `Claims-and-Falsifiers-Summary.md` state
  opposite things about the black hole.
- **V-019** — `bcc_smallk_to_weyl_residual`'s docstring asserts $O(k^2)$ for a single
  branch; F30 establishes $O(k)$ for a branch and $O(k^2)$ only for the pair. Measured
  order is $0.99$. Module contradicts finding.
- **V-020** — a `MeasuredConstant` reason string states $1/\sqrt{2d}$ where every other
  document and both registered values require $1/\sqrt d$.
- **V-009** (from V1) — `key-decisions.md` D1 names `casim.engine.lattice.cubic`;
  `CLAUDE.md` correctly says no such module exists.
- **V-012** — Design Decision 5, `key-decisions.md` and `photon.py`'s docstring all state
  the photon propagator **is** `_f26_rotation_step`. It is a bit-identical copy.

V4, V6 and V8 are covered in their own sections; their cross-finding items are folded in above `[V9.5]`.

---

## Omissions — physics absent or unaddressed

See **V8**. Summary: every row the 2026-06-29 audit flagged is now **open and
acknowledged** — $m_W/m_Z$ absolute (ratio only), $g-2$ (QED piece computed, hadronic and
EW explicitly deferred), CKM (three generations out of scope, F53), neutrino masses
(mechanism in F47, scale unfixed). **No row is open-and-unacknowledged.**

---

## Documentation and labelling defects

### V-002 — `casim backend` reports the wrong backend availability and gives false advice

```
$ casim backend
active FFT backend : pyfftw (FFTW, 4 threads, plan cache on)
available          : numpy

  pyfftw is not installed. Six of the eight channel types are
  FFT-bound, so this is the cheapest speedup available:
      pip install -e '.[fast]'
```

Ground truth, same interpreter:

```
casim.numerics.backends.available()  → ['numpy', 'pyfftw', 'scipy']
casim.numerics.backends.active()     → PyfftwBackend
pyfftw.__version__                   → 0.15.0 (vendored)
```

Cause, `src/casim/cli.py:399-406`: `_cmd_backend` builds its availability list by probing
`getattr(ca_fft, "_scipy_fft", None)` and `getattr(ca_fft, "_pyfftw_fft", None)` — private
attributes that no longer exist since D8 moved backend selection into
`casim.numerics.backends`. Both probes return `None`, so the list is always exactly
`["numpy"]` and the "not installed" branch always fires.

The irony is exact: the function's own docstring says it exists *"because the fallback used
to be invisible: pyfftw was preferred by ca_fft and never installed, so the project ran on
single-threaded scipy for its whole history without ever saying so."* It now misreports in
the opposite direction, and would tell a user to install a package that is already the
active backend.

Severity is reporting-only — `fft.describe()`, which the same command prints on the line
above, is correct, and the physics runs on the right backend. **Not fixed by this audit:**
`src/casim/cli.py` is inside the open `cowork-p4-p5` claim (trap #9).

### V-006 — the module registry's `reach` and the module graph still disagree, with new numbers

The prompt (V7.4) records this as a P6 defect at 47 `driven` (registry) vs 50 (graph).
Re-measured 2026-07-31 - 23:26:

| Source | Records/nodes | `driven` | `package-only` | `test-only` | `unreferenced` | `entry-script` |
|---|---:|---:|---:|---:|---:|---:|
| module registry (`code-index.md`'s source) | 181 | **49** | **131** | 0 | 0 | 1 |
| `docs/design/module-graph.json` (engine roles) | 187 | **52** | **3** | **92** | **31** | **9** |

So the disagreement is unchanged in kind and has moved in value: 49 vs 52 driven, and the
registry still collapses four graph categories into `package-only`. `registry.py` takes
`reach` as a manifest-supplied string rather than reading the graph, which is the
mechanism. The prompt authorises fixing this as plumbing; it is **deferred to V7**, where
the rest of the constants/exactness sweep lives, so that the fix and its verification land
together rather than mid-audit against a moving tree.

### V-007 — `exactness` is populated on 3 of 181 registry records

Roadmap §2.1 says the field is empty on all 178. Measured: **3 of 181** are populated,
which is empty for practical purposes but is no longer literally zero, so the roadmap text
is wrong in both the numerator and the denominator. `code-index.md` still renders a column
for it.

### V-008 — roadmap §2.1 and §2.5 are stale in eight places

Measured against `docs/roadmaps/roadmap-unified-program.md` as of 2026-07-31 - 23:30:

| Roadmap says | Actually |
|---|---|
| engine modules registered: 178 | 181 |
| findings: 261 files, max F266 | 268 files, max F273 |
| scenarios: 46 | 48 |
| tests: 347 files / 350 records | 357 files / 360 records |
| gate: 14 checks (implicitly 22 gate records) | 14 checks, 26 gate records |
| graph types 184 nodes | 187 |
| reach: 47 driven / 131 package-only vs graph 50 | 49 / 131 vs graph 52 |
| `exactness` empty on all 178 | populated on 3 of 181 |

The prompt already flagged the findings row. The rest are the same class. These are
generated-from-nothing prose numbers in a hand-written document; the fix is either to
regenerate the section or to stop quoting counts in it. **Not fixed here** — the roadmap is
narrative and the correction belongs with the audit's closing changelog entry.

### V-009 — `key-decisions.md` D1 names a module that does not exist

D1 reads *"simple-cubic code is retained as the continuum-limit regression target
(`casim.engine.lattice.cubic`)"*. There is no `cubic.py`; the code is in
`lattice/core.py` and `lattice/core_exact.py`, and the rename is the still-open P3.1
item 6 that F272's session handed back because this mount refuses `unlink`. `CLAUDE.md`
states the situation correctly (*"there is no `cubic.py`"*), so the two documents disagree.

**Deferred to V2.5**, which owns the cubic-layer verification and the `git mv` handoff.

### V-013 — F87 drifts, and the drift is round-off plus stored wall-clock time

`F87-charge-coupling-paired-photon` — a photon-chain record — **FAILS** on re-run. It is
one of the 28 known drift FAILs. Re-run in this session (so trap #1 is satisfied) and every
one of its 26 deltas characterised:

| Class | Count | Examples |
|---|---:|---|
| Absolute residuals **below** the $10^{-12}$ floor | 17 | `div_A_max` 1.21e-17→8.67e-18; `holo_minus_flux_loopA` 0.0→1.11e-16; `ampere_residual_resolved` 1.37e-15→1.41e-15. Largest of the class: **5.33e-15** |
| Absolute residuals **at or above** the floor | 4 (2 distinct, each mirrored in `_summary`) | `gauss_residual_max_100steps` 1.79e-12→1.05e-12; `magnetic_gauss_max_50steps` 1.52e-11→6.64e-12 |
| Physics observables, **unchanged to $\le10^{-16}$ relative** | 4 | `holo_value` 0.7→0.7 (rel 1.6e-16); `holo_value` 15.86134→15.86134 (rel 4.5e-16); `holo` 1.0 (rel 1.1e-16) |
| **Wall-clock time** | 1 | `_summary.runtime_s` 0.722→0.458 |
| **total** | **26** | |

**Recommended verdict: accept.** The two residuals above the floor are themselves numerical
zeros — a Gauss-law residual of $10^{-11}$ is the statement that Gauss's law holds — and
every observable with physical content reproduces to $10^{-16}$. Under the runner's own
rule, one value one decade above the floor drags 25 sub-floor values into a FAIL; that is
defensible as written, and the right fix is a per-record tolerance, which is a physics
owner's call and not the audit's.

The same pattern appears in `F72` (`S_even` −8.9e-16 → **0.0**, i.e. an exactly-zero claim
got *better*) and `F91` (`S_even` 4.4e-16 → **0.0**). Both were reported PASS by the
runner's sub-floor classifier, which is working.

**All six baselines this audit's re-runs touched — F67, F69, F72, F87, F91, F100 — were
restored from `HEAD`** via `git show HEAD:… > …` (trap #5). Only the five pre-existing
modifications recorded in the V0 table remain.

### V-021 — result baselines store wall-clock time, which guarantees permanent false drift

`wall_seconds`, `_summary.runtime_s` and `runtime_s` are written into committed result
artifacts and are then diffed by `check_result_drift.py` and the record runner.

`F100_gamma_from_transfer_operator.json`'s **only** delta on re-run was
`runtime_s: 0.056 → 0.083` — it "drifted" because the machine was busier. F72's only
non-numerical-zero delta is `wall_seconds: 0.50 → 0.59`.

This is a permanent noise source in `make drift`, it inflates the 28-FAIL backlog with
entries that can never be resolved by physics, and it makes "the baseline reproduces" a
weaker statement than it should be. Fix is one exclusion list in the comparator (or stop
writing timings into the artifact and put them in the journal, where they belong).
Cheap, mechanical, and it makes the drift signal trustworthy.

### V-011 — `pytest --collect-only` rewrites a git-tracked artifact

`tests/conftest.py:84` regenerates `test-results/casim-exactness-inventory.md` from
`pytest_sessionfinish`, which fires at the end of **every** pytest session — including a
pure `--collect-only`. So asking pytest what it *would* run mutates a tracked file.

Observed here: a `--collect-only` during V1.2 rewrote the file's header stamp from
`2026-07-31 - 08:18` to `2026-07-31 - 23:30`. Content was otherwise byte-identical (14/14
checks, same rows), so there is no drift — but the file then appears in `git status` for
the rest of the session, which is noise in exactly the place where real baseline drift is
supposed to be visible. Restored to `HEAD` by this audit (`git show HEAD:… > …`, per
trap #5); `git status` on it is now clean.

**Recommended one-line fix:** guard the hook with
`if getattr(session.config.option, "collectonly", False): return`. Not applied — the
conftest is the `tests` claim's territory and the fix wants its own gate run.

### V-010 — `git status` cannot serve as V9's cleanliness check in this repo

Deliverable 3 of the audit asks that `git status` show only intended files. That is not
achievable here: `HEAD` is `5b5c307`, which predates the C9 restructure, so the working
tree legitimately shows the entire `ca-simulation/` directory as deleted, all of
`src/casim/engine/` as new, and ~40 docs as modified. `git status --porcelain` returns
hundreds of lines before this audit writes anything.

**Recommended replacement for V9.3:** snapshot `git status --porcelain` at audit open,
diff it against the same command at audit close, and assert the difference is exactly the
intended file list. That is a check that can pass. Recorded now so V9 does not report a
false positive or quietly skip.

---

## Ratchets and debt — measured

See the supplementary table under *Starting state*. Every ratchet reads `OK`. Two
deliberately-unmet acceptance criteria are unmoved and have not been silently re-baselined:

- **`import_time_work` = 320** — P1.3/P1r.1's criterion, declared **NOT MET** at C7 rather
  than redefined. Confirmed still 320, still declared.
- **`legacy_script` = 47** — declared debt, ratcheted to zero as a target, unmoved.

The `tests/` rogue-literal backlog stands at **272** and is counted rather than gated,
which is the C7 design. 13 recorded `literal` sites remain, all under `tests/`.

---

## Verified correct — explicitly checked and found sound

### V1 — the barrier, check by check

Each run as its own bash call, per trap #6. Wall times are single-run and include ~2.5 s of
interpreter and import startup.

| Check | Verdict | Wall |
|---|---|---:|
| `tests/casim/test_constants_consistency.py` | **FAIL at 23:05 → PASS at 23:14** (V-001) | 6.1 s / 8.6 s |
| `tests/casim/test_supersession_ledger.py` | PASS — 19 PASS, 0 FAIL | 2.3 s |
| `tools/apply_supersession_banners.py --check` | PASS — 13 files, 13 ok | 0.1 s |
| `tools/audit_tests.py --ratchet` | PASS — nothing regressed | 2.8 s |
| `tools/audit_numerics.py --ratchet` | PASS — D8 has not regressed | 1.5 s |
| `tools/audit_constants.py --ratchet` | **FAIL `rogue_gate: 0 → 2` at 23:07 → PASS at 23:14** (V-001) | 5.9 s |
| `tools/check_test_registry.py` | PASS — 360 records, 26 gate, 47 declared debt | 1.9 s |
| `tools/gen_test_registry.py --check` | PASS — 360 records, 7 sector files | 2.2 s |
| `casim index --check` | PASS — all 7 targets, finding-number integrity clean | 5.2 s |
| `tools/gen_module_graph.py --check` | **STALE at 23:10 → current at 23:26** (V-001) | 3.1 s |
| `tools/check_deprecated.py` | PASS — 194 files accounted for | 0.6 s |
| `tools/check_module_registry.py` | PASS — 181 registered, 180 on disk, all covered | 1.5 s |
| `pytest tests/casim -m "not superseded and not slow"` | PASS — 209 passed, 2 skipped, 211 collected | ~55 s, run in 4 slices |
| `casim test --tier gate` | PASS — **26 of 26** | ~90 s, run in 5 slices |

The two 45-second-limit workarounds are recorded because they affect reproducibility: the
pytest run was split into four file groups (52 / 51+1s / 105 / 1+1s items) and the gate
tier into five `--id` batches. **Note for future sessions: `casim test --id` does not
accumulate** — repeating the flag silently keeps only the last value, which is why the
batches are shell loops over single `--id` invocations rather than one multi-flag call.
That is a latent foot-gun worth a one-line fix in `cli.py` (P4/P5 claim; not touched).

All 26 gate records, individually:

```
F272-F273-bz-period-lattices  PASS  6.2s  8 passed      chiral-core-caching   PASS  2.7s   4 passed
P3.2-engine-clock             PASS  2.7s  9 passed      constants-consistency PASS  8.6s  12 passed
P3.3-exchange-bus             PASS  3.7s 10 passed      device-precision-gate PASS  2.6s   7p 1s
P3.4-P3.6-total-energy…       PASS 18.5s 13 passed      engine-reproduces-…   PASS  2.9s   7 passed
backend                       PASS  2.7s  4 passed      fft-backend-equival…  PASS  2.7s   9 passed
casim-exactness               PASS  3.3s 14 passed      field-dump-vtk        PASS  2.7s   9 passed
checkpoint-ops                PASS  2.8s 10 passed      gravity-element       PASS  3.1s   6 passed
gui-render-spinor             PASS  2.7s  6 passed      registry-integrity    PASS  2.8s   7 passed
index-integrity               PASS  9.6s  7 passed      results-compare       PASS  2.7s   5 passed
particle-layer                PASS  4.4s 23 passed      scenario-schema-v2    PASS  3.2s  12 passed
registry-entries              PASS  2.7s  1p 1s (V-003) supersession-ledger   PASS  4.6s  21 passed
viz-api                       PASS  3.6s  5 passed
scenario-bcc-weyl             PASS  0.0s  3 gated observables within tolerance   (V-005)
scenario-gluon-bcc            PASS  0.1s  1 gated observable  within tolerance   (V-005)
scenario-photon-pair          PASS  0.2s  2 gated observables within tolerance   (V-005)
```

### V1.1 — device FFT ratchet and the machine floor — all three sub-claims hold

- **`device_fft_call_sites` is still 8**, and all 8 are in one file,
  `src/casim/engine/gauge/weak_wmu.py` (lines 842, 843, 848, 849, 855, 856, 859, 860),
  split between `_chiral_kernel` and `_massive_kernel` inside `_ensure_jax_kernels`.
- **`require_float64` guards them.** The guard is at `weak_wmu.py:798`, inside
  `use_jax(enabled=True)` — the opt-in switch — rather than at the call sites. Structurally
  this is sound: `_ensure_jax_kernels` is only reachable after `use_jax(True)`, so the
  guard dominates every path to the 8 calls. **One honest caveat:** because the guard fires
  at enable time and not at call time, flipping `jax.config` x64 *after* `use_jax(True)`
  would not re-trip it. Not a defect today (nothing in the tree does that); recorded so the
  claim is not stronger than the code.
- **`precision.MACHINE_GATE == casim.baselines.MACHINE_FLOOR`.** Both are `1e-12`. They are
  two separate literals (`is` returns `False`), which is exactly the drift risk the prompt
  names — **but the binding assertion exists**, at
  `tests/casim/test_device_precision_gate.py:65`, and it is a gate-tier test that ran and
  passed. The concern is answered. Worth noting for V7: `1e-12` is a load-bearing number
  written as a bare literal in two places and is **not** in the D7 constants registry, so
  the rogue-literal sweep cannot see it; the single assertion is the only thing holding
  them together.

### V1.3 — every engine `.py` accounted for by name

| Population | Count |
|---|---:|
| `.py` under `src/casim/engine/` (excl. `__pycache__`) | **194** |
| — of which `__init__.py` | 13 |
| — of which modules | **181** |
| module registry records | **181** |
| registered but not on disk | **0** |
| on disk (non-init) but not registered | **1** — `src/casim/engine/registry.py` |
| `__init__.py` files that *are* registered | **1** — `src/casim/engine/forks/__init__.py` |

So 181 records = 180 modules + `forks/__init__.py`, and 194 files = 181 modules + 13
`__init__.py`. The one module the registry does not hold is the registry itself, which
`check_module_registry.py` excludes by design — hence its "181 modules registered; 180
module file(s) on disk, all covered", which is internally consistent once the
`forks/__init__.py` record is accounted for.

**`check_module_registry.py` therefore has no hole.** The prompt's hypothesis ("if it is
green with a gap, the check has a hole and that is a finding") does not fire. The roadmap's
explanation — 6 of the gap being fork `__init__.py` files — is wrong: exactly one
`__init__.py` is registered, and the gap is 13 unregistered `__init__.py` files plus
`registry.py`.

Registry composition, for the record: origin `manifest` 168 / `spine` 13; sectors
interactions 51, forks 47, gauge 31, particles 22, core 17, lattice 13.

---

### V9 (partial) — re-run sample and arithmetic check over V0/V1

Per V9.1, a sample of the passing verdicts was re-run in a fresh interpreter and all
reproduced identically:

| Re-run | First reading | Second reading |
|---|---|---|
| `test_supersession_ledger.py` | 19 PASS, 0 FAIL | 19 PASS, 0 FAIL |
| `check_module_registry.py` | 181 registered / 180 on disk | identical |
| gate record `particle-layer` | PASS 4.4 s, 23 passed | PASS 4.4 s, 23 passed |
| gate record `scenario-photon-pair` | PASS 0.2 s, 2 gated observables | identical |
| `audit_constants.py --ratchet` | ratchet OK | ratchet OK |

Per V9.2, every count, sum and ratio in this report was re-derived programmatically and
asserted: the pytest totals (52+51+105+1 = 209 passed, +2 skipped = 211 collected), the
engine-file reconciliation (181+13 = 194; 180+1 = 181; 168+13 = 181; sector split = 181),
the record breakdowns (217+93+47+3 = 360; 334+26 = 360), the constants sectors
(25+7+7+2+2 = 43), both arming-journal partitions (=226 each way), the graph reach totals
(52/3/92/31/9, summing to 187), and the two drift readings quoted as inferences —
`FA_lgt_mc`'s plaquette move of **1.247e-3** against its own `sem_rel` of **3.114e-3**
(inside one SEM), and `FG7b results[5]` at **4.519e-5** relative. All asserted, all passed.

**V9 over V2/V3.** A second sample re-run in a fresh interpreter reproduced every verdict:
`bcc_unitarity_residual(0.7,0.3,1.1)` = **0.0**; $\Omega_\text{pair}(0)$ = **0.0**; on-axis
max error at $L{=}32$ = $6.661\times10^{-16}$ (identical to the first reading); doublers at
$L{=}48$ = 1 zero / 0 $\pi$; body-diagonal $\Omega/\lvert k\rvert$ at $\lvert k\rvert=1$ =
$0.57378447$ (identical).

Arithmetic asserted programmatically: the F30 series identity
$2\omega^+(k/2)=k/\sqrt3-\sqrt3k^2/54-\sqrt3k^3/486$ **`simplify` → 0, exact**; the three
convergence orders (2.000 / 0.967 / 2.000); F271's $1/n^3$ ratios (8.01, 8.00, 8.00, 8.00
against $2^3$); F87's sub-floor class maximum ($5.33\times10^{-15}<10^{-12}$) and its full
26-delta partition (17 + 4 + 4 + 1 = 26); and V-014's plateau (0.23% over a 32×
refinement, reported as 0.2%).

**Not done:** V9.5's verification subagent and V9.4's final full-gate re-run belong at the
close of the whole audit; the gate was re-confirmed green after V1 and again after V3.

## V9 — verifying the audit

### V9.1 — re-run sample

A seeded random 10% of the gate tier (`random.seed(20260801)` → `particle-layer`,
`scenario-gluon-bcc`, `scenario-bcc-weyl`) reproduced identically. Earlier blocks each
carried their own re-run sample; all reproduced.

### V9.2 — arithmetic, checked programmatically

**27 assertions over every percentage, dex, ratio and count in this report**, re-derived
from the raw figures rather than copied: the V8 residuals (sin²θ_W +0.22%, m_Z/m_W −0.064%
and the UV +1.77%, α_s at both +1.7% and the historical +1.3%, deuteron 0.026%, √σ/f_π
12.24%, T_c 14.26%, ρ_Λ 0.101 dex, m_n−m_p +17%, nucleon −1.05%, "27× better"), the V4.3
lattice identities ($a^3/2=4/(3\sqrt3)=4\sqrt3/9$, BZ/cube 1.2990, $4\pi/a=2\pi\sqrt3$),
F276's $6.3\times10^7$ gain and 0.23% plateau, V-023's 5.7× and 0.024% convergence, and
every partition (reach 51+4+90+26+10=181, exactness 12+16+14+1=43, channels 6+10+13=29,
F87 17+4+4+1=26, pytest 209+2=211, engine 181+13=194). **All passed.**

### V9.3 — tree state

`git status` cannot serve here (**V-010**): `HEAD` predates the C9 restructure, so hundreds
of files are legitimately dirty before this audit writes anything. Using the snapshot-diff
formulation V-010 recommends, this session's footprint is:

**Modified:** `src/casim/engine/lattice/curved.py` (F276), `src/casim/engine/registry.py`
(V7.4), `scenarios/refraction_2d.yaml`, `tests/registry/lattice.yaml`,
`docs/design/module-migration-manifest.yaml` (the claim), `docs/status/changelog.md`, and
the regenerated indexes (`code-index.md`, `docs-index.md`, `module-graph.json`,
`manifest.json`).
**Added:** this report, `findings/F276-*.md`, `tools/audit_v_battery.sh`,
`test-results/audit-v/`.
**Baselines:** unchanged. All eight that this audit's re-runs rewrote (F67, F69, F72, F87,
F91, F100, F244, F238) were restored with `git show HEAD:… > …`. Only the pre-existing
modifications recorded in the V0 table remain, and **nothing was staged**.

### V9.4 — final gate

Re-run at close: all nine ratchets/checks OK, `casim index --check` clean, constants gate
12 PASS / 0 FAIL, supersession ledger 19 PASS / 0 FAIL, and the gate tier at **27** records
(26 at open, +1 for F276). **The tree is in a better state than it was found in**, by the
one measurable step of the F276 repair and the V7.4 fix.

### V9.5 — the verification subagent

Given this report and one instruction — *find every claim the evidence does not support* —
an independent pass returned **16 findings**. All are folded in at their point of
correction, marked `[V9.5]`. The consequential ones:

| # | Severity | What it caught |
|---|---|---|
| 1 | **WRONG** | The status header said "V8 and V9 NOT STARTED" while a complete V8 sat 1300 lines below, and the UNVERIFIED table carried **duplicate rows with opposite verdicts**. Fixed |
| 2 | **OVERSTATED** | The no-doubler verdict is **conditional on Reading 1** — $\sqrt3\pi$ is exactly the BCC **H point**, so the $\omega=\pi$ mode sits on the true zone boundary, not merely "outside the cube". Verified to $<10^{-12}$ and now stated |
| 3 | **WRONG evidence** | The `photon_pair` lines quoted as "four lines apart" are 81 apart and in a *diagnostic*, not the propagator. Conclusion survives by the real route |
| 4 | **WRONG** | Two incompatible pre-F276 norm tables (6.1% vs 4.18e-2) for a stated-identical configuration — different initial data, now reconciled |
| 5,6 | WRONG / UNSUPPORTED | Face-diagonal figure −9.6e-4 → **−8.7e-4**; `pair_birefringence` "up to −0.447" → **[−2.03, +2.13]** on the L=32 cube |
| 15 | **OVERSTATED** | Gauss "flat in $L$" → **bounded and sub-linear** (rises 1.82× over a 6× range); "exactly conserved to machine precision" was two claims stacked |
| 7–14, 16 | NITPICK | F162 has **two** deltas not one (second is 1.4e-15); the "63.05" periodicity residual is grid-dependent; `gluon_self_energy:173` is **unconditional**, not in a `rule` branch; **29** channels not 20; `channels.py:86` not 78 (and four such imports); **two of four** "not c_lat" comments not three; the tests/ split is 11/2/14 not 7/2/18; `hypercharge.py:117-122`; 26 → 27 gate records |

**What it verified and could not fault:** every V2 symbolic claim (the unitarity identity,
the typo failing identically, the tetrahedral hop sum, $\det U=1$, $\operatorname{tr}U=2u$,
$c_\text{lat}$ isotropy), F105's on-axis figures digit for digit, the V3 photon numbers
($\Omega_\max=2.5915842645$, zone-edge agreement to $5\times10^{-16}$, transversality
3.4–4.9e-16), **V-023's entire sign-flip table digit for digit** with all three line numbers
exact, V4.3's lattice identities, the F265 plaquette closed form, V4.1's partition name for
name, F30's series, and **all five "nothing does X" claims** (V-016, V-017, V-003, V3.6,
V6.5).

It also flagged, correctly, that it could not check items requiring a re-run of committed
baselines or a harness this report does not ship — V6.4's Gauss harness among them. That is
a fair criticism: **the measurement scripts for V6.4, V6.6 and V-023 live only in this
session's transcript.** B5 in the Tier-B battery now ships the V-023 one; the other two
should be promoted to registry records rather than left as prose.

### V-005 — closed

The three scenario gates completing in 0.0–0.2 s **do run real physics**: `bcc_weyl` 200
ticks, `gluon_bcc` 150, `photon_pair` 40, with maximum state changes of 6.01, 6.53 and 5.19
respectively. They are fast because they are small lattices with spectral steppers, not
because they short-circuit. **Not a defect.**

### V2.4 extended

`tools/audit_v_battery.sh --only B3` ran here and extends the doubler sweep to **$L=96$ and
$L=128$**: 1 zero at the origin, 0 $\omega=\pi$, both branches, $\omega_\max<\pi$. The
sweep now covers $L\in\{24,25,33,36,48,64,96,128\}$.

---

## UNVERIFIED — what this audit could not run, and why

**This section is mandatory and is not a failure.** Coverage at the close of V1:

| Item | Status | Why |
|---|---|---|
| **V2** — foundation | **COMPLETE.** V-Q1 answered: sound | — |
| **V3** — the photon | **COMPLETE.** V-Q2 answered: sound | — |
| V2.5 — the `git mv` to `cubic.py` | **NOT PERFORMED** | Mount refuses `unlink`; commands (corrected for the 27 test-side imports, **V-018**) are in the handoff for Ben to run deliberately |
| V3.4 — the 55 F270-affected dumps move by exactly $2\times$ | **NOT VERIFIED** | Tier B by construction: re-running rewrites 55 committed baselines and the audit may not stage them. In the handoff |
| V3.5 — $[R_b,\text{evolution}]=0$ for **sourced** propagators | **STILL OPEN** | Asked by the 2026-06-29 audit, unclosed. Free even/chiral/Weyl laws are covered (F129/F130/F133/F134); no matter-coupled channel is tested under $R_b$, and the gravity case is the one the engine explicitly refuses |
| V2.4 at $L>64$ | **NOT RUN** | $L=24,36,48,64$ and odd $25,33$ all clean; larger $L$ is in the handoff |
| Long photon propagation runs | **NOT RUN** | 45 s cap. Longest here is 200 ticks at $L\le25$ |
| **V4** — cubic/BCC partition and the BZ question | **COMPLETE** (does not *decide* V4.3, by design) | — |
| **V5** — sector-by-sector | **PARTIAL, coverage stated** | 45 s cap makes a full 361-record sweep Tier B. See the V5 table for exactly what ran |
| V4.3 — the constructive discriminating test | **NOT BUILT** | Recommended, specified, in the handoff. This audit deliberately does not decide Reading 1 vs 2 |
| V4.4 — the remaining `lpt_*` measure re-derivation against the $\sqrt3$ period | **NOT DONE** | Classified (Wilson zone is correct as written); re-deriving the BCC-BZ vertex is F155/F239's open production job |
| V4.5 — exhaustive scope-note audit of F265's middle bucket | **SPOT-CHECKED ONLY** | `src/` side verified for the gravity set; the full 14-finding sweep is not done |
| V-023 — the three refold fixes and their re-runs | **NOT DONE** | Physics; outside the audit's authority. Diagnosed and quantified only |
| **V6** — cross-sector consistency | **COMPLETE** | — |
| **V7** — constants, exactness, ratchets | **COMPLETE** | `exactness` population deliberately not attempted (P6 work, not plumbing) |
| V6.4 — **SU(3)** Gauss law, and a full three-sector engine scenario | **NOT TESTED** | Only the U(1) sector at kernel level. F43/FG-7 and a live `quark_dirac`+`gluon_sourced`+`photon_sourced` stack remain open |
| V6.2 — the shipped 3.4e-14 conservation figure | **NOT REPRODUCED EXACTLY** | Re-ran the same physics at 1.70e-13 with different initial-data normalisation; both machine class, but the exact shipped number was not reproduced |
| **V9** — verify the audit | **COMPLETE** | 10% re-run sample, 27 programmatic arithmetic assertions, final gate, and V9.5's subagent (16 findings, all folded in) |
| `tools/audit_v_battery.sh` | **NOT WRITTEN** | Tier-B handoff, due at audit close |
| `test-results/audit-v/MANIFEST.md` | **NOT WRITTEN** | Same |
| Whole-file `pytest tests/casim` in one process | **NOT RUN** | 45 s cap. Run as four disjoint file groups; totals sum to the 211-item collection, but a single-process run could in principle differ through inter-test state. Recorded as a known reproducibility caveat |
| Whole `casim test --tier gate` in one process | **NOT RUN** | Same, five `--id` batches |
| `make drift` after a re-run | **NOT RUN** | Trap #1. The four drifting files were characterised from their committed state, **not** re-run. `FA_lgt_mc`'s "within one SEM" reading is an inference from the file's own `sem_rel`, not a fresh Monte Carlo |
| `make health` / `registry` / `numerics` / `structure` as Make targets | **PARTIAL** | The underlying tools were run individually; the Make wrappers were not |

**Audit-integrity caveat, applying to everything above.** The `cowork-p4-p5` session was
writing to the tree throughout. **Four** measurements demonstrably changed underneath this
audit inside a 30-minute window:

| Quantity | At audit open | 30 minutes later |
|---|---|---|
| rogue literals in `src/` | 2 (gate **RED**) | 0 (gate green) — fixed at 23:14:11 |
| `docs/design/module-graph.json` | **stale** | current — regenerated at 23:15:28 |
| findings files / max number | 268 / F273 | 270 / **F275** |
| `docs/status/changelog.md` | ends at F273 entry | ends at F275 / P5 entry |

Any V0/V1 number in this report is a reading at its stated timestamp, not a property of a
frozen tree. **F275 is the max finding number as of 23:33** — a later session must
re-check rather than trust this document.

---

## Recommended priority order

**Physics first:**

1. **V-023 — remove the `% 2π` refold from the three remaining sites.** One line each, with
   F272 as the worked precedent. In vacuum polarization it currently flips the sign of the
   measured quantity. Re-run F251/F258/F261/F264/F249 and the `gluon_self_energy` leg
   afterwards and triage what moves. **Highest item.**
2. **V4.3 — settle the mode-sum question with the constructive test.** Build the walk on an
   explicit two-sublattice BCC site set with integer hops and measure
   $\langle\cot\omega\rangle$ there: cube value → Reading 1, zero → Reading 2. It is the one
   experiment that discriminates, and no measurement on the current array-based code can.
   Note the stakes are now bounded: the spectrum survives either way (V4.3d).
3. **V-014 — done (F276).** Follow-up: **any F64-fork variable-$c$ number quoted from before
   2026-08-01 should be re-run** before it is used quantitatively.
4. **V-013 / V-021 — clean the drift signal.** Stop diffing wall-clock time, then re-triage
   the 28 FAILs. F87's recommended verdict is **accept**; F100's entire drift is a timing
   field. Both are one mechanical change away from being provably noise.
5. **V-024 — withdraw the horizon-free black hole from
   `papers/Claims-and-Falsifiers-Summary.md`.** It is currently published as a live
   falsifier for a prediction the model no longer makes.

**Then correctness of the record:**

4. **V-012** — make the photon propagator one object, not a bit-identical copy. Same defect
   class F270 fixed for `field_energy`; the docstrings already claim the fixed state.
5. **V-016 / V-017** — two missing assertions on load-bearing claims: nothing guards the
   $c_\text{lat}$ / `q_star_a_band_lo` separation, and F105 has no test of its own.
6. **V-018** — correct the `cubic.py` handoff before anyone runs it; it undercounts by 27
   import sites across 23 test files.
7. **V-004** — correct `CLAUDE.md`'s "what `pytest` runs, by construction": a bare `pytest`
   skips the three scenario gates, which are the physics ones.
8. **V-003** — decide whether `entry:` is the convention or the aspiration.

**Then hygiene:**

9. **V-015** — move `bcc_dispersion` to the `atan2` form, or document the small-$k$ floor.
10. **V-019 / V-020 / V-009 / V-002 / V-011** — one-line documentation and plumbing fixes.
11. **V-006 / V-007 / V-008** — P6 reach/exactness plumbing; batch at V7.
12. **V-001 / V-010** — process: adopt the snapshot-diff formulation for V9.3.

**Still to run:** V4, V5, V6, V7, V8, and V9's subagent pass.

---

## Appendix — reproduction

```bash
cd "<repo root>"
source .vendor/activate.sh
export PYTHONPATH="$PWD/src:$PYTHONPATH"

# gate, one call each (45 s cap)
python3 tests/casim/test_constants_consistency.py
python3 tests/casim/test_supersession_ledger.py
python3 tools/apply_supersession_banners.py --check
python3 tools/audit_tests.py --ratchet
python3 tools/audit_numerics.py --ratchet
python3 tools/audit_constants.py --ratchet
python3 tools/check_test_registry.py
python3 tools/gen_test_registry.py --check
python3 -m casim.cli index --check
python3 tools/gen_module_graph.py --check
python3 tools/check_deprecated.py
python3 tools/check_module_registry.py

# pytest, four disjoint groups (see logs)
# gate tier, one --id at a time — `--id` does NOT accumulate
for id in $(python3 -c "from casim.tests import registry as T; \
    print(' '.join(r.id for r in T.all_records() if r.tier=='gate'))"); do
  python3 -m casim.cli test --id "$id"
done
```

Raw output for every V1 check is under `test-results/audit-v/logs/`.
