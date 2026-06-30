# F199 — The angular self-duality $C/\lvert B\rvert=1/(2\cos\tfrac23)=0.63622$: the first-principles derivation is attempted along the full F176→F177→F179 program and **closes negative on three independent structural grounds** — there is no F92-analogue second relation ($Q$ is $\delta$-blind), the IR coupling does **not** cancel in the ratio (cubic = sea loop $O(\alpha^0)$, sextic = induced $O(\alpha^{\ge1})$), and the BPS wall degeneracy lands at $C/\lvert B\rvert=\tfrac12$ not $0.636$; with the exact $3\delta=\pi/4$ massless anchor recovered, the self-duality is a **forced posit**, not a theorem

**Date:** 2026-06-30 - 18:55
**Numbering:** F196 is the latest committed finding; F197 + F198 were taken by concurrent sessions (first-excitation dark sector; E_g relic misalignment) during this work — this is **F199** (re-checked at write time).
**Status:** Confirmed (honest terminus, negative) — 5/5 checks PASS. **What this does:** it executes the deferred *angular* half of the saturation self-duality (the "$3\delta^*=Q$" of F176, the open angular budget of F177, the un-performed sextic solve of F179) and reports the outcome without overclaiming. The headline is a **three-way structural no-go** that pins down *why* the angle is not derivable, each part sharper than the prior record: **(S1)** the F92 *radial* derivation worked because two independently-derived mass laws intersect at a unique angle; the angular problem has **no such second relation** — the Koide ratio $Q=\tfrac13+\tfrac16 r^2$ is **exactly $\delta$-independent** (radial), so nothing kinematic forces $3\delta=Q$ (sympy-exact, $\partial Q/\partial\delta\equiv0$). **(S2)** The decisive algebraic question of the program — does the IR coupling $\alpha_\text{eff}^*$ **cancel** in $C/\lvert B\rvert$? — is answered **no**, and structurally: the cubic $B$ is a **parameter-free Dirac-sea loop** ($O(\alpha^0)$, F95), the sextic $C=\lambda_6e^6$ is an **induced** condensate self-coupling ($O(\alpha^{\ge1})$, F145/F118), so their ratio carries $\alpha_\text{eff}^*$ undiluted and is a **computed nonperturbative number**, never an $\alpha$-independent theorem. The bare Fierz rational $\lambda_6=\tfrac29$ gives $C/\lvert B\rvert=0.582$ (not $0.636$), requiring a $1.094\times$ uncomputed IR enhancement. **(S3)** Standard BPS (F177-B2) is made **quantitative**: the only ratio the wall/bulk structure selects is the tetragonal→orthorhombic vacuum-existence threshold $C/\lvert B\rvert=\tfrac12$ (degeneracy $V_0-V_\text{int}=(2C-\lvert B\rvert)^2/4C$), and $\tfrac12\neq0.636$. **The necessary boundary condition passes exactly:** $m_e\to0$ + Koide $\Rightarrow3\delta=\pi/4$ (sympy-exact). **Value discrimination:** the data invariant sits at the self-dual $0.63622$ to $1\times10^{-5}$ ($0.89\sigma$, Koide-class) and *not* at $2/\pi$; but the **derivation** lands off **both** by $\sim9\%$, so it cannot discriminate — confirming the value is computed and the self-duality must be **posited**. **No new physics introduced to close the angle; the negative result is the deliverable.**
**Module:** (analysis-only; sympy exact algebra + real arithmetic; reuses F95/F118/F145/F176 closed forms and PDG masses — no chiral transforms)
**Script:** `tests/findings/test_F199_angular_self_duality_derivation.py` (~2 s, sympy + stdlib + real arithmetic only)
**Results:** `test-results/F199_angular_self_duality.json`
**Cross-references:** [[F176-saturation-self-duality-principle]] (the principle $3\delta^*=Q$ this attempts to derive — confirmed a posit), [[F177-bps-self-duality-completion]] (the radial half *is* BPS-derived; this finding sharpens the angular half's three no-gos), [[F179-lambda6-derivation-attempt-and-relabel]] (the relabel this finding **completes** by performing the deferred structural solve: S1/S2/S3 are the *mechanisms* behind F179's "non-rational saturation normalization"), [[F92-per-constituent-phase-consistency]] (the radial derivation whose structure S1 shows has **no** angular twin), [[F96-second-shell-Eg-gap-saturation]] (the exact $\delta=15°$/$3\delta=\pi/4$ massless anchor recovered in A), [[F95-B-derived-C-localized]] (the derived $B$ = sea loop, $O(\alpha^0)$ — the load-bearing fact for S2), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] ($\lambda_6=0.243$, the $C=\lambda_6e^6$ localization and saturation-point values), [[F145-route-c-induced-njl-coupling]] (the induced-coupling Fierz $c=\tfrac29$, $O(\alpha^{\ge1})$ — the other load-bearing fact for S2), [[F172-residual-algebraic-or-computed]] (the algebraic-vs-computed fork — this lands it firmly on **computed**). External: Foot $45°$ circle geometry; Bogomolny/BPS domain walls (standard); $2/\pi$ quadrant-average competitor.

---

## 1. The one number, and what was already known

The charged-lepton shape sector reduces to one angular Landau potential (F93/F95/F118)

$$F(\delta)=B\cos3\delta+C\cos^23\delta,\qquad
\cos3\delta^*=-\frac{B}{2C}\ \ (\text{minimiser}),$$

with $B<0$ **derived** ($B=-3\sqrt2\,I_2\bar y^4$, F95) and $C=\lambda_6e^6>0$ the open coefficient. The empirical lepton spectrum fixes $\cos3\delta^*=0.785874$, i.e. $3\delta^*=0.666689\approx Q=\tfrac23$ — the saturation self-duality $3\delta^*=Q$ (F176), equivalent to

$$\frac{C}{\lvert B\rvert}=\frac{1}{2\cos\tfrac23}=0.63622 .$$

F176 **posited** this; F177 showed the **radial** half ($Q=\tfrac23$) is BPS-derived but the angular half is *not* a standard-Bogomolny theorem and equals the one shared residual; F179 **relabelled** the spectrum as a one-angle fit after the bracket rationals $\tfrac29,\tfrac14$ both missed the angle, but explicitly **did not perform** the saturated-condensate solve, the BPS degeneracy test, or the $0.63622$-vs-$2/\pi$ discrimination. This finding performs exactly those, and finds the structural reasons the angle is not derivable.

## 2. A — the anchor is recovered exactly (necessary boundary condition)

Any massless-electron texture $(m_h,m_\text{mid},0)$ obeys (F96, re-derived sympy-exact here) $Q=\frac{1+u^2}{(1+u)^2}$, $\tan\delta=\frac{\sqrt3\,u}{2-u}$ with $u=\sqrt{m_\text{mid}/m_h}$, and

$$Q=\tfrac23\iff u=2-\sqrt3\iff\delta=\frac{\pi}{12}=15°\iff\boxed{\,3\delta=\frac\pi4\,},\quad\cos3\delta=\tfrac1{\sqrt2}.$$

So the boundary condition the task requires is satisfied **exactly**: as $m_e\to0$ the angle returns to the exact $\pi/4$ anchor. The physical $\delta^*=12.733°$ is the displacement that $m_e>0$ induces off $15°$; the question is whether that displacement is forced to land at $3\delta=Q=\tfrac23$. (Note $\pi/4=0.7854\neq Q=0.6667$: the self-duality is a genuinely $m_e>0$ phenomenon, not the anchor.)

## 3. S1 — there is **no** second exact relation (the F92 analogue does not exist)

F92's radial lock is a real derivation because **two independently-derived mass laws** (pair-sum $m=\sin2t$ and bilinear $m=y^2$) intersect at a unique angle, $45°$. The angular problem needs the same shape: a second exact expression for $3\delta$, independent of "minimise the brake," that forces $3\delta=Q$ when equated to the minimiser.

**It does not exist, and the proof is one line of algebra.** With the Foot parametrisation $\sqrt{m_a}=\mu\,(1+r\cos(\delta+2\pi a/3))$:

$$\sum_a\sqrt{m_a}=3\mu,\qquad\sum_a m_a=\mu^2\Big(3+\tfrac32r^2\Big)\ \Rightarrow\
\boxed{\,Q=\frac13+\frac{r^2}{6}\,},\qquad\frac{\partial Q}{\partial\delta}\equiv0 .$$

$Q$ depends **only** on the radial amplitude ratio $r=A/\bar y$ (it is $\tfrac23$ iff $r=\sqrt2$, F92) and is **exactly blind to the angle** $\delta$. $Q$ is radial; $3\delta$ is the orthogonal angular coordinate on the same condensate circle. There is therefore **no kinematic intersection** to force their equality — the two invariants are independent coordinates, and $3\delta=Q$ equates a quantity fixed by the radius to a quantity fixed by the orientation. The only equation that fixes $\delta$ is the brake minimiser, which lives entirely in the dynamics ($B,C$), not the kinematics. **The conceptual core closes negative: the self-duality is not a second-relation theorem.**

## 4. S2 — $\alpha_\text{eff}^*$ does **not** cancel in $C/\lvert B\rvert$ (the decisive algebraic question)

The program's decisive question (F172/F177): does the nonperturbative IR coupling cancel in the ratio, making $C/\lvert B\rvert$ an algebraic number? **No — on structural grounds, because the two invariants arise at different orders in the coupling:**

| invariant | origin | coupling order |
|---|---|---|
| cubic $B=-3\sqrt2\,I_2\bar y^4$ | **Dirac-sea loop**, *parameter-free* — "no coupling enters the argmin" (F95 §1, D1–D4) | $O(\alpha^0)$ |
| sextic $C=\lambda_6e^6$ | **induced** $E_g$ clock self-coupling — gluon-exchange Fierz (F145), sea loop excluded by sign+scaling (F95/F118) | $O(\alpha^{\ge1})$ |

The ratio $C/\lvert B\rvert\propto\lambda_6\propto\alpha_\text{eff}^*$ therefore carries the IR coupling **undiluted** — there is nothing of the same order in $B$ to cancel against. So $C/\lvert B\rvert$ is a **computed nonperturbative number**, exactly F172's "computed" fork, and the self-duality cannot be an $\alpha$-independent theorem. (The task's hypothetical premise "since $B$ also carries it" is false: $B$ is the parameter-free sea cubic.)

**Numerically (F118 saturation-point values $\lvert B\rvert=0.0569$, $e^6=0.14897$):**

| $\lambda_6$ | source | $C/\lvert B\rvert$ | $\cos3\delta^*$ | $\delta^*$ |
|---|---|---|---|---|
| $\tfrac29=0.2222$ | Fierz (F145) | $0.5818$ | $0.8594$ | $10.25°$ |
| $0.243$ (fit, F118) | — | $0.6362$ | $0.7859$ | $12.73°$ |
| $\tfrac14=0.2500$ | rotor (F115) | $0.6545$ | $0.7639$ | $13.40°$ |

The bare induced rational $\tfrac29$ gives $C/\lvert B\rvert=0.582$, missing the self-dual $0.636$ and requiring a $0.63622/0.5818=\mathbf{1.094\times}$ uncomputed nonperturbative enhancement — the same single IR factor the F124/F144/F145/F151/F152 cluster carries. This is the *mechanism* behind F179's "non-rational saturation normalization": it is not a clean rational because it is an $O(\alpha)$ induced coupling divided by an $O(\alpha^0)$ loop.

## 5. S3 — the BPS wall degeneracy is at $C/\lvert B\rvert=\tfrac12$, not $0.636$

F177-B2 stated qualitatively that Bogomolny fixes wall tension, not the vacuum angle. Made quantitative here. Writing $V(x)=Bx+Cx^2$ with $x=\cos3\delta$, $B=-\lvert B\rvert$, $C>0$: the interior (orthorhombic) vacuum is $x^*=\lvert B\rvert/2C$, which requires $x^*<1$, i.e. $C/\lvert B\rvert>\tfrac12$. The energy gap to the symmetric ($\delta=0$, tetragonal) point is (sympy-exact)

$$V(\delta{=}0)-V(\text{interior})=\frac{(2C-\lvert B\rvert)^2}{4C}\ \ge0,\quad=0\ \text{iff}\ \frac{C}{\lvert B\rvert}=\frac12 .$$

So the **only** special ratio the wall/bulk structure picks out is the **vacuum-existence threshold $C/\lvert B\rvert=\tfrac12$** (where the interior vacuum is born out of the symmetric point and the three $C_3$-image walls first appear). For every $C/\lvert B\rvert>\tfrac12$ the interior vacuum is strictly global and the walls exist, but the vacuum **angle** $\arccos(\lvert B\rvert/2C)$ is left completely free. Since $0.636\neq0.5$, the BPS structure does **not** pin the self-dual value. Step 3 closes negative.

## 6. V — value discrimination: data at the target, derivation off both

The self-dual $1/(2\cos\tfrac23)=0.63622$ and the quadrant-average competitor $2/\pi=0.63662$ differ by $4.0\times10^{-4}$.

- **The data invariant** sits at $C/\lvert B\rvert=0.63623$ — matching the self-dual value to $1\times10^{-5}$ ($0.89\sigma$ of the PDG $m_\tau$ error, the **same confidence class as Koide**) and **not** at $2/\pi$ (off by $4\times10^{-4}$). This is the F176/F179 *target*, re-confirmed: the physical condensate **does** obey $3\delta^*=Q$.
- **The derivation** (bare induced Fierz $\tfrac29$) lands at $C/\lvert B\rvert=0.582$ — off **both** candidates by $\sim9\%$ ($\gg10^{-4}$). It cannot discriminate $0.63622$ from $0.63662$; only the **fitted** $\lambda_6=0.243$ reaches the target.

Per the task's own criterion this is the **"converges off both"** outcome: $C/\lvert B\rvert$ is a genuinely computed nonperturbative number, and the self-duality must be **posited**, not derived. The honest terminus.

## 7. Verdict — forced posit, on three independent grounds

| step | question | result |
|---|---|---|
| A (anchor) | $m_e\to0\Rightarrow3\delta=\pi/4$? | **yes, exact** (necessary BC met) |
| S1 | second exact relation forcing $3\delta=Q$? | **no** — $Q$ is $\delta$-blind ($\partial Q/\partial\delta\equiv0$); no F92 analogue |
| S2 | $\alpha_\text{eff}^*$ cancels in $C/\lvert B\rvert$? | **no** — cubic $O(\alpha^0)$ sea, sextic $O(\alpha^{\ge1})$ induced; computed number |
| S3 | BPS wall/bulk degeneracy at $0.636$? | **no** — only at the threshold $C/\lvert B\rvert=\tfrac12$ |
| V | derivation predicts $0.63622$ vs $2/\pi$? | **neither** — off both by $9\%$; data at target only by fit |

The angular self-duality $3\delta^*=Q$ — equivalently $C/\lvert B\rvert=0.63622$ — is a **forced posit**. It is a real, currently-satisfied, Koide-confidence relation (the data obey it to $0.89\sigma$), motivated by the BPS/saturation picture, but it is **not derivable** from the existing structure: there is no kinematic second relation, the dynamical ratio is intrinsically $\alpha$-dependent (computed, not algebraic), and the BPS wall does not pin it. This is consistent with F176 (posit), F177 (half-derived, angular half = the shared residual), and F179 (relabel) — and **completes** them by exhibiting the three structural mechanisms behind the negative.

## 8. What this settles, and the residual (unchanged in kind)

**Settled:** the three open sub-questions F179 deferred are answered — (S1) no second relation exists, (S2) the IR coupling does not cancel so $C/\lvert B\rvert$ is computed, (S3) the BPS degeneracy is at $\tfrac12$ not $0.636$; and the necessary $\pi/4$ anchor is recovered exactly. The self-duality's epistemic status is now fully pinned: **posit with a Koide-confidence rationale, structurally proven non-derivable by the available routes.**

**Residual (the same single object as ever):** the one nonperturbative IR-coupling normalisation at the saturation/confinement scale (F124/F144/F145/F151/F152). Whichever computation delivers $\alpha_\text{eff}^*$ delivers $\lambda_6$, hence $C/\lvert B\rvert$, hence a *derivation-or-refutation* of the self-dual $0.63622$. The deepest open lepton-sector statement is therefore unchanged and sharp: **compute $\alpha_\text{eff}^*$ at saturation; the self-dual value $1/(2\cos\tfrac23)=0.63622$ is the prediction it must hit (to $\le10^{-4}$, against the $2/\pi$ alternative).**

## 9. Check summary (`test_F199_angular_self_duality_derivation.py`, 2026-06-30 - 18:52)

| Check | Statement | Tier | Result |
|---|---|---|---|
| A | massless Koide $\Rightarrow3\delta=\pi/4$ (sympy: $\delta=\pi/12$, $\cos3\delta=1/\sqrt2$) | exact / anchor | PASS |
| S1 | $Q=\tfrac13+\tfrac16r^2$, $\partial Q/\partial\delta\equiv0$; no second relation | exact / negative | PASS |
| S2 | cubic $O(\alpha^0)$ vs sextic $O(\alpha^{\ge1})$ $\Rightarrow$ no cancellation; bare $\tfrac29\to0.582$, needs $1.094\times$ | structural / negative | PASS |
| S3 | wall degeneracy $(2C-\lvert B\rvert)^2/4C$ at $C/\lvert B\rvert=\tfrac12\neq0.636$ | exact / negative | PASS |
| V | data at self-dual to $1\times10^{-5}$ ($0.89\sigma$), not $2/\pi$; derivation off both by $9\%$ | discrimination | PASS |

**Overall 5/5 PASS** (~2 s, sympy + real arithmetic only — numpy-safe).

## 10. Provenance

- **New content:** the proof that no second exact angular relation exists ($Q$ exactly $\delta$-independent, S1); the structural answer to the $\alpha$-cancellation question (different coupling orders of $B$ vs $C$, S2) and its numerical enhancement factor $1.094\times$; the quantitative BPS degeneracy at $C/\lvert B\rvert=\tfrac12$ (S3); the exact $\pi/4$ anchor recovery (A); and the explicit $0.63622$-vs-$2/\pi$ value discrimination (V).
- **Reused:** F96 massless texture algebra; F92 Foot/equipartition $Q=\tfrac23$; F95 derived sea-loop $B$ (parameter-free); F118 $\lambda_6=0.243$ and saturation-point $(\lvert B\rvert,e^6)$; F145 induced Fierz $c=\tfrac29$; F176 self-duality principle; F177 BPS analysis; F179 relabel; PDG masses ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86\pm0.12$ MeV).
- **Verification:** `tests/findings/test_F199_angular_self_duality_derivation.py` (2026-06-30 - 18:52, 5/5 PASS), results `test-results/F199_angular_self_duality.json`. Real arithmetic + sympy only — no chiral transforms, numpy-safe.
