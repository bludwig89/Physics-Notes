# F405 — F95's cubic $B$ with quark colour and charge factors cannot move the Koide equipartition point: identity-class dressing is sector-blind and $k$-blind (clean fail of report derivation four; three channels left open)

**Date:** 2026-09-24 - 14:58
**Status:** No-go for the stated class (clean fail of the test as posed) — 11/11 checks PASS. E1 and E2 are exact (sympy). U1 and U2 are exact but are identities: they hold by construction, and the test checks rather than discovers them. L1–L3 are numerical; S1, K1, P1 and P2 are quantitative. Two declared controls, each red exactly where declared.
**Verdict:** colour and charge factors rescale $B$ to $B_q=N_c\,k_f^3\,B_\ell$. No rescaling of $B$ can move $k$, and neither can any dressing proportional to the identity in generation space: a uniform mass rescale, an overall factor on the loop, or mass-independent gauge running. With a finite-stiffness selector, lepton Koide precision bounds the effect so tightly that the quark shifts would need a loop weight at least $4.6\times10^3$ times the lepton one, not $N_c=3$.
**Not covered, stated as open:**
- dressings that weight the $A_{1g}$ and $E_g$ components differently (inter-generation stiffness);
- generation-dependent (family) charges;
- a sector-dependent internal amplitude in the unitarity-cap regime (L3).

The power-law loophole gives $\varepsilon_U/\varepsilon_D\approx3.88$, against $Q_u^2/Q_d^2=4$ at 1.8–2.4σ depending on the error model, and needs an $O(1)$ coefficient. It is a **coincidence candidate**.
**Checked:** 2026-09-24 — 3 PASS / 9 WEAKENS / 1 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER** (the one FAIL, attack 4, was disclosure-only and is fixed; see Reviewed & corrected)
**Module:** `casim.engine.particles.derive_quark_B_colour_charge` (new, spine, status `live`)
**Test record:** `F405-quark-B-colour-charge` (tier gate, entry `check_quark_B_colour_charge`), driver `tests/findings/test_F405_quark_B_colour_charge.py` → `test-results/F405_quark_B_colour_charge.json`
**Claim:** none. This is a model-internal no-go on one candidate mechanism. Its only external-physics content, that gauge running identical for every generation leaves intra-sector mass ratios unchanged, is textbook SM. The project's current quark-Koide assertion is CL316.
**Cross-references:** [[F95-B-derived-C-localized]] (the $B$ being dressed: $B=-3\sqrt2\,I_2\,\bar y^4$, origin $3\bar yA^3$; its §7 "inter-generation loop responses not computed" loophole is the first open channel here), [[F80-one-45deg-em-saturation-koide]] (the $\phi=45°$ circle; its EM selector is a hypothesis), [[F92-per-constituent-phase-consistency]] (the $k=1$ equipartition; status Partial), [[F346-quark-shape-eg-t1u-leaning-nogo]] / [[F347-quark-mixed-koide-tuples-leaning-nogo]] (quark $\eta^2=2k^2$, $\delta$), [[F404-koide-pseudomass-quark-fork]] (route 1 of the same report), [[F170-lepton-colour-scale-link]] (strong-sector-induced $E_g$ self-couplings, the "home" route 3 cited). Research report `reports/Quark neutrino hierarchy lattice fit.md`, route 3 and derivation four.

---

## 1. The question

The 2026-09-24 flavour report ranked a **colour- or charge-dressed $E_g$ amplitude** (a Sumino-style radiative shift of equipartition) third among quark routes, and set derivation four:

> Compute F95's cubic coefficient $B$ with quark colour and charge factors. The test is whether the equipartition point shifts to $k^2\approx1.55$ (up) and $1.19$ (down). The derivation fails if the shift is sector-blind.

With the F76/F93/F95 parametrization $y_a=\bar y+A\cos(\delta+2\pi a/3)$, $A=\sqrt2\,k\,\bar y$, $m_a=y_a^2$, Żenczykowski's $k$ is the Koide amplitude: $k=1$ is the lepton equipartition and $Q=(1+k^2)/3$. In F346's notation $\eta^2=2k^2$.

**Scheme caveat on the targets.** The target $k^2_U=1.55$ is computed in the report's mixed scheme ($u,d,s$ at 2 GeV, $c,b$ at $m(m)$, $t$ direct). That is not a common-scale set. The move to $M_Z$ ($k^2_U=1.663$) is itself a mass-dependent effect of the P1 kind, so the mixed-scheme target is not RG-meaningful by itself. Both schemes are carried throughout.

## 2. E1, E2 (exact) — $B$ lives on the wrong coordinate

$$\textstyle\sum_a y_a=3\bar y,\qquad \sum_a y_a^2=3\bar y^2+\tfrac32A^2,\qquad Q=\frac{1+k^2}{3}.$$

Both sums are independent of $\delta$, so $Q$ and the equipartition point are functions of $k$ alone. $B$ is by definition the coefficient of $\cos3\delta$ (F93 form, F95 D1), and so is $C$'s $\cos^23\delta$. **No colour or charge factor on $B$ or $C$ can move $k$.** They set the angle, not the amplitude.

The exact Fourier projection of $\sum y^4$ gives the $\cos3\delta$ coefficient $3\bar yA^3$ (F95 D2, reproduced). Therefore

$$B(k)=k^3B(1),\qquad B_q=g_f\,k_f^3\,B_\ell\quad(\text{common }\bar y).$$

This uses colour only, $g_f=N_c=3$. The charge factor is set to 1 because the free Dirac sea of F95 contains no photon; a charge-dependent vertex factor would be one more overall $g_f$ and changes nothing below. With the lepton value $B_\ell=-0.0569$ (`B_sea_cubic`, F95):

| sector | $k^2$ (mixed) | $B_q/B_\ell=N_c k^3$ | $B_q$ |
|---|---|---|---|
| up $(u,c,t)$ | 1.5464 | 5.769 | −0.328 |
| down $(d,s,b)$ | 1.1939 | 3.913 | −0.223 |

These are the numbers the report asked for. They answer the angle question, not the amplitude question. How they move $\cos3\delta=-B/2C$ depends on what is held fixed:

- at fixed $C$, $\cos3\delta$ is multiplied by $N_ck^3$;
- at fixed $\lambda_6$ (so $C\propto e^6\propto k^6$), it is multiplied by $N_c/k^3$.

Either way the result also carries the unfixed quark internal amplitude through $B/C\propto\bar y^{-2}$, so no $\delta_q$ prediction follows. This is recorded, not tested.

## 3. U1, U2 (exact identities) — the identity class cannot move $k$

Colour ($N_c$, $C_F$) and electric charge ($Q_f$) take the same value on all three generations of a sector: $(u,c,t)$ all carry $\tfrac23$ and colour $\mathbf 3$. A dressing built only from them, and applied the same way to each generation, is a multiple of the identity in generation space. There are two ways it can enter, and both leave $k$ unchanged:

- **Overall factor on the loop,** $F\to g_fF$ with $g_f>0$. Every argmin in $(k,\delta)$ is unchanged *if the loop is the whole functional* (see S1 for the finite-stiffness case).
- **Uniform mass rescale,** $m_a\to\lambda_f m_a$. $Q$ is homogeneous of degree zero, so $Q(\lambda m)=Q(m)$.

U2 is the running version. The one-loop mass anomalous dimension in a mass-independent scheme, $\gamma_m=6C_F\alpha_s/4\pi+3Q_f^2\alpha/2\pi$, carries no generation index, so running multiplies all three masses in a sector by the same factor. This is the textbook SM statement that gauge running leaves intra-sector mass ratios invariant. It agrees with the observation that $Q_U(M_Z)\approx0.89$ barely moves up to $10^{14}$ GeV (Xing–Zhang, via the report notes).

**These are identities, not discoveries.** The checks ($\Delta Q=0$ symbolically, $2\times10^{-16}$ numerically) are zero by construction once the premise holds. The content of the no-go is the premise: colour and charge are generation scalars.

**What the identity class does not cover:**

1. **$A_{1g}$/$E_g$-differential dressing.** A dressing that treats the democratic and splitting components differently can move $k$. Examples are a uniform *additive* shift of the amplitude, $y_a\to y_a+c$ (which restores Koide with $c_U=+36.7$ and $c_D=+2.36\ \sqrt{\text{MeV}}$, mixed scheme), or a dressed $E_g$ stiffness. This is the literal reading of route 3's "dressed $E_g$ amplitude" and of F170's strong-sector-induced stiffness. It needs an inter-generation, non-per-axis term, which is the loophole F95 §7 left uncomputed. **Open.**
2. **Generation-dependent charges.** Family gauge charges (Sumino) or CKM-weighted charged-current corrections are not generation scalars. The model has neither. **Open, and outside the class.**

*Controls.* Give the up generations charges $(\tfrac23,\tfrac23,-\tfrac13)$: U1 goes red. Replace uniform running by a power law $m\to m^{1+\gamma}$: U2 goes red.

## 4. L1–L3 (numerical) — the loop prefers $k^2\approx1.9$, not 1

On F80's circle ($\sum y^2=R^2$ fixed, $k=\tan\phi$), the leading-order F95 loop energy is $-\tfrac{I_2}{2}R^4S_4(\phi,\cos3\delta)$ with

$$S_4=\tfrac13c^4+2c^2s^2+\tfrac12s^4+\tfrac{2\sqrt2}{3}\,c\,s^3\cos3\delta\qquad(c,s=\cos\phi,\sin\phi).$$

| $\delta$ | loop-preferred $k^2$ |
|---|---|
| $\delta^*=2/9$ | 1.896 |
| 0.0745 (up, mixed) | 1.988 (next to $Q\to1$) |
| 0.1101 (down, mixed) | 1.976 |

The full nonperturbative BCC sea (F46 map, both branches, $L=16$, $\phi$-grid $n=400$, $R=0.5$) gives $k^2=1.902$ at $\delta^*$ (L2). The referee found it stable for $L=8$–24 and $R=0.3$–1.0. It is identical under $g_f=N_c\cdot\tfrac49$.

So the loop *does* have a $k$-preference, $k^2\approx1.9$, and it is wrong for the charged leptons, where $k^2=1.0000$. $k=1$ is attributed to the F80/F81/F92 45° saturation, a chain whose F80 selector is a hypothesis and whose F92 is Partial. It is not set by the sea loop.

**L3, the unitarity-cap route.** Above $R\approx1.015$ the clamp $m\le1$ cuts the circle, and the argmin sweeps continuously with $R$ (at $\delta^*$):

| $R$ | 1.00 | 1.02 | 1.03 | 1.05 | 1.10 |
|---|---|---|---|---|---|
| $k^2$ | 1.883 | 1.374 | 0.992 | 0.688 | 0.383 |

It passes through 1.55, 1.19 and 1. It is $g_f$-blind, so colour and charge cannot drive it. But a sector-dependent **internal amplitude** $R_q$ could, and nothing in the model fixes $\bar y_q$. The lepton value $R\approx1.03$ (τ-pinned) lands at $k^2\approx0.99$. That is **circular**, because $R$ was taken from the lepton data at $k=1$. **Open, and not a colour/charge route.**

## 5. S1 (quantitative) — a finite-stiffness selector is bounded by lepton Koide

If the 45° selector has finite stiffness, $E=K(k^2-1)^2+g R^4V_\text{loop}(k^2,\delta)$, an overall loop weight *does* move $k$: in linear response $\delta k^2=-gR^4V'(1)/2K$. The loop pushes $k^2$ **up**, which is the right sign for quarks. But the same functional holds for the leptons:

- **Lepton bound.** $k^2_\ell-1=-6.6\times10^{-6}$, with $\sigma=1.5\times10^{-5}$ from $m_\tau=1776.93\pm0.09$ MeV (PDG 2024). At $2\sigma$, $|\delta k^2_\ell|\le3.7\times10^{-5}$.
- **Quark requirement.** The quark shifts (0.546 up, 0.194 down), corrected for the $\delta$-dependence of $V'$, need $(gR^4)_q/(gR^4)_\ell\ge4.6\times10^3$ (down) and $1.3\times10^4$ (up).

Colour supplies $N_c=3$. An amplitude factor $R^4$ cannot make up the rest in the interior regime: $R\lesssim1.015$ before the cap, and the lepton $R$ is already about 1.03. **Caveat:** this is linear response for an interior minimum, and the lepton point sits in the cap regime of L3. S1 excludes a colour/charge-weighted selector, not the L3 amplitude route.

## 6. P1, P2 (quantitative) — the power-law loophole is a coincidence candidate

A dressing that is uniform in *form* moves $k$ only if it depends on the mass itself: thresholds, or the $\ln m$ pieces of pole-versus-running relations (Sumino's QED case). The simplest such form, and the only one tried, is $m\to m^{1+\varepsilon}$. It is $\mu$-independent. The first-order form $m(1+\varepsilon\ln(m/\mu))$ has no up-sector solution for any $\mu$ from 1 MeV to $m_t$ (referee check), so the numbers below are specific to this ansatz. Solving $Q\big(m^{1/(1+\varepsilon)}\big)=\tfrac23$:

| | $\varepsilon_U$ | $\varepsilon_D$ | $\varepsilon_U/\varepsilon_D$ | $\kappa C_F=\varepsilon/Q_f^2$ (U / D) |
|---|---|---|---|---|
| mixed, independent errors | 0.639 | 0.165 | 3.885 ± 0.047 (2.4σ from 4) | 1.44 / 1.48 |
| mixed, correlated light-quark ratios | | | 3.878 ± 0.068 (1.8σ from 4) | |
| $M_Z$ (no errors propagated) | 0.821 | 0.210 | 3.915 | 1.85 / 1.89 |
| charged leptons | $\sim10^{-5}$ | | | |

The correlated model uses $m_{ud}$ at ±1%, $m_u/m_d=0.462\pm0.020$ and $m_s/m_{ud}=27.23\pm0.10$. The ratio sits near $Q_u^2/Q_d^2=4$ (and $Y_R^2$ also gives 4) in both schemes. **It is not adopted:**

1. **Tension depends on the error model.** It is 1.8–2.4σ, and the ratio's sensitivity is dominated by $m_s$ and $m_d$. The test records these σ values and does not gate on them.
2. **Size.** $\kappa C_F\approx1.4$–1.9 is $O(1)$. The smallest perturbative colour×charge source, $C_F\alpha\alpha_s/\pi^2=1.2\times10^{-4}$, is about $10^4$ times too small. **This is what P1 asserts.**
3. **Look-elsewhere.** About five natural targets lie in $[1,10]$ (1, 2, 3, 4, 9) with a ±0.115 window, giving a chance probability $p\approx0.1$ of landing this close to one. The target 4 was noticed after the data were in hand.
4. **No lepton-shaped parent (P2).** The undressed angles are $\delta_U=0.188$ and $\delta_D=0.139$ (mixed). Under the correlated error model they are $69\sigma$ and $154\sigma$ from $2/9$, and $49\sigma$ from each other.

This goes to derivation seven's look-elsewhere ledger alongside $\delta_U\approx2/27$, $\delta_D\approx1/9$ and $\sin(2/9)\approx|V_{us}|$.

## 7. What this settles and what it leaves

**Settled:**
- Colour and charge factors enter F95's $B$ as $B_q=N_ck_f^3B_\ell$, and no factor on $B$ or $C$ moves $k$.
- No identity-class dressing (uniform rescale, overall loop factor, mass-independent running) moves $k$.
- A finite-stiffness selector weighted by colour or charge is excluded by lepton Koide precision, by a factor of more than $10^3$.

This sharpens the report's "colour cannot distinguish up from down" to "a generation-scalar dressing cannot move $k$ at all." Route 3 in its $B$-dressing form is closed.

**Open (three channels, none supplied by the model today):**
1. an $A_{1g}$/$E_g$-differential (inter-generation) stiffness, the literal "dressed $E_g$ amplitude" and F95 §7's loophole;
2. generation-dependent (family) charges;
3. a sector-dependent internal amplitude in the unitarity-cap regime (L3).

The mass-dependent power-law pattern (P1) remains a coincidence candidate. The report's $k$-side quark physics stays with route 1 (F404) and route 2.

## 8. Prior art

- **RG invariance of intra-sector mass ratios** under pure gauge running in a mass-independent scheme is textbook. U2 rediscovers it and does not claim novelty.
- **Sumino** (arXiv:0812.2090, PLB 671 (2009) 477; arXiv:0812.2103, JHEP 05 (2009) 075) showed that the QED correction to pole masses breaks lepton Koide at the $10^{-3}$ level through an $\alpha\ln m$ term. His cure uses a U(3) family gauge symmetry whose charges *do* distinguish generations. That is exactly open channel 2, excluded here by assumption and not covered by the no-go.
- **Żenczykowski** (arXiv:1301.4143) supplies the $k$ parametrization and the quark $k$ values; $k_U=1.244$ and $k_D=1.093$ (mixed) are reproduced here.

## 9. Test summary (`casim test --id F405-quark-B-colour-charge`, 2026-09-24 - 15:30)

| Check | Statement | Residual / value | Class | Status |
|---|---|---|---|---|
| E1 | $\sum y=3\bar y$, $\sum y^2$ is $\delta$-blind, $Q=(1+k^2)/3$ | 0 (sympy) | exact | PASS |
| E2 | $\cos3\delta$ coeff $=3\bar yA^3$, $B(k)=k^3B(1)$ | 0 (sympy) | exact | PASS |
| K1 | required $k^2$: U 1.5464 / 1.6627, D 1.1939 / 1.2442; lepton 0.99999 | — | quantitative | PASS |
| U1 | identity-class dressing: $\Delta Q=0$ | 0 by construction | exact (identity) | PASS |
| U2 | mass-independent running: $\Delta Q=0$ | 0 by construction | exact (identity) | PASS |
| L1 | loop $k^2$ preference 1.896 / 1.988 / 1.976; $g_f$-blind | — | numerical | PASS |
| L2 | nonperturbative BCC sea agrees (1.902, $n=400$), $g_f$-blind | $<$ one grid step | numerical | PASS |
| L3 | cap sweep 1.37→0.38 for $R$ 1.02→1.10; $g_f$-blind | — | numerical | PASS |
| S1 | finite stiffness: need $(gR^4)_q/(gR^4)_\ell\ge4.6\times10^3$ | lepton bound $3.7\times10^{-5}$ | quantitative | PASS |
| P1 | power-law loophole needs $\kappa C_F/\text{pert}>10^3$; ratio σ recorded | 1.8–2.4σ from 4 | quantitative | PASS |
| P2 | undressed $\delta$ is $>3\sigma$ from 2/9 and U ≠ D | 69σ / 154σ / 49σ | quantitative | PASS |

**Controls:** `generation_charges_up=[2/3,2/3,-1/3]` → U1 red; `mass_dependent_dressing=true` → U2 red. The legs that cannot fail are U1 and U2 (identities) and the $g_f$-blindness parts of L1–L3 (argmin under a positive rescale). The legs that can fail on data are K1, S1, P1 and P2.

## Reviewed & corrected

**2026-09-24 - 15:30** — attack pass: **CONFIRMED-NARROWER**.

**Found:**
- The claims "any gauge dressing", "at any order" and "the loop does not select $k$ at all" were too wide: additive or $A_{1g}$/$E_g$-differential dressings, family charges and a finite-stiffness selector escape them.
- U1/U2 were presented as findings rather than identities.
- §2 had the $\cos3\delta$ factor inverted ($N_c/k^3$ should be $N_ck^3$ at fixed $C$).
- §4 wrongly said the cap argmin sits on the edge at $R\approx1$; it actually sweeps above $R\approx1.015$.
- P1's >2σ gate flipped to 1.8σ under correlated light-quark errors.
- The documented CLI control form errored.
- L2's tolerance was below its grid step.
- $m_\tau$ was pre-2024.
- Sumino was not credited.

**Fixed:**
- Claim narrowed to the identity class, with three open channels named.
- Identities disclosed.
- §2 factor corrected.
- New L3 (cap sweep) and S1 (finite-stiffness bound from lepton Koide) legs.
- P1 now gates on the coefficient size and records σ under both error models; P2 gets Monte Carlo σ.
- CLI string parsing fixed.
- L2 grid raised to $n=400$ with a one-step tolerance.
- $m_\tau$ updated to PDG 2024.
- Prior-art section added.
- Look-elsewhere number ($p\approx0.1$) added.

**Rejected (partly):** the referee's sign for the additive shift. Its magnitudes reproduce, but the shift is $c>0$ ($+36.7$, $+2.36\ \sqrt{\text{MeV}}$), not $c<0$; a negative $c$ moves the up-sector $Q$ away from 2/3.

**Deferred:** the $A_{1g}$/$E_g$-differential stiffness computation and the L3 amplitude route, both of which need an inter-generation loop F95 §7 never built. They land in the report's derivation list (`reports/Quark neutrino hierarchy lattice fit.md`, derivation four's result block).

## 10. Provenance

- **New:** the $B_q=N_ck^3B_\ell$ dressing, the identity-class no-go for $k$, the loop's own $k$-preference and its cap sweep, the finite-stiffness bound from lepton Koide, and the power-law loophole bound with its $Q_f^2$ coincidence.
- **Reused:** F95's projection and sea function; `casim.engine.lattice.bcc.bcc_dispersion`; F346/F347's circulant $\delta$ fit.
- **Inputs:**
  - PDG 2025 quark summary (mixed scheme);
  - $M_Z$ running masses from Antusch–Hinze–Saad arXiv:2510.01312, via the report notes, with no errors propagated;
  - PDG 2024 charged-lepton masses ($m_\tau=1776.93\pm0.09$ MeV);
  - FLAG-style light-quark ratios for the correlated error model;
  - $\alpha$ and $\alpha_s(M_Z)$, used only for the P1 size estimate.
