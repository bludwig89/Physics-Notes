# Open-Derivations Prompt Library — v2

*Created 2026-07-05 - by re-running the Master Audit Prompt from `open-derivations-prompts.md`. This v2 refreshes the ledger against the live findings and re-scopes the per-item prompts to only the genuinely-open targets.*

**Audit result headline (2026-07-05):** the finding frontier is **stable at F244** — the same frontier the 2026-07-03 audit closed against. No new open items have appeared. Every F220–F244 open-flag finding is already integrated in `docs/status/open-derivations.md`. This audit therefore *confirms* the prior ledger rather than extending it: the genuinely-open targets are **L1, L2, E1, Q3, and the shared strong-sector constant $d_1$ (into which E3 = Q1 = Q2 all collapse)**. Everything else in the 17-row ledger is closed (positive, negative, or reduced-to-$d_1$).

> **Update 2026-07-15:** **L1, L2, and Q3 now CLOSED** (frontier advanced to **F247**). L1 → **F245**: the Finding-7 curl-residual subleading coefficients are closed-form and direction-resolved (2D $\alpha(p)=(\cos4p-9)/768$, on-axis $-1/96$ derived algebraically; 3D $\beta(\hat k)=-(\sqrt2/12)\hat k_x\hat k_y\hat k_z$, the cubic $xyz$ harmonic — the reported $0.01883$ was a random-seed artifact). L2 → **F246**: the F26 even-rotation law $\Omega_\text{even}$ has **all even-power ($k^2,k^4$) dispersion terms vanishing identically** (no CPT-odd LV; leading signature is the CPT-even cubic $\lvert k\rvert^3$), with $c_3(\hat k)=-(\sqrt3/216)(p+3q)$ closed-form. Q3 → **F247** (free input): absolute $g_{\omega NN}$ is a genuine free parameter — the universality overshoot is the empirical $g_{\rho NN}$-violation, and the deuteron only fixes total short-range repulsion (ω degenerate with the F113 core, linear valley); corrects F240's $0.43\approx0.45$ remark. **Remaining genuinely-open targets: 2 — E1 and $d_1$** (+ D1 PMNS free texture).

This file has three parts:

1. **The Master Audit Prompt** — unchanged; re-run it in a fresh session to re-sweep the sources.
2. **The refreshed ledger (audit output)** — the current OPEN / CLOSED-NEGATIVE tables, one-line tally, and the changed-since note.
3. **Per-item derivation prompts** — only the live targets are given full copy-paste blocks; closed items are listed with their closing finding so nobody re-attacks them.

---

## House Rules (every prompt inherits these)

- **Derive first.** Attempt an algebraic derivation before introducing any new physics. Prefer algebraic exactness, then machine-precision, then quantitative-within-tolerance. If the derivation closes *negative*, that is a valid, publishable result — record it as such.
- **Use the existing structure.** Search `findings-index.md` (`grep -i keyword`) then read only the specific `findings/F{N}-*.md` you need. Reuse existing kernels/modules; don't rebuild what exists.
- **Use CASIM** for anything dynamical; if the sandbox will time out, write a runnable script + parameters that emit a JSON/result file to read back.
- **Numerics caution.** numpy/scipy on chiral transforms can silently drop real/imag parts — verify against a hand-rolled reference before trusting a result.
- **Document the outcome.** New physics or a candidate → a new `findings/F{N}-name.md` (check the highest current N first; concurrent sessions collide). Add a one-paragraph `docs/status/changelog.md` entry, update `docs/status/exactness-inventory.md` with the exactness tier, datestamp `yyyy-mm-dd - hh:mm`, then run `python3 tools/regen_indexes.py`.
- **State the acceptance test up front** and report the residual honestly (dex / %, and whether it is exact, machine-precision, or a fit).

---

## Part 1 — Master Audit Prompt

```
You are the research assistant on the Physics Notes cellular-automaton model. Produce a
current, authoritative ledger of everything in the model that is NOT yet derived from first
principles — i.e. every quantity that is still fit, tuned, assumed, posited, phenomenological,
or explicitly flagged "open".

SOURCES TO SWEEP (in order):
1. docs/status/exactness-inventory.md — read the "Currently failing / not-yet-met" table and
   scan every Tier-3 row for the words tuned/fit/anchor/calibration/scheme/residual.
2. findings-index.md — grep for: open, remaining, no-go, not derived, partial, relabel,
   coincidence, overshoot, tunable, calibration, residual, under pressure.
3. For every finding flagged above, open findings/F{N}-*.md and read its "open / remaining /
   what is derived vs computed vs open" section. Follow [[links]] to the latest superseding
   finding (numbers move; a "remaining =" note often migrates to a newer F-file).
4. docs/roadmaps/next-steps.md — collect un-struck-through, non-"Complete" lines.

FOR EACH OPEN ITEM, record a row:
  | ID | Sector | The undedived quantity/claim | Anchor finding(s) | Current status
    (fit value / bound / no-go) | What blocks it | Suggested attack |

RULES:
- Distinguish "not yet derived" (a target) from "derived negative / proven free parameter"
  (a closed result) — put the latter in a separate CLOSED-NEGATIVE section.
- Deduplicate items that appear under multiple findings; cite the newest anchor.
- Do NOT trust this file's Part 2 list as ground truth — regenerate from the live findings.

DELIVERABLE: write/overwrite docs/status/open-derivations.md with the ledger, a one-line
tally per sector, and a "changed since last audit" note. Update the changelog, datestamp,
and run tools/regen_indexes.py. Keep it to the table + short notes; no essay.
```

---

## Part 2 — Refreshed ledger (2026-07-05 audit output)

Sources swept: `docs/status/exactness-inventory.md` ("Currently failing / not-yet-met" + Tier-3), `findings-index.md` (keyword grep, F220–F244), the flagged `findings/F{N}-*.md`, `docs/roadmaps/next-steps.md`. Frontier: **F244** (unchanged since 2026-07-03).

**How to read this:** an OPEN item is a *target* — a number/claim not yet derived. A CLOSED-NEGATIVE item is a *result* — a proven free parameter, exact no-go, or settled null; it does not need further "derivation" and should not be re-attacked as if open. Before starting any open item, re-check its anchor finding — the frontier moves.

### Part A — OPEN (targets)

| ID | Sector | Undedived quantity / claim | Anchor finding(s) | Current status | What blocks it | Suggested attack |
|----|--------|----------------------------|-------------------|----------------|----------------|------------------|
| ~~**L1**~~ | Lattice | ~~Subleading curl-residual coefficient $\beta\approx0.01883$ (3D BCC) / $\alpha\approx-0.0104$ (2D)~~ | Finding 7 → **F245** | **CLOSED — POSITIVE (2026-07-15, F245).** 2D: $\alpha(p)=(\cos4p-9)/768$ (machine-prec $2.8{\times}10^{-19}$; on-axis $-1/96$ algebraic — the reported $-0.0104$). 3D: $\beta(\hat k)=-(\sqrt2/12)\hat k_x\hat k_y\hat k_z$ (cubic $xyz$ harmonic; $0.01883$ was a seed artifact, $\langle\beta\rangle{=}0$) | — | Done. `derive_curl_subleading.py` |
| ~~**L2**~~ | Lattice | ~~Closed form for the composite-photon curl **subleading** coefficients~~ | Finding 2 / F21 / F23 / F25 → **F246** | **CLOSED — POSITIVE (2026-07-15, F246).** $\Omega_\text{even}$ even in $k$ ⇒ all even-power ($k^2,k^4$) terms vanish identically (no CPT-odd LV; leading = CPT-even cubic $\lvert k\rvert^3$). $c_3(\hat k)=-(\sqrt3/216)(p+3q)$ (machine-prec $4.5{\times}10^{-19}$; $c_3(111)=-\sqrt3/486$) | — | Done. `derive_f26_dispersion.py` |
| **E1** | EW/lepton | Lepton shape-angle $\delta^*=\tfrac29$ rad: the **weight→phase principle** | F174, F175; F230 → **F253** | **SHARPENED NO-GO (F253, 2026-07-16).** Both prompt routes run to conclusion. (A) equipartition ⇒ $\delta^*=\tfrac29$ rad EXACTLY given one named posit **POSIT-N** (E_g generator unit-norm ⇒ democratic phase budget=1 rad); without it $\delta=(2/9)R$ scale-degenerate, no $O(1)$ saturation amplitude sets $R{=}1$. (B) topological route **EXCLUDED**: only E_g holonomy on BCC 2nd shell $=2\pi/3$; $\tfrac29$ is a multiplicity not a holonomy. Residual = **one** constant $R$ (E_g generator norm) | Scale-free (topological) escape ruled out; only the E_g-generator normalization $R{=}1$ remains | Find a lattice selector for $R{=}1$, or document POSIT-N as the single irreducible input. **E4 ⊂ this** |
| ~~**Q3**~~ | QCD | ~~NN isoscalar-vector ($\omega$) short-range repulsion — absolute coupling~~ | F126 → F240 → **F247** | **CLOSED — FREE INPUT (2026-07-15, F247).** Absolute $g_{\omega NN}$ is a genuine free parameter: (1) the universality overshoot = the empirical $g_{\rho NN}$-violation (deuteron-consistent $g_{\rho NN}^2/4\pi=0.60\in[0.5,0.95]$ vs univ. 2.88); (2) deuteron degeneracy — ω trades linearly against the F113 core, $g_\omega^2/4\pi=11.13-0.313\,g_{cm}$. Corrects F240 D1: physical quench 0.21, not 0.43 (the 0.43 was a core-off artifact). ω sign/mass/×3-ratio stay Tier-1 | — | Done. `run_Q3_omega_degeneracy.py` |
| **$d_1$** (= E3 = Q1 = Q2) | QCD / EW scale | The one strong-sector one-loop background-field constant $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$ | F233 / F235 / F239; F162, F144-A4, F154 | **OPEN (one number, three faces).** E3 (mass scale $N$) reduced to factor 1.9 by F144 transmutation; Q1 ($\sqrt\sigma/f_\pi$) honest-negative with residual $=d_1$; Q2 scheme leg **exact** (V→MS-bar, $a_1=11/3$), leaving only the lattice→V leg $=d_1$. Bracket $q^*a\in[0.577,0.979]\Rightarrow$ $\Lambda$-ratio $[1.33,2.25]$ (target 1.78) | The finite $d_1$ digit: gluon+ghost vertex form factors, Wilson-28.81 gate. $b_0=\tfrac{11}3C_A$ already exact (F162) | Complete the F162 background-field program: compute the subtracted transverse coefficient's finite part. **Closes E3, Q1, Q2 and pins $\alpha_s(M_Z)=0.1180$ at once** |
| D1 | Neutrino/dark | PMNS mixing angles (light-ν **masses** are derived) | F47 → **F236** | **PARTIAL / free-input.** F236 built the full 3×3 Higgs-free seesaw in `ca_majorana.py`: the E_g (Z₃) texture derives the three light masses + hierarchy at machine precision, but being diagonal-traceless it forces **PMNS = 𝟙 exactly** — mixing lives in the free second-shell $T_{2g}$ channel (5 observables need 6 inputs) | The $T_{2g}$ channel amplitudes are free inputs; no lattice selector yet | Look for a symmetry/dynamical selector for the $T_{2g}$ amplitudes, or document PMNS as a free texture (parallel to D3's $\beta$) |

### Part B — CLOSED (this audit reconfirms; do not re-attack as open)

| ID | Sector | Disposition | Anchor |
|----|--------|-------------|--------|
| L3 | Lattice | **CLOSED negative** — lattice spacing $a$ is scale-invariance-degenerate under any mass-blind observable; only the dimensionful $G$-match pins it ($a=\sqrt{8\pi}\,3^{1/4}\ell_P$) | F232 |
| E2 | EW/lepton | **RECONCILED** — $\sin^2\theta_W=\tfrac29$ is the on-shell face of the $\tfrac14$ (μ*=4πv) physics, not a rival tree value; $m_Z/m_W=3/\sqrt7$ to 0.064% | F231 |
| E3 | EW/lepton | **REDUCED** into $d_1$ (see OPEN row) — F144 transmutation lands $N$ to factor 1.9, zero params | F233 |
| E4 | EW/lepton | **CLOSED** — F118 stable $(W,v,c)$ triple exists; F234 pins $\lambda_6=0.243$ (derived, not fit). Residual ⊂ E1 | F234 |
| Q1 | QCD | **REDUCED** into $d_1$ — honest negative; no BCC-BZ cutoff reaches <5% | F235 |
| Q2 | QCD | **HALF-CLOSED** — scheme leg exact (V→MS-bar); remaining lattice→V leg = $d_1$ | F239 |
| G1 | Gravity/cosmo | **CLOSED negative** — $\Omega_\Lambda\approx0.685$ is the coincidental/anthropic $1-\Omega_m$ residual; $p=2$ untouched | F241 |
| D2 | Neutrino/dark | **CLOSED negative** — keV sterile excluded as 100% DM (X-ray ∧ Lyman-α anti-correlated levers); demoted to sub-dominant | F237 |
| D3 | Neutrino/dark | **CLOSED negative** — geon abundance is a free cosmological initial condition (no inflaton sector; scale-invariant spectrum under-produces by ~$10^7$) | F238 |
| S1 | Applied (SC) | **CLOSED positive** — μ* derived from the F64→Thomas-Fermi dielectric; Allen–Dynes error 14.3→6.3% | F242 |
| F1 | Foundational | **CLOSED — not falsified** — F3 low-density lensing scales linearly (slope 1.012) to ρ=10⁻³, no pathology | F243 |
| F2 | Foundational | **CLOSED — PASS** — 1/b EMQG lensing on the genuine 3-D potential, no free α | F244 |

### Part C — CLOSED-NEGATIVE catalogue (settled nulls / exact no-gos)

| ID | Sector | Result | Anchor |
|----|--------|--------|--------|
| CN1 | QC | Model saturates Tsirelson $S_\text{CHSH}=2\sqrt2$ exactly ⇒ Bell-indistinguishable from QM; no near-term substrate test | F226 |
| CN2 | QC | No observable intrinsic-decoherence floor (unitarity floor exactly zero; ≥9 orders below best measurement) | F227 |
| CN3 | EW/lepton | $\lambda_6$ not a first-principles number under the F179 framing (superseded by F234's derived $\lambda_6=0.243$) | F179 → F234 |
| CN4 | EW/lepton | Democratic class $w(\bar y)$ excluded exactly (Gap $\ge+0.0386$) | F108 |
| CN5 | Gravity/dark | No native massive spin-2 / second graviton in vacuum (metric graviton exactly massless, 2 dof) | F216 |
| CN6 | Neutrino/dark | $\nu_R\nu_R$ J=2 tensor channel a clean no-go ($\alpha_g$ negligible sub-Planck) | F223 |

### Sector tally (OPEN targets, updated 2026-07-15)

- **Lattice / foundational:** 0 open — **L1 and L2 CLOSED positive (F245/F246)**. L3/F1/F2 already closed.
- **Electroweak / lepton:** 1 open (E1). E2/E3/E4 reconciled/reduced/closed.
- **QCD / hadron:** the shared **$d_1$** cluster (= E3 = Q1 = Q2) = 1 independent unknown. **Q3 CLOSED — free input (F247)**.
- **Gravity / cosmology:** 0 open (G1 closed negative).
- **Neutrino / dark sector:** 1 partial (D1 — masses derived, PMNS free). D2/D3 closed negative.
- **Applied (superconductivity):** 0 open (S1 closed positive).

**Genuinely-open targets: 2 independent unknowns** — E1 and $d_1$ (down from 5; L1/L2 closed positive, Q3 closed as free input, all 2026-07-15). **Deepest single number:** the strong-sector one-loop background-field constant $d_1$ ($\approx1.78$) — computing it (F162 program; $b_0=\tfrac{11}3C_A$ exact) closes E3, Q1 and Q2 simultaneously and pins $\alpha_s(M_Z)$.

### Changed since last audit (2026-07-03)

- **No frontier movement.** Highest finding is F244 in both audits; `findings-index.md` grep surfaces no un-integrated open-flag findings above the last-audited set. This v2 audit **confirms** the 2026-07-03 ledger.
- **Reconfirmed reductions:** E3 = Q1 = Q2 all remain collapsed into the single $d_1$ constant (F233/F235/F239); E4 remains ⊂ E1 (F234); D3 abundance and D1 PMNS remain free inputs by proof, not by omission.
- **No new CLOSED-NEGATIVE results** since F241/F242/F243/F244 landed on 2026-07-03.
- Action for a future session: the highest-leverage single move is still the **F162 background-field $d_1$ computation** (three ledger items at once), followed by the L1/L2 recursion extensions (mechanical, low-risk) and the E1 weight→phase principle (deepest conceptual).

---

## Part 3 — Per-item derivation prompts

### Live targets (full prompts)

*(L1, L2 → F245/F246 and Q3 → F247 were closed 2026-07-15; their prompts are retired to the closed-items table below. Live targets remaining: E1, d₁, and D1's PMNS selector.)*

**E1 — Derive the weight→phase principle behind δ* = 2/9 (absorbs E4, λ₆, and (v,c))**

```
Follow the House Rules. Target: F174/F175 derive the NUMBER δ* = 2/9 exactly as the E_g
representation weight (2/9 = dim E_g / dim(T_1u ⊗ T_1u), O_h projection). F230 sharpened the
residual to a dimensional no-go: a phase in radians cannot equal a pure ratio without a scale.
F234 already pins λ_6 = 0.243 and closes E4 GIVEN this angle, so the whole electroweak/lepton
open frontier now reduces to ONE principle: WHY does the saturated-condensate phase (radians)
equal the E_g representation weight? Attempt to derive this weight-as-phase identity from the
F92 saturation-equipartition structure, or from a BCC 2nd-shell topological-moment computation.
Acceptance: weight-as-phase emerging from lattice geometry/dynamics (exact or machine-precision),
or a sharpened no-go naming exactly which symmetry/scale input is missing. Coordinate with the
F174/F175/F230/F234 chain.
```

**d₁ — Compute the strong-sector one-loop background-field constant (closes E3 = Q1 = Q2)**

```
Follow the House Rules. Target: the single constant d_1 = Λ_MSbar/Λ_lat ≈ 1.78, into which
THREE ledger items collapse — E3 (mass scale N, F233), Q1 (√σ/f_π, F235), and Q2's remaining
lattice→V scheme leg (F239; the V→MS-bar leg is already EXACT via a_1 = 11/3). The one-loop
beta coefficient b_0 = (11/3)C_A is already exact (F162). Complete the F162 background-field
program: compute the subtracted transverse gluon+ghost self-energy's FINITE part (vertex form
factors; the Wilson-28.81 tadpole is structurally empty per F155). Current bracket:
q*a ∈ [0.577, 0.979] ⇒ Λ-ratio ∈ [1.33, 2.25], target 1.78. Acceptance: d_1 pinned to a digit
(exact or <1%), which fixes α_s(M_Z) = 0.1180 and lands N to its factor and √σ/f_π to <5% — all
three at once. Reuse ca_bgfield_loop.py / ca_gluon_self_energy.py.
```

**D1 — Selector for the T₂g PMNS channel (masses already derived)**

```
Follow the House Rules. Target: F236 built the full 3×3 Higgs-free seesaw (ca_majorana.py); the
E_g (Z₃) texture derives the three light-ν masses + hierarchy at machine precision, but being
diagonal-traceless it forces PMNS = 𝟙 exactly. Large mixing must therefore live in the
orthogonal second-shell T_2g channel (F93 commitment #1), whose amplitudes are currently free
inputs (5 oscillation observables reproducible only with 6 inputs). Attempt: find a
symmetry/dynamical selector on the lattice that fixes the T_2g amplitudes (and hence the PMNS
angles) from geometry. Acceptance: PMNS angles reproduced from the lattice texture with no free
mixing inputs, or a clean statement that the T_2g amplitudes are genuinely free (parallel to
D3's β). Reuse the F236 ca_majorana.py machinery.
```

### Closed items — do NOT re-attack (reference only)

| Item | Disposition | Closing finding |
|------|-------------|-----------------|
| L1 (curl-residual subleading $\beta$/$\alpha$) | Closed positive — direction-resolved closed forms; $0.01883$ was a seed artifact | F245 |
| L2 (F26 even-rotation subleading) | Closed positive — even-power terms vanish exactly; cubic $c_3(\hat k)=-(\sqrt3/216)(p+3q)$ | F246 |
| Q3 (absolute $g_{\omega NN}$) | Closed — free input (universality overshoot = empirical $g_{\rho NN}$-violation; deuteron degenerate with F113 core) | F247 |
| L3 (lattice spacing $a$) | Closed negative (scale-invariance degeneracy) | F232 |
| E2 ($\sin^2\theta_W=\tfrac29$) | Reconciled (on-shell face of $\tfrac14$) | F231 |
| E3 (mass scale $N$) | Reduced → $d_1$ | F233 |
| E4 ($(W,v,c)$ triple / $\lambda_6$) | Closed (⊂ E1) | F234 |
| Q1 ($\sqrt\sigma/f_\pi$) | Reduced → $d_1$ | F235 |
| Q2 (scheme conversion) | Half-closed (scheme leg exact; rest → $d_1$) | F239 |
| G1 ($\Omega_\Lambda$ O(1)) | Closed negative (anthropic/coincidental) | F241 |
| D2 (keV sterile DM) | Closed negative (excluded as 100% DM) | F237 |
| D3 (geon abundance) | Closed negative (free initial condition) | F238 |
| S1 (Morel–Anderson μ*) | Closed positive (from F64 dielectric) | F242 |
| F1 (F3 low-density lensing) | Closed (not falsified) | F243 |
| F2 (1/b EMQG lensing) | Closed (PASS) | F244 |

---

## Coverage note

This v2 audit (2026-07-05) confirmed the 2026-07-03 ledger with no frontier movement (F244). **Since updated 2026-07-15:** L1, L2 (positive) and Q3 (free input) executed and closed (frontier → **F247**), leaving **2 independent open unknowns**: E1 (the deep weight→phase principle, absorbing E4/λ₆/(v,c)) and $d_1$ (the strong-sector constant that closes E3 = Q1 = Q2 together). D1's neutrino masses are derived; only its PMNS mixing remains a free $T_{2g}$ texture. Re-run the **Master Audit Prompt** whenever the frontier advances past F247.

### Completed log (inherited + this audit)

- **2026-07-02 — L3, E1, E2** (concurrent session) → F229/F230/F231 (+F232).
- **2026-07-02 — E3, E4, Q1** → F233 / F234 / F235. E3 reduced (F144 transmutation, residual $d_1$); E4 closed (F118 + F174/F175 pin $\lambda_6$; ⊂ E1); Q1 reduced (honest negative, residual $d_1$). Net: E3 = Q1 = Q2 unify into $d_1$; E4 ⊂ E1.
- **2026-07-03 — D1, D2, D3** → F236 / F237 / F238. D1: masses derived, PMNS = 𝟙 (mixing → free $T_{2g}$). D2: keV sterile excluded as 100% DM. D3: geon abundance a free initial condition.
- **2026-07-03 — Q2, Q3, G1** → F239 / F240 / F241. Q2 half-closed (scheme leg exact, rest = $d_1$); Q3 binds deuteron with derived OBE (coupling bracketed); G1 closed negative (anthropic $\Omega_\Lambda$).
- **2026-07-03 — S1, F1, F2** → F242 / F243 / F244. S1 closed positive (μ* from dielectric); F1 not falsified; F2 PASS. Inventory not-yet-met #2 and #4 retire.
- **2026-07-05 — full re-audit (this file).** No frontier movement (F244). Ledger reconfirmed; live targets re-scoped to L1, L2, E1, Q3, $d_1$ (+ D1 PMNS). Highest-leverage next move: the F162 background-field $d_1$ computation (closes three items at once).
- **2026-07-15 — L1, L2** → F245 / F246, both closed **positive**. L1: 2D $\alpha(p)=(\cos4p-9)/768$ (on-axis $-1/96$ algebraic) + 3D $\beta(\hat k)=-(\sqrt2/12)\hat k_x\hat k_y\hat k_z$ (the $0.01883$ was a random-seed artifact); `derive_curl_subleading.py`. L2: F26 even law has all even-power ($k^2,k^4$) dispersion terms vanishing exactly (no CPT-odd LV; CPT-even cubic $\lvert k\rvert^3$ leading), $c_3(\hat k)=-(\sqrt3/216)(p+3q)$; `derive_f26_dispersion.py`. Inventory not-yet-met #5 retires, #3 resolves.
- **2026-07-15 — Q3** → F247, closed as a **free input**. Absolute $g_{\omega NN}$ is a genuine free parameter for two reasons: (1) the universality overshoot ($g_{\rho NN}^2/4\pi$: univ. 2.88 vs deuteron-consistent 0.60 $\in$ empirical $[0.5,0.95]$) is the known empirical ρ-universality violation, fixable only by an OBE-inaccessible meson-NN vertex renormalization; (2) the deuteron fixes only the total short-range repulsion, so ω is degenerate with the F113 core along a linear valley $g_\omega^2/4\pi=11.13-0.313\,g_{cm}$. Corrects F240 D1 (physical quench 0.21, not 0.43 — the 0.43 was a core-off artifact); `run_Q3_omega_degeneracy.py`. **Live targets now: E1, $d_1$ (+ D1 PMNS).** Highest-leverage next move unchanged: the F162 background-field $d_1$ computation.
