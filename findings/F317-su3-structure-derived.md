# F317 — Colour is not put in twice: granted **one** internal index the rule does not read, SU(3)'s unitarity, its tracelessness, its locality, its connection, its vector-like coupling and its eight gluons are all **forced** — and the residual input is the index itself

**Date:** 2026-08-16 - 06:32
**Numbering:** drafted at **F316** and **renumbered to F317**: the concurrent session `gallant-great-brahmagupta-3` wrote `F316-laurent-pell-descent-proved.md` **70 seconds earlier**, so F316 is theirs and this file moved. This is exactly the residual race CLAUDE.md §Concurrency declares — the window between reading `NEXT FREE NUMBER` and writing the file — and it failed **loudly** (`casim index` reported `duplicates 1`) rather than silently, which is the trade the protocol was changed to make. F317 taken as `NEXT FREE NUMBER` (max+1; no gap closed). Session `keen-lucid-gell-mann`, sector `gauge`.
**Status:** Confirmed — **21/21 PASS** (2.2 s), **six** declared controls each verified red **and red only where declared**. Two residuals are literal `0.0`, five are exact over ℚ or ℚ[i] (`sympy`, not floats), the rest are ≤ 9.0×10⁻¹⁶.
**Verdict:** Completeness row **B1**'s colour leg moves from *"colour is still put in"* to **PARTIAL with a single named input**. $SU(3)_c$ is **not derived from nothing** — nothing here produces the internal index. What is derived is that *everything downstream of the index is not an independent choice*: grant the model one internal index its own rule does not read, and the group, its locality, its connection, its representation, the vector-like character of its coupling and its gluon count all follow.
**Side effect on an existing finding:** **F91's one unforced assignment is closed.** F91 recorded colour's vector-like coupling as `by construction` and the BCC gluon's even propagation law as **unforced**, selected by *"the elegant-design philosophy"*. §2 supplies the missing premise, so F91 G1's chain runs forward and the even law is **forced**.
**Modules:** `src/casim/engine/gauge/derive_su3_structure.py` (new)
**Test / results:** record `F317-su3-structure` (tier gate, entry `check_su3_structure`), driver `tests/findings/test_F317_su3_structure.py` → `test-results/F317_su3_structure.json`
**Cross-references:** [[F27-complex-mass-chiral-su2]] (β-gauging; *why* its $U(x)$ is pure gauge is derived here in §3), [[F91-pairing-classification-theorem]] (the assignment this closes), [[F68-minimal-coupling-forces-even-photon]] (the even-channel argument reused), [[F279-hypercharge-constraint-attribution]] / [[F293-why-three-colours]] (the hypercharge nullspace, **imported not re-derived**), [[F298-casimir-ladder-c7-rerun]] (the independent structural $N_c\le3$ that §6 agrees with), [[F289-spin-statistics-connection]] (Fermi statistics **derived**, which is what makes §6 more than a restatement), [[F43-fg7-dynamical-gluons]] ($f^{abc}$, the octet, the SU(3) links), [[F31-wmu-covariant-hopping]] / [[F110-realtime-link-hamiltonian-confinement]] (covariant hopping and Gauss law, whose *necessity* is what §3 measures), [[F313-time-signature]] (the re-typing discipline and the V-004 lesson §4 obeys), [[F71-colour-singlet-baryon-proton]] / [[F122-p2-dynamical-baryon-three-body]] (the three-body baryon §6 consumes).

---

## 0. What "put in" actually bundles, and which parts this attacks

`docs/status/completeness-2026-08-07.md` row **B1** reads:

> $SU(2)_L$ derived by β-gauging the complex-mass step; $U(1)_Y$ from bipartite sublattice parity; F291 adds the precondition that the phase $SU(2)_L$ gauges exists only for $\operatorname{coker}J=0$, i.e. $d\ge3$. **Colour is still put in**

That sentence is a bundle of six impositions, and they are not equally hard:

| | imposition | status after this finding |
|---|---|---|
| (i) | the quark carries an internal index **at all** | **still an input.** Nothing here produces it |
| (ii) | the index has dimension **3** | §6 — forced, *given* three-constituent baryons (one empirical input, labelled) |
| (iii) | its invariance group is **unitary** | §4 — **derived** (commutant computed, not assumed) |
| (iv) | the group is **special** unitary, not $U(3)$ | §5 — **derived** (the trace part is anomalous) |
| (v) | the symmetry is **local**, so it carries a connection | §3 — **derived** (and the same argument explains F27's pure-gauge $U(x)$) |
| (vi) | the coupling is **vector-like**, where $SU(2)_L$'s is chiral | §2 — **derived** (a chiral triplet is anomalous; a chiral doublet is not) |

**The honest headline is (i), and it is stated before the results rather than after them.** This finding does not derive colour. It shows that colour is *one* input, not six, and it names the one.

---

## 1. The generators are checked, not trusted

`su(N)` is built here from scratch (symmetric / antisymmetric off-diagonals plus the $N-1$ Cartan elements) rather than imported from `gauge.strong`, precisely because §2 is a statement *about* the colour sector and must not inherit its conventions. The basis is then verified: $\max_{ab}\lvert \operatorname{Tr}(T^aT^b)-\tfrac12\delta^{ab}\rvert = $ **`0.0`** (S0).

---

## 2. Colour **cannot** be chiral, and $SU(2)$ **can** — so the model's chiral/vector split is one fact, not two

Define the symmetric anomaly coefficient $A^{abc}=2\operatorname{Tr}\!\big(T^a\{T^b,T^c\}\big)$.

**S1a (exact over ℚ[i]).** For $su(2)$, **all 27** triples are exactly zero — largest magnitude the integer `0`, not a rounding. There is no symmetric invariant, so a single chiral doublet is anomaly-free.

**S1b (exact).** For $su(3)$,

$$A^{888} \;=\; 4\operatorname{Tr}\big(T^8\big)^3 \;=\; -\tfrac{1}{\sqrt3} \;=\; -\tfrac{\sqrt3}{3}\ \neq\ 0 .$$

**S1c.** Running the three candidate colour assignments through $A_L-A_R$:

| assignment | $\max\lvert A_L-A_R\rvert$ | consistent? |
|---|---:|---|
| **vector-like** ($L=\mathbf3$, $R=\mathbf3$) | **0.0** | **yes** |
| chiral ($L=\mathbf3$, $R=\mathbf1$) | $0.5773502691896257$ | no |
| conjugate ($L=\mathbf3$, $R=\bar{\mathbf3}$) | $1.1547005383792515$ | no |

Exactly one survives.

> **The model's chiral weak sector and vector-like strong sector are not two independent design decisions.** Given that the weak group is $SU(2)$ and the colour group is $SU(3)$, the first *may* be chiral and the second **must not** be. F27 was free to gauge $\beta$ chirally; colour never was.

### 2.1 What this closes in F91

F91's G1 row reads, verbatim:

> **G1 (machine):** … The model's own octet bilinear applies the *same* $T^a$ to both chiralities (η and χ): **vector-like by construction**.

and its Gluon row concludes:

> the assignment is **unforced**, and the F68-mirror argument + the elegant-design philosophy select the even law.

S1c replaces *by construction* with *forced*. F91's chain then runs with no free step:

$$\text{anomaly freedom}\ \Rightarrow\ (g_L,g_R)=(g_s,g_s)\ \Rightarrow\ \text{branch-space coupling}\ \propto\mathbf 1\ \Rightarrow\ \text{(F68 verbatim)}\ \text{even law}.$$

**S2a.** The traceless part of $\operatorname{diag}(g_L,g_R)$ is **`0.0`** for the vector-like assignment — a branch *scalar*, which can only source the helicity-symmetric channel.

**S2b (the contrast, so S2a is not vacuous).** Measured on the model's own BCC dispersion, on the body diagonal at $\lvert k\rvert=0.4$: a chiral colour would have split the branches by

$$\lvert\Omega^+-\Omega_\text{even}\rvert = 5.137\times10^{-3} \;=\; \tfrac12\lvert\Delta\Omega\rvert\quad(\text{identity residual } 1.4\times10^{-17}),$$

the F67/F91 separation. The even law is therefore a *statement*, not a tautology — and the declared control `chiral_colour=true` reds S2a and nothing else.

---

## 3. Locality forces the connection — and explains why F27's $U(x)$ does **not** need one

This is the part that is genuinely CA-native rather than borrowed.

**A cellular automaton has no global operations.** Its rule is *one* operator applied at every cell. So an internal rotation $V$ acting on an index the rule does not read commutes with the on-site step whether $V$ is constant or **site-dependent** — a local symmetry is free in a CA, not an extra assumption. The hopping step is different in kind, because it compares amplitudes at two cells that $V(x)$ and $V(x+\hat\mu)$ rotate differently.

Measured on a ring with an internal index (`locality_forces_connection`), and independently through the tree's own `gauge.strong` operators (`locality_forces_connection_tree`):

| leg | statement | residual |
|---|---|---:|
| **S3a** | on-site step commutes with a **site-dependent** $V(x)$ | $7.0\times10^{-16}$ |
| **S3b** | bare hop, no compensator — covariance **fails** | $\mathbf{1.343}$ |
| **S3c** | with $U_\mu\to V(x)U_\mu V^\dagger(x{+}\hat\mu)$ — covariance exact | $6.0\times10^{-16}$ |
| **S3d** | the same three legs on the tree's own SU(3) field/links/transforms | $\mathbf{1.391}$ / $4.3\times10^{-16}$ |

> **The gluon field is not added to the model. It is the price of the rule being local.** And the *same* statement, read on the other step, is F27's result: the mass step is **on-site**, so its $V(x)$ is absorbed with no compensator — which is exactly why F27 found $U(x)$ to be pure gauge and why F27's own limitation #1 (*"the kinetic step is not SU(2) invariant alone"*) had to be true. One principle covers both sectors.

The connection carries $N^2-1 = 8$ parameters per link, which is §7.

**Control.** `use_compensator=false` drops the link's transformation law: S3c **and** S3d go red, and only those. A covariance test that passes without the connection has not tested the forcing — that is the whole content of §3.

---

## 4. Unitarity fixes the group to $U(N)$ — the commutant is computed, not asserted

"Internal" *means* the rule acts on that factor as the identity: $R\otimes\mathbf 1_N$. Two numbers follow, and the first is what stops the second being trivial.

**S4a.** The model's own steps must generate the **full** $M_4$ on the Dirac factor, or the commutant would be large for an uninteresting reason. Taking the F27 mass step (branch-off-diagonal, re-typed from the finding) together with the BCC walk $A_s(k)=u_s(k)\mathbf1+i\,\tilde n_s(k)\!\cdot\!\sigma$ (re-typed from Paper 1 Eq. 15 / `lattice.dimensionality.bloch_vector`) at five probe momenta:

$$\dim\big\langle\, \text{mass},\ \text{walk}(k_i)\,\big\rangle = \mathbf{16} = \dim M_4 .$$

**The re-typed walk's unitarity is asserted, not assumed** — $\max\lVert W^\dagger W-\mathbf1\rVert = 2.2\times10^{-16}$. This is the guard the F313 review found missing in `check_C4b`, and it is here because that review is why the defect class is known.

*Recorded because it was hit:* the first draft used a branch-diagonal phase $\operatorname{diag}(e^{i\omega_+},e^{i\omega_-})\otimes\mathbf1_\text{spin}$ as the walk. It is **spin-blind**, so the generated algebra was $M_2\otimes\mathbf1$ of dimension **4**, and the commutant came out **36**, not 9. The count only means what it claims once the walk is the model's actual spin-mixing one. The false version is kept out of the module but recorded here, because a reader re-deriving this will reach for the same shortcut.

**S4b.** On the full $4N$ space, the commutant of the rule has dimension

$$\dim\mathcal C = 9 = N^2 = \dim M_N ,$$

i.e. the full matrix algebra on the internal factor. Its norm-preserving subgroup is exactly $U(N)$. **The group is a measured consequence of the rule being blind to the index plus the rule being unitary.**

**S4c — a prediction, not an input.** $R\otimes\mathbf1_N$ makes every level exactly $N$-fold degenerate: multiplicities $[3,3,3,3]$, residual $9.0\times10^{-16}$. This is *why* the index is unobservable in the dispersion, i.e. why it is internal at all.

**Control.** `rule_reads_colour=true` lets one Gell-Mann matrix into the rule. The commutant collapses $9\to\mathbf3$ and S4b goes red, alone. The index stops being internal and $U(3)$ stops being the invariance group.

---

## 5. $U(N)\to SU(N)$: the trace part is anomalous, **because $SU(2)_L$ is chiral**

The $U(1)$ subgroup of $U(N_c)$ assigns one colour-blind charge $b$ to every quark and none to any lepton. Only left-handed $SU(2)_L$ doublets contribute to $[SU(2)_L]^2U(1)_X$ — the model has no right-handed doublet, which is F27's chirality. Evaluated on the model's **own** hypercharge nullspace (imported from `derive_ncolour.hypercharge_nullspace_symbolic`, not re-derived), with $y_Q:y_L = 1:-N_c$:

$$\textbf{S5a}\quad A_{[SU(2)_L]^2U(1)_Y}=\tfrac12\big(N_c\,y_Q+y_L\big)=\tfrac12\big(N_c-N_c\big)\;\equiv\;\mathbf 0\quad\text{identically in }N_c$$

$$\textbf{S5b}\quad A_{[SU(2)_L]^2U(1)_\text{trace}}=\tfrac12\big(N_c\,b+0\big)=\boxed{\tfrac{N_c\,b}{2}}\;\neq\;0\ \ \text{for any }b\neq0$$

> **The colour group is the traceless part, and the reason is the model's own derived chirality.** $U(1)_Y$ survives because the *same* row that fixes hypercharge, $N_cy_Q+y_L=0$, is what a colour-blind charge cannot satisfy. If $SU(2)_L$ were vector-like both would vanish and $U(3)$ would be available; F27 is what removes it.

**S5c.** Independently: the nullspace has dimension **1** (F279/F293, for every $N_c$), so exactly one abelian direction exists and it is already spent on $Y$. A gauged colour trace would need a second.

**S5d/S5e — colour's own anomalies, on the model's own content, and neither is vacuous.** The first-generation content is one left-handed $SU(2)_L$ doublet of colour triplets (2 members) and two right-handed colour-triplet singlets $u_R,d_R$:

| anomaly | value | why it is not an identity |
|---|---|---|
| $SU(N_c)^3$ | $A(\mathbf3)\cdot(2-2) = \mathbf{0.0}$ | $A(\mathbf3)=0.5773502691896257 \neq 0$ (S1b), so this is a statement about the **content** |
| $SU(N_c)^2U(1)_Y$ | $2y_Q-(y_u+y_d) = 2-\big[(N_c{+}1)+(1{-}N_c)\big] \equiv \mathbf 0$ | a genuine cancellation between $y_u=N_c+1$ and $y_d=1-N_c$, **identically in $N_c$** |

**Control.** `drop_d_R=true` deletes one right-handed colour triplet: the cubic anomaly becomes $0.577$ and the mixed one becomes $1-N_c$. Both S5d and S5e go red, and only those. This is what makes them checks rather than restatements.

---

## 6. The multiplicity, given three-constituent baryons — an upper **and** lower bound in one computation

Computed, not quoted: the dimension of the $SU(N)$-invariant subspace of $\Lambda^3(\mathbb C^N)$, as the joint kernel of the total generators $G^a=T^a\!\otimes\!\mathbf1\!\otimes\!\mathbf1+\dots$ restricted to the antisymmetric subspace.

| $N$ | $\dim\Lambda^3(\mathbb C^N)$ | singlets |
|---:|---:|---:|
| 2 | 0 | 0 |
| **3** | **1** | **1** |
| 4 | 4 | 0 |
| 5 | 10 | 0 |
| 6 | 20 | 0 |

A totally antisymmetric **three**-index invariant exists at **exactly one** $N$, and it is 3. For $N\ge4$ the invariant tensor has $N$ indices, so the singlet needs $N$ constituents, not three.

**The inputs, separated.**

* **Derived here / in the tree:** Fermi statistics — F289 derives the spin-statistics theorem's *own two premises* ($R(2\pi)=-\mathbb1$ from the rotor; $\pi_1=S_n$ from the derived $d=3$), so the antisymmetry demand is not imported. Colour-singlet confinement (F86/F110).
* **Empirical, and this is the price:** that baryons are **three**-constituent bound states with a symmetric space⊗spin⊗flavour ground state. That is hadron spectroscopy — the constituent-quark $SU(6)$ 56-plet the tree's own F71 builds and F122 binds — not a lattice fact.

**What this is and is not, for row B10.** It is **not** one of B10's three closed routes: it is not the anomaly route (§5 is a statement about $U(1)$, not about $N_c$ — and F293's nullspace is dimension 1 for *every* $N_c$, which this finding uses and does not contradict), not the spatial-3 identification (F293 §2, untouched), and not the $\mathbb Z_3$ centre (F293 §3, untouched — no centre appears anywhere above). It agrees with, and is logically independent of, **F298**'s parameter-free $N_c\le3$: F298 bounds from above with no measured number, §6 pins exactly, consuming one. Neither is a derivation of 3 from lattice structure alone, and this finding does not claim one.

**Controls.** `n_colour=4` reds S6b and only S6b — the argument is $N$-sensitive, not generic. `n_colour=2` reds S1c, S5d **and** S6b together, which is the cleanest single statement of §2: *at $N=2$ colour could have been chiral, and there would be no three-quark singlet.*

---

## 7. Eight gluons

$\dim su(3)=N^2-1=\mathbf 8$; the algebra closes on its own structure constants (closure residual $5.6\times10^{-17}$, $f^{abc}$ antisymmetry $\le10^{-16}$), reproducing F43's octet from the connection §3 forced rather than from a posited field.

---

## 8. Prior art, and what is actually new

Stated plainly, because three of the seven legs are textbook results and a finding that hid that would deserve the F313 treatment.

| leg | prior art | what is new **here** |
|---|---|---|
| §2 $d^{abc}$ obstruction to a chiral triplet | standard (Georgi; Weinberg II §22) — $SU(2)$ is anomaly-safe, $SU(N\ge3)$ is not | it **closes F91's own recorded gap**: the model had colour vector-like *by construction* and the BCC gluon's even law *unforced*, chosen on elegance. The split is now forced by the model's content |
| §3 the gauge principle | standard; and F31/F110 already implement covariant hopping and Gauss law | the **CA-native half**: a CA rule has no global operations, so locality is not an extra assumption but a property of the update, and the on-site/hopping asymmetry *derives* why F27's $U(x)$ is pure gauge while the gluon is not. That contrast is measured, not argued |
| §4 commutant $\Rightarrow U(N)$ | Schur / double-commutant, standard | it is **computed on the model's own two steps**, with the walk re-typed and its unitarity asserted, and it yields the $N$-fold degeneracy as a *prediction* rather than an input |
| §5 $[SU(2)_L]^2U(1)_B\neq0$ | standard (why $B$ is not gauged in the SM) | evaluated on the **model's own derived nullspace**, where it becomes the statement that F27's chirality is what removes the $U(1)$ from $U(3)$ — and $S5e$'s $y_u+y_d=2$ cancellation is a fact about *this* model's hypercharges |
| §6 the $\varepsilon$/Fermi-statistics count | the oldest argument for colour (Greenberg 1964; the $\Delta^{++}$) | the antisymmetry premise is **derived in-tree** (F289) rather than imported, the singlet count is computed across $N=2..6$ rather than quoted, and it is placed against F298's independent upper bound |

**Nothing in §§2–7 is claimed as new mathematics.** What is claimed is that the model's colour sector, which the completeness report grades as *imposed*, is imposed **once** — and the six impositions it was carrying reduce to one.

---

## 9. Falsifiers

1. **§4 is the load-bearing one.** If any step of the rule is found to read the colour index — a genuine colour-dependence in the walk or the mass step, not a background gluon — then the commutant is no longer $M_N$, the invariance group is smaller than $U(N)$, and §§4–5 collapse. The control `rule_reads_colour=true` is exactly that failure, made to fire ($9\to3$).
2. **§2 fails if the model's colour representation is ever something other than a single fundamental per chirality.** A reducible or higher assignment can be anomaly-free while chiral, and the forcing of the even law goes with it.
3. **§5 fails if $SU(2)_L$ is ever made vector-like** — e.g. if a right-handed doublet enters the content. Then $[SU(2)_L]^2U(1)_\text{trace}$ vanishes, $U(3)$ becomes available, and the tracelessness of colour is unexplained again.
4. **§6 fails if the model's baryon is not a three-constituent object** — if the tree's own binding sector ever produces a stable colour-singlet from a different number of constituents, the $\Lambda^3$ count selects a different $N$.
5. **§3 is untouched by any of the above** and fails only if a local internal symmetry is exhibited that needs no compensator on a hopping step — which would mean the hop is not comparing two cells.

---

## 10. What this closes, and what remains

**Closes.**

* Row **B1**'s colour leg: from six impositions to one. (iii), (iv), (v), (vi) derived; (ii) pinned given one empirical input.
* **F91's last unforced assignment.** The BCC gluon's even propagation law was selected by elegance; it is now forced by anomaly freedom.
* The asymmetry *why is the weak force chiral and the strong force not?* — one line of group theory, evaluated on this model's content.

**Remains, and is the honest headline.**

1. **The internal index itself is still an input.** Nothing above produces it. The natural next attack is whether the cell dimension can carry it — F291's spatial bound $2\log_2 s+1$ and F313's $d_\text{time}=s-1$ both live on the *minimal* $s=2$ cell, and the coloured quark field is $s=36$. Whether the enlargement is forced or chosen has never been asked.
2. **§6 consumes one empirical number** and says so. A lattice-structural replacement for *"baryons have three constituents"* would make §6 a derivation; F298's $N_c\le3$ is the only other structural leg the tree has, and pairing them is the shortest route to closing B10 without the F293 selector.
3. **This finding does not touch the X1 colour-normalisation fork** (centre vs Casimir). Nothing above depends on which branch is right, and nothing above helps decide it.
4. **Higher generations and the third-generation content are not checked** — §5's anomaly rows are first-generation, exactly as F38/F279 are.
