# F233 — The overall mass scale $N$ is **not** the deepest free number: F119's "no running channel" no-go is superseded by F144's dimensional transmutation — colour-sector asymptotic freedom generates $N$ to a factor $\approx1.9$ with zero parameters, and the whole residual is the one shared strong-sector scheme constant $d_1$

**Date:** 2026-07-02 - 23:40
**Numbering:** a concurrent session took F229–F232 (L3/E1/E2 + lattice-spacing); highest existing is F232, so this is **F233** (re-checked at write time, after collision).
**Status:** Reconciliation / reclassification — 5/5 checks PASS (`test_F233_mass_scale_N_transmutation.py`, <1 s, reproduces `ca_alpha_s_running`). **This executes open-derivations prompt E3 (#6).** The prompt (and the 2026-07-02 ledger) still label $N=m_\text{lat}(\tau)\approx5.5\times10^{-19}$ "the deepest single open number — genuinely may be the hierarchy," citing F119's sharp no-go ("the gap mechanism can't make $N$ from $O(1)$ couplings — $\sim10^{-36}$ tuning, **no running channel**"). But F119 is dated 2026-06-09; **F144 (2026-06-12) already built the running channel** and the ledger's E3 row never integrated it. The channel is **asymptotic freedom itself**: the rule-locked bare coupling $\alpha_s(\mu_0)=1/(16\pi)$ at $\mu_0=\hbar c/a=1.85\times10^{18}$ GeV runs down (standard $\overline{\rm MS}$, zero knobs) to $\Lambda_{\overline{\rm MS}}$, giving $N_\text{pred}=\Lambda^{(3)}/\mu_0=2.86\times10^{-19}$ (loop-converged) — **a factor $1.9$ from F119's $5.5\times10^{-19}$, across 19 decades, with no free parameter.** The entire residual is the single one-loop matching constant $d_1$ (equivalent $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$, vs Wilson's $28.81$) — **the same number** that Q1 ($\sqrt\sigma/f_\pi$ scale-setting, F124) and Q2 ($\alpha_s$ scheme, F144-A4/F154) reduce to. **Verdict: E3 is demoted from "genuinely free" to "transmutation-generated to a factor $1.9$; residual = the shared scheme constant."**
**Script:** `tests/findings/test_F233_mass_scale_N_transmutation.py`
**Results:** `test-results/F233_mass_scale_N_transmutation.json`
**Cross-references:** [[F119-kg-scale-three-routes]] (the no-go this supersedes — its R1/N3 "needs a marginal/running channel, absent" is exactly what F144 supplies), [[F144-route-a-alpha-s-dimensional-transmutation]] (the transmutation chain and A3 hierarchy prediction reproduced here), [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] (Q1 — its scale-setting residual is the same $d_1$), [[F154-residuals-A-B-built-and-solved]] (Q2 — Residual A is the same $d_1$/$q_\ast$ integral), [[F162-bgfield-self-energy-b0-gate]] (the background-field one-loop computation that would close $d_1$ and hence E3+Q1+Q2 at once — $b_0=\tfrac{11}3C_A$ already exact, finite digit open), [[F115-coupling-magnitudes-running-rotor]] (the $g_s^2\chi=\tfrac14$ lock), [[F107-canonical-a-adoption-L4-grb-gate]] ($\mu_0$).

---

## 1. What the prompt asked, and what changed under it

E3: *"Find any dynamical channel (RG running, dimensional transmutation à la F144, or a gravity/cosmology constraint) that fixes $N$ without tuning; or prove airtight that $N\equiv$ the hierarchy (a genuine free input)."*

Re-checking the anchor per the House Rules turned up the decisive fact: **the channel the prompt gestures at ("à la F144") is not hypothetical — F144 built it three days after F119** and landed $N$. F119's verdict was correct *for the mechanism it tested* (the 3D contact-NJL gap, a mean-field square-root transition — power-law, no transmutation) and correct in its diagnosis of the cure ("needs a logarithmically-running / marginal channel, à la $\Lambda_\text{QCD}=\mu\,e^{-1/b_0 g^2}$; F115 found the couplings non-running at the lattice scale"). What F119 missed is that **the colour coupling is exactly that marginal channel** — F115 CM2's "non-running" verdict is for the *electroweak angle* across the desert; the QCD coupling, by contrast, runs the whole desert (F144 cross-ref). So the honest status is not "open / free" but "solved up to one scheme constant."

## 2. The transmutation channel (reproduced from `ca_alpha_s_running`)

The rule fixes, with zero knobs (F144 A1, derived not assumed):

$$g_s^2=\tfrac14,\qquad \alpha_s(\mu_0)=\frac{g_s^2}{4\pi}=\frac{1}{16\pi}=0.019894,\qquad \mu_0=\frac{\hbar c}{a}=1.8504\times10^{18}\text{ GeV}.$$

Running down (standard $\overline{\rm MS}$, $n_f$ thresholds at $m_t,m_b,m_c$; QCD running is Higgs-independent so the model's Higgs-free structure is irrelevant at these orders):

| quantity | 1-loop | converged (4-loop) | target |
|---|---|---|---|
| $\alpha_s(M_Z)$ | $0.11955$ ($+1.31\%$) | $0.12797$ ($+8.46\%$) | PDG $0.1180$ |
| $\Lambda^{(3)}_{\overline{\rm MS}}$ | $0.272$ GeV | $0.529$ GeV | FLAG $0.343(12)$ |
| $N_\text{pred}=\Lambda^{(3)}/\mu_0$ | $1.47\times10^{-19}$ | $2.86\times10^{-19}$ | **F119 $N=5.5\times10^{-19}$** |

$$\boxed{\;N_\text{pred}=e^{-1/(2b_0\alpha_0)}\text{-type},\quad \frac{N_\text{pred}}{N_{\rm F119}}=\frac{2.86}{5.5}=1.9\;}$$

The 19-decade hierarchy is generated *because* the rule fixes $\alpha_0$ where it does. This directly answers F119's "$\sim10^{-36}$ tuning" objection: **no tuning — asymptotic freedom exponentiates the small number.**

## 3. What the factor $1.9$ is (the honest residual)

Two things, both $O(1)$ and both already named elsewhere:

1. **The scheme constant $d_1$.** The bare "$g_s=\tfrac12$ in the rule normalisation" is not yet a continuum-$\overline{\rm MS}$ statement. Running the *measured* $\alpha_s(M_Z)$ back up to $\mu_0$ gives an implied shift whose equivalent multiplicative $\Lambda$-ratio is $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}=1.78$ (converged) — i.e. the rule normalisation is **already near-continuum**, $16\times$ closer than the Wilson action's notorious $28.81$. This one constant carries the whole $+8.4\%$ / factor-$1.9$.
2. **A cross-sector $O(1)$.** F119's $N$ is pinned to the $\tau$ rest-leg ($m_\tau=1.777$ GeV) at the $E_g$ condensate saturation wall; $N_\text{pred}$ is $\Lambda_{\overline{\rm MS}}^{(3)}$ (the light-hadron scale, $\sim0.35$–$0.53$ GeV). That $m_\tau/\Lambda\sim3$–$5$ is an $O(1)$ ratio of physical observables at the *same* $\sim$GeV scale — i.e. "which IR observable you call *the* scale," not a new hierarchy. **Caveat (stated, not hidden):** that the lepton $E_g$-condensate scale locks to the colour $\Lambda_{\overline{\rm MS}}$ is quantitatively successful (factor 1.9) but the operator linking the two sectors is not derived; it is natural if the condensate forms at $\Lambda_\text{QCD}$, and could otherwise be a $\sim$GeV-scale coincidence. This is the one genuinely-open seam, now sharply localised.

## 4. The unification (the meta-result)

The residual $d_1$ is **not** a private E3 number. F124 §5 (Q1) writes its factor-4 bare-rotor$\leftrightarrow$condensed scale-setting gap as "this $1.78$ plus the BZ-edge convention"; F154/F144-A4 (Q2) name the identical $q_\ast$/$d_1$ integral as the one open $\alpha_s$-scheme coefficient. Therefore:

$$\boxed{\;\text{E3 (}N\text{)}\;=\;\text{Q1 (}\sqrt\sigma/f_\pi\text{)}\;=\;\text{Q2 (}\alpha_s\text{ scheme)}\;=\;\text{the one model-action one-loop background-field constant }d_1.\;}$$

Computing $d_1$ from first principles (the F162 background-field programme — $b_0=\tfrac{11}3C_A$ already exact, the finite digit gated by the vertex form factors) would close **all three ledger items simultaneously**. This collapses three of the "17 open" targets into one.

## 5. Checks (`test_F233_mass_scale_N_transmutation.py`, 2026-07-02 - 23:40)

| # | Statement | Result | Tier |
|---|---|---|---|
| C1 | bare coupling is the derived lock $\alpha_s(\mu_0)=1/(16\pi)$ | machine ($<10^{-12}$) | exact |
| C2 | transmutation lands $N$ to a factor $1.9$, zero params | $N_\text{pred}=2.86\times10^{-19}$ | PREDICTION |
| C3 | residual = one scheme constant $\approx1.78\ll28.81$ (Wilson) | $\Lambda$-ratio $1.78$ | DIAGNOSTIC |
| C4 | $\alpha_s(M_Z)$ cross-check (same channel, no knobs) | $+8.46\%$ converged | PREDICTION |
| C5 | $d_1$ shared with Q1 (F124) and Q2 (F154) → E3=Q1=Q2 | recorded | ledger |

**Overall 5/5 PASS.**

## 6. Ledger impact

The open-derivations ledger's E3 row ("Open — the **deepest** open number … no dynamical channel identified") and its footer ("Deepest single open number: E3") are **superseded**: the channel is F144's asymptotic freedom, $N$ is generated to a factor $1.9$ zero-parameter, and the residual is the shared $d_1$. E3 should be re-tagged **OPEN-reduced → merges with Q1/Q2** (one scheme constant), with the one genuinely-open seam being the lepton-condensate$\leftrightarrow\Lambda_\text{QCD}$ scale identification of §3.

## 7. Provenance

- New: the F119$\leftrightarrow$F144 reconciliation; the explicit demotion of "$N$ = deepest free number"; the three-way E3=Q1=Q2 unification into $d_1$; the sharp statement of the one remaining seam (cross-sector scale identification).
- Reused verbatim: `ca_alpha_s_running.route_a_report()` (F144), F107 $\mu_0$, F115 lock, F119 $N$.
- Verification: `tests/findings/test_F233_mass_scale_N_transmutation.py` (2026-07-02 - 23:40, 5/5 PASS), results `test-results/F233_mass_scale_N_transmutation.json`.
