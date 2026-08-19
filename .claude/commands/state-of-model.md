# /state-of-model — Completeness overview of the model as it stands

Grade the whole model against an **external** rubric: what a well-built, robust fundamental
physics theory has to account for. Produce **two** dated files in `docs/status/`: the graded
report, and a companion file of **research prompts** — one self-contained, paste-ready prompt
for every row that did not come back `EXACT` or `MACHINE`, aimed at moving it up the ladder.

`$ARGUMENTS` may name one sector to restrict to (`gravity`, `qcd`, `ew`, `lepton`,
`cosmology`, `foundations`, `qed`, `nuclear`). Empty = full sweep.

> **This is a review, not research.** Do not open a claim in
> `docs/design/session-claims.yaml`, do not write a finding, do not change physics. If the
> sweep turns up a genuine new result, stop, claim numbers first, and do that in a separate
> session. The output of this command is **two markdown files** — the report and its prompt
> companion — and nothing else. Writing a prompt that *says* "derive X" is not deriving X, and
> is the only sanctioned way this command may point at future physics.

> **The rubric is the point.** The repo already grades itself against itself
> (`open-derivations.md`, `exactness-inventory.md`, `Claims-and-Falsifiers-Summary.md`).
> Those answer "how are our open items doing". This command answers a different question:
> **what does a complete theory owe, and which of those debts have we not even opened a line
> for?** The most valuable cell in the report is `ABSENT` — a thing the model has no sector
> for at all, which therefore appears in none of the internal ledgers.

---

## Step 0 — Timestamp

```bash
date "+%Y-%m-%d - %H:%M"
```

Report file is `docs/status/completeness-{yyyy-mm-dd}.md`. If one already exists for today,
append `-b`, `-c`, … rather than overwriting.

The companion prompt file is `docs/status/completeness-{yyyy-mm-dd}-prompts.md`, carrying the
**same** suffix letter as its report (`completeness-2026-08-19-b-prompts.md`). The two files are
issued together and are read together; a report without its companion is an incomplete run.

---

## Step 1 — Load context (small files only)

Read, in this order:

- `INDEX.md`
- `findings-index.md`
- `docs/status/open-derivations.md` — the internal OPEN / CLOSED-NEGATIVE / CLOSED-BY-DECISION ledger
- `docs/status/exactness-inventory.md` — read the **tier headers, the generated tally, and the
  "Currently failing / not-yet-met" section**; do not read all 1000+ lines of rows
- `papers/Claims-and-Falsifiers-Summary.md` — the external-facing claim register, including its
  **"Scope — what is *not* claimed"** section, which is the single richest source of honest
  `OPEN`/`ABSENT` grades in the repo
- `docs/theory/key-decisions.md` — the adopted posits (physics decisions and D1–D11)
- `docs/theory/supersessions.yaml` — what has been retracted
- `project-status-index.md`
- `tail -n 200 docs/status/changelog.md`
- The previous `docs/status/completeness-*.md`, if any (newest only)

Do **not** load `references/physics-notes-complete.md`, the full `project-status.md`, or a
directory of findings. Pull individual `findings/F{N}-*.md` only when a rubric row cannot be
graded from the ledgers — and note in the report which rows needed that.

**Cheap way to find `ABSENT` rows.** Grep the *whole tree* for the rubric keyword, not just
`findings-index.md` — a finding may cover a topic without the word appearing in its one-line
summary. Zero hits across `findings/`, `papers/` and `docs/theory/` is strong evidence of
`ABSENT`; a handful of hits usually turns out to be passing mentions, so read them before
grading.

```bash
for k in "CKM" "nucleosynthesis\|BBN" "inflaton" "spin-statistics" "sigma_8"; do
  printf "%-30s findings:%3s papers:%3s docs:%3s\n" "$k" \
    "$(grep -rli "$k" findings/ | wc -l)" \
    "$(grep -rli "$k" papers/*.md | wc -l)" \
    "$(grep -rli "$k" docs/ | wc -l)"
done
```

---

## Step 2 — Live health probe

The rubric grades *claims*; this step checks the claims still *run*. Run from the repo root,
**one target per bash call** — a single sandbox call dies at ~45 s. Use the `make` targets,
not bare `casim`: the Makefile exports `PYTHONPATH=src`.

```bash
source "$PWD/.vendor/activate.sh"   # vendored scipy/numpy/pytest; never pip install
make indexes-check                  # = casim index --check — are the indexes stale?
make registry                       # test-registry coverage
make numerics                       # D8 compliance
make health                         # suite health
```

`make gate` is the real barrier but takes ~2 min, so it will usually not fit in one call. If it
times out, record it as `NOT VERIFIED THIS RUN` and hand Ben the command — never report a gate
as green that you did not see go green. Remember pytest is *not* the barrier: it cannot collect
the three `kind: scenario` gate records, which are the physics gates.

Record for the report header: gate-tier record count, the max finding number, the exactness
tally (exact / machine / quantitative), and the module reach split:

```bash
PYTHONPATH=src python3 -c "
from casim.engine.registry import all_modules
from collections import Counter
m=list(all_modules()); print(len(m), Counter(x.reach for x in m).most_common())"
```

---

## Step 3 — Grading vocabulary

Every rubric row gets exactly one grade. The vocabulary is closed; do not invent a grade.

| Grade | Meaning |
|---|---|
| `EXACT` | Derived in closed form, algebraically exact, zero free parameters |
| `MACHINE` | Derived, verified to the numerical floor ($10^{-12}$–$10^{-16}$), zero free parameters |
| `QUANT` | Reproduces measurement within a stated tolerance; residual must be quoted |
| `PARTIAL` | Derived up to one *named* residual constant or seam — name it |
| `FIT` | Reproduced, but with $N$ fitted inputs — state $N$ and what they are |
| `POSIT` | Adopted founding decision; alternatives demonstrably closed (open-derivations Part C) |
| `OPEN` | A live target in the internal ledger; attack identified |
| `EXCLUDED` | Closed-negative — a proven no-go. This is a *result*, not a gap |
| `ABSENT` | **The model has no sector for this at all.** Not in any ledger. The real gaps |
| `WITHDRAWN` | Was claimed publicly, since retracted (check `supersessions.yaml`) |
| `N/A` | A Standard-Model artefact this model structurally does not need — justify in one line |

`ABSENT` and `N/A` require the most care and are the two most likely to be graded wrong. A
thing is `N/A` only if the model *explains away* the need; it is `ABSENT` if the model simply
has nothing to say. Do not launder an `ABSENT` into an `N/A` because the model is elegant
elsewhere. Note that **the Higgs field is not `N/A`** — the model does not dispense with it,
it *replaces* it with a specific mechanism (F27 chiral $SU(2)$), which gets graded on its own
merits at B5.

`EXCLUDED` is a *result*: a proven no-go closes a question. But when the excluded thing is the
**derivability of a parameter**, say so — "permanently free, cause named" is the honest
reading, not "answered".

---

## Step 4 — The rubric

Grade every row. Cite the finding number(s) and, where the grade is `QUANT` or `FIT`, the
residual and the input count. **Escape literal pipes as `\|`** inside table cells.

Blocks are **A, B, C, D, E, K, G, H**. Cosmology is **K**, not F — `F` is the finding-number
namespace, and `F1`–`F12` row IDs are unreadable next to it.

### A — Foundations (what any theory of everything owes)

| # | Requirement |
|---|---|
| A1 | Spacetime dimensionality — why 3+1. Note the BDPT uniqueness theorem forces the walk *given* 3D and does not select 3 |
| A2 | Lorentz invariance — exact, emergent, or bounded LIV with the bound quoted |
| A3 | Causality / locality / finite signal speed |
| A4 | CPT and its individual factors (C, P, T) |
| A5 | Unitarity of the evolution |
| A6 | Quantum superposition + Born rule — derived, or merely reproduced |
| A7 | Entanglement and Bell/Tsirelson behaviour |
| A8 | The measurement problem / classical emergence |
| A9 | Spin-statistics connection — *implemented* is not *derived* |
| A10 | Cluster decomposition / no superluminal signalling |
| A11 | UV completeness — the lattice cutoff vs the renormalisation program run on top of it |
| A12 | Continuum limit — does the lattice recover continuum physics, and how is that shown |

### B — Gauge structure

| # | Requirement |
|---|---|
| B1 | Origin of $SU(3)\times SU(2)_L\times U(1)_Y$ — grade sector by sector, they differ |
| B2 | Chirality — why $SU(2)$ acts only on left-handed fields |
| B3 | Anomaly cancellation (gauge, gravitational, Witten) |
| B4 | Hypercharge assignments and charge quantisation |
| B5 | Electroweak symmetry breaking mechanism |
| B6 | Weinberg angle, with its scale |
| B7 | Confinement |
| B8 | Asymptotic freedom / running of $\alpha_s$ |
| B9 | Running of $\alpha$ and the electroweak couplings |
| B10 | Why 3 colours |
| B11 | Strong-CP: is $\theta_\text{QCD}$ zero, and does it survive loops |
| B12 | Gauge-boson masses — separate the *ratio* from the *absolute scale* |

### C — Matter content

| # | Requirement |
|---|---|
| C1 | Exactly three generations — separate the group-theory theorem from the physical-identification hypothesis |
| C2 | The full first-generation multiplet structure |
| C3 | Quark colour triplet + fractional charge |
| C4 | Neutrino nature — Dirac vs Majorana. Is *either* forced? |
| C5 | Neutrino mass mechanism — mechanism vs absolute scale |
| C6 | Antimatter / charge conjugation as a sector |
| C7 | Beyond-SM content the model predicts, and what it has excluded |

### D — The parameter ledger

The sharpest test: the SM has **19** free parameters (+7 for Dirac neutrinos, +2 more if
Majorana, +2 gravitational/cosmological). One row each, same vocabulary. End the section with
a headline: *"$n$ of 28 derived, $p$ partial, $m$ fitted, $k$ open/absent."*

| Block | Parameters |
|---|---|
| Quark masses (6) | $m_u, m_d, m_s, m_c, m_b, m_t$ |
| Charged-lepton masses (3) | $m_e, m_\mu, m_\tau$ |
| CKM (4) | 3 angles + 1 CP phase |
| Gauge couplings (3) | $g_1, g_2, g_3$ (equivalently $\alpha,\ \sin^2\theta_W,\ \alpha_s$) |
| Higgs sector (2) | $v$ and $m_H$ (or $\mu,\lambda$) |
| Strong CP (1) | $\theta_\text{QCD}$ |
| Neutrino (7) | 3 masses + 3 PMNS angles + 1 Dirac phase (+2 Majorana phases if applicable) |
| Gravitational / cosmological (2) | $G$ and $\Lambda$ |

Grade honestly:

- A mass that comes out of a relation *given* one anchor is `FIT` with $N=1$, not `EXACT`.
- **If the *shape* is derived but the *scale* is anchored, split the row.** Mass ratios and the
  overall scale are different parameters and deserve different grades.
- A quantity derived from another derived quantity is only as exact as its weakest input —
  propagate the grade.
- **Do not let the headline drift** from "the sectors we built carry zero free parameters" to
  "we beat the SM's 19". Those are different claims and usually only the first is supportable.

### E — Gravity and general relativity

| # | Requirement |
|---|---|
| E1 | Field equation — what is the fundamental law |
| E2 | Equivalence principle |
| E3 | PPN parameters $\beta,\gamma$ |
| E4 | Classical tests: perihelion precession, light deflection, Shapiro delay, gravitational redshift |
| E5 | Newton's constant — derived or input |
| E6 | Gravitational waves: speed, polarisation content, dof count |
| E7 | Inspiral/merger waveforms and ringdown QNMs |
| E8 | Black holes: exact vacuum solution, horizon structure, shadow |
| E9 | Black-hole thermodynamics: area entropy, Hawking radiation |
| E10 | Singularities — resolved, or inherited |
| E11 | Interior solutions / TOV, neutron-star EoS |
| E12 | Gravity's quantum sector: graviton dof, mass, UV behaviour |
| E13 | Galactic-scale consistency (rotation curves with or without DM) |

### K — Cosmology

*Row IDs are `K`, never `F`.*

| # | Requirement |
|---|---|
| K1 | Expanding FRW background — *derived from* the lattice, or merely *solved with* the model's source? |
| K2 | Big-bang nucleosynthesis and light-element abundances |
| K3 | CMB: acoustic peak structure, spectral index $n_s$ |
| K4 | Inflation or a substitute for horizon/flatness |
| K5 | Primordial power spectrum normalisation |
| K6 | Baryogenesis — Sakharov conditions *met* is not the asymmetry *derived* |
| K7 | Dark-matter identity |
| K8 | Dark-matter abundance $\Omega_\text{DM}h^2 = 0.12$ |
| K9 | Dark energy: magnitude of $\Lambda$ |
| K10 | Dark energy: equation of state $w$, vs DESI |
| K11 | Structure formation / $\sigma_8$ |
| K12 | Cosmological initial conditions — posited vs derived |

### G — Emergent and precision physics (does it reproduce known measurements)

| # | Requirement |
|---|---|
| G1 | Maxwell's equations and classical EM |
| G2 | Hydrogen spectrum, fine structure, Lamb shift |
| G3 | QED precision: electron and muon $g-2$ — for the muon, check whether hadronic VP, HLbL and EW are computed or scoped out |
| G4 | Atomic structure beyond hydrogen; the periodic table |
| G5 | Hadron spectrum: $f_\pi$, $m_\pi$, string tension $\sqrt\sigma$, baryon masses |
| G6 | Nuclear binding: deuteron, saturation, $\alpha$ particle |
| G7 | Weak decays: $\beta$ decay, lifetimes, Fermi constant |
| G8 | Scattering: tree-level and loop-level cross-sections, S-matrix |
| G9 | Condensed-matter emergents already checked (superconductivity, slow light, Casimir, …) |
| G10 | Statistical mechanics / thermodynamics on the lattice |

### H — Model integrity (meta)

| # | Requirement |
|---|---|
| H1 | Parameter count vs the SM's 19+ — is the model *actually* cheaper? |
| H2 | Falsifiability: does every headline claim have a named killing experiment with a threshold |
| H3 | Out-of-sample survival: has any prediction survived a measurement revision |
| H4 | Retraction hygiene: is every withdrawn claim recorded — **and is any *derived* result still published as an input?** |
| H5 | Internal consistency: do the adopted decisions (CLAUDE.md 1–7, D1–D11) contradict each other anywhere |
| H6 | Reproducibility: does the gate run green, from a clean checkout |
| H7 | Module coverage: channel-driven vs test-only vs unreferenced |
| H8 | Findings with no test record — especially any cited as settled in a ledger |

---

## Step 5 — Delta since the previous run

If a previous `docs/status/completeness-*.md` exists, produce a table of rows whose grade
changed, in both directions. **Regressions get their own subsection** — a row that went
`QUANT → OPEN` because a finding was superseded is the single most important thing this
command can surface, and it will not appear in any index or changelog.

If no previous report exists, say so; this run becomes the baseline, and use the section
instead to flag rows *at risk* — e.g. a cited finding that has since been superseded with
downstream re-blessing unverified, or `candidate` baselines still failing by design.

---

## Step 6 — Write the report

`docs/status/completeness-{yyyy-mm-dd}.md`, in this shape:

```markdown
# Completeness overview — {yyyy-mm-dd - hh:mm}

*Graded against the external SM + GR + cosmology rubric in `.claude/commands/state-of-model.md`.
Scope: {full sweep | sector}. Health probe: {what actually ran}.
Research prompts for every row below `MACHINE`: `completeness-{yyyy-mm-dd}-prompts.md` ({N} prompts).*

## Scoreboard

| Block | EXACT | MACHINE | QUANT | PARTIAL | FIT | POSIT | OPEN | EXCLUDED | ABSENT | N/A |
|---|---|---|---|---|---|---|---|---|---|---|
| A Foundations | | | | | | | | | | |
| … | | | | | | | | | | |
| **Total** | | | | | | | | | | |

**Parameter ledger: {n} of 28 derived, {p} partial, {m} fitted, {k} open or absent.**

## The five things most worth building next

Ranked by (load-bearing × distance from closure). For each: what it is, why it matters,
what specifically blocks it, and the smallest next step. Prefer gaps that close several
rubric rows at once — those are the real leverage. These five head the priority table in the
prompt companion and are the rows that get a live literature pass (Step 7.5).

## What is ABSENT

The rows where the model has no sector at all — the list that does not appear in
`open-derivations.md`. Follow the table with a paragraph on what the *shape* of the list means.

## Regressions since {previous report date}

## Full rubric

{A, B, C, D, E, K, G, H tables: | # | Requirement | Grade | Evidence (F-numbers) | Residual / free inputs | Note |}

*Every row above whose grade is not `EXACT` or `MACHINE` has a prompt in
`completeness-{yyyy-mm-dd}-prompts.md` under the anchor of the same row ID.*

## Method notes

Which rows needed a finding file rather than the indexes; the three grades spot-checked and
what the check found; citations to superseded findings carried with their supersession;
anything the health probe could not verify this run.
```

Rules for the prose: no cheerleading, no restating the model's strengths. A completeness
report that reads like a press release is a failed completeness report. Where a grade is
arguable, state the argument in one line rather than picking silently.

---

## Step 7 — Write the companion research-prompt file

`docs/status/completeness-{yyyy-mm-dd}-prompts.md`. **One prompt per row that did not come back
`EXACT` or `MACHINE`** — every rubric row of A, B, C, E, K, G, H *and* every row of the D
parameter ledger.

**Who it is for.** A future session with **none of this session's context**, opening one prompt
and nothing else. Every prompt must be self-contained: a cold reader pastes it into a fresh
session and can start work without first opening the completeness report, this command file, or
any index. Cross-references buy depth; they must never be load-bearing for comprehension. The
test to apply before shipping a prompt: *strike out the rest of the file — does this still say
what the target is, what exists already, what is closed, and what to run first?*

**Nothing is exempt, including the closed rows.** `EXCLUDED` and `N/A` get prompts too — a
different *kind* of prompt (below), but they are not skipped. A no-go nobody ever re-examines is
indistinguishable from an assumption, and an `N/A` is a judgement the tree can outgrow.

**Coverage is a ratchet.** The prompt count must equal the sum of every scoreboard column
**except** `EXACT` and `MACHINE`, over both the rubric blocks and the D ledger. Print both
numbers in the companion's header and assert they match. If they do not, the report and the
companion disagree about what the model owes, and that is a defect to fix before issuing either.

### 7.1 — The ladder

The prompt's job is to name the *next rung*, not to wish for the top. State the target grade
explicitly, and where a further rung exists beyond it, name it in one clause so the session knows
the shape of the whole climb.

| From | Next rung | What earns the promotion |
|---|---|---|
| `ABSENT` | `OPEN` | a named attack, a first computation, and a row that a research session could open in `open-derivations.md`. Reaching `OPEN` is real progress here — do not write the prompt as though `EXACT` were one session away |
| `OPEN` | `QUANT` or `PARTIAL` | a number with a quoted residual, or a derivation down to one *named* seam |
| `FIT (N)` | `PARTIAL`, then `QUANT` | eliminate one anchor. Name **which** of the $N$ inputs is cheapest to kill and what would replace it |
| `POSIT` | derived, or `EXCLUDED` | either derive the posit or prove it underivable. Both are results; `open-derivations` Part C is the standing list |
| `WITHDRAWN` | `EXCLUDED`, or re-derived | does a repairable core survive the retraction, or should the retraction harden into a no-go |
| `QUANT` | `PARTIAL` | **name the residual.** Turn "agrees to $x\%$" into "derived up to this one object" — a named seam is strictly more informative than a tolerance, even at the same number |
| `PARTIAL` | `MACHINE` | compute the named residual/seam *from inside the model* and verify it to the numerical floor ($10^{-12}$–$10^{-16}$) with zero free parameters |
| `MACHINE` | `EXACT` | closed form, symbolically (sympy) rather than numerically. Say whether an exact form is plausibly *available* — for a row whose content is a measured lattice sum, `MACHINE` may be the ceiling, and saying so is worth more than an aspiration |
| `EXCLUDED` | stays `EXCLUDED` | re-examination, not re-attack — see 7.4 |
| `N/A` | stays `N/A` | re-justification against the current tree — see 7.4 |

### 7.2 — The reference bundle (findings, tests, code, claims)

Harvest mechanically and cheaply. **The claim card's front matter is the join table** — it
already carries `findings:`, `tests:`, `modules:`, `constants:` and `falsifier:` for its subject,
which is exactly the bundle each prompt owes. Do **not** read finding files in full for this
step; the report graded from the ledgers and the cards, and this step must not become the
expensive one.

```bash
# every claim card touching a finding, with its tests/modules/constants, off the generated projection
python3 - <<'PY'
import yaml
reg = yaml.safe_load(open('docs/claims/registry.yaml'))
want = {'F311', 'F319'}          # the row's evidence F-numbers
for c in reg['claims']:
    if want & set(c.get('findings') or []):
        print(c['id'], c['status'], c['exactness'], '| tier:', c['tier'],
              '| tests:', c.get('tests'), '| modules:', c.get('modules'),
              '| constants:', c.get('constants'), '| falsifier:', c.get('falsifier'))
PY

grep -rn "id: {record-id}" tests/registry/*.yaml     # tier, kind, path of a test record
grep -n  "{ledger row id}" docs/status/open-derivations.md
grep -n  "{F-number}"      docs/theory/supersessions.yaml
```

Each prompt's reference block lists, **with nothing invented and nothing rounded**:

- **Findings** — F-numbers with dates, each marked ⚠ if `supersessions.yaml` has it, carrying the
  superseding number. A prompt that sends a session at a superseded finding without saying so is
  worse than a prompt that omits it.
- **Claims** — CL ids with their `status:` and `tier:`, and the card's **`falsifier:`**. The
  falsifier is the prompt's own success/failure criterion. Quote it; do not invent a new one.
- **Tests** — registry record ids with tier (`gate`/`battery`) and kind, plus the command that
  runs them (`make gate`, `casim test {id}`), so the session can see the current state before
  touching anything.
- **Code** — module paths from the cards' `modules:`, and the D7 registered constants from
  `constants:`. Where a module is `unreferenced` or `fork_unclaimed` in the module registry, say
  so — that is often *why* the row is stuck.
- **Ledger** — the `open-derivations.md` row ID **and its Part** (A target / B closed-negative /
  C closed-by-decision / D contradiction), the `exactness-inventory.md` rows, and the rubric row.
  A row that appears in no ledger is the single most important thing the prompt can say.
- **Papers** — the section of `papers/Claims-and-Falsifiers-Summary.md` that carries it,
  **including any `Scope — what is not claimed` entry that disclaims it**. If the row is
  publicly disclaimed, promoting it obliges a summary edit; say so in the prompt.

### 7.3 — The do-not-re-attack block is mandatory

`open-derivations.md` Part B and its "Suggested attack" column already carry sentences of the
form *"do not re-attack the anomaly, the spatial-3 or the ℤ₃ routes — all three are closed with
reasons."* Every prompt carries the closed legs for its row **with the finding that closed
each**. This is the highest-value part of the prompt: re-attacking a settled no-go has cost this
project whole sessions, and a cold reader has no way to know. If a row has no closed legs, write
`none recorded` — never omit the block, because an absent block reads as "nothing is closed".

Where a row sits downstream of an unchosen branch or a live contradiction (`open-derivations`
Part D), the prompt says so at the top: *work here does not close until that fork is decided*.

### 7.4 — The four prompts that are not "go derive this"

- **`EXCLUDED` → re-examination.** The prompt names the **one assumption whose failure would
  reopen it** and asks for that assumption to be tested, not for the no-go to be beaten. State
  plainly that *"the no-go survives"* is a successful outcome and should be recorded as one. A
  no-go whose reopening condition is unnamed is not yet a result.
- **`N/A` → justification audit.** The model claimed it *explains away* the need. The prompt asks
  whether that argument still holds against the tree as it stands today, and what would demote
  the row back to `ABSENT`. Cheap, and it is the check that stops `N/A` becoming a dumping ground.
- **`POSIT` → derivability attack.** Aim at the posit itself: derive it, or prove it underivable
  and move it to Part B. Carry the alternatives already closed in `open-derivations` Part C.
- **`WITHDRAWN` → salvage or harden.** Was anything in the retracted claim independently sound?
  The prompt asks for the surviving core to be isolated, or for the retraction to be hardened
  into an `EXCLUDED` with a stated reason.

### 7.5 — External research: bounded, cited, and never laundered

Run a real literature pass **only** for the top tier — the rows in *"the five things most worth
building next"*, every `ABSENT` row, and any `EXCLUDED`/`N/A` row whose justification leans on an
external result. For those, use WebSearch and record, per source: collaboration or author, year,
arXiv id or DOI, the number **with its uncertainty**, and the date you searched.

Every other row gets **search terms and named sources** for the next session to run — the exact
queries, plus the standing anchors where they apply (PDG with its edition, FLAG, NuFIT, the
Planck or DESI data release, the specific review article). "No external anchor found, terms
tried: …" is a useful line; write it rather than leaving the block empty.

Budget the whole external pass at roughly **15 minutes**. Two hard rules:

1. **Never let an external number in without provenance.** An uncited number in a prompt will be
   treated as the model's own by the session that reads it.
2. **Never phrase a literature result as if the model produced it.** That is precisely the H4
   failure this rubric grades — a derived result published as an input, or here, an imported one
   published as derived.

### 7.6 — File shape

```markdown
# Research prompts — completeness {yyyy-mm-dd - hh:mm}

*Companion to `completeness-{yyyy-mm-dd}.md`. One paste-ready prompt per rubric or ledger row
graded below `MACHINE`. Coverage: {N} prompts against {N} non-EXACT/non-MACHINE rows
(scoreboard total {T} − EXACT {e} − MACHINE {m} = {N}) — **match**. External literature pass:
{which rows, searched {yyyy-mm-dd}}.*

**How to use one.** Paste a single fenced block into a fresh session. Each is self-contained.
Do not paste two — a session that claims two rows at once claims neither cleanly.

## Priority order

| Rank | Row | Grade → target | Why it is worth doing first | Est. cost |
|---|---|---|---|---|

{the five things first, then the rest by block}

## A — Foundations

### A2 — Lorentz invariance — `PARTIAL` → `MACHINE`

**Leverage:** {which other rows move with it}. **Cost:** {in-repo hours \| long run \| new sector}.
**Blocked by:** {fork or ledger row, or "nothing structural"}.

~~~text
Physics Notes research session. Target: rubric row A2 (Lorentz invariance), currently PARTIAL,
target MACHINE.

WHAT IS ALREADY TRUE: ...
THE RESIDUAL / WHAT IS MISSING: ...
DO NOT RE-ATTACK: ... (closed by F..., ...)
REFERENCES — findings: ...; claims: CL... (status, falsifier: ...); tests: ... (tier, how to run);
modules: ...; constants: ...; ledger: open-derivations {row}, Part {A|B|C|D}; papers: ...
EXTERNAL: ... (cited, with dates) / SEARCH TERMS: ...
FIRST STEP: ...
WHAT PROMOTES THE GRADE: ...
WHAT WOULD FALSIFY THE ATTEMPT: ...
PROTOCOL: this is research. Claim your topic in docs/design/session-claims.yaml before any
physics (/derive Step 0). Take finding numbers one at a time from `casim index` NEXT FREE NUMBER.
Close with the finding, its test record, and its claim card. `make gate` before you finish.
~~~

{…one section per row…}

## Method notes

Rows whose bundle needed a finding file rather than the cards; rows where the closed-leg block is
`none recorded`; which rows got a live literature pass and which got terms only; anything the
harvest could not resolve.
```

Use `~~~` for the prompt fence so the block survives being pasted into a ```` ``` ````-fenced
context, and keep the prompt body as plain text — no tables, no nested fences.

**Prose rules, same as the report.** A prompt that opens by praising the model wastes the first
line a cold session reads. Write the target, then the state, then the block list. If a row is
genuinely hopeless with current machinery, the prompt says so and says what would change that —
an honest *"nothing to do here until X lands"* is a legitimate prompt and better than busywork.

---

## Step 8 — Verify before finishing

1. **Spot-check three grades** against their cited finding files — pick the three you were
   least sure of, and record what the check found in Method notes. If any cited finding does
   not support the grade, fix the grade, not the citation.
2. **Check every F-number cited actually exists** (`ls findings/ | grep F{N}`). A citation to
   a superseded finding must carry the supersession.
3. **Check pipe escaping** — the report will be pulled into `docs-index.md`.
4. **Prompt coverage ratchet** — count the prompts in the companion and count the non-`EXACT`,
   non-`MACHINE` cells in the scoreboard plus the D ledger. Print both. They must be equal; if
   they are not, fix the file that is wrong before issuing either.
5. **Every id in the companion exists.** F-numbers (`ls findings/ | grep F{N}`), claim cards
   (`ls docs/claims/ | grep CL{N}`), test records (`grep -rn "id: {record}" tests/registry/`),
   module paths (`grep -rn "{module}" docs/design/module-registry.yaml` or the registry import).
   A prompt citing a record that does not exist sends a cold session hunting for nothing — this
   is the single most likely defect in the companion, because the bundle is assembled
   mechanically and never opened again.
6. **Read two prompts cold.** Pick the two whose rows you understand least well, and read each
   with the rest of the file covered. If either needs the report to make sense, rewrite it.
7. `make indexes` (confirm **both** new files appear in `docs-index.md`), then `make indexes-check`.
8. Add a one-paragraph `docs/status/changelog.md` entry, dated `yyyy-mm-dd - hh:mm`, naming both
   files and the prompt count.

Do **not** update `open-derivations.md` or `exactness-inventory.md` from this run. If the
sweep shows an item there is stale, say so in the report and let a research session act on it —
this command has no claim and must not edit the ledgers it grades against.

---

## Anti-patterns

- Grading from memory of the conversation instead of from the files.
- Reporting `make gate` green without having run it.
- Marking a row `EXACT` because the *method* is exact when the *input* was fitted.
- Turning `ABSENT` into `N/A` because the model is elegant elsewhere.
- Reading all of `findings/` — the indexes exist precisely so this command stays cheap.
- Opening a finding number, editing a ledger, or "fixing" physics mid-review.
- **A prompt whose body is "derive $X$".** If the prompt does not name what already exists, what
  is closed, and what to run first, it is a restatement of the rubric row, not a prompt.
- **A prompt that omits the do-not-re-attack block** — the most expensive defect this file can
  carry, because the cost lands on a session that cannot see the omission.
- **A prompt that skips `EXCLUDED` or `N/A`** because the row "isn't a gap". They are graded
  judgements, and the companion is where they get re-tested.
- **Aiming every prompt at `EXACT`.** `ABSENT → OPEN` is a real promotion; writing it as though
  closed form were one session away makes the file useless as a work queue.
- **Reading finding files in full to build the bundles** — the claim cards' front matter is the
  join table, and Step 7 must not become the expensive step.
- **An external number without provenance**, or a literature result phrased as the model's own.
