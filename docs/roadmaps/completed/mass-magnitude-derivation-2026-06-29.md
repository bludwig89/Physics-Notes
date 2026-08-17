# Roadmap — Deriving the mass *magnitude* (the open half of audit G1 / F167)

**Date:** 2026-06-29 - 19:10
**Purpose:** F167 closed the *structural* half of audit G1 (rest mass = the unique, unitarity-and-symmetry-forced zero-wavenumber rotation rate of the rule). This roadmap deep-researches the *magnitude* half — the value of the dimensionless rule parameter $m$, equivalently the overall fermion-mass scale $N\equiv m_\text{lat}(\tau)=5.54\times10^{-19}$ — and asks **how it could possibly be derived from first principles.**
**Headline:** the magnitude is *not* as open as F167-T6 / F119 framed it. **F144 (2026-06-12, post-dating F119) already derives the overall scale to a factor ~1.9 with no tuning**, via dimensional transmutation of the strong coupling. The remaining work is two well-defined pieces — a conventional lattice-scheme constant (in progress, F162/F163) and one genuine physics gap (the lepton↔colour scale link). This document ranks the routes and gives concrete next steps, grounded in the external literature.
**Cross-references:** [[F167-restmass-from-rule-zero-k-rotation]] (the structural half; its T6 scope note is *updated* here), [[F119-kg-scale-three-routes]] (the original no-go), [[F144-route-a-alpha-s-dimensional-transmutation]] (the answer), [[F151-scheme-constant-determined]]/[[F155-qstar-self-energy-and-freeze-bracket]]/[[F162-bgfield-self-energy-b0-gate]]/[[F163-wilson-lattice-selfenergy-vertices-28p81-gate]] (the residual scheme constant), [[F92-per-constituent-phase-consistency]]/[[F93-second-shell-Eg]]/[[F76-generation-mass-hierarchy-crystal-field]] (the shape sector), [[F150-eg-sextic-brake]]/[[F154-residuals-A-B]] (the last shape coefficient λ₆), [[F120-electron-calibrated-spectrum]]/[[F121-tau-anchored-canonical-spectrum]] (the calibration fallback).

---

## 1. What "the magnitude" actually decomposes into

The audit G1 "magnitude" is not one number. It splits cleanly (F119 N1: shape × scale factorisation, verified to $4\times10^{-7}$):

1. **Shape** — the dimensionless mass *ratios* ($m_e:m_\mu:m_\tau$, Koide $Q$). **Derived to $10^{-12}$** (F92 fixed point $Q=2/3$; F93/F76 the $E_g$ orthorhombic crystal-field), modulo **one residual coefficient** $\lambda_6\approx0.243$ / $\cos3\delta=0.7859$ (the $E_g$ sextic brake; F150 shows this is the *same* number as the QCD IR coupling residual).
2. **Overall scale** $N=5.54\times10^{-19}$ — the absolute placement of the whole spectrum. This is "the hierarchy," and is the real subject of G1's magnitude question.
3. **Units (kg/eV)** — *already discharged* (F119): once the cell $a$ is gravity-locked (F107), $\hbar$ carries the kilogram via $m_\text{phys}c^2=\hbar\arcsin(m_\text{lat})/\tau$; there is no free kg knob.

So "derive the magnitude" = **derive $N$** (scale) + **derive $\lambda_6$** (the last shape coefficient). Everything else is done.

## 2. The key update: $N$ is already derived to a factor ~1.9 (F144)

F119 (2026-06-09) concluded $N$ "can't be made from $O(1)$ couplings — no running channel" and named what would close it: *a logarithmically-running (marginal) coupling for dimensional transmutation*, $N=\exp(-K/g)$ with $K=-g\ln N\approx42$.

**F144 (2026-06-12) built exactly that channel.** The rule's own bare strong coupling is *derived* (not assumed) from rule circularity: $\chi=1\wedge\chi=1/(4g_s^2)\Rightarrow g_s=\tfrac12$, $\alpha_0=\alpha_s(\mu_0)=1/(16\pi)$ at the lattice/Planck scale $\mu_0=\hbar c/a$. Running this down by **asymptotic freedom** generates the hierarchy with no tuning:

$$N\sim e^{-1/(2b_0\alpha_0)},\qquad N_\text{pred}=\Lambda^{(3)}/\mu_0=2.9\times10^{-19}\ \ \text{vs}\ \ N_{F119}=5.5\times10^{-19}\quad(\textbf{factor }1.9),$$

and $\Lambda_{\overline{\rm MS}}^{(3)}=529$ MeV vs FLAG $343(12)$ MeV (factor 1.54). **The 19-decade hierarchy comes out of pure structure** because the rule fixes $\alpha_0=1/(16\pi)$. This is the single most important fact for G1's magnitude half, and it post-dates (and corrects) the "no-go" framing carried into F167-T6.

> **Honesty note (F167 update):** F167-T6 said "the value of $m$ is NOT fixed by the bare rule (F119 no-go)." That is now too strong. The *bare* rule does not fix it, but the *running* of the rule's derived strong coupling does — to a factor ~1.9. F167-T6 should be read as "the bare rule leaves $m$ free; the dynamics (F144 transmutation) then fixes the scale up to a scheme constant."

## 3. What remains genuinely open (two pieces)

**(R-scheme) The residual factor ~1.9 / 1.54 — a lattice→continuum scheme constant.** This is *not new physics*: it is the same $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}$ conversion (the QCD "Wilson 28.81" constant) that the calibration block is already computing. Status: $b_0$ recovery gate **passed exactly** (F162); the lattice 3-gluon+ghost vertices **transcribed and validated** (F163); the finite constant $d_1$/$q_\ast$ **bracketed** $q_\ast a\in[1/\sqrt3,\sim0.97]$ but **not pinned to the digit** (F155, F162 G3, F163 W5). Closing it is a conventional (hard) lattice-perturbation-theory computation, not a conceptual gap.

**(R-link) The lepton↔colour scale link — the one real physics gap.** F144 identifies the *fermion* scale $N$ with the *colour* transmutation scale $\Lambda/\mu_0$. But **leptons carry no colour**, and the lepton mass shape comes from the $E_g$ condensate (F93), not the gluon sector. So *why the lepton/$E_g$-condensate scale tracks $\Lambda_\text{QCD}$ to a factor ~2* is currently an **identification, not a derivation**. This is the genuine open conceptual item and the natural focus of new work.

## 4. External grounding — how absolute mass scales are derived in real physics

The literature is unambiguous on one point: **the only place the Standard Model derives a mass scale from first principles is QCD**, by exactly the mechanism F144 uses.

- **QCD dimensional transmutation (the precedent that works).** >99% of the proton mass is the QCD scale $\Lambda_\text{QCD}$, generated from the running of $\alpha_s$ and the trace anomaly — a massive proton from massless quarks/gluons. Lattice QCD computes it from first principles. The absolute $\Lambda_\text{QCD}/M_\text{Pl}$ still requires *one* input ($\alpha_s$ at some scale) — which in the CA model is *removed* because the rule fixes $\alpha_0=1/(16\pi)$. ([Argonne EIC/lattice proton mass](https://www.anl.gov/event/eic-physics-from-lattice-qcd-the-proton-mass-and-spin-decomposition); [Constantinou, proton mass from lattice](https://indico.phy.anl.gov/event/2/contributions/19/attachments/24/36/Proton_Mass_2021_Constantinou.pdf); [Dürr, proton mass from scratch](http://durr.itp.unibe.ch/talk_09_psi.pdf))
- **Technicolor / extended technicolor (the precedent for R-link).** EW symmetry is broken by a dynamically generated condensate "as in QCD" via dimensional transmutation — but **feeding that scale to ordinary fermions requires an extra (extended-technicolor) interaction**, and viable spectra need a **large condensate anomalous dimension** (walking/crawling). This is precisely the CA model's R-link problem (colour condensate → lepton mass) and tells us the link will hinge on the $E_g$ condensate's anomalous dimension. ([Large fermion masses from ETC, Nucl. Phys. B](https://www.sciencedirect.com/science/article/abs/pii/037026939090530J); [EWSB by dynamically generated quark/lepton masses, arXiv:1309.4688](https://arxiv.org/pdf/1309.4688); [Crawling technicolor, PRD 100, 095007](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.100.095007))
- **Asymptotic safety / UV boundary conditions (the precedent for the rule fixing $\alpha_0$).** Shaposhnikov–Wetterich predicted $m_H\approx126$ GeV from $\lambda(M_\text{Pl})=\beta_\lambda(M_\text{Pl})=0$; Eichhorn–Held predict a top pole mass $\approx171$ GeV from UV fixed-point boundary conditions on the Yukawas. This is the same epistemology as the CA rule fixing $g_s=1/2$ at $\mu_0$ and *running down* — a UV condition that predicts an IR mass. It legitimises Route A/B below. ([Eichhorn–Held, Top mass from asymptotic safety, arXiv:1707.01107](https://arxiv.org/pdf/1707.01107); [Why the quark mass is not the Planck mass, PRD](https://journals.aps.org/prd/abstract/10.1103/4jzf-byxc))
- **Koide / flavour-symmetry relations (the precedent for shape-only).** The Koide formula constrains *ratios up to an overall scale*; it needs one measured mass to set the scale. Confirms the CA shape/scale split and that the scale must come from dynamics, not a ratio relation. ([Koide formula overview, J. Baez](https://johncarlosbaez.wordpress.com/2021/04/04/the-koide-formula/); [Family gauge symmetry and Koide, arXiv:0812.2090](https://arxiv.org/pdf/0812.2090))
- **Dynamical mass / magnetic catalysis (a mechanism note).** In 3+1D a weak attractive channel can still generate a dynamical fermion mass via dimensional reduction $D\to D-2$ (e.g. magnetic catalysis $m_\text{dyn}\sim\sqrt{eB}\,e^{-\sqrt{\pi/\alpha}}$). Relevant because F119's no-go was specifically the *3D mean-field square-root* transition; a reduced-dimension or marginal channel evades it — which is exactly what the strong sector provides. ([Gusynin–Miransky–Shovkovy, hep-ph/9412257](https://arxiv.org/abs/hep-ph/9412257))

## 5. Candidate routes to *fully* derive the magnitude, ranked

### Route A — finish the strong-sector transmutation (primary; partially done)
The scale is already landed to factor ~1.9 (F144). Completing it has two sub-tasks:

- **A1 (R-scheme, in progress, conventional).** Pin the lattice→$\overline{\rm MS}$ scheme constant to kill the factor ~1.9/1.54. The machinery is built and gated (F162 $b_0$ exact, F163 vertices validated); what remains is the finite $d_1$/$q_\ast$ digit (F155 bracket). **Effort: high but bounded; no new physics.** Success criterion: $N_\text{pred}/N\to1$ within the F121 anchor precision.
- **A2 (R-link, the real physics). — EXECUTED at the mechanism level (F170, 2026-06-29).** The link is now *derived*: the $E_g$ condensate has **no independent coupling** (induced by the strong sector, F145/F150) and a gap kernel **near-degenerate** with the colour $\chi$SB channel ($G_c^{E_g}/G_c^{\text{s-wave}}\to1.08$), so nothing in the dynamics can make a hierarchy — $v_{E_g}=O(1)\times\Lambda_\text{QCD}$ is forced. The "extended interaction" is the induced coupling (integrating out the dielectric gluon), exactly the technicolor/ETC picture. **Residual:** the exact $O(1)$ ($m_\tau/\Lambda\approx3.4$–$5.7$; kernel $\approx1.1$ × saturation/angle $\approx3$) is the *same* saturated-condensate number as $\lambda_6$ (F150) — so A2 and C close together. Success criterion downgraded from "derive the ratio" to **"pin the shared saturated-condensate digit"** (= Route C).

**This is the route with a real chance of a zero-parameter magnitude**, and it is already half-built.

### Route B — UV-fixed-point reading (reframing of A, strengthens it)
Treat $\alpha_0=1/(16\pi)$ at $\mu_0$ as the rule's UV boundary condition and the IR mass as its prediction — the asymptotic-safety epistemology (Eichhorn–Held, Shaposhnikov–Wetterich). Concretely: run the *mass parameter* $m$ itself under the model's block-spin RG (F129/F130) and look for an IR-attractive (quasi-fixed-point) value. **Obstruction:** F115 found EW/lepton couplings essentially *non-running at the lattice scale*, so there may be no lepton-sector flow to attract — the flow that matters is the *strong* coupling's (Route A). Use B as the conceptual justification for A, not a separate mechanism. **Effort: medium (RG already exists); likely confirms A.**

### Route C — close the last shape coefficient $\lambda_6$ (independent, needed for "fully")
Derive the $E_g$ sextic brake $\lambda_6$ from the saturated-condensate solve (F150 structure closed: induced three-body self-coupling; F154 B-route solved the IR coupling $\alpha_\text{eff}^*\approx0.39$). This is the *same IR residual* as A2's anomalous-dimension number (F150), so **A2 and C likely close together.** **Effort: high; shares inputs with A2.** Success criterion: $\cos3\delta^*=\cos Q$ ($3\delta^*=2/3$ rad) derived, not fitted.

### Route D — accept one calibration mass (the honest fallback, already working)
Anchor $\tau$ (F121, exactly $\delta$-stable) → every other lepton mass is a parameter-free kg prediction to $\le0.1\%$; the kg is automatic. This is *exactly* what the Standard Model does (Yukawas are inputs) and what Koide does (one mass sets the scale). If A1's scheme constant proves intractable, D is the principled stopping point, and the model is then **no worse than the SM on the scale, and far ahead on the shape.** **Effort: zero (done).**

### Route E — environmental/landscape (only if A2 fails)
If no $O(1)$ link from $\Lambda_\text{QCD}$ to the lepton scale exists, the residual factor could be environmental. This is a *non-derivation* and should be the last resort; flagged for completeness.

## 6. Recommended program

1. **Promote the F144 result into the F167/G1 narrative** and amend F167-T6: the magnitude is derived to factor ~1.9, not open. *(Documentation; do now.)*
2. **Route A1** — push the scheme-constant computation (F162/F163/F155) to pin $q_\ast$ to the digit. This alone takes $N$ from factor-1.9 to precision, for the colour-bound sector. *(Highest leverage, bounded.)*
3. **Route A2 + C together** — the $E_g$ condensate anomalous dimension / IR coupling is the single number behind both the lepton↔colour scale link *and* $\lambda_6$. Target it once: derive $N_\text{lepton}/(\Lambda/\mu_0)=O(1)$ and $\cos3\delta^*=\cos Q$ from the saturated-condensate solve. *(The one genuine physics gap; highest value.)*
4. **Route B** as the RG cross-check / conceptual frame (asymptotic-safety reading).
5. **Route D** documented as the fallback so no claim ever overstates: worst case, one anchor, SM-equivalent.

**Bottom line.** "How could the magnitude possibly be derived?" — *the same way the proton mass is*: dimensional transmutation of the strong coupling, with the rule supplying the one input ($\alpha_0=1/16\pi$) that QCD itself cannot. The model has already executed this to a factor ~1.9 (F144). Full closure needs a conventional lattice-scheme constant (in progress) and one piece of real physics — the colourless-lepton ↔ colour-scale link, which the technicolor literature says will live in the $E_g$ condensate's anomalous dimension, the same number as the open shape coefficient $\lambda_6$.

## 7. Sources
- Internal: F119, F144, F151, F155, F162, F163, F92, F93, F76, F150, F154, F120, F121, F167.
- External (full URLs in §4): Argonne/Constantinou/Dürr (lattice proton mass & transmutation); Nucl. Phys. B / arXiv:1309.4688 / PRD 100,095007 (technicolor & ETC mass feeding); arXiv:1707.01107 & PRD "Why the quark mass is not the Planck mass" (asymptotic-safety mass predictions); J. Baez & arXiv:0812.2090 (Koide ratios-only); arXiv:hep-ph/9412257 (dynamical mass / magnetic catalysis).
