# F98 — The enforcer of the centre-phase budget is itself the binder (closing the F97 §4/§8 bridge)

**Date:** 2026-06-05 - 14:05
**Status:** Confirmed — 5/5 checks PASS. E1/E3/E5 algebraically exact (sympy/integer), E2 exact (BPS Tier-1, F86), E4 machine-precision round-trip (Tier-2). Builds the quantitative bridge that F97 §4 *theorized* and §8 flagged as open.
**Script:** `model-tests/test_F98_enforcer_is_binder.py` (<0.1 s)
**Results:** `test-results/F98_enforcer_is_binder.json`
**Cross-references:** [[F97-baryon-phase-closure-no-go]] (the closure principle this tests; §4 grammar, §8 open bridge), [[F86-colour-dielectric-dual-superconductor]] (Option C, $\sigma=2\pi v^2 n$), [[F94-lattice-gauge-mc-confinement-vs-F86]] (Option A, gauge-MC $\sigma$ and the $v^*=\sqrt{\sigma_A/2\pi}$ bridge), [[F71-colour-singlet-baryon-proton]] ($\varepsilon_{abc}$ singlet, N-ality-0), [[F70-gradient-flow-confinement-string-tension]] (area-law $\sigma$), [[F92-per-constituent-phase-consistency]] (the pair-sector instance of the same grammar).

---

## 1. The claim under test

F97 §4 stated the **closure principle** as theorized structure, not derived fact:

> A stable composite is a configuration whose phase budget closes exactly; the object that enforces the budget is itself the binding agent. Non-closure is priced either by over-wrap (kinematic instability, the pair sector) or linearly in separation (confinement, the colour sector).

For the colour sector the budget is the $\mathbb{Z}_3$ **centre phase** and the enforcer/binder is the F86 colour-dielectric condensate. F97 §8 named the missing piece explicitly: *“a dynamical demonstration that $\sigma$ emerges as the Lagrange-multiplier price of centre-phase non-closure.”* This finding supplies the quantitative bridge using the two binding-force builds that already exist — **Option C (F86)** and **Option A (F94)** from `roadmap-P1-binding-force-options.md`.

## 2. The one identification that makes “enforcer = binder” exact

The whole result turns on a single fact: the **centre charge / N-ality (triality) $k$ plays two roles at once.**

1. **Budget label.** The phase budget closes exactly iff $k\equiv0\pmod N$ (N-ality 0). This is the colour-sector stability condition (F71): $qqq$, $q\bar q$, pentaquark, gluon close; $q$, $qq$, $qqqq$ do not.
2. **Binder coefficient.** $k$ is the topological **winding $n$** of the dual-superconductor flux tube, hence the multiplier in the exact F86 tension $\sigma_\text{BPS}=2\pi v^2\,|n|$ (Option C) — and the *only* quantity the asymptotic string tension depends on in the full non-Abelian gauge sector (Option A).

So the object enforcing the budget (the centre charge, realised as condensate flux) is **literally the coefficient of the binding tension**. One object, two roles — which is exactly what “the enforcer of the budget is itself the binder” asserts.

$$\boxed{\;\sigma(\text{closed budget})=0,\qquad \sigma(\text{open budget})>0\;}$$

with $\sigma=0$ holding **iff** N-ality $=0$.

## 3. What each check establishes (5/5)

| Check | Statement | Route | Tier | Residual |
|---|---|---|---|---|
| E1 | Budget = $\mathbb{Z}_3$ centre phase: closes (N-ality 0) for $qqq$, $q\bar q$, pentaquark, gluon; open for $q$, $qq$, $qqqq$ | budget | exact (int) | 0 |
| E2 | **Option C:** $\sigma_\text{BPS}=2\pi v^2|n|$ with $n=$ centre charge; $\sigma=0$ **exactly** iff budget closes; multiplier $=$ N-ality ($\sigma(2)=2\sigma(1)$) | C (F86) | 1 | 0.0 |
| E3 | **Option A:** asymptotic $\sigma_k=\frac{k(N-k)}{N-1}\sigma_1$ depends **only** on N-ality; centre-periodic ($\sigma_0=\sigma_N=0$); adjoint screened, fundamental confined; $k\!\leftrightarrow\!N\!-\!k$ degenerate | A (F94) | exact (rational) | 0 |
| E4 | **A$\leftrightarrow$C bridge:** $v^*=\sqrt{\sigma_A/2\pi}$ maps the gauge-MC tension to the condensate scale; round-trip $\sigma_C(v^*)=\sigma_A$; both give $\sigma(\text{closed})=0$ | A+C | 2 | $<10^{-12}$ |
| E5 | $\sigma$ is the **Lagrange price of non-closure**: $E_\text{iso}(\text{closed})=0$ (finite, free), $E_\text{iso}(\text{open})=\sigma R\to\infty$ (confined); linear in $R$ | C (F86) | exact | 0 |

**E2** is the heart: the F86 condensate VEV $v$ (the enforcer of the dual-Meissner vacuum) sets the scale, and the centre charge $n$ is the multiplier, with $\sigma$ vanishing **identically** when the budget closes. **E3** is the gauge-invariant (full non-Abelian) form of the same statement: adding a gluon (N-ality 0) cannot change the asymptotic tension, so $\sigma$ is a function of the centre charge alone. **E4** shows the two routes are not rival mechanisms but one object — F94’s gauge-MC string tension *is* F86’s condensate scale, re-expressed. **E5** delivers the §8 bridge: $\sigma$ is the price conjugate to the centre-phase constraint — zero on closure (finite isolation energy ⇒ free asymptotic state), positive and linear off closure (infinite isolation energy ⇒ confinement).

## 4. What is now derived vs still theorized

**Now derived (this finding).** That the centre charge is simultaneously the budget label and the binding coefficient, so that the binding tension vanishes *exactly* on budget closure and is positive off it — across **both** P1 routes, with the A↔C bridge tying them to one condensate. This is the precise content of “enforcer = binder” and the “$\sigma$ as price of non-closure” bridge.

**Still theorized / honest scope.**
- **Detailed $k$-dependence differs between A and C.** Option C at the strict Abelian-Higgs BPS level gives $\sigma_k\propto k$ (so $\sigma_2=2\sigma_1$); the full non-Abelian Casimir/$k$-string law (Option A) gives $\sigma_k=\frac{k(N-k)}{N-1}\sigma_1$ with $\sigma_2=\sigma_1$. **The two agree on everything the F97 claim needs** — $\sigma_0=0$ and $\sigma_{k\neq0}>0$ — and differ only on the relative weight of the $k=2$ string. This is a known A-vs-C gap of the same character as the Coulomb-tail difference (F94 CMP3), flagged not papered over.
- **The Lagrange-multiplier statement is structural,** not yet a derivation of $\sigma$ as the multiplier emerging from the QCA update rule itself (the deeper form of the F97 §8 wish). E5 establishes the *price structure* ($\sigma=0$ on closure, $\sigma R\to\infty$ off it); deriving $\sigma$ as the constraint multiplier inside the rotation-rule update remains future work.
- **Production $\sigma_A$ is user-run** (F94): the gauge-sector content tested here is the exact centre-charge *structure* of the asymptotic tension, not a converged MC number.

## 5. Falsifiable handles (sharpening F97 §5)

1. **Binding ⇔ non-closure, with no exceptions.** Any asymptotic state with N-ality $\neq0$ (a free quark, a free diquark, a fractionally-charged hadron) would have $\sigma=0$ for a closed budget — falsifying the identification. None observed.
2. **Asymptotic tension is centre-only.** Any measured asymptotic string tension that depends on more than the N-ality of the source (e.g. an adjoint source that stays linearly confined to arbitrary $R$ without string-breaking/screening) falsifies E3. Lattice QCD confirms adjoint screening.
3. **$k=2$ string ratio.** A clean measurement of $\sigma_2/\sigma_1$ discriminates the Abelian-BPS value 2 (C) from the Casimir value 1 (A); the model predicts the non-Abelian Casimir/sine-law regime (A) is physical.

## 6. Provenance

- New content: the dual-role identification (§2) and its five-check verification (§3); the explicit A-vs-C $k$-dependence scope (§4).
- Reused exact results: F86 $\sigma_\text{BPS}=2\pi v^2 n$ (CD1), F94 $v^*=\sqrt{\sigma_A/2\pi}$ bridge (CMP2), F71 N-ality-0 singlet, F97 §4 closure grammar / P6 $\mathbb{Z}_3$ arithmetic.
- Verification: `model-tests/test_F98_enforcer_is_binder.py` (2026-06-05, 5/5 PASS), results `test-results/F98_enforcer_is_binder.json`.
