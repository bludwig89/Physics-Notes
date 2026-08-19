---
id: CL239
title: 'The $\bmod 2\pi$ refold is a real defect wherever the integrand lacks that period: four sites in the QED/gluon sweep, one of which flipped the sign of the vacuum-polarization diagnostic, and two independent mechanisms inside the background-field self-energy, where the fold fires iff $Q\ge\pi/n$'
slug: 'the-f272-refold-defect-was-in-four-places'
tier: supporting
kind: derivation
status: open
domain: [QFT, QCD]
exactness: machine
findings: [F277, F308, F307]
tests: [F308-refold-repaired, F272-F273-bz-period-lattices]
modules: [casim.engine.gauge.lpt_selfenergy, casim.engine.gauge.bgfield_loop]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-04'
last_verified: '2026-08-19'
provenance: extracted
review_state: authored
confidence: high
---

# CL239 — The refold defect, its four sites, and the two independent mechanisms inside the background-field self-energy

## Statement

Folding a loop momentum back into $[-\pi,\pi)$ per axis is legitimate only when the integrand has
that period. The rule kernel does not: its period lattice is $\sqrt3\cdot$fcc, not $2\pi$ per
axis, because the reciprocal of BCC($a$) is fcc($4\pi/a$) with $4\pi/a=2\pi\sqrt3$ (F278). So the
simple-cubic $2\pi$ lattice is not a sublattice of the kernel's, and refolding evaluates the
integrand **at a different physical momentum**. Measured on $K=3\,\Omega_\text{even}^2+k_t^2$:
the shift $2\pi(1,0,0)$ moves it by $71.58$ and plain fcc $2\pi(1,1,0)$ by $34.59$, while
$\sqrt3\cdot2\pi(1,1,0)$ and $\sqrt3\cdot2\pi(2,0,0)$ move it by $1.4\times10^{-14}$ and
$1.9\times10^{-14}$ — periods.

**Four sites (F277).** The fold survived F272's own fix in three sibling modules plus a runner the
original audit did not scan. At one of them the consequence is not a shift but a **sign**: the
vacuum-polarization diagnostic $\Delta=B_\text{rule}-B_\text{cont}$ changes sign between $n=10$
and $n=14$ under the fold and settles at the opposite sign and $\sim6\times$ the magnitude
($+8.578\times10^{-3}$ refolded against $-2.0916\times10^{-3}$ unfolded at $n=14$), with a factor
$859$ in the spread. Unfolded, $\Delta$ converges monotonically. Folding is an array-indexing
device and there is no array being indexed at any of the four sites.

**Two independent mechanisms, in one module (F308).** Inside
`casim.engine.gauge.lpt_selfenergy` the audit that the repair required found **two** folds where
F307 reported one, and they behave oppositely:

* on `fp='leading'`, the ghost momentum factor is a **sum**, $2\sin(k/2)+2\sin((k+q)/2)$; each
  term has period $4\pi$, so folding one flips its sign *relative* to the other and the sum
  becomes a difference — a factor-2 effect ($C:32.78\to16.52$ at $Q=0.6$). This is the mechanism
  F277 and F307 §4 measured, and their attribution is exactly right **for that branch**;
* on `fp='exact'`+`kernel='wilson'` the effect is **exactly $0.0$**: the form factor
  $2\sin((p+p')/2)$ takes a *global* sign under the shift, which cancels in the $t\otimes t$
  contraction, and Wilson's $\hat k^2$ is $2\pi$-periodic per axis;
* on `fp='exact'`+`kernel='rule'` — **the branch every published rule constant used** — the effect
  is small but real ($\lvert\Delta\Pi\rvert\approx2\times10^{-3}$, $\Delta C=0.008$ at $Q=0.6$),
  and it is F272's original defect verbatim, still resident four findings later:
  $K_\text{true,4d}$ has no axis-wise period at all, measured non-invariant under $2\pi$, $4\pi$
  **and** $8\pi$ shifts.

**The firing condition, in closed form.** With the loop grid
$k_j=(j+\tfrac12)\tfrac{2\pi}{n}-\pi$ and external momentum $q=(Q,0,0,0)$, $k+q$ leaves
$[-\pi,\pi)$ only on the top $1/n$ slice of the $k_0$ axis, and only when $Q$ exceeds the
half-spacing:

$$\boxed{\ \text{the fold fires}\iff Q\ \ge\ \pi/n\ }$$

This is why the defect survived: it is invisible at small $Q$ and on coarse grids — exactly where
a cheap sanity check runs. At $n=8$, $\pi/n=0.3927$ exceeds every $Q$ in the committed sweep, so
that row is provably untouched.

**What the repair therefore re-dates, and what it does not.** The whole Wilson side of
`test-results/d1_selfenergy_sweep.json` stands ($C=10.4250/10.6276/10.7018$,
$\Lambda=1.6062/1.6210/1.6265$) because the fold is provably a no-op there. The $n=8$ rule row
stands, $C=16.3311$, $\Lambda_\text{rule}=2.1008$, verified bit-unchanged. Exactly three rule rows
need a native re-run — $(n{=}12,Q{=}0.3)$ and $(n{=}16,Q{=}0.2,0.3)$ — and until they are run the
correct statement about the rule $\Lambda$ is **"clean at $n=8$, pending at $n=12,16$"**, which
narrows F307's embargo rather than lifting it: the contamination on the published branch is at the
$10^{-4}$ level, not the factor-2 level.

## What it extends

**Lattice perturbation theory's use of Brillouin-zone periodicity**, and through it the
lattice-to-$\overline{\rm MS}$ matching that CL252 and CL022 rest on. In continuum QFT a loop
integrand may be shifted freely; on a lattice the licence is the integrand's own period lattice,
and the standard practice of folding $\bmod 2\pi$ per axis silently assumes a simple-cubic
reciprocal lattice. This model's rule kernel is BCC, so the assumption is false for it, and the
claim states the mechanism, the magnitude at each affected branch, and the closed-form condition
under which it fires. It is a **methodological** result about the model's own perturbative
apparatus, not a new physical prediction — which is why it changes what may be cited without
moving a physical constant.

It also names a limit on grep-based auditing: F277's lesson is that a fold cannot be found by
searching for it, because "harmless here" is a per-integrand judgement, and F308 confirms it by
finding two of five call sites in one module to be mathematical no-ops that must nonetheless be
documented as such.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| record `F272-F273-bz-period-lattices` (gate, `expect: {exactness: exact}`) → `tests/casim/test_bz_period_lattices.py` | the $\sqrt3\cdot$fcc period lattice, and that $2\pi(1,0,0)$ and $2\pi(1,1,0)$ are **not** periods of $K$; the sign of the vacuum-polarization diagnostic is asserted, not just its magnitude | exact / $10^{-14}$ |
| `findings/F277-qed-gluon-refold-period.md` §1–§2 | four sites; the sign flip and the factor $859$ in the spread; that unfolded $\Delta$ converges monotonically | measured |
| `findings/F277-qed-gluon-refold-period.md` §5–§6 | the fourth site and why its effect is small; the Wilson-side sites left untouched because $\hat k^2$ genuinely *is* $2\pi$-periodic | measured |
| record `F308-refold-repaired` (gate, `expect: {exactness: machine}`), 6/6 PASS, 23.6 s | R1: the repaired production default equals F307's independently written refold-free `pi_loop` at $Q=0.8,1.2$ | machine, $6.8\times10^{-16}$ / $4.0\times10^{-16}$ |
| same record | R2 counts grid points leaving the cube rather than trusting the $Q\ge\pi/n$ formula that predicts it | exact |
| same record | R4: the two mechanisms are distinct **in size** — the `fp='leading'` sum-fold is $>10\times$ the `fp='exact'` rule-propagator fold | machine |
| same record | R5: $K_\text{true,4d}$ has no axis-wise period at $2\pi$, $4\pi$ or $8\pi$ — what makes folding the rule branch illegal rather than merely redundant; and the $n=8$ sweep rows bit-unchanged | machine, $\max\lvert\Delta\Pi\rvert=3.5\times10^{-18}$ |
| same record | R6: `seagull_tadpole` $Z_0$ identical to the committed sweep at $n=8,12,16$ | machine, $3\times10^{-17}$ |
| same record, declared control `unrepair_control: true` | putting the fold back into the production default reddens **exactly `R1`** — journalled `CONTROL`, and the record carries the *measured* red set, not the R1/R3/R6 set the finding's first draft predicted | — |
| same record | R2/R3: `F307-action-consistent-d1` still **PASS** after the repair and F307's own control still reddens its declared leg, so the demonstration survives the repair of the thing it demonstrated | — |
| `docs/status/exactness-inventory.md` row 340 (F278) | the structural reason: reciprocal of BCC($a$) is fcc($4\pi/a$), $4\pi/a\equiv2\pi\sqrt3$ | exact (sympy) |

## Falsifier

The mechanism claim is falsified by exhibiting an axis-wise period of the rule kernel: any shift
$2\pi m$ (integer $m$, per axis) under which $K_\text{true,4d}$ is invariant to better than
$10^{-13}$ would make the fold legal and this card wrong. R5 tests $2\pi$, $4\pi$ and $8\pi$ and
finds none.

The magnitude claim is falsified by the re-run: if $(n{=}12,Q{=}0.3)$ and $(n{=}16,Q{=}0.2,0.3)$
come back with $\Delta C$ materially above the pre-stated $\lesssim0.01$ per affected row
($\Delta C_\text{mean}\lesssim0.005$, $\Delta\Lambda/\Lambda\lesssim0.02\%$), then the
contamination on the published branch is not at the $10^{-4}$ level and the narrowed embargo above
is wrong. That estimate was stated before the run precisely so it can fail.

The repair claim is falsified by the declared control: `unrepair_control: true` must redden `R1`
and does. If it ever stops doing so, the repair has been silently undone.

## Status & history

`open`, and the gap is named: **the three affected rule rows are un-re-run.**
`tests/runners/run_d1_selfenergy.py --refold-rerun` does exactly those three evaluations
(~16 min, against ~1.2 h for the full 24-row sweep). Until then the rule $\Lambda$ trend
$2.1008\to2.1192\to2.1264$ is quoted as pending at $n=12,16$.

Two further gaps, both flagged rather than closed:

* **The cube-vs-fundamental-domain question is untouched.** Not folding is necessary, not
  sufficient: `_pi_bgfield` still averages the rule kernel over the **cube** with uniform measure,
  and that kernel is not cube-periodic. That is the *domain* hazard and it belongs to F267/F305.
* **`particles/induced_stiffness.py` holds six fold sites this audit did not examine.** Another
  sector, flagged not swept. Given this is the fifth and sixth instance of the class, a further
  instance is a reasonable prior.

**No $d_1$ number is claimed or moved by the F308 half.** CL252's band
$\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\in[1,7.98]$, F155's $q_\ast a\in[0.577,0.979]$
and F307's deliberate `quotable: False` all stand exactly as written. This card asserts a defect
and its closed-form firing condition; it does not close a leg.

**2026-08-19 — extended to F308, and promoted from `unreviewed-seed` to `authored`.** The card was
seeded 2026-08-04 as part of standing up the claims layer (D12), and its statement was F277's
title verbatim:

> The F272 refold defect was in four places, and in vacuum polarization it flipped a sign

That remains true and is now the first half of the statement above. F308 was named by no claim card
at all — the gap `tools/audit_finding_coverage.py` §E measured — and the decision recorded here is
that the refold defect is **one claim with several sites**, not one card per finding: F308's
$Q\ge\pi/n$ firing condition, its two-mechanism split and its row-level re-dating belong with
F277's four sites. `provenance` stays `extracted` because that is how the card originated;
`review_state` is now `authored` because the physics above was read from the findings and the two
gate records rather than lifted from a title. `exactness` and `falsifier` move off `unset` in the
same pass. `docs/claims/CL236-the-background-field-loop-refolded-k-q-by.md` (F272, the original
`no_go`) is unchanged and stays `withdrawn`.

Nothing in the findings, the modules, the test registry or the supersession ledger was changed in
writing this card.

## Sources

- `findings/F277-qed-gluon-refold-period.md` — the four sites and the sign flip
- `findings/F308-refold-repaired-and-two-defects-not-one.md` — the repair, the two mechanisms, the firing condition, the re-dating
- `findings/F307-action-consistent-d1-and-a-live-refold.md` — §4, which demonstrated the live fold and explicitly declined to repair it
- `findings/F272-bgfield-loop-refold-period.md` — the original defect
- `docs/claims/CL236-the-background-field-loop-refolded-k-q-by.md` — F272's own (withdrawn) card
- `docs/claims/CL252-d1-tadpole-free-band-subtracted-against-wilson.md` — the $d_1$ band this does **not** move
- `src/casim/engine/gauge/lpt_selfenergy.py`; `tests/findings/test_F308_refold_repaired.py`; `tests/casim/test_bz_period_lattices.py`
- `test-results/d1_selfenergy_sweep.json`; `tests/runners/run_d1_selfenergy.py`
- `docs/status/exactness-inventory.md` — row 340 (F278), the period-lattice reason
