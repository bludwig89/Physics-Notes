# The strong-sector scale-setting problem (the "IR coupling") — what's been tried, what's left

> **Update 2026-06-13 - 11:30 (F155).** Residual **A sharpened to a convergent bracket** (not yet pinned). The one-loop self-energy machinery is built (`ca_gluon_self_energy.py`): (i) the tadpole sector is proven **exactly empty** — the F26 link is machine-exactly $SO(2)$, $u_0\equiv1$, so the Wilson $Z_0$ (bulk of $28.81$) is structurally absent (F151-S2 as a machine check); (ii) the lattice−continuum **subtraction** machinery F154 named is built and **convergent** ($d_1$ stable, $b_0$ universal); (iii) the continuum-subtracted Lepage–Mackenzie loop momentum **converges** to the band top $q_\ast^\text{abelian}\sim0.97/a$ (the F129 near-perfect-action signature), so with F151's lower edge $q_\ast a\in[0.577,0.979]$ — implied $0.733$ **inside**, $\Lambda$-ratio $O(1)$ (1.33–2.25), **not** Wilson. The remaining pull-down to $0.733$ is the **gluonic 3-gluon+ghost finite part** (the bespoke $\Omega_\text{even}$ vertex algebra) — the one production computation still open — or, gauge-fixing-free, the **high-resolution static potential** (`run_su3_3d_string_tension.py` now has the Cornell $\alpha_V$ fit + JSON; production is one native run). Within **B**, the freeze value $\approx0.39$ is now **bracketed anchor-free**: the L-stable nonlinear χSB onset ($\alpha_\text{onset}=0.31$, set by $m_D$/decoupling) plus the steep gap rise pin it to $[0.31,0.38]\subset[0.3,0.5]$ with no $M(0)$ anchor; the exact value still needs A's scale. See `findings/F155-qstar-self-energy-and-freeze-bracket.md`.

> **Update 2026-06-12 - 19:30 (F154).** Residual **B is solved**: the full nonlinear self-consistent gap, with the physical constituent mass $M(0)=311$ MeV imposed, converges to the IR coupling $\alpha_\text{eff}^\ast=0.376/0.411\approx0.39$ (L-stable, reproducing F151-S5). Residual **A's cheap route is ruled out**: the gluon-propagator log-moment gives UV scales ($e/a$), not the matching scale — $q_\ast$ is the UV-finite lattice−continuum subtraction, so A still needs the full one-loop background-field integral. Net: the last strong-sector freedom is **one absolute scale** (A's integral); B supplies the gap physics around it. See `findings/F154-residuals-A-B-built-and-solved.md`. The §5 residuals below are updated accordingly.

`2026-06-12 - 18:40` — status synthesis. Companion to `docs/theory/qcd-calibration-derivation-routes.md` (the routes review) and the open-input audit `docs/audits/project-audit-inputs-dynamism-2026-06-06.md` (cluster 3: the QCD-calibration block). This document pulls together every finding that has attacked the single nonperturbative number the strong sector keeps bottoming out on, states what each established, and isolates exactly what remains.

---

## 1. The problem, in one paragraph

The model fixes the bare colour coupling **exactly** at the lattice scale — $g_s^2\chi=\tfrac14\Rightarrow g_s=\tfrac12$, $\alpha_s(\mu_0)=1/16\pi$ at $\mu_0=\hbar c/a=1.85\times10^{18}$ GeV (F115/F144, zero parameters). Everything physical in the strong sector — $\alpha_s(M_Z)$, the hadron scale $\Lambda$, the string tension $\sqrt\sigma$, the chiral condensate ($f_\pi$, $m_c$), the NJL contact $G$, even the charged-lepton mass texture's brake $\lambda_6$ — is then supposed to follow by running that one coupling down and condensing the vacuum. The recurring obstruction is a **single nonperturbative normalization** that connects the bare lattice world to the physical hadron world. Roughly ten findings have attacked it from different directions. None has produced a robust, fully-derived value; each has either been a **no-go** (ruling out a candidate source) or a **sharpening** (reducing the unknown to something smaller and better-posed). As of F151/F152 the unknown has been **split into two distinct, individually well-posed pieces**, one of which is now *determined up to a bounded scale choice*.

## 2. The current best understanding: it is *two* numbers, not one

Until 2026-06-12 the working assumption (F124/F144/F145/F150) was that one shared constant governed everything. F151 disproved the "one number" framing and resolved the structure:

| Face | Physical meaning | Status | Owns |
|---|---|---|---|
| **UV** | rule→$\overline{\rm MS}$ scheme/scale constant ($\Lambda_\text{rule}\!\to\!\Lambda_{\overline{\rm MS}}$) | **determined to a $\sqrt3$ band** (F151) | $\alpha_s(M_Z)$, $\Lambda^{(3)}$, $\sqrt\sigma$ scale-setting (F124) |
| **IR** | gap-saturated effective coupling $\alpha_\text{eff}^\ast\approx0.39$ | **value imported, scale+branch fixed** (F152), magnitude not first-principles | χSB point $G/G_c$ (F145/F77), the $E_g$ brake $\lambda_6$ (F150) |

They are connected by the running but **not identical** (F151-S5). This is the single most important structural advance: the problem stopped being one intractable knot and became two separate, each-well-posed computations.

## 3. What's been tried — the ledger

Chronological; "type" ∈ {lock = exact derivation, sharpening, no-go, partial}. Every entry is a verified finding (test suite PASS).

| # | Finding | Date | Angle of attack | Type | Result | Residual it left |
|---|---|---|---|---|---|---|
| 1 | **F100/F101** | 06-05 | string tension from the compact-rotor transfer operator | lock | $\sigma_1=\tfrac14\langle1/\Omega\rangle_\text{BZ}=0.2015$ (2D, exact); Gaussian→confinement crossover mapped | this is the *bare/strong* $\sigma$; ties to the physical $\sqrt\sigma$ only through the crossover |
| 2 | **F77** | (pre) | self-consistent NJL gap + RPA | partial | one coupling fixes $m_c$ and $E_b$; confirms the F74 ceiling | $G/G_c=1.277$ **fitted** |
| 3 | **F88 / F117** | — | colour condensate / gap-coupled gluon propagator | input | dual-Meissner mass **measured**: $m_D=0.532$ (F88, U(1) surrogate $\beta{=}1.8$) / $0.727$ (F117); $v=m_D/e=0.713$ | $m_D$ is a measured lattice number, not yet tied to $\Lambda$ in one scheme |
| 4 | **F115** | 06-08 | are $e,g,g_s$ independent? | lock + no-go | EW reduces to **one** magnitude; $g_s^2\chi=\tfrac14$ **locked**; +12% Weinberg gap is *not* desert running (CM2); the "$e^6$" of the $E_g$ brake is **not** the gauge coupling (CM4 notation no-go) | the one EW magnitude ($\alpha_\text{em}$) and the strong scale remain |
| 5 | **F116** | 06-08 | NJL re-derived on the lattice | sharpening | cutoff $\Lambda$ = **BZ edge** (not a fit); $G$ = induced coupling from the colour dielectric (NJ4 mechanism, $G\sim\tfrac49 g_s^2/M_g^2$ order-of-mag) | the precise dimensionless $G\Lambda^2$, $m_0/\Lambda$ still fit |
| 6 | **F119** | 06-09 | can the mass hierarchy $N$ come from $O(1)$ inputs? | no-go | the 3D gap mechanism **cannot** generate $N=5.5\times10^{-19}$ from $O(1)$ couplings — no running channel in the gap alone | $N$ must come from *running* (→ F144) |
| 7 | **F123** | 06-09 | SI absolute scale of the matter sector | partial | one $f_\pi$ anchor puts $3m_c=m_p$ within ~1% of 938 MeV | $f_\pi$ is a **hand anchor**; carries the whole MeV scale |
| 8 | **F124** | 06-09 | derive $\sqrt\sigma/f_\pi$ | partial + diagnostic | $=$ (exact chiral $\Lambda/f_\pi=7.04$) × (confinement $\sqrt\sigma/\Lambda=0.569$); model $4.00$ vs empirical $4.56$ (~12%); bare-rotor route collapses to $\sim1$ (factor-4 gap = scale-setting) | the $\sqrt\sigma/\Lambda$ scale-setting residual |
| 9 | **F129/F130** | 06-10/11 | block-spin RG of the rule | lock | rule's LIV/artifact operators are **irrelevant** ($\lambda_n=b^{-n}$) — near-**perfect** action; confinement $\hat\sigma$ is the one **relevant** direction ($\lambda_\sigma=b$) | (enabling result; explains why the scheme constant is $O(1)$, not Wilson's 29) |
| 10 | **F144** | 06-12 | Route A: dimensional transmutation from $g_s=\tfrac12$ | partial + diagnostic | $g_s=\tfrac12$ **derived** (circularity lemma); $\alpha_s(M_Z)$ **+8.4%** converged / +1.3% 1-loop; hierarchy $N$ ×1.9 of F119 (19 decades, no tuning) | A4: the scheme constant — implied $\Lambda$-ratio **1.78** (Wilson 28.81); "one open coefficient" |
| 11 | **F145** | 06-12 | Route C: induced NJL coupling | no-go + structural | exact Fierz $c=\tfrac29$ (F77 form forced); **bare coupling cannot break χS** ($R=0.075$–$0.10\ll1$); but the **running guarantees** χSB ($R=2.6$–$15\gg1$); fit $1.277$ bracketed | N5: the exact χSB point = the nonperturbative IR coupling |
| 12 | **F150** | 06-12 | the $E_g$ lepton brake $\lambda_6$ | sharpening | source closed (condensate self-coupling, F95⊕F147 two-route no-go); kind fixed (induced, F145); $\cos3\delta^\ast=\cos Q$ ($3\delta^\ast=\tfrac23$, $1.7\!\times\!10^{-5}$) | $\lambda_6$'s value = the IR-coupling normalization at saturation |
| 13 | **F151** | 06-12 | **the scheme constant, head-on** | **partial solution** | rule coupling **= V-scheme** (tree-exact); conversion = **known** $a_1=\tfrac{11}{3}$; $\Delta(1/\alpha)=0.640=\underbrace{0.292}_{a_1\text{ exact}}+\underbrace{0.348}_{q_\ast\text{ band}}$; band $[1/\sqrt3,1]/a$ **brackets** PDG $\alpha_s(M_Z)\in[0.114,0.123]$; $\Lambda^{(3)}=347$ MeV (FLAG 1.1%) | the matching scale $q_\ast$ inside a $\sqrt3$ window (UV face residual) |
| 14 | **F152** | 06-12 | the IR face (post-F151 split) | sharpening | $\alpha_\text{eff}^\ast\approx0.39$ is the **frozen, gap-saturated** coupling; scale = $m_D$; **decoupling/saturating branch** (continuum $\hat\alpha(0)/\pi=0.97$, $m_g\approx0.5$ GeV) | the IR face value from first principles (crossover solve) |

Supporting confinement infrastructure also exists (F70 exact 2D area law; F94 3+1D Monte-Carlo $\sigma$; F99 centre-Lagrange identity; F146 emergent SU(3) $\sigma$ to ~5%, $a_g=0.26$ fm), which supplies the physical-$\sigma$ leg but does not by itself set the scheme.

## 4. What is solid now (no longer open)

- **The bare lock (exact).** $g_s=\tfrac12$, $\alpha_s(\mu_0)=1/16\pi$ at $\mu_0=1/a$ — derived, zero parameters (F144 A1; F115 CM3; F110 C7).
- **The cutoff is the BZ edge** (F116) — $\Lambda$ is not an NJL fit parameter.
- **The Fierz channel structure is exact** — $c=\tfrac29$ in all four chiral channels; the F77 NJL form is *forced*, not chosen (F145 N1).
- **The scheme identification (UV face) is exact** — the rule coupling is the static-potential (V-) scheme coupling, so the one-loop conversion is the *known* $a_1=(93-10n_f)/9$ (F151 S1). The constant's tadpole-free smallness is explained structurally (F129 near-perfect action; F151 S2 Wilson-tadpole contrast).
- **The branch is correct** — the model is on QCD's saturating/decoupling side (finite $\alpha(0)$), because it generates a gluon mass gap by mechanism (F88/F117/F152); it is *not* on the spurious Landau-pole branch.
- **χSB is guaranteed** — not assumed: the running coupling is supercritical at the chiral scale (F145 N4), and the bare coupling is decisively subcritical (N3).
- **The two faces are distinct** and individually well-posed (F151-S5).

## 5. What still needs work — the two open residuals

Everything unresolved reduces to **two** nonperturbative computations. Close both and the entire strong-sector chain (α_s, Λ, √σ, f_π, m_c, G/G_c, λ_6, the hierarchy N) becomes parameter-free.

### Residual A — the UV face: the matching scale $q_\ast$ (one lattice-PT integral)
- **What it is.** The single scale $q_\ast$ at which $\alpha_V(q_\ast)=1/16\pi$, equivalently the finite part of the rule's one-loop gluon self-energy. F151 pinned it to the band $[1/\sqrt3,\,1]/a$ and the data imply $q_\ast=0.733/a$ (within 3.6% of the geometric mean $3^{-1/4}/a=0.760$ — suggestive, the F107 cell carries $3^{1/4}$, but not derived).
- **The computation.** The **one-loop background-field lattice perturbation theory** of the rule's gauge action (the F110 plaquette rotor / F26 rotation) on the BCC Brillouin zone. Its tadpole sector is empty by exact link unitarity (F151 S2), so it is a single, finite, vertex-driven BZ integral.
- **Falsification target (sharp).** It must yield $q_\ast=0.733/a$ (equivalently reproduce $\alpha_s(M_Z)=0.1180$ and the $\Lambda$-ratio $\approx1.8$). If it lands near Wilson's $\approx29$, the $g_s=\tfrac12$ lock is wrong.
- **Difficulty.** Hard but standard in kind (lattice PT). The propagator and vertices of the rotor action must be extracted first; then a 4D BZ quadrature. This is the highest-value single computation in the whole sector.
- **Sharpened to a convergent bracket (F155).** The tadpole sector is proven exactly empty ($u_0\equiv1$, Wilson $Z_0$ absent), the lattice−continuum subtraction machinery is built and convergent, and the subtracted Lepage–Mackenzie moment converges to the band top $q_\ast^\text{abelian}\sim0.97/a$, giving $q_\ast a\in[0.577,0.979]$ (implied $0.733$ inside; $\Lambda$-ratio $O(1)$, not Wilson). The single-value pin needs the **gluonic 3g+ghost finite part** (the $\Omega_\text{even}$ vertex algebra) or the high-res static potential (A-NP machinery now built). So A is *bracketed*, not yet *closed*.
- **Cheap route ruled out (F154).** The natural shortcut — the gluon-propagator log-moment $q_\ast a=\exp(\tfrac12\langle\ln K\rangle)$ — does **not** work: converged moments are UV scales ($\langle\ln K\rangle_\text{4D}=2$ exactly $\Rightarrow q_\ast^\text{bare}=e/a$; $1/K$-weighted $=2.30/a$), all above the band, while the band is reached only by an IR-divergent grid-dependent weight. $q_\ast$ is the UV-finite lattice−continuum *subtraction*, not a bare moment — confirming no shortcut substitutes for the full one-loop integral.
- **Loop ASSEMBLED, $b_0$ gate PASSED exactly (F162).** The background-field one-loop gluon self-energy is now assembled (Abbott/HKYS $\xi{=}1$: gluon loop $\Gamma^F\Gamma^F$ + ghost loop $-2(2k{+}q)(2k{+}q)$, `ca_bgfield_loop.py`) and its UV log part is **exactly transverse** with $b_0=\tfrac{11}{3}C_A=\mathbf{11}$ (gluon:ghost $=10{:}1$; scalar-bubble calibration $g{=}1$) — the loop-assembly validation F155 lacked. Confirmed (well-conditioned, subtracted) that the lattice propagator leaves $b_0$ unchanged ($\Delta=B_\text{lat}-B_\text{cont}$ q-flat, Wilson $<10^{-3}$; rule shift $\to0$, near-perfect action $\Rightarrow$ band top). **Still open:** the **finite** $d_1$ to the digit needs the bespoke lattice 3-gluon+ghost $\cos(k/2)$ **vertex form factors**, validated against the Wilson finite constant ($\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$) — not executed. So A's *running* is now certified exact on the lattice; the *bracket* $q_\ast a\in[1/\sqrt3,\sim0.97]$ (implied $0.733$ inside) still stands for the matching scale, with the vertex form-factor finite part as the sole remaining computation.

### Residual B — the IR face: the gap-saturated coupling $\alpha_\text{eff}^\ast$ — **SOLVED (F154)**
- **What it is.** The frozen effective coupling $\alpha_\text{eff}^\ast\approx0.39$ at which the chiral condensate forms.
- **Status: solved (F154).** The full nonlinear self-consistent $M(k)$ gap was built (`ca_gap_solve.py`) and solved. With the physical constituent mass $M(0)=311$ MeV imposed, the converged, $L$-stable coupling is $\alpha_\text{eff}^\ast=0.3764$ ($m_D{=}0.532$) / $0.4111$ ($m_V{=}0.727$) — reproducing F151-S5/F152 to 3 digits. Clarifications: the physical gap needs $G/G_c=2.4$–$3.6$ (nonlinear), not the linearised onset $1.277$; and the naive perturbative running overshoots ($M_0\approx1570$ MeV), so $\alpha_\text{eff}^\ast$ is a genuine nonperturbative input below the running.
- **What remains within B.** Two sub-items: (i) deriving the *freeze value* $0.39$ from the saturation mechanism **without** anchoring $M(0)$; (ii) the absolute MeV scale of $M(0)$ itself — which is Residual A. So B's dimensionless gap physics is closed; its absolute normalisation waits on A.

### Smaller dependent items (fall out once A and/or B close)
- **$f_\pi$ anchor → derived** (F123): once $\Lambda$ is absolute (A) and the condensate is solved (B), $f_\pi$ is an output, not a hand anchor.
- **$\lambda_6$ / the lepton brake** (F150): the IR-face value at saturation; closes with B.
- **The hierarchy $N$** (F119): already ×1.9 of target from running (F144); tightens with A.
- **$g_A$, $M_N$, $r_c$, $g_{\rho\pi\pi}$** (audit cluster 3): these need the dynamical baryon (roadmap P2), *not* the scale-setting constant — they are a separate, parallel debt and should not be conflated with A/B.

## 6. Why no robust full solution yet — the pattern

Each angle of attack has been *correct and productive* but bottoms out on A or B:
- Routes that fix **couplings/ratios** (F45 angle, F115 reduction, F144 lock, F145 Fierz) all terminate at "…times one nonperturbative scale/normalization."
- Routes that measure **condensate observables** ($\sigma$, $m_D$, $f_\pi$) give numbers in *lattice* units and need A to convert to physical units in one scheme.
- Routes that attack the **lepton brake** (F95/F118/F150) reduce $\lambda_6$ to "the saturated-condensate normalization" = B.

The two-face split (F151) is what finally separated these: the UV pile-up is residual **A**, the IR pile-up is residual **B**. The reason there is still no *value* is simply that neither A (a one-loop lattice integral) nor B (a self-consistent gap solve) has been executed — both are now isolated, well-posed, and individually falsifiable, which they were not before this session's findings.

## 7. Recommended next steps (in order)

1. **Residual A — the one-loop background-field constant** on the rule's action. Highest value: closes the UV face exactly, converts $\alpha_s(M_Z)$/$\Lambda$/$\sqrt\sigma$ from "bracketed" to "predicted," and is a finite, tadpole-free integral with a sharp pass/fail ($q_\ast=0.733/a$). First sub-task: extract the rotor action's gluon propagator + 3- and 4-point vertices on the BCC BZ.
2. **Residual B — the self-consistent $M(k)$ crossover solve** (F117 propagator + running). Closes the IR face, removes the F77 fit, and delivers $f_\pi$, $m_c$, $\lambda_6$ as outputs. Ingredients all exist as code.
3. Cross-check: A and B must be mutually consistent through the running (F151-S5) — running $\alpha_V(q_\ast)$ down to $m_D$ should land $\alpha_\text{eff}^\ast\approx0.39$. That consistency is itself a third, free falsification test once A and B are in hand.

## 8. One-line state of play

> The strong-sector scale problem is no longer one knot but two clean threads — a UV scheme constant (determined to a $\sqrt3$ band; needs one lattice-PT integral) and an IR gap-saturated coupling (scale and branch fixed; needs one self-consistent gap solve). Everything else in the sector is either exact or waits on these two.

---

### Source findings
F70, F77, F88, F94, F99, F100, F101, F110, F115, F116, F117, F119, F123, F124, F129, F130, F144, F145, F146, F150, F151, F152; audit `project-audit-inputs-dynamism-2026-06-06.md`; routes review `docs/theory/qcd-calibration-derivation-routes.md`.

### External anchors (targets, not inputs)
$\sqrt\sigma/\Lambda_{\overline{\rm MS}}\approx1.79$ and Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}=28.81$ (arXiv:0805.2913, 1303.3279); FLAG $\Lambda^{(3)}=343(12)$ MeV; process-independent $\hat\alpha(0)/\pi=0.97(4)$ (arXiv:1912.08232); gluon mass $m_g\approx0.5(2)$ GeV (arXiv:1002.4151, 1010.1975); the static-potential $a_1=(93-10n_f)/9$ (Fischler / standard).
