# F294 — Auditing the F110 C7 χ-map for $N_c$: the identity is **measured** $N$-free across $\mathbb Z_2..\mathbb Z_9$ and $U(1)$ (deviation literally `0.0`), but the F293 selector **does not survive** a Casimir reading — H2 gives $N_c=1.28$ and H3 has no root at all

**Date:** 2026-08-05 - 22:10
**Numbering:** **F294**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `tender-gifted-pascal-3`, sector `gauge`.
**Status:** Confirmed — the $N$-independence is **exact** (worst deviation across seven groups is literal `0.0`); the hypothesis comparison is a root-finding result. Folded into the F293 gate as checks **B6/B6b** (record now 17/17).
**Verdict:** **Two-edged, and the second edge matters more.** F293 §4.1 rested on an *observation about the written chain* ("no Casimir appears"); this finding replaces it with a *measurement* — the χ-map is exactly $N$-independent in the group family the model implements. But it also shows the F293 selector is **not robust against the translation hypothesis**: under a fundamental-Casimir reading the selector returns $N_c=1.28$, and under an adjoint reading it has **no solution**. **F293's falsifier understated this as "a 25% factor takes it to 2.54"; the correct statement is that the wrong reading destroys the selector rather than shifting it.** CL257 is corrected accordingly.
**Modules:** `src/casim/engine/gauge/derive_ncolour.py` (`c7_zn_independence`, `c7_translation_hypotheses`)
**Test / results:** record `F293-why-three-colours` (tier gate, entry `check_ncolour`, checks B6/B6b) → `test-results/F293_why_three_colours.json`
**Cross-references:** [[F293-why-three-colours]] (the finding whose named next step this executes, and whose falsifier this corrects), [[F110-realtime-link-hamiltonian-confinement]] (the C7 identity and the module audited — **its own scope note deferring the SU(3) Casimir ladder is the crux**), [[F144-route-a-alpha-s-dimensional-transmutation]] ($g_s=\tfrac12$), [[F97-baryon-no-go-centre-closure]] / [[F99-sigma-as-centre-lagrange-multiplier]] (why $\mathbb Z_3$ is the load-bearing case), [[F86-colour-dielectric-dual-superconductor]] (the dual-superconductor mechanism, which is centre-dominated).

---

## 1. What was open

F293 §"Remains" item 3 named this exactly:

> **The abelian→non-abelian translation of $g_s=\tfrac12$ is unaudited.** F110 C7 is a dual $U(1)$ construction. Confirming it carries no $N_c$ would harden §4; finding that it does would move the selector. This is a bounded, concrete next step and it is the one that most affects the result.

The whole F293 selector rests on one premise: $\alpha_s(\mu_0)=1/(16\pi)$ is $N_c$-free, so $N_c$ enters the running only through $\beta_0$. That premise was supported by *reading* the derivation and noticing no Casimir in it. Reading is weaker than measuring.

---

## 2. The identity, and why it could have carried $N$

F110's Kogut–Susskind Hamiltonian is

$$H=\frac{g^2}{2}\sum_{\ell}\hat E_\ell^{\,2}-\lambda\sum_p\cos\hat\phi_p,$$

and the C7 map comes from matching one open plaquette's **4 exclusive boundary links** against the F101 rotor $H=\frac1{2\chi}\hat E^2-\lambda\cos\hat\phi$:

$$\frac{g^2}{2}\cdot4m^2=\frac{1}{2\chi}m^2\quad\Longrightarrow\quad \chi=\frac1{4g^2}.$$

Where $N$ *could* enter: the module's $\mathbb Z_N$ electric energy uses the **symmetric residue** $s(e)=((e+\lfloor N/2\rfloor)\bmod N)-\lfloor N/2\rfloor$, so the set of available levels $\{s(m)\}$ **does** depend on $N$ — $\mathbb Z_3$ offers $\{-1,0,1\}$, $\mathbb Z_9$ offers $\{-4,\dots,4\}$. If the extracted $\chi$ depended on which levels a group supplies, the map would carry $N$ and F293's premise would fail.

---

## 3. The measurement: it does not

`build_dual_hamiltonian` accepts any $\mathbb Z_N$ (`group=N`), so the identity can simply be run across the family. Extracting $\chi_\text{measured}=s(m)^2/\big(2\,\mathrm{diag}(m)\big)$ at **every non-zero level of every group**, at $g^2=1/4$ (so $\chi$ should be 1):

| Group | levels $s(m)$ | $\chi$ measured |
|---|---|---|
| $\mathbb Z_2$ | $\{-1,0\}$ | $1.000000000000$ |
| $\mathbb Z_3$ | $\{-1,0,1\}$ | $1.000000000000$ |
| $\mathbb Z_4$ | $\{-2,-1,0,1\}$ | $1.000000000000$ |
| $\mathbb Z_5$ | $\{-2,\dots,2\}$ | $1.000000000000$ |
| $\mathbb Z_7$ | $\{-3,\dots,3\}$ | $1.000000000000$ |
| $\mathbb Z_9$ | $\{-4,\dots,4\}$ | $1.000000000000$ |
| $U(1)$ | $\lvert m\rvert\le6$ | $1.000000000000$ |

**Worst deviation across all seven groups and all levels: literal `0.0`.**

The reason is structural and worth stating, because it explains why the result is exact rather than merely small: **$s(m)^2$ cancels between the electric term and the rotor level**, so $\chi=1/(4g^2)$ holds *per level*. The identity is therefore blind to which levels the group supplies — which is exactly the $N$-independence F293 needed, now established by computation rather than by inspection.

**F293 §4.1 is upgraded**: "no Casimir appears in the written chain" → "the χ-map is measured $N$-independent across the implemented group family."

---

## 4. The uncomfortable half: only the implemented reading gives 3

The verification above covers the groups the model **implements** — $\mathbb Z_N$ (the centre) and compact $U(1)$. It does not cover a genuine $SU(N)$ link Hamiltonian, and `link_hamiltonian.py`'s own scope note says so in as many words:

> Dynamical-matter coupling and the **SU(3) Casimir ladder remain future work** (the centre projection argument F97–F99 is why $\mathbb Z_3$ is the load-bearing case).

If the correct translation instead matches the rotor's $m=1$ level to a link carrying the **fundamental representation**, the Casimir does *not* cancel: the matching becomes $\frac{g_s^2}{2}\cdot4\,C_2=\frac1{2\chi}$, i.e. $\alpha_0\to\alpha_0/C_2$. Root-finding the selector's self-consistency $N_c=\mathcal N\big(\alpha_0 h(N_c)\big)$ under each reading (root-found, **not** fixed-point iterated — the iteration diverges under H2/H3, and divergence is not the same as "no root"):

| Reading | $h(3)$ | root(s) in $N_c\in[1.05,13]$ | selector survives? |
|---|---:|---|---|
| **H1** centre / $U(1)$ — **implemented, verified $N$-free** | $1.0000$ | $2.9981$ | **yes** |
| **H2** fundamental Casimir, $\alpha_0/C_F$ | $0.7500$ | $1.2845$ | **no** |
| **H3** adjoint Casimir, $\alpha_0/C_A$ | $0.3333$ | **none** | **no** |

> **This corrects F293's falsifier.** F293 wrote that a 25% coupling factor "takes it to 2.54", which frames the fragility as a *shift*. It is not a shift. The physically motivated alternative reading is not a 25% perturbation — it is a different matching, and it returns 1.28 or nothing. **The selector does not degrade gracefully; it fails.**

---

## 5. Which reading is right, and how the model's own architecture votes

Three model-internal arguments favour **H1**, and none of them is a proof:

1. **It is what is implemented.** The tree's confinement sector is built on $\mathbb Z_N$ and $U(1)$; no $SU(N)$ Casimir ladder exists anywhere in it.
2. **F97–F99 argue the centre is load-bearing** — the area law is carried by the $\mathbb Z_3$ centre, which is why F110 chose $\mathbb Z_3$ as its exact-Hilbert-space case.
3. **F86's mechanism is a dual superconductor**, and dual-superconductor / centre-vortex confinement is centre-dominated: the string tension depends on the $\mathbb Z_N$ class, not on $C_2$.

Against that, the honest counterweight: **real QCD shows approximate Casimir scaling of $\sigma_R$ at intermediate distances**, with centre dominance only asymptotic. The two readings agree on *which* state is the fundamental string but disagree on its energy normalisation, and that normalisation is precisely what sets $\alpha_0$.

**So H1 is the model's choice, and it has never been validated against a genuine $SU(N)$ link Hamiltonian.** That validation is now the sharpest open item in the B10 line, because §4 shows the selector does not survive the alternative.

---

## 6. What this does to the B10 position

| Claim | Before F294 | After F294 |
|---|---|---|
| $\alpha_s(\mu_0)$ is $N_c$-free | asserted from reading the chain | **measured exact** across 7 groups |
| the selector's fragility | "a 25% factor moves it to 2.54" | **structural: wrong reading ⇒ 1.28 or no root** |
| what would settle it | unnamed | build F110's deferred $SU(N)$ Casimir ladder and test Casimir scaling vs centre dominance of $\sigma$ |

CL257's falsifier is rewritten and its confidence held at `medium` with the reason changed: not "the fragile direction is quantified" but "the selector is contingent on an unvalidated modelling choice, and the alternative destroys it."

---

## What this closes and what remains

**Closes.** F293's named next step. The C7 χ-map carries no $N$ in the group family the model uses, exactly, and the selector's dependence on the translation hypothesis is now quantified instead of flagged.

**Remains.**

1. **Build the $SU(N)$ Casimir ladder** that F110 deferred, and re-run C7 against it. This is the one computation that decides between H1 and H2, and therefore decides whether the F293 selector means anything.
2. **Discriminate physically:** measure $\sigma_R$ for higher representations in the model's own confinement sector (F86 analytic, F94 Monte-Carlo). Casimir scaling favours H2; dependence only on the $\mathbb Z_N$ class favours H1. The model has both engines and has never been asked this question.
3. **Nothing here derives $N_c=3$**, and the B10 grade does not move on this finding. If anything F294 makes the `PARTIAL` grade *more* conditional than F293 left it.
