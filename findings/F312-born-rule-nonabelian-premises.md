# F312 — A6's non-Abelian seam closed with **one theorem, not two more cases**: the current algebra is written out and its $\delta_{xy}$ is **exact** (the whole non-Abelian structure is intra-site, so it can never reach an inter-site measurement context), the record observable is a gauge singlet **literally**, and a **Schur reduction** makes the internal index drop out of Gleason's frame condition for *any* compact group — with a bonus, that $SU(3)_c$ alone clears the $d\ge3$ premise and makes F304's $d=2$ hole **unreachable in any charged sector**

**Date:** 2026-08-11 - 23:05
**Numbering:** **F312**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `serene-rigorous-wigner`, sector `interactions`.
**Status:** Confirmed — **18/18 PASS**, three declared controls each verified RED at exactly its own leg. G1–G7 are **exact** (literal zeros, or $\le2.2\times10^{-16}$); G8/G9 are **machine**. No RNG stream is consumed anywhere (D8): every probe state and group element is deterministic.
**Module:** `casim.engine.interactions.qi_born_nonabelian` (`src/casim/engine/interactions/qi_born_nonabelian.py`)
**Script:** `tests/findings/test_F312_born_nonabelian.py` (registry entry `check_born_nonabelian`, tier **gate**)
**Results:** `test-results/F312_born_nonabelian.json`
**Claim card:** **CL268** (`live`, `supporting`, rolls up to **CL264**) — `docs/claims/CL268-noncontextuality-holds-for-any-compact-gauge-group.md`
**Closes:** [[F304-born-rule-gleason-premises-forced]] **residual 3** — *"§2.1's context-blindness is proved for the $U(1)$ wrap generator only… the $SU(2)_L$ and $SU(3)_c$ commutators are still not written out."* Rubric row **A6**, downgraded `EXACT → PARTIAL` in `docs/status/completeness-2026-08-07.md` on exactly that residual.
**Cross-references:** [[F304-born-rule-gleason-premises-forced]] (§2 B2's measurement, reused with the sector present; §5's dichotomy, which G6 shows survives the internal factor; §5.5's regularity lemma, **untouched**), [[F281-measurement-pointer-basis-born-rule-rg-classicality]] (§1.6, the maximal-abelian pointer algebra G4/G5 stand on; open item 2, which this closes), [[F27-complex-mass-chiral-su2]] / [[F41-hypercharge-higgs-free]] (the Higgs-free minimal coupling — key decision 3 is load-bearing again), [[F86-colour-dielectric-confinement]] / [[F110-kogut-susskind-compact-rotor]] (confinement, the scope limit on G8), [[F290-cluster-decomposition-strict-cone]] (exact no-signalling, F304 §2.3's remote-context leg, unchanged), [[F293-why-three-colours]] (that $N_c=3$ is an input — G7 uses $N=3$ and does not derive it). External: Gleason 1957; Cooke–Keane–Moran 1985.

Raised by Ben, 2026-08-11: *"attempt to work on section A6 and build out superposition and the born rule for both SU(2)L and SU(3)C if possible."*

---

## 1. The seam, and the decision to close it with a theorem

F304 proved the frame-function theorem on this lattice and forced both of Gleason's premises from the rule. Then it wrote down what it had *not* done, and the 2026-08-07 completeness sweep downgraded **A6** on it:

> non-contextuality is proved for the **$U(1)$ wrap generator only**; the $SU(2)_L$ and $SU(3)_c$ commutators are "not written out". Non-contextuality is a *premise of the derivation*, so a premise verified on one of three gauge factors is a named seam.

The obvious response is to run F304's B2 twice more. **That would be the wrong shape**, because it would leave the next gauge factor — or the next irrep, or a bigger $N_c$ — reopening the same seam. So the question this finding actually answers is:

> *Why* can an internal gauge index not disturb Gleason's frame condition?

The answer is **Schur's lemma**, which does not know which group it was handed. Once that is written down (G6), $U(1)$, $SU(2)_L$ and $SU(3)_c$ are three instances of one statement, and so is anything the model might add later.

### The setting

$$\mathcal H=\mathcal H_p\otimes V,\qquad V=\mathbb C^N\ \text{carrying a unitary irrep of }G$$

$\mathcal H_p$ is the **pointer** factor — cells, occupations, where a record lives; F281 §1.6 established $\{\hat n(x)\}$ is maximal abelian, so there is exactly **one** pointer context. $V$ is the **internal** factor: isospin for $SU(2)_L$, colour for $SU(3)_c$. Minimal coupling (key decision 3: no Yukawa scalar, no derivative coupling, no non-minimal term anywhere in the tree) gives

$$H_\text{int}=\sum_x\sum_a\hat A^a(x)\otimes\hat J^a(x),\qquad \hat J^a(x)=\psi^\dagger(x)\,T^a\,\psi(x).$$

---

## 2. G1/G2 — the commutator, written out, and the half of it that matters

$$\boxed{\ [\hat J^a(x),\hat J^b(y)]=i\,\delta_{xy}\,f^{abc}\hat J^c(x)\ }$$

Two separate facts live in that line, and **the second is the load-bearing one**.

| | $SU(2)_L$ | $SU(3)_c$ |
|---|---:|---:|
| closure $[T^a,T^b]=if^{abc}T^c$ | **`0.0`** (literal) | $1.11\times10^{-16}$ |
| $f^{abc}$ totally antisymmetric | **`0.0`** | **`0.0`** |
| $f^{abc}$ identification | $=\varepsilon^{abc}$ to **`0.0`** | $f_{123}=1.0$, $f_{458}=0.8660254037844388$ ($\sqrt3/2$) |
| same-site closure, 2-site space | **`0.0`** | $\le1.1\times10^{-16}$ |
| **off-site commutator $[\hat J^a(x),\hat J^b(y)]$, $x\ne y$** | **`0.0`** | **`0.0`** |

The $\delta_{xy}$ is **exact**, for both groups: currents at different sites commute *literally*, not to a tolerance.

> **That is what "site-local, diagonal in position" means when it is written out instead of asserted — and it is the whole argument.** The entire non-Abelian structure is **intra-site**. A measurement context is a choice of basis on the pointer factor, which is an **inter-site** object. The structure constants never leave one site, so they cannot reach it.

Stated that way, the worry the seam encoded — *"non-Abelian generators don't commute, so maybe context-blindness fails"* — is answered by observing that the non-commutativity is confined to a factor the context does not act on.

---

## 3. G3 — the record is a gauge singlet, so the two algebras commute elementwise

$$[\hat J^a(x),\hat n(y)]=0\qquad\text{for every }a,\,x,\,y$$

measured at **`0.0`** for both groups, with $\hat n(y)=\sum_c\psi^\dagger_c(y)\psi_c(y)$ — the internal **trace**.

This is stronger than "they happen to commute". $\hat n$ is a singlet **by construction**: occupation is what a cell *holds*, not what colour it holds. So the record cannot resolve the internal index, and the internal index cannot move the record. The control (`break_singlet`, a colour-*resolving* record, which exists nowhere in the tree) reddens G3 exactly.

---

## 4. G4/G5 — context-blindness, measured with the sector genuinely present

F304 §2.2's measurement, re-run on $\mathcal H_p\otimes\mathcal H_\text{env}\otimes V$ with the rule's own non-Abelian coupling $\sum_a g_a(\hat n\otimes T^a)$ carried alongside the record channel:

| | Hilbert dimension | weight spread over 5 contexts sharing a ray |
|---|---:|---:|
| $SU(2)_L$ present | 64 | **`0.0`** (literal) |
| $SU(3)_c$ present | 96 | **`0.0`** (literal) |
| basis-referencing gauge term (**control**) | — | reddens G4 |

The control swaps the gauge term's pointer-side factor for the projectors of the *specific* context — an operator that exists nowhere in this tree, built only so the leg has a way to fail.

---

## 5. G6 — the theorem, and why the group does not matter

A $G$-invariant frame function on $\mathcal H_p\otimes V$ averages over the internal factor to a multiple of the identity (Schur, $V$ irreducible), so

$$f(v\otimes\chi)=f_p(v)\cdot c,\qquad c\ \text{independent of}\ \chi,$$

and the frame condition on $\mathcal H_p\otimes V$ **reduces to the frame condition on $\mathcal H_p$**. F304 §5's dichotomy — $b_k=(-1)^k/\binom{k+d-2}{k}$, surviving iff $1+(d-1)b_k=0$ — therefore applies unchanged.

Verified on the Casimir:

| group | $C_2=\sum_aT^aT^a$ | exact $(N^2-1)/2N$ | deviation from a multiple of $\mathbb 1$ |
|---|---:|---:|---:|
| $SU(2)_L$ | $0.75$ | $3/4$ | **`0.0`** |
| $SU(3)_c$ | $1.333333\ldots$ | $4/3$ | $2.22\times10^{-16}$ |

> **The group enters only through $C_2$, and $C_2$ cancels out of the ray weight.** That is why this is one theorem rather than two more special cases, and why it covers whatever the model adds next.

---

## 6. G7 — and the internal factor **closes** F304's $d=2$ hole

F304 §5 derived that at $d=2$ *every odd $k$* survives the frame condition, so Born is four dimensions of an infinite-dimensional space. The qubit exception is real, and it is why the dimension premise had to be forced separately.

With an internal factor, $\dim(\mathcal H_p\otimes V)=d_p\cdot N$:

| group | $N$ | dim with **no** pointer | dim with F304's minimal record pointer | clears $d\ge3$ alone? |
|---|---:|---:|---:|---|
| $SU(2)_L$ | 2 | 2 | 4 | no — needs $d_p\ge2$ |
| $SU(3)_c$ | 3 | **3** | 6 | **yes** |

> **$SU(3)_c$ clears Gleason's dimension premise with no reference to the pointer at all**, and the $d=2$ hole is **unreachable in any gauge-charged sector** — it requires a total singlet with a two-dimensional pointer. That strengthens F304 rather than repeating it.

(The $N=3$ here is F293's **input**, not a derivation; this finding uses it and does not pretend to supply it.)

---

## 7. G8/G9 — two premises the $U(1)$ case never had to check

Both are vacuous for a phase acting on a singlet, and neither is vacuous here.

| leg | statement | residual |
|---|---|---:|
| **G8** superposition on $V$ | the link step is **linear** and **unitary**, so a superposition of internal states evolves to the superposition of the evolved states | linearity $\le2.8\times10^{-16}$; unitarity $\le1.6\times10^{-15}$ |
| **G9** a gauge rotation is not a context | $V(x)\in SU(N)$ moves the internal state and must leave every record weight **fixed** | $\le1.3\times10^{-15}$ |

G9 is the non-Abelian analogue of F304 §2.2's *"outcome labels are not contexts"*, and it is a genuinely new premise: a $U(1)$ phase acts trivially on a singlet record, while an $SU(N)$ rotation does not.

---

## 8. Verdict

> **A6's non-Abelian seam is closed, and closed by a theorem.** The commutator F304 said was not written out is written out, and its $\delta_{xy}$ is **exact for both groups** — the entire non-Abelian structure is intra-site, so it can never reach an inter-site measurement context. The record observable is a gauge singlet **literally** ($[\hat J^a,\hat n]=0.0$), so the pointer and gauge algebras commute elementwise by construction. Context-blindness, re-measured with the sector genuinely present on Hilbert spaces of dimension 64 and 96, has **literal-zero** weight spread. And the reason all of this works is **Schur**: $\sum_aT^aT^a$ is a multiple of the identity with the exact value $(N^2-1)/2N$, so an invariant frame function factorises and F304 §5's dichotomy is untouched **for any compact group and any irrep**. One bonus falls out that F304 could not have had: since $\dim=d_p\cdot N$, **$SU(3)_c$ alone clears the $d\ge3$ premise** and the $d=2$ hole is unreachable in any charged sector.

**What this does to A6.** The row was `PARTIAL` for two stated reasons — non-contextuality on one of three gauge factors, and the CKM regularity lemma. **The first is now closed on all three, by a statement that does not depend on which three.** The second is untouched and stays named; A6's grade is a completeness-run decision and this finding does not make it.

---

## 9. Falsifiers

1. **A non-zero off-site current commutator.** Would break the $\delta_{xy}$ and with it the intra-site argument. Measured literally zero for both groups; `abelian_control` shows the leg can fail.
2. **A record observable in the tree that is *not* an internal singlet.** Would break G3 and re-open contextuality through the gauge index. The `break_singlet` control is exactly this operator, and it reddens.
3. **A coupling in the tree whose pointer-side factor references a context.** Would break G4/G5. Key decision 3 (Higgs-free, minimal coupling only) is what excludes it, and the `contextual_coupling` control is the operator that would do it.
4. **A reducible internal representation.** Schur gives a multiple of the identity per *irreducible* block; a reducible $V$ would give a block-diagonal $c$, and a frame function could then depend on which block — i.e. on a label. The model's $SU(2)_L$ doublet and $SU(3)_c$ triplet are both irreducible, so this is a live falsifier for any *future* multiplet, not a defect now.
5. **A gauge-charged sector with a two-dimensional total Hilbert space.** Would restore F304's $d=2$ hole in a charged sector. G7 asserts this is impossible given $N\ge2$.

---

## 10. What is exact vs computed vs open

| Piece | Status |
|---|---|
| $[T^a,T^b]=if^{abc}T^c$ closes, $SU(2)$ / $SU(3)$ | **exact** (`0.0` / $1.1\times10^{-16}$) |
| $f^{abc}=\varepsilon^{abc}$ for $SU(2)$; $f_{123}=1$, $f_{458}=\sqrt3/2$ for $SU(3)$ | **exact** |
| $f^{abc}$ totally antisymmetric | **exact** (`0.0`, both) |
| **Off-site commutator vanishes ($\delta_{xy}$)** | **exact** (`0.0`, both) — the load-bearing row |
| $[\hat J^a(x),\hat n(y)]=0$ | **exact** (`0.0`, both) |
| Context weight spread with the sector present | **exact** (`0.0`, dims 64 and 96) |
| $C_2$ a multiple of $\mathbb 1$, value $(N^2-1)/2N$ | **exact** (`0.0` / $2.2\times10^{-16}$) |
| The Schur reduction of the frame condition | **structural**, and the general theorem |
| $\dim=d_p\cdot N$; $SU(3)_c$ clears $d\ge3$ alone | **exact** (integer arithmetic) |
| Linearity and unitarity on $V$ | **machine** ($\le2.8\times10^{-16}$, $\le1.6\times10^{-15}$) |
| Gauge rotation leaves the record weight fixed | **machine** ($\le1.3\times10^{-15}$) |
| Gleason's dichotomy itself | **F304 §5** — proved there, reused here, **not re-proved** |
| $N_c=3$ | **input** (F293/B10) — used, not derived |
| **The Cooke–Keane–Moran regularity lemma** | **open** — A6's other named residual, untouched |

---

## 11. Honest scope

**Gleason is not proved here.** F304 §5 proves it; this finding supplies its premises on the two non-Abelian factors and the reduction that makes the internal index irrelevant to it. Presenting the Schur step as a proof of the theorem would be exactly the error F304 avoided when it was still citing Gleason.

**A6's other residual is untouched.** The Cooke–Keane–Moran regularity lemma — that a non-negative frame function is automatically continuous, whose entire content is the exclusion of *non-measurable* weight assignments — remains external and remains named. This finding closes one of A6's two stated reasons for `PARTIAL`, not both, and the grade is a completeness-run decision rather than this session's.

**Coloured superposition is not an asymptotic observable.** G8 says the rule's link step is linear and unitary on $V$, which is what "superposition is structural" means for the internal factor. Physical asymptotic states are colour singlets (F86/F110), so G8 is a statement about the rule and not about something a detector sees. Saying otherwise would overclaim in the one place where confinement makes the difference.

**$N_c=3$ is used, not derived.** G7's headline — that $SU(3)_c$ clears $d\ge3$ on its own — is a consequence of $N=3$, which ledger row **B10** records as an input and which F293 mapped without closing. If $N_c$ were 2, that bonus would evaporate and G7 would rest on the pointer alone.

**Irreducibility is a premise, and falsifier 4 is where it bites.** Schur gives a scalar on an *irreducible* block. Both multiplets used here are irreducible, so the reduction is clean — but a future reducible multiplet would make $c$ block-diagonal and re-open the question, which is why it is written as a falsifier rather than left implicit.

---

## 12. Files
- Module: `src/casim/engine/interactions/qi_born_nonabelian.py`
- Test: `tests/findings/test_F312_born_nonabelian.py` (record `F312-born-nonabelian`, tier gate, **18/18**, 0.1 s)
- Results: `test-results/F312_born_nonabelian.json`
- Controls: three, each verified **CONTROL** 2026-08-11 and journalled to `test-results/control-soundness.json`
