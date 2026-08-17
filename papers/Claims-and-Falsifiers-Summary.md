% A Universe in a Bottle — Claims and Falsifiers
% B. Ludwig (independent researcher)
% 2026-08-04 (revision 4; first issued 2026-06-08)

> **Revision 4 — 2026-08-04 - 23:55.** Two changes, one an **addition** and one
> **structural**. **(i)** The charged-lepton **shape angle** is added as core claim 11.
> $\delta^*=\tfrac29$ rad has been a *founding principle* of the model since
> 2026-07-16 (F253/F255/F256), and revision 3 — issued seventeen days later — did not
> carry it. That gap is the reason for the second change. **(ii)** This document is no
> longer the register. Every claim below now has a **card** in `docs/claims/`, with a
> status, a falsifier field, and the findings it rests on; `claims-index.md` lists all
> of them and `make gate` fails a card that says `live` while every finding under it is
> superseded. A prose summary could record the revision-2 withdrawals and the revision-3
> correction only as blockquotes — true, but not checkable, not discoverable from the
> finding, and not countable. See §"Where the claims live" at the end.

> **Revision 3 — 2026-08-02 - 09:12.** One change, and it is an **addition**, not a
> withdrawal: revision 2's Scope entry on **charge quantisation was wrong**, and understated
> a result the tree already had. F165 (2026-06-29) derives the hypercharge assignment up to
> one overall normalisation; revision 2 listed it as an input. **F279** adjudicated the
> contradiction by re-deriving the constraint system independently, upheld F165's conclusion,
> and corrected its attribution — the closing constraint is the F47 Higgs-free Majorana step,
> not the gravitational anomaly. Charge quantisation moves from **Scope** to a **core claim**
> (new claim 10). The residual input is named: one charge unit, plus $N_c=3$ for the specific
> thirds.

> **Revision 2 — 2026-08-02 - 10:15.** Issued against audit-V items V-024, V-029, V-030 and
> V6.8. Four changes, all withdrawals or corrections, none an addition of new physics:
> **(i)** the horizon-free black hole and its four dependent falsifiers are **withdrawn** —
> superseded by F178, under which the exact vacuum solution is Schwarzschild and the
> exponential metric is the PPN-order weak-field representation only; **(ii)** the
> $m_Z/m_W$ headline moves from the UV value $2/\sqrt3$ (1.77%) to the on-shell endpoint
> $3/\sqrt7$ (−0.064%, F49/F138), the number the tree actually computes; **(iii)** "three
> generations is a theorem" is corrected to match F75's own status line — the group theory
> is exact, the physical identification is a stated hypothesis; **(iv)** $\alpha_s$ and the
> deuteron residuals are re-checked against PDG 2025, and a **Scope** section is added
> saying what is *not* claimed.

## One-page summary

A deterministic **quantum cellular automaton (QCA)** on a body-centred-cubic (BCC) lattice is proposed as the physical vacuum. The free dynamics are *forced* (not chosen) by the Bisio–D'Ariano–Perinotti–Tosini uniqueness theorem: in 3D the minimal non-trivial one-particle QCA is the Weyl walk on the BCC lattice. From one reinterpretation — **the speed of light is the angular rotation rate of a real $(\mathbf E,\mathbf B)$ pair per unit wavenumber**, $c_\text{lat}=1/\sqrt3$ — the model recovers Maxwell's equations (as a linearised rotation), the Einstein mass shell (as a spherical-Pythagorean identity), and, with gauge structure added, the Standard-Model sectors and gravity. Every structural claim is verified numerically to machine precision (residuals $10^{-14}$–$10^{-16}$) or as exact rationals, in a public test suite. An eleven-paper series gives the full construction.

## Core claims (each a deviation from, or derivation of, the Standard Model)

1. **Light is a rotation rate, not a phase velocity** ($c_\text{lat}=d\Omega/d|\mathbf k|=1/\sqrt3$). Maxwell's curl law is its $O(\Omega)$ linearisation; energy conservation is geometric (length-preserving rotation).
2. **The photon is a bound pair of two spin-½ Weyl quanta** (de Broglie's neutrino theory of light), not a fundamental spin-1 boson — massless, luminal, transverse, and **exactly non-birefringent**.
3. **Mass without a Higgs field**: a chiral-$SU(2)$ complex-mass step carries weak isospin as an exact gauge symmetry (Ward identity to $1.1\times10^{-17}$); the would-be Higgs direction is pure gauge. Hypercharge rides the same field.
4. **Exactly three fermion generations.** The group theory is a **theorem** about the cubic point group $O_h$: from $\sum d^2=\lvert O_h\rvert=48$ the maximal single-valued irrep dimension is 3, and the parity-odd triplet $T_{1u}$ is unique. The **physical identification** — that a generation *is* that triplet, realised by the scalar mass selecting the odd-parity shell — is a **stated hypothesis**, not a theorem (F75 §7; F75 is a Candidate finding). Granting the hypothesis, a fourth generation is forbidden. Recorded this way because F79's structural $G$ inherits the same status.
5. **The Koide relation $Q=\tfrac23$** is an exact $45^\circ$ equipartition of the cubic amplitude $\sqrt m$ ($Q(\phi)=1/3\cos^2\phi$); electromagnetism selects the colour-free charged leptons to sit there.
6. **Confinement** is exact in 2D (area law, $\sigma=-\ln w(\beta)>0$ for all $\beta$); in 3+1D it is a colour-dielectric dual superconductor cross-checked against gauge Monte-Carlo, governed by $\mathbb Z_3$ centre-phase closure.
7. **The Weinberg angle is derived**, with its scale: $\sin^2\theta_W=\tfrac14$ is the **matching value at the compositeness scale** $\mu_\star=4\pi v=3.09$ TeV, forced by hypercharge having no lattice kinetic term (F41/F138). Running Higgs-free to $M_Z$ gives $0.23173$ (**+0.22%** vs MS-bar $0.23122$), and the on-shell endpoint is $\sin^2\theta_W^\text{os}=\tfrac29\Leftrightarrow m_Z/m_W=3/\sqrt7$ (F49). Zero new parameters; the model's two existing rulers only.
8. **Gravity is sourced by the full stress-energy tensor** — the canonical law is the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ (F178). The impedance-matched lattice dielectric $K=e^{2GM/rc^2}$ (reciprocal lock $AB\equiv1$) is its **vacuum/weak-field representation**: GR-identical PPN ($\beta=\gamma=1$), plus the rotation-rate origin story. **Newton's constant is structural**, $G=a^2c^3/(8\pi\sqrt3\,\hbar)$, fixing $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$.
9. **Gravitational waves travel at exactly the photon speed**, $c_\text{grav}=c_\text{lat}=1/\sqrt3=c_\gamma$, inherited through the F79 zero-tree-stiffness channel rather than imposed (F180). This is a genuine zero, not a small number.
10. **Charge quantisation is derived, not assumed** (F165, re-attributed by F279). Given the lattice-fixed representation content, the generation hypercharges are the **unique** solution — up to a single overall normalisation — of two anomaly rows, the three F27/F41 mass-step rows, and the **F47 Higgs-free Majorana step**. That last row is what closes the system: $\nu_R^{\mathsf T}C\nu_R$ carries hypercharge $2y_\nu$, so gauge invariance forces $y_\nu=0$ exactly, and a Majorana mass is available only to a field of exactly zero hypercharge. The solution is $y_Q:y_u:y_d:y_L:y_e:y_\nu=1:4:-2:-3:-6:0$ with $y_\phi=3y_Q$; normalising $y_Q=\tfrac16$ gives the SM assignment and the measured electric charges $(\tfrac23,-\tfrac13,0,-1)$, exactly over ℚ. Both the gravitational and the cubic $U(1)^3$ anomalies are then identically zero on that line — consistency checks, not constraints. **Two inputs remain and are named:** the overall charge unit (the $\alpha$/$\sin^2\theta_W$ question, F49), and $N_c=3$ — commensurability holds for any $N_c$ (ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c$), so colour supplies the *value* of the fraction, not the *fact* of quantisation. Unlike the Standard-Model theorems this parallels (Minahan–Ramond–Warner; Geng–Marshak), the closing constraint here is Higgs-free structure the model already needed for the see-saw.

11. **The charged-lepton shape is fixed by a representation weight, with zero shape parameters.** The condensate angle **is** the second-shell $E_g$ weight, $\delta^*=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ rad (exact $O_h$, F175) — *weight-as-phase*. $\delta^*$ is **primary** and the sextic clock coupling $\lambda_6=0.243$ (equivalently $W=6\lambda_6=1.46$) is an **output** via the F234 arrow $\lambda_6=\lvert B\rvert/(2e^6\cos\tfrac23)$, not a fit. From $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ the whole charged-lepton shape follows to $\le0.007\%$. It is adopted because **every alternative is closed, not because it fits best**: the angle is a genuine radian with $R=1$ forced by Schur-isotropy of the $E_g$ irrep metric (F255, derived not posited); a scale-free topological origin is excluded, the only available holonomy being $2\pi/3$ (F253); and the dynamical Landau route provably cannot give exact $3\delta^*=Q$, since the sea $B$ and the induced $C$ have independent $O(1)$ origins and the identity holds only to $1.7\times10^{-5}$ (F256). Together with claim 5 this fixes the *shape*; the overall *scale* remains an input (see Scope). Supersedes the F179/CN3 reading, under which the spectrum was a one-angle **fit**.

> **Withdrawn in revision 2.** The former claim 9, "black holes are horizon-free dielectric
> condensates", is **retracted**. F178 demotes the exponential metric to the PPN-order
> weak-field representation; the **exact vacuum solution is Schwarzschild**, with a horizon.
> The horizon-free throat, the $+4.63\%$ shadow, the absent Hawking spectrum, the late-time
> ringdown echoes and the $4\pi$ second-order deflection coefficient were all consequences of
> treating the exponential form as fundamental, and none of them is predicted by the model as
> it now stands. They are listed here, rather than deleted silently, because they were
> published as live falsifiers between 2026-06-08 and 2026-08-02.

## Headline verified numbers

All reference values are **PDG 2025 / CODATA 2022** as of 2026-08-02.

| Quantity | Model | Reference | Residual | Free parameters |
|---|---|---|---|---|
| $c_\text{lat}$ | $1/\sqrt3=0.5773503$ | — (definition of the lattice unit) | exact | 0 |
| BCC lattice constant $a$ | $2/\sqrt3=1.1547005$ | — (closed form, F278) | exact | 0 |
| $\sin^2\bar\theta_W(M_Z)$ | $0.23173$ | $0.23122$ | $+0.22\%$ | 0 |
| $m_Z/m_W$ (on-shell, $\sin^2\theta^\text{os}_W=\tfrac29$) | $3/\sqrt7=1.133893$ | $91.1880/80.3692=1.134614$ | $\mathbf{-0.064\%}$ | 0 |
| Koide $Q$ | $0.6666605$ | $\tfrac23$ | $0.91\sigma$; predicts $m_\tau=1776.97$ MeV ($6\times10^{-5}$) | 0 |
| Electric charges $(Q_u,Q_d,Q_\nu,Q_e)$ | $(\tfrac23,-\tfrac13,0,-1)$ | same | exact over ℚ (literal 0) | 1 (charge unit) + $N_c{=}3$ |
| $a/\ell_P$; $G$ | $6.5978$; $6.6743\times10^{-11}$ | CODATA | $3\times10^{-8}$ | 0 |
| $\alpha_s(M_Z)$ | $0.11955$ (1-loop) | $0.1175\pm0.0010$ | $+1.7\%$ ($2.1\sigma$) | 1 scheme-matching input |
| Deuteron $E_b$ | $2.224$ MeV | $2.22457$ MeV | $0.026\%$ | 1 ($b=0.55$ fm) |

**Two residuals moved since revision 1, and in both cases the *measurement* moved, not the
model.** $\alpha_s(M_Z)$ was recorded at $+1.3\%$ against a PDG average of $0.1180$; that
average is now $0.1175\pm0.0010$, so the same unchanged model number is $+1.7\%$, i.e.
$\approx2.1\sigma$ of experiment. This is the register's largest open tension and is stated
as such. The deuteron moved the other way, $0.34\%\to0.026\%$ — but at a chosen $b=0.55$ fm,
so it is a one-parameter result and is no longer described as zero-parameter.

**One prediction survived an out-of-sample revision.** $m_Z/m_W=3/\sqrt7$ was fixed before
PDG 2025 excluded the CDF-II $m_W$ measurement for low compatibility. Against the resulting
$m_W=80.3692\pm0.0133$ the model gives $-0.064\%$ (implied $m_W=80.4203$). Had it been tuned
to CDF it would now look worse; it was not, and it survives the exclusion cleanly.

## Falsifiable predictions (with thresholds)

- **Quantum-gravity dispersion.** A quadratic ($n=2$) vacuum dispersion with energy scale $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.36\times10^{19}$ GeV. **Any measured $n=2$ time-of-flight bound above $1.36\times10^{19}$ GeV kills the adopted lattice cell.**
- **Vacuum birefringence.** The physical (paired) photon is **exactly non-birefringent** — not within a tolerance, but structurally: the pair carries one single-valued rotation rate $\Omega_\text{pair}$, so there is no second branch to split from. A confirmed first-order vacuum birefringence in GRB/AGN polarimetry would contradict it (and would, conversely, revive the excluded chiral construction).
- **Gravitational-wave speed.** $c_\text{grav}=c_\gamma$ **exactly**, with no free coefficient (F180; GW170817 residual $\le3\times10^{-83}$). Any confirmed non-zero $c_\text{grav}/c_\gamma-1$ falsifies the inheritance mechanism.
- **Weinberg angle.** The chain is committed to $\sin^2\theta_W=\tfrac14$ at $\mu_\star=4\pi v$ and $\sin^2\theta_W^\text{os}=\tfrac29$ on shell. A precision $m_W$ that moved $m_Z/m_W$ off $3/\sqrt7$ by more than the running uncertainty would falsify it — which makes the PDG 2025 re-analysis (CDF-II excluded) a passed test, not a retrofit.
- **Charged-lepton shape.** A charged-lepton mass measurement inconsistent with the $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ shape at better than $0.007\%$. Because $\delta^*$ is an exact rational fixed by $O_h$ representation theory, **there is no parameter to re-fit** — the two no-gos (F253, F256) closed the alternatives deliberately, and that is what makes this falsifiable rather than adjustable.
- **Mercury precession.** PPN $\beta=\gamma=1$ (42.98″/cy). The naive *linear* dielectric ($\beta=\tfrac12$, 50.1″/cy) is excluded. Under F178 this is now a consistency requirement rather than a distinctive prediction: in vacuum the model **is** GR, so a confirmed PPN deviation falsifies it exactly as it would falsify GR.

**Withdrawn in revision 2** (all four were consequences of the pre-F178 exponential-metric-as-fundamental reading, and the model no longer predicts any of them): photon-ring imaging at $+4.63\%$; gravitational-wave ringdown echoes; absence of a thermal Hawking spectrum; the $4\pi$ second-order light-bending coefficient. **An observation matching Schwarzschild in any of these four would previously have been recorded as falsifying the model. It does not.**

## Scope — what is *not* claimed

Stated explicitly so that absence is not read as a prediction. Each is open and acknowledged,
not quietly omitted.

- **$m_W$ and $m_Z$ in absolute terms.** The model predicts their **ratio**. The electroweak scale $v$ is an anchor, not an output.
- **The CKM matrix and measured CP violation.** The construction is first-generation; $J=0$ is the arithmetic consequence of one generation ($N_\text{phase}=(n-1)(n-2)/2$), not a prediction that the CKM phase vanishes (F53). Three-generation mixing is out of scope.
- **Neutrino mass scale.** F47 supplies a Higgs-free see-saw *mechanism*; nothing in the model fixes $M_R$, so no absolute neutrino mass is predicted.
- **Muon $g-2$ beyond QED.** The QED piece is computed through two loops ($A_2(\mu)=0.765857$ vs the known $0.765857410$). Hadronic vacuum polarisation, hadronic light-by-light and electroweak contributions are **not** computed and not claimed.
- ~~**Charge quantisation.**~~ **Moved to core claim 10 in revision 3.** Revision 2 listed this as an input; that was wrong. It is derived (F165, re-derived and re-attributed by F279). What remains an input is the **one charge unit** — the overall normalisation, which is the $\alpha$ / $\sin^2\theta_W$ question (F49) — and, for the specific *thirds* rather than commensurability as such, $N_c=3$. Both are named in claim 10.
- **"No doublers" has a domain.** The BCC Weyl walk has exactly one zero, at $k=0$, and no $\omega=\pi$ point **on the cubic FFT grid** ($L$ up to 128, both branches). On the true BCC zone the $\omega=\pi$ mode sits exactly at the corner H, $\lvert\mathbf k\rvert=2\pi/a=\pi\sqrt3$ (F278). Every observable in the tree is computed on the grid, so no result depends on the distinction — but the unqualified form of the claim overstates it, and the discriminating test is not yet built.
- **The cosmological constant** is not derived; F193/F196 reduce the classic 121-order problem to the $\Omega_\Lambda\approx0.69$ coincidence, which is not the same as explaining it.

## Where the claims live

Since 2026-08-04 this document is a **summary**, not the register. The register is
`docs/claims/` — one card per claim, `CL{NNN}-{slug}.md`, each carrying a present-tense
status (`live` · `narrowed` · `contingent` · `open` · `withdrawn` · `not_claimed`), a
falsifier field, the findings it rests on, and its own revision history. `claims-index.md`
lists every card.

The distinction the cards exist to make: **a finding is a research record and a claim is a
position.** A finding is written once and superseded rather than rewritten — it is correct
for it to keep saying what a session concluded. The claim resting on it is what has to move,
and until now there was nowhere to move it. Sixteen findings in this project are named in a
`superseded:` list while their own headers still read `Confirmed — N/N PASS`; that is not a
defect in the findings, it is the gap the cards fill.

Three consequences worth stating here, because they are what a reader of *this* document
should know:

- **The revision-2 withdrawals are cards, not a blockquote.** The horizon-free black hole
  and its four dependent falsifiers are `CL023`–`CL027`, each `status: withdrawn`, each
  card's history section *being* the retraction record. A gate test asserts they are never
  deleted, because a withdrawn claim that is deleted is a claim that gets re-made.
- **Overstatement is now machine-checkable.** `tools/check_claims.py` fails a card marked
  `live` when *every* finding it rests on is named in a `superseded:` list. On its first
  run it caught seven. It deliberately does **not** fire on partial supersessions: of
  fourteen files one audit called superseded, exactly one was.
- **Not every card is authored.** 28 are; 223 are `review_state: unreviewed-seed` —
  extracted from a finding, classification *not* confirmed by a reviewer, and not citable
  as independent support. The count is a ratcheted debt, not a claim of 223 results.

## Reproducibility

Every claim above runs in a public test suite to the stated residual. The **structural** sector — lattice cell, gauge couplings, metric — carries **no free fit parameters**; the two rows that do carry one ($\alpha_s$, the deuteron) are marked in the table rather than folded into a headline. Source, tests, and per-finding write-ups accompany the papers.

*Barrier: `make gate`. A green bare `pytest` is not sufficient — it cannot collect the three
scenario records that run the engine on a lattice.*

*Full series (11 papers) and this summary: see the accompanying `papers/` directory. Contact: benludwig6382@gmail.com.*
