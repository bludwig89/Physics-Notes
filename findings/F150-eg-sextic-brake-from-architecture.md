# F150 — The $E_g$ sextic brake $C/W$ from the architecture: F147's rigidity theorem + F95's per-axis no-go close the **source** (a condensate self-coupling, two-route), F145's induced-coupling Fierz fixes the **kind** (legitimizing the F115/CM4 "notation collision"), and the magnitude joins the single QCD-sector IR residual — with the sharpened target $\cos3\delta^*=\cos Q$ ($3\delta^*=Q=\tfrac23$ rad, $1.7\times10^{-5}$)

**Date:** 2026-06-12 - 16:20
**Status:** Partial (a source closure + a kind identification + a residual merge + a sharpened target) — 5/5 checks PASS. **What this establishes:** (i) the brake $C$ **cannot** come from the free fermion sea — two independent no-gos now converge (F95's per-axis scaling/sign + F147's *exact-zero* one-tick rigidity in every channel), so $C$ is necessarily a **condensate self-coupling**; (ii) condensate self-couplings in this model are **induced couplings** with exact rational Fierz projections (F145, today), which retroactively **legitimizes** the proximity $\lambda_6\approx\tfrac14$ that F115/CM4 had to flag as an unjustified "notation collision" — F145 supplies the very mechanism F115 said was missing; (iii) the **exact value** of $\lambda_6$ is the *same single nonperturbative IR-coupling normalization* that already owns the F124/F144/F145 residuals — the lepton brake is now part of one residual cluster, not a separate fitted number; (iv) the convention-independent target $\cos3\delta^*=-B/(2C)=0.785874$ equals $\cos Q$ ($Q=\tfrac23$ the Koide ratio, F92) to $1.7\times10^{-5}$, i.e. $3\delta^*=Q=\tfrac23$ rad — both are invariants of the **same** second-shell $E_g$ condensate. **What remains (the honest residual, unchanged in kind but now localized):** the first-principles magnitude $\lambda_6$ (equivalently whether $3\delta^*=Q$ is exact) is the flavor-resolved **saturated-condensate** induced-coupling solve that F92 §6 / F95 §7 / F118 §7 all leave open; this finding does not perform it. See §7.
**Module:** (analysis-only; reuses `ca-simulation/ca_bcc.py`, F95/F118 closed forms)
**Script:** `tests/findings/test_F150_eg_sextic_brake.py` (~1 s, numpy + stdlib, real arithmetic only — no chiral transforms)
**Results:** `test-results/F150_eg_sextic_brake.json`
**Cross-references:** [[F147-walk-loop-rigidity-channel-equality]] (the one-tick gauge-rigidity theorem: zero induced stiffness in **every** channel — the new no-go pillar; its §2 reading "the gauge stiffness cannot come from the free fermion sector… it must come from the condensate sector F118" is exactly the statement applied here to the $E_g$ brake), [[F145-route-c-induced-njl-coupling]] (the induced-coupling template: exact Fierz $c=\tfrac29$, the bare-vs-running bracket, and "one number owns all three residuals" — the mechanism this finding ports to the condensate self-coupling), [[F95-B-derived-C-localized]] (the per-axis no-go and the localization of $C$ to the second-shell condensate; the derived $B=-3\sqrt2\,I_2\bar y^4$), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the $\lambda_6=0.243\approx\tfrac14$, $W=6\lambda_6=1.46$ localization this derives the *source/kind* of, and the wrong-sign sea-loop result B1), [[F93-orthorhombic-Eg-vacuum]] (the $\cos3\delta^*=-B/(2C)=0.7859$ target and the §8 flag "$\delta\approx2/9$ rad / $\cos(2/3)$", recorded there as a target — now given an architectural rationale), [[F92-per-constituent-phase-consistency]] ($Q=2/3$ from the $45°$ equipartition; the saturated-pair normalization the brake build needs), [[F115-coupling-magnitudes-running-rotor]] (CM4 the "notation collision" this resolves; CM3 the rotor lock $g_s^2\chi=\tfrac14$), [[F49-bcc-finite-k-weinberg-angle]] / [[F141-ws-cell-7axes-onshell-mass-counting]] (the *other* $2/9$), [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] / [[F144-route-a-alpha-s-dimensional-transmutation]] (the shared IR-coupling residual the brake now joins).

---

## 1. The object and the open input

F93/F95/F118 reduced the entire charged-lepton mass texture, beyond the count (F75) and $Q=2/3$ (F92), to **one** number: the ratio of the two $E_g$ Landau invariants of the second-neighbour condensate,

$$F(\delta)=B\cos3\delta+C\cos^23\delta,\qquad
\cos3\delta^*=-\frac{B}{2C}=0.785874 .$$

F95 **derived $B$** from the QCA Dirac sea — closed form $B=-3\sqrt2\,I_2\,\bar y^4$, $I_2=\langle\cot\omega\rangle_\text{BCC}=0.2202$, sign $B<0$ (data on the hierarchical side) — and proved $C$ **cannot** be any per-axis sea energy (it would scale as $\bar y^{\,7}$ against $B\sim\bar y^{4}$, locking the angle by 31 decades; F118-B1 added that the sea loop's own sextic is even *wrong-sign* at saturation). F118 then **localized** $C$ to the $E_g$ clock self-interaction $C=\lambda_6\,e^6$ and fitted $\lambda_6=0.636|B|/e^6=0.243\approx\tfrac14$, $W=6\lambda_6=1.46$ — but flagged the first-principles value of $\lambda_6$ as the one remaining fitted number in the lepton sector.

Two findings dated **2026-06-12** change what can be said about that number. This finding combines them.

## 2. The source is closed by a two-route no-go (F95 ⊕ F147)

F147 proved a **one-tick gauge-rigidity theorem**: the half-filled free walk sea has **exactly zero** static response to any plane-wave gauge field, in **every** channel (vector *and* staggered/hypercharge), to $10^{-12}$ at field strengths up to $\varepsilon=0.3$ — mechanism the spectral closure $\theta\to\pi-\theta$ plus bipartiteness. Its own §2 reading: *"the gauge stiffness cannot come from the free fermion sector… it must come from the condensate sector (F118)."*

Apply this to the brake. F95's no-go was *amplitude-scaling-and-sign* specific to per-axis energies; F147's is *categorical* (zero induced quadratic response of the free sea, full stop). Together:

> **The brake $C$ cannot arise from the free fermion sea by any mechanism — neither a per-axis loop (F95: wrong scaling and wrong sign) nor any sea-induced response at all (F147: exactly zero, every channel). $C$ is necessarily a self-interaction of the condensate sector.**

This is the same destination F141 §4 and F143 §5 reached for the gauge stiffness; F150 records that the $E_g$ brake lands there too, by the convergence of the two no-gos. The check S5 reproduces the F95 scaling separation ($B\sim\bar y^{3.99}$ vs $C_\text{loop}\sim\bar y^{7.2}$) as the independent half of the pillar.

## 3. The kind is fixed by F145, and the F115/CM4 "notation collision" is resolved

F115/CM4 was forced to a **no-go**: identifying the "$e$" in F95's $e^6\cos^23\delta$ (the $E_g$ order-parameter amplitude) with the gluon coupling $g_s$ "would be an unjustified notation collision… the two are unrelated by anything established in the model." That was correct *at the time* — no mechanism connected the generation-space condensate coupling to the colour/binding sector.

F145 (today) is that mechanism. It established that the model's contact self-couplings are **induced couplings**: integrate out the heavy binding exchange (the dual-Meissner/dielectric gluon), Fierz-project onto the symmetry-allowed invariant, and read off an $O(1)$ coefficient that is an **exact rational** — the NJL quartic is $c=\tfrac29=\underbrace{\tfrac49}_{\text{colour}}\!\times\!\underbrace{1}_{\text{Dirac}}\!\times\!\underbrace{\tfrac12}_{\text{flavour}}$, identical in all four chiral channels. The condensate's *higher* self-couplings (the cubic that builds $B$, the sextic clock that is $C$) are generated by the **same** integrating-out, one and two orders higher.

Therefore $\lambda_6$ is an **induced three-body self-coupling** of the second-shell $E_g$ condensate: $O(1)$, rational-structured, sourced by the binding sector. The bridge F115/CM4 said was absent now exists — so the proximity $\lambda_6=0.243\approx\tfrac14$ (F118) is **not** a coincidence to be apologized for; it is the induced-coupling architecture, and the relevant rationals are exactly the binding/rotor block's recurring numbers.

## 4. The magnitude joins one residual cluster (not a separate fit)

$C=\lambda_6 e^6$ is a *sextic* (three order-parameter insertions per side, $|\Phi^3|^2$): it can only be at $O(1)$ relative to the cubic $B$ in the **saturation regime** — the unit-budget internal amplitude F92 found for the pair ($y=\sqrt2\sin t\le1$, $t=45°$) and F95 §6 found the loop sextic finally approaches the needed strength at. This is the *same* regime, and the *same* nonperturbative object, as the open QCD-sector residual:

| residual | finding | what fixes it |
|---|---|---|
| $G/G_c$ (χSB point) | F145 §5 | nonperturbative IR coupling (bare $0.1$ < fit $1.28$ < running $2.6$–$15$) |
| $\sqrt\sigma/f_\pi$ (12%) | F124 §5 | the one scale-setting / IR constant |
| $\Lambda$ scheme constant | F144 A4 | the same ($\approx1.8$) |
| $\lambda_6$ ($E_g$ brake) | **F150 (here)** | the **same** IR-coupling normalization at saturation |

So the lepton brake stops being an isolated fitted number: its exact value is set by the one IR-coupling normalization the strong sector already isolates. The fitted $\lambda_6=0.243$ is **bracketed** by the binding/rotor block's two recurring $O(1)$ rationals — the Fierz $\tfrac29=0.2222$ (F145/F49) and the rotor $g_s^2\chi=\tfrac14=0.250$ (F115/F45) — sitting between them, structurally as F145's own fit sits between its bare and running brackets (S4). What selects the exact point inside the bracket is the IR residual above, not new physics.

(The bracketing is stated for orientation; $\lambda_6$ itself is convention-laden through the $e^6$ normalization and the $0.636$ factor. The **convention-independent** statement is the ratio $\cos3\delta^*=-B/(2C)$ — §5.)

## 5. The sharpened target: $\cos3\delta^*=\cos Q$, i.e. $3\delta^*=Q=\tfrac23$

Because $B$ is derived (F95), predicting $C$ is equivalent to predicting the angle $\cos3\delta^*=-B/(2C)$. From the PDG leptons (S1–S2): the $Z_3$ decomposition gives $A/\bar y=1.41420$ (the $\sqrt2$ equipartition, F80/F92) and the generic angle $\delta^*=12.7328°$, reproducing $\cos3\delta^*=0.785874$ (F93).

The architectural target (S3): this equals the cosine of the **Koide ratio**,

$$\boxed{\;\cos3\delta^*=\cos Q\;}\qquad Q=\frac{\sum m_a}{(\sum\sqrt{m_a})^2}=0.666661\;(\to\tfrac23,\ \text{F92}),$$

with $\cos Q=0.785891$ vs the data $0.785874$ — agreement to $1.7\times10^{-5}$, i.e. $3\delta^*=Q=\tfrac23$ rad to $4\times10^{-5}$. (Equivalently $\delta^*=\tfrac29$ rad, the same $2/9$ as the F145 Fierz coefficient and the F49 Weinberg ratio — F93 §8 flagged exactly this.) The **rationale**, now available where F93 had none: $3\delta^*$ (the angular minimum of the $E_g$ clock) and $Q$ (the radial equipartition invariant) are invariants of the **one and the same** second-shell $E_g$ condensate at saturation; $Q=\tfrac23$ is *derived* (F92, from $t=45°$); the induced-coupling framework (§3) makes $B$ and $C$ — hence $-B/(2C)$ — computable in principle from that same saturated condensate.

This is a **target with a rationale**, not a derivation: relating an angular measure ($3\delta^*$ in radians) to a dimensionless ratio ($Q$) is exactly the kind of identity only the saturated-condensate solve can confirm. Recorded as the sharpened form of F93's flag.

## 6. What this finding is and is not

- **Is:** a *source closure* (two-route no-go, §2), a *kind identification* (induced coupling, §3, resolving F115/CM4), a *residual merge* (the brake joins the single IR-coupling cluster, §4), and a *sharpened target* with rationale ($\cos3\delta^*=\cos Q$, §5).
- **Is not:** a first-principles computation of $\lambda_6$. That requires the flavor-resolved **saturated-condensate pairing solve** — measuring the $E_g$ order parameter's cubic and sextic induced self-couplings from the constituent contact at the unit-budget amplitude — which F92 §6, F95 §7, and F118 §7 all name as the remaining build. F150 specifies *what that solve must produce* ($\lambda_6$ such that $-B/2C=\cos Q$; an induced 3-body coupling in the binding/rotor block) and *why it is well-posed* (the source and kind are now fixed), but does not run it.

## 7. The residual, sharply

One number — the nonperturbative IR coupling at the saturation/confinement scale — now fixes, simultaneously: the χSB point $G/G_c$ (F145), the $\sqrt\sigma/f_\pi$ ratio (F124), the $\Lambda$ scheme constant (F144), **and** the $E_g$ brake $\lambda_6$ (here). Equivalently, the single still-open lepton-sector input ("the $E_g$ Landau ratio", F84 input #2 residue) is no longer independent of the strong sector: it is the *same* IR-coupling normalization, evaluated for the second-shell condensate's induced sextic. The deepest open problem of F93 ("derive $B$ and $C$ from the rule") is, after F95 (B) and F150 (C's source/kind/cluster), reduced to *one* nonperturbative number shared across the whole confining sector — to be delivered by the saturated-condensate solve.

## 8. Check summary (`test_F150_eg_sextic_brake.py`, 2026-06-12 - 16:18)

| Check | Statement | Tier | Result |
|---|---|---|---|
| S1 | $Z_3$ data decomposition: $A/\bar y=\sqrt2$ ($2\times10^{-5}$), $\delta^*=12.73°$ generic | data | PASS |
| S2 | $\cos3\delta^*=-B/(2C)=0.785874$ reproduced | data | PASS |
| S3 | $\cos3\delta^*=\cos Q$, $Q=2/3$, $3\delta^*=Q$ to $4.3\times10^{-5}$ | target | PASS |
| S4 | $\lambda_6=0.243$ bracketed by $\tfrac29$ (F145/F49) and $\tfrac14$ (F115/F45); $C_\text{req}/\lvert B\rvert=0.636$ | bracketing | PASS |
| S5 | per-axis loop scaling separation ($B\sim\bar y^4$, $C_\text{loop}\sim\bar y^7$) — the F95 half of the no-go | structural | PASS |

**Overall 5/5 PASS** (~1 s).

## 9. Provenance

- **New content:** the two-route source no-go (F95 ⊕ F147) for the $E_g$ brake; the induced-coupling *kind* identification via F145, resolving the F115/CM4 notation no-go; the merge of $\lambda_6$ into the single F124/F144/F145 IR-coupling residual; the $\cos3\delta^*=\cos Q$ ($3\delta^*=Q=\tfrac23$) sharpened target with its condensate-invariant rationale.
- **Reused:** F95 closed-form $B$ and per-axis no-go; F118 $\lambda_6$/$W$ localization and wrong-sign sea loop; F147 rigidity theorem; F145 induced Fierz $\tfrac29$ and residual-cluster logic; F92 $Q=2/3$ and the saturated-pair normalization; F93 angle data and §8 flag; F115 CM3/CM4.
- **Verification:** `tests/findings/test_F150_eg_sextic_brake.py` (2026-06-12 - 16:18, 5/5 PASS), results `test-results/F150_eg_sextic_brake.json`. Real arithmetic only (PDG masses + the F95/F118 closed forms) — no chiral transforms, numpy-safe.
- **Masses:** PDG ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86$ MeV).
