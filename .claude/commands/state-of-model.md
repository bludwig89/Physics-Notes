# /state-of-model — Completeness overview of the model as it stands

Grade the whole model against an **external** rubric: what a well-built, robust fundamental
physics theory has to account for. Produce a dated report in `docs/status/`.

`$ARGUMENTS` may name one sector to restrict to (`gravity`, `qcd`, `ew`, `lepton`,
`cosmology`, `foundations`, `qed`, `nuclear`). Empty = full sweep.

> **This is a review, not research.** Do not open a claim in
> `docs/design/session-claims.yaml`, do not write a finding, do not change physics. If the
> sweep turns up a genuine new result, stop, claim numbers first, and do that in a separate
> session. The output of this command is one markdown file and nothing else.

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
Scope: {full sweep | sector}. Health probe: {what actually ran}.*

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
rubric rows at once — those are the real leverage.

## What is ABSENT

The rows where the model has no sector at all — the list that does not appear in
`open-derivations.md`. Follow the table with a paragraph on what the *shape* of the list means.

## Regressions since {previous report date}

## Full rubric

{A, B, C, D, E, K, G, H tables: | # | Requirement | Grade | Evidence (F-numbers) | Residual / free inputs | Note |}

## Method notes

Which rows needed a finding file rather than the indexes; the three grades spot-checked and
what the check found; citations to superseded findings carried with their supersession;
anything the health probe could not verify this run.
```

Rules for the prose: no cheerleading, no restating the model's strengths. A completeness
report that reads like a press release is a failed completeness report. Where a grade is
arguable, state the argument in one line rather than picking silently.

---

## Step 7 — Verify before finishing

1. **Spot-check three grades** against their cited finding files — pick the three you were
   least sure of, and record what the check found in Method notes. If any cited finding does
   not support the grade, fix the grade, not the citation.
2. **Check every F-number cited actually exists** (`ls findings/ | grep F{N}`). A citation to
   a superseded finding must carry the supersession.
3. **Check pipe escaping** — the report will be pulled into `docs-index.md`.
4. `make indexes` (confirm the new file appears in `docs-index.md`), then `make indexes-check`.
5. Add a one-paragraph `docs/status/changelog.md` entry, dated `yyyy-mm-dd - hh:mm`.

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
