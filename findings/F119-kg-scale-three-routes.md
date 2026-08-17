# F119 — Tying the kilogram into the mass sector: the overall scale $N$ factorises cleanly out of the derived spectrum, but all three closure routes converge on the same verdict — $N$ is the fermion-mass hierarchy, the 3D gap mechanism cannot generate it from $O(1)$ inputs (a sharp no-go), $W$ is $O(1)$-localised but its value still fitted, and gravity pins the cell $a$ rather than the mass scale

**Date:** 2026-06-09 - 15:40
**Status:** Partial (one clean factorisation + one sharp no-go + one $O(1)$ localisation + one consistency cross-check) — 8/8 checks PASS (`test_F119_kg_scale_three_routes.py`, <1 s). Pure numpy/math (no scipy, per CLAUDE.md). The headline: **the kilogram is already tied in *as a unit*** — once $a$ is locked (F107), $\hbar$ carries the kg and $m_\text{phys}=\hbar\arcsin(m_\text{lat})/(\tau c^2)$ returns kg with no free parameter. What is *not* derived is the single dimensionless overall scale $N\equiv m_\text{lat}(\tau)=5.54\times10^{-19}$ (since the condensate pins $m^\text{cond}_\tau\equiv1$). The condensate gives the *shape* (ratios, Koide, angle) to $10^{-12}$; $N$ is a clean multiplicative scale on top. **The three attempted closures all fail in the same instructive way:** $N$ *is* the fermion-mass hierarchy.
**Script:** `tests/findings/test_F119_kg_scale_three_routes.py`
**Results:** `test-results/F119_kg_scale_three_routes.json`
**Cross-references:** [[F118-self-consistent-Wvc-and-C]] (the $W$/$\lambda_6$ localisation this builds on and tests), [[F116-njl-calibration-bz-cutoff-induced-G]] (the lattice-BZ gap machinery reused in the no-go), [[F115-coupling-magnitudes-running-rotor]] (couplings non-running ⇒ no transmutation channel; the rotor value $g_s^2\chi=\tfrac14$), [[F101b-one-heavy-branch-fit-W]] (the wall-pinning $y_\tau=1$ and the "saturation↔MeV" ledger gap), [[F83-fix-lattice-spacing-from-fermion-mass]] (the mass map $(\triangle)$, the $m_\text{lat}$ table, the top-quark ceiling), [[F79-structural-newton-constant]] / [[F112-si-predictions-from-canonical-a]] (the locked cell and the genuine $G=3\times10^{-8}$ prediction), [[F46-pythagorean-lattice-mass]] ($\Omega_\text{rest}=\arcsin m$), [[F95-B-derived-C-localized]] (the derived cubic $B$).

---

## 1. The problem, stated precisely

With the cell locked by F79/F107,
$$a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=1.06638\times10^{-34}\text{ m},\qquad \tau=\frac{a}{c\sqrt3}=2.05366\times10^{-43}\text{ s},$$
the metre, the second **and** the kilogram are dimensionally fixed. The F46/F83 map
$$m_\text{phys}\,c^2=\hbar\,\frac{\arcsin(m_\text{lat})}{\tau}$$
turns any dimensionless $m_\text{lat}$ into a definite kg — $\hbar$ (J·s = kg·m²/s) carries the kilogram. So the project's recurring phrase "absolute masses need the one kg anchor" is, dimensionally, **already discharged**: there is no free kg knob, only the same $\{c,\hbar,G\}$ triple that fixed the metre and second.

The genuine open item is **one dimensionless number**. The condensate sector (F96/F101/F118) pins the heaviest generation at the saturation wall, $y_\tau=1$, $m^\text{cond}_\tau=y_\tau^2=1$ (F101-A0). The physical τ rest-leg is instead $m_\text{lat}(\tau)=\sin(m_\tau c^2\tau/\hbar)=5.54\times10^{-19}$. Define the **condensate→rest-leg normalisation**
$$\boxed{\;N\equiv\frac{m_\text{lat}(\tau)}{m^\text{cond}_\tau}=m_\text{lat}(\tau)=5.54\times10^{-19}.\;}$$
This finding attempts the three routes to derive $N$ that the status review proposed.

## 2. N1 — the scale factorises cleanly out of the derived shape

The F101/F118 minimiser gives $y=(1,\,0.2438,\,0.0170)$ and $m^\text{cond}_a=y_a^2=(1,\,0.05945,\,2.876\times10^{-4})$, which reproduces the measured mass **ratios** $m_\mu/m_\tau,\ m_e/m_\tau$ to $<10^{-12}$. Because $\Omega_\text{rest}\approx m_\text{lat}$ is linear at these tiny amplitudes, the physical rest-leg masses factor *exactly*:
$$m_\text{lat}(a)=N\cdot m^\text{cond}_a\qquad(\text{verified to }4\times10^{-7}\text{ for }\mu,e).$$
So the model's content splits cleanly: **shape (derived) × scale $N$ (the one open number).** Koide $Q=2/3$, the $E_g$ angle, and the generation hierarchy all live in the shape and are *independent of $N$*.

## 3. ROUTE 1 — N2/N3: the gap mechanism cannot generate $N$ (sharp no-go)

The natural mechanism for a small mass-to-cutoff ratio is dynamical mass generation — the same lattice-BZ NJL gap equation F116 uses ($1=g\,I_1(M)$, $I_1(M)=\langle(K(\mathbf k)+M^2)^{-1/2}\rangle_\text{BZ}$, $g_c=1/I_1(0)$). Inverting in the chiral limit ($g/g_c=I_1(0)/I_1(M)$) and fitting the onset:

$$\frac{g-g_c}{g_c}\sim M^{\,p},\qquad p=1.95\ \Rightarrow\ \boxed{M\sim(g-g_c)^{1/2}}.$$

This is the **3D second-order (mean-field square-root) transition** — *power-law*, not exponential. Reaching $M=N=5.54\times10^{-19}$ therefore demands
$$\frac{g-g_c}{g_c}\sim N^{2}\approx 2.8\times10^{-36},$$
i.e. tuning the contact to criticality at the $10^{-36}$ level. **Dimensional transmutation is absent in 3D**: a small mass is not generated from an $O(1)$ coupling.

**N3 — what would close it.** Exponential suppression $N=\exp(-K/g)$ with an $O(1)$ coupling needs $K=-g\ln N\approx42$ — i.e. a **logarithmically-running / marginal channel** (à la $\Lambda_\text{QCD}=\mu\,e^{-1/b_0g^2}$). F115 found the model's couplings essentially **non-running at the lattice scale** (the +12 % Weinberg gap is a TeV matching offset, not running; Planck-scale running overshoots). So the one channel that could generate $N$ from $O(1)$ inputs is currently **absent**. $N$ remains an input — but the *requirement* to derive it is now explicit and sharp: find a marginal coupling, or accept one calibration mass.

## 4. ROUTE 2 — W1/W2/W3: $W$ is $O(1)$-localised, value still fitted

**W1 (reproduce F118).** The brake is the unique symmetry-allowed $E_g$ clock self-interaction $C=\lambda_6 e^6$ with $W=6\lambda_6$. The derived cubic $B_\text{sea}=-5.69\times10^{-2}$ (full BZ, F95) plus the measured angle $\cos3\delta=0.785874$ give
$$\lambda_6=\frac{0.636\,|B|}{e^6}=0.243=O(1),\qquad W=1.46,$$
reproducing F118 exactly. Existence of the self-consistent $(W,v,c)$ is **closed** on the spontaneous-$E_g$ branch (F118-A2); only the *value* of $\lambda_6$ is open.

**W2 (test the $\tfrac14$ conjecture).** Imposing the rotor value $\lambda_6=g_s^2\chi=\tfrac14$ (F115) as an independent input *predicts* the angle:
$$\cos3\delta=\frac{|B|}{2\cdot\tfrac14 e^6}=0.765\ \Rightarrow\ \delta=13.36°,\qquad\text{measured }12.733°.$$
A $+0.63°$ residual (2.7 % in $\lambda_6$): **suggestive of a universal $\tfrac14$ contact but not exact for leptons.**

**W3 (no clean closed form).** The F95 small-amplitude form $B_\text{lead}=3\sqrt2\,I_2\bar y^4$ underestimates the full nonperturbative $B$ at the saturation amplitude $\bar y=0.42$ by a factor $\approx2$ ($|B_\text{full}|/B_\text{lead}=1.95$). So $\lambda_6$ has **no clean perturbative closed form** — it is genuinely a saturation-scale ($O(1)$, nonperturbative) number. Localised, not closed; the residual is exactly F118's.

## 5. ROUTE 3 — X1: gravity pins the cell $a$, not the mass scale

The gravity sector (F79/F107) fixes $a\to\tau$ and yields the project's genuine $G$ prediction to $3\times10^{-8}$ (F112; the round-trip identity $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ holds to round-off here by construction). The **same cell** places every PDG fermion at $m_\text{lat}<1$ — the heaviest, the top, at $m_\text{lat}=5.39\times10^{-17}$. But $a$ sits $\approx16.5$ decades **below** the top-quark mass ceiling $a_\text{max}=\sqrt d\,\tfrac\pi2\bar\lambda_C^{\text{top}}$ (F83). Hence gravity **pins $a$** (and therefore $\tau$, and therefore the kg via $\hbar$) but is $\sim17$ orders of magnitude from pinning the dimensionless mass scale $N$. The cross-check is **consistent** — one cell underlies gravity, light-bending, LIV, and the fermion masses simultaneously — but it does **not** close $N$, confirming F83's "second anchor pins $a$, not the mass."

## 6. The one story across the three routes

| route | result | what it settles |
|---|---|---|
| **kg as a unit** | already in: $\hbar$ + locked $\tau$ ⇒ kg, no free param | the "kg anchor" is not a separate knob |
| **shape** | ratios, Koide $Q=2/3$, $E_g$ angle, $y_\tau=1$ | derived, independent of $N$ |
| **R1: $N$ from the gap** | NO-GO: 3D power-law, needs $10^{-36}$ tuning; transmutation needs a marginal channel (absent, F115) | $N$ *is* the hierarchy |
| **R2: close $W$** | $\lambda_6=0.243\approx\tfrac14$, $O(1)$, existence closed (F118); value fitted; $\tfrac14$ predicts $\delta=13.4°$ vs $12.7°$ | $W$ localised, not closed |
| **R3: gravity** | $G$ to $3\times10^{-8}$, all $m_\text{lat}<1$, but $a$ 17 decades below the ceiling | pins $a$, not $N$ |

**Bottom line.** The kilogram is tied in dimensionally; the spectrum *shape* is predicted; the single overall scale $N$ remains an input — and we now know precisely *why* (no marginal/running channel to transmute it) and *what* would close it (a logarithmically-running coupling, or one accepted calibration mass that then makes every other mass a parameter-free kg prediction).

## 7. Test summary (`test_F119_kg_scale_three_routes.py`, 2026-06-09 - 15:40)

| Check | Statement | Result | Status |
|---|---|---|---|
| N1 | shape×scale factorisation; $N=m_\text{lat}(\tau)$ | ratios $<10^{-12}$, fact. $4\times10^{-7}$ | PASS |
| N2 | gap-mechanism no-go: $M\sim(g-g_c)^{1/2}$, tuning $\sim10^{-36}$ | $p=1.95$, $2.8\times10^{-36}$ | PASS |
| N3 | exponential closure needs marginal channel ($K\approx42$) | $K=42.0$ | PASS |
| W1 | reproduce F118: $\lambda_6=0.243$, $W=1.46$ | $B=-0.0569$ | PASS |
| W2 | $\lambda_6=\tfrac14$ predicts $\delta=13.4°$ vs $12.7°$ | $+0.63°$ | PASS |
| W3 | no clean closed form: $|B_\text{full}|/B_\text{lead}=1.95$ | nonperturbative | PASS |
| X1 | gravity pins $a$ (G to $3\times10^{-8}$), 16.5 decades below ceiling | consistent, not closing | PASS |
| V | verdict recorded | — | PASS |

**Overall 8/8 PASS** (<1 s).

## 8. Provenance

- New content: the clean shape×scale factorisation $m_\text{lat}=N\,m^\text{cond}$ (N1); the gap-mechanism no-go with the measured 3D transition exponent and the $10^{-36}$ tuning requirement (N2); the marginal-channel requirement $K\approx42$ (N3); the quantitative $\lambda_6=\tfrac14$ angle prediction (W2) and the nonperturbative-$B$ obstruction to a closed form (W3); the gravity consistency-vs-non-closure cross-check (X1).
- Machinery: `ca_bcc.bcc_dispersion` + F46 sea tables (L=24, F101/F118 convention); lattice-BZ gap equation (F116 NJ2); F79/F107 cell; PDG 2024 masses; CODATA 2018 constants.
- Verification: `tests/findings/test_F119_kg_scale_three_routes.py` (2026-06-09 - 15:40, 8/8 PASS), results `test-results/F119_kg_scale_three_routes.json`.
