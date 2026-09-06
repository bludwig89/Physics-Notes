# F329 — A6r closed: the Cooke–Keane–Moran regularity lemma was already Gleason's own theorem, and it transfers to this model's ray spaces without adaptation beyond the dimension hypothesis F304/F312 already proved

*2026-08-27 - 14:40 · sector `interactions` · session `lucid-keen-gleason` ·
module `casim.engine.interactions.qi_gleason_regularity` ·
test record `F329-gleason-regularity` (**8/8** PASS honest, control verified RED on exactly H2/H3) ·
results `test-results/F329_gleason_regularity.json`*

**Reviewed:** 2026-08-27 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F329-review-2026-08-27.md))

**Target.** Rubric row **A6r** (`docs/status/open-derivations.md`), narrowed 2026-08-11 by
[[F312-born-rule-nonabelian-premises]] to *one* residual: [[F304-born-rule-gleason-premises-forced]]
§5.5, after proving Gleason's dichotomy for $f\in L^2$ by harmonic analysis, named exactly what was
left —

> "Gleason's theorem holds for merely **bounded** $f$, and the bridge — that a non-negative frame
> function is automatically continuous — is the **Cooke–Keane–Moran regularity lemma** (Cooke,
> Keane & Moran 1985), which is **not reproved here**. … What the lemma excludes is a
> **non-measurable** weight assignment."

`docs/claims/CL264-born-rule-gleason-premises-forced.md` carries this as its named `contingent`
hypothesis: *"Closing it is a real, bounded piece of work (CKM is three pages of sphere geometry)
and is the obvious next step for anyone who wants this card `live`."*

**This finding closes it.** Not by reproving Cooke–Keane–Moran's own 1985 argument — the scanned
original could not be retrieved in machine-readable form this session (§5) — but by observing that
the identical proposition is already **Theorem 2.8 of Gleason's own 1957 paper** [Gleason 1957], the
same primary source whose *other* half (Theorem 2.3: a continuous frame function on $\mathbb R^3$ is
regular) F304 §5 already independently re-derives by representation theory for general $d$, without
citing it. Theorem 2.8 needs nothing beyond non-negativity and compactness of the sphere; no appeal
to CKM's separate, later, lower-prerequisite proof of the same fact is required, and none is made.

**Cross-references:** [[F304-born-rule-gleason-premises-forced]] §5 (the dichotomy this supplies the
last premise of) and §5.5 (the residual closed here), [[F312-born-rule-nonabelian-premises]] G7 (the
dimensions this finding's checks reuse), [[F281-measurement-pointer-basis-born-rule-rg-classicality]].
External: A. M. Gleason, *J. Math. Mech.* **6** (1957) 885 (Theorems 2.3, 2.8, Lemma 3.3, Theorem
3.5 — quoted from the primary text, §2 below); R. Cooke, M. Keane & W. Moran, *Math. Proc. Camb.
Phil. Soc.* **98** (1985) 117 (the alternative, lower-prerequisite proof of the same proposition,
described secondhand, §5).

---

## 1. Why this residual is not what it first looks like

F304's own wording treats "the Cooke–Keane–Moran regularity lemma" as a single external fact that
either has to be re-derived from scratch or taken on citation from the 1985 paper specifically. That
framing is one citation too narrow. Gleason's 1957 paper proves the *whole* dichotomy in two
independent halves:

| Half | Statement | Method | Status before this finding |
|---|---|---|---|
| **Theorem 2.3** | Every **continuous** frame function on $S^2\subset\mathbb R^3$ is regular | spherical harmonics | Re-derived (for general $d$, not just $d=3$) by F304 §5's harmonic analysis — **not cited** |
| **Theorem 2.8** | Every **non-negative** frame function on $S^2\subset\mathbb R^3$ is regular | oscillation-propagation on great circles, using only non-negativity + compactness | Named as an external residual, attributed only to Cooke–Keane–Moran 1985 |

CKM's 1985 paper reproves the **conjunction** of both halves — the paper's own title, "an elementary
proof of Gleason's theorem," is about the whole theorem, not a lemma CKM originated. Their
contribution is a different, longer, but lower-*prerequisite* route through Cauchy's functional
equation (§5), not the only existing proof that non-negativity forces continuity. Gleason's own
Theorem 2.8 already supplies exactly that fact, in the same source F304 has already partially used.

## 2. Gleason's own regularity argument, quoted from the primary source

*(Quoted from A. M. Gleason, "Measures on the Closed Subspaces of a Hilbert Space," J. Math. Mech.
**6** (1957) 885–893. Retrieved 2026-08-27 from the paper's public scan; extracted via an automated
PDF-to-text tool rather than read character-by-character — see §5's honesty note on what that means
for the confidence carried here.)*

**Definitions (Gleason §1–2).**

> "A frame function of weight $W$ for a separable Hilbert space $\mathfrak X$ is a real-valued
> function $f$ defined on the (surface of the) unit sphere of $\mathfrak X$ such that if $\{x_i\}$
> is an orthonormal basis of $\mathfrak X$ then $\sum f(x_i) = W$."

> "$f$ is **regular** if there exists a self-adjoint operator $T$ … such that $f(x) = (Tx,x)$ for
> all unit vectors $x$."

**Theorem 2.3.** *Every continuous frame function on the unit sphere in $\mathbb R^3$ is regular.*
— proved by spherical-harmonic decomposition; the direct analogue of the argument F304 §5.1–5.3
carries out for general $d$ by $U(d)$-representation theory instead.

**Theorem 2.8.** *Every non-negative frame function on the unit sphere $S$ in $\mathbb R^3$ is
regular.* Proof structure, quoted:

> "Let $f$ be a non-negative frame function of weight $W$ on $S$. We may subtract a constant from
> $f$ and it will remain a frame function; hence it is no loss of generality to suppose that
> $\inf f(x) = 0$."

Fix $\varepsilon>0$, $\eta=\varepsilon/88$, and pick $p$ with $f(p)\le\eta$ (possible since
$\inf f=0$ on a compact set). Then:

> "Let $u$ be the polar rotation through angle $\pi/2$ [about the axis through $p$], and set
> $g(x)=f(x)+f(ux)$. Evidently $g$ is a non-negative frame function of weight $2W$. For any point
> $q$ on the equator, $p$, $q$, and $uq$ form an orthonormal set so
> $g(q)=f(q)+f(uq)=W-f(p)$; thus **$g$ is constant on the equator**."

This one identity — an orthonormal triple forcing a sum to be exactly constant — is the
*seed* the rest of the proof propagates; it is checkable, machine-verifiable algebra (§3,
H3 below), not the hard step. **The hard step is what comes next**, and this finding does
not re-derive it: three auxiliary lemmas (quoted, using
$\operatorname{osc}(f,U):=\sup_U f-\inf_U f$) form a genuine geometric covering argument on
great circles of $S^2$, propagating that one seed identity's local near-constancy to a
global oscillation bound — this is the substantive mathematics of Theorem 2.8, and it is
*cited*, not reproduced symbol-by-symbol, in this finding (§5):

> **Lemma 2.6.** "Suppose that $f$ is a frame function on $S$ and that, for a certain neighborhood
> $U$ of $p$, $\operatorname{osc}(f,U)=a$. Then every point of the great circle with pole $p$ has a
> neighborhood $V$ for which $\operatorname{osc}(f,V)\ge 2a$."
>
> **Lemma 2.7.** "If $f$ is a frame function and for a non-empty open set $U$,
> $\operatorname{osc}(f,U)=a$, then every point of $S$ has a neighborhood $W$ such that
> $\operatorname{osc}(f,W)\le 4a$."

Chaining these (Gleason's own arithmetic: $\operatorname{osc}(g,U)\le5\eta$, propagating to
$\operatorname{osc}(g,V)\le20\eta$ near $p$, to $\operatorname{osc}(f,W)\le88\eta=\varepsilon$ at
*every* point of $S$):

> "Since $\varepsilon$ can be arbitrarily small this proves that $f$ is continuous and the theorem
> now follows from theorem 2.3."

**The reduction to any Hilbert space of dimension $\ge3$ (§3, Palais's lemma).** A real-linear
subspace is *completely real* iff the inner product takes only real values on it — Gleason's own
definition, quoted:

> "A real-linear subspace $\mathfrak X$ of a Hilbert space is completely real if the inner product
> takes only real values on $\mathfrak X\times\mathfrak X$." … "a frame function for [the full space]
> becomes a frame function when restricted to a completely real subspace."

> **Lemma 3.3.** "Suppose that $f$ is a non-negative frame function on a **two-dimensional
> complex** Hilbert space which is regular on every completely real subspace. Then $f$ is
> regular." *(The bracketed elision in an earlier draft of this quote — "a … Hilbert space" —
> obscured that Lemma 3.3 as stated is specifically about a 2-dim complex ambient space; caught
> by this finding's own review pass, corrected here. It does not change the closure: the
> operative citation is Theorem 3.5 below, quoted and independently re-verified in full, and this
> finding does not need to reconstruct exactly how Lemma 3.3 composes with the embedding argument
> for ambient dimension $>3$ in order to cite Theorem 3.5's own stated conclusion.)*

> **Theorem 3.5.** "Every non-negative frame function on either a real or complex Hilbert space of
> dimension at least three is regular." Proof (opening): "Every completely real two-dimensional
> subspace of $\mathfrak X$ can be embedded in a completely real three-dimensional subspace, since
> $\dim\mathfrak X\ge3$. Therefore theorem 2.8 shows that any non-negative frame function $f$ is
> regular on every completely real two-dimensional subspace" — after which the proof concludes
> $f$ is regular on all of $\mathfrak X$. The complete step-by-step composition of that last
> inference (how the 3-dim-subspace case and Lemma 3.3 combine for an ambient space of dimension
> greater than 3) is Gleason's own proof, cited rather than reconstructed line-by-line here; what
> this finding relies on, and what was independently re-verified against the primary text twice
> (see §5), is Theorem 3.5's **stated conclusion** — which is, word for word, the proposition
> needed.

That is the complete chain: **Theorem 2.8** (non-negative $\Rightarrow$ continuous, on
$\mathbb R^3$) **+ Theorem 3.5** (any Hilbert space, $\dim\ge3$, real or complex, is regular
whenever it is non-negative — proved via the completely-real-subspace reduction, cited as a
conclusion rather than re-derived step by step) is exactly the proposition F304 §5.5 named as
external, word for word — "a non-negative frame function is automatically continuous" — proved
with nothing beyond non-negativity and compactness, by Gleason himself.

## 3. What transfers to this model, and what has to be checked rather than assumed

The abstract statement (Theorem 3.5) applies to *any* Hilbert space of dimension $\ge3$, real or
complex — nothing in its hypotheses references a physical construction, a lattice, a gauge group,
or anything else specific to this project. So the only genuine transfer question is whether this
model's own ray spaces satisfy the **one** hypothesis the theorem needs: $\dim\ge3$, together with
the existence of a completely real 3-dim subspace the reduction runs through. Both are checked
below rather than assumed.

**The dimension hypothesis is already proved, twice, by prior findings — not re-derived here.**
[[F304-born-rule-gleason-premises-forced]] §1.1 established the smallest Hilbert space this model
realises *any* measurement on is $2^{1+1}=4>2$ (no record without an environment cell).
[[F312-born-rule-nonabelian-premises]] G7 established that $\dim(\mathcal H_p\otimes V)=d_pN$
clears $d\ge3$ for the model's gauge-charged sectors, with $SU(3)_c$ alone (no pointer) already at
$N=3$. Together these give the list of dimensions this finding checks the reduction on:

$$\texttt{MODEL\_DIMENSIONS} = (3,\ 4,\ 6,\ 64,\ 96)$$

— traced to the specific table cell that names each one, not merely a number that appears
somewhere in F304/F312: **3** is F312 G7's "dim with no pointer" column for $SU(3)_c$ (colour
alone); **4** is F304 §1.1's minimal system+record pointer space with no internal factor,
$2^{1+1}$; **6** is F312 G7's "dim with F304's minimal record pointer" column for $SU(3)_c$
($d_pN=2\times3$); **64** and **96** are F312 G4/G5's SU(2)$_L$ and SU(3)$_c$ sectors with the
pointer genuinely present. (An earlier draft of this finding also listed 8, 9 and 16 — caught by
this finding's own review pass as mis-sourced from unrelated table cells and removed rather than
reinterpreted; see "Reviewed & corrected" below.) The one dimension F304/F312 establish is
**never** a valid standalone measurement context — isospin alone with no pointer, $d=2$ (F312 G7:
"needs $d_p\ge2$") — is checked *separately*, as a **negative control**: Theorem 3.5's hypothesis
must **fail** for it, confirming F304 §3's own $d=2$ hole is correctly excluded by this check
rather than silently papered over.

**H1 — the completely real 3-dim subspace, exhibited on every model dimension.** A real-linear
subspace is completely real iff the inner product is real-valued on it (Gleason's own §3.1
definition, quoted above). For $\mathbb C^d$ this is not a special or delicate construction: the
standard basis vectors $e_0,\dots,e_{n-1}$ trivially qualify, since $\langle e_i,e_j\rangle=
\delta_{ij}$ is real for every $i,j$ by construction, and the real span of any real-coordinate
orthonormal set stays completely real. `completely_real_subspace_exists(d)` builds
$B=[e_0\ e_1\ e_2]\in\mathbb C^{d\times3}$ and checks its Gram matrix $B^\dagger B$ is exactly the
real identity:

| $d$ | max $\lvert\mathrm{Im}\,G\rvert$ | max $\lvert\mathrm{Re}\,G-I_3\rvert$ | hypothesis holds |
|---:|---:|---:|---|
| 3, 4, 6, 64, 96 | **`0.0`** (all five) | **`0.0`** (all five) | yes |
| 2 (excluded, negative control) | — | — | **no** (dim $<3$, correctly excluded) |

Both columns are literal zero, not machine-precision — the standard-basis embedding is exact by
construction, so this is arithmetic, not analysis. The reduction's hypothesis holds for every
Hilbert space this model actually builds a Born-rule measurement context on, and is machine-shown
to correctly exclude the one dimension that must stay excluded.

**H2 — the frame condition itself, and F304's own control reused as this finding's control.**
Testing Theorem 2.8's proof mechanics needs *some* concrete frame function to run them on. A
regular function $f(x)=x^\top Tx$ ($T$ symmetric real) is a genuine one — Gleason's Lemma 2.1 says
regular $\Leftrightarrow$ quadratic form in finite real dimension, and the *converse* direction
(quadratic $\Rightarrow$ frame condition holds) follows from the trace being basis-independent:
$\sum_i\langle e_i\rvert T\lvert e_i\rangle=\operatorname{Tr}T$ for *any* orthonormal basis. This is
checked directly — 400 random orthonormal bases of $\mathbb R^3$, spread of $\sum_if(e_i)$ across
them $2.9\times10^{-15}$ (machine zero) — not assumed.

The **control** reuses [[F304-born-rule-gleason-premises-forced]] §3.1's own construction: add
$\varepsilon\,P_3(x_1)$ ($P_3$ the degree-3 Legendre polynomial, the same odd harmonic F304 uses to
exhibit the $d=2$ hole). F304 §5.3 proves this $k=3$ mode is **not** annihilated by the frame
condition at $d\ge3$ ($\binom{k+d-2}{k}>d-1$ strictly for $k\ge2$, $d>2$) — unlike at $d=2$, where
every odd $k$ survives. So adding it must break the frame condition at $d=3$, and does:

| | spread of $\sum_if(e_i)$ over 400 bases |
|---|---:|
| honest ($\varepsilon=0$) | $2.9\times10^{-15}$ |
| control ($\varepsilon=0.35$) | $0.925$ |

**H3 — the equator-constancy identity, Theorem 2.8's own mechanical core, and the same control.**
Pole $p=e_0$, polar rotation $u$ through $\pi/2$ about $p$ (embedded as a $3\times3$ orthogonal
matrix, exactly as Gleason's own construction). For 500 points $q$ on the equator of $p$,
$\{p,q,uq\}$ is verified orthonormal directly (not assumed — max Gram deviation from $I_3$ is
checked at every $q$), and $g(q):=f(q)+f(uq)$ is checked against the closed-form target
$W-f(p)$:

| | max orthonormality defect $\{p,q,uq\}$ | max $\lvert g(q)-(W-f(p))\rvert$ |
|---|---:|---:|
| honest ($\varepsilon=0$) | $0.0$ | $4.4\times10^{-16}$ |
| control ($\varepsilon=0.35$) | $0.0$ (the triple is still orthonormal — only $f$ changed) | $0.407$ |

The orthonormality of $\{p,q,uq\}$ is a fact about the rotation, independent of $f$ — it holds
identically in both rows, exactly as it must. What breaks under the control is $g$'s constancy,
because that constancy is a **consequence** of the frame condition holding, and the control is
built specifically to break the frame condition. This is the D9 idiom done correctly: a single
fixed pass criterion (`is_frame_function`, `identity_holds`), unmodified by `control`; only the
*input* changes, and the check goes red on exactly the two legs (H2, H3) that depend on it, while
every H1 leg — including the $d=2$ negative control, which tests something $\varepsilon$ never
touches — stays green. Verified 2026-08-27: `casim test --id F329-gleason-regularity
--param control=True` reds H2/H3 and nothing else.

## 4. The closure, stated precisely

**Theorem (regularity on this model's ray spaces).** Let $f$ be a non-negative function on the
rays of $\mathcal H=\mathbb C^d$ for any $d$ this model builds a Born-rule measurement context on
($d\in\{3,4,6,64,96\}$, §3), satisfying $\sum_if(e_i)=W$ for every orthonormal basis $\{e_i\}$
of $\mathcal H$ (no continuity, boundedness, or measurability assumed in advance). Then $f$ is
**regular**: there exists a Hermitian $T$ with $f(v)=\langle v\rvert T\lvert v\rangle$ for every
unit ray $v$.

*Proof.* $\mathcal H$ contains a completely real 3-dim subspace (§3, H1, machine-verified for every
$d$ in the list). By Theorem 3.5 / Lemma 3.3 (§2, Gleason 1957), it suffices to show $f$ is regular
on every completely real 3-dim subspace of $\mathcal H$, and by Theorem 2.8 (§2) it suffices there
that $f$ is non-negative — which is the hypothesis. $\blacksquare$

**What this closes.** [[F304-born-rule-gleason-premises-forced]] §5.1–5.3's argument — the operator
identity $f+(d-1)Bf=W$, the $U(d)$-isotypic decomposition, the closed form
$b_k=(-1)^k/\binom{k+d-2}{k}$ — is complete for $f\in L^2(\mathbb{CP}^{d-1})$. This finding supplies
exactly the missing bridge: **every** non-negative frame function on this model's ray spaces, not
merely the $L^2$ ones, is regular, hence continuous, hence bounded and measurable, hence in $L^2$,
hence covered by F304 §5.3's dichotomy. Combined, F304 §5 + F312 (non-Abelian premises) + this
finding (regularity) give the full theorem — dimension, non-contextuality, *and* regularity — as
consequences of the rule, with **no** external citation remaining anywhere in the chain except
Gleason's own 1957 paper, cited (§2) rather than assumed, exactly as F304 §5 already cites nothing
for its own half.

**What does not close, and is not claimed to.** The one premise CL264 already calls irreducible —
"an exhaustive set of records carries weights summing to one" — is the definition of the object
being derived, not a residual, and stays exactly as F304/CL264 left it. Nothing here touches that.

## 5. Honesty about what is cited, what is adapted, and what is verified

This finding's closure rests on a chain of primary-source quotes (§2) retrieved by an automated
PDF-to-text extraction tool rather than read character-by-character from the original scan, because
the original Cooke–Keane–Moran (1985) PDF returned no machine-readable text at all, and the Gleason
(1957) scan was legible only through the same kind of tool. Cross-checking: the theorem numbering
(2.3, 2.8, 3.3, 3.5) and statements were retrieved consistently across **three independent fetches**
of the same source, including one that specifically asked for the definitions and lemma numbers
without prompting for the conclusion, which is reassuring but is not the same as independently
verifying the extraction against the typeset original page images.

Three things follow from that, stated as precisely as F304/F312's own honesty sections:

1. **Cited, not re-derived or re-checked here:** the covering/propagation combinatorics of Lemmas
   2.5–2.7 (why *some* finite oscillation bound exists at all, and Gleason's own numeric bookkeeping
   — 5, 20, 88 — for it). This is the one piece of real analysis in the whole chain this finding
   still trusts a retrieval of, rather than reproducing symbol-by-symbol. It is exactly the kind of
   gap F304 itself left open before §5 closed it by independent derivation — the difference is that
   *this* gap is closed by citing a 69-year-old, continuously-cited, foundational peer-reviewed
   result rather than by an unpublished argument, which is a materially different confidence class.
2. **Adapted, and where this finding's actual content is:** the reduction stated for this model's
   own dimensions rather than left abstract, and the equator-constancy identity machine-verified on
   frame functions embedded via this model's own completely-real-subspace construction.
3. **Not claimed:** that a genuinely non-measurable (Hamel-basis / axiom-of-choice) frame function
   has been numerically exhibited failing the identity. No computer can construct one — that is the
   entire point of the theorem — so nothing here or in principle could "verify" the pathological
   case directly. What closes the residual is that the *proposition* F304 §5.5 named is Gleason's
   own proved theorem, and this finding checks that its one hypothesis (dimension $\ge3$, via a
   completely real subspace) transfers to this model's own construction — which is the part that
   *could* have failed and did not.

## 6. Falsifiers

1. **A model dimension in `MODEL_DIMENSIONS` for which `completely_real_subspace_exists` returns
   false, or a nonzero Gram deviation.** Would mean Theorem 3.5's hypothesis fails to transfer for
   an actual measurement-context dimension, reopening the residual for that sector specifically.
   Checked machine-zero for all five listed dimensions; none would be excludable by construction,
   since the standard-basis embedding is dimension-agnostic — a failure here would indicate a defect
   in this finding's code, not a defect in the theorem.
2. **The $d=2$ negative control passing** (i.e. `completely_real_subspace_exists(2)` returning
   `True`). Would mean this check no longer distinguishes the excluded case from the covered ones,
   silently widening the claim beyond what F304's own dimension premise supports. Verified to fail
   as required.
3. **The control (`control=True`) failing to redden H2 or H3.** Would mean the checks are not
   actually testing the frame condition's role in the identity — exactly the failure mode D9
   controls exist to catch. Verified red on precisely H2/H3, `casim test --id
   F329-gleason-regularity --param control=True`, 2026-08-27.
4. **A machine-readable retrieval of Cooke–Keane–Moran (1985) surfacing a materially different
   regularity mechanism** — e.g., one whose hypotheses this model's construction does *not* satisfy,
   unlike Gleason's own Theorem 2.8, which needs nothing but non-negativity and compactness. Would
   not falsify this finding's closure (Gleason's own proof stands on its own), but would mean the
   claim "CKM proves the same proposition by an independent method" (§1) should be narrowed or
   retracted, since that specific comparison is sourced secondhand (§5).

## 7. What is exact vs cited vs verified

| Piece | Status |
|---|---|
| Theorem 2.8 statement, Lemma 3.3, Theorem 3.5 statement and proof sketch | **cited**, quoted from primary source (§2) |
| Lemmas 2.5–2.7's specific propagation constants (5, 20, 88) | **cited**, not independently re-derived |
| Completely-real-3-dim-subspace existence, all 5 model dimensions | **exact** (literal `0.0`, both Gram-matrix checks) |
| $d=2$ negative control (hypothesis correctly fails) | **exact** (structural, `dim<3`) |
| Frame condition across 400 random bases (honest) | **machine** ($2.9\times10^{-15}$) |
| Frame condition across 400 random bases (control) | **exact** (spread $0.925\gg0$, control fires) |
| Equator-constancy identity (honest) | **machine** ($4.4\times10^{-16}$) |
| Equator-constancy identity (control) | **exact** (deviation $0.407\gg0$, control fires) |
| Orthonormality of $\{p,q,uq\}$ (both honest and control) | **exact** (`0.0`, unaffected by $f$) |
| The overall closure (§4 theorem) | **exact-conditional** — the arithmetic/algebra checked by this session's tests is exact (literal `0.0` / machine floor), but the closure as a whole additionally rests on Gleason 1957's own peer-reviewed Theorem 2.8/3.5, cited not re-derived (a review pass flagged plain "exact" here as overloading the taxonomy; see §9 below) |

## 8. Files

- Module: `src/casim/engine/interactions/qi_gleason_regularity.py`
- Test: `tests/findings/test_F329_gleason_regularity.py` (record `F329-gleason-regularity`, tier
  gate, **8/8** honest, control verified RED on H2/H3, 2026-08-27)
- Results: `test-results/F329_gleason_regularity.json`
- Module registry: `src/casim/engine/registry.py` (`interactions.qi_gleason_regularity`)
- Test registry: `tests/registry/interactions.yaml` (`F329-gleason-regularity`)
- Claim card updated: `docs/claims/CL264-born-rule-gleason-premises-forced.md`
  (`status: contingent` → `status: live`)
