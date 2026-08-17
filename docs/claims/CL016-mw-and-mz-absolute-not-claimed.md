---
id: CL016
title: 'm_W and m_Z in absolute terms are not predicted — only their ratio'
slug: 'mw-and-mz-absolute-not-claimed'
tier: headline
kind: non_claim
status: withdrawn
domain: [SM]
exactness: external
findings: [F138, F320]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: CL007
falsifier: none
first_issued: '2026-08-02'
last_verified: '2026-08-16'
provenance: authored
review_state: authored
confidence: high
---

# CL016 — m_W and m_Z in absolute terms are not predicted — only their ratio

## Statement

**WITHDRAWN 2026-08-16 by F320.** The claim this card made was:

> The model predicts the **ratio** $m_Z/m_W$ (CL007, CL014). It does **not** predict $m_W$ and $m_Z$ in absolute terms. The electroweak scale $v$ is an **anchor, not an output**.

The second sentence is false and the first and third are true. See `## Status & history` — that
split is the whole retraction. Live successors: **CL276** (the absolute masses) and **CL277**
($\rho=1$).

## What it extends

Recorded so that **absence is not read as a prediction**. This is a scope boundary, not a result: the project does not assert it, and `status: withdrawn` is the assertion that it does not assert it.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F138-weinberg-gap-closure-4piv-matching.md` | $\mu_\star=4\pi v$ — the matching scale is expressed *in terms of* $v$, which is therefore an input. **Still true.** | external |
| `findings/F320-absolute-gauge-boson-masses-and-rho.md` | $m_W=\tfrac{3v}{2}\sqrt{2\pi\alpha}$, $m_Z=\tfrac{9v}{2}\sqrt{2\pi\alpha/7}$ — the masses *are* outputs of $\{\alpha,G_F\}$. **This is what withdrew the card.** | exact |

Related open item: the absolute mass scale is the hierarchy problem as it appears in this model — see F119, which finds the one open number is the overall scale $N=m_\text{lat}(\tau)$ and that no O(1) mechanism produces it.

## Falsifier

None while the card stood — a scope boundary admits no falsifier, and it noted it would be
falsified "by the project later claiming the thing, which would be a status change on this card
rather than an observation". That is precisely what happened, on 2026-08-16. The card predicted
its own retraction mechanism correctly.

## Status & history

`not_claimed` from 2026-08-02 to 2026-08-16; **`withdrawn` 2026-08-16**. This section is the
retraction record and is the most important part of the card.

**What was right.** "$v$ is an anchor, not an output" was correct on 2026-08-02 and is still
correct today. F119 finds the overall scale $N=m_\text{lat}(\tau)$ has no $O(1)$ mechanism, F320
does not touch it, and parameter-ledger entry 17 stays `FIT (N=1)`. Nothing in the withdrawal
weakens that.

**What was wrong.** The card inferred "$m_W$ and $m_Z$ are not predicted" from "$v$ is an input",
and that inference does not hold. The two statements differ by the input *count*. The Standard
Model's electroweak sector takes three measured inputs — $\alpha$, $G_F$ and one boson mass — and
predicts the other. This model takes two, because $\sin^2\theta_W^\text{os}=2/9$ arrives from
lattice geometry (F49's counting, completed by F141's Wigner–Seitz lemma) instead of from a third
measurement. Two inputs is not zero inputs, but the object the card called "not predicted" is an
output with a quotable residual: $+0.222\%$ on $m_W$ and $+0.158\%$ on $m_Z$, stated free of
$\Delta r$ (F320 §4).

**Why it took this long to notice.** The card rested on F138, whose §4 correctly says "$v$ itself
remains an external ruler". Nothing in F138 was wrong; the card read a true statement about $v$ as
a statement about $m_W$. The missing step — eliminating F141's stiffness quantum $u$ against
$e=g\sin\theta_W$ — is three lines of algebra that nobody had written down, because F141 had no
reason to: it was after the ratio, and the ratio does not need $u$.

**The lesson this card is kept for.** A `non_claim` recorded to make omissions countable is itself
an assertion and can be wrong in the same ways as any other. This one was not too *modest* about
the physics; it was **imprecise about the accounting**, and the accounting is the part the card
existed to get right. It is the second card in the register to be withdrawn for stating a scope
boundary one step too far in.

Not deleted, per the standing rule: a withdrawn claim that is deleted is a claim that gets
re-made.

## Sources

- `findings/F138-weinberg-gap-closure-4piv-matching.md`
- `findings/F320-absolute-gauge-boson-masses-and-rho.md` — the withdrawal
- `docs/claims/CL276-absolute-gauge-boson-masses-two-inputs.md` — successor
- `docs/claims/CL277-rho-equals-one-from-rank-not-custodial.md` — successor
- `papers/Claims-and-Falsifiers-Summary.md` — Scope
