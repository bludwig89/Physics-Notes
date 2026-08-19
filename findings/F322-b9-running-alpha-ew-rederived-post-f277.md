# F322 — B9 re-derived post-F277: the $0.24\%$ never touched the refold, and what F277 actually supplied was its **warrant** — plus the shortfall is two-loop, and $80\%$ of it is already in the tree

> **[CITATION AMENDMENT 2026-08-18 - 16:20 — cross-reference added; no leg, control or number changed]**
>
> §6 of this finding and **§2.2 of [[F311-gap5-three-numbers-adjudicated]]** (2026-08-11 - 21:20, six days
> earlier) close the **same** residual by different routes, and this file cited F311 nowhere. It does now:
> **§6.1** is the reconciliation. Nothing in §1–§9 moves — no leg, no control, no value, and the `Status:`
> line below is unchanged. What changes is that the two published residuals stop being readable as rivals:
> **$0.0495\%$ is the model-internal number** (this finding, from F261's sympy-exact $b_1=1$: the two-loop
> *leading log* only) and **$0.00158\%$ is the number after importing the Källén–Sabry two-loop constant**
> (F311, which its own §8 states is *cited, not derived here*). Raised by
> `docs/status/completeness-2026-08-18.md` gap #4 and row **H5** item (ii).

**Date:** 2026-08-17 - 21:55
**Status:** Confirmed — 6/6 legs PASS, 2/2 declared controls verified `CONTROL` over **disjoint** red sets. Closes `docs/status/completeness-2026-08-07.md` gap **#5(a)** and moves rubric row **B9**, flagged un-re-derived for three consecutive reports. Roadmap item `next-steps-pt2` b9.
**Module:** `casim.engine.interactions.running_alpha_lattice_bound`
**Record:** `F322-b9-running-rederived` (`tests/registry/interactions.yaml`, gate tier, entry-driven)
**Results:** `test-results/F322_b9_running_rederivation.json`
**Cross-references:** [[F311-gap5-three-numbers-adjudicated]] (the *same* residual, identified six days earlier as the two-loop leptonic term using the **cited** Källén–Sabry constant, and the first closure of gap #5(a) — see §6.1), [[F251-qed-vacuum-polarization-running-alpha]] (the $\Pi$ and the Pi4 number under review; superseded by S12), [[F277-qed-gluon-refold-period]] (the sign flip that raised the flag), [[F261-twoloop-qed-ae-amu]] (the sympy-exact $b_1=1$ this feeds into the running for the first time), [[F115-coupling-magnitudes-running-rotor]] (B9's EW leg as graded — CM2's Planck-anchored negative), [[F138-weinberg-gap-closure-4piv-matching]] (the $\mu_\star=4\pi v$ matching that replaced it), [[F231-weinberg-2over9-onshell-face-of-1over4]] (the $8/9$ bridge), [[F162-bgfield-self-energy-b0-gate]] (the non-abelian $b_0$ template), [[F151-scheme-constant-determined]] / [[F152-ir-coupling-the-irface]] (the hadronic piece this still defers — rubric row G3)

---

## 1. What this addresses

Row B9 (*running of $\alpha$, EW couplings*) is graded `QUANT` on one number: F251's Pi4, leptonic $\Delta\alpha(M_Z)$ agreeing with PDG to $0.24\%$. F251 is superseded by **S12-F277**, which flipped a vacuum-polarization sign, and the report recorded for the third consecutive time that *"grep still finds no post-F277 re-derivation"* (gap #5a, "the cheapest — one number, one re-run").

The flag conflates two questions, and separating them is most of the result:

| | Question | Answer |
|---|---|---|
| **Accounting** | does the $0.24\%$ *depend* on the refolded path? | **No.** §2 |
| **Physics** | the $0.24\%$ is a *continuum* closed form. So what is the model's own **lattice** content in the running, and does it leave $\Delta\alpha$ alone at the precision being quoted? | Nobody had asked. §3–§5 |

This is the fourth consecutive amendment-class residual whose stated form turned out to be an accounting statement rather than a hard physics one (A11 → F319, B12, B11 → F321, now B9). Amendment 8's own lesson applies to itself: **a residual that has not moved in three reports is more likely mis-stated than hard.**

## 2. The accounting answer — the number could not have moved (L1)

`leptonic_running`'s call closure is exactly $\{$`_dalpha_lepton`$\}$. `_fermion_B` and `_K_lat` — the refolded path — are **not in it**; they are reached only from `lattice_b0_consistency`. The two closures are disjoint.

Measured rather than asserted: the lattice kernel is replaced by $7.3\,K_\text{lat}+0.5$ and $\Delta\alpha_\ell(M_Z)$ is required to return **bitwise** identical.

$$\Delta\alpha_\ell(M_Z)=0.03142092800460496\quad\text{base and perturbed, bit for bit.}$$

So the value B9 is graded on is $0.031421$ vs PDG $0.031498$ — $0.2447\%$ — post-F277 exactly as before it. F277 §6 already said *"F251 5/5 unchanged"*; what was missing was the reason, and the reason is that Pi4 is a closed form in $\ln(s/m_\ell^2)$ that never enters the loop integrand.

## 3. The physics the flag should have asked — $q$-flatness **is** $\Delta\alpha$ invariance

Because Pi4 is continuum, the honest question is what the *lattice* contributes. That content is entirely in Pi3, and its meaning has been understated since F251.

For $q=(Q,0,0,0)$ Euclidean, transversality (Pi1, exact) gives $\Pi^{\mu\nu}=(q^2\delta^{\mu\nu}-q^\mu q^\nu)\Pi(q^2)$, so the module's transverse coefficient is

$$B(Q)\;=\;\frac{\Pi^{00}-\Pi^{11}}{Q^2}\;=\;-\,\Pi(q^2).$$

The running is a **subtracted** object, $\Delta\alpha(s)=\Pi(0)-\Pi(s)$, so any $q$-**independent** additive constant in $\Pi$ cancels *identically*. With $\Delta(Q)\equiv B_\text{rule}(Q)-B_\text{cont}(Q)$,

$$\boxed{\;\Delta\alpha_\text{lattice}(s)-\Delta\alpha_\text{cont}(s)\;=\;f\,\big[\Delta(s)-\Delta(0)\big]\;}$$

So Pi3's $q$-flatness is not merely *"the log coefficient is propagator-independent"*. It is the stronger statement that **the lattice leaves $\Delta\alpha$ itself invariant**, and its measured non-flatness is therefore an *error bar on the model's $\Delta\alpha$ prediction* — the thing B9 never had.

## 4. The calibration $f=4\pi\alpha$ (exact, model-internal)

$f$ is fixed by the module's **own** $b_0$ gate, with no fit and no external normalisation. The UV log coefficient in $B$ units is $b_0^\text{QED}/(16\pi^2)=(4/3)/(16\pi^2)=1/(12\pi^2)$, against $d(\Delta\alpha)/d\ln s=\alpha/(3\pi)$ per unit-charge Dirac fermion:

$$f=\frac{\alpha/3\pi}{1/(12\pi^2)}=4\pi\alpha=0.09170124\ .$$

A fit was tried first and **rejected**: at finite $n$ the midpoint cube cannot resolve $\ln(1/Q^2)$ for $Q<\pi/n$, so the fitted slope drifts from $-1.08\times10^{-3}$ ($n{=}16$) toward $-3.24\times10^{-3}$ ($n{=}28$) against the exact $-1/(12\pi^2)=-8.443\times10^{-3}$ — still $62\%$ low at $n{=}28$. The IR is grid-limited on the *unsubtracted* leg. This is not a defect of $\Delta$, which is subtracted on a common domain and is where the artifacts cancel — but it does mean the normalisation must come from the algebra, not the quadrature.

## 5. The measured bound — F277 did not change the number, it created its **warrant**

Bound $=f\cdot(\text{spread}/\ln\text{-range})\cdot\ln(M_Z^2/m_e^2)$, i.e. the residual non-flatness read as a residual log and extrapolated over the full physical range $L=24.184$. Shortfall to PDG $=7.7072\times10^{-5}$.

| $n$ | spread of $\Delta$ | bound on $\delta(\Delta\alpha)$ | $\times$ shortfall | fraction of $\Delta\alpha$ |
|---:|---:|---:|---:|---:|
| **post-F277** 20 | $1.685\times10^{-5}$ | $1.701\times10^{-5}$ | $0.221$ | $5.4\times10^{-4}$ |
| 24 | $9.279\times10^{-6}$ | $9.366\times10^{-6}$ | $0.122$ | $3.0\times10^{-4}$ |
| 28 | $6.705\times10^{-6}$ | $6.767\times10^{-6}$ | $\mathbf{0.088}$ | $2.2\times10^{-4}$ |
| **refold restored** 20 | $1.4484\times10^{-2}$ | $1.4619\times10^{-2}$ | $189.7$ | $0.464$ |
| 24 | $1.4431\times10^{-2}$ | $1.4565\times10^{-2}$ | $189.0$ | $0.462$ |
| 28 | $1.3980\times10^{-2}$ | $1.4111\times10^{-2}$ | $\mathbf{183.1}$ | $0.448$ |

Two readings, and the second is the sharp one:

* **Magnitude.** Post-F277 the lattice's contribution to $\Delta\alpha(M_Z)$ is bounded at $0.09$–$0.22$ of the PDG shortfall — *below* the discrepancy, so the $0.24\%$ is a statement about continuum truncation and not about lattice artifact. With the refold it is $183$–$190\times$ the shortfall and **$45$–$46\%$ of $\Delta\alpha$ itself**.
* **$n$-dependence — the discriminator.** Grid noise shrinks with refinement; a genuine residual log does not. Post-F277 the ratio bound$(n{=}28)/$bound$(n{=}20)=\mathbf{0.398}$. Refolded it is $\mathbf{0.965}$ — flat, which is what a spurious log looks like. ($\Delta$'s *mean* tells the same story: post-F277 it converges monotonically to $-2.124\times10^{-3}$ at $n{=}28$, reproducing F277's $-2.1214\times10^{-3}$; refolded it drifts $+1.4\times10^{-3}\to+7.5\times10^{-3}$ and never converges.)

**So before F277 the quoted "matches PDG to $0.24\%$" carried a lattice uncertainty roughly $190\times$ larger than the agreement it claimed.** The number was simultaneously right and unwarranted. That — not a changed value — is the answer to gap #5a, and it is why the flag was worth carrying even though its literal form was wrong.

## 6. Attributing the shortfall — F261's $b_1=1$ closes $80\%$ of it, and was already in the tree

The $7.7072\times10^{-5}$ shortfall is **two-loop**, and the model has the coefficient: F261's two-loop QED $\beta$ is sympy-exact, $b_1=1$ per unit-charge fermion in $d(1/\alpha)/d\ln\mu^2=-(1/4\pi)(b_0+b_1(\alpha/\pi)+\dots)$. Propagating it into $\Delta\alpha=1-\alpha_0/\alpha(s)$ gives a two-loop leading-log term $\alpha^2L_\ell/(4\pi^2)$ per lepton. **It had never been fed into the running.**

| lepton | $L_\ell$ | one loop | two-loop LL |
|---|---:|---:|---:|
| $e$ | $24.1841$ | $0.01743466$ | $3.262\times10^{-5}$ |
| $\mu$ | $13.5209$ | $0.00917844$ | $1.824\times10^{-5}$ |
| $\tau$ | $7.8761$ | $0.00480783$ | $1.062\times10^{-5}$ |
| **sum** | | $\mathbf{0.03142093}$ | $\mathbf{6.1483\times10^{-5}}$ |

$$\Delta\alpha_\ell(M_Z)=0.03148241\quad\text{vs PDG }0.031498:\qquad 0.2447\%\;\longrightarrow\;\mathbf{0.0495\%}$$

$79.8\%$ of the shortfall, with the correct sign, from a coefficient the tree already owned. $1/\alpha(M_Z)\big|_\text{lep}$ moves $132.7302\to132.7218$. **Honest scope:** the leading log is what $b_1$ fixes; the two-loop non-log constant and three loops are **not** derived here, and they are the residual $1.559\times10^{-5}$.

### 6.1 Relation to F311 — the same residual, two published numbers, and the difference is one imported constant

F311 §2.2 reached this residual six days earlier and from the other end, and the two results are two
rows of **one sum**, not two answers to one question:

| piece of $\Delta\alpha_\ell(M_Z)$ | value | source | derived on the model's own fields? |
|---|---:|---|:---:|
| one loop, $\sum_\ell\frac{\alpha}{3\pi}[L_\ell-\frac53]$ | $3.1420928\times10^{-2}$ | F251 Pi4 / §2 here | **yes** ($b_0^\text{QED}=4/3$, sympy-exact) |
| two loop, **leading log** $\alpha^2L_\ell/(4\pi^2)$ | $+6.1483\times10^{-5}$ | §6 here, from F261's $b_1=1$ | **yes** (sympy-exact) |
| two loop, **non-log constant** $(\alpha/\pi)^2[\zeta(3)-\frac5{24}]$ per lepton | $+1.6085\times10^{-5}$ | **F311 §2.2** | **no — Källén–Sabry, cited** |
| two loop, total $(\alpha/\pi)^2[\frac{L_\ell}{4}+\zeta(3)-\frac5{24}]$ | $+7.7568\times10^{-5}$ | the two rows above, additively | mixed |
| PDG shortfall after one loop | $7.7072\times10^{-5}$ | — | — |

The third row **is** this finding's stated residual: $1.5589\times10^{-5}$ against the constant's
$1.6085\times10^{-5}$, i.e. the imported term supplies $\mathbf{103.2\%}$ of it. The excess is
$4.96\times10^{-7}$ in $\Delta\alpha$ — the *same* number F311 reports from the other side as
$100.6\%$ of the one-loop residual, and it is what $0.00158\%$ measures. So:

$$\underbrace{0.0495\%}_{\textbf{model-internal}\ (\text{one loop}+b_1\ \text{leading log})}\qquad\text{and}\qquad\underbrace{0.00158\%}_{\text{after importing the Källén–Sabry constant (F311)}}$$

**Three things follow, and they are the reason this section exists.**

1. **Neither finding supersedes the other and there is nothing to adjudicate.** The numbers are
   compatible by construction: they differ by exactly one term, whose value is known and whose
   *derivation on the model's own fields* is open in both files. This is **not** a Part D
   contradiction in `docs/status/open-derivations.md`, and it should not be recorded as one.
2. **B9's model-internal headline is the $0.0495\%$**, because it is the number the model derives
   end to end with zero imported constants. The $0.00158\%$ is quotable only with its provenance
   attached — *"after importing the two-loop constant"* — which is exactly how F311 §8 states it.
3. **The open work is unchanged and is jointly owned.** §9's third bullet and F311 §8 name the same
   target by the same route: the two-loop leptonic bubble on the model's own fields, starting from
   F261's dispersive machinery. Having the literature value of the term does not derive it.

**One priority note, recorded rather than absorbed.** §2 and the *refold restored* rows of §5 reproduce
F311 leg A1 — that S12-F277 does not reach Pi4, proved by reinstating the removed refold — which F311
established on 2026-08-11 and which closed `completeness-2026-08-07` gap #5(a) at that date. This
finding reached it independently and measured it differently (a $7.3\times{+}0.5$ kernel perturbation
on the *whole* Pi4 payload here, the reinstated `_fermion_B` refold there), so it stands as an
independent reproduction of a result whose first closure belongs to F311, not as its first statement.

## 7. B9's EW leg — reproduced, and the input its precision is owed to

B9's other half is graded on F115 (2026-06-08), whose CM2 anchored the bare angle at the Planck scale and overshot by $-74\%$. That reading is superseded in substance: F138 identifies $\tfrac14$ as the **compositeness-scale matching** at $\mu_\star=4\pi v=3094.09$ GeV, and F231 decomposes the $8/9$ bridge to the on-shell $\tfrac29$. One-loop Higgs-free running to $M_Z$ is reproduced here exactly:

$$\sin^2\bar\theta_W(M_Z)=0.2317341\quad\text{vs PDG }\overline{\text{MS}}\ 0.23122:\ +0.222\%$$

Then the measurement nobody had made. That running takes $\alpha_\text{em}(M_Z)$ as an **input**, and $s^2-\tfrac14\propto1/\alpha_\text{em}^{-1}$, so the residual is directly sensitive to it ($ds^2/d\alpha^{-1}=1.428\times10^{-4}$). Feeding the model's **own** $\alpha(M_Z)$ — leptonic only, scheme-matched by the measured on-shell$\to\overline{\text{MS}}$ offset $0.976$, i.e. *without* the hadronic vacuum polarization the model defers to row G3:

| $\alpha_\text{em}(M_Z)^{-1}$ used | source | $\sin^2\bar\theta_W(M_Z)$ | residual |
|---|---|---:|---:|
| $127.951$ | PDG $\overline{\text{MS}}$ (F138's input) | $0.2317341$ | $+0.222\%$ |
| $131.746$ | **model**, leptonic $+$ two-loop LL | $0.2322602$ | $\mathbf{+0.450\%}$ |

A factor **2.02**. The missing $3.795$ in $\alpha^{-1}$ is the hadronic piece. **So B9's two halves are not independent: they share one input, and half of the EW leg's quoted precision is owed to a number the model does not derive.** That is B9's real residual, and it is row G3 — not the refold.

## 8. Verification summary (6/6, 2/2 controls)

| leg | check | type | result |
|---|---|---|:---:|
| B9-1 | $\Delta\alpha_\ell$ bitwise unchanged under a $7.3\times{+}0.5$ kernel perturbation | measured | identical |
| B9-2 | $f=4\pi\alpha$ from $b_0^\text{QED}=4/3$; slope $=1/(12\pi^2)$ | exact | $<10^{-15}$ |
| B9-3 | lattice bound below the PDG shortfall at every $n$ | convergent | $0.088$–$0.221\times$ |
| B9-4 | bound falls fast with $n$ (grid noise, not a residual log) | convergent | ratio $0.398<0.7$ |
| B9-5 | F261 $b_1=1$ closes $>75\%$ of the shortfall; agreement $<0.06\%$ | quantitative | $79.8\%$, $0.0495\%$ |
| B9-6 | F138 $+0.222\%$ reproduced; leptonic-only $\alpha$ degrades it $>1.5\times$ | quantitative | $2.02\times$ |

**Controls (D9/H2), measured not expected, and their red sets are disjoint:**

| perturbation | reddens | why it must |
|---|---|---|
| `refold_control: true` | **B9-3, B9-4** | restores the exact F277 defect: the bound jumps to $190\times$ the shortfall and stops falling with $n$ |
| `b1_control: 0` | **B9-5** | removes the model's two-loop coefficient; the shortfall must reopen |

Neither control touches the other's legs, and neither touches B9-1, B9-2 or B9-6 — so `only: true` holds in both.

## 9. What this closes, and what it does not

**Closed.** Gap #5(a). B9's number is re-derived on post-F277 code, its lattice content is bounded for the first time, the bound is shown to be *below* the discrepancy and *shrinking*, and the discrepancy itself is attributed and $80\%$ removed. B9's `QUANT` grade is now carried by $0.0495\%$ (QED) and $+0.222\%$ (EW), with F251's ⚠ resolvable to "superseded, number re-derived, warrant supplied".

**Not closed, and stated rather than absorbed:**

* **The hadronic piece is still row G3.** It is $3.795$ in $\alpha^{-1}(\overline{\text{MS}})$, and §7 now quantifies what B9 pays for not having it: a factor 2 on the EW residual. F151/F152 remain the place it has to come from.
* **The two-loop non-log constant is not derived.** $1.559\times10^{-5}$ of $\Delta\alpha$, i.e. the residual $0.0495\%$. F261's dispersive machinery (the $K_1$ kernel on F251's spectral function) is the natural route and was not attempted here. **F311 §2.2 supplies its literature value** — $(\alpha/\pi)^2[\zeta(3)-\tfrac5{24}]$ per lepton, $1.6085\times10^{-5}$ summed, $103.2\%$ of this residual — which is what turns $0.0495\%$ into the imported $0.00158\%$. F311 §8 is explicit that the form is **cited, not derived**, so this bullet is unchanged by it: what is open is the constant *on the model's own fields*. See §6.1.
* **The absolute BZ measure for rule-kernel integrals is still F277 §8's open item.** Every number in §5 is a *subtracted* lattice$-$continuum difference on a common domain, which is what makes it meaningful; the fundamental domain of a $\sqrt3\cdot$fcc-periodic function is still not the midpoint cube, and F267 is where that gets settled. The §4 fit failure is an independent, milder symptom of the same thing.
* **The extrapolation in §5 is a bound, not a value.** Reading the residual non-flatness as a residual log over $\ln(M_Z^2/m_e^2)$ is deliberately the *pessimistic* reading — the measured $n$-dependence says it is grid noise, in which case the true lattice shift is smaller still. It is quoted as a ceiling on purpose.
* **$\alpha$ itself is not derived** (F127's four-avenue no-go). B9 was never a claim that it is.

## 10. Cross-references

[[F311-gap5-three-numbers-adjudicated]] · [[F251-qed-vacuum-polarization-running-alpha]] · [[F277-qed-gluon-refold-period]] · [[F261-twoloop-qed-ae-amu]] · [[F272-bgfield-loop-refold-period]] · [[F267-walk-bz-measure-not-the-fft-cube]] · [[F115-coupling-magnitudes-running-rotor]] · [[F138-weinberg-gap-closure-4piv-matching]] · [[F231-weinberg-2over9-onshell-face-of-1over4]] · [[F127-alpha-em-derivation-four-avenue-nogo]] · [[F151-scheme-constant-determined]] / [[F152-ir-coupling-the-irface]] · `docs/status/completeness-2026-08-07.md` row B9 + gap #5(a) · `docs/status/completeness-2026-08-18.md` gap #4 + row H5 (ii) · `docs/theory/supersessions.yaml` S12
