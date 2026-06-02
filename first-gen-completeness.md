# First-Generation Particle Model — Completeness Review

*2026-05-25 - 14:00 — Rigorous review of the BCC lattice-CA model against the requirements for a complete first-generation Standard-Model particle sector. Determines what is present, what must be added, outlines the tests still to run, and flags code no longer in use. Supersedes the 2026-05-22 `project-review-*.md` set for the particle-content question only; those remain valid for the broader physics/test summary.*

*2026-05-26 - 02:02 — **FG-1 ran and passed exactly.** All six anomaly traces over the first-generation chiral content vanish as exact rationals (not "to machine precision" — to **0/1**). Results in [`test-results/FG1_anomaly_cancellation.json`](test-results/FG1_anomaly_cancellation.json); test script at [`model-tests/test_FG1_anomaly_cancellation.py`](model-tests/test_FG1_anomaly_cancellation.py). Rows updated below: §2.3 anomaly row promoted to ✅; §5.1 FG-1 row shows the run result; §7 sequencing item 1 closed.*

*2026-05-26 - 03:15 — **FG-6 ran and passed.** Extended `ca_maxwell.py` to construct a two-helicity composite photon from BOTH BCC chirality branches (sign='+' and sign='-'); new helpers `EM_bilinears_branch`, `EM_bilinears_two_helicity`, `riemann_silberstein_decomp`, plus the matching W-triplet pair `triplet_bilinear_branch` / `triplet_bilinear_two_helicity`. Test suite `model-tests/test_FG6_two_helicity_photon.py` runs 10 tests (all PASS, 0.30 s total): per-branch singlet SU(2) invariance (3.4e-16), per-branch triplet adjoint rotation (2.6e-16), assembler linearity (0.0), Riemann-Silberstein E=(F^++F^-)/2 identity (0.0), chiral propagation F^+→Ω^+ and F^-→Ω^- per-helicity tracking (1.5e-15 over 10 ticks across 12 cases), F30 birefringence coefficient $-\sqrt3/27$ along (1,1,1) (4.5e-5 relative), and the F29-B4 raw triplet transversality scaling (2.9e-2 at k=0.05, matching c_lat·|k| = 0.0289). Results in [`test-results/FG6_two_helicity_photon.json`](test-results/FG6_two_helicity_photon.json); full write-up in [`findings/F39-two-helicity-photon-bilinear.md`](findings/F39-two-helicity-photon-bilinear.md). Closes §3 item 4 (two-helicity photon) and §5.1 FG-6.*

*2026-05-26 - 16:30 — **FG-2 and FG-3 ran and passed (Finding F40).** Two of the three structural gaps closed: (a) the quark sector now uses the project's adopted **F27 chiral-SU(2) complex-mass mechanism** (no Higgs), per flavour, per colour, with natural up/down/strange mass splitting; (b) the quark doublet $(u,d)_L$ is now **wired to a dynamical $W_\mu$ link field** via a 2D-square analog of F31/F34. Phase 1 (FG-2) — **11/11 PASS in 2.0 s**: per-flavour U(1) Ward identity $1.2\times10^{-16}$; degenerate-doublet SU(2)$_L$ Ward identity $8.4\times10^{-17}$; cold-link θ=0 regression bit-for-bit (0.0); mass splitting $r_d/r_u=3.96$ (exp 4), $r_s/r_u=15.22$ (exp 16); colour-charge conservation $1.7\times10^{-14}$. Diagnostics Q10 (split mass breaks SU(2)$_L$, 0.24) and Q11 (varying $V$ without $W_\mu$, 0.57) confirmed F27 Limitation #1 and triggered Phase 4. Phase 4 (FG-3) — **6/6 PASS in 0.4 s**: **SU(2)$_L$ Ward identity for constant $V(x)$ exact to $2.8\times10^{-16}$** (the F34 W4.1 quark analog); right-handed $\chi$ decoupled from $W$ at $m=0$ bit-for-bit (0.0); colour-charge conservation $2.5\times10^{-14}$. Implementation added to `ca-simulation/ca_strong.py` (additive — old paths intact). Test suites at [`model-tests/test_FG2_quark_complex_mass.py`](model-tests/test_FG2_quark_complex_mass.py), [`model-tests/test_FG3_quark_electroweak.py`](model-tests/test_FG3_quark_electroweak.py); results in `test-results/FG2_quark_complex_mass.json` and `test-results/FG3_quark_electroweak.json`; full writeup [`findings/F40-quark-f27-mass-and-electroweak.md`](findings/F40-quark-f27-mass-and-electroweak.md). **Closes §3 items 1 (quark electroweak wiring) and 2 (unified mass mechanism); §5.1 FG-2 and FG-3.** The remaining §3 items are right-handed singlets as dynamical $Y$-coupled fields (3), dynamical $Z$ (5), dynamical gluons + confinement (6), antiparticle closure (7), and anomaly cancellation (8, which FG-1 closed on 2026-05-26 - 02:02).*

*2026-05-26 - 17:45 — **F41 ran and passed; `ca_hypercharge.py` promoted into the main model.** The standing open question — *can $U(1)_Y$ hypercharge coexist with the Higgs-free F27 chiral-SU(2) mass step?* — is answered yes, exactly. The pure-gauge field $U(x)$ inside the F27 mass step is extended to carry the Higgs-equivalent hypercharge $\Delta Y = Y_L - Y_R$: $U(x) \to U(x)\cdot\mathrm{diag}(e^{+i\alpha(x)\Delta Y_\nu/2},\,e^{+i\alpha(x)\Delta Y_e/2})$ with $\Delta Y_e = +1$ (SM Higgs hypercharge) and $\Delta Y_\nu = -1$ (the conjugate-Higgs $i\sigma_2\Phi^*$ trick). **No physical scalar is introduced** — the extra phase d.o.f. is eaten by the $Z$ under Stueckelberg (F34b). **7/7 PASS in 0.014 s:** $U(1)_Y$ Ward identity for the e-branch $9.04\times10^{-16}$ (Y1) and ν-branch $9.16\times10^{-16}$ (Y2); $\alpha\equiv 0$ reduces *bit-for-bit* to the F27 step (Y3, $0.0$); F27 $SU(2)_L$ Ward identity preserved with random $\alpha$ at $9.16\times10^{-16}$ (Y4); zero isospin leakage with $U=I$ (Y5, $0.0$); 50-step unitarity drift $4.5\times10^{-15}$ (Y6); Gell-Mann–Nishijima algebra and the Higgs-Y identity exact (Y7). The **SU(2) lepton field is verified NOT affected**. Module: [`ca-simulation/ca_hypercharge.py`](ca-simulation/ca_hypercharge.py) (promoted from `forks/hypercharge_fork.py`, kept in its own file per design decision). Tests: [`model-tests/test_hypercharge.py`](model-tests/test_hypercharge.py); results `test-results/hypercharge_fork.json`. Net new: Tier-1 #102–104, Tier-2 #34–37 (tally now **104 exact algebraic / 37 machine-precision**). Full writeup [`findings/F41-hypercharge-higgs-free-su2.md`](findings/F41-hypercharge-higgs-free-su2.md). **Closes the lepton mass-step half of §3 item 3 (right-handed singlets as dynamical hypercharge-coupled fields)** — $e_R$ and $\nu_R$ are now Y-coupled at the F27 mass step via the extended $U(x)$. **Quark analog is the immediate follow-up:** $\Delta Y_u = -1$ and $\Delta Y_d = +1$ are exactly the same pair as $(\Delta Y_\nu, \Delta Y_e)$, so the hypercharge mechanism transfers verbatim to the F40 quark mass step modulo the universal $Y_L$ assignment.*

*2026-05-29 - 03:45 — **FG-5 closed (F42) and the Weinberg angle is now derived, not assumed (F45, F49).** Two updates fold in work that post-dates the FG-4/FG-7 pass but had not yet been reflected in the status tables below. **(1) FG-5 — right-handed singlets are now dynamical hypercharge-coupled fields, and the quark sector carries $U(1)_Y$.** F42 ([`findings/F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md`](findings/F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md)) extends F41's Higgs-free $U(1)_Y$ to the quark mass step ($\Delta Y_u=-1$, $\Delta Y_d=+1$, verbatim the lepton pair) AND promotes $e_R, u_R, d_R$ from passive $\chi$ spectators to genuinely $Y$-coupled fields via a Stueckelberg wrap of the spectral kinetic half-step. **8/8 PASS** (Y8–Y15) at machine ε: quark $U(1)_Y$ Ward identities $\sim 9\times10^{-16}$ (Y8/Y9), $\chi$ kinetic gauge-covariance for all three singlets $1.78\times10^{-15}$ (Y13), $\alpha\equiv0$ bit-for-bit reductions $0.0$ (Y10/Y14), quark GMN algebra $5.55\times10^{-17}$ (Y15). Module `ca-simulation/ca_hypercharge.py` (F42 block; F41 surface intact). **This closes §3 item 3 in full and §5.1 FG-5.** **(2) Weinberg angle — bare value derived from BCC structure.** F45 ([`findings/F45-sigma-tau-swap-weinberg-angle.md`](findings/F45-sigma-tau-swap-weinberg-angle.md)) derives $\sin^2\theta_W=1/4$ ($g'^2/g^2=1/3$, $m_Z/m_W=2/\sqrt3$) from the σ↔τ swap representation count (1 swap-singlet : 3 swap-triplet directions); the mass ratio lands within 1.77% of PDG with **zero fit parameters**. F49 ([`findings/F49-bcc-finite-k-weinberg-angle.md`](findings/F49-bcc-finite-k-weinberg-angle.md)) derives $\sin^2\theta_W=2/9$ from BCC bond-axis/sublattice counting (2 sublattices : 7 second-shell bond axes), matching PDG to **0.44%** as an exact rational — though the sublattice↔$Y$ assignment is not yet derived from first principles. F35's $\theta_W$ moves from a free input to a structure-derived prediction. Tables in §2.1, §2.2, §3, §4, §5.1, §7 updated below.*

Cross-references: [exactness-inventory.md](exactness-inventory.md) (138 Tier-1 / 51 Tier-2 / 26 Tier-3 as of 2026-05-28 - 14:00), [key-decisions.md](key-decisions.md), [findings/F27](findings/F27-complex-mass-chiral-su2.md), [F34](findings/F34-wmu-fermion-vertex.md), [F35](findings/F35-electroweak-mixing.md), [F37](findings/F37-rs-bcc-chirality-helicity.md), [F39](findings/F39-two-helicity-photon-bilinear.md), [F40](findings/F40-quark-f27-mass-and-electroweak.md), [F41](findings/F41-hypercharge-higgs-free-su2.md), [F42](findings/F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md), [F45](findings/F45-sigma-tau-swap-weinberg-angle.md), [F48](findings/F48-dynamical-Z-neutral-current.md), [F49](findings/F49-bcc-finite-k-weinberg-angle.md), and the [mass/Higgs verdict](reference-research/2026-05-24-mass-and-kinetic-without-wmu-higgs-verdict.md).

---

## 0. Executive summary

The model is now **structurally a complete first-generation Standard-Model fermion + electroweak sector, Higgs-free, with hypercharge wired across both leptons and quarks and a dynamical $Z$**. Since the original 2026-05-25 review, six of the seven Tier-A structural gaps have closed: **FG-1** (anomaly cancellation, 2026-05-26 - 02:02), **FG-2 + FG-3** (quark F27 mass + quark electroweak vertex, 2026-05-26 - 16:30), **FG-6** (two-helicity composite photon bilinear, 2026-05-26 - 03:15), **FG-5** (Higgs-free $U(1)_Y$ on leptons via F41 then quarks + dynamical right-handed singlets via F42, completed 2026-05-27 - 09:00), **FG-4** (dynamical $Z$ neutral current via F48, 2026-05-28 - 23:30), and **FG-7** (dynamical SU(3) gluon sector via F43, 2026-05-28). The model now has: lepton + electroweak sector (F27 + F34 + F35 + F41), quark electroweak sector (F40), $U(1)_Y$ on every fermion including the right-handed singlets as dynamical $Y$-coupled fields (F41 + F42), a unified mass mechanism across leptons and quarks (F27 everywhere), a two-helicity photon (F39), a dynamical $Z$ (F48), and a dynamical gluon sector (F43). Anomaly cancellation is verified algebraically across the full generation as exact rationals (F38). The **Weinberg angle is now derived rather than assumed**: F45 gives the bare $\sin^2\theta_W = 1/4$ from the σ↔τ swap count, and F49 gives $\sin^2\theta_W = 2/9$ (0.44% from PDG) from BCC bond-axis/sublattice counting.

The current model elements, by module, are: `ca_dirac.py` (F27 chiral SU(2) complex-mass step for the lepton doublet); `ca_wmu.py` (dynamical $W_\mu$ with Yang–Mills self-coupling, Stueckelberg mass, F26 rotation-law propagation, fermion–W vertex, F35 electroweak mixing, F37 chiral propagation); `ca_strong.py` (SU(3) colour links + Wilson plaquette + the F40 sections adding F27 quark mass and 2D quark–$W$ doublet wiring); `ca_maxwell.py` (composite-photon bilinear with FG-6 two-helicity assembler, RS decomposition, F30 birefringence); **`ca_hypercharge.py`** (newly promoted into the main model from `forks/`: Higgs-free $U(1)_Y$ gauging on the F27 chiral SU(2)$_L$ mass step). The model is now a single coherent generation rather than two disconnected halves.

Both remaining Tier-A items are now closed: the antiparticle / per-species $C$, $CP$ check (**FG-9**, F53, 2026-05-29 - 21:10, 6/6 PASS) and the end-to-end $\beta$-decay charged-current integration test (**FG-8**, F54, 2026-05-29 - 20:48, 10/10 PASS). **Every §5.1 Tier-A structural test is now complete** — the first generation is structurally closed as an integrated lattice model, with only Tier-B calibration (CO-1 SI units, couplings, masses) outstanding. Within the closed items, one residual refinement is noted: the gluon's **linear-confinement regime** (static $q\bar q$ potential via real-time link evolution) is a follow-up to FG-7, separate from the dynamical-field machinery that FG-7 delivered.

Beyond structure, a **calibration tier** (Tier B) remains largely open: the coupling *magnitudes* ($g, g', g_s$) and absolute masses are still symbolic, and the SI-unit identification (Finding 10) must be resolved before any absolute mass/energy can be quoted. The Weinberg angle is the one Tier-B item that has moved: its *ratio* $g'^2/g^2$ is now derived at tree level (F45: $1/4$; F49: $2/9$), leaving only the overall normalisation and any RG running to the measured value.

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
| $e_R$ as SU(2) singlet w/ $Y=-2$ coupling | ✅ | F42 Y13: $e_R$ is a **dynamical $U(1)_Y$-coupled field** — the spectral kinetic half-step is Stueckelberg-wrapped so $\chi\to e^{-i\alpha Y/2}\chi\to U_W\to e^{+i\alpha Y/2}\chi$ transforms covariantly to $1.78\times10^{-15}$; bit-for-bit reduces to bare Weyl at $\alpha=0$ (Y14, $0.0$) | mass *value* not calibrated (Tier B) |
| $\nu_e$ (left) | ✅ | upper doublet component | massless; no $\nu_R$, neutrino-mass mechanism undecided (QFT-5 oscillations imply mass) |
| $(u,d)_L$ quark doublet — **electroweak** coupling | ✅ | `ca_strong.covariant_quark_doublet_step_2d` (F40 / FG-3 QE2): SU(2)$_L$ Ward identity for constant $V$ exact to $2.8\times10^{-16}$; W4.1 quark analog. **Quark $U(1)_Y$ now also wired** (F42): quark mass step carries $\Delta Y_u=-1$, $\Delta Y_d=+1$, Ward identities $\sim9\times10^{-16}$ (Y8/Y9) | — |
| $u_R, d_R$ singlets w/ hypercharge | ✅ | F42 Y13: $u_R$ ($Y=+\tfrac43$) and $d_R$ ($Y=-\tfrac23$) promoted to **dynamical $Y$-coupled fields** via the same Stueckelberg-wrapped kinetic step; gauge covariance $1.78\times10^{-15}$, $\alpha=0$ reduction bit-for-bit (Y14); quark GMN algebra $5.55\times10^{-17}$ (Y15) | mass *values* not calibrated (Tier B) |
| Quark colour (3 colours, SU(3)) | ✅ | `ca_strong.py`: link variables, Gell-Mann normalisation (#31), colour-charge conservation (#8, $3.8\times10^{-13}$); also conserved under F27 mass + W-coupled doublet steps to $\sim 10^{-14}$ (F40 Q8, QE6) | — |
| Quark mass via the **adopted** F27 mechanism | ✅ | F40 / FG-2: per-flavour F27 1-flavour β-gauge mass step with $m_u, m_d, m_s$ splitting; U(1) Ward $1.2\times10^{-16}$; cold-link regression bit-for-bit; mass-gap without Higgs $N_R/N_{L0}=0.30$ | mass *values* not calibrated (Tier B) |
| Antiparticles | ✅ | Dirac 4-spinor carries them; **CPT** verified (`test_13_QFT8_CPT`); **F53 / FG-9 (2026-05-29 - 21:10):** explicit per-species $C$, $P$, $CP$ — antiparticle charge table negates $(T_3,Q,Y)$ with GMN exact for both (P1); $C$ and $P$ maximally violated by the left-only charged current ($A_C=A_P=1$, P2/P3); $CP$ conserved with single-generation Jarlskog $N(1)=0$ exact (P4); F27 mass-phase $\theta$ pure gauge ($3.3\times10^{-16}$ spectral + bit-for-bit gauge removal, P5); CPT per species at $0.0$ (P6). 6/6 PASS. | — |

### 2.2 Gauge-boson content

| Requirement | Status | Where it lives / what's verified | Gap |
|---|---|---|---|
| Photon $\gamma$ | ⚠️ | composite bilinear `ca_maxwell.py`, F26 rotation-law propagation exact; **two-helicity construction (FG-6, 2026-05-26): both Weyl branches now wired** via `EM_bilinears_two_helicity` + RS decomposition; F^+→Ω^+ and F^-→Ω^- tracked to 1.5e-15, F30 birefringence reproduced. | two photon objects still coexist (composite bilinear vs. the $U(1)$-gauge photon used for minimal coupling in `ca_dirac`) — not unified |
| $W^\pm$ — dynamical, massive | ✅ | `ca_wmu.py` Phases 1–7: covariant hopping (F31), free propagation (F32), Yang–Mills self-coupling (F33), Stueckelberg mass (F34b), Proca dispersion (F36) | mass *value* not calibrated |
| $Z^0$ | ✅ | **F48 / FG-4 (2026-05-28 - 23:30):** `ca_z_field.py` — propagating real $(E_Z, B_Z)$ pair, free massless F26 rotation + Proca mass $\omega^2=m_Z^2+\Omega_{\rm even}^2$; fermion neutral current $J^Z_0 = J^3_0 - \sin^2\theta_W J^{\rm em}_0$ built as SM decomposition and as per-species $\Sigma_f(g_L^f\rho_L^f + g_R^f\rho_R^f)$; source-basis identity at FFT floor (Z2 $2.7\times10^{-15}$); F45 bare-angle prediction $g_V^{e_L}=0$ at $\sin^2\theta_W=1/4$ bit-for-bit (Z11). 12/12 PASS. Mass ratio $m_Z/m_W=1/\cos\theta_W$ exact (F35 W6.3). | mass *value* not calibrated (Tier B) |
| Hypercharge $U(1)_Y$ field | ✅ | **F41 + F42:** the pure-gauge $U(x)$ in the F27 mass step carries $\Delta Y$ for both leptons (F41) and quarks (F42); $e_R, u_R, d_R$ couple to $\alpha(x)$ dynamically through the Stueckelberg-wrapped kinetic step (F42 Y13). Ward identities $\sim9\times10^{-16}$ across e/ν/u/d branches; commutes with F35 mixing. | overall coupling magnitude $g'$ not calibrated (Tier B; *ratio* $g'^2/g^2$ derived by F45/F49) |
| 8 gluons (SU(3)) | ✅ | F43 / FG-7 (2026-05-28): `ca_gluon.py` — colour-octet bilinear $G^{a,i}$ + F26 rotation per $a$ (PA.1–PA.6); Wilson plaquette $G^a_{\mu\nu}$ + Yang–Mills self-coupling via $f^{abc}$ (PB.1–PB.6); Wilson-loop area-law primitives + local-$V$ gauge invariance (PC.1–PC.3); quark colour current $\to$ gluon back-reaction (PD.1–PD.5). 2D and BCC both pass. | linear-confinement regime (Creutz / static $q\bar q$ potential) needs real-time link Hamiltonian evolution from a near-identity start; cooling/Kogut–Susskind driver is the follow-up |
| Mass mechanism (Higgs replacement) | ✅ | F27 chiral SU(2) complex-mass for **leptons and quarks** (F40 quark mass + F42 quark $U(1)_Y$); $W$ mass via rank-1 Stueckelberg (F34b/F44); literature-grounded as Stueckelberg/Kunimasa–Goto. No Higgs scalar anywhere in the first generation. | $W$-from-fermion-condensate story not pursued (not required — Stueckelberg suffices); mass *values* uncalibrated (Tier B) |

### 2.3 Consistency requirements

| Requirement | Status | Note |
|---|---|---|
| Electric charge quantisation $Q=T_3+Y/2$ | ✅ (algebraic) | F35 W6.4, 7 particles, $5.6\times10^{-17}$ |
| **Anomaly cancellation** (gauge + gravitational) | ✅ | **FG-1 (2026-05-26 - 02:02):** all six traces vanish as exact rationals — $[\text{grav}]^2\!\cdot\!U(1)_Y=0$, $U(1)_Y^3=0$, $[SU(2)_L]^2\!\cdot\!U(1)_Y=0$, $[SU(3)_c]^2\!\cdot\!U(1)_Y=0$, $[SU(3)_c]^3=0$, $[SU(2)_L]^3=0$. Run with `python3 model-tests/test_FG1_anomaly_cancellation.py`; results in [`test-results/FG1_anomaly_cancellation.json`](test-results/FG1_anomaly_cancellation.json). Supersedes F27's "anomaly cancellation … not tested" note. |
| CPT | ✅ | `test_13_QFT8_CPT` |
| Single mass mechanism across all fermions | ✅ | F27 chiral complex-mass for **both** leptons and quarks (F40 mass + F42 quark $U(1)_Y$); no Higgs–Yukawa anywhere — see 2.1 |

---

## 3. Tier A — what must be ADDED for structural completeness

In rough dependency order:

1. **Quark electroweak vertex. ✅ Done (FG-3)** Extend F34's `covariant_dirac_doublet_step` to the quark doublet $(u,d)_L$: couple it to the same $W_\mu$ links, carrying both colour (SU(3)) and weak isospin (SU(2)$_L$) indices. This is the single most important missing piece — it is what turns "leptons + separate quarks" into "one generation."

2. **Unified mass mechanism. ✅ Done (FG-2)** Replace the quark Higgs–Yukawa mass in `ca_strong.py` with the F27 chiral complex-mass coupling, using two distinct mass parameters for $u$ and $d$. This makes the quark mass story consistent with the adopted design and with the lepton sector.

3. **Right-handed singlets as dynamical, hypercharge-coupled fields. ✅ Done 2026-05-27 - 09:00 (F42, FG-5).** $e_R, u_R, d_R$ are promoted from "spectator $\chi$ / algebraic table entry" to fields that couple to $\alpha(x)$ dynamically: the spectral kinetic half-step is Stueckelberg-wrapped, $\chi\to e^{-i\alpha Y/2}\chi\to U_W\to e^{+i\alpha Y/2}\chi$, satisfying the local $U(1)_Y$ covariance law $S[\alpha+\beta](e^{i\beta Y/2}\chi)=e^{i\beta Y/2}S[\alpha](\chi)$ exactly (Y13, $1.78\times10^{-15}$) and reducing bit-for-bit to bare Weyl at $\alpha=0$ (Y14). The same finding ports F41's mass-step $\Delta Y$ to the quark doublet ($\Delta Y_u=-1$, $\Delta Y_d=+1$; Y8/Y9 Ward $\sim9\times10^{-16}$), so $U(1)_Y$ now acts on *all* first-generation fermions. This is what makes the $Z$ neutral current (F48/FG-4) and the photon emerge correctly for every fermion. **8/8 PASS** (Y8–Y15); module `ca_hypercharge.py`.

4. **Two-helicity photon.** ✅ **Done 2026-05-26 - 03:15 (FG-6).** `ca_maxwell.py` now exposes `EM_bilinears_branch`, `EM_bilinears_two_helicity`, `riemann_silberstein_decomp`, and the matching W-triplet helpers. The bilinear builds (E, B) from BOTH $\sign =\pm$ branches; under chiral propagation `w_propagation_step_spectral`, $F^+$ tracks $\Omega^+$ and $F^-$ tracks $\Omega^-$ to 1.5e-15 over 10 ticks, and the (1,1,1) birefringence reproduces F30's $-\sqrt3 k^2/27$ to 4.5e-5 relative. **What remains under "two-helicity photon":** confronting the predicted vacuum birefringence with polarisation *data* (an experimental comparison, not a model gap) is still open; this is a Tier-B / observational item.

5. **Dynamical $Z$ and hypercharge coupling. ✅ Done 2026-05-28 - 23:30 (F48, FG-4).** `ca_z_field.py` makes the Z a propagating real $(E_Z, B_Z)$ pair with free massless rotation (F26 even dispersion) and Proca-mass evolution $\omega^2 = m_Z^2 + \Omega_{\rm even}^2$. The fermion neutral current $J^Z_0(x) = J^3_0(x) - \sin^2\theta_W J^{\rm em}_0(x)$ is built explicitly, both as the SM decomposition and as the per-species sum $\Sigma_f (g_L^f \rho_L^f + g_R^f \rho_R^f)$ with $(g_L^f, g_R^f) = (T_3^f - Q^f s^2_W,\, -Q^f s^2_W)$. The source-basis identity $g W^3 J^3 + g'(B)(J^{\rm em}-J^3) = e A J^{\rm em} + g_Z Z (J^3 - s^2_W J^{\rm em})$ holds per site at FFT floor (Z2 = $2.7\times 10^{-15}$). At the F45 bare angle $\sin^2\theta_W = 1/4$, the electron Z vector coupling $g_V^{e_L} = -1/2 - 2(-1)(1/4) = 0$ exactly — a structural prediction of the σ ↔ τ swap (Z11, bit-for-bit). 12/12 PASS.

6. **Gluon to dynamical-field standard.** ✅Bring the colour sector up to the level the $W$ reached: dynamical gluon propagation (rotation-law analog), gluon self-coupling dynamics, and a confinement diagnostic. Right now the gluon is a static link variable.

7. **Antiparticle / charge-conjugation closure.** ✅ **Done 2026-05-29 - 21:10 (F53, FG-9).** $C$, $P$, and $CP$ verified explicitly per species: the antiparticle charge table negates $(T_3,Q,Y)$ with Gell-Mann–Nishijima exact for both particle and antiparticle; $C$ and $P$ are maximally violated by the left-only charged current ($A_C=A_P=1$); $CP$ is conserved, with the single-generation Jarlskog count $N(1)=(1-1)(1-2)/2=0$ showing no physical CP phase exists, and the F27 complex-mass phase $\theta$ confirmed pure gauge (spectral θ-independence + bit-for-bit chiral gauge removal). CPT per species reproduces `test_13` at $0.0$. The antiparticle content is now on the same footing as the particle content.

8. **Anomaly cancellation** (also a test — see §5). Structurally, this is the proof that the charge assignments in §1 are consistent; it is the capstone of the fermion content.

A first generation that has items 1–3 and 8 is *structurally* a real generation; items 4–7 bring the bosonic sector and antiparticles up to the same standard.

---

## 4. Tier B — calibration to measured data

Everything in Tier A can be verified with symbolic couplings and masses. To make the model *quantitatively* a first-generation model (i.e. reproduce measurements), the following must additionally be done — and all of it is currently open:

| Item | What it needs | Blocker |
|---|---|---|
| **SI-unit identification** | Pick one of the three Finding-10 resolutions for $a$ and $\tau$ so $c_{\rm lat}=1/\sqrt d$ maps to physical $c$ | Open foundational choice (F10); required before *any* absolute magnitude |
| **Coupling constants** | Fix $g, g', g_s$ → measured $\alpha\approx1/137$, $\sin^2\theta_W\approx0.231$, $\alpha_s(M_Z)\approx0.118$ | Currently arbitrary test values |
| **Weinberg angle** | ⚠️ **partially derived.** The *ratio* $g'^2/g^2$ is now fixed from BCC structure at tree level — F45: σ↔τ swap count gives $\sin^2\theta_W=1/4$ (1:3), $m_Z/m_W=2/\sqrt3$, within 1.77% of PDG with zero fit parameters; F49: bond-axis/sublattice count gives $\sin^2\theta_W=2/9$ (2:7), 0.44% from PDG as an exact rational. Remaining: choose/reconcile the two countings, fix the overall normalisation, and account for the residual gap (RG running / lattice loop corrections, currently absent). | Needs absolute scale + reconciliation of F45 vs F49 |
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
| ~~FG-4~~ ✅ **closed 2026-05-28 - 23:30** (F48, `ca_z_field.py`, 12/12 PASS — free + Proca propagation, per-species $(g_L, g_R)$ table, source-basis identity, sourced step at $g_Z = g/\cos\theta_W$; F45 bare-angle prediction $g_V^{e_L} = 0$ at $\sin^2\theta_W = 1/4$ verified bit-for-bit) | Tier 2/3 | Promotes F35 from algebraic to dynamical |
| FG-5 ✅ | **Hypercharge coupling** of $e_R, u_R, d_R$ to the dynamical $U(1)_Y$ field | Tier 1 | **Run 2026-05-27 - 09:00 — 8/8 PASS (F42).** Quark $U(1)_Y$ Ward identities $8.89/8.95\times10^{-16}$ (Y8/Y9); $\chi$ kinetic gauge-covariance for all three singlets $1.78\times10^{-15}$ (Y13); $\alpha\equiv0$ bit-for-bit reductions for both quark mass step and $\chi$ kinetic step (Y10/Y14, $0.0$); 50-step unitarity $4.43\times10^{-15}$ (Y12); quark GMN algebra $5.55\times10^{-17}$ (Y15). Script `model-tests/test_hypercharge_extension.py`; JSON `test-results/hypercharge_extension.json`; finding `findings/F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md`. Closes the right-handed-singlet gap and §3 item 3. |
| FG-6 ✅ | **Two-helicity photon + birefringence**: build $\Omega^\pm$ bilinear, measure $\Delta\Omega$ vs F30's $-\sqrt3\,k^2/27$ | Tier 1/2 | **Run 2026-05-26 - 03:15 — 10/10 PASS.** Two-helicity bilinears added to `ca_maxwell.py` (`EM_bilinears_branch`, `EM_bilinears_two_helicity`, `riemann_silberstein_decomp`, triplet pair). $F^+\!\to\!\Omega^+$ and $F^-\!\to\!\Omega^-$ tracked to 1.5e-15 over 10 ticks across single-branch + combined initial states; $\Delta\Omega$ on (1,1,1) reproduces $-\sqrt3/27$ to 4.5e-5; per-branch SU(2) singlet invariance + triplet adjoint at machine precision; F29-B4 raw triplet transversality 2.9e-2 = $c_\text{lat}\!\cdot\!k$ at $k$=0.05. Script `model-tests/test_FG6_two_helicity_photon.py`; JSON `test-results/FG6_two_helicity_photon.json`; finding `findings/F39-two-helicity-photon-bilinear.md`. |
| ~~FG-7~~ ✅ **closed 2026-05-28** (F43, `ca_gluon.py`, 20/20 PASS — rotation-law, $f^{abc}$ self-coupling, Wilson-loop primitives, quark-current back-reaction) | ~~linear-confinement regime~~ ✅ **closed 2026-06-01** (F70, `ca_cooling.py` + `ca_confinement.py`, 6/6 + 8/8 PASS — gauge-covariant Wilson gradient-flow/cooling driver; exact 2D area law $\langle W\rangle=w^{RT}$ ⇒ string tension $\sigma>0\,\forall\beta$, Creutz ratio $\chi=\sigma$, **linear static potential $V(R)=\sigma R$**) | Tier 2/3 | Brings SU(3) to the $W$ standard; confinement now predicted |
| **FG-10** (new) — colour-singlet hadron | ✅ **closed 2026-06-01** (F71, `ca_baryon.py`, 8/8 PASS — proton $B=\varepsilon_{abc}u^au^bd^c$: colour-singlet gauge invariance, zero colour charge, exact $Q=1/B=1$, $S_3$-symmetric spin-flavour + total Fermi antisymmetry, energetic binding $V(R)=\sigma R\to\infty$). Scope: operator-level, not yet a dynamical bound state. | Tier 1/2 | First composite hadron; answers "can a proton be built" |
| FG-8 ✅ | **$\beta$-decay charged current**: $d\to u + W^- \to u + e^- + \bar\nu_e$ as a lattice process | Tier 3 | **Run 2026-05-29 - 20:48 — 10/10 PASS (F54).** New additive `ca_charged_current.py` adds the $T^\pm$/$W^\pm$/$J^\pm$ raising-lowering structure. CC1 SU(2) algebra ($0.0$); CC2 $d\to u$ raising $\Delta Q=+1=-Q(W^-)$ (exact ℚ); CC3 both-vertex charge conservation; CC4 V−A parity violation ($0.0$); CC5 quark–lepton universality ($0.0$); CC6 $W^-$ sourced by $J^+$ exactly ($9.2\times10^{-16}$); CC7 Proca $W^-$ dispersion ($3.1\times10^{-13}$); CC8 Fermi limit $G_F/\sqrt2=g^2/8m_W^2$; CC9 full-process $\Delta Q=\Delta B=\Delta L=\Delta(B-L)=0$; CC10 causal A→B end-to-end pipeline. Script `model-tests/test_FG8_beta_decay.py`; JSON `test-results/FG8_beta_decay.json`; finding `findings/F54-fg8-beta-decay-charged-current.md`. Net new: 7 Tier-1 (#142–148), 2 Tier-2 (#54–55), 1 Tier-3 (#27). |
| FG-9 ✅ | **$C$ / $CP$ per species** (extend `test_13_QFT8_CPT`) | Tier 1/2 | **Run 2026-05-29 - 21:10 — 6/6 PASS (F53).** $C$ antiparticle table exact over rationals (P1); $C$ & $P$ maximally violated by the left-only charged current $A_C=A_P=1$ (P2/P3); $CP$ conserved + single-gen Jarlskog $N(1)=0$ exact (P4); F27 mass-phase $\theta$ pure gauge, spectral $3.3\times10^{-16}$ + bit-for-bit removal (P5); CPT per species $0.0$ (P6). Script `model-tests/test_FG9_C_CP_per_species.py`; JSON `test-results/FG9_C_CP_per_species.json`; finding `findings/F53-fg9-C-CP-per-species.md`. **Closes the antiparticle gap (§3 item 7).** |

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
3. **FG-5** — right-handed hypercharge coupling — ✅ **closed 2026-05-27 - 09:00 (F42).** Both halves done: quark mass-step $U(1)_Y$ and the dynamical $\chi$ kinetic step. Unlocked FG-4.
4. ~~**FG-4 dynamical $Z$**~~ ✅ closed 2026-05-28 - 23:30 (F48), ~~**FG-6 two-helicity photon**~~ ✅ closed 2026-05-26, ~~**FG-7 gluon/confinement**~~ ✅ closed 2026-05-28 (F43; linear-confinement regime remains a follow-up). Weinberg angle now derived at tree level (F45 $\tfrac14$, F49 $\tfrac29$) — no longer a free input to FG-4.
5. ~~**FG-9 $C$/$CP$ per species**~~ ✅ closed 2026-05-29 - 21:10 (F53, 6/6 PASS — antiparticle table, maximal $C$/$P$, conserved $CP$ with $N(1)=0$, θ pure gauge, CPT per species) and ~~**FG-8 $\beta$-decay**~~ ✅ closed 2026-05-29 - 20:48 (F54, 10/10 PASS — $T^\pm/W^\pm/J^\pm$ structure, both-vertex charge conservation, V−A parity violation, quark–lepton universality, Fermi limit, causal A→B end-to-end pipeline). **With both closed, every Tier-A structural test is complete; the first generation is structurally closed up to Tier-B calibration.**
6. In parallel, do the cheap file cleanup: retire `forks/complex_mass_fork.py` (§6.1) after fixing its citations, and consolidate the duplicate result dirs (§6.5).
7. Only after the structure is closed, open **Tier B**, starting with **CO-1 (SI units)** since every absolute number depends on it.

---

*End of review. This document covers the particle-content question only; the 2026-05-22 `project-review-{model,physics,tests,findings}.md` set remains the reference for the broader physics, and `exactness-inventory.md` remains the canonical results ledger.*
