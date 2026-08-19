# X1 — the colour-normalisation fork: research report and a resolution

**Date:** 2026-08-18
**Scope:** `docs/status/open-derivations.md` Part D row **X1**, and the chain F101 §7 → F144 → F115 (CM3) → F294 → F298 → F299 → F303.
**Status of this document:** research report, not a finding. Everything below is either a reproduction of a committed number or an argument about how two committed numbers relate. Nothing here has a gate record yet; §8 lists what would need one.
**Verification script:** `tools/x1_probe.py` (standalone, numpy only; reproduces every number in §2, §3 and §5 from scratch).

---

## 0. Summary

The X1 row states a fork the tree cannot choose between: branch **A** (Casimir, $g_s=\sqrt3/4$, $\alpha_s(M_Z)=0.0397$, $-66\%$) "supported by the structure and nothing else", branch **B** (centre, $g_s=\tfrac12$, $\alpha_s(M_Z)=0.1186$, $+0.5\%$) "supported by the measurement and nothing else", to be decided by a $d_1$ computation that has not been quoted.

**The fork resolves, and it resolves toward branch B, on two independent grounds — neither of which requires waiting for $d_1$:**

1. **The structural leg of branch A is an artefact of a mixed matching.** F298's $C_F$ appears only because the C7 identity is evaluated with the **abelian rotor's** eigenvalue $s(k)^2$ in the numerator against the **SU(N) gauge theory's** eigenvalue $C_2(R_k)$ in the denominator. Under either *self-consistent* matching — both sides abelian, or both sides $SU(N)$ — the identity returns $\chi=1/(4g^2)$ **exactly, for every $N$ and for every irrep**, with no representation content at all. Verified over $\mathbb Q$ in §2. Branch A therefore has no structural support; it has a bookkeeping error.

2. **Branch A is already excluded, numerically, by the model's own $d_1$ apparatus.** F280 S5 (record `F280-d1-subtracted`, 6/6 PASS, 2026-08-05, card **CL252**) publishes the bracket $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\in[1,\,7.980]$. Branch A requires $3.4\times10^6$ — **5.63 decades above the band's top**, and requiring the rule's loops-only one-loop constant to be **7.24×** Wilson's for an action F287 §4 *measures* to be $5.3$–$5.7\times$ **closer** to the continuum than Wilson's. Branch B's $1.7734$ sits inside the band at 11.1%. The X1 row and the $d_1$ row print both numbers and never compare them.

A third observation removes the appearance of a contradiction entirely:

3. **F299 does not discriminate between the branches, and was never capable of doing so.** Its engine gives $\sigma_6/\sigma_3 = 2.49115$ at $\beta=24$ (branch B's coupling) and $2.49540$ at $\beta=32$ (branch A's coupling) — the same answer, because Casimir scaling in 2D is a *theorem* about the $SU(3)$ Wilson measure at weak coupling, for any $\beta$. Reproduced independently in §3. What F299 actually establishes is that the model's link variables carry $SU(3)$ **representation content** — which is precisely the premise under which the $C_F$ in (1) cancels. **Correctly read, F299 is evidence *for* branch B, not against it.**

**The cost, stated up front:** resolving X1 this way costs **CN19** — F298's "the C7 identity exists only for $N_c\le3$", currently B10's only structural, reading-independent leg. That constraint is a property of the *mixed* matching too (§4). B10 loses a leg and reverts to fully open. This is a real price and it should not be paid quietly.

---

## 1. What the fork actually is

F144's A1 has three steps. F303 §2 audited them and found steps 1–2 sound and group-blind:

* **Step 1.** The rule's per-mode $(\mathbf E,\mathbf B)$ map is an exact circular rotation (residuals $<10^{-15}$).
* **Step 2.** The rotor lemma: $H=\tfrac a2E^2+\tfrac b2B^2$ has an orthogonal one-tick flow **iff $a=b$**. F303 re-derived it symbolically and showed every entry of $M^{\rm T}M-\mathbb 1$ carries an explicit factor $(r-1)$, $r=a/b$ — so the condition is on a *ratio*, and carries "no Casimir, no dimension, no representation content."
* **Step 3.** F110's C7 matching. One isolated plaquette has 4 exclusive boundary links, so
  $$\tfrac{g^2}{2}\cdot 4\cdot[\text{gauge }\hat E^2] \;=\; \tfrac{1}{2\chi}\cdot[\text{rotor }\hat E^2].$$

Step 3 is where the fork lives. The dispute is the ratio of the two bracketed quantities.

* **F294** evaluated both brackets in the **abelian** theory ($m^2$ against $m^2$) across $\mathbb Z_2..\mathbb Z_9$ and $U(1)$ and measured $\chi=1/(4g^2)$ with worst deviation literally `0.0`. Its own explanation, in the module: *"the $s(m)^2$ cancels between the electric term and the rotor level, so $\chi=1/(4g^2)$ holds per LEVEL."*
* **F298** evaluated the numerator in the **abelian** theory ($s(k)^2$, the $\mathbb Z_N$ symmetric residue) and the denominator in **$SU(N)$** ($C_2$ of the $k$-box antisymmetric irrep). It got $\chi=1/(4g^2C_F)$ at $N\le3$, level-dependent above.

Both are correct arithmetic. They differ in **which operator's eigenvalue goes in the numerator.**

---

## 2. The structural resolution: the $C_F$ is a matching artefact

Write the C7 extraction as a function of two independent choices — the rotor's spectrum and the gauge theory's spectrum:

$$\chi \;=\; \frac{[\text{rotor eigenvalue}]}{g^2\,n_\text{links}\,[\text{gauge eigenvalue}]},\qquad n_\text{links}=4\ \text{(derived geometry, F265/F303 §4.2)}.$$

At $g^2=\tfrac14$ the abelian answer is $\chi=1$. Evaluating the three possible readings over $\mathbb Q$ on the $k$-string tower (`Fraction`, no floats):

| $N$ | both abelian (F294) | **mixed: abelian rotor / $SU(N)$ gauge (F298)** | both $SU(N)$ |
|---:|---:|---:|---:|
| 2 | $1$ | $4/3$ | $1$ |
| 3 | $1$ | $3/4$ | $1$ |
| 4 | $1$ | level-dep $8/15,\,8/5$ | $1$ |
| 5 | $1$ | level-dep $5/12,\,10/9$ | $1$ |
| 6 | $1$ | level-dep $12/35,\,6/7,\,12/7$ | $1$ |
| 7 | $1$ | level-dep $7/24,\,7/10,\,21/16$ | $1$ |

The middle column reproduces F298's published table exactly (SU(2) $\to 4/3=1/C_F$, SU(3) $\to 3/4=1/C_F$, level-dependent for $N\ge4$). **The two outer columns are $1$ everywhere.**

Extending the right-hand column off the $k$-string tower to the full irrep set (all Young diagrams with $\le N-1$ rows, $\le5$ boxes):

| group | irreps tested | $\chi$ | level-independent |
|---|---:|---|---|
| SU(2) | 5 | $\{1\}$ | yes |
| SU(3) | 11 | $\{1\}$ | yes |
| SU(4) | 15 | $\{1\}$ | yes |
| SU(5) | 17 | $\{1\}$ | yes |
| SU(6) | 18 | $\{1\}$ | yes |
| SU(7) | 18 | $\{1\}$ | yes |

**Why this is the right reading, not merely a possible one.** The C7 identity is not a comparison of two physical systems; it is the statement that the F101 rotor **is** the F110 link Hamiltonian restricted to one plaquette's Gauss sector — F110 C1 verifies exactly that equivalence to machine precision. If the two are the same operator in different notation, their eigenvalues on corresponding states are equal *by construction*, the bracketed quantities cancel, and $\chi=1/(4g^2)$ carries only the geometric factor 4. That is what F294 measured, and it is why the measurement came out *exactly* $N$-free rather than approximately so.

The mixed reading instead computes the ratio of the spectra of two **different** rotors — a compact $U(1)$ rotor (spectrum $m^2$) and a non-abelian rotor (spectrum $C_2$) — and calls that ratio a stiffness. It is not a stiffness; it is a spectral discrepancy. F298 states the tell itself without drawing the conclusion: for $N\ge4$ the extracted "$\chi$" is level-dependent and *"the C7 identity does not exist"*. An identity that exists only when two unrelated spectra happen to be proportional is not an identity; it is a coincidence of the $N\le3$ truncation.

**Which rotor does the model actually have?** The $SU(N)$ one:

* `bcc_action.py` carries `plaquette_field_strength_su3(U_bcc, generators)` — the model's gauge action has **$SU(3)$-valued links** on 4-bond rhombi.
* F99 D3 runs its centre-covariance test on *"real SU(3) links"*; F94 is a 3+1D $SU(3)$ heat-bath.
* F317 derives the $SU(3)$ structure (commutant $=M_3$, dim 9 $\Rightarrow U(3)$; F27 chirality removes the $U(1)$).
* The integer/$\mathbb Z_N$ spectrum is **not derived from the rule**. `link_hamiltonian.py` introduces it as a solvability choice, in its own words an *"exact finite Hilbert space, no truncation error"*, alongside a $U(1)$ option truncated at $|m|\le m_\text{max}$; and the height representation it uses to solve Gauss's law exactly *only works for abelian groups*. F110's scope note says the $SU(3)$ Casimir ladder "remains future work".

So the model's gauge theory is $SU(3)$, and the integer ladder is the abelian reduction chosen for exact diagonalisation. The consistent C7 evaluation is the right-hand column: **$\chi=1/(4g^2)$, $\chi=1 \Rightarrow g_s=\tfrac12$, and the $SU(N_c)$ $\beta$-function is then the correct one to run with.** The apparent inconsistency the X1 row names — "normalised on the centre while running on $SU(N_c)$" — never existed; what existed was a $C_F$ imported by evaluating one side of an identity in a different theory from the other.

**This is a fourth reconciliation, and it is not one of F303's three.** F303 §4 enumerates three ways to *change the number in the numerator* — absorb it into the scheme constant (closed: 26×), change $n$ from 4 to 3 (closed: BCC parity), read it as the Cartan weight $|\lambda|^2=1/3$ (closed: Landau pole). All three accept the premise that the numerator and denominator carry different operators and ask what number should bridge them. The fourth option is that **no number bridges them, because it is one operator.** F303's own closing sentence anticipates the shape without finding it: *"or supply a fourth normalisation nobody has written down."* It is not a fourth normalisation. It is the absence of one.

---

## 3. F299 measures the premise, not the conclusion

F299 is arithmetically impeccable and I reproduced its table from scratch (independent Weyl-torus quadrature, division-free Jacobi–Trudi characters, $n=240$):

| rep | F299 published | this reproduction | Casimir law |
|---|---:|---:|---:|
| $6$ | 2.4911511 | 2.49115 | 5/2 |
| $8$ | 2.2433555 | 2.24336 | 9/4 |
| $10$ | 4.4634964 | 4.46350 | 9/2 |
| $15$ | 3.9720941 | 3.97209 | 4 |
| $15'$ | 6.9047286 | 6.90473 | 7 |
| $27$ | 5.9314777 | 5.93148 | 6 |

**But run the same engine at branch A's own coupling.** F299 uses $\beta=2N/g_s^2=24$ from $g_s=\tfrac12$ (branch B). Branch A's $g_s=\sqrt3/4$ gives $\beta=32$:

| $\beta$ | branch | $\sigma_6/\sigma_3$ | deviation from Casimir |
|---:|---|---:|---:|
| 24 | B ($g_s=1/2$) | 2.49115 | $-0.35\%$ |
| 32 | A ($g_s=\sqrt3/4$) | 2.49540 | $-0.18\%$ |
| 96 | — | 2.49956 | $-0.02\%$ |

**The "discriminator" returns the same answer under both branches.** It has to: F299 §3 itself states that in the continuum limit $\sigma_R=(g_0^2/2)C_2(R)$ *exactly*, so Casimir scaling is a theorem about the $SU(3)$ single-plaquette Wilson measure at weak coupling — true at every $\beta$, and therefore carrying zero information about which $\beta$ the rule fixes. The measure $d\mu_\beta\propto e^{(\beta/N)\operatorname{Re}\operatorname{Tr}U}\,dU_\text{Haar}$ in `confinement.py` is standard Wilson normalisation put in by hand; nothing in it comes from the CA rule.

So F299's content is: **the model's link variables carry $SU(3)$ irrep labels and their electric cost is $C_2(R)$.** That is exactly the premise of §2's right-hand column. F299 is a load-bearing input to the resolution, not an obstacle to it. The X1 row's framing — "F299 measured the model's own confinement engine and found it implements the Casimir law instead" — reads a premise as a verdict.

*(The $d=2$ caveat F299 states does not bear on this either way. The point here is not that centre dominance might appear in $d=4$; it is that Casimir scaling in $d=2$ is $\beta$-independent and so cannot select $\beta$.)*

---

## 4. What the resolution costs: CN19

CN19 — *"the C7 identity is well-defined only for $N_c\le3$, a structural constraint that consumes no measured number and is independent of the H1/H2 dispute"* — is currently the only leg of B10 that survives both branches. **It does not survive this resolution.** The $N\le3$ restriction is exactly the statement that $s(k)^2 \propto C_2(\text{antisym }k)$ holds only for $N\le3$; under the consistent matching no such proportionality is required, and the identity holds for every $N$ (§2, right column). CN19 is a property of the mixed matching, like the $C_F$ itself.

What survives, in weakened form, is a statement about the *implementation* rather than about $N_c$:

> The model's $\mathbb Z_N$ link Hilbert space is a faithful (up to one overall constant) effective description of the $SU(N)$ $k$-string ladder **only for $N\le3$**; from $N=4$ the middle of the tower pulls away and no rescaling repairs it.

That constrains where `link_hamiltonian.py` may be used. It does not select $N_c$, because the $\mathbb Z_N$ reduction is a solvability choice rather than a derived feature of the rule. **B10 therefore reverts from "one structural leg plus X1" to fully open**, and the ledger should say so. That is the honest price of the resolution and it is worth paying: a leg that rests on an inconsistent matching is not a leg.

There is one way to keep it, and it is a real question, not a rescue: **is the integer quantisation of the link flux a derived property of the CA rule, or a choice?** If someone can show the rule itself forces an integer-spectrum $\hat E$ on a link — not a $U(1)$/$\mathbb Z_N$ *model* of one — then the mixed matching is the physical one after all, branch A returns, and CN19 with it. Nothing in F101, F110, F99 or F294 currently makes that claim; all four introduce the compact ladder as the exactly-solvable case. This is the single sharpest question left in X1, and §8 lists it first.

---

## 5. The independent quantitative leg: branch A is already excluded by CL252

This leg does not depend on §2 at all, and it is the more surprising of the two, because it is a comparison of two numbers **both already committed to the tree**.

F280 S5 (`F280-d1-subtracted`, 6/6 PASS + control, 2026-08-05; card **CL252**; `exactness-inventory.md` row *"Tadpole-free band contains the target, excludes Wilson"*) publishes:

$$0\le\Delta C_\text{rule}^\text{loops}\le\Delta C_W^\text{loops}\quad\Longrightarrow\quad \frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}\in[1,\;7.980].$$

Reproduced from the committed inputs ($\Lambda_{\overline{\rm MS}}/\Lambda_L=28.8086$ Kawai–Nakayama–Seo; F163 $C_\text{lat}=6.138643$; $C_{\overline{\rm MS}}=131/66$):

* $\Delta C_W = 2\ln 28.8086 = 6.721348$
* $\Delta C_W^\text{loops} = 6.138643 - 131/66 = 4.153795$
* $T_W$ (seagull + Haar) $= 2.567553$ — F280's leg 1, published $-2.5676$ ✓
* band top $= e^{\Delta C_W^\text{loops}/2} = 7.9797$ ✓

Now place the two branches on it:

| | required $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ | required $\Delta C_\text{rule}^\text{loops}$ | as a multiple of Wilson's loops-only | position vs band |
|---|---:|---:|---:|---|
| **branch B** | $1.773444$ | $1.1458$ | $0.276\times$ | **inside**, at 11.1% |
| Wilson action (for scale) | $28.8086$ | $6.7213$ | $1.618\times$ | above top by $3.61\times$ |
| **branch A** | $3.4\times10^{6}$ | $30.0786$ | $\mathbf{7.24\times}$ | **above top by $4.26\times10^{5}$ = 5.63 decades** |

Two things to note.

**(i) The exclusion survives dropping F280's assumption.** F280 labels the monotonicity step ($\Delta C_\text{rule}^\text{loops}\le\Delta C_W^\text{loops}$) as an assumption, not a theorem — correctly. But branch A does not merely violate it marginally: it requires the rule's own loops-only one-loop constant to be **7.24 times Wilson's**, for an action whose $b_0$ discretisation error F287 §4 *measures* at $5.3$–$5.7\times$ **smaller** than Wilson's at every grid, and whose seagull/Haar sector is *exactly* empty ($u_0\equiv1$, F155-A0). Branch A needs the near-continuum action to be forty-odd times *worse* than Wilson's in the same quantity that is measured to be several times better.

**(ii) Every number the $d_1$ machinery has ever produced sits with branch B.** Not one of them is within five decades of branch A:

| source | $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ | status |
|---|---:|---|
| F307 §"for the record", leg-2 midpoint fed into F280's slot | $14.27$ | non-converged, F307 explicitly refuses to read it as physics |
| F307 action-consistent one-path value | $2.1348$ | $\times1.204$ of branch B's target; not quotable ($b_0$ recovery 0.41–0.49) |
| `lpt_selfenergy`, 2026-07-19 constants | $\approx2.06$–$2.08$ | withdrawn (F307 §"the live refold") |
| F307 propagator-only $\Delta C=0.981$ | $1.633$ | partial leg |
| F280 target (branch B) | $\mathbf{1.7734}$ | — |
| **branch A requirement** | $\mathbf{3.4\times10^{6}}$ | — |

The apparatus is not converged and cannot yet *pin* $\alpha_s$. It does not need to be converged to **exclude a value 5.63 decades outside its own bracket and outside the full spread of every partial result it has ever returned.**

**This comparison is not made anywhere in the tree.** `open-derivations.md`'s $d_1$ row (Part A) prints *"required $1.773444$ on branch B, $\approx3.4\times10^6$ on branch A"* and, in the same cell, *"band $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\in[1,7.98]$"*. CL252 is filed as `open / bracketed` and cross-references CL022, not CL257 or the X1 row. F303 §4.1 computes the $3.4\times10^6$ and compares it to Wilson's 28.81 and to F144's A4 residual — the two comparisons that were available in June — and never to the bracket that landed the previous day.

---

## 6. Why this went unnoticed for twelve days, mechanically

Worth recording alongside F303 §5's own lesson ("a deferral coming due"), because the mechanism here is different and is a D9-shaped gap rather than a deferral.

**(a) F298's record has no control on its load-bearing assumption.** `F298-casimir-ladder` declares two controls: the *symmetric* tower (proving the $N\le3$ result is not an artefact of choosing a convenient ladder) and a scan truncated at $N=3$ (proving the exclusion of $N\ge4$ is not vacuous). Both perturb the **tower**. Neither perturbs the **matching** — the choice of which operator supplies the numerator, which is the one assumption doing all the work. A control that swapped $s(k)^2$ for $C_2(R_k)$ in the numerator would have gone green when it should have gone red, i.e. would have shown the "identity" is insensitive to the thing being asserted. In D9 terms: *the record cannot see its own premise fail.*

**(b) The two halves of the fork were priced in different units and never converted.** X1 lives in $\alpha_s$/$\chi$ units; CL252 lives in $\Lambda$-ratio units. The conversion is one line ($\Delta(1/\alpha)=16\pi(C_F-1)=16.755 \Rightarrow \Lambda\text{-ratio}=e^{\Delta/2b_0}=3.4\times10^6$) and F303 wrote that line — but wrote it into a comparison against Wilson rather than against the model's own bracket. The bracket was six days older than the finding that needed it.

**(c) "The measurement" and "the structure" were both mislabelled.** The X1 row credits branch B with "the measurement" (the $0.08\%$ $\alpha_s$ agreement) and branch A with "the structure" (F298/F299). After §2 and §5, branch B holds **both** the structure and two independent measurements, and branch A holds neither. The row's symmetry was an artefact of not asking what F299 was sensitive to and not asking what CL252 already said.

---

## 7. What X1 should read after this

Proposed replacement for the Part D row, subject to the checks in §8 being landed:

> **X1 — RESOLVED toward branch B (centre-value coupling, $g_s=\tfrac12$), on structure and on the model's own $\Lambda$-bracket.** The $C_F$ in F298 arises from evaluating the C7 identity with the abelian rotor's eigenvalue against the $SU(N)$ gauge theory's eigenvalue; under either self-consistent evaluation $\chi=1/(4g^2)$ exactly, for every $N$ and every irrep, with no representation content. The model's links are $SU(3)$-valued (`bcc_action`, F94, F99 D3, F317), so the consistent evaluation is the $SU(N)$ one, $g_s=\tfrac12$ stands, and the $SU(N_c)$ $\beta$-function is the right one — the "centre-normalised coupling with an $SU(N_c)$ $\beta$-function" inconsistency never existed. Independently: branch A's required $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=3.4\times10^6$ is **5.63 decades outside CL252's committed bracket $[1,7.98]$** and requires the rule's loops-only constant to be $7.24\times$ Wilson's for an action measured $5.3$–$5.7\times$ closer to the continuum. F299 is reinstated as **support** for the resolution: it establishes that link cost is $C_2(R)$, which is the premise under which the $C_F$ cancels; its $\sigma_6/\sigma_3$ is $\beta$-independent (2.49115 at $\beta=24$, 2.49540 at $\beta=32$) and never discriminated between the branches.
> **Cost: CN19 falls.** The $N_c\le3$ restriction is a property of the mixed matching, not of C7. B10 returns to fully open with no structural leg. **Residual: the magnetic side of C7 has never been audited** (§8 item 2). **$d_1$'s role changes** from *deciding* the branch to *pinning* $\alpha_s$ within it.

Consequential edits, if this is accepted:

| object | change |
|---|---|
| **CN17** | unchanged as a no-go; add that it closed three routes within a premise now itself in question |
| **CN18** (F299) | re-characterise: measures link representation content, **not** coupling normalisation; add the $\beta$-independence datum |
| **CN19** (F298) | **withdraw** as a structural $N_c$ selector; retain the weakened implementation-validity statement (§4) |
| **CL022** | the $2.1\sigma$ framing stands and is no longer "contingent on H1"; the contingency note added by F303 can be lifted |
| **CL252** | add the branch-A exclusion as a second consequence of the bracket; cross-reference CL257 and the X1 row |
| **CL257** | remove the C7-based $N_c\le3$ leg; B10 `PARTIAL` → the grade should be re-examined, not merely re-blessed |
| **B10 row** | "conditional on X1" → unconditional and unattacked again, minus CN19 |
| **$d_1$ row** | drop the "$\approx3.4\times10^6$ on branch A" alternative; $d_1$ pins $\alpha_s$, it no longer decides a branch |
| `link_hamiltonian.py` scope note | state that the $\mathbb Z_N$/$U(1)$ ladder is a solvability reduction of an $SU(3)$ link, and that C7 transfers a **coefficient**, not a spectrum |

---

## 8. What would have to be landed, in order

1. **The one question that could reverse this (do it first).** Is the integer quantisation of the link electric flux **derived from the rule**, or is it the compact-$U(1)$/$\mathbb Z_N$ modelling choice that F101 §2, F110 and F294 all present it as? If derived, the mixed matching is physical, branch A returns and CN19 with it. Cheap to settle by reading F26/F43/F99 for whether $\hat E$'s spectrum is forced; expensive to settle if it needs a rule-level derivation. **Everything in §2 is conditional on the answer being "choice", which is what the four modules currently say.**

2. **Audit the magnetic side of C7 — the genuine new open item.** §2 fixes the electric term only. The $SU(3)$ plaquette operator is *not* $\cos\hat\phi$: its matrix elements between irreps carry dimension and $6j$ factors, whereas the abelian rotor's are $\tfrac12$. The circularity lock is $a=b$ (electric stiffness $=$ magnetic stiffness), so a non-abelian magnetic normalisation moves $\chi$ away from 1 by an $O(1)$ factor — a *different* correction from the Casimir, and one nobody has computed. This is bounded, well-posed, and is what X1's residual becomes. Note it can only shift $\chi$, not restore a $C_F$ in the electric matching.

3. **Add the missing control to `F298-casimir-ladder`.** Perturb the numerator's operator (`--param numerator=casimir`) and require the $C_F$ and the $N\le3$ restriction both to vanish. Per D9 this is what makes the record able to see its own premise fail. Roughly 20 lines against `casimir_ladder.c7_against_casimir_ladder`.

4. **Register the branch-A exclusion against CL252.** One check in `derive_coupling_normalisation.py`: the Casimir shift $16\pi(C_F-1)=16.755$ converts to $\Lambda$-ratio $3.4\times10^6$, which is outside `[1, 7.980]` by 5.63 decades and requires $\Delta C_\text{rule}^\text{loops}=7.24\times\Delta C_W^\text{loops}$ against F287 §4's measured $5.3$–$5.7\times$ *improvement*. Declare a control that widens the band and turns the check red.

5. **Then $d_1$, unchanged in method and reduced in stakes.** The native sweep at $n=28$–$40$ on the F308-repaired path, with **L6 decided first** (F305 §5's 86% propagator fork, and §4/§7.3's link-axis mode which flips the sign of $b_0$). Its job is now to pin $\alpha_s(M_Z)$ inside branch B and to close E3/Q1/Q2 — not to choose a branch. If it returns anything in $[1,7.98]$, X1 stays closed; if it returns $3.4\times10^6$, everything above is wrong and CN19 comes back.

---

## 9. Reproduction

`tools/x1_probe.py`, numpy only, ~2 s:

* §2 tables — exact over $\mathbb Q$ (`fractions.Fraction`), three matchings on the $k$-string tower for $N=2..7$ plus the full-irrep scan.
* §3 tables — independent 2D $SU(3)$ Weyl-torus quadrature with division-free Jacobi–Trudi characters, $n=240$, at $\beta=24/32/96$. Reproduces F299's seven rungs to 5–6 significant figures.
* §5 tables — $\Delta C_W$, $\Delta C_W^\text{loops}$, $T_W$, the band top, and each branch's required $\Delta C_\text{rule}^\text{loops}$, from the committed anchors.
* One-loop running $\mu_0\to M_Z$ with $n_f$ thresholds reproduces $\alpha_s(M_Z)=0.11954$ (branch B, 1-loop; F144 publishes 0.1195) and $0.03981$ (branch A; F303 publishes 0.03970), and the required $\alpha_0$ to $\sim0.1\%$ of F298's $0.0198779$ — the residual being threshold-placement convention, not method.

## 10. Sources

Findings: F101 §7, F110 (C1, C7), F115 (CM3), F144 (A1, A4), F155 (A0), F163, F239, F265, F280 (S5), F287 (§4, §5, §6), F293, F294 (§3, §4), F298 (§2, §3, §4), F299 (§1, §3, §5), F303 (§2, §3, §4), F305 (§4, §5, §7.3), F307 (§3, and its Λ values), F308, F317.
Modules: `casimir_ladder.py`, `casimir_scaling.py`, `confinement.py`, `derive_coupling_normalisation.py`, `derive_ncolour.py` (`c7_zn_independence`), `link_hamiltonian.py`, `bcc_action.py`.
Ledger/cards: `docs/status/open-derivations.md` (Part A $d_1$, Part B CN15–CN19, Part D X1), `docs/status/exactness-inventory.md`, CL022, CL252, CL257.
External: Kawai–Nakayama–Seo, *Nucl. Phys.* **B189** (1981) 40.
