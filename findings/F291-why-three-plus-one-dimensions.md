# F291 — Why 3+1: two independent selectors already fix $d=3$; only the "+1" is by construction

*2026-08-02 - 16:20 · sector `lattice` · module `casim.engine.lattice.dimensionality` ·
test record `F291-dimension-selectors` (9/9 PASS, gate tier) ·
results `test-results/F291_dimension_selectors.json`*

**Target.** `docs/status/completeness-2026-08-02.md` rubric row **A1** — the first entry of
the ABSENT table:

> *A1 · Why 3+1 spacetime dimensions — the BDPT uniqueness theorem forces the Weyl walk
> **given** 3D; nothing selects 3. Assumed, never examined.*

That is a correct statement about BDPT, and this finding does not dispute it. It disputes
the second clause: the model's **own adopted structure** selects $d=3$, twice over, and has
done so since founding decisions 1 and 2 were taken. Nobody had asked.

---

## 1. What BDPT does and does not give

Bisio–D'Ariano–Perinotti–Tosini derive the Weyl walk from linearity, unitarity, locality,
homogeneity and isotropy at minimal internal dimension $s=2$. They obtain a solution
**in each** of $d=1,2,3$ — the trivial shift, the square-lattice walk, and the BCC walk
(`references/qca-papers-1-4-overview.md` lines 26, 50–66). Uniqueness holds *within* a
dimension. Between dimensions the theorem is silent, which is exactly what A1 says.

So the question to ask is not "does BDPT pick 3" (it does not) but "**is $d$ still free once
the rest of the model is in place**". It is not.

---

## 2. The object every selector acts on

Write the walk's one-step unitary in the Pauli decomposition (Paper 1 Eq. 15)

$$A(\mathbf k) = u(\mathbf k)\,\mathbb I - i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}(\mathbf k),
\qquad u^2 + \lVert\tilde{\mathbf n}\rVert^2 = 1 .$$

Everything below is a statement about the **Jacobian of the Bloch vector at the origin**,

$$J \;=\; \frac{\partial\tilde{\mathbf n}}{\partial \mathbf k}\bigg|_{\mathbf k=0}
\;:\; \mathbb R^{d} \longrightarrow \mathbb R^{3}.$$

$J$ is $3\times d$ — **three rows in every dimension** — because the traceless Hermitian part
of a $2\times2$ matrix is 3-dimensional. That is not an assumption: every traceless Hermitian
$2\times2$ matrix is $\mathbf a\cdot\boldsymbol\sigma$ for a unique real 3-vector, and
$\{\mathbf a\cdot\boldsymbol\sigma,\ \mathbf b\cdot\boldsymbol\sigma\}=2(\mathbf a\cdot\mathbf b)\mathbb I$,
so *anticommuting is Euclidean orthogonality in $\mathbb R^3$* and the largest mutually
anticommuting set has exactly 3 elements. A fourth would have to be orthogonal to a basis,
hence zero (check A1).

Computed exactly from the BDPT walks (check A2):

| $d$ | $J$ at $\mathbf k=0$ | rank | $\dim\ker J$ | $\dim\operatorname{coker}J$ |
|---|---|---:|---:|---:|
| 1 | $(0,0,1)^{\mathsf T}$ | 1 | 0 | 2 |
| 2 | $\tfrac1{\sqrt2}\,[\,e_x\ e_y\,]$ (third row $\equiv0$) | 2 | 0 | 1 |
| 3 | $\operatorname{diag}(\tfrac1{\sqrt3},-\tfrac1{\sqrt3},\tfrac1{\sqrt3})$ | 3 | 0 | 0 |
| $\ge 4$ | 3 rows, $d$ columns | $\le3$ | $d-3>0$ | 0 |

$d=3$ is the one dimension where $J$ is **square and invertible**. Both selectors below are
one half of that sentence.

---

## 3. S1 — the upper bound, $d\le 3$

For $d\ge4$, $\ker J\neq0$ by counting alone: three rows cannot have trivial kernel on
$\mathbb R^{d>3}$. A nonzero $\mathbf k_0\in\ker J$ is a momentum direction with
$H_W(\mathbf k_0)=0$ at leading order — a zero-energy propagating direction.

Isotropy closes it, and there are two ways to close it — worth separating, because the first
carries a premise and the second does not.

*Route (a), the strong form.* The isotropy axiom makes the point group act on $\mathbb R^d$
with the vector representation irreducible (this is what makes the only invariant quadratic
form $\delta_{ij}$, hence $\omega$ isotropic at leading order). $\ker J$ is point-group
invariant, so it is $0$ or all of $\mathbb R^d$; the latter is $\tilde{\mathbf n}\equiv0$, the
trivial automaton. **This route assumes irreducibility**, which is standard for a Bravais
lattice's isotropy group but is a premise, not something proved here — the weakest link in S1
and flagged as such.

*Route (b), which needs no premise.* If $\ker J\ne0$ then the leading-order dispersion vanishes
identically along a subspace, so $\omega$ is not $\propto\lVert\mathbf k\rVert$ and the group
velocity is direction-dependent at leading order. Founding decision 2 defines $c_\text{lat}$ as
a *single number*, $d\Omega/d\lVert\mathbf k\rVert$ at $\lVert\mathbf k\rVert\to0$. With
$\ker J\ne0$ that limit does not exist independent of direction, and F26's whole construction —
and with it $c_\text{lat}=1/\sqrt d$, F79's $G$, F180's $c_\text{grav}=c_\gamma$ — has no
referent. So $d\ge4$ is excluded by the same decision that S3 uses, without any representation
theory.

Either way,

$$\boxed{\,d\le 3\,}\qquad\text{(check B1: } \ker J=0 \text{ exactly for } d\in\{1,2,3\}).$$

**Conditional on $s=2$.** For $s=2^{k}$ the Clifford bound is $2k+1$, so a larger cell would
relax this to $d\le 2k+1$. S3 below does not care.

---

## 4. S2 — the lower bound, $d\ge3$, and it is founding decision 1 that supplies it

$\operatorname{coker}J = \mathbb R^{3}/\operatorname{im}J$ is the set of **internal spin axes
that no momentum direction ever reaches**. Take $\hat{\mathbf m}\in\operatorname{coker}J$.
Because no momentum direction rotates it, $\hat{\mathbf m}$ is fixed by the whole point-group
action, so

$$H(\mathbf k) \;=\; \boldsymbol\sigma\cdot\tilde{\mathbf n}(\mathbf k) \;+\; m\,\boldsymbol\sigma\cdot\hat{\mathbf m}$$

is an admissible **isotropic mass term for a single Weyl walk**. At $d=2$ this is the familiar
parity-odd $\sigma_z$ mass of 2+1 dimensions, and check B2 verifies it explicitly:
$\operatorname{im}J=\operatorname{span}(e_x,e_y)$, the internal operator implementing a spatial
rotation is $e^{-i\theta\sigma_z/2}$, and $\sigma_z$ commutes with it.

At $d=1$ the cokernel is 2-dimensional. Note the scope carefully: the **counting** is checked,
the explicit invariance is checked only for $d=2$. Nothing rests on $d=1$ — it is already
excluded by S3, and independently by founding decision 5, since a one-dimensional space has no
transverse direction and therefore no photon polarisation at all.

Now the part that matters. **Hermiticity forces that $m$ to be real.** A diagonal mass carries
no phase. Founding decision 1 obtains chiral $SU(2)_L$ with no Higgs field by *gauging the
phase $\beta$ of the complex mass step* $m\to m e^{i\beta}$ (F27) — and an arbitrary phase
survives Hermiticity only in an **off-diagonal** mass block, i.e. only in the BDPT Dirac
construction (Paper 1 Eq. 23) that couples **two** Weyl walks. So:

$$\text{a phase to gauge exists} \iff \text{mass must be inter-branch} \iff \operatorname{coker}J=0 \iff d\ge3 .$$

At $d=1$ and $d=2$ a single walk can carry its own real mass, the two-branch coupling is not
forced, and **founding decision 1 has nothing to gauge**. Check B2 also verifies the converse
at $d=3$: $\operatorname{im}J=\mathbb R^{3}$, and a candidate $\mathbf a\cdot\boldsymbol\sigma$
commuting with all three internal generators forces $\mathbf a=0$.

$$\boxed{\,d\ge 3\,}\qquad\Longrightarrow\qquad \text{S1}\wedge\text{S2}:\ d=3 \quad\text{(check B3)}.$$

### Corollary — chirality is an orientation, and orientations need a square map

$J$ is square only at $d=3$, where

$$\det J \;=\; \mp\,3^{-3/2} \;=\; \mp\, c_\text{lat}^{3},$$

negative on the $+$ branch and positive on the $-$ branch (check D1). The helicity label that
F91 treats as *forced* is literally the **orientation** of the map from momentum space to spin
space. At $d\ne3$ there is no determinant, hence no two-valued handedness invariant. This is
the sharpest single-line form of S1 ∧ S2: *chirality exists because $J$ is square*.

---

## 5. S3 — the $(\mathbf E,\mathbf B)$ vector pair, exact and independent of $s$

Founding decision 2 defines $c_\text{lat}$ as the rotation rate of the real
$(\mathbf E,\mathbf B)$ **vector pair**, and the model's Maxwell law (Paper 1 Eq. 35, F25/F26)
is written with a cross product, $\partial_t\mathbf E = i\,2\mathbf n_{\mathbf k/2}\times\mathbf B$.
For $\mathbf B$ to be a vector rather than a bivector we need

$$\dim\Lambda^{2}\mathbb R^{d} = \dim\mathbb R^{d}
\quad\Longleftrightarrow\quad \frac{d(d-1)}{2}=d
\quad\Longleftrightarrow\quad d\in\{0,3\},$$

exact over the integers (check C1). $d=0$ is trivial, so $d=3$.

**No $d=7$ loophole.** A cross product also exists in $d=7$, but it is the octonionic product,
*not* the Hodge dual of a 2-form; the model's $\mathbf B$ is the dual object, and
$\star:\Lambda^2\to\Lambda^{d-2}$ is a 1-form only when $d-2=1$. Check C1 asserts both legs:
$\dim\Lambda^2\mathbb R^7 = 21 \ne 7$.

**The native form of the same statement.** The paired-spinor photon (founding decision 5, F69)
is a bilinear of two 2-spinors, so its field strength lives in the $\boldsymbol\sigma$-triplet
of $\mathbb C^2\otimes\mathbb C^2 = \mathbf 1\oplus\mathbf 3$ — a **three**-component object in
any $d$, because $\dim\mathfrak{su}(2)=3$. It can be identified with a spatial vector field only
at $d=3$.

S3 mentions the cell dimension $s$ nowhere. It is therefore not a restatement of S1/S2, and it
survives if BDPT's minimality postulate is dropped.

---

## 6. The "+1"

Time is one-dimensional **by the automaton's construction**, and this finding does not upgrade
that. The update is a single unitary $A$, so the evolution it generates is a $\mathbb Z$-action.
Any second commuting unitary flow would, under homogeneity, be a further generator of the
Cayley graph — that is, another **space** direction, which S1 then caps at three. So the
signature is $1+d$ and the content of the result is entirely in $d$.

Graded `structural`, not `exact`. A genuine derivation of the "+1" would have to explain why the
Cayley-graph/update split is not itself a choice, and that is the same territory as A8
(measurement and the classical limit), which remains ABSENT.

---

## 7. What this closes, and what it does not

**Closes.** $d$ is no longer a free integer of the model. Two logically independent routes each
return $\{3\}$:

| route | inputs | gives |
|---|---|---|
| S1 ∧ S2 | $s=2$ minimal cell; isotropy; founding decision 1 (Higgs-free chiral mass step) | $d=3$ |
| S3 | founding decision 2 ($(\mathbf E,\mathbf B)$ vector pair) **or** decision 5 (paired-spinor photon) | $d=3$ |

Losing either route leaves the other standing. Losing S3 *and* $s=2$ together would reopen the
question — that is the honest boundary.

**Does not close.** This is a derivation from *adopted* structure, not from nothing. It reduces
"why 3+1" to "why the minimal cell and the vector $(\mathbf E,\mathbf B)$ pair", which is a
strictly smaller assumption than a free integer, and it is the same reduction the model already
makes everywhere else (founding decision 6). It also does not derive the +1.

**Rubric consequence.** A1 should move `ABSENT → PARTIAL` on the next completeness run: the
grade is not `EXACT` because the "+1" is structural and because S1/S2 lean on $s=2$, but
`ABSENT` ("no sector at all") is no longer accurate — there is now a module, a gate-tier test
record and a falsifiable claim. Related: B10 ("why 3 colours") is **not** touched by this and
stays ABSENT; nothing here bears on $N_c$.

**$d$ is measurable.** $c_\text{lat}=1/\sqrt d$ (Paper 1 Eq. 21), so the model's light speed is
a readout of the spatial dimension, and $\lvert\det J\rvert = c_\text{lat}^{3}$ ties the same
number to the handedness structure. Verified against the constants registry at $3.2\times10^{-14}$
(check D2, finite differences on the engine's own `bcc._bcc_uvec`).

---

## 8. Falsifiers

1. **Exhibit an $s=2$ isotropic unitary walk in $d\ge4$ with $\ker J=0$.** S1 dies. (It cannot
   be done by counting, so this amounts to abandoning $s=2$ or isotropy.)
2. **Exhibit an isotropy-invariant intra-branch mass term for the $d=3$ BCC walk.** S2 dies, and
   with it the claim that founding decision 1 needs $d\ge3$. Equivalently: find a nonzero
   $\mathbf a$ with $[\mathbf a\cdot\boldsymbol\sigma,\ \sigma_i]=0$ for all $i$.
3. **Formulate the model's Maxwell sector with $\mathbf B$ as a bivector** and recover F25/F26's
   exact rotation law and $c_\text{lat}=d\Omega/d\lvert\mathbf k\rvert$. S3 dies and founding
   decision 2 is revealed as a convention rather than a constraint.
4. **Show $\det J$ is not the helicity label** — i.e. exhibit two BDPT branches at $d=3$ with the
   same sign of $\det J$, or a chirality-distinguishing invariant that survives $d\ne3$. The
   §4 corollary dies.
5. **A measured $c_\text{lat}\ne1/\sqrt3$** at the lattice scale would falsify $d=3$ directly,
   since $c_\text{lat}=1/\sqrt d$ is forced. This is the same observable F26/F28 already bound.

---

## 9. Provenance

- Module: `src/casim/engine/lattice/dimensionality.py` (`lattice` sector, `exactness=exact`,
  registered in `_SPINE`, D11).
- Test record: `F291-dimension-selectors`, `kind: assertion`, `tier: gate`, entry `check_all`,
  9/9 PASS. The load-bearing legs are re-derived with sympy **independently** of the module —
  the Bloch vectors are re-typed from the paper overview, not imported — and D2 additionally
  finite-differences the engine walk the simulator actually runs.
- Runner: `tests/runners/run_f291_dimension_selectors.py` → `test-results/F291_dimension_selectors.json`.
- Reads: F26 (rotation reinterpretation, $c_\text{lat}=1/\sqrt d$), F27 (chiral $SU(2)_L$ by
  $\beta$-gauging), F69 (paired-spinor photon), F91 (forced chirality classes), F25 (Maxwell as
  linearised rotation). Founding decisions 1, 2, 5, 6 in `CLAUDE.md`.
- Supersedes nothing. Contradicts nothing.
