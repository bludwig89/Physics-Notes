# F324 — The $N_c$ interval closes on $\{3\}$: F298's C7 support $\{2,3\}$ paired with the $\mathbb Z_2$ doublet parity of the model's **own derived** $SU(2)_L$ — one bit of new information, six premises, and the three-constituent baryon discharged as a corollary

> **X1 RESOLVED 2026-08-18 (F325, ledger record S22).** **The UPPER constraint of this finding is withdrawn, and §3 U1c is why.** U1 imports F298's
criterion — $\chi_k=s(k)^2/(4g^2C_2(\text{antisym }k))$ — which is the **mixed** matching; under
either self-consistent matching $\chi=1/(4g^2)$ for every $N$, so the C7 support $\{2,3\}$ does not
exist (F325 §2, leg **L6** of `F298-casimir-ladder`, exact over $\mathbb Q$). **This finding
anticipated it:** §3 U1c measured $\chi_6=3/10$ against the tower's $3/4$ and called it *"falsifier 5b
… the most serious structural exposure on the upper side"*, concluding *"the support $\{2,3\}$ is a
property of the **truncation**, not yet of the model."* It is realised — at $N=3$ the mixed matching
gives $\chi\in\{3/4,3/10,3/16\}$ plus **undefined** for the adjoint, decuplet and 27.
>
> **The lower constraint — the $\mathbb Z_2$ doublet parity — is untouched**, and the verdict that
> B10 *"stops being a dependent of the X1 fork"* stands, though by the fork **closing** rather than by
> the selector retiring. The bracket is now **odd $N_c\neq1$**: $\{3,5,7,\dots\}$. §8 priced the
> incremental content over F298 at *"one bit"*; that is exactly what this spends. The
> three-constituent-baryon corollary is $N_c$-conditional again. Card **CL281** narrowed to match.

**Date:** 2026-08-17 - 19:50
**Numbering:** **F324**, taken as max+1 against `F323` (no gap closed). **Caveat CLAUDE.md §Concurrency requires:** the device workspace was unavailable all session, so `casim index` could not be re-run immediately before writing. **Re-check `NEXT FREE NUMBER` before committing** and renumber if a concurrent session spent F324.
**Status:** **Physics verified, tree-unverified — read §11 before the header.** The entry returns **14/14 PASS** in an isolated harness (15/15 in-tree, with the F317 cross-check armed) and **eight** declared controls each go red **and red only where declared**. `make gate` and `casim test` were **not run**. Do not read this as `Confirmed`.
**Verdict:** Row **B10**: the $\Lambda$-scale selector is **no longer load-bearing**, and B10 **stops being a dependent of the X1 fork**. $N_c=3$ follows from two constraints that between them consume **no measured number**, **no three-constituent baryon** and **no X1 branch** — but **six premises**, all booked in §0. **The parity argument is prior art** (Bär & Wiese 2001) and is not claimed as new. **The incremental content over F298 is one bit.**
**Side effect on two existing findings, both liberating, neither a retraction:**
- **F317 §6's empirical input is discharged** — and §5 shows *why it cost nothing*: given quarks in the defining rep, "the $\varepsilon$-singlet has three constituents" was never information about the model independent of $N_c$.
- **F318's double-count warning loses its object**, since neither constraint here uses that fact.

**Modules:** `src/casim/engine/gauge/derive_ncolour_bracket.py` (new)
**Test / results:** record `F324-ncolour-bracket` (tier gate, entry `check_ncolour_bracket`), driver `tests/findings/test_F324_ncolour_bracket.py` → `test-results/F324_ncolour_bracket.json`
**Cross-references:** [[F317-su3-structure-derived]] (§10 item 2 — the close this executes; §6, discharged), [[F298-casimir-ladder-c7-rerun]] (the upper constraint, **imported**), [[F318-cell-carries-the-internal-index]] (premise (ii); the double-count), [[F293-why-three-colours]] (R1 measured blind; §4.2's selector, retired), [[F279-hypercharge-constraint-attribution]] (the six-row system), [[F27-complex-mass-chiral-su2]] (the chirality the parity needs), [[F75-three-generations-from-bcc-irrep-selection]] (premise (i)), [[F97-baryon-phase-closure-no-go]] / [[F99-sigma-as-centre-lagrange-multiplier]] (premise (iii)), [[F144-route-a-alpha-s-dimensional-transmutation]] / [[F110-realtime-link-hamiltonian-confinement]] (the C7 identity), [[F299-casimir-scaling-discriminator-reinstated]] / [[F303-no-centre-normalisation-argument]] (X1, untouched).

---

## 0. Everything consumed, before anything is claimed

**Six premises, not two.** This section is the finding; the rest is arithmetic.

| | premise | source | how it is broken |
|---|---|---|---|
| **(i)** | $n_\text{gen}$ is **odd** — only the parity, never the value | F75, whose physical identification F75 §7 calls **a stated hypothesis** | control `n_generations=2` |
| **(ii)** | the colour sector exists, i.e. the C7 identity has an object | **F318's standing residual**, unchanged | control `empty_tower_passes=true` |
| **(iii)** | the rotor modulus is the centre $\mathbb Z_{N_c}$ | F97/F99, adopted in a tree already built at $\mathbb Z_3$ | not broken here — §7 |
| **(iv)** | quarks sit in the **defining** rep with multiplicity $N_c$ | colour-sector fact, consumed by the *lower* constraint | control `quark_colour_rep=adjoint` |
| **(v)** | one colour-singlet lepton doublet per generation; right-handers $SU(2)$ singlets | posited in `derive_ncolour`'s six-row system, derived nowhere in this chain | control `include_lepton_doublet=false` |
| **(vi)** | no fermion doubling, $f=1$ | **CL020 is `narrowed`** | control `doubler_multiplicity=2` |

**Premise (i) is optional.** Bär & Wiese impose the anomaly **per generation**, which needs no generation count at all. That form is implemented (`per_generation=True`, returning the odd $N_c$ with `constraint_bites` true at any $n_\text{gen}$); it is stronger, and it costs the assumption that each generation must be independently consistent. The conservative total-count form is the default.

**What is *not* consumed:** any measured **number**; the three-constituent baryon; either branch of X1. *"No measured number" is not "no empirical input"*, and this finding does not use the two interchangeably — see §6.

---

## 1. Why $N_c=2$ was the crux, and what this actually adds

| route | kills $N_c=2$? | cost |
|---|---|---|
| F293 R1 — local anomaly cancellation | no | nullspace dim 1 for **every** $N_c$ |
| F293 R2 / R3 — spatial-3, $\mathbb Z_3$ | no | closed no-go; circular |
| F293 §4.2 — the $\Lambda$-scale selector | yes | a **measured number**, and F299 contradicted the reading it needs (**X1**) |
| F298 — the C7 identity | no | it is an *upper* bound; $N=2$ passes |
| F317 §6 / F318 §D | yes | the **same** three-constituent baryon, spent twice |
| **this finding** | **yes** | six premises, none of them a measurement or the $\varepsilon$ count |

**And the honest size of it: one bit.** F298 already left $\{2,3\}$. The parity selects between two members of a set the tree had, one of which ($N=2$) passes F298's criterion *vacuously* (§3). That is the whole incremental content, and §8 does not dress it up.

---

## 2. The lower constraint — the $\mathbb Z_2$ doublet parity

$\pi_4(SU(2))=\mathbb Z_2$: an $SU(2)$ gauge theory with an **odd** number of Weyl isospin-$\tfrac12$ doublets has no well-defined path integral (Witten 1982).

**This is prior art and is stated as such before the table.** Bär & Wiese, *Can one see the number of colors?*, Nucl. Phys. **B609** (2001) 225, write verbatim: *"In order to cancel Witten's global anomaly, the number of colors must be odd in the standard model."* What is new here is only that the group and the content are **derived in this tree** rather than assumed, and that the parity is **paired** with F298.

**G0 (the rule, quoted, and cross-checked against an independent form).** The obstruction is non-trivial iff $2j\equiv1\ (\mathrm{mod}\ 4)$, equivalently iff the Dynkin index normalised to $T(\tfrac12)=1$ is odd:

| $2j$ | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| $T(j)$ | **1** | 4 | 10 | 20 | **35** |
| carries $\mathbb Z_2$ | **yes** | no | no | no | **yes** |

The two forms agree on every isospin tested. *Caveat recorded although it does not bite:* on **non-spin** manifolds with a spin-$SU(2)$ structure there is a further obstruction at isospin $4r+\tfrac32$ (Wang–Wen–Witten, 1810.00844). The model has no isospin-$\tfrac32$ field, so only the $2j=1$ clause is ever used — which G0 asserts rather than assumes. Bosons contribute nothing to a *fermionic* mod-2 index, which is a statement about the index and not a claim that no bosonic sector could ever participate in anomaly matching.

**W1 (content, imported not re-typed).** `derive_ncolour.hypercharge_nullspace_symbolic` returns

$$y_Q:y_u:y_d:y_L:y_e:y_\nu:y_\phi=1:(N_c{+}1):(1{-}N_c):-N_c:-2N_c:0:N_c,$$

whose $y_L=-N_c\,y_Q$ row **is** the statement that the count is $N_c$ quark doublets against one lepton doublet. $D_\text{gen}=N_c+1$. W1 is deliberately **not** parameter-adaptive, so the content controls break it.

**W2 (the parity, exact over ℤ).** $D=n_\text{gen}(N_c+1)$:

| $N_c$ | 1 | **2** | **3** | **4** | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| $D$ at $n_\text{gen}=3$ | 6 | **9** | **12** | **15** | 18 | 21 | 24 | 27 |
| $\mathbb Z_2$ | 0 | **1** | **0** | **1** | 0 | 1 | 0 | 1 |

$N_c$ odd. **W2b:** the constraint excludes a non-empty set — exactly $\{2,4,6,8,10,12\}$ — so it is a statement, not a property of every content.

### 2.1 Two things the parity is *not*, and one thing it is

**W3 — not circular through colour.** If colour were $SU(2)$, the Weyl fermions in the **colour** doublet written all-left-handed are $Q_L$ (two, one per weak component) and $(u_R)^c,(d_R)^c$ (one each) — pseudo-real conjugation is count-preserving since $\mathbf2\cong\bar{\mathbf2}$ — so **four per generation, hence 12, hence even.** Colour's own $\mathbb Z_2$ anomaly is **satisfied** at $N_c=2$; the exclusion runs through $SU(2)_L$.

> **But this does not make the constraint colour-input-free.** Premise (iv) — quarks in the defining rep with multiplicity $N_c$ — is a colour fact and the parity consumes it. What the parity does **not** consume is the $\varepsilon$-singlet's index count, which is the fact F317 §6 and F318 §D share. That distinction is why the two constraints can be paired without double-counting, and it is narrower than "no colour fact is used".

**W3b — premise (iv), measured.** The bracket is a *function* of the quark's colour representation:

| $R_\text{colour}$ | fundamental | adjoint | two-index antisym | symmetric |
|---|---|---|---|---|
| bracket returns | $\{3\}$ | $\{2\}$ | $\{2,3\}$ | $\{2\}$ |

The bit's sign is set by an empirically fixed content. Recorded as a leg rather than a footnote because it is the sharpest available statement of how much work premise (iv) does.

**W4 — not a re-attack of F293 R1.** F293's six rows are anomaly-**cancellation** rows. The global obstruction is a mod-2 index and is not a linear condition on charges; the local reading of §2.2 is a **quantisation** condition, also not one of those rows. Measured: nullspace dim **1 at every $N_c$**, gravitational and cubic anomalies **identically zero in $N_c$**, while the $\mathbb Z_2$ invariant over $N_c=1,2,3,4,5,7$ reads $0,1,0,1,0,0$. R1 stays closed.

### 2.2 The same constraint arrives **locally** — Y1

If the model's true electroweak factor is $U(2)$ rather than $SU(2)\times U(1)$ — i.e. if hypercharge is quantised so the $\mathbb Z_2$ quotient acts — then by Davighi–Gripaios–Lohitsiri (1910.11277) and Davighi–Lohitsiri (2001.07731) the Witten anomaly is **replaced by a local one**, via the quantisation rule $q\equiv 2j\ (\mathrm{mod}\ 2)$: every doublet must carry odd charge. On this model's own nullspace $y_Q=1$, $y_L=-N_c$, so the rule reads **$N_c$ odd** — the same constraint by a different mechanism.

> This is a *strengthening*, not a hedge: the conclusion does not wait on the tree settling whether its global gauge group carries the quotient, because both structures give it.

### 2.3 What the parity rests on

It bites **because $SU(2)_L$ is chiral**. Pair every left-handed doublet with a right-handed one and $D$ doubles, every $N_c$ passes, and the constraint is vacuous (`vector_like_su2=true`). F27's chirality is load-bearing for the colour *count* — the same dependency F317 §5 found for colour's *tracelessness*, reached from the other side.

---

## 3. The upper constraint — F298, imported, and both its edges labelled

**U1.** F298's criterion unchanged: a level-independent $\chi_k=s(k)^2/(4g^2C_2(\text{antisym }k))$ exists iff the k-string tower is non-empty and every level agrees. F298 scanned $N=2\ldots7$; scanned from $N=1$:

| $N$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tower size | **0** | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| identity exists | **no** | **yes** | **yes** | no | no | no | no | no | no |

Support $\{2,3\}$. **U1b names both edges for what they are, because neither is a clean exclusion:**

* **$N=1$ fails by convention.** `_c7_exists_on_ladder` returns `len(chis) == 1`. Read "level-independent" as *"no two levels disagree"* instead of *"a unique $\chi$ is determined"* and the empty tower passes, the support becomes $\{1,2,3\}$, and the bracket returns $\{1,3\}$. **Uniqueness turns on one character.** Nothing in the mathematics chooses; **premise (ii) chooses**. The $N=1$ edge is therefore a *restatement of premise (ii) in the ladder's vocabulary*, not an independent leg, and the control `empty_tower_passes=true` is where that is measured rather than admitted.
* **$N=2$ passes vacuously** — one level, nothing matched.

> Over the whole scan the criterion has **exactly one non-trivial pass**, and it is $N=3$.

**U1c — the truncation cuts both ways, and this direction had not been named.** F298's tower is the k-string sector, not the full link Hilbert space (F110 deferred the rest, and `casimir_ladder`'s own scope note says so). The direction usually recorded is that mixed-symmetry irreps might *restore* level-independence at $N\ge4$. Measured here: they **break it at $N=3$ too.** The sextet $(2,0)$ carries $N$-ality 2, so the model's own rotor rule assigns $s^2=1$ against $C_2=10/3$:

$$\chi_{\mathbf 6}=\tfrac{3}{10}\qquad\text{against the tower's}\qquad \chi=1/C_F=\tfrac34 .$$

So the support $\{2,3\}$ is a property of the **truncation**, not yet of the model. That is falsifier 5b and it is the most serious structural exposure on the upper side.

**Mechanical note.** The criterion is re-evaluated on the imported `antisymmetric_ladder` rather than by calling `c7_against_casimir_ladder` at $N=1$, because that entry point also runs its *symmetric control tower*, whose $C_2([k],1)=0$ — it raises `ZeroDivisionError`. Agreement with F298's entry point wherever both are defined is a returned field, not an assumption.

---

## 4. The bracket

**B1.** Over $N=1\ldots12$, both edges scanned:

$$\{2,3\}\ \cap\ \{1,3,5,7,9,11\}\;=\;\boxed{\{3\}}$$

| $N_c$ | 1 | 2 | 3 | 4 | 5 | ≥6 |
|---|---|---|---|---|---|---|
| $\mathbb Z_2$ | ✓ | ✗ | ✓ | ✗ | ✓ | alternates |
| C7 | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| **allowed** | ✗ | ✗ | **✓** | ✗ | ✗ | ✗ |

**B1c — the argument can fail.** At a true $N_c\ge4$ the bracket returns the **empty set**: the model would be falsified, and F144's $g_s$ derivation would lose its object with it. Recorded as a leg because an argument that cannot fail is not an argument, and because this is the compensating virtue against §8's one-bit accounting.

**Not a check.** The flags *"consumes no measured number / no three-constituent baryon / no X1 branch"* are author **declarations**. They are returned in a `declarations` field and are deliberately **kept out of the pass count** — a flag that cannot go red has no business occupying a slot in an $n/n$.

---

## 5. The corollary, stated as a corollary

**P1.** With $N_c$ fixed independently, scan $n$ rather than fixing it at 3:

| $n$ | 1 | 2 | **3** | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| $\dim\Lambda^n(\mathbb C^3)$ | 3 | 3 | **1** | 0 | 0 |
| singlets | 0 | 0 | **1** | 0 | 0 |

> **This is a corollary, not a discovery.** Given premise (iv) and the totally antisymmetric singlet, the constituent count **is** $N_c$ — §0 says so. What §5 establishes is the **direction of the equivalence**: F317 §6's *"baryons have three constituents"* was never information about the model independent of $N_c$. That is precisely why discharging it costs nothing, and why F318's double-count warning loses its object.

**P2 — agreement, explicitly not confirmation.** The exact-over-ℚ kernel reproduces F317 §6's float/SVD route on the whole $n=3$ column: $(N,\text{singlets})=(2,0),(3,1),(4,0),(5,0),(6,0)$. Two implementations agreeing. Counting it as confirmation would be the double-count F318 warned about.

---

## 6. "No measured number" — what that does and does not mean

**True:** no real-valued measurement enters the bracket. Nothing from `derive_ncolour`'s $\alpha_s(M_Z)$ / $M_Z$ block reaches it; only the symbolic nullspace does. F293 §4.2's selector is not used, and neither X1 branch is.

**Not true:** that the bracket is empirical-input-free. It consumes six premises (§0), of which (i), (iv), (v) and (vi) are empirically sourced integers or booleans. **The claim is "no measured number", never "no measurement".** The card CL281 states it the same way, and a reader who finds the two used interchangeably anywhere in this tree should treat that as a defect and say so.

**The trade, stated without special pleading.** The old input was *logically equivalent to the answer*; the new premises are not. That is an improvement in **proximity** — not in empirical status (three generations is as empirical as three constituents) and **not in premise count**, which went *up*. §8 is where to disagree.

---

## 7. Declared controls, with the **measured** red sets

Eight controls, each red and red only where declared. Measured, not anticipated.

| control | measured reds | bracket | what it breaks |
|---|---|---|---|
| `n_generations=2` | W2, W2b, W3b, B1 | $\{2,3\}$ | premise (i) |
| `include_lepton_doublet=false` | W1, W2, B1 | $\{2\}$ | premise (v) — the parity **inverts** |
| `vector_like_su2=true` | W1, W2, W2b, B1 | $\{2,3\}$ | F27's chirality |
| `quark_colour_rep=adjoint` | W1, W2, B1 | $\{2\}$ | premise (iv) — the colour input the constraint *does* consume |
| `c7_n_max=3` | U1 | $\{3\}$ | F298's idiom: an untested $N\ge4$ is not an excluded one |
| `scan_from=2` | U1, U1b, B1 | $\{3\}$ over $2..12$ | an untested **lower** edge |
| `doubler_multiplicity=2` | W2, W2b, B1 | $\{2,3\}$ | premise (vi) |
| `empty_tower_passes=true` | U1, B1 | $\{1,3\}$ | premise (ii) — the $N=1$ convention |

Premise (iii) — *the rotor modulus is the centre $\mathbb Z_{N_c}$* — is the one premise with **no control**, because breaking it means rebuilding the link Hamiltonian on a modulus unrelated to the gauge group, which is a different finding. It is booked in §0 and it is the quietest assumption in the chain: it was adopted (F97/F99) in a tree already built at $\mathbb Z_3$, and there is no $N\ne3$ instance where the C7 identity was ever non-trivially validated.

---

## 8. Prior art, and the honest size of the result

| leg | prior art | new here |
|---|---|---|
| §2 the $\mathbb Z_2$ parity | Witten 1982. **And the conclusion itself:** Bär & Wiese 2001 (hep-ph/0105258) — *"the number of colors must be odd in the standard model"* — obtained **unconditionally**, per generation, i.e. **stronger than the default form used here** | the group and content are **derived in this tree**; and the parity is deployed as the lower edge of an **interval** rather than as a consistency check on a known $N_c$ |
| §2.2 the local $U(2)$ reading | Davighi–Gripaios–Lohitsiri 2019; Davighi–Lohitsiri 2020 | evaluated on **this model's** $y_L=-N_c$, where it becomes the same constraint |
| §3 the C7 support | F298, in this tree | scanned one step lower; **both edges labelled** (convention / vacuous); and the mixed-symmetry direction that threatens $N=3$ measured for the first time |
| §5 the $\Lambda^n$ singlet | Greenberg 1964 | run with $n$ free, exact over ℚ, and used to establish the **direction** of an equivalence rather than to consume it |

**The size, stated plainly.** The bracket's incremental content over F298 is **one bit**, selecting between two members of a set F298 already supplied, one of which passes F298's criterion vacuously. That bit's sign is a function of the assumed multiplet content (W3b). Non-post-hocness cannot be certified from inside: the C7 criterion, its rotor identification and its sector truncation were all written in a tree already built at $\mathbb Z_3$, and there is no $N\ne3$ case where the identity was non-trivially validated. The compensating virtue is B1c — at a true $N_c\ge4$ the bracket is empty and the model dies.

---

## 9. Falsifiers

1. **Fermion doubling** (premise (vi)). The parity counts *continuum Weyl species*; an even multiplicity $f$ makes it vacuous, and worse, a naively doubled spectrum is **vector-like**, so by Nielsen–Ninomiya there is no chiral gauge theory left to constrain. The constraint survives only in a **doubler-free (Ginsparg–Wilson)** formulation, where Bär & Campos (hep-lat/0001025) exhibit the lattice analogue of Witten's obstruction. CL020 is `narrowed`. **The most likely way this dies.**
2. **The continuum-limit status of the obstruction.** $\pi_4$ is a fact about the Lie group; the model's $SU(2)_L$ is a lattice gauge symmetry. A lattice-native form is **not** attempted. (§2.2's local reading is partial insurance: under a $U(2)$ embedding the constraint is perturbative and this falsifier does not apply.)
3. **Content** (premise (v), premise (iv)). A fourth doublet species, a right-handed doublet, or a different quark colour rep changes or vacates the parity. `include_lepton_doublet=false` and `quark_colour_rep=adjoint` show the conclusion does not weaken but **inverts**.
4. **Even $n_\text{gen}$** (premise (i)) kills it — unless the Bär–Wiese per-generation form is granted, in which case this falsifier is retired and replaced by *"each generation must be independently consistent"*.
5. **The C7 identity surviving at some $N\ge4$** reopens the upper edge. F298's k-string restriction is inherited unchanged.
6. **5b — and the same restriction failing at $N=3$.** Measured in U1c: the sextet gives $\chi=3/10$ against the tower's $3/4$. If the full link Hilbert space is followed and level-independence does not survive at $N=3$, the **upper constraint has no support at all** and the bracket has nothing to intersect. This is the exposure F298 did not name and this finding does.
7. **Premise (iii).** If the rotor modulus is not the colour centre, the upper constraint is not a function of $N_c$ and the whole pairing dissolves.

---

## 10. What this closes, and what remains

**Closes.**

* **F317 §10 item 2, as written** — a structural replacement for the three-constituent baryon, paired with F298.
* **F317 §6's input**, discharged, and §5 shows why it was never independent information.
* **F318's double-count warning**, which loses its object.
* **B10's dependence on X1.** F293's selector needed branch H1; F299 measured the tree implementing H2. Neither constraint here depends on the branch, so **B10 stops being one of X1's dependents.** X1 itself is untouched and $d_1$ remains the deciding computation for B8, D16, G5, E3, Q1, Q2.

**Remains.**

1. **Premise (ii)** — the index exists by fiat. This finding needs colour to exist in order to count it, and the $N=1$ edge is that premise restated.
2. **A transfer of debt, not a closure.** B10's conditionality moved from a hadron-spectroscopy fact to F75's parity (rubric **C1**) plus premises (iii)–(vi). A completeness sweep should record a **transfer** — and that the premise count went *up*.
3. **Premise (iii) has no control** (§7), and **U1c's exposure is live** (falsifier 5b/6).
4. **Nothing here bears on** B10's three closed routes, F303's dead $n\,C_F=4$ route, or X1.

**Recommended grade motion.** B10 `PARTIAL` → `PARTIAL`, row rewritten: *the route space is mapped, the empirical selector is retired, B10 is no longer X1-contingent, and $N_c=3$ follows from an imported upper constraint and a prior-art parity given six named in-tree premises.* **Not** a promotion. The reason is in §8: one bit, on a criterion never validated at any $N\ne3$.

---

## 11. Session integrity — read this before trusting the header

The device workspace was unavailable for the entire session:

* **`make gate` was not run.** Nor `casim test`, `casim index`, `make claims`, `make control`, `make registry`.
* 14/14 and the eight control red sets were measured in an **isolated harness** importing the tree's real `casimir_ladder.py` and `derive_ncolour.py` unmodified against a `casim.numerics` shim. P2 was verified by extracting `multiplicity_squeeze` from the real `derive_su3_structure.py`, because importing it whole pulls the `gauge.strong` operator stack.
* **`_SPINE` row, test-registry record, indexes and claim card are written but unarmed.** Order that closes this: `make indexes` → `make claims` → `make gate` → `make control`.
* **This finding has been through an adversarial pass** — two independent referees, one attacking the group theory against the literature and one attacking the reasoning for circularity and overclaim. Both returned hits, and all of them are in the document above rather than in a review file: the prior-art attribution (§8), the local-$U(2)$ correction to the "invisible to local anomalies" claim (§2.2), the colour-input correction to §2.1's headline, the $N=1$ convention (U1b), the mixed-symmetry exposure (U1c), the demotion of §5 to a corollary, the removal of an unfailable flag from the pass count (§4), and the "proximity, not kind" rewrite (§6). The first draft claimed more than this one does.

`**Status:** Confirmed` is withheld deliberately. The difference between "the physics is right" and "the record runs" is the whole point of D9.
