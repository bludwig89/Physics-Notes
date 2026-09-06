# F345 — Rubric E1 narrowed: at two-derivative order the left-hand side is forced by Lanczos–Bach in the model's derived $d=3+1$, the full-tensor source is forced by the metric variation itself, and two further alternative families are absent for want of a parameter

*2026-09-01 - 15:13 · sector `interactions` · module `casim.engine.interactions.gravity_field_equation_uniqueness` · test record `F345-field-equation-uniqueness` (8/8 PASS, gate tier, 3 controls verified RED, no spill) · results `test-results/F345_field_equation_uniqueness.json`*

**Checked:** 2026-09-01 — **INCONCLUSIVE** — the cold-subagent review was attempted and **cut off mid-run by an API spend limit**; the blind re-derivation was never obtained. 5 PASS / 1 WEAKENS / 0 FAIL / 7 NOT RUN, and the attacks that did run were run by this authoring session, which is not independent. **Treat this finding as UNREVIEWED** ([review record, with the two resumable agent ids](../docs/reviews/F345-review-2026-09-01.md)). — *SUPERSEDED by the line below; kept as the record of the interrupted run, per the review protocol's append rule.*
**Reviewed:** 2026-09-01 — **CONFIRMED-NARROWER** — both cold agents were **resumed and completed**; 3 PASS / 8 WEAKENS / 0 FAIL. The mathematical core is confirmed and the $d=4$ identity was verified **fully symbolically** by the referee, beyond what this finding sampled. Four corrections were required and are applied below: "$a$ is fixed" withdrawn, L4's bound restated, L5/L6 demoted from "closed" to "absent for want of a parameter", and the Vermeil-Weyl pincer on the headline acknowledged ([completed review](../docs/reviews/F345-review-2026-09-01-b.md)).

**Target.** Rubric row **E1** (`POSIT`) in `docs/status/completeness-2026-08-20.md`, ledger row **E1g** in `docs/status/open-derivations.md` **Part C**:

> **The induced Einstein equation** $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ as the fundamental field equation; the $K=\exp(2GM/rc^2)$ dielectric is its vacuum/weak-field representation — **DECISION 2026-06-29** (F178). Alternatives genuinely closed: the energy-only law is not Lorentz covariant and has no NS maximum mass. **Independently confirmed since**: F297's BBN gives the demoted law $Y_p=0.1856$, $-17.6\sigma$.

**What this finding does NOT do.** It does not re-attack the energy-only law. That alternative is closed three times over — Lorentz covariance and the absent neutron-star maximum mass (F178), and independently on an unrelated observable by F297's BBN — and is carried here as established, exactly as Part C's protocol requires.

**The question it asks instead.** The decision note gives three reasons for adopting the law and none for the *form* of the left-hand side. It was written 2026-06-29. Since then the tree has acquired **F319** (2026-08-16, the Wilsonian/EFT reading of the Brillouin-zone cutoff, with an exact-rational dimension-6 leading irrelevant operator), **F326** (2026-08-20, the "+1" closed), **F288** (zero slip, $\mu\equiv1$ with $\partial_k\mu\equiv0$, $\dot G/G\equiv0$, and *no screening mechanism*) and **F309** ($g_*$ derived). So: **how much of the field equation is still posited, given content that did not exist when it was posited?**

The answer is: less than the row says, and the part that remains is a different statement from the one the row names.

---

## 1. The shape of the argument

Write the induced long-wavelength effective action for whatever metric-like object the coarse-grained lattice carries,

$$W[g] \;=\; \int\!\sqrt{-g}\,\Big[\tfrac{1}{16\pi G}\big(R-2\Lambda\big) \;+\; \underbrace{c_1 a^2\,\mathcal{R}^2 + \dots}_{\text{F319's irrelevant tower}}\Big] \;+\; S_\text{matter}[g,\psi],$$

and ask what the stationarity condition $\delta W/\delta g^{\mu\nu}=0$ can possibly be. Five separate facts fix it, and only one premise is left over.

| | Statement | Where it comes from | Leg |
|---|---|---|---|
| (i) | the source of a metric field equation is a **conserved symmetric 2-tensor** | Bianchi identity — an identity of the geometry | **L1** exact |
| (ii) | it is the **full** $T_{\mu\nu}$, all ten components, **by construction** | the metric variation *is* $T_{\mu\nu}$ | **L2** exact |
| (iii) | its conservation is **not an extra condition** — it *is* the matter field equation | Noether / diffeomorphism invariance | **L2b** exact |
| (iv) | the left side is $aG_{\mu\nu}+bg_{\mu\nu}$ and **nothing else** *at two-derivative order* | Lanczos–Bach / Lovelock, in the model's own **derived** $d=4$ — but see the pincer in §4 | **L3** exact |
| (v) | $a$ is **adopted**, not fixed — and the four-derivative tower is suppressed by $\sim10^{-76}\times$ an **uncomputed** $O(1)$ | F79/F107 adoption; F59 does **not** close the coefficient (see §5) | **L4** order-of-magnitude |

**(iv) and (v) are not independent, and the original version of this finding wrongly presented them as two of five separate facts.** Divergence-freedom does *not* exclude higher-derivative terms: any $E_{\mu\nu}$ derived from a local diffeomorphism-invariant action is identically conserved by Noether, so $\nabla^\mu E_{\mu\nu}[R^2]\equiv0$ just as $\nabla^\mu G_{\mu\nu}\equiv0$ — verified mechanically by this finding's blind reviewer. The *only* thing that excludes $R^2$ is that $E_{\mu\nu}[R^2]$ depends on the metric 4-jet where $G_{\mu\nu}$ depends on the 2-jet. So the **at-most-second-order** premise is doing essential work, and (v) is the *size of the assumption (iv) needs* — not a separate result.

What is left over is stated in **L7**. The first version of this finding called it "a single sentence"; the completed review showed the honest count is **one premise plus two open sub-items inside it**.

---

## 2. L1 — the Bianchi identity constrains *any* source, before any physics

On the metric $ds^2=-e^{2f_0}dt^2+e^{2f_1}dx^2+e^{2f_2}dy^2+e^{2f_3}dz^2$ with four *arbitrary* functions $f_i(t,x)$ — inhomogeneous, anisotropic, time-dependent — sympy returns

$$\nabla^\mu G_{\mu\nu} = (0,0,0,0),\qquad \nabla^\mu g_{\mu\nu}=(0,0,0,0),$$

as **literal zeros**, on a family whose Ricci scalar is checked non-zero in the same call (so the zero is not vacuous).

*What this leg is and is not.* The Bianchi identity is a textbook theorem, not a result of this finding; the mechanical check is a **guard against a coding error** in this module's own tensor routines, which L3 then relies on. And the family is **diagonal**, so it does not realise the 4-distinct-index Riemann component ($R_{0123}\equiv0$ for any diagonal metric) — the check is an identity check on a restricted family, not on a fully general metric. Neither caveat threatens the corollary, which rests on the cited theorem. The *content* of L1 is the corollary, not the zero:

> **Any** local metric field equation $E_{\mu\nu}[g]=\kappa S_{\mu\nu}$ with $E_{\mu\nu}=aG_{\mu\nu}+bg_{\mu\nu}$ **forces** $\nabla^\mu S_{\mu\nu}=0$.

This is a stronger and structurally different statement from the covariance argument in F178's reason (1). F178 said a $T^{00}$-only source *is not a tensor equation*, which is an argument about frames. L1 says the geometry itself refuses any source that is not a conserved symmetric 2-tensor — a constraint on the *whole family*, delivered by an identity, with no appeal to boosts. The already-closed energy-only law is one member of that family; it is not this finding's subject.

## 3. L2 / L2b — the full-tensor source is not a choice

Two exact steps, deliberately separated so each is checked on its own:

**(a) the determinant identity.** With $g^{\mu\nu}$ carried as ten free symbols, brute-force differentiation of $\sqrt{-g}=(-\det g^{ab})^{-1/2}$ gives

$$\frac{\partial\sqrt{-g}}{\partial g^{\mu\nu}} = -\tfrac12\sqrt{-g}\,g_{\mu\nu}$$

for all ten components (sympy zero residual, no component excepted).

**(b) the stress tensor.** With (a), $T_{\mu\nu}=-2\,\partial\mathcal L/\partial g^{\mu\nu}+g_{\mu\nu}\mathcal L$, evaluated on two Lagrangians:

| matter | recovered $T_{\mu\nu}$ | symmetric | independent components |
|---|---|---|---|
| massless scalar, $\mathcal L=-\tfrac12 g^{ab}\partial_a\phi\,\partial_b\phi$ | $\partial_\mu\phi\,\partial_\nu\phi-\tfrac12 g_{\mu\nu}(\partial\phi)^2$ | ✓ exact | **10** |
| Maxwell, $\mathcal L=-\tfrac14 F_{ab}F^{ab}$ — the model's photon sector (F69) | $F_{\mu\alpha}F_\nu{}^\alpha-\tfrac14 g_{\mu\nu}F^2$ | ✓ exact | 10 |

The point is the component count, not the textbook match. A metric variation returns a symmetric rank-2 object with **ten** components; there is no variational route to a source with fewer. A one-component source leaves **nine** of the ten unspecified, and $G_{\mu\nu}$ has ten components with four Bianchi identities among them — so a scalar source under-determines the geometry by five functions. That is a *counting* fact about the variational principle, independent of any frame argument.

**L2b** closes the loop: on the same generic metric,

$$\nabla^\mu T_{\mu\nu} \;=\; (\Box\phi)\,\partial_\nu\phi \qquad\text{identically,}$$

so (i)'s constraint $\nabla^\mu S_{\mu\nu}=0$ is *satisfied exactly when the matter field equation holds* — it is not an extra assumption bolted onto the gravity sector. The same call verifies the divergence is **not** identically zero off-shell, so the identity has content.

## 4. L3 — the load-bearing new step: uniqueness is *inherited* from a derived dimension

Lovelock's theorem (Lovelock 1971) says: in $d=4$, the only symmetric, divergence-free rank-2 tensor built locally from the metric and its derivatives to second order is $aG_{\mu\nu}+bg_{\mu\nu}$. In $d>4$ it is not — the Gauss–Bonnet term contributes, and Einstein–Gauss–Bonnet is an equally admissible field equation.

**A grep is the evidence this route has never been taken here.** `lovelock` returns *nothing* in `findings/`, `docs/`, `papers/` or `src/` before this finding. The tree has a Sakharov induced-EH coefficient (F56/F57/F59), a Wilsonian cutoff (F319), and a derived spacetime dimension (F291/F326) — and has never joined them.

The test is deliberately stronger than a metric ansatz. Rather than checking one metric family, it builds a **generic algebraic curvature tensor** on flat $\eta_{ab}$ as a random rational combination of 24 Kulkarni–Nomizu squares of symmetric forms. By Fiedler's theorem every algebraic curvature tensor is such a combination, so this realises an *arbitrary* Riemann tensor at a point (normal coordinates) with every algebraic symmetry, first Bianchi included — verified in the same call. Then the Lanczos–Lovelock tensor

$$H_{\mu\nu}=2\big[R R_{\mu\nu}-2R_{\mu\alpha}R^\alpha{}_\nu-2R_{\mu\alpha\nu\beta}R^{\alpha\beta}+R_\mu{}^{\alpha\beta\gamma}R_{\nu\alpha\beta\gamma}\big]-\tfrac12 g_{\mu\nu}\mathcal{G},\qquad \mathcal{G}=R^2-4R_{\alpha\beta}R^{\alpha\beta}+R_{\alpha\beta\gamma\delta}R^{\alpha\beta\gamma\delta}$$

is computed in exact rationals:

| | Gauss–Bonnet **scalar** $\mathcal{G}$ | $H_{\mu\nu}$ |
|---|---|---|
| $d=4$, seed 11 | $-4265944095197/1190700000 \neq 0$ | **all 16 components exactly 0** |
| $d=4$, seed 12 | $223922549947/37800000\neq0$ | **all 16 components exactly 0** |
| $d=5$, seed 11 | $\neq0$ | **25 components non-zero** |

The contrast inside $d=4$ is the content: the GB *scalar* is a perfectly ordinary non-zero number while its *variation* vanishes identically. So the leading curvature-squared correction — the one term that would otherwise spoil (iv) at the first order that matters — is **topological in four dimensions and only in four dimensions**.

**The pincer on this headline — put here because it is the sharpest objection to it.** Uniqueness of $aG_{\mu\nu}+bg_{\mu\nu}$ among tensors **linear in $\partial^2 g$** is Vermeil (1917) / Weyl (1922) / Cartan (1922), and it holds in **every** dimension. So the dimension-dependence above is not a property of "the field equation" as such — it is a consequence of *which theorem one invokes*:

- **grant linearity in $\partial^2g$** → uniqueness is dimension-**independent**, and the model's derived $d$ does **no work** for this result;
- **drop linearity** (the honest choice for a derivative expansion, and the choice made here) → Lovelock applies and the dimension does the work, but then the **at-most-second-order** premise becomes essential and is only satisfied to the accuracy §5 quantifies.

Either horn narrows the headline. What survives on the second horn — the one this finding takes — is the statement below, and nothing wider.

*Attribution.* The $d=4$ vanishing of the Gauss–Bonnet variation is properly the **Lanczos–Bach identity** (Lanczos 1932/1938); Lovelock's contribution is the general classification and, in particular, [*The Four-Dimensionality of Space and the Einstein Tensor*, J. Math. Phys. **13**, 874 (1972)](https://ui.adsabs.harvard.edu/abs/1972JMP....13..874L/abstract) — the paper whose title is this finding's own headline, and which the first version of this finding failed to cite. The thermodynamic route to the same Lanczos–Lovelock class is Padmanabhan, hep-th/0607240 (2006): **this argument is prior art in the literature, and is novel only within this repository.**

*Strengthened since first issue.* The finding's own check sampled 24 random tensors. The adversarial reviewer went further and verified $H_{\mu\nu}\equiv0$ in $d=4$ **fully symbolically** in 20 free symbols, with the Gauss–Bonnet scalar $\not\equiv0$, and swept 48 configurations including `n_terms=1` — a rank-degenerate, deliberately *non*-generic tensor. So the identity is **confirmed, not sampled**, and the Fiedler/genericity framing is needed only for the $d=5$ converse, not for the $d=4$ zero.

*One loophole, closed.* The "4D Einstein–Gauss–Bonnet" programme rescales $\alpha\to\alpha/(D-4)$ and takes $D\to4$ to retain a Gauss–Bonnet contribution. It is not a counterexample: the rescaled field equations are not well defined for arbitrary metrics (Gürses–Şişman–Tekin; Shu, arXiv:2004.09339), and the surviving regularizations yield a scalar-tensor Horndeski theory — an **extra field**, excluded here by the metric-only premise rather than by this result.

**Why the derived dimension matters here specifically.** The model does not assume $d=4$. **F291** fixes $d_\text{space}=3$ by two independent selectors; **F326** closes the residual "+1" (no second candidate generator exists to close it against). So:

> Einstein uniqueness in this model is not an extra postulate about gravity. It is **inherited** from the already-derived spacetime dimension. In a $d=5$ version of this same lattice, the field equation would *not* be forced, and Einstein–Gauss–Bonnet would be admissible.

That converts F291/F326 from results adjacent to the gravity sector into results **load-bearing for E1**, which no finding had noticed.

## 5. L4 — the two-derivative truncation: a decade, not a bound

**This section was wrong in the first version of this finding and is restated.** It claimed $\varepsilon\le1.4\times10^{-76}$ as an upper bound, sourced to "F319's dimension-6 leading irrelevant operator with an exact rational coefficient." Three separate errors, all found by the cold review:

1. **F319 does not supply the coefficient.** F319's exact rational dimension-6 coefficient is the **photon-dispersion** one, and F319's own caveat says verbatim that other dimension-6 operators "are not computed here … the coefficients are not measured." There is **no gravitational curvature-squared Wilson coefficient anywhere in the tree.** The number below therefore carries an **uncomputed $O(1)$ factor**, and citing F319 for it was an over-extension of a finding into a sector it explicitly disclaims.
2. **The wrong invariant.** At a Schwarzschild horizon $R=R_{\mu\nu}=0$ identically, so $a^2R=0$; the invariant the four-derivative operators actually contain is $R_{\alpha\beta\gamma\delta}R^{\alpha\beta\gamma\delta}$, giving $\sqrt{K}=\sqrt{12}/r_s^2$ — a factor $\sqrt{12}=3.464$ larger, confirmed to four digits by both reviewers independently.
3. **The wrong extremum.** $\varepsilon\propto1/M^2$, so the **lightest** compact object sets the scale, not the most spectacular event. At $2.6\,M_\odot$ the proxy gives $6.68\times10^{-76}$ — **4.6× the figure claimed as a bound.**

And a fourth point, which cuts the other way and was raised by the referee against the reviewers' own correction: in **4D vacuum** the four-derivative sector is Gauss–Bonnet (topological, by §4) plus $R^2$ and $R_{\mu\nu}R^{\mu\nu}$, which are **removable by the standard EFT field redefinition** $g_{\mu\nu}\to g_{\mu\nu}+\alpha R_{\mu\nu}+\beta Rg_{\mu\nu}$. If that is right, the leading genuine correction at a vacuum horizon is *six*-derivative, $\sim(a/L)^4\sim10^{-152}$, and the vacuum-horizon rows below are a **proxy that does not carry the leading effect** — the regimes where four-derivative operators genuinely contribute are the **matter** ones. The referee flagged this sub-point as standard EFT lore for which it landed no confirming citation in-session, so it is recorded as indicative rather than settled.

The table, with the invariant now named per row and the model-internal row labelled as such ($a=1.0664\times10^{-34}$ m, F107):

| regime | invariant | $\varepsilon$ |
|---|---|---|
| Mercury's orbit (Sun) | $a^2r_s/r^3$ proxy | $1.73\times10^{-97}$ |
| neutron-star surface — **model-internal** (F184: $2.08\,M_\odot$, $R=11.1$ km, not a measurement) | $a^2r_s/r^3$ proxy | $5.11\times10^{-77}$ |
| **matter regime, NS mean density** | $8\pi Ga^2\bar\rho/c^2$ | $\sim2\times10^{-76}$ |
| stellar black-hole horizon, $3\,M_\odot$ (a *representative*, not its class's extremum) | $a^2r_s/r^3$ proxy | $1.45\times10^{-76}$ |
| lightest compact remnant, $\sim2.6\,M_\odot$ | $a^2\sqrt{K}$ | $6.68\times10^{-76}$ |
| Sgr A\* horizon | $a^2r_s/r^3$ proxy | $7.06\times10^{-89}$ |
| M87\* horizon | $a^2r_s/r^3$ proxy | $3.08\times10^{-95}$ |
| BBN, $T=10$ MeV ($g_*=10.749339$, F309) | $a^2H^2/c^2$ | $5.80\times10^{-82}$ |

A result worth keeping from the recomputation: **compact objects beat the early universe by about ten decades.** The earliest epoch any observation anchors is BBN, where $a^2H^2/c^2\approx6\times10^{-86}$; a $\sim3\,M_\odot$ horizon exceeds that by ten orders of magnitude, because $1/r_s^2$ for a 9 km horizon dwarfs $H^2/c^2$ at BBN.

**The honest statement, which is what this leg now claims:**

> the four-derivative correction is $\sim10^{-76}\times O(1)$, with the **decade robust** and nothing finer supportable — because the $O(1)$ gravitational Wilson coefficient is not computed anywhere in this model, the choice of invariant moves the figure by $3.5\times$, and which object counts as "reached by observation" moves it by another $\sim5\times$.

That is still 76 orders of magnitude of headroom, which is all the two-derivative truncation actually needs. But it is a decade estimate, not a bound, and it should never have been written as "$\le$".

*Scope note, so two numbers are not compared by mistake:* for the **matter**-sector dimension-6 operators F319 gives $3.0\times10^{-31}$ at LHC energies — 45 decades larger. The $10^{-76}$ here is specific to the *gravitational field equation*, where the expansion parameter is a curvature radius rather than a collision energy.

## 6. L5 / L6 — two further alternative families, **absent for want of a parameter**

**The first version of this finding said these families were "closed by the model's own structure … a different and stronger thing than being disfavoured by a bound." The comparative was wrong and the verb was too strong.** It is a *different* thing, not a *stronger* one, and the honest verb is **absent**, not **closed**. Two concessions come first, because they bound everything that follows.

**Concession 1 — the premise is downstream of the adopted law.** The four exact zeros below come from $AB\equiv1$ (F64 D-EM9) and the F106 reduction. `docs/theory/supersessions.yaml` `S4-F178-full-stress-energy` **reclassifies both F64 and F106** as the static/weak-field representation of the very Einstein equation under question. So as an *exclusion of a rival field equation* this argument is partly circular: it reduces to "our adopted field equation is not Brans–Dicke's field equation," which is true and thin. What the legs do establish is the **parameter content** of the model as adopted — and that is a real and checkable fact, just a narrower one.

**Concession 2 — neither family is refuted.** A Brans–Dicke theory with $\omega=10^{40}$, or an $f(R)$ with a Planckian scalaron, is observationally identical to this model and internally consistent. Nothing here rules those out. The model simply **contains no parameter with which to build one**.

**Taxonomy, which matters for reading the premise.** In Will's PPN classification **Brans–Dicke *is* a metric theory** — matter couples minimally to one metric. So "an emergent local, diffeomorphism-invariant metric theory" does **not** by itself exclude it. What excludes it is the stronger reading, **$g_{\mu\nu}$ is the only long-wavelength gravitational degree of freedom** ("metric-only on the left-hand side" in §7's premise list). That stronger reading is the one this finding intends, and saying so is not optional: under the weaker reading L5 is answered by hypothesis and is not a result at all.

### L5 — scalar-tensor / Brans–Dicke

Brans–Dicke needs $\gamma_\text{BD}=(1+\omega)/(2+\omega)$. Sympy returns **no finite $\omega$** solving $\gamma_\text{BD}=1$; the value is reached only as $\omega\to\infty$, the scalar decoupling. Cassini alone ($|\gamma-1|<2.3\times10^{-5}$) requires only $\omega>4.35\times10^4$ — a bound with room left. The model sits exactly at the decoupling point:

| signature | Brans–Dicke | this model | source | status of that source |
|---|---|---|---|---|
| PPN $\gamma$ | $\neq1$ for any finite $\omega$ | $=1$ **exactly** | $AB\equiv1$ (F64 D-EM9) | reclassified by `S4-F178` |
| linear slip $\Sigma-1$ | non-zero | sympy **literal 0** | $AB\equiv1$ (F288 S1) | ← same premise as above |
| $\partial\mu/\partial k$ | non-zero | sympy **literal 0**, $\mu\equiv1$ | F106 reduction (F288 S2) | reclassified by `S4-F178` |
| $\dot G/G$ | non-zero | **identically 0** (vs LLR $(7.1\pm7.6)\times10^{-14}\,\text{yr}^{-1}$) | rigid substrate (F79/F284) | independent of F64/F106 |

Note honestly that the first three share one premise, so "three independent structural sources" — which the module still reports as a hardcoded integer, and which the first version of this finding presented as content — overstates the independence. Only $\dot G/G$ is genuinely independent of the $AB\equiv1$ / F106 pair.

**Where the model is strongest, and it is not the PPN number.** The blind reviewer identified a sharper leg than any in the original: by F79 S3 the source-free EM stress tensor is **traceless in 3+1D**, so the conformal factor $\sigma=\tfrac12\ln K$ — the very object that would play Brans–Dicke's $\varphi$ — has **no source and no tree action**; its entire stiffness is the induced Einstein–Hilbert term. There is no kinetic term for a Brans–Dicke scalar because **there is no independent gravitational scalar at all**: $K$ is a reparametrisation of the $(\mathbf E,\mathbf B)$ rotation rule, not a field. That is the argument this leg should have led with.

### L6 — $f(R)$

Metric $f(R)$ in the Einstein frame is Brans–Dicke with $\omega=0$, hence $\gamma_{f(R)}=\tfrac12$ in the massless/unscreened limit — off Cassini by $2.17\times10^4$. Its escape is a **chameleon**, which needs a $k$-dependent $\mu(k,a)$; F288 S2 computes $\partial\mu/\partial k$ as a sympy literal zero and states the consequence: "the model has no screening mechanism." So both branches are unavailable — subject to Concessions 1 and 2, and to the limitation below.

### What these two legs do **not** touch

Named explicitly, because §7's "metric-only on the left-hand side" premise is only as closed as this list is short:

- **Vainshtein-screened Horndeski.** F288's $\partial_k\mu\equiv0$ is a statement about **linear** theory; Vainshtein screening is intrinsically non-linear and cannot show up in $\mu(k,a)$ at all. Untouched.
- **Vector-tensor** theories (Einstein-aether, TeVeS) and **bimetric** theories. Untouched.

So the metric-only premise is closed for Brans–Dicke and metric $f(R)$, and open for everything else with an extra field. That is a narrower statement than "two families closed," and it is the accurate one.

## 7. L7 — the residual, stated honestly

**Derived, given the premise:** the source is a conserved symmetric 2-tensor; it is the full $T_{\mu\nu}$ with all ten components, by construction; and the left side is $aG_{\mu\nu}+bg_{\mu\nu}$ **at two-derivative order**, by Lanczos–Bach in the model's derived $d=4$ — with the pincer in §4 acknowledged.

**Not derived, and corrected since first issue:** $a$ itself. The first version said "$a$ is fixed by F59." That was wrong, and it is the one place this finding asserted something a cited finding contradicts in its own header. F59's header reads: *"Partial derivation … the absolute $O(1)$ prefactor is reduced to two standard inputs ($\eta$, $g_*$) and evaluates to $\approx1$ for minimal Weyl content — **suggestive, not proven**."* Its status table marks $\eta$ **imported** and $g_*$ **assumed**, and its caveats name an **unreconciled channel fork**: the Sakharov BZ channel gives $1/G\propto\sqrt d$ while F58's clock-rate-stiffness channel gives $1/G\propto1/d$ — opposite $d$-exponents. So:

> $a$ is **adopted** at the F79/F107 value (`S5-F107-canonical-ruler` — a convention plus a GRB gate). F59 reduces the induced Einstein–Hilbert coefficient to two standard inputs and does **not** close it. **No leg of this finding tests $a$**, and it should not be read as doing so.

**Still posited — one sentence:**

> that the long-wavelength description of the lattice is a **local, diffeomorphism-invariant metric theory at all** — i.e. that an emergent Lorentzian metric exists and carries the dynamics.

**That sentence is doing real work, so here is everything inside it.** In full, the premise is: the long-wavelength description is carried by a **metric** $g_{\mu\nu}$ (not an independent affine connection — the Palatini route is *not* covered by §4 and would have to be closed separately), of **Lorentzian signature**, with a connection that is **torsion-free** and **metric-compatible**, in a **local** functional, whose field equations are of **at most second order** in derivatives of the metric, and with **no fields other than the metric on the left-hand side**.

Two of those are load-bearing and **not closed**:

- **at-most-second-order** is not a premise the model satisfies exactly. It is routed through §5, i.e. it holds to $\sim10^{-76}\times O(1)$ with the $O(1)$ uncomputed.
- **metric-only on the left-hand side** is closed for Brans–Dicke and metric $f(R)$ only (§6), and open for Vainshtein-screened Horndeski, vector-tensor and bimetric theories.

So the honest count is **not one premise but one premise plus two open items inside it.**

**Also not derived, and deliberately unchanged:** $b$, the cosmological constant. Lovelock *permits* it; it does not fix it. **CL021** ("the cosmological constant is not derived") stands, and nothing here narrows it.

**Where this sits against the literature, which is not comfortable.** Sindoni's review of microscopic/emergent-gravity models (arXiv:1110.0686) states that the emergence of an effective Lorentzian spacetime is **"not generic"** — the generic infrared being Finsler or multi-metric — and that "in absence of strong symmetry arguments, the emergence of a theory as simple as Newtonian gravity can be hopeless." **This finding's single remaining posit is precisely the step that literature identifies as the hard one that generically fails**, and a lattice with a preferred rest frame is the canonical setting for that failure. That does not make the posit wrong. It does mean it is not a formality, and the phrase "the field equation is not a choice" borrows confidence the premise has not earned.

**What would finish E1.** A derivation that the model's blockspin / coarse-graining flow (F130) *drives* the long-wavelength effective action to a local diff-invariant metric functional, rather than that form being assumed. That is a statement about emergence, not about gravity, and on the literature above it is the substantive open problem rather than a technicality.

**Net effect on the row.** E1 stays **POSIT**. The posit's *content* shrinks from "the fundamental field equation" to "an emergent local, diff-invariant metric description exists, with second-order truncation and metric-only content as named sub-items." Two alternative families are **absent from the model's parameter content** — not refuted, and not independently excluded, since the premise supplying their absence is downstream of the adopted law.

## 8. Legs, exactness, controls

| Leg | Statement | Exactness | Verdict |
|---|---|---|---|
| L1 | $\nabla^\mu G_{\mu\nu}\equiv0$, $\nabla^\mu g_{\mu\nu}\equiv0$ | exact — but a **textbook identity**, checked as a guard against coding error, on a **diagonal** family ($R_{0123}\equiv0$) | PASS |
| L2 | determinant identity, all 10 components; $T_{\mu\nu}$ for scalar and Maxwell | exact | PASS |
| L2b | $\nabla^\mu T_{\mu\nu}\equiv(\Box\phi)\partial_\nu\phi$; non-zero off-shell | exact | PASS |
| L3 | $H_{\mu\nu}\equiv0$ in $d=4$, $\neq0$ in $d=5$ | exact — and verified **symbolically** by the reviewer, stronger than the sampling here. Subject to the §4 pincer | PASS |
| L4 | $\sim10^{-76}\times$ an **uncomputed** $O(1)$ | **order-of-magnitude, not a bound** — restated; **not independent of L3** | PASS as restated |
| L5 | no finite $\omega$ gives $\gamma=1$; the model has no independent gravitational scalar | exact algebra over an **assumed input** ($\gamma=1$ typed, not computed); premise downstream of the adopted law | PASS as narrowed |
| L6 | $\gamma_{f(R)}=\tfrac12$; no screening mechanism to host a chameleon | as L5 | PASS as narrowed |
| L7 | the residual premise plus its **two open sub-items**; $\Lambda$ permitted-not-fixed; $a$ adopted-not-fixed | structural | PASS |

**Known test weaknesses, recorded rather than hidden.** Of the 11 test functions, 8 check identities or module-hardcoded integers; the L4 assertion is `worst_epsilon < 1e-60` against a claimed $10^{-76}$ — sixteen decades of slack, so it would pass if the figure were wrong by $10^{15}$. Only the three declared controls go red on anything but a coding error. The record's `expect.exactness: exact` does not describe a payload with a `computed` L4 and a `structural` L7. Tightening the L4 assertion and re-tiering the record are handed on as follow-ups.

**Controls** (D9/H2, all three verified RED with no spill):

| Perturbation | Reddens | Why it is the right control |
|---|---|---|
| `lovelock_dim=5` | L3 | the same code in five dimensions returns 25 non-zero components — the zero is about the **dimension**, not the contraction routine, which is what makes F291/F326 load-bearing |
| `gb_ricci_coeff=-3` | L3 | the $-4$ in $R^2-4R_{ab}R^{ab}+\text{Riem}^2$ is what makes the variation topological; perturbing it alone breaks the identity |
| `model_gamma=0.999999` | L5 | a $\gamma$ that is 1 to six digits admits a finite Brans–Dicke $\omega$ — the closure comes from **exactness**, not from Cassini |

**Test record:** `F345-field-equation-uniqueness` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`).
**Claim:** `CL292` — see `docs/claims/CL292-einstein-uniqueness-inherited-from-derived-dimension.md`.

**Cross-references:** [[F178-gravity-full-tensor-adoption]] (the decision this narrows, not re-opens), [[F297-bbn-light-element-abundances]] (the independent confirmation, carried), [[F59-induced-eh-prefactor-and-f10-selection]] (the induced-EH coefficient that supplies $a$), [[F319-uv-sector-reconciled-physical-cutoff-and-counterterms]] (the dimension-6 operator behind L4 — post-decision content), [[F288-structure-formation-zero-free-functions]] (the four structural zeros behind L5/L6), [[F291-why-three-plus-one-dimensions]] / [[F326-the-plus-one-closes-no-second-generator]] (the derived $d$ that L3 inherits from), [[F79-structural-newton-constant]] / [[F107-canonical-a-adoption-L4-grb-gate]] (structural $G$, the cell), [[F64-em-connection-gravity]] ($AB\equiv1$), [[F106-psi-K-sourcing-derivation]] (the weak-field reduction), [[F309-gstar-from-model-content]] ($g_*$ for L4's BBN row), [[F130-blockspin-rg-gauge-gravity]] (the flow that L7 names as the route to finishing), [[F184-tabulated-eos-neutron-stars]] (the NS mass/radius in L4).

**External:** D. Lovelock, *The uniqueness of the Einstein field equations in a four-dimensional space*, Arch. Rational Mech. Anal. **33**, 54 (1969); *The Einstein tensor and its generalizations*, J. Math. Phys. **12**, 498 (1971); and — the paper whose title is this finding's own headline, and which the first version failed to cite — [*The Four-Dimensionality of Space and the Einstein Tensor*, J. Math. Phys. **13**, 874 (1972)](https://ui.adsabs.harvard.edu/abs/1972JMP....13..874L/abstract). The linear-in-$\partial^2g$, dimension-**independent** half of the uniqueness is [Vermeil (1917) / Weyl (1922) / Cartan (1922)](https://en.wikipedia.org/wiki/Vermeil%27s_theorem); the $d=4$ vanishing is the **Lanczos–Bach identity** (Lanczos 1932/1938). The thermodynamic route to the same Lanczos–Lovelock class — i.e. this finding's §4 argument, published 2006 — is [Padmanabhan, *Thermodynamic route to field equations in Lanczos–Lovelock gravity*, hep-th/0607240](https://arxiv.org/abs/hep-th/0607240); see also [Padmanabhan & Kothawala, arXiv:1302.2151](https://arxiv.org/pdf/1302.2151). Sakharov induced gravity: M. Visser, hep-th/0204062; [Barceló, Visser & Liberati, *Einstein gravity as an emergent phenomenon?*, gr-qc/0106002](https://arxiv.org/html/gr-qc/0106002v1). **On the residual premise, against this finding:** [L. Sindoni, *Emergent Models for Gravity: an Overview*, arXiv:1110.0686](https://arxiv.org/pdf/1110.0686) — the emergence of an effective Lorentzian spacetime is "not generic". On the 4D-EGB limit, closed: [Shu, arXiv:2004.09339](https://arxiv.org/pdf/2004.09339v1). Measured anchors: B. Bertotti, L. Iess & P. Tortora, Nature **425**, 374 (2003), $\gamma-1=(2.1\pm2.3)\times10^{-5}$; Hofmann & Müller 2018, $\dot G/G=(7.1\pm7.6)\times10^{-14}\,\text{yr}^{-1}$.
