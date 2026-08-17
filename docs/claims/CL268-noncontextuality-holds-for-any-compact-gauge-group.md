---
id: CL268
title: Gleason's non-contextuality premise holds on every gauge factor of this model, and holds for any compact group — the non-Abelian structure is exactly intra-site, the record observable is a gauge singlet, and Schur's lemma factors the internal index out of the frame condition; one consequence is that colour alone clears the dimension premise, so the d=2 hole is unreachable in any charged sector
slug: noncontextuality-holds-for-any-compact-gauge-group
tier: supporting
kind: derivation
status: live
domain: [QM, QFT]
exactness: exact
findings: [F312, F304, F281, F27, F41]
tests: [F312-born-nonabelian]
modules: [casim.engine.interactions.qi_born_nonabelian]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL264
falsifier: stated
first_issued: 2026-08-11
last_verified: 2026-08-11
provenance: authored
review_state: authored
confidence: high
---

# CL268 — Non-contextuality holds for any compact gauge group, not just $U(1)$

## Statement

On $\mathcal H=\mathcal H_p\otimes V$ — a pointer factor of cells and occupations, and an internal
factor $V=\mathbb C^N$ carrying a unitary irrep of a compact gauge group $G$ — the model asserts
four things, each measured rather than assumed:

1. **The current algebra is exactly intra-site.**
   $[\hat J^a(x),\hat J^b(y)]=i\,\delta_{xy}f^{abc}\hat J^c(x)$, and the $\delta_{xy}$ is *exact*:
   the off-site commutator is **literally `0.0`** for both $SU(2)_L$ and $SU(3)_c$, not zero to a
   tolerance. The algebra closes at `0.0` (SU(2), with $f^{abc}=\varepsilon^{abc}$ at `0.0`) and
   $1.11\times10^{-16}$ (SU(3), with $f_{123}=1$ and $f_{458}=0.8660254037844388=\sqrt3/2$).

2. **The record observable is a gauge singlet.** $[\hat J^a(x),\hat n(y)]=0$ **literally**, for
   every generator, site pair and group, with $\hat n$ the internal trace.

3. **Therefore the weight is context-blind with the sector present.** Five contexts sharing a ray,
   on Hilbert spaces of dimension 64 ($SU(2)_L$) and 96 ($SU(3)_c$): weight spread **literally
   `0.0`**.

4. **And the reason is Schur, so the group is irrelevant.** $\sum_aT^aT^a$ is a multiple of the
   identity (deviation `0.0` and $2.22\times10^{-16}$) with the exact value $(N^2-1)/2N$ — $3/4$
   and $4/3$ — so a $G$-invariant frame function on $\mathcal H_p\otimes V$ factorises as
   $f(v\otimes\chi)=f_p(v)\cdot c$ with $c$ independent of the internal ray. **The frame condition
   reduces to the one on $\mathcal H_p$ for any compact $G$ and any irrep.**

One consequence is asserted separately because it strengthens rather than restates the above:
since $\dim(\mathcal H_p\otimes V)=d_p\cdot N$, **$SU(3)_c$ clears Gleason's $d\ge3$ premise with no
reference to the pointer at all**, and the $d=2$ hole — where CL264's parent finding shows every
odd $k$ survives the frame condition — is **unreachable in any gauge-charged sector**. It requires
a total gauge singlet with a two-dimensional pointer.

## What it extends

**Gleason's theorem (1957) takes non-contextuality as a premise.** In the standard treatment it is
an assumption about the experimenter — that the weight assigned to a ray does not depend on which
orthonormal basis the ray is completed into. This claim asserts it is instead a **property of the
rule**, and asserts it on the two non-Abelian factors of the Standard Model gauge group where the
naive worry is strongest: $SU(2)_L$ and $SU(3)_c$ generators do not commute among themselves, so it
is not obvious *a priori* that a context cannot be smuggled in through the internal index.

The specific extension is that the answer does not depend on the group. Standard treatments of
Gleason on a tensor product either restrict to the system factor or assume the internal degrees of
freedom are spectators; here that is derived from Schur's lemma plus the singlet character of the
record observable, so it covers $U(1)_Y$, $SU(2)_L$, $SU(3)_c$ and any multiplet the model may add.

**Nothing established is contradicted.** The claim is that a premise ordinarily assumed is here a
theorem, on all three factors.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F312-born-rule-nonabelian-premises.md` G1/G2 | Closure and total antisymmetry of $f^{abc}$; **off-site commutator literally `0.0`** for both groups — the $\delta_{xy}$ that keeps the non-Abelian structure intra-site | exact |
| `findings/F312-born-rule-nonabelian-premises.md` G3 | $[\hat J^a(x),\hat n(y)]=0$ literally, both groups, every site pair | exact |
| `findings/F312-born-rule-nonabelian-premises.md` G4/G5 | Context weight spread literally `0.0` with the sector present (dims 64 and 96) | exact |
| `findings/F312-born-rule-nonabelian-premises.md` G6 | $C_2=\sum_aT^aT^a$ a multiple of $\mathbb 1$, value $(N^2-1)/2N$ — the Schur reduction | exact |
| `findings/F312-born-rule-nonabelian-premises.md` G7 | $\dim=d_pN$; $SU(3)_c$ clears $d\ge3$ alone; the $d=2$ hole is unreachable when charged | exact |
| `findings/F312-born-rule-nonabelian-premises.md` G8/G9 | Linearity and unitarity on $V$; a gauge rotation leaves every record weight fixed | machine ($\le1.6\times10^{-15}$) |
| `findings/F304-born-rule-gleason-premises-forced.md` §2 | The $U(1)$ case this generalises, and the basis-referencing control reused here | exact |
| `test-results/F312_born_nonabelian.json` | 18/18 PASS, record `F312-born-nonabelian`, tier gate, tol $10^{-13}$ | — |
| `test-results/control-soundness.json` | Three declared controls, each verified **CONTROL** at the current fingerprint | — |

## Falsifier

**Five, each with a named operator or observation.**

1. **A non-zero off-site current commutator.** Kills the intra-site argument, which is what keeps
   the non-Abelian structure away from an inter-site measurement context. Measured literally zero;
   the `abelian_control` perturbation ($f^{abc}\to0$) shows the leg can go red.
2. **A record observable in this tree that is not an internal singlet.** Re-opens contextuality
   through the gauge index. The `break_singlet` control *is* that operator — a colour-resolving
   record — and it reddens G3.
3. **A coupling in this tree whose pointer-side factor references a context.** Kills G4/G5. Key
   decision 3 (Higgs-free; minimal coupling only, no Yukawa scalar, no derivative coupling, no
   non-minimal term) is what excludes it; the `contextual_coupling` control is the operator that
   would do it.
4. **A reducible internal multiplet.** Schur gives a scalar on an *irreducible* block; a reducible
   $V$ makes $c$ block-diagonal, and a frame function could then depend on which block — i.e. on a
   label. Both multiplets used here are irreducible, so this is a live falsifier for any *future*
   multiplet rather than a defect now.
5. **A gauge-charged sector with a two-dimensional total Hilbert space.** Would restore the $d=2$
   hole in a charged sector, against the $\dim=d_pN$ arithmetic with $N\ge2$.

## Status & history

Issued 2026-08-11 from F312, `status: live`. The claim rests on premises that are measured and on
one structural argument (Schur) that is standard mathematics applied to the model's own generators;
nothing here is contingent on the Cooke–Keane–Moran regularity lemma, which concerns the *theorem*
CL264 carries rather than these *premises*.

**What this card does and does not do for its parent.** `CL264` is the headline Born-rule claim and
is `contingent`. This card discharges the second of the two reasons rubric row **A6** was downgraded
`EXACT → PARTIAL` on 2026-08-07 — *"non-contextuality is proved for the $U(1)$ wrap generator only;
the $SU(2)_L$ and $SU(3)_c$ commutators are not written out"*. **CL264 stays `contingent`**, because
its remaining hypothesis is the CKM lemma of item 1, which this card does not touch. A6's grade is a
completeness-run decision and neither card makes it.

**One input is used and not derived.** $N_c=3$ is an input — ledger row **B10**, mapped but not
closed by F293 — and it is what makes statement 5's "colour clears $d\ge3$ alone" true. At $N_c=2$
that consequence evaporates and the dimension premise would rest on the pointer alone. The rest of
the claim is $N$-independent by construction, which is the point of the Schur route.

**One scope limit that is not a caveat about correctness.** Superposition on the internal factor
(G8) is a statement about the rule's linearity, not about an asymptotic observable: physical
asymptotic states are colour singlets under confinement (F86/F110). The card asserts the rule is
linear and unitary on $V$; it does not assert that a coloured superposition is detectable.

## Sources

- `findings/F312-born-rule-nonabelian-premises.md`
- `findings/F304-born-rule-gleason-premises-forced.md` (§2, the $U(1)$ case; §5, the dichotomy this leaves intact)
- `findings/F281-measurement-pointer-basis-born-rule-rg-classicality.md` (§1.6, the maximal-abelian pointer algebra; open item 2, closed here)
- `docs/claims/CL264-born-rule-gleason-premises-forced.md` (parent; its residual 1b)
- `docs/status/completeness-2026-08-07.md` row **A6**
- `docs/status/open-derivations.md` row **A6r**
- Gleason 1957; Schur's lemma; Cooke–Keane–Moran 1985 (named, not used here)
