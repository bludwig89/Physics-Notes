# F297 — K2: Big-Bang nucleosynthesis on the model's own expansion law — the light elements come out right, and BBN then measures $m_n-m_p$ 179× more sharply than F122 checked it

**Date:** 2026-08-05 - 23:20
**Status:** **Confirmed — 12/12 PASS**, and the confirmation is a *falsifier*. Rubric row **K2** moves `ABSENT → PARTIAL`. Two legs are quantitative against published standard-BBN reference values (network validation), two are structural (N_eff, $\dot G/G$), and the headline is differential (model $\Delta m$ vs measured $\Delta m$, computed inside the same network so the network's own error cancels).
**Module:** `src/casim/engine/interactions/cosmology_bbn.py`
**Test record:** `F297-bbn-light-elements` (gate tier)
**Results:** `test-results/F297_bbn_light_elements.json`
**Claim card:** `docs/claims/CL258-bbn-light-elements.md`

**Cross-references:** [[F79-structural-newton-constant]] and [[F107-canonical-a-adoption-L4-grb-gate]] (the structural $G$ that sets $H(T)$), [[F178-gravity-full-tensor-adoption]] and [[F182-friedmann-pressure-cosmology]] (the adopted source law, and the energy-only law this finding excludes on a second, independent observable), [[F284-rigid-lattice-expansion-and-primordial-state]] and [[F283-elastic-lattice-excluded-and-f282-invariance]] ($\dot G/G\equiv0$ — the BBN bound those findings *quote* becomes a prediction here), [[F122-p2-dynamical-baryon-three-body]] and [[F123-p6-si-scale-matter-sector]] (the $m_n-m_p$ this finding confronts), [[F104-p4-deuteron-tensor-bound-nucleus]] / [[F113-nn-short-range-repulsive-core]] / [[F126-nn-intermediate-range-sigma-attraction]] (the deuteron binding at the bottleneck), [[F47-majorana-seesaw-higgs-free]] / [[F165-hypercharge-quantisation-from-anomaly-and-mass]] / [[F279-hypercharge-constraint-attribution]] ($\nu_R$ a total singlet, hence $N_\text{eff}$), [[F202-leptogenesis-from-intrinsic-L-violation]] (the baryon asymmetry's *magnitude* is free and inherited, so $\eta_b$ is an input), [[F188-multicomponent-lcdm-cosmology]] (the expansion history this sits inside). External: Aver et al. 2021 (JCAP 03, 027; $Y_p$); Cooke, Pettini & Steidel 2018 (ApJ **855**, 102; D/H); Planck 2018 VI ($\eta_b$, $N_\text{eff}$); Smith, Kawano & Malaney 1993 (ApJS **85**, 219; reaction rates); Pitrou et al. 2018 (PRIMAT, reference abundances).

---

## 1. Why this row was absent, and what "absent" meant

Nine findings in this tree mention BBN. Every one uses it as an **external bound quoted at the model** — F283 and F284 read the BBN limit on $\dot G/G$, F237 reads the BBN limit on relics — and none computes an abundance. The 2026-08-04 completeness report put K2 in the ABSENT table for exactly that reason, and its Amendment 2 identified the pattern the other closures followed: *"absent" in this tree has mostly meant "never assembled", not "not there"*.

K2 is the same shape. BBN is a competition between **one expansion rate** and **a set of reaction rates**, and the model already owned the entire expansion side:

| BBN needs | The model has | Status |
|---|---|---|
| $H(T)$ in the radiation era | $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ (F79/F107), $3\times10^{-8}$ of CODATA, zero free parameters | derived |
| the source law | induced Einstein equation, $\rho+3p=2\rho$ for radiation (F178/F182) | adopted, and now independently tested |
| $\dot G/G$ | **exactly zero** on the rigid substrate (F79/F284) | derived |
| $N_\text{eff}$ | the model's own light content | derived (§3) |
| $m_n-m_p$ | $+1.51$ MeV, no QCD anchor (F122/F123) | derived — and this is where it fails |
| $B_d$ | 2.224 MeV on a derived OBE potential, one parameter $b=0.55$ fm fixed to it (F104/F113/F126/F240) | reproduced, not predicted |
| $\eta_b$ | nothing — F202 meets the Sakharov conditions structurally but derives no asymmetry number | **external input**, and labelled so |

So the assembly was available. What it produced was not what the "never assembled" pattern would predict.

---

## 2. Method, and the one methodological commitment that matters

`cosmology_bbn.py` is a compact standard-BBN code: entropy-conserving thermal history from $T=10$ MeV, six Born-level weak $n\leftrightarrow p$ channels written out separately, then an implicit 8-species / 12-reaction nuclear network (Wagoner–Kawano construction) to freeze-out of the abundances.

It is **not** PRIMAT, and pretending otherwise would make every number here unfalsifiable in the way the 2026-08-04 report's gap #2 describes. So its absolute accuracy is *measured* against published reference values at the same $(\eta_{10},N_\text{eff},\tau_n)$, and reported with every absolute number:

| Quantity | This network | Reference (PRIMAT class) | Offset |
|---|---|---|---|
| $Y_p$ | 0.24494 | 0.24709 | $-0.87\%$ |
| D/H | $2.473\times10^{-5}$ | $2.459\times10^{-5}$ | $+0.55\%$ |
| $^3$He/H | $1.097\times10^{-5}$ | $1.07\times10^{-5}$ | $+2.5\%$ |
| $^7$Li/H | $3.89\times10^{-11}$ | $5.0\times10^{-10}$ | **$-92\%$ — NOT validated** |

**The commitment:** every *model-level* conclusion below is a **difference computed inside this same network** — model $\Delta m$ against measured $\Delta m$, energy-only law against full-tensor law — so the $\sim1\%$ absolute offset cancels to first order. The differentials are the result; the absolutes are context.

**Lithium is declared broken, not quietly dropped.** The $A=7$ chain comes out an order of magnitude low, so four of the twelve rate fits are wrong or incomplete in this implementation. `Li7_H` is still returned, because suppressing it would hide the defect, and it is **excluded from the check battery** for the same reason it is named here. This finding makes **no lithium claim in either direction**, and the famous lithium problem is untouched by it.

Two further checks exist to make the thermodynamics itself falsifiable rather than assumed:

- **$T_\nu/T_\gamma\to(4/11)^{1/3}$ is emergent, not input.** The run starts above $e^\pm$ annihilation with $T_\nu=T_\gamma$ and the ratio is produced by entropy conservation. Recovered to $6.0\times10^{-5}$. It can fail: delete the $e^\pm$ term and the ratio goes to 1.
- **Detailed balance is emergent, not imposed.** The six weak channels are written from their separate matrix elements with a shared coupling $K$; $\lambda_{p\to n}/\lambda_{n\to p}\to e^{-\Delta m/T}$ then *has* to come out, and does, to $5.0\times10^{-5}$.

---

## 3. $N_\text{eff}$ — a prediction with no freedom

The question BBN asks is: what, in this model, is light and thermalised at $T\sim1$ MeV that is not a photon or an electron? The answer is *the three left-handed neutrinos and nothing else*, and every clause is owned by a finding rather than assumed:

- **$\nu_R$ never thermalises.** It is a **total** singlet — $Y=0$ is forced by the constraint system (F165, re-derived F279) — so it has no renormalisable coupling to the bath. It also carries the heavy see-saw Majorana mass (F47/F236). Two independent reasons for the same zero.
- **No light scalar exists to add.** The model is Higgs-free (founding decision 3); the $E_g$ doublet is the massive condensate direction (F253/F255).
- **No light dark sector.** The dark-matter candidate is a Planck-mass geon remnant (F223/F228), non-relativistic by nineteen orders.

$$N_\text{eff}=3.044\qquad(\text{Planck }2.99\pm0.17,\ +0.32\sigma).$$

The falsifier is sharp: any renormalisable $\nu_R$ coupling adds $\Delta N_\text{eff}=1.71$, excluded at more than $10\sigma$.

---

## 4. The gravitational law — BBN is an independent discriminator, and it agrees with F178

F178 adopted the induced Einstein equation over the energy-only dielectric on Lorentz covariance and the neutron-star maximum mass (F174/F176). BBN sits three decades of redshift away and tests the same choice on a completely different observable.

**The expansion normalisation is derived, not posited.** Take the acceleration equation with source $\kappa\rho$ — $\kappa=2$ for the adopted law ($\rho+3p=2\rho$ in radiation), $\kappa=1$ for the demoted energy-only law — impose continuity so $\rho\propto a^{-4}$, and look for $a\propto t^n$:

$$\frac{n(n-1)}{t^2}=-\frac{4\pi G}{3}\,\kappa\,\rho_0a^{-4}.$$

Power matching gives $n=\tfrac12$ for **either** law: the energy-only law does not change the power, it changes the normalisation. Fixing the coefficient and comparing with $H=n/t$:

$$\boxed{\;H^2=\frac{8\pi G}{3}\rho\cdot\frac{\kappa}{2}\quad\Longrightarrow\quad S(\text{law})=\sqrt{\kappa/2}\;}$$

$S=1$ for the full-tensor law — Friedmann I recovered exactly, as it must be — and $S=1/\sqrt2=0.7071$ for the energy-only law: **a universe expanding 41% too slowly at fixed temperature.** Since freeze-out is defined by $\lambda_\text{weak}=H$, that is a large, one-signed shift.

| | full-tensor (F178) | energy-only (F106) |
|---|---|---|
| $S$ | 1 | $0.70711$ |
| $T_\text{freeze-out}$ | 0.667 MeV | 0.583 MeV |
| $Y_p$ | 0.2449 | **0.1856** |
| D/H | $2.47\times10^{-5}$ | $1.19\times10^{-5}$ |
| vs Aver 2021 $Y_p=0.2453\pm0.0034$ | $-0.11\sigma$ | $\mathbf{-17.6\sigma}$ |

**State the conditionality, because it is real.** F182 A1 showed the energy-only law is *internally inconsistent* for $p\ne0$ — Friedmann I, the acceleration equation and continuity cannot all hold — so evaluating it at all requires choosing which equation survives. This control keeps the **dynamical** equation plus continuity, which is the reading under which the law is a law, and BBN excludes that reading at $17.6\sigma$. Under the other reading — keep Friedmann I and let the acceleration equation simply be violated — the expansion history is identical and **BBN says nothing**. This is a strong exclusion of one reading, not a second proof covering both. F182's Bianchi argument is what kills the other.

---

## 5. The result: BBN measures $m_n-m_p$, and the model's value is excluded

With the **measured** $\Delta m$ the model's BBN is standard and correct. With the model's **own** $\Delta m$ it is not.

| | $\Delta m=1.293$ MeV (measured) | $\Delta m=1.51$ MeV (F122/F123) |
|---|---|---|
| $Y_p$ | 0.2449 ($-0.11\sigma$) | **0.1210** ($\mathbf{-36.6\sigma}$) |
| D/H | $2.47\times10^{-5}$ ($-1.8\sigma$) | $1.85\times10^{-5}$ ($\mathbf{-22.6\sigma}$) |
| $\tau_n$ | 878.4 s (calibration) | **330.8 s** vs measured $878.4\pm0.4$ s |

The neutron lifetime is the sharper of the two and needs no network at all: the free-decay phase-space integral $f(q)$ rises steeply in $q=\Delta m/m_e$, so $\Delta m=1.51$ MeV predicts a neutron that lives 331 s. That is not a tension, it is a factor 2.7.

**Inverting BBN into a bound.** The local derivative is $\partial Y_p/\partial\Delta m=-0.607\ \text{MeV}^{-1}$, so the $Y_p$ observation alone pins

$$\Delta m = 1.293 \pm 0.0056\ \text{MeV}\quad(1\sigma).$$

F122's own acceptance criterion (check S8b) was **"within 1 MeV"**. BBN is **179× tighter**, and the model's value misses by $0.217$ MeV — $38.7\sigma$ on the BBN bound.

**What this is actually telling the matter sector.** F122 writes $m_n-m_p=(m_d-m_u)+(\delta^\text{EM}_n-\delta^\text{EM}_p)$ and evaluates it as $+2.51-1.00=+1.51$ MeV. Exactly one statement is now available: **one of those two terms is wrong by 0.217 MeV** — 8.6% of the strong term, or 21.7% of the electromagnetic one. The EM term is the more likely culprit on size grounds: it is a 1.00 MeV Coulomb self-energy difference estimated from a constituent-quark charge distribution, and 22% is an ordinary error for that estimate, whereas 8.6% on the F40 current-quark gap would move $m_d/m_u$ outside its PDG range. That is an actionable target, not a verdict.

**The sign is still right, and that was F122's real claim.** F122 said the down–up gap must beat EM and it does. Nothing here touches that. What changes is the tolerance the prediction is held to.

---

## 6. What BBN cannot see: the deuteron binding

$B_d$ is *reproduced* at 0.026%, not predicted parameter-free — $b=0.55$ fm is fixed to the binding (rubric G6). The honest question is whether BBN could tell the model's $B_d$ from the measured one. It cannot:

| | value |
|---|---|
| $B_d$ model $-$ PDG | $-0.026\%$ |
| resulting D/H shift | $+2.3\times10^{-8}$, i.e. $+0.078\sigma$ of Cooke 2018 |
| D/H sensitivity | $-9.0\times10^{-7}$ per 1% in $B_d$ |

So the deuterium bottleneck is **not** where this model is being tested, and a future parameter-free $B_d$ would have to beat $\sim0.4\%$ to be checked here at all. Worth recording precisely because it is a null: it stops a later session citing "BBN confirms the derived deuteron binding", which BBN does not do.

---

## 7. Check battery

`check_k2()`, 12 checks, all PASS. Every one can fail, and the record declares the perturbation under which two of them do.

| # | Check | Value | Verdict |
|---|---|---|---|
| K2-1 | network reproduces reference $Y_p$ to 3% | $-0.87\%$ | PASS |
| K2-2 | network reproduces reference D/H to 5% | $+0.55\%$ | PASS |
| K2-3 | $T_\nu/T_\gamma\to(4/11)^{1/3}$ from entropy alone | $6.0\times10^{-5}$ | PASS |
| K2-4 | detailed balance emerges, not imposed | $5.0\times10^{-5}$ | PASS |
| K2-5 | $N_\text{eff}$ within $1\sigma$ of Planck | $+0.32\sigma$ | PASS |
| K2-6 | energy-only law excluded by $Y_p$ at $>5\sigma$ | $-17.6\sigma$ | PASS |
| K2-7 | full-tensor law consistent within $2\sigma$ | $-0.11\sigma$ | PASS |
| K2-8 | BBN bounds $\Delta m$ $\ge100\times$ tighter than F122's 1 MeV | $0.0056$ MeV | PASS |
| K2-9 | model $\Delta m=1.51$ excluded at $>5\sigma$ | $-36.6\sigma$ | PASS |
| K2-10 | model $B_d$ invisible to D/H ($<0.2\sigma$) | $0.078\sigma$ | PASS |
| K2-11 | run at the swept $\Delta m$ matches $Y_p$ within $2\sigma$ | $-0.11\sigma$ | PASS |
| K2-12 | run at the swept $\Delta m$ matches D/H within $3\sigma$ | $-1.81\sigma$ | PASS |

**Declared failure mode.** `casim test --id F297-bbn-light-elements --param delta_m_mev=1.51` re-runs the battery at the model's own splitting and returns **10/12, RED on K2-11 and K2-12** ($-36.6\sigma$, $-22.6\sigma$). The record therefore has a named perturbation that makes it fail, which is what the 2026-08-04 report's gap #2 asks of every `kind: assertion` record.

---

## 8. Input ledger

Enumerated in `input_ledger()` so no reader has to reconstruct it.

**Model-native:** $G$ (F79/F107); the source law (F178); $\dot G/G\equiv0$ (F79/F284); $N_\text{eff}=3.044$ (F47/F165/F253); $\Delta m$ (F122/F123); $B_d$ (F104/F113/F126/F240, one tuned parameter).

**External input, not derived and not claimed:** $\eta_{10}=6.137$ (Planck; F202 derives no asymmetry number — rubric K6); $|V_{ud}|$ (CKM out of scope, ledger 10–13); $G_F$ (carries the $v$ anchor, ledger 17); the measured $\tau_n$, used *only* to fix the weak coupling $K$; the eleven non-$pn$ reaction rates (Smith–Kawano–Malaney 1993); the $t$, $^3$He, $^4$He, $^7$Li, $^7$Be binding energies.

One coupling cross-check worth recording: computing $K$ from the model's own $G_F$ and the registry $g_A$ (plus external $|V_{ud}|$) gives $\tau_n=948$ s against 878.4 measured, $+7.9\%$ — the expected size of the omitted Coulomb and radiative corrections ($f=1.6295\to1.7152$ is $+5.3\%$). The coupling side is sound; the $\Delta m$ side is not.

---

## 9. Verdict

> **K2 closes as a falsifier, not as a confirmation.** Assembled from parts the tree already owned, the model reproduces the light elements: $Y_p$ within $0.11\sigma$ of Aver 2021 and D/H within $1.8\sigma$ of Cooke 2018 on a structurally derived $G$, an exactly constant $G$, and a zero-freedom $N_\text{eff}=3.044$ — with $\eta_b$ the single external input, as it is in standard BBN. BBN then independently confirms the F178 law choice, excluding the demoted energy-only reading at $17.6\sigma$ on an observable unrelated to the neutron-star argument that decided it. And it turns the sharpest matter-sector prediction into the tightest-constrained one: $m_n-m_p$ is measured to $\pm0.0056$ MeV where F122 checked it to $\pm1$ MeV, and the model's $+1.51$ MeV is excluded at $38.7\sigma$ by helium and by a factor 2.7 in the free-neutron lifetime. The sign F122 actually claimed survives; the value does not, and one of its two terms is wrong by 0.217 MeV.

**Grade sought:** K2 `ABSENT → PARTIAL`. Not `QUANT`: $\eta_b$ is an external input by construction (K6/F202), the $A=7$ chain is not validated, and the network's own $\sim1\%$ absolute offset is carried on every absolute number.

## 10. Open / next

1. **Fix the EM self-energy in F122**, or show the F40 gap moves — the 0.217 MeV is now a specific target with a $\pm0.0056$ MeV acceptance band.
2. **Repair the $A=7$ rate fits** and only then say anything about lithium.
3. **Reduce the network's 0.87% absolute offset** (finite $T$–grid, no radiative/Coulomb corrections to the weak rates, no finite-nucleon-mass terms) if any *absolute* abundance is ever to be claimed.
4. **F283/F284 can be upgraded**: they quote the BBN $\dot G/G$ bound; with an abundance code in the tree, $\dot G/G\equiv0$ can be stated as a prediction that BBN confirms rather than a bound that is met.
