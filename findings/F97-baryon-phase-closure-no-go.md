# F97 — No F92-type fixed point for three constituents: the baryon's binding force and stability point are both centre-phase closure

**Date:** 2026-06-05 - 13:35
**Status:** Theoretical (no-go proven) — 7/7 checks PASS; P1–P6 algebraically exact, P7 quantitative data anchor. **What is derived (exact):** the F92 consistency construction (pair-sum law + Fock-normalized amplitude law) has **no joint solution inside the stability domain for three constituents** — both candidate fixed points land in a forbidden gap that opens for $N\ge3$ and provably does not exist for $N=2$. **What is theorized (structural, built on F70/F71/F86/F94, not newly derived):** the baryon sector obeys the *same grammar* as F92 — stability = exact closure of a phase budget, and the object enforcing the budget is itself the binder — but with the $\mathbb{Z}_3$ centre phase in place of the unitarity wrap. **What this predicts:** baryon mass cannot come from constituent phase kinematics (confirmed: PDG quark sum is 0.96% of $m_p$), and the only stable colour combinations are N-ality-0 closures (confirmed structurally by F71/F86).
**Script:** `model-tests/test_F97_baryon_phase_closure.py` (<1 s)
**Results:** `test-results/F97_baryon_phase_closure.json`
**Numbering note:** drafted as F96; renumbered **F97** (F96 taken by the concurrent second-shell E$_g$ gap finding).
**Cross-references:** [[F92-per-constituent-phase-consistency]] (the $N=2$ law this extends/negates), [[F73-spin0-bound-pair-scalar]] (pair-sum law, over-wrap cap), [[F78-koide-amplitude-from-cooper-pair]] (bilinear law), [[F69-paired-spinor-photon]] (phase-sum rule), [[F71-colour-singlet-baryon-proton]] ($\varepsilon_{abc}$ singlet, $C_2=0$), [[F70-gradient-flow-confinement-string-tension]] / [[F94-lattice-gauge-mc-confinement-vs-F86]] (area law $\sigma$), [[F86-colour-dielectric-dual-superconductor]] (the condensate-as-binder), [[F93-orthorhombic-Eg-vacuum]] (flavor-space E$_g$ — kept distinct from the colour question, §6).

---

## 1. The question

F92 showed that for a **two**-constituent bound state the model's two mass laws — L1 pair-sum kinematics $m=\sin(Nt)$ and L2 the Fock-normalized amplitude law — are jointly satisfiable at exactly one angle, $t=45°$, where three saturations coincide (amplitude unitarity $y=1$, composite mass peak $m=1$, phase wrap $Nt=\pi/2$). The consistency point *is* the stability point, and the unitarity budget that defines it *is* the binding statement ("the pair amplitude exactly fills unitarity").

Question (this finding): does the same law hold for the colour-neutral **three**-quark combination — is there an F92-type fixed point that is simultaneously the binding condition and the stability point of the baryon?

## 2. The honest answer: a no-go theorem (exact)

Extend the F92 machinery to $N=3$ with no new assumptions:

- **L1(3):** phase per tick = sum of constituent phases (F69/F73), so $m_\text{comp}=\sin(3t)$.
- **Fock:** the three-quantum matrix element gives $y=\sqrt3\,\sin t$ (P2-analog; $\langle2|a|3\rangle=\sqrt3$).
- **L2(3):** two natural readings — trilinear $m=y^3$ (the baryon operator $\varepsilon_{abc}qqq$ is trilinear, F71) or the F78 bilinear $m=y^2$ unchanged.

Both have a unique fixed point on $(0°,90°)$, in closed form:

| variant | consistency condition | fixed point | $t^*$ | $3t^*$ |
|---|---|---|---|---|
| trilinear $m=y^3$ | $3\sqrt3\sin^3t=\sin3t$ | $\sin^2 t^*=\dfrac{9\sqrt3-12}{11}$ | $34.831°$ | $104.49°$ |
| bilinear $m=y^2$ | $3\sin^2t=\sin3t$ | $\sin t^*=\dfrac{\sqrt{57}-3}{8}$ | $34.662°$ | $103.98°$ |

**Both over-wrap.** The F73 stability bound requires $3t\le\pi/2$, i.e. $t\le30°$ — equivalently a per-constituent cap $m_c\le\sin(\pi/6)=\tfrac12$ **exactly** (the $N=3$ analog of F73's $1/\sqrt2$). Both fixed points sit at $\approx34.7°$–$34.8°$, past the wrap cap. There is **no angle at which a three-constituent state satisfies both mass laws and is stable.**

### Why $N=2$ is special — the cap-coincidence theorem (P2, exact)

The two saturations are: amplitude unitarity $t\le\arcsin(N^{-1/2})$ and phase wrap $t\le\pi/(2N)$. They coincide **iff** $\sin\!\big(\tfrac{\pi}{2N}\big)=N^{-1/2}$, which holds exactly at $N=1$ (trivial) and $N=2$ ($\sin45°=1/\sqrt2$) and **fails strictly for all $N\ge3$**: since $\sin x<x$ and $\tfrac{\pi}{2N}<N^{-1/2}\iff N>\tfrac{\pi^2}{4}\approx2.47$, for $N\ge3$ we get $\sin\frac{\pi}{2N}<\frac{\pi}{2N}<\frac1{\sqrt N}$. For $N=3$ a forbidden gap $(30°,\,35.264°)$ opens between the wrap cap and the unitarity cap — and both candidate fixed points land **inside that gap** (P5): allowed by unitarity, killed by over-wrap.

**F92's triple coincidence is therefore a two-body theorem, not a generic law.** The 45° fixed point exists because — and only because — $\pi/4$ is simultaneously the half-budget angle and the $1/\sqrt2$ amplitude. No third constituent can join that closure.

## 3. The no-go is itself a successful prediction (P7)

If the baryon *could* sit at an F92-type fixed point, its mass would be constituent phase kinematics, bounded by the sub-additive sum $m_B\le m_u+m_u+m_d$ (F73). The measured proton:

$$\frac{2m_u+m_d}{m_p}=\frac{2(2.16)+4.67}{938.272}=0.96\%\qquad(\text{PDG }\overline{\rm MS},\ 2\ {\rm GeV}).$$

Baryon mass is **not** phase kinematics — it is $\sim99\%$ field energy. The model is forced to this by the no-go, and it already owns the mechanism: the F70/F94 area law and the F86 colour-dielectric condensate. The lepton sector (no colour, no confinement) is exactly the sector where the pure phase chain *can* and *does* close (F92, Koide $Q=2/3$); the baryon sector is exactly the sector where it *cannot*. The split in the model matches the split in nature.

## 4. The theorized law: same grammar, different budget

What survives the no-go — and this is the answer to the question — is the **structure** of F92, transplanted one level up:

> **Closure principle (theorized).** A stable composite is a configuration whose phase budget closes exactly; the object that enforces the budget is itself the binding agent. Non-closure is priced either by over-wrap (kinematic instability, the pair sector) or linearly in separation (confinement, the colour sector).

| | pair sector (F92) | baryon sector (this finding) |
|---|---|---|
| budget | unitarity wrap $\pi/2$ | $\mathbb{Z}_3$ centre phase, $2\pi$ |
| per-constituent share | $45°$ ($\pi/4$ each, 2 ways) | $2\pi/3$ each, 3 ways |
| closure condition | $y=\sqrt2\sin t=1$ at $t=45°$ | $\sum$ centre phases $\equiv0\pmod{2\pi}$ (N-ality 0) |
| enforcer = binder | unitarity of the one-tick mass step (F27/F46) | colour-dielectric condensate $\varepsilon_c$ (F86), priced as $\sigma R$ (F70/F94) |
| stability point | the 45° fixed point (unique) | the $\varepsilon_{abc}$ singlet, $C_2=0$ (unique in $3^{\otimes3}$, F71) |
| cost of non-closure | over-wrap, $m$ past peak | linear potential, infinite isolation energy |

The closure arithmetic is exact (P6): $qqq$: $3\times\tfrac{2\pi}3=2\pi\equiv0$ ✓; $q\bar q$: $\tfrac{2\pi}3-\tfrac{2\pi}3=0$ ✓; diquark $qq$: $\tfrac{4\pi}3\not\equiv0$ — confined, never asymptotic. So the baryon's "stability point" is not an angle on a mass curve; it is the unique point where the colour phase budget wraps completely. And the binding force is not a new ingredient — it is the same condensate that defines the budget, exactly as the F92 unitarity budget was enforced by the same mass-step rotation it constrains.

**What is and is not claimed.** Each row of the table is individually established (F27/F46, F70, F71, F86, F94). The new content is (i) the exact no-go of §2, which *forces* the baryon onto a different closure principle, and (ii) the identification of the two sectors as instances of one grammar. Not derived here: a dynamical demonstration that $\sigma$ emerges as the Lagrange-multiplier price of centre-phase non-closure in the QCA update rule (the F86 dielectric gets close in form; the bridge is future work, parallel in spirit to F92 §6's open bridge).

## 5. Falsifiable handles

1. **Spectrum selection rule:** only N-ality-0 combinations appear as asymptotic states — $qqq$, $q\bar q$, pentaquark $qqqq\bar q$, hexaquark, hybrids. Any confirmed free diquark or fractionally-charged asymptotic state falsifies the closure principle. (Matches all observed hadrons to date.)
2. **Per-constituent cap:** any future attempt to build a *phase-bound* (non-confined) three-body composite in the model must respect $m_c\le1/2$ in lattice units, and cannot satisfy both mass laws — a sharp internal consistency check on later constructions.
3. **No baryonic Koide from constituents:** the model predicts there is **no** exact algebraic relation of the F92 type among baryon masses derived from constituent rest phases; baryon masses are set by $\sigma$ and the condensate (Tier-B calibration). An exact constituent-phase baryon mass formula appearing in the data would falsify the no-go's relevance.

## 6. Boundary of the claim (read this)

This finding is about the **colour/constituent** level. It says nothing against a quark **generation-space** Koide relation: F92's $t$ is the generation polar angle, and the F93 E$_g$ vacuum machinery is flavor-space, colour-blind. Whether the quark generation triples inherit the F92 closure (the heavy-quark triple $(c,b,t)$ is known in the literature to sit near $Q\approx2/3$, but with scheme/running-mass ambiguities the leptons don't have) is a separate, open question — flagged, not claimed, and worth its own finding if pursued.

## 7. Test summary (`test_F97_baryon_phase_closure.py`, 2026-06-05 - 13:32)

| Check | Statement | Result | Status |
|---|---|---|---|
| P1 | $N=2$ regression: unique $\{\pi/4\}$; caps coincide | exact | PASS |
| P2 | caps coincide iff $N\in\{1,2\}$; strict split $N\ge3$ | exact | PASS |
| P3 | trilinear fixed point $\sin^2t^*=(9\sqrt3-12)/11$; $3t^*=104.49°$ over-wraps | $0$ (50 dp) | PASS |
| P4 | bilinear fixed point $\sin t^*=(\sqrt{57}-3)/8$; $3t^*=103.98°$ over-wraps | $0$ (50 dp) | PASS |
| P5 | both fixed points inside forbidden gap $(30°,35.264°)$; cap $m_c\le1/2$ exact | exact | PASS |
| P6 | $\mathbb{Z}_3$ closure: $qqq\to0$, $q\bar q\to0$, $qq\to4\pi/3\ne0$ | exact | PASS |
| P7 | PDG quark-sum/proton $=0.96\%$ | quantitative | PASS |

**Overall 7/7 PASS** (<1 s).

## 8. Provenance

- New content: the $N\ge3$ no-go theorem and cap-coincidence theorem (§2); the closure-principle synthesis (§4); the falsifiable handles (§5). Everything in the §4 table other than the synthesis is prior work (F27/F46/F69/F70/F71/F73/F78/F86/F92/F94).
- Verification: `model-tests/test_F97_baryon_phase_closure.py` (2026-06-05 - 13:32, 7/7 PASS), results `test-results/F97_baryon_phase_closure.json`.
- Data: PDG quark masses $m_u=2.16$, $m_d=4.67$ MeV ($\overline{\rm MS}$, 2 GeV), $m_p=938.272$ MeV.
