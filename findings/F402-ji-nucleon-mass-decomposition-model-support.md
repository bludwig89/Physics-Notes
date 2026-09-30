# F402 — The Ji-type four-term nucleon-mass decomposition, built in the model's own sectors: the quark-mass term and the trace sector are supported ($\sigma_N=46$ MeV), the quark-energy / gluon-energy split is not

**Date:** 2026-09-24 - 09:40
**Status:** Confirmed as a construction and a verdict — 7/7 gate legs PASS, two declared negative controls verified sound (each flips the verdict; the driver does not name individual legs).
**Reviewed:** 2026-09-24 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F402-review-2026-09-24.md)) — every headline number independently recomputed from a blind task card (identical $\sigma_N$, dilatation terms, Cornell expectation values); the algebra and both string-sector results survived; narrowed in-session: the gluon-share deficit is $2.0$–$2.9\sigma$ depending on the lattice target (not $2.9\sigma$), it is a statement about the non-derived $x_g=0$ start at $\Lambda_\text{NJL}$, the NJL 'anomaly analogue' is an Euler-theorem identity rather than a model result, and the $\sigma_N$ undershoot is reference-dependent. Machine-precision identities (Hellmann–Feynman, dilatation, virial); quantitative comparisons. **This is a sum-rule + momentum-fraction construction; the operator-level $\langle N|F^2|N\rangle$ separation is NOT built** (see §6).
**Module:** `src/casim/engine/particles/baryon_mass_decomposition.py`
**Test record:** `F402-baryon-mass-decomposition` (gate, quantitative)
**Results:** `test-results/F402_baryon_mass_decomposition.json`
**Claim:** CL314
**Cross-references:** [[F122-p2-dynamical-baryon-three-body]] (the two-term split and the NR Cornell engine this extends), [[F123-p6-si-scale-matter-sector]] (the NJL $M_N=3m_c$ nucleon), [[F77-njl-gap-rpa-selfconsistent]] (the gap equation differentiated here), [[F144-route-a-alpha-s-dimensional-transmutation]] (the model's $\alpha_s(\mu)$, used for the evolution), [[F152-ir-coupling-the-irface]] (the frozen IR coupling band), [[F97-baryon-phase-closure-no-go]]; `docs/theory/notebook-v2/NB2-004-nucleon-mass-field-energy.md` "New questions opened" item 2 (the question this answers).

---

## 1. The question

NB2-004 closed with: *"F122 only separates 'quark mass sum' from 'confining string + kinetic energy' — two terms. The lattice literature's ~9% figure comes from a four-term operator decomposition (quark mass, quark energy, gluon field energy, trace anomaly). Whether the model's own gluon/colour-dielectric sector could support building the same four-term split is a larger, LONG-RUN question."* This finding builds what the model can build and reports what it cannot.

The lattice reference (Yang et al., chiQCD, PRL 121, 212001 (2018), $\overline{\rm MS}$ 2 GeV, percent of $M_N$; (stat)(sys) combined in quadrature): quark energy $H_E=33(6)$, quark mass $H_m=9(2)$ [$u+d+s$], gluon field energy $H_g=37(6)$, trace anomaly $H_a=23(1)$.

## 2. The construction — three inputs, two identities

With the nucleon at rest ($\langle T^{ii}\rangle=0$, so $\langle T^\mu{}_\mu\rangle=M$) the decomposition follows from

$$H_a=\tfrac14\,(M-H_m),\qquad H_E=\tfrac34\,(x_qM-H_m),\qquad H_g=\tfrac34\,x_gM,\qquad x_q+x_g=1,$$

which sum to $M$ identically. A model therefore has to supply only **(a)** the mass term $H_m=m\,\partial M/\partial m$ (Feynman–Hellmann) and **(b)** the momentum fractions $x_q,x_g$. Two consequences are structural, not dynamical, and must not be read as tests of the model: $H_a=\tfrac14(M-H_m)$ gives $22$–$24\%$ for **any** $H_m$ between $5\%$ and $9\%$, and $H_E+H_g=\tfrac34(M-H_m)$ likewise. **All the dynamical content is in $H_m$ and $x_g$.**

## 3. NJL constituent nucleon ($M_N=3M_c$, F77/F123): the mass term, exactly

The gap equation $M=m_0+4GN_cN_fM\,I_1(M)$ is differentiated implicitly in closed form ($dI_1/dM=\frac{M}{2\pi^2}(\Lambda/E_\Lambda-\ln\frac{\Lambda+E_\Lambda}{M})$):

- **Mass term (Feynman–Hellmann):** $H_m=\sigma_N=3m_0\,dM_c/dm_0=\mathbf{46.2}$ MeV ($dM_c/dm_0=2.80$; $4.95\%$ of $3M_c=933.6$ MeV). Agrees with the test's independent finite difference to $<10^{-6}$. Measured nucleon sigma term ($u+d$): $59.1(3.5)$ MeV (Hoferichter et al. 2015) and $60.9(6.5)$ MeV (FLAG 2024) — the model is **$-3.7\sigma$ / $-2.3\sigma$** (22% low) against these two precise values; individual lattice determinations span roughly $40$–$60$ MeV, so the undershoot is **reference-dependent** (the model sits between the low-lattice cluster and the dispersive/FLAG values), and it is not robust to the NJL parameter set (which was fitted to meson data, not to this). A parameter-free (no nucleon input) (inputs $\{\Lambda,G\Lambda^2,m_0\}$ were fitted to $m_c,f_\pi,m_\pi,\langle\bar qq\rangle$, none to a nucleon quantity), but a valence mean-field one with binding neglected as in F123.
- **Dilatation (the model's own trace sum rule), exact:** dimensional analysis of the gap equation gives $M_N=m_0\partial_{m_0}M_N-2G\partial_GM_N+\Lambda\partial_\Lambda M_N$, verified to $5\times10^{-14}$ (module) and $10^{-9}$ (test's own finite differences, four parameter points). **The contact term ($-2G\partial_G M_N=-5.14\,\mathrm{GeV}$) and the regulator term ($\Lambda\partial_\Lambda M_N=+6.03\,\mathrm{GeV}$) each exceed $M_N$ by $5$–$6\times$ with opposite sign**, and each depends on whether $G$ or the dimensionless $g=G\Lambda^2$ is held fixed, so **neither is meaningful alone**. Their sum is $\Lambda\partial_\Lambda M_N$ at fixed $g$, which Euler's theorem fixes to $M_N-H_m$ ($=0.9505\,M_N$): **the NJL 'anomaly-analogue' is an identity, not a dynamical result** — $H_a=\tfrac14(M_N-H_m)=23.8\%$ follows from it and the quarter rule and says nothing about the model beyond $H_m$.
- **Momentum fractions:** gluons are integrated out into $G$, so at $\Lambda_\text{NJL}$: $x_q=1$, $x_g=0$ — quartet $(H_E,H_m,H_g,H_a)=(71.3,\,4.95,\,0,\,23.8)\%$. A gluon share can only be generated by evolution.

## 4. Momentum-fraction evolution with the model's $\alpha_s$

LO second-moment evolution, $t=\ln\mu^2$: $dx_g/dt=\frac{\alpha_s}{2\pi}[\frac{16}{9}x_q-\frac{n_f}{3}x_g]$, closed form $x_g=x_\infty(1-e^{-\lambda\tau})$, $x_\infty=16/(16+3n_f)$, $\lambda=16/9+n_f/3$, $\tau=\int\frac{\alpha_s}{2\pi}d\ln\mu^2$ (closed form checked against RK4 to $10^{-9}$). Two lattice targets at 2 GeV $\overline{\rm MS}$: $x_g=\frac43\cdot0.37=0.49(9)$ (chiQCD-derived) and $0.427(92)$ (ETMC, arXiv:2003.08486). They **require $\tau=0.53$ / $0.40$**, i.e. a mean $\alpha_s\approx1.5$ / $1.1$ over $0.65\to2$ GeV. The model supplies:

| source of $\tau$ | $\tau$ | $x_g(2\text{ GeV})$ |
|---|---:|---:|
| model $\alpha_s$ (F144 chain, 4-loop; Landau scale $\approx0.9$ GeV), start at 1 GeV | 0.118 | 0.18 |
| + frozen IR coupling $\alpha^\ast_\text{eff}\in[0.38,0.41]$ (F152) from $\Lambda_\text{NJL}$ to 1 GeV | 0.169–0.174 | 0.24–0.25 |
| lattice requirement (chiQCD-derived / ETMC) | 0.53 / 0.40 | 0.49(9) / 0.427(92) |

The model's own coupling supplies $0.33$–$0.44$ of the required evolution (deficit factor $3.0$ / $2.3$): $x_g$ is **$2.9\sigma$ / $2.0\sigma$ low**, and the quartet after evolution is $(52.9,\,4.95,\,18.4,\,23.8)\%$ against chiQCD $(33,\,9,\,37,\,23)\%$ — $H_E$ high by $+3.5\sigma$, $H_g$ low by $-2.9\sigma$.

**The deficit is a statement about the starting point.** Everything above starts from $x_g=0$ at $\Lambda_\text{NJL}$ (the Parisi–Petronzio / Jaffe–Ross low-scale quark-model device: model-motivated — gluons are integrated out there — but not derived). Swept on review: $n_f$ above $m_c$ and the kernel $n_f$ move $x_g$ by $\sim0.003$; the F152 band moves it $0.24$–$0.25$; a frozen coupling up to $1.0$ reaches only $0.32$. A start of $x_g^0\approx0.1$ gives $0.31$, $0.3$ gives $0.43$ (`x_g_start_sensitivity`): the model's own $\tau$ reaches the lattice value only if the F123 constituent nucleon **already carries a gluon momentum share of $0.29$ (ETMC) to $0.40$ (chiQCD-derived) at $\Lambda_\text{NJL}$** — i.e. the finding is that the pure-constituent-quark start is too quark-rich by that amount, not that the model's $\alpha_s$ is wrong.

## 5. Cornell three-body string (F122): exact identities, unphysical numbers

The only model-native gluon **field** energy is the F122 string. With $\langle T\rangle,\langle V_\text{conf}\rangle,\langle V_\text{coul}\rangle$ from the ECG ground vector, the string's stress tensor (trace $2\langle V_\text{conf}\rangle$, Coulomb traceless, NR quark trace $m-T$) gives $H_m=3m-\langle T\rangle$, $H_E=2\langle T\rangle$, $H_g=\tfrac12\langle V_\text{conf}\rangle+\langle V_\text{coul}\rangle$, $H_a=\tfrac12\langle V_\text{conf}\rangle$, and:

- **Hellmann–Feynman, exact at fixed basis** (check B1, test's own finite differences): $m\,dM/dm=3m-\langle T\rangle$, $\sigma\,dM/d\sigma=\langle V_\text{conf}\rangle$, $\alpha_s dM/d\alpha_s=\langle V_\text{coul}\rangle$ to $1.6\times10^{-9}$, $3\times10^{-10}$, $6\times10^{-12}$.
- **The quarter rule is the virial theorem:** $H_a-\tfrac14(M-H_m)=-\tfrac14\,[2\langle T\rangle-\langle V_\text{conf}\rangle+\langle V_\text{coul}\rangle]$ exactly (an algebraic identity, checked to $10^{-9}$); the virial residual falls from $3.3\times10^{-3}$ (8-mesh) to $1.5\times10^{-5}$ (14-mesh; not strictly monotonic beyond — $\approx7\times10^{-5}$ at 18).
- **Numbers (units of $\sqrt\sigma$, $M=8.09$ baseline):** $(H_E,H_m,H_g,H_a)=(62.8,\,-2.3,\,13.9,\,25.6)\%$, $x_g=0.19$. **$H_m<0$: the NR mass term $3m-\langle T\rangle$ is negative** because the quark kinetic energy ($0.85\sqrt\sigma$ per quark) exceeds the constituent mass ($0.785\sqrt\sigma$) — $\bar\psi\psi=m/E>0$ relativistically, so the NR string solver **cannot supply the mass term** (F122 §5 already says its absolute numbers need relativising). The sign is parameter-dependent (found on review): $H_m$ stays negative at $\alpha_s=0.3$ ($-0.5\%$) and $m=0.6$ ($-11\%$), and turns positive at the F122 half-rule Casimir scaling: $(49.2,\,13.5,\,15.7,\,21.6)\%$, $x_g=0.21$, $H_m$ positive but $2.7\times$ the NJL value.

Notably the string route's $x_g\approx0.19$–$0.21$ and the evolution route's $0.18$–$0.25$ **agree with each other and both fall $\approx2\times$ short of the lattice $0.43$–$0.49$** (string $x_g$ stays $0.185$–$0.25$ across mesh, $m$ and $\alpha_s$ variations) — two independent model-native gluon-share estimates with one deficit (the string number carries the NR caveat above).

## 6. Verdict — what the model supports

| Term / statement | Verdict | Basis |
|---|---|---|
| Four-term structure, $H_a=\tfrac14(M-H_m)$, $H_E+H_g=\tfrac34(M-H_m)$ | **Supported (structural)** | exact identities in both sectors; $H_a=23.8\%$ vs $23(1)\%$ is **not** an independent test |
| $H_m$, light quarks | **Supported, 22% low** | NJL $\sigma_N=46.2$ MeV vs $59.1(3.5)$ / $60.9(6.5)$; exact FH |
| $H_m$, full $u+d+s$ ($9\%$) | **Not built** | SU(2) NJL has no strangeness |
| $H_E:H_g$ split | **Not supported** | model $x_g=0.18$–$0.25$ (two routes) vs $0.427(92)$–$0.49(9)$: $2.0$–$2.9\sigma$ low ($H_E$ $+3.5\sigma$, $H_g$ $-2.9\sigma$ vs chiQCD); needs mean $\alpha_s\approx1.1$–$1.5$, or a $0.29$–$0.40$ gluon share already at $\Lambda_\text{NJL}$ |
| NJL anomaly-analogue $M_N-H_m$ | **An identity** | Euler's theorem ($\Lambda\partial_\Lambda|_g$); the contact/regulator pieces depend on the choice of held-fixed variable and cancel at $5$–$6\times M$ |
| NR Cornell mass term | **Unphysical** | $H_m<0$ at the F122 baseline |
| Operator-level $H_g$ vs $H_a$ ($\langle N|F^2|N\rangle$, running $\beta$) | **Not built** | model has $\beta$ (F144) but no dynamical baryon in the gauge sector |

**Honest scope.** $H_m$ is $u+d$ only (the lattice $9\%$ includes strange; light-only reference is $\sigma_{\pi N}/M_N\approx6.3$–$6.5\%$). Evolution is LO, second moment, $n_f=3$, started from $x_g=0$ at $\Lambda_\text{NJL}$ (a choice the model motivates — the scale where gluons are integrated out — but does not derive), with $\alpha_s$ below $\approx0.9$ GeV replaced by the F152 frozen coupling (imported, not recomputed). The NJL derivatives use $M_N=3M_c$ (binding neglected, F123). The quarter rule assumes Lorentz invariance of the rest-frame nucleon; the NJL uses a 3-momentum cutoff, so there it is an assumption, whereas in the Cornell sector it is *derived* as the virial theorem.

---

## 7. Checks

| # | Check | Type | Result |
|---|---|---|:---:|
| A1 | NJL dilatation identity, test's own finite differences, 4 parameter points | machine ($10^{-9}$) | PASS |
| A2 | $\sigma_N=46.2$ MeV vs independent FD; undershoot band $-4.5<\text{pull}<-1.5$; control: $m_0\to2m_0$ leaves it | quantitative | PASS |
| B1 | Cornell Hellmann–Feynman ($m,\sigma,\alpha_s$) | machine ($10^{-9}$) | PASS |
| B2 | virial residual shrinks with basis; quarter rule $\equiv-\text{virial}/4$ | exact identity / quantitative | PASS |
| B3 | NR $H_m<0$ at baseline, half-rule $H_m>2\times$NJL, $x_g<0.25$; control: $m=5$ makes $H_m>0$ | quantitative | PASS |
| C1 | LO evolution closed form $=$ RK4 ($10^{-9}$), conservation, $x_\infty=16/(16+3n_f)$ | machine | PASS |
| C2 | model $x_g(2\text{ GeV})<0.30$, below both lattice targets by $1.5$–$3.5\sigma$; $\tau$ deficit factor in $[2.0,3.6]$; required start share in $[0.25,0.45]$ | quantitative | PASS |

## 8. Falsifiers

1. **A relativistic three-body string baryon (Salpeter kinetic energy, $V_0$ handled) whose $H_g$ reaches $\gtrsim30\%$ with $H_m>0$ and $\lesssim7\%$.** Would repair the NR sector and could close the $H_E/H_g$ deficit within the model's own string dynamics.
2. **A model-native $\alpha_s(\mu)$ (or IR-saturated coupling) below $\approx1$ GeV giving $\tau\gtrsim0.4$ (ETMC) / $0.53$ (chiQCD) from $\Lambda_\text{NJL}$ to 2 GeV, or a derived $x_g(\Lambda_\text{NJL})\gtrsim0.3$.** §4's deficit dies.
3. **A beyond-mean-field NJL nucleon (pion cloud, binding) that moves $\sigma_N$ to $\ge56$ MeV.** The $-2.3\sigma$ undershoot dies.
4. **A dynamical baryon in the gauge sector giving $\langle N|F^2|N\rangle$** — would permit the operator-level $H_g/H_a$ split, replacing the sum-rule route.

## 9. Provenance

- Module: `casim.engine.particles.baryon_mass_decomposition` (`particles`, `exactness=quantitative`, `_SPINE`, D11). Reuses `meson.gap_solve`/`I1_closed`, `baryon_dynamics` ECG kernels, `running_alpha_s.alpha_s_chain`/`run_alpha`, and the constants registry ($\Lambda_\text{NJL}$, $G\Lambda^2$, $m_0$, $\alpha^\ast_\text{eff}$ via `endpoint`). Comparison targets (lattice fractions, $\sigma_{\pi N}$) are literals labelled as targets, never inputs.
- Test record `F402-baryon-mass-decomposition`, `kind: assertion`, `tier: gate`, 7/7, controls `m0_MeV=11` (reddens A2) and `cornell_m=5.0` (reddens B3), both verified RED (flipping the verdict; the driver asserts rather than emitting a `checks` list, so individual legs are not named). Load-bearing identities re-derived in the test with its own finite differences / RK4.
- External: Yang et al., PRL 121, 212001 (2018), arXiv:1808.08677 (decomposition values); Ji, PRL 74, 1071 (1995) (the decomposition); ETMC, arXiv:2003.08486 (gluon momentum fraction $0.427(92)$); Hoferichter et al. 2015 and FLAG Review 2024, arXiv:2411.04268 (sigma term). **Prior art, stated plainly:** the four-term rule $H_a=\tfrac14(M-H_m)$ and the asymptote $16/(16+3n_f)$ are standard; radiative generation of the gluon share from a low-scale $x_g=0$ quark-model start is the classic Parisi–Petronzio / Jaffe–Ross device; an NJL nucleon sigma term is a known quantity. What is new is the assembly inside this model's own sectors and the verdict on each term.
- **Supersedes nothing.** F122, F123 left bit-unchanged; NB2-004 item 2 is marked in the ledger.
