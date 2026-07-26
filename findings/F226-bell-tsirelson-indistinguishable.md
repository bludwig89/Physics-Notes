# F226 — Route 3: the lattice register saturates Tsirelson $S_\text{CHSH}=2\sqrt2$ **exactly**, so it is **Bell-indistinguishable** from QM; the only discreteness entry (analyzer-angle granularity) is quadratic and Planck-suppressed to $\sim10^{-54}$

**Date:** 2026-07-02 - 14:05
**Numbering:** **F226** (re-checked per CLAUDE.md; F215–F225 taken by concurrent sessions — grepped `findings-index.md`, F226 free). Companion to F227 (Route 4). Executes Route 3 of `docs/roadmaps/qc-routes-3-4-prompt.md`.
**Status:** Confirmed — 5/5 checks PASS. Tsirelson saturation is **machine-precision exact** ($\lvert S\rvert=2\sqrt2$ to $1.8\times10^{-15}$, convention-free Horodecki-optimal); the discreteness-correction curvature $-3\sqrt2$ and its quadratic scaling are **exact-algebraic** (verified to $<10^{-2}$); the Planck-suppression magnitude and the Bell-data confrontation are quantitative.
**Verdict:** The model is **Bell-indistinguishable from quantum mechanics** — a defensible, honest, publishable statement. Loophole-free Bell experiments **cannot** discriminate this substrate from QM, and this route does **not** yield a near-term test.
**Modules:** `ca-simulation/ca_bell_tsirelson.py` (CHSH on the native register; granularity/scaling; SI Planckian $\delta\phi$).
**Test / results:** `tests/findings/test_F226_bell_tsirelson.py` (5/5) → `test-results/F226_bell_tsirelson.json`.
**Cross-references:** [[F212-dynamical-entanglement-generation]] (the genuine $2^n$ register), [[F214-superexchange-and-live-entanglement-channel]] (the native exchange gate + derived rate), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=1/\sqrt3$; the rotor form of the measurement operator), [[F130-blockspin-rg-gauge-gravity]] (LIV operators RG-irrelevant), [[F123-p6-si-scale-matter-sector]] / [[F107-canonical-a-adoption-L4-grb-gate]] (the SI bridge $\tau,a$), `tests/priority/test_02_QM1_CHSH.py` (the earlier hand-inserted-product "singlet" this supersedes). External: Tsirelson bound $2\sqrt2$; Hensen et al. Nature **526**, 682 (2015); Giustina et al. PRL **115**, 250401 (2015); Shalm et al. PRL **115**, 250402 (2015); Horodecki CHSH criterion; ’t Hooft cellular-automaton interpretation.

---

## The question (Route 3)

A deterministic cellular-automaton substrate that reproduces QM must **either** (a) saturate Tsirelson's bound $S_\text{CHSH}=2\sqrt2$ *exactly* — in which case loophole-free Bell experiments cannot tell it apart from QM, and one must **say so plainly** — **or** (b) predict a discreteness deviation $\delta S(a,E)$ testable against the loophole-free Bell data that agree with QM to high precision. This finding settles which.

## 1. The genuine register saturates Tsirelson to machine precision (G1)

The earlier QM-1 test (`test_02_QM1_CHSH.py`) built its "singlet" as a **product** $A_\uparrow\!\cdot\!B_\downarrow$ — the entanglement was inserted by hand. Here the entangled pair is **generated** by the model's own perfect entangler: starting from the product $|{\uparrow\downarrow}\rangle$, one application of the native exchange gate

$$U_\text{exch}(\pi/8)=\exp\!\big(-i\tfrac{\pi}{8}\,\boldsymbol\sigma_A\!\cdot\!\boldsymbol\sigma_B\big)$$

(the F212/F214 gate whose coupling is *derived* from the `ca_dirac` hopping) produces a state with entanglement entropy $S=\ln 2$ to $10^{-16}$. Measuring it with the native $\boldsymbol\sigma\!\cdot\!\hat n$ operators and maximising CHSH over **all** measurement directions (the convention-free Horodecki criterion $S_\text{max}=2\sqrt{t_1+t_2}$, with $t_i$ the eigenvalues of $T^\top T$, $T_{ij}=\langle\sigma_i\otimes\sigma_j\rangle$) gives

$$S_\text{max}=2\sqrt2=2.8284271247\ldots,\qquad \text{residual }1.8\times10^{-15},$$

with the correlation matrix $T$ exactly orthogonal (eigenvalues $(1,1,1)$). **The emergent theory is quantum mechanics on this observable**: there is no $O(1)$ deviation and no $O(a\cdot p)$ correction. The register is a genuine $2^n$ Hilbert space (F212), so it violates Bell for the same reason QM does.

## 2. The only discreteness entry is analyzer-angle granularity — and it is quadratic (G2)

Because the register amplitudes and the rotor measurement operators are *exact* complex linear algebra, discreteness can enter in exactly **one** place: the **granularity of the achievable analyzer angles**. A physical single-qubit rotation accumulates continuously in time, but time is quantised in Planckian CA ticks $\tau$, so the settable angle comes in steps

$$\delta\phi=\omega\,\tau=\frac{E}{\hbar}\,\tau=\frac{E}{E_\text{lat}},\qquad E_\text{lat}\equiv\frac{\hbar}{\tau}=3.20\times10^{27}\ \text{eV}\;(\approx3.2\times10^{18}\ \text{GeV, the F119 scale}).$$

CHSH is **stationary at its optimum**: on the Bell family $(a,a',b,b')=(0,2\phi,\phi,3\phi)$ the closed form is $S(\phi)=3\cos\phi-\cos3\phi$, maximal at $\phi=\pi/4$ with $S'(\pi/4)=0$. The leading deviation is therefore second order,

$$\boxed{\;\delta S=-3\sqrt2\,(\delta\phi)^2\;}$$

(fitted curvature $-4.25$ vs $-3\sqrt2=-4.243$; log–log slope $2.00$). The vanishing first derivative is the crux: any misalignment of the analyzer from the optimum costs only $O(\delta\phi^2)$, not $O(\delta\phi)$.

## 3. Confrontation with loophole-free Bell data (G3) — indistinguishable

Plugging the Planckian granularity into $\delta S=-3\sqrt2(E/E_\text{lat})^2$:

| Qubit transition energy $E$ | $\delta\phi=E/E_\text{lat}$ | predicted $\lvert\delta S\rvert$ |
|---|---|---|
| $1.8$ eV (optical) | $5.6\times10^{-28}$ | $1.3\times10^{-54}$ |
| $1$ keV | $3.1\times10^{-25}$ | $4.1\times10^{-49}$ |
| $1$ MeV | $3.1\times10^{-22}$ | $4.1\times10^{-43}$ |
| $1$ GeV | $3.1\times10^{-19}$ | $4.1\times10^{-37}$ |

The measured loophole-free Bell values carry error bars of order $\delta S_\text{exp}\sim0.1$–$0.2$ (Hensen 2015: $S=2.42\pm0.20$; Giustina 2015 and Shalm 2015: photonic, high-significance). Even at $1$ GeV the predicted deviation is **$\gtrsim35$ orders of magnitude below** the smallest experimental error bar. **The model is Bell-indistinguishable from QM.**

This is the honest, defensible outcome the prompt anticipated: exact $2\sqrt2$ ⇒ **not discriminating**. It is itself a valuable statement — it says the deterministic substrate pays for its determinism at the Planck scale only, and leaves the entire Bell-test arena identical to standard QM.

## 4. Measurement-independence / superdeterminism (G4)

The register reproduces the singlet correlation $E(\hat a,\hat b)=-\cos(\theta_a-\theta_b)$ for **freely and independently chosen** settings $a,b$ (RMS deviation from $-\cos$ over 400 random independent setting pairs $<10^{-13}$). The native maximally-entangled state equals the singlet up to a **fixed local unitary** (setting-independent; infidelity $<10^{-12}$), so the correlation depends only on the *relative* analyzer angle, exactly as in QM.

**The violation does not rely on correlated settings.** The ’t Hooft deterministic substrate lives at the Planck scale; the emergent low-energy description is a genuine $2^n$ Hilbert space (F212), i.e. literally quantum mechanics — not a local-hidden-variable table that exploits setting–source correlations. The model therefore violates Bell **by being QM**, and the superdeterminism escape hatch is neither needed nor used. Bell tests are consequently **not** the arena in which this substrate could ever be distinguished from QM.

## Sanity controls (G5)

State normalised to $10^{-12}$; measurement operators Hermitian ($10^{-15}$) and involutive ($10^{-14}$); a separable product control obeys $S_\text{max}\le2$ (classical bound respected).

## What this closes and what remains

**Closes:** the Route-3 yes/no question. Answer: **exact Tsirelson saturation ⇒ Bell-indistinguishable from QM**; no near-term Bell test can discriminate the substrate, and the discreteness correction is quadratic and Planck-suppressed ($\sim10^{-54}$).

**Open:** the granularity argument assumes analyzer angles are the only discreteness channel; a fully field-native measurement model (projective readout realised as genuine second-quantised dynamics, cf. F220) could in principle add a state-preparation error, but F214's live channel already reaches $\ln2$ to the discrete-tick error $3\times10^{-7}$, so any such correction is far above the $10^{-54}$ angle term and still $\sim7$ orders below experiment — it would not change the verdict.
