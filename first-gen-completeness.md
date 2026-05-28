# First-Generation Particle Model — Completeness Review

*2026-05-25 - 14:00 — Rigorous review of the BCC lattice-CA model against the requirements for a complete first-generation Standard-Model particle sector. Determines what is present, what must be added, outlines the tests still to run, and flags code no longer in use. Supersedes the 2026-05-22 `project-review-*.md` set for the particle-content question only; those remain valid for the broader physics/test summary.*

*2026-05-26 - 02:02 — **FG-1 ran and passed exactly.** All six anomaly traces over the first-generation chiral content vanish as exact rationals (not "to machine precision" — to **0/1**). Results in [`test-results/FG1_anomaly_cancellation.json`](test-results/FG1_anomaly_cancellation.json); test script at [`model-tests/test_FG1_anomaly_cancellation.py`](model-tests/test_FG1_anomaly_cancellation.py). Rows updated below: §2.3 anomaly row promoted to ✅; §5.1 FG-1 row shows the run result; §7 sequencing item 1 closed.*

*2026-05-26 - 03:15 — **FG-6 ran and passed.** Extended `ca_maxwell.py` to construct a two-helicity composite photon from BOTH BCC chirality branches (sign='+' and sign='-'); new helpers `EM_bilinears_branch`, `EM_bilinears_two_helicity`, `riemann_silberstein_decomp`, plus the matching W-triplet pair `triplet_bilinear_branch` / `triplet_bilinear_two_helicity`. Test suite `model-tests/test_FG6_two_helicity_photon.py` runs 10 tests (all PASS, 0.30 s total): per-branch singlet SU(2) invariance (3.4e-16), per-branch triplet adjoint rotation (2.6e-16), assembler linearity (0.0), Riemann-Silberstein E=(F^++F^-)/2 identity (0.0), chiral propagation F^+→Ω^+ and F^-→Ω^- per-helicity tracking (1.5e-15 over 10 ticks across 12 cases), F30 birefringence coefficient $-\sqrt3/27$ along (1,1,1) (4.5e-5 relative), and the F29-B4 raw triplet transversality scaling (2.9e-2 at k=0.05, matching c_lat·|k| = 0.0289). Results in [`test-results/FG6_two_helicity_photon.json`](test-results/FG6_two_helicity_photon.json); full write-up in [`findings/F39-two-helicity-photon-bilinear.md`](findings/F39-two-helicity-photon-bilinear.md). Closes §3 item 4 (two-helicity photon) and §5.1 FG-6.*

*2026-05-26 - 16:30 — **FG-2 and FG-3 ran and passed (Finding F40).** Two of the three structural gaps closed: (a) the quark sector now uses the project's adopted **F27 chiral-SU(2) complex-mass mechanism** (no Higgs), per flavour, per colour, with natural up/down/strange mass splitting; (b) the quark doublet $(u,d)_L$ is now **wired to a dynamical $W_\mu$ link field** via a 2D-square analog of F31/F34. Phase 1 (FG-2) — **11/11 PASS in 2.0 s**: per-flavour U(1) Ward identity $1.2\times10^{-16}$; degenerate-doublet SU(2)$_L$ Ward identity $8.4\times10^{-17}$; cold-link θ=0 regression bit-for-bit (0.0); mass splitting $r_d/r_u=3.96$ (exp 4), $r_s/r_u=15.22$ (exp 16); colour-charge conservation $1.7\times10^{-14}$. Diagnostics Q10 (split mass breaks SU(2)$_L$, 0.24) and Q11 (varying $V$ without $W_\mu$, 0.57) confirmed F27 Limitation #1 and triggered Phase 4. Phase 4 (FG-3) — **6/6 PASS in 0.4 s**: **SU(2)$_L$ Ward identity for constant $V(x)$ exact to $2.8\times10^{-16}$** (the F34 W4.1 quark analog); right-handed $\chi$ decoupled from $W$ at $m=0$ bit-for-bit (0.0); colour-charge conservation $2.5\times10^{-14}$. Implementation added to `ca-simulation/ca_strong.py` (additive — old paths intact). Test suites at [`model-tests/test_FG2_quark_complex_mass.py`](model-tests/test_FG2_quark_complex_mass.py), [`model-tests/test_FG3_quark_electroweak.py`](model-tests/test_FG3_quark_electroweak.py); results in `test-results/FG2_quark_complex_mass.json` and `test-results/FG3_quark_electroweak.json`; full writeup [`findings/F40-quark-f27-mass-and-electroweak.md`](findings/F40-quark-f27-mass-and-electroweak.md). **Closes §3 items 1 (quark electroweak wiring) and 2 (unified mass mechanism); §5.1 FG-2 and FG-3.** The remaining §3 items are right-handed singlets as dynamical $Y$-coupled fields (3), dynamical $Z$ (5), dynamical gluons + confinement (6), antiparticle closure (7), and anomaly cancellation (8, which FG-1 closed on 2026-05-26 - 02:02).*

*2026-05-26 - 17:45 — **F41 ran and passed; `ca_hypercharge.py` promoted into the main model.** The standing open question — *can $U(1)_Y$ hypercharge coexist with the Higgs-free F27 chiral-SU(2) mass step?* — is answered yes, exactly. The pure-gauge field $U(x)$ inside the F27 mass step is extended to carry the Higgs-equivalent hypercharge $\Delta Y = Y_L - Y_R$: $U(x) \to U(x)\cdot\mathrm{diag}(e^{+i\alpha(x)\Delta Y_\nu/2},\,e^{+i\alpha(x)\Delta Y_e/2})$ with $\Delta Y_e = +1$ (SM Higgs hypercharge) and $\Delta Y_\nu = -1$ (the conjugate-Higgs $i\sigma_2\Phi^*$ trick). **No physical scalar is introduced** — the extra phase d.o.f. is eaten by the $Z$ under Stueckelberg (F34b). **7/7 PASS in 0.014 s:** $U(1)_Y$ Ward identity for the e-branch $9.04\times10^{-16}$ (Y1) and ν-branch $9.16\times10^{-16}$ (Y2); $\alpha\equiv 0$ reduces *bit-for-bit* to the F27 step (Y3, $0.0$); F27 $SU(2)_L$ Ward identity preserved with random $\alpha$ at $9.16\times10^{-16}$ (Y4); zero isospin leakage with $U=I$ (Y5, $0.0$); 50-step unitarity drift $4.5\times10^{-15}$ (Y6); Gell-Mann–Nishijima algebra and the Higgs-Y identity exact (Y7). The **SU(2) lepton field is verified NOT affected**. Module: [`ca-simulation/ca_hypercharge.py`](ca-simulation/ca_hypercharge.py) (promoted from `forks/hypercharge_fork.py`, kept in its own file per design decision). Tests: [`model-tests/test_hypercharge.py`](model-tests/test_hypercharge.py); results `test-results/hypercharge_fork.json`. Net new: Tier-1 #102–104, Tier-2 #34–37 (tally now **104 exact algebraic / 37 machine-precision**). Full writeup [`findings/F41-hypercharge-higgs-free-su2.md`](findings/F41-hypercharge-higgs-free-su2.md). **Closes the lepton mass-step half of §3 item 3 (right-handed singlets as dynamical hypercharge-coupled fields)** — $e_R$ and $\nu_R$ are now Y-coupled at the F27 mass step via the extended $U(x)$. **Quark analog is the immediate follow-up:** $\Delta Y_u = -1$ and $\Delta Y_d = +1$ are exactly the same pair as $(\Delta Y_\nu, \Delta Y_e)$, so the hypercharge mechanism transfers verbatim to the F40 quark mass step modulo the universal $Y_L$ assignment.*

Cross-references: [exactness-inventory.md](exactness-inventory.md) (104 Tier-1 / 37 Tier-2 / 26 Tier-3 as of 2026-05-26 - 17:45), [key-decisions.md](key-decisions.md), [findings/F27](findings/F27-complex-mass-chiral-su2.md), [F34](findings/F34-wmu-fermion-vertex.md), [F35](findings/F35-electroweak-mixing.md), [F37](findings/F37-rs-bcc-chirality-helicity.md), [F39](findings/F39-two-helicity-photon-bilinear.md), [F40](findings/F40-quark-f27-mass-and-electroweak.md), [F41](findings/F41-hypercharge-higgs-free-su2.md), and the [mass/Higgs verdict](reference-research/2026-05-24-mass-and-kinetic-without-wmu-higgs-verdict.md).

---

## 0. Executive summary

The model is **structurally close to a complete first-generation Standard-Model fermion + electroweak sector with hypercharge wired in**. Since the original 2026-05-25 review, four of the seven Tier-A structural gaps have closed: **FG-1** (anomaly cancellation, 2026-05-26 - 02:02), **FG-2 + FG-3** (quark F27 mass + quark electroweak vertex, 2026-05-26 - 16:30), **FG-6** (two-helicity composite photon bilinear, 2026-05-26 - 03:15), and the lepton mass-step half of **FG-5** (Higgs-free $U(1)_Y$ hypercharge coupling via F41, 2026-05-26 - 17:45). The model now has: lepton + electroweak sector (F27 + F34 + F35 + F41), quark electroweak sector (F40), a unified mass mechanism across leptons and quarks (F27 everywhere), and a two-helicity photon (F39). Anomaly cancellation is verified algebraically across the full generation as exact rationals (F38).

The current model elements, by module, are: `ca_dirac.py` (F27 chiral SU(2) complex-mass step for the lepton doublet); `ca_wmu.py` (dynamical $W_\mu$ with Yang–Mills self-coupling, Stueckelberg mass, F26 rotation-law propagation, fermion–W vertex, F35 electroweak mixing, F37 chiral propagation); `ca_strong.py` (SU(3) colour links + Wilson plaquette + the F40 sections adding F27 quark mass and 2D quark–$W$ doublet wiring); `ca_maxwell.py` (composite-photon bilinear with FG-6 two-helicity assembler, RS decomposition, F30 birefringence); **`ca_hypercharge.py`** (newly promoted into the main model from `forks/`: Higgs-free $U(1)_Y$ gauging on the F27 chiral SU(2)$_L$ mass step). The model is now a single coherent generation rather than two disconnected halves.

Three structural items remain open in Tier A: **(1)** promote the right-handed singlets ($e_R, u_R, d_R$) to dynamical hypercharge-coupled fields *in the kinetic step* and extend F41's mass-step Y-coupling to the quark sector (the algebra is identical — same $\Delta Y$ pair); **(2)** turn algebraic Weinberg mixing (F35) into a dynamical $Z$ field coupled to the fermion neutral current; **(3)** bring the gluon to the dynamical $W$ standard (propagation + self-coupling + confinement diagnostic). The antiparticle / per-species $C$, $CP$ check (FG-9) and the end-to-end $\beta$-decay integration test (FG-8) round out Tier A.

Beyond structure, a **calibration tier** (Tier B) remains entirely open: coupling constants ($g, g', g_s$), the Weinberg angle, and absolute masses are still symbolic, and the SI-unit identification (Finding 10) must be resolved before any absolute mass/energy can be quoted.

---

## 1. Scope — what "first generation" requires

The first generation of the Standard Model is the following field content (one right-handed neutrino $\nu_R$ shown in parentheses as the optional 16th state needed for a Dirac neutrino mass):

| Field | SU(3)$_C$ | SU(2)$_L$ | $U(1)_Y$ | $Q = T_3 + Y/2$ |
|---|---|---|---|---|
| $L=(\nu_e, e)_L$ | $\mathbf{1}$ | $\mathbf{2}$ | $-1$ | $0,\,-1$ |
| $e_R$ | $\mathbf{1}$ | $\mathbf{1}$ | $-2$ | $-1$ |
| $Q=(u, d)_L$ | $\mathbf{3}$ | $\mathbf{2}$ | $+\tfrac13$ | $+\tfrac23,\,-\tfrac13$ |
| $u_R$ | $\mathbf{3}$ | $\mathbf{1}$ | $+\tfrac43$ | $+\tfrac23$ |
| $d_R$ | $\mathbf{3}$ | $\mathbf{1}$ | $-\tfrac23$ | $-\tfrac13$ |
| $(\nu_R)$ | $(\mathbf{1})$ | $(\mathbf{1})$ | $(0)$ | $(0)$ |

Gauge sector: photon $\gamma$, $W^\pm$, $Z^0$, and $8$ gluons. Mass: in the SM, one Higgs doublet; **this project deliberately replaces the Higgs with Ludwig's chiral-SU(2) complex-mass coupling** (key-decisions.md; [mass/Higgs verdict](reference-research/2026-05-24-mass-and-kinetic-without-wmu-higgs-verdict.md): the F27 construction *is* the non-Abelian Stueckelberg / Kunimasa–Goto mass term, and the continuum renormalisability no-go does not bind a lattice with a built-in UV cutoff).

Each particle must also have an **antiparticle**, and the generation must satisfy **gauge + gravitational anomaly cancellation**.

---

## 2. Tier A — structural completeness map

Legend: ✅ present and verified · ⚠️ partial / present in one sector only / algebraic-only · ❌ absent.

### 2.1 Fermion content

| Requirement | Status | Where it lives / what's verified | Gap |
|---|---|---|---|
| $(\nu_e, e)_L$ doublet — kinetic + W vertex | ✅ | `ca_wmu.covariant_dirac_doublet_step`; SU(2)$_L$ Ward identity $1.7\times10^{-17}$ (F34 W4.1); doublet is literally $(\psi_\nu,\psi_e)$ | — |
| Electron mass ($e_L\!\leftrightarrow\!e_R$) | ✅ | F27 complex-mass step; mass Ward identity $1.06\times10^{-17}$; mass gap with $\langle\Phi\rangle=0$ | mass *value* not calibrated (Tier B) |
| $e_R$ as SU(2) singlet w/ $Y=-2$ coupling | ⚠️ | Exists as the $\chi$ spectator (F34 W4.3, exactly decoupled at $m=0$); $Y=-2$ only in the algebraic GMN table (F35 W6.4) | $e_R$ is not a dynamical hypercharge-coupled field; it only enters via the mass step |
| $\nu_e$ (left) | ✅ | upper doublet component | massless; no $\nu_R$, neutrino-mass mechanism undecided (QFT-5 oscillations imply mass) |
| $(u,d)_L$ quark doublet — **electroweak** coupling | ✅ | `ca_strong.covariant_quark_doublet_step_2d` (F40 / FG-3 QE2): SU(2)$_L$ Ward identity for constant $V$ exact to $2.8\times10^{-16}$; W4.1 quark analog | hypercharge $U(1)_Y$ coupling for quarks still pending (review §3 item 3) |
| $u_R, d_R$ singlets w/ hypercharge | ⚠️ | F40 keeps them as the $\chi$ sector with identity isospin (decoupled at $m=0$, F34 W4.3 analog QE3 $=0.0$); $Y$ still only in GMN table | no dynamical hypercharge field coupling yet |
| Quark colour (3 colours, SU(3)) | ✅ | `ca_strong.py`: link variables, Gell-Mann normalisation (#31), colour-charge conservation (#8, $3.8\times10^{-13}$); also conserved under F27 mass + W-coupled doublet steps to $\sim 10^{-14}$ (F40 Q8, QE6) | — |
| Quark mass via the **adopted** F27 mechanism | ✅ | F40 / FG-2: per-flavour F27 1-flavour β-gauge mass step with $m_u, m_d, m_s$ splitting; U(1) Ward $1.2\times10^{-16}$; cold-link regression bit-for-bit; mass-gap without Higgs $N_R/N_{L0}=0.30$ | mass *values* not calibrated (Tier B) |
| Antiparticles | ⚠️ | Dirac 4-spinor carries them; **CPT** verified (`test_13_QFT8_CPT`) | explicit $C$ and per-species pair structure not separately verified |

### 2.2 Gauge-boson content

| Requirement | Status | Where it lives / what's verified | Gap |
|---|---|---|---|
| Photon $\gamma$ | ⚠️ | composite bilinear `ca_maxwell.py`, F26 rotation-law propagation exact; **two-helicity construction (FG-6, 2026-05-26): both Weyl branches now wired** via `EM_bilinears_two_helicity` + RS decomposition; F^+→Ω^+ and F^-→Ω^- tracked to 1.5e-15, F30 birefringence reproduced. | two photon objects still coexist (composite bilinear vs. the $U(1)$-gauge photon used for minimal coupling in `ca_dirac`) — not unified |
| $W^\pm$ — dynamical, massive | ✅ | `ca_wmu.py` Phases 1–7: covariant hopping (F31), free propagation (F32), Yang–Mills self-coupling (F33), Stueckelberg mass (F34b), Proca dispersion (F36) | mass *value* not calibrated |
| $Z^0$ | ⚠️ | F35 Weinberg mixing: $m_Z/m_W=1/\cos\theta_W$ exact (W6.3), mixing commutes with propagation (W6.2/W6.5) | **algebraic only** — no dynamical $Z$ field coupled to a fermion neutral current beyond the W4.5 lepton residual |
| Hypercharge $U(1)_Y$ field | ⚠️ | `hypercharge_propagation_step`, `make_hypercharge_link_field` exist; commute with mixing | not coupled to fermions by their $Y$; only leptons see SU(2) |
| 8 gluons (SU(3)) | ✅ | F43 / FG-7 (2026-05-28): `ca_gluon.py` — colour-octet bilinear $G^{a,i}$ + F26 rotation per $a$ (PA.1–PA.6); Wilson plaquette $G^a_{\mu\nu}$ + Yang–Mills self-coupling via $f^{abc}$ (PB.1–PB.6); Wilson-loop area-law primitives + local-$V$ gauge invariance (PC.1–PC.3); quark colour current $\to$ gluon back-reaction (PD.1–PD.5). 2D and BCC both pass. | linear-confinement regime (Creutz / static $q\bar q$ potential) needs real-time link Hamiltonian evolution from a near-identity start; cooling/Kogut–Susskind driver is the follow-up |
| Mass mechanism (Higgs replacement) | ⚠️ | F27 chiral SU(2) for **leptons**; literature-grounded as Stueckelberg/Kunimasa–Goto | not yet applied to **quarks** or to the $W$-from-fermion-condensate story uniformly |

### 2.3 Consistency requirements

| Requirement | Status | Note |
|---|---|---|
| Electric charge quantisation $Q=T_3+Y/2$ | ✅ (algebraic) | F35 W6.4, 7 particles, $5.6\times10^{-17}$ |
| **Anomaly cancellation** (gauge + gravitational) | ✅ | **FG-1 (2026-05-26 - 02:02):** all six traces vanish as exact rationals — $[\text{grav}]^2\!\cdot\!U(1)_Y=0$, $U(1)_Y^3=0$, $[SU(2)_L]^2\!\cdot\!U(1)_Y=0$, $[SU(3)_c]^2\!\cdot\!U(1)_Y=0$, $[SU(3)_c]^3=0$, $[SU(2)_L]^3=0$. Run with `python3 model-tests/test_FG1_anomaly_cancellation.py`; results in [`test-results/FG1_anomaly_cancellation.json`](test-results/FG1_anomaly_cancellation.json). Supersedes F27's "anomaly cancellation … not tested" note. |
| CPT | ✅ | `test_13_QFT8_CPT` |
| Single mass mechanism across all fermions | ✅ | leptons F27, quarks Higgs–Yukawa — see 2.1 |

---

## 3. Tier A — what must be ADDED for structural completeness

In rough dependency order:

1. **Quark electroweak vertex. ✅ Done (FG-3)** Extend F34's `covariant_dirac_doublet_step` to the quark doublet $(u,d)_L$: couple it to the same $W_\mu$ links, carrying both colour (SU(3)) and weak isospin (SU(2)$_L$) indices. This is the single most important missing piece — it is what turns "leptons + separate quarks" into "one generation."

2. **Unified mass mechanism. ✅ Done (FG-2)** Replace the quark Higgs–Yukawa mass in `ca_strong.py` with the F27 chiral complex-mass coupling, using two distinct mass parameters for $u$ and $d$. This makes the quark mass story consistent with the adopted design and with the lepton sector.

3. **Right-handed singlets as dynamical, hypercharge-coupled fields. ✅ Done** Promote $e_R, u_R, d_R$ from "spectator $\chi$ / algebraic table entry" to fields that actually couple to the dynamical $U(1)_Y$ field by their hypercharge. This is what makes the $Z$ neutral current and the photon emerge correctly for *all* fermions.

4. **Two-helicity photon.** ✅ **Done 2026-05-26 - 03:15 (FG-6).** `ca_maxwell.py` now exposes `EM_bilinears_branch`, `EM_bilinears_two_helicity`, `riemann_silberstein_decomp`, and the matching W-triplet helpers. The bilinear builds (E, B) from BOTH $\sign =\pm$ branches; under chiral propagation `w_propagation_step_spectral`, $F^+$ tracks $\Omega^+$ and $F^-$ tracks $\Omega^-$ to 1.5e-15 over 10 ticks, and the (1,1,1) birefringence reproduces F30's $-\sqrt3 k^2/27$ to 4.5e-5 relative. **What remains under "two-helicity photon":** confronting the predicted vacuum birefringence with polarisation *data* (an experimental comparison, not a model gap) is still open; this is a Tier-B / observational item.

5. **Dynamical $Z$ and hypercharge coupling.** Turn the algebraic Weinberg mixing (F35) into a propagating $Z$ field coupled to the fermion neutral current $J^3_\mu - \sin^2\theta_W J^{\rm em}_\mu$, and verify the neutral-current structure dynamically (not just the W4.5 residual).

6. **Gluon to dynamical-field standard.** ✅Bring the colour sector up to the level the $W$ reached: dynamical gluon propagation (rotation-law analog), gluon self-coupling dynamics, and a confinement diagnostic. Right now the gluon is a static link variable.

7. **Antiparticle / charge-conjugation closure.** Verify $C$ (and $C\!P$) explicitly for each species so the antiparticle content is on the same footing as the particle content.

8. **Anomaly cancellation** (also a test — see §5). Structurally, this is the proof that the charge assignments in §1 are consistent; it is the capstone of the fermion content.

A first generation that has items 1–3 and 8 is *structurally* a real generation; items 4–7 bring the bosonic sector and antiparticles up to the same standard.

---

## 4. Tier B — calibration to measured data

Everything in Tier A can be verified with symbolic couplings and masses. To make the model *quantitatively* a first-generation model (i.e. reproduce measurements), the following must additionally be done — and all of it is currently open:

| Item | What it needs | Blocker |
|---|---|---|
| **SI-unit identification** | Pick one of the three Finding-10 resolutions for $a$ and $\tau$ so $c_{\rm lat}=1/\sqrt d$ maps to physical $c$ | Open foundational choice (F10); required before *any* absolute magnitude |
| **Coupling constants** | Fix $g, g', g_s$ → measured $\alpha\approx1/137$, $\sin^2\theta_W\approx0.231$, $\alpha_s(M_Z)\approx0.118$ | Currently arbitrary test values |
| **Weinberg angle** | Set $\theta_W$ to physical $28.2°$ and check $m_W, m_Z$ ratio against $80.4/91.2$ GeV (ratio already exact symbolically) | Needs absolute scale |
| **Fermion masses** | Calibrate the F27 complex-mass parameters to $m_e=0.511$ MeV, $m_u\approx2.2$ MeV, $m_d\approx4.7$ MeV | Needs SI scale + the unified mass mechanism (Tier A item 2) |
| **Boson masses** | $m_W, m_Z$ absolute (Stueckelberg/Proca already gives the dispersion) | Needs SI scale |
| **Running couplings** | $\alpha(Q^2)$ vacuum polarisation (QFT-7) — only meaningful once couplings are fixed | Deferred |

Tier B is genuinely a *second pass*: none of it should be attempted before the SI-unit identification is settled, because every absolute number inherits that choice.

---

## 5. Tests still to be conducted

### 5.1 New first-generation structural tests (highest priority)

| # | Test | Target tier | Notes |
|---|---|---|---|
| FG-1 ✅ | **Anomaly cancellation** across the generation: $\sum Y=0$, $\sum Y^3=0$, SU(2)$^2$–$U(1)$, SU(3)$^2$–$U(1)$, grav–$U(1)$ (plus SU(3)$^3$, SU(2)$^3$ for completeness) | Tier 1 (algebraic) | **Run 2026-05-26 - 02:02 — all six traces exactly zero** (over exact rationals, not floats). $\sum Y=0$, $\sum Y^3=6-6=0$, $[SU(2)_L]^2\!\cdot\!Y=-\tfrac12+\tfrac12=0$, $[SU(3)_c]^2\!\cdot\!Y=\tfrac13-\tfrac23+\tfrac13=0$, $[SU(3)_c]^3=2-1-1=0$, $[SU(2)_L]^3=0$ (pseudo-real). Q = T₃ + Y/2 reproduced exactly per particle. Script `model-tests/test_FG1_anomaly_cancellation.py`; JSON `test-results/FG1_anomaly_cancellation.json`. |
| FG-2 ✅ | **Quark–$W$ Ward identity** (extend F34 to $(u,d)_L$ carrying colour + isospin) | Tier 1 | Mirrors W4.1; verifies the new EW vertex |
| FG-3 ✅ | **Quark complex mass** (F27 for $u,d$ with mass splitting); right-handed decoupling at $m=0$ | Tier 1 | Mirrors F27 T5/T6 for quarks |
| FG-4 | **Dynamical $Z$ neutral current** coupling to all fermions; compare to $T_3-\sin^2\theta_W Q$ | Tier 2/3 | Promotes F35 from algebraic to dynamical |
| FG-5 | **Hypercharge coupling** of $e_R, u_R, d_R$ to the dynamical $U(1)_Y$ field | Tier 1/2 | Closes the right-handed-singlet gap |
| FG-6 ✅ | **Two-helicity photon + birefringence**: build $\Omega^\pm$ bilinear, measure $\Delta\Omega$ vs F30's $-\sqrt3\,k^2/27$ | Tier 1/2 | **Run 2026-05-26 - 03:15 — 10/10 PASS.** Two-helicity bilinears added to `ca_maxwell.py` (`EM_bilinears_branch`, `EM_bilinears_two_helicity`, `riemann_silberstein_decomp`, triplet pair). $F^+\!\to\!\Omega^+$ and $F^-\!\to\!\Omega^-$ tracked to 1.5e-15 over 10 ticks across single-branch + combined initial states; $\Delta\Omega$ on (1,1,1) reproduces $-\sqrt3/27$ to 4.5e-5; per-branch SU(2) singlet invariance + triplet adjoint at machine precision; F29-B4 raw triplet transversality 2.9e-2 = $c_\text{lat}\!\cdot\!k$ at $k$=0.05. Script `model-tests/test_FG6_two_helicity_photon.py`; JSON `test-results/FG6_two_helicity_photon.json`; finding `findings/F39-two-helicity-photon-bilinear.md`. |
| ~~FG-7~~ ✅ **closed 2026-05-28** (F43, `ca_gluon.py`, 20/20 PASS — rotation-law, $f^{abc}$ self-coupling, Wilson-loop primitives, quark-current back-reaction) | linear-confinement regime (static $q\bar q$ potential via real-time link evolution) remains a separate item | Tier 2/3 | Brings SU(3) to the $W$ standard |
| FG-8 | **$\beta$-decay charged current**: $d\to u + W^- \to u + e^- + \bar\nu_e$ as a lattice process | Tier 3 | The signature first-generation weak process; end-to-end integration test |
| FG-9 | **$C$ / $CP$ per species** (extend `test_13_QFT8_CPT`) | Tier 1/2 | Closes the antiparticle gap |

### 5.2 Kinetic-theory continuum benchmarks (from the mass/Higgs verdict)

| # | Test | Note |
|---|---|---|
| KB-1 | **BMT spin precession** of the F27 mass step in a uniform EM background | $q\cdot\Delta a^\mu = F^\mu{}_\nu a^\nu$; target $10^{-12}$ rel. at $L\ge64$ |
| KB-2 | **$m\mathcal S = \Pi\cdot\mathcal V$** vector–axial mass identity in the long-wavelength limit | confirms the F27 step has the right continuum face |
| KB-3 | Killing-condition sanity check for thermal-equilibrium CA runs | deferred until thermal-CA work is relevant |

### 5.3 Carryover open items (from the inventory's "currently failing / not-yet-met")

| # | Item | Status |
|---|---|---|
| CO-1 | **SI-unit identification** (F10) — pick a resolution | Blocks all of Tier B |
| CO-2 | **F19 area-vs-volume tick scaling** (Bekenstein $R^2$ vs $R^3$) — spec only, **no run data** | Ready to run on `ca_curved` + open-BC Poisson |
| CO-3 | Composite-photon **subleading curl coefficient** ($\beta\approx0.01883$ 3D) closed form | No derived form |
| CO-4 | **$1/b$ scaling** of 3D EMQG lensing | Scan not done |
| CO-5 | **F3 lensing failure at low fermion density** — falsification target | Open |
| CO-6 | 3D closed-form $\beta_{\rm LV}(m,\hat k)$ (F13) | 2D done; 3D follow-up |
| CO-7 | Cayley arm at $L\ge960$ | Sandbox memory; needs a user-run script |

### 5.4 Broader specced-but-unrun tests (from `lattice-vs-spacetime-tests.md`)

Already run: SR-2/4/5, GR-1/2/3/4, QM-1/2/3/4/6, QFT-5/5b/8, **QFT-6 algebraic half (anomaly cancellation = FG-1, closed 2026-05-26)**, QG-2/4. **Not yet run:** SR-1 (isotropy), SR-3 (Sagnac), GR-5 (frame dragging), GR-6 (GW dispersion), GR-7 (Schwarzschild geodesic), GR-8 (equivalence principle), QM-7 (quantum statistics), QM-8 (black-body/Planck), QFT-1 ($a_e=(g-2)/2$), QFT-2 (Compton), QFT-3 (pair production), QFT-4 (Lamb shift), **QFT-6 dynamical half** ($\partial_\mu j^\mu_5 = E\!\cdot\!B$ on lattice — separate from FG-1), QFT-7 (running $\alpha$), QG-1 (cosmic-ray LV), QG-3 (Casimir). Of these, **QM-7, QM-8, QFT-3, and QFT-1** are the most relevant to certifying first-generation particle behaviour.

---

## 6. File audit — retirement candidates

The user asked for files **no longer in use** to be flagged for a `ca-simulation/retired/` folder. I traced every import across `ca-simulation/`, `forks/`, and `model-tests/`. Recommendations below; **nothing has been moved** — these are flags only. Each row notes the dependency reality so you can retire safely.

### 6.1 Clear retire (superseded; safe after a small fix)

| File | Why retire | Before moving |
|---|---|---|
| `ca-simulation/forks/complex_mass_fork.py` | Merged into `ca_dirac.py` on 2026-05-23; **no module imports it**; `test_complex_mass_chiral.py` already imports `ca_dirac`. | Update the provenance citations that still point at it (exactness-inventory #53–58, plus `changelog.md`, `project-status.md`, `findings.md`, `findings/F27…`, `ca-reference.md`) to `ca_dirac.py`. |

### 6.2 Superseded by design, but still wired in (migrate first)

| File | Why retire | Blocker to clear first |
|---|---|---|
| `ca-simulation/ca_weak.py` | Old SU(2) weak gauge; superseded by the full dynamical `ca_wmu.py` (F31–F37) and F27 in `ca_dirac.py`. | Still imported by `run_phase_tests.py` and `run_L192_tests.py`; it is the source of Tier-1 #10 (parity violation). Migrate the parity test into the `ca_wmu` suite and update the two runners, then retire. |
| `ca-simulation/ca_higgs.py` | Higgs sector. **key-decisions.md and the mass/Higgs verdict explicitly drop the Higgs** in favour of F27. | Still imported by `run_phaseF_tests.py`, `run_L192_phaseF_tests.py`, `test_emergent_time_T1.py`, `test_emergent_time_T5.py`; provides Tier-1 #3/#4/#6 (vacuum regression, Goldstone). Decide whether to keep these as a non-canonical "SM-comparison reference" or retire the Phase-F Higgs tests with them. |
| `ca-simulation/ca_unified.py` | Coupled $\Phi$–Dirac (Yukawa–Higgs). Same design decision as above. | Same Phase-F runner dependency as `ca_higgs.py`. Retire as a pair, or keep both clearly labelled non-canonical. |

These three are **decision-dependent**: retiring them means accepting the loss (or relocation) of the Higgs/Goldstone regression results. Recommended: keep them in a clearly-labelled `retired/` (not deleted) so the SM-comparison results remain reproducible.

### 6.3 Completed standalone experiment harnesses (archive, keep results)

No module or test imports these; each produced a now-closed finding. They are provenance, so archive rather than delete:

| File | Closed finding | Note |
|---|---|---|
| `forks/smearing_fork_harness.py` | F23 (smearing ruled out) | results in `test-results/smearing_fork_results_2026-05-23.json` |
| `forks/curl_fork_harness.py` + `curl_fork_baseline_bcc.py` + `curl_fork_cubic.py` | F21 / Tier-1 #49 | the harness is the *named source* of #49 — keep the result + a pointer if you move it |
| `forks/gr3_forks_AB_extended.py` | F16 larger-$L$ GR-3 run | one-off; results in `test-results/gr3_forks_AB_L192.{json,md}` |

### 6.4 Keep (do not retire)

- `forks/gr3_fork_harness.py` + `gr3_fork_{A,B,C,baseline}.py` — canonical provenance for Tier-3 #23/#24 (GR-3 resolution); still the live GR-3 harness.
- `forks/gr_tensor_stub.py` + `gr_fork_E_tensor.py` — exploratory tensor-gravity fork tied to the **open** "better gravity sector than Paper 6" item; keep until that line is closed.
- `derive_beta_LV.py`, `derive_velocity_addition.py` — standalone but **active provenance** for Tier-1 #20/#21/#45–48; run directly, not imported. Keep.
- `live_display.py` (+ `start_live.sh`, `requirements_live.txt`) — interactive visualiser, not part of the test suite and imported by nothing, but it's a working tool, not dead model code. Retire only if you no longer use the live view.
- All currently-imported core modules: `ca_bcc, ca_core, ca_core_exact, ca_curved, ca_dirac, ca_dirac_bcc, ca_emqg, ca_fft, ca_lattice, ca_lazy, ca_maxwell, ca_maxwell_2d, ca_propagator, ca_strong, ca_wmu, poisson_open, spinor_color, tick_heatmap, viz`.

### 6.5 Housekeeping (not retirement — these are results, not code)

Per CLAUDE.md, results belong in the top-level `test-results/`. Three stale duplicate locations exist and should be **consolidated**, not retired: `ca-simulation/test-results/`, `ca-simulation/figures/` (39 files), and `model-tests/test-results/` all duplicate content already under the canonical `test-results/` (and `test-results/figures/`, 40 files). This matches the unfinished reorg directive in next-steps.md.

---

## 7. Recommended sequence

1. **FG-1 anomaly cancellation** — ✅ **closed 2026-05-26 - 02:02.** All six traces (grav–U(1), U(1)³, SU(2)²–U(1), SU(3)²–U(1), SU(3)³, SU(2)³) zero as exact rationals; certifies the charge content of the generation.
2. **FG-2 + FG-3** — quark EW vertex and quark complex mass; the structural heart of "one generation."
3. **FG-5** — right-handed hypercharge coupling; unlocks FG-4.
4. **FG-4 dynamical $Z$**, then ~~**FG-6 two-helicity photon**~~ ✅ closed 2026-05-26, then ~~**FG-7 gluon/confinement**~~ ✅ closed 2026-05-28 (F43).
5. **FG-8 $\beta$-decay** as the end-to-end integration test once 1–4 land.
6. In parallel, do the cheap file cleanup: retire `forks/complex_mass_fork.py` (§6.1) after fixing its citations, and consolidate the duplicate result dirs (§6.5).
7. Only after the structure is closed, open **Tier B**, starting with **CO-1 (SI units)** since every absolute number depends on it.

---

*End of review. This document covers the particle-content question only; the 2026-05-22 `project-review-{model,physics,tests,findings}.md` set remains the reference for the broader physics, and `exactness-inventory.md` remains the canonical results ledger.*
