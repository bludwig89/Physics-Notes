# F292 — Three is the only multiple of three: $d=6$ and $d=9$ excluded, and a reducible $d=3n$ freezes

*2026-08-02 - 17:05 · sector `lattice` · module `casim.engine.lattice.dimensionality` ·
test record `F292-higher-multiples` (8/8 PASS, gate tier) ·
results `test-results/F292_higher_multiples.json`*

**Question.** F291 showed the model's adopted structure selects $d=3$. The immediate follow-up,
raised by Ben: if 3 is special, is 6 or 9? And in particular — does the model admit
**three copies of three**, given that the number 3 already appears more than once in it?

**Answer.** No, and the two candidates fail for different reasons, which is what makes the
question worth a finding rather than a footnote. The reducible reading ($d=3n$ as $n$ copies of
$\mathbb R^3$) is the one that survives longest, and it fails in an informative way: the extra
directions are not compactified, they are **frozen**.

---

## 1. The scoreboard

| $d$ | $\dim\Lambda^2\mathbb R^d$ | overcount $\tfrac{d-1}{2}$ | $D=d+1$ | chirality? | min cell $2^{\lfloor d/2\rfloor}$ | reducible $\ker J$ |
|---:|---:|---:|---:|:--:|---:|---:|
| **3** | **3** | **1 ✓** | 4 | **yes** | 2 | 0 |
| 6 | 15 | $\tfrac52$ ✗ | 7 | **no** | 8 | 3 |
| 9 | 36 | 4 ✗ | 10 | yes | 16 | 6 |
| 12 | 66 | $\tfrac{11}2$ ✗ | 13 | no | 64 | 9 |

---

## 2. S3′ — the bivector overcount, in closed form

F291's S3 asked $\dim\Lambda^2\mathbb R^d = d$. Written as a ratio it is cleaner and says more:

$$\frac{\dim\Lambda^2\mathbb R^d}{d} \;=\; \frac{d-1}{2},$$

the factor by which a magnetic field **overcounts** a vector field. It equals 1 at exactly one
dimension, $d=3$ (check A1: `solve((d-1)/2 = 1) == [3]`). At $d=3n$ the factor is $(3n-1)/2$,
which is 1 only at $n=1$. So the answer to "why not a higher multiple of three" is a one-line
identity: **the overcount grows linearly and passes through 1 exactly once.**

$d=6$: $\tfrac52$. $d=9$: $4$. Neither can carry founding decision 2's $(\mathbf E,\mathbf B)$
**vector** pair. Independent of the cell dimension $s$.

---

## 3. S4 — chirality parity (new)

A chirality projector requires a traceless $\Gamma=\gamma_1\cdots\gamma_D$ squaring to the
identity. In **odd** spacetime dimension $D$ that product is proportional to $\mathbb I$ in the
irreducible representation, so there is no projector and the Dirac representation does not split.
Founding decision 1 gauges the phase relating a **left/right pair** (F27; F91's right-branch
weight $\equiv0$), so it needs that splitting:

$$\text{chirality} \iff D=d+1 \text{ even} \iff d \text{ odd}.$$

Not quoted from the literature — **constructed**. Checks B1/B2 build the Clifford algebra by an
explicit recursion in dimension $2^{\lfloor D/2\rfloor}$, verify
$\{\gamma_a,\gamma_b\}=2\delta_{ab}$ for $D=2\ldots8$, and confirm $\Gamma\propto\mathbb I$
precisely on odd $D$. (The test rebuilds the recursion separately from the module, so the verdict
is computed twice by two independently typed constructions.)

**Consequence.** $d=6$ has $D=7$: **no chirality at all**. It is not a near miss — founding
decision 1 has no left/right pair to gauge, exactly as at $d=2$. $d=9$ has $D=10$, even, so it is
the only multiple of three that clears S4 — and then dies on S3′.

### The cross-check worth noticing — $d=2$ is **excluded twice**

Read carefully: what follows is a *double rejection* of $d=2$, not a second candidate. S4 and
F291's S2 are unrelated arguments — one is Clifford parity, the other is the cokernel of the
Bloch Jacobian — and both **reject** $d=2$: S4 because $D=3$ is odd so no chirality projector
exists, S2 because the mass there is the real parity-odd $\sigma_z$ term with no phase to gauge
(check B3). Two independent routes rejecting the same dimension, neither built to test it, is
evidence the machinery is not circular.

For the avoidance of doubt, the complete ladder across F291 and F292 is:

| $d$ | verdict | excluded by |
|---|---|---|
| 1 | out | S3′ ($\dim\Lambda^2\mathbb R^1=0$); no transverse photon (decision 5) |
| 2 | out **twice** | S2 **and** S4 |
| **3** | **survives every selector** | — |
| $\ge4$ | out | S1 ($\ker J\neq0$) |
| 6, 9, 12, … | out | S3′; $d=6$ also S4 |

**$d=3$ is the only dimension left standing anywhere in F291 or F292.**

---

## 4. The reducible case — $d=3n$ as $n$ copies of $\mathbb R^3$

This is the version of the question actually worth asking, because it changes the premises.
Reading $\mathbb R^{3n}$ as $\bigoplus_{b=1}^{n}\mathbb R^3$ makes the point group act
**block-diagonally**, so F291's S1 route (a) — which assumed the vector representation is
irreducible — no longer applies.

It has a sharp answer, and the reason is the one structural fact F291 leant on throughout:
**a 2-dimensional cell has exactly one $\boldsymbol\sigma$-triplet** ($\dim\mathfrak{su}(2)=3$).
All $n$ blocks must map into the *same* internal $\mathbb R^3$. Hence (check C1)

$$\operatorname{rank}J = 3,\qquad \dim\ker J = 3(n-1),\qquad \dim\operatorname{coker}J = 0 .$$

**The walk sees exactly one $\mathbb R^3$.** The remaining $3(n-1)$ directions are exact zero
modes at leading order: the field is constant along them, they carry no dispersion, and nothing
propagates in them.

**This is not compactification.** There is no radius, no Kaluza–Klein tower, nothing to make
small and nothing that would reappear at high energy. It is degeneracy. The extra directions do
not exist dynamically, whatever the geometry says.

**And a residual coupling would not save them.** The model cannot supply the $O(k^2)$ terms of a
hypothetical $3n$ walk — BDPT gives no such walk — so this finding does not claim the freezing is
exact to all orders. It does not need to: any dependence entering at $O(k^2)$ or beyond is an
**irrelevant** operator under F130's *measured* Kadanoff spectrum ($\lambda_n=b^{-n}$), so
coarse-graining removes it. Frozen at leading order, irrelevant beyond it.

**What survives.** $\operatorname{coker}J=0$ throughout, so **founding decision 1 is untouched**
by the reducible case — the chiral mass step is fine in $d=3n$. The failure is S1 and S3′ only.
That the three selectors disagree about *which* dimensions they kill is the best available
evidence that they are independent constraints rather than one argument in three costumes.

---

## 5. A bigger cell does not rescue any of it

Relaxing BDPT minimality raises the reachable dimension — the minimal spinor is
$2^{\lfloor d/2\rfloor}$, so $d=6$ needs $s=8$ and $d=9$ needs $s=16$ (check C2). But S3′ and S4
**never mention $s$**. Growing the cell buys the upper bound and nothing else: $d=6$ is still
even, $d=9$ still overcounts by 4.

---

## 6. An observation, explicitly not a claim

The model does contain more than one "3", and this finding makes the pattern sharper: the map
from $n$ spatial copies of $\mathbb R^3$ into one internal triplet has multiplicity $n$, and
$\mathbb R^3$-valued multiplicity is exactly what F75 uses when it ties **three generations** to
$O_h$'s maximum single-valued irrep dimension 3, through the same $T_{1u}\cong(x,y,z)$ that
labels spatial directions (Paper 8 §"ties the number 3 to the three spatial dimensions").

It is tempting to read the frozen copies as generations. **This finding does not.** Nothing here
derives that identification, F75's own status is a *stated hypothesis* rather than a theorem
(rubric row C1), and the frozen directions have no dynamics to carry a generation label. The
honest statement is the negative one: the model's repeated threes are **internal labels sharing
one vector irrep**, not spatial copies — and $N_c=3$ (rubric row B10) remains ABSENT and is not
touched by anything here. Recorded so a later session does not rediscover the resemblance and
mistake it for a result. A falsifier is given below.

---

## 7. Falsifiers

1. **Exhibit an isotropic $s=2$ walk on $\mathbb R^{3n}$, $n\ge2$, with $\operatorname{rank}J>3$.**
   §4 dies. It cannot be done while the cell is a qubit, so this is really a challenge to $s=2$.
2. **Exhibit a chirality projector in odd $D$** — a traceless $\Gamma$ with $\Gamma^2=\mathbb I$
   anticommuting with no $\gamma_a$ — and $d=6$ reopens. Checks B1/B2 say it does not exist for
   $D\le8$; a general proof is standard Clifford theory and is *not* re-proved here, which is
   this finding's one imported step.
3. **Formulate the model's Maxwell sector at $d=9$ with $\mathbf B$ as a 36-component bivector**
   and recover F25/F26. S3′ dies (and so does F291's S3).
4. **Show the frozen directions are not RG-irrelevant** — i.e. produce a $3n$ walk whose extra-block
   dependence is relevant or marginal under F130's block-spin. The "irrelevant beyond leading
   order" clause in §4 dies, and the freezing becomes only a leading-order statement.
5. **Derive the generations–frozen-copies identification of §6.** That would *promote* an
   observation this finding deliberately refuses, and would bear on C1 and possibly B10.

---

## 8. Provenance

- Module: `casim.engine.lattice.dimensionality` (extended, not new; `findings=("F291","F292")`).
- Test record: `F292-higher-multiples`, `kind: assertion`, `tier: gate`, entry `check_all`, 8/8.
  The Clifford recursion is written twice — once in the module, once in the test — so B2 is a
  genuine cross-check.
- Runner: `tests/runners/run_f292_higher_multiples.py` → `test-results/F292_higher_multiples.json`.
- Reads: F291 (the three selectors), F27 (chiral $SU(2)_L$ by $\beta$-gauging), F91 (forced
  chirality classes), F130 (measured Kadanoff spectrum, $\lambda_n=b^{-n}$), F75 (three
  generations from $O_h$ — cited in §6 only to *decline* an inference).
- Supersedes nothing. Contradicts nothing. Rubric rows B10 and C1 are untouched.
