# F313 — The "+1": the Cayley-graph/update split is computed, not chosen, and the time rank is 1

*2026-08-12 - 09:40 · sector `lattice` · module `casim.engine.lattice.time_signature` ·
test record `F313-time-signature` (13/13 PASS, gate tier) ·
results `test-results/F313_time_signature.json`*

**Reviewed:** 2026-08-13 — **OVERSTATED** ([independent review](../docs/reviews/F313-review-2026-08-13.md)) ·
**Remediated:** 2026-08-13 - 14:10

> **What the review changed, in one place.** The $s=2$ result is **correct** and was independently
> re-derived by a blind agent via a different route (Newton-polytope descent rather than a cited
> Pell theorem), which is the strongest support the review process can produce. What was overstated
> was the packaging, and all of it has been retracted **in place** rather than rewritten away:
>
> | § | Change |
> |---|---|
> | §2 | **Inputs declared: three, not one.** $s=2$ **+ infinite volume + the three Cayley generators**. "Local ≡ Laurent" is the locality assumption, not its elimination |
> | §4 | gcd corrected $1+i\to\mathbf 1$; C2's criterion corrected from "is a constant" to "is a unit" |
> | §5 | "$d_\text{space}=3$ recovered from the commutant" **withdrawn** — circular |
> | §6 | Citation corrected: **not Abel 1826**; Pastor 2001 / Dubickas–Steuding 2004 Thm 2. The real import is the polynomial→Laurent **transfer** |
> | §8 | Boxed $(\dim\mathfrak{su}(s),\operatorname{rank}\mathfrak{su}(s))$ identity **withdrawn** — numerology, contradicted by the model's own $s=4$ cell |
> | §9 | Now **settled** by F315: the second flow does not survive interaction |
> | §11 | Falsifier 6 restated; three real falsifiers added |
> | header | check count corrected 11 → **12** (now **13**, after the C0 control was added) |
> | §6 | **the import itself CLOSED 2026-08-13 by F316** — the transfer is now proved in-repo |
>
> The claim that survives: **$d_\text{time}=1$ at $s=2$ on an infinite lattice**, with the update
> the unique flow up to shifts and powers. That is a real result and it is what CL269 now asserts.

**Target.** `docs/status/completeness-2026-08-07.md` rubric row **A1**, whose spatial half
F291/F292 closed and whose remaining residual is named in the row itself:

> *A1 · Spacetime dimensionality · PARTIAL · Residual / free inputs: **the "+1"**; $s=2$ minimal
> cell. … Not `EXACT` — the "+1" is by construction.*

F291 §6 is explicit about the gap and §7 states the price of closing it:

> *"A genuine derivation of the '+1' would have to explain why the Cayley-graph/update split is
> not itself a choice."*

This finding pays that price. The split is not assumed anywhere below; it is **computed**, and
it comes back with the ranks attached.

---

## 1. What F291 actually asserted, and why it is not enough

F291 §6 offers one sentence of argument:

> *"Any second commuting unitary flow would, under homogeneity, be a further generator of the
> Cayley graph — that is, another **space** direction, which S1 then caps at three."*

Read carefully, that is a claim in the **wrong direction**. It says *if* a second flow existed it
would be spatial — which, granted, would keep the total at four. But it presupposes exactly the
thing at issue: that "the Cayley graph" and "the update" are two separately given objects, one of
which absorbs any surprise. Nothing in F291 shows that the operators the model calls translations
are the *only* scalar symmetries, nor that the operators it calls evolution are the *only*
non-scalar ones. Both are stipulations of the construction.

The fix is to stop naming things. Take the one object the model has — the update unitary $A$ —
and ask for its **commutant** inside the local homogeneous unitaries. Then see what the commutant
does on its own.

---

## 2. The setting

Local homogeneous operators on the BCC lattice are $2\times2$ matrices over the Laurent ring

$$R \;=\; \mathbb C\!\left[w_1^{\pm1}, w_2^{\pm1}, w_3^{\pm1}\right],
\qquad w_j = e^{ik_j/\sqrt3},$$

with the involution $f^*$ = adjoint on the real torus ($w_j\mapsto w_j^{-1}$, coefficients
conjugated). **"Local" is exactly "Laurent polynomial"** — a finite neighbourhood is a finite
exponent support.

> **INPUTS DECLARED 2026-08-13** (review attack 2 — free inputs undercounted by 2). The original
> text said this "no locality condition has to be imposed by hand", which is backwards: writing the
> algebra as $R$ **is** the locality assumption, and it is load-bearing, because it is what makes
> the units monomials in §5. The finding's inputs are therefore **three, not one**:
>
> 1. **$s=2$**, the minimal cell (founding decision 6 / BDPT).
> 2. **Infinite volume.** Nowhere stated in the original finding, module, test or card, and
>    load-bearing. On a finite periodic $L^3$ lattice $\mathbb C[\Lambda/L\Lambda]$ is **not a
>    domain**, every homogeneous operator is trivially local, units are not monomials, and the
>    commutant's unitary group becomes a torus of rank $\sim2\lvert\mathrm{BZ}\rvert$. **§§5 and 6
>    both collapse.** $d_\text{time}=1$ is an infinite-volume statement.
> 3. **The three Cayley generators**, i.e. locality with respect to the automaton's own BCC group
>    $\Lambda$ (index 4 in $\mathbb Z^3$), not the ambient $\mathbb Z^3$.
>
> Also load-bearing and worth naming: the descent needs **unitarity** ($p^*=p$), not merely
> $\det=1$. Drop unitarity and one is left with a rank-2 *module* on which the $d_\text{time}$
> question has no answer.

The BCC Weyl update
(Paper 1 Eq. 15, in the sign-corrected form `lattice.bcc._bcc_uvec` runs) is

$$A \;=\; u\,\mathbb I \;-\; i\,\boldsymbol\sigma\cdot\tilde{\mathbf n},
\qquad u^2 + \lVert\tilde{\mathbf n}\rVert^2 = 1, \qquad u,\ \tilde n_j \in R .$$

Everything below is a statement about
$\mathcal C \;=\; \{\,B \text{ local, homogeneous, unitary} : BA = AB\,\}$.

---

## 3. C1 — the commutant is 2-dimensional, and $s=2$ leaves no other option

Solving $[B,A]=0$ for a general $2\times2$ $B$ over the function field returns a solution space of
dimension exactly **2**, spanned by $\mathbb I$ and $\boldsymbol\sigma\cdot\tilde{\mathbf n}$
(check C1).

This is not a fact about the BCC rule. It is a fact about $s=2$:

> A $2\times2$ unitary either **is a phase** — the trivial automaton, already excluded by F291's
> S1 route (b), which needs $c_\text{lat}=d\Omega/d\lVert\mathbf k\rVert$ to exist — or it has
> **two distinct eigenvalues**, in which case its commutant is the 2-dimensional algebra it
> generates. There is no third option.

So at the minimal cell there is **no room** for a second flow, and the count that follows is not a
lucky feature of the rule. At $s\ge3$ a *structural* degeneracy becomes available and duly occurs;
that is §8.

---

## 4. C2 — free of rank 2, so locality survives the split

A commutant element is $B = a\,\mathbb I + b\,\boldsymbol\sigma\cdot\tilde{\mathbf n}$ with
$a=\tfrac12\operatorname{tr}B$ manifestly Laurent but $b$ only manifestly **rational**. $b$ is
Laurent for every local $B$ exactly when the three Bloch components have no common factor: the
parallelism relations $b_i \tilde n_j = b_j \tilde n_i$ then force $b\in R$.

Checked (check C2): $\gcd(\tilde n_1,\tilde n_2,\tilde n_3) = \mathbf 1$, a **unit** of $R$.

> **VALUE CORRECTED 2026-08-13** (review, numbers table). This was published as $1+i$ in three
> places. $1+i$ is the `ZZ_I` *content* of the $\times 8w_1w_2w_3$-scaled representative — a sympy
> default-domain artifact. Over $\mathbb Q(i)$, which is the correct domain because $R$ has
> coefficients in a **field**, the gcd is $1$. Nothing was ever asserted *wrongly* — C2 tests
> unit-ness, not the value — but a wrong number was published, and C2's criterion has been
> corrected too: it now tests "is a monomial with nonzero coefficient", which is the actual
> definition of a unit of $R$. The old criterion (`free_symbols == set()`, i.e. "is a constant")
> would have reddened the 2D square lattice, whose gcd is $2w_3$ — a genuine unit.

Without this the two halves of the split could exchange non-local operators and the count would
be meaningless. It is the one step that could have failed quietly, which is why it is a check and
not a remark.

---

## 5. C3 — the scalar part is *exactly* the shifts

$\det:\mathcal C\to R$ is a homomorphism. An element with $b=0$ is $a\,\mathbb I$, and unitarity
forces $a\,a^*=1$, i.e. **$a$ is a unit of $R$**. The units of a Laurent ring over a field are
precisely the monomials $\zeta\,w^{\mathbf m}$. Hence

$$\{\,B\in\mathcal C : B \text{ scalar on the cell}\,\} \;=\; U(1)\times\mathbb Z^{3},$$

the shift lattice **and nothing else** (check C3). This is the half F291 asserted, now proved in
the forward direction: **no leftover translation is hiding in the commutant**.

> **NARROWED 2026-08-13** (review attack 1). This section originally added that "$d_\text{space}=3$
> is recovered from the commutant rather than imported into it." **That is circular and is
> withdrawn.** The $\mathbb Z^3$ here is the unit group of $R$, and $R$ has three variables because
> three Cayley generators were put in. The commutant proves *no extra* translations exist; it does
> not produce the number three. The three is F291's result and an input to this section.

---

## 6. C4 — the non-scalar part is a Pell group, and the update is its fundamental unit

On $\ker(\det)$ the unitarity conditions collapse to

$$a^2 - b^2 N \;=\; 1, \qquad N := \lVert\tilde{\mathbf n}\rVert^2 = 1-u^2, \qquad a,b\in R,$$

the **Pell equation** of the quadratic ring extension $R[X]/(X^2-N)$. Two hypotheses are checked
here rather than assumed:

**(a) $N$ is squarefree.** $N=(1-u)(1+u)$ with $1-u$ and $1+u$ each **irreducible** in $R$ and
distinct (check C4a, by explicit multivariate factorisation). So $R[\sqrt N]$ is a genuine
quadratic *field* extension. Had $N$ been a square the extension would **split** — and the honest
reading of that would be that the automaton is a direct sum of two automata, each with its own
clock, i.e. two universes rather than two times.

**(b) $A$ is the fundamental solution, with no search required.** The update is the pair
$(a,b)=(u,\,-i)$, and $b=-i$ is a **degree-zero constant** (check C4b). A nonzero Laurent
polynomial has degree $\ge 0$, so $\deg b = 0$ is minimal outright. The update is not merely *a*
time direction; it is the shortest one that exists.

The polynomial-Pell structure theorem — the solution group of a non-degenerate Pell equation is
generated by the fundamental solution — then gives

$$\boxed{\ \ker(\det) \;=\; \{\,\zeta\,A^{\,n} : n\in\mathbb Z\,\}, \qquad \text{rank } \mathbf 1. \ }$$

> **CITATION CORRECTED 2026-08-13** (review attack 3). This step was originally attributed to
> **Abel, *Crelle* 1 (1826) 185**. That is wrong: Abel 1826 is *Sur l'intégration de la formule
> différentielle* $\rho\,dx/\sqrt R$ and contains **no group-structure theorem**. It is the origin
> of the *equation*, not of the result used here. The correct sources are **Pastor, *Fundam. Prikl.
> Mat.* 7 (2001) 1123** and **Dubickas & Steuding, *Elem. Math.* 59 (2004) 133–143, Thm 2**, which
> also covers the several-variables case — so the theorem is *stronger* than what was cited, and
> in the polynomial case does not even need squarefreeness.

**The real import is not the theorem but a ring transfer, and that is the honest residual.**
Dubickas–Steuding runs on $k[x]$ with a **degree** satisfying "$\deg f=0\Rightarrow f$ constant".
That implication **fails** in $R=\mathbb C[w^{\pm}]$ — e.g. $\deg(1+w^{-1})=0$ but $1+w^{-1}$ is
not a unit. So the polynomial→Laurent transfer is a genuine gap, and it is what CL269 is
`contingent` on, replacing the previous (mis-stated) "Abel is imported".

> **CLOSED 2026-08-13 by F316 — this finding now imports nothing.** The route named here was
> taken. `findings/F316-laurent-pell-descent-proved.md` proves the descent over the Laurent ring
> from scratch: the two-sided width $D(f)=h_f(\lambda)+h_f(-\lambda)$ against a
> $\mathbb Q$-independent $\lambda$ is additive under multiplication and satisfies
> $D(f)=0\iff f$ monomial $\iff f$ a unit of $R$ — the exact replacement for the failing
> "$\deg 0\Rightarrow$ constant". The extra ingredient, which the polynomial proof neither has nor
> needs, is that **unitarity** forces $a^*=a$ and $b^*=-b$ and hence centrally symmetric Newton
> polytopes. Then $b'b''=1+b^2$ with $D(1+b^2)\le2D(b)$, and since the non-cancelling branch has
> $D(b'')=D(b)+2c$, the other satisfies $D(b')\le D(b)-2c$: **strict descent, measured to be by
> exactly $2c$ every step**, landing on $\{\pm1,\pm A^{\pm1}\}$ because $u$ has eight monomials and
> so is not a difference of two.
>
> **Scope, as F316 states it:** this is proved for *this* $N$ under unitarity. It is not a
> re-proof of Dubickas–Steuding in several variables, and F316 says so rather than implying
> otherwise. CL269 is no longer `contingent` on an import.

§7 exercises the theorem's *mechanism* regardless of which paper it is attributed to.

---

## 7. C5 — the tower and the descent, exercised

Running the group is the closest this finding can get to verifying what it cites, so it is run
(checks C5a–C5c, all exact over $\mathbb Q(i)$, $n\le8$):

| leg | result |
|---|---|
| the tower | $A^{n} = \bigl(T_n(u),\ -i\,U_{n-1}(u)\bigr)$ **exactly**, Chebyshev $T$ and $U$ |
| degree growth | $\deg b(A^{n}) = n-1$ exactly — one lattice step per tick, no plateau |
| descent | multiplying by $A^{-1}$ lowers $\deg b$ by exactly one, strictly, reaching $\mathbb I$ in exactly $n$ steps |
| order | $A^{n}$ is **never** a monomial times $\mathbb I$ ⇒ $\langle A\rangle\cong\mathbb Z$ |

The last row is worth its own sentence. A finite-order update would make the model's time a cyclic
clock $\mathbb Z_n$; a power of $A$ equal to a shift would make the time direction *become* a space
direction after $n$ ticks — which is precisely the collapse F291 §6 gestured at without excluding.
Neither happens, and that is measured.

---

## 8. The count — WITHDRAWN as stated, and what survives

> **WITHDRAWN 2026-08-13** by [the independent review](../docs/reviews/F313-review-2026-08-13.md),
> attack 5 (`FAIL` — numerology). The original §8 boxed an identity
> $(d_\text{space},d_\text{time})=(\dim\mathfrak{su}(s),\operatorname{rank}\mathfrak{su}(s))$ and
> called it "the substantive change". It is not a derivation. It is retracted here, in place, per
> D12 — the finding records what a session concluded, and this is the correction to it.

**Why it was wrong.** The identity merges two functions that agree **only at $s=2$**. The model's
actual spatial bound is F291's Clifford count $2\log_2 s+1$, while $\dim\mathfrak{su}(s)=s^2-1$:

| $s$ | F291's bound $2\log_2 s+1$ | $\dim\mathfrak{su}(s)=s^2-1$ | agree? |
|---:|---:|---:|---|
| 2 | 3 | 3 | yes |
| 4 | **5** | **15** | **no** |

The model's *own* $s=4$ cell contradicts it. Worse, the reviewer's look-elsewhere count is
decisive: $\{s^2-1,\ 2s-1,\ s+1,\ 2\log_2 s+1,\ 2^s-1\}$ all give 3 at $s=2$ and
$\{s-1,\ \log_2 s,\ s/2,\ s^2-3,\ 2^{s-1}-1\}$ all give 1, so **at least 25 equally natural pairs
land on $(3,1)$**. This is exactly what CLAUDE.md's constants rule forbids — *"values that coincide
stay separate constants… merging any of them turns a prediction into an input"* — applied to
functions instead of numbers. The module's own guard was vacuous too: `space_is_dim_su2_at_s2`
returned `True` at $s=4$ and $s=8$.

**What survives, and it is still the point of the finding.** Two separate statements, not one:

$$d_\text{time} = 1 \ \text{ at } s=2 \quad\text{(§§3–7, this finding)}, \qquad
d_\text{space} \le 2\log_2 s + 1 = 3 \ \text{ at } s=2 \quad\text{(F291 S1)}.$$

Both take $s=2$ as input, so it remains true that **the same premise feeds both halves of A1** —
that much of the original claim stands. What does **not** stand is that either is an instance of
one formula in $s$, or that $d_\text{time}=s-1$ holds for $s>2$. The $s$-general rank claim is
**unestablished**: at $s=4$ the candidate answers are 1, 2 and $\operatorname{rank}
\mathfrak{su}(4)=3$, and the finding measured **2** (§9), which the withdrawn identity predicted
to be 3.

The qualitative reading is unaffected and is worth keeping: **anticommuting** generators build the
Cayley graph while **commuting** ones build the flow. That is a description of the mechanism, not
a formula, and it should never have been dressed as one.

---

## 9. The residual, measured rather than argued

The theorem is sharp at $s=2$ and it is sharp *because* $s=2$. At $s=4$ the model's own massive
Dirac walk (Paper 1 Eq. 23, `particles.dirac_bcc`)

$$D = \begin{pmatrix} n A & i m\,\mathbb I \\ i m\,\mathbb I & n A^{\dagger}\end{pmatrix},
\qquad n^2+m^2=1$$

has eigenvalues $e^{\pm i\Omega}$ each **twice** degenerate, pointwise commutant dimension **8**,
and

$$V \;:=\; \mathbb I_\text{branch}\otimes A$$

commutes with $D$ — at every mass, not only at $m=0$ (measured: $\lVert[V,D]\rVert \le
2.2\times10^{-16}$ at $m=0,\,0.37,\,0.8$) — with a dispersion independent of $D$'s. So a **free
composite cell carries a second dispersive commuting flow**, and the rank-1 count does not survive
to $s=4$ on its own.

Two things are true about that, and both are recorded rather than one being chosen:

1. **$V$ is the $s=2$ update lifted branch-blind.** It is the fundamental clock standing beside its
   mass-dressed self, not a new one. The composite has not acquired a second time so much as
   displayed the fundamental one twice.
2. **The honest form of the caveat** is that C1's "no room" is a property of the **minimal** cell.
   A free theory is integrable and its commutant is large; only at $s=2$ is the cell too small to
   hold an extra flow. Whether $V$ survives interaction is **not settled here** — falsifier 5.

Since $s=2$ is founding decision 6 / BDPT minimality — the same $s=2$ F291's S1 already leans on —
this rests on no *new* input. It does rest on that one, and F291's boundary ("losing S3 *and*
$s=2$ together would reopen the question") is inherited verbatim.

---

## 10. What this closes, and what it does not

**Closes.** For an $s=2$ QCA on an **infinite** $\Lambda\cong\mathbb Z^3$ Cayley graph, the
Cayley-graph/update split named in F291 §7 is no longer a choice: it is the $\det$-splitting of the
update's own commutant, with $U(1)\times\mathbb Z^3$ on one side (*exactly* the shifts — no extra
translation hides there) and $\mathbb Z$ on the other (*exactly* the powers of the update, which is
**primitive**: there is no local "half tick"). $d_\text{time}=1$ is derived, from the same $s=2$
that F291's spatial bound uses.

**Does not close.**

- ~~The polynomial→Laurent transfer of Dubickas–Steuding Thm 2 (§6).~~ **CLOSED 2026-08-13 by
  F316** — proved in-repo. This finding's chain now has no import.
- **Infinite volume and the three Cayley generators are inputs**, not outputs (§2).
- **$d_\text{space}=3$ is F291's result, not this one** (§5).
- **Any $s$-general rank formula** (§8, withdrawn).
- **The composite cell** (§9) — **now settled by F315**: $V$ does not survive interaction, so the
  second flow is an artifact of freeness.
- **The arrow.** $\langle A\rangle\cong\mathbb Z$ has two generators, $A$ and $A^{-1}$. This
  derives that time is one-dimensional and infinite; it says nothing about a preferred direction.
  That is rubric row **A4**'s thin T and stays there — this finding does not touch it.

**Rubric consequence.** A1's residual should read *"$s=2$ minimal cell; infinite volume; the
Laurent transfer"* instead of *"the '+1'"*. The row's stated reason for not being `EXACT` — "the
'+1' is by construction" — is what has changed. Whether that moves the grade is a completeness-run
decision, and after the 2026-08-13 review the honest grade for this finding's own class is
**derived-with-named-import**, one below `exact`.

---

## 11. Falsifiers

1. **Exhibit a local homogeneous unitary commuting with $A$ that is scalar on the cell and is not a
   monomial.** §5 dies and the shift lattice is not the whole translation group.
2. **Exhibit a Pell solution $(a,b)$ with $b\ne0$ that is not $\zeta A^{n}$.** §6 dies — the time
   rank is $\ge2$ and the model has two times. Equivalently: show $\deg b$ fails to descend.
3. **Show $N=1-u^2$ is a square in $R$.** The extension splits and the automaton is a direct sum —
   two automata, not one spacetime.
4. **Exhibit $n\ne0$ with $A^{n}=\zeta\,w^{\mathbf m}\mathbb I$.** Time closes into a finite clock
   and the time direction is a space direction after $n$ ticks.
5. **Show $V=\mathbb I\otimes A$ survives the model's interactions** — gauge coupling (F68 minimal
   coupling), or the F86 colour dielectric — as a local homogeneous symmetry of the *interacting*
   walk. Then the second dispersive flow is physical and §9's reading ("the fundamental clock
   twice") is wrong. Conversely, showing it does **not** survive would upgrade §9 from residual to
   result.
6. **A cell with $s\ne2$.** *(Restated 2026-08-13 — the original form invoked $d_\text{time}=s-1$,
   which §8 withdrew.)* The $s=2$ premise is shared with F291's spatial bound, so evidence for a
   larger fundamental cell attacks both halves of A1 at once. What it would **not** do is hand back
   a predicted $d_\text{time}$: no $s$-general rank formula is established here, and the model's own
   $s=4$ cell measured **2**, not $\operatorname{rank}\mathfrak{su}(4)=3$.
7. **Measure $d_\text{time}$ at $s=4$ properly** (review's addition). 1, 2 and 3 are three
   different answers and only 2 has been measured, on the *free* walk. With F315 showing the extra
   flow does not survive interaction, the interacting answer is plausibly 1 — but it is not
   computed.
8. **Break the infinite-volume premise.** At what finite $L$, if any, does a rank $>1$ commutant
   appear, and is the infinite-volume limit approached smoothly or is it a discontinuity? A
   computation, not an appeal.
9. ~~Prove or refute the polynomial→Laurent transfer.~~ **DONE — F316, 2026-08-13.** It goes
   through, and CL269's contingency is gone. The live successors are F316's own falsifiers, of
   which the sharpest is: exhibit $f$ with $D(f)=0$ that is not a monomial.

---

## 12. Provenance

- Module: `src/casim/engine/lattice/time_signature.py` (`lattice` sector, `exactness=exact`,
  registered in `_SPINE`, D11). Exact Laurent arithmetic over $\mathbb Q(i)$ is hand-rolled in the
  module — sympy's multivariate `expand` on $A^{8}$ exhausts the sandbox, and CLAUDE.md's standing
  caution about library behaviour on chiral/complex objects applies. No numpy, no scipy, no FFT.
- Test record: `F313-time-signature`, `kind: assertion`, `tier: gate`, entry `check_all`, 11/11
  PASS, with **three declared controls** (`pell_nmax=1`, `cell_dim=4`, `fake_gcd=True`), each
  verified RED. The load-bearing legs are re-derived in the test independently of the module: the
  Bloch vector is re-typed from `references/qca-papers-1-4-overview.md` Eq. 15 rather than
  imported, and the commutant is solved with sympy from that re-typed form.
- Runner: `tests/runners/run_f313_time_signature.py` → `test-results/F313_time_signature.json`.
- Claim card: **CL269**.
- Reads: F291 (§6, §7 — the residual this attacks; S1's $s=2$ and its route (b)), F292 (reducible
  cells), F26 ($c_\text{lat}=d\Omega/d\lvert k\rvert$ as a single number), F27 (the mass phase),
  F290 (the strict causal cone), F289 (the precedent for a named imported step). Founding
  decisions 1, 2, 5, 6 in `CLAUDE.md`.
- **Supersedes nothing.** F291 §6 is **narrowed, not withdrawn**: its conclusion (one time) stands
  and its grade (`structural`) is what moves. F291's own text is left bit-unchanged, per the
  finding/claim split (D12) — the object that moves is CL269, not F291.
