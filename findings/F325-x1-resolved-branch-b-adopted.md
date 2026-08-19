# F325 — X1 resolved without $d_1$: the Casimir branch is **tested and closed** on two independent legs, the centre-value branch is **adopted**, and the fork's $C_F$ was a mixed-operator matching artefact all along

**Date:** 2026-08-18 - 23:40
**Numbering:** **F325**, taken as `max+1` against `F324` (`casim index` → `NEXT FREE NUMBER F325`, no gaps). Re-check before committing if a concurrent session has run since.
**Status:** Confirmed — **7/7 PASS**, both declared controls verified red and red only where declared. X1/X4/X5 are exact (unit-entry adjacency measured; $\ln 4$ exact; sympy over the lemma); X2 is an extrapolated law with a *measured* vanishing rate; X3 reproduces F111b T7 and measures the mismatch that makes it work; X6/X7 re-measure the other two legs by importing the entry points that own them.
**Verdict:** **Branch A (Casimir, $\chi=1/C_F=3/4$, $g_s=\sqrt3/4$, $\alpha_s(M_Z)=0.0397$): TESTED, CLOSED.** **Branch B ($\chi=1$, $g_s=\tfrac12$, $\alpha_s(\mu_0)=1/16\pi$): ADOPTED.** The "centre-normalised coupling with an $SU(N_c)$ $\beta$-function" inconsistency X1 named **never existed** — it was produced by evaluating one identity with two different theories' operators. Neither leg needs $d_1$, and neither needs the other.
**Cost, stated in the verdict rather than a footnote:** **CN19 falls**, and **F324's upper constraint falls with it** — B10 closes on **odd $N_c$** only, $\{3,5,7,\dots\}$. **$d_1$'s role changes and does not disappear:** it now *pins* $\alpha_s(M_Z)$ inside branch B and closes E3/Q1/Q2.
**Modules:** `src/casim/engine/gauge/derive_x1_branch.py` (new); legs also landed in `casimir_ladder.py` (`operator_consistency`, leg **L6**, plus the `numerator` control the F298 record was missing) and `derive_coupling_normalisation.py` (`casimir_branch_vs_f280_band`, leg **N8**, plus the `casimir_on` control)
**Test / results:** record `F325-x1-branch` (tier gate, entry `check_x1_branch`) → `test-results/F325_x1_branch.json`. Companion legs: `F298-casimir-ladder` (9/9, three controls), `F303-coupling-normalisation` (9/9, three controls)
**Reports:** `docs/status/x1-colour-normalisation-fork-2026-08-18.md` (the research pass), `docs/status/x1-section8-results-2026-08-18.md` (the five checks it named, run)
**Cross-references:** [[F303-no-centre-normalisation-argument]] (the three closed candidates — this is the fourth its own conclusion asked for), [[F299-casimir-scaling-discriminator-reinstated]] (re-characterised, §4), [[F298-casimir-ladder-c7-rerun]] (the mixed matching; results (1) and (2) superseded, S22), [[F294-c7-chi-map-ncolour-audit]] (its "Remains" item 1 was already closed by F111b), [[F111b-tree-gauge-su3-ladder]] (the SU(3) character rotor — the object F110 deferred and F294 asked for, built 2026-06-07; T7 defect in §5), [[F144-route-a-alpha-s-dimensional-transmutation]] (A1 step 2, §6), [[F280-d1-subtracted-against-wilson]] / CL252 (the bracket), [[F324-ncolour-bracket-closed]] (its upper constraint, §7), [[F101-strong-coupling-sigma-compact-rotor]] / [[F110-realtime-link-hamiltonian-confinement]] (the rotor and C7), [[F155-qstar-self-energy-and-freeze-bracket]] ($q_\ast$), [[F317-su3-structure-derived]] (the $SU(3)$ the links carry).

---

## 1. What X1 said, and why it does not need $d_1$

Part D recorded *"two adopted results that disagree"*: F144's $g_s=\tfrac12$ against F298/F299's Casimir reading, six decades apart in $\alpha_s$, load-bearing for B8, B10, D16, G5, E3, Q1, Q2, and decidable only by a one-loop background-field computation nobody had completed.

Branch A is closed by two arguments, and the point of writing them together is that **neither depends on the other**:

* **§2 (structural)** — the $C_F$ exists only in a *mixed* evaluation of the C7 identity. Both self-consistent evaluations give $\chi=1/(4g^2)$, for every $N$ and every irrep.
* **§3 (quantitative)** — branch A's required $\Lambda$-ratio is $5.63$ decades outside a bracket the model's own $d_1$ apparatus published on **2026-08-05**, the day *before* F299 and F303 framed the fork.

§4 then removes the appearance of a contradiction: F299 never discriminated between the branches and could not have. §5 audits the one thing C7 had never been checked against — the magnetic term — and closes X1's residual negatively.

---

## 2. The structural leg: the $C_F$ is a matching artefact

Write the C7 extraction with its two inputs separated:

$$\chi=\frac{[\text{rotor eigenvalue}]}{g^2\,n_\text{links}\,[\text{gauge eigenvalue}]},\qquad n_\text{links}=4\ \text{(F265: the BCC minimal loop is a 4-bond rhombus)}.$$

At $g^2=\tfrac14$ the abelian answer is $\chi=1$. Three evaluations, exact over $\mathbb Q$ (`casimir_ladder.operator_consistency`, leg **L6**):

| $N$ | both abelian (F294) | **mixed (F298)** | both $SU(N)$ | full irrep scan, consistent |
|---:|---:|---:|---:|---|
| 2 | 1 | 4/3 | 1 | 5 irreps → $\{1\}$ |
| 3 | 1 | 3/4 | 1 | 11 irreps → $\{1\}$ |
| 4 | 1 | 8/15, 8/5 | 1 | 15 irreps → $\{1\}$ |
| 5 | 1 | 5/12, 10/9 | 1 | 17 irreps → $\{1\}$ |
| 6 | 1 | 12/35, 6/7, 12/7 | 1 | 18 irreps → $\{1\}$ |
| 7 | 1 | 7/24, 7/10, 21/16 | 1 | 18 irreps → $\{1\}$ |

The middle column reproduces F298's published table exactly. **The two outer columns are 1 everywhere.**

**Why the consistent evaluation is the right one, not merely a possible one.** C7 is not a comparison of two systems: F110 C1 verifies to machine precision that the F101 rotor **is** the F110 link Hamiltonian restricted to one plaquette's Gauss sector. One operator in two notations has equal eigenvalues on corresponding states by construction; both brackets cancel and $\chi=1/(4g^2)$ carries only the geometric factor 4. That is exactly what F294 measured — *"the $s(m)^2$ cancels between the electric term and the rotor level"*, worst deviation literally `0.0` across seven groups — and it is why that measurement came out *exactly* $N$-free rather than approximately so.

**F298's own tell.** For $N\ge4$ its extracted "$\chi$" is level-dependent and *"the C7 identity does not exist"*. An identity that exists only where two unrelated spectra happen to be proportional is not an identity.

**And the mixed evaluation fails at $N=3$ too, once you leave the truncation.** F324 §3 U1c found the sextet leg of this and booked it as *"falsifier 5b … the most serious structural exposure on the upper side"*. The full picture at $N=3$ is worse than the one rung it sampled:

| irrep | $C_2$ | triality | rotor level $s^2$ | $\chi$ mixed | $\chi$ consistent |
|---|---:|---:|---:|---:|---:|
| $3$, $\bar3$ | 4/3 | 1, 2 | 1 | 3/4 | **1** |
| $6$ | 10/3 | 2 | 1 | **3/10** | **1** |
| $8$ | 3 | 0 | **0** | **undefined** | **1** |
| $10$ | 6 | 0 | **0** | **undefined** | **1** |
| $15$ | 16/3 | 1 | 1 | **3/16** | **1** |
| $27$ | 8 | 0 | **0** | **undefined** | **1** |

Three values and three undefined. The undefined rows are the sharpest statement of what the mixed matching is: a $\mathbb Z_3$ rotor cannot see triality-0 flux, so $s^2=0$ against $C_2\neq0$ — **it assigns zero electric cost to an adjoint, decuplet or 27 link.** Not an approximation with a small error. It is why the "identity" appears only on a tower every rung of which carries non-zero triality.

**Which evaluation the model is entitled to.** The $SU(N)$ one, because the integer spectrum is not derived from the rule:

* the rule's own $(\mathbf E,\mathbf B)$ are continuous real fields under an $SO(2)$ rotation (`weak_wmu._f26_rotation_step`; F26: *"real-valued 3-vectors"*);
* the integer spectrum is introduced as the exactly-solvable case — F101 *"keeps the same transfer operator but compact"*, `link_hamiltonian` *"the **integer** (compact) electric field"*, U(1) *"truncated at $|m|\le m_\text{max}$"*;
* Gauss's law is *"solved, not imposed"* — but by the **height** representation, which exists only for abelian groups, and integrality is an input to it;
* the model's own links are $SU(3)$-valued matrices (`strong.py`, `gluon.py`, `bcc_action.plaquette_field_strength_su3`, `confinement.py`, F94, F99 D3, and F317 derives the group). **`link_hamiltonian.py` holds no $SU(3)$ matrix at all.**

F298 and F303 already call the $\mathbb Z_3$ side an *"effective description"* of $SU(3)$. This finding takes that at face value and does the matching in one theory.

**This is a fourth reconciliation, and it is not one of F303's three.** F303 §4 enumerates three ways to *change the number in the numerator* — a scheme constant ($26\times$ too large), $n=3$ links (the BCC graph has no 3-bond loop), the Cartan weight $1/3$ (Landau pole). All three accept that the two sides carry different operators and ask what number bridges them. **Nothing bridges them, because it is one operator.** F303's own closing sentence asks for *"a fourth normalisation nobody has written down"*; it is not a fourth normalisation, it is the absence of one.

---

## 3. The quantitative leg: branch A is outside the model's own bracket

F280 S5 (record `F280-d1-subtracted`, 6/6 PASS, **2026-08-05**; card **CL252**) publishes

$$0\le\Delta C_\text{rule}^\text{loops}\le\Delta C_W^\text{loops}\ \Longrightarrow\ \frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}\in[1,\,7.980].$$

Rebuilt from the same three committed inputs rather than quoted (`casimir_branch_vs_f280_band`, leg **N8**), so the check moves if F163 or the Kawai–Nakayama–Seo anchor moves:

| | required $\Lambda$ | required $\Delta C_\text{rule}^\text{loops}$ | $\times$ Wilson's loops-only | position |
|---|---:|---:|---:|---|
| **branch B** | 1.773444 | 1.1458 | 0.276 | **inside**, at 11.08 % |
| Wilson action | 28.8086 | 6.7213 | 1.618 | above top by 3.610× |
| **branch A** | **3 400 378** | 30.0787 | **7.241** | **above top by $4.26\times10^{5}$ = 5.630 decades** |

Reproduced bookkeeping: $\Delta C_W=6.721348$, $\Delta C_W^\text{loops}=4.153795$, $T_W=2.567553$ (F280's leg 1, published $-2.5676$), band top $7.979672$.

**The exclusion survives dropping F280's named assumption.** Branch A does not merely violate monotonicity — it requires the rule's own loops-only one-loop constant to be **7.24×** Wilson's, for an action F287 §4 *measures* at $5.3$–$5.7\times$ **smaller** discretisation error than Wilson's at every grid, with an exactly empty seagull sector ($u_0\equiv1$, F155-A0).

**And every number the $d_1$ apparatus has ever returned sits with branch B**: F307's action-consistent $2.1348$, its propagator-only $1.633$, the withdrawn 2026-07-19 $\approx2.06$–$2.08$, and even its explicitly non-converged $14.27$. Not one is within five decades of branch A.

**This comparison had not been made.** The ledger's $d_1$ row prints *"required 1.773444 on branch B, $\approx3.4\times10^6$ on branch A"* and, in the same cell, *"band $\in[1,7.98]$"*. F303 §4.1 computed the $3.4\times10^6$ and compared it with F144's A4 residual and with Wilson's 28.81 — the two comparisons available in June — never with the bracket that landed the previous day. CL252 cross-references CL022, not CL257 and not X1.

---

## 4. F299 measured the premise, not the conclusion

F299 is arithmetically impeccable and reproduces independently (Weyl-torus quadrature, division-free Jacobi–Trudi, $n=240$): sextet $2.49115$ against its published $2.4911511$, and the other six rungs to 5–6 significant figures.

**But run the same engine at branch A's own coupling.** F299 uses $\beta=2N/g_s^2=24$ from $g_s=\tfrac12$; branch A's $g_s=\sqrt3/4$ gives $\beta=32$:

| $\beta$ | branch | $\sigma_6/\sigma_3$ | dev. from Casimir |
|---:|---|---:|---:|
| 24 | B | 2.49115 | $-0.35\%$ |
| 32 | **A** | **2.49540** | $-0.18\%$ |
| 96 | — | 2.49956 | $-0.02\%$ |

**The discriminator returns the same answer under both branches, and had to.** F299 §3 states the reason itself: in the continuum limit $\sigma_R=(g_0^2/2)C_2(R)$ *exactly*, so Casimir scaling is a theorem about the $SU(3)$ single-plaquette Wilson measure at weak coupling — true at every $\beta$, therefore carrying no information about which $\beta$ the rule fixes. The measure $d\mu_\beta\propto e^{(\beta/N)\operatorname{Re}\operatorname{Tr}U}dU_\text{Haar}$ in `confinement.py` is standard Wilson normalisation put in by hand; nothing in it comes from the CA rule.

So F299's content is: **the model's link variables carry $SU(3)$ irrep labels and their electric cost is $C_2(R)$** — which is precisely the premise under which the $C_F$ cancels in §2. **Correctly read, F299 supports branch B.** The X1 row's *"F299 measured the model's own confinement engine and found it implements the Casimir law instead"* reads a premise as a verdict.

*(The $d=2$ caveat F299 states is not the issue either way. The point is that Casimir scaling in $d=2$ is $\beta$-independent and so cannot select $\beta$. F323's $d=4$ successor is a statement about representation content too.)*

---

## 5. The magnetic side of C7 — X1's residual, closed negatively

C7 matched the *electric* term only. The live worry was that the $SU(3)$ plaquette operator is not $\cos\hat\phi$: its matrix elements between irreps could carry dimension or $6j$ factors and move $\chi$ off 1 by an $O(1)$ amount.

**X1 — it does not.** The magnetic operator is $-\tfrac{\lambda}{2}\times$(unit-entry adjacency $+$ transpose) in both theories: U(1)'s $\cos\hat\phi=\tfrac12(\Gamma+\Gamma^\dagger)$, and $SU(N)$'s $\chi_F+\chi_{\bar F}$, whose fundamental fusion is **multiplicity-free** so its adjacency is 0/1 (measured over the ladder to $p+q\le6$: non-zero entries $\{1.0\}$). Coefficient to coefficient, $\lambda\leftrightarrow\lambda$. **C7 survives a full electric $+$ magnetic audit against a genuine $SU(N)$ link Hamiltonian, and X1's named residual closes.**

**And the genuine $SU(N)$ link Hamiltonian already existed.** `su3_ladder.py`, created **2026-06-07** — five days before F144 — finding **F111b**, record `F111-tree-gauge-su3-ladder`. F294 §"Remains" item 1 read *"Build the $SU(N)$ Casimir ladder that F110 deferred, and re-run C7 against it. This is the one computation that decides between H1 and H2."* It had been built and run two months earlier, and none of F294/F298/F299/F303 cites F111b. (F299 does list a cross-reference `[[F111-su3-ladder-casimir-scaling]]` — a dangling link; the file is `F111b-tree-gauge-su3-ladder`.)

**X3 — but F111b T7 must not be quoted as confirmation, and this finding says why.** T7 reproduces (deviation $1.1\times10^{-3}$ against its own $5\times10^{-3}$ tolerance) — and it compares a **one-link** $SU(3)$ rotor, `su3_rotor_hamiltonian`'s $\tfrac{g^2}{2}C_2$, against a **four-link** U(1) rotor, `rotor_sigma1` at $\chi=1/(4g^2)$. Electric gaps $0.666667$ against $2.000000$, ratio exactly $3=n/C_F$: the two Hamiltonians are not the same physical system.

**X2 — compared consistently, the exact statement is different and carries no $N_c$ content:**

$$\frac{s_1^{SU(N)}}{s_1^{U(1)}}\;\longrightarrow\;\frac{2}{N^2-1}\qquad\text{as }\lambda\to0,\ \textbf{independent of }n_\text{links}.$$

Measured at $n=1$ and $n=4$ for $N=3,4,5$, Richardson-extrapolated to $\lambda=0$: worst residual $4.0\times10^{-9}$, with the departure vanishing at least linearly in $\lambda$ (slope 10 at $N=3$, 100 at $N\ge4$ — the singlet's return path through the ladder is shorter at $N=3$). Setting the ratio to 1 needs $N^2=3$. **So there is no $N_c$ selector hiding here**, and T7's agreement at $N=3$ is $C_Fd_F=(N^2-1)/2=4$ coinciding with the four links — attractive enough to be re-derived by someone who does not know it is a convention artefact, which is the same reason F303 §4.2 recorded the three-bond plaquette.

**X4 — new and exact.** Because $s_1$ differs by $2/(N^2-1)$ at the same $(\chi,\lambda)$,

$$\sigma_1^{SU(N)}-\sigma_1^{U(1)}=\ln\frac{N^2-1}{2}\ \xrightarrow{\,N=3\,}\ \ln4=\mathbf{1.386294}\ \text{nats},$$

a previously unrecorded correction to F99/F100/F101's string tension if the colour group is $SU(3)$ rather than the implemented $\mathbb Z_3$/U(1). **Orthogonal to $g_s$**, which is why it disturbs nothing above, and it belongs to the confinement sector as its own item.

---

## 6. X5 — a gap in F144 A1 step 2, and why it is not a rescue of branch A

Re-deriving F303's N1 symbolically reproduces its factorisation and then presses one step further:

```
M^T M - I  with a = r b:
  [0,0] = (r-1) sin^2(b sqrt(r) t)   [0,1] = (1-r) sin(2 b sqrt(r) t)/(2 sqrt(r))
solve for r  (b, t free)  ->  [{r: 1}, {r: pi^2/(b^2 t^2)}]     (the second carries t)
M^T M - I  at a = b       ->  [[0, 0], [0, 0]]   for EVERY b
```

F303 §2 states the premise verbatim — *"orthogonality at generic tick holds **iff $r=1$, whatever $b$ is**… the lemma constrains a *ratio* and nothing else"* — and concludes *"steps 1–2 survive"*. The consequence it does not draw: **a lemma that fixes only a ratio does not fix $\chi$.** At $a=b$ the one-tick map is a rotation through $\omega t=bt$, so with $t=1$ tick

$$a=b=\Omega(k)\qquad\Longrightarrow\qquad \chi=1/\Omega(k),$$

and $\chi=1$ requires $\Omega=1$. `running_alpha_s.py` states the chain as *"the rule's circular rotation FORCES equal electric/magnetic stiffness: chi = 1 in the rotor normalisation (F101 S7, **now derived**)"* — the forcing is real, the *value* is inherited from F101 §7. And it is the **same** compactification choice as §2's, so **F144's A1 carries two inherited choices of one origin, not zero knobs.**

Scale, on the rule's own 2D dispersion $\Omega(k)=2\arccos\!\big(\cos\tfrac{k_x}{2\sqrt2}\cos\tfrac{k_y}{2\sqrt2}\big)$: $\Omega$ spans $[0,2.744692]$ (BZ corner $2.744692$, edge $2.221441$, $\langle\Omega\rangle_\text{BZ}=1.645850$); F101 S5 hardcodes a representative $\Omega=1.3$; the measured $\alpha_s(M_Z)$ demands $\Omega=0.997829$ ($\chi=1.002176$); $\Omega=1$ sits at $|k|a=\sqrt2$ exactly on the axis.

**This does not restore branch A**, which needs $\chi=3/4$ i.e. $\Omega=4/3$ and has nothing selecting that either. What it does is relocate F144's open normalisation from *"zero knobs"* to **one $k$-selection**, plausibly the same object as the matching scale $q_\ast$ (F155's $q_\ast a\in[0.577,0.979]$). **Flagged as the residual, not as a claim** — the model's lattice is BCC and the above is the 2D square dispersion; the BCC $\Omega$ is the one that matters and has not been computed against this question. That is X1's residual after this finding.

---

## 7. What this costs, in full

**CN19 falls.** *"The C7 identity is well-defined only for $N_c\le3$"* is a property of the mixed matching (§2, right column: the identity holds for every $N$). It survives only in the weakened, and still useful, form: *the model's $\mathbb Z_N$ link Hilbert space is a faithful effective description of the $SU(N)$ k-string ladder only for $N\le3$* — a constraint on where `link_hamiltonian.py` may be used, not a selector for $N_c$.

**F324's upper constraint falls with it.** F324 (2026-08-17) closes $N_c$ on $\{3\}$ from a **lower** constraint (the $\mathbb Z_2$ doublet parity of the model's own derived $SU(2)_L$ — Witten's global anomaly; prior art, Bär & Wiese 2001, and F324 says so) paired with an **upper** one imported verbatim from F298. Remove the upper and the bracket closes on **odd $N_c$**, unbounded above: $\{3,5,7,\dots\}$ once F324's premise (ii) removes $N=1$. F324's own §3 U1c reaches the same place and books it as its falsifier 5b; §2 above realises it.

**So B10's honest post-resolution position is $N_c$ odd, $N_c\neq1$** — with $N_c=3$ favoured by everything empirical and by nothing structural. F324 prices its own incremental content at *"one bit"*; this finding spends that bit.

**Blast radius, measured rather than argued.** Exactly three registry records consume the two edited modules (`grep -rln` over `src`, `tests`, `tools`): `F298-casimir-ladder`, `F303-coupling-normalisation`, and `F324-ncolour-bracket` via `derive_ncolour_bracket.py`. All three **PASS** — F324 because its own "Mechanical note" re-evaluates the criterion on the imported `antisymmetric_ladder` rather than calling `c7_against_casimir_ladder`, so the new parameter does not reach it. **That is a passing test, not a passing argument:** F324's physics still rests on the mixed matching even though its code path no longer touches the function that implements it.

**$d_1$ is unchanged in method and reduced in stakes.** Its job is now to *pin* $\alpha_s(M_Z)$ inside branch B and close E3/Q1/Q2, not to choose between branches six decades apart. Its two-sided falsifier stands and is now the sharpest statement in the sector: a completed vertex computation returning $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ outside $[1,7.98]$ falsifies the $g_s=\tfrac12$ lock or F280's monotonicity assumption — **and a return of $3.4\times10^6$ would reinstate branch A and CN19 with it.** L6 (F305 §5, §4/§7.3) must still be decided before quoting.

---

## 8. Checks (`check_x1_branch`, 2026-08-18)

| # | Statement | Result | Tier |
|---|---|---|---|
| X1 | the magnetic term is $-\tfrac\lambda2\times$(unit adjacency $+$ transpose) in **both** theories, so it adds no factor to the $\chi$-map | entries $\{1.0\}$ / $\{1.0\}$ | exact (measured) |
| X2 | at equal $n$, $s_1^{SU(N)}/s_1^{U(1)}\to2/(N^2-1)$, independent of $n$, residual vanishing $\ge$ linearly in $\lambda$ | extrap. $4.0\times10^{-9}$; slopes 10 / 100 | quantitative |
| X3 | F111b T7 reproduces, and its electric gaps differ by exactly $n/C_F=3$ — the agreement is a 1-vs-4 artefact | dev $1.1\times10^{-3}$; ratio $3.000000$ | quantitative |
| X4 | $\sigma_1$ offset $\ln((N^2-1)/2)=\ln4$ between the $\mathbb Z_3$/U(1) engine and the $SU(3)$ one | $1.386294$ | exact |
| X5 | the lemma vanishes at $a=b$ for **every** $b$ ⇒ $\chi=1/\Omega(k)$, so $\chi=1$ is a normalisation | roots $\{1,\ \pi^2/(b^2t^2)\}$ | exact (sympy) |
| X6 | branch A closed on both legs | outside band by 5.630 decades | quantitative |
| X7 | branch B adopted, inside the model's own bracket | 11.08 % of $[1,7.98]$ | bracketed |

**7/7 PASS**, ~2 s.

**Controls (D9, both verified `CONTROL`).** `--param magnetic_scale=2.0` doubles the $SU(N)$ magnetic term only and reddens **X2** alone — the ratio law is a statement about *matched* magnetic normalisations, and a check that survives an unmatched one is not testing the matching. `--param su3_cut=2` truncates the character ladder below convergence and reddens **X2** alone.

**Two controls landed on the companion records in the same pass**, and the first of them is the one this finding turns on: `F298-casimir-ladder --param numerator=casimir` reddens exactly `[L2, L3]`. Both of that record's pre-existing controls perturb the **tower**; neither perturbed the **matching**, which was the one assumption doing all the work. `F303-coupling-normalisation --param casimir_on=False` reddens exactly `[N8]`.

---

## 9. Honest scope

- **The structural leg turns on one premise**, stated in §2 and testable: that the integer flux spectrum is a solvability choice rather than a derived property of the rule. Four modules and four findings present it as a choice and one stale document (`docs/audits/project-audit-inputs-dynamism-2026-06-06.md` line 41) files it as derived. **If someone shows the rule forces an integer-spectrum $\hat E$ on a link, the mixed matching is physical, branch A returns and CN19 with it.** That is the single sharpest way to attack this finding.
- **§3's exclusion inherits F280's inputs**, including F163's open $Q\to0$ extrapolation. It cannot inherit F280's *assumption*, because 7.24× in the wrong direction is not a monotonicity question.
- **§5's magnetic audit is single-plaquette**, matching C7's own scope. Multi-plaquette matrix elements are F110's remaining deferral and are not touched.
- **X4's $\ln4$ is exact for the leading strong-coupling law**; it is not a claim about $\sigma$ at the rule's actual coupling, which needs the full ground state at that $\lambda$.
- **§6 does not close $\Omega$.** It shows the lemma does not fix it and prices the gap at the 2D dispersion. The BCC computation is the next step and is not attempted here.
- **This finding does not compute $d_1$** and does not move E3/Q1/Q2.

## 10. Provenance

- **New:** the operator-consistency reading of C7 and its full-irrep scan (§2, leg L6); the off-tower table at $N=3$ including the three undefined rows; the confrontation of branch A with CL252's bracket (§3, leg N8); the $\beta$-independence of F299's discriminator (§4); the magnetic-adjacency audit and the exact ratio law $2/(N^2-1)$ (§5, X1/X2); the F111b T7 link-count defect (X3); the $\ln((N^2-1)/2)$ string-tension offset (X4); the $\chi=1/\Omega(k)$ consequence of F303's own lemma (§6, X5).
- **Reused:** `casimir_ladder` (F298's ladder and Casimirs), `su3_ladder` (F111b's character rotor and fusion), `derive_coupling_normalisation` (F303's chain), F280's committed band inputs and F163's constants, F287 §4's measured discretisation ratio, F324 §3 U1c's sextet.
- **External anchors (targets, not inputs):** $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.8086$ (Kawai–Nakayama–Seo, *Nucl. Phys.* **B189** (1981) 40); PDG $\alpha_s(M_Z)=0.1180$.
- **Verification:** record `F325-x1-branch` (tier gate, entry `check_x1_branch`), 7/7 PASS + two controls, 2026-08-18; companion legs `F298-casimir-ladder` 9/9 and `F303-coupling-normalisation` 9/9, three controls each.
