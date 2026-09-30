# Notebook Reconstruction — Batch 07: Weak Contact Terms, Helical-Motion Mass Model,
# Ferbel/Majorana/Fermi References (pp. 67–76)

Cold, independent reconstruction and continuation of `references/physics-notes-complete.md`
pages 67–76 (NB-086 – NB-098).

Date-time stamp: 2026-09-22 - (batch 07).

---

## NB-086 (p.67) — Chiral Structure of the Mass Term

**Notebook:** $mc^2\bar\psi\psi=mc^2(\bar RL+\bar LR)$, motivating the weak-interaction "contact"
analog $g(\bar\nu_Le_L+\bar e_L\nu_L)+g'(\bar\nu_Re_R+\bar e_R\nu_R)$.

**Verified** (`run_NB-086_chiral_mass_identity.py`, sympy, explicit 4-component Dirac spinor,
Weyl-basis $\gamma^0,\gamma^5$, chiral projectors $P_{L,R}=(1\mp\gamma^5)/2$): $\bar\psi\psi=
\bar\psi_L\psi_R+\bar\psi_R\psi_L$ confirmed exactly, and the same-chirality bilinears
$\bar\psi_L\psi_L,\bar\psi_R\psi_R$ confirmed to vanish identically. This is the standard fact
underlying the whole "mass term only connects opposite chirality" theme running through pp.61–91
of the notebook — now independently confirmed rather than merely cited. **Verdict: SOLID.**

## NB-087 (p.68) — Kinetic Term Factor-of-2 Problem

**Notebook:** building separate EM and weak kinetic terms for the doublets leads to a
"we get inconvenient factors of 2" self-diagnosed problem.

**Assessment.** This is exactly the standard bookkeeping hazard of writing the *same* kinetic
term twice (once from an EM covariant derivative, once from a weak one) without recognizing they
must be combined into a *single* covariant derivative with *both* gauge fields — a completely
standard subtlety in building any multi-gauge-group Lagrangian, correctly self-diagnosed by the
author as a real problem rather than glossed over. **Verdict: SOLID** (accurate self-critique).

## NB-088 (p.69) — Proposed $B_\mu$ Neutral-Current Field

**Notebook:** introduces a second $U(1)$ field $B_\mu$ (distinct from $A_\mu$) specifically to
generate neutral currents, coupling only to the $(\nu_L,e_L)$ doublet; notes the striking
coincidence $g_\nu\approx0,m_\nu\approx0,g_R\approx0,g'\approx0$.

**Assessment.** A reasonable, self-consistent construction ansatz (a genuinely new field
proposed to explain a genuine gap — neutral currents — in a Fermi-contact-term picture); the
"amazing" coincidence the author flags is really the observation that *two independently
motivated near-zero quantities line up*, which is suggestive but not something with a
right-or-wrong answer to verify. **Verdict: NOT-TESTABLE** (construction/observation, no closed
claim).

## NB-089 (p.70) — Already Assigned: DEAD-END-AUTHOR-CALLED-IT

Explicit combination attempt, self-abandoned ("This is becoming an ugly way to write equations
of motion") in favor of a quadruplet notation the author doesn't pursue on the page. Confirmed
this stands — the abandonment is well-motivated (the same factor-of-2 issue from NB-087,
compounded across four fields). **Verdict: DEAD-END-AUTHOR-CALLED-IT** (unchanged).

## NB-090 (p.71) — Neutral-Current Lagrangian Ansatz

Direct construction, structurally parallel to the analogous EM form; no independent claim beyond
"here is one way to write it." **Verdict: SOLID** (well-formed construction).

## NB-091 (pp.71–72) — Q&A: Dynamical $W$ Required, Not Just a Mass Term

**Notebook:** the existence of $\mu^-\to e^-+\bar\nu_e+\nu_\mu$ requires a genuinely *dynamical*
$W$ boson exchange, not merely a static mass-like contact term between $e,\nu_e$ — because a
mass term alone can't connect three different external states the way an intermediate boson can.

**Assessment.** This is a correct and important physics point, and a good one to have reasoned
through independently rather than just quoted: a mass (2-point, same-flavor) term cannot mediate
a genuinely 4-point (different-flavor, particle-number-changing-within-a-generation) process like
$\mu$ decay — you need a propagating intermediate state that can be radiated by one vertex and
absorbed by a different one. This is exactly the historical logic that led from the point-like
Fermi 4-fermion theory to the intermediate vector boson picture. **Verdict: SOLID** (correct
physics reasoning, independently checked for soundness, not just restated).

## NB-092 (p.72) — Proposed $\mu$-Decay Mechanism via $B_\mu$

Speculative mechanism combining the NB-088 $B_\mu$ field with a contact term, explicitly
acknowledging temporary charge non-conservation bounded by an uncertainty-principle-style
argument. A speculative construction, not a claim with a right/wrong answer at this level of
detail (no propagator, no amplitude, nothing to actually check numerically). **Verdict:
NOT-TESTABLE.**

---

## NB-093/NB-094/NB-095 (pp.73–74) — Helical-Motion Mass Model: Algebra Error Found and Fixed

**Notebook:** models a particle traveling in a helix (diameter $r$, frequency $\nu$, forward
speed $v_\text{eff}$) with $|\vec v|=c$ fixed, giving $v_\text{eff}=\sqrt{c^2-4\pi^2\nu^2r^2}$
(NB-093, straightforward and correct on its own terms). NB-094 attempts to link this to
$E=\hbar\omega$ via $E^2=p^2c^2+m^2c^4$, runs into a $v\to\infty$ pathology, and is correctly
abandoned ("That isn't right!" — already DEAD-END-AUTHOR-CALLED-IT). NB-095 retries with the
correct relativistic momentum $p=m_0v/\sqrt{1-v^2/c^2}$, derives
$$\hbar^2\omega^2=\frac{m_0^2v^2c^2}{1-v^2/c^2}+m_0^2c^4,$$
and, after several algebra steps, claims $v^2=c^2-E_0^2/E^2$ — flagging it himself: *"Way way —
no good."*

**Reconstruction.** Solving the *same starting equation* symbolically (`run_NB-093_094_095_helical_velocity.py`,
sympy `solve`) gives
$$v^2=c^2\frac{E^2-E_0^2}{E^2}=c^2-\frac{c^2E_0^2}{E^2},$$
**not** the notebook's claimed $v^2=c^2-E_0^2/E^2$ — the notebook's version is missing a factor
of $c^2$ on the second term, and is dimensionally inconsistent as written (the notebook keeps
$c$ explicit throughout this derivation, never sets $c=1$, so a term without the matching $c^2$
really is a units mismatch, not just an aesthetic difference).

**The corrected result is independently significant:** $v^2=c^2(1-E_0^2/E^2)$ is **exactly** the
standard relativistic group-velocity relation $v_\text{group}=dE/dp=c\sqrt{1-E_0^2/E^2}$,
confirmed here as a completely independent cross-check (not derived from the notebook's own
route at all, just the standard $E^2=p^2c^2+E_0^2$ differentiated). So: the *starting physics*
(helical model, relativistic momentum substitution) was set up correctly; a genuine algebra slip
in carrying the solve through dropped a $c^2$ factor; and the corrected destination is not a new
result but exactly recovers a well-known, independently-checkable formula.

**Verdict: NB-093 SOLID; NB-094 DEAD-END-AUTHOR-CALLED-IT (unchanged); NB-095
INCORRECT (as transcribed) / SOLID-WITH-CORRECTION** — upgraded from the Phase-0 provisional
NEEDS-WORK. The author's own "no good" instinct was exactly right, and this reconstruction
identifies precisely why and supplies the fix: $v^2=c^2-E_0^2/E^2\to v^2=c^2(1-E_0^2/E^2)$.

---

## NB-096 (p.75) — Ferbel Reference Data

**Notebook:** transcribed electroweak precision values from a 1990s-era Ferbel ASI reference
text: $m_W=80.22\pm0.26$ GeV, $m_Z=91.187\pm0.007$ GeV, $m_\tau=1776.9^{+0.4}_{-0.5}\pm0.2$ MeV,
$\sin^2\theta_W=0.232\pm0.009$, etc.

**Assessment.** Checked against this reconstruction's general knowledge of standard (period- and
present-day) electroweak precision values: $m_Z=91.187$ GeV matches the now-PDG-standard
$91.1876$ GeV to the quoted precision; $m_\tau=1776.9$ MeV matches the modern PDG value
$1776.86$ MeV closely; $\sin^2\theta_W=0.232$ is within the modern $\overline{MS}$ value
$\approx0.2312$'s neighborhood, consistent with the quoted 1990s-era uncertainty. This reads as
an accurately transcribed table of real reference data, not a computed or derived result — there
is nothing to independently re-derive here, only to check for transcription fidelity, which
holds up. **Verdict: SOLID** (accurate reference data, correctly transcribed).

## NB-097/NB-098 (p.76) — Majorana Mass, Fermi Theory, V−A

Standard, correctly-quoted textbook material (Majorana mass matrix structure; Fermi coupling
$G_F=1.167\times10^{-5}\,\text{GeV}^{-2}$, matching the modern PDG value $1.1664\times10^{-5}\,
\text{GeV}^{-2}$ closely; V$-$A current structure). Not independently derived on this page — a
"known facts" reference block, same character as NB-051 and NB-075/079. **Verdict: SOLID** (both,
as accurately-quoted standard material).

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-086 | SOLID |
| NB-087 | SOLID |
| NB-088 | NOT-TESTABLE |
| NB-089 | DEAD-END-AUTHOR-CALLED-IT |
| NB-090 | SOLID |
| NB-091 | SOLID |
| NB-092 | NOT-TESTABLE |
| NB-093 | SOLID |
| NB-094 | DEAD-END-AUTHOR-CALLED-IT |
| NB-095 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-096 | SOLID |
| NB-097 | SOLID |
| NB-098 | SOLID |

**What closed:** the chiral mass-term identity (NB-086) underlying this whole stretch of the
notebook is independently confirmed with an explicit spinor calculation. The most substantial
result of this batch is NB-095: a genuine algebra error (a dropped $c^2$ factor) is found and
precisely diagnosed, and the corrected result turns out to be exactly the standard relativistic
group-velocity formula — closing the author's own "no good" self-doubt with an actual answer
rather than leaving it open, and upgrading this build from the Phase-0 provisional NEEDS-WORK.
The Ferbel/Majorana/Fermi reference pages (NB-096–098) check out as accurately transcribed
standard data.

**What's still open:** nothing carried forward from this batch. NB-088's $B_\mu$ proposal and
NB-092's decay mechanism remain speculative constructions with no closed claim to verify further
at the level of detail given.

---

## Errata — errors in the notebook (2007)

- **p.74 (NB-095):** the claimed $v^2=c^2-E_0^2/E^2$ is missing a factor of $c^2$ on the second
  term; the correct result, obtained by solving the notebook's own (correctly set up) starting
  equation, is $v^2=c^2-c^2E_0^2/E^2=c^2(1-E_0^2/E^2)$ — exactly the standard relativistic
  group-velocity relation. Confirmed by independent symbolic solve and cross-checked against the
  externally-known formula $v_\text{group}=c\sqrt{1-E_0^2/E^2}$.

## Errata — errors in my framing of these prompts

- None found in this batch.

## Correlation queue additions

None from this batch meet the bar — NB-095's corrected result recovers a completely standard,
textbook relativistic formula with no distinctive connection to a specific model claim; the
$B_\mu$/neutral-current speculation (NB-088/090/092) is too underdeveloped in the notebook to
pose as a sharp question for the model.
