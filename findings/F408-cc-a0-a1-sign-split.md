# F408 — The cosmological-constant sign split: the model's one all-fermion heat-kernel sum has $a_0<0$ and $a_1>0$, so the diluted zero-point term and F196's ceiling are opposite-signed objects (ratio $24\sqrt3\pi$), the F183/F190 capacity ceiling cannot cancel the negative sum, and G1 is restated as $a_0$ removal (sequestering) + the positive $a_1$ horizon tension + $\Omega_\Lambda$

**Date:** 2026-09-27 - 11:38
**Checked:** 2026-09-27 - 11:52 -- 5 PASS / 7 WEAKENS / 1 FAIL / 0 NOT RUN -- **CONFIRMED-NARROWER**
**Numbering:** **F408**, taken as `NEXT FREE NUMBER` from `casim index` (max was F407, no free backlog).
**Status:** **Confirmed-narrower — 13/13 legs PASS, 5/5 declared controls CONTROL (red exactly on the declared legs).** Exact (Fraction/sympy) on S1, S3, S4, S5 and on the symbolic form of S2; machine precision on S2's numerical ratio ($8.7\times10^{-16}$), on the cell–content identity ($1.1\times10^{-16}$) and on the BZ moment $I_\text{cc}=3\sqrt3\pi/4$ ($2.7\times10^{-15}$). **Conditional on three declared inputs** (§2): the continuum Lichnerowicz $R/4$, **all gauge bosons composite**, and the principal quasi-energy branch. **One elementary negative result (S3), one withdrawal (§6), one ledger restatement (§7).** Does not derive $\Omega_\Lambda$; does not adopt sequestering; does not dispute F196's $L^{-2}$ scaling of the ceiling, CL275, or F241.
**Module:** `src/casim/engine/interactions/cosmology_lambda_sign_split.py`
**Test record:** `F408-cc-sign-split` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`, 5 controls verified)
**Results:** `test-results/F408_cc_sign_split.json`
**Claim:** CL021 (amended 2026-09-27: the §B-as-diluted-$a_0$ reading withdrawn, the route's carrier named as the $a_1$ term); CL303 annotated (its mechanism is the only non-local $a_0$-remover the tree has built, and is sign-blind). No new card — this is an internal-mechanism result about which of two of the model's own objects carries the residual, not an extension of GR/QFT.
**Addresses:** rubric row **K9**, ledger **G1** — the half of G1's standing task *"show that the F164 zero-point sum is made to respect the F183 capacity bound, or show that it is not"*: **it is not, and cannot be.**
**Cross-references:** [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] ($a_0$, and its all-fermion **negative** sign), [[F61-weyl-eta-and-gstar-prefactor]] ($\eta_\text{Weyl}=+1/12$: $a_1$ **positive**), [[F59-induced-eh-prefactor-and-f10-selection]] / [[F79-structural-newton-constant]] ($1/16\pi G$ is the $a_1$ sum; no bare kinetic term), [[F193-ontic-vacuum-gravitates-as-zero]] (§B and its line-88 sign reasoning — **withdrawn here**, §6), [[F196-dilution-exponent-derived]] (the ceiling, $a_1$-built), [[F183-blackhole-under-full-tensor]] / [[F190-horizon-entropy-lattice-microstates]] (the two capacity routes), [[F332-cc-dynamics-two-channels-excluded]] (ceiling = Friedmann-I), [[F367-cc-sequestering]] / [[F368-cc-sequestering-consistency]] (the non-local $a_0$-remover and its costs), [[F241-omega-lambda-o1-residual-anthropic]] ($\Omega_\Lambda$, unchanged), [[F319-uv-sector-reconciled-physical-cutoff-and-counterterms]] (U8/CL275, unchanged), [[F86-colour-dielectric-confinement]] (the string-tension comparison, §5). External: Seeley–DeWitt $a_1$ with Lichnerowicz $\slashed D^2=-\Box+R/4$ (standard); Kaloper & Padilla 2014 (via F367). Prior art: §8.

---

## 1. The question

Since 2026-08-18 the live K9 route is quoted as **one** route, "F193 §B + F196": the capacity ceiling $\rho\le3c^4/8\pi GL^2$ at $L=R_H$. It is written two ways in the tree:

- **F193 §B:** $\rho_\Lambda\approx\rho_\text{vac}\,(a/R_H)^2$ — the bare zero-point density diluted. This is an **$a_0$** object.
- **F196:** $\rho_\Lambda\approx3c^4/(8\pi G R_H^2)$ — built from $G$. Since $1/16\pi G$ *is* the model's $a_1$ sum (F59/F79/F61), this is an **$a_1$** object.

F164 fixed the sign of $a_0$ as **negative** (the model has no fundamental bosons; the Weyl tower's zero-point sum is $-\tfrac12\sum\hbar\omega$). F193 Part A was the only thing that removed that sign ("there is no negative beable tower, so the only sign that matters is the $w=-1$ sign", F193 line 88), and Part A was **excluded** on 2026-08-18 (CL275). Nothing in the tree re-checked the sign of the surviving route afterwards. This finding does, and asks the question raised in conversation on 2026-09-26: *does the lattice's vacuum stiffness contribute a positive, confinement-like energy?*

## 2. S1 — the sign split (exact)

For a Laplace-type operator $-\Box+E$ on a rank-$r$ bundle, $a_1/R=r/6-\mathrm{tr}E/R$. With statistics sign $s$ ($+1$ boson, $-1$ fermion):

| field | $a_0$ (zero-point, signed dof) | $a_1/R$ (unsigned) | $c=s\,a_1/R$ | $\eta=c/2$ |
|---|---|---|---|---|
| real minimal scalar | $+1$ | $+\tfrac16$ | $+\tfrac16$ | $+\tfrac1{12}$ |
| 2-component Weyl ($r=2$, Lichnerowicz $E=R/4$) | $-2$ | $2(\tfrac16-\tfrac14)=-\tfrac16$ | $+\tfrac16$ | $+\tfrac1{12}$ |

The fermion sign enters **both** moments; the Lichnerowicz $R/4$ makes the spinor $a_1$ trace negative, so for $a_1$ (only) the two minus signs cancel. Summed over the model's content — $g_*=48$ Weyl fields (F61 Part B: $16$ per generation incl. $\nu_R$) and **zero** fundamental bosons (F67–F69):

$$a_0\propto-96<0,\qquad \sum_i\eta_i=\tfrac{48}{12}=4>0,\qquad \operatorname{sign}(a_0)\operatorname{sign}(a_1)=-1 .$$

**One sum, two moments, opposite signs.** $a_1>0$ is exactly why gravity is attractive in an all-fermion model (F61); $a_0<0$ is F164's wrong-sign vacuum. The bookkeeping itself is textbook (§8); what is model-specific is the content it is summed over. $\sum\eta=4$ **is** the registered canonical cell: $(a/\ell_P)^2=2\pi\sum\eta\,\sqrt3=8\pi\sqrt3$ (F79), checked to $1.1\times10^{-16}$.

**Declared inputs of S1** (not derived here):
1. **Lichnerowicz $E=R/4$** — the continuum value, imported as in F61.
2. **Every gauge boson is composite** (decision 5; F67–F69; F164 Part B). A fundamental massless vector with its two ghosts has $a_1/R=4/6-1-2\cdot\tfrac16=-\tfrac23$, i.e. **$-4$ scalar units**. So $48$ Weyl $+\,12$ fundamental vectors ($8$ gluons, $W^\pm$, $Z$, $\gamma$) gives $\sum\eta=4-12\cdot\tfrac13=0$ **exactly**: no induced $1/G$ at this order. F61 §caveats already records the gauge sector as not included; F408's $a_1$ sign — and everything built on it in §3–§7 — is **conditional on the compositeness of all twelve**, which is the sharpest falsifier of this finding (lever `fundamental_vectors=12`). The lattice link variables of F94/F117 are gauge *connections* on which the matter fields hop, and whether they carry independent $a_1$ weight is the open question this names.
3. **Principal quasi-energy branch with a filled negative sea** for the sign of $a_0$. On a unitary QCA energy is defined modulo $2\pi\hbar/\tau$; on the $[0,2\pi)$ branch the lower band sits at $2\pi/\tau-\omega>0$. The $a_0<0$ statement is F164's convention, adopted, not re-derived.

Controls: deleting the $R/4$ term (`lichnerowicz_E=0`) flips $a_1$ negative; a real-scalar tower larger than the 96 fermionic dof (`fundamental_bosons=97`, the tower the model does not have) flips $a_0$ positive; `fundamental_vectors=12` zeroes $a_1$.

## 3. S2 — the two halves of the route are different objects (exact + machine)

Use the **same field content in both moments.** Let $N_b=\lvert a_0\rvert$ in half-$\hbar\omega$ branches ($2$ per Weyl field, $96$ for the model) and $\sum\eta$ the $a_1$ sum ($4$). F164's per-branch density is $\sqrt3\,I_\text{cc}\,\hbar c/a^4$ (F164's "$g_*=2$, two BCC Weyl branches" is **one** Weyl field), and the cell is $a=\sqrt{2\pi\sum\eta}\;3^{1/4}\ell_P$ (F59/F79). Then, with $\operatorname{sign}(G)=\operatorname{sign}(a_1)$:

$$\frac{\lvert\rho_{a_0}\rvert\,(a/R_H)^2}{3c^4/8\pi GR_H^2}=\frac{4N_b\,I_\text{cc}}{3\sum\eta}\ \xrightarrow{\ N_b=2g,\ \sum\eta=g/12\ }\ 32\,I_\text{cc}=24\sqrt3\,\pi=130.59\quad(2.12\ \text{dex}),$$

**independent of the field count $g$** (sympy, residual $0$), with $I_\text{cc}=3\sqrt3\cdot\tfrac12\langle\omega\rangle_\text{BZ}=3\sqrt3\pi/4$ ($\langle\omega\rangle=\pi/2$ exactly, F164). At $H_0=67.4$:

$$\rho_{a_0}(a/R_H)^2=-1.00\times10^{-7}\ \mathrm{J/m^3},\qquad \rho_{196}=\frac{3c^4}{8\pi GR_H^2}=+7.67\times10^{-10}\ \mathrm{J/m^3}.$$

Numerically on the tree's own `sakharov_moments` grid ($n=64$; even, so the $q\to q+\pi$ pairing is node-by-node — odd $n$ gives $\sim2\times10^{-7}$ and would fail the leg): $I_\text{cc}$ residual $2.7\times10^{-15}$; ratio residual $8.7\times10^{-16}$. (Structural $G$; CODATA $G$ differs by $-3.0\times10^{-8}$, the 7-digit rounding of the tabulated CODATA $\ell_P$.)

**Reading.** $\lvert a_0\rvert a^2$ and $a_1$ are both $\hbar c/a^2$ objects, so the diluted zero-point term is the ceiling times a fixed $O(10^2)$ number — of the **opposite sign**. **F193 §B as written** used $g_*=2$ branches in $\rho_\text{vac}$ against a $G$ calibrated at 48 Weyl fields and so got $\sqrt3\pi/2=2.72$ ($0.54$ dex from $\rho_\Lambda$); with consistent content §B's magnitude overshoots the ceiling by $2.1$ dex. §B's apparent agreement was a content mismatch, and the $0.09\%$ proximity of $\sqrt3\pi/2$ to $e$ is an artifact of that mismatch — recorded so nobody quotes it.

## 4. S3 — the capacity ceiling cannot cancel a negative $a_0$ (exact, elementary)

The ceiling $\rho\le3c^4/8\pi GL^2$ is a **one-sided upper bound**. A negative term satisfies it for every $L$, and an upper bound cannot raise or remove it — that is the whole content, and it is elementary. Two sympy checks make it concrete when $a_0$ is taken alone, in flat slicing (F182):

1. **F183 route (Schwarzschild capacity).** Saturation $2Gm(L)/(Lc^2)=1$ with $m=\tfrac{4\pi}{3}\rho L^3$ has, for $\rho=-X<0$, **no positive root** (sympy); for $\rho>0$ it has exactly one, $L=c\sqrt{3/(8\pi G\rho)}$. Negative energy never saturates a horizon bound.
2. **F190/F196 Route 2 (Bekenstein count × Gibbons–Hawking $T$).** Flat Friedmann-I gives $H^2=8\pi G\rho/3=-8\pi GX/3<0$: **no real $H$**, no de Sitter horizon, no $T_\text{dS}=\hbar H/2\pi$, nothing to count. (A negative vacuum drives toward anti-de Sitter; in open slicing AdS does have a real $H$, so this leg is a flat-slicing statement.)

**So G1's standing question has an answer for the $a_0$ half: the F164 zero-point sum is not "made to respect" the F183 capacity bound in any sense that removes it.** It already respects it trivially, being negative; the bound can neither raise it nor cancel it. With positive matter present the bound acts on the **total** density and says nothing about $a_0$ separately. The ceiling is a consistency condition (F241) and, by F332 K1, *is* Friedmann-I at $L=R_H$. Control: `fundamental_bosons=97` (positive $a_0$) produces both a saturation root and a real horizon.

## 5. S4 — the positive $a_1$ side is confinement-shaped (exact)

The capacity energy of a region of radius $L$ is

$$E(L)=\rho_\text{ceiling}(L)\cdot\tfrac{4\pi}{3}L^3=\frac{c^4}{2G}\,L=\sigma_H L,\qquad \sigma_H=\frac{c^4}{2G}=\frac{4\sqrt3\,\pi\,\hbar c}{a^2}=6.05\times10^{43}\ \mathrm{N},$$

**linear in $L$** ($d^2E/dL^2=0$, sympy), positive iff $a_1>0$. This is the form of the confining potential $V(R)=\sigma R$ — in F86 the BPS tension $\sigma=2\pi v^2n$ is set by the condensate stiffness; here $\sigma_H=8\pi\cdot(c^4/16\pi G)$ is set by the vacuum's $a_1$ stiffness, $4\sqrt3\pi$ units of $\hbar c$ per cell area ($\approx4\times10^{38}\,\sigma_\text{QCD}$). The gravitational analogue of string breaking is horizon formation (F183: packing a region past $\sigma_H L$ makes a black hole). **Scope:** by F332 K1 this is the geometric side of Friedmann-I, not an additional source — it is the answer to "does the stiffness contribute *positive* energy of confinement type" (**yes, in sign and scaling**), not a new term in $\rho$.

## 6. Withdrawn — F193 §B's sign reasoning inherited from Part A

Findings are written once (D12); F193 is not edited. What is withdrawn, as of this finding, for **citation** purposes:

1. **F193 line 88** — *"there is no negative beable tower, so the only sign that matters is the $w=-1$ Friedmann sign F192 already fixed"*. This was Part A's conclusion, and §B was explicitly built on it: F193 line 35, *"With the bare term gone, the observed $\rho_\Lambda$ is … the back-reaction of the actual non-vacuum content"*. So §B fell with Part A; F408 supplies the sign and the consistent magnitude of what is left. With Part A excluded (CL275), the negative tower is back: $a_0<0$ (S1). The sign of the vacuum sum is **not** settled by F192's $w=-1$ argument; F192 fixes that a *positive* $w=-1$ component accelerates, and says nothing about whether the model's $a_0$ is positive.
2. **F193 §B as the carrier of the residual.** $\rho_\text{vac}(a/R_H)^2$ with the F164 sign and consistent content is **negative** and $24\sqrt3\pi$ times the ceiling (S2). §B may be cited only for the structural observation that $\lvert a_0\rvert a^2$ and $a_1$ are the same kind of object, **not** as "the observed $\rho_\Lambda$ is the IR-diluted zero-point energy", and not for its $0.54$ dex agreement (a content mismatch). The positive, correctly signed object is F196's $a_1$ form.
3. **"F193 §B + F196 is one route"** (K9 adjudication 2026-08-18, open-derivations G1, CL021). They are two objects of opposite sign; only F196 is the route.

4. **F196's "dilution exponent of $\rho_\text{vac}$" reading.** F196 frames $p=2$ as the exponent in $\rho_\Lambda=\rho_\text{vac}(a/R_H)^p$ (its line 5). With §B's object withdrawn, that reading loses its referent. What survives from F196 is its own content: both of its routes compute the **capacity ceiling itself**, $\rho(L)=3c^4/8\pi GL^2\propto L^{-2}$, directly from $G$ — never from $\rho_\text{vac}$.

What is **not** withdrawn: F196's $L^{-2}$ scaling of the ceiling and its two routes, F241's ceiling theorem, F332's ceiling = Friedmann-I identity, CL275.

## 7. G1 restated

| Piece | Object | Sign | Status after F408 |
|---|---|---|---|
| **$a_0$ removal** | F164 zero-point sum, all 48 Weyl fields: $\rho_{a_0}\approx-1.7\times10^{113}$ J/m³ ($=48\times$ F164's $g_*=2$ figure) | **negative** | Needs a mechanism that removes a constant of **either sign**. The capacity ceiling cannot (S3); F332 closed AB≡1 and block-spin. The only non-local mechanism the tree has built is **F367 sequestering (CL303, contingent)**, which is sign-blind by construction (S5 re-checks it with $C$ real). A finite bare-$\Lambda$ counterterm (F319's Wilsonian reading) is also sign-blind, but it is a fit, not a mechanism. The sequestering adoption costs (new global fields, closure $k>0$, transient DE — F367/F368) are therefore **the price of a mechanistic K9**. |
| **The positive $a_1$ horizon term** | $3c^4/8\pi GL^2$, $E=\sigma_H L$ | **positive** (S1, S4; conditional on composite gauge bosons) | Sets the **scale** — the ceiling $\rho_\text{crit}$ — against which the old "120.66 decades" accounting was done (K9 adjudication, unchanged). By F332 K1 it *is* Friedmann-I, so it is **not a source** and not a component of $\rho_\Lambda$; it fixes a ceiling, not a value (F241). |
| **$\Omega_\Lambda$** | $\rho_\Lambda/\rho_\text{crit}=0.685$ | — | Unchanged: F241's coincidence residual $=1-\Omega_m$. |

**Net:** *K9/G1 = $a_0$ removal (sequestering, contingent) + the positive $a_1$ horizon term (the scale, not a source) + $\Omega_\Lambda$.* The old phrasing — "a dynamical enforcement of the capacity ceiling on the F164 sum" — asked an upper bound to remove a negative term, which it cannot do; it is replaced.

## Exactness

| Result | Type | Residual |
|--------|------|---------|
| S1: $a_0<0$, $\sum\eta=g_*/12=4>0$, sign product $-1$ (48 Weyl, 0 bosons) | exact (Fraction) | 0 |
| S2: $\lvert\rho_{a_0}\rvert(a/R_H)^2/\rho_{196}=4N_bI_\text{cc}/(3\sum\eta)=24\sqrt3\pi$, content-independent | exact (sympy) | 0 |
| S2: canonical cell $(a/\ell_P)^2=2\pi\sum\eta\sqrt3$ at $\sum\eta=4$ | machine | $1.1\times10^{-16}$ |
| S2: $I_\text{cc}=3\sqrt3\pi/4$ on the BCC grid | machine | $2.7\times10^{-15}$ |
| S2: numeric ratio $=24\sqrt3\pi$ | machine | $8.7\times10^{-16}$ |
| S2: signs $\rho_{a_0}<0<\rho_{196}$ | exact (sign algebra; restates S1) | — |
| S3: no positive saturation root, no real $H$ (flat) for $\rho<0$ alone | exact (sympy; elementary) | — |
| S4: $E(L)=\sigma_H L$, $\sigma_H=4\sqrt3\pi\hbar c/a^2$ | exact (sympy) | 0 |
| S5: sequestering residual independent of $C\in\mathbb R$ | exact (sympy) | 0 |

## Tests

`casim test --id F408-cc-sign-split` — **13/13 PASS**. `--control` — **5/5 CONTROL**: `lichnerowicz_E=0` → {S1-a1-positive, S1-eta-is-gstar-over-12, S1-sign-split, S2-cell-matches-content, S2-F196-positive, S4-tension-positive}; `fundamental_bosons=97` → {S1-a0-negative, S1-eta-is-gstar-over-12, S1-sign-split, S2-cell-matches-content, S2-F193B-negative, S2-ratio-closed-form, S3-no-saturation-for-a0, S3-no-horizon-for-a0}; `fundamental_vectors=12` → {S1-a1-positive, S1-eta-is-gstar-over-12, S1-sign-split, S2-cell-matches-content, S2-F196-positive, S2-ratio-closed-form, S4-tension-positive}; `zero_point_weight=0.5` → {S2-ratio-closed-form}; `sequester=false` → {S5-sequestering-sign-blind}. Journalled to `test-results/control-soundness.json` and `test-results/can-fail.json`. Of the 13 legs about half are independent computations (S1 arithmetic, the cell identity, the $I_\text{cc}$ grid, the S2 closed form, S3, S4 linearity, S5); the sign legs of S2 and S4 restate S1's signs by construction and are kept as bookkeeping.

## Honest scope

- **The $a_1$ sign has two imports**: the continuum Lichnerowicz $E=R/4$ (as F61 records), and the compositeness of all twelve gauge bosons (§2, input 2) — twelve fundamental vectors would make $\sum\eta=0$. The $a_0$ sign rests on the principal-branch filled-sea convention (§2, input 3).
- **Mode count.** F164's "$g_*=2$" is one Weyl field; F61's $g_*=48$ counts Weyl fields; the consistent S2 ratio uses both moments at 48 Weyl fields. F164's quoted $\rho_\text{vac}=3.46\times10^{111}$ is therefore $1/48$ of the model's full zero-point magnitude — a tree-wide units note, irrelevant to F164's 121-order statement but not to any $O(1)$ comparison.
- **S3 is elementary** — a one-sided bound cannot cancel a negative term — and is stated for $a_0$ alone in flat slicing. It does not show no local mechanism can remove $a_0$ (F332 and Weinberg's theorem cover that ground).
- **S4 is a reading, not a source.** The linear tension is the geometric (Friedmann-I) side; it adds no energy to $\rho$.
- **Nothing here adopts sequestering.** S5 strengthens CL303's case and removes an alternative; the adoption decision (decision-4 scope) is untouched.

## 8. Prior art

Nothing in S1, S4 or S5 is new physics. The opposite signs of fermionic $a_0$ and $a_1$ are standard in Sakharov induced gravity (Sakharov 1967; Visser, *Mod. Phys. Lett. A* **17**, 977 (2002); the spin-dependent heat-kernel coefficients in Vassilevich, *Phys. Rep.* **388**, 279 (2003)), including the negative $a_1$ weight of gauge vectors. $\rho\sim c^4/GL^2$ from a $\hbar c/a^2\times1/L^2$ product is the Cohen–Kaplan–Nelson (1999) / Li (2004) holographic relation. $E=c^4L/2G$ is the Schwarzschild $M=Rc^2/2G$ relation (cf. the maximum-force conjecture $c^4/4G$, Gibbons 2002). Sign-blindness is the defining property of Kaloper–Padilla sequestering (2014). **What is specific to this finding** is applying these to this model's own content and objects: that the two halves of the tree's live CC route carry opposite signs, the content-consistent ratio $24\sqrt3\pi$, the $g_*$ mismatch behind F193 §B's agreement, and the consequent restatement of G1.

## 9. Falsifiers

- **Any of the twelve gauge bosons being a fundamental propagating vector** (rather than composite, decision 5) moves $\sum\eta$ by $-1/3$ each; all twelve give $\sum\eta=0$ and remove the positive $a_1$ that §3–§7 rest on. Lever `fundamental_vectors`.
- **A fundamental bosonic tower of $>96$ real dof** flips $a_0$ positive and reopens the ceiling as a constraint on it (lever `fundamental_bosons`).
- **A lattice-native Lichnerowicz coefficient $E<R/6$** flips the per-Weyl $a_1$ (lever `lichnerowicz_E`).

## Reviewed & corrected

**2026-09-27 - 11:52** — attack pass: **CONFIRMED-NARROWER** (cold referee, 13 attacks: 5 PASS, 7 WEAKENS, 1 FAIL on attack 5, the handling of the $e$ coincidence). Found: (A) S2 mixed content — F193/F164's $g_*=2$ in $\rho_\text{vac}$ against the structural $G$, which is F79's induced $G$ at 48 Weyl fields — so the ratio first stated here, $g_*\sqrt3\pi/4$ ($2.72$ at $g_*=2$, "65.3 at $g_*=48$", "moves with $g_*$"), was an artifact; the consistent ratio is $24\sqrt3\pi=130.6$, content-independent, and the "$\approx e$" coincidence goes with the artifact. (B) The $a_1$ sign silently assumed no fundamental gauge vectors (12 would give $\sum\eta=0$). (C) The $a_0$ sign rests on a branch convention. Also: S3 overstated as "outside the domain" (it is an elementary one-sided-bound statement, flat slicing); the $a_1$ term was counted as a component of the solution though it is Friedmann-I; "only $a_0$-remover" should be "only non-local mechanism built"; withdrawing §B's object also withdraws F196's "dilution of $\rho_\text{vac}$" reading; prior art uncited; a `bool("false")` parsing bug, an `sp.ask`-None vacuous pass, and a divide-by-zero at $\sum\eta=0$. Fixed: S2 recomputed with content-consistent $N_b$ and $\sum\eta$ plus a cell–content leg; S1 split into sign and identity legs; `fundamental_vectors` lever and control added; three declared inputs, falsifiers and prior art written in; S3, §6, §7 and the G1/CL021/CL303/summary wording narrowed; the three code defects fixed. Rejected: none. Deferred: a lattice-native Lichnerowicz coefficient, and deciding whether the gauge link variables carry independent $a_1$ weight → `docs/status/open-derivations.md` G1.

## Status

Open, and now stated precisely: (i) whether to adopt a sign-blind $a_0$-remover (F367/CL303 and its F368 costs); (ii) a lattice-native Lichnerowicz coefficient for S1's $a_1$ leg, and whether the gauge link variables carry independent $a_1$ weight (the falsifier of §9); (iii) $\Omega_\Lambda$ (F241).
