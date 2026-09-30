# NB2-002 — Is the notebook's "$W^\pm$ coupling $=3e$" numerology an independent route to $\sin^2\theta_W=2/9$?

**Date:** 2026-09-23 - 14:05 · **Thread:** T07 · **Cluster:** Electroweak numerology → structure
**Lineage:** NB-133/NB-134 [RECON batch 10, SOLID / NEEDS-WORK] · XCHECK n/a (folded into the
pp.103-109 REINFORCES section) · CORR `notebook-reconstruction-correlation-queue.md` row 4 · MODEL
F49, F141, F138, F231, `casim.constants.sin2_thetaW_onshell`
**Disposition:** CLOSED-LINEAGE + CLOSED-NEGATIVE (on the "independent derivation" question)

## Where the notebook left it

p.104: an idle margin calculation, explicitly flagged by the author as unmotivated ("is there any
significance to this?"). Hypothesis: the charged-current coupling to $W^\pm$ equals exactly $3e$.
Solving $\sqrt2/\sin\theta_W=3$ gives $\sin\theta_W=\sqrt2/3$, $\sin^2\theta_W=2/9$ exactly [NB
p.104]. The very next calculation on the same page (a $Q_z$ matrix built from this
$\sin^2\theta_W$, plus a side self-consistency check treating rounded decimals as exact fractions)
ends in the author's own hand-marked **✗**.

## Where the three passes left it

**[RECON]** NB-133 verified SOLID — the algebra from the stated hypothesis to $\sin^2\theta_W=2/9$
is correct, scored purely on internal consistency, explicitly not scored as a derivation (the
notebook itself doesn't claim it is one). NB-134 verified NEEDS-WORK with both root causes found:
(1) a printed radical $\sqrt{1/7}$ should read $\sqrt{2/7}$ (transcription slip against its own
accompanying decimal 0.535); (2) the boxed $Q_z$ entry $2.37$ is not the value at
$\sin^2\theta_W=2/9$ at all — it is copied over from the previous page's *experimental* value. Once
both are corrected, the true entries are $\cot\theta_W+\tan\theta_W=\sqrt{7/2}+\sqrt{2/7}=
\tfrac{9\sqrt{14}}{14}\approx2.4054$ and $\cot\theta_W-\tan\theta_W=\tfrac{5\sqrt{14}}{14}
\approx1.3363$. The author's own self-flagged arithmetic failure ($11/6+6/11=157/66\ne7/3$) is
confirmed genuine: it comes from averaging two already-corrupted two-decimal roundings of the true
values, not from a real inconsistency in the underlying angle.

**[CORR]** The correlation queue's row asks whether this 2007 numerology has any relationship —
"historical, structural, or purely coincidental" — to the model's decision-7 $\delta^*=2/9$ lepton
shape angle, flagging explicitly that the notebook's own arithmetic undermines itself on the same
page and that the honest answer may be coincidence.

## What the model already has

Search terms: the queue row itself names `sin²θ_W`; cross-checked against `docs/theory/
key-decisions.md` D7 (constants registry) and `findings-index.md` for F49/F141/F138/F231.

**The queue row's framing conflates two different registered constants.** D7 states explicitly:
*"Three cases deliberately keep more than one entry, because collapsing them would turn a
prediction into an input: ... $\sin^2\theta_W$ (F45 UV $\tfrac14$ / F49 on-shell $\tfrac29$)"* — and
separately, decision 7's own text lists $\delta^*=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ rad
as a third, explicitly-unrelated $2/9$ (D7's fuller statement: *"2/9 is three unrelated model
constants (delta_star, sin2_thetaW_onshell, c_fierz_colour)"*). NB-133/134's page-104 content is
about the **electroweak** mixing angle — `casim.constants.sin2_thetaW_onshell`, a
`Fraction(2, 9)` — not about $\delta^*$ at all. So the correlation queue's literal question (does
this connect to the *lepton-shape* $\delta^*$) has a clean, structural answer: **no, by the
registry's own construction** — merging them is exactly the error D7 is written to forbid, and
nothing in NB-133/134's content (a coupling-ratio guess about $W^\pm$) touches representation
weights or $O_h$ crystal-field structure at all. That leaves the more interesting question the queue
row was reaching for, restated correctly: is NB-133's route an independent derivation of the
model's own $\sin^2\theta_{W,\text{on-shell}}=2/9$, or a restatement of it?

The model's own route: F49 derives a $2$-vs-$7$ split of the $9$ facet axes of the BCC Wigner-Seitz
cell (an exact lattice-combinatorics lemma, confirmed by F141), giving
$\sin^2\theta_W=2/9=\tfrac{2}{2+7}$ directly from counting, with $\cos^2\theta_W=7/9$ giving
$m_W^2:m_Z^2=7:9$ (F141's on-shell mass-counting statement). F231 supplies the exact bridge showing
$2/9$ is the on-shell face of the model's primary UV-matching value $\sin^2\theta_W=\tfrac14$
(at $\mu_\star=4\pi v$) via an $8/9$ decomposition — F138/CL014.

## The next step, taken

Algebraic, no CASIM run needed — the question is purely about which numbers are inputs and which
are outputs in each route.

**Is NB-133's hypothesis physically equivalent to F49's derivation?** No connection exists between
"assume the $W^\pm$ coupling is exactly $3e$" and "count the facet axes of a BCC Wigner-Seitz cell."
The former is a guessed integer ratio applied to an unknown coupling-normalization convention; the
latter is a lattice-geometry combinatorial count. Nothing in the notebook's own text motivates the
ratio $3$, and the reconstruction is explicit that this is scored as "idle numerology," not a
derivation — a verdict this entry endorses rather than revises.

**Does NB-133's guessed ratio hold at the model's *other* named value, $\sin^2\theta_W=\tfrac14$
(the UV-matching scale, CL014's stated primary value)?** At $\sin^2\theta_W=\tfrac14$,
$\sin\theta_W=\tfrac12$, so $\sqrt2/\sin\theta_W=2\sqrt2\approx2.828\ne3$. **It does not.** NB-133's
ratio only lands near the model's *secondary*, on-shell face of the prediction, not its primary
UV-matching value — consistent with $2/9$ being the on-shell projection of $1/4$ (F231), but adding
no independent support: a guess with one free integer parameter ($3$) has a reasonable chance of
landing within a few percent of *some* named value in a theory with only one dimensionless angle to
hit, and it does not reproduce the model's primary value at all.

**Does NB-134's corrected $Q_z$ matrix carry any content beyond the angle itself?** No. Once
corrected, $\cot\theta_W\pm\tan\theta_W$ are exact algebraic functions of $\cos^2\theta_W=7/9,
\sin^2\theta_W=2/9$ alone — the same two numbers F141 derives from BCC facet-axis counting,
restated in different trigonometric combinations. There is no new physical content in NB-134 beyond
NB-133's angle; its self-flagged failure is fully and only a transcription/rounding artifact, exactly
as the reconstruction found, with nothing further for this session's model-comparison to add beyond
confirming the corrected entries are consistent with — not independent evidence for — the model's own
value.

**Verdict:** the notebook's page-104 numerology is a coincidence in the ordinary sense — an
unmotivated guess that happens to land on the model's on-shell value, not a route to it, and not a
route to $\delta^*$ either (they are different objects by explicit registry design). This closes the
correlation queue's row honestly negative on "is there a connection," while making precise *which*
connection is absent (structural, to $\delta^*$) and *why* the remaining resemblance (to
$\sin^2\theta_{W,\text{on-shell}}$) carries no evidential weight (fails at the model's primary value,
carries no free content beyond the angle).

## Correlations exposed

- Directly closes correlation-queue row NB-133/134.
- Sharpens D7's own registry rule with a worked example: this is precisely the kind of coincidence
  the "three unrelated $2/9$'s" clause exists to keep un-merged, now with an external (2007,
  independently-timed) near-miss on record as a concrete illustration of why the rule matters.

## New questions opened

None beyond what the thread map's T01/T10 already name. This thread closes cleanly with no residual.

## Files touched

- `docs/theory/notebook-v2/NB2-002-sin2thetaW-2over9-lineage.md` (this file)
- `docs/theory/notebook-reconstruction-correlation-queue.md` — NB-133/134 row marked `CLOSED` below
