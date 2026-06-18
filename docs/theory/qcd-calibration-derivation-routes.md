# QCD calibration block — algebraic derivation routes (review)

`2026-06-12 - 02:20`

**Scope.** The Phase-3 open item "QCD calibration block" (`docs/roadmaps/roadmap-scale-to-real-space.md`), i.e. the strong-sector free knobs flagged in the 2026-06-06 audit (C.6/C.7/C.10), F123 §5 and F124 §5. This note inventories what is still underived, maps each knob to an internal derivation source already in the model, and collects the external algebraic resources found by literature search. It is a routes review, not a finding; each route is a candidate F-number when executed.

---

## 1. The knob ledger (current status)

| # | Knob | Value | Status after F115/F116/F123/F124 |
|---|---|---|---|
| 1 | $f_\pi$ anchor (the strong-sector ruler; F119's hierarchy $N$) | 92.07 MeV | user-selected; "set by the anchor, not derived" (F123 §5) |
| 2 | $\hat g=G\Lambda^2$ | 2.10 | mechanism derived (F116 NJ4: induced, $G\sim\tfrac49 g_s^2/M_g^2$); exact coefficient OPEN |
| 3 | $\hat m_0=m_0/\Lambda$ | $8.4\times10^{-3}$ | flagged to the quark texture (F92–F109 machinery); OPEN |
| 4 | $\sqrt\sigma/\Lambda$ residual | model 0.569 vs 0.645 | F124: derived to ~12%; residual = scale-setting / dimensional transmutation |
| 5 | $g_A$ | 1.272 | external (Goldberger–Treiman input to F104/F126) |
| 6 | $g_{\rho\pi\pi}$ | $\simeq6$ | external Tier-3 (KSRF contrast only) |

$\Lambda$ itself is closed (BZ edge, F116 NJ2/NJ3); $g_s$ is closed (rotor lock $g_s^2\chi=\tfrac14$, F115).

---

## 2. Route A — the anchor itself: dimensional transmutation from the locked $g_s=\tfrac12$ *(headline)*

> **EXECUTED 2026-06-12 → F144** (`findings/F144-route-a-alpha-s-dimensional-transmutation.md`, 5/5): $g_s=\tfrac12$ *derived* (circularity lemma ⇒ $\chi=1$ + F110 C7); $\alpha_s(M_Z)$ converged $+8.4\%$ (1-loop $+1.3\%$); hierarchy $N$ ×1.9 of F119 — the "no running channel" gap closed. Open coefficient bounded: equivalent scheme $\Lambda$-ratio 1.78 (Wilson 28.81). The numbers below were the pre-build estimates.

The model already owns both ends of the standard hierarchy argument and has never connected them:

- **UV end:** $g_s=\tfrac12$ is *locked* at the BZ edge $\mu_0=\hbar c/a=1.85\times10^{18}$ GeV (F115 CM3 + F107), so $\alpha_s(\mu_0)=\tfrac{1/4}{4\pi}=1/(16\pi)=0.0199$ with **zero free parameters**.
- **IR end:** the hadron scale, currently anchored by hand at $f_\pi$.

Wilczek's Nobel lecture states the textbook result in exactly the model's terms: the proton/Planck hierarchy follows if "the basic unit of color coupling strength $g$ is of order $1/2$ at the Planck scale" — asymptotic freedom then *generates* the hadron scale as $\Lambda\sim\mu_0\,e^{-1/(2b_0 g^2)}$.

**Numeric check (this session, 1-loop with thresholds $m_t,m_b,m_c$):** running $\alpha_s(\mu_0)=1/(16\pi)$ down gives

$$\alpha_s(M_Z)=0.1195\ \ (\text{PDG }0.1180,\ +1.3\%),\qquad \Lambda^{(n_f=3)}_{\text{1-loop}}\approx154\ \text{MeV}.$$

Two-loop shifts to $\alpha_s(M_Z)=0.128$ ($+8\%$) and $\Lambda^{(n_f=3)}_{\overline{\rm MS}}\approx372$ MeV (PDG $\sim340$). A zero-parameter prediction of the measured strong coupling to $\sim$1–10% strongly suggests the $f_\pi$ anchor (and hence F119's $N\approx5.5\times10^{-19}$) is **derivable**, not free: $\Lambda_{\overline{\rm MS}}\to\sqrt\sigma$ (Route B) $\to f_\pi$ (F124 chiral factor $\Lambda/f_\pi=7.04$, exact) closes the whole chain.

**What makes it well-posed rather than numerology:**

1. The methodology is already validated in-house: **F138** closed the +12% Weinberg gap with precisely this move (a forced matching condition at a derived scale + one-loop running), reducing the EW gap from +8.12% to +0.22%.
2. The $O(1)$ ambiguity — what $g_s=\tfrac12$ *means* in continuum-scheme terms — is the classic bare-lattice-coupling scheme conversion, computable algebraically at one loop (Hasenfratz & Hasenfratz technique): for Wilson SU(3), $\Lambda_{\overline{\rm MS}}=28.81\,\Lambda_{\rm lat}$. The model needs the analogous constant for *its own* action (the F110 rotor / F26 rotation rule). That single computable constant is the honest open coefficient of Route A.
3. The 2026-06-12 audit's new runner (`tests/runners/run_su2_3d_fluxtube.py`) already demonstrates the mechanism inside the model class: σ from β alone, via dimensional transmutation.

**Caveats:** threshold matching above $m_t$ used SM $n_f=6$ (the model's spectrum near $\mu_0$ may differ); 1-loop vs 2-loop spread is the current error bar; the rule-normalisation→$\overline{\rm MS}$ constant is unfixed (point 2).

---

## 3. Route B — the F124 ~12% residual ($\sqrt\sigma/\Lambda$): scheme conversion + RG flow

F124 §5 located the residual in "the scale-setting the lattice-QCD world performs numerically rather than analytically." Two complementary closures:

- **External (algebraic):** the quenched SU(3) lattice value $\Lambda_{\overline{\rm MS}}=0.558^{+0.017}_{-0.007}\sqrt\sigma$, i.e. $\sqrt\sigma/\Lambda_{\overline{\rm MS}}=1.79$ (ALPHA-style running-coupling programme). Combined with Route A's $\Lambda_{\overline{\rm MS}}$, this predicts $\sqrt\sigma$ absolutely with no hadronic input, replacing F124's condensed-vacuum estimate as the cross-check rather than the source. Note the quenched ($n_f=0$) vs dynamical caveat.
- **Internal (the model's own RG):** F130-C1 established the bond-moving flow $g^2\to b\,g^2$ ($\lambda_\sigma=b$, Migdal–Kadanoff type) and that coarse F110 reproduces $V(b\cdot R)$ exactly. Running the locked $g_s^2=\tfrac14$ from the BZ edge through $n$ blockings until the rotor enters the condensed/strong-coupling regime (the F101 Gaussian→confinement crossover) gives $\sqrt\sigma\,a$ as a function of nothing — the analytic counterpart of the F124 "bare rotor vs condensed vacuum" factor ~4. The block-spin machinery (F130–F134) did not exist when F124 was written; this is the new internal resource.
- **Convention term:** F124 C5 flags the BZ-edge↔3-momentum-cutoff convention (axis $\pi/a$ vs sphere $(6\pi^2)^{1/3}/a$ spans 4.00–3.23 vs 4.56). The Hasenfratz-type one-loop constant in Route A is the principled resolution of exactly this convention ambiguity — Routes A and B share their one open coefficient.

---

## 4. Route C — $\hat g=G\Lambda^2=2.10$: the Fierz coefficient

> **EXECUTED 2026-06-12 → F145** (`findings/F145-route-c-induced-njl-coupling.md`, 5/5): exact Fierz $c=\tfrac29$ in all four chiral channels (F77 form *forced*; NJ4's $\tfrac49$ corrected ×4); **bare-coupling no-go** ($R=G/G_c=0.075$–$0.10$, momentum-resolved); χSB **guaranteed** by Route A's running ($R=2.6$–$15$, $\alpha_\text{crit}=0.20$–$0.27$); fit $1.277$ bracketed, $\Leftrightarrow\alpha_\text{eff}=0.26$–$0.34$. Residual = the nonperturbative IR coupling, shared with F124/F144-A4. The paragraphs below were the pre-build brief.

F116 NJ4 derived the mechanism ($G\sim\tfrac49\,g_s^2/M_g^2$, requiring $\Lambda/M_g=4.35$) but left the coefficient as "the full momentum-dependent Fierz reduction (the gluon/dielectric propagator integrated against the lattice loop)." Two things have changed since:

- **F117** wired the gap-coupled dielectric into the time-evolved even-law gluon propagator — the momentum-dependent propagator the NJ4 integral needs now *exists as code*. The computation is: Fierz the one-dielectric-gluon exchange into the scalar $q\bar q$ channel using the F117 propagator, integrate against the BZ loop (F116 NJ2 machinery), read off $\hat g$. No new physics, one integral.
- $M_g$ should not be a second input: $M_g=m_D=e\,v$ with $v=0.713$ measured (F88), so the predicted $\hat g$ is parameter-free once the F117 propagator is used.

External resources: the chiral confining model programme (Chanfray et al., arXiv:2501.10177) does precisely "CSB potential → Fierz → equivalent NJL with computed couplings"; the channel bookkeeping is standard (arXiv:2501.07658). These fix conventions (the $4/9$ vs $2/9$ Fierz-factor traps) rather than supply the model-specific propagator.

---

## 5. Route D — $g_A=1.272$: now unblocked by F122

The audit (C.7) correctly said $g_A$ needs the dynamical baryon; **P2 is now built** (F122 ECG three-body, closed-form matrix elements). $g_A$ is the axial-current matrix element in that state:

- Non-relativistic spin–flavour gives $g_A=\tfrac53\,g_A^Q$; the physical 1.272 is the $5/3$ times relativistic lower-component reduction — computable directly from the F122 wavefunction (the ECG basis gives $\langle\sigma_z\tau_z\rangle$ in closed form; the relativistic correction needs the small components of the F27 spinor, which the model has).
- Cross-checks from the literature: large-$N_c$/Skyrme $g_A\sim(N_c+2)/3$ ($=5/3$ at $N_c=3$, same leading answer, corrections organised in $1/N_c$); dressed-quark (DSE) computations of $g_A$.
- A successful $g_A$ also retro-derives the πNN coupling in F104/F126 via Goldberger–Treiman, removing the deuteron sector's one external coupling.

---

## 6. Route E — $g_{\rho\pi\pi}\simeq6$: KSRF / vector RPA

Lowest priority (decorative, F103-F only). Internal: extend the F77 RPA ladder to the vector channel (the ρ pole) — F123 H5 already uses KSRF $m_\rho^2=2g_{\rho\pi\pi}^2f_\pi^2$ as Tier-3, so deriving the vector-channel residue upgrades H5 from Tier-3 to PREDICTION and outputs $g_{\rho\pi\pi}$ at once.

## 7. Route F — $\hat m_0$: no shortcut

The current-quark texture is the quark-sector extension of the open lepton-spectrum problem (F92–F109, audit #2/#3). No external resource substitutes: in the SM the current masses are Yukawa inputs. Correctly remains parked with the $C/W$ sextic-brake programme; any solution there should be tested against $\hat m_0$ immediately (the $n$–$p$ splitting H3 already constrains the $d$–$u$ part).

---

## 8. Recommended priority order

1. **Route A** (anchor via dimensional transmutation) — highest value: a ~1–10% zero-parameter hit on $\alpha_s(M_Z)$ already exists; success converts *every* F123 MeV row from "anchored" to "predicted" and closes F119's $N$. First sub-task: the one-loop scheme-conversion constant for the model's action (shared with Route B).
2. **Route C** ($\hat g$ Fierz integral) — all ingredients exist as code (F116 loop + F117 propagator + F88 $v$); one integral, removes the largest NJL knob.
3. **Route D** ($g_A$ from F122) — unblocked, closed-form basis, removes the deuteron sector's external coupling.
4. **Route B** internal flow (block-spin σ run) — shares its open coefficient with Route A; do after/with A.
5. **Route E** (vector RPA) — low priority.
6. **Route F** ($\hat m_0$) — parked with the lepton-spectrum programme.

## 9. External resources (collected)

- Wilczek, *Asymptotic Freedom: From Paradox to Paradigm* (Nobel lecture) — $g\sim1/2$ at the Planck scale ⇒ proton mass; the Route-A argument: https://arxiv.org/pdf/hep-ph/0502113
- Lepage, *Advanced Lattice QCD* — bare-lattice-coupling pathologies and scheme conversion context: https://arxiv.org/pdf/hep-lat/9802029
- $\Lambda_{\overline{\rm MS}}/\Lambda_{\rm lat}=28.809$ (one-loop, Wilson SU(3); the Hasenfratz-type constant Route A needs for the model's own action): https://arxiv.org/pdf/1303.3279
- Continuous-β-function determination of $\Lambda_{\overline{\rm MS}}$ SU(3): https://arxiv.org/abs/2303.00704
- $\Lambda_{\overline{\rm MS}}=0.558\,\sqrt\sigma$ (SU(3) lattice; Route B external leg): https://arxiv.org/pdf/hep-lat/9208028
- Running coupling in pure SU(N), $\sqrt\sigma/\Lambda_{\overline{\rm MS}}\approx1.77$–$1.79$: https://arxiv.org/pdf/0805.2913
- Chiral confining model (CSB potential → Fierz → NJL couplings; Route C conventions): https://arxiv.org/pdf/2501.10177 and https://arxiv.org/html/2501.07658
- Dressed-quark $g_A$ (DSE): https://arxiv.org/pdf/1207.5300
- Large-$N_c$ constituent-quark/Skyrme equivalence, $N_c\to N_c+2$ shift in $g_A$: https://arxiv.org/pdf/hep-ph/9304262
- Relativistic constituent-quark $g_A/g_V$ (lower-component reduction): https://arxiv.org/pdf/hep-ph/0408041

## 10. Honest caveats

- Route A's session numerics used the *continuum* $\overline{\rm MS}$ β-function from $\mu_0$ down with SM thresholds; the model's statement "$g_s=\tfrac12$ in the rule normalisation" (F115) is not yet a statement in any continuum scheme. The conversion constant is the entire respectability of the 1–10% agreement — treat the numbers above as motivation, not results, until it is computed.
- $\sqrt\sigma/\Lambda_{\overline{\rm MS}}=1.79$ is quenched; with light flavours the ratio shifts (and σ itself is string-breaking-ambiguous). State which theory each leg lives in when assembling the chain.
- Concurrent sessions: F135–F141 are taken; check `findings-index.md` before assigning a number to any executed route.
